# Project V API — Research Docs

## Purpose

This document defines the API contract family for Project V research-doc records.

It exists to answer:

```text
How should Project V create, read, update, list, and govern structured research-doc records that preserve planning-relevant analysis, synthesis, and bounded writeups without collapsing them into vague notes, giant external-link blobs, or shadow execution records?
```

This is a Tier 2 Project V API authority document.

---

## Scope

This document governs:

- the `research-docs` route family in Project V
- the role of research-doc records in planning, evaluation, and continuity
- allowed operations for creating, listing, reading, and updating research-doc records
- relationship rules between research docs and other Project V records
- validation and mutability posture for research-doc fields
- how research docs differ from external links, evidence links, and decision records

---

## Out of Scope

This document does not define:

- the full rich-text storage implementation detail
- document editor UI behavior
- external document provider sync behavior
- VEDA evidence or observatory storage
- V Forge execution findings or execution reporting

Those belong in implementation, provider, VEDA, or V Forge docs.

---

## System

- project-v

---

## Core Rule

Research-doc records are structured planning-relevant analysis artifacts.

They exist to preserve synthesis, investigation, rationale-building, and bounded planning support content that matters enough to keep as first-class Project V records.

A research doc is more than a link and less than a decision by itself.
It is where thoughtful analysis lives when that analysis should remain queryable, attributable, and attached to planning context.

Research docs must not become:
- random note piles
- giant copied data dumps
- execution logs
- decision records by another name
- a loophole for storing observatory truth that belongs to VEDA

---

## Record Role

A research-doc record captures a bounded research or analysis artifact relevant to planning.

Typical examples include:
- competitive analysis summary
- architecture option analysis
- bounded investigation into a dependency or risk
- synthesis of sources that inform an initiative or objective
- market or feasibility writeup already promoted into planning context

The record exists because the content matters as a planning artifact, not merely because a file exists somewhere.

---

## Route Family

Base route family:

```text
/api/research-docs
```

Canonical item route:

```text
/api/research-docs/{researchDocId}
```

This family is project-scoped.
All operations must run inside active project scope.

---

## Supported Operations

### List
```text
GET /api/research-docs
```

### Read one
```text
GET /api/research-docs/{researchDocId}
```

### Create
```text
POST /api/research-docs
```

### Update
```text
PATCH /api/research-docs/{researchDocId}
```

No delete route is required in first pass unless governed archival posture is added later.

---

## Record Shape

At minimum, a research-doc record should expose fields shaped like:

- `id`
- `projectId`
- `title`
- `docType`
- `status`
- `summary`
- `content`
- `linkedRecordType`
- `linkedRecordId`
- `sourceMode`
- `externalDocUrl`
- `visibility`
- `createdAt`
- `updatedAt`

Additional normalized or derived fields may exist in implementation, but they must remain subordinate to the meaning here.

---

## Field Meaning

### `title`
Human-readable title of the research document.

### `docType`
The governed classification of the research artifact.

Examples may include:
- `analysis`
- `investigation`
- `comparison`
- `feasibility`
- `risk_review`
- `synthesis`

### `status`
Lifecycle posture for the research doc.

Examples may include:
- `draft`
- `active`
- `superseded`
- `archived`

### `summary`
A bounded summary of what the document contains and why it matters.

### `content`
The canonical Project V body for the research doc when Project V owns the content directly.

### `linkedRecordType` / `linkedRecordId`
Optional governed attachment to a specific Project V record when the research doc primarily belongs to an objective, initiative, work item, dependency, or other supported record family.

### `sourceMode`
Indicates whether the research content is primarily:
- native to Project V
- mirrored in bounded form from an external doc location
- externally referenced while Project V stores only bounded summary/metadata

### `externalDocUrl`
Optional external canonical document reference when relevant.
This does not eliminate the need for a real Project V research-doc record when the artifact matters to Project V continuity.

### `visibility`
Governed visibility posture for operator surfaces and review contexts.

---

## Native vs External-Backed Rule

Research docs may be:
- fully native in Project V
- hybrid, where Project V stores the planning-relevant body plus an external canonical reference
- externally backed with bounded summary retained in Project V

The key rule is this:
Project V must preserve enough research continuity that planning does not depend on a disappearing external file plus tribal memory.

If the research matters, Project V must retain meaningful structured continuity.

---

## List Operation

### Route
```text
GET /api/research-docs
```

### Purpose
List research-doc records in project scope.

### Supported filtering should include
- `docType`
- `status`
- `linkedRecordType`
- `linkedRecordId`
- `visibility`

### Sorting should support
- `createdAt`
- `updatedAt`
- optionally `title`

### Includes
The route may support lightweight linked-record summary includes where useful.

### Rule
List results should help answer:
- what research artifacts exist for this initiative or objective?
- what active investigations exist in this project?
- which research docs are draft vs active vs superseded?

---

## Read-One Operation

### Route
```text
GET /api/research-docs/{researchDocId}
```

### Purpose
Return one research-doc record and its governed planning context.

### Should include
- full research-doc record
- minimal linked-record reference context where applicable

### Must not do
- fetch and inline a large external provider document by default as if Project V owns provider sync state
- collapse the distinction between Project V-owned summary/content and externally referenced material

---

## Create Operation

### Route
```text
POST /api/research-docs
```

### Purpose
Create a new research-doc record.

### Required inputs should include
- `title`
- `docType`
- at least one meaningful content continuity path:
  - `content`, or
  - bounded `summary` plus `externalDocUrl` under valid `sourceMode`

### Optional inputs
- `status`
- `summary`
- `content`
- `linkedRecordType`
- `linkedRecordId`
- `sourceMode`
- `externalDocUrl`
- `visibility`

### Server responsibilities
- validate doc type and status values
- validate linked record attachment if supplied
- reject empty shell docs that preserve no meaningful continuity
- reject unknown fields and forbidden caller-owned fields

### Rule
A research doc must preserve actual planning value.
A title plus vibes is not enough.

---

## Update Operation

### Route
```text
PATCH /api/research-docs/{researchDocId}
```

### Purpose
Update mutable research-doc fields.

### Mutable fields should include
- `title`
- `docType` where reclassification is allowed
- `status`
- `summary`
- `content`
- `sourceMode`
- `externalDocUrl`
- `visibility`
- optional linked-record attachment metadata where policy allows

### Stable identity posture
Implementation should strongly prefer immutability for:
- `projectId`
- `id`

For linked-record attachment, implementation may either:
- allow bounded correction when attachment was wrong, or
- prefer creating a new research doc when the artifact’s primary attachment meaning changes materially

### Rule
PATCH is for bounded refinement of a research artifact, not wholesale identity drift.

---

## Relationship to Other Record Families

### Versus External Links
External-link records are typed references.
Research-doc records are substantive planning artifacts.

Use `external-links` when the value is mainly the governed pointer.
Use `research-docs` when the planning-relevant content itself matters as a Project V artifact.

### Versus Evidence Links
Evidence-link records are tighter traceability links used in readiness/audit/evidence posture.
Research docs may cite evidence, but they are not just evidence attachment records.

### Versus Decision Records
Decision records capture governed decisions.
Research docs capture analysis that may inform those decisions.
A research doc may feed a decision record, but it is not the decision itself.

### Versus VEDA
Research docs may summarize or synthesize VEDA signal that has entered planning through the governed interface.
They must not become a warehouse for raw observatory data.

### Versus V Forge
Research docs are planning-side artifacts.
Execution findings and execution reports belong in V Forge, not here.

---

## Empty-Shell Prohibition

Project V should not allow research-doc records that preserve almost nothing.

Examples that should be rejected or treated as invalid:
- title only, no content, no meaningful summary, no valid external reference
- a bare external URL with no planning-relevant description or continuity
- copied placeholder text that does not describe actual research value

If an artifact matters enough to get a research-doc record, it matters enough to preserve meaningfully.

---

## Validation Rules

### Structural validation → 400
Examples:
- malformed UUID
- missing required fields
- unknown body field
- unknown PATCH field
- malformed external URL

### Semantic validation → 422
Examples:
- invalid `docType`
- invalid `status`
- invalid `sourceMode`
- invalid `visibility`
- linked record type/id pairing invalid
- research doc preserves insufficient continuity under route policy

### Scope failure → 404
Examples:
- research doc absent in project scope
- linked record absent in project scope
- linked record exists elsewhere but is out of scope

### Conflict posture → 409 where explicitly modeled
Examples:
- duplicate-title or duplicate-attachment policy if implementation chooses to model that as conflict

---

## Status Rule

A research doc should have a meaningful status lifecycle.

Recommended first-pass posture:
- `draft` for active authoring
- `active` for research that should be used operationally in planning
- `superseded` when replaced by a newer or better artifact
- `archived` when no longer primary but retained for continuity

This matters because research continuity without lifecycle posture turns into archaeology with no labels.

---

## Content Size and Shape Rule

Project V may store substantive content in research docs, but this family must not become an unbounded dumping ground.

Good uses:
- structured multi-section analysis
- bounded comparison writeup
- risk review synthesis
- feasibility rationale

Bad uses:
- raw provider exports
- giant copied logs
- execution transcripts
- observatory datasets

If the artifact is mostly raw data, it probably belongs elsewhere.

---

## LLM and Operator Use Rule

A capable LLM or operator should be able to use this route family to:
- find the research that informed an initiative or dependency
- understand the current state of an investigation
- distinguish active research from obsolete writeups
- move from research artifacts to linked decision or planning records cleanly

They should not have to guess whether a record is substantive or merely a pointer.

---

## Hammer Expectations

Project V hammer should verify at minimum that:
- empty-shell research docs are rejected
- linked-record validation is enforced
- out-of-scope linkage fails non-leakily
- status transitions remain valid
- route family preserves distinction between research docs and external links
- superseded/archived posture remains queryable and legible

---

## Usage

This document should be used:
- when implementing the `research-docs` route family
- when deciding whether a planning artifact belongs in research docs or another family
- when validating continuity requirements for research artifacts
- when reviewing whether Project V is preserving analysis as meaningful planning state rather than vague notes

---

## Related Docs

- `../api-conventions.md`
- `../endpoint-governance.md`
- `../polymorphic-reference-enforcement.md`
- `../schema-specification.md`
- `../schema-governance.md`
- `decision-records.md`
- `external-links.md`
- `evidence-links.md`
- `../github-integration.md`
