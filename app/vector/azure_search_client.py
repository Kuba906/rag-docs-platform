from azure.search.documents import SearchClient
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex,
    SearchField,
    SearchFieldDataType,
    VectorSearch,
    VectorSearchProfile,
    HnswAlgorithmConfiguration,
)
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ResourceNotFoundError
from core.config import settings
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def get_credential():
    """Get Azure credential (API key or MSI)."""
    if settings.AZURE_SEARCH_USE_MSI:
        return DefaultAzureCredential()
    else:
        if not settings.AZURE_SEARCH_API_KEY:
            raise ValueError("AZURE_SEARCH_API_KEY is required when not using MSI")
        return AzureKeyCredential(settings.AZURE_SEARCH_API_KEY)


def get_search_client() -> SearchClient:
    """Get Azure Search client with MSI or API key authentication."""
    return SearchClient(
        endpoint=settings.AZURE_SEARCH_ENDPOINT,
        index_name=settings.AZURE_SEARCH_INDEX,
        credential=get_credential()
    )


def get_index_client() -> SearchIndexClient:
    """Get Azure Search Index client for managing indexes."""
    return SearchIndexClient(
        endpoint=settings.AZURE_SEARCH_ENDPOINT,
        credential=get_credential()
    )


def create_index_if_not_exists() -> None:
    """
    Create the Azure Search index if it doesn't exist.

    Index schema:
    - id: unique document ID
    - tenant_id: for multi-tenancy filtering
    - file_id: source file name
    - text: the actual text content
    - text_vector: embedding vector (1536 dimensions for text-embedding-3-large)
    - source: source file name
    - hash: content hash for deduplication
    - page: optional page number
    - section: optional section name
    """
    index_client = get_index_client()
    index_name = settings.AZURE_SEARCH_INDEX

    # Check if index exists
    try:
        index_client.get_index(index_name)
        logger.info(f"Index '{index_name}' already exists")
        return
    except ResourceNotFoundError:
        logger.info(f"Index '{index_name}' not found, creating...")

    # Define index schema
    fields = [
        SearchField(
            name="id",
            type=SearchFieldDataType.String,
            key=True,
            filterable=True
        ),
        SearchField(
            name="tenant_id",
            type=SearchFieldDataType.String,
            filterable=True,
            facetable=True
        ),
        SearchField(
            name="file_id",
            type=SearchFieldDataType.String,
            filterable=True,
            facetable=True
        ),
        SearchField(
            name="text",
            type=SearchFieldDataType.String,
            searchable=True
        ),
        SearchField(
            name="text_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=1536,
            vector_search_profile_name="vector-profile"
        ),
        SearchField(
            name="source",
            type=SearchFieldDataType.String,
            filterable=True
        ),
        SearchField(
            name="hash",
            type=SearchFieldDataType.String,
            filterable=True
        ),
        SearchField(
            name="page",
            type=SearchFieldDataType.Int32,
            filterable=True
        ),
        SearchField(
            name="section",
            type=SearchFieldDataType.String,
            filterable=True
        ),
    ]

    # Configure vector search (HNSW algorithm for fast approximate search)
    vector_search = VectorSearch(
        profiles=[
            VectorSearchProfile(
                name="vector-profile",
                algorithm_configuration_name="hnsw-config"
            )
        ],
        algorithms=[
            HnswAlgorithmConfiguration(
                name="hnsw-config",
                parameters={
                    "m": 4,  # Number of bi-directional links
                    "efConstruction": 400,  # Size of dynamic candidate list for construction
                    "efSearch": 500,  # Size of dynamic candidate list for search
                    "metric": "cosine"  # Similarity metric
                }
            )
        ]
    )

    # Create index
    index = SearchIndex(
        name=index_name,
        fields=fields,
        vector_search=vector_search
    )

    index_client.create_index(index)
    logger.info(f"Created index '{index_name}' successfully")


def get_search_client() -> SearchClient:
    """Get Azure Search client with MSI or API key authentication."""
    return SearchClient(
        endpoint=settings.AZURE_SEARCH_ENDPOINT,
        index_name=settings.AZURE_SEARCH_INDEX,
        credential=get_credential()
    )


def upsert_chunks(chunks: List[Dict[str, Any]]) -> None:
    """
    Upsert chunks to Azure Cognitive Search.

    Args:
        chunks: List of dicts with keys: id, tenant_id, file_id, text, vector, source, hash
    """
    if not settings.AZURE_SEARCH_ENDPOINT:
        raise ValueError("AZURE_SEARCH_ENDPOINT not configured")

    # Ensure index exists before upserting
    create_index_if_not_exists()

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
