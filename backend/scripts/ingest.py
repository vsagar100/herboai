import argparse, json, os, sys
from pathlib import Path

# >>> Ensure project root is on sys.path and CWD is project root
ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)  # so relative files like app/seed_data.json work
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.db import upsert_herb, fetch_herb
from app.settings import settings
from app.rag_engine import embed_texts
import faiss

parser = argparse.ArgumentParser()
parser.add_argument("--seed", type=str, required=True)
args = parser.parse_args()

with open(args.seed, "r", encoding="utf-8") as f:
    data = json.load(f)

# upsert & collect docs to embed
ids, docs = [], []
for h in data:
    upsert_herb(h)
    row = fetch_herb(h["id"])
    from app.rag_engine import compose_doc
    doc = compose_doc(row)
    ids.append(h["id"])
    docs.append(doc)

X = embed_texts(docs)
index = faiss.IndexFlatIP(X.shape[1])
index.add(X)
Path(settings.INDEX_PATH).parent.mkdir(parents=True, exist_ok=True)
faiss.write_index(index, settings.INDEX_PATH)
with open(settings.INDEX_PATH + ".ids", "w", encoding="utf-8") as f:
    for _id in ids:
        f.write(_id + "\n")
print(f"Indexed {len(ids)} herbs → {settings.INDEX_PATH}")