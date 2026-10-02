from fastapi import APIRouter, Depends, HTTPException

from data import ACCOUNTS
from models import Account


router = APIRouter(prefix="/accounts", tags=["accounts"])


def get_account_or_404(account_id: str) -> dict:
    for account in ACCOUNTS:
        if account["account_id"] == account_id:
            return account
    raise HTTPException(status_code=404, detail="Account not found")


@router.get("")
def list_accounts():
    return ACCOUNTS


@router.get("/{account_id}")
def get_account(account: dict = Depends(get_account_or_404)):
    return account
