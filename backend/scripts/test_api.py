#!/usr/bin/env python3
"""
Enhanced test script for AYUSH Herbs AI API
"""

import requests
import json
import time
from typing import Dict, Any

API_BASE = "http://localhost:8000"

def test_endpoint(endpoint: str, method: str = "GET", data: Dict[Any, Any] = None) -> Dict[Any, Any]:
    """Test an API endpoint and return response"""
    url = f"{API_BASE}{endpoint}"
    
    try:
        if method == "POST":
            response = requests.post(url, json=data)
        else:
            response = requests.get(url)
        
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}

def main():
    print("🌿 AYUSH Herbs AI - API Test Suite")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing Health Endpoint...")
    result = test_endpoint("/health")
    if result["success"]:
        print("✅ Health check passed")
    else:
        print(f"❌ Health check failed: {result['error']}")
        return
    
    # Test 2: List herbs
    print("\n2. Testing Herbs List...")
    result = test_endpoint("/herbs?limit=5")
    if result["success"]:
        herbs = result["data"]
        print(f"✅ Retrieved {len(herbs)} herbs")
        if herbs:
            print(f"   Sample herb: {herbs[0]['name']}")
    else:
        print(f"❌ Failed to get herbs: {result['error']}")
    
    # Test 3: Search functionality  
    print("\n3. Testing Semantic Search...")
    test_queries = [
        "fever treatment",
        "digestive problems", 
        "skin diseases",
        "बुखार का इलाज",  # Fever treatment in Hindi
        "पाचन संबंधी समस्या"  # Digestive problems in Hindi
    ]
    
    for query in test_queries:
        result = test_endpoint(f"/search?q={query}&k=3")
        if result["success"]:
            matches = result["data"]["matches"]
            print(f"✅ Query: '{query}' → {len(matches)} matches")
        else:
            print(f"❌ Search failed for '{query}': {result['error']}")
    
    # Test 4: Question answering
    print("\n4. Testing Question Answering...")
    test_questions = [
        {
            "question": "What herbs are good for fever?",
            "lang": "en"
        },
        {
            "question": "How to treat digestive problems naturally?",
            "lang": "en"
        },
        {
            "question": "बुखार के लिए कौन सी जड़ी बूटी अच्छी है?",
            "lang": "hi"
        },
        {
            "question": "पेट की समस्या के लिए घरेलू उपाय क्या हैं?",
            "lang": "hi"
        }
    ]
    
    for i, test_case in enumerate(test_questions, 1):
        print(f"\n   Test {i}: {test_case['question'][:50]}...")
        
        start_time = time.time()
        result = test_endpoint("/query", "POST", test_case)
        response_time = time.time() - start_time
        
        if result["success"]:
            answer_data = result["data"]
            answer = answer_data["answer"]
            detected_lang = answer_data["lang"]
            sources = answer_data.get("sources", [])
            
            print(f"   ✅ Response time: {response_time:.2f}s")
            print(f"   📍 Detected language: {detected_lang}")
            print(f"   📚 Sources used: {len(sources)} herbs")
            print(f"   💬 Answer preview: {answer[:100]}{'...' if len(answer) > 100 else ''}")
            
            # Check for quality indicators
            if len(answer) < 20:
                print("   ⚠️  Warning: Very short response")
            if "use the use" in answer.lower() or answer.count("you are") > 2:
                print("   ⚠️  Warning: Possible repetition or prompt leakage")
            if not sources:
                print("   ⚠️  Warning: No source herbs referenced")
                
        else:
            print(f"   ❌ Query failed: {result['error']}")
    
    # Test 5: System performance
    print("\n5. Performance Test...")
    performance_queries = [
        {"question": "What is turmeric good for?", "lang": "en"},
        {"question": "Benefits of neem", "lang": "en"},
        {"question": "हल्दी के फायदे क्या हैं?", "lang": "hi"}
    ]
    
    total_time = 0
    successful_queries = 0
    
    for query in performance_queries:
        start_time = time.time()
        result = test_endpoint("/query", "POST", query)
        response_time = time.time() - start_time
        
        if result["success"]:
            successful_queries += 1
            total_time += response_time
    
    if successful_queries > 0:
        avg_time = total_time / successful_queries
        print(f"✅ Average response time: {avg_time:.2f}s")
        if avg_time < 5:
            print("   🚀 Good performance")
        elif avg_time < 10:
            print("   ⏱️  Moderate performance")
        else:
            print("   🐌 Slow performance - consider model optimization")
    
    print("\n" + "=" * 50)
    print("🔍 Test Summary Complete")
    
    # Recommendations
    print("\n📋 Recommendations:")
    print("1. If responses are garbled, try downloading a better model")
    print("2. For faster responses, use the lightweight model option") 
    print("3. Check logs for any error patterns")
    print("4. Ensure sufficient RAM for the selected model")

if __name__ == "__main__":
    main()