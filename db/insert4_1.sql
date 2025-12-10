-- WALNUT (Unani)
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
) VALUES (
  'Juglans regia',
  'Walnut',
  'अखरोट',
  'अक्रोड',
  NULL,
  'Juglandaceae',
  'Temperate tree; nuts are used in Unani regimes as nutritive, brain and joint-supporting ingredient in small doses.',
  'Temperate Himalayan orchards and imported produce.',
  '["seed_kernel","oil"]',
  '["madhura","kashaya_mild"]',
  'ushna_mild',
  'madhura',
  '["guru","snigdha"]',
  '["vata_pacifying","kapha_pacifying_mild"]',
  NULL,
  '["omega_3_fats","polyphenols","vitamin_E"]',
  '["nutritive_support","joint_support_mild","brain_support_traditional"]',
  NULL,
  0,
  'cultivated_and_imported',
  'Walnut.jpg',
  'unani'
);

-- PUMPKIN SEED (Unani)
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
) VALUES (
  'Cucurbita pepo',
  'Pumpkin Seed',
  'कद्दू के बीज',
  'भोपळ्याच्या बिया',
  NULL,
  'Cucurbitaceae',
  'Creeping or climbing plant; seeds are used in Unani as nutritive and urinary tract supportive food ingredient.',
  'Cultivated as vegetable crop in fields and home gardens.',
  '["seed","pulp"]',
  '["madhura"]',
  'sheeta_mild',
  'madhura',
  '["guru","snigdha"]',
  '["pitta_pacifying","vata_pacifying_mild"]',
  NULL,
  '["fatty_acids","zinc","phytosterols"]',
  '["prostate_support_mild","nutritive_support","urinary_support_mild"]',
  NULL,
  0,
  'cultivated',
  'Pumpkin_Seed.jpg',
  'unani'
);

-- MUSKMELON (Unani)
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
) VALUES (
  'Cucumis melo',
  'Muskmelon',
  'खरबूजा',
  'खरबूज',
  NULL,
  'Cucurbitaceae',
  'Climbing vine; sweet aromatic fruits form part of Unani diets for cooling and mild laxative support when digestion is adequate.',
  'Cultivated in plains as a warm-season crop.',
  '["fruit_fresh"]',
  '["madhura"]',
  'sheeta_mild',
  'madhura',
  '["laghu","snigdha"]',
  '["pitta_pacifying","vata_pacifying_mild"]',
  NULL,
  '["sugars","water","vitamins","minerals"]',
  '["cooling_support","mild_laxative_support","nutritive_support"]',
  NULL,
  0,
  'cultivated',
  'Muskmelon.jpg',
  'unani'
);

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Itrifal-e-Isabgol',
  'इत्रिफाल-ए-इसबगोल',
  'इत्रिफाल-ए-इसबगोल',
  'Itrifal-e-Isabgol',
  'electuary',
  'digestive_and_bowel_support',
  '1) Lightly roast Isabgol husk on very low heat. 2) Add small amount of honey or sugar syrup to bind. 3) Mix to soft paste consistency. 4) Store in clean glass jar.',
  'mixing_bowl;wooden_spoon;airtight_glass_jar',
  '20–25 minutes',
  'Variable; small batch electuary',
  'Store airtight away from moisture.',
  '1–2 months clean handling.',
  '{"adult":"1–2 teaspoons at bedtime with lukewarm water","child":"use only under practitioner guidance"}',
  'bedtime',
  'lukewarm_water',
  'Traditional Unani electuary for mild bowel regularity. Should be taken with adequate hydration.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en = 'Isabgol'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Itrifal-e-Isabgol');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Arq-e-Kasni',
  'अर्क-ए-कसनी',
  'अर्क-ए-कसनी',
  'Arq-e-Kasni',
  'herbal_water',
  'liver_and_digestive_support',
  '1) Clean Chicory roots. 2) Boil in large pot of water and allow steam to condense using simple lid-based distillation. 3) Collect condensed herbal water (Arq).',
  'large_pot;inverted_lid;collection_bowl;strainer',
  '1–1.5 hours',
  '300–500 ml depending on batch',
  'Refrigerate; store in sterilized bottle.',
  '7–10 days if refrigerated.',
  '{"adult":"10–20 ml once or twice daily","child":"use only under guidance"}',
  'morning_or_before_food',
  'plain',
  'Classically used in Unani for digestive comfort; prepared through gentle hydrodistillation.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en = 'Chicory'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Arq-e-Kasni');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Roghan-e-Kalonji',
  'रोगन-ए-कलौंजी',
  'रोगन-ए-कलौंजी',
  'Roghan-e-Kalonji',
  'oil_preparation',
  'respiratory_and_digestive_support_mild',
  '1) Lightly warm edible oil (typically sesame or olive). 2) Add crushed Black Seed and simmer on very low heat. 3) Strain and bottle.',
  'pan;strainer;dark_glass_bottle',
  '25–30 minutes',
  '100–200 ml',
  'Store in dark glass bottle away from heat.',
  '2–3 months',
  '{"adult":"half to one teaspoon once daily","child":"use only if advised"}',
  'morning_or_after_food',
  'as_is',
  'Traditional Unani oil used in tiny oral or external amounts; strong spice—avoid excess.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en = 'Black Seed'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Roghan-e-Kalonji');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Imli',
  'शरबत-ए-इमली',
  'शरबत-ए-इमली',
  'Sharbat-e-Imli',
  'syrup',
  'cooling_and_digestive_support',
  '1) Soak Tamarind pulp in warm water. 2) Mash and strain. 3) Add sugar and cook to light syrup consistency. 4) Cool and bottle.',
  'soaking_bowl;pan;strainer;bottle',
  '45–60 minutes',
  '1–2 bottles depending on batch',
  'Refrigerate after opening.',
  '1–2 months refrigerated',
  '{"adult":"15–30 ml mixed in water once or twice daily","child":"small diluted quantity"}',
  'after_food_or_as_drink',
  'cold_water',
  'Popular Unani cooling syrup used in summer; sweet and sour—watch in diabetes.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en = 'Tamarind'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Sharbat-e-Imli');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Qehwa-e-Sana',
  'क़हवा-ए-सना',
  'क़हवा-ए-सना',
  'Qehwa-e-Sana',
  'decoction',
  'bowel_cleansing_support',
  '1) Take a very small amount of Senna leaf/pod. 2) Boil in water for few minutes only. 3) Strain and use in strictly regulated dose.',
  'small_pot;strainer',
  '10–15 minutes',
  '50–100 ml',
  'Use fresh only.',
  'same_day',
  '{"adult":"10–20 ml only under supervision","child":"not recommended"}',
  'as_directed',
  'plain',
  'Senna has strong effect; used in very small, supervised doses in Unani.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en = 'Alexandrian Senna'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Qehwa-e-Sana');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps, equipment_needed,
  duration, yield, storage, shelf_life, dosage_json, timing,
  anupana, notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Ailwa',
  'शरबत-ए-एलोवेरा',
  'शरबत-ए-कोरफड',
  'Sharbat-e-Ailwa',
  'syrup',
  'cooling_and_digestive_support',
  '1) Extract fresh Aloe Vera gel. 2) Blend with water. 3) Cook gently with sugar until thin syrup consistency. 4) Cool and bottle.',
  'blender;pan;strainer;bottle',
  '30–40 minutes',
  '1–2 bottles',
  'Refrigerate after bottling.',
  '1–2 months refrigerated',
  '{"adult":"15–25 ml diluted in water","child":"mildly diluted as guided"}',
  'before_food_or_as_drink',
  'cold_water',
  'Traditional cooling syrup used in summer months; avoid in diarrhea.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en = 'Aloe Vera'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Sharbat-e-Ailwa');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Mulhathi',
  'शरबत-ए-मुलेठी',
  'शरबत-ए-जेष्ठमध (यूनानी)',
  'Sharbat-e-Mulhathi',
  'syrup',
  'throat_and_digestive_support',
  '1) Boil Licorice root in water until reduced. 2) Filter decoction. 3) Add sugar and cook to syrup consistency. 4) Cool and bottle.',
  'pot;strainer;pan;bottle',
  '45–60 minutes',
  '1–2 bottles',
  'Refrigerate after opening.',
  '1–2 months',
  '{"adult":"10–20 ml diluted in water","child":"5–10 ml diluted only if advised"}',
  'after_food',
  'water',
  'Classical Unani syrup for mild throat dryness and cough irritation.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Licorice (Unani)'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Sharbat-e-Mulhathi');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Murabba-e-Anjeer',
  'मुरब्बा-ए-अंजीर',
  'मुरब्बा-ए-अंजीर',
  'Murabba-e-Anjeer',
  'conserve',
  'nutritive_support',
  '1) Soak dried figs. 2) Cook in sugar syrup until soft. 3) Store in clean glass jar.',
  'soaking_bowl;pan;jar',
  '60–90 minutes',
  '10–15 pieces',
  'Store airtight in cool place.',
  '2–3 months',
  '{"adult":"1–2 pieces daily","child":"1 small piece if suitable"}',
  'morning',
  'as_is',
  'Unani nutritive preserve used in weakness and constipation tendencies.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Fig'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Murabba-e-Anjeer');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Roghan-e-Badam Shirin',
  'रोगन-ए-बादाम शिरीन',
  'रोगन-ए-बदाम शिरीन',
  'Roghan-e-Badam Shirin',
  'oil_preparation',
  'brain_and_nutritive_support',
  '1) Grind Almond kernels. 2) Warm gently with base oil. 3) Filter to obtain sweet almond oil.',
  'grinder;pan;cloth_filter;bottle',
  '45–60 minutes',
  '100–200 ml',
  'Store in cool place.',
  '2–3 months',
  '{"adult":"half–1 teaspoon daily","child":"few drops under guidance"}',
  'morning_or_bedtime',
  'as_is',
  'Traditional almond oil used in tiny doses for nutritive support.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Almond'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Roghan-e-Badam Shirin');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Majoon-e-Akhrot',
  'माजून-ए-अखरोट',
  'माजून-ए-अक्रोड',
  'Majoon-e-Akhrot',
  'electuary',
  'nutritive_and_joint_support',
  '1) Grind Walnut kernels to paste. 2) Add honey and mild warming spices. 3) Mix to semisolid electuary. 4) Store airtight.',
  'grinder;mixing_bowl;jar',
  '30–45 minutes',
  '50grams to 100grams',
  'Small jar',
  '1–2 months',
  '{"adult":"1 teaspoon daily","child":"tiny amount under guidance"}',
  'morning',
  'lukewarm_milk_optional',
  'Used as nutritive electuary in weakness and joint discomfort.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Walnut'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Majoon-e-Akhrot');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Majoon-e-Maghz-e-Kadu',
  'माजून-ए-मग़ज़-ए-कद्दू',
  'माजून-ए-कद्दू बिया',
  'Majoon-e-Maghz-e-Kadu',
  'electuary',
  'urinary_and_male_support_mild',
  '1) Grind Pumpkin seeds to paste. 2) Mix with honey. 3) Add mild spices if suitable. 4) Store airtight.',
  'grinder;mixing_bowl;jar',
  '20–30 minutes',
  '50grams to 100grams',
  'Small jar',
  '1–2 months',
  '{"adult":"1 teaspoon daily","child":"few drops under guidance"}',
  'morning',
  'lukewarm_water',
  'Traditional nutritive electuary supporting mild urinary tract wellbeing.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Pumpkin Seed'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Majoon-e-Maghz-e-Kadu');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Kheera',
  'शरबत-ए-खीरा',
  'शरबत-ए-काकडी',
  'Sharbat-e-Kheera',
  'syrup',
  'cooling_and_hydration_support',
  '1) Blend peeled Cucumber. 2) Filter to extract juice. 3) Add sugar and cook lightly to thin syrup. 4) Bottle.',
  'blender;sieve;pan;bottle',
  '30–40 minutes',
  '1 bottle',
  'Refrigerate',
  '2–3 weeks refrigerated',
  '{"adult":"15–30 ml with cold water","child":"small diluted portion"}',
  'afternoon_or_as_drink',
  'cold_water',
  'Used in Unani dietetics during hot seasons for cooling.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Cucumber'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Sharbat-e-Kheera');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Tarbooz',
  'शरबत-ए-तरबूज',
  'शरबत-ए-कलिंगड',
  'Sharbat-e-Tarbooz',
  'syrup',
  'hydration_and_cooling_support',
  '1) Blend Watermelon pulp. 2) Strain. 3) Add sugar to make mild syrup. 4) Bottle chilled.',
  'blender;strainer;pan;bottle',
  '30 minutes',
  '1 bottle',
  'Refrigerate',
  '1–2 weeks',
  '{"adult":"20–40 ml diluted","child":"small diluted amount"}',
  'midday',
  'cold_water',
  'Summer cooling syrup in Unani regimens.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Watermelon'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Sharbat-e-Tarbooz');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Murabba-e-Kharbooja',
  'मुरब्बा-ए-खरबूजा',
  'मुरब्बा-ए-खरबूज',
  'Murabba-e-Kharbooja',
  'conserve',
  'nutritive_cooling_support',
  '1) Cut Muskmelon pieces. 2) Cook in sugar syrup until translucent. 3) Cool and bottle.',
  'pan;sieve;jar',
  '60–90 minutes',
  '10–15 pieces',
  'Small jar',
  '1–2 months',
  '{"adult":"1–2 small pieces","child":"half piece if suitable"}',
  'morning',
  'as_is',
  'Cooling and mildly laxative Unani preserve.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Muskmelon'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Murabba-e-Kharbooja');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Amla',
  'शरबत-ए-आवला (यूनानी)',
  'शरबत-ए-आवळा (यूनानी)',
  'Sharbat-e-Amla',
  'syrup',
  'cooling_and_liver_support_mild',
  '1) Boil Amla pieces. 2) Mash and filter. 3) Cook pulp with sugar to syrup. 4) Add small rose essence if suitable.',
  'pot;strainer;pan;bottle',
  '60 minutes',
  '1–2 bottles',
  'Refrigerate',
  '1–2 months',
  '{"adult":"10–20 ml diluted","child":"small amount diluted"}',
  'after_food',
  'water',
  'Classic cooling and nutritive Unani syrup.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Indian Gooseberry (Unani)'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Sharbat-e-Amla');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Unnab',
  'शरबत-ए-ऊन्नाब',
  'शरबत-ए-बोर',
  'Sharbat-e-Unnab',
  'syrup',
  'respiratory_and_throat_support',
  '1) Boil dried Jujube in water until soft. 2) Filter. 3) Add sugar to create syrup. 4) Cool and bottle.',
  'pot;strainer;pan;bottle',
  '45–60 minutes',
  '1 bottle',
  'Refrigerate',
  '1–2 months',
  '{"adult":"10–20 ml diluted 1–2 times daily","child":"small warm diluted amount"}',
  'evening',
  'lukewarm_water',
  'One of the classical Unani throat syrups (Sharbat-e-Unnab).',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Jujube (Unani)'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Sharbat-e-Unnab');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Halwa-e-Gajar (Unani)',
  'हलवा-ए-गाजर (यूनानी)',
  'गाजर हलवा (यूनानी)',
  'Halwa-e-Gajar',
  'medicated_food',
  'nutritive_support',
  '1) Grate carrot. 2) Cook with milk and small ghee. 3) Add sugar. 4) Cook until thick. 5) Serve warm.',
  'grater;pan;spoon',
  '30–45 minutes',
  '2–4 servings',
  'Refrigerate',
  '2–3 days',
  '{"adult":"small bowl once daily","child":"small portion"}',
  'evening',
  'as_is',
  'Used nutritionally in weakness and low appetite.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Carrot'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Halwa-e-Gajar (Unani)');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Chukandar',
  'शरबत-ए-चुकंदर',
  'शरबत-ए-बीट',
  'Sharbat-e-Chukandar',
  'syrup',
  'blood_and_liver_support_mild',
  '1) Boil Beetroot slices. 2) Blend and strain. 3) Add sugar to prepare mild syrup. 4) Chill.',
  'pan;blender;strainer;bottle',
  '45 minutes',
  '1 bottle',
  'Refrigerate',
  '2–3 weeks',
  '{"adult":"20–30 ml diluted","child":"small diluted amount"}',
  'morning',
  'water',
  'Used in Unani nutrition for mild blood support.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Beetroot'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Sharbat-e-Chukandar');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Qehwa-e-Ajmod',
  'क़हवा-ए-अजमोद',
  'क़हवा-ए-अजमोदा',
  'Qehwa-e-Ajmod',
  'decoction',
  'digestive_and_joint_support',
  '1) Crush Celery seeds. 2) Boil in water for 10 minutes. 3) Filter and drink warm.',
  'pot;strainer',
  '10–15 minutes',
  '40–80 ml',
  'Use fresh.',
  'same_day',
  '{"adult":"20–30 ml after food","child":"very small amount only"}',
  'after_food',
  'warm_water',
  'Unani digestive/joint-support decoction.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Celery Seed'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Qehwa-e-Ajmod');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Joshanda-e-Dill',
  'जुशनदा-ए-सुवा',
  'जुशनदा-ए-शेपू',
  'Joshanda-e-Dill',
  'decoction',
  'digestive_and_colic_support',
  '1) Add Dill seeds to water. 2) Boil for 10 minutes. 3) Strain warm.',
  'small_pot;strainer',
  '10–15 minutes',
  '60–100 ml',
  'Fresh only',
  'same_day',
  '{"adult":"20–30 ml warm","child":"few teaspoons warm under supervision"}',
  'after_meals',
  'warm_water',
  'Used for digestive comfort and infant colic relief (only under guidance).',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Dill (Unani)'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Joshanda-e-Dill');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Sharbat-e-Pudina',
  'शरबत-ए-पुदीना',
  'शरबत-ए-पुदिना',
  'Sharbat-e-Pudina',
  'syrup',
  'digestive_and_cooling_support',
  '1) Grind fresh Mint leaves. 2) Extract juice. 3) Mix with sugar syrup. 4) Bottle chilled.',
  'blender;strainer;pan;bottle',
  '30–45 minutes',
  '1 bottle',
  'Refrigerate',
  '2–3 weeks',
  '{"adult":"10–20 ml diluted","child":"small diluted sip"}',
  'after_meals',
  'water',
  'Used for digestive comfort and cooling in summer.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Mint (Unani)'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Sharbat-e-Pudina');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Saqooq-e-Kulfa',
  'सकूक-ए-कुलफा',
  'सकूक-ए-कुलफा',
  'Saqooq-e-Kulfa',
  'herbal_water',
  'cooling_and_skin_support',
  '1) Soak Purslane leaves in warm water. 2) Allow infusion 1–2 hours. 3) Strain and drink cool.',
  'bowl;strainer',
  '1–2 hours infusion',
  '1–2 glasses',
  'Use same day.',
  'same_day',
  '{"adult":"half–1 glass","child":"small amount"}',
  'afternoon',
  'as_is',
  'Cooling Unani beverage sometimes used in skin/heat conditions.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Purslane'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Saqooq-e-Kulfa');

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage,
  shelf_life, dosage_json, timing, anupana,
  notes, ayush_system, plant_id
)
SELECT
  'Yakhni-e-Palak',
  'यख़नी-ए-पालक',
  'यख़नी-ए-पालक',
  'Yakhni-e-Palak',
  'medicated_broth',
  'nutritive_and_blood_support',
  '1) Boil Spinach leaves with mild spices. 2) Strain broth. 3) Serve warm.',
  'pot;strainer;cup',
  '20–25 minutes',
  '1–2 servings',
  'Refrigerate if needed',
  '1 day',
  '{"adult":"one bowl","child":"small portion"}',
  'with_meal',
  'as_is',
  'Traditional light broth used in weakness and mild anemia.',
  'unani',
  p.id
FROM plants p
WHERE p.common_name_en='Spinach'
AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en='Yakhni-e-Palak');

-- Helper: Isabgol (U1)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Isabgol'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Digestive Weakness and Gas')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Isabgol'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Constipation'));

-- Chicory (U2)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Chicory'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Digestive Weakness and Gas')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Chicory'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Liver Heat and Fatty Tendency'));

-- Black Seed (U3)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Black Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Digestive Weakness and Gas')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Black Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Cough and Throat Irritation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Black Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Cold, Catarrh and Sneezing')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Black Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Mild Asthma and Breathlessness'));

-- Tamarind (U4)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Tamarind'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Digestive Weakness and Gas')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Tamarind'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Constipation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Tamarind'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Liver Heat and Fatty Tendency'));

-- Alexandrian Senna (U5)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Alexandrian Senna'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Constipation'));

-- Aloe Vera (U6)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Aloe Vera'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Constipation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Aloe Vera'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Liver Heat and Fatty Tendency')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Aloe Vera'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Skin Heat and Itching'));

-- Sweet Violet (U7)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Sweet Violet'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Cough and Throat Irritation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Sweet Violet'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Cold, Catarrh and Sneezing')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Sweet Violet'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Mild Asthma and Breathlessness'));

-- Licorice (Unani) (U8)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Licorice (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Cough and Throat Irritation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Licorice (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue'));

-- Fig (U9)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Fig'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Constipation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Fig'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue'));

-- Almond (U10)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Almond'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Almond'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Nervous Tension and Anxiety')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Almond'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Sleep Disturbance and Insomnia'));

-- Walnut (U11)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Walnut'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Joint Pain and Stiffness')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Walnut'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue'));

-- Pumpkin Seed (U12)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Pumpkin Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Obesity and Weight Gain')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Pumpkin Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Kidney and Bladder Stone Tendency')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Pumpkin Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Urinary Burning and Frequency'));

-- Cucumber (U13)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Cucumber'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Digestive Weakness and Gas')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Cucumber'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Skin Heat and Itching'));

-- Watermelon (U14)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Watermelon'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Liver Heat and Fatty Tendency')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Watermelon'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Obesity and Weight Gain')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Watermelon'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Skin Heat and Itching'));

-- Muskmelon (U15)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Muskmelon'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Constipation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Muskmelon'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Obesity and Weight Gain')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Muskmelon'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Skin Heat and Itching'));

-- Indian Gooseberry (Unani) (U16)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Indian Gooseberry (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Liver Heat and Fatty Tendency')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Indian Gooseberry (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Anemia Tendency')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Indian Gooseberry (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani High Blood Sugar Tendency')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Indian Gooseberry (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Skin Heat and Itching'));

-- Black Raisin (U17)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Black Raisin'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Constipation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Black Raisin'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Black Raisin'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Anemia Tendency'));

-- Jujube (Unani) (U18)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Jujube (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Chronic Cough and Throat Irritation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Jujube (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Jujube (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Sleep Disturbance and Insomnia'));

-- Carrot (U19)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Carrot'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Carrot'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Anemia Tendency'));

-- Beetroot (U20)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Beetroot'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Beetroot'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Anemia Tendency'));

-- Celery Seed (U21)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Celery Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Joint Pain and Stiffness')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Celery Seed'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Digestive Weakness and Gas'));

-- Dill (Unani) (U22)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Dill (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Digestive Weakness and Gas')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Dill (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Pediatric Colic and Gas'));

-- Mint (Unani) (U23)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Mint (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Digestive Weakness and Gas')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Mint (Unani)'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Cold, Catarrh and Sneezing'));

-- Purslane (U24)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Purslane'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Obesity and Weight Gain')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Purslane'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Skin Heat and Itching')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Purslane'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Acne and Oily Skin'));

-- Spinach (U25)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Spinach'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Generalized Weakness and Fatigue')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Spinach'),
   (SELECT id FROM diseases WHERE name_en = 'Unani Anemia Tendency'));
