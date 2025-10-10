PRAGMA foreign_keys = OFF;
BEGIN IMMEDIATE;

-- 1) Drop FTS tables if you created them (optional; ignore errors)
DROP TABLE IF EXISTS plant_fts;
DROP TABLE IF EXISTS remedy_fts;

-- 2) Clear dependents first
DELETE FROM image;
DELETE FROM remedy;

-- 3) Clear plants/admin
DELETE FROM plant;
DELETE FROM admin_user WHERE username = 'admin';

-- 4) (Only if your tables use AUTOINCREMENT) reset sequences
-- If your DDL is just INTEGER PRIMARY KEY (no AUTOINCREMENT), this is harmless.
DELETE FROM sqlite_sequence WHERE name IN ('plant','image','remedy','admin_user');

COMMIT;
PRAGMA foreign_keys = ON;

-- 5) Now insert fresh data (IDs 1..10) — same content you tried before
BEGIN TRANSACTION;

/* Admin (dummy hash; replace later) */
INSERT INTO admin_user (id, username, password_hash)
VALUES (1, 'admin', 'pbkdf2:sha256:260000$demo$hash_here');

INSERT INTO plant (id, name, scientific_name, ayush_system, category, synonyms, parts_used,
  uses, phytochemicals, dosage, contraindications, formulations,
  languages_json, description, properties, created_at, updated_at
) VALUES
(1, 'Tulsi', 'Ocimum sanctum', 'Ayurveda', 'Respiratory', 'Holy Basil, तुलसी, तुळस',
 '["Leaves","Stem"]','Used for cough, cold, fever, immunity boost.',
 'Eugenol, Ursolic acid','Decoction 150ml twice daily after meals',
 'Avoid during pregnancy without doctor advice.','Tea, Kashaya (Decoction)',
 '{"hi":{"name":"तुलसी","uses":"खांसी, जुकाम, बुखार"},"mr":{"name":"तुळस","uses":"खोकला, सर्दी, ताप"}}',
 'Aromatic shrub widely used in Ayurveda.','Antipyretic, Immunomodulator',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(2, 'Ashwagandha', 'Withania somnifera', 'Ayurveda', 'Rejuvenative', 'Indian Ginseng, अश्वगंधा',
 '["Root"]','Improves strength, stamina, stress relief.','Withanolides, Alkaloids',
 'Powder 3-5g with milk once daily.','Avoid in hyperthyroidism.','Churna, Tablet','{}',
 'A key adaptogen in Ayurveda.','Adaptogenic, Nervine tonic',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(3, 'Neem', 'Azadirachta indica', 'Ayurveda', 'Skin and Detox', 'Margosa, नीम, कडुनिंब',
 '["Leaves","Bark","Oil"]','Treats skin disorders, purifies blood, insect repellant.',
 'Azadirachtin, Nimbin','Juice 10ml twice a day.','Avoid during pregnancy.','Oil, Juice, Decoction','{}',
 'Broad-spectrum herbal purifier.','Antimicrobial, Blood purifier',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(4, 'Amla', 'Phyllanthus emblica', 'Ayurveda', 'Digestive', 'Indian Gooseberry, आँवला, आवळा',
 '["Fruit"]','Improves digestion, eye health, hair growth.','Vitamin C, Gallic acid',
 '10–20 ml juice daily.','Avoid in acidity.','Chyawanprash, Rasayanas','{}',
 'Rich source of Vitamin C used in Chyawanprash.','Rejuvenative, Antioxidant',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(5, 'Giloy', 'Tinospora cordifolia', 'Ayurveda', 'Immunity', 'Guduchi, गिलोय, गुळवेल',
 '["Stem"]','Boosts immunity, reduces fever.','Tinosporine, Cordifolide',
 'Juice 15ml twice daily.','Avoid in autoimmune diseases.','Juice, Tablet, Decoction','{}',
 'Immune-modulating herb.','Antipyretic, Immunomodulator',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(6, 'Turmeric', 'Curcuma longa', 'Ayurveda', 'Anti-inflammatory', 'Haldi, हळद',
 '["Rhizome"]','Wound healing, inflammation, skin glow.','Curcumin',
 '1 tsp with warm milk at night.','Avoid high doses in gallbladder disorders.','Powder, Capsule, Paste','{}',
 'Golden spice with healing power.','Antioxidant, Anti-inflammatory',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(7, 'Brahmi', 'Bacopa monnieri', 'Ayurveda', 'Cognitive', 'Water Hyssop, ब्राह्मी',
 '["Leaves","Whole Plant"]','Enhances memory and focus.','Bacosides',
 'Powder 3g daily or tablet form.','Avoid in low heart rate conditions.','Syrup, Tablet','{}',
 'Brain tonic in Ayurvedic formulations.','Nootropic, Nervine tonic',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(8, 'Shatavari', 'Asparagus racemosus', 'Ayurveda', 'Reproductive', 'शतावरी, Satavar',
 '["Root"]','Female tonic, lactation and hormonal balance.','Saponins',
 'Powder 3g twice daily with milk.','Avoid in breast cancer cases.','Churna, Tablet','{}',
 'Used for women’s health.','Galactagogue, Tonic',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(9, 'Bael', 'Aegle marmelos', 'Ayurveda', 'Digestive', 'Bilva, बेल',
 '["Fruit","Leaves"]','Treats diarrhea, dysentery, gastric problems.','Aegeline, Marmelosin',
 'Fruit pulp 20g twice daily.','Avoid in constipation.','Sharbat, Pulp','{}',
 'Sacred fruit tree for gut health.','Digestive, Antimicrobial',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP),

(10, 'Mulethi', 'Glycyrrhiza glabra', 'Ayurveda', 'Respiratory', 'Licorice, मुलेठी, यष्टिमधु',
 '["Root"]','Soothes throat, cough and acidity.','Glycyrrhizin, Liquiritin',
 'Powder 2g with honey twice daily.','Avoid in high blood pressure.','Churna, Tablet','{}',
 'Sweet root herb for throat and GI relief.','Expectorant, Demulcent',CURRENT_TIMESTAMP,CURRENT_TIMESTAMP);

INSERT INTO image (plant_id, file_path, alt_text) VALUES
(1,'tulsi.jpg','Tulsi Plant'),
(2,'ashwagandha.jpg','Ashwagandha Roots'),
(3,'neem.jpg','Neem Leaves'),
(4,'amla.jpg','Amla Fruit'),
(5,'giloy.jpg','Giloy Stem'),
(6,'turmeric.jpg','Turmeric Rhizome'),
(7,'brahmi.jpg','Brahmi Herb'),
(8,'shatavari.jpg','Shatavari Root'),
(9,'bael.jpg','Bael Fruit'),
(10,'mulethi.jpg','Mulethi Root');

INSERT INTO remedy (
  symptom, diagnosis_pattern, plant_ids, preparation, dosage, lifestyle_recommendations,
  preparation_method, ayush_system, side_effects, contraindications, languages_json
) VALUES
('Cough','dry cough, sore throat','1,10',
 'Boil 10 Tulsi leaves + 2g Mulethi in 250ml water 10 min; add honey.',
 '150ml warm infusion twice daily after meals.',
 'Avoid cold drinks, steam inhalation.','Decoction','Ayurveda',
 'Excess Mulethi may raise BP.','Pregnancy consult doctor.','{}'),

('Fever','viral, chronic fever','5,1',
 'Giloy stem + Tulsi leaves decoction 150ml twice daily.',
 '150ml twice daily after meals.','Hydration, light diet.','Kadha','Ayurveda',
 '—','Autoimmune: avoid Giloy.','{}'),

('Indigestion','gas, bloating, appetite','4,9',
 'Amla juice 20ml with Bael pulp.',
 '1–2× daily.','Avoid fried food.','Juice blend','Ayurveda',
 '—','Acidity caution.','{}'),

('Stress & Anxiety','tension, insomnia','2,7',
 'Ashwagandha + Brahmi powder (3g each) with milk before sleep.',
 'Once nightly.','Meditation, reduce caffeine.','Churna Mix','Ayurveda',
 'Mild drowsiness.','Thyroid: avoid Ashwagandha.','{}'),

('Skin Allergy','eczema, acne','3,6',
 'Apply paste of Neem + Turmeric on affected area.',
 'Topical 2× daily.','Hygiene, avoid spicy food.','Paste','Ayurveda',
 'Irritation on sensitive skin.','Avoid near eyes.','{}'),

('Respiratory Weakness','bronchitis, asthma','10,1,5',
 'Mulethi, Tulsi, Giloy decoction 200ml.',
 '2× daily warm.','Avoid dust exposure.','Kadha','Ayurveda',
 '—','Pregnant/lactating: consult.','{}'),

('Low Immunity','frequent cold','5,2,4',
 'Giloy, Amla, Ashwagandha combination.',
 'Daily morning.','Sleep early, healthy diet.','Decoction','Ayurveda',
 '—','Autoimmune: avoid Giloy.','{}'),

('Acidity','heartburn, reflux','10,4',
 'Mulethi powder with Amla juice.',
 'Once daily after meal.','Avoid oily foods.','Churna','Ayurveda',
 'Mulethi may raise BP.','Hypertension.','{}'),

('Female Health','hormonal/lactation','8,4',
 'Shatavari powder with 10ml Amla juice.',
 'Twice daily.','Yoga, balanced diet.','Churna','Ayurveda',
 '—','Breast cancer cases avoid.','{}'),

('Joint Pain','arthritis, inflammation','6,5',
 'Turmeric milk + Giloy decoction.',
 'Night dose.','Warm compress, exercise.','Milk & Decoction','Ayurveda',
 '—','Gallbladder issues avoid Turmeric.','{}');

COMMIT;
