# Handoff Workflow

## Purpose

This document defines the cross-system workflow by which approved Project V work becomes active execution responsibility in V Forge inside the V Ecosystem.

It exists to answer:

```text
How does planning-ready work move from Project V into active V Forge execution, what stages govern that transition, and what responsibilities remain bounded on each side?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the workflow from Project V readiness into active V Forge execution responsibility
- the main stages of handoff from planning-side preparation through execution-side acceptance
- which systems are responsible at each stage
- the boundary posture operators and LLMs should use during handoff
- when a prepared handoff is not yet an active handoff
- when execution should not begin even if planning work is substantially complete

---

## Out of Scope

This document does not define:

- the detailed Project V internal planning workflow
- the detailed V Forge internal execution workflow
- the full approval policy for every handoff case
- the detailed transport or storage format of handoff packages
- the detailed return-to-planning workflow after execution has already begun

Those belong in Project V docs, V Forge docs, interface docs, governance docs, and later workflow docs.

---

## System

- workflows

---

## Core Rule

Handoff is the governed workflow by which execution responsibility moves from Project V to V Forge for approved work.

Planning readiness does not automatically become execution.
Handoff preparation does not automatically become active handoff.
Execution must not begin from a fuzzy “basically ready” state.

The handoff workflow exists to preserve the boundary between planning truth and execution truth while still allowing work to move forward.

---

## Workflow Definition

The handoff workflow is the bounded cross-system workflow that moves from:

- Project V readiness determination
- bounded handoff preparation
- approval or activation satisfaction where required

through:

- governed handoff activation
- V Forge receipt and execution-side assumption of responsibility

into:

- active V Forge execution responsibility for the handed-off scope

This workflow exists so that the ecosystem can move from planning to execution deliberately rather than by implication.

---

## Workflow Preconditions

The handoff workflow should begin only when:

- Project V has determined that the work is ready for handoff at the planning level
- the execution target and approved scope are bounded enough for execution
- the minimum handoff semantics required by the handoff interface are present
- the applicable approval, activation, or release posture is either already satisfied or has been explicitly identified as still pending

The handoff workflow must not begin from:

- incomplete or unbounded planning interpretation
- informal execution intent without governed planning readiness
- a recommendation that has not become a planning-side handoff-ready outcome
- execution pressure alone
- an assumption that V Forge can “figure out the rest” from partial planning

---

## Primary Workflow Stages

## Stage 1 — Handoff Readiness Determined

### Description
Project V determines that work is planning-ready for handoff.

This means Project V has concluded, at the level required for bounded execution, that:

- the work is real
- the scope is sufficiently bounded
- the execution objective is sufficiently clear
- known planning-side blockers have been handled, deferred explicitly, or surfaced as constraints
- the work should move toward execution rather than remain in planning

### Responsibility
- Project V owns readiness determination

### Boundary Rule
Readiness determination is still planning truth.
At this stage, execution responsibility has not moved.
V Forge does not determine whether Project V is ready to hand off.

---

## Stage 2 — Handoff Package Preparation

### Description
Project V prepares the bounded handoff package required for execution.

This includes, at minimum, preserving the semantic meaning of:

- what work is being handed off
- why it is ready
- what scope is approved
- what constraints apply
- what evidence references matter
- what outcomes or execution behavior are expected at a high level
- what conditions should trigger return-to-planning behavior

### Responsibility
- Project V owns handoff package preparation

### Boundary Rule
Handoff package preparation is not execution.
It is also not permission to widen scope casually.
Project V prepares the execution-facing planning subset, not a full dump of all planning state.

---

## Stage 3 — Approval or Activation Check

### Description
The ecosystem determines whether the handoff may become active now or must remain pending.

Depending on the case, this may include:

- human approval
- governance confirmation
- release-condition satisfaction
- confirmation that no materially relevant change has invalidated the pending handoff basis

### Responsibility
- Project V owns the planning-side awaiting state
- governance rules determine whether approval or escalation is required
- human operators may provide required approval where applicable

### Boundary Rule
A prepared handoff is not an active handoff if approval or activation is still pending.
No one gets to squint at a nearly finished package and declare victory.
Pending is pending.

---

## Stage 4 — Handoff Activation

### Description
The handoff becomes active through the governed Project V to V Forge handoff path.

At this point, the handoff is no longer merely prepared or awaiting activation.
It is now the active transfer of execution responsibility for the bounded approved scope.

### Responsibility
- Project V owns the planning-side activation of the handoff
- the cross-system transfer occurs through the governed handoff interface

### Boundary Rule
Handoff activation transfers execution responsibility, not planning ownership.
Project V remains the owner of planning and orchestration truth.
VEDA remains the owner of signal, evidence, and observability truth.

---

## Stage 5 — V Forge Receipt and Execution-Side Acceptance

### Description
V Forge receives the active handoff and assumes execution responsibility for the handed-off scope.

This means V Forge accepts the bounded execution-facing package as the basis for execution activity within the approved scope and constraints.

### Responsibility
- V Forge owns execution responsibility after valid handoff receipt
- Project V remains the owner of planning truth for the handed-off work

### Boundary Rule
V Forge receipt does not mean V Forge becomes the planner.
It means V Forge now owns execution truth for the handed-off scope.
If the handoff is invalid, materially incomplete, or cannot be acted on within scope, the correct response is governed interruption or return, not improvisational planning takeover.

---

## Stage 6 — Post-Handoff Boundary Stabilization

### Description
After handoff activation and receipt, each system must continue behaving according to its role.

This means:

- Project V preserves planning continuity and does not pretend to be the active execution ledger
- V Forge executes within bounded scope and does not casually redefine planning
- VEDA remains the signal and observability system of record
- later execution findings that affect planning must use the return-to-planning path rather than informal cross-system mutation

### Responsibility
- Project V owns continued planning continuity
- V Forge owns continued execution truth
- governance and interface rules continue to constrain both sides

### Boundary Rule
Handoff is a transfer of responsibility, not a boundary collapse.
If post-handoff behavior turns into shared fuzzy ownership, the workflow has drifted.

---

## Handoff Outcome Semantics

A valid handoff workflow outcome should be interpretable as answering:

- what work was handed off
- why handoff was justified
- what scope was approved for execution
- whether approval or activation was required and satisfied
- when execution responsibility actually transferred
- what constraints remained active at transfer time
- what kinds of findings should trigger return-to-planning behavior later

These semantics may later be represented through specific workflow states, records, or packages, but the semantic contract comes first.

---

## Awaiting State Principle

A key handoff distinction must remain explicit:

- handoff-prepared
- awaiting approval or activation
- actively handed off

These are not the same state.

Work that is prepared but still awaiting approval, release, or activation must not be treated as though execution has already begun.
If conditions materially change while the handoff is waiting, the pending handoff basis may need replanning or renewed approval rather than automatic continuation.

If a pending handoff's planning basis is materially invalidated by changed conditions while awaiting approval or activation — including changed evidence, changed readiness assessment, changed scope, or changed approval authority — the pending handoff must not be activated on the original basis.
The correct response is to return the handoff to Stage 2 preparation or Stage 1 readiness evaluation with the changed conditions explicitly preserved.
A stale awaiting-approval state is not authorization to proceed.

This distinction is one of the main places where planning-to-execution drift otherwise sneaks in.

---

## Execution Entry Principle

Execution should begin only after valid handoff activation and V Forge receipt.

Execution must not begin because:

- the work looks obvious
- the package is almost complete
- the operator expects it probably to go through
- the same kind of work was approved before
- delay feels inefficient

The handoff workflow exists partly to stop “probably fine” from becoming doctrine.

---

## Insufficient Handoff Principle

If a proposed handoff lacks the minimum semantics required for bounded execution, the correct result is not forced activation.

The correct response may include:

- remain in Project V handoff preparation
- return to readiness evaluation
- remain awaiting approval
- escalate
- reject activation
- preserve blocked transition state

Weak handoff packages should not be rescued by execution-side guesswork.

---

## Human-In-The-Loop Principle

Handoff is a governance-sensitive workflow because it changes which system is responsible for active work.

Human review or approval may be required depending on:

- project sensitivity
- execution risk
- external action implications
- mutation scope
- launch sensitivity
- cost or paid-action implications

The approval and escalation posture is defined in `../governance/approval-and-escalation-model.md`.

Before handoff activation, the pre-action verification obligations defined in `../governance/testing-and-verification-doctrine.md` apply — including Class V1 precondition verification and Class V4 approval verification.
Activation without verified preconditions is activation on unconfirmed assumptions.

---

## Decision Continuity Principle

The handoff workflow must preserve continuity across the planning-to-execution transition.

This means:

- readiness basis must remain traceable into handoff
- approval-sensitive handoffs must preserve whether approval was pending or satisfied
- active handoff must remain distinguishable from recommended or prepared handoff
- later return-to-planning events must be understandable in relation to the prior handoff

If the transition cannot be reconstructed later, the workflow was not governed strongly enough.

---

## Failure and Interruption Principle

When the handoff workflow cannot legitimately progress, the interruption must remain explicit.

Depending on the case, the correct response may be:

- remain in preparation
- remain awaiting approval or activation
- preserve blocked handoff state
- escalate
- return to planning readiness evaluation
- invalidate the proposed handoff basis

The workflow must not silently convert interruption into execution start.

Failure handling should remain consistent with `../governance/failure-and-recovery-doctrine.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- handoff is a multi-stage governed workflow, not a single state flip
- readiness, preparation, approval waiting, activation, and V Forge receipt are distinct
- execution responsibility transfers only at active handoff
- Project V remains the planning system of record after handoff
- V Forge becomes the execution system of record for the handed-off scope
- weak or pending handoffs must not be treated as active execution
- return-to-planning later exists for cases where execution findings require reconsideration

If the workflow is implemented as “Project V finished thinking, so execution probably starts now,” the doctrine is wrong.

---

## Usage

This document should be used:

- when designing workflow states around handoff
- when deciding whether planning-ready work may actually move into execution
- when checking whether a proposed handoff is still pending or truly active
- when reviewing whether Project V and V Forge are preserving boundary discipline during transition
- when writing more detailed Project V, V Forge, or maintenance workflow docs
- when evaluating whether execution has begun without a legitimate governed handoff

---

## Related Docs

- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/project-v.md`
- `../project-v/operational-workflow.md`
- `../v-forge/v-forge.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/testing-and-verification-doctrine.md`
- `maintenance-and-replanning-workflow.md`
