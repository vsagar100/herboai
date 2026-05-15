# Quick Start: Testing the Fix

## Step 1: Populate entity_i18n Table (REQUIRED)

```bash
cd backend
python -m services.migrate_to_entity_i18n --dry-run --verbose
```

Review the output. If it looks good:

```bash
python -m services.migrate_to_entity_i18n --verbose
```

This will:
- Translate 277 plants to Hindi and Marathi
- Translate diseases and preparations
- Rebuild FTS tables for all 3 languages
- Rebuild vector search tables
- Takes ~2-3 minutes depending on translation service speed

## Step 2: Restart Backend

```bash
# Stop current backend process
# Then restart it
python run.py
```

## Step 3: Test in Frontend

### Test Case 1: Disease Query (English)
```
User: "treatment for diabetes"
Expected Response:
- Should show "Diabetes overview" in English
- List 3-5 preparations
- Include markdown formatting (bold labels, etc.)
- NO repeated items
```

### Test Case 2: Same Session, Different Query
```
Same session_id:
User: "what helps diabetes?"
Expected Response:
- Should show DIFFERENT preparations (not repeat from Test 1)
- OR should say "no additional preparations found"
```

### Test Case 3: Hindi Query
```
User: "मधुमेह के लिए उपचार"
Expected Response:
- Response in Hindi
- "मधुमेह सारांश" (Diabetes overview)
- Herb names in Hindi (e.g., नीम, तुलसी)
- Preparation names in Hindi
- Markdown preserved (proper **bold**, not corrupted)
```

### Test Case 4: Marathi Query
```
User: "मधुमेह साठी उपचार"
Expected Response:
- Response in Marathi
- "मधुमेह विहंगावलोकन"
- Markdown preserved
```

### Test Case 5: Plant Info
```
User: "tell me about neem"
Expected Response:
- Plant profile in English
- Parts used, Key actions, Constitutional profile
- Markdown formatted
```

### Test Case 6: Followup Questions
```
Conversation:
1. User: "I have cough" 
   → Bot asks: "Since when?", "Better or worse?", "Age/gender?", etc.

2. User: "3 days" (same session)
   → Bot should ask DIFFERENT questions, NOT repeat "Since when?"
```

## Verification Checks

### ✅ Check 1: No Repeated Remedies
- Open browser dev console → Network tab → WebSocket
- Send disease query twice in same session
- Verify preparation IDs in responses don't overlap
- Session state should show: `returned_prep_ids: {1, 5, 7, ...}`

### ✅ Check 2: Multilingual Labels
Search for these in responses:
- English: "Parts used", "Key actions", "Helpful herbs"
- Hindi: "उपयोग के भाग", "मुख्य कार्य", "सहायक जड़ी बूटियां"
- Marathi: "वापरण्यास भाग", "मुख्य कार्ये", "मदतीस औषधी वनस्पती"

### ✅ Check 3: Markdown Preservation
- Check response contains:
  - `**Bold text**` properly rendered
  - `##` headers properly rendered
  - Bullet lists properly formatted
  - No UTF-8 corruption (Hindi/Marathi text readable)

### ✅ Check 4: SQL Fix Working
- Run this in SQLite:
```sql
SELECT COUNT(*) FROM preparations pr 
INNER JOIN preparation_ingredients pgi ON pgi.preparation_id = pr.id 
INNER JOIN plants p ON p.id = pgi.plant_id 
INNER JOIN plant_disease_mapping pdm ON pdm.plant_id = p.id 
AND pdm.disease_id = 1 LIMIT 1;
```
Should return rows without errors (disease_id=1 is diabetes).

### ✅ Check 5: No Repeated Followups
- Send symptom query: "I have fever"
- Bot asks followup questions
- Send answer: "3 days"
- Bot should ask NEW questions, not repeat the same ones
- Check session state: `asked_questions: {"Since when...?", "Better or worse...?", ...}`

## Debug: View Session State

Add this to `routes.py` or `chat.py` for debugging:

```python
@app.route("/debug/session/<session_id>", methods=["GET"])
def debug_session(session_id):
    from services.chat import _SESSIONS
    sess = _SESSIONS.get(session_id)
    if not sess:
        return {"error": "Session not found"}, 404
    return {
        "id": session_id,
        "lang": sess.get("lang"),
        "stage": sess.get("stage"),
        "returned_prep_ids": list(sess.get("returned_prep_ids", set())),
        "asked_questions": list(sess.get("asked_questions", set())),
        "slots": sess.get("slots", {}),
    }
```

Then visit: `http://localhost:5000/debug/session/YOUR_SESSION_ID`

## Troubleshooting

### Issue: entity_i18n table still empty after migration
```bash
python -m services.migrate_to_entity_i18n --verbose
# Check output for errors
# Ensure indic_translation_service.py is working
# Check database has permissions to write
```

### Issue: Responses still in English after migration
1. Check session state - is `lang` being detected? (Use `/debug/session/` endpoint)
2. Check if response_builder functions are being called with `lang` param
3. Verify entity_i18n has data: `SELECT COUNT(*) FROM entity_i18n;` should be > 0

### Issue: Markdown not rendering (bold, headers broken)
- This was the original issue (post-translation breaking markdown)
- If still happening: responses are being translated post-build
- Check chat.py line ~1435 - should NOT have `translate_from_en()` call
- Response builders should be called with `lang=lang` parameter

### Issue: Repeated remedies still appearing
- Check session state `returned_prep_ids` is being populated
- Verify deduplication logic in `handle_chat()` around line 1340-1360
- Check that session_id is consistent across messages

## Performance Notes

- First migration: ~2-3 minutes (translation via IndicTrans2)
- Subsequent queries: < 200ms (all content cached or in DB)
- Vector search fallback: < 100ms
- FTS queries: < 50ms

## Rollback

If anything breaks:
```bash
# Restore original response_builder.py
git checkout backend/services/response_builder.py

# Clear entity_i18n
sqlite3 <db_path> "DELETE FROM entity_i18n;"

# Restart
python run.py
```

System will fall back to English-only mode (original behavior).

---

**Support**: Check `IMPLEMENTATION_COMPLETE.md` for full documentation.
