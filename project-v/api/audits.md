# Audits API Family

## Purpose

This document defines the first-pass API contract family for Project V audit evaluations and audit gaps.

It exists to answer:

```text
What routes exist for audit runs and audit gaps, what do they accept, what do they return, what validations and ownership rules apply, and how do these records behave as server-governed BYDA audit assessments?
```

Read this with:

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../polymorphic-reference-enforcement.md`
- `../audit-evaluation-rules.md`
- `../multi-project-doctrine.md`
- `../status-transitions.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the audit run route family
- the audit gap sub-family
- request and response shape for first-pass audit routes
- audit initiation posture and server-owned audit behavior
- polymorphic entity targeting posture
- server-owned vs caller-supplied field posture
- applicability validation posture
- atomicity rules for audit run creation and gap creation
- staleness invalidation route posture
- immutability posture for audit run records after creation
- bounded mutability posture for audit gaps
- list ordering and filtering posture
- validation, error, and non-leakage posture for audit routes

---

## Out of Scope

This document does not define:

- the BYDA philosophy or ownership model (see `../byda-in-project-v.md`)
- the exact rule logic for each audit type (see `../audit-evaluation-rules.md`)
- the readiness route family (readiness and audit are separate; see `readiness.md`)
- schema migration sequencing
- audit UI rendering behavior

---

## System

- project-v

---

## Core Rule

Audit runs are server-governed BYDA assessments.

The server initiates, executes, and owns the audit result.
Callers do not supply results, summaries, or gaps directly.
Callers initiate an audit by supplying the audit type, the target entity (or project scope), and any allowed optional inputs.

Audit routes must preserve all of the following:

- explicit project scope
- deterministic ordering
- server-owned result production
- governed applicability checking before evaluation runs
- same-project polymorphic entity validation
- non-leaky cross-project rejection
- immutability of audit run records after creation
- bounded gap mutability only

Audit routes must not act like free-form scoring surfaces or general-purpose annotation storage.

---

## How Audits Differ from Readiness Evaluations

Audit runs and readiness evaluations are related but structurally separate.

Key differences that affect the API family:

- **Initiation framing**: both are server-governed, but audit runs include an explicit applicability gate (Step 2 in `audit-evaluation-rules.md`) that readiness evaluations do not. An applicability failure for an audit returns `422 Unprocessable Entity` before any evaluation logic runs.
- **Result posture**: audit results are `pass`, `fail`, `warning`, or `stale`. Readiness results are `ready`, `not_ready`, `ready_with_warnings`, or `deferred`. These are different controlled vocabularies.
- **Target scope**: audit runs may target `project` as an entity type. Readiness evaluations do not.
- **Staleness**: audit runs have a governed staleness invalidation route that produces a `StatusHistory` row. Readiness evaluations do not expose a staleness mutation path; they are simply superseded by a new evaluation.
- **Gap posture**: both have gap sub-families with similar bounded mutability, but they are separate record families and must not be conflated.
- **No `deferWithReason`**: audit runs do not support a caller-initiated defer mechanism. `stale` is a post-run invalidation state, not a pre-run deferral. There is no audit-side equivalent to the readiness `deferred` result path.

---

## What an Audit Run Is

An `AuditRun` record in Project V is the server-produced output of a governed BYDA audit of a planning entity or project scope.

It records:

- the audit type applied
- the target entity (polymorphic, or project-scoped where no target entity applies)
- the result produced by the server
- a server-generated summary of the audit basis
- when the audit started and completed

An audit run does not record execution state.
An audit run does not record V Forge outputs.
An audit run is Project V's owned, inspectable planning-quality assessment.

---

## What an Audit Gap Is

An `AuditGap` record is an explicit audit deficiency, contradiction, or ambiguity finding identified during an audit run.

It records:

- the audit run it belongs to
- the severity of the finding
- a description of the finding
- optional remediation guidance
- the status of the gap (`open`, `resolved`, or `invalidated`)

Gaps are created atomically as part of audit run creation.
They are not created independently of an audit run.
They may be updated in bounded ways after the audit is created.

Audit gaps and readiness gaps are separate record families. They must not be silently conflated. See `audit-evaluation-rules.md`.

---

## Canonical Record Basis

### AuditRun

Canonical fields governed by `schema-specification.md`:

- `id`
- `projectId`
- `auditType`
- `targetEntityType`
- `targetEntityId`
- `result`
- `summary`
- `startedAt`
- `completedAt`
- `createdAt`

### AuditGap

Canonical fields governed by `schema-specification.md`:

- `id`
- `projectId`
- `auditRunId`
- `severity`
- `description`
- `remediation`
- `status`
- `createdAt`
- `updatedAt`

Neither record family may introduce shadow fields outside the governed schema.

---

## Route Family

First-pass audit routes:

- `POST /audit-runs`
- `GET /audit-runs`
- `GET /audit-runs/{id}`
- `POST /audit-runs/{id}/stale`
- `GET /audit-runs/{id}/gaps`
- `PATCH /audit-runs/{id}/gaps/{gapId}`

No delete route exists for either record in the first pass.
No direct gap-creation route exists; gaps are created only as part of audit run creation.

---

## Scope Posture

All audit routes are project-scoped.

Project scope is resolved from the governed session/auth context.
The route must not trust caller-supplied project scope for authorization.

Where a route accepts `projectId` in the body or query for creation/filtering semantics, that value must still be validated against the governed session scope.
A mismatch must fail without cross-project leakage.

---

## Polymorphic Entity Rule

`targetEntityType` and `targetEntityId` form an optional polymorphic reference to the planning entity being audited.

Where supplied, both must follow `polymorphic-reference-enforcement.md`.

That means:

- allowed entity types are not free-form; they are governed by the Audit Run target entity-type vocabulary in `controlled-vocabularies.md`
- the referenced entity must exist
- the referenced entity must belong to the same project scope as the audit run
- cross-project entity references must fail without existence leakage
- the entity must be resolved before the audit begins

Allowed audit run target entity types, first pass:
- `project`
- `objective`
- `initiative`
- `work_item`
- `handoff`

Not every `auditType` is valid for every `targetEntityType`. Applicability is governed by `audit-evaluation-rules.md`. An applicability mismatch must fail with `422 Unprocessable Entity`.

### Project-target special case

When `targetEntityType = 'project'`, the same-project ownership check uses:

```text
AuditRun.projectId == targetEntityId
```

This is the `AuditRun.targetEntityType = 'project'` special case defined in `polymorphic-reference-enforcement.md`. The central resolver must handle it explicitly.

### Omitted target entity

`targetEntityType` and `targetEntityId` are optional as a pair. Some audit types may operate at project scope without a more specific entity target. If one is supplied without the other, the request must fail with `400 Bad Request`.

---

## Server-Owned Fields

The following fields are server-owned and must not be caller-settable:

- `id`
- `result`
- `summary`
- `startedAt`
- `completedAt`
- `createdAt`
- `projectId` (resolved from session context, not trusted from body)
- all `AuditGap` fields except `status` and `remediation` via the bounded PATCH route

Supplying a server-owned field in a creation request must fail with `400 Bad Request`.

`result` is the output of server-side audit evaluation logic governed by `audit-evaluation-rules.md`. Callers may not supply or override it.

`summary` is server-generated as part of audit execution. Callers may not supply it. The server must produce a non-empty summary as part of any audit it persists; an audit run must not be stored without one.

`startedAt` and `completedAt` are set by the server as part of execution lifecycle management. They must not be caller-settable on create or any mutation route. Both are set during evaluation execution and persisted as part of the single atomic creation write; they are not set in a separate subsequent update.

---

## Caller-Supplied Inputs on Creation

On audit creation, callers supply:

### `auditType`
Required. Must be a valid audit type from `controlled-vocabularies.md`.
Invalid value fails with `422 Unprocessable Entity`.

### `targetEntityType` + `targetEntityId`
Optional pair. Both must be supplied together or neither must be supplied.
If supplied, must pass polymorphic reference validation and applicability check.
Supplying one without the other fails with `400 Bad Request`.

### `projectId`
Required in the request body for creation scope clarity, but must be validated against governed session context. A mismatch fails without leakage.

---

## `POST /audit-runs`

### Purpose
Initiate a server-governed audit run for a planning entity or project scope.

### Request body

```json
{
  "projectId": "uuid",
  "auditType": "planning",
  "targetEntityType": "initiative",
  "targetEntityId": "uuid"
}
```

### Required fields
- `projectId`
- `auditType`

### Optional fields
- `targetEntityType`
- `targetEntityId`

### Forbidden fields
The caller must not supply:

- `id`
- `result`
- `summary`
- `startedAt`
- `completedAt`
- `createdAt`

Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- `projectId` must match current governed project scope
- `auditType` must be a valid audit type value
- if `targetEntityType` is supplied, `targetEntityId` must also be supplied and vice versa
- if both target fields are supplied, `targetEntityType` must be a valid audit target entity type
- `targetEntityId` must be a valid UUID where supplied
- referenced entity must resolve inside current project scope where supplied
- `auditType` must be applicable to `targetEntityType` per `audit-evaluation-rules.md`; applicability failure -> `422 Unprocessable Entity`

### Execution behavior
Once validation succeeds, the server:

1. Sets `startedAt`
2. Validates audit applicability for the audit type and target entity type combination
3. Executes the evaluation rules in the order governed by `audit-evaluation-rules.md`
4. Determines `result` from evaluation output
5. Generates `summary` from the audit basis
6. Sets `completedAt`
7. Creates the `AuditRun` record (including `startedAt` and `completedAt` set above) atomically with gap creation
8. Creates all associated `AuditGap` records atomically in the same transaction

All of steps 7 and 8 must succeed atomically or neither must be committed.
Partial audit writes are correctness violations.

Note: unlike readiness evaluations, audit runs do not synchronize any summary field on the evaluated entity. Planning entities do not have a server-managed `auditState` field analogous to `WorkItem.readinessState`.

### Response shape
Return `201 Created` with canonical audit run record body.

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "auditType": "planning",
  "targetEntityType": "initiative",
  "targetEntityId": "uuid",
  "result": "pass",
  "summary": "server-generated audit summary",
  "startedAt": "timestamp",
  "completedAt": "timestamp",
  "createdAt": "timestamp"
}
```

The response does not include gaps inline. Gaps are retrievable through `GET /audit-runs/{id}/gaps`.

---

## `GET /audit-runs`

### Purpose
List audit runs in current project scope.

### Query parameters
Allowed first-pass query parameters:

- `auditType`
- `targetEntityType`
- `targetEntityId`
- `result`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

### Query parameter semantics

#### `auditType`
- optional
- controlled-vocabulary value from audit type set
- invalid value -> `422 Unprocessable Entity`

#### `targetEntityType`
- optional
- controlled-vocabulary value from audit run target entity-type set
- invalid value -> `422 Unprocessable Entity`

#### `targetEntityId`
- optional
- UUID
- malformed UUID -> `400 Bad Request`
- must not be supplied without `targetEntityType`; supplying without type -> `400 Bad Request`
- if supplied with `targetEntityType`, filters audit runs for that exact resolved entity in current project scope
- if the referenced entity is not found in current project scope — whether it exists elsewhere or not — the route must return an empty result set without revealing whether the entity exists in another project

#### `result`
- optional
- controlled-vocabulary value from audit result set
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
`targetEntityId` must not be supplied without `targetEntityType`.
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
      "auditType": "controlled-value",
      "targetEntityType": "controlled-value or null",
      "targetEntityId": "uuid or null",
      "result": "controlled-value",
      "summary": "text",
      "startedAt": "timestamp or null",
      "completedAt": "timestamp or null",
      "createdAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- list responses return canonical audit run fields only
- gaps are not included in list responses
- all filters apply within current project scope only
- a valid filter that matches no audit runs in current scope returns an empty data array
- filters must not leak whether referenced entities exist in another project

---

## `GET /audit-runs/{id}`

### Purpose
Fetch one audit run by identifier inside current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Behavior
- if audit run exists in current project scope -> return canonical record
- if audit run does not exist in current scope -> `404 Not Found`
- if audit run exists in another project -> route must preserve non-leakage posture and return `404 Not Found`

### Response shape

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "auditType": "controlled-value",
  "targetEntityType": "controlled-value or null",
  "targetEntityId": "uuid or null",
  "result": "controlled-value",
  "summary": "text",
  "startedAt": "timestamp or null",
  "completedAt": "timestamp or null",
  "createdAt": "timestamp"
}
```

Gaps are not returned inline. Use the gaps sub-route.

---

## `POST /audit-runs/{id}/stale`

### Purpose
Mark a previously completed audit run as `stale` when its original basis has been materially invalidated.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Request body

```json
{
  "reason": "Required non-empty reason for staleness"
}
```

### Required fields
- `reason`

### Forbidden fields
The caller must not supply:

- `result`
- `summary`
- any canonical audit run fields outside this staleness contract

Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- audit run must exist in current project scope or return `404 Not Found`
- `reason` must be non-empty; missing or empty -> `400 Bad Request`
- current `result` must be `pass`, `fail`, or `warning`; attempting to mark an already-stale audit as stale must fail with `422 Unprocessable Entity`

Allowed result transitions into `stale` are governed by `status-transitions.md` under Audit Run Result Transitions: `pass → stale`, `fail → stale`, and `warning → stale` are allowed. `stale → stale` is forbidden and must fail with `422 Unprocessable Entity`.

### Execution behavior
When the staleness route succeeds, the server:

1. Updates `AuditRun.result` to `stale`
2. Updates `AuditRun.summary` to reflect the staleness reason alongside the prior summary basis
3. Writes a `StatusHistory` row atomically in the same transaction; `StatusHistory.entityType` must be `audit_run`

`AuditRun.result` and `AuditRun.summary` are the only fields on `AuditRun` that may be mutated after creation, and only through this governed staleness route.

This is the bounded governed update of `result` and `summary` described in `schema-specification.md` under `AuditRun` allowed mutations.

### Response shape
Return canonical audit run record after staleness transition.

### Atomicity rule
The `result` update, `summary` update, and `StatusHistory` write must be committed in a single transaction.
`StatusHistory.entityType` must be `audit_run`.
`StatusHistory.actor` must be server-resolved from the authenticated request context.
Partial writes are correctness violations.

---

## `GET /audit-runs/{id}/gaps`

### Purpose
List the audit gaps associated with a specific audit run in current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`
- the parent audit run must exist in current project scope or return `404 Not Found`

### Query parameters
Allowed first-pass query parameters:

- `status`
- `severity`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

#### `status`
- optional
- controlled-vocabulary value from audit gap status set (`open`, `resolved`, `invalidated`)
- invalid value -> `422 Unprocessable Entity`

#### `severity`
- optional
- controlled-vocabulary value from audit gap severity set
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

### Ordering
Default and required ordering:

```text
severity rank desc, createdAt asc, id asc
```

Severity rank is numeric, not lexical. Canonical rank: `critical` = 4, `major` = 3, `minor` = 2, `advisory` = 1.
Raw text ordering on severity is incorrect and must not be used.

This ordering is deterministic and must be the basis for cursor generation for this sub-family.

### Response shape

```json
{
  "data": [
    {
      "id": "uuid",
      "projectId": "uuid",
      "auditRunId": "uuid",
      "severity": "controlled-value",
      "description": "text",
      "remediation": "text or null",
      "status": "open|resolved|invalidated",
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- this sub-route uses the standard list envelope and cursor pagination rules from `api-conventions.md`
- an audit run with no gaps returns an empty data array, not a `404`
- gaps are always scoped to the parent audit run
- the parent audit run must be in current project scope; otherwise `404 Not Found`
- gaps may be updated through the PATCH route regardless of whether the parent audit run is `stale`; the stale status of the parent run does not block gap mutation in the first pass

---

## `PATCH /audit-runs/{id}/gaps/{gapId}`

### Purpose
Apply bounded updates to an audit gap.

### Path parameters
- `id` must be a valid UUID (parent audit run id)
- `gapId` must be a valid UUID
- malformed UUID for either -> `400 Bad Request`
- the parent audit run must exist in current project scope or return `404 Not Found`
- the gap must belong to that audit run or return `404 Not Found`

### Allowed fields
- `status`
- `remediation`

### Forbidden fields
The caller must not patch:

- `id`
- `projectId`
- `auditRunId`
- `severity`
- `description`
- `createdAt`
- `updatedAt`

Unknown PATCH fields must fail with `400 Bad Request`.
Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- `status`, if supplied, must be a valid audit gap status value; invalid value -> `422 Unprocessable Entity`
- illegal status transition must fail with `422 Unprocessable Entity`
- `remediation`, if supplied, may be `null` or non-empty text
- supplying an empty string for `remediation` must fail with `422 Unprocessable Entity`

### Status transition posture for audit gaps

Audit gap status does not use the governed transition route from `status-transitions.md` — it is a bounded field on the gap record, not a lifecycle-governed entity with a `StatusHistory` requirement. The PATCH route handles it directly.

Legal first-pass moves for audit gap `status` field:

- `open → resolved`
- `open → invalidated` (allowed with rationale; `remediation` should capture the invalidation basis)
- `resolved → invalidated`

The following are not allowed and must fail with `422 Unprocessable Entity`:

- `invalidated → open`
- `invalidated → resolved`

This matches the transition constraints in `status-transitions.md` under Audit Gap Status Transitions, but is enforced through the bounded PATCH route rather than a dedicated status endpoint.

### Response shape
Return canonical gap record after patch.

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "auditRunId": "uuid",
  "severity": "controlled-value",
  "description": "text",
  "remediation": "text or null",
  "status": "open|resolved|invalidated",
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

### Notes
`severity` and `description` are immutable after gap creation.
They are evaluation outputs, not caller-adjustable classifications.

---

## Immutability Rule

`AuditRun` records are immutable after creation except through the governed staleness route.

The only post-creation mutations allowed on `AuditRun` are:

- `result` → `stale` via `POST /audit-runs/{id}/stale`
- `summary` updated to reflect staleness reason, via the same route

No other fields on `AuditRun` may be mutated through any API path.

The append-mostly posture of audit runs means a new audit run must be initiated to supersede a prior result for any reason other than staleness marking. The prior audit run remains in history.

---

## Atomicity Rules

### Audit run creation atomicity
The following must be committed in a single transaction when audit creation succeeds:

1. The `AuditRun` row, including `startedAt` and `completedAt` values set during evaluation execution
2. All associated `AuditGap` rows

`startedAt` and `completedAt` are not set in a separate post-creation update; they are part of the same atomic write.
Partial writes are correctness violations. If gap creation fails, the entire creation must be rolled back.

### Staleness transition atomicity
The following must be committed in a single transaction when staleness succeeds:

1. `AuditRun.result` updated to `stale`
2. `AuditRun.summary` updated with staleness basis
3. `StatusHistory` row written with `entityType = 'audit_run'` and server-resolved `actor`

Partial writes for the staleness transition are correctness violations.

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
- `targetEntityId` supplied without `targetEntityType`
- `targetEntityType` supplied without `targetEntityId`
- missing or empty `reason` on the staleness route

### `422 Unprocessable Entity`
Use for:

- invalid controlled-vocabulary values for `auditType`, `result`, `severity`, `status`
- audit type not applicable to target entity type
- cross-project polymorphic entity rejection without existence leakage
- invalid polymorphic entity reference shape when the request is otherwise well-formed
- already-stale audit run marked stale again
- illegal audit gap status transition
- empty string supplied as `remediation`

### `404 Not Found`
Use for:

- audit run not found in current project scope
- audit run existing in another project but outside current scope
- gap not found under the specified parent audit run in current project scope

---

## Non-Leakage Rule

Audit routes must not leak whether an audited entity or an audit run exists in another project.

Filtering by `targetEntityId` without a match in current scope must return an empty result set, not a cross-project disclosure.

Fetching an audit run or gap outside current project scope must return `404 Not Found`.

Error body shape must not reveal whether the target exists elsewhere.

---

## Invariants

### Audit run invariants

1. `result` is always server-owned and never caller-settable on creation.
2. `summary` is always server-generated and non-empty on every persisted audit run.
3. All gaps associated with an audit run are created in the same transaction as the audit run.
4. `startedAt` and `completedAt` are server-set as part of the creation transaction and never caller-settable.
5. The only post-creation mutations to an `AuditRun` are `result → stale` and corresponding `summary` update, via the governed staleness route only.
6. Staleness transition must write a `StatusHistory` row in the same transaction; `StatusHistory.entityType` must be `audit_run`.
7. A caller-supplied `result` or `summary` must always fail with `400 Bad Request`.
8. An audit run existing in another project must return `404 Not Found`, not a cross-project disclosure.
9. Applicability mismatch between `auditType` and `targetEntityType` must fail with `422 Unprocessable Entity` before any evaluation runs.

### Audit gap invariants

10. `severity` and `description` on a gap are immutable after gap creation.
11. `invalidated` is a terminal gap status; no transition out of `invalidated` is allowed.
12. Gap `status` and `remediation` are the only mutable fields on an audit gap after creation.
13. Gaps are created only as part of audit run creation; no independent gap-creation route exists.
14. Gap updates are not blocked by the parent audit run's `stale` status in the first pass.

---

## Hammer Expectations

The hammer suite for audit runs and gaps should verify at minimum:

- audit creation with valid input for each supported entity type
- audit creation with no target entity (project-scoped)
- malformed UUID rejection with `400`
- unknown query parameter rejection with `400`
- forbidden field rejection on audit creation
- caller-supplied `result` rejection with `400`
- caller-supplied `summary` rejection with `400`
- caller-supplied `startedAt` or `completedAt` rejection with `400`
- `targetEntityId` without `targetEntityType` rejection with `400`
- `targetEntityType` without `targetEntityId` rejection with `400`
- invalid `auditType` rejection with `422`
- audit type / target entity type applicability mismatch rejection with `422`
- cross-project entity reference rejection without leakage
- entity not-found-in-scope returns empty list, not cross-project disclosure
- deterministic list ordering for audit runs and gaps
- cursor continuation correctness on both audit run list and gap list
- audit run immutability: no mutation path outside staleness route
- gap creation atomicity with parent audit run
- `startedAt` and `completedAt` set atomically in creation transaction
- staleness route: `reason` required
- staleness route: already-stale rejection with `422`
- staleness route atomicity: `result`, `summary`, and `StatusHistory` in one transaction
- staleness `StatusHistory` row has `entityType = 'audit_run'`
- audit run not stale-able from non-terminal prior result (valid: `pass`, `fail`, `warning` → `stale`)
- gap `severity` and `description` immutability after creation
- gap `status` and `remediation` patchable
- illegal gap status transition rejection with `422`
- `invalidated` terminal: no transition out
- empty `remediation` rejection with `422`
- unknown PATCH field rejection with `400` on gap route
- forbidden gap field rejection with `400`
- gap PATCH succeeds on a stale parent audit run
- cross-project audit run fetch non-leakage

---

## Final Rule

Audit runs are BYDA planning-quality assessments governed by explicit rules.

Their API family must remain server-governed, applicability-checked, and bounded in its mutation surface.

If audit routes begin accepting caller-supplied results, allow gap severity mutation, or skip the applicability gate, the family has broken its core posture.

Audit gaps and readiness gaps are structurally separate. They must never be silently merged or cross-queried as though they belong to the same family.

---

## Human-In-The-Loop Principle

Audit results are governance-sensitive because they constrain planning progression and handoff eligibility through their coupling to readiness.

Operators and bounded LLMs must be able to trust that:

- audit results are server-produced and not caller-manipulated
- gap severity and description cannot be retroactively adjusted
- a new audit run is required to produce a new result, except for staleness marking
- the staleness route preserves a traceable `StatusHistory` row with `entityType = 'audit_run'` rather than silently overwriting prior confidence
- cross-project entity information is not leaked through filter behavior

The API family must preserve that trust structurally.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- audit creation is an initiation request, not a data-insert request
- the server owns `result`, `summary`, `startedAt`, `completedAt`, and gap content
- the caller supplies what to audit and any allowed optional inputs only
- applicability validation happens before any evaluation logic runs
- audit runs are immutable after creation except through the governed staleness route
- `stale` is not a first-run result; it is a post-creation invalidation state
- the staleness route requires a non-empty reason and produces a `StatusHistory` row with `entityType = 'audit_run'`
- gaps are created atomically with the audit run and are not independently creatable
- gap `severity` and `description` cannot be changed; `status` and `remediation` can
- `invalidated` is a terminal gap status
- gap updates are not blocked by the parent run's `stale` status
- audit gaps and readiness gaps are separate record families
- unlike readiness evaluations, audit runs do not synchronize any summary state field on the evaluated entity
- `targetEntityId` filtering requires paired `targetEntityType` and must not leak cross-project entity existence

If implementation allows callers to set `result`, skips applicability checking, omits the `StatusHistory` row on staleness, or treats audit gaps as equivalent to readiness gaps, the contract is being violated.

---

## Usage

This document should be used:

- when implementing audit run and gap routes
- when writing migrations or tests that depend on audit API behavior
- when writing hammer coverage for audit routes
- when reviewing whether audit behavior remains server-governed and ownership-honest
- when checking whether staleness handling preserves required history and atomicity

---

## Related Docs

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../polymorphic-reference-enforcement.md`
- `../audit-evaluation-rules.md`
- `../byda-in-project-v.md`
- `../multi-project-doctrine.md`
- `../system-invariants.md`
- `../mcp-surface.md`
- `../schema-governance.md`
- `../status-transitions.md`
- `readiness.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../ecosystem/vocabulary.md`
