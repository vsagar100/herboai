from __future__ import annotations
import json
from db import get_db
from utils.json_tools import to_json_safe
from utils.i18n import normalize_lang, vec_table


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

def _json_list(s: str | None) -> list[str]:
    if not s:
        return []
    try:
        v = json.loads(s)
        if isinstance(v, list):
            return [str(x).strip().lower() for x in v if str(x).strip()]
    except Exception:
        pass
    return []

def _tag_overlap_score(query_tags: list[str], item_tags: list[str]) -> float:
    if not query_tags or not item_tags:
        return 1.0
    qs = set(query_tags)
    iset = set(item_tags)
    inter = qs.intersection(iset)
    if not inter:
        return 0.7  # soft penalty (still allow semantic match)
    # scale boost
    return 1.0 + min(0.6, 0.15 * len(inter))

def _efficacy_multiplier(e: int | None) -> float:
    if not e:
        return 1.0
    # 1..5 -> 1.0..1.6
    e = max(1, min(5, int(e)))
    return 1.0 + (e - 1) * 0.15

def vector_search_preparations_lang(query_embedding: bytes, lang: str, k: int = 10):
    """
    Assumes query_embedding is the same binary/bytes format currently used by your embedder.
    (Your existing embedding stack produces float array for vec0 MATCH; keep same.)
    """
    lang = normalize_lang(lang)
    db = get_db()
    vt = vec_table("prep", lang)  # prep_vec_en/hi/mr

    # sqlite-vec API style in your codebase: WHERE embedding MATCH ? AND k = ?
    rows = db.execute(
        f"""
        SELECT preparation_id AS id, distance
        FROM {vt}
        WHERE embedding MATCH ?
          AND k = ?
        """,
        (query_embedding, k),
    ).fetchall()
    return [dict(r) for r in rows]

def hydrate_preparations(ids: list[int]):
    if not ids:
        return []
    db = get_db()
    qmarks = ",".join(["?"] * len(ids))
    rows = db.execute(f"SELECT * FROM preparations WHERE id IN ({qmarks})", ids).fetchall()
    return [to_json_safe(r) for r in rows]

def rank_preparations(query_tags: list[str], candidates: list[dict], distance_by_id: dict[int, float],
                      severity_band: str = "medium") -> list[dict]:
    """
    severity_band influences efficacy preference.
    low: prefer gentle, medium: balanced, high: allow higher efficacy (still safety-gated elsewhere).
    """
    def sev_bias(efficacy: int | None) -> float:
        if not efficacy:
            return 1.0
        efficacy = max(1, min(5, int(efficacy)))
        if severity_band == "low":
            # penalize overly strong remedies
            return 1.15 if efficacy <= 3 else 0.95
        if severity_band == "high":
            return 1.10 if efficacy >= 3 else 0.95
        return 1.0

    scored = []
    for c in candidates:
        cid = int(c["id"])
        dist = distance_by_id.get(cid, 1.0)
        base = 1.0 / (1.0 + float(dist))  # convert distance to similarity-ish

        tags = _json_list(c.get("indications_tags"))
        tag_mul = _tag_overlap_score(query_tags, tags)
        eff_mul = _efficacy_multiplier(c.get("efficacy_level"))
        sev_mul = sev_bias(c.get("efficacy_level"))

        final = base * tag_mul * eff_mul * sev_mul
        c["_score"] = round(final, 6)
        scored.append(c)

    scored.sort(key=lambda x: x.get("_score", 0.0), reverse=True)
    return scored
