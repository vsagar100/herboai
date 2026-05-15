"""Simple conversation context"""
from datetime import datetime

_conversation_store = {}

def get_last_context(session_id):
    if not session_id or session_id not in _conversation_store:
        return None
    return _conversation_store[session_id][-1] if _conversation_store[session_id] else None

def persist_turn(session_id, user_text, lang, intent, entities, answer, structured, duration_ms):
    if not session_id:
        session_id = "default"
    if session_id not in _conversation_store:
        _conversation_store[session_id] = []
    
    _conversation_store[session_id].append({
        "user_text": user_text,
        "lang": lang,
        "intent": intent,
        "entities": entities,
        "answer": answer,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 10
    _conversation_store[session_id] = _conversation_store[session_id][-10:]