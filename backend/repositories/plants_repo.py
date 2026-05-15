from typing import Any
from db import get_db
from utils.json_tools import to_json_safe
from utils.i18n import normalize_lang, fts_table, get_localized_field

# Valid sort keys mapped to SQL ORDER BY expressions
_SORT_MAP = {
    "name_asc":  "common_name_en ASC",
    "name_desc": "common_name_en DESC",
    "botanical":  "botanical_name ASC",
    "family":    "family ASC NULLS LAST, common_name_en ASC",
    "ayush":     "ayush_system ASC NULLS LAST, common_name_en ASC",
    "newest":    "created_at DESC",
}


def _fts_is_usable(db, lang: str, min_rows: int = 10) -> bool:
    """Return True if the FTS table for *lang* has at least *min_rows* indexed."""
    tbl = fts_table("plant", lang)
    try:
        r = db.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()
        return r[0] >= min_rows
    except Exception:
        return False


def _ayush_where(ayush_system: str | None, prefix: str = "") -> tuple[str, tuple]:
    """Build a case-insensitive AYUSH WHERE clause."""
    col = f"{prefix}ayush_system" if prefix else "ayush_system"
    if not ayush_system:
        return "", ()
    return f"AND LOWER({col}) = LOWER(?)", (ayush_system,)


def list_plants(
    q: str | None,
    limit: int,
    offset: int,
    lang: str = "en",
    ayush_system: str | None = None,
    sort: str | None = None,
) -> dict[str, Any]:
    """Return paginated plant list with optional FTS/LIKE search, AYUSH filter, and sorting.
    Returns {items, count, total} where total is the full filtered count."""
    lang = normalize_lang(lang)
    db = get_db()
    cur = db.cursor()

    order_expr = _SORT_MAP.get(sort or "", _SORT_MAP["name_asc"])
    ayush_clause, ayush_params = _ayush_where(ayush_system, prefix="p." if q else "")

    if q:
        use_fts = _fts_is_usable(db, lang)

        if use_fts:
            fts = fts_table("plant", lang)
            count_sql = (
                f"SELECT COUNT(*) FROM (SELECT entity_id AS id FROM {fts} WHERE {fts} MATCH ?) h "
                f"JOIN plants p ON p.id = h.id WHERE 1=1 {ayush_clause}"
            )
            data_sql = (
                f"SELECT p.* FROM (SELECT entity_id AS id FROM {fts} WHERE {fts} MATCH ?) h "
                f"JOIN plants p ON p.id = h.id WHERE 1=1 {ayush_clause} "
                f"ORDER BY {order_expr} LIMIT ? OFFSET ?"
            )
            cur.execute(count_sql, (q, *ayush_params))
            total = cur.fetchone()[0]
            cur.execute(data_sql, (q, *ayush_params, limit, offset))
        else:
            # Fallback: LIKE-based search across key text columns
            like = f"%{q}%"
            where_parts = [
                "(p.common_name_en LIKE ? OR p.botanical_name LIKE ? OR p.common_name_hi LIKE ?"
                " OR p.common_name_mr LIKE ? OR p.description LIKE ?"
                " OR p.therapeutic_actions LIKE ? OR p.family LIKE ?)"
            ]
            like_params = [like] * 7
            if ayush_clause:
                # strip leading "AND " for the extra clause
                where_parts.append(ayush_clause.lstrip("AND "))

            where_sql = " AND ".join(where_parts)
            cur.execute(
                f"SELECT COUNT(*) FROM plants p WHERE {where_sql}",
                (*like_params, *ayush_params),
            )
            total = cur.fetchone()[0]
            cur.execute(
                f"SELECT p.* FROM plants p WHERE {where_sql} ORDER BY {order_expr} LIMIT ? OFFSET ?",
                (*like_params, *ayush_params, limit, offset),
            )
    else:
        # Browse mode (no query)
        ayush_browse, ayush_bp = _ayush_where(ayush_system)
        where = f"WHERE 1=1 {ayush_browse}" if ayush_browse else ""
        cur.execute(f"SELECT COUNT(*) FROM plants {where}", ayush_bp)
        total = cur.fetchone()[0]
        cur.execute(
            f"SELECT * FROM plants {where} ORDER BY {order_expr} LIMIT ? OFFSET ?",
            (*ayush_bp, limit, offset),
        )

    rows = cur.fetchall()
    cur.close()

    return {"items": [to_json_safe(r) for r in rows], "count": len(rows), "total": total}


def get_plant_stats() -> dict[str, Any]:
    """Return aggregate stats for the plant library dashboard."""
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM plants")
    total = cur.fetchone()[0]

    # Case-insensitive grouping: capitalise first letter for display
    cur.execute(
        "SELECT ayush_system, COUNT(*) AS cnt FROM plants "
        "WHERE ayush_system IS NOT NULL AND ayush_system != '' "
        "GROUP BY LOWER(ayush_system) ORDER BY cnt DESC"
    )
    raw = cur.fetchall()
    by_ayush: dict[str, int] = {}
    for r in raw:
        key = (r[0] or "").strip().capitalize()  # normalise display key
        if key:
            by_ayush[key] = by_ayush.get(key, 0) + r[1]

    cur.execute(
        "SELECT family, COUNT(*) AS cnt FROM plants "
        "WHERE family IS NOT NULL AND family != '' "
        "GROUP BY family ORDER BY cnt DESC LIMIT 10"
    )
    top_families = {r[0]: r[1] for r in cur.fetchall()}
    cur.execute("SELECT COUNT(*) FROM plants WHERE is_endangered = 1")
    endangered = cur.fetchone()[0]
    cur.close()
    return {
        "total_plants": total,
        "by_ayush_system": by_ayush,
        "top_families": top_families,
        "endangered_count": endangered,
    }

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
