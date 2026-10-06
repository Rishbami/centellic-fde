from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from anthropic import APIStatusError, APITimeoutError, RateLimitError
import knowledge_store as knowledge
import llm


router = APIRouter(prefix="/knowledge", tags=["knowledge"])


# Create class (question) using base model w 2 field (quesstion and top_k)
class Question(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, gt=0, le=8)


@router.post("/index")
def rebuild_index():
    """Embed the corpus. Costs tokens... so it is deliberate POST, rather than automatic."""
    tokens = knowledge.build_index()
    return {"indexed": knowledge.count(), "embedding_tokens": tokens}
