def contains_evidence(text: str, evidence: str) -> bool:
    normalised_text = " ".join(text.split()).casefold()
    normalised_evidence = " ".join(evidence.split()).casefold()

    return bool(normalised_evidence) and normalised_evidence in normalised_text
