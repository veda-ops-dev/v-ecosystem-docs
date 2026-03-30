# Invalidation and Supersedence Doctrine

## Purpose

This document defines how governing decisions, approvals, and planning
records are explicitly invalidated or superseded inside the V Ecosystem.

It exists to answer:

```text
When must a prior governing decision, approval, or planning record be
explicitly invalidated or superseded rather than silently replaced,
what makes invalidation or supersedence valid, who may initiate it,
and how must the ecosystem preserve the history of that change?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what invalidation and supersedence mean inside the V Ecosystem
- when each is the correct response to changed conditions
- what makes an invalidation or supersedence valid versus informal
- who has the authority to initiate invalidation or supersedence
- how invalidation and supersedence history must be preserved
- the anti-drift rules that prevent silent replacement of governing decisions

---

## Out of Scope

This document does not define:

- the detailed approval workflow for every decision class
- the exact schema of decision records or ADRs
- the detailed planning-side workflow for Project V replanning
- implementation-specific database mutation mechanics

Those belong in governance, project, and schema docs.

---

## System

- governance

---

## Core Rule

A governing decision, approval, or planning record that is no longer
correct, valid, or applicable must be explicitly invalidated or superseded
rather than silently replaced, quietly ignored, or gradually overwritten
by new assumptions.

Silent replacement is not governance.
It is drift that looks like normal operation until something breaks.

---

## Relationship to Decision Continuity Doctrine

This document extends and refines the invalidation and supersedence rules
established in `decision-continuity-doctrine.md`.

The decision continuity doctrine establishes:

- only approved governing decisions have continuity-binding force
- decisions must be referenced, not rediscovered
- replanning does not reset decision state
- changed evidence or findings do not automatically mutate decisions
- when a conflict exists, it must be resolved explicitly through reaffirmation,
  revision, supersedence, invalidation, or escalation

This document defines how supersedence and invalidation specifically work —
the conditions, authority, process, and record requirements for each.

Where this document is silent, the baseline rules from
`decision-continuity-doctrine.md` apply.

---

## Definitions

### Invalidation
Invalidation is the explicit determination that a prior governing decision,
approval, or planning record is no longer valid because:

- the underlying assumptions have been proven false
- the required conditions no longer exist
- governing context has materially changed
- later evidence or findings remove the basis for continued validity

An invalidated record remains part of history.
It must not continue to constrain active behavior.

### Supersedence
Supersedence is the explicit replacement of a prior governing decision,
approval, or planning record with a new governing decision that covers
the same or overlapping scope.

A superseded record remains part of history.
The new record becomes the active governing constraint.
The old and new records must not be treated as co-equal active authority
after supersedence occurs.

### Key Distinction
Invalidation removes a decision's binding force because its basis is gone.
Supersedence replaces a decision's binding force with a new governing choice.

Both require explicit action.
Neither happens automatically from changed conditions alone.

---

## When Invalidation Is Required

Invalidation is required when a governing decision, approval, or planning
record can no longer be treated as valid because:

- the factual assumptions it rested on have been materially contradicted
- the conditions required for the decision to remain applicable no longer exist
- later evidence demonstrates the decision was based on incorrect or
  incomplete information that would have changed the decision if known
- the decision's scope has become inapplicable due to structural changes
  in the ecosystem, project, or external environment

### Rule
Changed conditions alone do not automatically invalidate a decision.
Invalidation requires an explicit determination that the conditions above apply,
followed by an explicit governed invalidation action.
An actor may not treat a decision as implicitly invalidated merely because
circumstances have changed.

The materiality standard for determining whether changed conditions trigger an
invalidation obligation is the same standard used in `decision-continuity-doctrine.md`:
a change is material when it would have been decision-relevant at the time the
governing decision was made.
When materiality is uncertain, the default is to treat the change as potentially
material and apply this rule cautiously rather than assuming the prior decision
remains fully valid.

---

## When Supersedence Is Required

Supersedence is required when:

- a governing decision is being replaced by a new governing decision
  covering the same or overlapping scope
- a prior approval is being replaced by a revised approval for the
  same action class or scope
- a planning record is being revised in a way that changes what
  the ecosystem may do under that record's authority

### Rule
Supersedence must be explicit.
A new decision that implicitly overrides a prior decision without referencing
and superseding it creates contradictory governing context.
That contradiction must not be left unresolved.

---

## What Makes Invalidation Valid

An invalidation is valid only when all of the following are true:

- the invalidation is explicit — recorded and reviewable, not implied
- the invalidation identifies the specific decision, approval, or record
  being invalidated
- the invalidation states the reason — what conditions or evidence
  triggered the determination that validity is gone
- the invalidation is initiated by an actor with the authority required
  for the relevant decision class and impact level
- the invalidation satisfies the approval posture required by the
  decision class being invalidated

An invalidation that is present in form but absent in any of those
dimensions is not a valid governed invalidation.

---

## What Makes Supersedence Valid

A supersedence is valid only when all of the following are true:

- the supersedence is explicit — it references the prior governing decision
  being replaced
- the supersedence explains why the prior decision is no longer sufficient,
  no longer correct, or no longer the active governing choice
- the new governing decision is established through the appropriate
  governed path
- the supersedence satisfies the approval posture required for the
  new decision's scope and impact level
- the prior decision's history is preserved — supersedence does not
  erase the record, only its active binding force

---

## Authority Rule

Invalidation and supersedence must be initiated by the system or actor
that owns the relevant governing context, or through a governed escalation path.

This means:

- Project V governs the invalidation and supersedence of planning decisions,
  handoff records, readiness evaluations, and orchestration decisions
- VEDA governs the invalidation and supersedence of observatory configuration,
  evidence provenance records, and signal classification decisions
- V Forge must not unilaterally invalidate or supersede governing planning
  decisions — it may return findings that trigger reconsideration through
  the governed return-to-planning path
- cross-system invalidation or supersedence must pass through the relevant
  governed interface and approval path

### Rule
An actor may not self-authorize invalidation or supersedence of a decision
that belongs to a different system's truth domain.
The authority boundary for invalidation and supersedence mirrors the
authority boundary for the original decision.

---

## Approval Posture Rule

Invalidation and supersedence require the same or equivalent approval posture
as was required for the original decision.

If the original governing decision required human review and explicit approval,
its invalidation or supersedence requires the same.

If the original decision was approval-gated, the invalidation or supersedence
is also approval-gated.

### Rule
An agent may not reduce the approval posture required for invalidation or
supersedence below what the original decision required.
A decision that was hard to make should not be easy to invalidate.

---

## Partial Invalidation Rule

Some invalidations affect only part of a governing decision's scope.

When an invalidation is partial:

- the specific portion being invalidated must be identified explicitly
- the remaining portions that retain validity must be identified explicitly
- the partial invalidation must not be used to gradually erode
  the rest of the decision without additional explicit governed action

Partial invalidation is not a mechanism for incremental silent replacement.

---

## Scope Integrity Rule for Supersedence

A superseding decision must not silently expand scope beyond what the
prior decision covered unless that expansion is explicitly justified
and approved.

A superseding decision that expands scope is both a supersedence of
the prior decision and a new decision for the expanded scope.
Both aspects require appropriate governed treatment.

### Rule
Supersedence must not be used to launder scope expansion.
If the new decision covers more than the old one, the additional scope
is new governing territory that requires its own justification and approval.

---

## Record Preservation Rule

Both invalidated and superseded records must remain part of the ecosystem's
decision history.

Invalidated records must be:

- marked as invalidated with the date and reason
- preserved as historical context
- not used to constrain active behavior after invalidation

Superseded records must be:

- marked as superseded with a reference to the superseding decision
- preserved as historical context
- not treated as co-equal authority alongside the superseding decision

### Rule
Deletion of a governing decision record is not the same as invalidation.
Invalidation preserves the record while removing its binding force.
Deleting a record removes the governance history that later sessions need
to reconstruct why current governing decisions exist.

---

## Continuity After Invalidation Rule

When a governing decision is invalidated and there is no superseding
decision in place, the ecosystem must not behave as though the invalidated
decision still applies or as though anything is permitted in its absence.

Invalidation of a governing decision without replacement creates a
governance gap.
That gap must be explicitly managed:

- escalate to establish a replacement decision if one is needed
- explicitly withhold action that depended on the now-invalid decision
- preserve the governance gap as a known state rather than filling it
  with assumption

### Rule
An invalidation is not permission to operate freely in the gap it creates.
It is an obligation to manage that gap through governed means.

---

## Agent Behavior Rule

Agents must not initiate invalidation or supersedence unilaterally.

Agents may:

- identify evidence or conditions that suggest invalidation or supersedence
  may be warranted
- prepare a recommendation package describing the identified conditions
  and proposed action for human review
- surface the conflict explicitly through the governed escalation path

Agents must not:

- treat identified conditions as automatic authorization to invalidate
- self-authorize a supersedence by acting as though the prior decision
  is already replaced
- proceed under a new assumption without explicit invalidation or
  supersedence of the prior governing decision

### Rule
An agent that identifies a need for invalidation or supersedence must
escalate rather than self-execute.
Recognizing the need is not the same as having the authority to act on it.

---

## Forbidden Invalidation and Supersedence Patterns

The following are governance failures:

- treating a decision as implicitly invalidated because conditions changed
- treating a new decision as superseding a prior one without explicit reference
- initiating invalidation or supersedence without the required approval posture
- using partial invalidation to gradually erode a decision that should be
  explicitly superseded or fully invalidated
- using supersedence to launder scope expansion without additional approval
- deleting decision records instead of marking them as invalidated or superseded
- an agent self-authorizing invalidation or supersedence based on
  identified conditions alone
- allowing a governance gap created by invalidation to be filled by assumption
- V Forge unilaterally invalidating or superseding Project V governing decisions

---

## Human-In-The-Loop Principle

Invalidation and supersedence are governance-sensitive because they change
what the ecosystem is allowed to do.

Human review is required when:

- a governing decision with significant planning, access, or spend implications
  is being invalidated or superseded
- the invalidation or supersedence affects cross-system behavior or boundaries
- there is disagreement about whether conditions warrant invalidation
- the approval posture for the original decision required human review

An agent's determination that invalidation or supersedence is warranted
is a recommendation.
It is not authorization.

When actors disagree about whether conditions warrant invalidation or supersedence
of a governing decision, the disagreement must be resolved explicitly through the
governed conflict resolution path defined in `decision-continuity-doctrine.md` —
including escalation if required.
A disagreement about validity must not resolve through one actor quietly proceeding
as though the decision is invalid while another assumes it remains valid.
Unresolved disagreement about whether a decision should be invalidated or superseded
is itself a governance gap that requires explicit management, not silent assumption.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- changed conditions do not automatically invalidate or supersede decisions
- both invalidation and supersedence require explicit, governed action
- the authority to invalidate or supersede mirrors the authority to make
  the original decision
- agents may identify the need but must escalate rather than self-execute
- governance gaps created by invalidation must be managed, not assumed away
- decision history must be preserved even when binding force is removed

If an LLM treats a changed condition as permission to proceed under a
new assumption without explicit invalidation or supersedence, this
doctrine is failing.

---

## Usage

This document should be used:

- when evaluating whether a prior governing decision must be explicitly
  invalidated or superseded before new action may proceed
- when reviewing whether a proposed invalidation or supersedence satisfies
  the required conditions and authority
- when deciding whether an agent has correctly escalated an invalidation
  need rather than self-executing it
- when reviewing whether decision history has been correctly preserved
  after invalidation or supersedence
- when resolving conflicts between a current proposal and a prior
  governing decision that has not been formally addressed

---

## Related Docs

- `decision-continuity-doctrine.md`
- `approval-and-escalation-model.md`
- `auth-and-actor-model.md`
- `agent-operating-doctrine.md`
- `allowed-agent-actions-matrix.md`
- `failure-and-recovery-doctrine.md`
- `report-structure-and-required-fields.md`
- `../project-v/system-invariants.md`
- `../project-v/operational-workflow.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../ecosystem/cross-system-boundaries.md`
