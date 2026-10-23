import json
from pathlib import Path


def load_baseline() -> dict:
    report = json.loads(
        Path("eval_results/retrieval_baseline.json").read_text(encoding="utf-8")
    )

    if not report["questions"]:
        raise ValueError("The baseline contains no evaluation questions.")

    if len(report["questions"]) != len(report["ranked_results"]):
        raise ValueError("Questions and retrieval results do not match.")

    return report
