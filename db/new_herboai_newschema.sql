-- ============================================================================
-- HerboAI: Single-path multilingual storage + retrieval (en/hi/mr)
-- - entity_i18n (auto/verified)
-- - separate FTS per language
-- - separate vec0 per language
-- - efficacy_level + indications_tags (admin-curated)
-- ============================================================================

BEGIN;

-- 1) I18N store: single truth for user-facing text
CREATE TABLE IF NOT EXISTS entity_i18n (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  entity_type TEXT NOT NULL CHECK (entity_type IN ('plant','disease','preparation')),
  entity_id INTEGER NOT NULL,
  lang TEXT NOT NULL CHECK (lang IN ('en','hi','mr')),
  field TEXT NOT NULL,
  text TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'auto' CHECK (status IN ('auto','verified')),
  source TEXT NOT NULL DEFAULT 'indictrans2' CHECK (source IN ('indictrans2','manual')),
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE(entity_type, entity_id, lang, field)
);

CREATE INDEX IF NOT EXISTS idx_entity_i18n_lookup
ON entity_i18n(entity_type, entity_id, lang);

CREATE INDEX IF NOT EXISTS idx_entity_i18n_field
ON entity_i18n(entity_type, lang, field);


-- 2) Admin-curated efficacy + tags
-- Plants: baseline (used when plant-only answer, or as fallback)
ALTER TABLE plants ADD COLUMN efficacy_level INTEGER;
ALTER TABLE plants ADD COLUMN indications_tags TEXT; -- JSON array string, e.g. ["cough","fever"]
ALTER TABLE plants ADD COLUMN onset_speed TEXT;      -- optional: 'fast'|'medium'|'slow'

-- Preparations: primary efficacy lives here
ALTER TABLE preparations ADD COLUMN efficacy_level INTEGER;
ALTER TABLE preparations ADD COLUMN indications_tags TEXT; -- JSON array string
ALTER TABLE preparations ADD COLUMN onset_speed TEXT;      -- 'fast'|'medium'|'slow'
ALTER TABLE preparations ADD COLUMN difficulty_level TEXT; -- 'easy'|'medium'|'hard'

COMMIT;
