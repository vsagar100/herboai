from typing import List, Dict, Optional
from db import get_db

def top_plants_for_disease(disease_id: int, k: int = 5) -> List[Dict]:
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT p.*, pdm.efficacy_level, pdm.evidence_type, pdm.mechanism
        FROM plant_disease_mapping pdm
        JOIN plants p ON p.id=pdm.plant_id
        WHERE pdm.disease_id = ?
        ORDER BY pdm.efficacy_level DESC, p.common_name_en
        LIMIT ?
    """, (disease_id, k))
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    return rows

def top_preparations_for_disease(disease_id: int, k: int = 3) -> List[Dict]:
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT pr.*, pi.strength, pi.evidence_type, pi.notes
        FROM preparation_indications pi
        JOIN preparations pr ON pr.id = pi.preparation_id
        WHERE pi.disease_id = ?
        ORDER BY pi.strength DESC, pr.name_en
        LIMIT ?
    """, (disease_id, k))
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    return rows

def ingredients_for_preparation(preparation_id: int) -> List[Dict]:
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT p.common_name_en, p.botanical_name, pi.part, pi.quantity_value, pi.quantity_unit
        FROM preparation_ingredients pi
        JOIN plants p ON p.id = pi.plant_id
        WHERE pi.preparation_id = ?
        ORDER BY pi.id
    """, (preparation_id,))
    rows = [dict(r) for r in cur.fetchall()]
    cur.close()
    return rows

def disease_by_name_en(name_en: str) -> Optional[Dict]:
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT * FROM diseases WHERE name_en = ?", (name_en,))
    row = cur.fetchone()
    cur.close()
    return dict(row) if row else None
