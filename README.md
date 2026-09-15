# Incident copilot

Retrieve local support runbooks, ask Grok for next diagnostic steps, log the call, and score the answers.

This is a **Forward Deployed / .NET AI integration / application support** artifact — not a model-training lab.

**Order:** Python first (PyCharm), C# second (JetBrains Rider). Same runbooks, same eval cases, same xAI (Grok) API.

## Status

- **Python:** CLI + 10-case eval. **8/10 → 10/10** after splitting two runbook sections.
- **C#:** Same retrieve → Grok → log loop on .NET 9 (`csharp/IncidentCopilot.sln`, Rider).
- **Eval:** Python is the harness. C# is the production-shaped client.

See [ARCHITECTURE.md](ARCHITECTURE.md).

## Public data

All tickets in `samples/` and `evals/` are **invented**. No real bank logs, customer records, or API keys. The refusal case uses the well-known Visa test PAN `4111…` and a fake SSN so the copilot can be scored for refusing them. `.env` is gitignored.

## Problem

Application support already has the loop: reproduce, search the runbook, try a step, see if it worked. Wiki search is slow and the model is confidently wrong if you dump the whole catalog into the prompt. This repo puts Grok in the **search-and-suggest** step only, with retrieval and a scored eval.

## Architecture

1. Paste an incident (invented ticket text).
2. Chunk local markdown runbooks on `## ` headings.
3. Rank the top 3 chunks (TF-IDF). No vector database.
4. Ask Grok for next diagnostic steps; it may use only those chunks and must cite filenames.
5. Log the call. Score 10 cases in Python. Two failed until a runbook split; **8/10 → 10/10**.

Interview sentence:

> I took the support loop — reproduce, search the runbook, try a fix, see if it worked — and put an LLM in the search-and-suggest step. Retrieval plus a 10-case eval. It failed two cases until I split a runbook. Score went from 8/10 to 10/10.

## What this is not

- A ChatGPT clone
- Fine-tuning or training Grok
- A React dashboard
- Real employer logs or customer data

## How to run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
# Put your key in .env: XAI_API_KEY=...
python python/hello_grok.py
python python/app.py --incident samples/sql_timeout.txt
python python/eval.py
```

C# is the same retrieve → Grok → log loop on .NET (Python remains the eval harness):

```powershell
dotnet run --project csharp/IncidentCopilot -- --incident samples/sql_timeout.txt
```

Open `csharp/IncidentCopilot.sln` in JetBrains Rider. Key setup: [GETTING-STARTED.md](GETTING-STARTED.md).

Raw HTTP (no SDK): import [postman/](postman/README.md). Set `xai_api_key` in Postman; do not commit it.

## Layout

```
incident-copilot/
  README.md
  GETTING-STARTED.md
  ARCHITECTURE.md
  requirements.txt
  python/          eval harness and CLI
  csharp/          same loop on .NET 9 (Rider)
  runbooks/        markdown knowledge base
  evals/           cases.jsonl
  samples/         invented incidents
  postman/         raw Grok HTTP (canned SQL-timeout example)
```

## Stack

| Piece | Choice |
|---|---|
| Model | Grok via xAI (`XAI_API_KEY`, `https://api.x.ai/v1`) |
| Python IDE | **PyCharm** (Community or Professional) |
| Python | 3.13/3.14, pytest, venv at `.venv` |
| C# | .NET 9 console in JetBrains Rider |
| Retrieval | Keyword / TF-IDF first. Vectors only if time is left. |
| Secrets | `.env` gitignored. Never commit keys. |

## Mapping (career, not data)

| Piece | Why it is here |
|---|---|
| Runbooks + retrieval | Knowledge-base / TAG-style issue research |
| Incident → next steps | On-call, SQL, Fiddler/Postman |
| Fail then fix context | Same loop as measuring a bad wiki |
| C# client | Banking .NET and IIS estate |
| Refusal / PCI sample | Regulated banking |

Do not put real employer logs in this repo.

## Production notes (not implemented)

- Redact PAN, SSN, and passwords before the prompt
- Keep prompt/answer logs under a retention policy
- A human clicks “apply” before any mutating command
- Put Okta in front if this were an internal API
- Run eval in CI so a prompt change cannot silently regress

xAI docs: https://docs.x.ai/developers/quickstart · Models: https://docs.x.ai/developers/models
