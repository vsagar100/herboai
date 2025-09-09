import os
class Config:
    """Application configuration"""
    
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/ayush.db')
    
    # AI Models
    SPACY_MODELS = {
        'en': 'en_core_web_sm',
        'hi': 'xx_ent_wiki_sm',
        'mr': 'xx_ent_wiki_sm'
    }
    
    TRANSFORMER_MODEL = 'microsoft/DialoGPT-small'
    
    # API Settings
    MAX_QUERY_LENGTH = 500
    MAX_RESULTS = 5
    SESSION_TIMEOUT = 7200  # 2 hours
    
    # Languages
    SUPPORTED_LANGUAGES = ['en', 'hi', 'mr']
    DEFAULT_LANGUAGE = 'en'
