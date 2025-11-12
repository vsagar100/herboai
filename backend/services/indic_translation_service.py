"""
High-level translation helpers that reuse the reference IndicTranslator
implementation without modifying it.
"""

from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Sequence, Union

import torch
from services.indic_trans2 import IndicTranslator

# Map short codes used across the app to IndicTrans2 tags
LANG_CODE_MAP = {
    "en": "eng_Latn",
    "hi": "hin_Deva",
    "mr": "mar_Deva",
    "bn": "ben_Beng",
    "gu": "guj_Gujr",
    "ta": "tam_Taml",
    "te": "tel_Telu",
    "kn": "kan_Knda",
    "ml": "mal_Mlym",
    "pa": "pan_Guru",
    "or": "ory_Orya",
    "as": "asm_Beng",
    "sa": "san_Deva",
}


def _lang_tag(lang: str) -> str:
    tag = LANG_CODE_MAP.get(lang.lower())
    if not tag:
        raise ValueError(f"Unsupported language code: {lang}")
    return tag


class IndicTranslationService:
    """
    Thin wrapper that holds three IndicTrans2 translators (one per direction)
    and exposes convenient helpers.
    """

    def __init__(self):
        self.models = {
            "en-indic": IndicTranslator("en-indic"),
            "indic-en": IndicTranslator("indic-en"),
           # "indic-indic": IndicTranslator("indic-indic"),
        }

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    def translate_text(self, text: str, src_lang: str, tgt_lang: str) -> str:
        if not text or src_lang == tgt_lang:
            return text
        model, src_tag, tgt_tag = self._select_route(src_lang, tgt_lang)
        return self._run_translation(model, text, src_tag, tgt_tag)

    def translate_batch(
        self, texts: Sequence[str], src_lang: str, tgt_lang: str
    ) -> List[str]:
        if src_lang == tgt_lang:
            return list(texts)
        model, src_tag, tgt_tag = self._select_route(src_lang, tgt_lang)
        return self._run_translation(model, list(texts), src_tag, tgt_tag)

    def to_en(self, text: str, src_lang: Optional[str] = None) -> str:
        lang = (src_lang or self.detect_lang(text)).lower()
        return text if lang == "en" else self.translate_text(text, lang, "en")

    def to_hi(self, text: str) -> str:
        return self.translate_text(text, "en", "hi")

    def to_mr(self, text: str) -> str:
        return self.translate_text(text, "en", "mr")

    def translate_values(
        self, payload: Union[Dict, List], src_lang: str, tgt_lang: str
    ) -> Union[Dict, List]:
        if src_lang == tgt_lang:
            return payload

        def _walk(value: Any) -> Any:
            if isinstance(value, str):
                stripped = value.strip()
                if not stripped:
                    return value
                return self.translate_text(stripped, src_lang, tgt_lang)
            if isinstance(value, list):
                return [_walk(v) for v in value]
            if isinstance(value, dict):
                return {k: _walk(v) for k, v in value.items()}
            return value

        return _walk(copy.deepcopy(payload))

    @staticmethod
    def detect_lang(text: str) -> str:
        if not text:
            return "en"
        devanagari = "\u0900-\u097F"
        if any("\u0900" <= ch <= "\u097F" for ch in text):
            mr_markers = {"कारण", "करा", "कृपा", "औषध", "मधुमेह"}
            return "mr" if any(tok in text for tok in mr_markers) else "hi"
        return "en"

    def _select_route(
        self, src_lang: str, tgt_lang: str
    ) -> tuple[IndicTranslator, str, str]:
        src = src_lang.lower()
        tgt = tgt_lang.lower()
        src_tag = _lang_tag(src_lang)
        tgt_tag = _lang_tag(tgt_lang)

        if src == "en" and tgt != "en":
            return self.models["en-indic"], src_tag, tgt_tag
        if tgt == "en" and src != "en":
            return self.models["indic-en"], src_tag, tgt_tag
        return self.models["indic-indic"], src_tag, tgt_tag

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _run_translation(
        self,
        model: IndicTranslator,
        sentences: Union[str, Sequence[str]],
        src_tag: str,
        tgt_tag: str,
    ) -> Union[str, List[str]]:
        if isinstance(sentences, str):
            items = [sentences]
            single = True
        else:
            items = list(sentences)
            single = False

        processed = [model.preprocess_text(s, src_tag, tgt_tag) for s in items]
        inputs = model.tokenizer(
            processed,
            truncation=True,
            padding="longest",
            return_tensors="pt",
            max_length=256,
        ).to(model.device)

        tgt_id = model.tokenizer.convert_tokens_to_ids(tgt_tag)
        if tgt_id is None and hasattr(model.tokenizer, "lang_code_to_id"):
            tgt_id = model.tokenizer.lang_code_to_id.get(tgt_tag)
        if tgt_id is None:
            raise ValueError(f"Unknown target tag: {tgt_tag}")

        with torch.no_grad():
            generated = model.model.generate(
                **inputs,
                forced_bos_token_id=tgt_id,
                min_length=0,
                max_length=256,
                num_beams=5,
                num_return_sequences=1,
                use_cache=False,
            )

        decoded = model.tokenizer.batch_decode(
            generated, skip_special_tokens=True, clean_up_tokenization_spaces=True
        )
        cleaned = [model.postprocess_text(t) for t in decoded]
        return cleaned[0] if single else cleaned


_SERVICE: Optional[IndicTranslationService] = None


def get_indic_translation_service() -> IndicTranslationService:
    global _SERVICE
    if _SERVICE is None:
        _SERVICE = IndicTranslationService()
    return _SERVICE
