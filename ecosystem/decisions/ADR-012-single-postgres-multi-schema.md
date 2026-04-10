# ADR-012: Single PostgreSQL Database with Per-System Schema Separation

## Status
Accepted

## Date
2026-04-09

## Context

The original ecosystem database posture described in `ecosystem/db-posture.md`
assumed one separate database per bounded system, with cross-database credential
isolation as the primary enforcement mechanism.

This posture was never implemented as a discrete ADR — it existed as prose doctrine
in `db-posture.md`. In practice, the ecosystem is being built with a single
PostgreSQL database instance.

A single-database posture is operationally simpler and still supports strict logical
separation when schemas are used correctly. The critical constraint — that bounded
system ownership must be preserved and that physical consolidation must not become
conceptual merger — is achievable through schema-level separation rather than
database-level separation.

The ecosystem now has four bounded systems:
- Project V (planning truth)
- VEDA (observatory truth)
- VEDA Strategy (derived strategic intelligence)
- V Forge (execution truth)

## Decision

The V Ecosystem uses **one physical PostgreSQL database** with **four schemas**,
one per bounded system:

- `project_v` — owned by Project V
- `veda` — owned by VEDA
- `veda_strategy` — owned by VEDA Strategy
- `v_forge` — owned by V Forge

Logical separation is enforced by:
- schema ownership (each system owns its schema)
- database roles and credentials scoped per system
- service-layer boundaries (each system's API is the only entry point to its schema)
- MCP/tool boundaries (no tool bypasses the API layer)

Physical consolidation into one database does not imply shared ownership.
Each schema is an independently governed canonical persistence boundary.
Systems that share a database instance do not share truth.

## Consequences

- `ecosystem/db-posture.md` is updated to reflect this posture throughout
- All references to "separate databases" are replaced with "separate schemas"
- Credential isolation is scoped at the schema/role level, not the database level
- Migration runners are scoped to each system's own schema
- Cross-schema direct access remains forbidden; the API enforcement model from
  ADR-009 applies at the schema boundary
- The prior multi-database prose posture in `db-posture.md` is superseded by this ADR

## Non-Consequences

This decision does not weaken any ownership boundary.
Physical consolidation is an infrastructure choice.
Conceptual separation, ownership doctrine, and boundary enforcement rules remain
identical to what the prior multi-database posture required.

A future decision to move to separate database instances (e.g., for scaling or
isolation requirements) would not require changes to the ownership doctrine —
only to the infrastructure.

## Related Docs
- `../../ecosystem/db-posture.md`
- `ADR-009-no-direct-database-access.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../interfaces/data-boundaries.md`
