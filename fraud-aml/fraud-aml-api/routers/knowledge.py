from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from anthropic import APIStatusError, APITimeoutError, RateLimitError
import knowledge_store as knowledge
import llm
import os
from dotenv import load_dotenv

load_dotenv()


router = APIRouter(prefix="/knowledge", tags=["knowledge"])

RELEVANCE_FLOOR = os.getenv("RELEVANCE_FLOOR")


# Create class (question) using base model w 2 field (quesstion and top_k)
class Question(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, gt=0, le=8)


@router.post("/index")
def rebuild_index():
    """Embed the corpus. Costs tokens... so it is deliberate POST, rather than automatic."""
    tokens = knowledge.build_index()
    return {"indexed": knowledge.count(), "embedding_tokens": tokens}


@router.post("/search")
def search(q: Question):
    """Retrieval only... no model call or generated text etc... only what was found"""
    try:
        return {
            "question": q.question,
            "results": knowledge.search(q.question, q.top_k),
        }
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e))
