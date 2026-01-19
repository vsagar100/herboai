"""
Check if Hindi issue is in handle_chat or API layer
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app
from services.chat import handle_chat

app = create_app()

with app.app_context():
    # Test Hindi directly
    query_hi = "मधुमेह के लिए मुझे क्या लेना चाहिए?"
    
    print(f"Query: {query_hi}")
    print(f"{'='*60}")
    
    response = handle_chat(
        user_text=query_hi,
        session_id="test_hi",
        lang="hi"
    )
    
    print(f"handle_chat() returned:")
    print(f"  Answer length: {len(response.get('answer', ''))}")
    print(f"  Severity: {response.get('severity')}")
    print(f"  Followups: {len(response.get('followups', []))}")
    print(f"  Provisional count: {len(response.get('provisional', []))}")
    
    structured = response.get('structured', {})
    print(f"\n  Structured keys: {list(structured.keys())}")
    print(f"  Structured.condition: {structured.get('condition')}")
    print(f"  Structured.preparations count: {len(structured.get('preparations', []))}")
    
    # Now trace through API transformation
    print(f"\n{'='*60}")
    print(f"API Transformation Logic:")
    print(f"{'='*60}")
    
    structured = response.get("structured", {})
    print(f"1. Got structured from result: {list(structured.keys())}")
    print(f"2. Check: 'disease' in structured? {('disease' in structured)}")
    print(f"3. Check: 'condition' in structured? {('condition' in structured)}")
    print(f"4. Check: 'preparations' in structured? {('preparations' in structured)}")
    
    if "disease" in structured:
        print("5. -> Would take DISEASE branch")
    elif "condition" in structured and "preparations" in structured:
        print("5. -> Would take CONDITION+PREP branch")
        api_structured = {
            "condition": structured["condition"],
            "plants": structured.get("plants", [])[:5],
            "preparations": structured.get("preparations", [])[:6]
        }
        print(f"6. Would return preparations: {len(api_structured['preparations'])}")
    elif "plant" in structured:
        print("5. -> Would take PLANT branch")
    else:
        print("5. -> Would take DEFAULT branch")
