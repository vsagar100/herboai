
-- ============================================================================
-- SEED DATA (20+ plants, selected diseases, mappings, preparations)
-- Keep inserts concise; extended fields can be added later.
-- ============================================================================

-- Diseases
INSERT INTO diseases (name_en, name_hi, name_mr, category, ayurvedic_name, description, severity_level)
VALUES
('Type 2 Diabetes','मधुमेह','मधुमेह','metabolic','मधुमेह','Chronic elevation of blood sugar','chronic'),
('Common Cold','सर्दी-जुकाम','सर्दी-जुकाम','respiratory','प्रतिश्याय','Viral upper respiratory infection','mild'),
('Arthritis','गठिया','सांधेदुखी','musculoskeletal','आमवात','Joint inflammation and pain','moderate'),
('Hypertension','उच्च रक्तचाप','उच्च रक्तदाब','cardiovascular','रक्तगत वात','Elevated blood pressure','moderate'),
('Indigestion','अपच','अपचन','digestive','अजीर्ण','Impaired digestion','mild');

-- Plants (20 entries)
INSERT INTO plants (botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name, family, description, parts_used, rasa, virya, vipaka, guna, dosha_effect, therapeutic_actions)
VALUES
('Withania somnifera','Ashwagandha','अश्वगंधा','आश्वगंधा','अश्वगन्धा','Solanaceae','Adaptogenic Rasayana','["root","leaf"]','["tikta","madhura"]','ushna','madhura','["laghu","snigdha"]','{"vata":"reduces","pitta":"neutral","kapha":"reduces"}','["adaptogen","anxiolytic"]'),
('Ocimum sanctum','Holy Basil','तुलसी','तुळस','तुलसी','Lamiaceae','Respiratory & immunity support','["leaf","seed"]','["tikta","katu"]','ushna','katu','["laghu","ruksha"]','{"vata":"neutral","pitta":"slight_increase","kapha":"reduces"}','["antimicrobial","immunomodulator"]'),
('Terminalia chebula','Chebulic Myrobalan','हरड़','हिरडा','हरीतकी','Combretaceae','Triphala component','["fruit"]','["kashaya","amla"]','ushna','madhura','["laghu","ruksha"]','{"vata":"reduces","pitta":"reduces","kapha":"reduces"}','["laxative","digestive"]'),
('Phyllanthus emblica','Indian Gooseberry','आंवला','आवळा','आमलकी','Phyllanthaceae','Vitamin C rich Rasayana','["fruit"]','["amla","kashaya"]','sheeta','madhura','["laghu","ruksha"]','{"vata":"reduces","pitta":"reduces","kapha":"reduces"}','["antioxidant","immunomodulator"]'),
('Gymnema sylvestre','Gudmar','गुड़मार','कवळी','मधुनाशिनी','Apocynaceae','Sugar-destroyer for diabetes','["leaf"]','["tikta","kashaya"]','ushna','katu','["laghu","ruksha"]','{"kapha":"reduces"}','["anti-diabetic","hypoglycemic"]'),
('Azadirachta indica','Neem','नीम','कडूलिंब','निम्ब','Meliaceae','Village pharmacy','["leaf","bark","seed"]','["tikta","kashaya"]','sheeta','katu','["laghu","ruksha"]','{"pitta":"reduces","kapha":"reduces"}','["antimicrobial","blood_purifier"]'),
('Curcuma longa','Turmeric','हल्दी','हळद','हरिद्रा','Zingiberaceae','Anti-inflammatory golden spice','["rhizome"]','["tikta","katu"]','ushna','katu','["laghu","ruksha"]','{"kapha":"reduces"}','["anti-inflammatory","antioxidant"]'),
('Zingiber officinale','Ginger','अदरक','आलं','आर्द्रक','Zingiberaceae','Digestive & anti-nausea','["rhizome"]','["katu"]','ushna','madhura','["laghu","snigdha"]','{"vata":"reduces","kapha":"reduces"}','["digestive","expectorant"]'),
('Bacopa monnieri','Brahmi','ब्राह्मी','ब्राह्मी','ब्राह्मी','Plantaginaceae','Mind & memory tonic','["whole_plant"]','["tikta","kashaya"]','sheeta','madhura','["laghu"]','{"vata":"reduces","pitta":"reduces"}','["nootropic","anxiolytic"]'),
('Convolvulus pluricaulis','Shankhpushpi','शंखपुष्पी','शंखपुष्पी','शंखपुष्पी','Convolvulaceae','Brain tonic','["whole_plant"]','["madhura","tikta"]','sheeta','madhura','["laghu","snigdha"]','{"vata":"reduces","pitta":"reduces"}','["nootropic","sedative"]'),
('Tinospora cordifolia','Giloy','गिलोय','गुळवेल','गुडूची','Menispermaceae','Immunity & antipyretic','["stem"]','["tikta"]','ushna','madhura','["laghu"]','{"pitta":"reduces","kapha":"reduces"}','["immunomodulator","antipyretic"]'),
('Trigonella foenum-graecum','Fenugreek','मेथी','मेथी','मेथिका','Fabaceae','Glucose metabolism support','["seed","leaf"]','["tikta","kashaya"]','ushna','katu','["guru","snigdha"]','{"kapha":"reduces"}','["anti-diabetic","galactagogue"]'),
('Vitex negundo','Nirgundi','निर्गुंडी','निर्गुंडी','निरगुंडी','Lamiaceae','Anti-inflammatory, joint pains','["leaf"]','["tikta","katu"]','ushna','katu','["laghu","ruksha"]','{"vata":"reduces"}','["analgesic","anti-inflammatory"]'),
('Commiphora wightii','Guggulu','गुग्गुलु','गुग्गुळ','गुग्गुलु','Burseraceae','Lipid & joint health','["resin"]','["tikta","katu"]','ushna','katu','["laghu","ruksha"]','{"vata":"reduces","kapha":"reduces"}','["hypolipidemic","anti-inflammatory"]'),
('Boswellia serrata','Shallaki','शल्लकी','सालई','शल्लकी','Burseraceae','Joint anti-inflammatory','["resin"]','["kashaya","tikta"]','ushna','katu','["laghu","ruksha"]','{"vata":"reduces"}','["anti-inflammatory"]'),
('Terminalia arjuna','Arjuna','अर्जुन','अर्जुन','अर्जुन','Combretaceae','Cardio-protective bark','["bark"]','["kashaya"]','sheeta','katu','["guru","ruksha"]','{"pitta":"reduces"}','["cardioprotective"]'),
('Glycyrrhiza glabra','Licorice','मुलेठी','यष्टिमधु','यष्टिमधु','Fabaceae','Soothing demulcent','["root"]','["madhura"]','sheeta','madhura','["guru","snigdha"]','{"vata":"reduces","pitta":"reduces"}','["demulcent","anti-ulcer"]'),
('Asparagus racemosus','Shatavari','शतावरी','शतावरी','शतावरी','Asparagaceae','Female tonic','["root"]','["madhura","tikta"]','sheeta','madhura','["guru","snigdha"]','{"pitta":"reduces","vata":"reduces"}','["galactagogue","adaptogen"]'),
('Tribulus terrestris','Gokshura','गोक्षुरा','गोकशुरा','गोक्षुर','Zygophyllaceae','Diuretic & renal','["fruit"]','["madhura","tikta"]','sheeta','madhura','["laghu"]','{"vata":"reduces"}','["diuretic","nephroprotective"]'),
('Eclipta alba','Bhringraj','भृंगराज','भृंगराज','भृंगराज','Asteraceae','Hair & liver support','["leaf"]','["tikta"]','sheeta','katu','["laghu"]','{"pitta":"reduces"}','["hepatoprotective","hair_tonic"]');

-- Synonyms (a few examples)
INSERT INTO plant_synonyms (plant_id, synonym, language, kind)
SELECT id, 'Indian Ginseng','en','trade_name' FROM plants WHERE botanical_name='Withania somnifera';
INSERT INTO plant_synonyms (plant_id, synonym, language, kind)
SELECT id, 'Holy Basil','en','common_name' FROM plants WHERE botanical_name='Ocimum sanctum';

-- Basic media records
INSERT INTO media (plant_id, path, alt_text, is_primary)
SELECT id, 'images/ashwagandha.jpg','Ashwagandha',1 FROM plants WHERE botanical_name='Withania somnifera';
INSERT INTO media (plant_id, path, alt_text, is_primary)
SELECT id, 'images/tulsi.jpg','Tulsi',1 FROM plants WHERE botanical_name='Ocimum sanctum';

-- Plant ↔ Disease mappings (sample)
-- Diabetes: Gudmar, Fenugreek, Amla, Turmeric
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 5, 'traditional', 'Improves glucose tolerance'
FROM plants p JOIN diseases d
ON p.botanical_name='Gymnema sylvestre' AND d.name_en='Type 2 Diabetes';
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 4, 'traditional', 'Delays carb absorption'
FROM plants p JOIN diseases d
ON p.botanical_name='Trigonella foenum-graecum' AND d.name_en='Type 2 Diabetes';
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 3, 'traditional', 'Antioxidant improves beta-cell health'
FROM plants p JOIN diseases d
ON p.botanical_name='Phyllanthus emblica' AND d.name_en='Type 2 Diabetes';
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 3, 'traditional', 'Anti-inflammatory aids metabolic health'
FROM plants p JOIN diseases d
ON p.botanical_name='Curcuma longa' AND d.name_en='Type 2 Diabetes';

-- Common Cold: Tulsi, Ginger
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 4, 'traditional', 'Expectorant & antimicrobial'
FROM plants p JOIN diseases d
ON p.botanical_name='Ocimum sanctum' AND d.name_en='Common Cold';
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 4, 'traditional', 'Warming digestive, reduces nausea'
FROM plants p JOIN diseases d
ON p.botanical_name='Zingiber officinale' AND d.name_en='Common Cold';

-- Arthritis: Nirgundi, Shallaki, Guggulu, Turmeric
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 4, 'traditional', 'Analgesic anti-inflammatory'
FROM plants p JOIN diseases d
ON p.botanical_name='Vitex negundo' AND d.name_en='Arthritis';
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 4, 'traditional', 'Boswellic acids reduce inflammation'
FROM plants p JOIN diseases d
ON p.botanical_name='Boswellia serrata' AND d.name_en='Arthritis';
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 4, 'traditional', 'Resin supports joint health'
FROM plants p JOIN diseases d
ON p.botanical_name='Commiphora wightii' AND d.name_en='Arthritis';
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 3, 'traditional', 'Inflammation modulation'
FROM plants p JOIN diseases d
ON p.botanical_name='Curcuma longa' AND d.name_en='Arthritis';

-- Hypertension: Arjuna
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 4, 'traditional', 'Cardiotonic, improves LV function'
FROM plants p JOIN diseases d
ON p.botanical_name='Terminalia arjuna' AND d.name_en='Hypertension';

-- Indigestion: Triphala components + Ginger
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 4, 'traditional', 'Improves gut motility'
FROM plants p JOIN diseases d
ON p.botanical_name='Terminalia chebula' AND d.name_en='Indigestion';
INSERT INTO plant_disease_mapping (plant_id, disease_id, efficacy_level, evidence_type, mechanism)
SELECT p.id, d.id, 3, 'traditional', 'Carminative, enhances agni'
FROM plants p JOIN diseases d
ON p.botanical_name='Zingiber officinale' AND d.name_en='Indigestion';

-- Preparations
INSERT INTO preparations (name_en, name_hi, name_mr, classical_name, ayush_system_id, form_type, category, preparation_steps, duration, dosage_json, timing, anupana, notes)
VALUES
('Gudmar Decoction','गुड़मार का काढ़ा','गुड़मार काढा','Gudmar Kwatha',1,'decoction','single_herb','["Boil leaves in water","Reduce to 1/4","Filter"]','20 min','{"adult":"80-100 ml twice daily","child":"20-30 ml twice daily"}','after_food','water','Monitor glucose levels'),
('Tulsi-Ginger Tea','तुलसी-अदरक चाय','तुलसी-आलं काढा',NULL,1,'decoction','compound','["Boil tulsi leaves and ginger","Simmer 5-7 min","Serve warm"]','10 min','{"adult":"150 ml 2-3x/day"}','after_food','honey (optional)','For common cold'),
('Triphala Churna','त्रिफला चूर्ण','त्रिफळा चूर्ण',NULL,1,'powder','compound','["Dry fruits","Powder and sieve","Store airtight"]',NULL,'{"adult":"3-5 g with warm water at bedtime"}','empty_stomach','warm water','For indigestion & constipation'),
('Arjuna Kwatha','अर्जुन का काढ़ा','अर्जुन काढा',NULL,1,'decoction','single_herb','["Boil bark pieces","Reduce to 1/4","Filter"]','20-25 min','{"adult":"80-100 ml twice daily"}','after_food','milk or water','For hypertension/cardiac support');

-- Preparation ingredients linking
INSERT INTO preparation_ingredients (preparation_id, plant_id, part, quantity_value, quantity_unit)
SELECT pr.id, p.id, 'leaf', 10, 'g'
FROM preparations pr, plants p
WHERE pr.name_en='Gudmar Decoction' AND p.botanical_name='Gymnema sylvestre';

INSERT INTO preparation_ingredients (preparation_id, plant_id, part, quantity_value, quantity_unit)
SELECT pr.id, p.id, 'leaf', 5, 'g'
FROM preparations pr, plants p
WHERE pr.name_en='Tulsi-Ginger Tea' AND p.botanical_name='Ocimum sanctum';
INSERT INTO preparation_ingredients (preparation_id, plant_id, part, quantity_value, quantity_unit)
SELECT pr.id, p.id, 'rhizome', 5, 'g'
FROM preparations pr, plants p
WHERE pr.name_en='Tulsi-Ginger Tea' AND p.botanical_name='Zingiber officinale';

INSERT INTO preparation_ingredients (preparation_id, plant_id, part, quantity_value, quantity_unit)
SELECT pr.id, p.id, 'fruit', 1, 'part'
FROM preparations pr, plants p
WHERE pr.name_en='Triphala Churna' AND p.botanical_name='Terminalia chebula';

INSERT INTO preparation_ingredients (preparation_id, plant_id, part, quantity_value, quantity_unit)
SELECT pr.id, p.id, 'bark', 20, 'g'
FROM preparations pr, plants p
WHERE pr.name_en='Arjuna Kwatha' AND p.botanical_name='Terminalia arjuna';

-- Preparation indications
INSERT INTO preparation_indications (preparation_id, disease_id, strength, evidence_type, notes)
SELECT pr.id, d.id, 5, 'traditional', 'Blood sugar support'
FROM preparations pr, diseases d
WHERE pr.name_en='Gudmar Decoction' AND d.name_en='Type 2 Diabetes';

INSERT INTO preparation_indications (preparation_id, disease_id, strength, evidence_type, notes)
SELECT pr.id, d.id, 4, 'traditional', 'Cold & cough relief'
FROM preparations pr, diseases d
WHERE pr.name_en='Tulsi-Ginger Tea' AND d.name_en='Common Cold';

INSERT INTO preparation_indications (preparation_id, disease_id, strength, evidence_type, notes)
SELECT pr.id, d.id, 4, 'traditional', 'Digestive regulation'
FROM preparations pr, diseases d
WHERE pr.name_en='Triphala Churna' AND d.name_en='Indigestion';

INSERT INTO preparation_indications (preparation_id, disease_id, strength, evidence_type, notes)
SELECT pr.id, d.id, 4, 'traditional', 'Cardiac support'
FROM preparations pr, diseases d
WHERE pr.name_en='Arjuna Kwatha' AND d.name_en='Hypertension';

-- Safety examples
INSERT INTO contraindications (plant_id, condition, severity, details)
SELECT id, 'pregnancy','cautionary','High doses may not be advisable' FROM plants WHERE botanical_name='Withania somnifera';

INSERT INTO interactions (plant_id, interaction_type, interaction_with, effect, severity, recommendation)
SELECT id, 'drug','antidiabetic agents','May potentiate hypoglycemia','moderate','Monitor glucose & adjust dose'
FROM plants WHERE botanical_name='Gymnema sylvestre';
