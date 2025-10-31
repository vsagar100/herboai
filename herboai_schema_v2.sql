
-- ============================================================================
-- HERBOAI DATABASE SCHEMA v2 (SQLite)
-- Focus: Multilingual herbs, evidence-linked remedies, normalized preparations,
-- safety metadata, FTS + vectors, and compatibility view for "remedies".
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ============================================================================
-- LOOKUP TABLES
-- ============================================================================

CREATE TABLE IF NOT EXISTS ayush_system (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL UNIQUE  -- e.g., Ayurveda, Yoga, Unani, Siddha, Homeopathy
);

INSERT OR IGNORE INTO ayush_system (id, name) VALUES
(1,'Ayurveda'),(2,'Yoga'),(3,'Unani'),(4,'Siddha'),(5,'Homeopathy'),(6,'Multiple');

-- ============================================================================
-- CORE ENTITIES
-- ============================================================================

CREATE TABLE IF NOT EXISTS plants (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  botanical_name TEXT NOT NULL UNIQUE,
  common_name_en TEXT,
  common_name_hi TEXT,
  common_name_mr TEXT,
  sanskrit_name TEXT,
  family TEXT,
  ayush_system_id INTEGER NOT NULL DEFAULT 1,
  description TEXT,
  habitat TEXT,
  parts_used TEXT,                 -- JSON array ["root","leaf",...]
  rasa TEXT,                       -- JSON array ["madhura","tikta"]
  virya TEXT,                      -- "ushna" or "sheeta" etc.
  vipaka TEXT,
  guna TEXT,                       -- JSON array
  dosha_effect TEXT,               -- JSON {"vata":"reduces","pitta":"neutral","kapha":"reduces"}
  prabhava TEXT,
  active_compounds TEXT,           -- JSON array
  therapeutic_actions TEXT,        -- JSON array
  classical_references TEXT,       -- JSON array
  is_endangered INTEGER DEFAULT 0,
  cultivation_status TEXT,         -- "wild","cultivated","both"
  image_hero TEXT,                 -- optional hero image path/url
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (json_valid(parts_used) OR parts_used IS NULL),
  CHECK (json_valid(rasa) OR rasa IS NULL),
  CHECK (json_valid(guna) OR guna IS NULL),
  CHECK (json_valid(dosha_effect) OR dosha_effect IS NULL),
  CHECK (json_valid(active_compounds) OR active_compounds IS NULL),
  CHECK (json_valid(therapeutic_actions) OR therapeutic_actions IS NULL),
  CHECK (json_valid(classical_references) OR classical_references IS NULL),
  FOREIGN KEY (ayush_system_id) REFERENCES ayush_system(id) ON DELETE RESTRICT
);

CREATE TRIGGER IF NOT EXISTS trg_plants_updated
AFTER UPDATE ON plants FOR EACH ROW
BEGIN
  UPDATE plants SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Media (multiple images/videos per plant, local-friendly paths)
CREATE TABLE IF NOT EXISTS media (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  path TEXT NOT NULL,            -- relative file path (preferred) or URL
  alt_text TEXT,
  type TEXT DEFAULT 'image',     -- image | video | diagram
  is_primary INTEGER DEFAULT 0,
  attribution TEXT,
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);

-- Synonyms for plants (regional/trade names etc.)
CREATE TABLE IF NOT EXISTS plant_synonyms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  synonym TEXT NOT NULL,
  language TEXT,                 -- "en","hi","mr","regional"
  kind TEXT,                     -- "common_name","regional_name","trade_name"
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);

-- Diseases/conditions
CREATE TABLE IF NOT EXISTS diseases (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_en TEXT NOT NULL,
  name_hi TEXT,
  name_mr TEXT,
  category TEXT NOT NULL,        -- respiratory, digestive, metabolic, etc.
  ayurvedic_name TEXT,
  unani_name TEXT,
  siddha_name TEXT,
  description TEXT,
  symptoms TEXT,                 -- JSON array
  causes TEXT,                   -- JSON array
  dosha_involvement TEXT,        -- JSON e.g. {"kapha":"primary"}
  dhatu_involvement TEXT,        -- JSON
  severity_level TEXT CHECK(severity_level IN ('mild','moderate','severe','chronic')),
  is_lifestyle_related INTEGER DEFAULT 0,
  prevention_tips TEXT,          -- JSON array
  dietary_recommendations TEXT,  -- JSON
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (json_valid(symptoms) OR symptoms IS NULL),
  CHECK (json_valid(causes) OR causes IS NULL),
  CHECK (json_valid(dosha_involvement) OR dosha_involvement IS NULL),
  CHECK (json_valid(dhatu_involvement) OR dhatu_involvement IS NULL),
  CHECK (json_valid(prevention_tips) OR prevention_tips IS NULL),
  CHECK (json_valid(dietary_recommendations) OR dietary_recommendations IS NULL)
);

CREATE TABLE IF NOT EXISTS disease_synonyms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disease_id INTEGER NOT NULL,
  synonym TEXT NOT NULL,
  language TEXT,
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
);

-- Herb ↔ Disease mapping with evidence
CREATE TABLE IF NOT EXISTS plant_disease_mapping (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  disease_id INTEGER NOT NULL,
  efficacy_level INTEGER CHECK(efficacy_level BETWEEN 1 AND 5),
  evidence_type TEXT CHECK(evidence_type IN ('traditional','clinical','preclinical','anecdotal')),
  mechanism TEXT,
  duration_of_use TEXT,
  contraindications TEXT,
  special_instructions TEXT,
  reference_text TEXT,
  UNIQUE (plant_id, disease_id),
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE,
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
);

-- Preparations/formulations (normalized)
CREATE TABLE IF NOT EXISTS preparations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_en TEXT NOT NULL,
  name_hi TEXT,
  name_mr TEXT,
  classical_name TEXT,
  ayush_system_id INTEGER NOT NULL DEFAULT 1,
  form_type TEXT NOT NULL,        -- decoction, paste, powder, oil, ghrta, lehya, tablet
  category TEXT,                  -- single_herb, compound, patent_medicine
  preparation_steps TEXT NOT NULL, -- JSON array of steps
  equipment_needed TEXT,          -- JSON array
  duration TEXT,
  yield TEXT,
  storage TEXT,
  shelf_life TEXT,
  dosage_json TEXT,               -- JSON: {"adult":"...","child":"..."}
  timing TEXT,                    -- before_food, after_food, empty_stomach (free text ok)
  anupana TEXT,                   -- honey, water, milk, etc.
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (json_valid(preparation_steps)),
  CHECK (json_valid(equipment_needed) OR equipment_needed IS NULL),
  CHECK (json_valid(dosage_json) OR dosage_json IS NULL),
  FOREIGN KEY (ayush_system_id) REFERENCES ayush_system(id) ON DELETE RESTRICT
);

-- Many-to-many: preparation ↔ ingredients (plants/parts/qty)
CREATE TABLE IF NOT EXISTS preparation_ingredients (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  preparation_id INTEGER NOT NULL,
  plant_id INTEGER NOT NULL,
  part TEXT,                      -- leaf, root, seed, etc.
  quantity_value REAL,
  quantity_unit TEXT,             -- g, ml, tsp, etc.
  notes TEXT,
  FOREIGN KEY (preparation_id) REFERENCES preparations(id) ON DELETE CASCADE,
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE RESTRICT
);

-- Many-to-many: preparation ↔ indications (diseases)
CREATE TABLE IF NOT EXISTS preparation_indications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  preparation_id INTEGER NOT NULL,
  disease_id INTEGER NOT NULL,
  strength INTEGER CHECK(strength BETWEEN 1 AND 5),  -- heuristic strength
  evidence_type TEXT CHECK(evidence_type IN ('traditional','clinical','preclinical','anecdotal')),
  notes TEXT,
  FOREIGN KEY (preparation_id) REFERENCES preparations(id) ON DELETE CASCADE,
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE RESTRICT
);

-- Safety
CREATE TABLE IF NOT EXISTS contraindications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  condition TEXT NOT NULL,        -- pregnancy, lactation, hypertension...
  severity TEXT NOT NULL CHECK(severity IN ('absolute','relative','cautionary')),
  details TEXT,
  alternatives TEXT,
  reference TEXT,
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS interactions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  interaction_type TEXT NOT NULL CHECK(interaction_type IN ('drug','herb','food','supplement')),
  interaction_with TEXT NOT NULL,
  effect TEXT NOT NULL,
  severity TEXT NOT NULL CHECK(severity IN ('minor','moderate','major','severe')),
  mechanism TEXT,
  recommendation TEXT,
  reference TEXT,
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);

-- Embeddings (per-language + provenance)
CREATE TABLE IF NOT EXISTS plant_embeddings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  lang TEXT NOT NULL DEFAULT 'multilingual',
  model_name TEXT NOT NULL,
  model_version TEXT,
  model_sha TEXT,
  embedding BLOB NOT NULL,
  embedding_dimension INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (plant_id, lang, model_name, model_version),
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS disease_embeddings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disease_id INTEGER NOT NULL,
  lang TEXT NOT NULL DEFAULT 'multilingual',
  model_name TEXT NOT NULL,
  model_version TEXT,
  model_sha TEXT,
  embedding BLOB NOT NULL,
  embedding_dimension INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (disease_id, lang, model_name, model_version),
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS preparation_embeddings (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  preparation_id INTEGER NOT NULL,
  lang TEXT NOT NULL DEFAULT 'multilingual',
  model_name TEXT NOT NULL,
  model_version TEXT,
  model_sha TEXT,
  embedding BLOB NOT NULL,
  embedding_dimension INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE (preparation_id, lang, model_name, model_version),
  FOREIGN KEY (preparation_id) REFERENCES preparations(id) ON DELETE CASCADE
);

-- Telemetry
CREATE TABLE IF NOT EXISTS conversations (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT NOT NULL,
  user_query TEXT NOT NULL,
  detected_language TEXT,
  intent TEXT,
  entities TEXT,                  -- JSON
  response_text TEXT,
  structured_data TEXT,           -- JSON
  feedback INTEGER,               -- 1, -1, NULL
  feedback_comment TEXT,
  response_time_ms INTEGER,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (json_valid(entities) OR entities IS NULL),
  CHECK (json_valid(structured_data) OR structured_data IS NULL)
);

CREATE TABLE IF NOT EXISTS user_preferences (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id TEXT UNIQUE NOT NULL,
  preferred_language TEXT DEFAULT 'en',
  preferred_system_id INTEGER,    -- FK to ayush_system
  constitution_type TEXT,         -- vata, pitta, kapha, mixed
  bookmarked_plants TEXT,         -- JSON array of plant IDs
  bookmarked_preparations TEXT,   -- JSON array of preparation IDs
  medical_conditions TEXT,        -- JSON
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CHECK (json_valid(bookmarked_plants) OR bookmarked_plants IS NULL),
  CHECK (json_valid(bookmarked_preparations) OR bookmarked_preparations IS NULL),
  CHECK (json_valid(medical_conditions) OR medical_conditions IS NULL),
  FOREIGN KEY (preferred_system_id) REFERENCES ayush_system(id) ON DELETE SET NULL
);

CREATE TRIGGER IF NOT EXISTS trg_user_prefs_updated
AFTER UPDATE ON user_preferences FOR EACH ROW
BEGIN
  UPDATE user_preferences SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Provenance
CREATE TABLE IF NOT EXISTS data_sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  type TEXT,             -- book, research_paper, database, expert_review
  citation TEXT,
  reliability_score INTEGER CHECK(reliability_score BETWEEN 1 AND 5),
  last_verified TIMESTAMP
);

-- Junctions to tie evidence/provenance to entities
CREATE TABLE IF NOT EXISTS plant_sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  source_id INTEGER NOT NULL,
  note TEXT,
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE,
  FOREIGN KEY (source_id) REFERENCES data_sources(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS disease_sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disease_id INTEGER NOT NULL,
  source_id INTEGER NOT NULL,
  note TEXT,
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE,
  FOREIGN KEY (source_id) REFERENCES data_sources(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS preparation_sources (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  preparation_id INTEGER NOT NULL,
  source_id INTEGER NOT NULL,
  note TEXT,
  FOREIGN KEY (preparation_id) REFERENCES preparations(id) ON DELETE CASCADE,
  FOREIGN KEY (source_id) REFERENCES data_sources(id) ON DELETE CASCADE
);

-- ============================================================================
-- FULL-TEXT SEARCH
-- ============================================================================

CREATE VIRTUAL TABLE IF NOT EXISTS plants_fts USING fts5(
  botanical_name, common_name_en, common_name_hi, common_name_mr, description,
  content='plants', content_rowid='id'
);
CREATE VIRTUAL TABLE IF NOT EXISTS diseases_fts USING fts5(
  name_en, name_hi, name_mr, description, symptoms,
  content='diseases', content_rowid='id'
);
CREATE VIRTUAL TABLE IF NOT EXISTS preparations_fts USING fts5(
  name_en, name_hi, name_mr, classical_name, form_type, notes
);

CREATE TRIGGER IF NOT EXISTS trg_plants_fts_ai AFTER INSERT ON plants BEGIN
  INSERT INTO plants_fts(rowid, botanical_name, common_name_en, common_name_hi, common_name_mr, description)
  VALUES (new.id, new.botanical_name, new.common_name_en, new.common_name_hi, new.common_name_mr, new.description);
END;
CREATE TRIGGER IF NOT EXISTS trg_plants_fts_au AFTER UPDATE ON plants BEGIN
  UPDATE plants_fts SET
    botanical_name = new.botanical_name,
    common_name_en = new.common_name_en,
    common_name_hi = new.common_name_hi,
    common_name_mr = new.common_name_mr,
    description = new.description
  WHERE rowid = new.id;
END;
CREATE TRIGGER IF NOT EXISTS trg_plants_fts_ad AFTER DELETE ON plants BEGIN
  DELETE FROM plants_fts WHERE rowid = old.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_diseases_fts_ai AFTER INSERT ON diseases BEGIN
  INSERT INTO diseases_fts(rowid, name_en, name_hi, name_mr, description, symptoms)
  VALUES (new.id, new.name_en, new.name_hi, new.name_mr, new.description, new.symptoms);
END;
CREATE TRIGGER IF NOT EXISTS trg_diseases_fts_au AFTER UPDATE ON diseases BEGIN
  UPDATE diseases_fts SET
    name_en = new.name_en,
    name_hi = new.name_hi,
    name_mr = new.name_mr,
    description = new.description,
    symptoms = new.symptoms
  WHERE rowid = new.id;
END;
CREATE TRIGGER IF NOT EXISTS trg_diseases_fts_ad AFTER DELETE ON diseases BEGIN
  DELETE FROM diseases_fts WHERE rowid = old.id;
END;

CREATE TRIGGER IF NOT EXISTS trg_preps_fts_ai AFTER INSERT ON preparations BEGIN
  INSERT INTO preparations_fts(rowid, name_en, name_hi, name_mr, classical_name, form_type, notes)
  VALUES (new.id, new.name_en, new.name_hi, new.name_mr, new.classical_name, new.form_type, new.notes);
END;
CREATE TRIGGER IF NOT EXISTS trg_preps_fts_au AFTER UPDATE ON preparations BEGIN
  UPDATE preparations_fts SET
    name_en = new.name_en,
    name_hi = new.name_hi,
    name_mr = new.name_mr,
    classical_name = new.classical_name,
    form_type = new.form_type,
    notes = new.notes
  WHERE rowid = new.id;
END;
CREATE TRIGGER IF NOT EXISTS trg_preps_fts_ad AFTER DELETE ON preparations BEGIN
  DELETE FROM preparations_fts WHERE rowid = old.id;
END;

-- ============================================================================
-- COMPATIBILITY VIEW (read-only) FOR "remedy"-style ANSWERS
-- Aggregates plant + disease + top preparation into a single rowset.
-- ============================================================================

CREATE VIEW IF NOT EXISTS remedy_view AS
SELECT
  pdm.disease_id,
  d.name_en AS disease_en,
  p.id AS plant_id,
  p.botanical_name,
  p.common_name_en,
  pdm.efficacy_level,
  pdm.evidence_type,
  pr.id AS preparation_id,
  pr.name_en AS preparation_name,
  pr.form_type,
  pr.dosage_json,
  pr.timing,
  pr.anupana,
  pr.notes
FROM plant_disease_mapping pdm
JOIN plants p ON p.id = pdm.plant_id
JOIN diseases d ON d.id = pdm.disease_id
LEFT JOIN preparation_indications pi ON pi.disease_id = d.id
LEFT JOIN preparations pr ON pr.id = pi.preparation_id;

-- ============================================================================
-- INDEXES
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_plants_botanical ON plants(botanical_name);
CREATE INDEX IF NOT EXISTS idx_plants_system ON plants(ayush_system_id);
CREATE INDEX IF NOT EXISTS idx_diseases_category ON diseases(category);
CREATE INDEX IF NOT EXISTS idx_diseases_severity ON diseases(severity_level);
CREATE INDEX IF NOT EXISTS idx_pdm_disease ON plant_disease_mapping(disease_id, efficacy_level);
CREATE INDEX IF NOT EXISTS idx_pdm_plant ON plant_disease_mapping(plant_id, evidence_type);
CREATE INDEX IF NOT EXISTS idx_media_plant ON media(plant_id);
CREATE INDEX IF NOT EXISTS idx_prep_type ON preparations(form_type, ayush_system_id);
CREATE INDEX IF NOT EXISTS idx_prep_ing_p ON preparation_ingredients(preparation_id);
CREATE INDEX IF NOT EXISTS idx_prep_ing_pl ON preparation_ingredients(plant_id);
CREATE INDEX IF NOT EXISTS idx_prep_ind_d ON preparation_indications(disease_id);
CREATE INDEX IF NOT EXISTS idx_contra_plant ON contraindications(plant_id);
CREATE INDEX IF NOT EXISTS idx_interact_plant ON interactions(plant_id);
CREATE INDEX IF NOT EXISTS idx_conv_session ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_userprefs_session ON user_preferences(session_id);
