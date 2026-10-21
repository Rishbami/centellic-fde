import anthropic
import httpx
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_summary_returns_text_and_usage(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from routers.insights import router

    fake_summary = {
        "alert_id": "ALT-048",
        "account_id": "ACC-016",
        "summary": "High-volume payments flagged for analyst review.",
        "input_tokens": 120,
        "output_tokens": 95,
        "stop_reason": "end_turn",
    }
    monkeypatch.setattr(
        llm, "summarise_alert", lambda alert, account: fake_summary
    )

    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        response = client.post("/alerts/ALT-048/summary")

    assert response.status_code == 200
    assert response.json() == fake_summary


def test_summary_receives_correct_alert_and_account(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from data import ACCOUNTS, ALERTS
    from routers.insights import router

    expected_alert = next(a for a in ALERTS if a["alert_id"] == "ALT-048")
    expected_account = next(
        a for a in ACCOUNTS if a["account_id"] == expected_alert["account_id"]
    )
    calls = []

    def fake_summary(alert, account):
        calls.append((alert, account))
        return {"summary": "Summary for the selected alert."}

    monkeypatch.setattr(llm, "summarise_alert", fake_summary)
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        response = client.post("/alerts/ALT-048/summary")

    assert response.status_code == 200
    assert len(calls) == 1
    assert calls[0][0] is expected_alert
    assert calls[0][1] is expected_account


@pytest.mark.parametrize(
    "missing_record, expected_detail",
    [("alert", "Alert not found"), ("account", "Account not found")],
)
def test_missing_summary_context_returns_404_without_provider_work(
    monkeypatch, missing_record, expected_detail
):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from routers import accounts, alerts
    from routers.insights import router

    monkeypatch.setattr(
        alerts, "ALERTS",
        [] if missing_record == "alert" else [
            {"alert_id": "ALT-048", "account_id": "ACC-016"}
        ],
    )
    monkeypatch.setattr(accounts, "ACCOUNTS", [])

    def unexpected_summary(alert, account):
        pytest.fail("Summary generation must not run when context is missing")

    monkeypatch.setattr(llm, "summarise_alert", unexpected_summary)
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        response = client.post("/alerts/ALT-048/summary")

    assert response.status_code == 404
    assert response.json() == {"detail": expected_detail}


def test_provider_timeout_becomes_504(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from routers.insights import router

    def timeout(alert, account):
        raise anthropic.APITimeoutError(
            request=httpx.Request("POST", "https://example.test/messages")
        )

    monkeypatch.setattr(llm, "summarise_alert", timeout)
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        response = client.post("/alerts/ALT-048/summary")

    assert response.status_code == 504
    assert response.json() == {"detail": "LLM request timed out"}
