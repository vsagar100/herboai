from flask import Blueprint, jsonify, request
import sqlite3

herbs_bp = Blueprint("herbs", __name__)

def get_db():
    conn = sqlite3.connect("data/herbs.db")
    conn.row_factory = sqlite3.Row
    return conn

@herbs_bp.route("/", methods=["GET"])
def list_herbs():
    conn = get_db()
    herbs = conn.execute("SELECT * FROM herbs").fetchall()
    return jsonify([dict(row) for row in herbs])

@herbs_bp.route("/", methods=["POST"])
def add_herb():
    data = request.json
    conn = get_db()
    conn.execute(
        "INSERT INTO herbs (name, uses, remedy) VALUES (?, ?, ?)",
        (data["name"], data["uses"], data["remedy"])
    )
    conn.commit()
    return jsonify({"status": "success"})
