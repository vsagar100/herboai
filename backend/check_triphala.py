#!/usr/bin/env python
"""Check Triphala in database."""

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
conn = sqlite3.connect(str(db_path))
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print("=== SEARCHING FOR TRIPHALA ===\n")

cursor.execute("SELECT id, name_en FROM preparations WHERE LOWER(name_en) LIKE '%triphala%'")
rows = cursor.fetchall()
print("Triphala preparations:")
for row in rows:
    print(f"  ID {row['id']}: {row['name_en']}")

cursor.execute("SELECT id, common_name_en FROM plants WHERE LOWER(common_name_en) LIKE '%triphala%'")
rows = cursor.fetchall()
if rows:
    print("\nTriphala plants:")
    for row in rows:
        print(f"  ID {row['id']}: {row['common_name_en']}")
else:
    print("\nTriphala is not a plant - it's a preparation (blend of 3 fruits)")

conn.close()
