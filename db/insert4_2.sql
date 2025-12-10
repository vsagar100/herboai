-- P1. Nilavembu Kashayam (classical Siddha fever decoction)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Nilavembu Kashayam (Siddha)',
  'नीलवेम्बू कषाय (सिद्ध)',
  'नीलवेम्बू काढा (सिद्ध)',
  'Nilavembu Kudineer / Kashayam (simplified single-herb)',
  'decoction',
  'fever_and_viral_support',
  '1) Take coarse powder of Nilavembu herb. 2) Boil with 16 parts water and reduce to about one-quarter. 3) Filter and use lukewarm under professional guidance.',
  'decoction_pot;strainer;measuring_cup',
  '20–30 minutes',
  '60–120 ml',
  'Use freshly prepared; discard leftovers after a few hours.',
  'same_day',
  '{"adult":"30–60 ml once or twice daily in acute phase under Siddha physician supervision","child":"lower dose only as advised"}',
  'morning_and_evening',
  'lukewarm_water',
  'Key Siddha herbal decoction for fever and viral illness support; usually used as part of a multi-herb formula.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Nilavembu'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Nilavembu Kashayam (Siddha)');

-- P2. Keezhanelli Kashayam (for jaundice/liver)
INSERT INTO preparations (...)
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
INSERT INTO preparations (...)
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

-- P4. Thuthuvalai Soup (respiratory)
INSERT INTO preparations (...)
SELECT
  'Thuthuvalai Leaf Soup',
  'तुथुवलाई पत्ती सूप',
  'तुथुवलाई पानांचे सूप',
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
INSERT INTO preparations (...)
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
INSERT INTO preparations (...)
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

-- P7. Manathakkali Kanji (ulcer support porridge)
INSERT INTO preparations (...)
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

-- P8. Mudakathan Thailam (joint external oil)
INSERT INTO preparations (...)
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
INSERT INTO preparations (...)
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
INSERT INTO preparations (...)
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

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Musumusukkai Kashayam',
  'मुसुमुसुक्कै कषाय',
  'मुसुमुसुक्कै काढा',
  'Musumusukkai Kudineer',
  'decoction',
  'digestive_and_mild_fever_support',
  '1) Take coarse pieces of Musumusukkai whole plant or leaves. 2) Boil with about 8–10 times water and reduce to one-quarter. 3) Filter and drink warm under guidance.',
  'small_pot;strainer;measuring_cup',
  '20–25 minutes',
  '60–100 ml',
  'Use freshly prepared; do not store for long.',
  'same_day',
  '{"adult":"20–40 ml once or twice daily under Siddha supervision","child":"only under pediatric Siddha advice"}',
  'before_food_or_as_directed',
  'lukewarm_water',
  'Used traditionally in Siddha for digestive upset and mild fever as a simple kashayam.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Musumusukkai'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Musumusukkai Kashayam');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Vallarai Thuvaiyal',
  'वल्लरै चटनी (सिद्ध)',
  'वल्लाराय चटणी (सिद्ध)',
  'Vallarai Thuvaiyal',
  'medicated_food',
  'memory_and_nerve_support_mild',
  '1) Wash Vallarai leaves and lightly sauté with little ghee or oil. 2) Grind with coconut, mild spices and salt to chutney consistency. 3) Serve fresh with rice or idli.',
  'pan;grinder;spoon',
  '20–30 minutes',
  '2–3 servings',
  'Best consumed fresh; can refrigerate for short time.',
  '1_day',
  '{"adult":"2–3 tablespoons with one meal","child":"1–2 teaspoons mixed with rice if suitable"}',
  'with_meal',
  'as_part_of_regular_food',
  'Common Siddha-style dietary use of Vallarai for mild memory and nerve support as part of balanced food.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Vallarai (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Vallarai Thuvaiyal');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Kuppaimeni External Paste',
  'कुप्पाईमेनी बाह्य लेप',
  'कुप्पाईमेनी बाह्य लेप',
  'Kuppaimeni Thailam/Paste (simplified external)',
  'external_paste',
  'skin_eruption_support_external',
  '1) Wash fresh Kuppaimeni leaves thoroughly. 2) Grind with small amount of water or coconut oil to smooth paste. 3) Apply thin layer externally on advised area and wash off after some time as per physician guidance.',
  'mortar_and_pestle;spoon',
  '15–20 minutes',
  'Small bowl of paste',
  'Prepare fresh whenever needed.',
  'same_day',
  '{"adult":"external application only as advised","child":"use only under Siddha physician supervision"}',
  'external_use_only',
  'none',
  'Traditional Siddha external paste used in some skin conditions; not for open deep wounds or self-use without guidance.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Kuppaimeni'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Kuppaimeni External Paste');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Ponnanganni Keerai Poriyal',
  'पोन्नंगन्नी साग की सब्ज़ी',
  'पोन्नंगन्नी भाजी',
  'Ponnanganni Keerai Poriyal',
  'medicated_food',
  'eye_and_skin_support_food',
  '1) Clean and chop Ponnanganni leaves. 2) Lightly sauté with minimal oil, mustard, cumin, grated coconut and salt. 3) Serve as side dish with rice.',
  'pan;spatula',
  '20–25 minutes',
  '2–3 servings',
  'Consume fresh.',
  '1_day',
  '{"adult":"one small serving with lunch","child":"few spoonfuls mixed with rice if suitable"}',
  'with_lunch',
  'as_part_of_diet',
  'Leafy vegetable frequently used in Siddha diet for eye and skin support.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Ponnanganni'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Ponnanganni Keerai Poriyal');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Aruganpul Fresh Juice',
  'अरुगनपुल ताज़ा रस',
  'दुर्वा ताजा रस (सिद्ध)',
  'Aruganpul Saaru (fresh juice)',
  'fresh_juice',
  'pitta_and_bleeding_support_mild',
  '1) Wash Aruganpul (Bermuda grass) thoroughly to remove soil. 2) Grind with little clean water. 3) Filter through cloth to obtain green juice. 4) Use in small quantity immediately.',
  'mixer_or_mortar;cloth_filter',
  '15–20 minutes',
  '30–60 ml',
  'Use immediately after preparation.',
  'same_day',
  '{"adult":"10–20 ml diluted with water under guidance","child":"few ml only if advised"}',
  'morning_empty_stomach_or_as_directed',
  'water',
  'Used in Siddha/folk practice for minor bleeding and pitta disorders with strict hygiene.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Aruganpul'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Aruganpul Fresh Juice');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Nellikai Legiyam (Siddha)',
  'नेल्लिक्कई लेह्य (सिद्ध)',
  'नेल्लिकाय लेह्य (सिद्ध)',
  'Nellikai Legiyam',
  'lehya',
  'rasayana_and_liver_support',
  '1) Boil cut Nellikai fruits until soft and deseed. 2) Prepare pulp and mix with equal jaggery. 3) Cook slowly with small quantity of ghee/oil until thick lehya. 4) Cool and store in airtight jar.',
  'thick_bottom_pan;spatula;jar',
  '1–1.5 hours',
  'Small jar',
  'Keep in cool dry place.',
  '2–3 months',
  '{"adult":"5–10 g once daily","child":"small pea-sized quantity under guidance"}',
  'morning_or_evening',
  'lukewarm_water_or_milk_if_suitable',
  'Siddha-style legiyam preparation with Nellikai for general strength and liver support.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Nellikai (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Nellikai Legiyam (Siddha)');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Naval Seed Powder Mix',
  'नेवाळ बीज चूर्ण मिश्रण',
  'नेवाळ बी चूर्ण मिश्रण',
  'Naval Seed Choornam (simplified)',
  'powder',
  'glycemic_and_digestive_support',
  '1) Clean and dry Naval seeds. 2) Roast lightly on low flame. 3) Powder finely and store in airtight container.',
  'roasting_pan;grinder;airtight_jar',
  '40–60 minutes including drying',
  'Small jar of powder',
  'Store in dry airtight container.',
  '2–3 months',
  '{"adult":"half teaspoon once or twice daily under medical supervision","child":"generally not used"}',
  'before_food_or_as_directed',
  'lukewarm_water',
  'Siddha support powder often used as adjunct in high blood sugar tendency along with primary medical treatment.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Naval (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Naval Seed Powder Mix');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Vasambu Fumigation Powder (external)',
  'वसम्बु धूप चूर्ण (बाह्य)',
  'वसभु धुप चूर्ण (बाह्य)',
  'Vasambu Dhoopam (simplified)',
  'fumigation_powder',
  'respiratory_and_infant_care_support_external',
  '1) Dry Vasambu rhizome thoroughly and powder. 2) Use tiny pinch on charcoal or dhoop base for fumigation in room as per traditional practice. 3) Avoid direct inhalation in high concentration.',
  'roasting_pan;grinder;container',
  '40–60 minutes including drying',
  'Small bottle of powder',
  'Keep airtight and dry.',
  '6_months',
  '{"adult":"external fumigation only","child":"use only under expert guidance"}',
  'external_fumigation_only',
  'none',
  'Siddha traditional fumigation agent; not meant for direct oral use in this form.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Vasambu (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Vasambu Fumigation Powder (external)');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Chukku Kashayam (Siddha)',
  'सुक्का अदरक काढ़ा (सिद्ध)',
  'सुंठ काढा (सिद्ध)',
  'Chukku Milagu Thippili Kashayam (single-herb variant)',
  'decoction',
  'digestive_and_respiratory_support',
  '1) Take Chukku (dry ginger) coarse powder. 2) Boil with water and reduce to half. 3) Filter and drink warm.',
  'decoction_pot;strainer',
  '15–20 minutes',
  '60–100 ml',
  'Use fresh and warm.',
  'same_day',
  '{"adult":"20–30 ml after food once or twice daily","child":"only under pediatric advice"}',
  'after_food',
  'lukewarm_water',
  'Warming Siddha decoction used for indigestion, cold and cough tendencies.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Chukku (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Chukku Kashayam (Siddha)');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Milagu Rasam (Siddha)',
  'मिलगु रसम (सिद्ध)',
  'मिरी रसं (सिद्ध)',
  'Milagu Rasam',
  'medicated_food',
  'digestive_and_cold_support_food',
  '1) Powder Milagu (black pepper) with jeera and garlic. 2) Boil with tamarind water and salt to prepare rasam. 3) Consume hot as soup or with rice.',
  'pan;spoon',
  '20–25 minutes',
  '2–3 servings',
  'Consume fresh.',
  '1_day',
  '{"adult":"one small bowl with meal","child":"few spoons as tolerated"}',
  'with_meal',
  'as_part_of_diet',
  'Traditional pepper rasam in Siddha homes for cold, low appetite and digestion.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Milagu (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Milagu Rasam (Siddha)');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Thippili Kashayam (Siddha)',
  'थिप्पिलि काढ़ा (सिद्ध)',
  'थिप्पली काढा (सिद्ध)',
  'Thippili Kudineer',
  'decoction',
  'respiratory_and_kapha_support',
  '1) Take Thippili fruit spikes broken into pieces. 2) Boil in water and reduce to half or quarter. 3) Filter and drink warm.',
  'pot;strainer',
  '15–20 minutes',
  '60–80 ml',
  'Use fresh.',
  'same_day',
  '{"adult":"15–30 ml once or twice daily after food","child":"only under specialist advice"}',
  'after_food',
  'lukewarm_water',
  'Component of classic Trikatu support; used in chronic cough and cold in Siddha.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Thippili (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Thippili Kashayam (Siddha)');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Elumichai Herbal Lemon Drink',
  'एलुमिचाई हर्बल नींबू पेय',
  'एलुमिचाई हर्बल लिंबूपाणी',
  'Elumichai Panagam (simple)',
  'herbal_water',
  'digestive_and_vitamin_c_support',
  '1) Squeeze fresh Elumichai (lemon) into water. 2) Add pinch of ginger, pepper and little jaggery or salt as suitable. 3) Stir well and consume fresh.',
  'glass;spoon',
  '5–10 minutes',
  '1 glass',
  'Use immediately.',
  'same_day',
  '{"adult":"one glass with or after meals","child":"small quantity diluted"}',
  'with_food_or_after_food',
  'as_is',
  'Simple Siddha-style lemon drink for appetite and vitamin C support.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Elumichai (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Elumichai Herbal Lemon Drink');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Seenthil Kodi Kashayam',
  'सींथिल कोडी काढ़ा (सिद्ध)',
  'सींथिल कोडी काढा (सिद्ध)',
  'Seenthil Kudineer',
  'decoction',
  'fever_and_immune_support_mild',
  '1) Use Seenthil Kodi stem pieces. 2) Boil with water and reduce to one-quarter. 3) Filter and drink warm under supervision.',
  'decoction_pot;strainer',
  '20–25 minutes',
  '60–100 ml',
  'Use fresh.',
  'same_day',
  '{"adult":"20–40 ml once or twice daily as advised","child":"not generally used without physician guidance"}',
  'morning_or_evening',
  'lukewarm_water',
  'Guduchi-based Siddha decoction for fever and immune support.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Seenthil Kodi (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Seenthil Kodi Kashayam');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Perandai Thogayal',
  'पेरंडै ठोगयाल चटनी',
  'पेरंडई ठोगयल चटणी',
  'Perandai Thogayal',
  'medicated_food',
  'bone_and_joint_support_food',
  '1) Clean Perandai stem segments and remove outer fibers if needed. 2) Blanch briefly and sauté with lentils and spices. 3) Grind to thick thogayal and use with rice.',
  'pan;grinder',
  '30–40 minutes',
  '2–3 servings',
  'Consume fresh; refrigerate short term only.',
  '1_day',
  '{"adult":"2–3 tablespoons with meal once weekly or as advised","child":"small amount mixed with rice if ok"}',
  'with_lunch',
  'as_part_of_diet',
  'Perandai-based chutney used in Siddha food traditions for bone and joint support.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Perandai'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Perandai Thogayal');

INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Karunjeeragam Kashayam',
  'करुंजीरगम काढ़ा (सिद्ध)',
  'करुंजीरगम काढा (सिद्ध)',
  'Karunjeeragam Kudineer',
  'decoction',
  'digestive_and_metabolic_support',
  '1) Slightly crush Karunjeeragam seeds. 2) Boil in water and reduce to about half. 3) Filter and take in small quantity.',
  'small_pot;strainer',
  '15–20 minutes',
  '50–80 ml',
  'Use fresh.',
  'same_day',
  '{"adult":"10–20 ml once or twice daily under supervision","child":"generally avoided"}',
  'after_food',
  'lukewarm_water',
  'Siddha warming decoction used in small doses for digestion and metabolic support.',
  'siddha',
  p.id
FROM plants p
WHERE p.common_name_en = 'Karunjeeragam (Siddha)'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Karunjeeragam Kashayam');

-- Helper: Siddha mapping uses name_en and category = 'siddha_%'

-- S1 Nilavembu
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Nilavembu'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Viral Fever with Body Pain'));

-- S2 Keezhanelli
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Keezhanelli'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Jaundice and Liver Heat'));

-- S3 Adathodai
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Adathodai'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Chronic Bronchitis and Wheeze'));

-- S4 Thuthuvalai
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Thuthuvalai'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Chronic Bronchitis and Wheeze'));

-- S5 Omavalli
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Omavalli'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Chronic Bronchitis and Wheeze')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Omavalli'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Peptic Ulcer and Gastric Irritation')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Omavalli'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Pediatric Colic and Gas'));

-- S6 Musumusukkai
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Musumusukkai'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Viral Fever with Body Pain')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Musumusukkai'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Peptic Ulcer and Gastric Irritation'));

-- S7 Vallarai (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Vallarai (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Nervous Weakness and Anxiety'));

-- S8 Karisalai
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Karisalai'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Jaundice and Liver Heat')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Karisalai'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Skin Eruptions with Itching'));

-- S9 Kuppaimeni
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Kuppaimeni'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Skin Eruptions with Itching')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Kuppaimeni'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Chronic Bronchitis and Wheeze'));

-- S10 Manathakkali
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Manathakkali'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Peptic Ulcer and Gastric Irritation'));

-- S11 Ponnanganni
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Ponnanganni'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Skin Eruptions with Itching')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Ponnanganni'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Anemia Tendency'));

-- S12 Aruganpul
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Aruganpul'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Jaundice and Liver Heat'));

-- S13 Mudakathan
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Mudakathan'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Joint Pain and Arthritic Stiffness'));

-- S14 Sirukurinjan
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Sirukurinjan'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Diabetes Mellitus (Neerizhivu)')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Sirukurinjan'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Obesity and Metabolic Syndrome'));

-- S15 Nellikai (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Nellikai (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Jaundice and Liver Heat')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Nellikai (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Diabetes Mellitus (Neerizhivu)')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Nellikai (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Nervous Weakness and Anxiety'));

-- S16 Naval (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Naval (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Diabetes Mellitus (Neerizhivu)'));

-- S17 Nannari (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Nannari (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Jaundice and Liver Heat')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Nannari (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Skin Eruptions with Itching'));

-- S18 Vasambu (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Vasambu (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Pediatric Colic and Gas')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Vasambu (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Chronic Bronchitis and Wheeze'));

-- S19 Chukku (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Chukku (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Chronic Bronchitis and Wheeze')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Chukku (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Peptic Ulcer and Gastric Irritation'));

-- S20 Milagu (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Milagu (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Chronic Bronchitis and Wheeze')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Milagu (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Obesity and Metabolic Syndrome'));

-- S21 Thippili (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Thippili (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Chronic Bronchitis and Wheeze'));

-- S22 Elumichai (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Elumichai (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Peptic Ulcer and Gastric Irritation'));

-- S23 Seenthil Kodi (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Seenthil Kodi (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Viral Fever with Body Pain')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Seenthil Kodi (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Jaundice and Liver Heat'));

-- S24 Perandai
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Perandai'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Joint Pain and Arthritic Stiffness'));

-- S25 Karunjeeragam (Siddha)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id) VALUES
  ((SELECT id FROM plants   WHERE common_name_en = 'Karunjeeragam (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Diabetes Mellitus (Neerizhivu)')),
  ((SELECT id FROM plants   WHERE common_name_en = 'Karunjeeragam (Siddha)'),
   (SELECT id FROM diseases WHERE name_en = 'Siddha Obesity and Metabolic Syndrome'));

