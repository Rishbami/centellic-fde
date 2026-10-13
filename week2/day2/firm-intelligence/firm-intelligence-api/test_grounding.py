import grounding

SOURCES = {
    "doc-101": "Harding & Voss closed the year with a revenue of $1.24 billion, up to 4.1%.",
    "doc-102": "Fixed-share partners are excluded from the equity partner count.",
}

# failure 1 - ungrounded claims


# test that refusal needs to no citations
def test_refusal_needs_no_citations():
    report = grounding.check_citations(grounding.REFUSAL_SENTENCE, [])
    assert report["refusal"] is True and report["passed"] is True


# test fully cited answer passes
def test_fully_cited_answer_passes():
    answer = (
        "Harding & Voss reported revenue of $1.24 billion [doc-101]. "
        "Fixed-share partners are excluded from the equity partner count [doc-102]."
    )

    report = grounding.check_citations(answer, list(SOURCES))

    assert report["passed"] is True
    assert report["refusal"] is False
    assert report["cited"] == ["doc-101", "doc-102"]
    assert report["invalid"] == []
    assert report["uncited_sentences"] == []


# test uncited sentence is flagged
def test_uncited_sentence_is_flagged():
    uncited = "The firm plans to expand internationally."
    answer = "Harding & Voss reported revenue of $1.24 billion [doc-101]. " + uncited

    report = grounding.check_citations(answer, list(SOURCES))

    assert report["passed"] is False
    assert report["uncited_sentences"] == [uncited]
    assert report["invalid"] == []


# test citations after the full stop still counts
def test_citation_after_full_stop_still_counts():
    answer = "Harding & Voss reported revenue of $1.24 billion. [doc-101]"

    report = grounding.check_citations(answer, list(SOURCES))

    assert report["passed"] is True
    assert report["cited"] == ["doc-101"]
    assert report["uncited_sentences"] == []
    assert report["invalid"] == []
