# Project V to V Forge Handoff Interface

## Purpose

This document defines the interface by which Project V activates and delivers a
governed handoff to V Forge, transferring execution responsibility for an approved
bounded scope.

It exists to answer:

```text
What constitutes a valid governed handoff, what must the handoff package carry,
how is the transfer activated and confirmed, what happens when delivery fails or
the package is stale, and how does this interface relate to adjacent governed paths?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the access model for Project V → V Forge handoff delivery
- what must be true for a handoff to be valid
- the minimum semantic contents of a valid handoff package
- handoff activation as an approval-sensitive event
- receipt confirmation requirements
- degraded-mode and recovery behavior
- how this interface is distinct from return-to-planning, recall, clarification,
  and scope update interfaces
- activity trail requirements for handoff events
- cost and accounting posture

---

## Out of Scope

This document does not define:

- Project V internal planning or readiness workflow
- V Forge internal execution workflow
- full approval policy — that belongs in `../governance/approval-and-escalation-model.md`
  and `../governance/approval-mechanics-seam-model.md`
- return-to-planning when execution findings require planning reconsideration —
  that is `v-forge-to-project-v-return-to-planning-interface.md`
- handoff recall before V Forge has materially acted —
  that is `project-v-handoff-recall-interface.md`
- mid-execution scope clarification —
  that is `project-v-to-v-forge-execution-clarification-interface.md`
- post-replanning scope updates —
  that is `project-v-to-v-forge-scope-update-interface.md`
- transport-layer implementation details or API schemas

---

## System

- interfaces

---

## Core Rule

A handoff transfers execution responsibility from Project V to V Forge for an
approved bounded scope.

A handoff does not transfer planning ownership.
A handoff does not transfer signal-system ownership.
A handoff does not authorize open-ended scope expansion by V Forge.
Handoff transfer is not complete until V Forge confirms receipt.

---

## Access Model

**This interface uses Project V-initiated push delivery with V Forge receipt confirmation.**

Project V initiates every handoff delivery on this interface. V Forge does not
poll or query for handoffs. Handoff transfer is not complete until V Forge confirms
receipt.

Activation and delivery are distinct events:

- **Activation approval** — governed approval that authorizes the handoff to proceed.
  This is the approval-sensitive event. Approval is required before delivery begins.
- **Delivery** — Project V pushes the handoff package to V Forge after activation
  approval is in place.
- **Receipt confirmation** — V Forge acknowledges that the package has arrived and
  is available for execution. This completes the transfer event.

All three phases are required. A handoff is not active until all three are complete.

Project V must not treat a prepared handoff as active. Project V must not treat
an approved handoff as delivered. Project V must not treat a delivered handoff as
confirmed until V Forge confirmation is received.

---

## Handoff Validity Conditions

A handoff is valid only when all of the following are true:

- Project V has determined that the work is ready for handoff at the planning level
- the required activation approval posture has been satisfied (see Approval-Sensitive
  Event section)
- the handoff package contains the minimum semantic fields defined below
- the execution scope is bounded — it is specific enough for V Forge to act within
  without requiring unilateral scope interpretation
- the target system is V Forge
- the evidence or planning basis referenced in the package is not materially stale
  or superseded at the time of activation
- the package has not been superseded by a later planning decision that invalidates
  the basis for this handoff

A handoff that fails any of these conditions must not be treated as valid. V Forge
must not begin execution on a package that fails validity conditions. If V Forge
identifies a validity failure on receipt, the correct path is governed interruption,
not improvised scope interpretation.

---

## Handoff Package Semantics

A valid handoff package must be interpretable as carrying at minimum the following
semantic fields.

### Required semantic fields

**Handoff / delivery identity**
A stable identifier for this handoff and delivery event. Required for activity trail
records, receipt confirmation, re-delivery, and recall or supersedence events. Must
remain stable across re-delivery attempts unless the package itself is regenerated
due to a materially changed basis.

**Originating planning context or source entity**
A reference to the Project V planning entity that generated this handoff — the
objective, initiative, or work item whose readiness determination justified the
handoff. This allows the handoff to be traced back to planning context.

**Approved execution scope**
A bounded description of what work is being handed off. Must be specific enough
that V Forge can determine what is in scope and what is not. Open-ended scope
descriptions that require unilateral interpretation are not valid.

**Target system**
V Forge. Must be stated explicitly.

**Execution constraints and boundaries**
Any conditions, limits, or constraints that execution must respect — cost bounds,
external action limits, launch conditions, dependency conditions, or other
governing constraints from the planning side.

**Readiness basis**
Why this handoff is valid now — the readiness determination that justified it.
This preserves the planning rationale and supports continuity across sessions.

**Evidence references or supporting planning basis**
Bounded references to the evidence, signal, or planning rationale that supports
this handoff. These are references, not copies of VEDA-owned evidence. The
evidence referenced here must be traceable through the system that owns it.

**Expected outcomes or intended execution objective**
What execution is intended to produce — the high-level objective that V Forge
should work toward within the approved scope. This is not a detailed execution
specification; it is the planning-side expectation.

**Conditions that should trigger return-to-planning**
What kinds of execution findings, failures, or changed conditions should cause
V Forge to return findings to planning rather than proceeding autonomously.
This makes the return-to-planning trigger explicit at handoff time.

**Activation timestamp**
When Project V activated this handoff for delivery.

**Package revision posture**
Whether this package is the original or a revision of a prior package for the
same scope. If a revision, the prior handoff identity must be referenced so the
activity trail can link the revision to its predecessor.

### What the package must not contain

A handoff package must not contain:

- open-ended research authority or observatory gathering instructions
- permission for V Forge to redefine project structure
- planning state beyond what execution requires to operate within approved scope
- VEDA's full observatory records or signal archives
- fabricated readiness claims — the readiness basis must be traceable to actual
  Project V readiness evaluation

---

## Approval-Sensitive Event

Handoff activation is an approval-sensitive event governed under Class B of the
approval model, with potential escalation to Class C depending on scope, risk,
and launch sensitivity.

**Initiating system:** Project V generates the activation approval request.

**Pending state:** While activation approval is pending, the handoff workflow must
be in `awaiting_approval`. The handoff package is prepared. Execution responsibility
has not transferred. V Forge must not begin execution.

**Approval does not equal delivery.** Approval authorizes Project V to initiate the
push delivery. Delivery and receipt confirmation are the subsequent steps.

If conditions change materially while in `awaiting_approval` — scope, evidence,
approval authority, or readiness basis — the pending approval must be evaluated for
staleness before activation proceeds. A stale pending approval cannot be silently
carried forward.

For full approval mechanics — what the approval request must contain, what the
decision outcomes are, and how re-entry works — see:

- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`

This interface does not redefine approval mechanics.

---

## Boundary and Authority Rule

After a valid handoff transfer with confirmed receipt:

- V Forge owns execution truth for the handed-off scope
- Project V retains planning truth and planning-side continuity for the handed-off work
- Project V retains orchestration truth
- VEDA retains signal and observability truth

**The handoff transfers execution responsibility. It does not transfer planning ownership.**

V Forge must execute within the approved scope and constraints defined in the
handoff package. V Forge must not redefine the project structure, expand scope
unilaterally, or treat the handoff as authorization for open-ended work.

If execution discovers a planning problem — a blocking finding, a changed condition,
or an assumption that cannot be validated — the governed path is return-to-planning
through `v-forge-to-project-v-return-to-planning-interface.md`, not unilateral
reinterpretation. A missing handoff semantic is a governed interruption event, not
a license for improvised scope definition.

---

## Distinction from Adjacent Interfaces

This handoff interface is the primary governed transfer of execution responsibility.
It is distinct from:

**`v-forge-to-project-v-return-to-planning-interface.md`**
Used when V Forge returns bounded execution findings that require planning
reconsideration. The return path is V Forge → Project V; the handoff path is
Project V → V Forge. These are complementary, not interchangeable.

**`project-v-handoff-recall-interface.md`**
Used for operator-directed recall of a handoff that has been transferred but not
yet materially acted on by V Forge. Recall reverses a transfer; this interface
initiates one.

**`project-v-to-v-forge-execution-clarification-interface.md`**
Used to deliver bounded clarification or guidance to V Forge during active
execution — resolving a specific ambiguity without a new handoff and without
triggering return-to-planning. Clarification is scoped to an existing execution
relationship; this interface establishes one.

**`project-v-to-v-forge-scope-update-interface.md`**
Used after governed replanning to notify V Forge of updated scope or constraints
within an active execution relationship. Scope updates carry the output of replanning
into an existing execution context; this interface initiates the execution context.

None of these adjacent interfaces are substitutes for or extensions of the handoff
transfer itself.

---

## Degraded-Mode Behavior

### V Forge unavailable at delivery time

If V Forge cannot receive the delivery — because it is unavailable or the delivery
cannot be completed — Project V must:

- not treat the handoff as confirmed or active
- retain the package for re-delivery using the same handoff identity
- record the delivery attempt and failure in the activity trail
- not allow execution to begin

V Forge must not assume a handoff has been received if it has not confirmed receipt.

### Receipt confirmation not returned within expected window

If Project V has initiated delivery but receipt confirmation has not been returned
within a reasonable window, Project V must treat delivery as incomplete. Same
behavior as "V Forge unavailable" applies.

### Package invalid or incomplete at activation time

If V Forge receives a handoff package that is missing required semantic fields or
fails validity conditions, V Forge must not begin execution. V Forge must surface
the insufficiency through the governed interruption path rather than proceeding on
an incomplete package.

### Package becomes stale or superseded before confirmation

If the handoff package has been delivered but not yet confirmed by V Forge, and
the planning basis has materially changed — scope revised, evidence invalidated,
approval withdrawn — Project V must assess whether the package can still support
honest execution within approved bounds.

If the basis change is material:
- Project V should not allow V Forge to confirm and begin execution on the basis
  of a superseded package
- The pending delivery must be voided and a new package issued if the change
  warrants it
- The original handoff identity should be referenced as superseded in the new package

### Duplicate delivery / retry case

If V Forge receives a delivery it has already confirmed — due to a retry after a
temporary failure — V Forge must handle the duplicate gracefully using the handoff
identity. It must not begin a second parallel execution for the same scope.

---

## Recovery Behavior

After degraded mode clears or a delivery failure is resolved:

- Project V may re-deliver the same package using the same handoff identity, provided
  the basis has not materially changed
- If the basis has materially changed during the delay, a new package must be generated
  and the old handoff identity should be referenced as the prior version
- Receipt confirmation of the re-delivered package completes the transfer event
- Project V must not assume that a prior delivery attempt subsequently succeeded
  without confirmed receipt

---

## Allowed Use of Handoff Inputs by V Forge

V Forge may use the handoff package to:

- execute the approved work within the stated scope and constraints
- validate that execution requirements are satisfied within the approved scope,
  without expanding or reinterpreting that scope
- perform bounded execution-side research needed to complete or validate the
  approved scope
- produce execution outputs and bounded execution findings
- return blocked, failed, incomplete, or changed execution conditions through the
  governed return-to-planning path

---

## Forbidden Interpretations of Handoff

A handoff must not be interpreted as:

- permission for V Forge to become the planner or redefine project structure
- permission for V Forge to perform open-ended ecosystem research
- permission for V Forge to absorb VEDA's signal-system role
- permission for Project V to continue acting as the canonical execution ledger
  after confirmed transfer
- authorization for scope beyond what the package explicitly defines

---

## Activity Trail

Every handoff event on this interface must produce activity trail records.

**Producing system:** Project V (for delivery-side events); V Forge (for receipt confirmation)
**Target system:** V Forge (for delivery-side events); Project V (for confirmation events)

The following events must each produce a record:

| Event | When it occurs |
|---|---|
| Activation approval requested | Project V generates the approval request |
| Activation approved / rejected | Decision outcome is reached |
| Handoff delivery initiated | Project V initiates the push delivery |
| Receipt confirmed | V Forge confirms receipt |
| Delivery failed / unconfirmed | Delivery attempt produced no confirmation |
| Re-delivery initiated | Project V re-delivers a previously unconfirmed package |
| Package superseded / voided | Package invalidated before confirmation |

Each event record must carry, at minimum:

- the handoff / delivery identity
- the source planning entity reference
- the approved execution scope identifier
- the approval-sensitive status (whether activation approval applies and its outcome)
- the receipt confirmation status
- whether delivery is original or a retry
- whether the package has been superseded or voided, and by what

The exact canonical action type names must align with the activity trail model
(`../ecosystem/activity-trail-model.md`) and the activity trail integration map
(`../ecosystem/activity-trail-integration-map.md`). The mapping for this interface
is defined in integration map Section 2 (delivery events) and Section 5a (activation
approval events).

Handoff events that produce no activity trail records are not governed events.

---

## Cost and Accounting Posture

Handoff preparation and delivery are governed system activity. The costs associated
with preparing a handoff package and delivering it are attributable to Project V as
the producing and initiating system.

Cost attribution must be:

- reviewable after the fact
- associated with the handoff identity and project scope
- captured in the activity trail where applicable

Re-delivery costs are attributed to the same handoff event chain, traceable through
the handoff identity.

---

## Human-In-The-Loop Principle

Handoff activation is a governance-sensitive transition. Human review or approval
may be required depending on project sensitivity, execution risk, external action
implications, mutation scope, and launch sensitivity.

See the Approval-Sensitive Event section above and the seam-level mechanics in
`../governance/approval-mechanics-seam-model.md`.

A handoff must never be treated as a casual internal state flip if it changes who
is responsible for execution. The approval, delivery, and confirmation sequence
ensures the transfer is governed, traceable, and reversible through the proper paths.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- Project V initiates handoff delivery; V Forge does not poll for it
- activation approval, push delivery, and receipt confirmation are three distinct
  required phases — completing one does not mean the others have occurred
- the handoff package must carry the semantic fields defined here; an incomplete
  package is not a valid handoff
- the handoff transfers execution responsibility for a bounded scope, not planning
  ownership
- V Forge discovering a planning problem during execution must use return-to-planning,
  not unilateral scope redefinition
- activity trail records are required for every handoff event
- this handoff interface is distinct from return-to-planning, recall, clarification,
  and scope update paths

If the interface is implemented as a state flag that V Forge polls, as an unbounded
execution authorization, or as a transfer that requires no confirmation, the doctrine
is wrong.

---

## Usage

This document should be used:

- when implementing Project V's handoff activation and delivery
- when implementing V Forge's handoff receipt and confirmation
- when defining what a valid handoff package must carry
- when reviewing whether a proposed handoff is too broad, too weak, or missing
  required fields
- when writing Project V and V Forge workflow docs that involve the planning-to-execution
  transition
- when evaluating whether a handoff event should produce an activity trail record

---

## Related Docs

- `v-forge-to-project-v-return-to-planning-interface.md`
- `project-v-handoff-recall-interface.md`
- `project-v-to-v-forge-execution-clarification-interface.md`
- `project-v-to-v-forge-scope-update-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/cross-system-access-governance.md`
- `../ecosystem/activity-trail-model.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
- `../workflows/handoff-workflow.md`
- `../governance/recommendation-packaging-doctrine.md`
