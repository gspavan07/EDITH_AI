"""MCP client abstraction for remote and local servers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class MCPServer:
    name: str
    endpoint: str
    is_remote: bool
    capabilities: List[str]


class MCPClient:
    """Dynamic MCP discovery and invocation layer."""

    def __init__(self, servers: List[MCPServer]) -> None:
        self.servers = {server.name: server for server in servers}

    def list_servers(self) -> List[MCPServer]:
        return list(self.servers.values())

    def invoke(self, tool: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke an MCP tool call.

        NOTE: This placeholder returns structured data for now.
        """
        return {
            "tool": tool,
            "params": params,
            "status": "queued",
        }
