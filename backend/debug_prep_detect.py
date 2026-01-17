#!/usr/bin/env python
"""Debug Turmeric milk preparation query."""

from services.chat import is_preparation_like_query, _simple_tokens
import re

text = "Turmeric milk preparation"
text_en = text.lower()

print("=== TESTING PREPARATION DETECTION ===\n")
print(f"Original text: '{text}'")
print(f"is_preparation_like_query: {is_preparation_like_query(text, text_en)}")

# Test keyword matching
prep_keywords_en = [
    "how to make", "how to prepare", "recipe", "method", "steps",
    "preparation", "prepare",
    "kadha", "kada", "kadhha",
    "kwath", "kwatha",
    "decoction", "kashaya", "kashayam",
    "churna", "powder", "tablet", "vati",
    "taila", "oil", "ghrita", "ghee",
    "lehyam", "avaleha", "arishta", "asava", "syrup",
]

combined = text.lower()
for kw in prep_keywords_en:
    if kw in combined:
        print(f"\n✓ Found keyword: '{kw}'")

# Test plant term extraction
print("\n=== TESTING PLANT TERM EXTRACTION ===\n")

# Simulate _extract_plant_term logic
toks = text.lower().split()
print(f"Tokens: {toks}")
print(f"Last token would be: '{toks[-1]}' (milk)")

# Look for plant names
prep_names = ["turmeric", "tulsi", "neem", "brahmi", "ashwagandha"]
for name in prep_names:
    if name in combined:
        print(f"✓ Found plant hint: '{name}'")
