"""Minimal runtime entry for Vesper.

This module provides the xlOS / grok-install compatible entry points.
The real voice loop is driven by the YAML swarm + tools once the
Grok multi-agent runtime is available.
"""

from __future__ import annotations

import os
from typing import Any


def check_kill_switch() -> None:
    if os.getenv("VESPER_DISABLED") == "1":
        raise RuntimeError("Vesper kill switch engaged (VESPER_DISABLED=1)")


def start_voice_session(user_id: str, mode: str = "reactive") -> dict[str, Any]:
    """Start a new voice session (reactive or proactive)."""
    check_kill_switch()
    return {
        "status": "session_started",
        "user_id": user_id,
        "mode": mode,
        "swarm": "vesper-presence-swarm",
        "memory": "governed-contracts",
        "presence": "enabled",
    }


def handle_turn(session_id: str, transcript: str, x_context: list[dict] | None = None) -> dict[str, Any]:
    """Process one voice turn with optional live X context."""
    check_kill_switch()
    return {
        "session_id": session_id,
        "received": transcript[:120],
        "x_context_items": len(x_context or []),
        "action": "coordinator_delegates",
        "next": "memory_query + response + optional avatar update",
    }


def update_presence(expression: str, status: str, intensity: float = 0.7) -> dict[str, Any]:
    """Update the reactive visual presence."""
    return {
        "expression": expression,
        "status": status,
        "intensity": intensity,
        "avatar": "updated",
    }
