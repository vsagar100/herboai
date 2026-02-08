"""Test intelligent slot filling conversation"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from init import create_app

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("TESTING INTELLIGENT QUESTIONNAIRE FLOW")
    print("="*70)
    
    with app.test_client() as client:
        # Turn 1: Initial query
        print("\n\n📌 TURN 1: Initial Query")
        print("-" * 70)
        print("User: 'I have diabetes. What helps?'")
        
        response = client.post(
            "/api/query",
            json={"text": "I have diabetes. What helps?", "lang": "en"},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.get_json()
            session_id = data.get('session_id')
            answer = data.get('answer', '')
            followups = data.get('followups', [])
            
            print(f"\nSession ID: {session_id}")
            print(f"\n✅ Got remedy: {'Yes' if len(answer) > 200 else 'No'}")
            print(f"✅ Asked {len(followups)} questions:")
            for i, q in enumerate(followups, 1):
                print(f"   {i}. {q}")
            
            print(f"\nResponse preview (first 400 chars):")
            print(answer[:400])
        
        # Turn 2: Answer ONE question (duration)
        print("\n\n📌 TURN 2: Answer Duration Question")
        print("-" * 70)
        print("User: '2 months'")
        
        response = client.post(
            "/api/query",
            json={"text": "2 months", "lang": "en", "session_id": session_id},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.get_json()
            answer = data.get('answer', '')
            followups = data.get('followups', [])
            
            # Check if "Duration" is acknowledged
            has_acknowledgment = "Noted" in answer and "Duration" in answer
            
            # Check if duration question is removed
            duration_still_asked = any("Since when" in q or "days/months" in q for q in followups)
            
            print(f"\n✅ Acknowledged answer: {'Yes' if has_acknowledgment else 'No'}")
            print(f"✅ Removed duration question: {'Yes' if not duration_still_asked else 'No ❌ BUG!'}")
            print(f"✅ Remaining questions: {len(followups)}")
            for i, q in enumerate(followups, 1):
                print(f"   {i}. {q}")
            
            print(f"\nResponse preview (first 500 chars):")
            print(answer[:500])
        
        # Turn 3: Answer another question (age/gender)
        print("\n\n📌 TURN 3: Answer Age/Gender Question")
        print("-" * 70)
        print("User: '35 female'")
        
        response = client.post(
            "/api/query",
            json={"text": "35 female", "lang": "en", "session_id": session_id},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.get_json()
            answer = data.get('answer', '')
            followups = data.get('followups', [])
            
            # Check if age/gender is acknowledged
            has_acknowledgment = "Age/Gender" in answer or "35 years" in answer
            
            # Check if age/gender question is removed
            age_still_asked = any("Age and gender" in q for q in followups)
            
            print(f"\n✅ Acknowledged answer: {'Yes' if has_acknowledgment else 'No'}")
            print(f"✅ Removed age/gender question: {'Yes' if not age_still_asked else 'No ❌ BUG!'}")
            print(f"✅ Remaining questions: {len(followups)}")
            for i, q in enumerate(followups, 1):
                print(f"   {i}. {q}")
            
            print(f"\nResponse preview (first 500 chars):")
            print(answer[:500])
    
    print("\n" + "="*70)
    print("TESTING COMPLETE")
    print("="*70)
    print("\n✅ Expected behavior:")
    print("  - Each turn should acknowledge the answered question")
    print("  - Each turn should REMOVE the answered question from followups")
    print("  - Only REMAINING questions should be shown")
    print("  - Remedies should be shown in ALL turns (never blocked)")
