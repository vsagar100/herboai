#!/usr/bin/env python3
"""Rebuild Hindi/Marathi rows in entity_i18n from clean English/base data.

Goals:
- Fix corrupted hi/mr text in entity_i18n (names, descriptions, etc.)
- Keep entity_i18n as the primary source for non-English responses
- Use:
    * Base-table hi/mr name columns where available (they are curated)
    * English source text from entity_i18n(lang='en') or base tables
    * IndicTrans2 for translating non-name fields (description, symptoms, etc.)

Usage (from repo root):
  backend/.venv/Scripts/python.exe -m services.rebuild_entity_i18n_hi_mr --dry-run
  backend/.venv/Scripts/python.exe -m services.rebuild_entity_i18n_hi_mr
"""

from __future__ import annotations

import argparse
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

from services.indic_translation_service import get_indic_translation_service
from services.fix_entity_i18n_translate_text import translate_text_value


DB_PATH = Path(__file__).resolve().parent.parent.parent / "db" / "new_herboai.db"


@dataclass
class SourceField:
    entity_type: str
    entity_id: int
    field: str
    text_en: str


FIELD_MAPPING: Dict[str, Dict[str, str]] = {
    "plant": {
        "common_name_en": "name",
        "description": "description",
        "therapeutic_actions": "therapeutic_actions",
        "parts_used": "parts_used",
    },
    "disease": {
        "name_en": "name",
        "description": "description",
        "symptoms": "symptoms",
        "causes": "causes",
        "prevention_tips": "prevention_tips",
    },
    "preparation": {
        "name_en": "name",
        "preparation_steps": "preparation_steps",
        "notes": "notes",
        "dosage_json": "dosage_json",
    },
}


def connect_db() -> sqlite3.Connection:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"DB not found: {DB_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def get_en_source_text(conn: sqlite3.Connection, entity_type: str, entity_id: int, field: str) -> Optional[str]:
    """Get English source for a given entity/field.

    Priority:
      1) entity_i18n(lang='en') text
      2) Base-table English column
    """
    # 1) entity_i18n EN
    row = conn.execute(
        """SELECT text FROM entity_i18n
            WHERE entity_type=? AND entity_id=? AND lang='en' AND field=?""",
        (entity_type, entity_id, field),
    ).fetchone()
    if row:
        text = row["text"] if "text" in row.keys() else row[0]
        if isinstance(text, str) and text.strip():
            return text.strip()

    # 2) Base-table EN column
    base_spec = FIELD_MAPPING.get(entity_type, {})
    base_col = None
    for src_col, tgt_field in base_spec.items():
        if tgt_field == field:
            base_col = src_col
            break
    if not base_col:
        return None

    row = conn.execute(
        f"SELECT {base_col} FROM {entity_type}s WHERE id=?",
        (entity_id,),
    ).fetchone()
    if not row:
        return None

    val = row[base_col] if base_col in row.keys() else row[0]
    if isinstance(val, str) and val.strip():
        return val.strip()
    return None


def upsert_i18n(
    conn: sqlite3.Connection,
    entity_type: str,
    entity_id: int,
    field: str,
    lang: str,
    text: str,
) -> None:
    # Use source='manual' to satisfy existing CHECK constraint on entity_i18n.source
    conn.execute(
        """
        INSERT INTO entity_i18n(entity_type, entity_id, field, lang, text, status, source, updated_at)
        VALUES(?,?,?,?,?, 'auto', 'manual', datetime('now'))
        ON CONFLICT(entity_type, entity_id, lang, field)
        DO UPDATE SET text=excluded.text,
                      status=excluded.status,
                      source=excluded.source,
                      updated_at=excluded.updated_at
        """,
        (entity_type, entity_id, field, lang, text),
    )


def rebuild_for_entity_type(conn: sqlite3.Connection, entity_type: str, dry_run: bool, names_only: bool) -> None:
    svc = get_indic_translation_service() if not names_only else None

    if entity_type == "plant":
        rows = conn.execute(
            "SELECT id, common_name_en, common_name_hi, common_name_mr FROM plants",
        ).fetchall()
    elif entity_type == "disease":
        rows = conn.execute(
            "SELECT id, name_en, name_hi, name_mr FROM diseases",
        ).fetchall()
    elif entity_type == "preparation":
        rows = conn.execute(
            "SELECT id, name_en FROM preparations",
        ).fetchall()
    else:
        return

    print(f"[rebuild] {entity_type}: processing {len(rows)} entities")

    for r in rows:
        eid = int(r["id"])

        # --- Names: prefer curated base hi/mr when present ---
        if entity_type in {"plant", "disease"}:
            for lang, col in (("hi", "common_name_hi" if entity_type == "plant" else "name_hi"),
                              ("mr", "common_name_mr" if entity_type == "plant" else "name_mr")):
                if col in r.keys():
                    val = r[col]
                else:
                    val = None
                if isinstance(val, str) and val.strip():
                    if dry_run:
                        print(f"  [DRY] {entity_type} {eid} {lang}.name <- base {col}: {val[:40]}")
                    else:
                        upsert_i18n(conn, entity_type, eid, "name", lang, val.strip())

        elif entity_type == "preparation" and not names_only:
            # preparations rarely have hi/mr names; translate from English if needed
            name_en = r["name_en"]
            if isinstance(name_en, str) and name_en.strip() and svc is not None:
                for lang in ("hi", "mr"):
                    translated = svc.translate_text(name_en.strip(), "en", lang)
                    if dry_run:
                        print(f"  [DRY] preparation {eid} {lang}.name <- {translated[:40]}")
                    else:
                        upsert_i18n(conn, "preparation", eid, "name", lang, translated)

        # --- Other fields: translate from English source text ---
        if not names_only:
            for src_col, tgt_field in FIELD_MAPPING[entity_type].items():
                if tgt_field == "name":
                    continue  # handled above

                text_en = get_en_source_text(conn, entity_type, eid, tgt_field)
                if not text_en:
                    continue

                for lang in ("hi", "mr"):
                    translated = translate_text_value(text_en, lang, tgt_field)
                    if dry_run:
                        preview = translated.replace("\n", " ")[:60]
                        print(f"  [DRY] {entity_type} {eid} {lang}.{tgt_field} <- {preview}")
                    else:
                        upsert_i18n(conn, entity_type, eid, tgt_field, lang, translated)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild hi/mr rows in entity_i18n from English/base data")
    parser.add_argument("--db", type=str, default=str(DB_PATH), help="Path to sqlite DB")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing to DB")
    parser.add_argument("--names-only", action="store_true", help="Only rebuild hi/mr 'name' fields (no heavy translation)")
    args = parser.parse_args()

    conn = connect_db()

    try:
        for et in ("plant", "disease", "preparation"):
            rebuild_for_entity_type(conn, et, dry_run=args.dry_run, names_only=args.names_only)

        if args.dry_run:
            print("[rebuild] DRY RUN complete (no changes written)")
        else:
            conn.commit()
            print("[rebuild] Changes committed to DB")
    finally:
        conn.close()

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
