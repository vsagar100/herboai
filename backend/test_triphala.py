#!/usr/bin/env python
"""Test Triphala powder query."""

from init import create_app
from services.chat import run_pipeline

app = create_app()
with app.app_context():
    result = run_pipeline(user_text="Triphala powder", lang="en")
    
    print("=== TRIPHALA POWDER TEST ===\n")
    print(f"Severity: {result.get('severity')}")
    print(f"Provisional preps: {len(result.get('provisional', []))}")
    for p in result.get('provisional', []):
        print(f"  - {p.get('name_en')}")
    
    answer = result.get('answer', '')
    if len(answer) > 150:
        print(f"\nAnswer (first 150 chars): {answer[:150]}...")
    else:
        print(f"\nAnswer: {answer}")
