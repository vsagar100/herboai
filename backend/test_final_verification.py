#!/usr/bin/env python3
"""
Final verification: Test Marathi query through the API pipeline.
"""
import sys
import os

sys.path.insert(0, str(os.path.dirname(os.path.abspath(__file__))))

from run import create_app

app = create_app()

print("=" * 80)
print("FINAL VERIFICATION: Marathi Query Pipeline")
print("=" * 80)

with app.app_context():
    from services.chat import run_pipeline
    
    # Test the exact user query that was failing
    marathi_query = "मधुमेह साठी काय घ्यावं?"  # "What to take for diabetes in Marathi?"
    
    print(f"\nTesting query: {marathi_query}")
    print(f"Language: Marathi (mr)")
    
    result = run_pipeline(user_text=marathi_query, session_id="test-session", lang="mr")
    
    structured = result.get("structured", {})
    preps = structured.get("preparations", [])
    
    print(f"\n✅ RESULT:")
    print(f"   Condition detected: {structured.get('condition')}")
    print(f"   Number of preparations: {len(preps)}")
    
    if len(preps) > 0:
        print(f"\n   ✅ SUCCESS! Preparations returned:")
        for i, prep in enumerate(preps, 1):
            name = prep.get('name_en', 'Unknown')
            form = prep.get('form_type', '?')
            print(f"      {i}. {name} ({form})")
    else:
        print(f"\n   ❌ FAILED: No preparations returned")
        
    # Check response message includes preparations
    answer_text = result.get("answer", "")
    if "Jamun" in answer_text or "Vijayasar" in answer_text:
        print(f"\n   ✅ Answer includes preparation details")
    elif "no mapped preparation" in answer_text.lower() or "नाही" in answer_text:
        print(f"\n   ⚠️  Answer indicates no preparations found")
    else:
        print(f"\n   ✓ Answer provided (checking content...)")

print("\n" + "=" * 80)
print("Verification Complete")
print("=" * 80)
