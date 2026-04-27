# Architecture

This MVP uses a small FastAPI backend with a deterministic router and two workflow modules.

```text
POST /query
  -> backend.router.route_query
    -> agents.onboarding.run_onboarding_agent
    -> agents.weekly_reporting.run_weekly_reporting_agent
      -> connectors/mock_*.py
        -> data/*.json
```

The connectors are intentionally local and file-backed. They represent the places where real integrations such as Google Drive, Slack, Jira, or meeting transcription systems can be added later.
