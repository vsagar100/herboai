from flask import Blueprint, jsonify, request
import sqlite3
from database.db_utils import fetch_all_herbs

herbs_bp = Blueprint("herbs", __name__)

def get_db():
    conn = sqlite3.connect("data/herbs.db")
    conn.row_factory = sqlite3.Row
    return conn

@herbs_bp.route("/herbs", methods=["GET"])
def list_herbs():
    herbs = fetch_all_herbs()
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
