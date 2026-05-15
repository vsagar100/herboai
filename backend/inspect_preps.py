#!/usr/bin/env python
"""Inspect preparation table structure."""

import sqlite3
from pathlib import Path
import json

def inspect_preparations():
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=== PREPARATIONS TABLE SCHEMA ===")
    cursor.execute("PRAGMA table_info(preparations)")
    cols = cursor.fetchall()
    for col in cols:
        print(f"  {col['name']}: {col['type']}")

    print("\n=== SAMPLE PREPARATION RECORDS ===")
    cursor.execute("SELECT * FROM preparations LIMIT 3")
    rows = cursor.fetchall()
    for i, row in enumerate(rows, 1):
        print(f"\nPreparation {i}:")
        data = dict(row)
        for k, v in data.items():
            if v and len(str(v)) > 100:
                print(f"  {k}: {str(v)[:100]}...")
            else:
                print(f"  {k}: {v}")

    print("\n=== INGREDIENTS DATA LOCATION ===")
    # Check if ingredients are stored as JSON in a field
    cursor.execute("SELECT id, name_en FROM preparations WHERE id IN (1, 2, 3)")
    rows = cursor.fetchall()
    for row in rows:
        prep_id = row['id']
        # Try to find field containing ingredients
        cursor.execute(f"SELECT * FROM preparations WHERE id = {prep_id}")
        prep = dict(cursor.fetchone())
        print(f"\nPrep {prep_id} ({prep.get('name_en')}):")
        
        # Look for ingredient fields
        for field in ['ingredient', 'ingredients', 'plants', 'plant_ingredients', 'composition']:
            if field in prep:
                val = prep[field]
                if val:
                    print(f"  Found field '{field}': {val[:100]}")

    # Check if there's data in the SQL dump
    print("\n=== CHECKING SQL DUMP FOR SAMPLE DATA ===")
    print("The 'preparation_ingredients' table needs to be populated.")
    print("This table should link preparations to their plant ingredients.")

    conn.close()

if __name__ == '__main__':
    inspect_preparations()
