from typing import Literal

from pydantic import BaseModel, Field


WorkflowName = Literal["onboarding", "weekly_reporting"]


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User question or instruction.")


class RoutingMetadata(BaseModel):
    selected_workflow: str
    routing_reason: str
    routing_confidence: str


class OnboardingResponse(BaseModel):
    workflow: Literal["onboarding"]
    routing: RoutingMetadata
    summary: str
    first_week_tasks: list[str] = Field(default_factory=list)
    documents_to_read: list[str] = Field(default_factory=list)
    people_to_contact: list[str] = Field(default_factory=list)
    meetings: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class WeeklyReportingResponse(BaseModel):
    workflow: Literal["weekly_reporting"]
    routing: RoutingMetadata
    summary: str
    completed_work: list[str] = Field(default_factory=list)
    in_progress_work: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    owner_task_counts: dict[str, int] = Field(default_factory=dict)
    next_steps: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class ClarificationResponse(BaseModel):
    workflow: None
    routing: RoutingMetadata
    summary: str
    sources: list[str] = Field(default_factory=list)


QueryResponse = OnboardingResponse | WeeklyReportingResponse | ClarificationResponse
