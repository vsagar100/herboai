# blueprints/remedies.py
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from database import get_session
from models import Remedy, Plant
from utils.pagination import parse_pagination
from utils.security import admin_required

bp = Blueprint("remedies", __name__, url_prefix="/api/remedies")

def remedy_to_dict(r: Remedy):
    return {
        "id": r.id,
        "symptom": r.symptom,
        "plant_ids": r.plant_ids,
        "preparation": r.preparation,
        "dosage": r.dosage,
        "lifestyle_recommendations": r.lifestyle_recommendations,
        "preparation_method": r.preparation_method,
        "ayush_system": r.ayush_system,
        "side_effects": r.side_effects,
        "contraindications": r.contraindications,
        "languages_json": r.languages_json,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }

@bp.get("")
def list_remedies():
    q = (request.args.get("q") or "").strip()
    page, limit, offset = parse_pagination()
    db = next(get_session())
    query = db.get(Remedy)
    if q:
        like = f"%{q}%"
        query = query.filter((Remedy.symptom.ilike(like)) | (Remedy.preparation.ilike(like)) | (Remedy.dosage.ilike(like)))
    total = query.count()
    items = query.order_by(Remedy.symptom).offset(offset).limit(limit).all()
    return jsonify({"total": total, "items": [remedy_to_dict(r) for r in items]})

@bp.get("/by-plant/<int:plant_id>")
def remedies_by_plant(plant_id):
    db = next(get_session())
    like = f"%{plant_id}%"
    items = db.get(Remedy).filter(Remedy.plant_ids.ilike(like)).all()
    return jsonify([remedy_to_dict(r) for r in items])

@bp.post("")
@admin_required
def create_remedy():
    db: Session = next(get_session())
    data = request.get_json()
    r = Remedy(**data)
    db.add(r)
    db.commit()
    return jsonify({"id": r.id})

@bp.put("/<int:remedy_id>")
@admin_required
def update_remedy(remedy_id):
    db: Session = next(get_session())
    r = db.get(Remedy).get(remedy_id)
    if not r:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    for k, v in data.items():
        setattr(r, k, v)
    db.commit()
    return jsonify({"ok": True})

@bp.delete("/<int:remedy_id>")
@admin_required
def delete_remedy(remedy_id):
    db: Session = next(get_session())
    r = db.get(Remedy).get(remedy_id)
    if not r:
        return jsonify({"error": "Not found"}), 404
    db.delete(r)
    db.commit()
    return jsonify({"ok": True})
