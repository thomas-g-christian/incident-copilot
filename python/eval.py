"""Score the incident copilot against evals/cases.jsonl."""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from app import ROOT, append_jsonl, extract_incident_id, run_copilot

CASES_PATH = ROOT / "evals" / "cases.jsonl"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Incident copilot eval")
    parser.add_argument(
        "--cases",
        default=str(CASES_PATH),
        help="Path to cases.jsonl",
    )
    return parser.parse_args()


def load_cases(path: Path) -> list[dict]:
    if not path.is_file():
        raise FileNotFoundError(f"eval cases not found: {path}")
    cases = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        row = json.loads(line)
        if "id" not in row or "incident" not in row:
            raise ValueError(f"{path}:{line_no} needs id and incident")
        cases.append(row)
    if not cases:
        raise ValueError(f"no cases in {path}")
    return cases


def score_answer(answer: str, case: dict) -> tuple[bool, list[str]]:
    """Return (passed, missed terms). Substring match, case-insensitive."""
    haystack = answer.lower()
    missed: list[str] = []
    for term in case.get("must_include", []):
        if term.lower() not in haystack:
            missed.append(term)
    any_terms = case.get("must_include_any", [])
    if any_terms and not any(term.lower() in haystack for term in any_terms):
        missed.append("any:" + "|".join(any_terms))
    for term in case.get("must_not_include", []):
        if term.lower() in haystack:
            missed.append("forbidden:" + term)
    return (not missed, missed)


def main() -> None:
    args = parse_args()
    cases_path = Path(args.cases)
    if not cases_path.is_absolute():
        cwd_path = Path.cwd() / cases_path
        cases_path = cwd_path if cwd_path.is_file() else ROOT / cases_path

    cases = load_cases(cases_path)
    passed = 0
    print(f"Cases: {cases_path} ({len(cases)})")
    print()

    for case in cases:
        case_id = case["id"]
        incident = case["incident"]
        result = run_copilot(incident, k=3)
        ok, missed = score_answer(result["answer"], case)
        retrieved = ", ".join(
            f"{hit['name']}/{hit['heading']}" for hit in result["hits"]
        )
        if ok:
            passed += 1
            status = "PASS"
        else:
            status = "FAIL"
        print(f"{status}  {case_id}  {result['latency_s']:.1f}s")
        print(f"  retrieved: {retrieved}")
        if missed:
            print(f"  missed: {missed}")
        print()

        append_jsonl(
            {
                "case_id": case_id,
                "incident_id": extract_incident_id(incident),
                "passed": ok,
                "missed": missed,
                "chunks_used": [
                    {
                        "name": hit["name"],
                        "heading": hit["heading"],
                        "score": hit["score"],
                    }
                    for hit in result["hits"]
                ],
                "model": result["model"],
                "answer": result["answer"],
                "latency_s": round(result["latency_s"], 3),
            },
            filename="eval.jsonl",
        )

    total = len(cases)
    print(f"{passed}/{total} passed")
    if passed != total:
        sys.exit(1)


if __name__ == "__main__":
    main()
