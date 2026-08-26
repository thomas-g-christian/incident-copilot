"""Incident copilot CLI: load a ticket and local support runbooks."""

import argparse
from pathlib import Path
from dotenv import load_dotenv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")


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
    for hit in hits:
        print(hit["name"], hit["heading"], round(hit["score"], 3))


if __name__ == "__main__":
    main()
