"""
One chroma collection per chunking strategy... so that strategies can be compared side by side

Each collection remembers a "fingerprint" of the chunks and the embedding model that built it.
If either changes, the collection is rebuilt from scratch.
"""

import hashlib
import chromadb

import chunking
import knowledge
from corpus import CORPUS_DOCUMENTS
from documents import DOCUMENTS
import time

ALL_DOCUMENTS = DOCUMENTS + CORPUS_DOCUMENTS
BATCH_SIZE = (
    128  # Voyage's own guidance: batch documents to stay well inside rate limits
)

chroma = chromadb.PersistentClient(path="./chroma_store")


def collection_name(strategy: str) -> str:
    return f"chunks_{strategy}"


def collection_for(strategy: str):
    return chroma.get_or_create_collection(
        name=collection_name(strategy), configuration={"hnsw": {"space": "cosine"}}
    )


def embed_batched(texts: list[str], input_type: str) -> tuple[list[list[float]], int]:
    """Embed any number of texts in batches. Return all vectors and the total token count."""
    vectors: list[list[float]] = []
    tokens = 0

    for start in range(0, len(texts), BATCH_SIZE):
        batch_vectors, batch_tokens = knowledge.embed_texts(
            texts[start : start + BATCH_SIZE], input_type=input_type
        )
        vectors.extend(batch_vectors)
        tokens += batch_tokens

        print("Waiting 65 seconds for Voyage's rate limit...", flush=True)
        time.sleep(65)
    return vectors, tokens


def fingerprint(chunks: list[dict]) -> str:
    # SHA-256 - a reciept that turns any text into a fixed-length code
    digest = hashlib.sha256(knowledge.EMBED_MODEL.encode())
    for c in chunks:
        digest.update(f"{c['id']}\n{c['text']}\n".encode())
    return digest.hexdigest()[:16]


def build(strategy: str, force: bool = False) -> dict:
    """Make sure the strategy's collection matches the current corupus, chunker and model."""
    """Answers one q... is the index I already have still correct?"""
    # pt1
    chunks = chunking.chunk_corpus(ALL_DOCUMENTS, strategy)
    fp = fingerprint(chunks)
    col = collection_for(strategy)
    stored = col.get(limit=1, include=["metadatas"])["metadatas"]
    if (
        not force
        and col.count() == len(chunks)
        and stored
        and stored[0].get("fingerprint") == fp
    ):
        return {
            "strategy": strategy,
            "chunks": len(chunks),
            "embedding_tokens": 0,
            "rebuilt": False,
        }

    # pt2 - the rebuild
    try:
        chroma.delete_collection(collection_name(strategy))
    except Exception:
        pass

    col = collection_for(strategy)
    vectors, tokens = embed_batched([c["text"] for c in chunks], input_type="document")
    col.upsert(
        ids=[c["id"] for c in chunks],
        embeddings=vectors,
        documents=[c["text"] for c in chunks],
        metadatas=[
            {"doc_id": c["doc_id"], "title": c["title"], "fingerprint": fp}
            for c in chunks
        ],
    )
    return {
        "strategy": strategy,
        "chunks": len(chunks),
        "embedding_tokens": tokens,
        "rebuilt": True,
    }


# CURRENT -

# NEW FUNCTIONS ADDS - search_with_vectors
# the read side
# it takes question vectors that are already embedded, so questions are embedded once and reused across all 6 categories


def search_with_vectors(
    strategy: str,
    query_vectors: list[list[float]],
    k: int,
) -> list[list[dict]]:
    """
    We embed the question once, then searches many strategies with the same vectors.
    """

    col = collection_for(strategy)
    if col.count() == 0:
        raise RuntimeError(f"Index for '{strategy}' is empty, build it first.")

    # the search
    result = col.query(query_embeddings=query_vectors, n_results=min(k, col.count()))

    # what result looks like
    # - result["ids"] - a list of 2 lists, each holding 3 ids
    # - result["documents"] - a list of 2 lists, each holding 3 texts
    # - result["metadatas"] - a list of 2 lists, each holding 3 metadata dictionaries
    # - result["distances"] - a list of 2 lists, each holding 3 distances
    # e.g. ids                ["doc-001#00", "doc-101#01", "doc-107#00"]
    # e.g. distances          [0.375, 0.389, 0.30]

    return [
        # Chroma returns 4 parallel nested list
        [
            {
                "id": meta["doc_id"],
                "chunk_id": chunk_id,
                "title": meta["title"],
                "text": text,
                "score": 1 - distance,
            }
            for chunk_id, text, meta, distance in zip(ids, docs, metas, dists)
        ]
        for ids, docs, metas, dists in zip(
            result["ids"], result["documents"], result["metadatas"], result["distances"]
        )
    ]


"""
a chunk that only keyword search found has no cosine score... our relevance gate needs one
"""


def cosine_for(
    strategy: str, query_vector: list[float], chunk_ids: list[str]
) -> dict[str, float]:
    if not chunk_ids:
        return {}

    stored = collection_for(strategy).get(ids=chunk_ids, include=["embeddings"])

    return {
        chunk_id: float(knowledge.cosine_similarity(query_vector, list(vector)))
        for chunk_id, vector in zip(stored["ids"], stored["embeddings"])
    }


# where it fits in hybrid.py:
# vector search returns its top 10 with a cosine
# keyword search resturns its top 10
# RRF merges them
# any chunk in the keyword list but NOT in the vector list is passed to "cosine_for"
# now every hit has a cosine... so that gate works the same on all of them:
# score >= 0.45 orrrr exact_switch

# question mentions 3307
# chunk mentions 3307
