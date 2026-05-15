"""
Test actual API response for diabetes queries in different languages
"""
import sys
sys.path.insert(0, '.')

import json
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Import after Flask is initialized
from services.chat import handle_chat

def test_query(query, lang):
    """Test a query and show the response"""
    print(f"\n{'='*80}")
    print(f"QUERY: {query} (lang={lang})")
    print('='*80)
    
    try:
        with app.app_context():
            result = handle_chat(query, session_id=f"test_{lang}", lang=lang)
            
            print(f"\nStatus: {result.get('status')}")
            print(f"Stage: {result.get('stage')}")
            print(f"Answer (first 200 chars): {result.get('answer', '')[:200]}")
            
            # Check remedies (key is 'provisional', not 'remedies')
            remedies = result.get('provisional', [])
            print(f"\n✅ Remedies/Preparations count: {len(remedies)}")
            
            if remedies:
                print("\nRemedies:")
                for i, rem in enumerate(remedies[:5], 1):
                    print(f"\n  {i}. {rem.get('name_en') or rem.get('name', 'Unknown')}")
                    print(f"     ID: {rem.get('id')}")
                    print(f"     Form: {rem.get('form_type', 'N/A')}")
            else:
                print("\n❌ NO REMEDIES RETURNED!")
                print("\nThis is the issue the user is reporting.")
            
            # Check questions (key is 'followups', not 'questions')
            questions = result.get('followups', [])
            print(f"\n📋 Questions count: {len(questions)}")
            if questions:
                for q in questions[:3]:
                    print(f"  - {q}")
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

def main():
    print("\n" + "="*80)
    print("TESTING ACTUAL API RESPONSES FOR DIABETES")
    print("="*80)
    
    # Test in different languages
    test_queries = [
        ("I have diabetes", "en"),
        ("मुझे मधुमेह है", "hi"),
        ("मला मधुमेह आहे", "mr"),
    ]
    
    for query, lang in test_queries:
        test_query(query, lang)
    
    print("\n\n" + "="*80)
    print("DIAGNOSIS")
    print("="*80)
    print("""
If remedies count = 0:
  → entity_i18n has corrupted data
  → System is trying to return Hindi/Marathi names from entity_i18n
  → But the names are garbled (transliterated English, not proper translation)
  → Frontend displays garbled text or filters them out
  
Fix: 
  1. Use base table columns (common_name_hi, common_name_mr) instead of entity_i18n
  2. OR: Re-translate entity_i18n data properly
    """)

if __name__ == "__main__":
    main()
