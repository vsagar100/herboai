# File: app/herb_card_generator.py
# Complete intelligent context-aware herb card generation with all functions

import json
from typing import List, Dict, Any
from loguru import logger
from .ollama_llm_adapter import get_llm

async def generate_contextual_herb_cards(
    user_query: str, 
    target_lang: str, 
    herb_ids: List[str], 
    ai_response: str,
    fetch_herb_func
) -> List[Dict[str, Any]]:
    """
    Generate intelligent, contextual herb cards using LLM
    This shows specific remedies relevant to user's query only
    """
    
    if not herb_ids:
        return []
    
    # Get LLM instance
    llm = await get_llm()
    
    # Fetch herb data
    herbs_data = []
    for herb_id in herb_ids[:4]:  # Limit to 4 herbs for better UX
        herb_row = fetch_herb_func(herb_id)
        if herb_row:
            herbs_data.append(herb_row)
    
    if not herbs_data:
        return []
    
    # Create contextual herb card generation prompt
    herb_card_prompt = create_herb_card_generation_prompt(
        user_query, target_lang, herbs_data, ai_response
    )
    
    # Generate contextual herb cards
    try:
        response = llm.generate(
            herb_card_prompt,
            max_tokens=1000,
            temperature=0.1
        )
        
        # Parse the generated herb cards
        herb_cards = parse_generated_herb_cards(response, target_lang)
        
        logger.info(f"Generated {len(herb_cards)} contextual herb cards for query: {user_query[:50]}")
        return herb_cards
        
    except Exception as e:
        logger.error(f"Error generating contextual herb cards: {e}")
        # Fallback to basic cards
        return create_fallback_herb_cards(herbs_data, target_lang)

def create_herb_card_generation_prompt(
    user_query: str, 
    target_lang: str, 
    herbs_data: List[Dict], 
    ai_response: str
) -> str:
    """Create prompt for generating contextual herb cards"""
    
    # Prepare herbs information
    herbs_info = []
    for herb in herbs_data:
        try:
            lang_data = json.loads(herb.get("languages_json", "{}"))
        except:
            lang_data = {}
        
        herb_info = f"""
Herb ID: {herb.get('id')}
Name: {herb.get('name')}
Scientific Name: {herb.get('scientific_name', '')}
General Uses: {herb.get('uses', '')}
Contraindications: {herb.get('contraindications', '')}
General Dosage: {herb.get('dosage', '')}
AYUSH System: {herb.get('ayush_system', 'Ayurveda')}
Parts Used: {herb.get('parts_used', '')}
Language Data: {json.dumps(lang_data, ensure_ascii=False)}
"""
        herbs_info.append(herb_info)
    
    herbs_context = "\n---\n".join(herbs_info)
    
    if target_lang == "hi":
        return f"""आप एक AYUSH जड़ी-बूटी विशेषज्ञ हैं। उपयोगकर्ता के प्रश्न के अनुसार विशिष्ट जड़ी-बूटी कार्ड बनाएं।

महत्वपूर्ण: केवल वैध JSON array वापस करें। कोई व्याख्या नहीं, कोई अतिरिक्त टेक्स्ट नहीं।

उपयोगकर्ता का प्रश्न: {user_query}

AI का मुख्य उत्तर: {ai_response}

उपलब्ध जड़ी-बूटी की जानकारी:
{herbs_context}

केवल इस JSON फॉर्मेट में वापस करें:
[
  {{
    "id": "herb_id",
    "name": "हिंदी नाम",
    "scientific_name": "वैज्ञानिक नाम", 
    "common_names": ["हिंदी नाम", "अन्य नाम"],
    "specific_use_for_query": "इस समस्या के लिए विशिष्ट उपयोग",
    "contextual_remedies": [
      {{
        "condition": "उपयोगकर्ता की समस्या",
        "preparation": "तैयारी की विधि",
        "dosage": "सटीक खुराक",
        "duration": "कितने दिन तक",
        "timing": "कब लें (सुबह/शाम)"
      }}
    ],
    "contraindications": "सावधानियां",
    "ayush_system": "आयुर्वेद",
    "parts_used": "उपयोग किए जाने वाले भाग"
  }}
]

महत्वपूर्ण: केवल JSON array वापस करें। कोई अन्य टेक्स्ट नहीं।"""

    elif target_lang == "mr":
        return f"""तुम्ही AYUSH औषधी वनस्पती तज्ञ आहात. वापरकर्त्याच्या प्रश्नानुसार विशिष्ट औषधी वनस्पती कार्ड तयार करा.

महत्वाचे: फक्त वैध JSON array परत करा. कोणतेही स्पष्टीकरण नाही, कोणताही अतिरिक्त टेक्स्ट नाही.

वापरकर्त्याचा प्रश्न: {user_query}

AI चे मुख्य उत्तर: {ai_response}

उपलब्ध औषधी वनस्पतींची माहिती:
{herbs_context}

फक्त या JSON फॉर्मेटमध्ये परत करा:
[
  {{
    "id": "herb_id",
    "name": "मराठी नाव",
    "scientific_name": "वैज्ञानिक नाव",
    "common_names": ["मराठी नाव", "इतर नावे"],
    "specific_use_for_query": "या समस्येसाठी विशिष्ट वापर",
    "contextual_remedies": [
      {{
        "condition": "वापरकर्त्याची समस्या",
        "preparation": "तयारीची पद्धत",
        "dosage": "अचूक डोस",
        "duration": "किती दिवस",
        "timing": "केव्हा घ्या (सकाळी/संध्याकाळी)"
      }}
    ],
    "contraindications": "सावधगिरी",
    "ayush_system": "आयुर्वेद",
    "parts_used": "वापरले जाणारे भाग"
  }}
]

महत्वाचे: फक्त JSON array परत करा. इतर कोणताही टेक्स्ट नाही."""

    else:  # English
        return f"""You are an AYUSH herbal medicine expert. Create specific herb cards based on the user's query.

CRITICAL: Return ONLY a valid JSON array. No explanations, no additional text, no markdown formatting.

User's Question: {user_query}

AI's Main Response: {ai_response}

Available Herb Information:
{herbs_context}

Create detailed cards for each herb that are ONLY relevant to the user's specific problem.

Return ONLY this JSON format:
[
  {{
    "id": "herb_id",
    "name": "Common Name",
    "scientific_name": "Scientific Name",
    "common_names": ["Common Name", "Alternative Names"],
    "specific_use_for_query": "Specific use for this condition",
    "contextual_remedies": [
      {{
        "condition": "User's specific problem",
        "preparation": "How to prepare",
        "dosage": "Exact dosage",
        "duration": "How many days",
        "timing": "When to take (morning/evening)"
      }}
    ],
    "contraindications": "Specific precautions",
    "ayush_system": "Ayurveda",
    "parts_used": "Parts of plant used"
  }}
]

IMPORTANT: Return ONLY the JSON array above. No other text before or after."""

def parse_generated_herb_cards(response: str, target_lang: str) -> List[Dict[str, Any]]:
    """Parse the LLM generated herb cards from JSON response"""
    
    try:
        # Clean the response
        cleaned_response = response.strip()
        
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in cleaned_response:
            start = cleaned_response.find("```json") + 7
            end = cleaned_response.find("```", start)
            if end != -1:
                cleaned_response = cleaned_response[start:end]
        elif "```" in cleaned_response:
            start = cleaned_response.find("```") + 3
            end = cleaned_response.find("```", start)
            if end != -1:
                cleaned_response = cleaned_response[start:end]
        
        # More aggressive JSON extraction - find the JSON array bounds
        cleaned_response = cleaned_response.strip()
        
        # Find the start of JSON array
        start_bracket = cleaned_response.find('[')
        if start_bracket == -1:
            logger.error("No JSON array start found")
            return create_fallback_from_response(response, target_lang)
        
        # Find the matching closing bracket
        bracket_count = 0
        end_bracket = -1
        
        for i in range(start_bracket, len(cleaned_response)):
            char = cleaned_response[i]
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                if bracket_count == 0:
                    end_bracket = i
                    break
        
        if end_bracket == -1:
            logger.error("No matching closing bracket found")
            return create_fallback_from_response(response, target_lang)
        
        # Extract only the JSON array
        json_only = cleaned_response[start_bracket:end_bracket + 1]
        
        logger.debug(f"Extracted JSON: {json_only[:200]}...")
        
        # Parse JSON
        herb_cards = json.loads(json_only)
        
        # Validate and clean the parsed cards
        validated_cards = []
        for card in herb_cards:
            if validate_herb_card(card):
                validated_cards.append(card)
        
        logger.info(f"Successfully parsed {len(validated_cards)} herb cards")
        return validated_cards
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Attempted JSON: {json_only if 'json_only' in locals() else 'N/A'}")
        return create_fallback_from_response(response, target_lang)
    except Exception as e:
        logger.error(f"Error parsing herb cards: {e}")
        return create_fallback_from_response(response, target_lang)

def create_fallback_from_response(response: str, target_lang: str) -> List[Dict[str, Any]]:
    """Create fallback herb cards by extracting information from the raw response"""
    
    fallback_cards = []
    
    try:
        # Try to extract herb information from the response text
        lines = response.split('\n')
        current_herb = {}
        
        for line in lines:
            line = line.strip()
            
            # Look for herb names or IDs
            if 'herb_' in line.lower() and 'id' in line.lower():
                if current_herb:  # Save previous herb
                    fallback_cards.append(create_basic_fallback_card(current_herb, target_lang))
                current_herb = {'raw_text': line}
            elif line and current_herb:
                current_herb['raw_text'] = current_herb.get('raw_text', '') + ' ' + line
        
        # Add the last herb
        if current_herb:
            fallback_cards.append(create_basic_fallback_card(current_herb, target_lang))
    
    except Exception as e:
        logger.error(f"Fallback parsing failed: {e}")
    
    # Ensure we always return at least one card
    return fallback_cards[:4] if fallback_cards else [create_basic_fallback_card({}, target_lang)]

def create_basic_fallback_card(herb_info: dict, target_lang: str) -> Dict[str, Any]:
    """Create a basic herb card from extracted text"""
    
    fallback_messages = {
        "en": {
            "name": "Herbal Remedy",
            "use": "Natural wellness support",
            "prep": "Consult healthcare provider for preparation method",
            "dose": "Follow practitioner guidance",
            "precaution": "Consult healthcare professional before use"
        },
        "hi": {
            "name": "जड़ी-बूटी उपचार",
            "use": "प्राकृतिक स्वास्थ्य सहायता",
            "prep": "तैयारी की विधि के लिए चिकित्सक से सलाह लें",
            "dose": "चिकित्सक के मार्गदर्शन का पालन करें",
            "precaution": "उपयोग से पहले स्वास्थ्य पेशेवर से सलाह लें"
        },
        "mr": {
            "name": "औषधी वनस्पती उपचार",
            "use": "नैसर्गिक आरोग्य आधार",
            "prep": "तयारीच्या पद्धतीसाठी डॉक्टरांचा सल्ला घ्या",
            "dose": "डॉक्टरांच्या मार्गदर्शनाचे पालन करा",
            "precaution": "वापरण्यापूर्वी आरोग्य तज्ञांचा सल्ला घ्या"
        }
    }
    
    msgs = fallback_messages.get(target_lang, fallback_messages["en"])
    
    return {
        "id": "fallback_herb",
        "name": msgs["name"],
        "scientific_name": "",
        "common_names": [msgs["name"]],
        "specific_use_for_query": msgs["use"],
        "contextual_remedies": [
            {
                "condition": msgs["use"],
                "preparation": msgs["prep"],
                "dosage": msgs["dose"],
                "duration": "As advised",
                "timing": "As directed"
            }
        ],
        "contraindications": msgs["precaution"],
        "ayush_system": "Ayurveda",
        "parts_used": "Various"
    }

def validate_herb_card(card: Dict[str, Any]) -> bool:
    """Validate that a herb card has required fields"""
    required_fields = ["id", "name", "specific_use_for_query"]
    
    for field in required_fields:
        if field not in card or not card[field]:
            return False
    
    return True

def create_fallback_herb_cards(herbs_data: List[Dict], target_lang: str) -> List[Dict[str, Any]]:
    """Create fallback herb cards if LLM generation fails"""
    
    fallback_cards = []
    
    for herb in herbs_data:
        try:
            lang_data = json.loads(herb.get("languages_json", "{}"))
        except:
            lang_data = {}
        
        # Get language-specific data
        target_data = lang_data.get(target_lang, {})
        en_data = lang_data.get("en", {})
        
        # Build fallback card
        card = {
            "id": herb.get("id"),
            "name": herb.get("name", "Unknown"),
            "scientific_name": herb.get("scientific_name", ""),
            "common_names": target_data.get("common_names", [herb.get("name", "Unknown")]),
            "specific_use_for_query": herb.get("uses", "General wellness"),
            "contextual_remedies": target_data.get("remedies", []),
            "contraindications": herb.get("contraindications", ""),
            "ayush_system": herb.get("ayush_system", "Ayurveda"),
            "parts_used": herb.get("parts_used", "")
        }
        
        fallback_cards.append(card)
    
    return fallback_cards