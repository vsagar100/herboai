# blueprints/admin.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import Session
from database import get_session
from models import AdminUser
from utils.security import admin_required

bp = Blueprint("admin", __name__, url_prefix="/api/admin")

@bp.post("/users")
@admin_required
def create_admin():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if not username or not password:
        return jsonify({"error": "username/password required"}), 400
    db: Session = next(get_session())
    if db.query(AdminUser).filter_by(username=username).first():
        return jsonify({"error": "username exists"}), 409
    u = AdminUser(username=username, password_hash=generate_password_hash(password))
    db.add(u); db.commit()
    return jsonify({"id": u.id})
