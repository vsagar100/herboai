"""
Test API call with explicit detailed logging
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app
import json

app = create_app()

def test_single_language(lang, query):
    """Test a single language query"""
    print(f"\n{'='*70}")
    print(f"Testing {lang.upper()}: {query[:50]}...")
    print(f"{'='*70}")
    
    with app.test_client() as client:
        response = client.post(
            "/api/query",
            json={"text": query, "lang": lang},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"HTTP Status: {response.status_code}")
        data = response.get_json()
        
        # Get all keys
        print(f"Top-level keys: {list(data.keys())}")
        
        # Check structured
        struct = data.get('structured', {})
        print(f"Structured keys: {list(struct.keys())}")
        
        # Check each key
        for key in struct.keys():
            val = struct[key]
            if isinstance(val, list):
                print(f"  {key}: {len(val)} items")
            elif isinstance(val, dict):
                print(f"  {key}: dict with keys {list(val.keys())[:5]}")
            else:
                print(f"  {key}: {str(val)[:60]}")
        
        # Return count
        preps = struct.get('preparations', [])
        print(f"\n✅ Result: {len(preps)} preparations")
        return len(preps)

# Test each language
print("\n" + "="*70)
print("MULTILINGUAL API TEST")
print("="*70)

results = {}
results['en'] = test_single_language("en", "What should I take for diabetes?")
results['hi'] = test_single_language("hi", "मधुमेह के लिए मुझे क्या लेना चाहिए?")
results['mr'] = test_single_language("mr", "मधुमेह साठी मला काय घ्यावं?")

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'='*70}")
for lang, count in results.items():
    status = "✅" if count >= 6 else "❌"
    print(f"{status} {lang.upper()}: {count} preps")
