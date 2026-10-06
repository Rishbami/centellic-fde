"""Persistent Chroma storage and retrieval operations."""

import chromadb
from documents import DOCUMENTS
from knowledge import embed_texts

chroma = chromadb.PersistentClient(path="./chroma_store")

collection = chroma.get_or_create_collection(
    name="aml_documents",
    # HNSW (Hierarchical Navigable Small World)
    configuration={"hnsw": {"space": "cosine"}},
)


def build_index() -> int:
    """Embed every document and hand the vectors to Chroma."""
    texts = [doc["content"] for doc in DOCUMENTS]
    vectors, tokens = embed_texts(texts, input_type="document")

    collection.upsert(
        ids=[doc["document_id"] for doc in DOCUMENTS],
        embeddings=vectors,
        documents=texts,
        metadatas=[
            {"title": doc["title"], "type": doc["document_type"]} for doc in DOCUMENTS
        ],
    )

    return tokens


def search(question: str, top_k: int = 3) -> list[dict]:
    """Embed the question and let Chroma do the storing."""
    query_vectors, _ = embed_texts([question], input_type="query")

    result = collection.query(query_embeddings=query_vectors, n_results=top_k)

    return [
        {
            "id": doc_id,
            "title": metadata["title"],
            "text": text,
            # Chroma will give us back distance... lower is closer...
            # we will do (1 - distance) in order to flip from return distance, to similarity
            "score": 1 - distance,
        }
        for doc_id, text, metadata, distance in zip(
            result["ids"][0],
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        )
    ]
