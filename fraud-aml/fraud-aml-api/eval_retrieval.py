from eval_tools import contains_evidence
import statistics

K_VALUES = (1, 3, 5)


def first_hit_rank(
    hits: list[dict],
    doc_id: str,
    evidence: str,
) -> int | None:
    for rank, hit in enumerate(hits, start=1):
        source_id = hit.get("doc_id", hit["id"])

        # Prevent wrong-source match:
        # Require the labelled document, so the same text in another source doesn't count as a hit.
        if source_id == doc_id and contains_evidence(hit["text"], evidence):
            return rank

    return None


def score_strategy(questions: list[dict], ranked: list[list[dict]]) -> dict:
    """Score retrieval ranks, context size, and similarity scores for one strategy."""
    paired = list(zip(questions, ranked, strict=True))
    answerable = [(q, hits) for q, hits in paired if q["doc_id"] is not None]
    unanswerable = [(q, hits) for q, hits in paired if q["doc_id"] is None]

    if not answerable:
        raise ValueError("At least one answerable question is required.")

    ranks = [first_hit_rank(hits, q["doc_id"], q["evidence"]) for q, hits in answerable]

    kinds: dict[str, list[bool]] = {}
    for (q, _), rank in zip(answerable, ranks, strict=True):
        kinds.setdefault(q["kind"], []).append(rank is not None and rank <= 3)

    top_scores = {
        "answerable": [hits[0]["score"] for _, hits in answerable if hits],
        "unanswerable": [hits[0]["score"] for _, hits in unanswerable if hits],
    }

    return {
        **{
            f"recall@{k}": round(
                statistics.mean(r is not None and r <= k for r in ranks), 3
            )
            for k in K_VALUES
        },
        "mrr": round(statistics.mean(1 / r if r is not None else 0 for r in ranks), 3),
        "context_words@3": round(
            statistics.mean(
                sum(len(h["text"].split()) for h in hits[:3]) for _, hits in answerable
            )
        ),
        **{
            f"top_score_{group}": round(statistics.mean(values), 3) if values else None
            for group, values in top_scores.items()
        },
        "recall@3_by_kind": {
            kind: round(statistics.mean(values), 2)
            for kind, values in sorted(kinds.items())
        },
        "missed@3": [
            q["id"]
            for (q, _), rank in zip(answerable, ranks, strict=True)
            if rank is None or rank > 3
        ],
    }
