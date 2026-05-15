"""Test NLU parsing for 'Neem for acne' query"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.nlu_optimized import parse_query

# Test the NLU parsing
result = parse_query("Neem for acne", "en")

print("\n=== NLU PARSING: 'Neem for acne' ===\n")
print(f"Intent: {result['intent']}")
print(f"Disease terms: {result['disease_terms']}")
print(f"Plant terms: {result['plant_terms']}")
print(f"Preparation terms: {result['preparation_terms']}")
print(f"Severity: {result.get('severity')}")
print(f"\nRaw result:")
for key, value in result.items():
    if value:
        print(f"  {key}: {value}")
