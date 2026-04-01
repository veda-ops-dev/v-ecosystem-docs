# Schema Specification

## Purpose

This document defines the first-pass concrete schema specification for Project V.

It exists to answer:

```text
What are the exact columns, types, constraints, indexes, and allowed mutations for the first-pass Project V schema that remains after refoundation?
```

Read this with:

- `schema-authority.md`
- `v-forge-integration.md`
- `system-invariants.md`
- `multi-project-doctrine.md`
- `controlled-vocabularies.md`
- `status-transitions.md`

If this document conflicts with `schema-authority.md`, the conflict must be resolved explicitly. Neither should be silently ignored.

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the exact first-pass canonical Project V tables
- exact columns, types, constraints, and indexes
- allowed mutations for each canonical table
- same-project integrity rules
- ordering-support posture
- bounded external-link posture
- mutation restrictions needed to prevent schema drift

---

## Out of Scope

This document does not define:

- migration sequencing
- route-by-route API payloads
- endpoint contract families
- VEDA schema design
- V Forge schema design
- provider-specific external integration models beyond the thin ExternalLink family

Those belong in migration docs, API docs, and other system-specific authority docs.

---

## System

- project-v

---

## Core Rule

Project V schema must remain strictly aligned to Project V ownership.

This means the first-pass schema may model:

- planning truth
- orchestration truth
- readiness truth
- audit truth
- bounded planning-side traceability

It must not model:

- VEDA observability truth
- V Forge execution truth
- convenience copies of downstream execution state
- rich provider-specific execution models inside Project V

Exact schema detail exists to make this boundary buildable, not negotiable.

---

## Type Conventions

These specifications assume PostgreSQL.

Recommended baseline type posture:

- primary keys: `uuid`
- foreign keys: `uuid`
- short stable keys: `text`
- titles and descriptions: `text`
- status and controlled-vocabulary fields: `text` constrained by application and later enum/check strategy
- timestamps: `timestamptz`
- booleans: `boolean`
- bounded flexible payloads only where justified: `jsonb`
- ranking / scoring fields where used: `integer`

---

## Controlled Vocabulary Rule

Controlled vocabulary fields must remain explicit and small.

They may initially be implemented as constrained `text` values, with a later decision on database enum vs check-constraint strategy.

The canonical value sets belong to `controlled-vocabularies.md`.
This document names which fields must use those vocabularies.

The following fields must use controlled vocabularies in the first pass:

- project `status`
- objective `status`
- initiative `status`
- initiative `targetSystem`
- work item `type`
- work item `status`
- work item `readinessState`
- work item `targetSystem`
- dependency `dependencyType`
- dependency `status`
- decision record `status`
- research doc `sourceType`
- research doc `status`
- evidence link `evidenceType`
- readiness evaluation `entityType`
- readiness evaluation `evaluationType`
- readiness evaluation `result`
- readiness gap `severity`
- handoff `sourceEntityType`
- handoff `targetSystem`
- handoff `handoffType`
- handoff `status`
- status history `entityType`
- audit run `auditType`
- audit run `targetEntityType`
- audit run `result`
- audit gap `severity`
- audit gap `status`
- external link `sourceEntityType`
- external link `targetSystem`
- external link `linkType`

---

## Severity Ordering Rule

Where list surfaces sort by severity, they must not use raw text ordering.

The canonical severity rank from highest to lowest is:

- `critical` = 4
- `major` = 3
- `minor` = 2
- `advisory` = 1

Raw lexical ordering on severity values is incorrect and must not be used.

---

## 1. `Project`

### Purpose
Project-scoped planning anchor.

### Columns
- `id uuid primary key`
- `key text not null`
- `name text not null`
- `status text not null default 'active'`
- `description text null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- unique: `(key)`
- `key` must be non-empty
- `key` must conform to the governed key format
- `name` must be non-empty

### Indexes
- unique index on `key`
- index on `(status, updatedAt desc, id)`

### Allowed mutations
- create
- bounded update of `name`, `description`
- explicit status transition route or governed mutation path for `status`
- no delete in first pass

---

## 2. `Objective`

### Purpose
Project-scoped major outcome.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `key text not null`
- `title text not null`
- `description text null`
- `status text not null default 'proposed'`
- `priority integer not null default 100`
- `targetStartAt timestamptz null`
- `targetEndAt timestamptz null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- unique: `(projectId, key)`
- `key` must conform to the governed key format
- `title` must be non-empty
- if both target dates exist, `targetEndAt >= targetStartAt`

### Indexes
- unique index on `(projectId, key)`
- index on `(projectId, status, priority, updatedAt desc, id)`

### Allowed mutations
- create
- bounded update of `title`, `description`, `priority`, `targetStartAt`, `targetEndAt`
- explicit status transition route or governed mutation path
- no delete in first pass

---

## 3. `Initiative`

### Purpose
Project-scoped bounded body of work.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `objectiveId uuid null references Objective(id)`
- `key text not null`
- `title text not null`
- `description text null`
- `status text not null default 'proposed'`
- `priority integer not null default 100`
- `targetSystem text null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- unique: `(projectId, key)`
- `key` must conform to the governed key format
- `title` must be non-empty
- if `objectiveId` is not null, the referenced Objective must belong to the same `projectId`

### Indexes
- unique index on `(projectId, key)`
- index on `(projectId, objectiveId)`
- index on `(projectId, status, priority, updatedAt desc, id)`
- index on `(projectId, targetSystem, updatedAt desc, id)`

### Allowed mutations
- create
- bounded update of `title`, `description`, `objectiveId`, `priority`, `targetSystem`
- explicit status transition route or governed mutation path
- no delete in first pass

---

## 4. `WorkItem`

### Purpose
Project-scoped planning or handoff-preparation unit.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `initiativeId uuid null references Initiative(id)`
- `key text not null`
- `title text not null`
- `description text null`
- `type text not null`
- `status text not null default 'proposed'`
- `readinessState text not null default 'unevaluated'`
- `targetSystem text not null`
- `blocked boolean not null default false`
- `blockedReason text null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- unique: `(projectId, key)`
- `key` must conform to the governed key format
- `title` must be non-empty
- if `initiativeId` is not null, the referenced Initiative must belong to the same `projectId`
- if `blocked = true`, `blockedReason` must be non-null and non-empty; this is enforced by the governed mutation path rather than a DB-level check in the first pass

### Indexes
- unique index on `(projectId, key)`
- index on `(projectId, initiativeId)`
- index on `(projectId, status, updatedAt desc, id)`
- index on `(projectId, readinessState, updatedAt desc, id)`
- index on `(projectId, targetSystem, updatedAt desc, id)`
- index on `(projectId, blocked, updatedAt desc, id)`

### Allowed mutations
- create
- bounded update of `title`, `description`, `initiativeId`, `type`, `targetSystem`, `blocked`, `blockedReason`
- server-managed update of `readinessState` only through governed readiness evaluation behavior
- explicit status transition route or governed mutation path
- no delete in first pass

---

## 5. `Dependency`

### Purpose
Explicit dependency relationship between Project V records.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `sourceEntityType text not null`
- `sourceEntityId uuid not null`
- `targetEntityType text not null`
- `targetEntityId uuid not null`
- `dependencyType text not null`
- `status text not null default 'active'`
- `rationale text null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- source and target entities must belong to the same `projectId`
- source and target must not be identical in both type and id
- the unique index on `(projectId, sourceEntityType, sourceEntityId, targetEntityType, targetEntityId, dependencyType)` enforces deduplication structurally; duplicate logical dependencies within the same scope must fail with a constraint violation

### Indexes
- unique index on `(projectId, sourceEntityType, sourceEntityId, targetEntityType, targetEntityId, dependencyType)`
- index on `(projectId, sourceEntityType, sourceEntityId)`
- index on `(projectId, targetEntityType, targetEntityId)`
- index on `(projectId, status, updatedAt desc, id)`

### Allowed mutations
- create
- bounded update of `status`, `rationale`
- no delete in first pass unless a later ADR explicitly permits dependency removal semantics

---

## 6. `DecisionRecord`

### Purpose
Recoverable decision and rationale.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `entityType text null`
- `entityId uuid null`
- `title text not null`
- `decisionSummary text not null`
- `rationale text not null`
- `status text not null default 'recorded'`
- `actor text not null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- if `entityType` and `entityId` are present, the referenced entity must belong to the same `projectId`
- `title`, `decisionSummary`, and `rationale` must be non-empty

### Indexes
- index on `(projectId, createdAt desc, id)`
- index on `(projectId, entityType, entityId, createdAt desc, id)`
- index on `(projectId, status, createdAt desc, id)`

### Allowed mutations
- create
- bounded governed status update only (`recorded -> superseded`); this transition must also write a `StatusHistory` row in the same transaction
- no delete in first pass

---

## 7. `ReadinessEvaluation`

### Purpose
Inspectable readiness evaluation.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `entityType text not null`
- `entityId uuid not null`
- `evaluationType text not null`
- `result text not null`
- `rulePackage text not null`
- `summary text not null`
- `createdAt timestamptz not null default now()`

### Constraints
- evaluated entity must belong to the same `projectId`
- `summary` must be non-empty
- no evaluation may be stored without inspectable basis according to application rules

### Summary generation rule
`summary` is server-generated by the evaluation execution logic. Callers must not supply it as input. The server must produce a non-empty summary as part of completing any readiness evaluation; an evaluation may not be persisted without one.

### Indexes
- index on `(projectId, entityType, entityId, createdAt desc, id)`
- index on `(projectId, result, createdAt desc, id)`
- index on `(projectId, evaluationType, createdAt desc, id)`

### Allowed mutations
- create
- no generic update in first pass
- no delete in first pass

---

## 8. `ReadinessGap`

### Purpose
Explicit readiness deficiency or blocker.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `readinessEvaluationId uuid not null references ReadinessEvaluation(id)`
- `severity text not null`
- `description text not null`
- `remediationSuggestion text null`
- `resolved boolean not null default false`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- linked readiness evaluation must belong to the same `projectId`
- `description` must be non-empty

### Indexes
- index on `(projectId, readinessEvaluationId)`
- index on `(projectId, resolved, severity, createdAt desc, id)`

### Resolved toggle rule
`resolved` may be set from `false` to `true` by a caller through the governed PATCH route. Setting `resolved` back to `false` is also allowed in the first pass — there is no one-way lifecycle on this field yet.

### Allowed mutations
- create
- bounded update of `resolved`, `remediationSuggestion`
- no delete in first pass

---

## 9. `ResearchDoc`

### Purpose
Planning-support research artifact.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `title text not null`
- `sourceType text not null`
- `storageLocator text not null`
- `status text not null`
- `summary text null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- `title` must be non-empty
- `storageLocator` must be non-empty

### Indexes
- index on `(projectId, status, updatedAt desc, id)`
- index on `(projectId, sourceType, updatedAt desc, id)`

### Allowed mutations
- create
- bounded update of `title`, `status`, `summary`, `storageLocator`
- no delete in first pass

---

## 10. `EvidenceLink`

### Purpose
Directional link from planning truth to supporting evidence.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `sourceEntityType text not null`
- `sourceEntityId uuid not null`
- `evidenceType text not null`
- `targetLocator text not null`
- `note text null`
- `relevanceScore integer null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- source entity must belong to the same `projectId`
- `targetLocator` must be non-empty
- if `relevanceScore` exists, it must remain in the governed range `0..100`

### Indexes
- index on `(projectId, sourceEntityType, sourceEntityId, createdAt desc, id)`
- index on `(projectId, evidenceType, createdAt desc, id)`
- index on `(projectId, sourceEntityType, sourceEntityId, updatedAt desc, id)`

### Allowed mutations
- create
- bounded update of `note`, `relevanceScore`
- no delete in first pass

---

## 11. `Handoff`

### Purpose
Bounded transition of responsibility.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `sourceEntityType text not null`
- `sourceEntityId uuid not null`
- `targetSystem text not null`
- `handoffType text not null`
- `status text not null default 'proposed'`
- `readinessBasisSummary text null`
- `createdAt timestamptz not null default now()`
- `completedAt timestamptz null`
- `updatedAt timestamptz not null default now()`

### Constraints
- source entity must belong to the same `projectId`
- `targetSystem` and `handoffType` must use controlled vocabularies
- `completedAt` must not precede `createdAt`

### Indexes
- index on `(projectId, status, createdAt desc, id)`
- index on `(projectId, targetSystem, createdAt desc, id)`
- index on `(projectId, sourceEntityType, sourceEntityId, createdAt desc, id)`

### Allowed mutations
- create
- bounded update of `readinessBasisSummary`
- explicit status transition route or governed mutation path
- no delete in first pass

### Completed-at atomicity rule
When a status transition sets `Handoff.status` to `completed`, the same governed transition must set `completedAt` in the same transaction. A handoff may not remain in `completed` status with a null `completedAt`.

---

## 12. `StatusHistory`

### Purpose
Recoverable history for meaningful state changes.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `entityType text not null`
- `entityId uuid not null`
- `previousStatus text null`
- `newStatus text not null`
- `reason text null`
- `actor text not null`
- `createdAt timestamptz not null default now()`

### Constraints
- referenced entity must belong to the same `projectId`
- `newStatus` must be non-empty
- history entries must be created atomically with the transitions they describe when history is required

### Indexes
- index on `(projectId, entityType, entityId, createdAt desc, id)`
- index on `(projectId, createdAt desc, id)`

### Allowed mutations
- create
- no update in first pass
- no delete in first pass

---

## 13. `AuditRun`

### Purpose
Project-scoped BYDA-style audit execution.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `auditType text not null`
- `targetEntityType text null`
- `targetEntityId uuid null`
- `result text not null`
- `summary text not null`
- `startedAt timestamptz null`
- `completedAt timestamptz null`
- `createdAt timestamptz not null default now()`

### Constraints
- if `targetEntityType` and `targetEntityId` are present, the referenced entity must belong to the same `projectId`
- `summary` must be non-empty
- `completedAt` must not precede `startedAt` where both exist

### Indexes
- index on `(projectId, auditType, createdAt desc, id)`
- index on `(projectId, result, createdAt desc, id)`
- index on `(projectId, targetEntityType, targetEntityId, createdAt desc, id)`

### Allowed mutations
- create
- bounded update of `completedAt` where the audit execution path requires completion stamping
- bounded governed update of `result` only where a prior audit is explicitly invalidated into `stale`
- bounded governed update of `summary` only where audit execution finalization or invalidation requires it
- no delete in first pass

### Controlled-vocabulary note
`auditType` and `result` must use the governed value sets in `controlled-vocabularies.md`.
`targetEntityType` uses the allowed value set defined in `polymorphic-reference-enforcement.md`.

### Note
Execution-adjacent audit types remain bounded planning-side interpretations only. They do not make Project V the owner of execution truth.

---

## 14. `AuditGap`

### Purpose
Project-scoped audit deficiency or failure.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `auditRunId uuid not null references AuditRun(id)`
- `severity text not null`
- `description text not null`
- `remediation text null`
- `status text not null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- linked audit run must belong to the same `projectId`
- `description` must be non-empty

### Indexes
- index on `(projectId, auditRunId)`
- index on `(projectId, status, severity, createdAt desc, id)`

### Allowed mutations
- create
- bounded update of `status`, `remediation`
- no delete in first pass

---

## 15. `ExternalLink`

### Purpose
Project-scoped thin external linkage for planning-side traceability and handoff context.

### Columns
- `id uuid primary key`
- `projectId uuid not null references Project(id)`
- `sourceEntityType text not null`
- `sourceEntityId uuid not null`
- `targetSystem text not null`
- `linkType text not null`
- `url text not null`
- `externalId text null`
- `label text null`
- `createdAt timestamptz not null default now()`
- `updatedAt timestamptz not null default now()`

### Constraints
- source entity must belong to the same `projectId`
- `url` must be non-empty and must begin with `https://`; format validation is enforced at the application layer
- unique: `(projectId, sourceEntityType, sourceEntityId, targetSystem, linkType, url)`
- linkage remains bounded reference truth only; it must not be used as a covert execution-state store

### Indexes
- unique index on `(projectId, sourceEntityType, sourceEntityId, targetSystem, linkType, url)`
- index on `(projectId, sourceEntityType, sourceEntityId, createdAt desc, id)`
- index on `(projectId, targetSystem, linkType, createdAt desc, id)`
- index on `(projectId, updatedAt desc, id)`

### Allowed mutations
- create
- bounded update of `label`, `url`, `externalId`
- no delete in first pass

---

## Archived-Parent Integrity Rule

In the first pass, archived parent records should freeze normal forward child growth beneath them.

That means:

- do not create child objectives, initiatives, or work items under an archived parent
- do not re-parent active children under an archived parent

If an exception is later needed, it should be modeled explicitly.

---

## `updatedAt` Maintenance Rule

Where a first-pass canonical table has an `updatedAt` column, Project V should update that column through the application/service mutation path in the same transaction as the governed write.

The first-pass posture does not depend on database triggers for `updatedAt`.

---

## Cross-Table Integrity Rules

### Same-project relation rule
Where one project-scoped record references another, both must belong to the same `projectId` unless a later ADR explicitly introduces a bounded exception.

### Orphan prevention rule
Project-scoped child records must not outlive the project anchor without an explicit archival or cascade strategy.

### Atomic state/history rule
Where a transition requires status history, the state change and history row must be written in the same transaction.

### Atomic completed-at rule
Where a transition to `completed` requires a completion timestamp, the state change and completion timestamp must be written in the same transaction.

### Deterministic ordering support rule
All list surfaces must be supportable by explicit ordering backed by stable tie-breakers.

### Thin external-link rule
External linkage is permitted because it preserves bounded planning-side traceability and handoff context. It must not widen into a rich execution model inside Project V.

---

## Mutation Summary

### Create allowed in first pass
- Project
- Objective
- Initiative
- WorkItem
- Dependency
- DecisionRecord
- ReadinessEvaluation
- ReadinessGap
- ResearchDoc
- EvidenceLink
- Handoff
- StatusHistory
- AuditRun
- AuditGap
- ExternalLink

### Generic update allowed in first pass
- Project (bounded fields)
- Objective (bounded fields)
- Initiative (bounded fields)
- WorkItem (bounded fields)
- Dependency (bounded fields)
- DecisionRecord (governed status transition only; `recorded -> superseded` with StatusHistory row required)
- ReadinessGap (bounded fields)
- ResearchDoc (bounded fields)
- EvidenceLink (bounded fields)
- Handoff (bounded fields)
- AuditRun (bounded finalization / invalidation fields only)
- AuditGap (bounded fields)
- ExternalLink (bounded fields)

### Explicit status-transition path preferred
- Project when lifecycle status changes are governed explicitly
- Objective
- Initiative
- WorkItem
- Handoff

### No delete in first pass
No canonical first-pass table should expose destructive delete behavior until deletion semantics are explicitly modeled and hammered.

---

## Final Rule

This schema specification is intentionally strict.

If implementation pressure suggests broadening it casually, the correct response is governance review, not improvisation.

This document is the concrete companion to `schema-authority.md`.
If future implementation wants to diverge from exact first-pass table shape, columns, constraints, or mutation posture, the divergence must be reviewed explicitly rather than introduced by migration convenience.

---

## Human-In-The-Loop Principle

Schema detail is implementation-shaping authority.

Human review may be required where schema change would:

- broaden Project V ownership
- add new canonical record families
- weaken multi-project integrity
- deepen external-link posture into execution modeling
- collapse readiness, audit, and handoff boundaries

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- Project V schema is intentionally explicit and small
- every retained record family exists for a governed planning or orchestration reason
- exact schema detail is not a local implementation preference
- same-project integrity is structural, not optional
- readiness and audit remain separate families
- ExternalLink is the thin bounded replacement for older heavier external-linkage assumptions
- delete semantics are intentionally deferred rather than casually allowed

If implementation tries to widen Project V schema because it seems convenient, this specification is being violated.

---

## Usage

This document should be used:

- when writing migrations for first-pass Project V schema
- when reviewing whether a proposed column or constraint belongs in first-pass authority
- when writing API family docs that depend on exact table shape
- when reviewing whether mutation behavior remains inside governed bounds
- when checking whether old legacy assumptions still match current shared-root authority

---

## Related Docs

- `schema-authority.md`
- `controlled-vocabularies.md`
- `status-transitions.md`
- `readiness-methodology.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `schema-governance.md`
- `mcp-surface.md`
- `github-integration.md`
- `project-v.md`
- `system-invariants.md`
- `multi-project-doctrine.md`
- `v-forge-integration.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/decision-continuity-doctrine.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
