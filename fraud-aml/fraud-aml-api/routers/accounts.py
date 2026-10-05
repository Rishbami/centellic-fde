from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from data import ACCOUNTS
from models.account import AccountStatus


router = APIRouter(prefix="/accounts", tags=["accounts"])


class NewAccount(BaseModel):
    account_holder_name: str = Field(min_length=1)
    balance: float = Field(ge=0)
    country: str = Field(pattern=r"^[A-Z]{2}$")
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


@router.post("", status_code=201)
def add_account(new: NewAccount):
    new_number = (
        max(int(account["account_id"].split("-")[1]) for account in ACCOUNTS) + 1
    )

    account = {
        "account_id": f"ACC-{new_number:03d}",
        "account_holder_name": new.account_holder_name,
        "balance": new.balance,
        "country": new.country,
        "status": new.status,
    }

    ACCOUNTS.append(account)
    return account


@router.put("/{account_id}")
def update_account(
    updated: NewAccount,
    account: dict = Depends(get_account_or_404),
):
    account.update(updated.model_dump())
    return account
