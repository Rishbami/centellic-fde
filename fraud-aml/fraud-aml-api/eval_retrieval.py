from eval_tools import contains_evidence

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
