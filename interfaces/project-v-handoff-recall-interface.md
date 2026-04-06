# Project V Handoff Recall Interface

## Purpose

This document defines the interface by which a transferred handoff is recalled
through an operator-directed governed path before V Forge has materially acted
on it.

It exists to answer:

```text
How is a handoff recalled after transfer when V Forge has not yet materially
acted on it, what makes this a governed event rather than a silent state
collapse, and how is handoff recall distinguished from return-to-planning?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the meaning of a governed handoff recall
- when handoff recall is applicable vs when return-to-planning is required instead
- what must cross through this interface to make the recall a governed event
- the boundary conditions that distinguish recall from return-to-planning and
  from informal cancellation

---

## Out of Scope

This document does not define:

- detailed transport or implementation format
- approval mechanics beyond the boundary note below
- field-level schemas
- Project V internal lifecycle handling after recall
- V Forge internal state handling during recall

Those belong in workflow, governance, and implementation-specific docs.

---

## System

- interfaces

---

## Interface Direction

**Operator-directed → Project V (governing) → V Forge (receiving)**

Recall is initiated by an operator decision, governed through Project V, and
delivered to V Forge. Project V owns the planning-side recall event. V Forge
receives notice that the handoff is recalled and must cease execution preparation.

---

## Governing Systems

- **Initiator:** Operator (via governed operator surface) and Project V
- **Receiver:** V Forge

---

## Core Rule

A handoff recall is the governed reversal of a transferred handoff in the period
after transfer but before V Forge has materially acted on it.

Recall is not:

- return-to-planning (which applies when V Forge has already begun execution
  and surfaces findings that require planning reconsideration)
- informal cancellation
- a silent state collapse in Project V
- permission to recall in-flight execution after execution responsibility is
  already materially active

The recall must produce an explicit governed event. The Handed-Off lifecycle
state in Project V must not be overwritten without a traceable governing reason
attached to the recall event.

If V Forge has already materially acted on the handoff, the correct path is
return-to-planning, not recall through this interface.

---

## Applicability Condition

This interface applies only when:

- the handoff has been transferred through the governed handoff interface
- V Forge has not yet materially acted on the handoff (no meaningful execution
  work has begun)

"Materially acted" means V Forge has taken execution steps based on the handoff
beyond merely receiving and acknowledging it. The exact threshold for material
action must be determinable from V Forge's execution state at recall time.

---

## Minimum Semantic Elements

A valid handoff recall must be interpretable as carrying at minimum:

- which handoff is being recalled (reference to the handoff identity)
- the governing reason for recall
- that this is a governed recall event, not a silent state change
- what state Project V returns to after recall (back to planning or readiness
  evaluation, with prior handoff history preserved)
- confirmation that V Forge must not proceed with the recalled handoff

---

## Boundary and Ownership Rule

After a valid handoff recall:

- Project V resumes planning-side ownership of the work
- V Forge must not continue execution on the recalled handoff
- the prior Handed-Off lifecycle state must remain part of history; it must not
  be silently overwritten
- the recall event must be preserved as a traceable governing event in Project V
- a changed planning preference alone is not sufficient justification for recall;
  the recall must reference a governing reason

---

## Activity Trail

Activity trail integration is required for this interface.

The exact canonical action type mapping and required fields will be defined in
the activity trail integration map (`../ecosystem/activity-trail-integration-map.md`)
once that document is completed.

This stub does not finalize the activity trail action vocabulary for this interface.
Implementations must not proceed without that mapping in place.

---

## Usage

This document should be used:

- when an operator needs to recall a transferred handoff before V Forge has
  materially acted
- when reviewing whether a proposed recall is within the applicability condition
  of this interface or should be a return-to-planning event instead
- when verifying that a recall produces a governed event rather than a silent
  state collapse

---

## Related Docs

- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `../project-v/v-forge-integration.md`
- `../project-v/lifecycle.md`
- `../ecosystem/cross-system-boundaries.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/decision-continuity-doctrine.md`
