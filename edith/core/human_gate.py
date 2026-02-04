"""Human approval gate for sensitive actions."""

from __future__ import annotations

from dataclasses import dataclass

from edith.core.planner import PlanStep


@dataclass
class ApprovalRequest:
    session_id: str
    step: PlanStep


class HumanApprovalGate:
    """Stops execution until a user confirms a sensitive action."""

    def request_approval(self, step: PlanStep, session_id: str) -> bool:
        _ = ApprovalRequest(session_id=session_id, step=step)
        return False
