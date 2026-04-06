# ADR-010 — Agent Orchestration Is a Desktop Runtime Capability

## Status
Accepted

## Context
The V Ecosystem has three core systems:
- Project V (planning)
- VEDA (observability)
- V Forge (execution)

New runtime capabilities (orchestration, memory, compaction, etc.) must be integrated without creating a new system.

## Decision
Agent orchestration is a desktop/runtime capability.
It is not a fourth peer system and does not introduce new truth ownership.

This decision aligns with ADR-011, which establishes the Tauri 2 desktop application as the primary operator host.

## Core Rule
Orchestration coordinates bounded runtime behavior. It does not create authority.

## Constraints
- No governance bypass
- No hidden approvals
- No new system of record
- Delegation does not increase authority

## Consequences
- Requires desktop runtime doctrine docs
- Requires updates to desktop readme and execution plan

## Related Docs

- `../../interfaces/desktop-agent-orchestration-model.md`
- `ADR-011-tauri-2-desktop-is-the-operator-host.md`
