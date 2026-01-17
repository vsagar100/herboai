# HerboAI Language & Response Pipeline Documentation

## Overview

The HerboAI chatbot uses a **database-first approach** for response generation, meaning all responses are built from actual database data rather than templates. The system has full multilingual support for English, Hindi, and Marathi.

---

## 1. How Language Detection & Handling Works

### 1.1 Language Detection Flow

```
User Query (Marathi/Hindi/English)
    ↓
detect_language(user_text)  [from nlu_optimized.py]
    ↓
normalize_lang(detected_lang)
    ↓
Store in session["lang"]  (stable per session)
```

**Key Code** ([chat.py](chat.py#L1128-L1134)):
```python
# Language: respect explicit; otherwise detect once and keep stable in session
sess = _get_session(session_id)
if lang:
    lang = normalize_lang(lang)
else:
    # prefer stable session language if already known
    lang = normalize_lang(sess.get("lang") or detect_language(user_text))
sess["lang"] = lang

# English text for intent/NER (always process in English internally)
text_en = user_text if lang == "en" else translate_to_en(user_text, lang_hint=lang)
```

### 1.2 Language Processing Stages

| Stage | Input | Process | Output |
|-------|-------|---------|--------|
| **Detect** | Raw user text | `detect_language()` | Language code (en/hi/mr) |
| **Normalize** | Language code | `normalize_lang()` | Canonical code (en/hi/mr) |
| **Translate to EN** | Marathi/Hindi text | `translate_to_en()` (IndicTrans2) | English for NLU |
| **Process** | English text | Intent/entities/NLU | Processing results |
| **Translate from EN** | English response | `translate_from_en()` (IndicTrans2) | User's language |

### 1.3 Supported Languages

| Language | Code | Detection | Translation |
|----------|------|-----------|-------------|
| English | `en` | ✅ Auto-detected | ✅ No translation needed |
| Hindi | `hi` | ✅ Auto-detected | ✅ IndicTrans2 |
| Marathi | `mr` | ✅ Auto-detected | ✅ IndicTrans2 |

---

## 2. How Responses Are Built (Database-First)

### 2.1 Response Flow Architecture

The system **ALWAYS uses actual database data** to build responses. Here's the complete flow:

```
User Query (any language)
    ↓
Language Detection & Translation to English
    ↓
Intent Classification & Entity Extraction
    ↓
Resolve to Database IDs (plant ID, disease ID, preparation ID)
    ↓
Fetch ACTUAL data from database
    ↓
Build response using response_builder.py with real data
    ↓
Translate response to user's language
    ↓
Return to user
```

### 2.2 Response Builder Functions

The [response_builder.py](response_builder.py) module has these key functions:

#### For Plant Queries:
```python
build_plant_answer(plant: Dict, lang: str = "en") -> str
```
- **Input**: Plant data dict with ID for entity_i18n lookup
- **Process**:
  1. Fetch localized plant name from `entity_i18n` table (or fallback to base table)
  2. Fetch localized description, therapeutic actions, parts used
  3. Format Ayurvedic properties (rasa, guna, virya, vipaka, dosha)
  4. Build formatted response
- **Output**: Formatted plant profile response in user's language
- **Data Used**: `plants` table + `entity_i18n` table

#### For Disease/Remedy Queries:
```python
build_final_response(severity, provisional, optional_questions, condition, slots, lang) -> str
```
- **Input**: 
  - `provisional`: List of preparation dicts fetched from DB
  - `condition`: Disease classification
  - `lang`: User's language
- **Process**:
  1. Get disease info from `diseases` table
  2. For each preparation in `provisional`:
     - Fetch localized name from `entity_i18n`
     - Fetch actual preparation_steps, dosage_json, timing, anupana from `preparations` table
     - Format with real data
  3. Build final response markdown
- **Output**: Complete remedy response with actual preparation recipes
- **Data Used**: `diseases` table + `preparations` table + `entity_i18n` table

#### For Preparation Queries:
```python
_build_plant_preparation_answer(plant: Dict, preps: List[Dict]) -> str
```
- **Input**: Plant dict + list of preparation dicts from DB
- **Process**:
  1. Get plant name and botanical name
  2. For each preparation dict:
     - Extract `preparation_steps` from DB (formatted as JSON or text)
     - Extract `dosage_json` from DB
     - Extract `timing`, `anupana`, `notes` from DB
     - Format as markdown
- **Output**: Formatted preparation recipe response
- **Data Used**: `plants` table + `preparations` table

### 2.3 Entity Localization

The `get_localized_field()` function ([i18n.py](i18n.py#L47-L100)):
```python
def get_localized_field(entity_type: str, entity_id: int, field: str, lang: str) -> str
```

**Process**:
1. First, try to fetch from `entity_i18n` table:
   ```sql
   SELECT text FROM entity_i18n 
   WHERE entity_type=? AND entity_id=? AND lang=? AND field=?
   ```

2. If not found, fallback to base tables (backward compatibility):
   ```sql
   SELECT {field_column} FROM {entity_type}s WHERE id=?
   ```

**Example**:
- Query: `get_localized_field("plant", 131, "description", "mr")`
- First tries: `entity_i18n WHERE entity_type='plant' AND entity_id=131 AND lang='mr' AND field='description'`
- If found: Returns Marathi description
- If not found: Falls back to `plants.description` (English)

---

## 3. Complete Query-to-Response Examples

### Example 1: English Plant Query ✅

**User Query**: "Tell me about Ashwagandha"

```
Step 1: Language Detection
  detect_language("Tell me about Ashwagandha") → "en"
  
Step 2: NLU
  intent = "plant_info"
  entities = {"plant": "ashwagandha"}
  
Step 3: Database Lookup
  _find_plant_id("ashwagandha") → ID 2
  _fetch_plant_full(2) → {id: 2, common_name_en: "Ashwagandha", ...}
  
Step 4: Response Building
  build_plant_answer(plant, lang="en")
    → Fetches from plants table + entity_i18n (lang='en')
    → Returns English plant profile with actual data
    
Step 5: No Translation Needed
  Response is already in English
```

**Response**:
```
## Ashwagandha (Withania somnifera)

Ashwagandha is a powerful adaptogenic herb...

**Parts used:** Root, Leaves
**Key actions:** Stress relief, Immune support, Energy enhancement
**Rasa (taste):** Bitter, Astringent
...
```

---

### Example 2: Marathi Disease Query ⚠️ (Currently Has Issues)

**User Query**: "मला सर्दी आहे" (I have a cold - Marathi)

```
Step 1: Language Detection
  detect_language("मला सर्दी आहे") → "mr"
  sess["lang"] = "mr"
  
Step 2: Translation to English
  translate_to_en("मला सर्दी आहे", lang_hint="mr") → "I have a cold"
  text_en = "I have a cold"
  
Step 3: NLU (on English text)
  intent = "symptom" or "disease"
  entities = {"disease": "cold"}
  
Step 4: Condition Classification
  _classify_condition("मला सर्दी आहे") → "cold_cough"
  
Step 5: Disease Resolution
  CONDITION_TO_DISEASE["cold_cough"] → "common cold"
  resolve_disease_id(db, "common cold") → ID 173
  
Step 6: Database Fetch
  fetch_preparations_for_disease(173) → [
    {id: 12, name_en: "Turmeric Milk", preparation_steps: "...", ...},
    {id: 45, name_en: "Ginger Tea", ...},
    ...
  ]
  
Step 7: Response Building
  build_final_response(
    provisional=[preps from DB],
    lang="mr"
  )
    → Fetches localized disease name from entity_i18n (lang='mr')
    → For each preparation:
      - Fetches localized name from entity_i18n
      - Gets actual preparation_steps, dosage from preparations table
      - Formats as markdown
    → Returns markdown in English
    
Step 8: Translate to Marathi
  translate_from_en(response_en, "mr") → Response in Marathi
```

---

## 4. Data Sources for Responses

### 4.1 Base Tables (Always Used)

| Table | Fields Used | Purpose |
|-------|------------|---------|
| `plants` | id, common_name_en, botanical_name, description, therapeutic_actions, parts_used, rasa, guna, virya, vipaka, dosha_effect | Plant core data |
| `diseases` | id, name_en, description, symptoms, causes, prevention_tips | Disease core data |
| `preparations` | id, name_en, plant_id, form_type, preparation_steps, dosage_json, timing, anupana, notes | Preparation recipes & dosage |
| `plant_disease_mapping` | plant_id, disease_id, efficacy_level | Which plants treat which diseases |

### 4.2 Localization Table (For Multilingual)

| Table | Fields | Purpose |
|-------|--------|---------|
| `entity_i18n` | entity_type, entity_id, lang, field, text | Localized content for plants/diseases/preparations |

**Example entries**:
```
entity_type='plant', entity_id=131, lang='mr', field='name', text='हळद'
entity_type='plant', entity_id=131, lang='hi', field='name', text='हल्दी'
entity_type='disease', entity_id=173, lang='mr', field='description', text='सर्दी ही एक...'
```

### 4.3 Records Verified ✅

From earlier `db_check.py`:
- **plants**: 230 records with English names ✅
- **diseases**: 64 records with English names ✅
- **preparations**: 277 records with recipes ✅
- **entity_i18n**: 4,696 localized entries ✅
- **plant_disease_mapping**: 278+ mappings ✅

---

## 5. Current Issues with Marathi Queries

### Issue: Marathi Responses Are Incomplete/Truncated

**Evidence**:
- English responses: Full, detailed, with all sections (symptoms, preparations, dosage, etc.)
- Marathi responses: Missing sections, truncated preparation details

**Root Cause Analysis**:

The system **IS using actual database data**, but there's a translation pipeline issue:

1. **Step 1-6 Work Correctly**:
   - Marathi → English translation works
   - NLU detects intent correctly
   - Database fetch returns full preparation data

2. **Step 7-8 Have Issues**:
   - `build_final_response()` builds full English response ✅
   - `translate_from_en(response_en, "mr")` translates but may **truncate or lose sections**

**Why Translation Fails**:
- IndicTrans2 model may have length limits
- JSON structure in `preparation_steps` might not translate well
- Complex markdown formatting might break during translation

### Potential Fixes

**Option 1: Translate Individual Fields (Recommended)**
```python
# Instead of translating the full response markdown:
answer_en = build_final_response(...)  # Full response
answer_mr = translate_from_en(answer_en, "mr")  # May truncate

# Do this instead:
for prep in provisional:
    prep["name_mr"] = translate_from_en(prep["name_en"], "mr")
    prep["steps_mr"] = translate_from_en(prep["preparation_steps"], "mr")
    prep["dosage_mr"] = translate_from_en(prep["dosage_json"], "mr")

# Then build response using localized fields
```

**Option 2: Use entity_i18n For All Fields**
- Pre-populate `entity_i18n` with Marathi preparation details
- This avoids on-demand translation delays/truncation

**Option 3: Check Translation Service Limits**
```python
# In indic_translation_service.py
# Check if there are length/chunk limits in IndicTrans2
```

---

## 6. Confirmation: YES, Using Actual Database Data

### Evidence That Responses Use Real Data:

1. **Plant Queries** ✅
   - `build_plant_answer()` calls `get_localized_field("plant", plant_id, field, lang)`
   - Which queries `entity_i18n` table
   - Falls back to `plants` table
   - **Actual data from DB used**

2. **Disease Queries** ✅
   - `fetch_preparations_for_disease(disease_id)` queries `preparations` table
   - `build_final_response()` iterates over preparation dicts
   - For each prep, fetches localized name + details from DB
   - **Actual data from DB used**

3. **Preparation Queries** ✅
   - `_build_plant_preparation_answer()` uses prep dicts from DB
   - Extracts `preparation_steps`, `dosage_json`, `timing`, `anupana` directly
   - No templates, only actual DB data
   - **Actual data from DB used**

### NOT Using Templates:
- ❌ No hardcoded responses
- ❌ No template files
- ❌ No fallback generic strings (except for error/help messages)
- ✅ Everything comes from database

---

## 7. Summary & Recommendations

### Current State

| Query Type | English | Hindi | Marathi |
|-----------|---------|-------|---------|
| Plant Info | ✅ Working | ⚠️ Untested | ⚠️ Likely truncated |
| Disease/Remedy | ✅ Working | ⚠️ Untested | ⚠️ Likely truncated |
| Preparation | ✅ Working | ⚠️ Untested | ⚠️ Likely truncated |

### Why Marathi Fails

1. **Database**: ✅ Has data (4,696 i18n entries)
2. **Detection**: ✅ Marathi detected correctly
3. **NLU**: ✅ Intent extracted correctly
4. **Lookup**: ✅ Database queries return full data
5. **Response Building**: ✅ Markdown built with all sections
6. **Translation**: ⚠️ **IndicTrans2 may truncate/lose formatting**

### Next Steps to Debug/Fix

1. **Check translation limits**:
   ```python
   # Test in services/indic_translation_service.py
   long_text = "..." # 500+ word response
   result = translate_to_en(long_text, "mr")
   print(len(result))  # Does it match input length?
   ```

2. **Try field-level translation**:
   - Translate preparation names separately
   - Translate steps separately
   - Combine in response building

3. **Check entity_i18n population**:
   - Are Marathi preparation names in entity_i18n?
   - Or relying on translate_from_en every time?

4. **Test with smaller responses**:
   - Query with 1 disease instead of 5+
   - See if fewer preps = complete Marathi response

---

## File References

- **Main Pipeline**: [backend/services/chat.py](chat.py#L1122-L1160)
- **Response Builder**: [backend/services/response_builder.py](response_builder.py)
- **Language/i18n**: [backend/utils/i18n.py](i18n.py)
- **Translation Service**: [backend/services/indic_translation_service.py](services/indic_translation_service.py)
