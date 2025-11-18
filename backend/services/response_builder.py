"""
Utility functions to turn structured plant/disease data into natural
language responses without relying on an external LLM.
"""

from __future__ import annotations

import re
from typing import Dict, List, Sequence


def _join(items: Sequence[str]) -> str:
    cleaned = [item.strip() for item in items if item]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return " and ".join(cleaned)
    return ", ".join(cleaned[:-1]) + f", and {cleaned[-1]}"

def _format_list(items: Sequence[str]) -> str:
    """
    Format list-like data safely. If a plain string is passed, avoid
    iterating over characters by treating it as a single item (and
    splitting on common delimiters when present).
    """
    if not items:
        return ""

    # Accept a single string without breaking it into characters
    if isinstance(items, str):
        tokens = [t.strip() for t in re.split(r"[;,\n]+", items) if t.strip()]
        cleaned = tokens or [items.strip()]
        return "; ".join(cleaned)

    cleaned: List[str] = []
    for item in items:
        if not item:
            continue
        if isinstance(item, str):
            tokens = [t.strip() for t in re.split(r"[;,\n]+", item) if t.strip()]
            cleaned.extend(tokens or [item.strip()])
        else:
            cleaned.append(str(item).strip())

    if not cleaned:
        return ""
    return "; ".join(cleaned)


def build_plant_answer(plant: Dict) -> str:
    name = plant.get("common_name_en") or plant.get("common_name") or "This plant"
    botanical = plant.get("botanical_name") or ""
    header = f"{name} ({botanical})" if botanical else name

    parts = [header]

    if plant.get("description"):
        parts.append(plant["description"])

    if plant.get("parts_used"):
        parts.append(f"Parts used: {_format_list(plant['parts_used'])}.")

    if plant.get("therapeutic_actions"):
        parts.append(
            f"Key actions: {_format_list(plant['therapeutic_actions'])}."
        )

    rasa = _format_list(plant.get("rasa") or [])
    guna = _format_list(plant.get("guna") or [])
    virya = plant.get("virya")
    vipaka = plant.get("vipaka")
    dosha = _format_list(plant.get("dosha_effect") or [])

    energetics = []
    if rasa:
        energetics.append(f"Rasa (taste): {rasa}")
    if guna:
        energetics.append(f"Guna (qualities): {guna}")
    if virya:
        energetics.append(f"Virya (potency): {virya}")
    if vipaka:
        energetics.append(f"Vipaka (post-digestive effect): {vipaka}")
    if dosha:
        energetics.append(f"Dosha impact: {dosha}")
    if energetics:
        parts.append("Constitutional profile: " + "; ".join(energetics) + ".")

    parts.append(
        "Always consult a qualified practitioner before starting or changing any herbal regimen."
    )

    return "\n\n".join(parts)


def build_remedy_answer(
    disease: Dict,
    plants: Sequence[Dict],
    preparations: Sequence[Dict],
) -> str:
    name = disease.get("name_en") or "This condition"
    parts = [f"{name} overview:"]

    if disease.get("description"):
        parts.append(disease["description"])

    if disease.get("symptoms"):
        parts.append(
            f"Typical symptoms: {_format_list(disease['symptoms'])}."
        )
    if disease.get("causes"):
        parts.append(f"Root causes noted in Ayurveda: {_format_list(disease['causes'])}.")

    if plants:
        lines = []
        for plant in plants[:5]:
            pname = plant.get("common_name_en") or plant.get("common_name")
            bname = plant.get("botanical_name") or ""
            actions = _format_list(
                plant.get("therapeutic_actions") or plant.get("actions") or []
            )
            line = f"- {pname}"
            if bname:
                line += f" ({bname})"
            if actions:
                line += f": {actions}"
            lines.append(line)
        parts.append("Helpful herbs:\n" + "\n".join(lines))

    if preparations:
        lines = []
        for prep in preparations[:3]:
            pname = prep.get("name_en") or prep.get("name")
            form = prep.get("form_type") or prep.get("category")
            steps = prep.get("preparation_steps")
            if isinstance(steps, list):
                steps = "; ".join(steps[:2])
            line = f"- {pname}"
            if form:
                line += f" ({form})"
            if steps:
                line += f": {steps}"
            lines.append(line)
        parts.append("Common preparations:\n" + "\n".join(lines))

    if disease.get("prevention_tips"):
        parts.append(
            f"Prevention & lifestyle tips: {_format_list(disease['prevention_tips'])}."
        )

    parts.append(
        "Please use these insights as general guidance and work with a qualified Ayurvedic practitioner for personalized care."
    )

    return "\n\n".join(parts)


def build_generic_answer(plants: Sequence[Dict], diseases: Sequence[Dict]) -> str:
    parts = []
    if plants:
        plant_names = _join(
            [p.get("common_name_en") or p.get("common_name") for p in plants]
        )
        parts.append(f"I found references to {plant_names}.")

    if diseases:
        disease_names = _join([d.get("name_en") for d in diseases if d.get("name_en")])
        if disease_names:
            parts.append(f"The query also relates to {disease_names}.")

    parts.append(
        "Let me know if you want details about a specific plant, condition, or preparation."
    )
    return " ".join(parts)


def build_no_data_answer(user_text: str) -> str:
    return (
        "I couldn't link this query to any plant or condition in the knowledge base. "
        "Please try mentioning a plant name, disease, or preparation so I can help."
    )
