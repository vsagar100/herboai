"""
High-level translation helpers that reuse the reference IndicTranslator
implementation without modifying it.
"""

from __future__ import annotations

import copy
import os
from functools import lru_cache
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


# ----------------------------
# Translation Cache (LRU)
# ----------------------------
# Caches only DIRECT routes (en->hi/mr or hi/mr->en). Indic-to-Indic still goes via-English.
# This gives a big speedup for repeated queries / repeated chunks.
_TRANSLATION_CACHE_MAXSIZE = int(os.getenv("TRANSLATION_CACHE_MAXSIZE", "4096"))


@lru_cache(maxsize=_TRANSLATION_CACHE_MAXSIZE)
def _cached_direct_translate(text: str, src_lang: str, tgt_lang: str) -> str:
    svc = get_indic_translation_service()
    # Safety: keep cache bounded to avoid huge memory use for very long texts
    if len(text) > 2000:
        return svc._direct_translate_uncached(text, src_lang, tgt_lang)
    return svc._direct_translate_uncached(text, src_lang, tgt_lang)


class IndicTranslationService:
    """
    Thin wrapper that holds the publicly available IndicTrans2 translators
    (en→indic and indic→en) and exposes convenient helpers.
    """

    def __init__(self):
        self.models = {
            "en-indic": IndicTranslator("en-indic"),
            "indic-en": IndicTranslator("indic-en"),
        }

    # ------------------------------------------------------------------
    # Core helpers
    # ------------------------------------------------------------------

    def _direct_translate_uncached(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """
        Direct single-hop translation where either src or tgt is English.
        This is the expensive model call that we cache.
        """
        model, src_tag, tgt_tag = self._select_route(src_lang, tgt_lang)
        return self._run_translation(model, text, src_tag, tgt_tag)

    def translate_text(self, text: str, src_lang: str, tgt_lang: str) -> str:
        if not text or src_lang == tgt_lang:
            return text

        # Indic -> Indic uses via-English routing
        if src_lang != "en" and tgt_lang != "en":
            interim = self.translate_text(text, src_lang, "en")
            return self.translate_text(interim, "en", tgt_lang)

        # Direct route (en<->hi/mr): cached
        return _cached_direct_translate(text, src_lang, tgt_lang)

    def translate_batch(self, texts: Sequence[str], src_lang: str, tgt_lang: str) -> List[str]:
        if src_lang == tgt_lang:
            return list(texts)
        if src_lang != "en" and tgt_lang != "en":
            interim = self.translate_batch(texts, src_lang, "en")
            return self.translate_batch(interim, "en", tgt_lang)
        model, src_tag, tgt_tag = self._select_route(src_lang, tgt_lang)
        return self._run_translation(model, list(texts), src_tag, tgt_tag)

    def to_en(self, text: str, src_lang: Optional[str] = None) -> str:
        lang = (src_lang or self.detect_lang(text)).lower()
        return text if lang == "en" else self.translate_text(text, lang, "en")

    def to_hi(self, text: str) -> str:
        return self.translate_text(text, "en", "hi")

    def to_mr(self, text: str) -> str:
        return self.translate_text(text, "en", "mr")

    def translate_values(self, payload: Union[Dict, List], src_lang: str, tgt_lang: str) -> Union[Dict, List]:
        if src_lang == tgt_lang:
            return payload

        def _translate_str(text: str) -> str:
            stripped = text.strip()
            if not stripped:
                return text
            return self.translate_text(stripped, src_lang, tgt_lang)

        def _walk(value: Any) -> Any:
            if isinstance(value, str):
                return _translate_str(value)
            if isinstance(value, list):
                # Translate homogeneous string lists in a batch to avoid
                # repeated model calls and reduce latency.
                if all(isinstance(v, str) or v is None for v in value):
                    strings = [v for v in value if isinstance(v, str) and v.strip()]
                    translated = iter(self.translate_batch(strings, src_lang, tgt_lang) if strings else [])
                    out: List[Any] = []
                    for v in value:
                        if isinstance(v, str) and v.strip():
                            out.append(next(translated))
                        else:
                            out.append(v)
                    return out
                return [_walk(v) for v in value]
            if isinstance(value, dict):
                return {k: _walk(v) for k, v in value.items()}
            return value

        return _walk(copy.deepcopy(payload))

    @staticmethod
    def detect_lang(text: str, lang_hint: str | None = None) -> str:
        """
        Robust, zero-dependency detector for en/hi/mr:
        - Non-Devanagari -> 'en'
        - Devanagari -> score Hindi vs Marathi using lexicons + morphology
        - Optional `lang_hint` can steer decision if it matches script
        Returns: 'en' | 'hi' | 'mr'
        """
        if not text or not text.strip():
            return "en"

        raw = text.strip()
        cleaned = raw.lstrip(" .,:;|/\\-—–·*#\u200c\u200b")

        # 0) Script probe
        def has_devanagari(s: str) -> bool:
            return any("\u0900" <= ch <= "\u097F" for ch in s)

        if not has_devanagari(cleaned):
            return "en"

        # 1) If caller provided a hint and it matches the script, trust it
        if lang_hint in {"hi", "mr"}:
            return lang_hint

        # 2) Tokenize (very light)
        import re

        toks = [t for t in re.split(r"[^\w\u0900-\u097F]+", cleaned) if t]

        # 3) High-signal lexicons (small but precise)
        #    IMPORTANT: keep shared/medical/ayurveda terms in NEUTRAL to avoid flip-flops.
        HINDI_ONLY = {
            # core Hindi function words
            "क्या", "और", "में","है","नहीं","के","लिए","यह","वह","इस","उस","इन","उन","कब","कहाँ","कौन",
            "किस","किसे","किसका","किसकी","किसके","कैसे","क्यों","क्यूँ","कृपया","बताइए","बताएं","बताइये","बताओ",
            "को","से","पर","तक","बिना","सहित","द्वारा","बारे","बारेमें","हैं","था","थे","थी","हुआ","हुई","हुए","चाहिए",
            "चाहता","चाहती","वाला","वाले","वाली",
        }

        MARATHI_ONLY = {
            # Marathi function words / pronouns
            "काय","आणि","मध्ये","आहे","नाही","किंवा","होय","कधी","कसा","कसे","किती","कुठे","कोण","मला","तुला",
            "आपल्याला","त्यांना","हे","ते","ही","तो","ती","त्या","यात","त्यात","इथे","तिथे","साठी","कडून","कडे","पासून",
            "पर्यंत","मधून","वर","खाली","पण","मात्र","म्हणून","तरी","होतो","होते","होतात","होईल","होणार","करतो",
            "करते","करतात","करणं","करायला","करायचं","करायचे","घ्यावं","घ्यावे","घ्या","प्यावं","खावं","वाढवणारे","रोगप्रतिकारक",
            "रोग प्रतिकार","शक्ती","त्रास","डोकं","पोट","पोटदुखी",
        }

        # Words shared across both (neutral): ignore in scoring
        NEUTRAL = {
            # Ayurveda/health topic words (shared)
            "रोग","आयुर्वेद","आयुर्वेदिक","उपाय","औषध","दवा","इलाज","उपचार","लक्षण","मात्रा","सेवन","उपयोग",
            "रक्तदाब","रक्तचाप","फायदा","फायदे","तोटा","नुकसान","दर्द","बुखार","सर्दी","खांसी","जुकाम","गैस","पाचन",
            "शुगर","डायबिटीज","काढा","चूर्ण","वटी","लेप","घृत","तेल",        
            }

        # 4) Morphology patterns (true suffixes only; keep postpositions as tokens)
        MR_SUFFIXES = (
           "णारा","णारे","णारी","ण्यात","ताना","तील","ल्यावर","ल्याने","ल्यास","ण्याची","ण्याचे","ण्याला",
        )
        HI_SUFFIXES = (
            "वाला","वाले","वाली","एगा","एगी","एंगे","इए","इये",
        )

        # 5) Score hits (weighted)
        hi_score = 0
        mr_score = 0

        for w in toks:
            if w in NEUTRAL:
                continue

            if w in HINDI_ONLY:
                hi_score += 2
            if w in MARATHI_ONLY:
                mr_score += 2

            # suffixes (light nudge)
            if w.endswith(MR_SUFFIXES):
                mr_score += 1
            if w.endswith(HI_SUFFIXES):
                hi_score += 1

        # 6) Extra n-gram nudges (short inputs benefit)
        s = cleaned
        if "प्रतिरोधक क्षमता" in s:
            hi_score += 3
        if ("रोग प्रतिकार शक्ती" in s) or ("रोगप्रतिकारक शक्ती" in s) or ("वाढवणारे" in s):
            mr_score += 3

        # 7) Decide with confidence thresholds
        if mr_score >= hi_score + 2:
            return "mr"
        if hi_score >= mr_score + 2:
            return "hi"

        # soft ties — Marathi giveaways
        if any(g in s for g in ("वाढवणारे", "रोग प्रतिकार शक्ती", "रोगप्रतिकारक", "साठी", "कडून", "कडे", "होईल", "करतो")):
            return "mr"

        # final tie-break: prefer Hindi
        return "hi"

    def _select_route(self, src_lang: str, tgt_lang: str) -> tuple[IndicTranslator, str, str]:
        src = src_lang.lower()
        tgt = tgt_lang.lower()
        src_tag = _lang_tag(src_lang)
        tgt_tag = _lang_tag(tgt_lang)

        if src == "en" and tgt != "en":
            return self.models["en-indic"], src_tag, tgt_tag
        if tgt == "en" and src != "en":
            return self.models["indic-en"], src_tag, tgt_tag
        raise ValueError("Direct Indic-to-Indic translation requires via-English routing.")

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
                num_beams=1,
                num_return_sequences=1,
                use_cache=True,
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
