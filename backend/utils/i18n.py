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
