REFUSAL_SENTENCE = "The provided documents do not answer that question."


def normalise(text: str) -> str:
    return " ".join(text.split()).casefold()


def if_refusal(answer: str | None) -> bool:
    return answer is None or normalise(REFUSAL_SENTENCE) in normalise(answer)
