import os, glob
import re
from typing import Dict, List, Tuple
from db import get_db
import sentencepiece as spm
import ctranslate2

DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")  # Hindi/Marathi script range

# ---- Bilingual hint maps (extend as needed) ----
HI_MR_TO_EN = {
    # disease/intent keywords
    "मधुमेह": "diabetes", "मधु मेह": "diabetes", "शुगर": "blood sugar",
    "खोकला": "cough", "सर्दी": "cold", "जुलाब": "diarrhea", "कब्ज": "constipation",
    "गॅस": "indigestion", "निद्रानाश": "insomnia", "त्वचा": "skin",
    "बीपी": "bp", "रक्तदाब": "hypertension", "दाब": "hypertension",

    # plants (sample; add yours)
    "गुळवेल": "guduchi", "गिलोय": "guduchi", "नीम": "neem", "तुळस": "tulsi",
}
EN_TO_HI = {
    "diabetes": "मधुमेह",
    "guduchi": "गुडूची",  # or "गिलोय"
    "neem": "नीम",
    "tulsi": "तुलसी",
}

MR_MARKERS = {"बद्दल", "माहिती", "तुळस", "गुळवेल", "औषधी", "काढा"}

# -------- Language detection --------
def detect_language(text: str) -> str:
    # Very fast heuristic: if Devanagari present -> 'hi_or_mr', else 'en'
    # We'll disambiguate hi vs mr using small word hints.
    if DEVANAGARI_RE.search(text or ""):
        # naive hints
        mr_markers = {"आलं", "हिरडा", "काढा", "औषधी", "आवळा", "तुळस", "दुखी", "बद्दल", "माहिती", "गुळवेल"}
        if any(tok in text for tok in mr_markers):
            return "mr"
        return "hi"
    return "en"

# -------- Translation adapter (pluggable) --------

def _find_spm(dir_path: str):
    import os, glob
    spms = glob.glob(os.path.join(dir_path, "*.spm"))
    if len(spms) >= 2:
        return spms[0], spms[1]
    if len(spms) == 1:
        # use same SPM for src & tgt if the model is joint
        return spms[0], spms[0]
    # common names
    for a, b in [("source.spm","target.spm"), ("src.spm","tgt.spm")]:
        sa, sb = os.path.join(dir_path, a), os.path.join(dir_path, b)
        if os.path.isfile(sa) and os.path.isfile(sb):
            return sa, sb
    return None, None


class Translator:
    """
    Offline MarianMT via CTranslate2 for hi↔en and mr↔en.
    Falls back to dictionary swaps if models missing.
    """
    def __init__(self):
        root = os.getenv("HERBOAI_MODELS_ROOT", os.path.join(os.getcwd(), "models", "ct2"))
        self.paths = {
            "hi_en": {"model_dir": os.path.join(root, "hi-en-int8")},
            "en_hi": {"model_dir": os.path.join(root, "en-hi-int8")},
            "mr_en": {"model_dir": os.path.join(root, "mr-en-int8")},
            "en_mr": {"model_dir": os.path.join(root, "en-mr-int8")},
        }
        self.available = False
        self.mode = "noop"

        self._t = {}     # key -> ctranslate2.Translator
        self._sp_src = {}  # key -> SentencePieceProcessor
        self._sp_tgt = {}  # key -> SentencePieceProcessor

        try:
            ok = True
            for k, v in self.paths.items():
                model_dir = v["model_dir"]
                if not os.path.isfile(os.path.join(model_dir, "model.bin")):
                    ok = False; break
                sp_src, sp_tgt = _find_spm(model_dir)
                if not sp_src or not sp_tgt:
                    ok = False; break
                v["sp_src"], v["sp_tgt"] = sp_src, sp_tgt
            if ok:
                self.available = True
                self.mode = "marian_ct2"
        except Exception:
            self.available = False
            self.mode = "noop"

    def _ensure_loaded(self, key: str):
        if key in self._t:  # already loaded
            return
        v = self.paths[key]
        self._t[key] = ctranslate2.Translator(v["model_dir"])
        self._sp_src[key] = spm.SentencePieceProcessor(model_file=v["sp_src"])
        self._sp_tgt[key] = spm.SentencePieceProcessor(model_file=v["sp_tgt"])

    def _translate(self, text: str, key: str) -> str:
        self._ensure_loaded(key)
        toks = self._sp_src[key].encode(text, out_type=str)
        res = self._t[key].translate_batch([toks], beam_size=4, max_decoding_length=256, repetition_penalty=1.1)
        out_tokens = res[0].hypotheses[0]
        return self._sp_tgt[key].decode(out_tokens)

    # public
    def to_en(self, text: str, src_lang: str) -> str:
        if not text:
            return text
        # dictionary booster first
        t = text
        for k, v in HI_MR_TO_EN.items():
            if k in t:
                t = t.replace(k, v)
        if src_lang == "en" or not self.available or self.mode != "marian_ct2":
            return t
        try:
            key = "hi_en" if src_lang == "hi" else ("mr_en" if src_lang == "mr" else None)
            if not key:
                return t
            out = self._translate(t, key)
            return out or t
        except Exception:
            return t

    def from_en(self, text: str, tgt_lang: str) -> str:
        if not text or tgt_lang == "en":
            return text
        if not self.available or self.mode != "marian_ct2":
            out = text
            for en, hi in EN_TO_HI.items():
                out = out.replace(en, hi)
            return out
        try:
            key = "en_hi" if tgt_lang == "hi" else ("en_mr" if tgt_lang == "mr" else None)
            if not key:
                return text
            out = self._translate(text, key)
            return out or text
        except Exception:
            out = text
            for en, hi in EN_TO_HI.items():
                out = out.replace(en, hi)
            return out

translator = Translator()

# -------- Intent classification (deterministic) --------
INTENTS = ("remedy_lookup", "plant_info", "preparation_info", "lifestyle_advice", "none")

def classify_intent(text_en_or_src: str) -> str:
    t = (text_en_or_src or "").lower()

    complaint_cues = [
        "i have ", "i am having ", "i suffer from ", "i am suffering from ",
        "remedy for", "treatment for", "herbs for", "help with ",
        "my blood sugar", "my bp", "my pressure"
    ]

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
    if any(k in t for k in complaint_cues) or any(k in t for k in disease_cues):
        return "remedy_lookup"
    if any(k in t for k in plant_cues):
        return "plant_info"
    if "preparation" in t or "dosage" in t or "how to make" in t or "kashaya" in t or "decoction" in t:
        return "preparation_info"

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

def extract_entities(text: str, text_en: str | None = None, prefer_en: bool = False) -> Tuple[List[Dict], List[Dict]]:
    """
    Returns (plants, diseases) as lists of dict rows.
    Tries robustly: direct match, then FTS fallback.
    """
    q = (text_en if prefer_en and text_en else text)
    tokens = re.findall(r"[A-Za-z\u0900-\u097F]+", q or "")
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
