"""
Chucking strategies
Every strategy takes a document and returns a list of chunks.

A chunck i a dict:
    - id           "<doc id>#<two-digit-number>, kept stable for the same input
    - doc_id       the parent document, used for citations
    - title        the parent documents title
    - text         exactly what gets embedded and what the model will read

"""

import re


def _chunk(doc: dict, number: int, text: str) -> dict:
    # 2 -> 02
    return {
        "id": f"{doc['id']}#{number:02d}",
        "doc_id": doc["id"],
        "title": doc["title"],
        "text": text,
    }


def split_sentences(text: str) -> list[str]:
    """Sentences, with each '## Heading' line kept as a unit of its own"""
    units = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("## "):
            units.append(line)
        else:
            units.extend(s for s in re.split(r"(?<=[.!?])\s+", line) if s)
    return units


def pack(units: list[str], max_words: int) -> list[str]:
    """Join whole units until adding the next one would pass max_words"""
    # groups holds finished chunks, current is the chunk being built, count is its word total
    groups, current, count = [], [], 0
    for unit in units:
        n = len(unit.split())
        if current and count + n > max_words:
            groups.append(" ".join(current))
            current, count = [], 0
        current.append(unit)
        count += n
    if current:
        groups.append(" ".join(current))
    return groups


# --------------------------- CHUNKING STRATEGIES ----------------------------


# whole document
def whole_document(doc: dict) -> list[dict]:
    """Baseline... what our project has done until now."""
    return [_chunk(doc, 0, doc["body"].strip())]


# fixed_words
def fixed_words(doc: dict, size: int = 100, overlap: int = 0) -> list[dict]:
    """Every 'size' words, regardless of sentences or section. Cheap and blind"""
    if not 0 <= overlap < size:
        raise ValueError("overlap must be at least 0 AND smaller than size.")
    words = doc["body"].split()
    step = size - overlap
    chunks = []

    # range(0, 385, 75)
    for number, start in enumerate(range(0, len(words), step)):
        chunks.append(_chunk(doc, number, " ".join(words[start : start + size])))
        if start + size >= len(words):
            break
    return chunks


# sentenced_packed
def sentenced_packed(doc: dict, max_words: int = 100) -> list[dict]:
    """Whole sentences only, packed up to max_words. Never cuts a sentence in half."""
    units = split_sentences(doc["body"])
    groups = pack(units, max_words)

    return [_chunk(doc, number, text) for number, text in enumerate(groups)]


# by_section
def by_section(doc: dict, max_words: int = 150, contextual: bool = True) -> list[dict]:
    """
    One chunk per '## ' section... long sentences are packed by section
    contextual = True prefixes each chnk with "Document title> Section Heading", so a chunk that never names its subject still carries it into the embedding.

    ## Tokyo

    """

    chunks, number = [], 0
    parts = (
        re.split(r"(?m)^## ", doc["body"]) if "## " in doc["body"] else [doc["body"]]
    )
    for part in parts:
        heading, _, text = (
            part.partition("\n") if "## " in doc["body"] else ("", "", part)
        )
        heading, text = heading.strip(), text.strip()
        if not text:
            continue

        for piece in pack(split_sentences(text), max_words):
            if contextual:
                prefix = (
                    f"{doc['title']} > {heading}\n" if heading else f"{doc['title']}\n"
                )
                piece = prefix + piece
            chunks.append(_chunk(doc, number, piece))
            number += 1
    return chunks


STRATEGIES = {
    "whole_document": whole_document,
    "fixed_100": lambda d: fixed_words(d, size=100, overlap=0),
    "fixed_overlap_25": lambda d: fixed_words(d, size=100, overlap=25),
    "sentences_100": lambda d: sentenced_packed(d, max_words=100),
    "sections_plain": lambda d: by_section(d, max_words=150, contextual=False),
    "sections_contextual": lambda d: by_section(d, max_words=150, contextual=True),
}


def chunk_corpus(docs: list[dict], strategy: str) -> list[dict]:
    return [chunk for doc in docs for chunk in STRATEGIES[strategy](doc)]


# import chunking, corpus, documents

# combine old and new docs

# loop through and call chunk_corpus
