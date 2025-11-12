# scripts/seed_synonyms.py
"""
Populate plant_synonyms and disease_synonyms tables
Run once to enable better multilingual search
"""
import sqlite3
import sys

# Common plant synonyms (add more as needed)
PLANT_SYNONYMS = [
    # Format: (botanical_name, synonym, language)
    # Ashwagandha
    ("Withania somnifera", "Ashwagandha", "en"),
    ("Withania somnifera", "अश्वगंधा", "hi"),
    ("Withania somnifera", "आश्वगंध", "mr"),
    ("Withania somnifera", "Indian Ginseng", "en"),
    ("Withania somnifera", "Winter Cherry", "en"),
    
    # Tulsi
    ("Ocimum sanctum", "Tulsi", "en"),
    ("Ocimum sanctum", "Holy Basil", "en"),
    ("Ocimum sanctum", "तुलसी", "hi"),
    ("Ocimum sanctum", "तुळस", "mr"),
    
    # Neem
    ("Azadirachta indica", "Neem", "en"),
    ("Azadirachta indica", "नीम", "hi"),
    ("Azadirachta indica", "कडुनिंब", "mr"),
    ("Azadirachta indica", "Margosa", "en"),
    
    # Guduchi/Giloy
    ("Tinospora cordifolia", "Guduchi", "en"),
    ("Tinospora cordifolia", "Giloy", "en"),
    ("Tinospora cordifolia", "गुडूची", "hi"),
    ("Tinospora cordifolia", "गिलोय", "hi"),
    ("Tinospora cordifolia", "गुळवेल", "mr"),
    
    # Amla
    ("Phyllanthus emblica", "Amla", "en"),
    ("Phyllanthus emblica", "Indian Gooseberry", "en"),
    ("Phyllanthus emblica", "आँवला", "hi"),
    ("Phyllanthus emblica", "आमला", "hi"),
    ("Phyllanthus emblica", "आवळा", "mr"),
    
    # Haritaki
    ("Terminalia chebula", "Haritaki", "en"),
    ("Terminalia chebula", "Harad", "en"),
    ("Terminalia chebula", "हरीतकी", "hi"),
    ("Terminalia chebula", "हरड", "hi"),
    ("Terminalia chebula", "हिरडा", "mr"),
    
    # Turmeric
    ("Curcuma longa", "Turmeric", "en"),
    ("Curcuma longa", "हल्दी", "hi"),
    ("Curcuma longa", "हळद", "mr"),
    
    # Ginger
    ("Zingiber officinale", "Ginger", "en"),
    ("Zingiber officinale", "अदरक", "hi"),
    ("Zingiber officinale", "आलं", "mr"),
    ("Zingiber officinale", "सुंठ", "hi"),  # dried
    
    # Brahmi
    ("Bacopa monnieri", "Brahmi", "en"),
    ("Bacopa monnieri", "ब्राह्मी", "hi"),
    ("Bacopa monnieri", "ब्राम्ही", "mr"),
    
    # Shankhpushpi
    ("Convolvulus pluricaulis", "Shankhpushpi", "en"),
    ("Convolvulus pluricaulis", "शंखपुष्पी", "hi"),
    ("Convolvulus pluricaulis", "शंखपुष्पी", "mr"),
    
    # Triphala components
    ("Emblica officinalis", "Amla", "en"),
    ("Terminalia bellirica", "Bibhitaki", "en"),
    ("Terminalia bellirica", "बहेड़ा", "hi"),
    ("Terminalia bellirica", "बेहडा", "mr"),
]

# Common disease synonyms
DISEASE_SYNONYMS = [
    # Format: (disease_name_en, synonym, language)
    # Diabetes
    ("Diabetes Mellitus", "Diabetes", "en"),
    ("Diabetes Mellitus", "Sugar", "en"),
    ("Diabetes Mellitus", "मधुमेह", "hi"),
    ("Diabetes Mellitus", "मधुप्रमेह", "hi"),
    ("Diabetes Mellitus", "मधुमेह", "mr"),
    ("Diabetes Mellitus", "शुगर", "hi"),
    ("Diabetes Mellitus", "डायबिटीज", "hi"),
    
    # Hypertension
    ("Hypertension", "High BP", "en"),
    ("Hypertension", "High Blood Pressure", "en"),
    ("Hypertension", "उच्च रक्तदाब", "hi"),
    ("Hypertension", "बीपी", "hi"),
    ("Hypertension", "उच्च रक्तदाब", "mr"),
    ("Hypertension", "रक्तदाब", "mr"),
    
    # Common Cold
    ("Common Cold", "Cold", "en"),
    ("Common Cold", "सर्दी", "hi"),
    ("Common Cold", "जुकाम", "hi"),
    ("Common Cold", "सर्दी", "mr"),
    ("Common Cold", "प्रतिश्याय", "hi"),
    
    # Cough
    ("Cough", "खांसी", "hi"),
    ("Cough", "खोकला", "mr"),
    ("Cough", "कास", "hi"),
    
    # Fever
    ("Fever", "ज्वर", "hi"),
    ("Fever", "बुखार", "hi"),
    ("Fever", "ताप", "mr"),
    
    # Arthritis
    ("Arthritis", "Joint Pain", "en"),
    ("Arthritis", "गठिया", "hi"),
    ("Arthritis", "संधिवात", "hi"),
    ("Arthritis", "जोडदुखी", "mr"),
    
    # Constipation
    ("Constipation", "कब्ज", "hi"),
    ("Constipation", "बद्धकोष्ठ", "hi"),
    ("Constipation", "बद्धकोष्ठता", "mr"),
    
    # Acidity
    ("Acidity", "Heartburn", "en"),
    ("Acidity", "अम्लपित्त", "hi"),
    ("Acidity", "एसिडिटी", "hi"),
    ("Acidity", "आम्लपित्त", "mr"),
    
    # Indigestion
    ("Indigestion", "अपच", "hi"),
    ("Indigestion", "अजीर्ण", "hi"),
    ("Indigestion", "अपचन", "mr"),
    
    # Insomnia
    ("Insomnia", "Sleeplessness", "en"),
    ("Insomnia", "अनिद्रा", "hi"),
    ("Insomnia", "निद्रानाश", "hi"),
    ("Insomnia", "अनिद्रा", "mr"),
    
    # Asthma
    ("Asthma", "श्वास", "hi"),
    ("Asthma", "दमा", "hi"),
    ("Asthma", "श्वासरोग", "mr"),
]

def seed_synonyms(db_path: str = "herboai.db"):
    """Populate synonym tables"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    print("Seeding plant and disease synonyms...")
    
    # 1. Plant Synonyms
    plant_insert_count = 0
    for botanical_name, synonym, language in PLANT_SYNONYMS:
        # Find plant_id by botanical name
        row = cur.execute(
            "SELECT id FROM plants WHERE botanical_name = ?",
            (botanical_name,)
        ).fetchone()
        
        if not row:
            print(f"  Warning: Plant '{botanical_name}' not found, skipping synonym '{synonym}'")
            continue
        
        plant_id = row["id"]
        
        # Check if synonym already exists
        existing = cur.execute(
            "SELECT id FROM plant_synonyms WHERE plant_id = ? AND synonym = ?",
            (plant_id, synonym)
        ).fetchone()
        
        if existing:
            continue  # Skip duplicates
        
        # Insert
        cur.execute("""
            INSERT INTO plant_synonyms (plant_id, synonym, language)
            VALUES (?, ?, ?, ?)
        """, (plant_id, synonym, language))
        plant_insert_count += 1
    
    conn.commit()
    print(f"✓ Inserted {plant_insert_count} plant synonyms")
    
    # 2. Disease Synonyms
    disease_insert_count = 0
    for disease_name_en, synonym, language in DISEASE_SYNONYMS:
        # Find disease_id by English name
        row = cur.execute(
            "SELECT id FROM diseases WHERE name_en = ?",
            (disease_name_en,)
        ).fetchone()
        
        if not row:
            print(f"  Warning: Disease '{disease_name_en}' not found, skipping synonym '{synonym}'")
            continue
        
        disease_id = row["id"]
        
        # Check if synonym already exists
        existing = cur.execute(
            "SELECT id FROM disease_synonyms WHERE disease_id = ? AND synonym = ?",
            (disease_id, synonym)
        ).fetchone()
        
        if existing:
            continue
        
        # Insert
        cur.execute("""
            INSERT INTO disease_synonyms (disease_id, synonym, language)
            VALUES (?, ?, ?)
        """, (disease_id, synonym, language))
        disease_insert_count += 1
    
    conn.commit()
    print(f"✓ Inserted {disease_insert_count} disease synonyms")
    
    conn.close()
    print("\n✓ Synonym seeding complete!")

if __name__ == "__main__":
    db_path = sys.argv[1] if len(sys.argv) > 1 else "herboai.db"
    seed_synonyms(db_path)