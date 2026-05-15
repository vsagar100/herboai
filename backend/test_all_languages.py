"""
Comprehensive test: Verify Marathi/Hindi/English all work
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app

app = create_app()

def test_all_languages():
    """Test the same query in 3 languages"""
    
    test_cases = [
        ("en", "What should I take for diabetes?"),
        ("hi", "मधुमेह के लिए मुझे क्या लेना चाहिए?"),
        ("mr", "मधुमेह साठी मला काय घ्यावं?"),
    ]
    
    print(f"\n{'='*80}")
    print("COMPREHENSIVE MULTILINGUAL TEST")
    print(f"{'='*80}\n")
    
    results = []
    
    with app.test_client() as client:
        for lang, query in test_cases:
            print(f"Testing {lang.upper()}: {query[:60]}...")
            
            response = client.post(
                "/api/query",
                json={
                    "text": query,
                    "lang": lang
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.get_json()
                preps = data.get('structured', {}).get('preparations', [])
                answer_len = len(data.get('answer', ''))
                
                status = "✅" if len(preps) >= 6 else "⚠️"
                print(f"  {status} Answer: {answer_len} chars | Preparations: {len(preps)}")
                results.append((lang, len(preps) >= 6, len(preps)))
            else:
                print(f"  ❌ Error: Status {response.status_code}")
                results.append((lang, False, 0))
    
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}\n")
    
    all_pass = True
    for lang, success, count in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} | {lang.upper():2} | {count:2} preparations")
        if not success:
            all_pass = False
    
    print(f"\n{'='*80}")
    if all_pass:
        print("🎉 ALL TESTS PASSED - Multilingual queries working!")
    else:
        print("⚠️  Some tests failed")
    print(f"{'='*80}\n")
    
    return all_pass

if __name__ == "__main__":
    success = test_all_languages()
    sys.exit(0 if success else 1)
