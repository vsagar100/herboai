from db import get_db
from utils.json_tools import to_json_safe

def get_preparation(preparation_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM preparations WHERE id = ?", (preparation_id,))
    row = cur.fetchone()
    cur.close()
    return to_json_safe(row)

def list_preparations(q: str | None, limit: int, offset: int):
    db = get_db()
    cur = db.cursor()
    if q:
        cur.execute(
            """
            WITH hits AS (
              SELECT rowid AS id
              FROM preparations_fts
              WHERE preparations_fts MATCH ?
              LIMIT ? OFFSET ?
            )
            SELECT pr.*
            FROM hits h JOIN preparations pr ON pr.id = h.id
            """,
            (q, limit, offset),
        )
    else:
        cur.execute("SELECT * FROM preparations ORDER BY name_en LIMIT ? OFFSET ?", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    return [to_json_safe(r) for r in rows]

def get_ingredients(preparation_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT pr.name_en AS preparation,
               pi.part, pi.quantity_value, pi.quantity_unit,
               p.id as plant_id, p.common_name_en, p.botanical_name
        FROM preparation_ingredients pi
        JOIN preparations pr ON pr.id = pi.preparation_id
        JOIN plants p ON p.id = pi.plant_id
        WHERE pi.preparation_id = ?
        ORDER BY pi.id
        """,
        (preparation_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return [to_json_safe(r) for r in rows]

def get_indications(preparation_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT pr.name_en AS preparation,
               d.id as disease_id, d.name_en as disease, pi.strength, pi.evidence_type, pi.notes
        FROM preparation_indications pi
        JOIN preparations pr ON pr.id = pi.preparation_id
        JOIN diseases d ON d.id = pi.disease_id
        WHERE pi.preparation_id = ?
        ORDER BY pi.strength DESC, d.name_en
        """,
        (preparation_id,),
    )
    rows = cur.fetchall()
    cur.close()
    return [to_json_safe(r) for r in rows]
