# Project V API — Decision Records

## Purpose

This document defines the API contract family for Project V decision-record records.

It exists to answer:

```text
How should Project V create, read, update, list, and govern structured decision-records that preserve planning decisions, their status, rationale, alternatives, and linked evidence without turning decision continuity into scattered prose, hidden chat memory, or mutable historical fog?
```

This is a Tier 2 Project V API authority document.

---

## Scope

This document governs:

- the `decision-records` route family in Project V
- the role of decision-records in planning continuity and governance
- allowed operations for creating, listing, reading, and updating decision records
- linkage between decisions and other Project V records
- lifecycle posture for active, superseded, or withdrawn decisions
- validation and mutation rules for decision-record fields

---

## Out of Scope

This document does not define:

- the full schema detail for decision-record storage
- ADR markdown file conventions outside Project V API posture
- approval workflow implementation details
- chat UI behavior for decision drafting
- V Forge execution findings or VEDA evidence storage

Those belong in schema, governance, or companion docs.

---

## System

- project-v

---

## Core Rule

Decision records are governed planning decisions with continuity value.

They exist to preserve what was decided, why it was decided, what alternatives were considered, and how later operators or LLMs should understand the decision’s current standing.

A decision record must make it possible to answer:
- what was decided?
- why?
- what did it apply to?
- what alternatives were considered?
- is it still active, superseded, or withdrawn?

Decision records must not become:
- vague note fragments
- unstructured chat residue
- endlessly mutable history that erases what was actually decided
- execution findings disguised as planning decisions

---

## Record Role

A decision-record captures a governed decision artifact inside Project V.

Typical examples include:
- decision to adopt a schema direction
- decision to split or combine work streams
- decision to accept or reject a dependency path
- decision to revise planning assumptions after review
- decision to supersede an earlier planning direction

The decision record is the continuity artifact for the decision itself, not just a pointer to where someone once discussed it.

---

## Route Family

Base route family:

```text
/api/decision-records
```

Canonical item route:

```text
/api/decision-records/{decisionRecordId}
```

This family is project-scoped.
All operations must run inside active project scope.

---

## Supported Operations

### List
```text
GET /api/decision-records
```

### Read one
```text
GET /api/decision-records/{decisionRecordId}
```

### Create
```text
POST /api/decision-records
```

### Update
```text
PATCH /api/decision-records/{decisionRecordId}
```

No delete route is required in first pass.
Decision continuity should strongly prefer status/lifecycle change over hard deletion.

---

## Record Shape

At minimum, a decision-record should expose fields shaped like:

- `id`
- `projectId`
- `title`
- `decisionType`
- `status`
- `summary`
- `decisionText`
- `rationale`
- `alternativesConsidered`
- `linkedRecordType`
- `linkedRecordId`
- `effectiveAt`
- `supersedesDecisionRecordId`
- `visibility`
- `createdAt`
- `updatedAt`

Additional normalized or derived fields may exist in implementation, but they must remain subordinate to the governed meaning here.

---

## Field Meaning

### `title`
Short human-readable title of the decision.

### `decisionType`
Governed classification of the decision.

Examples may include:
- `architecture`
- `schema`
- `planning`
- `dependency`
- `workflow`
- `governance`

### `status`
Current lifecycle posture of the decision record.

Examples may include:
- `proposed`
- `accepted`
- `superseded`
- `withdrawn`

### `summary`
Bounded summary of the decision.

### `decisionText`
The actual statement of what was decided.

### `rationale`
Why the decision was taken.

### `alternativesConsidered`
Bounded structured or textual description of meaningful alternatives.

### `linkedRecordType` / `linkedRecordId`
Optional governed attachment to a specific Project V record when the decision primarily belongs to an objective, initiative, work item, dependency, or other supported record family.

### `effectiveAt`
The date/time the decision became effective when meaningful.

### `supersedesDecisionRecordId`
Optional reference to an earlier decision record this one supersedes.

### `visibility`
Governed visibility posture for operator and review surfaces.

---

## Immutability and Historical Honesty Rule

Decision records carry historical continuity.
That means they must not be treated like endlessly editable living notes.

Recommended posture:
- bounded correction of obvious errors is allowed
- status can change over time
- supersession can be recorded
- the basic continuity of what was decided should not be casually rewritten into something else later

If a materially new decision exists, it should usually create a new decision record rather than rewriting the old one into a new reality.

---

## List Operation

### Route
```text
GET /api/decision-records
```

### Purpose
List decision records in active project scope.

### Supported filtering should include
- `decisionType`
- `status`
- `linkedRecordType`
- `linkedRecordId`
- `visibility`
- `supersedesDecisionRecordId`

### Sorting should support
- `createdAt`
- `updatedAt`
- `effectiveAt`

### Includes
The route may support lightweight linked-record summary includes and lightweight supersession context.

### Rule
List results should help answer:
- what decisions exist for this initiative or dependency?
- which decisions are currently accepted?
- which decisions were superseded or withdrawn?

---

## Read-One Operation

### Route
```text
GET /api/decision-records/{decisionRecordId}
```

### Purpose
Return one governed decision record.

### Should include
- full decision-record fields
- minimal linked-record context where applicable
- lightweight supersession context where applicable

### Must not do
- collapse current status and historical origin into one blurred state
- hide whether the record was superseded or withdrawn

A decision record is only useful if its current standing is legible.

---

## Create Operation

### Route
```text
POST /api/decision-records
```

### Purpose
Create a new decision record.

### Required inputs should include
- `title`
- `decisionType`
- `status`
- `decisionText`
- enough bounded rationale continuity to explain the decision meaningfully

### Optional inputs
- `summary`
- `rationale`
- `alternativesConsidered`
- `linkedRecordType`
- `linkedRecordId`
- `effectiveAt`
- `supersedesDecisionRecordId`
- `visibility`

### Server responsibilities
- validate decision type and status values
- validate linked record attachment if supplied
- validate superseded decision reference if supplied
- reject empty-shell decisions that preserve no actual decision continuity
- reject unknown fields and forbidden caller-owned fields

### Rule
A decision record must preserve a real decision.
A title plus one sentence of fog is not enough.

---

## Update Operation

### Route
```text
PATCH /api/decision-records/{decisionRecordId}
```

### Purpose
Apply bounded corrections or lifecycle updates to an existing decision record.

### Mutable fields should include only bounded items such as
- `status`
- `summary`
- `rationale`
- `alternativesConsidered`
- `effectiveAt`
- `supersedesDecisionRecordId`
- `visibility`
- narrowly scoped correction of `decisionText` if policy permits and historical honesty is preserved

### Strongly stable fields should include
- `projectId`
- `id`
- original core identity of the decision record

### Rule
PATCH must not turn one decision into a fundamentally different decision artifact.
When meaning changes materially, create a new decision record and use supersession.

---

## Supersession Rule

Decision records should support explicit supersession.

That means:
- a later decision may supersede an earlier one
- the earlier record should remain readable
- the later record should point back to the earlier one when that relationship matters
- the earlier record’s status should be compatible with being superseded

This preserves continuity instead of forcing operators to infer history from scattered edits.

---

## Relationship to Other Record Families

### Versus Research Docs
Research docs preserve analysis.
Decision records preserve the actual decision.
A research doc may inform a decision record, but it is not the same thing.

### Versus Evidence Links
Evidence links attach supporting evidence to planning/review artifacts.
A decision record may use evidence links, but the decision record is the continuity artifact for the decision itself.

### Versus External Links
External links are governed references to outside resources.
Decision records are first-class Project V continuity records.

### Versus V Forge
Execution findings and return-to-planning artifacts may influence decisions, but execution truth belongs in V Forge. Decision records belong in Project V.

---

## Empty-Shell Prohibition

Project V should reject decision records that do not preserve meaningful decision continuity.

Examples that should be rejected or treated as invalid:
- title only
- status with no real decision text
- vague placeholder such as “to be decided later” used as though it were a decision record
- supersession reference with no actual new decision continuity

If there is no actual decision yet, use an appropriate planning artifact instead of pretending one exists.

---

## Validation Rules

### Structural validation → 400
Examples:
- malformed UUID
- missing required fields
- unknown body field
- unknown PATCH field

### Semantic validation → 422
Examples:
- invalid `decisionType`
- invalid `status`
- invalid `visibility`
- linked record type/id pairing invalid
- invalid supersession relationship
- decision record preserves insufficient continuity under route policy

### Scope failure → 404
Examples:
- decision record absent in project scope
- linked record absent in project scope
- superseded decision reference absent in project scope
- referenced record exists elsewhere but is out of scope

### Conflict posture → 409 where explicitly modeled
Examples:
- illegal self-supersession
- duplicate record policy if implementation models strong uniqueness for certain decision classes

---

## Status Rule

A decision record should have a meaningful lifecycle posture.

Recommended first-pass meanings:
- `proposed` — under active consideration but not accepted yet
- `accepted` — adopted and current
- `superseded` — replaced by a later decision
- `withdrawn` — intentionally no longer in force without direct replacement

The route family must preserve those distinctions honestly.

---

## LLM and Operator Use Rule

A capable LLM or operator should be able to use this route family to:
- determine what planning decisions currently govern a work area
- distinguish accepted decisions from obsolete ones
- trace from a decision to its linked planning context
- understand whether later decisions replaced earlier ones

They should not need to infer all of this from prose archaeology.

---

## Hammer Expectations

Project V hammer should verify at minimum that:
- empty-shell decision records are rejected
- linked-record validation is enforced
- supersession relationships are valid and non-leaky
- materially historical continuity is not casually erased through PATCH
- list/filter behavior for active vs superseded vs withdrawn works correctly
- read-one exposes status and supersession posture clearly

---

## Usage

This document should be used:
- when implementing the `decision-records` route family
- when deciding whether an artifact is a research doc, decision record, or another planning record
- when reviewing whether Project V is preserving decision continuity honestly over time
- when validating supersession and lifecycle posture for planning decisions

---

## Related Docs

- `../api-conventions.md`
- `../endpoint-governance.md`
- `../polymorphic-reference-enforcement.md`
- `../schema-specification.md`
- `../schema-governance.md`
- `../implementation-traceability.md`
- `research-docs.md`
- `external-links.md`
- `evidence-links.md`
