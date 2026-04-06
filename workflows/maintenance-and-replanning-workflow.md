# Maintenance and Replanning Workflow

## Purpose

This document defines the governed workflow by which V Forge execution findings
re-enter Project V planning reconsideration and produce a downstream governed outcome.

It exists to answer:

```text
What stages does the return-to-planning / replanning workflow move through, what
event causes each transition, what pending state applies, when may Project V act
and when must it wait, how do receipt, review, and planning mutation differ, and
what governed path does each replanning outcome route into?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the concrete stage sequence from V Forge return-to-planning delivery through
  Project V receipt, governed review, replanning, and downstream outcome routing
- entry conditions and return-package validity posture
- review gate behavior and canonical pending state
- receipt, review, and planning mutation as distinct phases
- degraded-mode and interruption handling
- re-entry rules when basis changes during pending review
- downstream routing into scope update, new handoff, execution clarification,
  deferral, cancellation, or no-change
- activity-trail obligations for all return-to-planning events
- maintenance vs replanning distinction

---

## Out of Scope

This document does not define:

- the return-to-planning interface data contract — that belongs in
  `interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- full approval class definitions and escalation principles — those belong in
  `governance/approval-and-escalation-model.md` and
  `governance/approval-mechanics-seam-model.md`
- Project V internal decision records or planning mutation mechanics
- V Forge internal execution workflow or how V Forge decides to return findings
- detailed failure recovery mechanics below the workflow level
- the original handoff workflow — that belongs in `workflows/handoff-workflow.md`
- VEDA signal delivery to Project V — that is governed by
  `interfaces/veda-to-project-v-signal-interface.md`

---

## System

- workflows

---

## Relationship to Governing Interface Docs

This workflow governs sequencing and transition rules. The interface contracts govern
what packages must carry.

- `interfaces/v-forge-to-project-v-return-to-planning-interface.md` — defines the
  return package semantics, validity conditions, delivery model, and boundary rules.
  This workflow must remain consistent with that contract.
- `governance/approval-mechanics-seam-model.md` — defines the shared seam-level
  approval mechanics pattern used at Stage 3. This workflow carries the seam-specific
  facts; the mechanics doc carries the shared pattern.
- `ecosystem/activity-trail-integration-map.md` — defines the canonical action type
  mapping for all activity-trail records produced by this workflow.

---

## Core Rule

Receipt, review, and planning mutation are three distinct required phases.
None may substitute for or imply the others.

- **Receipt** — Project V confirms the V Forge return package has arrived
- **Review** — a human or governed review determines whether and how Project V
  should respond to the findings
- **Planning mutation** — Project V changes planning state based on the
  governed review outcome

Planning mutation must not occur before receipt and review are complete.
Returned findings do not self-apply as planning changes.

---

## Key Distinctions

### Maintenance vs Replanning

Maintenance is ongoing bounded work within existing approved scope that does not
require reconsideration of prior governing decisions.

Replanning is a governed reconsideration of prior planning decisions triggered
by execution findings, changed conditions, or new signal that affects the planning
basis.

Maintenance does not require this workflow.
Replanning does.

If a maintenance action changes a governing decision, it is replanning, not
maintenance, regardless of how it is labeled.

### Return-to-Planning vs Planning Mutation

Return-to-planning is the governed transfer of bounded execution findings from
V Forge to Project V. It is not automatic authorization to change planning state.

Planning mutation is the actual change of planning records, decisions, or
orchestration state. It may follow return-to-planning after governed review,
but does not follow automatically.

### Replanning vs Scope Creep

Replanning is a bounded, governed reconsideration of specific planning decisions
affected by new information. Scope creep is the gradual expansion of planning
through accumulated assumptions or execution-side findings treated as planning
authority without going through this workflow.

---

## Entry Conditions

This workflow is triggered when one or more of the following occur:

- V Forge delivers a valid return-to-planning package through
  `interfaces/v-forge-to-project-v-return-to-planning-interface.md` containing
  execution findings that materially affect the planning basis
- execution is blocked, failed, or incomplete in a way that cannot be resolved
  within the approved handoff scope
- changed execution conditions invalidate assumptions that underpinned a prior
  handoff or governing planning decision
- an operator identifies planning drift that requires explicit reconsideration

This workflow is **not** triggered by:

- execution findings that V Forge can resolve within the approved scope
- bounded maintenance activity within already-approved scope
- minor execution variations that do not affect the planning basis
- VEDA signal that arrives without an associated execution finding or handoff impact
  (VEDA signal routes through `interfaces/veda-to-project-v-signal-interface.md`
  and may trigger planning reconsideration at Stage 4 of the intake workflow instead)

---

## Workflow Stages

### Stage 1 — Return Package Delivery and Receipt

**Entry event:** V Forge initiates return-to-planning delivery through the governed
return-to-planning interface.

**What happens at this stage:**
Project V receives the V Forge return package. Project V confirms receipt. Receipt
confirmation signals that the package has arrived and is available for review — it
does not mean review has occurred or planning has changed.

**Exit condition → Stage 2:** Project V confirms receipt.
**Exit condition → Stage 6a (degraded):** Project V is unavailable or confirmation is
not returned within the expected window.
**Exit condition → Stage 6b (invalid):** Project V receives the package but it fails
validity conditions.

**Activity trail:** `execution.return` record produced by V Forge on delivery;
`execution.return.confirmed` record produced by Project V on confirmation.

**Boundary rule:** V Forge retains ownership of execution truth after delivering
findings. Receipt does not transfer execution ownership to Project V. Project V
does not begin planning mutation at this stage.

---

### Stage 2 — Trigger Classification and Validity Assessment

**Entry event:** Return package receipt confirmed at Stage 1.

**What happens at this stage:**
Project V classifies the trigger and assesses the return package:

- confirms the package is tied to a real handoff or bounded execution context
- confirms findings are bounded and planning-relevant, not an unrestricted dump
- identifies which prior governing decisions are potentially affected
- determines whether the trigger is material enough to warrant review-gated
  replanning vs maintenance-only response

**Exit condition → Stage 3:** Trigger is classified as material; review is required.
**Exit condition → Stage 7 (no-change):** Trigger is classified as not warranting
replanning (findings can be addressed within current scope without changing planning).

**Fallback:** If the return package cannot be classified — it is ambiguous, incomplete
after validity check, or the affected decisions cannot be identified — Project V must
surface the gap explicitly rather than proceeding on assumption. This may trigger
escalation.

**Boundary rule:** Classification must not itself constitute a planning mutation.
Recognizing that reconsideration is needed is not the same as deciding the outcome.

---

### Stage 3 — Review Request Generated

**Entry event:** Trigger classified as material at Stage 2; human review required
before planning reconsideration proceeds.

**What happens at this stage:**
Project V generates the review request per the approval mechanics model. The request
must contain: the return findings summary, which prior planning decisions are affected,
the proposed reconsideration scope, and what happens on each review outcome.

**Pending state:** `awaiting_review` — begins immediately on review request generation.
No planning mutation may occur while in `awaiting_review`.

**Activity trail:** `approval.request` record produced by Project V. Required fields
from `ecosystem/activity-trail-integration-map.md` Section 5b: `entity_type:
execution_return`, `entity_id: <return package identity>`, `approval_class`,
`originating_handoff_ref`, `review_trigger_summary`.

**Exit condition → Stage 4:** A governed review decision is received.
**Exit condition → Stage 5 (escalation):** Review is escalated.
**Exit condition → Stage 6c (stale):** Findings become superseded or basis changes
materially before review completes.

**Boundary rule:** While in `awaiting_review`, planning must remain in its current
state. A received return package does not mutate planning truth until review says so.

---

### Stage 4 — Review Decision Received

**Entry event:** Human operator or governed review surface reaches a decision.

**Decision outcomes and workflow consequences:**

| Outcome | Workflow action |
|---|---|
| `approved` | Proceed to Stage 5 (replanning scope determination) |
| `rejected` | Proposed reconsideration does not proceed. Return findings are preserved. Planning remains in current state. Exit via Stage 7 (no-change or defer). |
| `escalated` | Enter Stage 5a (escalation handling). Workflow remains in `awaiting_review`. |
| `expired` | Prior review basis may be stale. Re-evaluate at Stage 6c before generating a new review request. |

**Activity trail:** `approval.decide` record at decision time. Required fields from
integration map Section 5b: `entity_type: execution_return`, `entity_id: <return
package identity>`, `approval_class`, `decision`, `reconsideration_path` if approved.

**Boundary rule:** Review approval authorizes planning mutation. It does not constitute
planning mutation. Stage 5 (replanning) must still proceed before planning state changes.

---

### Stage 5 — Replanning Scope Determination and Execution

**Entry event:** Review `approved` outcome from Stage 4.

**What happens at this stage:**
Project V retrieves prior decision context, determines the bounded replanning scope,
and performs the governed replanning work within that scope.

**Replanning scope determination:**
- retrieve the relevant prior governing decisions and handoff basis
- identify which decisions are actually affected by the trigger
- identify which decisions remain valid and should not be reopened
- bound the scope of reconsideration to what the trigger requires

**Replanning execution (within bounded scope):**
- reaffirm prior decisions that remain valid
- revise, supersede, or invalidate decisions where warranted
- prepare the downstream action for the replanning outcome (see Downstream Routing)

**Approval posture:** Replanning decisions that involve superseding or invalidating
prior governing decisions require the approval posture defined in
`governance/approval-mechanics-seam-model.md` Section D (Replanning with Prior
Decision Supersedence). The pending state for that sub-gate is `awaiting_approval`.

If replanning scope cannot be bounded without effectively dissolving all prior
governing decisions, the correct response is escalation — not silent replanning
as a new planning baseline.

**Exit condition → Stage 6 (outcome routing):** Replanning complete; downstream
path determined.

**Boundary rule:** Replanning scope must remain bounded to what the trigger actually
requires. Using a replanning event to reopen unrelated decisions is scope creep.
V Forge retains execution truth. VEDA retains observability truth.

---

### Stage 5a — Escalation Handling

**Entry event:** Review escalated at Stage 4.

**What happens at this stage:**
The workflow remains in `awaiting_review`. No planning mutation proceeds. The
escalation is preserved and routed through the governed escalation path.

**Activity trail:** `approval.escalate` record produced by Project V. Required fields
from integration map Section 5b: `entity_type: execution_return`, `entity_id: <return
package identity>`, `approval_class`, `escalation_reason`.

**Exit condition:** Escalation resolves. Outcome re-enters Stage 4 as a governed
decision.

---

### Stage 6 — Downstream Outcome Routing

**Entry event:** Replanning complete at Stage 5; specific downstream action determined.

This stage routes to the correct governed path based on the replanning outcome. The
options are defined in the Downstream Routing section below.

Each routing option may itself trigger an additional governed workflow (e.g., new
handoff re-enters the handoff workflow; scope update follows its interface).

**Exit condition:** Downstream action initiated through the correct governed path.
The return-to-planning / replanning workflow is complete once routing is confirmed.

---

### Stage 6a — Degraded / Delivery Failed

**Entry event:** V Forge attempts return delivery but Project V is unavailable, or
Project V receipt confirmation not returned within expected window.

**Handling rules:**
- V Forge must retain the package for re-delivery using the same package identity
- V Forge must not assume the return was received
- V Forge may attempt re-delivery; re-delivery produces a new `execution.return`
  record with `is_retry: true` and `prior_delivery_id`
- If conditions materially change during the failure window, proceed to Stage 6c
  (stale/superseded finding assessment)

**Activity trail:** `execution.return.failed` record produced by V Forge. On
re-delivery: `execution.return` record with `is_retry: true`.

**Exit condition → Stage 1:** Project V confirms receipt on re-delivery.

---

### Stage 6b — Return Package Invalid at Receipt

**Entry event:** Project V receives the package but it fails validity conditions
(missing required fields, no originating handoff reference, unbounded scope).

**Handling rules:**
- Project V must not treat an invalid package as a valid return-to-planning event
- Project V must surface the invalidity through governed interruption
- V Forge assesses whether the package can be corrected and re-delivered
- If package is correctable: V Forge revises and re-delivers (new package identity,
  referencing prior as superseded)
- If package cannot be corrected: V Forge and Project V must assess whether the
  underlying execution condition warrants escalation

**Activity trail:** `execution.return.failed` record. If package voided:
`execution.return.voided` record with `void_reason`.

---

### Stage 6c — Stale / Superseded Finding

**Entry event:** Return findings become stale or the execution basis materially changes
before Stage 3 review completes, or a review expires.

**Handling rules:**
- V Forge assesses whether the original package still honestly represents the
  current execution condition
- If basis has materially changed: V Forge delivers an updated package (new package
  identity, superseding prior); prior review request must be closed and re-initiated
  against the updated package
- If basis is still valid within freshness bounds: prior package may be re-confirmed
  and review continues

**Activity trail:** If package superseded: `execution.return.voided` record for the
original package with `superseded_by_ref`. New delivery: `execution.return` record
for the updated package.

**Exit condition → Stage 1:** Re-delivery of updated package.
**Exit condition → Stage 3:** Prior package confirmed still valid; re-initiate review.

---

### Stage 7 — No Change / Defer

**Entry event:** Review rejected at Stage 4, or trigger classified as not warranting
replanning at Stage 2.

**What happens:**
The proposed reconsideration does not proceed. The return findings are preserved as
historical record. Planning remains in its current state. If deferral is the outcome,
the deferral reason and conditions for future reconsideration must be preserved.

This is a governed outcome — a rejected review is not a null event. The rejection
and reason must be traceable.

**Exit condition:** Workflow complete. V Forge remains in its current execution posture
or escalates separately if the blocking condition remains unresolved.

---

## Transition Summary Table

| From | Event | To |
|---|---|---|
| Entry conditions met | V Forge initiates return delivery | Stage 1 |
| Stage 1 | Receipt confirmed | Stage 2 |
| Stage 1 | Delivery failed / confirmation not returned | Stage 6a |
| Stage 1 | Package invalid at receipt | Stage 6b |
| Stage 2 | Trigger material; review required | Stage 3 |
| Stage 2 | Trigger not material | Stage 7 (no-change) |
| Stage 3 | Review request generated; decision pending | Stage 4 |
| Stage 3 | Basis changes before review | Stage 6c |
| Stage 4 | `approved` | Stage 5 |
| Stage 4 | `rejected` | Stage 7 |
| Stage 4 | `escalated` | Stage 5a |
| Stage 4 | `expired` | Stage 6c |
| Stage 5 | Replanning complete; outcome determined | Stage 6 (routing) |
| Stage 5a | Escalation resolves | Stage 4 |
| Stage 6 | Downstream path initiated | Workflow complete |
| Stage 6a | Re-delivery confirmed | Stage 1 |
| Stage 6a | Basis changed during failure | Stage 6c |
| Stage 6b | Revised package re-delivered | Stage 1 |
| Stage 6c | Updated package re-delivered | Stage 1 |
| Stage 6c | Prior package still valid | Stage 3 |
| Stage 7 | — | Workflow complete |

---

## Downstream Routing

After Stage 5 (replanning complete), the outcome routes into one of the following
governed paths. Choose the path that reflects the actual replanning conclusion.

### No Planning Change (→ Stage 7)

Use when: Review finds the prior plan remains valid despite the execution findings.
Planning remains in current state. Return findings are preserved as historical record.

### Scope Update (→ `interfaces/project-v-to-v-forge-scope-update-interface.md`)

Use when: Replanning produces revised scope or constraints that apply to V Forge's
active execution context, but the core execution relationship and handoff remain valid.

A scope update is appropriate when the change is bounded and does not require
re-activating a new handoff.

Distinct from new handoff: if the replanning outcome requires fundamentally different
execution scope or target that cannot be expressed as a delta on the existing handoff,
use the new handoff path instead.

### Execution Clarification (→ `interfaces/project-v-to-v-forge-execution-clarification-interface.md`)

Use when: Replanning produces a bounded clarification or constraint update that V Forge
needs to resolve a specific ambiguity — without changing the scope or requiring a
new handoff.

Use this path only for narrow, bounded clarifications that stay within the existing
approved handoff scope. Do not use it as a substitute for scope update or new handoff.

### New Handoff (→ `workflows/handoff-workflow.md`)

Use when: Replanning produces a revised or substantially changed execution scope that
requires re-entering the handoff workflow with a new handoff package.

The new handoff must go through the full handoff workflow from Stage 1 (preparation)
including approval. A replanning outcome does not bypass the handoff approval gate.

If the replanning includes superseding a prior governing decision, the supersedence
approval requirements from `governance/approval-mechanics-seam-model.md` Section D
apply before the new handoff may be initiated.

### Deferral or Cancellation

Use when: Replanning concludes that the work should be deferred or cancelled outright.
The deferral or cancellation must be recorded as a governed planning outcome — it is
not a null event. Prior governing decisions affected by the deferral or cancellation
must be explicitly addressed (reaffirmed, superseded, or invalidated).

V Forge is notified that execution on the original handoff scope should stop, if it
has not already stopped through the return-to-planning event itself.

---

## Approval Gate: Seam-Specific Facts

Return-to-planning receipt and review is an approval-sensitive seam event. This section
carries the seam-specific facts. The shared mechanics pattern is governed by
`governance/approval-mechanics-seam-model.md`.

| Fact | Value |
|---|---|
| Initiating system for review request | Project V |
| Canonical pending state | `awaiting_review` |
| Approval class | Class B or Class C (scope and strategic impact dependent) |
| Receipt does not equal review approval | True — receipt confirms delivery only |
| Review approval does not equal planning mutation | True — mutation requires replanning at Stage 5 |

For the full mechanics — review request contents, decision re-entry rules, escalation
path, activity trail obligations — see `governance/approval-mechanics-seam-model.md`
Section B (Return-to-Planning Receipt / Review).

If replanning involves superseding a prior governing decision, the additional approval
gate from Section D of the same doc applies.

---

## Adjacent Interface Boundaries

This workflow governs the return-to-planning / replanning path. Adjacent interfaces
handle different concerns and must not be conflated.

**Original handoff (`workflows/handoff-workflow.md`):** Governs Project V → V Forge
transfer of execution responsibility. This workflow begins where the handoff workflow
ends — when V Forge returns findings that require planning reconsideration.

**Return-to-planning interface (`interfaces/v-forge-to-project-v-return-to-planning-interface.md`):**
Governs the data contract and delivery mechanics for Stage 1. This workflow governs
the sequencing around it.

**Handoff recall (`interfaces/project-v-handoff-recall-interface.md`):** Governs
operator-directed recall of a transferred but not-yet-acted handoff. Recall applies
before V Forge has materially acted. Return-to-planning applies after execution is
already underway. Do not conflate.

**VEDA signal delivery to Project V (`interfaces/veda-to-project-v-signal-interface.md`):**
VEDA signal may inform planning reconsideration, but it arrives through its own
governed push delivery path. If VEDA signal triggers planning reconsideration without
an associated V Forge return-to-planning event, it routes through the project intake
or planning evaluation workflow, not this workflow.

**VEDA → V Forge paths (startup push and active query):** These are V Forge execution
intelligence paths that operate independently of the return-to-planning flow. They
are not affected by return-to-planning events unless a new handoff is issued, at
which point VEDA startup signal delivery may be re-triggered for the new scope.

---

## Activity Trail Requirements

All return-to-planning and replanning workflow events must produce activity trail
records using the canonical action types from `ecosystem/activity-trail-integration-map.md`
Sections 3 and 5b.

| Workflow event | Action type | Producing system |
|---|---|---|
| Return delivery initiated (Stage 1) | `execution.return` | V Forge |
| Receipt confirmed (Stage 1) | `execution.return.confirmed` | Project V |
| Delivery failed (Stage 6a) | `execution.return.failed` | V Forge |
| Re-delivery initiated (Stage 6a retry) | `execution.return` with `is_retry: true` | V Forge |
| Package voided / superseded (Stage 6b, 6c) | `execution.return.voided` | V Forge |
| Review request generated (Stage 3) | `approval.request` | Project V |
| Review decision received (Stage 4) | `approval.decide` | Operator / review surface |
| Review escalated (Stage 5a) | `approval.escalate` | Project V |

Activity records that are not produced are not governed events. Implementations
must not skip activity-trail logging for any of the events above.

See `ecosystem/activity-trail-integration-map.md` for the minimum required fields
per event. See `ecosystem/activity-trail-model.md` for base required fields that
apply to every record.

Downstream actions initiated at Stage 6 (scope update, new handoff, etc.) produce
their own activity records per the relevant interface or workflow docs.

---

## Decision Continuity

The replanning workflow must preserve decision continuity throughout:

- replanning events must reference prior governing decisions rather than treating
  them as absent
- replanning scope must identify which decisions are affected and which are not
- replanning outcomes must explicitly address what happened to prior governing
  decisions (reaffirmed, revised, superseded, invalidated)
- the connection between trigger, reconsideration, and outcome must be traceable
- a replanning event that leaves no durable record has not produced governed
  continuity — it has produced drift

See `governance/decision-continuity-doctrine.md` for the full doctrine.

---

## Human-In-The-Loop Principle

Return-to-planning and replanning are governance-sensitive because they change what
the ecosystem will do next. Human review may be required when:

- replanning involves superseding or invalidating prior governing decisions
- replanning involves significant scope change or priority shift
- replanning involves revised handoff activation
- replanning affects cross-system approval posture
- the trigger involves external paid actions or evidence

The approval class and mechanics are defined in `governance/approval-and-escalation-model.md`
and `governance/approval-mechanics-seam-model.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the return-to-planning / replanning workflow has eight distinct named stages
  with concrete transitions
- receipt, review, and planning mutation are three separate required phases
- `awaiting_review` is the canonical pending state while review is unresolved
- returned findings do not self-apply as planning changes — review and replanning
  must occur first
- a rejected or expired review does not authorize planning mutation
- replanning scope must be bounded to what the trigger requires
- each downstream outcome (scope update, clarification, new handoff, no-change)
  has a specific governed path and specific conditions
- a scope update is not a substitute for a new handoff when the scope change is
  fundamental
- activity trail records are required for every named workflow event
- VEDA signal and V Forge active evidence queries are adjacent paths, not part
  of this workflow

If the workflow is implemented as "V Forge returned something, so Project V can
now update whatever it wants," the doctrine is wrong.

---

## Usage

This document should be used:

- when implementing the return-to-planning and replanning workflow states and transitions
- when deciding whether a situation warrants replanning or only maintenance
- when reviewing whether receipt, review, and planning mutation are being treated
  as distinct
- when evaluating which downstream outcome path is correct for a given replanning result
- when auditing whether the activity trail covers all required workflow events
- when routing between scope update, new handoff, clarification, or no-change outcomes

---

## Related Docs

- `handoff-workflow.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/project-v-to-v-forge-scope-update-interface.md`
- `../interfaces/project-v-to-v-forge-execution-clarification-interface.md`
- `../interfaces/project-v-handoff-recall-interface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-evidence-access-contract.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/invalidation-and-supersedence-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/activity-trail-integration-map.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
- `launch-readiness-workflow.md`
