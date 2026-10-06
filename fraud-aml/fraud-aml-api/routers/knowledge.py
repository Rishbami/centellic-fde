from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from anthropic import APIStatusError, APITimeoutError, RateLimitError
import knowledge_store as knowledge
import llm
import os
from dotenv import load_dotenv

load_dotenv()


router = APIRouter(prefix="/knowledge", tags=["knowledge"])

RELEVANCE_FLOOR = float(os.getenv("RELEVANCE_FLOOR", "0.35"))


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


@router.post("/ask")
def ask(q: Question):
    try:
        hits = knowledge.search(q.question, q.top_k)
    except RuntimeError as e:
        raise HTTPException(status_code=409, detail=str(e))

    usable = [hit for hit in hits if hit["score"] >= RELEVANCE_FLOOR]

    if not usable:
        return {
            "question": q.question,
            "answer": None,
            "refused": True,
            "reason": "No document in the corpus is relevant to that question.",
            "sources": [],
        }

    context = "\n\n".join(f"[{h['id']}] {h['title']}\n{h['text']}" for h in usable)

    try:
        result = llm.answer_from_context(q.question, context)
    except RateLimitError:
        raise HTTPException(
            status_code=429, detail="Answer provider rate limit exceeded"
        )
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="Answer provider timed out")
    except APIStatusError:
        raise HTTPException(status_code=502, detail="Answer provider unavailable")

    return {
        "question": q.question,
        "answer": result["answer"],
        "refused": False,
        "sources": [
            {"id": h["id"], "title": h["title"], "score": round(h["score"], 3)}
            for h in usable
        ],
        "input_tokens": result["input_tokens"],
        "output_tokens": result["output_tokens"],
    }
