"""A chunker must not lose, duplicate, or mangle text"""

import pytest

import chunking
from corpus import CORPUS_DOCUMENTS
from documents import DOCUMENTS

DOC = next(d for d in CORPUS_DOCUMENTS if d["id"] == "doc-105")
ALL_DOCS = DOCUMENTS + CORPUS_DOCUMENTS


# test_fixed_chunks_without_overlap_lose_no_words
def test_fixed_chunks_without_overlap_lose_no_words():
    chunks = chunking.fixed_words(DOC, size=100)
    rebuilt = " ".join(c["text"] for c in chunks).split()
    assert rebuilt == DOC["body"].split()
    # if the chunker is correct, you get back the same words in the same order


# test_overlap_repeats_exactly_the_overlap_words
def test_overlap_repeats_exactly_the_overlap_works():
    chunks = chunking.fixed_words(DOC, size=100, overlap=25)
    for first, second in zip(chunks, chunks[1:]):
        assert first["text"].split()[-25:] == second["text"].split()[:25]


# test overlap must be smaller than size
@pytest.mark.parametrize("overlap", [100, 101])
def test_overlap_must_be_smaller_than_size(overlap):
    with pytest.raises(ValueError, match="smaller than size"):
        chunking.fixed_words(DOC, size=100, overlap=overlap)


# test sentences packing never cuts a sentence
def test_sentences_packing_never_cuts_a_sentence():
    doc = {
        "id": "test-sentences",
        "title": "Sentence packing",
        "body": (
            "Revenue rose. Costs fell! Profits improved? "
            "This whole sentence exceeds the word limit. Hiring paused."
        ),
    }

    chunks = chunking.sentenced_packed(doc, max_words=4)

    assert [c["text"] for c in chunks] == [
        "Revenue rose. Costs fell!",
        "Profits improved?",
        "This whole sentence exceeds the word limit.",
        "Hiring paused.",
    ]


# test contextual sections carry title and heading
def test_contextual_sections_carry_title_and_heading():
    doc = {
        "id": "test-sections",
        "title": "Firm review",
        "body": "## Tokyo\nRevenue rose. Costs fell.\n## London\nHiring paused.",
    }

    chunks = chunking.by_section(doc, max_words=2, contextual=True)

    assert [c["text"] for c in chunks] == [
        "Firm review > Tokyo\nRevenue rose.",
        "Firm review > Tokyo\nCosts fell.",
        "Firm review > London\nHiring paused.",
    ]


# test plain sections carry no heading
def test_plain_sections_carry_no_heading():
    doc = {
        "id": "test-sections",
        "title": "Firm review",
        "body": "## Tokyo\nRevenue rose. Costs fell.\n## London\nHiring paused.",
    }

    chunks = chunking.by_section(doc, max_words=2, contextual=False)

    assert [c["text"] for c in chunks] == [
        "Revenue rose.",
        "Costs fell.",
        "Hiring paused.",
    ]
