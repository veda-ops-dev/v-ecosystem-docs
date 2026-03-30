# V Forge Human-In-The-Loop Doctrine

## Purpose

This document defines how human-in-the-loop control works inside V Forge.

It exists to answer:

```text
When does V Forge require human review or approval before proceeding, what kinds
of execution actions must never be self-authorized by an agent, and how does
V Forge preserve meaningful human control without blocking all execution?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- when V Forge execution requires human review or approval
- what action classes must not be self-authorized by agents in V Forge
- how human approval integrates with the handoff, launch, and return-to-planning workflows
- how V Forge preserves governed human control without blocking routine bounded execution
- the anti-drift rules that prevent V Forge from treating agent confidence as human approval

---

## Out of Scope

This document does not define:

- the detailed approval thresholds for every action variant
- implementation-specific UI or notification mechanics
- every project-specific execution variant

Those belong in governance docs, workflow docs, and project-specific docs.

---

## System

- v-forge

---

## Core Rule

V Forge is a bounded execution system, not an autonomous execution engine.

Human-in-the-loop control inside V Forge means that approval-sensitive execution
actions require explicit human authorization before they become active.
Agent confidence, execution momentum, and operational efficiency do not substitute
for required human approval.

Bounded, low-risk execution within clearly approved scope may proceed without
per-action human approval. Approval-sensitive actions may not.

---

## What Always Requires Human Approval

The following V Forge actions require explicit human approval before proceeding
regardless of agent assessment:

### Launch-sensitive execution
Any action that creates or changes externally visible content, initiates
public-facing distribution, activates paid spend at launch scale, or creates
changes that are difficult or impossible to reverse.

The launch readiness workflow governs this approval gate:
`../workflows/launch-readiness-workflow.md`

### External actions beyond approved scope
Any external mutation, paid retrieval, or outbound communication beyond the
scope confirmed in the active handoff and its approval posture.

### Execution scope expansion
Any widening of the execution scope beyond what the active handoff approved.
Scope expansion requires a new or revised handoff, not self-authorization.

### Return-to-planning activation that materially affects planning direction
When V Forge determines that execution findings require planning reconsideration,
the return-to-planning interface transfer and subsequent planning review involve
human evaluation of whether replanning is warranted.

### Archive or close decisions
V Forge does not archive or close projects independently.
Those are planning-level lifecycle decisions governed by Project V with human review.

---

## What Does Not Require Per-Action Human Approval

Within an active, valid, approved handoff scope, V Forge agents may proceed
with bounded execution without per-action human approval when:

- the action is clearly within the approved execution scope
- the action does not involve external mutation, paid spend, or launch-sensitive behavior
- the action does not widen scope beyond the handoff
- the action does not produce a finding that requires return-to-planning
- the action is not producing a result that the agent cannot honestly characterize

Routine bounded execution is not approval-gated at every step.
Approval gates apply to the transitions and actions that qualify as
governance-sensitive under the approval and escalation model.

---

## Agent Behavior Under Approval Requirement

When V Forge execution reaches a point requiring human approval, the agent must:

1. Stop before the approval-sensitive action
2. Package a bounded recommendation or approval request
3. Surface it through the governed reporting path
4. Wait for explicit human authorization before proceeding

The agent must not:
- proceed because the action seems clearly right
- proceed because prior similar actions were approved
- proceed because stopping seems operationally inconvenient
- reframe the action as lower-risk to avoid the approval gate
- treat operator presence in the session as implicit approval

---

## Pre-Launch Verification

Before launch-sensitive execution, V Forge must complete pre-launch verification
as defined in Stage 3 of the launch readiness workflow.

Pre-launch verification is the execution-side confirmation that:
- execution work is complete and ready at the required level
- the execution scope matches what was handed off and approved
- no mid-execution findings have emerged that affect launch readiness
- external action preconditions are satisfied

Pre-launch verification is an input to the cross-system launch readiness confirmation.
It is not itself launch authorization.
Human launch authorization must still follow through Stage 5 of the launch
readiness workflow, even when pre-launch verification is complete.

---

## Reporting as Governance

V Forge's governed reporting is part of how human oversight remains real.

When V Forge reports honestly on:
- what execution was performed
- what was not completed
- what findings emerged
- what uncertainty exists
- what requires human review

...it makes human approval meaningful rather than ceremonial.

A V Forge report that hides partial completion, smooths over uncertainty,
or presents ambiguous outcomes as clean results weakens human-in-the-loop
control regardless of whether a human technically reviewed it.

Reporting standards are defined in:
`../governance/report-structure-and-required-fields.md`

---

## Failure and Interruption Posture

When V Forge execution cannot proceed safely or within authorized scope,
the correct response is to halt, preserve state, report, and await guidance.

V Forge must not:
- continue executing past a scope limit because momentum feels productive
- improvise a solution that bypasses the approval gate
- self-authorize a return-to-planning without the governed return path

The failure and recovery doctrine governs interruption behavior:
`../governance/failure-and-recovery-doctrine.md`

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- approval-sensitive V Forge actions require explicit human authorization
- agent confidence does not substitute for human approval
- bounded routine execution within approved scope does not require per-action approval
- honest reporting is itself a governance mechanism
- stopping at an approval gate is correct behavior, not failure

If a V Forge agent self-authorizes a launch-sensitive action because it assessed
the action as clearly correct, this doctrine is failing.

---

## Usage

This document should be used:

- when designing V Forge execution workflows to identify where approval gates belong
- when reviewing whether an execution action required human approval and received it
- when evaluating whether an agent correctly stopped at an approval boundary
- when writing V Forge operator surface docs and reporting docs

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `reporting-and-approval-model.md`
- `../workflows/launch-readiness-workflow.md`
- `../workflows/handoff-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/allowed-agent-actions-matrix.md`
- `../governance/report-structure-and-required-fields.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/external-action-governance.md`
- `../interfaces/operator-surface-interfaces.md`