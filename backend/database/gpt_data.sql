CREATE TABLE IF NOT EXISTS herbs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    scientific_name TEXT,
    ayush_system TEXT NOT NULL,
    uses TEXT,
    parts_used TEXT,
    phytochemicals TEXT,
    contraindications TEXT
);

CREATE TABLE IF NOT EXISTS common_names (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    herb_id INTEGER,
    name TEXT NOT NULL,
    FOREIGN KEY (herb_id) REFERENCES herbs(id)
);

CREATE TABLE IF NOT EXISTS remedies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    herb_id INTEGER,
    condition_name TEXT NOT NULL,
    preparation TEXT NOT NULL,
    form TEXT,
    FOREIGN KEY (herb_id) REFERENCES herbs(id)
);

CREATE TABLE IF NOT EXISTS herb_languages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    herb_id INTEGER,
    field TEXT NOT NULL,
    language_code TEXT NOT NULL,
    translation TEXT NOT NULL,
    FOREIGN KEY (herb_id) REFERENCES herbs(id)
);



-- ======================
-- Ayurveda Herbs 1–10
-- ======================

-- Herbs
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications) VALUES
(1, 'Tulsi', 'Ocimum sanctum', 'Ayurveda', 'Immunity booster, cold and cough', 'Leaves', 'Eugenol, Ursolic acid', 'Avoid during pregnancy'),
(2, 'Ashwagandha', 'Withania somnifera', 'Ayurveda', 'Stress relief, strength enhancer', 'Roots', 'Withanolides', 'Avoid in hyperthyroidism'),
(3, 'Neem', 'Azadirachta indica', 'Ayurveda', 'Skin disorders, blood purifier', 'Leaves, Bark', 'Azadirachtin, Nimbin', 'Avoid during pregnancy'),
(4, 'Amla', 'Phyllanthus emblica', 'Ayurveda', 'Rich source of Vitamin C, rejuvenator', 'Fruit', 'Ascorbic acid, Gallic acid', 'May cause acidity in excess'),
(5, 'Brahmi', 'Bacopa monnieri', 'Ayurveda', 'Memory booster, anxiety relief', 'Whole plant', 'Bacosides', 'Avoid during pregnancy'),
(6, 'Shatavari', 'Asparagus racemosus', 'Ayurveda', 'Female reproductive health, lactation', 'Roots', 'Shatavarin', 'Avoid in estrogen-sensitive conditions'),
(7, 'Triphala', 'Blend of three fruits', 'Ayurveda', 'Digestive health, detoxification', 'Fruits', 'Tannins, Gallic acid', 'Avoid in diarrhea'),
(8, 'Guggul', 'Commiphora wightii', 'Ayurveda', 'Cholesterol management, arthritis relief', 'Resin', 'Guggulsterones', 'Avoid in hyperthyroidism'),
(9, 'Haritaki', 'Terminalia chebula', 'Ayurveda', 'Digestive tonic, mild laxative', 'Fruit', 'Chebulinic acid', 'Avoid during dehydration'),
(10, 'Giloy', 'Tinospora cordifolia', 'Ayurveda', 'Fever, immunity enhancer', 'Stem', 'Tinosporin, Berberine', 'Avoid in autoimmune disorders');

-- Common Names
INSERT INTO common_names (herb_id, name) VALUES
(1, 'Tulsi'), (1, 'तुलसी'), (1, 'तुळस'),
(2, 'Ashwagandha'), (2, 'अश्वगंधा'), (2, 'अश्वगंधा'),
(3, 'Neem'), (3, 'नीम'), (3, 'निंब'),
(4, 'Amla'), (4, 'आंवला'), (4, 'आवळा'),
(5, 'Brahmi'), (5, 'ब्राह्मी'), (5, 'ब्राह्मी'),
(6, 'Shatavari'), (6, 'शतावरी'), (6, 'शतावरी'),
(7, 'Triphala'), (7, 'त्रिफला'), (7, 'त्रिफळा'),
(8, 'Guggul'), (8, 'गुग्गुल'), (8, 'गुग्गुळ'),
(9, 'Haritaki'), (9, 'हरितकी'), (9, 'हरितकी'),
(10, 'Giloy'), (10, 'गिलोय'), (10, 'गुळवेल');

-- Remedies (2–3 per herb, shortened example)
INSERT INTO remedies (herb_id, condition_name, preparation, form) VALUES
(1, 'Cold', 'Boil Tulsi leaves in water and drink warm', 'Decoction'),
(1, 'Immunity', 'Chew fresh Tulsi leaves daily', 'Raw'),
(2, 'Stress', 'Powdered Ashwagandha root with milk at night', 'Powder'),
(2, 'Weakness', 'Ashwagandha root decoction taken daily', 'Decoction'),
(3, 'Skin problems', 'Neem leaf paste applied to affected area', 'Topical'),
(3, 'Fever', 'Neem leaf tea prepared with honey', 'Tea'),
(4, 'Vitamin deficiency', 'Amla juice daily in the morning', 'Juice'),
(4, 'Rejuvenation', 'Powdered Amla fruit with honey', 'Powder'),
(5, 'Memory loss', 'Brahmi extract with milk daily', 'Extract'),
(5, 'Anxiety', 'Brahmi tea before bedtime', 'Tea');

-- Herb Languages
INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(1, 'name', 'hi', 'तुलसी'), (1, 'name', 'mr', 'तुळस'),
(1, 'uses', 'hi', 'प्रतिरक्षा बढ़ाने वाला, सर्दी और खांसी में लाभकारी'),
(1, 'uses', 'mr', 'रोग प्रतिकार शक्ती वाढवणारे, सर्दी व खोकल्यावर उपयुक्त'),
(1, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(1, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर करू नका'),

(2, 'name', 'hi', 'अश्वगंधा'), (2, 'name', 'mr', 'अश्वगंधा'),
(2, 'uses', 'hi', 'तनाव से राहत, शक्ति बढ़ाने में सहायक'),
(2, 'uses', 'mr', 'तणाव कमी करणारे, शक्ती वाढवणारे'),
(2, 'contraindications', 'hi', 'हाइपरथायरॉयडिज्म में उपयोग न करें'),
(2, 'contraindications', 'mr', 'हायपरथायरॉईडीझममध्ये वापर टाळा'),

(3, 'name', 'hi', 'नीम'), (3, 'name', 'mr', 'निंब'),
(3, 'uses', 'hi', 'त्वचा रोगों में लाभकारी, रक्त को शुद्ध करने वाला'),
(3, 'uses', 'mr', 'त्वचा रोगांवर उपयुक्त, रक्त शुद्ध करणारे'),
(3, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(3, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर करू नका');

-- ======================
-- Ayurveda Herbs 11–20
-- ======================

-- Herbs
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications) VALUES
(11, 'Turmeric', 'Curcuma longa', 'Ayurveda', 'Anti-inflammatory, wound healing', 'Rhizome', 'Curcumin', 'Avoid in gallstones'),
(12, 'Mulethi', 'Glycyrrhiza glabra', 'Ayurveda', 'Sore throat, cough relief', 'Roots', 'Glycyrrhizin', 'Avoid in high blood pressure'),
(13, 'Safed Musli', 'Chlorophytum borivilianum', 'Ayurveda', 'Aphrodisiac, vitality tonic', 'Roots', 'Saponins', 'Avoid in diabetes without monitoring'),
(14, 'Arjuna', 'Terminalia arjuna', 'Ayurveda', 'Cardiac tonic, blood pressure control', 'Bark', 'Arjunolic acid', 'Avoid with anticoagulants'),
(15, 'Manjistha', 'Rubia cordifolia', 'Ayurveda', 'Blood purifier, skin health', 'Roots', 'Anthraquinones', 'Avoid in pregnancy'),
(16, 'Kutki', 'Picrorhiza kurroa', 'Ayurveda', 'Liver tonic, digestive health', 'Roots', 'Picroside', 'Avoid in diarrhea'),
(17, 'Shankhpushpi', 'Convolvulus pluricaulis', 'Ayurveda', 'Memory booster, stress relief', 'Whole plant', 'Alkaloids, Flavonoids', 'Avoid in hypotension'),
(18, 'Bael', 'Aegle marmelos', 'Ayurveda', 'Digestive aid, diarrhea control', 'Fruit, Leaves', 'Marmelosin', 'Avoid in constipation'),
(19, 'Punarnava', 'Boerhavia diffusa', 'Ayurveda', 'Diuretic, kidney health', 'Roots, Leaves', 'Punarnavine', 'Avoid in dehydration'),
(20, 'Kalmegh', 'Andrographis paniculata', 'Ayurveda', 'Fever, liver health, immunity', 'Whole plant', 'Andrographolide', 'Avoid in pregnancy');

-- Common Names
INSERT INTO common_names (herb_id, name) VALUES
(11, 'Turmeric'), (11, 'हल्दी'), (11, 'हळद'),
(12, 'Mulethi'), (12, 'मुलेठी'), (12, 'जेष्ठमध'),
(13, 'Safed Musli'), (13, 'सफेद मुसली'), (13, 'सफेद मुसली'),
(14, 'Arjuna'), (14, 'अर्जुन'), (14, 'अर्जुन'),
(15, 'Manjistha'), (15, 'मंजिष्ठा'), (15, 'मंजिष्ठा'),
(16, 'Kutki'), (16, 'कुटकी'), (16, 'कुटकी'),
(17, 'Shankhpushpi'), (17, 'शंखपुष्पी'), (17, 'शंखपुष्पी'),
(18, 'Bael'), (18, 'बेल'), (18, 'बेल'),
(19, 'Punarnava'), (19, 'पुनर्नवा'), (19, 'पुनर्नवा'),
(20, 'Kalmegh'), (20, 'कालमेघ'), (20, 'कालमेघ');

-- Remedies (2–3 per herb, examples)
INSERT INTO remedies (herb_id, condition_name, preparation, form) VALUES
(11, 'Wound healing', 'Apply turmeric paste on wounds', 'Topical'),
(11, 'Arthritis', 'Turmeric powder in warm milk daily', 'Milk decoction'),
(12, 'Cough', 'Boil Mulethi roots and drink decoction', 'Decoction'),
(12, 'Throat pain', 'Chew small Mulethi sticks', 'Raw'),
(13, 'Vitality', 'Safed Musli powder with milk at night', 'Powder'),
(13, 'Weakness', 'Safed Musli extract as tonic', 'Extract'),
(14, 'Heart health', 'Arjuna bark decoction with milk', 'Decoction'),
(14, 'Blood pressure', 'Arjuna bark powder with warm water', 'Powder'),
(15, 'Skin problems', 'Manjistha root paste applied externally', 'Topical'),
(15, 'Blood purifier', 'Manjistha root decoction taken daily', 'Decoction'),
(16, 'Liver health', 'Kutki root decoction once daily', 'Decoction'),
(16, 'Digestion', 'Kutki root powder with honey', 'Powder');

-- Herb Languages
INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(11, 'name', 'hi', 'हल्दी'), (11, 'name', 'mr', 'हळद'),
(11, 'uses', 'hi', 'सूजन कम करने वाला, घाव भरने में सहायक'),
(11, 'uses', 'mr', 'दाह कमी करणारे, जखम भरण्यास मदत करणारे'),
(11, 'contraindications', 'hi', 'पित्ताशय की पथरी में उपयोग न करें'),
(11, 'contraindications', 'mr', 'पित्ताशयात खडे असल्यास वापर करू नका'),

(12, 'name', 'hi', 'मुलेठी'), (12, 'name', 'mr', 'जेष्ठमध'),
(12, 'uses', 'hi', 'गले की खराश और खांसी में लाभकारी'),
(12, 'uses', 'mr', 'घशातील खवखव आणि खोकल्यावर उपयुक्त'),
(12, 'contraindications', 'hi', 'उच्च रक्तचाप में उपयोग न करें'),
(12, 'contraindications', 'mr', 'उच्च रक्तदाबात वापर करू नका'),

(13, 'name', 'hi', 'सफेद मुसली'), (13, 'name', 'mr', 'सफेद मुसली'),
(13, 'uses', 'hi', 'कामोद्दीपक, शक्ति और स्फूर्ति बढ़ाने वाला'),
(13, 'uses', 'mr', 'कामोत्तेजक, शक्ती आणि उत्साह वाढवणारे'),
(13, 'contraindications', 'hi', 'मधुमेह में सावधानी से उपयोग करें'),
(13, 'contraindications', 'mr', 'मधुमेह असल्यास काळजीपूर्वक वापर करा'),

(14, 'name', 'hi', 'अर्जुन'), (14, 'name', 'mr', 'अर्जुन'),
(14, 'uses', 'hi', 'हृदय के लिए टॉनिक, रक्तचाप नियंत्रित करने वाला'),
(14, 'uses', 'mr', 'हृदयासाठी टॉनिक, रक्तदाब नियंत्रित करणारे'),
(14, 'contraindications', 'hi', 'रक्त पतला करने वाली दवाओं के साथ न लें'),
(14, 'contraindications', 'mr', 'रक्त पातळ करणाऱ्या औषधांसोबत घेऊ नका'),

(15, 'name', 'hi', 'मंजिष्ठा'), (15, 'name', 'mr', 'मंजिष्ठा'),
(15, 'uses', 'hi', 'रक्त शुद्ध करने वाला, त्वचा रोगों में उपयोगी'),
(15, 'uses', 'mr', 'रक्त शुद्ध करणारे, त्वचा रोगांवर उपयुक्त'),
(15, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(15, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर करू नका');

-- ======================
-- Ayurveda Herbs 21–30
-- ======================

-- Herbs
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications) VALUES
(21, 'Bhringraj', 'Eclipta alba', 'Ayurveda', 'Hair growth, liver health', 'Leaves, Roots', 'Wedelolactone', 'Avoid in hypotension'),
(22, 'Neem', 'Azadirachta indica', 'Ayurveda', 'Skin purifier, anti-parasitic', 'Leaves, Bark, Seeds', 'Azadirachtin', 'Avoid in pregnancy'),
(23, 'Ashoka', 'Saraca asoca', 'Ayurveda', 'Female reproductive health', 'Bark, Flowers', 'Flavonoids', 'Avoid in pregnancy without supervision'),
(24, 'Vidanga', 'Embelia ribes', 'Ayurveda', 'Anti-parasitic, digestive aid', 'Fruits', 'Embelin', 'Avoid in pregnancy'),
(25, 'Haritaki', 'Terminalia chebula', 'Ayurveda', 'Digestive aid, laxative, immunity', 'Fruits', 'Tannins', 'Avoid in severe diarrhea'),
(26, 'Bibhitaki', 'Terminalia bellirica', 'Ayurveda', 'Respiratory health, eye disorders', 'Fruits', 'Gallic acid', 'Avoid in dehydration'),
(27, 'Amalaki', 'Phyllanthus emblica', 'Ayurveda', 'Immunity booster, digestive health', 'Fruits', 'Vitamin C, Tannins', 'Avoid in hyperacidity'),
(28, 'Triphala', 'Combination of 3 fruits', 'Ayurveda', 'Digestive health, detoxification', 'Fruits', 'Tannins, Polyphenols', 'Avoid in loose motions'),
(29, 'Chitrak', 'Plumbago zeylanica', 'Ayurveda', 'Digestive stimulant, metabolism booster', 'Roots', 'Plumbagin', 'Avoid in ulcers, pregnancy'),
(30, 'Nagarmotha', 'Cyperus rotundus', 'Ayurveda', 'Digestive aid, fever relief', 'Rhizome', 'Cyperene', 'Avoid in constipation');

-- Common Names
INSERT INTO common_names (herb_id, name) VALUES
(21, 'Bhringraj'), (21, 'भृंगराज'), (21, 'भृंगराज'),
(22, 'Neem'), (22, 'नीम'), (22, 'कडुलिंब'),
(23, 'Ashoka'), (23, 'अशोक'), (23, 'अशोक'),
(24, 'Vidanga'), (24, 'विदंग'), (24, 'विदंग'),
(25, 'Haritaki'), (25, 'हरितकी'), (25, 'हिरडा'),
(26, 'Bibhitaki'), (26, 'बिभीतकी'), (26, 'बेहेडा'),
(27, 'Amalaki'), (27, 'आमलकी'), (27, 'आवळा'),
(28, 'Triphala'), (28, 'त्रिफला'), (28, 'त्रिफळा'),
(29, 'Chitrak'), (29, 'चित्रक'), (29, 'चित्रक'),
(30, 'Nagarmotha'), (30, 'नागरमोथा'), (30, 'नागरमोथा');

-- Remedies
INSERT INTO remedies (herb_id, condition_name, preparation, form) VALUES
(21, 'Hair growth', 'Apply Bhringraj oil on scalp', 'Oil'),
(21, 'Liver health', 'Bhringraj leaf juice with honey', 'Juice'),
(22, 'Skin problems', 'Apply Neem paste on skin', 'Topical'),
(22, 'Worm infection', 'Neem leaf decoction orally', 'Decoction'),
(23, 'Menstrual issues', 'Ashoka bark decoction with water', 'Decoction'),
(23, 'Female health tonic', 'Ashoka flower syrup', 'Syrup'),
(24, 'Intestinal worms', 'Vidanga fruit powder with warm water', 'Powder'),
(24, 'Digestive aid', 'Vidanga seed decoction', 'Decoction'),
(25, 'Immunity booster', 'Haritaki fruit powder with honey', 'Powder'),
(25, 'Constipation', 'Haritaki fruit decoction at night', 'Decoction'),
(26, 'Respiratory issues', 'Bibhitaki fruit powder with warm water', 'Powder'),
(26, 'Eye health', 'Bibhitaki fruit decoction for wash', 'Decoction'),
(27, 'Immunity', 'Amalaki juice daily in morning', 'Juice'),
(27, 'Digestion', 'Amalaki powder with warm water', 'Powder'),
(28, 'Detoxification', 'Triphala powder with warm water at night', 'Powder'),
(28, 'Constipation', 'Triphala decoction before bed', 'Decoction'),
(29, 'Appetite loss', 'Chitrak root powder with ghee', 'Powder'),
(29, 'Indigestion', 'Chitrak root decoction once daily', 'Decoction'),
(30, 'Fever', 'Nagarmotha rhizome decoction twice daily', 'Decoction'),
(30, 'Diarrhea', 'Nagarmotha powder with buttermilk', 'Powder');

-- Herb Languages
INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(21, 'name', 'hi', 'भृंगराज'), (21, 'name', 'mr', 'भृंगराज'),
(21, 'uses', 'hi', 'बालों की वृद्धि और यकृत स्वास्थ्य'),
(21, 'uses', 'mr', 'केस वाढीसाठी आणि यकृत आरोग्यासाठी'),
(21, 'contraindications', 'hi', 'निम्न रक्तचाप में उपयोग न करें'),
(21, 'contraindications', 'mr', 'कमी रक्तदाब असल्यास वापर करू नका'),

(22, 'name', 'hi', 'नीम'), (22, 'name', 'mr', 'कडुलिंब'),
(22, 'uses', 'hi', 'त्वचा की शुद्धि और परजीवी नाशक'),
(22, 'uses', 'mr', 'त्वचा शुद्ध करणारे आणि परजीवी नाशक'),
(22, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(22, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर करू नका'),

(23, 'name', 'hi', 'अशोक'), (23, 'name', 'mr', 'अशोक'),
(23, 'uses', 'hi', 'महिला प्रजनन स्वास्थ्य के लिए उपयोगी'),
(23, 'uses', 'mr', 'स्त्रियांच्या प्रजनन आरोग्यासाठी उपयुक्त'),
(23, 'contraindications', 'hi', 'गर्भावस्था में बिना निगरानी के उपयोग न करें'),
(23, 'contraindications', 'mr', 'गर्भावस्थेत डॉक्टरांच्या देखरेखीशिवाय वापर करू नका'),

(24, 'name', 'hi', 'विदंग'), (24, 'name', 'mr', 'विदंग'),
(24, 'uses', 'hi', 'कृमिनाशक और पाचन में सहायक'),
(24, 'uses', 'mr', 'कृमिनाशक आणि पचनासाठी उपयुक्त'),
(24, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(24, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर करू नका'),

(25, 'name', 'hi', 'हरितकी'), (25, 'name', 'mr', 'हिरडा'),
(25, 'uses', 'hi', 'पाचन सहायक, रेचक और रोग प्रतिकार शक्ति बढ़ाने वाला'),
(25, 'uses', 'mr', 'पचन सुधारक, जुलाब आणि रोगप्रतिकार शक्ती वाढवणारे'),
(25, 'contraindications', 'hi', 'गंभीर दस्त में उपयोग न करें'),
(25, 'contraindications', 'mr', 'तीव्र जुलाबात वापर करू नका');

-- ======================
-- Ayurveda Herbs 31–40
-- ======================

-- Herbs
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications) VALUES
(31, 'Shankhpushpi', 'Convolvulus pluricaulis', 'Ayurveda', 'Memory booster, anxiety relief', 'Whole plant', 'Alkaloids, Flavonoids', 'Avoid in hypotension'),
(32, 'Jatamansi', 'Nardostachys jatamansi', 'Ayurveda', 'Stress relief, sleep aid', 'Roots, Rhizomes', 'Nardosinone', 'Avoid in low blood pressure'),
(33, 'Giloy', 'Tinospora cordifolia', 'Ayurveda', 'Immunity booster, antipyretic', 'Stem', 'Tinosporin', 'Avoid in autoimmune conditions'),
(34, 'Kalmegh', 'Andrographis paniculata', 'Ayurveda', 'Liver tonic, fever reducer', 'Leaves', 'Andrographolide', 'Avoid in pregnancy'),
(35, 'Arjuna', 'Terminalia arjuna', 'Ayurveda', 'Cardiac tonic, blood pressure control', 'Bark', 'Arjunolic acid', 'Avoid in hypotension'),
(36, 'Shatavari', 'Asparagus racemosus', 'Ayurveda', 'Female health tonic, lactation support', 'Roots', 'Shatavarins', 'Avoid in kidney disorders'),
(37, 'Punarnava', 'Boerhavia diffusa', 'Ayurveda', 'Diuretic, kidney health', 'Roots, Whole plant', 'Boeravinone', 'Avoid in dehydration'),
(38, 'Guggul', 'Commiphora mukul', 'Ayurveda', 'Cholesterol management, arthritis relief', 'Resin', 'Guggulsterone', 'Avoid in hyperthyroidism'),
(39, 'Kutki', 'Picrorhiza kurroa', 'Ayurveda', 'Liver tonic, digestive aid', 'Rhizomes', 'Picroside', 'Avoid in diarrhea'),
(40, 'Mulethi', 'Glycyrrhiza glabra', 'Ayurveda', 'Cough relief, anti-inflammatory', 'Roots', 'Glycyrrhizin', 'Avoid in hypertension');

-- Common Names
INSERT INTO common_names (herb_id, name) VALUES
(31, 'Shankhpushpi'), (31, 'शंखपुष्पी'), (31, 'शंखपुष्पी'),
(32, 'Jatamansi'), (32, 'जटामांसी'), (32, 'जटामांसी'),
(33, 'Giloy'), (33, 'गिलोय'), (33, 'गुळवेल'),
(34, 'Kalmegh'), (34, 'कालमेघ'), (34, 'कालमेघ'),
(35, 'Arjuna'), (35, 'अर्जुन'), (35, 'अर्जुन'),
(36, 'Shatavari'), (36, 'शतावरी'), (36, 'शतावरी'),
(37, 'Punarnava'), (37, 'पुनर्नवा'), (37, 'पुनर्नवा'),
(38, 'Guggul'), (38, 'गुग्गुल'), (38, 'गुग्गुळ'),
(39, 'Kutki'), (39, 'कुटकी'), (39, 'कुटकी'),
(40, 'Mulethi'), (40, 'मुलेठी'), (40, 'जेष्ठमध');

-- Remedies
INSERT INTO remedies (herb_id, condition_name, preparation, form) VALUES
(31, 'Memory enhancer', 'Shankhpushpi syrup daily', 'Syrup'),
(31, 'Anxiety', 'Shankhpushpi powder with warm milk', 'Powder'),
(32, 'Stress', 'Jatamansi root powder with honey', 'Powder'),
(32, 'Sleep aid', 'Jatamansi decoction at night', 'Decoction'),
(33, 'Immunity', 'Giloy stem juice daily', 'Juice'),
(33, 'Fever', 'Giloy decoction with water', 'Decoction'),
(34, 'Liver tonic', 'Kalmegh leaf powder with honey', 'Powder'),
(34, 'Fever', 'Kalmegh decoction with water', 'Decoction'),
(35, 'Heart health', 'Arjuna bark decoction daily', 'Decoction'),
(35, 'Blood pressure', 'Arjuna bark powder with milk', 'Powder'),
(36, 'Female tonic', 'Shatavari root powder with milk', 'Powder'),
(36, 'Lactation support', 'Shatavari granules daily', 'Granules'),
(37, 'Kidney health', 'Punarnava root decoction daily', 'Decoction'),
(37, 'Edema', 'Punarnava juice twice daily', 'Juice'),
(38, 'Cholesterol', 'Guggul resin tablets daily', 'Tablet'),
(38, 'Arthritis', 'Guggul resin with warm water', 'Powder'),
(39, 'Liver health', 'Kutki powder with honey', 'Powder'),
(39, 'Digestion', 'Kutki rhizome decoction', 'Decoction'),
(40, 'Cough', 'Mulethi root powder with honey', 'Powder'),
(40, 'Sore throat', 'Mulethi decoction as gargle', 'Decoction');

-- Herb Languages
INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(31, 'name', 'hi', 'शंखपुष्पी'), (31, 'name', 'mr', 'शंखपुष्पी'),
(31, 'uses', 'hi', 'स्मृति बढ़ाने और चिंता कम करने में सहायक'),
(31, 'uses', 'mr', 'स्मरणशक्ती वाढवण्यासाठी आणि चिंता कमी करण्यासाठी उपयुक्त'),
(31, 'contraindications', 'hi', 'निम्न रक्तचाप में उपयोग न करें'),
(31, 'contraindications', 'mr', 'कमी रक्तदाबात वापर करू नका'),

(32, 'name', 'hi', 'जटामांसी'), (32, 'name', 'mr', 'जटामांसी'),
(32, 'uses', 'hi', 'तनाव कम करने और नींद लाने में सहायक'),
(32, 'uses', 'mr', 'ताण कमी करण्यासाठी आणि झोपेसाठी उपयुक्त'),
(32, 'contraindications', 'hi', 'निम्न रक्तचाप में उपयोग न करें'),
(32, 'contraindications', 'mr', 'कमी रक्तदाब असल्यास वापर करू नका'),

(33, 'name', 'hi', 'गिलोय'), (33, 'name', 'mr', 'गुळवेल'),
(33, 'uses', 'hi', 'प्रतिरक्षा बढ़ाने और बुखार में लाभकारी'),
(33, 'uses', 'mr', 'रोग प्रतिकार शक्ती वाढवण्यासाठी आणि तापात उपयुक्त'),
(33, 'contraindications', 'hi', 'स्व-प्रतिरक्षा रोगों में उपयोग न करें'),
(33, 'contraindications', 'mr', 'ऑटोइम्यून आजारांमध्ये वापर करू नका'),

(34, 'name', 'hi', 'कालमेघ'), (34, 'name', 'mr', 'कालमेघ'),
(34, 'uses', 'hi', 'यकृत टॉनिक और बुखार में लाभकारी'),
(34, 'uses', 'mr', 'यकृतासाठी टॉनिक आणि तापावर उपयुक्त'),
(34, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(34, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर करू नका'),

(35, 'name', 'hi', 'अर्जुन'), (35, 'name', 'mr', 'अर्जुन'),
(35, 'uses', 'hi', 'हृदय स्वास्थ्य और रक्तचाप नियंत्रण में सहायक'),
(35, 'uses', 'mr', 'हृदय आरोग्य आणि रक्तदाब नियंत्रणासाठी उपयुक्त'),
(35, 'contraindications', 'hi', 'निम्न रक्तचाप में उपयोग न करें'),
(35, 'contraindications', 'mr', 'कमी रक्तदाबात वापर करू नका'),

(36, 'name', 'hi', 'शतावरी'),
(36, 'name', 'mr', 'शतावरी'),
(36, 'uses', 'hi', 'स्त्री स्वास्थ्य टॉनिक, स्तनपान में सहायक'),
(36, 'uses', 'mr', 'स्त्री आरोग्यासाठी टॉनिक, दूध वाढवण्यासाठी उपयुक्त'),
(36, 'contraindications', 'hi', 'किडनी की समस्याओं में सावधानी बरतें'),
(36, 'contraindications', 'mr', 'किडनी विकार असल्यास सावधगिरी बाळगा'),

(37, 'name', 'hi', 'पुनर्नवा'),
(37, 'name', 'mr', 'पुनर्नवा'),
(37, 'uses', 'hi', 'मूत्रवर्धक, गुर्दे के लिए लाभकारी'),
(37, 'uses', 'mr', 'मूत्रवर्धक, किडनी आरोग्यासाठी उपयुक्त'),
(37, 'contraindications', 'hi', 'निर्जलीकरण में उपयोग न करें'),
(37, 'contraindications', 'mr', 'निर्जलीकरण असल्यास वापरू नका'),

(38, 'name', 'hi', 'गुग्गुल'),
(38, 'name', 'mr', 'गुग्गुळ'),
(38, 'uses', 'hi', 'कोलेस्ट्रॉल नियंत्रण और गठिया में राहत'),
(38, 'uses', 'mr', 'कोलेस्टेरॉल नियंत्रण आणि सांधेदुखीत आराम'),
(38, 'contraindications', 'hi', 'हाइपरथायरॉयडिज्म में उपयोग न करें'),
(38, 'contraindications', 'mr', 'हायपरथायरॉईडीझममध्ये वापर टाळा'),

(39, 'name', 'hi', 'कुटकी'),
(39, 'name', 'mr', 'कुटकी'),
(39, 'uses', 'hi', 'यकृत टॉनिक और पाचन में सहायक'),
(39, 'uses', 'mr', 'यकृत टॉनिक आणि पचनासाठी उपयुक्त'),
(39, 'contraindications', 'hi', 'दस्त की स्थिति में उपयोग न करें'),
(39, 'contraindications', 'mr', 'दस्त असल्यास वापरू नका'),

(40, 'name', 'hi', 'मुलेठी'),
(40, 'name', 'mr', 'जेष्ठमध'),
(40, 'uses', 'hi', 'खांसी और गले के दर्द में उपयोगी'),
(40, 'uses', 'mr', 'खोकल्यावर व घशातील वेदना साठी उपयुक्त'),
(40, 'contraindications', 'hi', 'उच्च रक्तचाप में परहेज़ करें'),
(40, 'contraindications', 'mr', 'उच्च रक्तदाब असल्यास वापर टाळा');

-- ======================
-- Ayurveda Herbs 41–50
-- ======================

-- Herbs
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications) VALUES
(41, 'Manjistha', 'Rubia cordifolia', 'Ayurveda', 'Blood purifier, skin health', 'Roots', 'Alizarin, Purpurin', 'Avoid in pregnancy'),
(42, 'Bala', 'Sida cordifolia', 'Ayurveda', 'Strength, nerve tonic', 'Roots, Leaves', 'Ephedrine, Sterols', 'Avoid in hypertension'),
(43, 'Atibala', 'Abutilon indicum', 'Ayurveda', 'Anti-inflammatory, nerve tonic', 'Roots, Seeds', 'Flavonoids', 'Avoid in hypotension'),
(44, 'Shigru', 'Moringa oleifera', 'Ayurveda', 'Nutrient-rich, anti-inflammatory', 'Leaves, Pods', 'Moringinine, Vitamin C', 'Avoid in thyroid disorders'),
(45, 'Vacha', 'Acorus calamus', 'Ayurveda', 'Memory enhancer, digestion aid', 'Rhizomes', 'Beta-asarone', 'Avoid in pregnancy'),
(46, 'Tagar', 'Valeriana wallichii', 'Ayurveda', 'Sleep aid, anxiety relief', 'Roots', 'Valepotriates', 'Avoid in pregnancy and children'),
(47, 'Karpura', 'Cinnamomum camphora', 'Ayurveda', 'Decongestant, pain relief', 'Wood, Oil', 'Camphor', 'Avoid in infants'),
(48, 'Ela', 'Elettaria cardamomum', 'Ayurveda', 'Digestive aid, mouth freshener', 'Seeds', 'Cineole, Terpinyl acetate', 'Avoid in gallstones'),
(49, 'Dalchini', 'Cinnamomum verum', 'Ayurveda', 'Digestive stimulant, blood sugar control', 'Bark', 'Cinnamaldehyde', 'Avoid in ulcers'),
(50, 'Lodhra', 'Symplocos racemosa', 'Ayurveda', 'Gynecological health, wound healing', 'Bark', 'Symplocoside', 'Avoid in pregnancy');

-- Common Names
INSERT INTO common_names (herb_id, name) VALUES
(41, 'Manjistha'), (41, 'मंजिष्ठा'), (41, 'मंजिष्ठा'),
(42, 'Bala'), (42, 'बला'), (42, 'बळा'),
(43, 'Atibala'), (43, 'अतिबला'), (43, 'अतिबळा'),
(44, 'Shigru'), (44, 'शिग्रु'), (44, 'शेवगा'),
(45, 'Vacha'), (45, 'वचा'), (45, 'वचा'),
(46, 'Tagar'), (46, 'तगर'), (46, 'टगर'),
(47, 'Karpura'), (47, 'कर्पूर'), (47, 'कापूर'),
(48, 'Ela'), (48, 'एला'), (48, 'वेलची'),
(49, 'Dalchini'), (49, 'दालचीनी'), (49, 'दालचिनी'),
(50, 'Lodhra'), (50, 'लोढ्रा'), (50, 'लोढ्र');

-- Remedies
INSERT INTO remedies (herb_id, condition_name, preparation, form) VALUES
(41, 'Skin health', 'Manjistha root decoction daily', 'Decoction'),
(41, 'Blood purifier', 'Manjistha powder with honey', 'Powder'),
(42, 'Weakness', 'Bala root decoction daily', 'Decoction'),
(42, 'Nerve tonic', 'Bala powder with milk', 'Powder'),
(43, 'Inflammation', 'Atibala seed paste on affected area', 'Paste'),
(43, 'Nerve health', 'Atibala root decoction daily', 'Decoction'),
(44, 'Nutrition', 'Shigru leaf powder in meals', 'Powder'),
(44, 'Inflammation', 'Shigru leaf decoction', 'Decoction'),
(45, 'Memory', 'Vacha root powder with honey', 'Powder'),
(45, 'Digestion', 'Vacha decoction with water', 'Decoction'),
(46, 'Insomnia', 'Tagar root decoction at night', 'Decoction'),
(46, 'Anxiety', 'Tagar root powder with honey', 'Powder'),
(47, 'Cold', 'Inhale Karpura vapors', 'Inhalation'),
(47, 'Pain', 'Apply Karpura oil on joints', 'Oil'),
(48, 'Digestion', 'Ela seeds chewed after meals', 'Raw'),
(48, 'Mouth freshener', 'Ela seed decoction', 'Decoction'),
(49, 'Blood sugar', 'Dalchini bark decoction daily', 'Decoction'),
(49, 'Digestion', 'Dalchini powder in food', 'Powder'),
(50, 'Menstrual issues', 'Lodhra bark decoction daily', 'Decoction'),
(50, 'Wounds', 'Lodhra bark paste applied topically', 'Paste');

-- Herb Languages
INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
-- 41 Manjistha
(41, 'name', 'hi', 'मंजिष्ठा'), (41, 'name', 'mr', 'मंजिष्ठा'),
(41, 'uses', 'hi', 'रक्त शुद्ध करने और त्वचा स्वास्थ्य में सहायक'),
(41, 'uses', 'mr', 'रक्त शुद्धीकरण आणि त्वचा आरोग्यासाठी उपयुक्त'),
(41, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(41, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा'),

-- 42 Bala
(42, 'name', 'hi', 'बला'), (42, 'name', 'mr', 'बळा'),
(42, 'uses', 'hi', 'शक्ति प्रदान करने वाला और स्नायु टॉनिक'),
(42, 'uses', 'mr', 'शक्तिवर्धक आणि मज्जासंस्थेचे टॉनिक'),
(42, 'contraindications', 'hi', 'उच्च रक्तचाप में उपयोग न करें'),
(42, 'contraindications', 'mr', 'उच्च रक्तदाब असल्यास वापरू नका'),

-- 43 Atibala
(43, 'name', 'hi', 'अतिबला'), (43, 'name', 'mr', 'अतिबळा'),
(43, 'uses', 'hi', 'सूजन कम करने और स्नायु टॉनिक'),
(43, 'uses', 'mr', 'दाह कमी करणारे आणि मज्जासंस्थेचे टॉनिक'),
(43, 'contraindications', 'hi', 'निम्न रक्तचाप में उपयोग न करें'),
(43, 'contraindications', 'mr', 'कमी रक्तदाब असल्यास वापरू नका'),

-- 44 Shigru
(44, 'name', 'hi', 'शिग्रु'), (44, 'name', 'mr', 'शेवगा'),
(44, 'uses', 'hi', 'पोषक तत्वों से भरपूर और सूजन में सहायक'),
(44, 'uses', 'mr', 'पोषक तत्वांनी समृद्ध आणि दाह कमी करणारे'),
(44, 'contraindications', 'hi', 'थायरॉयड विकारों में उपयोग से बचें'),
(44, 'contraindications', 'mr', 'थायरॉईड विकारांमध्ये वापर टाळा'),

-- 45 Vacha
(45, 'name', 'hi', 'वचा'), (45, 'name', 'mr', 'वचा'),
(45, 'uses', 'hi', 'स्मरणशक्ति बढ़ाने और पाचन में सहायक'),
(45, 'uses', 'mr', 'स्मरणशक्ती वाढवणारे आणि पचनासाठी उपयुक्त'),
(45, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(45, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा'),

-- 46 Tagar
(46, 'name', 'hi', 'तगर'), (46, 'name', 'mr', 'टगर'),
(46, 'uses', 'hi', 'नींद लाने और चिंता कम करने में सहायक'),
(46, 'uses', 'mr', 'झोप आणणारे आणि चिंता कमी करणारे'),
(46, 'contraindications', 'hi', 'गर्भावस्था और बच्चों में उपयोग न करें'),
(46, 'contraindications', 'mr', 'गर्भवती व लहान मुलांमध्ये वापरू नका'),

-- 47 Karpura
(47, 'name', 'hi', 'कर्पूर'), (47, 'name', 'mr', 'कापूर'),
(47, 'uses', 'hi', 'नाक बंद में राहत और दर्द निवारण'),
(47, 'uses', 'mr', 'नाक बंद झाल्यास आराम आणि वेदनाशामक'),
(47, 'contraindications', 'hi', 'शिशुओं में उपयोग न करें'),
(47, 'contraindications', 'mr', 'लहान बालकांमध्ये वापरू नका'),

-- 48 Ela
(48, 'name', 'hi', 'एला'), (48, 'name', 'mr', 'वेलची'),
(48, 'uses', 'hi', 'पाचन में सहायक और मुखशुद्धि करने वाला'),
(48, 'uses', 'mr', 'पचनासाठी उपयुक्त आणि तोंडाची दुर्गंधी दूर करणारे'),
(48, 'contraindications', 'hi', 'पित्ताशय की पथरी में सावधानी बरतें'),
(48, 'contraindications', 'mr', 'पित्ताशयातील खडे असल्यास काळजी घ्या'),

-- 49 Dalchini
(49, 'name', 'hi', 'दालचीनी'), (49, 'name', 'mr', 'दालचिनी'),
(49, 'uses', 'hi', 'पाचन में सहायक और रक्त शर्करा नियंत्रण'),
(49, 'uses', 'mr', 'पचन सुधारक आणि रक्तशर्करा नियंत्रणासाठी उपयुक्त'),
(49, 'contraindications', 'hi', 'अल्सर में उपयोग न करें'),
(49, 'contraindications', 'mr', 'अल्सर असल्यास वापर टाळा'),

-- 50 Lodhra
(50, 'name', 'hi', 'लोढ्रा'), (50, 'name', 'mr', 'लोढ्र'),
(50, 'uses', 'hi', 'स्त्री रोग स्वास्थ्य और घाव भरने में सहायक'),
(50, 'uses', 'mr', 'स्त्रीरोग आरोग्यासाठी आणि जखम भरण्यासाठी उपयुक्त'),
(50, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(50, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा');

-- ======================
-- Ayurveda Herbs 51–60
-- ======================

-- Herbs
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications) VALUES
(51, 'Aragvadha', 'Cassia fistula', 'Ayurveda', 'Mild laxative, skin health', 'Pods, Bark', 'Anthraquinones', 'Avoid in diarrhea'),
(52, 'Kutaja', 'Holarrhena antidysenterica', 'Ayurveda', 'Anti-dysenteric, intestinal health', 'Bark, Seeds', 'Conessine, Alkaloids', 'Avoid in constipation'),
(53, 'Vidanga', 'Embelia ribes', 'Ayurveda', 'Anti-parasitic, digestive health', 'Fruits', 'Embelin', 'Avoid in pregnancy'),
(54, 'Nimba', 'Azadirachta indica', 'Ayurveda', 'Antibacterial, skin purifier', 'Leaves, Bark, Seeds', 'Azadirachtin, Nimbin', 'Avoid in severe liver disorders'),
(55, 'Jatamansi', 'Nardostachys jatamansi', 'Ayurveda', 'Calming, sleep aid', 'Roots', 'Jatamansone', 'Avoid in low blood pressure'),
(56, 'Haridra', 'Curcuma longa', 'Ayurveda', 'Anti-inflammatory, antioxidant', 'Rhizomes', 'Curcumin', 'Avoid in gallstones'),
(57, 'Daruharidra', 'Berberis aristata', 'Ayurveda', 'Eye health, skin conditions', 'Roots, Stem', 'Berberine', 'Avoid in pregnancy'),
(58, 'Bhunimba', 'Andrographis paniculata', 'Ayurveda', 'Liver tonic, immunity booster', 'Leaves', 'Andrographolide', 'Avoid in pregnancy'),
(59, 'Guduchi Satva', 'Tinospora cordifolia extract', 'Ayurveda', 'Immunity booster, fever reduction', 'Extract', 'Alkaloids, Glycosides', 'Avoid in autoimmune conditions'),
(60, 'Amla', 'Phyllanthus emblica', 'Ayurveda', 'Vitamin C rich, rejuvenative', 'Fruit', 'Ascorbic acid, Tannins', 'Avoid in hyperacidity');

-- Common Names
INSERT INTO common_names (herb_id, name) VALUES
(51, 'Aragvadha'), (51, 'आरग्वध'), (51, 'बहावा'),
(52, 'Kutaja'), (52, 'कुटज'), (52, 'कुटज'),
(53, 'Vidanga'), (53, 'विडंग'), (53, 'विडंग'),
(54, 'Nimba'), (54, 'नीम'), (54, 'कडुनिंब'),
(55, 'Jatamansi'), (55, 'जटामांसी'), (55, 'जटामांसी'),
(56, 'Haridra'), (56, 'हल्दी'), (56, 'हळद'),
(57, 'Daruharidra'), (57, 'दारुहरिद्रा'), (57, 'दारुहरिद्रा'),
(58, 'Bhunimba'), (58, 'भूनिंबा'), (58, 'भूनिंबा'),
(59, 'Guduchi Satva'), (59, 'गुडूची सत्व'), (59, 'गुळवेल सत्व'),
(60, 'Amla'), (60, 'आंवला'), (60, 'आवळा');

-- Remedies
INSERT INTO remedies (herb_id, condition_name, preparation, form) VALUES
(51, 'Constipation', 'Aragvadha pulp with water at night', 'Pulp'),
(51, 'Skin health', 'Aragvadha bark decoction', 'Decoction'),
(52, 'Diarrhea', 'Kutaja bark decoction twice daily', 'Decoction'),
(52, 'Intestinal health', 'Kutaja seed powder with honey', 'Powder'),
(53, 'Worm infestation', 'Vidanga fruit powder with milk', 'Powder'),
(53, 'Digestive health', 'Vidanga decoction after meals', 'Decoction'),
(54, 'Skin diseases', 'Nimba leaf paste on affected area', 'Paste'),
(54, 'Antibacterial', 'Nimba leaf juice daily', 'Juice'),
(55, 'Insomnia', 'Jatamansi root decoction at bedtime', 'Decoction'),
(55, 'Stress', 'Jatamansi root powder with honey', 'Powder'),
(56, 'Inflammation', 'Haridra powder with milk daily', 'Powder'),
(56, 'Antioxidant', 'Haridra decoction with warm water', 'Decoction'),
(57, 'Eye health', 'Daruharidra decoction as eyewash', 'Decoction'),
(57, 'Skin conditions', 'Daruharidra paste applied topically', 'Paste'),
(58, 'Liver health', 'Bhunimba leaf decoction daily', 'Decoction'),
(58, 'Immunity', 'Bhunimba leaf powder with honey', 'Powder'),
(59, 'Fever', 'Guduchi Satva mixed with water', 'Extract'),
(59, 'Immunity', 'Guduchi Satva with honey', 'Extract'),
(60, 'Rejuvenation', 'Amla fruit raw or juice daily', 'Raw/Juice'),
(60, 'Vitamin C supplement', 'Amla powder with water', 'Powder');

-- Herb Languages
INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
-- 51 Aragvadha
(51, 'name', 'hi', 'आरग्वध'), (51, 'name', 'mr', 'बहावा'),
(51, 'uses', 'hi', 'हल्का रेचक और त्वचा स्वास्थ्य'),
(51, 'uses', 'mr', 'मंद जुलाब आणि त्वचा आरोग्यासाठी उपयुक्त'),
(51, 'contraindications', 'hi', 'दस्त में उपयोग न करें'),
(51, 'contraindications', 'mr', 'जुलाब असल्यास वापरू नका'),

-- 52 Kutaja
(52, 'name', 'hi', 'कुटज'), (52, 'name', 'mr', 'कुटज'),
(52, 'uses', 'hi', 'अतिसार और आंतों के स्वास्थ्य में सहायक'),
(52, 'uses', 'mr', 'अतिसार आणि आंत आरोग्यासाठी उपयुक्त'),
(52, 'contraindications', 'hi', 'कब्ज में उपयोग न करें'),
(52, 'contraindications', 'mr', 'बद्धकोष्ठ असल्यास वापरू नका'),

-- 53 Vidanga
(53, 'name', 'hi', 'विडंग'), (53, 'name', 'mr', 'विडंग'),
(53, 'uses', 'hi', 'कृमिनाशक और पाचन स्वास्थ्य में सहायक'),
(53, 'uses', 'mr', 'कृमिनाशक आणि पचन आरोग्यासाठी उपयुक्त'),
(53, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(53, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा'),

-- 54 Nimba
(54, 'name', 'hi', 'नीम'), (54, 'name', 'mr', 'कडुनिंब'),
(54, 'uses', 'hi', 'जीवाणुरोधी और त्वचा शुद्ध करने वाला'),
(54, 'uses', 'mr', 'प्रतिजैविक आणि त्वचा शुद्ध करणारे'),
(54, 'contraindications', 'hi', 'गंभीर यकृत विकारों में उपयोग न करें'),
(54, 'contraindications', 'mr', 'गंभीर यकृत विकार असल्यास वापरू नका'),

-- 55 Jatamansi
(55, 'name', 'hi', 'जटामांसी'), (55, 'name', 'mr', 'जटामांसी'),
(55, 'uses', 'hi', 'मन को शांत करने और नींद में सहायक'),
(55, 'uses', 'mr', 'मन शांत करणारे आणि झोपेसाठी उपयुक्त'),
(55, 'contraindications', 'hi', 'निम्न रक्तचाप में उपयोग न करें'),
(55, 'contraindications', 'mr', 'कमी रक्तदाब असल्यास वापरू नका'),

-- 56 Haridra
(56, 'name', 'hi', 'हल्दी'), (56, 'name', 'mr', 'हळद'),
(56, 'uses', 'hi', 'सूजन कम करने और एंटीऑक्सीडेंट'),
(56, 'uses', 'mr', 'दाह कमी करणारे आणि प्रतिऑक्सिडंट'),
(56, 'contraindications', 'hi', 'पित्ताशय की पथरी में उपयोग न करें'),
(56, 'contraindications', 'mr', 'पित्ताशयातील खडे असल्यास वापर टाळा'),

-- 57 Daruharidra
(57, 'name', 'hi', 'दारुहरिद्रा'), (57, 'name', 'mr', 'दारुहरिद्रा'),
(57, 'uses', 'hi', 'नेत्र स्वास्थ्य और त्वचा रोगों में सहायक'),
(57, 'uses', 'mr', 'नेत्र आरोग्य आणि त्वचारोगांमध्ये उपयुक्त'),
(57, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(57, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा'),

-- 58 Bhunimba
(58, 'name', 'hi', 'भूनिंबा'), (58, 'name', 'mr', 'भूनिंबा'),
(58, 'uses', 'hi', 'यकृत टॉनिक और रोग प्रतिकारक शक्ति बढ़ाने वाला'),
(58, 'uses', 'mr', 'यकृत टॉनिक आणि रोगप्रतिकारशक्ती वाढवणारे'),
(58, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(58, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा'),

-- 59 Guduchi Satva
(59, 'name', 'hi', 'गुडूची सत्व'), (59, 'name', 'mr', 'गुळवेल सत्व'),
(59, 'uses', 'hi', 'प्रतिरक्षा शक्ति बढ़ाने और ज्वर कम करने में सहायक'),
(59, 'uses', 'mr', 'रोगप्रतिकारशक्ती वाढवणारे आणि ताप कमी करणारे'),
(59, 'contraindications', 'hi', 'ऑटोइम्यून रोगों में उपयोग से बचें'),
(59, 'contraindications', 'mr', 'स्वप्रतिरक्षी आजार असल्यास वापर टाळा'),

-- 60 Amla
(60, 'name', 'hi', 'आंवला'), (60, 'name', 'mr', 'आवळा'),
(60, 'uses', 'hi', 'विटामिन C से भरपूर और पुनर्योजी'),
(60, 'uses', 'mr', 'विटामिन C ने समृद्ध आणि पुनरुज्जीवक'),
(60, 'contraindications', 'hi', 'अत्यधिक अम्लता में उपयोग न करें'),
(60, 'contraindications', 'mr', 'जास्त आम्लपित्त असल्यास वापरू नका');

-- ======================
-- Ayurveda Herbs 61–70
-- ======================

-- Herbs
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications) VALUES
(61, 'Pippali', 'Piper longum', 'Ayurveda', 'Respiratory health, digestion stimulant', 'Fruits', 'Piperine', 'Avoid in gastric ulcers'),
(62, 'Maricha', 'Piper nigrum', 'Ayurveda', 'Appetite stimulant, cough relief', 'Fruits', 'Piperine, Chavicine', 'Avoid in stomach irritation'),
(63, 'Shunthi', 'Zingiber officinale', 'Ayurveda', 'Digestive aid, anti-inflammatory', 'Rhizome', 'Gingerol, Shogaol', 'Avoid in acid reflux'),
(64, 'Yashtimadhu', 'Glycyrrhiza glabra', 'Ayurveda', 'Soothes throat, ulcers remedy', 'Roots', 'Glycyrrhizin', 'Avoid in high blood pressure'),
(65, 'Shankhapushpi', 'Convolvulus pluricaulis', 'Ayurveda', 'Memory enhancer, calming', 'Whole plant', 'Alkaloids, Flavonoids', 'Avoid in low blood pressure'),
(66, 'Mandukaparni', 'Centella asiatica', 'Ayurveda', 'Memory booster, wound healing', 'Leaves', 'Asiaticoside', 'Avoid in liver disease'),
(67, 'Tagara', 'Valeriana wallichii', 'Ayurveda', 'Sleep aid, calming herb', 'Roots', 'Valepotriates', 'Avoid in pregnancy'),
(68, 'Kachur', 'Curcuma zedoaria', 'Ayurveda', 'Digestive stimulant, anti-inflammatory', 'Rhizome', 'Curcuminoids', 'Avoid in pregnancy'),
(69, 'Patha', 'Cissampelos pareira', 'Ayurveda', 'Urinary health, antipyretic', 'Roots', 'Isoquinoline alkaloids', 'Avoid in pregnancy'),
(70, 'Eranda', 'Ricinus communis', 'Ayurveda', 'Laxative, joint pain relief', 'Seeds, Leaves', 'Ricinoleic acid', 'Avoid in pregnancy');

-- Common Names
INSERT INTO common_names (herb_id, name) VALUES
(61, 'Pippali'), (61, 'पिप्पली'), (61, 'पिप्पली'),
(62, 'Maricha'), (62, 'काली मिर्च'), (62, 'मिरी'),
(63, 'Shunthi'), (63, 'सौंठ'), (63, 'सुंठ'),
(64, 'Yashtimadhu'), (64, 'मुलेठी'), (64, 'जेष्ठमध'),
(65, 'Shankhapushpi'), (65, 'शंखपुष्पी'), (65, 'शंखपुष्पी'),
(66, 'Mandukaparni'), (66, 'मंडूकपर्णी'), (66, 'मंडूकपर्णी'),
(67, 'Tagara'), (67, 'तगर'), (67, 'तगर'),
(68, 'Kachur'), (68, 'कचूर'), (68, 'कचुरा'),
(69, 'Patha'), (69, 'पाठा'), (69, 'पाठा'),
(70, 'Eranda'), (70, 'एरण्ड'), (70, 'एरंड');

-- Remedies
INSERT INTO remedies (herb_id, condition_name, preparation, form) VALUES
(61, 'Asthma', 'Pippali powder with honey twice daily', 'Powder'),
(61, 'Digestion', 'Pippali decoction after meals', 'Decoction'),
(62, 'Cough', 'Maricha powder with honey', 'Powder'),
(62, 'Appetite', 'Maricha fruit decoction before meals', 'Decoction'),
(63, 'Indigestion', 'Shunthi powder with warm water', 'Powder'),
(63, 'Inflammation', 'Shunthi decoction twice daily', 'Decoction'),
(64, 'Sore throat', 'Yashtimadhu decoction as gargle', 'Decoction'),
(64, 'Ulcers', 'Yashtimadhu root powder with milk', 'Powder'),
(65, 'Memory', 'Shankhapushpi juice with milk', 'Juice'),
(65, 'Anxiety', 'Shankhapushpi powder with honey', 'Powder'),
(66, 'Memory booster', 'Mandukaparni leaf juice daily', 'Juice'),
(66, 'Wound healing', 'Mandukaparni paste on wounds', 'Paste'),
(67, 'Insomnia', 'Tagara root decoction before bed', 'Decoction'),
(67, 'Stress relief', 'Tagara powder with honey', 'Powder'),
(68, 'Digestive stimulant', 'Kachur rhizome powder with honey', 'Powder'),
(68, 'Anti-inflammatory', 'Kachur decoction with warm water', 'Decoction'),
(69, 'Fever', 'Patha root decoction daily', 'Decoction'),
(69, 'Urinary health', 'Patha paste with water', 'Paste'),
(70, 'Constipation', 'Eranda oil with warm water', 'Oil'),
(70, 'Joint pain', 'Eranda leaf paste applied topically', 'Paste');

-- Herb Languages
INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
-- 61 Pippali
(61, 'name', 'hi', 'पिप्पली'), (61, 'name', 'mr', 'पिप्पली'),
(61, 'uses', 'hi', 'श्वसन स्वास्थ्य और पाचन को उत्तेजित करने वाला'),
(61, 'uses', 'mr', 'श्वसन आरोग्यासाठी आणि पचनास उत्तेजन देणारे'),
(61, 'contraindications', 'hi', 'गैस्ट्रिक अल्सर में उपयोग न करें'),
(61, 'contraindications', 'mr', 'पोटातील अल्सर असल्यास वापर टाळा'),

-- 62 Maricha
(62, 'name', 'hi', 'काली मिर्च'), (62, 'name', 'mr', 'मिरी'),
(62, 'uses', 'hi', 'भूख बढ़ाने और खांसी में राहत देने वाला'),
(62, 'uses', 'mr', 'भूक वाढवणारे आणि खोकल्यावर आराम देणारे'),
(62, 'contraindications', 'hi', 'पेट की जलन में उपयोग न करें'),
(62, 'contraindications', 'mr', 'पोट जळजळ असल्यास वापर टाळा'),

-- 63 Shunthi
(63, 'name', 'hi', 'सौंठ'), (63, 'name', 'mr', 'सुंठ'),
(63, 'uses', 'hi', 'पाचन में सहायक और सूजन कम करने वाला'),
(63, 'uses', 'mr', 'पचनास मदत करणारे आणि दाह कमी करणारे'),
(63, 'contraindications', 'hi', 'अम्लपित्त में उपयोग न करें'),
(63, 'contraindications', 'mr', 'अम्लपित्त असल्यास वापर टाळा'),

-- 64 Yashtimadhu
(64, 'name', 'hi', 'मुलेठी'), (64, 'name', 'mr', 'जेष्ठमध'),
(64, 'uses', 'hi', 'गले को आराम देने और अल्सर में सहायक'),
(64, 'uses', 'mr', 'घशातील वेदना कमी करणारे आणि अल्सरमध्ये उपयुक्त'),
(64, 'contraindications', 'hi', 'उच्च रक्तचाप में उपयोग न करें'),
(64, 'contraindications', 'mr', 'उच्च रक्तदाब असल्यास वापर टाळा'),

-- 65 Shankhapushpi
(65, 'name', 'hi', 'शंखपुष्पी'), (65, 'name', 'mr', 'शंखपुष्पी'),
(65, 'uses', 'hi', 'स्मरण शक्ति बढ़ाने और मन को शांत करने वाला'),
(65, 'uses', 'mr', 'स्मरणशक्ती वाढवणारे आणि मन शांत करणारे'),
(65, 'contraindications', 'hi', 'निम्न रक्तचाप में उपयोग न करें'),
(65, 'contraindications', 'mr', 'कमी रक्तदाब असल्यास वापर टाळा'),

-- 66 Mandukaparni
(66, 'name', 'hi', 'मंडूकपर्णी'), (66, 'name', 'mr', 'मंडूकपर्णी'),
(66, 'uses', 'hi', 'स्मृति बढ़ाने और घाव भरने में सहायक'),
(66, 'uses', 'mr', 'स्मरणशक्ती वाढवणारे आणि जखम भरण्यास उपयुक्त'),
(66, 'contraindications', 'hi', 'यकृत रोगों में उपयोग न करें'),
(66, 'contraindications', 'mr', 'यकृत विकार असल्यास वापर टाळा'),

-- 67 Tagara
(67, 'name', 'hi', 'तगर'), (67, 'name', 'mr', 'तगर'),
(67, 'uses', 'hi', 'नींद लाने और मन को शांत करने वाला'),
(67, 'uses', 'mr', 'झोपेस मदत करणारे आणि मन शांत करणारे'),
(67, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(67, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा'),

-- 68 Kachur
(68, 'name', 'hi', 'कचूर'), (68, 'name', 'mr', 'कचुरा'),
(68, 'uses', 'hi', 'पाचन को उत्तेजित करने और सूजन कम करने वाला'),
(68, 'uses', 'mr', 'पचन उत्तेजित करणारे आणि दाह कमी करणारे'),
(68, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(68, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा'),

-- 69 Patha
(69, 'name', 'hi', 'पाठा'), (69, 'name', 'mr', 'पाठा'),
(69, 'uses', 'hi', 'मूत्र मार्ग स्वास्थ्य और ज्वर नाशक'),
(69, 'uses', 'mr', 'मूत्र आरोग्यासाठी आणि ताप कमी करणारे'),
(69, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(69, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा'),

-- 70 Eranda
(70, 'name', 'hi', 'एरण्ड'), (70, 'name', 'mr', 'एरंड'),
(70, 'uses', 'hi', 'जुलाब और जोड़ों के दर्द में सहायक'),
(70, 'uses', 'mr', 'जुलाब आणणारे आणि सांधेदुखीत उपयुक्त'),
(70, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(70, 'contraindications', 'mr', 'गर्भावस्थेदरम्यान वापर टाळा');

-- =========================
-- Ayurveda Herbs 71–80
-- =========================

-- 71. Bakuchi (Psoralea corylifolia)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (71, 'Bakuchi', 'Psoralea corylifolia', 'Ayurveda', 'Skin disorders, vitiligo, leprosy', 'Seeds', 'Psoralen, Isopsoralen', 'Avoid in pregnancy and sensitive skin conditions');

INSERT INTO common_names (herb_id, name) VALUES
(71, 'Bakuchi'),
(71, 'बकुची'),
(71, 'बावची');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(71, 'name', 'hi', 'बकुची'),
(71, 'name', 'mr', 'बावची'),
(71, 'uses', 'hi', 'त्वचा रोग, श्वेतकुष्ठ और कोढ़ में उपयोगी'),
(71, 'uses', 'mr', 'त्वचारोग, श्वेतकुष्ठ व कुष्ठरोगावर उपयुक्त'),
(71, 'contraindications', 'hi', 'गर्भावस्था और संवेदनशील त्वचा में उपयोग न करें'),
(71, 'contraindications', 'mr', 'गर्भावस्था व संवेदनशील त्वचेत वापर टाळा');

-- 72. Lodhra (Symplocos racemosa)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (72, 'Lodhra', 'Symplocos racemosa', 'Ayurveda', 'Gynecological disorders, wound healing', 'Bark', 'Lodhraquinone, Symplocoside', 'Avoid in chronic constipation');

INSERT INTO common_names (herb_id, name) VALUES
(72, 'Lodhra'),
(72, 'लोध्र'),
(72, 'लोध्र');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(72, 'name', 'hi', 'लोध्र'),
(72, 'name', 'mr', 'लोध्र'),
(72, 'uses', 'hi', 'स्त्री रोग और घाव भरने में सहायक'),
(72, 'uses', 'mr', 'स्त्रीरोग आणि जखम भरण्यासाठी उपयुक्त'),
(72, 'contraindications', 'hi', 'दीर्घकालीन कब्ज में परहेज़ करें'),
(72, 'contraindications', 'mr', 'जुनी बद्धकोष्ठता असल्यास वापर टाळा');

-- 73. Manjishtha (Rubia cordifolia)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (73, 'Manjishtha', 'Rubia cordifolia', 'Ayurveda', 'Blood purifier, skin diseases, detoxification', 'Root', 'Rubiadin, Purpurin', 'Avoid during pregnancy');

INSERT INTO common_names (herb_id, name) VALUES
(73, 'Manjishtha'),
(73, 'मंजिष्ठा'),
(73, 'मंजिष्ठा');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(73, 'name', 'hi', 'मंजिष्ठा'),
(73, 'name', 'mr', 'मंजिष्ठा'),
(73, 'uses', 'hi', 'रक्त शुद्धिकरण, त्वचा रोग और डिटॉक्स के लिए उपयोगी'),
(73, 'uses', 'mr', 'रक्तशुद्धीकरण, त्वचारोग व डिटॉक्ससाठी उपयुक्त'),
(73, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(73, 'contraindications', 'mr', 'गर्भावस्थेत वापर टाळा');

-- 74. Vidanga (Embelia ribes)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (74, 'Vidanga', 'Embelia ribes', 'Ayurveda', 'Anthelmintic, digestive stimulant', 'Fruits', 'Embelin, Ribesin', 'Avoid in pregnancy and children below 5 years');

INSERT INTO common_names (herb_id, name) VALUES
(74, 'Vidanga'),
(74, 'विदंग'),
(74, 'विडंग');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(74, 'name', 'hi', 'विदंग'),
(74, 'name', 'mr', 'विडंग'),
(74, 'uses', 'hi', 'कृमिनाशक और पाचन सुधारक'),
(74, 'uses', 'mr', 'कृमिनाशक व पचन सुधारक'),
(74, 'contraindications', 'hi', 'गर्भवती और छोटे बच्चों में उपयोग न करें'),
(74, 'contraindications', 'mr', 'गर्भवती व ५ वर्षांखालील मुलांमध्ये वापर टाळा');

-- 75. Arjuna (Terminalia arjuna)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (75, 'Arjuna', 'Terminalia arjuna', 'Ayurveda', 'Cardioprotective, hypertension, cholesterol management', 'Bark', 'Arjunolic acid, Tannins', 'Avoid with anticoagulants');

INSERT INTO common_names (herb_id, name) VALUES
(75, 'Arjuna'),
(75, 'अर्जुन'),
(75, 'अर्जुन');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(75, 'name', 'hi', 'अर्जुन'),
(75, 'name', 'mr', 'अर्जुन'),
(75, 'uses', 'hi', 'हृदय स्वास्थ्य और रक्तचाप नियंत्रक'),
(75, 'uses', 'mr', 'हृदय आरोग्य व रक्तदाब नियंत्रक'),
(75, 'contraindications', 'hi', 'रक्त पतला करने वाली दवाओं के साथ उपयोग न करें'),
(75, 'contraindications', 'mr', 'रक्त पातळ करणाऱ्या औषधांसोबत वापर टाळा');

-- 76. Bhumi Amla (Phyllanthus niruri)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (76, 'Bhumi Amla', 'Phyllanthus niruri', 'Ayurveda', 'Liver tonic, jaundice, antiviral', 'Whole plant', 'Phyllanthin, Hypophyllanthin', 'Avoid in low blood pressure');

INSERT INTO common_names (herb_id, name) VALUES
(76, 'Bhumi Amla'),
(76, 'भू-आंवला'),
(76, 'भुईआवळा');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(76, 'name', 'hi', 'भू-आंवला'),
(76, 'name', 'mr', 'भुईआवळा'),
(76, 'uses', 'hi', 'यकृत टॉनिक, पीलिया और एंटीवायरल गुणकारी'),
(76, 'uses', 'mr', 'यकृत टॉनिक, पिवळ्या कावीळ व विषाणूरोधक गुणकारी'),
(76, 'contraindications', 'hi', 'निम्न रक्तचाप में उपयोग न करें'),
(76, 'contraindications', 'mr', 'कमी रक्तदाब असल्यास वापर टाळा');

-- 77. Agnimantha (Clerodendrum phlomidis)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (77, 'Agnimantha', 'Clerodendrum phlomidis', 'Ayurveda', 'Anti-inflammatory, fever, arthritis', 'Root, bark', 'Clerodin, Phlomisoside', 'Avoid in severe gastric irritation');

INSERT INTO common_names (herb_id, name) VALUES
(77, 'Agnimantha'),
(77, 'अग्निमंथ'),
(77, 'अग्निमंथ');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(77, 'name', 'hi', 'अग्निमंथ'),
(77, 'name', 'mr', 'अग्निमंथ'),
(77, 'uses', 'hi', 'सूजन, बुखार और गठिया में सहायक'),
(77, 'uses', 'mr', 'सूज, ताप व संधिवातात उपयुक्त'),
(77, 'contraindications', 'hi', 'तीव्र गैस्ट्रिक समस्या में उपयोग न करें'),
(77, 'contraindications', 'mr', 'गंभीर जठराच्या तक्रारीत वापर टाळा');

-- 78. Patha (Cissampelos pareira)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (78, 'Patha', 'Cissampelos pareira', 'Ayurveda', 'Diarrhea, dysentery, urinary tract infections', 'Root', 'Cissampeline, Pareirubrines', 'Avoid in pregnancy');

INSERT INTO common_names (herb_id, name) VALUES
(78, 'Patha'),
(78, 'पाठा'),
(78, 'पाठा');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(78, 'name', 'hi', 'पाठा'),
(78, 'name', 'mr', 'पाठा'),
(78, 'uses', 'hi', 'दस्त, पेचिश और मूत्र संक्रमण में लाभकारी'),
(78, 'uses', 'mr', 'जुलाब, पेचिश व मूत्रमार्गाच्या संक्रमणात उपयुक्त'),
(78, 'contraindications', 'hi', 'गर्भावस्था में उपयोग न करें'),
(78, 'contraindications', 'mr', 'गर्भावस्थेत वापर टाळा');

-- 79. Jivanti (Leptadenia reticulata)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (79, 'Jivanti', 'Leptadenia reticulata', 'Ayurveda', 'Rejuvenative, eye health, lactation support', 'Leaves, root', 'Reticulatin, Stigmasterol', 'Avoid in diabetes without monitoring');

INSERT INTO common_names (herb_id, name) VALUES
(79, 'Jivanti'),
(79, 'जीवन्ती'),
(79, 'जीवन्ती');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(79, 'name', 'hi', 'जीवन्ती'),
(79, 'name', 'mr', 'जीवन्ती'),
(79, 'uses', 'hi', 'पुनर्यौवन, नेत्र स्वास्थ्य और स्तनपान में सहायक'),
(79, 'uses', 'mr', 'पुनर्यौवन, डोळ्यांचे आरोग्य व स्तनपानासाठी उपयुक्त'),
(79, 'contraindications', 'hi', 'मधुमेह रोगियों में सावधानीपूर्वक प्रयोग करें'),
(79, 'contraindications', 'mr', 'मधुमेह असलेल्या रुग्णांमध्ये काळजीपूर्वक वापरावे');

-- 80. Yashtimadhu (Glycyrrhiza glabra)
INSERT INTO herbs (id, name, scientific_name, ayush_system, uses, parts_used, phytochemicals, contraindications)
VALUES (80, 'Yashtimadhu', 'Glycyrrhiza glabra', 'Ayurveda', 'Sore throat, gastritis, ulcers', 'Root', 'Glycyrrhizin, Liquiritin', 'Avoid in hypertension');

INSERT INTO common_names (herb_id, name) VALUES
(80, 'Yashtimadhu'),
(80, 'यष्टिमधु'),
(80, 'जेष्ठमध');

INSERT INTO herb_languages (herb_id, field, language_code, translation) VALUES
(80, 'name', 'hi', 'यष्टिमधु'),
(80, 'name', 'mr', 'जेष्ठमध'),
(80, 'uses', 'hi', 'गले की खराश, गैस्ट्राइटिस और अल्सर में लाभकारी'),
(80, 'uses', 'mr', 'घशातील खवखव, गॅस्ट्रिक समस्या व अल्सर मध्ये उपयुक्त'),
(80, 'contraindications', 'hi', 'उच्च रक्तचाप में परहेज़ करें'),
(80, 'contraindications', 'mr', 'उच्च रक्तदाब असल्यास वापर टाळा');

