# Schema Authority

## Purpose

This document defines the canonical schema authority for Project V.

It exists to answer:

```text
What records does Project V canonically own, what does each record mean, how is project scope enforced, and what structural rules must the schema preserve?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the canonical first-pass schema shape Project V is allowed to own
- the meaning and ownership posture of each retained canonical record family
- the structural rules the schema must preserve
- how project scope, cross-record integrity, and bounded external linkage must be enforced
- the anti-drift constraints operators and LLMs must preserve when extending Project V schema

---

## Out of Scope

This document does not define:

- exact columns, exact SQL types, or exact indexes for every field
- detailed migration sequencing
- detailed endpoint contracts
- VEDA schema design
- V Forge schema design

Those belong in more specific schema-specification, migration, API, and system-specific docs.

---

## System

- project-v

---

## Core Rule

Project V schema must model only canonical planning and orchestration truth that Project V owns.

Project V schema must not model:

- canonical observability truth
- canonical evidence truth that belongs to VEDA
- canonical execution truth
- convenience copies of another bounded system's state
- deep implementation workflow structures that belong to V Forge

The Project V schema must remain:

- multi-project-safe
- explicit
- intentionally small
- queryable by real operator workflows
- hard to drift casually

A handoff is a transition of responsibility, not shared ownership.
Project V may preserve bounded post-handoff visibility and bounded external linkage, but it does not become the owner of execution truth after handoff.

---

## Schema Authority Rule

This document is the canonical authority for the retained first-pass Project V schema shape.

If implementation, migrations, route design, or convenience schema ideas diverge from this document, the divergence must be reviewed explicitly.

Schema authority must not be inferred from:

- ad hoc route payloads
- migration convenience
- local implementation assumptions
- old bootstrap-era schema shapes
- one-off operator expectations

If a proposed record family is not clearly justified here or in an explicitly subordinate schema-specification doc, it is not yet governed schema.

The detailed companion specification for exact columns, relations, constraints, and index posture lives in `schema-specification.md`.
That companion remains subordinate to this authority doc and must not weaken the ownership and boundary rules defined here.

---

## Scope Classification Rule

Every Project V table or canonical record family must be classifiable as one of:

- **project-scoped**
- **intentionally global**
- **system metadata**

### Rule
Project-scoped tables must belong to exactly one project.
Global tables must be rare and justified.
System metadata must not become a loophole for storing project truth or cross-system convenience state.

---

## Canonical First-Pass Record Families

The canonical first-pass Project V schema should retain these record families:

1. `Project`
2. `Objective`
3. `Initiative`
4. `WorkItem`
5. `Dependency`
6. `DecisionRecord`
7. `ReadinessEvaluation`
8. `ReadinessGap`
9. `ResearchDoc`
10. `EvidenceLink`
11. `Handoff`
12. `StatusHistory`
13. `AuditRun`
14. `AuditGap`
15. `ExternalLink`

These are the retained first-pass canonical families because they directly support planning truth, orchestration truth, readiness truth, handoff truth, audit truth, and bounded planning-side traceability.

---

## 1. `Project`

### Scope
Project-scoped planning anchor.

### Purpose
Represents the planning identity of a project inside Project V.

### Required traits
- stable primary key
- stable `key`
- name
- status
- description or summary field
- created / updated timestamps

### Constraints
- `key` must be globally unique inside Project V
- `key` must conform to the governed key format
- no row may be created without the required identifying fields

### Notes
`Project` is Project V's planning anchor, not a copy of all other system-specific project truth.

---

## 2. `Objective`

### Scope
Project-scoped.

### Purpose
Represents a major outcome a project is pursuing.

### Required traits
- primary key
- `projectId`
- stable per-project `key`
- title
- description
- status
- priority
- horizon or target-period fields where governed
- created / updated timestamps

### Constraints
- every row belongs to exactly one project
- uniqueness must be scoped at least to `(projectId, key)`
- reads and writes must enforce project ownership

---

## 3. `Initiative`

### Scope
Project-scoped.

### Purpose
Represents a bounded body of work advancing an objective.

### Required traits
- primary key
- `projectId`
- optional `objectiveId`
- stable per-project `key`
- title
- description
- status
- priority
- target-system classification where appropriate
- created / updated timestamps

### Constraints
- every row belongs to exactly one project
- if `objectiveId` exists, the referenced objective must belong to the same project
- uniqueness must be scoped at least to `(projectId, key)`

---

## 4. `WorkItem`

### Scope
Project-scoped.

### Purpose
Represents a concrete unit of planning or handoff-preparation work.

### Required traits
- primary key
- `projectId`
- optional `initiativeId`
- stable per-project `key`
- title
- description
- type
- status
- readiness state
- target-system classification
- blocked summary or blocked flag where governed
- created / updated timestamps

### Constraints
- every row belongs to exactly one project
- if `initiativeId` exists, the referenced initiative must belong to the same project
- uniqueness must be scoped at least to `(projectId, key)`
- target-system classification must use a controlled vocabulary

### Notes
`WorkItem` does not become the canonical owner of execution truth.

---

## 5. `Dependency`

### Scope
Project-scoped.

### Purpose
Represents an explicit dependency between Project V records.

### Required traits
- primary key
- `projectId`
- source record reference
- target record reference
- dependency type
- status
- optional rationale or notes
- created / updated timestamps

### Constraints
- source and target must belong to the same project unless an explicitly modeled bounded exception exists later
- illegal cross-project dependencies must fail
- duplicate logical dependencies inside a project must be prevented

### Notes
Dependencies must not live only in prose.

---

## 6. `DecisionRecord`

### Scope
Project-scoped.

### Purpose
Represents a recoverable planning or orchestration decision.

### Required traits
- primary key
- `projectId`
- optional related entity references
- title
- decision summary
- rationale
- status
- actor or origin field
- created timestamp
- updated timestamp where governed

### Constraints
- related referenced entities must belong to the same project where applicable
- meaningful transitions that require decision continuity must have an explicit path to align with decision history

---

## 7. `ReadinessEvaluation`

### Scope
Project-scoped.

### Purpose
Represents an inspectable evaluation of whether a record is ready to move forward.

### Required traits
- primary key
- `projectId`
- evaluated entity reference
- evaluation type
- result
- rule package or methodology reference
- summary
- created timestamp

### Constraints
- evaluated entity must belong to the same project
- evaluation must preserve inspectable basis
- repeated evaluation against unchanged inputs should be reproducible

### Notes
Readiness remains planning truth. It does not transfer execution ownership into Project V.

---

## 8. `ReadinessGap`

### Scope
Project-scoped.

### Purpose
Represents a missing condition, blocker, or deficiency produced by a readiness evaluation.

### Required traits
- primary key
- `projectId`
- `readinessEvaluationId`
- severity
- description
- remediation guidance
- resolved state
- created / updated timestamps

### Constraints
- evaluation and gap must belong to the same project
- orphan gaps must be impossible

### Notes
Readiness gaps remain separate from audit gaps.

---

## 9. `ResearchDoc`

### Scope
Project-scoped.

### Purpose
Represents a planning-support research artifact used by Project V.

### Required traits
- primary key
- `projectId`
- title
- source type
- storage locator or path reference
- status
- summary fields where governed
- created / updated timestamps

### Constraints
- every row belongs to exactly one project
- imported or external provenance should remain visible

### Notes
Research docs support planning truth. They are not observability truth.

---

## 10. `EvidenceLink`

### Scope
Project-scoped.

### Purpose
Represents a directional link from planning truth to supporting evidence.

### Required traits
- primary key
- `projectId`
- source planning record reference
- evidence type
- target reference or locator
- note
- optional relevance or confidence classification
- created timestamp

### Constraints
- the source planning record must belong to the same project
- evidence links must not overclaim canonical ownership of referenced external truth

### Notes
Evidence links support planning, audit, and handoff rationale. They do not make Project V the owner of external truth.

---

## 11. `Handoff`

### Scope
Project-scoped.

### Purpose
Represents a bounded transition from Project V into another system or surface.

### Required traits
- primary key
- `projectId`
- source entity reference
- target system classification
- handoff type
- readiness basis summary or reference
- status
- created / completed timestamps

### Constraints
- source entity must belong to the same project
- target system classification must use a controlled vocabulary
- handoffs must not collapse ownership between systems

### Notes
A handoff is a transition of responsibility. Project V may preserve orchestration-side visibility after handoff, but execution truth belongs to the receiving system.

---

## 12. `StatusHistory`

### Scope
Project-scoped.

### Purpose
Represents recoverable status history for meaningful planning and orchestration state changes.

### Required traits
- primary key
- `projectId`
- entity type
- entity id
- prior status
- new status
- reason or transition summary
- actor or origin field
- created timestamp

### Constraints
- referenced entity must belong to the same project
- state/history alignment must be enforceable by application logic and transaction boundaries
- status history must not exist for a project-scoped entity in another project
- status history should be generated only for record families with meaningful state-change governance consequences; first-pass candidates include `Objective`, `Initiative`, `WorkItem`, `Handoff`, and `AuditRun`
- thin linkage records such as `EvidenceLink` and `ExternalLink` do not require status history in the first pass
- adding a new entity type to status-history tracking is a schema governance event

### Notes
This record family exists because workflow and invariants require recoverable history around meaningful Project V state changes. It does not make Project V the owner of downstream execution history.
ReadinessEvaluation records are superseded by new evaluations, not transitioned. No StatusHistory is written for them.

---

## 13. `AuditRun`

### Scope
Project-scoped.

### Purpose
Represents a bounded BYDA-style audit execution against a project-scoped target.

### Required traits
- primary key
- `projectId`
- audit type
- optional target entity reference
- result
- summary
- started / completed timestamps where governed
- created timestamp

### Constraints
- target entity must belong to the same project where a target is present
- audit records remain separate from readiness records
- audit invalidation or staleness behavior must remain explicit rather than assumed
- the `auditType` field must use the controlled BYDA vocabulary defined in `byda-in-project-v.md`; first-pass governed values are `research`, `planning`, `implementation_readiness`, `code_alignment`, `handoff`, and `hygiene`
- adding a new audit type is a schema and doctrine governance event, not a local implementation convenience

### Notes
Audit remains planning and governance truth. Any execution-adjacent audit type must remain bounded and non-authoritative with respect to V Forge truth.

---

## 14. `AuditGap`

### Scope
Project-scoped.

### Purpose
Represents a gap, failure, or deficiency identified during an audit run.

### Required traits
- primary key
- `projectId`
- `auditRunId`
- severity
- description
- remediation guidance
- status
- created / updated timestamps

### Constraints
- linked audit run must belong to the same project
- audit gaps remain separate from readiness gaps

### Notes
Where audit cannot answer a required question honestly, the correct response is an explicit audit gap rather than hidden ambiguity.

---

## 15. `ExternalLink`

### Scope
Project-scoped.

### Purpose
Represents a thin, explicit external reference used for planning-side traceability, handoff context, or bounded orchestration visibility.

### Required traits
- primary key
- `projectId`
- source entity reference
- target system classification
- link type
- URL or external identifier
- optional label or summary
- created timestamp
- updated timestamp where mutation exists

### Constraints
- source entity must belong to the same project
- external linkage remains planning-side traceability, not canonical execution truth
- the model must remain thin; it must not expand into rich execution-state storage by stealth

### Notes
`ExternalLink` is not part of Project V canonical planning truth in the same way that `Project`, `DecisionRecord`, or `ReadinessEvaluation` are. It is a governed Project V record family for bounded external reference and traceability support. It exists because Project V may preserve thin external linkage, not because the referenced foreign truth has become Project V-owned truth.
This record family intentionally replaces heavier GitHub-specific assumptions. Project V may keep bounded external references, but it must not normalize rich execution modeling inside its own schema before V Forge-side receiving and execution boundary doctrine is clearer.
The concrete first-pass shape and constraints for this family are defined in `schema-specification.md`, while the GitHub-specific boundary posture and rationale live in `github-integration.md`.

---

## Possible Global Tables

Global tables must be rare.

The only acceptable early candidates are things like:

- rule packages
- controlled vocabularies
- narrowly scoped system configuration

### Rule
A global table must justify why project scope would be incorrect.
Global convenience must not become a loophole for mixed ownership or cross-project leakage.
Controlled vocabularies governing fields such as target-system classification, audit type, and handoff type may be represented as global tables or as governed enum/check-constraint definitions in subordinate schema-specification work, but in either case the vocabulary must remain explicit, governed, and not casually expandable.

---

## Required Common Fields Posture

Project-scoped record families should strongly prefer the following where relevant:

- `id`
- `projectId`
- `key` where human-meaningful stable identity helps
- `status`
- `createdAt`
- `updatedAt`

Not every record family needs every field, but omission must be deliberate rather than accidental.

---

## Integrity Rules

### 1. No orphaned project-scoped records

A project-scoped row must not exist without a valid project anchor.

### 2. No illegal cross-project relations

If one project-scoped row references another, project compatibility must be enforced.

### 3. Canonical scope must be enforceable structurally

Critical integrity should be enforced at the database layer where practical, not only in application logic.

### 4. Uniqueness must match real ownership scope

If a key is unique only within a project, uniqueness must include `projectId`.

### 5. Important planning state must remain explicit

Do not hide important planning or orchestration state in vague notes or unstructured metadata.

### 6. Status changes and history must stay aligned

Where a transition requires recoverable history, the state change and history record must be created atomically or be guaranteed by an equally explicit governed mechanism.

### 7. External linkage must stay thin

External references are allowed because they preserve bounded orchestration visibility and planning-side traceability.
They must not become a loophole for recreating execution models inside Project V.

### 8. Audit and readiness must remain separate

Audit records and readiness records may relate to one another.
They must not be silently collapsed into one undifferentiated family.

---

## Index Posture

The first-pass schema should be indexable for real multi-project access patterns.

At minimum, schema design should support queries such as:

- list objectives for a project
- list initiatives for a project
- list open work items for a project
- list blocked work items for a project
- list readiness gaps for a project or initiative
- list handoffs by target system
- list decisions by project and time
- list status history for a project and entity
- list bounded external links for a project and source entity
- list audit runs and audit gaps for a project and target entity

This implies deliberate indexing on:

- `projectId`
- common status filters
- common relation joins
- common ordering fields
- history lookup fields such as entity type and entity id

---

## Ordering Rule

List surfaces must have deterministic ordering.

Schema design must support predictable ordering with stable tie-breakers rather than relying on implicit database behavior.

---

## JSON Rule

JSON may be used only where flexible payload storage is genuinely justified, such as:

- imported external payload traces
- bounded metadata with truly variable shape

JSON must not become a substitute for unresolved schema design.

### Rule
If a concept is important enough to govern, query, validate, or classify repeatedly, it probably needs explicit schema rather than a JSON hiding place.

---

## Freeze Posture

This first-pass schema set should be treated as the governed base.

After approval:

- endpoint and mutation design should conform to it
- later schema additions should be exceptional
- schema expansion requires governance review and hammer updates

This is not a ban on future change.
It is a ban on casual schema drift.

---

## Companion Implementation Rule

Before implementation begins in earnest, each retained canonical record family above should be converted into a more specific schema specification with:

- exact columns
- exact types
- exact relations
- exact constraints
- exact indexes
- exact allowed mutations

That more specific specification remains subordinate to this authority doc.
It must not silently replace or override it.

Record families or concepts still under refoundation pressure should be narrowed or deferred before being hardened into detailed first-pass specification.

This companion-spec conversion is now carried by `schema-specification.md` for the current first-pass retained families.
Further expansion should patch that companion doc rather than re-opening authority posture here unless ownership, scope, or schema-family meaning changes.

---

## Human-In-The-Loop Principle

Schema authority is governance-sensitive because schema shape determines what Project V can and cannot become.

Human review may be required where schema change would:

- broaden Project V ownership
- introduce new project-scoped record families
- increase cross-system linkage depth
- weaken multi-project integrity
- add record families that resemble execution truth or observability truth

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- Project V schema must stay strictly inside planning and orchestration truth
- first-pass canonical record families are intentionally small and explicit
- project scope and bounded ownership are structural requirements, not style preferences
- audit, readiness, handoff, and traceability records are allowed because they support planning truth
- external linkage must remain thin and must not become a shadow execution model
- schema expansion requires explicit governance rather than implementation convenience

If schema design makes Project V broader, more execution-shaped, less project-safe, or harder to classify, the doctrine is wrong.

---

## Usage

This document should be used:

- when deciding whether a proposed record family belongs in Project V schema
- when evaluating whether a schema concept is canonical, derived, or out of bounds
- when writing subordinate schema-specification or migration docs
- when reviewing whether schema ideas preserve multi-project integrity and ownership boundaries
- when rejecting convenience-driven schema drift

---

## Related Docs

- `project-v.md`
- `system-invariants.md`
- `schema-specification.md`
- `github-integration.md`
- `byda-in-project-v.md`
- `implementation-traceability.md`
- `data-boundaries.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
