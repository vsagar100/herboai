BEGIN TRANSACTION;

-- =========================================================
-- PREPARATIONS (NEW) — schema aligned to:
-- preparations(id, name_en, name_hi, name_mr, classical_name, form_type, category,
-- preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
-- dosage_json, timing, anupana, notes, created_at, updated_at, ayush_system, plant_id)
--
-- NOTE: updated_at is nullable in your PRAGMA output; we omit it.
-- =========================================================

INSERT OR IGNORE INTO preparations (
  name_en, name_hi, name_mr, classical_name,
  form_type, category, preparation_steps,
  equipment_needed, duration, yield, storage, shelf_life,
  dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) VALUES

-- 238 Jivanti
(
  'Jivanti Ksheerapaka',
  'जीवन्ती क्षीरपाक',
  'जीवन्ती क्षीरपाक',
  'जीवन्ती क्षीरपाक',
  'ksheerapaka',
  'rasayana',
  '1) Take 5 g Jivanti coarse powder. 2) Add 200 ml milk + 200 ml water. 3) Simmer on low flame until reduced to ~200 ml. 4) Strain and consume lukewarm.',
  'Saucepan, strainer, measuring cup',
  '30–40 min',
  '~200 ml',
  'Best fresh; refrigerate up to 12 hours if needed',
  'Fresh preferred; up to 12 hours refrigerated',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Prefer at night or as advised."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Only under practitioner guidance."}}',
  'Night / as advised',
  'None / warm milk base',
  'Traditional nourishing ksheerapaka; avoid if milk intolerance.',
  'ayurveda',
  238
),

-- 242 Danti
(
  'Danti Kashaya (Traditional Purgative Support)',
  'दन्ती कषाय',
  'दन्ती कषाय',
  'दन्ती कषाय',
  'decoction',
  'digestive',
  '1) Take 1–2 g Danti root powder (very potent). 2) Add to 250 ml water. 3) Simmer 15–20 minutes and reduce to ~150 ml. 4) Strain. 5) Use ONLY under qualified guidance.',
  'Saucepan, strainer, measuring spoon',
  '20–25 min',
  '~150 ml',
  'Fresh only',
  'Fresh only',
  '{"adult":{"dose":"as_prescribed","frequency_per_day":0,"notes":"Use only with qualified Ayurvedic practitioner due to strong action."},"child":{"dose":"not_recommended","frequency_per_day":0,"notes":"Avoid."}}',
  'As prescribed',
  'Warm water',
  'Strong herb; not for self-medication, pregnancy, elderly, or dehydration risk.',
  'ayurveda',
  242
),

-- 243 Trivrit
(
  'Trivrit Kashaya (Bowel Cleansing Support)',
  'त्रिवृत कषाय',
  'त्रिवृत कषाय',
  'त्रिवृत कषाय',
  'decoction',
  'digestive',
  '1) Take 2–3 g Trivrit root powder (potent). 2) Add to 250 ml water. 3) Simmer 15–20 minutes to ~150 ml. 4) Strain. 5) Use only under professional guidance.',
  'Saucepan, strainer, measuring spoon',
  '20–25 min',
  '~150 ml',
  'Fresh only',
  'Fresh only',
  '{"adult":{"dose":"as_prescribed","frequency_per_day":0,"notes":"Use under practitioner supervision."},"child":{"dose":"not_recommended","frequency_per_day":0,"notes":"Avoid."}}',
  'As prescribed',
  'Warm water',
  'Strong virechana-support herb; avoid self-medication.',
  'ayurveda',
  243
),

-- 245 Deodar
(
  'Deodar Steam Inhalation (Supportive)',
  'देवदारु वाष्प',
  'देवदारू वाफ',
  NULL,
  'steam',
  'respiratory',
  '1) Boil 1–2 tsp Deodar coarse powder (or small chips) in 1–1.5 L water for 5–7 minutes. 2) Turn off heat. 3) Inhale steam carefully for 5–8 minutes.',
  'Pot, towel, hot water setup',
  '10–15 min',
  '1 session',
  'Not applicable',
  'Use immediately',
  '{"adult":{"dose":"1_session","frequency_per_day":1,"notes":"Stop if dizziness/irritation."},"child":{"dose":"not_recommended","frequency_per_day":0,"notes":"Avoid steam for small children."}}',
  'Evening / symptomatic use',
  'None',
  'Supportive measure for congestion; maintain safe distance from steam.',
  'ayurveda',
  245
),

-- 248 Parpata
(
  'Parpata Kashaya',
  'पर्पट कषाय',
  'पर्पट काढा',
  'पर्पट कषाय',
  'decoction',
  'hepatic',
  '1) Take 3–5 g Parpata (dried herb). 2) Add to 250 ml water. 3) Simmer 15–20 minutes to ~150 ml. 4) Strain and consume lukewarm.',
  'Saucepan, strainer',
  '20–25 min',
  '~150 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Prefer daytime."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'Daytime',
  'Warm water',
  'Traditional pitta-support kashaya; if fever/jaundice is severe seek medical care.',
  'ayurveda',
  248
),

-- 249 Guduchi (Sinensis variant)
(
  'Guduchi Kashaya (Variant)',
  'गुडूची कषाय',
  'गुळवेल काढा',
  'गुडूची कषाय',
  'decoction',
  'immune',
  '1) Take 10 g Guduchi stem pieces (or 5 g coarse powder). 2) Boil with 400 ml water. 3) Reduce to ~200 ml. 4) Strain and consume warm.',
  'Saucepan, strainer',
  '30–40 min',
  '~200 ml',
  'Fresh preferred; refrigerate up to 12 hours if needed',
  'Up to 12 hours refrigerated',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Commonly used in intermittent fever support."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'Morning / daytime',
  'Warm water',
  'Traditional immuno-metabolic support decoction.',
  'ayurveda',
  249
),

-- 250 Mahabala
(
  'Mahabala Taila (Simple External Oil Infusion)',
  'महाबला तैल (सरल बाह्य उपयोग)',
  'महाबला तेल (बाह्य उपयोग)',
  NULL,
  'oil',
  'musculoskeletal',
  '1) Warm 50–100 ml sesame oil on very low heat. 2) Add 10 g Mahabala coarse powder. 3) Maintain gentle warmth 10–15 minutes (do not burn). 4) Cool, filter, store. 5) Use for gentle external massage.',
  'Pan, strainer, glass bottle',
  '30–45 min',
  '50–90 ml',
  'Airtight bottle; away from sunlight',
  '1–2 months (clean, dry storage)',
  '{"adult":{"dose":"external_use","frequency_per_day":1,"notes":"Massage 10–15 minutes."},"child":{"dose":"external_use","frequency_per_day":1,"notes":"Use mild pressure."}}',
  'Anytime',
  'None',
  'External supportive oil; patch-test first.',
  'ayurveda',
  250
),

-- 251 Kali Musli
(
  'Kali Musli Milk Decoction',
  'काली मुसली क्षीर',
  'काळी मुसळी दूध काढा',
  NULL,
  'ksheerapaka',
  'rasayana',
  '1) Take 3–5 g Kali Musli powder. 2) Add 200 ml milk + 200 ml water. 3) Simmer to ~200 ml. 4) Strain and drink lukewarm.',
  'Saucepan, strainer',
  '30–40 min',
  '~200 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Prefer night."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'Night',
  'Milk base',
  'Nourishing ksheerapaka; avoid if lactose intolerance.',
  'ayurveda',
  251
),

-- 254 Priyangu
(
  'Priyangu Infusion (Cooling Herbal Tea)',
  'प्रियंगु फाँट',
  'प्रियंगु फांट',
  NULL,
  'infusion',
  'skin',
  '1) Take 2–3 g Priyangu dried material. 2) Add to 200 ml hot water. 3) Cover and steep 10–12 minutes. 4) Strain and drink lukewarm.',
  'Cup, lid, strainer',
  '10–15 min',
  '~180 ml',
  'Fresh only',
  'Use immediately',
  '{"adult":{"dose":"150-180 ml","frequency_per_day":1,"notes":"Prefer daytime."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Mild strength only."}}',
  'Daytime',
  'Warm water',
  'Cooling infusion; supportive for pitta-prone tendencies.',
  'ayurveda',
  254
),

-- 256 Tejphal
(
  'Tejphal Digestive Decoction',
  'तेजफल काढ़ा',
  'तेजफळ काढा',
  NULL,
  'decoction',
  'digestive',
  '1) Take 1–2 g Tejphal powder. 2) Boil with 250 ml water to ~150 ml. 3) Strain and sip warm after meals.',
  'Saucepan, strainer',
  '15–20 min',
  '~150 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"After meals."},"child":{"dose":"not_recommended_without_clinician","frequency_per_day":0,"notes":"Consult."}}',
  'After meals',
  'Warm water',
  'Digestive supportive; stop if gastric irritation occurs.',
  'ayurveda',
  256
),

-- 259 White Sandalwood
(
  'White Sandalwood Cooling Paste (External)',
  'श्वेत चन्दन लेप',
  'श्वेत चंदन लेप',
  'चन्दन लेप',
  'paste',
  'skin',
  '1) Take 1–2 tsp sandalwood powder. 2) Add rose water or clean water to make smooth paste. 3) Apply thin layer on clean skin. 4) Wash off after 15–20 minutes.',
  'Bowl, spoon',
  '5–10 min',
  'Single use',
  'Prepare fresh each time',
  'Use immediately',
  '{"adult":{"dose":"external_use","frequency_per_day":1,"notes":"Patch test first."},"child":{"dose":"external_use","frequency_per_day":1,"notes":"Use mild dilution."}}',
  'Anytime',
  'None',
  'External soothing paste; avoid on broken skin.',
  'ayurveda',
  259
),

-- 263 Babul
(
  'Babul Bark Decoction (Gargle Support)',
  'बबूल छाल काढ़ा (गरारे)',
  'बाभूळ सालीचा काढा (गरारे)',
  NULL,
  'decoction',
  'oral',
  '1) Take 5–7 g Babul bark coarse pieces. 2) Boil with 400 ml water to ~200 ml. 3) Cool to lukewarm. 4) Use as gargle 2–3 times/day.',
  'Saucepan, strainer',
  '30–40 min',
  '~200 ml',
  'Refrigerate up to 24 hours',
  'Up to 24 hours refrigerated',
  '{"adult":{"dose":"gargle_50-100ml","frequency_per_day":2,"notes":"Do not swallow large quantities."},"child":{"dose":"not_recommended_without_clinician","frequency_per_day":0,"notes":"Consult."}}',
  'Morning/evening',
  'None',
  'Supportive oral/throat care.',
  'ayurveda',
  263
),

-- 270 Bamboo
(
  'Bamboo Manna Warm Drink (Supportive)',
  'वंशलोचन पेय',
  'वंशलोचन पेय',
  'वंशलोचन',
  'drink',
  'respiratory',
  '1) Take 1–2 g Vanshlochan (bamboo manna). 2) Mix in 150–200 ml warm water or warm milk. 3) Stir well and consume.',
  'Cup, spoon',
  '2–3 min',
  '1 serving',
  'Not applicable',
  'Use immediately',
  '{"adult":{"dose":"1-2 g","frequency_per_day":1,"notes":"Prefer at night for throat comfort."},"child":{"dose":"0.5-1 g","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'Night / as needed',
  'Warm water / warm milk',
  'Supportive for throat comfort; not a substitute for medical care.',
  'ayurveda',
  270
),

-- 273 Psyllium
(
  'Psyllium Husk in Warm Water',
  'इसबगोल भूसी',
  'इसबगोल भुशी',
  NULL,
  'powder',
  'digestive',
  '1) Take 5 g psyllium husk. 2) Mix in 200 ml warm water. 3) Drink immediately, then drink additional water.',
  'Glass, spoon',
  '2–3 min',
  '1 serving',
  'Keep husk dry, airtight',
  '6 months (airtight, dry)',
  '{"adult":{"dose":"5 g","frequency_per_day":1,"notes":"Increase water intake."},"child":{"dose":"2-3 g","frequency_per_day":1,"notes":"Only with adequate water and supervision."}}',
  'Night / after dinner',
  'Warm water',
  'Avoid if swallowing difficulty; ensure adequate hydration.',
  'ayurveda',
  273
),

-- 275 Chicory
(
  'Chicory Root Decoction',
  'कासनी काढ़ा',
  'कासणी काढा',
  NULL,
  'decoction',
  'hepatic',
  '1) Take 3–5 g chicory root. 2) Boil with 300 ml water to ~180 ml. 3) Strain and drink lukewarm.',
  'Saucepan, strainer',
  '20–30 min',
  '~180 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"150-180 ml","frequency_per_day":1,"notes":"Prefer daytime."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'Daytime',
  'Warm water',
  'Traditional hepatic support decoction.',
  'ayurveda',
  275
),

-- 283 Agnimantha (Dashamoola)
(
  'Dashamoola Kvatha (Agnimantha-led)',
  'दशमूल क्वाथ',
  'दशमूळ क्वाथ',
  'दशमूल क्वाथ',
  'decoction',
  'musculoskeletal',
  '1) Mix Dashamoola coarse powders in equal parts (Agnimantha, Shyonaka, Patala, Gambhari, Shalaparni, Prishniparni, Brihati, Kantakari, Gokshura, Bilva). 2) Take 10 g of the mix. 3) Boil with 400 ml water. 4) Reduce to ~200 ml. 5) Strain and consume warm.',
  'Saucepan, strainer, measuring spoon',
  '35–45 min',
  '~200 ml',
  'Fresh preferred; refrigerate up to 12 hours if needed',
  'Up to 12 hours refrigerated',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Commonly used in vata-kapha discomfort."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Only under practitioner guidance."}}',
  'Morning/evening',
  'Warm water',
  'Classical kvatha for supportive use; not a substitute for medical evaluation.',
  'ayurveda',
  283
),

-- 289 Rasna
(
  'Rasna Kashaya',
  'रास्ना कषाय',
  'रास्ना काढा',
  'रास्ना कषाय',
  'decoction',
  'musculoskeletal',
  '1) Take 5 g Rasna coarse powder. 2) Boil with 300 ml water to ~180 ml. 3) Strain and consume warm.',
  'Saucepan, strainer',
  '20–30 min',
  '~180 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"120-180 ml","frequency_per_day":1,"notes":"Prefer after meals."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'After meals',
  'Warm water',
  'Supportive for vata-related discomfort.',
  'ayurveda',
  289
),

-- 290 Lodhra
(
  'Lodhra Kashaya (Women’s Support)',
  'लोध्र कषाय',
  'लोध्र काढा',
  'लोध्र कषाय',
  'decoction',
  'gynecological',
  '1) Take 5 g Lodhra bark powder. 2) Boil with 300 ml water to ~180 ml. 3) Strain and consume warm.',
  'Saucepan, strainer',
  '20–30 min',
  '~180 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Only under qualified guidance for menstrual concerns."},"child":{"dose":"not_recommended","frequency_per_day":0,"notes":"Avoid."}}',
  'Daytime',
  'Warm water',
  'Traditional use in women’s health; consult clinician for heavy bleeding or persistent issues.',
  'ayurveda',
  290
),

-- 291 Nagakesara
(
  'Nagakesara Infusion',
  'नागकेसर फाँट',
  'नागकेसर फांट',
  NULL,
  'infusion',
  'digestive',
  '1) Take 1–2 g Nagakesara. 2) Add to 200 ml hot water. 3) Steep 10 minutes, strain, sip warm.',
  'Cup, lid, strainer',
  '10–12 min',
  '~180 ml',
  'Fresh only',
  'Use immediately',
  '{"adult":{"dose":"150-180 ml","frequency_per_day":1,"notes":"After meals."},"child":{"dose":"not_recommended_without_clinician","frequency_per_day":0,"notes":"Consult."}}',
  'After meals',
  'Warm water',
  'Supportive infusion for digestion comfort.',
  'ayurveda',
  291
),

-- 292 Ativisha
(
  'Ativisha Kashaya (Digestive Support)',
  'अतिविषा कषाय',
  'अतिविषा काढा',
  'अतिविषा कषाय',
  'decoction',
  'digestive',
  '1) Take 1–2 g Ativisha root powder. 2) Add to 250 ml water. 3) Simmer 15 minutes to ~150 ml. 4) Strain and consume lukewarm.',
  'Saucepan, strainer',
  '15–20 min',
  '~150 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"75-120 ml","frequency_per_day":1,"notes":"If symptoms persist, seek medical care."},"child":{"dose":"25-50 ml","frequency_per_day":1,"notes":"Only under practitioner guidance."}}',
  'Daytime',
  'Warm water',
  'Traditional digestive support; avoid overdose.',
  'ayurveda',
  292
),

-- 294 Bharangi
(
  'Bharangi Kashaya',
  'भरंगी कषाय',
  'भरंगी काढा',
  'भरंगी कषाय',
  'decoction',
  'respiratory',
  '1) Take 5 g Bharangi root/bark powder. 2) Boil with 300 ml water to ~180 ml. 3) Strain and consume warm.',
  'Saucepan, strainer',
  '20–30 min',
  '~180 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Supportive for cough tendency."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'Evening',
  'Warm water',
  'Supportive for cough/bronchial discomfort; not a substitute for medical care.',
  'ayurveda',
  294
),

-- 295 Varuna
(
  'Varuna Decoction',
  'वरुण काढ़ा',
  'वरुण काढा',
  'वरुण कषाय',
  'decoction',
  'urinary',
  '1) Take 5–7 g Varuna bark powder. 2) Boil with 400 ml water to ~200 ml. 3) Strain and consume warm.',
  'Saucepan, strainer',
  '30–40 min',
  '~200 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Traditional urinary tract support."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'Morning',
  'Warm water',
  'Supportive for urinary comfort; if severe pain/fever/blood in urine, seek urgent care.',
  'ayurveda',
  295
),

-- 353 Sharpunkha
(
  'Sharpunkha Kashaya',
  'शर्पुंखा कषाय',
  'शर्पुंखा काढा',
  'शर्पुंखा कषाय',
  'decoction',
  'hepatic',
  '1) Take 5 g Sharpunkha whole plant powder. 2) Boil with 300 ml water to ~180 ml. 3) Strain and drink lukewarm.',
  'Saucepan, strainer',
  '20–30 min',
  '~180 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"120-180 ml","frequency_per_day":1,"notes":"Prefer daytime."},"child":{"dose":"50-75 ml","frequency_per_day":1,"notes":"Practitioner guidance."}}',
  'Daytime',
  'Warm water',
  'Traditional liver-support kashaya.',
  'ayurveda',
  353
),

-- 355 Kanchanara
(
  'Kanchanara Bark Decoction',
  'कांचनार काढ़ा',
  'कांचनार काढा',
  'कांचनार कषाय',
  'decoction',
  'metabolic',
  '1) Take 5–7 g Kanchanara bark powder. 2) Boil with 400 ml water to ~200 ml. 3) Strain and consume warm.',
  'Saucepan, strainer',
  '30–40 min',
  '~200 ml',
  'Fresh preferred',
  'Fresh preferred',
  '{"adult":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Traditional gland/metabolic support; consult if thyroid issues."},"child":{"dose":"not_recommended_without_clinician","frequency_per_day":0,"notes":"Consult."}}',
  'Morning',
  'Warm water',
  'Supportive decoction; consult clinician for lumps/swelling or thyroid conditions.',
  'ayurveda',
  355
),

-- UNANI: 204 Walnut
(
  'Unani Roghan-e-Girda (Walnut Oil Support)',
  'अखरोट तेल (यूनानी)',
  'अक्रोड तेल (युनानी)',
  NULL,
  'oil',
  'nutritive',
  '1) Use cold-pressed walnut oil. 2) Take measured dose with warm milk/water as advised. 3) Store tightly closed away from heat/light.',
  'Measuring spoon, bottle',
  '2–3 min',
  'Per dose',
  'Cool dark place; tightly closed',
  '2–3 months (check rancidity)',
  '{"adult":{"dose":"5-10 ml","frequency_per_day":1,"notes":"Dietary support; not for nut allergy."},"child":{"dose":"not_recommended_without_clinician","frequency_per_day":0,"notes":"Consult."}}',
  'With breakfast',
  'Warm milk / warm water',
  'Avoid in nut allergy; discontinue if GI upset.',
  'unani',
  204
),

-- UNANI: 205 Pumpkin Seed
(
  'Unani Maghz-e-Kadu Drink',
  'कद्दू बीज पेय (यूनानी)',
  'भोपळ्याच्या बियांचे पेय (युनानी)',
  NULL,
  'drink',
  'urinary',
  '1) Take 15–20 g pumpkin seeds. 2) Lightly crush and soak 30 minutes. 3) Blend with 200 ml water and strain. 4) Consume fresh.',
  'Mortar/pestle or blender, strainer',
  '35–40 min (incl. soak)',
  '~180 ml',
  'Fresh only',
  'Use immediately',
  '{"adult":{"dose":"150-200 ml","frequency_per_day":1,"notes":"Dietary urinary support."},"child":{"dose":"75-100 ml","frequency_per_day":1,"notes":"Supervision advised."}}',
  'Daytime',
  'Water',
  'Food-based drink; not a substitute for UTI treatment.',
  'unani',
  205
),

-- UNANI: 206 Muskmelon
(
  'Unani Kharbuza Sharbat (Simple)',
  'खरबूजा शरबत (यूनानी)',
  'खरबुज शरबत (युनानी)',
  NULL,
  'syrup',
  'hydration',
  '1) Blend ripe muskmelon pulp. 2) Strain if needed. 3) Mix 1 part pulp with 1–2 parts cool water. 4) Serve fresh.',
  'Blender, sieve (optional)',
  '5–10 min',
  '1–2 servings',
  'Fresh only',
  'Use immediately',
  '{"adult":{"dose":"200-300 ml","frequency_per_day":1,"notes":"Avoid added sugar if diabetic."},"child":{"dose":"100-150 ml","frequency_per_day":1,"notes":"Fresh only."}}',
  'Daytime',
  'Water',
  'Hydration support; avoid excess sugar.',
  'unani',
  206
);

COMMIT;

BEGIN;

-- =========================================================
-- A) FIX: image_hero should NOT contain <>  + must use underscores
-- =========================================================
UPDATE plants
SET image_hero = REPLACE(REPLACE(COALESCE(image_hero,''), '<',''), '>','')
WHERE image_hero LIKE '%<%' OR image_hero LIKE '%>%';

-- Rebuild image_hero from common_name_en (spaces -> underscores) for ALL plants where common_name_en exists
UPDATE plants
SET image_hero = REPLACE(TRIM(common_name_en), ' ', '_') || '.jpg',
    updated_at = CURRENT_TIMESTAMP
WHERE common_name_en IS NOT NULL AND TRIM(common_name_en) <> '';

-- =========================================================
-- B) NEXT BATCH: Classical Ayurveda plants (25) - UNIQUE botanical_name
-- NOTE: JSON fields MUST be valid JSON strings (arrays/objects)
-- =========================================================
INSERT OR IGNORE INTO plants
(botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name, family,
 description, habitat, parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
 active_compounds, therapeutic_actions, classical_references, is_endangered, cultivation_status, image_hero, ayush_system)
VALUES
-- 1
('Oroxylum indicum','Shyonaka','श्योनक','श्योनक','श्योनक','Bignoniaceae',
 'Classical Ayurvedic tree drug used traditionally in formulations; commonly counted in Dashamoola group.','Tropical deciduous forests; plains to sub-Himalayan tracts.',
 '["root_bark","stem_bark"]','["कषाय","तिक्त"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"vata":"pacifies","kapha":"pacifies"}','Dashamoola-dravya',
 NULL,'["deepana","shothahara"]','Charaka Samhita; Dashamoola references',0,'Cultivated/Wild',
 'Shyonaka.jpg','ayurveda'),

-- 2
('Gmelina arborea','Gambhari','गम्भारी','गंभीर','गम्भारी','Lamiaceae',
 'Classical Ayurvedic tree drug, traditionally used in Dashamoola group.','Moist deciduous forests; cultivated in many regions.',
 '["root_bark","stem_bark"]','["मधुर","कषाय"]','शीत','मधुर','["गुरु","स्निग्ध"]',
 '{"vata":"pacifies","pitta":"pacifies"}','Dashamoola-dravya',
 NULL,'["balya","brimhana"]','Charaka Samhita; Dashamoola references',0,'Cultivated/Wild',
 'Gambhari.jpg','ayurveda'),

-- 3
('Stereospermum suaveolens','Patala','पाटला','पाटला','पाटला','Bignoniaceae',
 'Classical Ayurvedic tree drug, traditionally part of Dashamoola.','Deciduous forests of India; also planted near villages.',
 '["root_bark","stem_bark"]','["तिक्त","कषाय"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"vata":"pacifies","kapha":"pacifies"}','Dashamoola-dravya',
 NULL,'["shothahara","vedanasthapana"]','Charaka Samhita; Dashamoola references',0,'Wild/Cultivated',
 'Patala.jpg','ayurveda'),

-- 4
('Clerodendrum phlomidis','Agnimantha','अग्निमन्थ','अग्निमंथ','अग्निमन्थ','Lamiaceae',
 'Classical Ayurvedic shrub/tree, traditionally listed in Dashamoola.','Dry regions; scrub forests; hedges.',
 '["root","root_bark"]','["तिक्त","कटु"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"vata":"pacifies","kapha":"pacifies"}','Dashamoola-dravya',
 NULL,'["deepana","shothahara"]','Charaka Samhita; Dashamoola references',0,'Wild/Cultivated',
 'Agnimantha.jpg','ayurveda'),

-- 5
('Desmodium gangeticum','Shalaparni','शालपर्णी','शालपर्णी','शालपर्णी','Fabaceae',
 'Classical Ayurvedic herb, traditionally counted in Dashamoola.','Forest undergrowth; dry forests; plains.',
 '["root","whole_plant"]','["मधुर","तिक्त"]','शीत','मधुर','["गुरु","स्निग्ध"]',
 '{"vata":"pacifies","pitta":"pacifies"}','Dashamoola-dravya',
 NULL,'["balya","rasayana"]','Charaka Samhita; Dashamoola references',0,'Wild/Cultivated',
 'Shalaparni.jpg','ayurveda'),

-- 6
('Uraria picta','Prishniparni','पृश्निपर्णी','पृश्निपर्णी','पृश्निपर्णी','Fabaceae',
 'Classical Ayurvedic herb, traditionally counted in Dashamoola.','Dry regions; scrub forests; open fields.',
 '["root","whole_plant"]','["मधुर","तिक्त"]','उष्ण','मधुर','["लघु"]',
 '{"vata":"pacifies","kapha":"pacifies"}','Dashamoola-dravya',
 NULL,'["balya","shothahara"]','Charaka Samhita; Dashamoola references',0,'Wild',
 'Prishniparni.jpg','ayurveda'),

-- 7
('Asteracantha longifolia','Kokilaksha (Alt)','कोकिलाक्ष','कोकिलाक्ष','कोकिलाक्ष','Acanthaceae',
 'Ayurvedic plant used traditionally for urinary support and related formulations.','Wetlands; riverbanks; marshy areas.',
 '["seed","root","whole_plant"]','["मधुर"]','शीत','मधुर','["गुरु","स्निग्ध"]',
 '{"pitta":"pacifies","vata":"pacifies"}','Mutrala-dravya',
 NULL,'["mutrala","balya"]','Bhavaprakasha Nighantu',0,'Wild/Cultivated',
 'Kokilaksha_(Alt).jpg','ayurveda'),

-- 8
('Symplocos racemosa','Lodhra (Alt)','लोध्र','लोधर','लोध्र','Symplocaceae',
 'Classical Ayurvedic bark drug used traditionally in women’s health related formulations.','Himalayan foothills; moist forests.',
 '["bark"]','["कषाय"]','शीत','कटु','["लघु","रूक्ष"]',
 '{"kapha":"pacifies","pitta":"pacifies"}','Stambhana-dravya',
 NULL,'["stambhana","raktaprasadana"]','Bhavaprakasha Nighantu',0,'Wild/Cultivated',
 'Lodhra_(Alt).jpg','ayurveda'),

-- 9
('Mesua ferrea','Nagakesara (Alt)','नागकेसर','नागकेसर','नागकेसर','Calophyllaceae',
 'Classical Ayurvedic flower/stamen drug used traditionally in bleeding tendency patterns.','Evergreen forests; humid regions.',
 '["stamen","flower_bud"]','["कषाय","तिक्त"]','शीत','कटु','["लघु","रूक्ष"]',
 '{"pitta":"pacifies","kapha":"pacifies"}','Raktapitta-hara',
 NULL,'["stambhana","raktaprasadana"]','Charaka Samhita; Bhavaprakasha',0,'Cultivated/Wild',
 'Nagakesara_(Alt).jpg','ayurveda'),

-- 10
('Aconitum heterophyllum','Ativisha (Alt)','अतिविषा','अतिविषा','अतिविषा','Ranunculaceae',
 'Classical Ayurvedic tuber drug used traditionally in digestive/fever-related formulations.','Himalayan regions; alpine zones.',
 '["tuberous_root"]','["तिक्त","कटु"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"kapha":"pacifies","vata":"pacifies"}','Deepana-pachana',
 NULL,'["deepana","pachana"]','Charaka Samhita; Bhavaprakasha',0,'Wild (regulated collection)',
 'Ativisha_(Alt).jpg','ayurveda'),

-- 11
('Semecarpus anacardium','Bhallataka (Alt)','भल्लातक','भिलावा','भल्लातक','Anacardiaceae',
 'Classical Ayurvedic drug used traditionally in specific formulations (processed use in practice).','Subtropical forests; dry regions.',
 '["fruit"]','["कटु","तिक्त"]','उष्ण','कटु','["लघु","तीक्ष्ण"]',
 '{"kapha":"pacifies","vata":"pacifies"}','Agnideepana',
 NULL,'["deepana","kaphahara"]','Bhavaprakasha Nighantu',0,'Wild/Cultivated',
 'Bhallataka_(Alt).jpg','ayurveda'),

-- 12
('Clerodendrum serratum','Bharangi (Alt)','भारंगी','भारंगी','भारंगी','Lamiaceae',
 'Classical Ayurvedic root drug used traditionally in respiratory patterns.','Hilly tracts; forest edges.',
 '["root"]','["तिक्त","कटु"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"kapha":"pacifies","vata":"pacifies"}','Shwasahara',
 NULL,'["kaphahara","shwasahara"]','Charaka Samhita; Bhavaprakasha',0,'Wild/Cultivated',
 'Bharangi_(Alt).jpg','ayurveda'),

-- 13
('Crataeva nurvala','Varuna (Alt)','वरुण','वरुण','वरुण','Capparaceae',
 'Classical Ayurvedic bark drug used traditionally for urinary stone tendency patterns.','Riverbanks; moist forests; cultivated.',
 '["bark","root_bark"]','["तिक्त","कषाय"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"kapha":"pacifies","vata":"pacifies"}','Ashmari-hara',
 NULL,'["mutrala","ashmarihara"]','Bhavaprakasha Nighantu',0,'Cultivated/Wild',
 'Varuna_(Alt).jpg','ayurveda'),

-- 14
('Pluchea lanceolata','Rasna (Alt)','रस्ना','रस्ना','रस्ना','Asteraceae',
 'Classical Ayurvedic herb used traditionally in vata-related joint discomfort patterns.','Plains; dry places; field margins.',
 '["root","leaf"]','["तिक्त"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"vata":"pacifies"}','Vatahara',
 NULL,'["vatahara","shothahara"]','Bhavaprakasha Nighantu',0,'Wild/Cultivated',
 'Rasna_(Alt).jpg','ayurveda'),

-- 15
('Aegle marmelos (root)','Bilva Root','बिल्व मूल','बिल्व मुळ','बिल्व मूल','Rutaceae',
 'Bilva root is used in classical group-drugs and formulations; distinct from fruit usage.','Cultivated; dry forests and plains.',
 '["root_bark"]','["कषाय","तिक्त"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"vata":"pacifies","kapha":"pacifies"}','Dashamoola-related use',
 NULL,'["deepana","grahi"]','Charaka Samhita; Dashamoola references',0,'Cultivated',
 'Bilva_Root.jpg','ayurveda'),

-- 16
('Glycyrrhiza glabra (stem)','Licorice Stem','मुलेठी तना','जेष्ठमध कांड','यष्टिमधु','Fabaceae',
 'Stem portion used traditionally similar to root as supportive raw material in some preparations.','Cultivated; dry regions.',
 '["stem"]','["मधुर"]','शीत','मधुर','["गुरु","स्निग्ध"]',
 '{"vata":"pacifies","pitta":"pacifies"}','Madhura-rasayana',
 NULL,'["rasayana","vranaropana"]','Bhavaprakasha Nighantu',0,'Cultivated',
 'Licorice_Stem.jpg','ayurveda'),

-- 17
('Tinospora cordifolia (leaf)','Guduchi Leaf','गुडूची पत्ती','गुळवेल पान','गुडूची','Menispermaceae',
 'Guduchi leaf is used traditionally in decoctions/infusions as supportive raw material.','Tropical India; climbs on trees.',
 '["leaf"]','["तिक्त","कषाय"]','उष्ण','मधुर','["लघु","स्निग्ध"]',
 '{"tridosha":"balances"}','Rasayana',
 NULL,'["rasayana","jwaraghna"]','Charaka Samhita',0,'Wild/Cultivated',
 'Guduchi_Leaf.jpg','ayurveda'),

-- 18
('Terminalia chebula (unripe)','Haritaki (Unripe)','हरड़ (कच्चा)','हिरडा (कच्चा)','हरितकी','Combretaceae',
 'Unripe fruit used traditionally as astringent/grahi in classical practice.','Deciduous forests; cultivated.',
 '["fruit_unripe"]','["कषाय"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"kapha":"pacifies","pitta":"pacifies"}','Grahi',
 NULL,'["anulomana","grahi"]','Bhavaprakasha Nighantu',0,'Wild/Cultivated',
 'Haritaki_(Unripe).jpg','ayurveda'),

-- 19
('Terminalia bellirica (kernel)','Bibhitaki Kernel','बहेड़ा गिरी','बेहडा गर','बिभीतकी','Combretaceae',
 'Kernel used traditionally in powders; supportive raw material.','Deciduous forests; cultivated.',
 '["seed_kernel"]','["कषाय"]','उष्ण','मधुर','["लघु","रूक्ष"]',
 '{"kapha":"pacifies"}','Kaphahara',
 NULL,'["kaphahara","kasahara"]','Bhavaprakasha Nighantu',0,'Wild/Cultivated',
 'Bibhitaki_Kernel.jpg','ayurveda'),

-- 20
('Saraca asoca (leaf)','Ashoka Leaf','अशोक पत्ता','अशोक पान','अशोक','Fabaceae',
 'Leaf used traditionally as supportive raw material in women’s health patterns.','Moist forests; cultivated.',
 '["leaf"]','["कषाय","तिक्त"]','शीत','कटु','["लघु","रूक्ष"]',
 '{"pitta":"pacifies","kapha":"pacifies"}','Stambhana',
 NULL,'["stambhana","yonidoshahara"]','Charaka Samhita; Bhavaprakasha',0,'Cultivated',
 'Ashoka_Leaf.jpg','ayurveda'),

-- 21
('Azadirachta indica (bark)','Neem Bark','नीम की छाल','निंबाची साल','निंब','Meliaceae',
 'Bark used traditionally in classical preparations as astringent bitter drug.','Throughout India; widely cultivated.',
 '["bark"]','["तिक्त","कषाय"]','शीत','कटु','["लघु","रूक्ष"]',
 '{"pitta":"pacifies","kapha":"pacifies"}','Krimighna',
 NULL,'["krimighna","kandughna"]','Charaka Samhita',0,'Cultivated/Wild',
 'Neem_Bark.jpg','ayurveda'),

-- 22
('Zingiber officinale (dry)','Dry Ginger','सोंठ','सुंठ','शुण्ठी','Zingiberaceae',
 'Dry ginger used traditionally for digestive and respiratory support in classical practice.','Cultivated.',
 '["rhizome_dry"]','["कटु"]','उष्ण','मधुर','["लघु","रूक्ष"]',
 '{"vata":"pacifies","kapha":"pacifies"}','Deepana',
 NULL,'["deepana","pachana"]','Charaka Samhita',0,'Cultivated',
 'Dry_Ginger.jpg','ayurveda'),

-- 23
('Piper nigrum (fruit)','Black Pepper (Fruit)','काली मिर्च','काळी मिरी','मरिच','Piperaceae',
 'Fruit used traditionally in powders and decoctions as deepana/kaphahara drug.','Cultivated.',
 '["fruit"]','["कटु"]','उष्ण','कटु','["लघु","तीक्ष्ण"]',
 '{"kapha":"pacifies","vata":"pacifies"}','Trikatu component',
 NULL,'["deepana","kaphahara"]','Charaka Samhita',0,'Cultivated',
 'Black_Pepper_(Fruit).jpg','ayurveda'),

-- 24
('Piper longum (root)','Pippali Root','पीपली मूल','पिंपळी मुळ','पिप्पलीमूल','Piperaceae',
 'Root used traditionally as supportive raw material; distinct from fruit usage.','Cultivated.',
 '["root"]','["कटु"]','उष्ण','मधुर','["लघु","स्निग्ध"]',
 '{"vata":"pacifies","kapha":"pacifies"}','Rasayana-like in practice',
 NULL,'["deepana","kaphahara"]','Bhavaprakasha Nighantu',0,'Cultivated',
 'Pippali_Root.jpg','ayurveda'),

-- 25
('Embelia ribes (fruit)','Vidanga (Fruit)','विडंग','विडंग','विडंग','Primulaceae',
 'Fruit used traditionally for worm tendency patterns in classical practice.','Hilly forests; cultivated in some areas.',
 '["fruit"]','["कटु","कषाय"]','उष्ण','कटु','["लघु","रूक्ष"]',
 '{"kapha":"pacifies","vata":"pacifies"}','Krimighna',
 NULL,'["krimighna","deepana"]','Charaka Samhita; Bhavaprakasha',0,'Wild/Cultivated',
 'Vidanga_(Fruit).jpg','ayurveda');

-- =========================================================
-- C) ADD DISEASES (ONLY if missing): add 10 Ayurveda-relevant diseases (JSON-valid)
--    Uses INSERT OR IGNORE pattern by name_en uniqueness is not enforced in schema,
--    so we guard with WHERE NOT EXISTS
-- =========================================================
INSERT OR IGNORE INTO diseases
(name_en, name_hi, name_mr, category, ayurvedic_name, unani_name, siddha_name, description,
 symptoms, causes, dosha_involvement, dhatu_involvement, severity_level, is_lifestyle_related,
 prevention_tips, dietary_recommendations, updated_at)
SELECT
'Joint Inflammation / Shotha Pattern','जोड़ों की सूजन (शोथ)','सांध्यांची सूज (शोथ)','musculoskeletal',
'शोथ',NULL,NULL,
'Inflammatory swelling pattern described in classical Ayurveda as shotha; may present with pain, heaviness, restricted movement.',
'["joint swelling","pain","stiffness","warmth"]',
'["dietary indiscretion","overuse","seasonal aggravation","ama accumulation"]',
'{"vata":"secondary","kapha":"primary"}',
'{"asthi":"secondary","mamsa":"primary"}',
'moderate',1,
'["regular movement","avoid heavy/cold foods","maintain sleep routine"]',
'{"avoid":["deep-fried","excess dairy","cold drinks"],"prefer":["warm soups","light gruels","spices in moderation"]}',
CURRENT_TIMESTAMP
WHERE NOT EXISTS (SELECT 1 FROM diseases WHERE name_en='Joint Inflammation / Shotha Pattern');

INSERT OR IGNORE INTO diseases
(name_en, name_hi, name_mr, category, ayurvedic_name, description,
 symptoms, causes, dosha_involvement, dhatu_involvement, severity_level, is_lifestyle_related,
 prevention_tips, dietary_recommendations, updated_at)
SELECT
'Respiratory Congestion / Kasa-Shwasa Pattern','श्वसन जकड़न (कास-श्वास)','श्वसन कोंडी (कास-श्वास)','respiratory',
'कास-श्वास',
'Congestion pattern described in Ayurveda with cough/breathing difficulty tendency.',
'["cough","wheezing","thick sputum","chest heaviness"]',
'["cold exposure","dust/smoke exposure","kapha aggravating diet"]',
'{"kapha":"primary","vata":"secondary"}',
'{"prana_vaha_srotas":"primary"}',
'moderate',1,
'["warm water sips","steam inhalation","avoid cold foods"]',
'{"avoid":["ice-cold foods","curd at night"],"prefer":["warm liquids","light meals"]}',
CURRENT_TIMESTAMP
WHERE NOT EXISTS (SELECT 1 FROM diseases WHERE name_en='Respiratory Congestion / Kasa-Shwasa Pattern');

INSERT OR IGNORE INTO diseases
(name_en, name_hi, name_mr, category, ayurvedic_name, description,
 symptoms, causes, dosha_involvement, dhatu_involvement, severity_level, is_lifestyle_related,
 prevention_tips, dietary_recommendations, updated_at)
SELECT
'Poor Appetite / Agnimandya','भूख कम लगना (अग्निमांद्य)','भूक मंदावणे (अग्निमांद्य)','digestive',
'अग्निमांद्य',
'Digestive fire weakness pattern described in Ayurveda (agnimandya).',
'["low appetite","bloating","heaviness after meals"]',
'["irregular meals","heavy foods","stress","low activity"]',
'{"kapha":"primary","vata":"secondary"}',
'{"rasa":"primary"}',
'mild',1,
'["regular meal timing","light dinner","walk after meals"]',
'{"prefer":["warm cooked foods","spices in moderation"],"avoid":["very heavy meals","late-night eating"]}',
CURRENT_TIMESTAMP
WHERE NOT EXISTS (SELECT 1 FROM diseases WHERE name_en='Poor Appetite / Agnimandya');

INSERT OR IGNORE INTO diseases
(name_en, name_hi, name_mr, category, ayurvedic_name, description,
 symptoms, causes, dosha_involvement, dhatu_involvement, severity_level, is_lifestyle_related,
 prevention_tips, dietary_recommendations, updated_at)
SELECT
'Worm Tendency / Krimi Pattern','कृमि प्रवृत्ति','कृमी प्रवृत्ती','digestive',
'कृमि',
'Traditional krimi tendency pattern described in Ayurveda.',
'["itching around anus","abdominal discomfort","nausea","irregular stools"]',
'["poor hygiene","contaminated food","kapha/ama accumulation"]',
'{"kapha":"primary"}',
'{"rasa":"primary"}',
'moderate',1,
'["hand hygiene","safe drinking water","properly cooked food"]',
'{"avoid":["excess sweets"],"prefer":["light meals","warm water"]}',
CURRENT_TIMESTAMP
WHERE NOT EXISTS (SELECT 1 FROM diseases WHERE name_en='Worm Tendency / Krimi Pattern');

-- =========================================================
-- D) MAP: new batch plants -> diseases (use existing disease ids + the new ones above)
--     Existing disease IDs you already have:
--       10 Intestinal Worm Infestation
--       11 Bronchial Asthma
--       12 Chronic Cough and Bronchitis
--       157 Constipation
--       161 Osteoarthritis / Joint Degeneration
--       164 Allergic Rhinitis
--       166 Migraine / Recurrent Headache
--     New diseases inserted above are name-based, so we map via subqueries.
-- =========================================================

-- Helper: map Dashamoola-related plants to joint/inflammation + respiratory
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p, diseases d
WHERE p.botanical_name IN ('Oroxylum indicum','Gmelina arborea','Stereospermum suaveolens','Clerodendrum phlomidis','Desmodium gangeticum','Uraria picta')
  AND d.name_en IN ('Joint Inflammation / Shotha Pattern','Respiratory Congestion / Kasa-Shwasa Pattern');

-- Digestive fire / agnimandya mapping for dry ginger / peppers
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p, diseases d
WHERE p.botanical_name IN ('Zingiber officinale (dry)','Piper nigrum (fruit)','Piper longum (root)')
  AND d.name_en IN ('Poor Appetite / Agnimandya');

-- Krimi mapping for Vidanga fruit + existing intestinal worm disease (id=10)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, 10
FROM plants p
WHERE p.botanical_name IN ('Embelia ribes (fruit)');

-- Respiratory mapping for Bharangi-like (already inserted above as Bharangi Alt)
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, 12
FROM plants p
WHERE p.botanical_name IN ('Clerodendrum serratum');

-- Joint degeneration mapping for Rasna
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, 161
FROM plants p
WHERE p.botanical_name IN ('Pluchea lanceolata');

-- Urinary stones mapping for Varuna
INSERT OR IGNORE INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, 7
FROM plants p
WHERE p.botanical_name IN ('Crataeva nurvala');

-- =========================================================
-- E) PREPARATIONS: create primary-herb preparations for this batch (schema-accurate)
-- IMPORTANT: preparations.plant_id is NOT NULL
-- =========================================================

-- 1) Dashamoola Kvatha (primary herb: Shyonaka)
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Dashamoola Kvatha (Shyonaka-led)','दशमूल क्वाथ (श्योनक प्रधान)','दशमूळ क्वाथ (श्योनक प्रधान)',
'दशमूल क्वाथ','decoction','classical_formulation',
'1) Take coarse powder of Dashamoola group raw drugs as per availability (traditionally 10 roots). 2) Add 16 parts water. 3) Boil on mild flame till reduced to 1/4. 4) Filter warm. 5) Use fresh as per traditional practice.',
'["steel pot","stove","strainer","measuring cup"]',
'45–60 minutes','~250–300 ml','Use fresh; refrigerate if needed','24 hours (best fresh)',
'{"adult":{"dose_ml":"30-60","frequency_per_day":1},"child":{"dose_ml":"10-20","frequency_per_day":1},"notes":"adjust based on classical/clinical guidance"}',
'After food / as advised','Warm water / as advised','Warm decoction is preferred in kapha/vata patterns.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Oroxylum indicum');

-- 2) Gambhari Bark Decoction
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Gambhari Bark Decoction','गम्भारी छाल क्वाथ','गंभीर सालीचा क्वाथ',
'गम्भारी क्वाथ','decoction','single_herb',
'1) Take 10–15 g coarse bark. 2) Add 200–250 ml water. 3) Boil till ~1/4 remains. 4) Filter warm.',
'["steel pot","stove","strainer"]',
'30–45 minutes','~50–70 ml','Use fresh; refrigerate if required','24 hours (best fresh)',
'{"adult":{"dose_ml":"30-50","frequency_per_day":1},"notes":"traditional use; keep mild strength"}',
'After meals','Warm water','Keep decoction mild; avoid very concentrated boiling.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Gmelina arborea');

-- 3) Patala Kashaya
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Patala Kashaya','पाटला कषाय','पाटला काढा',
'पाटला कषाय','decoction','single_herb',
'1) Take 10 g coarse bark. 2) Add 200 ml water. 3) Simmer to ~50 ml. 4) Filter warm.',
'["steel pot","stove","strainer"]',
'30–45 minutes','~50 ml','Use fresh','24 hours (best fresh)',
'{"adult":{"dose_ml":"30-50","frequency_per_day":1}}',
'After food','Warm water','Traditional single-drug use; can be combined under guidance.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Stereospermum suaveolens');

-- 4) Agnimantha Root Decoction
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Agnimantha Root Decoction','अग्निमन्थ मूल क्वाथ','अग्निमंथ मुळ काढा',
'अग्निमन्थ क्वाथ','decoction','single_herb',
'1) Take 10 g coarse root/root-bark. 2) Add 200 ml water. 3) Boil to ~50 ml. 4) Filter.',
'["steel pot","stove","strainer"]',
'30–45 minutes','~50 ml','Use fresh','24 hours (best fresh)',
'{"adult":{"dose_ml":"30-50","frequency_per_day":1}}',
'After meals','Warm water','Traditionally used as deepana/shothahara support.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Clerodendrum phlomidis');

-- 5) Shalaparni Kashaya
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Shalaparni Kashaya','शालपर्णी कषाय','शालपर्णी काढा',
'शालपर्णी कषाय','decoction','single_herb',
'1) Take 10 g coarse root/whole plant. 2) Add 200 ml water. 3) Reduce to ~50 ml. 4) Filter warm.',
'["steel pot","stove","strainer"]',
'30–45 minutes','~50 ml','Use fresh','24 hours (best fresh)',
'{"adult":{"dose_ml":"30-50","frequency_per_day":1}}',
'After meals','Warm water','Classically used within Dashamoola; single use is traditional.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Desmodium gangeticum');

-- 6) Prishniparni Kashaya
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Prishniparni Kashaya','पृश्निपर्णी कषाय','पृश्निपर्णी काढा',
'पृश्निपर्णी कषाय','decoction','single_herb',
'1) Take 10 g coarse root/whole plant. 2) Add 200 ml water. 3) Reduce to ~50 ml. 4) Filter warm.',
'["steel pot","stove","strainer"]',
'30–45 minutes','~50 ml','Use fresh','24 hours (best fresh)',
'{"adult":{"dose_ml":"30-50","frequency_per_day":1}}',
'After meals','Warm water','Often combined in Dashamoola; keep strength moderate.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Uraria picta');

-- 7) Varuna Bark Decoction (mutrala support)
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Varuna Bark Decoction','वरुण छाल क्वाथ','वरुण सालीचा काढा',
'वरुण क्वाथ','decoction','single_herb',
'1) Take 10–15 g coarse bark. 2) Add 250 ml water. 3) Boil to ~60 ml. 4) Filter warm.',
'["steel pot","stove","strainer"]',
'35–50 minutes','~60 ml','Use fresh','24 hours (best fresh)',
'{"adult":{"dose_ml":"30-60","frequency_per_day":1},"notes":"traditional urinary support"}',
'Morning / as advised','Warm water','Traditional use in urinary patterns; hydration is important.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Crataeva nurvala');

-- 8) Rasna Decoction (vata support)
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Rasna Decoction','रस्ना कषाय','रस्ना काढा',
'रस्ना कषाय','decoction','single_herb',
'1) Take 10 g coarse root/leaf. 2) Add 200 ml water. 3) Reduce to ~50 ml. 4) Filter.',
'["steel pot","stove","strainer"]',
'30–45 minutes','~50 ml','Use fresh','24 hours (best fresh)',
'{"adult":{"dose_ml":"30-50","frequency_per_day":1}}',
'After meals','Warm water','Traditionally used for vata-related stiffness patterns.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Pluchea lanceolata');

-- 9) Vidanga Churna (single herb powder)
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Vidanga Churna','विडंग चूर्ण','विडंग चूर्ण',
'विडंग चूर्ण','powder','single_herb',
'1) Clean and shade-dry fruits. 2) Pulverize to fine powder. 3) Sieve and store airtight.',
'["grinder","sieve","airtight jar"]',
'30–60 minutes','As prepared','Airtight; cool dry place','3 months',
'{"adult":{"dose_g":"1-3","frequency_per_day":1},"notes":"traditional use for krimi tendency; follow guidance"}',
'After meals','Warm water / honey (as advised)','Keep dose low; follow classical/clinical guidance.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Embelia ribes (fruit)');

-- 10) Dry Ginger Infusion (simple)
INSERT OR IGNORE INTO preparations
(name_en, name_hi, name_mr, classical_name, form_type, category,
 preparation_steps, equipment_needed, duration, yield, storage, shelf_life,
 dosage_json, timing, anupana, notes, updated_at, ayush_system, plant_id)
SELECT
'Dry Ginger Infusion (Sonth)','सोंठ फांट','सुंठ फांट',
'शुण्ठी फाण्ट','infusion','single_herb',
'1) Add 1–2 g dry ginger powder to hot water. 2) Cover 5–10 minutes. 3) Strain if needed.',
'["cup","kettle"]',
'10 minutes','1 cup','Fresh only','Use immediately',
'{"adult":{"dose":"1 cup","frequency_per_day":1},"notes":"traditional digestive support"}',
'Morning / after meals','Warm water','Avoid overly strong infusion.','CURRENT_TIMESTAMP','ayurveda',
(SELECT id FROM plants WHERE botanical_name='Zingiber officinale (dry)');

COMMIT;
