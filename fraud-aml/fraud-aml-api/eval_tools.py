import re
from grounding import if_refusal


def contains_evidence(text: str, evidence: str) -> bool:
    normalised_text = " ".join(text.split()).casefold()
    normalised_evidence = " ".join(evidence.split()).casefold()

    return bool(normalised_evidence) and normalised_evidence in normalised_text


def _alternative_matches(answer: str, alternative: str) -> bool:
    prefix = alternative.endswith("*")
    core = re.escape(alternative.rstrip("*").casefold())
    ending = "" if prefix else r"(?![a-z0-9])"

    return (
        re.search(
            rf"(?<![a-z0-9]){core}{ending}",
            answer.casefold(),
        )
        is not None
    )


def keywords_present(answer: str | None, keywords: list[str]) -> bool:
    if answer is None or if_refusal(answer):
        return False

    return all(
        any(
            _alternative_matches(answer, alternative)
            for alternative in group.split("|")
        )
        for group in keywords
    )
