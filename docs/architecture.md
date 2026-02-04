# EDITH Architecture Notes

## Core Principles
- MCP-first design with dynamic discovery.
- Remote MCPs by default, local MCPs for OS/editor access.
- Human approval for sensitive actions.

## Runtime Flow
1. User request enters UI layer.
2. Orchestrator classifies intent.
3. Planner builds a multi-step plan.
4. Human Approval Gate pauses when required.
5. Tool Router invokes MCP Client.
6. Memory Manager stores the interaction locally.

## Extension Points
- Add MCP servers via config without code changes.
- Add UI adapters that call the same orchestrator API.
