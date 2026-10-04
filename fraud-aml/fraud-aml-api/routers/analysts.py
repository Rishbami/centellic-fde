from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from data import ANALYSTS
from models.analyst import AnalystStatus


router = APIRouter(prefix="/analysts", tags=["analysts"])


class NewAnalyst(BaseModel):
    name: str = Field(min_length=1)
    team: str = Field(min_length=1)
    status: AnalystStatus


def get_analyst_or_404(analyst_id: str) -> dict:
    for analyst in ANALYSTS:
        if analyst["analyst_id"] == analyst_id:
            return analyst
    raise HTTPException(status_code=404, detail="Analyst not found")


@router.get("")
def list_analysts():
    return ANALYSTS


@router.get("/{analyst_id}")
def get_analyst(analyst: dict = Depends(get_analyst_or_404)):
    return analyst


@router.post("", status_code=201)
def add_analyst(new: NewAnalyst):
    new_number = (
        max(int(analyst["analyst_id"].split("-")[1]) for analyst in ANALYSTS) + 1
    )

    analyst = {
        "analyst_id": f"ANL-{new_number:03d}",
        "name": new.name,
        "team": new.team,
        "status": new.status,
    }

    ANALYSTS.append(analyst)
    return analyst


@router.put("/{analyst_id}")
def update_analyst(
    updated: NewAnalyst,
    analyst: dict = Depends(get_analyst_or_404),
):
    analyst.update(updated.model_dump())
    return analyst
