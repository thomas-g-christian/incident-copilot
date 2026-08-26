import argparse
from pathlib import Path
from dotenv import load_dotenv

"""
Set the project root
"""
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

"""
Parse the incident
"""
def parse_args() ->argparse.Namespace:
    parser = argparse.ArgumentParser(description="Incident copilot")
    parser.add_argument(
        "--incident",
        required=True,
        help="Path to a sample ticket .txt file",
    )
    return parser.parse_args()

"""
Resolve the path
"""
def resolve_incident_path(raw: str, root: Path) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    cwd_path = Path.cwd() / path
    if cwd_path.is_file():
        return cwd_path.resolve()
    return (root / path).resolve()
 
"""
Read the ticket
"""
def load_incident(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"incident file not found: {path}")
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        raise ValueError(f"Incident file is empty: {path}")
    return text

"""
Incident ID
"""
def extract_incident_id(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line.lower().startswith("ticket number:"):
            return line.split(":", 1)[1].strip() or "unknown"
    return "unknown"

"""
Call MAIN
"""