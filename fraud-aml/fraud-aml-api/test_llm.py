from types import SimpleNamespace

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


def test_provider_rate_limit_becomes_429(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from routers.insights import router

    def rate_limited(alert, account):
        raise anthropic.RateLimitError(
            "Provider rate limit reached",
            response=httpx.Response(
                429,
                request=httpx.Request("POST", "https://example.test/messages"),
            ),
            body=None,
        )

    monkeypatch.setattr(llm, "summarise_alert", rate_limited)
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        response = client.post("/alerts/ALT-048/summary")

    assert response.status_code == 429
    assert response.json() == {"detail": "LLM rate limit exceeded"}


@pytest.mark.parametrize("failure", ["connection", "authentication", "server"])
def test_provider_failure_becomes_502(monkeypatch, failure):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from routers.insights import router

    def provider_failure(alert, account):
        request = httpx.Request("POST", "https://example.test/messages")
        message = "Private provider diagnostic"
        if failure == "connection":
            raise anthropic.APIConnectionError(message=message, request=request)
        error_type, status = (
            (anthropic.AuthenticationError, 401)
            if failure == "authentication" else (anthropic.InternalServerError, 500)
        )
        raise error_type(
            message,
            response=httpx.Response(status, request=request),
            body={"error": {"message": message}},
        )

    monkeypatch.setattr(llm, "summarise_alert", provider_failure)
    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        response = client.post("/alerts/ALT-048/summary")

    assert response.status_code == 502
    assert response.json() == {"detail": "LLM provider unavailable"}


def test_estimate_does_not_generate_a_summary(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from routers.insights import router

    estimate_calls = []

    def fake_estimate(alert, account):
        estimate_calls.append((alert["alert_id"], account["account_id"]))
        return 137

    def unexpected_generation(*args, **kwargs):
        pytest.fail("Token estimation must not generate a summary")

    monkeypatch.setattr(llm, "estimate_input_tokens", fake_estimate)
    monkeypatch.setattr(llm, "MODEL", "test-model")
    monkeypatch.setattr(llm, "summarise_alert", unexpected_generation)
    monkeypatch.setattr(llm.client.messages, "create", unexpected_generation)

    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        response = client.get("/alerts/ALT-048/summary/estimate")

    assert response.status_code == 200
    assert response.json() == {
        "alert_id": "ALT-048",
        "estimated_input_tokens": 137,
        "model": "test-model",
    }
    assert estimate_calls == [("ALT-048", "ACC-016")]


def test_stream_returns_summary_text(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from routers.insights import router

    stream_calls = []

    def fake_stream(alert, account):
        stream_calls.append((alert["alert_id"], account["account_id"]))
        return iter(["High-volume ", "payments flagged ", "for review."])

    monkeypatch.setattr(llm, "stream_alert_summary", fake_stream)
    app = FastAPI()
    app.include_router(router)
    with (
        TestClient(app) as client,
        client.stream("GET", "/alerts/ALT-048/summary/stream") as response,
    ):
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/plain")
        body = "".join(response.iter_text())

    assert body == "High-volume payments flagged for review."
    assert stream_calls == [("ALT-048", "ACC-016")]


def test_summarise_alert_sends_context_and_returns_usage(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from data import ACCOUNTS, ALERTS

    alert = next(a for a in ALERTS if a["alert_id"] == "ALT-048")
    account = next(a for a in ACCOUNTS if a["account_id"] == alert["account_id"])
    calls = []

    def fake_create(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(text="High-volume payments need review.")],
            usage=SimpleNamespace(input_tokens=120, output_tokens=95),
            stop_reason="end_turn",
        )

    monkeypatch.setattr(llm, "MODEL", "test-model")
    monkeypatch.setattr(llm.client.messages, "create", fake_create)

    result = llm.summarise_alert(alert, account)

    assert result == {
        "alert_id": "ALT-048",
        "account_id": "ACC-016",
        "summary": "High-volume payments need review.",
        "input_tokens": 120,
        "output_tokens": 95,
        "stop_reason": "end_turn",
    }
    assert len(calls) == 1
    assert calls[0]["model"] == "test-model"
    assert calls[0]["system"] == llm.SYSTEM_PROMPT
    assert calls[0]["max_tokens"] == 500
    assert len(calls[0]["messages"]) == 1
    assert calls[0]["messages"][0]["role"] == "user"
    prompt = calls[0]["messages"][0]["content"]
    assert f"Alert ID: {alert['alert_id']}" in prompt
    assert f"Amount (currency not provided): {alert['amount']}" in prompt
    assert f"Payment corridor: {alert['corridor']}" in prompt
    assert f"Rule triggered: {alert['rule_triggered']}" in prompt
    assert f"Counterparty: {alert['counterparty']}" in prompt
    assert f"Account ID: {account['account_id']}" in prompt
    assert f"Account holder: {account['account_holder_name']}" in prompt
    assert f"Account balance (currency not provided): {account['balance']}" in prompt


def test_estimate_input_tokens_counts_context_without_generation(monkeypatch):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    import llm
    from data import ACCOUNTS, ALERTS

    alert = next(a for a in ALERTS if a["alert_id"] == "ALT-048")
    account = next(a for a in ACCOUNTS if a["account_id"] == alert["account_id"])
    calls = []

    def fake_count_tokens(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(input_tokens=137)

    def unexpected_generation(*args, **kwargs):
        pytest.fail("Token counting must not generate a response")

    monkeypatch.setattr(llm, "MODEL", "test-model")
    monkeypatch.setattr(llm.client.messages, "count_tokens", fake_count_tokens)
    monkeypatch.setattr(llm.client.messages, "create", unexpected_generation)
    monkeypatch.setattr(llm.client.messages, "stream", unexpected_generation)

    result = llm.estimate_input_tokens(alert, account)

    assert result == 137
    assert len(calls) == 1
    assert calls[0]["model"] == "test-model"
    assert calls[0]["system"] == llm.SYSTEM_PROMPT
    assert len(calls[0]["messages"]) == 1
    assert calls[0]["messages"][0]["role"] == "user"
    prompt = calls[0]["messages"][0]["content"]
    assert f"Alert ID: {alert['alert_id']}" in prompt
    assert f"Account ID: {account['account_id']}" in prompt
    assert f"Counterparty: {alert['counterparty']}" in prompt
