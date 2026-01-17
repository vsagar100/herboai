#!/usr/bin/env python
"""Check for Turmeric preparations."""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== SEARCHING FOR TURMERIC PREPARATIONS ===\n")

cursor.execute("SELECT id, name_en FROM preparations WHERE LOWER(name_en) LIKE '%turmeric%'")
rows = cursor.fetchall()
if rows:
    print("Turmeric preparations found:")
    for row in rows:
        print(f"  ID {row['id']}: {row['name_en']}")
else:
    print("No Turmeric preparations found!")

# Check the first few preparations to see their plant_id
cursor.execute("SELECT id, name_en, plant_id FROM preparations LIMIT 5")
rows = cursor.fetchall()
print("\nSample preparations (with plant_id):")
for row in rows:
    print(f"  {row['name_en']} → plant_id {row['plant_id']}")

conn.close()
