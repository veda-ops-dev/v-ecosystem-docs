# ADR-010 — Agent Orchestration Is an Extension Runtime Capability

## Status
Accepted

## Context
The V Ecosystem has three core systems:
- Project V (planning)
- VEDA (observability)
- V Forge (execution)

New runtime capabilities (orchestration, memory, compaction, etc.) must be integrated without creating a new system.

## Decision
Agent orchestration is an extension/runtime capability.
It is not a fourth peer system and does not introduce new truth ownership.

## Core Rule
Orchestration coordinates bounded runtime behavior. It does not create authority.

## Constraints
- No governance bypass
- No hidden approvals
- No new system of record
- Delegation does not increase authority

## Consequences
- Requires new extension runtime doctrine docs
- Requires updates to extension readme and execution plan
