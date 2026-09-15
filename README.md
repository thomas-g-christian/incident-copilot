# FDE / AI integration portfolio

Work folder: `.`

This is **not** another model-training lab. `grok-python-lab` stays the “I measured a toy model” repo. This folder is the **Forward Deployed / .NET AI integration / AI application support** artifact: an incident copilot with retrieval, logging, and a scored eval.

**Order:** Python first (PyCharm), C# second (JetBrains Rider 2026.2). Same runbooks, same eval cases, same xAI (Grok) API.

## Status

- **Done:** Week 1 CLI (retrieve → Grok → `logs/copilot.jsonl`). Week 2 eval: `evals/cases.jsonl` (10 cases), `python/eval.py`.
- **Eval:** **8/10 → 10/10**. Two misses were retrieval. Split `okta_auth.md` (Invalid token / E0000011) and `iis_codes.md` (502 / ARR / bad gateway), then both ranked.
- **Next:** Week 3 C# console (same runbooks, same samples).
- **Not started:** Week 3 C#.

See [PLAN.md](PLAN.md) for the full checklist.

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
- Real Columbia Bank / Fiserv logs or customer data

Sanitized sample incidents only. Say so in the README of the public repo.

## Layout (as you build)

```
FDE_Ai_intergration/
  README.md                 this file
  GETTING-STARTED.md        PyCharm + how to get XAI_API_KEY
  PLAN.md                   week-by-week checklist
  TALK-TRACK.md             90-second interview script
  .gitignore
  python/                   Week 1–2 (primary)
  csharp/                   Week 3 (same API, same runbooks)
  runbooks/                 shared markdown knowledge base
  evals/                    shared cases.jsonl
  samples/                  fake incidents
```

Public GitHub: https://github.com/thomas-g-christian/incident-copilot.git  
This Windows folder is the working copy.

## Stack

| Piece | Choice |
|---|---|
| Model | Grok via xAI (`XAI_API_KEY`, `https://api.x.ai/v1`) |
| Python IDE | **PyCharm** (Community or Professional) |
| Week 1–2 | Python (3.14 in this venv), pytest, PyCharm venv at `.venv` |
| Week 3 | C# console in JetBrains Rider 2026.2 |
| Retrieval | Keyword / TF-IDF first. Vectors only if time is left. |
| Secrets | `.env` gitignored. Never commit keys. |

## Related

- Python lab (separate story): `grok-python-lab`
- xAI docs: https://docs.x.ai/developers/quickstart
- Models: https://docs.x.ai/developers/models

Start at [GETTING-STARTED.md](GETTING-STARTED.md) (PyCharm + API key), then [PLAN.md](PLAN.md).
