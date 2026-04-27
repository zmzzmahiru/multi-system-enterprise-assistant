from collections import Counter

from connectors.mock_chat import get_chat_logs
from connectors.mock_meetings import get_meeting_notes
from connectors.mock_tasks import get_task_updates


def run_weekly_reporting_agent(query: str):
    chat_logs = get_chat_logs()
    tasks = get_task_updates()
    meetings = get_meeting_notes()

    completed = [task for task in tasks if task["status"] == "done"]
    in_progress = [task for task in tasks if task["status"] == "in_progress"]
    blocked = [task for task in tasks if task["status"] == "blocked"]
    owners = Counter(task["owner"] for task in tasks)

    decisions = [
        note["decision"]
        for meeting in meetings
        for note in meeting.get("decisions", [])
    ]
    risks = [
        message["text"]
        for message in chat_logs
        if any(token in message["text"].lower() for token in ("blocked", "risk", "delay"))
    ]

    answer = "\n".join(
        [
            "Weekly summary",
            "",
            f"- Completed: {len(completed)} task(s): {', '.join(task['title'] for task in completed)}.",
            f"- In progress: {len(in_progress)} task(s): {', '.join(task['title'] for task in in_progress)}.",
            f"- Blocked: {len(blocked)} task(s): {', '.join(task['title'] for task in blocked) or 'None'}.",
            f"- Most active task owner: {owners.most_common(1)[0][0]}.",
            "",
            "Key decisions:",
            *[f"- {decision}" for decision in decisions],
            "",
            "Risks and follow-ups:",
            *([f"- {risk}" for risk in risks] or ["- No major risks found in mock logs."]),
        ]
    )

    return {
        "workflow": "weekly_reporting",
        "answer": answer,
        "sources": [
            "data/chat_logs.json",
            "data/task_updates.json",
            "data/meeting_notes.json",
        ],
        "metadata": {
            "query": query,
            "chat_messages": len(chat_logs),
            "tasks": len(tasks),
            "meetings": len(meetings),
        },
    }
