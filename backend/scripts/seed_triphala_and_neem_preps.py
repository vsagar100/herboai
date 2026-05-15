"""Idempotent seed: Triphala formulation + key preparations (Triphala Churna, Neem Oil topical).

Why this exists:
- Some prep-like queries (e.g. "Triphala powder dosage", "Neem oil usage for skin")
  can mis-resolve to an unrelated plant if the DB lacks a first-class entity.
- This script creates the missing canonical entities and updates multilingual
  rows in `entity_i18n`, then rebuilds per-language FTS + vec indexes.

Run (from backend/):
  python scripts/seed_triphala_and_neem_preps.py

Notes:
- Uses Flask app context so `get_db()` and sqlite-vec are available.
- Keeps translations minimal + safe; you can later edit/verify from admin.
"""

from __future__ import annotations

import json
from typing import Optional

from init import create_app
from db import get_db
from utils.i18n import upsert_i18n
from services.indexer import rebuild_fts_for_entity, rebuild_vec_for_entity


def _rowid_int(row, key: str = "id") -> int:
    try:
        return int(row[key])
    except Exception:
        return int(row[0])


def _find_plant_id_by_common_name_en(name_en: str) -> Optional[int]:
    db = get_db()
    row = db.execute(
        "SELECT id FROM plants WHERE LOWER(common_name_en)=LOWER(?) LIMIT 1",
        (name_en,),
    ).fetchone()
    return _rowid_int(row) if row else None


def _find_plant_id_by_botanical_name(botanical_name: str) -> Optional[int]:
    db = get_db()
    row = db.execute(
        "SELECT id FROM plants WHERE LOWER(botanical_name)=LOWER(?) LIMIT 1",
        (botanical_name,),
    ).fetchone()
    return _rowid_int(row) if row else None


def _ensure_triphala_plant() -> int:
    """Create a pseudo-plant to represent Triphala formulation."""
    db = get_db()

    existing = _find_plant_id_by_common_name_en("Triphala")
    if existing:
        return existing

    botanical_name = "Triphala formulation"
    existing = _find_plant_id_by_botanical_name(botanical_name)
    if existing:
        return existing

    db.execute(
        """
        INSERT INTO plants(
          botanical_name,
          common_name_en, common_name_hi, common_name_mr,
          sanskrit_name,
          description,
          therapeutic_actions,
          ayush_system
        ) VALUES(?,?,?,?,?,?,?,?)
        """,
        (
            botanical_name,
            "Triphala",
            "त्रिफला",
            "त्रिफळा",
            "त्रिफला",
            "Triphala is a classical Ayurvedic formulation made from three fruits: Amalaki (Amla), Haritaki, and Bibhitaki.",
            json.dumps(["digestive support", "mild laxative", "rasayana"], ensure_ascii=False),
            "Ayurveda",
        ),
    )
    new_id = db.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    return int(new_id)


def _ensure_preparation(
    *,
    plant_id: int,
    name_en: str,
    name_hi: str,
    name_mr: str,
    form_type: str,
    category: str,
    preparation_steps: list[str],
    dosage_json: dict,
    timing: str,
    anupana: str,
    notes_en: str,
    notes_hi: str,
    notes_mr: str,
) -> int:
    db = get_db()

    row = db.execute(
        """
        SELECT id FROM preparations
        WHERE plant_id=? AND LOWER(name_en)=LOWER(?)
        LIMIT 1
        """,
        (plant_id, name_en),
    ).fetchone()
    if row:
        return _rowid_int(row)

    db.execute(
        """
        INSERT INTO preparations(
          plant_id,
          name_en, name_hi, name_mr,
          classical_name,
          ayush_system,
          form_type, category,
          preparation_steps,
          equipment_needed,
          dosage_json,
          timing, anupana,
          notes
        ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,
        (
            plant_id,
            name_en,
            name_hi,
            name_mr,
            None,
            "Ayurveda",
            form_type,
            category,
            json.dumps(preparation_steps, ensure_ascii=False),
            None,
            json.dumps(dosage_json, ensure_ascii=False),
            timing,
            anupana,
            notes_en,
        ),
    )
    prep_id = db.execute("SELECT last_insert_rowid() AS id").fetchone()["id"]
    prep_id = int(prep_id)

    # i18n: English verified + minimal hi/mr (manual)
    upsert_i18n("preparation", prep_id, "en", "name", name_en, status="verified", source="manual")
    upsert_i18n(
        "preparation",
        prep_id,
        "en",
        "preparation_steps",
        json.dumps(preparation_steps, ensure_ascii=False),
        status="verified",
        source="manual",
    )
    upsert_i18n(
        "preparation",
        prep_id,
        "en",
        "dosage_json",
        json.dumps(dosage_json, ensure_ascii=False),
        status="verified",
        source="manual",
    )
    upsert_i18n("preparation", prep_id, "en", "timing", timing or "", status="verified", source="manual")
    upsert_i18n("preparation", prep_id, "en", "anupana", anupana or "", status="verified", source="manual")
    upsert_i18n("preparation", prep_id, "en", "notes", notes_en or "", status="verified", source="manual")

    upsert_i18n("preparation", prep_id, "hi", "name", name_hi, status="verified", source="manual")
    upsert_i18n(
        "preparation",
        prep_id,
        "hi",
        "preparation_steps",
        json.dumps(preparation_steps, ensure_ascii=False),
        status="verified",
        source="manual",
    )
    upsert_i18n(
        "preparation",
        prep_id,
        "hi",
        "dosage_json",
        json.dumps(dosage_json, ensure_ascii=False),
        status="verified",
        source="manual",
    )
    upsert_i18n("preparation", prep_id, "hi", "timing", timing or "", status="verified", source="manual")
    upsert_i18n("preparation", prep_id, "hi", "anupana", anupana or "", status="verified", source="manual")
    upsert_i18n("preparation", prep_id, "hi", "notes", notes_hi or "", status="verified", source="manual")

    upsert_i18n("preparation", prep_id, "mr", "name", name_mr, status="verified", source="manual")
    upsert_i18n(
        "preparation",
        prep_id,
        "mr",
        "preparation_steps",
        json.dumps(preparation_steps, ensure_ascii=False),
        status="verified",
        source="manual",
    )
    upsert_i18n(
        "preparation",
        prep_id,
        "mr",
        "dosage_json",
        json.dumps(dosage_json, ensure_ascii=False),
        status="verified",
        source="manual",
    )
    upsert_i18n("preparation", prep_id, "mr", "timing", timing or "", status="verified", source="manual")
    upsert_i18n("preparation", prep_id, "mr", "anupana", anupana or "", status="verified", source="manual")
    upsert_i18n("preparation", prep_id, "mr", "notes", notes_mr or "", status="verified", source="manual")

    return prep_id


def _ensure_triphala_churna(triphala_plant_id: int) -> int:
    prep_id = _ensure_preparation(
        plant_id=triphala_plant_id,
        name_en="Triphala Churna",
        name_hi="त्रिफला चूर्ण",
        name_mr="त्रिफळा चूर्ण",
        form_type="powder",
        category="digestive",
        preparation_steps=[
            "Mix equal parts of Amla (Amalaki), Haritaki, and Bibhitaki powders.",
            "Store in an airtight container away from moisture.",
        ],
        dosage_json={
            "adult": "Typically 1/2 to 1 teaspoon with warm water at bedtime; start low.",
            "child": "Only under qualified guidance.",
        },
        timing="after_food_or_bedtime",
        anupana="warm_water",
        notes_en=(
            "General traditional guidance only. Avoid excessive use. If pregnant, breastfeeding, or on medicines, consult a qualified practitioner."
        ),
        notes_hi=(
            "यह केवल पारंपरिक सामान्य जानकारी है। अधिक मात्रा से बचें। गर्भावस्था/स्तनपान या दवाइयाँ चल रही हों तो योग्य चिकित्सक से सलाह लें।"
        ),
        notes_mr=(
            "ही केवळ पारंपरिक सामान्य माहिती आहे. अति वापर टाळा. गर्भधारणा/स्तनपान किंवा औषधे सुरू असल्यास पात्र तज्ञांचा सल्ला घ्या."
        ),
    )

    # Best-effort ingredient links (only if plants exist)
    db = get_db()
    for common_name in ("Amla", "Haritaki", "Bibhitaki"):
        pid = _find_plant_id_by_common_name_en(common_name)
        if not pid:
            continue
        exists = db.execute(
            """
            SELECT 1 FROM preparation_ingredients
            WHERE preparation_id=? AND plant_id=?
            LIMIT 1
            """,
            (prep_id, pid),
        ).fetchone()
        if exists:
            continue
        db.execute(
            """
            INSERT INTO preparation_ingredients(preparation_id, plant_id, part, quantity_value, quantity_unit, notes)
            VALUES(?,?,?,?,?,?)
            """,
            (prep_id, pid, "fruit", None, None, None),
        )

    return prep_id


def _ensure_neem_oil_prep() -> Optional[int]:
    neem_id = _find_plant_id_by_common_name_en("Neem")
    if not neem_id:
        return None

    return _ensure_preparation(
        plant_id=neem_id,
        name_en="Neem Oil (Topical Use)",
        name_hi="नीम तेल (बाहरी उपयोग)",
        name_mr="नीम तेल (बाह्य उपयोग)",
        form_type="oil",
        category="skin",
        preparation_steps=[
            "Use commercially prepared Neem oil from a reliable source.",
            "For sensitive skin, dilute a few drops in a carrier oil (e.g., coconut or sesame) before applying.",
            "Do a patch test first and discontinue if irritation occurs.",
        ],
        dosage_json={
            "adult": "External use only. Apply a thin layer once daily initially; adjust based on tolerance.",
            "child": "External use only and only with guidance.",
        },
        timing="external_or_as_directed",
        anupana="plain",
        notes_en=(
            "External use guidance only. Avoid eyes and broken skin. Do not ingest unless prescribed. Consult a qualified practitioner for chronic or severe skin problems."
        ),
        notes_hi=(
            "यह केवल बाहरी उपयोग हेतु सामान्य जानकारी है। आँखों/घाव वाली त्वचा से बचें। बिना चिकित्सकीय सलाह के सेवन न करें। गंभीर/पुरानी समस्या में योग्य चिकित्सक से सलाह लें।"
        ),
        notes_mr=(
            "हे फक्त बाह्य वापरासाठी सामान्य मार्गदर्शन आहे. डोळे/जखमी त्वचा टाळा. वैद्यकीय सल्ल्याशिवाय सेवन करू नका. गंभीर/दीर्घ त्वचा तक्रारींसाठी पात्र तज्ञांचा सल्ला घ्या."
        ),
    )


def main() -> None:
    app = create_app()
    with app.app_context():
        db = get_db()

        # Triphala pseudo-plant + i18n
        triphala_id = _ensure_triphala_plant()
        upsert_i18n("plant", triphala_id, "en", "name", "Triphala", status="verified", source="manual")
        upsert_i18n(
            "plant",
            triphala_id,
            "en",
            "description",
            "Triphala is a classical Ayurvedic formulation made from three fruits: Amalaki (Amla), Haritaki, and Bibhitaki.",
            status="verified",
            source="manual",
        )
        upsert_i18n("plant", triphala_id, "hi", "name", "त्रिफला", status="verified", source="manual")
        upsert_i18n(
            "plant",
            triphala_id,
            "hi",
            "description",
            "त्रिफला आयुर्वेद का एक प्रसिद्ध योग है जो तीन फलों—आँवला (आमलकी), हरितकी और बिभीतकी—से बनता है।",
            status="verified",
            source="manual",
        )
        upsert_i18n("plant", triphala_id, "mr", "name", "त्रिफळा", status="verified", source="manual")
        upsert_i18n(
            "plant",
            triphala_id,
            "mr",
            "description",
            "त्रिफळा हा आयुर्वेदातील प्रसिद्ध योग आहे जो तीन फळे—आवळा (आमलकी), हरितकी आणि बिभीतकी—यांपासून बनतो.",
            status="verified",
            source="manual",
        )

        triphala_churna_id = _ensure_triphala_churna(triphala_id)
        neem_oil_id = _ensure_neem_oil_prep()

        # Rebuild indexes for affected entities
        for ent_type, ent_id in (
            ("plant", triphala_id),
            ("preparation", triphala_churna_id),
            ("preparation", neem_oil_id) if neem_oil_id else (None, None),
        ):
            if not ent_type or not ent_id:
                continue
            rebuild_fts_for_entity(ent_type, int(ent_id))
            rebuild_vec_for_entity(ent_type, int(ent_id))

        db.commit()

        print("[seed] OK")
        print(f"[seed] Triphala plant_id={triphala_id}")
        print(f"[seed] Triphala Churna prep_id={triphala_churna_id}")
        if neem_oil_id:
            print(f"[seed] Neem Oil prep_id={neem_oil_id}")
        else:
            print("[seed] Neem plant not found; skipped Neem Oil prep")


if __name__ == "__main__":
    main()
