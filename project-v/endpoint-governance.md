# Endpoint Governance

## Purpose

This document defines the rules for adding, modifying, constraining, and reviewing Project V endpoints and endpoint families.

It exists to answer:

```text
How does the Project V API surface grow, stay consistent, stay bounded, and stay honest about ownership without depending on memory, habit, or improvisation?
```

Read this with:

- `api-conventions.md`
- `schema-specification.md`
- `schema-governance.md`
- `controlled-vocabularies.md`
- `status-transitions.md`
- `polymorphic-reference-enforcement.md`
- `multi-project-doctrine.md`
- `data-boundaries.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- why endpoint governance exists
- what counts as an endpoint family vs a one-off route
- what must exist before a new endpoint or family is admitted
- the relationship between endpoint admission and schema authority
- the relationship between endpoint admission and controlled vocabulary
- the relationship between endpoint admission and status-transition authority
- the relationship between endpoint admission and polymorphic reference governance
- rules for introducing new mutation routes
- rules for introducing list filters
- rules for status routes vs bounded PATCH
- rules for server-owned vs caller-supplied fields
- non-leakage and project-scoping requirements
- how to decide whether a route belongs in Project V vs another system
- review posture for endpoint expansion
- anti-drift rules
- non-goals

---

## Out of Scope

This document does not define:

- shared API contract rules across route families (see `api-conventions.md`)
- schema column types or mutation posture (see `schema-specification.md`)
- controlled vocabulary values (see `controlled-vocabularies.md`)
- status transition tables (see `status-transitions.md`)
- polymorphic resolution mechanics (see `polymorphic-reference-enforcement.md`)
- individual endpoint family contracts (see `project-v/api/`)
- MCP tool surface contracts (see `mcp-surface.md`)
- hammer coverage planning (see `hammer-plan.md`, `hammer-coverage-map.md`)

---

## System

- project-v

---

## Core Rule

Project V endpoints must be justified by planning and orchestration truth.

Endpoints grow from schema authority and domain need, not from feature requests, convenience shortcuts, or implementation momentum.

If a proposed route cannot be grounded in a canonical schema record, a clear planning-side purpose, and a specific operator or LLM need that cannot be served by existing routes, it is not ready to be admitted.

---

## Why Endpoint Governance Exists

The Project V API surface is not static, but growth without discipline creates drift that compounds.

Without explicit endpoint governance:
- mutation surfaces creep beyond what schema authority supports
- filter proliferation makes behavior harder to predict and test
- one-off convenience routes undermine family consistency
- server-owned fields become caller-settable through overlooked edge cases
- non-leakage posture weakens unevenly across families
- routes appear that properly belong in VEDA or V Forge

Endpoint governance exists to prevent these failure modes from accumulating silently.

---

## Endpoint Family vs One-Off Route

### Endpoint family
A coherent set of routes that together represent the full first-pass API contract for a governed Project V canonical record type.

An endpoint family:
- is grounded in one canonical schema record from `schema-specification.md`
- has a named authority doc in `project-v/api/`
- defines all supported routes, request shapes, response shapes, ordering, filtering, validation, error posture, non-leakage, and hammer expectations in that doc
- follows `api-conventions.md` for all cross-family contract rules
- must be admitted through the full endpoint admission gate before it is built

### One-off route
A route that does not constitute a new endpoint family but adds a bounded action to an existing family.

Examples:
- adding a staleness route to an existing audit family
- adding a sub-resource list route to an existing evaluation family
- adding a reverse-lookup filter to an existing list route

One-off route additions satisfy the authority-doc requirement by updating the existing family authority doc rather than creating a new one. They still must satisfy all applicable gate conditions for any new schema, vocabulary, transition, or polymorphic implications they introduce. See the Endpoint Admission Gate section.

### Rule
A record family that is merely similar to another family is not an extension of that family.
If a distinct canonical schema record requires a distinct set of routes, it requires a distinct endpoint family authority doc.

---

## Endpoint Admission Gate

A new endpoint family is not ready to be implemented until all of the following are true, evaluated in this order.

### Gate condition 1 — Schema authority exists

The canonical record the family governs must already exist in `schema-specification.md`.

A proposed endpoint family for a record that is not yet in `schema-specification.md` must not proceed until the schema is governed and documented first.

The endpoint docs must not outrun schema authority.

### Gate condition 2 — Controlled vocabulary is governed

All controlled-vocabulary fields used by the family must already exist in `controlled-vocabularies.md`.

A family must not invent new vocabulary values locally. If new values are needed, update `controlled-vocabularies.md` first through the vocabulary change process defined there.

### Gate condition 3 — Status transitions are governed

If the family includes status routes or governed lifecycle transitions, all allowed and forbidden transitions must already be defined in `status-transitions.md`.

A family must not define its own lifecycle transition tables. If new transitions are needed, update `status-transitions.md` first.

### Gate condition 4 — Polymorphic types are governed

If the family uses polymorphic references, all allowed entity types for that record must already be defined in `polymorphic-reference-enforcement.md`.

A family must not invent local polymorphic entity type sets.

### Gate condition 5 — Ownership boundary is clear

The record type the family governs must belong to Project V as planning or orchestration truth.

It must not model VEDA observability truth, V Forge execution truth, or thin references that properly belong in `ExternalLink` rather than a full record family.

Before admission, answer explicitly:
- does this record represent planning truth that Project V owns canonically?
- does it belong in Project V and not in VEDA, V Forge, or another bounded system?

If the answer is ambiguous, the family is not ready.

### Gate condition 6 — No existing route or family already serves the need

Before drafting a new family authority doc, verify that the need cannot be served by:
- an existing endpoint family's list filter
- an existing endpoint family's PATCH route
- a sub-resource route on an existing family
- a cross-family query composed by the caller

If the need can already be served, add no new surface.

This check comes before drafting a new authority doc deliberately: there is no point committing to a new doc only to discover afterward that the need was already covered.

### Gate condition 7 — Authority doc requirement is satisfied

For a new endpoint family: a full first-pass authority doc must be written for `project-v/api/{family}.md` before implementation begins. That doc must cover all routes, request and response shapes, ordering, filtering, validation, error posture, non-leakage, server-owned field posture, and hammer expectations.

For a one-off route addition to an existing family: the existing family authority doc must be updated to reflect the addition before implementation begins.

Implementation must not proceed from an outline or informal description in either case.

---

## One-Off Route Additions and the Gate

One-off additions within an existing family follow the same gate logic as new families for any new schema, vocabulary, transition, or polymorphic implications they introduce.

Specifically:
- if the addition touches a field not yet in `schema-specification.md` for that record, gate condition 1 applies
- if the addition uses a new controlled-vocabulary value, gate condition 2 applies
- if the addition introduces a new status transition, gate condition 3 applies
- if the addition uses a new polymorphic entity type, gate condition 4 applies
- if the addition widens the ownership surface, gate condition 5 applies
- gate condition 6 (redundancy check) always applies
- gate condition 7 is satisfied by updating the existing family authority doc, not by creating a new one

One-off additions that touch none of gates 1–5 still require the redundancy check and a doc update before implementation.

---

## New Mutation Route Rules

Mutation routes include: `POST` for creation, `PATCH` for field updates, `POST /{id}/status` for governed transitions, purpose-specific routes such as `POST /{id}/stale`, and any other route that writes or updates records.

### Rule 1 — Mutation must be grounded in schema authority
Every field a mutation route accepts or modifies must exist in the canonical schema for that record. No mutation route may modify fields that are not in `schema-specification.md`.

### Rule 2 — Server-owned fields must not be caller-settable
Fields whose value is produced by server-side logic must be excluded from all caller-supplied inputs.

First-pass examples: `result` on evaluations, `summary` on evaluations and audits, `readinessState` on work items, `completedAt` on handoffs, `actor` on status history, `startedAt` and `completedAt` on audit runs.

A caller supplying a server-owned field must fail with `400 Bad Request`. Silent ignore is not allowed.

### Rule 3 — Unknown fields in mutation bodies must be rejected
Every PATCH route must reject unknown body fields with `400 Bad Request`.
Creation routes must reject forbidden fields with `400 Bad Request`.
Silent ignore of unknown or forbidden fields is not allowed on any mutation route.

### Rule 4 — Mutation scope must be bounded and justified
Do not create mutation surfaces that accept arbitrary sets of fields just because they are convenient to expose. Mutation scope must be the minimum needed to support governed behavior.

A creation route that accepts every field on a record is usually wrong. Most fields on most records are server-owned, defaulted, or governed through explicit transition routes.

### Rule 5 — Cross-project mutation is forbidden
No mutation route may write to records outside the current governed project scope.
Project scope is resolved from session context. Caller-supplied scope values must be validated against session context.
A project-scope mismatch must fail without cross-project existence leakage.

### Rule 6 — Immutable fields must not be patchable
Fields defined as immutable after creation in the canonical record family must not appear in any PATCH surface.
If an immutable field is supplied in a PATCH body, the route must fail with `400 Bad Request`.

---

## List and Filter Route Rules

### Rule 1 — Only governed query parameters
Every list endpoint must define an explicit whitelist of allowed query parameters.
Unknown query parameters must fail with `400 Bad Request`. Silent ignore is not allowed.

### Rule 2 — No implicit cross-project leakage through filters
When filtering by entity IDs, parent IDs, or polymorphic references, non-matching results must return an empty result set rather than a cross-project existence disclosure.

A filter that does not match anything in current project scope must return an empty `data` array, not a `404` or an error that reveals whether the referenced entity exists in another project.

### Rule 3 — Deterministic ordering is mandatory
Every list endpoint must define explicit ordering that includes a stable tie-breaker.
No endpoint may rely on implicit database ordering.

### Rule 4 — Cursor pagination is the default
First-pass list endpoints must use cursor pagination unless the family contract explicitly justifies a no-pagination exception with a stated rationale.
Offset pagination is not allowed.

### Rule 5 — Filter proliferation requires justification
Adding a new query parameter to an existing list endpoint requires:
- a clear operator or LLM use case that cannot be served by existing filters
- an explicitly governed parameter type: a controlled-vocabulary value, a valid UUID, a boolean, or another explicitly named scalar type — open-ended string filters without type governance are not allowed
- explicit non-leakage behavior defined for the new filter
- a doc update to the owning family authority file

Do not add filters speculatively or to cover hypothetical future needs.

---

## Status Route vs Bounded PATCH Rules

Project V has two distinct mutation patterns for record fields:

**Status route** (`POST /{id}/status` or purpose-specific equivalent):
- for governed lifecycle transitions that require `StatusHistory`, actor attribution, or explicit reason tracking
- for transitions where moving from one status to another is a governed event that must be auditable and recoverable
- for transitions with legal/forbidden rules defined in `status-transitions.md`

**Bounded PATCH** (`PATCH /{id}`):
- for field updates that do not carry lifecycle semantics
- for updates where no `StatusHistory` row is required
- for nullable fields that may be updated or cleared without lifecycle consequence

### Rule — Use the right surface
Do not use a PATCH route to handle what is actually a governed lifecycle transition.
Do not use a status route for simple field updates that carry no lifecycle history requirement.

The deciding question: does the mutation need to be traceable through `StatusHistory` and does it follow transition rules in `status-transitions.md`?

If yes: use a status route.
If no: a bounded PATCH is sufficient.

Mixed posture — where a PATCH route secretly changes status through a field update — is explicitly forbidden.

---

## Non-Leakage Requirement

Every Project V route must preserve non-leakage posture.

This means:

- a resource that exists in another project must return `404 Not Found`, not a cross-project-aware error
- error body shape must not reveal whether the resource exists elsewhere
- filter results must not imply the existence of out-of-scope resources
- referenced entity validation failures for out-of-scope entities must be indistinguishable from genuinely absent entities

Non-leakage is not optional and is not a quality-of-life enhancement. It is a first-class requirement for every route in every family.

Where a family doc does not explicitly state non-leakage posture for a given route, the default posture from `api-conventions.md` applies. Absence of an explicit exception means `404 Not Found` for out-of-scope resources.

---

## Project Scoping Requirement

Every Project V route that operates on project-scoped records must resolve project scope from the governed session/auth context.

Project scope must not be trusted from caller-supplied body fields alone.
Where `projectId` appears in a creation body, it must still be validated against the governed session scope.

Routes must not accept requests that would operate across project scope without explicit governed multi-project posture.

See `multi-project-doctrine.md` for portfolio-level planning posture.

---

## Ownership Boundary Rules

### Rule 1 — Routes must not model another system's truth
A Project V route must not return, accept, or mutate data that belongs canonically to VEDA or V Forge.

Planning-side references to external systems are allowed (e.g. `EvidenceLink.targetLocator`, `ExternalLink.url`).
Owning the referenced content is not allowed.

### Rule 2 — Routes must not validate external existence
Project V routes must not make outbound calls to validate that a referenced external resource resolves, exists, or is reachable.

External reference validation would turn Project V into a client or proxy for other systems and violates boundary posture. See `api-conventions.md` External Reference Validation Rule.

### Rule 3 — Routes must not replicate another system's state
A Project V route must not accept, store, or return execution state owned by V Forge, observability state owned by VEDA, or any rich cross-system state model that makes Project V behave as a shadow system.

### Rule 4 — If a route feels like it belongs in VEDA or V Forge, it probably does
If the primary function of a proposed route is to record observations, track execution progress, or manage editorial workflow, it does not belong in Project V.

---

## Endpoint Expansion Review Posture

### What requires explicit review before admission
- any new endpoint family
- any new route added to an existing family that extends the mutation surface
- any new filter that involves a new entity type reference
- any change to an existing family's ordering rule
- any change to which fields are server-owned vs caller-supplied

### What does not require new review
- routine implementation of a family that has already been admitted through a full authority doc
- hammer test additions or updates
- doc clarifications that do not change route contract behavior

### How review happens and who approves

The human operator (Chaz) is the approval authority for new endpoint family admission and for any major expansion of an existing family's mutation or filter surface.

The review artifact is the family authority doc. For a new family, that means the full `project-v/api/{family}.md` doc. For a one-off addition, that means the updated version of the existing family doc. Review is complete when the authority doc is finalized and approved, not when implementation is complete.

A family authority doc is not finalized until all of the following sections are explicitly present and complete:
- ownership boundary (what the family owns and does not own)
- server-owned vs caller-supplied field posture
- non-leakage behavior per route
- route and mutation posture (all supported routes with request/response shapes)
- hammer expectations

A doc that is missing any of these sections is a draft, not a finalized authority doc. Implementation must not proceed against a draft.

---

## Invariants

1. No endpoint family may be implemented before its gate conditions are all satisfied.
2. No mutation route may modify fields that are not in `schema-specification.md` for the canonical record it governs.
3. No mutation route may accept server-owned fields from callers; doing so must fail with `400 Bad Request`.
4. No mutation route may silently ignore unknown body fields; all unknown fields must fail with `400 Bad Request`.
5. No list route may silently ignore unknown query parameters; all must fail with `400 Bad Request`.
6. No route may leak cross-project existence through response shape, error message, or filter behavior.
7. No vocabulary value may be introduced locally in a family doc; all values must come from `controlled-vocabularies.md`.
8. No status path may be defined locally in a family doc; all lifecycle transitions must come from `status-transitions.md`.
9. No polymorphic entity type set may be defined locally in a family doc; all sets come from `polymorphic-reference-enforcement.md`.
10. Every list route must have deterministic ordering with an explicit stable tie-breaker.

---

## Anti-Drift Rules

### Do not add routes to serve one-time needs
If a use case appears once and will not recur, it likely does not warrant a permanent route surface. Look for existing routes that can be composed to serve it.

### Do not add convenience mutation shortcuts
Routes that collapse multiple governed actions into one undocumented shortcut erode contract clarity. Each mutation surface must be explicit about what it does and what it does not do.

### Do not let route count substitute for route quality
More routes does not mean better API coverage. Duplicate, overlapping, or vaguely-scoped routes make the surface harder to test, harder to reason about, and harder to govern.

### Do not let a new feature need drive schema or vocabulary expansion
If implementing a route requires new schema or new vocabulary, those changes must be governed first. The implementation sequence is: govern schema → govern vocabulary → govern transitions → write family authority doc → implement.

### Do not use JSON fields to escape contract clarity
Route bodies must use typed, explicit fields. JSON payloads that hold untyped heterogeneous data are not a substitute for explicit request shape design.

### Do not let PATCH become a general update surface
PATCH routes must accept only the specific fields that are caller-settable and non-identity. If the list of patchable fields grows beyond the fields that are genuinely bounded field updates, the surface has drifted.

---

## Non-Goals

This document does not:

- define the full set of routes that Project V will eventually have
- guarantee that the current first-pass API families are complete or final
- prevent future new families from being admitted through proper governance
- govern VEDA or V Forge endpoint surfaces
- govern MCP tool surface contracts
- govern the VSCode extension's operator-facing surfaces
- replace the individual family authority docs in `project-v/api/`

---

## Human-In-The-Loop Principle

Endpoint admission affects what operators and LLMs can do with Project V.

Human review and approval by the human operator is especially important when:

- a proposed route would widen mutation scope
- a proposed route would accept fields previously classified as server-owned
- a proposed family would overlap with a record or behavior owned by another system
- a proposed filter would extend query capabilities in ways that could weaken non-leakage posture
- a proposed change to an existing family would alter server-owned field classification or ordering behavior

The human operator's approval is the gate. A finalized authority doc without human operator approval is not an admitted surface.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:

- endpoint families must be grounded in schema authority, not invented from convenience
- all seven gate conditions must be satisfied in order before a new family is implemented
- the redundancy check (gate condition 6) comes before committing to a new authority doc (gate condition 7)
- one-off additions within an existing family follow the same gate logic for any new schema/vocabulary/transition/polymorphic implications, but satisfy the authority-doc condition by updating the existing doc
- mutation surfaces must be minimal, explicit, and bounded to schema
- server-owned fields must never be caller-settable
- unknown fields and unknown query params must always be rejected, not ignored
- non-leakage and project scoping are non-negotiable requirements on every route
- vocabulary, status transitions, and polymorphic type sets must come from shared authority docs, never from local family invention
- the authority doc for a family is the review artifact; implementation without a finalized and human-approved doc is ungoverned

If a proposed route requires inventing schema, inventing vocabulary, inventing status paths, or blurring ownership with VEDA or V Forge, that proposal is not ready.

---

## Usage

This document should be used:

- when proposing a new endpoint family
- when proposing a new route within an existing family
- when reviewing whether a proposed filter or mutation surface is justified
- when checking whether implementation has outrun schema or vocabulary authority
- when reviewing whether a route correctly preserves non-leakage, project-scoping, and server-owned field posture
- when deciding whether a new mutation need should use a status route or a bounded PATCH

---

## Related Docs

- `api-conventions.md`
- `schema-specification.md`
- `schema-authority.md`
- `schema-governance.md`
- `controlled-vocabularies.md`
- `status-transitions.md`
- `polymorphic-reference-enforcement.md`
- `multi-project-doctrine.md`
- `data-boundaries.md`
- `system-invariants.md`
- `mcp-surface.md`
- `hammer-doctrine.md`
- `hammer-plan.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
