-- =========================================================
-- PREPARATIONS FOR PLANTS 26–69
-- =========================================================

------------------------------------------------------------
-- 26. Kantakari – Kantakari Cough Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Kantakari Cough Decoction',
  'कंटकारी खांसी काढ़ा',
  'कंटकारी खोकला काढा',
  'Kantakari Kwatha',
  'decoction',
  'respiratory_support',
  '1) Take dried Kantakari whole plant (especially aerial parts) as coarse powder. 2) Boil in water and reduce to approx. one-quarter. 3) Filter and serve warm in small supervised doses.',
  'decoction_pot;strainer;measuring_cup',
  '20–30 minutes.',
  '60–100 ml per batch.',
  'Use fresh and warm; discard leftover.',
  'Same-day use only.',
  '{"adult":"15–30 ml once or twice daily under supervision","child":"only under pediatric Ayurvedic guidance"}',
  'after_food_or_as_directed',
  'plain',
  'Kantakari is part of Dasamoola and used for cough/asthma patterns; classically combined with other herbs.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Kantakari'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Kantakari Cough Decoction');

------------------------------------------------------------
-- 27. Brihati – Brihati Cough Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Brihati Cough Decoction',
  'बृहतखीरा खांसी काढ़ा',
  'भुई वांगे खोकला काढा',
  'Brihati Kwatha',
  'decoction',
  'respiratory_support',
  '1) Take dried Brihati whole plant (without large thorns). 2) Boil with water and reduce as per kwatha rule. 3) Filter and give warm.',
  'pot;strainer',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily with supervision","child":"only if prescribed"}',
  'after_food',
  'plain',
  'Brihati is also a Dasamoola member, used in cough/asthma; usually combined with other roots.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Brihati'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Brihati Cough Decoction');

------------------------------------------------------------
-- 28. Asthisamharaka – Bone Support Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Asthisamharaka Bone Decoction',
  'अस्थिसंहरक अस्थि काढ़ा',
  'अस्थिसंहरक हाड काढा',
  'Asthisamharaka Kwatha',
  'decoction',
  'bone_and_fracture_support',
  '1) Use dried stem pieces of Asthisamharaka (Cissus quadrangularis). 2) Boil with water until reduced. 3) Filter and use warm in small supervised doses.',
  'decoction_pot;strainer;knife',
  '20–30 minutes.',
  '60–100 ml per batch.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily along with orthopedic care","child":"only under pediatric supervision"}',
  'after_meals',
  'plain',
  'Used traditionally as adjunct for fractures and bone weakness; not a substitute for proper immobilization and orthopedic management.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Asthisamharaka'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Asthisamharaka Bone Decoction');

------------------------------------------------------------
-- 29. Vijayasar – Anti-diabetic Wood Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Vijayasar Wood Decoction',
  'विजयसार लकड़ी काढ़ा',
  'विजयसार लाकूड काढा',
  'Vijaysar Kwatha',
  'decoction',
  'diabetes_support',
  '1) Take heartwood chips of Vijayasar. 2) Soak briefly then boil in water until reduced and colored. 3) Filter and drink in supervised doses.',
  'pot;strainer',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"20–40 ml once or twice daily along with diabetic management","child":"use only if prescribed"}',
  'before_food_or_as_directed',
  'plain',
  'Popular adjunct in type 2 diabetes; glucose monitoring and modern therapy remain primary.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Vijayasar'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Vijayasar Wood Decoction');

------------------------------------------------------------
-- 30. Manjishta – Manjishta Blood Purifier Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Manjishta Blood Decoction',
  'मंजिष्ठा रक्त शोधक काढ़ा',
  'मंजिष्ठा रक्तशोधक काढा',
  'Manjishta Kwatha',
  'decoction',
  'blood_and_skin_support',
  '1) Use dried Manjishta roots cut into small pieces. 2) Boil with water and reduce as per kwatha. 3) Filter and use.',
  'pot;strainer;knife',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"20–40 ml once or twice daily as advised","child":"only under specialist guidance"}',
  'after_food',
  'plain',
  'Classical herb for Rakta and skin support; liver and kidney status must be considered.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Manjishta'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Manjishta Blood Decoction');

------------------------------------------------------------
-- 31. Golden Shower Tree – Flower Infusion
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Golden Shower Flower Infusion',
  'अमलतास पुष्प फांटा',
  'बहावा फुलांचा फांटा',
  'Aragvadha Pushpa Phanta',
  'herbal_tea',
  'mild_laxative_support',
  '1) Use dried flowers of Golden Shower Tree. 2) Pour hot water over a small quantity and cover for 5–10 minutes. 3) Strain and use in small doses.',
  'cup;strainer',
  '10–15 minutes.',
  'One cup per preparation.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"20–40 ml as mild laxative support when advised","child":"only under pediatric supervision"}',
  'bedtime_or_as_directed',
  'as_is',
  'Golden Shower Tree is used for mild laxative and skin support; pods are stronger and used cautiously.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Golden Shower Tree'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Golden Shower Flower Infusion');

------------------------------------------------------------
-- 32. Kutaja – Kutaja Bark Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Kutaja Bark Decoction',
  'कुटज की छाल का काढ़ा',
  'कुडज सालीचा काढा',
  'Kutaja Kwatha',
  'decoction',
  'antidiarrheal_support',
  '1) Take dried Kutaja bark. 2) Prepare coarse pieces and boil in water to reduce. 3) Filter and use in small doses.',
  'pot;strainer;knife',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"20–40 ml once or twice daily in diarrhea/IBS pattern as advised","child":"only under pediatric care"}',
  'as_directed',
  'plain',
  'Kutaja is classical antidiarrheal herb; dehydration and infection still require modern medical care.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Kutaja'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Kutaja Bark Decoction');

------------------------------------------------------------
-- 33. Kokilaksha – Kokilaksha Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Kokilaksha Decoction',
  'कौकिलाक्ष काढ़ा',
  'कोकिलाक्ष काढा',
  'Kokilaksha Kwatha',
  'decoction',
  'urinary_and_joint_support',
  '1) Use dried aerial parts of Kokilaksha as coarse powder. 2) Boil with water and reduce. 3) Filter and administer warm.',
  'pot;strainer',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily under guidance","child":"use only if prescribed"}',
  'after_food',
  'plain',
  'Used in classical texts for urinary and joint disorders; kidney function and uric acid should be monitored.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Kokilaksha'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Kokilaksha Decoction');

------------------------------------------------------------
-- 34. Noni – Noni Fruit Tonic
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Noni Fruit Tonic',
  'नोनी फल टॉनिक',
  'नोनी फळ टॉनिक',
  'Noni Phala Ras (folk)',
  'juice',
  'immune_and_vitality_support',
  '1) Take fully ripe Noni fruits. 2) Wash, slice and press to extract juice, or ferment-controlled juice as per pharmacopeia. 3) Dilute with water before intake.',
  'knife;press_or_juicer;strainer',
  '20–30 minutes (non-fermented).',
  'Several small servings.',
  'Refrigerate and use within a few days if fresh; fermented products follow label.',
  'Few days (fresh juice).',
  '{"adult":"10–30 ml diluted once or twice daily as guided","child":"small amount only if suitable"}',
  'morning_or_as_directed',
  'diluted_with_water',
  'Noni has become popular nutraceutical; quality control and dose individualization are important.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Noni'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Noni Fruit Tonic');

------------------------------------------------------------
-- 35. Apamarga – Apamarga Kshara Preparation (simplified)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Apamarga Kshara Base',
  'अपामार्ग क्षार आधार',
  'अपामार्ग क्षार बेस',
  'Apamarga Kshara (simplified)',
  'alkaline_salt',
  'digestive_and_fistula_support',
  '1) Burn dried whole plant of Apamarga to ash as per classical kshara method. 2) Extract water-soluble portion, filter and evaporate to obtain kshara. 3) Dry and store airtight.',
  'earthen_pan;filter_cloth;evaporation_pan',
  'Several hours including burning and evaporation.',
  'Depends on starting biomass.',
  'Store in airtight container protected from moisture.',
  'Many months if dry and airtight.',
  '{"adult":"dose in tens to few hundred milligrams as part of formulations under strict supervision","child":"not generally used"}',
  'as_directed',
  'with_suitable_vehicle_like_buttermilk_or_water',
  'Apamarga kshara is potent and used in ksharasutra and digestive disorders; must be prepared and dosed only by experts.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Apamarga'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Apamarga Kshara Base');

------------------------------------------------------------
-- 36. Red Sandalwood – Rakta Cooling Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Red Sandalwood Cooling Decoction',
  'रक्तचंदन शीत काढ़ा',
  'रक्तचंदन थंड काढा',
  'Raktachandana Kwatha',
  'decoction',
  'cooling_and_rakta_support',
  '1) Use chips or coarse powder of Red Sandalwood. 2) Boil in water until color and extract develop. 3) Filter and use in small quantities.',
  'pot;strainer',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily as supportive drink","child":"small quantity only if suitable"}',
  'between_meals_or_as_directed',
  'as_is',
  'Used classically for Pitta-Rakta conditions such as burning, rashes, and epistaxis; internal use should be supervised.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Red Sandalwood'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Red Sandalwood Cooling Decoction');

------------------------------------------------------------
-- 37. Patha – Patha Digestive Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Patha Digestive Decoction',
  'पाठा पाचन काढ़ा',
  'पाठा पचन काढा',
  'Patha Kwatha',
  'decoction',
  'diarrhea_and_digestive_support',
  '1) Take dried Patha roots. 2) Cut into small pieces and boil with water. 3) Reduce to kwatha volume and filter.',
  'pot;strainer;knife',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily as per advice","child":"only if prescribed"}',
  'after_food',
  'plain',
  'Patha is used in Atisara, Grahani and certain fevers; usually combined with herbs like Kutaja/Mustaka.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Patha'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Patha Digestive Decoction');

------------------------------------------------------------
-- 38. Shati – Shati Digestive Powder
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Shati Digestive Powder',
  'शाठी पाचन चूर्ण',
  'शाठी पचन चूर्ण',
  'Shati Churna',
  'powder',
  'digestive_and_antiemetic_support',
  '1) Clean and dry Shati rhizomes. 2) Powder to fine churna. 3) Store in airtight container.',
  'grinder;sieve;airtight_jar',
  '20–30 minutes.',
  'Close to rhizome weight.',
  'Store cool and dry.',
  'Few months.',
  '{"adult":"500–1000 mg once or twice daily","child":"only under guidance"}',
  'after_food',
  'with_honey_or_lukewarm_water',
  'Shati is aromatic rhizome used for nausea and digestive issues; dose adjusted to Pitta status.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Shati'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Shati Digestive Powder');

------------------------------------------------------------
-- 39. Daruharidra – Daruharidra Eye/Gut Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Daruharidra Decoction',
  'दारुहरिद्रा काढ़ा',
  'दारुहरिद्रा काढा',
  'Daruharidra Kwatha',
  'decoction',
  'eye_and_gut_support',
  '1) Use stem bark pieces of Daruharidra. 2) Boil with water to kwatha strength. 3) Filter; internal use is in small doses, and cooled decoction sometimes used externally near eyes as per classical guidance.',
  'pot;strainer',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily internally under supervision","child":"only if prescribed"}',
  'after_food',
  'plain',
  'Berberine-rich bark used for infections and eye/gut issues; modern drug interactions must be considered.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Daruharidra'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Daruharidra Decoction');

------------------------------------------------------------
-- 40. Chirayata – Chirayata Bitter Tea
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Chirayata Bitter Tea',
  'चिरायता कड़वी चाय',
  'चिरायता कडू चहा',
  'Kirata Tikta Phanta',
  'herbal_tea',
  'fever_and_liver_support',
  '1) Take small quantity of dried Chirayata herb. 2) Steep in hot water for 10–15 minutes. 3) Strain and drink slowly.',
  'cup;strainer',
  '10–15 minutes.',
  'One cup.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"20–40 ml once or twice daily due to strong bitterness","child":"only under strict supervision"}',
  'before_food_or_as_directed',
  'plain',
  'Very bitter hepatic and antipyretic herb; excessive usage is avoided.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Chirayata'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Chirayata Bitter Tea');

------------------------------------------------------------
-- 41. Galangal – Galangal Digestive Tea
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Galangal Digestive Tea',
  'कुलंजन पाचन चाय',
  'कुलंजन पचन चहा',
  'Kulanjan Phanta',
  'herbal_tea',
  'digestive_and_respiratory_support',
  '1) Slice dried Galangal rhizome. 2) Boil or steep in hot water for several minutes. 3) Strain and sip warm.',
  'cup_or_pot;strainer',
  '10–15 minutes.',
  'One cup.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"one cup once or twice daily after food","child":"small amount only if suitable"}',
  'after_meals',
  'as_is',
  'Warming rhizome used in cough, indigestion and voice issues; Pitta aggravation needs monitoring.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Galangal'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Galangal Digestive Tea');

------------------------------------------------------------
-- 42. Nagarmotha (Scariosus) – Nagarmotha Digestive Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Nagarmotha Digestive Decoction',
  'नागरमोथा पाचन काढ़ा',
  'नागरमोथा पचन काढा',
  'Mustaka/Nagarmotha Kwatha',
  'decoction',
  'diarrhea_and_fever_support',
  '1) Use dried tubers of Nagarmotha. 2) Crush and boil in water till reduced. 3) Filter and take warm.',
  'pot;crusher;strainer',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily under guidance","child":"only under pediatric supervision"}',
  'after_meals',
  'plain',
  'Very similar action to Mustaka; used in diarrhea, fever and digestive complaints.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Nagarmotha (Scariosus)'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Nagarmotha Digestive Decoction');

------------------------------------------------------------
-- 43. Talispatra – Talispatra Cough Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Talispatra Cough Decoction',
  'तालिसपत्र खांसी काढ़ा',
  'तालीसपत्र खोकला काढा',
  'Talispatra Kwatha',
  'decoction',
  'respiratory_support',
  '1) Use dried leaves of Talispatra. 2) Boil in water and reduce. 3) Filter and consume lukewarm.',
  'pot;strainer',
  '15–20 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily as supportive cough remedy","child":"only if prescribed"}',
  'after_food',
  'plain',
  'Aromatic leaf used in cough, cold and asthma formulations.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Talispatra'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Talispatra Cough Decoction');

------------------------------------------------------------
-- 44. Pushkarmoola – Pushkarmoola Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Pushkarmoola Decoction',
  'पुष्करमूल काढ़ा',
  'पुष्करमुळ काढा',
  'Pushkaramoola Kwatha',
  'decoction',
  'respiratory_and_cardiac_support',
  '1) Take dried Pushkarmoola roots. 2) Prepare coarse pieces and boil with water. 3) Filter and use warm.',
  'pot;strainer;knife',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily under supervision","child":"only under pediatric specialist"}',
  'after_food',
  'plain',
  'Classical herb for breathlessness and certain cardiac complaints; always used with close monitoring.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Pushkarmoola'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Pushkarmoola Decoction');

------------------------------------------------------------
-- 45. Black Nightshade – Leaf Decoction (supervised)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Black Nightshade Leaf Decoction',
  'माकोय पत्ती काढ़ा',
  'भुई भोपळा पानांचा काढा',
  'Kakamachi Kwatha',
  'decoction',
  'liver_and_skin_support',
  '1) Use correctly identified Black Nightshade leaves and tender aerial parts. 2) Boil in water and reduce moderately. 3) Filter and administer in small supervised doses only.',
  'pot;strainer',
  '15–20 minutes.',
  '60–80 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"10–20 ml once or twice daily under expert guidance","child":"generally avoided unless prescribed"}',
  'after_food',
  'plain',
  'Solanum species may be toxic if misidentified or overdosed; this decoction must be supervised.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Black Nightshade'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Black Nightshade Leaf Decoction');

------------------------------------------------------------
-- 46. Vidarikand – Vidarikand Milk Tonic
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Vidarikand Milk Tonic',
  'विदारीकंद दूध टॉनिक',
  'विदारीकंद दूध टॉनिक',
  'Vidari Kanda Ksheerapaka',
  'medicated_milk',
  'rasayana_and_reproductive_support',
  '1) Use dried Vidarikand tuber powder. 2) Boil with milk and water as ksheerapaka. 3) Reduce and serve warm.',
  'pan;stirrer',
  '20–30 minutes.',
  'One or two servings.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"50–100 ml once or twice daily as advised","child":"only under specialist supervision"}',
  'morning_or_evening',
  'as_is',
  'Vidarikand is sweet, cooling Rasayana; useful in debility and reproductive issues when indicated.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Vidarikand'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Vidarikand Milk Tonic');

------------------------------------------------------------
-- 47. Karkatashringi – Karkatashringi Cough Powder
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Karkatashringi Cough Powder',
  'कर्कटश्रृंगी खांसी चूर्ण',
  'कर्कटश्रृंगी खोकला चूर्ण',
  'Karkatashringi Churna',
  'powder',
  'cough_support',
  '1) Clean dried Karkatashringi galls. 2) Powder to fine churna. 3) Store airtight.',
  'grinder;sieve;airtight_jar',
  '20–30 minutes.',
  'Close to gall weight.',
  'Store cool and dry.',
  'Few months.',
  '{"adult":"500–1000 mg with honey 2–3 times daily as advised","child":"smaller doses only under supervision"}',
  'after_food',
  'with_honey',
  'Classical cough remedy often combined with Vasa, Pippali, etc.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Karkatashringi'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Karkatashringi Cough Powder');

------------------------------------------------------------
-- 48. Kalijiri – Kalijiri Metabolic Powder
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Kalijiri Metabolic Powder',
  'कलिजीरी चूर्ण',
  'कलिजीरी चूर्ण',
  'Kalajiri Churna',
  'powder',
  'metabolic_and_digestive_support',
  '1) Clean Kalijiri seeds. 2) Lightly roast if desired and grind to powder. 3) Store in airtight jar.',
  'pan;grinder;airtight_jar',
  '15–20 minutes.',
  'Close to seed weight.',
  'Store cool and dry.',
  '1–2 months.',
  '{"adult":"1–3 g daily in divided doses as guided","child":"use only under guidance"}',
  'before_meals_or_as_directed',
  'with_lukewarm_water',
  'Used in some classical/regional anti-obesity and metabolic formulations.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Kalijiri'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Kalijiri Metabolic Powder');

------------------------------------------------------------
-- 49. Indian Sarsaparilla – Sariva Sharbat
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Sariva Sharbat',
  'सारिवा शरबत',
  'सारिवा शरबत',
  'Sariva Panaka',
  'syrup',
  'blood_and_cooling_support',
  '1) Soak Sariva root chips in water, boil gently and reduce. 2) Add sugar to form light syrup. 3) Strain and bottle; dilute in water before drinking.',
  'pot;strainer;bottles;spoon',
  '40–60 minutes.',
  'Several servings.',
  'Refrigerate after cooling.',
  'Few weeks if stored hygienically.',
  '{"adult":"10–20 ml syrup diluted in water once or twice daily","child":"5–10 ml diluted if suitable"}',
  'in_hot_season',
  'diluted_in_cool_water',
  'Sariva is classic Rakta-pitta cooling herb; sugar load considered in metabolic disorders.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Indian Sarsaparilla'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Sariva Sharbat');

------------------------------------------------------------
-- 50. Vriddhadaru – Vriddhadaru Tonic Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Vriddhadaru Tonic Decoction',
  'वृद्धदारु टॉनिक काढ़ा',
  'वृद्धदारू टॉनिक काढा',
  'Vriddhadaru Kwatha',
  'decoction',
  'reproductive_and_vata_support',
  '1) Take dried Vriddhadaru root bark. 2) Boil with water as kwatha. 3) Filter and use warm.',
  'pot;strainer;knife',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily as advised","child":"only under specialist guidance"}',
  'morning_and/or_evening',
  'with_milk_or_as_directed',
  'Referenced as supportive herb in male reproductive and Vata conditions.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Vriddhadaru'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Vriddhadaru Tonic Decoction');

------------------------------------------------------------
-- 51. Pashanbhed – Stone Support Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Pashanbhed Stone Decoction',
  'पाषाणभेद किडनी स्टोन काढ़ा',
  'पाषाणभेद मूत्रमार्ग काढा',
  'Pashanbheda Kwatha',
  'decoction',
  'urinary_stone_support',
  '1) Use rhizomes of Pashanbhed cut into pieces. 2) Boil in water and reduce. 3) Filter and use warm in small doses.',
  'pot;strainer;knife',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily under urology and Ayurvedic guidance","child":"only under pediatric supervision"}',
  'after_food',
  'plain',
  'Classical supportive herb in renal calculi; not a replacement for surgical/urological interventions when needed.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Pashanbhed'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Pashanbhed Stone Decoction');

------------------------------------------------------------
-- 52. Mango – Mango Leaf/Home Decoctions etc. (use fruit drink)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Ripe Mango Digestive Drink',
  'पका आम पाचन पेय',
  'पिकलेल्या आंब्याचे पचन पेय',
  'Amra Phala Rasa (dietary)',
  'medicated_food',
  'digestive_and_nourishing_support',
  '1) Take ripe Mango pulp, remove fibers and seeds. 2) Blend with small amount of water or buttermilk as per constitution. 3) Serve fresh in moderate quantity.',
  'knife;blender;strainer_optional',
  '10–15 minutes.',
  '2–3 servings.',
  'Use fresh; short refrigeration only.',
  'Same-day.',
  '{"adult":"one glass once daily in season if suitable","child":"small quantity adjusted to age"}',
  'with_or_between_meals',
  'as_is_or_with_diluted_buttermilk',
  'Ripe Mango is heavy but nourishing; quantity adjusted per Agni and Prakriti.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Mango'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Ripe Mango Digestive Drink');

------------------------------------------------------------
-- 53. Bakuchi – Bakuchi External Oil (for vitiligo support)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Bakuchi External Oil',
  'बावची बाह्य तेल',
  'बावची बाह्य तेल',
  'Bakuchi Taila (simplified)',
  'medicated_oil_external',
  'vitiligo_and_skin_support_external',
  '1) Soak Bakuchi seeds in suitable medium, then boil with base oil (like sesame) as per classical taila paka. 2) Filter and store. 3) Apply thinly on depigmented patches as advised and avoid sun overexposure.',
  'oil_pan;filter_cloth;bottle',
  '1–2 hours including boiling and cooling.',
  'Depends on oil volume.',
  'Store in cool, dark place.',
  'Few months.',
  '{"adult":"external application in tiny amount as prescribed","child":"only under specialist dermatology/Ayurveda care"}',
  'external_use_only',
  'none',
  'Bakuchi is photosensitizing; improper use can cause burns—strict specialist supervision is required.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Bakuchi'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Bakuchi External Oil');

------------------------------------------------------------
-- 54. Sweet Flag – Vacha Nasya Powder (very cautious)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Vacha Fine Powder',
  'वचा बारीक चूर्ण',
  'वचा बारीक चूर्ण',
  'Vacha Churna',
  'powder',
  'speech_and_neuro_support_small_dose',
  '1) Clean and dry Sweet Flag rhizomes. 2) Powder very finely and sieve. 3) Store airtight. 4) Use only in very small doses as per expert advice.',
  'grinder;fine_sieve;airtight_jar',
  '20–30 minutes.',
  'Close to rhizome weight.',
  'Store cool and dry.',
  'Few months.',
  '{"adult":"tiny pinch (50–125 mg) internally or as per nasya/prayoga by physician","child":"only under pediatric specialist supervision"}',
  'as_directed',
  'with_honey_or_ghee',
  'Vacha is potent, with CNS effects; excessive use or wrong species may be toxic.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Sweet Flag'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Vacha Fine Powder');

------------------------------------------------------------
-- 55. Betel Leaf – Betel Digestive Mouth Pack
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Betel Digestive Mouth Pack',
  'पान पाचन पूड़',
  'पान पचन पान',
  'Tambula (non-tobacco)',
  'medicated_food',
  'digestive_and_freshness_support',
  '1) Take tender Betel leaf, wash and dry. 2) Add small amount of fennel, cardamom, clove, coconut etc., without tobacco or lime. 3) Fold and chew after meals if suitable.',
  'knife;plate',
  '5–10 minutes.',
  '1–2 mouthful packs.',
  'Best used fresh.',
  'Same-day.',
  '{"adult":"one mild pack after heavy meal occasionally","child":"generally avoided"}',
  'after_meals',
  'chewed_and_spat_or_swallowed_as_per_custom',
  'Traditional non-tobacco betel chewing aids digestion but can still irritate mucosa if overused.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Betel Leaf'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Betel Digestive Mouth Pack');

------------------------------------------------------------
-- 56. Indian Bay Leaf – Tejpatra Digestive Tea
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Tejpatra Herbal Digestive Tea',
  'तेजपत्ता हर्बल पाचन चाय',
  'तामालपत्र हर्बल पचन चहा',
  'Tamala Patra Phanta',
  'herbal_tea',
  'digestive_support',
  '1) Tear Indian Bay Leaf into pieces. 2) Steep in hot water for 5–10 minutes. 3) Strain and sip warm after meals.',
  'cup;strainer',
  '10–15 minutes.',
  'One cup.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"one cup after heavy meal","child":"not routine; small quantity only if suitable"}',
  'after_meals',
  'as_is',
  'Aromatic tea useful for gas and heaviness.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Indian Bay Leaf'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Tejpatra Herbal Digestive Tea');

------------------------------------------------------------
-- 57. Hibiscus – Hibiscus Flower Hair Rinse
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Hibiscus Hair Rinse',
  'गुड़हल केश धुलाई काढ़ा',
  'जास्वंद केस धुण्याचा काढा',
  'Japa Pushpa Kashaya (external)',
  'decoction',
  'hair_support_external',
  '1) Boil Hibiscus flowers and leaves in water until lightly reduced and slimy. 2) Cool to lukewarm. 3) Use as hair/scalp rinse before or after gentle shampoo.',
  'pot;strainer;bowl',
  '20–30 minutes.',
  'Sufficient for one or two rinses.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"external hair rinse 1–2 times/week","child":"external use if suitable"}',
  'external_use_only',
  'none',
  'Hibiscus rinse is popular for hair fall/dandruff support; part of broader hair-care regimen.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Hibiscus'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Hibiscus Hair Rinse');

------------------------------------------------------------
-- 58. Mexican Poppy – External-only Cautionary Paste
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Mexican Poppy External Paste',
  'सत्यानाशी बाह्य लेप',
  'सत्यानाशी बाह्य लेप',
  'Satyanshi Lepa (folk)',
  'paste',
  'skin_support_external_only',
  '1) Prepare paste from leaves/latex of Mexican Poppy ONLY if explicitly indicated and under expert guidance. 2) Apply carefully on localized warts or lesions. 3) Remove within advised time and wash thoroughly.',
  'mortar_and_pestle;gloves;bowl',
  '10–15 minutes to prepare.',
  'Small quantity.',
  'Use immediately; do not store.',
  'Single-use or same-day.',
  '{"adult":"external spot application only under strict supervision","child":"generally avoided"}',
  'external_use_only',
  'none',
  'Plant is potentially toxic; internal use is avoided and external use must be very cautious.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Mexican Poppy'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Mexican Poppy External Paste');

------------------------------------------------------------
-- 59. Arka – Arka External Latex Application (very cautious)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Arka Latex External Application',
  'आर्क क्षीर बाह्य उपयोग',
  'आर्क क्षीर बाह्य उपयोग',
  'Arka Ksheera Prayoga (external)',
  'latex_external',
  'wart_and_skin_lesion_support_external',
  '1) Collect minute quantity of Arka latex carefully with gloves. 2) Touch only on wart/corn as per classical guidance. 3) Avoid contact with normal skin, eyes or mucosa; wash thoroughly after time.',
  'gloves;applicator_stick;water_for_wash',
  'Few minutes to apply.',
  'Drop-level quantity.',
  'Use immediately.',
  'Single-use only.',
  '{"adult":"external spot application only under specialist supervision","child":"generally avoided"}',
  'external_use_only',
  'none',
  'Arka latex is irritant and potentially toxic; used traditionally on warts/corns with extreme caution.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Arka'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Arka Latex External Application');

------------------------------------------------------------
-- 60. Datura – ONLY External Oil (for pain, strictly supervised)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Datura External Pain Oil',
  'धतूरा बाह्य दर्द तेल',
  'धोत्रा बाह्य वेदना तेल',
  'Dhattura Taila (external)',
  'medicated_oil_external',
  'pain_and_vata_support_external',
  '1) Use small quantity of Datura leaves/seeds processed in oil under classical taila preparation with safeguards. 2) Filter and store. 3) Apply thinly on painful joints/muscles externally; do not use on broken skin.',
  'oil_pan;filter_cloth;bottles',
  '1–2 hours including heating and cooling.',
  'Depends on oil volume.',
  'Store in cool, dark place.',
  'Few months.',
  '{"adult":"external massage in thin layer under supervision","child":"usually avoided"}',
  'external_use_only',
  'none',
  'Datura is highly toxic if ingested; Arka/Datura oils are strictly external and physician-supervised only.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Datura'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Datura External Pain Oil');

------------------------------------------------------------
-- 61. Erect Boerhavia – Punarnava-like Decoction
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Erect Boerhavia Decoction',
  'एरैक्ट बोर्हाविया काढ़ा',
  'उभा बोर्हाविया काढा',
  'Punarnava Prakar Kwatha',
  'decoction',
  'renal_and_edema_support',
  '1) Use roots/aerial parts of Erect Boerhavia similar to Punarnava. 2) Boil with water and reduce. 3) Filter and use under guidance.',
  'pot;strainer',
  '20–30 minutes.',
  '60–100 ml.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"15–30 ml once or twice daily as advised","child":"only under supervision"}',
  'morning_or_evening',
  'plain',
  'Related species used similarly to Punarnava for edema and urinary issues; species ID is important.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Erect Boerhavia'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Erect Boerhavia Decoction');

------------------------------------------------------------
-- 62. Bhringraj – Bhringraj Hair Oil
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Bhringraj Hair Oil',
  'भृंगराज केश तेल',
  'भृंगराज केस तेल',
  'Bhringaraja Taila',
  'medicated_oil_external',
  'hair_and_scalp_support',
  '1) Prepare Bhringraj juice or decoction. 2) Cook with base oil and suitable kalka (pulp) in classical taila paka. 3) Filter and store. 4) Apply to scalp and hair roots.',
  'oil_pan;filter_cloth;bottles',
  '1–2 hours.',
  'Depends on oil volume.',
  'Store in closed bottles away from heat.',
  'Few months.',
  '{"adult":"scalp massage 2–3 times/week","child":"external use if suitable"}',
  'external_use_only',
  'none',
  'Highly popular oil for hair fall and early greying support.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Bhringraj'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Bhringraj Hair Oil');

------------------------------------------------------------
-- 63. Ram Tulsi – Ram Tulsi Herbal Tea
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Ram Tulsi Herbal Tea',
  'राम तुलसी हर्बल चाय',
  'राम तुळस हर्बल चहा',
  'Tulasi Phanta',
  'herbal_tea',
  'respiratory_and_immunity_support',
  '1) Take fresh Ram Tulsi leaves, wash and lightly crush. 2) Pour hot water over and cover for 5–10 minutes. 3) Strain and sip warm.',
  'cup;strainer',
  '10–15 minutes.',
  'One cup.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"one cup 1–2 times/day in cold/cough seasons","child":"smaller quantity if suitable"}',
  'morning_and/evening',
  'as_is',
  'Sacred Tulsi species used in colds, cough and mild anxiety.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Ram Tulsi'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Ram Tulsi Herbal Tea');

------------------------------------------------------------
-- 64. Sweet Basil – Sweet Basil Herbal Tea
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Sweet Basil Herbal Tea',
  'स्वीट बेसिल हर्बल चाय',
  'स्वीट बेसिल हर्बल चहा',
  'Tulasi Videshi Phanta (modern)',
  'herbal_tea',
  'digestive_and_relax_support',
  '1) Use fresh or dried Sweet Basil leaves. 2) Steep in hot water for 5–10 minutes. 3) Strain and drink warm.',
  'cup;strainer',
  '10–15 minutes.',
  'One cup.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"one cup once or twice daily as relaxing tea","child":"small amount, if suitable"}',
  'evening_or_after_meals',
  'as_is',
  'Parallel to Tulsi but milder; used for digestion and mild relaxation.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Sweet Basil'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Sweet Basil Herbal Tea');

------------------------------------------------------------
-- 65. Field Mint – Pudina Digestive Water
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Pudina Digestive Water',
  'पुदीना पाचन जल',
  'पुदिना पचन पाणी',
  'Pudina Jala (folk)',
  'herbal_water',
  'digestive_and_cooling_support',
  '1) Crush fresh Field Mint leaves lightly. 2) Infuse in potable water for some time. 3) Strain and drink in small amounts.',
  'jug;strainer',
  '15–30 minutes infusion.',
  'Several glasses.',
  'Keep covered and use within the day.',
  'Same-day use.',
  '{"adult":"small glass 1–2 times/day in hot season","child":"smaller quantity if suitable"}',
  'between_meals',
  'as_is',
  'Mint water aids digestion and cooling; avoid in very cold constitution or reflux if worsened.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Field Mint'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Pudina Digestive Water');

------------------------------------------------------------
-- 66. Peppermint – Peppermint Digestive Tea
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Peppermint Digestive Tea',
  'पेपरमिंट पाचन चाय',
  'पेपरमिंट पचन चहा',
  'Peppermint Phanta',
  'herbal_tea',
  'digestive_and_spasm_support',
  '1) Take fresh/dried Peppermint leaves. 2) Steep in hot water for 5–10 minutes. 3) Strain and sip warm.',
  'cup;strainer',
  '10–15 minutes.',
  'One cup.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"one cup after meals for gas/spasm relief","child":"small quantity only if suitable"}',
  'after_meals',
  'as_is',
  'Peppermint tea can relieve spasm but may worsen reflux in some individuals.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Peppermint'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Peppermint Digestive Tea');

------------------------------------------------------------
-- 67. Dill – Dill Seed Digestive Tea
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Dill Seed Digestive Tea',
  'सोया बीज पाचन चाय',
  'शेप बी पचन चहा',
  'Soya/Shepa Phanta',
  'herbal_tea',
  'infant_colic_and_digestive_support',
  '1) Lightly crush Dill seeds. 2) Steep in hot water for 5–10 minutes. 3) Strain and cool before use.',
  'cup;strainer',
  '10–15 minutes.',
  'One cup.',
  'Use fresh.',
  'Same-day.',
  '{"adult":"one cup after meals as needed","child":"few teaspoons of cooled tea for infant colic only on pediatric advice"}',
  'after_meals',
  'as_is',
  'Dill seed tea is popular for colic; exact infant dosing must be guided by pediatrician.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Dill'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Dill Seed Digestive Tea');

------------------------------------------------------------
-- 68. Garlic – Garlic Rasayana Paste (mild)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Garlic Rasayana Paste',
  'लहसुन रसायन लेप्य',
  'लसूण रसायन पेस्ट',
  'Lashuna Rasayana (simplified)',
  'paste',
  'cardio_and_digestive_support',
  '1) Peel Garlic cloves and pound to paste. 2) Gently fry in ghee until mild aroma and remove from flame. 3) Use small quantity with food.',
  'pan;spatula;mortar_and_pestle',
  '15–20 minutes.',
  'Few tablespoons.',
  'Refrigerate for short time if needed.',
  '2–3 days if refrigerated.',
  '{"adult":"1–3 small cloves worth per day depending on tolerance","child":"minimal or none unless advised"}',
  'with_main_meal',
  'as_part_of_food',
  'Garlic is cardioprotective and digestive but can aggravate Pitta and cause odor/reflux.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Garlic'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Garlic Rasayana Paste');

------------------------------------------------------------
-- 69. Onion – Onion Warming Poultice (external)
------------------------------------------------------------
INSERT INTO preparations (
  name_en, name_hi, name_mr, classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Onion Warming Poultice',
  'प्याज गरम पोटली',
  'कांदा गरम पट्टी',
  'Palandu Lepa (external)',
  'paste',
  'respiratory_and_joint_support_external',
  '1) Chop Onion and lightly warm in pan (optional with little oil). 2) Wrap in clean cloth as poultice. 3) Apply warm (not hot) over chest/back or joint under guidance.',
  'pan;cloth;spatula',
  '15–20 minutes.',
  'One or two poultices.',
  'Use immediately; do not store.',
  'Single-use.',
  '{"adult":"external application for 15–20 minutes at a time","child":"only under careful supervision to avoid burns"}',
  'external_use_only',
  'none',
  'Traditional warming poultice for congestion and aches; temperature must be carefully checked.',
  'ayurveda',
  p.id
FROM plants p
WHERE p.common_name_en = 'Onion'
  AND NOT EXISTS (SELECT 1 FROM preparations pr WHERE pr.name_en = 'Onion Warming Poultice');
