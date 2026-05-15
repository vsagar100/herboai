#!/usr/bin/env python
"""Check for Turmeric in plants."""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== SEARCHING FOR TURMERIC ===\n")

cursor.execute("SELECT id, common_name_en FROM plants WHERE LOWER(common_name_en) LIKE '%turmeric%'")
rows = cursor.fetchall()
if rows:
    print("Turmeric plants found:")
    for row in rows:
        print(f"  ID {row['id']}: {row['common_name_en']}")
else:
    print("No Turmeric found!")

# Check for Haldi (Turmeric in Hindi)
cursor.execute("SELECT id, common_name_en, common_name_hi FROM plants WHERE LOWER(common_name_hi) LIKE '%हल्दी%' OR LOWER(common_name_mr) LIKE '%हळद%'")
rows = cursor.fetchall()
if rows:
    print("\nTurmeric (Hindi/Marathi name) found:")
    for row in rows:
        print(f"  ID {row['id']}: {row['common_name_en']} (HI: {row['common_name_hi']})")

conn.close()
