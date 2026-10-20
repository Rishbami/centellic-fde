import importlib
import json
from datetime import datetime

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from data import ACCOUNTS, ALERTS


class FakeToolUseBlock:
    type = "tool_use"
    name = "find_similar_alerts"

    def __init__(self, tool_id, input_):
        self.id = tool_id
        self.input = input_


class FakeUsage:
    input_tokens = 100
    output_tokens = 15


class FakeResponse:
    def __init__(self, content, stop_reason):
        self.usage = FakeUsage()
        self.content = content
        self.stop_reason = stop_reason


class FakeTextBlock:
    type = "text"

    def __init__(self, text):
        self.text = text


def test_agent_stops_at_max_iterations_instead_of_looping_forever(monkeypatch):
    # Client construction needs a key, but all model calls below are replaced.
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    llm = importlib.import_module("llm")
    model_calls = []
    tool_calls = []

    def fake_create(**kwargs):
        model_calls.append(kwargs)
        return FakeResponse(
            [FakeToolUseBlock(f"toolu-{len(model_calls)}", {"limit": 2})],
            "tool_use",
        )

    def fake_find_similar_alerts(alert, limit):
        tool_calls.append((alert["alert_id"], limit))
        return [{"alert_id": "HISTORICAL-001", "review_outcome": "escalated"}]

    monkeypatch.setattr(llm.client.messages, "create", fake_create)
    monkeypatch.setattr(llm, "find_similar_alerts", fake_find_similar_alerts)

    alert = next(a for a in ALERTS if a["alert_id"] == "ALT-048")
    account = next(a for a in ACCOUNTS if a["account_id"] == alert["account_id"])

    with pytest.raises(RuntimeError, match="maximum number of rounds"):
        llm.review_with_similar_alerts(alert, account)

    assert len(model_calls) == 5
    assert tool_calls == [("ALT-048", 2)] * 5


def test_agent_returns_assessment_after_sending_tool_evidence(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    llm = importlib.import_module("llm")
    alert = next(a for a in ALERTS if a["alert_id"] == "ALT-048")
    account = next(a for a in ACCOUNTS if a["account_id"] == alert["account_id"])
    evidence = [
        {
            "alert_id": "HISTORICAL-001",
            "review_outcome": "closed_false_positive",
            "same_corridor": True,
            "amount_difference": 15400,
        }
    ]
    assessment = "Historical cases support further review by the analyst."
    tool_request = FakeToolUseBlock("toolu-01", {"limit": 2})
    model_calls = []
    tool_calls = []

    def fake_create(**kwargs):
        model_calls.append(kwargs)
        if len(model_calls) == 1:
            return FakeResponse([tool_request], "tool_use")

        assert len(model_calls) == 2
        messages = kwargs["messages"]
        assert messages[-2] == {
            "role": "assistant",
            "content": [tool_request],
        }
        assert messages[-1]["role"] == "user"
        results = messages[-1]["content"]
        assert len(results) == 1
        assert results[0]["type"] == "tool_result"
        assert results[0]["tool_use_id"] == tool_request.id
        assert json.loads(results[0]["content"]) == evidence
        return FakeResponse([FakeTextBlock(assessment)], "end_turn")

    def fake_find_similar_alerts(current_alert, limit):
        tool_calls.append((current_alert, limit))
        return evidence

    monkeypatch.setattr(llm.client.messages, "create", fake_create)
    monkeypatch.setattr(llm, "find_similar_alerts", fake_find_similar_alerts)

    result = llm.review_with_similar_alerts(alert, account)

    assert tool_calls == [(alert, 2)]
    assert len(model_calls) == 2
    assert result == {
        "alert_id": "ALT-048",
        "assessment": assessment,
        "tool_calls_made": 1,
        "input_tokens": 200,
        "output_tokens": 30,
    }


def test_agent_can_review_alert_after_assignment_updates_timestamp(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    llm = importlib.import_module("llm")
    from routers import agent, alerts

    alert = dict(next(a for a in ALERTS if a["alert_id"] == "ALT-048"))
    monkeypatch.setattr(alerts, "ALERTS", [alert])
    prompts = []

    def fake_create(**kwargs):
        prompts.append(kwargs["messages"][0]["content"])
        return FakeResponse([FakeTextBlock("Assessment after assignment.")], "end_turn")

    monkeypatch.setattr(llm.client.messages, "create", fake_create)
    app = FastAPI()
    app.include_router(alerts.router)
    app.include_router(agent.router)

    with TestClient(app) as client:
        payload = {key: value for key, value in alert.items() if key != "alert_id"}
        payload.update(analyst_id="ANL-001", status="under_review")
        response = client.put("/alerts/ALT-048", json=payload)
        assert response.status_code == 200
        assert isinstance(alert["created_at"], datetime)

        response = client.post(
            "/agent/ask",
            json={
                "alert_id": "ALT-048",
                "question": "Compare this assigned alert with historical cases.",
            },
        )

    assert response.status_code == 200
    assert response.json()["assessment"] == "Assessment after assignment."
    assert alert["created_at"].isoformat() in prompts[0]
    assert isinstance(alert["created_at"], datetime)
