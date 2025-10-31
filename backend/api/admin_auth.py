from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from db import get_db

admin_auth_bp = Blueprint("api/auth", __name__)

# --------------------------------------------
# CREATE ADMIN USER (super-admin only / initial setup)
# --------------------------------------------
@admin_auth_bp.post("/create_admin")
def create_admin():
    data = request.get_json() or {}
    name = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not (name and email and password):
        return jsonify({"error": "name, email, and password are required"}), 400

    db = get_db()
    cur = db.execute("SELECT id FROM admin_users WHERE email=?", (email,))
    if cur.fetchone():
        return jsonify({"error": "Admin already exists"}), 400

    pw_hash = generate_password_hash(password)
    db.execute(
        "INSERT INTO admin_users (username, email, password_hash) VALUES (?, ?, ?)",
        (name, email, pw_hash),
    )
    db.commit()

    return jsonify({"message": f"Admin user {name} created successfully."}), 201


# --------------------------------------------
# LOGIN ENDPOINT
# --------------------------------------------
@admin_auth_bp.post("/login")
def admin_login():
    data = request.get_json() or {}
    username = data.get("username", "").strip().lower()
    password = data.get("password", "").strip()

    print("Login attempt for user:", username)
    db = get_db()
    row = db.execute(
        "SELECT id, username, email, password_hash, is_active FROM admin_users WHERE username=?", (username,)
    ).fetchone()
    print(row)
    if not row:
        return jsonify({"error": "Invalid credentials"}), 401
    if not row["is_active"]:
        return jsonify({"error": "User deactivated"}), 403
    if not check_password_hash(row["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(
        identity={"id": row["id"], "username": row["username"] },
        expires_delta=timedelta(hours=12),
    )

    return jsonify({"token": token, "name": row["username"], "is_active": row["is_active"]})


# --------------------------------------------
# AUTH CHECK
# --------------------------------------------
@admin_auth_bp.get("/me")
@jwt_required()
def admin_me():
    user = get_jwt_identity()
    return jsonify(user)
