from connectors.mock_contacts import get_contacts
from connectors.mock_docs import search_onboarding_docs


def format_contact(label: str, contact: dict[str, str]) -> str:
    role = contact.get("role", "Contact")
    slack = contact.get("slack")
    slack_text = f", {slack}" if slack else ""
    return f"{label}: {contact['name']} ({role}) - {contact['email']}{slack_text}"


def run_onboarding_agent(query: str):
    matches = search_onboarding_docs(query)
    contacts = get_contacts()
    selected_docs = matches[:3]
    selected_or_default_docs = selected_docs or [
        {
            "title": "New Hire First Week Checklist",
            "tasks": [
                "Complete Workday profile, tax forms, and direct deposit by Monday afternoon.",
                "Finish security awareness training before Wednesday standup.",
                "Draft a 30/60/90 day plan with your manager by Friday.",
            ],
            "meetings": [
                "New hire cohort orientation on Monday at 10:00.",
                "Manager 30/60/90 planning session on Friday.",
            ],
        },
        {
            "title": "Device, SSO, and Application Access",
            "tasks": [
                "Sign in to Okta and verify email, VPN, Slack, Jira, and GitHub access.",
            ],
            "meetings": [
                "IT setup office hours are available Tuesday and Thursday at 14:00.",
            ],
        },
    ]

    summary = (
        "Here is the most relevant first-week onboarding guidance I found for your question."
        if selected_docs
        else "I could not find an exact onboarding match, so here are the core first-week resources to get started."
    )
    tasks = [
        task
        for item in selected_or_default_docs
        for task in item.get("tasks", [])
    ]
    meetings = [
        meeting
        for item in selected_or_default_docs
        for meeting in item.get("meetings", [])
    ]

    return {
        "workflow": "onboarding",
        "summary": summary,
        "first_week_tasks": tasks[:6],
        "documents_to_read": [item["title"] for item in selected_or_default_docs],
        "people_to_contact": [
            format_contact("People Ops", contacts["hr"]),
            format_contact("IT Service Desk", contacts["it"]),
            format_contact("Workplace", contacts["facilities"]),
        ],
        "meetings": meetings[:4],
        "sources": [item["source"] for item in selected_docs] or ["data/contacts.json"],
    }
