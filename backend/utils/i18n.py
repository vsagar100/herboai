from __future__ import annotations
from typing import Iterable
from db import get_db

SUPPORTED_LANGS = {"en", "hi", "mr"}


def normalize_lang(lang: str | None) -> str:
    if not lang:
        return "en"
    lang = lang.strip().lower()
    return lang if lang in SUPPORTED_LANGS else "en"


def upsert_i18n(
    entity_type: str,
    entity_id: int,
    lang: str,
    field: str,
    text: str,
    status: str = "auto",
    source: str = "indictrans2",
) -> None:
    """Upsert a row into entity_i18n.

    DB commit is left to the caller.
    """
    lang = normalize_lang(lang)
    if not text:
        return
    db = get_db()
    db.execute(
        """
        INSERT INTO entity_i18n(entity_type, entity_id, lang, field, text, status, source)
        VALUES(?,?,?,?,?,?,?)
        ON CONFLICT(entity_type, entity_id, lang, field)
        DO UPDATE SET text=excluded.text,
                      status=excluded.status,
                      source=excluded.source,
                      updated_at=CURRENT_TIMESTAMP
        """,
        (entity_type, entity_id, lang, field, text, status, source),
    )


def get_i18n_fields(entity_type: str, entity_id: int, lang: str) -> dict[str, str]:
    """Return all i18n fields for an entity/lang as a dict."""
    lang = normalize_lang(lang)
    db = get_db()
    rows = db.execute(
        "SELECT field, text FROM entity_i18n WHERE entity_type=? AND entity_id=? AND lang=?",
        (entity_type, entity_id, lang),
    ).fetchall()
    return {r["field"]: r["text"] for r in rows}


def get_localized_field(entity_type: str, entity_id: int, field: str, lang: str) -> str:
    """Fetch a localized field from entity_i18n with fallback to base tables.

    Behaviour (matches your requirement):
    - For all languages (en/hi/mr), we FIRST try entity_i18n.
    - If there is no row or it's empty, we fall back to base-table columns.
    - This keeps entity_i18n as the primary source for Marathi/Hindi once data is fixed.
    """

    lang = normalize_lang(lang)
    db = get_db()

    # 1) Primary: entity_i18n
    try:
        row = db.execute(
            "SELECT text FROM entity_i18n WHERE entity_type=? AND entity_id=? AND lang=? AND field=?",
            (entity_type, entity_id, lang, field),
        ).fetchone()

        if row:
            # sqlite3.Row supports index and key access when row_factory is set
            try:
                text = row["text"]
            except Exception:
                text = row[0]

            if isinstance(text, str):
                text = text.strip()
                if text:
                    return text
    except Exception as e:
        import logging

        logger = logging.getLogger("i18n")
        logger.warning(
            f"[i18n] entity_i18n lookup failed for {entity_type}:{entity_id}.{field} ({lang}): {e}"
        )

    # 2) Fallback: base tables (English or existing localized columns)
    col_map: dict[str, dict[str, str]] = {
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
    if not base_col:
        return ""

    try:
        row = db.execute(
            f"SELECT {base_col} FROM {entity_type}s WHERE id=?",
            (entity_id,),
        ).fetchone()

        if not row:
            return ""

        # sqlite3.Row access – prefer dict-style, then index
        try:
            val = row[base_col]
        except Exception:
            val = row[0]

        if isinstance(val, str):
            text = val.strip()
            if text:
                return text
    except Exception as e:
        import logging

        logger = logging.getLogger("i18n")
        logger.warning(
            f"[i18n] Base table fallback failed for {entity_type}:{entity_id}.{field}: {e}"
        )

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
