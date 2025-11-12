# services/chat.py
import time
import json
import math
import os
from typing import Dict, Any, List, Optional
from sentence_transformers import SentenceTransformer
from sqlite_vec import serialize_float32

from db import get_db
from api.nlu_optimized import detect_language, classify_intent, extract_entities
from services.indic_translation_service import get_indic_translation_service
from api.context import get_last_context, persist_turn
from semantic import top_plants_for_disease, top_preparations_for_disease, ingredients_for_preparation

# Global embedding model (lazy loaded)
_EMB_MODEL = None
_SENTENCE_MODEL_NAME = os.getenv("SENTENCE_MODEL_NAME", "all-MiniLM-L6-v2")
_SENTENCE_MODEL_CACHE = os.getenv("SENTENCE_MODEL_CACHE")  # e.g., /data/models/sentencetransformers

# ============================================================================
# HELPERS
# ============================================================================

def _as_list(x):
    """Parse JSON array or return as-is"""
    if not x:
        return None
    if isinstance(x, list):
        return x
    try:
        v = json.loads(x)
        return v if isinstance(v, list) else None
    except Exception:
        return None

def _l2_normalize(v: List[float]) -> List[float]:
    """L2 normalize vector for cosine similarity"""
    s = math.sqrt(sum(x*x for x in v)) or 1.0
    return [x / s for x in v]

def _embed_384(text: str) -> bytes:
    """Generate 384-dim embedding using all-MiniLM-L6-v2"""
    global _EMB_MODEL
    if _EMB_MODEL is None:
        if _SENTENCE_MODEL_CACHE:
            print(f"[Embeddings] Loading {_SENTENCE_MODEL_NAME} with cache at {_SENTENCE_MODEL_CACHE}")
            _EMB_MODEL = SentenceTransformer(_SENTENCE_MODEL_NAME, cache_folder=_SENTENCE_MODEL_CACHE)
        else:
            print(f"[Embeddings] Loading {_SENTENCE_MODEL_NAME} (default cache)")
            _EMB_MODEL = SentenceTransformer(_SENTENCE_MODEL_NAME)
    v = _EMB_MODEL.encode(text).astype("float32").tolist()
    v = _l2_normalize(v)
    return serialize_float32(v)

# Optional preload to avoid first-request download latency
if os.getenv("SENTENCE_PRELOAD", "0") == "1":
    try:
        _ = _embed_384("warmup")
        print("[Embeddings] Preloaded successfully")
    except Exception as e:
        print(f"[Embeddings] Preload failed: {e}")

# ============================================================================
# DATABASE RETRIEVAL
# ============================================================================

def _search_similar_vec(table: str, id_col: str, qtext: str, k: int = 3) -> List[Dict]:
    """Vector similarity search using sqlite-vec"""
    db = get_db()
    qv = _embed_384(qtext)
    sql = f"""
        SELECT {id_col} AS id, distance
        FROM {table}
        WHERE embedding MATCH ?
          AND k = ?
    """
    try:
        return [dict(r) for r in db.execute(sql, (qv, k)).fetchall()]
    except Exception as e:
        print(f"[Vector search error] {e}")
        return []

def _fetch_plant_full(plant_id: int) -> Optional[Dict]:
    """Fetch complete plant record"""
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
    
    row = db.execute("""
        SELECT id, common_name_en, common_name_hi, common_name_mr,
               botanical_name, description, parts_used,
               therapeutic_actions, rasa, virya, vipaka, guna, dosha_effect,
               image_hero
        FROM plants
        WHERE id = ?
    """, (plant_id,)).fetchone()
    
    if not row:
        return None
    
    # Parse JSON fields
    for k in ["parts_used", "therapeutic_actions", "rasa", "guna", "dosha_effect"]:
        if row.get(k):
            row[k] = _as_list(row[k])
    
    return row

def _fetch_disease_full(disease_id: int) -> Optional[Dict]:
    """Fetch complete disease record"""
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
    
    row = db.execute("""
        SELECT id, name_en, name_hi, name_mr, category,
               description, symptoms, causes, dosha_involvement,
               severity_level, prevention_tips
        FROM diseases
        WHERE id = ?
    """, (disease_id,)).fetchone()
    
    if not row:
        return None
    
    # Parse JSON fields
    for k in ["symptoms", "causes", "dosha_involvement", "prevention_tips"]:
        if row.get(k):
            row[k] = _as_list(row[k])
    
    return row

def _diseases_for_plant(plant_id: int, k: int = 5) -> List[Dict]:
    """Get diseases that a plant can treat"""
    db = get_db()
    db.row_factory = lambda cursor, row: dict(zip([col[0] for col in cursor.description], row))
    
    rows = db.execute("""
        SELECT d.id, d.name_en, d.name_hi, d.name_mr, d.category, d.description,
               pdm.efficacy_level, pdm.evidence_type, pdm.mechanism
        FROM plant_disease_mapping pdm
        JOIN diseases d ON d.id = pdm.disease_id
        WHERE pdm.plant_id = ?
        ORDER BY pdm.efficacy_level DESC
        LIMIT ?
    """, (plant_id, k)).fetchall()
    
    return rows

def _prune_vec_hits(hits: List[Dict], max_distance: float) -> List[Dict]:
    """Filter out weak vector matches"""
    return [h for h in hits if "distance" not in h or (h.get("distance", 999) <= max_distance)]

# ============================================================================
# KNOWLEDGE CONTEXT BUILDING
# ============================================================================

def build_knowledge_context(
    plants: List[Dict],
    diseases: List[Dict],
    lang: str
) -> str:
    """
    Build compact, structured knowledge context for LLM
    This replaces the need for translation - LLM gets facts in English
    and responds in user's language
    """
    context_parts = []
    
    # === PLANTS SECTION ===
    if plants:
        context_parts.append("=== MEDICINAL PLANTS ===")
        for p in plants[:3]:  # Limit to top 3
            name_en = p.get("common_name_en", "")
            botanical = p.get("botanical_name", "")
            desc = (p.get("description") or "")[:200]
            actions = p.get("therapeutic_actions", [])
            
            context_parts.append(f"\n**{name_en}** ({botanical})")
            if desc:
                context_parts.append(f"Description: {desc}")
            if actions:
                if isinstance(actions, list):
                    context_parts.append(f"Therapeutic Actions: {', '.join(actions[:5])}")
                else:
                    context_parts.append(f"Therapeutic Actions: {actions}")
            
            # Ayurvedic properties
            props = []
            rasa = p.get("rasa")
            if rasa:
                if isinstance(rasa, list):
                    props.append(f"Rasa: {', '.join(rasa[:3])}")
                else:
                    props.append(f"Rasa: {rasa}")
            
            if p.get("virya"):
                props.append(f"Virya: {p['virya']}")
            
            if p.get("vipaka"):
                props.append(f"Vipaka: {p['vipaka']}")
            
            dosha = p.get("dosha_effect")
            if dosha and isinstance(dosha, dict):
                dosha_str = ", ".join([f"{k}: {v}" for k, v in dosha.items()])
                props.append(f"Dosha Effect: {dosha_str}")
            
            if props:
                context_parts.append(" | ".join(props))
    
    # === DISEASES SECTION ===
    if diseases:
        context_parts.append("\n\n=== MEDICAL CONDITIONS ===")
        for d in diseases[:2]:  # Limit to top 2
            name = d.get("name_en", "")
            category = d.get("category", "")
            desc = (d.get("description") or "")[:150]
            symptoms = d.get("symptoms", [])
            
            context_parts.append(f"\n**{name}** ({category})")
            if desc:
                context_parts.append(f"Description: {desc}")
            if symptoms and isinstance(symptoms, list):
                context_parts.append(f"Symptoms: {', '.join(symptoms[:5])}")
    
    return "\n".join(context_parts)

def build_remedy_context(disease_row: Dict) -> str:
    """Build context for remedy recommendations"""
    d_id = disease_row["id"]
    plants = top_plants_for_disease(d_id, k=5)
    preps = top_preparations_for_disease(d_id, k=3)
    
    parts = []
    
    # Disease info
    parts.append(f"=== CONDITION: {disease_row.get('name_en', '')} ===")
    if disease_row.get("description"):
        parts.append(f"Description: {disease_row['description'][:200]}")
    
    # Recommended plants
    if plants:
        parts.append("\n=== RECOMMENDED HERBS ===")
        for i, p in enumerate(plants[:5], 1):
            name = p.get("common_name_en") or p.get("botanical_name")
            botanical = p.get("botanical_name", "")
            efficacy = p.get("efficacy_level", "")
            evidence = p.get("evidence_type", "")
            
            parts.append(f"{i}. {name} ({botanical})")
            if efficacy:
                parts.append(f"   Efficacy: {efficacy}/5")
            if evidence:
                parts.append(f"   Evidence: {evidence}")
            
            # Add therapeutic actions if available
            actions = p.get("therapeutic_actions")
            if actions:
                if isinstance(actions, list):
                    parts.append(f"   Actions: {', '.join(actions[:3])}")
    
    # Preparations
    if preps:
        parts.append("\n=== PREPARATIONS ===")
        for pr in preps[:3]:
            name = pr.get("name_en", "")
            form = pr.get("form_type", "")
            parts.append(f"\n**{name}** ({form})")
            
            # Ingredients
            ings = ingredients_for_preparation(pr["id"])
            if ings:
                ing_list = []
                for ing in ings[:5]:
                    qty = f"{ing.get('quantity_value', '')} {ing.get('quantity_unit', '')}".strip()
                    ing_name = ing.get("common_name_en", ing.get("botanical_name", ""))
                    if qty:
                        ing_list.append(f"{ing_name} ({qty})")
                    else:
                        ing_list.append(ing_name)
                parts.append(f"Ingredients: {', '.join(ing_list)}")
            
            # Dosage
            dosage = pr.get("dosage_json")
            if dosage:
                if isinstance(dosage, str):
                    try:
                        dosage = json.loads(dosage)
                    except:
                        pass
                if isinstance(dosage, dict):
                    parts.append(f"Dosage: Adult - {dosage.get('adult', 'As prescribed')}")
            
            # Timing & Anupana
            if pr.get("timing"):
                parts.append(f"Timing: {pr['timing']}")
            if pr.get("anupana"):
                parts.append(f"Anupana: {pr['anupana']}")
    
    return "\n".join(parts)

# ============================================================================
# MULTILINGUAL LLM RESPONSE GENERATION
# ============================================================================

def generate_multilingual_response(
    user_query: str,
    detected_lang: str,
    intent: str,
    knowledge_context: str,
    conversation_history: str = ""
) -> str:
    """
    Single Ollama call that:
    1. Takes original query (any language)
    2. Gets English knowledge context
    3. Responds in user's language
    
    This eliminates the translate->generate->translate pipeline
    """
    import requests
    import os
    
    lang_names = {"en": "English", "hi": "Hindi", "mr": "Marathi"}
    response_lang = lang_names.get(detected_lang, "English")
    
    system_prompt = f"""You are HerboAI, an expert Ayurvedic consultant specializing in medicinal herbs and traditional medicine.

Your role:
1. Answer questions about medicinal plants, diseases, and herbal preparations
2. Provide evidence-based information from the KNOWLEDGE CONTEXT provided below
3. Give practical, safe, and specific recommendations
4. CRITICAL: Respond ENTIRELY in {response_lang} language
5. Be concise but complete (3-5 sentences for simple queries, more for complex ones)
6. Always include dosage, timing, and preparation details when available
7. Mention contraindications and precautions when relevant

IMPORTANT RULES:
- Use ONLY information from the knowledge context - never invent plant names or properties
- If information is not in the context, politely say you don't have that information
- Never diagnose serious conditions - recommend consulting healthcare professionals
- For emergency symptoms, always advise immediate medical attention
- Respect the cultural and traditional knowledge while being scientifically accurate

Response format:
- Start with direct answer to the question
- Include plant names: Common name (Botanical name)
- Mention preparation method if applicable  
- Add brief safety disclaimer at the end
- Use natural, conversational {response_lang}

Remember: Your entire response must be in {response_lang}, including plant names in the local language when possible."""

    user_prompt = f"""User Query: {user_query}

Intent: {intent}

{knowledge_context}

{conversation_history}

Based on the knowledge context above, provide a helpful answer in {response_lang}. Be specific, practical, and include preparation/dosage details when available."""

    try:
        # Resolve Ollama chat endpoint robustly across env var variants
        host = os.getenv("OLLAMA_HOST")
        url_generate = os.getenv("OLLAMA_URL")
        base_url = os.getenv("OLLAMA_BASE_URL") or os.getenv("OLLAMA_CHAT_URL")
        if not base_url:
            if host:
                base_url = f"{host.rstrip('/')}/api/chat"
            elif url_generate:
                base_url = (
                    url_generate.replace("/api/generate", "/api/chat")
                    if "/api/generate" in url_generate
                    else f"{url_generate.rstrip('/')}/chat"
                )
            else:
                base_url = "http://localhost:11434/api/chat"

        model = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
        timeout = int(os.getenv("OLLAMA_HTTP_TIMEOUT", "300"))
        
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "options": {
                "temperature": 0.3,  # Lower for consistency
                "num_ctx": 6144,     # Balanced context size
                "top_p": 0.9,
                "top_k": 40
            }
        }
        
        print(f"[Ollama] Calling {model} for {response_lang} response...")
        start = time.time()
        
        payload["keep_alive"] = "2m"
        response = requests.post(base_url, json=payload, timeout=timeout)
        response.raise_for_status()
        
        elapsed = time.time() - start
        print(f"[Ollama] Response received in {elapsed:.2f}s")
        
        data = response.json()
        content = (data.get("message") or {}).get("content", "")
        
        if isinstance(data, dict):
            if "message" in data and isinstance(data["message"], dict):
                content = data["message"].get("content", "") or ""
            elif "choices" in data and data["choices"]:
                content = data["choices"][0].get("message", {}).get("content", "") or ""

        if not content:
            raise Exception(f"Empty response from Ollama (model={model})")

        # Debug-print a small preview of the generated answer
        preview = content.strip()[:200]
        print(f"[Ollama] Answer preview: {preview}...")

        return content.strip()
        
    except Exception as e:
        print(f"[Ollama Error] {e}")
       # Log full cause for server console & attach small marker back
        import traceback
        print(f"[Ollama Error] {e}\n{traceback.format_exc()}")
        
        # Language-appropriate fallback
        fallbacks = {
            "hi": "मुझे खेद है, मैं अभी आपकी मदद नहीं कर सकता। कृपया बाद में पुनः प्रयास करें। यदि यह समस्या बनी रहती है, तो कृपया अपने स्वास्थ्य सेवा प्रदाता से परामर्श करें।",
            "mr": "मला माफ करा, मी आत्ता तुमची मदत करू शकत नाही. कृपया नंतर पुन्हा प्रयत्न करा. जर ही समस्या कायम राहिली तर कृपया आपल्या आरोग्य सेवा प्रदात्याशी सल्लामसलत करा.",
            "en": "I apologize, but I'm unable to provide an answer at this moment. Please try again later. If the issue persists, please consult with your healthcare provider."
        }
        
        marker = {
           "hi": "\n\n[नोट: LLM उपलब्ध नहीं / विलंबित]",
           "mr": "\n\n[टीप: LLM उपलब्ध नाही / उशीर]",
            "en": "\n\n[Note: LLM unavailable / delayed]"
        }
        return (fallbacks.get(detected_lang, fallbacks["en"]) + marker.get(detected_lang, marker["en"]))

# ============================================================================
# MAIN PIPELINE
# ============================================================================

def run_pipeline(user_text: str, session_id: str | None) -> Dict[str, Any]:
    """
    Optimized multilingual RAG pipeline:
    1. Detect language & intent (fast)
    2. Extract entities with FTS + vector fallback
    3. Build knowledge context
    4. Single LLM call for multilingual response
    5. Return structured result
    """
    t0 = time.time()
    
    # Step 1: Language detection (no translation yet)
    lang = detect_language(user_text)
    print(f"[Pipeline] Language: {lang}")
    translator = get_indic_translation_service()
    # Step 2: Translate ONLY for intent classification (internal routing)
    # This is quick since it's just for classification, not the full response
    if lang != "en":
        text_for_intent = translator.to_en(user_text, src_lang=lang)
        print(f"[Translate] Query -> EN: {text_for_intent}")
    else:
        text_for_intent = user_text
    intent = classify_intent(text_for_intent)
    print(f"[Pipeline] Intent: {intent}")
    
    # Step 3: Entity extraction (works on original multilingual query)
    plants, diseases = extract_entities(user_text, text_for_intent, prefer_en=(lang != "en"))
    print(f"[Pipeline] Found {len(plants)} plants, {len(diseases)} diseases (FTS)")
    
    # Step 4: Vector fallback if FTS didn't find anything
    if not diseases:
        vec_diseases = _search_similar_vec("disease_vec", "disease_id", user_text, 3)
        vec_diseases = _prune_vec_hits(vec_diseases, 1.8)  # Tune threshold
        print(f"[Pipeline] Found {len(vec_diseases)} diseases (vector)")
        diseases = vec_diseases
    
    if not plants:
        vec_plants = _search_similar_vec("plant_vec", "plant_id", user_text, 3)
        vec_plants = _prune_vec_hits(vec_plants, 1.8)
        print(f"[Pipeline] Found {len(vec_plants)} plants (vector)")
        plants = vec_plants
    
    # Step 5: Hydrate entities (fetch full records if we only have IDs)
    plants_full = []
    for p in plants[:3]:  # Limit to top 3
        if "botanical_name" in p and p.get("botanical_name"):
            plants_full.append(p)
        elif "id" in p:
            full = _fetch_plant_full(p["id"])
            if full:
                plants_full.append(full)
    
    diseases_full = []
    for d in diseases[:3]:
        if "name_en" in d and d.get("name_en"):
            diseases_full.append(d)
        elif "id" in d:
            full = _fetch_disease_full(d["id"])
            if full:
                diseases_full.append(full)
    
    # Step 6: Context recall from conversation
    last = get_last_context(session_id) if session_id else None
    if not diseases_full and last and last.get("entities", {}).get("diseases"):
        diseases_full = last["entities"]["diseases"][:2]
    if not plants_full and last and last.get("entities", {}).get("plants"):
        plants_full = last["entities"]["plants"][:2]
    if intent == "none" and last:
        intent = last.get("intent", "none")
    
    print(f"[Pipeline] After hydration: {len(plants_full)} plants, {len(diseases_full)} diseases")
    
    # Step 7: Build knowledge context & generate response
    answer_text = ""
    structured = {}
    
    if intent in ("remedy_lookup", "preparation_info") and diseases_full:
        # Remedy lookup - build detailed context
        disease_row = diseases_full[0]
        knowledge_ctx = build_remedy_context(disease_row)
        
        print(f"[Pipeline] Knowledge context: {len(knowledge_ctx)} chars")
        
        # Generate multilingual response
        conv_history = ""
        if last:
            conv_history = f"Previous query: {last.get('user_text', '')}"
        
        answer_text = generate_multilingual_response(
            user_text, lang, intent, knowledge_ctx, conv_history
        )
        
        # Also prepare structured data for frontend
        structured = {
            "disease": disease_row,
            "plants": top_plants_for_disease(disease_row["id"], k=5),
            "preparations": top_preparations_for_disease(disease_row["id"], k=3)
        }
    
    elif intent == "plant_info" and plants_full:
        # Plant info - simpler context
        plant = plants_full[0]
        knowledge_ctx = build_knowledge_context([plant], [], lang)
        
        answer_text = generate_multilingual_response(
            user_text, lang, intent, knowledge_ctx
        )
        
        structured = {"plant": plant}
    
    elif plants_full or diseases_full:
        # Generic query with entities - provide general context
        knowledge_ctx = build_knowledge_context(plants_full, diseases_full, lang)
        
        answer_text = generate_multilingual_response(
            user_text, lang, intent, knowledge_ctx
        )
        
        structured = {
            "plants": plants_full,
            "diseases": diseases_full
        }
    
    else:
        # No entities found - use fallback
        fallbacks = {
            "hi": "मुझे खेद है, मुझे इस विषय पर कोई जानकारी नहीं मिली। कृपया अधिक विशिष्ट प्रश्न पूछें या किसी पौधे या रोग का नाम बताएं।",
            "mr": "मला माफ करा, मला या विषयावर माहिती सापडली नाही. कृपया अधिक विशिष्ट प्रश्न विचारा किंवा एखाद्या वनस्पतीचे किंवा रोगाचे नाव सांगा.",
            "en": "I'm sorry, I couldn't find information on this topic. Please ask a more specific question or mention a plant or condition name."
        }
        answer_text = fallbacks.get(lang, fallbacks["en"])
    
    # Step 8: Persist conversation
    entities_dump = {
        "plants": plants_full,
        "diseases": diseases_full
    }
    
    json_data = {
        "answer": answer_text,
        "structured": structured,
    }
    # Do NOT re-translate the answer: generate_multilingual_response already
    # produced it in the user's language. This avoids a second heavy Ollama call
    # that can cause UI timeouts. We keep keys/structure in English.

    duration_ms = int((time.time() - t0) * 1000)
    persist_turn(
        session_id or "default",
        user_text,
        lang,
        intent,
        entities_dump,
        answer_text,
        structured,
        duration_ms
    )
    print(f"[Pipeline] Complete in {duration_ms}ms")

    return {
        "answer": json_data.get("answer", ""),
        "intent": intent,
        "detected_language": lang,
        "structured": json_data.get("structured", {}),
        "metadata": {
            "session_id": session_id,
            "duration_ms": duration_ms,
            "entities_found": {
                "plants": len(plants_full),
                "diseases": len(diseases_full)
            }
        }
    }
