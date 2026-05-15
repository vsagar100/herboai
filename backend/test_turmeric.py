#!/usr/bin/env python
"""Test specific chat queries."""

from init import create_app
from services.chat import run_pipeline

def test():
    app = create_app()
    
    with app.app_context():
        # Test Turmeric milk preparation
        result = run_pipeline(user_text="Turmeric milk preparation", lang="en")
        
        print("=== TURMERIC MILK PREPARATION TEST ===\n")
        print(f"Severity: {result.get('severity')}")
        print(f"Provisional preps: {len(result.get('provisional', []))}")
        for p in result.get('provisional', [])[:3]:
            print(f"  - {p.get('name_en')}")
        print(f"\nAnswer (first 200 chars): {result.get('answer', '')[:200]}")

if __name__ == '__main__':
    test()
