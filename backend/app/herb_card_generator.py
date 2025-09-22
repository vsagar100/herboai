# File: app/herb_card_generator.py
# Intelligent context-aware herb card generation

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
            max_tokens=800,
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

उपयोगकर्ता का प्रश्न: {user_query}

AI का मुख्य उत्तर: {ai_response}

उपलब्ध जड़ी-बूटी की जानकारी:
{herbs_context}

कृपया प्रत्येक जड़ी-बूटी के लिए JSON फॉर्मेट में विस्तृत कार्ड बनाएं जो केवल उपयोगकर्ता की समस्या से संबंधित हो। प्रत्येक कार्ड में शामिल करें:

1. नाम और वैज्ञानिक नाम (हिंदी में)
2. इस विशिष्ट समस्या के लिए उपयोग
3. इस समस्या के लिए विशिष्ट उपचार विधि
4. सटीक खुराक और उपयोग की विधि
5. तैयारी की विधि
6. सावधानियां
7. कब तक उपयोग करें

JSON फॉर्मेट:
```json
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
```

केवल JSON आउटपुट दें, अन्य कोई टेक्स्ट न दें।"""

    elif target_lang == "mr":
        return f"""तुम्ही AYUSH औषधी वनस्पती तज्ञ आहात. वापरकर्त्याच्या प्रश्नानुसार विशिष्ट औषधी वनस्पती कार्ड तयार करा.

वापरकर्त्याचा प्रश्न: {user_query}

AI चे मुख्य उत्तर: {ai_response}

उपलब्ध औषधी वनस्पतींची माहिती:
{herbs_context}

कृपया प्रत्येक औषधी वनस्पतीसाठी JSON फॉर्मेटमध्ये तपशीलवार कार्ड तयार करा जे फक्त वापरकर्त्याच्या समस्येशी संबंधित असेल. प्रत्येक कार्डमध्ये समाविष्ट करा:

1. नाव आणि वैज्ञानिक नाव (मराठीत)
2. या विशिष्ट समस्येसाठी वापर
3. या समस्येसाठी विशिष्ट उपचार पद्धती
4. अचूक डोस आणि वापराची पद्धत
5. तयारीची पद्धत
6. सावधगिरी
7. किती दिवस वापरावे

JSON फॉर्मेट:
```json
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
```

फक्त JSON आउटपुट द्या, इतर कोणताही टेक्स्ट नाही."""

    else:  # English
        return f"""You are an AYUSH herbal medicine expert. Create specific herb cards based on the user's query.

User's Question: {user_query}

AI's Main Response: {ai_response}

Available Herb Information:
{herbs_context}

Please create detailed cards for each herb in JSON format that are ONLY relevant to the user's specific problem. Include for each card:

1. Name and scientific name
2. Specific use for this condition
3. Specific remedy methods for this problem
4. Precise dosage and usage method
5. Preparation method
6. Precautions specific to this use
7. Duration of use

JSON Format:
```json
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
```

Provide ONLY the JSON output, no other text."""

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
        
        # Parse JSON
        herb_cards = json.loads(cleaned_response)
        
        # Validate and clean the parsed cards
        validated_cards = []
        for card in herb_cards:
            if validate_herb_card(card):
                validated_cards.append(card)
        
        return validated_cards
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {e}")
        logger.error(f"Response content: {response[:200]}")
        return []
    except Exception as e:
        logger.error(f"Error parsing herb cards: {e}")
        return []

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