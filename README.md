# RAG Docs API — Starter (Azure-first)

## Wymagania
- Docker Desktop + docker compose
- (Opcjonalnie) dostęp do Azure OpenAI (endpoint + key)

## Szybki start (lokalnie: Qdrant + Redis)
```bash
cp .env.example .env   # uzupełnij AZURE_OPENAI_* jeśli chcesz prawdziwe embeddingi
docker compose up -d --build
# zdrowie
curl http://localhost:8000/healthz

# załaduj plik
curl -F "file=@README.md" http://localhost:8000/ingest

# zapytaj
curl -H "Content-Type: application/json" -d '{"question":"O czym jest ten plik?"}' http://localhost:8000/ask
```

## Testy
```bash
docker compose exec api pytest -q
# lub
make test
```

## Notatki
- Domyślnie używamy Qdrant (lokalnie). W Azure polecam Azure AI Search (vector).
- Wersje modeli/SDK dopasuj do swojej subskrypcji Azure.
