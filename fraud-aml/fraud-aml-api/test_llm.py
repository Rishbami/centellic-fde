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
