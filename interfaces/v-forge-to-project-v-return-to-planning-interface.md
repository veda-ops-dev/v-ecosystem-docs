# V Forge to Project V Return-to-Planning Interface

## Purpose

This document defines the interface by which V Forge returns bounded execution
findings to Project V when execution requires planning reconsideration.

It exists to answer:

```text
What constitutes a valid return-to-planning package, what must the package carry,
how is delivery confirmed, what does receipt mean for planning, how is human review
triggered, and what happens when delivery fails or findings are stale?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the access model for V Forge → Project V return-to-planning delivery
- the minimum semantic contents of a valid return-to-planning package
- what must be true for a return package to be valid
- receipt confirmation requirements
- the finding-report boundary: what this interface transfers and what it does not
- return-to-planning receipt/review as an approval-sensitive event
- degraded-mode and recovery behavior
- how this interface is distinct from adjacent governed paths
- activity trail requirements for return-to-planning events
- cost and accounting posture

---

## Out of Scope

This document does not define:

- V Forge internal execution workflow
- Project V internal replanning workflow
- full approval policy — that belongs in `../governance/approval-and-escalation-model.md`
  and `../governance/approval-mechanics-seam-model.md`
- the forward handoff transfer — that is `project-v-to-v-forge-handoff-interface.md`
- handoff recall before V Forge has materially acted —
  that is `project-v-handoff-recall-interface.md`
- mid-execution scope clarification —
  that is `project-v-to-v-forge-execution-clarification-interface.md`
- post-replanning scope updates —
  that is `project-v-to-v-forge-scope-update-interface.md`
- detailed report structure — that belongs in
  `../governance/report-structure-and-required-fields.md`
- transport-layer implementation details or API schemas

---

## System

- interfaces

---

## Core Rule

The return-to-planning interface transfers bounded execution findings from V Forge
back to Project V when execution requires planning reconsideration.

Returned findings do not transfer execution truth ownership to Project V.
Returned findings do not self-apply as planning changes.
Receipt of returned findings is not authorization for planning mutation.
Project V reviews and interprets; V Forge continues to own execution truth.

---

## Access Model

**This interface uses V Forge-initiated push delivery with Project V receipt confirmation.**

V Forge initiates every return-to-planning delivery on this interface. Project V
does not poll for findings. Return transfer is not complete until Project V confirms
receipt.

Delivery, receipt, and planning review are distinct phases:

- **Delivery** — V Forge pushes the bounded findings package to Project V
- **Receipt confirmation** — Project V acknowledges that the package has arrived
  and is available for planning review
- **Planning review** — Project V evaluates the findings and determines whether
  and how planning should respond

All three phases are required before the return event is complete. Receipt
confirmation does not mean planning has acted. Planning review does not begin
until receipt is confirmed. Planning mutation does not follow automatically from
review — a governed planning decision is still required.

---

## Return-to-Planning Package Semantics

A valid return-to-planning package must be interpretable as carrying at minimum
the following semantic fields.

### Required semantic fields

**Return package / delivery identity**
A stable identifier for this return event and delivery. Required for activity trail
records, receipt confirmation, de-duplication, and re-delivery handling. Must remain
stable across re-delivery attempts unless the finding basis materially changes.

**Originating handoff identity or execution context reference**
A reference to the handoff or bounded execution context that generated these
findings. This ties the return to its originating governed transfer and prevents
orphaned or contextless findings from entering planning.

**Bounded finding or result summary**
A bounded description of what happened in execution — what was completed, what
was not, what was blocked, or what changed condition was encountered. This is
execution-side reporting, not a planning instruction.

**Why return-to-planning is being triggered**
An explicit statement of the reason execution cannot proceed, has been halted,
or requires planning reconsideration. The trigger reason must be one of the
categories defined in the Validity Conditions section.

**Scope of what execution could and could not complete**
What portion of the approved scope was completed before the triggering condition,
what remains incomplete, and what the current execution state is. This preserves
the boundary between what V Forge owns and what requires planning review.

**Execution constraints or blockers encountered**
The specific constraint, failure, missing condition, or changed circumstance that
led to this return. Must be execution-side in nature — not a planning re-scoping
attempt disguised as a finding.

**Evidence basis or execution-side provenance**
The execution-side basis for the finding — what V Forge observed, attempted, or
encountered. Where the finding references external conditions, the provenance must
be traceable. Findings without an execution-side basis must not be presented as
V Forge-originated.

**Freshness and timing of the returned condition**
When the triggering condition was observed or arose. This allows Project V to
assess how current the finding is and whether urgency applies.

**What planning concern is implicated**
A bounded statement of what aspect of the prior plan or planning assumption the
finding speaks to. This is V Forge's curation rationale — it is not a planning
instruction. V Forge states what the finding is relevant to; Project V determines
what to do with it.

**Current execution posture**
Whether execution has halted, is paused, has completed within bounded limits, or
is continuing under degraded conditions while this return is in transit. This
prevents ambiguity about whether V Forge is still active on the scope.

**Finding boundary marker**
An explicit statement that these findings are bounded execution outputs for planning
reconsideration — not VEDA signal, not planning decisions, not automatic planning
mutations. This marker makes the finding-report boundary contract-explicit.

### What the package must not contain

A return package must not contain:

- unrestricted execution-state dumps that reconstruct V Forge's full internal state
- planning instructions or recommendations that bypass Project V's planning authority
- direct assertions that specific planning decisions must change
- signal or evidence presented as though V Forge originated it (evidence attribution
  must trace to VEDA where VEDA is the source)
- findings disconnected from the originating handoff scope

---

## Validity Conditions

A return-to-planning package is valid only when all of the following are true:

- the package is tied to a real handoff or bounded execution context, identified
  by the originating handoff / execution context reference
- the findings are bounded and planning-relevant — they cannot be resolved within
  the approved execution scope without changing what planning should do next
- the package is not an unrestricted execution-state dump
- the package contains all required semantic fields
- the trigger reason is explicit and falls into one of these valid trigger categories:
  - execution is blocked and cannot proceed within approved scope
  - execution has failed and the failure affects the planning basis
  - execution is incomplete in a way that requires planning choice
  - changed conditions have invalidated assumptions the original handoff depended on
  - findings have emerged that require Project V to reconsider planning direction
- the execution-side basis and provenance for the finding are present
- the package is not fabricated, contextless, or orphaned from the originating scope

A package that fails any of these conditions must not be treated as a valid
return-to-planning event. Project V must not act on a package that fails validity
conditions. If Project V identifies a validity failure on receipt, the correct path
is governed interruption — surfacing the invalidity — not silent ingestion of an
incomplete return package.

---

## Finding-Report Boundary Rule

This is the most critical boundary this interface must enforce.

**V Forge returns bounded execution findings. It does not dump execution truth into
Project V. Project V reviews findings and makes planning decisions. Findings do not
make planning decisions for Project V.**

Specifically:

- returned findings are bounded execution outputs for planning reconsideration
- they are not VEDA signal
- they are not governing Project V planning decisions
- they do not automatically mutate planning state
- they do not automatically supersede prior governing decisions
- Project V must interpret the planning consequence through its own governed
  planning and decision process

The finding boundary marker in the package makes this explicit at the package level.
The governance rules in `../governance/report-structure-and-required-fields.md`
govern what a finding report must and must not assert.

---

## Boundary and Authority Rule

After a valid return-to-planning delivery and receipt confirmation:

- V Forge remains the owner of execution truth for the handed-off scope
- Project V remains the owner of planning and orchestration truth
- Project V may reconsider planning based on the bounded returned findings
- VEDA remains the owner of signal, evidence, and observability truth

**The return-to-planning interface delivers findings for reconsideration. It does not
transfer execution truth ownership back to Project V. It does not transfer planning
decision authority to V Forge.**

A return-to-planning transition does not automatically cancel or supersede the
existing handoff. The status of the original handoff and any ongoing execution is
governed by the outcome of Project V's planning reconsideration.

---

## Receipt Confirmation

Return-to-planning delivery is not complete until Project V confirms receipt.

**What receipt confirmation means:**
Project V acknowledges that the return package has arrived and is available for
planning review. Receipt confirmation does not mean planning has reviewed the
findings. Receipt does not mean planning will act on the findings.

**What V Forge must do if receipt confirmation is not returned:**
V Forge must not treat the delivery as complete. V Forge must retain the package
for re-delivery. V Forge may attempt re-delivery after an appropriate wait interval.
V Forge must not generate a new package to replace an unconfirmed delivery as if
the prior delivery never happened — the package identity must remain stable across
re-delivery attempts, provided the finding basis has not changed.

**What Project V must not assume:**
Project V must not assume that a return delivery it has not confirmed has not
occurred. If Project V receives a delivery it has already confirmed (e.g., due to
a retry), it must handle the duplicate gracefully using the package identity.

---

## Approval-Sensitive Event

Return-to-planning receipt and review is an approval-sensitive seam event where
the returned findings affect planning direction.

**Governing system for the review:** Project V governs the review of returned
findings. Project V generates the human review request where required.

V Forge does not initiate the review approval — V Forge initiates the delivery.
Project V governs what review is needed before planning responds.

**Pending state:** While planning review is pending, the workflow must be in
`awaiting_review`. The return package has been received. Planning reconsideration
has been proposed. No planning mutation has occurred.

**Receipt does not equal approval to change planning.** Reviewing the findings does
not equal approval to change planning. A governing planning decision following
governed review is still required before any planning state changes.

For full approval mechanics — what the review request must contain, what the
decision outcomes are, and how re-entry works — see:

- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`

This interface does not redefine approval mechanics.

---

## Distinction from Adjacent Interfaces

This return-to-planning interface is distinct from:

**`project-v-to-v-forge-handoff-interface.md`**
The forward transfer of execution responsibility from Project V to V Forge. The
return-to-planning interface is the complementary reverse path. These are not
interchangeable.

**`project-v-handoff-recall-interface.md`**
Used for operator-directed recall of a handoff that has been transferred but not
yet materially acted on. Recall reverses a transfer before meaningful execution
begins. Return-to-planning is used when execution is already underway and findings
require planning reconsideration.

**`project-v-to-v-forge-execution-clarification-interface.md`**
Used to deliver bounded clarification or guidance from Project V to V Forge during
active execution. Clarification resolves a specific ambiguity without triggering
planning reconsideration. Return-to-planning is used when execution cannot resolve
a concern within approved scope.

**`project-v-to-v-forge-scope-update-interface.md`**
Used after governed replanning to notify V Forge of updated scope or constraints.
A scope update delivers the output of replanning back into an active execution
context. Return-to-planning is what causes replanning to be needed in the first place.

None of these adjacent interfaces are substitutes for or extensions of the
return-to-planning transfer.

---

## Degraded-Mode Behavior

### Project V unavailable at delivery time

If Project V cannot receive the delivery, V Forge must:

- not treat the delivery as confirmed
- retain the package for re-delivery using the same package identity
- record the delivery attempt and failure in the activity trail
- not discard the finding

V Forge must remain in the current execution posture as stated in the package
(halted, paused, or continuing under bounded conditions) until receipt is confirmed.

### Receipt confirmation not returned within expected window

If V Forge has initiated delivery but receipt confirmation has not been returned
within a reasonable window, V Forge must treat delivery as incomplete. Same behavior
as "Project V unavailable" applies.

### Package invalid or incomplete

If Project V receives a return package that is missing required semantic fields or
fails validity conditions, Project V must not treat it as a valid return-to-planning
event. Project V must surface the invalidity. The correct path is governed
interruption, not silent ingestion of a deficient package.

### Findings become stale or superseded before review

If the return package has been received but not yet reviewed, and the execution
basis has materially changed — the condition resolved on its own, a different
blocking condition emerged, or the scope of the finding changed — V Forge must
assess whether the original package still honestly represents the finding.

If the basis change is material:
- V Forge should deliver an updated package rather than allowing review to proceed
  on a package that no longer accurately represents the current execution state
- The updated package carries a new delivery identity but must reference the prior
  package identity as superseded
- The original pending review must be closed and re-initiated against the updated package

### Duplicate delivery / retry case

If Project V receives a return package it has already confirmed — due to a retry
after a temporary failure — Project V must handle the duplicate gracefully using
the package identity. It must not initiate a second planning review for the same
finding set.

---

## Recovery Behavior

After degraded mode clears or a delivery failure is resolved:

- V Forge may re-deliver the same package using the same package identity, provided
  the finding basis has not materially changed
- If the finding basis has materially changed during the delay, a new package must
  be generated and the old package identity referenced as the prior version
- Receipt confirmation of the re-delivered package completes the delivery phase
- V Forge must not assume that a prior delivery attempt subsequently succeeded
  without confirmed receipt

---

## Allowed Use of Return Inputs by Project V

Project V may use return-to-planning inputs to:

- reconsider planning assumptions
- reconsider readiness
- reconsider handoff scope
- create revised planning or orchestration decisions through governed planning paths
- determine whether further bounded evidence is needed through the governed evidence
  request path
- determine whether new handoff, deferral, cancellation, or restructuring is required

---

## Activity Trail

Every return-to-planning event on this interface must produce activity trail records.

**Producing system:** V Forge (for delivery-side events); Project V (for receipt
confirmation and review events)
**Target system:** Project V (for delivery-side events)

The following events must each produce a record:

| Event | When it occurs |
|---|---|
| Delivery initiated | V Forge initiates the push delivery |
| Receipt confirmed | Project V confirms receipt |
| Delivery failed / unconfirmed | Delivery attempt produced no confirmation |
| Re-delivery initiated | V Forge re-delivers a previously unconfirmed package |
| Package superseded / voided | Finding basis changed before review; package invalidated |
| Review initiated | Project V begins planning review of the findings |
| Review outcome reached | Planning review produces a governed outcome |

Each event record must carry, at minimum:

- the return package / delivery identity
- the originating handoff / execution context reference
- the trigger reason for the return
- the current execution posture at time of delivery
- receipt confirmation status
- whether delivery is original or a retry
- for review events: the review outcome and which system generated the review

The exact canonical action type names must align with the activity trail model
(`../ecosystem/activity-trail-model.md`) and the activity trail integration map
(`../ecosystem/activity-trail-integration-map.md`). The mapping for this interface
is defined in integration map Section 3 (delivery events) and Section 5b (review
approval events).

Return-to-planning events that produce no activity trail records are not governed
events.

---

## Cost and Accounting Posture

Return-to-planning packaging and delivery are governed system activity. The costs
associated with producing a return package and delivering it are attributable to
V Forge as the producing and initiating system.

Cost attribution must be:

- reviewable after the fact
- associated with the package identity and the originating handoff scope
- captured in the activity trail where applicable

Re-delivery costs are attributed to the same return event chain, traceable through
the package identity.

---

## Human-In-The-Loop Principle

All return-to-planning transitions that affect planning direction should be reviewed
by a human before planning reconsideration results in new ecosystem actions.

Human review may be required depending on project sensitivity, execution risk or
failure severity, strategic impact, mutation scope, and launch or maintenance
sensitivity.

See the Approval-Sensitive Event section above and the seam-level mechanics in
`../governance/approval-mechanics-seam-model.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- V Forge initiates return-to-planning delivery; Project V does not poll for findings
- delivery, receipt confirmation, and planning review are three distinct required phases
- returned findings do not self-apply as planning changes — they require governed
  review and a planning decision
- the finding-report boundary is explicit: findings are bounded execution outputs
  for reconsideration, not planning instructions
- V Forge continues to own execution truth after a return-to-planning delivery
- activity trail records are required for every return-to-planning event
- this interface is distinct from handoff, recall, clarification, and scope update paths

If the interface is implemented as an unrestricted execution-state dump, as automatic
planning mutation, or as a delivery that requires no confirmation, the doctrine is wrong.

---

## Usage

This document should be used:

- when implementing V Forge's return-to-planning delivery
- when implementing Project V's receipt confirmation and review initiation
- when defining what a valid return-to-planning package must carry
- when reviewing whether a proposed return is too broad, too weak, or missing
  required fields
- when evaluating whether the finding-report boundary is being respected
- when writing V Forge and Project V workflow docs involving execution-to-planning flow

---

## Related Docs

- `project-v-to-v-forge-handoff-interface.md`
- `project-v-handoff-recall-interface.md`
- `project-v-to-v-forge-execution-clarification-interface.md`
- `project-v-to-v-forge-scope-update-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/report-structure-and-required-fields.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/cross-system-access-governance.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/vocabulary.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
- `../workflows/maintenance-and-replanning-workflow.md`
