"""Test API endpoints for preparation query fixes."""
import requests
import json
import sys

BASE = "http://127.0.0.1:5000/api/query"

tests = [
    # Fixed prep queries (were broken)
    ("गुडमारचा काढा कसा बनवायचा?", "Gudmar prep (was Bamboo)"),
    ("हळदीचे दूध बनवण्याची पद्धत", "Turmeric milk (was Kovidara_Vine)"),
    ("अश्वगंधाबद्दल सांगा", "Ashwagandha info (was working)"),
    # Regression tests
    ("मुरुमांसाठी निंब", "Neem for pimples (Marathi)"),
    ("I have diabetes. What helps?", "Diabetes English"),
    ("neem for acne", "Neem for acne English"),

    # Prep resolution regressions (reported in screenshots)
    ("Neem oil usage for skin", "Neem oil topical usage (must NOT become Kalmegh)"),
    ("Triphala powder dosage", "Triphala dosage (must NOT become Haritaki)"),
]

def _contains_any(hay: str, needles: list[str]) -> bool:
    h = (hay or "").lower()
    return any(n.lower() in h for n in needles)

def _plant_names(structured: dict) -> list[str]:
    plants = structured.get("plants") or []
    out = []
    for p in plants:
        if isinstance(p, dict):
            out.append(p.get("common_name_en") or p.get("name") or p.get("botanical_name") or "")
    return [x for x in out if x]

failed = 0

for text, label in tests:
    print(f"\n{'='*70}")
    print(f"TEST: {label}")
    print(f"Query: {text}")
    print(f"{'='*70}")
    try:
        r = requests.post(BASE, json={"text": text}, timeout=120)
        data = r.json()
        print(f"Intent: {data.get('intent')}")
        print(f"Language: {data.get('detected_language')}")
        
        structured = data.get("structured", {})
        plants = structured.get("plants", [])
        preps = structured.get("preparations", [])
        condition = structured.get("condition", "")
        
        if plants:
            print(f"Plants: {[p.get('name') or p.get('common_name') for p in plants]}")
        if preps:
            print(f"Preparations ({len(preps)}):")
            for p in preps[:3]:
                print(f"  - {p.get('name', p.get('name_en', '?'))}")
        if condition:
            print(f"Condition: {condition}")
        
        answer = data.get("answer", "")
        # Print first 300 chars of answer
        print(f"Answer preview: {answer[:300]}...")

        # Minimal assertions for the two regressions
        plants_in_struct = _plant_names(structured)

        if text.lower().startswith("neem oil"):
            if _contains_any(answer, ["kalmegh", "andrographis"]):
                print("ASSERT FAIL: Neem oil query returned Kalmegh")
                failed += 1
            if not _contains_any(answer, ["neem", "azadirachta"]) and not _contains_any(" ".join(plants_in_struct), ["neem"]):
                print("ASSERT FAIL: Neem oil query did not mention Neem")
                failed += 1

        if text.lower().startswith("triphala powder"):
            has_triphala = _contains_any(answer, ["triphala"]) or _contains_any(" ".join(plants_in_struct), ["triphala"])
            has_haritaki = _contains_any(answer, ["haritaki", "terminalia chebula"]) or _contains_any(" ".join(plants_in_struct), ["haritaki"])

            # Haritaki is a legitimate ingredient of Triphala; it's only a failure if
            # the answer/structured output is missing Triphala and instead focuses on Haritaki.
            if has_haritaki and not has_triphala:
                print("ASSERT FAIL: Triphala query appears to have collapsed to Haritaki")
                failed += 1
            if not has_triphala:
                print("ASSERT FAIL: Triphala query did not mention Triphala")
                failed += 1
    except Exception as e:
        print(f"ERROR: {e}")
        failed += 1

print(f"\n{'='*70}")
print("ALL TESTS COMPLETE")

if failed:
    print(f"\nFAILED: {failed} checks")
    sys.exit(1)
print("\nPASSED")
