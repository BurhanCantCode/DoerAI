from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path


SCHEMA_VERSION_CURRENT = 1
SCHEMA_VERSION_MIN = 0


@dataclass(frozen=True)
class Settings:
    host: str = os.getenv("ORANGE_SIDECAR_HOST", "127.0.0.1")
    port: int = int(os.getenv("ORANGE_SIDECAR_PORT", "7789"))
    model_simple: str = os.getenv("ORANGE_MODEL_SIMPLE", "gpt-4o-mini")
    model_complex: str = os.getenv("ORANGE_MODEL_COMPLEX", "gpt-4o")
    enable_remote_llm: bool = os.getenv("ORANGE_ENABLE_REMOTE_LLM", "0") == "1"

    @property
    def repo_root(self) -> Path:
        return Path(__file__).resolve().parents[2]

    @property
    def vendor_macos_use(self) -> Path:
        return self.repo_root / "vendor" / "macos-use"


settings = Settings()
