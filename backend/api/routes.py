from flask import Blueprint, request, jsonify, abort
import sqlite3
import json
from utils.pagination import get_pagination, absolute_file_url
from repositories.plants_repo import (
    list_plants, get_plant, get_plant_media, get_plant_synonyms, get_plants_for_disease
)
from repositories.diseases_repo import list_diseases, get_disease
from repositories.preparations_repo import (
    list_preparations, get_preparation, get_ingredients, get_indications
)
from repositories.search_repo import remedy_view_for_disease
from services.chat import run_pipeline
from db import get_db

bp = Blueprint("api", __name__)

def _safe_json(v):
    if v is None:
        return None
    if isinstance(v, (dict, list)):
        return v
    if not isinstance(v, str):
        return v
    try:
        return json.loads(v)
    except Exception:
        return v

def _rowdict(row):
    return dict(row) if row is not None else None


@bp.get("/plants")
def plants():
    print("Listing plants")
    q = request.args.get("q")
    print(f"Search plants with q={q}")
    page, size, offset = get_pagination()
    data = list_plants(q, size, offset)
    print(data)
    return {"page": page, "size": size, "items": data["items"], "count": data["count"]}, 200

@bp.get("/plants/<int:plant_id>")
def get_plant_detail(plant_id: int):
    db = get_db()
    db.row_factory = sqlite3.Row

    # --- core plant row
    plant_row = db.execute("""
        SELECT id, botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
               family, ayush_system, description, habitat,
               parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
               active_compounds, therapeutic_actions,
               image_hero, is_endangered, cultivation_status,
               created_at, updated_at
        FROM plants
        WHERE id = ?
    """, (plant_id,)).fetchone()

    if not plant_row:
        abort(404, description="Plant not found")

    plant = _rowdict(plant_row)

    # parse JSON-ish columns
    for k in ["parts_used","rasa","guna","dosha_effect","active_compounds","therapeutic_actions"]:
        plant[k] = _safe_json(plant.get(k))

    # --- synonyms
    synonyms = [
        _rowdict(r) for r in db.execute("""
            SELECT synonym AS name, language, kind
            FROM plant_synonyms
            WHERE plant_id = ?
            ORDER BY id
        """, (plant_id,)).fetchall()
    ]

    # --- contraindications
    contraindications = [
        _rowdict(r) for r in db.execute("""
            SELECT condition, severity, details, alternatives, reference
            FROM contraindications
            WHERE plant_id = ?
            ORDER BY id
        """, (plant_id,)).fetchall()
    ]

    # --- interactions (drug/herb/food)
    interactions = [
        _rowdict(r) for r in db.execute("""
            SELECT interaction_type, interaction_with, effect, severity, mechanism, recommendation, reference
            FROM interactions
            WHERE plant_id = ?
            ORDER BY id
        """, (plant_id,)).fetchall()
    ]

    # --- preparations:
    #  a) direct: primary_plant_id = plant_id
    #  b) indirect: ingredients JSON contains this plant_id
    # Use parameterized pattern to search inside JSON string.
    pattern = f'"plant_id": {plant_id}'
    prep_rows = db.execute("""
        SELECT DISTINCT 
            p.id, p.name_en, p.name_hi, p.name_mr, p.classical_name,
            p.ayush_system,
            p.form_type, p.category,
            p.preparation_steps, p.equipment_needed, p.duration, p.yield, 
            p.storage, p.shelf_life,
            p.dosage_json, p.timing, p.anupana, p.notes,
            p.created_at, p.updated_at
        FROM preparations p
        WHERE p.id IN (
            SELECT DISTINCT preparation_id 
            FROM preparation_ingredients 
            WHERE plant_id = ?
        )

        ORDER BY p.id
    """, (plant_id)).fetchall()

    preparations = []
    for r in prep_rows:
        d = _rowdict(r)
        for k in ["ingredients","preparation_steps","equipment_needed","dosage_json","indications"]:
            d[k] = _safe_json(d.get(k))
        preparations.append(d)

    # Build final payload (note: no `media`, only `image_hero`)
    payload = {
        "plant": plant,
        "synonyms": synonyms,
        "contraindications": contraindications,
        "interactions": interactions,
        "preparations": preparations,
        # kept empty for compatibility; frontend should use image_hero only
        "media": []
    }
    return jsonify(payload)

# --- BRIEF BY ID (for chat thumbnails)
@bp.get("/plants/<int:plant_id>/brief")
def get_plant_brief(plant_id: int):
    db = get_db()
    db.row_factory = sqlite3.Row
    row = db.execute("""
        SELECT id, common_name_en, botanical_name, description, image_hero,
               therapeutic_actions
        FROM plants WHERE id = ?
    """, (plant_id,)).fetchone()
    if not row:
        abort(404)
    d = _rowdict(row)
    d["therapeutic_actions"] = _safe_json(d.get("therapeutic_actions"))
    d["image_url"] = absolute_file_url(d.get("image_hero"))
    return jsonify(d)

# --- BRIEF LIST / SEARCH (for library or smart search)
@bp.get("/plants/brief")
def list_plants_brief():
    q = (request.args.get("q") or "").strip()
    limit = int(request.args.get("limit") or 24)
    offset = int(request.args.get("offset") or 0)

    db = get_db()
    db.row_factory = sqlite3.Row

    if q:
        # simple search: name like or FTS if available
        rows = db.execute("""
            SELECT id, common_name_en, botanical_name, description, image_hero, therapeutic_actions
            FROM plants
            WHERE common_name_en LIKE ? OR botanical_name LIKE ?
            ORDER BY id LIMIT ? OFFSET ?
        """, (f"%{q}%", f"%{q}%", limit, offset)).fetchall()
    else:
        rows = db.execute("""
            SELECT id, common_name_en, botanical_name, description, image_hero, therapeutic_actions
            FROM plants ORDER BY id LIMIT ? OFFSET ?
        """, (limit, offset)).fetchall()

    items = []
    for r in rows:
        d = _rowdict(r)
        d["therapeutic_actions"] = _safe_json(d.get("therapeutic_actions"))
        d["image_url"] = absolute_file_url(d.get("image_hero"))
        items.append(d)

    return jsonify({"items": items, "limit": limit, "offset": offset, "count": len(items)})

@bp.get("/diseases")
def diseases():
    q = request.args.get("q")
    page, size, offset = get_pagination()
    items = list_diseases(q, size, offset)
    return {"page": page, "size": size, "items": items, "count": len(items)}, 200

@bp.get("/diseases/<int:disease_id>")
def disease_detail(disease_id: int):
    d = get_disease(disease_id)
    if not d:
        return {"error": "Disease not found"}, 404
    page, size, offset = get_pagination()
    herbs = get_plants_for_disease(disease_id, size, offset)
    return {"disease": d, "herbs": herbs, "page": page, "size": size}, 200

@bp.get("/preparations")
def preparations():
    q = request.args.get("q")
    page, size, offset = get_pagination()
    items = list_preparations(q, size, offset)
    return {"page": page, "size": size, "items": items, "count": len(items)}, 200

@bp.get("/preparations/<int:prep_id>")
def preparation_detail(prep_id: int):
    prep = get_preparation(prep_id)
    if not prep:
        return {"error": "Preparation not found"}, 404
    ing = get_ingredients(prep_id)
    ind = get_indications(prep_id)
    return {"preparation": prep, "ingredients": ing, "indications": ind}, 200

@bp.get("/remedy")
def remedy():
    """
    Compatibility: returns assembled rows via remedy_view
    ?disease=Type%202%20Diabetes
    """
    disease = request.args.get("disease")
    if not disease:
        return {"error": "Missing 'disease' query param (name_en)"}, 400

    page, size, offset = get_pagination()
    items = remedy_view_for_disease(disease, size, offset)
    return {"disease": disease, "items": items, "page": page, "size": size, "count": len(items)}, 200

@bp.post("/query")
def query():
    """
    Smart AI-like query endpoint:
    - Uses language detection, intent, entity extraction
    - Retrieves from DB and composes deterministic replies (no hallucination)
    - Uses conversations for session context
    """
    data = (request.get_json(silent=True) or {})
    user_text = data.get("text") or ""
    session_id = request.headers.get("x-session-id") or data.get("session_id") or "default"

    if not user_text.strip():
        return {"error": "Empty text"}, 400

    result = run_pipeline(user_text=user_text.strip(), session_id=session_id)
    return jsonify(result), 200
