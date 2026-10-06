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
