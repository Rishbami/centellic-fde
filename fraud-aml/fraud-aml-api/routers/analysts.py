from fastapi import APIRouter, Depends, HTTPException

from data import ANALYSTS
from models import Analyst


router = APIRouter(prefix="/analysts", tags=["analysts"])


def get_analyst_or_404(account_id: str) -> dict:
    for account in ACCOUNTS:
        if account["account_id"] == account_id:
            return account
    raise HTTPException(status_code=404, detail="Account not found")


@router.get("")
def list_analysts():
    return ANALYSTS


@router.get("/{analyst_id}")
def get_analyst(analyst: dict = Depends(get_analyst_or_404)):
    return analyst
