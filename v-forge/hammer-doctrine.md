# V Forge Hammer Doctrine

## Purpose

This document defines the hammer doctrine V Forge uses to verify that its execution behavior, boundaries, and operator surfaces remain faithful under real operation.

It exists to answer:

```text
How should V Forge verify, under real execution conditions, that it remains the execution system of record, preserves graph truth and release truth honestly, respects planning and observability boundaries, enforces governed action posture, and does not quietly drift into a more convenient but incorrect system?
```

This is a Tier 2 V Forge verification authority document.

---

## Scope

This document governs:

- what the V Forge hammer layer is for
- which categories of V Forge behavior must be verified
- what counts as a hammer-worthy invariant in V Forge
- how hammer differs from unit tests, integration tests, and implementation convenience checks
- how hammer should treat operator surfaces, runtime posture, graph truth, release truth, and return-to-planning behavior
- anti-drift rules for V Forge verification design

---

## Out of Scope

This document does not define:

- the exact implementation code for every hammer module
- the full hammer plan or module inventory
- low-level CI wiring
- generic unit test philosophy for all code
- Project V hammer doctrine or VEDA hammer doctrine

Those belong in `hammer-plan.md`, implementation docs, or system-specific hammer docs.

---

## System

- v-forge

---

## Core Rule

The V Forge hammer exists to verify that V Forge remains V Forge under real execution pressure.

It is not enough for the code to compile, the UI to render, or the happy path to succeed.
The hammer must verify that V Forge:
- preserves execution truth honestly
- preserves graph truth honestly
- preserves release and rollback truth honestly
- stays inside execution ownership
- returns to planning instead of silently becoming planning
- consumes bounded signal without becoming observability ownership
- exposes operator surfaces that do not hide governance or boundary drift

If V Forge feels useful but fails those checks, V Forge is wrong.

---

## Hammer Definition

The V Forge hammer is the invariant-verification layer that tests whether V Forge’s real behavior remains compatible with its doctrine under meaningful operational conditions.

Hammer is not just “testing more.”
It is a specific class of verification concerned with:
- system identity
- system boundaries
- truthful state behavior
- governance posture
- operator-surface discipline
- drift resistance under realistic use

The hammer should behave like a skeptical auditor, not like a hype man for passing demos.

---

## What Hammer Must Verify

At minimum, the V Forge hammer must verify the following categories.

## 1. System Identity Invariants

The hammer must verify that V Forge behaves like the execution system of record rather than some blended system.

Examples:
- V Forge does not create or mutate Project V planning truth directly
- V Forge does not act like VEDA and own raw signal
- V Forge does not reinterpret execution intelligence as planning sovereignty
- V Forge does not use graph structures as shadow planning records

### Rule
If V Forge can pass all happy-path execution tests while still behaving like a shadow planner, the hammer layer is insufficient.

---

## 2. Execution Truth Invariants

The hammer must verify that execution state remains honest.

Examples:
- blocked, failed, partial, return-required, and rollback-active states are preserved honestly
- completion is not reported when only part of the work completed
- sending a return package does not silently mark a work unit completed
- release continuity reflects what actually happened, not what was intended

### Rule
Execution truth must survive friction.
If uncomfortable outcomes disappear under UI smoothing or state shortcuts, hammer must fail.

---

## 3. Content Graph Truth Invariants

The hammer must verify that graph operations remain tied to real built execution truth.

Examples:
- graph records are created only when assets become real enough to register
- graph changes follow actual content execution change
- graph does not pre-model future desired structure
- cross-project graph contamination does not occur
- graph correction restores truth rather than inventing strategy

### Rule
A graph that is convenient but speculative is a hammer failure.

---

## 4. Release and Rollback Invariants

The hammer must verify that release behavior remains disciplined.

Examples:
- release readiness is not treated as release authorization
- authorization-sensitive release actions are visibly distinct from routine actions
- release continuity updates only after real release action
- rollback is recorded as first-class execution truth
- rollback does not occur outside current authority without explicit governed handling

### Rule
Release convenience must never be allowed to masquerade as governed release legitimacy.

---

## 5. Return-to-Planning Invariants

The hammer must verify that V Forge stops at real planning boundaries.

Examples:
- planning-relevant findings can be surfaced through the governed return path
- execution does not silently widen admitted scope instead of returning
- return packaging preserves execution facts, interpretation, and uncertainty distinctly enough
- a returned work unit is not falsely classified as fully complete

### Rule
If V Forge can keep “helpfully” going where doctrine requires return, hammer must fail.

---

## 6. Execution Intelligence Boundary Invariants

The hammer must verify that execution intelligence stays execution-side.

Examples:
- execution intelligence does not become raw signal ownership
- signal mismatch does not automatically mutate graph truth
- execution intelligence outputs do not self-authorize new work
- planning-relevant outputs route through return-to-planning instead of silent local expansion

### Rule
Analytics must remain powerful but non-sovereign.
If intelligence becomes permission, hammer must fail.

---

## 7. Operator Surface Invariants

The hammer must verify that the extension surfaces preserve doctrine.

Examples:
- V Forge panels do not expose direct Project V planning mutation controls
- V Forge surfaces do not hide blocked/failed/return-required posture
- authorization-sensitive release actions are visibly distinguished
- chat is not the only place where critical V Forge truth or action exists
- return-to-planning is a first-class visible path

### Rule
A pretty surface that hides governance drift is a hammer failure.

---

## 8. Scope and Multi-Project Invariants

The hammer must verify that project scope remains hard.

Examples:
- work-unit inspection stays project-scoped
- graph inspection stays project-scoped
- release continuity stays project-scoped
- no accidental cross-project reads or mutations occur through convenience surfaces or tool flows

### Rule
Cross-project contamination is never a minor bug.
It is a system-identity failure.

---

## 9. Absent-Affordance Invariants

The hammer must verify not only what exists, but what is absent.

Examples:
- no planning-mutation controls inside V Forge panels
- no generic approve-and-continue shortcuts that bypass governance posture
- no speculative graph design controls
- no hidden one-click ship-it affordances where stronger discipline is required

### Rule
Absent affordances are part of the doctrine.
If the wrong control exists, hammer should care.

---

## What Hammer Is Not

The V Forge hammer is not:
- a code coverage metric
- a UI smoke-test suite
- a generic snapshot test collection
- a substitute for unit or integration testing
- a performance benchmark suite
- a bag of end-to-end happy path demos

Those may all be useful.
They are not enough.

Hammer asks:
**“Does this still behave like V Forge under stress and ambiguity?”**

---

## Verification Posture

Hammer verification should prefer:
- realistic operational flows
- realistic boundary pressure
- realistic ambiguity around state and scope
- realistic operator-surface interaction patterns
- realistic return, rollback, partial, and blocked conditions

Hammer should distrust:
- only testing perfect happy paths
- only testing backend rules without surface behavior
- only testing surfaces without state truth
- only testing prose conformance without actual behavior

A system that passes idealized tests while failing under real operational pressure has not passed hammer.

---

## Hammer-Worthy V Forge Questions

A hammer test is worth writing when it answers a question like:
- does V Forge stay in execution ownership here?
- can the system still tell the truth when the outcome is messy?
- does the graph stay tied to built reality here?
- does release discipline remain explicit here?
- does the operator surface still make the right actions visible and the wrong ones absent?
- does the system stop and return when planning ownership is required?

If a test only proves that a label renders correctly in a trivial case, it may be useful, but it is not hammer by itself.

---

## Failure Philosophy

Hammer failures should be treated as doctrine failures, not cosmetic defects.

Examples of hammer-significant failures:
- release action available in the wrong posture
- graph records created ahead of execution truth
- planning mutation exposed inside V Forge surface
- return-required work silently marked completed
- execution intelligence auto-authorizing new work
- blocked/failed state hidden behind softened UI language

### Rule
When hammer finds that V Forge behavior has crossed a boundary, the correct response is not to rename the bug as “just UX.”
It is a doctrine break until proven otherwise.

---

## Surface and Runtime Coupling Rule

The hammer must verify both runtime logic and operator-surface behavior where doctrine depends on both.

Examples:
- it is not enough that release authorization exists in backend logic if the UI still presents release like a casual action
- it is not enough that return-to-planning exists in backend state if the operator cannot see or use it properly
- it is not enough that graph correction is bounded in theory if the surface encourages speculative graph editing behavior

### Rule
If doctrine is enforced partly by what the operator can and cannot do, hammer must test that reality.

---

## Relationship to Playbooks

The hammer should validate the practical flows that the playbooks rely on.

That includes flows consistent with:
- `playbooks/content-update-playbook.md`
- `playbooks/new-content-execution-playbook.md`
- `playbooks/release-execution-playbook.md`
- `playbooks/return-to-planning-playbook.md`

If the actual extension or runtime behavior makes those playbooks impossible to follow honestly, hammer should fail.

---

## Anti-Drift Rules

### 1. No happy-path-only rule
Do not define hammer in a way that only checks ideal completion paths.

### 2. No backend-only comfort rule
Do not ignore surface-level drift just because the backend has the right internal flags.

### 3. No UI-only comfort rule
Do not accept pretty surfaces if underlying truth behavior is wrong.

### 4. No planner-creep tolerance rule
Do not treat silent planning drift inside execution as minor.

### 5. No analytics-sovereignty tolerance rule
Do not let execution intelligence become permission or ownership.

### 6. No convenience-affordance amnesty rule
Do not excuse wrong controls merely because they are handy during implementation.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:
- V Forge hammer verifies system identity, not just surface polish
- truthful blocked/failed/partial/rollback/return states matter deeply
- graph truth, release truth, and return posture are all hammer-worthy
- operator surfaces are part of doctrine enforcement
- absent affordances matter as much as visible ones
- hammer failures indicate doctrine drift, not just implementation untidiness

If an LLM could use this document to justify a shallow test suite that proves only that the demo looks nice, this doctrine is failing.

---

## Usage

This document should be used:
- before designing the V Forge hammer plan
- when deciding whether a proposed test belongs in hammer or ordinary testing
- when reviewing whether V Forge surfaces and runtime still enforce the right boundaries
- when deciding whether a defect is doctrine-significant enough to merit hammer coverage

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `mcp-surface.md`
- `content-lifecycle-workflow.md`
- `release-lifecycle-workflow.md`
- `content-graph-operations.md`
- `execution-intelligence-operations.md`
- `operator-quickstart.md`
- `operator-surfaces/vscode-extension.md`
- `playbooks/content-update-playbook.md`
- `playbooks/new-content-execution-playbook.md`
- `playbooks/release-execution-playbook.md`
- `playbooks/return-to-planning-playbook.md`
- `../governance/testing-and-verification-doctrine.md`
- `../interfaces/extension-vscode-surface-architecture.md`
- `../interfaces/extension-governance-and-gating-model.md`
