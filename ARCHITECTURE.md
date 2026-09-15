# Architecture

Incident copilot: retrieve a few local runbooks, ask Grok for next diagnostic steps, log the call, score the answers.

```
incident .txt  →  chunk runbooks (## headings)
               →  TF-IDF top 3
               →  Grok (runbooks only)
               →  logs/copilot.jsonl
               →  python/eval.py  (10 cases)
```

## Loop

1. **Incident** — UTF-8 ticket text (`samples/`). Ticket id from `Ticket Number:`.
2. **Retrieve** — Load repo-root `runbooks/*.md`. Split on `## `. Rank top 3 chunks (Python: sklearn TF-IDF; C#: in-process TF-IDF cosine). No vector database.
3. **Prompt** — System rule: use only the excerpts, cite filenames, say you do not know if it is missing. Model: `grok-4.6` at `https://api.x.ai/v1`.
4. **Log** — Append one JSON line: timestamp, incident id, chunks, model, answer, latency. `logs/` is gitignored.
5. **Eval** — `python/eval.py` scores `must_include` terms. Python is the harness. C# is the same loop on .NET 9.

## What is shared

| Path | Role |
|---|---|
| `runbooks/` | Knowledge base (both languages) |
| `samples/` | Invented tickets |
| `evals/cases.jsonl` | Python eval only |
| `.env` | `XAI_API_KEY` (gitignored) |
| `logs/copilot.jsonl` | Audit log (gitignored) |

## Production notes (not implemented)

- Redact PAN, SSN, passwords before the prompt
- Retain prompt/answer logs under a policy
- A human clicks “apply” before any mutating command
- Okta in front if this were an internal API
- Run eval in CI so a prompt change cannot silently regress
