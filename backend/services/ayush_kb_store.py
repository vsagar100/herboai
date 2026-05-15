from __future__ import annotations

import json
from datetime import datetime
import sqlite3


def _now() -> str:
    return datetime.utcnow().isoformat(sep=" ", timespec="seconds")


def seed_ayush_kb(conn: sqlite3.Connection) -> None:
    """Seed a small, editable AYUSH knowledge base.

    - English is stored as the canonical source.
    - Hindi/Marathi are generated on-demand at read-time (no DB inserts),
      so entity_i18n remains unaffected.

    Safe to run multiple times.
    """

    cur = conn.cursor()

    # Seed articles only if the table is empty
    count = cur.execute("SELECT COUNT(*) AS c FROM ayush_kb_articles").fetchone()[0]
    if int(count or 0) == 0:
        ts = _now()
        articles = [
            {
                "slug": "ayush-what",
                "title_en": "What is AYUSH?",
                "keywords_en": "ayush, ayurveda, yoga, naturopathy, unani, siddha, homeopathy, sowa-rigpa",
                "body_en": (
                    "AYUSH is an umbrella term for India’s traditional systems of medicine:\n\n"
                    "- Ayurveda\n"
                    "- Yoga & Naturopathy\n"
                    "- Unani\n"
                    "- Siddha\n"
                    "- Sowa-Rigpa\n"
                    "- Homoeopathy\n\n"
                    "In HerboAI, AYUSH knowledge is presented in a practical way:\n"
                    "- plant information (identity, parts used, traditional uses)\n"
                    "- preparations (how they’re made and typical household usage)\n"
                    "- disease/condition support (non-emergency guidance aligned with the knowledge base)\n"
                    "- lifestyle basics (sleep, diet, routine)\n\n"
                    "Safety note: This is educational information, not a medical diagnosis. If symptoms are severe, worsening, or unclear, consult a qualified clinician/vaidya."
                ),
            },
            {
                "slug": "ayurveda",
                "title_en": "Ayurveda: a quick overview",
                "keywords_en": "ayurveda, dosha, vata, pitta, kapha, prakriti, dinacharya",
                "body_en": (
                    "Ayurveda is a classical system that emphasizes balance and routine. Common concepts include:\n\n"
                    "- **Prakriti**: your constitution (often described via Vata–Pitta–Kapha tendencies)\n"
                    "- **Dinacharya**: daily routine (sleep, meals, movement, hygiene)\n"
                    "- **Ahara & Vihara**: diet and lifestyle as foundational support\n\n"
                    "In practice, Ayurveda advice is usually personalized. General guidance should be gentle and safe (especially for pregnancy, children, elders, or chronic illnesses)."
                ),
            },
            {
                "slug": "yoga-naturopathy",
                "title_en": "Yoga & Naturopathy: what they focus on",
                "keywords_en": "yoga, pranayama, asana, naturopathy, lifestyle",
                "body_en": (
                    "**Yoga** focuses on physical postures (asana), breathing practices (pranayama), and mental well-being.\n\n"
                    "**Naturopathy** emphasizes lifestyle and natural approaches such as:\n"
                    "- sleep and stress management\n"
                    "- movement and posture\n"
                    "- food habits and hydration\n\n"
                    "For any medical condition, choose practices that are safe for your body and consult a professional if you have pain, dizziness, heart/lung issues, or recent surgery."
                ),
            },
            {
                "slug": "other-ayush-systems",
                "title_en": "Unani, Siddha, Sowa-Rigpa, Homoeopathy (high level)",
                "keywords_en": "unani, siddha, sowa-rigpa, homeopathy, homoeopathy",
                "body_en": (
                    "AYUSH also includes multiple well-established traditions:\n\n"
                    "- **Unani**: a Greco-Arab system with its own diagnostic and dietary framework.\n"
                    "- **Siddha**: a traditional system with deep roots in South India.\n"
                    "- **Sowa-Rigpa**: traditional Tibetan medicine.\n"
                    "- **Homoeopathy**: a distinct therapeutic approach using highly diluted preparations.\n\n"
                    "HerboAI can store and present educational information across systems, but clinical decisions should be made by qualified practitioners."
                ),
            },
            {
                "slug": "lifestyle-basics",
                "title_en": "Lifestyle basics: good habits and common pitfalls",
                "keywords_en": "lifestyle, routine, sleep, diet, exercise, stress",
                "body_en": (
                    "Healthy lifestyle guidance (general, non-medical):\n\n"
                    "**Good habits**\n"
                    "- consistent sleep schedule\n"
                    "- balanced meals; avoid extreme dieting\n"
                    "- daily movement (walks / mobility)\n"
                    "- hydration and mindful eating\n"
                    "- stress reduction (breathing, meditation, nature, social support)\n\n"
                    "**Common pitfalls**\n"
                    "- irregular sleep\n"
                    "- frequent ultra-processed foods and excess sugar\n"
                    "- inactivity for long hours\n"
                    "- self-medicating serious symptoms without evaluation\n\n"
                    "If you have a diagnosed condition (e.g., diabetes, hypertension), follow your clinician’s plan and use lifestyle changes as supportive care."
                ),
            },
            {
                "slug": "safety",
                "title_en": "Safety: when to consult a doctor",
                "keywords_en": "safety, emergency, consult doctor, red flags",
                "body_en": (
                    "Please seek medical advice (or urgent care) if you have:\n\n"
                    "- severe chest pain, breathlessness, fainting\n"
                    "- very high fever that persists\n"
                    "- signs of stroke (face droop, weakness, speech difficulty)\n"
                    "- uncontrolled bleeding, severe dehydration\n"
                    "- pregnancy-related concerns, severe allergic reactions\n\n"
                    "Herbal/home remedies should not replace emergency care."
                ),
            },
        ]

        for a in articles:
            cur.execute(
                """
                INSERT INTO ayush_kb_articles (slug, title_en, body_en, keywords_en, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    a["slug"],
                    a["title_en"],
                    a["body_en"],
                    a.get("keywords_en"),
                    ts,
                    ts,
                ),
            )

        conn.commit()

    # Seed nav if missing
    nav_row = cur.execute(
        "SELECT nav_json, nav_json_en FROM ayush_kb_nav WHERE key = ?",
        ("ayush",),
    ).fetchone()

    if nav_row and (not (nav_row["nav_json_en"] or "").strip()) and (nav_row["nav_json"] or "").strip():
        # One-time backfill for legacy DBs
        cur.execute(
            "UPDATE ayush_kb_nav SET nav_json_en = ? WHERE key = ?",
            (nav_row["nav_json"], "ayush"),
        )
        conn.commit()

    if not nav_row:
        nav = [
            {
                "title": "AYUSH Systems",
                "items": [
                    {"label": "What is AYUSH?", "slug": "ayush-what"},
                    {"label": "Ayurveda", "slug": "ayurveda"},
                    {"label": "Yoga & Naturopathy", "slug": "yoga-naturopathy"},
                    {"label": "Other AYUSH systems", "slug": "other-ayush-systems"},
                ],
            },
            {
                "title": "Lifestyle",
                "items": [
                    {"label": "Lifestyle basics", "slug": "lifestyle-basics"},
                    {"label": "Safety (when to consult)", "slug": "safety"},
                ],
            },
            {
                "title": "Quick Links",
                "items": [
                    {"label": "Plant Library", "href": "/library"},
                    {"label": "Ask HerboAI", "href": "/chat"},
                ],
            },
        ]
        cur.execute(
            """
            INSERT OR REPLACE INTO ayush_kb_nav (key, nav_json, nav_json_en, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                "ayush",
                json.dumps(nav, ensure_ascii=False),
                json.dumps(nav, ensure_ascii=False),
                _now(),
            ),
        )
        conn.commit()

    cur.close()
