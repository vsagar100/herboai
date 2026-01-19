"""
Debug Hindi vs Marathi handling
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app
from services.chat import handle_chat

app = create_app()

def test_languages():
    """Test Hindi and Marathi to see where they differ"""
    
    with app.app_context():
        tests = [
            ("hi", "मधुमेह के लिए मुझे क्या लेना चाहिए?"),
            ("mr", "मधुमेह साठी मला काय घ्यावं?"),
        ]
        
        for lang, query in tests:
            print(f"\n{'='*60}")
            print(f"Testing {lang.upper()}: {query}")
            print(f"{'='*60}")
            
            response = handle_chat(
                user_text=query,
                session_id=f"test_{lang}",
                lang=lang
            )
            
            structured = response.get('structured', {})
            preps = structured.get('preparations', [])
            
            print(f"Condition: {structured.get('condition')}")
            print(f"Preparations: {len(preps)}")
            print(f"Answer length: {len(response.get('answer', ''))}")
            print(f"Followups: {len(response.get('followups', []))}")

if __name__ == "__main__":
    test_languages()
