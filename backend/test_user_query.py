"""
Test the EXACT user query
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app

app = create_app()

def test_user_query():
    """Test the exact query the user reported"""
    query = "मधुमेह साठी काय घ्यावं?"
    
    print(f"\n{'='*80}")
    print(f"USER QUERY TEST")
    print(f"{'='*80}")
    print(f"\nQuery: {query}")
    print(f"Language: Marathi")
    
    with app.test_client() as client:
        response = client.post(
            "/api/query",
            json={"text": query, "lang": "mr"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.get_json()
            
            preps = data.get('structured', {}).get('preparations', [])
            answer_len = len(data.get('answer', ''))
            
            print(f"\nStatus: ✅ Success (HTTP 200)")
            print(f"Answer length: {answer_len} characters")
            print(f"Preparations found: {len(preps)}")
            
            if len(preps) > 0:
                print(f"\nPreparation names:")
                for i, prep in enumerate(preps[:6], 1):
                    print(f"  {i}. {prep.get('name_en')}")
            
            print(f"\n{'='*80}")
            if len(preps) >= 6:
                print("✅ FIXED! Query is now working correctly!")
            else:
                print(f"⚠️  Only {len(preps)} preps (expected 6+)")
            print(f"{'='*80}\n")
        else:
            print(f"❌ Error: HTTP {response.status_code}")
            print(data.get('error', 'Unknown error'))

if __name__ == "__main__":
    test_user_query()
