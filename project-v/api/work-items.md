# Work Items API Family

## Purpose

This document defines the first-pass API contract family for Project V work items.

It exists to answer:

```text
What routes exist for work items, what do they accept, what do they return, what validations and lifecycle rules apply, and how do work items behave as governed project-scoped planning and handoff-preparation records?
```

Read this with:

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../status-transitions.md`
- `../multi-project-doctrine.md`
- `../polymorphic-reference-enforcement.md`
- `../readiness-evaluation-rules.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the work-item route family
- request and response shape for first-pass work-item routes
- work-item list ordering and filtering posture
- create, read, update, and status-transition behavior
- same-project parent-link validation for `initiativeId`
- controlled-vocabulary handling for `type`, `status`, `readinessState`, and `targetSystem`
- server-owned field posture for `readinessState`
- blocked-state validation posture for `blocked` and `blockedReason`
- validation, error, and non-leakage posture for work-item routes
- transaction behavior where status history is required

---

## Out of Scope

This document does not define:

- objective or initiative routes
- generic API conventions shared by all route families
- readiness evaluation execution routes beyond their effect on work-item state
- schema migration sequencing
- work-item UI rendering behavior

Those belong in their own docs.

---

## System

- project-v

---

## Core Rule

Work items are project-scoped planning and handoff-preparation records.

Work-item routes must preserve all of the following:

- explicit project scope
- deterministic ordering
- controlled-vocabulary type handling
- controlled-vocabulary target-system handling
- governed lifecycle transitions
- same-project parent-link validation
- server-owned readiness-state handling
- explicit blocked-state behavior
- non-leaky cross-project rejection

Work-item routes must not act like generic task storage or convenience mutation surfaces.

---

## Canonical Record Basis

This route family governs the `WorkItem` record defined in `schema-specification.md`.

Canonical fields:

- `id`
- `projectId`
- `initiativeId`
- `key`
- `title`
- `description`
- `type`
- `status`
- `readinessState`
- `targetSystem`
- `blocked`
- `blockedReason`
- `createdAt`
- `updatedAt`

The route family must not introduce shadow fields that are not part of the governed work-item model.

---

## Route Family

First-pass work-item routes:

- `GET /work-items`
- `GET /work-items/{id}`
- `POST /work-items`
- `PATCH /work-items/{id}`
- `POST /work-items/{id}/status`

No delete route exists in the first pass.

---

## Scope Posture

All work-item routes are project-scoped.

Project scope is resolved from the governed session/auth context.
The route must not trust caller-supplied project scope for authorization.

Where a route accepts `projectId` in the body or query for creation/filtering semantics, that value must still be validated against the governed session scope.
A mismatch must fail without cross-project leakage.

---

## Parent-Link Rule

`initiativeId` is optional, but when supplied it must resolve to an `Initiative` in the same project scope as the work item.

This route family must not allow:

- linking a work item to an initiative in another project
- linking a work item to a non-existent initiative
- silently dropping an invalid `initiativeId`

Validation must happen before commit.

---

## Type Rule

`type` is required on work items.

It must use the governed work-item type vocabulary from `controlled-vocabularies.md`.
Invalid work-item type values must fail with `422 Unprocessable Entity`.

---

## Target-System Rule

`targetSystem` is required on work items.

It must use the governed work-item target-system vocabulary from `controlled-vocabularies.md`.
Invalid target-system values must fail with `422 Unprocessable Entity`.

---

## Readiness-State Rule

`readinessState` is server-owned.

It must not be caller-settable on create, patch, or status-transition routes.
It changes only through governed readiness evaluation behavior as defined by `readiness-evaluation-rules.md` and related authority docs.

Supplying `readinessState` where the route contract does not permit it must fail with `400 Bad Request`.

The full set of allowed readiness-state values is governed by `controlled-vocabularies.md`.
The meaning and transition conditions for each value are defined in `readiness-evaluation-rules.md`.

---

## Blocked-State Rule

`blocked` and `blockedReason` must be treated together.

First-pass route posture:

- when `blocked = true`, `blockedReason` must be non-empty after request application
- when `blocked = false`, `blockedReason` may be `null`
- the route must not silently preserve an old `blockedReason` if the caller explicitly clears the blocked state and supplies `blockedReason = null`
- the route must not silently allow `blocked = true` with an empty or null reason

This is a semantic validity rule and must fail with `422 Unprocessable Entity` when violated.

---

## `GET /work-items`

### Purpose
List work items in current project scope.

### Query parameters
Allowed first-pass query parameters:

- `status`
- `type`
- `readinessState`
- `initiativeId`
- `targetSystem`
- `blocked`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

### Query parameter semantics

#### `status`
- optional
- controlled-vocabulary value from work-item status set
- invalid value -> `422 Unprocessable Entity`

#### `type`
- optional
- controlled-vocabulary value from work-item type set
- invalid value -> `422 Unprocessable Entity`

#### `readinessState`
- optional
- controlled-vocabulary value from work-item readiness-state set
- invalid value -> `422 Unprocessable Entity`

#### `initiativeId`
- optional
- UUID
- malformed UUID -> `400 Bad Request`
- if supplied, filters work items linked to that initiative within current project scope
- if the referenced initiative is not found in current project scope — whether it exists elsewhere or not — the route must return an empty result set without revealing whether the initiative exists in another project

#### `targetSystem`
- optional
- controlled-vocabulary value from work-item target-system set
- invalid value -> `422 Unprocessable Entity`

#### `blocked`
- optional
- boolean
- malformed or non-boolean value -> `400 Bad Request`

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
status asc, updatedAt desc, id asc
```

This ordering is deterministic and must be the basis for cursor generation for this family.
`WorkItem` has no `priority` field. Ordering by status first groups active and blocked items before completed and archived ones, giving operators a useful default view.

### Response shape

```json
{
  "data": [
    {
      "id": "uuid",
      "projectId": "uuid",
      "initiativeId": "uuid or null",
      "key": "work-item-key",
      "title": "text",
      "description": "text or null",
      "type": "controlled-value",
      "status": "proposed|active|blocked|completed|archived",
      "readinessState": "unevaluated|not_ready|ready_with_warnings|ready|deferred",
      "targetSystem": "project_v|veda|v_forge",
      "blocked": true,
      "blockedReason": "text or null",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- list responses return canonical work-item fields only
- no hidden derived workflow fields should be injected unless a later doc governs them explicitly
- all filters apply within current project scope only
- a valid filter value that matches no work items in current scope returns an empty data array
- filters must not leak whether matching work items or parent initiatives exist in another project

---

## `GET /work-items/{id}`

### Purpose
Fetch one work item by identifier inside current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Behavior
- if work item exists in current project scope -> return canonical record
- if work item does not exist in current scope -> `404 Not Found`
- if work item exists in another project -> route must still preserve non-leakage posture and return `404 Not Found`

### Response shape

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "initiativeId": "uuid or null",
  "key": "work-item-key",
  "title": "text",
  "description": "text or null",
  "type": "controlled-value",
  "status": "proposed|active|blocked|completed|archived",
  "readinessState": "unevaluated|not_ready|ready_with_warnings|ready|deferred",
  "targetSystem": "project_v|veda|v_forge",
  "blocked": true,
  "blockedReason": "text or null",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

---

## `POST /work-items`

### Purpose
Create a new work item in current project scope.

### Request body

```json
{
  "projectId": "uuid",
  "initiativeId": "uuid or null",
  "key": "work-item-key",
  "title": "Work item title",
  "description": "Optional description",
  "type": "controlled-value",
  "targetSystem": "v_forge",
  "blocked": false,
  "blockedReason": null
}
```

### Required fields
- `projectId`
- `key`
- `title`
- `type`
- `targetSystem`

### Optional fields
- `initiativeId`
- `description`
- `blocked`
- `blockedReason`

### Forbidden fields
The caller must not supply:

- `id`
- `status`
- `readinessState`
- `createdAt`
- `updatedAt`

Supplying forbidden fields must fail with `400 Bad Request`.

### Defaults
- `status = proposed`
- `readinessState = unevaluated`
- `blocked = false` if omitted
- `blockedReason = null` if omitted and `blocked = false`

### Validation
- `projectId` must match current governed project scope
- `key` must satisfy governed key format
- `title` must be non-empty
- `type` must be a valid work-item type value
- `targetSystem` must be a valid work-item target-system value
- if `initiativeId` is supplied, it must resolve to an initiative in current project scope
- if `blocked = true`, `blockedReason` must be non-empty
- if `blocked = false` and `blockedReason` is omitted, it defaults to `null`
- duplicate `(projectId, key)` -> `409 Conflict`

### Response shape
Return `201 Created` with canonical record body.
The response body shape is the same as `GET /work-items/{id}` for the same record.

---

## `PATCH /work-items/{id}`

### Purpose
Apply bounded field updates to a work item.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Allowed fields
- `title`
- `description`
- `initiativeId`
- `type`
- `targetSystem`
- `blocked`
- `blockedReason`

### Forbidden fields
The caller must not patch:

- `id`
- `projectId`
- `key`
- `status`
- `readinessState`
- `createdAt`
- `updatedAt`

Unknown PATCH fields must fail with `400 Bad Request`.
Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- work item must exist in current project scope or return `404 Not Found`
- `title`, if supplied, must be non-empty
- `initiativeId`, if supplied and non-null, must resolve to an initiative in current project scope
- `type`, if supplied, must be a non-null valid work-item type value; supplying `type = null` must fail with `422 Unprocessable Entity`
- `targetSystem`, if supplied, must be a non-null valid work-item target-system value; supplying `targetSystem = null` must fail with `422 Unprocessable Entity`
- after patch application, if `blocked = true`, `blockedReason` must be non-empty
- after patch application, if `blocked = false` and `blockedReason` is explicitly supplied as `null`, the cleared value must be preserved as `null`

### Response shape
Return canonical work-item record after patch.

### Notes
This route must not mutate `status`.
Lifecycle changes happen only through the status route.
Setting `initiativeId` to `null` is allowed in the first pass and explicitly detaches the work item from an initiative.

---

## `POST /work-items/{id}/status`

### Purpose
Apply a governed status transition to a work item.

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
- `readinessState`
- any canonical work-item fields outside this transition contract

Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- work item must exist in current project scope or return `404 Not Found`
- `newStatus` must be a valid work-item status value
- transition must be legal according to `status-transitions.md`
- if the transition requires a reason, `reason` must be non-empty
- if the work item is already in `newStatus`, fail with `422 Unprocessable Entity`

### Atomicity rule
If the transition requires `StatusHistory`, the work-item status update and `StatusHistory` row must be written in the same transaction.
The `actor` value must be server-resolved.

### Response shape
Return canonical work-item record after transition.

---

## Status Transition Posture

Work-item status values are governed by `controlled-vocabularies.md`.
Legal transition paths are governed by `status-transitions.md`.

This route family must not redefine work-item lifecycle locally.
If the work-item lifecycle changes, update the shared status-transition authority first.

---

## Validation and Error Posture

### `400 Bad Request`
Use for:

- malformed UUIDs
- malformed cursor
- malformed `blocked` query value
- unknown query parameters
- unknown PATCH fields
- forbidden caller-supplied fields
- wrong types
- missing required fields

### `422 Unprocessable Entity`
Use for:

- invalid controlled-vocabulary values
- illegal status transition
- missing required reason for a governed transition
- invalid `initiativeId` link shape when the request is well-formed but semantically invalid
- invalid blocked-state combination

### `404 Not Found`
Use for:

- work item not found in current project scope
- work item existing in another project but outside current scope

### `409 Conflict`
Use for:

- duplicate work-item key within the same project scope

---

## Non-Leakage Rule

Work-item routes must not leak whether a work item or parent initiative exists in another project.

A caller attempting to fetch, patch, or transition a work item outside current project scope must receive the same `404 Not Found` posture as for a genuinely absent work item.

Error body shape must not reveal whether the target exists elsewhere.

---

## Hammer Expectations

The hammer suite for work items should verify at minimum:

- work-item creation with valid input
- duplicate key rejection with `409`
- malformed UUID rejection with `400`
- unknown query parameter rejection with `400`
- unknown PATCH field rejection with `400`
- forbidden field rejection on create, patch, and status routes
- deterministic list ordering
- cursor continuation correctness
- initiativeId filter non-leakage in list behavior
- same-project `initiativeId` validation on create and patch
- invalid `type` rejection with `422`
- invalid `targetSystem` rejection with `422`
- caller-supplied `readinessState` rejection with `400`
- blocked-state invalid combination rejection with `422`
- illegal status transition rejection with `422`
- required-reason transition rejection with `422`
- status transition + history atomicity
- cross-project fetch/patch/status non-leakage

---

## Final Rule

Work items are one of the core bounded planning and handoff-preparation record families in Project V.

Their API family must stay simple, explicit, and lifecycle-governed.
If work-item routes become a dumping ground for convenience behaviors, hidden readiness mutation, or soft blocked-state semantics, the family has drifted.

---

## Human-In-The-Loop Principle

Work-item lifecycle, readiness posture, and blocked-state handling are governance-sensitive.

Operators and bounded LLMs must be able to trust that:

- list behavior is deterministic
- parent linkage is same-project validated
- readiness state is not caller-controlled
- blocked state has explicit rules
- status changes follow one governed path
- cross-project visibility is not accidentally leaked

The API family must preserve that trust structurally.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- work-item routes are project-scoped and non-leaky
- `PATCH` is for bounded field updates only
- status changes require the dedicated status route
- `type` and `targetSystem` are controlled values
- `readinessState` is server-owned and must not be caller-set
- `initiativeId` is optional but governed when present
- `blocked` and `blockedReason` are coupled and semantically validated together
- unknown fields and unknown query params are rejected, not ignored
- `404` does not imply the target never existed anywhere
- work-item lifecycle is governed by shared transition authority, not local route improvisation

If implementation makes work-item behavior more permissive or more magical than this document allows, the contract is being violated.

---

## Usage

This document should be used:

- when implementing work-item routes
- when writing migrations or tests that depend on work-item API behavior
- when writing hammer coverage for work-item routes
- when reviewing whether work-item behavior remains within bounded planning truth
- when writing later dependency, readiness, and handoff family docs by analogy

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
- `../readiness-evaluation-rules.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../ecosystem/vocabulary.md`
