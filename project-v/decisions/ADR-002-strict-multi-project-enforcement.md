# ADR-002: Strict Multi-Project Enforcement

## Status

Accepted.

---

## Context

Project V is designed for multi-project operation — potentially hundreds of
projects simultaneously. At that scale, operator memory, hidden defaults, and
loose conventions become liabilities.

Without structural enforcement, the system will drift toward:
- cross-project data leakage
- ambiguous reads that return results from the wrong project
- accidental writes under incorrect project scope
- weak uniqueness rules that break at scale

That drift is unacceptable.

---

## Decision

Project V enforces multi-project isolation structurally, not by convention.

Every record must be classified as one of:
- **project-scoped** — belongs to exactly one project
- **intentionally global** — rare, explicitly justified, documented
- **system metadata** — not project-owned truth

Reads and writes must enforce explicit project scope.
Project-scoped records must be unreadable across project boundaries by default.

---

## Rules

### Project-scoped records
- must belong to exactly one project
- must require explicit project context for writes
- must reject cross-project relations
- must be invisible across project lines by default in reads

### Global records
- must be rare
- must be documented with a justified reason
- must not become a loophole for project-owned truth

### Reads
- must resolve project scope explicitly where required
- must not leak cross-project existence by default
- must return deterministic ordering

### Writes
- must require explicit project context for project-scoped truth
- must reject cross-project contamination

---

## Why

- protects correctness and auditability at scale
- makes LLM-assisted usage safer — scoped tool calls cannot contaminate other projects
- keeps operator surfaces honest — what you see is what you acted on
- aligns with the session token model (ADR-005) which enforces project scope at the MCP layer

---

## Relationship to Ecosystem ADRs

ADR-005 (session token model) enforces project scope at the MCP layer so the LLM
never sees project UUIDs and cannot contaminate sessions.
This ADR ensures the database layer enforces the same boundary independently.
Both layers must hold for the boundary to be reliable.

---

## Related Docs

- `../system-invariants.md`
- `../multi-project-doctrine.md`
- `../schema-authority.md`
- `../../interfaces/mcp-coordination-model.md`
- `../../ecosystem/decisions/ADR-005-session-token-model-for-project-scope.md`