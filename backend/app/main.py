from fastapi import FastAPI, HTTPException, Query
from app.schemas import QueryRequest, QueryAnswer
from app.rag_engine import answer, search
from app.ollama_llm_adapter import get_llm
from app.db import list_herbs, fetch_herb

app = FastAPI(title="Ayush Herbs AI", version="0.1.0")


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/herbs")
def herbs(limit: int = 50, offset: int = 0):
    return list_herbs(limit, offset)


@app.get("/herbs/{herb_id}")
def herb(herb_id: str):
    row = fetch_herb(herb_id)
    if not row:
        raise HTTPException(404, "Not found")
    return row


@app.get("/search")
def semantic_search(q: str = Query(..., min_length=2), k: int = 5):
    hits = search(q, top_k=k)
    return {"matches": [{"id": i, "score": s} for i, s in hits]}


@app.post("/query", response_model=QueryAnswer)
async def query(req: QueryRequest):
    llm = await get_llm()
    text, lang, sources = await answer(req.question, req.lang, llm)
    return QueryAnswer(answer=text, lang=lang, sources=sources)
