# services/nlu.py
from langdetect import detect
import re, unicodedata
from typing import Literal, Tuple, Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func, literal, or_, text 
from models import Plant, Remedy

Intent = Literal["plant", "condition"]

# Canonical remedy labels present in DB
CANON = {
    "cough": "Cough",
    "fever": "Fever",
    "indigestion": "Indigestion",
    "stress": "Stress & Anxiety",
    "skin_allergy": "Skin Allergy",
    "resp_weakness": "Respiratory Weakness",
    "low_immunity": "Low Immunity",
    "acidity": "Acidity",
    "female_health": "Female Health",
    "joint_pain": "Joint Pain",
}

# Multilingual synonyms → canonical keys
SYM_MAP = {
    "en": {
        "cough": ["cough", "cold", "sore throat", "throat", "bronchitis"],
        "fever": ["fever", "temperature", "pyrexia"],
        "indigestion": ["indigestion", "gas", "bloating", "acidity problem", "upset stomach"],
        "stress": ["stress", "anxiety", "tension", "insomnia", "sleepless"],
        "skin_allergy": ["skin", "eczema", "itching", "allergy", "acne", "rash"],
        "resp_weakness": ["asthma", "bronchitis", "breathing", "wheezing", "respiratory"],
        "low_immunity": ["low immunity", "immune", "weak immunity", "frequent cold"],
        "acidity": ["acidity", "heartburn", "reflux", "gerd"],
        "female_health": ["female", "hormonal", "lactation", "women health"],
        "joint_pain": ["joint pain", "arthritis", "inflammation", "knee pain"],
    },
    "hi": {
        "cough": ["खांसी", "सर्दी", "जुकाम", "गला दर्द"],
        "fever": ["बुखार", "ताप"],
        "indigestion": ["अपच", "गैस", "फूलना", "बदहजमी"],
        "stress": ["तनाव", "चिंता", "नींद नहीं", "अनिद्रा"],
        "skin_allergy": ["त्वचा", "एक्जिमा", "खुजली", "एलर्जी", "मुँहासे", "दाने"],
        "resp_weakness": ["अस्थमा", "श्वसन", "सांस", "सांस फूलना", "ब्रोंकाइटिस"],
        "low_immunity": ["कम प्रतिरक्षा", "प्रतिरक्षा", "बार-बार जुकाम"],
        "acidity": ["अम्लता", "सीने में जलन", "एसिडिटी"],
        "female_health": ["महिला", "हार्मोन", "स्तनपान", "लैक्टेशन"],
        "joint_pain": ["जोड़ दर्द", "गठिया", "सूजन"],
    },
    "mr": {
        "cough": ["खोकला", "सर्दी", "घसा दुखणे"],
        "fever": ["ताप", "ज्वर"],
        "indigestion": ["अपचन", "गॅस", "पोट फुगणे"],
        "stress": ["ताण", "चिंता", "झोप नाही", "अनिद्रा"],
        "skin_allergy": ["त्वचा", "एक्झिमा", "खाज", "अॅलर्जी", "पुरळ"],
        "resp_weakness": ["दम्याचा त्रास", "श्वसन", "श्वास", "ब्रॉन्कायटिस"],
        "low_immunity": ["कमी प्रतिकारशक्ती", "वारंवार सर्दी"],
        "acidity": ["अम्लपित्त", "छातीत जळजळ", "अॅसिडिटी"],
        "female_health": ["महिला", "हार्मोन", "स्तनपान", "लेक्टेशन"],
        "joint_pain": ["सांधेदुखी", "आर्थ्रायटिस", "दाह"],
    }
}

def normalize(s: str) -> str:
    # NFC keeps Devanagari composed; do not lose Unicode case
    s = unicodedata.normalize("NFC", s or "")
    s = s.replace("/", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s.lower()  # lower() is no-op for Devanagari and safe for Latin

def _split_tokens(q_norm: str) -> List[str]:
    return [t for t in re.split(r"[^0-9A-Za-z\u0900-\u097F]+", q_norm) if t]

def lookup_plant(db: Session, q_norm: str) -> Optional[Plant]:
    """
    Deterministic Unicode-safe lookup order:
      (A) FTS5 MATCH on plant_fts (name, scientific, synonyms, uses, description, properties)
      (B) Raw SQL LIKE on name/scientific/synonyms with the longest token
      (C) Python-side contains as a final guardrail
    Returns actual Plant instance or None.
    """
    # ---------- A) FTS5 (best for multilingual / fuzzy) ----------
    try:
        tokens = _split_tokens(q_norm)
        q_fts = " OR ".join(tokens[:6]) if tokens else q_norm
        row = db.execute(
            text(
                """SELECT p.id
                   FROM plant p
                   JOIN plant_fts f ON f.rowid = p.id
                   WHERE plant_fts MATCH :q
                   ORDER BY length(p.name) DESC
                   LIMIT 1"""
            ),
            {"q": q_fts},
        ).fetchone()
        if row:
            return db.get(Plant, row[0])
    except Exception as _:
        pass  # fall through

    # ---------- B) Raw SQL LIKE (no ORM ilike/instr quirks) ----------
    tokens = _split_tokens(q_norm)
    longest = max(tokens, key=len) if tokens else q_norm
    like = f"%{longest}%"
    row = db.execute(
        text(
            """SELECT id FROM plant
               WHERE coalesce(name,'') LIKE :like
                  OR coalesce(scientific_name,'') LIKE :like
                  OR coalesce(synonyms,'') LIKE :like
               ORDER BY length(name) DESC
               LIMIT 1"""
        ),
        {"like": like},
    ).fetchone()
    if row:
        return db.get(Plant, row[0])

    # ---------- C) Python-side contains (last resort, always works) ----------
    # lightweight scan; plant table is tiny (dozens/hundreds)
    for pid, nm, sci, syn in db.query(Plant.id, Plant.name, Plant.scientific_name, Plant.synonyms).all():
        if not nm and not sci and not syn:
            continue
        hay = " ".join([str(nm or ""), str(sci or ""), str(syn or "")]).lower()
        if q_norm in hay or any(t in hay for t in tokens):
            return db.get(Plant, pid)

    return None
################################################################################################################

def detect_lang(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"

def _tokens(q_norm: str) -> List[str]:
    toks = re.split(r"[^0-9A-Za-z\u0900-\u097F]+", q_norm)
    return [t for t in toks if len(t) >= 2]

def canonical_symptoms(q_norm: str, lang: str) -> List[str]:
    """Return list of canonical English labels present in the query."""
    lang = "hi" if lang.startswith("hi") else "mr" if lang.startswith("mr") else "en"
    toks = set(_tokens(q_norm))
    hits = []
    for key, synonyms in SYM_MAP[lang].items():
        for syn in synonyms:
            # match a token or phrase in normalized string
            if " " in syn:
                if syn.lower() in q_norm:
                    hits.append(CANON[key])
                    break
            else:
                if syn.lower() in toks:
                    hits.append(CANON[key])
                    break
    return list(dict.fromkeys(hits))  # unique preserve order

def search_remedies(db: Session, q_norm: str, lang: str, limit=10) -> List[Remedy]:
    labels = canonical_symptoms(q_norm, lang)
    if labels:
        # Try matching by canonical symptom name first (fast and reliable)
        q = db.query(Remedy).filter(func.lower(Remedy.symptom).in_([l.lower() for l in labels]))
        res = q.limit(limit).all()
        if res:
            return res

    # FTS with simplified query (use single-words/phrases)
    try:
        q_simple = " OR ".join(_tokens(q_norm)[:6]) or q_norm
        rows = db.execute(
            """SELECT r.id
               FROM remedy r
               JOIN remedy_fts f ON f.rowid = r.id
               WHERE remedy_fts MATCH :q
               LIMIT :lim
            """,
            {"q": q_simple, "lim": limit},
        ).fetchall()
        if rows:
            ids = [row[0] for row in rows]
            return db.query(Remedy).filter(Remedy.id.in_(ids)).all()
    except Exception:
        pass

    # LAST: LIKE over key fields
    like = f"%{q_norm}%"
    return db.query(Remedy).filter(
        (Remedy.symptom.ilike(like)) |
        (Remedy.diagnosis_pattern.ilike(like)) |
        (Remedy.preparation.ilike(like)) |
        (Remedy.dosage.ilike(like)) |
        (Remedy.lifestyle_recommendations.ilike(like)) |
        (Remedy.side_effects.ilike(like)) |
        (Remedy.contraindications.ilike(like))
    ).limit(limit).all()

# services/nlu.py

def lookup_plant(db: Session, q_norm: str) -> Optional[Plant]:
    """
    Robust plant lookup that works with English and Devanagari tokens.
    Strategy:
      (a) reverse-contains on name/scientific,
      (b) token LIKE across name/scientific/synonyms,
      (c) last-resort reverse-contains on whole synonyms blob.
    """
    from sqlalchemy import or_
    qlit = literal(q_norm)

    # (a) reverse on name/scientific (fast)
    candidate = (
        db.query(Plant)
        .filter(
            (func.instr(qlit, func.lower(Plant.name)) > 0) |
            (func.instr(qlit, func.lower(Plant.scientific_name)) > 0)
        )
        .order_by(func.length(Plant.name).desc())
        .first()
    )
    if candidate:
        return candidate

    # (b) token LIKE across all text fields (handles "तुलसी"/"तुळस")
    toks = _tokens(q_norm)
    if toks:
        ors = []
        for t in toks[:8]:
            like = f"%{t}%"
            ors.extend([
                Plant.name.ilike(like),
                Plant.scientific_name.ilike(like),
                func.coalesce(Plant.synonyms, "").ilike(like),
            ])
        cand = db.query(Plant).filter(or_(*ors)).order_by(Plant.name.asc()).first()
        if cand:
            return cand

    # (c) reverse-contains on entire synonyms blob (last resort)
    return (
        db.query(Plant)
        .filter(func.instr(qlit, func.lower(func.coalesce(Plant.synonyms, ""))) > 0)
        .first()
    )

def parse_intent(db: Session, text: str) -> Tuple[Intent, Optional[Plant]]:
    """
    IMPORTANT: Try to resolve a plant FIRST.
    If no plant is found, then classify as 'condition'.
    This guarantees queries like 'तुलसी के बारे में बताओ' pick the plant path.
    """
    q = normalize(text)
    p = lookup_plant(db, q)
    if p:
        return "plant", p
    # fall back to remedies
    return "condition", None


# --- ADD near the top of services/nlu.py imports ---
from sqlalchemy import text
from typing import Dict

# --- ADD these helpers to services/nlu.py ---

def _fts_query_string(q_norm: str, lang: str) -> str:
    """
    Build a compact MATCH query that mixes tokens plus canonical symptom labels.
    """
    toks = _tokens(q_norm)[:6]
    # pull canonical English labels (even if lang is hi/mr, we mapped to CANON)
    labels = canonical_symptoms(q_norm, lang)
    parts = toks + [l.lower() for l in labels]
    return " OR ".join(dict.fromkeys([p for p in parts if p])) or q_norm

def fts_plants(db: Session, q_norm: str, lang: str, limit: int = 6) -> list[Plant]:
    """
    Primary: FTS5 with BM25. Secondary: LIKE fallback.
    """
    q = _fts_query_string(q_norm, lang)
    try:
        rows = db.execute(
            text("""
                SELECT p.id
                FROM plant p
                JOIN plant_fts f ON f.rowid = p.id
                WHERE plant_fts MATCH :q
                ORDER BY bm25(plant_fts) ASC, length(p.name) DESC
                LIMIT :lim
            """),
            {"q": q, "lim": limit*2},
        ).fetchall()
        if rows:
            ids = [r[0] for r in rows]
            got = db.query(Plant).filter(Plant.id.in_(ids)).all()
            # preserve FTS ranking order
            order = {pid:i for i,pid in enumerate(ids)}
            got.sort(key=lambda p: order.get(p.id, 10**9))
            return got[:limit]
    except Exception:
        pass

    like = f"%{q_norm}%"
    return db.query(Plant).filter(
        (Plant.name.ilike(like)) |
        (Plant.scientific_name.ilike(like)) |
        (func.coalesce(Plant.synonyms, "").ilike(like)) |
        (func.coalesce(Plant.uses, "").ilike(like)) |
        (func.coalesce(Plant.description, "").ilike(like))
    ).limit(limit).all()

def fts_remedies(db: Session, q_norm: str, lang: str, limit: int = 5) -> list[Remedy]:
    """
    Try canonical labels → FTS (BM25) → LIKE.
    """
    labels = canonical_symptoms(q_norm, lang)
    if labels:
        q = db.query(Remedy).filter(func.lower(Remedy.symptom).in_([l.lower() for l in labels]))
        hit = q.limit(limit).all()
        if hit:
            return hit

    q = _fts_query_string(q_norm, lang)
    try:
        rows = db.execute(
            text("""
                SELECT r.id
                FROM remedy r
                JOIN remedy_fts f ON f.rowid = r.id
                WHERE remedy_fts MATCH :q
                ORDER BY bm25(remedy_fts) ASC
                LIMIT :lim
            """),
            {"q": q, "lim": limit*2},
        ).fetchall()
        if rows:
            ids = [r[0] for r in rows]
            got = db.query(Remedy).filter(Remedy.id.in_(ids)).all()
            order = {pid:i for i,pid in enumerate(ids)}
            got.sort(key=lambda r: order.get(r.id, 10**9))
            return got[:limit]
    except Exception:
        pass

    like = f"%{q_norm}%"
    return db.query(Remedy).filter(
        (Remedy.symptom.ilike(like)) |
        (Remedy.diagnosis_pattern.ilike(like)) |
        (Remedy.preparation.ilike(like)) |
        (Remedy.dosage.ilike(like)) |
        (Remedy.lifestyle_recommendations.ilike(like)) |
        (Remedy.side_effects.ilike(like)) |
        (Remedy.contraindications.ilike(like))
    ).limit(limit).all()

def hybrid_retrieve(db: Session, q_norm: str, lang: str,
                    plant_limit: int = 5, remedy_limit: int = 3) -> Dict[str, list]:
    """
    Pull both plants and remedies; let the caller decide how to answer.
    """
    plants = fts_plants(db, q_norm, lang, plant_limit)
    remedies = fts_remedies(db, q_norm, lang, remedy_limit)
    return {"plants": plants, "remedies": remedies}
