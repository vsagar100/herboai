#!/usr/bin/env python3
"""Quick test: Marathi query pipeline for मुरुमांसाठी निंब"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from init import create_app
app = create_app()

with app.app_context():
    from services.chat import handle_chat

    query = "\u092E\u0941\u0930\u0941\u092E\u093E\u0902\u0938\u093E\u0920\u0940 \u0928\u093F\u0902\u092C"
    print(f"\n{'='*60}")
    print(f"QUERY: {query}")
    print(f"{'='*60}\n")

    try:
        result = handle_chat(query, session_id="test_marathi_001", lang="mr")

        print(f"ANSWER:\n{result.get('answer', 'NO ANSWER')}\n")
        print(f"SEVERITY: {result.get('severity')}")
        print(f"FOLLOWUPS: {result.get('followups', [])}")

        structured = result.get("structured", {})
        if structured:
            disease = structured.get("disease", {})
            plant = structured.get("plant", {})
            preps = structured.get("preparations", [])
            print(f"\nDISEASE: {disease.get('name_en', 'N/A')} (id={disease.get('id', 'N/A')})")
            print(f"PLANT: {plant.get('common_name_en', 'N/A')} (id={plant.get('id', 'N/A')})")
            print(f"PREPARATIONS ({len(preps)}):")
            for p in preps[:3]:
                print(f"  - {p.get('name_en', '?')}: {(p.get('preparation_steps','') or '')[:100]}")

        print(f"\nFULL RESULT KEYS: {list(result.keys())}")

    except Exception as e:
        import traceback
        print(f"ERROR: {e}")
        traceback.print_exc()

    # Show full English response
    print(f"\n[FULL RESPONSE] English (I have a cold):")
    print("-" * 80)
    print(result_en['answer'])

    # Show full Marathi response
    print(f"\n[FULL RESPONSE] Marathi (मला सर्दी आहे):")
    print("-" * 80)
    print(result_mr['answer'])
