#!/usr/bin/env python3
"""
ETL Migration Script: Populate entity_i18n table from existing plant/disease/preparation data.
Version 2: Direct database access, no Flask dependency

This script:
1. Reads all plants, diseases, preparations from base tables  
2. Auto-translates user-facing fields (name, description, symptoms, etc.) to Hindi & Marathi
3. Stores translations in entity_i18n table with status="auto"

Run once during migration to populate entity_i18n. Safe to run multiple times (uses upsert logic).

Usage:
    python migrate_to_entity_i18n_v2.py [--dry-run] [--verbose]
"""

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

# Import translation services directly (without Flask dependency)
from services.indic_translation_service import translate_en_to_hi, translate_en_to_mr

# Database configuration
DB_PATH = Path(__file__).parent.parent.parent / "db" / "new_herboai.db"

# Fields to translate per entity type
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


def get_db_connection() -> sqlite3.Connection:
    """Get direct database connection (no Flask required)."""
    print(f"[DB_CONNECTION] Attempting to connect to: {DB_PATH}", flush=True)
    
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    
    print(f"[DB_CONNECTION] Database file exists, size: {DB_PATH.stat().st_size} bytes", flush=True)
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None  # Autocommit mode
    
    # Test connection
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM plants")
    plant_count = cursor.fetchone()["cnt"]
    print(f"[DB_CONNECTION] Connected successfully. Found {plant_count} plants in database", flush=True)
    
    return conn


def upsert_translation(
    conn: sqlite3.Connection,
    entity_type: str,
    entity_id: int,
    field_name: str,
    lang: str,
    translated_value: str,
    status: str = "auto",
    dry_run: bool = False,
    verbose: bool = False
) -> bool:
    """Upsert a translation into entity_i18n table."""
    if dry_run:
        if verbose:
            print(f"    [DRY] Would insert: {entity_type}#{entity_id} {field_name} {lang}")
        return True
    
    try:
        cursor = conn.cursor()
        if verbose:
            print(f"    [INSERT] {entity_type}#{entity_id} {field_name} {lang}: {translated_value[:50]}...", end="")
        
        cursor.execute("""
            INSERT OR REPLACE INTO entity_i18n 
            (entity_type, entity_id, field, lang, text, status, source, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, 'indictrans2', datetime('now'))
        """, (entity_type, entity_id, field_name, lang, translated_value, status))
        
        if verbose:
            print(f" OK (rows affected: {cursor.rowcount})")
        return cursor.rowcount > 0
    except Exception as e:
        print(f"    [ERROR INSERT] {entity_type}#{entity_id} {field_name} {lang}: {e}")
        return False


def migrate_plants(conn: sqlite3.Connection, dry_run: bool = False, verbose: bool = False) -> int:
    """Migrate plants table to entity_i18n."""
    print("[MIGRATE_PLANTS] Starting...", flush=True)
    cursor = conn.cursor()
    
    # Get all plants
    print("[MIGRATE_PLANTS] Querying plants from database...", flush=True)
    cursor.execute("SELECT id, common_name_en, description, therapeutic_actions, parts_used FROM plants")
    plants = cursor.fetchall()
    print(f"[MIGRATE_PLANTS] Found {len(plants)} plants to process", flush=True)
    
    count = 0
    for idx, plant in enumerate(plants):
        plant_id = plant["id"]
        print(f"\n[PLANT {idx+1}/{len(plants)}] ID={plant_id}", flush=True)
        
        # Translate each field
        translations = {}
        translations["common_name_en"] = plant["common_name_en"]
        translations["description"] = plant["description"] if plant["description"] else ""
        translations["therapeutic_actions"] = plant["therapeutic_actions"] if plant["therapeutic_actions"] else ""
        translations["parts_used"] = plant["parts_used"] if plant["parts_used"] else ""
        
        # Skip plants without English data
        if not translations["common_name_en"]:
            print(f"  [SKIP] No English name", flush=True)
            continue
        
        print(f"  Name: {translations['common_name_en'][:60]}", flush=True)
        
        # Translate to Hindi and Marathi
        try:
            for src_field, tgt_field in FIELD_MAPPING["plant"].items():
                text_to_translate = translations[src_field]
                
                if text_to_translate and len(text_to_translate.strip()) > 0:
                    # Translate to Hindi
                    try:
                        print(f"    [TRANSLATE HI] {tgt_field}: {text_to_translate[:40]}...", end="", flush=True)
                        hi_text = translate_en_to_hi(text_to_translate[:500])
                        print(f" -> {hi_text[:40]}...", flush=True)
                        upsert_translation(
                            conn, "plant", plant_id, tgt_field, "hi", hi_text,
                            dry_run=dry_run, verbose=verbose
                        )
                    except Exception as e:
                        print(f" ERROR: {e}", flush=True)
                    
                    # Translate to Marathi
                    try:
                        print(f"    [TRANSLATE MR] {tgt_field}: {text_to_translate[:40]}...", end="", flush=True)
                        mr_text = translate_en_to_mr(text_to_translate[:500])
                        print(f" -> {mr_text[:40]}...", flush=True)
                        upsert_translation(
                            conn, "plant", plant_id, tgt_field, "mr", mr_text,
                            dry_run=dry_run, verbose=verbose
                        )
                    except Exception as e:
                        print(f" ERROR: {e}", flush=True)
            
            print(f"  [SUCCESS] Plant {plant_id} processed", flush=True)
            count += 1
            
        except Exception as e:
            print(f"  [ERROR] Plant {plant_id}: {e}", flush=True)
            import traceback
            traceback.print_exc()
    
    print(f"\n[MIGRATE_PLANTS] Completed. {count} plants processed.", flush=True)
    return count


def migrate_diseases(conn: sqlite3.Connection, dry_run: bool = False, verbose: bool = False) -> int:
    """Migrate diseases table to entity_i18n."""
    cursor = conn.cursor()
    
    # Get all diseases
    cursor.execute("""
        SELECT id, name_en, description, symptoms, causes, prevention_tips 
        FROM diseases
    """)
    diseases = cursor.fetchall()
    
    count = 0
    for disease in diseases:
        disease_id = disease["id"]
        
        # Translate each field
        translations = {}
        translations["name_en"] = disease["name_en"]
        translations["description"] = disease["description"] if disease["description"] else ""
        translations["symptoms"] = disease["symptoms"] if disease["symptoms"] else ""
        translations["causes"] = disease["causes"] if disease["causes"] else ""
        translations["prevention_tips"] = disease["prevention_tips"] if disease["prevention_tips"] else ""
        
        # Skip diseases without English name
        if not translations["name_en"]:
            continue
        
        try:
            if verbose:
                print(f"  Translating disease {disease_id}: {translations['name_en'][:40]}...", end="")
            
            for src_field, tgt_field in FIELD_MAPPING["disease"].items():
                text_to_translate = translations[src_field]
                
                if text_to_translate and len(text_to_translate.strip()) > 0:
                    try:
                        hi_text = translate_en_to_hi(text_to_translate[:500])
                        upsert_translation(
                            conn, "disease", disease_id, tgt_field, "hi", hi_text,
                            dry_run=dry_run
                        )
                    except Exception as e:
                        if verbose:
                            print(f" [HI FAIL: {str(e)[:30]}]", end="")
                
                # Translate to Marathi
                if text_to_translate and len(text_to_translate.strip()) > 0:
                    try:
                        mr_text = translate_en_to_mr(text_to_translate[:500])
                        upsert_translation(
                            conn, "disease", disease_id, tgt_field, "mr", mr_text,
                            dry_run=dry_run
                        )
                    except Exception as e:
                        if verbose:
                            print(f" [MR FAIL: {str(e)[:30]}]", end="")
            
            if verbose:
                print(" OK")
            count += 1
            
        except Exception as e:
            if verbose:
                print(f"\n    ERROR: {e}")
            else:
                print(".", end="", flush=True)
    
    if not verbose:
        print()
    
    return count


def migrate_preparations(conn: sqlite3.Connection, dry_run: bool = False, verbose: bool = False) -> int:
    """Migrate preparations table to entity_i18n."""
    cursor = conn.cursor()
    
    # Get all preparations
    cursor.execute("""
        SELECT id, name_en, preparation_steps, notes, dosage_json 
        FROM preparations
    """)
    preparations = cursor.fetchall()
    
    count = 0
    for prep in preparations:
        prep_id = prep["id"]
        
        # Translate each field
        translations = {}
        translations["name_en"] = prep["name_en"]
        translations["preparation_steps"] = prep["preparation_steps"] if prep["preparation_steps"] else ""
        translations["notes"] = prep["notes"] if prep["notes"] else ""
        translations["dosage_json"] = prep["dosage_json"] if prep["dosage_json"] else ""
        
        # Skip preps without English name
        if not translations["name_en"]:
            continue
        
        try:
            if verbose:
                print(f"  Translating preparation {prep_id}: {translations['name_en'][:40]}...", end="")
            
            for src_field, tgt_field in FIELD_MAPPING["preparation"].items():
                text_to_translate = translations[src_field]
                
                if text_to_translate and len(text_to_translate.strip()) > 0:
                    try:
                        hi_text = translate_en_to_hi(text_to_translate[:500])
                        upsert_translation(
                            conn, "preparation", prep_id, tgt_field, "hi", hi_text,
                            dry_run=dry_run
                        )
                    except Exception as e:
                        if verbose:
                            print(f" [HI FAIL: {str(e)[:30]}]", end="")
                
                # Translate to Marathi
                if text_to_translate and len(text_to_translate.strip()) > 0:
                    try:
                        mr_text = translate_en_to_mr(text_to_translate[:500])
                        upsert_translation(
                            conn, "preparation", prep_id, tgt_field, "mr", mr_text,
                            dry_run=dry_run
                        )
                    except Exception as e:
                        if verbose:
                            print(f" [MR FAIL: {str(e)[:30]}]", end="")
            
            if verbose:
                print(" OK")
            count += 1
            
        except Exception as e:
            if verbose:
                print(f"\n    ERROR: {e}")
            else:
                print(".", end="", flush=True)
    
    if not verbose:
        print()
    
    return count


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Populate entity_i18n with auto-translated plants, diseases, preparations"
    )
    parser.add_argument("--preview", action="store_true", help="Preview what will be migrated (no translations)")
    parser.add_argument("--dry-run", action="store_true", help="Translate but don't write to DB")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print details for each entity")
    parser.add_argument("--plants-only", action="store_true", help="Migrate only plants")
    parser.add_argument("--diseases-only", action="store_true", help="Migrate only diseases")
    parser.add_argument("--preparations-only", action="store_true", help="Migrate only preparations")
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("HerboAI MIGRATION: Populate entity_i18n for Multilingual Support")
    print("="*70)
    
    if args.preview:
        print("[PREVIEW MODE] Showing what will be migrated (no translations)")
    elif args.dry_run:
        print("[DRY RUN] Translating but not writing to database")
    
    start_time = time.time()
    total = 0
    
    try:
        # Connect to database
        print("[MAIN] Connecting to database...", flush=True)
        conn = get_db_connection()
        print("[MAIN] Database connection successful", flush=True)
        
        if args.preview:
            # Fast preview - just count records
            cursor = conn.cursor()
            
            if not args.diseases_only and not args.preparations_only:
                cursor.execute("SELECT COUNT(*) as cnt FROM plants WHERE common_name_en IS NOT NULL AND common_name_en != ''")
                plant_count = cursor.fetchone()["cnt"]
                print(f"\nPlants to migrate: {plant_count}")
            
            if not args.plants_only and not args.preparations_only:
                cursor.execute("SELECT COUNT(*) as cnt FROM diseases WHERE name_en IS NOT NULL AND name_en != ''")
                disease_count = cursor.fetchone()["cnt"]
                print(f"Diseases to migrate: {disease_count}")
            
            if not args.plants_only and not args.diseases_only:
                cursor.execute("SELECT COUNT(*) as cnt FROM preparations WHERE name_en IS NOT NULL AND name_en != ''")
                prep_count = cursor.fetchone()["cnt"]
                print(f"Preparations to migrate: {prep_count}")
            
            total = plant_count + disease_count + prep_count
            print(f"\nTotal entities: {total}")
            print("Each entity will be translated to Hindi and Marathi (2 languages)")
            print(f"Total translation pairs: {total * 2}")
        
        else:
            # Actual migration with translations
            # Migrate plants
            if not args.diseases_only and not args.preparations_only:
                print("\n" + "="*70)
                print("MIGRATING: Plants")
                print("="*70)
                total += migrate_plants(conn, dry_run=args.dry_run, verbose=args.verbose)
            
            # Migrate diseases
            if not args.plants_only and not args.preparations_only:
                print("\n" + "="*70)
                print("MIGRATING: Diseases")
                print("="*70)
                total += migrate_diseases(conn, dry_run=args.dry_run, verbose=args.verbose)
            
            # Migrate preparations
            if not args.plants_only and not args.diseases_only:
                print("\n" + "="*70)
                print("MIGRATING: Preparations")
                print("="*70)
                total += migrate_preparations(conn, dry_run=args.dry_run, verbose=args.verbose)
            
            # Commit changes if not dry run
            if not args.dry_run:
                print("\n[MAIN] Auto-commit enabled - changes saved immediately", flush=True)
        
        print("[MAIN] Closing database connection...", flush=True)
        conn.close()
        print("[MAIN] Database connection closed", flush=True)
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Total entities processed: {total}")
        print(f"Time elapsed: {elapsed:.1f} seconds")
        
        if args.preview:
            print("\nTo migrate: python migrate_to_entity_i18n_v2.py --dry-run")
            print("To apply changes: python migrate_to_entity_i18n_v2.py")
        elif args.dry_run:
            print("\nTo apply changes: python migrate_to_entity_i18n_v2.py")
        else:
            print("\nMigration completed successfully!")
        
        return 0
    
    except Exception as e:
        print(f"\nMigration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
