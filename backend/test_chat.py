#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test chat pipeline with disease query."""

import sys
import os
from services.chat import run_pipeline
import json

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'

def test_chat():
    test_queries = [
        ("I have running nose and coughing last 5 days", "en"),
        ("I have cold", "en"),
        ("Tell me about Ashwagandha", "en"),
        ("Turmeric milk preparation", "en"),
    ]
    
    print("=== TESTING CHAT PIPELINE ===\n")
    
    for query, lang in test_queries:
        print(f"Query: '{query}' (lang: {lang})")
        print("-" * 50)
        
        try:
            result = run_pipeline(user_text=query, lang=lang)
            
            print(f"Severity: {result.get('severity')}")
            print(f"Provisional preps: {len(result.get('provisional', []))} items")
            if result.get('provisional'):
                for p in result['provisional'][:2]:
                    print(f"  - {p.get('name_en')}")
            
            print(f"Followups: {len(result.get('followups', []))} items")
            
            # First 200 chars of answer
            answer = result.get('answer', '')[:200]
            print(f"Answer preview: {answer}...")
            
        except Exception as e:
            print(f"ERROR: {str(e)}")
        
        print("\n")

if __name__ == '__main__':
    test_chat()
