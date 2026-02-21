from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import hmac
import json
import os
import time
from typing import Any

import httpx
import jwt
from fastapi import FastAPI, Header, HTTPException, Request, status
from pydantic import BaseModel, ConfigDict, EmailStr, Field

app = FastAPI(title="Orange Backend API", version="0.2.0")

FREE_COMMAND_LIMIT = 300
PRO_COMMAND_LIMIT = 10_000_000
STRIPE_SIGNATURE_TOLERANCE_SECONDS = 300


def _csv_env(name: str) -> set[str]:
    raw = os.getenv(name, "")
    return {item.strip().lower() for item in raw.split(",") if item.strip()}


ALLOWED_BETA_EMAILS = _csv_env("ORANGE_BETA_ALLOWLIST_EMAILS")
ALLOWED_BETA_TOKENS = _csv_env("ORANGE_BETA_ALLOWLIST_TOKENS")

USAGE_EVENTS: list["UsageIngestRequest"] = []
WAITLIST_SIGNUPS: list["WaitlistSignupRequest"] = []
TELEMETRY_EVENTS: list["SessionTelemetryEvent"] = []
USER_PLAN_BY_ID: dict[str, str] = {}
USER_EMAIL_BY_ID: dict[str, str] = {}
STRIPE_CUSTOMER_TO_USER: dict[str, str] = {}
PROCESSED_STRIPE_EVENTS: set[str] = set()

JWKS_CACHE_KEYS: list[dict[str, Any]] | None = None
JWKS_CACHE_EXPIRY: float = 0


class AuthTokenRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(min_length=20)
    invite_token: str | None = None


class AuthTokenResponse(BaseModel):
    user_id: str
    email: EmailStr
    plan: str
    beta_access: bool
    issued_at: str


class UsageIngestRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: str
    session_id: str
    command_text: str | None = None
    status: str
    latency_ms: int | None = Field(default=None, ge=0)
    app: str | None = None
    created_at: str = Field(default_factory=lambda: datetime.now(tz=timezone.utc).isoformat())


class UsageResponse(BaseModel):
    user_id: str
    plan: str
    period: str
    commands_used: int
    command_limit: int
    remaining: int
    can_execute: bool


class SessionTelemetryEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    session_id: str
    timestamp: str = Field(default_factory=lambda: datetime.now(tz=timezone.utc).isoformat())
    stage: str
    app: str | None = None
    action_kind: str | None = None
    status: str
    latency_ms: int | None = Field(default=None, ge=0)
    error_code: str | None = None


class WaitlistSignupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    full_name: str | None = None
    source: str = "website"
    created_at: str = Field(default_factory=lambda: datetime.now(tz=timezone.utc).isoformat())


class WaitlistSignupResponse(BaseModel):
    status: str
    beta_access: bool
    beta_token: str | None = None


class BetaInviteClaimRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    invite_token: str


class BetaInviteClaimResponse(BaseModel):
    status: str
    beta_token: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/auth/token", response_model=AuthTokenResponse)
def issue_token(request: AuthTokenRequest) -> AuthTokenResponse:
    claims = _decode_supabase_access_token(request.access_token)
    user_id = str(claims.get("sub") or "").strip()
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token subject")

    email = _extract_email(claims)
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing email")

    if not _has_beta_access(email=email, invite_token=request.invite_token):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is not in the private beta allowlist",
        )

    USER_EMAIL_BY_ID[user_id] = email
    plan = USER_PLAN_BY_ID.get(user_id, "free")

    return AuthTokenResponse(
        user_id=user_id,
        email=email,
        plan=plan,
        beta_access=True,
        issued_at=datetime.now(tz=timezone.utc).isoformat(),
    )


@app.post("/usage/ingest")
def usage_ingest(event: UsageIngestRequest) -> dict[str, int | str]:
    USAGE_EVENTS.append(event)
    if len(USAGE_EVENTS) > 50_000:
        del USAGE_EVENTS[:5_000]
    return {"status": "accepted", "count": len(USAGE_EVENTS)}


@app.post("/telemetry/ingest")
def telemetry_ingest(event: SessionTelemetryEvent) -> dict[str, int | str]:
    TELEMETRY_EVENTS.append(event)
    if len(TELEMETRY_EVENTS) > 50_000:
        del TELEMETRY_EVENTS[:5_000]
    return {"status": "accepted", "count": len(TELEMETRY_EVENTS)}


@app.get("/telemetry")
def telemetry_recent(limit: int = 100) -> dict[str, list[dict[str, Any]]]:
    safe_limit = max(1, min(limit, 1000))
    return {
        "events": [item.model_dump(mode="json") for item in TELEMETRY_EVENTS[-safe_limit:]],
    }


@app.get("/usage/current", response_model=UsageResponse)
def usage_current(user_id: str) -> UsageResponse:
    plan = USER_PLAN_BY_ID.get(user_id, "free")
    current_period = datetime.now(tz=timezone.utc).strftime("%Y-%m")
    used = sum(1 for event in USAGE_EVENTS if event.user_id == user_id and event.created_at.startswith(current_period))
    limit = PRO_COMMAND_LIMIT if plan == "pro" else FREE_COMMAND_LIMIT
    remaining = max(0, limit - used)
    can_execute = remaining > 0
    return UsageResponse(
        user_id=user_id,
        plan=plan,
        period=current_period,
        commands_used=used,
        command_limit=limit,
        remaining=remaining,
        can_execute=can_execute,
    )


@app.post("/stripe/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str | None = Header(default=None, alias="stripe-signature"),
) -> dict[str, str]:
    payload = await request.body()
    secret = os.getenv("STRIPE_WEBHOOK_SECRET", "").strip()
    if not secret:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Webhook secret not configured")
    if not stripe_signature:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing stripe-signature header")
    if not _verify_stripe_signature(payload, stripe_signature, secret):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook signature")

    event = json.loads(payload.decode("utf-8"))
    event_id = str(event.get("id") or "")
    if event_id in PROCESSED_STRIPE_EVENTS:
        return {"status": "duplicate"}
    PROCESSED_STRIPE_EVENTS.add(event_id)

    event_type = str(event.get("type") or "")
    data_object = event.get("data", {}).get("object", {})
    if event_type.startswith("customer.subscription."):
        _handle_subscription_event(data_object)

    return {"status": "accepted"}


@app.post("/beta/waitlist", response_model=WaitlistSignupResponse)
def beta_waitlist(signup: WaitlistSignupRequest) -> WaitlistSignupResponse:
    WAITLIST_SIGNUPS.append(signup)
    beta_access = _has_beta_access(email=signup.email, invite_token=None)
    beta_token = _mint_beta_token(signup.email) if beta_access else None
    return WaitlistSignupResponse(status="accepted", beta_access=beta_access, beta_token=beta_token)


@app.post("/beta/invite/claim", response_model=BetaInviteClaimResponse)
def beta_claim_invite(request: BetaInviteClaimRequest) -> BetaInviteClaimResponse:
    invite = request.invite_token.strip().lower()
    if invite not in ALLOWED_BETA_TOKENS and request.email.lower() not in ALLOWED_BETA_EMAILS:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid invite token")
    return BetaInviteClaimResponse(status="ok", beta_token=_mint_beta_token(request.email))


def _has_beta_access(email: str, invite_token: str | None) -> bool:
    if not ALLOWED_BETA_EMAILS and not ALLOWED_BETA_TOKENS:
        return True
    normalized_email = email.strip().lower()
    normalized_token = (invite_token or "").strip().lower()
    return normalized_email in ALLOWED_BETA_EMAILS or normalized_token in ALLOWED_BETA_TOKENS


def _mint_beta_token(email: str) -> str:
    secret = os.getenv("ORANGE_BETA_TOKEN_SECRET", "orange-beta-secret")
    payload = f"{email.lower()}:{secret}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"beta_{digest[:32]}"


def _handle_subscription_event(data_object: dict[str, Any]) -> None:
    customer_id = str(data_object.get("customer") or "").strip()
    status_value = str(data_object.get("status") or "").strip().lower()
    metadata = data_object.get("metadata", {}) or {}
    user_id = str(metadata.get("user_id") or metadata.get("supabase_user_id") or "").strip()
    if customer_id and user_id:
        STRIPE_CUSTOMER_TO_USER[customer_id] = user_id
    if not user_id and customer_id:
        user_id = STRIPE_CUSTOMER_TO_USER.get(customer_id, "")
    if not user_id:
        return
    USER_PLAN_BY_ID[user_id] = "pro" if status_value in {"active", "trialing"} else "free"


def _verify_stripe_signature(payload: bytes, header: str, secret: str) -> bool:
    signature_parts = {}
    for part in header.split(","):
        if "=" in part:
            key, value = part.split("=", 1)
            signature_parts[key.strip()] = value.strip()
    timestamp = signature_parts.get("t")
    signature = signature_parts.get("v1")
    if not timestamp or not signature:
        return False

    try:
        ts_int = int(timestamp)
    except ValueError:
        return False

    if abs(time.time() - ts_int) > STRIPE_SIGNATURE_TOLERANCE_SECONDS:
        return False

    signed_payload = f"{timestamp}.{payload.decode('utf-8')}".encode("utf-8")
    expected = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


def _decode_supabase_access_token(access_token: str) -> dict[str, Any]:
    audience = os.getenv("SUPABASE_JWT_AUDIENCE", "authenticated").strip()
    issuer = os.getenv("SUPABASE_JWT_ISSUER", "").strip() or None
    jwt_secret = os.getenv("SUPABASE_JWT_SECRET", "").strip()

    try:
        if jwt_secret:
            return jwt.decode(
                access_token,
                jwt_secret,
                algorithms=["HS256"],
                audience=audience if audience else None,
                issuer=issuer,
                options={"verify_aud": bool(audience), "verify_iss": bool(issuer)},
            )

        signing_key = _resolve_jwks_signing_key(access_token)
        return jwt.decode(
            access_token,
            signing_key,
            algorithms=["RS256"],
            audience=audience if audience else None,
            issuer=issuer,
            options={"verify_aud": bool(audience), "verify_iss": bool(issuer)},
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token validation failed: {exc}") from exc


def _resolve_jwks_signing_key(access_token: str) -> Any:
    jwks_url = os.getenv("SUPABASE_JWKS_URL", "").strip()
    if not jwks_url:
        supabase_url = os.getenv("SUPABASE_URL", "").strip()
        if supabase_url:
            jwks_url = f"{supabase_url.rstrip('/')}/auth/v1/.well-known/jwks.json"
    if not jwks_url:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Missing SUPABASE_JWKS_URL")

    header = jwt.get_unverified_header(access_token)
    kid = header.get("kid")
    if not kid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing kid")
    jwk = _fetch_jwk_for_kid(jwks_url, kid)
    if not jwk:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Signing key not found")
    return jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))


def _fetch_jwk_for_kid(jwks_url: str, kid: str) -> dict[str, Any] | None:
    global JWKS_CACHE_EXPIRY
    global JWKS_CACHE_KEYS

    now = time.time()
    if JWKS_CACHE_KEYS is None or now >= JWKS_CACHE_EXPIRY:
        try:
            with httpx.Client(timeout=4.0) as client:
                response = client.get(jwks_url)
                response.raise_for_status()
                payload = response.json()
                JWKS_CACHE_KEYS = payload.get("keys", [])
                JWKS_CACHE_EXPIRY = now + 600
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Unable to fetch Supabase JWKS: {exc}",
            ) from exc

    for key in JWKS_CACHE_KEYS or []:
        if key.get("kid") == kid:
            return key
    return None


def _extract_email(claims: dict[str, Any]) -> str | None:
    email = claims.get("email")
    if isinstance(email, str) and email.strip():
        return email.strip().lower()
    user_meta = claims.get("user_metadata", {})
    if isinstance(user_meta, dict):
        email = user_meta.get("email")
        if isinstance(email, str) and email.strip():
            return email.strip().lower()
    return None
