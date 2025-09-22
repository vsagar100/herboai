# File: app/i18n.py
# Enhanced language detection and handling for AYUSH Herbs AI
# Fixed compatibility issues with langdetect

import re
from typing import Optional
from langdetect import detect
from loguru import logger

# Handle different langdetect versions
try:
    from langdetect import LangDetectError
except ImportError:
    # Fallback for older versions
    class LangDetectError(Exception):
        pass

def detect_lang(text: str) -> str:
    """
    Enhanced language detection with Marathi and Hindi script recognition
    Completely offline - no internet required
    """
    if not text or not text.strip():
        return "en"
    
    # Clean text for detection
    cleaned_text = text.strip()
    
    # Check for Devanagari script (Hindi/Marathi)
    devanagari_pattern = re.compile(r'[\u0900-\u097F]')
    devanagari_chars = len(devanagari_pattern.findall(cleaned_text))
    total_chars = len(re.sub(r'\s+', '', cleaned_text))
    
    if total_chars > 0:
        devanagari_ratio = devanagari_chars / total_chars
        
        # If significant Devanagari content, detect Hindi vs Marathi
        if devanagari_ratio > 0.3:
            return detect_hindi_marathi(cleaned_text)
    
    # Use langdetect for other languages (offline library)
    try:
        detected = detect(cleaned_text)
        logger.debug(f"Language detected: {detected} for text: {cleaned_text[:50]}")
        
        # Map detected languages to supported ones
        if detected in ['hi', 'mr']:
            return detected
        elif detected == 'en':
            return 'en'
        else:
            # Default to English for unsupported languages
            return 'en'
            
    except (LangDetectError, Exception) as e:
        logger.warning(f"Language detection failed: {e}, defaulting to English")
        return 'en'

def detect_hindi_marathi(text: str) -> str:
    """
    Distinguish between Hindi and Marathi based on specific markers
    Completely offline - no internet required
    """
    # Marathi-specific words and patterns
    marathi_markers = [
        'काय', 'कसे', 'कुठे', 'केव्हा', 'कोण', 'कश्यासाठी',  # Question words
        'घ्यावे', 'करावे', 'जावे', 'येईल', 'होईल',  # Verb forms
        'साठी', 'मध्ये', 'वर', 'ला', 'ने',  # Postpositions
        'आहे', 'होते', 'असे', 'तसे',  # Common words
        'डोकेदुखी', 'औषध', 'वनस्पती', 'उपचार',  # Health-related terms
        'तुळस', 'कडुनिंब', 'हळद', 'आले'  # Herb names in Marathi
    ]
    
    # Hindi-specific words and patterns  
    hindi_markers = [
        'क्या', 'कैसे', 'कहाँ', 'कब', 'कौन', 'क्यों',  # Question words
        'लेना', 'करना', 'जाना', 'आएगा', 'होगा',  # Verb forms
        'के लिए', 'में', 'पर', 'को', 'से',  # Postpositions
        'है', 'था', 'ऐसे', 'वैसे',  # Common words
        'सिरदर्द', 'दवा', 'जड़ी', 'इलाज',  # Health-related terms
        'तुलसी', 'नीम', 'हल्दी', 'अदरक'  # Herb names in Hindi
    ]
    
    marathi_score = sum(1 for marker in marathi_markers if marker in text)
    hindi_score = sum(1 for marker in hindi_markers if marker in text)
    
    logger.debug(f"Language scoring - Marathi: {marathi_score}, Hindi: {hindi_score}")
    
    if marathi_score > hindi_score:
        return 'mr'
    elif hindi_score > marathi_score:
        return 'hi'
    else:
        # If unclear, try langdetect as fallback
        try:
            detected = detect(text)
            return 'mr' if detected == 'mr' else 'hi'
        except:
            return 'hi'  # Default to Hindi if still unclear

def get_language_name(lang_code: str) -> str:
    """Get human-readable language name"""
    names = {
        'en': 'English',
        'hi': 'हिंदी',
        'mr': 'मराठी'
    }
    return names.get(lang_code, 'English')

def get_no_results_message(lang: str) -> str:
    """Get 'no results' message in appropriate language without translation"""
    messages = {
        "en": "I couldn't find relevant herbal information for your question. Please try rephrasing or ask about specific herbs.",
        "hi": "मुझे आपके प्रश्न के लिए प्रासंगिक जड़ी-बूटी की जानकारी नहीं मिली। कृपया पुनः प्रयास करें या किसी विशिष्ट जड़ी-बूटी के बारे में पूछें।",
        "mr": "मला तुमच्या प्रश्नासाठी संबंधित औषधी वनस्पतींची माहिती सापडली नाही. कृपया पुन्हा प्रयत्न करा किंवा विशिष्ट औषधी वनस्पतीबद्दल विचारा."
    }
    return messages.get(lang, messages["en"])

def get_insufficient_context_message(lang: str) -> str:
    """Get 'insufficient context' message in appropriate language"""
    messages = {
        "en": "No sufficiently relevant herbal information found.",
        "hi": "पर्याप्त प्रासंगिक जड़ी-बूटी की जानकारी नहीं मिली।",
        "mr": "पुरेशी संबंधित औषधी वनस्पतींची माहिती आढळली नाही."
    }
    return messages.get(lang, messages["en"])

def validate_response_language(response: str, expected_lang: str) -> tuple[str, bool]:
    """
    Validate if response is in expected language
    Returns (response, is_correct_language)
    """
    if not response or expected_lang == 'en':
        return response, True
    
    # Detect actual language of response
    actual_lang = detect_lang(response)
    
    if actual_lang == expected_lang:
        return response, True
    
    # If language doesn't match, log warning
    logger.warning(f"Response language mismatch. Expected: {expected_lang}, Got: {actual_lang}")
    logger.warning("Consider improving model prompts for better language consistency")
    
    return response, False

def translate(text: str, src: str, tgt: str) -> str:
    """
    Offline translation fallback - returns original text
    This replaces the previous online translation dependency
    """
    if src == tgt:
        return text
    
    # Since we removed online translation, just return original text
    # The system now relies on proper prompting to get correct language responses
    logger.warning(f"Translation requested but offline mode active: {src} -> {tgt}")
    return text

# Test cases for validation
def test_language_detection():
    """Test language detection with sample queries"""
    test_cases = [
        ("डोकेदुखीसाठी काय घ्यावे?", "mr"),
        ("तनाव के लिए क्या लें?", "hi"), 
        ("What helps with anxiety?", "en"),
        ("हल्दी के फायदे क्या हैं?", "hi"),
        ("औषधी वनस्पती कोणत्या आहेत?", "mr"),
        ("तुळशीचे फायदे काय आहेत?", "mr"),
        ("नीम का उपयोग कैसे करें?", "hi"),
        ("पाचनशक्ती सुधारण्यासाठी काय करावे?", "mr")
    ]
    
    print("Testing Enhanced Language Detection:")
    print("-" * 50)
    for text, expected in test_cases:
        detected = detect_lang(text)
        status = "✅" if detected == expected else "❌"
        print(f"{status} '{text}' -> Detected: {detected}, Expected: {expected}")

if __name__ == "__main__":
    test_language_detection()