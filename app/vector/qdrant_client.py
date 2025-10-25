from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue

_client: QdrantClient | None = None
COLL = "chunks"

def qdrant() -> QdrantClient:
    global _client
    if _client is None:
        _client = QdrantClient(host="qdrant", port=6333)
        try:
            _client.get_collection(COLL)
        except Exception:
            _client.recreate_collection(COLL, vectors_config=VectorParams(size=1536, distance=Distance.COSINE))
    return _client

def upsert_chunks(items: list[dict]):
    qc = qdrant()
    points = [PointStruct(id=i["id"], vector=i["vector"], payload=i) for i in items]
    qc.upsert(collection_name=COLL, points=points)

def search(query_vec: list[float], tenant: str, top_k: int = 4):
    qc = qdrant()
    return qc.search(
        collection_name=COLL,
        query_vector=query_vec,
        limit=top_k,
        query_filter=Filter(must=[FieldCondition(key="tenant_id", match=MatchValue(value=tenant))])
    )

def search_chunks(query_vector: list[float], tenant_id: str, top_k: int = 5) -> list[dict]:
    """
    Search for similar chunks (compatible with factory interface).

    Returns list of dicts with standardized format.
    """
    hits = search(query_vector, tenant_id, top_k)
    return [{
        "id": str(h.id),
        "text": h.payload.get("text"),
        "source": h.payload.get("source"),
        "file_id": h.payload.get("file_id"),
        "page": h.payload.get("page"),
        "section": h.payload.get("section"),
        "score": h.score
    } for h in hits]
