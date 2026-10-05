from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from data import ALERTS
from models.alert import AlertStatus, ReviewOutcome


router = APIRouter(prefix="/alerts", tags=["alerts"])


class NewAlert(BaseModel):
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


def get_alert_or_404(alert_id: str) -> dict:
    for alert in ALERTS:
        if alert["alert_id"] == alert_id:
            return alert
    raise HTTPException(status_code=404, detail="Alert not found")


@router.get("")
def list_alerts():
    return ALERTS


@router.get("/{alert_id}")
def get_alert(alert: dict = Depends(get_alert_or_404)):
    return alert
