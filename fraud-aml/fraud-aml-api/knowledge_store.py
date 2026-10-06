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
