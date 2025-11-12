#!/usr/bin/env python3
"""
Test script to verify the optimized multilingual chat pipeline
Run after migration to ensure everything works
"""
import requests
import json
import time
import sys
from typing import Dict, List

BASE_URL = "http://localhost:5000"

# Test cases covering all languages and intents
TEST_CASES = [
    {
        "name": "Hindi - Diabetes Remedy",
        "query": "मुझे मधुमेह है। कौन सी जड़ी बूटी मदद करेगी?",
        "expected_lang": "hi",
        "expected_intent": "remedy_lookup",
        "should_have": ["plants", "disease"]
    },
    {
        "name": "Marathi - Tulsi Info",
        "query": "तुळस बद्दल माहिती द्या",
        "expected_lang": "mr",
        "expected_intent": "plant_info",
        "should_have": ["plant"]
    },
    {
        "name": "English - Guduchi Preparation",
        "query": "How to prepare Guduchi decoction?",
        "expected_lang": "en",
        "expected_intent": "preparation_info",
        "should_have": ["plants"]
    },
    {
        "name": "Hindi - Cold Remedy",
        "query": "सर्दी और खांसी के लिए क्या लूं?",
        "expected_lang": "hi",
        "expected_intent": "remedy_lookup",
        "should_have": ["plants"]
    },
    {
        "name": "Marathi - BP Query",
        "query": "बीपी कमी करायचा आहे",
        "expected_lang": "mr",
        "expected_intent": "remedy_lookup",
        "should_have": ["plants"]
    },
    {
        "name": "English - Ashwagandha Benefits",
        "query": "What are the benefits of Ashwagandha?",
        "expected_lang": "en",
        "expected_intent": "plant_info",
        "should_have": ["plant"]
    }
]

def test_health_endpoint():
    """Test if backend is running"""
    print("\n" + "="*60)
    print("TESTING: Backend Health")
    print("="*60)
    
    try:
        resp = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if resp.status_code == 200:
            print("✅ Backend is running")
            print(f"   Response: {resp.json()}")
            return True
        else:
            print(f"❌ Backend returned {resp.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend not reachable: {e}")
        return False

def test_query(test_case: Dict) -> Dict:
    """Test a single query"""
    print(f"\n{'─'*60}")
    print(f"TEST: {test_case['name']}")
    print(f"{'─'*60}")
    print(f"Query: {test_case['query']}")
    
    result = {
        "name": test_case["name"],
        "passed": False,
        "time": 0,
        "errors": []
    }
    
    try:
        start = time.time()
        
        resp = requests.post(
            f"{BASE_URL}/api/query",
            json={"text": test_case["query"]},
            headers={"x-session-id": f"test-{int(time.time())}"},
            timeout=60
        )
        
        elapsed = time.time() - start
        result["time"] = elapsed
        
        if resp.status_code != 200:
            result["errors"].append(f"Status code: {resp.status_code}")
            print(f"❌ Status: {resp.status_code}")
            print(f"   Response: {resp.text[:200]}")
            return result
        
        data = resp.json()
        
        # Check response structure
        if "answer" not in data:
            result["errors"].append("Missing 'answer' field")
        
        if "detected_language" not in data:
            result["errors"].append("Missing 'detected_language' field")
        
        if "intent" not in data:
            result["errors"].append("Missing 'intent' field")
        
        if "structured" not in data:
            result["errors"].append("Missing 'structured' field")
        
        # Validate detected language
        detected_lang = data.get("detected_language")
        expected_lang = test_case.get("expected_lang")
        
        if detected_lang != expected_lang:
            result["errors"].append(
                f"Language mismatch: got '{detected_lang}', expected '{expected_lang}'"
            )
        else:
            print(f"✅ Language: {detected_lang}")
        
        # Validate intent
        detected_intent = data.get("intent")
        expected_intent = test_case.get("expected_intent")
        
        if detected_intent != expected_intent:
            result["errors"].append(
                f"Intent mismatch: got '{detected_intent}', expected '{expected_intent}'"
            )
        else:
            print(f"✅ Intent: {detected_intent}")
        
        # Check structured data has required fields
        structured = data.get("structured", {})
        should_have = test_case.get("should_have", [])
        
        for field in should_have:
            if field not in structured or not structured[field]:
                result["errors"].append(f"Missing or empty '{field}' in structured data")
            else:
                if isinstance(structured[field], list):
                    print(f"✅ Found {len(structured[field])} {field}")
                else:
                    print(f"✅ Found {field}")
        
        # Check answer is not empty
        answer = data.get("answer", "")
        if not answer or len(answer) < 10:
            result["errors"].append("Answer is empty or too short")
        else:
            print(f"✅ Answer: {answer[:80]}...")
        
        # Check response time
        print(f"✅ Response time: {elapsed:.2f}s")
        
        if elapsed > 35:
            result["errors"].append(f"Response too slow: {elapsed:.2f}s (target: <30s)")
        
        # Mark as passed if no errors
        if not result["errors"]:
            result["passed"] = True
            print(f"\n✅ PASSED")
        else:
            print(f"\n❌ FAILED:")
            for err in result["errors"]:
                print(f"   - {err}")
        
        # Print full structured data for debugging
        if "--verbose" in sys.argv:
            print(f"\nFull response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        
    except requests.exceptions.Timeout:
        result["errors"].append("Request timed out (>60s)")
        print(f"❌ Timeout")
    
    except Exception as e:
        result["errors"].append(str(e))
        print(f"❌ Error: {e}")
    
    return result

def print_summary(results: List[Dict]):
    """Print test summary"""
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for r in results if r["passed"])
    total = len(results)
    
    print(f"\nResults: {passed}/{total} passed ({passed/total*100:.1f}%)")
    
    # Time statistics
    times = [r["time"] for r in results if r["time"] > 0]
    if times:
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        
        print(f"\nResponse Times:")
        print(f"  Average: {avg_time:.2f}s")
        print(f"  Min: {min_time:.2f}s")
        print(f"  Max: {max_time:.2f}s")
        
        if avg_time > 30:
            print(f"  ⚠️  Average time exceeds 30s target")
    
    # Failed tests
    failed = [r for r in results if not r["passed"]]
    if failed:
        print(f"\nFailed Tests:")
        for r in failed:
            print(f"  ❌ {r['name']}")
            for err in r["errors"]:
                print(f"     - {err}")
    
    print("\n" + "="*60)
    
    # Exit code
    sys.exit(0 if passed == total else 1)

def main():
    """Run all tests"""
    print("HerboAI Multilingual Chat - Migration Test")
    print("="*60)
    
    # Check backend health first
    if not test_health_endpoint():
        print("\n❌ Backend is not running. Start it with: python app.py")
        sys.exit(1)
    
    # Run all test cases
    results = []
    for test_case in TEST_CASES:
        result = test_query(test_case)
        results.append(result)
        time.sleep(1)  # Brief pause between tests
    
    # Print summary
    print_summary(results)

if __name__ == "__main__":
    main()