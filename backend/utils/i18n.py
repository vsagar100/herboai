from __future__ import annotations
from typing import Iterable
from db import get_db

SUPPORTED_LANGS = {"en", "hi", "mr"}

def normalize_lang(lang: str | None) -> str:
    if not lang:
        return "en"
    lang = lang.strip().lower()
    return lang if lang in SUPPORTED_LANGS else "en"

def upsert_i18n(entity_type: str, entity_id: int, lang: str, field: str,
                text: str, status: str = "auto", source: str = "indictrans2") -> None:
    lang = normalize_lang(lang)
    if not text:
        return
    db = get_db()
    db.execute(
        """
        INSERT INTO entity_i18n(entity_type, entity_id, lang, field, text, status, source)
        VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(entity_type, entity_id, lang, field)
        DO UPDATE SET text=excluded.text, status=excluded.status, source=excluded.source, updated_at=CURRENT_TIMESTAMP
        """,
        (entity_type, entity_id, lang, field, text, status, source),
    )
    db.commit()

def get_i18n_fields(entity_type: str, entity_id: int, lang: str) -> dict[str, str]:
    lang = normalize_lang(lang)
    db = get_db()
    rows = db.execute(
        "SELECT field, text FROM entity_i18n WHERE entity_type=? AND entity_id=? AND lang=?",
        (entity_type, entity_id, lang),
    ).fetchall()
    return {r["field"]: r["text"] for r in rows}

def get_localized_field(entity_type: str, entity_id: int, field: str, lang: str) -> str:
    """
    Fetch a localized field from entity_i18n with fallback to base tables.
    
    First tries entity_i18n; if not found, falls back to base table column.
    This maintains backward compatibility while supporting new multilingual table.
    
    Args:
        entity_type: 'plant', 'disease', or 'preparation'
        entity_id: ID of the entity
        field: field name (e.g., 'name', 'description')
        lang: language code ('en', 'hi', 'mr')
    
    Returns:
        Localized text, or empty string if not found
    """
    lang = normalize_lang(lang)
    db = get_db()
    
    # Try entity_i18n first
    row = db.execute(
        "SELECT text FROM entity_i18n WHERE entity_type=? AND entity_id=? AND lang=? AND field=?",
        (entity_type, entity_id, lang, field),
    ).fetchone()
    
    if row and row[0]:
        return row[0].strip()
    
    # Fallback to base tables (for backward compatibility)
    # Map field names to base table columns
    col_map = {
        "plant": {
            "name": "common_name_en",
            "description": "description",
            "therapeutic_actions": "therapeutic_actions",
            "parts_used": "parts_used",
        },
        "disease": {
            "name": "name_en",
            "description": "description",
            "symptoms": "symptoms",
            "causes": "causes",
            "prevention_tips": "prevention_tips",
        },
        "preparation": {
            "name": "name_en",
            "preparation_steps": "preparation_steps",
            "notes": "notes",
            "dosage_json": "dosage_json",
        },
    }
    
    base_col = col_map.get(entity_type, {}).get(field)
    if base_col:
        row = db.execute(
            f"SELECT {base_col} FROM {entity_type}s WHERE id=?",
            (entity_id,),
        ).fetchone()
        if row and row[0]:
            val = row[0]
            if isinstance(val, str):
                text = val.strip()
                # Log when we're falling back to English for non-English request
                if lang != "en" and text:
                    import logging
                    logger = logging.getLogger("i18n")
                    logger.debug(f"[i18n FALLBACK] {entity_type}:{entity_id} {field} for {lang} -> using English column {base_col}")
                return text
    
    return ""

def build_fts_content(chunks: Iterable[str]) -> str:
    # Compact join with safe spacing
    parts = [c.strip() for c in chunks if c and c.strip()]
    return "\n".join(parts)

def fts_table(entity: str, lang: str) -> str:
    lang = normalize_lang(lang)
    return f"{entity}s_fts_{lang}"  # plants_fts_en / diseases_fts_en / preparations_fts_en

def vec_table(entity: str, lang: str) -> str:
    lang = normalize_lang(lang)
    # entity: 'plant'|'disease'|'prep'
    return f"{entity}_vec_{lang}"
