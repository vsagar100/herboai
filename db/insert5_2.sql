-- insert5_2_homeopathy_mapping.sql
-- Wire 25 Homeopathy remedies → 12 homeopathy_* diseases

-- Helper comments:
-- HD1  homeopathy_trauma
-- HD2  homeopathy_psych_acute
-- HD3  homeopathy_fever_acute
-- HD4  homeopathy_respiratory_dry
-- HD5  homeopathy_musculoskeletal
-- HD6  homeopathy_digestive
-- HD7  homeopathy_psych_chronic
-- HD8  homeopathy_neurologic
-- HD9  homeopathy_dermatologic
-- HD10 homeopathy_respiratory_catarrh
-- HD11 homeopathy_skin_chronic
-- HD12 homeopathy_fever_lowgrade


-- Utility pattern:
-- INSERT INTO plant_disease_mapping (plant_id, disease_id)
-- SELECT p.id, d.id
-- FROM plants p
-- JOIN diseases d ON d.category = '...'
--                AND d.name_en = '...'
-- WHERE p.common_name_en = '...'
--   AND NOT EXISTS (
--     SELECT 1 FROM plant_disease_mapping m
--     WHERE m.plant_id = p.id AND m.disease_id = d.id
--   );


----------------------------------------------------------------
-- H1 Arnica → trauma, wound/slow healing
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_trauma'
 AND d.name_en = 'Homeopathic Bruise and Soft Tissue Injury'
WHERE p.common_name_en = 'Arnica'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_dermatologic'
 AND d.name_en = 'Homeopathic Local Wound and Slow Healing'
WHERE p.common_name_en = 'Arnica'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H2 Aconite → acute shock, high fever
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_psych_acute'
 AND d.name_en = 'Homeopathic Acute Shock and Fear Reaction'
WHERE p.common_name_en = 'Aconite'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_acute'
 AND d.name_en = 'Homeopathic High Fever with Throbbing Headache'
WHERE p.common_name_en = 'Aconite'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H3 Belladonna → high fever
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_acute'
 AND d.name_en = 'Homeopathic High Fever with Throbbing Headache'
WHERE p.common_name_en = 'Belladonna'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H4 Bryonia → dry painful cough, musculoskeletal
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_respiratory_dry'
 AND d.name_en = 'Homeopathic Dry Painful Cough and Chest Pain'
WHERE p.common_name_en = 'Bryonia'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_musculoskeletal'
 AND d.name_en = 'Homeopathic Joint Sprain and Stiffness'
WHERE p.common_name_en = 'Bryonia'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H5 Rhus Tox → joint stiffness, chronic skin eruption
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_musculoskeletal'
 AND d.name_en = 'Homeopathic Joint Sprain and Stiffness'
WHERE p.common_name_en = 'Rhus Tox'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_skin_chronic'
 AND d.name_en = 'Homeopathic Chronic Skin Eruption and Itching'
WHERE p.common_name_en = 'Rhus Tox'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H6 Nux Vomica → indigestion, low-grade fever/inflam tendency
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_digestive'
 AND d.name_en = 'Homeopathic Indigestion from Overeating and Stimulants'
WHERE p.common_name_en = 'Nux Vomica'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_lowgrade'
 AND d.name_en = 'Homeopathic Low-grade Fever and Inflammatory Tendency'
WHERE p.common_name_en = 'Nux Vomica'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H7 Pulsatilla → indigestion, sinus catarrh, emotional upset
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_digestive'
 AND d.name_en = 'Homeopathic Indigestion from Overeating and Stimulants'
WHERE p.common_name_en = 'Pulsatilla'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_respiratory_catarrh'
 AND d.name_en = 'Homeopathic Chronic Sinus Catarrh'
WHERE p.common_name_en = 'Pulsatilla'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_psych_chronic'
 AND d.name_en = 'Homeopathic Acute Grief and Emotional Upset'
WHERE p.common_name_en = 'Pulsatilla'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H8 Chamomilla → colic/indigestion, acute irritability/fear-like
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_digestive'
 AND d.name_en = 'Homeopathic Indigestion from Overeating and Stimulants'
WHERE p.common_name_en = 'Chamomilla'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_psych_acute'
 AND d.name_en = 'Homeopathic Acute Shock and Fear Reaction'
WHERE p.common_name_en = 'Chamomilla'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H9 Gelsemium → dull flu-like, low-grade fever / anticipatory anxiety
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_lowgrade'
 AND d.name_en = 'Homeopathic Low-grade Fever and Inflammatory Tendency'
WHERE p.common_name_en = 'Gelsemium'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_psych_acute'
 AND d.name_en = 'Homeopathic Acute Shock and Fear Reaction'
WHERE p.common_name_en = 'Gelsemium'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H10 Ignatia → acute grief/emotional upset
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_psych_chronic'
 AND d.name_en = 'Homeopathic Acute Grief and Emotional Upset'
WHERE p.common_name_en = 'Ignatia'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H11 Hypericum → nerve injury, trauma
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_neurologic'
 AND d.name_en = 'Homeopathic Nerve Injury and Shooting Pain'
WHERE p.common_name_en = 'Hypericum'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_trauma'
 AND d.name_en = 'Homeopathic Bruise and Soft Tissue Injury'
WHERE p.common_name_en = 'Hypericum'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H12 Calendula → local wound / slow healing
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_dermatologic'
 AND d.name_en = 'Homeopathic Local Wound and Slow Healing'
WHERE p.common_name_en = 'Calendula'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H13 Ruta → tendon/ligament strain, nerve injury
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_musculoskeletal'
 AND d.name_en = 'Homeopathic Joint Sprain and Stiffness'
WHERE p.common_name_en = 'Ruta'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_neurologic'
 AND d.name_en = 'Homeopathic Nerve Injury and Shooting Pain'
WHERE p.common_name_en = 'Ruta'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H14 Ledum → puncture/bite trauma, wound/skin
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_trauma'
 AND d.name_en = 'Homeopathic Bruise and Soft Tissue Injury'
WHERE p.common_name_en = 'Ledum'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_dermatologic'
 AND d.name_en = 'Homeopathic Local Wound and Slow Healing'
WHERE p.common_name_en = 'Ledum'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H15 Eupatorium perfoliatum → acute/high & low-grade fever aches
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_acute'
 AND d.name_en = 'Homeopathic High Fever with Throbbing Headache'
WHERE p.common_name_en = 'Eupatorium perfoliatum'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_lowgrade'
 AND d.name_en = 'Homeopathic Low-grade Fever and Inflammatory Tendency'
WHERE p.common_name_en = 'Eupatorium perfoliatum'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H16 Ferrum Phos → low-grade fever/inflammatory tendency
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_lowgrade'
 AND d.name_en = 'Homeopathic Low-grade Fever and Inflammatory Tendency'
WHERE p.common_name_en = 'Ferrum Phos'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H17 Kali Bichrom → chronic sinus catarrh
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_respiratory_catarrh'
 AND d.name_en = 'Homeopathic Chronic Sinus Catarrh'
WHERE p.common_name_en = 'Kali Bichrom'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H18 Natrum Mur → chronic skin, grief/emotional pattern
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_skin_chronic'
 AND d.name_en = 'Homeopathic Chronic Skin Eruption and Itching'
WHERE p.common_name_en = 'Natrum Mur'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_psych_chronic'
 AND d.name_en = 'Homeopathic Acute Grief and Emotional Upset'
WHERE p.common_name_en = 'Natrum Mur'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H19 Sulphur → chronic skin eruption
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_skin_chronic'
 AND d.name_en = 'Homeopathic Chronic Skin Eruption and Itching'
WHERE p.common_name_en = 'Sulphur'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H20 Hepar Sulph → suppurative / infected lesions, sinus catarrh
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_dermatologic'
 AND d.name_en = 'Homeopathic Local Wound and Slow Healing'
WHERE p.common_name_en = 'Hepar Sulph'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_respiratory_catarrh'
 AND d.name_en = 'Homeopathic Chronic Sinus Catarrh'
WHERE p.common_name_en = 'Hepar Sulph'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H21 Lycopodium → gas/indigestion, sinus catarrh
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_digestive'
 AND d.name_en = 'Homeopathic Indigestion from Overeating and Stimulants'
WHERE p.common_name_en = 'Lycopodium'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_respiratory_catarrh'
 AND d.name_en = 'Homeopathic Chronic Sinus Catarrh'
WHERE p.common_name_en = 'Lycopodium'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H22 Sepia → pelvic/hormonal mood patterns → psych_chronic, skin
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_psych_chronic'
 AND d.name_en = 'Homeopathic Acute Grief and Emotional Upset'
WHERE p.common_name_en = 'Sepia'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_skin_chronic'
 AND d.name_en = 'Homeopathic Chronic Skin Eruption and Itching'
WHERE p.common_name_en = 'Sepia'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H23 Silicea → slow healing, chronic skin
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_dermatologic'
 AND d.name_en = 'Homeopathic Local Wound and Slow Healing'
WHERE p.common_name_en = 'Silicea'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_skin_chronic'
 AND d.name_en = 'Homeopathic Chronic Skin Eruption and Itching'
WHERE p.common_name_en = 'Silicea'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H24 Arsenicum Album → GI upset, skin, low-grade fever/anxiety
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_digestive'
 AND d.name_en = 'Homeopathic Indigestion from Overeating and Stimulants'
WHERE p.common_name_en = 'Arsenicum Album'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_skin_chronic'
 AND d.name_en = 'Homeopathic Chronic Skin Eruption and Itching'
WHERE p.common_name_en = 'Arsenicum Album'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_lowgrade'
 AND d.name_en = 'Homeopathic Low-grade Fever and Inflammatory Tendency'
WHERE p.common_name_en = 'Arsenicum Album'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );


----------------------------------------------------------------
-- H25 Carbo Veg → gas/flatulence with collapse-like weakness, low-grade
----------------------------------------------------------------
INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_digestive'
 AND d.name_en = 'Homeopathic Indigestion from Overeating and Stimulants'
WHERE p.common_name_en = 'Carbo Veg'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );

INSERT INTO plant_disease_mapping (plant_id, disease_id)
SELECT p.id, d.id
FROM plants p
JOIN diseases d
  ON d.category = 'homeopathy_fever_lowgrade'
 AND d.name_en = 'Homeopathic Low-grade Fever and Inflammatory Tendency'
WHERE p.common_name_en = 'Carbo Veg'
  AND NOT EXISTS (
    SELECT 1 FROM plant_disease_mapping m
    WHERE m.plant_id = p.id AND m.disease_id = d.id
  );
