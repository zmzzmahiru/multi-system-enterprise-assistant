from typing import Literal

from pydantic import BaseModel, Field


WorkflowName = Literal["onboarding", "weekly_reporting"]


class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, description="User question or instruction.")


class OnboardingResponse(BaseModel):
    workflow: Literal["onboarding"]
    summary: str
    first_week_tasks: list[str] = Field(default_factory=list)
    documents_to_read: list[str] = Field(default_factory=list)
    people_to_contact: list[str] = Field(default_factory=list)
    meetings: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class WeeklyReportingResponse(BaseModel):
    workflow: Literal["weekly_reporting"]
    summary: str
    completed_work: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    owners: dict[str, int] = Field(default_factory=dict)
    next_steps: list[str] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)


class ClarificationResponse(BaseModel):
    workflow: None
    summary: str
    sources: list[str] = Field(default_factory=list)


QueryResponse = OnboardingResponse | WeeklyReportingResponse | ClarificationResponse
