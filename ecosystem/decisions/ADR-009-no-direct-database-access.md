# ADR-009: No Direct Database Access — API Is the Only Entry Point

## Status
Accepted

## Date
2026-03-29

## Context
In systems where MCP tools or other automation can access the database directly, enforcement becomes fragmented. Business rules, validation, and authorization that live in the API get bypassed. Project isolation that the API enforces disappears when something reaches the database directly. Schema assumptions can be violated by callers who bypass the API's validation layer.

## Decision
The database is never accessed directly by MCP tools, LLM agents, or operator surfaces.

The only entry point to any V Ecosystem system's database is that system's API.

This applies to:
- MCP tools — all calls go through the API
- VSCode extension — all data operations go through the API
- LLM agents — all state reads and writes go through the API
- Scripts and automation — all writes go through the API (read-only scripts may have exceptions with explicit justification)

The API is the enforcement layer. It is the only enforcement layer. It enforces:
- project scope
- system ownership boundaries
- authorization and actor rules
- input validation
- event logging requirements
- business rules

Nothing bypasses it.

## Consequences
- No MCP tool uses Prisma, direct SQL, or any database client
- No VSCode extension code writes directly to any database
- Every system's API must be fully capable of supporting all required operations — there are no "internal shortcuts" to the database
- The hammer can verify enforcement by testing the API layer directly, without needing to test every possible client
- Adding a new capability always starts with the API, not with a direct database operation

## Related Docs
- `../../interfaces/mcp-coordination-model.md`
- `../../ecosystem/db-posture.md`
- `ADR-004-mcp-tools-are-thin-wrappers.md`
