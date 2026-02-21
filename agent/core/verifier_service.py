from __future__ import annotations

from core.config import SCHEMA_VERSION_CURRENT
from core.schemas import VerifyRequest, VerifyResponse


class VerifierService:
    """Deterministic verifier baseline with corrective hints."""

    async def verify(self, request: VerifyRequest) -> VerifyResponse:
        if request.execution_result == "success":
            return VerifyResponse(
                schema_version=SCHEMA_VERSION_CURRENT,
                session_id=request.session_id,
                status="success",
                confidence=0.9,
                reason="Execution reported success",
                corrective_actions=[],
            )

        corrective_actions = []
        if request.execution_result in {"failure", "partial"} and request.action_plan.actions:
            failed_action = request.action_plan.actions[-1]
            corrective_actions.append(failed_action.model_copy(update={"id": "retry_1"}))

        return VerifyResponse(
            schema_version=SCHEMA_VERSION_CURRENT,
            session_id=request.session_id,
            status="failure",
            confidence=0.55,
            reason=request.reason or "Execution did not complete successfully",
            corrective_actions=corrective_actions,
        )
