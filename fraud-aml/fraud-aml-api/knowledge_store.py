"""Persistent Chroma storage and retrieval operations."""

import chromadb
from documents import DOCUMENTS
from knowledge import embed_texts

chroma = chromadb.PersistentClient(path="./chroma_store")
