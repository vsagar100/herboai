CREATE TABLE IF NOT EXISTS "plants" (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  botanical_name TEXT NOT NULL UNIQUE,
  common_name_en TEXT,
  common_name_hi TEXT,
  common_name_mr TEXT,
  sanskrit_name TEXT,
  family TEXT,
  description TEXT,
  habitat TEXT,
  parts_used TEXT,
  rasa TEXT,
  virya TEXT,
  vipaka TEXT,
  guna TEXT,
  dosha_effect TEXT,
  prabhava TEXT,
  active_compounds TEXT,
  therapeutic_actions TEXT,
  classical_references TEXT,
  is_endangered INTEGER DEFAULT 0,
  cultivation_status TEXT,
  image_hero TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  ayush_system TEXT,
  CHECK (json_valid(parts_used) OR parts_used IS NULL),
  CHECK (json_valid(rasa) OR rasa IS NULL),
  CHECK (json_valid(guna) OR guna IS NULL),
  CHECK (json_valid(dosha_effect) OR dosha_effect IS NULL),
 -- CHECK (json_valid(active_compounds) OR active_compounds IS NULL),
 -- CHECK (json_valid(classical_references) OR classical_references IS NULL),
  CHECK (json_valid(therapeutic_actions) OR therapeutic_actions IS NULL)
);
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE plant_synonyms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  synonym TEXT NOT NULL,
  language TEXT,                 -- "en","hi","mr","regional"
  kind TEXT,                     -- "common_name","regional_name","trade_name"
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);
CREATE TABLE diseases (
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
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP,
  CHECK (json_valid(symptoms) OR symptoms IS NULL),
  CHECK (json_valid(causes) OR causes IS NULL),
  CHECK (json_valid(dosha_involvement) OR dosha_involvement IS NULL),
  CHECK (json_valid(dhatu_involvement) OR dhatu_involvement IS NULL),
  CHECK (json_valid(prevention_tips) OR prevention_tips IS NULL),
  CHECK (json_valid(dietary_recommendations) OR dietary_recommendations IS NULL)
);
CREATE TABLE disease_synonyms (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  disease_id INTEGER NOT NULL,
  synonym TEXT NOT NULL,
  language TEXT,
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE CASCADE
);
CREATE TABLE plant_disease_mapping (
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
CREATE TABLE preparation_ingredients (
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
CREATE TABLE preparation_indications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  preparation_id INTEGER NOT NULL,
  disease_id INTEGER NOT NULL,
  strength INTEGER CHECK(strength BETWEEN 1 AND 5),  -- heuristic strength
  evidence_type TEXT CHECK(evidence_type IN ('traditional','clinical','preclinical','anecdotal')),
  notes TEXT,
  FOREIGN KEY (preparation_id) REFERENCES preparations(id) ON DELETE CASCADE,
  FOREIGN KEY (disease_id) REFERENCES diseases(id) ON DELETE RESTRICT
);
CREATE TABLE contraindications (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  plant_id INTEGER NOT NULL,
  condition TEXT NOT NULL,        -- pregnancy, lactation, hypertension...
  severity TEXT NOT NULL CHECK(severity IN ('absolute','relative','cautionary')),
  details TEXT,
  alternatives TEXT,
  reference TEXT,
  FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE CASCADE
);
CREATE TABLE interactions (
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
CREATE TABLE plant_embeddings (
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
CREATE TABLE disease_embeddings (
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
CREATE TABLE preparation_embeddings (
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
CREATE TABLE conversations (
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
CREATE VIRTUAL TABLE plants_fts USING fts5(
  botanical_name, common_name_en, common_name_hi, common_name_mr, description,
  content='plants', content_rowid='id'
)
/* plants_fts(botanical_name,common_name_en,common_name_hi,common_name_mr,description) */;
CREATE TABLE IF NOT EXISTS 'plants_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
CREATE TABLE IF NOT EXISTS 'plants_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS 'plants_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
CREATE TABLE IF NOT EXISTS 'plants_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
CREATE VIRTUAL TABLE diseases_fts USING fts5(
  name_en, name_hi, name_mr, description, symptoms,
  content='diseases', content_rowid='id'
)
/* diseases_fts(name_en,name_hi,name_mr,description,symptoms) */;
CREATE TABLE IF NOT EXISTS 'diseases_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
CREATE TABLE IF NOT EXISTS 'diseases_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS 'diseases_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
CREATE TABLE IF NOT EXISTS 'diseases_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
CREATE VIRTUAL TABLE preparations_fts USING fts5(
  name_en, name_hi, name_mr, classical_name, form_type, notes
)
/* preparations_fts(name_en,name_hi,name_mr,classical_name,form_type,notes) */;
CREATE TABLE IF NOT EXISTS 'preparations_fts_data'(id INTEGER PRIMARY KEY, block BLOB);
CREATE TABLE IF NOT EXISTS 'preparations_fts_idx'(segid, term, pgno, PRIMARY KEY(segid, term)) WITHOUT ROWID;
CREATE TABLE IF NOT EXISTS 'preparations_fts_content'(id INTEGER PRIMARY KEY, c0, c1, c2, c3, c4, c5);
CREATE TABLE IF NOT EXISTS 'preparations_fts_docsize'(id INTEGER PRIMARY KEY, sz BLOB);
CREATE TABLE IF NOT EXISTS 'preparations_fts_config'(k PRIMARY KEY, v) WITHOUT ROWID;
CREATE TRIGGER trg_diseases_fts_ai AFTER INSERT ON diseases BEGIN
  INSERT INTO diseases_fts(rowid, name_en, name_hi, name_mr, description, symptoms)
  VALUES (new.id, new.name_en, new.name_hi, new.name_mr, new.description, new.symptoms);
END;
CREATE TRIGGER trg_diseases_fts_au AFTER UPDATE ON diseases BEGIN
  UPDATE diseases_fts SET
    name_en = new.name_en,
    name_hi = new.name_hi,
    name_mr = new.name_mr,
    description = new.description,
    symptoms = new.symptoms
  WHERE rowid = new.id;
END;
CREATE TRIGGER trg_diseases_fts_ad AFTER DELETE ON diseases BEGIN
  DELETE FROM diseases_fts WHERE rowid = old.id;
END;
CREATE INDEX idx_diseases_category ON diseases(category);
CREATE INDEX idx_diseases_severity ON diseases(severity_level);
CREATE INDEX idx_pdm_disease ON plant_disease_mapping(disease_id, efficacy_level);
CREATE INDEX idx_pdm_plant ON plant_disease_mapping(plant_id, evidence_type);
CREATE INDEX idx_prep_ing_p ON preparation_ingredients(preparation_id);
CREATE INDEX idx_prep_ing_pl ON preparation_ingredients(plant_id);
CREATE INDEX idx_prep_ind_d ON preparation_indications(disease_id);
CREATE INDEX idx_contra_plant ON contraindications(plant_id);
CREATE INDEX idx_interact_plant ON interactions(plant_id);
CREATE INDEX idx_conv_session ON conversations(session_id);
CREATE TABLE schema_version (
  version TEXT PRIMARY KEY,
  applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  description TEXT
);
CREATE TRIGGER trg_diseases_updated
AFTER UPDATE ON diseases FOR EACH ROW
BEGIN
  UPDATE diseases SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
CREATE INDEX idx_plant_synonyms_text
  ON plant_synonyms(synonym, language);
CREATE INDEX idx_disease_synonyms_text
  ON disease_synonyms(synonym, language);
CREATE TABLE admin_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_active INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_admin_users_email ON admin_users(email);
CREATE TABLE IF NOT EXISTS "vec_health_demo_info" (key text primary key, value any);
CREATE TABLE IF NOT EXISTS "vec_health_demo_chunks"(chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,size INTEGER NOT NULL,validity BLOB NOT NULL,rowids BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "vec_health_demo_rowids"(rowid INTEGER PRIMARY KEY AUTOINCREMENT,id,chunk_id INTEGER,chunk_offset INTEGER);
CREATE TABLE IF NOT EXISTS "vec_health_demo_vector_chunks00"(rowid PRIMARY KEY,vectors BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "vec_health_demo_metadatachunks00"(rowid PRIMARY KEY, data BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "vec_health_demo_metadatatext00"(rowid PRIMARY KEY, data TEXT);
CREATE TABLE IF NOT EXISTS "disease_vec_info" (key text primary key, value any);
CREATE TABLE IF NOT EXISTS "disease_vec_chunks"(chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,size INTEGER NOT NULL,validity BLOB NOT NULL,rowids BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "disease_vec_rowids"(rowid INTEGER PRIMARY KEY AUTOINCREMENT,id,chunk_id INTEGER,chunk_offset INTEGER);
CREATE TABLE IF NOT EXISTS "disease_vec_vector_chunks00"(rowid PRIMARY KEY,vectors BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "disease_vec_metadatachunks00"(rowid PRIMARY KEY, data BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "disease_vec_metadatatext00"(rowid PRIMARY KEY, data TEXT);
CREATE TABLE IF NOT EXISTS "plant_vec_info" (key text primary key, value any);
CREATE TABLE IF NOT EXISTS "plant_vec_chunks"(chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,size INTEGER NOT NULL,validity BLOB NOT NULL,rowids BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "plant_vec_rowids"(rowid INTEGER PRIMARY KEY AUTOINCREMENT,id,chunk_id INTEGER,chunk_offset INTEGER);
CREATE TABLE IF NOT EXISTS "plant_vec_vector_chunks00"(rowid PRIMARY KEY,vectors BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "plant_vec_metadatachunks00"(rowid PRIMARY KEY, data BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "plant_vec_metadatatext00"(rowid PRIMARY KEY, data TEXT);
CREATE TABLE IF NOT EXISTS "prep_vec_info" (key text primary key, value any);
CREATE TABLE IF NOT EXISTS "prep_vec_chunks"(chunk_id INTEGER PRIMARY KEY AUTOINCREMENT,size INTEGER NOT NULL,validity BLOB NOT NULL,rowids BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "prep_vec_rowids"(rowid INTEGER PRIMARY KEY AUTOINCREMENT,id,chunk_id INTEGER,chunk_offset INTEGER);
CREATE TABLE IF NOT EXISTS "prep_vec_vector_chunks00"(rowid PRIMARY KEY,vectors BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "prep_vec_metadatachunks00"(rowid PRIMARY KEY, data BLOB NOT NULL);
CREATE TABLE IF NOT EXISTS "prep_vec_metadatatext00"(rowid PRIMARY KEY, data TEXT);
CREATE TABLE IF NOT EXISTS "preparations" (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name_en TEXT NOT NULL,
  name_hi TEXT,
  name_mr TEXT,
  classical_name TEXT,
  form_type TEXT NOT NULL,
  category TEXT,
  preparation_steps TEXT NOT NULL,
  equipment_needed TEXT,
  duration TEXT,
  yield TEXT,
  storage TEXT,
  shelf_life TEXT,
  dosage_json TEXT,
  timing TEXT,
  anupana TEXT,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP,
  ayush_system TEXT
, plant_id INTEGER NOT NULL REFERENCES plants(id) ON DELETE RESTRICT);
CREATE TRIGGER trg_plants_updated
AFTER UPDATE ON plants FOR EACH ROW
BEGIN
  UPDATE plants SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
CREATE TRIGGER trg_plants_fts_ai AFTER INSERT ON plants BEGIN
  INSERT INTO plants_fts(rowid, botanical_name, common_name_en, common_name_hi, common_name_mr, description)
  VALUES (new.id, new.botanical_name, new.common_name_en, new.common_name_hi, new.common_name_mr, new.description);
END;
CREATE TRIGGER trg_plants_fts_au AFTER UPDATE ON plants BEGIN
  UPDATE plants_fts SET
    botanical_name = new.botanical_name,
    common_name_en = new.common_name_en,
    common_name_hi = new.common_name_hi,
    common_name_mr = new.common_name_mr,
    description = new.description
  WHERE rowid = new.id;
END;
CREATE TRIGGER trg_plants_fts_ad AFTER DELETE ON plants BEGIN
  DELETE FROM plants_fts WHERE rowid = old.id;
END;
CREATE TRIGGER trg_preparations_updated
AFTER UPDATE ON preparations FOR EACH ROW
BEGIN
  UPDATE preparations SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
CREATE TRIGGER trg_preps_fts_ai AFTER INSERT ON preparations BEGIN
  INSERT INTO preparations_fts(rowid, name_en, name_hi, name_mr, classical_name, form_type, notes)
  VALUES (new.id, new.name_en, new.name_hi, new.name_mr, new.classical_name, new.form_type, new.notes);
END;
CREATE TRIGGER trg_preps_fts_au AFTER UPDATE ON preparations BEGIN
  UPDATE preparations_fts SET
    name_en = new.name_en,
    name_hi = new.name_hi,
    name_mr = new.name_mr,
    classical_name = new.classical_name,
    form_type = new.form_type,
    notes = new.notes
  WHERE rowid = new.id;
END;
CREATE TRIGGER trg_preps_fts_ad AFTER DELETE ON preparations BEGIN
  DELETE FROM preparations_fts WHERE rowid = old.id;
END;
CREATE VIEW remedy_view AS
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
LEFT JOIN preparations pr ON pr.id = pi.preparation_id
/* remedy_view(disease_id,disease_en,plant_id,botanical_name,common_name_en,efficacy_level,evidence_type,preparation_id,preparation_name,form_type,dosage_json,timing,anupana,notes) */;
