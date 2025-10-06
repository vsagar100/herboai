"""Translation helpers for multilingual chat support."""

import logging
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# Devanagari range to auto-detect Hindi/Marathi input when the
# frontend has not explicitly shared the language code.
DEVANAGARI_RANGE = range(0x0900, 0x097F + 1)


def _has_devanagari(text: str) -> bool:
    return any(ord(ch) in DEVANAGARI_RANGE for ch in (text or ""))


class TranslationService:
    """Lightweight translation facade used by the chatbot.

    The service favours on-device processing.  When the optional
    ``transformers`` dependency (and therefore MarianMT models) is not
    available we gracefully fall back to returning the original text so
    the rest of the pipeline can keep working.
    """

    _MODEL_MAP: Dict[Tuple[str, str], str] = {
        ("en", "hi"): "Helsinki-NLP/opus-mt-en-hi",
        ("en", "mr"): "Helsinki-NLP/opus-mt-en-mr",
        ("hi", "en"): "Helsinki-NLP/opus-mt-hi-en",
        ("mr", "en"): "Helsinki-NLP/opus-mt-mr-en",
    }

    def __init__(self) -> None:
        self._pipelines: Dict[Tuple[str, str], object] = {}
        try:
            from transformers import pipeline  # type: ignore

            self._pipeline_factory = pipeline
        except Exception as exc:  # pragma: no cover - optional dependency
            logger.warning("transformers not available for translation: %s", exc)
            self._pipeline_factory = None

    # ------------------------------------------------------------------
    # Translation helpers
    # ------------------------------------------------------------------
    def _get_pipe(self, source: str, target: str):
        if self._pipeline_factory is None:
            return None

        key = (source, target)
        if key in self._pipelines:
            return self._pipelines[key]

        model_name = self._MODEL_MAP.get(key)
        if not model_name:
            return None

        try:
            pipe = self._pipeline_factory("translation", model=model_name)
            self._pipelines[key] = pipe
            return pipe
        except Exception as exc:  # pragma: no cover - model download failures
            logger.warning("Failed to load translation model %s: %s", model_name, exc)
            return None

    def translate_out(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        """Translate an English answer into the requested language."""

        target_lang = (target_lang or "en").lower()
        source_lang = (source_lang or "en").lower()

        if not text or target_lang == source_lang or target_lang == "en":
            return text

        pipe = self._get_pipe(source_lang, target_lang)
        if pipe is None:
            return text

        try:
            out = pipe(text, max_length=1024)
            return out[0]["translation_text"]
        except Exception as exc:
            logger.warning("translate_out failed: %s", exc)
            return text

    def translate_in(self, text: str, source_lang: Optional[str]) -> str:
        """Translate user input into English for downstream processing."""

        if not text:
            return text

        lang = (source_lang or "").lower().strip()
        if not lang:
            lang = "hi" if _has_devanagari(text) else "en"

        if lang in ("en", ""):
            return text

        pipe = self._get_pipe(lang, "en")
        if pipe is None:
            return text

        try:
            out = pipe(text, max_length=1024)
            return out[0]["translation_text"]
        except Exception:
            return text

    # ------------------------------------------------------------------
    # Keyword normalisation for multilingual queries
    # ------------------------------------------------------------------
    def normalize_symptom_terms(self, text: str, lang: str) -> List[str]:
        """Return a small set of English keywords detected in ``text``.

        The method helps the retrieval layer reuse the same symptom and
        herb vocab regardless of whether the visitor types in English,
        Hindi or Marathi.  Only compact, high-signal vocab is mapped so
        that we do not introduce too much noise.
        """

        text = (text or "").lower()
        lang = (lang or "").lower()

        hi: Dict[str, str] = {
            "खांसी": "cough",
            "जुकाम": "cold",
            "बुखार": "fever",
            "दर्द": "pain",
            "अपचन": "indigestion",
            "उल्टी": "nausea",
            "मतली": "nausea",
            "तना": "stress",
            "तनाव": "stress",
            "नींद": "sleep",
            "अनिद्रा": "insomnia",
            "त्वचा": "skin",
            "मधुमेह": "diabetes",
            "घाव": "wound",
            "घाव भरना": "wound healing",
            "पाचन": "digestion",
            "वात": "vata",
            "पित्त": "pitta",
            "कफ": "kapha",
            "तुलसी": "tulsi",
            "होली बेसिल": "tulsi",
            "होलि बेसिल": "tulsi",
        }

        mr: Dict[str, str] = {
            "खोकला": "cough",
            "सर्दी": "cold",
            "ताप": "fever",
            "वेदना": "pain",
            "अपचन": "indigestion",
            "उलटी": "nausea",
            "मळमळ": "nausea",
            "तणाव": "stress",
            "झोप": "sleep",
            "अनिद्रा": "insomnia",
            "त्वचा": "skin",
            "मधुमेह": "diabetes",
            "जखम": "wound",
            "जखम भरणे": "wound healing",
            "पचन": "digestion",
            "वात": "vata",
            "पित्त": "pitta",
            "कफ": "kapha",
            "तुळस": "tulsi",
            "तुलसी": "tulsi",
        }

        table = hi if lang == "hi" else mr if lang == "mr" else {}
        terms = {english for native, english in table.items() if native in text}

        transliteration_hits: Dict[str, str] = {
            "tulsi": "tulsi",
            "amla": "amla",
            "ashwagandha": "ashwagandha",
            "neem": "neem",
            "haldi": "turmeric",
            "halad": "turmeric",
            "haridra": "turmeric",
            "adrak": "ginger",
            "sunth": "ginger",
            "khansi": "cough",
            "jukam": "cold",
            "apchan": "indigestion",
        }

        for key, value in transliteration_hits.items():
            if key in text:
                terms.add(value)

        return sorted(terms)

