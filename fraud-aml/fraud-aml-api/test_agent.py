import importlib

import pytest

from data import ACCOUNTS, ALERTS


class FakeToolUseBlock:
    type = "tool_use"
    name = "find_similar_alerts"

    def __init__(self, tool_id, input_):
        self.id = tool_id
        self.input = input_


class FakeResponse:
    def __init__(self, content, stop_reason):
        self.content = content
        self.stop_reason = stop_reason


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
    account = next(
        a for a in ACCOUNTS if a["account_id"] == alert["account_id"]
    )

    with pytest.raises(RuntimeError, match="maximum number of rounds"):
        llm.review_with_similar_alerts(alert, account)

    assert len(model_calls) == 5
    assert tool_calls == [("ALT-048", 2)] * 5
