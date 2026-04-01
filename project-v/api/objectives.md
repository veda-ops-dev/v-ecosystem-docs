# Objectives API Family

## Purpose

This document defines the first-pass API contract family for Project V objectives.

It exists to answer:

```text
What routes exist for objectives, what do they accept, what do they return, what validations and lifecycle rules apply, and how do objectives behave as governed project-scoped planning records?
```

Read this with:

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../status-transitions.md`
- `../polymorphic-reference-enforcement.md`
- `../multi-project-doctrine.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the objective route family
- request and response shape for first-pass objective routes
- objective list ordering and filtering posture
- create, read, update, and status-transition behavior
- validation, error, and non-leakage posture for objective routes
- transaction behavior where status history is required

---

## Out of Scope

This document does not define:

- initiative or work-item routes
- generic API conventions shared by all route families
- schema migration sequencing
- objective UI rendering behavior

Those belong in their own docs.

---

## System

- project-v

---

## Core Rule

Objectives are project-scoped planning records.

Objective routes must preserve all of the following:

- explicit project scope
- deterministic ordering
- controlled vocabulary status handling
- governed lifecycle transitions
- non-leaky cross-project rejection

Objective routes must not act like generic document storage or convenience mutation surfaces.

---

## Canonical Record Basis

This route family governs the `Objective` record defined in `schema-specification.md`.

Canonical fields:

- `id`
- `projectId`
- `key`
- `title`
- `description`
- `status`
- `priority`
- `targetStartAt`
- `targetEndAt`
- `createdAt`
- `updatedAt`

The route family must not introduce shadow fields that are not part of the governed objective model.

---

## Route Family

First-pass objective routes:

- `GET /objectives`
- `GET /objectives/{id}`
- `POST /objectives`
- `PATCH /objectives/{id}`
- `POST /objectives/{id}/status`

No delete route exists in the first pass.

---

## Scope Posture

All objective routes are project-scoped.

Project scope is resolved from the governed session/auth context.
The route must not trust caller-supplied project scope for authorization.

Where a route accepts `projectId` in the body or query for creation/filtering semantics, that value must still be validated against the governed session scope.
A mismatch must fail without cross-project leakage.

---

## `GET /objectives`

### Purpose
List objectives in current project scope.

### Query parameters
Allowed first-pass query parameters:

- `status`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

### Query parameter semantics

#### `status`
- optional
- controlled vocabulary value from objective status set
- invalid value -> `422 Unprocessable Entity`

#### `limit`
- optional
- positive integer
- bounded server-side maximum
- malformed or non-integer -> `400 Bad Request`
- out-of-range but well-formed -> `422 Unprocessable Entity`
- the server-side maximum is governed by shared implementation convention across Project V list families, not family-local choice

#### `cursor`
- optional
- opaque continuation token
- malformed cursor -> `400 Bad Request`

### Ordering
Default and required ordering:

```text
priority asc, updatedAt desc, id asc
```

This ordering is deterministic and must be the basis for cursor generation for this family.

### Response shape

```json
{
  "data": [
    {
      "id": "uuid",
      "projectId": "uuid",
      "key": "objective-key",
      "title": "text",
      "description": "text or null",
      "status": "proposed|active|blocked|completed|archived",
      "priority": 100,
      "targetStartAt": "timestamp or null",
      "targetEndAt": "timestamp or null",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- list responses return canonical objective fields only
- no hidden derived workflow fields should be injected unless a later doc governs them explicitly
- status filtering applies within current project scope only
- a valid status value that matches no objectives in current scope returns an empty data array
- the filter must not leak whether matching objectives exist in another project

---

## `GET /objectives/{id}`

### Purpose
Fetch one objective by identifier inside current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Behavior
- if objective exists in current project scope -> return canonical record
- if objective does not exist in current scope -> `404 Not Found`
- if objective exists in another project -> route must still preserve non-leakage posture and return `404 Not Found`

### Response shape

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "key": "objective-key",
  "title": "text",
  "description": "text or null",
  "status": "proposed|active|blocked|completed|archived",
  "priority": 100,
  "targetStartAt": "timestamp or null",
  "targetEndAt": "timestamp or null",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

---

## `POST /objectives`

### Purpose
Create a new objective in current project scope.

### Request body

```json
{
  "projectId": "uuid",
  "key": "objective-key",
  "title": "Objective title",
  "description": "Optional description",
  "priority": 100,
  "targetStartAt": "timestamp or null",
  "targetEndAt": "timestamp or null"
}
```

### Required fields
- `projectId`
- `key`
- `title`

### Optional fields
- `description`
- `priority`
- `targetStartAt`
- `targetEndAt`

### Forbidden fields
The caller must not supply:

- `id`
- `status`
- `createdAt`
- `updatedAt`

Supplying forbidden fields must fail with `400 Bad Request`.

### Defaults
- `status = proposed`
- `priority = 100` if omitted

### Validation
- `projectId` must match current governed project scope
- `key` must satisfy governed key format
- `title` must be non-empty
- `priority` must be within governed range; see `controlled-vocabularies.md` for the exact range and default
- if both target dates are present, `targetEndAt >= targetStartAt`
- duplicate `(projectId, key)` -> `409 Conflict`

### Response shape
Return `201 Created` with canonical record body.
The response body shape is the same as `GET /objectives/{id}` for the same record.

---

## `PATCH /objectives/{id}`

### Purpose
Apply bounded field updates to an objective.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Allowed fields
- `title`
- `description`
- `priority`
- `targetStartAt`
- `targetEndAt`

### Forbidden fields
The caller must not patch:

- `id`
- `projectId`
- `key`
- `status`
- `createdAt`
- `updatedAt`

Unknown PATCH fields must fail with `400 Bad Request`.
Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- objective must exist in current project scope or return `404 Not Found`
- `title`, if supplied, must be non-empty
- `priority`, if supplied, must remain within governed range; see `controlled-vocabularies.md` for the exact range and default
- if both target dates are present after patch application, `targetEndAt >= targetStartAt`

### Response shape
Return canonical objective record after patch.

### Notes
This route must not mutate `status`.
Lifecycle changes happen only through the status route.

---

## `POST /objectives/{id}/status`

### Purpose
Apply a governed status transition to an objective.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Request body

```json
{
  "newStatus": "active",
  "reason": "Optional reason when required"
}
```

### Required fields
- `newStatus`

### Optional fields
- `reason`

### Forbidden fields
The caller must not supply:

- `actor`
- `previousStatus`
- `projectId`
- any canonical objective fields outside this transition contract

Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- objective must exist in current project scope or return `404 Not Found`
- `newStatus` must be a valid objective status value
- transition must be legal according to `status-transitions.md`
- if the transition requires a reason, `reason` must be non-empty
- if the objective is already in `newStatus`, fail with `422 Unprocessable Entity`

### Atomicity rule
If the transition requires `StatusHistory`, the objective status update and `StatusHistory` row must be written in the same transaction.
The `actor` value must be server-resolved.

### Response shape
Return canonical objective record after transition.

---

## Status Transition Posture

Objective status values are governed by `controlled-vocabularies.md`.
Legal transition paths are governed by `status-transitions.md`.

This route family must not redefine objective lifecycle locally.
If the objective lifecycle changes, update the shared status-transition authority first.

---

## Validation and Error Posture

### `400 Bad Request`
Use for:

- malformed UUIDs
- malformed cursor
- unknown query parameters
- unknown PATCH fields
- forbidden caller-supplied fields
- wrong types
- missing required fields

### `422 Unprocessable Entity`
Use for:

- invalid controlled-vocabulary values
- out-of-range priority
- illegal status transition
- missing required reason for a governed transition
- invalid target-date relationship

### `404 Not Found`
Use for:

- objective not found in current project scope
- objective existing in another project but outside current scope

### `409 Conflict`
Use for:

- duplicate objective key within the same project scope

---

## Non-Leakage Rule

Objective routes must not leak whether an objective exists in another project.

A caller attempting to fetch or patch an objective outside current project scope must receive the same `404 Not Found` posture as for a genuinely absent objective.

Error body shape must not reveal whether the target exists elsewhere.

---

## Hammer Expectations

The hammer suite for objectives should verify at minimum:

- objective creation with valid input
- duplicate key rejection with `409`
- malformed UUID rejection with `400`
- unknown query parameter rejection with `400`
- unknown PATCH field rejection with `400`
- forbidden field rejection on create and patch
- deterministic list ordering
- cursor continuation correctness
- status filter non-leakage in list behavior
- illegal status transition rejection with `422`
- required-reason transition rejection with `422`
- status transition + history atomicity
- cross-project fetch/patch/status non-leakage

---

## Final Rule

Objectives are one of the core planning record families in Project V.

Their API family must stay simple, explicit, and lifecycle-governed.
If objective routes become a dumping ground for convenience behaviors, the family has drifted.

---

## Human-In-The-Loop Principle

Objective lifecycle state is governance-sensitive.

Operators and bounded LLMs must be able to trust that:

- list behavior is deterministic
- status changes follow one governed path
- hidden convenience mutation does not exist
- cross-project visibility is not accidentally leaked

The API family must preserve that trust structurally.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- objective routes are project-scoped and non-leaky
- `PATCH` is for bounded field updates only
- status changes require the dedicated status route
- `status` is not caller-settable on create or patch
- unknown fields and unknown query params are rejected, not ignored
- `404` does not imply the target never existed anywhere
- objective lifecycle is governed by shared transition authority, not local route improvisation

If implementation makes objective behavior more permissive or more magical than this document allows, the contract is being violated.

---

## Usage

This document should be used:

- when implementing objective routes
- when writing migrations or tests that depend on objective API behavior
- when writing hammer coverage for objective routes
- when reviewing whether objective behavior remains within bounded planning truth
- when writing later initiative and work-item family docs by analogy

---

## Related Docs

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../status-transitions.md`
- `../multi-project-doctrine.md`
- `../system-invariants.md`
- `../mcp-surface.md`
- `../schema-governance.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../ecosystem/vocabulary.md`
