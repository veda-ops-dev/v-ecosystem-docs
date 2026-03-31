# Polymorphic Reference Enforcement

## Purpose

This document defines how Project V enforces polymorphic references safely.

It exists to answer:

```text
How do tables that use entityType + entityId references stay valid, same-project, and implementation-safe when normal database foreign keys cannot enforce them directly?
```

Read this with:

- `schema-authority.md`
- `schema-specification.md`
- `multi-project-doctrine.md`
- `system-invariants.md`
- `controlled-vocabularies.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the central enforcement strategy for polymorphic references in Project V
- the first-pass tables that use polymorphic references
- the allowed entity-type sets per table
- same-project enforcement requirements
- write-time and read-time enforcement posture
- error and non-leakage posture
- hammer expectations for polymorphic reference behavior

---

## Out of Scope

This document does not define:

- endpoint family request and response shapes
- migration sequencing
- generic API conventions beyond what polymorphic enforcement requires
- VEDA or V Forge polymorphic behavior

Those belong in API docs, migration docs, and system-specific authority docs.

---

## System

- project-v

---

## Core Rule

Project V uses polymorphic references in several first-pass tables.

That means some records point at a target through:

- `entityType`
- `entityId`

rather than a single normal foreign key.

Because PostgreSQL cannot enforce this shape with a single native foreign key, Project V must enforce it deliberately and consistently.

Implementation must not invent different enforcement strategies in different routes, services, or tools.

Polymorphic resolution in Project V exists to protect planning and orchestration truth.
It does not widen Project V into an execution-system surrogate.

---

## Tables Affected

First-pass tables that use polymorphic references include:

- `Dependency`
- `DecisionRecord`
- `ReadinessEvaluation`
- `EvidenceLink`
- `Handoff`
- `StatusHistory`
- `AuditRun`
- `ExternalLink`

These tables are valid only if the referenced entity:

- exists
- belongs to the same project
- matches the declared `entityType`
- is allowed for that table and field

---

## Canonical Enforcement Strategy

Project V must use a central polymorphic-reference resolver in application logic.

That resolver must:

1. map each allowed `entityType` to a canonical Project V table
2. verify the referenced row exists
3. verify the referenced row belongs to the supplied `projectId`
4. fail deterministically if the row does not exist or belongs to another project
5. return a normalized resolution result for the calling mutation path

This logic must not be reimplemented differently in each route handler.
A route may call the resolver. It must not replace it with local guesswork.

---

## Resolver Output Contract

The central resolver should return a normalized result shape that gives the caller enough information to proceed safely.

At minimum, the resolved result should include:

- normalized `entityType`
- resolved canonical table name
- resolved `entityId`
- resolved owning `projectId`
- whether the row exists in current project scope

The resolver must not return partial success for an illegal reference shape.
If the reference is invalid, the resolver returns failure and the mutation path must stop.

---

## Allowed Entity Types By Table

### `Dependency`
Allowed `sourceEntityType` and `targetEntityType` values:

- `objective`
- `initiative`
- `work_item`
- `handoff`

### `DecisionRecord`
Allowed `entityType` values:

- `objective`
- `initiative`
- `work_item`
- `handoff`

### `ReadinessEvaluation`
Allowed `entityType` values:

- `objective`
- `initiative`
- `work_item`
- `handoff`

### `EvidenceLink`
Allowed `sourceEntityType` values:

- `objective`
- `initiative`
- `work_item`
- `handoff`
- `decision_record`
- `research_doc`

### `Handoff`
Allowed `sourceEntityType` values:

- `objective`
- `initiative`
- `work_item`

### `StatusHistory`
Allowed `entityType` values:

- `project`
- `objective`
- `initiative`
- `work_item`
- `handoff`
- `decision_record`
- `audit_run`

### `AuditRun`
Allowed `targetEntityType` values:

- `project`
- `objective`
- `initiative`
- `work_item`
- `handoff`

### `ExternalLink`
Allowed `sourceEntityType` values:

- `objective`
- `initiative`
- `work_item`
- `handoff`
- `decision_record`
- `research_doc`
- `audit_run`

### Notes on `ExternalLink`

External linkage remains thin and bounded.
Allowing an entity type here does not imply that the entity becomes the owner of downstream execution truth.

`audit_run` is intentionally allowed here because ExternalLinks may reference external artifacts that support or document audit findings, such as GitHub issues, reports, or other bounded external records.
It is intentionally absent from `EvidenceLink` because evidence links point to supporting planning evidence, not audit outputs.

If a new entity type is introduced later, update:

- `controlled-vocabularies.md`
- this enforcement doc
- affected schema/API docs
- hammer expectations

---

## Same-Project Enforcement Rule

Every polymorphic reference must resolve inside the same `projectId` as the owning row.

Examples:

- a `Dependency` row in project A may not point to an `Initiative` in project B
- a `ReadinessEvaluation` row in project A may not evaluate a `WorkItem` in project B
- a `StatusHistory` row in project A may not record a transition for a `Handoff` in project B
- an `ExternalLink` row in project A may not attach to a `WorkItem` in project B

If the referenced row exists but belongs to another project, the operation must fail without cross-project existence leakage.

---

## Special-Case Rule: `AuditRun.targetEntityType = 'project'`

Most polymorphic tables resolve same-project ownership by checking:

```text
resolvedRow.projectId == owningRow.projectId
```

When `AuditRun.targetEntityType = 'project'`, the target row is the `Project` table.
The `Project` table has no `projectId` column because its `id` is the project anchor itself.

The same-project check for this case is therefore:

```text
AuditRun.projectId == targetEntityId
```

The central resolver must handle this case explicitly.
It must not attempt to apply the normal `resolvedRow.projectId` rule to `Project` rows.

---

## Read and Write Enforcement Rule

### Writes
All writes that create or mutate polymorphic references must resolve the reference before commit.

The write must fail if:

- `entityType` is not allowed
- `entityId` does not exist
- `entityId` exists under another project
- the reference shape is illegal for that table

### Reads
Read surfaces that expose these references must not promise more than they can validate.

When filtering by polymorphic targets, the filter behavior must remain explicit and deterministic.
A read surface must not behave as if polymorphic resolution is free-form or fuzzy.

---

## Query Strategy Rule

For read filters that rely on a referenced entity not stored directly on the filtered table, document the filter as join-based or resolver-based.

Do not pretend a table has a direct field when the filter actually depends on traversing a related record.

If a list or filter depends on entity-type-specific joins, that must be explicit in the API family doc for that route.

---

## Transaction Rule

If a mutation both:

- changes a referenced entity state
- and writes a polymorphic record about that entity

then the operation must use one transaction where the invariant requires atomicity.

This is especially important for:

- status transitions + `StatusHistory`
- readiness evaluation + `ReadinessGap`
- governed transitions + `DecisionRecord` where required

---

## Error Posture Rule

Polymorphic reference failures must be deterministic.

Recommended behavior:

- malformed `entityType` -> validation failure
- unknown `entityType` -> validation failure
- non-existent `entityId` in project scope -> not found or semantically invalid according to route contract
- cross-project target -> unavailable or semantically invalid without existence leakage

The route family should keep that posture stable.
Do not let one route leak existence while another hides it.

---

## Hammer Expectations

The hammer suite must verify at minimum:

- illegal `entityType` rejection
- same-project enforcement for all polymorphic tables
- cross-project target rejection without leakage
- invalid `entityId` rejection
- special-case project-target enforcement for `AuditRun`
- transaction alignment where polymorphic writes are coupled to state transitions

---

## Final Rule

Polymorphic references are allowed in Project V only because they are governed.

If implementation treats them as casual string-plus-UUID fields without a shared enforcement strategy, the design is wrong.

If a new polymorphic table or a new allowed entity type is introduced, that is a schema governance event. It must update the vocabulary registry, this enforcement doc, affected schema docs, and hammer expectations together.

---

## Human-In-The-Loop Principle

Polymorphic reference behavior is implementation-shaping authority.

Human review may be required where a proposed change would:

- add new allowed entity types
- widen cross-record linkage depth
- weaken same-project enforcement
- introduce ambiguous read or write behavior
- create a new loophole for cross-project existence leakage

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- polymorphic references are governed, not casual
- entityType strings are not free-form values
- same-project enforcement is required on every polymorphic resolution
- `project` as an `AuditRun` target is a real special case and must be handled explicitly
- routes should call a central resolver rather than reimplementing resolution logic locally
- adding a new polymorphic entity type requires coordinated documentation and hammer updates

If implementation treats `entityType` plus `entityId` as an unchecked convenience field pair, this doctrine is being violated.

---

## Usage

This document should be used:

- when implementing polymorphic reference validation in Project V services
- when writing route handlers that create or mutate polymorphic references
- when reviewing whether a proposed entity type is allowed for a given table
- when writing hammer tests for cross-project rejection and resolver behavior
- when reviewing whether current API family docs preserve non-leakage and deterministic enforcement

---

## Related Docs

- `schema-authority.md`
- `schema-specification.md`
- `controlled-vocabularies.md`
- `schema-governance.md`
- `multi-project-doctrine.md`
- `system-invariants.md`
- `status-transitions.md`
- `mcp-surface.md`
- `../ecosystem/vocabulary.md`
