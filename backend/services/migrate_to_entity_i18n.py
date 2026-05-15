#!/usr/bin/env python3
"""
ETL Migration Script: Populate entity_i18n table from existing plant/disease/preparation data.

This script:
1. Reads all plants, diseases, preparations from base tables
2. Auto-translates user-facing fields (name, description, symptoms, etc.) to Hindi & Marathi
3. Stores translations in entity_i18n table with status="auto"
4. Rebuilds FTS and vector tables for all 3 languages

Run once during migration to populate entity_i18n. Safe to run multiple times (uses upsert logic).

Usage:
    python migrate_to_entity_i18n.py [--dry-run] [--verbose]
"""

from __future__ import annotations
import sys
import json
from typing import Any, Dict, List, Optional
import argparse
import time
from pathlib import Path
import sqlite3
import os

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Initialize Flask app context (required for translate functions)
try:
    from init import create_app
    app = create_app()
except Exception as e:
    # If Flask init fails, create minimal context
    print("Warning: Could not import Flask app. Trying direct DB access...")
    print(f"Error: {str(e)[:50]}")
    app = None

from db import get_db
from utils.i18n import upsert_i18n, normalize_lang
from services.indic_translation_service import translate_en_to_hi, translate_en_to_mr
from services.indexer import rebuild_fts_for_entity, rebuild_vec_for_entity

# Fields to translate per entity type
# Mapping: base_table_column → entity_i18n field name
TRANSLATABLE_FIELDS = {
    "plant": [
        "common_name_en",  # → "name"
        "description",
        "therapeutic_actions",
        "parts_used",
    ],
    "disease": [
        "name_en",  # → "name"
        "description",
        "symptoms",
        "causes",
        "prevention_tips",
    ],
    "preparation": [
        "name_en",  # → "name"
        "preparation_steps",
        "notes",
        "dosage_json",
    ],
}

# Map base table column names to entity_i18n field names
FIELD_MAPPING = {
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


def _as_string(val: Any) -> str:
    """Convert various formats to displayable string."""
    if not val:
        return ""
    if isinstance(val, str):
        return val.strip()
    if isinstance(val, list):
        return "; ".join(str(x).strip() for x in val if x)
    if isinstance(val, dict):
        try:
            parsed = json.loads(json.dumps(val))  # ensure JSON serializable
            items = []
            for k, v in parsed.items():
                if isinstance(v, list):
                    items.append(f"{k}: {', '.join(str(x) for x in v)}")
                else:
                    items.append(f"{k}: {v}")
            return "; ".join(items)
        except Exception:
            return str(val).strip()
    return str(val).strip()


def _try_parse_json(val: Any) -> list[str] | dict[str, Any] | str:
    """Parse JSON or return original."""
    if not val:
        return ""
    if isinstance(val, (list, dict)):
        return val
    if isinstance(val, str):
        try:
            return json.loads(val)
        except Exception:
            return val
    return str(val)


def translate_text(text: str, target_lang: str) -> str:
    """Translate English text to target language."""
    if not text or target_lang == "en":
        return text
    
    text = text.strip()
    if len(text) > 2000:
        # Translation models may struggle with very long text; truncate with ellipsis
        text = text[:2000] + "..."
    
    try:
        if target_lang == "hi":
            return translate_en_to_hi(text)
        elif target_lang == "mr":
            return translate_en_to_mr(text)
    except Exception as e:
        print(f"  ⚠️ Translation failed for {target_lang}: {e}")
        return ""
    
    return ""


def migrate_plants(dry_run: bool = False, verbose: bool = False) -> int:
    """Migrate plant data to entity_i18n."""
    print("\n" + "="*70)
    print("MIGRATING: Plants")
    print("="*70)
    
    db = get_db()
    db.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    
    rows = db.execute("SELECT id, common_name_en, description, therapeutic_actions, parts_used FROM plants").fetchall()
    count = 0
    
    for row in rows:
        plant_id = row["id"]
        
        if verbose:
            print(f"\n  Plant ID {plant_id}: {row.get('common_name_en', 'Unknown')}")
        
        # English (verified)
        for base_col, field_name in FIELD_MAPPING["plant"].items():
            val = row.get(base_col)
            text = _as_string(val)
            
            if text:
                if not dry_run:
                    upsert_i18n("plant", plant_id, "en", field_name, text, status="verified", source="manual")
                if verbose:
                    print(f"    ✓ {field_name} (en, verified)")
        
        # Hindi & Marathi (auto-translated)
        for base_col, field_name in FIELD_MAPPING["plant"].items():
            val = row.get(base_col)
            text = _as_string(val)
            
            if text:
                for lang in ("hi", "mr"):
                    translated = translate_text(text, lang)
                    
                    if translated:
                        if not dry_run:
                            upsert_i18n("plant", plant_id, lang, field_name, translated, status="auto", source="indictrans2")
                        if verbose:
                            print(f"    ✓ {field_name} ({lang}, auto)")
                    elif verbose:
                        print(f"    ⚠ {field_name} ({lang}, failed to translate)")
        
        # Rebuild FTS & vectors for this plant
        if not dry_run:
            try:
                rebuild_fts_for_entity("plant", plant_id)
                rebuild_vec_for_entity("plant", plant_id)
            except Exception as e:
                print(f"  ⚠️ Index rebuild failed for plant {plant_id}: {e}")
        
        count += 1
        if count % 10 == 0:
            print(f"  ... processed {count} plants")
    
    print(f"\n✅ Processed {count} plants")
    return count


def migrate_diseases(dry_run: bool = False, verbose: bool = False) -> int:
    """Migrate disease data to entity_i18n."""
    print("\n" + "="*70)
    print("MIGRATING: Diseases")
    print("="*70)
    
    db = get_db()
    db.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    
    rows = db.execute(
        "SELECT id, name_en, description, symptoms, causes, prevention_tips FROM diseases"
    ).fetchall()
    count = 0
    
    for row in rows:
        disease_id = row["id"]
        
        if verbose:
            print(f"\n  Disease ID {disease_id}: {row.get('name_en', 'Unknown')}")
        
        # English (verified)
        for base_col, field_name in FIELD_MAPPING["disease"].items():
            val = row.get(base_col)
            text = _as_string(val)
            
            if text:
                if not dry_run:
                    upsert_i18n("disease", disease_id, "en", field_name, text, status="verified", source="manual")
                if verbose:
                    print(f"    ✓ {field_name} (en, verified)")
        
        # Hindi & Marathi (auto-translated)
        for base_col, field_name in FIELD_MAPPING["disease"].items():
            val = row.get(base_col)
            text = _as_string(val)
            
            if text:
                for lang in ("hi", "mr"):
                    translated = translate_text(text, lang)
                    
                    if translated:
                        if not dry_run:
                            upsert_i18n("disease", disease_id, lang, field_name, translated, status="auto", source="indictrans2")
                        if verbose:
                            print(f"    ✓ {field_name} ({lang}, auto)")
                    elif verbose:
                        print(f"    ⚠ {field_name} ({lang}, failed to translate)")
        
        # Rebuild FTS & vectors for this disease
        if not dry_run:
            try:
                rebuild_fts_for_entity("disease", disease_id)
                rebuild_vec_for_entity("disease", disease_id)
            except Exception as e:
                print(f"  ⚠️ Index rebuild failed for disease {disease_id}: {e}")
        
        count += 1
        if count % 10 == 0:
            print(f"  ... processed {count} diseases")
    
    print(f"\n✅ Processed {count} diseases")
    return count


def migrate_preparations(dry_run: bool = False, verbose: bool = False) -> int:
    """Migrate preparation data to entity_i18n."""
    print("\n" + "="*70)
    print("MIGRATING: Preparations")
    print("="*70)
    
    db = get_db()
    db.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    
    rows = db.execute(
        "SELECT id, name_en, preparation_steps, notes, dosage_json FROM preparations"
    ).fetchall()
    count = 0
    
    for row in rows:
        prep_id = row["id"]
        
        if verbose:
            print(f"\n  Preparation ID {prep_id}: {row.get('name_en', 'Unknown')}")
        
        # English (verified)
        for base_col, field_name in FIELD_MAPPING["preparation"].items():
            val = row.get(base_col)
            text = _as_string(val)
            
            if text:
                if not dry_run:
                    upsert_i18n("preparation", prep_id, "en", field_name, text, status="verified", source="manual")
                if verbose:
                    print(f"    ✓ {field_name} (en, verified)")
        
        # Hindi & Marathi (auto-translated)
        for base_col, field_name in FIELD_MAPPING["preparation"].items():
            val = row.get(base_col)
            text = _as_string(val)
            
            if text:
                for lang in ("hi", "mr"):
                    translated = translate_text(text, lang)
                    
                    if translated:
                        if not dry_run:
                            upsert_i18n("preparation", prep_id, lang, field_name, translated, status="auto", source="indictrans2")
                        if verbose:
                            print(f"    ✓ {field_name} ({lang}, auto)")
                    elif verbose:
                        print(f"    ⚠ {field_name} ({lang}, failed to translate)")
        
        # Rebuild FTS & vectors for this preparation
        if not dry_run:
            try:
                rebuild_fts_for_entity("preparation", prep_id)
                rebuild_vec_for_entity("preparation", prep_id)
            except Exception as e:
                print(f"  ⚠️ Index rebuild failed for preparation {prep_id}: {e}")
        
        count += 1
        if count % 10 == 0:
            print(f"  ... processed {count} preparations")
    
    print(f"\n✅ Processed {count} preparations")
    return count


def main():
    parser = argparse.ArgumentParser(
        description="Migrate plant/disease/preparation data to entity_i18n table for multilingual support."
    )
    parser.add_argument("--dry-run", action="store_true", help="Don't write to database, just show what would happen")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print details for each entity")
    parser.add_argument("--plants-only", action="store_true", help="Migrate only plants")
    parser.add_argument("--diseases-only", action="store_true", help="Migrate only diseases")
    parser.add_argument("--preparations-only", action="store_true", help="Migrate only preparations")
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("HerboAI MIGRATION: Populate entity_i18n for Multilingual Support")
    print("="*70)
    
    if args.dry_run:
        print("[DRY RUN] No changes will be written to database")
    
    start_time = time.time()
    total = 0
    
    try:
        # Use app context if available
        if app:
            with app.app_context():
                if not args.diseases_only and not args.preparations_only:
                    total += migrate_plants(dry_run=args.dry_run, verbose=args.verbose)
                
                if not args.plants_only and not args.preparations_only:
                    total += migrate_diseases(dry_run=args.dry_run, verbose=args.verbose)
                
                if not args.plants_only and not args.diseases_only:
                    total += migrate_preparations(dry_run=args.dry_run, verbose=args.verbose)
        else:
            # Run without context
            if not args.diseases_only and not args.preparations_only:
                total += migrate_plants(dry_run=args.dry_run, verbose=args.verbose)
            
            if not args.plants_only and not args.preparations_only:
                total += migrate_diseases(dry_run=args.dry_run, verbose=args.verbose)
            
            if not args.plants_only and not args.diseases_only:
                total += migrate_preparations(dry_run=args.dry_run, verbose=args.verbose)
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*70)
        print("MIGRATION SUMMARY")
        print("="*70)
        print(f"Total entities processed: {total}")
        print(f"Time elapsed: {elapsed:.1f} seconds")
        
        if not args.dry_run:
            print("\nMigration completed successfully!")
            print("\nNext steps:")
            print("  1. Verify translated content in entity_i18n table")
            print("  2. Run test_migration.py to test multilingual queries")
            print("  3. Monitor admin_i18n_indexer for any issues")
        else:
            print("\nDry run completed. Run without --dry-run to apply changes.")
        
        return 0
    
    except Exception as e:
        print(f"\nMigration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
