"""Show full answer text for the key queries."""
import requests, json

BASE = "http://127.0.0.1:5000/api/query"

tests = [
    "गुडमारचा काढा कसा बनवायचा?",
    "हळदीचे दूध बनवण्याची पद्धत",
]

for text in tests:
    print(f"\n{'='*70}")
    print(f"Query: {text}")
    print(f"{'='*70}")
    r = requests.post(BASE, json={"text": text}, timeout=120)
    data = r.json()
    print(f"Language: {data.get('detected_language')}")
    print(f"\nFULL ANSWER:\n{data.get('answer', '')}")
