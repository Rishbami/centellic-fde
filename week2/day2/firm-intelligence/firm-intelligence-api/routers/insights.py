from anthropic import (
    APIStatusError,
    APITimeoutError,
    RateLimitError,
    APIConnectionError,
)
import knowledge
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from pydantic import ValidationError

import llm
from routers.firms import get_firm_or_404

router = APIRouter(prefix="/firms", tags=["insights"])

# Create a post endpoint for /firms/{firm_id}/summary
# it should take in a firm and find it (or not...)
# try to make the llm call to get a summary of the call
# if unsuccessful throw an appropriate error and status code


@router.post("/{firm_id}/summary")
def summarise_firm(firm: dict = Depends(get_firm_or_404)):
    try:
        return llm.summarise_firm(firm)
    except RateLimitError:
        raise HTTPException(status_code=429, detail="LLM rate limit exceeded")
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="LLM request timed out")
    except APIStatusError:
        raise HTTPException(status_code=502, detail="LLM request failed")


@router.get("/{firm_id}/summary/estimate")
def estimate(firm: dict = Depends(get_firm_or_404)):
    return {
        "id": firm["id"],
        "estimated_input_tokens": llm.estimate_input_tokens(firm),
        "model": llm.MODEL,
    }


@router.get("/{firm_id}/summary/stream")
def stream_summary(firm: dict = Depends(get_firm_or_404)):
    return StreamingResponse(
        llm.stream_firm_summary(firm),
        media_type="text/plain",
    )


# enpoint challenge
# post endpoint at firms/firm_id/analyis
# tries to analyse firm... if not, raise apropriate exception(s)
@router.post("/{firm_id}/analyse")
def firm_analysis(firm: dict = Depends(get_firm_or_404)):
    try:
        return llm.analyse_firm(firm)
    except RateLimitError:
        raise HTTPException(status_code=429, detail="LLM rate limit exceeded")
    except APITimeoutError:
        raise HTTPException(status_code=504, detail="LLM request timed out")
    except APIStatusError:
        raise HTTPException(status_code=502, detail="LLM request failed")
