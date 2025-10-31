import re
from typing import Dict, List, Tuple
from db import get_db

DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")  # Hindi/Marathi script range

# -------- Language detection --------
def detect_language(text: str) -> str:
    # Very fast heuristic: if Devanagari present -> 'hi_or_mr', else 'en'
    # We'll disambiguate hi vs mr using small word hints.
    if DEVANAGARI_RE.search(text or ""):
        # naive hints
        mr_markers = {"आलं", "हिरडा", "काढा", "औषधी", "आवळा", "तुळस", "दुखी"}
        if any(tok in text for tok in mr_markers):
            return "mr"
        return "hi"
    return "en"

# -------- Translation adapter (pluggable) --------
class Translator:
    """
    Pluggable translator.
    - If IndicTrans2 + CTranslate2 are installed, use them (CPU friendly).
    - Otherwise, no-op to keep pipeline runnable without net/GPU.
    """
    def __init__(self):
        self.available = False
        self.mode = "noop"
        # Lazy detection (do not import heavy libs if not present)
        try:
            # Example (commented): wire your local models here
            # from indictrans2 import IndicTransliterator
            # import ctranslate2
            # self.available = True
            # self.mode = "indictrans2_ct2"
            pass
        except Exception:
            self.available = False
            self.mode = "noop"

    def to_en(self, text: str, src_lang: str) -> str:
        if src_lang == "en":
            return text
        if not text:
            return text
        if self.mode == "indictrans2_ct2" and self.available:
            # TODO: plug actual call
            return text  # placeholder until you wire model path
        # Safe fallback (no external calls): keep text; retrieval still works via FTS on hi/mr fields/synonyms
        return text

    def from_en(self, text: str, tgt_lang: str) -> str:
        if tgt_lang == "en":
            return text
        if not text:
            return text
        if self.mode == "indictrans2_ct2" and self.available:
            # TODO: plug actual call
            return text
        return text

translator = Translator()

# -------- Intent classification (deterministic) --------
INTENTS = ("remedy_lookup", "plant_info", "preparation_info", "lifestyle_advice", "none")

def classify_intent(text_en_or_src: str) -> str:
    t = (text_en_or_src or "").lower()

    # broaden disease cues to include bare keywords
    disease_cues = [
        "diabetes",                 # <— added
        "for diabetes",
        "blood sugar",
        "cough", "cold", "arthritis", "joint",
        "bp", "hypertension",
        "gastric", "indigestion", "constipation",
        "sleep", "insomnia", "skin"
    ]
    prep_cues = ["how to prepare", "kwatha", "decoction", "churna", "powder", "oil", "ghrita", "taila"]
    plant_cues = ["what is", "about", "uses of", "benefits of"]

    if any(k in t for k in prep_cues):
        return "preparation_info"
    if any(k in t for k in disease_cues):
        return "remedy_lookup"
    if any(k in t for k in plant_cues):
        return "plant_info"
    return "none"


# -------- Entity extraction via DB (FTS & synonyms) --------
def search_plants_by_text(q: str, limit=5) -> List[Dict]:
    db = get_db()
    cur = db.cursor()
    # Try synonyms exact-ish first
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
              SELECT rowid AS id
              FROM plants_fts
              WHERE plants_fts MATCH ?
              LIMIT ?
            )
            SELECT p.* FROM hits h JOIN plants p ON p.id=h.id
        """, (q, limit))
        rows = cur.fetchall()
    cur.close()
    return [dict(r) for r in rows]

def search_diseases_by_text(q: str, limit=5) -> List[Dict]:
    db = get_db()
    cur = db.cursor()
    # try synonyms first
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
              SELECT rowid AS id
              FROM diseases_fts
              WHERE diseases_fts MATCH ?
              LIMIT ?
            )
            SELECT d.* FROM hits h JOIN diseases d ON d.id=h.id
        """, (q, limit))
        rows = cur.fetchall()
    cur.close()
    return [dict(r) for r in rows]

def extract_entities(text: str) -> Tuple[List[Dict], List[Dict]]:
    """
    Returns (plants, diseases) as lists of dict rows.
    Tries robustly: direct match, then FTS fallback.
    """
    tokens = re.findall(r"[A-Za-z\u0900-\u097F]+", text or "")
    plants, diseases = [], []
    # probe longest tokens first
    for tok in sorted(set(tokens), key=len, reverse=True):
        if len(plants) < 3:
            ps = search_plants_by_text(tok, limit=1)
            if ps:
                plants.extend(ps)
        if len(diseases) < 3:
            ds = search_diseases_by_text(tok, limit=1)
            if ds:
                diseases.extend(ds)
    return plants[:3], diseases[:3]
