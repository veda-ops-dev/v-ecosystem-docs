# Project V API — External Links

## Purpose

This document defines the API contract family for Project V external-link records.

It exists to answer:

```text
How should Project V create, read, update, list, and govern external-link records that connect planning and execution work to GitHub items, docs, research sources, release URLs, tickets, and other governed references without letting link records turn into a duplicate document store or vague URL junk drawer?
```

This is a Tier 2 Project V API authority document.

---

## Scope

This document governs:

- the `external-links` route family in Project V
- the role of external-link records in Project V planning and traceability
- allowed operations for creating, listing, reading, and updating external-link records
- validation and mutation posture for external-link fields
- linkage between external links and other Project V records
- visibility and governance rules for link records

---

## Out of Scope

This document does not define:

- the full database schema for external-link records
- the full polymorphic reference implementation detail
- the GitHub API or provider integration internals
- V Forge execution-side publication continuity or release records
- the full research-doc storage model

Those belong in schema, provider, V Forge, or companion API docs.

---

## System

- project-v

---

## Core Rule

External-link records are governed references, not content containers.

They exist to preserve durable, queryable linkage between Project V planning records and relevant external or cross-system resources.

An external-link record should help an operator or LLM answer questions like:
- what GitHub PR is associated with this work item?
- what doc or source supports this decision?
- what release or public URL should be considered alongside this initiative?
- what issue or ticket is connected to this objective or dependency?

External-link records must not become:
- a dumping ground for random URLs
- a shadow document store
- a replacement for research-doc records
- a substitute for execution continuity owned by V Forge

---

## Record Role

An external-link record represents a governed reference from a Project V record to a URL or provider-backed external resource.

Typical examples include:
- GitHub PR URL
- GitHub issue URL
- GitHub release URL
- external design doc URL
- support ticket URL
- specification or standards page URL
- bounded supporting evidence URL

The record exists because the relationship matters to planning, auditability, readiness, dependency review, or implementation traceability.

The value is not the raw URL alone.
The value is the governed, typed relationship.

---

## Route Family

Base route family:

```text
/api/external-links
```

Canonical item route:

```text
/api/external-links/{externalLinkId}
```

This family is project-scoped.
All operations must run inside active project scope.

---

## Supported Operations

### List
```text
GET /api/external-links
```

### Read one
```text
GET /api/external-links/{externalLinkId}
```

### Create
```text
POST /api/external-links
```

### Update
```text
PATCH /api/external-links/{externalLinkId}
```

No delete route is required in first pass unless governance explicitly admits soft-delete/archive posture later.

---

## Record Shape

At minimum, an external-link record should expose fields shaped like:

- `id`
- `projectId`
- `linkedRecordType`
- `linkedRecordId`
- `linkType`
- `url`
- `provider`
- `title`
- `notes`
- `visibility`
- `createdAt`
- `updatedAt`

Additional normalized or derived fields may exist in implementation, but they must remain subordinate to the governed meaning here.

---

## Field Meaning

### `linkedRecordType`
The Project V record family this link belongs to.

Examples may include:
- `objective`
- `initiative`
- `work_item`
- `dependency`
- `handoff`
- `readiness_evaluation`
- `audit_record`
- `decision_record`

This field must use governed controlled vocabularies.

### `linkedRecordId`
The ID of the Project V record the link belongs to.

### `linkType`
The semantic role of the link.

Examples may include:
- `github_pr`
- `github_issue`
- `github_release`
- `doc`
- `ticket`
- `spec`
- `evidence`
- `reference`

This field must use governed controlled vocabularies.

### `url`
The canonical external URL or resource location.

### `provider`
A bounded classification for the external system or provider.

Examples may include:
- `github`
- `google_docs`
- `notion`
- `jira`
- `linear`
- `other`

### `title`
A short operator-visible label for the linked resource.

### `notes`
Optional bounded notes explaining why the link matters.
Not a place to duplicate the linked document.

### `visibility`
A governed label indicating whether the link is broadly visible in Project V surfaces or more restricted to certain review contexts.

---

## List Operation

### Route
```text
GET /api/external-links
```

### Purpose
List external-link records in active project scope.

### Supported filtering should include
- `linkedRecordType`
- `linkedRecordId`
- `linkType`
- `provider`
- `visibility`

### Sorting should support
- `createdAt`
- `updatedAt`

### Includes
The list route may support lightweight include posture for the linked Project V record summary where that is useful and non-redundant.

### Rule
List responses should make it easy to answer:
- what external links are attached to this record?
- what GitHub or doc references exist for this initiative or work item?
- which links of a certain class exist across the project?

---

## Read-One Operation

### Route
```text
GET /api/external-links/{externalLinkId}
```

### Purpose
Return the governed reference record for one external link.

### Should include
- the full external-link record
- minimal linked-record reference context where useful

### Must not do
- fetch and inline the full linked external document as if Project V owns it
- turn read-one into a provider sync operation by default

The record is the governed linkage, not a mirror of the resource.

---

## Create Operation

### Route
```text
POST /api/external-links
```

### Purpose
Create a new governed external-link record attached to a Project V record.

### Required inputs
- `linkedRecordType`
- `linkedRecordId`
- `linkType`
- `url`

### Optional inputs
- `provider`
- `title`
- `notes`
- `visibility`

### Server responsibilities
- verify linked record exists in active project scope
- verify link type is valid
- verify URL is structurally valid
- normalize provider classification where supported
- reject unknown fields and forbidden caller-owned fields

### Rule
Creation should be explicit and typed.
A raw URL with no meaningful linkage semantics is not enough.

---

## Update Operation

### Route
```text
PATCH /api/external-links/{externalLinkId}
```

### Purpose
Update mutable metadata on an existing external-link record.

### Mutable fields should include only bounded metadata such as
- `linkType` if reclassification is legitimately allowed
- `url`
- `provider`
- `title`
- `notes`
- `visibility`

### Immutable or effectively stable posture
Implementation should strongly prefer immutability for:
- `projectId`
- `linkedRecordType`
- `linkedRecordId`

If relinking is ever needed, create a new external-link record rather than mutating the record’s core attachment identity casually.

### Rule
PATCH is for bounded correction or metadata refinement, not identity drift.

---

## Relationship to Polymorphic References

External-link records are one of the clearest Project V uses of governed polymorphic references.

The linked Project V record may vary across families, but the relationship must remain explicit and validated.

This route family must respect the polymorphic reference doctrine from:
- `project-v/polymorphic-reference-enforcement.md`

That means:
- `linkedRecordType` and `linkedRecordId` must be validated together
- impossible pairings must fail
- out-of-scope pairings must fail non-leakily

---

## Visibility Rule

Not every external link has the same operator visibility posture.

Examples:
- a public GitHub release link may be broadly visible
- an internal design doc or ticket link may be more restricted
- an evidence/supporting-reference link may be visible in review contexts but not primary work dashboards

The API must preserve the visibility label honestly.
It must not silently flatten all links into one universal visibility class.

---

## Single-Table Rationale

Project V should prefer one governed `external-links` family rather than many tiny link tables by provider.

That is the right first-pass posture because:
- the core value is the typed relationship, not provider-specific fragmentation
- most operations want to query “links attached to this record” regardless of provider
- provider-specific nuances can be expressed through `provider`, `linkType`, and bounded metadata
- this keeps implementation and operator reasoning simpler without losing governance

If a provider later needs deeper modeled behavior, that should be governed explicitly rather than smuggled in through table sprawl.

---

## Validation Rules

### Structural validation → 400
Examples:
- malformed UUID
- missing required field
- invalid URL format
- unknown body field
- unknown PATCH field

### Semantic validation → 422
Examples:
- invalid `linkedRecordType`
- invalid `linkType`
- invalid `provider`
- visibility value outside allowed vocabulary
- valid-looking URL but unsupported by route policy if such policy is enforced

### Scope failure → 404
Examples:
- linked record absent in project scope
- external-link record absent in project scope
- linked record exists elsewhere but is out of scope

### Conflict posture → 409 where explicitly modeled
Examples:
- duplicate link policy violation if implementation forbids repeated identical link attachments for the same record and type

The family must remain consistent with Project V API conventions.

---

## Duplicate Handling Rule

Implementation should define a clear duplicate posture.

Recommended first-pass default:
- allow multiple links to the same provider when they serve genuinely different semantic roles
- reject exact duplicate attachments when `linkedRecordType`, `linkedRecordId`, `linkType`, and canonicalized `url` are all the same

That keeps the family from degenerating into link spam while preserving legitimate multiple references.

---

## Notes Field Rule

`notes` is optional bounded rationale.
It must not become a shadow document body.

Good uses:
- “Primary PR for milestone delivery”
- “Spec page used for compliance review”
- “Public release URL referenced in launch readiness”

Bad uses:
- full copied design doc
- freeform research dump
- large implementation narrative that belongs in a research doc or decision record

---

## LLM and Operator Use Rule

A capable LLM or operator should be able to use this route family to:
- locate all GitHub artifacts tied to a work item
- trace supporting docs tied to readiness or audit work
- connect a decision record to the evidence or spec links that informed it
- inspect implementation or release references tied to an initiative

They should not need to guess whether a link is important or what it is for.
The route family should make the relationship legible.

---

## Non-Goals

This route family is not for:
- storing whole documents
- mirroring provider state continuously
- replacing research-doc records
- replacing V Forge release/publication continuity
- replacing evidence-link semantics where those are more tightly governed and purpose-specific

Where a more specific record family exists, use it.

---

## Hammer Expectations

Project V hammer should verify at minimum that:
- invalid linked-record type/id pairings fail
- out-of-scope linked records fail non-leakily
- exact duplicate policy is enforced consistently if modeled
- immutable identity fields are not casually mutable
- list filtering by linked record and link type works
- visibility posture survives create/read/update flows

---

## Usage

This document should be used:
- when implementing the `external-links` route family
- when validating polymorphic link attachments
- when deciding whether a provider URL belongs in `external-links` or another family
- when reviewing whether link records are staying governed and typed rather than becoming URL clutter

---

## Related Docs

- `../api-conventions.md`
- `../endpoint-governance.md`
- `../polymorphic-reference-enforcement.md`
- `../schema-specification.md`
- `../schema-governance.md`
- `../github-integration.md`
- `evidence-links.md`
- `research-docs.md`
- `decision-records.md`
