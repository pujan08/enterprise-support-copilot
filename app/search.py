from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from langsmith import traceable

from app.config import settings


def get_search_client() -> SearchClient:
    return SearchClient(
        endpoint=settings.azure_search_endpoint,
        index_name=settings.azure_search_index_name,
        credential=AzureKeyCredential(settings.azure_search_api_key),
    )


def test_search_connection() -> dict:
    missing = []

    if not settings.azure_search_endpoint:
        missing.append("AZURE_SEARCH_ENDPOINT")
    if not settings.azure_search_index_name:
        missing.append("AZURE_SEARCH_INDEX_NAME")
    if not settings.azure_search_api_key:
        missing.append("AZURE_SEARCH_API_KEY")

    if missing:
        return {
            "ok": False,
            "message": "Missing Azure AI Search configuration",
            "missing": missing,
        }

    try:
        client = get_search_client()
        doc_count = client.get_document_count()

        return {
            "ok": True,
            "message": "Azure AI Search connection successful",
            "index_name": settings.azure_search_index_name,
            "document_count": doc_count,
        }
    except Exception as e:
        return {
            "ok": False,
            "message": "Azure AI Search connection failed",
            "error": str(e),
        }


def make_snippet(text: str, max_length: int = 300) -> str:
    if not text:
        return ""

    clean_text = text.replace("\r", " ").replace("\n", " ").strip()

    if len(clean_text) <= max_length:
        return clean_text

    return clean_text[:max_length].rstrip() + "..."


@traceable(name="run_search", tags=["support-search"], metadata={"component": "search"})
def run_search(query: str, top: int = 3) -> dict:
    missing = []

    if not settings.azure_search_endpoint:
        missing.append("AZURE_SEARCH_ENDPOINT")
    if not settings.azure_search_index_name:
        missing.append("AZURE_SEARCH_INDEX_NAME")
    if not settings.azure_search_api_key:
        missing.append("AZURE_SEARCH_API_KEY")

    if missing:
        return {
            "ok": False,
            "message": "Missing Azure AI Search configuration",
            "missing": missing,
        }

    try:
        client = get_search_client()
        results = client.search(search_text=query, top=top)

        items = []
        for result in results:
            items.append(
                {
                    "id": result.get("id"),
                    "title": result.get("title"),
                    "snippet": make_snippet(result.get("content")),
                    "content": result.get("content"),
                    "score": result.get("@search.score"),
                }
            )

        return {
            "ok": True,
            "query": query,
            "top": top,
            "count": len(items),
            "results": items,
        }
    except Exception as e:
        return {
            "ok": False,
            "message": "Azure AI Search query failed",
            "error": str(e),
        }