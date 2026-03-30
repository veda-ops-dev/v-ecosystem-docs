# Testing and Verification Doctrine

## Purpose

This document defines the testing and verification doctrine for the V Ecosystem.

It exists to answer:

```text
What must every system in the V Ecosystem verify about itself, how must that verification work, and what principles govern the hammer layer that makes invariant verification real rather than merely declared?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the ecosystem-wide testing and verification philosophy
- the hammer doctrine as universal ecosystem law
- what every system must verify
- the three categories of hammer verification
- what the hammer is and is not
- how the hammer adapts to each system's specific surfaces and invariants

---

## Out of Scope

This document does not define:

- the specific hammer modules for each system
- provider-specific verification mechanics
- unit test frameworks or code coverage requirements
- CI/CD pipeline implementation
- performance or load testing

Those belong in system-specific implementation docs and testing runbooks.

---

## System

- governance

---

## Core Rule

A declared invariant that is not verified is weak architecture.

Every system in the V Ecosystem must implement a hammer layer that verifies its invariants hold under real execution.

The hammer is not optional.
The hammer is not a unit test suite.
The hammer is not a code coverage metric.
The hammer is an invariant and boundary verification system that runs against a live system and confirms that what the docs say the system does is actually what the system does.

---

## The Hammer Doctrine

The hammer doctrine was established in VEDA and has been elevated to ecosystem-wide law.

The core principle is:

> Verify that system invariants hold under realistic execution.

A system may look correct at the code level while violating its invariants in practice. The hammer catches that. Schema assumptions may look correct in migration files while failing under real data shapes. The hammer catches that. Project isolation may be declared in docs while leaking across boundaries in API responses. The hammer catches that.

The hammer exists because declarations are not enough. Verification is required.

---

## What the Hammer Is

The hammer is an integration and invariant test layer.

It verifies:

- routes and API endpoints behave correctly against a running system
- request validation rejects invalid input as documented
- successful requests return stable, contract-compliant response shapes
- project-scoped isolation is enforced — no cross-project data leakage
- read-only surfaces do not perform hidden writes
- write operations are atomic where atomicity is required
- persistence and schema assumptions hold under real execution
- event logging occurs where it is required
- transaction rollback behavior works correctly

The hammer runs against a real running system with real execution paths.
It does not mock the things it is trying to verify.

---

## What the Hammer Is Not

The hammer is not:

- a unit test suite — unit tests test individual functions, the hammer tests system invariants
- a code coverage tool — the hammer targets invariants, not coverage percentages
- a style or refactor enforcement mechanism
- a place to test every helper function because it exists
- a performance benchmark
- optional

Code quality may improve as a side effect of hammer work.
That is not the hammer's mission.

---

## The Three Hammer Categories

Every system's hammer must cover at least these three categories. Each category targets a different class of invariant.

### Category 1 — Persistence Hammer
Verifies that persistence assumptions hold under real execution.

Must verify:
- schema integrity — tables, columns, and constraints match expected structure
- migration integrity — migrations apply cleanly and produce the expected schema
- no unexpected write side effects — operations that should be read-only do not write
- atomicity — multi-write operations succeed or fail as a unit, never partially

### Category 2 — Contract Hammer
Verifies that API contracts behave as documented.

Must verify:
- request validation rejects invalid input with the documented error shape
- successful requests return the documented response shape
- list endpoints use deterministic ordering with stable tie-breakers
- zero-state behavior (empty results, missing records) is handled correctly and explicitly
- pagination, filtering, and sorting behave as documented

### Category 3 — Boundary Hammer
Verifies that system and project boundaries hold under real execution.

Must verify:
- read-only routes remain read-only — no hidden writes
- project isolation is enforced — data from one project cannot be read or written by another project's session
- cross-project violation probes fail — explicit attempts to access another project's data must return 404, not 403 or a descriptive error
- system ownership boundaries hold — a system does not silently absorb another system's truth domain through convenience shortcuts
- transaction rollback works — rollback behavior for multi-write mutations must be tested, not assumed

---

## The Five Hammer Principles

### Principle 1 — Invariants First
Hammer coverage must prioritize structural truths over implementation trivia.

The hammer should answer questions like:
- does this route stay read-only when it is supposed to be read-only?
- does this write remain atomic?
- does project isolation hold when directly tested?
- does invalid input get rejected correctly?

Not questions like:
- does this helper function return the right type?
- does this variable have the right name?

### Principle 2 — Real Execution Over Mock Theater
The hammer exercises live routes and realistic system state whenever possible.

A hammer that mocks the things it is trying to verify is not a hammer. It is confidence theater.
Where real execution is not possible in a test environment, the reason must be explicit and the gap must be documented.

### Principle 3 — Exact Contract Beats Vibes
A useful hammer assertion is precise.

Good assertions:
- exact required fields in response
- exact absent fields
- exact meta fields
- exact deterministic ordering
- explicit zero-state behavior (empty list returns empty array, not null)

Bad assertions:
- "field exists somewhere in the response"
- "status code is 2xx"
- "response is not empty"

### Principle 4 — Route Intent Must Remain Visible
A hammer module should make the route's purpose legible.

If a route is observability-only, the hammer must explicitly protect that property by probing for hidden writes.
If a route enforces project isolation, the hammer must explicitly test cross-project access and confirm it fails.
The hammer is documentation of what the system actually does, not just what it says it does.

### Principle 5 — Boring Structure Wins
Hammer modules should be organized by contract concern, not by file growth.

When a hammer file becomes too large to reason about safely, split it into focused modules.
A thin coordinator may compose the modules.
The modules stay organized by concern: persistence, contract, boundary.

---

## System-Specific Hammer Adaptation

Every system implements its own hammer adapted to its specific invariants and surfaces. The doctrine is universal. The specifics are per-system.

### VEDA Hammer
VEDA's hammer must verify:

- observatory routes stay read-only — no mutations on GET endpoints
- project isolation holds across all observatory domains
- observation records are append-friendly — existing records are not silently overwritten
- event logging is atomic with state changes
- search intelligence surfaces remain derived, not sovereign

### Project V Hammer
Project V's hammer must verify:

- planning truth is project-scoped and isolated
- BYDA audit runs are correctly scoped and scored
- lifecycle transitions enforce the correct state machine
- decision continuity records are preserved correctly
- handoff packages are correctly structured and scoped
- approval posture is enforced before state-sensitive transitions
- cross-project planning state does not bleed

### V Forge Hammer
V Forge's hammer must verify:

- content graph records are project-scoped and isolated
- cross-project content graph junctions are structurally impossible — no page, topic, entity, or link may connect across project boundaries
- cross-project content graph contamination is impossible at the database constraint level
- execution records are correctly scoped
- return-to-planning packages are correctly structured
- scope boundaries hold during execution — out-of-scope actions are rejected
- external action governance routes enforce the correct approval posture

---

## Cross-Project Violation Probes Are Required

Every system's hammer must include explicit cross-project violation probes.

A cross-project violation probe:
- creates or uses data belonging to Project A
- attempts to access that data using a session scoped to Project B
- confirms the attempt returns 404 — not 403, not an error with descriptive content, 404

This must be tested, not assumed.

A system that claims project isolation without hammer-verified cross-project probes has declared an invariant it has not proven.

---

## Transaction Rollback Testing Is Required

Where a system performs multi-write mutations, rollback behavior must be tested.

Testing rollback means:
- forcing a failure condition after the first write and before subsequent writes complete
- confirming that all writes are rolled back, not just the failed write
- confirming that no partial state exists after rollback
- confirming that no event log entries exist for writes that were rolled back

Atomicity claims are not enough.
Rollback behavior must be verified under real failure conditions.

---

## Hammer Failure Means the System Is Not Safe

If the hammer fails, the system is not safe for production use.

A failing hammer test is not a minor CI inconvenience.
It means a declared invariant is not holding under real execution.
That is an architectural problem, not a test configuration problem.

The correct response to a failing hammer test is:
1. Stop — do not deploy or merge
2. Understand why the invariant is not holding
3. Fix the system behavior or correct the invariant if it was wrong
4. Confirm the hammer passes before proceeding

Suppressing hammer failures to unblock a release is a governance failure.

---

## Hammer Coverage Growth Rule

The hammer is a living verification layer.

When new capabilities are added to a system, the hammer must grow to cover the new invariants.
When a bug is found that violated an invariant, a hammer test must be added to prevent regression.
When a new external provider integration is added, the hammer must cover its ingest correctness and project isolation.

The hammer does not stay the same size as the system grows.

---

## Human-In-The-Loop Principle

Hammer verification supports human governance by making system behavior verifiable rather than declarative.

When an operator or LLM says a system behaves correctly, the hammer is the evidence that supports or contradicts that claim.

Human review of hammer results is appropriate when:
- hammer tests are added or modified
- hammer failures are investigated
- a new system capability requires new invariant coverage
- the hammer is used to verify a system before a significant deployment

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- every V Ecosystem system must have a hammer layer
- the hammer verifies invariants under real execution, not through mocks
- the three required categories are persistence, contract, and boundary
- cross-project violation probes are required in every system's hammer
- transaction rollback behavior must be tested, not assumed
- a failing hammer means the system is not safe — it is not a minor inconvenience
- content graph junction isolation belongs in V Forge's hammer, not VEDA's

If an LLM treats the hammer as optional, as equivalent to unit tests, or as something that can be added "later," this doctrine is failing.

---

## Usage

This document should be used:

- when building the hammer layer for any V Ecosystem system
- when reviewing whether a system's hammer covers the required categories
- when deciding what to verify when a new capability is added
- when investigating a hammer failure
- when establishing whether a system is safe for production use

---

## Related Docs

- `../ecosystem/vocabulary.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/external-provider-integration-doctrine.md`
- `../project-v/system-invariants.md`
- `../veda/system-invariants.md`
- `../v-forge/system-invariants.md`
- `../interfaces/mcp-coordination-model.md`
- `agent-operating-doctrine.md`
- `failure-and-recovery-doctrine.md`
