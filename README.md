# RAG Docs Platform — Starter

A minimal Retrieval-Augmented Generation (RAG) service for answering questions from your documents (PDF/DOCX/TXT/HTML).  
Runs locally in Docker (FastAPI + Redis cache + Qdrant vector DB). Optionally uses **Azure OpenAI** for embeddings and answers.

---

## What it does

1. **Ingest** — Upload a document. The app extracts text, cleans it, splits it into chunks, creates embeddings, and stores them in a vector index.  
2. **Ask** — Send a question. The app retrieves the most relevant chunks and asks the LLM to answer **with citations**.  
3. **Cache** — Redis caches embeddings for lower latency and cost.

---

## Prerequisites

- **Docker Desktop** (Apple Silicon or Intel)
- (Optional but recommended) **Azure OpenAI** resource with two deployments:
  - Chat model (e.g., `gpt-4o-mini`)
  - Embeddings model (e.g., `text-embedding-3-large`)

> Without Azure OpenAI credentials, `/ingest` cannot compute embeddings. Tests still run using mocks.

---

## Quick start (local, Docker)

```bash
unzip rag-docs-platform-starter.zip
cd rag-docs-platform
cp .env.example .env
# Fill Azure OpenAI variables in .env if you want real embeddings
docker compose up -d --build

# Health
curl http://localhost:8000/healthz

# Ingest a file (example: README)
curl -F "file=@README.md" http://localhost:8000/ingest

# Ask a question
curl -H "Content-Type: application/json" \
     -d '{"question":"What is this project about?"}' \
     http://localhost:8000/ask

## Tests
```bash
docker compose exec api pytest -q
# or
make test
```