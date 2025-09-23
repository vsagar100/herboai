# File: app/main.py
# Updated main.py with intelligent contextual herb card generation

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from app.rag_engine import answer, search
from app.ollama_llm_adapter import get_llm
from app.db import list_herbs, fetch_herb
from app.i18n import detect_lang, get_language_name
from app.herb_card_generator import generate_contextual_herb_cards
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

def determine_intent(query: str, lang: str) -> str:
    """Determine user intent based on query content"""
    query_lower = query.lower()
    
    # Multi-language keyword mapping
    intent_keywords = {
        "pain_relief": {
            "en": ["headache", "pain", "ache", "joint", "arthritis", "migraine"],
            "hi": ["सिरदर्द", "दर्द", "जोड़", "गठिया", "माइग्रेन"],
            "mr": ["डोकेदुखी", "दुखणे", "वेदना", "सांधे"]
        },
        "cough_cold": {
            "en": ["cough", "cold", "throat", "respiratory", "bronchitis"],
            "hi": ["खांसी", "सर्दी", "गला", "श्वसन"],
            "mr": ["खोकला", "सर्दी", "घसा", "श्वसन"]
        },
        "digestive_health": {
            "en": ["digestion", "stomach", "gastric", "indigestion", "acidity"],
            "hi": ["पाचन", "पेट", "गैस", "अपच", "एसिडिटी"],
            "mr": ["पाचन", "पोट", "गॅस", "अपचन"]
        },
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
    Handle query requests from frontend with intelligent contextual herb cards
    Expected frontend request: {"query": "user question", "lang": "optional"}
    """
    try:
        # Extract query from request
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
        
        # 🔥 NEW: Generate intelligent contextual herb cards
        intelligent_herb_cards = await generate_contextual_herb_cards(
            user_query=user_query,
            target_lang=response_lang,
            herb_ids=source_herb_ids,
            ai_response=ai_response,
            fetch_herb_func=fetch_herb
        )
        
        # Determine user intent
        intent = determine_intent(user_query, response_lang)
        
        # Calculate confidence score
        confidence = 0.5  # Base confidence
        if intelligent_herb_cards:
            confidence += 0.3  # Found relevant herbs
        if response_lang == detected_lang:
            confidence += 0.1  # Language detection matches
        if len(source_herb_ids) >= 2:
            confidence += 0.1  # Multiple sources
        
        confidence = min(confidence, 0.95)  # Cap at 95%
        
        # Build enhanced metadata
        metadata = {
            "language": response_lang,
            "detected_language": detected_lang,
            "query_length": len(user_query),
            "herbs_found": len(intelligent_herb_cards),
            "sources_used": len(source_herb_ids),
            "confidence": round(confidence, 2),
            "intent": intent,
            "language_name": get_language_name(response_lang),
            "processing_method": "intelligent_contextual"  # Indicates enhanced processing
        }
        
        # Return response with intelligent herb cards
        return {
            "success": True,
            "ai_response": ai_response,
            "results": intelligent_herb_cards,  # These are now contextually intelligent!
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
                "confidence": 0.0,
                "processing_method": "error_fallback"
            }
        }