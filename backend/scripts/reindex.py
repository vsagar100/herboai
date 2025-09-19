# Simplest strategy: re-read DB IDs list and rebuild. For 500 rows this is fast on CPU.
# Can be optimized with FAISS IDMap & add/remove later.

import os, sys
from pathlib import Path
# >>> Ensure project root is on sys.path and CWD is project root
ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)  # so relative files like app/seed_data.json work
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.db import list_herbs, fetch_herb
from app.settings import settings
from app.rag_engine import embed_texts, compose_doc
from pathlib import Path
import faiss

lst = list_herbs(limit=10000, offset=0)
ids, docs = [], []
for r in lst:
    row = fetch_herb(r["id"])
    ids.append(row["id"])
    docs.append(compose_doc(row))

X = embed_texts(docs)
index = faiss.IndexFlatIP(X.shape[1])
index.add(X)
Path(settings.INDEX_PATH).parent.mkdir(parents=True, exist_ok=True)
faiss.write_index(index, settings.INDEX_PATH)
with open(settings.INDEX_PATH + ".ids", "w", encoding="utf-8") as f:
    for _id in ids:
        f.write(_id + "\n")
print("Reindex done.")