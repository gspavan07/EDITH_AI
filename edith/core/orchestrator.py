"""EDITH Orchestrator: coordinates intent, planning, tool routing, and memory."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from edith.core.intent_classifier import IntentClassifier, IntentResult
from edith.core.planner import Plan, PlannerAgent
from edith.core.tool_router import ToolRouter
from edith.core.human_gate import HumanApprovalGate
from edith.core.memory_manager import MemoryManager


@dataclass
class OrchestratorResponse:
    """Represents a structured response from the orchestrator."""

    summary: str
    plan: Plan | None = None
    tool_results: List[Dict[str, Any]] | None = None


class EDITHOrchestrator:
    """Primary coordinator for EDITH actions."""

    def __init__(
        self,
        intent_classifier: IntentClassifier,
        planner: PlannerAgent,
        tool_router: ToolRouter,
        human_gate: HumanApprovalGate,
        memory_manager: MemoryManager,
    ) -> None:
        self.intent_classifier = intent_classifier
        self.planner = planner
        self.tool_router = tool_router
        self.human_gate = human_gate
        self.memory_manager = memory_manager

    def handle_message(self, message: str, session_id: str) -> OrchestratorResponse:
        """Process a user message end-to-end."""
        intent: IntentResult = self.intent_classifier.classify(message)
        plan = self.planner.build_plan(message, intent)
        tool_results: List[Dict[str, Any]] = []

        for step in plan.steps:
            if step.requires_approval:
                approved = self.human_gate.request_approval(step, session_id)
                if not approved:
                    return OrchestratorResponse(
                        summary="Action cancelled pending user approval.",
                        plan=plan,
                        tool_results=tool_results,
                    )
            result = self.tool_router.execute(step)
            tool_results.append(result)

        self.memory_manager.save_interaction(session_id, message, tool_results)
        summary = self.planner.summarize_results(plan, tool_results)
        return OrchestratorResponse(summary=summary, plan=plan, tool_results=tool_results)
