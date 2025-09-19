import threading
class SimpleSessionManager:
    """Simplified session manager"""
    
    def __init__(self):
        self.sessions = {}
        self.lock = threading.RLock()
    
    def get_user_context(self, request_info):
        """Get user context"""
        return {
            'user_id': 'anonymous',
            'total_queries': 0,
            'preferred_language': 'en'
        }
    
    def update_session_context(self, user_id, query, response_data):
        """Update session context"""
        pass  # Simplified - no session tracking for now
    
    def get_session_statistics(self):
        """Get session statistics"""
        return {
            'active_sessions': 0,
            'total_conversations': 0,
            'languages_used': [],
            'popular_intents': {},
            'popular_herbs': {}
        }

