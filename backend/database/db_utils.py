# backend/utils/db_utils.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "ayush.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def fetch_all_herbs():
    """Fetches all herbs with relations as nested dicts"""
    conn = get_connection()
    cur = conn.cursor()

    # Main herbs
    cur.execute("SELECT * FROM herbs")
    herbs = [dict(row) for row in cur.fetchall()]

    # Common names
    cur.execute("SELECT * FROM common_names")
    common_names = {}
    for row in cur.fetchall():
        common_names.setdefault(row["herb_id"], []).append(row["name"])

    # Remedies
    cur.execute("SELECT * FROM remedies")
    remedies = {}
    for row in cur.fetchall():
        remedies.setdefault(row["herb_id"], []).append({
            "condition": row["condition_name"],
            "preparation": row["preparation"],
            "form": row["form"]
        })

    # Languages
    cur.execute("SELECT * FROM herb_languages")
    languages = {}
    for row in cur.fetchall():
        languages.setdefault(row["herb_id"], []).append({
            "lang": row["language_code"],
            "translation": row["translation"]
        })

    conn.close()

    # Merge all
    for herb in herbs:
        hid = herb["id"]
        herb["common_names"] = common_names.get(hid, [])
        herb["remedies"] = remedies.get(hid, [])
        herb["languages"] = {item["lang"]: item["translation"] for item in languages.get(hid, [])}

    return herbs
