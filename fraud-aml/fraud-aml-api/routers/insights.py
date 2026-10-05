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
