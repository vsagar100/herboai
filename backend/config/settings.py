import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'herboai-secret-key-change-in-production'
    
    # Database Configuration
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f'sqlite:///{os.path.join(basedir, "..", "herboai.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_timeout': 20,
        'pool_recycle': -1,
        'pool_pre_ping': True
    }
    
    # AI Model Configuration
    NLP_MODEL = os.environ.get('NLP_MODEL') or 'en_core_web_sm'
    EMBEDDING_MODEL = os.environ.get('EMBEDDING_MODEL') or 'all-MiniLM-L6-v2'
    VECTOR_STORE_TYPE = os.environ.get('VECTOR_STORE_TYPE') or 'chromadb'
    
    # Data Paths
    DATA_PATH = os.path.join(basedir, '..', 'data')
    MODELS_PATH = os.path.join(DATA_PATH, 'models')
    EMBEDDINGS_PATH = os.path.join(DATA_PATH, 'embeddings')
    IMAGES_PATH = os.path.join(basedir, '..', 'static', 'images')
    
    # API Configuration
    API_RATE_LIMIT = os.environ.get('API_RATE_LIMIT') or '100 per hour'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    
    # Cache Configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # Multilingual Support
    SUPPORTED_LANGUAGES = ['en', 'hi', 'mr']
    DEFAULT_LANGUAGE = 'en'
    
    # AYUSH Systems
    AYUSH_SYSTEMS = [
        'Ayurveda',
        'Yoga',
        'Unani',
        'Siddha',
        'Homeopathy',
        'Naturopathy'
    ]
    
    # Plant Categories
    PLANT_CATEGORIES = [
        'Anti-inflammatory',
        'Antibacterial',
        'Antiviral',
        'Antifungal',
        'Digestive',
        'Respiratory',
        'Cardiovascular',
        'Nervous System',
        'Immune System',
        'Skin & Hair',
        'Reproductive Health',
        'Adaptogen',
        'Detoxification',
        'Pain Relief',
        'Mental Health'
    ]
    
    # Logging Configuration
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.path.join(basedir, '..', 'logs', 'herboai.log')
    
    # Security Configuration
    SESSION_TIMEOUT = timedelta(hours=24)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD') or 'admin123'
    
    # Vector Database Configuration
    CHROMADB_PATH = os.path.join(DATA_PATH, 'chromadb')
    VECTOR_DIMENSIONS = 384  # For all-MiniLM-L6-v2
    
    # Search Configuration
    MAX_SEARCH_RESULTS = 20
    SEMANTIC_SEARCH_THRESHOLD = 0.7
    
    # Chat Configuration
    MAX_CHAT_HISTORY = 100
    RESPONSE_MAX_LENGTH = 1000
    
    @staticmethod
    def init_app(app):
        """Initialize application with this config"""
        # Create necessary directories
        os.makedirs(Config.DATA_PATH, exist_ok=True)
        os.makedirs(Config.MODELS_PATH, exist_ok=True)
        os.makedirs(Config.EMBEDDINGS_PATH, exist_ok=True)
        os.makedirs(Config.IMAGES_PATH, exist_ok=True)
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
        os.makedirs(Config.CHROMADB_PATH, exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    LOG_LEVEL = 'DEBUG'


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'WARNING'
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Use PostgreSQL in production
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://username:password@localhost/herboai'


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}