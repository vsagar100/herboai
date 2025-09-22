# File: app/rag_engine.py
# Enhanced RAG engine with improved language detection and handling

from __future__ import annotations
from typing import List, Tuple
from .settings import settings
from .i18n import detect_lang, get_no_results_message, get_insufficient_context_message, validate_response_language
from .db import fetch_herb
from loguru import logger
import os, json, numpy as np

from sentence_transformers import SentenceTransformer
import faiss

_model: SentenceTransformer | None = None
_index: faiss.Index | None = None
_idmap: list[str] = []

def format_chat_prompt(system: str, user: str) -> str:
    """Format prompt for Llama 3.2 Instruct model"""
    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

{system}<|eot_id|><|start_header_id|>user<|end_header_id|>

{user}<|eot_id|><|start_header_id|>assistant<|end_header_id|>

"""

def _load_embeddings() -> SentenceTransformer:
    global _model
    if _model is None:
        os.environ.setdefault("HF_HOME", settings.HF_HOME)
        _model = SentenceTransformer(settings.EMBEDDINGS_MODEL)
    return _model

def load_faiss(index_path: str) -> Tuple[faiss.Index, list[str]]:
    global _index, _idmap
    if _index is None:
        _index = faiss.read_index(index_path)
        with open(index_path + ".ids", "r", encoding="utf-8") as f:
            _idmap = [line.strip() for line in f]
    return _index, _idmap

def embed_texts(texts: List[str]) -> np.ndarray:
    model = _load_embeddings()
    vecs = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return vecs.astype("float32")

def compose_doc(herb_row: dict) -> str:
    """Create a well-structured document from herb data"""
    try:
        langs = json.loads(herb_row.get("languages_json", "{}"))
    except (json.JSONDecodeError, TypeError):
        langs = {}
    
    en = langs.get("en", {})
    hi = langs.get("hi", {})
    mr = langs.get("mr", {})

    # Create structured content
    doc_parts = []
    
    # Basic info
    name_parts = [herb_row.get('name', 'Unknown')]
    if herb_row.get('scientific_name'):
        name_parts.append(f"({herb_row['scientific_name']})")
    doc_parts.append(f"Herb: {' '.join(name_parts)}")
    
    # Uses and benefits
    if herb_row.get('uses'):
        doc_parts.append(f"Uses: {herb_row['uses']}")
    
    # Descriptions in different languages
    if en.get('short_description'):
        doc_parts.append(f"Description (EN): {en['short_description']}")
    if hi.get('short_description'):
        doc_parts.append(f"Description (HI): {hi['short_description']}")
    if mr.get('short_description'):
        doc_parts.append(f"Description (MR): {mr['short_description']}")
    
    # Safety information
    if herb_row.get('contraindications'):
        doc_parts.append(f"Contraindications: {herb_row['contraindications']}")
    
    # Dosage information
    if herb_row.get('dosage'):
        doc_parts.append(f"Dosage: {herb_row['dosage']}")
    
    return "\n".join(doc_parts)

def search(question: str, top_k: int = 4) -> List[Tuple[str, float]]:
    idx, idmap = load_faiss(settings.INDEX_PATH)
    qv = embed_texts([question])
    D, I = idx.search(qv, top_k)
    hits: List[Tuple[str, float]] = []
    for i, d in zip(I[0], D[0]):
        if i == -1:
            continue
        hits.append((idmap[i], float(d)))
    logger.debug(f"Search hits: {hits}")
    return hits

def create_system_prompt(lang: str) -> str:
    """Create very strict language-specific system prompts"""
    
    if lang == "hi":
        return """आप एक AYUSH जड़ी-बूटी विशेषज्ञ हैं। आपको केवल हिंदी में उत्तर देना है।

महत्वपूर्ण नियम:
- केवल हिंदी में लिखें, अंग्रेजी का एक भी शब्द न इस्तेमाल करें
- देवनागरी लिपि का उपयोग करें
- दिए गए संदर्भ का ही उपयोग करें
- संक्षिप्त और स्पष्ट उत्तर दें
- जड़ी-बूटी के नाम, उपयोग और सावधानियां बताएं
- हमेशा डॉक्टर से सलाह लेने की बात कहें

आपकी भूमिका:
1. जड़ी-बूटियों के औषधीय गुणों की जानकारी देना
2. AYUSH चिकित्सा पद्धति के अनुसार उपचार सुझाना
3. खुराक और उपयोग की विधि बताना
4. सुरक्षा संबंधी चेतावनी देना"""
    
    elif lang == "mr":
        return """तुम्ही AYUSH औषधी वनस्पती तज्ञ आहात। तुम्हाला फक्त मराठीत उत्तर द्यावे लागेल।

महत्वाचे नियम:
- फक्त मराठीत लिहा, इंग्रजीचा एकही शब्द वापरू नका
- देवनागरी लिपीचा वापर करा
- दिलेल्या संदर्भाचा वापर करा
- थोडक्यात आणि स्पष्ट उत्तर द्या
- औषधी वनस्पतींची नावे, उपयोग आणि सावधगिरी सांगा
- नेहमी डॉक्टरांचा सल्ला घेण्याचे सांगा

तुमची भूमिका:
1. औषधी वनस्पतींच्या गुणधर्मांची माहिती देणे
2. AYUSH पद्धतीनुसार उपचार सुचवणे
3. डोस आणि वापराची पद्धत सांगणे
4. सुरक्षेबाबत चेतावणी देणे"""
    
    else:  # English
        return """You are an AYUSH herbal medicine expert. You must answer ONLY in English.

Important Rules:
- Write only in English, no other language
- Use only the provided context information
- Give brief and clear answers
- Mention herb names, uses, and precautions
- Always advise consulting healthcare professionals

Your role:
1. Provide information about medicinal properties of herbs
2. Suggest AYUSH treatments based on context
3. Give dosage and usage instructions
4. Mention safety warnings and contraindications"""

def create_user_prompt(question: str, context: str, lang: str) -> str:
    """Create very strict language-specific user prompts"""
    
    if lang == "hi":
        return f"""प्रश्न: {question}

जड़ी-बूटी की जानकारी:
{context}

कृपया इस प्रश्न का उत्तर केवल हिंदी में दें। उपयुक्त जड़ी-बूटियों के नाम, उनके उपयोग और सावधानियों का उल्लेख करें।"""
    
    elif lang == "mr":
        return f"""प्रश्न: {question}

औषधी वनस्पतींची माहिती:
{context}

कृपया या प्रश्नाचे उत्तर फक्त मराठीत द्या. योग्य औषधी वनस्पतींची नावे, त्यांचे उपयोग आणि सावधगिरी सांगा."""
    
    else:  # English
        return f"""Question: {question}

Herbal information:
{context}

Please answer this question in English only. Mention appropriate herb names, their uses, and precautions."""

def clean_response_offline(response: str, target_lang: str) -> str:
    """Clean response without using online translation"""
    
    # Basic cleaning
    cleaned = response.strip()
    
    # Remove common prompt artifacts
    artifacts = [
        "You are an AYUSH", "आप एक AYUSH", "तुम्ही AYUSH",
        "Answer in", "उत्तर दें", "उत्तर द्या",
        "Based on", "के आधार पर", "च्या आधारे",
        "Please answer", "कृपया उत्तर", "कृपया उत्तर द्या",
        "Question:", "प्रश्न:", 
        "Context:", "संदर्भ:", "माहिती:"
    ]
    
    for artifact in artifacts:
        cleaned = cleaned.replace(artifact, "")
    
    # Remove excessive newlines
    cleaned = '\n'.join(line.strip() for line in cleaned.split('\n') if line.strip())
    
    # If response is too short or seems wrong, provide fallback
    if len(cleaned.strip()) < 30:
        fallbacks = {
            "en": "I need more specific information to provide a proper herbal recommendation. Please ask about a particular health condition or specific herb.",
            "hi": "उचित जड़ी-बूटी की सलाह देने के लिए मुझे अधिक विशिष्ट जानकारी चाहिए। कृपया किसी विशेष स्वास्थ्य समस्या या विशिष्ट जड़ी-बूटी के बारे में पूछें।",
            "mr": "योग्य औषधी वनस्पतीची शिफारस देण्यासाठी मला अधिक विशिष्ट माहिती हवी आहे. कृपया एखाद्या विशिष्ट आरोग्य समस्येबद्दल किंवा विशिष्ट औषधी वनस्पतीबद्दल विचारा."
        }
        return fallbacks.get(target_lang, fallbacks["en"])
    
    return cleaned

async def answer(question: str, lang: str | None, llm) -> tuple[str, str, List[str]]:
    """Generate answer using enhanced RAG pipeline with better language handling"""
    
    # Enhanced language detection
    detected_lang = detect_lang(question)
    
    # Use detected language if no language preference provided
    target_lang = lang or detected_lang
    
    # Ensure we support the target language
    if target_lang not in ["en", "hi", "mr"]:
        target_lang = "en"
    
    logger.info(f"Query: '{question[:50]}...' | Detected: {detected_lang} | Target: {target_lang}")
    
    # Search for relevant herbs
    hits = search(question, top_k=4)
    if not hits:
        return (get_no_results_message(target_lang), target_lang, [])

    # Collect and format context
    context_blocks, used_ids = [], []
    for hid, score in hits:
        if score < 0.15:  # Slightly higher threshold for better relevance
            continue
            
        row = fetch_herb(hid)
        if not row:
            continue
            
        context_blocks.append(compose_doc(row))
        used_ids.append(hid)
    
    if not context_blocks:
        return (get_insufficient_context_message(target_lang), target_lang, [])
    
    # Create context
    context_text = "\n\n---\n\n".join(context_blocks)
    
    # Create very specific prompts based on target language
    system_prompt = create_system_prompt(target_lang)
    user_prompt = create_user_prompt(question, context_text, target_lang)
    
    # Format full prompt
    full_prompt = format_chat_prompt(system_prompt, user_prompt)
    
    # Generate response with very conservative settings for consistency
    response = llm.generate(
        full_prompt,
        max_tokens=min(settings.MAX_TOKENS, 350),
        temperature=0.1,  # Very low for consistency
    )
    
    # Clean and validate response
    cleaned_response = clean_response_offline(response, target_lang)
    
    # Validate response language
    validated_response, language_correct = validate_response_language(cleaned_response, target_lang)
    
    if not language_correct:
        logger.warning(f"Response language validation failed for target: {target_lang}")
    
    # Final check - if response seems to be in wrong language for non-English targets
    if target_lang in ["hi", "mr"]:
        # Simple check for Devanagari characters
        import re
        devanagari_chars = len(re.findall(r'[\u0900-\u097F]', validated_response))
        if devanagari_chars < 5:  # Very few Devanagari characters
            logger.warning("Response appears to be in wrong script, may need model fine-tuning")
    
    return validated_response, target_lang, used_ids