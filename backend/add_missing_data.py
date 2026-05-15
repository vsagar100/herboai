"""Add missing disease synonyms and plant-disease mappings"""
from flask import Flask
from db import init_app, get_db

app = Flask(__name__)
app.config["DB_PATH"] = "../db/new_herboai.db"
init_app(app)

with app.app_context():
    db = get_db()
    
    print("\n=== ADDING MISSING DATA ===\n")
    
    # 1. Add disease synonyms for acne
    print("1. Adding disease synonyms for acne...")
    acne_disease_id = 184  # "Acne / Pimples"
    
    synonyms_to_add = [
        (acne_disease_id, 'acne', 'en'),
        (acne_disease_id, 'pimples', 'en'),
        (acne_disease_id, 'pimple', 'en'),
        (acne_disease_id, 'मुरुम', 'hi'),
        (acne_disease_id, 'फुंसी', 'hi'),
        (acne_disease_id, 'पिंपल्स', 'mr'),
    ]
    
    for disease_id, synonym, language in synonyms_to_add:
        # Check if exists
        exists = db.execute(
            "SELECT 1 FROM disease_synonyms WHERE disease_id=? AND LOWER(synonym)=LOWER(?)",
            (disease_id, synonym)
        ).fetchone()
        
        if not exists:
            db.execute(
                "INSERT INTO disease_synonyms (disease_id, synonym, language) VALUES (?, ?, ?)",
                (disease_id, synonym, language)
            )
            print(f"  ✓ Added: '{synonym}' ({language})")
        else:
            print(f"  - Already exists: '{synonym}'")
    
    # 2. Add neem-acne mapping
    print("\n2. Adding plant-disease mapping: Neem → Acne...")
    neem_id = 4
    
    exists = db.execute(
        "SELECT 1 FROM plant_disease_mapping WHERE plant_id=? AND disease_id=?",
        (neem_id, acne_disease_id)
    ).fetchone()
    
    if not exists:
        db.execute("""
            INSERT INTO plant_disease_mapping 
            (plant_id, disease_id, efficacy_level, evidence_type)
            VALUES (?, ?, ?, ?)
        """, (
            neem_id, 
            acne_disease_id,
            4,  # efficacy: 4/5 (strong traditional evidence)
            'traditional'
        ))
        print("  ✓ Added: Neem → Acne (efficacy: 4)")
    else:
        print("  - Already exists")
    
    # 3. Add common skin condition synonyms
    print("\n3. Adding synonyms for common skin conditions...")
    skin_disease_id = 5  # "Chronic Skin Disease"
    
    more_synonyms = [
        (skin_disease_id, 'skin problem', 'en'),
        (skin_disease_id, 'skin issue', 'en'),
        (skin_disease_id, 'skin rash', 'en'),
        (skin_disease_id, 'eczema', 'en'),
        (skin_disease_id, 'त्वचा रोग', 'hi'),
        (skin_disease_id, 'खाज', 'hi'),
    ]
    
    for disease_id, synonym, language in more_synonyms:
        exists = db.execute(
            "SELECT 1 FROM disease_synonyms WHERE disease_id=? AND LOWER(synonym)=LOWER(?)",
            (disease_id, synonym)
        ).fetchone()
        
        if not exists:
            db.execute(
                "INSERT INTO disease_synonyms (disease_id, synonym, language) VALUES (?, ?, ?)",
                (disease_id, synonym, language)
            )
            print(f"  ✓ Added: '{synonym}' ({language})")
    
    db.commit()
    print("\n✅ All data added successfully!")
    
    # Verification
    print("\n=== VERIFICATION ===")
    count = db.execute(
        "SELECT COUNT(*) as cnt FROM disease_synonyms WHERE disease_id=?",
        (acne_disease_id,)
    ).fetchone()['cnt']
    print(f"Acne disease now has {count} synonyms")
    
    mapping = db.execute(
        "SELECT COUNT(*) as cnt FROM plant_disease_mapping WHERE plant_id=? AND disease_id=?",
        (neem_id, acne_disease_id)
    ).fetchone()['cnt']
    print(f"Neem-Acne mapping exists: {mapping > 0}")
