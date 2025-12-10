-- insert4_2_fix.sql
-- Fix for Siddha preparations that earlier used "INSERT INTO preparations (...)"

-- Common column list for all preparation inserts:
-- name_en, name_hi, name_mr,
-- classical_name, form_type, category,
-- preparation_steps, equipment_needed, duration, yield,
-- storage, shelf_life, dosage_json, timing, anupana, notes,
-- ayush_system, plant_id


-- P2. Keezhanelli Kashayam (for jaundice/liver)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Keezhanelli Kashayam',
  'कीझनेल्ली कषाय',
  'कीळानेली काढा',
  'Keezhanelli Kudineer',
  'decoction',
  'liver_and_jaundice_support',
  '1) Use fresh or dried Keezhanelli whole plant, make coarse pieces. 2) Boil in water and reduce as kashayam. 3) Filter and drink slightly warm.',
  'small_pot;strainer',
  '20–25 minutes',
  '60–100 ml',
  'Use fresh; do not store long.',
  'same_day',
  '{"adult":"20–40 ml once or twice daily under medical supervision","child":"only under specialist pediatric guidance"}',
  'before_food_or_as_directed',
  'plain_or_with_small_amount_of_honey_when_lukewarm_if_suitable',
  'Traditional Siddha decoction for jaundice and liver-related complaints along with strict diet.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Keezhanelli'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Keezhanelli Kashayam');


-- P3. Adathodai Kashayam (chronic cough)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Adathodai Kashayam',
  'अडथोड़ाई कषाय',
  'अडथोडी काढा',
  'Adathodai Kudineer',
  'decoction',
  'chronic_cough_and_asthma_support',
  '1) Take Adathodai leaves, wash and cut. 2) Boil with water until reduced to one-quarter. 3) Filter and serve warm.',
  'pot;strainer;cup',
  '20–25 minutes',
  '60–100 ml',
  'Use fresh, warm.',
  'same_day',
  '{"adult":"20–30 ml twice daily after food","child":"only under pediatric Siddha supervision"}',
  'after_food',
  'lukewarm_water_or_with_little_honey_if_suitable',
  'Common Siddha decoction for chronic cough, bronchitis and wheeze along with other measures.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Adathodai'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Adathodai Kashayam');


-- P4. Thuthuvalai Leaf Soup (respiratory)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Thuthuvalai Leaf Soup',
  'तुथुवलाई पत्ती सूप',
  'তुथुवलाई पानांचे सूप',
  'Thuthuvalai Rasam / Soup',
  'medicated_food',
  'respiratory_and_kapha_support',
  '1) Wash Thuthuvalai leaves and lightly crush. 2) Cook with pepper, garlic, cumin and tamarind water in rasam/soup style. 3) Serve warm with rice or as drink.',
  'cooking_pot;ladle',
  '20–30 minutes',
  '2–3 servings',
  'Best consumed same day.',
  '1_day',
  '{"adult":"one small bowl with meal","child":"small quantity depending on tolerance"}',
  'with_meal',
  'as_part_of_regular_food',
  'Popular Siddha-style home remedy rasam for chronic cough and wheeze.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Thuthuvalai'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Thuthuvalai Leaf Soup');


-- P5. Omavalli Leaf Extract (pediatric colic/cough)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Omavalli Leaf Extract',
  'ओमवल्ली पत्ती रस',
  'ओमावली पानांचा रस',
  'Omavalli Thylam/Leaf Juice (simplified oral)',
  'fresh_juice',
  'pediatric_colic_and_cough_support',
  '1) Take fresh Omavalli leaves, wash well. 2) Crush and express juice. 3) Use tiny quantity directly or mixed with honey as per classical practice under physician guidance.',
  'mortar_and_pestle;cloth_filter',
  '10–15 minutes',
  'Very small quantity',
  'Prepare fresh each time.',
  'same_day',
  '{"adult":"5–10 drops for digestion as advised","child":"few drops as per Siddha pediatric advice only"}',
  'as_directed',
  'plain_or_with_honey_if_suitable',
  'Frequently used leaf juice in Siddha households for colic, cough and indigestion in small doses.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Omavalli'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Omavalli Leaf Extract');


-- P6. Karisalai Lehya (liver and hair support)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Karisalai Lehya',
  'करिसालाई लेह्य',
  'करिसलाई लेह्य',
  'Karisalai Legiyam (simplified)',
  'lehya',
  'liver_and_hair_support',
  '1) Prepare decoction of Karisalai whole plant. 2) Add jaggery and ghee/gingelly oil and cook to thick lehya. 3) Store in airtight container.',
  'decoction_pot;thick_bottom_pan;spatula;jar',
  '1–2 hours',
  'Small jar of lehya',
  'Keep in clean airtight jar away from moisture.',
  '2–3 months',
  '{"adult":"5–10 g once daily under guidance","child":"only under physician advice"}',
  'morning_or_after_food',
  'lukewarm_water_or_milk_if_suitable',
  'Traditional Siddha-style legiyam targeting liver and hair support.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Karisalai'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Karisalai Lehya');


-- P7. Manathakkali Rice Porridge (ulcer support)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Manathakkali Rice Porridge',
  'मनतक्कलि चावल का कांजी',
  'मनतक्कळी भाताची कांजी',
  'Manathakkali Kanji',
  'medicated_food',
  'ulcer_and_gastric_support',
  '1) Lightly cook Manathakkali leaves with rice and excess water. 2) Prepare soft porridge. 3) Season very mildly with salt and little ghee.',
  'pot;ladle',
  '30–40 minutes',
  '2–3 servings',
  'Consume fresh.',
  '1_day',
  '{"adult":"one bowl once daily during active complaints","child":"small portion only if suitable"}',
  'morning_or_midday',
  'as_part_of_diet',
  'Siddha pathiyam food for gastritis and peptic ulcer tendency.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Manathakkali'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Manathakkali Rice Porridge');


-- P8. Mudakathan Thailam (external oil)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Mudakathan Thailam (external)',
  'मुदाक्कत्तान तेल (बाह्य)',
  'मुदाक्कत्तान तेल (बाह्य)',
  'Mudakathan Ennai (simplified)',
  'oil_preparation',
  'joint_and_stiffness_support_external',
  '1) Boil Mudakathan leaves in gingelly oil with suitable base. 2) Heat gently until water evaporates and only medicated oil remains. 3) Filter and store.',
  'thick_bottom_pan;cloth_filter;oil_container',
  '1–1.5 hours',
  '100–200 ml',
  'Store in cool dry place away from direct sun.',
  '3–6 months',
  '{"adult":"apply lukewarm oil on affected joints once or twice daily","child":"use under physician guidance only"}',
  'external_use_only',
  'none',
  'Classic Siddha style external oil for joint pain and stiffness.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Mudakathan'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Mudakathan Thailam (external)');


-- P9. Sirukurinjan Decoction (glycemic support)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Sirukurinjan Decoction',
  'सिरुकरिंजन काढ़ा',
  'सिरुकरिंजन काढा',
  'Sirukurinjan Kudineer',
  'decoction',
  'glycemic_support',
  '1) Take Sirukurinjan leaves, make coarse pieces. 2) Boil in water and reduce to one-quarter. 3) Filter and use in small doses along with medical therapy.',
  'pot;strainer;cup',
  '20–25 minutes',
  '60–100 ml',
  'Use fresh.',
  'same_day',
  '{"adult":"20–30 ml once or twice daily under medical supervision (with blood sugar monitoring)","child":"not generally used"}',
  'before_food_or_as_directed',
  'plain',
  'Siddha support herb for high blood sugar tendency; not a replacement for modern antidiabetic drugs.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Sirukurinjan'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Sirukurinjan Decoction');


-- P10. Nannari Sarbath (cooling drink)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Nannari Sarbath (Siddha)',
  'नन्नारी शरबत (सिद्ध)',
  'नन्नारी शरबत (सिद्ध)',
  'Nannari Syrup / Sarbath',
  'syrup',
  'summer_cooling_and_skin_support',
  '1) Clean and crush Nannari roots. 2) Boil in water to extract flavour. 3) Add sugar and make syrup. 4) Cool, bottle and serve diluted with cool water.',
  'pan;strainer;bottle',
  '45–60 minutes',
  '1–2 bottles',
  'Refrigerate after bottling.',
  '1–2 months',
  '{"adult":"20–30 ml diluted in water once daily in hot season","child":"small glass diluted"}',
  'midday_during_summer',
  'cold_water',
  'Popular cooling beverage in Siddha regions, considered supportive for heat and skin.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Nannari (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Nannari Sarbath (Siddha)');
