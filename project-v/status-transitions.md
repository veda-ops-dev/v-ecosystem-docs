# Status Transitions

## Purpose

This document defines the first-pass legal status transitions for all Project V records that use explicit status routes.

It exists to answer:

```text
Which status transitions are allowed, which are forbidden, and what rules govern transition behavior across Project V's planning and orchestration domain?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the legal status transitions for every Project V entity that uses governed status
- what transitions are allowed, allowed with explicit reason, or forbidden
- when `StatusHistory` must be written
- the transition enforcement rules the API must apply

---

## Out of Scope

This document does not define:

- API route shape or request format
- controlled vocabulary values (see `controlled-vocabularies.md`)
- schema column types or exact field names (see `schema-authority.md`)
- readiness or audit result transitions (those are governed by `readiness-evaluation-rules.md` and `audit-evaluation-rules.md`)

---

## System

- project-v

---

## Core Rule

If an API contract says illegal status transitions must fail, those legal transitions must be defined here.

Implementation must not invent transition rules ad hoc.

Status transitions in this document govern Project V planning and orchestration truth. They do not make Project V the owner of downstream V Forge execution lifecycle.

---

## Transition Rule Types

All transitions fall into three categories:

- **allowed** — may proceed without an explicit reason
- **allowed with explicit reason** — may proceed only when the caller supplies a non-empty reason; missing or empty reason must fail with `400 Bad Request`
- **forbidden** — must be rejected with `422 Unprocessable Entity`

---

## General Enforcement Rules

All transition requests must:

- supply an explicit target status
- supply a non-empty reason when the transition category requires one
- be rejected with `422 Unprocessable Entity` for any forbidden transition
- write a `StatusHistory` row atomically when the entity type mandates history (see per-entity sections below)

---

## Project Status Transitions

Allowed values: `active`, `deferred`, `archived`

### Allowed transitions
- `active → deferred`
- `deferred → active`

### Allowed with explicit reason
- `active → archived`
- `deferred → archived`

### Forbidden transitions
- `archived → active`
- `archived → deferred`

### StatusHistory requirement
All project status transitions must write a `StatusHistory` row in the same transaction.
`StatusHistory.entityType` must be `project`.

### Notes
Archival is one-way in the first pass.

---

## Objective Status Transitions

Allowed values: `proposed`, `active`, `blocked`, `completed`, `archived`

### Allowed transitions
- `proposed → active`
- `proposed → blocked`
- `active → blocked`
- `blocked → active`
- `active → completed`
- `completed → archived`

### Allowed with explicit reason
- `blocked → archived`
- `proposed → archived`

### Forbidden transitions
- `completed → active`
- `completed → blocked`
- `archived → proposed`
- `archived → active`
- `archived → blocked`
- `archived → completed`

### StatusHistory requirement
All objective status transitions must write a `StatusHistory` row in the same transaction.
`StatusHistory.entityType` must be `objective`.

---

## Initiative Status Transitions

Allowed values: `proposed`, `active`, `blocked`, `completed`, `archived`

### Allowed transitions
- `proposed → active`
- `proposed → blocked`
- `active → blocked`
- `blocked → active`
- `active → completed`
- `completed → archived`

### Allowed with explicit reason
- `blocked → archived`
- `proposed → archived`

### Forbidden transitions
- `completed → active`
- `completed → blocked`
- `archived → proposed`
- `archived → active`
- `archived → blocked`
- `archived → completed`

### StatusHistory requirement
All initiative status transitions must write a `StatusHistory` row in the same transaction.
`StatusHistory.entityType` must be `initiative`.

---

## Work Item Status Transitions

Allowed values: `proposed`, `active`, `blocked`, `completed`, `archived`

### Allowed transitions
- `proposed → active`
- `proposed → blocked`
- `active → blocked`
- `blocked → active`
- `active → completed`
- `completed → archived`

### Allowed with explicit reason
- `blocked → archived`
- `proposed → archived`

### Forbidden transitions
- `proposed → completed`
- `completed → active`
- `completed → blocked`
- `archived → proposed`
- `archived → active`
- `archived → blocked`
- `archived → completed`

### StatusHistory requirement
All work-item status transitions must write a `StatusHistory` row in the same transaction.
`StatusHistory.entityType` must be `work_item`.

### Notes
The first pass requires visible activation (`proposed → active`) before completion. Direct `proposed → completed` is forbidden.

---

## Handoff Status Transitions

Allowed values: `proposed`, `ready`, `handed_off`, `accepted`, `closed`

### Allowed transitions (forward path)
- `proposed → ready`
- `ready → handed_off`
- `handed_off → accepted`
- `accepted → closed`

### Allowed with explicit reason (direct closure)
- `proposed → closed`
- `ready → closed`
- `handed_off → closed`

### Allowed with explicit reason (reverse / re-entry path)
- `handed_off → ready`
- `handed_off → proposed`

### Forbidden transitions
- `accepted → handed_off`
- `accepted → ready`
- `accepted → proposed`
- `closed → proposed`
- `closed → ready`
- `closed → handed_off`
- `closed → accepted`
- `proposed → accepted`
- `proposed → handed_off`
- `ready → proposed`
- `ready → accepted`

### StatusHistory requirement
All handoff status transitions must write a `StatusHistory` row in the same transaction.
`StatusHistory.entityType` must be `handoff`.

`completedAt` on the `Handoff` record must be set to `now()` atomically in the same transaction when the status transitions to `closed`. For all other transitions, `completedAt` remains null.

### Notes
Handoff progression is normally forward and linear.

Reverse re-entry transitions (`handed_off → ready`, `handed_off → proposed`) are explicitly allowed but require an explicit reason and must leave recoverable status history. These transitions remain orchestration-side decisions. They do not model V Forge internal execution lifecycle or rejection semantics.

Once a handoff reaches `accepted` or `closed`, no reverse transition is allowed in the first pass.

---

## Decision Record Status Transitions

Allowed values: `recorded`, `superseded`

### Allowed with explicit reason
- `recorded → superseded`

### Forbidden transitions
- `superseded → recorded`

### StatusHistory requirement
The `recorded → superseded` transition must write a `StatusHistory` row in the same transaction.
`StatusHistory.entityType` must be `decision_record`.

### Notes
Decision records preserve planning history rather than bouncing between statuses. Supersedence is one-way in the first pass.

---

## Research Doc Status Transitions

Allowed values: `active`, `archived`

### Allowed with explicit reason
- `active → archived`

### Forbidden transitions
- `archived → active`

### Notes
Research-doc archival is one-way in the first pass. No `StatusHistory` is required for research docs in the first pass.

---

## Dependency Status Transitions

Allowed values: `active`, `resolved`

### Allowed transitions
- `active → resolved`

### Forbidden transitions
- `resolved → active`

### Notes
The first pass treats dependency resolution as one-way. If reopening is needed later, it must be modeled explicitly. No `StatusHistory` is required for dependencies in the first pass.

---

## Audit Run Result Transitions

Allowed values: `pass`, `fail`, `warning`, `stale`

### Allowed with explicit reason (staleness path)
- `pass → stale`
- `fail → stale`
- `warning → stale`

### Forbidden transitions
- `stale → pass`
- `stale → fail`
- `stale → warning`

### StatusHistory requirement
The staleness transitions must write a `StatusHistory` row in the same transaction when the staleness path is explicitly triggered through the governed invalidation mechanism.
`StatusHistory.entityType` must be `audit_run`.

### Notes
Audit results are planning and governance outputs, not execution-lifecycle statuses. Staleness is the bounded invalidation mechanism in the first pass.

---

## Audit Gap Status Transitions

Allowed values: `open`, `resolved`, `invalidated`

### Allowed transitions
- `open → resolved`

### Allowed with explicit reason
- `open → invalidated`
- `resolved → invalidated`

### Forbidden transitions
- `invalidated → open`
- `invalidated → resolved`

### Notes
No `StatusHistory` is required for audit gaps in the first pass.

---

## ExternalLink

`ExternalLink` does not use a governed lifecycle status in the first pass. It is created, updated in bounded ways, or superseded by new linkage records rather than forced through an artificial status-transition model.

---

## Readiness Evaluation Results

Readiness evaluation results are controlled vocabulary outputs, not mutable lifecycle statuses. They must not be treated as status-transition records. See `readiness-evaluation-rules.md`.

---

## Human-In-The-Loop Principle

Status transitions that involve archival, closure, supersedence, or reverse re-entry are governance-sensitive. Human review may be required before these transitions are allowed in approval-gated workflow contexts.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- every transition not listed as allowed is forbidden
- forbidden transitions must be rejected with `422 Unprocessable Entity`
- transitions requiring explicit reason must fail with `400 Bad Request` if reason is missing or empty
- `StatusHistory` must be written in the same transaction for the entity types that require it
- archival and supersedence are one-way in the first pass

---

## Usage

This document should be used:

- when implementing transition endpoints
- when writing validation logic for status changes
- when writing hammer tests for transition enforcement
- when reviewing whether a proposed transition is legal

---

## Related Docs

- `controlled-vocabularies.md`
- `schema-authority.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/approval-and-escalation-model.md`
