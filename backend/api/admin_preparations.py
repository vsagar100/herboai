# backend/blueprints/preparations.py
from flask import Blueprint, request, jsonify, current_app
import sqlite3, json
from db import get_db

admin_prep_bp = Blueprint("preparations", __name__, url_prefix="/api/preparations")

def _json_or_null(value):
    """Accept list/dict/None/str and always return a valid JSON string or None."""
    if value is None or value == "":
        return None
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    # If string, try to parse; if valid JSON keep as-is; else treat as text (wrap)
    try:
        parsed = json.loads(value)
        return json.dumps(parsed, ensure_ascii=False)
    except Exception:
        # Wrap plain text into JSON array for array fields; caller chooses correctly.
        return json.dumps(value, ensure_ascii=False)

def _normalize_arrays(payload):
    """
    Ensure array JSON fields are always valid JSON text in DB:
      - preparation_steps: JSON array of strings
      - equipment_needed:  JSON array of strings (nullable)
      - dosage_json:       JSON object with {"adult": "...", "child": "..."} (nullable)
    """
    steps = payload.get("preparation_steps", [])
    if isinstance(steps, str):
        try:
            steps = json.loads(steps)
        except Exception:
            # split by newline or semicolon as a fallback
            steps = [s.strip() for s in steps.replace("\r", "").split("\n") if s.strip()]
    if not isinstance(steps, list):
        steps = [str(steps)]
    payload["preparation_steps"] = json.dumps(steps, ensure_ascii=False)

    equip = payload.get("equipment_needed")
    if equip in (None, "", []):
        payload["equipment_needed"] = None
    else:
        if isinstance(equip, str):
            try:
                equip = json.loads(equip)
            except Exception:
                equip = [s.strip() for s in equip.replace("\r", "").split("\n") if s.strip()]
        if not isinstance(equip, list):
            equip = [str(equip)]
        payload["equipment_needed"] = json.dumps(equip, ensure_ascii=False)

    dosage = payload.get("dosage_json")
    if dosage in (None, "", {}):
        payload["dosage_json"] = None
    else:
        if isinstance(dosage, str):
            dosage = json.loads(dosage)
        if not isinstance(dosage, dict):
            raise ValueError("dosage_json must be an object with keys like 'adult'/'child'")
        payload["dosage_json"] = json.dumps(dosage, ensure_ascii=False)

    return payload

def _row_to_dict(row):
    d = dict(row)
    # Parse JSON fields to Python types for responses
    for k in ("preparation_steps", "equipment_needed", "dosage_json"):
        if d.get(k):
            try:
                d[k] = json.loads(d[k])
            except Exception:
                pass
    return d

@admin_prep_bp.get("/preparations")
def list_preparations():
    q = request.args.get("q", "").strip()
    form_type = request.args.get("form_type", "").strip()
    category = request.args.get("category", "").strip()
    limit = int(request.args.get("limit", 20))
    offset = int(request.args.get("offset", 0))

    sql = "SELECT * FROM preparations WHERE 1=1"
    params = []
    if q:
        sql += " AND (name_en LIKE ? OR classical_name LIKE ?)"
        like = f"%{q}%"
        params.extend([like, like])
    if form_type:
        sql += " AND form_type = ?"
        params.append(form_type)
    if category:
        sql += " AND category = ?"
        params.append(category)
    sql += " ORDER BY name_en ASC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    conn = get_db()
    rows = conn.execute(sql, params).fetchall()
    total = conn.execute("SELECT COUNT(*) FROM preparations").fetchone()[0]
    data = [_row_to_dict(r) for r in rows]
    return jsonify({"items": data, "total": total})

@admin_prep_bp.get("/preparations/<int:prep_id>")
def get_preparation(prep_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM preparations WHERE id=?", (prep_id,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(_row_to_dict(row))

@admin_prep_bp.post("/preparations")
def create_preparation():
    try:
        payload = request.get_json(force=True, silent=False) or {}
        required = ["name_en", "form_type", "preparation_steps"]
        for r in required:
            if not payload.get(r):
                return jsonify({"error": f"Missing field: {r}"}), 400

        payload = _normalize_arrays(payload)

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO preparations
            (name_en, name_hi, name_mr, classical_name, ayush_system, form_type, category,
             preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
             dosage_json, timing, anupana, notes)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            payload.get("name_en"),
            payload.get("name_hi"),
            payload.get("name_mr"),
            payload.get("classical_name"),
            payload.get("ayush_system"),
            payload.get("form_type"),
            payload.get("category"),
            payload.get("preparation_steps"),
            payload.get("equipment_needed"),
            payload.get("duration"),
            payload.get("yield"),
            payload.get("storage"),
            payload.get("shelf_life"),
            payload.get("dosage_json"),
            payload.get("timing"),
            payload.get("anupana"),
            payload.get("notes"),
        ))
        conn.commit()
        new_id = cur.lastrowid
        row = conn.execute("SELECT * FROM preparations WHERE id=?", (new_id,)).fetchone()
        return jsonify(_row_to_dict(row)), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except sqlite3.IntegrityError as ie:
        return jsonify({"error": f"Integrity error: {ie}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500

@admin_prep_bp.put("/preparations/<int:prep_id>")
def update_preparation(prep_id):
    try:
        payload = request.get_json(force=True, silent=False) or {}

        # Only normalize keys that may exist; allow partial updates
        fields = [
            "name_en","name_hi","name_mr","classical_name","ayush_system",
            "form_type","category","preparation_steps","equipment_needed",
            "duration","yield","storage","shelf_life","dosage_json",
            "timing","anupana","notes"
        ]
        # If JSON fields appear, normalize; else leave untouched
        to_update = {}
        for f in fields:
            if f in payload:
                to_update[f] = payload[f]

        # Normalize JSON fields if present
        touch_json = any(k in to_update for k in ("preparation_steps","equipment_needed","dosage_json"))
        if touch_json:
            to_update = _normalize_arrays(to_update)

        if not to_update:
            return jsonify({"error": "No fields to update"}), 400

        sets = []
        params = []
        for k, v in to_update.items():
            sets.append(f"{k}=?")
            params.append(v)
        params.append(prep_id)

        conn = get_db()
        cur = conn.cursor()
        cur.execute(f"UPDATE preparations SET {', '.join(sets)} WHERE id=?", params)
        if cur.rowcount == 0:
            return jsonify({"error": "Not found"}), 404
        conn.commit()

        row = conn.execute("SELECT * FROM preparations WHERE id=?", (prep_id,)).fetchone()
        return jsonify(_row_to_dict(row))
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except sqlite3.IntegrityError as ie:
        return jsonify({"error": f"Integrity error: {ie}"}), 400
    except Exception as e:
        return jsonify({"error": f"Server error: {e}"}), 500

@admin_prep_bp.delete("/preparations/<int:prep_id>")
def delete_preparation(prep_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM preparations WHERE id=?", (prep_id,))
    if cur.rowcount == 0:
        return jsonify({"error": "Not found"}), 404
    conn.commit()
    return jsonify({"ok": True, "deleted_id": prep_id})
