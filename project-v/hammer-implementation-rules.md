# Hammer Implementation Rules

## Purpose

This document defines the governed rules for implementing Project V hammer modules and hammer checks.

It exists to answer:

```text
What does a valid Project V hammer module look like, how must individual checks be structured,
what anti-fake-coverage rules apply, and how must hammer implementation remain aligned with
doctrine, plan, and coverage map?
```

Read this with:

- `hammer-doctrine.md`
- `hammer-plan.md`
- `hammer-coverage-map.md`
- `../governance/testing-and-verification-doctrine.md`
- `schema-specification.md`
- `api-conventions.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `status-transitions.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- what counts as a hammer module
- what counts as a hammer check
- the relationship between this doc and hammer-doctrine, hammer-plan, and hammer-coverage-map
- the relationship between this doc and testing-and-verification-doctrine
- valid-path vs invalid-path implementation rules
- persistence check implementation rules
- contract check implementation rules
- non-leakage check implementation rules
- atomicity check implementation rules
- determinism check implementation rules
- boundary check implementation rules
- mutation-boundary check implementation rules
- concurrency check implementation rules
- multi-project scope-isolation check implementation rules
- server-owned field check implementation rules
- shared vs family-owned coverage rules
- anti-fake-coverage rules
- module naming, scoping, and structure rules
- anti-drift rules

---

## Out of Scope

This document does not define:

- hammer doctrine principles — those belong in `hammer-doctrine.md`
- the phased module plan — that belongs in `hammer-plan.md`
- the invariant-to-module coverage map — that belongs in `hammer-coverage-map.md`
- ecosystem-wide testing and verification philosophy — that belongs in `../governance/testing-and-verification-doctrine.md`
- individual API family contracts — those belong in `project-v/api/`
- implementation code or test runner tooling choices

---

## System

- project-v

---

## Core Rule

Hammer implementation must be authority-derived, not ad hoc QA improvisation.

Every hammer module and every hammer check must trace to a named invariant, a named API family expectation, a named doctrine category, or a concurrency or integration scenario documented in `hammer-plan.md`.

A check that cannot be traced to authority is not a governed hammer check.
A module that cannot be traced to a coverage map entry is not a governed hammer module.

---

## Relationship to Hammer Doctrine

`hammer-doctrine.md` defines what the hammer is, what it must protect, and the design principles every check must follow.

This document defines how those principles must be concretely implemented.

The distinction:

- Doctrine says: "Every important surface must be tested with both valid and invalid use."
- Implementation rules say: what constitutes a valid-path check, what constitutes an invalid-path check, and what is not sufficient to qualify as either.

Implementation rules are subordinate to doctrine. If a rule stated here conflicts with `hammer-doctrine.md`, the doctrine takes precedence and this document must be updated.

---

## Relationship to Hammer Plan

`hammer-plan.md` defines the phased execution plan: which modules must exist, what each phase protects, which concurrency scenarios are required, and which integration scenarios are required.

This document does not add new modules or new phases.

This document defines how modules listed in the plan must be built. If a module listed in `hammer-plan.md` is not built according to these rules, it does not count as real coverage regardless of its presence in the plan.

---

## Relationship to Hammer Coverage Map

`hammer-coverage-map.md` tracks which invariants, API family expectations, and doctrine categories are mapped to which modules, and what the current posture is.

This document defines what posture designations like `V`, `I`, and `V+I` require in concrete implementation terms.

The relationship:

- The coverage map says a check exists at a posture level.
- This document defines what that posture level requires the check to actually do.
- A check that does not satisfy the implementation requirements for its stated posture is an overclaim.

When a new check is implemented, it must satisfy the rules defined here before the coverage map entry may be updated from `—` to a concrete posture.

---

## Relationship to Testing and Verification Doctrine

`../governance/testing-and-verification-doctrine.md` defines the ecosystem-wide hammer doctrine: the three required categories (Persistence, Contract, Boundary), the five principles, and what the hammer is and is not.

Project V's hammer implementation must satisfy that doctrine's category requirements.

Section 0 of `hammer-coverage-map.md` maps the doctrine's three categories to Project V modules. This document defines what the checks in those modules must do to count as real coverage for each category.

---

## What Counts as a Hammer Module

A hammer module is a bounded, independently runnable verification unit that:

1. Declares which invariant(s), API family expectations, or doctrine categories it protects.
2. Has an entry in `hammer-coverage-map.md` that names it explicitly.
3. Has a named module in `hammer-plan.md` that assigns it to a phase.
4. Runs against the real Project V system: real route handlers, real database, real validation.
5. Starts from a known clean state and does not depend on data left by another module.
6. Produces a clear pass or fail result with enough output to classify what failed and why.
7. Can be rerun from a clean state and produce the same result.

A file full of test cases with no coverage map entry is not a hammer module.
A coverage map entry with no corresponding implementation is not a hammer module — it is a planned gap.
A module that depends on another module's fixture data is not a valid hammer module.

---

## What Counts as a Hammer Check

A hammer check is a single bounded assertion within a hammer module that:

1. Targets exactly one behavior or constraint — it does not bundle unrelated assertions.
2. Makes an exact assertion, not a vague one.
3. Is classifiable as either valid-path or invalid-path — not both within a single check. `V+I` coverage requires two distinct checks.
4. Leaves the system in a clean state after it runs, or explicitly documents the state it leaves.
5. Fails with a diagnostic that names the behavior that broke — it does not produce a silent failure.

A check that asserts "something returned 200" is not a valid hammer check.
A check that asserts "the response status is 200 and the response body contains fields X, Y, Z with exact values A, B, C" may be a valid hammer check.
A check that asserts "the route rejected an invalid input" without verifying the rejection status code and error shape is not a valid hammer check.

---

## Valid-Path vs Invalid-Path Implementation Rules

### Valid-path check requirements

A valid-path check must:

- Supply a well-formed, in-scope, governed input.
- Assert the exact response status code expected for success.
- Assert the exact response shape specified in the API family authority doc.
- Assert that the correct record was persisted where persistence is involved.
- Assert that server-owned fields reflect correct server-computed values, not caller-supplied values.
- Not accidentally test invalid behavior by supplying a casually incorrect input.

### Invalid-path check requirements

An invalid-path check must:

- Supply exactly the invalid condition being probed — not a generally messy input.
- Assert the exact rejection status code (`400` or `422` per api-conventions.md rules).
- Assert the error response shape is present and correct.
- Assert that no unintended persistence occurred as a side effect of the rejection.
- Be named or labeled in a way that makes the invalid condition explicit.

### Classification rule

Valid-path checks and invalid-path checks must be deliberately distinguished in implementation.

Do not write a single check that muddles both a valid result and an invalid fallback.
Do not assume a check is invalid-path just because it happens to fail.

If the coverage map marks a row as `V+I`, both a valid-path check and an invalid-path check must exist as distinct checks, not as one check that loosely covers both.

---

## Persistence Check Implementation Rules

A persistence check verifies that database state matches the expected outcome of an operation.

### Minimum requirements

- After a creation operation, query the database directly to confirm the record exists with the correct field values — do not rely on the creation response alone as proof of persistence.
- After a mutation operation, query the database directly to confirm the mutation was applied correctly.
- After a rejected operation, query the database to confirm that no partial write occurred.
- After an atomicity-required operation, verify that all required rows exist — not just the primary row.

### What is not sufficient

- Asserting only on the API response without reading back from the database.
- Asserting that a creation response returned 201 without confirming the row exists with correct values.
- Asserting that a rejection returned 422 without confirming the database remained clean.
- Asserting that all rows exist on the happy-path for a multi-write operation without verifying rollback posture — a persistence check for an atomic operation is not complete unless the rollback case is also verified. See Atomicity Check Implementation Rules for the required rollback verification.

---

## Contract Check Implementation Rules

A contract check verifies that a route behaves as its API family authority doc specifies.

### Minimum requirements

- Assert the exact response status code.
- Assert the exact required fields in the response body.
- Assert that forbidden fields are absent from the response body.
- Assert the exact error body shape and error code when verifying a rejection.
- Assert deterministic ordering for list responses — not just that records are present.
- Assert cursor behavior: `nextCursor` is `null` when results are exhausted, non-null when more exist.
- Assert that unknown PATCH body fields are rejected with `400`, not silently ignored.
- Assert that unknown query parameters on list routes are rejected with `400`, not silently ignored.

### What is not sufficient

- Asserting that a response is "not empty."
- Asserting only the top-level status code without verifying response shape.
- Asserting that a list returned "some records" without verifying count, order, and structure.
- Asserting that a PATCH succeeded without verifying exactly which fields changed.

---

## Non-Leakage Check Implementation Rules

A non-leakage check verifies that out-of-scope resources are not disclosed through any response channel.

### Minimum requirements

- Create resource A in project scope A.
- Attempt to access resource A using a session scoped to project B.
- Assert the response is `404 Not Found`.
- Assert the error body shape does not contain any reference to resource A or its project.
- Assert the response is structurally identical to what would be returned for a genuinely non-existent resource.
- Repeat for each access modality being tested: GET by ID, list with filter, PATCH, status route.

### What is not sufficient

- Asserting only that the response status is not `200`.
- Asserting that a `403 Forbidden` was returned — `403` discloses existence; `404` is the only correct response.
- Asserting that an error was returned without verifying the error body does not leak information.
- Treating a filter that returns zero results as a verified non-leakage probe — an empty list from an ambiguous filter may be leaking silently through a different mechanism.

---

## Atomicity Check Implementation Rules

An atomicity check verifies that a multi-write operation succeeds or fails as a unit with no partial state surviving.

### Minimum requirements

- Identify the complete set of writes that must be atomic for the operation.
- Verify the happy-path case: all writes succeed and all rows exist with correct values.
- Verify the rollback case: force a failure condition after the first write and before later writes complete, then confirm all rows are absent.
- Verify that no partial state can be read from the database after the rollback case.

### Atomicity operations requiring explicit rollback checks

The following are governed atomicity operations in Project V. Each must have a rollback check, not only a happy-path check:

- Status transition + StatusHistory write (all entity types that require StatusHistory)
- ReadinessEvaluation creation + ReadinessGap creation + WorkItem.readinessState update (where entity is WorkItem)
- DecisionRecord supersedence + StatusHistory write
- Handoff transition to `closed` status + `completedAt` set atomically in the same transaction
- AuditRun creation + AuditGap creation + startedAt + completedAt
- AuditRun staleness transition + StatusHistory write

### Rule: Handoff.completedAt null verification is required

The atomicity check for handoffs is two-sided. The check must verify:

- `Handoff.completedAt` is set to a non-null value atomically when status transitions to `closed`
- `Handoff.completedAt` remains `null` on all other status transitions: `proposed → ready`, `ready → handed_off`, `handed_off → accepted`, and reverse re-entry transitions

A check that only verifies the non-null case has not verified atomicity — it has only verified one direction of a two-sided constraint.

### What is not sufficient

- Verifying only the happy-path success and calling it an atomicity check.
- Asserting that a transaction "rolled back" without reading from the database to confirm no partial state exists.
- Simulating rollback at the database engine level alone without verifying the application layer behavior.

---

## Determinism Check Implementation Rules

A determinism check verifies that stable inputs produce stable outputs across repeated executions.

### Minimum requirements

- Supply identical input twice against the same clean state.
- Assert that the output is identical in both runs.
- For list ordering checks: insert records in a non-trivially ordered sequence, then assert the list response uses the governed ordering on each retrieval.
- For readiness evaluation: run the same evaluation twice on the same unchanged entity and assert identical results.

### Determinism surfaces requiring explicit checks

- List ordering for all API families (owned by `hammer-ordering`)
- Readiness evaluation results on the same inputs (owned by `hammer-readiness-reproducibility`)
- Ambiguity detection classification results (owned by `hammer-ambiguity-detection`)

### What is not sufficient

- Asserting that two outputs are "both valid" without asserting they are identical.
- Asserting list ordering only in a trivially ordered case where any ordering strategy would produce the same result.
- Accepting non-determinism as "acceptable variation."

---

## Boundary Check Implementation Rules

A boundary check verifies that Project V does not absorb VEDA observability truth or V Forge execution truth as canonical Project V state.

### Minimum requirements

- Submit a payload that represents the out-of-bounds data category to a Project V write surface.
- Assert the write is rejected at the contract level with the correct error status and shape.
- Assert that no record of the rejected payload appears in the database after rejection.

### Observatory-shaped payload categories to probe

- A payload containing SERP observation data submitted to any Project V creation route.
- A payload containing GA4 signal data submitted to any Project V creation route.
- A payload containing crawl or indexation observation data submitted to any Project V route.

### Execution-shaped payload categories to probe

- A payload containing V Forge draft state submitted to a Project V creation route.
- A payload containing publishing workflow state submitted to a Project V route.
- A payload containing rich execution-progress fields submitted to a Project V work item or handoff route.

### What is not sufficient

- Asserting only that a general malformed payload was rejected.
- Asserting the rejection without naming the boundary being enforced.
- Treating boundary enforcement as equivalent to generic input validation — boundary enforcement targets the system-ownership boundary, not structural malformation.

---

## Concurrency Check Implementation Rules

A concurrency check verifies that Project V enforces uniqueness, constraint, and single-winner invariants when two competing operations target the same resource simultaneously.

### First-pass scope

A first-pass concurrency probe may use two requests designed to stress the same constraint within a single hammer run. This does not require high-fidelity production load simulation. Two sequential requests constructed to target the same constraint are sufficient for first pass, per `hammer-doctrine.md`.

### Minimum requirements

- Execute two competing operations that target the same constraint (same key, same dependency, same evaluation target, same status transition).
- Assert the governed expected outcome, not merely the absence of a server crash:
  - Exactly one operation must succeed where doctrine requires a single winner.
  - The competing operation must be rejected with the correct status code (typically `409 Conflict` for duplicate creation, `422 Unprocessable Entity` for duplicate transition).
- After both requests complete, query the database to verify final persisted state:
  - Exactly one row exists where doctrine requires uniqueness.
  - No duplicate row, no corrupted state, and no partial write from the rejected operation.

### What is not sufficient

- Asserting only on HTTP response codes from both requests without reading the database to confirm the final persisted count and state.
- Asserting "no crash" or "both requests returned a response" without verifying which operation won and that the database reflects exactly one winner.
- Using a non-persisted or fabricated competitor identifier rather than a genuinely concurrent attempt against the same real constraint.

### Required first-pass concurrency scenarios

The following scenarios are required per `hammer-plan.md` and `hammer-coverage-map.md` Section 4. Each must satisfy the minimum requirements above:

- Concurrent project-scoped unique key creation (modules: `hammer-core-projects`, `hammer-core-work-items`)
- Concurrent conflicting status transitions on the same record (module: `hammer-state-transitions`)
- Concurrent duplicate dependency creation (module: `hammer-dependencies`)
- Concurrent duplicate readiness evaluation trigger (module: `hammer-readiness-core`)

**Readiness evaluation race — scenario-specific posture:** Unlike duplicate-creation or duplicate-transition scenarios, the readiness evaluation race does not require that one request be rejected with a `409` or `422`. `ReadinessEvaluation` records are distinct events and are not governed by a uniqueness constraint that mandates rejection of competing requests. The required outcome is that the system does not produce duplicate evaluation records for the same concurrent trigger. The check must verify this by reading the database after both requests complete and confirming that exactly one evaluation record exists for that trigger — not two. If the system serializes or deduplicates internally without returning a rejection code, the check is still valid provided the persisted state is correct. Do not assert a rejection code for this scenario unless a future authority doc explicitly governs one.

---

## Mutation-Boundary Check Implementation Rules

A mutation-boundary check verifies that state changes obey the governed rules in `status-transitions.md` and that PATCH surfaces accept only the governed patchable fields.

### Minimum requirements for status transition checks

- Attempt each forbidden transition listed in `status-transitions.md` for the entity type being tested.
- Assert each forbidden transition returns `422 Unprocessable Entity`.
- Attempt a transition that requires explicit reason with an empty or missing reason field.
- Assert that attempt returns `400 Bad Request`.
- Verify that a `StatusHistory` row is written atomically with the successful transition for entity types that require history.
- Verify that a repeat transition into an already-held status returns `422`.

### Minimum requirements for PATCH boundary checks

- Submit a PATCH body containing fields that are not in the governed patchable field set and assert rejection with `400 Bad Request`.
- Submit a PATCH body containing identity fields or immutable fields and assert rejection with `400 Bad Request`.

### What is not sufficient

- Testing only allowed transitions and assuming forbidden transitions will behave correctly.
- Testing only one forbidden transition per entity type and asserting full mutation-boundary coverage.
- Verifying the transition response without verifying the database state and history row creation.

---

## Multi-Project Scope-Isolation Check Implementation Rules

A scope-isolation check verifies that project boundaries are structurally enforced across all data access paths.

### Minimum requirements

- Create two explicitly separate project contexts in the database: project A and project B.
- Create records in project A.
- Attempt to access project A records from project B context via each access modality being tested.
- Assert `404 Not Found` for each cross-project attempt.
- Assert no cross-project existence leakage through error body, error code, or response shape.
- Attempt to create a cross-project dependency or relationship and assert rejection.

### Rule: Two contexts must be genuinely separate

A scope-isolation check that uses only one project context is not a scope-isolation check.
Both project A and project B must be real created projects in the database.
Using a fabricated or non-persisted project B identifier does not constitute a genuine scope-isolation probe.

### What is not sufficient

- Asserting only that a list filtered by a cross-project entity ID returned zero results.
- Using a UUID that happens not to match any project rather than a genuinely created project B.
- Treating a generic 404 as a verified scope-isolation result without confirming the resource was found under project A.

---

## Server-Owned Field Check Implementation Rules

A server-owned field check verifies that fields whose value must be produced by server-side logic cannot be overridden by callers.

### First-pass server-owned fields requiring checks

- `WorkItem.readinessState` — must not be caller-settable on creation or PATCH
- `ReadinessEvaluation.result` — must not be caller-settable
- `ReadinessEvaluation.summary` — must not be caller-settable
- `AuditRun.result` — must not be caller-settable
- `AuditRun.summary` — must not be caller-settable
- `AuditRun.startedAt` — must not be caller-settable
- `AuditRun.completedAt` — must not be caller-settable
- `Handoff.completedAt` — must not be caller-settable
- `StatusHistory.actor` — must not be caller-settable

### Minimum requirements

- Submit a creation or mutation request that includes a server-owned field in the caller body.
- Assert the request is rejected with `400 Bad Request`.
- Assert the rejection is not silent: the response body must indicate a forbidden field error.

### What is not sufficient

- Asserting that the server-computed value is correct without testing that a caller-supplied value is rejected.
- Asserting that the field does not appear in the response body without testing whether a caller-supplied value was silently ignored.
- Silent ignore is an implementation defect, not a passing check. The caller must receive a `400` error.

---

## Hammer Module Rules

### Rule 1 — Module must be named by bounded concern

Use: `hammer-<bounded-concern>`

Module names must match the names in `hammer-plan.md` exactly. Do not introduce new module names without a corresponding plan and coverage-map update.

### Rule 2 — Module must have clean-state isolation

Each module must start from a known clean state.
Acceptable strategies:

- Truncate relevant tables before the module run.
- Use transaction-wrapped test cases that roll back after each case.

One strategy must be chosen and applied consistently within a module. Mixed isolation strategies within one module are not permitted.

A module must not depend on data created by another module.
A module must not depend on implicit global state.
Fixtures must be created explicitly within the module or its setup step.

### Rule 3 — Module must produce classifiable output

A module run must produce output that makes visible:

- which checks passed
- which checks failed
- what the failure was
- how many checks passed and failed in total

A module that produces silent output is not a valid hammer module.

### Rule 4 — Module must declare what it protects

Each module must make explicit, either in its header or in a companion coverage-map entry:

- the invariant(s) it covers
- the records or routes it touches
- the valid path being verified
- the invalid path being verified
- the exact pass criteria

A module that cannot explain what invariant it is protecting is too vague.

### Rule 5 — Module must not absorb another family's core coverage

A module may include cross-family setup (for example, creating a project to test a work item) but must not own the primary coverage for another family's invariants.

Example: `hammer-readiness-core` may create a WorkItem as a fixture, but it must not own the WorkItem validity checks that belong to `hammer-core-work-items`.

If a check belongs logically to a different module per the coverage map, it must be in that module, not duplicated elsewhere.

---

## Hammer Check Rules

### Rule 1 — Checks must target one behavior

Each check targets exactly one invariant assertion or contract assertion. Do not bundle assertions about different behaviors into one check.

### Rule 2 — Check names must state intent

Check names or labels must identify the surface being tested, the behavior being asserted, and whether it is a valid or invalid path.

Acceptable naming examples:

- "work-item creation with valid input succeeds and persists correct fields"
- "work-item creation with caller-supplied readinessState fails with 400"
- "cross-project work-item fetch returns 404 without leakage"

### Rule 3 — Checks must use exact assertions

Assert exact values, exact status codes, exact field presence or absence. Do not assert "response is valid" or "error occurred."

### Rule 4 — Checks must read from the database where persistence is involved

A check that tests persistence must query the database after the operation to confirm actual state. API response bodies alone are not proof of persistence.

### Rule 5 — Checks must not share mutable state

Checks within a module must not share mutable fixture state in a way where one check's outcome affects another check's result. Either isolate fixture creation per check, or design checks to operate on non-overlapping fixture records.

---

## Required Check Categories

The following categories must be covered per `../governance/testing-and-verification-doctrine.md`.
Section 0 of `hammer-coverage-map.md` maps each category to Project V modules. Each category requires the stated implementation posture.

### Persistence category

Required checks:

- Schema integrity verification for each canonical record family: the tables, columns, and constraints match the expected structure in `schema-specification.md`.
- Migration integrity verification: migrations apply cleanly against a fresh schema and the resulting schema matches `schema-specification.md`. This is distinct from post-migration schema inspection — it verifies the migration execution path itself, not only the end state.
- Atomicity verification for each operation in the governed atomicity list: all writes succeed together or are absent together after failure.
- Rejected-write confirmation: the database remains clean after a rejected creation or mutation.

### Contract category

Required checks:

- Request validation rejects each invalid input type with the correct error code and shape.
- Successful requests return the documented response shape with exact required fields.
- List endpoints return deterministically ordered results per the governed ordering rule.
- Zero-state behavior produces correct response (empty `data` array, not `null`, and `nextCursor` of `null`).
- Cursor pagination continuation is correct: a non-null `nextCursor` produces additional results; a null `nextCursor` does not.

### Boundary category

Required checks:

- Each read-only route remains read-only: a request to a read-only route must not produce any database write.
- Project isolation enforced across every access modality tested.
- Cross-project violation probes return `404 Not Found` with no existence disclosure in any response field.
- Observatory-shaped payloads rejected at Project V write surfaces.
- Execution-shaped payloads rejected at Project V write surfaces.
- Transaction rollback verified under forced failure conditions for each governed atomicity operation.

---

## Shared vs Family-Owned Coverage Rules

### Shared modules

Some coverage naturally applies across all families and is owned by shared modules. These modules own the listed coverage and must not be duplicated in family modules as the primary location:

- `hammer-ordering` — deterministic list ordering across all families
- `hammer-validation` — error-code distinction (`400` vs `422`) across families
- `hammer-contracts-read` — read-route shape, non-leakage posture, and zero-state behavior across families
- `hammer-contracts-write` — write-route forbidden-field and server-owned-field posture across families
- `hammer-scope-isolation` — cross-project isolation probes across families

### Family-owned modules

Each API family module owns the primary coverage for its specific record type:

- Creation with valid input and persistence verification
- Duplicate rejection specific to that record type
- Same-project relationship validation specific to that record type
- Record-type-specific invariants listed in `hammer-coverage-map.md` for that module

### Rule: No silent absorption of family coverage

A shared module must not quietly assume ownership of a family-specific check just because the check happens to be exercised in a shared context.

If a check belongs to a family module per the coverage map, it must exist in that module.
If a check belongs to a shared module per the coverage map, it must not be duplicated as the primary coverage location elsewhere.

---

## Anti-Fake-Coverage Rules

Fake coverage is any condition where a check nominally exists but does not actually verify what it claims to verify.

### Rule 1 — A module entry in the plan does not equal real coverage

A module listed in `hammer-plan.md` assigned a `—` posture in `hammer-coverage-map.md` has no coverage. Coverage exists only when a check satisfying the requirements in this document is implemented and passing.

### Rule 2 — A check is not valid merely because it hits a route once

A check that calls a route and asserts a non-error response does not constitute coverage. Coverage requires exact status code, exact response shape, and database verification where persistence is involved.

### Rule 3 — Partial coverage must not be declared complete

If a row in the coverage map requires `V+I` posture:

- And only a valid-path check exists, the posture must remain `V`.
- And only an invalid-path check exists, the posture must remain `I`.
- `V+I` must not be declared until both a valid-path check and an invalid-path check exist and satisfy their respective implementation requirements.

### Rule 4 — Non-leakage checks must verify absence of disclosure

A non-leakage check is not valid if it asserts only that an error was returned. It must assert that the error body contains no cross-project information and that the response structure is indistinguishable from a genuine not-found response.

### Rule 5 — Atomicity checks must verify rollback posture

An atomicity check is not valid if it asserts only the happy-path success. It must include a forced-failure scenario that verifies no partial state survives in the database.

### Rule 6 — Determinism checks must verify repeated-input consistency

A determinism check is not valid if it runs a process once and asserts the result. It must run the same process twice and assert that outputs are identical.

### Rule 7 — Boundary checks must verify rejection and database cleanliness

A boundary check is not valid if it asserts only that a payload was rejected. It must also confirm that no trace of the rejected payload exists in the database after the rejection.

### Rule 8 — Unimplemented coverage must remain visible

Do not promote a coverage map entry from `—` to a posture designation until the check satisfying the implementation requirements exists and passes. A stale coverage map that claims coverage where none exists is a governance failure.

---

## Anti-Drift Rules

### Rule 1 — Hammer checks must not invent invariants

Hammer checks must verify invariants and API family expectations stated in authority docs. Do not write checks for behaviors not documented in `system-invariants.md`, `api-conventions.md`, the API family docs, or `status-transitions.md`.

### Rule 2 — New checks must be mapped before being counted

A new check added to a hammer module must have a corresponding coverage map entry before it can be counted as coverage. Adding a check without updating the coverage map produces invisible, uncounted coverage.

### Rule 3 — Retired or renamed modules must be removed from the coverage map

If a module is retired or renamed, its entries in `hammer-coverage-map.md` must be updated in the same session. Stale module names in the coverage map create false confidence.

### Rule 4 — New API family docs require coverage map updates

When a new API family authority doc is admitted, its hammer expectations must be added to the coverage map immediately. Hammer expectations that appear in API family docs but have no coverage map entry are invisible gaps.

### Rule 5 — Hammer implementation must not outrun schema authority

Hammer checks must test only fields and behaviors defined in `schema-specification.md` and the API family authority docs. Checks that probe fields or behaviors not yet governed are not valid hammer checks.

---

## Hammer Enforcement Gate

This document operates under the **Hammer Enforcement Gate** defined in `hammer-doctrine.md`.

Hammer must pass before any of the following are considered ready:

- **schema changes** — any addition, removal, or modification to the Project V schema
- **API changes** — any new endpoint family, new route, or change to an existing contract
- **evaluation logic changes** — any modification to how readiness is evaluated, how gaps are recorded, or how audit results constrain planning state

This is a policy requirement, not a suggestion. If hammer cannot pass after a proposed change, the change is not ready. If hammer coverage does not exist for the area being changed, adding that coverage is part of the work.

The gate applies to both valid-path and invalid-path coverage. A change that adds a capability but only adds happy-path hammer coverage has not cleared the gate.

---

## Final Rule

A hammer module that does not satisfy the rules in this document is not providing coverage, regardless of how it is labeled.

A Project V surface is not hardened by the presence of a hammer module name.
A Project V surface is hardened when the implemented checks in that module satisfy the requirements in this document and are passing against the real system.

---

## Usage

This document should be used:

- when writing or reviewing a new hammer module
- when deciding whether an existing check satisfies its claimed posture level
- when updating the coverage map posture from `—` to a concrete posture
- when investigating whether a hammer module provides genuine coverage or fake coverage
- when reviewing whether a proposed check tests the right thing at the right level of precision

---

## Related Docs

- `hammer-doctrine.md`
- `hammer-plan.md`
- `hammer-coverage-map.md`
- `system-invariants.md`
- `schema-specification.md`
- `api-conventions.md`
- `status-transitions.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `polymorphic-reference-enforcement.md`
- `data-boundaries.md`
- `../governance/testing-and-verification-doctrine.md`
- `project-v/api/work-items.md`
- `project-v/api/dependencies.md`
- `project-v/api/handoffs.md`
- `project-v/api/readiness.md`
- `project-v/api/audits.md`
- `project-v/api/evidence-links.md`
