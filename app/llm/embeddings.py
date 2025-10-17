import hashlib, json
from typing import List
import redis
from openai import AsyncAzureOpenAI
from core.config import settings

_r = redis.from_url(settings.REDIS_URL)

async def _client() -> AsyncAzureOpenAI:
    return AsyncAzureOpenAI(
        azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
        api_key=settings.AZURE_OPENAI_API_KEY,
        api_version="2024-07-01-preview",
    )

def _key(s: str) -> str:
    return "emb:" + hashlib.sha256(s.encode("utf-8")).hexdigest()

async def embed_chunks(chunks: List[str]) -> List[List[float]]:
    out: List[List[float]] = []
    to_query = []
    order = []
    for i, ch in enumerate(chunks):
        k = _key(ch)
        v = _r.get(k)
        if v:
            out.append(json.loads(v))
        else:
            to_query.append(ch)
            order.append(i)
            out.append(None)
    if to_query:
        cli = await _client()
        resp = await cli.embeddings.create(input=to_query, model=settings.AZURE_OPENAI_DEPLOYMENT_EMBED)
        vecs = [d.embedding for d in resp.data]
        for idx, vec in zip(order, vecs):
            out[idx] = vec
            _r.setex(_key(chunks[idx]), 60*60*24*7, json.dumps(vec))
    return out
