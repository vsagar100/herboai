from __future__ import annotations
from typing import Dict

from utils.i18n import upsert_i18n
from services.indexer import rebuild_fts_for_entity, rebuild_vec_for_entity
from services.indic_translation_service import translate_en_to_hi, translate_en_to_mr

# Fields that are user-facing and should be translated
TRANSLATABLE_FIELDS = {
    "plant": [
        "name", "description", "parts_used", "benefits", "dosage", "precautions"
    ],
    "disease": [
        "name", "description", "symptoms", "causes", "precautions"
    ],
    "preparation": [
        "name", "description", "steps", "dosage", "precautions"
    ],
}

def _translate(text: str, lang: str) -> str:
    if not text:
        return ""
    if lang == "hi":
        return translate_en_to_hi(text)
    if lang == "mr":
        return translate_en_to_mr(text)
    return text

def admin_save_with_i18n(
    entity_type: str,
    entity_id: int,
    en_fields: Dict[str, str],
    *,
    source: str = "manual"
) -> None:
    """
    Called AFTER canonical entity row is saved.
    - Stores English as verified
    - Auto-translates to hi/mr as auto
    - Rebuilds FTS + vec for that entity
    """

    fields = TRANSLATABLE_FIELDS.get(entity_type, [])

    # 1) English (verified)
    for field in fields:
        text = en_fields.get(field)
        if text:
            upsert_i18n(
                entity_type,
                entity_id,
                lang="en",
                field=field,
                text=text,
                status="verified",
                source=source,
            )

    # 2) Auto translate to Hindi / Marathi
    for lang in ("hi", "mr"):
        for field in fields:
            text = en_fields.get(field)
            if not text:
                continue
            translated = _translate(text, lang)
            if translated:
                upsert_i18n(
                    entity_type,
                    entity_id,
                    lang=lang,
                    field=field,
                    text=translated,
                    status="auto",
                    source="indictrans2",
                )

    # 3) Rebuild indexes (single-path guarantee)
    rebuild_fts_for_entity(entity_type, entity_id)
    rebuild_vec_for_entity(entity_type, entity_id)
