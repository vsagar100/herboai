"""
Detailed response structure inspection
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app

app = create_app()

def test_response_structure():
    """Check what's actually in the response"""
    with app.test_client() as client:
        marathi_query = "मधुमेह साठी काय घ्यावं?"
        
        response = client.post(
            "/api/query",
            json={
                "text": marathi_query,
                "lang": "mr"
            },
            headers={"Content-Type": "application/json"}
        )
        
        data = response.get_json()
        
        print("Response keys:", list(data.keys()))
        print("\nStructured keys:", list(data.get('structured', {}).keys()))
        
        struct = data.get('structured', {})
        print("\nDetailed structured data:")
        for key in struct.keys():
            val = struct[key]
            if isinstance(val, list):
                print(f"  {key}: [{len(val)} items]")
                if len(val) > 0:
                    print(f"    - First item keys: {list(val[0].keys()) if isinstance(val[0], dict) else type(val[0])}")
            elif isinstance(val, dict):
                print(f"  {key}: {list(val.keys())}")
            else:
                print(f"  {key}: {type(val).__name__} = {str(val)[:100]}")
        
        # Check if preparations are in the response but in a different location
        print("\n\nSearching for preparations...")
        if 'preparations' in struct and struct['preparations']:
            print(f"✅ Found in structured.preparations: {len(struct['preparations'])} items")
        
        if 'provisional' in data and data['provisional']:
            print(f"✅ Found in provisional: {len(data['provisional'])} items")
        
        answer = data.get('answer', '')
        if 'preparation' in answer.lower():
            print(f"✅ Found 'preparation' text in answer")

if __name__ == "__main__":
    test_response_structure()
