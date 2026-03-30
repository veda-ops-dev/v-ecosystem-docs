# Project V Hammer Doctrine

## Purpose

This document defines the hammer-testing doctrine for Project V.

It exists to answer:

```text
How should Project V be tested so its database integrity, API contracts, and orchestration rules are hardened instead of merely assumed?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- what the hammer is and is not
- the primary goals hammer tests must protect
- the core doctrine principles
- the hammer categories
- test design rules
- concurrency and race-condition coverage
- test environment and isolation posture
- the hammer enforcement gate

---

## Out of Scope

This document does not define:

- the specific hammer modules and phases (see `hammer-plan.md`)
- the invariant-to-module coverage map (that belongs in a companion `hammer-coverage-map.md` once tests exist)
- implementation-specific test runner or tooling choices

---

## System

- project-v

---

## Core Rule

Hammer tests exist to verify that Project V preserves its system invariants under realistic execution and deliberate boundary pressure.

Their job is not to perform shallow demo validation. Their job is to make it hard for architectural drift, weak contracts, partial writes, or convenience shortcuts to survive unnoticed.

---

## What the Hammer Is

The hammer is a testing doctrine centered on:

- invariant-first validation
- real database interaction
- real contract execution
- deliberate misuse probes
- deterministic assertions
- regression resistance

The hammer must prove not only that Project V works when used correctly, but also that it fails correctly when used incorrectly.

---

## What the Hammer Is Not

The hammer is not:

- UI screenshot theater
- mock-heavy false confidence
- shallow endpoint smoke testing only
- a substitute for unit tests
- a substitute for architecture discipline

Unit tests still matter. Type safety still matters. Linting still matters. But hammer tests are where the system proves its bounded behavior under realistic persistence and contract conditions.

---

## Primary Goals

Project V hammer tests must protect:

- bounded ownership integrity
- database integrity
- transaction integrity
- readiness and gating integrity
- deterministic ordering
- traceability integrity
- explicit state-transition discipline
- cross-system boundary integrity
- multi-project scope isolation

---

## Doctrine Principles

### 1. Invariants first

Every meaningful hammer module must correspond to one or more Project V invariants. If a behavior matters architecturally, there must be a hammer path that can prove it or break it.

### 2. Real execution over mock theater

Where practical, hammer tests must exercise real route handlers, real validation, real database writes and reads, and real transaction behavior. The closer the hammer is to real execution, the more trustworthy it is.

### 3. Exact contract beats vibes

A route must not merely return something plausible. It must return the correct status, the correct shape, the correct error posture, and the correct state behavior.

### 4. Breakage attempts are required

Each important surface must be tested in at least two ways: valid use and invalid or hostile use.

Project V must be probed for:
- missing required data
- invalid transitions
- illegal cross-system references
- non-deterministic ordering
- partial write exposure
- readiness claims without evidence

### 5. Boring structure wins

Hammer modules must be easy to read, easy to rerun, and easy to classify. A future operator or LLM must be able to tell: what invariant is being tested, what setup is required, what pass looks like, and what fail means.

---

## Hammer Categories

### 1. Persistence hammer

Verifies database truth and integrity.

Examples:
- required records persist correctly
- invalid writes are rejected
- multi-write mutations roll back correctly on failure
- orphaned records are rejected

### 2. Contract hammer

Verifies route and API contract behavior.

Examples:
- response status and shape
- validation errors return correct codes
- deterministic ordering
- explicit missing-resource behavior

### 3. Mutation-boundary hammer

Verifies that state changes obey bounded rules.

Examples:
- illegal state transition attempts fail with `422`
- explicit actions are required for readiness changes
- derived outputs do not silently overwrite canonical planning truth

### 4. Readiness hammer

Verifies that gating and audit behavior are explainable and inspectable.

Examples:
- a readiness evaluation records its basis
- readiness gaps appear when conditions fail
- the same evaluation yields the same result on the same inputs
- advisory outputs do not silently mutate canonical records

### 5. Audit hammer

Verifies BYDA audit behavior is explicit, consistent, and correctly bounded.

Examples:
- audit results are server-owned and not caller-settable
- hard-failure conditions produce `fail`
- cross-artifact contradictions are detected
- ambiguity detection behaves deterministically
- audit gaps and readiness gaps remain structurally separate

### 6. Boundary hammer

Verifies that Project V does not collapse into VEDA or V Forge responsibilities.

Examples:
- observatory-shaped payloads cannot be stored as canonical Project V truth
- execution-only state cannot be smuggled into Project V models
- cross-system writes through convenience paths are rejected

### 7. Determinism hammer

Verifies that stable inputs produce stable outputs.

Examples:
- list ordering remains deterministic
- readiness evaluation remains reproducible
- context assembly does not reorder arbitrarily

### 8. Scope isolation hammer

Verifies that multi-project separation is structurally enforced.

Examples:
- records from project A cannot be read under project B context
- cross-project relationships fail at the database level where required
- writes require explicit project scope

---

## Test Design Rules

### 1. Name modules by bounded concern

Examples:
- `hammer-core`
- `hammer-readiness`
- `hammer-dependencies`
- `hammer-handoffs`
- `hammer-contracts`
- `hammer-scope-isolation`
- `hammer-boundary-enforcement`

### 2. Keep fixtures explicit

Test setup must make ownership and intent visible. Do not hide important state assumptions in mystery helpers.

### 3. Prefer exact assertions

Assert exact failure reasons, exact ordering, exact mutation effects, and exact rollback behavior where practical.

### 4. Probe rollback deliberately

If an operation claims atomicity, the hammer must attempt to break the operation mid-flight and verify rollback.

### 5. Test the negative path on purpose

If a behavior should fail, that failure must be part of the expected passing test result.

---

## Concurrency and Race-Condition Coverage

Hammer tests must include concurrency scenarios for high-risk areas. Single-thread logic passing is not sufficient proof that a surface is hardened.

Required concurrency scenarios:

### Concurrent status transitions
- Attempt to transition a record through two conflicting states simultaneously.
- Expected: exactly one transition succeeds; the other fails with a clear rejection. No silent corruption.
- Coverage module: `hammer-state-transitions`

### Duplicate dependency creation
- Attempt to create the same dependency relationship from two concurrent requests.
- Expected: exactly one creation succeeds; the other fails with a conflict error. No duplicate row.
- Coverage module: `hammer-dependencies`

### Readiness evaluation races
- Attempt to trigger a readiness evaluation on the same target from two concurrent requests.
- Expected: the system does not produce duplicate evaluation records for the same run.
- Coverage module: `hammer-readiness-core`

### Concurrent canonical record creation
- Attempt to create two records with the same project-scoped unique key simultaneously.
- Expected: exactly one creation succeeds; the other is rejected with a uniqueness violation.
- Applicable to any record with a `projectId + key` uniqueness constraint.
- Coverage modules: `hammer-core-projects`, `hammer-core-work-items`, and equivalents per record type

First-pass concurrency testing does not require distributed simulation. Two sequential requests inside a single hammer run designed to stress the same constraint are sufficient for first pass.

---

## Test Environment and Isolation Posture

### Reset strategy

Each hammer module run must start from a known, clean state.

Preferred approach for first pass: truncate relevant tables before each module run, or use transaction-wrapped test cases that roll back after each case. Choose one strategy and apply it consistently within a module.

One hammer module's fixture data must not bleed into another module's assertions.

### Isolation expectations

- Hammer modules must not depend on data created by a previous module run.
- Hammer modules must not depend on implicit global state from the application or environment.
- Fixtures must be created explicitly within the module or its setup step.
- Module ordering in the coordinator must not be required to produce a correct per-module result.

### Reproducibility requirements

- Running the same hammer module twice against the same clean state must produce the same result.
- A module that passes on first run but fails on second run without any code change is flaky and must be treated as a defect.
- Non-deterministic ordering, time-dependent assertions, or hidden global state are not acceptable.

### Environment definition

- Hammer tests run against the `project_v` database on the shared local Postgres cluster.
- The database must exist and migrations must have run before the hammer suite starts.
- Hammer must not attempt to run its own migrations.
- Connection configuration must come from the same source as the application.

---

## Hammer Enforcement Gate

Hammer is not advisory. It is a hard gate.

Hammer must pass before:

- **schema changes** — any addition, removal, or modification to the Project V schema
- **API changes** — any new endpoint family, new route, or change to an existing contract
- **readiness or audit logic changes** — any modification to how readiness is evaluated, how gaps are recorded, or how audit results constrain planning state

This gate is a policy requirement. It applies regardless of whether automated tooling enforces it.

If hammer cannot pass after a proposed change, the change is not ready. If hammer coverage does not exist for the area being changed, adding that coverage is part of the work, not an afterthought.

The gate applies to both valid-path and invalid-path coverage. A change that adds a capability but only adds happy-path hammer coverage has not cleared the gate.

---

## Success Standard

A Project V surface is not considered hardened because it appears to work once.

A surface is hardened when:

- its invariant obligations are explicit
- its valid behavior is verified
- its invalid behavior is rejected correctly
- its persistence effects are inspectable
- its rollback posture is verified where relevant
- its results are repeatable

---

## Maintenance Rule

When a new important Project V capability is added:

1. Identify the invariants it touches
2. Add or extend hammer coverage
3. Verify both valid and invalid paths
4. Rerun the broader coordinator suite

Do not call a capability complete until it survives the hammer.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the hammer verifies real behavior, not shallow demos
- every important surface needs both valid-path and invalid-path coverage
- the hammer enforcement gate is a hard policy requirement, not a suggestion
- concurrency scenarios are required, not optional
- a failing hammer means the change is not ready

---

## Usage

This document should be used:

- as the primary doctrine reference when designing or extending hammer tests
- when deciding whether a capability is complete
- when reviewing whether hammer coverage is sufficient for a proposed change
- before approving schema, API, or evaluation logic changes

---

## Related Docs

- `hammer-plan.md`
- `system-invariants.md`
- `schema-authority.md`
- `schema-governance.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `../governance/testing-and-verification-doctrine.md`
