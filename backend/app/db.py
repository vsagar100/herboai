from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from pathlib import Path
from app.settings import settings

Path(settings.DB_PATH).parent.mkdir(parents=True, exist_ok=True)
_engine: Engine = create_engine(f"sqlite:///{settings.DB_PATH}", future=True)

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS herbs (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  scientific_name TEXT,
  ayush_system TEXT NOT NULL,
  synonyms TEXT,
  parts_used TEXT,
  uses TEXT,
  phytochemicals TEXT,
  dosage TEXT,
  contraindications TEXT,
  formulations TEXT,
  languages_json TEXT NOT NULL,
  examples TEXT,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
"""

def init_db():
    with _engine.begin() as cx:
        cx.exec_driver_sql(SCHEMA_SQL)

def upsert_herb(h: dict):
    import json
    fields = {
        "id": h["id"],
        "name": h["name"],
        "scientific_name": h.get("scientific_name"),
        "ayush_system": ",".join(h.get("ayush_system", [])),
        "synonyms": ",".join(h.get("synonyms", [])),
        "parts_used": ",".join(h.get("parts_used", [])),
        "uses": h.get("uses", ""),
        "phytochemicals": h.get("phytochemicals", ""),
        "dosage": h.get("dosage", ""),
        "contraindications": h.get("contraindications", ""),
        "formulations": ",".join(h.get("formulations", [])),
        "languages_json": json.dumps(h.get("languages", {}), ensure_ascii=False),
        "examples": "\n".join(h.get("examples", [])),
    }
    sql = text("""
        INSERT INTO herbs(id,name,scientific_name,ayush_system,synonyms,parts_used,uses,phytochemicals,dosage,contraindications,formulations,languages_json,examples)
        VALUES(:id,:name,:scientific_name,:ayush_system,:synonyms,:parts_used,:uses,:phytochemicals,:dosage,:contraindications,:formulations,:languages_json,:examples)
        ON CONFLICT(id) DO UPDATE SET
          name=excluded.name,
          scientific_name=excluded.scientific_name,
          ayush_system=excluded.ayush_system,
          synonyms=excluded.synonyms,
          parts_used=excluded.parts_used,
          uses=excluded.uses,
          phytochemicals=excluded.phytochemicals,
          dosage=excluded.dosage,
          contraindications=excluded.contraindications,
          formulations=excluded.formulations,
          languages_json=excluded.languages_json,
          examples=excluded.examples
    """)
    with _engine.begin() as cx:
        cx.execute(sql, fields)

def fetch_herb(id_: str):
    with _engine.begin() as cx:
        row = cx.execute(text("SELECT * FROM herbs WHERE id=:id"), {"id": id_}).mappings().first()
        return dict(row) if row else None

def list_herbs(limit: int = 50, offset: int = 0):
    with _engine.begin() as cx:
        rows = cx.execute(text("SELECT id,name,scientific_name FROM herbs ORDER BY name LIMIT :l OFFSET :o"), {"l": limit, "o": offset}).mappings().all()
        return [dict(r) for r in rows]

init_db()