# backend/api/mt_health.py
"""
Translation health + microservice endpoints backed by IndicTrans2.
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

from flask import Blueprint, Response, jsonify, request

from services.indic_translation_service import (
    LANG_CODE_MAP,
    get_indic_translation_service,
)

bp = Blueprint("mt", __name__)
translator = get_indic_translation_service()


@bp.get("/mt/health")
def mt_health():
    """Simple heartbeat exposing supported languages."""
    return jsonify(
        {
            "ok": True,
            "engine": "IndicTrans2",
            "languages": sorted(LANG_CODE_MAP.keys()),
        }
    )


# -----------------------------------------------------------------------------
# Optional standalone Flask app (used when running `python api/mt_health.py`)
# -----------------------------------------------------------------------------

try:
    from flask import Flask

    _STANDALONE = True
except Exception:  # pragma: no cover - Flask always available in app
    _STANDALONE = False


if _STANDALONE:
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False

    try:
        from flask_cors import CORS

        CORS(app, resources={r"/api/*": {"origins": "*"}})
    except Exception:
        pass

    log = logging.getLogger("mt_service")
    logging.basicConfig(level=logging.INFO)

    def _json_response(payload: Any, status: int = 200) -> Response:
        body = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
        return Response(body, status=status, mimetype="application/json; charset=utf-8")

    @app.get("/api/mt/health")
    def standalone_health():
        return _json_response(
            {"ok": True, "engine": "IndicTrans2", "languages": sorted(LANG_CODE_MAP)}
        )

    @app.post("/api/mt/translate")
    def mt_translate():
        """
        Translate JSON values only; keep keys/structure intact.
        Body JSON:
        {
          "json": {...},              // required
          "target_lang": "hi",        // required (hi/mr/en/...)
          "source_lang": "en"         // optional (default "en")
        }
        """
        try:
            body: Dict[str, Any] = request.get_json(force=True, silent=False)
        except Exception as exc:  # pragma: no cover - handled at runtime
            log.exception("Invalid JSON")
            return _json_response({"error": f"Invalid JSON body: {exc}"}, 400)

        if not isinstance(body, dict):
            return _json_response({"error": "Body must be a JSON object."}, 400)

        payload_json = body.get("json")
        target_lang = body.get("target_lang")
        source_lang = body.get("source_lang", "en")

        if payload_json is None:
            return _json_response({"error": "Missing 'json' field to translate."}, 400)
        if not target_lang or target_lang not in LANG_CODE_MAP:
            return _json_response(
                {"error": f"Invalid 'target_lang'. Allowed: {sorted(LANG_CODE_MAP)}"},
                400,
            )
        if source_lang not in LANG_CODE_MAP:
            return _json_response(
                {"error": f"Invalid 'source_lang'. Allowed: {sorted(LANG_CODE_MAP)}"},
                400,
            )

        try:
            translated = translator.translate_values(payload_json, source_lang, target_lang)
            return _json_response(
                {
                    "ok": True,
                    "engine": "IndicTrans2",
                    "source_lang": source_lang,
                    "target_lang": target_lang,
                    "json": translated,
                }
            )
        except Exception as exc:  # pragma: no cover - runtime error surface
            log.exception("Translation error")
            return _json_response({"error": f"Translation failed: {exc}"}, 500)

    if __name__ == "__main__":  # pragma: no cover - manual runs only
        app.run(host="0.0.0.0", port=5000, debug=False)
