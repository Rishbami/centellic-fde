"""Analyst API models."""

from typing import Literal

from pydantic import BaseModel, Field


AnalystStatus = Literal["active", "away", "inactive"]


class Analyst(BaseModel):
    analyst_id: str
    name: str = Field(min_length=1)
    team: str = Field(min_length=1)
    status: AnalystStatus
