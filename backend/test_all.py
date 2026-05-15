#!/usr/bin/env python
"""Comprehensive test of all chat fixes."""

from init import create_app
from services.chat import run_pipeline

def test_all():
    app = create_app()
    
    with app.app_context():
        tests = [
            ("Running nose and coughing last 5 days", "en", "disease query with symptoms"),
            ("I have cold", "en", "simple disease query"),
            ("Tell me about Ashwagandha", "en", "plant info query"),
            ("Turmeric milk preparation", "en", "preparation query"),
        ]
        
        print("=" * 70)
        print("COMPREHENSIVE CHAT PIPELINE TEST")
        print("=" * 70)
        
        for query, lang, desc in tests:
            print(f"\n{desc}")
            print(f"Query: '{query}'")
            print("-" * 70)
            
            try:
                result = run_pipeline(user_text=query, lang=lang)
                
                severity = result.get('severity', {})
                preps = result.get('provisional', [])
                followups = result.get('followups', [])
                
                status = "PASS" if (preps if desc != "plant info query" else True) else "FAIL"
                
                print(f"[{status}] Severity: {severity.get('band', 'unknown')}")
                print(f"[{status}] Preparations: {len(preps)} found", end="")
                if preps:
                    print(f" ({preps[0].get('name_en')}...)")
                else:
                    print()
                print(f"[INFO] Followups: {len(followups)}")
                
            except Exception as e:
                print(f"[FAIL] ERROR: {str(e)[:100]}")

if __name__ == '__main__':
    test_all()
