"""Test data completeness for acne and neem"""
import sys
from flask import Flask
from db import init_app, get_db

app = Flask(__name__)
app.config["DB_PATH"] = "../db/new_herboai.db"  # Correct path
init_app(app)

with app.app_context():
    db = get_db()
    
    print("\n=== 1. CHECK ACNE IN DISEASES TABLE ===")
    rows = db.execute("""
        SELECT id, name_en, category FROM diseases 
        WHERE LOWER(name_en) LIKE '%acne%' 
           OR LOWER(name_en) LIKE '%pimple%'
           OR LOWER(name_en) LIKE '%skin%'
        LIMIT 5
    """).fetchall()
    print(f"Found {len(rows)} diseases")
    for r in rows:
        print(f"  ID={r['id']}: {r['name_en']} (category: {r['category']})")
    
    print("\n=== 2. CHECK NEEM IN PLANTS TABLE ===")
    rows = db.execute("""
        SELECT id, common_name_en, botanical_name FROM plants 
        WHERE LOWER(common_name_en) LIKE '%neem%'
           OR LOWER(botanical_name) LIKE '%azadirachta%'
        LIMIT 5
    """).fetchall()
    print(f"Found {len(rows)} plants")
    for r in rows:
        print(f"  ID={r['id']}: {r['common_name_en']} ({r['botanical_name']})")
    
    neem_id = rows[0]['id'] if rows else None
    
    print("\n=== 3. CHECK PLANT_DISEASE_MAPPING ===")
    if neem_id:
        rows = db.execute("""
            SELECT pdm.*, d.name_en as disease_name
            FROM plant_disease_mapping pdm
            JOIN diseases d ON d.id = pdm.disease_id
            WHERE pdm.plant_id = ?
            ORDER BY pdm.efficacy_level DESC
            LIMIT 10
        """, (neem_id,)).fetchall()
        print(f"Neem is mapped to {len(rows)} diseases:")
        for r in rows:
            print(f"  - {r['disease_name']} (efficacy: {r['efficacy_level']})")
    
    print("\n=== 4. CHECK IF NEEM-ACNE MAPPING EXISTS ===")
    rows = db.execute("""
        SELECT pdm.*, p.common_name_en, d.name_en as disease_name
        FROM plant_disease_mapping pdm
        JOIN plants p ON p.id = pdm.plant_id
        JOIN diseases d ON d.id = pdm.disease_id
        WHERE LOWER(p.common_name_en) LIKE '%neem%'
          AND (LOWER(d.name_en) LIKE '%acne%' OR LOWER(d.name_en) LIKE '%skin%')
    """).fetchall()
    print(f"Found {len(rows)} neem-acne/skin mappings")
    for r in rows:
        print(f"  {r['common_name_en']} → {r['disease_name']}")
    
    print("\n=== 5. CHECK DISEASE SYNONYMS FOR 'acne' ===")
    rows = db.execute("""
        SELECT ds.*, d.name_en FROM disease_synonyms ds
        JOIN diseases d ON d.id = ds.disease_id
        WHERE LOWER(ds.synonym) LIKE '%acne%' OR LOWER(ds.synonym) LIKE '%pimple%'
        LIMIT 5
    """).fetchall()
    print(f"Found {len(rows)} synonyms")
    for r in rows:
        print(f"  '{r['synonym']}' → {r['name_en']} (lang: {r.get('lang', 'N/A')})")
    
    print("\n=== 6. CHECK PREPARATIONS FOR NEEM ===")
    if neem_id:
        rows = db.execute("""
            SELECT p.id, p.classical_name, p.form_type
            FROM preparations p
            JOIN preparation_ingredients pi ON pi.preparation_id = p.id
            WHERE pi.plant_id = ?
            LIMIT 5
        """, (neem_id,)).fetchall()
        print(f"Found {len(rows)} preparations using neem")
        for r in rows:
            print(f"  {r['classical_name']} ({r['form_type']})")
