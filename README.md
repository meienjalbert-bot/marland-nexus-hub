# marland-nexus-hub (v2)

Gateway API (FastAPI) + RAG minimal, conforme au plan validé (poly-repo, Phase 1).

## Démarrage

```bash
cp .env.example .env
docker compose --profile deps up -d        # Meili + Qdrant
docker compose --profile hub up -d         # API hub (:8000)
curl -s http://localhost:8000/health
```

## Endpoints

- `GET /health`
- `GET /query?q=...` (RAG minimal interne)
- `GET /query/cortex?q=...&k=5` (délégation vers Cortex `/route` si `CORTEX_URL` défini)

## Profils Compose
- `deps`: Meilisearch + Qdrant
- `hub`: API Gateway
