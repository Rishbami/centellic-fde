from anthropic import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    RateLimitError,
)
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

import agent


router = APIRouter(prefix="/agent", tags=["agent"])


class AgentQuestion(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(min_length=1)


@router.post("/ask")
def ask(request: AgentQuestion):
    try:
        return agent.ask_with_tools(request.question)
    except APITimeoutError:
        raise HTTPException(
            status_code=504,
            detail="Agent provider timed out",
        )
    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail="Agent provider rate limit exceeded",
        )
    except (APIConnectionError, APIStatusError):
        raise HTTPException(
            status_code=502,
            detail="Agent provider unavailable",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Agent request failed",
        )
