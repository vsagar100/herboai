# Quick Reference: Where Everything Is

## Question 1: Marathi Prep Loss Bug 🐛

### The Bug Location
**File**: [backend/services/chat.py](chat.py#L1430-1460)

**Suspected Bug Area** (around line 1456):
```python
all_preps = fetch_preparations_for_disease(db, disease_id, limit=6)
# For English: returns [6 prep dicts] ✅
# For Marathi: returns [6 prep dicts] ✅

excluded_ids = sess.get("returned_prep_ids", set())
provisional = [p for p in all_preps if p.get("id") not in excluded_ids]
# For English: provisional = [6 prep dicts] ✅
# For Marathi: provisional = [] ❌ ← BUG IS HERE!
```

### How to Debug
Add this after line 1458:
```python
print(f"[DEBUG chat.py:1460] all_preps={len(all_preps)}, lang={lang}")
print(f"[DEBUG chat.py:1461] excluded_ids={excluded_ids}")
print(f"[DEBUG chat.py:1463] provisional after filter={len(provisional)}")
```

Then run the test:
```bash
cd backend
python test_marathi_query.py 2>&1 | grep "DEBUG"
```

---

## Question 2: Actual Database Data Usage ✅

### How Responses Are Built

**For Plant Profiles**:
- **Function**: `build_plant_answer()` in [response_builder.py](response_builder.py#L47-120)
- **Data Source**: `plants` table + `entity_i18n` table
- **Key Line 53-56**: Fetches localized fields using `get_localized_field()`

**For Preparation Recipes**:
- **Function**: `_prep_card()` in [response_builder.py](response_builder.py#L490-525)
- **Data Source**: `preparations` table columns directly
- **Key Fields Used**:
  - `name_en` (preparation name)
  - `preparation_steps` (step-by-step recipe)
  - `dosage_json` (dosage information)
  - `timing` (when to take)
  - `anupana` (with what to take)
  - `notes` (cautions)

**For Disease/Remedy Responses**:
- **Function**: `build_final_response()` in [response_builder.py](response_builder.py#L320-350)
- **Data Source**: Database objects passed as parameters
- **Key Line 340-365**: Iterates over `provisional` list (database records)

### Where to Verify Data Is Real

**Open these files and search for these terms**:

1. In [response_builder.py](response_builder.py):
   - Search: `"preparation_steps"` → Shows real DB field being used
   - Search: `"dosage_json"` → Shows real dosage from database
   - Search: `"get_localized_field"` → Shows lookup from entity_i18n table

2. In [chat.py](chat.py):
   - Search: `"fetch_preparations_for_disease"` → Shows database query
   - Search: `"build_final_response"` → Shows response being built with DB data

3. In [i18n.py](i18n.py):
   - Search: `"entity_i18n"` → Shows localization table lookup
   - Search: `"SELECT text FROM"` → Shows actual SQL queries

---

## Question 3: Marathi/Hindi Language Handling 🌍

### The Complete Pipeline with Line Numbers

| Stage | File | Function | Lines | What Happens |
|-------|------|----------|-------|--------------|
| 1. Detect | [api/nlu_optimized.py](api/nlu_optimized.py) | `detect_language()` | ? | Identifies language |
| 2. Normalize | [utils/i18n.py](i18n.py#L7-11) | `normalize_lang()` | 7-11 | Converts to standard code |
| 3. Store | [chat.py](chat.py#L1128-1135) | `handle_chat()` | 1128-1135 | Saves in session |
| 4. Translate In | [services/indic_translation_service.py](services/indic_translation_service.py) | `translate_to_en()` | ? | Converts to English |
| 5. NLU | [api/nlu_optimized.py](api/nlu_optimized.py) | `classify_intent()` | ? | Processes in English |
| 6. Database | [db.py](db.py#L160-189) | `fetch_preparations_for_disease()` | 160-189 | Language-agnostic query |
| 7. Build Response | [response_builder.py](response_builder.py#L320-350) | `build_final_response()` | 320-350 | Builds with localization |
| 8. Translate Out | [services/indic_translation_service.py](services/indic_translation_service.py) | `translate_from_en()` | ? | Converts to user language |

### Key Code Locations

**Language Detection & Storage** (lines 1128-1135 in [chat.py](chat.py)):
```python
sess = _get_session(session_id)
if lang:
    lang = normalize_lang(lang)
else:
    lang = normalize_lang(sess.get("lang") or detect_language(user_text))
sess["lang"] = lang
```

**Translation for NLU** (line 1134 in [chat.py](chat.py)):
```python
text_en = user_text if lang == "en" else translate_to_en(user_text, lang_hint=lang)
```

**Response Building with Language** (line 1505-1520 in [chat.py](chat.py)):
```python
response = build_final_response(
    ...
    lang=lang,  # ← Must be "mr" for Marathi
)
```

**Translation of Response** (line 1520+ in [chat.py](chat.py)):
```python
answer = translate_from_en(response, lang) if lang != "en" else response
```

### Localization Table Lookup

**File**: [i18n.py](i18n.py#L47-100)

**Function**: `get_localized_field()`

**How it works**:
```python
# Line 53-56: Try localization table first
row = db.execute(
    "SELECT text FROM entity_i18n WHERE entity_type=? AND entity_id=? AND lang=? AND field=?",
    (entity_type, entity_id, lang, field),
).fetchone()

# Line 60+: Fall back to base table if not found
```

**Usage in response building** ([response_builder.py](response_builder.py#L50-56)):
```python
name = get_localized_field("plant", plant_id, "name", lang)
description = get_localized_field("plant", plant_id, "description", lang)
```

---

## How to Test Each Language

### Test English Plant Query
```python
from services.chat import handle_chat

result = handle_chat("Tell me about Ashwagandha", session_id="test_en_1")
print(result['answer'][:200])
# Should show: "## Ashwagandha (Withania somnifera)"
```

### Test Marathi Plant Query
```python
result = handle_chat("अश्वगंधाबद्दल माहिती द्या", session_id="test_mr_1", lang="mr")
print(result['answer'][:200])
# Should show localized response in Marathi
```

### Test Disease Query
```python
# English
result_en = handle_chat("I have a cold", session_id="test_en_cold")
print(f"English preps: {len(result_en['provisional'])}")  # Should be 6

# Marathi (BUG)
result_mr = handle_chat("मला सर्दी आहे", session_id="test_mr_cold", lang="mr")
print(f"Marathi preps: {len(result_mr['provisional'])}")  # Should be 6, but shows 0!
```

---

## Database Schema Reference

### plants table
```sql
SELECT id, common_name_en, botanical_name, description, therapeutic_actions, 
       parts_used, rasa, guna, virya, vipaka, dosha_effect 
FROM plants 
WHERE id = 131;  -- Turmeric
```

### diseases table
```sql
SELECT id, name_en, description, symptoms, causes, prevention_tips 
FROM diseases 
WHERE id = 173;  -- Common Cold
```

### preparations table
```sql
SELECT id, name_en, plant_id, form_type, preparation_steps, 
       dosage_json, timing, anupana, notes 
FROM preparations 
WHERE id = 12;  -- Vasa Leaf Decoction
```

### entity_i18n table (Localization)
```sql
SELECT entity_type, entity_id, lang, field, text 
FROM entity_i18n 
WHERE entity_type='preparation' AND entity_id=12 AND lang='mr' AND field='name';
-- Returns: Marathi name for preparation ID 12
```

### plant_disease_mapping table
```sql
SELECT plant_id, disease_id, efficacy_level 
FROM plant_disease_mapping 
WHERE disease_id = 173;  -- All plants that treat Common Cold
```

---

## Configuration Files

### Model Paths
- **Sentence Embeddings**: [backend/models/all-MiniLM-L6-v2/](models/all-MiniLM-L6-v2/)
- **IndicTrans2 (Hi/Mr)**: [backend/models/trans-en-in/](models/trans-en-in/) and [backend/models/trans-in-en/](models/trans-in-en/)

### Database
- **Path**: [db/new_herboai.db](../db/new_herboai.db)
- **Schema**: [db/new_herboai_newschema.sql](../db/new_herboai_newschema.sql)

---

## Verification Commands

### Verify Database Tables Are Populated
```bash
cd backend
python -c "
from db import get_db
from flask import Flask
app = Flask(__name__)
app.config['DB_PATH'] = '../db/new_herboai.db'
with app.app_context():
    db = get_db()
    print('Plants:', db.execute('SELECT COUNT(*) FROM plants').fetchone()[0])
    print('Diseases:', db.execute('SELECT COUNT(*) FROM diseases').fetchone()[0])
    print('Preparations:', db.execute('SELECT COUNT(*) FROM preparations').fetchone()[0])
    print('entity_i18n:', db.execute('SELECT COUNT(*) FROM entity_i18n').fetchone()[0])
"
```

### Check If Marathi Data Exists
```bash
python -c "
from db import get_db
from flask import Flask
app = Flask(__name__)
app.config['DB_PATH'] = '../db/new_herboai.db'
with app.app_context():
    db = get_db()
    # Check Marathi in entity_i18n
    result = db.execute(
        'SELECT COUNT(*) FROM entity_i18n WHERE lang=\"mr\"'
    ).fetchone()[0]
    print(f'Marathi entries in entity_i18n: {result}')
"
```

### Run Full Test Suite
```bash
cd backend
python final_verification.py 2>&1 | grep -E "TEST|PASS|FAIL|SUMMARY"
```

---

## Next Steps

1. **Add debug logging** to [chat.py](chat.py#L1430-1460) around the `provisional` list
2. **Run test** to see where preps disappear: `python test_marathi_query.py`
3. **Identify the bug** in the response-building flow
4. **Fix the condition** that's stripping out preps for Marathi
5. **Test again** to confirm preps appear in Marathi response

This should take 15-30 minutes once debug output pinpoints the issue!
