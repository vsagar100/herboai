from __future__ import annotations
from typing import List, Tuple
from .settings import settings
from .i18n import detect_lang, translate
from .db import fetch_herb
from loguru import logger
import os, json, numpy as np

from sentence_transformers import SentenceTransformer
import faiss

_model: SentenceTransformer | None = None
_index: faiss.Index | None = None
_idmap: list[str] = []

def format_chat_prompt(system: str, user: str) -> str:
    """Format prompt for Llama 2 Chat model"""
    return f"""<s>[INST] <<SYS>>
{system}
<</SYS>>

{user} [/INST]"""

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
    langs = json.loads(herb_row["languages_json"])
    en = langs.get("en", {})
    hi = langs.get("hi", {})
    mr = langs.get("mr", {})

    # Create structured content
    doc_parts = []
    
    # Basic info
    name_parts = [herb_row['name']]
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
    """Create system prompt based on target language"""
    lang_instructions = {
        "en": "Answer in English only.",
        "hi": "Answer in Hindi only. Use proper Hindi script (Devanagari).",
        "mr": "Answer in Marathi only. Use proper Marathi script (Devanagari)."
    }
    
    return f"""You are an AYUSH (Ayurveda, Yoga, Unani, Siddha, Homeopathy) herbal medicine expert assistant.

Your role:
1. Provide accurate information about herbs and their medicinal uses
2. Suggest appropriate AYUSH remedies based on the context provided
3. Give clear dosage and usage instructions when available
4. Mention contraindications and safety warnings
5. {lang_instructions.get(lang, "Answer in the requested language.")}

Guidelines:
- Only use information from the provided context
- If information is insufficient, clearly state your limitations
- Always mention consulting healthcare professionals for serious conditions
- Be concise but comprehensive
- Focus on traditional AYUSH knowledge and practices"""

def create_user_prompt(question: str, context: str, lang: str) -> str:
    """Create user prompt with question and context"""
    lang_map = {"en": "English", "hi": "Hindi", "mr": "Marathi"}
    
    return f"""Question: {question}

Based on the following herbal information, please provide a helpful answer in {lang_map.get(lang, lang)}:

Context:
{context}

Please provide a clear, accurate response about AYUSH herbal remedies relevant to this question."""

async def answer(question: str, lang: str | None, llm) -> tuple[str, str, List[str]]:
    """Generate answer using RAG pipeline"""
    
    # Detect language if not provided
    qlang = lang or detect_lang(question)
    if qlang not in ["en", "hi", "mr"]:
        qlang = "en"  # Default to English
    
    # Search for relevant herbs
    hits = search(question, top_k=4)
    if not hits:
        msg = {
            "en": "I couldn't find relevant herbal information for your question. Please try rephrasing or ask about specific herbs.",
            "hi": "मुझे आपके प्रश्न के लिए प्रासंगिक जड़ी-बूटी की जानकारी नहीं मिली। कृपया पुनः प्रयास करें या किसी विशिष्ट जड़ी-बूटी के बारे में पूछें।",
            "mr": "मला तुमच्या प्रश्नासाठी संबंधित औषधी वनस्पतींची माहिती सापडली नाही. कृपया पुन्हा प्रयत्न करा किंवा विशिष्ट औषधी वनस्पतीबद्दल विचारा."
        }
        return (msg.get(qlang, msg["en"]), qlang, [])

    # Collect and format context
    context_blocks, used_ids = [], []
    for hid, score in hits:
        if score < 0.1:  # Skip very low relevance matches
            continue
            
        row = fetch_herb(hid)
        if not row:
            continue
            
        context_blocks.append(compose_doc(row))
        used_ids.append(hid)
    
    if not context_blocks:
        msg = {
            "en": "No sufficiently relevant herbal information found.",
            "hi": "पर्याप्त प्रासंगिक जड़ी-बूटी की जानकारी नहीं मिली।",
            "mr": "पुरेशी संबंधित औषधी वनस्पतींची माहिती आढळली नाही."
        }
        return (msg.get(qlang, msg["en"]), qlang, [])
    
    # Create context
    context_text = "\n\n---\n\n".join(context_blocks)
    
    # Create prompts
    system_prompt = create_system_prompt(qlang)
    user_prompt = create_user_prompt(question, context_text, qlang)
    
    # Format full prompt
    full_prompt = format_chat_prompt(system_prompt, user_prompt)
    
    # Generate response with conservative settings for better quality
    response = llm.generate(
        full_prompt,
        max_tokens=min(settings.MAX_TOKENS, 400),  # Keep responses focused
        temperature=0.2,  # Low temperature for consistency
    )
    
    # Validate output language and translate if necessary
    detected_lang = detect_lang(response)
    if qlang in ("hi", "mr") and detected_lang != qlang:
        # If model didn't respond in correct language, translate
        try:
            response = translate(response, detected_lang, qlang)
        except Exception as e:
            logger.warning(f"Translation failed: {e}")
            # Keep original response if translation fails
    
    return response, qlang, used_ids