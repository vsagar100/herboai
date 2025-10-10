# seeds.py
from database import Base, engine, SessionLocal
from models import Plant, Remedy, AdminUser, Image
from werkzeug.security import generate_password_hash
import json, os

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if not db.query(AdminUser).first():
        db.add(AdminUser(username="admin", password_hash=generate_password_hash("admin@123")))
        db.commit()

    if not db.query(Plant).first():
        tulsi = Plant(
            name="Tulsi",
            scientific_name="Ocimum sanctum",
            ayush_system="Ayurveda",
            category="Respiratory",
            synonyms="Holy Basil, तुलसी, तुळस",
            parts_used=json.dumps(["Leaves", "Stem"]),
            uses="Cough, cold, immunity support",
            phytochemicals="Eugenol, Ursolic acid",
            dosage="Infusion: 150 ml twice daily after meals",
            contraindications="Pregnancy: consult physician; possible interaction with blood thinners.",
            formulations="Kashaya (decoction), Tea",
            description="Aromatic shrub used widely in Ayurveda.",
            properties="Antitussive, immunomodulatory",
            languages_json=json.dumps({
                "hi": {
                    "name": "तुलसी",
                    "uses": "खांसी, जुकाम, रोग प्रतिरोधक शक्ति बढ़ाना",
                    "dosage": "काढ़ा: 150 ml दिन में दो बार भोजन के बाद",
                    "contraindications": "गर्भावस्था में चिकित्सक से सलाह लें; रक्त पतला करने वाली दवाओं से पारस्परिक प्रभाव।",
                    "description": "आयुर्वेद में व्यापक रूप से उपयोगी सुगंधित पौधा।",
                },
                "mr": {
                    "name": "तुळस",
                    "uses": "खोकला, सर्दी, प्रतिकारशक्ती सुधार",
                    "dosage": "काढा: 150 ml दिवसात दोनदा जेवणानंतर",
                    "contraindications": "गर्भधारणेत डॉक्टरांचा सल्ला घ्या; रक्त पातळ करणाऱ्या औषधांशी परस्पर क्रिया.",
                    "description": "आयुर्वेदात मोठ्या प्रमाणात वापरला जाणारा सुगंधी वनस्पती.",
                }
            })
        )
        db.add(tulsi); db.commit()

        db.add(Remedy(
            symptom="cough",
            diagnosis_pattern="dry cough, sore throat, khansi, खांसी, खोकला",
            plant_ids=str(tulsi.id),
            preparation="Boil 8–10 Tulsi leaves in 250 ml water for 7–8 minutes. Add ginger and honey (optional).",
            dosage="150 ml warm infusion, 2×/day after meals for 3–5 days.",
            lifestyle_recommendations="Warm fluids, avoid cold exposure, rest voice.",
            preparation_method="Decoction/tea",
            ayush_system="Ayurveda",
            side_effects="Generally safe in dietary amounts; excess may cause nausea.",
            contraindications="Pregnancy, anticoagulant therapy: consult physician.",
            languages_json=json.dumps({
                "hi": {
                    "symptom": "खांसी",
                    "preparation": "250 ml पानी में 8–10 तुलसी पत्ते 7–8 मिनट उबालें; अदरक/शहद (वैकल्पिक)।",
                },
                "mr": {
                    "symptom": "खोकला",
                    "preparation": "250 ml पाण्यात 8–10 तुळशीची पाने 7–8 मिनिटे उकळा; आलं/मध (ऐच्छिक).",
                }
            })
        ))
        db.commit()

    db.close()

if __name__ == "__main__":
    run()
