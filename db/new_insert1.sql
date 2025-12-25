-- Batch: Classical Ayurvedic plants (UNIQUE botanical_name) with JSON-valid fields
-- image_hero: common_name_en with underscores + .jpg (NO <>)

INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Premna integrifolia',
  'Agnimantha',
  'अग्निमन्था', 'अग्निमंथ', 'अग्निमन्था',
  'Verbenaceae',
  'Agnimantha is a classical Dashamoola drug traditionally used for vata–kapha disorders, swelling and musculoskeletal discomfort.',
  'Dry deciduous forests and plains; cultivated in some regions.',
  '["root_bark","stem_bark","leaves"]',
  '["तिक्त","कषाय"]',
  'उष्ण',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"vata":"pacifies","kapha":"pacifies","pitta":"may_increase_if_excess"}',
  'शोथहर',
  NULL,
  '["शोथहर","दीपन","पाचन","वातकफहर","शूलहर"]',
  'Dashamoola (Brihat Panchamoola); Nighantu references in classical Ayurveda.',
  0,
  'wild_and_cultivated',
  'Agnimantha.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Oroxylum indicum',
  'Shyonaka',
  'श्योणाक', 'श्योणाक', 'श्योणाक',
  'Bignoniaceae',
  'Shyonaka (Sona Patha) is a Dashamoola herb traditionally used for vata–kapha conditions, respiratory support and inflammation-related discomfort.',
  'Moist deciduous forests; foothills and plains in tropical regions.',
  '["root_bark","stem_bark","bark","seeds"]',
  '["मधुर","तिक्त","कषाय","कटु"]',
  'उष्ण',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"vata":"pacifies","kapha":"pacifies","pitta":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["शोथहर","दीपन","ग्राही","कासहर","श्वासहर","व्रणहर"]',
  'Dashamoola (Brihat Panchamoola); references across Samhita/Nighantu literature.',
  0,
  'wild_and_cultivated',
  'Shyonaka.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Stereospermum suaveolens',
  'Patala',
  'पाटला', 'पाटला', 'पाटला',
  'Bignoniaceae',
  'Patala is a Dashamoola herb traditionally used in vata–kapha disorders and for respiratory support in classical formulations.',
  'Tropical forests and plains; commonly found in India.',
  '["root_bark","bark","flowers"]',
  '["तिक्त","कटु"]',
  'उष्ण',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"vata":"pacifies","kapha":"pacifies","pitta":"variable"}',
  'श्वासहर',
  NULL,
  '["श्वासहर","कासहर","शोथहर","दीपन","पाचन"]',
  'Dashamoola (Brihat Panchamoola); used in classical kvatha groups.',
  0,
  'wild_and_cultivated',
  'Patala.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Gmelina arborea',
  'Gambhari',
  'गम्भारी', 'गम्हारी', 'गम्भारी',
  'Lamiaceae',
  'Gambhari (Kashmari) is a Dashamoola herb traditionally used for vata–pitta balancing and swelling-related discomfort.',
  'Moist deciduous forests; widely distributed in India.',
  '["root_bark","bark","fruits","leaves"]',
  '["तिक्त","कषाय","मधुर"]',
  'उष्ण',
  'कटु',
  '["गुरु"]',
  '{"vata":"pacifies","pitta":"pacifies","kapha":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["शोथहर","दीपन","पाचन","बल्य","मेद्य"]',
  'Dashamoola (Brihat Panchamoola); Nighantu references.',
  0,
  'wild_and_cultivated',
  'Gambhari.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Desmodium gangeticum',
  'Shalaparni',
  'शलपर्णी', 'शलपर्णी', 'शलपर्णी',
  'Fabaceae',
  'Shalaparni is a Laghu Panchamoola/Dashamoola component traditionally used for strength support and in fever/respiratory formulations.',
  'Plains and lower hills across India; common in scrub/forest margins.',
  '["root","whole_plant"]',
  '["मधुर","तिक्त"]',
  'उष्ण',
  'मधुर',
  '["गुरु","स्निग्ध"]',
  '{"vata":"pacifies","pitta":"pacifies","kapha":"pacifies"}',
  NULL,
  NULL,
  '["बल्य","रसायन","ज्वरघ्न","कासहर","श्वासहर","दीपन","पाचन"]',
  'Dashamoola (Laghu Panchamoola) references; classical usage noted in Ayurvedic literature.',
  0,
  'wild_and_cultivated',
  'Shalaparni.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Uraria picta',
  'Prishniparni',
  'पृष्णिपर्णी', 'पृष्णिपर्णी', 'पृष्णिपर्णी',
  'Fabaceae',
  'Prishniparni is a Laghu Panchamoola/Dashamoola herb traditionally used for strength support and vata-related formulations.',
  'Plains and dry regions; common in scrublands and open forests.',
  '["root","whole_plant"]',
  '["मधुर","तिक्त"]',
  'उष्ण',
  'मधुर',
  '["लघु","स्निग्ध"]',
  '{"vata":"pacifies","pitta":"pacifies","kapha":"pacifies"}',
  NULL,
  NULL,
  '["बल्य","दीपन","पाचन","श्वासहर","कासहर","रसायन"]',
  'Dashamoola (Laghu Panchamoola) references; classical usage noted in Ayurvedic literature.',
  0,
  'wild_and_cultivated',
  'Prishniparni.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Pluchea lanceolata',
  'Rasna',
  'रास्ना', 'रास्ना', 'रास्ना',
  'Asteraceae',
  'Rasna is traditionally used for pain, indigestion and vata-related complaints in classical Ayurveda.',
  'Dry plains and wastelands; cultivated locally and found wild in North India.',
  '["root","rhizome","leaves"]',
  '["कटु","तिक्त"]',
  'उष्ण',
  'कटु',
  '["लघु"]',
  '{"vata":"pacifies","kapha":"supports","pitta":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["वातहर","शूलहर","दीपन","पाचन","शोथहर"]',
  'Referenced in classical practice as Rasna (with regional source plants noted in Nighantu traditions).',
  0,
  'wild_and_cultivated',
  'Rasna.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Symplocos racemosa',
  'Lodhra',
  'लोध्र', 'लोध्र', 'लोध्र',
  'Symplocaceae',
  'Lodhra is traditionally used for astringent/styptic support and in classical women’s health formulations.',
  'Himalayan foothills and moist forests; also cultivated.',
  '["bark"]',
  '["कषाय"]',
  'शीत',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"kapha":"pacifies","pitta":"pacifies","vata":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["स्तम्भन","रक्तस्तम्भन","नेत्र्य","शोथहर","त्वच्य"]',
  'Classical references since Sushruta period; widely cited in Nighantu/Prayoga for stambhana karma.',
  0,
  'wild_and_cultivated',
  'Lodhra.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Mesua ferrea',
  'Nagakesara',
  'नागकेसर', 'नागकेसर', 'नागकेसर',
  'Calophyllaceae',
  'Nagakesara is a classical aromatic drug used traditionally in formulations like Chyawanprash and for pitta–kapha conditions.',
  'Evergreen forests of South/Southeast Asia; cultivated in parts of India.',
  '["stamens","flowers","seeds"]',
  '["कषाय","तिक्त"]',
  'शीत',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"pitta":"pacifies","kapha":"pacifies","vata":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["स्तम्भन","शोथहर","दीपन","पाचन","रक्तप्रसादन"]',
  'Used in classical groups (e.g., Chaturjata usage traditions; referenced across Ayurvedic formulations).',
  0,
  'wild_and_cultivated',
  'Nagakesara.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Aconitum heterophyllum',
  'Ativisha',
  'अतिविषा', 'अतिविषा', 'अतिविषा',
  'Ranunculaceae',
  'Ativisha is a classical herb traditionally used in digestive and pediatric support formulations in Ayurveda.',
  'Himalayan regions; alpine/sub-alpine zones; mostly wild-sourced.',
  '["root"]',
  '["तिक्त","कटु"]',
  'शीत',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"kapha":"pacifies","pitta":"pacifies","vata":"supports"}',
  NULL,
  NULL,
  '["दीपन","पाचन","ग्राही","ज्वरघ्न"]',
  'Classically referenced in digestive and jwara-related contexts; used with caution as per traditional practice.',
  0,
  'wild_sourced',
  'Ativisha.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Semecarpus anacardium',
  'Bhallataka',
  'भल्लातक', 'भिलावा', 'भल्लातक',
  'Anacardiaceae',
  'Bhallataka is a traditionally strong, hot-potency herb used only after classical purification (शोधन) and in specific indications.',
  'Tropical forests and plains; found wild in India.',
  '["nut"]',
  '["कटु","तिक्त","कषाय"]',
  'उष्ण',
  'कटु',
  '["तीक्ष्ण","स्निग्ध"]',
  '{"kapha":"pacifies","vata":"pacifies","pitta":"may_aggravate"}',
  NULL,
  NULL,
  '["दीपन","पाचन","शूलहर","कुष्ठघ्न","मेध्य"]',
  'Classical texts emphasize शोधन before use; referenced in multiple gana/skandha contexts.',
  0,
  'wild_sourced',
  'Bhallataka.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Clerodendrum serratum',
  'Bharangi',
  'भारंगी', 'भारंगी', 'भारंगी',
  'Verbenaceae',
  'Bharangi is traditionally used for kapha–vata respiratory support in classical Ayurveda.',
  'Forest margins and scrublands; found across India.',
  '["root","root_bark","leaves"]',
  '["तिक्त","कटु"]',
  'उष्ण',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"kapha":"pacifies","vata":"pacifies","pitta":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["श्वासहर","कासहर","ज्वरघ्न","शोथहर","पाचन"]',
  'Referenced under various gana/skandha traditions in classical literature for respiratory uses.',
  0,
  'wild_and_cultivated',
  'Bharangi.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Tephrosia purpurea',
  'Sharpunkha',
  'शरपुंखा', 'शरपुंखा', 'शरपुंखा',
  'Fabaceae',
  'Sharpunkha is traditionally used for liver–spleen support and in classical formulations for kapha-related conditions.',
  'Dry plains and wastelands; widely distributed in India.',
  '["whole_plant","root","leaves"]',
  '["तिक्त","कषाय"]',
  'उष्ण',
  'कटु',
  '["लघु","रूक्ष","तीक्ष्ण"]',
  '{"kapha":"pacifies","pitta":"supports","vata":"supports"}',
  'प्लीहघ्न',
  NULL,
  '["दीपन","पाचन","यकृत्य","प्लीहघ्न","कृमिघ्न"]',
  'Classical mention with prabhava as प्लीहघ्न in traditional literature.',
  0,
  'wild_and_cultivated',
  'Sharpunkha.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Crataeva nurvala',
  'Varuna',
  'वरुण', 'वरुण', 'वरुण',
  'Capparaceae',
  'Varuna is classically used for urinary support and is a key herb in ashmari-related traditional contexts.',
  'Riverbanks and moist forests; widely distributed and cultivated.',
  '["stem_bark","root_bark","leaves","flowers"]',
  '["तिक्त","कटु","कषाय"]',
  'उष्ण',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"kapha":"pacifies","vata":"pacifies","pitta":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["अश्मरीघ्न","मूत्रल","शोथहर","दीपन","पाचन"]',
  'Referenced in Varunadi gana traditions; classical usage for urinary disorders.',
  0,
  'wild_and_cultivated',
  'Varuna.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Bauhinia variegata',
  'Kanchanara',
  'काञ्चनार', 'कांचनार', 'काञ्चनार',
  'Fabaceae',
  'Kanchanara bark is traditionally used in kapha–pitta conditions and in classical glandular/lymph node related contexts.',
  'Plains and sub-Himalayan regions; commonly cultivated.',
  '["stem_bark","flowers","leaves","seeds"]',
  '["कषाय"]',
  'शीत',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"kapha":"pacifies","pitta":"pacifies","vata":"may_increase_if_excess"}',
  'गण्डमाला-नाशन',
  NULL,
  '["कफहर","शोथहर","स्तम्भन","कण्ठ्य","रक्तशोधक"]',
  'Traditional references include Gandamala contexts; widely used in classical practice.',
  0,
  'wild_and_cultivated',
  'Kanchanara.jpg',
  'ayurveda'
);

BEGIN TRANSACTION;

-- Next batch: Classical Ayurvedic plants (unique botanical_name) + native-script names
-- NOTE: JSON-valid columns only for parts_used, rasa, guna, dosha_effect, therapeutic_actions (others plain text)
-- image_hero: <common_name_en_with_underscores>.jpg  (NO angle brackets)

INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES

-- 1
(
  'Leptadenia reticulata',
  'Jivanti',
  'जीवन्ती', 'जीवन्ती', 'जीवन्ती',
  'Apocynaceae',
  'Jivanti is a classical Ayurvedic herb traditionally used in rasayana and nourishing formulations.',
  'Dry regions and scrub forests; also cultivated.',
  '["leaves","stem","root"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["रसायन","बल्य","धातुपोषण","स्तन्यवर्धक"]',
  'Bhavaprakasha Nighantu; classical nighantu references.',
  0,
  'wild_and_cultivated',
  'Jivanti.jpg',
  'ayurveda'
),

-- 2
(
  'Butea superba',
  'Kovidara_Vine',
  'कोविदार लता', 'कोविदार लता', 'कोविदारलता',
  'Fabaceae',
  'A traditional Ayurvedic climber used in strengthening and vitality-support contexts in regional practice.',
  'Tropical forests; wild-sourced in parts of India.',
  '["root","stem"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["बल्य","वातहर","धातुपोषण"]',
  'Regional Ayurvedic practice; nighantu mentions vary by tradition.',
  0,
  'wild_sourced',
  'Kovidara_Vine.jpg',
  'ayurveda'
),

-- 3
(
  'Pseudarthria viscida',
  'Prishniparni_(South)',
  'पृष्णिपर्णी', 'पृष्णिपर्णी', 'पृष्णिपर्णी',
  'Fabaceae',
  'A Prishniparni-source plant used in classical Dashamoola/Laghu Panchamoola traditions in some regions.',
  'Forest margins and scrublands; regional distribution.',
  '["root","whole_plant"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["बल्य","श्वासहर","कासहर","दीपन","पाचन"]',
  'Classical Dashamoola/Laghu Panchamoola usage traditions (regional source variants).',
  0,
  'wild_sourced',
  'Prishniparni_(South).jpg',
  'ayurveda'
),

-- 4
(
  'Boerhavia repens',
  'Punarnava_(Repens)',
  'पुनर्नवा', 'पुनर्नवा', 'पुनर्नवा',
  'Nyctaginaceae',
  'Punarnava-type species traditionally used for swelling and urinary support in Ayurveda (regional usage).',
  'Dry and semi-arid regions; field margins.',
  '["root","whole_plant"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["मूत्रल","शोथहर","दीपन","पाचन"]',
  'Ayurvedic usage traditions; species variants used regionally.',
  0,
  'wild_sourced',
  'Punarnava_(Repens).jpg',
  'ayurveda'
),

-- 5
(
  'Baliospermum montanum',
  'Danti',
  'दन्ती', 'दन्ती', 'दन्ती',
  'Euphorbiaceae',
  'Danti is a classical Ayurvedic herb traditionally used in virechana-oriented formulations under expert guidance.',
  'Subtropical forests; wild-sourced in parts of India.',
  '["root"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["विरेचक","दीपन","पाचन"]',
  'Classical nighantu references; used with caution in traditional practice.',
  0,
  'wild_sourced',
  'Danti.jpg',
  'ayurveda'
),

-- 6
(
  'Operculina turpethum',
  'Trivrit',
  'त्रिवृत्', 'त्रिवृत', 'त्रिवृत्',
  'Convolvulaceae',
  'Trivrit is a well-known classical Ayurvedic drug used in purgative (virechana) contexts under supervision.',
  'Tropical regions; cultivated and wild.',
  '["root"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["विरेचक","दीपन","पाचन"]',
  'Classical references across Ayurvedic literature for virechana usage.',
  0,
  'wild_and_cultivated',
  'Trivrit.jpg',
  'ayurveda'
),

-- 7
(
  'Cyperus rotundus (rhizome)',
  'Musta_Rhizome',
  'मुस्ता', 'मुस्ता', 'मुस्ता',
  'Cyperaceae',
  'Musta rhizome is a classical Ayurvedic drug used for digestive support and fever-related formulations.',
  'Common in plains; fields and moist soils.',
  '["rhizome"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["दीपन","पाचन","ज्वरघ्न","ग्राही"]',
  'Bhavaprakasha Nighantu; classical usage in digestive/jwara contexts.',
  0,
  'wild_sourced',
  'Musta_Rhizome.jpg',
  'ayurveda'
),

-- 8
(
  'Cedrus deodara',
  'Deodar',
  'देवदार', 'देवदार', 'देवदारु',
  'Pinaceae',
  'Devadaru is a classical aromatic wood used in vata–kapha contexts and external applications.',
  'Himalayan regions; cultivated in some areas.',
  '["heartwood","bark","oil"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["वातहर","कफहर","शोथहर","शूलहर"]',
  'Classical nighantu references for Devadaru.',
  0,
  'wild_and_cultivated',
  'Deodar.jpg',
  'ayurveda'
),

-- 9
(
  'Nymphaea nouchali',
  'Blue_Water_Lily',
  'नीलोत्पल', 'नीलोत्पल', 'नीलोत्पल',
  'Nymphaeaceae',
  'Neelotpala is traditionally used in pitta-pacifying contexts and cooling formulations.',
  'Ponds and freshwater bodies across India.',
  '["flowers","leaves","rhizome"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["पित्तशामक","दाहशमन","शीतल"]',
  'Classical nighantu references for Utpala/Neelotpala.',
  0,
  'wild_sourced',
  'Blue_Water_Lily.jpg',
  'ayurveda'
),

-- 10
(
  'Nelumbo nucifera (stamen)',
  'Lotus_Stamen',
  'पद्मकेसर', 'पद्मकेसर', 'पद्मकेसर',
  'Nelumbonaceae',
  'Lotus stamen is used traditionally for stambhana and pitta-related formulations in Ayurveda.',
  'Freshwater lakes and ponds; cultivated widely.',
  '["stamen"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["स्तम्भन","पित्तशामक","दाहशमन"]',
  'Classical usage in stambhana/pitta contexts; nighantu references.',
  0,
  'cultivated',
  'Lotus_Stamen.jpg',
  'ayurveda'
),

-- 11
(
  'Fumaria parviflora',
  'Parpata',
  'पर्पट', 'पर्पट', 'पर्पट',
  'Papaveraceae',
  'Parpata is traditionally used in fever and skin-related supportive formulations in Ayurveda.',
  'Plains; fields and waste places.',
  '["whole_plant"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["ज्वरघ्न","रक्तप्रसादन","त्वच्य","दीपन"]',
  'Classical nighantu references for Parpata/Parpataka traditions.',
  0,
  'wild_sourced',
  'Parpata.jpg',
  'ayurveda'
),

-- 12
(
  'Tinospora sinensis',
  'Guduchi_(Sinensis)',
  'गुडूची', 'गुळवेल', 'गुडूची',
  'Menispermaceae',
  'A Guduchi-type species used in regional traditions; classical Guduchi references primarily align with Tinospora cordifolia.',
  'Tropical forests; climbing on trees; wild-sourced.',
  '["stem","leaves"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["रसायन","ज्वरघ्न","दीपन","पाचन"]',
  'Regional usage traditions; classical Guduchi references generally cite T. cordifolia.',
  0,
  'wild_sourced',
  'Guduchi_(Sinensis).jpg',
  'ayurveda'
),

-- 13
(
  'Sida rhombifolia',
  'Mahabala',
  'महाबला', 'महाबला', 'महाबला',
  'Malvaceae',
  'Mahabala is traditionally used for strength and vata-support in classical Ayurvedic practice (Bala group).',
  'Plains and wastelands; common across India.',
  '["root","whole_plant"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["बल्य","वातहर","शूलहर"]',
  'Classical Bala/Mahabala traditions in Ayurveda.',
  0,
  'wild_and_cultivated',
  'Mahabala.jpg',
  'ayurveda'
),

-- 14
(
  'Curculigo orchioides',
  'Kali_Musli',
  'काली मुसली', 'काळी मुसळी', 'तालीमखाना',
  'Hypoxidaceae',
  'Kali Musli is traditionally used in vajikarana and strengthening formulations in Ayurveda.',
  'Forests and shaded areas; wild-sourced and cultivated.',
  '["rhizome","root"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["बल्य","वाजीकरण","रसायन"]',
  'Classical vajikarana/rasayana traditions; nighantu references.',
  0,
  'wild_and_cultivated',
  'Kali_Musli.jpg',
  'ayurveda'
),

-- 15
(
  'Tinospora crispa',
  'Guduchi_(Crispa)',
  'गुडूची', 'गुळवेल', 'गुडूची',
  'Menispermaceae',
  'A Guduchi-type climber used in some traditions; primary classical Guduchi aligns with T. cordifolia.',
  'Tropical regions; climbing; wild-sourced.',
  '["stem","leaves"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["रसायन","ज्वरघ्न","दीपन","पाचन"]',
  'Regional usage traditions; classical Guduchi references generally cite T. cordifolia.',
  0,
  'wild_sourced',
  'Guduchi_(Crispa).jpg',
  'ayurveda'
),

-- 16
(
  'Glycyrrhiza glabra (seed)',
  'Licorice_Seed',
  'मुलेठी बीज', 'जेष्ठमध बी', 'यष्टिमधु',
  'Fabaceae',
  'Licorice seed is occasionally used regionally; classical primary part is root.',
  'Cultivated; also found in suitable temperate zones.',
  '["seeds"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["कण्ठ्य","श्वासहर","व्रणरोपण"]',
  'Root is classically emphasized; seed usage varies regionally.',
  0,
  'cultivated',
  'Licorice_Seed.jpg',
  'ayurveda'
),

-- 17
(
  'Callicarpa macrophylla',
  'Priyangu',
  'प्रियंगु', 'प्रियंगु', 'प्रियंगु',
  'Lamiaceae',
  'Priyangu is traditionally used for stambhana and pitta-related supportive formulations.',
  'Sub-Himalayan regions and forests; wild-sourced.',
  '["flowers","leaves","bark"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["स्तम्भन","पित्तशामक","त्वच्य"]',
  'Classical nighantu references for Priyangu.',
  0,
  'wild_sourced',
  'Priyangu.jpg',
  'ayurveda'
),

-- 18
(
  'Salvadora persica',
  'Piloo',
  'पीलु', 'पीलू', 'पीलु',
  'Salvadoraceae',
  'Piloo is traditionally used in kapha–vata contexts and regional formulations; also known for dental twig usage.',
  'Arid and semi-arid regions; saline soils.',
  '["fruits","bark","twigs"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["कफहर","वातहर","दीपन","पाचन"]',
  'Classical and regional nighantu mentions.',
  0,
  'wild_sourced',
  'Piloo.jpg',
  'ayurveda'
),

-- 19
(
  'Zanthoxylum armatum',
  'Tejphal',
  'तेजफल', 'तेजफळ', 'तुम्बुरु',
  'Rutaceae',
  'Tejphal (Tumburu) is an aromatic drug used traditionally for digestive support and kapha–vata contexts.',
  'Himalayan foothills; wild-sourced and cultivated.',
  '["fruits","seeds","bark"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["दीपन","पाचन","कफहर","वातहर"]',
  'Classical nighantu references for Tumburu/Tejphal.',
  0,
  'wild_and_cultivated',
  'Tejphal.jpg',
  'ayurveda'
),

-- 20
(
  'Elephantopus scaber',
  'Anantamoola_(South)',
  'अनन्तमूल', 'अनंतमूळ', 'अनन्तमूल',
  'Asteraceae',
  'Anantamoola-type usage varies regionally; used traditionally for cooling and supportive purposes in some practices.',
  'Moist places and forests; wild-sourced.',
  '["root","whole_plant"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["दाहशमन","रक्तप्रसादन","त्वच्य"]',
  'Regional Ayurvedic practice; name usage varies by region/tradition.',
  0,
  'wild_sourced',
  'Anantamoola_(South).jpg',
  'ayurveda'
),

-- 21
(
  'Aegle marmelos (leaf)',
  'Bael_Leaf',
  'बेल पत्ता', 'बेल पान', 'बिल्वपत्र',
  'Rutaceae',
  'Bael leaf is traditionally used in digestive contexts and classical prayoga patterns.',
  'Dry and mixed forests; widely cultivated.',
  '["leaves"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["दीपन","पाचन","ग्राही"]',
  'Classical Bilva traditions; leaf usage common in practice.',
  0,
  'cultivated',
  'Bael_Leaf.jpg',
  'ayurveda'
),

-- 22
(
  'Santalum album',
  'White_Sandalwood',
  'सफ़ेद चंदन', 'पांढरे चंदन', 'चन्दन',
  'Santalaceae',
  'Chandana is a classical cooling aromatic wood used for pitta-related support and topical applications.',
  'Dry tropical regions; cultivated; protected in many areas.',
  '["heartwood","oil"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["पित्तशामक","दाहशमन","त्वच्य"]',
  'Classical nighantu references for Chandana.',
  1,
  'protected_cultivation',
  'White_Sandalwood.jpg',
  'ayurveda'
),

-- 23
(
  'Emblica officinalis (seed)',
  'Amla_Seed',
  'आँवला बीज', 'आवळ्याचे बी', 'आमलकी',
  'Phyllanthaceae',
  'Amla seed is occasionally used in regional practices; classical primary part is fruit.',
  'Cultivated and wild across India.',
  '["seeds"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["रसायन","बल्य"]',
  'Fruit is classically emphasized; seed usage varies regionally.',
  0,
  'cultivated',
  'Amla_Seed.jpg',
  'ayurveda'
),

-- 24
(
  'Cissampelos pareira (root)',
  'Patha_Root',
  'पाठा मूल', 'पाठा मुळ', 'पाठा',
  'Menispermaceae',
  'Patha root is used traditionally in digestive and fever-related formulations in Ayurveda.',
  'Tropical forests; climbing shrub; wild-sourced.',
  '["root"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["दीपन","पाचन","ज्वरघ्न","ग्राही"]',
  'Classical references for Patha in Ayurvedic literature.',
  0,
  'wild_sourced',
  'Patha_Root.jpg',
  'ayurveda'
),

-- 25
(
  'Strychnos potatorum',
  'Nirmali',
  'निर्मली', 'निर्मळी', 'निर्मली',
  'Loganiaceae',
  'Nirmali seeds are traditionally known for water clarification and are referenced in Ayurvedic practice.',
  'Dry regions and forests; found in India.',
  '["seeds"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["जलशोधन","कफहर","दीपन"]',
  'Traditional Ayurvedic practice mentions Nirmali for jalashodhana.',
  0,
  'wild_sourced',
  'Nirmali.jpg',
  'ayurveda'
);

-- Ensure image_hero formatting for ALL rows (removes spaces in filename)
UPDATE plants
SET image_hero = REPLACE(TRIM(image_hero), ' ', '_')
WHERE image_hero IS NOT NULL AND image_hero LIKE '%.jpg%';

COMMIT;

BEGIN TRANSACTION;

INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES

-- =========================
-- AYURVEDA (Classical batch)
-- =========================

(
  'Acacia nilotica',
  'Babul',
  'बबूल', 'बाभूळ', 'बबूल',
  'Fabaceae',
  'Classical astringent herb traditionally used for stambhana and oral/throat supportive uses in Ayurveda.',
  'Plains and dry regions across India; common along roadsides and fields.',
  '["bark","gum","pods","leaves"]',
  '["कषाय"]',
  'शीत',
  'कटु',
  '["गुरु","रूक्ष"]',
  '{"pitta":"pacifies","kapha":"pacifies","vata":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["स्तम्भन","रक्तस्तम्भन","कण्ठ्य","दन्त्य","त्वच्य"]',
  'Nighantu references for बबूल; traditional stambhana usage.',
  0,
  'wild_and_cultivated',
  'Babul.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Achillea millefolium',
  'Yarrow',
  'यैरो', 'यॅरो', NULL,
  'Asteraceae',
  'Aromatic bitter herb used in traditional herbal practice; included here as supportive plant entry (not a core classical Ayurvedic dravya).',
  'Temperate regions; cultivated as an herb.',
  '["aerial_parts","flowers","leaves"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["पाचनसहायक","मृदु_शामक"]',
  NULL,
  0,
  'cultivated',
  'Yarrow.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Acorus calamus',
  'Vacha',
  'वचा', 'वचा', 'वचा',
  'Acoraceae',
  'Vacha is a classical aromatic drug traditionally used for medhya and kapha–vata support in Ayurveda.',
  'Marshy areas and riverbanks; cultivated.',
  '["rhizome"]',
  '["कटु","तिक्त"]',
  'उष्ण',
  'कटु',
  '["लघु","तीक्ष्ण"]',
  '{"kapha":"pacifies","vata":"pacifies","pitta":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["मेध्य","कफहर","दीपन","पाचन","कण्ठ्य"]',
  'Classical nighantu references for वचा.',
  0,
  'wild_and_cultivated',
  'Vacha.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Aerva lanata',
  'Gorakshaganja',
  'गोरक्षगंजा', 'गोरखगंजा', 'गोरक्षगंजा',
  'Amaranthaceae',
  'Traditionally used for urinary support and as a mild diuretic in Ayurveda (regional practice).',
  'Dry regions and wastelands across India.',
  '["whole_plant","root"]',
  '["मधुर","कषाय"]',
  'शीत',
  'मधुर',
  '["लघु"]',
  '{"pitta":"pacifies","kapha":"supports","vata":"supports"}',
  NULL,
  NULL,
  '["मूत्रल","शोथहर","अश्मरीसहायक"]',
  'Regional Ayurvedic practice references.',
  0,
  'wild_sourced',
  'Gorakshaganja.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Aloe barbadensis Miller',
  'Aloe Vera',
  'घृतकुमारी', 'कोरफड', 'घृतकुमारी',
  'Asphodelaceae',
  'Ghritkumari is traditionally used for pitta support and in skin/digestive supportive contexts.',
  'Cultivated widely; dry regions and home gardens.',
  '["leaf_pulp","gel"]',
  '["तिक्त"]',
  'शीत',
  'कटु',
  '["गुरु","स्निग्ध"]',
  '{"pitta":"pacifies","vata":"supports","kapha":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["पित्तशामक","त्वच्य","मृदु_विरेचक"]',
  'Traditional usage noted in Ayurvedic practice.',
  0,
  'cultivated',
  'Aloe_Vera.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Asclepias curassavica',
  'Bloodflower',
  'ब्लडफ्लॉवर', 'ब्लडफ्लॉवर', NULL,
  'Apocynaceae',
  'Ornamental medicinal plant used in folk traditions; included as supportive entry (not a core classical dravya).',
  'Cultivated ornamental; tropical climates.',
  '["leaves","latex"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["लोकपरंपरा_उपयोग"]',
  NULL,
  0,
  'cultivated',
  'Bloodflower.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Bacopa monnieri',
  'Brahmi',
  'ब्राह्मी', 'ब्राह्मी', 'ब्राह्मी',
  'Plantaginaceae',
  'Classical medhya rasayana herb used traditionally for memory and calmness support.',
  'Wetlands, marshy areas; cultivated.',
  '["whole_plant"]',
  '["तिक्त","कषाय"]',
  'शीत',
  'मधुर',
  '["लघु"]',
  '{"pitta":"pacifies","vata":"pacifies","kapha":"supports"}',
  NULL,
  NULL,
  '["मेध्य","रसायन","शामक"]',
  'Classical medhya references in Ayurvedic literature.',
  0,
  'wild_and_cultivated',
  'Brahmi.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Bambusa arundinacea',
  'Bamboo',
  'बाँस', 'बांबू', 'वंश',
  'Poaceae',
  'Vansha is traditionally used; bamboo-related dravyas (like banslochan) are used in classical practice.',
  'Widely cultivated; forests and plantations.',
  '["shoots","nodes","siliceous_exudate"]',
  '["मधुर","कषाय"]',
  'शीत',
  'मधुर',
  '["लघु"]',
  '{"pitta":"pacifies","kapha":"supports","vata":"supports"}',
  NULL,
  NULL,
  '["कफहर","कासहर","श्वासहर"]',
  'Traditional use of वंश/वंशलोचन in classical formulations.',
  0,
  'cultivated',
  'Bamboo.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Boerhavia diffusa',
  'Punarnava',
  'पुनर्नवा', 'पुनर्नवा', 'पुनर्नवा',
  'Nyctaginaceae',
  'Punarnava is a classical herb used for swelling and urinary support in Ayurveda.',
  'Plains and fields across India; common and cultivated.',
  '["root","whole_plant"]',
  '["तिक्त","कषाय"]',
  'उष्ण',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"kapha":"pacifies","vata":"pacifies","pitta":"supports"}',
  NULL,
  NULL,
  '["मूत्रल","शोथहर","दीपन","पाचन"]',
  'Classical references for पुनर्नवा in nighantu and practice.',
  0,
  'wild_and_cultivated',
  'Punarnava.jpg',
  'ayurveda'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Butea monosperma',
  'Palash',
  'पलाश', 'पळस', 'पलाश',
  'Fabaceae',
  'Palasha is a classical herb used traditionally in various internal and external applications in Ayurveda.',
  'Plains and dry deciduous forests; common across India.',
  '["flowers","bark","gum","seeds"]',
  '["कषाय","तिक्त"]',
  'उष्ण',
  'कटु',
  '["लघु","रूक्ष"]',
  '{"kapha":"pacifies","vata":"pacifies","pitta":"may_increase_if_excess"}',
  NULL,
  NULL,
  '["कृमिघ्न","शोथहर","दीपन","पाचन"]',
  'Classical references for पलाश in Ayurvedic literature.',
  0,
  'wild_and_cultivated',
  'Palash.jpg',
  'ayurveda'
),

-- =========================
-- UNANI (new additions)
-- =========================

(
  'Plantago ovata',
  'Psyllium',
  'इसबगोल', 'इसबगोल', NULL,
  'Plantaginaceae',
  'Commonly used as a dietary fiber; included as Unani-aligned plant entry.',
  'Cultivated; arid/semi-arid regions.',
  '["husk","seeds"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["मलसंग्रह_सहायक","पाचनसहायक"]',
  NULL,
  0,
  'cultivated',
  'Psyllium.jpg',
  'unani'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Rosa damascena',
  'Damask Rose',
  'गुलाब', 'गुलाब', NULL,
  'Rosaceae',
  'Aromatic rose used widely in traditional systems including Unani for cooling and supportive preparations.',
  'Cultivated widely; gardens and farms.',
  '["petals","flowers"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["शीतल","शामक","सुगंधित"]',
  NULL,
  0,
  'cultivated',
  'Damask_Rose.jpg',
  'unani'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Cichorium intybus',
  'Chicory',
  'कासनी', 'कासनी', NULL,
  'Asteraceae',
  'Kaasni is used traditionally in Unani for liver-related supportive contexts.',
  'Cultivated; fields and temperate zones.',
  '["root","leaves"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["यकृत_सहायक","पाचनसहायक"]',
  NULL,
  0,
  'cultivated',
  'Chicory.jpg',
  'unani'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Foeniculum vulgare',
  'Fennel',
  'सौंफ', 'बडीशेप', NULL,
  'Apiaceae',
  'Aromatic seed used in multiple systems including Unani for digestive support.',
  'Cultivated; farms and kitchen gardens.',
  '["seeds"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["पाचनसहायक","वातहर"]',
  NULL,
  0,
  'cultivated',
  'Fennel.jpg',
  'unani'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Glycyrrhiza glabra',
  'Licorice',
  'मुलेठी', 'जेष्ठमध', NULL,
  'Fabaceae',
  'Mulethi is widely used in Unani for throat/respiratory supportive syrups and decoctions.',
  'Cultivated; suitable temperate regions.',
  '["root"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["कण्ठ्य","श्वाससहायक","शामक"]',
  NULL,
  0,
  'cultivated',
  'Licorice.jpg',
  'unani'
),

-- =========================
-- SIDDHA (new additions)
-- =========================

(
  'Andrographis paniculata',
  'Nilavembu',
  'नीलवेम्बू', 'नीलवेम्बू', NULL,
  'Acanthaceae',
  'Nilavembu is widely recognized in Siddha practice; included as Siddha-aligned plant entry.',
  'Tropical regions; cultivated and wild.',
  '["leaves","whole_plant"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["ज्वरसहायक","पाचनसहायक"]',
  NULL,
  0,
  'wild_and_cultivated',
  'Nilavembu.jpg',
  'siddha'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Tinospora cordifolia',
  'Seenthil',
  'सींथिल', 'सींथिल', NULL,
  'Menispermaceae',
  'Seenthil (Guduchi) is used in Siddha and Ayurveda for supportive purposes.',
  'Tropical forests; climbing; cultivated.',
  '["stem"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["रसायन","ज्वरसहायक"]',
  NULL,
  0,
  'wild_and_cultivated',
  'Seenthil.jpg',
  'siddha'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Phyllanthus emblica',
  'Nellikai',
  'नेल्लिकाई', 'नेल्लिकाई', NULL,
  'Phyllanthaceae',
  'Nellikai is a key fruit used across traditions; included as Siddha-aligned entry.',
  'Cultivated and wild in India.',
  '["fruit"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["रसायन","पित्तशामक"]',
  NULL,
  0,
  'cultivated',
  'Nellikai.jpg',
  'siddha'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Syzygium cumini',
  'Naval',
  'जामुन', 'जांभूळ', NULL,
  'Myrtaceae',
  'Naval is used traditionally; included here as Siddha-aligned plant entry.',
  'Plains; cultivated and wild.',
  '["seeds","bark","fruit"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["मेटाबॉलिक_सहायक","कषाय"]',
  NULL,
  0,
  'wild_and_cultivated',
  'Naval.jpg',
  'siddha'
);
INSERT OR IGNORE INTO plants (
  botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
  family, description, habitat,
  parts_used, rasa, virya, vipaka, guna, dosha_effect, prabhava,
  active_compounds, therapeutic_actions, classical_references,
  is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
(
  'Centella asiatica',
  'Vallarai',
  'वल्लराई', 'वल्लराई', NULL,
  'Apiaceae',
  'Vallarai is a Siddha-recognized herb used for memory and calming support.',
  'Wetlands and moist places; cultivated.',
  '["whole_plant","leaves"]',
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  NULL,
  '["मेध्य","शामक","रसायन"]',
  NULL,
  0,
  'wild_and_cultivated',
  'Vallarai.jpg',
  'siddha'
);

-- Enforce image_hero underscore rule from common_name_en for any newly inserted rows missing image_hero
UPDATE plants
SET image_hero = REPLACE(TRIM(common_name_en), ' ', '_') || '.jpg'
WHERE (image_hero IS NULL OR TRIM(image_hero) = '')
  AND common_name_en IS NOT NULL
  AND TRIM(common_name_en) != '';

COMMIT;
