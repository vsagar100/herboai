INSERT INTO plants (
    botanical_name, common_name_en, common_name_hi, common_name_mr, sanskrit_name,
    family, description, habitat,
    parts_used, rasa, virya, vipaka, guna, dosha_effect,
    prabhava, active_compounds, therapeutic_actions, classical_references,
    is_endangered, cultivation_status, image_hero, ayush_system
) VALUES
-----------------------------------------------------------------------------------
-- 1. Brahmi
('Bacopa monnieri', 'Brahmi', 'ब्राह्मी', 'ब्राह्मी', 'ब्राह्मी',
 'Plantaginaceae',
 'Classical Medhya Rasayana enhancing memory, concentration and calming the mind.',
 'Moist wetlands, pond edges and paddy fields.',
 '["whole plant","aerial parts"]',
 '["tikta","kashaya"]', 'sheeta', 'madhura',
 '["laghu","snigdha"]',
 '{"vata":"reduces","pitta":"reduces","kapha":"balances"}',
 'Improves intellect and stabilizes mental faculties.',
 '{"Bacosides A & B", "brahmine", "herpestine"}',
 '["nootropic","anxiolytic","antioxidant","neuroprotective"]',
 'Charaka Samhita — listed as Medhya Rasayana.',
 0, 'cultivated', 'Brahmi.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 2. Gotu Kola
('Centella asiatica', 'Gotu Kola', 'मंडूकपर्णी', 'मंडूकपर्णी', 'मण्डूकपर्णी',
 'Apiaceae',
 'Creeping Medhya herb used for cognition, wound healing and anxiety.',
 'Moist shady soils, paddy fields and wetlands.',
 '["leaf","whole plant"]',
 '["tikta","kashaya"]', 'sheeta', 'madhura',
 '["laghu","ruksha"]',
 '{"vata":"reduces","pitta":"reduces","kapha":"balances"}',
 'Enhances longevity, intellect and tissue repair.',
 '{"Asiaticoside", "madecassoside", "triterpenoids"}',
 '["nootropic","anxiolytic","wound_healing","microcirculatory"]',
 'Referenced as Medhya Rasayana across classical texts.',
 0, 'wild_and_cultivated', 'Gotu_Kola.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 3. Giloy
('Tinospora cordifolia', 'Giloy', 'गिलोय', 'गिलोय', 'अमृता',
 'Menispermaceae',
 'Prominent Rasayana for fever, immunity, sugar balance and liver protection.',
 'Deciduous forests; climbs on neem and other trees.',
 '["stem","leaf"]',
 '["tikta","kashaya"]', 'ushna', 'madhura',
 '["laghu","snigdha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Supports longevity and immunity, known as Amrita.',
 '{"Tinosporaside", "alkaloids", "polysaccharides"}',
 '["immunomodulator","antipyretic","hepatoprotective","antidiabetic"]',
 'One of the most referenced herbs for jwara and prameha.',
 0, 'cultivated', 'Giloy.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 4. Neem
('Azadirachta indica', 'Neem', 'नीम', 'नीम', 'निंब',
 'Meliaceae',
 'Broad-spectrum antimicrobial and skin purifying herb.',
 'Dry and semi-arid tropical regions; common avenue tree.',
 '["leaf","bark","seed","flower"]',
 '["tikta","kashaya"]', 'sheeta', 'katu',
 '["laghu","ruksha"]',
 '{"vata":"increases","pitta":"reduces","kapha":"reduces"}',
 'Powerful krimighna and kushtaghna properties.',
 '{"Azadirachtin", "nimbidin", "nimbin"}',
 '["antimicrobial","antiparasitic","antiinflammatory","dermatoprotective"]',
 'Used traditionally in krimi, kushtha, danta roga.',
 0, 'wild_and_planted', 'Neem.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 5. Arjuna
('Terminalia arjuna', 'Arjuna', 'अर्जुन', 'अर्जुन', 'अर्जुन',
 'Combretaceae',
 'Cardiotonic bark used for heart strengthening, BP regulation and lipid management.',
 'River banks and moist deciduous forests.',
 '["bark"]',
 '["kashaya","tikta"]', 'sheeta', 'katu',
 '["guru","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Strong affinity for cardiac muscle and circulation.',
 '{"Arjunolic acid", "flavonoids", "tannins"}',
 '["cardioprotective","antihypertensive","hypolipidemic","antioxidant"]',
 'Described in hridroga chikitsa across classical texts.',
 0, 'cultivated', 'Arjuna.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 6. Gokshura
('Tribulus terrestris', 'Gokshura', 'गोक्षुर', 'गोक्षुर', 'गोक्षुर',
 'Zygophyllaceae',
 'Mutrala herb used in urinary stones, kidney function support and male vitality.',
 'Dry sandy soils and wastelands.',
 '["fruit","whole plant"]',
 '["madhura","tikta"]', 'sheeta', 'madhura',
 '["guru","snigdha"]',
 '{"vata":"reduces","pitta":"balances","kapha":"increases"}',
 'Strengthens mutravaha & shukravaha srotas.',
 '{"Protodioscin", "saponins"}',
 '["diuretic","nephroprotective","androgen_support","antiurolithic"]',
 'Classically used in mutrakrichra and shukra dhatu enhancement.',
 0, 'wild', 'Gokshura.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 7. Punarnava
('Boerhavia diffusa', 'Punarnava', 'पुनर्नवा', 'पुनर्नवा', 'पुनर्नवा',
 'Nyctaginaceae',
 'Renal & hepatic supportive herb used in edema and shotha.',
 'Roadsides and cultivated field margins.',
 '["root","whole plant"]',
 '["kashaya","tikta","madhura"]', 'ushna', 'madhura',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Restores fluid balance and reduces inflammation.',
 '{"Punarnavine", "boeravinones"}',
 '["diuretic","antiinflammatory","hepatoprotective","nephroprotective"]',
 'Referenced for shotha and yakrit vikriti.',
 0, 'wild_and_cultivated', 'Punarnava.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 8. Shatavari
('Asparagus racemosus', 'Shatavari', 'शतावरी', 'शतावरी', 'शतावरी',
 'Asparagaceae',
 'Major female Rasayana used for fertility, hormonal balance and gastric ulcers.',
 'Dry forests; widely cultivated.',
 '["tuberous root"]',
 '["madhura","tikta"]', 'sheeta', 'madhura',
 '["guru","snigdha"]',
 '{"vata":"reduces","pitta":"reduces","kapha":"increases"}',
 'Strengthens reproductive tissues & improves lactation.',
 '{"Shatavarins", "saponins"}',
 '["galactagogue","adaptogenic","antiulcer","hormonal_support"]',
 'Used traditionally as stanyavardhaka and rasayana.',
 0, 'cultivated', 'Shatavari.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 9. Licorice
('Glycyrrhiza glabra', 'Licorice', 'मुलेठी', 'जेष्ठमध', 'यष्टिमधु',
 'Fabaceae',
 'Demulcent root used in sore throat, ulcers and respiratory comfort.',
 'Dry temperate regions; cultivated in North India.',
 '["root"]',
 '["madhura"]', 'sheeta', 'madhura',
 '["guru","snigdha"]',
 '{"vata":"reduces","pitta":"reduces","kapha":"increases"}',
 'Soothing prabhava on mucosa and respiratory tract.',
 '{"Glycyrrhizin", "liquiritin"}',
 '["expectorant","demulcent","antiulcer","adaptogenic_support"]',
 'Applied in kasa, amlapitta and as rasayana.',
 0, 'cultivated', 'Licorice.jpg', 'Ayurveda'
),

-----------------------------------------------------------------------------------
--10. Kalmegh
('Andrographis paniculata', 'Kalmegh', 'कालमेघ', 'कालमेघ', 'भूनिंब',
 'Acanthaceae',
 'Highly bitter liver-protective herb used in fevers and digestive disorders.',
 'Moist tropical wastelands and field edges.',
 '["leaf","whole plant"]',
 '["tikta"]', 'sheeta', 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Acts on liver & immune channels as Bhunimba.',
 '{"Andrographolide", "diterpenes"}',
 '["hepatoprotective","antipyretic","immunomodulator","digestive_stimulant"]',
 'Used in jwara and yakrit roga across traditional texts.',
 0, 'cultivated', 'Kalmegh.jpg', 'Ayurveda'
);

INSERT INTO plants (
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
) VALUES
-----------------------------------------------------------------------------------
-- 1. Bael
('Aegle marmelos',
 'Bael',
 'बेल',
 'बेल',
 'बिल्व',
 'Rutaceae',
 'Sacred tree whose unripe fruit is used in Ayurveda for diarrhea, IBS and weak digestion.',
 'Dry deciduous forests and homestead gardens across India.',
 '["fruit","leaf","root"]',
 '["kashaya","tikta","madhura"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"reduces","pitta":"balances","kapha":"reduces"}',
 'Strengthens digestive fire and arrests atisara without excessive constipation.',
 '{"Coumarins", "marmelosin", "tannins"}',
 '["antidiarrheal","digestive_tonic","carminative","antiinflammatory"]',
 'Described in atisara and grahani chikitsa in classical texts.',
 0,
 'cultivated',
 'Bael.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 2. Guggul
('Commiphora mukul',
 'Guggul',
 'गुग्गुल',
 'गुग्गुळ',
 'गुग्गुलु',
 'Burseraceae',
 'Oleogum resin used in many classical formulations for lipids, obesity and joint disorders.',
 'Arid and semi arid regions of Rajasthan and Gujarat.',
 '["oleo-gum-resin"]',
 '["tikta","katu"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"reduces","pitta":"increases","kapha":"reduces"}',
 'Scrapes excess meda dhatu and helps clear ama from srotas.',
 '{"Guggulsterones", "essential oils", "diterpenes"}',
 '["hypolipidemic","antiinflammatory","analgesic","thyroid_support"]',
 'Key ingredient in Yogaraja guggulu, Triphala guggulu and similar yogas.',
 1,
 'wild_and_cultivated',
 'Guggul.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 3. Bhumyamalaki
('Phyllanthus niruri',
 'Bhumyamalaki',
 'भू्यमालकी',
 'भूयामावळा',
 'भूधात्री',
 'Phyllanthaceae',
 'Small herb used for liver support, viral hepatitis and urinary stone management.',
 'Grows as a weed in moist open ground and cultivated fields.',
 '["whole plant"]',
 '["tikta","kashaya"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Shows special affinity for yakrit and mutravaha srotas.',
 '{"Lignans such as phyllanthin", "flavonoids", "tannins"}',
 '["hepatoprotective","antiviral_support","diuretic","antiurolithic"]',
 'Traditionally indicated in kamala and as a liver tonic.',
 0,
 'wild',
 'Bhumyamalaki.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 4. Kutki
('Picrorhiza kurroa',
 'Kutki',
 'कुटकि',
 'कुटकी',
 'कटुकी',
 'Plantaginaceae',
 'Highly bitter rhizome used for liver congestion, fevers and skin diseases.',
 'Subalpine Himalayas on moist rocky slopes.',
 '["rhizome"]',
 '["tikta","katu"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Acts as strong cholegogue and liver cleansing agent.',
 '{"Iridoid glycosides such as picroside I and II"}',
 '["hepatoprotective","choleretic","antipyretic","antiinflammatory"]',
 'Mentioned in context of yakrit vikriti in later nighantus.',
 1,
 'wild',
 'Kutki.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 5. Long Pepper
('Piper longum',
 'Long Pepper',
 'पिप्पली',
 'पिंपळी',
 'पिप्पली',
 'Piperaceae',
 'Heating spice used in Trikatu for deepana, pachana and respiratory support.',
 'Humid tropical forests and small plantations.',
 '["fruit"]',
 '["katu"]',
 'ushna',
 'madhura',
 '["laghu","snigdha"]',
 '{"vata":"reduces","pitta":"increases","kapha":"reduces"}',
 'Excellent deepaniya with strong bioavailability enhancing prabhava.',
 '{"Piperine", "volatile oils", "lignans"}',
 '["carminative","expectorant","bioavailability_enhancer","thermogenic"]',
 'One of the three components of Trikatu churna in many formulations.',
 0,
 'cultivated',
 'Long_Pepper.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 6. Black Pepper
('Piper nigrum',
 'Black Pepper',
 'काली मिर्च',
 'काळी मिरी',
 'मरिच',
 'Piperaceae',
 'Common kitchen spice used to kindle agni and clear kapha from respiratory tract.',
 'Climber grown on support trees in humid tropical regions.',
 '["fruit"]',
 '["katu"]',
 'ushna',
 'madhura',
 '["laghu","tikshna"]',
 '{"vata":"reduces","pitta":"increases","kapha":"reduces"}',
 'Penetrates srotas and helps in ama pachana.',
 '{"Piperine", "essential oils", "flavonoids"}',
 '["carminative","expectorant","digestive_stimulant","antioxidant"]',
 'Used with ginger and long pepper in Trikatu and many other yogas.',
 0,
 'cultivated',
 'Black_Pepper.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 7. Vidanga
('Embelia ribes',
 'Vidanga',
 'विदंग',
 'विदंग',
 'विदंग',
 'Primulaceae',
 'Classical krimighna fruit used against intestinal parasites and for digestive stimulation.',
 'Subtropical forests and hilly tracts of India.',
 '["fruit"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"reduces","pitta":"increases","kapha":"reduces"}',
 'Shows special prabhava against intestinal worms and ama.',
 '{"Embeline", "quercitol", "tannins"}',
 '["anthelmintic","carminative","digestive_stimulant","antimicrobial"]',
 'Described as chief krimighna dravya in several nighantus.',
 0,
 'wild',
 'Vidanga.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 8. Chitrak
('Plumbago zeylanica',
 'Chitrak',
 'चित्रक',
 'चित्रक',
 'चित्रक',
 'Plumbaginaceae',
 'Strong deepana pachana root used in low appetite, ama and obesity regimens.',
 'Coastal thickets and scrub forests in tropical regions.',
 '["root"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","tikshna"]',
 '{"vata":"reduces","pitta":"increases","kapha":"reduces"}',
 'Rapidly kindles digestive fire and digests ama.',
 '{"Plumbagin", "essential oils"}',
 '["digestive_stimulant","carminative","antiobesity_support","counterirritant"]',
 'Used in Chitrakadi vati and other deepana formulations.',
 0,
 'wild_and_cultivated',
 'Chitrak.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 9. Jatamansi
('Nardostachys jatamansi',
 'Jatamansi',
 'जटामांसी',
 'जटामांसी',
 'जटामांसी',
 'Caprifoliaceae',
 'Aromatic rhizome used for insomnia, anxiety, epilepsy and as medhya rasayana.',
 'High altitude Himalayan slopes and rocky soils.',
 '["rhizome"]',
 '["tikta","kashaya","madhura"]',
 'sheeta',
 'katu',
 '["laghu","snigdha"]',
 '{"vata":"reduces","pitta":"reduces","kapha":"balances"}',
 'Calming prabhava on manovaha srotas and prana vayu.',
 '{"Jatamansone", "sesquiterpenes", "volatile oils"}',
 '["sedative","anxiolytic","anticonvulsant_support","nootropic"]',
 'Mentioned for unmada, apasmara and nidra vikriti in classical literature.',
 1,
 'wild',
 'Jatamansi.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 10. Kustha
('Saussurea lappa',
 'Kustha',
 'कुष्ठ',
 'कुस्थ',
 'कुष्ठ',
 'Asteraceae',
 'Aromatic root used in respiratory conditions, skin diseases and pain disorders.',
 'Temperate Himalayan regions, now restricted in wild populations.',
 '["root"]',
 '["tikta","katu"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"reduces","pitta":"balances","kapha":"reduces"}',
 'Acts on pranavaha and rasavaha srotas with warming property.',
 '{"Costunolide", "dehydrocostus lactone", "volatile oils"}',
 '["expectorant","bronchodilator_support","analgesic","antiinflammatory"]',
 'Classically indicated in kasa, shwasa and kushtha.',
 1,
 'cultivated',
 'Kustha.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 11. Vasaka / Malabar Nut
('Adhatoda vasica',
 'Malabar Nut',
 'अडूसा',
 'आडुळसा',
 'वासा',
 'Acanthaceae',
 'Important shwasahara herb used in cough, bronchitis and asthma.',
 'Shrubs on roadsides and hedges in tropical India.',
 '["leaf","flower"]',
 '["tikta","kashaya"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Shows strong prabhava on pranavaha srotas and kapha in lungs.',
 '{"Vasicine", "vasicinone", "alkaloids"}',
 '["expectorant","bronchodilator_support","mucolytic","antitussive"]',
 'Recommended for kasa and shwasa in several Ayurvedic texts.',
 0,
 'wild_and_cultivated',
 'Malabar_Nut.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 12. Saptaparna
('Alstonia scholaris',
 'Saptaparna',
 'सप्तपर्ण',
 'सप्तपर्ण',
 'सप्तपर्णी',
 'Apocynaceae',
 'Bitter bark traditionally used in fevers, malaria like conditions and respiratory complaints.',
 'Evergreen forests and avenue plantations in tropical regions.',
 '["bark"]',
 '["tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Acts as bitter febrifuge with kapha pitta reducing action.',
 '{"Alkaloids such as echitamine", "triterpenes"}',
 '["antipyretic","antimalarial_support","expectorant","digestive_stimulant"]',
 'Mentioned in nighantus for jwara and shwasa.',
 0,
 'wild_and_planted',
 'Saptaparna.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 13. Mustaka / Nagarmotha
('Cyperus rotundus',
 'Mustaka',
 'नागरमोथा',
 'नागरमोथा',
 'मुस्तक',
 'Cyperaceae',
 'Rhizome used for diarrhea, fever and as aromatic digestive.',
 'Common grass like weed in fields and open lands.',
 '["rhizome"]',
 '["tikta","katu","kashaya"]',
 'sheeta',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Useful in amapachana and atisara with associated fever.',
 '{"Essential oils such as cyperene", "flavonoids", "sesquiterpenes"}',
 '["carminative","antidiarrheal","antipyretic","spasmolytic"]',
 'Found in formulations for atisara and jwara.',
 0,
 'wild',
 'Mustaka.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 14. Atibala
('Abutilon indicum',
 'Atibala',
 'अतिबला',
 'अतिबळा',
 'अतिबला',
 'Malvaceae',
 'Strength promoting herb used in neurological weakness, vata disorders and wound healing.',
 'Roadsides, waste places and field margins in tropical India.',
 '["root","leaf","seed"]',
 '["madhura"]',
 'sheeta',
 'madhura',
 '["guru","snigdha"]',
 '{"vata":"reduces","pitta":"reduces","kapha":"increases"}',
 'Promotes bala of nerves and muscles.',
 '{"Mucilage", "flavonoids", "sterols"}',
 '["nervine_tonic","antiinflammatory","demulcent","wound_healing"]',
 'Described in vata vyadhi and as balya herb in later texts.',
 0,
 'wild',
 'Atibala.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 15. Bala
('Sida cordifolia',
 'Bala',
 'बला',
 'बळा',
 'बला',
 'Malvaceae',
 'Balya and brimhaniya herb used in nervine weakness, post illness debility and vata disorders.',
 'Common weed in plains, roadsides and fields.',
 '["root","whole plant"]',
 '["madhura"]',
 'ushna',
 'madhura',
 '["guru","snigdha"]',
 '{"vata":"reduces","pitta":"balances","kapha":"increases"}',
 'Strengthens mamsa and asthi dhatu and calms vata.',
 '{"Alkaloids", "mucilage", "sterols"}',
 '["nervine_tonic","analgesic","antiinflammatory","adaptogenic_support"]',
 'Listed among balya and brimhaniya dravyas in classical literature.',
 0,
 'wild_and_cultivated',
 'Bala.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 16. Kantakari
('Solanum xanthocarpum',
 'Kantakari',
 'कंटकारी',
 'कंटकारी',
 'कण्टकारी',
 'Solanaceae',
 'Spiny herb used in asthma, cough and urinary disorders.',
 'Dry wastelands and field borders throughout India.',
 '["whole plant","fruit"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"balances","kapha":"reduces"}',
 'Prominent member of Dashamoola with effect on pranavaha srotas.',
 '{"Solasonine", "solasodine", "steroidal", "alkaloids"}',
 '["expectorant","bronchodilator_support","diuretic","antiinflammatory"]',
 'Part of Dashamoola group used in shwasa and kasa.',
 0,
 'wild',
 'Kantakari.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 17. Brihati
('Solanum indicum',
 'Brihati',
 'बृहती',
 'बृहती',
 'बृहती',
 'Solanaceae',
 'Shrub used in respiratory, urinary and abdominal disorders as part of Dashamoola.',
 'Fields, hedges and waste ground across India.',
 '["whole plant","root"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"balances","kapha":"reduces"}',
 'Acts on pranavaha, mutravaha and annavaha srotas.',
 '{"Steroidal alkaloids", "glycosides"}',
 '["expectorant","diuretic","carminative","antiinflammatory"]',
 'Included in Dashamoola formulations in respiratory and abdominal complaints.',
 0,
 'wild',
 'Brihati.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 18. Asthisamharaka
('Cissus quadrangularis',
 'Asthisamharaka',
 'हडजोड',
 'हाडजोड',
 'अस्थिसंहर',
 'Vitaceae',
 'Succulent stem used for fracture healing, osteoporosis and joint health.',
 'Rocky, dry regions and hedges in tropical India.',
 '["stem"]',
 '["katu","tikta"]',
 'ushna',
 'katu',
 '["laghu","snigdha"]',
 '{"vata":"reduces","pitta":"balances","kapha":"balances"}',
 'Shows special prabhava on asthi dhatu and fracture union.',
 '{"Triterpenoids", "carotenoids", "vitamin C", "calcium"}',
 '["osteoprotective","antiinflammatory","analgesic","bone_healing_support"]',
 'Traditionally indicated in asthibhanga and sandhivata.',
 0,
 'wild_and_cultivated',
 'Asthisamharaka.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 19. Vijayasar
('Pterocarpus marsupium',
 'Vijayasar',
 'विजयसार',
 'विजयसार',
 'विजयसार',
 'Fabaceae',
 'Heartwood used for diabetes, obesity and lipid disorders, often as diabetic tumbler.',
 'Moist deciduous forests of India and Sri Lanka.',
 '["heartwood"]',
 '["tikta","kashaya"]',
 'sheeta',
 'katu',
 '["guru","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Scrapes meda and helps in prameha related complications.',
 '{"Pterostilbene", "marsupsin", "tannins"}',
 '["antidiabetic_support","hypolipidemic","astringent","antioxidant"]',
 'Recommended in some nighantus for prameha and meda vikriti.',
 1,
 'wild',
 'Vijayasar.jpg',
 'Ayurveda'
),

-----------------------------------------------------------------------------------
-- 20. Manjishta
('Rubia cordifolia',
 'Manjishta',
 'मंजिष्ठा',
 'मंजिष्ठा',
 'मञ्जिष्ठा',
 'Rubiaceae',
 'Important blood purifier used in skin disorders, varicose veins and menstrual problems.',
 'Climber found in hilly regions and forest edges.',
 '["root"]',
 '["tikta","kashaya"]',
 'ushna',
 'katu',
 '["laghu","ruksha"]',
 '{"vata":"balances","pitta":"reduces","kapha":"reduces"}',
 'Acts strongly on raktavaha srotas and microcirculation.',
 '{"Anthraquinones such as munjistin", "rubiadin", "tannins"}',
 '["blood_purifier","depurative","antiinflammatory","venotonic_support"]',
 'Used in raktapitta, kushtha and varna prasadana formulations.',
 0,
 'wild_and_cultivated',
 'Manjishta.jpg',
 'Ayurveda'
);


INSERT INTO plant_synonyms (plant_id, synonym, language, kind)
SELECT p.id, s.synonym, s.language, s.kind
FROM plants p
JOIN (
    -- Brahmi
    SELECT 'Bacopa monnieri' AS botanical_name, 'Brahmi' AS synonym, 'en' AS language, 'common_name' AS kind
    UNION ALL SELECT 'Bacopa monnieri','जल ब्राह्मी','hi','regional_name'
    UNION ALL SELECT 'Bacopa monnieri','जल ब्राह्मी','mr','regional_name'
    UNION ALL SELECT 'Bacopa monnieri','Water Hyssop','en','common_name'

    -- Gotu Kola
    UNION ALL SELECT 'Centella asiatica','Mandukaparni','en','common_name'
    UNION ALL SELECT 'Centella asiatica','Gotu Kola','en','common_name'
    UNION ALL SELECT 'Centella asiatica','गोटू कोला','hi','regional_name'
    UNION ALL SELECT 'Centella asiatica','थल ब्राह्मी','mr','regional_name'

    -- Giloy
    UNION ALL SELECT 'Tinospora cordifolia','Guduchi','en','common_name'
    UNION ALL SELECT 'Tinospora cordifolia','Giloy','en','common_name'
    UNION ALL SELECT 'Tinospora cordifolia','गुडूची','hi','common_name'
    UNION ALL SELECT 'Tinospora cordifolia','गुळवेल','mr','common_name'

    -- Neem
    UNION ALL SELECT 'Azadirachta indica','Neem','en','common_name'
    UNION ALL SELECT 'Azadirachta indica','Margosa','en','common_name'
    UNION ALL SELECT 'Azadirachta indica','निंब','hi','common_name'
    UNION ALL SELECT 'Azadirachta indica','कडुलिंब','mr','common_name'

    -- Arjuna
    UNION ALL SELECT 'Terminalia arjuna','Arjun Tree','en','common_name'
    UNION ALL SELECT 'Terminalia arjuna','अर्जुन छाल','hi','common_name'
    UNION ALL SELECT 'Terminalia arjuna','अर्जुनाची साल','mr','common_name'

    -- Gokshura
    UNION ALL SELECT 'Tribulus terrestris','Land Caltrops','en','common_name'
    UNION ALL SELECT 'Tribulus terrestris','गोक्षुर','hi','common_name'
    UNION ALL SELECT 'Tribulus terrestris','गोखरू','mr','regional_name'

    -- Punarnava
    UNION ALL SELECT 'Boerhavia diffusa','Punarnava','en','common_name'
    UNION ALL SELECT 'Boerhavia diffusa','स्प्रेडिंग हॉगवीड','en','common_name'
    UNION ALL SELECT 'Boerhavia diffusa','पुनर्नवा','hi','common_name'
    UNION ALL SELECT 'Boerhavia diffusa','शोठपर्णी','mr','regional_name'

    -- Shatavari
    UNION ALL SELECT 'Asparagus racemosus','Shatavari','en','common_name'
    UNION ALL SELECT 'Asparagus racemosus','Wild Asparagus','en','common_name'
    UNION ALL SELECT 'Asparagus racemosus','शतावरी','hi','common_name'
    UNION ALL SELECT 'Asparagus racemosus','शतावरी','mr','common_name'

    -- Licorice
    UNION ALL SELECT 'Glycyrrhiza glabra','Yashtimadhu','en','common_name'
    UNION ALL SELECT 'Glycyrrhiza glabra','Licorice','en','common_name'
    UNION ALL SELECT 'Glycyrrhiza glabra','मुलेठी','hi','common_name'
    UNION ALL SELECT 'Glycyrrhiza glabra','जेष्ठमध','mr','common_name'

    -- Kalmegh
    UNION ALL SELECT 'Andrographis paniculata','Kalmegh','en','common_name'
    UNION ALL SELECT 'Andrographis paniculata','Bhunimba','en','common_name'
    UNION ALL SELECT 'Andrographis paniculata','कालमेघ','hi','common_name'
    UNION ALL SELECT 'Andrographis paniculata','किरात','mr','regional_name'
) AS s
ON p.botanical_name = s.botanical_name;

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
-- 1. Anxiety and Stress
('Anxiety and Stress',
 'चिंता व तनाव',
 'चिंता व ताण',
 'mental_health',
 'Chinta',
 NULL,
 NULL,
 'Persistent worry, restlessness and stress with disturbed sleep.',
 '["restlessness","racing thoughts","poor sleep","palpitations"]',
 '["chronic stress","work pressure","emotional trauma"]',
 '{"vata":"vitiated","pitta":"mildly_vitiated","kapha":"reduced"}',
 '{"mano_dhatu":"primary","majja_dhatu":"secondary"}',
 'moderate',
 1,
 '["adopt regular sleep schedule","practice relaxation and breathing","limit stimulants like caffeine"]',
 '{"favour":["warm light meals","ghee in moderation","herbal teas like brahmi or jatamansi"],"avoid":["excess coffee","refined sugar","heavy late-night meals"]}'
),

-- 2. Memory Weakness
('Memory Weakness',
 'स्मरण शक्ति दुर्बलता',
 'स्मरण कमी',
 'neurological',
 'Smriti bhramsha',
 NULL,
 NULL,
 'Reduced ability to recall recent events, difficulty concentrating and mental fatigue.',
 '["forgetfulness","low concentration","mental fatigue"]',
 '["chronic stress","sleep deprivation","aging"]',
 '{"vata":"vitiated","pitta":"balanced","kapha":"slightly_reduced"}',
 '{"majja_dhatu":"primary","rasa_dhatu":"secondary"}',
 'mild',
 1,
 '["ensure adequate sleep","mental exercises","regular meditation"]',
 '{"favour":["nuts and seeds in moderation","ghee and milk if tolerated","fresh fruits"],"avoid":["very dry foods","skipping meals","excess screen time at night"]}'
),

-- 3. Recurrent Fever
('Recurrent Fever',
 'बार-बार बुखार',
 'पुन्हा पुन्हा ताप',
 'infectious',
 'Punarbhu Jwara',
 NULL,
 NULL,
 'Episodes of raised body temperature occurring repeatedly over weeks or months.',
 '["repeated episodes of fever","chills","body ache","fatigue"]',
 '["recurrent infections","low immunity","incomplete recovery from prior illness"]',
 '{"vata":"vitiated","pitta":"vitiated","kapha":"mildly_vitiated"}',
 '{"rakta_dhatu":"primary","ras_dhatu":"secondary"}',
 'moderate',
 0,
 '["complete previous course of treatment","adequate post-illness rest","maintain hygiene and hydration"]',
 '{"favour":["light khichdi","warm herbal decoctions","adequate fluids"],"avoid":["very oily foods","cold drinks and ice cream","heavy fried meals during recovery"]}'
),

-- 4. Chronic Liver Disorder
('Chronic Liver Disorder',
 'दीर्घकालिक यकृत विकार',
 'दीर्घकालीन यकृत विकार',
 'hepatic',
 'Yakrit vikara',
 NULL,
 NULL,
 'Long-standing disturbance in liver function with fatigue, poor digestion and heaviness.',
 '["fatigue","loss of appetite","abdominal heaviness","mild jaundice in some cases"]',
 '["alcohol misuse","fatty diet","viral hepatitis","metabolic syndrome"]',
 '{"pitta":"vitiated","kapha":"vitiated","vata":"secondary"}',
 '{"rakta_dhatu":"primary","mamsa_dhatu":"secondary"}',
 'chronic',
 1,
 '["avoid alcohol","maintain healthy body weight","regular physical activity"]',
 '{"favour":["light easily digestible food","bitter green vegetables","adequate water"],"avoid":["alcohol","very oily and fried food","excessive refined sugar"]}'
),

-- 5. Chronic Skin Disease
('Chronic Skin Disease',
 'दीर्घकालिक त्वचा रोग',
 'जिद्दी त्वचा विकार',
 'dermatological',
 'Kushtha',
 NULL,
 NULL,
 'Long-standing skin disorder with itching, discoloration, scaling or thickening of skin.',
 '["itching","redness or discoloration","scaling","dry or thickened skin"]',
 '["immune imbalance","chronic inflammation","exposure to irritants"]',
 '{"pitta":"vitiated","kapha":"vitiated","vata":"secondary"}',
 '{"rakta_dhatu":"primary","mamsa_dhatu":"secondary"}',
 'chronic',
 0,
 '["avoid known triggers","maintain skin hygiene","reduce stress"]',
 '{"favour":["light non-spicy diet","bitter vegetables like neem leaves preparations","adequate hydration"],"avoid":["very spicy food","fermented food","alcohol"]}'
),

-- 6. Ischemic Heart Disease
('Ischemic Heart Disease',
 'हृदय में रक्तसंचार की कमी',
 'हृदयातील रक्तपुरवठा कमी',
 'cardiovascular',
 'Hridroga',
 NULL,
 NULL,
 'Reduced blood flow to heart muscle causing chest discomfort or breathlessness on exertion.',
 '["chest discomfort","breathlessness on exertion","easy fatigue"]',
 '["atherosclerosis","hypertension","diabetes","smoking","sedentary lifestyle"]',
 '{"vata":"vitiated","kapha":"vitiated","pitta":"secondary"}',
 '{"rakta_dhatu":"primary","mamsa_dhatu":"primary"}',
 'severe',
 1,
 '["stop smoking","control blood pressure and blood sugar","regular gentle exercise under medical guidance"]',
 '{"favour":["light low-fat diet","foods rich in natural antioxidants","controlled salt intake"],"avoid":["trans fats","smoking","very salty and fried food"]}'
),

-- 7. Urinary Stones
('Urinary Stones',
 'मूत्र पथरी',
 'मूत्र पथरी',
 'urinary',
 'Ashmari',
 NULL,
 NULL,
 'Stone formation in kidneys or urinary tract leading to colicky pain and burning urination.',
 '["flank pain","colicky abdominal pain","burning urination","blood in urine in some cases"]',
 '["low water intake","high salt intake","metabolic imbalance"]',
 '{"vata":"vitiated","pitta":"vitiated","kapha":"contributing"}',
 '{"mutra_vaha_srotas":"primary","rakta_dhatu":"secondary"}',
 'moderate',
 1,
 '["increase daily water intake","avoid holding urine","regular physical activity"]',
 '{"favour":["adequate plain water","citrate containing fruits in moderation","light food"],"avoid":["very salty food","excess animal protein","dehydration"]}'
),

-- 8. Menstrual Irregularity
('Menstrual Irregularity',
 'मासिक धर्म अनियमितता',
 'मासिक पाळी अनियमित',
 'gynecological',
 'Artava vyapad',
 NULL,
 NULL,
 'Irregular menstrual cycles with variable flow, cramps or premenstrual discomfort.',
 '["irregular cycle length","variable flow","cramps","premenstrual discomfort"]',
 '["hormonal imbalance","stress","sudden weight gain or loss"]',
 '{"vata":"vitiated","pitta":"vitiated","kapha":"variable"}',
 '{"rakta_dhatu":"primary","artava_dhatu":"primary"}',
 'moderate',
 1,
 '["maintain regular sleep and food timings","manage stress","moderate exercise"]',
 '{"favour":["warm light meals","iron-rich foods if needed","adequate hydration"],"avoid":["skipping meals","excess caffeine","very cold foods around menses"]}'
),

-- 9. Gastric Ulcer / Hyperacidity
('Gastric Ulcer and Hyperacidity',
 'अम्लपित्त व अल्सर',
 'अम्लपित्त व अल्सर',
 'digestive',
 'Amlapitta',
 NULL,
 NULL,
 'Burning in epigastric region, sour belching and discomfort related to meals.',
 '["burning in upper abdomen","sour belching","nausea","discomfort after meals"]',
 '["irregular meals","spicy fried food","stress"]',
 '{"pitta":"vitiated","vata":"secondary","kapha":"reduced"}',
 '{"ras_dhatu":"primary","mamsa_dhatu":"secondary"}',
 'moderate',
 1,
 '["avoid long fasting","eat on regular timings","manage stress"]',
 '{"favour":["soft easy to digest food","lukewarm water","mildly spiced food"],"avoid":["very spicy and fried items","excess tea coffee","late-night heavy meals"]}'
);

INSERT INTO plant_disease_mapping (
    plant_id,
    disease_id,
    efficacy_level,
    evidence_type,
    mechanism,
    duration_of_use,
    contraindications,
    special_instructions,
    reference_text
)
-- Brahmi → Anxiety and Stress
SELECT p.id, d.id,
       4,
       'traditional',
       'Calms mind, supports medhya rasayana and improves stress resilience.',
       '4-12 weeks with periodic reassessment.',
       'Use cautiously with strong sedatives; monitor in hypotensive patients.',
       'Start with low dose in the evening and monitor sleep quality.',
       'Classical medhya rasayana use of Brahmi described in Charaka and later texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Bacopa monnieri'
 AND d.name_en = 'Anxiety and Stress'

UNION ALL
-- Gotu Kola → Anxiety and Stress
SELECT p.id, d.id,
       3,
       'traditional',
       'Mild anxiolytic and adaptogenic effect with improved microcirculation.',
       '4-8 weeks.',
       'Avoid very high doses in pregnancy without supervision.',
       'Combine with lifestyle stress management for best effect.',
       'Use of Mandukaparni for manas roga is noted in classical nighantus.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Centella asiatica'
 AND d.name_en = 'Anxiety and Stress'

UNION ALL
-- Brahmi → Memory Weakness
SELECT p.id, d.id,
       4,
       'traditional',
       'Enhances cognition, attention and recall as medhya rasayana.',
       '12 weeks or more, with long term maintenance doses as needed.',
       'Use cautiously with existing antiepileptic medication; monitor clinically.',
       'Monitor cognitive scores or subjective memory improvement periodically.',
       'Brahmi is repeatedly cited as medhya herb for smriti-bruddhi.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Bacopa monnieri'
 AND d.name_en = 'Memory Weakness'

UNION ALL
-- Gotu Kola → Memory Weakness
SELECT p.id, d.id,
       3,
       'traditional',
       'Supports circulation to brain and neurotrophic processes.',
       '8-12 weeks.',
       'Avoid overdose in patients on multiple sedative drugs.',
       'Better used in divided doses through the day.',
       'Mandukaparni is described among medhya dravyas for smriti and buddhi.'

FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Centella asiatica'
 AND d.name_en = 'Memory Weakness'

UNION ALL
-- Giloy → Recurrent Fever
SELECT p.id, d.id,
       4,
       'traditional',
       'Immunomodulatory and antipyretic action helps reduce frequency of febrile episodes.',
       '2-6 weeks during and after acute episodes.',
       'Caution in autoimmune conditions where immunomodulation must be supervised.',
       'Combine with adequate hydration and rest; do not replace necessary acute care.',
       'Guduchi is a prime herb in jwara chikitsa across classical texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Tinospora cordifolia'
 AND d.name_en = 'Recurrent Fever'

UNION ALL
-- Kalmegh → Recurrent Fever
SELECT p.id, d.id,
       3,
       'traditional',
       'Bitter antipyretic acting on liver and immune system.',
       'Short courses of 1-3 weeks during active episodes.',
       'Avoid in very frail patients without supervision due to strong tikta rasa.',
       'Preferably used in combination with supporting herbs.',
       'Andrographis (Bhunimba) is used for jwara and yakrit roga in traditional texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Andrographis paniculata'
 AND d.name_en = 'Recurrent Fever'

UNION ALL
-- Giloy → Chronic Liver Disorder
SELECT p.id, d.id,
       3,
       'traditional',
       'Supports liver function and reduces inflammatory load.',
       '6-12 weeks with monitoring of liver parameters where appropriate.',
       'Use with caution alongside hepatotoxic drugs; requires medical oversight.',
       'Monitor liver function tests where available.',
       'Guduchi is described as yakrit-uttejaka and rakta-prasadaka in many formulations.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Tinospora cordifolia'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- Punarnava → Chronic Liver Disorder
SELECT p.id, d.id,
       4,
       'traditional',
       'Decongests liver and reduces edema related to hepatic dysfunction.',
       '4-12 weeks depending on response.',
       'Avoid in severe renal failure unless supervised.',
       'Monitor weight, edema status and basic liver profile if feasible.',
       'Punarnava is widely used in shotha and yakrit vikriti management.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Boerhavia diffusa'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- Neem → Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Antimicrobial, blood purifying and antiinflammatory effects on skin.',
       'Variable; often several weeks to months in chronic conditions.',
       'High internal doses may worsen vata or cause GI upset; avoid in pregnancy in strong doses.',
       'Support with external applications and suitable diet.',
       'Neem is a classical kushtaghna and krimighna herb for chronic skin disorders.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Azadirachta indica'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- Arjuna → Ischemic Heart Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Cardioprotective and tonic to heart muscle; may improve exercise tolerance.',
       'Long term, often several months along with conventional care.',
       'Not a substitute for emergency care; caution with multiple cardiac drugs.',
       'Use as adjuvant under supervision; monitor BP, heart rate and symptoms.',
       'Arjuna ksheerapaka and related preparations are described in hridroga management.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Terminalia arjuna'
 AND d.name_en = 'Ischemic Heart Disease'

UNION ALL
-- Gokshura → Urinary Stones
SELECT p.id, d.id,
       3,
       'traditional',
       'Diuretic and soothing to urinary tract; supports clearance of small calculi.',
       '4-8 weeks along with high fluid intake.',
       'Use cautiously in advanced renal failure.',
       'Ensure adequate hydration and monitoring of pain or obstruction signs.',
       'Gokshura is a traditional mutrala and ashmari-nashaka ingredient.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Tribulus terrestris'
 AND d.name_en = 'Urinary Stones'

UNION ALL
-- Shatavari → Menstrual Irregularity
SELECT p.id, d.id,
       4,
       'traditional',
       'Supports female hormonal balance and nourishes artava dhatu.',
       'At least 3-6 cycles to judge response.',
       'Caution in estrogen-sensitive conditions; requires clinician judgement.',
       'Use with dietary and lifestyle balancing; track cycle pattern.',
       'Shatavari is described as stanyajanana and artava poshaka in classical texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Asparagus racemosus'
 AND d.name_en = 'Menstrual Irregularity'

UNION ALL
-- Licorice → Gastric Ulcer / Hyperacidity
SELECT p.id, d.id,
       4,
       'traditional',
       'Forms protective mucosal coating and reduces pitta in stomach.',
       '2-8 weeks with tapering as symptoms settle.',
       'Avoid in uncontrolled hypertension and fluid retention due to glycyrrhizin.',
       'Monitor blood pressure and edema in long-term use.',
       'Yashtimadhu is a key dravya in amlapitta and uras roga formulations.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Glycyrrhiza glabra'
 AND d.name_en = 'Gastric Ulcer and Hyperacidity'
;

INSERT INTO plant_synonyms (plant_id, synonym, language, kind)
SELECT p.id, s.synonym, s.language, s.kind
FROM plants p
JOIN (
    --------------------------------------------------------------------
    -- Bael - Aegle marmelos
    --------------------------------------------------------------------
    SELECT 'Aegle marmelos' AS botanical_name, 'Bael' AS synonym, 'en' AS language, 'common_name' AS kind
    UNION ALL SELECT 'Aegle marmelos','Bilva','en','classical_name'
    UNION ALL SELECT 'Aegle marmelos','बेल','hi','common_name'
    UNION ALL SELECT 'Aegle marmelos','बेल','mr','common_name'

    --------------------------------------------------------------------
    -- Guggul - Commiphora mukul
    --------------------------------------------------------------------
    UNION ALL SELECT 'Commiphora mukul','Guggul','en','common_name'
    UNION ALL SELECT 'Commiphora mukul','Indian Bdellium','en','common_name'
    UNION ALL SELECT 'Commiphora mukul','गुग्गुल','hi','common_name'
    UNION ALL SELECT 'Commiphora mukul','गुग्गुळ','mr','common_name'

    --------------------------------------------------------------------
    -- Bhumyamalaki - Phyllanthus niruri
    --------------------------------------------------------------------
    UNION ALL SELECT 'Phyllanthus niruri','Bhumyamalaki','en','common_name'
    UNION ALL SELECT 'Phyllanthus niruri','Stonebreaker','en','common_name'
    UNION ALL SELECT 'Phyllanthus niruri','भू्यमालकी','hi','common_name'
    UNION ALL SELECT 'Phyllanthus niruri','भुईआवळा','mr','common_name'

    --------------------------------------------------------------------
    -- Kutki - Picrorhiza kurroa
    --------------------------------------------------------------------
    UNION ALL SELECT 'Picrorhiza kurroa','Kutki','en','common_name'
    UNION ALL SELECT 'Picrorhiza kurroa','Katuki','en','common_name'
    UNION ALL SELECT 'Picrorhiza kurroa','कुटकी','hi','common_name'
    UNION ALL SELECT 'Picrorhiza kurroa','कुटकी','mr','common_name'

    --------------------------------------------------------------------
    -- Long Pepper - Piper longum
    --------------------------------------------------------------------
    UNION ALL SELECT 'Piper longum','Long Pepper','en','common_name'
    UNION ALL SELECT 'Piper longum','Pippali','en','classical_name'
    UNION ALL SELECT 'Piper longum','पीपली','hi','common_name'
    UNION ALL SELECT 'Piper longum','पिंपळी','mr','common_name'

    --------------------------------------------------------------------
    -- Black Pepper - Piper nigrum
    --------------------------------------------------------------------
    UNION ALL SELECT 'Piper nigrum','Black Pepper','en','common_name'
    UNION ALL SELECT 'Piper nigrum','Kala Mirch','en','common_name'
    UNION ALL SELECT 'Piper nigrum','काली मिर्च','hi','common_name'
    UNION ALL SELECT 'Piper nigrum','काळी मिरी','mr','common_name'

    --------------------------------------------------------------------
    -- Vidanga - Embelia ribes
    --------------------------------------------------------------------
    UNION ALL SELECT 'Embelia ribes','Vidanga','en','common_name'
    UNION ALL SELECT 'Embelia ribes','False Black Pepper','en','common_name'
    UNION ALL SELECT 'Embelia ribes','विदंग','hi','common_name'
    UNION ALL SELECT 'Embelia ribes','विदंग','mr','common_name'

    --------------------------------------------------------------------
    -- Chitrak - Plumbago zeylanica
    --------------------------------------------------------------------
    UNION ALL SELECT 'Plumbago zeylanica','Chitrak','en','common_name'
    UNION ALL SELECT 'Plumbago zeylanica','Ceylon Leadwort','en','common_name'
    UNION ALL SELECT 'Plumbago zeylanica','चित्रक','hi','common_name'
    UNION ALL SELECT 'Plumbago zeylanica','चितरक','mr','regional_name'

    --------------------------------------------------------------------
    -- Jatamansi - Nardostachys jatamansi
    --------------------------------------------------------------------
    UNION ALL SELECT 'Nardostachys jatamansi','Jatamansi','en','common_name'
    UNION ALL SELECT 'Nardostachys jatamansi','Indian Spikenard','en','common_name'
    UNION ALL SELECT 'Nardostachys jatamansi','जटामांसी','hi','common_name'
    UNION ALL SELECT 'Nardostachys jatamansi','जटामांसी','mr','common_name'

    --------------------------------------------------------------------
    -- Kustha - Saussurea lappa
    --------------------------------------------------------------------
    UNION ALL SELECT 'Saussurea lappa','Kustha','en','common_name'
    UNION ALL SELECT 'Saussurea lappa','Costus Root','en','common_name'
    UNION ALL SELECT 'Saussurea lappa','कुष्ठ','hi','common_name'
    UNION ALL SELECT 'Saussurea lappa','कुथ','mr','regional_name'

    --------------------------------------------------------------------
    -- Malabar Nut - Adhatoda vasica
    --------------------------------------------------------------------
    UNION ALL SELECT 'Adhatoda vasica','Malabar Nut','en','common_name'
    UNION ALL SELECT 'Adhatoda vasica','Vasaka','en','common_name'
    UNION ALL SELECT 'Adhatoda vasica','अडूसा','hi','common_name'
    UNION ALL SELECT 'Adhatoda vasica','आडुळसा','mr','common_name'

    --------------------------------------------------------------------
    -- Saptaparna - Alstonia scholaris
    --------------------------------------------------------------------
    UNION ALL SELECT 'Alstonia scholaris','Saptaparna','en','common_name'
    UNION ALL SELECT 'Alstonia scholaris','Devil Tree','en','common_name'
    UNION ALL SELECT 'Alstonia scholaris','सप्तपर्ण','hi','common_name'
    UNION ALL SELECT 'Alstonia scholaris','सप्तपर्ण','mr','common_name'

    --------------------------------------------------------------------
    -- Mustaka / Nagarmotha - Cyperus rotundus
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cyperus rotundus','Mustaka','en','common_name'
    UNION ALL SELECT 'Cyperus rotundus','Nagarmotha','en','common_name'
    UNION ALL SELECT 'Cyperus rotundus','नागरमोथा','hi','common_name'
    UNION ALL SELECT 'Cyperus rotundus','नागरमोथा','mr','common_name'

    --------------------------------------------------------------------
    -- Atibala - Abutilon indicum
    --------------------------------------------------------------------
    UNION ALL SELECT 'Abutilon indicum','Atibala','en','common_name'
    UNION ALL SELECT 'Abutilon indicum','Indian Mallow','en','common_name'
    UNION ALL SELECT 'Abutilon indicum','अतिबला','hi','common_name'
    UNION ALL SELECT 'Abutilon indicum','अतिबळा','mr','common_name'

    --------------------------------------------------------------------
    -- Bala - Sida cordifolia
    --------------------------------------------------------------------
    UNION ALL SELECT 'Sida cordifolia','Bala','en','common_name'
    UNION ALL SELECT 'Sida cordifolia','Country Mallow','en','common_name'
    UNION ALL SELECT 'Sida cordifolia','बला','hi','common_name'
    UNION ALL SELECT 'Sida cordifolia','बळा','mr','common_name'

    --------------------------------------------------------------------
    -- Kantakari - Solanum xanthocarpum
    --------------------------------------------------------------------
    UNION ALL SELECT 'Solanum xanthocarpum','Kantakari','en','common_name'
    UNION ALL SELECT 'Solanum xanthocarpum','Yellow-berried Nightshade','en','common_name'
    UNION ALL SELECT 'Solanum xanthocarpum','कंटकारी','hi','common_name'
    UNION ALL SELECT 'Solanum xanthocarpum','कंटकारी','mr','common_name'

    --------------------------------------------------------------------
    -- Brihati - Solanum indicum
    --------------------------------------------------------------------
    UNION ALL SELECT 'Solanum indicum','Brihati','en','common_name'
    UNION ALL SELECT 'Solanum indicum','Indian Nightshade','en','common_name'
    UNION ALL SELECT 'Solanum indicum','बृहती','hi','common_name'
    UNION ALL SELECT 'Solanum indicum','बृहती','mr','common_name'

    --------------------------------------------------------------------
    -- Asthisamharaka - Cissus quadrangularis
    --------------------------------------------------------------------
    UNION ALL SELECT 'Cissus quadrangularis','Asthisamharaka','en','common_name'
    UNION ALL SELECT 'Cissus quadrangularis','Hadjod','en','common_name'
    UNION ALL SELECT 'Cissus quadrangularis','हडजोड','hi','common_name'
    UNION ALL SELECT 'Cissus quadrangularis','हाडजोड','mr','common_name'

    --------------------------------------------------------------------
    -- Vijayasar - Pterocarpus marsupium
    --------------------------------------------------------------------
    UNION ALL SELECT 'Pterocarpus marsupium','Vijayasar','en','common_name'
    UNION ALL SELECT 'Pterocarpus marsupium','Indian Kino','en','common_name'
    UNION ALL SELECT 'Pterocarpus marsupium','विजयसार','hi','common_name'
    UNION ALL SELECT 'Pterocarpus marsupium','विजयसार','mr','common_name'

    --------------------------------------------------------------------
    -- Manjishta - Rubia cordifolia
    --------------------------------------------------------------------
    UNION ALL SELECT 'Rubia cordifolia','Manjishta','en','common_name'
    UNION ALL SELECT 'Rubia cordifolia','Indian Madder','en','common_name'
    UNION ALL SELECT 'Rubia cordifolia','मंजिष्ठा','hi','common_name'
    UNION ALL SELECT 'Rubia cordifolia','मंजिष्ठा','mr','common_name'
) AS s
  ON p.botanical_name = s.botanical_name;

INSERT INTO plant_disease_mapping (
    plant_id,
    disease_id,
    efficacy_level,
    evidence_type,
    mechanism,
    duration_of_use,
    contraindications,
    special_instructions,
    reference_text
)
-- Bael → Gastric Ulcer / Hyperacidity
SELECT p.id, d.id,
       4,
       'traditional',
       'Astringent unripe fruit protects gut mucosa and normalizes loose stools and excess acid.',
       '2-6 weeks with review based on symptoms.',
       'Avoid use of very unripe fruit in severe constipation.',
       'Prefer lightly cooked or decoction form in sensitive digestion.',
       'Bilva phala is classical dravya for atisara and grahani in Ayurvedic texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Aegle marmelos'
 AND d.name_en = 'Gastric Ulcer and Hyperacidity'

UNION ALL
-- Guggul → Ischemic Heart Disease
SELECT p.id, d.id,
       3,
       'traditional',
       'Improves lipid profile and reduces inflammation contributing to atherosclerosis.',
       '8-12 weeks, often as part of guggulu yogas.',
       'Use cautiously in hyperthyroidism and with multiple cardiac drugs.',
       'Always as an adjuvant; not a substitute for emergency cardiac care.',
       'Guggulu preparations are widely used in medoroga and related hridroga contexts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Commiphora mukul'
 AND d.name_en = 'Ischemic Heart Disease'

UNION ALL
-- Bhumyamalaki → Chronic Liver Disorder
SELECT p.id, d.id,
       4,
       'traditional',
       'Supports hepatocyte function and may reduce enzyme elevations in chronic liver stress.',
       '6-12 weeks with periodic monitoring.',
       'Use with caution in severe decompensated liver disease under medical supervision.',
       'Combine with dietary modification and avoidance of hepatotoxic substances.',
       'Bhumyamalaki is a key herb in kamala and yakrit vikara management in classical practice.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Phyllanthus niruri'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- Kutki → Chronic Liver Disorder
SELECT p.id, d.id,
       4,
       'traditional',
       'Bitter cholegogue improving bile flow and clearing hepatic congestion.',
       '4-8 weeks with gradual adjustment.',
       'Strong tikta and sheeta; avoid in severe debility without supervision.',
       'Best used in small divided doses with suitable anupana.',
       'Katuki is described as tikta dravya of choice in yakrit vikriti.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Picrorhiza kurroa'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- Long Pepper → Gastric Ulcer / Hyperacidity (for low-agni, non-erosive states)
SELECT p.id, d.id,
       3,
       'traditional',
       'Deepana and pachana actions help in functional dyspepsia and ama-related acidity when used judiciously.',
       '2-4 weeks in small doses along with appropriate diet.',
       'Avoid in frank erosive ulcer or severe pitta prakopa.',
       'Administer with ghee or milk in pitta-predominant patients if used.',
       'Pippali is central in Trikatu and many deepana formulations described for agnimandya and amlapitta.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Piper longum'
 AND d.name_en = 'Gastric Ulcer and Hyperacidity'

UNION ALL
-- Black Pepper → Gastric Ulcer / Hyperacidity (careful use)
SELECT p.id, d.id,
       2,
       'traditional',
       'Stimulates digestion and ama pachana; role more in low-agni dyspepsia than frank ulcer.',
       'Short courses of 2-3 weeks in small amounts.',
       'Avoid in active erosive ulcer, severe burning and in very pitta-dominant patients.',
       'Use only as minor component of formulations, not as high-dose single herb.',
       'Maricha is used in Trikatu for deepana but is restricted in strong pitta conditions.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Piper nigrum'
 AND d.name_en = 'Gastric Ulcer and Hyperacidity'

UNION ALL
-- Jatamansi → Anxiety and Stress
SELECT p.id, d.id,
       4,
       'traditional',
       'Sedative and anxiolytic effect through manovaha srotas modulation and prana vayu pacification.',
       '4-8 weeks, usually in bedtime doses.',
       'Caution with concurrent strong sedatives; may potentiate drowsiness.',
       'Begin at low bedtime dose and titrate; monitor daytime drowsiness.',
       'Jatamansi is described for unmada, apasmara and nidra-vikriti in classical texts.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Nardostachys jatamansi'
 AND d.name_en = 'Anxiety and Stress'

UNION ALL
-- Jatamansi → Memory Weakness
SELECT p.id, d.id,
       3,
       'traditional',
       'Improves quality of sleep and calms mind, indirectly supporting cognitive performance.',
       '6-8 weeks.',
       'Same caution as above regarding sedatives and hypotension.',
       'Combine with medhya herbs such as Brahmi when appropriate.',
       'Used in manas rog and medhya formulas as supportive herb.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Nardostachys jatamansi'
 AND d.name_en = 'Memory Weakness'

UNION ALL
-- Kustha → Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Acts on skin and blood with antiinflammatory and krimighna effects.',
       '6-12 weeks, often as part of compound formulations.',
       'Check sustainability of supply because of conservation concerns.',
       'Prefer cultivated sources and judicious dosing under supervision.',
       'Kustha is a classical kushthaghna root used in various skin conditions.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Saussurea lappa'
 AND d.name_en = 'Chronic Skin Disease'

UNION ALL
-- Malabar Nut → Recurrent Fever (respiratory-focused)
SELECT p.id, d.id,
       3,
       'traditional',
       'Reduces kapha in lungs and supports recovery during respiratory infections with recurrent fever.',
       '1-4 weeks during acute or subacute phase.',
       'Use cautiously in very low BP or severe weakness.',
       'Combine with rest and fluid intake; continue any essential allopathic therapy.',
       'Vasaka is repeatedly indicated in kasa and shwasa with associated jwara.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Adhatoda vasica'
 AND d.name_en = 'Recurrent Fever'

UNION ALL
-- Saptaparna → Recurrent Fever
SELECT p.id, d.id,
       3,
       'traditional',
       'Bitter bark used as febrifuge in malaria-like and recurrent fevers.',
       'Short courses of 1-3 weeks as part of combination therapy.',
       'Avoid unsupervised high doses due to alkaloid content.',
       'Should be combined with clinical monitoring in suspected malaria or complicated fever.',
       'Saptaparna is mentioned for jwara and visama jwara in traditional sources.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Alstonia scholaris'
 AND d.name_en = 'Recurrent Fever'

UNION ALL
-- Mustaka → Gastric Ulcer / Hyperacidity
SELECT p.id, d.id,
       3,
       'traditional',
       'Reduces diarrhea and abdominal discomfort associated with infections and acidity.',
       '2-4 weeks depending on response.',
       'Avoid in marked constipation or very dry prakriti without adjustment.',
       'Useful when atisara and jwara coexist with pitta symptoms.',
       'Mustaka is described in atisara and jwara formulations.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Cyperus rotundus'
 AND d.name_en = 'Gastric Ulcer and Hyperacidity'

UNION ALL
-- Atibala → Anxiety and Stress (nervine weakness)
SELECT p.id, d.id,
       2,
       'traditional',
       'Nourishing nervine tonic that can reduce vata-related weakness and irritability.',
       '4-8 weeks alongside broader lifestyle work.',
       'Use cautiously in marked kapha or obesity due to guru and snigdha properties.',
       'Best combined with movement, physiotherapy or yoga.',
       'Atibala is listed as balya and helpful in vata vyadhi.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Abutilon indicum'
 AND d.name_en = 'Anxiety and Stress'

UNION ALL
-- Bala → Anxiety and Stress (vata vyadhi)
SELECT p.id, d.id,
       3,
       'traditional',
       'Strengthens neuromuscular system and calms vata, indirectly reducing stress symptoms.',
       '4-12 weeks depending on chronicity.',
       'Use with care in kapha-dominant, very sedentary patients.',
       'Often combined with abhyanga and vatashamaka regimen.',
       'Bala is a classical balya and brimhaniya herb for vata disorders.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Sida cordifolia'
 AND d.name_en = 'Anxiety and Stress'

UNION ALL
-- Vijayasar → Chronic Liver Disorder (metabolic-related)
SELECT p.id, d.id,
       3,
       'traditional',
       'Improves metabolic parameters and may indirectly support fatty liver and related issues.',
       '8-12 weeks with metabolic monitoring.',
       'Avoid unsupervised use in advanced liver failure.',
       'Monitor body weight and basic biochemical parameters if possible.',
       'Vijayasar is traditionally used in prameha and medoroga, often with hepatic benefit.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Pterocarpus marsupium'
 AND d.name_en = 'Chronic Liver Disorder'

UNION ALL
-- Manjishta → Chronic Skin Disease
SELECT p.id, d.id,
       4,
       'traditional',
       'Blood purifier improving microcirculation and reducing inflammation in chronic skin disorders.',
       '8-16 weeks depending on severity.',
       'Use cautiously in patients on anticoagulants; may influence coagulation.',
       'Support with appropriate diet and skin hygiene.',
       'Manjishta is a key raktashodhaka herb used in kushtha and raktapitta conditions.'
FROM plants p
JOIN diseases d
  ON p.botanical_name = 'Rubia cordifolia'
 AND d.name_en = 'Chronic Skin Disease'
;

INSERT INTO diseases (
    name_en, name_hi, name_mr, category,
    ayurvedic_name, unani_name, siddha_name,
    description, symptoms, causes, dosha_involvement, dhatu_involvement,
    severity_level, is_lifestyle_related, prevention_tips, dietary_recommendations
) VALUES
-----------------------------------------------------------------------------------
-- 1. Intestinal Worm Infestation
('Intestinal Worm Infestation',
 'आंतों में कृमि संक्रमण',
 'आतड्यात कृमी',
 'parasitic',
 'Krimi Roga',
 NULL,
 NULL,
 'Presence of parasitic worms in the intestine causing digestive disturbances.',
 '["abdominal pain","itching around anus","disturbed appetite","weakness"]',
 '["poor hygiene","contaminated food","weak digestion"]',
 '{"pitta":"raised","kapha":"raised","vata":"disturbed"}',
 '{"rasa_dhatu":"affected"}',
 'moderate',
 0,
 '["maintain hygiene","wash vegetables properly","boil water"]',
 '{"favour":["light warm food","herbal decoctions"],"avoid":["sweets","raw uncooked food"]}'
),

-----------------------------------------------------------------------------------
-- 2. Bronchial Asthma
('Bronchial Asthma',
 'दमा रोग',
 'दमा',
 'respiratory',
 'Tamaka Shwasa',
 NULL,
 NULL,
 'Chronic inflammatory airway condition causing breathlessness and wheezing.',
 '["wheezing","shortness of breath","cough","tight chest"]',
 '["allergens","cold exposure","exercise","pollution"]',
 '{"vata":"disturbed","kapha":"excess","pitta":"variable"}',
 '{"pranavaha_srotas":"affected"}',
 'chronic',
 0,
 '["avoid cold exposure","practice breathing exercises"]',
 '{"favour":["warm soups","herbal steam inhalation"],"avoid":["cold drinks","dusty environments"]}'
),

-----------------------------------------------------------------------------------
-- 3. Chronic Cough / Bronchitis
('Chronic Cough and Bronchitis',
 'दीर्घकालिक खाँसी और ब्रोंकाइटिस',
 'जिद्दी खोकला',
 'respiratory',
 'Kasa Roga',
 NULL,
 NULL,
 'Persistent cough due to airway inflammation or mucus accumulation.',
 '["persistent cough","wheezing","sputum","breathlessness"]',
 '["infection","kapha accumulation","pollution"]',
 '{"kapha":"excess","vata":"associated"}',
 '{"pranavaha_srotas":"primary"}',
 'moderate',
 0,
 '["avoid cold foods","keep chest warm","hydration"]',
 '{"favour":["warm water","light diet"],"avoid":["curd","cold items"]}'
),

-----------------------------------------------------------------------------------
-- 4. Osteoporosis / Bone Weakness
('Osteoporosis and Bone Weakness',
 'हड्डियों की कमजोरी',
 'हाडांची कमजोरी',
 'musculoskeletal',
 'Asthi Kshaya',
 NULL,
 NULL,
 'Loss of bone density resulting in fragile and easily breakable bones.',
 '["bone pain","frequent fractures","weakness"]',
 '["aging","low calcium","hormonal imbalance"]',
 '{"vata":"high","pitta":"variable","kapha":"low"}',
 '{"asthi_dhatu":"depleted"}',
 'chronic',
 1,
 '["weight bearing exercise","adequate sunlight","calcium rich food"]',
 '{"favour":["milk","sesame seeds","leafy greens"],"avoid":["excess tea coffee","soda"]}'
),

-----------------------------------------------------------------------------------
-- 5. Diabetes Mellitus Type-2
('Diabetes Mellitus Type 2',
 'मधुमेह',
 'मधुमेह',
 'metabolic',
 'Prameha',
 NULL,
 NULL,
 'Metabolic disorder characterized by high blood glucose and insulin resistance.',
 '["excess thirst","frequent urination","fatigue","slow wound healing"]',
 '["obesity","poor diet","inactivity","genetic factors"]',
 '{"kapha":"elevated","pitta":"moderately high","vata":"secondary"}',
 '{"meda_dhatu":"excess","rasa_dhatu":"impure"}',
 'chronic',
 1,
 '["daily walking","weight control","avoid excessive sweets"]',
 '{"favour":["millets","bitter vegetables"],"avoid":["sugar","refined carbs"]}'
),

-----------------------------------------------------------------------------------
-- 6. Obesity
('Obesity',
 'मोटापा',
 'लठ्ठपणा',
 'metabolic',
 'Sthaulya',
 NULL,
 NULL,
 'Excess body fat accumulation associated with metabolic disturbances.',
 '["weight gain","fatigue","breathlessness on exertion"]',
 '["overeating","high-calorie foods","sedentary lifestyle"]',
 '{"kapha":"very_high","vata":"low","pitta":"mildly_increased"}',
 '{"meda_dhatu":"excess"}',
 'chronic',
 1,
 '["regular exercise","avoid daytime sleep"]',
 '{"favour":["warm light foods"],"avoid":["fried foods","sweets"]}'
),

-----------------------------------------------------------------------------------
-- 7. Jaundice (Kamala)
('Jaundice',
 'पीलिया',
 'कामला',
 'hepatic',
 'Kamala',
 NULL,
 NULL,
 'Yellow discoloration of skin and eyes due to bilirubin accumulation.',
 '["yellow eyes","fatigue","low appetite","itching"]',
 '["viral infection","liver inflammation","bile obstruction"]',
 '{"pitta":"very_high","vata":"disturbed"}',
 '{"rakta_dhatu":"affected"}',
 'moderate',
 0,
 '["rest","avoid heavy food"]',
 '{"favour":["light diet","sugarcane juice if appropriate"],"avoid":["spices","oily foods"]}'
),

-----------------------------------------------------------------------------------
-- 8. Diarrhea / IBS
('Diarrhea and IBS',
 'दस्त और आईबीएस',
 'जुलाब व आयबीएस',
 'digestive',
 'Atisara',
 NULL,
 NULL,
 'Increased stool frequency with abdominal discomfort or infection.',
 '["loose stools","abdominal cramps","bloating"]',
 '["infection","weak digestion","food intolerance"]',
 '{"vata":"irregular","pitta":"high","kapha":"variable"}',
 '{"rasa_dhatu":"disturbed"}',
 'moderate',
 0,
 '["maintain hydration","avoid street food"]',
 '{"favour":["rice gruel","pomegranate"],"avoid":["milk","spicy food"]}'
),

-----------------------------------------------------------------------------------
-- 9. Neuromuscular Weakness
('Neuromuscular Weakness',
 'न्यूरो-मस्कुलर कमजोरी',
 'न्यूरो-मस्कुलर कमजोरी',
 'neurological',
 'Vata Vyadhi',
 NULL,
 NULL,
 'Generalized weakness due to poor nerve-muscle coordination.',
 '["muscle weakness","tremors","fatigability"]',
 '["vata aggravation","nutritional deficiency"]',
 '{"vata":"high","pitta":"normal","kapha":"low"}',
 '{"mamsa_dhatu":"low","majja_dhatu":"weakened"}',
 'moderate',
 1,
 '["regular massage","light stretching"]',
 '{"favour":["warm foods","ghee in moderation"],"avoid":["cold dry foods"]}'
);

INSERT INTO plant_disease_mapping (
    plant_id, disease_id,
    efficacy_level, evidence_type,
    mechanism, duration_of_use, contraindications,
    special_instructions, reference_text
)
-------------------------------------------------------------------------------
-- Vidanga → Intestinal Worm Infestation
SELECT p.id, d.id,
       5,'traditional',
       'Embeline shows strong anthelmintic action clearing intestinal parasites.',
       '1-3 weeks with repeat course if needed.',
       'Avoid in pregnancy due to strong expelling action.',
       'Use with light warm diet; avoid sweets which increase krimi.',
       'Vidanga is chief krimighna herb mentioned in Ayurvedic Nighantus.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Embelia ribes'
  AND d.name_en='Intestinal Worm Infestation'

UNION ALL
-- Kantakari → Bronchial Asthma
SELECT p.id, d.id, 4,'traditional',
       'Reduces kapha in lungs and eases bronchospasm.',
       '2-6 weeks.',
       'Use cautiously in severe pitta conditions.',
       'Often used as part of Dashamoola for shwasa.',
       'Kantakari is classical shwasahara herb.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Solanum xanthocarpum'
  AND d.name_en='Bronchial Asthma'

UNION ALL
-- Brihati → Bronchial Asthma
SELECT p.id, d.id, 3,'traditional',
       'Works on kapha accumulation and mucus clearance.',
       '2-6 weeks.',
       'Avoid excessive use in high pitta.',
       'Often co-prescribed with Kantakari.',
       'Brihati used in Dashamoola for respiratory disorders.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Solanum indicum'
  AND d.name_en='Bronchial Asthma'

UNION ALL
-- Malabar Nut → Chronic Cough
SELECT p.id, d.id, 5,'traditional',
       'Vasicine acts as bronchodilator and mucolytic.',
       '1-4 weeks.',
       'Avoid in very low BP.',
       'Best used fresh or as decoction.',
       'Vasaka is well-documented in kasa and shwasa chikitsa.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Adhatoda vasica'
  AND d.name_en='Chronic Cough and Bronchitis'

UNION ALL
-- Asthisamharaka → Osteoporosis
SELECT p.id, d.id, 5,'traditional',
       'Stimulates osteoblasts and accelerates fracture healing.',
       '6-12 weeks.',
       'Avoid excessive drying formulations if patient is vata prakriti.',
       'Combine with calcium-rich diet and sunlight.',
       'Asthisamhara is classical herb for fractures in Ayurveda.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Cissus quadrangularis'
  AND d.name_en='Osteoporosis and Bone Weakness'

UNION ALL
-- Vijayasar → Diabetes
SELECT p.id, d.id, 4,'traditional',
       'Pterostilbene improves glucose metabolism and reduces insulin resistance.',
       '6-12 weeks.',
       'Monitor sugar levels to avoid hypoglycemia.',
       'Commonly given as “diabetic tumbler”.',
       'Vijayasar is central in prameha management.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Pterocarpus marsupium'
  AND d.name_en='Diabetes Mellitus Type 2'

UNION ALL
-- Vijayasar → Obesity
SELECT p.id, d.id, 3,'traditional',
       'Scrapes meda (fat) and reduces inflammation in metabolic tissues.',
       '6-12 weeks.',
       'Use under supervision in liver disorders.',
       'Combine with exercise for best effect.',
       'Vijayasar used in medoroga management.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Pterocarpus marsupium'
  AND d.name_en='Obesity'

UNION ALL
-- Mustaka → IBS / Diarrhea
SELECT p.id, d.id, 4,'traditional',
       'Reduces spasms, diarrhea and normalizes gut motility.',
       '1-4 weeks.',
       'Use cautiously in severe constipation.',
       'Best used as decoction.',
       'Mustaka described in atisara chikitsa.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Cyperus rotundus'
  AND d.name_en='Diarrhea and IBS'

UNION ALL
-- Atibala → Neuromuscular Weakness
SELECT p.id, d.id, 4,'traditional',
       'Strengthens nerves and muscles; improves vata disorders.',
       '4-8 weeks.',
       'Avoid in severe kapha disorders.',
       'Combine with physiotherapy.',
       'Atibala is a balya herb for vata vyadhi.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Abutilon indicum'
  AND d.name_en='Neuromuscular Weakness'

UNION ALL
-- Bala → Neuromuscular Weakness
SELECT p.id, d.id, 5,'traditional',
       'Strong nervine tonic improving muscle strength and nerve conduction.',
       '4-12 weeks.',
       'Avoid overuse in obesity due to snigdha guna.',
       'Pair with abhyanga massage.',
       'Bala is main herb for vata disease.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Sida cordifolia'
  AND d.name_en='Neuromuscular Weakness'

UNION ALL
-- Kutki → Jaundice
SELECT p.id, d.id, 4,'traditional',
       'Strong tikta dravya clearing liver heat and bile stagnation.',
       '2-6 weeks.',
       'Avoid in severe debility.',
       'Combine with light-pitta reducing diet.',
       'Kutki is classical kamala medicine.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Picrorhiza kurroa'
  AND d.name_en='Jaundice'

UNION ALL
-- Bhumyamalaki → Jaundice
SELECT p.id, d.id, 5,'traditional',
       'Supports hepatocyte repair in hepatitis.',
       '4-8 weeks.',
       'Use under medical supervision for acute viral hepatitis.',
       'Encourage hydration.',
       'Bhumyamalaki widely used in kamala.'
FROM plants p JOIN diseases d
WHERE p.botanical_name='Phyllanthus niruri'
  AND d.name_en='Jaundice';

