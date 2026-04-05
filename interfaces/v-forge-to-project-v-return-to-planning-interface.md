# V Forge to Project V Return-to-Planning Interface

## Purpose

This document defines the interface by which V Forge returns bounded execution findings to Project V when execution requires planning reconsideration.

It exists to answer:

```text
What crosses from V Forge back to Project V when execution needs planning reconsideration, what does that return mean, and what does it not mean?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the meaning of a V Forge to Project V return-to-planning transition
- what kinds of information may cross through the return-to-planning interface
- when execution-side information should return to planning
- what responsibility changes at return time
- what is explicitly not transferred at return time
- the boundary posture operators and LLMs should use when interpreting return-to-planning behavior

---

## Out of Scope

This document does not define:

- V Forge internal execution workflow
- Project V internal replanning workflow
- detailed approval policy
- detailed report structure
- detailed transport or implementation format

Those belong in V Forge docs, Project V docs, workflow docs, governance docs, and implementation-specific docs.

---

## System

- interfaces

---

## Core Rule

The return-to-planning interface transfers bounded execution findings from V Forge back to Project V when execution requires planning reconsideration.

A return-to-planning transition does not transfer execution truth ownership back to Project V.
A return-to-planning transition does not erase the boundary between execution truth and planning truth.
A return-to-planning transition does not turn Project V into the execution ledger.

---

## Interface Definition

The V Forge to Project V return-to-planning interface is the bounded mechanism by which V Forge provides Project V with the execution-side findings required for planning reconsideration.

The return-to-planning interface exists so that:

- V Forge can remain the execution system of record
- Project V can reconsider planning when execution reveals blockers, failures, incompleteness, changed conditions, or findings that affect prior planning assumptions
- execution findings can influence planning without ownership blur

A return-to-planning transition does not automatically cancel or supersede the existing handoff.
The status of the original handoff and any ongoing execution is governed by the outcome of Project V's planning reconsideration.

---

## Return-to-Planning Validity Conditions

A return-to-planning transition is valid only when:

- V Forge has produced bounded execution findings relevant to planning reconsideration
- the return is triggered by blocked, failed, incomplete, or changed execution conditions that cannot be resolved within the approved handoff scope, or by findings that change what planning should do next
- the minimum return-to-planning semantics required by this interface are present

This document does not define the full approval or workflow model.
But a return-to-planning transition must not be treated as valid if these conditions are not met.

---

## Retention Principle

Not all execution findings warrant a return to planning.

Findings that can be resolved within the approved handoff scope without changing what planning should do next should remain inside V Forge execution handling.

Return-to-planning is warranted when the findings:

- cannot be resolved within the approved handoff scope
- block, fail, or materially interrupt approved execution
- change what planning should do next
- invalidate planning assumptions that the original handoff depended on

---

## What Return-to-Planning Transfers

A valid return-to-planning transition transfers:

- bounded execution findings relevant to planning reconsideration
- bounded description of what happened in execution
- the bounded reason execution requires planning reconsideration
- bounded description of blockers, failures, incompleteness, changed conditions, or findings that affect prior planning assumptions where applicable
- any bounded references or artifacts required for Project V to interpret the findings correctly

### Explanation
Return-to-planning does not transfer all execution state.
It transfers the bounded planning-relevant subset of execution-side truth needed for Project V to reconsider planning.
V Forge is responsible for determining what execution-side information is included in the return and for ensuring that only planning-relevant findings cross the interface.

### Finding Boundary Constraint

Execution findings returned through this interface must not be presented as:

- VEDA signal
- governing Project V planning decisions

Execution findings are bounded execution outputs that may inform planning reconsideration.
They do not carry independent planning authority and must be interpreted within the governance rules defined in `../governance/report-structure-and-required-fields.md`.

---

## What Return-to-Planning Does Not Transfer

A return-to-planning transition does not transfer:

- execution truth ownership back to Project V
- open-ended execution state as a planning payload
- permission for Project V to act as the canonical execution ledger
- signal-system ownership
- permission for Project V to reinterpret the return as a full replacement for execution records

### Explanation
After a return-to-planning transition:

- V Forge remains the system of record for execution truth
- Project V remains the system of record for planning and orchestration truth
- VEDA remains the system of record for signal, evidence, and observability truth

The return-to-planning interface changes what Project V may reconsider, not who owns execution history.

---

## Minimum Interface Semantics

A return-to-planning transition should be interpretable as carrying at least the following semantic elements:

- what handed-off work or execution context the return refers to
- what happened in execution at a bounded level
- why execution now requires planning reconsideration
- what findings, blockers, failures, incompleteness, changed conditions, or findings that affect prior planning assumptions matter
- what constraints or assumptions appear invalidated or newly relevant
- what Project V should reconsider at a planning level

These semantics may later be represented through specific data structures, but the semantic contract comes first.

---

## Ownership After Return

After a valid return-to-planning transition:

- V Forge remains the owner of execution truth
- Project V remains the owner of planning truth
- Project V may reconsider planning based on bounded execution findings
- VEDA remains the owner of signal, evidence, and observability truth

No return-to-planning transition changes the owner of those truth domains.

---

## Allowed Use of Return Inputs by Project V

Project V may use return-to-planning inputs to:

- reconsider planning assumptions
- reconsider readiness
- reconsider handoff scope
- create revised planning or orchestration decisions
- request additional bounded evidence through the appropriate ecosystem path where needed
- determine whether new handoff, deferral, cancellation, or restructuring is required

---

## Forbidden Interpretations of Return-to-Planning

A return-to-planning transition must not be interpreted as:

- permission for Project V to absorb full execution state
- permission for Project V to become the canonical execution ledger
- permission for V Forge to redefine planning directly
- permission for Project V to treat all execution findings as new signal-system ownership
- permission to collapse the distinction between execution truth and planning truth
- permission for Project V to issue a new or expanded handoff without re-running appropriate planning and readiness evaluation

If a return-to-planning transition is interpreted that way, the interface model is being used incorrectly.

---

## Relationship to Handoff

The return-to-planning interface works together with the Project V to V Forge handoff interface.

- the handoff interface defines what crosses from Project V to V Forge to begin execution responsibility
- the return-to-planning interface defines what crosses from V Forge back to Project V when planning reconsideration is needed

This document does not define the handoff path.
That path is defined separately.

---

## Human-In-The-Loop Principle

A return-to-planning transition is a governance-sensitive transition because it can change what planning does next.

Human review or approval may be required depending on:

- project sensitivity
- execution risk or failure severity
- strategic impact
- mutation scope
- launch or maintenance sensitivity

All return-to-planning transitions that affect planning direction should be reviewed by a human before planning reconsideration results in new ecosystem actions.
The governance and approval model for these decisions is defined in `../governance/approval-and-escalation-model.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- return-to-planning is a bounded interface
- Project V receives bounded execution findings, not full execution ownership
- V Forge remains the execution system of record after the return
- return-to-planning exists to trigger planning reconsideration, not ownership collapse
- the return interface is one of the main places where execution/planning boundary drift must be prevented

If the interface is implemented as an unbounded execution-state dump or an ownership blur, the doctrine is wrong.

---

## Usage

This document should be used:

- when defining return-to-planning payloads or packages
- when deciding what execution-side information may cross back into planning
- when reviewing whether a proposed return-to-planning transition is too broad or too weak
- when writing Project V and V Forge workflow docs
- when evaluating whether an execution-side issue should remain inside execution or return to planning

---

## Related Docs

- `project-v-to-v-forge-handoff-interface.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/report-structure-and-required-fields.md`
