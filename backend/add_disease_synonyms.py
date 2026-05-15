"""
Add missing disease synonyms for Hindi/Marathi/English aliases.
This ensures fuzzy entity extraction can resolve non-English disease queries.
"""
import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "new_herboai.db"))

# (disease_id, synonym) pairs to insert
# We focus on the major conditions that users commonly query in Hindi/Marathi
SYNONYMS = [
    # ─── Hypertension (id=160) ───
    (160, "उच्च रक्तचाप"),        # Hindi
    (160, "उच्च रक्तदाब"),        # Marathi
    (160, "high bp"),
    (160, "high blood pressure"),
    (160, "रक्तदाब"),             # Marathi short
    (160, "ब्लड प्रेशर"),         # Hindi transliteration
    (160, "हाय बीपी"),            # Hindi transliteration
    
    # ─── High Blood Pressure (Hypertension) (id=171) ───
    (171, "उच्च रक्तचाप"),
    (171, "उच्च रक्तदाब"),
    (171, "high bp"),
    (171, "blood pressure"),
    (171, "रक्तदाब"),
    (171, "ब्लड प्रेशर"),
    (171, "बीपी"),
    
    # ─── Low Blood Pressure (id=172) ───
    (172, "निम्न रक्तचाप"),       # Hindi
    (172, "कमी रक्तदाब"),         # Marathi
    (172, "low bp"),
    (172, "low blood pressure"),
    
    # ─── Diabetes Mellitus Type 2 (id=14) — already has some, add more ───
    (14, "डायबिटीज"),             # Hindi transliteration
    (14, "मधुमेह रोग"),           # Hindi formal
    (14, "साखरेचा आजार"),         # Marathi colloquial
    (14, "ब्लड शुगर"),            # Hindi
    (14, "type 2 diabetes"),
    (14, "sugar disease"),
    
    # ─── Common Cold — find the right id first ───
    # We'll handle these dynamically below
    
    # ─── Gastric / Hyperacidity (id=9) — add more ───
    (9, "गॅस"),                   # Gas
    (9, "अपचन"),                  # Indigestion  
    (9, "पोटात जळजळ"),           # Marathi: burning in stomach
    (9, "पेट में जलन"),           # Hindi: burning in stomach
    (9, "एसिडिटी"),              # Transliteration
    (9, "acidity"),
    (9, "heartburn"),
    (9, "gastric"),
    (9, "hyperacidity"),
    
    # ─── Bronchial Asthma (id=11) ───
    (11, "अस्थमा"),              # Hindi transliteration  
    (11, "दमा"),                  # Hindi colloquial
    (11, "श्वसन विकार"),          # Marathi
    
    # ─── Chronic Cough (id=12) ───
    (12, "खोकला"),                # Marathi
    (12, "खांसी"),                # Hindi
    (12, "सर्दी"),                # Hindi: cold
    (12, "सर्दी खोकला"),          # Marathi
    (12, "जुकाम"),                # Hindi: cold
    (12, "cold"),
    (12, "cough"),
    (12, "common cold"),
    (12, "flu"),
    
    # ─── Obesity (id=15) — add more ───
    (15, "वजन वाढ"),              # Marathi: weight gain
    (15, "वजन कमी करणे"),         # Marathi: weight loss
    (15, "मोटापा कम करना"),       # Hindi
    (15, "overweight"),
    (15, "weight loss"),
    
    # ─── Diarrhea and IBS (id=17) ───
    (17, "पोटदुखी"),              # Marathi: stomachache
    (17, "पेट दर्द"),             # Hindi: stomach pain
    (17, "loose motion"),
    (17, "loose motions"),
    (17, "ibs"),
    
    # ─── Jaundice (id=16) — already has some, keep ───
    (16, "कावीळ"),                # Marathi
    (16, "लिव्हर"),               # Marathi colloquial
    (16, "पीलिया रोग"),           # Hindi formal
    
    # ─── Anxiety and Stress (id=1) ───
    (1, "तणाव"),                  # Marathi: stress
    (1, "stress"),
    (1, "anxiety"),
    (1, "टेन्शन"),               # Transliteration
    (1, "मानसिक ताण"),            # Marathi: mental stress
    
    # ─── Recurrent Fever (id=3) ───
    (3, "ताप"),                   # Marathi: fever
    (3, "बुखार"),                 # Hindi: fever
    (3, "fever"),
    (3, "ज्वर"),                  # Sanskrit/formal
    
    # ─── Chronic Skin Disease (id=5) ───
    (5, "त्वचा"),                 # skin
    (5, "skin problem"),
    (5, "skin disease"),
    (5, "एक्झिमा"),              # eczema transliteration
    (5, "दाद"),                   # ringworm Hindi
    
    # ─── Urinary Stones (id=7) ───
    (7, "किडनी स्टोन"),           # transliteration
    (7, "kidney stone"),
    (7, "पथरी"),                  # Hindi
    (7, "मूतखडा"),                # Marathi
    
    # ─── Menstrual Irregularity (id=8) ───
    (8, "मासिक पाळी"),            # Marathi
    (8, "पीरियड्स"),              # transliteration
    (8, "periods problem"),
    (8, "irregular periods"),
    (8, "माहवारी"),               # Hindi
    
    # ─── Osteoporosis (id=13) ───
    (13, "हाडे कमजोर"),           # Marathi
    (13, "हड्डी कमजोर"),          # Hindi
    (13, "bone weakness"),
    (13, "calcium deficiency"),
    
    # ─── Intestinal Worms (id=10) ───
    (10, "जंत"),                  # Marathi: worms
    (10, "कृमी"),                 # Marathi formal
    (10, "पेट के कीड़े"),         # Hindi
    (10, "worms"),
    
    # ─── Neuromuscular Weakness (id=18) ───
    (18, "अशक्तपणा"),            # Marathi: weakness
    (18, "कमजोरी"),              # Hindi: weakness
    (18, "weakness"),
    (18, "nerve weakness"),
    
    # ─── Acne / Pimples (id=184) ───
    (184, "मुरुम"),               # Marathi
    (184, "acne"),
    (184, "pimples"),
]

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Check existing synonyms to avoid duplicates
    existing = set()
    rows = conn.execute("SELECT disease_id, synonym FROM disease_synonyms").fetchall()
    for r in rows:
        existing.add((r["disease_id"], r["synonym"].strip().lower()))
    
    inserted = 0
    skipped = 0
    for disease_id, synonym in SYNONYMS:
        key = (disease_id, synonym.strip().lower())
        if key in existing:
            skipped += 1
            continue
        
        # Verify disease_id exists
        row = conn.execute("SELECT id FROM diseases WHERE id = ?", (disease_id,)).fetchone()
        if not row:
            print(f"  WARNING: disease_id={disease_id} not found, skipping synonym '{synonym}'")
            continue
        
        conn.execute(
            "INSERT INTO disease_synonyms (disease_id, synonym) VALUES (?, ?)",
            (disease_id, synonym)
        )
        existing.add(key)
        inserted += 1
    
    conn.commit()
    
    # Verify
    total = conn.execute("SELECT COUNT(*) FROM disease_synonyms").fetchone()[0]
    print(f"Disease synonyms: inserted={inserted}, skipped(dupes)={skipped}, total_now={total}")
    
    # Quick verification for hypertension
    rows = conn.execute("""
        SELECT ds.synonym, d.name_en 
        FROM disease_synonyms ds 
        JOIN diseases d ON d.id = ds.disease_id 
        WHERE ds.synonym LIKE '%रक्तदाब%' OR ds.synonym LIKE '%hypert%' OR ds.synonym LIKE '%bp%'
    """).fetchall()
    print(f"\nVerification - Hypertension/BP synonyms:")
    for r in rows:
        print(f"  {r['synonym']:30s} -> {r['name_en']}")
    
    conn.close()

if __name__ == "__main__":
    main()
