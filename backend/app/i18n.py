from langdetect import detect

try:
    import argostranslate.package
    import argostranslate.translate
    _HAS_ARGOS = True
except Exception:
    _HAS_ARGOS = False

LANG_MAP = {"en": "en", "hi": "hi", "mr": "mr"}

def detect_lang(text: str) -> str:
    try:
        code = detect(text)
        return "hi" if code.startswith("hi") else ("mr" if code.startswith("mr") else "en")
    except Exception:
        return "en"

# Argos helper (optional); requires language packs installed separately
#   argos-translate-cli --from-lang en --to-lang hi --install

def translate(text: str, src: str, tgt: str) -> str:
    if src == tgt:
        return text
    if not _HAS_ARGOS:
        return text  # fallback: return original if Argos not present
    try:
        return argostranslate.translate.translate(text, src, tgt)
    except Exception:
        return text