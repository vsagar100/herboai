# services/nlu.py
from langdetect import detect
import re
from typing import Literal, Tuple, Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import func, literal, or_
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

def detect_lang(text: str) -> str:
    try:
        return detect(text)
    except Exception:
        return "en"

def normalize(s: str) -> str:
    s = s.replace("/", " ")
    return re.sub(r"\s+", " ", s).strip().lower()

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
