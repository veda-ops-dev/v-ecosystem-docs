# Evidence Links API Family

## Purpose

This document defines the first-pass API contract family for Project V evidence links.

It exists to answer:

```text
What routes exist for evidence links, what do they accept, what do they return, what validations and ownership rules apply, and how do evidence links behave as bounded planning-side references to supporting evidence?
```

Read this with:

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../polymorphic-reference-enforcement.md`
- `../data-boundaries.md`
- `../implementation-traceability.md`
- `../multi-project-doctrine.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the evidence link route family
- request and response shape for first-pass evidence link routes
- evidence link list ordering and filtering posture
- create, read, update behavior
- polymorphic source entity validation
- controlled-vocabulary handling for `evidenceType`
- server-owned vs caller-supplied field posture
- boundary rules distinguishing Project V planning-side references from evidence truth owned by VEDA
- validation, error, and non-leakage posture for evidence link routes

---

## Out of Scope

This document does not define:

- VEDA evidence content, provenance, or source-trust handling (see `../../veda/evidence-and-source-provenance.md`)
- the VEDA to Project V signal interface (see `../../interfaces/veda-to-project-v-signal-interface.md`)
- external link routes (see the external links API family doc)
- research doc routes
- schema migration sequencing
- evidence link UI rendering behavior

---

## System

- project-v

---

## Core Rule

Evidence links are project-scoped planning-side references from a governed Project V record to supporting evidence.

They are owned by Project V as planning truth about what evidence was considered.
They do not own the evidence itself.

Evidence link routes must preserve all of the following:

- explicit project scope
- deterministic ordering
- same-project polymorphic source entity validation
- controlled-vocabulary evidence-type handling
- non-leaky cross-project rejection

Evidence link routes must not act like evidence content storage, VEDA observability mirrors, or general-purpose annotation dumps.

---

## What an Evidence Link Is

An `EvidenceLink` record in Project V is a bounded planning-side reference from a governed Project V planning entity or evaluation record to external supporting evidence.

It records:

- the source entity being supported (polymorphic: type and id)
- the type of evidence being referenced
- the locator pointing to the evidence (external URL, VEDA locator, or other explicit reference)
- an optional explanatory note
- an optional relevance score

An evidence link does not store the evidence content itself.
An evidence link does not make Project V the owner of VEDA observability truth.
An evidence link is Project V's planning-side record of what evidence was considered and where it lives.

---

## Ownership Boundary

Evidence links are directional and non-owning.

The planning entity or evaluation record in Project V is the owner.
The referenced evidence target is owned by the external system, VEDA, or external source it lives in.

Project V preserves the planning-side record of the reference.
Project V does not validate, mirror, or synchronize the evidence content.

If evidence behind a link becomes stale, moved, or inaccessible, that is a planning-side concern governed by `../data-boundaries.md`.
It does not automatically mutate or invalidate the evidence link record itself.
Staleness handling belongs in planning-side gap and audit logic, not in this route family.

---

## Canonical Record Basis

Canonical fields governed by `schema-specification.md`:

- `id`
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `evidenceType`
- `targetLocator`
- `note`
- `relevanceScore`
- `createdAt`
- `updatedAt`

The route family must not introduce shadow fields outside the governed schema.

---

## Route Family

First-pass evidence link routes:

- `POST /evidence-links`
- `GET /evidence-links`
- `GET /evidence-links/{id}`
- `PATCH /evidence-links/{id}`

No status-transition route exists for evidence links.
No delete route exists in the first pass.

---

## Scope Posture

All evidence link routes are project-scoped.

Project scope is resolved from the governed session/auth context.
The route must not trust caller-supplied project scope for authorization.

Where a route accepts `projectId` in the body or query for creation/filtering semantics, that value must still be validated against the governed session scope.
A mismatch must fail without cross-project leakage.

---

## Polymorphic Source Entity Rule

`sourceEntityType` and `sourceEntityId` form a polymorphic reference to the Project V planning entity the evidence link belongs to.

Both must follow `polymorphic-reference-enforcement.md`.

That means:

- allowed source entity types are not free-form; they are governed by the Evidence Link Source Entity Type vocabulary in `controlled-vocabularies.md`
- the referenced source entity must exist
- the referenced source entity must belong to the same project scope as the evidence link
- cross-project source entity references must fail without existence leakage
- the source entity must be resolved before commit

Allowed evidence link source entity types, first pass:

- `objective`
- `initiative`
- `work_item`
- `handoff`
- `decision_record`
- `research_doc`

This route family must not expand the allowed type set locally.

---

## Evidence Type Rule

`evidenceType` is required on creation.

It must use the governed evidence link type vocabulary from `controlled-vocabularies.md`.
Invalid `evidenceType` values must fail with `422 Unprocessable Entity`.

---

## Target Locator Rule

`targetLocator` is required on creation.

It must be non-empty.
An empty `targetLocator` must fail with `422 Unprocessable Entity`.

No format constraint beyond non-empty is enforced in the first pass. `targetLocator` is intentionally not constrained to `https://` URLs because VEDA locators, internal system locators, and other reference formats are valid targets. Implementers must not copy the stricter `https://`-prefix rule from `ExternalLink.url` onto this field.

Project V does not validate whether the referenced locator resolves, whether external content exists at the locator, or whether VEDA holds a record at the referenced address. External existence validation would violate Project V's boundary posture. See `../api-conventions.md` External Reference Validation Rule.

The locator is a planning-side reference. Staleness is the caller's responsibility.

---

## Relevance Score Rule

`relevanceScore` is optional.

When supplied, it must be an integer within the governed range `0..100`.
An out-of-range value must fail with `422 Unprocessable Entity`.
A non-integer must fail with `400 Bad Request`.

---

## `POST /evidence-links`

### Purpose
Create a new evidence link in current project scope.

### Request body

```json
{
  "projectId": "uuid",
  "sourceEntityType": "work_item",
  "sourceEntityId": "uuid",
  "evidenceType": "observation",
  "targetLocator": "veda://observations/abc123",
  "note": "Optional planning-side note about this evidence",
  "relevanceScore": 80
}
```

### Required fields
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `evidenceType`
- `targetLocator`

### Optional fields
- `note`
- `relevanceScore`

### Forbidden fields
The caller must not supply:

- `id`
- `createdAt`
- `updatedAt`

Supplying forbidden fields must fail with `400 Bad Request`.

### Defaults
- `note = null` if omitted
- `relevanceScore = null` if omitted

### Validation
- `projectId` must match current governed project scope
- `sourceEntityType` must be a valid evidence link source entity type
- `sourceEntityId` must be a valid UUID
- source entity must resolve inside current project scope
- `evidenceType` must be a valid evidence link type value
- `targetLocator` must be non-empty
- `relevanceScore`, if supplied, must be an integer in range `0..100`
- `note`, if supplied, must be non-empty text or `null`

### Response shape
Return `201 Created` with canonical record body.

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "sourceEntityType": "work_item",
  "sourceEntityId": "uuid",
  "evidenceType": "observation",
  "targetLocator": "veda://observations/abc123",
  "note": "text or null",
  "relevanceScore": 80,
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

---

## `GET /evidence-links`

### Purpose
List evidence links in current project scope.

### Query parameters
Allowed first-pass query parameters:

- `sourceEntityType`
- `sourceEntityId`
- `evidenceType`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

### Query parameter semantics

#### `sourceEntityType`
- optional
- controlled-vocabulary value from evidence link source entity type set
- invalid value -> `422 Unprocessable Entity`

#### `sourceEntityId`
- optional
- UUID
- malformed UUID -> `400 Bad Request`
- must not be supplied without `sourceEntityType`; supplying without type -> `400 Bad Request`
- if supplied with `sourceEntityType`, filters evidence links whose source matches that exact resolved entity in current project scope
- if the referenced source entity is not found in current project scope — whether it exists elsewhere or not — the route must return an empty result set without revealing whether the entity exists in another project

#### `evidenceType`
- optional
- controlled-vocabulary value from evidence link type set
- invalid value -> `422 Unprocessable Entity`

#### `limit`
- optional
- positive integer
- bounded server-side maximum
- malformed or non-integer -> `400 Bad Request`
- out-of-range but well-formed -> `422 Unprocessable Entity`
- the server-side maximum is governed by shared implementation convention across Project V list families

#### `cursor`
- optional
- opaque continuation token
- malformed cursor -> `400 Bad Request`

### Pairing rule
`sourceEntityId` must not be supplied without `sourceEntityType`.
A missing type for a supplied entity id is a structurally malformed filter and must fail with `400 Bad Request`.

### Ordering
Default and required ordering:

```text
createdAt desc, id asc
```

This ordering is deterministic and must be the basis for cursor generation for this family.

### Response shape

```json
{
  "data": [
    {
      "id": "uuid",
      "projectId": "uuid",
      "sourceEntityType": "controlled-value",
      "sourceEntityId": "uuid",
      "evidenceType": "controlled-value",
      "targetLocator": "text",
      "note": "text or null",
      "relevanceScore": "integer or null",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- list responses return canonical evidence link fields only
- all filters apply within current project scope only
- a valid filter value that matches no evidence links in current scope returns an empty data array
- filters must not leak whether referenced source entities exist in another project

---

## `GET /evidence-links/{id}`

### Purpose
Fetch one evidence link by identifier inside current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Behavior
- if evidence link exists in current project scope -> return canonical record
- if evidence link does not exist in current scope -> `404 Not Found`
- if evidence link exists in another project -> route must preserve non-leakage posture and return `404 Not Found`

### Response shape

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "sourceEntityType": "controlled-value",
  "sourceEntityId": "uuid",
  "evidenceType": "controlled-value",
  "targetLocator": "text",
  "note": "text or null",
  "relevanceScore": "integer or null",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

---

## `PATCH /evidence-links/{id}`

### Purpose
Apply bounded field updates to an evidence link.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Allowed fields
- `note`
- `relevanceScore`

### Forbidden fields
The caller must not patch:

- `id`
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `evidenceType`
- `targetLocator`
- `createdAt`
- `updatedAt`

Unknown PATCH fields must fail with `400 Bad Request`.
Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- evidence link must exist in current project scope or return `404 Not Found`
- `note`, if supplied, may be `null` or non-empty text; supplying an empty string must fail with `422 Unprocessable Entity`
- `relevanceScore`, if supplied, may be `null` or an integer in range `0..100`; out-of-range value must fail with `422 Unprocessable Entity`; non-integer must fail with `400 Bad Request`

### Response shape
Return canonical evidence link record after patch.

### Notes
`sourceEntityType`, `sourceEntityId`, `evidenceType`, and `targetLocator` are immutable after creation.
They are the identity and directional posture of the link.
If the intent changes enough to warrant different identity fields, a new evidence link should be created.

Setting `note` to `null` explicitly clears the note.
Setting `relevanceScore` to `null` explicitly removes the score.

---

## Identity and Immutability Posture

The identity of an evidence link is defined by:

```text
(projectId, sourceEntityType, sourceEntityId, evidenceType, targetLocator)
```

These fields are immutable after creation.

Only `note` and `relevanceScore` may be updated after creation.

This posture keeps evidence links as stable planning-side references rather than mutable annotation records.
If the evidence being referenced changes materially, a new evidence link should be created to capture the updated reference.

Creating a new evidence link does not automatically supersede, invalidate, or remove any prior evidence link. There is no status field, delete route, or supersedence mechanism for evidence links in the first pass. Prior links remain as historical planning record. An operator who intends to replace a reference with a different one must be aware that both links will coexist unless a future governed mechanism is introduced.

---

## Validation and Error Posture

### `400 Bad Request`
Use for:

- malformed UUIDs
- malformed cursor
- unknown query parameters
- unknown PATCH fields
- forbidden caller-supplied fields
- wrong types (including non-integer `relevanceScore`)
- missing required fields
- `sourceEntityId` supplied without `sourceEntityType`

### `422 Unprocessable Entity`
Use for:

- invalid controlled-vocabulary values for `sourceEntityType`, `evidenceType`
- empty `targetLocator`
- empty string supplied as `note`
- out-of-range `relevanceScore`
- cross-project polymorphic source entity rejection without existence leakage
- invalid polymorphic entity reference shape when the request is otherwise well-formed

### `404 Not Found`
Use for:

- evidence link not found in current project scope
- evidence link existing in another project but outside current scope

---

## Non-Leakage Rule

Evidence link routes must not leak whether an evidence link or a referenced source entity exists in another project.

A caller attempting to fetch or patch an evidence link outside current project scope must receive the same `404 Not Found` posture as for a genuinely absent evidence link.

Source entity list filters must return empty results rather than revealing whether a referenced entity exists elsewhere.

Error body shape must not reveal whether the target exists elsewhere.

---

## Invariants

1. `sourceEntityType` and `sourceEntityId` are immutable after creation.
2. `evidenceType` is immutable after creation.
3. `targetLocator` is immutable after creation.
4. Only `note` and `relevanceScore` may be mutated after creation, through the bounded PATCH route.
5. A caller-supplied `id`, `createdAt`, or `updatedAt` must always fail with `400 Bad Request`.
6. `relevanceScore`, when present, must always be in range `0..100`.
7. `targetLocator` must always be non-empty on any persisted record.
8. Source entity must resolve inside current project scope at creation time.
9. An evidence link existing in another project must return `404 Not Found`, not a cross-project disclosure.
10. Creating a new evidence link does not supersede or invalidate prior links for the same source entity.

---

## Hammer Expectations

The hammer suite for evidence links should verify at minimum:

- evidence link creation with valid input for each supported source entity type
- omitted `note` defaults to `null` on creation
- omitted `relevanceScore` defaults to `null` on creation
- malformed UUID rejection with `400`
- unknown query parameter rejection with `400`
- unknown PATCH field rejection with `400`
- forbidden field rejection on create and patch
- `sourceEntityId` without `sourceEntityType` rejection with `400`
- invalid `evidenceType` rejection with `422`
- empty `targetLocator` rejection with `422`
- out-of-range `relevanceScore` rejection with `422`
- non-integer `relevanceScore` rejection with `400`
- empty `note` string rejection with `422`
- `note` cleared to `null` through PATCH
- `relevanceScore` cleared to `null` through PATCH
- same-project source entity validation on create
- cross-project source entity reference rejection without leakage
- source entity filter non-leakage in list behavior
- deterministic list ordering
- cursor continuation correctness
- identity field immutability: `sourceEntityType`, `sourceEntityId`, `evidenceType`, `targetLocator` not patchable
- cross-project fetch/patch non-leakage

---

## Final Rule

Evidence links are bounded planning-side references.

Their API family must stay simple, explicit, and ownership-honest.
They point toward evidence. They do not own it.

If evidence link routes become content stores, VEDA mirrors, or free-form annotation surfaces, the family has drifted from its role.

---

## Human-In-The-Loop Principle

Evidence link configuration is governance-sensitive because evidence links support readiness, audit, and handoff rationale.

Operators and bounded LLMs must be able to trust that:

- list behavior is deterministic
- source entity references are same-project validated
- evidence type classification is controlled and explicit
- target locators are present and stable once created
- creating a new link does not silently retire an older one
- cross-project visibility is not accidentally leaked

The API family must preserve that trust structurally.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- evidence links are project-scoped planning-side references, not content stores
- `sourceEntityType`, `sourceEntityId`, `evidenceType`, and `targetLocator` are immutable after creation
- only `note` and `relevanceScore` may be updated through PATCH
- `note` and `relevanceScore` default to `null` on creation if omitted
- `targetLocator` has no format constraint beyond non-empty in the first pass; it is not restricted to `https://` URLs
- Project V does not validate whether the `targetLocator` resolves or whether the evidence exists
- evidence ownership belongs to VEDA or the external source, not to Project V
- creating a new link does not supersede or invalidate prior links for the same source entity
- `sourceEntityId` filtering requires paired `sourceEntityType` and must not leak cross-project entity existence

If implementation allows identity field mutation, validates external evidence content, applies an `https://`-only constraint to `targetLocator`, or treats evidence links as a general annotation system, the contract is being violated.

---

## Usage

This document should be used:

- when implementing evidence link routes
- when writing migrations or tests that depend on evidence link API behavior
- when writing hammer coverage for evidence link routes
- when reviewing whether evidence link behavior remains bounded planning-side reference posture
- when checking whether evidence link mutation paths exceed `note` and `relevanceScore`

---

## Related Docs

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../polymorphic-reference-enforcement.md`
- `../data-boundaries.md`
- `../implementation-traceability.md`
- `../multi-project-doctrine.md`
- `../system-invariants.md`
- `../mcp-surface.md`
- `../schema-governance.md`
- `../../veda/evidence-and-source-provenance.md`
- `../../interfaces/veda-to-project-v-signal-interface.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../ecosystem/vocabulary.md`
