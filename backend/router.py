from dataclasses import dataclass
import re

from agents.onboarding import run_onboarding_agent
from agents.weekly_reporting import run_weekly_reporting_agent
from backend.schemas import (
    ClarificationResponse,
    OnboardingResponse,
    QueryRequest,
    QueryResponse,
    WeeklyReportingResponse,
    WorkflowName,
)


REPORTING_KEYWORDS = {
    "weekly",
    "report",
    "summary",
    "summarize",
    "status",
    "task",
    "tasks",
    "meeting",
    "meetings",
    "blocker",
    "blockers",
}

ONBOARDING_KEYWORDS = {
    "onboard",
    "onboarding",
    "new hire",
    "first week",
    "benefits",
    "laptop",
    "badge",
    "access",
    "hr",
    "manager",
    "it",
}


@dataclass(frozen=True)
class RouteDecision:
    workflow: WorkflowName | None
    confidence: float
    scores: dict[str, int]


def score_keywords(query: str, keywords: set[str]) -> int:
    normalized = query.lower()
    tokens = set(re.findall(r"\b[a-z0-9]+\b", normalized))

    score = 0
    for keyword in keywords:
        if " " in keyword:
            score += keyword in normalized
        else:
            score += keyword in tokens
    return score


def infer_workflow(query: str) -> RouteDecision:
    reporting_score = score_keywords(query, REPORTING_KEYWORDS)
    onboarding_score = score_keywords(query, ONBOARDING_KEYWORDS)
    scores = {
        "onboarding": onboarding_score,
        "weekly_reporting": reporting_score,
    }

    if onboarding_score == reporting_score:
        return RouteDecision(workflow=None, confidence=0.0, scores=scores)

    if reporting_score > onboarding_score:
        confidence = reporting_score / (reporting_score + onboarding_score)
        return RouteDecision(
            workflow="weekly_reporting",
            confidence=confidence,
            scores=scores,
        )

    confidence = onboarding_score / (reporting_score + onboarding_score)
    return RouteDecision(workflow="onboarding", confidence=confidence, scores=scores)


def route_query(request: QueryRequest) -> QueryResponse:
    decision = infer_workflow(request.query)

    if decision.workflow is None:
        return ClarificationResponse(
            workflow=None,
            summary=(
                "I am not sure which workflow should handle this. "
                "Please clarify whether this is an onboarding question or a weekly reporting request."
            ),
            sources=[],
        )

    if decision.workflow == "weekly_reporting":
        return WeeklyReportingResponse(**run_weekly_reporting_agent(request.query))
    return OnboardingResponse(**run_onboarding_agent(request.query))
