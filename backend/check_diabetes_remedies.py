"""
Check remedies/plants for diabetes
"""
import sys
sys.path.insert(0, '.')

from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from db import get_db

def main():
    with app.app_context():
        db = get_db()
        
        print("\n=== DIABETES REMEDIES CHECK ===\n")
        
        # Get diabetes disease ID
        diabetes = db.execute("""
            SELECT id, name_en
            FROM diseases
            WHERE LOWER(name_en) LIKE '%diabetes%'
        """).fetchone()
        
        if not diabetes:
            print("ERROR: Diabetes not found in database!")
            return
        
        disease_id = diabetes['id']
        print(f"Diabetes ID: {disease_id} ({diabetes['name_en']})")
        
        # Check plant-disease mappings
        print("\n--- Plant-Disease Mappings ---")
        mappings = db.execute("""
            SELECT pdm.*, p.common_name_en, p.common_name_hi, p.common_name_mr
            FROM plant_disease_mapping pdm
            JOIN plants p ON p.id = pdm.plant_id
            WHERE pdm.disease_id = ?
            ORDER BY pdm.efficacy_level DESC
        """, (disease_id,)).fetchall()
        
        if mappings:
            print(f"\nFound {len(mappings)} plant mappings for diabetes:")
            for m in mappings:
                print(f"\n  Plant ID: {m['plant_id']}")
                print(f"    EN: {m['common_name_en']}")
                print(f"    HI: {m['common_name_hi']}")
                print(f"    MR: {m['common_name_mr']}")
                print(f"    Efficacy: {m['efficacy_level']}")
                print(f"    Evidence: {m['evidence_type']}")
                
                # Check entity_i18n for this plant
                plant_i18n = db.execute("""
                    SELECT lang, field, SUBSTR(text, 1, 50) as text_preview
                    FROM entity_i18n
                    WHERE entity_type='plant' AND entity_id=? AND field='name'
                """, (m['plant_id'],)).fetchall()
                
                if plant_i18n:
                    print(f"    entity_i18n names:")
                    for i18n in plant_i18n:
                        print(f"      {i18n['lang']}: {i18n['text_preview']}")
                else:
                    print(f"    ❌ NO entity_i18n name data")
        else:
            print("\n❌ NO PLANT MAPPINGS FOUND FOR DIABETES!")
            print("\nThis means the system has no remedies to recommend.")
        
        # Check if there are ANY plant-disease mappings
        total_mappings = db.execute("""
            SELECT COUNT(*) as count FROM plant_disease_mapping
        """).fetchone()
        
        print(f"\n\nTotal plant-disease mappings in database: {total_mappings['count']}")
        
        # Show some example mappings
        print("\n--- Sample Plant-Disease Mappings (First 10) ---")
        sample_mappings = db.execute("""
            SELECT pdm.disease_id, d.name_en as disease_name,
                   pdm.plant_id, p.common_name_en as plant_name,
                   pdm.efficacy_level
            FROM plant_disease_mapping pdm
            JOIN diseases d ON d.id = pdm.disease_id
            JOIN plants p ON p.id = pdm.plant_id
            LIMIT 10
        """).fetchall()
        
        for m in sample_mappings:
            print(f"  {m['disease_name']} ← {m['plant_name']} (efficacy: {m['efficacy_level']})")

if __name__ == "__main__":
    main()
