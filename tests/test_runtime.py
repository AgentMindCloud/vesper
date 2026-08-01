"""Tests for Vesper runtime entrypoints."""

import os
import pytest

from vesper.runtime import (
    check_kill_switch,
    validate_env,
    start_voice_session,
    handle_turn,
    update_presence,
)
from vesper.memory import MemoryStore


def test_kill_switch_clear(monkeypatch):
    monkeypatch.delenv("VESPER_DISABLED", raising=False)
    check_kill_switch()  # should not raise


def test_kill_switch_engaged(monkeypatch):
    monkeypatch.setenv("VESPER_DISABLED", "1")
    with pytest.raises(RuntimeError, match="kill switch"):
        check_kill_switch()


def test_validate_env_missing(monkeypatch):
    for key in ("XAI_API_KEY", "X_BEARER_TOKEN", "GROK_VOICE_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    with pytest.raises(EnvironmentError, match="Missing"):
        validate_env()


def test_validate_env_ok(monkeypatch):
    monkeypatch.setenv("XAI_API_KEY", "xai-testkey123456")
    monkeypatch.setenv("X_BEARER_TOKEN", "AAAAAAAAAAAAAAAAAAAAAtesttoken")
    monkeypatch.setenv("GROK_VOICE_API_KEY", "xai-testkey123456")
    found = validate_env()
    assert "XAI_API_KEY" in found


def test_start_voice_session(monkeypatch):
    monkeypatch.delenv("VESPER_DISABLED", raising=False)
    result = start_voice_session("user-42", mode="proactive")
    assert result["status"] == "session_started"
    assert result["user_id"] == "user-42"
    assert result["mode"] == "proactive"
    assert result["swarm"] == "vesper-presence-swarm"


def test_handle_turn_returns_contracts(monkeypatch):
    monkeypatch.delenv("VESPER_DISABLED", raising=False)
    store = MemoryStore()
    store.write(
        {
            "content": "Test preference",
            "source": "user_said",
            "confidence": 0.95,
            "scope": "session",
            "retention_days": 0,
            "write_permission": "user_only",
            "created_at": "2026-08-01T00:00:00Z",
            "last_accessed": "2026-08-01T00:00:00Z",
        }
    )
    result = handle_turn("sess-1", "hello", store=store)
    assert result["session_id"] == "sess-1"
    assert "memory_contracts" in result
    assert result["action"] == "coordinator_delegates"


def test_update_presence_valid():
    result = update_presence("thoughtful", "thinking", 0.8)
    assert result["expression"] == "thoughtful"
    assert result["status"] == "thinking"
    assert result["intensity"] == 0.8


def test_update_presence_clamps_invalid():
    result = update_presence("invalid_expr", "bad_status", 2.5)
    assert result["expression"] == "neutral"
    assert result["status"] == "idle"
    assert result["intensity"] == 1.0
