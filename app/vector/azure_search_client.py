from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from core.config import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def get_search_client() -> SearchClient:
    """Get Azure Search client with MSI or API key authentication."""
    if settings.AZURE_SEARCH_USE_MSI:
        credential = DefaultAzureCredential()
    else:
        if not settings.AZURE_SEARCH_API_KEY:
            raise ValueError("AZURE_SEARCH_API_KEY is required when not using MSI")
        credential = AzureKeyCredential(settings.AZURE_SEARCH_API_KEY)

    return SearchClient(
        endpoint=settings.AZURE_SEARCH_ENDPOINT,
        index_name=settings.AZURE_SEARCH_INDEX,
        credential=credential
    )


def upsert_chunks(chunks: List[Dict[str, Any]]) -> None:
    """
    Upsert chunks to Azure Cognitive Search.

    Args:
        chunks: List of dicts with keys: id, tenant_id, file_id, text, vector, source, hash
    """
    if not settings.AZURE_SEARCH_ENDPOINT:
        raise ValueError("AZURE_SEARCH_ENDPOINT not configured")

    client = get_search_client()

    # Transform chunks to Azure Search document format
    documents = []
    for chunk in chunks:
        doc = {
            "id": chunk["id"],
            "tenant_id": chunk["tenant_id"],
            "file_id": chunk["file_id"],
            "text": chunk["text"],
            "text_vector": chunk["vector"],  # Azure Search uses text_vector field
            "source": chunk["source"],
            "hash": chunk["hash"],
        }
        # Optional fields
        if chunk.get("page"):
            doc["page"] = chunk["page"]
        if chunk.get("section"):
            doc["section"] = chunk["section"]

        documents.append(doc)

    logger.info(f"Upserting {len(documents)} chunks to Azure Search index '{settings.AZURE_SEARCH_INDEX}'")
    result = client.upload_documents(documents=documents)

    success_count = sum(1 for r in result if r.succeeded)
    logger.info(f"Successfully uploaded {success_count}/{len(documents)} documents")

    if success_count < len(documents):
        logger.warning(f"Failed to upload {len(documents) - success_count} documents")


def search_chunks(query_vector: List[float], tenant_id: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Search for similar chunks using vector similarity.

    Args:
        query_vector: Embedding vector for the query
        tenant_id: Tenant ID to filter results
        top_k: Number of results to return

    Returns:
        List of matching chunks with text and metadata
    """
    if not settings.AZURE_SEARCH_ENDPOINT:
        raise ValueError("AZURE_SEARCH_ENDPOINT not configured")

    client = get_search_client()

    vector_query = VectorizedQuery(
        vector=query_vector,
        k_nearest_neighbors=top_k,
        fields="text_vector"
    )

    results = client.search(
        search_text=None,
        vector_queries=[vector_query],
        filter=f"tenant_id eq '{tenant_id}'",
        select=["id", "text", "source", "file_id", "page", "section"],
        top=top_k
    )

    chunks = []
    for result in results:
        chunks.append({
            "id": result["id"],
            "text": result["text"],
            "source": result.get("source"),
            "file_id": result.get("file_id"),
            "page": result.get("page"),
            "section": result.get("section"),
            "score": result.get("@search.score", 0.0)
        })

    logger.info(f"Found {len(chunks)} chunks for tenant '{tenant_id}'")
    return chunks
