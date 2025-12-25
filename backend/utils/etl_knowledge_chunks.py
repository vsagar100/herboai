#!/usr/bin/env python
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

DB_PATH = "../../db/new_herboai.db"   # <-- adjust to your DB file
MODEL_NAME = "all-MiniLM-L6-v2"

def l2_normalize(v: np.ndarray) -> np.ndarray:
    v = v.astype("float32")
    n = np.linalg.norm(v)
    return v if n == 0 else v / n

def main():
    conn = sqlite3.connect(DB_PATH)
    print("conn status : ", conn.getconfig)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    model = SentenceTransformer(MODEL_NAME)
    print("[ETL] Loading chunks without embeddings...")
    rows = cur.execute(
        """
        SELECT id, content
        FROM knowledge_chunks
        WHERE embedding IS NULL OR length(embedding) = 0
        """
    ).fetchall()

    if not rows:
        print("[ETL] No chunks to embed.")
        return

    texts = [r["content"] for r in rows]
    print(f"[ETL] Encoding {len(texts)} chunks...")
    embs = model.encode(texts, batch_size=32, show_progress_bar=True)

    for row, emb in zip(rows, embs):
        vec = l2_normalize(np.array(emb, dtype="float32"))
        blob = vec.tobytes()  # <- direct BLOB, no sqlite-vec / vec0
        cur.execute(
            "UPDATE knowledge_chunks SET embedding = ? WHERE id = ?",
            (blob, row["id"]),
        )

    conn.commit()
    print("[ETL] Done.")

if __name__ == "__main__":
    main()
