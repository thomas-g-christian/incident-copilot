"""Incident copilot CLI: retrieve runbooks, ask Grok, log the call."""

import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from xai_sdk import Client
from xai_sdk.chat import system, user

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

MODEL = "grok-4.6"
LOG_DIR = ROOT / "logs"
SYSTEM_PROMPT = """You are an application-support copilot for a banking portal.

Rules:
- Use ONLY the runbook excerpts in the user message.
- Cite the runbook filename (for example sql_timeout.md) on each recommended step.
- If the runbooks do not cover the issue, say you do not know. Do not invent procedures.
- Do not ask for PAN, SSN, passwords, or full customer records.
- Output short numbered diagnostic next steps. No preamble."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Incident copilot")
    parser.add_argument(
        "--incident",
        required=True,
        help="Path to a sample ticket .txt file",
    )
    return parser.parse_args()


def resolve_incident_path(raw: str, root: Path) -> Path:
    """Resolve --incident to an absolute path (cwd first, then project root)."""
    path = Path(raw)
    if path.is_absolute():
        return path
    cwd_path = Path.cwd() / path
    if cwd_path.is_file():
        return cwd_path.resolve()
    return (root / path).resolve()


def load_incident(path: Path) -> str:
    """Read the incident file. Raises if missing or empty."""
    if not path.is_file():
        raise FileNotFoundError(f"incident file not found: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Incident file is empty: {path}")
    return text


def extract_incident_id(text: str) -> str:
    """Return the Ticket Number: value, or 'unknown'."""
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("ticket number:"):
            return line.split(":", 1)[1].strip() or "unknown"
    return "unknown"


def load_runbooks(root: Path) -> list[dict]:
    """Load non-empty *.md files from <root>/runbooks."""
    runbooks_dir = root / "runbooks"
    if not runbooks_dir.is_dir():
        raise FileNotFoundError(f"runbooks folder not found: {runbooks_dir}")

    loaded = []
    for path in sorted(runbooks_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            continue
        loaded.append({
            "path": path,
            "name": path.name,
            "text": text,
        })

    if not loaded:
        raise ValueError(f"no runbook markdown files in {runbooks_dir}")
    return loaded


def chunk_runbooks(runbooks: list[dict]) -> list[dict[str, str]]:
    """Split each runbook on ## headings. Files with no ## stay one chunk."""
    chunks: list[dict[str, str]] = []
    for book in runbooks:
        heading = book["name"]
        lines: list[str] = []
        for line in book["text"].splitlines():
            if line.startswith("## "):
                text = "\n".join(lines).strip()
                if text:
                    chunks.append({
                        "name": book["name"],
                        "heading": heading,
                        "text": text,
                    })
                heading = line[3:].strip()
                lines = [line]
            else:
                lines.append(line)
        text = "\n".join(lines).strip()
        if text:
            chunks.append({
                "name": book["name"],
                "heading": heading,
                "text": text,
            })
    return chunks


def retrieve(
    incident_text: str,
    chunks: list[dict[str, str]],
    k: int = 3,
) -> list[dict]:
    """Return the k runbook chunks closest to the incident text."""
    if not chunks:
        return []

    corpus = [chunk["text"] for chunk in chunks]
    vectorizer = TfidfVectorizer(stop_words="english")
    chunk_vectors = vectorizer.fit_transform(corpus)
    incident_vector = vectorizer.transform([incident_text])
    scores = cosine_similarity(incident_vector, chunk_vectors)[0]

    ranked = sorted(
        zip(scores, chunks),
        key=lambda pair: pair[0],
        reverse=True,
    )

    hits = []
    for score, chunk in ranked[:k]:
        hits.append({
            "name": chunk["name"],
            "heading": chunk["heading"],
            "text": chunk["text"],
            "score": float(score),
        })
    return hits


def format_user_message(incident_text: str, hits: list[dict]) -> str:
    """Incident plus retrieved runbook excerpts for the Grok user turn."""
    parts = ["Incident:", incident_text.strip(), "", "Runbook excerpts:"]
    for i, hit in enumerate(hits, 1):
        parts.append(f"--- [{i}] {hit['name']} / {hit['heading']} ---")
        parts.append(hit["text"].strip())
        parts.append("")
    return "\n".join(parts)


def ask_grok(incident_text: str, hits: list[dict]) -> tuple[str, float]:
    """Call Grok with the incident and retrieved chunks. Returns (answer, latency_s)."""
    api_key = os.getenv("XAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "XAI_API_KEY is missing.\n"
            f"Put one line in {ROOT / '.env'}:\n"
            "XAI_API_KEY=your_key_here"
        )

    client = Client(api_key=api_key)
    chat = client.chat.create(
        model=MODEL,
        messages=[system(SYSTEM_PROMPT)],
    )
    chat.append(user(format_user_message(incident_text, hits)))
    started = time.perf_counter()
    response = chat.sample()
    latency_s = time.perf_counter() - started
    answer = (response.content or "").strip()
    if not answer:
        raise RuntimeError("Grok returned an empty answer")
    return answer, latency_s


def append_jsonl(record: dict) -> Path:
    """Append one JSON object to logs/copilot.jsonl."""
    LOG_DIR.mkdir(exist_ok=True)
    path = LOG_DIR / "copilot.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    return path


def main() -> None:
    args = parse_args()
    path = resolve_incident_path(args.incident, ROOT)
    text = load_incident(path)
    ticket_id = extract_incident_id(text)
    print(f"Incident ID: {ticket_id}")
    print(f"File: {path}")
    print()
    print(text)

    runbooks = load_runbooks(ROOT)
    chunks = chunk_runbooks(runbooks)
    hits = retrieve(text, chunks, k=3)
    print()
    print("Retrieved:")
    for hit in hits:
        print(f"  {hit['name']} / {hit['heading']}  {round(hit['score'], 3)}")

    answer, latency_s = ask_grok(text, hits)
    print()
    print(f"Model: {MODEL}  latency: {latency_s:.3f}s")
    print()
    print(answer)

    log_path = append_jsonl({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "incident_id": ticket_id,
        "incident_file": str(path),
        "chunks_used": [
            {
                "name": hit["name"],
                "heading": hit["heading"],
                "score": hit["score"],
            }
            for hit in hits
        ],
        "model": MODEL,
        "answer": answer,
        "latency_s": round(latency_s, 3),
    })
    print()
    print(f"Logged: {log_path}")


if __name__ == "__main__":
    main()
