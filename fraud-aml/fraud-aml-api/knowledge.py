"""Embedding operations for AML knowledge retrieval."""

import math
import os

import voyageai
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL")
