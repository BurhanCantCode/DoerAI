from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_plan_returns_actions() -> None:
    payload = {
        "schema_version": 1,
        "session_id": "session-1",
        "transcript": "open Safari",
        "app": {"name": "Finder", "bundle_id": "com.apple.finder"},
    }
    response = client.post("/v1/plan", json=payload)
    assert response.status_code == 200

    body = response.json()
    assert body["session_id"] == "session-1"
    assert body["actions"]
    assert body["actions"][0]["kind"] == "open_app"


def test_verify_failure_returns_corrective_action() -> None:
    plan = {
        "schema_version": 1,
        "session_id": "session-2",
        "actions": [
            {
                "id": "a1",
                "kind": "click",
                "target": "Send button",
                "timeout_ms": 3000,
                "destructive": False,
            }
        ],
        "confidence": 0.8,
        "risk_level": "medium",
        "requires_confirmation": True,
    }
    payload = {
        "schema_version": 1,
        "session_id": "session-2",
        "action_plan": plan,
        "execution_result": "failure",
        "reason": "Element not found",
    }

    response = client.post("/v1/verify", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "failure"
    assert len(body["corrective_actions"]) == 1
