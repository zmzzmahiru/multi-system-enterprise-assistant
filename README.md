# Multi-System Enterprise Assistant

Lightweight MVP of a simple agent backend for enterprise assistant workflows.

## What It Does

The backend exposes a single `/query` endpoint and infers which workflow should handle the request:

- **Onboarding Agent**: answers first-week and new-hire questions using mock onboarding docs and contact info.
- **Weekly Reporting Agent**: generates a weekly summary from mock chat logs, task updates, and meeting notes.

## Project Layout

```text
backend/
  main.py          FastAPI app and HTTP endpoints
  router.py        Simple rule-based workflow router
  schemas.py       Request/response models
agents/
  onboarding.py
  weekly_reporting.py
connectors/
  mock_*.py        Local file-backed mock connectors
data/
  *.json           Sample onboarding and reporting data
docs/
  architecture.md
frontend/
  index.html       Minimal single-page UI
  app.js           Browser fetch/render logic
  styles.css       Small CSS stylesheet
tests/
  test_router.py
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, activate with:

```bash
source .venv/bin/activate
```

## Run Backend

```bash
uvicorn backend.main:app --reload
```

Open the API docs at:

```text
http://127.0.0.1:8000/docs
```

## Run Frontend

In a second terminal:

```bash
python -m http.server 5500 -d frontend
```

Open the UI at:

```text
http://127.0.0.1:5500
```

The frontend expects the backend to be running at:

```text
http://127.0.0.1:8000
```

## Example Queries

Onboarding:

```bash
curl -X POST http://127.0.0.1:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"How do I get laptop and VPN access?\"}"
```

Weekly reporting:

```bash
curl -X POST http://127.0.0.1:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Generate this week's project summary\"}"
```

Unclear query:

```bash
curl -X POST http://127.0.0.1:8000/query ^
  -H "Content-Type: application/json" ^
  -d "{\"query\":\"Can you help me with this?\"}"
```

## API

### `POST /query`

Request:

```json
{
  "query": "What benefits steps do I need in my first week?"
}
```

The client does not need to provide a workflow. The backend infers one from the query using a small keyword-based router.

Response:

```json
{
  "workflow": "onboarding",
  "summary": "Found onboarding guidance from the internal first-week docs.",
  "first_week_tasks": [
    "Complete HR paperwork on Monday.",
    "Finish security training by Wednesday.",
    "Confirm role-specific setup with your manager by Friday.",
    "Open an IT helpdesk ticket for any missing laptop, email, VPN, Slack, or Jira access."
  ],
  "documents_to_read": [
    "First-week schedule",
    "Benefits enrollment"
  ],
  "people_to_contact": [
    "HR: Maya Chen (hr-onboarding@example.com)",
    "IT Helpdesk: IT Helpdesk (it-helpdesk@example.com)",
    "Facilities: Facilities Desk (facilities@example.com)"
  ],
  "meetings": [
    "Benefits Q&A on Tuesday at 10:00.",
    "Manager setup check-in by Friday."
  ],
  "sources": ["data/onboarding_docs.json#first-week-schedule"]
}
```

Weekly reporting response:

```json
{
  "workflow": "weekly_reporting",
  "summary": "Completed 2 task(s), kept 1 task(s) in progress, and found 2 blocker(s).",
  "completed_work": [
    "Finalize API contract",
    "Draft launch checklist"
  ],
  "blockers": [
    "Configure SSO integration",
    "Validate billing connector",
    "Risk: vendor SSO metadata is delayed until Thursday."
  ],
  "owners": {
    "Ari": 2,
    "Priya": 1,
    "Sam": 1,
    "Noah": 1
  },
  "next_steps": [
    "Continue: Build dashboard prototype (Priya)",
    "Resolve blocker: Configure SSO integration (Sam)"
  ],
  "sources": [
    "data/chat_logs.json",
    "data/task_updates.json",
    "data/meeting_notes.json"
  ]
}
```

If the router cannot confidently choose a workflow, it asks for clarification:

```json
{
  "workflow": null,
  "summary": "I am not sure which workflow should handle this. Please clarify whether this is an onboarding question or a weekly reporting request.",
  "sources": []
}
```

## Tests

```bash
python -m unittest discover -s tests
```

## Next Steps

- Replace mock connectors with real systems such as Slack, Jira, Google Drive, or Microsoft Graph.
- Add authentication and tenant-aware data access.
- Add retrieval/vector search for larger internal document collections.
- Expand routing tests as new workflows are added.
