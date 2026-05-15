#!/usr/bin/env python
"""Check preparation_ingredients table."""

import sqlite3
from pathlib import Path

def check_prep_ingredients():
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Check table existence
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='preparation_ingredients'")
    exists = cursor.fetchone()
    
    print("=== PREPARATION_INGREDIENTS TABLE ===")
    if not exists:
        print("✗ Table 'preparation_ingredients' DOES NOT EXIST!")
        print("\nAvailable tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        for t in tables:
            cursor.execute(f"SELECT COUNT(*) as cnt FROM {t['name']}")
            cnt = cursor.fetchone()['cnt']
            print(f"  - {t['name']}: {cnt} records")
    else:
        print("✓ Table 'preparation_ingredients' EXISTS")
        cursor.execute("SELECT COUNT(*) as cnt FROM preparation_ingredients")
        cnt = cursor.fetchone()['cnt']
        print(f"  Records: {cnt}")
        
        if cnt > 0:
            cursor.execute("SELECT * FROM preparation_ingredients LIMIT 5")
            rows = cursor.fetchall()
            print("\n  Sample records:")
            for r in rows:
                print(f"    {dict(r)}")
        else:
            print("  ⚠️ Table is EMPTY!")

    conn.close()

if __name__ == '__main__':
    check_prep_ingredients()
