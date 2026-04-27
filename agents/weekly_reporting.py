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
    blocker_items = [
        f"{task['title']}: {task.get('blocker', task.get('update', 'Blocked.'))}"
        for task in blocked
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
        *[f"Follow up on decision: {decision}" for decision in decisions[:1]],
        *[f"Complete meeting action: {item}" for item in action_items[:2]],
    ]

    return {
        "workflow": "weekly_reporting",
        "summary": (
            f"This week, the team completed {len(completed)} item(s), has {len(in_progress)} item(s) "
            f"in progress, and is tracking {len(blocker_items)} blocker(s)."
        ),
        "completed_work": [
            f"{task['title']}: {task.get('update', 'Done.')}" for task in completed
        ],
        "in_progress_work": [
            f"{task['title']}: {task.get('update', 'In progress.')}" for task in in_progress
        ],
        "blockers": blocker_items,
        "owner_task_counts": dict(owners),
        "next_steps": next_steps[:6],
        "sources": [
            "data/chat_logs.json",
            "data/task_updates.json",
            "data/meeting_notes.json",
        ],
    }
