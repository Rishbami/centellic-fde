from contextlib import contextmanager
from itertools import chain

from anthropic import (
    APIConnectionError,
    APIStatusError,
    APITimeoutError,
    RateLimitError,
)
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

import llm
from routers.accounts import get_account_or_404
from routers.alerts import get_alert_or_404

router = APIRouter(prefix="/alerts", tags=["insights"])


def get_alert_context(
    alert: dict = Depends(get_alert_or_404),
) -> tuple[dict, dict]:
    account = get_account_or_404(alert["account_id"])
    return alert, account


@contextmanager
def handle_llm_errors():
    try:
        yield
    except RateLimitError as exc:
        raise HTTPException(status_code=429, detail="LLM rate limit exceeded") from exc
    except APITimeoutError as exc:
        raise HTTPException(status_code=504, detail="LLM request timed out") from exc
    except (APIConnectionError, APIStatusError) as exc:
        raise HTTPException(status_code=502, detail="LLM provider unavailable") from exc


@router.post("/{alert_id}/summary")
def summarise_alert(
    context: tuple[dict, dict] = Depends(get_alert_context),
):
    alert, account = context
    with handle_llm_errors():
        return llm.summarise_alert(alert, account)


@router.get("/{alert_id}/summary/estimate")
def estimate_summary(
    context: tuple[dict, dict] = Depends(get_alert_context),
):
    alert, account = context
    with handle_llm_errors():
        return {
            "alert_id": alert["alert_id"],
            "estimated_input_tokens": llm.estimate_input_tokens(alert, account),
            "model": llm.MODEL,
        }
