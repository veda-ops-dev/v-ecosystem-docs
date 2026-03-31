# Handoffs API Family

## Purpose

This document defines the first-pass API contract family for Project V handoffs.

It exists to answer:

```text
What routes exist for handoffs, what do they accept, what do they return, what validations and lifecycle rules apply, and how do handoffs behave as governed project-scoped planning-to-execution transfer records?
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
- `../v-forge-integration.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../../workflows/handoff-workflow.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the handoff route family
- request and response shape for first-pass handoff routes
- handoff list ordering and filtering posture
- create, read, update, and status-transition behavior
- same-project polymorphic source-entity validation
- controlled-vocabulary handling for `sourceEntityType`, `targetSystem`, `handoffType`, and `status`
- server-owned field posture for `completedAt`
- transition rules and their atomicity requirements
- reverse re-entry and recall posture at the API level
- validation, error, and non-leakage posture for handoff routes
- relationship to return-to-planning without reproducing interface doctrine

---

## Out of Scope

This document does not define:

- the cross-system handoff interface contract (see `../../interfaces/project-v-to-v-forge-handoff-interface.md`)
- the return-to-planning interface (see `../../interfaces/v-forge-to-project-v-return-to-planning-interface.md`)
- the cross-system handoff workflow (see `../../workflows/handoff-workflow.md`)
- the full approval and escalation model (see `../../governance/approval-and-escalation-model.md`)
- V Forge internal execution lifecycle
- readiness evaluation or audit route families
- schema migration sequencing
- handoff UI rendering behavior

---

## System

- project-v

---

## Core Rule

Handoffs are project-scoped planning records that capture the Project V side of bounded execution-responsibility transfer.

Handoff routes must preserve all of the following:

- explicit project scope
- deterministic ordering
- same-project polymorphic source-entity validation
- controlled-vocabulary handling for `targetSystem`, `handoffType`, and `status`
- governed lifecycle transitions with full `StatusHistory` support
- `completedAt` atomicity when the `closed` status is reached
- non-leaky cross-project rejection

Handoff routes represent planning truth about execution-responsibility transfer.
They do not own V Forge execution truth.
They do not act as the canonical execution ledger.

---

## What a Handoff Record Is

A `Handoff` record in Project V is the planning-side record of a bounded execution-responsibility transfer.

It records:

- what planning entity is the source of the transfer
- what target system is the execution destination
- what type of handoff is occurring
- what readiness basis justified the transfer
- the lifecycle status of the transfer from a planning-side perspective
- when the transfer reached a closed terminal state

A handoff record does not store V Forge execution state.
A handoff record does not store execution outputs, execution logs, or execution findings.
A handoff record is Project V's planning-side view of whether and how a bounded execution-responsibility transfer was prepared, activated, and concluded.

---

## Canonical Record Basis

This route family governs the `Handoff` record defined in `schema-specification.md`.

Canonical fields:

- `id`
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `targetSystem`
- `handoffType`
- `status`
- `readinessBasisSummary`
- `createdAt`
- `completedAt`
- `updatedAt`

The route family must not introduce shadow fields that are not part of the governed handoff model.

---

## Route Family

First-pass handoff routes:

- `GET /handoffs`
- `GET /handoffs/{id}`
- `POST /handoffs`
- `PATCH /handoffs/{id}`
- `POST /handoffs/{id}/status`

No delete route exists in the first pass.

---

## Scope Posture

All handoff routes are project-scoped.

Project scope is resolved from the governed session/auth context.
The route must not trust caller-supplied project scope for authorization.

Where a route accepts `projectId` in the body or query for creation/filtering semantics, that value must still be validated against the governed session scope.
A mismatch must fail without cross-project leakage.

---

## Source Entity Rule

`sourceEntityType` and `sourceEntityId` form a polymorphic reference to the planning entity being handed off.

Both must follow `polymorphic-reference-enforcement.md`.

That means:

- allowed source entity types are not free-form; they are governed by `polymorphic-reference-enforcement.md`
- the referenced source entity must exist
- the referenced source entity must belong to the same project scope as the handoff row
- cross-project source references must fail without existence leakage
- the source entity must be resolved before commit

This route family must not redefine allowed source entity types locally.

---

## Target-System Rule

`targetSystem` is required on creation.

It must use the governed target-system vocabulary from `controlled-vocabularies.md`.
Invalid `targetSystem` values must fail with `422 Unprocessable Entity`.

The first-pass canonical target system for handoffs is `v_forge`.
Other target system values may exist in the controlled vocabulary but their meaning is governed by that vocabulary, not expanded here.

---

## Handoff-Type Rule

`handoffType` is required on creation.

It must use the governed handoff-type vocabulary from `controlled-vocabularies.md`.
Invalid `handoffType` values must fail with `422 Unprocessable Entity`.

---

## `completedAt` Rule

`completedAt` is server-owned.

It must not be caller-settable on create, patch, or status-transition routes.
It is set atomically by the server only when the handoff status transitions to `closed`.

For all statuses other than `closed`, `completedAt` must remain `null`.
Supplying `completedAt` where the route contract does not permit it must fail with `400 Bad Request`.

---

## `GET /handoffs`

### Purpose
List handoffs in current project scope.

### Query parameters
Allowed first-pass query parameters:

- `status`
- `targetSystem`
- `handoffType`
- `sourceEntityType`
- `sourceEntityId`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

### Query parameter semantics

#### `status`
- optional
- controlled-vocabulary value from handoff status set
- invalid value -> `422 Unprocessable Entity`

#### `targetSystem`
- optional
- controlled-vocabulary value from handoff target-system set
- invalid value -> `422 Unprocessable Entity`

#### `handoffType`
- optional
- controlled-vocabulary value from handoff-type set
- invalid value -> `422 Unprocessable Entity`

#### `sourceEntityType`
- optional
- controlled by allowed handoff source entity-type set from `polymorphic-reference-enforcement.md`
- invalid value -> `422 Unprocessable Entity`

#### `sourceEntityId`
- optional
- UUID
- malformed UUID -> `400 Bad Request`
- must not be supplied without `sourceEntityType`; if supplied without type -> `400 Bad Request`
- if supplied with `sourceEntityType`, filters handoffs whose source matches that exact resolved entity in current project scope
- if the referenced source entity is not found in current project scope — whether it exists elsewhere or not — the route must return an empty result set without revealing whether the entity exists in another project

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
createdAt desc, id asc
```

This ordering is deterministic and must be the basis for cursor generation for this family.
Handoffs do not have a priority field. `createdAt desc` surfaces the most recently created handoffs first, which is the natural list posture for an operator reviewing transfer history.

### Response shape

```json
{
  "data": [
    {
      "id": "uuid",
      "projectId": "uuid",
      "sourceEntityType": "controlled-value",
      "sourceEntityId": "uuid",
      "targetSystem": "controlled-value",
      "handoffType": "controlled-value",
      "status": "proposed|ready|handed_off|accepted|closed",
      "readinessBasisSummary": "text or null",
      "createdAt": "timestamp",
      "completedAt": "timestamp or null",
      "updatedAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- list responses return canonical handoff fields only
- all filters apply within current project scope only
- a valid filter value that matches no handoffs in current scope returns an empty data array
- filters must not leak whether referenced source entities exist in another project

---

## `GET /handoffs/{id}`

### Purpose
Fetch one handoff by identifier inside current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Behavior
- if handoff exists in current project scope -> return canonical record
- if handoff does not exist in current scope -> `404 Not Found`
- if handoff exists in another project -> route must still preserve non-leakage posture and return `404 Not Found`

### Response shape

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "sourceEntityType": "controlled-value",
  "sourceEntityId": "uuid",
  "targetSystem": "controlled-value",
  "handoffType": "controlled-value",
  "status": "proposed|ready|handed_off|accepted|closed",
  "readinessBasisSummary": "text or null",
  "createdAt": "timestamp",
  "completedAt": "timestamp or null",
  "updatedAt": "timestamp"
}
```

---

## `POST /handoffs`

### Purpose
Create a new handoff record in current project scope.

### Request body

```json
{
  "projectId": "uuid",
  "sourceEntityType": "work_item",
  "sourceEntityId": "uuid",
  "targetSystem": "v_forge",
  "handoffType": "controlled-value",
  "readinessBasisSummary": "Optional summary of readiness basis"
}
```

### Required fields
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `targetSystem`
- `handoffType`

### Optional fields
- `readinessBasisSummary`

### Forbidden fields
The caller must not supply:

- `id`
- `status`
- `completedAt`
- `createdAt`
- `updatedAt`

Supplying forbidden fields must fail with `400 Bad Request`.

### Defaults
- `status = proposed`
- `completedAt = null`

### Validation
- `projectId` must match current governed project scope
- `sourceEntityType` must be an allowed handoff source entity type
- `sourceEntityId` must be a valid UUID
- source entity must resolve inside current project scope
- `targetSystem` must be a valid handoff target-system value
- `handoffType` must be a valid handoff-type value
- `readinessBasisSummary`, if supplied, must be non-empty text

### Response shape
Return `201 Created` with canonical record body.
The response body shape is the same as `GET /handoffs/{id}` for the same record.

### Notes
Creating a handoff record does not activate handoff or transfer execution responsibility.
A handoff record in `proposed` status represents a planning intent that has not yet satisfied readiness, approval, or activation requirements.

---

## `PATCH /handoffs/{id}`

### Purpose
Apply bounded field updates to a handoff.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Allowed fields
- `readinessBasisSummary`

### Forbidden fields
The caller must not patch:

- `id`
- `projectId`
- `sourceEntityType`
- `sourceEntityId`
- `targetSystem`
- `handoffType`
- `status`
- `completedAt`
- `createdAt`
- `updatedAt`

Unknown PATCH fields must fail with `400 Bad Request`.
Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- handoff must exist in current project scope or return `404 Not Found`
- `readinessBasisSummary`, if supplied, must be non-empty text or `null`; supplying an empty string must fail with `422 Unprocessable Entity`

### Response shape
Return canonical handoff record after patch.

### Notes
Identity fields (`sourceEntityType`, `sourceEntityId`, `targetSystem`, `handoffType`) are immutable after creation.
Changing the logical identity of a handoff is not a bounded patch operation.
Status changes happen only through the dedicated status route.

---

## `POST /handoffs/{id}/status`

### Purpose
Apply a governed status transition to a handoff.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Request body

```json
{
  "newStatus": "ready",
  "reason": "Required for certain transitions"
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
- `completedAt`
- any canonical handoff fields outside this transition contract

Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- handoff must exist in current project scope or return `404 Not Found`
- `newStatus` must be a valid handoff status value
- transition must be legal according to `status-transitions.md`
- if the transition requires a reason, `reason` must be non-empty
- if the handoff is already in `newStatus`, fail with `422 Unprocessable Entity`

### Atomicity rules

#### `StatusHistory` rule
All handoff status transitions must write a `StatusHistory` row in the same transaction.
The `actor` value must be server-resolved from the authenticated request context.
`StatusHistory.entityType` must be `handoff`.

#### `completedAt` rule
When the status transitions to `closed`, `completedAt` must be set to `now()` in the same transaction.
For all other transitions, `completedAt` must not be modified.

These are not optional behaviors. Partial writes for any governed handoff transition are correctness violations.

### Response shape
Return canonical handoff record after transition.

---

## Status Transition Posture

Handoff status values are governed by `controlled-vocabularies.md`.
Legal transition paths and their reason requirements are governed by `status-transitions.md`.

The forward path is:

```
proposed → ready → handed_off → accepted → closed
```

Allowed direct-closure transitions with explicit reason:
- `proposed → closed`
- `ready → closed`
- `handed_off → closed`

Allowed reverse re-entry transitions with explicit reason:
- `handed_off → ready`
- `handed_off → proposed`

Once a handoff reaches `accepted` or `closed`, no reverse transition is allowed in the first pass.

This route family must not redefine handoff lifecycle locally.
If the handoff lifecycle changes, update the shared status-transition authority first.

### Reverse re-entry posture

Reverse transitions from `handed_off` are orchestration-side reconsideration decisions.
They must leave recoverable status history.
They do not model V Forge internal execution lifecycle or rejection semantics.
A reverse re-entry transition records that Project V reconsidered or recalled the transfer; it does not represent a V Forge execution state.

---

## Relationship to Readiness

A handoff record may reference a readiness basis through `readinessBasisSummary`.

This field is Project V's planning-side record of why the handoff was judged ready.
It is not a live readiness evaluation result.
It is not replaced by or synchronized with `ReadinessEvaluation` records automatically.

If the operator wants to associate specific readiness evaluations with a handoff, that association belongs in the `EvidenceLink` family or through explicit planning decisions, not through hidden coupling between this route family and the readiness route family.

---

## Relationship to Return-to-Planning

When V Forge execution findings require planning reconsideration, that return occurs through the interface defined in `../../interfaces/v-forge-to-project-v-return-to-planning-interface.md`.

This route family does not own return-to-planning semantics.

However, when a return-to-planning event causes planning reconsideration that ends the original handoff's active transfer, the handoff status route is the correct mechanism for recording the resulting planning-side state change.

Specifically:
- if the handoff is in `handed_off` status and return inputs require it to return to planning reconsideration, the `handed_off → ready` or `handed_off → proposed` transitions (with explicit reason) are the governed mechanism
- the reason field must record why the handoff is being recalled or reconsidered at the planning level

The handoff record preserves a recoverable trace of the recall. It does not directly encode V Forge execution findings. Those findings are returned through the interface layer.

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
- `sourceEntityId` supplied without `sourceEntityType`

### `422 Unprocessable Entity`
Use for:

- invalid controlled-vocabulary values for `status`, `targetSystem`, `handoffType`, `sourceEntityType`
- illegal status transition
- missing required reason for a governed transition
- invalid polymorphic reference shape when the request is otherwise well-formed
- cross-project polymorphic source-entity rejection without existence leakage
- empty string supplied as `readinessBasisSummary`

### `404 Not Found`
Use for:

- handoff not found in current project scope
- handoff existing in another project but outside current scope

---

## Non-Leakage Rule

Handoff routes must not leak whether a handoff or a referenced source entity exists in another project.

A caller attempting to fetch, patch, or transition a handoff outside current project scope must receive the same `404 Not Found` posture as for a genuinely absent handoff.

Source-entity list filters must return empty results rather than revealing whether a referenced entity exists elsewhere.

Error body shape must not reveal whether the target exists elsewhere.

---

## Invariants

The following invariants must hold across all handoff route behavior:

1. A handoff record in any status other than `closed` must have `completedAt = null`.
2. A handoff record in `closed` status must have a non-null `completedAt`.
3. Every handoff status transition must produce exactly one `StatusHistory` row in the same transaction.
4. `sourceEntityType` and `sourceEntityId` must not change after creation.
5. `targetSystem` and `handoffType` must not change after creation.
6. Source entity must resolve inside current project scope at creation time.
7. A caller-supplied `completedAt` must always fail with `400 Bad Request`.
8. No forbidden transition may succeed; any attempt must fail with `422 Unprocessable Entity`.
9. A transition into an already-held status must fail with `422 Unprocessable Entity`.
10. A reverse re-entry transition must require a non-empty reason; a missing or empty reason must fail with `400 Bad Request`.

---

## Hammer Expectations

The hammer suite for handoffs should verify at minimum:

- handoff creation with valid input
- malformed UUID rejection with `400`
- unknown query parameter rejection with `400`
- unknown PATCH field rejection with `400`
- forbidden field rejection on create, patch, and status routes
- caller-supplied `completedAt` rejection with `400`
- deterministic list ordering
- cursor continuation correctness
- source-entity filter non-leakage in list behavior
- same-project source-entity validation on create
- invalid `targetSystem` rejection with `422`
- invalid `handoffType` rejection with `422`
- empty `readinessBasisSummary` rejection with `422`
- illegal status transition rejection with `422`
- required-reason transition rejection with `400`
- already-in-status rejection with `422`
- `completedAt` null for all non-closed statuses
- `completedAt` non-null atomicity on transition to `closed`
- status transition + history atomicity
- reverse re-entry transition requires explicit reason
- `accepted` and `closed` are terminal: no reverse transitions allowed
- cross-project fetch/patch/status non-leakage

---

## Final Rule

Handoff records are Project V's planning-side record of bounded execution-responsibility transfer.

They must remain explicit, lifecycle-governed, and ownership-honest.

If handoff routes begin absorbing V Forge execution state, encoding execution findings directly, or treating a prepared handoff as an active transfer, the family has drifted from its planning-truth role.

---

## Human-In-The-Loop Principle

Handoff lifecycle transitions are governance-sensitive because they determine when execution responsibility actually transfers.

Operators and bounded LLMs must be able to trust that:

- list behavior is deterministic
- source-entity references are same-project validated
- status changes follow one governed path
- reverse re-entry requires explicit reason and leaves traceable history
- `completedAt` is server-owned and atomically tied to `closed` status
- cross-project visibility is not accidentally leaked
- a handoff record in `proposed` status does not mean execution has begun

The API family must preserve that trust structurally.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- handoff routes are project-scoped and non-leaky
- creating a handoff record in `proposed` status does not transfer execution responsibility
- `PATCH` is only for bounded updates to `readinessBasisSummary`
- status changes require the dedicated status route
- `targetSystem`, `handoffType`, and `sourceEntityType` are controlled values
- source entity references are governed polymorphic pairs, not free-form fields
- `completedAt` is server-owned and must only be set at the `closed` transition
- `accepted` and `closed` are terminal statuses with no reverse transitions
- `handed_off` supports reverse re-entry transitions with explicit reason
- unknown fields and unknown query params are rejected, not ignored
- `404` does not imply the target never existed anywhere
- handoff lifecycle is governed by shared transition authority, not local route improvisation
- this family records planning-side transfer state; it does not own V Forge execution truth

If implementation makes handoff behavior more permissive, treats preparation as activation, or allows `completedAt` to be caller-set, the contract is being violated.

---

## Usage

This document should be used:

- when implementing handoff routes
- when writing migrations or tests that depend on handoff API behavior
- when writing hammer coverage for handoff routes
- when reviewing whether handoff behavior remains within bounded planning truth
- when checking whether a proposed handoff state change is governed by shared transition authority

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
- `../polymorphic-reference-enforcement.md`
- `../v-forge-integration.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../../workflows/handoff-workflow.md`
- `../../governance/approval-and-escalation-model.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../ecosystem/vocabulary.md`
