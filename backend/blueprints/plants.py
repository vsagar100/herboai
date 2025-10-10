# blueprints/plants.py
import os, uuid, json
from flask import Blueprint, request, jsonify, current_app
from sqlalchemy.orm import Session
from database import get_session
from models import Plant, Image
from utils.pagination import parse_pagination
from utils.security import admin_required

bp = Blueprint("plants", __name__, url_prefix="/api/plants")

def plant_to_dict(p: Plant, locale="en"):
    data = {
        "id": p.id,
        "name": p.name,
        "scientific_name": p.scientific_name,
        "ayush_system": p.ayush_system,
        "category": p.category,
        "synonyms": p.synonyms,
        "parts_used": p.parts_used,
        "uses": p.uses,
        "phytochemicals": p.phytochemicals,
        "dosage": p.dosage,
        "contraindications": p.contraindications,
        "formulations": p.formulations,
        "description": p.description,
        "properties": p.properties,
        "images": [{"id": im.id, "path": im.file_path, "alt": im.alt_text} for im in p.images],
        "languages_json": p.languages_json,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }
    return data

@bp.get("")
def list_plants():
    q = (request.args.get("q") or "").strip()
    page, limit, offset = parse_pagination()
    db = next(get_session())
    query = db.get(Plant)
    if q:
        like = f"%{q}%"
        query = query.filter((Plant.name.ilike(like)) | (Plant.scientific_name.ilike(like)) | (Plant.synonyms.ilike(like)))
    total = query.count()
    plants = query.order_by(Plant.name).offset(offset).limit(limit).all()
    return jsonify({"total": total, "items": [plant_to_dict(p) for p in plants]})

@bp.get("/<int:plant_id>")
def get_plant(plant_id):
    db = next(get_session())
    p = db.get(Plant).get(plant_id)
    if not p:
        return jsonify({"error": "Not found"}), 404
    return jsonify(plant_to_dict(p))

@bp.post("")
@admin_required
def create_plant():
    db: Session = next(get_session())
    data = request.get_json()
    p = Plant(**data)
    db.add(p)
    db.commit()
    return jsonify({"id": p.id})

@bp.put("/<int:plant_id>")
@admin_required
def update_plant(plant_id):
    db: Session = next(get_session())
    p = db.get(Plant).get(plant_id)
    if not p:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    for k, v in data.items():
        setattr(p, k, v)
    db.commit()
    return jsonify({"ok": True})

@bp.delete("/<int:plant_id>")
@admin_required
def delete_plant(plant_id):
    db: Session = next(get_session())
    p = db.get(Plant).get(plant_id)
    if not p:
        return jsonify({"error": "Not found"}), 404
    db.delete(p)
    db.commit()
    return jsonify({"ok": True})

@bp.post("/upload-image/<int:plant_id>")
@admin_required
def upload_image(plant_id):
    db: Session = next(get_session())
    p = db.get(Plant).get(plant_id)
    if not p:
        return jsonify({"error": "Plant not found"}), 404
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files["file"]
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    ext = file.filename.rsplit(".", 1)[-1].lower()
    allowed = set(current_app.config["ALLOWED_IMAGE_EXT"].split(","))
    if ext not in allowed:
        return jsonify({"error": f"Unsupported extension: {ext}"}), 400

    fname = f"{uuid.uuid4().hex}.{ext}"
    dest = os.path.join(current_app.config["UPLOAD_FOLDER"], fname)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    file.save(dest)

    im = Image(plant_id=plant_id, file_path=fname, alt_text=f"{p.name} image")
    db.add(im)
    db.commit()
    return jsonify({"image_id": im.id, "file_path": fname})
