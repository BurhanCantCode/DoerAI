from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .config import SCHEMA_VERSION_CURRENT, SCHEMA_VERSION_MIN


ActionKind = Literal[
    "click",
    "type",
    "key_combo",
    "scroll",
    "open_app",
    "run_applescript",
    "select_menu_item",
    "wait",
]
RiskLevel = Literal["low", "medium", "high"]
ExecutionStatus = Literal["success", "failure", "partial"]


class AppMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    bundle_id: str | None = None
    window_title: str | None = None
    url: str | None = None


class PlannerPreferences(BaseModel):
    model_config = ConfigDict(extra="forbid")

    preferred_model: str | None = None
    locale: str | None = None
    low_latency: bool = True


class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    kind: ActionKind
    target: str | None = None
    text: str | None = None
    key_combo: str | None = None
    app_bundle_id: str | None = None
    timeout_ms: int = Field(default=3000, ge=100, le=120000)
    destructive: bool = False
    expected_outcome: str | None = None


class ActionPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = SCHEMA_VERSION_CURRENT
    session_id: str = Field(min_length=1)
    actions: list[Action] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)
    risk_level: RiskLevel
    requires_confirmation: bool
    summary: str | None = None


class PlanRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = SCHEMA_VERSION_CURRENT
    session_id: str = Field(min_length=1)
    transcript: str = Field(min_length=1, max_length=4000)
    screenshot_base64: str | None = None
    ax_tree_summary: str | None = None
    app: AppMetadata | None = None
    preferences: PlannerPreferences | None = None

    @field_validator("schema_version")
    @classmethod
    def schema_version_supported(cls, value: int) -> int:
        if value < SCHEMA_VERSION_MIN or value > SCHEMA_VERSION_CURRENT:
            raise ValueError(
                f"Unsupported schema_version={value}; supported=[{SCHEMA_VERSION_MIN}, {SCHEMA_VERSION_CURRENT}]"
            )
        return value


class VerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = SCHEMA_VERSION_CURRENT
    session_id: str = Field(min_length=1)
    action_plan: ActionPlan
    execution_result: ExecutionStatus
    reason: str | None = None
    before_context: str | None = None
    after_context: str | None = None

    @field_validator("schema_version")
    @classmethod
    def schema_version_supported(cls, value: int) -> int:
        if value < SCHEMA_VERSION_MIN or value > SCHEMA_VERSION_CURRENT:
            raise ValueError(
                f"Unsupported schema_version={value}; supported=[{SCHEMA_VERSION_MIN}, {SCHEMA_VERSION_CURRENT}]"
            )
        return value


class VerifyResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: int = SCHEMA_VERSION_CURRENT
    session_id: str
    status: Literal["success", "failure"]
    confidence: float = Field(ge=0.0, le=1.0)
    reason: str | None = None
    corrective_actions: list[Action] = Field(default_factory=list)


class StreamEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    event: str
    message: str
    progress: int | None = Field(default=None, ge=0, le=100)
