from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
import sys

from core.config import settings
from core.schemas import Action


@dataclass
class AdapterResult:
    actions: list[Action]
    confidence: float
    summary: str


class MacOSUseAdapter:
    """
    Adapter boundary for vendored macOS-use.

    For now this layer reuses upstream prompt primitives (SystemPrompt) and
    provides deterministic action planning heuristics as a safe baseline.
    """

    def __init__(self) -> None:
        self._vendor_loaded = False
        self._important_rules = ""
        self._load_vendor_prompt_rules()

    def _load_vendor_prompt_rules(self) -> None:
        vendor_path = settings.vendor_macos_use
        if not vendor_path.exists():
            return

        sys.path.insert(0, str(vendor_path))
        try:
            from mlx_use.agent.prompts import SystemPrompt  # type: ignore

            prompt = SystemPrompt(
                action_description=(
                    "open_app, click, type, key_combo, scroll, run_applescript, select_menu_item, wait"
                ),
                current_date=datetime.now(),
                max_actions_per_step=4,
            )
            self._important_rules = prompt.important_rules()
            self._vendor_loaded = True
        except Exception:
            self._important_rules = self._load_rules_from_source(vendor_path)
            self._vendor_loaded = bool(self._important_rules)
        finally:
            if str(vendor_path) in sys.path:
                sys.path.remove(str(vendor_path))

    @staticmethod
    def _load_rules_from_source(vendor_path: Path) -> str:
        """
        Parse upstream prompts.py as a dependency-light fallback.

        This keeps Orange aligned with macOS-use guidance even when optional
        upstream runtime dependencies are unavailable in local environments.
        """
        prompt_file = vendor_path / "mlx_use" / "agent" / "prompts.py"
        if not prompt_file.exists():
            return ""

        content = prompt_file.read_text(encoding="utf-8")
        match = re.search(
            r"def important_rules\\(self\\) -> str:\\n\\s+\"\"\".*?\"\"\"\\n\\s+text = \"\"\"(.*?)\"\"\"",
            content,
            flags=re.DOTALL,
        )
        if not match:
            return ""
        return match.group(1).strip()

    async def plan_actions(
        self,
        *,
        transcript: str,
        active_app_name: str | None,
        _ax_tree_summary: str | None,
    ) -> AdapterResult:
        text = transcript.strip().lower()
        app_name = (active_app_name or "").strip()

        if text.startswith("open "):
            target = transcript.strip()[5:].strip()
            return AdapterResult(
                actions=[
                    Action(
                        id="a1",
                        kind="open_app",
                        target=target,
                        expected_outcome=f"{target} is frontmost",
                    )
                ],
                confidence=0.92,
                summary=f"Open {target}",
            )

        url_match = re.search(r"(https?://\S+|\b\w+\.com\b)", text)
        if "go to" in text and url_match:
            raw_url = url_match.group(1)
            url = raw_url if raw_url.startswith("http") else f"https://{raw_url}"
            browser_target = app_name if app_name in {"Safari", "Google Chrome"} else "Safari"
            return AdapterResult(
                actions=[
                    Action(id="a1", kind="open_app", target=browser_target, expected_outcome="Browser opened"),
                    Action(id="a2", kind="key_combo", key_combo="cmd+l", expected_outcome="Address bar focused"),
                    Action(id="a3", kind="type", text=url, expected_outcome=f"URL entered: {url}"),
                    Action(id="a4", kind="key_combo", key_combo="enter", expected_outcome="Page loads"),
                ],
                confidence=0.86,
                summary=f"Navigate to {url}",
            )

        if "reply" in text and "slack" in text:
            response_text = self._extract_reply_text(transcript) or "I'll be there."
            return AdapterResult(
                actions=[
                    Action(id="a1", kind="click", target="Last message thread", expected_outcome="Thread selected"),
                    Action(id="a2", kind="click", target="Message composer", expected_outcome="Input focused"),
                    Action(id="a3", kind="type", text=response_text, expected_outcome="Reply text entered"),
                    Action(
                        id="a4",
                        kind="key_combo",
                        key_combo="enter",
                        destructive=True,
                        expected_outcome="Message sent",
                    ),
                ],
                confidence=0.78,
                summary="Reply in Slack thread",
            )

        # Safe default that keeps control deterministic and auditable.
        return AdapterResult(
            actions=[
                Action(
                    id="a1",
                    kind="type",
                    text=transcript,
                    expected_outcome="Transcript typed in focused input",
                )
            ],
            confidence=0.6,
            summary="Type transcript in focused field",
        )

    @staticmethod
    def _extract_reply_text(transcript: str) -> str | None:
        patterns = [r"saying\s+(.+)$", r"reply\s+(.+)$"]
        for pattern in patterns:
            match = re.search(pattern, transcript, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip().strip('"')
        return None

    @property
    def vendor_loaded(self) -> bool:
        return self._vendor_loaded

    @property
    def vendor_rules(self) -> str:
        return self._important_rules
