# Readiness API Family

## Purpose

This document defines the first-pass API contract family for Project V readiness evaluations and readiness gaps.

It exists to answer:

```text
What routes exist for readiness evaluations and readiness gaps, what do they accept, what do they return, what validations and ownership rules apply, and how do these records behave as server-governed planning-quality assessments?
```

Read this with:

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../polymorphic-reference-enforcement.md`
- `../readiness-evaluation-rules.md`
- `../readiness-methodology.md`
- `../multi-project-doctrine.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the readiness evaluation route family
- the readiness gap sub-family
- request and response shape for first-pass readiness routes
- evaluation initiation posture and server-owned evaluation behavior
- polymorphic entity targeting posture
- server-owned vs caller-supplied field posture
- rule-package selection and override posture
- defer-with-reason posture
- atomicity rules for evaluation creation and gap creation
- `WorkItem.readinessState` synchronization rules
- invalidation-boundary posture for `WorkItem.readinessState`
- immutability posture for evaluation records after creation
- bounded mutability posture for readiness gaps
- list ordering and filtering posture
- validation, error, and non-leakage posture for readiness routes

---

## Out of Scope

This document does not define:

- the readiness evaluation methodology or dimension coverage (see `../readiness-methodology.md`)
- the exact rule logic for producing results (see `../readiness-evaluation-rules.md`)
- audit route families (readiness and audit are separate; see the audit API family doc)
- schema migration sequencing
- readiness UI rendering behavior
- work-item routes beyond the synchronization rule
- the governed invalidation mechanism that can reset `WorkItem.readinessState` to `unevaluated`

---

## System

- project-v

---

## Core Rule

Readiness evaluations are server-governed planning-quality assessments.

The server initiates, executes, and owns the evaluation result.
Callers do not supply results, summaries, or gaps directly.
Callers initiate evaluation by supplying the entity to evaluate and any allowed optional inputs.

Readiness evaluation routes must preserve all of the following:

- explicit project scope
- deterministic ordering
- server-owned result production
- same-project polymorphic entity validation
- non-leaky cross-project rejection
- immutability of evaluation records after creation
- bounded gap mutability only

Readiness routes must not act like free-form planning-state storage or general-purpose scoring surfaces.

---

## What a Readiness Evaluation Is

A `ReadinessEvaluation` record in Project V is the server-produced output of a governed evaluation of a planning entity.

It records:

- the entity evaluated (polymorphic: type and id)
- the evaluation type applied
- the rule package used
- the result produced by the server
- a server-generated summary of the evaluation basis
- when the evaluation was created

A readiness evaluation does not record execution state.
A readiness evaluation does not record V Forge outputs.
A readiness evaluation is Project V's owned, inspectable judgment of whether a planning record can legitimately move to the next planning or orchestration stage.

---

## What a Readiness Gap Is

A `ReadinessGap` record is an explicit deficiency or blocker identified during a readiness evaluation.

It records:

- the evaluation it belongs to
- the severity of the deficiency
- a description of the deficiency
- optional remediation guidance
- whether the gap has been resolved

Gaps are created atomically as part of evaluation creation.
They are not created independently of an evaluation.
They may be updated in bounded ways after the evaluation is created.

---

## Canonical Record Basis

### ReadinessEvaluation

Canonical fields governed by `schema-specification.md`:

- `id`
- `projectId`
- `entityType`
- `entityId`
- `evaluationType`
- `result`
- `rulePackage`
- `summary`
- `createdAt`

### ReadinessGap

Canonical fields governed by `schema-specification.md`:

- `id`
- `projectId`
- `readinessEvaluationId`
- `severity`
- `description`
- `remediationSuggestion`
- `resolved`
- `createdAt`
- `updatedAt`

Neither record family may introduce shadow fields outside the governed schema.

---

## Route Family

First-pass readiness routes:

- `POST /readiness-evaluations`
- `GET /readiness-evaluations`
- `GET /readiness-evaluations/{id}`
- `GET /readiness-evaluations/{id}/gaps`
- `PATCH /readiness-evaluations/{id}/gaps/{gapId}`

No status-transition route exists for readiness evaluations.
No delete route exists for either record in the first pass.
No direct gap-creation route exists; gaps are created only as part of evaluation creation.

---

## Scope Posture

All readiness routes are project-scoped.

Project scope is resolved from the governed session/auth context.
The route must not trust caller-supplied project scope for authorization.

Where a route accepts `projectId` in the body or query for creation/filtering semantics, that value must still be validated against the governed session scope.
A mismatch must fail without cross-project leakage.

---

## Polymorphic Entity Rule

`entityType` and `entityId` form a polymorphic reference to the planning entity being evaluated.

Both must follow `polymorphic-reference-enforcement.md`.

That means:

- allowed entity types are not free-form; they are governed by the Readiness Entity Type vocabulary in `controlled-vocabularies.md`
- the referenced entity must exist
- the referenced entity must belong to the same project scope as the evaluation
- cross-project entity references must fail without existence leakage
- the entity must be resolved before evaluation begins

Allowed readiness entity types, first pass:
- `objective`
- `initiative`
- `work_item`
- `handoff`

This route family must not expand the allowed type set locally.

---

## Archived-Entity Posture

This route family does not treat archived status on the evaluated entity as an automatic scope-validity failure.

If an entity is archived but still exists within current project scope and is otherwise a valid readiness target, evaluation may still be initiated in the first pass.

This route family does not assign special readiness semantics to archived status beyond whatever effect archived state has through the governed rule package.
If archived-entity evaluation behavior needs stricter gating later, that rule must be added explicitly in shared readiness authority rather than inferred locally.

---

## Server-Owned Fields

The following fields are server-owned and must not be caller-settable:

- `id`
- `result`
- `summary`
- `projectId` (resolved from session context, not trusted from body)
- `createdAt`
- all `ReadinessGap` fields except `resolved` and `remediationSuggestion` via the bounded PATCH route

Supplying a server-owned field in a creation request must fail with `400 Bad Request`.

The `result` field is the output of server-side evaluation logic governed by `readiness-evaluation-rules.md`.
Callers may not supply or override it.

The `summary` field is server-generated as part of evaluation execution.
Callers may not supply it.
The server must produce a non-empty summary as part of any evaluation it persists; an evaluation must not be stored without one.

---

## Caller Inputs

### Required input

#### `evaluationType`
Required. Must be a valid readiness evaluation type from `controlled-vocabularies.md`.
Invalid value fails with `422 Unprocessable Entity`.

### Optional inputs

#### `rulePackage`
Optional. Overrides the default rule package for the given evaluation type.
If omitted, the server uses the default rule package mapping from `controlled-vocabularies.md`.
If supplied, it must be a known, compatible rule package for the supplied evaluation type.
An unknown or incompatible `rulePackage` value must fail with `422 Unprocessable Entity`.

#### `deferWithReason`
Optional. A non-empty string that instructs the server to produce a `deferred` result and preserve the reason in the evaluation summary.
If supplied, it must be non-empty; an empty string must fail with `422 Unprocessable Entity`.
When `deferWithReason` is supplied, the server returns `deferred` as the result and does not execute the full evaluation rule logic.
See `readiness-evaluation-rules.md` for the full deferred condition specification.

---

## `POST /readiness-evaluations`

### Purpose
Initiate a server-governed readiness evaluation for a planning entity in current project scope.

### Request body

```json
{
  "projectId": "uuid",
  "entityType": "work_item",
  "entityId": "uuid",
  "evaluationType": "planning",
  "rulePackage": "standard_planning_v1",
  "deferWithReason": null
}
```

### Required fields
- `projectId`
- `entityType`
- `entityId`
- `evaluationType`

### Optional fields
- `rulePackage`
- `deferWithReason`

### Forbidden fields
The caller must not supply:

- `id`
- `result`
- `summary`
- `createdAt`

Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- `projectId` must match current governed project scope
- `entityType` must be a valid readiness entity type
- `entityId` must be a valid UUID
- referenced entity must resolve inside current project scope
- `evaluationType` must be a valid readiness evaluation type
- `rulePackage`, if supplied, must be known and compatible with `evaluationType`
- `deferWithReason`, if supplied, must be non-empty

### Execution behavior
Once validation succeeds, the server:

1. Resolves the rule package (caller-supplied or default)
2. If `deferWithReason` is supplied: produces `deferred` result and stores the reason in `summary`; no further evaluation runs and no `ReadinessGap` rows are created
3. Otherwise: executes the evaluation rules in the order governed by `readiness-evaluation-rules.md`
4. Determines `result` from evaluation output
5. Generates `summary` from the evaluation basis
6. Creates the `ReadinessEvaluation` record
7. Creates all associated `ReadinessGap` records atomically in the same transaction
8. If the evaluated entity is a `WorkItem`: updates `WorkItem.readinessState` in the same transaction

All of steps 6 through 8 must succeed atomically or none must be committed.
Partial evaluation writes are correctness violations.

### Response shape
Return `201 Created` with canonical evaluation record body.

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "entityType": "work_item",
  "entityId": "uuid",
  "evaluationType": "planning",
  "result": "not_ready",
  "rulePackage": "standard_planning_v1",
  "summary": "server-generated evaluation summary",
  "createdAt": "timestamp"
}
```

The response does not include gaps inline. Gaps are retrievable through `GET /readiness-evaluations/{id}/gaps`.

---

## `GET /readiness-evaluations`

### Purpose
List readiness evaluations in current project scope.

### Query parameters
Allowed first-pass query parameters:

- `entityType`
- `entityId`
- `evaluationType`
- `result`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

### Query parameter semantics

#### `entityType`
- optional
- controlled-vocabulary value from readiness entity type set
- invalid value -> `422 Unprocessable Entity`

#### `entityId`
- optional
- UUID
- malformed UUID -> `400 Bad Request`
- must not be supplied without `entityType`; supplying without type -> `400 Bad Request`
- if supplied with `entityType`, filters evaluations for that exact resolved entity in current project scope
- if the referenced entity is not found in current project scope — whether it exists elsewhere or not — the route must return an empty result set without revealing whether the entity exists in another project

#### `evaluationType`
- optional
- controlled-vocabulary value from readiness evaluation type set
- invalid value -> `422 Unprocessable Entity`

#### `result`
- optional
- controlled-vocabulary value from readiness evaluation result set
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
`entityId` must not be supplied without `entityType`.
A missing type for a supplied entity id is a structurally malformed filter and must fail with `400 Bad Request`.

### Ordering
Default and required ordering:

```text
createdAt desc, id asc
```

This ordering is deterministic and must be the basis for cursor generation for this family.
Readiness evaluations are append-only records. `createdAt desc` surfaces the most recent evaluations first, which is the natural view for an operator checking current readiness state.

### Response shape

```json
{
  "data": [
    {
      "id": "uuid",
      "projectId": "uuid",
      "entityType": "controlled-value",
      "entityId": "uuid",
      "evaluationType": "controlled-value",
      "result": "controlled-value",
      "rulePackage": "text",
      "summary": "text",
      "createdAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- list responses return canonical evaluation fields only
- gaps are not included in list responses
- all filters apply within current project scope only
- a valid filter value that matches no evaluations in current scope returns an empty data array
- filters must not leak whether referenced entities exist in another project

---

## `GET /readiness-evaluations/{id}`

### Purpose
Fetch one readiness evaluation by identifier inside current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`

### Behavior
- if evaluation exists in current project scope -> return canonical record
- if evaluation does not exist in current scope -> `404 Not Found`
- if evaluation exists in another project -> route must preserve non-leakage posture and return `404 Not Found`

### Response shape

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "entityType": "controlled-value",
  "entityId": "uuid",
  "evaluationType": "controlled-value",
  "result": "controlled-value",
  "rulePackage": "text",
  "summary": "text",
  "createdAt": "timestamp"
}
```

Gaps are not returned inline. Use the gaps sub-route.

---

## `GET /readiness-evaluations/{id}/gaps`

### Purpose
List the readiness gaps associated with a specific readiness evaluation in current project scope.

### Path parameter
- `id` must be a valid UUID
- malformed UUID -> `400 Bad Request`
- the parent evaluation must exist in current project scope or return `404 Not Found`

### Query parameters
Allowed first-pass query parameters:

- `resolved`
- `severity`
- `cursor`
- `limit`

Unknown query parameters must fail with `400 Bad Request`.

#### `resolved`
- optional
- boolean
- malformed or non-boolean value -> `400 Bad Request`

#### `severity`
- optional
- controlled-vocabulary value from readiness gap severity set
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
      "readinessEvaluationId": "uuid",
      "severity": "controlled-value",
      "description": "text",
      "remediationSuggestion": "text or null",
      "resolved": false,
      "createdAt": "timestamp",
      "updatedAt": "timestamp"
    }
  ],
  "nextCursor": "opaque-string-or-null"
}
```

### Notes
- this sub-route uses the standard list envelope and cursor pagination rules from `api-conventions.md`
- an evaluation with no gaps returns an empty data array, not a `404`
- gaps are always scoped to the parent evaluation
- the parent evaluation must be in current project scope; otherwise `404 Not Found`

---

## `PATCH /readiness-evaluations/{id}/gaps/{gapId}`

### Purpose
Apply bounded updates to a readiness gap.

### Path parameters
- `id` must be a valid UUID (parent evaluation id)
- `gapId` must be a valid UUID
- malformed UUID for either -> `400 Bad Request`
- the parent evaluation must exist in current project scope or return `404 Not Found`
- the gap must belong to that evaluation or return `404 Not Found`

### Allowed fields
- `resolved`
- `remediationSuggestion`

### Forbidden fields
The caller must not patch:

- `id`
- `projectId`
- `readinessEvaluationId`
- `severity`
- `description`
- `createdAt`
- `updatedAt`

Unknown PATCH fields must fail with `400 Bad Request`.
Supplying forbidden fields must fail with `400 Bad Request`.

### Validation
- `resolved`, if supplied, must be a boolean; wrong type -> `400 Bad Request`
- `remediationSuggestion`, if supplied, may be `null` or non-empty text
- supplying an empty string for `remediationSuggestion` must fail with `422 Unprocessable Entity`

### Response shape
Return canonical gap record after patch.

```json
{
  "id": "uuid",
  "projectId": "uuid",
  "readinessEvaluationId": "uuid",
  "severity": "controlled-value",
  "description": "text",
  "remediationSuggestion": "text or null",
  "resolved": true,
  "createdAt": "timestamp",
  "updatedAt": "timestamp"
}
```

### Notes
`severity` and `description` are immutable after creation.
They are evaluation outputs, not caller-adjustable classifications.
`resolved` has no one-way constraint in the first pass; it may be set `false -> true` or `true -> false` through this route.
This route does not re-trigger evaluation, does not mutate the parent evaluation, and does not change `WorkItem.readinessState`.
The governed invalidation path that can reset `WorkItem.readinessState` to `unevaluated` is outside this route family.

---

## Immutability Rule

`ReadinessEvaluation` records are immutable after creation.

No PATCH route exists for evaluation records.
`result`, `summary`, `rulePackage`, `entityType`, `entityId`, and `evaluationType` must not be mutatable through any API path.

The append-only posture of evaluations means a new evaluation must be initiated to supersede a prior result.
The prior evaluation remains in history.

---

## WorkItem Readiness State Synchronization Rule

When a `ReadinessEvaluation` is created for an entity with `entityType = work_item`, the server must update `WorkItem.readinessState` in the same transaction.

The mapping is direct:

- evaluation `result = ready` → `readinessState = ready`
- evaluation `result = not_ready` → `readinessState = not_ready`
- evaluation `result = ready_with_warnings` → `readinessState = ready_with_warnings`
- evaluation `result = deferred` → `readinessState = deferred`

`WorkItem.readinessState` must not be set to `unevaluated` through this path. It is set to `unevaluated` only by the governed invalidation mechanism when prior evaluation basis becomes stale.

This synchronization is mandatory. If the `WorkItem` update fails, the entire evaluation creation must be rolled back.

---

## Atomicity Rule

All of the following must be committed in a single transaction when evaluation creation succeeds:

1. The `ReadinessEvaluation` row
2. All associated `ReadinessGap` rows where rule execution produces gaps
3. The `WorkItem.readinessState` update where applicable

Partial writes are correctness violations.
If any component fails, the entire transaction must be rolled back and the creation must fail with an appropriate server error.

---

## Evaluation Immutability vs Gap Bounded Mutability

Evaluation records are immutable.
Gap records have bounded mutability: only `resolved` and `remediationSuggestion` may be updated.

These are different postures and must not be conflated.

Updating a gap's `resolved` state does not change the parent evaluation's `result`.
A gap resolved to `true` does not re-trigger evaluation or re-sync `WorkItem.readinessState`.
If a new evaluation is required after gaps are resolved, the caller must initiate a new `POST /readiness-evaluations`.

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
- `entityId` supplied without `entityType`

### `422 Unprocessable Entity`
Use for:

- invalid controlled-vocabulary values for `entityType`, `evaluationType`, `result`, `severity`
- `rulePackage` that is unknown or incompatible with the supplied `evaluationType`
- cross-project polymorphic entity rejection without existence leakage
- invalid polymorphic entity reference shape when the request is otherwise well-formed
- empty string supplied as `deferWithReason`
- empty string supplied as `remediationSuggestion`

### `404 Not Found`
Use for:

- evaluation not found in current project scope
- evaluation existing in another project but outside current scope
- gap not found under the specified parent evaluation in current project scope

---

## Non-Leakage Rule

Readiness routes must not leak whether an evaluated entity or a readiness evaluation exists in another project.

Filtering by `entityId` without a match in current scope must return an empty result set, not a cross-project disclosure.

Fetching an evaluation or gap outside current project scope must return `404 Not Found`.

Error body shape must not reveal whether the target exists elsewhere.

---

## Invariants

The following invariants must hold across all readiness route behavior:

### Evaluation-level invariants

1. `result` is always server-owned and never caller-settable.
2. `summary` is always server-generated and non-empty on every persisted evaluation.
3. `rulePackage` is always present, non-null, and reflects the actual package used, whether defaulted or caller-overridden.
4. A caller-supplied `result` or `summary` must always fail with `400 Bad Request`.
5. `deferWithReason`, when supplied and non-empty, produces `deferred` as the result without running full evaluation logic.
6. When `deferWithReason` short-circuits evaluation, no `ReadinessGap` rows are created.
7. Evaluation records have no PATCH route and no mutation path after creation.
8. An evaluation existing in another project must return `404 Not Found`, not a cross-project disclosure.

### Gap and synchronization invariants

9. All gaps associated with an evaluation are created in the same transaction as the evaluation when rule execution produces gaps.
10. `WorkItem.readinessState` is updated in the same transaction as the evaluation creation when `entityType = work_item`.
11. `severity` and `description` on a gap are immutable after gap creation.
12. Gap updates through `PATCH /readiness-evaluations/{id}/gaps/{gapId}` do not mutate the parent evaluation and do not change `WorkItem.readinessState`.

---

## Hammer Expectations

The hammer suite for readiness evaluations and gaps should verify at minimum:

- evaluation creation with valid input for each supported entity type
- malformed UUID rejection with `400`
- unknown query parameter rejection with `400`
- forbidden field rejection on evaluation creation
- caller-supplied `result` rejection with `400`
- caller-supplied `summary` rejection with `400`
- `entityId` without `entityType` rejection with `400`
- invalid `evaluationType` rejection with `422`
- invalid `rulePackage` rejection with `422`
- empty `deferWithReason` rejection with `422`
- `deferWithReason` non-empty produces `deferred` result without full evaluation and without gap creation
- default rule package selection when `rulePackage` omitted
- caller-supplied `rulePackage` override applied correctly
- cross-project entity reference rejection without leakage
- entity not-found-in-scope returns empty list, not cross-project disclosure
- deterministic list ordering for evaluations and gaps
- cursor continuation correctness
- evaluation immutability: no mutation path exists
- gap creation atomicity with parent evaluation
- `WorkItem.readinessState` sync atomicity on `work_item` evaluation
- `WorkItem.readinessState` not changed for non-work-item entity types
- gap `severity` and `description` immutability after creation
- gap `resolved` and `remediationSuggestion` patchable
- empty `remediationSuggestion` rejection with `422`
- unknown PATCH field rejection with `400` on gap route
- forbidden gap field rejection with `400`
- gap PATCH does not re-trigger evaluation or readiness-state sync
- cross-project evaluation fetch non-leakage

---

## Final Rule

Readiness evaluations are one of the highest-value planning-quality judgment families in Project V.

Their API family must remain server-governed, explicit, and immutable-output-oriented.
Callers initiate evaluation. The server produces judgment.

If readiness evaluation routes become a free-form scoring surface, allow caller-supplied results, or permit evaluation mutation after creation, the family has broken its core posture.

---

## Human-In-The-Loop Principle

Readiness results are governance-sensitive because they gate planning progression and handoff eligibility.

Operators and bounded LLMs must be able to trust that:

- evaluation results are server-produced and not caller-manipulated
- gap severity and description cannot be retroactively adjusted to change a result
- a new evaluation is required to supersede a prior result
- `WorkItem.readinessState` accurately reflects the latest evaluation for that work item
- gap resolution does not masquerade as reevaluation
- cross-project entity information is not accidentally leaked through filter behavior

The API family must preserve that trust structurally.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- readiness evaluation creation is an initiation request, not a data-insert request
- the server owns `result`, `summary`, and gap content
- the caller supplies what to evaluate and allowed override inputs only
- evaluations are immutable after creation; a new evaluation supersedes the old one in history
- gaps are created atomically with the evaluation and are not independently creatable
- deferred evaluations do not generate gaps in the first pass
- gap `severity` and `description` cannot be changed; `resolved` and `remediationSuggestion` can
- `WorkItem.readinessState` sync is mandatory and transactional for work-item evaluations
- resolving a gap does not change the evaluation result or re-sync readiness state
- `entityId` filtering requires paired `entityType` and must not leak cross-project entity existence
- `404` does not imply the target never existed anywhere

If implementation allows callers to set `result`, treats evaluation creation as plain CRUD, or allows gap severity mutation, the contract is being violated.

---

## Usage

This document should be used:

- when implementing readiness evaluation and gap routes
- when writing migrations or tests that depend on readiness API behavior
- when writing hammer coverage for readiness routes
- when reviewing whether readiness behavior remains server-governed and ownership-honest
- when checking whether evaluation or gap mutation paths exceed their bounded posture

---

## Related Docs

- `../api-conventions.md`
- `../schema-specification.md`
- `../schema-authority.md`
- `../controlled-vocabularies.md`
- `../polymorphic-reference-enforcement.md`
- `../readiness-evaluation-rules.md`
- `../readiness-methodology.md`
- `../multi-project-doctrine.md`
- `../system-invariants.md`
- `../mcp-surface.md`
- `../schema-governance.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../ecosystem/vocabulary.md`
