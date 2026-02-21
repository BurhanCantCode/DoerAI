from __future__ import annotations

import json

from fastapi import FastAPI
from fastapi.responses import JSONResponse, StreamingResponse

from core.event_bus import EventBus
from core.planner_service import PlannerService
from core.schemas import PlanRequest, VerifyRequest
from core.verifier_service import VerifierService


app = FastAPI(title="Orange Sidecar", version="0.1.0")

_event_bus = EventBus()
_planner = PlannerService(_event_bus)
_verifier = VerifierService()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/plan")
async def plan(request: PlanRequest) -> JSONResponse:
    plan_result = await _planner.plan(request)
    return JSONResponse(plan_result.model_dump(mode="json"))


@app.post("/v1/verify")
async def verify(request: VerifyRequest) -> JSONResponse:
    result = await _verifier.verify(request)
    return JSONResponse(result.model_dump(mode="json"))


@app.get("/v1/events/{session_id}")
async def events(session_id: str) -> StreamingResponse:
    async def stream() -> str:
        async for event in _event_bus.subscribe(session_id):
            payload = json.dumps(event.model_dump(mode="json"))
            yield f"event: {event.event}\ndata: {payload}\n\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
