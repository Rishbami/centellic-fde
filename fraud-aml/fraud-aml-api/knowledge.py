"""Embedding operations for AML knowledge retrieval."""

import math
import os

import voyageai
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL")

voyage = voyageai.Client(
    api_key=os.environ["VOYAGE_API_KEY"],
    max_retries=3,
    timeout=3,
)


def embed_texts(texts: list[str], input_type: str) -> tuple[list[list[float]]]:
    # embed a batch
    # input_type: tells Voyage whether these are docs or a query
    result = voyage.embed(texts=texts, model=EMBED_MODEL, input_type=input_type)

    # returns the vectors and token count (can see cost)
    return result.embeddings, result.total_tokens
