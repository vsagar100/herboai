"""
Debug test for Marathi query: मधुमेह साठी काय घ्यावं?
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app
from services.chat import handle_chat

app = create_app()

def test_marathi_query():
    """Test the exact failing query"""
    with app.app_context():
        # The failing query
        marathi_query = "मधुमेह साठी काय घ्यावं?"
        print(f"\n{'='*80}")
        print(f"Testing Marathi Query: {marathi_query}")
        print(f"{'='*80}")
        
        # Test 1: Call handle_chat with language parameter (this is the actual function)
        try:
            response = handle_chat(
                user_text=marathi_query,
                session_id="test_session_123",
                lang="mr"
            )
            print(f"\n✅ Response received (length: {len(str(response))} chars)")
            print(f"\nResponse structure:")
            if isinstance(response, dict):
                for key in response.keys():
                    val = response[key]
                    if isinstance(val, str):
                        print(f"  {key}: {val[:100]}..." if len(str(val)) > 100 else f"  {key}: {val}")
                    elif isinstance(val, list):
                        print(f"  {key}: [{len(val)} items]")
                    else:
                        print(f"  {key}: {val}")
            else:
                print(f"Response: {response}")
                
        except Exception as e:
            print(f"❌ Error in handle_chat: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            
        # Test 2: Test condition classification directly
        print(f"\n{'='*60}")
        print("Testing condition classification:")
        print(f"{'='*60}")
        from services.chat import _classify_condition
        
        condition = _classify_condition(marathi_query)
        print(f"Condition detected: '{condition}'")
        
        # Test 3: Test language detection
        print(f"\n{'='*60}")
        print("Testing language detection:")
        print(f"{'='*60}")
        from services.chat import detect_language
        
        detected_lang = detect_language(marathi_query)
        print(f"Language detected: '{detected_lang}'")
        
        # Test 4: Test translation if needed
        print(f"\n{'='*60}")
        print("Testing translation:")
        print(f"{'='*60}")
        if detected_lang != "en":
            from services.chat import translate_to_en
            translated = translate_to_en(marathi_query, detected_lang)
            print(f"Translated to English: '{translated}'")
            
            # Re-classify with translated text
            condition_after = _classify_condition(translated)
            print(f"Condition after translation: '{condition_after}'")

if __name__ == "__main__":
    test_marathi_query()
