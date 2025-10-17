from fastapi import APIRouter, UploadFile, File
from ingest.extract import extract_text
from ingest.normalize import normalize
from ingest.chunk import chunk_text
from ingest.dedupe import chunk_hash
from llm.embeddings import embed_chunks
from vector.qdrant_client import upsert_chunks
from core.config import settings
import uuid

router = APIRouter()

@router.post("")
async def ingest(file: UploadFile = File(...), tenant_id: str | None = None):
    data = await file.read()
    text = normalize(extract_text(data, file.filename))
    chunks = chunk_text(text)
    ids = [str(uuid.uuid4()) for _ in chunks]
    vecs = await embed_chunks(chunks)
    items = []
    tenant = tenant_id or settings.DEFAULT_TENANT
    for i, ch, v in zip(ids, chunks, vecs):
        items.append({
            "id": i,
            "tenant_id": tenant,
            "file_id": file.filename,
            "page": None,
            "section": None,
            "text": ch,
            "vector": v,
            "source": file.filename,
            "hash": chunk_hash(ch)
        })
    upsert_chunks(items)
    return {"tenant": tenant, "file_id": file.filename, "chunks": len(chunks)}
