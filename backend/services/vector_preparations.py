# db/vector_preparations.py

from typing import List, Dict, Any

def search_similar_preparations(conn, query_embedding: bytes, top_k: int = 8) -> List[Dict[str, Any]]:
    """
    Semantic search over preparation_embeddings using sqlite-vec.
    Returns hydrated preparations in ranked order.
    """
    rows = conn.execute(
        """
        SELECT 
            pe.preparation_id,
            vec_distance_L2(pe.embedding, :q) AS distance
        FROM preparation_embeddings pe
        ORDER BY distance ASC
        LIMIT :k;
        """,
        {"q": query_embedding, "k": top_k},
    ).fetchall()

    if not rows:
        return []

    prep_ids = [r["preparation_id"] for r in rows]
    placeholders = ",".join("?" for _ in prep_ids)

    # Hydrate preparations + join main herb for context (optional)
    preps_sql = f"""
    SELECT 
        p.id,
        p.name_en,
        p.name_hi,
        p.name_mr,
        p.form_type,
        p.classical_name,
        p.description,
        p.method_description,
        p.dosage,
        p.ayush_system
    FROM preparations p
    WHERE p.id IN ({placeholders});
    """
    preps = {row["id"]: dict(row) for row in conn.execute(preps_sql, prep_ids)}

    ranked: List[Dict[str, Any]] = []
    for r in rows:
        prep = preps.get(r["preparation_id"])
        if not prep:
            continue
        prep["distance"] = r["distance"]
        ranked.append(prep)

    return ranked
