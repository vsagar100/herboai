from __future__ import annotations
import logging
from typing import Dict

from config import Config
from utils.i18n import upsert_i18n
from services.indexer import rebuild_fts_for_entity, rebuild_vec_for_entity
from services.indic_translation_service import translate_en_to_hi, translate_en_to_mr

log = logging.getLogger("admin_i18n")

# Fields that are user-facing and should be translated
# Maps field names as they appear in the database
TRANSLATABLE_FIELDS = {
    "plant": [
        "name",                    # from common_name_en
        "description",
        "therapeutic_actions",
        "parts_used",
        "rasa",
        "guna",
        "virya",
        "vipaka"
    ],
    "disease": [
        "name",                    # from name_en
        "description",
        "symptoms",
        "causes",
        "prevention_tips"
    ],
    "preparation": [
        "name",                    # from name_en
        "preparation_steps",
        "dosage_json",
        "timing",
        "anupana",
        "notes"
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
    - Stores English as verified in entity_i18n
    - Auto-translates to hi/mr as auto  (if ENABLE_I18N_TRANSLATION is True)
    - Rebuilds FTS + vec for that entity (if ENABLE_I18N_TRANSLATION is True)

    Callers pass en_fields using i18n field names as keys:
      Plant:       {name, description, therapeutic_actions, parts_used, rasa, guna, virya, vipaka}
      Disease:     {name, description, symptoms, causes, prevention_tips}
      Preparation: {name, preparation_steps, dosage_json, timing, anupana, notes}
    """

    if not getattr(Config, "ENABLE_I18N_TRANSLATION", False):
        log.info("[i18n] ENABLE_I18N_TRANSLATION is OFF — skipping translation & entity_i18n upsert")
        return

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
            try:
                translated = _translate(text, lang)
            except Exception as exc:
                log.warning("[i18n] translation failed for %s.%s (%s): %s", entity_type, field, lang, exc)
                continue
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
