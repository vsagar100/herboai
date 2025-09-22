# File: app/main.py
# Main FastAPI application with enhanced language support

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.rag_engine import answer, search
from app.ollama_llm_adapter import get_llm
from app.db import list_herbs, fetch_herb
from app.i18n import detect_lang, get_language_name
import json
from typing import List, Dict, Any
from loguru import logger

app = FastAPI(title="Ayush Herbs AI", version="0.1.0")

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/herbs")
def herbs(limit: int = 50, offset: int = 0):
    return list_herbs(limit, offset)

@app.get("/herbs/{herb_id}")
def herb(herb_id: str):
    row = fetch_herb(herb_id)
    if not row:
        raise HTTPException(404, "Not found")
    return row

@app.get("/search")
def semantic_search(q: str = Query(..., min_length=2), k: int = 5):
    hits = search(q, top_k=k)
    return {"matches": [{"id": i, "score": s} for i, s in hits]}

def format_herb_for_frontend(herb_row: dict, lang: str = "en") -> dict:
    """Format herb data to match frontend HerbCard expectations"""
    try:
        languages_data = json.loads(herb_row.get("languages_json", "{}"))
    except (json.JSONDecodeError, TypeError):
        languages_data = {}
    
    # Get language-specific data
    lang_data = languages_data.get(lang, {})
    en_data = languages_data.get("en", {})
    
    # Extract common names
    common_names = []
    if lang_data.get("common_names"):
        if isinstance(lang_data["common_names"], list):
            common_names.extend(lang_data["common_names"])
        else:
            common_names.append(lang_data["common_names"])
    
    if en_data.get("common_names") and lang != "en":
        if isinstance(en_data["common_names"], list):
            common_names.extend(en_data["common_names"])
        else:
            common_names.append(en_data["common_names"])
    
    # Build formatted herb object
    formatted_herb = {
        "id": herb_row.get("id"),
        "name": herb_row.get("name", "Unknown"),
        "scientific_name": herb_row.get("scientific_name", ""),
        "common_names": common_names or [herb_row.get("name", "Unknown")],
        "uses": herb_row.get("uses", "Uses not specified"),
        "ayush_system": herb_row.get("ayush_system", "Ayurveda"),
        "parts_used": herb_row.get("parts_used", ""),
        "contraindications": herb_row.get("contraindications", ""),
        "dosage": herb_row.get("dosage", ""),
        "remedies": []
    }
    
    # Add remedies if available in language data
    if lang_data.get("remedies"):
        formatted_herb["remedies"] = lang_data["remedies"]
    elif en_data.get("remedies"):
        formatted_herb["remedies"] = en_data["remedies"]
    
    # Add descriptions
    description = (lang_data.get("short_description") or 
                  en_data.get("short_description") or 
                  formatted_herb["uses"])
    formatted_herb["description"] = description
    
    return formatted_herb

def determine_intent(query: str, lang: str) -> str:
    """Determine user intent based on query content"""
    query_lower = query.lower()
    
    # Multi-language keyword mapping
    intent_keywords = {
        "stress_relief": {
            "en": ["stress", "anxiety", "tension", "worry", "nervous"],
            "hi": ["तनाव", "चिंता", "घबराहट", "परेशानी"],
            "mr": ["तणाव", "चिंता", "काळजी", "अस्वस्थता"]
        },
        "immunity_boost": {
            "en": ["immunity", "immune", "resistance", "defense"],
            "hi": ["प्रतिरक्षा", "रोग", "बचाव", "शक्ति"],
            "mr": ["रोगप्रतिकारक", "शक्ती", "संरक्षण"]
        },
        "digestive_health": {
            "en": ["digestion", "stomach", "gastric", "indigestion"],
            "hi": ["पाचन", "पेट", "गैस", "अपच"],
            "mr": ["पाचन", "पोट", "गॅस"]
        },
        "respiratory_health": {
            "en": ["respiratory", "breathing", "cough", "cold", "lungs"],
            "hi": ["श्वसन", "सांस", "खांसी", "सर्दी", "फेफड़े"],
            "mr": ["श्वसन", "श्वास", "खोकला", "सर्दी"]
        },
        "pain_relief": {
            "en": ["pain", "ache", "headache", "joint", "arthritis"],
            "hi": ["दर्द", "सिरदर्द", "जोड़", "गठिया"],
            "mr": ["दुखणे", "डोकेदुखी", "सांधे", "वेदना"]
        },
        "skin_health": {
            "en": ["skin", "rash", "acne", "eczema", "dermatitis"],
            "hi": ["त्वचा", "चकत्ते", "मुंहासे", "खुजली"],
            "mr": ["त्वचा", "पुरळ", "खाज"]
        }
    }
    
    # Check for intent keywords
    for intent, lang_keywords in intent_keywords.items():
        keywords = lang_keywords.get(lang, []) + lang_keywords.get("en", [])
        if any(keyword in query_lower for keyword in keywords):
            return intent
    
    return "general_health"

@app.post("/query")
async def query(request: dict):
    """
    Handle query requests from frontend with enhanced language support
    Expected frontend request: {"query": "user question", "lang": "optional"}
    """
    try:
        # Extract query from request - handle both formats
        user_query = request.get("query") or request.get("question", "")
        user_lang = request.get("lang", None)
        
        if not user_query.strip():
            raise HTTPException(400, "Query cannot be empty")
        
        # Enhanced language detection
        detected_lang = detect_lang(user_query)
        target_lang = user_lang or detected_lang
        
        # Ensure supported language
        if target_lang not in ["en", "hi", "mr"]:
            target_lang = "en"
        
        logger.info(f"Processing query in {target_lang}: {user_query[:100]}")
        
        # Get LLM instance
        llm = await get_llm()
        
        # Generate answer using enhanced RAG
        ai_response, response_lang, source_herb_ids = await answer(user_query, target_lang, llm)
        
        # Fetch and format herb data for frontend
        herbs_data = []
        for herb_id in source_herb_ids[:5]:  # Limit to top 5 herbs
            herb_row = fetch_herb(herb_id)
            if herb_row:
                formatted_herb = format_herb_for_frontend(herb_row, response_lang)
                herbs_data.append(formatted_herb)
        
        # Determine user intent
        intent = determine_intent(user_query, response_lang)
        
        # Calculate confidence score based on various factors
        confidence = 0.5  # Base confidence
        if herbs_data:
            confidence += 0.3  # Found relevant herbs
        if response_lang == detected_lang:
            confidence += 0.1  # Language detection matches
        if len(source_herb_ids) >= 2:
            confidence += 0.1  # Multiple sources
        
        confidence = min(confidence, 0.95)  # Cap at 95%
        
        # Build metadata
        metadata = {
            "language": response_lang,
            "detected_language": detected_lang,
            "query_length": len(user_query),
            "herbs_found": len(herbs_data),
            "sources_used": len(source_herb_ids),
            "confidence": round(confidence, 2),
            "intent": intent,
            "language_name": get_language_name(response_lang)
        }
        
        # Return response in frontend-expected format
        return {
            "success": True,
            "ai_response": ai_response,
            "results": herbs_data,
            "metadata": metadata
        }
        
    except Exception as e:
        logger.error(f"Error in query endpoint: {e}")
        
        # Determine language for error message
        try:
            error_lang = detect_lang(request.get("query", ""))
        except:
            error_lang = "en"
        
        error_messages = {
            "en": "I apologize, but I'm experiencing technical difficulties. Please try again or rephrase your question.",
            "hi": "मुझे खेद है, लेकिन मुझे तकनीकी कठिनाइयों का सामना करना पड़ रहा है। कृपया पुनः प्रयास करें या अपना प्रश्न दूसरे तरीके से पूछें।",
            "mr": "मला माफ करा, परंतु मला तांत्रिक अडचणी येत आहेत. कृपया पुन्हा प्रयत्न करा किंवा तुमचा प्रश्न वेगळ्या पद्धतीने विचारा."
        }
        
        return {
            "success": False,
            "error": str(e),
            "ai_response": error_messages.get(error_lang, error_messages["en"]),
            "results": [],
            "metadata": {
                "language": error_lang,
                "error": True,
                "confidence": 0.0
            }
        }