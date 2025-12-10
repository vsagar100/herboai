-- insert5_1_homeopathy_diseases_fixed.sql

-- 1) Remove any previous homeopathy_* diseases
DELETE FROM diseases
WHERE category LIKE 'homeopathy_%';

-- 2) Insert Homeopathy-specific diseases with schema-compliant JSON

INSERT INTO diseases (
  name_en,
  name_hi,
  name_mr,
  category,
  ayurvedic_name,
  unani_name,
  siddha_name,
  description,
  symptoms,
  causes,
  dosha_involvement,
  dhatu_involvement,
  severity_level,
  is_lifestyle_related,
  prevention_tips,
  dietary_recommendations
) VALUES
-- HD1: Trauma / bruises
(
 'Homeopathic Bruise and Soft Tissue Injury',
 'होम्योपैथिक चोट और नरम ऊतक की सूजन',
 'होमिओपॅथिक मऊ ऊतक दुखापत आणि सूज',
 'homeopathy_trauma',
 NULL, NULL, NULL,
 'Soft tissue trauma with bruising and soreness where homeopathic trauma remedies are often considered as supportive.',
 '["bruising","soreness","stiffness","pain_after_fall_or_overexertion"]',
 '["sports_injury","domestic_fall","minor_accident","overexertion"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'mild',
 1,
 '["use_protective_gear","warm_up_before_exercise","avoid_slippery_or_unsafe_surfaces"]',
 '["adequate_protein_intake","good_hydration","balanced_meals_for_tissue_repair"]'
),

-- HD2: Acute shock and fear
(
 'Homeopathic Acute Shock and Fear Reaction',
 'होम्योपैथिक तीव्र घबराहट और डर प्रतिक्रिया',
 'होमिओपॅथिक अचानक भीती आणि धक्का प्रतिक्रिया',
 'homeopathy_psych_acute',
 NULL, NULL, NULL,
 'Short-lasting intense fear or shock with restlessness and anxiety.',
 '["sudden_panic","racing_heart","restlessness","sense_of_dread"]',
 '["accident","frightening_event","sudden_bad_news"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'moderate',
 1,
 '["learn_breathing_exercises","seek_emotional_support","consult_professional_if_persistent"]',
 '["light_easily_digested_food","avoid_excess_caffeine","maintain_regular_small_meals"]'
),

-- HD3: High fever / throbbing
(
 'Homeopathic High Fever with Throbbing Headache',
 'होम्योपैथिक तेज बुखार और धड़कता सिरदर्द',
 'होमिओपॅथिक जास्त ताप आणि ठणकणारा डोकेदुखी',
 'homeopathy_fever_acute',
 NULL, NULL, NULL,
 'Acute high fever with flushed face, throbbing headache and sensitivity to light or noise.',
 '["high_fever","throbbing_headache","red_face","sensitivity_to_light","sensitivity_to_noise"]',
 '["viral_infection","bacterial_infection","acute_inflammatory_illness"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'severe',
 0,
 '["seek_early_medical_assessment","maintain_good_hygiene","follow_vaccination_guidelines"]',
 '["adequate_fluids_like_water_soups_ors","light_easily_digestible_food_if_appetite"]'
),

-- HD4: Dry painful cough / pleuritic pain
(
 'Homeopathic Dry Painful Cough and Chest Pain',
 'होम्योपैथिक सूखी दर्दनाक खांसी और सीने में दर्द',
 'होमिओपॅथिक कोरडा दुखरी खोकला आणि छातीत वेदना',
 'homeopathy_respiratory_dry',
 NULL, NULL, NULL,
 'Dry painful cough and chest pain worse from movement or deep breathing.',
 '["dry_hacking_cough","sharp_chest_pain","pain_on_deep_breathing","pain_worse_by_movement"]',
 '["respiratory_infection","pleuritic_irritation","overuse_of_voice","irritant_exposure"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'moderate',
 0,
 '["avoid_smoking","reduce_pollutant_exposure","seek_medical_opinion_if_persistent"]',
 '["warm_fluids","avoid_very_cold_drinks","limit_heavily_spicy_or_oily_food"]'
),

-- HD5: Joint sprain / stiffness
(
 'Homeopathic Joint Sprain and Stiffness',
 'होम्योपैथिक मोच और जोड़ की जकड़न',
 'होमिओपॅथिक मुरगळणे आणि सांध्यातील कडकपणा',
 'homeopathy_musculoskeletal',
 NULL, NULL, NULL,
 'Joint and periarticular sprain or strain with stiffness, often better from gentle motion.',
 '["sprain","joint_swelling","morning_stiffness","pain_on_starting_movement","relief_on_gentle_motion"]',
 '["sports_overuse","sudden_wrong_movement","incorrect_lifting","poor_ergonomics"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'mild',
 1,
 '["do_proper_warm_up","maintain_good_ergonomics","avoid_sudden_heavy_loads"]',
 '["balanced_diet_with_protein","adequate_calcium_and_vitamin_d","maintain_healthy_weight"]'
),

-- HD6: Indigestion from overeating / stimulants
(
 'Homeopathic Indigestion from Overeating and Stimulants',
 'होम्योपैथिक अपच (अधिक भोजन और उत्तेजक से)',
 'होमिओपॅथिक अपचन (जास्त खाणे आणि उत्तेजकांमुळे)',
 'homeopathy_digestive',
 NULL, NULL, NULL,
 'Digestive upset from rich food, late-night meals, coffee or alcohol overuse.',
 '["heaviness_in_stomach","bloating","gas","heartburn","irritability_after_meals"]',
 '["rich_spicy_food","late_night_eating","excess_coffee","alcohol_overuse","stress_eating"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'mild',
 1,
 '["adopt_regular_meal_timing","limit_stimulants_and_alcohol","avoid_very_heavy_late_dinners"]',
 '["prefer_light_less_oily_less_spicy_meals","maintain_good_hydration","include_fiber_in_diet"]'
),

-- HD7: Acute grief / emotional upset
(
 'Homeopathic Acute Grief and Emotional Upset',
 'होम्योपैथिक तीव्र शोक और भावनात्मक तनाव',
 'होमिओपॅथिक तीव्र दु:ख आणि भावनिक ताण',
 'homeopathy_psych_chronic',
 NULL, NULL, NULL,
 'Recent bereavement or strong emotional shock with sighing, sobbing and mood swings.',
 '["crying_spells","lump_in_throat_sensation","mood_swings","sleep_disturbance","loss_of_appetite"]',
 '["bereavement","relationship_breakup","sudden_life_change","acute_emotional_shock"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'moderate',
 1,
 '["seek_emotional_and_social_support","consider_counseling_if_needed","practice_relaxation_or_mindfulness"]',
 '["regular_small_meals","adequate_fluids","avoid_using_alcohol_or_junk_food_for_coping"]'
),

-- HD8: Nerve injury pain
(
 'Homeopathic Nerve Injury and Shooting Pain',
 'होम्योपैथिक नसों की चोट और चुभन वाला दर्द',
 'होमिओपॅथिक नस दुखापत आणि झटका देणारी वेदना',
 'homeopathy_neurologic',
 NULL, NULL, NULL,
 'Pain in areas rich in nerves after crush injuries or surgery with radiating, shooting character.',
 '["sharp_shooting_pain","tingling","burning_sensation","sensitivity_at_fingertips_or_spine"]',
 '["trauma","surgery","repetitive_strain","nerve_entrapment"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'moderate',
 0,
 '["protect_affected_area","follow_physio_or_rehab_programs","avoid_repetitive_strain"]',
 '["nourishing_balanced_diet","avoid_smoking","avoid_excess_alcohol"]'
),

-- HD9: Local wound / slow healing
(
 'Homeopathic Local Wound and Slow Healing',
 'होम्योपैथिक घाव और धीमी भरपाई',
 'होमिओपॅथिक जखम आणि हळू भरून येणे',
 'homeopathy_dermatologic',
 NULL, NULL, NULL,
 'Shallow wounds, cuts or abrasions that are slow to heal or tend to inflame.',
 '["persistent_soreness","delayed_healing","mild_discharge","local_redness"]',
 '["repeated_trauma","local_infection","poor_local_care","underlying_diabetes_or_anemia"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'moderate',
 1,
 '["maintain_wound_hygiene","protect_from_friction","control_diabetes_and_anemia"]',
 '["protein_rich_foods","adequate_vitamins_and_minerals","avoid_smoking_to_support_healing"]'
),

-- HD10: Chronic sinus catarrh
(
 'Homeopathic Chronic Sinus Catarrh',
 'होम्योपैथिक जीर्ण साइनस नज़ला',
 'होमिओपॅथिक जुनाट सायनस नजला',
 'homeopathy_respiratory_catarrh',
 NULL, NULL, NULL,
 'Chronic sinus complaints with thick, stringy mucus and post-nasal drip.',
 '["headache","facial_pressure","sticky_nasal_discharge","post_nasal_drip","recurrent_cough"]',
 '["allergy","repeated_sinus_infections","structural_nasal_issues","irritant_exposure"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'chronic',
 1,
 '["avoid_smoking_and_pollution","manage_allergies","use_steam_inhalation_if_advised"]',
 '["simple_less_processed_diet","adequate_warm_fluids","limit_very_cold_food_and_drinks"]'
),

-- HD11: Chronic skin eruptions / itching
(
 'Homeopathic Chronic Skin Eruption and Itching',
 'होम्योपैथिक पुरानी त्वचा विकृति और खुजली',
 'होमिओपॅथिक जुनाट त्वचा विकार आणि खाज',
 'homeopathy_skin_chronic',
 NULL, NULL, NULL,
 'Longstanding superficial skin eruptions with itching and burning in constitutional cases.',
 '["itchy_rash","dryness_or_oozing","recurrent_flare_ups","worse_from_heat_in_some_people"]',
 '["genetic_tendency","irritant_exposure","allergen_exposure","metabolic_imbalance","stress"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'chronic',
 1,
 '["avoid_harsh_soaps_and_detergents","avoid_known_allergens","keep_skin_moisturized"]',
 '["simple_less_processed_food","adequate_water_intake","maintain_healthy_weight_and_metabolic_control"]'
),

-- HD12: Low-grade fever / inflammatory tendency
(
 'Homeopathic Low-grade Fever and Inflammatory Tendency',
 'होम्योपैथिक कम दर्ज़े का बुखार और सूजन प्रवृत्ति',
 'होमिओपॅथिक सौम्य ताप आणि दाह प्रवृत्ती',
 'homeopathy_fever_lowgrade',
 NULL, NULL, NULL,
 'Recurrent low-grade fever or early inflammatory states where tissue salts and supportive remedies are sometimes considered.',
 '["recurrent_low_grade_fever","fatigue","vague_body_aches","early_local_redness_or_swelling"]',
 '["chronic_low_grade_infection","autoimmune_process","post_viral_state","poor_recovery_from_illness"]',
 '["not_tagged_for_homeopathy"]',
 '["not_tagged_for_homeopathy"]',
 'chronic',
 0,
 '["ensure_full_medical_evaluation","allow_adequate_rest","manage_stress_and_sleep"]',
 '["nutritious_diet_with_enough_protein","adequate_micronutrients","follow_medical_dietary_guidance_if_given"]'
);


-- Common columns:
-- name_en, name_hi, name_mr,
-- classical_name, form_type, category,
-- preparation_steps, equipment_needed, duration, yield,
-- storage, shelf_life, dosage_json, timing, anupana, notes,
-- ayush_system, plant_id

-- HP1 Arnica 30C oral globules
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
)
SELECT
  'Arnica 30C Oral Globules',
  'आर्निका 30C गोलियां',
  'आर्निका 30C गोळ्या',
  'Arnica montana 30C',
  'globules',
  'trauma_and_bruise_support',
  'Prepared industrially as per homeopathic pharmacopeia; in practice patient takes medicated sugar globules as per physician advice.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Store in cool, dry, dark place, away from strong odours.',
  '3–5_years',
  '{"adult":"3–5 globules once or twice daily as advised by homeopathic physician","child":"lower dose as advised"}',
  'as_directed_by_physician',
  'none',
  'Used as a classic homeopathic trauma remedy for bruises and soreness in appropriate indications.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Arnica'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Arnica 30C Oral Globules');

-- HP2 Aconite 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Aconite 30C Oral Globules',
  'एकोनाइट 30C गोलियां',
  'एकोनाइट 30C गोळ्या',
  'Aconitum napellus 30C',
  'globules',
  'acute_shock_and_fear_support',
  'Prepared industrially in high dilution following homeopathic standards.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Store cool, dry, away from sunlight.',
  '3–5_years',
  '{"adult":"3–5 globules in acute phase as advised","child":"only under physician supervision"}',
  'as_directed_by_physician',
  'none',
  'Traditionally considered in very early sudden fear and shock states.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Aconite'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Aconite 30C Oral Globules');

-- HP3 Belladonna 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Belladonna 30C Oral Globules',
  'बेलाडोना 30C गोलियां',
  'बेलाडोना 30C गोळ्या',
  'Belladonna 30C',
  'globules',
  'high_fever_and_throbbing_support',
  'Industrial preparation in homeopathic potency; used only under professional guidance.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Away from heat and moisture.',
  '3–5_years',
  '{"adult":"dose pattern as advised by physician","child":"only under expert advice"}',
  'as_directed_by_physician',
  'none',
  'Used in homeopathy for sudden high fever with throbbing patterns when indicated.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Belladonna'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Belladonna 30C Oral Globules');

-- HP4 Bryonia 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Bryonia 30C Oral Globules',
  'ब्रायोनिया 30C गोलियां',
  'ब्रायोनिया 30C गोळ्या',
  'Bryonia alba 30C',
  'globules',
  'dry_painful_cough_and_serous_inflammation',
  'Standard homeopathic globule preparation; dose only as prescribed.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Keep sealed, cool and dry.',
  '3–5_years',
  '{"adult":"3–5 globules as per homeopathic schedule","child":"dose under pediatric homeopath"}',
  'as_directed_by_physician',
  'none',
  'Considered in dry cough or pleuritic-type pains worse by movement in homeopathic practice.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Bryonia'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Bryonia 30C Oral Globules');

-- HP5 Rhus Tox 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Rhus Tox 30C Oral Globules',
  'रूस टॉक्स 30C गोलियां',
  'रूस टॉक्स 30C गोळ्या',
  'Rhus toxicodendron 30C',
  'globules',
  'joint_sprain_and_stiffness_support',
  'Prepared as medicated globules for oral use in standard homeopathic potencies.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Store at room temperature, away from humidity.',
  '3–5_years',
  '{"adult":"typical regimen is a few globules per dose as individualized","child":"reduced dose under guidance"}',
  'as_directed_by_physician',
  'none',
  'Used when joint stiffness and sprain pains improve on gentle motion in homeopathic tradition.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Rhus Tox'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Rhus Tox 30C Oral Globules');

-- HP6 Nux Vomica 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Nux Vomica 30C Oral Globules',
  'नक्स वोमिका 30C गोलियां',
  'नक्स वोमिका 30C गोळ्या',
  'Nux vomica 30C',
  'globules',
  'overeating_and_stimulant_indigestion_support',
  'Globules medicated with Nux vomica 30C as per pharmacopoeia.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Keep well closed, protect from strong odours.',
  '3–5_years',
  '{"adult":"few globules per dose as prescribed, usually not self-prescribed in chronic cases","child":"only if physician prescribes"}',
  'as_directed_by_physician',
  'none',
  'Used in homeopathy for indigestion and irritability from rich food and stimulants when indicated.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Nux Vomica'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Nux Vomica 30C Oral Globules');

-- HP7 Pulsatilla 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Pulsatilla 30C Oral Globules',
  'पल्सेटिला 30C गोलियां',
  'पल्सेटिला 30C गोळ्या',
  'Pulsatilla nigricans 30C',
  'globules',
  'digestive_and_menstrual_support_changeable',
  'Prepared as standard homeopathic globules.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Dry, odour-free storage.',
  '3–5_years',
  '{"adult":"dose and repetition individualized by physician","child":"reduced dose only under guidance"}',
  'as_directed_by_physician',
  'none',
  'Traditionally used in changeable symptom pictures, fatty-food aggravation and certain menstrual complaints.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Pulsatilla'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Pulsatilla 30C Oral Globules');

-- HP8 Chamomilla 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Chamomilla 30C Oral Globules',
  'कैमोमिला 30C गोलियां',
  'कॅमोमिला 30C गोळ्या',
  'Chamomilla 30C',
  'globules',
  'pediatric_colic_and_pain_sensitivity_support',
  'Homeopathic globules prepared from Chamomilla in 30C potency.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Away from heat and contamination.',
  '3–5_years',
  '{"adult":"few globules if indicated","child":"dose strictly as guided by pediatric homeopath"}',
  'as_directed_by_physician',
  'none',
  'Used for colicky pains with extreme irritability in homeopathic practice.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Chamomilla'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Chamomilla 30C Oral Globules');

-- HP9 Gelsemium 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Gelsemium 30C Oral Globules',
  'जेल्सेमियम 30C गोलियां',
  'जेल्सेमियम 30C गोळ्या',
  'Gelsemium sempervirens 30C',
  'globules',
  'dull_flu_like_and_anticipatory_anxiety_support',
  'Standard homeopathic globule preparation taken as per practitioner advice.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Store cool, dry.',
  '3–5_years',
  '{"adult":"3–5 globules per dose as advised","child":"smaller dose as per pediatric advice"}',
  'as_directed_by_physician',
  'none',
  'Used in homeopathy for dull heavy flu-like states and anticipatory anxiety.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Gelsemium'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Gelsemium 30C Oral Globules');

-- HP10 Ignatia 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Ignatia 30C Oral Globules',
  'इगनेशिया 30C गोलियां',
  'इगनेशिया 30C गोळ्या',
  'Ignatia amara 30C',
  'globules',
  'acute_grief_and_emotional_support',
  'Globules medicated with Ignatia 30C for use under professional guidance.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Protected from direct sunlight and odours.',
  '3–5_years',
  '{"adult":"few globules per dose in acute emotional events if prescribed","child":"only under physician guidance"}',
  'as_directed_by_physician',
  'none',
  'Used in acute grief or emotional shock patterns in homeopathic tradition.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Ignatia'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Ignatia 30C Oral Globules');

-- HP11 Hypericum 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Hypericum 30C Oral Globules',
  'हाइपेरिकम 30C गोलियां',
  'हायपेरिकम 30C गोळ्या',
  'Hypericum perforatum 30C',
  'globules',
  'nerve_injury_pain_support',
  'Homeopathic globules prepared from Hypericum in 30C potency.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Cool, dry storage.',
  '3–5_years',
  '{"adult":"dose individualized by practitioner","child":"only on expert advice"}',
  'as_directed_by_physician',
  'none',
  'Considered for nerve-rich trauma pains in homeopathic use.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Hypericum'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Hypericum 30C Oral Globules');

-- HP12 Calendula external mother tincture
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Calendula External Lotion (Mother Tincture Dilution)',
  'कैलेंडुला बाह्य लोशन',
  'कॅलेंडुला बाह्य लोशन',
  'Calendula officinalis Q (external use)',
  'mother_tincture_dilution',
  'wound_and_skin_support_external',
  'Mother tincture is diluted with clean water or base as advised and used externally only on closed or appropriately cleaned wounds.',
  'measuring_cup;clean_container',
  'few_minutes_to_prepare_dilution',
  'small_lotion_volume',
  'Use freshly prepared dilution; discard remainder after short time.',
  '1_day_for_dilution',
  '{"adult":"external application only as directed","child":"under medical supervision only"}',
  'external_use_only',
  'none',
  'Commonly used externally in homeopathy as local support for wound healing.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Calendula'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Calendula External Lotion (Mother Tincture Dilution)');

-- HP13 Ruta 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Ruta 30C Oral Globules',
  'रूटा 30C गोलियां',
  'रूटा 30C गोळ्या',
  'Ruta graveolens 30C',
  'globules',
  'tendon_and_ligament_strain_support',
  'Globules medicated with Ruta 30C as per pharmacopeia.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Keep dry and odour-free.',
  '3–5_years',
  '{"adult":"3–5 globules per dose as advised","child":"reduced dose under guidance"}',
  'as_directed_by_physician',
  'none',
  'Used for tendon and ligament strains and eye strain in homeopathic practice.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Ruta'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Ruta 30C Oral Globules');

-- HP14 Ledum 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Ledum 30C Oral Globules',
  'लेडम 30C गोलियां',
  'लेडम 30C गोळ्या',
  'Ledum palustre 30C',
  'globules',
  'puncture_wound_and_bite_support',
  'Standard homeopathic globule form of Ledum.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Dry, cool storage.',
  '3–5_years',
  '{"adult":"few globules per dose as scheduled","child":"only under practitioner oversight"}',
  'as_directed_by_physician',
  'none',
  'Used in homeopathy for puncture wounds and insect bites when clinically appropriate.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Ledum'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Ledum 30C Oral Globules');

-- HP15 Eupatorium perfoliatum 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Eupatorium perfoliatum 30C Globules',
  'यूफेटोरियम पेरफोलिएटम 30C गोलियां',
  'युफॅटोरियम पेरफोलिएटम 30C गोळ्या',
  'Eupatorium perfoliatum 30C',
  'globules',
  'bony_ache_fever_support',
  'Homeopathic globules prepared from Eupatorium perfoliatum.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Store closed, away from humidity.',
  '3–5_years',
  '{"adult":"few globules per dose when prescribed","child":"lower dose only under physician"}',
  'as_directed_by_physician',
  'none',
  'Used where flu-like states with intense bone pain are present in homeopathic indications.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Eupatorium perfoliatum'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Eupatorium perfoliatum 30C Globules');

-- HP16 Ferrum Phos 6X (tissue salt)
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Ferrum Phos 6X Tablets',
  'फेरम फॉस 6X टेबलेट',
  'फेरम फॉस 6X गोळ्या',
  'Ferrum phosphoricum 6X (tissue salt)',
  'trituration_tablet',
  'low_grade_fever_and_anemia_support',
  'Prepared as lactose-based tablets containing Ferrum phosphoricum 6X in accordance with homeopathic tissue salt standards.',
  'tablet_press_unit',
  'industrial',
  'bottle',
  'Keep well-sealed, away from moisture.',
  '3–5_years',
  '{"adult":"1–4 tablets per day divided as advised","child":"lower frequency as guided"}',
  'throughout_day_as_directed',
  'none',
  'Used as supportive tissue salt in low-grade inflammatory states and mild anemia tendency (not a replacement for medical treatment).',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Ferrum Phos'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Ferrum Phos 6X Tablets');

-- HP17 Kali Bichrom 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Kali Bichrom 30C Oral Globules',
  'काली बाइक्रोम 30C गोलियां',
  'काली बायक्रोम 30C गोळ्या',
  'Kalium bichromicum 30C',
  'globules',
  'chronic_sinus_catarrh_support',
  'Globules doped with Kali bichromicum 30C.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Store cool, dry.',
  '3–5_years',
  '{"adult":"few globules per dose as part of individualized plan","child":"only if physician prescribes"}',
  'as_directed_by_physician',
  'none',
  'Used in homeopathy for thick stringy mucus and sinus catarrh pictures.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Kali Bichrom'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Kali Bichrom 30C Oral Globules');

-- HP18 Natrum Mur 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Natrum Mur 30C Oral Globules',
  'नैट्रम म्यूर 30C गोलियां',
  'नॅट्रम म्यूर 30C गोळ्या',
  'Natrium muriaticum 30C',
  'globules',
  'headache_and_grief_pattern_support',
  'Standard homeopathic Natrum mur 30C globules.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Dry and odour-free storage.',
  '3–5_years',
  '{"adult":"3–5 globules per dose as advised","child":"lower dose pattern"}',
  'as_directed_by_physician',
  'none',
  'Used for chronic headache and grief-tendency states in homeopathic tradition.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Natrum Mur'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Natrum Mur 30C Oral Globules');

-- HP19 Sulphur 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Sulphur 30C Oral Globules',
  'सल्फर 30C गोलियां',
  'सल्फर 30C गोळ्या',
  'Sulphur 30C',
  'globules',
  'chronic_skin_eruption_support',
  'Homeopathic globules made from Sulphur 30C potency.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Cool, odour-free place.',
  '3–5_years',
  '{"adult":"few globules as per constitutional plan","child":"only under specialist guidance"}',
  'as_directed_by_physician',
  'none',
  'Used as a constitutional remedy for chronic skin and heat patterns when indicated.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Sulphur'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Sulphur 30C Oral Globules');

-- HP20 Hepar Sulph 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Hepar Sulph 30C Oral Globules',
  'हेपर सल्फ 30C गोलियां',
  'हेपर सल्फ 30C गोळ्या',
  'Hepar sulphuris calcareum 30C',
  'globules',
  'suppurative_tendency_support',
  'Globules medicated with Hepar sulph in 30C potency.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Store in closed container away from strong odours.',
  '3–5_years',
  '{"adult":"dose and repetition individualized by doctor","child":"lower dose as advised"}',
  'as_directed_by_physician',
  'none',
  'Used in homeopathy for painful inflamed lesions with tendency to suppurate.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Hepar Sulph'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Hepar Sulph 30C Oral Globules');

-- HP21 Lycopodium 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Lycopodium 30C Oral Globules',
  'लायकॉपोडियम 30C गोलियां',
  'लायकॉपोडियम 30C गोळ्या',
  'Lycopodium clavatum 30C',
  'globules',
  'gas_and_digestive_anxiety_support',
  'Globules medicated with Lycopodium 30C.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Dry, room-temperature storage.',
  '3–5_years',
  '{"adult":"few globules per dose in chronic work planned by physician","child":"pediatric guidance only"}',
  'as_directed_by_physician',
  'none',
  'Used for bloating, gas and anticipatory anxiety patterns in homeopathic practice.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Lycopodium'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Lycopodium 30C Oral Globules');

-- HP22 Sepia 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Sepia 30C Oral Globules',
  'सेपिया 30C गोलियां',
  'सेपिया 30C गोळ्या',
  'Sepia officinalis 30C',
  'globules',
  'pelvic_and_hormonal_mood_support',
  'Homeopathic Sepia 30C globules.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Keep tightly closed, away from heat.',
  '3–5_years',
  '{"adult":"few globules per dose in individualized prescriptions","child":"rarely used and only under specialist care"}',
  'as_directed_by_physician',
  'none',
  'Used in specific pelvic and mood patterns in homeopathic tradition.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Sepia'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Sepia 30C Oral Globules');

-- HP23 Silicea 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Silicea 30C Oral Globules',
  'सिलिसिया 30C गोलियां',
  'सिलिसिया 30C गोळ्या',
  'Silicea terra 30C',
  'globules',
  'slow_healing_and_connective_tissue_support',
  'Standard Silicea 30C globules as per homeopathic standards.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Cool, dry storage.',
  '3–5_years',
  '{"adult":"dose and repetition per constitutional plan","child":"only under professional guidance"}',
  'as_directed_by_physician',
  'none',
  'Used in slow-healing, chronic suppuration and tissue weakness pictures.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Silicea'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Silicea 30C Oral Globules');

-- HP24 Arsenicum Album 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Arsenicum Album 30C Oral Globules',
  'आर्सेनिकम एल्बम 30C गोलियां',
  'आर्सेनिकम अल्बम 30C गोळ्या',
  'Arsenicum album 30C',
  'globules',
  'anxiety_restlessness_and_gi_support',
  'Industrial preparation of Arsenicum album 30C globules.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Store away from heat and direct sunlight.',
  '3–5_years',
  '{"adult":"few globules per dose as part of individualized treatment","child":"only under physician"}',
  'as_directed_by_physician',
  'none',
  'Used for anxiety with restlessness and digestive irritation patterns in homeopathic practice.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Arsenicum Album'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Arsenicum Album 30C Oral Globules');

-- HP25 Carbo Veg 30C
INSERT INTO preparations (
  name_en, name_hi, name_mr,
  classical_name, form_type, category,
  preparation_steps, equipment_needed, duration, yield,
  storage, shelf_life, dosage_json, timing, anupana, notes,
  ayush_system, plant_id
) 
SELECT
  'Carbo Veg 30C Oral Globules',
  'कार्बो वेज 30C गोलियां',
  'कार्बो वेज 30C गोळ्या',
  'Carbo vegetabilis 30C',
  'globules',
  'gas_collapse_like_weakness_support',
  'Globules medicated with Carbo veg 30C potency.',
  'homeopathic_manufacturing_unit',
  'industrial',
  'bottle',
  'Keep tightly closed, cool and dry.',
  '3–5_years',
  '{"adult":"few globules per dose when indicated","child":"dose under pediatric homeopath"}',
  'as_directed_by_physician',
  'none',
  'Used in homeopathy for flatulence with exhaustion and low vitality states needing fresh air.',
  'homeopathy',
  p.id
FROM plants p
WHERE p.common_name_en = 'Carbo Veg'
  AND NOT EXISTS (SELECT 1 FROM preparations WHERE name_en = 'Carbo Veg 30C Oral Globules');

