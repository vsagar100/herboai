from __future__ import annotations
import json
from db import get_db
from utils.i18n import normalize_lang, build_fts_content
from utils.i18n import fts_table, vec_table

# NOTE: you already have an embedder in your codebase producing 384-d vectors.
# We will wire this function to your existing embed_384 implementation once we patch chat/embedding module.
def embed_384(text: str):
    raise RuntimeError("embed_384 not wired yet - will be wired after chat/embed module is re-uploaded")

def _i18n_text(entity_type: str, entity_id: int, lang: str) -> dict[str, str]:
    db = get_db()
    rows = db.execute(
        "SELECT field, text FROM entity_i18n WHERE entity_type=? AND entity_id=? AND lang=?",
        (entity_type, entity_id, normalize_lang(lang)),
    ).fetchall()
    return {r["field"]: r["text"] for r in rows}

def rebuild_fts_for_entity(entity_type: str, entity_id: int) -> None:
    db = get_db()
    for lang in ("en", "hi", "mr"):
        fts = fts_table(entity_type, lang)
        fields = _i18n_text(entity_type, entity_id, lang)
        content = build_fts_content(fields.values())

        db.execute(f"DELETE FROM {fts} WHERE entity_id=?", (entity_id,))
        if content.strip():
            db.execute(f"INSERT INTO {fts}(entity_id, content) VALUES(?,?)", (entity_id, content))
    db.commit()

def rebuild_vec_for_entity(entity_type: str, entity_id: int) -> None:
    db = get_db()
    if entity_type == "preparation":
        vec_prefix = "prep"
        id_col = "preparation_id"
    else:
        vec_prefix = entity_type
        id_col = f"{entity_type}_id"

    for lang in ("en", "hi", "mr"):
        vt = vec_table(vec_prefix, lang)
        fields = _i18n_text(entity_type, entity_id, lang)

        # Use only fields that matter for retrieval: name + key description-like fields
        # (kept generic; admin can control relevance by populating i18n).
        text = build_fts_content(fields.values())
        if not text.strip():
            continue

        vec = embed_384(text)
        name = fields.get("name", "")[:200] if fields.get("name") else ""

        db.execute(
            f"""
            INSERT INTO {vt}({id_col}, name, embedding)
            VALUES(?,?,?)
            ON CONFLICT({id_col})
            DO UPDATE SET name=excluded.name, embedding=excluded.embedding
            """,
            (entity_id, name, vec),
        )
    db.commit()
