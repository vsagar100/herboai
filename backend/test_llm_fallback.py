"""Test intelligent LLM fallback for queries without DB mappings"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set UTF-8 encoding for console output
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from init import create_app

# Initialize Flask app
app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("TESTING INTELLIGENT LLM FALLBACK MECHANISM")
    print("="*70)
    
    # Test 1: Query with DB mapping (should return DB data)
    print("\n\n📌 TEST 1: Query WITH database mapping")
    print("-" * 70)
    print("Query: 'Neem for acne'")
    print("Expected: DB preparation (Neem Leaf Decoction)")
    print("-" * 70)
    
    with app.test_client() as client:
        response = client.post(
            "/api/query",
            json={"text": "Neem for acne", "lang": "en"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.get_json()
            answer = data.get('answer', '')
            
            # Check if it's from DB or LLM
            if 'AI-generated' in answer or 'AI द्वारा' in answer:
                print("❌ UNEXPECTED: Got LLM-generated content (should be from DB)")
            else:
                print("✅ CORRECT: Got DB preparation")
            
            print("\nResponse preview (first 500 chars):")
            print(answer[:500] + "..." if len(answer) > 500 else answer)
        else:
            print(f"❌ Error: {response.status_code}")
    
    # Test 2: Query without DB mapping (should use LLM fallback)
    print("\n\n📌 TEST 2: Query WITHOUT database mapping")
    print("-" * 70)
    print("Query: 'Ashwagandha for anxiety'")
    print("Expected: LLM-generated remedy (if no DB mapping exists)")
    print("-" * 70)
    
    with app.test_client() as client:
        response = client.post(
            "/api/query",
            json={"text": "Ashwagandha for anxiety", "lang": "en"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.get_json()
            answer = data.get('answer', '')
            
            # Check source
            if 'AI-generated' in answer or 'AI द्वारा' in answer:
                print("✅ CORRECT: Got LLM-generated content (fallback working)")
            elif answer and len(answer) > 50:
                print("✅ CORRECT: Got DB preparation (mapping exists)")
            else:
                print("⚠️ WARNING: Empty or minimal response")
            
            print("\nResponse preview (first 500 chars):")
            print(answer[:500] + "..." if len(answer) > 500 else answer)
        else:
            print(f"❌ Error: {response.status_code}")
    
    # Test 3: General plant query without disease
    print("\n\n📌 TEST 3: General plant query (no specific disease)")
    print("-" * 70)
    print("Query: 'Uses of Tulsi'")
    print("Expected: Plant information or general preparations")
    print("-" * 70)
    
    with app.test_client() as client:
        response = client.post(
            "/api/query",
            json={"text": "Uses of Tulsi", "lang": "en"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.get_json()
            answer = data.get('answer', '')
            
            if answer and len(answer) > 100:
                print("✅ CORRECT: Got meaningful response")
            else:
                print("⚠️ WARNING: Response too short")
            
            print("\nResponse preview (first 500 chars):")
            print(answer[:500] + "..." if len(answer) > 500 else answer)
        else:
            print(f"❌ Error: {response.status_code}")
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70)
