# blueprints/chat.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import load_only
from database import get_session
from services.nlu import parse_intent, search_remedies, detect_lang, normalize, hybrid_retrieve
from models import Plant, Remedy
from services.i18n import pick_locale, maybe_translate
from services.rag_service import RAGService

# OPTIONAL semantic fallback (safe even if not configured)
try:
    from services import semantic
    _SEMANTIC_OK = True
except Exception:
    semantic = None
    _SEMANTIC_OK = False

_rag = RAGService(Plant, Remedy)
try:
    _rag._load_embedding_model()
except Exception:
    pass

bp = Blueprint("chat", __name__, url_prefix="/api")


def _plant_payload(plant: Plant, target_lang: str) -> dict:
    """Build a localized plant response."""
    base = {
        "type": "plant",
        "plant": {
            "id": plant.id,
            "name": plant.name,
            "scientific_name": plant.scientific_name,
            "ayush_system": plant.ayush_system,
            "category": plant.category,
            "synonyms": plant.synonyms,
            "parts_used": plant.parts_used,
            "uses": plant.uses,
            "phytochemicals": plant.phytochemicals,
            "dosage": plant.dosage,
            "contraindications": plant.contraindications,
            "formulations": plant.formulations,
            "description": plant.description,
            "properties": plant.properties,
            "taste": plant.taste,
            "dosha": plant.dosha,
            "therapeutic_uses": plant.therapeutic_uses,
            "images": [{"path": im.file_path, "alt": im.alt_text} for im in plant.images],
        }
    }
    # overlay multilingual fields if present
    loc = pick_locale(plant.languages_json, target_lang)
    if isinstance(loc, dict):
        for k, v in loc.items():
            if k in base["plant"] and isinstance(v, str) and v.strip():
                base["plant"][k] = v

    # optional last-mile translate (keeps local-first content)
    for key in ["uses", "dosage", "contraindications", "description", "properties", "formulations", "parts_used", "category"]:
        base["plant"][key] = maybe_translate(base["plant"].get(key), target_lang)

    return base


def _remedies_payload(remedies, db, target_lang: str) -> dict:
    """Build a localized remedies list payload."""
    out = []
    for r in remedies:
        # collect related plants
        related = []
        ids = []
        try:
            ids = [int(x) for x in (r.plant_ids or "").replace(" ", "").split(",") if x]
        except Exception:
            ids = []
        if ids:
            plist = db.query(Plant).filter(Plant.id.in_(ids)).all()
            for p in plist:
                loc = pick_locale(p.languages_json, target_lang) or {}
                related.append({
                    "id": p.id,
                    "name": loc.get("name") or p.name,
                    "scientific_name": p.scientific_name,
                    "images": [{"path": im.file_path, "alt": im.alt_text} for im in p.images],
                })

        loc = pick_locale(r.languages_json, target_lang) or {}
        item = {
            "symptom": loc.get("symptom") or r.symptom,
            "preparation": maybe_translate(loc.get("preparation") or r.preparation, target_lang),
            "dosage": maybe_translate(loc.get("dosage") or r.dosage, target_lang),
            "side_effects": maybe_translate(loc.get("side_effects") or r.side_effects, target_lang),
            "contraindications": maybe_translate(loc.get("contraindications") or r.contraindications, target_lang),
            "lifestyle_recommendations": maybe_translate(loc.get("lifestyle_recommendations") or r.lifestyle_recommendations, target_lang),
            "plants": related,
            "ayush_system": r.ayush_system,
        }
        out.append(item)
    return {"type": "remedies", "items": out, "lang": target_lang}

def _plant_card(p):
    return {
        "id": p.id,
        "name": p.name,
        "scientific_name": p.scientific_name,
        "ayush_system": p.ayush_system,
        "category": p.category,
        "parts_used": p.parts_used,
        "uses": p.uses,
        "phytochemicals": p.phytochemicals,
        "dosage": p.dosage,
        "contraindications": p.contraindications,
        "formulations": p.formulations,
        "description": p.description,
        "properties": p.properties,
        "images": [{"path": im.file_path, "alt": im.alt_text} for im in p.images],
    }

    related = [_plant_card(p) for p in plants[:5]]


@bp.post("/chat")
def query():
    try:
        payload = request.get_json(silent=True) or {}
        text = (payload.get("text") or "").strip()
        # NEW: short-term context (previous user query) optionally passed by UI
        ctx = (payload.get("context") or "").strip()
        if ctx:
            text = f"{ctx}. {text}"

        if not text:
            return jsonify({"error": "Empty query"}), 400

        target_lang = (payload.get("lang") or "").strip().lower()
        if not target_lang:
            try:
                target_lang = detect_lang(text)
            except Exception:
                target_lang = "en"

        db = next(get_session())

        # === NEW: hybrid retrieval using FTS5 (+ canonical labels) ===
        q_norm = normalize(text)
        bundle = hybrid_retrieve(db, q_norm, target_lang, plant_limit=5, remedy_limit=3)
        plants = bundle.get("plants") or []
        remedies = bundle.get("remedies") or []

        # If the user clearly asked *about a specific plant*, still allow the detailed single-plant view
        intent, plant = parse_intent(db, text)
        if intent == "plant" and plant and (not remedies) and (plants[:1] and plants[0].id == plant.id):
            return jsonify(_plant_payload(plant, target_lang))

        # === Consolidated “LLM-like” answer, with semantic re-ranking if model loaded ===
        answer_text = _rag.generate_response(text, plants, remedies)

        # Build a compact related plants list for the UI card strip
        related = []
        for p in plants[:5]:
            related.append({
                "id": p.id,
                "name": p.name,
                "scientific_name": p.scientific_name,
                "images": [{"path": im.file_path, "alt": im.alt_text} for im in p.images],
            })

        # NEW: a generic 'answer' type the UI can render like a chat completion
        return jsonify({
            "type": "answer",
            "text": answer_text,
            "plants": related,
            "lang": target_lang
        }), 200

    except Exception as e:
        from traceback import format_exc
        print("QUERY_ERROR:", e, "\n", format_exc())
        return jsonify({"error": "Unhandled server error"}), 500