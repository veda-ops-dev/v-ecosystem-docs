# Dependencies API Family

## Purpose

This document defines the first-pass API contract family for Project V dependencies.

It exists to answer:

```text
What routes exist for dependencies, what do they accept, what do they return, what validations and lifecycle rules apply, and how do dependencies behave as governed same-project relationships between Project V records?
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

- the dependency route family
- request and response shape for first-pass dependency routes
- dependency list ordering and filtering posture
- create and bounded update behavior
- same-project polymorphic reference validation for source and target entities
- controlled-vocabulary handling for `dependencyType` and `status`
- duplicate-logical-dependency prevention posture
- validation, error, and non-leakage posture for dependency routes

---

## Out of Scope

This document does not define:

- objective, initiative, or work-item routes
- generic API conventions shared by all route families
- schema migration sequencing
- dependency UI rendering behavior
- future dependency deletion semantics

Those belong in their own docs.

---

## System

- project-v

---

## Core Rule

Dependencies are project-scoped explicit relationships between governed Project V records.

Dependency routes must preserve all of the following:

- explicit project scope
- deterministic ordering
- same-project polymorphic reference validation
- controlled-vocabulary dependency-type handling
- controlled-vocabulary status handling
- duplicate-logical-dependency prevention
- non-leaky cross-project rejection

Dependency routes must not act like free-form graph storage or generic cross-system linkage surfaces.

---

## Canonical Record Basis

This route family governs the `Dependency` record defined in `schema-specification.md`.

Canonical fields:

- `id`
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `targetEntityType`
- `targetEntityId`
- `dependencyType`
- `status`
- `rationale`
- `createdAt`
- `updatedAt`

The route family must not introduce shadow fields that are not part of the governed dependency model.

---

## Route Family

First-pass dependency routes:

- `GET /dependencies`
- `GET /dependencies/{id}`
- `POST /dependencies`
- `PATCH /dependencies/{id}`

No delete route exists in the first pass.
No dedicated status-transition route exists in the first pass because dependency status updates are bounded field updates, not governed lifecycle transitions with `StatusHistory`.

---

## Scope Posture

All dependency routes are project-scoped.

Project scope is resolved from the governed session/auth context.
The route must not trust caller-supplied project scope for authorization.

Where a route accepts `projectId` in the body or query for creation/filtering semantics, that value must still be validated against the governed session scope.
A mismatch must fail without cross-project leakage.

---

## Polymorphic Reference Rule

Dependencies use two polymorphic references:

- `sourceEntityType` + `sourceEntityId`
- `targetEntityType` + `targetEntityId`

Both references must follow `polymorphic-reference-enforcement.md`.

That means:

- allowed entity types are not free-form
- both referenced entities must exist
- both referenced entities must belong to the same project scope as the dependency row
- cross-project references must fail without existence leakage
- the source and target pair must be resolved before commit

Allowed dependency entity types are governed by `polymorphic-reference-enforcement.md`.
This route family must not redefine them locally.

---

## Identity Rule

A dependency is identified logically by this tuple inside a project scope:

```text
(projectId, sourceEntityType, sourceEntityId, targetEntityType, targetEntityId, dependencyType)
```

The first-pass unique constraint on that tuple is structural authority.
Duplicate logical dependencies in the same scope must fail with `409 Conflict`.

---

## Self-Reference Rule

A dependency must not point from an entity to itself.

If both:

- `sourceEntityType == targetEntityType`
- `sourceEntityId == targetEntityId`

then the request must fail with `422 Unprocessable Entity`.

---

## `GET /dependencies`

### Purpose
List dependencies in current project scope.

### Query parameters
Allowed first-pass query parameters:

- `sourceEntityType`
- `sourceEntityId`
- `targetEntityType`
- `targetEntityId`
- `dependencyType`
- `status`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

### Query parameter semantics

#### `sourceEntityType`
- optional
- controlled by allowed dependency entity-type set from `polymorphic-reference-enforcement.md`
- invalid value -> `422 Unprocessable Entity`

#### `sourceEntityId`
- optional
- UUID
- malformed UUID -> `400 Bad Request`
- if supplied with `sourceEntityType`, filters dependencies whose source matches that exact resolved entity in current project scope
- if the referenced source entity is not found in current project scope — whether it exists elsewhere or not — the route must return an empty result set without revealing whether the entity exists in another project

#### `targetEntityType`
- optional
- controlled by allowed dependency entity-type set from `polymorphic-reference-enforcement.md`
- invalid value -> `422 Unprocessable Entity`

#### `targetEntityId`
- optional
- UUID
- malformed UUID -> `400 Bad Request`
- if supplied with `targetEntityType`, filters dependencies whose target matches that exact resolved entity in current project scope
- if the referenced target entity is not found in current project scope — whether it exists elsewhere or not — the route must return an empty result set without revealing whether the entity exists in another project

#### `dependencyType`
- optional
- controlled-vocabulary value from dependency-type set
- invalid value -> `422 Unprocessable Entity`

#### `status`
- optional
- controlled-vocabulary value from dependency status set
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

### Pairing rule
`sourceEntityId` must not be supplied without `sourceEntityType`.
`targetEntityId` must not be supplied without `targetEntityType`.

A missing type for a supplied entity id is a structurally malformed filter and must fail with `400 Bad Request`.

### Ordering
Default and required ordering:

```text
updatedAt desc, id asc
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
      "targetEntityType": "controlled-value",
      "targetEntityId": "uuid",
      "dependencyType": "controlled-value",
      "status": "controlled-value",
      "rationale": "text or null",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- list responses return canonical dependency fields only
- all filters apply within current project scope only
- a valid filter value that matches no dependencies in current scope returns an empty data array
- filters must not leak whether referenced entities exist in another project

---

## `GET /dependencies/{id}`

### Purpose
Fetch one dependency by identifier inside current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Behavior
- if dependency exists in current project scope -> return canonical record
- if dependency does not exist in current scope -> `404 Not Found`
- if dependency exists in another project -> route must still preserve non-leakage posture and return `404 Not Found`

### Response shape

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "sourceEntityType": "controlled-value",
  "sourceEntityId": "uuid",
  "targetEntityType": "controlled-value",
  "targetEntityId": "uuid",
  "dependencyType": "controlled-value",
  "status": "controlled-value",
  "rationale": "text or null",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

---

## `POST /dependencies`

### Purpose
Create a new dependency in current project scope.

### Request body

```json
{
  "projectId": "uuid",
  "sourceEntityType": "initiative",
  "sourceEntityId": "uuid",
  "targetEntityType": "work_item",
  "targetEntityId": "uuid",
  "dependencyType": "blocks",
  "rationale": "Optional rationale"
}
```

### Required fields
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `targetEntityType`
- `targetEntityId`
- `dependencyType`

### Optional fields
- `rationale`

### Forbidden fields
The caller must not supply:

- `id`
- `status`
- `createdAt`
- `updatedAt`

Supplying forbidden fields must fail with `400 Bad Request`.

### Defaults
- `status = active`

### Validation
- `projectId` must match current governed project scope
- `sourceEntityType` must be an allowed dependency source type
- `targetEntityType` must be an allowed dependency target type
- `sourceEntityId` and `targetEntityId` must be valid UUIDs
- source and target must resolve inside current project scope
- source and target must not refer to the same logical entity
- `dependencyType` must be a valid dependency-type value
- duplicate logical dependency tuple -> `409 Conflict`

### Response shape
Return `201 Created` with canonical record body.
The response body shape is the same as `GET /dependencies/{id}` for the same record.

---

## `PATCH /dependencies/{id}`

### Purpose
Apply bounded field updates to a dependency.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Allowed fields
- `status`
- `rationale`

### Forbidden fields
The caller must not patch:

- `id`
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `targetEntityType`
- `targetEntityId`
- `dependencyType`
- `createdAt`
- `updatedAt`

Unknown PATCH fields must fail with `400 Bad Request`.
Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- dependency must exist in current project scope or return `404 Not Found`
- `status`, if supplied, must be a non-null valid dependency status value; supplying `status = null` must fail with `422 Unprocessable Entity`
- `rationale`, if supplied, may be `null` or non-empty text in the first pass

### Response shape
Return canonical dependency record after patch.

### Notes
This route must not mutate source identity, target identity, or dependency type.
Changing the logical identity of a dependency is not a bounded patch in the first pass.

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
- `sourceEntityId` without `sourceEntityType`
- `targetEntityId` without `targetEntityType`

### `422 Unprocessable Entity`
Use for:

- invalid controlled-vocabulary values
- invalid allowed dependency entity-type values
- same-entity self-reference
- invalid polymorphic reference shape when the request is otherwise well-formed
- cross-project polymorphic target/reference rejection without existence leakage

### `404 Not Found`
Use for:

- dependency not found in current project scope
- dependency existing in another project but outside current scope

### `409 Conflict`
Use for:

- duplicate logical dependency tuple within the same project scope

---

## Non-Leakage Rule

Dependency routes must not leak whether a dependency or a referenced source/target entity exists in another project.

A caller attempting to fetch or patch a dependency outside current project scope must receive the same `404 Not Found` posture as for a genuinely absent dependency.

Entity-targeted list filters must return empty results rather than revealing whether a referenced entity exists elsewhere.

Error body shape must not reveal whether the target exists elsewhere.

---

## Hammer Expectations

The hammer suite for dependencies should verify at minimum:

- dependency creation with valid input
- duplicate logical dependency rejection with `409`
- malformed UUID rejection with `400`
- sourceEntityId-without-type rejection with `400`
- targetEntityId-without-type rejection with `400`
- unknown query parameter rejection with `400`
- unknown PATCH field rejection with `400`
- forbidden field rejection on create and patch
- deterministic list ordering
- cursor continuation correctness
- source and target entity filter non-leakage in list behavior
- same-project polymorphic reference validation on create
- self-reference rejection with `422`
- invalid dependencyType rejection with `422`
- invalid dependency status rejection with `422`
- cross-project fetch/patch non-leakage

---

## Final Rule

Dependencies are governed same-project relationships, not free-form graph edges.

Their API family must stay simple, explicit, and identity-stable.
If dependency routes become a dumping ground for graph-like convenience mutation or cross-project linkage, the family has drifted.

---

## Human-In-The-Loop Principle

Dependency linkage is governance-sensitive because it shapes planning interpretation and execution readiness.

Operators and bounded LLMs must be able to trust that:

- dependency identity is explicit and stable
- source and target references are same-project validated
- duplicate logical dependencies are prevented
- hidden cross-project linkage does not exist
- list filters do not leak out-of-scope entity existence

The API family must preserve that trust structurally.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- dependency routes are project-scoped and non-leaky
- dependencies are identified by a logical tuple, not just row id
- source and target references are governed polymorphic pairs, not free-form fields
- `PATCH` is only for bounded updates to `status` and `rationale`
- duplicate logical dependencies must fail with `409`
- self-reference is illegal
- sourceEntityId and targetEntityId filters require their paired type filters
- `404` does not imply a dependency or referenced entity never existed anywhere

If implementation makes dependency behavior more permissive or more graph-like than this document allows, the contract is being violated.

---

## Usage

This document should be used:

- when implementing dependency routes
- when writing migrations or tests that depend on dependency API behavior
- when writing hammer coverage for dependency routes
- when reviewing whether dependency behavior remains within bounded planning truth
- when writing later readiness and handoff family docs by analogy

---

## Related Docs

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../status-transitions.md`
- `../polymorphic-reference-enforcement.md`
- `../multi-project-doctrine.md`
- `../system-invariants.md`
- `../mcp-surface.md`
- `../schema-governance.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../ecosystem/vocabulary.md`
