"""Account API models."""

from typing import Literal

from pydantic import BaseModel, Field


AccountStatus = Literal["active", "under_review", "restricted"]


class Account(BaseModel):
    account_id: str
    account_holder_name: str = Field(min_length=1)
    balance: float = Field(ge=0)
    country: str = Field(pattern=r"^[A-Z]{2}$")  # e.g., "US", "GB", "FR"
    status: AccountStatus
