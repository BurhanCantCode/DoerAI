from __future__ import annotations

from core.config import SCHEMA_VERSION_CURRENT
from core.event_bus import EventBus
from core.schemas import Action, ActionPlan, PlanRequest, StreamEvent
from macos_use_adapter.adapter import MacOSUseAdapter


RISKY_ACTIONS = {"run_applescript"}
RISKY_KEY_COMBOS = {"enter"}


class PlannerService:
    def __init__(self, event_bus: EventBus, adapter: MacOSUseAdapter | None = None) -> None:
        self._event_bus = event_bus
        self._adapter = adapter or MacOSUseAdapter()

    async def plan(self, request: PlanRequest) -> ActionPlan:
        await self._event_bus.publish(
            StreamEvent(
                session_id=request.session_id,
                event="planning_started",
                message="Planning actions from transcript",
                progress=10,
            )
        )

        adapter_result = await self._adapter.plan_actions(
            transcript=request.transcript,
            active_app_name=(request.app.name if request.app else None),
            _ax_tree_summary=request.ax_tree_summary,
        )

        await self._event_bus.publish(
            StreamEvent(
                session_id=request.session_id,
                event="planning_generated",
                message=f"Generated {len(adapter_result.actions)} actions",
                progress=65,
            )
        )

        risk_level, requires_confirmation = self._compute_risk(adapter_result.actions)

        plan = ActionPlan(
            schema_version=SCHEMA_VERSION_CURRENT,
            session_id=request.session_id,
            actions=adapter_result.actions,
            confidence=adapter_result.confidence,
            risk_level=risk_level,
            requires_confirmation=requires_confirmation,
            summary=adapter_result.summary,
        )

        await self._event_bus.publish(
            StreamEvent(
                session_id=request.session_id,
                event="planning_completed",
                message="Plan ready",
                progress=100,
            )
        )
        return plan

    @staticmethod
    def _compute_risk(actions: list[Action]) -> tuple[str, bool]:
        high = False
        medium = False
        for action in actions:
            if action.destructive:
                high = True
                continue
            if action.kind in RISKY_ACTIONS:
                high = True
                continue
            if action.kind == "key_combo" and (action.key_combo or "").lower() in RISKY_KEY_COMBOS:
                medium = True

        if high:
            return "high", True
        if medium:
            return "medium", True
        return "low", False
