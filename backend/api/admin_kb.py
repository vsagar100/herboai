from __future__ import annotations

import json
from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from db import get_db
from config import Config
from services.async_translator import get_async_translator

admin_kb_bp = Blueprint("admin_kb", __name__)


def _now() -> str:
    return datetime.utcnow().isoformat(sep=" ", timespec="seconds")


def _tx(text: str, lang: str, timeout: int = 30) -> str | None:
    """Translate English -> lang using the async translator.

    Returns None if translator isn't ready within warm_timeout or translation fails.
    """
    if not text or lang == "en":
        return text
    try:
        tx = get_async_translator()
        return tx.translate_async(text, lang, timeout=timeout, warm_timeout=5)
    except Exception:
        return None


def _translate_article_fields(title_en: str, body_en: str, keywords_en: str | None) -> dict:
    if not Config.ENABLE_I18N_TRANSLATION:
        return {
            "title_hi": None,
            "body_hi": None,
            "keywords_hi": None,
            "title_mr": None,
            "body_mr": None,
            "keywords_mr": None,
        }

    title_hi = _tx(title_en, "hi")
    body_hi = _tx(body_en, "hi")
    title_mr = _tx(title_en, "mr")
    body_mr = _tx(body_en, "mr")

    # keywords are optional; leaving them blank is fine
    keywords_hi = _tx(keywords_en or "", "hi") if keywords_en else None
    keywords_mr = _tx(keywords_en or "", "mr") if keywords_en else None

    return {
        "title_hi": title_hi,
        "body_hi": body_hi,
        "keywords_hi": keywords_hi,
        "title_mr": title_mr,
        "body_mr": body_mr,
        "keywords_mr": keywords_mr,
    }


def _translate_nav(nav: list) -> tuple[str | None, str | None]:
    """Translate nav structure for hi/mr by translating 'title' and item 'label'."""
    if not Config.ENABLE_I18N_TRANSLATION:
        return None, None

    def _translate_nav_for(lang: str) -> str | None:
        out = []
        for grp in nav:
            if not isinstance(grp, dict):
                continue
            g2 = dict(grp)
            g2["title"] = _tx(str(grp.get("title") or ""), lang) or str(grp.get("title") or "")
            items_out = []
            for it in grp.get("items") or []:
                if not isinstance(it, dict):
                    continue
                it2 = dict(it)
                if "label" in it2:
                    it2["label"] = _tx(str(it.get("label") or ""), lang) or str(it.get("label") or "")
                items_out.append(it2)
            g2["items"] = items_out
            out.append(g2)
        try:
            return json.dumps(out, ensure_ascii=False)
        except Exception:
            return None

    return _translate_nav_for("hi"), _translate_nav_for("mr")


@admin_kb_bp.get("/kb/ayush/articles")
@jwt_required()
def list_ayush_articles():
    db = get_db()
    rows = db.execute(
        "SELECT id, slug, title_en, updated_at FROM ayush_kb_articles ORDER BY id ASC"
    ).fetchall()
    return jsonify({"items": [dict(r) for r in rows]})


@admin_kb_bp.get("/kb/ayush/articles/<int:article_id>")
@jwt_required()
def get_ayush_article(article_id: int):
    db = get_db()
    row = db.execute(
        "SELECT id, slug, title_en, body_en, keywords_en, updated_at FROM ayush_kb_articles WHERE id = ?",
        (article_id,),
    ).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))


@admin_kb_bp.post("/kb/ayush/articles")
@jwt_required()
def create_ayush_article():
    data = request.get_json() or {}
    slug = (data.get("slug") or "").strip()
    title_en = (data.get("title_en") or "").strip()
    body_en = (data.get("body_en") or "").strip()
    keywords_en = (data.get("keywords_en") or "").strip() or None

    if not slug or not title_en or not body_en:
        return jsonify({"error": "slug, title_en, body_en are required"}), 400

    ts = _now()
    db = get_db()
    tx_fields = _translate_article_fields(title_en, body_en, keywords_en)
    try:
        db.execute(
            """
            INSERT INTO ayush_kb_articles (
                slug,
                title_en, title_hi, title_mr,
                body_en, body_hi, body_mr,
                keywords_en, keywords_hi, keywords_mr,
                created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                slug,
                title_en, tx_fields.get("title_hi"), tx_fields.get("title_mr"),
                body_en, tx_fields.get("body_hi"), tx_fields.get("body_mr"),
                keywords_en, tx_fields.get("keywords_hi"), tx_fields.get("keywords_mr"),
                ts,
                ts,
            ),
        )
        db.commit()
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    row = db.execute("SELECT id, slug, title_en, updated_at FROM ayush_kb_articles WHERE slug = ?", (slug,)).fetchone()
    return jsonify(dict(row)), 201


@admin_kb_bp.put("/kb/ayush/articles/<int:article_id>")
@jwt_required()
def update_ayush_article(article_id: int):
    data = request.get_json() or {}

    slug = (data.get("slug") or "").strip()
    title_en = (data.get("title_en") or "").strip()
    body_en = (data.get("body_en") or "").strip()
    keywords_en = (data.get("keywords_en") or "").strip() or None

    if not slug or not title_en or not body_en:
        return jsonify({"error": "slug, title_en, body_en are required"}), 400

    db = get_db()
    row = db.execute("SELECT id FROM ayush_kb_articles WHERE id = ?", (article_id,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404

    # Preserve existing translations if new translation is unavailable
    existing = db.execute(
        "SELECT title_hi, title_mr, body_hi, body_mr, keywords_hi, keywords_mr FROM ayush_kb_articles WHERE id = ?",
        (article_id,),
    ).fetchone()

    tx_fields = _translate_article_fields(title_en, body_en, keywords_en)
    if existing:
        for k in ("title_hi", "title_mr", "body_hi", "body_mr", "keywords_hi", "keywords_mr"):
            if tx_fields.get(k) is None:
                tx_fields[k] = existing[k]

    db.execute(
        """
        UPDATE ayush_kb_articles
        SET slug = ?,
            title_en = ?, title_hi = ?, title_mr = ?,
            body_en = ?, body_hi = ?, body_mr = ?,
            keywords_en = ?, keywords_hi = ?, keywords_mr = ?,
            updated_at = ?
        WHERE id = ?
        """,
        (
            slug,
            title_en, tx_fields.get("title_hi"), tx_fields.get("title_mr"),
            body_en, tx_fields.get("body_hi"), tx_fields.get("body_mr"),
            keywords_en, tx_fields.get("keywords_hi"), tx_fields.get("keywords_mr"),
            _now(),
            article_id,
        ),
    )
    db.commit()

    updated = db.execute(
        "SELECT id, slug, title_en, body_en, keywords_en, updated_at FROM ayush_kb_articles WHERE id = ?",
        (article_id,),
    ).fetchone()
    return jsonify(dict(updated))


@admin_kb_bp.delete("/kb/ayush/articles/<int:article_id>")
@jwt_required()
def delete_ayush_article(article_id: int):
    db = get_db()
    db.execute("DELETE FROM ayush_kb_articles WHERE id = ?", (article_id,))
    db.commit()
    return jsonify({"ok": True})


@admin_kb_bp.get("/kb/ayush/nav")
@jwt_required()
def get_admin_ayush_nav():
    db = get_db()
    row = db.execute("SELECT nav_json, updated_at FROM ayush_kb_nav WHERE key = ?", ("ayush",)).fetchone()
    if not row:
        return jsonify({"nav_json": "[]", "updated_at": None})
    return jsonify({"nav_json": row["nav_json"], "updated_at": row["updated_at"]})


@admin_kb_bp.put("/kb/ayush/nav")
@jwt_required()
def update_admin_ayush_nav():
    data = request.get_json() or {}
    nav_json = data.get("nav_json")
    if nav_json is None:
        return jsonify({"error": "nav_json is required"}), 400

    # Validate JSON
    try:
        parsed = json.loads(nav_json) if isinstance(nav_json, str) else nav_json
        nav_json_str = json.dumps(parsed, ensure_ascii=False)
    except Exception as exc:
        return jsonify({"error": f"Invalid JSON: {exc}"}), 400

    # Generate stored translations for nav (hi/mr)
    nav_list = None
    try:
        nav_list = json.loads(nav_json_str)
    except Exception:
        nav_list = None

    nav_hi, nav_mr = (None, None)
    if isinstance(nav_list, list):
        nav_hi, nav_mr = _translate_nav(nav_list)

    db = get_db()
    db.execute(
        """
        INSERT OR REPLACE INTO ayush_kb_nav (
            key, nav_json, nav_json_en, nav_json_hi, nav_json_mr, updated_at
        ) VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("ayush", nav_json_str, nav_json_str, nav_hi, nav_mr, _now()),
    )
    db.commit()
    return jsonify({"ok": True})


@admin_kb_bp.post("/kb/ayush/regenerate")
@jwt_required()
def regenerate_kb_translations():
    """Generate missing Hindi/Marathi translations for all KB content.

    This avoids per-request translation cost.
    """
    if not Config.ENABLE_I18N_TRANSLATION:
        return jsonify({"ok": True, "skipped": True, "reason": "i18n disabled"})

    db = get_db()
    rows = db.execute(
        """
        SELECT id, title_en, body_en, keywords_en, title_hi, title_mr, body_hi, body_mr
        FROM ayush_kb_articles
        """
    ).fetchall()

    updated = 0
    for r in rows:
        need_hi = not (r["title_hi"] or "").strip() or not (r["body_hi"] or "").strip()
        need_mr = not (r["title_mr"] or "").strip() or not (r["body_mr"] or "").strip()
        if not (need_hi or need_mr):
            continue

        tx_fields = _translate_article_fields(r["title_en"], r["body_en"], r["keywords_en"])
        db.execute(
            """
            UPDATE ayush_kb_articles
            SET title_hi = COALESCE(NULLIF(title_hi, ''), ?),
                body_hi  = COALESCE(NULLIF(body_hi, ''), ?),
                title_mr = COALESCE(NULLIF(title_mr, ''), ?),
                body_mr  = COALESCE(NULLIF(body_mr, ''), ?),
                updated_at = ?
            WHERE id = ?
            """,
            (
                tx_fields.get("title_hi") or r["title_hi"],
                tx_fields.get("body_hi") or r["body_hi"],
                tx_fields.get("title_mr") or r["title_mr"],
                tx_fields.get("body_mr") or r["body_mr"],
                _now(),
                r["id"],
            ),
        )
        updated += 1

    # Nav
    nav_row = db.execute(
        "SELECT nav_json_en, nav_json FROM ayush_kb_nav WHERE key = ?",
        ("ayush",),
    ).fetchone()
    if nav_row:
        nav_json_en = (nav_row["nav_json_en"] or nav_row["nav_json"] or "[]")
        try:
            nav_list = json.loads(nav_json_en)
        except Exception:
            nav_list = None
        if isinstance(nav_list, list):
            nav_hi, nav_mr = _translate_nav(nav_list)
            db.execute(
                "UPDATE ayush_kb_nav SET nav_json_en = ?, nav_json_hi = ?, nav_json_mr = ?, updated_at = ? WHERE key = ?",
                (nav_json_en, nav_hi, nav_mr, _now(), "ayush"),
            )

    db.commit()
    return jsonify({"ok": True, "articles_updated": updated})
