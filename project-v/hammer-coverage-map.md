# Hammer Coverage Map

## Purpose

This document maps Project V invariants, system-level behaviors, and API family hammer expectations to the specific hammer modules that protect them.

It exists to answer:

```text
For every invariant and every API family's stated hammer expectations, which hammer module is responsible for verifying it, and what does that coverage look like?
```

Read this with:

- `hammer-doctrine.md`
- `hammer-plan.md`
- `system-invariants.md`
- `api-conventions.md`
- `../governance/testing-and-verification-doctrine.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the mapping from the three required hammer categories to planned modules
- the mapping from named system invariants to hammer modules
- the mapping from named API family hammer expectations to hammer modules
- the module ownership model
- coverage gap tracking
- the update rule for this document

---

## Out of Scope

This document does not define:

- the hammer doctrine or principles (see `hammer-doctrine.md`)
- the phased execution plan for hammer modules (see `hammer-plan.md`)
- the individual API family contracts being tested (see `project-v/api/`)
- implementation-specific test runner or tooling choices

---

## System

- project-v

---

## Core Rule

An invariant or hammer expectation that does not appear in this map is not covered.

This map must be updated whenever a new hammer module is added, retired, or reassigned. It must also be updated when a new API family doc lists hammer expectations that are not yet mapped here.

A claimed hammer coverage that does not appear in this map is an uncovered claim, not a protected invariant.

---

## How to Read This Map

Each entry identifies:

- the invariant or expectation being covered
- the source document where it is stated
- the hammer module responsible
- the hammer phase in which coverage is expected
- the coverage posture: valid-path, invalid-path, or both

**Coverage posture key:**
- `V` = valid-path only (incomplete — should-fix)
- `I` = invalid-path only (unusual — flag for review)
- `V+I` = both valid and invalid paths (complete first-pass coverage)
- `—` = module is planned and assigned but specific test not yet written
- `(unassigned)` = no module assignment exists yet; must be resolved before claiming coverage

---

## Module Ownership Index

The following modules are defined in `hammer-plan.md`. Each owns the coverage listed in this map.

| Module | Phase | Primary concern |
|---|---|---|
| `hammer-core-projects` | 1 | Project creation, scope, uniqueness |
| `hammer-core-objectives` | 1 | Objective creation, parent scope, ordering |
| `hammer-core-initiatives` | 1 | Initiative creation, parent scope, ordering |
| `hammer-core-work-items` | 1 | Work item creation, type, targetSystem, readinessState |
| `hammer-dependencies` | 1 | Dependency creation, polymorphic reference validation, duplicate rejection |
| `hammer-scope-isolation` | 1 | Multi-project cross-contamination rejection |
| `hammer-state-transitions` | 2 | All governed status routes, StatusHistory atomicity |
| `hammer-decisions` | 2 | DecisionRecord creation, supersedence, StatusHistory |
| `hammer-transaction-rollback` | 2 | Atomicity under mid-write failure conditions |
| `hammer-readiness-core` | 3 | Readiness evaluation initiation, result, gap + readinessState atomicity |
| `hammer-readiness-gaps` | 3 | Gap PATCH posture, immutability of gap identity fields |
| `hammer-readiness-reproducibility` | 3 | Same-input determinism for readiness evaluations |
| `hammer-research-docs` | 4 | ResearchDoc creation, status, boundary posture |
| `hammer-evidence-links` | 4 | EvidenceLink identity immutability, bounded PATCH |
| `hammer-derived-honesty` | 4 | Derived/imported records do not masquerade as canonical truth |
| `hammer-audits` | 4.5 | Audit initiation, applicability gate, result posture, staleness |
| `hammer-audit-readiness-coupling` | 4.5 | Audit state constraining readiness correctly |
| `hammer-cross-artifact-consistency` | 4.5 | Cross-artifact contradiction detection |
| `hammer-ambiguity-detection` | 4.5 | Material vs advisory ambiguity classification |
| `hammer-external-links` | 4.5 | ExternalLink bounded reference posture |
| `hammer-handoffs` | 5 | Handoff lifecycle, completedAt atomicity, reverse re-entry |
| `hammer-boundary-enforcement` | 5 | Observatory/execution payloads rejected as Project V truth |
| `hammer-cross-system-references` | 5 | Stale, invalid, and cross-project external references |
| `hammer-contracts-read` | 6 | Read route shape, ordering, non-leakage |
| `hammer-contracts-write` | 6 | Write route shape, forbidden fields, server-owned fields |
| `hammer-ordering` | 6 | Deterministic list ordering across all families |
| `hammer-validation` | 6 | Error codes, 400 vs 422 distinctions across families |
| `hammer-coordinator` | 7 | Full suite regression run |

---

## Section 0 — Doctrine Category Coverage

`governance/testing-and-verification-doctrine.md` requires every system's hammer to cover three categories. This section maps those categories to Project V modules and states current coverage status.

### Persistence Hammer
*Verifies schema integrity, migration integrity, atomicity, and no unexpected write side effects.*

| Behavior | Modules | Status |
|---|---|---|
| Schema integrity — tables, columns, constraints match expected structure | `hammer-core-projects`, `hammer-core-work-items`, and per-family core modules | Planned / unimplemented |
| Migration integrity — migrations apply cleanly and produce expected schema | `hammer-transaction-rollback` | Planned / unimplemented |
| Atomicity — multi-write operations succeed or fail as a unit | `hammer-state-transitions`, `hammer-transaction-rollback`, `hammer-readiness-core`, `hammer-handoffs`, `hammer-audits` | Planned / unimplemented |
| No unexpected write side effects | `hammer-contracts-read` | Planned / unimplemented |

**Category status: Partially assigned; no modules yet implemented.**

### Contract Hammer
*Verifies API contracts behave as documented: validation, response shapes, ordering, pagination, filtering.*

| Behavior | Modules | Status |
|---|---|---|
| Request validation rejects invalid input with correct error shape | `hammer-validation`, `hammer-contracts-write`, all family modules | Planned / unimplemented |
| Successful requests return documented response shape | `hammer-contracts-read`, all family modules | Planned / unimplemented |
| List endpoints use deterministic ordering with stable tie-breakers | `hammer-ordering` | Planned / unimplemented |
| Zero-state behavior handled correctly | `hammer-contracts-read` | Planned / unimplemented |
| Pagination, filtering, and sorting behave as documented | `hammer-ordering`, `hammer-contracts-read` | Planned / unimplemented |

**Category status: Partially assigned; no modules yet implemented.**

### Boundary Hammer
*Verifies project isolation, system ownership boundaries, cross-project violation probes, rollback behavior.*

| Behavior | Modules | Status |
|---|---|---|
| Project isolation — data from one project cannot be read or written by another project's session | `hammer-scope-isolation` | Planned / unimplemented |
| Cross-project violation probes — explicit attempts return `404 Not Found` | `hammer-scope-isolation`, `hammer-contracts-read` | Planned / unimplemented |
| System ownership boundaries — Project V does not absorb VEDA or V Forge truth | `hammer-boundary-enforcement`, `hammer-derived-honesty` | Planned / unimplemented |
| Transaction rollback works under real failure conditions | `hammer-transaction-rollback` | Planned / unimplemented |

**Category status: Partially assigned; no modules yet implemented.**

---

## Section 1 — System Invariant Coverage

These map `system-invariants.md` invariants to hammer modules.

### Invariant 1 — Project V Owns Planning and Orchestration Truth

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| Project-scoped records are created with valid project scope | `hammer-core-projects` | 1 | V+I |
| Records without a valid project are rejected | `hammer-core-projects` | 1 | I |
| Observatory-shaped payloads cannot be stored as canonical Project V state | `hammer-boundary-enforcement` | 5 | I |
| Execution-shaped payloads cannot be stored as canonical Project V state | `hammer-boundary-enforcement` | 5 | I |

### Invariant 2 — Project V Does Not Own Execution Truth

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| Execution-lifecycle state is rejected when submitted to Project V write routes | `hammer-boundary-enforcement` | 5 | I |
| Rich execution-progress payloads are rejected at the contract level | `hammer-boundary-enforcement` | 5 | I |

### Invariant 3 — Project V Does Not Own Signal or Observability Truth

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| SERP, crawl, GA4, or observatory-shaped payloads are rejected at Project V write routes | `hammer-boundary-enforcement` | 5 | I |
| Evidence links remain directional references; they do not store evidence content | `hammer-evidence-links` | 4 | V+I |

### Invariant 4 — Project V Governs Handoff Without Becoming Execution

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| Handoffs require explicit target-system classification | `hammer-handoffs` | 5 | V+I |
| Handoffs in `proposed` status do not imply execution has begun | `hammer-handoffs` | 5 | V+I |
| `completedAt` is set atomically on `closed` transition | `hammer-handoffs` | 5 | V+I |

### Invariant 5 — Project V Replans Through Governed Return Paths

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| Returned findings do not automatically mutate planning records | `hammer-boundary-enforcement` | 5 | I |
| Reverse re-entry transitions on handoffs require explicit reason | `hammer-handoffs` | 5 | V+I |

### Invariant 6 — Project V Preserves Decision Continuity

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| DecisionRecord creation is well-formed with required fields | `hammer-decisions` | 2 | V+I |
| `recorded → superseded` transition requires explicit reason and writes StatusHistory | `hammer-decisions` | 2 | V+I |
| StatusHistory is written atomically with the governed transition | `hammer-state-transitions` | 2 | V+I |

### Invariant 7 — Project V Does Not Treat Interpretation as Decision

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| Readiness evaluation result is server-owned and not caller-settable | `hammer-readiness-core` | 3 | I |
| A `ready` result does not automatically activate a handoff | `hammer-handoffs` | 5 | I |
| Derived outputs do not silently mutate canonical state | `hammer-derived-honesty` | 4 | I |

### Invariant 8 — Project V Must Remain Multi-Project Capable

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| Records from project A cannot be read under project B context | `hammer-scope-isolation` | 1 | I |
| Cross-project dependency creation is rejected | `hammer-scope-isolation` | 1 | I |
| Writes require explicit project scope that matches session context | `hammer-core-projects` | 1 | V+I |
| Cross-project existence is not leaked through filter or error responses | `hammer-contracts-read` | 6 | I |

### Invariant 9 — Project V Must Remain Governed

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| Status transitions that require explicit reason are rejected without it | `hammer-state-transitions` | 2 | I |
| `ready_with_warnings` requiring approval has a linked DecisionRecord | `hammer-readiness-core` | 3 | V+I |

### Invariant 10 — Project V Must Remain Interface-Respecting

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| External references remain directional and bounded | `hammer-cross-system-references` | 5 | V+I |
| Invalid external identifiers are rejected at write time | `hammer-cross-system-references` | 5 | I |
| Stale external references are detectable through audit or readiness evaluation | `hammer-cross-system-references` | 5 | V+I |

### Invariant 11 — Project V Must Preserve Planning-Side Traceability

| Behavior | Module | Phase | Posture |
|---|---|---|---|
| ReadinessEvaluation records basis fields explicitly (summary, rulePackage) | `hammer-readiness-core` | 3 | V |
| EvidenceLink records reference the source entity and locator explicitly | `hammer-evidence-links` | 4 | V |
| AuditRun records summary and result basis | `hammer-audits` | 4.5 | V |

### Invariant 12 — Project V Must Not Collapse Into Implementation Detail

Not directly hammer-testable. Enforced through documentation discipline and review.

---

## Section 2 — API Conventions Coverage

These map cross-family rules from `api-conventions.md` to hammer modules.

| Convention | Module | Phase | Posture |
|---|---|---|---|
| Unknown PATCH body fields rejected with `400` | `hammer-contracts-write` | 6 | I |
| Unknown query parameters rejected with `400` | `hammer-contracts-read` | 6 | I |
| Caller-supplied forbidden fields rejected with `400` | `hammer-contracts-write` | 6 | I |
| Server-owned fields not caller-settable | `hammer-contracts-write` | 6 | I |
| Cursor pagination: malformed cursor rejected with `400` | `hammer-contracts-read` | 6 | I |
| `nextCursor = null` signals end of results | `hammer-ordering` | 6 | V |
| Deterministic ordering with stable tie-breaker on all list routes | `hammer-ordering` | 6 | V+I |
| `400` vs `422` distinction maintained correctly | `hammer-validation` | 6 | V+I |
| `409 Conflict` on duplicate natural-uniqueness violation | `hammer-contracts-write` | 6 | I |
| External reference format validation (non-empty, https:// where required) | `hammer-contracts-write` | 6 | I |
| Non-leakage: out-of-scope resource returns `404 Not Found` | `hammer-scope-isolation` | 1 | I |
| Actor resolution is server-side; caller must not supply actor | `hammer-state-transitions` | 2 | I |
| Transaction: status change + StatusHistory written atomically | `hammer-state-transitions` | 2 | V+I |
| Transaction: readiness evaluation + gaps + WorkItem.readinessState (where applicable) written atomically | `hammer-readiness-core` | 3 | V+I |
| Transaction: completedAt set atomically on terminal transition | `hammer-handoffs` | 5 | V+I |

---

## Section 3 — API Family Hammer Expectations

These map the hammer expectations stated in each API family authority doc to hammer modules.

### Objectives (`api/objectives.md`)

| Expectation | Module | Phase | Posture |
|---|---|---|---|
| Creation with valid input | `hammer-core-objectives` | 1 | V |
| Duplicate key rejection with `409` | `hammer-core-objectives` | 1 | I |
| Malformed UUID rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown query parameter rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown PATCH field rejection with `400` | `hammer-contracts-write` | 6 | I |
| Forbidden field rejection on create and patch | `hammer-contracts-write` | 6 | I |
| Deterministic list ordering | `hammer-ordering` | 6 | V |
| Cursor continuation correctness | `hammer-ordering` | 6 | V |
| Status filter non-leakage | `hammer-scope-isolation` | 1 | I |
| Illegal status transition rejection with `422` | `hammer-state-transitions` | 2 | I |
| Required-reason transition rejection with `422` | `hammer-state-transitions` | 2 | I |
| Status transition + history atomicity | `hammer-state-transitions` | 2 | V+I |
| Cross-project fetch/patch/status non-leakage | `hammer-scope-isolation` | 1 | I |

### Initiatives (`api/initiatives.md`)

| Expectation | Module | Phase | Posture |
|---|---|---|---|
| Creation with valid input | `hammer-core-initiatives` | 1 | V |
| Duplicate key rejection with `409` | `hammer-core-initiatives` | 1 | I |
| Malformed UUID rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown query/PATCH field rejection with `400` | `hammer-contracts-write` | 6 | I |
| Forbidden field rejection on create and patch | `hammer-contracts-write` | 6 | I |
| Deterministic list ordering | `hammer-ordering` | 6 | V |
| Cursor continuation correctness | `hammer-ordering` | 6 | V |
| objectiveId filter non-leakage | `hammer-scope-isolation` | 1 | I |
| Same-project objectiveId validation on create and patch | `hammer-core-initiatives` | 1 | I |
| Invalid targetSystem rejection with `422` | `hammer-validation` | 6 | I |
| Illegal status transition rejection with `422` | `hammer-state-transitions` | 2 | I |
| Required-reason transition rejection with `422` | `hammer-state-transitions` | 2 | I |
| Status transition + history atomicity | `hammer-state-transitions` | 2 | V+I |
| Cross-project fetch/patch/status non-leakage | `hammer-scope-isolation` | 1 | I |

### Work Items (`api/work-items.md`)

| Expectation | Module | Phase | Posture |
|---|---|---|---|
| Creation with valid input | `hammer-core-work-items` | 1 | V |
| Duplicate key rejection with `409` | `hammer-core-work-items` | 1 | I |
| Malformed UUID rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown query/PATCH field rejection with `400` | `hammer-contracts-write` | 6 | I |
| Forbidden field rejection on create, patch, status routes | `hammer-contracts-write` | 6 | I |
| Deterministic list ordering | `hammer-ordering` | 6 | V |
| Cursor continuation correctness | `hammer-ordering` | 6 | V |
| initiativeId filter non-leakage | `hammer-scope-isolation` | 1 | I |
| Same-project initiativeId validation on create and patch | `hammer-core-work-items` | 1 | I |
| Invalid type rejection with `422` | `hammer-validation` | 6 | I |
| Invalid targetSystem rejection with `422` | `hammer-validation` | 6 | I |
| Caller-supplied readinessState rejection with `400` | `hammer-contracts-write` | 6 | I |
| blocked=true without blockedReason rejection with `422` | `hammer-core-work-items` | 1 | I |
| Illegal status transition rejection with `422` | `hammer-state-transitions` | 2 | I |
| Required-reason transition rejection with `422` | `hammer-state-transitions` | 2 | I |
| Status transition + history atomicity | `hammer-state-transitions` | 2 | V+I |
| Cross-project fetch/patch/status non-leakage | `hammer-scope-isolation` | 1 | I |

### Dependencies (`api/dependencies.md`)

| Expectation | Module | Phase | Posture |
|---|---|---|---|
| Creation with valid input | `hammer-dependencies` | 1 | V |
| Duplicate logical dependency rejection with `409` | `hammer-dependencies` | 1 | I |
| Malformed UUID rejection with `400` | `hammer-contracts-read` | 6 | I |
| sourceEntityId-without-type rejection with `400` | `hammer-contracts-write` | 6 | I |
| targetEntityId-without-type rejection with `400` | `hammer-contracts-write` | 6 | I |
| Unknown query/PATCH field rejection with `400` | `hammer-contracts-write` | 6 | I |
| Forbidden field rejection on create and patch | `hammer-contracts-write` | 6 | I |
| Deterministic list ordering | `hammer-ordering` | 6 | V |
| Cursor continuation correctness | `hammer-ordering` | 6 | V |
| Source and target entity filter non-leakage | `hammer-scope-isolation` | 1 | I |
| Same-project polymorphic reference validation on create | `hammer-dependencies` | 1 | I |
| Self-reference rejection with `422` | `hammer-dependencies` | 1 | I |
| Invalid dependencyType rejection with `422` | `hammer-validation` | 6 | I |
| Invalid dependency status rejection with `422` | `hammer-validation` | 6 | I |
| Cross-project fetch/patch non-leakage | `hammer-scope-isolation` | 1 | I |

### Handoffs (`api/handoffs.md`)

| Expectation | Module | Phase | Posture |
|---|---|---|---|
| Creation with valid input | `hammer-handoffs` | 5 | V |
| Malformed UUID rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown query/PATCH field rejection with `400` | `hammer-contracts-write` | 6 | I |
| Forbidden field rejection on create, patch, status routes | `hammer-contracts-write` | 6 | I |
| Caller-supplied completedAt rejection with `400` | `hammer-handoffs` | 5 | I |
| Deterministic list ordering | `hammer-ordering` | 6 | V |
| Cursor continuation correctness | `hammer-ordering` | 6 | V |
| Source-entity filter non-leakage | `hammer-scope-isolation` | 1 | I |
| Same-project source-entity validation on create | `hammer-handoffs` | 5 | I |
| Invalid targetSystem rejection with `422` | `hammer-validation` | 6 | I |
| Invalid handoffType rejection with `422` | `hammer-validation` | 6 | I |
| Empty readinessBasisSummary string rejection with `422` | `hammer-handoffs` | 5 | I |
| Illegal status transition rejection with `422` | `hammer-state-transitions` | 2 | I |
| Required-reason transition rejection with `400` | `hammer-state-transitions` | 2 | I |
| Already-in-status rejection with `422` | `hammer-state-transitions` | 2 | I |
| completedAt null for all non-closed statuses | `hammer-handoffs` | 5 | V+I |
| completedAt non-null atomicity on transition to `closed` | `hammer-handoffs` | 5 | V+I |
| Status transition + history atomicity | `hammer-state-transitions` | 2 | V+I |
| Reverse re-entry transition requires explicit reason | `hammer-handoffs` | 5 | I |
| accepted and closed are terminal (no reverse transitions) | `hammer-handoffs` | 5 | I |
| Cross-project fetch/patch/status non-leakage | `hammer-scope-isolation` | 1 | I |

### Readiness (`api/readiness.md`)

| Expectation | Module | Phase | Posture |
|---|---|---|---|
| Evaluation creation with valid input for each supported entity type | `hammer-readiness-core` | 3 | V |
| Malformed UUID rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown query parameter rejection with `400` | `hammer-contracts-read` | 6 | I |
| Forbidden field rejection on evaluation creation | `hammer-contracts-write` | 6 | I |
| Caller-supplied result rejection with `400` | `hammer-readiness-core` | 3 | I |
| Caller-supplied summary rejection with `400` | `hammer-readiness-core` | 3 | I |
| entityId without entityType rejection with `400` | `hammer-contracts-write` | 6 | I |
| Invalid evaluationType rejection with `422` | `hammer-validation` | 6 | I |
| Invalid rulePackage rejection with `422` | `hammer-readiness-core` | 3 | I |
| Empty deferWithReason rejection with `422` | `hammer-readiness-core` | 3 | I |
| deferWithReason non-empty produces deferred result without full evaluation and without gap creation | `hammer-readiness-core` | 3 | V+I |
| Default rule package selection when rulePackage omitted | `hammer-readiness-core` | 3 | V |
| Caller-supplied rulePackage override applied correctly | `hammer-readiness-core` | 3 | V |
| Cross-project entity reference rejection without leakage | `hammer-scope-isolation` | 1 | I |
| Entity not-found-in-scope returns empty list, not disclosure | `hammer-scope-isolation` | 1 | I |
| Deterministic list ordering for evaluations and gaps | `hammer-ordering` | 6 | V |
| Cursor continuation correctness | `hammer-ordering` | 6 | V |
| Evaluation immutability: no mutation path exists | `hammer-readiness-core` | 3 | I |
| Gap + WorkItem.readinessState atomicity with parent evaluation creation | `hammer-readiness-core` | 3 | V+I |
| WorkItem.readinessState sync atomicity on work_item evaluation | `hammer-readiness-core` | 3 | V+I |
| WorkItem.readinessState not changed for non-work-item entity types | `hammer-readiness-core` | 3 | I |
| Gap severity and description immutability after creation | `hammer-readiness-gaps` | 3 | I |
| Gap resolved and remediationSuggestion patchable | `hammer-readiness-gaps` | 3 | V |
| Empty remediationSuggestion rejection with `422` | `hammer-readiness-gaps` | 3 | I |
| Unknown PATCH field rejection with `400` on gap route | `hammer-readiness-gaps` | 3 | I |
| Forbidden gap field rejection with `400` | `hammer-readiness-gaps` | 3 | I |
| Gap PATCH does not re-trigger evaluation or readiness-state sync | `hammer-readiness-gaps` | 3 | I |
| Cross-project evaluation fetch non-leakage | `hammer-scope-isolation` | 1 | I |
| Same-input determinism for readiness evaluation results | `hammer-readiness-reproducibility` | 3 | V |

### Audits (`api/audits.md`)

| Expectation | Module | Phase | Posture |
|---|---|---|---|
| Audit creation with valid input for each supported entity type | `hammer-audits` | 4.5 | V |
| Audit creation with no target entity (project-scoped) | `hammer-audits` | 4.5 | V |
| Malformed UUID rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown query parameter rejection with `400` | `hammer-contracts-read` | 6 | I |
| Forbidden field rejection on audit creation | `hammer-contracts-write` | 6 | I |
| Caller-supplied result rejection with `400` | `hammer-audits` | 4.5 | I |
| Caller-supplied summary rejection with `400` | `hammer-audits` | 4.5 | I |
| Caller-supplied startedAt or completedAt rejection with `400` | `hammer-audits` | 4.5 | I |
| targetEntityId without targetEntityType rejection with `400` | `hammer-contracts-write` | 6 | I |
| targetEntityType without targetEntityId rejection with `400` | `hammer-contracts-write` | 6 | I |
| Invalid auditType rejection with `422` | `hammer-validation` | 6 | I |
| Audit type / target entity type applicability mismatch rejection with `422` | `hammer-audits` | 4.5 | I |
| Cross-project entity reference rejection without leakage | `hammer-scope-isolation` | 1 | I |
| Entity not-found-in-scope returns empty list, not disclosure | `hammer-scope-isolation` | 1 | I |
| Deterministic list ordering for audit runs and gaps | `hammer-ordering` | 6 | V |
| Cursor continuation correctness on audit run list and gap list | `hammer-ordering` | 6 | V |
| Audit run immutability: no mutation path outside staleness route | `hammer-audits` | 4.5 | I |
| Gap creation atomicity with parent audit run | `hammer-audits` | 4.5 | V+I |
| startedAt and completedAt set atomically in creation transaction | `hammer-audits` | 4.5 | V |
| Staleness route: reason required | `hammer-audits` | 4.5 | I |
| Staleness route: already-stale rejection with `422` | `hammer-audits` | 4.5 | I |
| Staleness route atomicity: result, summary, and StatusHistory in one transaction | `hammer-audits` | 4.5 | V+I |
| Staleness StatusHistory row has entityType = 'audit_run' | `hammer-audits` | 4.5 | V |
| Audit run not stale-able from non-terminal prior result | `hammer-audits` | 4.5 | V+I |
| Gap severity and description immutability after creation | `hammer-audits` | 4.5 | I |
| Gap status and remediation patchable | `hammer-audits` | 4.5 | V |
| Illegal gap status transition rejection with `422` | `hammer-audits` | 4.5 | I |
| invalidated terminal: no transition out | `hammer-audits` | 4.5 | I |
| Empty remediation rejection with `422` | `hammer-audits` | 4.5 | I |
| Unknown PATCH field rejection with `400` on gap route | `hammer-audits` | 4.5 | I |
| Forbidden gap field rejection with `400` | `hammer-audits` | 4.5 | I |
| Gap PATCH succeeds on a stale parent audit run | `hammer-audits` | 4.5 | V |
| Cross-project audit run fetch non-leakage | `hammer-scope-isolation` | 1 | I |
| Hard-failure conditions produce `fail` result | `hammer-audits` | 4.5 | V+I |
| Non-blocking conditions can produce `warning` result | `hammer-audits` | 4.5 | V |
| Cross-artifact contradictions are detected | `hammer-cross-artifact-consistency` | 4.5 | V+I |
| Ambiguity detection behaves deterministically | `hammer-ambiguity-detection` | 4.5 | V+I |

### Evidence Links (`api/evidence-links.md`)

| Expectation | Module | Phase | Posture |
|---|---|---|---|
| Creation with valid input for each supported source entity type | `hammer-evidence-links` | 4 | V |
| Omitted note defaults to null on creation | `hammer-evidence-links` | 4 | V |
| Omitted relevanceScore defaults to null on creation | `hammer-evidence-links` | 4 | V |
| Malformed UUID rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown query parameter rejection with `400` | `hammer-contracts-read` | 6 | I |
| Unknown PATCH field rejection with `400` | `hammer-contracts-write` | 6 | I |
| Forbidden field rejection on create and patch | `hammer-contracts-write` | 6 | I |
| sourceEntityId without sourceEntityType rejection with `400` | `hammer-contracts-write` | 6 | I |
| Invalid evidenceType rejection with `422` | `hammer-validation` | 6 | I |
| Empty targetLocator rejection with `422` | `hammer-evidence-links` | 4 | I |
| Out-of-range relevanceScore rejection with `422` | `hammer-evidence-links` | 4 | I |
| Non-integer relevanceScore rejection with `400` | `hammer-evidence-links` | 4 | I |
| Empty note string rejection with `422` | `hammer-evidence-links` | 4 | I |
| note cleared to null through PATCH | `hammer-evidence-links` | 4 | V |
| relevanceScore cleared to null through PATCH | `hammer-evidence-links` | 4 | V |
| Same-project source entity validation on create | `hammer-scope-isolation` | 1 | I |
| Cross-project source entity reference rejection without leakage | `hammer-scope-isolation` | 1 | I |
| Source entity filter non-leakage in list behavior | `hammer-scope-isolation` | 1 | I |
| Deterministic list ordering | `hammer-ordering` | 6 | V |
| Cursor continuation correctness | `hammer-ordering` | 6 | V |
| Identity field immutability: sourceEntityType, sourceEntityId, evidenceType, targetLocator not patchable | `hammer-evidence-links` | 4 | I |
| Creating a new link does not supersede prior links for the same source entity | `hammer-evidence-links` | 4 | V |
| Cross-project fetch/patch non-leakage | `hammer-scope-isolation` | 1 | I |

---

## Section 4 — Concurrency Probe Coverage

These map the required concurrency scenarios from `hammer-plan.md` to modules and phases.

All entries use `—` (module planned and assigned, specific test not yet written).

| Scenario | Module | Phase | Status |
|---|---|---|---|
| Concurrent status transitions on the same record | `hammer-state-transitions` | 2 | — |
| Concurrent duplicate dependency creation | `hammer-dependencies` | 1 | — |
| Concurrent duplicate readiness evaluation trigger | `hammer-readiness-core` | 3 | — |
| Concurrent project-scoped unique key creation (projects) | `hammer-core-projects` | 1 | — |
| Concurrent project-scoped unique key creation (work items) | `hammer-core-work-items` | 1 | — |

All concurrency probes are currently unimplemented. These are the highest-risk first-pass scenarios and must be addressed before claiming Phase 1, 2, or 3 is hardened.

---

## Section 5 — Integration Scenario Coverage

These map the integration scenarios from `hammer-plan.md` Phase 5 to modules.

All entries use `—` (module planned and assigned, specific test not yet written).

| Scenario | Module | Phase | Status |
|---|---|---|---|
| Stale external references flagged during audit or readiness | `hammer-cross-system-references` | 5 | — |
| Invalid external identifiers rejected at write time | `hammer-cross-system-references` | 5 | — |
| Cross-project external reference rejection | `hammer-scope-isolation` | 1 | — |
| LLM-introduced capture context remains distinguishable from source evidence | `hammer-evidence-links` | 4 | — |
| Observatory-shaped payload rejected at Project V write surface | `hammer-boundary-enforcement` | 5 | — |
| Execution-shaped payload rejected at Project V write surface | `hammer-boundary-enforcement` | 5 | — |

---

## Section 6 — Coverage Gaps

The following are known gaps as of the initial version of this map. `—` indicates a planned module with no tests written yet. `(unassigned)` would indicate no module exists; all items below have module assignments from `hammer-plan.md`.

### High-priority gaps — these must be addressed before claiming any phase is hardened

- **All concurrency probes (Section 4):** `—` — modules assigned, no tests written. Concurrency failures are the highest-risk silent failures in a multi-project system; these cannot be deferred past Phase 1–3 implementation.
- **All integration scenarios (Section 5):** `—` — modules assigned, no tests written. Required before Phase 5 is considered hardened.
- **`hammer-cross-artifact-consistency`:** `—` — covers audit cross-artifact contradiction detection; blocks Phase 4.5 hardening.
- **`hammer-ambiguity-detection`:** `—` — covers BYDA material vs advisory ambiguity classification; blocks Phase 4.5 hardening.
- **`hammer-audit-readiness-coupling`:** `—` — covers required-audit-fail constraining readiness; blocks Phase 4.5 hardening. Without this, the audit-to-readiness coupling in `readiness-evaluation-rules.md` is declared but unverified.

### Lower-priority gaps — important but not blocking early phases

- **`hammer-derived-honesty`:** `—` — covers imported/derived records not masquerading as canonical truth. Lower priority because no current API family exposes a direct mutation surface for derived convenience data; the risk surface is smaller than the boundary and atomicity risks above.
- **`hammer-research-docs`:** `—` — covers ResearchDoc boundary posture. Lower priority because ResearchDoc routes have not yet been written as an API family doc; coverage cannot be completed until the API family authority doc exists.
- **`hammer-readiness-reproducibility`:** `—` — covers same-input determinism testing for readiness evaluations. Lower priority because determinism failures are detectable through repeated evaluation runs during normal development; this is catch-up verification rather than primary gate verification.

---

## Update Rule

This document must be updated when:

- a new hammer module is added, retired, or renamed
- a new API family authority doc is added that includes hammer expectations
- a new invariant is added to `system-invariants.md`
- a coverage gap is resolved (change `—` to `V`, `I`, or `V+I` and remove from Section 6)
- a concurrency probe or integration scenario is implemented
- a module changes phase assignment

Do not defer this update until the end of a work session.
A stale coverage map is a false confidence claim.

---

## Related Docs

- `hammer-doctrine.md`
- `hammer-plan.md`
- `system-invariants.md`
- `api-conventions.md`
- `schema-specification.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `status-transitions.md`
- `../governance/testing-and-verification-doctrine.md`
- `project-v/api/objectives.md`
- `project-v/api/initiatives.md`
- `project-v/api/work-items.md`
- `project-v/api/dependencies.md`
- `project-v/api/handoffs.md`
- `project-v/api/readiness.md`
- `project-v/api/audits.md`
- `project-v/api/evidence-links.md`
