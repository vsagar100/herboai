"""
Test if Hindi issue is a session/state problem
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app

app = create_app()

def test_order():
    """Test different order of requests"""
    
    queries = [
        ("mr", "मधुमेह साठी मला काय घ्यावं?", "Marathi first"),
        ("hi", "मधुमेह के लिए मुझे क्या लेना चाहिए?", "Hindi second"),
        ("en", "What should I take for diabetes?", "English third"),
    ]
    
    print("\n" + "="*70)
    print("TEST 1: MR -> HI -> EN")
    print("="*70)
    
    with app.test_client() as client:
        for lang, query, label in queries:
            response = client.post(
                "/api/query",
                json={"text": query, "lang": lang},
                headers={"Content-Type": "application/json"}
            )
            
            data = response.get_json()
            preps = data.get('structured', {}).get('preparations', [])
            print(f"{label:20} | {lang:2} | Preps: {len(preps):2}")
    
    # Test reverse order
    print("\n" + "="*70)
    print("TEST 2: EN -> HI -> MR (Reverse order)")
    print("="*70)
    
    queries_reverse = [
        ("en", "What should I take for diabetes?", "English first"),
        ("hi", "मधुमेह के लिए मुझे क्या लेना चाहिए?", "Hindi second"),
        ("mr", "मधुमेह साठी मला काय घ्यावं?", "Marathi third"),
    ]
    
    with app.test_client() as client:
        for lang, query, label in queries_reverse:
            response = client.post(
                "/api/query",
                json={"text": query, "lang": lang},
                headers={"Content-Type": "application/json"}
            )
            
            data = response.get_json()
            preps = data.get('structured', {}).get('preparations', [])
            print(f"{label:20} | {lang:2} | Preps: {len(preps):2}")

if __name__ == "__main__":
    test_order()
