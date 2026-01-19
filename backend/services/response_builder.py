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


def _fmt_steps(steps) -> str:
    """Format preparation steps."""
    if not steps:
        return ""
    if isinstance(steps, list):
        items = [s.strip() for s in steps if isinstance(s, str) and s.strip()]
        return "\n".join([f"  {i+1}) {t}" for i, t in enumerate(items[:10])])
    if isinstance(steps, str):
        s = steps.strip()
        return s
    return ""


def _try_parse_json_text(value):
    """Best-effort JSON parser for values that may be JSON-encoded strings."""
    if value is None:
        return None
    if isinstance(value, (dict, list)):
        return value
    if not isinstance(value, str):
        return value
    s = value.strip()
    if not s:
        return value
    if not (s.startswith("{") or s.startswith("[")):
        return value
    try:
        return json.loads(s)
    except Exception:
        return value


def _fmt_dosage(dosage, lang: str = "en") -> str:
    """Format dosage information."""
    lang = normalize_lang(lang)
    if not dosage:
        return ""
    if isinstance(dosage, dict):
        labels = {
            "en": {"adult": "Adult", "child": "Child"},
            "hi": {"adult": "वयस्क", "child": "बच्चे"},
            "mr": {"adult": "प्रौढ", "child": "मुलं"},
        }
        lc = labels.get(lang, labels["en"])
        out = []
        adult = dosage.get("adult")
        child = dosage.get("child")
        general = dosage.get("general")
        if adult:
            out.append(f"  - {lc['adult']}: {adult}")
        if child:
            out.append(f"  - {lc['child']}: {child}")
        if general and not (adult or child):
            out.append(f"  - {general}")
        # show a couple more keys if present
        extra_keys = [k for k in dosage.keys() if k not in ("adult", "child", "general")]
        for k in extra_keys[:2]:
            out.append(f"  - {k}: {dosage.get(k)}")
        return "\n".join(out)
    # if it's a string (already formatted)
    if isinstance(dosage, str):
        return dosage.strip()
    return ""


def _prep_card(p: dict, lang: str = "en") -> str:
    """Format a preparation card in target language."""
    lang = normalize_lang(lang)
    
    prep_id = p.get("id")
    if prep_id:
        name = get_localized_field("preparation", prep_id, "name", lang) or p.get("name_en") or p.get("name") or p.get("classical_name") or "Herbal preparation"
        # Also try to get localized steps, dosage, notes if available
        steps_localized = get_localized_field("preparation", prep_id, "preparation_steps", lang)
        dosage_localized = get_localized_field("preparation", prep_id, "dosage_json", lang)
        notes_localized = get_localized_field("preparation", prep_id, "notes", lang)
    else:
        name = p.get("name_en") or p.get("name") or p.get("classical_name") or "Herbal preparation"
        steps_localized = ""
        dosage_localized = ""
        notes_localized = ""
    
    form = p.get("form_type") or p.get("category") or ""
    timing = (p.get("timing") or "").strip()
    anupana = (p.get("anupana") or "").strip()
    notes = (p.get("notes") or "").strip()

    # Use localized versions if available, otherwise use database versions
    steps = _fmt_steps(steps_localized or p.get("preparation_steps"))
    dosage_val = dosage_localized if dosage_localized else p.get("dosage_json")
    dosage_val = _try_parse_json_text(dosage_val)
    dosage = _fmt_dosage(dosage_val, lang=lang)
    notes = notes_localized or notes

    lines = []
    lines.append(f"**{name}**" + (f" ({form})" if form else ""))

    if steps:
        lines.append(f"**{_get_label('steps', lang)}:**")
        lines.append(steps)

    if dosage:
        lines.append(f"**{_get_label('dosage', lang)}:**")
        lines.append(dosage)

    if timing:
        lines.append(f"**{_get_label('timing', lang)}:** {timing}")
    if anupana:
        lines.append(f"**{_get_label('anupana', lang)}:** {anupana}")
    if notes:
        notes_label = "Notes/Caution" if lang == "en" else ("नोट्स/सावधानी" if lang == "hi" else "टीप/सावधगिरी")
        lines.append(f"**{notes_label}:** {notes}")

    return "\n".join(lines)


def build_hybrid_response(severity: str, followups: list[str], provisional: list[dict], lang: str = "en") -> str:
    """
    Used while collecting followups.
    MUST still give useful prep/remedy output.
    """
    lang = normalize_lang(lang)
    lines = []
    
    severity_label = severity.capitalize() if lang == "en" else (
        severity.capitalize() if lang == "hi" else severity.capitalize()
    )
    lines.append(f"🔍 **Assessment:** {severity_label} severity\n")

    if provisional:
        prep_label = _get_label('preparations', lang)
        lines.append(f"🌿 **{prep_label} (from HerboAI DB):**")
        for idx, p in enumerate(provisional[:3], 1):
            lines.append(f"\n{idx}) " + _prep_card(p, lang))
        lines.append("")

    if followups:
        q_label = "A few quick questions" if lang == "en" else (
            "कुछ त्वरित प्रश्न" if lang == "hi" else "काही द्रुत प्रश्न"
        )
        lines.append(f"❓ **{q_label} (to personalize, optional but helpful):**")
        for i, q in enumerate(followups, 1):
            lines.append(f"{i}. {q}")
        lines.append("")

    disclaimer = _get_label('medical_disclaimer', lang)
    lines.append(disclaimer)
    return "\n".join(lines)


def build_final_response(
    severity: str, 
    provisional: list[dict], 
    optional_questions: list[str], 
    condition: str, 
    slots: dict,
    lang: str = "en"
) -> str:
    """
    Final answer after required slots are present.
    All content is now fully localized - no hardcoded English mixed in.
    """
    lang = normalize_lang(lang)
    lines = []
    
    severity_label = severity.capitalize() if lang == "en" else (
        severity.capitalize() if lang == "hi" else severity.capitalize()
    )
    lines.append(f"🔍 **Assessment:** {severity_label} severity\n")

    # Build condition-specific advice using localized labels
    # This replaces hardcoded English content with a more flexible system
    condition_advice = _build_condition_advice(condition, lang)
    if condition_advice:
        lines.append(condition_advice)
        lines.append("")

    if provisional:
        prep_label = _get_label('preparations', lang)
        lines.append(f"🌿 **{prep_label} (from HerboAI DB):**")
        for idx, p in enumerate(provisional[:5], 1):
            lines.append(f"\n{idx}) " + _prep_card(p, lang))
        lines.append("")
    else:
        if lang == "en":
            lines.append("🌿 I couldn't find a mapped preparation in the current DB for this query.\n")
        elif lang == "hi":
            lines.append("🌿 मुझे इस प्रश्न के लिए वर्तमान डीबी में कोई मैप की गई तैयारी नहीं मिल सकी।\n")
        elif lang == "mr":
            lines.append("🌿 मला या प्रश्नाकरिता वर्तमान डीबीमध्ये कोणतीही मैप केलेली तयारी सापडली नाही।\n")

    if optional_questions:
        opt_label = "Optional" if lang == "en" else (
            "वैकल्पिक" if lang == "hi" else "वैकल्पिक"
        )
        lines.append(f"✅ **{opt_label} (for better personalization):**")
        for i, q in enumerate(optional_questions, 1):
            lines.append(f"{i}. {q}")
        lines.append("")

    disclaimer = _get_label('medical_disclaimer', lang)
    lines.append(disclaimer)
    return "\n".join(lines)


def _build_condition_advice(condition: str, lang: str = "en") -> str:
    """
    Build condition-specific lifestyle advice in target language.
    Fully localized - no hardcoded English content.
    """
    lang = normalize_lang(lang)
    
    # Mapping of conditions to localized advice
    advice_map = {
        "diabetes": {
            "en": [
                "🩺 **Diabetes support (AYUSH-friendly, non-emergency):**",
                "- Diet: reduce refined carbs/sugar; prefer fiber-rich meals.",
                "- Activity: daily walk + consistent sleep.",
                "- Don't stop prescribed medicines without doctor advice.",
            ],
            "hi": [
                "🩺 **मधुमेह समर्थन (आयुष-अनुकूल, गैर-आपातकालीन):**",
                "- आहार: परिष्कृत कार्बोहाइड्रेट/चीनी में कमी करें; फाइबर युक्त भोजन पसंद करें।",
                "- गतिविधि: दैनिक चलना + सुसंगत नींद।",
                "- डॉक्टर की सलाह के बिना निर्धारित दवाएं बंद न करें।",
            ],
            "mr": [
                "🩺 **मधुमेह समर्थन (आयुष-अनुकूल, गैर-आपातकालीन):**",
                "- आहार: परिष्कृत कार्बोहाइड्रेट/साखर कमी करा; फाइबर समृद्ध खाना पसंद करा।",
                "- क्रिया: दैनिक चालना + सुसंगत झोप।",
                "- डॉक्टराच्या सल्ल्याशिवाय विहित औषध बंद करू नका।",
            ],
        },
        "hypertension": {
            "en": [
                "🩺 **High Blood Pressure support (AYUSH-friendly, non-emergency):**",
                "- Diet: reduce salt intake; increase potassium-rich foods.",
                "- Stress: daily meditation or yoga.",
                "- Continue prescribed medications under doctor's supervision.",
            ],
            "hi": [
                "🩺 **उच्च रक्तचाप समर्थन (आयुष-अनुकूल, गैर-आपातकालीन):**",
                "- आहार: नमक का सेवन कम करें; पोटेशियम युक्त खाद्य पदार्थ बढ़ाएं।",
                "- तनाव: दैनिक ध्यान या योग।",
                "- डॉक्टर की देखरेख में निर्धारित दवाएं जारी रखें।",
            ],
            "mr": [
                "🩺 **उच्च रक्तदाब समर्थन (आयुष-अनुकूल, गैर-आपातकालीन):**",
                "- आहार: मीठ्यांचा सेवन कमी करा; पोटेशियम समृद्ध अन्न वाढवा।",
                "- तणाव: दैनिक ध्यान किंवा योग।",
                "- डॉक्टराच्या देखरेखीखाली विहित औषध चालू ठेवा।",
            ],
        },
        "arthritis": {
            "en": [
                "🩺 **Joint/Arthritis support (AYUSH-friendly, non-emergency):**",
                "- Movement: gentle stretches and low-impact exercise.",
                "- Warmth: warm oil massage (abhyanga) may help.",
                "- Avoid: cold foods and heavy/fried meals.",
            ],
            "hi": [
                "🩺 **जोड़/गठिया समर्थन (आयुष-अनुकूल, गैर-आपातकालीन):**",
                "- आंदोलन: हल्के व्यायाम और कम प्रभाव वाली कसरत।",
                "- गर्माहट: गर्म तेल की मालिश (अभ्यंग) मदद कर सकती है।",
                "- बचें: ठंडे खाद्य और भारी/तले हुए भोजन।",
            ],
            "mr": [
                "🩺 **सांध/गठिया समर्थन (आयुष-अनुकूल, गैर-आपातकालीन):**",
                "- गती: हल्के व्यायाम आणि कमी प्रभाव वाले व्यायाम।",
                "- उष्णता: गर्म तेलाची मालिश (अभ्यंग) मदत करू शकते।",
                "- टाळा: थंड खाद्य आणि जड/तळलेले भोजन।",
            ],
        },
        "cold_cough": {
            "en": [
                "🩺 **Cold/Cough support (AYUSH-friendly, non-emergency):**",
                "- Rest: prioritize sleep and avoid exposure to cold.",
                "- Hydration: warm water, herbal teas, broth.",
                "- Avoid: dairy and heavy foods during active symptoms.",
            ],
            "hi": [
                "🩺 **सर्दी/खांसी समर्थन (आयुष-अनुकूल, गैर-आपातकालीन):**",
                "- विश्राम: नींद को प्राथमिकता दें और ठंड के संपर्क से बचें।",
                "- जलयोजन: गर्म पानी, हर्बल चाय, शोरबा।",
                "- बचें: सक्रिय लक्षणों के दौरान दूध और भारी खाद्य पदार्थ।",
            ],
            "mr": [
                "🩺 **सर्दी/खांसी समर्थन (आयुष-अनुकूल, गैर-आपातकालीन):**",
                "- विश्राम: झोपेला प्राधान्य द्या आणि थंडीचा संपर्क टाळा।",
                "- जलयोजन: गरम पाणी, औषधी चहा, शोरबा।",
                "- बचा: सक्रिय लक्षणांच्या काळात दूध आणि जड खाद्य।",
            ],
        },
    }
    
    if condition and condition != "general" and condition in advice_map:
        localized_advice = advice_map[condition].get(lang)
        if localized_advice:
            return "\n".join(localized_advice)
    
    return ""


def build_plant_knowledge_snippet(plant: Dict) -> str:
    """
    Build a brief snippet of plant knowledge for context passing to LLM.
    Used in build_llm_context to create formatted plant summaries.
    """
    if not plant:
        return ""
    
    name = plant.get("common_name_en") or plant.get("name") or "Unknown plant"
    description = plant.get("description") or ""
    actions = plant.get("therapeutic_actions") or ""
    
    # Format therapeutic actions if it's a JSON array
    if actions and actions.startswith("["):
        try:
            import json
            actions_list = json.loads(actions)
            actions = ", ".join(actions_list)
        except:
            pass
    
    lines = [f"**{name}**"]
    if description:
        lines.append(f"Description: {description[:200]}")
    if actions:
        lines.append(f"Uses: {actions[:200]}")
    
    return "\n".join(lines)


def build_disease_knowledge_snippet(disease: Dict) -> str:
    """
    Build a brief snippet of disease knowledge for context passing to LLM.
    Used in build_llm_context to create formatted disease summaries.
    """
    if not disease:
        return ""
    
    name = disease.get("name_en") or disease.get("name") or "Unknown condition"
    description = disease.get("description") or ""
    symptoms = disease.get("symptoms") or ""
    
    lines = [f"**{name}**"]
    if description:
        lines.append(f"Overview: {description[:200]}")
    if symptoms:
        lines.append(f"Symptoms: {symptoms[:200]}")
    
    return "\n".join(lines)
