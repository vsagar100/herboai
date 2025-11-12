# api/nlu_optimized.py
"""
Optimized NLU for multilingual queries
- Fast language detection
- Smart entity extraction with synonym matching
- No translation needed for entity extraction
"""
import re
from typing import Dict, List, Tuple
from db import get_db

# Language detection patterns
DEVANAGARI_RE = re.compile(r"[\u0900-\u097F]")

# Marathi-specific markers
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

def detect_language(text: str) -> str:
    """
    Fast language detection
    Returns: 'en', 'hi', or 'mr'
    """
    if not text:
        return "en"
    
    t = text.lower()
    
    # Check for Devanagari script
    if not DEVANAGARI_RE.search(t):
        return "en"
    
    # Count Marathi vs Hindi markers
    mr_count = sum(1 for marker in MR_MARKERS if marker in t)
    hi_count = sum(1 for marker in HI_MARKERS if marker in t)
    
    # Marathi if more MR markers or specific words
    if mr_count > hi_count or any(word in t for word in ["गुळवेल", "तुळस", "आवळा", "हिरडा"]):
        return "mr"
    
    return "hi"

def classify_intent(text: str) -> str:
    """
    Classify user intent based on query patterns
    Returns: remedy_lookup, plant_info, preparation_info, lifestyle_advice, none
    """
    t = text.lower()
    
    # Preparation queries
    prep_patterns = [
        "how to prepare", "kwatha", "decoction", "kashaya", "काढा", "काढे",
        "churna", "powder", "चूर्ण", "oil", "taila", "तेल", "घृत",
        "dosage", "dose", "मात्रा", "कसे बनवायचे", "कैसे बनाएं"
    ]
    if any(p in t for p in prep_patterns):
        return "preparation_info"
    
    # Plant info queries
    plant_patterns = [
        "what is", "about", "uses of", "benefits", "properties",
        "बद्दल", "के बारे", "फायदे", "गुण", "उपयोग", "माहिती"
    ]
    if any(p in t for p in plant_patterns):
        return "plant_info"
    
    # Remedy/disease queries (most common)
    remedy_patterns = [
        "i have", "i am having", "suffering from", "remedy for",
        "treatment for", "herbs for", "cure for", "help with",
        "मला", "मुझे", "साठी", "के लिए", "उपचार", "औषधी"
    ]
    disease_keywords = [
        "diabetes", "मधुमेह", "bp", "pressure", "cough", "खांसी",
        "cold", "सर्दी", "fever", "ज्वर", "pain", "दुखी", "दर्द",
        "acidity", "gas", "गॅस", "constipation", "कब्ज"
    ]
    
    if any(p in t for p in remedy_patterns) or any(k in t for k in disease_keywords):
        return "remedy_lookup"
    
    return "none"

def normalize_query_token(token: str) -> List[str]:
    """
    Normalize a token to handle phonetic variations
    Returns list of possible variations
    """
    token_lower = token.lower().strip()
    
    # Return original + any known transliterations
    variations = [token_lower]
    
    # Check direct transliteration map
    if token_lower in TRANSLITERATION_MAP:
        variations.append(TRANSLITERATION_MAP[token_lower])
    
    # Check reverse (Devanagari -> English)
    for eng, dev in TRANSLITERATION_MAP.items():
        if token_lower == dev:
            variations.append(eng)
    
    # Common spelling variations
    replacements = [
        ("v", "w"), ("f", "ph"), ("s", "sh"), ("z", "j"),
        ("aa", "a"), ("ee", "i"), ("oo", "u")
    ]
    for old, new in replacements:
        if old in token_lower:
            variations.append(token_lower.replace(old, new))
    
    return list(set(variations))

def search_plants_fuzzy(query: str, limit: int = 5) -> List[Dict]:
    """
    Fuzzy search for plants with synonym matching
    """
    db = get_db()
    cur = db.cursor()
    
    tokens = re.findall(r"[A-Za-z\u0900-\u097F]+", query.lower())
    if not tokens:
        return []
    
    # Try each token with variations
    all_results = []
    seen_ids = set()
    
    for token in tokens:
        if len(token) < 3:  # Skip very short tokens
            continue
        
        variations = normalize_query_token(token)
        
        for variant in variations[:3]:  # Limit variations to prevent slowdown
            # 1. Try synonym table first (exact/prefix match)
            rows = cur.execute("""
                SELECT DISTINCT p.*
                FROM plant_synonyms ps
                JOIN plants p ON p.id = ps.plant_id
                WHERE ps.synonym LIKE ? OR ps.synonym LIKE ?
                LIMIT ?
            """, (f"{variant}%", f"%{variant}%", limit)).fetchall()
            
            for row in rows:
                if row["id"] not in seen_ids:
                    all_results.append(dict(row))
                    seen_ids.add(row["id"])
            
            if len(all_results) >= limit:
                break
        
        if len(all_results) >= limit:
            break
    
    # 2. If still not enough, try FTS
    if len(all_results) < limit:
        fts_query = " OR ".join(tokens[:3])  # Limit to first 3 tokens
        try:
            rows = cur.execute("""
                WITH hits AS (
                  SELECT rowid AS id FROM plants_fts
                  WHERE plants_fts MATCH ?
                  LIMIT ?
                )
                SELECT p.* FROM hits h JOIN plants p ON p.id = h.id
            """, (fts_query, limit - len(all_results))).fetchall()
            
            for row in rows:
                if row["id"] not in seen_ids:
                    all_results.append(dict(row))
                    seen_ids.add(row["id"])
        except:
            pass  # FTS might fail on some queries
    
    cur.close()
    return all_results[:limit]

def search_diseases_fuzzy(query: str, limit: int = 5) -> List[Dict]:
    """
    Fuzzy search for diseases with synonym matching
    """
    db = get_db()
    cur = db.cursor()
    
    tokens = re.findall(r"[A-Za-z\u0900-\u097F]+", query.lower())
    if not tokens:
        return []
    
    all_results = []
    seen_ids = set()
    
    for token in tokens:
        if len(token) < 3:
            continue
        
        variations = normalize_query_token(token)
        
        for variant in variations[:3]:
            # 1. Try synonym table
            rows = cur.execute("""
                SELECT DISTINCT d.*
                FROM disease_synonyms ds
                JOIN diseases d ON d.id = ds.disease_id
                WHERE ds.synonym LIKE ? OR ds.synonym LIKE ?
                LIMIT ?
            """, (f"{variant}%", f"%{variant}%", limit)).fetchall()
            
            for row in rows:
                if row["id"] not in seen_ids:
                    all_results.append(dict(row))
                    seen_ids.add(row["id"])
            
            if len(all_results) >= limit:
                break
        
        if len(all_results) >= limit:
            break
    
    # 2. Try FTS if needed
    if len(all_results) < limit:
        fts_query = " OR ".join(tokens[:3])
        try:
            rows = cur.execute("""
                WITH hits AS (
                  SELECT rowid AS id FROM diseases_fts
                  WHERE diseases_fts MATCH ?
                  LIMIT ?
                )
                SELECT d.* FROM hits h JOIN diseases d ON d.id = h.id
            """, (fts_query, limit - len(all_results))).fetchall()
            
            for row in rows:
                if row["id"] not in seen_ids:
                    all_results.append(dict(row))
                    seen_ids.add(row["id"])
        except:
            pass
    
    cur.close()
    return all_results[:limit]

def extract_entities(text: str, text_en: str | None = None, prefer_en: bool = False) -> Tuple[List[Dict], List[Dict]]:
    """
    Extract plant and disease entities from query
    Works on original text (no translation needed)
    """
    query = (text_en if prefer_en and text_en else text) or ""
    
    # Use fuzzy search which handles multilingual internally
    plants = search_plants_fuzzy(query, limit=3)
    diseases = search_diseases_fuzzy(query, limit=3)
    
    return plants, diseases

# Backward compatibility exports
__all__ = [
    'detect_language',
    'classify_intent', 
    'extract_entities',
    'search_plants_fuzzy',
    'search_diseases_fuzzy'
]