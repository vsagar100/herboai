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
