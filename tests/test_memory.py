"""Tests for governed memory contracts and MemoryStore."""

import pytest

from vesper.memory import (
    MemoryStore,
    validate_contract,
    ContractValidationError,
    get_default_store,
)


def _valid_fact(**overrides):
    base = {
        "content": "User prefers calm answers",
        "source": "user_said",
        "confidence": 0.9,
        "scope": "session",
        "retention_days": 0,
        "write_permission": "user_only",
        "created_at": "2026-08-01T12:00:00Z",
        "last_accessed": "2026-08-01T12:00:00Z",
    }
    base.update(overrides)
    return base


def test_validate_contract_happy_path():
    clean = validate_contract(_valid_fact())
    assert clean["content"] == "User prefers calm answers"
    assert clean["confidence"] == 0.9


def test_validate_contract_missing_field():
    fact = _valid_fact()
    del fact["source"]
    with pytest.raises(ContractValidationError, match="Missing required fields"):
        validate_contract(fact)


def test_validate_contract_bad_confidence():
    with pytest.raises(ContractValidationError, match="confidence"):
        validate_contract(_valid_fact(confidence=1.5))


def test_validate_contract_bad_source():
    with pytest.raises(ContractValidationError, match="source"):
        validate_contract(_valid_fact(source="invented"))


def test_store_write_and_query():
    store = MemoryStore()
    stored = store.write(_valid_fact())
    assert "id" in stored
    assert store.size == 1

    results = store.query(max_records=3)
    assert len(results) == 1
    assert results[0]["content"] == "User prefers calm answers"


def test_store_cross_session_blocked_without_consent():
    store = MemoryStore(cross_session_enabled=True)
    with pytest.raises(ContractValidationError, match="consent"):
        store.write(_valid_fact(scope="user", retention_days=30))


def test_store_cross_session_allowed_with_consent():
    store = MemoryStore(cross_session_enabled=True)
    stored = store.write(
        _valid_fact(scope="user", retention_days=30),
        user_consent_for_cross_session=True,
    )
    assert stored["scope"] == "user"
    assert stored["retention_days"] == 30


def test_store_revoke():
    store = MemoryStore()
    stored = store.write(_valid_fact())
    assert store.revoke(stored["id"]) is True
    assert store.size == 0
    assert store.revoke("nonexistent") is False


def test_store_clear_session():
    store = MemoryStore()
    store.write(_valid_fact(scope="session"))
    store.write(_valid_fact(content="another", scope="session"))
    removed = store.clear_session()
    assert removed == 2
    assert store.size == 0


def test_default_store_seeded():
    store = get_default_store()
    assert store.size >= 1
    results = store.query(max_records=5)
    assert len(results) >= 1
