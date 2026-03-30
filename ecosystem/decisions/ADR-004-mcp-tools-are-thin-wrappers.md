# ADR-004: MCP Tools Are Thin Wrappers — API Is the Enforcement Layer

## Status
Accepted

## Date
2026-03-29

## Context
Early MCP implementations risk conflating the tool layer with the enforcement layer. If MCP tools contain business logic, validation, or authorization checks, the enforcement becomes fragmented — spread across the tool layer and the API layer, creating inconsistency and brittleness. If MCP tools access the database directly, system boundaries dissolve because any tool can reach any data.

## Decision
MCP tools are thin wrappers. The API is the enforcement layer. The database is never accessed directly by MCP tools.

The enforcement chain is always:

```
LLM declares intent
→ MCP tool (thin wrapper — transport only)
→ API call (enforcement layer — business rules, scope, ownership, validation)
→ Database (never accessed directly by MCP tools)
```

MCP tools are responsible for: formatting the request, passing session context, returning the API response.

The API is responsible for: project scope enforcement, system ownership boundaries, authorization, input validation, event logging, response shaping.

No MCP tool may bypass this chain. No MCP tool may add business logic that belongs to the API.

## Consequences
- All MCP tools must be built as thin API wrappers
- No MCP tool uses Prisma, direct SQL, or any database client
- Business rules, validation, and authorization live exclusively in the API layer
- Adding a new MCP tool does not require adding enforcement logic — the API already has it
- The API can be tested and verified independently of the MCP tool layer
- The hammer can verify API enforcement without needing to go through the MCP layer

## Related Docs
- `../../interfaces/mcp-coordination-model.md`
- `../../ecosystem/cross-system-boundaries.md`
- `ADR-005-session-token-model-for-project-scope.md`
