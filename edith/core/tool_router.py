"""Tool router that dispatches plan steps to MCP clients."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from edith.core.mcp_client import MCPClient
from edith.core.planner import PlanStep


@dataclass
class ToolResponse:
    tool: str
    output: Dict[str, Any]


class ToolRouter:
    """Route a plan step to the correct MCP client."""

    def __init__(self, mcp_client: MCPClient) -> None:
        self.mcp_client = mcp_client

    def execute(self, step: PlanStep) -> Dict[str, Any]:
        response = self.mcp_client.invoke(step.tool, step.params)
        return ToolResponse(tool=step.tool, output=response).__dict__
