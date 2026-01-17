#!/usr/bin/env python
"""Check disease synonyms for cold/cough diseases."""

import sqlite3
from pathlib import Path

def check_synonyms():
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=== DISEASE SYNONYMS FOR RESPIRATORY DISEASES ===")
    
    # Get cough/cold/respiratory diseases
    cursor.execute("""
        SELECT d.id, d.name_en
        FROM diseases d
        WHERE LOWER(d.name_en) LIKE '%cough%' 
           OR LOWER(d.name_en) LIKE '%cold%'
           OR LOWER(d.name_en) LIKE '%respiratory%'
           OR LOWER(d.name_en) LIKE '%rhinitis%'
        ORDER BY d.id
    """)
    
    diseases = cursor.fetchall()
    print(f"Found {len(diseases)} respiratory diseases:\n")
    
    for disease in diseases:
        disease_id = disease['id']
        disease_name = disease['name_en']
        
        # Check synonyms
        cursor.execute("""
            SELECT synonym FROM disease_synonyms 
            WHERE disease_id = ?
            ORDER BY synonym
        """, (disease_id,))
        
        synonyms = cursor.fetchall()
        
        # Check plant mappings
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM plant_disease_mapping
            WHERE disease_id = ?
        """, (disease_id,))
        
        plant_count = cursor.fetchone()['cnt']
        
        print(f"Disease {disease_id}: {disease_name}")
        print(f"  Plant mappings: {plant_count}")
        if synonyms:
            print(f"  Synonyms:")
            for syn in synonyms:
                print(f"    - {syn['synonym']}")
        else:
            print(f"  Synonyms: (none)")
        print()

    conn.close()

if __name__ == '__main__':
    check_synonyms()
