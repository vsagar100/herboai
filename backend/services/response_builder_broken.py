"""
Utility functions to turn structured plant/disease data into natural
language responses without relying on an external LLM.

Supports multilingual response building (en/hi/mr) by accepting language parameter
and fetching localized content from entity_i18n when available.
"""

from __future__ import annotations

import re
import json
from typing import Dict, List, Sequence
from utils.i18n import get_localized_field, normalize_lang

# Labels & text snippets for different languages
LABELS = {
    "en": {
        "overview": "overview",
        "parts_used": "Parts used",
        "key_actions": "Key actions",
        "rasa": "Rasa (taste)",
        "guna": "Guna (qualities)",
        "virya": "Virya (potency)",
        "vipaka": "Vipaka (post-digestive effect)",
        "dosha": "Dosha impact",
        "constitutional": "Constitutional profile",
        "disclaimer_plant": "Always consult a qualified practitioner before starting or changing any herbal regimen.",
        "typical_symptoms": "Typical symptoms",
        "root_causes": "Root causes noted in Ayurveda",
        "helpful_herbs": "Helpful herbs",
        "preparations": "Common preparations",
        "prevention": "Prevention & lifestyle tips",
        "steps": "How to prepare",
        "dosage": "Typical dosage",
        "timing": "Timing",
        "anupana": "Anupana",
        "medical_disclaimer": "⚠️ This information is for educational purposes only. Always confirm dosage and suitability with a qualified Ayurvedic practitioner.",
    },
    "hi": {
        "overview": "सारांश",
        "parts_used": "उपयोग के भाग",
        "key_actions": "मुख्य कार्य",
        "rasa": "रस (स्वाद)",
        "guna": "गुण (गुणवत्ता)",
        "virya": "वीर्य (शक्ति)",
        "vipaka": "विपाक (पाचन के बाद प्रभाव)",
        "dosha": "दोष प्रभाव",
        "constitutional": "संवैधानिक प्रोफ़ाइल",
        "disclaimer_plant": "कोई भी हर्बल आहार शुरू करने या बदलने से पहले हमेशा एक योग्य चिकित्सक से परामर्श लें।",
        "typical_symptoms": "विशिष्ट लक्षण",
        "root_causes": "आयुर्वेद में नोट किए गए मूल कारण",
        "helpful_herbs": "सहायक जड़ी बूटियां",
        "preparations": "सामान्य तैयारियां",
        "prevention": "रोकथाम और जीवनशैली सुझाव",
        "steps": "तैयार करने के लिए कैसे",
        "dosage": "विशिष्ट खुराक",
        "timing": "समय",
        "anupana": "अनुपान",
        "medical_disclaimer": "⚠️ यह जानकारी केवल शैक्षणिक उद्देश्यों के लिए है। हमेशा योग्य आयुर्वेदिक चिकित्सक के साथ खुराक और उपयुक्तता की पुष्टि करें।",
    },
    "mr": {
        "overview": "विहंगावलोकन",
        "parts_used": "वापरण्यास भाग",
        "key_actions": "मुख्य कार्ये",
        "rasa": "रस (स्वाद)",
        "guna": "गुण (गुणवत्ता)",
        "virya": "वीर्य (शक्ती)",
        "vipaka": "विपाक (पचन नंतर प्रभाव)",
        "dosha": "दोष प्रभाव",
        "constitutional": "संवैधानिक प्रोफाईल",
        "disclaimer_plant": "कोणतीही हर्बल औषध सुरू करण्यापूर्वी किंवा बदलण्यापूर्वी नेहमी पात्र वैद्यकीय व्यावसायिकांशी सल्ला घ्या।",
        "typical_symptoms": "विशिष्ट लक्षणे",
        "root_causes": "आयुर्वेदात नोंदविलेल्या मूळ कारणे",
        "helpful_herbs": "मदतीस औषधी वनस्पती",
        "preparations": "सामान्य तयारी",
        "prevention": "प्रतिबंध आणि जीवनशैली सुचना",
        "steps": "कसे तयार करायचे",
        "dosage": "विशिष्ट औषधप्रमाण",
        "timing": "वेळ",
        "anupana": "अनुपान",
        "medical_disclaimer": "⚠️ ही माहिती केवळ शैक्षणिक उद्देश्यांसाठी आहे। हमेशा योग्य आयुर्वेदिक व्यावसायिकांशी औषधप्रमाण आणि उपयुक्तता पुष्टी करा।",
    },
}


def _get_label(key: str, lang: str = "en") -> str:
    """Get localized label for a key."""
    lang = normalize_lang(lang)
    return LABELS.get(lang, LABELS["en"]).get(key, key)


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


def build_plant_answer(plant: Dict, lang: str = "en") -> str:
    """
    Build plant profile response in target language.
    
    Args:
        plant: Plant data dict (should include id for entity_i18n lookup)
        lang: Target language ('en', 'hi', 'mr')
    
    Returns:
        Formatted plant profile response in target language
    """
    lang = normalize_lang(lang)
    
    # Get localized name and description
    plant_id = plant.get("id")
    if plant_id:
        name = get_localized_field("plant", plant_id, "name", lang) or plant.get("common_name_en", "This plant")
        description = get_localized_field("plant", plant_id, "description", lang) or plant.get("description", "")
        therapeutic_actions_text = get_localized_field("plant", plant_id, "therapeutic_actions", lang) or plant.get("therapeutic_actions", "")
        parts_used_text = get_localized_field("plant", plant_id, "parts_used", lang) or plant.get("parts_used", "")
    else:
        name = plant.get("common_name_en") or plant.get("common_name") or "This plant"
        description = plant.get("description", "")
        therapeutic_actions_text = plant.get("therapeutic_actions", "")
        parts_used_text = plant.get("parts_used", "")
    
    botanical = plant.get("botanical_name") or ""
    header = f"{name} ({botanical})" if botanical else name

    parts = [f"## {header}"]

    if description:
        parts.append(description)

    if parts_used_text:
        parts.append(f"**{_get_label('parts_used', lang)}:** {_format_list(parts_used_text)}")

    if therapeutic_actions_text:
        parts.append(f"**{_get_label('key_actions', lang)}:** {_format_list(therapeutic_actions_text)}")

    rasa = _format_list(plant.get("rasa") or [])
    guna = _format_list(plant.get("guna") or [])
    virya = plant.get("virya")
    vipaka = plant.get("vipaka")
    dosha = _format_list(plant.get("dosha_effect") or [])

    energetics = []
    if rasa:
        energetics.append(f"{_get_label('rasa', lang)}: {rasa}")
    if guna:
        energetics.append(f"{_get_label('guna', lang)}: {guna}")
    if virya:
        energetics.append(f"{_get_label('virya', lang)}: {virya}")
    if vipaka:
        energetics.append(f"{_get_label('vipaka', lang)}: {vipaka}")
    if dosha:
        energetics.append(f"{_get_label('dosha', lang)}: {dosha}")
    if energetics:
        parts.append(f"**{_get_label('constitutional', lang)}:** {'; '.join(energetics)}")

    parts.append(f"⚠️ {_get_label('disclaimer_plant', lang)}")

    return "\n\n".join(parts)


def build_remedy_answer(
    disease: Dict,
    plants: Sequence[Dict],
    preparations: Sequence[Dict],
    lang: str = "en",
) -> str:
    """
    Build disease remedy response in target language.
    
    Args:
        disease: Disease data dict (should include id for entity_i18n lookup)
        plants: List of plant dicts
        preparations: List of preparation dicts
        lang: Target language ('en', 'hi', 'mr')
    
    Returns:
        Formatted remedy response in target language
    """
    lang = normalize_lang(lang)
    
    # Get localized disease name and description
    disease_id = disease.get("id")
    if disease_id:
        name = get_localized_field("disease", disease_id, "name", lang) or disease.get("name_en", "This condition")
        description = get_localized_field("disease", disease_id, "description", lang) or disease.get("description", "")
        symptoms_text = get_localized_field("disease", disease_id, "symptoms", lang) or disease.get("symptoms", "")
        causes_text = get_localized_field("disease", disease_id, "causes", lang) or disease.get("causes", "")
        prevention_text = get_localized_field("disease", disease_id, "prevention_tips", lang) or disease.get("prevention_tips", "")
    else:
        name = disease.get("name_en") or "This condition"
        description = disease.get("description", "")
        symptoms_text = disease.get("symptoms", "")
        causes_text = disease.get("causes", "")
        prevention_text = disease.get("prevention_tips", "")
    
    parts = [f"## {name} {_get_label('overview', lang)}"]

    if description:
        parts.append(description)

    if symptoms_text:
        parts.append(f"**{_get_label('typical_symptoms', lang)}:** {_format_list(symptoms_text)}")
    
    if causes_text:
        parts.append(f"**{_get_label('root_causes', lang)}:** {_format_list(causes_text)}")

    if plants:
        lines = []
        for plant in plants[:5]:
            plant_id = plant.get("id")
            if plant_id:
                pname = get_localized_field("plant", plant_id, "name", lang) or plant.get("common_name_en", "")
                actions_text = get_localized_field("plant", plant_id, "therapeutic_actions", lang) or plant.get("therapeutic_actions", "")
            else:
                pname = plant.get("common_name_en") or plant.get("common_name", "")
                actions_text = plant.get("therapeutic_actions", "")
            
            bname = plant.get("botanical_name") or ""
            actions = _format_list(actions_text)
            
            line = f"- **{pname}**"
            if bname:
                line += f" _{bname}_"
            if actions:
                line += f": {actions}"
            lines.append(line)
        
        if lines:
            parts.append(f"**{_get_label('helpful_herbs', lang)}:**\n" + "\n".join(lines))

    if preparations:
        lines = []
        for prep in preparations[:3]:
            prep_id = prep.get("id")
            if prep_id:
                pname = get_localized_field("preparation", prep_id, "name", lang) or prep.get("name_en", "")
                steps_text = get_localized_field("preparation", prep_id, "preparation_steps", lang) or prep.get("preparation_steps", "")
            else:
                pname = prep.get("name_en") or prep.get("name", "")
                steps_text = prep.get("preparation_steps", "")
            
            form = prep.get("form_type") or prep.get("category", "")
            
            line = f"- **{pname}**"
            if form:
                line += f" ({form})"
            
            # Parse steps if JSON
            if isinstance(steps_text, str):
                try:
                    steps_parsed = json.loads(steps_text)
                    if isinstance(steps_parsed, list):
                        steps_text = "; ".join(steps_parsed[:2])
                except Exception:
                    pass
            
            if steps_text:
                step_summary = str(steps_text)[:100] + ("..." if len(str(steps_text)) > 100 else "")
                line += f": {step_summary}"
            
            lines.append(line)
        
        if lines:
            parts.append(f"**{_get_label('preparations', lang)}:**\n" + "\n".join(lines))

    if prevention_text:
        parts.append(f"**{_get_label('prevention', lang)}:** {_format_list(prevention_text)}")
    
    parts.append(_get_label('medical_disclaimer', lang))

    return "\n\n".join(parts)


def build_generic_answer(plants: Sequence[Dict], diseases: Sequence[Dict], lang: str = "en") -> str:
    """Build generic response for mixed plant/disease mentions."""
    lang = normalize_lang(lang)
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

    if lang == "en":
        parts.append("Let me know if you want details about a specific plant, condition, or preparation.")
    elif lang == "hi":
        parts.append("कृपया एक विशिष्ट पौधे, स्थिति या तैयारी के बारे में जानकारी चाहते हैं तो बताएं।")
    elif lang == "mr":
        parts.append("कृपया एक विशिष्ट वनस्पती, स्थिती किंवा तयारीबद्दल माहिती हवेत तर सांगा।")
    
    return " ".join(parts)


def build_no_data_answer(user_text: str, lang: str = "en") -> str:
    """Build response when no data found."""
    lang = normalize_lang(lang)
    
    if lang == "en":
        return "I couldn't link this query to any plant or condition in the knowledge base. Please try mentioning a plant name, disease, or preparation so I can help."
    elif lang == "hi":
        return "मुझे इस प्रश्न को ज्ञान आधार में किसी भी पौधे या स्थिति से जोड़ नहीं सका। कृपया एक पौधे का नाम, बीमारी या तैयारी का उल्लेख करके मुझे मदद करने दें।"
    elif lang == "mr":
        return "मला या प्रश्नाला ज्ञान आधारामधील कोणत्याही वनस्पती किंवा स्थितीशी जोडू शकलो नाही। कृपया एक वनस्पती, रोग किंवा तयारीचा उल्लेख करून मला मदत करण्याची परवानगी द्या।"
    
    return "Could not find data for this query."

def build_plant_knowledge_snippet(plant: Dict) -> str:
    """
    Compact, embedding-friendly plant description that matches the tone
    of build_plant_answer but without disclaimers or chat framing.

    Used for:
    - plant_embeddings ETL
    - RAG context building
    """
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
        parts.append("; ".join(energetics) + ".")

    # No disclaimer here – this is pure knowledge text for embeddings / context.
    return " ".join(p.strip() for p in parts if p and str(p).strip())

def build_disease_knowledge_snippet(disease: Dict) -> str:
    """
    Compact, embedding-friendly disease description that aligns with
    build_remedy_answer's tone but focused only on the condition itself.
    """
    name = disease.get("name_en") or "This condition"
    parts = [f"{name}:"]

    if disease.get("ayurvedic_name"):
        parts.append(f"Ayurvedic name: {disease['ayurvedic_name']}.")

    if disease.get("description"):
        parts.append(disease["description"])

    if disease.get("symptoms"):
        parts.append(
            f"Typical symptoms: {_format_list(disease['symptoms'])}."
        )
    if disease.get("causes"):
        parts.append(
            f"Root causes and risk factors: {_format_list(disease['causes'])}."
        )

    dosha = _format_list(disease.get("dosha_involvement") or [])
    dhatu = _format_list(disease.get("dhatu_involvement") or [])
    severity = disease.get("severity_level")

    if dosha:
        parts.append(f"Dosha involvement: {dosha}.")
    if dhatu:
        parts.append(f"Dhatu involvement: {dhatu}.")
    if severity:
        parts.append(f"Severity level: {severity}.")

    if disease.get("prevention_tips"):
        parts.append(
            f"Prevention and lifestyle tips: {_format_list(disease['prevention_tips'])}."
        )
    if disease.get("dietary_recommendations"):
        parts.append(
            f"Dietary recommendations: {_format_list(disease['dietary_recommendations'])}."
        )

    # Again, no generic disclaimer – context only.
    return " ".join(p.strip() for p in parts if p and str(p).strip())

def _fmt_steps(steps) -> str:
    if not steps:
        return ""
    if isinstance(steps, list):
        items = [s.strip() for s in steps if isinstance(s, str) and s.strip()]
        return "\n".join([f"  {i+1}) {t}" for i, t in enumerate(items[:10])])
    if isinstance(steps, str):
        s = steps.strip()
        return s
    return ""


def _fmt_dosage(dosage) -> str:
    if not dosage:
        return ""
    if isinstance(dosage, dict):
        out = []
        adult = dosage.get("adult")
        child = dosage.get("child")
        general = dosage.get("general")
        if adult:
            out.append(f"  - Adult: {adult}")
        if child:
            out.append(f"  - Child: {child}")
        if general and not (adult or child):
            out.append(f"  - {general}")
        # show a couple more keys if present
        extra_keys = [k for k in dosage.keys() if k not in ("adult", "child", "general")]
        for k in extra_keys[:2]:
            out.append(f"  - {k}: {dosage.get(k)}")
        return "\n".join(out)
    # if it’s a string (already formatted)
    if isinstance(dosage, str):
        return dosage.strip()
    return ""


def _prep_card(p: dict) -> str:
    name = p.get("name_en") or p.get("name") or p.get("classical_name") or "Herbal preparation"
    form = p.get("form_type") or p.get("category") or ""
    timing = (p.get("timing") or "").strip()
    anupana = (p.get("anupana") or "").strip()
    notes = (p.get("notes") or "").strip()

    steps = _fmt_steps(p.get("preparation_steps"))
    dosage = _fmt_dosage(p.get("dosage_json"))

    lines = []
    lines.append(f"**{name}**" + (f" ({form})" if form else ""))

    if steps:
        lines.append("**How to prepare:**")
        lines.append(steps)

    if dosage:
        lines.append("**Dosage (general guidance):**")
        lines.append(dosage)

    if timing:
        lines.append(f"**Timing:** {timing}")
    if anupana:
        lines.append(f"**Anupana:** {anupana}")
    if notes:
        lines.append(f"**Notes/Caution:** {notes}")

    return "\n".join(lines)


def build_hybrid_response(severity: str, followups: list[str], provisional: list[dict]) -> str:
    """
    Used while collecting followups.
    MUST still give useful prep/remedy output.
    """
    lines = []
    lines.append(f"🔍 **Assessment:** {severity.capitalize()} severity\n")

    if provisional:
        lines.append("🌿 **Suggested preparations (from HerboAI DB):**")
        for idx, p in enumerate(provisional[:3], 1):
            lines.append(f"\n{idx}) " + _prep_card(p))
        lines.append("")

    if followups:
        lines.append("❓ **A few quick questions (to personalize, optional but helpful):**")
        for i, q in enumerate(followups, 1):
            lines.append(f"{i}. {q}")
        lines.append("")

    lines.append("⚠️ If symptoms worsen/persist or you have serious symptoms, consult a qualified doctor or AYUSH practitioner.")
    return "\n".join(lines)


def build_final_response(severity: str, provisional: list[dict], optional_questions: list[str], condition: str, slots: dict) -> str:
    """
    Final answer after required slots are present.
    """
    lines = []
    lines.append(f"🔍 **Assessment:** {severity.capitalize()} severity\n")

    if condition == "diabetes":
        lines.append("🩺 **Diabetes support (AYUSH-friendly, non-emergency):**")
        lines.append("- Diet: reduce refined carbs/sugar; prefer fiber-rich meals.")
        lines.append("- Activity: daily walk + consistent sleep.")
        lines.append("- Don’t stop prescribed medicines without doctor advice.\n")

    if provisional:
        lines.append("🌿 **Preparations (from HerboAI DB):**")
        for idx, p in enumerate(provisional[:5], 1):
            lines.append(f"\n{idx}) " + _prep_card(p))
        lines.append("")
    else:
        lines.append("🌿 I couldn’t find a mapped preparation in the current DB for this query.\n")

    if optional_questions:
        lines.append("✅ **Optional (for better personalization):**")
        for i, q in enumerate(optional_questions, 1):
            lines.append(f"{i}. {q}")
        lines.append("")

    lines.append("⚠️ If symptoms worsen/persist or you have serious symptoms, consult a qualified doctor or AYUSH practitioner.")
    return "\n".join(lines)
