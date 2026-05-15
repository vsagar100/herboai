#!/usr/bin/env python3
"""
Fast Migration Script: Populate entity_i18n table with English content (no translation)

This script:
1. Reads all plants, diseases, preparations from base tables  
2. Copies English fields to entity_i18n for 'en' language
3. Uses placeholder translations for Hindi/Marathi (or skips them)
4. Completes in seconds instead of hours

Run this to populate entity_i18n with English content immediately.
Later, run with --translate flag to add actual Hindi/Marathi translations.

Usage:
    python migrate_fast.py [--preview]
"""

import sys
import json
from pathlib import Path
import sqlite3
import argparse
import time

# Database configuration
DB_PATH = Path(__file__).parent.parent.parent / "db" / "new_herboai.db"

# Fields to migrate per entity type
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
    """Get direct database connection."""
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def insert_translation(
    conn: sqlite3.Connection,
    entity_type: str,
    entity_id: int,
    field_name: str,
    lang: str,
    value: str,
) -> bool:
    """Insert a translation into entity_i18n table."""
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT OR IGNORE INTO entity_i18n 
            (entity_type, entity_id, field, lang, text, status, source, updated_at)
            VALUES (?, ?, ?, ?, ?, 'auto', 'fast-migration', datetime('now'))
        """, (entity_type, entity_id, field_name, lang, value))
        return True
    except Exception as e:
        print(f"    Insert failed: {e}")
        return False


def migrate_plants(conn: sqlite3.Connection) -> int:
    """Migrate plants table to entity_i18n."""
    cursor = conn.cursor()
    
    # Get all plants
    cursor.execute("SELECT id, common_name_en, description, therapeutic_actions, parts_used FROM plants")
    plants = cursor.fetchall()
    
    count = 0
    for plant in plants:
        plant_id = plant["id"]
        
        # Skip plants without English name
        if not plant["common_name_en"]:
            continue
        
        # Insert English fields
        for src_field, tgt_field in FIELD_MAPPING["plant"].items():
            value = plant[src_field]
            if value and len(str(value).strip()) > 0:
                insert_translation(
                    conn, "plant", plant_id, tgt_field, "en", str(value)
                )
        
        count += 1
        if count % 50 == 0:
            print(f"  Processed {count} plants...", flush=True)
    
    print(f"  Total plants migrated: {count}")
    return count


def migrate_diseases(conn: sqlite3.Connection) -> int:
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
        
        # Skip diseases without English name
        if not disease["name_en"]:
            continue
        
        # Insert English fields
        for src_field, tgt_field in FIELD_MAPPING["disease"].items():
            value = disease[src_field]
            if value and len(str(value).strip()) > 0:
                insert_translation(
                    conn, "disease", disease_id, tgt_field, "en", str(value)
                )
        
        count += 1
        if count % 20 == 0:
            print(f"  Processed {count} diseases...", flush=True)
    
    print(f"  Total diseases migrated: {count}")
    return count


def migrate_preparations(conn: sqlite3.Connection) -> int:
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
        
        # Skip preps without English name
        if not prep["name_en"]:
            continue
        
        # Insert English fields
        for src_field, tgt_field in FIELD_MAPPING["preparation"].items():
            value = prep[src_field]
            if value and len(str(value).strip()) > 0:
                insert_translation(
                    conn, "preparation", prep_id, tgt_field, "en", str(value)
                )
        
        count += 1
        if count % 50 == 0:
            print(f"  Processed {count} preparations...", flush=True)
    
    print(f"  Total preparations migrated: {count}")
    return count


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fast migration: populate entity_i18n with English content"
    )
    parser.add_argument("--preview", action="store_true", help="Preview what will be migrated")
    
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("FAST MIGRATION: Populate entity_i18n with English Content")
    print("="*70)
    
    start_time = time.time()
    total = 0
    
    try:
        conn = get_db_connection()
        
        if args.preview:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM plants WHERE common_name_en IS NOT NULL AND common_name_en != ''")
            plant_count = cursor.fetchone()["cnt"]
            cursor.execute("SELECT COUNT(*) as cnt FROM diseases WHERE name_en IS NOT NULL AND name_en != ''")
            disease_count = cursor.fetchone()["cnt"]
            cursor.execute("SELECT COUNT(*) as cnt FROM preparations WHERE name_en IS NOT NULL AND name_en != ''")
            prep_count = cursor.fetchone()["cnt"]
            
            print(f"\nWill migrate:")
            print(f"  Plants: {plant_count} (4 fields each)")
            print(f"  Diseases: {disease_count} (5 fields each)")
            print(f"  Preparations: {prep_count} (4 fields each)")
            print(f"\nTotal translation rows: {(plant_count * 4) + (disease_count * 5) + (prep_count * 4)}")
        else:
            print("\nMigrating plants...")
            total += migrate_plants(conn)
            
            print("\nMigrating diseases...")
            total += migrate_diseases(conn)
            
            print("\nMigrating preparations...")
            total += migrate_preparations(conn)
            
            print("\nCommitting changes...")
            conn.commit()
            
            elapsed = time.time() - start_time
            
            print("\n" + "="*70)
            print("MIGRATION COMPLETE")
            print("="*70)
            print(f"Total entities migrated: {total}")
            print(f"Time elapsed: {elapsed:.2f} seconds")
            print("\nThe chatbot can now work with English content!")
            print("Next: Run translation script separately to add Hindi/Marathi translations")
        
        conn.close()
        return 0
    
    except Exception as e:
        print(f"\nMigration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
