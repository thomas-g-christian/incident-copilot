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

"""
Incident ID
"""

"""
Call MAIN
"""