from sqlite_vec import serialize_float32
from db import get_db

def upsert_disease_vec(disease_id: int, name_en: str, emb_384: list[float]):
    db = get_db()
    db.execute("""
      INSERT INTO disease_vec(disease_id, name_en, embedding)
      VALUES (?, ?, ?)
      ON CONFLICT(disease_id) DO UPDATE SET
        name_en=excluded.name_en,
        embedding=excluded.embedding
    """, (disease_id, name_en, serialize_float32(emb_384)))
    db.commit()
