import json
import math
import os
from typing import Dict, List, Sequence

from sentence_transformers import SentenceTransformer
from sqlite_vec import serialize_float32

from db import get_db_standalone

_MODEL = None
_MODEL_NAME = os.getenv("SENTENCE_MODEL_NAME", "all-MiniLM-L6-v2")
_MODEL_CACHE = os.getenv("SENTENCE_MODEL_CACHE")


def _get_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        if _MODEL_CACHE:
            print(f"[VectorIndex] Loading {_MODEL_NAME} with cache at {_MODEL_CACHE}")
            _MODEL = SentenceTransformer(_MODEL_NAME, cache_folder=_MODEL_CACHE)
        else:
            print(f"[VectorIndex] Loading {_MODEL_NAME} (default cache)")
            _MODEL = SentenceTransformer(_MODEL_NAME)
    return _MODEL


def _embed(text: str) -> bytes:
    vec = _get_model().encode(text).astype("float32").tolist()
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    vec = [x / norm for x in vec]
    return serialize_float32(vec)


def _flatten_json(value) -> str:
    if not value:
        return ""
    data = value
    if isinstance(value, str):
        try:
            data = json.loads(value)
        except Exception:
            return value
    if isinstance(data, list):
        return " ".join(str(x) for x in data if x)
    if isinstance(data, dict):
        return " ".join(f"{k}: {v}" for k, v in data.items() if v)
    return str(data)


def _row_to_dict(row) -> Dict:
    if hasattr(row, "keys"):
        return {key: row[key] for key in row.keys()}
    return dict(row)


def _table_columns(db, table: str) -> List[str]:
    cur = db.execute(f"PRAGMA table_info({table})")
    rows = cur.fetchall()
    return [row[1] for row in rows]


def _select_rows(db, table: str, required: Sequence[str], optional: Sequence[str]):
    columns = _table_columns(db, table)
    missing = [col for col in required if col not in columns]
    if missing:
        raise RuntimeError(f"{table} missing required columns: {missing}")
    select_list = list(required) + [col for col in optional if col in columns]
    cols_sql = ", ".join(select_list)
    sql = f"SELECT {cols_sql} FROM {table}"
    return db.execute(sql).fetchall()


def _needs_rebuild(db, vec_table: str, source_table: str) -> bool:
    try:
        vec_total = db.execute(f"SELECT COUNT(*) FROM {vec_table}").fetchone()[0]
    except Exception:
        return True
    try:
        total = db.execute(f"SELECT COUNT(*) FROM {source_table}").fetchone()[0]
    except Exception:
        return False
    return vec_total < total


def _rebuild_disease_index(db) -> int:
    rows = _select_rows(
        db,
        "diseases",
        required=("id", "name_en"),
        optional=(
            "description",
            "symptoms",
            "causes",
            "dosha_involvement",
            "prevention_tips",
            "dietary_recommendations",
        ),
    )
    db.execute("DELETE FROM disease_vec")
    inserted = 0
    for row in rows:
        data = _row_to_dict(row)
        text = " ".join(
            part
            for part in [
                data.get("name_en") or "",
                data.get("description") or "",
                _flatten_json(data.get("symptoms")),
                _flatten_json(data.get("causes")),
                _flatten_json(data.get("dosha_involvement")),
                _flatten_json(data.get("prevention_tips")),
                _flatten_json(data.get("dietary_recommendations")),
            ]
            if part
        ).strip()
        if not text:
            continue
        db.execute(
            """
            INSERT OR REPLACE INTO disease_vec(disease_id, name_en, embedding)
            VALUES (?, ?, ?)
            """,
            (data["id"], data.get("name_en") or "", _embed(text)),
        )
        inserted += 1
    db.commit()
    return inserted


def _rebuild_plant_index(db) -> int:
    rows = _select_rows(
        db,
        "plants",
        required=("id", "common_name_en", "botanical_name"),
        optional=("description", "therapeutic_actions", "rasa", "guna", "dosha_effect"),
    )
    db.execute("DELETE FROM plant_vec")
    inserted = 0
    for row in rows:
        data = _row_to_dict(row)
        text = " ".join(
            part
            for part in [
                data.get("common_name_en") or "",
                data.get("botanical_name") or "",
                data.get("description") or "",
                _flatten_json(data.get("therapeutic_actions")),
                _flatten_json(data.get("rasa")),
                _flatten_json(data.get("guna")),
                _flatten_json(data.get("dosha_effect")),
            ]
            if part
        ).strip()
        if not text:
            continue
        display_name = data.get("common_name_en") or data.get("botanical_name") or ""
        db.execute(
            """
            INSERT OR REPLACE INTO plant_vec(plant_id, name_en, embedding)
            VALUES (?, ?, ?)
            """,
            (data["id"], display_name, _embed(text)),
        )
        inserted += 1
    db.commit()
    return inserted


def _rebuild_prep_index(db) -> int:
    rows = _select_rows(
        db,
        "preparations",
        required=("id", "name_en"),
        optional=("classical_name", "form_type", "preparation_steps", "notes", "description"),
    )
    db.execute("DELETE FROM prep_vec")
    inserted = 0
    for row in rows:
        data = _row_to_dict(row)
        text = " ".join(
            part
            for part in [
                data.get("name_en") or "",
                data.get("classical_name") or "",
                data.get("form_type") or "",
                data.get("description") or "",
                data.get("notes") or "",
                _flatten_json(data.get("preparation_steps")),
            ]
            if part
        ).strip()
        if not text:
            continue
        db.execute(
            """
            INSERT OR REPLACE INTO prep_vec(preparation_id, name_en, embedding)
            VALUES (?, ?, ?)
            """,
            (data["id"], data.get("name_en") or data.get("classical_name") or "", _embed(text)),
        )
        inserted += 1
    db.commit()
    return inserted


def ensure_vector_indexes(force_full: bool = False) -> Dict[str, int]:
    """
    Ensure that disease_vec, plant_vec, and prep_vec exist and contain
    embeddings aligned with the master tables.

    Returns:
      - diseases/plants/preparations: total rows currently present in vec tables
      - diseases_rebuilt/plants_rebuilt/preparations_rebuilt: rows rebuilt this run
    """
    print("[VectorIndex] Starting vector index check...")
    db = get_db_standalone()
    try:
        rebuilt = {"diseases": 0, "plants": 0, "preparations": 0}

        if force_full or _needs_rebuild(db, "disease_vec", "diseases"):
            rebuilt["diseases"] = _rebuild_disease_index(db)
        if force_full or _needs_rebuild(db, "plant_vec", "plants"):
            rebuilt["plants"] = _rebuild_plant_index(db)
        if force_full or _needs_rebuild(db, "prep_vec", "preparations"):
            rebuilt["preparations"] = _rebuild_prep_index(db)

        # True readiness = counts that exist now
        totals = {
            "diseases": db.execute("SELECT COUNT(*) FROM disease_vec").fetchone()[0],
            "plants": db.execute("SELECT COUNT(*) FROM plant_vec").fetchone()[0],
            "preparations": db.execute("SELECT COUNT(*) FROM prep_vec").fetchone()[0],
            "diseases_rebuilt": rebuilt["diseases"],
            "plants_rebuilt": rebuilt["plants"],
            "preparations_rebuilt": rebuilt["preparations"],
        }
        return totals
    finally:
        db.close()

def rebuild_all_indexes() -> Dict[str, int]:
    """
    Force a full rebuild, used by maintenance tasks or manual API endpoints.
    """
    return ensure_vector_indexes(force_full=True)
