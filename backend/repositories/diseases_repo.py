from db import get_db
from utils.json_tools import to_json_safe

def list_diseases(q: str | None, limit: int, offset: int):
    db = get_db()
    cur = db.cursor()
    if q:
        cur.execute(
            """
            WITH hits AS (
              SELECT rowid AS id
              FROM diseases_fts
              WHERE diseases_fts MATCH ?
              LIMIT ? OFFSET ?
            )
            SELECT d.*
            FROM hits h JOIN diseases d ON d.id = h.id
            """,
            (q, limit, offset),
        )
    else:
        cur.execute("SELECT * FROM diseases ORDER BY name_en LIMIT ? OFFSET ?", (limit, offset))
    rows = cur.fetchall()
    cur.close()
    return [to_json_safe(r) for r in rows]

def get_disease(disease_id: int):
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM diseases WHERE id = ?", (disease_id,))
    row = cur.fetchone()
    cur.close()
    return to_json_safe(row)
