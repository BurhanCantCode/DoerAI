from __future__ import annotations

import hashlib
import hmac
import json
from pathlib import Path
import sys
import time

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from api.app import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_usage_ingest_and_current() -> None:
    payload = {
        "user_id": "user-1",
        "session_id": "session-1",
        "command_text": "open safari",
        "status": "success",
        "latency_ms": 900,
        "app": "Safari",
        "created_at": "2026-02-21T00:00:00+00:00",
    }
    ingest = client.post("/usage/ingest", json=payload)
    assert ingest.status_code == 200
    usage = client.get("/usage/current", params={"user_id": "user-1"})
    assert usage.status_code == 200
    body = usage.json()
    assert body["user_id"] == "user-1"
    assert body["commands_used"] >= 1


def test_waitlist_capture() -> None:
    response = client.post(
        "/beta/waitlist",
        json={"email": "beta-user@example.com", "full_name": "Beta User", "source": "website"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "accepted"
    assert "beta_access" in body


def test_stripe_webhook_signature_validation(monkeypatch) -> None:
    secret = "whsec_test"
    monkeypatch.setenv("STRIPE_WEBHOOK_SECRET", secret)
    payload_obj = {
        "id": "evt_1",
        "type": "customer.subscription.updated",
        "data": {"object": {"customer": "cus_1", "status": "active", "metadata": {"user_id": "user-2"}}},
    }
    payload = json.dumps(payload_obj)

    timestamp = str(int(time.time()))
    signed_payload = f"{timestamp}.{payload}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    header = f"t={timestamp},v1={signature}"

    response = client.post(
        "/stripe/webhook",
        data=payload,
        headers={"stripe-signature": header, "content-type": "application/json"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
