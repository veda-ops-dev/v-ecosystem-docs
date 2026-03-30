# ADR-004: Separate Audit and Readiness Records

## Status

Accepted.

---

## Context

Project V models readiness as a first-class concept:
- ReadinessEvaluation — the governed gate that determines whether work may proceed
- ReadinessGap — a specific gap that must be resolved before readiness is satisfied

The BYDA layer introduces additional concepts:
- AuditRun — a bounded structured audit against a declared audit type and target
- AuditGap — a specific finding from an audit run requiring governance attention
- GitHubLink — bounded traceability linkage to source-control artifacts

A structural decision was required: expand readiness records to absorb audit,
or model audit as a related but separate subsystem.

---

## Decision

Audit records are modeled separately from readiness records.

Readiness and audit are related but answer different questions:
- readiness answers: may this work proceed?
- audit answers: what was checked, against what criteria, with what findings?

The initial schema additions are:
- **AuditRun** — records that a BYDA-style audit occurred, its type, target, and result
- **AuditGap** — records specific findings from an audit run with severity and remediation
- **GitHubLink** — records bounded traceability linkage to GitHub for planning-side audit

Readiness records (ReadinessEvaluation, ReadinessGap) remain unchanged.
Linking between readiness and audit is explicit, not assumed.

---

## Why

- readiness stays smaller and purpose-focused as the governed progression gate
- BYDA-style audit can evolve toward richer lifecycle and artifact-aware framing
  without distorting readiness semantics
- code-alignment and cross-artifact consistency checking can be added to audit
  without overloading the readiness record family
- separation makes each record type easier to govern, test, and hammer

---

## Deferred Schema

The following schema concepts are deferred until explicitly promoted through
governed schema expansion (per ADR-003):
- ArtifactManifest
- ArtifactDeclaration
- ImplementationPackage
- DriftFinding
- dedicated AuditLayerResult

These must not be added without satisfying the governed schema expansion criteria.

---

## Rules

- readiness remains server-owned and governed by readiness rules
- audit remains artifact-aware and lifecycle-aware
- any coupling between audit and readiness must be explicit, not assumed
- GitHubLink remains bounded traceability — not source-control ownership

---

## Related Docs

- `../system-invariants.md`
- `../byda-in-project-v.md`
- `../schema-authority.md`
- `../github-integration.md`
- `ADR-003-governed-schema-and-endpoint-expansion.md`