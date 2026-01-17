from __future__ import annotations
from typing import Dict

from utils.i18n import upsert_i18n
from services.indexer import rebuild_fts_for_entity, rebuild_vec_for_entity
from services.indic_translation_service import translate_en_to_hi, translate_en_to_mr

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
    - Stores English as verified
    - Auto-translates to hi/mr as auto
    - Rebuilds FTS + vec for that entity
    
    en_fields maps:
    - Plant: {common_name_en, description, therapeutic_actions, parts_used, rasa, guna, virya, vipaka, ...}
    - Disease: {name_en, description, symptoms, causes, prevention_tips, ...}
    - Preparation: {name_en, preparation_steps, dosage_json, timing, anupana, notes, ...}
    """

    fields = TRANSLATABLE_FIELDS.get(entity_type, [])
    
    # Map database column names to i18n field names
    field_mapping = {
        "plant": {"common_name_en": "name"},
        "disease": {"name_en": "name"},
        "preparation": {"name_en": "name"},
    }.get(entity_type, {})

    # 1) English (verified)
    for field in fields:
        # Check if en_fields uses mapped name (e.g., "common_name_en") or direct name (e.g., "name")
        db_col = None
        for db_name, i18n_name in field_mapping.items():
            if i18n_name == field:
                db_col = db_name
                break
        
        # Try both mapped and direct names
        text = en_fields.get(db_col) if db_col else en_fields.get(field)
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
