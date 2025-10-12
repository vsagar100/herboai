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
        "uses": p.uses if isinstance(p.uses, list) else [],
        "phytochemicals": p.phytochemicals,
        "dosage": p.dosage,
        "contraindications": p.contraindications,
        "formulations": p.formulations,
        "description": p.description,
        "properties": p.properties,
        "preparation": getattr(p, 'preparation', None),
        "images": [{"id": im.id, "path": im.file_path, "alt": im.alt_text} for im in p.images],
        "image_path": os.path.join(current_app.config["UPLOAD_FOLDER"], p.images[0].file_path) if p.images else None,
        "languages_json": p.languages_json,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }
    return data

@bp.get("")
def list_plants():
    """
    List all plants with optional pagination.
    Query params:
    - per_page: items per page (default 10)
    - page: page number (default 1)
    - q: search query (optional)
    """
    q = (request.args.get("q") or "").strip()
    
    # Parse pagination parameters explicitly
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    
    # Calculate offset
    offset = (page - 1) * per_page
    limit = per_page
    
    print(f"DEBUG: Received params - page={page}, per_page={per_page}, q='{q}'")
    
    db = next(get_session())
    
    # Start with base query
    query = db.query(Plant)
    
    # Apply search filter if provided
    if q:
        like = f"%{q}%"
        query = query.filter(
            (Plant.name.ilike(like)) | 
            (Plant.scientific_name.ilike(like)) | 
            (Plant.synonyms.ilike(like))
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination and fetch results
    plants = query.order_by(Plant.name).offset(offset).limit(limit).all()
    
    # Calculate total pages
    pages = (total + per_page - 1) // per_page if per_page > 0 else 1
    
    print(f"DEBUG: Returning {len(plants)} plants out of {total} total")
    
    return jsonify({
        "items": [plant_to_dict(p) for p in plants],
        "plants": [plant_to_dict(p) for p in plants],  # backward compatibility
        "total": total,
        "pages": pages,
        "page": page,
        "per_page": per_page
    })

@bp.get("/<int:plant_id>")
def get_plant(plant_id):
    """Get a single plant by ID"""
    db = next(get_session())
    p = db.get(Plant, plant_id)
    
    if not p:
        return jsonify({"error": "Plant not found"}), 404
    
    return jsonify(plant_to_dict(p))

@bp.post("")
@admin_required
def create_plant():
    """Create a new plant (admin only)"""
    db: Session = next(get_session())
    data = request.get_json()
    
    # Validate required fields
    if not data.get('name'):
        return jsonify({"error": "Plant name is required"}), 400
    
    p = Plant(**data)
    db.add(p)
    db.commit()
    db.refresh(p)
    
    return jsonify({"id": p.id, "plant": plant_to_dict(p)}), 201

@bp.put("/<int:plant_id>")
@admin_required
def update_plant(plant_id):
    """Update an existing plant (admin only)"""
    db: Session = next(get_session())
    p = db.get(Plant, plant_id)
    
    if not p:
        return jsonify({"error": "Plant not found"}), 404
    
    data = request.get_json()
    
    # Update only provided fields
    for k, v in data.items():
        if hasattr(p, k):
            setattr(p, k, v)
    
    db.commit()
    db.refresh(p)
    
    return jsonify({"ok": True, "plant": plant_to_dict(p)})

@bp.delete("/<int:plant_id>")
@admin_required
def delete_plant(plant_id):
    """Delete a plant (admin only)"""
    db: Session = next(get_session())
    p = db.get(Plant, plant_id)
    
    if not p:
        return jsonify({"error": "Plant not found"}), 404
    
    # Delete associated images from disk
    for img in p.images:
        try:
            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], img.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting image file: {e}")
    
    db.delete(p)
    db.commit()
    
    return jsonify({"ok": True})

@bp.post("/upload-image/<int:plant_id>")
@admin_required
def upload_image(plant_id):
    """Upload an image for a plant (admin only)"""
    db: Session = next(get_session())
    p = db.get(Plant, plant_id)
    
    if not p:
        return jsonify({"error": "Plant not found"}), 404
    
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    
    file = request.files["file"]
    
    if not file.filename:
        return jsonify({"error": "Empty filename"}), 400

    # Validate file extension
    ext = file.filename.rsplit(".", 1)[-1].lower()
    allowed = set(current_app.config["ALLOWED_IMAGE_EXT"].split(","))
    
    if ext not in allowed:
        return jsonify({"error": f"Unsupported extension: {ext}. Allowed: {', '.join(allowed)}"}), 400

    # Generate unique filename
    fname = f"{uuid.uuid4().hex}.{ext}"
    dest = os.path.join(current_app.config["UPLOAD_FOLDER"], fname)
    
    # Ensure upload directory exists
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    
    # Save file
    file.save(dest)

    # Create image record
    alt_text = request.form.get("alt_text", f"{p.name} image")
    im = Image(plant_id=plant_id, file_path=fname, alt_text=alt_text)
    db.add(im)
    db.commit()
    db.refresh(im)
    
    return jsonify({
        "ok": True,
        "image_id": im.id, 
        "file_path": fname,
        "image": {"id": im.id, "path": im.file_path, "alt": im.alt_text}
    }), 201