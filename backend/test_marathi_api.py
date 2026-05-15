"""
Test the complete flow: Simulate frontend API call
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app

app = create_app()

def test_marathi_api():
    """Simulate what the frontend sends to /api/query"""
    with app.test_client() as client:
        marathi_query = "मधुमेह साठी काय घ्यावं?"
        
        print(f"\n{'='*80}")
        print(f"Testing Frontend API Call")
        print(f"{'='*80}")
        print(f"\nQuery: {marathi_query}")
        print(f"Endpoint: POST /api/query")
        
        # Simulate frontend request
        response = client.post(
            "/api/query",
            json={
                "text": marathi_query,
                "lang": "mr"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.get_json()
            
            print(f"\n{'='*80}")
            print("RESPONSE STRUCTURE:")
            print(f"{'='*80}")
            print(f"Answer length: {len(data.get('answer', ''))} chars")
            print(f"Intent: {data.get('intent')}")
            print(f"Language: {data.get('detected_language')}")
            
            structured = data.get('structured', {})
            print(f"\nStructured data keys: {list(structured.keys())}")
            
            if 'disease' in structured and structured['disease']:
                print(f"  Disease: {structured['disease'].get('name')}")
            
            preps = structured.get('preparations', [])
            if preps:
                print(f"  Preparations found: {len(preps)}")
                for i, prep in enumerate(preps[:3], 1):
                    print(f"    {i}. {prep.get('name_en', 'Unknown')}")
            
            print(f"\n{'='*80}")
            print("ANSWER PREVIEW (first 500 chars):")
            print(f"{'='*80}")
            answer = data.get('answer', '')
            # Just print the length and first part (avoid encoding issues in terminal)
            print(f"[{len(answer)} total characters]")
            print(answer[:500] if len(answer) > 500 else answer)
            
            # Verify success
            if preps and len(preps) >= 6:
                print(f"\n✅ SUCCESS: Got {len(preps)} preparations (expected 6+)")
                return True
            else:
                print(f"\n⚠️  WARNING: Got {len(preps) if preps else 0} preparations (expected 6+)")
                return False
        else:
            print(f"❌ ERROR: Status {response.status_code}")
            print(f"Response: {response.get_json()}")
            return False

if __name__ == "__main__":
    success = test_marathi_api()
    sys.exit(0 if success else 1)
