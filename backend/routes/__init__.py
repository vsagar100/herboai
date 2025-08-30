import re
import unicodedata

# Minimal normalizer for multilingual queries (en/hi/mr)
def _normalize_text(text: str) -> str:
    s = text.strip().lower()
    s = unicodedata.normalize("NFKC", s)
    # collapse spaces/punct
    s = re.sub(r"\s+", " ", s)
    # common transliteration-ish fixes not to be too aggressive
    return s
