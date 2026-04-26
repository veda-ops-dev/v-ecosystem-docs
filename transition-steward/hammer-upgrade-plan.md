# Hammer Upgrade Plan — Ecosystem DB Hardening and Boundary Torture

## Purpose

This document captures the next hammer expansion required to convert the
current database posture and transaction-boundary doctrine from asserted rules
into mechanically verified reality.

This is a transition-support plan.
It is not authority doctrine.
It exists so that when implementation reaches the hammer-expansion phase,
future work does not have to rediscover what is currently missing.

---

## Why this plan exists

The current hammer doctrine stack is strong at the system level.

Project V hammer doctrine and V Forge hammer doctrine already define:

- invariants-first testing posture
- real execution over mocks
- exact assertions rather than vague “worked” checks
- concurrency probes as required, not optional
- rollback verification by reading persisted state after failure
- fake-coverage rules that block route-hit theater from counting as validation

That is the right foundation.

What is still missing is a layer above the per-system hammers:

**ecosystem-level DB hardening for the shared Postgres / multi-schema posture.**

The current architecture now depends on these claims being mechanically true:

- schema-scoped credentials are real
- one system cannot read or write another system’s schema by default
- DB-layer constraints still hold if app-layer validation fails or is bypassed
- transaction rollback is verified under deterministic mid-transaction failure
- required activity-trail writes fail atomically with the governed state change
- connection/session state does not leak across pooled usage
- migration independence across the four schemas is real

Today those are partially doctrine-backed and partially unproven.
This plan exists to close that gap deliberately instead of waiting for drift
or implementation accidents to expose it.

---

## Scope

This plan governs transition-support planning for hammer expansion in the
following areas:

- ecosystem-level cross-schema credential isolation probes
- DB-layer constraint probes
- deterministic transaction-failure injection for atomicity validation
- activity-trail atomicity failure probes
- lock contention / deadlock probes relevant to multi-write governed workflows
- connection pool/session hygiene checks
- migration independence and idempotency checks for the four-schema posture
- a minimal set of additional bounded probes that close high-value DB-hardening gaps

---

## Out of Scope

This plan does not define:

- the final authority location for ecosystem hammer doctrine
- the final runtime or language implementation of the hammer harness
- distributed-systems chaos tooling
- load testing for throughput/capacity
- non-DB implementation details for unrelated system modules
- a rewrite of the current Project V or V Forge hammer doctrine docs

This plan is for the missing hardening layer, not a full hammer redesign.

---

## Core framing

The existing hammers answer questions like:

- does Project V remain Project V?
- does V Forge remain V Forge?

The next missing layer must answer:

- does the shared Postgres instance actually preserve the four-schema boundary model?
- do transaction and rollback rules remain real under adversarial failure?
- does the activity-trail contract hold when the system is stressed or partially failing?

Those are ecosystem questions, not just system questions.

---

## Why this must not be skipped

If the ecosystem ships implementation before these probes exist, several of the
most load-bearing architecture claims remain honorific:

- the four-schema boundary can be silently defeated by one over-scoped DB user
- transaction safety can be assumed rather than proven
- activity-trail atomicity can fail open under error
- migration independence can be broken by accidental cross-schema coupling

The doctrine would still read cleanly.
The implementation would simply stop matching it.

That is the exact kind of drift this repo is trying to prevent.

---

## Recommended plan shape

When this work begins, create or promote an ecosystem-level hammer layer.

Probable home options once authority placement is chosen:

- `ecosystem/hammer-ecosystem-db-hardening.md`
- or equivalent authority path under governance/hammer doctrine

Until that authority location is chosen and written, this document remains the
transition-support control note for the upgrade.

---

## Priority order

The following priority order is the recommended execution sequence.

### Priority 1 — Cross-schema credential isolation probes

**Why first:** This is the single biggest doctrine-vs-reality gap in the repo.
If schema-scoped credentials are not mechanically enforced, the one-Postgres /
four-schema architecture is only a naming convention.

Required probe shape:

- connect using each bounded system’s DB credentials
- attempt read access into each non-owned schema
- attempt write access into each non-owned schema
- attempt metadata discovery paths that may still leak table existence
  (`information_schema`, catalog introspection, etc.)
- assert failure by privilege boundary, not by app-layer mediation

Minimum expectation:

- all cross-schema read attempts fail
- all cross-schema write attempts fail
- metadata discovery does not leak more than the intended posture allows

This should be treated as an ecosystem hammer module, not a local Project V or
V Forge-only check.

---

### Priority 2 — Deterministic mid-transaction failure injection

**Why second:** Every serious atomicity probe depends on being able to force
failure at a known point in a multi-write transaction.

Required capability:

- a test helper or harness mechanism that can force a transaction to fail on
  a chosen write boundary or query step
- verification must read the DB afterward to confirm rollback actually occurred

Without this, rollback tests tend to become ORM trust exercises instead of
real failure validation.

---

### Priority 3 — DB-layer constraint probes

**Why third:** App validation is not enough. The schema must still reject bad
writes when the app layer is bypassed or regresses.

Required probe shape:

- open a direct DB connection in test context
- attempt inserts/updates that violate:
  - NOT NULL constraints
  - foreign key integrity
  - uniqueness constraints
  - any CHECK constraints used to preserve state validity
- assert the DB rejects them with the expected failure class

This proves the DB is the last line of defense, not just the app.

---

### Priority 4 — Activity-trail atomicity failure probes

**Why fourth:** The ecosystem depends on required activity-trail writes being
atomic with governed state changes.

Required probe shape:

- force the activity-trail insert to fail during an operation that requires it
- attempt the governed state change
- verify that neither the state change nor the activity-trail record survives
  partially

This is the probe that converts “atomic or rollback” from doctrine into a
mechanically proven rule.

---

### Priority 5 — Deadlock and lock-order probes

**Why fifth:** The current hammer posture already covers some concurrency and
race patterns. What remains missing is deliberate lock-order violation.

Required probe shape:

- construct a two-transaction lock-order conflict
- assert one side fails with deadlock semantics
- assert the surviving side commits correctly
- assert the persisted DB state is valid after the deadlock resolution

This is especially relevant once handoff + activity-trail + multi-write seams
become real.

---

### Priority 6 — Connection/session hygiene probes

**Why sixth:** Shared Postgres + pooled connections means session leakage can
quietly erode boundary assumptions.

Required probe shape:

- after aborted transactions, reuse a pooled connection
- verify session state is clean:
  - expected `search_path`
  - no advisory locks left behind
  - no leaked temp objects
  - no leaked session settings/GUCs relevant to correctness

This is a cheap check that catches a class of silent weirdness early.

---

### Priority 7 — Migration independence and idempotency checks

**Why seventh:** Four independent schemas only remain independent if migration
ordering does not become an implicit dependency.

Required probe shape:

- apply each schema’s migrations in isolation
- verify the target schema reaches a valid end state without hidden reliance
  on another schema’s migration order
- re-run latest migrations or the full migration application where appropriate
  to verify idempotent/no-op behavior where expected

This helps catch accidental cross-schema coupling before it becomes entrenched.

---

### Priority 8 — Additional bounded probes

These are worthwhile but lower priority than the seven items above:

- timestamp abuse on append-only records
- mild boundary-check payload mutation/fuzz passes
- bounded-volume determinism replay checks
- crash/restart interruption matrix for handoff phase boundaries
- compaction safety checks once compaction exists

These should not block the first ecosystem DB hardening layer unless a concrete
implementation slice makes one of them immediately necessary.

---

## Recommended first module set

The minimum useful first cut is:

1. cross-schema credential isolation
2. deterministic mid-transaction failure helper
3. DB-layer constraint probes
4. activity-trail atomicity failure probes

That set closes the largest doctrine-vs-reality gaps with the least expansion
surface.

---

## Relationship to existing docs

This plan is downstream of and justified by the current settled docs, including:

- `ecosystem/db-posture.md`
- `ecosystem/cross-system-boundaries.md`
- `ecosystem/ecosystem-schema-spine.md`
- Project V hammer doctrine docs
- V Forge hammer doctrine docs
- any transaction, activity-trail, and handoff docs that require atomic state change behavior

This plan does not replace those docs.
It identifies what the current hammer posture still needs in order to prove the
most important database and boundary claims in implementation.

---

## Transition-plan placement rule

When the transition reaches the implementation-hardening phase, the relevant
entry in `transition-steward/transition-plan.md` should explicitly reference
this file by path so future work reads it before starting the hammer-expansion
pass.

Reference path:

- `transition-steward/hammer-upgrade-plan.md`

---

## Steward note

This document exists because the current doctrine is strong enough that the next
real risk is not conceptual confusion but unverified implementation assumptions.

The hammer upgrade should therefore focus on:

- proving the architecture’s hardest boundary claims mechanically
- testing the shared Postgres posture at the ecosystem layer
- preventing the first implementation slice from turning settled doctrine into
  optimistic folklore

---

## Related files

- `transition-plan.md`
- `../ecosystem/db-posture.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/ecosystem-schema-spine.md`
- `../project-v/hammer-doctrine.md`
- `../project-v/hammer-plan.md`
- `../project-v/hammer-implementation-rules.md`
- `../project-v/hammer-coverage-map.md`
- `../v-forge/hammer-doctrine.md`
