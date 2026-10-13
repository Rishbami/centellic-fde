# embed_texts... is imported, not rewiritten
# the embedding provider has not changed... only where the vectors get stored

import knowledge
import chunk_index

# out chose strategy
CHUNK_STRATEGY = "sections_contexual"


def count() -> int:
    return chunk_index.collection_for(CHUNK_STRATEGY)


def build_index() -> int:
    """Chunk and ambed the corups... Free if nothing has changed snce the last build."""
    return chunk_index.build(CHUNK_STRATEGY)["embedding_tokens"]


def search(question: str, top_k: int = 3) -> list[dict]:
    """Embed the question and let Chroma do the storing."""
    if count() == 0:
        raise RuntimeError("Index is empty, call POST /knowedlge/ask/index first")
    query_vectors, _ = knowledge.embed_texts([question], input_type="query")

    return chunk_index.search_with_vectors(CHUNK_STRATEGY, query_vectors, k=top_k)[0]
