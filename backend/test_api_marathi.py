#!/usr/bin/env python3
"""
Test the API endpoint directly with Marathi query.
"""
import requests
import json

BASE_URL = "http://localhost:5000"

test_queries = [
    {"query": "मधुमेह साठी काय घ्यावं?", "lang": "mr", "desc": "What to take for diabetes in Marathi"},
]

print("=" * 80)
print("Testing API Endpoint with Marathi Query")
print("=" * 80)

for test in test_queries:
    print(f"\nQuery: {test['query']}")
    print(f"Language: {test['lang']}")
    print(f"Description: {test['desc']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/query",
            json={"query": test["query"], "lang": test["lang"], "session_id": None},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            prep_count = len(result.get("structured", {}).get("preparations", []))
            print(f"✅ Status: {response.status_code}")
            print(f"   Preparations: {prep_count}")
            if prep_count > 0:
                print("   First 2 preparations:")
                for prep in result["structured"]["preparations"][:2]:
                    print(f"     - {prep.get('name_en', 'N/A')}")
        else:
            print(f"❌ Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

print("\n" + "=" * 80)
print("Note: Make sure the Flask server is running on port 5000")
print("=" * 80)
