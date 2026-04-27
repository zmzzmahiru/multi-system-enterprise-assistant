# Multi-System Enterprise Assistant

Lightweight MVP of a simple agent backend for enterprise assistant workflows.

## What It Does

The backend exposes a single `/query` endpoint and routes requests to one of two workflows:

- **Onboarding Agent**: answers first-week and new-hire questions using mock onboarding docs and contact info.
- **Weekly Reporting Agent**: generates a weekly summary from mock chat logs, task updates, and meeting notes.

## Project Layout

```text
backend/
  main.py          FastAPI app and HTTP endpoints
  router.py        Simple workflow router
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

## Run

```bash
uvicorn backend.main:app --reload
```

Open the API docs at:

```text
http://127.0.0.1:8000/docs
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
  -d "{\"workflow\":\"weekly_reporting\",\"query\":\"Generate this week's project summary\"}"
```

## API

### `POST /query`

Request:

```json
{
  "query": "What benefits steps do I need in my first week?",
  "workflow": "onboarding"
}
```

`workflow` is optional. Supported values are:

- `onboarding`
- `weekly_reporting`

Response:

```json
{
  "workflow": "onboarding",
  "answer": "Here is what I found...",
  "sources": ["data/onboarding_docs.json#benefits-enrollment"],
  "metadata": {
    "matches": 1
  }
}
```

## Next Steps

- Replace mock connectors with real systems such as Slack, Jira, Google Drive, or Microsoft Graph.
- Add authentication and tenant-aware data access.
- Add retrieval/vector search for larger internal document collections.
- Add tests around routing and workflow output.
