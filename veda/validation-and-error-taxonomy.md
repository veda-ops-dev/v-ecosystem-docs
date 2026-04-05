# VEDA Validation and Error Taxonomy

## Purpose

This document defines the validation classes, error semantics, and response taxonomy VEDA uses across its API surface.

It exists to answer:

```text
How should VEDA classify invalid input, malformed requests, scope failures, provider failures, ingest failures, lifecycle violations, provenance violations, and cross-system boundary errors so developers, operators, and LLMs can reason about failures without drifting into leaky, inconsistent, or boundary-weak API behavior?
```

This is a Tier 2 VEDA implementation-build-spec authority document.

---

## Scope

This document governs:

- the validation classes used across VEDA routes
- the status-code semantics VEDA uses for malformed, invalid, conflicting, missing, and out-of-scope requests
- the stable error envelope for VEDA responses
- route-family error posture for read, write, ingest, and derived-output routes
- scope-enforcement and non-leakage error behavior
- provider and ingest-specific failure posture
- provenance-related validation posture
- anti-drift rules that keep VEDA errors boring, consistent, and boundary-safe

This document assumes the active binding of:
- `api-contract-principles.md`
- `schema-reference.md`
- `observatory-models.md`
- `evidence-and-source-provenance.md`
- `data-boundaries.md`
- `system-invariants.md`
- `mcp-surface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`

---

## Out of Scope

This document does not define:

- the exact request and response schema for every route family
- operator-surface rendering of errors
- MCP tool prompt wording or UI copy
- provider-specific transport retry algorithms
- database migration details

Those belong in route-family docs, operator docs, MCP docs, or implementation docs.

---

## System

- veda

---

## Core Rule

VEDA errors must preserve observatory boundaries, project-scope isolation, provenance honesty, and contract consistency.

Errors must be:
- boring
- stable
- non-leaky
- machine-classifiable
- truthful about what went wrong

A response that is friendlier but leaks cross-project existence, blurs malformed input with semantically invalid input, or hides provenance-critical failure is not a better error response. It is a drift vector.

---

## Error Model Definition

VEDA uses a bounded error model so callers can distinguish between:
- malformed requests
- semantically invalid but well-formed input
- missing or out-of-scope resources
- conflicts with current lifecycle or state
- authorization or provider registration failures
- internal or upstream operational failures

This taxonomy exists so route behavior is predictable across families and so downstream tools do not need to reverse-engineer meaning from inconsistent failures.

---

## Stable Error Envelope

All VEDA error responses must use a stable envelope.

### Required shape

```json
{
  "error": {
    "code": "machine_readable_code",
    "message": "Human-readable explanation",
    "details": {},
    "requestId": "optional-correlation-id"
  }
}
```

### Field rules

- `error.code` — required; stable machine-readable code
- `error.message` — required; human-readable explanation
- `error.details` — optional; structured detail for callers when useful and non-leaking
- `error.requestId` — optional; correlation identifier when available

### Envelope rules

- the envelope shape must not vary by route family
- the presence of `details` must not leak information the status code posture forbids
- upstream/provider failures may include bounded operational detail, but must not expose secrets or raw credentials

---

## Primary Status-Code Semantics

VEDA uses the following primary status-code semantics.

## 400 Bad Request
Use when the request is structurally malformed.

Examples:
- missing required body field
- wrong field type
- malformed UUID or identifier
- malformed cursor
- unknown query parameter
- unknown PATCH field
- caller-supplied server-owned field
- immutable field supplied on update

### Rule
400 means the request could not be interpreted as a valid contract-shaped request.
It is not used for semantically invalid but well-formed domain input.

---

## 404 Not Found
Use when the requested resource is absent in the caller’s permitted project scope.

Examples:
- record does not exist
- record exists outside the active project scope
- caller attempts cross-project read or write against a project-scoped resource

### Rule
404 in VEDA is non-leaking.
It must not distinguish between “not found” and “exists but out of scope” when that distinction would leak cross-project existence.

---

## 409 Conflict
Use when the request is structurally valid and domain-valid in the abstract, but conflicts with current resource state, lifecycle posture, or uniqueness rules that are modeled as state conflict rather than semantic invalidity.

Examples:
- attempting to create a record that violates a uniqueness constraint intended to be surfaced as conflict
- attempting to transition or mutate a resource while another bounded state makes the action conflicting rather than semantically nonsensical
- attempting to ingest a duplicate observation in a way the ingest contract defines as conflict rather than accepted idempotency

### Rule
409 is for state conflict, not for general invalid domain data.
If the issue is that the input is domain-invalid even on a fresh resource, use 422 instead.

---

## 422 Unprocessable Entity
Use when the request is well-formed but semantically invalid against VEDA’s domain rules.

Examples:
- controlled-vocabulary violation
- lifecycle invalidity
- invalid derived-output request parameters that break domain rules while remaining structurally well-formed
- invalid provider/source classification value
- provenance rule violation in a route that accepts governed metadata fields
- illegal status transition where the transition is modeled as domain invalidity

### Rule
422 means the request shape is fine, but the requested meaning violates VEDA’s domain rules.

---

## 500 Internal Server Error
Use when VEDA itself fails unexpectedly and no narrower operational classification is appropriate.

Examples:
- unhandled server exception
- serialization failure not caused by caller input
- internal invariant failure

### Rule
500 should be rare and boring.
Do not turn caller mistakes or provider failures into 500 because classification work was skipped.

---

## 502 Bad Gateway
Use when a required upstream provider or transport dependency returns an invalid, failed, or unusable response during governed ingest or upstream-bound operations.

Examples:
- provider returns malformed payload
- provider response cannot be interpreted under the registered integration contract
- upstream dependency fails in a way that makes the request impossible to complete correctly

### Rule
502 is about upstream failure, not VEDA ownership failure.
It should preserve bounded operational truth without exposing provider secrets.

---

## 503 Service Unavailable
Use when a required service is temporarily unavailable and the route cannot complete.

Examples:
- provider temporarily unreachable
- ingest subsystem intentionally unavailable
- VEDA service dependency unavailable in a way expected to be temporary

### Rule
503 is operational unavailability, not malformed or semantically invalid caller input.

---

## Validation Classes

VEDA validation should happen in ordered classes.

## Class 1 — Structural Validation
Checks whether the request matches the contract shape.

Examples:
- required fields present
- field types valid
- identifiers well-formed
- cursor shape valid
- unknown query params rejected
- unknown PATCH fields rejected

### Failure status
400 Bad Request

---

## Class 2 — Scope Validation
Checks whether the request remains inside active project scope and allowed route scope.

Examples:
- record belongs to active project
- project-scoped route not being used cross-project
- route family being used against the correct resource family

### Failure status
404 Not Found for non-leaking scope failure

---

## Class 3 — Ownership and Mutability Validation
Checks whether the caller is trying to set or modify fields or records they are not allowed to control.

Examples:
- server-owned field supplied on create or update
- immutable field supplied on update
- caller attempting write against observation-ledger records through a client route

### Failure status
400 Bad Request when contract shape is violated by forbidden caller-controlled fields

---

## Class 4 — Domain Validation
Checks whether the request is semantically valid within VEDA’s domain rules.

Examples:
- controlled vocabulary values valid
- allowed lifecycle/status values
- provider/source classification valid
- derived-route parameters semantically valid
- route-specific domain constraints satisfied

### Failure status
422 Unprocessable Entity

---

## Class 5 — State and Conflict Validation
Checks whether the request conflicts with current state, uniqueness, or lifecycle posture.

Examples:
- uniqueness conflict on governed records
- state conflict during idempotent or duplicate-sensitive ingest
- conflicting transition request on current record state

### Failure status
409 Conflict when modeled as state conflict
422 when modeled as domain invalidity

### Rule
A route-family spec must choose one posture consistently for comparable cases.
Do not mix 409 and 422 for the same failure class without explicit justification.

---

## Class 6 — Provenance and Evidence Integrity Validation
Checks whether a route that accepts or packages provenance-bearing data preserves required provenance rules.

Examples:
- required provenance field missing in governed ingest context
- source field invalid or inconsistent with registered provider
- payload schema version missing where required by ingest contract
- response-packaging route attempts to suppress required provenance fields

### Failure status
400 when structural provenance fields are malformed or missing from required contract shape
422 when provenance meaning is semantically invalid despite being well-formed
502 when upstream/provider response prevents provenance-safe ingest

---

## Read Route Error Posture

Read routes must be simple and non-leaky.

### Common read failures
- malformed identifiers or cursor → 400
- out-of-scope or absent record → 404
- semantically invalid derived query parameters → 422
- upstream dependency failure on a derived route that depends on live upstream fetch → 502 or 503 depending on posture

### Rule
Canonical observation reads should almost never produce 409.
A read that conflicts with state is usually mis-modeled.

---

## Write Route Error Posture

Write routes must enforce server ownership and bounded mutability aggressively.

### Common write failures
- missing required body field → 400
- unknown PATCH field → 400
- immutable field on update → 400
- server-owned field supplied by caller → 400
- invalid controlled vocabulary value → 422
- illegal status/lifecycle change → 422 or 409 depending on family’s chosen posture
- uniqueness collision → 409 where modeled as conflict
- out-of-scope target record → 404

### Rule
Silent ignore is forbidden.
If the caller attempted to set something forbidden or unknown, the route must fail explicitly.

---

## Ingest Route Error Posture

Ingest routes are special because they operate on observation-ledger truth and provider registration.

### Common ingest failures
- unregistered provider → 422 or 400 depending on whether the contract models provider identity as semantic value or malformed identity field; pick one and keep it consistent per ingest family
- provider credential/auth mismatch → 404 or 403-equivalent posture is out of scope here; if exposed through the API layer, keep it non-leaky and consistent with security posture chosen by implementation
- malformed provider payload → 502 when upstream response is unusable
- temporary provider outage → 503
- duplicate ingest collision → 409 if modeled as conflict
- provenance-critical field absent in upstream response → 502 if upstream failure prevents trustworthy ingest

### Rule
Ingest must fail closed on provenance-critical uncertainty.
If VEDA cannot ingest without preserving source truth honestly, it must not accept the record.

---

## Derived Output Route Error Posture

Derived-output routes must preserve the distinction between malformed requests, invalid derivation requests, and weak or incomplete basis.

### Common derived-route failures
- malformed query inputs → 400
- semantically invalid time range or unsupported derivation mode → 422
- required bounded source records absent in scope → 404 or valid empty result depending on route-family semantics
- insufficient basis for a strong output class → either a valid degraded response with explicit uncertainty or a 422 if the route contract requires minimum basis and that basis is absent

### Rule
Do not use 500 because derivation basis is weak.
Weak basis is usually a modeled domain condition, not an internal server explosion.

---

## Non-Leakage Rule

VEDA must preserve non-leakage on project-scope failures.

This means:
- cross-project read attempts return 404, not helpful hints
- cross-project write attempts against a target record return 404, not confirmation that the record exists elsewhere
- `details` fields must not reveal out-of-scope record identifiers, titles, or existence indicators
- error wording must not vary in a way that allows callers to distinguish absent-in-scope from exists-out-of-scope

A “friendlier” scope failure that leaks existence is incorrect.

---

## Provenance-Critical Failure Rule

Where provenance is required to preserve observatory truth, missing or invalid provenance must block the operation.

Examples:
- missing `source` on ingest
- missing or unusable `capturedAt` when required for observation truth
- provider response that cannot support trustworthy provenance labeling
- route shaping that would strip required provenance from a cross-system signal response

### Rule
Provenance-critical failures must not degrade silently.
If provenance cannot be preserved honestly, the operation must fail or downgrade explicitly according to route contract.

---

## Empty Result vs Error Rule

VEDA must distinguish between:
- a valid query with no results
- an invalid query
- an out-of-scope resource request

### Use valid empty result when:
- the route is a list or search route
- the query is valid
- there are simply no in-scope results

### Use 404 when:
- the route targets a specific resource by identifier
- the resource is absent in scope or out of scope

### Use 422 when:
- the query is semantically invalid even though structurally well-formed

A route family must not switch between empty result and error for the same query pattern without explicit documented reason.

---

## Controlled Vocabulary Failure Rule

When a request supplies a value outside an allowed controlled vocabulary, the failure is semantic, not structural.

### Status
422 Unprocessable Entity

### Examples
- invalid lifecycle state value
- invalid source classification value
- invalid domain enum on a governed route

### Rule
Do not use 400 for controlled vocabulary failure unless the route is literally malformed at the parser level.

---

## Unknown Field and Unknown Parameter Rule

Unknown fields and unknown parameters are contract-shape violations.

### Status
400 Bad Request

### Applies to
- unknown query parameters
- unknown request body fields on create routes
- unknown PATCH fields

### Rule
Unknown input must be rejected, not ignored.
That keeps contracts stable and caller expectations honest.

---

## Immutable and Server-Owned Field Rule

Supplying immutable or server-owned fields in caller-controlled contexts is a contract violation.

### Status
400 Bad Request

### Examples
- caller sets `capturedAt` on a governed client route where the server owns it
- caller attempts to patch immutable `url` on `SourceItem`
- caller supplies `rawPayload` directly through a client write route

### Rule
Do not silently drop forbidden fields.
Explicit failure is required.

---

## Lifecycle and Transition Failure Rule

When a status or lifecycle change is not allowed by VEDA’s domain rules, the route must fail consistently.

### Status
- 422 if modeled as semantic invalidity
- 409 if modeled as current-state conflict

### Rule
Choose one posture per route family and document it.
Do not alternate unpredictably.

---

## Duplicate and Idempotency Rule

Route families that may encounter duplicates must explicitly choose whether the duplicate is:
- a conflict
- an idempotent replay
- a semantically invalid request

### Suggested default posture
- 409 when the same unique governed record would be created twice and the second attempt conflicts with existing state
- success with same canonical result only when the route explicitly supports idempotent replay

### Rule
Do not let duplicate handling become accidental behavior.
It must be documented per family.

---

## Upstream and Provider Failure Rule

When VEDA depends on a provider or upstream service during ingest or governed live-derived operations, failures must be classified honestly.

### Use 502 when:
- upstream returned unusable or invalid response
- upstream payload cannot be interpreted under the governed integration contract

### Use 503 when:
- upstream or dependency is temporarily unavailable
- service outage prevents completion

### Rule
Do not collapse all upstream trouble into 500.
The difference matters operationally.

---

## Error Code Design Rules

`error.code` values should be:
- stable
- machine-readable
- short but specific
- reusable across comparable route families

### Example error codes
- `invalid_uuid`
- `unknown_query_parameter`
- `unknown_patch_field`
- `server_owned_field_supplied`
- `immutable_field_supplied`
- `controlled_value_invalid`
- `resource_not_found`
- `resource_out_of_scope`
- `state_conflict`
- `duplicate_record_conflict`
- `provider_not_registered`
- `provider_payload_invalid`
- `provenance_required`
- `upstream_unavailable`

### Rule
Do not create route-family-specific novelty codes when a shared code already describes the same failure class.

---

## Details Field Rules

`error.details` may be used to help callers fix valid-in-scope problems.

### Allowed uses
- identify which input field failed validation
- list allowed enum values where non-sensitive
- show which query parameter was unknown
- show cursor parsing issue
- explain which immutable field was supplied

### Forbidden uses
- revealing out-of-scope resource existence
- revealing another project’s identifiers or metadata
- exposing provider secrets or credentials
- leaking internal stack traces

### Rule
`details` is for repairability, not gossip.

---

## Hammer Expectations

The VEDA hammer layer should verify at minimum that:
- malformed requests reliably return 400
- controlled vocabulary violations reliably return 422
- cross-project access attempts return non-leaking 404
- unknown PATCH fields are rejected
- immutable fields are rejected on update
- server-owned fields are rejected in caller-controlled routes
- provider registration failures are classified consistently
- provenance-critical failures fail closed
- error envelope shape remains stable across route families

A route that returns the right broad status code but the wrong leakage posture still fails hammer.

---

## Anti-Drift Rules

### 1. No friendly leakage rule
Do not make errors more helpful by leaking cross-project existence.

### 2. No silent ignore rule
Do not ignore unknown, immutable, or server-owned caller input.

### 3. No 500-for-laziness rule
Do not use 500 where a stable caller-meaningful classification exists.

### 4. No provenance-softening rule
Do not accept ingest or package signal when required provenance cannot be preserved honestly.

### 5. No route-family roulette rule
Do not let equivalent validation failures map to different statuses randomly across families.

### 6. No provider-chaos rule
Do not let provider-specific weirdness destabilize the canonical error model.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:
- 400 means malformed contract usage
- 422 means well-formed but semantically invalid domain usage
- 404 is deliberately non-leaking for scope failures
- 409 is for explicit conflict posture, not generic invalidity
- provenance failures matter enough to block operations
- upstream/provider failures should be classified separately from internal failures
- VEDA errors are designed to preserve boundaries, not just developer convenience

If an LLM could use this document to justify leaky scope failures, silent field ignoring, or collapse all weird cases into 500, this taxonomy is failing.

---

## Usage

This document should be used:
- when writing VEDA route-family docs
- when implementing validation layers for VEDA routes
- when deciding 400 vs 404 vs 409 vs 422 posture
- when designing ingest failure handling
- when building hammer verification for VEDA API behavior
- when checking that VEDA preserves observatory and project boundaries in its failures

---

## Related Docs

- `api-contract-principles.md`
- `schema-reference.md`
- `observatory-models.md`
- `evidence-and-source-provenance.md`
- `data-boundaries.md`
- `system-invariants.md`
- `mcp-surface.md`
- `operator-surfaces.md`
- `providers/registry.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/data-boundaries.md`
- `../project-v/api-conventions.md`
