# api/nlu.py
import re
from typing import Dict, List, Tuple
from db import get_db

DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

HI_MR_TO_EN = {
    "मधुमेह": "diabetes", "मधु मेह": "diabetes", "शुगर": "blood sugar",
    "खोकला": "cough", "सर्दी": "cold", "जुलाब": "diarrhea", "कब्ज": "constipation",
    "गॅस": "indigestion", "निद्रानाश": "insomnia", "त्वचा": "skin",
    "बीपी": "bp", "রक्तदाब": "hypertension", "दाब": "hypertension",
    "गुळवेल": "guduchi", "गिलोय": "guduchi", "नीम": "neem", "तुळस": "tulsi",
}
EN_TO_HI = {"diabetes": "मधुमेह", "guduchi": "गुडूची", "neem": "नीम", "tulsi": "तुलसी"}
MR_MARKERS = {"बद्दल", "माहिती", "तुळस", "गुळवेल", "औषधी", "काढा"}

def detect_language(text: str) -> str:
    t = text or ""
    if DEVANAGARI_RE.search(t):
        mr_markers = {"आलं", "हिरडा", "काढा", "औषधी", "आवळा", "तुळस", "दुखी", "बद्दल", "माहिती", "गुळवेल"}
        return "mr" if any(tok in t for tok in mr_markers) else "hi"
    return "en"


INTENTS = ("remedy_lookup", "plant_info", "preparation_info", "lifestyle_advice", "none")

def classify_intent(text_en_or_src: str) -> str:
    t = (text_en_or_src or "").lower()
    complaint = ["i have ", "i am having ", "i suffer from ", "i am suffering from ",
                 "remedy for", "treatment for", "herbs for", "help with ",
                 "my blood sugar", "my bp", "my pressure"]
    disease = ["diabetes", "for diabetes", "blood sugar", "cough", "cold", "arthritis", "joint",
               "bp", "hypertension", "gastric", "indigestion", "constipation", "sleep", "insomnia", "skin"]
    prep = ["how to prepare", "kwatha", "decoction", "churna", "powder", "oil", "ghrita", "taila"]
    plant = ["what is", "about", "uses of", "benefits of"]

    if any(k in t for k in prep): return "preparation_info"
    if any(k in t for k in complaint) or any(k in t for k in disease): return "remedy_lookup"
    if any(k in t for k in plant): return "plant_info"
    if "preparation" in t or "dosage" in t or "how to make" in t or "kashaya" in t or "decoction" in t:
        return "preparation_info"
    return "none"

def search_plants_by_text(q: str, limit=5) -> List[Dict]:
    db = get_db(); cur = db.cursor()
    cur.execute("""
        SELECT p.*, ps.synonym
        FROM plant_synonyms ps
        JOIN plants p ON p.id = ps.plant_id
        WHERE ps.synonym LIKE ?
        LIMIT ?
    """, (f"%{q}%", limit))
    rows = cur.fetchall()
    if not rows:
        cur.execute("""
            WITH hits AS (
              SELECT rowid AS id FROM plants_fts
              WHERE plants_fts MATCH ? LIMIT ?
            )
            SELECT p.* FROM hits h JOIN plants p ON p.id=h.id
        """, (q, limit))
        rows = cur.fetchall()
    cur.close()
    return [dict(r) for r in rows]

def search_diseases_by_text(q: str, limit=5) -> List[Dict]:
    db = get_db(); cur = db.cursor()
    cur.execute("""
        SELECT d.*, ds.synonym
        FROM disease_synonyms ds
        JOIN diseases d ON d.id = ds.disease_id
        WHERE ds.synonym LIKE ?
        LIMIT ?
    """, (f"%{q}%", limit))
    rows = cur.fetchall()
    if not rows:
        cur.execute("""
            WITH hits AS (
              SELECT rowid AS id FROM diseases_fts
              WHERE diseases_fts MATCH ? LIMIT ?
            )
            SELECT d.* FROM hits h JOIN diseases d ON d.id=h.id
        """, (q, limit))
        rows = cur.fetchall()
    cur.close()
    return [dict(r) for r in rows]

def extract_entities(text: str, text_en: str | None = None, prefer_en: bool = False) -> Tuple[List[Dict], List[Dict]]:
    q = (text_en if prefer_en and text_en else text) or ""
    tokens = re.findall(r"[A-Za-z\u0900-\u097F]+", q)
    plants, diseases = [], []
    for tok in sorted(set(tokens), key=len, reverse=True):
        if len(plants) < 3:
            ps = search_plants_by_text(tok, limit=1);  plants.extend(ps or [])
        if len(diseases) < 3:
            ds = search_diseases_by_text(tok, limit=1); diseases.extend(ds or [])
    return plants[:3], diseases[:3]
