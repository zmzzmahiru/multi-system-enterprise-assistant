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

## Demo Prompts

Use these prompts in the frontend or send them to `POST /query`.

| Prompt | Expected workflow |
| --- | --- |
| `Create a weekly status report for the team.` | `weekly_reporting` |
| `Help onboard a new teammate.` | `onboarding` |
| `Can you help me with this?` | `fallback` |

Weekly report routing metadata:

```json
{
  "routing": {
    "selected_workflow": "weekly_reporting",
    "routing_reason": "Matched weekly/report/status-related keywords",
    "routing_confidence": "rule-based"
  }
}
```

Onboarding routing metadata:

```json
{
  "routing": {
    "selected_workflow": "onboarding",
    "routing_reason": "Matched onboarding/new-hire/access-related keywords",
    "routing_confidence": "rule-based"
  }
}
```

Fallback routing metadata:

```json
{
  "routing": {
    "selected_workflow": "fallback",
    "routing_reason": "No clear keyword match; asking the user to clarify",
    "routing_confidence": "low-confidence rule-based"
  }
}
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

The client does not need to provide a workflow. The backend infers one from the query using a small keyword-based router and returns routing metadata explaining the decision.

Onboarding response:

```json
{
  "workflow": "onboarding",
  "routing": {
    "selected_workflow": "onboarding",
    "routing_reason": "Matched onboarding/new-hire/access-related keywords",
    "routing_confidence": "rule-based"
  },
  "summary": "Here is the most relevant first-week onboarding guidance I found for your question.",
  "first_week_tasks": [
    "Sign in to Okta and verify email, VPN, Slack, Jira, and GitHub access.",
    "Open a ServiceDesk ticket for any missing application access.",
    "Enroll the laptop in device management before accessing customer data."
  ],
  "documents_to_read": [
    "Device, SSO, and Application Access"
  ],
  "people_to_contact": [
    "People Ops: Maya Chen (People Operations Partner) - maya.chen@acme-corp.example, @maya-people",
    "IT Service Desk: Jordan Patel (IT Service Desk Lead) - it-servicedesk@acme-corp.example, @it-help",
    "Workplace: Elena Garcia (Workplace Experience Coordinator) - workplace@acme-corp.example, @workplace"
  ],
  "meetings": [
    "IT setup office hours are available Tuesday and Thursday at 14:00."
  ],
  "sources": ["data/onboarding_docs.json#laptop-and-account-access"]
}
```

Weekly reporting response:

```json
{
  "workflow": "weekly_reporting",
  "routing": {
    "selected_workflow": "weekly_reporting",
    "routing_reason": "Matched weekly/report/status-related keywords",
    "routing_confidence": "rule-based"
  },
  "summary": "This week, the team completed 2 item(s), has 2 item(s) in progress, and is tracking 2 blocker(s).",
  "completed_work": [
    "Publish customer dashboard API contract: Confluence page published with response examples and error codes.",
    "Draft pilot launch checklist: Checklist covers pilot accounts, rollback owner, support channel, and launch comms."
  ],
  "in_progress_work": [
    "Build read-only pilot dashboard: Account health table is implemented; renewal date filter is still in review.",
    "Prepare customer success kickoff notes: Success criteria are drafted; waiting for final pilot account list confirmation."
  ],
  "blockers": [
    "Validate Northstar Bank SSO integration: Waiting on SAML metadata from Northstar Bank IT.",
    "Run billing connector validation: Finance has not approved access to the shared Stripe sandbox."
  ],
  "owner_task_counts": {
    "Ari Nguyen": 1,
    "Priya Shah": 1,
    "Sam Rivera": 1,
    "Noah Kim": 1,
    "Mina Okafor": 2
  },
  "next_steps": [
    "Priya Shah: Finish renewal date filtering and send preview link to Sales.",
    "Mina Okafor: Send kickoff notes to Customer Success before Monday EOD.",
    "Sam Rivera: Escalate through Customer Success if metadata is not received by Tuesday noon.",
    "Noah Kim: Finance approver to grant sandbox credentials or provide masked export."
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
  "routing": {
    "selected_workflow": "fallback",
    "routing_reason": "No clear keyword match; asking the user to clarify",
    "routing_confidence": "low-confidence rule-based"
  },
  "summary": "I am not sure which workflow should handle this. Please clarify whether this is an onboarding question or a weekly reporting request.",
  "sources": []
}
```

## Tests

```bash
python -m unittest discover -s tests
python -m compileall backend agents connectors tests
python -c "from backend.main import app; print(app.title)"
node --check frontend/app.js
```

## Next Steps

- Replace mock connectors with real systems such as Slack, Jira, Google Drive, or Microsoft Graph.
- Add authentication and tenant-aware data access.
- Add retrieval/vector search for larger internal document collections.
- Expand routing tests as new workflows are added.
