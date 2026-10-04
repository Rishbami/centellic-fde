from fastapi import APIRouter, Depends, HTTPException

from data import ALERTS
from models import Alert


router = APIRouter(prefix="/alerts", tags=["alerts"])


def get_alert_or_404(alert_id: str) -> dict:
    for alert in ALERTS:
        if alert["alert_id"] == alert_id:
            return alert
    raise HTTPException(status_code=404, detail="Alert not found")
