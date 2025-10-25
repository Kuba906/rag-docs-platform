"""
Vector store factory - automatically selects Qdrant (local) or Azure Search (cloud).
"""
from core.config import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def get_vector_store_type() -> str:
    """
    Determine which vector store to use based on environment.

    Returns:
        "azure_search" if Azure Search endpoint is configured, otherwise "qdrant"
    """
    if settings.AZURE_SEARCH_ENDPOINT:
        return "azure_search"
    return "qdrant"


def upsert_chunks(chunks: List[Dict[str, Any]]) -> None:
    """
    Upsert chunks to the appropriate vector store.

    Automatically uses Azure Search if configured, otherwise falls back to Qdrant.
    """
    store_type = get_vector_store_type()
    logger.info(f"Using vector store: {store_type}")

    if store_type == "azure_search":
        from vector.azure_search_client import upsert_chunks as azure_upsert
        azure_upsert(chunks)
    else:
        from vector.qdrant_client import upsert_chunks as qdrant_upsert
        qdrant_upsert(chunks)


def search_chunks(query_vector: List[float], tenant_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar chunks in the appropriate vector store.

    Automatically uses Azure Search if configured, otherwise falls back to Qdrant.
    """
    store_type = get_vector_store_type()
    logger.info(f"Using vector store: {store_type}")

    if store_type == "azure_search":
        from vector.azure_search_client import search_chunks as azure_search
        return azure_search(query_vector, tenant_id, top_k)
    else:
        from vector.qdrant_client import search_chunks as qdrant_search
        return qdrant_search(query_vector, tenant_id, top_k)
