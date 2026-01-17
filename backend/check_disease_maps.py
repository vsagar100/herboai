#!/usr/bin/env python
"""Check which diseases have plant mappings."""

import sqlite3
from pathlib import Path

def check_disease_mappings():
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=== DISEASES WITH PLANT MAPPINGS ===")
    cursor.execute("""
        SELECT d.id, d.name_en, COUNT(pdm.plant_id) as plant_count
        FROM diseases d
        LEFT JOIN plant_disease_mapping pdm ON pdm.disease_id = d.id
        GROUP BY d.id
        ORDER BY plant_count DESC
        LIMIT 20
    """)
    rows = cursor.fetchall()
    
    mapped_count = sum(1 for r in rows if r['plant_count'] > 0)
    total_count = len(rows)
    
    print(f"Diseases with mappings: {mapped_count}/{total_count}\n")
    
    for row in rows:
        status = "✓" if row['plant_count'] > 0 else "✗"
        print(f"{status} Disease {row['id']:3d}: {row['name_en']:40s} → {row['plant_count']:2d} plants")

    # Find common cold by different patterns
    print("\n=== SEARCHING FOR 'COLD' DISEASES ===")
    cursor.execute("SELECT id, name_en FROM diseases WHERE LOWER(name_en) LIKE '%cold%'")
    cold_diseases = cursor.fetchall()
    for disease in cold_diseases:
        cursor.execute("""
            SELECT COUNT(*) as cnt FROM plant_disease_mapping 
            WHERE disease_id = ?
        """, (disease['id'],))
        cnt = cursor.fetchone()['cnt']
        print(f"Disease {disease['id']}: {disease['name_en']} → {cnt} plants")

    conn.close()

if __name__ == '__main__':
    check_disease_mappings()
