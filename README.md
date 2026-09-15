# Incident copilot

Retrieve local support runbooks, ask Grok for next diagnostic steps, log the call, and score the answers.

This is a **Forward Deployed / .NET AI integration / application support** artifact — not a model-training lab.

**Order:** Python first (PyCharm), C# second (JetBrains Rider). Same runbooks, same eval cases, same xAI (Grok) API.

## Status

- **Done:** CLI (retrieve → Grok → `logs/copilot.jsonl`). Eval harness: `evals/cases.jsonl` (10 cases) and `python/eval.py`.
- **Eval:** **8/10 → 10/10**. Two misses were retrieval. Split `okta_auth.md` (Invalid token / E0000011) and `iis_codes.md` (502 / ARR / bad gateway), then both ranked.
- **Next:** C# console (same runbooks, same samples).

See [PLAN.md](PLAN.md) for the full checklist.

## Public data

All tickets in `samples/` and `evals/` are **invented**. No real bank logs, customer records, or API keys. The refusal case uses the well-known Visa test PAN `4111…` and a fake SSN so the copilot can be scored for refusing them. `.env` is gitignored.

## Goal

Build a small product that looks like application support:

1. Paste an incident (log, error, ticket text).
2. Retrieve 2–4 relevant snippets from local markdown runbooks.
3. Ask Grok for next diagnostic steps, using only those snippets.
4. Score answers on a tiny eval set. Show one failure, fix the runbook/retrieval, show the score move.

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

Key setup: [GETTING-STARTED.md](GETTING-STARTED.md).

## Layout

```
incident-copilot/
  README.md
  GETTING-STARTED.md
  PLAN.md
  TALK-TRACK.md
  requirements.txt
  python/          eval harness and CLI
  csharp/          same loop on .NET (not started)
  runbooks/        markdown knowledge base
  evals/           cases.jsonl
  samples/         invented incidents
```

## Stack

| Piece | Choice |
|---|---|
| Model | Grok via xAI (`XAI_API_KEY`, `https://api.x.ai/v1`) |
| Python IDE | **PyCharm** (Community or Professional) |
| Week 1–2 | Python (3.14 in this venv), pytest, PyCharm venv at `.venv` |
| Week 3 | C# console in JetBrains Rider 2026.2 |
| Retrieval | Keyword / TF-IDF first. Vectors only if time is left. |
| Secrets | `.env` gitignored. Never commit keys. |

## Mapping (career, not data)

| Piece | Why it is here |
|---|---|
| Runbooks + retrieval | Knowledge-base / TAG-style issue research |
| Incident → next steps | On-call, SQL, Fiddler/Postman |
| Fail then fix context | Same loop as measuring a bad wiki |
| C# client (next) | Banking .NET and IIS estate |
| Refusal / PCI sample | Regulated banking |

Do not put real employer logs in this repo.

xAI docs: https://docs.x.ai/developers/quickstart · Models: https://docs.x.ai/developers/models
