# ADR-003: Governed Schema and Endpoint Expansion

## Status

Accepted.

---

## Context

Project V is designed to be strict, multi-project-safe, and resistant to drift.
Uncontrolled schema growth and endpoint sprawl are two of the fastest paths
to destroying that goal.

A system that adds fields, tables, and routes casually during implementation
becomes harder to classify, harder to test, easier to drift, and less
readable by LLMs and humans alike.

The docs-are-the-build-spec principle (ecosystem ADR-007) requires that
implementation follows governed documentation rather than the reverse.
Schema and endpoint expansion must conform to that principle.

---

## Decision

Project V adopts governed expansion for both schema and endpoints.

The initial approved core model and endpoint families are the governed base.
Later additions are exceptional, not routine.
Each schema or endpoint change must justify itself against the criteria below
before it may be treated as part of the governed model.

Implementation convenience is not sufficient justification.

---

## Schema Change Criteria

A schema change must justify:
- why the truth belongs in Project V and not another system
- why the shape is canonical rather than derived or imported
- why existing schema is insufficient
- how project scope and integrity are enforced for the new records
- what hammer coverage will verify correctness of the new schema

## Endpoint Change Criteria

An endpoint change must justify:
- why existing route families are insufficient
- what bounded capability it exposes or mutates
- how project scope is resolved in the new route
- what validation posture it requires
- how deterministic behavior is preserved

---

## Why

- reduces schema drift and API sprawl
- protects multi-project integrity
- keeps docs and code aligned (supports ADR-007)
- improves testability — governed additions are easier to hammer
- improves LLM readability — a smaller, well-governed surface generates safer code

---

## Relationship to Ecosystem ADRs

ADR-006 (hammer doctrine) requires that every system implement hammer verification.
Governed expansion ensures the hammer can actually verify what was added.
ADR-007 (docs are the build spec) requires that the schema follow the docs, not the reverse.
This ADR makes the schema expansion pathway consistent with that principle.

---

## Related Docs

- `../system-invariants.md`
- `../schema-authority.md`
- `../../governance/testing-and-verification-doctrine.md`
- `../../ecosystem/decisions/ADR-006-hammer-doctrine-is-ecosystem-law.md`
- `../../ecosystem/decisions/ADR-007-docs-are-build-spec-db-owns-operational-state.md`