from agents.onboarding import run_onboarding_agent
from agents.weekly_reporting import run_weekly_reporting_agent
from backend.schemas import QueryRequest, QueryResponse, WorkflowName


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


def infer_workflow(query: str) -> WorkflowName:
    normalized = query.lower()
    reporting_score = sum(keyword in normalized for keyword in REPORTING_KEYWORDS)
    onboarding_score = sum(keyword in normalized for keyword in ONBOARDING_KEYWORDS)

    if reporting_score > onboarding_score:
        return "weekly_reporting"
    return "onboarding"


def route_query(request: QueryRequest) -> QueryResponse:
    workflow = request.workflow or infer_workflow(request.query)

    if workflow == "weekly_reporting":
        return QueryResponse(**run_weekly_reporting_agent(request.query))
    return QueryResponse(**run_onboarding_agent(request.query))
