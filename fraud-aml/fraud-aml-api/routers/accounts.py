from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from data import ACCOUNTS
from models.account import AccountStatus


router = APIRouter(prefix="/accounts", tags=["accounts"])


class NewAccount(BaseModel):
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    status: AccountStatus


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
