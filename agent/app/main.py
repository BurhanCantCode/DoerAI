from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

from core.event_bus import EventBus
from core.planner_service import PlannerService
from core.schemas import PlanRequest, PlanSimulationRequest, TelemetryEvent, VerifyRequest
from core.verifier_service import VerifierService


app = FastAPI(title="Orange Sidecar", version="0.1.0")

_event_bus = EventBus()
_planner = PlannerService(_event_bus)
_verifier = VerifierService()
_telemetry_events: list[TelemetryEvent] = []


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/plan")
async def plan(request: PlanRequest) -> JSONResponse:
    plan_result = await _planner.plan(request)
    return JSONResponse(plan_result.model_dump(mode="json"))


@app.post("/v1/plan/simulate")
async def plan_simulate(request: PlanSimulationRequest) -> JSONResponse:
    simulation = await _planner.simulate(request)
    return JSONResponse(simulation.model_dump(mode="json"))


@app.get("/v1/models")
async def models() -> JSONResponse:
    payload = _planner.models()
    return JSONResponse(payload.model_dump(mode="json"))


@app.post("/v1/verify")
async def verify(request: VerifyRequest) -> JSONResponse:
    result = await _verifier.verify(request)
    return JSONResponse(result.model_dump(mode="json"))


@app.post("/v1/telemetry")
async def telemetry(event: TelemetryEvent) -> JSONResponse:
    _telemetry_events.append(event)
    if len(_telemetry_events) > 5_000:
        del _telemetry_events[:1_000]
    return JSONResponse({"status": "accepted", "count": len(_telemetry_events)})


@app.get("/v1/telemetry")
async def telemetry_recent(limit: int = 100) -> JSONResponse:
    safe_limit = max(1, min(limit, 1000))
    recent = _telemetry_events[-safe_limit:]
    return JSONResponse({"events": [e.model_dump(mode="json") for e in recent]})


@app.get("/v1/events/{session_id}")
async def events(session_id: str) -> StreamingResponse:
    async def stream() -> str:
        async for event in _event_bus.subscribe(session_id):
            payload = json.dumps(event.model_dump(mode="json"))
            yield f"event: {event.event}\ndata: {payload}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
