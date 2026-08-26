"""Incident copilot CLI: load a ticket and local support runbooks."""

import argparse
from pathlib import Path
from dotenv import load_dotenv

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
    for book in runbooks:
        print(book["name"], len(book["text"]))


if __name__ == "__main__":
    main()
