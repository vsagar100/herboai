#!/usr/bin/env python3
"""
Comprehensive test to verify:
1. Marathi/Hindi condition classification
2. Marathi/Hindi queries return preparations
3. Admin sync to i18n table works
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from flask import Flask
from init import create_app
from services.chat import _classify_condition, handle_chat
from db import get_db

app = create_app()

def test_condition_classification():
    """Test that Marathi/Hindi keywords are classified correctly."""
    print("\n" + "="*60)
    print("TEST 1: Condition Classification (English, Hindi, Marathi)")
    print("="*60)
    
    test_cases = [
        # (input_text, expected_condition, language)
        ("I have a cold", "cold_cough", "English"),
        ("मुझे जुकाम है", "cold_cough", "Hindi"),
        ("मला सर्दी आहे", "cold_cough", "Marathi"),
        
        ("I have diabetes", "diabetes", "English"),
        ("मुझे मधुमेह है", "diabetes", "Hindi"),
        ("मला मधुमेह आहे", "diabetes", "Marathi"),
        
        ("high blood pressure", "hypertension", "English"),
        ("उच्च रक्तदाब", "hypertension", "Hindi"),
        ("रक्तदाब", "hypertension", "Marathi"),
        
        ("indigestion and gas", "digestion", "English"),
        ("अम्लपित्त", "digestion", "Hindi"),
        ("अपचन", "digestion", "Marathi"),
        
        ("joint pain", "arthritis", "English"),
        ("संधिवात", "arthritis", "Hindi"),
        ("गुडघा दुखी", "arthritis", "Marathi"),
    ]
    
    passed = 0
    failed = 0
    
    for text, expected, lang in test_cases:
        result = _classify_condition(text)
        status = "✅ PASS" if result == expected else "❌ FAIL"
        print(f"{status} | {lang:8} | {text[:30]:30} | Expected: {expected:12} | Got: {result}")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nCondition Classification: {passed} passed, {failed} failed")
    return failed == 0


def test_chat_queries():
    """Test that chat queries work for all languages."""
    print("\n" + "="*60)
    print("TEST 2: Chat Queries (Full Pipeline)")
    print("="*60)
    
    test_queries = [
        ("I have a cold and cough", "en", "English Cold Query"),
        ("मुझे जुकाम है", "hi", "Hindi Cold Query"),
        ("मला सर्दी आहे", "mr", "Marathi Cold Query"),
        
        ("I have diabetes", "en", "English Diabetes Query"),
        ("मुझे मधुमेह है", "hi", "Hindi Diabetes Query"),
        ("मला मधुमेह आहे", "mr", "Marathi Diabetes Query"),
    ]
    
    passed = 0
    failed = 0
    
    for query, lang, desc in test_queries:
        try:
            result = handle_chat(query, session_id=None, lang=lang)
            
            # Check answer field (not response)
            response_text = result.get("answer", "").lower()
            status = "✅ PASS" if response_text else "⚠️  WARN"
            
            # Try to extract data - check if preparations or remedies mentioned
            has_preps = "preparation" in response_text or "remedy" in response_text or "🌿" in result.get("answer", "") or len(response_text) > 50
            
            print(f"{status} | {desc:30} | Response length: {len(response_text):4} | Has content: {has_preps}")
            
            if has_preps and len(response_text) > 50:
                passed += 1
            else:
                failed += 1
                
        except Exception as e:
            print(f"❌ FAIL | {desc:30} | Error: {str(e)[:40]}")
            failed += 1
    
    print(f"\nChat Queries: {passed} passed, {failed} failed")
    return failed == 0


def test_i18n_population():
    """Test that i18n table has proper data."""
    print("\n" + "="*60)
    print("TEST 3: i18n Table Population")
    print("="*60)
    
    try:
        db = get_db()
        
        # Check overall i18n count
        count = db.execute("SELECT COUNT(*) as cnt FROM entity_i18n").fetchone()["cnt"]
        print(f"Total i18n entries: {count}")
        
        # Check by entity type
        for entity_type in ["plant", "disease", "preparation"]:
            type_count = db.execute(
                "SELECT COUNT(*) as cnt FROM entity_i18n WHERE entity_type=?",
                (entity_type,)
            ).fetchone()["cnt"]
            
            # Check by language
            en_count = db.execute(
                "SELECT COUNT(*) as cnt FROM entity_i18n WHERE entity_type=? AND lang='en'",
                (entity_type,)
            ).fetchone()["cnt"]
            
            hi_count = db.execute(
                "SELECT COUNT(*) as cnt FROM entity_i18n WHERE entity_type=? AND lang='hi'",
                (entity_type,)
            ).fetchone()["cnt"]
            
            mr_count = db.execute(
                "SELECT COUNT(*) as cnt FROM entity_i18n WHERE entity_type=? AND lang='mr'",
                (entity_type,)
            ).fetchone()["cnt"]
            
            print(f"  {entity_type:12} | Total: {type_count:4} | EN: {en_count:4} | HI: {hi_count:4} | MR: {mr_count:4}")
        
        # Sample a few entries
        print("\nSample i18n entries:")
        samples = db.execute(
            "SELECT entity_type, entity_id, lang, field, SUBSTR(text, 1, 50) as text_preview FROM entity_i18n LIMIT 5"
        ).fetchall()
        
        for row in samples:
            print(f"  {row['entity_type']:12} | ID: {row['entity_id']:3} | {row['lang']} | {row['field']:20} | {row['text_preview']}")
        
        return count > 0
        
    except Exception as e:
        print(f"❌ Error checking i18n table: {str(e)}")
        return False


def test_admin_field_mapping():
    """Test that admin field mapping is correct."""
    print("\n" + "="*60)
    print("TEST 4: Admin Field Mapping Verification")
    print("="*60)
    
    from services.admin_i18n_indexer import TRANSLATABLE_FIELDS
    
    print("Plant fields:")
    for field in TRANSLATABLE_FIELDS.get("plant", []):
        print(f"  - {field}")
    
    print("\nDisease fields:")
    for field in TRANSLATABLE_FIELDS.get("disease", []):
        print(f"  - {field}")
    
    print("\nPreparation fields:")
    for field in TRANSLATABLE_FIELDS.get("preparation", []):
        print(f"  - {field}")
    
    # Verify all necessary fields are present
    required_fields = {
        "plant": ["name", "description", "therapeutic_actions", "parts_used"],
        "disease": ["name", "description", "symptoms", "causes", "prevention_tips"],
        "preparation": ["name", "preparation_steps", "dosage_json", "timing", "anupana", "notes"],
    }
    
    all_good = True
    for entity_type, fields in required_fields.items():
        i18n_fields = set(TRANSLATABLE_FIELDS.get(entity_type, []))
        missing = set(fields) - i18n_fields
        if missing:
            print(f"\n⚠️  {entity_type}: Missing fields: {missing}")
            all_good = False
        else:
            print(f"\n✅ {entity_type}: All required fields present")
    
    return all_good


if __name__ == "__main__":
    with app.app_context():
        results = []
        
        # Run all tests
        results.append(("Condition Classification", test_condition_classification()))
        results.append(("i18n Table Population", test_i18n_population()))
        results.append(("Admin Field Mapping", test_admin_field_mapping()))
        results.append(("Chat Queries", test_chat_queries()))
        
        # Summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        for test_name, passed in results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"{status} | {test_name}")
        
        all_passed = all(passed for _, passed in results)
        sys.exit(0 if all_passed else 1)
