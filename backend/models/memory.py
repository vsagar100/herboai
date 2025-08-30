session_memory = {}

def update_memory(session_id: str, query: str, herb_name: str):
    """Save last herb discussed per session"""
    session_memory[session_id] = {
        "last_query": query,
        "last_herb": herb_name
    }

def resolve_context(session_id: str, query: str):
    """If user asks follow-up like 'इसके फायदे', resolve herb"""
    mem = session_memory.get(session_id, {})
    if "इसके" in query or "इसके" in query:
        return mem.get("last_herb")
    return None
