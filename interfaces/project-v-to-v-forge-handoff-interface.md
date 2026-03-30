# Project V to V Forge Handoff Interface

## Purpose

This document defines the interface by which Project V hands off work to V Forge.

It exists to answer:

```text
What crosses from Project V into V Forge at handoff time, what does that transfer mean, and what does it not mean?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the meaning of a Project V to V Forge handoff
- what kinds of information may cross through the handoff interface
- what responsibility is transferred at handoff time
- what is explicitly not transferred at handoff time
- the boundary posture operators and LLMs should use when interpreting handoff behavior

---

## Out of Scope

This document does not define:

- Project V internal planning workflow
- V Forge internal execution workflow
- detailed approval policy
- detailed report structure
- detailed transport or implementation format

Those belong in Project V docs, V Forge docs, workflow docs, governance docs, and implementation-specific docs.

---

## System

- interfaces

---

## Core Rule

A handoff transfers execution responsibility from Project V to V Forge for approved work.

A handoff does not transfer planning ownership.
A handoff does not transfer signal-system ownership.
A handoff does not erase the boundary between planning truth and execution truth.

---

## Interface Definition

The Project V to V Forge handoff interface is the bounded mechanism by which Project V provides V Forge with the execution-facing package required to carry out approved work.

The handoff interface exists so that:

- Project V can remain the planning and orchestration system of record
- V Forge can become responsible for execution truth for the handed-off work
- execution can begin without ownership blur

---

## Handoff Validity Conditions

A handoff is valid only when:

- Project V has determined that the work is ready for handoff
- the required planning-side approval posture has been satisfied
- the minimum handoff semantics required by this interface are present

This document does not define the full approval model.
That model belongs in governance docs.
But a handoff must not be treated as valid if these conditions are not met.

---

## What a Handoff Transfers

A valid handoff transfers:

- execution responsibility for the approved work
- bounded planning context needed to execute the work
- the relevant scope of the approved work
- the relevant readiness truth for the work
- any bounded constraints or conditions that execution must respect
- any bounded evidence references that execution requires

### Explanation
The handoff is not a dump of all planning context.
It is the bounded execution-facing subset of planning truth necessary for V Forge to act correctly.
Project V is responsible for determining what planning context is included in a handoff and for ensuring that only execution-relevant context crosses the interface.

---

## What a Handoff Does Not Transfer

A handoff does not transfer:

- planning ownership
- orchestration ownership
- project-creation authority
- readiness ownership as an open-ended concept
- signal-system ownership
- open-ended research authority
- permission to redefine the project structure casually

### Explanation
After handoff, Project V remains the system of record for planning and orchestration.
V Forge becomes the system of record for execution truth related to the handed-off work.

---

## Minimum Interface Semantics

A handoff should be interpretable as carrying at least the following semantic elements:

- what work is being handed off
- why it is ready to be handed off
- what execution scope is approved
- what boundaries or constraints apply
- what references or evidence are relevant
- what outcomes, artifacts, or execution behavior are expected at a high level
- what should cause V Forge to report findings back or trigger return-to-planning behavior

These semantics may later be represented through specific data structures, but the semantic contract comes first.

---

## Ownership After Handoff

After a valid handoff:

- Project V remains the owner of planning truth
- Project V remains the owner of orchestration truth
- V Forge becomes the owner of execution truth for the handed-off work
- VEDA remains the owner of signal, evidence, and observability truth

No handoff changes the owner of those truth domains.

---

## Allowed Use of Handoff Inputs by V Forge

V Forge may use handoff inputs to:

- execute the approved work
- validate that execution requirements are satisfied within the approved scope, without expanding or reinterpreting that scope
- perform bounded execution-side research needed to complete or validate the handoff
- produce execution outputs
- produce bounded execution findings
- return blocked, failed, incomplete, or changed execution conditions back into the ecosystem

---

## Forbidden Interpretations of Handoff

A handoff must not be interpreted as:

- permission for V Forge to become the planner
- permission for V Forge to perform open-ended ecosystem research
- permission for V Forge to redefine the project casually
- permission for Project V to continue acting as the canonical execution ledger
- permission for V Forge to absorb VEDA’s signal-system role

If a handoff is interpreted that way, the handoff model is being used incorrectly.

---

## Return-to-Planning Trigger Principle

A handoff is not a one-way deletion of planning responsibility.

While execution responsibility moves to V Forge, bounded execution findings may still return to Project V when:

- execution is blocked
- execution fails
- execution is incomplete
- changed conditions affect planning assumptions
- revised evidence or findings require planning reconsideration

The handoff interface therefore works together with the return-to-planning interface.
The handoff interface defines what crosses from Project V to V Forge.
The return-to-planning interface defines what crosses from V Forge back to Project V.
This document does not define that return path.

---

## Human-In-The-Loop Principle

A handoff is a governance-sensitive transition.

Human review or approval may be required before a handoff becomes active, depending on:

- project sensitivity
- execution risk
- external action implications
- mutation scope
- launch sensitivity

A handoff should never be treated as a casual internal state flip if it changes who is responsible for execution.
The governance and approval model for handoff authorization is defined in `../governance/approval-and-escalation-model.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- handoff is a bounded interface
- handoff transfers execution responsibility, not planning ownership
- V Forge receives what it needs to execute, not everything Project V knows
- findings and blocked execution may return to planning later
- the handoff interface is one of the main places where boundary drift must be prevented

If the interface is implemented as an unbounded context dump or an ownership blur, the doctrine is wrong.

---

## Usage

This document should be used:

- when defining handoff packages
- when deciding what planning information may cross into execution
- when reviewing whether a proposed handoff is too broad or too weak
- when writing Project V and V Forge workflow docs
- when evaluating whether a cross-system execution action is correctly authorized

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
- `v-forge-to-project-v-return-to-planning-interface.md` *(planned)*
- `../workflows/handoff-workflow.md` *(planned)*
- `../governance/approval-and-escalation-model.md` *(planned)*
- `../governance/recommendation-packaging-doctrine.md` *(planned)*
