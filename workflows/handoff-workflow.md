# Handoff Workflow

## Purpose

This document defines the governed workflow by which approved Project V work becomes active execution responsibility in V Forge.

It exists to answer:

```text
What stages does the handoff workflow move through, what event causes each transition,
what pending state applies at each stage, when may Project V proceed and when may it
not, and what happens when delivery fails, approval is rejected, or basis changes?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the concrete stage sequence from planning readiness through V Forge receipt confirmation
- entry conditions and handoff validity posture
- approval gate behavior and canonical pending state
- push delivery and receipt confirmation as distinct phases
- degraded-mode and interruption handling
- re-entry and recovery rules
- adjacent interface routing (recall, clarification, scope update, return-to-planning)
- activity-trail obligations for handoff events

---

## Out of Scope

This document does not define:

- the handoff interface data contract — that belongs in
  `interfaces/project-v-to-v-forge-handoff-interface.md`
- full approval class definitions and escalation principles — those belong in
  `governance/approval-and-escalation-model.md` and
  `governance/approval-mechanics-seam-model.md`
- Project V internal planning or readiness workflow
- V Forge internal execution workflow
- return-to-planning workflow after execution has begun — that belongs in
  `workflows/maintenance-and-replanning-workflow.md`
- transport or storage implementation details

---

## System

- workflows

---

## Relationship to Governing Interface Docs

This workflow governs sequencing and transition rules. The interface contract governs
what the handoff package must carry.

- `interfaces/project-v-to-v-forge-handoff-interface.md` — defines the handoff package
  semantics, validity conditions, delivery model, and boundary rules. This workflow must
  remain consistent with that contract.
- `governance/approval-mechanics-seam-model.md` — defines the shared seam-level
  approval mechanics pattern used at Stage 3. This workflow carries the seam-specific
  facts; the mechanics doc carries the shared pattern.
- `ecosystem/activity-trail-integration-map.md` — defines the canonical action type
  mapping for all activity-trail records produced by this workflow.

---

## Core Rule

Approval, delivery, and receipt confirmation are three distinct required phases.
None may substitute for or imply the others.

- **Approval** authorizes Project V to initiate the push delivery
- **Delivery** transfers the handoff package to V Forge
- **Receipt confirmation** completes the transfer and makes execution responsibility active

Execution must not begin until all three phases are complete.

---

## Entry Conditions

The handoff workflow may enter Stage 1 only when all of the following are true:

- Project V has determined that the work is planning-ready for handoff
- the execution target is V Forge
- the execution scope is bounded and specific enough for V Forge to act within
- the handoff package contains at minimum the semantic fields required by the interface
  contract: handoff identity, originating planning context, approved execution scope,
  constraints, readiness basis, evidence references, expected outcome, and
  return-to-planning trigger conditions
- the evidence and planning basis referenced in the package are not materially stale
  or superseded at entry time
- no active governance-sensitive change is in flight that would invalidate the
  readiness basis before approval can be obtained

If any of these conditions are not met, the workflow must not enter Stage 1. Work
remains in Project V planning state until conditions are satisfied.

---

## Workflow Stages

### Stage 1 — Handoff Package Prepared

**Entry event:** Project V readiness evaluation concludes that work is handoff-ready.

**What happens at this stage:**
Project V prepares the bounded handoff package. The package assembles the
execution-facing planning subset: approved scope, constraints, readiness basis,
evidence references, expected outcomes, and return-to-planning trigger conditions.
The handoff identity is assigned. Package revision posture is established.

**Pending state:** None — this stage is an active preparation stage, not a pending stage.

**Exit condition → Stage 2:** Package is complete and meets the validity conditions
in the interface contract.

**Fallback:** If the package cannot be completed to meet validity conditions, work
returns to Project V planning / readiness evaluation. The incomplete package must
not be activated.

**Boundary rule:** Handoff package preparation is planning truth. Execution responsibility
has not moved. V Forge is not yet involved.

---

### Stage 2 — Approval Request Generated

**Entry event:** Handoff package passes validity check and is ready for activation.

**What happens at this stage:**
Project V generates the activation approval request. The request must contain
the minimum semantic contents required by the approval mechanics model: the action
being requested (handoff activation), the execution scope, the readiness basis, the
approval class, the conditions, and what happens on each outcome. The request is
delivered to the human operator or governed approval surface.

**Pending state:** `awaiting_approval` — begins immediately on request generation.

**Approval class:** Class B or Class C depending on execution scope, risk, launch
sensitivity, and external action implications. Determined per the Tier 1 approval model.

**Activity trail:** `approval.request` record produced by Project V. Required fields
from `ecosystem/activity-trail-integration-map.md` Section 5a: `entity_type: handoff`,
`entity_id: <handoff identity>`, `approval_class`, `execution_scope_id`,
`readiness_basis_ref`.

**Exit condition → Stage 3:** A governed approval decision is received.
**Exit condition → Stage 5 (degraded):** Approval becomes expired or stale.
**Exit condition → Stage 7 (escalation):** Approval is escalated.

**Boundary rule:** While in `awaiting_approval`, the handoff is not active. V Forge
must not begin execution. Project V must not treat the handoff as delivered.

---

### Stage 3 — Approval Decision Received

**Entry event:** Human operator or governed approval surface reaches a decision.

**Decision outcomes and workflow consequences:**

| Outcome | Workflow action |
|---|---|
| `approved` | Proceed to Stage 4 (delivery) |
| `rejected` | Handoff does not proceed. Return handoff to Stage 1 or Project V planning. Rejection is a governed outcome — preserve reason and scope. |
| `escalated` | Enter Stage 7 (escalation handling). Handoff remains in `awaiting_approval`. |
| `expired` | Prior approval cannot be silently reused. Re-evaluate basis per Stage 8 (basis change handling). |

**Activity trail:** `approval.decide` record at decision time. Required fields from
integration map Section 5a: `entity_type: handoff`, `entity_id: <handoff identity>`,
`approval_class`, `decision` (`approved`, `rejected`, or `expired`), `decision_scope`.

**Boundary rule:** Approval authorizes delivery. It does not constitute delivery.
The handoff is not active after approval — delivery and receipt confirmation are still
required.

---

### Stage 4 — Delivery Initiated

**Entry event:** Activation approval received (`approved` outcome from Stage 3).

**What happens at this stage:**
Project V initiates the push delivery of the handoff package to V Forge through
`interfaces/project-v-to-v-forge-handoff-interface.md`. The handoff identity is
stable across all delivery attempts for this package. A delivery-initiated event
is produced.

**Activity trail:** `handoff.create` record produced by Project V. Required fields
from integration map Section 2: `entity_type: handoff`, `entity_id: <handoff identity>`,
`source_planning_entity_ref`, `execution_scope_id`, `package_version_posture`.

**Exit condition → Stage 5:** V Forge confirms receipt.
**Exit condition → Stage 6a (degraded):** V Forge unavailable or confirmation not returned.
**Exit condition → Stage 6b (invalid):** V Forge identifies a validity failure on receipt.

**Boundary rule:** Delivery is not confirmed until V Forge receipt is returned.
Project V must not treat delivery as complete until Stage 5 is reached.

---

### Stage 5 — Receipt Confirmed / Handoff Active

**Entry event:** V Forge confirms receipt of the handoff package.

**What happens at this stage:**
V Forge confirms receipt through the governed path. Execution responsibility transfers
to V Forge for the approved bounded scope. The handoff is now active. V Forge may begin
execution within the scope and constraints defined in the package.

**Activity trail:** `handoff.confirmed` record produced by V Forge. Required fields
from integration map Section 2: `entity_type: handoff`, `entity_id: <handoff identity>`,
`receipt_confirmed_at`.

**Exit condition:** The handoff workflow is complete. Post-handoff governance applies
(see Post-Handoff Boundary Stabilization below).

**Adjacent paths that may now apply:**
- VEDA startup signal delivery to V Forge is a related but distinct layer that
  may activate at this point — see Adjacent Interface Routing.
- Execution clarification, scope update, and return-to-planning become the
  governing paths for any subsequent changes or findings.

**Boundary rule:** Receipt confirmation transfers execution responsibility. It does
not transfer planning ownership. Project V remains the planning system of record.
V Forge owns execution truth for the handed-off scope.

---

### Stage 6a — Degraded / Delivery Failed

**Entry event:** Delivery attempted but V Forge is unavailable, or receipt confirmation
not returned within the expected window.

**What happens at this stage:**
Project V retains the package and records the delivery failure. The handoff identity
is preserved for re-delivery. V Forge must not assume the handoff has been received.

**Handling rules:**
- VEDA must not treat startup signal delivery as applicable until handoff receipt is confirmed
- Project V may attempt re-delivery using the same handoff identity
- If re-delivery is attempted, a re-delivery-initiated record is produced
- If delivery fails repeatedly or conditions change materially, proceed to Stage 8
  (basis change / voiding assessment)

**Activity trail:** `handoff.failed` record produced by Project V. On re-delivery:
`handoff.create` record with `is_retry: true` and `prior_delivery_id` in `details`.

**Exit condition → Stage 5:** V Forge confirms receipt on re-delivery.
**Exit condition → Stage 8:** Basis has materially changed during delivery failure window.

---

### Stage 6b — Package Invalid at Receipt

**Entry event:** V Forge receives the package but identifies a validity failure
(missing required fields, invalid scope, or basis contradiction).

**What happens at this stage:**
V Forge must not begin execution. V Forge surfaces the validity failure through
the governed interruption path. Project V receives the interruption.

**Handling rules:**
- Project V assesses whether the package can be corrected and re-delivered, or
  whether the readiness basis must be re-evaluated
- If the package is correctable: revise, regenerate (new handoff identity with
  reference to prior package as superseded), and return to Stage 2
- If the basis is invalid: return to Stage 1 or Project V planning

**Activity trail:** `handoff.failed` record. If package is voided/superseded:
`handoff.reject` record with `superseded_by_ref` and `void_reason`.

---

### Stage 7 — Escalation Handling

**Entry event:** Approval escalated at Stage 3.

**What happens at this stage:**
The handoff remains in `awaiting_approval`. No delivery may proceed. The escalation
is preserved. The governing escalation path defined in the approval mechanics model
applies.

**Activity trail:** `approval.escalate` record produced by Project V. Required fields
from integration map Section 5a: `entity_type: handoff`, `entity_id: <handoff identity>`,
`approval_class`, `escalation_reason`.

**Exit condition:** Escalation resolves. Outcome re-enters Stage 3 as a governed
decision outcome.

**Boundary rule:** Escalation is a named pending state, not a stall. Work must not
proceed while escalated.

---

### Stage 8 — Basis Change / Approval Expiry Assessment

**Entry event:** Conditions materially change while in `awaiting_approval` or during
a delivery failure window; or an approval expires.

**What happens at this stage:**
Project V assesses whether the original handoff basis remains valid given the
changed conditions. A stale `awaiting_approval` state is not authorization to proceed.

**Assessment outcomes:**

| Assessment | Workflow action |
|---|---|
| Basis still valid | Re-confirm basis and re-enter Stage 2 (new approval request if expired) |
| Basis requires revision | Return to Stage 1 (package re-preparation with updated basis) |
| Basis is no longer valid | Return to Project V planning / readiness evaluation |

**Activity trail:** If package is voided before confirmation: `handoff.reject` record
with `void_reason` referencing the change in basis.

**Boundary rule:** A changed basis does not automatically invalidate a handoff, but
it must be assessed explicitly. The ecosystem must not silently continue under a basis
that would not survive scrutiny.

---

## Post-Handoff Boundary Stabilization

After Stage 5 (receipt confirmed):

- Project V preserves planning continuity and does not act as the active execution ledger
- V Forge executes within the bounded approved scope and does not casually redefine
  planning — if scope is insufficient, the governed paths (clarification, scope update,
  return-to-planning) apply
- VEDA remains the signal and observability system of record
- Handoff is a transfer of responsibility, not a boundary collapse

If post-handoff behavior produces shared fuzzy ownership, the workflow has drifted.

---

## Transition Summary Table

| From stage | Event | To stage |
|---|---|---|
| Entry conditions met | — | Stage 1 |
| Stage 1 complete | Package passes validity | Stage 2 |
| Stage 1 blocked | Cannot complete package | Return to planning |
| Stage 2 | Approval request generated, decision pending | Stage 3 |
| Stage 3 | `approved` | Stage 4 |
| Stage 3 | `rejected` | Stage 1 or planning |
| Stage 3 | `escalated` | Stage 7 |
| Stage 3 | `expired` | Stage 8 |
| Stage 4 | Receipt confirmed | Stage 5 |
| Stage 4 | Delivery failed / no confirmation | Stage 6a |
| Stage 4 | Package invalid at receipt | Stage 6b |
| Stage 5 | — | Workflow complete |
| Stage 6a | Receipt confirmed on re-delivery | Stage 5 |
| Stage 6a | Basis materially changed | Stage 8 |
| Stage 6b | Package correctable | Stage 2 (revised package) |
| Stage 6b | Basis invalid | Stage 1 or planning |
| Stage 7 | Escalation resolves | Stage 3 |
| Stage 8 | Basis still valid | Stage 2 |
| Stage 8 | Basis requires revision | Stage 1 |
| Stage 8 | Basis no longer valid | Planning |

---

## Adjacent Interface Routing

When adjacent governed paths become relevant, route to them — do not fold their
semantics into this workflow.

### Handoff Recall (`interfaces/project-v-handoff-recall-interface.md`)

Applies: before Stage 5 (before V Forge has materially acted on the handoff).

Use when: an operator-directed recall is needed for a transferred but not-yet-acted
handoff.

Distinct from: return-to-planning (which applies when execution is already underway
and findings require planning reconsideration).

This workflow ends; the recall interface governs the recall event.

### VEDA Startup Signal Delivery (`interfaces/veda-to-v-forge-signal-interface.md`)

Applies: at or around Stage 5 receipt confirmation, as V Forge is initializing
execution intelligence context for the handed-off scope.

Distinct from: the handoff itself. Startup signal delivery is a related but separate
VEDA-initiated push layer. It does not replace or substitute for handoff receipt.
The handoff must be confirmed before VEDA startup signal delivery is applicable.

### Execution Clarification (`interfaces/project-v-to-v-forge-execution-clarification-interface.md`)

Applies: after Stage 5, during active execution.

Use when: V Forge has raised a bounded ambiguity that Project V can resolve without
triggering return-to-planning or issuing a new handoff.

Distinct from: a new handoff (which would require re-entering this workflow from Stage 1).

### Scope Update (`interfaces/project-v-to-v-forge-scope-update-interface.md`)

Applies: after Stage 5, following a governed replanning event.

Use when: governed replanning has produced revised scope or constraints that must
be communicated to V Forge for an active execution context.

Distinct from: a new handoff. If the replanning outcome requires fundamentally
different execution scope, re-enter this workflow from Stage 1.

### Return-to-Planning (`interfaces/v-forge-to-project-v-return-to-planning-interface.md`)

Applies: after Stage 5, when V Forge encounters blocked, failed, or changed execution
conditions that cannot be resolved within the approved scope.

Distinct from: all other adjacent paths. Return-to-planning is V Forge-initiated and
delivers bounded execution findings to Project V for planning reconsideration.

This workflow ends at Stage 5. Return-to-planning and its subsequent replanning cycle
is governed by `workflows/maintenance-and-replanning-workflow.md`.

---

## Activity Trail Requirements

All handoff workflow events must produce activity trail records using the canonical
action types from `ecosystem/activity-trail-integration-map.md` Section 2 and
Section 5a.

| Workflow event | Action type | Producing system |
|---|---|---|
| Approval request generated (Stage 2) | `approval.request` | Project V |
| Approval decision received (Stage 3) | `approval.decide` | Operator / approval surface |
| Approval escalated (Stage 7) | `approval.escalate` | Project V |
| Delivery initiated (Stage 4) | `handoff.create` | Project V |
| Receipt confirmed (Stage 5) | `handoff.confirmed` | V Forge |
| Delivery failed (Stage 6a) | `handoff.failed` | Project V |
| Re-delivery initiated (Stage 6a retry) | `handoff.create` with `is_retry: true` | Project V |
| Package voided / superseded (Stage 6b, 8) | `handoff.reject` | Project V |

Activity records that are not produced are not governed events. Implementations
must not skip activity-trail logging for any of the events above.

See `ecosystem/activity-trail-integration-map.md` for the minimum required fields
per event. See `ecosystem/activity-trail-model.md` for base required fields that
apply to every record.

---

## Approval Gate: Seam-Specific Facts

Handoff activation is an approval-sensitive event. This section carries the
seam-specific facts. The shared mechanics pattern is governed by
`governance/approval-mechanics-seam-model.md`.

| Fact | Value |
|---|---|
| Initiating system | Project V |
| Canonical pending state | `awaiting_approval` |
| Approval class | Class B or Class C (scope- and risk-dependent) |
| Approval does not equal delivery | True — approval authorizes delivery initiation only |
| Stale approval reuse | Not permitted — basis must be re-evaluated if conditions have materially changed |

For the full mechanics — request contents, decision re-entry rules, escalation path,
activity trail obligations — see `governance/approval-mechanics-seam-model.md`
Section A (Handoff Activation).

---

## Decision Continuity

The handoff workflow must preserve continuity across the planning-to-execution transition:

- readiness basis must remain traceable into the handoff package
- whether approval was pending or satisfied must be preserved
- active handoff must remain distinguishable from prepared or recommended handoff
- later return-to-planning events must be understandable in relation to the prior handoff

If the transition cannot be reconstructed from activity trail records later, the
workflow was not governed strongly enough.

---

## Human-In-The-Loop Principle

Handoff activation is governance-sensitive because it changes which system is
responsible for active work. Human review or approval may be required depending on:

- project sensitivity
- execution risk
- external action implications
- mutation scope
- launch sensitivity
- cost or paid-action implications

The approval class and mechanics are defined in `governance/approval-and-escalation-model.md`
and `governance/approval-mechanics-seam-model.md`.

Pre-activation verification obligations from `governance/testing-and-verification-doctrine.md`
apply — including precondition verification and approval verification.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the handoff workflow has eight distinct named stages with concrete transitions
- approval, delivery, and receipt confirmation are three separate required phases
- `awaiting_approval` is the canonical pending state while approval is unresolved
- execution must not begin until Stage 5 (receipt confirmed) is reached
- a rejected, expired, or escalated approval does not proceed to delivery
- a delivery failure does not mean the handoff is active
- basis changes while pending must be assessed explicitly, not silently ignored
- activity trail records are required for every named workflow event
- adjacent paths (recall, clarification, scope update, return-to-planning) each have
  specific entry conditions and must not be conflated with each other or with this workflow

If the workflow is implemented as "Project V finished preparing, so execution starts
when V Forge gets around to it," the doctrine is wrong.

---

## Usage

This document should be used:

- when implementing the Project V → V Forge handoff workflow states and transitions
- when deciding whether a handoff is in preparation, pending approval, delivered,
  or confirmed
- when reviewing whether approval, delivery, and receipt are being treated as distinct
- when evaluating whether degraded delivery or a changed basis requires re-entry
- when routing to adjacent interfaces (recall, clarification, scope update, return-to-planning)
- when auditing whether the activity trail covers all required workflow events

---

## Related Docs

- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/project-v-handoff-recall-interface.md`
- `../interfaces/project-v-to-v-forge-execution-clarification-interface.md`
- `../interfaces/project-v-to-v-forge-scope-update-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/testing-and-verification-doctrine.md`
- `../governance/decision-continuity-doctrine.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/activity-trail-integration-map.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
- `maintenance-and-replanning-workflow.md`
