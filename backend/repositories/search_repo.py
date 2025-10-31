from db import get_db
from utils.json_tools import to_json_safe

def remedy_view_for_disease(disease_name_en: str, limit: int, offset: int):
    db = get_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT *
        FROM remedy_view
        WHERE disease_en = ?
        ORDER BY efficacy_level DESC, preparation_name
        LIMIT ? OFFSET ?
        """,
        (disease_name_en, limit, offset),
    )
    rows = cur.fetchall()
    cur.close()
    return [to_json_safe(r) for r in rows]
