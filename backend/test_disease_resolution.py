#!/usr/bin/env python3
"""
Debug test to check if disease_id is being resolved correctly for Marathi queries.
"""
import sys
import os
import sqlite3

sys.path.insert(0, str(os.path.dirname(os.path.abspath(__file__))))

# Direct database access
db_path = os.path.join(os.path.dirname(__file__), "..", "db", "new_herboai.db")

db = sqlite3.connect(db_path)
db.row_factory = sqlite3.Row

def resolve_disease_id(conn: sqlite3.Connection, disease_text_en: str):
    q = (disease_text_en or "").strip().lower()
    if not q:
        return None

    row = conn.execute(
        "SELECT id FROM diseases WHERE LOWER(name_en)=? LIMIT 1",
        (q,),
    ).fetchone()
    if row:
        return int(row["id"])

    row = conn.execute(
        "SELECT disease_id FROM disease_synonyms WHERE LOWER(synonym)=? LIMIT 1",
        (q,),
    ).fetchone()
    if row:
        return int(row["disease_id"])

    like = f"%{q}%"
    row = conn.execute(
        "SELECT id FROM diseases WHERE LOWER(name_en) LIKE ? ORDER BY id LIMIT 1",
        (like,),
    ).fetchone()
    if row:
        return int(row["id"])

    row = conn.execute(
        "SELECT disease_id FROM disease_synonyms WHERE LOWER(synonym) LIKE ? ORDER BY disease_id LIMIT 1",
        (like,),
    ).fetchone()
    if row:
        return int(row["disease_id"])

    return None

# Test disease resolution
test_diseases = ["diabetes", "Diabetes", "DIABETES"]

print("=" * 80)
print("Testing Disease Resolution")
print("=" * 80)

for disease in test_diseases:
    disease_id = resolve_disease_id(db, disease)
    print(f"\nDisease: '{disease}'")
    print(f"  Resolved ID: {disease_id}")
    
    if disease_id:
        # Fetch preparations for this disease
        preps_sql = """
        SELECT DISTINCT pr.id, pr.name_en
        FROM preparations pr
        LEFT JOIN preparation_indications pi ON pi.preparation_id = pr.id
        LEFT JOIN plant_disease_mapping pdm ON pdm.plant_id = pr.plant_id
        WHERE pi.disease_id = ? OR pdm.disease_id = ?
        LIMIT 10
        """
        preps = db.execute(preps_sql, (disease_id, disease_id)).fetchall()
        print(f"  Preparations: {len(preps)}")
        for prep in preps[:3]:
            print(f"    - {prep['name_en']}")

# Also check what diseases exist in the database
print("\n" + "=" * 80)
print("Diseases in Database")
print("=" * 80)

rows = db.execute("""
    SELECT id, name_en FROM diseases ORDER BY id LIMIT 20
""").fetchall()

for row in rows:
    disease_id, name = row
    preps_sql = """
    SELECT DISTINCT pr.id, pr.name_en
    FROM preparations pr
    LEFT JOIN preparation_indications pi ON pi.preparation_id = pr.id
    LEFT JOIN plant_disease_mapping pdm ON pdm.plant_id = pr.plant_id
    WHERE pi.disease_id = ? OR pdm.disease_id = ?
    LIMIT 1
    """
    preps = db.execute(preps_sql, (disease_id, disease_id)).fetchall()
    print(f"{disease_id:3d}. {name:30s} ({len(preps)} preps)")

print("=" * 80)
