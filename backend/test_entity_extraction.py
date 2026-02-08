"""Test disease entity extraction for 'Neem for acne'"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app
from api.nlu_optimized import classify_intent, extract_entities, search_diseases_fuzzy

# Initialize Flask app
app = create_app()

with app.app_context():
    query = "Neem for acne"

    print("\n=== TESTING NLU for 'Neem for acne' ===\n")

    # Step 1: Intent classification
    intent = classify_intent(query)
    print(f"1. Intent: {intent}")

    # Step 2: Entity extraction 
    plants, diseases = extract_entities(query, text_en=query, prefer_en=True)
    print(f"\n2. Plants extracted: {len(plants)}")
    for p in plants:
        print(f"   - {p.get('name_en', 'N/A')} (ID={p.get('id', 'N/A')})")

    print(f"\n3. Diseases extracted: {len(diseases)}")
    for d in diseases:
        print(f"   - {d.get('name_en', 'N/A')} (ID={d.get('id', 'N/A')})")

    # Step 3: Direct disease search
    print("\n4. Direct disease search for 'acne':")
    acne_results = search_diseases_fuzzy("acne", limit=5)
    print(f"   Found {len(acne_results)} results:")
    for d in acne_results:
        print(f"   - {d.get('name_en', 'N/A')} (ID={d.get('id', 'N/A')})")
