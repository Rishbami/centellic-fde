import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture
def knowledge_client(monkeypatch, tmp_path):
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key-not-real")
    monkeypatch.setenv("VOYAGE_API_KEY", "test-key-not-real")
    monkeypatch.setenv("ANONYMIZED_TELEMETRY", "False")
    # The storage module opens its database at import time, relative to cwd.
    monkeypatch.chdir(tmp_path)
    import knowledge_store as knowledge
    from routers.knowledge import router

    app = FastAPI()
    app.include_router(router)
    with TestClient(app) as client:
        yield client, knowledge


def test_search_returns_ranked_hits_without_generation(monkeypatch, knowledge_client):
    import llm

    client, knowledge = knowledge_client
    question = "What checks apply to a sanctions name match?"
    hits = [
        {
            "id": "doc-001",
            "title": "Sanctions screening procedure",
            "text": "Verify identifying details before escalating a name match.",
            "score": 0.85,
        },
        {
            "id": "doc-002",
            "title": "Investigation records",
            "text": "Record the evidence considered during review.",
            "score": 0.62,
        },
    ]
    calls = []

    def fake_search(query, top_k):
        calls.append((query, top_k))
        return hits

    def unexpected_generation(*args, **kwargs):
        pytest.fail("Search-only requests must not generate an answer")

    monkeypatch.setattr(knowledge, "search", fake_search)
    monkeypatch.setattr(llm, "answer_from_context", unexpected_generation)
    monkeypatch.setattr(llm.client.messages, "create", unexpected_generation)

    response = client.post(
        "/knowledge/search", json={"question": question, "top_k": 2}
    )

    assert response.status_code == 200
    assert response.json() == {"question": question, "results": hits}
    assert calls == [(question, 2)]
