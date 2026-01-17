#!/usr/bin/env python
"""Debug plant_disease_mapping."""

import sqlite3
from pathlib import Path

def check_mapping():
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=== PLANT_DISEASE_MAPPING SAMPLE ===")
    cursor.execute("""
        SELECT pdm.plant_id, pdm.disease_id, pdm.efficacy_level,
               p.common_name_en, d.name_en
        FROM plant_disease_mapping pdm
        INNER JOIN plants p ON p.id = pdm.plant_id
        INNER JOIN diseases d ON d.id = pdm.disease_id
        LIMIT 5
    """)
    rows = cursor.fetchall()
    for row in rows:
        print(f"Plant {row['plant_id']}: {row['common_name_en']} → Disease {row['disease_id']}: {row['name_en']} (efficacy: {row['efficacy_level']})")

    # Check for Common Cold specifically
    print("\n=== PLANTS FOR COMMON COLD (Disease ID 173) ===")
    cursor.execute("""
        SELECT pdm.plant_id, pdm.efficacy_level, p.common_name_en
        FROM plant_disease_mapping pdm
        INNER JOIN plants p ON p.id = pdm.plant_id
        WHERE pdm.disease_id = 173
        ORDER BY pdm.efficacy_level DESC
        LIMIT 10
    """)
    rows = cursor.fetchall()
    if rows:
        print(f"Found {len(rows)} plants for Common Cold:")
        for row in rows:
            print(f"  Plant {row['plant_id']}: {row['common_name_en']} (efficacy: {row['efficacy_level']})")
    else:
        print("No plants mapped to Common Cold!")

    # Check for preparations with those plants
    print("\n=== PREPARATIONS FOR COMMON COLD PLANTS ===")
    cursor.execute("""
        SELECT DISTINCT pr.id, pr.name_en, pr.plant_id, p.common_name_en
        FROM preparations pr
        INNER JOIN plants p ON p.id = pr.plant_id
        INNER JOIN plant_disease_mapping pdm ON pdm.plant_id = p.id AND pdm.disease_id = 173
        LIMIT 10
    """)
    rows = cursor.fetchall()
    if rows:
        print(f"Found {len(rows)} preparations from plants used for Common Cold:")
        for row in rows:
            print(f"  Prep {row['id']}: {row['name_en']} (from plant {row['plant_id']}: {row['common_name_en']})")
    else:
        print("No preparations found!")

    conn.close()

if __name__ == '__main__':
    check_mapping()
