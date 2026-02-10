from __future__ import annotations

import json
from typing import Any, Optional

from db import get_db
from utils.i18n import normalize_lang


def get_ayush_nav(lang: str = "en") -> list[dict[str, Any]]:
    lang = normalize_lang(lang)
    db = get_db()
    row = db.execute(
        "SELECT nav_json, nav_json_en, nav_json_hi, nav_json_mr FROM ayush_kb_nav WHERE key = ?",
        ("ayush",),
    ).fetchone()
    if not row:
        return []

    row = dict(row)
    if not row.get("nav_json"):
        return []

    # Prefer lang-specific stored JSON; fall back to English.
    nav_json = None
    if lang == "hi":
        nav_json = row.get("nav_json_hi")
    elif lang == "mr":
        nav_json = row.get("nav_json_mr")
    elif lang == "en":
        nav_json = row.get("nav_json_en") or row.get("nav_json")

    nav_json = (nav_json or row.get("nav_json_en") or row.get("nav_json") or "[]")
    try:
        nav = json.loads(nav_json)
        return nav if isinstance(nav, list) else []
    except Exception:
        return []


def get_article(slug: str, lang: str = "en") -> Optional[dict[str, Any]]:
    slug = (slug or "").strip()
    if not slug:
        return None

    lang = normalize_lang(lang)
    db = get_db()
    row = db.execute(
        """
        SELECT id, slug,
               title_en, title_hi, title_mr,
               body_en, body_hi, body_mr,
               keywords_en, updated_at
        FROM ayush_kb_articles
        WHERE slug = ?
        """,
        (slug,),
    ).fetchone()
    if not row:
        return None

    row = dict(row)

    title_en = row.get("title_en") or ""
    body_en = row.get("body_en") or ""
    title_hi = row.get("title_hi") or ""
    body_hi = row.get("body_hi") or ""
    title_mr = row.get("title_mr") or ""
    body_mr = row.get("body_mr") or ""

    if lang == "hi":
        title = title_hi.strip() or title_en
        body = body_hi.strip() or body_en
    elif lang == "mr":
        title = title_mr.strip() or title_en
        body = body_mr.strip() or body_en
    else:
        title = title_en
        body = body_en

    return {
        "id": row.get("id"),
        "slug": row.get("slug"),
        "title": title,
        "body": body,
        "updated_at": row.get("updated_at"),
    }


def list_articles() -> list[dict[str, Any]]:
    db = get_db()
    rows = db.execute(
        "SELECT id, slug, title_en, updated_at FROM ayush_kb_articles ORDER BY id ASC"
    ).fetchall()
    return [dict(r) for r in rows]


def pick_slug(user_text: str, text_en: str) -> Optional[str]:
    raw = (user_text or "").strip().lower()
    en = (text_en or "").strip().lower()
    combined = f"{raw} {en}".strip()

    # High-signal triggers
    if any(k in combined for k in ("ayush", "आयुष")):
        return "ayush-what"
    if any(k in combined for k in ("ayurveda", "आयुर्वेद")):
        return "ayurveda"
    if any(k in combined for k in ("yoga", "योग", "pranayama", "asana", "naturop")):
        return "yoga-naturopathy"
    if any(k in combined for k in ("unani", "siddha", "sowa", "rigpa", "homeopathy", "homoeopathy")):
        return "other-ayush-systems"

    # Lifestyle / general health education (non-medical)
    # Keep triggers fairly specific to avoid stealing plant/disease queries.
    if any(k in combined for k in (
        "dinacharya",
        "dincharya",
        "daily routine",
        "lifestyle tips",
        "healthy habits",
        "दिनचर्य",  # matches दिनचर्या/दिनचर्येचे etc.
        "दनचरय",    # fallback if matras get stripped
        "जीवनशैली",
        "लाइफस्टाइल",
        "आहार विहार",
        "झोप",
        "ताण",
    )):
        return "lifestyle-basics"

    if any(k in combined for k in (
        "when to consult",
        "red flag",
        "emergency",
        "warning signs",
        "सावधान",
        "कधी डॉक्टर",
        "डॉक्टरकडे कधी",
        "कब डॉक्टर",
        "डॉक्टर से कब",
    )):
        return "safety"

    return None


def maybe_answer_ayush_kb(
    user_text: str,
    text_en: str,
    lang: str,
    entities: dict,
) -> Optional[str]:
    """Return a KB answer if this looks like an AYUSH/general-info query.

    Guard rails:
    - If plants/diseases are already detected, we assume it is a domain query and
      let the main pipeline handle it.
    """

    try:
        has_entities = bool((entities or {}).get("plants")) or bool((entities or {}).get("diseases"))
    except Exception:
        has_entities = False

    if has_entities:
        return None

    slug = pick_slug(user_text, text_en)
    if not slug:
        return None

    article = get_article(slug, lang=lang)
    if not article:
        return None

    # Keep response compact but useful (chat UX)
    title = article.get("title") or ""
    body = article.get("body") or ""
    return f"**{title}**\n\n{body}".strip()
