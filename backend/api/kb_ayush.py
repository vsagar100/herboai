from __future__ import annotations

from flask import Blueprint, request, jsonify

from services.ayush_kb import get_ayush_nav, get_article
from utils.i18n import normalize_lang

kb_ayush_bp = Blueprint("kb_ayush", __name__)


@kb_ayush_bp.get("/kb/ayush/nav")
def ayush_nav():
    lang = normalize_lang(request.args.get("lang", "en"))
    return jsonify({"nav": get_ayush_nav(lang)})


@kb_ayush_bp.get("/kb/ayush/article/<slug>")
def ayush_article(slug: str):
    lang = normalize_lang(request.args.get("lang", "en"))
    article = get_article(slug, lang)
    if not article:
        return jsonify({"error": "Not found"}), 404
    return jsonify(article)
