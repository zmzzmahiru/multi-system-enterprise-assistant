from fastapi import FastAPI

from backend.router import route_query
from backend.schemas import QueryRequest, QueryResponse


app = FastAPI(
    title="Multi-System Enterprise Assistant",
    description="Lightweight MVP backend with simple agent routing.",
    version="0.1.0",
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    return route_query(request)
