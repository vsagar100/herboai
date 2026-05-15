# scripts/build_embeddings.py
import sqlite3, json
import math
from typing import List
import sqlite_vec
#from db import get_db
from sqlite_vec import load as load_sqlite_vec
from sqlite_vec import serialize_float32
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")   # CPU-friendly, 384-dim

def _l2_normalize(v: List[float]) -> List[float]:
    s = math.sqrt(sum(x*x for x in v)) or 1.0
    return [x / s for x in v]

def get_db():
    db_path = "../db/new_herboai.db" #current_app.config["DB_PATH"]
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.enable_load_extension(True)
    try:
        load_sqlite_vec(conn)  # ← registers vec0
        print("✅ sqlite-vec (vec0) loaded")
    except Exception as e:
        print("⚠️ sqlite-vec not loaded:", e)
    conn.enable_load_extension(False)
    return conn

def _upsert(sql, rows, text_fn, id_fn, name_fn):
    try:
        db = get_db()
        for r in rows:
                txt = text_fn(r).strip()
                if not txt: 
                        continue
                vec = model.encode(txt).astype("float32").tolist()
                vec = _l2_normalize(vec) # normalize for better distance comparisons
                db.execute(sql, (id_fn(r), name_fn(r), serialize_float32(vec)))
        db.commit()
    except Exception as e:
        print("Error during upsert:", e)

def main():
    db = get_db(); db.row_factory = sqlite3.Row

    # Diseases
    #rows = db.execute("SELECT id, name_en, description, symptoms FROM diseases").fetchall()
    #_upsert("""INSERT OR REPLACE INTO disease_vec(disease_id,name_en,embedding) VALUES (?,?,?)""",
    #        rows,
    #        lambda r: " ".join(filter(None, [r["name_en"], r["description"] or "", 
    #                " ".join(json.loads(r["symptoms"])) if r["symptoms"] else ""])),
     #       lambda r: r["id"], lambda r: r["name_en"])

    # Plants
    #rows = db.execute("SELECT id, common_name_en, botanical_name, description, therapeutic_actions FROM plants").fetchall()
    #_upsert("""INSERT OR REPLACE INTO plant_vec(plant_id,name_en,embedding) VALUES (?,?,?)""",
    #        rows,
     #       lambda r: " ".join(filter(None, [r["common_name_en"] or r["botanical_name"] or "",
     #               r["botanical_name"] or "", r["description"] or "", 
     #               " ".join(json.loads(r["therapeutic_actions"])) if r["therapeutic_actions"] else ""])),
      #      lambda r: r["id"], lambda r: r["common_name_en"] or r["botanical_name"])

    # Preparations (optional now; handy later)
    rows = db.execute("SELECT id, name_en, classical_name, form_type, preparation_steps FROM preparations").fetchall()
    _upsert("""INSERT OR REPLACE INTO prep_vec(preparation_id,name_en,embedding) VALUES (?,?,?)""",
            rows,
            lambda r: " ".join(filter(None, [r["name_en"] or "", r["classical_name"] or "", r["form_type"] or "",
                    " ".join(json.loads(r["preparation_steps"])) if r["preparation_steps"] else ""])),
            lambda r: r["id"], lambda r: r["name_en"])

if __name__ == "__main__":
    main()
