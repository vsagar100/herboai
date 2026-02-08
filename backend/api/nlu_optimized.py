# api/nlu_optimized.py
"""
Optimized NLU for multilingual queries
- Fast language detection
- Smart entity extraction with synonym + i18n + vector matching
- Marathi/Hindi postposition stripping for accurate token matching
- Embedding-based semantic search for entity identification
"""
import re
import logging
from typing import Dict, List, Tuple
from db import get_db

_nlu_log = logging.getLogger("nlu")

try:
    from services.indic_translation_service import IndicTranslationService
except Exception:
    IndicTranslationService = None  # type: ignore

# Language detection patterns
DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

# Lightweight markers as a fallback if shared detector is unavailable
MR_MARKERS = {
    "बद्दल", "माहिती", "तुळस", "गुळवेल", "औषधी", "काढा",
    "आलं", "हिरडा", "आवळा", "दुखी", "साठी", "मला", "आहे"
}

# Hindi-specific markers
HI_MARKERS = {
    "के लिए", "क्या", "कैसे", "मुझे", "है", "में", "को",
    "से", "बारे", "जानकारी", "औषधि"
}

# Common transliterations & phonetic variations
TRANSLITERATION_MAP = {
    # Plants
    "ashwagandha": "अश्वगंधा", "ashvagandha": "अश्वगंधा",
    "tulsi": "तुलसी", "tulasi": "तुलसी", "basil": "तुलसी",
    "neem": "नीम", "nim": "नीम",
    "guduchi": "गुडूची", "giloy": "गिलोय", "gulvel": "गुळवेल",
    "amla": "आँवला", "amalaki": "आमलकी", "आवळा": "आँवला",
    "haritaki": "हरीतकी", "harad": "हरड", "hirda": "हिरडा",
    "turmeric": "हल्दी", "haldi": "हल्दी", "halad": "हळद",
    "ginger": "अदरक", "adrak": "अदरक", "आलं": "अदरक",
    
    # Diseases
    "diabetes": "मधुमेह", "madhumeha": "मधुमेह", "sugar": "मधुमेह",
    "bp": "उच्च रक्तदाब", "hypertension": "उच्च रक्तदाब",
    "cough": "खांसी", "khansi": "खांसी", "खोकला": "खांसी",
    "cold": "सर्दी", "sardi": "सर्दी", "जुकाम": "सर्दी",
    "fever": "ज्वर", "bukhar": "बुखार", "ताप": "ज्वर",
    "arthritis": "गठिया", "जोडदुखी": "गठिया",
    "constipation": "कब्ज", "kabaj": "कब्ज", "बद्धकोष्ठ": "कब्ज",
    "acidity": "अम्लपित्त", "gas": "वायु", "गॅस": "वायु"
}

_QUERY_STOPWORDS = {
    "how", "to", "prepare", "make", "making", "do", "use", "usage",
    "powder", "tablet", "decoction", "kwath", "kwatha", "kadha",
    "syrup", "capsule", "oil", "taila", "ghrita",
    "for", "of", "the", "a", "an", "is", "what", "tell", "me",
    "dosage", "dose", "remedy", "info", "information", "guide",
    "about", "benefits", "help"
}

# ── Marathi / Hindi postposition & suffix stripping ──
# These are common grammatical suffixes that get attached to nouns
# e.g. "मुरुमांसाठी" = "मुरुम" + "ांसाठी" (for pimples)
#      "निंबाचे"     = "निंब" + "ाचे"    (of neem)
# Ordered longest-first so greedy stripping picks the right suffix.
_INDIC_SUFFIXES = sorted([
    # Marathi postpositions (साठी = for, ला = to, ने = by, etc.)
    "ांसाठी", "ासाठी", "साठी",
    "ामध्ये", "मध्ये",
    "ाबद्दल", "बद्दल",
    "ावर", "ावरून",
    "ाला", "ाने", "ाचा", "ाची", "ाचे", "ाच्या",
    "ांचा", "ांची", "ांचे", "ांच्या", "ांना",
    "चा", "ची", "चे", "च्या",
    "ला", "ने", "ना", "त", "ं",
    # Hindi postpositions (के लिए handled at phrase level above)
    "ों", "ें", "ां",
], key=len, reverse=True)

# Marathi / Hindi stopword tokens (not entity-bearing)
_INDIC_STOPWORDS = {
    "साठी", "बद्दल", "माहिती", "काय", "कसे", "कसा", "करा",
    "सांगा", "मला", "आहे", "आहेत", "हवे", "हवी", "बनवा",
    "के", "लिए", "क्या", "कैसे", "बताओ", "मुझे", "है", "हैं",
    "और", "या", "किंवा", "आणि",
}


def _strip_indic_suffix(token: str) -> List[str]:
    """
    Strip Marathi/Hindi postpositions / inflectional suffixes from a
    Devanagari token and return all plausible stems (including original).
    """
    stems = [token]
    for suf in _INDIC_SUFFIXES:
        if token.endswith(suf) and len(token) > len(suf) + 1:
            stem = token[:-len(suf)]
            if stem not in stems:
                stems.append(stem)
    return stems


def _tokenize_query_terms(query: str) -> List[str]:
    """
    Break query into unique tokens (>=2 chars for Devanagari, >=3 for Latin)
    preserving order. Includes stemmed variants for Devanagari tokens.
    """
    raw_tokens = re.findall(r"[A-Za-z\u0900-\u097F]+", (query or "").lower())
    tokens: List[str] = []
    seen = set()
    for tok in raw_tokens:
        min_len = 2 if re.search(r"[\u0900-\u097F]", tok) else 3
        if len(tok) < min_len or tok in seen:
            continue
        # Skip known Indic stopword tokens
        if tok in _INDIC_STOPWORDS:
            continue
        seen.add(tok)
        tokens.append(tok)
        # Also add stemmed variants for Devanagari tokens
        if re.search(r"[\u0900-\u097F]", tok):
            for stem in _strip_indic_suffix(tok):
                if stem != tok and stem not in seen and len(stem) >= 2:
                    seen.add(stem)
                    tokens.append(stem)
    return tokens


def _prioritized_tokens(query: str) -> List[str]:
    """
    Return the most meaningful tokens for lookup (filter stopwords first).
    """
    tokens = _tokenize_query_terms(query)
    if not tokens:
        return []

    meaningful = [tok for tok in tokens if tok not in _QUERY_STOPWORDS]
    return meaningful or tokens

def detect_language(text: str) -> str:
    """
    Fast language detection
    Returns: 'en', 'hi', or 'mr'
    """
    if not text:
        return "en"

    # Prefer the shared detector (no model load; pure heuristics)
    if IndicTranslationService:
        try:
            return IndicTranslationService.detect_lang(text)
        except Exception:
            pass

    t = text.lower()
    if not DEVANAGARI_RE.search(t):
        return "en"

    mr_count = sum(1 for marker in MR_MARKERS if marker in t)
    hi_count = sum(1 for marker in HI_MARKERS if marker in t)
    if mr_count > hi_count or any(word in t for word in ["गुळवेल", "तुळस", "आवळा", "हिरडा"]):
        return "mr"
    return "hi"

def classify_intent(text: str) -> str:
    """
    Classify user intent based on query patterns
    Returns: remedy_lookup, plant_info, preparation_info, lifestyle_advice, none
    """
    t = (text or "").lower()

    # --- 1) Explicit preparation queries (highest priority) ---
    prep_patterns = [
        "how to prepare", "how to make", "recipe for", "making", "prepare",
        "kwatha", "decoction", "kashaya", "काढा", "काढे",
        "churna", "powder", "चूर्ण", "oil", "taila", "तेल", "घृत",
        "dosage", "dose", "मात्रा", "कसे बनवायचे", "कैसे बनाएं",
        "कसा बनवायचा", "बनवण्याची पद्धत", "बनव"  # generic Marathi/Hindi 'to make'
    ]
    if any(p in t for p in prep_patterns):
        return "preparation_info"

    # --- 2) Signals for plant-info vs. remedy ---
    plant_patterns = [
        "what is", "about", "uses of", "benefits", "properties",
        "बद्दल", "के बारे", "फायदे", "गुण", "उपयोग", "माहिती"
    ]

    remedy_patterns = [
        "i have", "i am having", "suffering from", "remedy for",
        "treatment for", "herbs for", "cure for", "help with",
        "मला", "मुझे", "साठी", "के लिए", "उपचार", "औषधी"
    ]

    # Comprehensive disease keywords (100+ conditions)
    disease_keywords = [
        # Chronic conditions
        "diabetes", "मधुमेह", "sugar", "शुगर",
        "bp", "pressure", "hypertension", "उच्च रक्तदाब", "रक्तदाब",
        "arthritis", "गठिया", "joint pain", "संधिवात", "जोडदुखी",
        "asthma", "दमा", "श्वास", "breathing",
        "thyroid", "थायरॉइड", "थायराइड",
        
        # Respiratory & seasonal
        "cough", "खांसी", "खोकला",
        "cold", "सर्दी", "जुकाम",
        "fever", "ज्वर", "बुखार", "ताप",
        "flu", "इन्फ्लूएंजा", "सर्दी-जुकाम",
        "sore throat", "throat pain", "गळा दुखणे", "गले में दर्द",
        "sinusitis", "सायनसायटिस", "नाक बंद",
        
        # Digestive
        "acidity", "अम्लपित्त", "एसिडिटी",
        "gas", "गॅस", "वायु", "पेट फूलना",
        "constipation", "कब्ज", "बद्धकोष्ठ",
        "diarrhea", "अतिसार", "दस्त", "loose motion",
        "indigestion", "अपचन", "digestion",
        "stomach", "पेट", "gastric", "ulcer", "व्रण",
        "nausea", "मतली", "उलटी", "vomiting",
        "ibs", "irritable bowel",
        
        # Skin conditions
        "acne", "pimples", "मुरुम", "पिंपल्स", "फुंसी",
        "eczema", "एक्जिमा", "खाज",
        "psoriasis", "सोरायसिस", "त्वचा रोग",
        "skin", "त्वचा", "rash", "खरुज", "चकत्ते",
        "itching", "खाज", "खुजली",
        "fungal", "बुरशी", "infection",
        "vitiligo", "लेकोडर्मा", "पांढरे डाग",
        "dark spots", "काळे डाग", "pigmentation",
        
        # Hair problems
        "hair fall", "hair loss", "केस गळणे", "बाल झड़ना",
        "baldness", "टक्कल", "alopecia",
        "dandruff", "कोंडा", "रूसी",
        "grey hair", "पांढरे केस", "सफेद बाल",
        
        # Mental health
        "anxiety", "चिंता", "tension", "तणाव",
        "stress", "तणाव", "मानसिक तणाव",
        "depression", "नैराश्य", "उदासी",
        "insomnia", "अनिद्रा", "झोप न येणे", "नींद न आना",
        "sleep", "झोप", "नींद",
        "memory", "स्मरणशक्ती", "याददाश्त",
        
        # Pain & inflammation
        "pain", "दुखी", "दर्द", "वेदना",
        "headache", "डोकेदुखी", "सिरदर्द",
        "migraine", "मायग्रेन", "अर्धशिशी",
        "backache", "पाठदुखी", "कमर दर्द",
        "knee pain", "गुडघा दुखणे", "घुटने का दर्द",
        "muscle pain", "स्नायू दुखणे",
        "inflammation", "सूज", "सुजन",
        
        # Women's health
        "periods", "मासिक पाळी", "माहवारी", "menstrual",
        "pcos", "pcod", "पीसीओएस",
        "menopause", "रजोनिवृत्ती",
        "leucorrhea", "श्वेतप्रदर",
        "pregnancy", "गर्भावस्था",
        
        # Metabolic & blood
        "anemia", "अॅनिमिया", "रक्ताची कमी", "खून की कमी",
        "weakness", "अशक्तपणा", "कमजोरी",
        "fatigue", "थकवा", "थकान",
        "weight loss", "वजन कमी", "वजन घटाना",
        "obesity", "लठ्ठपणा", "मोटापा", "वजन",
        "cholesterol", "कोलेस्टेरॉल",
        
        # Urinary & kidney
        "kidney", "किडनी", "मूत्रपिंड",
        "stone", "पथरी", "खडे",
        "urine", "लघवी", "पेशाब", "uti",
        
        # Liver
        "liver", "यकृत", "जिगर", "लिव्हर",
        "jaundice", "कावीळ", "पीलिया",
        "fatty liver", "फॅटी लिव्हर",
        
        # Others
        "allergy", "ऍलर्जी", "अलर्जी",
        "wound", "जखम", "घाव",
        "burn", "भाजलेले", "जलना",
        "piles", "मूळव्याध", "बवासीर",
        "fistula", "भगंदर",
        "worms", "किडे", "कृमी"
    ]

    has_plant = any(p in t for p in plant_patterns)
    has_remedy = any(p in t for p in remedy_patterns)
    has_disease_kw = any(k in t for k in disease_keywords)

    # If disease words are present, or the user clearly asks for
    # help/उपचार, treat as a remedy/condition query even if there are
    # generic plant-info words like "उपयोग". This fixes Marathi
    # sentences like "मला मधुमेह आहे. काय उपयोगी पडेल?".
    if has_disease_kw or has_remedy:
        return "remedy_lookup"

    # Pure "about / uses / benefits" queries with no disease/remedy
    # markers fall back to plant_info.
    if has_plant:
        return "plant_info"

    return "none"

def normalize_query_token(token: str) -> List[str]:
    """
    Normalize a token to handle phonetic variations AND Indic inflections.
    Returns list of possible variations (original + stemmed + transliterated).
    """
    token_lower = (token or "").lower().strip()

    # Base variation list always includes the raw token
    variations = [token_lower]

    # ── Devanagari suffix stripping (comprehensive) ──
    # Uses the global _INDIC_SUFFIXES list which covers postpositions,
    # possessives, and oblique-case markers.
    if re.search(r"[\u0900-\u097F]", token_lower):
        for stem in _strip_indic_suffix(token_lower):
            if stem != token_lower and stem not in variations:
                variations.append(stem)
    
    # Check direct transliteration map
    if token_lower in TRANSLITERATION_MAP:
        variations.append(TRANSLITERATION_MAP[token_lower])
    
    # Check reverse (Devanagari -> English)
    for eng, dev in TRANSLITERATION_MAP.items():
        if token_lower == dev:
            variations.append(eng)
    
    # Also check stems against transliteration map
    for var in list(variations):
        if var in TRANSLITERATION_MAP and TRANSLITERATION_MAP[var] not in variations:
            variations.append(TRANSLITERATION_MAP[var])
        for eng, dev in TRANSLITERATION_MAP.items():
            if var == dev and eng not in variations:
                variations.append(eng)
    
    # Common spelling variations (Latin script)
    if re.search(r"[A-Za-z]", token_lower):
        replacements = [
            ("v", "w"), ("f", "ph"), ("s", "sh"), ("z", "j"),
            ("aa", "a"), ("ee", "i"), ("oo", "u")
        ]
        for old, new in replacements:
            if old in token_lower:
                variations.append(token_lower.replace(old, new))
    
    return list(set(v for v in variations if v))

def search_plants_fuzzy(query: str, limit: int = 5) -> List[Dict]:
    """
    Multi-strategy plant search:
      1. Synonym table (plant_synonyms) — exact & LIKE
      2. entity_i18n (multilingual names) — LIKE on name field
      3. Base-table multilingual columns (common_name_hi, common_name_mr)
      4. FTS5 full-text search
      5. Vector/embedding similarity (semantic search)
    Handles Devanagari tokens with automatic suffix stripping.
    """
    db = get_db()
    cur = db.cursor()

    tokens = _prioritized_tokens(query)
    if not tokens:
        return []

    all_results: List[Dict] = []
    seen_ids: set = set()

    def _add(row):
        pid = row["id"] if isinstance(row, dict) else row[0]
        if isinstance(row, dict):
            rid = row.get("id")
        else:
            rid = int(row["id"]) if "id" in row.keys() else int(row[0])
        if rid not in seen_ids:
            seen_ids.add(rid)
            all_results.append(dict(row))

    for token in tokens:
        if len(all_results) >= limit:
            break
        variations = normalize_query_token(token)

        for variant in variations[:5]:
            if len(all_results) >= limit:
                break

            # ── 1. plant_synonyms (existing) ──
            try:
                rows = cur.execute("""
                    SELECT DISTINCT p.*
                    FROM plant_synonyms ps
                    JOIN plants p ON p.id = ps.plant_id
                    WHERE LOWER(ps.synonym) LIKE ? OR LOWER(ps.synonym) LIKE ?
                    LIMIT ?
                """, (f"{variant}%", f"%{variant}%", limit)).fetchall()
                for r in rows:
                    _add(r)
            except Exception as e:
                _nlu_log.debug(f"[NLU] plant_synonyms search err: {e}")

            # ── 2. entity_i18n (multilingual name lookup — THE KEY FIX) ──
            try:
                rows = cur.execute("""
                    SELECT DISTINCT p.*
                    FROM entity_i18n ei
                    JOIN plants p ON p.id = ei.entity_id
                    WHERE ei.entity_type = 'plant'
                      AND ei.field = 'name'
                      AND (LOWER(ei.text) LIKE ? OR LOWER(ei.text) LIKE ?)
                    LIMIT ?
                """, (f"{variant}%", f"%{variant}%", limit)).fetchall()
                for r in rows:
                    _add(r)
            except Exception as e:
                _nlu_log.debug(f"[NLU] entity_i18n plant search err: {e}")

            # ── 3. Base-table multilingual columns ──
            try:
                rows = cur.execute("""
                    SELECT * FROM plants
                    WHERE LOWER(common_name_en) LIKE ?
                       OR LOWER(common_name_hi) LIKE ?
                       OR LOWER(common_name_mr) LIKE ?
                       OR LOWER(botanical_name) LIKE ?
                       OR LOWER(sanskrit_name) LIKE ?
                    LIMIT ?
                """, (f"%{variant}%", f"%{variant}%", f"%{variant}%",
                      f"%{variant}%", f"%{variant}%", limit)).fetchall()
                for r in rows:
                    _add(r)
            except Exception as e:
                _nlu_log.debug(f"[NLU] plants base-table search err: {e}")

    # ── 4. FTS5 (English tokens only — Devanagari may fail MATCH) ──
    if len(all_results) < limit:
        latin_tokens = [t for t in tokens[:3] if re.match(r'^[A-Za-z]+$', t)]
        if latin_tokens:
            fts_query = " OR ".join(latin_tokens)
            try:
                rows = cur.execute("""
                    WITH hits AS (
                      SELECT rowid AS id FROM plants_fts
                      WHERE plants_fts MATCH ?
                      LIMIT ?
                    )
                    SELECT p.* FROM hits h JOIN plants p ON p.id = h.id
                """, (fts_query, limit - len(all_results))).fetchall()
                for r in rows:
                    _add(r)
            except Exception as e:
                _nlu_log.debug(f"[NLU] plants_fts err: {e}")

    # ── 5. Vector / embedding semantic search (AI-powered) ──
    if len(all_results) < limit:
        try:
            from services.chat import _embed_384
            qvec = _embed_384(query)
            # Try per-language vec table first, then legacy
            for vtable in ("plant_vec_mr", "plant_vec_hi", "plant_vec_en", "plant_vec"):
                try:
                    id_col = "plant_id"
                    vec_rows = cur.execute(f"""
                        SELECT {id_col} AS id, distance
                        FROM {vtable}
                        WHERE embedding MATCH ?
                          AND k = ?
                    """, (qvec, limit * 2)).fetchall()
                    for vr in vec_rows:
                        vid = int(vr["id"]) if "id" in vr.keys() else int(vr[0])
                        dist = float(vr["distance"]) if "distance" in vr.keys() else float(vr[1])
                        if dist < 1.2 and vid not in seen_ids:  # reasonable similarity
                            plant_row = cur.execute("SELECT * FROM plants WHERE id=?", (vid,)).fetchone()
                            if plant_row:
                                d = dict(plant_row)
                                d["_vec_distance"] = dist
                                _add(d)
                    if all_results:
                        break  # found hits, stop checking other tables
                except Exception:
                    continue
        except Exception as e:
            _nlu_log.debug(f"[NLU] plant vec search err: {e}")

    cur.close()
    _nlu_log.debug(f"[NLU] search_plants_fuzzy({query!r}) → {len(all_results)} results")
    return all_results[:limit]

def search_diseases_fuzzy(query: str, limit: int = 5) -> List[Dict]:
    """
    Multi-strategy disease search:
      1. Synonym table (disease_synonyms) — exact & LIKE
      2. entity_i18n (multilingual names) — LIKE on name field
      3. Base-table multilingual columns (name_en, name_hi, name_mr)
      4. FTS5 full-text search
      5. Vector/embedding similarity (semantic search)
    Handles Devanagari tokens with automatic suffix stripping.
    """
    db = get_db()
    cur = db.cursor()

    tokens = _prioritized_tokens(query)
    if not tokens:
        return []

    all_results: List[Dict] = []
    seen_ids: set = set()

    def _add(row):
        if isinstance(row, dict):
            rid = row.get("id")
        else:
            rid = int(row["id"]) if "id" in row.keys() else int(row[0])
        if rid not in seen_ids:
            seen_ids.add(rid)
            all_results.append(dict(row))

    for token in tokens:
        if len(all_results) >= limit:
            break
        variations = normalize_query_token(token)

        for variant in variations[:5]:
            if len(all_results) >= limit:
                break

            # ── 1. disease_synonyms (existing) ──
            try:
                rows = cur.execute("""
                    SELECT DISTINCT d.*
                    FROM disease_synonyms ds
                    JOIN diseases d ON d.id = ds.disease_id
                    WHERE LOWER(ds.synonym) LIKE ? OR LOWER(ds.synonym) LIKE ?
                    LIMIT ?
                """, (f"{variant}%", f"%{variant}%", limit)).fetchall()
                for r in rows:
                    _add(r)
            except Exception as e:
                _nlu_log.debug(f"[NLU] disease_synonyms search err: {e}")

            # ── 2. entity_i18n (THE KEY FIX — search multilingual names) ──
            try:
                rows = cur.execute("""
                    SELECT DISTINCT d.*
                    FROM entity_i18n ei
                    JOIN diseases d ON d.id = ei.entity_id
                    WHERE ei.entity_type = 'disease'
                      AND ei.field = 'name'
                      AND (LOWER(ei.text) LIKE ? OR LOWER(ei.text) LIKE ?)
                    LIMIT ?
                """, (f"{variant}%", f"%{variant}%", limit)).fetchall()
                for r in rows:
                    _add(r)
            except Exception as e:
                _nlu_log.debug(f"[NLU] entity_i18n disease search err: {e}")

            # ── 3. Base-table multilingual columns ──
            try:
                rows = cur.execute("""
                    SELECT * FROM diseases
                    WHERE LOWER(name_en) LIKE ?
                       OR LOWER(name_hi) LIKE ?
                       OR LOWER(name_mr) LIKE ?
                    LIMIT ?
                """, (f"%{variant}%", f"%{variant}%", f"%{variant}%", limit)).fetchall()
                for r in rows:
                    _add(r)
            except Exception as e:
                _nlu_log.debug(f"[NLU] diseases base-table search err: {e}")

    # ── 4. FTS5 (English tokens) ──
    if len(all_results) < limit:
        latin_tokens = [t for t in tokens[:3] if re.match(r'^[A-Za-z]+$', t)]
        if latin_tokens:
            fts_query = " OR ".join(latin_tokens)
            try:
                rows = cur.execute("""
                    WITH hits AS (
                      SELECT rowid AS id FROM diseases_fts
                      WHERE diseases_fts MATCH ?
                      LIMIT ?
                    )
                    SELECT d.* FROM hits h JOIN diseases d ON d.id = h.id
                """, (fts_query, limit - len(all_results))).fetchall()
                for r in rows:
                    _add(r)
            except Exception as e:
                _nlu_log.debug(f"[NLU] diseases_fts err: {e}")

    # ── 5. Vector / embedding semantic search (AI-powered) ──
    if len(all_results) < limit:
        try:
            from services.chat import _embed_384
            qvec = _embed_384(query)
            for vtable in ("disease_vec_mr", "disease_vec_hi", "disease_vec_en", "disease_vec"):
                try:
                    id_col = "disease_id"
                    vec_rows = cur.execute(f"""
                        SELECT {id_col} AS id, distance
                        FROM {vtable}
                        WHERE embedding MATCH ?
                          AND k = ?
                    """, (qvec, limit * 2)).fetchall()
                    for vr in vec_rows:
                        vid = int(vr["id"]) if "id" in vr.keys() else int(vr[0])
                        dist = float(vr["distance"]) if "distance" in vr.keys() else float(vr[1])
                        if dist < 1.2 and vid not in seen_ids:
                            disease_row = cur.execute("SELECT * FROM diseases WHERE id=?", (vid,)).fetchone()
                            if disease_row:
                                d = dict(disease_row)
                                d["_vec_distance"] = dist
                                _add(d)
                    if all_results:
                        break
                except Exception:
                    continue
        except Exception as e:
            _nlu_log.debug(f"[NLU] disease vec search err: {e}")

    cur.close()
    _nlu_log.debug(f"[NLU] search_diseases_fuzzy({query!r}) → {len(all_results)} results")
    return all_results[:limit]

def extract_entities(text: str, text_en: str | None = None, prefer_en: bool = False) -> Tuple[List[Dict], List[Dict]]:
    """
    Extract plant and disease entities from query.
    Multi-strategy: searches BOTH original text AND English translation.
    Uses synonym tables, entity_i18n, base table columns, FTS, and vector search.
    """
    # Search on both original text AND English translation for maximum recall
    plants_orig = search_plants_fuzzy(text, limit=3)
    diseases_orig = search_diseases_fuzzy(text, limit=3)

    # If English translation available and different, search on that too
    if text_en and text_en.strip().lower() != (text or "").strip().lower():
        plants_en = search_plants_fuzzy(text_en, limit=3)
        diseases_en = search_diseases_fuzzy(text_en, limit=3)

        # Merge (deduplicate by id)
        seen_plant_ids = {p.get("id") for p in plants_orig}
        for p in plants_en:
            if p.get("id") not in seen_plant_ids:
                plants_orig.append(p)
                seen_plant_ids.add(p.get("id"))

        seen_disease_ids = {d.get("id") for d in diseases_orig}
        for d in diseases_en:
            if d.get("id") not in seen_disease_ids:
                diseases_orig.append(d)
                seen_disease_ids.add(d.get("id"))

    _nlu_log.debug(
        f"[NLU] extract_entities: plants={[p.get('common_name_en') for p in plants_orig[:3]]}, "
        f"diseases={[d.get('name_en') for d in diseases_orig[:3]]}"
    )
    return plants_orig[:3], diseases_orig[:3]

# Backward compatibility exports
__all__ = [
    'detect_language',
    'classify_intent', 
    'extract_entities',
    'search_plants_fuzzy',
    'search_diseases_fuzzy'
]
