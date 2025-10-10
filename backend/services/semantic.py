# services/semantic.py (sketch)
import os
import numpy as np
from typing import List, Tuple
from sentence_transformers import SentenceTransformer
import faiss

_model = None
_index = None
_id_map = None

def load_index(model_path="all-MiniLM-L6-v2", index_path="semantic.idx", idmap_path="semantic.ids"):
    global _model, _index, _id_map
    _model = SentenceTransformer(model_path)
    if os.path.exists(index_path) and os.path.exists(idmap_path):
        _index = faiss.read_index(index_path)
        _id_map = np.load(idmap_path)  # array of DB ids
    else:
        _index = None
        _id_map = None

def search(text: str, topk=5) -> List[int]:
    if _model is None or _index is None: return []
    v = _model.encode([text], normalize_embeddings=True)
    D, I = _index.search(v.astype("float32"), topk)
    hits = I[0]
    return [int(_id_map[i]) for i in hits if i >= 0]
