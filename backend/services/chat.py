import time
from typing import Dict, Any
import json
import math
from sentence_transformers import SentenceTransformer
from sqlite_vec import serialize_float32
from db import get_db
from nlu import detect_language, translator, classify_intent, extract_entities
from semantic import (
    disease_by_name_en,
    top_plants_for_disease, top_preparations_for_disease, ingredients_for_preparation
)
from context import get_last_context, persist_turn

def compose_remedy_answer(disease_row: Dict[str, Any]) -> Dict[str, Any]:
    d_id = disease_row["id"]
    plants = top_plants_for_disease(d_id, k=5)
    preps  = top_preparations_for_disease(d_id, k=3)

    # Deterministic, no hallucination: summarize only rows we fetched
    parts = []
    parts.append(f"Condition: {disease_row.get('name_en','')}")
    if disease_row.get("ayurvedic_name"):
        parts.append(f"Ayurvedic name: {disease_row['ayurvedic_name']}")
    if plants:
        herbs_line = ", ".join([p.get("common_name_en") or p.get("botanical_name") for p in plants])
        parts.append(f"Helpful herbs (sorted by mapped efficacy): {herbs_line}.")
    if preps:
        p_lines = []
        for pr in preps:
            dose = pr.get("dosage_json") or ""
            p_lines.append(f"{pr.get('name_en')} ({pr.get('form_type')})")
        parts.append("Relevant preparations: " + "; ".join(p_lines) + ".")
        # Add details for the first preparation
        first = preps[0]
        ings = ingredients_for_preparation(first["id"])
        if ings:
            ing_str = ", ".join([f"{i['common_name_en']} {i['quantity_value'] or ''}{i['quantity_unit'] or ''}".strip()
                                 for i in ings])
            parts.append(f"Example preparation – {first['name_en']}: ingredients → {ing_str}.")
        if first.get("dosage_json"):
            parts.append(f"Dosage: {first['dosage_json']}")
        if first.get("timing"):
            parts.append(f"Timing: {first['timing']}")
        if first.get("anupana"):
            parts.append(f"Anupana: {first['anupana']}")
        if first.get("notes"):
            parts.append(f"Notes: {first['notes']}")

    return {
        "text": " ".join(parts),
        "plants": plants,
        "preparations": preps
    }

def old_run_pipeline(user_text: str, session_id: str | None) -> Dict[str, Any]:
    t0 = time.time()

    # 1) Language detect
    lang = detect_language(user_text)

    # 2) Translate-to-EN for internal routing (no-op if translator not wired)
    text_for_intent = translator.to_en(user_text, src_lang=lang)

    # 3) Intent
    intent = classify_intent(text_for_intent)

    # 4) Entities (plants/diseases)
    plants, diseases = extract_entities(user_text)

    # 5) Context integration (fallback if entities are empty)
    last = get_last_context(session_id) if session_id else None
    if not diseases and last and last.get("entities", {}).get("diseases"):
        diseases = last["entities"]["diseases"]
    
    if diseases and intent == "none":
        intent = "remedy_lookup"

    # 6) Retrieval & answer (strictly DB-backed, no hallucination)
    answer_payload: Dict[str, Any] = {"text": "Sorry, I couldn’t find a direct remedy. Try another term."}
    structured: Dict[str, Any] = {}

    if intent in ("remedy_lookup", "preparation_info"):
        # try first disease by name if present
        d_row = None
        if diseases:
            # entities list may contain partial dicts; ensure 'id' or resolve by name_en
            d = diseases[0]
            if "id" in d:
                d_row = d
            elif "name_en" in d:
                d_row = disease_by_name_en(d["name_en"])
        if not d_row:
            # heuristic: map common mentions to known diseases
            # (example: "diabetes" -> Type 2 Diabetes)
            if "diabetes" in text_for_intent.lower():
                d_row = disease_by_name_en("Type 2 Diabetes")
            elif "cold" in text_for_intent.lower() or "cough" in text_for_intent.lower():
                d_row = disease_by_name_en("Common Cold")
            elif "arthritis" in text_for_intent.lower() or "joint" in text_for_intent.lower():
                d_row = disease_by_name_en("Arthritis")
            elif "bp" in text_for_intent.lower() or "hypertension" in text_for_intent.lower():
                d_row = disease_by_name_en("Hypertension")
            elif "indigestion" in text_for_intent.lower() or "constipation" in text_for_intent.lower():
                d_row = disease_by_name_en("Indigestion")

        if d_row:
            structured = compose_remedy_answer(d_row)
            answer_payload = {"text": structured["text"]}

    elif intent == "plant_info" and plants:
        p = plants[0]
        # Compose plant summary strictly from columns
        lines = [f"{p.get('common_name_en') or p.get('botanical_name')} ({p.get('botanical_name')})"]
        if p.get("therapeutic_actions"):
            lines.append(f"Actions: {p['therapeutic_actions']}")
        if p.get("rasa"):
            lines.append(f"Rasa: {p['rasa']}")
        if p.get("virya"):
            lines.append(f"Virya: {p['virya']}")
        if p.get("vipaka"):
            lines.append(f"Vipaka: {p['vipaka']}")
        answer_payload = {"text": " | ".join(lines)}
        structured = {"plant": p}

    # 7) Translate back to user language (no-op if translator not wired)
    final_text = translator.from_en(answer_payload["text"], tgt_lang=lang)

    # 8) Persist turn
    entities_dump = {
        "plants": plants,
        "diseases": diseases
    }
    duration_ms = int((time.time() - t0) * 1000)
    persist_turn(session_id or "default", user_text, lang, intent, entities_dump, final_text, structured, duration_ms)

    return {
        "lang_detected": lang,
        "intent": intent,
        "entities": entities_dump,
        "answer": final_text,
        "context": {
            "last_intent": (last or {}).get("intent"),
        },
        "structured": structured,
        "duration_ms": duration_ms
    }

########################################################################################

# --- helper: embedding cosine fallback (SQLite vector extension compatible) ---
def _search_similar_embeddings(table: str, query_text: str, k: int = 3) -> list[dict]:
    """
    Fallback semantic search using precomputed embeddings table.
    Works only if you have SQLite vector0 / vss0 extension or you store embeddings as JSON arrays.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")  # light, CPU-friendly
    q_emb = model.encode(query_text).tolist()

    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(f"""
            SELECT entity_id AS id, name_en,
                   1 - (embedding <-> json_array(?)) AS score
            FROM {table}
            ORDER BY score DESC LIMIT ?
        """, (json.dumps(q_emb), k))
        rows = [dict(r) for r in cur.fetchall()]
    except Exception:
        # fallback if vector extension not available
        rows = []
    cur.close()
    return rows

# --- helper: diseases for a given plant ---
def _diseases_for_plant(plant_id: int, k: int = 5) -> list[dict]:
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT d.*, pdm.efficacy_level, pdm.evidence_type
        FROM plant_disease_mapping pdm
        JOIN diseases d ON d.id = pdm.disease_id
        WHERE pdm.plant_id = ?
        ORDER BY pdm.efficacy_level DESC, d.name_en
        LIMIT ?
    """, (plant_id, k))
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    return rows

def run_pipeline(user_text: str, session_id: str | None) -> Dict[str, Any]:
    t0 = time.time()
    lang = detect_language(user_text)
    text_for_intent = translator.to_en(user_text, src_lang=lang)
    intent = classify_intent(text_for_intent)

    plants, diseases = extract_entities(user_text)

    # Embedding fallback if FTS/synonyms didn’t find anything
    if not diseases:
        diseases = _search_similar_vec("disease_vec", "disease_id", user_text, 3)
    if not plants:
        plants   = _search_similar_vec("plant_vec",   "plant_id",   user_text, 3)
    # prune obviously weak matches (tune 1.6~2.0 as you observe)
    plants   = _prune_vec_hits(plants,   1.6)
    diseases = _prune_vec_hits(diseases, 1.6)

    # --- context recall ---
    last = get_last_context(session_id) if session_id else None
    if not diseases and last and last.get("entities", {}).get("diseases"):
        diseases = last["entities"]["diseases"]
    if not plants and last and last.get("entities", {}).get("plants"):
        plants = last["entities"]["plants"]
    if intent == "none" and last:
        intent = last.get("intent", "none")

    # --- answer assembly ---
    answer_payload = {"text": "Sorry, I couldn’t find a direct remedy."}
    structured = {}

    if intent in ("remedy_lookup", "preparation_info"):
        d_row = None
        if diseases:
            d = diseases[0]
            if "id" in d:
                # hydrate by id if needed
                d_row = d if ("name_en" in d and d.get("name_en")) else _fetch_disease_min(d["id"])
            elif "name_en" in d:
                d_row = disease_by_name_en(d["name_en"])


        # if still not found, semantic fallback for keywords
        if not d_row and plants:
            # infer disease list for given plant
            ds = _diseases_for_plant(plants[0]["id"])
            if ds:
                d_row = ds[0]

        if d_row:
            structured = compose_remedy_answer(d_row)
            answer_payload = {"text": structured["text"]}

    elif intent == "plant_info" and plants:
        p = plants[0]
        # If the candidate came from vec search, it only has {id, distance}. Hydrate from DB.
        if ("botanical_name" not in p or p.get("botanical_name") is None) and "id" in p:
            dbp = _fetch_plant_min(p["id"])
            if dbp:
                # keep distance if present (useful for debugging), overlay DB fields
                p = {**p, **dbp}

        lines = [f"{p.get('common_name_en') or p.get('botanical_name')} ({p.get('botanical_name')})"]
        if p.get("therapeutic_actions"):
            lines.append(f"Actions: {p['therapeutic_actions']}")
        if p.get("rasa"):
            lines.append(f"Rasa: {p['rasa']}")
        if p.get("virya"):
            lines.append(f"Virya: {p['virya']}")
        if p.get("vipaka"):
            lines.append(f"Vipaka: {p['vipaka']}")
        answer_payload = {"text": " | ".join(lines)}
        structured = {"plant": p}

    # --- translation back ---
    final_text = translator.from_en(answer_payload["text"], tgt_lang=lang)

    # --- persist conversation ---
    entities_dump = {"plants": plants, "diseases": diseases}
    duration_ms = int((time.time() - t0) * 1000)
    persist_turn(session_id or "default", user_text, lang, intent, entities_dump,
                 final_text, structured, duration_ms)

    return {
        "lang_detected": lang,
        "intent": intent,
        "entities": entities_dump,
        "answer": final_text,
        "context": {"last_intent": (last or {}).get("intent")},
        "structured": structured,
        "duration_ms": duration_ms
    }

_EMB_MODEL = None
def _embed_384(text: str) -> bytes:
    global _EMB_MODEL
    if _EMB_MODEL is None:
        _EMB_MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    v = _EMB_MODEL.encode(text).astype("float32").tolist()
    return serialize_float32(v)

def _search_similar_vec(table: str, id_col: str, qtext: str, k: int = 3):
    db = get_db()
    qv = _embed_384(qtext)
    sql = f"""SELECT {id_col} AS id, distance
              FROM {table}
              WHERE embedding MATCH ?
                AND k = ?"""
    return [dict(r) for r in db.execute(sql, (qv, k)).fetchall()]

def _fetch_plant_min(plant_id: int) -> dict | None:
    db = get_db()
    row = db.execute("""
        SELECT id, common_name_en, botanical_name, therapeutic_actions, rasa, virya, vipaka
        FROM plants
        WHERE id = ?
    """, (plant_id,)).fetchone()
    return dict(row) if row else None

def _fetch_disease_min(disease_id: int) -> dict | None:
    db = get_db()
    row = db.execute("""
        SELECT id, name_en, ayurvedic_name, description, severity_level
        FROM diseases
        WHERE id = ?
    """, (disease_id,)).fetchone()
    return dict(row) if row else None

def _prune_vec_hits(hits: list[dict], max_distance: float) -> list[dict]:
    # distance is smaller => closer. Tune threshold with real data.
    return [h for h in hits if "distance" not in h or (h["distance"] is not None and h["distance"] <= max_distance)]
