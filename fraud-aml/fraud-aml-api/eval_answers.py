import json
from pathlib import Path
import statistics

from eval_tools import keywords_present
from grounding import if_refusal


def load_baseline() -> dict:
    report = json.loads(
        Path("eval_results/retrieval_baseline.json").read_text(encoding="utf-8")
    )

    if not report["questions"]:
        raise ValueError("The baseline contains no evaluation questions.")

    if len(report["questions"]) != len(report["ranked_results"]):
        raise ValueError("Questions and retrieval results do not match.")

    return report


def run(questions: list[dict], ranked: list[list[dict]], floor: float) -> dict:
    import llm

    records = []
    model_calls = 0
    input_tokens = 0

    for q, hits in zip(questions, ranked, strict=True):
        usable = [hit for hit in hits[:3] if hit["score"] >= floor]
        result = {
            "answer": None,
            "input_tokens": 0,
            "output_tokens": 0,
            "stop_reason": "insufficient_guidance",
        }

        if usable:
            context = "\n\n".join(
                f"[{hit['id']}] {hit['title']}\n{hit['text']}" for hit in usable
            )
            result = llm.answer_from_context(q["question"], context)
            model_calls += 1
            input_tokens += result["input_tokens"]

        completed = result["stop_reason"] in ("end_turn", "insufficient_guidance")
        refused = completed and if_refusal(result["answer"])
        passed = completed and (
            keywords_present(result["answer"], q["keywords"])
            if q["doc_id"] is not None
            else refused
        )

        records.append(
            {
                "id": q["id"],
                "expected_doc_id": q["doc_id"],
                "passed": passed,
                "refused": refused,
                "sources": [hit["id"] for hit in usable],
                **result,
            }
        )

    answerable = [r for r in records if r["expected_doc_id"] is not None]
    unanswerable = [r for r in records if r["expected_doc_id"] is None]

    return {
        "answer_accuracy": (
            round(statistics.mean(r["passed"] for r in answerable), 3)
            if answerable
            else None
        ),
        "refusal_accuracy": (
            round(statistics.mean(r["passed"] for r in unanswerable), 3)
            if unanswerable
            else None
        ),
        "false_refusals": [r["id"] for r in answerable if r["refused"]],
        "wrong_or_unrefused": [
            r["id"]
            for r in records
            if not r["passed"]
            and not (r["expected_doc_id"] is not None and r["refused"])
        ],
        "model_calls": model_calls,
        "avg_input_tokens": round(input_tokens / model_calls) if model_calls else 0,
        "answers": records,
    }
