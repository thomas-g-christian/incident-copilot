# Postman — raw Grok HTTP

Same `POST https://api.x.ai/v1/chat/completions` call the C# `HttpClient` and the Python xAI SDK make. This is **not** retrieval: the SQL-timeout request already has canned runbook excerpts.

The ticket text is invented (`DataPortal`). `xai_api_key` is blank in git. Do not export a personal Postman environment with a real key back into this folder.

## Import

1. Postman → **Import** → `incident-copilot.postman_collection.json`
2. Import `incident-copilot.postman_environment.json` (optional). Or set collection variables.
3. Set **`xai_api_key`** to your console key (same value as `.env`). Leave it empty in git.

Never commit a real key. The checked-in files have `xai_api_key` blank.

## Requests

| Request | What it is |
|---|---|
| Health — grok-4.6 hello | Key + model check (`python/hello_grok.py`) |
| Incident copilot — SQL timeout | Same system prompt as `GrokClient.cs` / `python/app.py`, plus `samples/sql_timeout.txt` and the three `sql_timeout.md` chunks those apps rank |

## If it 401s

The variable is empty, or the key has no credits. Use the repo-root `.env` locally; do not paste the key into the JSON on disk.