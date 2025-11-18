# services/chat.py
import time
import json
import math
import os
from typing import Dict, Any, List, Optional
from sentence_transformers import SentenceTransformer
from sqlite_vec import serialize_float32

from db import get_db
from api.nlu_optimized import detect_language, classify_intent, extract_entities
from services.async_translator import get_async_translator
from services.indic_translation_service import get_indic_translation_service
from services.response_builder import (
    build_generic_answer,
    build_no_data_answer,
    build_plant_answer,
    build_remedy_answer,
)
from api.context import get_last_context, persist_turn
from semantic import top_plants_for_disease, top_preparations_for_disease, ingredients_for_preparation

# Global embedding model (lazy loaded)
_EMB_MODEL = None
_SENTENCE_MODEL_NAME = os.getenv("SENTENCE_MODEL_NAME", "all-MiniLM-L6-v2")
_SENTENCE_MODEL_CACHE = os.getenv("SENTENCE_MODEL_CACHE")  # e.g., /data/models/sentencetransformers

# ============================================================================
# HELPERS
# ============================================================================

def _as_list(x):
    """Parse JSON array or return as-is"""
    if not x:
        return None
    if isinstance(x, list):
        return x
    try:
        v = json.loads(x)
        return v if isinstance(v, list) else None
    except Exception:
        return None

def _l2_normalize(v: List[float]) -> List[float]:
    """L2 normalize vector for cosine similarity"""
    s = math.sqrt(sum(x*x for x in v)) or 1.0
    return [x / s for x in v]

def _embed_384(text: str) -> bytes:
    """Generate 384-dim embedding using all-MiniLM-L6-v2"""
    global _EMB_MODEL
    if _EMB_MODEL is None:
        if _SENTENCE_MODEL_CACHE:
            print(f"[Embeddings] Loading {_SENTENCE_MODEL_NAME} with cache at {_SENTENCE_MODEL_CACHE}")
            _EMB_MODEL = SentenceTransformer(_SENTENCE_MODEL_NAME, cache_folder=_SENTENCE_MODEL_CACHE)
        else:
            print(f"[Embeddings] Loading {_SENTENCE_MODEL_NAME} (default cache)")
            _EMB_MODEL = SentenceTransformer(_SENTENCE_MODEL_NAME)
    v = _EMB_MODEL.encode(text).astype("float32").tolist()
    v = _l2_normalize(v)
    return serialize_float32(v)


def _prioritize_name_match(items: List[Dict], query: str, keys: List[str]) -> List[Dict]:
    """Bring exact/partial name matches to the front of the list."""
    if not items or not query:
        return items

    q = query.lower().strip()

    def score(item: Dict) -> int:
        names = []
        for key in keys:
            if not isinstance(item, dict):
                continue
            value = item.get(key)
            if isinstance(value, str):
                names.append(value.lower())
            elif isinstance(value, list):
                names.extend(v.lower() for v in value if isinstance(v, str))
        if not names:
            return 3
        if any(q == name for name in names):
            return 0
        if any(name.startswith(q) or q in name for name in names):
            return 1
        return 2

    return sorted(items, key=score)

# Optional preload to avoid first-request download latency
if os.getenv("SENTENCE_PRELOAD", "0") == "1":
    try:
        _ = _embed_384("warmup")
        print("[Embeddings] Preloaded successfully")
    except Exception as e:
        print(f"[Embeddings] Preload failed: {e}")

# ============================================================================
# DATABASE RETRIEVAL
# ============================================================================

def _search_similar_vec(table: str, id_col: str, qtext: str, k: int = 3) -> List[Dict]:
    """Vector similarity search using sqlite-vec"""
    db = get_db()
    qv = _embed_384(qtext)
    sql = f"""
        SELECT {id_col} AS id, distance
        FROM {table}
        WHERE embedding MATCH ?
          AND k = ?
    """
    try:
        return [dict(r) for r in db.execute(sql, (qv, k)).fetchall()]
    except Exception as e:
        print(f"[Vector search error] {e}")
        return []

def _fetch_plant_full(plant_id: int) -> Optional[Dict]:
    """Fetch complete plant record"""
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
    
    row = db.execute("""
        SELECT id, common_name_en, common_name_hi, common_name_mr,
               botanical_name, description, parts_used,
               therapeutic_actions, rasa, virya, vipaka, guna, dosha_effect,
               image_hero
        FROM plants
        WHERE id = ?
    """, (plant_id,)).fetchone()
    
    if not row:
        return None
    
    # Parse JSON fields
    for k in ["parts_used", "therapeutic_actions", "rasa", "guna", "dosha_effect"]:
        if row.get(k):
            row[k] = _as_list(row[k])
    
    return row

def _fetch_disease_full(disease_id: int) -> Optional[Dict]:
    """Fetch complete disease record"""
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
    
    row = db.execute("""
        SELECT id, name_en, name_hi, name_mr, category,
               description, symptoms, causes, dosha_involvement,
               severity_level, prevention_tips
        FROM diseases
        WHERE id = ?
    """, (disease_id,)).fetchone()
    
    if not row:
        return None
    
    # Parse JSON fields
    for k in ["symptoms", "causes", "dosha_involvement", "prevention_tips"]:
        if row.get(k):
            row[k] = _as_list(row[k])
    
    return row

def _diseases_for_plant(plant_id: int, k: int = 5) -> List[Dict]:
    """Get diseases that a plant can treat"""
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
    
    rows = db.execute("""
        SELECT d.id, d.name_en, d.name_hi, d.name_mr, d.category, d.description,
               pdm.efficacy_level, pdm.evidence_type, pdm.mechanism
        FROM plant_disease_mapping pdm
        JOIN diseases d ON d.id = pdm.disease_id
        WHERE pdm.plant_id = ?
        ORDER BY pdm.efficacy_level DESC
        LIMIT ?
    """, (plant_id, k)).fetchall()
    
    return rows

def _prune_vec_hits(hits: List[Dict], max_distance: float) -> List[Dict]:
    """Filter out weak vector matches"""
    return [h for h in hits if "distance" not in h or (h.get("distance", 999) <= max_distance)]

# ============================================================================
# KNOWLEDGE CONTEXT BUILDING
# ============================================================================

def build_knowledge_context(
    plants: List[Dict],
    diseases: List[Dict],
    lang: str
) -> str:
    """
    Build compact, structured knowledge context for LLM
    This replaces the need for translation - LLM gets facts in English
    and responds in user's language
    """
    context_parts = []
    
    # === PLANTS SECTION ===
    if plants:
        context_parts.append("=== MEDICINAL PLANTS ===")
        for p in plants[:3]:  # Limit to top 3
            name_en = p.get("common_name_en", "")
            botanical = p.get("botanical_name", "")
            desc = (p.get("description") or "")[:200]
            actions = p.get("therapeutic_actions", [])
            
            context_parts.append(f"\n**{name_en}** ({botanical})")
            if desc:
                context_parts.append(f"Description: {desc}")
            if actions:
                if isinstance(actions, list):
                    context_parts.append(f"Therapeutic Actions: {', '.join(actions[:5])}")
                else:
                    context_parts.append(f"Therapeutic Actions: {actions}")
            
            # Ayurvedic properties
            props = []
            rasa = p.get("rasa")
            if rasa:
                if isinstance(rasa, list):
                    props.append(f"Rasa: {', '.join(rasa[:3])}")
                else:
                    props.append(f"Rasa: {rasa}")
            
            if p.get("virya"):
                props.append(f"Virya: {p['virya']}")
            
            if p.get("vipaka"):
                props.append(f"Vipaka: {p['vipaka']}")
            
            dosha = p.get("dosha_effect")
            if dosha and isinstance(dosha, dict):
                dosha_str = ", ".join([f"{k}: {v}" for k, v in dosha.items()])
                props.append(f"Dosha Effect: {dosha_str}")
            
            if props:
                context_parts.append(" | ".join(props))
    
    # === DISEASES SECTION ===
    if diseases:
        context_parts.append("\n\n=== MEDICAL CONDITIONS ===")
        for d in diseases[:2]:  # Limit to top 2
            name = d.get("name_en", "")
            category = d.get("category", "")
            desc = (d.get("description") or "")[:150]
            symptoms = d.get("symptoms", [])
            
            context_parts.append(f"\n**{name}** ({category})")
            if desc:
                context_parts.append(f"Description: {desc}")
            if symptoms and isinstance(symptoms, list):
                context_parts.append(f"Symptoms: {', '.join(symptoms[:5])}")
    
    return "\n".join(context_parts)

def build_remedy_context(disease_row: Dict) -> str:
    """Build context for remedy recommendations"""
    d_id = disease_row["id"]
    plants = top_plants_for_disease(d_id, k=5)
    preps = top_preparations_for_disease(d_id, k=3)
    
    parts = []
    
    # Disease info
    parts.append(f"=== CONDITION: {disease_row.get('name_en', '')} ===")
    if disease_row.get("description"):
        parts.append(f"Description: {disease_row['description'][:200]}")
    
    # Recommended plants
    if plants:
        parts.append("\n=== RECOMMENDED HERBS ===")
        for i, p in enumerate(plants[:5], 1):
            name = p.get("common_name_en") or p.get("botanical_name")
            botanical = p.get("botanical_name", "")
            efficacy = p.get("efficacy_level", "")
            evidence = p.get("evidence_type", "")
            
            parts.append(f"{i}. {name} ({botanical})")
            if efficacy:
                parts.append(f"   Efficacy: {efficacy}/5")
            if evidence:
                parts.append(f"   Evidence: {evidence}")
            
            # Add therapeutic actions if available
            actions = p.get("therapeutic_actions")
            if actions:
                if isinstance(actions, list):
                    parts.append(f"   Actions: {', '.join(actions[:3])}")
    
    # Preparations
    if preps:
        parts.append("\n=== PREPARATIONS ===")
        for pr in preps[:3]:
            name = pr.get("name_en", "")
            form = pr.get("form_type", "")
            parts.append(f"\n**{name}** ({form})")
            
            # Ingredients
            ings = ingredients_for_preparation(pr["id"])
            if ings:
                ing_list = []
                for ing in ings[:5]:
                    qty = f"{ing.get('quantity_value', '')} {ing.get('quantity_unit', '')}".strip()
                    ing_name = ing.get("common_name_en", ing.get("botanical_name", ""))
                    if qty:
                        ing_list.append(f"{ing_name} ({qty})")
                    else:
                        ing_list.append(ing_name)
                parts.append(f"Ingredients: {', '.join(ing_list)}")
            
            # Dosage
            dosage = pr.get("dosage_json")
            if dosage:
                if isinstance(dosage, str):
                    try:
                        dosage = json.loads(dosage)
                    except:
                        pass
                if isinstance(dosage, dict):
                    parts.append(f"Dosage: Adult - {dosage.get('adult', 'As prescribed')}")
            
            # Timing & Anupana
            if pr.get("timing"):
                parts.append(f"Timing: {pr['timing']}")
            if pr.get("anupana"):
                parts.append(f"Anupana: {pr['anupana']}")
    
    return "\n".join(parts)


# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_pipeline(user_text: str, session_id: str | None) -> Dict[str, Any]:
    """
    Optimized multilingual RAG pipeline:
    1. Detect language & intent (fast)
    2. Extract entities with FTS + vector fallback
    3. Build knowledge context
    4. Single LLM call for multilingual response
    5. Return structured result
    """
    t0 = time.time()
    
    # Step 1: Language detection (no translation yet)
    lang = detect_language(user_text)
    print(f"[Pipeline] Language: {lang}")
    translator = None
    async_tx = get_async_translator()

    # Step 2: Translate ONLY for intent classification (internal routing)
    # Keep best-effort: if the heavy model is still loading, skip to avoid blocking.
    text_for_intent = user_text
    if lang != "en":
        if async_tx.is_ready():
            try:
                translator = get_indic_translation_service()
                text_for_intent = translator.to_en(user_text, src_lang=lang)
                print(f"[Translate] Query -> EN (intent): {text_for_intent}")
            except Exception as exc:
                print(f"[Translate] Skipping intent translation: {exc}")
        else:
            async_tx.warmup()
            print("[Translate] Translator warming up; using original text for intent")
    intent = classify_intent(text_for_intent)
    print(f"[Pipeline] Intent: {intent} (text_for_intent={text_for_intent})")
    
    # Step 3: Entity extraction (works on original multilingual query)
    plants, diseases = extract_entities(user_text, text_for_intent, prefer_en=(lang != "en"))
    print(f"[Pipeline] Found {len(plants)} plants, {len(diseases)} diseases (FTS)")

    name_hint = text_for_intent or user_text
    plants = _prioritize_name_match(
        plants, name_hint, ["common_name_en", "botanical_name", "synonym", "name"]
    )
    diseases = _prioritize_name_match(
        diseases, name_hint, ["name_en", "name", "synonym"]
    )
    
    # Step 4: Vector fallback if FTS didn't find anything
    if not diseases:
        vec_diseases = _search_similar_vec("disease_vec", "disease_id", user_text, 3)
        vec_diseases = _prune_vec_hits(vec_diseases, 1.8)  # Tune threshold
        print(f"[Pipeline] Found {len(vec_diseases)} diseases (vector)")
        diseases = vec_diseases
    
    if not plants:
        vec_plants = _search_similar_vec("plant_vec", "plant_id", user_text, 3)
        vec_plants = _prune_vec_hits(vec_plants, 1.8)
        print(f"[Pipeline] Found {len(vec_plants)} plants (vector)")
        plants = vec_plants
    
    # Step 5: Hydrate entities (fetch full records if we only have IDs)
    plants_full = []
    for p in plants[:3]:  # Limit to top 3
        if "botanical_name" in p and p.get("botanical_name"):
            plants_full.append(p)
        elif "id" in p:
            full = _fetch_plant_full(p["id"])
            if full:
                plants_full.append(full)
    
    diseases_full = []
    for d in diseases[:3]:
        if "name_en" in d and d.get("name_en"):
            diseases_full.append(d)
        elif "id" in d:
            full = _fetch_disease_full(d["id"])
            if full:
                diseases_full.append(full)
    
    # Step 6: Context recall from conversation
    last = get_last_context(session_id) if session_id else None
    if not diseases_full and last and last.get("entities", {}).get("diseases"):
        diseases_full = last["entities"]["diseases"][:2]
    if not plants_full and last and last.get("entities", {}).get("plants"):
        plants_full = last["entities"]["plants"][:2]
    if intent == "none" and last:
        intent = last.get("intent", "none")

    # Heuristic: if the query text implies "for <condition>" and we found diseases,
    # prefer remedy_lookup even if the classifier leaned plant_info.
    text_lower = (text_for_intent or user_text).lower()
    if intent != "remedy_lookup" and diseases_full:
        if any(needle in text_lower for needle in [" साठी", "साठी", "के लिए", "for "]):
            intent = "remedy_lookup"
    
    print(f"[Pipeline] After hydration: {len(plants_full)} plants, {len(diseases_full)} diseases")
    
    # Step 7: Deterministic response generation (no external LLM)
    
    tructured: Dict[str, Any] = {}
    answer_text_en = ""

    if intent in ("remedy_lookup", "preparation_info") and diseases_full:
        disease_row = diseases_full[0]
        structured = {
            "disease": disease_row,
            "plants": top_plants_for_disease(disease_row["id"], k=5),
            "preparations": top_preparations_for_disease(disease_row["id"], k=3),
        }
        answer_text_en = build_remedy_answer(
            disease_row,
            structured["plants"],
            structured["preparations"],
        )

    elif intent == "plant_info" and plants_full:
        plant = plants_full[0]
        structured = {
            "plant": plant,
            "plants": [plant],
        }
        answer_text_en = build_plant_answer(plant)

    elif plants_full or diseases_full:
        structured = {
            "plants": plants_full,
            "diseases": diseases_full,
        }
        answer_text_en = build_generic_answer(plants_full, diseases_full)

    else:
        structured = {}
        answer_text_en = build_no_data_answer(user_text)

    print(f"[Pipeline] Answer (en): {answer_text_en}")

    answer_text = answer_text_en
    structured_local = structured
    if lang != "en":
        translated = None

        # First, try async with a short timeout
        try:
            translated = async_tx.translate_async(
                answer_text_en, lang, timeout=3000, warm_timeout=8
            )
        except Exception as exc:  # pragma: no cover - runtime failure guard
            print(f"[Translation] Async worker error: {exc}")

        # If async timed out/failed, fall back to sync translate (model should be warm by now)
        if not translated:
            try:
                translator = translator or get_indic_translation_service()
                translated = translator.translate_text(answer_text_en, "en", lang)
                print("[Translation] Used sync translator after async timeout")
            except Exception as exc:
                print(f"[Translation] Sync fallback failed: {exc}")

        if translated:
            answer_text = translated
            print(f"[Translation] Answer ({lang}): {answer_text}")
            try:
                translator = translator or get_indic_translation_service()
                if structured and os.getenv("TRANSLATE_STRUCTURED_JSON", "0") == "1":
                    print("[Translation] Translating structured payload...")
                    structured_local = translator.translate_values(structured, "en", lang)
                    print("[Translation] Structured payload translated")
                else:
                    structured_local = structured
                    print("[Translation] Skipped structured payload translation")
            except Exception as exc:
                print(f"[Translation] Structured fallback: {exc}")
                structured_local = structured
        else:
            print("[Translation] Falling back to English response (timeout or error)")
    else:
        print("[Translation] Skipped; language is en")

    # Step 8: Persist conversation
    entities_dump = {
        "plants": plants_full,
        "diseases": diseases_full
    }

    duration_ms = int((time.time() - t0) * 1000)
    persist_turn(
        session_id or "default",
        user_text,
        lang,
        intent,
        entities_dump,
        answer_text,
        structured_local,
        duration_ms
    )
    print(f"[Pipeline] Complete in {duration_ms}ms")

    return {
        "answer": answer_text,
        "intent": intent,
        "detected_language": lang,
        "structured": structured_local,
        "metadata": {
            "session_id": session_id,
            "duration_ms": duration_ms,
            "entities_found": {
                "plants": len(plants_full),
                "diseases": len(diseases_full)
            }
        }
    }
