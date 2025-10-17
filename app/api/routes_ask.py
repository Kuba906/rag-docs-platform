from fastapi import APIRouter
from pydantic import BaseModel
from qdrant_client.http.models import ScoredPoint
from vector.qdrant_client import search
from llm.embeddings import embed_chunks
from llm.chat import answer_with_context
from core.config import settings

router = APIRouter()

class Q(BaseModel):
    question: str
    tenant_id: str | None = None
    k: int = 4

@router.post("")
async def ask(q: Q):
    vec = (await embed_chunks([q.question]))[0]
    tenant = q.tenant_id or settings.DEFAULT_TENANT
    hits: list[ScoredPoint] = search(vec, tenant, top_k=q.k)
    ctx = [{
        "file_id": h.payload.get("file_id"),
        "page": h.payload.get("page"),
        "text": h.payload.get("text"),
        "score": h.score,
    } for h in hits]
    ans, citations, cost = await answer_with_context(q.question, ctx)
    return {"answer": ans, "sources": citations, "cost": cost}
