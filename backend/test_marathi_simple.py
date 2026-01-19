"""
Simple test of Marathi query end-to-end
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app
from services.chat import handle_chat

app = create_app()

def test_marathi():
    with app.app_context():
        marathi_query = "मधुमेह साठी काय घ्यावं?"
        print(f"\nQuery: {marathi_query}")
        print(f"{'='*80}\n")
        
        response = handle_chat(
            user_text=marathi_query,
            session_id="test_123",
            lang="mr"
        )
        
        print(f"Answer length: {len(response.get('answer', ''))} chars")
        print(f"Intent: {response.get('intent')}")
        print(f"Language: {response.get('detected_language')}")
        print(f"\n{'='*80}")
        print(f"ANSWER:\n{response.get('answer', 'ERROR - NO ANSWER')}")
        print(f"\n{'='*80}")
        
        # Check structured data
        struct = response.get('structured', {})
        print(f"\nStructured data:")
        if 'disease' in struct:
            print(f"  Disease: {struct['disease'].get('name')}")
        if 'preparations' in struct:
            print(f"  Preparations found: {len(struct['preparations'])}")
            for prep in struct['preparations'][:3]:
                print(f"    - {prep.get('name')}")

if __name__ == "__main__":
    test_marathi()
