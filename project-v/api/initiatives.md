# Initiatives API Family

## Purpose

This document defines the first-pass API contract family for Project V initiatives.

It exists to answer:

```text
What routes exist for initiatives, what do they accept, what do they return, what validations and lifecycle rules apply, and how do initiatives behave as governed project-scoped planning records linked to objectives and target systems?
```

Read this with:

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../status-transitions.md`
- `../multi-project-doctrine.md`
- `../polymorphic-reference-enforcement.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the initiative route family
- request and response shape for first-pass initiative routes
- initiative list ordering and filtering posture
- create, read, update, and status-transition behavior
- same-project parent-link validation for `objectiveId`
- target-system validation posture
- validation, error, and non-leakage posture for initiative routes
- transaction behavior where status history is required

---

## Out of Scope

This document does not define:

- objective or work-item routes
- generic API conventions shared by all route families
- schema migration sequencing
- initiative UI rendering behavior

Those belong in their own docs.

---

## System

- project-v

---

## Core Rule

Initiatives are project-scoped bounded bodies of work.

Initiative routes must preserve all of the following:

- explicit project scope
- deterministic ordering
- controlled-vocabulary status handling
- controlled-vocabulary target-system handling
- governed lifecycle transitions
- same-project parent-link validation
- non-leaky cross-project rejection

Initiative routes must not act like generic document storage or convenience mutation surfaces.

---

## Canonical Record Basis

This route family governs the `Initiative` record defined in `schema-specification.md`.

Canonical fields:

- `id`
- `projectId`
- `objectiveId`
- `key`
- `title`
- `description`
- `status`
- `priority`
- `targetSystem`
- `createdAt`
- `updatedAt`

The route family must not introduce shadow fields that are not part of the governed initiative model.

---

## Route Family

First-pass initiative routes:

- `GET /initiatives`
- `GET /initiatives/{id}`
- `POST /initiatives`
- `PATCH /initiatives/{id}`
- `POST /initiatives/{id}/status`

No delete route exists in the first pass.

---

## Scope Posture

All initiative routes are project-scoped.

Project scope is resolved from the governed session/auth context.
The route must not trust caller-supplied project scope for authorization.

Where a route accepts `projectId` in the body or query for creation/filtering semantics, that value must still be validated against the governed session scope.
A mismatch must fail without cross-project leakage.

---

## Parent-Link Rule

`objectiveId` is optional, but when supplied it must resolve to an `Objective` in the same project scope as the initiative.

This route family must not allow:

- linking an initiative to an objective in another project
- linking an initiative to a non-existent objective
- silently dropping an invalid `objectiveId`

Validation must happen before commit.

---

## Target-System Rule

`targetSystem` is optional on initiatives.

When supplied, it must use the governed initiative target-system vocabulary from `controlled-vocabularies.md`.

Invalid target-system values must fail with `422 Unprocessable Entity`.

---

## `GET /initiatives`

### Purpose
List initiatives in current project scope.

### Query parameters
Allowed first-pass query parameters:

- `status`
- `objectiveId`
- `targetSystem`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

### Query parameter semantics

#### `status`
- optional
- controlled-vocabulary value from initiative status set
- invalid value -> `422 Unprocessable Entity`

#### `objectiveId`
- optional
- UUID
- malformed UUID -> `400 Bad Request`
- if supplied, filters initiatives linked to that objective within current project scope
- if the referenced objective is not found in current project scope — whether it exists elsewhere or not — the route must return an empty result set without revealing whether the objective exists in another project

#### `targetSystem`
- optional
- controlled-vocabulary value from initiative target-system set
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
      "objectiveId": "uuid or null",
      "key": "initiative-key",
      "title": "text",
      "description": "text or null",
      "status": "proposed|active|blocked|completed|archived",
      "priority": 100,
      "targetSystem": "project_v|veda|v_forge|null",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- list responses return canonical initiative fields only
- no hidden derived workflow fields should be injected unless a later doc governs them explicitly

---

## `GET /initiatives/{id}`

### Purpose
Fetch one initiative by identifier inside current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Behavior
- if initiative exists in current project scope -> return canonical record
- if initiative does not exist in current scope -> `404 Not Found`
- if initiative exists in another project -> route must still preserve non-leakage posture and return `404 Not Found`

### Response shape

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "objectiveId": "uuid or null",
  "key": "initiative-key",
  "title": "text",
  "description": "text or null",
  "status": "proposed|active|blocked|completed|archived",
  "priority": 100,
  "targetSystem": "project_v|veda|v_forge|null",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

---

## `POST /initiatives`

### Purpose
Create a new initiative in current project scope.

### Request body

```json
{
  "projectId": "uuid",
  "objectiveId": "uuid or null",
  "key": "initiative-key",
  "title": "Initiative title",
  "description": "Optional description",
  "priority": 100,
  "targetSystem": "v_forge"
}
```

### Required fields
- `projectId`
- `key`
- `title`

### Optional fields
- `objectiveId`
- `description`
- `priority`
- `targetSystem`

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
- if `objectiveId` is supplied, it must resolve to an objective in current project scope
- if `targetSystem` is supplied, it must be a valid initiative target-system value
- duplicate `(projectId, key)` -> `409 Conflict`

### Response shape
Return `201 Created` with canonical record body.
The response body shape is the same as `GET /initiatives/{id}` for the same record.

---

## `PATCH /initiatives/{id}`

### Purpose
Apply bounded field updates to an initiative.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Allowed fields
- `title`
- `description`
- `objectiveId`
- `priority`
- `targetSystem`

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
- initiative must exist in current project scope or return `404 Not Found`
- `title`, if supplied, must be non-empty
- `priority`, if supplied, must remain within governed range; see `controlled-vocabularies.md` for the exact range and default
- `objectiveId`, if supplied and non-null, must resolve to an objective in current project scope
- `targetSystem`, if supplied and non-null, must be a valid initiative target-system value

### Response shape
Return canonical initiative record after patch.

### Notes
This route must not mutate `status`.
Lifecycle changes happen only through the status route.
Setting `objectiveId` to `null` is allowed in the first pass and explicitly detaches the initiative from an objective.

---

## `POST /initiatives/{id}/status`

### Purpose
Apply a governed status transition to an initiative.

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
- any canonical initiative fields outside this transition contract

Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- initiative must exist in current project scope or return `404 Not Found`
- `newStatus` must be a valid initiative status value
- transition must be legal according to `status-transitions.md`
- if the transition requires a reason, `reason` must be non-empty
- if the initiative is already in `newStatus`, fail with `422 Unprocessable Entity`

### Atomicity rule
If the transition requires `StatusHistory`, the initiative status update and `StatusHistory` row must be written in the same transaction.
The `actor` value must be server-resolved.

### Response shape
Return canonical initiative record after transition.

---

## Status Transition Posture

Initiative status values are governed by `controlled-vocabularies.md`.
Legal transition paths are governed by `status-transitions.md`.

This route family must not redefine initiative lifecycle locally.
If the initiative lifecycle changes, update the shared status-transition authority first.

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
- invalid `objectiveId` link shape when the request is well-formed but semantically invalid

### `404 Not Found`
Use for:

- initiative not found in current project scope
- initiative existing in another project but outside current scope

### `409 Conflict`
Use for:

- duplicate initiative key within the same project scope

---

## Non-Leakage Rule

Initiative routes must not leak whether an initiative or parent objective exists in another project.

A caller attempting to fetch, patch, or transition an initiative outside current project scope must receive the same `404 Not Found` posture as for a genuinely absent initiative.

Error body shape must not reveal whether the target exists elsewhere.

---

## Hammer Expectations

The hammer suite for initiatives should verify at minimum:

- initiative creation with valid input
- duplicate key rejection with `409`
- malformed UUID rejection with `400`
- unknown query parameter rejection with `400`
- unknown PATCH field rejection with `400`
- forbidden field rejection on create and patch
- deterministic list ordering
- cursor continuation correctness
- objectiveId filter non-leakage in list behavior
- same-project `objectiveId` validation on create and patch
- invalid target-system rejection with `422`
- illegal status transition rejection with `422`
- required-reason transition rejection with `422`
- status transition + history atomicity
- cross-project fetch/patch/status non-leakage

---

## Final Rule

Initiatives are one of the core bounded work-planning record families in Project V.

Their API family must stay simple, explicit, and lifecycle-governed.
If initiative routes become a dumping ground for convenience behaviors or hidden parent-link magic, the family has drifted.

---

## Human-In-The-Loop Principle

Initiative lifecycle and parent linkage are governance-sensitive.

Operators and bounded LLMs must be able to trust that:

- list behavior is deterministic
- parent linkage is same-project validated
- status changes follow one governed path
- hidden convenience mutation does not exist
- cross-project visibility is not accidentally leaked

The API family must preserve that trust structurally.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- initiative routes are project-scoped and non-leaky
- `PATCH` is for bounded field updates only
- status changes require the dedicated status route
- `status` is not caller-settable on create or patch
- `objectiveId` is optional but governed when present
- `targetSystem` is optional but must use a controlled value when present
- unknown fields and unknown query params are rejected, not ignored
- `404` does not imply the target never existed anywhere
- initiative lifecycle is governed by shared transition authority, not local route improvisation

If implementation makes initiative behavior more permissive or more magical than this document allows, the contract is being violated.

---

## Usage

This document should be used:

- when implementing initiative routes
- when writing migrations or tests that depend on initiative API behavior
- when writing hammer coverage for initiative routes
- when reviewing whether initiative behavior remains within bounded planning truth
- when writing later work-item family docs by analogy

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
