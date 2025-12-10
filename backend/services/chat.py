# services/chat.py
import time, logging
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
    build_plant_knowledge_snippet,
    build_disease_knowledge_snippet,
)
from api.context import get_last_context, persist_turn
from semantic import top_plants_for_disease, top_preparations_for_disease, ingredients_for_preparation

log = logging.getLogger("pipeline")


# Global embedding model (lazy loaded)
_EMB_MODEL = None
_SENTENCE_MODEL_NAME = os.getenv("SENTENCE_MODEL_NAME", "all-MiniLM-L6-v2")
_SENTENCE_MODEL_CACHE = os.getenv("SENTENCE_MODEL_CACHE")  # e.g., /data/models/sentencetransformers

# ============================================================================
# HELPERS
# ============================================================================

HERBOAI_SYSTEM_PROMPT = """
    You are HerboAI, an AI vaidya (AYUSH-based herbal assistant) that runs locally.

    GOAL:
    - Understand the user’s intention: 
    * plant information (identity, properties, uses),
    * disease/condition information,
    * Ayurvedic/herbal remedy advice,
    * or general wellness questions.
    - Use ONLY the factual herbal and disease knowledge given in the CONTEXT section.
    - Answer in a warm, conversational tone like a helpful Ayurvedic doctor, not like a FAQ page.
    - Always respond in the SAME LANGUAGE as the user’s query (Marathi, Hindi, or English).

    CONTEXT RULES:
    - The CONTEXT block contains trusted summaries of plants, diseases and preparations from validated AYUSH sources.
    - Never invent new plants, diseases, or preparations that are not present in the context.
    - If something is not present in the context, say that it is not available in the current HerboAI knowledge base.

    SAFETY & MEDICAL DISCLAIMER:
    - You are NOT a replacement for a doctor.
    - Do not give emergency or critical-care instructions.
    - For serious, worsening, or unclear symptoms, ALWAYS suggest consulting a qualified doctor or vaidyas in person.

    STYLE:
    - Start by briefly acknowledging the user’s need (e.g., “तुम्हाला मधुमेहासाठी आयुर्वेदिक उपाय जाणून घ्यायचे आहेत…”).
    - Use simple language appropriate for the user’s language (Marathi/Hindi/English).
    - When useful, organize the answer into small sections with headings, like:
    * वनस्पती माहिती / Plant Information
    * आयुर्वेदिक उपयोग / Ayurvedic Uses
    * तयारी आणि सेवन पद्धत / Preparation & Dosage
    * खबरदारी / Precautions
    - Keep dosage suggestions gentle and within traditional dietary / household ranges. 
    Never prescribe aggressive, high-dose, or toxic regimens.

    INTENT HANDLING:
    - If user mainly asks “what is this plant / गुणधर्म / uses”, focus on:
    * identity, rasa–guna–virya–vipaka, dosha effects, therapeutic actions, general household preparations.
    - If user mainly asks about a disease/condition, focus on:
    * short disease explanation + relevant lifestyle/diet + supporting herbs from context.
    - If user asks “उपाय/उपचार/remedy for X”, focus on:
    * a few key herbs from context, simple preparation steps, and safety notes.
    - If user query is vague/general, provide a balanced overview of any relevant plants/diseases from context.
    """.strip()

def build_herboai_context(
    plants: list,
    diseases: list,
    preparations: list,
) -> str:
    """
    Build a single context string passed to the LLM.
    `plants`, `diseases`, `preparations` are lists of dicts coming
    from your DB/retrieval layer.

    This is what gets embedded (via ETL) AND what gets fed back
    to the model at query time.
    """
    sections = []

    if plants:
        plant_lines = ["=== MEDICINAL PLANTS ==="]
        for p in plants:
            snippet = build_plant_knowledge_snippet(p)
            if snippet:
                plant_lines.append(snippet)
        sections.append("\n\n".join(plant_lines))

    if diseases:
        disease_lines = ["=== MEDICAL CONDITIONS ==="]
        for d in diseases:
            snippet = build_disease_knowledge_snippet(d)
            if snippet:
                disease_lines.append(snippet)
        sections.append("\n\n".join(disease_lines))

    if preparations:
        # You can refine this later into a dedicated builder.
        prep_lines = ["=== HERBAL PREPARATIONS ==="]
        for prep in preparations:
            name = prep.get("name") or prep.get("preparation_name") or "Unnamed preparation"
            form = prep.get("form") or prep.get("dosage_form")
            desc = prep.get("description") or ""
            line = name
            if form:
                line += f" ({form})"
            if desc:
                line += f": {desc}"
            prep_lines.append(line)
        sections.append("\n\n".join(prep_lines))

    return "\n\n".join(s for s in sections if s.strip())

def is_preparation_like_query(user_text: str, text_for_intent: str | None) -> bool:
    """
    Heuristic: detect queries asking 'how to prepare / kadha / decoction / churna' etc.
    Works on both the original text and the translated text_for_intent.
    """
    raw = (user_text or "").lower()
    intent_txt = (text_for_intent or "").lower()
    combined = raw + " " + intent_txt

    # English / transliterated preparation keywords
    prep_keywords_en = [
        "how to make", "how to prepare", "recipe", "method", "steps",
        "kadha", "kada", "kadhha",
        "kwath", "kwatha",
        "decoction", "kashaya", "kashayam",
        "churna", "powder", "tablet", "vati",
        "taila", "oil", "ghrita", "ghee",
        "lehyam", "avaleha", "arishta", "asava", "syrup",
    ]

    # A few direct Devanagari hints
    prep_keywords_local = [
        "काढा", "काढ़ा", "काढ़ा", "काढा कसा", "काढा कसा बनवायचा",
        "काढा कैसे", "काढ़ा कैसे", "कसे बनवायचे", "कसा बनवायचा",
    ]

    for kw in prep_keywords_en:
        if kw in combined:
            return True
    for kw in prep_keywords_local:
        if kw in combined:
            return True

    return False

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

_NAME_STOPWORDS = {
    "how", "to", "prepare", "make", "do", "use", "usage",
    "powder", "tablet", "decoction", "kwath", "kwatha", "kadha",
    "syrup", "capsule", "oil", "taila", "ghrita",
    "for", "of", "the", "a", "an", "is", "what", "tell", "me",
    "dosage", "dose"
}

def _simple_tokens(text: str) -> list[str]:
    """Lowercase a–z word tokens, skip very short / stopwords."""
    if not text:
        return []
    import re
    raw = re.findall(r"[a-zA-Z]+", text.lower())
    return [w for w in raw if len(w) >= 3 and w not in _NAME_STOPWORDS]

def _prioritize_name_match(items: List[Dict], query: str, keys: List[str]) -> List[Dict]:
    """
    Bring the most likely plant/disease to the front.

    Strategy:
    1) Extract meaningful tokens from the query (e.g. 'gudmar', 'neem', 'triphala').
    2) For each item, collect all name/synonym strings from `keys`.
    3) Score items by token overlap with those names.
       - More exact token matches => better score
       - Then partial (substring) matches
       - Fallback to old behaviour when no tokens match at all.
    """
    if not items or not query:
        return items

    q_tokens = _simple_tokens(query)
    if not q_tokens:
        # Nothing useful to score on -> keep original behaviour
        return items

    def gather_names(item: Dict) -> list[str]:
        names: list[str] = []
        for key in keys:
            val = item.get(key)
            if isinstance(val, str):
                names.append(val)
            elif isinstance(val, list):
                for v in val:
                    if isinstance(v, str):
                        names.append(v)
        return names

    def score_item(item: Dict) -> tuple[int, int, int]:
        """
        Lower score is better.
        return: (primary_rank, secondary_rank, fallback_rank)
        """
        names = gather_names(item)
        if not names:
            # No names to compare -> send to end
            return (3, 3, 3)

        # Tokenize all names
        name_tokens: set[str] = set()
        for n in names:
            for t in _simple_tokens(n):
                name_tokens.add(t)

        if not name_tokens:
            # Names exist but nothing tokenizable; treat as weak
            return (2, 3, 3)

        exact = 0
        partial = 0
        for q in q_tokens:
            if q in name_tokens:
                exact += 1
            elif any(q in t for t in name_tokens):
                partial += 1

        # If we have any exact matches, this is almost certainly the right plant.
        if exact > 0:
            return (0, -exact, -partial)  # more exact/partial -> smaller (better)
        # Next prefer partial substring matches
        if partial > 0:
            return (1, -partial, 0)

        # No overlap at all -> weak; keep order but behind others
        return (2, 0, 0)

    return sorted(items, key=score_item)

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

def _preparations_for_plant(plant_id: int, k: int = 5) -> List[Dict]:
    """Get preparations where this plant appears as an ingredient."""
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))

    rows = db.execute("""
        SELECT DISTINCT 
            p.id, p.name_en, p.name_hi, p.name_mr, p.classical_name,
            p.ayush_system,
            p.form_type, p.category,
            p.preparation_steps, p.equipment_needed, p.duration, p.yield, 
            p.storage, p.shelf_life,
            p.dosage_json, p.timing, p.anupana, p.notes
        FROM preparations p
        WHERE p.id IN (
            SELECT DISTINCT preparation_id 
            FROM preparation_ingredients pi
            WHERE pi.plant_id = ?
        )
        ORDER BY p.id
        LIMIT ?
    """, (plant_id, k)).fetchall()

    preps: List[Dict] = []
    for r in rows:
        d = dict(r)
        # Normalize JSON-ish fields
        for key in ["preparation_steps", "equipment_needed", "dosage_json"]:
            val = d.get(key)
            if isinstance(val, str):
                try:
                    d[key] = json.loads(val)
                except Exception:
                    d[key] = val
        preps.append(d)
    return preps


def _build_plant_preparation_answer(plant: Dict[str, Any], preps: List[Dict[str, Any]]) -> str:
    """Human-readable answer focused on how to prepare this plant's remedies."""
    name_en = plant.get("common_name_en") or plant.get("botanical_name") or "the plant"
    botanical = plant.get("botanical_name") or ""
    header = f"For **{name_en}**"
    if botanical:
        header += f" (_{botanical}_)"
    header += ", here are the preparations available in the HerboAI knowledge base:\n\n"

    if not preps:
        return (
            header
            + "Detailed step-by-step preparations are not yet stored for this plant in the database.\n"
              "You can still use it only under guidance of a qualified Ayurvedic practitioner."
        )

    lines: List[str] = [header]
    for i, prep in enumerate(preps, start=1):
        pname = prep.get("name_en") or prep.get("classical_name") or "Unnamed preparation"
        form = prep.get("form_type") or ""
        lines.append(f"{i}. **{pname}**" + (f" ({form})" if form else ""))

        # Steps
        steps = prep.get("preparation_steps")
        if isinstance(steps, list) and steps:
            lines.append("   • Preparation steps:")
            for idx, step in enumerate(steps[:8], start=1):
                if isinstance(step, str):
                    lines.append(f"     {idx}) {step.strip()}")

        # Dosage
        dosage = prep.get("dosage_json")
        if isinstance(dosage, dict):
            adult = dosage.get("adult")
            child = dosage.get("child")
            if adult or child:
                lines.append("   • Typical dosage (for general guidance):")
                if adult:
                    lines.append(f"     – Adult: {adult}")
                if child:
                    lines.append(f"     – Child: {child}")

        # Timing & Anupana
        if prep.get("timing"):
            lines.append(f"   • Timing: {prep['timing']}")
        if prep.get("anupana"):
            lines.append(f"   • Anupana: {prep['anupana']}")

        if prep.get("notes"):
            notes = prep["notes"]
            if isinstance(notes, str):
                lines.append(f"   • Notes: {notes.strip()}")

        lines.append("")  # Blank line between preparations

    lines.append(
        "⚠️ This information is for educational purposes only. "
        "Always confirm dosage and suitability with a qualified Ayurvedic practitioner."
    )
    return "\n".join(lines)

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
    4. Deterministic answer + translation (no external LLM yet)
    5. Return structured result
    """
    t0 = time.perf_counter()
    
    # Step 1: Language detection (no translation yet)
    lang = detect_language(user_text)
    print(f"[Pipeline] Language: {lang}")
    translator = None
    t1 = time.perf_counter()
    async_tx = get_async_translator()
    t2 = time.perf_counter()
    # Step 2: Translate ONLY for intent classification (internal routing)
    # Keep best-effort: if the heavy model is still loading, skip to avoid blocking.
    text_for_intent = user_text
    t3=t4=t5=0
    if lang != "en":
        if async_tx.is_ready():
            try:
                t3 = time.perf_counter()
                translator = get_indic_translation_service()
                t4 = time.perf_counter()
                text_for_intent = translator.to_en(user_text, src_lang=lang)
                t5 = time.perf_counter()
                print(f"[Translate] Query -> EN (intent): {text_for_intent}")
            except Exception as exc:
                print(f"[Translate] Skipping intent translation: {exc}")
        else:
            t3 = time.perf_counter()
            async_tx.warmup()
            t4 = time.perf_counter()
            print("[Translate] Translator warming up; using original text for intent")
            t5 = time.perf_counter()
    t6 = time.perf_counter()
    intent = classify_intent(text_for_intent)
    print(f"[Pipeline] Intent: {intent} (text_for_intent={text_for_intent})")
        # Heuristic override: if user is clearly asking "how to prepare / kadha / decoction / churna"
    # then treat this as preparation_info regardless of what the classifier said.
    if is_preparation_like_query(user_text, text_for_intent):
        print("[Heuristic] Overriding intent -> preparation_info (prep-like query)")
        intent = "preparation_info"

    
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
    plants_full: List[Dict[str, Any]] = []
    for p in plants[:3]:  # Limit to top 3
        if "botanical_name" in p and p.get("botanical_name"):
            plants_full.append(p)
        elif "id" in p:
            full = _fetch_plant_full(p["id"])
            if full:
                plants_full.append(full)
    
    diseases_full: List[Dict[str, Any]] = []
    for d in diseases[:3]:
        if "name_en" in d and d.get("name_en"):
            diseases_full.append(d)
        elif "id" in d:
            full = _fetch_disease_full(d["id"])
            if full:
                diseases_full.append(full)
    
    # Step 6: Context recall from conversation
        # Step 6: Context recall from conversation
    last = get_last_context(session_id) if session_id else None
    if not diseases_full and last and last.get("entities", {}).get("diseases"):
        diseases_full = last["entities"]["diseases"][:2]
    if not plants_full and last and last.get("entities", {}).get("plants"):
        plants_full = last["entities"]["plants"][:2]

    # Heuristic: if the query text implies "for <condition>" and we found diseases,
    # prefer remedy_lookup even if the classifier leaned plant_info.
    text_lower = (text_for_intent or user_text).lower()
    if intent != "remedy_lookup" and diseases_full:
        if any(needle in text_lower for needle in [" साठी", "साठी", "के लिए", "for "]):
            intent = "remedy_lookup"

    # >>> NEW: re-prioritize hydrated entities based on the actual names <<<
    name_hint = text_for_intent or user_text

    if plants_full:
        plants_full = _prioritize_name_match(
            plants_full,
            name_hint,
            [
                "common_name_en",
                "botanical_name",
                "common_name_hi",
                "common_name_mr",
                "sanskrit_name",
                "synonym",
                "name",
            ],
        )

    if diseases_full:
        diseases_full = _prioritize_name_match(
            diseases_full,
            name_hint,
            [
                "name_en",
                "name_hi",
                "name_mr",
                "ayurvedic_name",
                "synonym",
                "name",
            ],
        )

    print(f"[Pipeline] After hydration: {len(plants_full)} plants, {len(diseases_full)} diseases")
    
    # Step 7: Deterministic, chat-style response generation (no external LLM yet)
    
    structured: Dict[str, Any] = {}
    answer_text_en = ""

    # --- 7A: Preparation-info should be PLANT-centric when a plant is clear ---
    if intent == "preparation_info":
        if plants_full:
            plant = plants_full[0]
            preps = _preparations_for_plant(plant["id"], k=5)
            structured = {
                "plant": plant,
                "preparations": preps,
            }
            answer_text_en = _build_plant_preparation_answer(plant, preps)
        elif diseases_full:
            # Fallback: if user asked "how to prepare decoction for <disease>"
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
        else:
            structured = {}
            answer_text_en = build_no_data_answer(user_text)

    # --- 7B: Disease-centric remedy lookup ---
    elif intent == "remedy_lookup" and diseases_full:
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

    # --- 7C: Pure plant information ---
    elif intent == "plant_info" and plants_full:
        plant = plants_full[0]
        structured = {
            "plant": plant,
            "plants": [plant],
        }
        answer_text_en = build_plant_answer(plant)

    # --- 7D: Generic “I found some plants/diseases” answer ---
    elif plants_full or diseases_full:
        structured = {
            "plants": plants_full,
            "diseases": diseases_full,
        }
        answer_text_en = build_generic_answer(plants_full, diseases_full)

    # --- 7E: No entities at all ---
    else:
        structured = {}
        answer_text_en = build_no_data_answer(user_text)


    # Light conversational wrapper so it feels like an AI guide
    if answer_text_en:
        if intent == "plant_info":
            prefix = "Here is an Ayurvedic overview based on your question:\n\n"
        elif intent in ("remedy_lookup", "preparation_info"):
            prefix = (
                "Based on classical Ayurvedic references in the knowledge base, "
                "here is a concise guideline:\n\n"
            )
        else:
            prefix = ""
        if prefix:
            answer_text_en = prefix + answer_text_en

    print(f"[Pipeline] Answer (en): {answer_text_en}")
    t7 =0
    t8=0
    t9=0
    t10=0
    t11=0
    t12=0
    answer_text = answer_text_en
    structured_local = structured
    if lang != "en":
        translated = None

        # First, try async with a short timeout
        try:
            t7 = time.perf_counter()
            translated = async_tx.translate_async(
                answer_text_en, lang, timeout=3000, warm_timeout=8
            )
            t8 = time.perf_counter()
        except Exception as exc:  # pragma: no cover - runtime failure guard
            print(f"[Translation] Async worker error: {exc}")

        # If async timed out/failed, fall back to sync translate (model should be warm by now)
        if not translated:
            try:                
                translator = translator or get_indic_translation_service()
                t9 = time.perf_counter()
                translated = translator.translate_text(answer_text_en, "en", lang)
                t10 = time.perf_counter()
                print("[Translation] Used sync translator after async timeout")
            except Exception as exc:
                print(f"[Translation] Sync fallback failed: {exc}")

        if translated:
            answer_text = translated
            print(f"[Translation] Answer ({lang}): {answer_text}")
            try:
                translator = translator or get_indic_translation_service()
                t11 = time.perf_counter()
                if structured and os.getenv("TRANSLATE_STRUCTURED_JSON", "0") == "1":
                    print("[Translation] Translating structured payload.")
                    structured_local = translator.translate_values(structured, "en", lang)
                    print("[Translation] Structured payload translated")
                else:
                    structured_local = structured
                    print("[Translation] Skipped structured payload translation")
                t12 = time.perf_counter()
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

    log.info("timings(s): detect_language=%.2f get_async_translator=%.2f other=%.2f "
         "get_async_translator=%.2f translator.to_en=%.2f classify_intent=%.2f "
         "async_tx.translate_async=%.2f get_indic_translation_service=%.2f "
         "translator.translate_text=%.2f translate_values=%.2f total=%.2f",
         t1-t0, t2-t1, t3-t2, t4-t3, t5-t4, t7-t5, t8-t7, t9-t8, t10-t9, 
         (t11 - t10) if t10 != 0 else (t11 - t8), t12 - t0)
    
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
