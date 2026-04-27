from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.router import route_query
from backend.schemas import QueryRequest, QueryResponse


app = FastAPI(
    title="Multi-System Enterprise Assistant",
    description="Lightweight MVP backend with simple agent routing.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8001",
        "http://localhost:8001",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    return route_query(request)
