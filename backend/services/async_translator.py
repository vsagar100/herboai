# services/async_translator.py
import queue
import threading
from typing import Dict, Optional

from services.indic_translation_service import get_indic_translation_service


class AsyncTranslator:
    """
    Fire-and-forget translator with a small worker pool. The heavy model load
    happens in the background to avoid blocking the first inbound request.
    """

    def __init__(self, max_workers: int = 3):
        self.translator = None
        self._loading = False
        self._ready = threading.Event()
        self.request_queue: "queue.Queue[tuple[str, str, queue.Queue]]" = queue.Queue()
        self.workers = []

        for _ in range(max_workers):
            worker = threading.Thread(target=self._worker, daemon=True)
            worker.start()
            self.workers.append(worker)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _load_translator(self):
        try:
            self.translator = get_indic_translation_service()
            print("[AsyncTranslator] Translator loaded")
            self._ready.set()
        except Exception as exc:
            print(f"[AsyncTranslator] Translator load failed: {exc}")
        finally:
            self._loading = False

    def _ensure_ready(self) -> bool:
        if self.translator:
            return True
        if not self._loading:
            self._loading = True
            threading.Thread(target=self._load_translator, daemon=True).start()
            print("[AsyncTranslator] Warming up translator in background")
        return self._ready.is_set()

    def _worker(self):
        while True:
            try:
                job = self.request_queue.get(timeout=1)
                if job is None:
                    break

                text, lang, result_queue = job

                if not self.translator:
                    # Translator not ready; drop quickly to avoid hanging callers
                    result_queue.put(("error", "translator not ready"))
                    self.request_queue.task_done()
                    continue

                try:
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

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def warmup(self):
        """Kick off background loading without enqueuing work."""
        self._ensure_ready()

    def is_ready(self) -> bool:
        return self._ready.is_set()

    def translate_async(
        self, text: str, lang: str, timeout: int = 30, warm_timeout: int = 5
    ) -> Optional[str]:
        """
        Non-blocking translation with timeout. If the model is still warming
        up, return None immediately so callers can fall back to English.
        """
        if lang == "en":
            return text

        if not self._ensure_ready():
            # Give the loader a brief chance before bailing out
            self._ready.wait(timeout=warm_timeout)
            if not self._ready.is_set():
                print("[AsyncTranslator] Translator not ready; responding in English")
                return None

        result_queue: "queue.Queue[tuple[str, str]]" = queue.Queue()
        self.request_queue.put((text, lang, result_queue))

        try:
            status, result = result_queue.get(timeout=timeout)
            if status == "success":
                return result
            print(f"[AsyncTranslator] Error: {result}")
        except queue.Empty:
            print(f"[AsyncTranslator] Timeout after {timeout}s")
        return None


# Global instance
_async_translator: Optional[AsyncTranslator] = None


def get_async_translator() -> AsyncTranslator:
    global _async_translator
    if _async_translator is None:
        _async_translator = AsyncTranslator()
    return _async_translator
