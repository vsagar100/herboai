#!/usr/bin/env python3
"""
Test and verify Marathi response returns correct preparations.
"""
import sys
import os
import json

sys.path.insert(0, str(os.path.dirname(os.path.abspath(__file__))))

from run import create_app

app = create_app()

test_cases = [
    ("मधुमेह साठी काय घ्यावं?", "mr", "Diabetes in Marathi"),
    ("diabetes", "en", "Diabetes in English"),
]

print("=" * 80)
print("Testing Marathi and English Query Results")
print("=" * 80)

with app.app_context():
    from services.chat import handle_chat
    
    for query, lang, desc in test_cases:
        print(f"\n{desc}")
        print(f"Query: {query}")
        print(f"Language: {lang}")
        
        try:
            result = handle_chat(query, lang=lang, session_id=None)
            
            structured = result.get("structured", {})
            preps = structured.get("preparations", [])
            
            print(f"✅ Condition: {structured.get('condition')}")
            print(f"✅ Preparations: {len(preps)}")
            
            if preps:
                print("   Preparation Details:")
                for i, prep in enumerate(preps, 1):
                    print(f"   {i}. {prep.get('name_en')} ({prep.get('form_type')})")
            else:
                print("   ⚠️  No preparations returned")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")

print("\n" + "=" * 80)
