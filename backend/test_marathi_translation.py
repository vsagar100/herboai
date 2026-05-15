#!/usr/bin/env python3
"""
Test translation fallback and condition classification with Marathi.
"""
import sys
import os
import logging

logging.basicConfig(level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s")

from services.indic_translation_service import translate_to_en
from api.nlu_optimized import classify_intent

test_queries = [
    ("मधुमेह साठी काय घ्यावं?", "mr"),
    ("मराठी वैद्य", "mr"),
    ("घाव भरण्यासाठी काय वापरावे", "mr"),
]

print("=" * 70)
print("Testing Marathi Translation and Intent Classification")
print("=" * 70)

for marathi_text, lang in test_queries:
    print(f"\nQuery: {marathi_text}")
    print(f"Language: {lang}")
    
    # Test translation
    try:
        translated = translate_to_en(marathi_text, lang_hint=lang)
        print(f"Translated: {translated}")
        if translated == marathi_text:
            print("  ⚠️  FALLBACK: Original text returned (translation likely failed)")
    except Exception as e:
        print(f"  ❌ Translation error: {e}")
        translated = marathi_text
    
    # Test intent classification with translated text
    try:
        intent = classify_intent(translated)
        print(f"Intent (from translated): {intent}")
    except Exception as e:
        print(f"  ❌ Intent classification error: {e}")
    
    # Also test intent classification with original Marathi (for fallback scenario)
    try:
        intent_native = classify_intent(marathi_text)
        print(f"Intent (from native Marathi): {intent_native}")
    except Exception as e:
        print(f"  ❌ Intent classification (native) error: {e}")

print("\n" + "=" * 70)
