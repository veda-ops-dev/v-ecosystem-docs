# Approval and Escalation Model

## Purpose

This document defines how approvals and escalations work inside the V Ecosystem.

It exists to answer:

```text
When is approval required, what kinds of approvals exist, when must work escalate, and how should agents behave when approval posture is unclear?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the approval posture used across the V Ecosystem
- when work may proceed without approval and when it may not
- what kinds of approval-sensitive transitions exist
- when escalation is required
- how agents should behave when approval status is missing, ambiguous, or exceeded
- the non-approval posture of delegated runtime work and continuity artifacts

---

## Out of Scope

This document does not define:

- detailed report schemas
- detailed project-specific workflow states
- implementation-specific permission systems
- detailed external-action policies for every tool or provider

Those belong in more specific governance, workflow, and system docs.

---

## System

- governance

---

## Core Rule

Approval is the governance mechanism that allows an action, transition, or outcome to become active when doctrine requires review.

If approval is required, lack of explicit approval is not permission.
If approval posture is unclear, the default is not to proceed as though approval exists.
Escalation is required when a meaningful action cannot be safely or correctly resolved within the current approval posture.

Delegation is not approval.
Continuity artifacts are not approval.

---

## Model Definition

The approval and escalation model exists so that:

- agents do not infer permission from convenience
- governance-sensitive actions are reviewable before they become active
- cross-system transitions remain controlled
- human-in-the-loop control remains real where it matters
- escalation has a defined role instead of being improvised

This document defines the baseline model.
More specific governance docs may refine approval classes for particular workflows or action types.

---

## Approval Principle

Approval is not a general feeling that something seems acceptable.

Approval is a governed state that applies to a specific action, transition, or bounded class of actions under defined conditions.

Approval should be interpreted as:

- explicit rather than implied
- bounded rather than open-ended
- reviewable rather than informal
- contextual rather than universal
- revocable rather than permanent

---

## Escalation Principle

Escalation is required when a situation cannot be safely resolved within the current doctrine, workflow, boundary posture, or approval state.

Escalation exists to prevent silent overreach.
It is not a failure condition by default.
It is the correct behavior when the current governance posture does not support safe continuation.

---

## Governance-Sensitive Action Principle

An action is governance-sensitive when it involves one or more of the following:

- state mutation with meaningful system impact
- external action
- paid action
- approval-gated transition
- launch-sensitive behavior
- cross-system boundary crossing that affects ownership or continuity
- new project creation
- handoff activation
- replanning that materially changes what the ecosystem will do next

Governance-sensitive actions may not proceed as though approval is implied.

---

## Approval Classes

At the baseline level, approval posture should be understood through these classes.

### Class A — In-Bounds, Low-Risk, Non-Mutating Support
Examples:

- bounded interpretation
- bounded classification
- bounded recommendation drafting
- bounded packaging
- preparing reports
- preparing candidate plans without activating them

### Rule
These actions may proceed without special approval when they remain inside current doctrine, workflow, and system boundaries.

---

### Class B — Bounded, Reviewable Mutation or Transition
Examples:

- activating an intake outcome that materially changes planning status
- preparing or activating a handoff
- returning execution findings into a planning-affecting path
- mutating governed records where the action is expected but still meaningful

### Rule
These actions may require approval depending on workflow stage, system role, and risk level.
They must not proceed if the current approval posture is unclear.

### Class B — Doubt-Default Rule
When an action is potentially Class B but the current approval posture is ambiguous, the default is to treat it as requiring approval rather than assuming approval-free continuation.

An agent must not resolve Class B ambiguity by proceeding. The correct response is to produce a bounded recommendation, produce a reviewable approval request, surface the approval question explicitly, or escalate. Treating the action as Class B does not mean the agent may skip directly to activation.

### Class B — Stale Approval Behavior
A Class B approval that was satisfied in a prior session, workflow stage, or planning cycle does not automatically carry forward into a changed context.

If the underlying scope, conditions, or planning basis have materially changed since a Class B approval was granted, the approval must be treated as stale and must not be reused without explicit reconfirmation.
A stale Class B approval posture is unclear approval posture and must be treated accordingly.

Orchestration-produced or runtime-produced changes may also be material when they alter the basis the operator would review for the action.
If delegated work, refreshed context, or continuity reclassification changes what the approval would now mean, the prior approval must be treated cautiously rather than silently reused.

---

### Class C — External, Paid, High-Impact, or Launch-Sensitive Action
Examples:

- paid data pulls
- external publication-sensitive actions
- launch-sensitive changes
- broad-scope execution mutations
- actions that can materially alter ecosystem priorities or public-facing outcomes

### Rule
These actions require explicit governed approval before they become active.
Informal direction does not substitute for governed approval.

---

### Class D — Boundary-Exceeding, Doctrine-Unclear, or Exception Action
Examples:

- actions that appear to exceed current doctrine
- actions that depend on ambiguous authority
- actions that route around normal interfaces or approval paths
- requests that would require exception handling or override posture

### Rule
These actions must escalate.
They must not proceed as normal approved work.

---

## Approval State Principle

For an action that depends on approval, the relevant approval state must be classifiable as one of the following:

- not required
- pending
- approved
- rejected
- expired
- revoked
- escalated

If the approval state cannot be classified, it must be treated as unclear.
Unclear approval state does not permit action.

---

## Approval Scope Principle

An approval applies only to the scope it actually covers.

Approval scope must not be widened silently.

This means agents must not assume that approval for one of the following automatically covers another:

- one workflow stage -> a later workflow stage
- one project -> another project
- one mutation -> broader mutation
- one bounded external action -> future external actions
- one handoff -> a revised or expanded handoff

If the scope is unclear, the approval is not safe to reuse.

---

## Informal Direction Is Not Governed Approval

An operator stating that something is approved in conversation does not automatically constitute a governed approval event.

Where governed approval is required, the approval must still be interpretable as:

- explicit
- reviewable
- bounded in scope
- attached to the relevant action or transition

Informal direction may clarify intent.
It does not erase approval requirements.

---

## Delegation Is Not Approval

Delegated runtime work, specialist-agent output, and coordinator routing do not satisfy approval posture.

A delegated worker may prepare or package material for review.
A coordinator may route or organize work.
Neither creates a governed approval event.

Delegation may improve specialization and operator usefulness.
It must not become a shadow approval path.

---

## Continuity Artifacts Are Not Approval

Memory artifacts, transcript artifacts, compacted continuity products, and retained worker findings may improve continuity and reviewability.
They do not satisfy approval posture.

A continuity artifact may help explain prior context.
It must not be treated as a persisted approval record or as proof that approval still applies.

---

## Reviewability Principle

A valid approval must be reviewable after the fact.

That means the ecosystem should be able to determine:

- what action or transition was approved
- who approved it
- what scope the approval covered
- what conditions or limits applied
- whether the approval is still active, expired, revoked, or superseded

If that cannot be determined, the approval posture is weak and should be treated cautiously.

---

## Escalation Triggers

Escalation is required when one or more of the following are true:

- approval is required but missing
- approval scope is unclear
- authority is unclear
- a requested action appears to exceed current doctrine
- a cross-system transition would occur without a clearly governed path
- uncertainty materially affects correctness
- an exception or override appears necessary
- a prior approval may no longer apply

Escalation should produce a reviewable outcome rather than silent non-deterministic behavior.

---

## Agent Behavior Under Unclear Approval

When approval posture is unclear, the agent must not:

- proceed as though approval exists
- widen the scope of a prior approval silently
- reinterpret informal direction as governed approval
- substitute its own confidence for governance
- treat delegation or continuity artifacts as proof that approval has already been satisfied

Instead, the agent should do one or more of the following:

- stop before activation
- produce a bounded recommendation
- produce a reviewable approval request
- escalate the matter explicitly
- return a no-action posture with the reason preserved

---

## Approval and Workflow Relationship

Approval does not replace workflow.
Workflow does not replace approval.

A workflow may define when an action becomes eligible for approval.
Approval determines whether an approval-sensitive action may become active.

This means:

- readiness is not the same as approval
- recommendation is not the same as approval
- handoff preparation is not the same as handoff activation
- return-to-planning findings are not the same as approval to act on them

When workflow and approval are both relevant, both constraints apply.

---

## Approval and Boundary Relationship

Approval does not erase system boundaries.

Even when an action is approved, the action must still:

- remain inside the correct system role
- use the correct interface or workflow path
- preserve ownership boundaries
- preserve reporting and continuity requirements

Approval authorizes action within doctrine.
It does not authorize doctrine collapse.

---

## Human-In-The-Loop Principle

Human review remains first-class for governance-sensitive actions.

This model assumes that meaningful actions may require human approval before becoming active, especially when they involve:

- project creation
- handoff activation
- external or paid actions
- launch-sensitive behavior
- high-impact replanning
- exceptions or overrides

This principle is not optional ceremony.
It is part of how the ecosystem remains governed.

---

## Approval Request Principle

When an agent requests approval, the request should be bounded and reviewable.

A good approval request should make clear:

- what action is being requested
- why the action is being requested
- what system and workflow stage it belongs to
- what scope the approval would cover
- what risks, uncertainties, or conditions matter
- what happens if approval is granted
- what happens if approval is not granted

An approval request should not bury the real action inside vague language.

---

## Rejection Principle

A rejection is a governed outcome, not a null event.

If approval is denied, the agent must not proceed as though the work is informally tolerated.

Where relevant, rejection should preserve:

- what was denied
- why it was denied
- what conditions would need to change before reconsideration
- whether later reconsideration is expected or not

This supports continuity and prevents repeated rediscovery of rejected paths.

---

## Expiration and Revocation Principle

Approvals are not assumed to remain valid forever.

An approval may become invalid because:

- the workflow stage changed
- the scope changed
- the context changed materially
- the approval was explicitly revoked
- the approval was superseded by a later decision

Agents must not assume stale approval remains reusable.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- approval must be explicit when doctrine requires it
- unclear approval posture is not permission
- escalation is correct when safe continuation is not possible
- workflow eligibility is not the same as approval
- approval does not erase boundaries
- informal direction is not automatically governed approval
- delegation does not satisfy approval
- continuity artifacts do not satisfy approval

If the model is used to justify acting first and normalizing governance later, the doctrine is wrong.

---

## Usage

This document should be used:

- when deciding whether an action may proceed
- when determining whether escalation is required
- when interpreting whether a prior approval still applies
- when designing approval requests or approval records
- when reviewing whether governance-sensitive actions are being handled correctly

---

## Related Docs

- `agent-operating-doctrine.md`
- `decision-continuity-doctrine.md`
- `report-structure-and-required-fields.md`
- `external-action-governance.md`
- `../interfaces/extension-agent-orchestration-model.md`
- `../interfaces/extension-memory-and-continuity-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/project-intake-workflow.md`
