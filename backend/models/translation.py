import argostranslate.translate

# Simple Unicode-based language detection
def detect_language(text):
    # Hindi Unicode range
    if any("\u0900" <= ch <= "\u097F" for ch in text):
        return "hi"
    return "en"

def translate(text, from_lang="en", to_lang="hi"):
    if from_lang == to_lang:
        return text
    return argostranslate.translate.translate(text, from_lang, to_lang)

def translate_to_english(text):
    lang = detect_language(text)
    if lang != "en":
        return translate(text, lang, "en")
    return text

def translate_from_english(text, target_lang):
    if target_lang != "en":
        return translate(text, "en", target_lang)
    return text
