"""Memory management for EDITH sessions."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class SessionMemory:
    session_id: str
    history: List[Dict[str, Any]] = field(default_factory=list)


class MemoryManager:
    """Store and retrieve conversation history locally."""

    def __init__(self) -> None:
        self.sessions: Dict[str, SessionMemory] = {}

    def save_interaction(self, session_id: str, message: str, tool_results: List[Dict[str, Any]]) -> None:
        session = self.sessions.setdefault(session_id, SessionMemory(session_id=session_id))
        session.history.append({"message": message, "tool_results": tool_results})

    def load_session(self, session_id: str) -> SessionMemory | None:
        return self.sessions.get(session_id)
