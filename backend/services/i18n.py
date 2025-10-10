# services/i18n.py
import os, json, requests
from typing import Optional

ADAPTER = os.getenv("I18N_ADAPTER", "none").lower()
LIBRE_URL = os.getenv("LIBRE_TRANSLATE_URL", "").strip()

def pick_locale(data_json: str, locale: str, fallback="en") -> dict:
    try:
        data = json.loads(data_json or "{}")
    except Exception:
        data = {}
    return data.get(locale) or data.get(fallback) or {}

def maybe_translate(text: str, target_lang: str) -> str:
    if not text or target_lang in ("", "en") or ADAPTER == "none":
        return text
    if ADAPTER == "libre" and LIBRE_URL:
        try:
            r = requests.post(LIBRE_URL, data={"q": text, "source": "auto", "target": target_lang, "format": "text"}, timeout=6)
            if r.ok:
                return r.json().get("translatedText", text)
        except Exception:
            return text
    return text
