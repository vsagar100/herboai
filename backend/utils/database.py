import logging
import json
import os
from typing import List, Dict, Optional
from sqlalchemy import text

logger = logging.getLogger(__name__)

def init_database(db, app):
    """Initialize database with tables and initial data"""
    try:
        with app.app_context():
            # Create all tables
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Load initial data if tables are empty
            from app import Plant
            if Plant.query.count() == 0:
                load_initial_plants(db)
            
            return True
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        return False

def load_initial_plants(db):
    """Load initial plant data"""
    try:
        from app import Plant
        
        initial_plants = [
            {
                'name': 'Turmeric',
                'scientific_name': 'Curcuma longa',
                'ayush_system': 'Ayurveda',
                'category': 'Anti-inflammatory',
                'uses': ['Joint pain', 'Digestive issues', 'Skin conditions', 'Wound healing'],
                'description': 'A powerful anti-inflammatory herb used in traditional medicine for thousands of years. Known for its active compound curcumin.',
                'preparation': 'Can be used as powder mixed with warm milk, made into paste for external use, or taken as decoction. Typical dose: 1-3g daily.',
                'contraindications': 'Avoid in gallstone patients. May increase bleeding risk with anticoagulants. Reduce dose if stomach upset occurs.',
                'properties': {
                    'taste': 'bitter, pungent',
                    'potency': 'hot',
                    'dosha': 'balances all three doshas',
                    'active_compounds': 'curcumin, turmerone'
                }
            },
            {
                'name': 'Neem',
                'scientific_name': 'Azadirachta indica',
                'ayush_system': 'Ayurveda',
                'category': 'Antibacterial',
                'uses': ['Skin infections', 'Dental health', 'Blood purification', 'Diabetes', 'Fever'],
                'description': 'Known as the village pharmacy, neem has potent antibacterial, antifungal, and antiviral properties.',
                'preparation': 'Leaves can be chewed (2-4 fresh leaves daily), made into paste for skin application, or used as decoction.',
                'contraindications': 'Avoid during pregnancy and breastfeeding. May lower blood sugar - monitor if diabetic.',
                'properties': {
                    'taste': 'bitter',
                    'potency': 'cold',
                    'dosha': 'pacifies pitta and kapha',
                    'active_compounds': 'azadirachtin, nimbin'
                }
            },
            {
                'name': 'Ashwagandha',
                'scientific_name': 'Withania somnifera',
                'ayush_system': 'Ayurveda',
                'category': 'Adaptogen',
                'uses': ['Stress relief', 'Energy boost', 'Sleep improvement', 'Immunity', 'Anxiety'],
                'description': 'A powerful adaptogenic herb that helps the body manage stress and anxiety while boosting energy and immunity.',
                'preparation': 'Root powder: 1-6g daily with warm milk or water. Best taken at bedtime for sleep or morning for energy.',
                'contraindications': 'Avoid during pregnancy. May interact with thyroid medications. Start with low doses.',
                'properties': {
                    'taste': 'bitter, sweet',
                    'potency': 'hot',
                    'dosha': 'balances vata and kapha',
                    'active_compounds': 'withanolides'
                }
            },
            {
                'name': 'Tulsi',
                'scientific_name': 'Ocimum sanctum',
                'ayush_system': 'Ayurveda',
                'category': 'Respiratory',
                'uses': ['Cough', 'Cold', 'Bronchitis', 'Stress', 'Immunity'],
                'description': 'Sacred basil is revered for its respiratory benefits and stress-relieving properties.',
                'preparation': 'Fresh leaves can be chewed (5-10 leaves daily) or made into tea. Dried powder: 1-3g daily.',
                'contraindications': 'Generally safe. May lower blood sugar slightly.',
                'properties': {
                    'taste': 'pungent, bitter',
                    'potency': 'hot',
                    'dosha': 'balances kapha and vata',
                    'active_compounds': 'eugenol, ursolic acid'
                }
            },
            {
                'name': 'Amla',
                'scientific_name': 'Emblica officinalis',
                'ayush_system': 'Ayurveda',
                'category': 'Antioxidant',
                'uses': ['Immunity', 'Hair health', 'Digestion', 'Diabetes', 'Heart health'],
                'description': 'Indian gooseberry is one of the richest sources of Vitamin C and powerful antioxidants.',
                'preparation': 'Fresh fruit juice: 20-30ml daily. Powder: 3-6g daily with water or honey.',
                'contraindications': 'Generally safe. May enhance iron absorption.',
                'properties': {
                    'taste': 'sour, sweet, bitter, pungent, astringent',
                    'potency': 'cold',
                    'dosha': 'balances all three doshas',
                    'active_compounds': 'vitamin C, tannins'
                }
            },
            {
                'name': 'Ginger',
                'scientific_name': 'Zingiber officinale',
                'ayush_system': 'Ayurveda',
                'category': 'Digestive',
                'uses': ['Nausea', 'Indigestion', 'Cold', 'Arthritis', 'Motion sickness'],
                'description': 'A warming spice excellent for digestion, nausea, and respiratory conditions.',
                'preparation': 'Fresh ginger tea: 1-2g in hot water. Powder: 250-1000mg daily.',
                'contraindications': 'Avoid large amounts if taking blood thinners. May increase heart rate.',
                'properties': {
                    'taste': 'pungent',
                    'potency': 'hot',
                    'dosha': 'pacifies vata and kapha',
                    'active_compounds': 'gingerol, shogaol'
                }
            }
        ]
        
        for plant_data in initial_plants:
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
        logger.info(f"Loaded {len(initial_plants)} initial plants")
        
    except Exception as e:
        logger.error(f"Error loading initial plants: {str(e)}")
        db.session.rollback()

def backup_database(db, backup_path: str) -> bool:
    """Create database backup"""
    try:
        # For SQLite, simply copy the database file
        import shutil
        db_path = db.engine.url.database
        
        if os.path.exists(db_path):
            shutil.copy2(db_path, backup_path)
            logger.info(f"Database backed up to {backup_path}")
            return True
        
        return False
        
    except Exception as e:
        logger.error(f"Error backing up database: {str(e)}")
        return False

def get_database_stats(db) -> Dict:
    """Get database statistics"""
    try:
        from app import Plant, Remedy, ChatHistory
        
        stats = {
            'total_plants': Plant.query.count(),
            'total_remedies': Remedy.query.count(),
            'total_chats': ChatHistory.query.count(),
            'plants_by_system': {},
            'plants_by_category': {}
        }
        
        # Plants by AYUSH system
        systems = db.session.query(Plant.ayush_system, db.func.count(Plant.id)).group_by(Plant.ayush_system).all()
        for system, count in systems:
            stats['plants_by_system'][system] = count
        
        # Plants by category
        categories = db.session.query(Plant.category, db.func.count(Plant.id)).group_by(Plant.category).all()
        for category, count in categories:
            if category:
                stats['plants_by_category'][category] = count
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting database stats: {str(e)}")
        return {}

def search_plants_by_text(db, search_term: str, limit: int = 20) -> List:
    """Search plants using text-based search"""
    try:
        from app import Plant
        
        search_pattern = f"%{search_term}%"
        
        plants = Plant.query.filter(
            db.or_(
                Plant.name.ilike(search_pattern),
                Plant.scientific_name.ilike(search_pattern),
                Plant.description.ilike(search_pattern),
                Plant.uses.ilike(search_pattern),
                Plant.category.ilike(search_pattern)
            )
        ).limit(limit).all()
        
        return plants
        
    except Exception as e:
        logger.error(f"Error searching plants: {str(e)}")
        return []

def validate_plant_data(plant_data: Dict) -> tuple[bool, List[str]]:
    """Validate plant data before insertion"""
    errors = []
    
    # Required fields
    required_fields = ['name', 'scientific_name', 'ayush_system']
    for field in required_fields:
        if not plant_data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate AYUSH system
    valid_systems = ['Ayurveda', 'Siddha', 'Unani', 'Homeopathy', 'Yoga', 'Naturopathy']
    if plant_data.get('ayush_system') not in valid_systems:
        errors.append(f"Invalid AYUSH system. Must be one of: {', '.join(valid_systems)}")
    
    # Validate uses format
    if plant_data.get('uses'):
        if not isinstance(plant_data['uses'], (list, str)):
            errors.append("Uses must be a list or string")
    
    # Validate properties format
    if plant_data.get('properties'):
        if not isinstance(plant_data['properties'], (dict, str)):
            errors.append("Properties must be a dictionary or JSON string")
    
    return len(errors) == 0, errors

def clean_database(db) -> Dict:
    """Clean up database - remove duplicates, orphaned records"""
    try:
        from app import Plant, Remedy, ChatHistory
        
        results = {
            'duplicates_removed': 0,
            'orphaned_removed': 0,
            'errors': []
        }
        
        # Remove duplicate plants (same scientific name)
        duplicates = db.session.query(Plant.scientific_name).group_by(Plant.scientific_name).having(db.func.count() > 1).all()
        
        for (scientific_name,) in duplicates:
            plants = Plant.query.filter_by(scientific_name=scientific_name).order_by(Plant.id).all()
            # Keep the first one, remove others
            for plant in plants[1:]:
                db.session.delete(plant)
                results['duplicates_removed'] += 1
        
        # Remove old chat history (keep only last 1000 entries)
        total_chats = ChatHistory.query.count()
        if total_chats > 1000:
            old_chats = ChatHistory.query.order_by(ChatHistory.timestamp).limit(total_chats - 1000).all()
            for chat in old_chats:
                db.session.delete(chat)
                results['orphaned_removed'] += 1
        
        db.session.commit()
        logger.info(f"Database cleanup completed: {results}")
        
        return results
        
    except Exception as e:
        logger.error(f"Error cleaning database: {str(e)}")
        db.session.rollback()
        return {'error': str(e)}

def export_plants_to_json(db, file_path: str) -> bool:
    """Export all plants to JSON file"""
    try:
        from app import Plant
        
        plants = Plant.query.all()
        plants_data = []
        
        for plant in plants:
            plant_dict = plant.to_dict()
            plants_data.append(plant_dict)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(plants_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Exported {len(plants_data)} plants to {file_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error exporting plants: {str(e)}")
        return False

def import_plants_from_json(db, file_path: str) -> Dict:
    """Import plants from JSON file"""
    try:
        from app import Plant
        
        with open(file_path, 'r', encoding='utf-8') as f:
            plants_data = json.load(f)
        
        imported = 0
        errors = []
        
        for plant_data in plants_data:
            try:
                # Validate data
                is_valid, validation_errors = validate_plant_data(plant_data)
                if not is_valid:
                    errors.extend(validation_errors)
                    continue
                
                # Check if plant already exists
                existing = Plant.query.filter_by(scientific_name=plant_data['scientific_name']).first()
                if existing:
                    continue
                
                # Create new plant
                plant = Plant(
                    name=plant_data['name'],
                    scientific_name=plant_data['scientific_name'],
                    ayush_system=plant_data['ayush_system'],
                    category=plant_data.get('category'),
                    uses=json.dumps(plant_data.get('uses', [])),
                    description=plant_data.get('description'),
                    preparation=plant_data.get('preparation'),
                    contraindications=plant_data.get('contraindications'),
                    properties=json.dumps(plant_data.get('properties', {}))
                )
                
                db.session.add(plant)
                imported += 1
                
            except Exception as e:
                errors.append(f"Error importing {plant_data.get('name', 'unknown')}: {str(e)}")
        
        db.session.commit()
        
        return {
            'imported': imported,
            'errors': errors,
            'total_processed': len(plants_data)
        }
        
    except Exception as e:
        logger.error(f"Error importing plants: {str(e)}")
        db.session.rollback()
        return {'error': str(e)}

def optimize_database(db) -> bool:
    """Optimize database performance"""
    try:
        # For SQLite, run VACUUM and ANALYZE
        db.session.execute(text('VACUUM'))
        db.session.execute(text('ANALYZE'))
        db.session.commit()
        
        logger.info("Database optimization completed")
        return True
        
    except Exception as e:
        logger.error(f"Error optimizing database: {str(e)}")
        return False