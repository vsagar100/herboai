# blueprints/admin_plants.py
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from datetime import datetime
import os, json, sqlite3

from db import get_db

admin_plants_bp = Blueprint("admin_plants", __name__)

# ------------------- helpers -------------------
JSON_FIELDS = [
    "parts_used", "rasa", "guna", "therapeutic_actions",
    "active_compounds", "classical_references", "dosha_effect"
]

def _js(v):
    # stringify Python lists/dicts → JSON; pass-through for None/str
    if v is None:
        return None
    if isinstance(v, (list, dict)):
        return json.dumps(v, ensure_ascii=False)
    return v

def _coerce_payload(data: dict) -> dict:
    """Coerce incoming payload to DB-friendly structure."""
    out = {}
    # Required
    if "botanical_name" in data: out["botanical_name"] = data["botanical_name"].strip()
    # Optional basics
    for k in [
        "common_name_en","common_name_hi","common_name_mr","sanskrit_name",
        "family","description","habitat","virya","vipaka","prabhava",
        "ayush_system","cultivation_status","image_hero"
    ]:
        if k in data: out[k] = data[k]
    # JSON-ish fields
    for k in JSON_FIELDS:
        if k in data: out[k] = _js(data[k])
    # Booleans/ints
    if "is_endangered" in data: out["is_endangered"] = int(bool(data["is_endangered"]))
    # Explicitly ignore ayush_system_id (deprecated)
    # timestamps
    out["updated_at"] = datetime.utcnow().isoformat(sep=" ", timespec="seconds")
    return out

def _row_to_obj(row: sqlite3.Row) -> dict:
    d = dict(row)
    # Parse JSON-ish columns back to native
    for k in JSON_FIELDS:
        if d.get(k):
            try: d[k] = json.loads(d[k])
            except Exception: pass
    return d

# ------------------- PUBLIC READ APIs -------------------
@admin_plants_bp.get("/plants")
def public_list_plants():
    """Public list with search/pagination."""
    db = get_db()
    q = (request.args.get("q") or "").strip()
    page = max(1, int(request.args.get("page", 1)))
    size = max(1, min(100, int(request.args.get("size", 10))))
    offset = (page - 1) * size

    if q:
        # Prefer FTS if you’ve created plants_fts, else LIKE fallback
        try:
            items = db.execute(
                """
                SELECT p.* FROM plants_fts f
                JOIN plants p ON p.id = f.rowid
                WHERE plants_fts MATCH ?
                ORDER BY lower(coalesce(p.common_name_en, p.botanical_name)) ASC
                """,
                (q, size, offset)
            ).fetchall()
            # count is approximate; do a quick LIKE fallback for count
            cnt = db.execute(
                "SELECT COUNT(*) AS c FROM plants WHERE botanical_name LIKE ? OR common_name_en LIKE ?",
                (f"%{q}%", f"%{q}%")
            ).fetchone()["c"]
        except Exception:
            items = db.execute(
                """
                SELECT * FROM plants
                WHERE botanical_name LIKE ? OR common_name_en LIKE ?
                ORDER BY lower(coalesce(common_name_en, botanical_name)) ASC LIMIT ? OFFSET ?
                """,
                (f"%{q}%", f"%{q}%", size, offset)
            ).fetchall()
            cnt = db.execute(
                "SELECT COUNT(*) AS c FROM plants WHERE botanical_name LIKE ? OR common_name_en LIKE ?",
                (f"%{q}%", f"%{q}%")
            ).fetchone()["c"]
    else:
        items = db.execute(
            "SELECT * FROM plants ORDER BY lower(coalesce(common_name_en, botanical_name)) ASC LIMIT ? OFFSET ?",
            (size, offset)
        ).fetchall()
        cnt = db.execute("SELECT COUNT(*) AS c FROM plants").fetchone()["c"]

    return jsonify({
        "items": [_row_to_obj(r) for r in items],
        "count": cnt,
        "page": page,
        "size": size,
    })


@admin_plants_bp.get("/plants/<int:plant_id>")
def public_get_plant(plant_id: int):
    db = get_db()
    row = db.execute("SELECT * FROM plants WHERE id=?", (plant_id,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(_row_to_obj(row))

# Optional: serve image files if image_hero stores relative paths like "plant_images/gudmar.jpg"
@admin_plants_bp.get("/files/<path:relpath>")
def serve_file(relpath):
    base = current_app.config.get("FILE_ROOT", os.path.join(current_app.root_path, "files"))
    full = os.path.abspath(os.path.join(base, relpath))
    if not full.startswith(os.path.abspath(base)) or not os.path.exists(full):
        return jsonify({"error": "file not found"}), 404
    directory, filename = os.path.split(full)
    return send_from_directory(directory, filename)

# ------------------- ADMIN CRUD (JWT protected) -------------------
@admin_plants_bp.post("/admin/plants")
@jwt_required()
def admin_create_plant():
    print("Create plant request received")
    try:
        data = request.get_json() or {}
        if not data.get("botanical_name"):
            return jsonify({"error": "botanical_name is required"}), 400

        payload = _coerce_payload(data)
        # enforce uniqueness on botanical_name
        db = get_db()
        exists = db.execute("SELECT id FROM plants WHERE lower(botanical_name)=lower(?)",
                            (payload["botanical_name"],)).fetchone()
        if exists:
            return jsonify({"error": "botanical_name already exists"}), 409

        cols = ", ".join(payload.keys())
        qs = ", ".join(["?"] * len(payload))
        db.execute(f"INSERT INTO plants ({cols}) VALUES ({qs})", tuple(payload.values()))
        db.commit()

        new_id = db.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
        row = db.execute("SELECT * FROM plants WHERE id=?", (new_id,)).fetchone()
        return jsonify(_row_to_obj(row)), 201
    except Exception as e:
        print("Create plant error:", e)
        return jsonify({"error": "creation failed"}), 500


@admin_plants_bp.put("/plants/<int:plant_id>") 
@jwt_required()
def admin_update_plant(plant_id: int):
    print("Update plant ID:")
    data = request.get_json() or {}
    payload = _coerce_payload(data)
    print("Update payload:", payload)
    if not payload:
        return jsonify({"error": "nothing to update"}), 400

    # If botanical_name is changing, re-check uniqueness
    if "botanical_name" in payload:
        db = get_db()
        exists = db.execute("""SELECT id FROM plants
                               WHERE lower(botanical_name)=lower(?) AND id<>?""",
                            (payload["botanical_name"], plant_id)).fetchone()
        if exists:
            return jsonify({"error": "botanical_name already exists"}), 409

    # build UPDATE
    sets = ", ".join([f"{k}=?" for k in payload.keys()])
    db = get_db()
    cur = db.execute(f"UPDATE plants SET {sets} WHERE id=?", (*payload.values(), plant_id))
    if cur.rowcount == 0:
        return jsonify({"error": "Not found"}), 404
    db.commit()

    row = db.execute("SELECT * FROM plants WHERE id=?", (plant_id,)).fetchone()
    return jsonify(_row_to_obj(row))

@admin_plants_bp.delete("/plants/<int:plant_id>")
@jwt_required()
def admin_delete_plant(plant_id: int):
    db = get_db()
    cur = db.execute("DELETE FROM plants WHERE id=?", (plant_id,))
    if cur.rowcount == 0:
        return jsonify({"error": "Not found"}), 404
    db.commit()
    return jsonify({"status": "deleted", "id": plant_id})

# ------------------- optional: image upload -------------------
ALLOWED_EXT = {"jpg", "jpeg", "png", "webp"}

@admin_plants_bp.post("/uploads/plant-image")
@jwt_required()
def admin_upload_plant_image():
    """
    Upload an image and return a file path you can store in `plants.image_hero`.
    Client then calls PUT /admin/plants/:id with {"image_hero": "<returned_path>"}.
    """
    print("Upload request received")
    try:
        if "file" not in request.files:
            return jsonify({"error": "file missing"}), 400
        f = request.files["file"]
        if not f.filename:
            return jsonify({"error": "filename missing"}), 400

        ext = f.filename.rsplit(".", 1)[-1].lower()
        if ext not in ALLOWED_EXT:
            return jsonify({"error": "unsupported file type"}), 400

        root = current_app.config.get("FILE_ROOT", os.path.join(current_app.root_path, "files"))
        os.makedirs(root, exist_ok=True)

        safe_name = secure_filename(f.filename)
        save_path = os.path.join(root, safe_name)
        f.save(save_path)
        rel_path = os.path.relpath(save_path, root).replace("\\", "/")
        return jsonify({"path": rel_path})
    except Exception as e:
        print("Upload error:", e)
        return jsonify({"error": "upload failed."}), 500