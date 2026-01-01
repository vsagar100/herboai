BEGIN;

-- =========================================================
-- Common diseases to add (new rows) with valid JSON columns
-- NOTE: symptoms/causes/prevention_tips MUST be JSON arrays
--       dosha_involvement/dhatu_involvement/dietary_recommendations MUST be JSON
-- =========================================================

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('High Blood Pressure (Hypertension)','उच्च रक्तचाप','उच्च रक्तदाब','cardiovascular',
 NULL,NULL,NULL,
 'A chronic condition where arterial blood pressure remains persistently elevated; often asymptomatic but increases cardiovascular risk.',
 '["Often none (silent)","Headache","Dizziness","Blurred vision","Shortness of breath","Chest discomfort"]',
 '["High salt intake","Obesity","Physical inactivity","Stress","Family history","Kidney disease","Alcohol/tobacco use"]',
 '{"vata":"secondary","pitta":"secondary","kapha":"primary"}',
 '{"rakta":"primary","rasa":"secondary"}',
 'chronic',1,
 '["Reduce salt","Maintain healthy weight","Regular walking/exercise","Limit alcohol","Stop tobacco","Regular BP checks","Manage stress and sleep"]',
 '{"recommended":["vegetables","whole grains","fruits","low-salt foods","adequate water"],"avoid":["excess salt","processed foods","excess caffeine","excess alcohol"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Low Blood Pressure (Hypotension)','निम्न रक्तचाप','कमी रक्तदाब','cardiovascular',
 NULL,NULL,NULL,
 'A condition where blood pressure is lower than normal; may be asymptomatic or cause dizziness/fainting depending on cause.',
 '["Dizziness","Lightheadedness","Fainting","Blurred vision","Fatigue","Nausea"]',
 '["Dehydration","Prolonged standing","Blood loss","Certain medicines","Heart conditions","Endocrine issues"]',
 '{"vata":"primary","pitta":"secondary","kapha":"secondary"}',
 '{"rasa":"primary","rakta":"secondary"}',
 'moderate',0,
 '["Adequate hydration","Rise slowly from sitting/lying","Small frequent meals","Avoid prolonged standing","Check medicines with clinician"]',
 '{"recommended":["adequate fluids","oral rehydration","balanced meals"],"avoid":["skipping meals","dehydrating drinks (excess alcohol)"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Common Cold (Acute Rhinitis)','सामान्य सर्दी-जुकाम','सामान्य सर्दी-खोकला','respiratory',
 NULL,NULL,NULL,
 'A common viral upper respiratory infection causing nasal congestion, sore throat, and cough.',
 '["Runny/blocked nose","Sneezing","Sore throat","Mild fever","Cough","Body ache"]',
 '["Viral infection","Close contact","Poor hand hygiene","Crowded places","Low sleep"]',
 '{"vata":"secondary","pitta":"secondary","kapha":"primary"}',
 '{"rasa":"primary"}',
 'mild',0,
 '["Hand hygiene","Warm fluids","Adequate rest","Avoid close contact when ill","Use mask in crowded areas if needed"]',
 '{"recommended":["warm soups","ginger-infused warm water","light meals"],"avoid":["cold drinks","heavy fried food"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Acid Reflux / GERD','अम्लपित्त / एसिड रिफ्लक्स','अम्लपित्त / अ‍ॅसिड रिफ्लक्स','digestive',
 'अम्लपित्त',NULL,NULL,
 'A digestive disorder where stomach acid frequently flows back into the food pipe, causing burning and regurgitation.',
 '["Heartburn","Sour belching","Chest burning after meals","Nausea","Bloating","Throat irritation"]',
 '["Spicy/fatty meals","Late-night eating","Obesity","Alcohol/tobacco","Certain medicines","Hiatal hernia"]',
 '{"pitta":"primary","vata":"secondary","kapha":"secondary"}',
 '{"rasa":"secondary","rakta":"secondary"}',
 'chronic',1,
 '["Eat smaller meals","Avoid late-night meals","Reduce spicy/fried food","Weight management","Elevate head while sleeping"]',
 '{"recommended":["light meals","buttermilk (if tolerated)","cooked vegetables"],"avoid":["spicy food","deep-fried food","excess tea/coffee","late-night heavy meals"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Urinary Tract Infection (UTI)','मूत्र मार्ग संक्रमण','मूत्रमार्ग संसर्ग','urinary',
 NULL,NULL,NULL,
 'An infection of the urinary tract causing burning urination, frequency, and lower abdominal discomfort.',
 '["Burning urination","Frequent urination","Urgency","Lower abdominal pain","Foul-smelling urine","Fever (sometimes)"]',
 '["Bacterial infection","Low water intake","Poor hygiene","Urine retention","Diabetes","Catheter use"]',
 '{"pitta":"primary","vata":"secondary","kapha":"secondary"}',
 '{"mutravaha_srotas":"primary","rakta":"secondary"}',
 'moderate',0,
 '["Increase water intake","Do not hold urine","Hygiene","Urinate after intercourse","Manage blood sugar if diabetic"]',
 '{"recommended":["adequate fluids","light meals","coconut water (if tolerated)"],"avoid":["dehydration","excess irritants (very spicy food)"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Chronic Kidney Disease (CKD)','दीर्घकालिक गुर्दा रोग','दीर्घकालीन मूत्रपिंड विकार','urinary',
 NULL,NULL,NULL,
 'A long-term decline in kidney function; often associated with diabetes and hypertension.',
 '["Fatigue","Swelling in legs","Reduced appetite","Nausea","Changes in urination","High blood pressure"]',
 '["Diabetes","Hypertension","Recurrent kidney infections","Long-term analgesic use","Glomerular diseases"]',
 '{"vata":"primary","kapha":"secondary","pitta":"secondary"}',
 '{"mutravaha_srotas":"primary","rasa":"secondary"}',
 'chronic',0,
 '["Regular monitoring","Control BP and blood sugar","Avoid unnecessary painkillers","Adequate hydration as advised","Follow clinician dietary advice"]',
 '{"recommended":["as advised by clinician","balanced protein (not excess)"],"avoid":["self-medication","excess salt","highly processed food"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('High Uric Acid / Gout','उच्च यूरिक एसिड / गाउट','युरिक अ‍ॅसिड वाढ / गाऊट','musculoskeletal',
 NULL,NULL,NULL,
 'A metabolic condition where uric acid builds up, sometimes causing painful joint inflammation (gout attacks).',
 '["Sudden joint pain (often big toe)","Swelling","Redness","Warmth","Limited movement"]',
 '["High purine diet","Alcohol","Obesity","Kidney dysfunction","Dehydration","Genetic tendency"]',
 '{"vata":"primary","pitta":"secondary","kapha":"secondary"}',
 '{"asthi":"primary","rakta":"secondary"}',
 'chronic',1,
 '["Hydration","Weight management","Limit alcohol","Limit high-purine foods","Regular activity"]',
 '{"recommended":["water","low-fat dairy (if tolerated)","vegetables"],"avoid":["organ meats","excess red meat","beer/alcohol"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Thyroid Underactivity (Hypothyroidism)','हाइपोथायरॉइडिज्म (थायरॉइड की कमी)','हायपोथायरॉईड (थायरॉईड कमी)','endocrine',
 NULL,NULL,NULL,
 'A condition where the thyroid gland produces insufficient hormones, leading to sluggish metabolism.',
 '["Fatigue","Weight gain","Cold intolerance","Dry skin","Constipation","Slow heart rate"]',
 '["Autoimmune thyroiditis","Iodine deficiency/excess","Thyroid surgery","Certain medicines"]',
 '{"kapha":"primary","vata":"secondary","pitta":"secondary"}',
 '{"rasa":"primary","meda":"secondary"}',
 'chronic',0,
 '["Regular screening if symptomatic","Adequate sleep","Balanced diet","Follow prescribed therapy"]',
 '{"recommended":["balanced meals","adequate protein"],"avoid":["extreme dieting","self-medication"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Thyroid Overactivity (Hyperthyroidism)','हाइपरथायरॉइडिज्म (थायरॉइड की अधिकता)','हायपरथायरॉईड (थायरॉईड वाढ)','endocrine',
 NULL,NULL,NULL,
 'A condition where the thyroid gland produces excess hormones, increasing metabolic activity.',
 '["Weight loss","Palpitations","Heat intolerance","Anxiety","Tremor","Increased appetite"]',
 '["Autoimmune (Graves)","Thyroid nodules","Excess iodine","Thyroid inflammation"]',
 '{"pitta":"primary","vata":"secondary","kapha":"secondary"}',
 '{"rasa":"secondary","rakta":"secondary"}',
 'chronic',0,
 '["Avoid excess stimulants","Adequate sleep","Clinical evaluation and monitoring"]',
 '{"recommended":["balanced meals","adequate fluids"],"avoid":["excess caffeine","self-medication"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Depression (Low Mood Disorder)','अवसाद','नैराश्य / नैराश्य विकार','mental_health',
 NULL,NULL,NULL,
 'A mood disorder characterized by persistent low mood, loss of interest, and functional impairment.',
 '["Persistent sadness","Loss of interest","Sleep changes","Low energy","Poor concentration","Feelings of hopelessness"]',
 '["Chronic stress","Life events","Genetic tendency","Substance use","Medical illnesses"]',
 '{"vata":"primary","kapha":"secondary","pitta":"secondary"}',
 '{"manovaha_srotas":"primary"}',
 'chronic',0,
 '["Seek professional support","Regular routine and sleep","Physical activity","Social support","Avoid alcohol/substance misuse"]',
 '{"recommended":["regular meals","omega-3 sources if appropriate","adequate hydration"],"avoid":["excess alcohol","sleep deprivation"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('PCOS / Menstrual Hormonal Imbalance','पीसीओएस / हार्मोनल असंतुलन','पीसीओएस / हार्मोनल असंतुलन','gynecology',
 NULL,NULL,NULL,
 'A hormonal disorder that can cause irregular periods, acne, and weight gain; often linked with insulin resistance.',
 '["Irregular periods","Acne","Excess hair growth","Weight gain","Pelvic discomfort (sometimes)"]',
 '["Insulin resistance","Genetic tendency","Obesity","Lifestyle factors"]',
 '{"kapha":"primary","vata":"secondary","pitta":"secondary"}',
 '{"artava":"primary","meda":"secondary"}',
 'chronic',1,
 '["Weight management","Regular exercise","Balanced low-glycemic diet","Sleep routine","Medical follow-up"]',
 '{"recommended":["high-fiber foods","vegetables","whole grains","protein"],"avoid":["high sugar foods","highly processed food"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Non-Alcoholic Fatty Liver (NAFLD)','गैर-मादक वसायुक्त यकृत रोग','नॉन-अल्कोहोलिक फॅटी लिव्हर','hepatic',
 NULL,NULL,NULL,
 'Fat accumulation in liver not due to alcohol; commonly linked with obesity and insulin resistance.',
 '["Often none","Fatigue","Right upper abdominal heaviness","Elevated liver enzymes"]',
 '["Obesity","Insulin resistance","High triglycerides","Sedentary lifestyle"]',
 '{"kapha":"primary","pitta":"secondary","vata":"secondary"}',
 '{"yakrit":"primary","meda":"secondary"}',
 'chronic',1,
 '["Weight reduction","Regular exercise","Limit sugar and refined carbs","Medical monitoring"]',
 '{"recommended":["vegetables","whole grains","lean protein"],"avoid":["sugary drinks","refined carbs","excess fried food"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Anxiety Disorder (Persistent Worry)','चिंता विकार','चिंता विकार','mental_health',
 NULL,NULL,NULL,
 'A condition with persistent excessive worry, restlessness, and physical symptoms affecting daily life.',
 '["Excessive worry","Restlessness","Palpitations","Sweating","Sleep issues","Irritability"]',
 '["Chronic stress","Genetic tendency","Substance use","Medical illness","Sleep deprivation"]',
 '{"vata":"primary","pitta":"secondary","kapha":"secondary"}',
 '{"manovaha_srotas":"primary"}',
 'chronic',0,
 '["Breathing exercises","Sleep hygiene","Limit caffeine","Structured routine","Seek professional support if persistent"]',
 '{"recommended":["warm light meals","adequate hydration"],"avoid":["excess caffeine","alcohol misuse","sleep deprivation"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Acne / Pimples','मुंहासे','मुरुम','skin',
 NULL,NULL,NULL,
 'A common skin condition with pimples due to blocked follicles and inflammation.',
 '["Pimples","Oily skin","Blackheads/whiteheads","Redness","Tender bumps"]',
 '["Hormonal changes","Oily skin","Stress","Cosmetics","Diet triggers in some"]',
 '{"pitta":"primary","kapha":"secondary","vata":"secondary"}',
 '{"rakta":"primary","rasa":"secondary"}',
 'moderate',1,
 '["Gentle cleansing","Avoid comedogenic cosmetics","Do not pick lesions","Balanced diet","Adequate sleep"]',
 '{"recommended":["vegetables","adequate water"],"avoid":["high sugar foods","excess oily/junk foods"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Dandruff / Scalp Scaling','रूसी (डैंड्रफ)','कोंडा','skin',
 NULL,NULL,NULL,
 'A scalp condition causing flaking and itching; can be aggravated by dryness or oily scalp and yeast overgrowth.',
 '["White flakes","Scalp itching","Scalp redness (sometimes)","Dryness or greasiness"]',
 '["Seborrheic tendency","Dry scalp","Stress","Weather changes","Yeast overgrowth"]',
 '{"kapha":"primary","pitta":"secondary","vata":"secondary"}',
 '{"rasa":"secondary"}',
 'moderate',1,
 '["Regular scalp hygiene","Avoid harsh hair products","Manage stress","Do not keep scalp very oily"]',
 '{"recommended":["balanced diet","adequate water"],"avoid":["excess sugar","excess fried food"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Vitamin D Deficiency Pattern','विटामिन डी की कमी','व्हिटॅमिन डी ची कमतरता','nutritional',
 NULL,NULL,NULL,
 'A nutritional deficiency that may present with bone pain, weakness, and low immunity.',
 '["Fatigue","Bone pain","Muscle weakness","Frequent infections (sometimes)"]',
 '["Low sunlight exposure","Poor dietary intake","Malabsorption","Obesity"]',
 '{"vata":"primary","kapha":"secondary","pitta":"secondary"}',
 '{"asthi":"primary","majja":"secondary"}',
 'chronic',0,
 '["Safe sunlight exposure","Balanced diet","Testing if symptomatic","Supplementation as prescribed"]',
 '{"recommended":["foods rich in vitamin D/calcium","adequate protein"],"avoid":["self-medication overdoses"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Seasonal Flu-like Viral Fever','वायरल बुखार (फ्लू जैसा)','व्हायरल ताप (फ्लू सारखा)','infectious',
 NULL,NULL,NULL,
 'An acute viral illness with fever, body ache, and respiratory symptoms.',
 '["Fever","Body ache","Chills","Sore throat","Cough","Fatigue"]',
 '["Viral infection","Close contact","Crowded exposure","Low sleep"]',
 '{"vata":"secondary","pitta":"primary","kapha":"secondary"}',
 '{"rasa":"primary"}',
 'moderate',0,
 '["Hand hygiene","Rest","Hydration","Avoid close contact when ill","Seek care if severe symptoms"]',
 '{"recommended":["warm fluids","light meals","soups"],"avoid":["alcohol","very heavy meals"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Constipation (Chronic Pattern)','कब्ज (दीर्घकालिक)','बद्धकोष्ठता (दीर्घकालीन)','digestive',
 NULL,NULL,NULL,
 'A persistent pattern of hard stools, infrequent bowel movements, or straining.',
 '["Hard stools","Infrequent stools","Straining","Bloating","Incomplete evacuation"]',
 '["Low fiber diet","Low water intake","Sedentary lifestyle","Stress","Irregular meal timings"]',
 '{"vata":"primary","kapha":"secondary","pitta":"secondary"}',
 '{"purishavaha_srotas":"primary","rasa":"secondary"}',
 'chronic',1,
 '["Increase fiber","Increase water","Daily walking","Regular bowel routine","Limit ultra-processed food"]',
 '{"recommended":["fiber-rich foods","warm water","cooked vegetables"],"avoid":["very dry foods","low-fiber diet"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Back Pain (Mechanical/Strain Pattern)','कमर दर्द','पाठदुखी / कंबरदुखी','musculoskeletal',
 NULL,NULL,NULL,
 'A common musculoskeletal condition often due to poor posture, strain, or degenerative changes.',
 '["Lower back pain","Stiffness","Pain on movement","Muscle spasm","Reduced flexibility"]',
 '["Poor posture","Prolonged sitting","Heavy lifting","Weak core muscles","Degeneration"]',
 '{"vata":"primary","kapha":"secondary","pitta":"secondary"}',
 '{"mamsa":"primary","asthi":"secondary"}',
 'moderate',1,
 '["Posture correction","Regular stretching","Core strengthening","Avoid sudden heavy lifting","Ergonomic seating"]',
 '{"recommended":["adequate protein","hydration"],"avoid":["prolonged sitting without breaks"]}',
 CURRENT_TIMESTAMP);

INSERT INTO diseases
(name_en,name_hi,name_mr,category,ayurvedic_name,unani_name,siddha_name,description,
 symptoms,causes,dosha_involvement,dhatu_involvement,severity_level,is_lifestyle_related,
 prevention_tips,dietary_recommendations,updated_at)
VALUES
('Headache / Tension Headache','तनाव सिरदर्द','ताणतणावजन्य डोकेदुखी','neurology',
 NULL,NULL,NULL,
 'A common headache pattern associated with stress, posture strain, and sleep disturbance.',
 '["Dull head pain","Tight band-like sensation","Neck/shoulder tightness","Irritability","Poor concentration"]',
 '["Stress","Poor sleep","Dehydration","Screen strain","Neck posture issues"]',
 '{"vata":"primary","pitta":"secondary","kapha":"secondary"}',
 '{"manovaha_srotas":"secondary","majja":"secondary"}',
 'moderate',1,
 '["Hydration","Regular sleep","Screen breaks","Neck stretches","Stress management"]',
 '{"recommended":["water","light meals"],"avoid":["skipping meals","excess caffeine"]}',
 CURRENT_TIMESTAMP);

COMMIT;

