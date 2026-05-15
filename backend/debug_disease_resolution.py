#!/usr/bin/env python
"""Debug disease resolution in chat pipeline."""

import sqlite3
from pathlib import Path

def resolve_disease_id_raw(conn, disease_text_en):
    """Raw version of resolve_disease_id without Flask context."""
    q = (disease_text_en or "").strip().lower()
    if not q:
        return None

    row = conn.execute(
        "SELECT id FROM diseases WHERE LOWER(name_en)=? LIMIT 1",
        (q,),
    ).fetchone()
    if row:
        return int(row[0])

    row = conn.execute(
        "SELECT disease_id FROM disease_synonyms WHERE LOWER(synonym)=? LIMIT 1",
        (q,),
    ).fetchone()
    if row:
        return int(row[0])

    like = f"%{q}%"
    row = conn.execute(
        "SELECT id FROM diseases WHERE LOWER(name_en) LIKE ? ORDER BY id LIMIT 1",
        (like,),
    ).fetchone()
    if row:
        return int(row[0])

    row = conn.execute(
        "SELECT disease_id FROM disease_synonyms WHERE LOWER(synonym) LIKE ? ORDER BY disease_id LIMIT 1",
        (like,),
    ).fetchone()
    if row:
        return int(row[0])

    return None

def test_disease_lookup():
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    
    # Test direct resolution
    test_terms = [
        "common cold",
        "cold",
        "cough",
        "cold_cough",
    ]
    
    print("=== DISEASE RESOLUTION TEST ===\n")
    
    for term in test_terms:
        disease_id = resolve_disease_id_raw(conn, term)
        print(f"Term: '{term}' -> Disease ID: {disease_id}")
        
        if disease_id:
            # Try fetching preparations
            sql = """
            SELECT DISTINCT pr.id, pr.name_en
            FROM preparations pr
            INNER JOIN plants p ON p.id = pr.plant_id
            INNER JOIN plant_disease_mapping pdm ON pdm.plant_id = p.id AND pdm.disease_id = ?
            LIMIT 5
            """
            rows = conn.execute(sql, (disease_id,)).fetchall()
            print(f"  Preparations: {len(rows)} found")
            for p in rows[:2]:
                print(f"    - {p['name_en']}")
        print()
    
    conn.close()

if __name__ == '__main__':
    test_disease_lookup()
