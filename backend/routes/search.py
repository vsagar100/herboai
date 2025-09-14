import json
import os
import re
from flask import Blueprint, request, jsonify
import spacy
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from datetime import datetime, timedelta
import uuid
import hashlib
import threading
from collections import defaultdict
from langdetect import detect, DetectorFactory
import unicodedata

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Local utils
from database.db_utils import fetch_all_herbs
from utils.translator import translate_text

# Main API Blueprint
search_bp = Blueprint("api", __name__)

def initialize_ai_system():
   """
   Initialize the AI system with all required components.
   This function must be called before the Flask app starts serving requests.
   
   Returns:
       bool: True if initialization successful, False otherwise
   """
   global ai_herbal_system, ai_session_manager
   
   try:
       print("Initializing Advanced HerboAI System...")
       
       # Step 1: Load herb data from database
       print("Loading herbs data from database...")
       herbs_data = fetch_all_herbs()
       
       if not herbs_data:
           print("Error: No herbs data found in database!")
           return False
           
       print(f"Loaded {len(herbs_data)} herbs from database")
       
       # Step 2: Initialize AI system components
       print("Initializing AI processing system...")
       ai_herbal_system = IntelligentHerbalAI(herbs_data)
       print("AI herbal system initialized")
       
       # Step 3: Initialize session manager
       print("Initializing session management...")
       ai_session_manager = AISessionManager()
       print("Session manager initialized")
       
       # Step 4: Verify system components
       print("Verifying system components...")
       
       # Check if AI system has required components
       if not hasattr(ai_herbal_system, 'lang_processor'):
           raise Exception("Language processor not initialized")
           
       if not hasattr(ai_herbal_system, 'herb_profiles'):
           raise Exception("Herb profiles not created")
           
       if len(ai_herbal_system.herb_profiles) == 0:
           raise Exception("No herb profiles found")
           
       # Check if language models are loaded
       if not ai_herbal_system.lang_processor.nlp_models:
           raise Exception("NLP models not loaded")
           
       print("All system components verified")
       
       # Step 5: Test system with a simple query
       print("Running system test...")
       test_result = ai_herbal_system.process_query("test query")
       
       if not test_result or 'response_text' not in test_result:
           raise Exception("System test failed - no response generated")
           
       print("System test passed")
       
       print("HerboAI Advanced System Ready!")
       print(f"   Knowledge base: {len(herbs_data)} herbs")
       print(f"   Languages: {list(ai_herbal_system.lang_processor.nlp_models.keys())}")
       print(f"   Intent patterns: {len(ai_herbal_system.intent_patterns)}")
       print(f"   Symptom mappings: {len(ai_herbal_system.symptom_herb_mapping)}")
       
       return True
       
   except ImportError as e:
       print(f"Missing required packages: {e}")
       print("Please install: pip install spacy transformers langdetect")
       return False
       
   except OSError as e:
       print(f"Model loading error: {e}")
       print("Please download models:")
       print("  python -m spacy download en_core_web_sm")
       print("  python -m spacy download xx_ent_wiki_sm")
       return False
       
   except Exception as e:
       print(f"Failed to initialize AI system: {str(e)}")
       import traceback
       traceback.print_exc()
       return False

# Also add these global variables at the top of your file
ai_herbal_system = None
ai_session_manager = None

class AISessionManager:
    """
    Enhanced session management for AI conversations.
    Maintains user context, conversation history, and preferences.
    """
    
    def __init__(self):
        self.sessions = {}  # user_id -> session_data
        self.session_lock = threading.RLock()  # Thread-safe operations
        self.cleanup_interval = 3600  # 1 hour cleanup cycle
        self.max_session_age = 7200  # 2 hours session timeout
        self.last_cleanup = datetime.now()
        self.max_conversations_per_session = 20  # Limit memory usage
    
    def _generate_user_id(self, request_info):
        """
        Generate consistent user ID from request information.
        Creates anonymous but consistent identifier for users.
        
        Args:
            request_info (dict): Contains 'remote_addr' and 'user_agent'
        
        Returns:
            str: Hashed user identifier (16 chars)
        """
        ip = request_info.get('remote_addr', 'unknown')
        user_agent = request_info.get('user_agent', 'unknown')
        
        # Create hash for privacy - same user gets same ID
        user_string = f"{ip}:{user_agent}"
        return hashlib.md5(user_string.encode()).hexdigest()[:16]
    
    def _cleanup_old_sessions(self):
        """
        Remove expired sessions to prevent memory leaks.
        Runs periodically based on cleanup_interval.
        """
        now = datetime.now()
        if (now - self.last_cleanup).seconds < self.cleanup_interval:
            return
        
        with self.session_lock:
            expired_sessions = []
            for user_id, session in self.sessions.items():
                if (now - session['last_activity']).seconds > self.max_session_age:
                    expired_sessions.append(user_id)
            
            for user_id in expired_sessions:
                del self.sessions[user_id]
            
            self.last_cleanup = now
            if expired_sessions:
                print(f"Cleaned up {len(expired_sessions)} expired sessions")
    
    def get_or_create_session(self, request_info):
        """
        Get existing session or create new one for user.
        
        Args:
            request_info (dict): Request information for user identification
            
        Returns:
            dict: Session data for the user
        """
        user_id = self._generate_user_id(request_info)
        
        with self.session_lock:
            self._cleanup_old_sessions()
            
            # Create new session if doesn't exist
            if user_id not in self.sessions:
                self.sessions[user_id] = {
                    'user_id': user_id,
                    'created_at': datetime.now(),
                    'last_activity': datetime.now(),
                    'conversation_history': [],
                    'user_preferences': {
                        'preferred_language': 'en',
                        'health_interests': [],  # Track user's health topics
                        'frequent_queries': [],  # Common query patterns
                        'preferred_herbs': []    # Herbs user asks about often
                    },
                    'context': {
                        'current_symptoms': [],      # Recently mentioned symptoms
                        'mentioned_herbs': [],       # Recently discussed herbs
                        'health_goals': [],         # User's health objectives
                        'conversation_topic': None, # Current conversation focus
                        'last_intent': None        # Previous query intent
                    },
                    'statistics': {
                        'total_queries': 0,
                        'queries_by_language': defaultdict(int),
                        'intents_used': defaultdict(int),
                        'herbs_requested': defaultdict(int)
                    }
                }
            
            # Update last activity
            self.sessions[user_id]['last_activity'] = datetime.now()
            return self.sessions[user_id]
    
    def update_session_context(self, user_id, query, response_data):
        """
        Update session with new conversation context.
        This is key for maintaining conversation continuity.
        
        Args:
            user_id (str): User identifier
            query (str): User's original query
            response_data (dict): AI response metadata
        """
        if user_id not in self.sessions:
            return
        
        session = self.sessions[user_id]
        
        with self.session_lock:
            # Add to conversation history
            conversation_entry = {
                'query': query,
                'timestamp': datetime.now(),
                'intent': response_data.get('intent', ''),
                'language': response_data.get('language', 'en'),
                'herbs_mentioned': [
                    herb.get('name', '') 
                    for herb in response_data.get('herbs_data', [])
                ],
                'entities': response_data.get('entities', {}),
                'confidence': response_data.get('confidence', 0.0)
            }
            
            session['conversation_history'].append(conversation_entry)
            
            # Limit conversation history to prevent memory bloat
            if len(session['conversation_history']) > self.max_conversations_per_session:
                session['conversation_history'] = session['conversation_history'][-self.max_conversations_per_session:]
            
            # Update user preferences
            self._update_user_preferences(session, response_data)
            
            # Update conversation context
            self._update_conversation_context(session, response_data)
            
            # Update statistics
            self._update_session_statistics(session, query, response_data)
    
    def _update_user_preferences(self, session, response_data):
        """Update user preferences based on interaction"""
        prefs = session['user_preferences']
        
        # Update preferred language
        language = response_data.get('language', 'en')
        prefs['preferred_language'] = language
        
        # Track health interests from entities
        entities = response_data.get('entities', {})
        if entities.get('symptoms'):
            prefs['health_interests'].extend(entities['symptoms'])
            # Keep only unique recent interests (last 10)
            prefs['health_interests'] = list(set(prefs['health_interests']))[-10:]
        
        # Track frequently mentioned herbs
        herbs_data = response_data.get('herbs_data', [])
        for herb in herbs_data:
            herb_name = herb.get('name', '')
            if herb_name and herb_name not in prefs['preferred_herbs']:
                prefs['preferred_herbs'].append(herb_name)
        
        # Keep only recent preferred herbs (last 5)
        prefs['preferred_herbs'] = prefs['preferred_herbs'][-5:]
    
    def _update_conversation_context(self, session, response_data):
        """Update conversation context for continuity"""
        context = session['context']
        
        # Update current symptoms
        entities = response_data.get('entities', {})
        if entities.get('symptoms'):
            context['current_symptoms'].extend(entities['symptoms'])
            # Keep unique recent symptoms
            context['current_symptoms'] = list(set(context['current_symptoms']))[-5:]
        
        # Update mentioned herbs
        herbs_data = response_data.get('herbs_data', [])
        herb_names = [herb.get('name', '') for herb in herbs_data]
        context['mentioned_herbs'].extend(herb_names)
        context['mentioned_herbs'] = list(set(context['mentioned_herbs']))[-5:]
        
        # Set conversation topic based on intent
        intent = response_data.get('intent', '')
        if intent:
            context['conversation_topic'] = intent
            context['last_intent'] = intent
    
    def _update_session_statistics(self, session, query, response_data):
        """Update session statistics for analytics"""
        stats = session['statistics']
        
        stats['total_queries'] += 1
        
        # Track language usage
        language = response_data.get('language', 'en')
        stats['queries_by_language'][language] += 1
        
        # Track intent usage
        intent = response_data.get('intent', 'unknown')
        stats['intents_used'][intent] += 1
        
        # Track herb requests
        herbs_data = response_data.get('herbs_data', [])
        for herb in herbs_data:
            herb_name = herb.get('name', '')
            if herb_name:
                stats['herbs_requested'][herb_name] += 1
    
    def get_user_context(self, request_info):
        """
        Get contextual information about user for personalized responses.
        
        Args:
            request_info (dict): Request information
            
        Returns:
            dict: User context for AI processing
        """
        session = self.get_or_create_session(request_info)
        
        # Get recent conversation patterns
        recent_queries = session['conversation_history'][-5:] if session['conversation_history'] else []
        
        return {
            'user_id': session['user_id'],
            'session_age_minutes': (datetime.now() - session['created_at']).seconds // 60,
            'total_queries': session['statistics']['total_queries'],
            'preferred_language': session['user_preferences']['preferred_language'],
            'recent_queries': [q['query'] for q in recent_queries],
            'recent_intents': [q['intent'] for q in recent_queries],
            'current_symptoms': session['context']['current_symptoms'],
            'mentioned_herbs': session['context']['mentioned_herbs'],
            'conversation_topic': session['context']['conversation_topic'],
            'last_intent': session['context']['last_intent'],
            'health_interests': session['user_preferences']['health_interests'],
            'language_preference': session['user_preferences']['preferred_language']
        }
    
    def get_session_statistics(self):
        """
        Get overall system statistics.
        
        Returns:
            dict: System-wide session statistics
        """
        with self.session_lock:
            if not self.sessions:
                return {
                    'active_sessions': 0,
                    'total_conversations': 0,
                    'languages_used': [],
                    'popular_intents': {},
                    'popular_herbs': {}
                }
            
            total_conversations = sum(
                len(s['conversation_history']) 
                for s in self.sessions.values()
            )
            
            # Aggregate language usage
            all_languages = set()
            for session in self.sessions.values():
                all_languages.update(session['statistics']['queries_by_language'].keys())
            
            # Aggregate popular intents
            intent_counts = defaultdict(int)
            herb_counts = defaultdict(int)
            
            for session in self.sessions.values():
                for intent, count in session['statistics']['intents_used'].items():
                    intent_counts[intent] += count
                for herb, count in session['statistics']['herbs_requested'].items():
                    herb_counts[herb] += count
            
            return {
                'active_sessions': len(self.sessions),
                'total_conversations': total_conversations,
                'languages_used': list(all_languages),
                'popular_intents': dict(sorted(intent_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
                'popular_herbs': dict(sorted(herb_counts.items(), key=lambda x: x[1], reverse=True)[:5]),
                'average_queries_per_session': total_conversations / len(self.sessions) if self.sessions else 0
            }
    
    def clear_user_session(self, request_info):
        """
        Clear a specific user's session (for privacy/reset).
        
        Args:
            request_info (dict): Request information to identify user
            
        Returns:
            bool: True if session was found and cleared
        """
        user_id = self._generate_user_id(request_info)
        
        with self.session_lock:
            if user_id in self.sessions:
                del self.sessions[user_id]
                return True
            return False

class AdvancedLanguageProcessor:
    """Enhanced language processing with spaCy and transformers"""
    
    def __init__(self):
        self.nlp_models = {}
        self.intent_classifier = None
        self.response_generator = None
        self.load_models()
    
    def load_models(self):
        """Load all required models for offline operation"""
        print("Loading language models...")
        
        try:
            # Load spaCy models for different languages
            model_configs = {
                'en': 'en_core_web_sm',
                'hi': 'xx_ent_wiki_sm',  # Multilingual model for Hindi
                'mr': 'xx_ent_wiki_sm'   # Same for Marathi
            }
            
            for lang, model_name in model_configs.items():
                try:
                    self.nlp_models[lang] = spacy.load(model_name)
                    print(f"✓ Loaded {model_name} for {lang}")
                except OSError:
                    print(f"⚠️ {model_name} not found, using fallback")
                    self.nlp_models[lang] = spacy.load('xx_ent_wiki_sm')
            
            # Load lightweight language model for response generation
            print("Loading response generator...")
            model_name = "microsoft/DialoGPT-small"  # Lightweight conversational model
            
            self.response_tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.response_model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add special tokens for herbal context
            special_tokens = ["<herb>", "</herb>", "<symptom>", "</symptom>", "<ayush>", "</ayush>"]
            self.response_tokenizer.add_special_tokens({"additional_special_tokens": special_tokens})
            
            print("✓ All models loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading models: {e}")
            raise

class IntelligentHerbalAI:
    """Advanced AI system for herbal consultations"""
    
    def __init__(self, herbs_data):
        self.herbs_data = herbs_data
        self.lang_processor = AdvancedLanguageProcessor()
        self.intent_patterns = self._build_intent_patterns()
        self.symptom_herb_mapping = self._build_symptom_mapping()
        self.prepare_knowledge_base()
    
    def _build_intent_patterns(self):
        """Build patterns for intent recognition"""
        return {
            'search_herb': [
                r'(?:what is|tell me about|information about)\s+(.+)',
                r'(?:properties of|benefits of|uses of)\s+(.+)',
                r'^([a-zA-Z\u0900-\u097F\s]+)(?:\s+(?:plant|herb|medicine))?$'
            ],
            'symptom_query': [
                r'(?:i have|i am experiencing|suffering from)\s+(.+)',
                r'(?:cure for|treatment for|remedy for)\s+(.+)',
                r'(?:pain|ache|problem|issue|trouble)(?:\s+in\s+(.+))?',
                r'(?:stress|anxiety|depression|headache|fever|cold|cough)'
            ],
            'recommendation': [
                r'(?:suggest|recommend|advise)\s+(?:something for|herbs for|medicine for)\s+(.+)',
                r'(?:what should i take for|what helps with|what is good for)\s+(.+)',
                r'(?:natural remedy|herbal treatment|ayurvedic medicine)\s+for\s+(.+)'
            ],
            'general_health': [
                r'(?:improve|boost|enhance)\s+(?:my\s+)?(.+)',
                r'(?:strengthen|increase|build)\s+(?:my\s+)?(.+)',
                r'(?:how to|ways to)\s+(.+)'
            ]
        }
    
    def _build_symptom_mapping(self):
        """Enhanced symptom to herb mapping"""
        return {
            'stress': ['ashwagandha', 'brahmi', 'tulsi', 'jatamansi'],
            'anxiety': ['ashwagandha', 'brahmi', 'tulsi', 'shankhpushpi'],
            'depression': ['brahmi', 'mandukaparni', 'ashwagandha'],
            'insomnia': ['jatamansi', 'brahmi', 'ashwagandha'],
            'memory': ['brahmi', 'mandukaparni', 'shankhpushpi'],
            'immunity': ['tulsi', 'giloy', 'amla', 'turmeric'],
            'cold': ['tulsi', 'ginger', 'turmeric', 'licorice'],
            'cough': ['tulsi', 'vasaka', 'licorice', 'honey'],
            'fever': ['tulsi', 'neem', 'giloy', 'willow bark'],
            'inflammation': ['turmeric', 'neem', 'guggul', 'boswellia'],
            'arthritis': ['turmeric', 'guggul', 'boswellia', 'ginger'],
            'diabetes': ['gurmar', 'jamun', 'karela', 'methi'],
            'skin': ['neem', 'turmeric', 'aloe vera', 'manjistha'],
            'hair': ['bhringraj', 'amla', 'brahmi', 'fenugreek'],
            'digestion': ['ginger', 'ajwain', 'fennel', 'triphala'],
            'liver': ['kalmegh', 'bhumi amla', 'kutki', 'milk thistle'],
            'kidney': ['gokshura', 'punarnava', 'varun', 'cranberry'],
            'heart': ['arjuna', 'garlic', 'hawthorn', 'brahmi'],
            'respiratory': ['vasaka', 'tulsi', 'licorice', 'pippali'],
            'energy': ['ashwagandha', 'ginseng', 'shatavari', 'kapikacchu'],
            'weight_loss': ['triphala', 'guggul', 'garcinia', 'green tea'],
            'menstrual': ['shatavari', 'ashoka', 'lodhra', 'aloe vera'],
            'pregnancy': ['shatavari', 'dates', 'almonds', 'milk'],
            'elderly': ['brahmi', 'ashwagandha', 'shatavari', 'bala']
        }
###############################################

# Add these methods to your IntelligentHerbalAI class in search.py

    def _format_herb_data_for_frontend(self, herbs, language):
        """Format herb data with proper language support for frontend display"""
        formatted_herbs = []
        
        for herb in herbs:
            formatted_herb = {
                'id': herb.get('id', 0),
                'name': self._get_herb_name_in_language(herb, language),
                'scientific_name': herb.get('scientific_name', ''),
                'common_names': self._get_common_names_in_language(herb, language),
                'ayush_system': herb.get('ayush_system', 'Ayurveda'),
                'parts_used': self._translate_field_to_language(herb.get('parts_used', ''), language),
                'uses': self._translate_field_to_language(herb.get('uses', ''), language),
                'properties': self._translate_field_to_language(herb.get('properties', ''), language),
                'contraindications': self._translate_field_to_language(
                    herb.get('contraindications', '') or herb.get('precautions', ''), 
                    language
                ),
                'remedies': self._format_remedies_for_language(herb.get('remedies', []), language),
                'languages': herb.get('languages', {})
            }
            formatted_herbs.append(formatted_herb)
        
        return formatted_herbs

    def _get_common_names_in_language(self, herb, language):
        """Get common names prioritizing the requested language"""
        common_names = herb.get('common_names', [])
        languages_dict = herb.get('languages', {})
        
        # Start with the name in requested language if available
        names = []
        if language in languages_dict and languages_dict[language]:
            names.append(languages_dict[language])
        
        # Add main name if not already included
        main_name = herb.get('name', '')
        if main_name and main_name not in names:
            names.append(main_name)
        
        # Add other common names
        if isinstance(common_names, list):
            for name in common_names:
                if name and name not in names:
                    names.append(name)
        
        return names[:5]  # Limit to 3 names

    def _format_remedies_for_language(self, remedies, language):
        """Format remedies with proper language translation"""
        if not remedies:
            return []
        
        formatted_remedies = []
        for remedy in remedies[:3]:  # Limit to 3 remedies
            if isinstance(remedy, dict):
                formatted_remedy = {
                    'condition': self._translate_field_to_language(remedy.get('condition', ''), language),
                    'preparation': self._translate_field_to_language(remedy.get('preparation', ''), language),
                    'dosage': self._translate_field_to_language(remedy.get('dosage', ''), language) if remedy.get('dosage') else ''
                }
                formatted_remedies.append(formatted_remedy)
        
        return formatted_remedies

    def _translate_field_to_language(self, text, target_language):
        """Translate a field to target language if needed"""
        if not text or target_language == 'en':
            return str(text)
        
        # Check if text is already in target script
        if target_language in ['hi', 'mr'] and any('\u0900' <= ch <= '\u097F' for ch in str(text)):
            return str(text)
        
        # Use predefined translations for common terms
        common_translations = {
            'hi': {
                'Leaves': 'पत्ते',
                'Roots': 'जड़ें', 
                'Bark': 'छाल',
                'Seeds': 'बीज',
                'Flowers': 'फूल',
                'Whole plant': 'पूरा पौधा',
                'Rhizome': 'प्रकंद',
                'Immunity booster': 'रोग प्रतिरोधक क्षमता बढ़ाने वाला',
                'Anti-inflammatory': 'सूजन रोधी',
                'Antioxidant': 'एंटीऑक्सीडेंट',
                'cold and cough': 'सर्दी और खांसी',
                'Avoid during pregnancy': 'गर्भावस्था में उपयोग न करें',
                'Avoid in gallstones': 'पित्त की पथरी में न लें',
                'Consult doctor before use': 'उपयोग से पहले चिकित्सक से सलाह लें',
                'Boil Tulsi leaves in water and drink warm': 'तुलसी के पत्तों को पानी में उबालकर गर्म पिएं',
                'Apply turmeric paste on wounds': 'घावों पर हल्दी का पेस्ट लगाएं'
            },
            'mr': {
                'Leaves': 'पाने',
                'Roots': 'मुळे',
                'Bark': 'सालकाठ', 
                'Seeds': 'बिया',
                'Flowers': 'फुले',
                'Whole plant': 'संपूर्ण वनस्पती',
                'Rhizome': 'भूकंद',
                'Immunity booster': 'रोगप्रतिकारशक्ती वाढवणारे',
                'Anti-inflammatory': 'सूज कमी करणारे',
                'Antioxidant': 'अँटीऑक्सिडंट',
                'cold and cough': 'सर्दी आणि खोकला',
                'Avoid during pregnancy': 'गर्भावस्थेदरम्यान वापर करू नका',
                'Avoid in gallstones': 'पित्ताशयात खडे असल्यास वापर करू नका',
                'Consult doctor before use': 'वापरण्यापूर्वी डॉक्टरांचा सल्ला घ्या',
                'Boil Tulsi leaves in water and drink warm': 'तुळशीची पाने पाण्यात उकळून गरम प्या',
                'Apply turmeric paste on wounds': 'जखमांवर हळदीचा पेस्ट लावा'
            }
        }
        
        text_str = str(text)
        translations = common_translations.get(target_language, {})
        
        # Try direct translation first
        if text_str in translations:
            return translations[text_str]
        
        # Try to translate individual terms
        for english_term, translated_term in translations.items():
            if english_term.lower() in text_str.lower():
                text_str = text_str.replace(english_term, translated_term)
        
        # Fallback: try using the translator utility if available
        try:
            from utils.translator import translate_text
            return translate_text(text_str, 'en', target_language)
        except:
            pass
        
        return text_str

    def _get_herb_name_in_language(self, herb, language):
        """Get herb name in specified language with fallback"""
        if language in ['hi', 'mr']:
            languages = herb.get('languages', {})
            if isinstance(languages, dict) and language in languages:
                lang_name = languages[language]
                if lang_name and lang_name.strip():
                    return lang_name
        
        # Fallback to main name
        return herb.get('name', '')

    # MOST IMPORTANT: Update your process_query method to actually use the formatting
    def process_query(self, query):
        """
        Main query processing pipeline with improved formatting
        """
        print(f"\n=== PROCESSING QUERY: '{query}' ===")
        
        # Step 1: Language detection
        language = self.detect_language_advanced(query)
        print(f"Detected language: {language}")
        
        # Step 2: Intent analysis
        intent_data = self.analyze_intent(query, language)
        intent_data['original_query'] = query
        print(f"Intent analysis: {intent_data}")
        
        # Step 3: Find relevant herbs
        relevant_herbs = self.find_relevant_herbs(intent_data)
        print(f"Found {len(relevant_herbs)} relevant herbs")
        
        # Step 4: Format herbs data for frontend (THIS IS THE KEY ADDITION)
        formatted_herbs = self._format_herb_data_for_frontend(relevant_herbs, language)
        
        # Step 5: Generate contextual response
        response = self.generate_contextual_response(query, relevant_herbs, intent_data)
        
        # Step 6: Prepare API response with properly formatted data
        api_response = {
            'response_text': response,
            'herbs_found': len(relevant_herbs),
            'intent': intent_data['intent'],
            'language': language,
            'confidence': intent_data['confidence'],
            'herbs_data': formatted_herbs,  # Now properly formatted for frontend
            'entities': intent_data['entities']
        }
        
        print(f"=== RESPONSE GENERATED ===\n")
        return api_response    

###############################################
    def process_query1(self, query):
        """
        Main query processing pipeline - This is the core AI method.
        
        Args:
            query (str): User's query in any supported language
            
        Returns:
            dict: Complete AI response with metadata
        """
        print(f"\n=== PROCESSING QUERY: '{query}' ===")
        
        # Step 1: Language detection
        language = self.detect_language_advanced(query)
        print(f"Detected language: {language}")
        
        # Step 2: Intent analysis
        intent_data = self.analyze_intent(query, language)
        intent_data['original_query'] = query
        print(f"Intent analysis: {intent_data}")
        
        # Step 3: Find relevant herbs
        relevant_herbs = self.find_relevant_herbs(intent_data)
        print(f"Found {len(relevant_herbs)} relevant herbs")
        
        # Step 4: Generate contextual response
        response = self.generate_contextual_response(query, relevant_herbs, intent_data)
        
        # Step 5: Prepare API response
        api_response = {
            'response_text': response,
            'herbs_found': len(relevant_herbs),
            'intent': intent_data['intent'],
            'language': language,
            'confidence': intent_data['confidence'],
            'herbs_data': relevant_herbs[:3],  # Include herb data for frontend
            'entities': intent_data['entities']
        }
        
        print(f"=== RESPONSE GENERATED ===\n")
        return api_response
    
    def prepare_knowledge_base(self):
        """Prepare enhanced knowledge base"""
        print("Building knowledge base...")
        
        self.herb_profiles = {}
        self.semantic_knowledge = []
        
        for i, herb in enumerate(self.herbs_data):
            # Create comprehensive herb profile
            profile = {
                'index': i,
                'name': herb.get('name', ''),
                'scientific_name': herb.get('scientific_name', ''),
                'common_names': herb.get('common_names', []),
                'languages': herb.get('languages', {}),
                'uses': herb.get('uses', ''),
                'properties': herb.get('properties', ''),
                'parts_used': herb.get('parts_used', ''),
                'dosage': herb.get('dosage', ''),
                'precautions': herb.get('precautions', ''),
                'ayush_system': herb.get('ayush_system', ''),
                'remedies': herb.get('remedies', []),
                'therapies': herb.get('therapies', []),
                'related_conditions': herb.get('related_conditions', [])
            }
            
            self.herb_profiles[i] = profile
            
            # Build semantic knowledge text
            knowledge_text = f"""
            {profile['name']} ({profile['scientific_name']}) is a medicinal plant used in {profile['ayush_system']} system.
            Common names: {', '.join(profile['common_names']) if profile['common_names'] else 'None'}.
            Uses: {profile['uses']}.
            Properties: {profile['properties']}.
            Parts used: {profile['parts_used']}.
            Treats conditions: {', '.join(profile['related_conditions']) if profile['related_conditions'] else 'Various'}.
            """
            
            self.semantic_knowledge.append(knowledge_text.strip())
    
    def detect_language_advanced(self, text):
        """Advanced language detection"""
        text = text.strip()
        
        # Check for Devanagari script
        if any('\u0900' <= ch <= '\u097F' for ch in text):
            # Use character-based detection for Hindi vs Marathi
            marathi_chars = set('ळऱवझञ')
            hindi_chars = set('क़ख़ग़ज़ड़ढ़फ़य़')
            
            text_chars = set(text)
            if text_chars & marathi_chars:
                return 'mr'
            elif text_chars & hindi_chars:
                return 'hi'
            else:
                # Use common words for detection
                marathi_words = ['तुळस', 'आळू', 'काळा', 'पिळू']
                hindi_words = ['तुलसी', 'आलू', 'काला', 'पीला']
                
                for word in marathi_words:
                    if word in text:
                        return 'mr'
                for word in hindi_words:
                    if word in text:
                        return 'hi'
                
                return 'hi'  # Default to Hindi
        
        # Try langdetect for other languages
        try:
            detected = detect(text)
            return detected if detected in ['en', 'hi', 'mr'] else 'en'
        except:
            return 'en'
    
    def analyze_intent(self, query, language):
        """Analyze user intent using spaCy and patterns"""
        nlp = self.lang_processor.nlp_models.get(language, self.lang_processor.nlp_models['en'])
        doc = nlp(query.lower())
        
        # Extract entities
        entities = {
            'symptoms': [],
            'body_parts': [],
            'herbs': [],
            'conditions': []
        }
        
        # Define entity patterns
        symptom_keywords = {
            'en': ['pain', 'ache', 'stress', 'anxiety', 'depression', 'fever', 'cold', 'cough', 'headache'],
            'hi': ['दर्द', 'तनाव', 'चिंता', 'बुखार', 'सर्दी', 'खांसी', 'सिरदर्द'],
            'mr': ['वेदना', 'ताण', 'चिंता', 'ताप', 'सर्दी', 'खोकला', 'डोकेदुखी']
        }
        
        body_parts = {
            'en': ['head', 'stomach', 'chest', 'back', 'joints', 'skin', 'hair', 'heart', 'liver', 'kidney'],
            'hi': ['सिर', 'पेट', 'छाती', 'पीठ', 'जोड़', 'त्वचा', 'बाल', 'दिल', 'यकृत', 'गुर्दा'],
            'mr': ['डोके', 'पोट', 'छाती', 'पाठ', 'सांधे', 'त्वचा', 'केस', 'हृदय', 'यकृत', 'मूत्रपिंड']
        }
        
        # Extract entities based on keywords
        query_lower = query.lower()
        lang_symptoms = symptom_keywords.get(language, symptom_keywords['en'])
        lang_body_parts = body_parts.get(language, body_parts['en'])
        
        for symptom in lang_symptoms:
            if symptom in query_lower:
                entities['symptoms'].append(symptom)
        
        for part in lang_body_parts:
            if part in query_lower:
                entities['body_parts'].append(part)
        
        # Determine intent
        intent = 'general_query'
        confidence = 0.5
        
        if entities['symptoms']:
            intent = 'symptom_treatment'
            confidence = 0.9
        elif any(word in query_lower for word in ['suggest', 'recommend', 'advise', 'सुझाव', 'सल्ला']):
            intent = 'recommendation_request'
            confidence = 0.8
        elif any(word in query_lower for word in ['what is', 'tell me', 'information', 'क्या है', 'काय आहे']):
            intent = 'herb_information'
            confidence = 0.8
        elif len(query.split()) <= 2:
            intent = 'herb_search'
            confidence = 0.7
        
        return {
            'intent': intent,
            'confidence': confidence,
            'entities': entities,
            'language': language
        }
    
    def _find_herb_by_name_enhanced(self, herb_name):
        """Enhanced herb finding with better matching"""
        if not herb_name:
            return None
            
        herb_name_normalized = self._normalize_text(herb_name.lower())
        
        print(f"Looking for herb: '{herb_name}' (normalized: '{herb_name_normalized}')")
        
        for herb in self.herbs_data:
            # Check main name
            main_name = herb.get('name', '')
            if main_name and self._normalize_text(main_name.lower()) == herb_name_normalized:
                print(f"Exact main name match found: '{main_name}'")
                return herb
            
            # Check if herb name is contained in main name or vice versa
            if main_name and (herb_name_normalized in self._normalize_text(main_name.lower()) or 
                            self._normalize_text(main_name.lower()) in herb_name_normalized):
                print(f"Partial main name match found: '{main_name}'")
                return herb
            
            # Check alternative names
            alt_names = herb.get('alt_names', [])
            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    if alt_name and self._normalize_text(alt_name.lower()) == herb_name_normalized:
                        print(f"Exact alt name match found: '{alt_name}' -> '{main_name}'")
                        return herb
                    if alt_name and (herb_name_normalized in self._normalize_text(alt_name.lower()) or 
                                    self._normalize_text(alt_name.lower()) in herb_name_normalized):
                        print(f"Partial alt name match found: '{alt_name}' -> '{main_name}'")
                        return herb
            
            # Check multilingual names
            languages_dict = herb.get('languages', {})
            if isinstance(languages_dict, dict):
                for lang_code, lang_name in languages_dict.items():
                    if lang_name and self._normalize_text(lang_name.lower()) == herb_name_normalized:
                        print(f"Exact language name match found: '{lang_name}' ({lang_code}) -> '{main_name}'")
                        return herb
                    if lang_name and (herb_name_normalized in self._normalize_text(lang_name.lower()) or 
                                    self._normalize_text(lang_name.lower()) in herb_name_normalized):
                        print(f"Partial language name match found: '{lang_name}' ({lang_code}) -> '{main_name}'")
                        return herb
        
        print(f"No herb found for: '{herb_name}'")
        return None
    
    def _translate_symptom_to_english(self, symptom, language):
        """Enhanced symptom translation"""
        if language == 'en':
            return symptom
        
        # Symptom translation mapping
        symptom_translations = {
            'hi': {
                'दर्द': 'pain',
                'तनाव': 'stress',
                'चिंता': 'anxiety',
                'बुखार': 'fever',
                'सर्दी': 'cold',
                'खांसी': 'cough',
                'सिरदर्द': 'headache',
                'ऊर्जा': 'energy',
                'शक्ति': 'energy',
                'बल': 'energy',
                'रोग प्रतिरोधक': 'immunity',
                'प्रतिरक्षा': 'immunity'
            },
            'mr': {
                'वेदना': 'pain',
                'ताण': 'stress',
                'चिंता': 'anxiety',
                'ताप': 'fever',
                'सर्दी': 'cold',
                'खोकला': 'cough',
                'डोकेदुखी': 'headache',
                'ऊर्जा': 'energy',
                'शक्ती': 'energy',
                'रोगप्रतिकारशक्ति': 'immunity'
            }
        }
        
        translations = symptom_translations.get(language, {})
        return translations.get(symptom, symptom)
    
    def _enhanced_herb_name_search(self, query, language):
        """Enhanced herb name search with better fuzzy matching"""
        query_normalized = self._normalize_text(query)
        matches = []
        
        print(f"Searching for herbs with normalized query: '{query_normalized}'")
        
        # Common herb name mappings for different languages
        herb_name_mappings = {
            'अशोक': 'ashoka',
            'अश्वगंधा': 'ashwagandha',
            'तुलसी': 'tulsi',
            'हल्दी': 'turmeric',
            'अदरक': 'ginger',
            'आंवला': 'amla',
            'गिलोय': 'giloy',
            'ब्राह्मी': 'brahmi',
            'नीम': 'neem',
            'एलोवेरा': 'aloe vera',
            'अशोका': 'ashoka',  # Marathi
            'तुळशी': 'tulsi',    # Marathi
            'हळद': 'turmeric',   # Marathi
        }
        
        # Check direct mappings first
        for local_name, english_name in herb_name_mappings.items():
            if local_name in query_normalized:
                matches.append(english_name)
                print(f"Direct mapping found: '{local_name}' -> '{english_name}'")
        
        # Search through database
        for herb in self.herbs_data:
            herb_found = False
            
            # Check main name
            herb_name = herb.get('name', '').lower()
            if query_normalized in herb_name or herb_name in query_normalized:
                matches.append(herb.get('name', ''))
                herb_found = True
                print(f"Main name match: '{herb_name}'")
            
            # Check alternative names
            if not herb_found:
                alt_names = herb.get('alt_names', [])
                if isinstance(alt_names, list):
                    for alt_name in alt_names:
                        alt_name_normalized = self._normalize_text(alt_name.lower())
                        if query_normalized in alt_name_normalized or alt_name_normalized in query_normalized:
                            matches.append(herb.get('name', ''))
                            herb_found = True
                            print(f"Alt name match: '{alt_name}' -> '{herb.get('name', '')}'")
                            break
            
            # Check multilingual names
            if not herb_found:
                languages_dict = herb.get('languages', {})
                if isinstance(languages_dict, dict):
                    for lang_code, lang_name in languages_dict.items():
                        if lang_name:
                            lang_name_normalized = self._normalize_text(lang_name.lower())
                            if query_normalized in lang_name_normalized or lang_name_normalized in query_normalized:
                                matches.append(herb.get('name', ''))
                                herb_found = True
                                print(f"Language name match: '{lang_name}' ({lang_code}) -> '{herb.get('name', '')}'")
                                break
        
        return list(dict.fromkeys(matches))  # Remove duplicates while preserving order
    
    def _find_herb_by_name_enhanced(self, herb_name):
        """Enhanced herb finding with better matching"""
        if not herb_name:
            return None
            
        herb_name_normalized = self._normalize_text(herb_name.lower())
        
        print(f"Looking for herb: '{herb_name}' (normalized: '{herb_name_normalized}')")
        
        for herb in self.herbs_data:
            # Check main name
            main_name = herb.get('name', '')
            if main_name and self._normalize_text(main_name.lower()) == herb_name_normalized:
                print(f"Exact main name match found: '{main_name}'")
                return herb
            
            # Check if herb name is contained in main name or vice versa
            if main_name and (herb_name_normalized in self._normalize_text(main_name.lower()) or 
                            self._normalize_text(main_name.lower()) in herb_name_normalized):
                print(f"Partial main name match found: '{main_name}'")
                return herb
            
            # Check alternative names
            alt_names = herb.get('alt_names', [])
            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    if alt_name and self._normalize_text(alt_name.lower()) == herb_name_normalized:
                        print(f"Exact alt name match found: '{alt_name}' -> '{main_name}'")
                        return herb
                    if alt_name and (herb_name_normalized in self._normalize_text(alt_name.lower()) or 
                                    self._normalize_text(alt_name.lower()) in herb_name_normalized):
                        print(f"Partial alt name match found: '{alt_name}' -> '{main_name}'")
                        return herb
            
            # Check multilingual names
            languages_dict = herb.get('languages', {})
            if isinstance(languages_dict, dict):
                for lang_code, lang_name in languages_dict.items():
                    if lang_name and self._normalize_text(lang_name.lower()) == herb_name_normalized:
                        print(f"Exact language name match found: '{lang_name}' ({lang_code}) -> '{main_name}'")
                        return herb
                    if lang_name and (herb_name_normalized in self._normalize_text(lang_name.lower()) or 
                                    self._normalize_text(lang_name.lower()) in herb_name_normalized):
                        print(f"Partial language name match found: '{lang_name}' ({lang_code}) -> '{main_name}'")
                        return herb
        
        print(f"No herb found for: '{herb_name}'")
        return None

    def _normalize_text(self, text):
        """Normalize text for better matching"""
        import unicodedata
        import re
        
        if not text:
            return ""
        
        # Normalize unicode characters
        normalized = unicodedata.normalize("NFKC", text)
        # Remove extra whitespace
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        
        return normalized

    # Also update the symptom_herb_mapping to include more comprehensive mappings
    def _build_symptom_mapping(self):
        """Enhanced symptom to herb mapping"""
        return {
            'stress': ['ashwagandha', 'brahmi', 'tulsi', 'jatamansi', 'shankhpushpi'],
            'anxiety': ['ashwagandha', 'brahmi', 'tulsi', 'shankhpushpi', 'jatamansi'],
            'depression': ['brahmi', 'mandukaparni', 'ashwagandha', 'shankhpushpi'],
            'insomnia': ['jatamansi', 'brahmi', 'ashwagandha', 'chamomile'],
            'memory': ['brahmi', 'mandukaparni', 'shankhpushpi', 'ginkgo'],
            'immunity': ['tulsi', 'giloy', 'amla', 'turmeric', 'ginger', 'echinacea'],
            'cold': ['tulsi', 'ginger', 'turmeric', 'licorice', 'elderberry'],
            'cough': ['tulsi', 'vasaka', 'licorice', 'honey', 'ginger'],
            'fever': ['tulsi', 'neem', 'giloy', 'willow bark', 'ginger'],
            'inflammation': ['turmeric', 'neem', 'guggul', 'boswellia', 'ginger'],
            'arthritis': ['turmeric', 'guggul', 'boswellia', 'ginger', 'ashwagandha'],
            'diabetes': ['gurmar', 'jamun', 'karela', 'methi', 'cinnamon'],
            'skin': ['neem', 'turmeric', 'aloe vera', 'manjistha', 'calendula'],
            'hair': ['bhringraj', 'amla', 'brahmi', 'fenugreek', 'rosemary'],
            'digestion': ['ginger', 'ajwain', 'fennel', 'triphala', 'peppermint'],
            'liver': ['kalmegh', 'bhumi amla', 'kutki', 'milk thistle', 'dandelion'],
            'kidney': ['gokshura', 'punarnava', 'varun', 'cranberry', 'nettle'],
            'heart': ['arjuna', 'garlic', 'hawthorn', 'brahmi', 'ginger'],
            'respiratory': ['vasaka', 'tulsi', 'licorice', 'pippali', 'eucalyptus'],
            'energy': ['ashwagandha', 'ginseng', 'shatavari', 'kapikacchu', 'rhodiola'],
            'weight_loss': ['triphala', 'guggul', 'garcinia', 'green tea', 'ginger'],
            'menstrual': ['shatavari', 'ashoka', 'lodhra', 'aloe vera', 'ginger'],
            'pregnancy': ['shatavari', 'dates', 'almonds', 'milk', 'ginger'],
            'elderly': ['brahmi', 'ashwagandha', 'shatavari', 'bala', 'ginkgo']
        }

    
    def generate_contextual_response(self, query, relevant_herbs, intent_data):
        """Generate AI-like contextual response"""
        language = intent_data['language']
        intent = intent_data['intent']
        entities = intent_data['entities']
        
        if not relevant_herbs:
            return self._generate_no_results_response(query, language)
        
        # Generate response based on intent
        if intent == 'symptom_treatment':
            response = self._generate_symptom_treatment_response(relevant_herbs, entities, language)
        elif intent == 'herb_information':
            response = self._generate_herb_information_response(relevant_herbs, language)
        elif intent == 'recommendation_request':
            response = self._generate_recommendation_response(relevant_herbs, entities, language)
        else:
            response = self._generate_general_response(relevant_herbs, language)
        
        # Add AI personality and safety disclaimer
        response = self._add_ai_personality(response, language)
        response += self._get_safety_disclaimer(language)
        
        return response
    
    def _generate_symptom_treatment_response(self, herbs, entities, language):
        """Generate response for symptom treatment queries"""
        symptoms = entities['symptoms']
        
        templates = {
            'en': {
                'intro': "Based on traditional AYUSH knowledge, here are some herbs that may help with {}:",
                'herb_format': "🌿 **{}** ({})\n   • Uses: {}\n   • Preparation: {}\n   • Precautions: {}\n",
                'outro': "\nThese are traditional remedies used in {} system."
            },
            'hi': {
                'intro': "पारंपरिक आयुष ज्ञान के आधार पर, {} के लिए ये जड़ी-बूटियां सहायक हो सकती हैं:",
                'herb_format': "🌿 **{}** ({})\n   • उपयोग: {}\n   • तैयारी: {}\n   • सावधानियां: {}\n",
                'outro': "\nये {} पद्धति में उपयोग होने वाले पारंपरिक उपचार हैं।"
            },
            'mr': {
                'intro': "पारंपरिक आयुष ज्ञानाच्या आधारे, {} साठी ही औषधी वनस्पती उपयुक्त असू शकतात:",
                'herb_format': "🌿 **{}** ({})\n   • उपयोग: {}\n   • तयारी: {}\n   • खबरदारी: {}\n",
                'outro': "\nहे {} पद्धतीमधील पारंपरिक उपचार आहेत।"
            }
        }
        
        template = templates.get(language, templates['en'])
        
        # Build response
        symptom_text = ', '.join(symptoms) if symptoms else 'आपकी समस्या'
        response = template['intro'].format(symptom_text) + "\n\n"
        
        for herb in herbs[:3]:  # Limit to 3 herbs
            herb_name = self._get_herb_name_in_language(herb, language)
            scientific_name = herb.get('scientific_name', 'N/A')
            uses = self._get_herb_uses_in_language(herb, language)
            preparation = self._get_preparation_info(herb, language)
            precautions = self._get_precautions_in_language(herb, language)
            
            response += template['herb_format'].format(
                herb_name, scientific_name, uses, preparation, precautions
            )
        
        # Add system info
        systems = list(set([herb.get('ayush_system', 'AYUSH') for herb in herbs]))
        response += template['outro'].format(', '.join(systems))
        
        return response

    def _get_herb_uses_in_language(self, herb, language):
        """Get herb uses in specified language"""
        uses = herb.get('uses', '')
        if language in ['hi', 'mr'] and uses:
            try:
                return translate_text(str(uses), 'en', language)
            except:
                return uses
        return uses
    
    def _get_preparation_info(self, herb, language):
        """Get preparation information"""
        remedies = herb.get('remedies', [])
        if remedies and len(remedies) > 0:
            if isinstance(remedies[0], dict):
                return remedies[0].get('preparation', 'As directed by physician')
        
        templates = {
            'en': 'As directed by qualified practitioner',
            'hi': 'योग्य चिकित्सक के निर्देशानुसार',
            'mr': 'योग्य वैद्याच्या सूचनेनुसार'
        }
        return templates.get(language, templates['en'])
    
    def _get_precautions_in_language(self, herb, language):
        """Get precautions in specified language"""
        precautions = herb.get('precautions', '') or herb.get('contraindications', '')
        if not precautions:
            templates = {
                'en': 'Consult healthcare provider before use',
                'hi': 'उपयोग से पहले चिकित्सक से सलाह लें',
                'mr': 'वापरण्यापूर्वी डॉक्टरांचा सल्ला घ्या'
            }
            return templates.get(language, templates['en'])
        
        if language in ['hi', 'mr']:
            try:
                return translate_text(str(precautions), 'en', language)
            except:
                return precautions
        return precautions

    def _format_uses(self, uses, language):
        """Format uses text for display"""
        if isinstance(uses, list):
            return '\n'.join([f"• {use}" for use in uses[:3]])
        elif isinstance(uses, str):
            # Split by periods or commas and create bullet points
            uses_list = [use.strip() for use in re.split(r'[.,;]', uses) if use.strip()]
            return '\n'.join([f"• {use}" for use in uses_list[:3]])
        return str(uses)

    def _format_preparations(self, remedies, language):
        """Format preparation instructions"""
        if not remedies:
            templates = {
                'en': '• Consult AYUSH practitioner for proper preparation',
                'hi': '• उचित तैयारी के लिए आयुष चिकित्सक से सलाह लें',
                'mr': '• योग्य तयारीसाठी आयुष वैद्यांचा सल्ला घ्या'
            }
            return templates.get(language, templates['en'])
        
        formatted = []
        for remedy in remedies[:3]:
            if isinstance(remedy, dict):
                condition = remedy.get('condition', '')
                preparation = remedy.get('preparation', '')
                if condition and preparation:
                    formatted.append(f"• {condition}: {preparation}")
        
        return '\n'.join(formatted) if formatted else self._format_preparations([], language)

    def _generate_multiple_herbs_info(self, herbs, language):
        """Generate information for multiple herbs"""
        templates = {
            'en': "Here are several herbs that might be relevant to your query:\n\n",
            'hi': "आपके प्रश्न से संबंधित कुछ जड़ी-बूटियां यहां हैं:\n\n",
            'mr': "तुमच्या प्रश्नाशी संबंधित काही औषधी वनस्पती येथे आहेत:\n\n"
        }
        
        response = templates.get(language, templates['en'])
        
        for herb in herbs[:3]:
            herb_name = self._get_herb_name_in_language(herb, language)
            scientific_name = herb.get('scientific_name', '')
            uses = herb.get('uses', '')[:100] + '...' if len(str(herb.get('uses', ''))) > 100 else herb.get('uses', '')
            
            response += f"🌿 **{herb_name}** ({scientific_name})\n"
            response += f"   {self._get_herb_uses_in_language(herb, language)}\n\n"
        
        return response

    def _generate_recommendation_response(self, herbs, entities, language):
        """Generate recommendation-style response"""
        templates = {
            'en': "I recommend considering these traditional herbs:\n\n",
            'hi': "मैं इन पारंपरिक जड़ी-बूटियों पर विचार करने की सलाह देता हूं:\n\n",
            'mr': "मी या पारंपरिक औषधी वनस्पतींचा विचार करण्याची शिफारस करतो:\n\n"
        }
        
        response = templates.get(language, templates['en'])
        
        for i, herb in enumerate(herbs[:3], 1):
            herb_name = self._get_herb_name_in_language(herb, language)
            uses = self._get_herb_uses_in_language(herb, language)
            response += f"{i}. **{herb_name}**: {uses}\n\n"
        
        return response

    def _generate_general_response(self, herbs, language):
        """Generate general response"""
        return self._generate_multiple_herbs_info(herbs, language)

    def _translate_to_english(self, text, source_language):
        """Translate text to English for internal processing"""
        if source_language == 'en':
            return text
        
        try:
            return translate_text(text, source_language, 'en')
        except:
            return text
    
    def _generate_herb_information_response(self, herbs, language):
        """Generate detailed information about specific herbs"""
        if len(herbs) == 1:
            return self._generate_detailed_herb_info(herbs[0], language)
        else:
            return self._generate_multiple_herbs_info(herbs, language)
    
    def _generate_detailed_herb_info(self, herb, language):
        """Generate detailed information for a single herb"""
        templates = {
            'en': """🌿 **{}** ({})

**AYUSH System**: {}
**Parts Used**: {}
**Properties**: {}

**Primary Uses**:
{}

**Traditional Preparations**:
{}

**Precautions**: {}

**Related Conditions**: {}
""",
            'hi': """🌿 **{}** ({})

**आयुष पद्धति**: {}
**उपयोगी भाग**: {}
**गुण**: {}

**मुख्य उपयोग**:
{}

**पारंपरिक तैयारी**:
{}

**सावधानियां**: {}

**संबंधित रोग**: {}
""",
            'mr': """🌿 **{}** ({})

**आयुष पद्धती**: {}
**वापरण्याचे भाग**: {}
**गुणधर्म**: {}

**मुख्य उपयोग**:
{}

**पारंपरिक तयारी**:
{}

**खबरदारी**: {}

**संबंधित आजार**: {}
"""
        }
        
        template = templates.get(language, templates['en'])
        
        herb_name = self._get_herb_name_in_language(herb, language)
        scientific_name = herb.get('scientific_name', 'N/A')
        ayush_system = herb.get('ayush_system', 'AYUSH')
        parts_used = herb.get('parts_used', 'N/A')
        properties = herb.get('properties', 'N/A')
        uses = self._format_uses(herb.get('uses', ''), language)
        preparations = self._format_preparations(herb.get('remedies', []), language)
        precautions = herb.get('precautions', 'कोई विशेष सावधानी नहीं')
        conditions = ', '.join(herb.get('related_conditions', []))
        
        return template.format(
            herb_name, scientific_name, ayush_system, parts_used, properties,
            uses, preparations, precautions, conditions
        )
    
    def _generate_no_results_response(self, query, language):
        """Generate response when no relevant herbs found"""
        responses = {
            'en': f"""I understand you're asking about "{query}", but I couldn't find specific herbal information related to this query in my knowledge base.

Could you please:
• Rephrase your question more specifically
• Mention specific symptoms or conditions
• Try using common names for herbs
• Ask about general health concerns

For example: "herbs for stress relief" or "what is tulsi used for"

I'm here to help with traditional AYUSH medicinal plants and their uses!""",
            
            'hi': f"""मैं समझ गया कि आप "{query}" के बारे में पूछ रहे हैं, लेकिन मुझे अपने ज्ञान आधार में इससे संबंधित जानकारी नहीं मिली।

कृपया आप:
• अपना प्रश्न अधिक स्पष्ट रूप से पूछें
• विशिष्ट लक्षण या समस्याओं का उल्लेख करें
• जड़ी-बूटियों के सामान्य नामों का उपयोग करें
• सामान्य स्वास्थ्य संबंधी चिंताओं के बारे में पूछें

उदाहरण: "तनाव के लिए जड़ी बूटी" या "तुलसी का क्या उपयोग है"

मैं पारंपरिक आयुष औषधीय पौधों की जानकारी देने के लिए यहां हूं!""",
            
            'mr': f"""मला समजले की तुम्ही "{query}" बद्दल विचारत आहात, पण माझ्या ज्ञान आधारात याशी संबंधित माहिती सापडली नाही।

कृपया तुम्ही:
• तुमचा प्रश्न अधिक स्पष्टपणे विचारा
• विशिष्ट लक्षणे किंवा समस्यांचा उल्लेख करा
• औषधी वनस्पतींची सामान्य नावे वापरा
• सामान्य आरोग्य समस्यांबद्दल विचारा

उदाहरण: "तणावासाठी औषधी वनस्पती" किंवा "तुळशीचा काय उपयोग आहे"

मी पारंपरिक आयुष औषधी वनस्पतींची माहिती देण्यासाठी येथे आहे!"""
        }
        
        return responses.get(language, responses['en'])
    
    def _add_ai_personality(self, response, language):
        """Add AI personality to make responses more conversational"""
        personality_prefixes = {
            'en': [
                "Based on traditional AYUSH wisdom, ",
                "From my knowledge of medicinal plants, ",
                "According to traditional herbal medicine, ",
                "In AYUSH systems, "
            ],
            'hi': [
                "पारंपरिक आयुष ज्ञान के अनुसार, ",
                "औषधीय पौधों के मेरे ज्ञान से, ",
                "पारंपरिक हर्बल चिकित्सा के अनुसार, ",
                "आयुष पद्धतियों में, "
            ],
            'mr': [
                "पारंपरिक आयुष ज्ञानानुसार, ",
                "औषधी वनस्पतींच्या माझ्या ज्ञानावरून, ",
                "पारंपरिक वनौषधी उपचारानुसार, ",
                "आयुष पद्धतींमध्ये, "
            ]
        }
        
        # Don't add prefix if response already starts with one
        prefixes = personality_prefixes.get(language, personality_prefixes['en'])
        if not any(response.startswith(prefix) for prefix in prefixes):
            prefix = np.random.choice(prefixes)
            response = prefix + response
        
        return response
    
    def _get_safety_disclaimer(self, language):
        """Get safety disclaimer in appropriate language"""
        disclaimers = {
            'en': "\n\n⚠️ **Important**: This information is for educational purposes only. Please consult qualified healthcare practitioners before starting any herbal treatment, especially if you have existing medical conditions or are taking medications.",
            
            'hi': "\n\n⚠️ **महत्वपूर्ण**: यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। कोई भी हर्बल उपचार शुरू करने से पहले योग्य चिकित्सा विशेषज्ञों से सलाह लें, विशेषकर यदि आपकी कोई मौजूदा बीमारी है या आप दवाएं ले रहे हैं।",
            
            'mr': "\n\n⚠️ **महत्त्वाचे**: ही माहिती केवळ शैक्षणिक हेतूंसाठी आहे। कोणताही वनौषधी उपचार सुरू करण्यापूर्वी योग्य आरोग्य तज्ञांचा सल्ला घ्या, विशेषतः जर तुमच्याकडे विद्यमान वैद्यकीय समस्या असतील किंवा तुम्ही औषधे घेत असाल."
        }
        
        return disclaimers.get(language, disclaimers['en'])
    
    def _search_herbs_by_name(self, query):
        """Search herbs by name with fuzzy matching"""
        query_normalized = unicodedata.normalize("NFKC", query.lower().strip())
        matches = []
        
        for herb in self.herbs_data:
            # Check main name
            if query_normalized in herb.get('name', '').lower():
                matches.append(herb.get('name', ''))
            
            # Check alternative names
            alt_names = herb.get('alt_names', [])
            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    if query_normalized in alt_name.lower():
                        matches.append(herb.get('name', ''))
                        break
            
            # Check multilingual names
            languages = herb.get('languages', {})
            if isinstance(languages, dict):
                for lang_name in languages.values():
                    if lang_name and query_normalized in lang_name.lower():
                        matches.append(herb.get('name', ''))
                        break
        
        return list(set(matches))[:5]
    
    def _find_herb_by_name(self, herb_name):
        """Find herb object by name"""
        herb_name_lower = herb_name.lower()
        
        for herb in self.herbs_data:
            if herb.get('name', '').lower() == herb_name_lower:
                return herb
            
            # Check alternative names
            alt_names = herb.get('alt_names', [])
            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    if alt_name.lower() == herb_name_lower:
                        return herb
        
        return None
    
    def _get_herb_name_in_language(self, herb, language):
        """Get herb name in specified language"""
        if language in ['hi', 'mr']:
            languages = herb.get('languages', {})
            if isinstance(languages, dict) and language in languages:
                return languages[language]
    """Advanced AI system for herbal consultations"""
    
    def __init__(self, herbs_data):
        self.herbs_data = herbs_data
        self.lang_processor = AdvancedLanguageProcessor()
        self.intent_patterns = self._build_intent_patterns()
        self.symptom_herb_mapping = self._build_symptom_mapping()
        self.prepare_knowledge_base()
    
    def _build_intent_patterns(self):
        """Build patterns for intent recognition"""
        return {
            'search_herb': [
                r'(?:what is|tell me about|information about)\s+(.+)',
                r'(?:properties of|benefits of|uses of)\s+(.+)',
                r'^([a-zA-Z\u0900-\u097F\s]+)(?:\s+(?:plant|herb|medicine))?$'
            ],
            'symptom_query': [
                r'(?:i have|i am experiencing|suffering from)\s+(.+)',
                r'(?:cure for|treatment for|remedy for)\s+(.+)',
                r'(?:pain|ache|problem|issue|trouble)(?:\s+in\s+(.+))?',
                r'(?:stress|anxiety|depression|headache|fever|cold|cough)'
            ],
            'recommendation': [
                r'(?:suggest|recommend|advise)\s+(?:something for|herbs for|medicine for)\s+(.+)',
                r'(?:what should i take for|what helps with|what is good for)\s+(.+)',
                r'(?:natural remedy|herbal treatment|ayurvedic medicine)\s+for\s+(.+)'
            ],
            'general_health': [
                r'(?:improve|boost|enhance)\s+(?:my\s+)?(.+)',
                r'(?:strengthen|increase|build)\s+(?:my\s+)?(.+)',
                r'(?:how to|ways to)\s+(.+)'
            ]
        }
    
    def _build_symptom_mapping(self):
        """Enhanced symptom to herb mapping"""
        return {
            'stress': ['ashwagandha', 'brahmi', 'tulsi', 'jatamansi'],
            'anxiety': ['ashwagandha', 'brahmi', 'tulsi', 'shankhpushpi'],
            'depression': ['brahmi', 'mandukaparni', 'ashwagandha'],
            'insomnia': ['jatamansi', 'brahmi', 'ashwagandha'],
            'memory': ['brahmi', 'mandukaparni', 'shankhpushpi'],
            'immunity': ['tulsi', 'giloy', 'amla', 'turmeric'],
            'cold': ['tulsi', 'ginger', 'turmeric', 'licorice'],
            'cough': ['tulsi', 'vasaka', 'licorice', 'honey'],
            'fever': ['tulsi', 'neem', 'giloy', 'willow bark'],
            'inflammation': ['turmeric', 'neem', 'guggul', 'boswellia'],
            'arthritis': ['turmeric', 'guggul', 'boswellia', 'ginger'],
            'diabetes': ['gurmar', 'jamun', 'karela', 'methi'],
            'skin': ['neem', 'turmeric', 'aloe vera', 'manjistha'],
            'hair': ['bhringraj', 'amla', 'brahmi', 'fenugreek'],
            'digestion': ['ginger', 'ajwain', 'fennel', 'triphala'],
            'liver': ['kalmegh', 'bhumi amla', 'kutki', 'milk thistle'],
            'kidney': ['gokshura', 'punarnava', 'varun', 'cranberry'],
            'heart': ['arjuna', 'garlic', 'hawthorn', 'brahmi'],
            'respiratory': ['vasaka', 'tulsi', 'licorice', 'pippali'],
            'energy': ['ashwagandha', 'ginseng', 'shatavari', 'kapikacchu'],
            'weight_loss': ['triphala', 'guggul', 'garcinia', 'green tea'],
            'menstrual': ['shatavari', 'ashoka', 'lodhra', 'aloe vera'],
            'pregnancy': ['shatavari', 'dates', 'almonds', 'milk'],
            'elderly': ['brahmi', 'ashwagandha', 'shatavari', 'bala']
        }
    
    def prepare_knowledge_base(self):
        """Prepare enhanced knowledge base"""
        print("Building knowledge base...")
        
        self.herb_profiles = {}
        self.semantic_knowledge = []
        
        for i, herb in enumerate(self.herbs_data):
            # Create comprehensive herb profile
            profile = {
                'index': i,
                'name': herb.get('name', ''),
                'scientific_name': herb.get('scientific_name', ''),
                'common_names': herb.get('alt_names', []),
                'languages': herb.get('languages', {}),
                'uses': herb.get('uses', ''),
                'properties': herb.get('properties', ''),
                'parts_used': herb.get('parts_used', ''),
                'dosage': herb.get('dosage', ''),
                'precautions': herb.get('precautions', ''),
                'ayush_system': herb.get('ayush_system', ''),
                'remedies': herb.get('remedies', []),
                'therapies': herb.get('therapies', []),
                'related_conditions': herb.get('related_conditions', [])
            }
            
            self.herb_profiles[i] = profile
            
            # Build semantic knowledge text
            knowledge_text = f"""
            {profile['name']} ({profile['scientific_name']}) is a medicinal plant used in {profile['ayush_system']} system.
            Common names: {', '.join(profile['common_names']) if profile['common_names'] else 'None'}.
            Uses: {profile['uses']}.
            Properties: {profile['properties']}.
            Parts used: {profile['parts_used']}.
            Treats conditions: {', '.join(profile['related_conditions']) if profile['related_conditions'] else 'Various'}.
            """
            
            self.semantic_knowledge.append(knowledge_text.strip())
        print("Knowledge base built with {} herbs.",self.semantic_knowledge)
    
    def detect_language_advanced(self, text):
        """Advanced language detection"""
        text = text.strip()
        
        # Check for Devanagari script
        if any('\u0900' <= ch <= '\u097F' for ch in text):
            # Use character-based detection for Hindi vs Marathi
            marathi_chars = set('ळऱवझञ')
            hindi_chars = set('क़ख़ग़ज़ड़ढ़फ़य़')
            
            text_chars = set(text)
            if text_chars & marathi_chars:
                return 'mr'
            elif text_chars & hindi_chars:
                return 'hi'
            else:
                # Use common words for detection
                marathi_words = ['तुळस', 'आळू', 'काळा', 'पिळू']
                hindi_words = ['तुलसी', 'आलू', 'काला', 'पीला']
                
                for word in marathi_words:
                    if word in text:
                        return 'mr'
                for word in hindi_words:
                    if word in text:
                        return 'hi'
                
                return 'hi'  # Default to Hindi
        
        # Try langdetect for other languages
        try:
            detected = detect(text)
            return detected if detected in ['en', 'hi', 'mr'] else 'en'
        except:
            return 'en'
    
    def analyze_intent(self, query, language):
        """Analyze user intent using spaCy and patterns"""
        nlp = self.lang_processor.nlp_models.get(language, self.lang_processor.nlp_models['en'])
        doc = nlp(query.lower())
        
        # Extract entities
        entities = {
            'symptoms': [],
            'body_parts': [],
            'herbs': [],
            'conditions': []
        }
        
        # Define entity patterns
        symptom_keywords = {
            'en': ['pain', 'ache', 'stress', 'anxiety', 'depression', 'fever', 'cold', 'cough', 'headache'],
            'hi': ['दर्द', 'तनाव', 'चिंता', 'बुखार', 'सर्दी', 'खांसी', 'सिरदर्द'],
            'mr': ['वेदना', 'ताण', 'चिंता', 'ताप', 'सर्दी', 'खोकला', 'डोकेदुखी']
        }
        
        body_parts = {
            'en': ['head', 'stomach', 'chest', 'back', 'joints', 'skin', 'hair', 'heart', 'liver', 'kidney'],
            'hi': ['सिर', 'पेट', 'छाती', 'पीठ', 'जोड़', 'त्वचा', 'बाल', 'दिल', 'यकृत', 'गुर्दा'],
            'mr': ['डोके', 'पोट', 'छाती', 'पाठ', 'सांधे', 'त्वचा', 'केस', 'हृदय', 'यकृत', 'मूत्रपिंड']
        }
        
        # Extract entities based on keywords
        query_lower = query.lower()
        lang_symptoms = symptom_keywords.get(language, symptom_keywords['en'])
        lang_body_parts = body_parts.get(language, body_parts['en'])
        
        for symptom in lang_symptoms:
            if symptom in query_lower:
                entities['symptoms'].append(symptom)
        
        for part in lang_body_parts:
            if part in query_lower:
                entities['body_parts'].append(part)
        
        # Determine intent
        intent = 'general_query'
        confidence = 0.5
        
        if entities['symptoms']:
            intent = 'symptom_treatment'
            confidence = 0.9
        elif any(word in query_lower for word in ['suggest', 'recommend', 'advise', 'सुझाव', 'सल्ला']):
            intent = 'recommendation_request'
            confidence = 0.8
        elif any(word in query_lower for word in ['what is', 'tell me', 'information', 'क्या है', 'काय आहे']):
            intent = 'herb_information'
            confidence = 0.8
        elif len(query.split()) <= 2:
            intent = 'herb_search'
            confidence = 0.7
        
        return {
            'intent': intent,
            'confidence': confidence,
            'entities': entities,
            'language': language
        }
    
    def debug_herb_database(self):
        """Debug method to check herb database"""
        print(f"=== HERB DATABASE DEBUG ===")
        print(f"Total herbs loaded: {len(self.herbs_data) if self.herbs_data else 0}")
        
        if self.herbs_data:
            print(f"First 3 herbs:")
            for i, herb in enumerate(self.herbs_data[:3]):
                print(f"  {i+1}. Name: {herb.get('name', 'NO_NAME')}")
                print(f"     Alt names: {herb.get('alt_names', [])}")
                print(f"     Languages: {herb.get('languages', {})}")
                print(f"     Uses: {str(herb.get('uses', ''))[:100]}...")
                print()
            
            # Test immunity herbs specifically
            immunity_herbs = ['tulsi', 'giloy', 'amla', 'turmeric', 'ginger']
            print(f"Checking for immunity herbs:")
            for herb_name in immunity_herbs:
                found = self._find_herb_by_name_enhanced(herb_name)
                print(f"  {herb_name}: {'FOUND' if found else 'NOT FOUND'}")
                if found:
                    print(f"    -> {found.get('name', 'NO_NAME')}")
        else:
            print("No herbs data available!")
        
        print(f"Symptom mappings available: {len(self.symptom_herb_mapping)}")
        print(f"Immunity mapping: {self.symptom_herb_mapping.get('immunity', 'NOT FOUND')}")
        print(f"=== END DEBUG ===\n")
    
    def find_relevant_herbs(self, intent_data):
        """Find herbs based on intent analysis - IMPROVED DEBUG VERSION"""
        print(f"\n=== FINDING RELEVANT HERBS ===")
        
        # First, debug the database
        if not hasattr(self, '_debug_done'):
            self.debug_herb_database()
            self._debug_done = True
        
        intent = intent_data['intent']
        entities = intent_data['entities']
        language = intent_data['language']
        query = intent_data['original_query'].lower()
        
        print(f"Intent: {intent}")
        print(f"Query: '{query}'")
        print(f"Language: {language}")
        print(f"Entities: {entities}")
        
        relevant_herbs = []
        
        # Check if we have herbs data
        if not self.herbs_data:
            print("ERROR: No herbs data available!")
            return []
        
        # Method 1: Check immunity specifically first
        if 'immunity' in query or 'immune' in query:
            print("IMMUNITY QUERY DETECTED")
            immunity_herbs = ['tulsi', 'giloy', 'amla', 'turmeric', 'ginger', 'neem']
            for herb_name in immunity_herbs:
                herb_obj = self._find_herb_by_name_simple(herb_name)
                if herb_obj:
                    relevant_herbs.append(herb_obj)
                    print(f"Found immunity herb: {herb_obj.get('name', 'UNKNOWN')}")
            
            if relevant_herbs:
                print(f"Returning {len(relevant_herbs)} immunity herbs")
                return relevant_herbs[:5]
        
        # Method 2: Enhanced keyword matching
        health_keywords = {
            'energy': ['energy', 'stamina', 'vigor', 'ऊर्जा', 'शक्ति', 'बल'],
            'immunity': ['immunity', 'immune', 'रोग प्रतिरोधक', 'प्रतिरक्षा'],
            'stress': ['stress', 'tension', 'तनाव', 'चिंता'],
            'cold': ['cold', 'सर्दी', 'जुकाम'],
            'cough': ['cough', 'खांसी', 'खोकला'],
            'fever': ['fever', 'बुखार', 'ताप'],
            'digestion': ['digestion', 'पाचन', 'अपच'],
            'skin': ['skin', 'त्वचा', 'तवचा'],
            'hair': ['hair', 'बाल', 'केस']
        }
        
        print("Checking health keywords...")
        for condition, keywords in health_keywords.items():
            for keyword in keywords:
                if keyword in query:
                    print(f"Found keyword '{keyword}' for condition '{condition}'")
                    condition_herbs = self.symptom_herb_mapping.get(condition, [])
                    print(f"Mapped to herbs: {condition_herbs}")
                    
                    for herb_name in condition_herbs:
                        herb_obj = self._find_herb_by_name_simple(herb_name)
                        if herb_obj:
                            relevant_herbs.append(herb_obj)
                            print(f"Added herb: {herb_obj.get('name', 'UNKNOWN')}")
                    
                    if relevant_herbs:
                        return relevant_herbs[:5]
        
        # Method 3: Direct herb name search
        print("Trying direct herb name search...")
        common_herbs = {
            'tulsi': ['tulsi', 'तुलसी', 'तुळशी', 'holy basil'],
            'ashwagandha': ['ashwagandha', 'अश्वगंधा', 'winter cherry'],
            'turmeric': ['turmeric', 'haldi', 'हल्दी', 'हळद'],
            'ginger': ['ginger', 'adrak', 'अदरक', 'आले'],
            'amla': ['amla', 'आंवला', 'आवळा', 'indian gooseberry'],
            'neem': ['neem', 'नीम', 'कडुनिंब'],
            'giloy': ['giloy', 'गिलोय', 'गुडुची'],
            'brahmi': ['brahmi', 'ब्राह्मी'],
            'ashoka': ['ashoka', 'अशोक', 'अशोका']
        }
        
        for english_name, variations in common_herbs.items():
            for variation in variations:
                if variation in query:
                    print(f"Found herb variation '{variation}' -> '{english_name}'")
                    herb_obj = self._find_herb_by_name_simple(english_name)
                    if herb_obj:
                        relevant_herbs.append(herb_obj)
                        print(f"Added herb: {herb_obj.get('name', 'UNKNOWN')}")
                        return [herb_obj]  # Return immediately for direct herb queries
        
        # Method 4: Fallback - return some popular herbs
        if not relevant_herbs:
            print("Using fallback popular herbs...")
            popular_herbs = ['tulsi', 'ashwagandha', 'turmeric', 'ginger', 'amla']
            for herb_name in popular_herbs:
                herb_obj = self._find_herb_by_name_simple(herb_name)
                if herb_obj:
                    relevant_herbs.append(herb_obj)
                    print(f"Added fallback herb: {herb_obj.get('name', 'UNKNOWN')}")
        
        print(f"Final herbs found: {len(relevant_herbs)}")
        return relevant_herbs[:5]
    
    def _find_herb_by_name_simple(self, herb_name):
        """Simplified herb finder for debugging"""
        if not herb_name or not self.herbs_data:
            return None
        
        herb_name_lower = herb_name.lower().strip()
        print(f"Searching for herb: '{herb_name_lower}'")
        
        # Try exact match first
        for herb in self.herbs_data:
            main_name = herb.get('name', '').lower().strip()
            if main_name == herb_name_lower:
                print(f"Exact match found: {herb.get('name', 'UNKNOWN')}")
                return herb
        
        # Try partial match
        for herb in self.herbs_data:
            main_name = herb.get('name', '').lower().strip()
            if herb_name_lower in main_name or main_name in herb_name_lower:
                print(f"Partial match found: {herb.get('name', 'UNKNOWN')}")
                return herb
            
            # Check alt names
            alt_names = herb.get('alt_names', [])
            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    if alt_name and herb_name_lower in alt_name.lower():
                        print(f"Alt name match found: {alt_name} -> {herb.get('name', 'UNKNOWN')}")
                        return herb
        
        print(f"No match found for: '{herb_name_lower}'")
        return None

    # Also add this method to check what herbs are actually in your database
    def list_available_herbs(self):
        """List all herbs in the database for debugging"""
        if not self.herbs_data:
            return []
        
        herb_names = []
        for herb in self.herbs_data:
            name = herb.get('name', 'UNNAMED')
            herb_names.append(name)
        
        return sorted(herb_names)

    def generate_contextual_response(self, query, relevant_herbs, intent_data):
        """Generate AI-like contextual response"""
        language = intent_data['language']
        intent = intent_data['intent']
        entities = intent_data['entities']
        
        if not relevant_herbs:
            return self._generate_no_results_response(query, language)
        
        # Generate response based on intent
        if intent == 'symptom_treatment':
            response = self._generate_symptom_treatment_response(relevant_herbs, entities, language)
        elif intent == 'herb_information':
            response = self._generate_herb_information_response(relevant_herbs, language)
        elif intent == 'recommendation_request':
            response = self._generate_recommendation_response(relevant_herbs, entities, language)
        else:
            response = self._generate_general_response(relevant_herbs, language)
        
        # Add AI personality and safety disclaimer
        response = self._add_ai_personality(response, language)
        response += self._get_safety_disclaimer(language)
        
        return response
    
    def _generate_symptom_treatment_response(self, herbs, entities, language):
        """Generate response for symptom treatment queries"""
        symptoms = entities['symptoms']
        
        templates = {
            'en': {
                'intro': "Based on traditional AYUSH knowledge, here are some herbs that may help with {}:",
                'herb_format': "🌿 **{}** ({})\n   • Uses: {}\n   • Preparation: {}\n   • Precautions: {}\n",
                'outro': "\nThese are traditional remedies used in {} system."
            },
            'hi': {
                'intro': "पारंपरिक आयुष ज्ञान के आधार पर, {} के लिए ये जड़ी-बूटियां सहायक हो सकती हैं:",
                'herb_format': "🌿 **{}** ({})\n   • उपयोग: {}\n   • तैयारी: {}\n   • सावधानियां: {}\n",
                'outro': "\nये {} पद्धति में उपयोग होने वाले पारंपरिक उपचार हैं।"
            },
            'mr': {
                'intro': "पारंपरिक आयुष ज्ञानाच्या आधारे, {} साठी ही औषधी वनस्पती उपयुक्त असू शकतात:",
                'herb_format': "🌿 **{}** ({})\n   • उपयोग: {}\n   • तयारी: {}\n   • खबरदारी: {}\n",
                'outro': "\nहे {} पद्धतीमधील पारंपरिक उपचार आहेत।"
            }
        }
        
        template = templates.get(language, templates['en'])
        
        # Build response
        symptom_text = ', '.join(symptoms) if symptoms else 'आपकी समस्या'
        response = template['intro'].format(symptom_text) + "\n\n"
        
        for herb in herbs[:3]:  # Limit to 3 herbs
            herb_name = self._get_herb_name_in_language(herb, language)
            scientific_name = herb.get('scientific_name', 'N/A')
            uses = self._get_herb_uses_in_language(herb, language)
            preparation = self._get_preparation_info(herb, language)
            precautions = self._get_precautions_in_language(herb, language)
            
            response += template['herb_format'].format(
                herb_name, scientific_name, uses, preparation, precautions
            )
        
        # Add system info
        systems = list(set([herb.get('ayush_system', 'AYUSH') for herb in herbs]))
        response += template['outro'].format(', '.join(systems))
        
        return response
    
    def _generate_herb_information_response(self, herbs, language):
        """Generate detailed information about specific herbs"""
        if len(herbs) == 1:
            return self._generate_detailed_herb_info(herbs[0], language)
        else:
            return self._generate_multiple_herbs_info(herbs, language)
    
    def _generate_detailed_herb_info(self, herb, language):
        """Generate detailed information for a single herb"""
        templates = {
            'en': """🌿 **{}** ({})

**AYUSH System**: {}
**Parts Used**: {}
**Properties**: {}

**Primary Uses**:
{}

**Traditional Preparations**:
{}

**Precautions**: {}

**Related Conditions**: {}
""",
            'hi': """🌿 **{}** ({})

**आयुष पद्धति**: {}
**उपयोगी भाग**: {}
**गुण**: {}

**मुख्य उपयोग**:
{}

**पारंपरिक तैयारी**:
{}

**सावधानियां**: {}

**संबंधित रोग**: {}
""",
            'mr': """🌿 **{}** ({})

**आयुष पद्धती**: {}
**वापरण्याचे भाग**: {}
**गुणधर्म**: {}

**मुख्य उपयोग**:
{}

**पारंपरिक तयारी**:
{}

**खबरदारी**: {}

**संबंधित आजार**: {}
"""
        }
        
        template = templates.get(language, templates['en'])
        
        herb_name = self._get_herb_name_in_language(herb, language)
        scientific_name = herb.get('scientific_name', 'N/A')
        ayush_system = herb.get('ayush_system', 'AYUSH')
        parts_used = herb.get('parts_used', 'N/A')
        properties = herb.get('properties', 'N/A')
        uses = self._format_uses(herb.get('uses', ''), language)
        preparations = self._format_preparations(herb.get('remedies', []), language)
        precautions = herb.get('precautions', 'कोई विशेष सावधानी नहीं')
        conditions = ', '.join(herb.get('related_conditions', []))
        
        return template.format(
            herb_name, scientific_name, ayush_system, parts_used, properties,
            uses, preparations, precautions, conditions
        )
    
    def _generate_no_results_response(self, query, language):
        """Generate response when no relevant herbs found"""
        responses = {
            'en': f"""I understand you're asking about "{query}", but I couldn't find specific herbal information related to this query in my knowledge base.

Could you please:
• Rephrase your question more specifically
• Mention specific symptoms or conditions
• Try using common names for herbs
• Ask about general health concerns

For example: "herbs for stress relief" or "what is tulsi used for"

I'm here to help with traditional AYUSH medicinal plants and their uses!""",
            
            'hi': f"""मैं समझ गया कि आप "{query}" के बारे में पूछ रहे हैं, लेकिन मुझे अपने ज्ञान आधार में इससे संबंधित जानकारी नहीं मिली।

कृपया आप:
• अपना प्रश्न अधिक स्पष्ट रूप से पूछें
• विशिष्ट लक्षण या समस्याओं का उल्लेख करें
• जड़ी-बूटियों के सामान्य नामों का उपयोग करें
• सामान्य स्वास्थ्य संबंधी चिंताओं के बारे में पूछें

उदाहरण: "तनाव के लिए जड़ी बूटी" या "तुलसी का क्या उपयोग है"

मैं पारंपरिक आयुष औषधीय पौधों की जानकारी देने के लिए यहां हूं!""",
            
            'mr': f"""मला समजले की तुम्ही "{query}" बद्दल विचारत आहात, पण माझ्या ज्ञान आधारात याशी संबंधित माहिती सापडली नाही।

कृपया तुम्ही:
• तुमचा प्रश्न अधिक स्पष्टपणे विचारा
• विशिष्ट लक्षणे किंवा समस्यांचा उल्लेख करा
• औषधी वनस्पतींची सामान्य नावे वापरा
• सामान्य आरोग्य समस्यांबद्दल विचारा

उदाहरण: "तणावासाठी औषधी वनस्पती" किंवा "तुळशीचा काय उपयोग आहे"

मी पारंपरिक आयुष औषधी वनस्पतींची माहिती देण्यासाठी येथे आहे!"""
        }
        
        return responses.get(language, responses['en'])
    
    def _add_ai_personality(self, response, language):
        """Add AI personality to make responses more conversational"""
        personality_prefixes = {
            'en': [
                "Based on traditional AYUSH wisdom, ",
                "From my knowledge of medicinal plants, ",
                "According to traditional herbal medicine, ",
                "In AYUSH systems, "
            ],
            'hi': [
                "पारंपरिक आयुष ज्ञान के अनुसार, ",
                "औषधीय पौधों के मेरे ज्ञान से, ",
                "पारंपरिक हर्बल चिकित्सा के अनुसार, ",
                "आयुष पद्धतियों में, "
            ],
            'mr': [
                "पारंपरिक आयुष ज्ञानानुसार, ",
                "औषधी वनस्पतींच्या माझ्या ज्ञानावरून, ",
                "पारंपरिक वनौषधी उपचारानुसार, ",
                "आयुष पद्धतींमध्ये, "
            ]
        }
        
        # Don't add prefix if response already starts with one
        prefixes = personality_prefixes.get(language, personality_prefixes['en'])
        if not any(response.startswith(prefix) for prefix in prefixes):
            prefix = np.random.choice(prefixes)
            response = prefix + response
        
        return response
    
    def _get_safety_disclaimer(self, language):
        """Get safety disclaimer in appropriate language"""
        disclaimers = {
            'en': "\n\n⚠️ **Important**: This information is for educational purposes only. Please consult qualified healthcare practitioners before starting any herbal treatment, especially if you have existing medical conditions or are taking medications.",
            
            'hi': "\n\n⚠️ **महत्वपूर्ण**: यह जानकारी केवल शैक्षिक उद्देश्यों के लिए है। कोई भी हर्बल उपचार शुरू करने से पहले योग्य चिकित्सा विशेषज्ञों से सलाह लें, विशेषकर यदि आपकी कोई मौजूदा बीमारी है या आप दवाएं ले रहे हैं।",
            
            'mr': "\n\n⚠️ **महत्त्वाचे**: ही माहिती केवळ शैक्षणिक हेतूंसाठी आहे। कोणताही वनौषधी उपचार सुरू करण्यापूर्वी योग्य आरोग्य तज्ञांचा सल्ला घ्या, विशेषतः जर तुमच्याकडे विद्यमान वैद्यकीय समस्या असतील किंवा तुम्ही औषधे घेत असाल."
        }
        
        return disclaimers.get(language, disclaimers['en'])
    
    def _search_herbs_by_name(self, query):
        """Search herbs by name with fuzzy matching"""
        query_normalized = unicodedata.normalize("NFKC", query.lower().strip())
        matches = []
        
        for herb in self.herbs_data:
            # Check main name
            if query_normalized in herb.get('name', '').lower():
                matches.append(herb.get('name', ''))
            
            # Check alternative names
            alt_names = herb.get('alt_names', [])
            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    if query_normalized in alt_name.lower():
                        matches.append(herb.get('name', ''))
                        break
            
            # Check multilingual names
            languages = herb.get('languages', {})
            if isinstance(languages, dict):
                for lang_name in languages.values():
                    if lang_name and query_normalized in lang_name.lower():
                        matches.append(herb.get('name', ''))
                        break
        
        return list(set(matches))[:5]
    
    def _find_herb_by_name(self, herb_name):
        """Find herb object by name"""
        herb_name_lower = herb_name.lower()
        
        for herb in self.herbs_data:
            if herb.get('name', '').lower() == herb_name_lower:
                return herb
            
            # Check alternative names
            alt_names = herb.get('alt_names', [])
            if isinstance(alt_names, list):
                for alt_name in alt_names:
                    if alt_name.lower() == herb_name_lower:
                        return herb
        
        return None
    
    def _get_herb_name_in_language(self, herb, language):
        """Get herb name in specified language"""
        if language in ['hi', 'mr']:
            languages = herb.get('languages', {})
            if isinstance(languages, dict) and language in languages:
                return languages[language]
            
# Add this endpoint to your search.py file, after the existing code

@search_bp.route('/query', methods=['POST'])
def ai_query():
    """
    Main AI query endpoint that the frontend calls.
    Processes natural language queries and returns AI-generated responses.
    """
    try:
        # Check if AI system is initialized
        if not ai_herbal_system or not ai_session_manager:
            return jsonify({
                'success': False,
                'error': 'AI system not initialized. Please restart the server.',
                'ai_response': 'I apologize, but my knowledge base is currently unavailable. Please try again later.'
            }), 500
        
        # Get request data
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                'success': False,
                'error': 'No query provided',
                'ai_response': 'Please provide a query to search for herbal information.'
            }), 400
        
        query = data['query'].strip()
        if not query:
            return jsonify({
                'success': False,
                'error': 'Empty query provided',
                'ai_response': 'Please ask me something about herbs or health concerns.'
            }), 400
        
        print(f"Processing AI query: {query}")
        
        # Get user context for personalized responses
        request_info = {
            'remote_addr': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', '')
        }
        
        user_context = ai_session_manager.get_user_context(request_info)
        
        # Process the query through AI system
        ai_response = ai_herbal_system.process_query(query)
        
        # Update session with conversation context
        ai_session_manager.update_session_context(
            user_context['user_id'], 
            query, 
            ai_response
        )
        print(f"AI response data: {ai_response}")
        
        # Format response for frontend
        response_data = {
            'success': True,
            'ai_response': ai_response['response_text'],
            'results': ai_response.get('herbs_data', []),
            'metadata': {
                'intent': ai_response.get('intent', ''),
                'language': ai_response.get('language', 'en'),
                'confidence': ai_response.get('confidence', 0.0),
                'herbs_found': ai_response.get('herbs_found', 0),
                'entities': ai_response.get('entities', {}),
                'user_context': {
                    'session_queries': user_context['total_queries'],
                    'preferred_language': user_context['preferred_language']
                }
            }
        }
        
        print(f"AI query processed successfully. Response length: {len(ai_response['response_text'])} chars")
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error in AI query processing: {str(e)}")
        import traceback
        traceback.print_exc()
        
        # Return user-friendly error response
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}',
            'ai_response': 'I encountered an issue while processing your query. Please try rephrasing your question or contact support if the problem persists.'
        }), 500

# Optional: Add a health check endpoint
@search_bp.route('/health', methods=['GET'])
def health_check():
    """Check if AI system is properly initialized"""
    try:
        if ai_herbal_system and ai_session_manager:
            # Get system stats
            stats = ai_session_manager.get_session_statistics()
            
            return jsonify({
                'status': 'healthy',
                'ai_system_ready': True,
                'herbs_loaded': len(ai_herbal_system.herbs_data) if ai_herbal_system.herbs_data else 0,
                'active_sessions': stats.get('active_sessions', 0),
                'languages_supported': ['en', 'hi', 'mr']
            })
        else:
            return jsonify({
                'status': 'unhealthy',
                'ai_system_ready': False,
                'error': 'AI system not initialized'
            }), 503
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'ai_system_ready': False,
            'error': str(e)
        }), 500