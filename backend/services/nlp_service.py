import spacy
import re
from typing import List, Dict, Tuple
import logging
from collections import defaultdict

logger = logging.getLogger(__name__)

class NLPService:
    """Natural Language Processing service for herbal queries"""
    
    def __init__(self):
        self.nlp = None
        self.symptom_keywords = self._load_symptom_keywords()
        self.herb_keywords = self._load_herb_keywords()
        self.ayush_systems = ['ayurveda', 'siddha', 'unani', 'homeopathy', 'yoga', 'naturopathy']
        self._load_model()
    
    def _load_model(self):
        """Load spaCy model with fallback options"""
        try:
            # Try to load English model
            self.nlp = spacy.load("en_core_web_sm")
            logger.info("Loaded spaCy en_core_web_sm model")
        except OSError:
            try:
                # Fallback to basic English model
                self.nlp = spacy.load("en_core_web_md")
                logger.info("Loaded spaCy en_core_web_md model")
            except OSError:
                # Create blank model if no pre-trained model available
                self.nlp = spacy.blank("en")
                logger.warning("Using blank spaCy model - limited functionality")
    
    def _load_symptom_keywords(self) -> Dict[str, List[str]]:
        """Load symptom keywords mapping"""
        return {
            'pain': [
                'pain', 'ache', 'aching', 'hurt', 'hurting', 'sore', 'soreness',
                'joint pain', 'back pain', 'headache', 'muscle pain', 'arthritis'
            ],
            'digestive': [
                'indigestion', 'stomach', 'gastric', 'acidity', 'bloating',
                'constipation', 'diarrhea', 'nausea', 'vomiting', 'appetite'
            ],
            'respiratory': [
                'cough', 'cold', 'fever', 'bronchitis', 'asthma', 'breathing',
                'throat', 'sinus', 'congestion', 'phlegm'
            ],
            'skin': [
                'skin', 'rash', 'eczema', 'acne', 'wound', 'cut', 'burn',
                'psoriasis', 'dermatitis', 'itching', 'allergy'
            ],
            'mental': [
                'stress', 'anxiety', 'depression', 'insomnia', 'sleep',
                'mood', 'mental', 'nervous', 'tension', 'worry'
            ],
            'immune': [
                'immunity', 'infection', 'bacterial', 'viral', 'fungal',
                'inflammation', 'swelling', 'fever', 'weakness'
            ]
        }
    
    def _load_herb_keywords(self) -> Dict[str, List[str]]:
        """Load common herb name variations"""
        return {
            'turmeric': ['turmeric', 'haldi', 'curcuma', 'curcumin'],
            'neem': ['neem', 'margosa', 'azadirachta'],
            'ashwagandha': ['ashwagandha', 'withania', 'winter cherry'],
            'ginger': ['ginger', 'adrak', 'zingiber'],
            'garlic': ['garlic', 'lehsun', 'allium'],
            'tulsi': ['tulsi', 'basil', 'ocimum'],
            'amla': ['amla', 'gooseberry', 'emblica'],
            'brahmi': ['brahmi', 'bacopa', 'water hyssop']
        }
    
    def process_query(self, query: str) -> Dict:
        """Process user query and extract relevant information"""
        try:
            # Clean and normalize query
            cleaned_query = self._clean_query(query)
            
            # Process with spaCy
            doc = self.nlp(cleaned_query)
            
            # Extract entities and keywords
            entities = self._extract_entities(doc)
            symptoms = self._extract_symptoms(cleaned_query)
            herbs = self._extract_herbs(cleaned_query)
            ayush_system = self._extract_ayush_system(cleaned_query)
            intent = self._classify_intent(cleaned_query)
            
            # Extract key phrases
            key_phrases = self._extract_key_phrases(doc)
            
            return {
                'original_query': query,
                'cleaned_query': cleaned_query,
                'entities': entities,
                'symptoms': symptoms,
                'herbs': herbs,
                'ayush_system': ayush_system,
                'intent': intent,
                'key_phrases': key_phrases,
                'tokens': [token.text for token in doc if not token.is_stop and not token.is_punct]
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return {
                'original_query': query,
                'cleaned_query': query,
                'entities': [],
                'symptoms': [],
                'herbs': [],
                'ayush_system': None,
                'intent': 'general',
                'key_phrases': [],
                'tokens': query.split()
            }
    
    def _clean_query(self, query: str) -> str:
        """Clean and normalize the input query"""
        # Convert to lowercase
        query = query.lower().strip()
        
        # Remove extra whitespace
        query = re.sub(r'\s+', ' ', query)
        
        # Handle common variations
        replacements = {
            'joint pain': 'arthritis',
            'stomach pain': 'gastric',
            'head ache': 'headache',
            'back ache': 'backache',
        }
        
        for old, new in replacements.items():
            query = query.replace(old, new)
        
        return query
    
    def _extract_entities(self, doc) -> List[Dict]:
        """Extract named entities from the processed document"""
        entities = []
        for ent in doc.ents:
            entities.append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        return entities
    
    def _extract_symptoms(self, query: str) -> List[str]:
        """Extract symptoms mentioned in the query"""
        symptoms = []
        query_lower = query.lower()
        
        for category, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in query_lower:
                    if keyword not in symptoms:
                        symptoms.append(keyword)
        
        return symptoms
    
    def _extract_herbs(self, query: str) -> List[str]:
        """Extract herb names mentioned in the query"""
        herbs = []
        query_lower = query.lower()
        
        for herb_name, variations in self.herb_keywords.items():
            for variation in variations:
                if variation in query_lower:
                    if herb_name not in herbs:
                        herbs.append(herb_name)
        
        return herbs
    
    def _extract_ayush_system(self, query: str) -> str:
        """Extract AYUSH system mentioned in the query"""
        query_lower = query.lower()
        
        for system in self.ayush_systems:
            if system in query_lower:
                return system
        
        return None
    
    def _classify_intent(self, query: str) -> str:
        """Classify the intent of the user query"""
        query_lower = query.lower()
        
        # Intent patterns
        if any(word in query_lower for word in ['cure', 'treatment', 'remedy', 'heal']):
            return 'treatment'
        elif any(word in query_lower for word in ['what is', 'tell me about', 'information']):
            return 'information'
        elif any(word in query_lower for word in ['how to use', 'dosage', 'preparation']):
            return 'usage'
        elif any(word in query_lower for word in ['side effects', 'contraindication', 'safe']):
            return 'safety'
        elif any(word in query_lower for word in ['find', 'search', 'show me']):
            return 'search'
        else:
            return 'general'
    
    def _extract_key_phrases(self, doc) -> List[str]:
        """Extract key phrases from the document"""
        key_phrases = []
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1:  # Multi-word phrases
                key_phrases.append(chunk.text.lower())
        
        # Extract compound words and important single words
        for token in doc:
            if (token.pos_ in ['NOUN', 'ADJ'] and 
                not token.is_stop and 
                not token.is_punct and 
                len(token.text) > 3):
                key_phrases.append(token.text.lower())
        
        return list(set(key_phrases))  # Remove duplicates
    
    def extract_symptoms_advanced(self, query: str) -> List[Dict]:
        """Advanced symptom extraction with confidence scores"""
        doc = self.nlp(query)
        symptoms = []
        
        for category, keywords in self.symptom_keywords.items():
            for keyword in keywords:
                if keyword in query.lower():
                    # Calculate confidence based on context
                    confidence = self._calculate_symptom_confidence(doc, keyword)
                    symptoms.append({
                        'symptom': keyword,
                        'category': category,
                        'confidence': confidence
                    })
        
        # Sort by confidence
        return sorted(symptoms, key=lambda x: x['confidence'], reverse=True)
    
    def _calculate_symptom_confidence(self, doc, symptom: str) -> float:
        """Calculate confidence score for symptom extraction"""
        confidence = 0.5  # Base confidence
        
        # Check for direct mention
        if symptom in doc.text.lower():
            confidence += 0.3
        
        # Check for context words
        context_words = ['have', 'suffering', 'experiencing', 'feel', 'pain']
        for token in doc:
            if token.text.lower() in context_words:
                confidence += 0.1
                break
        
        # Check for medical context
        medical_words = ['doctor', 'medicine', 'treatment', 'cure', 'heal']
        for token in doc:
            if token.text.lower() in medical_words:
                confidence += 0.1
                break
        
        return min(confidence, 1.0)
    
    def get_query_embeddings(self, query: str) -> List[float]:
        """Get embeddings for the query using spaCy vectors"""
        try:
            doc = self.nlp(query)
            if doc.has_vector:
                return doc.vector.tolist()
            else:
                # Fallback: create simple word-based features
                return self._create_simple_features(query)
        except Exception as e:
            logger.error(f"Error getting embeddings: {str(e)}")
            return self._create_simple_features(query)
    
    def _create_simple_features(self, query: str) -> List[float]:
        """Create simple feature vector when embeddings are not available"""
        features = [0.0] * 100  # 100-dimensional feature vector
        
        # Word count features
        words = query.lower().split()
        features[0] = len(words)
        
        # Symptom category features
        for i, (category, keywords) in enumerate(self.symptom_keywords.items()):
            if i < 20:  # Use first 20 features for symptoms
                for keyword in keywords:
                    if keyword in query.lower():
                        features[i + 10] = 1.0
                        break
        
        # Herb features
        for i, (herb, variations) in enumerate(self.herb_keywords.items()):
            if i < 20:  # Use next 20 features for herbs
                for variation in variations:
                    if variation in query.lower():
                        features[i + 30] = 1.0
                        break
        
        # Intent features
        intents = ['treatment', 'information', 'usage', 'safety', 'search']
        intent = self._classify_intent(query)
        if intent in intents:
            features[50 + intents.index(intent)] = 1.0
        
        return features
    
    def similarity_score(self, query1: str, query2: str) -> float:
        """Calculate similarity between two queries"""
        try:
            doc1 = self.nlp(query1)
            doc2 = self.nlp(query2)
            
            if doc1.has_vector and doc2.has_vector:
                return doc1.similarity(doc2)
            else:
                # Fallback: simple word overlap
                words1 = set(query1.lower().split())
                words2 = set(query2.lower().split())
                intersection = len(words1.intersection(words2))
                union = len(words1.union(words2))
                return intersection / union if union > 0 else 0.0
                
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0