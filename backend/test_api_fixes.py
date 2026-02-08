"""Test API endpoints for preparation query fixes."""
import requests
import json
import sys

BASE = "http://127.0.0.1:5000/api/query"

tests = [
    # Fixed prep queries (were broken)
    ("गुडमारचा काढा कसा बनवायचा?", "Gudmar prep (was Bamboo)"),
    ("हळदीचे दूध बनवण्याची पद्धत", "Turmeric milk (was Kovidara_Vine)"),
    ("अश्वगंधाबद्दल सांगा", "Ashwagandha info (was working)"),
    # Regression tests
    ("मुरुमांसाठी निंब", "Neem for pimples (Marathi)"),
    ("I have diabetes. What helps?", "Diabetes English"),
    ("neem for acne", "Neem for acne English"),
]

for text, label in tests:
    print(f"\n{'='*70}")
    print(f"TEST: {label}")
    print(f"Query: {text}")
    print(f"{'='*70}")
    try:
        r = requests.post(BASE, json={"text": text}, timeout=120)
        data = r.json()
        print(f"Intent: {data.get('intent')}")
        print(f"Language: {data.get('detected_language')}")
        
        structured = data.get("structured", {})
        plants = structured.get("plants", [])
        preps = structured.get("preparations", [])
        condition = structured.get("condition", "")
        
        if plants:
            print(f"Plants: {[p.get('name') or p.get('common_name') for p in plants]}")
        if preps:
            print(f"Preparations ({len(preps)}):")
            for p in preps[:3]:
                print(f"  - {p.get('name', p.get('name_en', '?'))}")
        if condition:
            print(f"Condition: {condition}")
        
        answer = data.get("answer", "")
        # Print first 300 chars of answer
        print(f"Answer preview: {answer[:300]}...")
    except Exception as e:
        print(f"ERROR: {e}")

print(f"\n{'='*70}")
print("ALL TESTS COMPLETE")
