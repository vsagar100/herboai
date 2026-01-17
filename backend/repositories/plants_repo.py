from typing import Any
from db import get_db
from utils.json_tools import to_json_safe
from utils.i18n import normalize_lang, fts_table, get_localized_field

def list_plants(q: str | None, limit: int, offset: int, lang: str = "en") -> dict[str, Any]:
    lang = normalize_lang(lang)
    db = get_db()
    cur = db.cursor()

    if q:
        fts = fts_table("plant", lang)  # plants_fts_en
        cur.execute(
            f"""
            WITH hits AS (
              SELECT entity_id AS id
              FROM {fts}
              WHERE {fts} MATCH ?
              LIMIT ? OFFSET ?
            )
            SELECT p.*
            FROM hits h JOIN plants p ON p.id = h.id
            """,
            (q, limit, offset),
        )
    else:
        order_col = {"en": "common_name_en", "hi": "common_name_hi", "mr": "common_name_mr"}.get(lang, "common_name_en")
        cur.execute(
            f"SELECT * FROM plants ORDER BY {order_col} NULLS LAST, botanical_name LIMIT ? OFFSET ?",
            (limit, offset),
        )

    rows = cur.fetchall()
    cur.close()

    return {"items": [to_json_safe(r) for r in rows], "count": len(rows)}

def get_plant(plant_id: int, lang: str = "en"):
    lang = normalize_lang(lang)
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM plants WHERE id = ?", (plant_id,))
    plant = cur.fetchone()
    cur.close()
    
    if plant:
        result = to_json_safe(plant)
        # Enrich with localized fields from entity_i18n
        result["localized_name"] = get_localized_field("plant", plant_id, "name", lang)
        result["localized_description"] = get_localized_field("plant", plant_id, "description", lang)
        result["localized_therapeutic_actions"] = get_localized_field("plant", plant_id, "therapeutic_actions", lang)
        result["localized_parts_used"] = get_localized_field("plant", plant_id, "parts_used", lang)
        return result
    return None

def get_plant_media(plant_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM media WHERE plant_id = ? ORDER BY is_primary DESC, id", (plant_id,))
    rows = cur.fetchall()
    cur.close()
    return [to_json_safe(r) for r in rows]

def get_plant_synonyms(plant_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT synonym, language, kind FROM plant_synonyms WHERE plant_id = ? ORDER BY id", (plant_id,))
    rows = cur.fetchall()
    cur.close()
    return [to_json_safe(r) for r in rows]

def get_plants_for_disease(disease_id: int, limit: int, offset: int, lang: str = "en"):
    lang = normalize_lang(lang)
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT p.*, pdm.efficacy_level, pdm.evidence_type, pdm.mechanism
        FROM plant_disease_mapping pdm
        JOIN plants p ON p.id = pdm.plant_id
        WHERE pdm.disease_id = ?
        ORDER BY pdm.efficacy_level DESC, p.common_name_en
        LIMIT ? OFFSET ?
        """,
        (disease_id, limit, offset),
    )
    rows = cur.fetchall()
    cur.close()
    
    results = []
    for row in rows:
        result = to_json_safe(row)
        plant_id = result.get("id")
        if plant_id:
            result["localized_name"] = get_localized_field("plant", plant_id, "name", lang)
            result["localized_therapeutic_actions"] = get_localized_field("plant", plant_id, "therapeutic_actions", lang)
        results.append(result)
    return results
