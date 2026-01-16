from db import get_db
from utils.json_tools import to_json_safe
from utils.i18n import normalize_lang, fts_table

def list_diseases(q: str | None, limit: int, offset: int, lang: str = "en"):
    lang = normalize_lang(lang)
    db = get_db()
    cur = db.cursor()
    if q:
        fts = fts_table("disease", lang)
        cur.execute(
            f"""
            WITH hits AS (
              SELECT entity_id AS id
              FROM {fts}
              WHERE {fts} MATCH ?
              LIMIT ? OFFSET ?
            )
            SELECT d.*
            FROM hits h JOIN diseases d ON d.id = h.id
            """,
            (q, limit, offset),
        )
    else:
        order_col = {"en": "name_en", "hi": "name_hi", "mr": "name_mr"}.get(lang, "name_en")
        cur.execute(f"SELECT * FROM diseases ORDER BY {order_col} LIMIT ? OFFSET ?", (limit, offset))

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
