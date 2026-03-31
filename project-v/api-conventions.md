# API Conventions

## Purpose

This document defines the common API conventions for Project V.

It exists to answer:

```text
What common rules should all Project V endpoints follow so the API remains explicit, deterministic, multi-project-safe, and resistant to drift?
```

Read this with:

- `schema-specification.md`
- `polymorphic-reference-enforcement.md`
- `schema-governance.md`
- `controlled-vocabularies.md`
- `status-transitions.md`
- `multi-project-doctrine.md`
- `mcp-surface.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- common API contract rules across Project V route families
- pagination posture
- error-code posture
- request and response envelope posture
- actor resolution posture
- unknown-field and unknown-parameter handling
- idempotency posture
- transaction-boundary posture
- external-reference validation posture
- route-family expansion posture

---

## Out of Scope

This document does not define:

- individual endpoint family schemas
- route-by-route request/response bodies
- migration sequencing
- database engine implementation details
- VEDA or V Forge API contracts

Those belong in endpoint family docs and other system-specific authority docs.

---

## System

- project-v

---

## Core Rule

Project V APIs must expose bounded planning and orchestration truth clearly.

They must be:

- explicit
- deterministic
- scope-honest
- boring
- stable

If an API design makes ownership, project scope, or mutation posture harder to understand, it is incorrect.

---

## Naming Rule

Endpoint families should be named after bounded domain concepts.

Examples:

- `projects`
- `objectives`
- `initiatives`
- `work-items`
- `dependencies`
- `decision-records`
- `readiness`
- `research-docs`
- `evidence-links`
- `handoffs`
- `external-links`

Do not use vague family names like:

- `misc`
- `helpers`
- `actions`
- `manager`

Do not preserve old family names that no longer match current shared-root authority. `GitHubLink`-style family naming is replaced by `ExternalLink` posture in the current Project V model.

---

## Scope Rule

Project-scoped routes must make project context explicit.

That means the contract must make it clear:

- whether the route is project-scoped
- how project scope is supplied
- how cross-project access is rejected

Mutation routes must not rely on hidden project inference.

Project scope must be resolved from the governed session/auth context, not caller-supplied convenience fields that can be forged or drift.

---

## Read Rule

Read routes must:

- preserve project boundaries
- return deterministic ordering for list surfaces
- fail safely when scope is wrong or ambiguous
- avoid hidden side effects

Reading by identifier alone must not bypass project ownership rules.

A route that sounds read-only must not mutate state.

---

## Write Rule

Write routes must:

- require explicit project context where project-scoped truth is involved
- represent explicit actions
- reject illegal state changes
- preserve transaction integrity where multiple writes are involved
- avoid hidden convenience mutation

A route that sounds read-only must not mutate state.

Server-owned fields must not be caller-settable just because they are easy to include in a payload.

---

## Ordering Rule

All list-like responses must define deterministic ordering.

Ordering must include a stable tie-breaker where needed.
No endpoint may rely on implicit database ordering.

If a family contract does not state its ordering explicitly, it is incomplete.

---

## Pagination Rule

First-pass list endpoints must use cursor pagination. Offset pagination is not allowed.

Required posture:

- `limit` — maximum number of records to return per page; must be a positive integer; a bounded maximum is enforced server-side
- `cursor` — opaque continuation token from the previous page; omit for the first page
- deterministic ordering that matches the cursor strategy

### Cursor format rule

The first-pass cursor must be a base64url-encoded opaque string that encodes the last seen ordered tuple needed for continuation.

For a route with ordering:

```text
updatedAt desc, id asc
```

the cursor encodes the last seen `updatedAt` and `id` values from the previous page.

Clients must treat cursor values as opaque. Decoding or constructing cursor values manually is not supported.

### Cursor behavior rule

- a cursor is valid only for the ordering defined by that route family
- a malformed cursor must fail with `400 Bad Request`
- a cursor from one route family must not be used with another route family
- a route must not mix offset and cursor behavior in the same contract
- `offset` and `page` query parameters are not allowed on list endpoints

### Response behavior rule

Every list response must include:

- `data` — the array of records for this page
- `nextCursor` — the cursor to use to fetch the next page; must be `null` (not omitted) when there are no more results

A `nextCursor` of `null` is the definitive signal that the caller has reached the end of results.

### No-pagination exception

If a list family is small enough to return all records in a single response without pagination, that must be explicitly declared in the family contract with a stated justification. The default is cursor pagination.

Do not leave pagination behavior hypothetical in contract docs.

---

## Validation Rule

Validation behavior must be explicit and reproducible.

Contracts must make clear:

- what input is required
- what failures block the request
- what fields use controlled vocabulary
- what fields are server-owned
- what fields are immutable after creation if any
- what failures produce `400` vs `422`

Validation must not be guesswork delegated to operator intuition or LLM inference.

---

## Error Code Rule

Project V uses a two-level error distinction across all route families:

- `400 Bad Request` — structural malformation: missing required fields, wrong types, malformed identifiers, malformed cursor, unknown query parameters, caller-supplied forbidden fields, unknown PATCH fields
- `422 Unprocessable Entity` — semantically invalid but well-formed input: controlled-vocabulary violations, lifecycle invalidity, same-project integrity failures, rule-package incompatibility, illegal status transition, illegal polymorphic reference shape

This distinction is not optional.
All route families must apply it consistently.
The phrase "if that distinction is adopted" must not appear in any Project V API contract.

### Not-found and non-leakage posture

Where project scope is wrong or the target record is outside current project scope, route families must preserve non-leakage posture.

A route family may choose `404 Not Found` for absent-in-scope resources, but it must not leak cross-project existence through a different response shape or more permissive message.
The family contract must keep that posture stable.

---

## Actor Resolution Rule

Where a route writes a `StatusHistory` row, the `actor` field is server-resolved from the authenticated request context.

Callers must not supply `actor` in the request body.
The server must produce a non-empty `actor` value as part of completing any transition that writes a history row.

This same posture applies to other server-owned provenance fields if they are introduced later.

---

## Server-Owned Fields Rule

Fields whose value is owned by server-side execution logic must not be caller-settable.

First-pass examples include:

- `WorkItem.readinessState`
- `ReadinessEvaluation.result`
- `ReadinessEvaluation.summary`
- `AuditRun.result`
- `StatusHistory.actor`

If a caller supplies one of these fields where the contract does not permit it, the request must fail with `400 Bad Request`.
Silent ignore is not allowed.

---

## PATCH Body Unknown Fields Rule

Unknown fields in a PATCH request body must be rejected with `400 Bad Request`.

Silent ignore of extra body fields is not allowed.
This rule applies to all PATCH routes across all Project V families.

---

## Unknown Query Parameter Rule

All list endpoints must fail with `400 Bad Request` when an unrecognized query parameter is supplied.

Silent ignore of unknown parameters is not allowed.
Operators and LLMs must be able to trust that a query with an unrecognized filter is rejected rather than quietly returning unfiltered results.

---

## Error Response Rule

Error responses should use one stable body shape across Project V route families.

Recommended first-pass shape:

- `error.code`
- `error.message`
- `error.details` optional structured data
- `error.requestId` optional correlation value if available

The same class of error should not return wildly different body shapes across route families.

---

## Response Shape Rule

Responses should prefer:

- stable field names
- explicit IDs
- explicit status fields
- explicit project references where helpful
- explicit derived vs canonical distinctions where relevant

Do not return vague payloads that require guesswork.

### List response envelope vs item fields

Family docs describe item-level fields under their response-shape sections.
Those field lists describe the contents of the `data` array, not the full list response envelope.
The `data` / `nextCursor` wrapper is governed by the Pagination Rule above and applies to all list responses.
Family docs do not need to repeat the wrapper structure unless a family-specific exception exists.

---

## External Reference Validation Rule

Project V accepts external references (URLs, storage locators, external identifiers) but does not validate external existence.

First-pass posture:

- **Project V does not make outbound calls to validate external references.** Checking whether a GitHub URL resolves, a VEDA observation exists, or a storage locator is reachable would turn Project V into an observatory or execution client and violate its boundary invariants.
- **Format validation is required.** External references must conform to basic syntactic rules at the point of creation or mutation.
- **Staleness is the caller's responsibility.** Project V does not track whether an external reference has become stale, moved, or been deleted.
- **Duplicate external references** are governed by natural uniqueness constraints where they exist.

### First-pass examples

- `ExternalLink.url` must be non-empty and must begin with `https://`
- `EvidenceLink.targetLocator` must be non-empty
- `ResearchDoc.storageLocator` must be non-empty

This posture preserves boundary integrity.
Project V is a planning record of external references, not a cache or validator of external state.

---

## Boundary Honesty Rule

Project V APIs must not pretend to be VEDA or V Forge APIs.

If Project V references another bounded system, the contract must keep that boundary visible.

A referenced external identifier is not the same thing as owned external truth.
A bounded planning-side link is not permission to widen Project V into a downstream execution model.

---

## Expansion Rule

New route families or major route changes require governance review.

Do not add a route just because a surface wants a one-off shortcut.
Prefer coherent families over scattered convenience endpoints.

Endpoint expansion must remain consistent with `schema-governance.md` and later endpoint-governance authority.

---

## Idempotency Posture Rule

Project V POST endpoints do not provide idempotency guarantees beyond natural uniqueness constraints.

First-pass posture:

- **Entities with a caller-supplied `key`** (`Project`, `Objective`, `Initiative`, `WorkItem`): duplicate creation attempts with the same `key` within the same scope must fail with `409 Conflict`
- **Naturally deduplicated relationships** (`Dependency`, `ExternalLink`): duplicate creation attempts that violate natural uniqueness must fail with `409 Conflict`
- **Non-deduplicated support records** (`EvidenceLink`, `ResearchDoc`): repeated requests may create repeated records unless a later contract introduces stronger deduplication
- **Evaluation events** (`ReadinessEvaluation`, `AuditRun`): each creation is a distinct event and is not considered a duplicate even if the target is the same
- **Status transitions**: repeating a transition into an already-held status must fail with `422 Unprocessable Entity`, not silently succeed

Project V does not support idempotency keys, request deduplication tokens, or conditional PUT semantics in the first pass.
If stronger idempotency is required, it must be modeled explicitly through governance.

---

## Transaction Boundary Rule

The following operation classes must execute atomically.
A partial write for any of these is a correctness violation.

- **Status transition + StatusHistory write**: any status route that produces a `StatusHistory` row must write the state change and the history row in the same transaction
- **Readiness evaluation creation**: creating a `ReadinessEvaluation` must atomically create all associated `ReadinessGap` records and, where the evaluated entity is a `WorkItem`, update `readinessState`
- **DecisionRecord supersedence**: the `recorded -> superseded` transition must write the status update and the `StatusHistory` row in the same transaction where history is required
- **Handoff completion**: any governed transition that sets `Handoff.status` to `completed` must set `completedAt` in the same transaction
- **Entity creation with same-project validation**: creation of records that validate cross-entity ownership (for example `Dependency`, `Handoff`, `Initiative` with `objectiveId`, `WorkItem` with `initiativeId`) must resolve and validate all referenced entities before commit

Do not specify database-engine implementation details in API contracts.
State the atomicity requirement at the contract level and let implementation choose the correct mechanism.

---

## Polymorphic Reference Rule

Any route family that accepts or mutates `entityType` + `entityId` references must follow `polymorphic-reference-enforcement.md`.

That means:

- allowed entity types are not free-form
- same-project validation is mandatory
- the central resolver must be used
- the `AuditRun.targetEntityType = 'project'` special case must be handled explicitly

No API family may invent its own polymorphic resolution rules.

---

## Hammer Rule

Important routes should not be considered hardened until hammer coverage verifies:

- scope enforcement
- validation behavior
- deterministic ordering
- negative-path rejection
- transaction correctness where relevant
- polymorphic non-leakage where relevant

---

## Final Rule

Project V APIs should feel like governed contracts, not improvised plumbing.

If a route becomes harder to classify, harder to test, easier to sprawl, or easier to misuse across project boundaries, the route is wrong.

---

## Human-In-The-Loop Principle

API contract quality matters because human operators and bounded LLMs both depend on deterministic system behavior.

If the API silently accepts malformed fields, leaks project existence, or permits server-owned fields to be caller-set, human governance becomes theater and LLM behavior becomes harder to bound.

The API must preserve the same anti-drift posture the docs require.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- Project V APIs are explicit and stable by design
- `400` vs `422` is a governed distinction, not an optional style preference
- cursor pagination is required unless a family explicitly justifies a no-pagination exception
- server-owned fields must not be caller-set
- polymorphic references require central resolution and same-project enforcement
- natural uniqueness is not the same as full idempotency
- Project V does not validate external existence because that would violate boundary posture

If implementation makes the API more magical, more permissive, or more ad hoc than this document allows, the conventions are being violated.

---

## Usage

This document should be used:

- before writing any Project V endpoint family doc
- when deciding request validation posture
- when deciding error-code behavior for a new route
- when reviewing whether a family preserves project-scope honesty and non-leakage
- when writing hammer expectations for API behavior
- when rejecting convenience-driven endpoint sprawl

---

## Related Docs

- `schema-specification.md`
- `polymorphic-reference-enforcement.md`
- `schema-authority.md`
- `schema-governance.md`
- `controlled-vocabularies.md`
- `status-transitions.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `multi-project-doctrine.md`
- `mcp-surface.md`
- `github-integration.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
