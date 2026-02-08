# services/chat.py
import time, logging
import json
import math
import os
import re
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
from sentence_transformers import SentenceTransformer
from sqlite_vec import serialize_float32
import numpy as np

from db import get_db, fetch_preparations_for_disease, resolve_disease_id, rank_preparations_by_severity
from api.nlu_optimized import detect_language, classify_intent, extract_entities
from services.async_translator import get_async_translator
from services.indic_translation_service import get_indic_translation_service
from services.response_builder import (
    build_generic_answer,
    build_hybrid_response,
    build_no_data_answer,
    build_plant_answer,
    build_remedy_answer,
    build_plant_knowledge_snippet,
    build_disease_knowledge_snippet,
)
from services.llm_gateway import generate_herboai_answer

from api.context import get_last_context, persist_turn
from semantic import top_plants_for_disease, top_preparations_for_disease, ingredients_for_preparation

from services.severity import assess_severity
from services.followups import generate_followup_questions
from services.indic_translation_service import translate_to_en, translate_from_en
from repositories.search_repo import (
    vector_search_preparations_lang,
    hydrate_preparations,
    rank_preparations,
)
from utils.i18n import normalize_lang


log = logging.getLogger("pipeline")


# Global embedding model (lazy loaded)
_EMB_MODEL = None
_SENTENCE_MODEL_NAME = os.getenv("SENTENCE_MODEL_NAME", "all-MiniLM-L6-v2")
_SENTENCE_MODEL_CACHE = os.getenv("SENTENCE_MODEL_CACHE", str(Path(__file__).parent.parent / "models"))  # e.g., /data/models/sentencetransformers

def warmup_pipeline():
    """
    Warm up heavyweight components so first real request is not slow.
    Safe to call multiple times.
    """
    try:
        # 1) Translator (background loader)
        get_async_translator().warmup()

        # 2) IndicTranslationService (loads IndicTrans2 models)
        get_indic_translation_service()

        # 3) Embedding model (SentenceTransformer)
        global _EMB_MODEL
        if _EMB_MODEL is None:
            if _SENTENCE_MODEL_CACHE:
                _EMB_MODEL = SentenceTransformer(_SENTENCE_MODEL_NAME, cache_folder=_SENTENCE_MODEL_CACHE)
            else:
                _EMB_MODEL = SentenceTransformer(_SENTENCE_MODEL_NAME)

        # tiny warm query to compile/allocate CPU kernels
        _ = _EMB_MODEL.encode(["warmup"], normalize_embeddings=True)

        log.info("[Warmup] translator + embeddings warmed successfully")
    except Exception as e:
        log.exception(f"[Warmup] failed: {e}")


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
        "preparation", "prepare",  # Added: direct prep reference
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
        "बनव",  # generic verb stem 'to make' in Marathi/Hindi
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

def _embed_384_np(text: str) -> np.ndarray:
    """Return L2-normalized 384-dim embedding as float32 numpy array."""
    global _EMB_MODEL
    if _EMB_MODEL is None:
        if _SENTENCE_MODEL_CACHE:
            print(f"[Embeddings] Loading {_SENTENCE_MODEL_NAME} with cache at {_SENTENCE_MODEL_CACHE}")
            _EMB_MODEL = SentenceTransformer(_SENTENCE_MODEL_NAME, cache_folder=_SENTENCE_MODEL_CACHE)
        else:
            print(f"[Embeddings] Loading {_SENTENCE_MODEL_NAME} (default cache)")
            _EMB_MODEL = SentenceTransformer(_SENTENCE_MODEL_NAME)

    v = _EMB_MODEL.encode(text, convert_to_numpy=True).astype("float32")
    n = np.linalg.norm(v)
    if n > 0:
        v = v / n
    return v

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
    """Get preparations where this plant is used (either directly or as ingredient)."""
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))

    # Try to find preparations in two ways:
    # 1. Direct: preparations.plant_id = ?
    # 2. Via ingredients: preparation_ingredients.plant_id = ?
    rows = db.execute("""
        SELECT DISTINCT 
            p.id, p.name_en, p.name_hi, p.name_mr, p.classical_name,
            p.ayush_system,
            p.form_type, p.category,
            p.preparation_steps, p.equipment_needed, p.duration, p.yield, 
            p.storage, p.shelf_life,
            p.dosage_json, p.timing, p.anupana, p.notes
        FROM preparations p
        WHERE p.plant_id = ?
           OR p.id IN (
               SELECT DISTINCT preparation_id 
               FROM preparation_ingredients pi
               WHERE pi.plant_id = ?
           )
        ORDER BY p.id
        LIMIT ?
    """, (plant_id, plant_id, k)).fetchall()

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

def _fetch_knowledge_chunk(chunk_id: int) -> Optional[Dict[str, Any]]:
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
    row = db.execute(
        """
        SELECT id, entity_type, entity_id, section, content, source, embedding
        FROM knowledge_chunks
        WHERE id = ?
        """,
        (chunk_id,),
    ).fetchone()
    if not row:
        return None
    # embedding is left as bytes; we only decode when needed
    return row

def _search_knowledge_chunks(
    query: str,
    plants_full: List[Dict[str, Any]],
    diseases_full: List[Dict[str, Any]],
    k: int = 5,
) -> List[Dict[str, Any]]:
    """
    Python-only cosine similarity search over knowledge_chunks.embedding.
    No vec0 / sqlite-vec virtual table required.
    """
    if not query:
        return []

    db = get_db()
    db.row_factory = sqlite3.Row if False else db.row_factory  # keep whatever you have

    qvec = _embed_384_np(query)

    # Optional filtering by entities present in this turn
    plant_ids = [p.get("id") for p in plants_full if p.get("id")]
    disease_ids = [d.get("id") for d in diseases_full if d.get("id")]

    where_clauses = []
    params: list[Any] = []

    if plant_ids:
        placeholders = ",".join("?" for _ in plant_ids)
        where_clauses.append(f"(entity_type = 'plant' AND entity_id IN ({placeholders}))")
        params.extend(plant_ids)

    if disease_ids:
        placeholders = ",".join("?" for _ in disease_ids)
        where_clauses.append(f"(entity_type = 'disease' AND entity_id IN ({placeholders}))")
        params.extend(disease_ids)

    # Always allow some general knowledge chunks
    where_clauses.append("entity_type = 'general'")

    where_sql = " OR ".join(where_clauses)
    sql = f"""
        SELECT id, entity_type, entity_id, section, content, source, embedding
        FROM knowledge_chunks
        WHERE {where_sql}
    """

    rows = db.execute(sql, tuple(params)).fetchall()
    scored: list[tuple[float, Dict[str, Any]]] = []

    for row in rows:
        emb_bytes = row["embedding"]
        if not emb_bytes:
            continue
        vec = np.frombuffer(emb_bytes, dtype="float32")
        if vec.size != qvec.size:
            continue
        # assuming both normalized -> dot = cosine similarity
        sim = float(np.dot(qvec, vec))
        rdict = dict(row)
        rdict["score"] = sim
        scored.append((sim, rdict))

    scored.sort(key=lambda x: x[0], reverse=True)
    top = [r for _, r in scored[:k]]
    print(f"[RAG] knowledge_chunks: considered={len(scored)}, top={len(top)}")
    return top

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

def _chunks_to_context(chunks: List[Dict[str, Any]]) -> str:
    if not chunks:
        return ""
    lines = ["=== KNOWLEDGE CHUNKS ==="]
    for c in chunks:
        label = c.get("source") or c.get("section") or c.get("entity_type") or "HerboAI note"
        lines.append(f"[{label}] {c.get('content','').strip()}")
    return "\n\n".join(lines)

# ============================================================================
# MAIN PIPELINE
# ============================================================================

# -----------------------------------------------------------------------------
# Conversation state for follow-up Q/A (in-memory; good for single-user/dev)
# -----------------------------------------------------------------------------

_SESSION_TTL_SEC = 60 * 30  # 30 minutes
_SESSIONS: Dict[str, Dict[str, Any]] = {}

_SLOT_KEYS = ("duration", "trend", "pain_fever_severity", "age_gender", "existing_illness")

def _now() -> float:
    return time.time()

def _gc_sessions() -> None:
    cutoff = _now() - _SESSION_TTL_SEC
    dead = [sid for sid, s in _SESSIONS.items() if s.get("updated_at", 0) < cutoff]
    for sid in dead:
        _SESSIONS.pop(sid, None)

def _get_session(session_id: Optional[str]) -> Dict[str, Any]:
    _gc_sessions()
    if not session_id:
        session_id = str(uuid.uuid4())
    sess = _SESSIONS.get(session_id)
    if not sess:
        sess = {
            "id": session_id,
            "stage": "new",        # new | collecting | ready
            "slots": {},
            "previous_slots": {},  # Track previous turn's slots to show only NEW info
            "last_q": None,
            "lang": None,
            "returned_prep_ids": set(),  # Track preparation IDs already returned
            "returned_plant_ids": set(),  # Track plant IDs already returned
            "asked_slots": set(),         # Track which SLOTS were asked (not question text)
            "updated_at": _now(),
        }
        _SESSIONS[session_id] = sess
    sess["updated_at"] = _now()
    return sess

def _classify_condition(text: str) -> str:
    """Classify health condition from text (supports English, Hindi, Marathi).
    
    Returns a condition code that determines:
      - Which followup slots to ask
      - How to map to disease names for DB lookup
      - Whether to treat as explicit-disease (skip slot-gating) or symptom-narrative
    """
    t = (text or "").lower()
    
    # Diabetes keywords: English + Hindi (मधुमेह) + Marathi (मधुमेह/साखर)
    if any(x in t for x in ("diabetes", "sugar", "मधुमेह", "साखर", "ब्लड शुगर", "ठराविक साखर")):
        return "diabetes"
    
    # Hypertension keywords: English + Hindi (उच्च रक्तदाब/दाब) + Marathi (रक्तदाब)
    if any(x in t for x in ("hypertension", "bp", "blood pressure", "उच्च रक्तदाब", "दाब", "रक्तदाब", "उच्च दाब")):
        return "hypertension"
    
    # Cold/Cough keywords
    if any(x in t for x in (
        "cold", "cough", "sore throat", "runny nose", "congestion",
        "जुकाम", "खोकला", "कफ", "नाक बहना", "गले में खराश",
        "सर्दी", "खोकी", "घसरघस", "नाक वाहणे", "गळ्याला खरास"
    )):
        return "cold_cough"
    
    # Digestion/Acidity keywords
    if any(x in t for x in (
        "acidity", "gas", "indigestion", "heartburn", "bloating",
        "अम्लपित्त", "गॅस", "अपचन", "पेट में जलन",
        "पोटात जळजळ", "बद्धकोष्ठ", "कब्ज", "constipation",
        "diarrhea", "अतिसार", "दस्त", "loose motion"
    )):
        return "digestion"
    
    # Arthritis/Joint pain keywords
    if any(x in t for x in (
        "arthritis", "joint pain", "joint", "knee pain", "back pain",
        "संधिवात", "गुडघा दुखी", "कमर दर्द", "जोड़ों का दर्द",
        "सांधेदुखी", "गुडघ्याचा दुखी", "पीठीचा दुखी", "संधिरोग",
        "जोडदुखी"
    )):
        return "arthritis"

    # ── Skin conditions (NEW — includes acne/pimples/मुरुम) ──
    if any(x in t for x in (
        "acne", "pimple", "पिंपल", "मुरुम", "मुंहासे", "फुंसी",
        "eczema", "एक्जिमा", "psoriasis", "सोरायसिस",
        "skin", "त्वचा", "rash", "खरुज", "खाज", "खुजली",
        "itching", "fungal", "बुरशी", "vitiligo", "पांढरे डाग",
        "dark spot", "काळे डाग", "pigmentation",
        "ringworm", "दाद", "urticaria", "अंगावर उठणे",
        "dermatitis", "त्वचारोग", "boil", "गळू"
    )):
        return "skin"
    
    # ── Hair conditions (NEW) ──
    if any(x in t for x in (
        "hair fall", "hair loss", "केस गळ", "बाल झड", "alopecia",
        "baldness", "टक्कल", "dandruff", "कोंडा", "रूसी",
        "grey hair", "पांढरे केस", "सफेद बाल"
    )):
        return "hair"
    
    # ── Respiratory (beyond cold/cough) ──
    if any(x in t for x in (
        "asthma", "दमा", "श्वास", "breathing", "bronchitis",
        "sinusitis", "सायनस", "nasal", "नाक बंद"
    )):
        return "respiratory"
    
    # ── Fever ──
    if any(x in t for x in (
        "fever", "ज्वर", "बुखार", "ताप", "flu", "इन्फ्लूएंजा"
    )):
        return "fever"
    
    # ── Mental health / stress ──
    if any(x in t for x in (
        "anxiety", "चिंता", "stress", "तणाव", "depression", "नैराश्य",
        "insomnia", "अनिद्रा", "झोप न येणे", "नींद न आना",
        "sleep", "memory", "स्मरणशक्ती", "याददाश्त"
    )):
        return "mental_health"
    
    # ── Urinary / kidney ──
    if any(x in t for x in (
        "kidney", "किडनी", "मूत्रपिंड", "stone", "पथरी", "खडे",
        "urine", "लघवी", "पेशाब", "uti"
    )):
        return "urinary"
    
    # ── Liver ──
    if any(x in t for x in (
        "liver", "यकृत", "जिगर", "लिव्हर",
        "jaundice", "कावीळ", "पीलिया", "fatty liver"
    )):
        return "liver"
    
    # ── Women's health ──
    if any(x in t for x in (
        "periods", "मासिक पाळी", "माहवारी", "menstrual",
        "pcos", "pcod", "पीसीओएस", "menopause", "रजोनिवृत्ती",
        "leucorrhea", "श्वेतप्रदर"
    )):
        return "womens_health"
    
    # ── Pain (generic) ──
    if any(x in t for x in (
        "headache", "डोकेदुखी", "सिरदर्द", "migraine", "मायग्रेन",
        "pain", "दुखी", "दर्द", "वेदना", "सूज", "inflammation"
    )):
        return "pain"
    
    # ── Metabolic / blood ──
    if any(x in t for x in (
        "anemia", "अॅनिमिया", "रक्ताची कमी", "weakness", "अशक्तपणा",
        "obesity", "लठ्ठपणा", "मोटापा", "weight", "cholesterol",
        "कोलेस्टेरॉल", "thyroid", "थायरॉइड"
    )):
        return "metabolic"
    
    # ── Piles / fistula ──
    if any(x in t for x in (
        "piles", "मूळव्याध", "बवासीर", "fistula", "भगंदर",
        "hemorrhoid"
    )):
        return "piles"
    
    # ── Allergy ──
    if any(x in t for x in (
        "allergy", "ऍलर्जी", "अलर्जी", "allergic"
    )):
        return "allergy"
    
    # Default to general
    return "general"

_CONDITION_SLOTS = {
    "diabetes": ("duration", "age_gender", "trend", "meds", "sugar_values"),
    "hypertension": ("duration", "age_gender", "trend", "meds", "bp_values"),
    "cold_cough": ("duration", "trend", "pain_fever_severity", "age_gender", "existing_illness"),
    "digestion": ("duration", "trend", "severity", "age_gender", "existing_illness"),
    "arthritis": ("duration", "trend", "severity", "age_gender", "existing_illness"),
    "skin": ("duration", "trend", "severity", "age_gender", "existing_illness"),
    "hair": ("duration", "trend", "age_gender", "existing_illness"),
    "respiratory": ("duration", "trend", "pain_fever_severity", "age_gender", "existing_illness"),
    "fever": ("duration", "trend", "pain_fever_severity", "age_gender", "existing_illness"),
    "mental_health": ("duration", "trend", "age_gender", "existing_illness"),
    "urinary": ("duration", "trend", "age_gender", "existing_illness"),
    "liver": ("duration", "trend", "age_gender", "existing_illness"),
    "womens_health": ("duration", "trend", "age_gender", "existing_illness"),
    "pain": ("duration", "trend", "severity", "age_gender", "existing_illness"),
    "metabolic": ("duration", "trend", "age_gender", "existing_illness"),
    "piles": ("duration", "trend", "severity", "age_gender", "existing_illness"),
    "allergy": ("duration", "trend", "severity", "age_gender", "existing_illness"),
    "general": ("duration", "trend", "pain_fever_severity", "age_gender", "existing_illness"),
}

# Required slots per condition (must be filled before "full guidance")
_CONDITION_REQUIRED = {
    "diabetes": ("duration", "age_gender", "trend"),
    "hypertension": ("duration", "age_gender", "trend"),
    "cold_cough": ("duration", "trend", "pain_fever_severity", "age_gender"),
    "digestion": ("duration", "trend", "severity", "age_gender"),
    "arthritis": ("duration", "trend", "severity", "age_gender"),
    "skin": ("duration",),  # Minimal — don't block remedy for simple queries
    "hair": ("duration",),
    "respiratory": ("duration", "trend", "age_gender"),
    "fever": ("duration", "trend", "pain_fever_severity", "age_gender"),
    "mental_health": ("duration", "age_gender"),
    "urinary": ("duration", "age_gender"),
    "liver": ("duration", "age_gender"),
    "womens_health": ("duration", "age_gender"),
    "pain": ("duration", "trend"),
    "metabolic": ("duration", "age_gender"),
    "piles": ("duration", "severity"),
    "allergy": ("duration",),
    "general": ("duration", "trend", "age_gender"),
}

# Optional slots (nice to have, NEVER block remedies)
_CONDITION_OPTIONAL = {
    "diabetes": ("meds", "sugar_values"),
    "hypertension": ("meds", "bp_values"),
    "cold_cough": ("existing_illness",),
    "digestion": ("existing_illness",),
    "arthritis": ("existing_illness",),
    "skin": ("trend", "severity", "age_gender", "existing_illness"),
    "hair": ("trend", "age_gender", "existing_illness"),
    "respiratory": ("existing_illness",),
    "fever": ("existing_illness",),
    "mental_health": ("trend", "existing_illness"),
    "urinary": ("trend", "existing_illness"),
    "liver": ("trend", "existing_illness"),
    "womens_health": ("trend", "existing_illness"),
    "pain": ("severity", "age_gender", "existing_illness"),
    "metabolic": ("trend", "existing_illness"),
    "piles": ("age_gender", "existing_illness"),
    "allergy": ("trend", "severity", "age_gender", "existing_illness"),
    "general": ("existing_illness",),
}


def _missing_required(sess: Dict[str, Any]) -> list[str]:
    slots = sess.get("slots", {})
    cond = sess.get("condition") or "general"
    required = _CONDITION_REQUIRED.get(cond, _CONDITION_REQUIRED["general"])
    return [k for k in required if k not in slots]

def _missing_optional(sess: Dict[str, Any]) -> list[str]:
    slots = sess.get("slots", {})
    cond = sess.get("condition") or "general"
    optional = _CONDITION_OPTIONAL.get(cond, ())
    return [k for k in optional if k not in slots]

def _slot_questions(condition: str | None, missing: list[str], lang: str = "en", sess: Dict = None) -> list[str]:
    qmap = {
        "en": {
            "duration": "Since when (days/months/years)?",
            "trend": "Is it getting better or worse?",
            "pain_fever_severity": "Any fever/pain severity (none / mild / moderate / severe)?",
            "severity": "Severity (mild / moderate / severe)?",
            "age_gender": "Age and gender?",
            "existing_illness": "Any existing illness (BP/thyroid/asthma etc.)?",
            "meds": "Are you currently taking any medicines? (name if possible)",
            "sugar_values": "Do you know your recent fasting/PP sugar or HbA1c? (optional)",
            "bp_values": "Do you know your recent BP readings? (optional)",
        },
        "hi": {
            "duration": "यह कितने दिन/महीने/साल से है?",
            "trend": "क्या यह बेहतर हो रहा है या बदतर?",
            "pain_fever_severity": "कोई बुखार/दर्द की गंभीरता (कोई नहीं / हल्का / मध्यम / गंभीर)?",
            "severity": "गंभीरता (हल्का / मध्यम / गंभीर)?",
            "age_gender": "उम्र और लिंग?",
            "existing_illness": "कोई मौजूदा बीमारी (BP/थायराइड/अस्थमा आदि)?",
            "meds": "क्या आप कोई दवा ले रहे हैं? (यदि संभव हो तो नाम)",
            "sugar_values": "क्या आप अपने हाल के उपवास/PP चीनी या HbA1c को जानते हैं? (वैकल्पिक)",
            "bp_values": "क्या आप अपने हाल के BP रीडिंग को जानते हैं? (वैकल्पिक)",
        },
        "mr": {
            "duration": "हे कितने दिवस/महीने/वर्षांपूर्वी आहे?",
            "trend": "हे बरेच चांगले होत आहे किंवा वाईट?",
            "pain_fever_severity": "कोणताही ताप/दर्द गंभीरता (नाही / हल्का / मध्यम / गंभीर)?",
            "severity": "गंभीरता (हल्का / मध्यम / गंभीर)?",
            "age_gender": "वय आणि लिंग?",
            "existing_illness": "कोणतीही विद्यमान रोग (BP/थायरॉईड/दमा इ.)?",
            "meds": "आप सध्या कोणतीही औषध घेत आहात? (शक्य असल्यास नाव)",
            "sugar_values": "तुम्हाला तुमच्या अलीकडील उपवास/PP साखरेची किंवा HbA1c माहिती आहे? (वैकल्पिक)",
            "bp_values": "तुम्हाला तुमच्या अलीकडील BP रीडिंग माहिती आहे? (वैकल्पिक)",
        },
    }

    lang = normalize_lang(lang)
    lang_map = qmap.get(lang, qmap["en"])
    
    # Track filled slots to avoid re-asking
    filled_slots = sess.get("slots", {}) if sess else {}
    
    questions = []
    for m in missing:
        # Skip if this slot was already filled (user answered it)
        if m in filled_slots:
            continue
            
        if m in lang_map:
            q = lang_map[m]
            questions.append(q)
    
    return questions


def _extract_slots(text: str) -> Dict[str, str]:
    """
    Enhanced slot extraction from natural user responses.
    Works with single answers like "2 months" or complete sentences.
    """
    t = (text or "").strip().lower()
    slots: Dict[str, str] = {}

    # duration: "2 years", "6 months", "10 days", or just "2 months" as single answer
    m = re.search(r"(\d+)\s*(year|years|yr|yrs|month|months|mo|mos|day|days|d)\b", t)
    if m:
        num = m.group(1)
        unit = m.group(2)
        # Normalize unit
        if unit.startswith('y'):
            unit = 'year' if num == '1' else 'years'
        elif unit.startswith('mo'):
            unit = 'month' if num == '1' else 'months'
        elif unit.startswith('d'):
            unit = 'day' if num == '1' else 'days'
        slots["duration"] = f"{num} {unit}"

    # trend
    if any(w in t for w in ("better", "improving", "improved", "getting better")):
        slots["trend"] = "improving"
    elif any(w in t for w in ("worse", "worsening", "getting worse", "deteriorating")):
        slots["trend"] = "worsening"
    elif "same" in t or "no change" in t or "stable" in t:
        slots["trend"] = "stable"

    # severity
    if "severe" in t:
        slots["pain_fever_severity"] = "severe"
    elif "moderate" in t:
        slots["pain_fever_severity"] = "moderate"
    elif "mild" in t:
        slots["pain_fever_severity"] = "mild"

    if "no fever" in t or "without fever" in t or "afebrile" in t:
        slots["pain_fever_severity"] = "none"
    if "no pain" in t or "without pain" in t:
        slots.setdefault("pain_fever_severity", "none")

    # meds
    if "metformin" in t or "insulin" in t or "glimepiride" in t or "gliclazide" in t:
        slots["meds"] = "mentioned"
    if "no medicine" in t or "not taking" in t:
        slots["meds"] = "none"

    # sugar values hints
    if "hba1c" in t:
        slots["sugar_values"] = "provided"
    if "fasting" in t or "pp" in t or "postprandial" in t:
        slots["sugar_values"] = "provided"

    # bp values hints
    if re.search(r"\b\d{2,3}\s*/\s*\d{2,3}\b", t):
        slots["bp_values"] = "provided"


    # age + gender (enhanced patterns)
    # e.g. "age 35 male", "35M", "female 28", "35 years, female", "28 f"
    m = re.search(r"\b(\d{1,3})\s*(m|male|f|female)\b", t)
    if m:
        age = m.group(1)
        gender = "male" if m.group(2) in ['m', 'male'] else "female"
        slots["age_gender"] = f"{age} years, {gender}"
    else:
        # Try to extract age and gender separately
        age_match = re.search(r"\b(\d{1,3})\s*(years?|yrs?)?\b", t)
        if age_match:
            age = age_match.group(1)
            # Look for gender anywhere in text
            if any(w in t for w in ["male", "man", "boy", " m ", "m,", "m."]):
                slots["age_gender"] = f"{age} years, male"
            elif any(w in t for w in ["female", "woman", "girl", " f ", "f,", "f."]):
                slots["age_gender"] = f"{age} years, female"

    # existing illness
    illness_hits = []
    for k in ("bp", "blood pressure", "diabetes", "thyroid", "asthma", "heart", "kidney", "liver"):
        if k in t:
            illness_hits.append(k)
    if illness_hits:
        slots["existing_illness"] = ", ".join(sorted(set(illness_hits)))

    return slots

def _detect_lang_stable(user_text: str, lang: str | None) -> str:
    # respect explicit lang, otherwise detect
    if lang:
        return normalize_lang(lang)
    try:
        return normalize_lang(detect_language(user_text))
    except Exception:
        return "en"


def _text_for_intent(user_text: str, lang: str) -> str:
    if lang == "en":
        return user_text
    try:
        result = translate_to_en(user_text, lang_hint=lang)
        if result == user_text and lang != "en":
            log.warning(f"[Translation Fallback] Marathi->EN translation returned original text for: {user_text[:50]}")
        return result
    except Exception as e:
        log.error(f"[Translation Error] Exception in translate_to_en: {e}", exc_info=True)
        return user_text


def _extract_plant_term(user_text_en: str, entities: dict | None) -> str | None:
    # best: NLU entities
    if isinstance(entities, dict):
        for key in ("plant", "plant_name", "herb", "entity"):
            v = entities.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip().lower()
            if isinstance(v, list) and v:
                if isinstance(v[0], str) and v[0].strip():
                    return v[0].strip().lower()

    # fallback: pick last meaningful token (works for "tulsi preparation")
    toks = _simple_tokens(user_text_en)
    return toks[-1].lower() if toks else None


def _find_plant_id_by_name(plant_term_en: str) -> int | None:
    if not plant_term_en:
        return None
    db = get_db()
    term = plant_term_en.strip().lower()

    row = db.execute(
        """
        SELECT id
        FROM plants
        WHERE LOWER(common_name_en)=?
           OR LOWER(botanical_name)=?
           OR LOWER(common_name_hi)=?
           OR LOWER(common_name_mr)=?
        LIMIT 1
        """,
        (term, term, term, term),
    ).fetchone()
    if row:
        return int(row["id"]) if isinstance(row, dict) else int(row[0])

    # fallback LIKE (safer but limited)
    row = db.execute(
        """
        SELECT id
        FROM plants
        WHERE LOWER(common_name_en) LIKE ?
           OR LOWER(botanical_name) LIKE ?
        LIMIT 1
        """,
        (f"%{term}%", f"%{term}%"),
    ).fetchone()
    if row:
        return int(row["id"]) if isinstance(row, dict) else int(row[0])

    return None


def _missing_slots(sess: Dict[str, Any]) -> list[str]:
    slots = sess.get("slots", {})
    return [k for k in _SLOT_KEYS if k not in slots]

def embed_query(text: str) -> bytes:
    """
    Stable embedding API used by the query pipeline.
    Returns bytes compatible with sqlite-vec vec0 MATCH.
    """
    return _embed_384(text)

def get_language_aware_similarity_threshold(session: dict, current_lang: str) -> float:
    """
    Return similarity threshold that adjusts based on language switching.
    
    When user just switched language, use a HIGHER threshold (stricter matching)
    to avoid pulling in results from previous language's context.
    
    Args:
        session: Current session dict
        current_lang: Current language ('en', 'hi', 'mr')
    
    Returns:
        Float similarity threshold (0.0-1.0). Higher = stricter filtering.
    """
    previous_lang = session.get("lang")
    last_query = session.get("last_q")
    
    # If language just switched, be stricter to avoid context bleed
    if previous_lang and previous_lang != current_lang:
        # Use 0.65+ for cross-language searches (very strict)
        print(f"[SIMILARITY_THRESHOLD] Language switched {previous_lang}->{current_lang}, using strict threshold 0.65")
        return 0.65
    
    # Same language: use normal threshold
    # 0.45 allows broader matching for follow-up questions within same language
    return 0.45

def looks_new_query(text: str) -> bool:
    t = (text or "").strip().lower()
    # short answers should NEVER reset conversation
    if len(t.split()) <= 4:
        return False
    return any(k in t for k in ("what helps", "remedy", "treatment", "how to", "?"))


def handle_chat(user_text: str, session_id: str | None, lang: str | None = None) -> dict:
    """
    Fixed pipeline behavior:
      - Plant/preparation intent is handled FIRST (no symptom followups).
      - Disease/remedy intent returns DB-mapped preparations immediately.
      - Symptom narrative can ask followups, but still returns provisional remedies.
      - Never relies on disease name embedded in preparations table.
      - Language-aware: clears context when language changes.
    """
    user_text = (user_text or "").strip()
    if not user_text:
        return {
            "answer": "Please enter a query.",
            "severity": {"band": "low", "red_flags": []},
            "followups": [],
            "provisional": [],
            "session_id": session_id,
        }

    # -----------------------------
    # Language: respect explicit; otherwise detect once and keep stable in session
    # CRITICAL: Handle language switching by resetting context intelligently
    # -----------------------------
    sess = _get_session(session_id)
    old_lang = sess.get("lang")
    if lang:
        lang = normalize_lang(lang)
    else:
        # prefer stable session language if already known
        lang = normalize_lang(sess.get("lang") or detect_language(user_text))
    
    # INTELLIGENT LANGUAGE SWITCH DETECTION:
    # When user changes language, treat as a fresh conversation context
    # but keep useful metadata like medication history (if any)
    if old_lang and old_lang != lang:
        print(f"[LANGUAGE SWITCH] {old_lang} -> {lang}")
        # Clear conversation state that depends on language/condition
        sess["returned_prep_ids"] = set()  # Clear preparation history
        sess["returned_plant_ids"] = set()  # Clear plant history
        
        # CRITICAL: Reset these to force fresh condition detection
        sess["condition"] = None  # Will be re-detected from new language query
        sess["slots"] = {}  # Clear age/gender/other slots from previous language
        sess["stage"] = "initial"  # Reset to initial stage
        sess["last_q"] = None  # Clear previous question
        
        print(f"[LANGUAGE SWITCH] Cleared session state for fresh context in {lang}")
    
    sess["lang"] = lang
    sess["last_q"] = user_text

    # English text is still useful for LLM/RAG, but
    # intent classification and entity extraction should
    # operate on the original (possibly non-English) text
    # to give a native-language experience.
    text_en = user_text if lang == "en" else translate_to_en(user_text, lang_hint=lang)

    # NLU
    try:
        # Use original text for intent so Hindi/Marathi patterns
        # in api.nlu_optimized.classify_intent are fully leveraged.
        intent = classify_intent(user_text)
    except Exception:
        intent = None
    try:
        # extract_entities: use English translation when available and valid,
        # fall back to original text otherwise.
        translation_ok = (text_en and text_en != user_text and lang != "en")
        extracted = extract_entities(user_text, text_en, prefer_en=translation_ok)
        if extracted and isinstance(extracted, tuple) and len(extracted) == 2:
            entities = {
                "plants": extracted[0] or [],
                "diseases": extracted[1] or []
            }
        else:
            entities = {"plants": [], "diseases": []}
    except Exception:
        entities = {"plants": [], "diseases": []}

    # -----------------------------
    # ⚡ CRITICAL: Route informational intents BEFORE severity check
    # Plant info and preparation queries should NOT trigger emergency warnings
    # -----------------------------
    informational_intents = ("plant", "plant_info", "herb", "plant_identity", 
                             "preparation", "preparation_info", "recipe")
    is_informational = intent in informational_intents
    
    # -----------------------------
    # Severity (only for symptom/disease queries)
    # -----------------------------
    sev = {"band": "normal", "red_flags": []}  # Default for informational queries
    
    if not is_informational:
        # Only assess severity for symptom/disease queries
        sev = assess_severity(user_text)
        if isinstance(sev, str):
            sev = {"band": sev, "red_flags": []}

        if sev.get("band") == "emergency":
            msg_en = (
                "⚠️ This may be serious.\n\n"
                "Please seek immediate medical care. Herbal remedies are not advised for emergency symptoms."
            )
            msg = translate_from_en(msg_en, lang) if lang != "en" else msg_en
            return {
                "answer": msg,
                "severity": sev,
                "followups": [],
                "provisional": [],
                "session_id": sess["id"],
            }

    # -----------------------------
    # Local helpers (keep changes contained inside handle_chat)
    # -----------------------------
    def _extract_plant_term(en_text: str, ent: dict) -> str | None:
        # First check if we have extracted plant entities
        if isinstance(ent, dict) and "plants" in ent:
            plants = ent.get("plants", [])
            if plants and len(plants) > 0:
                # Return the name of the first plant found
                first_plant = plants[0]
                if isinstance(first_plant, dict):
                    # Try to get name in different formats
                    return (first_plant.get("common_name_en") or 
                            first_plant.get("name_en") or
                            first_plant.get("botanical_name") or
                            first_plant.get("name", "")).lower()
                elif isinstance(first_plant, str):
                    return first_plant.lower()
        
        # Legacy: Try NLU entities (backward compatibility)
        if isinstance(ent, dict):
            for k in ("plant", "plant_name", "herb", "ingredient", "entity"):
                v = ent.get(k)
                if isinstance(v, str) and v.strip():
                    return v.strip().lower()
                if isinstance(v, list) and v and isinstance(v[0], str) and v[0].strip():
                    return v[0].strip().lower()

        # Fallback: look for common plant names in text (works for "turmeric milk preparation")
        # Common Ayurvedic plant names
        common_plants = [
            "turmeric", "haldi", "tulsi", "basil", "neem", "brahmi", "ashwagandha",
            "amla", "triphala", "giloy", "brahmi", "shankhpushpi", "brahmi",
            "ginger", "garlic", "black cumin", "fenugreek", "cinnamon",
            "cardamom", "clove", "pepper", "cumin", "coriander",
            "gotu kola", "bhumyamalaki", "bhringraj", "bhumi", "kama",
            "gudmar", "gymnema", "meshashringi"
        ]
        
        text_lower = (en_text or "").lower()
        for plant in common_plants:
            if plant in text_lower:
                return plant
        
        # Enhanced fallback: extract meaningful token (skip preparation types)
        # Words to skip when looking for plant names
        prep_type_words = {
            "decoction", "powder", "churna", "oil", "taila", "ghrita",
            "kwatha", "kadha", "kashaya", "syrup", "capsule", "tablet",
            "juice", "extract", "tincture", "infusion", "tea",
            "preparation", "remedy", "medicine", "formulation",
            "how", "make", "prepare", "recipe", "method"
        }
        
        # Tokenize and find plant name (skip prep types)
        tokens = re.findall(r'\b[a-z]{3,}\b', text_lower)
        for token in reversed(tokens):  # Start from end (plant names often at end)
            if token not in prep_type_words and len(token) >= 3:
                # Check if it looks like a plant name (not a common word)
                if token not in {"the", "for", "with", "from", "about", "what", "tell"}:
                    return token
        
        # Last resort: last meaningful token (works for "tulsi preparation")
        toks = _simple_tokens(en_text)
        return toks[-1].lower() if toks else None

    def _find_plant_id(term: str | None) -> int | None:
        if not term:
            return None
        db = get_db()
        t = term.strip().lower()

        row = db.execute(
            """
            SELECT id
            FROM plants
            WHERE LOWER(common_name_en)=?
               OR LOWER(botanical_name)=?
               OR LOWER(common_name_hi)=?
               OR LOWER(common_name_mr)=?
            LIMIT 1
            """,
            (t, t, t, t),
        ).fetchone()
        if row:
            try:
                return int(row["id"])
            except Exception:
                return int(row[0])

        # LIKE fallback
        row = db.execute(
            """
            SELECT id
            FROM plants
            WHERE LOWER(common_name_en) LIKE ?
               OR LOWER(botanical_name) LIKE ?
            LIMIT 1
            """,
            (f"%{t}%", f"%{t}%"),
        ).fetchone()
        if row:
            try:
                return int(row["id"])
            except Exception:
                return int(row[0])

        return None

    def _extract_disease_term(en_text: str, ent: dict) -> str:
        # ✅ PRIORITY 1: keyword-based condition classifier on original text.
        # This handles Marathi/Hindi disease keywords reliably
        # (e.g. "रक्तदाब" → hypertension) and avoids false positives
        # from fuzzy synonym search on Devanagari tokens.
        cond = _classify_condition(user_text)

        # PRIORITY 1b: Use extracted disease entities from NLU FIRST
        # because they have the exact disease ID and name from DB.
        # This is more accurate than the coarse condition classifier.
        if isinstance(ent, dict) and "diseases" in ent:
            diseases = ent.get("diseases", [])
            if diseases and len(diseases) > 0:
                first_disease = diseases[0]
                if isinstance(first_disease, dict):
                    name = (first_disease.get("name_en") or 
                            first_disease.get("name") or 
                            first_disease.get("disease_name", ""))
                    if name:
                        print(f"[DISEASE_TERM] entity extraction → {name}")
                        return name

        if cond and cond != "general":
            # Map condition code → English disease name for DB lookup
            _COND_TO_NAME = {
                "diabetes": "diabetes",
                "hypertension": "hypertension",
                "cold_cough": "common cold",
                "digestion": "indigestion",
                "arthritis": "arthritis",
                "skin": "acne / pimples",
                "hair": "hair fall",
                "respiratory": "asthma",
                "fever": "fever",
                "mental_health": "anxiety",
                "urinary": "kidney stones",
                "liver": "jaundice",
                "womens_health": "menstrual disorders",
                "pain": "headache",
                "metabolic": "obesity",
                "piles": "piles",
                "allergy": "allergy",
            }
            mapped = _COND_TO_NAME.get(cond)
            if mapped:
                print(f"[DISEASE_TERM] condition classifier → {cond} → {mapped}")
                return mapped
        
        # PRIORITY 3: Legacy explicit entity keys (backward compatibility)
        if isinstance(ent, dict):
            for k in ("disease", "condition", "problem", "illness"):
                v = ent.get(k)
                if isinstance(v, str) and v.strip():
                    return v.strip()
                if isinstance(v, list) and v and isinstance(v[0], str) and v[0].strip():
                    return v[0].strip()
        
        # PRIORITY 4: try extracting from English translation text
        if en_text and en_text != user_text:
            # Simple keyword scan on translated text
            t = en_text.lower()
            for disease_kw in ["diabetes", "hypertension", "blood pressure", "cold",
                               "cough", "arthritis", "joint pain", "indigestion",
                               "acidity", "asthma", "jaundice", "fever", "obesity",
                               "anemia", "piles", "diarrhea", "skin disease",
                               "kidney stone", "thyroid", "cholesterol"]:
                if disease_kw in t:
                    print(f"[DISEASE_TERM] text_en keyword → {disease_kw}")
                    return disease_kw

        # Fallback: return condition even if "general"
        return cond

    # -----------------------------
    # ✅ 1) PREPARATION / RECIPE / "HOW TO MAKE" intent short-circuit
    # -----------------------------
    prep_like = is_preparation_like_query(user_text, text_en)
    if prep_like or intent in ("preparation", "plant_preparation", "recipe", "how_to"):
        plant_term = _extract_plant_term(text_en, entities)
        plant_id = _find_plant_id(plant_term)

        if not plant_id:
            # Fallback: search for preparation by name (e.g., "Triphala Churna" is not a plant)
            db = get_db()
            term_lower = plant_term.lower() if plant_term else ""
            
            if term_lower:
                # Try exact match on preparation name
                row = db.execute(
                    "SELECT id, name_en, plant_id FROM preparations WHERE LOWER(name_en) LIKE ? LIMIT 1",
                    (f"%{term_lower}%",)
                ).fetchone()
                
                if row:
                    # Found a preparation directly
                    prep_id = int(row["id"])
                    prep_name = row["name_en"]
                    plant_id_from_prep = row["plant_id"] if "plant_id" in row.keys() else None
                    
                    # Get prep details
                    prep_row = db.execute(
                        "SELECT * FROM preparations WHERE id = ? LIMIT 1",
                        (prep_id,)
                    ).fetchone()
                    
                    answer_en = f"## {prep_name}\n\n"
                    if prep_row:
                        steps = prep_row["preparation_steps"] if "preparation_steps" in prep_row.keys() else ""
                        dosage = prep_row["dosage_json"] if "dosage_json" in prep_row.keys() else ""
                        timing = prep_row["timing"] if "timing" in prep_row.keys() else ""
                        anupana = prep_row["anupana"] if "anupana" in prep_row.keys() else ""
                        notes = prep_row["notes"] if "notes" in prep_row.keys() else ""
                        
                        if steps:
                            answer_en += f"**How to prepare:**\n{steps}\n\n"
                        if dosage:
                            answer_en += f"**Dosage:**\n{dosage}\n\n"
                        if timing:
                            answer_en += f"**Timing:** {timing}\n\n"
                        if anupana:
                            answer_en += f"**Anupana:** {anupana}\n\n"
                        if notes:
                            answer_en += f"**Notes:** {notes}\n\n"
                    
                    answer = translate_from_en(answer_en, lang) if lang != "en" else answer_en
                    
                    return {
                        "answer": answer,
                        "severity": sev,
                        "followups": [],
                        "provisional": [dict(prep_row)] if prep_row else [],
                        "session_id": sess["id"],
                    }
            
            # Still no match - ask for plant name
            msg_en = "Please tell me the plant name for the preparation (e.g., Tulsi, Neem, Amla)."
            msg = translate_from_en(msg_en, lang) if lang != "en" else msg_en
            return {
                "answer": msg,
                "severity": sev,
                "followups": [],
                "provisional": [],
                "session_id": sess["id"],
            }

        plant = _fetch_plant_full(plant_id) or {}
        preps = _preparations_for_plant(plant_id, k=5)  # uses ingredient mapping

        answer_en = _build_plant_preparation_answer(plant, preps)
        answer = translate_from_en(answer_en, lang) if lang != "en" else answer_en

        return {
            "answer": answer,
            "severity": sev,
            "followups": [],
            "provisional": preps,
            "structured": {"intent": "preparation", "plant": plant, "preparations": preps},
            "session_id": sess["id"],
        }

    # -----------------------------
    # ✅ 2) PLANT INFO intent short-circuit
    # -----------------------------
    if intent in ("plant", "plant_info", "herb", "plant_identity"):
        plant_term = _extract_plant_term(text_en, entities)
        plant_id = _find_plant_id(plant_term)

        if not plant_id:
            msg_en = "Please tell me the plant name (e.g., Tulsi, Neem, Ashwagandha)."
            msg = translate_from_en(msg_en, lang) if lang != "en" else msg_en
            return {
                "answer": msg,
                "severity": sev,
                "followups": [],
                "provisional": [],
                "session_id": sess["id"],
            }

        plant = _fetch_plant_full(plant_id) or {}
        preps = _preparations_for_plant(plant_id, k=3)

        # Build plant profile response natively in target language (no post-translation)
        answer = build_plant_answer(plant, lang=lang)

        if preps:
            # Add preparation list (already in target language)
            prep_label = "🌿 **Preparations available in HerboAI DB:**" if lang == "en" else (
                "🌿 **HerboAI DB में उपलब्ध तैयारियां:**" if lang == "hi" else
                "🌿 **HerboAI DB मध्ये उपलब्ध तयारी:**"
            )
            answer += f"\n\n{prep_label}\n"
            for p in preps[:3]:
                nm = p.get("localized_name") or p.get("name_en") or p.get("classical_name") or "Preparation"
                form = p.get("form_type") or ""
                answer += f"- {nm}" + (f" ({form})" if form else "") + "\n"

        return {
            "answer": answer,
            "severity": sev,
            "followups": [],
            "provisional": preps,
            "structured": {"intent": "plant_info", "plant": plant, "preparations": preps},
            "session_id": sess["id"],
        }

    # -----------------------------
    # From here onward: disease / remedy / symptom flow
    # -----------------------------

    # Detect/lock condition once per session (but avoid nonsense for plant-only queries)
    if not sess.get("condition"):
        sess["condition"] = _classify_condition(user_text)
    condition = sess["condition"]

    # Update slots only in disease/symptom mode (keeps UX sane)
    new_slots = _extract_slots(user_text)
    if new_slots:
        sess.setdefault("slots", {}).update(new_slots)
        sess["stage"] = "collecting"
    slots = sess.get("slots", {})
    
    # CRITICAL: Detect if this is a followup answer (short response filling a slot)
    # If the user just answered a question, treat it as followup conversation
    is_followup_answer = (
        new_slots and  # User provided slot info
        len(text_en.split()) <= 5 and  # Short response (not a new query)
        sess.get("stage") == "collecting"  # Already in conversation
    )

    # ─────────────────────────────────────────────────────────────────────
    # ✅ NEW SHORT-CIRCUIT: Both plant AND disease identified
    # When user says "मुरुमांसाठी निंब" (neem for acne), we KNOW
    # the exact plant + disease. Skip symptom slots entirely and
    # provide the remedy immediately.
    # ─────────────────────────────────────────────────────────────────────
    has_plant_entity = entities and entities.get("plants") and len(entities["plants"]) > 0
    has_disease_entity = entities and entities.get("diseases") and len(entities["diseases"]) > 0
    
    if has_plant_entity and has_disease_entity and intent in ("remedy_lookup", "remedy", "none"):
        plant_ent = entities["plants"][0]
        disease_ent = entities["diseases"][0]
        
        plant_id = plant_ent.get("id")
        disease_id_direct = disease_ent.get("id")
        
        print(f"[CHAT SHORTCIRCUIT] Plant+Disease detected: plant_id={plant_id}, disease_id={disease_id_direct}")
        
        if plant_id and disease_id_direct:
            try:
                db = get_db()
                plant = _fetch_plant_full(int(plant_id)) or {}
                
                # Fetch ALL preparations for this disease (generous limit)
                all_preps = fetch_preparations_for_disease(db, int(disease_id_direct), limit=15)
                
                # Separate plant-specific preps (move to front) from others
                plant_preps = [p for p in all_preps if p.get("plant_id") == int(plant_id)]
                other_preps = [p for p in all_preps if p.get("plant_id") != int(plant_id)]
                
                # Combine: user's plant first, then other herbs for the disease
                combined_preps = plant_preps + other_preps
                
                # If no preps at all, try plant-specific preparations
                if not combined_preps:
                    combined_preps = _preparations_for_plant(int(plant_id), k=6)
                
                # Apply severity-based intelligence ranking
                severity_band = sev.get("band", "normal") if isinstance(sev, dict) else "normal"
                ranked_preps = rank_preparations_by_severity(
                    combined_preps, severity_band=severity_band, limit=8
                )
                
                # Collect unique plants from all preps for display
                all_plants = [plant] if plant else []
                seen_pids = {int(plant_id)} if plant_id else set()
                for pr in ranked_preps:
                    pid = pr.get("plant_id")
                    if pid and int(pid) not in seen_pids:
                        seen_pids.add(int(pid))
                        all_plants.append({
                            "id": int(pid),
                            "common_name_en": pr.get("common_name_en"),
                            "common_name_hi": pr.get("common_name_hi"),
                            "common_name_mr": pr.get("common_name_mr"),
                            "botanical_name": pr.get("botanical_name"),
                        })
                
                if ranked_preps or plant:
                    # Build structured remedy answer with severity-ranked preps
                    answer = build_remedy_answer(
                        disease=disease_ent,
                        preparations=ranked_preps,
                        plants=all_plants,
                        lang=lang,
                        severity_band=severity_band,
                    )
                    
                    print(f"[CHAT SHORTCIRCUIT] Returning {len(ranked_preps)} preps ({len(all_plants)} herbs) for {disease_ent.get('name_en')} + {plant.get('common_name_en')}")
                    
                    return {
                        "answer": answer,
                        "severity": sev,
                        "detected_language": lang or "en",
                        "followups": [],
                        "provisional": ranked_preps,
                        "structured": {
                            "condition": condition,
                            "plant": plant,
                            "plants": all_plants,
                            "disease": disease_ent,
                            "preparations": ranked_preps,
                        },
                        "session_id": sess["id"],
                    }
            except Exception as e:
                print(f"[CHAT SHORTCIRCUIT] Error: {e}")
                import traceback
                traceback.print_exc()
    
    # ─────────────────────────────────────────────────────────────────────
    # ✅ NEW SHORT-CIRCUIT: Disease entity identified (no specific plant)
    # When the NLU found a disease entity, use it directly for remedy
    # lookup instead of relying on _classify_condition → CONDITION_TO_DISEASE
    # mapping which may not cover all diseases.
    # ─────────────────────────────────────────────────────────────────────
    if has_disease_entity and intent in ("remedy_lookup", "remedy", "none") and not has_plant_entity:
        disease_ent = entities["diseases"][0]
        disease_id_direct = disease_ent.get("id")
        
        if disease_id_direct:
            try:
                db = get_db()
                all_preps = fetch_preparations_for_disease(db, int(disease_id_direct), limit=15)
                
                if all_preps:
                    # Apply severity-based intelligence ranking
                    severity_band = sev.get("band", "normal") if isinstance(sev, dict) else "normal"
                    ranked_preps = rank_preparations_by_severity(
                        all_preps, severity_band=severity_band, limit=8
                    )
                    
                    print(f"[CHAT DISEASE_DIRECT] Found {len(all_preps)} preps, ranked {len(ranked_preps)} for disease_id={disease_id_direct} (severity={severity_band})")
                    
                    # Extract unique plants from ranked preps
                    plants_from_preps = []
                    seen_pids = set()
                    for pr in ranked_preps:
                        pid = pr.get("plant_id")
                        if pid and int(pid) not in seen_pids:
                            seen_pids.add(int(pid))
                            plants_from_preps.append({
                                "id": int(pid),
                                "common_name_en": pr.get("common_name_en"),
                                "common_name_hi": pr.get("common_name_hi"),
                                "common_name_mr": pr.get("common_name_mr"),
                                "botanical_name": pr.get("botanical_name"),
                            })
                    
                    answer = build_remedy_answer(
                        disease=disease_ent,
                        preparations=ranked_preps,
                        plants=plants_from_preps,
                        lang=lang,
                        severity_band=severity_band,
                    )
                    
                    print(f"[CHAT DISEASE_DIRECT] Returning {len(ranked_preps)} preps ({len(plants_from_preps)} herbs) for {disease_ent.get('name_en')}")
                    
                    return {
                        "answer": answer,
                        "severity": sev,
                        "detected_language": lang or "en",
                        "followups": [],
                        "provisional": ranked_preps,
                        "structured": {
                            "condition": condition,
                            "disease": disease_ent,
                            "plants": plants_from_preps,
                            "preparations": ranked_preps,
                        },
                        "session_id": sess["id"],
                    }
            except Exception as e:
                print(f"[CHAT DISEASE_DIRECT] Error: {e}")
                import traceback
                traceback.print_exc()

    # Decide whether we should be strict with followups (symptom narrative) or not (explicit disease/remedy)
    # IMPROVED: Also treat "remedy_lookup" intent as explicit (covers "मुरुमांसाठी निंब" type queries)
    # Also: if NLU found disease entities, treat as explicit even if condition is "general"
    explicit_disease_or_remedy = (
        intent in ("disease", "remedy", "treatment", "condition", "remedy_lookup") or
        (condition != "general" and not is_followup_answer) or
        (has_disease_entity and not is_followup_answer)
    )
    symptom_like = intent in ("symptom", "complaint", "triage") or (not explicit_disease_or_remedy) or is_followup_answer

    # Debug: Log decision point
    print(f"[CHAT] intent={intent}, condition={condition}, symptom_like={symptom_like}, explicit={explicit_disease_or_remedy}, is_followup={is_followup_answer}")

    # -----------------------------
    # Provisional retrieval (DB-first schema-correct)
    # disease -> mapping -> preparations
    # Mapping from condition classifier to searchable disease names
    CONDITION_TO_DISEASE = {
        "cold_cough": "common cold",
        "diabetes": "diabetes",
        "hypertension": "hypertension",
        "digestion": "indigestion",
        "arthritis": "arthritis",
        "skin": "acne / pimples",
        "hair": "hair fall",
        "respiratory": "asthma",
        "fever": "fever",
        "mental_health": "anxiety",
        "urinary": "kidney stones",
        "liver": "jaundice",
        "womens_health": "menstrual disorders",
        "pain": "headache",
        "metabolic": "obesity",
        "piles": "piles",
        "allergy": "allergy",
        "general": None,
    }
    # -----------------------------
    provisional: list[dict] = []
    try:
        db = get_db()
        disease_term = _extract_disease_term(text_en, entities)
        disease_id = resolve_disease_id(db, disease_term) if isinstance(disease_term, str) else None

        # Debug: Log disease resolution
        print(f"[CHAT] disease_term={disease_term}, resolved disease_id={disease_id}")

        # fallback using coarse condition if disease term doesn't resolve
        if not disease_id and condition and condition != "general":
            # Map condition code to disease name (e.g., "cold_cough" -> "common cold")
            mapped_disease_name = CONDITION_TO_DISEASE.get(condition)
            if mapped_disease_name:
                disease_id = resolve_disease_id(db, mapped_disease_name)
                print(f"[CHAT] Fallback: mapped condition '{condition}' to disease '{mapped_disease_name}', id={disease_id}")

        if disease_id:
            all_preps = fetch_preparations_for_disease(db, disease_id, limit=6)
            print(f"[CHAT] Fetched {len(all_preps)} preps for disease_id={disease_id}")
            
            # Filter out already-returned preparations
            excluded_ids = sess.get("returned_prep_ids", set())
            print(f"[CHAT] excluded_ids={excluded_ids}, all_preps={len(all_preps)}")
            
            provisional = [p for p in all_preps if p.get("id") not in excluded_ids]
            print(f"[CHAT] After filtering: provisional={len(provisional)} preps, lang={lang}")

        # Optional vector fallback if DB mapping yields none
        if not provisional:
            try:
                seed = condition if condition != "general" else text_en
                qvec = embed_query(seed if isinstance(seed, str) else text_en)
                vec_hits = vector_search_preparations_lang(qvec, lang, k=8)
                
                # Apply language-aware similarity filtering
                # When language switched, be stricter about which results to accept
                similarity_threshold = get_language_aware_similarity_threshold(sess, lang)
                filtered_hits = [h for h in vec_hits if h.get("distance", 0.0) <= (1.0 - similarity_threshold)]
                
                print(f"[CHAT VEC] Language={lang}, similarity_threshold={similarity_threshold}, filtered {len(vec_hits)} -> {len(filtered_hits)} hits")
                
                ids = [h["id"] for h in filtered_hits]
                # Filter out already-returned preparations
                excluded_ids = sess.get("returned_prep_ids", set())
                ids = [id for id in ids if id not in excluded_ids]
                prep_rows = hydrate_preparations(ids)
                dist_by_id = {h["id"]: h.get("distance", 0.0) for h in filtered_hits}
                ranked = rank_preparations(
                    query_tags=[condition],
                    candidates=prep_rows,
                    distance_by_id=dist_by_id,
                    severity_band=sev.get("band", "low"),
                )
                provisional = ranked[:3]
            except Exception:
                provisional = []
                
        # ⚡ INTELLIGENT FALLBACK: LLM-generated remedy when DB + vector search fail
        # This makes the system truly "intelligent" - it can reason about remedies
        # even when explicit database mappings don't exist
        if not provisional and disease_id:
            try:
                print(f"[CHAT LLM FALLBACK] No DB/vector results, trying LLM generation")
                
                # Extract plant from entities if available
                plant_id = None
                plant_name = None
                plant_info = None
                
                if entities and "plants" in entities and entities["plants"]:
                    first_plant = entities["plants"][0]
                    if isinstance(first_plant, dict):
                        plant_id = first_plant.get("id")
                        plant_name = first_plant.get("common_name_en") or first_plant.get("name_en")
                        plant_info = first_plant
                
                # Get disease info
                disease_row = db.execute(
                    "SELECT * FROM diseases WHERE id = ?", (disease_id,)
                ).fetchone()
                disease_info = dict(disease_row) if disease_row else {}
                disease_name = disease_info.get("name_en", disease_term)
                
                # Generate LLM-based remedy
                from services.llm_gateway import generate_plant_remedy, generate_general_plant_remedy
                
                llm_response = None
                if plant_name and plant_id:
                    # Specific plant + disease combination
                    print(f"[LLM] Generating remedy: {plant_name} for {disease_name}")
                    llm_response = generate_plant_remedy(plant_name, plant_info, disease_name, disease_info)
                elif plant_name:
                    # General plant usage (no specific disease)
                    print(f"[LLM] Generating general remedy for: {plant_name}")
                    llm_response = generate_general_plant_remedy(plant_name, plant_info)
                
                if llm_response:
                    # Translate LLM output to user's language if needed
                    if lang != "en":
                        try:
                            llm_translated = translate_from_en(llm_response, lang)
                            if llm_translated and llm_translated != llm_response:
                                print(f"[LLM] Translated response to {lang}")
                                llm_response = llm_translated
                        except Exception as te:
                            print(f"[LLM] Translation to {lang} failed: {te}")

                    # Create a pseudo-preparation object for the response builder
                    provisional = [{
                        "id": 999999,  # Special ID for LLM-generated content
                        "name_en": f"{plant_name or 'Herbal'} Remedy for {disease_name}",
                        "form_type": "generated",
                        "preparation_steps": llm_response,
                        "source": "llm_generated",
                        "localized_name": f"{plant_name or 'Herbal'} Remedy for {disease_name}"
                    }]
                    print(f"[LLM] Generated remedy successfully")
                else:
                    print(f"[LLM] Failed to generate remedy")
                    
            except Exception as e:
                print(f"[CHAT LLM FALLBACK] Error: {type(e).__name__}: {str(e)[:200]}")
                import traceback
                traceback.print_exc()
                
    except Exception as e:
        print(f"[CHAT] ERROR in provisional retrieval: {type(e).__name__}: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        provisional = []
    
    # Track returned preparation IDs in session to prevent repeats
    for prep in provisional:
        prep_id = prep.get("id")
        if prep_id:
            sess.setdefault("returned_prep_ids", set()).add(prep_id)

    # -----------------------------
    # Followups: only strict-gate for symptom narrative
    # -----------------------------
    req_missing = _missing_required(sess)
    opt_missing = _missing_optional(sess)

    print(f"[CHAT] query: ", user_text)
    # Symptom narrative: ask REQUIRED, but still show remedies (hybrid response)
    if symptom_like and req_missing:
        
        print(f"[CHAT HYBRID] symptom_like=True, req_missing={req_missing}, provisional={len(provisional)}")
        print(f"[CHAT SLOTS] filled={slots}, asked_slots={sess.get('asked_slots', set())}")
        
        followups = _slot_questions(condition, req_missing, lang=lang, sess=sess)
        
        # Build clean acknowledgment of newly filled slots
        noted = ""
        if slots:
            # Only show NEW slots filled in this turn
            prev_slots = sess.get("previous_slots", {})
            new_slots = {k: v for k, v in slots.items() if k not in prev_slots or prev_slots[k] != v}
            
            if new_slots:
                # Clean, user-friendly acknowledgment
                slot_labels = {
                    "duration": "Duration" if lang == "en" else "अवधि" if lang == "hi" else "कालावधी",
                    "age_gender": "Age/Gender" if lang == "en" else "उम्र/लिंग" if lang == "hi" else "वय/लिंग",
                    "trend": "Progress" if lang == "en" else "प्रगति" if lang == "hi" else "प्रगती",
                    "existing_illness": "Existing conditions" if lang == "en" else "मौजूदा स्थितियां" if lang == "hi" else "विद्यमान स्थिती",
                }
                
                ack_items = []
                for k, v in new_slots.items():
                    label = slot_labels.get(k, k.replace('_', ' ').title())
                    ack_items.append(f"{label}: {v}")
                
                noted_text = "Noted" if lang == "en" else "नोट किया" if lang == "hi" else "नोंदवले"
                noted = f"✅ {noted_text}: " + "; ".join(ack_items) + "\n\n"
            
            # Update previous slots tracker
            sess["previous_slots"] = slots.copy()

        print(f"[RESPONSE_BUILDER HYBRID] Calling with provisional={len(provisional)}, lang={lang}, followups={len(followups)}")
        response = build_hybrid_response(
            severity=sev.get("band", "low"),
            followups=followups,
            provisional=provisional,
            lang=lang,
        )
        if noted:
            response = f"{noted}{response}"

        return {
            "answer": response,
            "severity": sev,
            "followups": followups,
            "provisional": provisional,
            "structured": {"condition": condition, "preparations": provisional},
            "session_id": sess["id"],
        }

    # Disease/remedy explicit: NEVER block behind required slots; show final response + optional questions
    sess["stage"] = "ready"

    # Debug: Log before response building
    print(f"[CHAT FINAL] provisional={len(provisional)} preps, symptom_like={symptom_like}, req_missing={req_missing}")

    # Optional questions: for explicit disease/remedy, keep them truly optional
    optional_qs: list[str] = []
    if opt_missing:
        optional_qs.extend(_slot_questions(condition, opt_missing, lang=lang, sess=sess))
    # if explicit disease intent, we may add required questions as optional too (but don't gate)
    if explicit_disease_or_remedy and req_missing:
        optional_qs = _slot_questions(condition, req_missing, lang=lang, sess=sess) + optional_qs

    from services.response_builder import build_final_response
    print(f"[RESPONSE_BUILDER] Calling with provisional={len(provisional)}, lang={lang}")
    response = build_final_response(
        severity=sev.get("band", "low"),
        provisional=provisional,
        optional_questions=optional_qs,
        condition=condition,
        slots=slots,
        lang=lang,
    )

    # Structured plants extraction from preparation ingredients (nice for UI)
    structured: dict = {"condition": condition, "preparations": provisional}
    try:
        plants: list[dict] = []
        seen: set[int] = set()
        for pr in provisional[:3]:
            pid = pr.get("id")
            if not pid:
                continue
            for ing in ingredients_for_preparation(int(pid))[:6]:
                plant_id = ing.get("plant_id")
                if plant_id and int(plant_id) not in seen:
                    seen.add(int(plant_id))
                    plants.append(
                        {
                            "id": int(plant_id),
                            "common_name_en": ing.get("common_name_en"),
                            "botanical_name": ing.get("botanical_name"),
                        }
                    )
        if plants:
            structured["plants"] = plants
    except Exception:
        pass

    return {
        "answer": response,
        "severity": sev,
        "followups": optional_qs,
        "provisional": provisional,
        "structured": structured,
        "session_id": sess["id"],
    }

# -----------------------------------------------------------------------------
# Public API expected by api/routes.py (stable entrypoints)
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Public API expected by api/routes.py (stable entrypoints)
# -----------------------------------------------------------------------------

def run_pipeline(
    payload: dict | None = None,
    *,
    user_text: str | None = None,
    session_id: str | None = None,
    lang: str | None = None,
) -> dict:
    """
    Supports BOTH call styles:
      1) run_pipeline(payload_dict)
      2) run_pipeline(user_text=..., session_id=..., lang=...)
    """
    if payload is not None:
        user_text = (
            payload.get("message")
            or payload.get("query")
            or payload.get("text")
            or user_text
            or ""
        )
        session_id = payload.get("session_id") or payload.get("session") or session_id
        lang = payload.get("lang") or payload.get("language") or lang

    user_text = (user_text or "").strip()
    if not user_text:
        return {
            "answer": "Please enter a query.",
            "severity": {"band": "low", "red_flags": []},
            "followups": [],
            "provisional": [],
        }

    # Call your actual core function here
    return handle_chat(user_text=user_text, session_id=session_id, lang=lang)

