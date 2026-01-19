"""
Detailed API response for each language
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app

app = create_app()

def test_api_responses():
    """Check what the API returns for each language"""
    
    test_cases = [
        ("en", "What should I take for diabetes?"),
        ("hi", "मधुमेह के लिए मुझे क्या लेना चाहिए?"),
        ("mr", "मधुमेह साठी मला काय घ्यावं?"),
    ]
    
    with app.test_client() as client:
        for lang, query in test_cases:
            print(f"\n{'='*60}")
            print(f"{lang.upper()}: Full API Response")
            print(f"{'='*60}")
            
            response = client.post(
                "/api/query",
                json={"text": query, "lang": lang},
                headers={"Content-Type": "application/json"}
            )
            
            data = response.get_json()
            
            print(f"Status: {response.status_code}")
            print(f"Response keys: {list(data.keys())}")
            print(f"Structured keys: {list(data.get('structured', {}).keys())}")
            
            struct = data.get('structured', {})
            preps = struct.get('preparations', [])
            
            print(f"\nPreparations count: {len(preps)}")
            if len(preps) > 0:
                print(f"First prep: {preps[0].get('name_en')}")
            
            # Print raw JSON for inspection
            print(f"\nRaw structured data:")
            print(json.dumps(struct, indent=2, default=str)[:500])

if __name__ == "__main__":
    test_api_responses()
