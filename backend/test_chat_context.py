#!/usr/bin/env python
"""Test chat pipeline with Flask context."""

from init import create_app
from services.chat import run_pipeline

def test_with_context():
    app = create_app()
    
    with app.app_context():
        test_queries = [
            ("I have running nose and coughing last 5 days", "en"),
            ("I have cold", "en"),
            ("Turmeric milk preparation", "en"),
        ]
        
        print("=== TESTING CHAT PIPELINE WITH FLASK CONTEXT ===\n")
        
        for query, lang in test_queries:
            print(f"Query: '{query}'")
            print("-" * 60)
            
            try:
                result = run_pipeline(user_text=query, lang=lang)
                
                severity = result.get('severity', {})
                preps = result.get('provisional', [])
                followups = result.get('followups', [])
                
                print(f"Severity: {severity.get('band', 'unknown')}")
                print(f"Provisional preps: {len(preps)} items")
                for p in preps[:3]:
                    print(f"  - {p.get('name_en')}")
                
                print(f"Followups: {len(followups)} items")
                
                answer = result.get('answer', '')
                if len(answer) > 150:
                    print(f"Answer: {answer[:150]}...")
                else:
                    print(f"Answer: {answer}")
                    
            except Exception as e:
                print(f"ERROR: {str(e)[:200]}")
            
            print("\n")

if __name__ == '__main__':
    test_with_context()
