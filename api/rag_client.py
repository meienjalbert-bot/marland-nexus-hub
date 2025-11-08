import os, httpx

MEILI_HOST = os.getenv("MEILI_HOST", "http://meili:7700").rstrip("/")
MEILI_INDEX = os.getenv("MEILI_INDEX", "docs")
QDRANT_HOST = os.getenv("QDRANT_HOST", "http://qdrant:6333").rstrip("/")
QDRANT_COLLECTION = os.getenv("QDRANT_COLLECTION", "nexus_docs")

async def rag_query(query: str, k: int = 5):
    results = {"lexical": [], "semantic": []}
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.post(f"{MEILI_HOST}/indexes/{MEILI_INDEX}/search", json={"q": query, "limit": k})
            if r.status_code == 200:
                hits = r.json().get("hits", [])
                results["lexical"] = [{"text": h.get("text") or h.get("content") or "", "id": h.get("id")} for h in hits]
    except Exception:
        pass
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            r = await client.post(f"{QDRANT_HOST}/collections/{QDRANT_COLLECTION}/points/search",
                                  json={"vector": [0.0]*4, "limit": k})
            if r.status_code == 200:
                pts = r.json().get("result", [])
                results["semantic"] = [{"text": p.get("payload", {}).get("text", ""), "score": p.get("score")} for p in pts]
    except Exception:
        pass
    return results
