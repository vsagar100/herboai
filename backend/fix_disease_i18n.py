"""
Fix garbled disease entity_i18n data and add plant_disease_mapping for Hypertension.

Current issues:
1. Disease symptoms/causes/prevention_tips in entity_i18n are character-by-character
   transliterations, not proper Hindi/Marathi translations
2. Hypertension (disease_id=160, 171) has no plant_disease_mapping entries
"""
import sqlite3, os, json

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "db", "new_herboai.db"))

# ══════════════════════════════════════════════════════════════
# PART 1: Fix garbled disease entity_i18n for key diseases
# ══════════════════════════════════════════════════════════════
# Format: (disease_id, field, lang, text)
DISEASE_I18N_FIXES = [
    # ─── Diabetes (id=14) ───
    (14, "symptoms", "hi", '["अत्यधिक प्यास", "बार-बार पेशाब आना", "थकान", "घाव भरने में देरी"]'),
    (14, "symptoms", "mr", '["अतिशय तहान", "वारंवार लघवी होणे", "थकवा", "जखम लवकर भरत नाही"]'),
    (14, "causes", "hi", '["मोटापा", "खराब आहार", "शारीरिक निष्क्रियता", "आनुवांशिक कारण"]'),
    (14, "causes", "mr", '["लठ्ठपणा", "चुकीचा आहार", "शारीरिक निष्क्रियता", "अनुवांशिक कारणे"]'),
    (14, "prevention_tips", "hi", '["प्रतिदिन चलना", "वजन नियंत्रण", "मिठाई का अत्यधिक सेवन न करें"]'),
    (14, "prevention_tips", "mr", '["रोज चालणे", "वजन नियंत्रण", "अतिरिक्त गोड पदार्थ टाळा"]'),
    (14, "description", "hi", "इंसुलिन प्रतिरोध और उच्च रक्त शर्करा से होने वाला चयापचय विकार।"),
    (14, "description", "mr", "इन्सुलिन प्रतिरोध आणि उच्च रक्त शर्करा यामुळे होणारा चयापचय विकार."),

    # ─── Hypertension (id=160) ───
    (160, "symptoms", "hi", '["अक्सर लक्षणरहित", "सिरदर्द", "चक्कर आना", "धड़कन बढ़ना", "थकान"]'),
    (160, "symptoms", "mr", '["बहुतेक वेळा लक्षणरहित", "डोकेदुखी", "चक्कर येणे", "हृदयाची धडधड", "थकवा"]'),
    (160, "causes", "hi", '["अधिक नमक सेवन", "तणाव", "मोटापा", "शारीरिक निष्क्रियता", "शराब", "नींद की कमी"]'),
    (160, "causes", "mr", '["अधिक मीठ सेवन", "ताणतणाव", "लठ्ठपणा", "शारीरिक निष्क्रियता", "मद्यपान", "झोपेची कमतरता"]'),
    (160, "prevention_tips", "hi", '["नमक कम करें", "नियमित व्यायाम", "तणाव प्रबंधन", "पर्याप्त नींद", "नियमित रक्तदाब जाँच"]'),
    (160, "prevention_tips", "mr", '["मीठ कमी करा", "नियमित व्यायाम", "ताणतणाव व्यवस्थापन", "पुरेशी झोप", "नियमित रक्तदाब तपासणी"]'),
    (160, "description", "hi", "रक्तदाब लगातार ऊँचा रहने की स्थिति; हृदय रोग का प्रमुख जोखिम कारक।"),
    (160, "description", "mr", "रक्तदाब सतत उच्च राहण्याची स्थिती; हृदयरोगाचा प्रमुख जोखीम घटक."),

    # ─── High Blood Pressure (id=171) ───
    (171, "symptoms", "hi", '["अक्सर लक्षणरहित", "सिरदर्द", "चक्कर", "धुंधली दृष्टि", "श्वास फूलना"]'),
    (171, "symptoms", "mr", '["बहुधा लक्षणरहित", "डोकेदुखी", "चक्कर", "अंधूक दृष्टी", "धाप लागणे"]'),
    (171, "causes", "hi", '["खराब आहार", "तणाव", "मोटापा", "आनुवांशिक कारण", "धूम्रपान", "शराब"]'),
    (171, "causes", "mr", '["चुकीचा आहार", "ताणतणाव", "लठ्ठपणा", "अनुवांशिक कारणे", "धूम्रपान", "मद्यपान"]'),
    (171, "prevention_tips", "hi", '["नमक कम करें", "फल व सब्जी अधिक खाएं", "नियमित व्यायाम", "वजन नियंत्रण", "तणाव कम करें"]'),
    (171, "prevention_tips", "mr", '["मीठ कमी करा", "फळे व भाज्या जास्त खा", "नियमित व्यायाम", "वजन नियंत्रण", "ताणतणाव कमी करा"]'),
    (171, "description", "hi", "रक्तवाहिकाओं में रक्तदाब लगातार ऊँचा रहने की पुरानी बीमारी।"),
    (171, "description", "mr", "रक्तवाहिन्यांमध्ये रक्तदाब सतत उच्च राहण्याचा जुनाट आजार."),

    # ─── Anxiety and Stress (id=1) ───
    (1, "symptoms", "hi", '["बेचैनी", "नींद न आना", "चिड़चिड़ापन", "ध्यान लगाने में कठिनाई", "सिरदर्द"]'),
    (1, "symptoms", "mr", '["अस्वस्थता", "झोप न लागणे", "चिडचिडेपणा", "लक्ष केंद्रित करण्यात अडचण", "डोकेदुखी"]'),
    (1, "causes", "hi", '["कार्य तणाव", "कम नींद", "अनियमित जीवनशैली", "कैफीन अधिकता"]'),
    (1, "causes", "mr", '["कामाचा ताण", "झोपेची कमतरता", "अनियमित जीवनशैली", "कॅफिन अतिरेक"]'),
    (1, "prevention_tips", "hi", '["योग और ध्यान", "नियमित व्यायाम", "पर्याप्त नींद", "संतुलित आहार"]'),
    (1, "prevention_tips", "mr", '["योग आणि ध्यान", "नियमित व्यायाम", "पुरेशी झोप", "संतुलित आहार"]'),

    # ─── Recurrent Fever (id=3) ───
    (3, "symptoms", "hi", '["बार-बार बुखार", "कमजोरी", "भूख न लगना", "शरीर में दर्द"]'),
    (3, "symptoms", "mr", '["वारंवार ताप येणे", "अशक्तपणा", "भूक न लागणे", "अंगदुखी"]'),
    (3, "causes", "hi", '["संक्रमण", "कमजोर प्रतिरक्षा", "मलेरिया", "टायफाइड"]'),
    (3, "causes", "mr", '["संसर्ग", "कमकुवत प्रतिकारशक्ती", "मलेरिया", "टायफॉइड"]'),
    (3, "prevention_tips", "hi", '["स्वच्छ पानी पिएं", "प्रतिरक्षा मजबूत करें", "स्वच्छता रखें"]'),
    (3, "prevention_tips", "mr", '["स्वच्छ पाणी प्या", "प्रतिकारशक्ती वाढवा", "स्वच्छता राखा"]'),

    # ─── Chronic Liver Disorder (id=4) ───
    (4, "symptoms", "hi", '["थकान", "पेट दर्द", "पीलिया", "भूख न लगना", "वजन कम होना"]'),
    (4, "symptoms", "mr", '["थकवा", "पोटदुखी", "कावीळ", "भूक न लागणे", "वजन घटणे"]'),
    (4, "causes", "hi", '["शराब का अत्यधिक सेवन", "हेपेटाइटिस", "मोटापा", "खराब आहार"]'),
    (4, "causes", "mr", '["मद्यपान अतिरेक", "हिपॅटायटिस", "लठ्ठपणा", "चुकीचा आहार"]'),
    (4, "prevention_tips", "hi", '["शराब से बचें", "संतुलित आहार", "नियमित जाँच", "व्यायाम"]'),
    (4, "prevention_tips", "mr", '["मद्यपान टाळा", "संतुलित आहार", "नियमित तपासणी", "व्यायाम"]'),

    # ─── Chronic Skin Disease (id=5) ───
    (5, "symptoms", "hi", '["खुजली", "लालिमा", "चकत्ते", "रूखी त्वचा", "दाने"]'),
    (5, "symptoms", "mr", '["खाज", "लालसरपणा", "पुरळ", "कोरडी त्वचा", "फोड"]'),
    (5, "causes", "hi", '["एलर्जी", "तणाव", "आनुवांशिकता", "प्रदूषण", "खराब आहार"]'),
    (5, "causes", "mr", '["ऍलर्जी", "ताणतणाव", "आनुवंशिकता", "प्रदूषण", "चुकीचा आहार"]'),
    (5, "prevention_tips", "hi", '["त्वचा साफ रखें", "तणाव कम करें", "संतुलित आहार", "पर्याप्त पानी पिएं"]'),
    (5, "prevention_tips", "mr", '["त्वचा स्वच्छ ठेवा", "ताणतणाव कमी करा", "संतुलित आहार", "पुरेसे पाणी प्या"]'),

    # ─── Ischemic Heart Disease (id=6) ───
    (6, "symptoms", "hi", '["सीने में दर्द", "श्वास फूलना", "थकान", "चक्कर आना"]'),
    (6, "symptoms", "mr", '["छातीत दुखणे", "धाप लागणे", "थकवा", "चक्कर येणे"]'),
    (6, "causes", "hi", '["उच्च कोलेस्ट्रॉल", "उच्च रक्तदाब", "मोटापा", "धूम्रपान", "मधुमेह"]'),
    (6, "causes", "mr", '["उच्च कोलेस्टेरॉल", "उच्च रक्तदाब", "लठ्ठपणा", "धूम्रपान", "मधुमेह"]'),
    (6, "prevention_tips", "hi", '["स्वस्थ आहार", "नियमित व्यायाम", "धूम्रपान छोड़ें", "तणाव कम करें"]'),
    (6, "prevention_tips", "mr", '["स्वास्थ्यपूर्ण आहार", "नियमित व्यायाम", "धूम्रपान सोडा", "ताणतणाव कमी करा"]'),

    # ─── Urinary Stones (id=7) ───
    (7, "symptoms", "hi", '["पेट में तेज दर्द", "पेशाब में खून", "जलन", "बार-बार पेशाब"]'),
    (7, "symptoms", "mr", '["पोटात तीव्र वेदना", "लघवीत रक्त", "जळजळ", "वारंवार लघवी"]'),
    (7, "causes", "hi", '["कम पानी पीना", "अधिक नमक", "आनुवांशिकता", "कुछ दवाएं"]'),
    (7, "causes", "mr", '["कमी पाणी पिणे", "अधिक मीठ", "आनुवंशिकता", "काही औषधे"]'),
    (7, "prevention_tips", "hi", '["पर्याप्त पानी पिएं", "नमक कम करें", "संतुलित आहार"]'),
    (7, "prevention_tips", "mr", '["पुरेसे पाणी प्या", "मीठ कमी करा", "संतुलित आहार"]'),

    # ─── Menstrual Irregularity (id=8) ───
    (8, "symptoms", "hi", '["अनियमित माहवारी", "अधिक रक्तस्राव", "दर्द", "मूड बदलना"]'),
    (8, "symptoms", "mr", '["अनियमित मासिक पाळी", "अधिक रक्तस्राव", "वेदना", "मूड बदलणे"]'),
    (8, "causes", "hi", '["हार्मोनल असंतुलन", "तणाव", "थायराइड विकार", "PCOS"]'),
    (8, "causes", "mr", '["हार्मोनल असंतुलन", "ताणतणाव", "थायरॉईड विकार", "PCOS"]'),
    (8, "prevention_tips", "hi", '["नियमित व्यायाम", "संतुलित आहार", "तणाव प्रबंधन", "पर्याप्त नींद"]'),
    (8, "prevention_tips", "mr", '["नियमित व्यायाम", "संतुलित आहार", "ताणतणाव व्यवस्थापन", "पुरेशी झोप"]'),

    # ─── Gastric Ulcer and Hyperacidity (id=9) ───
    (9, "symptoms", "hi", '["सीने में जलन", "पेट दर्द", "खट्टी डकार", "मतली", "भूख कम"]'),
    (9, "symptoms", "mr", '["छातीत जळजळ", "पोटदुखी", "आंबट ढेकर", "मळमळ", "भूक कमी"]'),
    (9, "causes", "hi", '["अनियमित भोजन", "मसालेदार भोजन", "तणाव", "धूम्रपान", "दवाएं (NSAIDs)"]'),
    (9, "causes", "mr", '["अनियमित जेवण", "तिखट अन्न", "ताणतणाव", "धूम्रपान", "औषधे (NSAIDs)"]'),
    (9, "prevention_tips", "hi", '["समय पर भोजन", "मसालेदार भोजन कम करें", "तणाव प्रबंधन", "शराब से बचें"]'),
    (9, "prevention_tips", "mr", '["वेळेवर जेवण", "तिखट अन्न कमी करा", "ताणतणाव व्यवस्थापन", "मद्यपान टाळा"]'),

    # ─── Intestinal Worm Infestation (id=10) ───
    (10, "symptoms", "hi", '["पेट दर्द", "दस्त", "वजन कम होना", "खुजली (गुदा)", "भूख बदलना"]'),
    (10, "symptoms", "mr", '["पोटदुखी", "जुलाब", "वजन घटणे", "खाज (गुदद्वार)", "भूक बदलणे"]'),
    (10, "causes", "hi", '["दूषित पानी/भोजन", "स्वच्छता की कमी", "कच्चा मांस"]'),
    (10, "causes", "mr", '["दूषित पाणी/अन्न", "स्वच्छतेचा अभाव", "कच्चे मांस"]'),
    (10, "prevention_tips", "hi", '["हाथ अवश्य धोएं", "स्वच्छ पानी पिएं", "फल-सब्जी धोकर खाएं"]'),
    (10, "prevention_tips", "mr", '["हात अवश्य धुवा", "स्वच्छ पाणी प्या", "फळे-भाज्या धुवून खा"]'),

    # ─── Bronchial Asthma (id=11) ───
    (11, "symptoms", "hi", '["श्वास फूलना", "खाँसी", "सीने में जकड़न", "घरघराहट"]'),
    (11, "symptoms", "mr", '["धाप लागणे", "खोकला", "छातीत आकुंचन", "श्वासात घरघर"]'),
    (11, "causes", "hi", '["एलर्जी", "धूल", "प्रदूषण", "ठंडी हवा", "तणाव"]'),
    (11, "causes", "mr", '["ऍलर्जी", "धूळ", "प्रदूषण", "थंड हवा", "ताणतणाव"]'),
    (11, "prevention_tips", "hi", '["एलर्जी कारकों से बचें", "नियमित व्यायाम", "धूम्रपान छोड़ें"]'),
    (11, "prevention_tips", "mr", '["ऍलर्जी कारणे टाळा", "नियमित व्यायाम", "धूम्रपान सोडा"]'),

    # ─── Chronic Cough and Bronchitis (id=12) ───
    (12, "symptoms", "hi", '["लगातार खाँसी", "कफ निकलना", "श्वास फूलना", "सीने में दर्द"]'),
    (12, "symptoms", "mr", '["सतत खोकला", "कफ पडणे", "धाप लागणे", "छातीत दुखणे"]'),
    (12, "causes", "hi", '["श्वसन संक्रमण", "धूम्रपान", "प्रदूषण", "एलर्जी"]'),
    (12, "causes", "mr", '["श्वसन संसर्ग", "धूम्रपान", "प्रदूषण", "ऍलर्जी"]'),
    (12, "prevention_tips", "hi", '["धूम्रपान छोड़ें", "प्रदूषण से बचें", "गर्म पानी पिएं", "भाप लें"]'),
    (12, "prevention_tips", "mr", '["धूम्रपान सोडा", "प्रदूषण टाळा", "कोमट पाणी प्या", "वाफ घ्या"]'),

    # ─── Osteoporosis and Bone Weakness (id=13) ───
    (13, "symptoms", "hi", '["हड्डियों में दर्द", "आसानी से फ्रैक्चर", "कमर दर्द", "ऊँचाई कम होना"]'),
    (13, "symptoms", "mr", '["हाडांमध्ये दुखणे", "सहज फ्रॅक्चर", "कमरदुखी", "उंची कमी होणे"]'),
    (13, "causes", "hi", '["कैल्शियम की कमी", "विटामिन D की कमी", "व्यायाम न करना", "उम्र बढ़ना"]'),
    (13, "causes", "mr", '["कॅल्शियमची कमतरता", "व्हिटॅमिन D ची कमतरता", "व्यायामाचा अभाव", "वाढते वय"]'),
    (13, "prevention_tips", "hi", '["कैल्शियम युक्त आहार", "विटामिन D", "नियमित व्यायाम", "धूम्रपान छोड़ें"]'),
    (13, "prevention_tips", "mr", '["कॅल्शियमयुक्त आहार", "व्हिटॅमिन D", "नियमित व्यायाम", "धूम्रपान सोडा"]'),

    # ─── Obesity (id=15) ───
    (15, "symptoms", "hi", '["अधिक वजन", "थकान", "श्वास फूलना", "जोड़ों में दर्द", "पसीना अधिक"]'),
    (15, "symptoms", "mr", '["अतिरिक्त वजन", "थकवा", "धाप लागणे", "सांधेदुखी", "अधिक घाम"]'),
    (15, "causes", "hi", '["अस्वस्थ आहार", "शारीरिक निष्क्रियता", "आनुवांशिकता", "हार्मोनल असंतुलन"]'),
    (15, "causes", "mr", '["अस्वास्थ्यकर आहार", "शारीरिक निष्क्रियता", "अनुवांशिकता", "हार्मोनल असंतुलन"]'),
    (15, "prevention_tips", "hi", '["संतुलित आहार", "नियमित व्यायाम", "पर्याप्त नींद", "पानी अधिक पिएं"]'),
    (15, "prevention_tips", "mr", '["संतुलित आहार", "नियमित व्यायाम", "पुरेशी झोप", "पुरेसे पाणी प्या"]'),

    # ─── Jaundice (id=16) ───
    (16, "symptoms", "hi", '["आँखों और त्वचा में पीलापन", "थकान", "भूख न लगना", "खुजली", "गहरे रंग का मूत्र"]'),
    (16, "symptoms", "mr", '["डोळे व त्वचा पिवळी होणे", "थकवा", "भूक न लागणे", "खाज", "गडद रंगाचे मूत्र"]'),
    (16, "causes", "hi", '["यकृत संक्रमण", "पित्ताश्मरी", "हेपेटाइटिस", "शराब"]'),
    (16, "causes", "mr", '["यकृत संसर्ग", "पित्ताशयातील खडे", "हिपॅटायटिस", "मद्यपान"]'),
    (16, "prevention_tips", "hi", '["स्वच्छ पानी पिएं", "शराब से बचें", "स्वच्छता रखें", "टीकाकरण"]'),
    (16, "prevention_tips", "mr", '["स्वच्छ पाणी प्या", "मद्यपान टाळा", "स्वच्छता राखा", "लसीकरण"]'),

    # ─── Diarrhea and IBS (id=17) ───
    (17, "symptoms", "hi", '["बार-बार दस्त", "पेट दर्द", "ऐंठन", "गैस", "जी मिचलाना"]'),
    (17, "symptoms", "mr", '["वारंवार जुलाब", "पोटदुखी", "पोटात पेटके", "गॅस", "मळमळ"]'),
    (17, "causes", "hi", '["संक्रमण", "खराब आहार", "तणाव", "दवाएं"]'),
    (17, "causes", "mr", '["संसर्ग", "चुकीचा आहार", "ताणतणाव", "औषधे"]'),
    (17, "prevention_tips", "hi", '["स्वच्छ भोजन", "पानी उबालकर पिएं", "हाथ धोएं", "तणाव कम करें"]'),
    (17, "prevention_tips", "mr", '["स्वच्छ अन्न", "पाणी उकळून प्या", "हात धुवा", "ताणतणाव कमी करा"]'),

    # ─── Neuromuscular Weakness (id=18) ───
    (18, "symptoms", "hi", '["मांसपेशियों में कमजोरी", "थकान", "संतुलन की कमी", "अकड़न", "सुन्नपन"]'),
    (18, "symptoms", "mr", '["स्नायूंमध्ये कमकुवतपणा", "थकवा", "संतुलनाचा अभाव", "ताठरपणा", "बधिरपणा"]'),
    (18, "causes", "hi", '["पोषण की कमी", "तंत्रिका विकार", "उम्र बढ़ना", "विटामिन B12 की कमी"]'),
    (18, "causes", "mr", '["पोषणाची कमतरता", "मज्जातंतू विकार", "वाढते वय", "व्हिटॅमिन B12 ची कमतरता"]'),
    (18, "prevention_tips", "hi", '["संतुलित आहार", "नियमित व्यायाम", "विटामिन पूर्ति", "पर्याप्त आराम"]'),
    (18, "prevention_tips", "mr", '["संतुलित आहार", "नियमित व्यायाम", "व्हिटॅमिन पूर्ती", "पुरेशी विश्रांती"]'),

    # ─── Common Cold (id=173) ───
    (173, "symptoms", "hi", '["नाक बहना", "छींकना", "गले में खराश", "हल्का बुखार", "खाँसी"]'),
    (173, "symptoms", "mr", '["नाक वाहणे", "शिंकणे", "घसा दुखणे", "हलका ताप", "खोकला"]'),
    (173, "causes", "hi", '["वायरस संक्रमण", "ठंड लगना", "कमजोर प्रतिरक्षा"]'),
    (173, "causes", "mr", '["विषाणू संसर्ग", "थंडी लागणे", "कमकुवत प्रतिकारशक्ती"]'),
    (173, "prevention_tips", "hi", '["हाथ धोएं", "गर्म पानी पिएं", "प्रतिरक्षा मजबूत करें", "ठंड से बचें"]'),
    (173, "prevention_tips", "mr", '["हात धुवा", "कोमट पाणी प्या", "प्रतिकारशक्ती वाढवा", "थंडीपासून बचाव"]'),
    (173, "description", "hi", "नाक और गले का वायरल संक्रमण; सामान्यतः स्वयं ठीक होता है।"),
    (173, "description", "mr", "नाक आणि घशाचा विषाणू संसर्ग; साधारणतः स्वतःच बरा होतो."),
    (173, "name", "hi", "सामान्य सर्दी"),
    (173, "name", "mr", "सामान्य सर्दी"),

    # ─── Allergic Rhinitis (id=164) ───
    (164, "symptoms", "hi", '["छींकना", "नाक बहना", "आँखों में खुजली", "नाक बंद होना"]'),
    (164, "symptoms", "mr", '["शिंकणे", "नाक वाहणे", "डोळ्यांना खाज", "नाक बंद होणे"]'),
    (164, "causes", "hi", '["धूल", "पराग", "पालतू जानवर", "फफूंद"]'),
    (164, "causes", "mr", '["धूळ", "परागकण", "पाळीव प्राणी", "बुरशी"]'),
    (164, "prevention_tips", "hi", '["धूल से बचें", "एयर फिल्टर उपयोग करें", "घर साफ रखें"]'),
    (164, "prevention_tips", "mr", '["धूळ टाळा", "एअर फिल्टर वापरा", "घर स्वच्छ ठेवा"]'),

    # ─── Low Blood Pressure (id=172) ───
    (172, "symptoms", "hi", '["चक्कर आना", "धुंधली दृष्टि", "बेहोशी", "थकान", "जी मिचलाना"]'),
    (172, "symptoms", "mr", '["चक्कर येणे", "अंधूक दृष्टी", "बेशुद्ध पडणे", "थकवा", "मळमळ"]'),
    (172, "causes", "hi", '["निर्जलीकरण", "अधिक रक्तस्राव", "हृदय विकार", "कुपोषण"]'),
    (172, "causes", "mr", '["निर्जलीकरण", "अधिक रक्तस्राव", "हृदय विकार", "कुपोषण"]'),
    (172, "prevention_tips", "hi", '["पर्याप्त पानी पिएं", "नमक थोड़ा बढ़ाएं", "धीरे-धीरे खड़े हों"]'),
    (172, "prevention_tips", "mr", '["पुरेसे पाणी प्या", "मीठ थोडे वाढवा", "हळूहळू उभे राहा"]'),

    # ─── Acne / Pimples (id=184) ───
    (184, "symptoms", "hi", '["चेहरे पर दाने", "लालिमा", "सूजन", "काले धब्बे"]'),
    (184, "symptoms", "mr", '["चेहऱ्यावर मुरुम", "लालसरपणा", "सूज", "काळे डाग"]'),
    (184, "causes", "hi", '["हार्मोनल बदलाव", "तैलीय त्वचा", "तणाव", "खराब आहार"]'),
    (184, "causes", "mr", '["हार्मोनल बदल", "तेलकट त्वचा", "ताणतणाव", "चुकीचा आहार"]'),
    (184, "prevention_tips", "hi", '["चेहरा साफ रखें", "तैलीय भोजन कम करें", "पानी अधिक पिएं"]'),
    (184, "prevention_tips", "mr", '["चेहरा स्वच्छ ठेवा", "तेलकट अन्न कमी करा", "पुरेसे पाणी प्या"]'),
]

# ══════════════════════════════════════════════════════════════
# PART 2: Add plant_disease_mapping for Hypertension
# ══════════════════════════════════════════════════════════════
# We need to link blood-pressure-friendly plants to disease_id=160
# Plants known in Ayurveda for hypertension management:
# Looking up their IDs from the database dynamically

HYPERTENSION_PLANT_NAMES = [
    # Ayurvedic plants commonly used for blood pressure
    "Arjuna",        # Terminalia arjuna - primary for heart/BP
    "Sarpagandha",   # Rauwolfia serpentina - classic for BP
    "Ashwagandha",   # Withania somnifera - adaptogen, stress-BP
    "Garlic",        # Allium sativum - well known for BP
    "Brahmi",        # Bacopa monnieri - calming, supports BP
    "Jatamansi",     # Nardostachys jatamansi - calming
    "Shankhpushpi",  # Convolvulus pluricaulis - calming, BP
    "Gokshura",      # Tribulus terrestris - renal, BP
    "Punarnava",     # Boerhavia diffusa - diuretic, BP
    "Moringa",       # Drumstick - nutritive, BP
]


def main():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # ── PART 1: Fix disease entity_i18n ──
    print("=== PART 1: Fixing disease entity_i18n ===")
    updated = 0
    inserted = 0
    for disease_id, field, lang, text in DISEASE_I18N_FIXES:
        # Check if row exists
        existing = conn.execute(
            "SELECT id FROM entity_i18n WHERE entity_type='disease' AND entity_id=? AND lang=? AND field=?",
            (disease_id, lang, field)
        ).fetchone()
        
        if existing:
            conn.execute(
                """UPDATE entity_i18n 
                   SET text=?, status='verified', source='manual', updated_at=CURRENT_TIMESTAMP
                   WHERE entity_type='disease' AND entity_id=? AND lang=? AND field=?""",
                (text, disease_id, lang, field)
            )
            updated += 1
        else:
            conn.execute(
                """INSERT INTO entity_i18n(entity_type, entity_id, lang, field, text, status, source)
                   VALUES('disease', ?, ?, ?, ?, 'verified', 'manual')""",
                (disease_id, lang, field, text)
            )
            inserted += 1
    
    conn.commit()
    print(f"  Disease i18n: updated={updated}, inserted={inserted}")
    
    # ── PART 2: Add plant_disease_mapping for Hypertension ──
    print("\n=== PART 2: Adding plant_disease_mapping for Hypertension ===")
    
    # Find plant IDs
    plant_ids_found = []
    for plant_name in HYPERTENSION_PLANT_NAMES:
        row = conn.execute(
            """SELECT id, common_name_en FROM plants 
               WHERE LOWER(common_name_en) LIKE ? 
                  OR LOWER(botanical_name) LIKE ?
               LIMIT 1""",
            (f"%{plant_name.lower()}%", f"%{plant_name.lower()}%")
        ).fetchone()
        if row:
            plant_ids_found.append((row["id"], row["common_name_en"]))
        else:
            print(f"  WARNING: Plant '{plant_name}' not found in DB")
    
    print(f"  Found {len(plant_ids_found)} plants for Hypertension mapping")
    
    # Check existing mappings
    mapping_inserted = 0
    for disease_id in [160, 171]:  # both hypertension diseases
        for plant_id, plant_name in plant_ids_found:
            existing = conn.execute(
                "SELECT id FROM plant_disease_mapping WHERE plant_id=? AND disease_id=?",
                (plant_id, disease_id)
            ).fetchone()
            if existing:
                continue
            
            conn.execute(
                """INSERT INTO plant_disease_mapping(plant_id, disease_id, efficacy_level, evidence_type, mechanism)
                   VALUES(?, ?, ?, ?, ?)""",
                (plant_id, disease_id, 3, "traditional", 
                 f"{plant_name} is traditionally used in Ayurveda for blood pressure management")
            )
            mapping_inserted += 1
            print(f"  Mapped: {plant_name} (id={plant_id}) -> disease_id={disease_id}")
    
    conn.commit()
    print(f"  Mappings inserted: {mapping_inserted}")
    
    # ── Verification ──
    print("\n=== Verification ===")
    
    # Check disease i18n for Hypertension
    rows = conn.execute(
        "SELECT field, lang, text FROM entity_i18n WHERE entity_type='disease' AND entity_id=160 AND field='symptoms' ORDER BY lang"
    ).fetchall()
    for r in rows:
        print(f"  disease 160 symptoms ({r['lang']}): {r['text'][:80]}")
    
    # Check plant_disease_mapping for hypertension
    rows = conn.execute("""
        SELECT p.common_name_en, pdm.efficacy_level
        FROM plant_disease_mapping pdm 
        JOIN plants p ON p.id = pdm.plant_id
        WHERE pdm.disease_id = 160
    """).fetchall()
    print(f"\n  Plants mapped to Hypertension (160): {len(rows)}")
    for r in rows:
        print(f"    {r['common_name_en']} ({r['efficacy_level']})")
    
    # Check preps now available for hypertension
    rows = conn.execute("""
        SELECT DISTINCT pr.id, pr.name_en
        FROM preparations pr
        JOIN plants pl ON pl.id = pr.plant_id
        JOIN plant_disease_mapping pdm ON pdm.plant_id = pl.id
        WHERE pdm.disease_id = 160
        LIMIT 10
    """).fetchall()
    print(f"\n  Preparations now available for Hypertension: {len(rows)}")
    for r in rows:
        print(f"    prep_id={r['id']}: {r['name_en']}")
    
    conn.close()
    print("\nDone!")

if __name__ == "__main__":
    main()
