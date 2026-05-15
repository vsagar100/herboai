#!/usr/bin/env python3
"""Fix incorrect English placeholders in entity_i18n.

Problem:
- entity_i18n has lang='hi'/'mr' rows whose `text` is still English (placeholders).

This script:
1) Creates a timestamped backup of the sqlite DB file.
2) Translates entity_i18n.text from English -> target language based on entity_i18n.lang.
3) Preserves JSON structures (dict/list) when possible.

Safe defaults:
- Only updates rows for langs in {hi,mr}
- Only updates rows whose text appears non-Devanagari (i.e., likely English)
- Only updates rows where source='manual' and status='auto' (placeholder rows)

Usage (from repo root):
  backend/.venv/Scripts/python.exe -m services.fix_entity_i18n_translate_text --dry-run
  backend/.venv/Scripts/python.exe -m services.fix_entity_i18n_translate_text

Optional:
  --db <path>        (default: db/new_herboai.db)
  --limit N          (process at most N rows per language)
  --langs hi,mr
  --force            (translate even if text already contains Devanagari)
"""

from __future__ import annotations

import argparse
import json
import shutil
import sqlite3
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable

from services.indic_translation_service import get_indic_translation_service


@dataclass(frozen=True)
class Row:
    id: int
    lang: str
    field: str
    text: str
    source: str
    status: str


DEVANAGARI_START = 0x0900
DEVANAGARI_END = 0x097F


def has_devanagari(s: str) -> bool:
    return any(DEVANAGARI_START <= ord(ch) <= DEVANAGARI_END for ch in (s or ""))


def looks_like_code_token(s: str) -> bool:
    """Heuristic: keep code-like tokens unmodified (snake_case, ids, etc.)."""
    if not s:
        return True
    t = s.strip()
    if not t:
        return True
    # If it has spaces, it's probably user-facing text
    if any(ch.isspace() for ch in t):
        return False
    # numbers-only or mostly punctuation -> skip
    alnum = sum(ch.isalnum() for ch in t)
    if alnum == 0:
        return True
    # snake_case / kebab-case / identifiers
    if "_" in t or "-" in t:
        return True
    # short tokens are usually codes (e.g., ml, tsp)
    if len(t) <= 3:
        return True
    return False


FORCE_TRANSLATE_FIELDS = {
    # user-facing fields
    "name",
    "description",
    "symptoms",
    "causes",
    "prevention_tips",
    "notes",
    "preparation_steps",
    "dosage_json",
    # these are often stored as token lists; we still want localized display text
    "therapeutic_actions",
    "parts_used",
}


def try_parse_json(text: str) -> Any:
    if not isinstance(text, str):
        return text
    s = text.strip()
    if not s:
        return text
    if not (s.startswith("{") or s.startswith("[")):
        return text
    try:
        return json.loads(s)
    except Exception:
        return text


def translate_payload(payload: Any, tgt_lang: str, *, field: str) -> Any:
    """Translate nested JSON-like payload values while skipping code-like tokens."""
    svc = get_indic_translation_service()

    force = field in FORCE_TRANSLATE_FIELDS

    def normalize_token(token: str) -> str:
        # For token lists (snake_case), normalize to space-separated text for better translation.
        t = token.strip()
        if field in {"therapeutic_actions", "parts_used", "name"}:
            t = t.replace("_", " ").replace("-", " ")
        return t

    def translate_str(text: str) -> str:
        raw = (text or "")
        stripped = normalize_token(raw)
        if not stripped:
            return raw
        if (not force) and looks_like_code_token(stripped):
            return raw
        return svc.translate_text(stripped, "en", tgt_lang)

    def walk(value: Any) -> Any:
        if isinstance(value, str):
            return translate_str(value)
        if isinstance(value, list):
            # translate string lists in a batch when beneficial
            if all(isinstance(v, str) or v is None for v in value):
                strings = [
                    normalize_token(v)
                    for v in value
                    if isinstance(v, str)
                    and normalize_token(v)
                    and (force or not looks_like_code_token(normalize_token(v)))
                ]
                translated_iter: Iterable[str]
                if strings:
                    translated_iter = iter(svc.translate_batch(strings, "en", tgt_lang))
                else:
                    translated_iter = iter(())
                out: list[Any] = []
                for v in value:
                    nv = normalize_token(v) if isinstance(v, str) else ""
                    if isinstance(v, str) and nv and (force or not looks_like_code_token(nv)):
                        out.append(next(translated_iter))
                    else:
                        out.append(v)
                return out
            return [walk(v) for v in value]
        if isinstance(value, dict):
            return {k: walk(v) for k, v in value.items()}
        return value

    return walk(payload)


def translate_text_value(text: str, tgt_lang: str, field: str) -> str:
    """Translate a single entity_i18n.text value.

    - If value is JSON, translate string values and re-encode JSON with ensure_ascii=False.
    - Otherwise translate as plain text.
    """
    parsed = try_parse_json(text)

    # Preserve JSON for dosage_json explicitly (keys like adult/child/general must remain)
    if isinstance(parsed, dict):
        translated = translate_payload(parsed, tgt_lang, field=field)
        return json.dumps(translated, ensure_ascii=False)

    if isinstance(parsed, list):
        translated = translate_payload(parsed, tgt_lang, field=field)
        return json.dumps(translated, ensure_ascii=False)

    # Plain string
    svc = get_indic_translation_service()
    stripped = (text or "").strip()
    if not stripped:
        return text

    # For some fields, we intentionally translate tokens that look code-like
    if field in {"therapeutic_actions", "parts_used", "name"}:
        stripped = stripped.replace("_", " ").replace("-", " ")

    if (field not in FORCE_TRANSLATE_FIELDS) and looks_like_code_token(stripped):
        return text

    return svc.translate_text(stripped, "en", tgt_lang)


def backup_db(db_path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = db_path.with_suffix(db_path.suffix + f".bak_{stamp}")
    shutil.copy2(db_path, backup_path)
    return backup_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Translate entity_i18n.text into hi/mr based on lang")
    repo_root = Path(__file__).resolve().parent.parent.parent
    default_db = repo_root / "db" / "new_herboai.db"
    parser.add_argument("--db", type=str, default=str(default_db), help="Path to sqlite DB")
    parser.add_argument("--langs", type=str, default="hi,mr", help="Comma-separated languages to fix (default: hi,mr)")
    parser.add_argument("--limit", type=int, default=0, help="Limit rows per language (0 = no limit)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--force", action="store_true", help="Translate even if text already contains Devanagari")
    args = parser.parse_args()

    db_path = Path(args.db).resolve()
    if not db_path.exists():
        raise FileNotFoundError(f"DB not found: {db_path}")

    langs = [x.strip().lower() for x in args.langs.split(",") if x.strip()]
    langs = [x for x in langs if x in {"hi", "mr"}]
    if not langs:
        print("Nothing to do: no valid langs (expected hi and/or mr)")
        return 0

    if not args.dry_run:
        backup = backup_db(db_path)
        print(f"[backup] {backup}")

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row

    total_updated = 0

    try:
        for lang in langs:
            limit_sql = f"LIMIT {int(args.limit)}" if args.limit and args.limit > 0 else ""
            rows = conn.execute(
                f"""
                SELECT id, lang, field, text, source, status
                FROM entity_i18n
                WHERE lang=?
                  AND source='manual'
                  AND status='auto'
                {limit_sql}
                """,
                (lang,),
            ).fetchall()

            candidates: list[Row] = []
            for r in rows:
                row = Row(
                    id=int(r["id"]),
                    lang=str(r["lang"]),
                    field=str(r["field"]),
                    text=str(r["text"]),
                    source=str(r["source"]),
                    status=str(r["status"]),
                )
                if not args.force and has_devanagari(row.text):
                    continue
                candidates.append(row)

            print(f"[{lang}] candidates: {len(candidates)}")
            if not candidates:
                continue

            # Translate + update in a transaction
            if not args.dry_run:
                conn.execute("BEGIN")

            updated = 0
            for idx, row in enumerate(candidates, 1):
                new_text = translate_text_value(row.text, lang, row.field)
                if not new_text:
                    continue
                if new_text == row.text:
                    continue

                updated += 1
                if args.dry_run:
                    if updated <= 5:
                        print(f"  [DRY] id={row.id} field={row.field} preview: {row.text[:40]} -> {new_text[:40]}")
                else:
                    conn.execute(
                        """
                        UPDATE entity_i18n
                        SET text=?, source='indictrans2', status='auto', updated_at=CURRENT_TIMESTAMP
                        WHERE id=?
                        """,
                        (new_text, row.id),
                    )

                if idx % 50 == 0:
                    print(f"  ... {lang}: processed {idx}/{len(candidates)} (updated {updated})")

            if not args.dry_run:
                conn.execute("COMMIT")

            print(f"[{lang}] updated: {updated}")
            total_updated += updated

    except Exception:
        if not args.dry_run:
            try:
                conn.execute("ROLLBACK")
            except Exception:
                pass
        raise
    finally:
        conn.close()

    print(f"[done] total updated: {total_updated}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
