#!/usr/bin/env python
"""Debug disease and preparation lookup."""

import sqlite3
from pathlib import Path

def debug_disease_lookup():
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    test_queries = [
        "running nose",
        "coughing",
        "cold",
        "cough",
        "rhinitis",
        "common cold",
    ]

    print("=== DISEASE RESOLUTION TEST ===\n")
    for q in test_queries:
        q_lower = q.lower()
        
        # Exact match
        row = cursor.execute(
            "SELECT id, name_en FROM diseases WHERE LOWER(name_en) = ?",
            (q_lower,)
        ).fetchone()
        
        if row:
            print(f"✓ '{q}' → EXACT MATCH → Disease ID {row['id']}: {row['name_en']}")
            continue
        
        # LIKE match
        row = cursor.execute(
            "SELECT id, name_en FROM diseases WHERE LOWER(name_en) LIKE ?",
            (f"%{q_lower}%",)
        ).fetchone()
        
        if row:
            print(f"✓ '{q}' → LIKE MATCH → Disease ID {row['id']}: {row['name_en']}")
        else:
            print(f"✗ '{q}' → NO MATCH found")

    # Check plant_disease_mapping
    print("\n=== PLANT_DISEASE_MAPPING CHECK ===\n")
    cursor.execute("SELECT COUNT(*) as cnt FROM plant_disease_mapping")
    cnt = cursor.fetchone()['cnt']
    print(f"Total mappings in plant_disease_mapping: {cnt}")
    
    if cnt == 0:
        print("⚠️ plant_disease_mapping is EMPTY! This is the root cause.")
        print("Preparations won't be found because fetch_preparations_for_disease")
        print("relies on plant_disease_mapping JOIN.")
    
    # Check preparation_indications
    print("\n=== PREPARATION_INDICATIONS CHECK ===\n")
    cursor.execute("SELECT COUNT(*) as cnt FROM preparation_indications")
    cnt = cursor.fetchone()['cnt']
    print(f"Total records in preparation_indications: {cnt}")
    
    if cnt == 0:
        print("⚠️ preparation_indications is EMPTY!")

    # Check disease_synonyms
    print("\n=== DISEASE_SYNONYMS CHECK ===\n")
    cursor.execute("SELECT COUNT(*) as cnt FROM disease_synonyms")
    cnt = cursor.fetchone()['cnt']
    print(f"Total records in disease_synonyms: {cnt}")

    # Try actual preparation lookup for Common Cold
    print("\n=== PREPARATION LOOKUP FOR 'COMMON COLD' ===\n")
    cursor.execute("SELECT id FROM diseases WHERE LOWER(name_en) LIKE '%cold%'")
    cold = cursor.fetchone()
    
    if cold:
        disease_id = cold['id']
        print(f"Found disease ID {disease_id} for 'Common Cold'")
        
        # Try the full fetch_preparations_for_disease query
        sql = """
        SELECT DISTINCT
          pr.id, pr.name_en,
          COALESCE(pi.strength, pdm.efficacy_level, 3) AS efficacy_level
        FROM preparations pr
        INNER JOIN preparation_ingredients pgi ON pgi.preparation_id = pr.id
        INNER JOIN plants p ON p.id = pgi.plant_id
        INNER JOIN plant_disease_mapping pdm ON pdm.plant_id = p.id AND pdm.disease_id = ?
        LEFT JOIN preparation_indications pi 
          ON pi.preparation_id = pr.id AND pi.disease_id = ?
        ORDER BY COALESCE(pi.strength, pdm.efficacy_level, 0) DESC
        LIMIT 10
        """
        
        rows = cursor.execute(sql, (disease_id, disease_id)).fetchall()
        
        if rows:
            print(f"✓ Found {len(rows)} preparations for disease {disease_id}:")
            for row in rows:
                print(f"  - Prep ID {row['id']}: {row['name_en']} (efficacy: {row['efficacy_level']})")
        else:
            print(f"✗ No preparations found for disease {disease_id}")
            print("\nThis is because plant_disease_mapping or preparation_ingredients might be empty.")

    conn.close()

if __name__ == '__main__':
    debug_disease_lookup()
