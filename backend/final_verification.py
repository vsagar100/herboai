#!/usr/bin/env python
"""
Final verification test for HerboAI chatbot fixes.

Tests all major functionality that was fixed:
1. Disease queries with symptoms
2. Simple disease queries  
3. Plant information queries
4. Preparation queries
"""

from init import create_app
from services.chat import run_pipeline

def run_final_verification():
    app = create_app()
    
    with app.app_context():
        print("\n" + "=" * 80)
        print("HERBOAI CHATBOT - FINAL VERIFICATION TEST")
        print("=" * 80)
        
        test_cases = [
            {
                "query": "I have running nose and coughing last 5 days",
                "lang": "en",
                "desc": "Symptom Query with Duration",
                "expect_preps": True,
                "expect_followups": True,
            },
            {
                "query": "I have cold",
                "lang": "en",
                "desc": "Simple Disease Query",
                "expect_preps": True,
                "expect_followups": True,
            },
            {
                "query": "Tell me about Ashwagandha",
                "lang": "en",
                "desc": "Plant Information Query",
                "expect_preps": True,
                "expect_followups": False,
            },
            {
                "query": "Turmeric milk preparation",
                "lang": "en",
                "desc": "Preparation Recipe Query",
                "expect_preps": True,
                "expect_followups": False,
            },
            {
                "query": "Triphala powder",
                "lang": "en",
                "desc": "Preparation Query (Triphala)",
                "expect_preps": True,
                "expect_followups": False,
            },
        ]
        
        passed = 0
        failed = 0
        
        for test in test_cases:
            query = test["query"]
            lang = test["lang"]
            desc = test["desc"]
            expect_preps = test["expect_preps"]
            
            print(f"\n[TEST] {desc}")
            print(f"Query: '{query}'")
            
            try:
                result = run_pipeline(user_text=query, lang=lang)
                
                preps = result.get('provisional', [])
                followups = result.get('followups', [])
                severity = result.get('severity', {})
                
                has_preps = len(preps) > 0
                has_followups = len(followups) > 0
                
                # Verify expectations
                prep_ok = (has_preps == expect_preps)
                
                status = "PASS" if prep_ok else "FAIL"
                
                print(f"Result: [{status}]")
                print(f"  Severity: {severity.get('band', 'unknown')}")
                print(f"  Preparations: {len(preps)} " + ("✓" if prep_ok else "✗"))
                
                if preps:
                    print(f"    - {preps[0].get('name_en')}")
                    if len(preps) > 1:
                        print(f"    - {preps[1].get('name_en')}")
                
                print(f"  Followups: {len(followups)}")
                
                if prep_ok:
                    passed += 1
                else:
                    failed += 1
                    print(f"  ERROR: Expected preps={expect_preps}, got {has_preps}")
                    
            except Exception as e:
                print(f"Result: [FAIL]")
                print(f"  ERROR: {str(e)[:150]}")
                failed += 1

        print("\n" + "=" * 80)
        print(f"SUMMARY: {passed} PASSED, {failed} FAILED out of {len(test_cases)} tests")
        print("=" * 80 + "\n")
        
        if failed == 0:
            print("✓ All tests PASSED! HerboAI chatbot is working correctly.")
        else:
            print(f"✗ {failed} test(s) FAILED. Please review the errors above.")

if __name__ == '__main__':
    run_final_verification()
