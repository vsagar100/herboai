"""Check entity_i18n actual translations for preparations."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
os.chdir(os.path.dirname(__file__))

from init import create_app
app = create_app()

with app.app_context():
    from db import get_db
    db = get_db()
    
    # Check total counts
    total = db.execute("SELECT COUNT(*) FROM entity_i18n WHERE entity_type='preparation'").fetchone()[0]
    print(f"Total preparation i18n rows: {total}")
    
    hi_rows = db.execute("SELECT COUNT(*) FROM entity_i18n WHERE entity_type='preparation' AND lang='hi'").fetchone()[0]
    mr_rows = db.execute("SELECT COUNT(*) FROM entity_i18n WHERE entity_type='preparation' AND lang='mr'").fetchone()[0]
    en_rows = db.execute("SELECT COUNT(*) FROM entity_i18n WHERE entity_type='preparation' AND lang='en'").fetchone()[0]
    print(f"  en={en_rows}, hi={hi_rows}, mr={mr_rows}")
    
    # Check distinct fields stored
    fields = db.execute("SELECT DISTINCT field FROM entity_i18n WHERE entity_type='preparation'").fetchall()
    print(f"Fields: {[f[0] for f in fields]}")
    
    # Sample: prep_id=108 (Gudmar), check what translations exist
    gudmar_preps = db.execute("""
        SELECT p.id, p.name_en FROM preparations p WHERE p.plant_id = 108
    """).fetchall()
    print(f"\nGudmar (plant_id=108) preparations: {[(r[0], r[1]) for r in gudmar_preps]}")
    
    for prep in gudmar_preps[:2]:
        prep_id = prep[0]
        print(f"\n--- Prep {prep_id} ({prep[1]}) ---")
        i18n = db.execute("""
            SELECT lang, field, substr(text, 1, 80) as text_preview 
            FROM entity_i18n 
            WHERE entity_type='preparation' AND entity_id=?
            ORDER BY lang, field
        """, (prep_id,)).fetchall()
        for r in i18n:
            print(f"  [{r[0]}] {r[1]}: {r[2]}")
    
    # Also check Turmeric preps (plant_id=131)
    turmeric_preps = db.execute("""
        SELECT p.id, p.name_en FROM preparations p WHERE p.plant_id = 131
    """).fetchall()
    print(f"\nTurmeric (plant_id=131) preparations: {[(r[0], r[1]) for r in turmeric_preps]}")
    
    for prep in turmeric_preps[:2]:
        prep_id = prep[0]
        print(f"\n--- Prep {prep_id} ({prep[1]}) ---")
        i18n = db.execute("""
            SELECT lang, field, substr(text, 1, 80) as text_preview 
            FROM entity_i18n 
            WHERE entity_type='preparation' AND entity_id=?
            ORDER BY lang, field
        """, (prep_id,)).fetchall()
        for r in i18n:
            print(f"  [{r[0]}] {r[1]}: {r[2]}")
    
    # Check if timing/anupana fields exist in entity_i18n
    timing_count = db.execute("SELECT COUNT(*) FROM entity_i18n WHERE entity_type='preparation' AND field='timing'").fetchone()[0]
    anupana_count = db.execute("SELECT COUNT(*) FROM entity_i18n WHERE entity_type='preparation' AND field='anupana'").fetchone()[0]
    print(f"\ntiming i18n rows: {timing_count}")
    print(f"anupana i18n rows: {anupana_count}")
    
    # Check raw preparations table columns for prep 108 stuff
    print("\n--- RAW preparations columns for a Gudmar prep ---")
    if gudmar_preps:
        raw = db.execute("SELECT timing, anupana, dosage_json, notes FROM preparations WHERE id=?", (gudmar_preps[0][0],)).fetchone()
        if raw:
            print(f"  timing: {raw[0]}")
            print(f"  anupana: {raw[1]}")
            print(f"  dosage_json: {str(raw[2])[:100]}")
            print(f"  notes: {str(raw[3])[:100]}")
    
    # Check if entity_i18n has ACTUAL translations (non-English text in hi/mr)
    print("\n--- Checking if mr/hi texts are truly translated ---")
    sample = db.execute("""
        SELECT i18n.entity_id, i18n.field, i18n.lang, substr(i18n.text, 1, 60) as i18n_text,
               CASE i18n.field 
                   WHEN 'name' THEN p.name_en 
                   WHEN 'notes' THEN substr(p.notes, 1, 60)
               END as en_text
        FROM entity_i18n i18n
        JOIN preparations p ON p.id = i18n.entity_id
        WHERE i18n.entity_type = 'preparation' AND i18n.lang = 'mr' AND i18n.field IN ('name', 'notes')
        LIMIT 10
    """).fetchall()
    for r in sample:
        same = (r[3] == r[4]) if r[3] and r[4] else "?"
        print(f"  prep {r[0]} [{r[2]}] {r[1]}: same_as_en={same}")
        print(f"    i18n: {r[3]}")
        print(f"    en:   {r[4]}")
