from fastapi import APIRouter
from pydantic import BaseModel, Field

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentQuestion(BaseModel):
    alert_id: str = Field(min_length=1)
    question: str = Field(min_length=1)
