# V Forge Hammer Plan

## Purpose

This document defines the first-pass hammer plan for V Forge.

It exists to answer:

```text
What hammer modules, verification targets, and scenario families should V Forge implement first so the system can prove it remains the execution system of record under real operational pressure rather than merely looking correct in happy-path demos?
```

This is a Tier 2 V Forge verification planning authority document.

---

## Scope

This document governs:

- the first-pass hammer module map for V Forge
- what each hammer area is responsible for verifying
- which scenario classes are highest priority for first-pass coverage
- how V Forge hammer should divide runtime, surface, and boundary verification work
- what remains deferred after first pass

---

## Out of Scope

This document does not define:

- the exact implementation code for hammer modules
- CI pipeline wiring details
- generic unit or integration test inventory
- Project V or VEDA hammer plans
- final pass/fail thresholds for every implementation detail

Those belong in implementation, CI, or system-specific verification docs.

---

## System

- v-forge

---

## Core Rule

The V Forge hammer plan must verify doctrine-significant behavior before convenience behavior.

The first hammer modules should not optimize for easy demos.
They should optimize for proving that V Forge:
- stays inside execution ownership
- tells the truth when execution is messy
- preserves graph and release truth honestly
- stops and returns when planning ownership is required
- exposes operator surfaces that do not hide wrong actions or wrong state

If first-pass hammer spends its energy on easy polish checks while boundary drift remains unverified, the plan is wrong.

---

## First-Pass Hammer Objectives

The first pass should prove all of the following at a meaningful level:

1. V Forge remains the execution system of record
2. execution truth survives blocked, failed, partial, and rollback scenarios
3. content graph truth stays grounded in real built assets
4. release readiness is not treated as release authorization
5. return-to-planning works as a real governed exit path
6. execution intelligence does not become planning or observability ownership
7. operator surfaces preserve absent affordances and visible governance posture
8. project scope stays hard across execution, graph, release, and surface flows

These objectives are more important than broad but shallow coverage.

---

## Module Design Principles

### 1. Doctrine-first grouping
Modules should be grouped around load-bearing doctrine areas, not arbitrary code directories.

### 2. Realistic scenario pressure
Modules should prefer realistic workflow scenarios over abstract isolated assertions when doctrine depends on sequence and context.

### 3. Surface + runtime coupling
Where doctrine depends on both state logic and operator surface, hammer coverage should include both.

### 4. Failure-state seriousness
Blocked, failed, partial, rollback, and return-required states deserve first-pass verification, not last-pass cleanup.

### 5. Absence matters
Some hammer checks should verify that the wrong control, wrong mutation path, or wrong cross-system affordance does not exist.

---

## First-Pass Module Map

V Forge first-pass hammer should be organized into the following modules.

## Module 1 — Identity and Boundary Hammer

### Purpose
Verify that V Forge remains V Forge and does not drift into Project V or VEDA behavior.

### Must verify
- no direct planning mutation paths exist in V Forge behavior flows
- no VEDA raw-signal ownership behavior appears in V Forge flows
- execution intelligence does not become planning sovereignty
- graph and release records are treated as execution truth, not planning truth

### High-priority scenarios
- attempt to continue local execution when a planning decision is actually required
- attempt to interpret execution intelligence as permission for broader work
- inspect whether V Forge surfaces imply Project V-style ownership

### Why first-pass
This is the identity anchor.
If this fails, V Forge can look competent while being wrong.

---

## Module 2 — Execution Truth Hammer

### Purpose
Verify that work-unit truth remains honest under non-happy-path conditions.

### Must verify
- blocked state remains blocked
- partial state does not become completed
- failed state remains visible
- return-required does not become quietly resolved
- sending a return package does not auto-complete the work unit

### High-priority scenarios
- partial content update
- blocked new-content execution
- failed release attempt
- return-required work after planning contradiction discovered

### Why first-pass
Execution truth is core V Forge identity.
Without it, the system becomes status theater.

---

## Module 3 — Content Graph Truth Hammer

### Purpose
Verify that graph truth follows real built execution truth and remains project-scoped.

### Must verify
- new asset registration occurs only after the asset becomes real enough
- graph updates follow actual content change
- speculative future graph structure is not created
- cross-project graph contamination is blocked
- graph correction restores truthful structure rather than inventing strategy

### High-priority scenarios
- new content creation followed by graph registration
- existing content update with structural change
- attempted speculative graph mutation without execution basis
- attempted cross-project graph lookup or join

### Why first-pass
The content graph is one of V Forge’s key owned truth layers.
It cannot be left to weak verification.

---

## Module 4 — Release and Rollback Hammer

### Purpose
Verify disciplined release behavior.

### Must verify
- release readiness does not unlock release by itself
- authorization-sensitive release actions remain differentiated
- release continuity updates only after real action
- rollback is recorded honestly
- rollback outside admitted authority is blocked or escalated

### High-priority scenarios
- validated-but-not-authorized release
- authorized release with continuity update
- failed release producing honest state
- rollback in-bounds
- rollback attempted out-of-bounds

### Why first-pass
Release drift is one of the fastest ways execution systems become unsafe.

---

## Module 5 — Return-to-Planning Hammer

### Purpose
Verify that V Forge stops cleanly at real planning boundaries.

### Must verify
- planning-relevant findings can produce return-required posture
- return package preserves execution facts and uncertainty distinctly enough
- execution does not silently widen scope instead of returning
- local work-unit classification remains honest after return is sent

### High-priority scenarios
- content work reveals broader planning contradiction
- release work reveals planning-level authorization mismatch
- execution intelligence output becomes planning-relevant rather than execution-local

### Why first-pass
A system that never returns is usually a system that has quietly stolen planning authority.

---

## Module 6 — Execution Intelligence Boundary Hammer

### Purpose
Verify that execution intelligence remains powerful but non-sovereign.

### Must verify
- bounded signal use does not become signal ownership
- signal mismatch does not automatically mutate graph truth
- intelligence outputs do not self-authorize new work
- planning-relevant outputs route toward return instead of local silent expansion

### High-priority scenarios
- execution-local maintenance candidate
- planning-relevant mismatch finding
- attempt to auto-create new work from analytical result
- attempt to mutate graph purely from mismatch analysis

### Why first-pass
Execution intelligence is a likely drift vector because it feels smart.

---

## Module 7 — Operator Surface Hammer

### Purpose
Verify that the VS Code operator surface preserves doctrine.

### Must verify
- blocked / failed / partial / return-required states are visible
- release-sensitive actions are visually differentiated
- V Forge panels do not expose planning mutation controls
- graph inspection is not a speculative strategy canvas
- chat is not the only place critical V Forge truth or action exists
- return-to-planning is visible and operable

### High-priority scenarios
- inspect V Forge overview with messy states present
- inspect release panel with authorization-sensitive action present
- inspect findings/return surface with planning-relevant finding
- verify absence of direct planning controls in V Forge surface

### Why first-pass
Operator surfaces enforce doctrine in practice, not just in theory.

---

## Module 8 — Scope and Cross-Project Hammer

### Purpose
Verify that all major V Forge flows remain project-scoped.

### Must verify
- execution work-unit reads stay in active project scope
- graph inspection and mutation stay in active project scope
- release continuity stays in active project scope
- return packaging does not accidentally mix project contexts
- no convenience path leaks cross-project data through surface or runtime

### High-priority scenarios
- attempt to open out-of-project work unit
- attempt cross-project graph inspection
- attempt cross-project release lookup
- attempt return packaging with contaminated project context

### Why first-pass
Project-scope hardening is non-negotiable ecosystem law.

---

## Recommended First-Pass Execution Order

Implement hammer in this order:

1. **Identity and Boundary Hammer**
2. **Execution Truth Hammer**
3. **Content Graph Truth Hammer**
4. **Release and Rollback Hammer**
5. **Return-to-Planning Hammer**
6. **Execution Intelligence Boundary Hammer**
7. **Scope and Cross-Project Hammer**
8. **Operator Surface Hammer**

### Why this order
- identity failures poison everything else
- truth failures break core system trust
- graph and release truth are major owned surfaces
- return and intelligence are high-risk drift vectors
- operator surface checks matter a lot, but they depend on underlying runtime behavior being real first

---

## Scenario Families To Cover Early

Across modules, first-pass hammer should prioritize the following scenario families.

### 1. Clean happy path
Needed only as baseline, not as the center of the hammer.

### 2. Partial completion path
Critical for honest execution truth.

### 3. Blocked path
Critical for real-world execution posture.

### 4. Failed path
Critical for truthful reporting and continuity.

### 5. Authorization-mismatch path
Critical for release discipline.

### 6. Planning-boundary path
Critical for return-to-planning verification.

### 7. Cross-project contamination attempt
Critical for scope hardening.

### 8. Surface absence verification
Critical for absent-affordance doctrine.

---

## Deferred After First Pass

These areas may wait until after the first hammer wave if the core doctrine modules above are covered first.

- more detailed performance-oriented verification
- advanced surface execution condition verification once that feature is actually admitted
- broad experimentation or optimization flows
- commercial/runtime execution flows
- advanced analytics depth beyond core boundary checks
- deeper visual polish assertions that do not affect doctrine

### Rule
Do not defer identity, truth, scope, release discipline, or return behavior in favor of fancier secondary coverage.

---

## Pass/Fail Philosophy

A first-pass hammer module should count as successful when it proves a doctrine-significant area is actually defended, not merely present on paper.

Examples of real pass criteria:
- a wrong action path is absent or blocked
- a wrong state collapse does not occur
- a release cannot proceed without the required posture
- a planning-relevant finding produces a real return path
- a cross-project contamination attempt fails cleanly

Examples of fake pass criteria:
- the label rendered correctly once
- the demo path worked once
- the backend had a flag even though the surface still violated doctrine

Hammer pass means the system behaved correctly under pressure.

---

## Relationship to Other Verification Layers

V Forge should still have:
- unit tests
- integration tests
- route tests
- surface interaction tests

But hammer is different.

### Unit tests answer
“Did this isolated behavior do what the code expected?”

### Integration tests answer
“Did these pieces connect correctly?”

### Hammer answers
“Under realistic execution pressure, does this still behave like V Forge and preserve doctrine?”

All three matter.
Hammer is the one that protects system identity.

---

## Relationship to Extension-Wide Verification

Some V Forge hammer coverage will depend on extension-wide surfaces and runtime behavior.

Where that happens:
- V Forge-specific hammer cases should still articulate the V Forge invariant being protected
- shared extension verification may provide harness or execution support
- ownership of the invariant remains with V Forge when the invariant is about V Forge doctrine

The unified extension shell does not erase system-specific hammer responsibility.

---

## Anti-Drift Rules

### 1. No shallow-module inflation rule
Do not create many tiny modules that look comprehensive but skip the hard doctrine checks.

### 2. No demo-first prioritization rule
Do not prioritize photogenic happy-path tests ahead of boundary and truth verification.

### 3. No surface-free verification rule
Do not ignore operator-surface checks where doctrine depends on visible affordances.

### 4. No runtime-free verification rule
Do not rely on surface appearance when underlying state behavior is wrong.

### 5. No deferred-boundary rule
Do not postpone identity, scope, or return-to-planning checks to a later wave in favor of easier work.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:
- the first V Forge hammer wave should protect doctrine-significant areas first
- identity, truth, graph, release, return, intelligence, scope, and surface behavior all deserve module-level verification
- happy-path success is necessary but not sufficient
- absent affordances and messy-state truth are first-class hammer concerns
- the hammer plan is a priority map, not a random test wishlist

If an LLM could use this plan to justify a broad but shallow verification pass that leaves core V Forge drift vectors untested, this plan is failing.

---

## Usage

This document should be used:
- when implementing first-pass V Forge hammer modules
- when deciding the order of verification work
- when reviewing whether V Forge hammer coverage is doctrine-first or convenience-first
- when checking whether important drift vectors remain uncovered

---

## Related Docs

- `hammer-doctrine.md`
- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `mcp-surface.md`
- `content-lifecycle-workflow.md`
- `release-lifecycle-workflow.md`
- `content-graph-operations.md`
- `execution-intelligence-operations.md`
- `operator-surfaces/vscode-extension.md`
- `playbooks/content-update-playbook.md`
- `playbooks/new-content-execution-playbook.md`
- `playbooks/release-execution-playbook.md`
- `playbooks/return-to-planning-playbook.md`
- `../governance/testing-and-verification-doctrine.md`
- `../interfaces/extension-vscode-surface-architecture.md`
