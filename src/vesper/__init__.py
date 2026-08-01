"""Vesper — next-generation voice presence agent for X."""

__version__ = "0.1.1"

from vesper.memory import MemoryStore, validate_contract, ContractValidationError
from vesper.runtime import (
    check_kill_switch,
    validate_env,
    start_voice_session,
    handle_turn,
    update_presence,
)

__all__ = [
    "__version__",
    "MemoryStore",
    "validate_contract",
    "ContractValidationError",
    "check_kill_switch",
    "validate_env",
    "start_voice_session",
    "handle_turn",
    "update_presence",
]
