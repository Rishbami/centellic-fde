# embed_texts... is imported, not rewiritten
# the embedding provider has not changed... only where the vectors get stored

import knowledge
import chunk_index
import hybrid

# out chose strategy
CHUNK_STRATEGY = "sections_contextual"

SEARCH_MODE = "hybrid"


def count() -> int:
    return chunk_index.collection_for(CHUNK_STRATEGY).count()


def build_index() -> int:
    """Chunk and ambed the corups... Free if nothing has changed snce the last build."""
    return chunk_index.build(CHUNK_STRATEGY)["embedding_tokens"]


def search(question: str, top_k: int = 3) -> list[dict]:
    """Embed the question and let Chroma do the storing."""
    if count() == 0:
        raise RuntimeError("Index is empty, call POST /knowedlge/ask/index first")
    query_vectors, _ = knowledge.embed_texts([question], input_type="query")
    if SEARCH_MODE == "hybrid":
        return hybrid.search_with_vector(
            CHUNK_STRATEGY, question, query_vectors[0], top_k
        )

    return chunk_index.search_with_vectors(CHUNK_STRATEGY, query_vectors, k=top_k)[0]
