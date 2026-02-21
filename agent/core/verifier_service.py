from __future__ import annotations

from difflib import SequenceMatcher

from core.config import SCHEMA_VERSION_CURRENT
from core.schemas import VerifyRequest, VerifyResponse


class VerifierService:
    """Deterministic verifier baseline with corrective hints."""

    async def verify(self, request: VerifyRequest) -> VerifyResponse:
        before_context = (request.before_context or "").strip()
        after_context = (request.after_context or "").strip()
        delta_score = self._context_delta(before_context, after_context)

        if request.execution_result == "success" and delta_score >= 0.01:
            return VerifyResponse(
                schema_version=SCHEMA_VERSION_CURRENT,
                session_id=request.session_id,
                status="success",
                confidence=0.9 if delta_score > 0.05 else 0.75,
                reason=f"Execution reported success with context delta {delta_score:.2f}",
                corrective_actions=[],
            )

        corrective_actions = []
        if request.execution_result in {"failure", "partial"} and request.action_plan.actions:
            failed_action = request.action_plan.actions[-1]
            corrective_actions.append(failed_action.model_copy(update={"id": "retry_1"}))
        elif request.execution_result == "success" and request.action_plan.actions:
            # Report a conservative retry when no observable context change is detected.
            corrective_actions.append(request.action_plan.actions[-1].model_copy(update={"id": "retry_verify_1"}))

        return VerifyResponse(
            schema_version=SCHEMA_VERSION_CURRENT,
            session_id=request.session_id,
            status="failure",
            confidence=0.55 if request.execution_result != "success" else 0.45,
            reason=request.reason or self._default_failure_reason(request.execution_result, delta_score),
            corrective_actions=corrective_actions,
        )

    @staticmethod
    def _context_delta(before: str, after: str) -> float:
        if not before and not after:
            return 0.0
        if before and not after:
            return 0.0
        if not before and after:
            return 1.0
        ratio = SequenceMatcher(a=before, b=after).ratio()
        return max(0.0, 1.0 - ratio)

    @staticmethod
    def _default_failure_reason(execution_result: str, delta_score: float) -> str:
        if execution_result == "success":
            return f"No meaningful UI/context delta detected after success report ({delta_score:.2f})"
        return "Execution did not complete successfully"
