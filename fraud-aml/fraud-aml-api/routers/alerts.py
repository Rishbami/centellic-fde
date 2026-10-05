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


@router.post("", status_code=201)
def add_alert(new: NewAlert):
    new_number = max(int(alert["alert_id"].split("-")[1]) for alert in ALERTS) + 1

    alert = {
        "alert_id": f"ALERT-{new_number:03d}",
        "account_id": new.account_id,
        "analyst_id": new.analyst_id,
        "amount": new.amount,
        "corridor": new.corridor,
        "rule_triggered": new.rule_triggered,
        "risk_score": new.risk_score,
        "status": new.status,
        "counterparty": new.counterparty,
        "created_at": new.created_at,
        "review_outcome": new.review_outcome,
    }

    ALERTS.append(alert)
    return alert


@router.put("/{alert_id}")
def update_alert(
    updated: NewAlert,
    alert: dict = Depends(get_alert_or_404),
):
    alert.update(updated.model_dump())
    return alert


@router.delete("/{alert_id}")
def delete_alert(
    alert: dict = Depends(get_alert_or_404),
):
    ALERTS.remove(alert)
    return alert
