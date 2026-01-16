def generate_followup_questions(severity_band: str) -> list[str]:
    base = [
        "Symptoms since how many days?",
        "Is the problem getting better or worse?",
        "Any fever or pain severity (mild / moderate / severe)?",
        "Age and gender?",
        "Any existing illness (BP, diabetes, thyroid)?",
    ]

    if severity_band == "high":
        base.append("Are you currently taking any medicines?")

    return base[:6]
