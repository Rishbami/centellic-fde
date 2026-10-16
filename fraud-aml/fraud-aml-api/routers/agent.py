from fastapi import APIRouter
from pydantic import BaseModel, Field

import llm
from routers.alerts import get_alert_or_404
from routers.accounts import get_account_or_404
from routers.insights import handle_llm_errors

router = APIRouter(prefix="/agent", tags=["agent"])


class AgentQuestion(BaseModel):
    alert_id: str = Field(min_length=1)
    question: str = Field(min_length=1)


@router.post("/ask")
def ask(request: AgentQuestion):
    alert = get_alert_or_404(request.alert_id)
    account = get_account_or_404(alert["account_id"])

    with handle_llm_errors():
        return llm.review_with_similar_alerts(
            alert,
            account,
            request.question,
        )
