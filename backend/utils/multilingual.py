import re
import logging
from typing import Dict, List, Optional
import json
import os

logger = logging.getLogger(__name__)

class MultilingualProcessor:
    """Multilingual processing service for Hindi, Marathi, and English"""
    
    def __init__(self):
        self.supported_languages = ['en', 'hi', 'mr']
        self.translations = self._load_translations()
        self.transliteration_map = self._load_transliteration_map()
        self.plant_names_map = self._load_plant_names_map()
    
    def _load_translations(self) -> Dict:
        """Load translation dictionaries"""
        return {
            'hi': {
                # Common medical terms
                'pain': 'दर्द',
                'headache': 'सिरदर्द',
                'stomach': 'पेट',
                'fever': 'बुखार',
                'cough': 'खांसी',
                'cold': 'सर्दी',
                'skin': 'त्वचा',
                'joint': 'जोड़',
                'back': 'पीठ',
                'chest': 'छाती',
                'throat': 'गला',
                'eye': 'आंख',
                'ear': 'कान',
                'nose': 'नाक',
                'tooth': 'दांत',
                'mouth': 'मुंह',
                'hand': 'हाथ',
                'foot': 'पैर',
                'leg': 'पैर',
                'arm': 'बांह',
                
                # Symptoms
                'swelling': 'सूजन',
                'inflammation': 'सूजन',
                'infection': 'संक्रमण',
                'allergy': 'एलर्जी',
                'weakness': 'कमजोरी',
                'fatigue': 'थकान',
                'stress': 'तनाव',
                'anxiety': 'चिंता',
                'depression': 'अवसाद',
                'insomnia': 'अनिद्रा',
                'constipation': 'कब्ज',
                'diarrhea': 'दस्त',
                'acidity': 'अम्लता',
                'gas': 'गैस',
                'bloating': 'पेट फूलना',
                'nausea': 'मतली',
                'vomiting': 'उल्टी',
                
                # Common herbs (Hindi names)
                'turmeric': 'हल्दी',
                'ginger': 'अदरक',
                'garlic': 'लहसुन',
                'onion': 'प्याज',
                'neem': 'नीम',
                'tulsi': 'तुलसी',
                'ashwagandha': 'अश्वगंधा',
                'brahmi': 'ब्राह्मी',
                'amla': 'आंवला',
                'triphala': 'त्रिफला',
                'giloy': 'गिलोय',
                'fenugreek': 'मेथी',
                'cumin': 'जीरा',
                'coriander': 'धनिया',
                'fennel': 'सौंफ',
                'cardamom': 'इलायची',
                'cinnamon': 'दालचीनी',
                'cloves': 'लौंग',
                'black pepper': 'काली मिर्च',
                
                # Action words
                'cure': 'इलाज',
                'treatment': 'उपचार',
                'remedy': 'उपाय',
                'medicine': 'दवा',
                'herb': 'जड़ी-बूटी',
                'natural': 'प्राकृतिक',
                'ayurvedic': 'आयुर्वेदिक',
                'help': 'मदद',
                'relief': 'राहत',
                'healing': 'चिकित्सा'
            },
            
            'mr': {
                # Common medical terms
                'pain': 'दुखणे',
                'headache': 'डोकेदुखी',
                'stomach': 'पोट',
                'fever': 'ताप',
                'cough': 'खोकला',
                'cold': 'सर्दी',
                'skin': 'त्वचा',
                'joint': 'सांधे',
                'back': 'पाठ',
                'chest': 'छाती',
                'throat': 'घसा',
                'eye': 'डोळा',
                'ear': 'कान',
                'nose': 'नाक',
                'tooth': 'दात',
                'mouth': 'तोंड',
                'hand': 'हात',
                'foot': 'पाय',
                'leg': 'पाय',
                'arm': 'हात',
                
                # Symptoms
                'swelling': 'सूज',
                'inflammation': 'दाह',
                'infection': 'संसर्ग',
                'allergy': 'ऍलर्जी',
                'weakness': 'अशक्तपणा',
                'fatigue': 'थकवा',
                'stress': 'तणाव',
                'anxiety': 'चिंता',
                'depression': 'नैराश्य',
                'insomnia': 'निद्रानाश',
                'constipation': 'बद्धकोष्ठता',
                'diarrhea': 'जुलाब',
                'acidity': 'आम्लता',
                'gas': 'वायू',
                'bloating': 'पोट फुगणे',
                'nausea': 'मळमळ',
                'vomiting': 'उलटी',
                
                # Common herbs (Marathi names)
                'turmeric': 'हळद',
                'ginger': 'आले',
                'garlic': 'लसूण',
                'onion': 'कांदा',
                'neem': 'कडुनिंब',
                'tulsi': 'तुळस',
                'ashwagandha': 'अश्वगंधा',
                'brahmi': 'ब्राह्मी',
                'amla': 'आवळा',
                'triphala': 'त्रिफळा',
                'giloy': 'गुडुची',
                'fenugreek': 'मेथी',
                'cumin': 'जिरे',
                'coriander': 'धणे',
                'fennel': 'बडीशेप',
                'cardamom': 'वेलची',
                'cinnamon': 'दालचिनी',
                'cloves': 'लवंग',
                'black pepper': 'काळी मिरी',
                
                # Action words
                'cure': 'इलाज',
                'treatment': 'उपचार',
                'remedy': 'उपाय',
                'medicine': 'औषध',
                'herb': 'औषधी वनस्पती',
                'natural': 'नैसर्गिक',
                'ayurvedic': 'आयुर्वेदिक',
                'help': 'मदत',
                'relief': 'आराम',
                'healing': 'उपचार'
            }
        }
    
    def _load_transliteration_map(self) -> Dict:
        """Load transliteration mappings for common plant names"""
        return {
            'hi': {
                # English to Hindi transliteration
                'haldi': 'हल्दी',
                'adrak': 'अदरक',
                'lahsun': 'लहसुन',
                'pyaz': 'प्याज',
                'neem': 'नीम',
                'tulsi': 'तुलसी',
                'amla': 'आंवला',
                'methi': 'मेथी',
                'jeera': 'जीरा',
                'dhania': 'धनिया',
                'saunf': 'सौंफ',
                'elaichi': 'इलायची',
                'dalchini': 'दालचीनी',
                'laung': 'लौंग',
                'kali mirch': 'काली मिर्च'
            },
            'mr': {
                # English to Marathi transliteration
                'halad': 'हळद',
                'ale': 'आले',
                'lasun': 'लसूण',
                'kanda': 'कांदा',
                'kadunimb': 'कडुनिंब',
                'tulas': 'तुळस',
                'avala': 'आवळा',
                'methi': 'मेथी',
                'jire': 'जिरे',
                'dhane': 'धणे',
                'badishep': 'बडीशेप',
                'velchi': 'वेलची',
                'dalchini': 'दालचिनी',
                'lavang': 'लवंग',
                'kali miri': 'काळी मिरी'
            }
        }
    
    def _load_plant_names_map(self) -> Dict:
        """Load comprehensive plant names mapping"""
        return {
            'turmeric': {
                'hi': ['हल्दी', 'हरिद्रा'],
                'mr': ['हळद'],
                'en': ['turmeric', 'curcuma', 'haldi']
            },
            'neem': {
                'hi': ['नीम', 'निम्ब'],
                'mr': ['कडुनिंब', 'नीम'],
                'en': ['neem', 'margosa', 'azadirachta']
            },
            'tulsi': {
                'hi': ['तुलसी', 'वृंदा'],
                'mr': ['तुळस'],
                'en': ['tulsi', 'holy basil', 'ocimum']
            },
            'ginger': {
                'hi': ['अदरक', 'आद्रक'],
                'mr': ['आले'],
                'en': ['ginger', 'adrak', 'zingiber']
            },
            'amla': {
                'hi': ['आंवला', 'आमलकी'],
                'mr': ['आवळा'],
                'en': ['amla', 'gooseberry', 'emblica']
            }
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of the input text"""
        # Simple heuristic-based language detection
        
        # Check for Devanagari script (Hindi/Marathi)
        devanagari_chars = re.findall(r'[\u0900-\u097F]', text)
        
        if devanagari_chars:
            # Try to distinguish between Hindi and Marathi
            marathi_indicators = ['आवळा', 'हळद', 'आले', 'कडुनिंब', 'तुळस']
            hindi_indicators = ['आंवला', 'हल्दी', 'अदरक', 'नीम', 'तुलसी']
            
            marathi_count = sum(1 for indicator in marathi_indicators if indicator in text)
            hindi_count = sum(1 for indicator in hindi_indicators if indicator in text)
            
            if marathi_count > hindi_count:
                return 'mr'
            else:
                return 'hi'
        
        return 'en'
    
    def translate_to_english(self, text: str, source_lang: str) -> str:
        """Translate text from source language to English"""
        if source_lang == 'en':
            return text
        
        if source_lang not in self.translations:
            logger.warning(f"Unsupported source language: {source_lang}")
            return text
        
        translated_text = text.lower()
        translation_dict = self.translations[source_lang]
        
        # Reverse translation dictionary (target -> source)
        reverse_dict = {v: k for k, v in translation_dict.items()}
        
        # Replace terms
        for native_term, english_term in reverse_dict.items():
            if native_term in translated_text:
                translated_text = translated_text.replace(native_term, english_term)
        
        # Handle transliteration
        if source_lang in self.transliteration_map:
            for romanized, native in self.transliteration_map[source_lang].items():
                if romanized in translated_text:
                    # Find English equivalent
                    for plant, names in self.plant_names_map.items():
                        if native in names[source_lang]:
                            translated_text = translated_text.replace(romanized, plant)
                            break
        
        return translated_text
    
    def translate_from_english(self, text: str, target_lang: str) -> str:
        """Translate text from English to target language"""
        if target_lang == 'en':
            return text
        
        if target_lang not in self.translations:
            logger.warning(f"Unsupported target language: {target_lang}")
            return text
        
        translated_text = text
        translation_dict = self.translations[target_lang]
        
        # Replace English terms with target language terms
        for english_term, native_term in translation_dict.items():
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(english_term) + r'\b'
            translated_text = re.sub(pattern, native_term, translated_text, flags=re.IGNORECASE)
        
        return translated_text
    
    def normalize_plant_name(self, plant_name: str, source_lang: str = None) -> str:
        """Normalize plant name to standard English name"""
        if not source_lang:
            source_lang = self.detect_language(plant_name)
        
        plant_name_lower = plant_name.lower().strip()
        
        # Check in plant names mapping
        for standard_name, names_dict in self.plant_names_map.items():
            for lang, variations in names_dict.items():
                if plant_name_lower in [v.lower() for v in variations]:
                    return standard_name
        
        # Fallback: translate using general translation dictionary
        if source_lang != 'en' and source_lang in self.translations:
            reverse_dict = {v.lower(): k for k, v in self.translations[source_lang].items()}
            if plant_name_lower in reverse_dict:
                return reverse_dict[plant_name_lower]
        
        return plant_name
    
    def get_local_plant_names(self, english_name: str, target_lang: str) -> List[str]:
        """Get local names for a plant in target language"""
        english_name_lower = english_name.lower()
        
        # Check in comprehensive plant mapping
        for plant, names_dict in self.plant_names_map.items():
            if plant.lower() == english_name_lower or english_name_lower in [n.lower() for n in names_dict.get('en', [])]:
                return names_dict.get(target_lang, [])
        
        # Fallback: check in general translation dictionary
        if target_lang in self.translations:
            translation_dict = self.translations[target_lang]
            if english_name_lower in translation_dict:
                return [translation_dict[english_name_lower]]
        
        return [english_name]  # Return original if no translation found
    
    def preprocess_query(self, query: str, source_lang: str = None) -> Dict:
        """Preprocess multilingual query"""
        if not source_lang:
            source_lang = self.detect_language(query)
        
        # Normalize and translate to English for processing
        english_query = self.translate_to_english(query, source_lang)
        
        # Extract plant names and normalize them
        plant_names = []
        for word in query.split():
            normalized = self.normalize_plant_name(word, source_lang)
            if normalized != word.lower():
                plant_names.append(normalized)
        
        return {
            'original_query': query,
            'detected_language': source_lang,
            'english_query': english_query,
            'extracted_plants': plant_names,
            'normalized_query': english_query
        }
    
    def localize_response(self, response: str, target_lang: str) -> str:
        """Localize response to target language"""
        if target_lang == 'en':
            return response
        
        # Translate the response
        localized = self.translate_from_english(response, target_lang)
        
        # Add language-specific formatting or cultural adaptations
        if target_lang in ['hi', 'mr']:
            # Add respectful addressing common in Indian languages
            if 'recommendation' in response.lower() or 'suggest' in response.lower():
                localized = self._add_cultural_context(localized, target_lang)
        
        return localized
    
    def _add_cultural_context(self, text: str, lang: str) -> str:
        """Add cultural context appropriate for the language"""
        cultural_additions = {
            'hi': {
                'prefix': 'आयुर्वेद के अनुसार, ',
                'suffix': '\n\nकृपया किसी योग्य वैद्य से सलाह लें।'
            },
            'mr': {
                'prefix': 'आयुर्वेदानुसार, ',
                'suffix': '\n\nकृपया योग्य वैद्याचा सल्ला घ्या।'
            }
        }
        
        if lang in cultural_additions:
            addition = cultural_additions[lang]
            # Add prefix for treatment suggestions
            if any(word in text for word in ['उपचार', 'इलाज', 'दवा', 'औषध']):
                text = addition['prefix'] + text
            
            # Add suffix for medical advice
            text += addition['suffix']
        
        return text
    
    def get_translation_confidence(self, original: str, translated: str) -> float:
        """Calculate confidence score for translation"""
        # Simple confidence calculation based on translation coverage
        original_words = set(original.lower().split())
        translated_words = set(translated.lower().split())
        
        if len(original_words) == 0:
            return 0.0
        
        # Check how many words were actually translated
        unchanged_words = original_words.intersection(translated_words)
        coverage = 1.0 - (len(unchanged_words) / len(original_words))
        
        return min(coverage, 1.0)