"""Alert API models."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


AlertStatus = Literal[
    "unassigned",
    "under_review",
    "reviewed",
]

ReviewOutcome = Literal[
    "escalated",
    "information_requested",
    "closed_false_positive",
]


class Alert(BaseModel):
    alert_id: str
    account_id: str
    analyst_id: str | None = None
    amount: float = Field(gt=0)
    corridor: str = Field(pattern=r"^[A-Z]{2}->[A-Z]{2}$")
    rule_triggered: str = Field(min_length=1)
    risk_score: int = Field(ge=0, le=100)
    status: AlertStatus
    counterparty: str = Field(min_length=1)
    created_at: datetime
    review_outcome: ReviewOutcome | None = None
