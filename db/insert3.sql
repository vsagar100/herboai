INSERT OR IGNORE INTO plants (
  botanical_name,
  common_name_en,
  common_name_hi,
  common_name_mr,
  sanskrit_name,
  family,
  description,
  habitat,
  parts_used,
  rasa,
  virya,
  vipaka,
  guna,
  dosha_effect,
  prabhava,
  active_compounds,
  therapeutic_actions,
  classical_references,
  is_endangered,
  cultivation_status,
  image_hero,
  ayush_system
) VALUES
-- 71. Indian Gooseberry (Amalaki)
('Phyllanthus emblica',
 'Indian Gooseberry',
 'आंवला',
 'आवळा',
 'Amalaki',
 'Phyllanthaceae',
 'Small deciduous tree; fruits are a key Rasayana used to support immunity, digestion, skin and longevity.',
 'Wild and cultivated throughout India in dry and moist deciduous regions.',
 '["fruit"]',
 '["amla_mixed_rasas"]',
 'sheeta',
 'madhura',
 '["guru","ruksha"]',
 '["pitta_pacifying","tridosha_balancing"]',
 NULL,
 '["vitamin_C","tannins","polyphenols"]',
 '["rejuvenative","antioxidant","digestive","supportive_in_diabetes"]',
 '["Charaka Samhita","Sushruta Samhita"]',
 0,
 'wild_and_cultivated',
 'Indian_Gooseberry.jpg',
 'ayurveda'),

-- 72. Haritaki
('Terminalia chebula',
 'Haritaki',
 'हरड़ (हरितकी)',
 'हरडे',
 'Haritaki',
 'Combretaceae',
 'Medium-sized tree; fruits are part of Triphala and used for digestion, bowel regulation and Rasayana.',
 'Dry deciduous forests and hill slopes in India and Southeast Asia.',
 '["fruit"]',
 '["kashaya","tikta","madhura"]',
 'ushna',
 'madhura',
 '["laghu","ruksha"]',
 '["vata_pacifying","tridosha_balancing"]',
 NULL,
 '["chebulinic_acid","gallic_acid","tannins"]',
 '["mild_laxative","digestive","antioxidant","rasayana"]',
 '["Charaka Samhita"]',
 0,
 'wild_and_cultivated',
 'Haritaki.jpg',
 'ayurveda'),

-- 73. Bibhitaki
('Terminalia bellirica',
 'Bibhitaki',
 'बहेरा',
 'बहेरा',
 'Bibhitaka',
 'Combretaceae',
 'Large tree; fruits are one of the Triphala components, used in respiratory and metabolic disorders.',
 'Moist and dry deciduous forests, avenues and village groves.',
 '["fruit"]',
 '["kashaya"]',
 'ushna',
 'madhura',
 '["laghu","ruksha"]',
 '["kapha_pacifying","pitta_pacifying"]',
 NULL,
 '["tannins","ellagic_acid"]',
 '["expectorant","astringent","mild_laxative","triphala_component"]',
 '["Bhava Prakasha"]',
 0,
 'wild_and_cultivated',
 'Bibhitaki.jpg',
 'ayurveda'),

-- 74. Turmeric
('Curcuma longa',
 'Turmeric',
 'हल्दी',
 'हळद',
 'Haridra',
 'Zingiberaceae',
 'Rhizomatous herb; rhizome used widely as spice and medicine for skin, liver and inflammatory conditions.',
 'Cultivated in warm, humid regions; common in Indian farms and home gardens.',
 '["rhizome"]',
 '["tikta","katu"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","pitta_pacifying"]',
 NULL,
 '["curcumin","turmerones"]',
 '["anti-inflammatory","hepatoprotective","wound_healing","skin_support"]',
 '["Charaka Samhita","Sushruta Samhita"]',
 0,
 'cultivated',
 'Turmeric.jpg',
 'ayurveda'),

-- 75. Ginger
('Zingiber officinale',
 'Ginger',
 'अदरक',
 'आले',
 'Shunthi / Ardraka',
 'Zingiberaceae',
 'Perennial herb; fresh and dry rhizome used for digestion, nausea, circulation and respiratory support.',
 'Widely cultivated in tropical and subtropical regions.',
 '["rhizome_fresh","rhizome_dry"]',
 '["katu"]',
 'ushna',
 'madhura',
 '["laghu","snigdha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["gingerols","shogaols"]',
 '["carminative","antiemetic","circulatory_stimulant","expectorant"]',
 NULL,
 0,
 'cultivated',
 'Ginger.jpg',
 'ayurveda'),

-- 76. Coriander
('Coriandrum sativum',
 'Coriander',
 'धनिया',
 'कोथिंबीर',
 'Dhanyaka',
 'Apiaceae',
 'Soft aromatic herb; leaves and seeds used as cooling digestive and mild diuretic.',
 'Cultivated extensively in fields and kitchen gardens.',
 '["leaf","seed"]',
 '["madhura","tikta"]',
 'sheeta',
 'madhura',
 '["laghu"]',
 '["pitta_pacifying","vata_pacifying"]',
 NULL,
 '["linalool","essential_oils"]',
 '["digestive","carminative","cooling","diuretic_mild"]',
 NULL,
 0,
 'cultivated',
 'Coriander.jpg',
 'ayurveda'),

-- 77. Cumin
('Cuminum cyminum',
 'Cumin',
 'जीरा',
 'जिरे',
 'Jiraka',
 'Apiaceae',
 'Annual herb; seeds are important kitchen spice used to aid digestion and relieve bloating.',
 'Cultivated in dry temperate and semi-arid regions.',
 '["seed"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["cuminaldehyde","terpenes"]',
 '["carminative","digestive","mild_lactagogue"]',
 NULL,
 0,
 'cultivated',
 'Cumin.jpg',
 'ayurveda'),

-- 78. Fennel
('Foeniculum vulgare',
 'Fennel',
 'सौंफ',
 'बडीशेप',
 'Mishreya',
 'Apiaceae',
 'Aromatic herb; seeds are used as sweet digestive, carminative and cooling mouth freshener.',
 'Cultivated widely in plains and semi-arid regions.',
 '["seed"]',
 '["madhura","tikta"]',
 'sheeta',
 'madhura',
 '["laghu","snigdha_mild"]',
 '["pitta_pacifying","vata_pacifying"]',
 NULL,
 '["anethole","fenchone"]',
 '["carminative","digestive","galactagogue_mild","cooling"]',
 NULL,
 0,
 'cultivated',
 'Fennel.jpg',
 'ayurveda'),

-- 79. Ajwain
('Trachyspermum ammi',
 'Ajwain',
 'अजवाइन',
 'ओवा',
 'Yavani',
 'Apiaceae',
 'Strongly aromatic seed; used to reduce gas, abdominal colic and Kapha in digestion and respiration.',
 'Cultivated in dry fields of North and West India.',
 '["seed"]',
 '["katu"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["thymol","essential_oils"]',
 '["carminative","antispasmodic","digestive","mild_bronchodilator"]',
 NULL,
 0,
 'cultivated',
 'Ajwain.jpg',
 'ayurveda'),

-- 80. Fenugreek
('Trigonella foenum-graecum',
 'Fenugreek',
 'मेथी',
 'मेथी',
 'Methi',
 'Fabaceae',
 'Annual herb; seeds and leaves used for digestion, lactation support and metabolic balance.',
 'Cultivated as winter crop and kitchen garden plant.',
 '["seed","leaf"]',
 '["tikta","katu"]',
 'ushna',
 'katu',
 '["guru","snigdha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["saponins","fenugreek_fiber"]',
 '["digestive","hypoglycemic_support","galactagogue","lipid_support"]',
 NULL,
 0,
 'cultivated',
 'Fenugreek.jpg',
 'ayurveda'),

-- 81. Green Cardamom
('Elettaria cardamomum',
 'Green Cardamom',
 'इलायची',
 'वेलची',
 'Ela',
 'Zingiberaceae',
 'Perennial herb; aromatic seed used as carminative, mouth freshener and mild respiratory support.',
 'Shade-grown plantations in humid hilly regions.',
 '["seed"]',
 '["madhura","katu","tikta"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '["pitta_pacifying","kapha_pacifying"]',
 NULL,
 '["cineole","terpenes","essential_oils"]',
 '["carminative","digestive","mild_expectorant","mouth_freshener"]',
 NULL,
 0,
 'cultivated',
 'Green_Cardamom.jpg',
 'ayurveda'),

-- 82. Clove
('Syzygium aromaticum',
 'Clove',
 'लौंग',
 'लवंग',
 'Lavanga',
 'Myrtaceae',
 'Evergreen tree; dried flower buds used as warming aromatic for toothache, digestion and respiratory support.',
 'Cultivated in humid tropical coastal regions.',
 '["flower_bud"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","tikshna"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["eugenol","essential_oils"]',
 '["analgesic_dental","carminative","antimicrobial","expectorant_mild"]',
 NULL,
 0,
 'cultivated',
 'Clove.jpg',
 'ayurveda'),

-- 83. Cinnamon
('Cinnamomum verum',
 'Cinnamon',
 'दालचीनी',
 'दालचिनी',
 'Tvak',
 'Lauraceae',
 'Medium tree; inner bark used as warming spice to support circulation, digestion and glycemic balance.',
 'Cultivated plantations in humid tropical and sub-tropical climates.',
 '["bark"]',
 '["katu","madhura","tikta"]',
 'ushna',
 'katu',
 '["laghu","tikshna"]',
 '["vata_pacifying","kapha_pacifying"]',
 NULL,
 '["cinnamaldehyde","eugenol"]',
 '["carminative","digestive","circulatory_stimulant","metabolic_support"]',
 NULL,
 0,
 'cultivated',
 'Cinnamon.jpg',
 'ayurveda'),

-- 84. Curry Leaf
('Murraya koenigii',
 'Curry Leaf',
 'करी पत्ता',
 'कढीपत्ता',
 'Krishnanimba / Surabhinimba',
 'Rutaceae',
 'Small tree or shrub; leaves used as aromatic spice and for digestion, hair and metabolic support.',
 'Common in home gardens, hedges and field borders in tropical India.',
 '["leaf"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["carbazole_alkaloids","essential_oils"]',
 '["digestive","antioxidant","hair_support","metabolic_support_mild"]',
 NULL,
 0,
 'cultivated',
 'Curry_Leaf.jpg',
 'ayurveda'),

-- 85. Sacred Lotus
('Nelumbo nucifera',
 'Sacred Lotus',
 'कमल',
 'कमळ',
 'Padma',
 'Nelumbonaceae',
 'Aquatic plant; flowers, seeds and rhizomes used as cooling, hemostatic and mind-calming agents.',
 'Lakes, ponds and slow-moving water bodies across Asia.',
 '["flower","seed","rhizome"]',
 '["madhura","kashaya"]',
 'sheeta',
 'madhura',
 '["guru","snigdha"]',
 '["pitta_pacifying","rakta_pacifying"]',
 NULL,
 '["flavonoids","alkaloids"]',
 '["cooling","hemostatic","sedative_mild"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Sacred_Lotus.jpg',
 'ayurveda'),

-- 86. Rose
('Rosa centifolia',
 'Rose',
 'गुलाब',
 'गुलाब',
 'Shatapatri',
 'Rosaceae',
 'Shrub with fragrant flowers; petals used as heart-soothing, mild laxative and cooling agent.',
 'Cultivated in gardens and farms; some wild varieties in temperate hills.',
 '["flower_petals"]',
 '["madhura","kashaya"]',
 'sheeta',
 'madhura',
 '["laghu","snigdha"]',
 '["pitta_pacifying","sadhaka_pitta_support"]',
 NULL,
 '["essential_oils","flavonoids"]',
 '["cooling","mild_laxative","cardiac_mind_soothing"]',
 NULL,
 0,
 'cultivated',
 'Rose.jpg',
 'ayurveda'),

-- 87. Aloe Vera
('Aloe barbadensis miller',
 'Aloe Vera',
 'घृतकुमारी',
 'कोरफड',
 'Kumari',
 'Asphodelaceae',
 'Succulent herb; leaf gel used for skin, digestion and gynecological support.',
 'Cultivated in dry and semi-arid regions, also as pot plant.',
 '["leaf_gel"]',
 '["tikta","madhura"]',
 'sheeta',
 'madhura',
 '["snigdha"]',
 '["pitta_pacifying","rakta_pacifying"]',
 NULL,
 '["aloins","polysaccharides"]',
 '["skin_healing","digestive_support","cooling","gynecological_support_traditional"]',
 NULL,
 0,
 'cultivated',
 'Aloe_Vera.jpg',
 'ayurveda'),

-- 88. Sesame
('Sesamum indicum',
 'Sesame',
 'तिल',
 'तीळ',
 'Tila',
 'Pedaliaceae',
 'Annual herb; seeds and oil used as nutritive, Vata-pacifying and base oil in many Ayurvedic formulations.',
 'Cultivated in semi-arid and dry regions.',
 '["seed","oil"]',
 '["madhura","tikta"]',
 'ushna',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying"]',
 NULL,
 '["sesamin","sesamolin","unsaturated_fats"]',
 '["balya_tonic","snigdha_laxative","skin_nourishing"]',
 NULL,
 0,
 'cultivated',
 'Sesame.jpg',
 'ayurveda'),

-- 89. Flaxseed
('Linum usitatissimum',
 'Flaxseed',
 'अलसी',
 'जवस',
 'Atasi',
 'Linaceae',
 'Annual herb; seeds and oil used for bowel regulation, nutrition and lipid support.',
 'Cultivated in temperate and sub-temperate regions.',
 '["seed","oil"]',
 '["madhura","tikta"]',
 'ushna',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying"]',
 NULL,
 '["omega_3_fatty_acids","lignans"]',
 '["mild_laxative","hypolipidemic_support","nutritive"]',
 NULL,
 0,
 'cultivated',
 'Flaxseed.jpg',
 'ayurveda');

-- =========================================================
-- PLANT–DISEASE MAPPING FOR PLANTS 71–90
-- (Only plant_id & disease_id, everything else NULL)
-- =========================================================

-- Helper pattern (used below repeatedly):
-- INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
-- SELECT p.id, d.id
-- FROM plants p JOIN diseases d ON d.name_en = '<Disease Name>'
-- WHERE p.common_name_en = '<Common Name>'
--   AND NOT EXISTS (
--     SELECT 1 FROM plant_disease_mapping m
--     WHERE m.plant_id = p.id AND m.disease_id = d.id
--   );

------------------------------------------------------------
-- 71. Indian Gooseberry (Amalaki)
------------------------------------------------------------

-- Amalaki – Chronic Liver Disorder
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Liver Disorder'
WHERE p.common_name_en = 'Indian Gooseberry'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Amalaki – Chronic Skin Disease
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Indian Gooseberry'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Amalaki – Diabetes Mellitus Type 2
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Indian Gooseberry'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Amalaki – Jaundice
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Jaundice'
WHERE p.common_name_en = 'Indian Gooseberry'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 72. Haritaki
------------------------------------------------------------

-- Haritaki – Diarrhea and IBS (bowel regulation/IBS patterns)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Haritaki'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 73. Bibhitaki
------------------------------------------------------------

-- Bibhitaki – Chronic Cough and Bronchitis
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Bibhitaki'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Bibhitaki – Chronic Skin Disease (through Triphala-type use)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Bibhitaki'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 74. Turmeric
------------------------------------------------------------

-- Turmeric – Chronic Skin Disease
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Turmeric'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Turmeric – Chronic Liver Disorder
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Liver Disorder'
WHERE p.common_name_en = 'Turmeric'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Turmeric – Jaundice (supportive in hepatic conditions)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Jaundice'
WHERE p.common_name_en = 'Turmeric'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 75. Ginger
------------------------------------------------------------

-- Ginger – Recurrent Fever (supportive in Jvara-type patterns)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Recurrent Fever'
WHERE p.common_name_en = 'Ginger'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Ginger – Chronic Cough and Bronchitis
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Ginger'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 76. Coriander
------------------------------------------------------------

-- Coriander – Gastric Ulcer and Hyperacidity (cooling digestive)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Coriander'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Coriander – Chronic Liver Disorder (mild supportive)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Liver Disorder'
WHERE p.common_name_en = 'Coriander'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 77. Cumin
------------------------------------------------------------

-- Cumin – Diarrhea and IBS (Agni + gas regulation)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Cumin'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 78. Fennel
------------------------------------------------------------

-- Fennel – Gastric Ulcer and Hyperacidity (cooling carminative)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Fennel'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Fennel – Diarrhea and IBS (mild gut support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Fennel'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 79. Ajwain
------------------------------------------------------------

-- Ajwain – Intestinal Worm Infestation (krimi-related)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Intestinal Worm Infestation'
WHERE p.common_name_en = 'Ajwain'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Ajwain – Diarrhea and IBS (gas, colic)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Ajwain'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 80. Fenugreek
------------------------------------------------------------

-- Fenugreek – Diabetes Mellitus Type 2
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Fenugreek'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Fenugreek – Obesity (Kapha/meda supportive)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Fenugreek'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Fenugreek – Chronic Liver Disorder (mild metabolic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Liver Disorder'
WHERE p.common_name_en = 'Fenugreek'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 81. Green Cardamom
------------------------------------------------------------

-- Green Cardamom – Gastric Ulcer and Hyperacidity
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Green Cardamom'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Green Cardamom – Chronic Cough and Bronchitis (mild aromatic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Green Cardamom'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 82. Clove
------------------------------------------------------------

-- Clove – Chronic Cough and Bronchitis
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Clove'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Clove – Intestinal Worm Infestation (traditional krimi support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Intestinal Worm Infestation'
WHERE p.common_name_en = 'Clove'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 83. Cinnamon
------------------------------------------------------------

-- Cinnamon – Diabetes Mellitus Type 2 (metabolic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Cinnamon'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Cinnamon – Obesity (Kapha/meda support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Cinnamon'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 84. Curry Leaf
------------------------------------------------------------

-- Curry Leaf – Diabetes Mellitus Type 2
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Curry Leaf'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Curry Leaf – Obesity
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Curry Leaf'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 85. Sacred Lotus
------------------------------------------------------------

-- Sacred Lotus – Anxiety and Stress
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Anxiety and Stress'
WHERE p.common_name_en = 'Sacred Lotus'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Sacred Lotus – Ischemic Heart Disease (calming, Hridya support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Ischemic Heart Disease'
WHERE p.common_name_en = 'Sacred Lotus'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 86. Rose
------------------------------------------------------------

-- Rose – Anxiety and Stress (Shantikara)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Anxiety and Stress'
WHERE p.common_name_en = 'Rose'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Rose – Gastric Ulcer and Hyperacidity (mild cooling & soothing)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Rose'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Rose – Ischemic Heart Disease (Hridya support, traditional)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Ischemic Heart Disease'
WHERE p.common_name_en = 'Rose'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 87. Aloe Vera
------------------------------------------------------------

-- Aloe Vera – Chronic Skin Disease
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Aloe Vera'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Aloe Vera – Gastric Ulcer and Hyperacidity (internal gel use, traditional)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Aloe Vera'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Aloe Vera – Jaundice (hepato-biliary support, traditional)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Jaundice'
WHERE p.common_name_en = 'Aloe Vera'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 88. Sesame
------------------------------------------------------------

-- Sesame – Osteoporosis and Bone Weakness (calcium & Vata support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Osteoporosis and Bone Weakness'
WHERE p.common_name_en = 'Sesame'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Sesame – Neuromuscular Weakness (Vata-pacifying, balya)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Sesame'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 89. Flaxseed
------------------------------------------------------------

-- Flaxseed – Ischemic Heart Disease (lipid support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Ischemic Heart Disease'
WHERE p.common_name_en = 'Flaxseed'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Flaxseed – Obesity (weight & lipid support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Flaxseed'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Flaxseed – Diabetes Mellitus Type 2 (metabolic & fiber support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Flaxseed'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 90. Indian Blackberry (Jamun)
------------------------------------------------------------

-- Indian Blackberry – Diabetes Mellitus Type 2 (classic Jamun seed use)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Jamun'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Indian Blackberry – Diarrhea and IBS (fruit astringent action)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Jamun'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


-- =========================================================
-- PREPARATIONS (new schema; plant_id is NOT NULL)
-- Primary herb from plants 71–90
-- =========================================================

------------------------------------------------------------
-- 1. Triphala Churna  (primary plant: Indian Gooseberry / Amalaki)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Triphala Churna',
  'त्रिफला चूर्ण',
  'त्रिफळा चूर्ण',
  'Triphala Churna',
  'powder',
  'digestive_support',
  '1) Take equal parts by weight of dried fruits of Haritaki, Bibhitaki and Amalaki. 2) Clean and remove foreign material. 3) Powder each fruit separately to fine powder. 4) Sieve if required and mix all three powders thoroughly in equal proportions. 5) Store the mixed powder in airtight container.',
  'grinder_or_pulverizer; sieve; airtight_container; weighing_scale',
  'About 45–60 minutes depending on batch size.',
  'Close to total weight of dried fruits after cleaning.',
  'Store in a cool, dry, airtight container away from moisture.',
  'Commonly used within 3–6 months under proper storage conditions.',
  '{"adult":"3–5 g once or twice daily with suitable anupana","child":"1–2 g once daily under supervision"}',
  'usually_at_bedtime_or_as_directed',
  'lukewarm_water_or_ghee_or_honey_as_suitable',
  'Classical Triphala powder used traditionally to support digestion, bowel regularity, eye health and Rasayana actions. Not a substitute for medical care.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Indian Gooseberry'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Triphala Churna'
  );

------------------------------------------------------------
-- 2. Turmeric Milk  (Haldi Doodh)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Turmeric Milk',
  'हल्दी वाला दूध',
  'हळदीचे दूध',
  'Haridra Ksheerapaka (simple form)',
  'medicated_milk',
  'respiratory_and_skin_support',
  '1) Take about 150–200 ml milk (or suitable milk alternative). 2) Add 1/4–1/2 teaspoon turmeric powder and mix. 3) Heat gently to near boiling, stirring well. 4) Optionally add a pinch of black pepper and small amount of ghee as advised. 5) Consume warm.',
  'small_pan; heating_source; spoon/measuring_spoon',
  '10–15 minutes.',
  'One serving (150–200 ml).',
  'Use fresh; do not store for later use.',
  'Single serving; discard leftovers.',
  '{"adult":"150–200 ml once daily, usually at night, as suitable","child":"Use lower quantity and only under guidance."}',
  'usually_at_bedtime',
  'plain_or_with_small_amount_of_ghee_or_jaggery_as_suitable',
  'Traditional household preparation used in Ayurveda and folk practice for skin support, minor respiratory complaints and general Rasayana benefit. Not a replacement for medical treatment.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Turmeric'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Turmeric Milk'
  );

------------------------------------------------------------
-- 3. Ajwain Digestive Water
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Ajwain Digestive Water',
  'अजवाइन का पानी',
  'ओव्याचे पाणी',
  'Yavani Jala (simple household form)',
  'herbal_water',
  'digestive_support',
  '1) Lightly roast ajwain seeds in a pan until aromatic. 2) Add about 1 teaspoon roasted seeds to 200–250 ml water. 3) Boil gently for several minutes, then allow to steep. 4) Filter when lukewarm. 5) Sip as directed.',
  'small_pan; heating_source; strainer; measuring_spoon',
  '15–20 minutes.',
  'Approx. 200–250 ml herbal water.',
  'Can be kept covered and used within the same day.',
  'Same-day use recommended.',
  '{"adult":"30–60 ml after meals, up to 2–3 times a day as needed","child":"Use only with professional guidance and adjusted dose."}',
  'after_meals',
  'plain_lukewarm',
  'Traditional carminative water used in Indian households for gas, bloating and mild colicky discomfort. Dose and duration individualized.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Ajwain'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Ajwain Digestive Water'
  );

------------------------------------------------------------
-- 4. Jamun Seed Churna
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Jamun Seed Churna',
  'जामुन बीज चूर्ण',
  'जांभुळ बी चूर्ण',
  'Jambu Bija Churna',
  'powder',
  'metabolic_support',
  '1) Collect mature Jamun seeds and wash thoroughly. 2) Dry completely in shade and then in gentle sun if needed. 3) Remove any outer pulp remnants. 4) Powder the dried seeds to fine churna. 5) Store in airtight, moisture-free container.',
  'cleaning_tray; drying_arrangement; grinder; airtight_container',
  'Several hours to days for drying; powdering time depends on batch size.',
  'Yield depends on number of seeds; approx. equal to dry weight.',
  'Store in cool, dry, airtight container away from moisture and direct heat.',
  'Typically used within 3–6 months under proper storage conditions.',
  '{"adult":"1–3 g once or twice daily under professional supervision","child":"Only under qualified supervision with individualized dose."}',
  'usually_before_meals_or_as_directed',
  'plain_water_or_as_directed_by_practitioner',
  'Jamun seed powder is used traditionally in Ayurveda as a supportive measure in Madhumeha/Type 2 Diabetes and related metabolic patterns, along with diet, lifestyle and medical treatment.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Jamun'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Jamun Seed Churna'
  );

INSERT OR IGNORE INTO plants (
  botanical_name,
  common_name_en,
  common_name_hi,
  common_name_mr,
  sanskrit_name,
  family,
  description,
  habitat,
  parts_used,
  rasa,
  virya,
  vipaka,
  guna,
  dosha_effect,
  prabhava,
  active_compounds,
  therapeutic_actions,
  classical_references,
  is_endangered,
  cultivation_status,
  image_hero,
  ayush_system
) VALUES
-- 91. Ashwagandha
('Withania somnifera',
 'Ashwagandha',
 'अश्वगंधा',
 'अश्वगंधा',
 'Ashvagandha',
 'Solanaceae',
 'Small shrub; roots used as Rasayana to support strength, sleep, stress adaptation and neuromuscular health.',
 'Dry and subtropical regions; cultivated fields and wastelands.',
 '["root"]',
 '["tikta","kashaya","madhura"]',
 'ushna',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying","kapha_pacifying"]',
 NULL,
 '["withanolides","alkaloids"]',
 '["adaptogenic","anxiolytic_support","strengthening","rejuvenative"]',
 NULL,
 0,
 'cultivated',
 'Ashwagandha.jpg',
 'ayurveda'),

-- 92. Shankhpushpi (Convolvulus type)
('Convolvulus pluricaulis',
 'Shankhpushpi',
 'शंखपुष्पी',
 'शंखपुष्पी',
 'Shankhapushpi',
 'Convolvulaceae',
 'Prostrate herb; whole plant used as Medhya Rasayana for memory, concentration and calmness.',
 'Dry open fields and wastelands in many parts of India.',
 '["whole_plant"]',
 '["tikta","kashaya"]',
 'sheeta',
 'madhura',
 '["laghu","snigdha"]',
 '["pitta_pacifying","vata_pacifying"]',
 NULL,
 '["flavonoids","alkaloids"]',
 '["nootropic_support","anxiolytic_support","adaptogenic_mild"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Shankhpushpi.jpg',
 'ayurveda'),

-- 93. Indian Coleus
('Coleus forskohlii',
 'Indian Coleus',
 'मकंडी',
 'मकंडी',
 'Makandi',
 'Lamiaceae',
 'Perennial herb; roots used traditionally for heart, respiration and metabolic support.',
 'Rocky slopes of mountains and dry hilly regions.',
 '["root"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["forskolin"]',
 '["cardio_support","bronchodilator_support","metabolic_support"]',
 NULL,
 1,
 'wild_and_cultivated',
 'Indian_Coleus.jpg',
 'ayurveda'),

-- 94. Indian Frankincense
('Boswellia serrata',
 'Indian Frankincense',
 'सालाई गुग्गुलु',
 'सलाई गुग्गुळ',
 'Shallaki',
 'Burseraceae',
 'Medium tree; gum resin used for joint, inflammatory and respiratory support.',
 'Dry hilly forests of Central and Northern India.',
 '["oleo-gum-resin"]',
 '["katu","tikta","kashaya"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["boswellic_acids","essential_oils"]',
 '["anti-inflammatory_support","analgesic_support","joint_support"]',
 NULL,
 1,
 'wild',
 'Indian_Frankincense.jpg',
 'ayurveda'),

-- 95. Drumstick Tree
('Moringa oleifera',
 'Drumstick Tree',
 'सहजन',
 'शेवगा',
 'Shigru',
 'Moringaceae',
 'Fast-growing tree; leaves, pods and seeds used as nutritious food and in Ayurveda for joints, digestion and metabolism.',
 'Cultivated and naturalized in many parts of India, especially semi-arid areas.',
 '["leaf","pod","seed"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","tikshna"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["vitamins","minerals","isothiocyanates"]',
 '["nutritive","anti-inflammatory_support","metabolic_support","digestive"]',
 NULL,
 0,
 'cultivated',
 'Drumstick_Tree.jpg',
 'ayurveda'),

-- 96. Pomegranate
('Punica granatum',
 'Pomegranate',
 'अनार',
 'डाळिंब',
 'Dadima',
 'Lythraceae',
 'Shrub or small tree; fruit rind and juice used for digestion, anemia and cardiac support.',
 'Cultivated orchards and homestead gardens in many climatic zones.',
 '["fruit_rind","fruit_juice"]',
 '["kashaya","madhura","amla"]',
 'ushna',
 'madhura',
 '["laghu","snigdha"]',
 '["vata_pacifying","pitta_pacifying"]',
 NULL,
 '["polyphenols","tannins","anthocyanins"]',
 '["digestive","astringent","cardio_support","anemia_support"]',
 NULL,
 0,
 'cultivated',
 'Pomegranate.jpg',
 'ayurveda'),

-- 97. Lemon
('Citrus limon',
 'Lemon',
 'नींबू',
 'लिंबू',
 'Nimbuka',
 'Rutaceae',
 'Small tree; fruits used as sour condiment and for digestion, vitamin C and mild detox support.',
 'Cultivated widely in tropical and subtropical regions, home gardens and orchards.',
 '["fruit"]',
 '["amla","kashaya_mild"]',
 'ushna',
 'madhura',
 '["laghu"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["vitamin_C","citrus_flavonoids"]',
 '["digestive","carminative","anti-scorbutic","mild_detox_support"]',
 NULL,
 0,
 'cultivated',
 'Lemon.jpg',
 'ayurveda'),

-- 98. Holy Fig
('Ficus religiosa',
 'Holy Fig',
 'पीपल',
 'पिंपळ',
 'Ashvattha',
 'Moraceae',
 'Large sacred tree; bark, leaves and tender roots used traditionally for respiratory, cardiac and wound support.',
 'Roadsides, river banks, temple premises and village commons across India.',
 '["bark","leaf","tender_root"]',
 '["kashaya","tikta"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '["pitta_pacifying","rakta_pacifying"]',
 NULL,
 '["tannins","flavonoids"]',
 '["respiratory_support","wound_healing_support","cardio_support_mild"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Holy_Fig.jpg',
 'ayurveda'),

-- 99. Banyan Tree
('Ficus benghalensis',
 'Banyan Tree',
 'वट वृक्ष',
 'वड',
 'Vatavriksha',
 'Moraceae',
 'Large evergreen tree with aerial roots; bark, latex and tender aerial roots used traditionally in Ayurveda for wound, dental and metabolic support.',
 'Commonly found in villages, roadsides and temple compounds throughout India.',
 '["bark","latex","aerial_root"]',
 '["kashaya"]',
 'sheeta',
 'katu',
 '["guru","ruksha"]',
 '["pitta_pacifying","rakta_pacifying"]',
 NULL,
 '["tannins","flavonoids"]',
 '["astringent","wound_support","dental_support_traditional","metabolic_support_mild"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Banyan_Tree.jpg',
 'ayurveda'),

-- 100. Coconut
('Cocos nucifera',
 'Coconut',
 'नारियल',
 'नारळ',
 'Narikela',
 'Arecaceae',
 'Tall palm; water, kernel and oil used as cooling, nutritive and in many Ayurvedic formulations.',
 'Coastal regions and humid tropics; widely cultivated.',
 '["tender_coconut_water","kernel","oil"]',
 '["madhura"]',
 'sheeta',
 'madhura',
 '["guru","snigdha"]',
 '["pitta_pacifying","vata_pacifying"]',
 NULL,
 '["medium_chain_triglycerides","electrolytes"]',
 '["cooling","nutritive","balya_tonic","skin_and_hair_support"]',
 NULL,
 0,
 'cultivated',
 'Coconut.jpg',
 'ayurveda'),

-- 101. Nutmeg
('Myristica fragrans',
 'Nutmeg',
 'जायफल',
 'जायफळ',
 'Jatiphala',
 'Myristicaceae',
 'Evergreen tree; seed (nutmeg) and aril (mace) used as aromatic digestive and for sleep support in small doses.',
 'Cultivated in humid tropical regions.',
 '["seed","aril"]',
 '["katu","tikta","kashaya"]',
 'ushna',
 'katu',
 '["laghu","tikshna"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["myristicin","essential_oils"]',
 '["carminative","digestive","mild_sedative_support"]',
 NULL,
 0,
 'cultivated',
 'Nutmeg.jpg',
 'ayurveda'),

-- 102. Saffron
('Crocus sativus',
 'Saffron',
 'केसर',
 'केशर',
 'Kumkuma / Keshara',
 'Iridaceae',
 'Low-growing plant; dried stigmas used in very small amounts as aromatic coloring agent and Rasayana for mind, heart and reproductive system.',
 'Cultivated in cool, dry temperate regions such as Kashmir and parts of Iran.',
 '["stigma"]',
 '["tikta","katu","kashaya"]',
 'ushna',
 'katu',
 '["laghu"]',
 '["vata_pacifying","kapha_pacifying"]',
 NULL,
 '["crocin","safranal","picrocrocin"]',
 '["rasayana_support","mood_support","cardio_support_mild"]',
 NULL,
 0,
 'cultivated',
 'Saffron.jpg',
 'ayurveda'),

-- 103. Black Cardamom
('Amomum subulatum',
 'Black Cardamom',
 'बड़ी इलायची',
 'मोठी वेलची',
 'Brihad Ela',
 'Zingiberaceae',
 'Perennial herb; large smoky capsules used as warming aromatic for digestion and respiratory support.',
 'Cultivated in cool, moist hilly regions.',
 '["fruit"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["essential_oils","cineole"]',
 '["carminative","digestive","mild_expectorant"]',
 NULL,
 0,
 'cultivated',
 'Black_Cardamom.jpg',
 'ayurveda'),

-- 104. Star Anise
('Illicium verum',
 'Star Anise',
 'चक्र फूल',
 'चक्रफूल',
 'Chakra Phala (commonly used name)',
 'Schisandraceae',
 'Evergreen tree; star-shaped dried fruits used as aromatic spice and carminative.',
 'Cultivated in some subtropical regions; also imported.',
 '["fruit"]',
 '["madhura","katu"]',
 'ushna',
 'katu',
 '["laghu"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["anethole","essential_oils"]',
 '["carminative","digestive","flavoring_agent"]',
 NULL,
 0,
 'cultivated',
 'Star_Anise.jpg',
 'ayurveda'),

-- 105. Grapes
('Vitis vinifera',
 'Grapes',
 'अंगूर',
 'द्राक्ष',
 'Draksha',
 'Vitaceae',
 'Climbing vine; fresh fruits and raisins used as mild laxative, Rasayana and cardio-supportive in Ayurveda.',
 'Cultivated vineyards and home gardens.',
 '["fruit","raisin"]',
 '["madhura"]',
 'sheeta',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying","pitta_pacifying"]',
 NULL,
 '["resveratrol","flavonoids","sugars"]',
 '["mild_laxative","cardio_support","rejuvenative","cooling"]',
 NULL,
 0,
 'cultivated',
 'Grapes.jpg',
 'ayurveda'),

-- 106. Dates
('Phoenix dactylifera',
 'Dates',
 'खजूर',
 'खजूर',
 'Khajura',
 'Arecaceae',
 'Tall palm; sweet fruits used as energy tonic, mild laxative and Rasayana in many traditional systems.',
 'Cultivated in arid and semi-arid regions; fruits widely traded.',
 '["fruit"]',
 '["madhura"]',
 'ushna',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying"]',
 NULL,
 '["natural_sugars","minerals","fiber"]',
 '["energy_tonic","mild_laxative","nutritive"]',
 NULL,
 0,
 'cultivated',
 'Dates.jpg',
 'ayurveda'),

-- 107. Black Cumin
('Nigella sativa',
 'Black Cumin',
 'कलौंजी',
 'काळे जिरे',
 'Krishna Jiraka (in some texts)',
 'Ranunculaceae',
 'Erect herb; small black seeds used as spice in Unani and also as supportive in some Ayurvedic contexts for digestion and metabolism.',
 'Cultivated in fields and kitchen gardens in various regions.',
 '["seed"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["thymoquinone","essential_oils"]',
 '["digestive","carminative","metabolic_support"]',
 NULL,
 0,
 'cultivated',
 'Black_Cumin.jpg',
 'ayurveda'),

-- 108. Garden Cress
('Lepidium sativum',
 'Garden Cress',
 'हलिम',
 'अळशीकाडे / हालिम (regionally)',
 'Chandrashura / Halim',
 'Brassicaceae',
 'Small annual herb; seeds used as nutritive, especially for iron, and support in bone and reproductive health.',
 'Cultivated in small plots and kitchen gardens; also as salad/green.',
 '["seed","leaf"]',
 '["madhura","tikta"]',
 'ushna',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying"]',
 NULL,
 '["iron","protein","glucosinolates"]',
 '["hematinic_support","bone_support","nutritive"]',
 NULL,
 0,
 'cultivated',
 'Garden_Cress.jpg',
 'ayurveda'),

-- 109. Cutch Tree
('Acacia catechu',
 'Cutch Tree',
 'खैर',
 'खैर',
 'Khadira',
 'Fabaceae',
 'Medium tree; heartwood and its extract (kattha) used as astringent in oral, skin and wound applications.',
 'Dry deciduous forests and cultivated plantations.',
 '["heartwood","bark"]',
 '["kashaya","tikta"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '["pitta_pacifying","kapha_pacifying"]',
 NULL,
 '["catechin","tannins"]',
 '["astringent","oral_health_support","skin_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Cutch_Tree.jpg',
 'ayurveda'),

-- 110. Vetiver
('Chrysopogon zizanioides',
 'Vetiver',
 'खस',
 'खस',
 'Ushir / Ushira',
 'Poaceae',
 'Perennial grass; aromatic roots used as cooling, diaphoretic and in perfumery and Ayurveda for Pitta and Rakta pacification.',
 'Grown in fields, river banks and as soil-binding grass in many parts of India.',
 '["root"]',
 '["tikta","madhura"]',
 'sheeta',
 'madhura',
 '["laghu","ruksha"]',
 '["pitta_pacifying","rakta_pacifying"]',
 NULL,
 '["vetiver_oil","sesquiterpenes"]',
 '["cooling","diaphoretic","calming","skin_support"]',
 NULL,
 0,
 'cultivated',
 'Vetiver.jpg',
 'ayurveda');

INSERT OR IGNORE INTO plants (
  botanical_name,
  common_name_en,
  common_name_hi,
  common_name_mr,
  sanskrit_name,
  family,
  description,
  habitat,
  parts_used,
  rasa,
  virya,
  vipaka,
  guna,
  dosha_effect,
  prabhava,
  active_compounds,
  therapeutic_actions,
  classical_references,
  is_endangered,
  cultivation_status,
  image_hero,
  ayush_system
) VALUES
-- 111. Safed Musli
('Chlorophytum borivilianum',
 'Safed Musli',
 'सफेद मूसली',
 'सफेद मूसळी',
 'Swetha Musali',
 'Asparagaceae',
 'Tubers traditionally used as Rasayana for strength, vitality and reproductive health.',
 'Forests and cultivated farms; tropical regions.',
 '["tuber"]',
 '["madhura"]',
 'sheeta',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying"]',
 NULL,
 '["saponins"]',
 '["balya","rasayana","reproductive_support"]',
 NULL,
 1,
 'cultivated',
 'Safed_Musli.jpg',
 'ayurveda'),

-- 112. Shilajit (Mineral-herbal exudate)
('Asphaltum punjabinum',
 'Shilajit',
 'शिलाजीत',
 'शिलाजीत',
 'Shilajatu',
 'Natural_organic_mineral',
 'Mineral-rich exudate used as Rasayana for stamina, metabolism and rejuvenation.',
 'Himalayan mountain crevices.',
 '["exudate"]',
 '["katu","tikta"]',
 'ushna',
 'madhura',
 '["laghu","tikshna"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["fulvic_acid","humic_substances"]',
 '["stamina_support","metabolic_support","rasayana"]',
 NULL,
 1,
 'wild',
 'Shilajit.jpg',
 'ayurveda'),

-- 113. Kapikacchu (Mucuna)
('Mucuna pruriens',
 'Kapikacchu',
 'कौंच',
 'कोंच',
 'Kapikacchu',
 'Fabaceae',
 'Leguminous plant; seeds used as Rasayana and for neuromuscular & reproductive support.',
 'Hilly tropical regions, forest edges.',
 '["seed"]',
 '["madhura","tikta"]',
 'ushna',
 'madhura',
 '["guru"]',
 '["vata_pacifying"]',
 NULL,
 '["L-DOPA","alkaloids"]',
 '["neuromuscular_support","reproductive_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Kapikacchu.jpg',
 'ayurveda'),

-- 114. Bala (Country Mallow)
('Sida cordifolia',
 'Country Mallow',
 'बला',
 'बला',
 'Bala',
 'Malvaceae',
 'Roots used as strengthening, anti-inflammatory and Vata pacifying.',
 'Dry wastelands; plains of India.',
 '["root","leaf"]',
 '["madhura"]',
 'sheeta',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying"]',
 NULL,
 '["alkaloids","flavonoids"]',
 '["balya","anti-inflammatory_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Country_Mallow.jpg',
 'ayurveda'),

-- 115. Ashoka Tree
('Saraca asoca',
 'Ashoka Tree',
 'अशोक',
 'अशोक',
 'Ashoka',
 'Fabaceae',
 'Bark used traditionally for women’s reproductive support and bleeding disorders.',
 'Moist deciduous and evergreen forests.',
 '["bark"]',
 '["kashaya","tikta"]',
 'sheeta',
 'katu',
 '["laghu"]',
 '["pitta_pacifying"]',
 NULL,
 '["tannins","flavonoids"]',
 '["reproductive_support","astringent"]',
 NULL,
 1,
 'wild_and_cultivated',
 'Ashoka_Tree.jpg',
 'ayurveda'),

-- 117. Indian Mallow (Atibala)
('Abutilon indicum',
 'Indian Mallow',
 'अतिबला',
 'अतिबला',
 'Atibala',
 'Malvaceae',
 'Roots/leaves used for Vata disorders, nerve weakness and inflammation.',
 'Roadside, wasteland habitats in tropical climate.',
 '["root","leaf"]',
 '["madhura"]',
 'sheeta',
 'madhura',
 '["snigdha","guru"]',
 '["vata_pacifying"]',
 NULL,
 '["mucilage","flavonoids"]',
 '["balya","anti-inflammatory_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Indian_Mallow.jpg',
 'ayurveda'),

-- 118. Cardiospermum (Balloon Vine)
('Cardiospermum halicacabum',
 'Balloon Vine',
 'कांजीर',
 'कांजीर',
 'Jyotishmati (regional confusion avoided)',
 'Sapindaceae',
 'Climbing plant used traditionally for joint, skin and Vata disorders.',
 'Tropical regions; scrublands.',
 '["leaf","root"]',
 '["tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["vata_pacifying"]',
 NULL,
 '["flavonoids","alkaloids"]',
 '["joint_support","anti-inflammatory_support"]',
 NULL,
 0,
 'wild',
 'Balloon_Vine.jpg',
 'ayurveda'),

-- 120. Chirbilva (Holarrhena pubescens)
('Holarrhena pubescens',
 'Holarrhena',
 'कुटज (छोटी जात)',
 'कुडज',
 'Kutaja',
 'Apocynaceae',
 'Bark/seeds used for diarrhea and IBS-related disturbances.',
 'Dry deciduous forests.',
 '["bark","seed"]',
 '["kashaya","tikta"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '["pitta_pacifying","kapha_pacifying"]',
 NULL,
 '["conessine","alkaloids"]',
 '["antidiarrheal","gut_support"]',
 NULL,
 0,
 'wild',
 'Holarrhena.jpg',
 'ayurveda'),

-- 121. Mahua
('Madhuca longifolia',
 'Mahua',
 'माहुआ',
 'महुआ',
 'Madhuka',
 'Sapotaceae',
 'Flowers, seeds used in traditional practices; nutritive and mild laxative.',
 'Dry tropical forests.',
 '["flower","seed"]',
 '["madhura"]',
 'sheeta',
 'madhura',
 '["snigdha","guru"]',
 '["pitta_pacifying"]',
 NULL,
 '["sugars","fatty_oils"]',
 '["nutritive","mild_laxative"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Mahua.jpg',
 'ayurveda'),

-- 122. Arjun Bark Flower Variant (Arjuna Pushpa)
('Terminalia arjuna (flower)',
 'Arjuna Flower',
 'अर्जुन पुष्प',
 'अर्जुन फूल',
 'Arjuna Pushpa',
 'Combretaceae',
 'Flowers used mildly in cardiac and cooling formulations.',
 'Deciduous forests.',
 '["flower"]',
 '["kashaya","madhura"]',
 'sheeta',
 'madhura',
 '["laghu"]',
 '["pitta_pacifying"]',
 NULL,
 '["flavonoids","tannins"]',
 '["cardiac_support_mild"]',
 NULL,
 0,
 'wild',
 'Arjuna_Flower.jpg',
 'ayurveda'),

-- 123. Shorea Robusta (Sal Tree)
('Shorea robusta',
 'Sal Tree',
 'साल वृक्ष',
 'साल',
 'Shala',
 'Dipterocarpaceae',
 'Resin and bark used in wound healing, skin and joint support.',
 'Tropical forests across Central & Eastern India.',
 '["resin","bark"]',
 '["kashaya"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '["pitta_pacifying","rakta_pacifying"]',
 NULL,
 '["resins","tannins"]',
 '["wound_healing_support","skin_support"]',
 NULL,
 1,
 'wild',
 'Sal_Tree.jpg',
 'ayurveda'),

-- 124. Takrarista Herb Base (Buttermilk Ayurveda Herb)
('Buttermilk_base_herb',
 'Takra Herb Base',
 'तक्र औषध मूल',
 'तक्र औषध मूळ',
 'Takra Dravya',
 'Dairy_derivative_with_herbs',
 'Used as vehicle (Anupana) for digestion-related medicines.',
 'Prepared traditionally in households.',
 '["liquid_vehicle"]',
 '["amla","kashaya_mild"]',
 'ushna',
 'katu',
 '["laghu"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["lactic_acid"]',
 '["digestive_support"]',
 NULL,
 0,
 'prepared',
 'Takra_Herb_Base.jpg',
 'ayurveda'),

-- 125. Marsh Barley (Yava)
('Hordeum vulgare',
 'Barley',
 'जौ',
 'बार्ली',
 'Yava',
 'Poaceae',
 'Seeds used in digestive, urinary and metabolic disorders.',
 'Cultivated temperate regions.',
 '["seed"]',
 '["kashaya","tikta","madhura"]',
 'sheeta',
 'madhura',
 '["laghu","ruksha"]',
 '["kapha_pacifying","pitta_pacifying"]',
 NULL,
 '["beta_glucans","fiber"]',
 '["digestive","diuretic","metabolic_support"]',
 NULL,
 0,
 'cultivated',
 'Barley.jpg',
 'ayurveda'),

-- 127. Kesar Mango Leaf (Ayurvedic edible leaf variant)
('Mangifera indica leaf',
 'Mango Leaf',
 'आम पत्ता',
 'आंबा पान',
 'Amra Patra',
 'Anacardiaceae',
 'Leaves used traditionally in mild glycemic and respiratory support.',
 'Cultivated orchards.',
 '["leaf"]',
 '["tikta"]',
 'sheeta',
 'katu',
 '["laghu"]',
 '["pitta_pacifying"]',
 NULL,
 '["polyphenols"]',
 '["respiratory_support","glycemic_support_mild"]',
 NULL,
 0,
 'cultivated',
 'Mango_Leaf.jpg',
 'ayurveda'),

-- 128. Bhrami Gajak (Sweet resin-like root)
('Glycyrrhiza glabra (soft_variant)',
 'Licorice Soft Root',
 'यष्टिमधु नरम रूप',
 'जेष्ठमध नरम',
 'Madhuka Mrudu',
 'Fabaceae',
 'Used as milder variant of licorice for throat and gastric comfort.',
 'Cultivated dry climates.',
 '["root"]',
 '["madhura"]',
 'sheeta',
 'madhura',
 '["snigdha"]',
 '["pitta_pacifying","vata_pacifying"]',
 NULL,
 '["glycyrrhizin"]',
 '["throat_support","ulcer_support"]',
 NULL,
 0,
 'cultivated',
 'Licorice_Soft_Root.jpg',
 'ayurveda'),

-- 129. Palash Tree
('Butea monosperma',
 'Palash',
 'पलाश',
 'पळस',
 'Palasha',
 'Fabaceae',
 'Flowers and bark used for urinary, skin and reproductive support.',
 'Dry deciduous forests.',
 '["flower","bark"]',
 '["kashaya","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","pitta_pacifying"]',
 NULL,
 '["flavonoids","palasonin"]',
 '["urinary_support","skin_support","krimi_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Palash.jpg',
 'ayurveda'),

-- 130. Cinnamon Leaf (Tejpatra variant)
('Tamal Patra',
 'Indian Bay Leaf (Tejpatra)',
 'तेज पत्ता',
 'तामालपत्र',
 'Tamala Patra',
 'Lauraceae',
 'Leaves used as aromatic spice in digestion, respiratory and metabolic support.',
 'Hilly forests of NE and South India.',
 '["leaf"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["cinnamaldehyde","eugenol"]',
 '["digestive","carminative","mild_expectorant"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Indian_Bay_Leaf_(Tejpatra).jpg',
 'ayurveda');

-- =========================================================
-- PLANT–DISEASE MAPPING FOR PLANTS 111–130
-- =========================================================

------------------------------------------------------------
-- 111. Safed Musli → Strength / bone / neuromuscular support
------------------------------------------------------------
-- Safed Musli – Neuromuscular Weakness
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Safed Musli'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Safed Musli – Osteoporosis and Bone Weakness
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Osteoporosis and Bone Weakness'
WHERE p.common_name_en = 'Safed Musli'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 112. Shilajit → metabolic/strength support
------------------------------------------------------------
-- Shilajit – Diabetes Mellitus Type 2 (supportive)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Shilajit'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Shilajit – Obesity (metabolic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Shilajit'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Shilajit – Neuromuscular Weakness (Rasayana/strength)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Shilajit'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 113. Kapikacchu → neuro / memory
------------------------------------------------------------
-- Kapikacchu – Neuromuscular Weakness
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Kapikacchu'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Kapikacchu – Memory Weakness (Medhya Rasayana role)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Memory Weakness'
WHERE p.common_name_en = 'Kapikacchu'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 114. Country Mallow (Bala type)
------------------------------------------------------------
-- Country Mallow – Neuromuscular Weakness
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Country Mallow'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Country Mallow – Osteoporosis and Bone Weakness (balya)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Osteoporosis and Bone Weakness'
WHERE p.common_name_en = 'Country Mallow'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 115. Ashoka Tree → menstrual support
------------------------------------------------------------
-- Ashoka – Menstrual Irregularity
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Menstrual Irregularity'
WHERE p.common_name_en = 'Ashoka Tree'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 96. Pomegranate
------------------------------------------------------------
-- Pomegranate Flower – Gastric Ulcer and Hyperacidity (astringent, cooling)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Pomegranate'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Pomegranate Flower – Ischemic Heart Disease (cardio-supportive, traditional)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Ischemic Heart Disease'
WHERE p.common_name_en = 'Pomegranate'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 117. Indian Mallow (Atibala)
------------------------------------------------------------
-- Indian Mallow – Neuromuscular Weakness
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Indian Mallow'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 118. Balloon Vine
------------------------------------------------------------
-- Balloon Vine – Osteoporosis and Bone Weakness (joint support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Osteoporosis and Bone Weakness'
WHERE p.common_name_en = 'Balloon Vine'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Balloon Vine – Neuromuscular Weakness (Vata/joint patterns)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Balloon Vine'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 119. Indian Madder (Manjishta)
------------------------------------------------------------
-- Indian Madder – Chronic Skin Disease
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Indian Madder'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Indian Madder – Chronic Liver Disorder (Rakta/pitta clearing)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Liver Disorder'
WHERE p.common_name_en = 'Indian Madder'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Indian Madder – Jaundice (supportive in Rakta/Pitta disorders)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Jaundice'
WHERE p.common_name_en = 'Indian Madder'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 120. Holarrhena (Kutaja)
------------------------------------------------------------
-- Holarrhena – Diarrhea and IBS (classical use)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Holarrhena'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 121. Mahua
------------------------------------------------------------
-- Mahua – Neuromuscular Weakness (nutritive, balya)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Mahua'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Mahua – Osteoporosis and Bone Weakness (nutritive support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Osteoporosis and Bone Weakness'
WHERE p.common_name_en = 'Mahua'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 122. Arjuna Flower
------------------------------------------------------------
-- Arjuna Flower – Ischemic Heart Disease (mild cardiac support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Ischemic Heart Disease'
WHERE p.common_name_en = 'Arjuna Flower'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 123. Sal Tree
------------------------------------------------------------
-- Sal Tree – Chronic Skin Disease (resin/bark)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Sal Tree'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 124. Takra Herb Base (buttermilk vehicle)
------------------------------------------------------------
-- Takra Herb Base – Diarrhea and IBS (digestive support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Takra Herb Base'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Takra Herb Base – Gastric Ulcer and Hyperacidity (properly used buttermilk)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Takra Herb Base'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 125. Barley (Yava)
------------------------------------------------------------
-- Barley – Diabetes Mellitus Type 2
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Barley'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Barley – Obesity (Yavanna upayoga, Meda support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Barley'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Barley – Urinary Stones (Mutravaha, diuretic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Urinary Stones'
WHERE p.common_name_en = 'Barley'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 126. Indian Sarsaparilla (Nannari)
------------------------------------------------------------
-- Nannari – Chronic Skin Disease
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Indian Sarsaparilla'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Nannari – Jaundice (cooling, Rakta/Pitta support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Jaundice'
WHERE p.common_name_en = 'Indian Sarsaparilla'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Nannari – Chronic Liver Disorder
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Liver Disorder'
WHERE p.common_name_en = 'Indian Sarsaparilla'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 127. Mango Leaf
------------------------------------------------------------
-- Mango Leaf – Diabetes Mellitus Type 2 (folk glycemic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Mango Leaf'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Mango Leaf – Bronchial Asthma (traditional smoke/fumes usage)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Bronchial Asthma'
WHERE p.common_name_en = 'Mango Leaf'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 128. Licorice Soft Root
------------------------------------------------------------
-- Licorice Soft Root – Gastric Ulcer and Hyperacidity
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Licorice Soft Root'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Licorice Soft Root – Chronic Cough and Bronchitis
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Licorice Soft Root'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 129. Palash
------------------------------------------------------------
-- Palash – Intestinal Worm Infestation (krimi)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Intestinal Worm Infestation'
WHERE p.common_name_en = 'Palash'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Palash – Chronic Skin Disease (Rakta/pitta related)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Palash'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 130. Indian Bay Leaf (Tejpatra)
------------------------------------------------------------
-- Indian Bay Leaf – Gastric Ulcer and Hyperacidity (digestive support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Gastric Ulcer and Hyperacidity'
WHERE p.common_name_en = 'Indian Bay Leaf (Tejpatra)'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Indian Bay Leaf – Chronic Cough and Bronchitis (mild expectorant)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Indian Bay Leaf (Tejpatra)'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- =========================================================
-- PREPARATIONS – PRIMARY HERB FROM PLANTS 111–130
-- =========================================================

------------------------------------------------------------
-- 1. Safed Musli Rasayana Granules
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Safed Musli Rasayana Granules',
  'सफेद मूसली रसायन ग्रेन्यूल्स',
  'सफेद मूसळी रसायन ग्रॅन्यूल्स',
  'Musali Rasayana (simplified)',
  'granules',
  'rasayana_and_strength_support',
  '1) Clean and dry Safed Musli tubers thoroughly. 2) Powder to a coarse/fine consistency as required. 3) Prepare a suitable sweet base (e.g., sugar or jaggery syrup) and mix with the powder to form granules. 4) Dry the granules gently in shade until free-flowing. 5) Store in airtight container.',
  'grinder; mixing_bowl; tray_for_drying; airtight_container',
  'Several hours to a day including drying time.',
  'Yield depends on amount of Safed Musli and sweet base used; typically close to combined dry weight.',
  'Store in a cool, dry place in airtight container away from moisture.',
  'Often used within 3–6 months under proper storage.',
  '{"adult":"5–10 g once or twice daily under professional supervision","child":"only under qualified guidance"}',
  'usually_morning_and_or_evening_after_food',
  'lukewarm_milk_or_lukewarm_water_as_suitable',
  'Safed Musli-based granules used traditionally as Rasayana and balya for strength, vitality and reproductive support, under supervision and with attention to metabolic status.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Safed Musli'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Safed Musli Rasayana Granules'
  );

------------------------------------------------------------
-- 2. Ashoka Bark Decoction (Ashoka Kwatha)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Ashoka Bark Decoction',
  'अशोक की छाल का काढ़ा',
  'अशोक सालीचा काढा',
  'Ashoka Kwatha (simplified)',
  'decoction',
  'gynecological_support',
  '1) Take coarse powder of Ashoka bark. 2) Add to water in classical proportion (e.g., 1 part coarse powder to 16 parts water, reduce to 1/4), or as guided. 3) Boil gently until reduced; stir intermittently. 4) Filter warm and use as prescribed.',
  'decoction_pot; heating_source; strainer; measuring_cup',
  '30–45 minutes depending on volume.',
  'Typically one dose of 60–120 ml from initial water volume.',
  'Best used fresh and warm; can be kept covered for few hours if needed.',
  'Same-day use recommended unless otherwise specified.',
  '{"adult":"30–60 ml once or twice daily under gynecological supervision","child":"use only if specifically prescribed"}',
  'as_directed_by_practitioner',
  'plain_or_with_suitable_vehicle_as_advised',
  'Traditional Ashoka bark decoction used in Ayurveda for support in menstrual and gynecological complaints, under qualified supervision.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Ashoka Tree'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Ashoka Bark Decoction'
  );

------------------------------------------------------------
-- 3. Barley Water (Yava Jala / Yavodaka)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Barley Water',
  'जौ का पानी',
  'बार्लीचे पाणी',
  'Yava Jala (Yavodaka)',
  'herbal_water',
  'digestive_and_metabolic_support',
  '1) Clean and lightly roast or wash barley grains. 2) Boil a measured quantity of barley in several times water until grains are soft and the water becomes slightly viscous. 3) Filter to obtain clear barley water. 4) Cool to lukewarm or room temperature and use as directed.',
  'cooking_pot; heating_source; strainer; measuring_cups',
  '30–45 minutes depending on quantity.',
  'Typically 500–1000 ml barley water from one small batch of grains.',
  'Can be kept covered and used during the same day; refrigerate if stored longer.',
  'Preferably consumed within 12–24 hours.',
  '{"adult":"50–150 ml 2–3 times daily as supportive drink","child":"smaller quantities as suitable under guidance"}',
  'throughout_day_or_as_directed',
  'plain; may be lightly seasoned as per advice',
  'Traditional barley water preparation used in Ayurveda for digestion, metabolic and urinary support, often in Kapha/Medo and Mutravaha conditions.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Barley'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Barley Water'
  );

------------------------------------------------------------
-- 4. Nannari Cooling Syrup (Indian Sarsaparilla Sharbat Base)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Nannari Cooling Syrup',
  'नन्नारी शीतल सिरप',
  'नन्नारी शीतल सिरप',
  'Anantamula Sharbat (regionally popular form)',
  'syrup',
  'cooling_and_liver_support',
  '1) Clean and wash Indian Sarsaparilla roots thoroughly. 2) Cut into small pieces and soak in water for several hours to extract flavor. 3) Boil the soaked roots with the same water to concentrate the decoction; filter. 4) Add sugar to the filtered decoction and cook to syrup (phanta/paaka) consistency. 5) Cool and store in clean bottles.',
  'knife; soaking_vessel; boiling_pot; strainer; stirring_spoon; bottles',
  'Several hours including soaking, boiling and syrup preparation.',
  'Multiple servings; yield depends on root and sugar quantity (e.g., 500–1000 ml syrup).',
  'Store in sterilized, airtight bottles in cool place or refrigerator.',
  'Often usable for few weeks when stored hygienically and refrigerated; follow local best practice.',
  '{"adult":"15–30 ml syrup diluted in water once or twice daily in hot season","child":"5–10 ml diluted in water under guidance"}',
  'mainly_in_hot_season_or_as_directed',
  'cool_water_as_diluent',
  'Traditionally used as a cooling sharbat base with Indian Sarsaparilla root, providing gentle Pitta and Rakta support and pleasant flavor; sugar content should be considered in metabolic disorders.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Indian Sarsaparilla (Nannari)'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Nannari Cooling Syrup'
  );

------------------------------------------------------------
-- 5. Palash Flower Decoction for Krimi Support
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Palash Flower Decoction',
  'पलाश पुष्प काढ़ा',
  'पळस फुलांचा काढा',
  'Palasha Pushpa Kwatha (simplified)',
  'decoction',
  'krimi_and_skin_support',
  '1) Take dried Palash flowers and clean to remove foreign matter. 2) Prepare coarse powder or use broken flowers. 3) Boil in suitable quantity of water until volume reduces as per kwatha standard. 4) Filter warm and use strictly as advised by practitioner.',
  'decoction_pot; heating_source; strainer; measuring_cup',
  '20–30 minutes.',
  'Single or multiple doses depending on starting volume.',
  'Should be prepared fresh; use same day.',
  'Same-day use recommended.',
  '{"adult":"dose and duration only as per professional prescription","child":"use only under strict professional supervision"}',
  'as_directed_by_practitioner',
  'plain_or_with_suitable_vehicle_as_prescribed',
  'Palash flower decoction is employed traditionally in krimi and certain Rakta/Pitta-related conditions; use is individualized and requires supervision.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Palash'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Palash Flower Decoction'
  );

INSERT OR IGNORE INTO plants (
  botanical_name,
  common_name_en,
  common_name_hi,
  common_name_mr,
  sanskrit_name,
  family,
  description,
  habitat,
  parts_used,
  rasa,
  virya,
  vipaka,
  guna,
  dosha_effect,
  prabhava,
  active_compounds,
  therapeutic_actions,
  classical_references,
  is_endangered,
  cultivation_status,
  image_hero,
  ayush_system
) VALUES
-- 131. Gudmar (Gymnema)
('Gymnema sylvestre',
 'Gudmar',
 'गुड़मार',
 'गुढमार',
 'Meshashringi',
 'Apocynaceae',
 'Climbing shrub; leaves traditionally used in Ayurveda to support healthy blood sugar and reduce excessive sweet cravings.',
 'Dry forests and scrublands of central and southern India; also cultivated.',
 '["leaf"]',
 '["tikta","kashaya"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","pitta_pacifying"]',
 NULL,
 '["gymnemic_acids","saponins"]',
 '["glycemic_support","digestive_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Gudmar.jpg',
 'ayurveda'),

-- 132. Tagara (Indian Valerian)
('Valeriana wallichii',
 'Tagara',
 'टगर',
 'टगर',
 'Tagara',
 'Caprifoliaceae',
 'Perennial herb; rhizomes used as mild sedative, sleep-supportive and calming agent in Ayurvedic practice.',
 'Himalayan regions, moist temperate forests.',
 '["rhizome","root"]',
 '["tikta","kashaya"]',
 'ushna',
 'katu',
 '["laghu","snigdha"]',
 '["vata_pacifying","kapha_pacifying"]',
 NULL,
 '["valepotriates","essential_oils"]',
 '["mild_sedative_support","anxiety_support","sleep_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Tagara.jpg',
 'ayurveda'),

-- 133. Asafoetida (Hing)
('Ferula asafoetida',
 'Asafoetida',
 'हींग',
 'हिंग',
 'Hingu',
 'Apiaceae',
 'Oleogum-resin from Ferula species; used in very small quantities as carminative and Vata-pacifying spice.',
 'Dry mountainous regions; resin usually imported and processed.',
 '["oleo-gum-resin"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","tikshna"]',
 '["vata_pacifying","kapha_pacifying"]',
 NULL,
 '["ferulic_acid","sulfur_compounds","resins"]',
 '["carminative","digestive","antispasmodic_support"]',
 NULL,
 0,
 'cultivated_and_collected',
 'Asafoetida.jpg',
 'ayurveda'),

-- 134. Indian Mustard
('Brassica juncea',
 'Indian Mustard',
 'सरसों',
 'मोहरी',
 'Sarshapa',
 'Brassicaceae',
 'Annual herb; seeds and oil used as pungent spice and external application for stiffness and cold.',
 'Cultivated widely as oilseed crop in North and Central India.',
 '["seed","oil","leaf"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","tikshna"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["allyl_isothiocyanate","omega_fats"]',
 '["carminative","rubefacient_external","digestive_support"]',
 NULL,
 0,
 'cultivated',
 'Indian_Mustard.jpg',
 'ayurveda'),

-- 135. Indian Senna
('Cassia angustifolia',
 'Indian Senna',
 'सनाई',
 'सनई',
 'Svarnapatri / Senna',
 'Fabaceae',
 'Small shrub; leaflets and pods used as classical herbal laxative in carefully monitored doses.',
 'Cultivated in arid regions of India.',
 '["leaf","pod"]',
 '["tikta"]',
 'ushna',
 'madhura',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["sennosides"]',
 '["laxative","bowel_motility_support"]',
 NULL,
 0,
 'cultivated',
 'Indian_Senna.jpg',
 'ayurveda'),

-- 136. Pointed Gourd
('Trichosanthes dioica',
 'Pointed Gourd',
 'परवल',
 'परवल',
 'Patola',
 'Cucurbitaceae',
 'Climbing vegetable; fruits used as light, digestible vegetable with use in Pitta and Kapha disorders in some Ayurvedic diet contexts.',
 'Cultivated in Eastern and Northern India, in warm, humid regions.',
 '["fruit"]',
 '["tikta","madhura_mild"]',
 'sheeta',
 'madhura',
 '["laghu"]',
 '["pitta_pacifying","kapha_pacifying"]',
 NULL,
 '["vitamins","minerals","fiber"]',
 '["light_digestive_food","mild_cooling_support"]',
 NULL,
 0,
 'cultivated',
 'Pointed_Gourd.jpg',
 'ayurveda'),

-- 137. Bitter Gourd
('Momordica charantia',
 'Bitter Gourd',
 'करेला',
 'कारलं',
 'Karavella / Karela',
 'Cucurbitaceae',
 'Climbing vegetable; bitter fruits used traditionally to support digestion and healthy blood sugar.',
 'Cultivated as vegetable crop in warm regions throughout India.',
 '["fruit"]',
 '["tikta","katu"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","pitta_pacifying"]',
 NULL,
 '["charantin","momordicosides"]',
 '["digestive","glycemic_support","liver_support_mild"]',
 NULL,
 0,
 'cultivated',
 'Bitter_Gourd.jpg',
 'ayurveda'),

-- 138. Bottle Gourd
('Lagenaria siceraria',
 'Bottle Gourd',
 'लौकी',
 'दुधी भोपळा',
 'Alabu / Lauki',
 'Cucurbitaceae',
 'Climbing vine; tender fruits used as light, cooling vegetable beneficial in Pitta and certain cardiac/urinary conditions.',
 'Cultivated widely in kitchen gardens and fields across India.',
 '["fruit"]',
 '["madhura","tikta_mild"]',
 'sheeta',
 'madhura',
 '["laghu"]',
 '["pitta_pacifying","kapha_pacifying"]',
 NULL,
 '["water_content","fiber","minerals"]',
 '["light_digestive_food","cooling","cardio_support_mild","urinary_support_mild"]',
 NULL,
 0,
 'cultivated',
 'Bottle_Gourd.jpg',
 'ayurveda'),

-- 139. Ridge Gourd
('Luffa acutangula',
 'Ridge Gourd',
 'तोरी',
 'शिराळे',
 'Dhodhaka / Jhinga',
 'Cucurbitaceae',
 'Climbing vegetable; young fruits used as light, mildly pungent vegetable aiding digestion.',
 'Cultivated extensively in warm climates as a vegetable crop.',
 '["fruit"]',
 '["tikta","katu_mild"]',
 'ushna',
 'katu',
 '["laghu"]',
 '["kapha_pacifying","vata_pacifying_mild"]',
 NULL,
 '["fiber","vitamins","minerals"]',
 '["light_digestive_food","mild_carminative"]',
 NULL,
 0,
 'cultivated',
 'Ridge_Gourd.jpg',
 'ayurveda'),

-- 140. Castor
('Ricinus communis',
 'Castor',
 'अरंडी',
 'एरंड',
 'Eranda',
 'Euphorbiaceae',
 'Shrub or small tree; oil from seeds used externally and internally in carefully regulated doses for Vata disorders.',
 'Waste lands, field borders; also cultivated as oilseed.',
 '["seed","oil","leaf"]',
 '["katu","tikta"]',
 'ushna',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying"]',
 NULL,
 '["ricinoleic_acid","fixed_oils"]',
 '["purgative_support","joint_support_external","vata_pacifying_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Castor.jpg',
 'ayurveda'),

-- 141. Indian Beech (Karanja)
('Pongamia pinnata',
 'Indian Beech',
 'करंज',
 'करंज',
 'Karanja',
 'Fabaceae',
 'Medium-sized tree; seeds and oil used externally for skin and joint applications in traditional practice.',
 'Coastal and riverine areas; avenue and boundary tree.',
 '["seed","oil","leaf"]',
 '["tikta","katu"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["karanjin","pongamol","fixed_oils"]',
 '["skin_support_external","joint_support_external","krimi_support_external"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Indian_Beech.jpg',
 'ayurveda'),

-- 142. Henna
('Lawsonia inermis',
 'Henna',
 'मेहंदी',
 'मेहेंदी',
 'Madayanti / Henna',
 'Lythraceae',
 'Shrub; leaves used externally as cooling, coloring and for scalp and skin support.',
 'Cultivated in dry and semi-arid regions; also grown in gardens.',
 '["leaf"]',
 '["tikta","kashaya"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '["pitta_pacifying","rakta_pacifying"]',
 NULL,
 '["lawsone","tannins","flavonoids"]',
 '["cooling_external","scalp_and_skin_support"]',
 NULL,
 0,
 'cultivated',
 'Henna.jpg',
 'ayurveda'),

-- 143. Guava
('Psidium guajava',
 'Guava',
 'अमरूद',
 'पेरू',
 'Peru / Amrudha (descriptive)',
 'Myrtaceae',
 'Small tree; fruits and leaves used as food and in folk Ayurveda for gut and metabolic support.',
 'Cultivated orchards and home gardens throughout tropical regions.',
 '["fruit","leaf"]',
 '["madhura","kashaya_mild"]',
 'ushna',
 'madhura',
 '["laghu"]',
 '["kapha_pacifying","pitta_pacifying_mild"]',
 NULL,
 '["vitamin_C","fiber","flavonoids"]',
 '["digestive_support","mild_antidiarrheal_leaf","metabolic_support_mild"]',
 NULL,
 0,
 'cultivated',
 'Guava.jpg',
 'ayurveda'),

-- 144. Papaya
('Carica papaya',
 'Papaya',
 'पपीता',
 'पपई',
 'Erandakarkati (in some texts)',
 'Caricaceae',
 'Soft-wooded plant; ripe fruit used as light laxative and digestive, unripe fruit used cautiously as tenderizer and in some traditional applications.',
 'Cultivated in home gardens and farms in tropical and subtropical regions.',
 '["fruit_ripe","fruit_unripe_leaf_with_caution"]',
 '["madhura","tikta_mild"]',
 'ushna',
 'madhura',
 '["laghu"]',
 '["kapha_pacifying","vata_pacifying_mild"]',
 NULL,
 '["papain","carotenoids","vitamin_C"]',
 '["digestive_support","mild_laxative_ripe","skin_support_mild"]',
 NULL,
 0,
 'cultivated',
 'Papaya.jpg',
 'ayurveda'),

-- 145. Indian Jujube (Ber)
('Ziziphus jujuba',
 'Indian Jujube',
 'बर',
 'बोर',
 'Badara / Ber',
 'Rhamnaceae',
 'Small tree; fruits used as mild laxative and nutritive, leaves and seeds used traditionally for calming support.',
 'Dry and semi-arid regions; widely cultivated and naturalized.',
 '["fruit","leaf","seed"]',
 '["madhura","kashaya_mild"]',
 'sheeta',
 'madhura',
 '["guru","snigdha"]',
 '["vata_pacifying","pitta_pacifying"]',
 NULL,
 '["vitamins","flavonoids","sugars"]',
 '["nutritive","mild_laxative","calming_support_mild"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Indian_Jujube.jpg',
 'ayurveda'),

-- 146. Mulberry
('Morus alba',
 'Mulberry',
 'शहतूत',
 'तूत',
 'Tudata / Tut (regional)',
 'Moraceae',
 'Medium tree; fruits and leaves used as food and in traditional practice for blood and metabolic support.',
 'Temperate to subtropical regions; cultivated and sometimes naturalized.',
 '["fruit","leaf"]',
 '["madhura","tikta_mild"]',
 'sheeta',
 'madhura',
 '["laghu","snigdha_mild"]',
 '["pitta_pacifying","rakta_pacifying"]',
 NULL,
 '["anthocyanins","flavonoids","vitamin_C"]',
 '["blood_support_mild","metabolic_support_mild","nutritive"]',
 NULL,
 0,
 'cultivated',
 'Mulberry.jpg',
 'ayurveda'),

-- 147. Camphor Tree
('Cinnamomum camphora',
 'Camphor Tree',
 'कपूर वृक्ष',
 'कापूर झाड',
 'Karpura Vriksha',
 'Lauraceae',
 'Evergreen tree; wood and leaves yield camphor, used in tiny quantities externally and in some formulations for respiratory and topical applications.',
 'Cultivated in gardens and some hilly regions; camphor often commercially produced.',
 '["wood","leaf","distilled_camphor"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","tikshna"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["camphor","terpenes"]',
 '["topical_rubefacient","respiratory_support_aromatic","krimi_support_external"]',
 NULL,
 0,
 'cultivated',
 'Camphor_Tree.jpg',
 'ayurveda'),

-- 148. Indian Borage (Ajwain Patta)
('Coleus aromaticus',
 'Indian Borage',
 'अजवाइन पत्ता',
 'ओवा पान',
 'Pashanabheda / Karpooravalli (regionally)',
 'Lamiaceae',
 'Aromatic succulent herb; leaves used in home remedies for cough, cold and digestion.',
 'Kitchen gardens and pots in many parts of India; prefers warm climate.',
 '["leaf"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","snigdha_mild"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["essential_oils","thymol_like_compounds"]',
 '["mild_expectorant","carminative","respiratory_support_mild"]',
 NULL,
 0,
 'cultivated',
 'Indian_Borage.jpg',
 'ayurveda'),

-- 149. Vana Tulsi
('Ocimum gratissimum',
 'Vana Tulsi',
 'वन तुलसी',
 'वन तुळस',
 'Vanatulasi',
 'Lamiaceae',
 'Aromatic shrub; leaves used similarly to other Tulsi types for respiratory, immune and digestive support.',
 'Wild and cultivated in many warm regions, hedges and field borders.',
 '["leaf"]',
 '["katu","tikta","madhura_mild"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["essential_oils","eugenol","thymol"]',
 '["respiratory_support","immune_support_mild","digestive_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Vana_Tulsi.jpg',
 'ayurveda'),

-- 150. Climbing Brinjal (Solanum trilobatum)
('Solanum trilobatum',
 'Climbing Brinjal',
 'अलगुंडा (प्रांतीय)',
 'तूती सोलanum (प्रांतीय)',
 'Alarka / Kantakari_var (regionally used)',
 'Solanaceae',
 'Climbing shrub; leaves and berries used in some Southern Ayurvedic traditions for respiratory and Kapha disorders.',
 'Dry scrublands and fences in South India; sometimes cultivated.',
 '["leaf","fruit"]',
 '["tikta","katu"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '["kapha_pacifying","vata_pacifying"]',
 NULL,
 '["steroidal_alkaloids","saponins"]',
 '["respiratory_support","expectorant_support"]',
 NULL,
 0,
 'wild_and_cultivated',
 'Climbing_Brinjal.jpg',
 'ayurveda');

-- =========================================================
-- PLANT–DISEASE MAPPING FOR PLANTS 131–150
-- =========================================================

------------------------------------------------------------
-- 131. Gudmar (Gymnema sylvestre)
------------------------------------------------------------
-- Gudmar – Diabetes Mellitus Type 2
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Gudmar'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Gudmar – Obesity (metabolic / appetite support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Gudmar'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 132. Tagara (Indian Valerian)
------------------------------------------------------------
-- Tagara – Anxiety and Stress
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Anxiety and Stress'
WHERE p.common_name_en = 'Tagara'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Tagara – Memory Weakness (calming sleep/nootropic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Memory Weakness'
WHERE p.common_name_en = 'Tagara'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Tagara – Neuromuscular Weakness (Vata-calming support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Tagara'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 133. Asafoetida (Hing)
------------------------------------------------------------
-- Asafoetida – Diarrhea and IBS (Vata-colic / gas patterns, small doses)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Asafoetida'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Asafoetida – Intestinal Worm Infestation (krimi support, traditional)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Intestinal Worm Infestation'
WHERE p.common_name_en = 'Asafoetida'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 134. Indian Mustard
------------------------------------------------------------
-- Indian Mustard – Bronchial Asthma (warming, kapha-melting support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Bronchial Asthma'
WHERE p.common_name_en = 'Indian Mustard'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Indian Mustard – Chronic Cough and Bronchitis (warming spice support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Indian Mustard'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 135. Indian Senna
------------------------------------------------------------
-- Note: classical laxative mainly for constipation; your disease list
-- does not include constipation, so we do NOT map it here to avoid
-- misleading associations.

------------------------------------------------------------
-- 136. Pointed Gourd (Patola)
------------------------------------------------------------
-- Pointed Gourd – Diabetes Mellitus Type 2 (light vegetable support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Pointed Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Pointed Gourd – Obesity (low-calorie, Kapha-oriented diet support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Pointed Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 137. Bitter Gourd (Karela)
------------------------------------------------------------
-- Bitter Gourd – Diabetes Mellitus Type 2 (classical metabolic use)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Bitter Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Bitter Gourd – Obesity (Kapha/meda diet support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Bitter Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 138. Bottle Gourd (Lauki)
------------------------------------------------------------
-- Bottle Gourd – Ischemic Heart Disease (light, cardiac-friendly diet support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Ischemic Heart Disease'
WHERE p.common_name_en = 'Bottle Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Bottle Gourd – Obesity (low-calorie, pitta-pacifying diet support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Bottle Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 139. Ridge Gourd
------------------------------------------------------------
-- Ridge Gourd – Diabetes Mellitus Type 2 (light veg in diabetic diet)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Ridge Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Ridge Gourd – Obesity (low-calorie, Kapha diet support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Obesity'
WHERE p.common_name_en = 'Ridge Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 140. Castor (Eranda)
------------------------------------------------------------
-- Castor – Neuromuscular Weakness (Vata/joint-related support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Castor'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 141. Indian Beech (Karanja)
------------------------------------------------------------
-- Indian Beech – Chronic Skin Disease (external applications)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Indian Beech'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 142. Henna
------------------------------------------------------------
-- Henna – Chronic Skin Disease (cooling scalp/skin support, external)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Skin Disease'
WHERE p.common_name_en = 'Henna'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 143. Guava
------------------------------------------------------------
-- Guava Leaf – Diarrhea and IBS (folk antidiarrheal leaf decoction)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diarrhea and IBS'
WHERE p.common_name_en = 'Guava'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 144. Papaya
------------------------------------------------------------
-- Papaya – Diabetes Mellitus Type 2 (leaf-based metabolic support contexts)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Papaya'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 145. Indian Jujube (Ber)
------------------------------------------------------------
-- Indian Jujube – Anxiety and Stress (mild calming support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Anxiety and Stress'
WHERE p.common_name_en = 'Indian Jujube'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Indian Jujube – Neuromuscular Weakness (balya/nutritive)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Neuromuscular Weakness'
WHERE p.common_name_en = 'Indian Jujube'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 146. Mulberry
------------------------------------------------------------
-- Mulberry – Diabetes Mellitus Type 2 (leaf metabolic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Diabetes Mellitus Type 2'
WHERE p.common_name_en = 'Mulberry'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Mulberry – Chronic Liver Disorder (Rakta/pitta & metabolic support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Liver Disorder'
WHERE p.common_name_en = 'Mulberry'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 147. Camphor Tree
------------------------------------------------------------
-- Camphor Tree – Chronic Cough and Bronchitis (aromatic rubs/inhalations)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Camphor Tree'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Camphor Tree – Bronchial Asthma (traditional aromatic support, cautious)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Bronchial Asthma'
WHERE p.common_name_en = 'Camphor Tree'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 148. Indian Borage (Ajwain Patta)
------------------------------------------------------------
-- Indian Borage – Chronic Cough and Bronchitis
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Indian Borage'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Indian Borage – Bronchial Asthma (home remedy, mild support)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Bronchial Asthma'
WHERE p.common_name_en = 'Indian Borage'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 149. Vana Tulsi
------------------------------------------------------------
-- Vana Tulsi – Chronic Cough and Bronchitis
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Vana Tulsi'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Vana Tulsi – Bronchial Asthma (Kapha/Vata respiratory patterns)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Bronchial Asthma'
WHERE p.common_name_en = 'Vana Tulsi'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

------------------------------------------------------------
-- 150. Climbing Brinjal (Solanum trilobatum)
------------------------------------------------------------
-- Climbing Brinjal – Chronic Cough and Bronchitis (classical Southern use)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Chronic Cough and Bronchitis'
WHERE p.common_name_en = 'Climbing Brinjal'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- Climbing Brinjal – Bronchial Asthma (expectorant support, traditional)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d ON d.name_en = 'Bronchial Asthma'
WHERE p.common_name_en = 'Climbing Brinjal'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

-- =========================================================
-- PREPARATIONS – PRIMARY HERB FROM PLANTS 131–150
-- =========================================================

------------------------------------------------------------
-- 1. Gudmar Leaf Churna
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Gudmar Leaf Churna',
  'गुड़मार पत्ती चूर्ण',
  'गुढमार पानांचा चूर्ण',
  'Meshashringi Patra Churna (simplified)',
  'powder',
  'metabolic_support',
  '1) Collect Gudmar leaves from identified plants and wash thoroughly. 2) Shade-dry the leaves until completely crisp and moisture-free. 3) Powder the dried leaves to fine churna. 4) Sieve if required to get uniform powder. 5) Store in airtight container away from moisture.',
  'cleaning_tray; drying_surface; grinder; sieve; airtight_container',
  '1–2 days for proper drying depending on climate; powdering time is short.',
  'Close to dry weight of leaves after cleaning and drying.',
  'Store in cool, dry place in airtight container away from direct sunlight.',
  'Typically used within 3–6 months under proper storage conditions.',
  '{"adult":"1–3 g once or twice daily under professional supervision, especially in diabetes","child":"only under expert supervision with individualized dose"}',
  'usually_before_meals_or_as_directed',
  'plain_water_or_as_directed_by_practitioner',
  'Gudmar leaf powder is used in Ayurveda as a supportive measure in Madhumeha/Type 2 diabetes and appetite for sweets, always along with diet, lifestyle and medical care.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Gudmar'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Gudmar Leaf Churna'
  );

------------------------------------------------------------
-- 2. Tagara Sleep Support Powder
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Tagara Sleep Support Powder',
  'टगर निद्रा चूर्ण',
  'टगर निद्रा चूर्ण',
  'Tagara Churna (simplified)',
  'powder',
  'sleep_and_anxiety_support',
  '1) Clean Tagara rhizomes/roots and cut into small pieces. 2) Dry thoroughly in shade, avoiding high heat. 3) Powder to a moderately fine churna. 4) Sieve if needed and store in airtight container. 5) Use in very small, supervised doses.',
  'knife; drying_tray; grinder; sieve; airtight_container',
  'Several hours to day(s) for drying; grinding time is short.',
  'Close to dry root weight after cleaning and drying.',
  'Keep in airtight container in a cool, dry place away from strong light.',
  'Commonly used within 6 months if stored well.',
  '{"adult":"0.5–2 g at bedtime under professional supervision","child":"not routinely used; only under expert guidance"}',
  'bedtime',
  'lukewarm_water_or_as_directed',
  'Tagara powder is traditionally used as mild sedative/anxiolytic support in Ayurveda. Dose is individualized and may interact with other sedatives; use under supervision.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Tagara'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Tagara Sleep Support Powder'
  );

------------------------------------------------------------
-- 3. Bitter Gourd Fresh Juice (Karela Juice)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Bitter Gourd Juice',
  'करेला का रस',
  'कारल्याचा रस',
  'Karavella Swarasa (simplified)',
  'juice',
  'metabolic_support',
  '1) Select fresh, tender Bitter Gourd fruits and wash thoroughly. 2) Remove seeds if large and chop fruits into small pieces. 3) Crush/blend with small quantity of water to obtain juice. 4) Filter if required and consume immediately in small, supervised quantity.',
  'knife; cutting_board; juicer_or_blender; strainer; measuring_cup',
  '15–20 minutes.',
  'Quantity depends on number of fruits; typically 30–50 ml per person.',
  'Use fresh; do not store for long durations.',
  'Use immediately; discard after a few hours.',
  '{"adult":"10–30 ml once daily on empty stomach or before food under strict supervision","child":"use only under expert guidance"}',
  'morning_empty_stomach_or_as_directed',
  'plain_or_diluted_with_small_amount_of_water',
  'Fresh Bitter Gourd juice is a strong preparation traditionally used in small doses as metabolic support in diabetes-related contexts; care is required to avoid excessive use or hypoglycemia.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Bitter Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Bitter Gourd Juice'
  );

------------------------------------------------------------
-- 4. Bottle Gourd Light Soup
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Bottle Gourd Light Soup',
  'लौकी का हल्का सूप',
  'दुधी भोपळ्याचे हलके सूप',
  'Alabu Supa (dietary form)',
  'medicated_food',
  'cardiac_and_metabolic_support_food',
  '1) Peel and cut tender Bottle Gourd into small cubes after washing. 2) Boil in adequate water until soft. 3) Lightly mash and season with small amount of suitable spice (e.g., cumin, black pepper) and a little salt as appropriate. 4) Avoid heavy oil and frying; keep preparation light and easily digestible. 5) Serve warm as part of meal.',
  'knife; cooking_pot; ladle; masher_or_spoon',
  '20–30 minutes.',
  '2–3 servings depending on quantity of Bottle Gourd used.',
  'Best consumed fresh; refrigerate only if needed for short time.',
  'Use within the same day; preferably within a few hours.',
  '{"adult":"one bowl as part of lunch or dinner in indicated individuals","child":"smaller portion according to appetite"}',
  'with_main_meal',
  'taken_as_part_of_sattvic_light_diet',
  'Bottle Gourd light soup is used as a part of Ayurvedic-style light diet for certain heart, obesity and Pitta-related conditions; emphasis is on proper selection of fresh gourds (not overly bitter) and medical supervision if there are cardiac issues.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Bottle Gourd'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Bottle Gourd Light Soup'
  );

------------------------------------------------------------
-- 5. Indian Borage Leaf Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Indian Borage Leaf Decoction',
  'अजवाइन पत्ती काढ़ा',
  'ओव्याच्या पानांचा काढा',
  'Indian Borage Kwatha (home-style)',
  'decoction',
  'respiratory_support',
  '1) Pluck a few fresh Indian Borage leaves and wash properly. 2) Tear or cut them and add to water in a small vessel. 3) Boil gently for several minutes until aroma is released and water is reduced slightly. 4) Filter and use warm in small quantities.',
  'small_pot; heating_source; strainer; measuring_cup',
  '10–15 minutes.',
  'One or two small servings (30–60 ml each).',
  'Use fresh; keep covered if using within a few hours.',
  'Same-day use; preferably within a few hours of preparation.',
  '{"adult":"15–30 ml warm, sipped 1–2 times daily during acute phase under guidance","child":"very small quantity and only under professional supervision"}',
  'after_meals_or_as_directed',
  'plain_warm',
  'Indian Borage leaf decoction is a common household remedy for mild cough/cold and digestive discomfort, typically used short-term and alongside appropriate medical care where needed.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Indian Borage'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Indian Borage Leaf Decoction'
  );

------------------------------------------------------------
-- 6. Vana Tulsi Herbal Tea
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Vana Tulsi Herbal Tea',
  'वन तुलसी की हर्बल चाय',
  'वन तुळशीची हर्बल चहा',
  'Vanatulasi Phanta (infusion)',
  'herbal_tea',
  'respiratory_and_immune_support',
  '1) Take fresh or shade-dried Vana Tulsi leaves. 2) Add to hot water just off the boil. 3) Cover and steep for 5–10 minutes. 4) Strain and drink warm. 5) Optionally add small amount of honey only when tea is lukewarm, if suitable.',
  'cup_or_teapot; strainer; kettle_or_heating_source',
  '10–15 minutes including steeping time.',
  'One cup (about 100–150 ml) per preparation.',
  'Best used fresh and warm.',
  'Use within a short time after preparation.',
  '{"adult":"one cup once or twice daily in suitable seasons","child":"small quantity diluted, only if appropriate"}',
  'morning_or_evening',
  'plain_or_with_small_amount_of_honey_when_lukewarm',
  'Vana Tulsi herbal tea is used in Ayurveda-inspired practice to support respiratory comfort, light digestion and general well-being, especially in changing seasons.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Vana Tulsi'
  AND NOT EXISTS (
    SELECT 1 FROM preparations pr WHERE pr.name_en = 'Vana Tulsi Herbal Tea'
  );

