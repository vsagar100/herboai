#!/usr/bin/env python3
"""
Test the full query pipeline with Marathi.
"""
import sys
import os
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

# Add backend to path
sys.path.insert(0, str(os.path.dirname(os.path.abspath(__file__))))

from services.chat import handle_chat
from api.context import get_last_context
import uuid

test_query = "मधुमेह साठी काय घ्यावं?"  # "What to take for diabetes?"
session_id = str(uuid.uuid4())

print("=" * 80)
print(f"Testing Full Query Pipeline with Marathi")
print("=" * 80)
print(f"Query: {test_query}")
print(f"Session ID: {session_id}")
print()

try:
    result = handle_chat(test_query, lang="mr", session_id=session_id)
    
    print("RESULT:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if "error" in result:
        print(f"\n❌ ERROR: {result['error']}")
    elif "structured" in result:
        prep_count = len(result.get("structured", {}).get("preparations", []))
        print(f"\n✅ SUCCESS: Got {prep_count} preparations")
    else:
        print("\n⚠️  Unexpected response structure")
        
except Exception as e:
    print(f"❌ EXCEPTION: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)
