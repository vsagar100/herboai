"""Final validation: Marathi + English queries"""
import requests, json

def test(text, lang=None):
    payload = {"text": text}
    if lang:
        payload["lang"] = lang
    r = requests.post("http://127.0.0.1:5000/api/query", json=payload, timeout=90)
    data = r.json()
    ans = data.get("answer", "")[:200]
    d = data.get("structured", {}).get("disease", {})
    p = data.get("structured", {}).get("plants", [])
    preps = data.get("structured", {}).get("preparations", [])
    lang_det = data.get("detected_language", "?")
    disease_name = d.get("name_en", "N/A")
    disease_id = d.get("id", "?")
    plant_names = [pl.get("common_name_en") for pl in p[:3]]
    print(f"  Status: {r.status_code} | Lang: {lang_det}")
    print(f"  Disease: {disease_name} (id={disease_id})")
    print(f"  Plants: {plant_names}")
    print(f"  Preps: {len(preps)}")
    print(f"  Answer: {ans}...")
    print()

print("=== Test 1: Marathi - मुरुमांसाठी निंब ===")
test("\u092E\u0941\u0930\u0941\u092E\u093E\u0902\u0938\u093E\u0920\u0940 \u0928\u093F\u0902\u092C", "mr")

print("=== Test 2: English - Neem for acne ===")
test("Neem for acne")
