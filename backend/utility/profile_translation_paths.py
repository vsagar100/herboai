import os
import sys
import time
from pathlib import Path

# Ensure backend root is on sys.path when running as a script
HERE = Path(__file__).resolve()
BACKEND_ROOT = HERE.parent.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from services.indic_trans2 import IndicTranslator
from init import create_app


def load_sample_text() -> str:
    """Load sample text from translation_text.txt next to this file."""
    path = Path(__file__).with_name("translation_text.txt")
    if path.exists():
        text = path.read_text(encoding="utf-8").strip()
        if text:
            return text
    return "Tell me about Ashwagandha and its uses for stress."


def profile_direct(text: str) -> None:
    print("=== Direct IndicTranslator (en -> hi) ===")
    t0 = time.time()
    translator = IndicTranslator(direction="en-indic")
    load_time = time.time() - t0

    t1 = time.time()
    _ = translator.translate(text, src_lang="eng_Latn", tgt_lang="hin_Deva")
    translate_time = time.time() - t1

    print(f"Model load time:    {load_time:.2f} s")
    print(f"Single translate:   {translate_time:.2f} s")


def profile_pipeline(text: str) -> None:
    print("\n=== Chat run_pipeline (full RAG + translation) ===")
    app = create_app()
    from services.chat import run_pipeline  # Import after app creation

    with app.app_context():
        t0 = time.time()
        result = run_pipeline(user_text=text, session_id="profile-test")
        total_time = time.time() - t0

    duration_ms = result.get("metadata", {}).get("duration_ms")
    print(f"run_pipeline total wall time: {total_time:.2f} s")
    if duration_ms is not None:
        print(f"Reported pipeline duration_ms: {duration_ms} ms")


def main() -> None:
    text = load_sample_text()
    print(f"Sample text ({len(text)} chars): {text[:120]!r}")
    profile_direct(text)
    profile_pipeline(text)


if __name__ == "__main__":
    main()
