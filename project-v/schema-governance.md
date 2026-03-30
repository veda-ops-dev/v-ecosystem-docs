# Schema Governance

## Purpose

This document defines the rules for Project V schema design and schema change.

It exists to answer:

```text
How do we keep the Project V database strict, multi-project-safe, and protected from schema drift during development?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the primary rule for schema additions and changes
- schema design principles
- the schema change gate (what must be in place before any change is allowed)
- required questions for every proposed schema change
- anti-drift rules
- the schema freeze posture
- index and constraint posture
- JSON discipline

---

## Out of Scope

This document does not define:

- exact column types or table shapes (see `schema-authority.md`)
- controlled vocabulary values (see `controlled-vocabularies.md`)
- status transition rules (see `status-transitions.md`)
- API contract design

---

## System

- project-v

---

## Core Rule

Project V must not grow its schema casually during implementation.

The schema is governed architecture. It is not a scratchpad for whatever field feels convenient during the current coding session.

Once the initial schema direction is approved, further schema changes must be rare, justified, documented, reviewed, and hammered.

---

## Primary Rule

No schema addition is allowed merely because it makes the next feature easier.

A schema change must justify:

- why the data belongs in Project V
- why the shape is canonical rather than derived
- why existing tables and fields are insufficient
- how the change preserves multi-project integrity
- what query pattern or invariant requires it

If that justification is weak, the change must not happen.

---

## Schema Design Principles

### 1. Model canonical truth explicitly

If Project V owns a concept canonically, model it clearly.

Prefer explicit tables, explicit columns, explicit relations, and explicit status fields.

Avoid using JSON as a lazy substitute for real modeling.

### 2. Keep the model small on purpose

A smaller explicit schema is better than a sprawling speculative schema.

Do not add tables or columns for imagined future possibilities unless the need is clear and durable.

### 3. Multi-project scope must be visible in the schema

Every project-scoped table must make project ownership obvious and enforceable.

Project scope must not be implied only at the application layer.

### 4. Uniqueness must match real scope

Uniqueness constraints must reflect actual ownership scope.

If a value is unique only within a project, the uniqueness rule must include project scope.

Global uniqueness must be rare and intentional.

### 5. State must be inspectable

Important orchestration state must not hide in vague text blobs or unstructured metadata.

### 6. Derived convenience data must stay secondary

If something can be deterministically re-derived from canonical truth, be careful about storing it as first-class state.

Stored derivations create drift risk.

---

## Key Format Rule

Project V keys must use the governed format defined in `controlled-vocabularies.md`.

This rule applies to: `Project.key`, `Objective.key`, `Initiative.key`, `WorkItem.key`.

---

## `updatedAt` Maintenance Rule

Where a first-pass canonical table has an `updatedAt` column, Project V must maintain that column through the application/service mutation path in the same transaction as the governed write.

The first-pass posture does not depend on database triggers for `updatedAt`. This keeps mutation behavior explicit and easier to reason about during early implementation and hammering.

---

## Schema Change Gate

A schema change is only allowed when all of the following exist:

1. **Clear bounded ownership** — the new data belongs in Project V and not in VEDA or V Forge
2. **Written justification** — explains why existing tables and fields are insufficient
3. **Updated authority docs** — `schema-authority.md` and any other affected docs updated first
4. **Migration plan** — the change has a concrete migration path
5. **Hammer coverage** — hammer tests exist or are updated for the affected invariants
6. **Query and index impact considered** — access patterns and index needs are explicit
7. **Multi-project contamination risk reviewed** — the change cannot create cross-project leakage

If any one of these is missing, the change is not ready.

---

## Required Questions for Every Schema Change

Before adding or changing schema, answer these questions explicitly.

### Ownership

- Does this truth belong in Project V?
- Is it planning truth or orchestration truth rather than observatory or execution truth?

### Canonical status

- Is this canonical state or derived convenience state?
- If derived, why should it be stored?

### Scope

- Is this project-scoped, global, or system metadata?
- How is that scope enforced?

### Cardinality and integrity

- What relations does it create?
- What illegal cross-project connections must be prevented?
- What orphan risks exist?

### Query shape

- What real query pattern needs this shape?
- What indexes are needed?
- What ordering rules depend on it?

### Mutation behavior

- What writes create or update this record?
- What transaction boundaries are required?
- What rollback behavior matters?

If the answers are vague, the schema change is not ready.

---

## Anti-Drift Rules

### 1. No ad hoc field additions during route implementation

Do not add columns just because a route or screen would be easier to finish that way.

Implementation must conform to the governed model. The model must not be bent around implementation convenience.

### 2. No JSON escape hatches for unresolved modeling

A JSON field may exist where evidence, import payloads, or flexible metadata are genuinely appropriate.

It must not become a hiding place for unfinished schema thinking.

### 3. No duplicate concepts under different names

Do not create overlapping tables or fields that model the same thing slightly differently.

### 4. No premature convenience tables

Do not add cached or denormalized tables unless there is a proven reason.

### 5. No silent broadening of scope

A project-scoped concept must not quietly drift toward global behavior without explicit review and documentation.

---

## Schema Freeze Posture

Project V must adopt a practical schema freeze posture after the initial domain model is approved.

That means:

- the core table set is chosen intentionally
- endpoint design conforms to that model
- later additions are exceptional, not routine
- schema evolution is governed, not casual

This does not mean the schema can never change. It means schema change becomes a controlled architectural event instead of a habit.

---

## Canonical First-Pass Table Set

The first-pass Project V schema includes these fifteen canonical record families, as defined in `schema-authority.md`:

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

This set must be stressed and hammered before major expansion.

---

## Index and Constraint Posture

The schema must be designed for real multi-project access patterns.

That implies:

- indexes on `projectId` where appropriate
- composite uniqueness where scope requires it
- explicit foreign keys where integrity matters
- ordering support for common list surfaces
- rejection of orphaned records and illegal cross-project relations

The database must help enforce structure. The application must not carry that burden alone.

---

## Required Companion Updates

When an approved schema change occurs, update these docs as needed:

- `schema-authority.md`
- `controlled-vocabularies.md` if affected vocabulary changes
- `status-transitions.md` if affected transitions change
- `system-invariants.md` if affected invariants change
- `multi-project-doctrine.md` if affected multi-project rules change
- hammer planning docs

If the docs are not updated, the system truth is drifting.

---

## Final Rule

Treat the Project V schema as a governed contract.

If a change would make the schema broader without stronger justification, more ambiguous, less multi-project-safe, harder to test, or easier to drift, the change is wrong.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- schema changes require justification, not just implementation convenience
- the change gate has seven explicit conditions, all of which must be satisfied
- anti-drift rules are not optional — they are enforcement constraints
- the fifteen-table first-pass set is a governed base, not a starting suggestion

---

## Usage

This document should be used:

- when proposing a new table, column, or relation for Project V
- when reviewing whether a migration is ready to proceed
- when evaluating whether a schema shortcut is acceptable
- when updating hammer coverage after a schema change

---

## Related Docs

- `schema-authority.md`
- `controlled-vocabularies.md`
- `status-transitions.md`
- `system-invariants.md`
- `multi-project-doctrine.md`
- `data-boundaries.md`
- `hammer-doctrine.md`
