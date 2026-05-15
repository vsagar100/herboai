"""
Quick check of entity_i18n data and disease resolution
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
        
        print("\n=== ENTITY_I18N DATA CHECK ===\n")
        
        # Count by type and language
        rows = db.execute("""
            SELECT entity_type, lang, COUNT(*) as count
            FROM entity_i18n
            GROUP BY entity_type, lang
            ORDER BY entity_type, lang
        """).fetchall()
        
        print("Entity i18n counts:")
        for row in rows:
            print(f"  {row['entity_type']:12} | {row['lang']:4} | {row['count']:6} records")
        
        # Check diabetes specifically
        print("\n=== DIABETES DATA CHECK ===\n")
        
        diabetes_rows = db.execute("""
            SELECT d.id, d.name_en, d.name_hi, d.name_mr
            FROM diseases d
            WHERE LOWER(d.name_en) LIKE '%diabetes%'
               OR LOWER(d.name_hi) LIKE '%मधुमेह%'
               OR LOWER(d.name_mr) LIKE '%मधुमेह%'
        """).fetchall()
        
        print(f"Found {len(diabetes_rows)} diabetes-related diseases:")
        for row in diabetes_rows:
            print(f"\n  ID: {row['id']}")
            print(f"  EN: {row['name_en']}")
            print(f"  HI: {row['name_hi']}")
            print(f"  MR: {row['name_mr']}")
            
            # Check entity_i18n data for this disease
            i18n_rows = db.execute("""
                SELECT lang, field, text
                FROM entity_i18n
                WHERE entity_type='disease' AND entity_id=?
                ORDER BY lang, field
            """, (row['id'],)).fetchall()
            
            if i18n_rows:
                print(f"  entity_i18n data:")
                for i18n in i18n_rows:
                    text_preview = i18n['text'][:40] + "..." if len(i18n['text']) > 40 else i18n['text']
                    print(f"    {i18n['lang']}.{i18n['field']}: {text_preview}")
            else:
                print(f"  ❌ NO entity_i18n data")
        
        # Check disease synonyms
        print("\n=== DISEASE SYNONYMS CHECK ===\n")
        
        synonym_rows = db.execute("""
            SELECT ds.disease_id, ds.synonym, ds.language, d.name_en
            FROM disease_synonyms ds
            JOIN diseases d ON d.id = ds.disease_id
            WHERE LOWER(ds.synonym) IN ('diabetes', 'मधुमेह', 'sugar')
        """).fetchall()
        
        print(f"Found {len(synonym_rows)} diabetes synonyms:")
        for row in synonym_rows:
            print(f"  '{row['synonym']}' ({row['language']}) → Disease ID {row['disease_id']} ({row['name_en']})")
        
        # Test entity extraction
        print("\n=== TESTING ENTITY EXTRACTION ===\n")
        
        from api.nlu_optimized import search_diseases_fuzzy
        
        test_queries = [
            "diabetes",
            "मधुमेह",
            "I have diabetes",
            "मला मधुमेह आहे",
            "मुझे मधुमेह है"
        ]
        
        for query in test_queries:
            print(f"\nQuery: '{query}'")
            diseases = search_diseases_fuzzy(query, limit=3)
            if diseases:
                for d in diseases:
                    print(f"  ✅ Found: {d.get('name_en')} (ID: {d.get('id')})")
            else:
                print(f"  ❌ NO MATCH FOUND")

if __name__ == "__main__":
    main()
