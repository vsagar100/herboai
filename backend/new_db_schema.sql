/* =========================================================
   HerboAI — FULL RESET + SEED (plants+images+remedies+admin)
   - Creates tables (with taste/dosha/system/therapeutic_uses)
   - Sets up FTS5 + triggers
   - Inserts 10 plants (with HI/MR overlays), images, remedies
   - No hardcoded IDs (uses scientific_name to resolve)
========================================================= */

PRAGMA foreign_keys = OFF;
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;

/* -----------------------------
   0) DROP (if present)
------------------------------*/
DROP TRIGGER IF EXISTS plant_ai;
DROP TRIGGER IF EXISTS plant_ad;
DROP TRIGGER IF EXISTS plant_au;
DROP TRIGGER IF EXISTS trg_plant_updated_at;
DROP TRIGGER IF EXISTS remedy_ai;
DROP TRIGGER IF EXISTS remedy_ad;
DROP TRIGGER IF EXISTS remedy_au;

DROP TABLE IF EXISTS image;
DROP TABLE IF EXISTS remedy;
DROP TABLE IF EXISTS plant;
DROP TABLE IF EXISTS admin_user;

-- virtual tables must be dropped explicitly
DROP TABLE IF EXISTS plant_fts;
DROP TABLE IF EXISTS remedy_fts;

PRAGMA foreign_keys = ON;

/* -----------------------------
   1) CREATE TABLES
------------------------------*/
CREATE TABLE plant (
  id                INTEGER PRIMARY KEY,
  name              TEXT NOT NULL,
  scientific_name   TEXT NOT NULL UNIQUE,
  ayush_system      TEXT NOT NULL,
  category          TEXT,
  synonyms          TEXT,
  parts_used        TEXT,
  uses              TEXT,
  phytochemicals    TEXT,
  dosage            TEXT,
  contraindications TEXT,
  formulations      TEXT,
  languages_json    TEXT NOT NULL DEFAULT '{}',
  description       TEXT,
  properties        TEXT,
  -- NEW Ayurveda metadata
  taste             TEXT,
  dosha             TEXT,
  therapeutic_uses  TEXT,
  created_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at        DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE image (
  id         INTEGER PRIMARY KEY,
  plant_id   INTEGER NOT NULL,
  file_path  TEXT NOT NULL UNIQUE,  -- relative path/filename
  alt_text   TEXT,
  FOREIGN KEY (plant_id) REFERENCES plant(id) ON DELETE CASCADE
);

CREATE TABLE remedy (
  id                          INTEGER PRIMARY KEY,
  symptom                     TEXT NOT NULL,        -- canonical label
  diagnosis_pattern           TEXT,
  plant_ids                   TEXT,                 -- CSV of plant ids
  preparation                 TEXT,
  dosage                      TEXT,
  lifestyle_recommendations   TEXT,
  preparation_method          TEXT,
  ayush_system                TEXT,
  side_effects                TEXT,
  contraindications           TEXT,
  languages_json              TEXT NOT NULL DEFAULT '{}',
  created_at                  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE admin_user (
  id             INTEGER PRIMARY KEY,
  username       TEXT NOT NULL UNIQUE,
  password_hash  TEXT NOT NULL,
  created_at     DATETIME DEFAULT CURRENT_TIMESTAMP
);

/* -----------------------------
   2) FTS (contentless) + TRIGGERS
------------------------------*/
CREATE VIRTUAL TABLE plant_fts
USING fts5(
  name,
  scientific_name,
  synonyms,
  uses,
  description,
  properties,
  tokenize = "unicode61"
);

CREATE VIRTUAL TABLE remedy_fts
USING fts5(
  symptom,
  diagnosis_pattern,
  preparation,
  dosage,
  lifestyle_recommendations,
  side_effects,
  contraindications,
  tokenize = "unicode61"
);

-- keep updated_at
CREATE TRIGGER trg_plant_updated_at
AFTER UPDATE ON plant
FOR EACH ROW
BEGIN
  UPDATE plant SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- plant → FTS sync
CREATE TRIGGER plant_ai AFTER INSERT ON plant BEGIN
  INSERT INTO plant_fts(rowid, name, scientific_name, synonyms, uses, description, properties)
  VALUES (NEW.id, NEW.name, NEW.scientific_name, NEW.synonyms, NEW.uses, NEW.description, NEW.properties);
END;

CREATE TRIGGER plant_ad AFTER DELETE ON plant BEGIN
  INSERT INTO plant_fts(plant_fts, rowid) VALUES('delete', OLD.id);
END;

CREATE TRIGGER plant_au AFTER UPDATE ON plant BEGIN
  INSERT INTO plant_fts(plant_fts, rowid) VALUES('delete', OLD.id);
  INSERT INTO plant_fts(rowid, name, scientific_name, synonyms, uses, description, properties)
  VALUES (NEW.id, NEW.name, NEW.scientific_name, NEW.synonyms, NEW.uses, NEW.description, NEW.properties);
END;

-- remedy → FTS sync
CREATE TRIGGER remedy_ai AFTER INSERT ON remedy BEGIN
  INSERT INTO remedy_fts(rowid, symptom, diagnosis_pattern, preparation, dosage, lifestyle_recommendations, side_effects, contraindications)
  VALUES (NEW.id, NEW.symptom, NEW.diagnosis_pattern, NEW.preparation, NEW.dosage, NEW.lifestyle_recommendations, NEW.side_effects, NEW.contraindications);
END;

CREATE TRIGGER remedy_ad AFTER DELETE ON remedy BEGIN
  INSERT INTO remedy_fts(remedy_fts, rowid) VALUES('delete', OLD.id);
END;

CREATE TRIGGER remedy_au AFTER UPDATE ON remedy BEGIN
  INSERT INTO remedy_fts(remedy_fts, rowid) VALUES('delete', OLD.id);
  INSERT INTO remedy_fts(rowid, symptom, diagnosis_pattern, preparation, dosage, lifestyle_recommendations, side_effects, contraindications)
  VALUES (NEW.id, NEW.symptom, NEW.diagnosis_pattern, NEW.preparation, NEW.dosage, NEW.lifestyle_recommendations, NEW.side_effects, NEW.contraindications);
END;

/* -----------------------------
   3) ADMIN
------------------------------*/
INSERT INTO admin_user (username, password_hash)
VALUES ('admin', 'pbkdf2:sha256:260000$demo$replace_with_real_hash');

/* -----------------------------
   4) PLANTS (10) with Ayurveda metadata
------------------------------*/
BEGIN;

INSERT INTO plant
(name, scientific_name, ayush_system, category, synonyms, parts_used, uses, phytochemicals, dosage, contraindications, formulations, languages_json, description, properties, taste, dosha, therapeutic_uses)
VALUES
('Tulsi','Ocimum sanctum','Ayurveda','Respiratory','Holy Basil, तुलसी, तुळस','["Leaves","Stem"]',
 'Used for cough, cold, fever, immunity boost.','Eugenol, Ursolic acid','Decoction 150ml twice daily after meals',
 'Avoid during pregnancy without doctor advice.','Tea, Kashaya (Decoction)',
 '{"hi":{"name":"तुलसी","uses":"खांसी, जुकाम, बुखार","description":"आयुर्वेदिक औषधीय पौधा"},"mr":{"name":"तुळस","uses":"खोकला, सर्दी, ताप"}}',
 'Aromatic shrub widely used in Ayurveda.','Antipyretic, Immunomodulator',
 'Katu (Pungent), Tikta (Bitter)','Balances Kapha/Vata; may increase Pitta in excess',
 'Cough; Cold; Fever; Immunity; Sore Throat'),

('Ashwagandha','Withania somnifera','Ayurveda','Rejuvenative','Indian Ginseng, अश्वगंधा','["Root"]',
 'Improves strength, stamina, stress relief.','Withanolides, Alkaloids','Powder 3-5g with milk once daily.',
 'Avoid in hyperthyroidism.','Churna, Tablet',
 '{"hi":{"name":"अश्वगंधा"},"mr":{"name":"अश्वगंधा"}}',
 'A key adaptogen in Ayurveda.','Adaptogenic, Nervine tonic',
 'Madhura (Sweet), Tikta (Slightly Bitter)','Balances Vata/Pitta; may increase Kapha in excess',
 'Stress; Anxiety; Sleep; Strength; Stamina'),

('Neem','Azadirachta indica','Ayurveda','Skin and Detox','Margosa, नीम, कडुनिंब','["Leaves","Bark","Oil"]',
 'Treats skin disorders, purifies blood, insect repellant.','Azadirachtin, Nimbin','Juice 10ml twice a day.',
 'Avoid during pregnancy.','Oil, Juice, Decoction',
 '{}',
 'Broad-spectrum herbal purifier.','Antimicrobial, Blood purifier',
 'Tikta (Bitter), Kashaya (Astringent)','Balances Pitta/Kapha; may increase Vata',
 'Skin Allergy; Acne; Blood Purifier'),

('Amla','Phyllanthus emblica','Ayurveda','Digestive','Indian Gooseberry, आँवला, आवळा','["Fruit"]',
 'Improves digestion, eye health, hair growth.','Vitamin C, Gallic acid','10–20 ml juice daily.',
 'Avoid in acidity.','Chyawanprash, Rasayanas',
 '{}',
 'Rich source of Vitamin C used in Chyawanprash.','Rejuvenative, Antioxidant',
 'Amla (Sour), Madhura (Sweet)','Balances Tridosha; mainly Pitta pacifying',
 'Digestion; Rasayana; Eye Health; Hair'),

('Giloy','Tinospora cordifolia','Ayurveda','Immunity','Guduchi, गिलोय, गुळवेल','["Stem"]',
 'Boosts immunity, reduces fever.','Tinosporine, Cordifolide','Juice 15ml twice daily.',
 'Avoid in autoimmune diseases.','Juice, Tablet, Decoction',
 '{}',
 'Immune-modulating herb.','Antipyretic, Immunomodulator',
 'Tikta (Bitter)','Balances Pitta/Kapha',
 'Fever; Immunity; Chronic Fatigue'),

('Turmeric','Curcuma longa','Ayurveda','Anti-inflammatory','Haldi, हळद','["Rhizome"]',
 'Wound healing, inflammation, skin glow.','Curcumin','1 tsp with warm milk at night.',
 'Avoid high doses in gallbladder disorders.','Powder, Capsule, Paste',
 '{}',
 'Golden spice with healing power.','Antioxidant, Anti-inflammatory',
 'Katu (Pungent), Tikta (Bitter)','Balances Kapha/Vata; may increase Pitta in excess',
 'Inflammation; Wounds; Skin; Joints'),

('Brahmi','Bacopa monnieri','Ayurveda','Cognitive','Water Hyssop, ब्राह्मी','["Leaves","Whole Plant"]',
 'Enhances memory and focus.','Bacosides','Powder 3g daily or tablet form.',
 'Avoid in low heart rate conditions.','Syrup, Tablet',
 '{}',
 'Brain tonic in Ayurvedic formulations.','Nootropic, Nervine tonic',
 'Tikta (Bitter)','Balances Pitta; may increase Vata if excess',
 'Memory; Focus; Anxiety'),

('Shatavari','Asparagus racemosus','Ayurveda','Reproductive','शतावरी, Satavar','["Root"]',
 'Female tonic, lactation and hormonal balance.','Saponins','Powder 3g twice daily with milk.',
 'Avoid in breast cancer cases.','Churna, Tablet',
 '{}',
 'Used for women’s health.','Galactagogue, Tonic',
 'Madhura (Sweet), Tikta (Bitter)','Balances Vata/Pitta',
 'Female Health; Lactation; Hormonal Support'),

('Bael','Aegle marmelos','Ayurveda','Digestive','Bilva, बेल','["Fruit","Leaves"]',
 'Treats diarrhea, dysentery, gastric problems.','Aegeline, Marmelosin','Fruit pulp 20g twice daily.',
 'Avoid in constipation.','Sharbat, Pulp',
 '{}',
 'Sacred fruit tree for gut health.','Digestive, Antimicrobial',
 'Kashaya (Astringent), Madhura (Sweet)','Balances Kapha/Pitta',
 'Diarrhea; Dysentery; Gut Health'),

('Mulethi','Glycyrrhiza glabra','Ayurveda','Respiratory','Licorice, मुलेठी, यष्टिमधु','["Root"]',
 'Soothes throat, cough and acidity.','Glycyrrhizin, Liquiritin','Powder 2g with honey twice daily.',
 'Avoid in high blood pressure.','Churna, Tablet',
 '{}',
 'Sweet root herb for throat and GI relief.','Expectorant, Demulcent',
 'Madhura (Sweet)','Increases Kapha if excess; pacifies Vata/Pitta',
 'Cough; Sore Throat; Acidity');

COMMIT;

/* -----------------------------
   5) IMAGES
------------------------------*/
BEGIN;
INSERT INTO image (plant_id, file_path, alt_text) VALUES
((SELECT id FROM plant WHERE scientific_name='Ocimum sanctum'),'tulsi.jpg','Tulsi Plant'),
((SELECT id FROM plant WHERE scientific_name='Withania somnifera'),'ashwagandha.jpg','Ashwagandha Roots'),
((SELECT id FROM plant WHERE scientific_name='Azadirachta indica'),'neem.jpg','Neem Leaves'),
((SELECT id FROM plant WHERE scientific_name='Phyllanthus emblica'),'amla.jpg','Amla Fruit'),
((SELECT id FROM plant WHERE scientific_name='Tinospora cordifolia'),'giloy.jpg','Giloy Stem'),
((SELECT id FROM plant WHERE scientific_name='Curcuma longa'),'turmeric.jpg','Turmeric Rhizome'),
((SELECT id FROM plant WHERE scientific_name='Bacopa monnieri'),'brahmi.jpg','Brahmi Herb'),
((SELECT id FROM plant WHERE scientific_name='Asparagus racemosus'),'shatavari.jpg','Shatavari Root'),
((SELECT id FROM plant WHERE scientific_name='Aegle marmelos'),'bael.jpg','Bael Fruit'),
((SELECT id FROM plant WHERE scientific_name='Glycyrrhiza glabra'),'mulethi.jpg','Mulethi Root');
COMMIT;

/* -----------------------------
   6) REMEDIES (no hardcoded IDs)
------------------------------*/
BEGIN;

INSERT INTO remedy
(symptom, diagnosis_pattern, plant_ids, preparation, dosage, lifestyle_recommendations, preparation_method, ayush_system, side_effects, contraindications, languages_json)
VALUES
('Cough','dry cough, sore throat',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Ocimum sanctum') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Glycyrrhiza glabra') AS TEXT)),
 'Boil 10 Tulsi leaves + 2g Mulethi in 250ml water 10 min; add honey.',
 '150ml warm infusion twice daily after meals.',
 'Avoid cold drinks, rest voice, take steam.','Decoction','Ayurveda',
 'Excess Mulethi may raise BP.','Pregnancy consult doctor.',
 '{"hi":{"symptom":"खांसी","preparation":"250 ml पानी में 10 तुलसी पत्ते + 2g मुलेठी उबालें।"},"mr":{"symptom":"खोकला","preparation":"250 ml पाण्यात 10 तुळशीची पाने + 2g ज्येष्ठमध उकळा."}}'),

('Fever','viral fever, typhoid, chronic fever',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Tinospora cordifolia') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Ocimum sanctum') AS TEXT)),
 'Giloy stem + Tulsi leaves decoction 150ml twice daily.',
 '150ml twice daily after meals.',
 'Stay hydrated, avoid heavy food.','Kadha','Ayurveda',
 '—','Autoimmune disorder: avoid Giloy.','{}'),

('Indigestion','gas, bloating, loss of appetite',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Phyllanthus emblica') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Aegle marmelos') AS TEXT)),
 'Amla juice 20ml with Bael pulp.',
 'Once or twice daily.','Eat light, avoid fried food.','Juice blend','Ayurveda',
 '—','Acidity caution.','{}'),

('Stress & Anxiety','tension, sleeplessness',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Withania somnifera') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Bacopa monnieri') AS TEXT)),
 'Ashwagandha + Brahmi powder (3g each) with milk before sleep.',
 'Once daily at night.','Meditate, avoid caffeine.','Churna Mix','Ayurveda',
 'Mild drowsiness.','Thyroid disorders: avoid Ashwagandha.','{}'),

('Skin Allergy','eczema, itching, acne',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Azadirachta indica') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Curcuma longa') AS TEXT)),
 'Apply paste of Neem + Turmeric on affected area.',
 'Twice daily application.','Hygiene, avoid spicy food.','Paste','Ayurveda',
 'Irritation in sensitive skin.','Avoid near eyes.','{}'),

('Respiratory Weakness','bronchitis, asthma',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Glycyrrhiza glabra') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Ocimum sanctum') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Tinospora cordifolia') AS TEXT)),
 'Mulethi, Tulsi, Giloy decoction 200ml.',
 'Twice daily warm.','Avoid dust exposure.','Kadha','Ayurveda',
 '—','Pregnant/lactating: consult physician.','{}'),

('Low Immunity','frequent cold, weak stamina',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Tinospora cordifolia') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Phyllanthus emblica') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Withania somnifera') AS TEXT)),
 'Giloy, Amla, Ashwagandha combination.',
 'One dose daily morning.','Sleep early, healthy diet.','Decoction','Ayurveda',
 '—','Autoimmune: avoid Giloy.','{}'),

('Acidity','heartburn, reflux',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Glycyrrhiza glabra') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Phyllanthus emblica') AS TEXT)),
 'Mulethi powder with Amla juice.',
 'Once daily after meal.','Avoid spicy and oily foods.','Churna','Ayurveda',
 'Mulethi may raise BP.','Hypertension.','{}'),

('Female Health','hormonal imbalance, lactation',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Asparagus racemosus') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Phyllanthus emblica') AS TEXT)),
 'Shatavari powder with Amla juice 10ml.',
 'Twice daily.','Yoga, balanced diet.','Churna','Ayurveda',
 '—','Breast cancer cases avoid.','{}'),

('Joint Pain','arthritis, inflammation',
 (SELECT CAST((SELECT id FROM plant WHERE scientific_name='Curcuma longa') AS TEXT) || ',' ||
         CAST((SELECT id FROM plant WHERE scientific_name='Tinospora cordifolia') AS TEXT)),
 'Turmeric milk + Giloy decoction.',
 'Night dose.','Warm compress, mild exercise.','Milk & Decoction','Ayurveda',
 '—','Gallbladder issues: avoid high turmeric doses.','{}');

COMMIT;

/* -----------------------------
   7) QUICK CHECKS (optional)
------------------------------*/
-- SELECT id,name,scientific_name FROM plant ORDER BY id;
-- SELECT plant_id,file_path FROM image ORDER BY plant_id;
-- SELECT id,symptom,plant_ids FROM remedy ORDER BY id LIMIT 10;
