# api/admin_diseases.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
import sqlite3
import re
import json

from db import get_db
from services.admin_i18n_indexer import admin_save_with_i18n


admin_diseases_bp = Blueprint("admin_diseases", __name__)

ARRAY_FIELDS = ["symptoms", "causes", "prevention_tips"]
OBJECT_FIELDS = ["dosha_involvement", "dhatu_involvement", "dietary_recommendations"]


# ---------- Helpers to normalize incoming JSON-ish data ----------
def _to_clean_list(value):
    """Coerce value into a clean list[str] with de-dupe and trimmed tokens."""
    if value is None:
        return []
    if isinstance(value, list):
        seq = value
    elif isinstance(value, str):
        s = value.strip()
        if not s:
            return []
        # Try strict JSON first
        try:
            parsed = json.loads(s)
            if isinstance(parsed, list):
                seq = parsed
            else:
                # Fall back to CSV/newline/semicolon split
                seq = re.split(r"[,\n;]+", s)
        except Exception:
            seq = re.split(r"[,\n;]+", s)
    else:
        # Unknown -> wrap as a single string item
        seq = [str(value)]

    cleaned = []
    for x in seq:
        t = "" if x is None else str(x).strip()
        if t:
            cleaned.append(t)

    # De-dup while preserving order
    seen = set()
    uniq = []
    for x in cleaned:
        if x not in seen:
            uniq.append(x)
            seen.add(x)
    return uniq


def _to_clean_obj(value):
    """Coerce value into a dict; invalid/empty -> {}."""
    if value is None or value == "":
        return {}
    if isinstance(value, dict):
        # strip None keys
        return json.dumps(value, ensure_ascii=False)
        #return {k: v for k, v in value.items() if k is not None}
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return {}
        try:
            parsed = json.loads(s)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    # anything else -> ignore
    return {}


def _ensure_json_text(field, value):
    """
    Ensure JSON TEXT for SQLite, based on field type.
    Arrays -> "[]", Objects -> "{}", always valid JSON strings.
    """
    if field in ARRAY_FIELDS:
        print("Ensuring array for field:", field, "value:", value)
        arr = _to_clean_list(value)
        return json.dumps(arr, ensure_ascii=False)

    if field in OBJECT_FIELDS:
        obj = _to_clean_obj(value)
        return json.dumps(obj, ensure_ascii=False)

    # Fallback for unexpected fields
    if value is None:
        return None
    if isinstance(value, (list, dict)):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, str):
        s = value.strip()
        if not s:
            return None
        try:
            json.loads(s)  # if valid JSON string, keep as-is
            return s
        except Exception:
            # try to treat it as CSV -> array
            arr = [x.strip() for x in s.split(",") if x.strip()]
            return json.dumps(arr, ensure_ascii=False)
    # scalar -> wrap as single item array
    return json.dumps([str(value)], ensure_ascii=False)


def _coerce_payload(data: dict) -> dict:
    """Build a column-safe payload for INSERT/UPDATE."""
    out = {}
    # Basic scalar columns
    basic = [
        "name_en", "name_hi", "name_mr", "category",
        "ayurvedic_name", "unani_name", "siddha_name",
        "description", "severity_level"
    ]
    for k in basic:
        if k in data:
            out[k] = data[k]

    # Booleans
    if "is_lifestyle_related" in data:
        out["is_lifestyle_related"] = int(bool(data["is_lifestyle_related"]))

    # JSON columns (arrays/objects)
    for f in ARRAY_FIELDS + OBJECT_FIELDS:
        if f in data:
            out[f] = _ensure_json_text(f, data[f])

    out["updated_at"] = datetime.utcnow().isoformat(sep=" ", timespec="seconds")
    return out


def _row_to_obj(row: sqlite3.Row) -> dict:
    """Convert DB row -> API object (parse JSON text back to native)."""
    d = dict(row)
    for f in ARRAY_FIELDS + OBJECT_FIELDS:
        if d.get(f):
            try:
                d[f] = json.loads(d[f])
            except Exception:
                pass
    return d


# ---------- Routes ----------
@admin_diseases_bp.get("/diseases")
def list_diseases():
    db = get_db()
    q = (request.args.get("q") or "").strip()
    page = max(1, int(request.args.get("page", 1)))
    size = max(1, min(100, int(request.args.get("size", 10))))
    offset = (page - 1) * size

    if q:
        items = db.execute("""
            SELECT * FROM diseases
            WHERE name_en LIKE ? OR ayurvedic_name LIKE ? OR category LIKE ?
               OR unani_name LIKE ? OR siddha_name LIKE ?
            ORDER BY lower(coalesce(name_en, ayurvedic_name)) ASC
            LIMIT ? OFFSET ?""",
            (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%", size, offset)
        ).fetchall()
        cnt = db.execute("""
            SELECT COUNT(*) AS c FROM diseases
            WHERE name_en LIKE ? OR ayurvedic_name LIKE ? OR category LIKE ?
               OR unani_name LIKE ? OR siddha_name LIKE ?""",
            (f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%", f"%{q}%")
        ).fetchone()["c"]
    else:
        items = db.execute(
            "SELECT * FROM diseases ORDER BY lower(coalesce(name_en, ayurvedic_name)) ASC LIMIT ? OFFSET ?",
            (size, offset)
        ).fetchall()
        cnt = db.execute("SELECT COUNT(*) AS c FROM diseases").fetchone()["c"]

    return jsonify({"items": [_row_to_obj(r) for r in items], "count": cnt, "page": page, "size": size})


@admin_diseases_bp.get("/diseases/<int:disease_id>")
def get_disease(disease_id: int):
    db = get_db()
    row = db.execute("SELECT * FROM diseases WHERE id=?", (disease_id,)).fetchone()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(_row_to_obj(row))


@admin_diseases_bp.post("/diseases")
@jwt_required()
def create_disease():
    data = request.get_json() or {}
    if not data.get("name_en"):
        return jsonify({"error": "name_en is required"}), 400
    if not data.get("category"):
        return jsonify({"error": "category is required"}), 400

    try:
        payload = _coerce_payload(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    db = get_db()
    exists = db.execute(
        "SELECT id FROM diseases WHERE lower(name_en)=lower(?)",
        (payload.get("name_en", ""),)
    ).fetchone()
    if exists:
        return jsonify({"error": "name_en already exists"}), 409

    cols = ", ".join(payload.keys())
    qs = ", ".join(["?"] * len(payload))
    db.execute(f"INSERT INTO diseases ({cols}) VALUES ({qs})", tuple(payload.values()))
    db.commit()
    new_id = db.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]

    admin_save_with_i18n(
        entity_type="disease",
        entity_id=new_id,
        en_fields={
            "name": data.get("name_en"),
            "description": data.get("description_en"),
            "symptoms": data.get("symptoms_en"),
            "causes": data.get("causes_en"),
            "precautions": data.get("precautions_en"),
        },
    )

    row = db.execute("SELECT * FROM diseases WHERE id=?", (new_id,)).fetchone()
    return jsonify(_row_to_obj(row)), 201


@admin_diseases_bp.put("/diseases/<int:disease_id>")
@jwt_required()
def update_disease(disease_id: int):
    data = request.get_json() or {}
    try:
        payload = _coerce_payload(data)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if not payload:
        return jsonify({"error": "nothing to update"}), 400

    try:
        if "name_en" in payload:
            db = get_db()
            ex = db.execute(
                "SELECT id FROM diseases WHERE lower(name_en)=lower(?) AND id<>?",
                (payload["name_en"], disease_id)
            ).fetchone()
            if ex:
                return jsonify({"error": "name_en already exists"}), 409

        sets = ", ".join([f"{k}=?" for k in payload.keys()])
        db = get_db()
        print("Update disease payload:", sets, payload)
        cur = db.execute(f"UPDATE diseases SET {sets} WHERE id=?", (*payload.values(), disease_id))
        if cur.rowcount == 0:
            return jsonify({"error": "Not found"}), 404

        db.commit()

        admin_save_with_i18n(
        entity_type="disease",
        entity_id=disease_id,
        en_fields={
            "name": data.get("name_en"),
            "description": data.get("description_en"),
            "symptoms": data.get("symptoms_en"),
            "causes": data.get("causes_en"),
            "precautions": data.get("precautions_en"),
        },
    )

        row = db.execute("SELECT * FROM diseases WHERE id=?", (disease_id,)).fetchone()
        return jsonify(_row_to_obj(row))
    except Exception as e:
        # Optional: log e
        return jsonify({"error": "update failed"}), 500


@admin_diseases_bp.delete("/diseases/<int:disease_id>")
@jwt_required()
def delete_disease(disease_id: int):
    db = get_db()
    cur = db.execute("DELETE FROM diseases WHERE id=?", (disease_id,))
    if cur.rowcount == 0:
        return jsonify({"error": "Not found"}), 404
    db.commit()
    return jsonify({"status": "deleted", "id": disease_id})
