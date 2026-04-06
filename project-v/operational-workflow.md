# Project V Operational Workflow

## Purpose

This document defines the core operational workflow by which Project V performs planning and orchestration inside the V Ecosystem.

It exists to answer:

```text
How does Project V actually operate from intake through planning, readiness, handoff preparation, and return-aware replanning while staying inside its role, governance bounds, and system invariants?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the core operational flow of Project V
- how Project V moves from intake to planning to readiness to handoff preparation
- how Project V handles replanning after governed return inputs
- how Project V should behave when workflow pressure conflicts with governance or boundary rules
- the bounded planning-side workflow posture shared across Project V activity

---

## Out of Scope

This document does not define:

- the detailed intake workflow for the whole ecosystem
- the detailed handoff payload contract
- the detailed return-to-planning payload contract
- detailed schema design
- implementation-specific queueing, scheduling, or UI behavior

Those belong in workflow, interface, and more specific Project V docs.

---

## System

- project-v

---

## Core Rule

Project V operates by turning planning-relevant input into governed planning state, readiness determination, and bounded handoff preparation.

It must not skip from input to execution.
It must not skip from recommendation to approval.
It must not skip from return input to mutated planning truth without governed replanning.

Operational speed does not outrank planning doctrine.

---

## Workflow Definition

The Project V operational workflow is the bounded planning cycle by which Project V:

- receives or recognizes planning-relevant input
- classifies and structures work
- develops planning interpretation
- determines readiness or non-readiness
- prepares handoff when appropriate
- preserves planning continuity
- re-enters planning when governed return inputs require reconsideration

This workflow exists so that Project V remains a planning and orchestration system rather than degrading into ad hoc coordination.

---

## Workflow Principle

Project V must always know which planning state it is in.

The workflow must remain interpretable enough that a later reader or capable LLM can determine:

- what input entered planning
- what Project V concluded about it
- what planning state is now active
- whether work is ready, blocked, deferred, or awaiting approval
- whether handoff is justified
- whether return-driven replanning occurred

If Project V behavior cannot be reconstructed as a governed planning workflow, the operational model has degraded.

---

## Core Operational States

At the baseline level, Project V’s operational workflow should be understood through the following planning-side states.

### 1. Intake-Recognized
Project V has received, recognized, or been given planning-relevant input.

### 2. Planning-In-Progress
Project V is interpreting, structuring, or refining the work as planning truth.

### 3. Readiness-Evaluation
Project V is determining whether the work is planning-ready for handoff, further review, deferment, or rejection.

### 4. Handoff-Preparation
Project V is packaging bounded execution responsibility for V Forge without mutating execution truth itself.

### 5. Awaiting-Approval-or-Activation
Project V has completed the planning-side package or recommendation but is waiting on the approval, activation, or workflow event required before handoff can become active.

### 6. Handed-Off
Project V has completed the governed planning-side handoff transition.
Execution responsibility has moved out of Project V.

### 7. Return-Triggered-Replanning
Project V has received governed return-to-planning input and is re-entering planning for reconsideration.

### Rule
These states may be implemented through different structures, but the planning logic must preserve their semantic distinction.
Project V must not collapse them into one fuzzy "working on it" state.

---

## Entry Rule

Project V work begins when planning-relevant input is recognized through a governed path.

This may include:

- intake-recognized work
- signal-informed planning input
- operator-directed planning input
- return-to-planning input
- continuity-relevant rejected or deferred work being reconsidered through a governed path

Project V must not treat unclassified noise, informal or unrecorded operator statements that have not been established as governed planning direction, or bypassed interface input as equivalent to governed workflow entry.
Operator casual direction expressed in conversation is not automatically governed workflow entry.
It must be classified, scoped, and confirmed as planning-relevant input before Project V admits it as a workflow event.

---

## Intake and Initial Classification Rule

When work enters Project V, the first operational obligation is classification.

Project V must determine, at the level required for planning correctness:

- what the subject is
- whether the input is planning-relevant
- whether the work belongs in Project V at all
- whether the work is new, ongoing, deferred, rejected, or return-triggered
- whether immediate planning is appropriate or whether additional clarification, review, or no-action is required

Project V must not skip classification just because the desired next step feels obvious.

---

## Planning Structuring Rule

Once work is admitted into planning, Project V must structure it as planning truth.

This includes, as appropriate:

- defining work boundaries
- identifying dependencies
- identifying planning-relevant risks or blockers
- relating the work to prior decisions or existing project state
- determining whether the work belongs to an existing project, a new project, or a cross-project planning context

Planning structure must remain reviewable.
A planning state that only exists in transient reasoning is weak Project V behavior.

---

## Recommendation and Decision Rule

Project V may generate recommendations as part of planning.

Project V must preserve the distinction between:

- interpretation
- recommendation
- planning decision
- approval-sensitive action
- handoff activation

A strong planning recommendation must not be treated as though it already changed planning truth unless the governed decision path has actually occurred.

Where approval is required, Project V must wait for the governed approval posture rather than silently advancing the workflow.

---

## Readiness Evaluation Rule

Project V must explicitly determine whether work is ready for handoff, not ready for handoff, deferred, blocked, or rejected.

Readiness evaluation must account for:

- planning completeness at the level required for bounded execution
- whether the execution target and scope are clear
- whether dependencies or blockers materially prevent execution
- whether approval posture is satisfied or still pending
- whether the proposed handoff remains inside Project V’s actual planning authority

Readiness must not be inferred from momentum.
Prepared work is not automatically ready work.

---

## Handoff Preparation Rule

When work is ready to move toward execution, Project V may prepare a bounded handoff package.

Handoff preparation means:

- packaging execution-relevant planning truth
- preserving what is in scope
- preserving what is out of scope
- preserving what approvals or activation state still apply
- preserving the decision and readiness basis for handoff

Handoff preparation is not execution.
Handoff preparation is not approval.
Handoff preparation is not the activation of execution responsibility.

---

## Approval and Activation Rule

Where approval, explicit activation, or governed release conditions are required, Project V must enter an awaiting state rather than pretending the handoff is active already.

This means:

- Project V may complete its planning work before handoff becomes active
- Project V must preserve that approval or activation is still pending
- Project V must not package pending handoff as though execution responsibility has already transferred

When work remains in Awaiting-Approval-or-Activation and conditions materially change, including changed approval authority, changed scope, changed readiness basis, or materially changed evidence, Project V must not treat the original pending approval as still applicable.
The changed condition must be assessed against the governing approval posture.
If the prior approval package is no longer valid for the changed conditions, Project V must return the work to Planning-In-Progress or Readiness-Evaluation rather than advancing on a stale approval basis.
Stale awaiting state is not a shortcut to handoff.

The approval model is governed by `../governance/approval-and-escalation-model.md`.

---

## Handoff Completion Rule

Project V completes the handoff-side workflow only when execution responsibility has transferred through the governed Project V to V Forge handoff path.

At that point:

- Project V remains the owner of planning truth
- V Forge becomes the owner of execution truth for the handed-off scope
- Project V must not continue to behave as though it still owns the active execution path

A prepared but inactive handoff is not a completed handoff.

---

## Return-Triggered Replanning Rule

When Project V receives governed return-to-planning input, it must re-enter planning as a new bounded planning event rather than mutating planning truth directly from the returned content.

This means Project V must:

- classify the return input
- preserve what findings, changes, or conditions triggered return
- determine whether prior planning decisions still hold
- determine whether the prior path should be reaffirmed, revised, superseded, invalidated, or escalated
- preserve continuity between prior planning state and the new replanning state

Return input is not self-applying planning truth.

---

## Deferred, Blocked, and Rejected Workflow Rule

Project V must preserve non-progress states explicitly.

This includes:

- deferred work
- blocked work
- rejected work
- work awaiting approval
- work awaiting clarification

Project V must not treat these as invisible pauses.
They are real planning states and must remain continuity-supporting where later action depends on them.

---

## Decision Continuity Rule

Project V operational workflow must preserve planning-side decision continuity at every stage.

This means:

- intake does not erase prior planning context
- replanning does not reset governing decisions
- handoff preparation does not silently widen prior decisions
- return-triggered reconsideration does not mutate decisions by implication

When continuity conflict appears, the governed path in `../governance/decision-continuity-doctrine.md` applies.

---

## Interface Discipline Rule

Project V operational workflow must preserve interface discipline in both directions.

This means:

- inbound signal must not be treated as governed planning input if it bypassed the proper signal path
- outbound execution responsibility must not bypass the governed handoff path
- inbound return findings must not be treated as proper replanning input if they bypassed the return-to-planning interface

Interface convenience is still interface drift.

---

## Multi-Project Workflow Rule

When Project V operates across multiple projects, it must preserve both portfolio visibility and project-local integrity.

This means:

- project-local planning state must remain distinguishable
- cross-project prioritization must not erase per-project readiness and approval posture
- shared orchestration context must not become an excuse for uncontrolled cross-project mutation

When two or more projects have planning states that materially conflict, including conflicting readiness determinations, conflicting handoff eligibility, or conflicting resource or dependency claims, Project V must surface the conflict explicitly rather than resolving it by momentum or recency.
Cross-project conflict resolution requires the same governed decision and approval posture as intra-project planning decisions.
Project V must not resolve cross-project conflicts informally simply because they seem obvious.

Portfolio-level planning is still governed planning, not portfolio-level override magic.

---

## Governance Conflict Rule

If workflow momentum conflicts with approval posture, actor authority, decision continuity, interface discipline, or bounded scope, governance wins.

Project V must not continue simply because:

- work is almost ready
- the intended next step seems obvious
- a recommendation is strong
- a prior session appeared to want the same outcome
- delay feels inefficient

Project V is a governed planning system, not a momentum engine.

---

## Failure and Replanning Rule

When planning-side failure, blocked workflow progression, invalid approval posture, or continuity conflict prevents legitimate progression, Project V must not hide the interruption.

Depending on the case, the correct response may be:

- halt
- preserve blocked state
- recommend action without activating it
- escalate
- defer
- reject
- re-enter planning through a governed path

Failure handling within Project V must remain consistent with `../governance/failure-and-recovery-doctrine.md`.

---

## Reviewability Rule

Project V operational workflow must remain reviewable enough that a later reader can determine:

- what state the work entered
- what state it moved into
- why the transition occurred
- what approval or continuity posture applied
- what next state is expected

If Project V transitions cannot be reconstructed after the fact, the workflow is not governed strongly enough.

---

## Forbidden Workflow Drift Patterns

Project V operational workflow has drifted if it begins to:

- skip classification
- treat recommendations as decisions
- treat prepared handoffs as active handoffs
- accept bypassed interface input as normal workflow entry
- absorb returned findings as direct planning mutation
- hide deferred, blocked, or rejected work
- use portfolio awareness to erase project-local boundaries
- continue through governance conflict because the outcome appears desirable

These are workflow failures, not harmless shortcuts.

---

## Human-In-The-Loop Principle

Project V operational workflow remains governed human-assisted planning.

Human review remains especially important when the workflow reaches:

- project admission or rejection
- priority change
- readiness change
- handoff activation
- decision revision
- approval-sensitive orchestration change
- return-triggered replanning that changes prior planning posture

Project V should make human planning review more structured, not more ceremonial.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- Project V workflow begins with governed entry and classification
- planning, readiness, handoff preparation, approval waiting, and handoff completion are distinct states
- return-to-planning creates a new bounded replanning event
- deferred, blocked, rejected, and awaiting states are real workflow states
- governance conflict must stop or redirect workflow progression rather than being smoothed over
- interface discipline applies on both inbound and outbound workflow paths

If an LLM could treat Project V workflow as a vague flow from input to action without explicit state distinctions, this doc is failing.

---

## Usage

This document should be used:

- as the baseline operational model for Project V
- when reviewing whether Project V workflow design preserves its role and invariants
- when writing more detailed Project V workflow docs
- when checking whether implementation shortcuts are weakening planning-state clarity
- when aligning future Project V docs to a common workflow spine

---

## Related Docs

- `project-v.md`
- `system-invariants.md`
- `multi-project-doctrine.md`
- `lifecycle.md`
- `v-forge-integration.md`
- `data-boundaries.md`
- `schema-authority.md`
- `../workflows/project-intake-workflow.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/auth-and-actor-model.md`
