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
    action_items = [
        item
        for meeting in meetings
        for item in meeting.get("action_items", [])
    ]
    risks = [
        message["text"]
        for message in chat_logs
        if any(token in message["text"].lower() for token in ("blocked", "risk", "delay"))
    ]
    next_steps = [
        *[
            f"{task['owner']}: {task.get('next_step', 'Continue ' + task['title'])}"
            for task in in_progress
        ],
        *[
            f"{task['owner']}: {task.get('next_step', 'Resolve blocker for ' + task['title'])}"
            for task in blocked
        ],
        *[f"Decision follow-up: {decision}" for decision in decisions[:2]],
        *[f"Meeting action: {item}" for item in action_items[:3]],
    ]

    return {
        "workflow": "weekly_reporting",
        "summary": (
            f"Completed {len(completed)} task(s), kept {len(in_progress)} task(s) in progress, "
            f"and found {len(blocked)} blocker(s)."
        ),
        "completed_work": [
            f"{task['title']}: {task.get('update', 'Done.')}" for task in completed
        ],
        "blockers": [
            f"{task['title']}: {task.get('blocker', task.get('update', 'Blocked.'))}"
            for task in blocked
        ]
        + risks,
        "owners": dict(owners),
        "next_steps": next_steps[:8],
        "sources": [
            "data/chat_logs.json",
            "data/task_updates.json",
            "data/meeting_notes.json",
        ],
    }
