from typing import Any, Literal

from pydantic import BaseModel, Field


WorkflowName = Literal["onboarding", "weekly_reporting"]


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User question or instruction.")
    workflow: WorkflowName | None = Field(
        default=None,
        description="Optional explicit workflow. If omitted, the router infers one.",
    )


class QueryResponse(BaseModel):
    workflow: WorkflowName
    answer: str
    sources: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
