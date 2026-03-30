# ADR-005: Session Token Model for Project Scope

## Status
Accepted

## Date
2026-03-29

## Context
With 20+ projects in the ecosystem, cross-project contamination is a serious risk. The most obvious solution — having the LLM pass a project ID header on each MCP tool call — is insufficient. The LLM controls what it passes. Drift, hallucination, or a simple mistake could cause the LLM to pass the wrong project ID and read or write another project's data.

Several options were considered:

Option A: LLM passes project ID as a parameter on each tool call.
Option B: Extension sets a project ID header that MCP forwards on every call.
Option C: Extension initializes a server-side session bound to the project UUID. MCP server returns an opaque session token. All subsequent tool calls use the session token. Project ID is never exposed to the LLM.

## Decision
Option C — the session token model.

The human operator selects the active project in the VSCode extension. The extension calls the MCP server's session initialization endpoint with the project UUID. The MCP server creates a server-side session record bound to that UUID and returns an opaque session token. All MCP tool calls use the session token. The project ID is resolved server-side from the token. The LLM never sees the project ID.

Option A was rejected because the LLM controls the parameter — drift or error can cause the wrong project to be targeted.

Option B was better than A but still client-controlled. A determined or mistaken LLM could theoretically manipulate headers. Moving the binding to the server-side removes that risk entirely.

## Consequences
- The MCP server must implement a session initialization endpoint
- Session tokens are opaque and project-bound server-side
- The LLM cannot change the active project during a session
- Project switching requires a deliberate human action in the extension
- Cross-project contamination is structurally prevented rather than behaviorally discouraged
- Session tokens can be invalidated server-side instantly
- The extension displays the active project name visibly at all times in the status bar

## Related Docs
- `../../interfaces/mcp-coordination-model.md`
- `ADR-004-mcp-tools-are-thin-wrappers.md`
