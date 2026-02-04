"""Planner agent for EDITH."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from edith.core.intent_classifier import IntentResult, IntentType


@dataclass
class PlanStep:
    """A single step in an execution plan."""

    name: str
    description: str
    tool: str
    params: Dict[str, Any]
    requires_approval: bool = False


@dataclass
class Plan:
    """Structured plan for an EDITH request."""

    steps: List[PlanStep]


class PlannerAgent:
    """Constructs multi-step plans based on user intent."""

    def build_plan(self, message: str, intent: IntentResult) -> Plan:
        if intent.intent == IntentType.COMMUNICATION:
            return Plan(
                steps=[
                    PlanStep(
                        name="gmail_list",
                        description="List unread Gmail messages.",
                        tool="gmail.list_unread",
                        params={"limit": 10},
                        requires_approval=False,
                    )
                ]
            )
        if intent.intent == IntentType.PROFESSIONAL_PRESENCE:
            return Plan(
                steps=[
                    PlanStep(
                        name="linkedin_post",
                        description="Create a LinkedIn post draft.",
                        tool="linkedin.create_post",
                        params={"content": message},
                        requires_approval=True,
                    )
                ]
            )
        if intent.intent == IntentType.DEVELOPER:
            return Plan(
                steps=[
                    PlanStep(
                        name="github_repo",
                        description="Describe repository structure.",
                        tool="github.describe_repo",
                        params={"query": message},
                        requires_approval=False,
                    )
                ]
            )
        if intent.intent == IntentType.LIVE_SEARCH:
            return Plan(
                steps=[
                    PlanStep(
                        name="search",
                        description="Run a live search query.",
                        tool="search.query",
                        params={"query": message},
                        requires_approval=False,
                    )
                ]
            )
        if intent.intent == IntentType.DOCUMENT:
            return Plan(
                steps=[
                    PlanStep(
                        name="doc_analyze",
                        description="Analyze a document via MCP.",
                        tool="docs.analyze",
                        params={"query": message},
                        requires_approval=False,
                    )
                ]
            )
        if intent.intent == IntentType.WEB_NAVIGATION:
            return Plan(
                steps=[
                    PlanStep(
                        name="browser_navigate",
                        description="Navigate with visible browser automation.",
                        tool="browser.navigate",
                        params={"task": message},
                        requires_approval=True,
                    )
                ]
            )
        return Plan(
            steps=[
                PlanStep(
                    name="chat",
                    description="Respond conversationally.",
                    tool="chat.respond",
                    params={"message": message},
                    requires_approval=False,
                )
            ]
        )

    def summarize_results(self, plan: Plan, tool_results: List[Dict[str, Any]]) -> str:
        if not tool_results:
            return "No tool results were produced."
        summary_lines = [f"Step {index + 1}: {step.name} completed." for index, step in enumerate(plan.steps)]
        return "\n".join(summary_lines)
