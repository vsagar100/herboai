# services/llm_gateway.py
import os
from typing import Optional
from llama_cpp import Llama

_llm: Optional[Llama] = None

def _get_llm() -> Llama:
    global _llm
    if _llm is not None:
        return _llm

    _llm = Llama(
        model_path="models/Phi-3-mini-4k-instruct-q4.gguf",
        n_ctx=int(os.getenv("HERBOAI_CTX_SIZE", "4096")),
        n_threads=int(os.getenv("HERBOAI_THREADS", "4")),
        n_batch=int(os.getenv("HERBOAI_BATCH", "128")),
        verbose=False,
    )
    return _llm


def generate_herboai_answer(
    system_prompt: str,
    user_query_en: str,
    context: str,
) -> str:
    llm = _get_llm()

    messages = [
        {
            "role": "system",
            "content": system_prompt.strip(),
        },
        {
            "role": "user",
            "content": (
                "Use ONLY the knowledge in the CONTEXT below.\n\n"
                f"CONTEXT:\n{context.strip()}\n\n"
                f"QUESTION:\n{user_query_en.strip()}"
            ),
        },
    ]

    result = llm.create_chat_completion(
        messages=messages,
        max_tokens=int(os.getenv("HERBOAI_MAX_TOKENS", "384")),
        temperature=float(os.getenv("HERBOAI_LLM_TEMP", "0.6")),
        top_p=float(os.getenv("HERBOAI_TOP_P", "0.9")),
    )

    return result["choices"][0]["message"]["content"].strip()


def generate_plant_remedy(plant_name: str, plant_info: dict, disease_name: str, disease_info: dict) -> str:
    """
    Generate a remedy using LLM when database doesn't have explicit mapping.
    Uses RAG-style approach with plant and disease context.
    """
    llm = _get_llm()
    
    # Build context from database info
    context_parts = []
    
    # Plant context
    if plant_info:
        context_parts.append(f"PLANT: {plant_name}")
        if plant_info.get('botanical_name'):
            context_parts.append(f"Botanical Name: {plant_info['botanical_name']}")
        if plant_info.get('properties'):
            context_parts.append(f"Properties: {plant_info['properties']}")
        if plant_info.get('common_uses'):
            context_parts.append(f"Common Uses: {plant_info['common_uses']}")
    
    # Disease context
    if disease_info:
        context_parts.append(f"\nDISEASE: {disease_name}")
        if disease_info.get('description'):
            context_parts.append(f"Description: {disease_info['description']}")
        if disease_info.get('symptoms'):
            context_parts.append(f"Symptoms: {disease_info['symptoms']}")
    
    context = "\n".join(context_parts)
    
    system_prompt = """You are an expert Ayurvedic practitioner. Generate a safe, traditional remedy based on classical Ayurvedic principles.
Your response must be structured and practical, following this EXACT format:

**Preparation Method:**
[Detailed step-by-step instructions]

**Dosage:**
- Adult: [specific dosage]
- Child: [specific dosage or contraindication]

**Timing:** [when to take - morning/evening/with meals]

**Anupana:** [what to take it with - water/honey/milk/ghee]

**Precautions:**
[Important safety notes, contraindications, when to consult a practitioner]

Keep the remedy simple, safe, and based on traditional Ayurvedic use. If internal use requires expert supervision, clearly state that."""

    user_query = f"How can {plant_name} be used to treat {disease_name}? Provide a traditional Ayurvedic remedy."
    
    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": f"{context}\n\nQUESTION: {user_query}"}
    ]
    
    try:
        result = llm.create_chat_completion(
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            top_p=0.9,
        )
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LLM] Error generating remedy: {e}")
        return None


def generate_general_plant_remedy(plant_name: str, plant_info: dict) -> str:
    """
    Generate general remedy suggestions when disease is not specific.
    """
    llm = _get_llm()
    
    context_parts = [f"PLANT: {plant_name}"]
    if plant_info:
        if plant_info.get('properties'):
            context_parts.append(f"Properties: {plant_info['properties']}")
        if plant_info.get('common_uses'):
            context_parts.append(f"Common Uses: {plant_info['common_uses']}")
        if plant_info.get('botanical_name'):
            context_parts.append(f"Botanical Name: {plant_info['botanical_name']}")
    
    context = "\n".join(context_parts)
    
    system_prompt = """You are an expert Ayurvedic practitioner. Provide 2-3 common, safe preparation methods for the given plant.
Format each preparation as:

**[Preparation Name]** ([form - decoction/powder/paste/oil])
- How to prepare: [brief steps]
- Common uses: [what it helps with]
- Dosage: [typical adult dosage]
- Precautions: [key safety notes]

Keep suggestions practical, safe, and based on traditional Ayurvedic use."""

    user_query = f"What are the most common traditional preparations and uses of {plant_name}?"
    
    messages = [
        {"role": "system", "content": system_prompt.strip()},
        {"role": "user", "content": f"{context}\n\nQUESTION: {user_query}"}
    ]
    
    try:
        result = llm.create_chat_completion(
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            top_p=0.9,
        )
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"[LLM] Error generating general remedy: {e}")
        return None
