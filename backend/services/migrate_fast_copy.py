#!/usr/bin/env python3
"""
FAST Migration: Copy English text as placeholders for Hindi/Marathi

This is a quick alternative to full translation. It copies English text
as placeholders so the entity_i18n table gets populated and the chatbot can work.

Later, we can replace these with actual translations via IndicTrans2.

Usage:
    python migrate_fast_copy.py [--dry-run]
"""

import sys
from pathlib import Path
import sqlite3
import time

# Database configuration
DB_PATH = Path(__file__).parent.parent.parent / "db" / "new_herboai.db"

def get_db_connection() -> sqlite3.Connection:
    """Get direct database connection with autocommit."""
    print(f"[DB] Connecting to: {DB_PATH}", flush=True)
    
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None  # Autocommit mode
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) as cnt FROM plants")
    plant_count = cursor.fetchone()["cnt"]
    print(f"[DB] Found {plant_count} plants", flush=True)
    
    return conn


def migrate_fast(dry_run: bool = False) -> int:
    """Copy English text as placeholders for all languages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    total_inserted = 0
    
    # PLANTS
    print("\n[PLANTS] Processing...", flush=True)
    cursor.execute("SELECT id, common_name_en, description, therapeutic_actions, parts_used FROM plants WHERE common_name_en IS NOT NULL")
    plants = cursor.fetchall()
    
    for idx, plant in enumerate(plants):
        plant_id = plant["id"]
        
        # Insert English version for each language
        fields = [
            ("name", plant["common_name_en"]),
            ("description", plant["description"] or ""),
            ("therapeutic_actions", plant["therapeutic_actions"] or ""),
            ("parts_used", plant["parts_used"] or ""),
        ]
        
        for field_name, field_value in fields:
            if field_value and len(field_value.strip()) > 0:
                if not dry_run:
                    # Insert for Hindi
                    cursor.execute("""
                        INSERT OR REPLACE INTO entity_i18n 
                        (entity_type, entity_id, field, lang, text, status, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ("plant", plant_id, field_name, "hi", field_value, "auto", "manual"))
                    total_inserted += 1
                    
                    # Insert for Marathi
                    cursor.execute("""
                        INSERT OR REPLACE INTO entity_i18n 
                        (entity_type, entity_id, field, lang, text, status, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ("plant", plant_id, field_name, "mr", field_value, "auto", "manual"))
                    total_inserted += 1
        
        if (idx + 1) % 20 == 0:
            print(f"  {idx + 1}/{len(plants)} plants", flush=True)
    
    print(f"  Total: {len(plants)} plants -> {len(plants) * 4 * 2} entries", flush=True)
    
    # DISEASES
    print("\n[DISEASES] Processing...", flush=True)
    cursor.execute("SELECT id, name_en, description, symptoms, causes, prevention_tips FROM diseases WHERE name_en IS NOT NULL")
    diseases = cursor.fetchall()
    
    for idx, disease in enumerate(diseases):
        disease_id = disease["id"]
        
        fields = [
            ("name", disease["name_en"]),
            ("description", disease["description"] or ""),
            ("symptoms", disease["symptoms"] or ""),
            ("causes", disease["causes"] or ""),
            ("prevention_tips", disease["prevention_tips"] or ""),
        ]
        
        for field_name, field_value in fields:
            if field_value and len(field_value.strip()) > 0:
                if not dry_run:
                    # Insert for Hindi
                    cursor.execute("""
                        INSERT OR REPLACE INTO entity_i18n 
                        (entity_type, entity_id, field, lang, text, status, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ("disease", disease_id, field_name, "hi", field_value, "auto", "manual"))
                    total_inserted += 1
                    
                    # Insert for Marathi
                    cursor.execute("""
                        INSERT OR REPLACE INTO entity_i18n 
                        (entity_type, entity_id, field, lang, text, status, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ("disease", disease_id, field_name, "mr", field_value, "auto", "manual"))
                    total_inserted += 1
        
        if (idx + 1) % 10 == 0:
            print(f"  {idx + 1}/{len(diseases)} diseases", flush=True)
    
    print(f"  Total: {len(diseases)} diseases -> {len(diseases) * 5 * 2} entries", flush=True)
    
    # PREPARATIONS
    print("\n[PREPARATIONS] Processing...", flush=True)
    cursor.execute("SELECT id, name_en, preparation_steps, notes, dosage_json FROM preparations WHERE name_en IS NOT NULL")
    preparations = cursor.fetchall()
    
    for idx, prep in enumerate(preparations):
        prep_id = prep["id"]
        
        fields = [
            ("name", prep["name_en"]),
            ("preparation_steps", prep["preparation_steps"] or ""),
            ("notes", prep["notes"] or ""),
            ("dosage_json", prep["dosage_json"] or ""),
        ]
        
        for field_name, field_value in fields:
            if field_value and len(field_value.strip()) > 0:
                if not dry_run:
                    # Insert for Hindi
                    cursor.execute("""
                        INSERT OR REPLACE INTO entity_i18n 
                        (entity_type, entity_id, field, lang, text, status, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ("preparation", prep_id, field_name, "hi", field_value, "auto", "manual"))
                    total_inserted += 1
                    
                    # Insert for Marathi
                    cursor.execute("""
                        INSERT OR REPLACE INTO entity_i18n 
                        (entity_type, entity_id, field, lang, text, status, source)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, ("preparation", prep_id, field_name, "mr", field_value, "auto", "manual"))
                    total_inserted += 1
        
        if (idx + 1) % 30 == 0:
            print(f"  {idx + 1}/{len(preparations)} preparations", flush=True)
    
    print(f"  Total: {len(preparations)} preparations -> {len(preparations) * 4 * 2} entries", flush=True)
    
    conn.close()
    return total_inserted


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Fast migration: copy English as placeholders")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    args = parser.parse_args()
    
    print("\n" + "="*70)
    print("FAST MIGRATION: Copy English text as placeholders")
    print("="*70)
    
    if args.dry_run:
        print("DRY RUN MODE")
    
    start_time = time.time()
    
    try:
        total = migrate_fast(dry_run=args.dry_run)
        
        elapsed = time.time() - start_time
        
        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        
        if args.dry_run:
            print(f"DRY RUN: Would insert ~{total} placeholder entries")
        else:
            print(f"Inserted {total} placeholder entries")
        
        print(f"Time: {elapsed:.1f} seconds")
        print("\nNote: These entries use English text (status='auto', source='manual')")
        print("Later, run the full IndicTrans2 migration to get proper Hindi/Marathi translations.")
        
        sys.exit(0)
    
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
