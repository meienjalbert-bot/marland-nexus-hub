from fastapi import FastAPI, Query
from pydantic import BaseModel
import os, httpx
from .rag_client import rag_query

app = FastAPI(title="marland-nexus-hub")

class QueryResponse(BaseModel):
    source: str
    data: dict

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/query")
async def query(q: str = Query(..., min_length=1)):
    results = await rag_query(q)
    return {"source": "hub-rag", "data": results}

@app.get("/query/cortex")
async def query_cortex(q: str = Query(..., min_length=1), k: int = 5):
    url = os.environ.get("CORTEX_URL", "").rstrip("/")
    if not url:
        return {"error": "CORTEX_URL not configured"}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(f"{url}/route", params={"q": q, "k": k})
        r.raise_for_status()
        return {"source": "cortex-route", "data": r.json()}
