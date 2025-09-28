# services/translation_service.py
import logging
logger = logging.getLogger(__name__)

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
