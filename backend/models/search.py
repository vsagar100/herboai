from models.translation import translate_to_english, translate_from_english
import json, os
from database.db import HerbalDataFetcher

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../database')
DATA_FILE = os.path.join(db_path, "data.json")

fetcher = HerbalDataFetcher('herboai.db')
HERB_DATA = fetcher.fetch_all_herbs()

#with open(DATA_FILE, "r", encoding="utf-8") as f:
#    HERB_DATA = json.load(f)

def search_by_symptom(query, lang="en"):
    query_en = translate_to_english(query) if lang != "en" else query
    results = []

    for herb in HERB_DATA:
        if any(q.lower() in cond.lower() for cond in herb["conditions"] for q in query_en.split()):
            results.append(herb)
        elif any(q.lower() in alias.lower() for alias in herb["aliases"] for q in query_en.split()):
            results.append(herb)

    if lang != "en":
        for r in results:
            r["name"] = translate_from_english(r["name"], lang)
            r["remedy"] = translate_from_english(r["remedy"], lang)
            r["conditions"] = [translate_from_english(c, lang) for c in r["conditions"]]

    return results
