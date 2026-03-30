# Failure and Recovery Doctrine

## Purpose

This document defines how failure, partial failure, blocked execution, unexpected outcomes, and recovery behavior are governed inside the V Ecosystem.

It exists to answer:

```text
What counts as failure inside the V Ecosystem, how should failures be classified and handled, when must work halt, recover, return, escalate, or be reported, and how does the ecosystem prevent failure handling from turning into silent drift, cover-up, or unauthorized improvisation?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what failure means inside the V Ecosystem
- how failures and partial failures should be classified
- how failure handling relates to system boundaries, approvals, and authority
- when work must halt, recover, escalate, or return to planning
- what recovery behavior is allowed and what is forbidden
- what failure outcomes must be preserved through governed reporting and continuity paths
- the baseline failure and recovery posture shared across the ecosystem

This doctrine applies across all ecosystem systems, including Project V planning failures, VEDA signal or evidence failures, and V Forge execution failures.

---

## Out of Scope

This document does not define:

- provider-specific rollback mechanics
- implementation-specific retry logic for every subsystem
- every project-specific incident workflow
- detailed disaster-recovery infrastructure design
- detailed test harness behavior

Those belong in more specific governance, workflow, implementation, or project docs.

---

## System

- governance

---

## Core Rule

Failure handling inside the V Ecosystem must remain bounded, reviewable, attributable, and authority-consistent.

Failure does not authorize boundary collapse.
Failure does not authorize silent recovery.
Failure does not authorize unapproved scope widening.
Failure does not authorize decision drift, approval bypass, or external improvisation.

The correct response to failure is governed recovery, not improvisational sovereignty.

---

## Failure Definition

A failure is any outcome, condition, or interruption in which actual behavior diverges from the governed, approved, expected, or safe path strongly enough that correctness, continuity, governance, or outcome integrity may be affected.

Failure includes more than hard technical breakage.
It also includes:

- blocked execution
- partial completion
- invalid or unsafe state transition
- unexpected external effect
- approval-sensitive work occurring under invalid posture
- recovery conditions that require reassessment
- inability to continue without unauthorized assumption

A failure may be internal, cross-system, or external-facing.
What matters is whether governed handling is required.

---

## Failure Principle

The ecosystem must treat failure as a governed state change, not as an embarrassing detail to smooth over.

Failure handling exists so that:

- the ecosystem can stop making things worse
- incorrect or unsafe state is not normalized by momentum
- operators and later sessions can understand what happened
- recovery remains bounded and reviewable
- return-to-planning, escalation, rollback, or no-action can occur without losing continuity

A clean-looking story that hides real failure is not valid recovery.

---

## Failure Classes

At the baseline level, failures should be understood through the following classes.

### Class F1 — Recoverable Local Failure
Examples:

- bounded operation failure within current approved scope
- retry-safe internal step failure
- recoverable local processing error
- bounded validation failure that does not change governing state

### Rule
F1 failures may be handled locally when recovery remains inside existing authority, approved scope, and workflow boundaries.
F1 does not authorize silent widening of action or scope.

---

### Class F2 — Partial Failure or Uncertain Completion
Examples:

- some but not all approved work completed
- externally visible action may have partially succeeded
- system state cannot be trusted as fully complete or fully failed
- execution outcome is ambiguous

### Rule
F2 failures require explicit state preservation and governed reporting.
Do not assume success.
Do not assume failure.
Do not continue as though ambiguity resolves itself.

---

### Class F3 — Boundary, Authority, or Approval Failure
Examples:

- action attempted under invalid approval posture
- unauthorized scope widening
- external action attempted without required legitimacy
- actor authority found to be invalid or ambiguous during execution
- system role boundary crossed incorrectly

### Rule
F3 failures are governance failures, not ordinary operational noise.
They require halt, preservation, and explicit escalation or governed recovery.

Recovery from an F3 governance failure requires explicit re-establishment of valid authority and approval posture before any action may resume.
The action that triggered the F3 failure must not be retried as though the prior invalid posture was merely a technical glitch.
Re-authorization must follow the same path as original authorization.
If re-authorization is not achievable within the current session or workflow, the situation must return to planning or remain escalated until governing posture is re-established.

---

### Class F4 — External or High-Impact Failure
Examples:

- failed or partial external mutation
- public-facing error or publication error
- spend-creating action with incorrect effect
- launch-sensitive failure
- external side effect with reputational, financial, or compliance consequence

### Rule
F4 failures require immediate governance-sensitive handling.
They must not be treated as routine local execution noise.

---

## Failure Detection Rule

When a failure is detected or materially suspected, the ecosystem must not continue as though the approved path is still clearly valid.

A failure is materially suspected when the evidence available would lead a reasonable actor in the current system and workflow role to question whether the governed path is still clearly valid.
This materiality standard is consistent with the materiality definitions used in `decision-continuity-doctrine.md` and `daily-report-doctrine.md`.

The first obligation is to re-establish what is true now.

This means failure handling should begin by determining, at the level required by the failure class:

- what actually happened
- what is still uncertain
- what scope was affected
- whether governed state has changed
- whether continued action is still authorized

If those questions cannot be answered with enough confidence to proceed safely, the work must not continue as though confidence exists.

---

## Halt Rule

Work must halt at the earliest safe stopping point when one or more of the following are true:

- continued execution would widen the failure
- continued execution would cross approval or authority bounds
- external effect is still unfolding under unclear governance posture
- current state cannot be trusted enough to support safe continuation
- recovery would require unapproved scope expansion
- the actor can no longer determine whether the action remains legitimate

Halt does not always mean abandon.
It means stop making the situation less governable.

---

## Earliest Safe Stopping Point Principle

The earliest safe stopping point is the earliest point at which further action can pause without creating greater harm than continued execution.

The ecosystem must not use "earliest safe stopping point" as an excuse to continue for convenience.

Where stopping immediately would create greater direct harm, the actor may take only the bounded minimum action needed to reach a safer paused state.
That bounded minimum action must not be reinterpreted as permission to continue normal execution.

This principle also applies to mid-execution external actions governed under `external-action-governance.md`.
That doc's halt rule for external action uses this principle as its stopping criterion.

---

## Recovery Principle

Recovery is the bounded process of returning from failure toward a governed, interpretable, and acceptable state.

Recovery may include:

- bounded retry
- rollback
- containment
- state preservation
- return-to-planning
- escalation
- deferred re-entry
- explicit no-action after failure

Recovery is valid only when it remains inside:

- actor authority
- approved scope
- workflow bounds
- system ownership bounds
- reporting and continuity requirements

Recovery is not permission to "just fix it" by any means available.

---

## Local Recovery Rule

Local recovery is allowed only when all of the following are true:

- the failure is classifiable as locally recoverable
- the recovery path remains within existing approved scope
- the actor has authority for the recovery action
- the recovery does not mutate cross-system or external state beyond already approved bounds
- recovery does not require a new decision, new approval, or changed planning posture
- the recovery outcome remains reportable and reviewable

If these conditions are not all true, local recovery is not sufficient.

---

## Retry Rule

A retry is not automatically harmless.

Retry is allowed only when:

- the retry remains within the same approved scope
- the retry does not increase external, financial, or state-mutation risk beyond what was already governed
- the prior failure does not indicate that retry itself is unsafe or illegitimate
- the retry does not conceal the original failure

Repeated retry without changing understanding of the failure is drift, not recovery.

---

## Rollback Rule

Rollback is a governed recovery action, not an automatic reflex.

A rollback may be appropriate when:

- the failed state is less acceptable than the known prior state
- rollback remains authorized and technically possible
- rollback does not create a worse external or governance outcome than containment
- rollback scope is understood and bounded

A rollback must not be treated as invisible cleanup.
If rollback materially affects state, continuity, external effect, or governance posture, it must be reported and preserved.

---

## Containment Rule

Containment is appropriate when full rollback or full continuation is not yet safe.

Containment means taking the bounded minimum action needed to:

- stop further spread of failure
- prevent additional unauthorized effect
- preserve reviewable state
- hold the situation in a governable posture

Containment does not authorize broader mutation.
Containment is a bounded stabilizing action, not a hidden new implementation phase.

Where containment involves external-facing action, it must also comply with `external-action-governance.md`.
External containment does not erase external-action authorization requirements.

---

## Return-to-Planning Rule

Failure handling must return to planning when the failure reveals that:

- the approved execution scope is no longer sufficient
- the original assumptions are materially invalid
- planning must choose among new paths
- recovery requires changed readiness, changed approval, or changed handoff logic
- the ecosystem can no longer treat the prior path as planning-valid

In those cases, failure handling must not mutate planning truth directly from execution.
The governed return-to-planning path must be used.
The governed return-to-planning path is defined in `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`.
Failure-triggered returns must follow that interface model, including its minimum semantic requirements, rather than creating informal ad hoc return signals.

---

## Escalation Rule

Failure handling must escalate when:

- authority is unclear
- approval posture is unclear or invalid
- external consequences exceed local recovery legitimacy
- the correct recovery path cannot be determined safely
- rollback or continuation both have governance-sensitive risk
- recovery requires exception handling
- material uncertainty remains unresolved beyond the point where safe local recovery is possible

Escalation is not failure to manage failure.
It is correct governance behavior when the recovery boundary has been reached.

---

## External Failure Rule

External-facing failure requires stronger control than purely internal failure.

Where failure involves external systems, external audiences, spend, publication, or launch-visible effects:

- external state must be treated as real even if internal state is unclear
- the ecosystem must not assume reversibility without verification
- external recovery must remain inside external-action governance rules
- reputational, financial, contractual, and compliance consequences must be treated as part of the failure state

External failure must not be normalized as ordinary internal retry noise.

---

## Partial and Ambiguous State Rule

When the ecosystem cannot determine whether an action fully succeeded, fully failed, or partially completed, the state must be preserved as ambiguous rather than silently collapsed into success or failure.

This means:

- do not report completion unless completion is justified
- do not report clean failure if externally or internally meaningful residue may remain
- do not continue with follow-on actions that assume resolved state
- preserve what is known, what is unknown, and what remains to be verified

Ambiguous state is a governed state, not an inconvenience to write around.

---

## Approval and Authority Integrity Rule

Failure does not repair invalid authority.
Failure does not convert missing approval into emergency permission by default.

If a failure reveals that an action occurred under invalid or unclear authority posture:

- that invalidity must be preserved explicitly
- recovery must not pretend the original action was legitimate
- follow-up action must still satisfy the relevant authority and approval rules

A bad action followed by a clever cleanup is still a governance event.

---

## Reporting and Durability Rule

Failures, partial failures, blocked recovery, rollback, containment, escalations, and failure-related no-action outcomes that matter to governance must be attributable and durably reportable.

The ecosystem must be able to determine, after the fact:

- what failed
- what class of failure occurred
- what state was affected
- what recovery path was attempted or withheld
- who or what acted
- what approval or authority posture applied
- what uncertainty remained
- what next step was required

If that cannot be determined, failure handling is weak and continuity is degraded.

The report structure is governed by `report-structure-and-required-fields.md`.
Recurring visibility is further governed by `daily-report-doctrine.md`.

---

## Failure vs No-Action Rule

Sometimes the correct governed failure response is no further action.

This may occur when:

- recovery is not authorized
- rollback would create greater harm
- escalation has been raised and no further local action is legitimate
- the safest bounded action has already been taken
- continuation would require unapproved scope or invalid authority

A failure-related no-action outcome must not be confused with neglect.
Where continuity, review, or later action depends on it, the no-action outcome must be preserved explicitly.

---

## Forbidden Failure Patterns

Failure handling is insufficient or invalid when:

- failure is hidden to preserve appearance of success
- retry is used to conceal uncertainty or repeated illegitimacy
- recovery widens scope without approval
- rollback or cleanup occurs without preserving that it happened
- execution mutates planning truth directly after failure
- ambiguous state is reported as resolved without basis
- external failure is treated as ordinary internal noise
- actor authority is assumed during recovery because the original path already started
- a governance failure is rewritten as a purely technical incident

These are governance failures, not acceptable recovery shortcuts.

---

## Human-In-The-Loop Principle

Failure handling is one of the main places where human review must remain real.

If failure is handled through silent improvisation:

- operators lose the ability to understand what actually happened
- later approvals become less trustworthy
- continuity degrades
- risk compounds instead of shrinking
- external consequences become harder to govern

Good recovery is not invisible heroism.
It is bounded, reviewable governance under pressure.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- failure is a governed state, not just a technical inconvenience
- halt, containment, rollback, retry, escalation, and return-to-planning are distinct responses
- failure does not authorize scope widening, approval bypass, or authority improvisation
- ambiguous completion state must be preserved rather than guessed away
- local recovery is allowed only when it stays fully in-bounds
- external failure requires stronger control than internal-only failure

If an LLM treats failure as permission to improvise until the result looks clean, the doctrine is wrong.

---

## Usage

This document should be used:

- when deciding how to respond to failure or uncertain completion
- when reviewing whether recovery is locally allowed or must escalate
- when deciding whether rollback, containment, retry, or return-to-planning is the correct path
- when reviewing whether a failure outcome has been preserved clearly enough for continuity and audit
- when tightening workflow rules for failure-sensitive execution or external action handling

---

## Related Docs

- `approval-and-escalation-model.md`
- `auth-and-actor-model.md`
- `external-action-governance.md`
- `report-structure-and-required-fields.md`
- `daily-report-doctrine.md`
- `decision-continuity-doctrine.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `testing-and-verification-doctrine.md` *(planned)*
