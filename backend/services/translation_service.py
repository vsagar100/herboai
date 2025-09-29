# services/translation_service.py
import logging
logger = logging.getLogger(__name__)

# ADD near the top (after imports)
DEVANAGARI_RANGE = range(0x0900, 0x097F + 1)

def _has_devanagari(text: str) -> bool:
    return any(ord(ch) in DEVANAGARI_RANGE for ch in (text or ""))

class TranslationService:
    """
    Best-effort translator. Tries MarianMT (transformers).
    Falls back to returning the English text unchanged if model load fails.
    """
    def __init__(self):
        self.models = {}  # cache {("en","hi"): pipeline, ...}
        try:
            from transformers import pipeline
            self.pipeline_factory = pipeline
        except Exception as e:
            logger.warning(f"transformers not available for translation: {e}")
            self.pipeline_factory = None

    def _get_pipe(self, src: str, tgt: str):
        if self.pipeline_factory is None:
            return None
        key = (src, tgt)
        if key in self.models:
            return self.models[key]
        # MarianMT models (lightweight) – will download on first use
        model_map = {
            ("en", "hi"): "Helsinki-NLP/opus-mt-en-hi",
            ("en", "mr"): "Helsinki-NLP/opus-mt-en-mr",
            ("hi", "en"): "Helsinki-NLP/opus-mt-hi-en",
            ("mr", "en"): "Helsinki-NLP/opus-mt-mr-en",
        }
        name = model_map.get(key)
        if not name:
            return None
        try:
            pipe = self.pipeline_factory("translation", model=name)
            self.models[key] = pipe
            return pipe
        except Exception as e:
            logger.warning(f"Failed to load translation model {name}: {e}")
            return None

    def translate_out(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        target_lang = (target_lang or "en").lower()
        if target_lang == source_lang or target_lang == "en":
            return text
        pipe = self._get_pipe(source_lang, target_lang)
        if pipe is None:
            return text  # fallback: keep English
        try:
            out = pipe(text, max_length=1024)
            return out[0]["translation_text"]
        except Exception as e:
            logger.warning(f"translate_out failed: {e}")
            return text
    
    def translate_in(self, text: str, source_lang: str | None) -> str:
        """
        Translate user query INTO English for retrieval.
        If models unavailable, just return text (best-effort).
        """
        if not text:
            return text
        lang = (source_lang or "").lower().strip()
        if not lang:
            # heuristic: devanagari -> default to hi
            lang = "hi" if _has_devanagari(text) else "en"

        if lang in ("en", ""):
            return text

        # Prefer explicit pair; else heuristic
        model_key = (lang, "en")
        pipe = self._get_pipe(*model_key)
        if pipe is None:
            return text
        try:
            out = pipe(text, max_length=1024)
            return out[0]["translation_text"]
        except Exception:
            return text


    def normalize_symptom_terms(self, text: str, lang: str) -> list[str]:
        """
        Map common HI/MR symptom words to EN tokens for keyword retrieval.
        Keeps list small & high-signal.
        """
        t = (text or "").lower()

        # Hindi -> English
        hi = {
            "खांसी": "cough", "जुकाम": "cold", "बुखार": "fever", "दर्द": "pain",
            "अपचन": "indigestion", "उल्टी": "nausea", "मतली": "nausea",
            "तना": "stress", "तनाव": "stress", "नींद": "sleep", "अनिद्रा": "insomnia",
            "त्वचा": "skin", "मधुमेह": "diabetes", "घाव": "wound", "घाव भरना": "wound healing",
            "पाचन": "digestion", "वात": "vata", "पित्त": "pitta", "कफ": "kapha",
            "तुलसी": "tulsi", "होलि बेसिल": "tulsi"
        }

        # Marathi -> English
        mr = {
            "खोकला": "cough", "सर्दी": "cold", "ताप": "fever", "वेदना": "pain",
            "अपचन": "indigestion", "उलटी": "nausea", "मळमळ": "nausea",
            "तणाव": "stress", "झोप": "sleep", "अनिद्रा": "insomnia",
            "त्वचा": "skin", "मधुमेह": "diabetes", "जखम": "wound", "जखम भरणे": "wound healing",
            "पचन": "digestion", "वात": "vata", "पित्त": "pitta", "कफ": "kapha",
            "तुळस": "tulsi", "तुलसी": "tulsi"
        }

        table = hi if lang == "hi" else (mr if lang == "mr" else {})
        terms = {v for k, v in table.items() if k in t}

        # Easy english keywords derived from transliterations users often type
        translit_hits = {
            "tulsi": "tulsi", "amla": "amla", "ashwagandha": "ashwagandha", "neem": "neem",
            "haldi": "turmeric", "halad": "turmeric", "haridra": "turmeric", "adrak": "ginger",
            "sunth": "ginger",
            "khansi": "cough", "jukam": "cold", "apchan": "indigestion"
        }
        for k, v in translit_hits.items():
            if k in t:
                terms.a

