"""
Diagnostic script to check non-English query processing flow
Tests:
1. Language detection
2. Intent classification
3. Entity extraction (direct from query, not translated)
4. Disease/plant ID resolution
5. entity_i18n data availability
"""

import sys
sys.path.insert(0, '.')

from flask import Flask
from config import Config

# Initialize Flask app for context
app = Flask(__name__)
app.config.from_object(Config)

from db import get_db
from api.nlu_optimized import detect_language, classify_intent, extract_entities
from services.indic_translation_service import translate_to_en

# Test queries in different languages
TEST_QUERIES = {
    "hindi": [
        "मुझे मधुमेह है",
        "डायबिटीज के लिए क्या करें",
        "खांसी का इलाज बताएं",
        "तुलसी के फायदे क्या हैं"
    ],
    "marathi": [
        "मला मधुमेह आहे",
        "डायबिटीससाठी काय करावे",
        "खोकला बरा करण्यासाठी",
        "तुळशीचे फायदे काय आहेत"
    ],
    "english": [
        "I have diabetes",
        "What to do for diabetes",
        "Cure for cough",
        "Benefits of tulsi"
    ]
}

def check_entity_i18n_data():
    """Check if entity_i18n has data for Hindi/Marathi"""
    db = get_db()
    
    print("\n" + "="*80)
    print("ENTITY_I18N DATA CHECK")
    print("="*80)
    
    # Count by entity_type and lang
    rows = db.execute("""
        SELECT entity_type, lang, COUNT(*) as count
        FROM entity_i18n
        GROUP BY entity_type, lang
        ORDER BY entity_type, lang
    """).fetchall()
    
    print("\n📊 Entity i18n counts by type and language:")
    for row in rows:
        print(f"  {row['entity_type']:12} | {row['lang']:4} | {row['count']:6} records")
    
    # Check specific diseases for Hindi/Marathi data
    print("\n🔍 Sample disease translations:")
    disease_check = db.execute("""
        SELECT d.id, d.name_en, d.name_hi, d.name_mr,
               GROUP_CONCAT(ei.lang || ':' || ei.text, ' | ') as translations
        FROM diseases d
        LEFT JOIN entity_i18n ei ON ei.entity_type='disease' AND ei.entity_id=d.id AND ei.field='name'
        WHERE d.name_en IN ('Diabetes', 'Cough', 'Cold', 'Fever', 'Hypertension')
        GROUP BY d.id
    """).fetchall()
    
    for row in disease_check:
        print(f"\n  Disease: {row['name_en']} (ID: {row['id']})")
        print(f"    Base table: hi={row['name_hi']}, mr={row['name_mr']}")
        print(f"    entity_i18n: {row['translations'] or 'NONE'}")
    
    # Check specific plants
    print("\n🔍 Sample plant translations:")
    plant_check = db.execute("""
        SELECT p.id, p.common_name_en, p.common_name_hi, p.common_name_mr,
               GROUP_CONCAT(ei.lang || ':' || ei.text, ' | ') as translations
        FROM plants p
        LEFT JOIN entity_i18n ei ON ei.entity_type='plant' AND ei.entity_id=p.id AND ei.field='name'
        WHERE p.common_name_en IN ('Tulsi', 'Neem', 'Turmeric', 'Ashwagandha', 'Giloy')
        GROUP BY p.id
    """).fetchall()
    
    for row in plant_check:
        print(f"\n  Plant: {row['common_name_en']} (ID: {row['id']})")
        print(f"    Base table: hi={row['common_name_hi']}, mr={row['common_name_mr']}")
        print(f"    entity_i18n: {row['translations'] or 'NONE'}")

def test_query_flow(query, expected_lang):
    """Test complete flow for a single query"""
    print("\n" + "-"*80)
    print(f"QUERY: {query}")
    print("-"*80)
    
    # 1. Language detection
    detected_lang = detect_language(query)
    print(f"\n1️⃣  Language Detection:")
    print(f"    Expected: {expected_lang}")
    print(f"    Detected: {detected_lang}")
    print(f"    ✅ MATCH" if detected_lang == expected_lang else f"    ❌ MISMATCH")
    
    # 2. Intent classification
    intent = classify_intent(query)
    print(f"\n2️⃣  Intent Classification:")
    print(f"    Intent: {intent}")
    
    # 3. Translation (if needed)
    if detected_lang != "en":
        try:
            query_en = translate_to_en(query, lang_hint=detected_lang)
            print(f"\n3️⃣  Translation to English:")
            print(f"    Original: {query}")
            print(f"    Translated: {query_en}")
        except Exception as e:
            print(f"\n3️⃣  Translation FAILED: {e}")
            query_en = query
    else:
        query_en = query
        print(f"\n3️⃣  No translation needed (English)")
    
    # 4. Entity extraction (works on original query, not translated)
    plants, diseases = extract_entities(query, query_en)
    
    print(f"\n4️⃣  Entity Extraction (from original query):")
    print(f"    Plants found: {len(plants)}")
    for i, plant in enumerate(plants[:3], 1):
        print(f"      {i}. {plant.get('common_name_en')} (ID: {plant.get('id')}) - Score: {plant.get('score', 'N/A')}")
    
    print(f"    Diseases found: {len(diseases)}")
    for i, disease in enumerate(diseases[:3], 1):
        print(f"      {i}. {disease.get('name_en')} (ID: {disease.get('id')}) - Score: {disease.get('score', 'N/A')}")
    
    # 5. Check if entity_i18n has data for detected entities
    if diseases:
        disease_id = diseases[0].get('id')
        if disease_id:
            db = get_db()
            print(f"\n5️⃣  entity_i18n data for disease '{diseases[0].get('name_en')}' (ID: {disease_id}):")
            
            for lang in ['en', 'hi', 'mr']:
                i18n_data = db.execute("""
                    SELECT field, text
                    FROM entity_i18n
                    WHERE entity_type='disease' AND entity_id=? AND lang=?
                """, (disease_id, lang)).fetchall()
                
                if i18n_data:
                    print(f"    {lang.upper()}:")
                    for row in i18n_data:
                        text = row['text'][:50] + "..." if len(row['text']) > 50 else row['text']
                        print(f"      - {row['field']}: {text}")
                else:
                    print(f"    {lang.upper()}: ❌ NO DATA")
    
    return detected_lang, intent, plants, diseases

def main():
    with app.app_context():
        print("\n" + "="*80)
        print("NON-ENGLISH QUERY FLOW DIAGNOSTIC")
        print("="*80)
        
        # First check if we have i18n data
        check_entity_i18n_data()
    
        # Test each query
        print("\n\n" + "="*80)
        print("TESTING QUERIES")
        print("="*80)
        
        results = []
        
        for lang_name, queries in TEST_QUERIES.items():
            print(f"\n\n{'='*80}")
            print(f"{lang_name.upper()} QUERIES")
            print('='*80)
            
            for query in queries:
                result = test_query_flow(query, lang_name[:2])  # 'hi', 'mr', 'en'
                results.append((query, result))
        
        # Summary
        print("\n\n" + "="*80)
        print("SUMMARY")
        print("="*80)
        
        print("\n📋 Issues Found:")
        issues = []
        
        for query, (detected_lang, intent, plants, diseases) in results:
            if not diseases and not plants:
                issues.append(f"  ❌ No entities found: {query}")
        
        if issues:
            for issue in issues:
                print(issue)
        else:
            print("  ✅ All queries returned entities")

if __name__ == "__main__":
    main()
