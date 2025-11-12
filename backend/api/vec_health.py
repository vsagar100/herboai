# api/vec_health.py
from flask import Blueprint, jsonify
from db import get_db
from sqlite_vec import serialize_float32
from sentence_transformers import SentenceTransformer

bp = Blueprint("vec_health", __name__)

@bp.get("/vec/health")
def vec_health():
    conn = get_db()
    conn.enable_load_extension(True)

    # 1) Load sqlite-vec (registers vec0 on this connection)
    try:
        import sqlite_vec
        sqlite_vec.load(conn)
    except Exception as e:
        return jsonify({"ok": False, "stage": "load", "error": str(e)}), 500

    try:
        # 2) Create a tiny demo vec0 table
        conn.execute("DROP TABLE IF EXISTS vec_health_demo;")
        conn.execute("""
            CREATE VIRTUAL TABLE vec_health_demo USING vec0(
              id INTEGER PRIMARY KEY,
              name TEXT,
              embedding FLOAT[3]
            );
        """)

        # 3) Insert two 3-D vectors
        from sqlite_vec import serialize_float32
        v1 = serialize_float32([0.1, 0.2, 0.3])
        v2 = serialize_float32([0.1, 0.21, 0.31])
        conn.execute("INSERT INTO vec_health_demo(name, embedding) VALUES (?,?)", ("a", v1))
        conn.execute("INSERT INTO vec_health_demo(name, embedding) VALUES (?,?)", ("b", v2))
        conn.commit()

        # 4) KNN query (nearest 2 to a probe)
        probe = serialize_float32([0.1, 0.205, 0.305])
        rows = conn.execute("""
            SELECT id, name, distance
            FROM vec_health_demo
            WHERE embedding MATCH ?
              AND k = 2
        """, (probe,)).fetchall()

        return jsonify({
            "ok": True,
            "results": [dict(r) for r in rows]
        }), 200

    except Exception as e:
        return jsonify({"ok": False, "stage": "knn", "error": str(e)}), 500

@bp.get("/vec/initialize")
def vec_initialize():
    try:
        db = get_db()
        db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS disease_vec USING vec0(
        disease_id INTEGER PRIMARY KEY,
        name_en TEXT,
        embedding FLOAT[384]
        );
        """)
        db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS plant_vec USING vec0(
        plant_id INTEGER PRIMARY KEY,
        name_en TEXT,
        embedding FLOAT[384]
        );
        """)
        db.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS prep_vec USING vec0(
        preparation_id INTEGER PRIMARY KEY,
        name_en TEXT,
        embedding FLOAT[384]
        );
        """)
        db.commit()
        print("vec0 tables ready")
        return jsonify({"ok": True, "message": "vec0 tables initialized"}), 200
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


model = SentenceTransformer("all-MiniLM-L6-v2")

@bp.post("/vec/reindex")
def vec_reindex():
    try:
        db = get_db(); db.row_factory = None
        rows = db.execute("""
            SELECT id, name_en, description
            FROM diseases
            WHERE updated_at > datetime('now', '-1 day')
        """).fetchall()
        for rid, name, desc in rows:
            vec = model.encode(f"{name} {desc or ''}").astype("float32").tolist()
            db.execute("""
                INSERT OR REPLACE INTO disease_vec(disease_id, name_en, embedding)
                VALUES (?, ?, ?)
            """, (rid, name, serialize_float32(vec)))
        db.commit()
        return jsonify({"ok": True, "updated": len(rows)})
    except Exception as e:
        print("Error in /vec/reindex:", e)
        return jsonify({"ok": False, "error": str(e)}), 500
