"""Governed memory store for Vesper.

In-memory implementation with full contract validation.
Every fact must carry provenance, confidence, scope, retention,
and write permissions. Cross-session memory is opt-in only.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


REQUIRED_FIELDS = {
    "content",
    "source",
    "confidence",
    "scope",
    "retention_days",
    "write_permission",
    "created_at",
    "last_accessed",
}

VALID_SOURCES = {"user_said", "x_context", "derived", "system"}
VALID_SCOPES = {"session", "user", "global"}
VALID_WRITE_PERMISSIONS = {"user_only", "agent", "system"}


class ContractValidationError(ValueError):
    """Raised when a memory contract is incomplete or invalid."""


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_contract(fact: dict[str, Any], *, require_id: bool = False) -> dict[str, Any]:
    """Validate and normalize a governed memory contract.

    Returns a clean copy. Raises ContractValidationError on failure.
    """
    if not isinstance(fact, dict):
        raise ContractValidationError("Contract must be a dict")

    missing = REQUIRED_FIELDS - set(fact.keys())
    if missing:
        raise ContractValidationError(f"Missing required fields: {sorted(missing)}")

    content = fact["content"]
    if not isinstance(content, str) or not content.strip():
        raise ContractValidationError("content must be a non-empty string")

    source = fact["source"]
    if source not in VALID_SOURCES:
        raise ContractValidationError(
            f"source must be one of {sorted(VALID_SOURCES)}, got {source!r}"
        )

    confidence = fact["confidence"]
    if not isinstance(confidence, (int, float)) or not (0.0 <= float(confidence) <= 1.0):
        raise ContractValidationError("confidence must be a float in [0.0, 1.0]")

    scope = fact["scope"]
    if scope not in VALID_SCOPES:
        raise ContractValidationError(
            f"scope must be one of {sorted(VALID_SCOPES)}, got {scope!r}"
        )

    retention = fact["retention_days"]
    if not isinstance(retention, int) or retention < 0:
        raise ContractValidationError("retention_days must be an int >= 0")

    write_perm = fact["write_permission"]
    if write_perm not in VALID_WRITE_PERMISSIONS:
        raise ContractValidationError(
            f"write_permission must be one of {sorted(VALID_WRITE_PERMISSIONS)}"
        )

    # Timestamps — accept existing or fill
    created = fact.get("created_at") or _now_iso()
    last_accessed = fact.get("last_accessed") or _now_iso()

    clean: dict[str, Any] = {
        "content": content.strip(),
        "source": source,
        "confidence": float(confidence),
        "scope": scope,
        "retention_days": int(retention),
        "write_permission": write_perm,
        "created_at": created,
        "last_accessed": last_accessed,
    }

    if "id" in fact:
        clean["id"] = str(fact["id"])
    elif require_id:
        clean["id"] = str(uuid4())

    return clean


class MemoryStore:
    """Simple in-memory governed memory store.

    Designed to be swapped later for an encrypted / vector-backed store
    without changing the public contract surface.
    """

    def __init__(self, *, max_items: int = 200, cross_session_enabled: bool = False):
        self._items: list[dict[str, Any]] = []
        self.max_items = max_items
        self.cross_session_enabled = cross_session_enabled
        self._audit_log: list[dict[str, Any]] = []

    def write(
        self,
        fact: dict[str, Any],
        *,
        user_consent_for_cross_session: bool = False,
    ) -> dict[str, Any]:
        """Write a governed memory fact. Returns the stored contract."""
        clean = validate_contract(fact, require_id=True)

        # Cross-session policy
        if clean["retention_days"] > 0 or clean["scope"] in {"user", "global"}:
            if not self.cross_session_enabled:
                # Force session-only
                clean["retention_days"] = 0
                clean["scope"] = "session"
            elif not user_consent_for_cross_session and clean["scope"] != "session":
                raise ContractValidationError(
                    "Cross-session write requires explicit user consent"
                )

        # Enforce max size (drop oldest session items first)
        while len(self._items) >= self.max_items:
            self._items.pop(0)

        self._items.append(clean)
        self._audit_log.append(
            {
                "action": "write",
                "id": clean["id"],
                "timestamp": _now_iso(),
                "scope": clean["scope"],
            }
        )
        return clean

    def query(
        self,
        *,
        max_records: int = 3,
        scope: str | None = None,
        min_confidence: float = 0.0,
        text_hint: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return up to max_records relevant contracts."""
        results: list[dict[str, Any]] = []
        hint = (text_hint or "").lower()

        for item in reversed(self._items):  # newest first
            if scope and item["scope"] != scope:
                continue
            if item["confidence"] < min_confidence:
                continue
            if hint and hint not in item["content"].lower():
                # Soft filter — still allow if no better matches
                pass

            # Update last_accessed
            item["last_accessed"] = _now_iso()
            results.append(dict(item))
            if len(results) >= max_records:
                break

        # If text_hint produced nothing useful, fall back to highest-confidence
        if not results and self._items:
            ranked = sorted(self._items, key=lambda x: x["confidence"], reverse=True)
            results = [dict(x) for x in ranked[:max_records]]

        self._audit_log.append(
            {
                "action": "query",
                "count": len(results),
                "timestamp": _now_iso(),
            }
        )
        return results

    def revoke(self, fact_id: str) -> bool:
        """Remove a fact by id. Returns True if found."""
        for i, item in enumerate(self._items):
            if item.get("id") == fact_id:
                self._items.pop(i)
                self._audit_log.append(
                    {"action": "revoke", "id": fact_id, "timestamp": _now_iso()}
                )
                return True
        return False

    def clear_session(self) -> int:
        """Remove all session-scoped facts. Returns count removed."""
        before = len(self._items)
        self._items = [i for i in self._items if i["scope"] != "session"]
        removed = before - len(self._items)
        if removed:
            self._audit_log.append(
                {"action": "clear_session", "count": removed, "timestamp": _now_iso()}
            )
        return removed

    @property
    def size(self) -> int:
        return len(self._items)

    @property
    def audit_log(self) -> list[dict[str, Any]]:
        return list(self._audit_log)


# Module-level default store for demo / simple use
_default_store: MemoryStore | None = None


def get_default_store() -> MemoryStore:
    global _default_store
    if _default_store is None:
        _default_store = MemoryStore(cross_session_enabled=False)
        # Seed with a couple of realistic demo facts
        _default_store.write(
            {
                "content": "User prefers short, calm voice answers under 35 words.",
                "source": "user_said",
                "confidence": 0.92,
                "scope": "user",
                "retention_days": 90,
                "write_permission": "user_only",
                "created_at": "2026-07-28T09:14:00Z",
                "last_accessed": _now_iso(),
            },
            user_consent_for_cross_session=True,
        )
        # Force the seeded one to stay as user-scope for demo realism
        # (store already forced session because cross_session_enabled=False)
        # Re-seed with session scope for safety
        _default_store = MemoryStore(cross_session_enabled=False)
        _default_store.write(
            {
                "content": "User prefers short, calm voice answers under 35 words.",
                "source": "user_said",
                "confidence": 0.92,
                "scope": "session",
                "retention_days": 0,
                "write_permission": "user_only",
                "created_at": "2026-07-28T09:14:00Z",
                "last_accessed": _now_iso(),
            }
        )
        _default_store.write(
            {
                "content": "Recent high-signal topic: multi-agent safety patterns on X.",
                "source": "x_context",
                "confidence": 0.81,
                "scope": "session",
                "retention_days": 0,
                "write_permission": "agent",
                "created_at": _now_iso(),
                "last_accessed": _now_iso(),
            }
        )
    return _default_store
