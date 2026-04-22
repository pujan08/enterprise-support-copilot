from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.graph import support_graph
from app.models import AskRequest
from app.search import test_search_connection, run_search

settings.validate_required_runtime_config()

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://storage2026ex.z13.web.core.windows.net",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "message": f"{settings.app_name} is running",
        "environment": settings.app_env,
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.app_env,
        "integrations": settings.integration_status(),
    }


@app.get("/debug/search")
def debug_search():
    return test_search_connection()


@app.get("/debug/search-query")
def debug_search_query(q: str, top: int = 3):
    return run_search(q, top=top)


@app.post("/ask")
def ask(request: AskRequest):
    graph_result = support_graph.invoke(
        {
            "question": request.question,
            "top": request.top,
        }
    )
    return graph_result["result"]