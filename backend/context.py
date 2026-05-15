from typing import Optional, Dict, Any
import json
from db import get_db

def get_last_context(session_id: str) -> Optional[Dict[str, Any]]:
    if not session_id:
        return None
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT intent, entities
        FROM conversations
        WHERE session_id = ?
        ORDER BY created_at DESC, id DESC
        LIMIT 1
    """, (session_id,))
    row = cur.fetchone()
    cur.close()
    if not row:
        return None
    return {
        "intent": row["intent"],
        "entities": json.loads(row["entities"]) if row["entities"] else {}
    }

def persist_turn(session_id: str, user_query: str, detected_language: str,
                 intent: str, entities: Dict[str, Any],
                 response_text: str, structured_data: Dict[str, Any],
                 response_time_ms: int | None = None):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO conversations (session_id, user_query, detected_language, intent, entities, response_text, structured_data, response_time_ms)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        session_id,
        user_query,
        detected_language,
        intent,
        json.dumps(entities, ensure_ascii=False, default=str),
        response_text,
        json.dumps(structured_data, ensure_ascii=False, default=str),
        response_time_ms
    ))
    db.commit()
    cur.close()
