# Audit GitHub Issue Creation Sequence

Date: 2025-04-05
Repo: `C:\dev\v-ecosystem-docs`

---

## 1. Purpose of this sequence

This document defines the order in which GitHub issues should be **opened** — not necessarily the order in which they will be completed. Opening issues before their dependencies are resolved creates noise: assignees have nowhere to start, scope may shift after a design decision, and the tracker becomes a list of blocked items with no clear next action.

The sequence below keeps the tracker clean by front-loading the issues that are immediately actionable, staging the decision gates explicitly, and holding downstream work in backlog until the gates that constrain their scope are closed.

---

## 2. Sequencing principles

**Open only what is actionable.** An issue is actionable when its scope is stable and an assignee can start work. Issues whose scope depends on an unresolved architectural decision should stay in draft or backlog.

**Decision gates block their downstream issues.** ISSUE-AD-01 through ISSUE-AD-04 are architectural decisions, not documentation tasks. Their downstream issues cannot be scoped correctly until the decision is made. Opening downstream issues before these decisions are resolved creates phantom scope.

**Blocker issues open before everything else.** ISSUE-01 and the four AD issues are blockers. They define what is correct before anyone else writes code or docs against the affected paths.

**Parallel batches are explicit.** Issues that have no dependency on each other can be opened in the same batch and assigned simultaneously.

**Issue creation ≠ issue readiness.** Some issues can be created in a "draft" or "backlog" state with a note that they are gated on a specific decision. This gives visibility into the full scope without implying the work is ready to start.

---

## 3. Suggested issue labels and metadata

Apply these labels consistently across all issues.

### Priority labels
| Label | Meaning |
|---|---|
| `priority:blocker` | Unsafe to proceed without this resolved |
| `priority:high` | Required before affected seam can be implemented |
| `priority:medium` | Required before repo is fully implementation-safe |
| `priority:low` | Cleanup; does not block implementation |

### Phase labels
| Label | Meaning |
|---|---|
| `phase:0` | Stop-ship corrections |
| `phase:1` | Governance and seam infrastructure |
| `phase:2` | Missing/incomplete interface contracts |
| `phase:3` | Activity trail and approval integration |
| `phase:4` | Workflow codability repairs |
| `phase:5` | Vocabulary and consistency cleanup |

### Workstream labels
| Label | Meaning |
|---|---|
| `ws:governance` | Access governance corrections (WS-A) |
| `ws:known-fixes` | Pre-specified bounded patches (WS-B) |
| `ws:interfaces` | Missing or incomplete interface docs (WS-C, WS-D) |
| `ws:activity-trail` | Activity trail wiring and coverage (WS-E) |
| `ws:approval-seam` | Human approval mechanics (WS-F) |
| `ws:workflows` | Workflow codability repairs (WS-G) |
| `ws:vocabulary` | Vocabulary and consistency cleanup (WS-H) |
| `ws:decision` | Architectural decision gate |

### Status labels
| Label | Meaning |
|---|---|
| `status:ready` | Actionable now; no unresolved gates |
| `status:gated` | Depends on an unresolved decision; do not start |
| `status:draft` | Created for tracking visibility; scope may shift |
| `status:backlog` | Low priority; open but not in current wave |

### System labels (apply when an issue primarily touches one system)
| Label |
|---|
| `system:project-v` |
| `system:veda` |
| `system:v-forge` |
| `system:ecosystem` |
| `system:cross-system` |

---

## 4. Batch 0 — Open immediately

These are the first issues to open. They are actionable right now and gate everything else. Do not wait for any of these to complete before opening them; they can all be opened on day one.

**ISSUE-01** — Rewrite `ecosystem/cross-system-access-governance.md`
**ISSUE-AD-01** — Resolve push/pull transport model for handoff/signal delivery
**ISSUE-AD-02** — Reconcile dual VEDA → V Forge access models
**ISSUE-AD-03** — Define Project V → VEDA evidence request path model
**ISSUE-AD-04** — Decide centralized vs distributed approval mechanics location

**Why open all five immediately:** ISSUE-01 is a stop-ship correction with no dependencies. The four AD issues are architectural decisions that gate multiple downstream issues. Opening them all in Batch 0 signals to the team which decisions are blocking and allows parallel work on the decisions while ISSUE-01 is being executed.

ISSUE-AD-01 and ISSUE-AD-02 are related (both concern transport model); consider assigning them to the same person or pairing them in a single decision session.

---

## 5. Batch 1 — Open after ISSUE-01 exists

ISSUE-02 can be opened as soon as ISSUE-01 is created (not completed). Its patches do not touch `cross-system-access-governance.md`, so there is no merge conflict risk. Mark it `status:ready` immediately.

**ISSUE-02** — Apply known-fixes patch set and two new confirmed vocabulary corrections

Also at this stage, open with `status:draft` so the scope is visible:
**ISSUE-03** — Create stubs for the five missing interface documents

Mark ISSUE-03 with `status:gated` on ISSUE-AD-01 (for items 1 and 2 specifically). Items 3, 4, and 5 of ISSUE-03 can begin before AD decisions resolve — flag this in the issue body so the assignee knows which sub-items are unblocked.

---

## 6. Batch 2 — Open after architectural decisions are resolved (AD-01 through AD-04 closed)

Once the four decision gates close, open the following issues. Their scope is now stable.

**ISSUE-04** — Upgrade four primary interface docs from semantic to implementation contracts
**ISSUE-05** — Create `ecosystem/activity-trail-integration-map.md`
**ISSUE-07** — Define human approval mechanics at the seam level

Note: ISSUE-05 can be opened as a `status:draft` as soon as ISSUE-03 stubs are created, but it becomes `status:ready` only after ISSUE-04 is complete (the map needs to cover the complete upgraded interface set).

ISSUE-07's scope is gated on ISSUE-AD-04. Open it only after that decision is made.

**Also open at this stage:**
**ISSUE-13** — Add canonical definitions for five undefined load-bearing terms to `ecosystem/vocabulary.md`
**ISSUE-14** — Specify the `actor` field format in Project V schema

These do not depend on the AD decisions but benefit from ISSUE-07 being underway (to clarify the scope of "governance-sensitive"). Open them in `status:ready` — they can proceed in parallel with ISSUE-04.

---

## 7. Batch 3 — Open once seam infrastructure is defined (ISSUE-04 and ISSUE-05 complete)

These issues depend on the interface contracts being written and the activity trail integration map existing.

**ISSUE-06** — Wire activity trail logging into all nine interface docs
**ISSUE-08** — Repair `workflows/handoff-workflow.md` codability
**ISSUE-09** — Repair `workflows/project-intake-workflow.md` codability
**ISSUE-10** — Repair `workflows/maintenance-and-replanning-workflow.md` codability
**ISSUE-11** — Repair `workflows/launch-readiness-workflow.md` codability
**ISSUE-12** — Repair `workflows/post-launch-observation-workflow.md` codability

ISSUE-06 should be opened as soon as ISSUE-05 (integration map) is complete.

ISSUE-08 through ISSUE-12 should be opened when both ISSUE-06 is underway and ISSUE-07 is complete (so the approval mechanics can be referenced in the workflow repair). However, ISSUE-10 and ISSUE-12 (maintenance-and-replanning and post-launch-observation) have fewer missing-interface dependencies and can be opened and started slightly ahead of ISSUE-08, ISSUE-09, and ISSUE-11.

Opening order within this batch: ISSUE-06, ISSUE-10, ISSUE-12, then ISSUE-08, ISSUE-09, ISSUE-11.

---

## 8. Batch 4 — Backlog / cleanup issues

Open these in backlog at any point after Batch 1 completes. They are low urgency and do not block implementation.

**ISSUE-15** — Remove or archive stale superseded docs from active folders
**ISSUE-16** — Resolve the `v-forge/vs-veda.md` ADR-003 dangling reference

These can be opened immediately if you want them tracked, but mark them `status:backlog` so they do not pollute the active work queue.

---

## 9. Per-issue opening notes

### ISSUE-01 — Rewrite `ecosystem/cross-system-access-governance.md`
- **When to open:** Day one
- **Status on open:** `status:ready`
- **Labels:** `priority:blocker`, `phase:0`, `ws:governance`, `system:ecosystem`
- **Dependency note:** None
- **Scope risk:** None — the errors are confirmed and the corrections are specified

---

### ISSUE-02 — Apply known-fixes patch set and two new confirmed vocabulary corrections
- **When to open:** Day one (simultaneous with Batch 0)
- **Status on open:** `status:ready`
- **Labels:** `priority:high`, `phase:1`, `ws:known-fixes`, `system:ecosystem`
- **Dependency note:** Does not touch the same files as ISSUE-01; no merge conflict risk
- **Scope risk:** None — all items are pre-specified

---

### ISSUE-03 — Create stubs for the five missing interface documents
- **When to open:** After ISSUE-01 is created (Batch 1)
- **Status on open:** `status:draft` (partially gated)
- **Labels:** `priority:high`, `phase:2`, `ws:interfaces`, `system:cross-system`
- **Dependency note:** Items 3, 4, 5 (scope clarification, handoff recall, scope update) are unblocked. Items 1 and 2 (evidence request, scope expansion) are gated on ISSUE-AD-03 and ISSUE-AD-01 respectively.
- **Scope risk:** Items 1 and 2 may require structural changes to their stubs once the AD decisions resolve. Note this in the issue body.

---

### ISSUE-04 — Upgrade four primary interface docs from semantic to implementation contracts
- **When to open:** After ISSUE-AD-01 and ISSUE-AD-02 are resolved (Batch 2)
- **Status on open:** `status:ready`
- **Labels:** `priority:high`, `phase:2`, `ws:interfaces`, `system:cross-system`
- **Dependency note:** ISSUE-AD-01 required (transport model); ISSUE-AD-02 required (VEDA → V Forge reconciliation); ISSUE-03 stubs should exist
- **Scope risk:** The `veda-to-v-forge-signal-interface.md` upgrade scope depends directly on ISSUE-AD-02 resolution. Do not begin that doc's upgrade until AD-02 is closed.

---

### ISSUE-05 — Create `ecosystem/activity-trail-integration-map.md`
- **When to open:** After ISSUE-AD-01/AD-02 resolve; ISSUE-03 stubs exist (Batch 2)
- **Status on open:** `status:draft` until ISSUE-04 is complete; `status:ready` after ISSUE-04
- **Labels:** `priority:high`, `phase:3`, `ws:activity-trail`, `system:ecosystem`
- **Dependency note:** Needs the upgraded interface docs to be complete so the map covers accurate contracts. Can begin drafting the map structure before ISSUE-04 is done.
- **Scope risk:** If the activity trail vocabulary is extended (new action types for return-to-planning delivery, lifecycle transitions), the map may need revision after ISSUE-06. Plan for one revision pass.

---

### ISSUE-06 — Wire activity trail logging into all nine interface docs
- **When to open:** After ISSUE-05 is complete (Batch 3)
- **Status on open:** `status:ready`
- **Labels:** `priority:high`, `phase:3`, `ws:activity-trail`, `system:cross-system`
- **Dependency note:** ISSUE-05 must be complete — the logging sections reference the action types and field mappings from the integration map
- **Scope risk:** None once ISSUE-05 is complete

---

### ISSUE-07 — Define human approval mechanics at the seam level
- **When to open:** After ISSUE-AD-04 is resolved; ISSUE-04 underway (Batch 2)
- **Status on open:** `status:ready` (after AD-04 closes)
- **Labels:** `priority:high`, `phase:3`, `ws:approval-seam`, `system:cross-system`
- **Dependency note:** ISSUE-AD-04 determines whether output is additions to interface docs or a new governance doc. Scope of work changes meaningfully depending on the decision.
- **Scope risk:** High until AD-04 closes. Do not start until the decision is made.

---

### ISSUE-08 — Repair `workflows/handoff-workflow.md` codability
- **When to open:** After ISSUE-07 is complete (Batch 3)
- **Status on open:** `status:ready`
- **Labels:** `priority:high`, `phase:4`, `ws:workflows`, `system:cross-system`
- **Dependency note:** ISSUE-07 required (approval mechanics at Stage 3); ISSUE-06 recommended (activity trail wiring gives observable state targets)
- **Scope risk:** Stage 3 human approval section cannot be completed until ISSUE-07 is done

---

### ISSUE-09 — Repair `workflows/project-intake-workflow.md` codability
- **When to open:** After ISSUE-07 and ISSUE-03 item 1 are complete (Batch 3)
- **Status on open:** `status:gated` until ISSUE-03 item 1 exists
- **Labels:** `priority:high`, `phase:4`, `ws:workflows`, `system:project-v`
- **Dependency note:** The "request additional bounded evidence" outcome in Stage 5 cannot be specified without ISSUE-03 item 1 existing. Human approval at Stage 4 requires ISSUE-07.
- **Scope risk:** If ISSUE-AD-03 produces an unexpected evidence request model, the Stage 5 transition in this workflow may need revision.

---

### ISSUE-10 — Repair `workflows/maintenance-and-replanning-workflow.md` codability
- **When to open:** After ISSUE-07 is complete; ISSUE-03 item 5 (scope update interface) exists (Batch 3)
- **Status on open:** `status:ready` (after ISSUE-07)
- **Labels:** `priority:medium`, `phase:4`, `ws:workflows`, `system:project-v`
- **Dependency note:** Stage 5 human review requires ISSUE-07; Stage 6 post-replanning notification requires ISSUE-03 item 5
- **Scope risk:** Low — the trigger list and escalation condition are already well-specified in the doc; additions are primarily structural

---

### ISSUE-11 — Repair `workflows/launch-readiness-workflow.md` codability
- **When to open:** After ISSUE-07 is complete (Batch 3)
- **Status on open:** `status:ready`
- **Labels:** `priority:medium`, `phase:4`, `ws:workflows`, `system:cross-system`
- **Dependency note:** Stage 5 authorization requires ISSUE-07; Stage 4 cross-system confirmation requires all systems' interface docs to be upgraded (ISSUE-04)
- **Scope risk:** Stage 4 is the most complex transition — the "cross-system readiness confirmation artifact" definition may require coordination between Project V, VEDA, and V Forge owners

---

### ISSUE-12 — Repair `workflows/post-launch-observation-workflow.md` codability
- **When to open:** After ISSUE-07 is complete; ISSUE-03 stubs exist (Batch 3)
- **Status on open:** `status:ready`
- **Labels:** `priority:medium`, `phase:4`, `ws:workflows`, `system:cross-system`
- **Dependency note:** Stage 6 escalation routing requires ISSUE-07; otherwise this is the most self-contained of the five workflow repairs
- **Scope risk:** Low — the primary work (defining "governed intervals" and "materially significant signal event") is doc-internal and does not require external design decisions

---

### ISSUE-13 — Add canonical definitions for five undefined load-bearing terms to `ecosystem/vocabulary.md`
- **When to open:** After ISSUE-02 is complete; after ISSUE-07 is underway (to scope "governance-sensitive") (Batch 2)
- **Status on open:** `status:ready`
- **Labels:** `priority:medium`, `phase:5`, `ws:vocabulary`, `system:ecosystem`
- **Dependency note:** Soft dependency on ISSUE-07 for the "governance-sensitive" definition scope; can draft other four terms in parallel
- **Scope risk:** Low for four of the five terms; "governance-sensitive" definition benefits from ISSUE-07 being resolved first

---

### ISSUE-14 — Specify the `actor` field format in Project V schema
- **When to open:** After ISSUE-02 is complete (Batch 2)
- **Status on open:** `status:ready`
- **Labels:** `priority:medium`, `phase:5`, `ws:vocabulary`, `system:project-v`
- **Dependency note:** No blocking dependencies; independent of AD decisions
- **Scope risk:** Low — the format decision (structured type vs enum) is internal to Project V schema governance

---

### ISSUE-15 — Remove or archive stale superseded docs from active folders
- **When to open:** Any time; backlog
- **Status on open:** `status:backlog`
- **Labels:** `priority:low`, `phase:5`, `ws:vocabulary`, `system:ecosystem`
- **Dependency note:** None
- **Scope risk:** None — purely mechanical archiving/marking work

---

### ISSUE-16 — Resolve the `v-forge/vs-veda.md` ADR-003 dangling reference
- **When to open:** Any time; backlog
- **Status on open:** `status:backlog`
- **Labels:** `priority:low`, `phase:5`, `ws:vocabulary`, `system:v-forge`
- **Dependency note:** None
- **Scope risk:** If the team decides to create ADR-003 formally, scope expands slightly; if not, it is a single reference change

---

### ISSUE-AD-01 — Resolve the push/pull transport model for handoff/signal delivery
- **When to open:** Day one
- **Status on open:** `status:ready`
- **Labels:** `priority:blocker`, `phase:1`, `ws:decision`, `system:cross-system`
- **Dependency note:** None — this is an originating decision
- **Scope risk:** N/A (this IS the decision)

---

### ISSUE-AD-02 — Reconcile dual VEDA → V Forge access models
- **When to open:** Day one
- **Status on open:** `status:ready`
- **Labels:** `priority:blocker`, `phase:1`, `ws:decision`, `system:veda`, `system:v-forge`
- **Dependency note:** Related to ISSUE-AD-01; consider resolving together in a single session
- **Scope risk:** N/A

---

### ISSUE-AD-03 — Define the Project V → VEDA evidence request path model
- **When to open:** Day one
- **Status on open:** `status:ready`
- **Labels:** `priority:high`, `phase:1`, `ws:decision`, `system:project-v`, `system:veda`
- **Dependency note:** Related to ISSUE-AD-01 (transport model may constrain options)
- **Scope risk:** N/A

---

### ISSUE-AD-04 — Decide centralized vs distributed approval mechanics location
- **When to open:** Day one
- **Status on open:** `status:ready`
- **Labels:** `priority:high`, `phase:1`, `ws:decision`, `system:cross-system`
- **Dependency note:** None
- **Scope risk:** N/A

---

## 10. Suggested first-week issue opening sequence

Open in this order during the first wave:

**Day 1:**
1. ISSUE-01 — `status:ready` — assign immediately
2. ISSUE-AD-01 — `status:ready` — assign to tech lead or decision group
3. ISSUE-AD-02 — `status:ready` — pair with ISSUE-AD-01
4. ISSUE-AD-03 — `status:ready` — assign to Project V / VEDA owner
5. ISSUE-AD-04 — `status:ready` — assign to governance or doc lead

**Day 1–2 (after ISSUE-01 is created):**

6. ISSUE-02 — `status:ready` — assign immediately; can proceed in parallel with ISSUE-01
7. ISSUE-03 — `status:draft` — open for tracking; mark items 1 and 2 as gated, items 3–5 as ready

**After ISSUE-02 is in flight:**

8. ISSUE-15 — `status:backlog` — open for tracking; no urgency
9. ISSUE-16 — `status:backlog` — open for tracking; no urgency

---

## 11. Suggested follow-on opening sequence

**After ISSUE-AD-01 and ISSUE-AD-02 close:**
- ISSUE-04 — `status:ready`
- ISSUE-13 — `status:ready`
- ISSUE-14 — `status:ready`

**After ISSUE-AD-04 closes:**
- ISSUE-07 — `status:ready`

**After ISSUE-03 stubs are created:**
- ISSUE-05 — `status:draft` (becomes ready after ISSUE-04 completes)

**After ISSUE-04 is complete:**
- ISSUE-05 — flip to `status:ready`

**After ISSUE-05 is complete:**
- ISSUE-06 — `status:ready`

**After ISSUE-07 is complete:**
- ISSUE-08 — `status:ready`
- ISSUE-09 — `status:gated` on ISSUE-03 item 1; flip to `status:ready` when item 1 exists
- ISSUE-10 — `status:ready`
- ISSUE-11 — `status:ready`
- ISSUE-12 — `status:ready`

---

## 12. Anti-patterns to avoid

**Do not open all 20 issues on day one.** Issues gated on unresolved architectural decisions will sit in a blocked state, creating tracker noise and giving the impression that work is stalled when it is actually gated by a decision.

**Do not mark gated issues as `status:ready`.** An issue is not ready if its scope will change when a decision resolves. Use `status:gated` and note the specific decision gate in the issue body.

**Do not open ISSUE-04 before ISSUE-AD-01 and ISSUE-AD-02 are resolved.** The interface contract work for `veda-to-v-forge-signal-interface.md` depends on the dual-access model decision. Opening and assigning ISSUE-04 before that decision is made means the assignee will work on scope that may be invalidated.

**Do not open ISSUE-07 before ISSUE-AD-04 is resolved.** The approval mechanics output is either additions to interface docs or a new governance doc. These require very different scopes and different assignees. Pre-opening forces the assignee to wait.

**Do not assign ISSUE-08, ISSUE-09, ISSUE-11 before ISSUE-07 is complete.** Human approval stages in those workflows reference the mechanics defined in ISSUE-07. Without ISSUE-07, the workflow repair is incomplete by design.

**Do not split the AD decision issues into smaller sub-tasks.** Each architectural decision should be one issue with one owner and one output: a documented decision. Splitting them fragments accountability.

**Do not use the remediation plan workstream labels as status.** A workstream label (`ws:interfaces`) identifies what kind of work it is, not whether it is done. Do not repurpose it as a completion indicator.

---

## 13. Closing note

The sequencing above concentrates the first week on two things: fixing the one doc that actively misdirects (ISSUE-01) and running the decision gates that everything downstream needs (AD-01 through AD-04). Everything else waits on those five outputs.

The four AD decisions are the true critical path. If the team resolves them quickly, Batches 2 and 3 can begin in rapid succession. If the decisions drag, the work in Phases 2–4 remains correctly staged in backlog rather than accumulating phantom scope.

The ownership split — Project V owns planning truth, VEDA owns signal/evidence/observability truth, V Forge owns execution truth — does not change as a result of any of the design decisions. The decisions affect transport model and spec location, not system identity or role boundaries. That split is the one architectural conclusion the audit confirmed as correct, and no issue in this sequence should produce output that challenges it.
