from sqlite_vec import serialize_float32
from db import get_db

def search_similar_vec(table: str, id_col: str, qvec_384: list[float], k: int = 3):
    db = get_db()
    qv = serialize_float32(qvec_384)
    sql = f"""
      SELECT {id_col} AS id, distance
      FROM {table}
      WHERE embedding MATCH ?
        AND k = ?
    """
    return [dict(r) for r in db.execute(sql, (qv, k)).fetchall()]
