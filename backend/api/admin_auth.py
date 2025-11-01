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
    username = data.get("username", "").strip()
    password = data.get("password", "")
    
    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400
    
    db = get_db()
    user = db.execute(
        "SELECT * FROM admin_users WHERE username = ?", (username,)
    ).fetchone()
    
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Verify password
    if not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # IMPORTANT: Use string as identity, not dict
    token = create_access_token(identity=username)  # <-- Changed from object to string
    
    return jsonify({
        "token": token,
        "username": username
    }), 200

# --------------------------------------------
# AUTH CHECK
# --------------------------------------------
@admin_auth_bp.get("/me")
@jwt_required()
def admin_me():
    username = get_jwt_identity()  # This is now a string
    
    # Fetch user details from DB
    db = get_db()
    user = db.execute(
        "SELECT id, username FROM admin_users WHERE username = ?", 
        (username,)
    ).fetchone()
    
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    return jsonify({
        "id": user["id"],
        "username": user["username"],
        "is_admin": True
    })
