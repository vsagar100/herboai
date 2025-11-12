# services/async_translator.py
import threading
import queue
from typing import Dict, Optional
from services.indic_translation_service import get_indic_translation_service

class AsyncTranslator:
    def __init__(self, max_workers=3):
        self.translator = get_indic_translation_service()
        self.request_queue = queue.Queue()
        self.workers = []
        
        # Start worker threads
        for _ in range(max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)
    
    def _worker(self):
        while True:
            try:
                job = self.request_queue.get(timeout=1)
                if job is None:
                    break
                
                text, lang, result_queue = job
                try:
                    # Translate from English to requested lang; assume English input
                    translated = (
                        text
                        if lang == "en"
                        else self.translator.translate_text(text, "en", lang)
                    )
                    result_queue.put(("success", translated))
                except Exception as e:
                    result_queue.put(("error", str(e)))
                finally:
                    self.request_queue.task_done()
            except queue.Empty:
                continue
    
    def translate_async(self, text: str, lang: str, timeout: int = 30) -> Optional[str]:
        """Non-blocking translation with timeout"""
        result_queue = queue.Queue()
        self.request_queue.put((text, lang, result_queue))
        
        try:
            status, result = result_queue.get(timeout=timeout)
            if status == "success":
                return result
            else:
                print(f"[AsyncTranslator] Error: {result}")
                return None
        except queue.Empty:
            print(f"[AsyncTranslator] Timeout after {timeout}s")
            return None

# Global instance
_async_translator = None

def get_async_translator():
    global _async_translator
    if _async_translator is None:
        _async_translator = AsyncTranslator()
    return _async_translator
