# blueprints/auth.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from database import get_session
from models import AdminUser
from flask_jwt_extended import create_access_token

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()
    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    db = next(get_session())
    user = db.query(AdminUser).filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = create_access_token(identity=user.id)
    return jsonify({"token": token})

@bp.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()
    db = next(get_session())
    user = db.query(AdminUser).filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username
    })
