from typing import Any
from db import get_db
from utils.json_tools import to_json_safe

def list_plants(q: str | None, limit: int, offset: int) -> dict[str, Any]:
    db = get_db()
    cur = db.cursor()

    if q:
        # FTS first, hydrate from base table
        cur.execute(
            """
            WITH hits AS (
              SELECT rowid AS id
              FROM plants_fts
              WHERE plants_fts MATCH ?
              LIMIT ? OFFSET ?
            )
            SELECT p.*
            FROM hits h JOIN plants p ON p.id = h.id
            """,
            (q, limit, offset),
        )
    else:
        cur.execute(
            "SELECT * FROM plants ORDER BY common_name_en NULLS LAST, botanical_name LIMIT ? OFFSET ?",
            (limit, offset),
        )

    rows = cur.fetchall()
    cur.close()

    return {
        "items": [to_json_safe(r) for r in rows],
        "count": len(rows)
    }

def get_plant(plant_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM plants WHERE id = ?", (plant_id,))
    plant = cur.fetchone()
    cur.close()
    return to_json_safe(plant)

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

def get_plants_for_disease(disease_id: int, limit: int, offset: int):
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
    return [to_json_safe(r) for r in rows]
