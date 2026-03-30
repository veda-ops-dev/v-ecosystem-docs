# Project V Hammer Plan

## Purpose

This document turns the Project V hammer doctrine into an initial execution plan.

It exists to answer:

```text
What should the first hammer modules test, in what order, and which invariants do they protect?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the phased plan for Project V hammer modules
- what each phase protects
- what high-risk probes must be included
- the concurrency probe schedule
- the coordinator rule

---

## Out of Scope

This document does not define:

- the doctrine principles behind the hammer (see `hammer-doctrine.md`)
- the invariant-to-module coverage map (a companion `hammer-coverage-map.md` should be maintained alongside implementation)
- implementation-specific test runner or tooling choices

---

## System

- project-v

---

## Core Rule

Project V must not claim to be hardened until its highest-risk invariants are covered by repeatable hammer modules.

Happy-path proof is not enough. Each important area needs: valid-path coverage, invalid-path coverage, persistence inspection, boundary-pressure coverage, and deterministic assertions.

---

## Phase 1 — Core Persistence and Scope

**Goal:** Prove the basic multi-project data model is structurally safe.

**Modules:**
- `hammer-core-projects`
- `hammer-core-objectives`
- `hammer-core-initiatives`
- `hammer-core-work-items`
- `hammer-scope-isolation`

**Invariants protected:**
- Project-scoped rows belong to exactly one project
- Orphaned canonical records are rejected
- List behavior is deterministic
- Writes require valid scope
- Cross-project leakage fails

**Concurrency probes due in this phase:**
- Concurrent project-scoped unique key creation (hammer-core-projects, hammer-core-work-items)

---

## Phase 2 — State Transitions, Decisions, and Rollback

**Goal:** Prove that important state changes are explicit, aligned, and atomic.

**Modules:**
- `hammer-state-transitions`
- `hammer-decisions`
- `hammer-transaction-rollback`

**Invariants protected:**
- Illegal state transitions fail with `422`
- Required reason is enforced on reason-required transitions
- Decision / history alignment holds
- Partial writes do not survive failed mutations

**Concurrency probes due in this phase:**
- Concurrent conflicting status transitions (hammer-state-transitions)

---

## Phase 3 — Readiness and Gaps

**Goal:** Prove readiness is inspectable, reproducible, and not magic.

**Modules:**
- `hammer-readiness-core`
- `hammer-readiness-gaps`
- `hammer-readiness-reproducibility`

**Invariants protected:**
- Readiness requires visible basis
- Caller-supplied result cannot override server-owned result
- Gaps are recorded explicitly when conditions fail
- Advisory outputs do not silently mutate canonical state
- Same inputs produce same readiness result
- `ready_with_warnings` with required approval has a linked `DecisionRecord`
- Work item `readinessState` is updated atomically on evaluation creation

**Concurrency probes due in this phase:**
- Duplicate readiness evaluation trigger (hammer-readiness-core)

---

## Phase 4 — Evidence, Research, and Honesty

**Goal:** Prove supporting artifacts remain directional and honest.

**Modules:**
- `hammer-research-docs`
- `hammer-evidence-links`
- `hammer-derived-honesty`

**Invariants protected:**
- Evidence links do not overclaim ownership
- Imported or derived artifacts remain non-canonical where appropriate
- Summaries do not silently replace source planning truth
- VEDA-sourced research docs and evidence links carry correct boundary markers

---

## Phase 4.5 — Audits, Polymorphic References, and External Linkage

**Goal:** Prove the BYDA / traceability extension stays same-project, bounded, deterministic, and honest.

**Modules:**
- `hammer-audits`
- `hammer-audit-readiness-coupling`
- `hammer-cross-artifact-consistency`
- `hammer-ambiguity-detection`
- `hammer-external-links`

**Invariants protected:**
- Audit results are server-owned and not caller-settable
- Hard-failure conditions produce `fail`; warnings produce `warning`
- Required audit outcomes constrain readiness correctly
- Stale audit confidence triggers re-evaluation requirement
- Cross-artifact contradictions are detected
- Ambiguity detection behaves deterministically for governed patterns
- External linkage remains bounded traceability rather than ownership blur
- Audit gaps and readiness gaps remain structurally separate

---

## Phase 5 — Handoffs and Boundary Enforcement

**Goal:** Prove Project V does not collapse into VEDA or V Forge.

**Modules:**
- `hammer-handoffs`
- `hammer-boundary-enforcement`
- `hammer-cross-system-references`

**Invariants protected:**
- Handoffs require explicit target-system classification
- Project V does not accept observatory truth as its own canonical state
- Project V does not accept execution truth as its own canonical state
- Cross-system references remain explicit and bounded
- Invalid or ambiguous handoffs fail correctly
- Cross-project handoff contamination is rejected

**Integration scenarios required in this phase:**

**Stale external references**
- A Project V record references a VEDA or V Forge identifier that is no longer valid.
- Expected: stale references are detectable and flagged during audit or readiness evaluation. They must not be elevated to canonical planning truth.
- Coverage target: `hammer-cross-system-references`

**Invalid external identifiers**
- A handoff or cross-system reference is submitted with a structurally invalid external identifier.
- Expected: the write is rejected at the contract level. No malformed reference is stored as valid.
- Coverage targets: `hammer-cross-system-references`, `hammer-handoffs`

**Cross-project contamination via integration path**
- A Project V record in project A references a VEDA or V Forge record belonging to project B.
- Expected: cross-project external references are rejected or fail safely.
- Coverage targets: `hammer-scope-isolation`, `hammer-cross-system-references`

**Provenance violations**
- A planning conclusion derived from a VEDA observation is stored in a way that loses the VEDA provenance.
- Expected: evidence links and decision records citing VEDA material must preserve recoverable provenance.
- Coverage targets: `hammer-evidence-links`, `hammer-cross-system-references`

**Observatory-shaped payload stored as canonical Project V state**
- A payload containing SERP data, crawl observations, or GA4 signals is submitted to a Project V write surface.
- Expected: the write is rejected.
- Coverage target: `hammer-boundary-enforcement`

**Execution-shaped payload stored as canonical Project V state**
- A payload containing draft state, revision workflow, or publish status is submitted to a Project V write surface.
- Expected: the write is rejected.
- Coverage target: `hammer-boundary-enforcement`

---

## Phase 6 — Contract Hardening

**Goal:** Prove routes behave exactly and fail exactly.

**Modules:**
- `hammer-contracts-read`
- `hammer-contracts-write`
- `hammer-ordering`
- `hammer-validation`

**Invariants protected:**
- Response shape is stable
- Validation is deterministic
- Ordering is deterministic
- Negative paths fail with correct status codes

---

## Phase 7 — Coordinator Regression

**Goal:** Prove the whole hammer suite can be rerun as a reliable gate.

**Modules:**
- `hammer-coordinator`

**Invariants protected:**
- Broad regression coverage remains repeatable
- One broken area does not hide behind local passing tests
- Coordinator output clearly shows pass count, fail count, skip count, and failing module names

---

## Initial High-Risk Probes

The earliest hammer suite must intentionally try to break Project V through cases like:

- Create project-scoped records without a project
- Create records under the wrong project context
- Read a row from another project by direct identifier
- Create cross-project dependencies without explicit support
- Record readiness with no inspectable basis
- Create history without the corresponding state change
- Change state without required history
- Allow non-deterministic list ordering
- Persist derived convenience data as if it were canonical truth
- Create handoffs without valid target-system classification
- Treat stale audit confidence as if it were current
- Allow a required failing audit without constraining readiness
- Miss a material contradiction between schema, API, or transition docs
- Accept observatory-shaped or execution-shaped payloads as canonical Project V state

---

## Module Naming Rule

Use: `hammer-<bounded-concern>`

Examples:
- `hammer-scope-isolation`
- `hammer-readiness-core`
- `hammer-transaction-rollback`
- `hammer-boundary-enforcement`

Keep names explicit and tied to the invariant being stressed.

---

## Coverage Mapping Rule

Each hammer module must identify:

- the invariant(s) it covers
- the records or routes it touches
- the setup required
- the valid path being verified
- the invalid path being verified
- the exact pass criteria

If a module cannot explain what it is protecting, it is too vague.

Maintain a companion `hammer-coverage-map.md` that maps each invariant to the modules that protect it. That map must be updated whenever a module is added or retired. An invariant that does not appear in the coverage map is not protected.

---

## Coordinator Rule

A full coordinator must eventually run all active hammer modules in a stable order and produce a result that is easy to classify: pass count, fail count, skip count, failing module names.

The coordinator must become part of the standard hardening gate before major schema or endpoint expansion.

---

## Final Rule

Do not call Project V hardened because it works in the happy path once.

Call it hardened when the hammer can repeatedly prove: scope safety, transaction safety, readiness honesty, boundary integrity, deterministic behavior, and correct failure under pressure.

---

## Related Docs

- `hammer-doctrine.md`
- `system-invariants.md`
- `schema-authority.md`
- `schema-governance.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `controlled-vocabularies.md`
- `status-transitions.md`
