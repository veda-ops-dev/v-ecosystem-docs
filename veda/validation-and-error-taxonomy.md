# VEDA Validation and Error Taxonomy

## Purpose

This document defines the governed validation and error taxonomy for VEDA.

It exists to answer:

```text
What kinds of failures does VEDA's API and ingest surface recognize, how must each
failure class be handled, what must be rejected as malformed vs semantically invalid,
what must remain non-leaky, and what error shapes are stable enough for consistent
implementation and hammer coverage?
```

Read this with:

- `api-contract-principles.md`
- `schema-reference.md`
- `observatory-models.md`
- `search-intelligence-layer.md`
- `evidence-and-source-provenance.md`
- `system-invariants.md`
- `providers/registry.md`
- `../ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-003-veda-brain-eliminated.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the classification of all VEDA validation and error conditions
- the malformed vs semantically invalid distinction across all VEDA surfaces
- required-field validation rules
- unknown-field and unknown-parameter posture
- scope and project-isolation validation
- non-leakage posture for scope failures
- provider identity and provider authentication failure classes
- ingest-path validation posture
- deferred-domain rejection posture
- derived-response validation posture
- stable error-shape principles
- what details may be surfaced vs must be withheld
- anti-drift rules that prevent provider-shaped or content-graph-era error semantics from re-entering

---

## Out of Scope

This document does not define:

- individual route family request/response body schemas — those belong in route-family authority docs
- the full API contract governing principles — those belong in `api-contract-principles.md`
- provider-specific payload formats or ingest implementation details — those belong in provider-specific docs
- MCP tool surface contracts — those belong in `mcp-surface.md`
- operator surface behavior — that belongs in `operator-surfaces.md`
- signal package payload formats — those belong in the interface docs
- HTTP transport or authentication protocol mechanics beyond what affects error posture
- database-engine constraint error handling beyond the contract-level posture described here

---

## System

- veda

---

## Core Rule

VEDA validation must preserve observatory boundaries, not just data shape.

Validation is not only structural input checking. It also enforces:

- project isolation
- observatory ownership boundaries
- provider registration and authentication
- schema family access rules
- deferred-domain admission gates
- provenance completeness for observation intake

A request that passes structural validation but violates one of these observatory boundaries must still be rejected. The failure class and the error code depend on the specific violation. This document defines both.

---

## Relationship to API Contract Principles

`api-contract-principles.md` establishes the governing contract posture — including that VEDA uses a two-level error distinction (`400` vs `422`), that error responses use a stable shape, and that non-leakage is mandatory for scope failures. This document provides the implementation-level taxonomy that maps specific failure conditions to those principles.

The relationship:

- `api-contract-principles.md` says what the error posture must be.
- This document says what specific conditions trigger each error class and how each must be handled.

Where a rule in this document appears to conflict with `api-contract-principles.md`, the contract principles document takes precedence and this document must be updated to match.

---

## Relationship to `schema-reference.md`

`schema-reference.md` governs which fields exist, which are server-owned, which are immutable after creation, and which controlled vocabulary values are governed. This document references that authority when stating validation rules for specific field categories. The field-level source of truth is always `schema-reference.md`.

---

## Relationship to `search-intelligence-layer.md`

The search intelligence layer produces derived outputs from canonical observation records. Validation rules specific to derived-response requests — including provenance-basis validation and deferred-domain admission gating — are stated here and must remain consistent with the derivation posture in `search-intelligence-layer.md`.

---

## The Two-Level Error Distinction

VEDA uses exactly two HTTP error codes for client-originated failures:

**`400 Bad Request`** — structural malformation. The request cannot be parsed into a meaningful operation because it is missing required structure, contains wrong types, supplies forbidden fields, supplies server-owned fields, or includes unrecognized structural elements.

**`422 Unprocessable Entity`** — semantically invalid but well-formed. The request is structurally parseable but violates a governed semantic rule: a controlled vocabulary constraint, a lifecycle rule, a project-integrity rule, or a uniqueness constraint that can only be detected after parsing.

These two codes are not interchangeable. The distinction must be applied consistently across all route families and ingest paths. An implementer must not return `400` when `422` is correct, and must not return `422` when `400` is correct.

Additional HTTP codes used by VEDA and their meaning:

**`401 Unauthorized`** — the request did not supply valid authentication. The caller's identity cannot be established.

**`403 Forbidden`** — the caller's identity is established or asserted but the requested operation is not permitted. This covers two distinct sub-cases: (a) a registered provider whose credentials are valid but whose identity does not confer authority for the specific ingest surface being targeted, and (b) a provider whose asserted identity is not present in the registry at all — because an unregistered provider identity does not confer ingest authority regardless of whether credentials are technically well-formed. See Rule PI1 and Rule PI2 for the distinction. `403` must never be used in place of `404` for scope failures. Using `403` for a cross-project access attempt leaks the existence of the out-of-scope record. See Non-Leakage Rules.

**`404 Not Found`** — the requested record does not exist within the current project scope. This is the correct response for cross-project access attempts. See Non-Leakage Rules.

**`409 Conflict`** — a creation attempt would violate a natural uniqueness constraint on the record family (e.g., attempting to create a duplicate `KeywordTarget` for the same `(projectId, query, locale, device)` tuple or a duplicate `SERPSnapshot` for the same uniqueness key). `409` is the correct code for uniqueness violations that arise from a valid, well-formed, semantically coherent request.

**`500 Internal Server Error`** — an unexpected server-side failure. This must not leak internal stack traces, database error messages, raw provider error payloads, or any information that reveals internal implementation details. See Error Detail Surface Rules.

---

## Validation Categories

The following categories organize all VEDA validation conditions. Each category has specific rules defined in subsequent sections.

### Category 1 — Structural / Malformation (→ `400`)
Missing required fields, wrong types, unrecognized field names, malformed identifiers, malformed cursors, server-owned fields supplied by caller, unknown query parameters.

### Category 2 — Semantic Invalidity (→ `422`)
Controlled-vocabulary violations, lifecycle/status invalidity, project-integrity violations, uniqueness violations detectable only after parsing (→ `409` where applicable), provenance completeness violations on intake paths.

### Category 3 — Scope and Project Isolation (→ `404` with non-leakage)
Cross-project access attempts. Out-of-scope record references. Missing project context where required.

### Category 4 — Provider and Ingest Authentication (→ `401` or `403`)
Unregistered provider attempting ingest. Registered provider failing credential verification. Ingest arriving through an ungoverned path.

### Category 5 — Deferred-Domain Rejection (→ `422` with stable message)
Request targeting a deferred observatory domain — GA4, YouTube enrichment — that has no governed canonical record family.

### Category 6 — Derived Response Validation (→ `400`, `404`, or `422` depending on failure type)
Derived route request where the derivation basis is missing, out of scope, or requests a derivation VEDA does not own.

---

## Category 1 — Structural Malformation Rules (400)

These failures occur when the request cannot be correctly parsed or mapped to a valid operation target regardless of any business logic.

### Rule S1 — Missing required fields

A required field that is absent from a creation or mutation request body must fail with `400 Bad Request`.

Required fields for each record family are defined in `schema-reference.md`. Common examples:

- `SourceItem` creation: `url`, `sourceType`, `platform`, `capturedBy`, `operatorIntent`, `contentHash` are all required at creation
- `KeywordTarget` creation: `query`, `locale`, `device` are required identity fields
- `SERPSnapshot` ingest: `query`, `locale`, `device`, `capturedAt`, `source`, `rawPayload` are required

A missing required field must be reported in `error.details` identifying which field(s) were absent.

### Rule S2 — Wrong field types

A field supplied with the wrong data type must fail with `400 Bad Request`. Type mismatch includes: a non-UUID value where a UUID is required, a non-boolean where a boolean is required, a non-integer where an integer is required.

### Rule S3 — Unknown fields on creation routes

A creation request body containing fields not defined for that record family must fail with `400 Bad Request`. Silent ignore of unknown creation fields is not allowed.

### Rule S4 — Unknown fields on PATCH routes

A PATCH request body containing fields not in the governed patchable-field set for that record family must fail with `400 Bad Request`. Silent ignore is not allowed. This applies to all PATCH routes across all VEDA surfaces.

### Rule S5 — Caller-supplied server-owned fields

If a caller supplies a field that is server-owned — such as `SERPSnapshot.capturedAt`, `SERPSnapshot.source`, `SERPSnapshot.rawPayload`, `SourceItem.capturedAt`, `SourceItem.capturedBy` — the request must fail with `400 Bad Request`. The error must identify the field as server-owned. Silent ignore is not allowed.

The definitive list of server-owned fields per record family is in `schema-reference.md`. Server-owned status does not vary by route context — a field that is server-owned is server-owned everywhere.

### Rule S6 — Immutable fields on update

A PATCH or update request supplying a field designated as immutable after creation must fail with `400 Bad Request`. Common examples:

- `SourceItem.url`, `SourceItem.capturedAt`, `SourceItem.capturedBy`, `SourceItem.operatorIntent`, `SourceItem.contentHash`
- `KeywordTarget.query`, `KeywordTarget.locale`, `KeywordTarget.device`

The definitive immutability posture per field is in `schema-reference.md`.

### Rule S7 — Malformed identifiers

A UUID field supplied with a non-UUID string must fail with `400 Bad Request`. A malformed cursor value must fail with `400 Bad Request`.

### Rule S8 — Unknown query parameters

Any unrecognized query parameter on any list or filter route must fail with `400 Bad Request`. Silent ignore of unknown query parameters is not allowed. The error must indicate that unrecognized parameters are not permitted, and `error.details` should identify the offending parameter name where feasible.

This rule applies to all VEDA routes — read routes, write routes, and ingest-path query interfaces.

### Rule S9 — Caller-supplied primary keys

All VEDA record primary keys are server-generated UUIDs. A request that supplies a primary key value for a new record must fail with `400 Bad Request`.

---

## Category 2 — Semantic Invalidity Rules (422 / 409)

These failures occur when the request is structurally well-formed but violates a governed semantic constraint detectable after parsing.

### Rule V1 — Controlled vocabulary violations

A field that uses a governed controlled vocabulary and receives a value not in that vocabulary must fail with `422 Unprocessable Entity`. The vocabulary in question and the invalid value must be identifiable from the error response.

Governed vocabularies in VEDA (source of truth: `schema-reference.md` Controlled Vocabularies section):

- `SourceItem.sourceType`: `rss`, `webpage`, `comment`, `reply`, `video`, `other`
- `SourceItem.platform`, `SourceFeed.platform`: `website`, `x`, `youtube`, `github`, `reddit`, `hackernews`, `substack`, `linkedin`, `discord`, `other`
- `SourceItem.status`: `ingested`, `triaged`, `used`, `archived`
- `SourceItem.capturedBy` / actor fields: `human`, `llm`, `system`
- `Project.lifecycleState`: `created`, `bootstrapping`, `active`, `paused`, `archived`
- `SERPSnapshot.aiOverviewStatus`: `present`, `absent`, `parse_error`
- `EventLog.eventType`: governed event vocabulary in `schema-reference.md`
- `EventLog.entityType`: governed entity-type vocabulary in `schema-reference.md`

A vocabulary value not in the governed list is invalid regardless of how plausible it appears. Local implementation must not accept unlisted values silently.

### Rule V2 — Illegal status transitions

A status transition on a governance record that is not permitted must fail with `422 Unprocessable Entity`. Status transition tables are not defined in this document; they belong in governance record family docs as they are written. The posture here is: a transition request for a status that the current state does not permit produces `422`, not `400`, because the request is structurally valid.

### Rule V3 — Provenance completeness violations on intake

An intake request where a required provenance field is present but empty — for example, `SourceItem.operatorIntent` is an empty string — must fail with `422 Unprocessable Entity`. The field is present (so it is not a missing-field `400`) but empty (so it is semantically invalid for provenance purposes).

Required provenance fields that must be non-empty:

- `SourceItem.operatorIntent` — must not be an empty string
- `SERPSnapshot.source` — must not be an empty string
- `SERPSnapshot.rawPayload` — must not be empty/null JSON on ingest

### Rule V4 — Uniqueness constraint violations

A creation attempt that would violate a natural uniqueness constraint for a record family must fail with `409 Conflict` where the conflict is detectable from well-formed input. This is distinct from a semantic invalidity that causes `422` — the uniqueness conflict arises from a structurally and semantically valid request that simply conflicts with existing state.

First-pass uniqueness constraints:

- `(projectId, feedUrl)` on `SourceFeed`
- `(projectId, url)` on `SourceItem`
- `(projectId, query, locale, device)` on `KeywordTarget`
- `(projectId, query, locale, device, capturedAt)` on `SERPSnapshot`
- `(projectId, query, pageUrl, dateStart, dateEnd)` on `SearchPerformance`
- `key` global uniqueness on `SystemConfig`

The `409` response must not leak whether a conflicting record belongs to another project. If the conflict cannot be confirmed within the current project scope, return `409` only if the conflict is provably intra-project.

In practice, all first-pass VEDA uniqueness constraints span `projectId` or are globally scoped (as with `SystemConfig.key`); a genuinely ambiguous intra-vs-cross-project uniqueness conflict should not arise from the governed schema. If one does arise, it indicates a schema boundary issue that must be escalated through governed review rather than silently resolved with a generic error code.

### Rule V5 — Same-project FK integrity failures

A creation request where a referenced FK target (e.g., `SourceItem.sourceFeedId`) does not exist within the current project scope must fail with `422 Unprocessable Entity`. This is semantically invalid input — the FK value is a well-formed UUID, but the referenced record is not found within scope. See Non-Leakage Rules for how the response must be shaped when the referenced record might exist in another project.

---

## Category 3 — Scope and Non-Leakage Rules (404)

### Rule NL1 — Cross-project access attempts return 404

A request that attempts to read, update, or delete a record belonging to a project other than the active session project must return `404 Not Found`. VEDA must not return `403 Forbidden` for cross-project access attempts, as `403` reveals that the record exists — which is itself a leakage of cross-project information.

The `404` response for a cross-project attempt must be structurally identical to the `404` response for a genuinely non-existent record. The error body must not contain any field or message that allows the caller to distinguish between "this record does not exist" and "this record exists in another project."

### Rule NL2 — Missing project scope returns 422

A request that is project-scoped but provides no project context at all must fail with `422 Unprocessable Entity` — it is semantically invalid input, not a structural malformation. The project context is required for the operation to be meaningful.

This rule applies when the session itself is valid but no project scope can be resolved from it. An absent or invalid session token produces `401 Unauthorized` before project-scope resolution is attempted; that failure is governed by the `401` definition above and is not a project-scope semantic failure.

If project scope cannot be resolved from the session/auth context and no caller-supplied scope is present, the failure is `422` and the error message must not indicate whether any project exists.

### Rule NL3 — Project scope is resolved from session context, not request body

Project scope must be resolved from the governed session or authentication context. A caller-supplied `projectId` field in a request body must be validated against the session-resolved scope. If the two do not match, the request must fail with `422 Unprocessable Entity`, not `403`. `422` does not reveal whether the supplied projectId belongs to any real project.

### Rule NL4 — Same-project FK reference failures on creation must not leak cross-project existence

When a creation request supplies a FK reference (e.g., `sourceFeedId`) that is a well-formed UUID but does not resolve to a record within the current project, the response must fail with `422 Unprocessable Entity`. The response must not vary in shape or message based on whether that UUID belongs to a record in another project. A response that says "this feed belongs to a different project" is a cross-project existence leak. The response must only say the referenced feed was not found in the current project scope.

### Rule NL5 — List routes with out-of-scope filters return empty, not error

A list route that accepts a filter by FK (e.g., `sourceFeedId`) where the filter value does not match any record in the current project scope must return an empty `data` array with `nextCursor: null`. It must not return `404` or any error that would reveal the existence of the filtered entity in another project. Empty results are the correct and complete response.

---

## Category 4 — Provider and Ingest Failure Rules

### Rule PI1 — Unregistered provider ingest must be rejected before producing any record

An ingest request whose source identity does not match any entry in `providers/registry.md` must be rejected before any record is created. The ingest path must not partially write a `SERPSnapshot` or `SearchPerformance` record for an unregistered source.

The correct response is `403 Forbidden` — the ingest endpoint was reached but the caller does not have ingest authority. The error message must not enumerate the contents of the provider registry or indicate whether a "close" name might be registered. The response must state only that the provider is not recognized as an active integration.

### Rule PI2 — Provider authentication failure is distinct from unknown provider

An ingest request from a provider that is registered in `providers/registry.md` but fails credential verification must be rejected with `401 Unauthorized`. This is distinct from Rule PI1 (unknown provider → `403`):

- `401`: the provider name is known, but the credential or token presented does not authenticate successfully
- `403`: the provider name is not registered at all

These two cases must produce distinct HTTP status codes. An implementer must not collapse them into a single generic rejection, because the distinction matters for incident diagnosis.

The error body for both must not reveal which specific credential check failed or what the correct credential format is.

### Rule PI3 — Raw provider error payloads must not be forwarded to API clients

When a provider ingest path fails due to a provider-side error — the upstream provider returned an error payload, a timeout, or an unexpected response — the VEDA API must not forward the raw provider error to the client. The error VEDA returns to the caller must use the stable VEDA error shape and must describe the failure in VEDA's own terms: "the ingest operation could not be completed," not a verbatim copy of the upstream provider's error body.

Provider-specific error internals are evidence for VEDA's own logging and diagnostics. They must not leak into the client-facing error surface.

### Rule PI4 — Ingest path validation must enforce the same field rules as client write routes

The ingest path for observation records (`SERPSnapshot`, `SearchPerformance`) must apply all of the same structural and semantic validation rules that apply to client write routes. The fact that an ingest request arrives through a provider-authenticated path does not exempt it from required-field validation, vocabulary validation, or uniqueness constraint handling.

Ingest paths are governed entry points, not bypass gates.

### Rule PI5 — Ingest for deferred domains must be rejected

An ingest attempt targeting a record family for a deferred observatory domain — GA4 observations, YouTube enrichment data — must be rejected. No ingest path may accept data for a deferred domain before its canonical record family is governed and added to `schema-reference.md`. See Category 5 for the error posture.

---

## Category 5 — Deferred-Domain Rejection Rules

### Rule DD1 — Deferred domains do not have active routes or ingest paths

Observatory domains that are owned by VEDA but not yet governed — currently GA4 observations and YouTube enrichment data — must not have active API routes, active ingest paths, or any active write surface. A request targeting such a domain must be rejected.

### Rule DD2 — Deferred-domain rejection posture is 422, not 404

A request that explicitly targets a deferred domain — for example, an ingest attempt labeled as a GA4 observation record — must fail with `422 Unprocessable Entity`. The failure is semantic, not structural: the request is well-formed but references a domain that is not yet active.

The error message must make clear that the domain is recognized as owned by VEDA but is not yet available for active use. The response must not imply that the domain does not belong to VEDA. The correct framing is: "This observatory domain is not yet active. Governance has not yet admitted it for implementation."

### Rule DD3 — Deferred domains must not receive partial support

Partial support for a deferred domain — for example, accepting ingest for it but not exposing read routes, or exposing a read route that returns an empty schema — is a boundary violation. A deferred domain is either fully admitted (canonical record family governed, schema updated, routes active) or fully rejected. Half-admission is not allowed.

---

## Category 6 — Derived Response Validation Rules

### Rule DR1 — Derived route requests must validate their derivation basis before responding

A route that serves derived search intelligence output must verify that the canonical observation records underlying the derivation exist and are accessible within the current project scope before computing or returning a response. If the derivation basis does not exist in scope, the response must fail with `404 Not Found`.

### Rule DR2 — Derived output requests for deferred domains fail with 422

A request for a derived output that would require aggregating data from a deferred domain must fail with `422 Unprocessable Entity`, using the same posture as Rule DD2. The response must not pretend to serve partial derived output that excludes the deferred domain silently.

### Rule DR3 — Derived routes must not accept canonical-record mutation parameters

A route that returns derived output must not accept parameters that imply mutation of canonical observation records. If a request to a derived route includes parameters that look like creation or modification of underlying observation records, the request must fail with `400 Bad Request`.

### Rule DR4 — Derived response validation must not blur raw-vs-derived boundary

A request that asks for a derived output must receive a clearly labeled derived response. A request that asks for a canonical observation record must receive the canonical record. If a caller supplies parameters that would cause a canonical-record route to silently return derived output instead, the route must not comply. The canonical record must be returned as-is, or the route must fail. The raw-vs-derived boundary must not be negotiable at request time.

---

## Error Shape Rules

### Rule ES1 — All VEDA error responses use a stable shape

Every error response — across all routes, all failure categories, all surfaces — must use the following shape:

```json
{
  "error": {
    "code": "string — machine-readable error code",
    "message": "string — human-readable description",
    "details": "object or null — optional structured detail",
    "requestId": "string or null — optional correlation identifier"
  }
}
```

Deviations from this shape are not allowed. A route that returns a different error body structure is non-conforming.

### Rule ES2 — Error codes are machine-readable and stable

The `error.code` field must be a stable machine-readable string — not a freeform sentence or a dynamic value. Error codes must be consistent across route families for the same class of error.

First-pass error code conventions:

- `MISSING_REQUIRED_FIELD` — Rule S1
- `WRONG_FIELD_TYPE` — Rule S2
- `UNKNOWN_FIELD` — Rules S3, S4
- `SERVER_OWNED_FIELD` — Rule S5
- `IMMUTABLE_FIELD` — Rule S6
- `MALFORMED_IDENTIFIER` — Rule S7
- `UNKNOWN_QUERY_PARAMETER` — Rule S8
- `CALLER_SUPPLIED_ID` — Rule S9
- `INVALID_VOCABULARY_VALUE` — Rule V1
- `INVALID_STATUS_TRANSITION` — Rule V2
- `EMPTY_REQUIRED_PROVENANCE_FIELD` — Rule V3
- `CONFLICT` — Rule V4 (used with `409`)
- `REFERENCED_RECORD_NOT_FOUND` — Rule V5
- `PROVIDER_NOT_REGISTERED` — Rule PI1 (used with `403`)
- `PROVIDER_AUTHENTICATION_FAILED` — Rule PI2 (used with `401`)
- `DOMAIN_NOT_YET_ACTIVE` — Rules DD2, DR2
- `DERIVATION_BASIS_NOT_FOUND` — Rule DR1
- `SCOPE_NOT_RESOLVED` — Rule NL2

This list is not exhaustive. Additional codes may be introduced in route-family docs as needed. Any new code introduced in a route-family doc must be consistent with the categories in this document.

### Rule ES3 — Error details must not leak internal implementation

The `error.details` object may contain structured information that helps the caller fix their request — field names that were missing or invalid, the vocabulary values that are accepted, the constraint that was violated. It must not contain:

- database error messages or constraint names
- provider error payloads or provider-specific error codes
- internal stack traces, class names, or file paths
- cross-project record identifiers or project UUIDs not belonging to the active session
- information about other records, other projects, or other callers

The rule: if a piece of information would help someone attack the system boundary or infer the existence of records outside their scope, it must not appear in the error response.

### Rule ES4 — The 500 error body must contain no internal detail

A `500 Internal Server Error` response must return the stable error shape with a generic `error.code` (e.g., `INTERNAL_ERROR`) and a non-specific `error.message`. The `error.details` field must be `null`. Internal failure details belong in server-side logs, not in client responses.

### Rule ES5 — Error body shape must not vary by error category

The error body shape must be the same for `400`, `401`, `403`, `404`, `409`, `422`, and `500` responses. The only variation is in the HTTP status code, the `error.code` value, and the `error.message` and `error.details` content. The enclosing structure `{ "error": { ... } }` must be present in every error response.

---

## Anti-Drift Rules

### Rule 1 — Validation must not be shaped by provider error semantics

When a provider upstream returns an error, VEDA must translate that error into VEDA's own error taxonomy before returning a response. Provider-specific error codes, provider-specific field names, and provider-specific status codes must not appear in VEDA's client-facing error surface. VEDA's validation posture is observatory-owned, not provider-dictated.

### Rule 2 — Content-graph and planning concepts must not re-enter through validation language

Validation error messages and error codes must not reference content graph entities (pages, topics, entities) or planning entities (objectives, initiatives, work items). If a validation rule rejects a request because it references a content graph concept, the error must frame the rejection in terms of VEDA's observatory boundary, not in terms of content graph ownership.

### Rule 3 — Non-leakage must be applied uniformly, not only where it is convenient

The non-leakage posture defined in Category 3 applies to every route family, every filter parameter, and every FK-reference validation. A route family doc that establishes its own more permissive non-leakage posture is producing a doctrine violation, not a justified exception.

### Rule 4 — Deferred domains must not receive any active error posture that implies they are active

A `422` response for a deferred-domain request must not include error details that suggest the domain is partially supported, queued for activation, or temporarily unavailable. The message must communicate that the domain is owned but not yet admitted for implementation. No other framing is acceptable.

### Rule 5 — Provider authentication failures must not collapse into a single undifferentiated rejection

The distinction between an unregistered provider (`403`) and a registered provider with failed credentials (`401`) must be maintained. Collapsing both into a generic `403` would hide the distinction between "we don't know who you are" and "we know who you are but your credentials are wrong" — and that distinction matters for incident diagnosis without leaking provider registry contents.

### Rule 6 — Ingest paths must not bypass client-route validation rules

An ingest path is not exempt from the validation rules that apply to client write routes. Any rule stated in this document for required fields, vocabulary constraints, server-owned fields, or uniqueness constraints applies equally to ingest paths and to client write routes.

### Rule 7 — Error taxonomy additions require governance review

Adding a new `error.code` value or a new failure category not covered by this document requires updating this document through governed review. An implementation that introduces local error codes not traceable to this taxonomy produces ungoverned error behavior that cannot be consistently hammer-covered.

### Rule 8 — The raw-vs-derived boundary must not be negotiable at request time

No combination of query parameters, headers, or request body fields should cause a canonical-record route to behave as a derived route, or a derived route to behave as a canonical-record route. The route type determines the response type. The caller cannot negotiate that distinction away.

---

## Non-Goals

This document does not:

- define individual VEDA route family schemas or request/response body shapes
- govern MCP tool surface error behavior beyond what the underlying API enforces
- define provider-specific ingest pipeline implementation
- govern HTTP authentication mechanism choices (token format, OAuth flow, etc.)
- constitute a full route-by-route error reference
- govern error behavior for deferred domains that have not yet been admitted
- define the full set of `error.code` values that will ever exist in VEDA — that grows as route families are documented

---

## Final Rule

VEDA validation enforces observatory boundaries, not just data shape. A request that is structurally well-formed can still be wrong if it violates project isolation, attempts to ingest from an unregistered provider, targets a deferred domain, or tries to write canonical truth that VEDA does not own.

The error taxonomy exists to make those rejections consistent, non-leaky, and covererable by hammer tests. A VEDA surface that returns inconsistent, leaky, or provider-shaped error behavior is a governed boundary failure, not a minor API style preference.

---

## Usage

This document should be used:

- when implementing validation logic for any VEDA route family or ingest path
- when deciding which HTTP status code applies to a specific failure condition
- when writing hammer test expectations for VEDA validation behavior
- when reviewing whether a VEDA error response leaks internal or cross-project information
- when deciding whether a new failure condition belongs in an existing category or requires a new one
- when reviewing whether a route family doc's stated error posture is consistent with this taxonomy

---

## Related Docs

- `api-contract-principles.md`
- `schema-reference.md`
- `observatory-models.md`
- `search-intelligence-layer.md`
- `veda.md`
- `system-invariants.md`
- `data-boundaries.md`
- `evidence-and-source-provenance.md`
- `mcp-surface.md`
- `providers/registry.md`
- `../ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-003-veda-brain-eliminated.md`
- `../project-v/api-conventions.md`
- `../governance/testing-and-verification-doctrine.md`
