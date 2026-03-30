# ADR-001: Separate Databases Per Bounded System

## Status

Accepted.

---

## Context

The V Ecosystem divides into bounded systems with distinct truth domains:
- Project V owns planning and orchestration truth
- VEDA owns observatory truth
- V Forge owns execution truth

A shared database across bounded systems would make it easier for implementation
convenience, LLM-generated code, and operational shortcuts to blur canonical ownership.
That blur is a governance failure.

The ecosystem-level ADR-009 (no direct database access) establishes that all
cross-system data access must go through APIs. This ADR establishes the
persistence-layer shape that supports that enforcement: separate databases,
one per bounded system, within a shared cluster.

---

## Decision

Use one shared Postgres cluster with one database per bounded system.

Database assignments:
- `project_v` — canonical persistence for Project V
- `veda` — canonical persistence for VEDA
- `v_forge` — canonical persistence for V Forge

Each system owns its database. No system may write canonically to another
system's database. Cross-system data exchange goes through the governing API,
as required by ADR-009.

---

## Why

- preserves bounded ownership at the persistence layer
- makes cross-system writes structurally harder than convenience writes
- allows schema evolution per system without affecting other systems
- enables per-system credential separation if needed later
- supports later infrastructure separation without a data migration crisis
- aligns implementation structure with doc-level system boundaries

---

## Rules Implied

- no mixed canonical ownership across databases
- no direct convenience writes into another system's tables
- cross-system references must be explicit IDs, not foreign-key joins across databases
- imported or derived data stored locally must be marked as non-canonical

---

## Relationship to Ecosystem ADRs

ADR-009 (no direct database access) establishes that APIs are the enforcement layer.
This ADR establishes that the databases themselves are separated by system to
make boundary enforcement structurally reinforced, not just policy-enforced.

---

## Related Docs

- `../system-invariants.md`
- `../data-boundaries.md`
- `../../interfaces/data-boundaries.md`
- `../../ecosystem/db-posture.md`
- `../../ecosystem/decisions/ADR-009-no-direct-database-access.md`