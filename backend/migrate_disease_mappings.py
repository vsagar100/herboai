#!/usr/bin/env python
"""
Populate missing disease_synonyms and fallback mappings for diseases without plant mappings.

Strategy:
1. Add disease_synonyms for diseases without them (Common Cold, Allergic Rhinitis, etc.)
2. For diseases with no plant mappings, copy mappings from related diseases
"""

import sqlite3
from pathlib import Path

def migrate_disease_mappings():
    db_path = Path(__file__).parent.parent / 'db' / 'new_herboai.db'
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all diseases with no plant mappings
    cursor.execute("""
        SELECT d.id, d.name_en
        FROM diseases d
        LEFT JOIN plant_disease_mapping pdm ON pdm.disease_id = d.id
        WHERE pdm.plant_id IS NULL
        ORDER BY d.id
    """)
    
    unmapped_diseases = cursor.fetchall()
    print(f"Found {len(unmapped_diseases)} diseases with no plant mappings:\n")

    # Disease mapping strategy: group related diseases
    disease_groups = {
        "respiratory": {
            "main": 12,  # Chronic Cough and Bronchitis (has 17 plants)
            "related": [173, 148, 164, 168],  # Common Cold, Dry Cough, Allergic Rhinitis, Respiratory Congestion
        },
        "allergic": {
            "main": 164,  # Allergic Rhinitis
            "related": [173, 168],
        },
    }

    changes_made = 0

    # For each unmapped disease, find the best source disease and copy mappings
    for disease_id, disease_name in unmapped_diseases:
        print(f"Processing Disease {disease_id}: {disease_name}")
        
        # Determine source disease for mapping (use Chronic Cough for respiratory issues)
        source_disease_id = None
        
        if "cold" in disease_name.lower() or "rhinitis" in disease_name.lower():
            source_disease_id = 12  # Chronic Cough has the most mappings
        elif "cough" in disease_name.lower():
            source_disease_id = 12
        elif "respiratory" in disease_name.lower() or "congestion" in disease_name.lower():
            source_disease_id = 12
        
        if source_disease_id:
            # Copy plant mappings from source to target disease
            cursor.execute("""
                INSERT OR IGNORE INTO plant_disease_mapping 
                    (plant_id, disease_id, efficacy_level, evidence_type)
                SELECT plant_id, ?, efficacy_level, evidence_type
                FROM plant_disease_mapping
                WHERE disease_id = ?
            """, (disease_id, source_disease_id))
            
            affected = cursor.rowcount
            if affected > 0:
                print(f"  ✓ Copied {affected} plant mappings from Disease {source_disease_id}")
                changes_made += affected
            
            # Also add disease synonym pointing to source if not exists
            cursor.execute("""
                SELECT COUNT(*) as cnt FROM disease_synonyms
                WHERE disease_id = ? AND LOWER(synonym) = LOWER(?)
            """, (disease_id, disease_name.lower()))
            
            if cursor.fetchone()['cnt'] == 0:
                cursor.execute("""
                    INSERT INTO disease_synonyms (disease_id, synonym, language)
                    VALUES (?, ?, 'en')
                """, (disease_id, disease_name.lower()))
                print(f"  ✓ Added synonym '{disease_name.lower()}' to Disease {disease_id}")
                changes_made += 1
        else:
            print(f"  ! Could not find mapping strategy for {disease_name}")
        
        print()

    # Commit changes
    conn.commit()
    print(f"\n✓ Migration complete! {changes_made} changes made.")
    
    # Verification: check unmapped diseases again
    cursor.execute("""
        SELECT d.id, d.name_en, COUNT(pdm.plant_id) as plant_count
        FROM diseases d
        LEFT JOIN plant_disease_mapping pdm ON pdm.disease_id = d.id
        WHERE LOWER(d.name_en) LIKE '%cold%' OR LOWER(d.name_en) LIKE '%rhinitis%' OR LOWER(d.name_en) LIKE '%respiratory%'
        GROUP BY d.id
        ORDER BY d.id
    """)
    
    print("\n=== VERIFICATION ===\n")
    for row in cursor.fetchall():
        print(f"Disease {row['id']}: {row['name_en']} → {row['plant_count']} plants")

    conn.close()

if __name__ == '__main__':
    migrate_disease_mappings()
