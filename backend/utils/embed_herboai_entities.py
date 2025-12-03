#!/usr/bin/env python
"""
HerboAI embedding ETL for plants, diseases, preparations.

- Uses SENTENCE_MODEL_NAME env (default: all-MiniLM-L6-v2)
- Writes to:
    plant_embeddings
    disease_embeddings
    preparation_embeddings

Usage examples:

    # Basic run, only missing embeddings
    python embed_herboai_entities.py --db new_herboai/db/new_herboai.db

    # Force rebuild all plant embeddings
    python embed_herboai_entities.py --db new_herboai/db/new_herboai.db --force-plants

    # Only diseases
    python embed_herboai_entities.py --db new_herboai/db/new_herboai.db --only diseases
"""

import os
import sys
import argparse
import sqlite3
from typing import List, Dict, Any, Iterable, Tuple, Set
from services.response_builder import (
    build_plant_knowledge_snippet,
    build_disease_knowledge_snippet,
)


import numpy as np
from sentence_transformers import SentenceTransformer


DEFAULT_MODEL_NAME = os.getenv("SENTENCE_MODEL_NAME", "all-MiniLM-L6-v2")
DEFAULT_LANG = os.getenv("EMBED_LANG", "multilingual")
DEFAULT_MODEL_VERSION = os.getenv("SENTENCE_MODEL_VERSION", "v1")
DEFAULT_MODEL_SHA = os.getenv("SENTENCE_MODEL_SHA", "na")



# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def connect_db(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def chunked(iterable: Iterable[Any], size: int) -> Iterable[List[Any]]:
    """Yield items from iterable in chunks of given size."""
    batch: List[Any] = []
    for item in iterable:
        batch.append(item)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch


# ---------------------------------------------------------------------------
# Text builders
# ---------------------------------------------------------------------------

def build_plant_embedding_text(row: sqlite3.Row) -> str:
    """
    Build embedding text for a plant row by mapping DB row -> plant dict
    and delegating to response_builder.build_plant_knowledge_snippet.
    """
    plant = {
        "common_name_en": row["common_name_en"],
        "common_name": row["common_name_en"],  # fallback alias
        "botanical_name": row["botanical_name"],
        "description": row["description"],
        "parts_used": row["parts_used"],
        "therapeutic_actions": row["therapeutic_actions"],
        "rasa": row["rasa"],
        "virya": row["virya"],
        "vipaka": row["vipaka"],
        "guna": row["guna"],
        "dosha_effect": row["dosha_effect"],
        # you could also pass ayush_system if later you extend builder
        # "ayush_system": row["ayush_system"],
    }
    return build_plant_knowledge_snippet(plant)

def build_disease_embedding_text(row: sqlite3.Row) -> str:
    """
    Build embedding text for a disease row via response_builder.
    """
    disease = {
        "name_en": row["name_en"],
        "name_hi": row["name_hi"],
        "name_mr": row["name_mr"],
        "category": row["category"],
        "ayurvedic_name": row["ayurvedic_name"],
        "unani_name": row["unani_name"],
        "siddha_name": row["siddha_name"],
        "description": row["description"],
        "symptoms": row["symptoms"],
        "causes": row["causes"],
        "dosha_involvement": row["dosha_involvement"],
        "dhatu_involvement": row["dhatu_involvement"],
        "severity_level": row["severity_level"],
        "is_lifestyle_related": row["is_lifestyle_related"],
        "prevention_tips": row["prevention_tips"],
        "dietary_recommendations": row["dietary_recommendations"],
    }
    return build_disease_knowledge_snippet(disease)

def build_preparation_embedding_text(row: sqlite3.Row) -> str:
    """
    Build embedding text for a preparation.
    We do not know your exact schema, so we concatenate all non-technical columns
    except 'id' into one descriptive string. You can refine this later.
    """
    ignore_cols = {"id", "created_at", "updated_at"}
    parts = []
    for key in row.keys():
        if key in ignore_cols:
            continue
        value = row[key]
        if value is None:
            continue
        text = str(value).strip()
        if not text:
            continue
        # Make a simple "Label: value" line
        pretty_label = key.replace("_", " ").capitalize()
        parts.append(f"{pretty_label}: {text}")
    return " ".join(parts)


# ---------------------------------------------------------------------------
# Existing embeddings / upsert logic
# ---------------------------------------------------------------------------

def get_existing_entity_ids(
    conn: sqlite3.Connection,
    table_name: str,
    id_column: str,
    lang: str,
    model_name: str,
    model_version: str,
) -> Set[int]:
    """
    For a given embeddings table, get all entity IDs that already have
    an embedding for (lang, model_name, model_version).
    """
    sql = f"""
        SELECT {id_column}
        FROM {table_name}
        WHERE lang = ?
          AND model_name = ?
          AND model_version = ?
    """
    cur = conn.execute(sql, (lang, model_name, model_version))
    return {int(row[id_column]) for row in cur.fetchall()}


def upsert_plant_embeddings(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    lang: str,
    model_name: str,
    model_version: str,
    model_sha: str,
    force: bool = False,
    batch_size: int = 64,
) -> None:
    print("==> Processing plant embeddings")
    cur = conn.execute("SELECT * FROM plants ORDER BY id ASC")
    plant_rows = cur.fetchall()

    if not plant_rows:
        print("No plants found, skipping.")
        return

    if force:
        existing_ids: Set[int] = set()
        print("Force mode ON: existing plant embeddings will be overwritten via UPSERT.")
    else:
        existing_ids = get_existing_entity_ids(
            conn,
            table_name="plant_embeddings",
            id_column="plant_id",
            lang=lang,
            model_name=model_name,
            model_version=model_version,
        )
        print(f"Found {len(existing_ids)} plants already embedded for this model/lang.")

    to_process: List[sqlite3.Row] = [
        r for r in plant_rows if force or (int(r["id"]) not in existing_ids)
    ]
    print(f"Plants to embed: {len(to_process)}")

    if not to_process:
        return

    dim = model.get_sentence_embedding_dimension()

    upsert_sql = """
        INSERT INTO plant_embeddings (
            plant_id, lang, model_name, model_version, model_sha,
            embedding, embedding_dimension
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(plant_id, lang, model_name, model_version) DO UPDATE SET
            embedding = excluded.embedding,
            embedding_dimension = excluded.embedding_dimension,
            created_at = CURRENT_TIMESTAMP
    """

    for batch in chunked(to_process, batch_size):
        ids = [int(r["id"]) for r in batch]
        texts = [build_plant_embedding_text(r) for r in batch]

        embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        with conn:
            for plant_id, vec in zip(ids, embeddings):
                vec = np.asarray(vec, dtype=np.float32)
                blob = sqlite3.Binary(vec.tobytes())
                conn.execute(
                    upsert_sql,
                    (
                        plant_id,
                        lang,
                        model_name,
                        model_version,
                        model_sha,
                        blob,
                        int(dim),
                    ),
                )

        print(f"  Embedded plants {ids[0]}–{ids[-1]}")

    print("Plant embeddings done.\n")


def upsert_disease_embeddings(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    lang: str,
    model_name: str,
    model_version: str,
    model_sha: str,
    force: bool = False,
    batch_size: int = 64,
) -> None:
    print("==> Processing disease embeddings")
    cur = conn.execute("SELECT * FROM diseases ORDER BY id ASC")
    disease_rows = cur.fetchall()

    if not disease_rows:
        print("No diseases found, skipping.")
        return

    if force:
        existing_ids: Set[int] = set()
        print("Force mode ON: existing disease embeddings will be overwritten via UPSERT.")
    else:
        existing_ids = get_existing_entity_ids(
            conn,
            table_name="disease_embeddings",
            id_column="disease_id",
            lang=lang,
            model_name=model_name,
            model_version=model_version,
        )
        print(f"Found {len(existing_ids)} diseases already embedded for this model/lang.")

    to_process: List[sqlite3.Row] = [
        r for r in disease_rows if force or (int(r["id"]) not in existing_ids)
    ]
    print(f"Diseases to embed: {len(to_process)}")

    if not to_process:
        return

    dim = model.get_sentence_embedding_dimension()

    upsert_sql = """
        INSERT INTO disease_embeddings (
            disease_id, lang, model_name, model_version, model_sha,
            embedding, embedding_dimension
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(disease_id, lang, model_name, model_version) DO UPDATE SET
            embedding = excluded.embedding,
            embedding_dimension = excluded.embedding_dimension,
            created_at = CURRENT_TIMESTAMP
    """

    for batch in chunked(to_process, batch_size):
        ids = [int(r["id"]) for r in batch]
        texts = [build_disease_embedding_text(r) for r in batch]

        embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        with conn:
            for disease_id, vec in zip(ids, embeddings):
                vec = np.asarray(vec, dtype=np.float32)
                blob = sqlite3.Binary(vec.tobytes())
                conn.execute(
                    upsert_sql,
                    (
                        disease_id,
                        lang,
                        model_name,
                        model_version,
                        model_sha,
                        blob,
                        int(dim),
                    ),
                )

        print(f"  Embedded diseases {ids[0]}–{ids[-1]}")

    print("Disease embeddings done.\n")


def upsert_preparation_embeddings(
    conn: sqlite3.Connection,
    model: SentenceTransformer,
    lang: str,
    model_name: str,
    model_version: str,
    model_sha: str,
    force: bool = False,
    batch_size: int = 64,
) -> None:
    print("==> Processing preparation embeddings")
    # If table does not exist, skip gracefully
    try:
        cur = conn.execute("SELECT * FROM preparations ORDER BY id ASC")
    except sqlite3.OperationalError as e:
        print(f"preparations table not found, skipping. ({e})")
        return

    prep_rows = cur.fetchall()
    if not prep_rows:
        print("No preparations found, skipping.")
        return

    if force:
        existing_ids: Set[int] = set()
        print("Force mode ON: existing preparation embeddings will be overwritten via UPSERT.")
    else:
        existing_ids = get_existing_entity_ids(
            conn,
            table_name="preparation_embeddings",
            id_column="preparation_id",
            lang=lang,
            model_name=model_name,
            model_version=model_version,
        )
        print(f"Found {len(existing_ids)} preparations already embedded for this model/lang.")

    to_process: List[sqlite3.Row] = [
        r for r in prep_rows if force or (int(r["id"]) not in existing_ids)
    ]
    print(f"Preparations to embed: {len(to_process)}")

    if not to_process:
        return

    dim = model.get_sentence_embedding_dimension()

    upsert_sql = """
        INSERT INTO preparation_embeddings (
            preparation_id, lang, model_name, model_version, model_sha,
            embedding, embedding_dimension
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(preparation_id, lang, model_name, model_version) DO UPDATE SET
            embedding = excluded.embedding,
            embedding_dimension = excluded.embedding_dimension,
            created_at = CURRENT_TIMESTAMP
    """

    for batch in chunked(to_process, batch_size):
        ids = [int(r["id"]) for r in batch]
        texts = [build_preparation_embedding_text(r) for r in batch]

        embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        if embeddings.ndim == 1:
            embeddings = embeddings.reshape(1, -1)

        with conn:
            for prep_id, vec in zip(ids, embeddings):
                vec = np.asarray(vec, dtype=np.float32)
                blob = sqlite3.Binary(vec.tobytes())
                conn.execute(
                    upsert_sql,
                    (
                        prep_id,
                        lang,
                        model_name,
                        model_version,
                        model_sha,
                        blob,
                        int(dim),
                    ),
                )

        print(f"  Embedded preparations {ids[0]}–{ids[-1]}")

    print("Preparation embeddings done.\n")


# ---------------------------------------------------------------------------
# CLI / main
# ---------------------------------------------------------------------------

def parse_args(argv: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="HerboAI embedding ETL for plants/diseases/preparations.")
    parser.add_argument(
        "--db",
        required=True,
        help="Path to SQLite database file (e.g. new_herboai/db/new_herboai.db)",
    )
    parser.add_argument(
        "--lang",
        default=DEFAULT_LANG,
        help=f"Language tag to store in embeddings.lang (default: {DEFAULT_LANG})",
    )
    parser.add_argument(
        "--model-name",
        default=DEFAULT_MODEL_NAME,
        help=f"SentenceTransformer model name (default: {DEFAULT_MODEL_NAME})",
    )
    parser.add_argument(
        "--model-version",
        default=DEFAULT_MODEL_VERSION,
        help=f"Model version string stored in DB (default: {DEFAULT_MODEL_VERSION})",
    )
    parser.add_argument(
        "--model-sha",
        default=DEFAULT_MODEL_SHA,
        help=f"Model SHA or build identifier (default: {DEFAULT_MODEL_SHA})",
    )

    parser.add_argument(
        "--only",
        choices=["all", "plants", "diseases", "preparations"],
        default="all",
        help="Limit embedding to only a specific entity type (default: all).",
    )

    parser.add_argument(
        "--force-plants",
        action="store_true",
        help="Rebuild plant embeddings even if rows already exist (UPSERT).",
    )
    parser.add_argument(
        "--force-diseases",
        action="store_true",
        help="Rebuild disease embeddings even if rows already exist (UPSERT).",
    )
    parser.add_argument(
        "--force-preparations",
        action="store_true",
        help="Rebuild preparation embeddings even if rows already exist (UPSERT).",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
        help="Batch size for embedding calls (default: 64).",
    )
    return parser.parse_args(argv)


def main(argv: List[str]) -> None:
    args = parse_args(argv)

    print(f"Using DB: {args.db}")
    print(f"Model: {args.model_name} (version={args.model_version}, sha={args.model_sha})")
    print(f"Lang tag: {args.lang}")
    print(f"Scope: {args.only}")

    conn = connect_db(args.db)

    print("Loading sentence-transformer model...")
    model = SentenceTransformer(args.model_name)
    dim = model.get_sentence_embedding_dimension()
    print(f"Model loaded. Embedding dimension: {dim}")

    # Plants
    if args.only in ("all", "plants"):
        upsert_plant_embeddings(
            conn,
            model,
            lang=args.lang,
            model_name=args.model_name,
            model_version=args.model_version,
            model_sha=args.model_sha,
            force=args.force_plants,
            batch_size=args.batch_size,
        )

    # Diseases
    if args.only in ("all", "diseases"):
        upsert_disease_embeddings(
            conn,
            model,
            lang=args.lang,
            model_name=args.model_name,
            model_version=args.model_version,
            model_sha=args.model_sha,
            force=args.force_diseases,
            batch_size=args.batch_size,
        )

    # Preparations
    if args.only in ("all", "preparations"):
        upsert_preparation_embeddings(
            conn,
            model,
            lang=args.lang,
            model_name=args.model_name,
            model_version=args.model_version,
            model_sha=args.model_sha,
            force=args.force_preparations,
            batch_size=args.batch_size,
        )

    conn.close()
    print("All done.")


if __name__ == "__main__":
    main(sys.argv[1:])
