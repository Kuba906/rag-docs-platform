from fastapi import FastAPI
from core.telemetry import setup_logging
from core.middleware import RequestIdMiddleware, MetricsMiddleware
from api.routes_ingest import router as ingest_router
from api.routes_ask import router as ask_router
from api.routes_admin import router as admin_router

app = FastAPI(title="RAG Docs API")
setup_logging()
app.add_middleware(RequestIdMiddleware)
app.add_middleware(MetricsMiddleware)

@app.get("/healthz")
def health():
    return {"ok": True}

app.include_router(ingest_router, prefix="/ingest", tags=["ingest"])
app.include_router(ask_router, prefix="/ask", tags=["ask"])
app.include_router(admin_router, prefix="/admin", tags=["admin"])
