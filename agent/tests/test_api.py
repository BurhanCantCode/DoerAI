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


def test_plan_simulate_returns_risk() -> None:
    payload = {
        "schema_version": 1,
        "session_id": "session-3",
        "transcript": "open Safari and go to openai.com",
        "app": {"name": "Finder"},
    }
    response = client.post("/v1/plan/simulate", json=payload)
    assert response.status_code == 200
    body = response.json()
    assert body["session_id"] == "session-3"
    assert "risk_level" in body
    assert body["proposed_actions_count"] >= 1


def test_models_endpoint() -> None:
    response = client.get("/v1/models")
    assert response.status_code == 200
    body = response.json()
    assert body["schema_version"] == 1
    assert isinstance(body["routing"], list)
    assert isinstance(body["feature_flags"], dict)


def test_telemetry_round_trip() -> None:
    event = {
        "session_id": "session-t1",
        "stage": "executing",
        "status": "success",
        "latency_ms": 123,
    }
    post_response = client.post("/v1/telemetry", json=event)
    assert post_response.status_code == 200
    assert post_response.json()["status"] == "accepted"

    get_response = client.get("/v1/telemetry?limit=1")
    assert get_response.status_code == 200
    body = get_response.json()
    assert len(body["events"]) == 1
    assert body["events"][0]["session_id"] == "session-t1"
