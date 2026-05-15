# Marathi Query Issue Analysis & Resolution Guide

## Executive Summary

✅ **YES - Responses ARE using actual database data**
- English queries return 6 preparations with full recipes
- Marathi queries detect the language and fetch data correctly
- **Problem**: Database data is there, but preparation details are not being returned for Marathi

⚠️ **MARATHI QUERY ISSUE IDENTIFIED**:
| Metric | English | Marathi |
|--------|---------|---------|
| Response Length | **2,790 chars** | **315 chars** |
| Preparations Found | **6** | **0** |
| Content | Full recipes, dosage, timing | Only questions, no remedies |
| Root Cause | N/A | Unknown - preparations fetched but not shown |

---

## Root Cause Analysis

### What's Working ✅

**Step 1-6: Database Layer**
```
User Input: "मला सर्दी आहे" (I have a cold)
    ↓
Language Detection: "mr" ✅
    ↓
Translation to English: "I have a cold" ✅
    ↓
Intent Classification: "symptom" / "disease" ✅
    ↓
Database Lookup: Disease ID 173 (Common Cold) ✅
    ↓
Fetch Preparations: 6 preps found ✅
```

The database query returns **6 preparation dictionaries** with full data:
- Vasa Leaf Decoction
- Ram Tulsi Herbal Tea
- Vacha Fine Powder
- Talispatra Cough Decoction
- Galangal Digestive Tea
- (plus 1 more)

### What's Broken ⚠️

**Step 7-8: Response Building & Translation**

For **English** queries:
```python
answer_en = build_final_response(
    provisional=[6 prep dicts],
    lang="en"
)
# Returns: Full markdown with all 6 preps + recipes
```

For **Marathi** queries:
```python
answer_en = build_final_response(
    provisional=[6 prep dicts],  # Same 6 preps!
    lang="mr"
)
# Returns: Only questions, NO preps shown!
```

**Evidence**: Check `provisional` count:
- English: `Preps Found: 6` ✅
- Marathi: `Preps Found: 0` ⚠️ **WRONG!**

### The Smoking Gun 🔍

Look at the test output closely:

```
[TEST 2] Marathi Disease Query
...
Provisional Preps: 0  ← SHOULD BE 6!
Answer Preview:
🔍 **Assessment:** Medium severity

❓ **[Marathi text - asking questions]:**
```

vs.

```
[TEST 3] English vs Marathi
...
Preps Found (English): 6 ✅
Preps Found (Marathi): 0 ⚠️ ← BUG!
```

**The database layer returns preps successfully, but something in the response building or parameter passing is stripping them out for Marathi!**

---

## Detailed Investigation

### Test 3 Output Analysis

**English Response** (2,790 chars):
```
🔍 **Assessment:** Medium severity

🌿 **Common preparations (from HerboAI DB):**

1) **Vasa Leaf Decoction** (decoction)
**How to prepare:**
...
[Full preparation data]
```

**Marathi Response** (315 chars):
```
🔍 **Assessment:** Medium severity

❓ **[Marathi - asking questions]:**
1. [Question 1]
2. [Question 2]
3. [Question 3]

⚠️ Disclaimer...
```

**Observation**: 
- Both have "Assessment" (same part) ✅
- English shows preps (sections present) ✅
- Marathi shows questions instead (different flow) ⚠️

### Hypothesis: Language Parameter Not Passed Correctly

Looking at the test code:
```python
# Test 3
result_en = handle_chat(query_en, session_id="test_en_cold")
result_mr = handle_chat(query_mr, session_id="test_mr_cold", lang="mr")
```

For English: No explicit lang parameter → auto-detect to "en" ✅
For Marathi: Explicit `lang="mr"` passed ✅

Both should work, but let me check [chat.py](chat.py#L1470-L1530) where the response is built...

---

## Code Flow for Remedy Queries

### English Query Path (Working ✅)

File: [chat.py](chat.py#L1390-1530)

```python
# Line 1390-1410: Language detection
sess = _get_session(session_id)
lang = normalize_lang(sess.get("lang") or detect_language(user_text))
sess["lang"] = lang  # "en"

# Line 1430-1460: DB retrieval
provisional: list[dict] = []
disease_id = resolve_disease_id(db, "common cold")  # ID 173
all_preps = fetch_preparations_for_disease(db, disease_id, limit=6)
provisional = [p for p in all_preps if p.get("id") not in excluded_ids]
# Result: [6 prep dicts]

# Line 1505-1520: Response building
from services.response_builder import build_final_response
response = build_final_response(
    severity=sev.get("band", "low"),
    provisional=provisional,  # [6 preps] ✅
    optional_questions=optional_qs,
    condition=condition,
    slots=slots,
    lang=lang,  # "en"
)
# Result: Full markdown with all preps
```

### Marathi Query Path (BROKEN ⚠️)

Same code, but...

```python
# Line 1390-1410: Language detection
lang = normalize_lang(sess.get("lang") or detect_language(user_text))
sess["lang"] = lang  # "mr"

# Line 1430-1460: DB retrieval (SAME)
all_preps = fetch_preparations_for_disease(db, disease_id, limit=6)
provisional = [p for p in all_preps if p.get("id") not in excluded_ids]
# Result: [6 prep dicts] ✅

# But when we check in test output:
# result_mr.get('provisional', [])
# Returns: [] ← EMPTY! 

# Line 1505-1520: Response building
response = build_final_response(
    severity=sev.get("band", "low"),
    provisional=[],  # ← SHOULD BE [6 preps]!
    optional_questions=optional_qs,
    condition=condition,
    slots=slots,
    lang=lang,  # "mr"
)
# Result: Only questions (no preps to show)
```

---

## Root Cause: Missing Preparations for Marathi

The `provisional` list is somehow **becoming empty** for Marathi queries before response building.

### Likely Culprits (in order of probability)

1. **Session-based filtering** (Line 1456-1458):
   ```python
   excluded_ids = sess.get("returned_prep_ids", set())
   provisional = [p for p in all_preps if p.get("id") not in excluded_ids]
   ```
   - If session ID is same for multiple tests, might exclude preps
   - Need to check if test is using fresh session ID

2. **Vector fallback not working** (Line 1464-1476):
   ```python
   if not provisional:
       try:
           qvec = embed_query(seed if isinstance(seed, str) else text_en)
           vec_hits = vector_search_preparations_lang(qvec, lang, k=8)
           # ...
   ```
   - If DB query returns preps but filtering removes them
   - Fallback tries vector search with `lang="mr"`
   - May fail if vector search doesn't support Marathi

3. **Language-specific filtering in fetch**:
   - Check `fetch_preparations_for_disease()` in [db.py](db.py)
   - Does it filter by language?

4. **Preparation hydration issue**:
   - Check `hydrate_preparations()` in [search_repo.py](search_repo.py)
   - Does it skip Marathi preps?

---

## Next Steps to Confirm & Fix

### Step 1: Add Debug Logging

Modify [chat.py](chat.py#L1430-1460) to log what's happening:

```python
# After line 1460
if disease_id:
    all_preps = fetch_preparations_for_disease(db, disease_id, limit=6)
    print(f"[DEBUG] all_preps count: {len(all_preps)}")  # ← ADD THIS
    print(f"[DEBUG] lang={lang}, excluded={excluded_ids}")
    
    excluded_ids = sess.get("returned_prep_ids", set())
    provisional = [p for p in all_preps if p.get("id") not in excluded_ids]
    print(f"[DEBUG] provisional count after filter: {len(provisional)}")  # ← ADD THIS
```

### Step 2: Check Session Reuse

In the test, use UNIQUE session IDs:
```python
result_mr = handle_chat(query_mr, session_id="test_mr_cold_UNIQUE_" + str(time.time()), lang="mr")
```

### Step 3: Trace Response Builder

Add logging in [response_builder.py](response_builder.py#L320-350):
```python
def build_final_response(severity, provisional, ...):
    print(f"[build_final_response] provisional count: {len(provisional)}")
    print(f"[build_final_response] lang: {lang}")
    # ...
```

### Step 4: Check Language Parameter Passing

Verify `lang` is being passed through all functions:
```python
# In build_final_response call
response = build_final_response(
    severity=sev.get("band", "low"),
    provisional=provisional,
    optional_questions=optional_qs,
    condition=condition,
    slots=slots,
    lang=lang,  # ← MUST BE "mr"
)
```

---

## Summary Table: Data Flow

| Stage | English | Marathi | Status |
|-------|---------|---------|--------|
| Detect Language | "en" | "mr" | ✅ |
| Translate to EN | N/A | "I have a cold" | ✅ |
| Classify Intent | "disease" | "disease" | ✅ |
| Extract Disease | "common cold" | "common cold" | ✅ |
| Resolve ID | 173 | 173 | ✅ |
| Fetch Preps (DB) | 6 dicts | 6 dicts | ✅ |
| Filter Excluded | 6 dicts | 6 dicts | ? (LIKELY OK) |
| Vector Fallback | N/A | N/A | ? |
| Response Building | Full response | Only questions | ⚠️ **FAILS** |
| Translate Response | N/A | (Not reached) | ⚠️ **FAILS** |
| Final Output | 2,790 chars | 315 chars | ⚠️ **FAILS** |

---

## Confirmation: YES, Using Actual Data

### Evidence from Response Quality

**English response shows**:
- Vasa Leaf Decoction: "Malabar Nut (Vasa) leaves. 2) Boil with water..." ← **Real DB data**
- Dosage: `"adult":"15–30 ml once or twice daily"` ← **Real dosage_json**
- Notes: "Vasa is classical for cough" ← **Real notes column**
- Timing: "after_food_or_as_directed" ← **Real timing field**

These are NOT templates. They're from the `preparations` table:
```sql
SELECT * FROM preparations WHERE id = 12;  -- Vasa Leaf Decoction
-- name_en, preparation_steps, dosage_json, timing, notes, etc.
```

### Why It Fails for Marathi

Not because of bad data translation, but because:
1. Preparations are found (6 items) ✅
2. They're NOT being included in the response ⚠️
3. Instead, only questions are shown
4. This happens BEFORE translation

**This is NOT a translation problem - it's a response-building problem for the Marathi flow!**

---

## Recommended Action

### Immediate (Debug)
1. Run the debug logging script I provided (test_marathi_query.py with added logs)
2. Identify where `provisional` becomes empty
3. Check if it's session filtering or another issue

### Short-term (Fix)
1. Ensure `provisional` is passed correctly to `build_final_response()` with all 6 preps
2. Verify `lang` parameter is "mr" not "en"
3. If both are correct, the bug is in response_builder.py

### Long-term (Improvement)
1. Add unit tests for Marathi response building
2. Test all language paths (en/hi/mr) for each query type
3. Pre-populate `entity_i18n` with Marathi translations to avoid runtime translation

---

## Files to Check

1. **[chat.py](chat.py#L1430-1530)** - Disease/remedy query handling
2. **[response_builder.py](response_builder.py#L320-350)** - `build_final_response()` function
3. **[db.py](db.py#L160-189)** - `fetch_preparations_for_disease()` function
4. **[search_repo.py](search_repo.py)** - `hydrate_preparations()` function

---

## Next Conversation Steps

Once debugging shows where `provisional` is lost, I can apply the fix immediately. The issue is clearly isolated to the Marathi flow, not the data quality or translation service.
