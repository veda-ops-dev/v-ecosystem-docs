# Recommendation Packaging Doctrine

## Purpose

This document defines how recommendations must be packaged inside the V Ecosystem so they remain bounded, reviewable, and distinct from decisions, approvals, actions, and escalations.

It exists to answer:

```text
How should a recommendation be structured and presented so that it supports planning, approval, escalation, or review without being mistaken for a decision, an approval, an authorized action, or an active escalation outcome?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what a recommendation is inside the V Ecosystem
- how recommendations must be bounded and packaged
- what a recommendation must and must not contain
- how recommendations relate to decisions, approvals, actions, escalations, and governed reports
- the baseline recommendation posture shared across systems

---

## Out of Scope

This document does not define:

- the approval process for acting on a recommendation
- the full structure of decision records or ADRs
- workflow-specific implementation details for every recommendation source
- every project-specific recommendation variant
- detailed source trust doctrine

Those belong in more specific governance, workflow, interface, and project docs.

---

## System

- governance

---

## Core Rule

A recommendation is a bounded proposed course of action or interpretation presented for review.

A recommendation is not a decision.
A recommendation is not an approval.
A recommendation is not permission to act.
A recommendation is not an escalation outcome.
A recommendation must be packaged so that later readers can determine what is being proposed, why it is being proposed, what scope it covers, what uncertainty remains, and what must happen before it could become active.

---

## Recommendation Definition

A recommendation is the bounded packaging of a proposed next step, proposed interpretation, or proposed governance-sensitive outcome that is not yet active as governing state.

The recommendation packaging doctrine exists so that:

- recommendations remain reviewable
- recommendations do not get mistaken for decisions or approvals
- agents can propose next steps without silently activating them
- planning, approval, and escalation paths receive clear inputs
- future sessions can understand what was proposed and what still required review

A recommendation may support planning, approval requests, escalations, reprioritization, handoff preparation, return-to-planning review, or no-action reasoning.
But recommendation packaging must preserve that it is still proposed rather than active.

---

## Recommendation Principle

A recommendation must describe a proposed path clearly enough to be evaluated, but narrowly enough that it does not widen scope by packaging alone.

A recommendation must be:

- explicit rather than implied
- bounded rather than open-ended
- reviewable rather than conversationally vague
- attributable rather than anonymous (actor authority is defined in `auth-and-actor-model.md`)
- uncertainty-preserving rather than overconfident
- governance-aware rather than action-smuggling

A recommendation that cannot be evaluated cleanly is weak.
A recommendation that appears to authorize action is mispackaged.

---

## Relationship to Decisions

A recommendation may inform a decision.
It does not become a decision by being well argued, strongly worded, or operationally convenient.

This means:

- a recommendation may propose a decision
- a recommendation may summarize reasons for a decision
- a recommendation may identify the likely best path
- a recommendation does not itself create governing decision state

Where a recommendation is later adopted, the resulting decision must still be established through the proper decision and approval path.

---

## Relationship to Approval

A recommendation may support an approval request.
It is not itself an approval request unless it is explicitly packaged as one through the governed reporting path.

A recommendation must not:

- imply that approval already exists
- imply that approval is unnecessary when doctrine requires it
- hide the fact that additional review is needed
- treat operator preference or agent confidence as governed approval

A recommendation may state that approval is recommended or required.
It must still preserve the distinction between recommendation and approval posture.

---

## Relationship to Action

A recommendation may propose an action.
It must not be packaged in a way that implies the action already occurred, is already authorized, or may proceed automatically.

This means a recommendation must not:

- read like an execution confirmation when execution has not occurred
- read like an approved handoff when approval has not occurred
- read like a resolved escalation when review has not occurred
- read like a final planning decision when planning review remains pending

If a recommendation is packaged so that downstream readers would reasonably treat it as already active, the packaging is wrong.

---

## Relationship to Escalation

A recommendation may propose escalation.
That does not make it an escalation report or an active escalation outcome.

The distinction is:

- a recommendation to escalate proposes that escalation should occur
- an escalation report records that escalation is required, active, or already raised through the governed reporting path

A recommendation to escalate must be packaged with the same bounded elements as any other recommendation.
If immediate escalation is required rather than merely recommended, use the governed escalation report path defined in `report-structure-and-required-fields.md`.

---

## When Recommendation Packaging Is Required

Recommendation packaging is required whenever an agent or operator is proposing a meaningful next step, interpretation, prioritization, change, approval-sensitive transition, or governance-sensitive response that is not yet active as governing state.

This includes at minimum:

- proposed planning changes
- proposed intake outcomes before activation
- proposed handoffs before authorization
- proposed return-to-planning responses
- proposed escalation paths
- proposed approval-sensitive actions
- proposed no-action paths where the no-action itself is being recommended rather than merely reported

When in doubt whether an output is merely descriptive or is actually proposing what should happen next, the safer default is to package it as a recommendation explicitly.

---

## When Recommendation Packaging Is Not Required

Recommendation packaging is not required when the output is purely descriptive, purely historical, or already governed through a different active record type and is not proposing a next step.

Examples include:

- reporting what already happened
- recording an already-made decision
- recording an already-granted approval
- recording an already-completed rejection outcome
- reporting a finding without proposing what should be done next

If the output contains a proposed next step, scope change, or governance-sensitive path, recommendation packaging is required.
When in doubt whether an output contains a proposed next step or governance-sensitive path, the default is to package it as a recommendation explicitly.
The burden of confidence is on the absence of proposed or governance-sensitive content.

---

## Minimum Recommendation Package Semantics

A recommendation package should be interpretable as containing, at minimum, the following semantic elements:

- producer attribution
- recommendation subject
- proposed path
- bounded scope
- basis
- uncertainty, risk, or countervailing considerations
- required approval, review, or escalation posture
- recommended next step

These semantics may later be represented through more specific formats, but the semantic contract comes first.

A recommendation without producer attribution cannot be fully evaluated for authority, scope, or basis.

---

## Required Recommendation Elements

A valid recommendation package must make clear, at minimum:

- who or what produced the recommendation
- what is being recommended
- why it is being recommended
- what scope the recommendation covers
- what assumptions, evidence, findings, or decision context support it
- what uncertainty, risk, or unresolved condition affects it
- what must happen before it could become active
- what would happen if it is accepted
- what the default state is if it is not accepted

A recommendation that cannot answer these questions is not sufficiently packaged for governed use.

---

## Subject Rule

A recommendation must clearly identify what it is about.

Examples include:

- intake candidate
- project priority change
- handoff package
- execution response to findings
- approval-sensitive external action
- escalation question

A recommendation without a clear subject is hard to evaluate and easy to misapply.

---

## Proposed Path Rule

A recommendation must state the proposed path directly.

Examples include:

- recommend creating a project
- recommend deferring intake
- recommend escalating for approval clarification
- recommend withholding handoff pending additional evidence
- recommend return-to-planning rather than execution-side resolution

A recommendation must not force the reader to infer the real proposal from hints or surrounding prose.
Where multiple options are presented, the recommendation must identify which path is being recommended, not merely list alternatives.
An options list without a stated recommended path is incomplete packaging.

---

## Bounded Scope Rule

A recommendation must identify the scope it actually covers.

This means the package must make clear:

- what action, change, or review path is being proposed
- what is inside scope
- what is outside scope
- whether the recommendation is local, cross-system, approval-sensitive, or continuity-sensitive

A recommendation must not silently widen from:

- one action to a broader action class
- one workflow stage to later stages
- one project to multiple projects
- one bounded change to open-ended change

Scope clarity is one of the main protections against recommendation-driven drift.

---

## Basis Rule

A recommendation must include the bounded basis that supports it.

The basis may include:

- signal
- findings
- planning context
- governing decision context
- approval posture
- blocked conditions
- relevant uncertainty
- relevant evidence or references

A recommendation basis must justify why the proposed path is reasonable.
A recommendation that only states a preference without basis is weak packaging.

---

## Uncertainty and Risk Rule

A recommendation must preserve material uncertainty, risk, and relevant countervailing considerations.

This includes cases where:

- evidence is incomplete
- approval posture is unclear
- decision context is unresolved
- a different recommendation could also be reasonable
- the proposed path has meaningful downside or dependency risk

A recommendation must not present itself as certainty when material uncertainty remains.

---

## Approval, Review, and Escalation Rule

A recommendation package must make clear what governance posture still applies.

This means the package must state, where relevant:

- whether approval is required
- whether review is required
- whether escalation is required
- whether the recommendation is only preparatory and not yet activation-ready

A recommendation must not package governance-sensitive action as though no further gate exists.

---

## Acceptance and Non-Acceptance Rule

A recommendation package must make clear what happens if it is accepted and what the default state is if it is not accepted.

This includes, where relevant:

- what action or state change follows acceptance
- whether an alternative path is recommended or expected if it is not accepted
- whether non-acceptance preserves the current state, triggers escalation, or requires different review

For recommendations involving approval-sensitive transitions, handoffs, escalations, or no-action paths, the consequence of non-acceptance must be explicit.

---

## Cross-System Recommendation Rule

A recommendation may refer to more than one system, but it must not collapse ownership boundaries.

This means a recommendation must not:

- package VEDA signal as Project V decision truth
- package V Forge findings as VEDA signal
- package Project V planning intent as V Forge execution authorization
- package cross-system visibility as shared ownership

Cross-system recommendations are allowed.
Cross-system ownership blur is not.

---

## Recommendation vs Report Rule

A report preserves what is true now.
A recommendation proposes what should happen next.

A single artifact may contain both reporting and recommendation content, but the two must remain distinguishable.

If a document includes both:

- the report portion must preserve current governed state
- the recommendation portion must preserve the proposed next step as still proposed

The package must not let recommendation language overwrite the reporting of current state.

---

## Recommendation vs No-Action Rule

A recommendation may recommend no action.
That does not make it equivalent to a no-action report.

The distinction is:

- a no-action report states that no action was taken and why
- a no-action recommendation proposes that no action should be taken next and why

This distinction must remain explicit.
A recommendation for no action must not be packaged as though non-action already occurred unless it actually did.

---

## Recommendation Sufficiency Patterns

A recommendation package is sufficient when it allows a later reviewer to understand:

- what is being proposed
- why it is being proposed
- what scope it covers
- what uncertainty or governance gates still apply
- what would happen next if it were accepted

A recommendation package is insufficient when it:

- sounds decisive without making the action still-proposed status explicit
- hides approval, review, or escalation requirements
- omits material uncertainty or downside
- widens scope by implication
- collapses reporting and recommendation into one ambiguous state
- cannot be evaluated without reconstructing the live session context

---

## Human-In-The-Loop Principle

Recommendation packaging is one of the main ways the ecosystem allows agents to be useful without silently governing.

If recommendations are packaged poorly:

- agents can smuggle action through prose
- approvals become less reliable
- decisions become harder to audit
- cross-system drift becomes easier
- human review becomes less meaningful

Good recommendation packaging preserves the difference between helping decide and deciding.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- a recommendation is proposed, not active
- recommendation quality does not convert recommendation status into decision status
- recommendations must preserve scope, basis, uncertainty, and governance posture
- cross-system recommendations must preserve ownership boundaries
- recommendation packaging exists to support review and safe next-step reasoning, not to bypass approval or decision paths

If recommendation packaging is used to make a proposal feel settled before it is governed, the doctrine is wrong.

---

## Usage

This document should be used:

- when packaging a proposed next step for review
- when deciding whether an output is a recommendation or a report
- when reviewing whether a recommendation is too vague, too broad, or too action-smuggling
- when preparing approval-sensitive or escalation-sensitive proposals
- when tightening recommendation outputs so they remain bounded and reviewable

---

## Related Docs

- `agent-operating-doctrine.md`
- `approval-and-escalation-model.md`
- `report-structure-and-required-fields.md`
- `daily-report-doctrine.md`
- `decision-continuity-doctrine.md`
- `auth-and-actor-model.md`
- `external-action-governance.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/project-intake-workflow.md`
