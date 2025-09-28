from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import json
import re
import logging
from werkzeug.security import generate_password_hash, check_password_hash

# Import custom modules
from services.nlp_service import NLPService
from services.vector_service import VectorService
from services.rag_service import RAGService
from services.embedding_service import EmbeddingService
from utils.multilingual import MultilingualProcessor
from config.settings import Config

# Initialize Flask app
app = Flask(__name__, static_folder="static", static_url_path="/static")
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
CORS(app)

UPLOAD_DIR = os.path.join(app.root_path, "static", "plant_images")
os.makedirs(UPLOAD_DIR, exist_ok=True)


multilingual_processor = MultilingualProcessor()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

_slug_re = re.compile(r"[^a-z0-9]+")
def plant_slug(name: str) -> str:
    return _slug_re.sub("-", (name or "").lower()).strip("-")

# Database Models
class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100), unique=True, nullable=False)
    ayush_system = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50))
    uses = db.Column(db.Text)  # JSON string of uses
    preparation = db.Column(db.Text)
    contraindications = db.Column(db.Text)
    image_path = db.Column(db.String(255))
    description = db.Column(db.Text)
    properties = db.Column(db.Text)  # JSON string of properties
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'scientific_name': self.scientific_name,
            'ayush_system': self.ayush_system,
            'category': self.category,
            'uses': json.loads(self.uses) if self.uses else [],
            'preparation': self.preparation,
            'contraindications': self.contraindications,
            'image_path': self.image_path,
            'description': self.description,
            'properties': json.loads(self.properties) if self.properties else {},
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class Remedy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String(100), nullable=False)
    diagnosis_pattern = db.Column(db.Text)
    plant_ids = db.Column(db.Text)  # JSON string of plant IDs
    dosage = db.Column(db.Text)
    lifestyle_recommendations = db.Column(db.Text)
    preparation_method = db.Column(db.Text)
    ayush_system = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'symptom': self.symptom,
            'diagnosis_pattern': self.diagnosis_pattern,
            'plant_ids': json.loads(self.plant_ids) if self.plant_ids else [],
            'dosage': self.dosage,
            'lifestyle_recommendations': self.lifestyle_recommendations,
            'preparation_method': self.preparation_method,
            'ayush_system': self.ayush_system,
            'created_at': self.created_at.isoformat()
        }

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False)
    user_query = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(10), default='en')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize services
nlp_service = NLPService()
vector_service = VectorService()
embedding_service = EmbeddingService()
rag_service = RAGService(Plant)

# API Routes

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

@app.route('/api/plants', methods=['GET'])
def get_plants():
    """Get all plants with optional filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        ayush_system = request.args.get('ayush_system', '')
        
        query = Plant.query
        
        if search:
            query = query.filter(
                db.or_(
                    Plant.name.ilike(f'%{search}%'),
                    Plant.scientific_name.ilike(f'%{search}%'),
                    Plant.description.ilike(f'%{search}%')
                )
            )
        
        if category:
            query = query.filter(Plant.category == category)
        
        if ayush_system:
            query = query.filter(Plant.ayush_system == ayush_system)
        
        plants = query.paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        return jsonify({
            'plants': [plant.to_dict() for plant in plants.items],
            'total': plants.total,
            'pages': plants.pages,
            'current_page': page,
            'per_page': per_page
        })
    
    except Exception as e:
        logger.error(f"Error fetching plants: {str(e)}")
        return jsonify({'error': 'Failed to fetch plants'}), 500

@app.route('/api/plants/<int:plant_id>', methods=['GET'])
def get_plant(plant_id):
    """Get a specific plant by ID"""
    try:
        plant = Plant.query.get_or_404(plant_id)
        return jsonify(plant.to_dict())
    except Exception as e:
        logger.error(f"Error fetching plant {plant_id}: {str(e)}")
        return jsonify({'error': 'Plant not found'}), 404

@app.route('/api/plants', methods=['POST'])
def add_plant():
    """Add a new plant (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'scientific_name', 'ayush_system']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        plant = Plant(
            name=data['name'],
            scientific_name=data['scientific_name'],
            ayush_system=data['ayush_system'],
            category=data.get('category', ''),
            uses=json.dumps(data.get('uses', [])),
            preparation=data.get('preparation', ''),
            contraindications=data.get('contraindications', ''),
            image_path=data.get('image_path', ''),
            description=data.get('description', ''),
            properties=json.dumps(data.get('properties', {}))
        )
        
        db.session.add(plant)
        db.session.commit()
        
        # Generate embeddings for the new plant
        embedding_service.generate_plant_embeddings(plant)
        
        logger.info(f"Added new plant: {plant.name}")
        return jsonify(plant.to_dict()), 201
        
    except Exception as e:
        logger.error(f"Error adding plant: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to add plant'}), 500

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        payload = request.get_json(force=True) or {}
        query = payload.get('query', '') or ''
        language = payload.get('language', 'en')
        session_id = payload.get('session_id', 'web')

        # 1) Preprocess
        processed = nlp_service.process_query(query, language=language)

        # 2) Retrieve (models expected)
        relevant_models = rag_service.get_relevant_plants(processed, limit=5)

        # 3) Generate response (accepts models or dicts, but we pass models)
        response_text = rag_service.generate_response(query, relevant_models)

        # 4) Prepare JSON-safe plants
        relevant_out = []
        for p in relevant_models:
            if hasattr(p, "to_dict"):
                relevant_out.append(p.to_dict())
            elif isinstance(p, dict):
                relevant_out.append(p)  # already dict
            else:
                # ultra-safe fallback
                relevant_out.append({
                    "id": getattr(p, "id", None),
                    "name": getattr(p, "name", ""),
                    "scientific_name": getattr(p, "scientific_name", ""),
                    "ayush_system": getattr(p, "ayush_system", ""),
                    "category": getattr(p, "category", ""),
                    "uses": getattr(p, "uses", []),
                    "description": getattr(p, "description", ""),
                    "preparation": getattr(p, "preparation", ""),
                    "contraindications": getattr(p, "contraindications", "")
                })

        # (Optional) log chat_history here safely

        return jsonify({
            "response": response_text,
            "relevant_plants": relevant_out,
            "session_id": session_id
        }), 200

    except Exception as e:
        app.logger.error(f"Error processing chat query: {e}")
        return jsonify({"error": "Chat processing failed"}), 500


@app.route('/api/search', methods=['GET'])
def search_plants():
    """Advanced plant search using semantic search"""
    try:
        query = request.args.get('query', '')
        language = request.args.get('language', 'en')
        limit = request.args.get('limit', 10, type=int)
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        # Translate query if needed
        if language != 'en':
            translated_query = multilingual_processor.translate_to_english(query, language)
        else:
            translated_query = query
        
        # Use vector search for semantic matching
        results = vector_service.semantic_search(translated_query, limit=limit)
        
        return jsonify({
            'results': results,
            'query': query,
            'translated_query': translated_query if language != 'en' else None
        })
        
    except Exception as e:
        logger.error(f"Error in semantic search: {str(e)}")
        return jsonify({'error': 'Search failed'}), 500

@app.route('/api/remedies', methods=['GET'])
def get_remedies():
    """Get remedies by symptom"""
    try:
        symptom = request.args.get('symptom', '')
        ayush_system = request.args.get('ayush_system', '')
        
        query = Remedy.query
        
        if symptom:
            query = query.filter(Remedy.symptom.ilike(f'%{symptom}%'))
        
        if ayush_system:
            query = query.filter(Remedy.ayush_system == ayush_system)
        
        remedies = query.all()
        
        return jsonify([remedy.to_dict() for remedy in remedies])
        
    except Exception as e:
        logger.error(f"Error fetching remedies: {str(e)}")
        return jsonify({'error': 'Failed to fetch remedies'}), 500


@app.post("/api/admin/plant/<int:plant_id>/image")
def upload_plant_image(plant_id):
    if "file" not in request.files:
        return jsonify({"error": "No file"}), 400
    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid extension"}), 400

    plant = Plant.query.get_or_404(plant_id)
    ext = file.filename.rsplit(".", 1)[1].lower()
    # filename: turmeric.jpg (slug of plant name)
    filename = secure_filename(f"{plant_slug(plant.name)}.{ext}")
    fs_path = os.path.join(UPLOAD_DIR, filename)
    # If replacing, optionally delete old file here
    file.save(fs_path)

    web_path = f"/static/plant_images/{filename}"
    plant.image_path = web_path
    plant.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({"ok": True, "image_path": web_path, "plant": plant.to_dict()}), 200

@app.route('/api/admin/analytics', methods=['GET'])
def get_analytics():
    """Get system analytics (admin only)"""
    try:
        # Basic analytics
        total_plants = Plant.query.count()
        total_remedies = Remedy.query.count()
        total_chats = ChatHistory.query.count()
        
        # Recent activity
        recent_chats = ChatHistory.query.order_by(
            ChatHistory.timestamp.desc()
        ).limit(10).all()
        
        # Popular queries (simplified)
        popular_symptoms = db.session.query(
            Remedy.symptom, 
            db.func.count(Remedy.symptom).label('count')
        ).group_by(Remedy.symptom).order_by(db.desc('count')).limit(5).all()
        
        return jsonify({
            'total_plants': total_plants,
            'total_remedies': total_remedies,
            'total_chats': total_chats,
            'recent_chats': [
                {
                    'query': chat.user_query[:100] + '...' if len(chat.user_query) > 100 else chat.user_query,
                    'timestamp': chat.timestamp.isoformat(),
                    'language': chat.language
                }
                for chat in recent_chats
            ],
            'popular_symptoms': [
                {'symptom': symptom, 'count': count}
                for symptom, count in popular_symptoms
            ]
        })
        
    except Exception as e:
        logger.error(f"Error fetching analytics: {str(e)}")
        return jsonify({'error': 'Failed to fetch analytics'}), 500

@app.route('/api/admin/import', methods=['POST'])
def import_plants():
    """Import plants from uploaded data (admin only)"""
    try:
        data = request.get_json()
        plants_data = data.get('plants', [])
        
        imported_count = 0
        errors = []
        
        for plant_data in plants_data:
            try:
                # Check if plant already exists
                existing_plant = Plant.query.filter_by(
                    scientific_name=plant_data.get('scientific_name')
                ).first()
                
                if existing_plant:
                    continue
                
                plant = Plant(
                    name=plant_data.get('name'),
                    scientific_name=plant_data.get('scientific_name'),
                    ayush_system=plant_data.get('ayush_system', 'Ayurveda'),
                    category=plant_data.get('category', ''),
                    uses=json.dumps(plant_data.get('uses', [])),
                    preparation=plant_data.get('preparation', ''),
                    contraindications=plant_data.get('contraindications', ''),
                    description=plant_data.get('description', ''),
                    properties=json.dumps(plant_data.get('properties', {}))
                )
                
                db.session.add(plant)
                imported_count += 1
                
            except Exception as e:
                errors.append(f"Error importing {plant_data.get('name', 'unknown')}: {str(e)}")
        
        db.session.commit()
        
        return jsonify({
            'imported_count': imported_count,
            'errors': errors
        })
        
    except Exception as e:
        logger.error(f"Error importing plants: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Import failed'}), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Database initialization
# Database initialization - Updated for Flask 2.2+
def create_tables():
    """Create database tables and load initial data"""
    with app.app_context():
        db.create_all()
        
        # Load initial data if tables are empty
        if Plant.query.count() == 0:
            load_initial_data()

# Call the function directly instead of using decorator
def init_database():
    """Initialize database on startup"""
    create_tables()

def load_initial_data():
    """Load initial plant and remedy data"""
    try:
        # Sample plants data
        sample_plants = [
            {
                'name': 'Turmeric',
                'scientific_name': 'Curcuma longa',
                'ayush_system': 'Ayurveda',
                'category': 'Anti-inflammatory',
                'uses': ['Joint pain', 'Digestive issues', 'Skin conditions', 'Wound healing'],
                'description': 'A powerful anti-inflammatory herb used in traditional medicine for thousands of years.',
                'preparation': 'Can be used as powder, paste, or decoction. Mix 1 tsp with warm milk.',
                'contraindications': 'Avoid in gallstone patients. May increase bleeding risk.',
                'properties': {'taste': 'bitter, pungent', 'potency': 'hot', 'dosha': 'balances all doshas'}
            },
            {
                'name': 'Neem',
                'scientific_name': 'Azadirachta indica',
                'ayush_system': 'Ayurveda',
                'category': 'Antibacterial',
                'uses': ['Skin infections', 'Dental health', 'Blood purification', 'Diabetes'],
                'description': 'Known as the village pharmacy, neem has potent antibacterial and antifungal properties.',
                'preparation': 'Leaves can be chewed, made into paste, or used as decoction.',
                'contraindications': 'Avoid during pregnancy. May lower blood sugar.',
                'properties': {'taste': 'bitter', 'potency': 'cold', 'dosha': 'pacifies pitta and kapha'}
            }
        ]
        
        for plant_data in sample_plants:
            plant = Plant(
                name=plant_data['name'],
                scientific_name=plant_data['scientific_name'],
                ayush_system=plant_data['ayush_system'],
                category=plant_data['category'],
                uses=json.dumps(plant_data['uses']),
                description=plant_data['description'],
                preparation=plant_data['preparation'],
                contraindications=plant_data['contraindications'],
                properties=json.dumps(plant_data['properties'])
            )
            db.session.add(plant)
        
        db.session.commit()
        logger.info("Initial data loaded successfully")
        
    except Exception as e:
        logger.error(f"Error loading initial data: {str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    # Initialize database before running
    init_database()
    app.run(debug=True, host='0.0.0.0', port=5000)