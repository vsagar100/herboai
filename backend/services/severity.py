from __future__ import annotations

RED_FLAG_KEYWORDS = {
    "chest pain", "breathlessness", "unconscious",
    "severe bleeding", "blood vomiting", "paralysis",
    "sudden weakness", "fits", "seizure"
}

HIGH_SEVERITY_HINTS = {
    "high fever", "persistent fever", "severe pain",
    "worsening", "not improving", "extreme weakness"
}

def assess_severity(text: str, context: dict | None = None) -> dict:
    t = text.lower()

    red_flags = [k for k in RED_FLAG_KEYWORDS if k in t]
    if red_flags:
        return {
            "band": "emergency",
            "red_flags": red_flags,
            "ask_followups": False,
        }

    high = [k for k in HIGH_SEVERITY_HINTS if k in t]
    if high:
        return {
            "band": "high",
            "red_flags": [],
            "ask_followups": True,
        }

    # Ayurveda-friendly default
    return {
        "band": "medium",
        "red_flags": [],
        "ask_followups": True,
    }
