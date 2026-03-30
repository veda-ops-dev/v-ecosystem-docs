# Maintenance and Replanning Workflow

## Purpose

This document defines the cross-system workflow by which the V Ecosystem
re-enters planning after execution findings, changed conditions, or
planning-side drift require reconsideration of prior governing decisions.

It exists to answer:

```text
How does the ecosystem move from active execution or stable post-handoff state
back into governed planning reconsideration without collapsing execution truth
into planning truth, without silently resetting decision continuity, and without
treating every execution finding as authorization to rewrite prior planning?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the workflow by which execution findings, changed conditions, or planning
  drift trigger governed reconsideration
- how return-to-planning inputs are received and classified before replanning begins
- how replanning preserves decision continuity rather than resetting it
- how the ecosystem distinguishes replanning from ordinary planning-state mutation
- how maintenance activity — ongoing bounded work within existing approved scope —
  is distinguished from replanning
- the boundary posture operators and LLMs must preserve during reconsideration

---

## Out of Scope

This document does not define:

- the detailed internal Project V replanning workflow steps
- the detailed V Forge execution workflow after a revised handoff
- the exact return-to-planning payload format
- detailed failure recovery mechanics
- every project-specific replanning variant

Those belong in Project V docs, V Forge docs, interface docs, governance docs,
and the failure-and-recovery-doctrine.

---

## System

- workflows

---

## Core Rule

Return-to-planning and replanning are governed workflow events, not silent
state corrections.

When execution findings, changed conditions, or planning drift require
reconsideration, the ecosystem must re-enter planning explicitly through
a governed path — preserving what was known before, what changed, and
why reconsideration is warranted.

Replanning does not reset decision continuity.
Replanning does not erase who owns what.
Replanning does not convert execution findings into automatic planning mutations.

---

## Key Distinctions

Before describing the workflow, three key distinctions must be clear.

### Maintenance vs Replanning
Maintenance is ongoing bounded work within existing approved scope that
does not require reconsideration of prior governing decisions.

Replanning is a governed reconsideration of prior planning decisions triggered
by new information, changed conditions, or execution findings that affect
the planning basis.

Maintenance does not require this workflow.
Replanning does.

### Return-to-Planning vs Planning Mutation
Return-to-planning is the governed transfer of bounded execution findings
from V Forge to Project V through the governed interface.
It is a handoff of information, not a handoff of planning authority.

Planning mutation is the direct change of planning records, decisions, or
orchestration state.
Planning mutation may follow return-to-planning, but it does not occur
automatically from return-to-planning input alone.

### Replanning vs Scope Creep
Replanning is a bounded, governed reconsideration of specific planning
decisions affected by new information.

Scope creep is the gradual expansion of planning through accumulated
assumptions, execution-side findings treated as planning authority, or
convenience-driven additions that bypass the replanning workflow.

Scope creep is a drift pattern, not a workflow outcome.

---

## Workflow Triggers

The maintenance and replanning workflow is triggered when one or more of
the following occur:

- V Forge returns bounded execution findings through the governed
  return-to-planning interface that materially affect planning
- execution is blocked, failed, or incomplete in a way that requires
  Project V to reconsider the planning basis
- changed external conditions invalidate assumptions that underpinned
  a governing handoff or planning decision
- VEDA surfaces materially changed signal that affects a governing
  planning decision's evidence basis
- an operator or governance review identifies planning drift that
  requires explicit reconsideration
- the ecosystem detects a contradiction between current execution state
  and prior governing planning decisions

The workflow is not triggered by:

- execution findings that can be resolved within approved scope by V Forge
- bounded maintenance activity within already-approved scope
- minor implementation variations that do not affect the planning basis
- operator preference for a different approach without a material basis for
  reconsideration

---

## Primary Workflow Stages

## Stage 1 — Trigger Recognition and Classification

### Description
The ecosystem recognizes that a replanning trigger has occurred and classifies
it before any planning state changes occur.

Classification must determine:

- what triggered the reconsideration need
- whether the trigger is material enough to warrant replanning
- whether this is a maintenance matter, a return-to-planning event, or a
  deeper replanning event
- what system owns the input (V Forge findings, VEDA signal, operator direction)
- what prior governing decisions may be affected

### Responsibility
- Project V owns classification of planning-relevant triggers
- V Forge surfaces execution findings through the governed return-to-planning path
- VEDA surfaces changed signal through the governed signal interface
- Operators may surface triggers through governed operator direction

### Boundary Rule
Trigger classification must not itself constitute a planning mutation.
Recognizing that reconsideration is needed is not the same as deciding
what the reconsideration outcome will be.

---

## Stage 2 — Return-to-Planning Input Handling

### Description
When V Forge has returned bounded execution findings through the governed
return-to-planning interface, those findings are received and assessed
before any planning action occurs.

Assessment must preserve:

- what findings V Forge returned and why
- what the execution state was at time of return
- what prior planning decisions the findings affect
- what V Forge continues to own regardless of the return

### Responsibility
- Project V owns the receipt and assessment of return-to-planning inputs
- V Forge retains ownership of execution truth even after returning findings
- the return-to-planning interface governs what may cross the boundary

### Boundary Rule
Returned execution findings are inputs to planning reconsideration.
They are not automatic planning mutations.
Project V must not treat returned findings as having already rewritten
planning truth.
V Forge must not treat the return as having transferred execution ownership
back to Project V.

---

## Stage 3 — Prior Decision Context Retrieval

### Description
Before replanning begins, the relevant prior governing decisions, handoff
basis, and planning continuity context must be retrieved and understood.

This means establishing:

- what governing decisions are relevant to the reconsideration
- what the prior approval basis was for the handed-off work
- what evidence or signal supported those decisions
- what has changed since those decisions were made
- whether prior decisions should be reaffirmed, revised, superseded,
  or invalidated

### Responsibility
- Project V owns planning continuity and prior decision context
- decision-continuity-doctrine governs how prior decisions are handled

### Boundary Rule
Replanning must not reset prior decision context.
The ecosystem must know what it previously decided before it decides
what to do differently.
Treating replanning as a clean slate is not replanning — it is
decision continuity failure.

---

## Stage 4 — Replanning Scope Determination

### Description
Once trigger context and prior decision context are established, the
ecosystem must determine the bounded scope of replanning.

This includes determining:

- which prior decisions are actually affected by the trigger
- which prior decisions remain valid and should not be reopened
- what new planning decisions or revisions are required
- what execution scope implications follow from those decisions
- whether a revised handoff, new handoff, deferral, or cancellation
  is the appropriate outcome

### Responsibility
- Project V owns replanning scope determination
- operator direction may shape scope where appropriate within governance

### Boundary Rule
Replanning scope must remain bounded to what the trigger actually
requires reconsideration of.
Using a replanning event to opportunistically reopen unrelated decisions
is scope creep disguised as governance.

---

## Stage 5 — Governed Replanning

### Description
Within the determined bounded scope, Project V performs the governed
replanning work.

This may include:

- reaffirming prior decisions where they remain valid
- revising planning decisions where revision is warranted
- superseding prior decisions where a new governing direction is needed
- invalidating prior decisions where their basis is gone
- restructuring work, updating readiness evaluations, or deferring
  previously planned work
- preparing a revised handoff or new handoff where appropriate

### Responsibility
- Project V owns replanning
- approval posture requirements apply to decisions being revised,
  superseded, or invalidated
- the invalidation-and-supersedence-doctrine governs those specific actions

### Boundary Rule
Replanning decisions must follow the same approval posture required for
equivalent original decisions.
A revision to a governed decision is not less governed than the original.

When replanning scope cannot be bounded without reopening so many prior
governing decisions that the reconsideration effectively becomes a new
planning baseline, the correct response is escalation rather than replanning.
A replanning event that requires dissolving all prior governing decisions
is not replanning — it is a new planning cycle that requires human review
and governed approval before proceeding as such.

---

## Stage 6 — Replanning Outcome Preservation

### Description
Replanning outcomes must be preserved in a way that supports decision
continuity and later reconstruction.

This means:

- revised or new governing decisions are recorded explicitly
- prior decisions are marked as reaffirmed, revised, superseded, or
  invalidated as appropriate
- the connection between the trigger, the reconsideration, and the
  replanning outcome is traceable
- V Forge is informed of any scope or constraint changes through the
  governed interface

### Responsibility
- Project V owns replanning record preservation
- if a revised handoff is required, it follows the handoff workflow

### Boundary Rule
Replanning outcomes must not exist only in session memory.
A replanning event that leaves no durable trace has not produced governed
continuity — it has produced drift that looks like planning.

---

## Maintenance Activity Model

Not all post-handoff Project V activity is replanning.

Maintenance activity is the ongoing bounded planning-side work that continues
within existing approved scope without requiring replanning.

Examples of maintenance activity:

- updating bounded planning-side status as execution progresses
- reviewing and updating orchestration-side tracking within approved scope
- performing readiness re-evaluation for subsequent planned work items
- applying minor planning-side refinements that do not change governing decisions

Maintenance activity does not require:

- returning to Stage 1 trigger recognition
- retrieving prior decision context as though reconsideration is needed
- obtaining renewed approval for already-approved scope

### Rule
Maintenance must not be used to smuggle planning mutations that should
go through the replanning workflow.
If a maintenance action changes a governing decision, it is replanning,
not maintenance, regardless of how it is labeled.

---

## Return-to-Planning Interface Principle

When V Forge initiates return-to-planning, the transfer must occur
through the governed return-to-planning interface.

This principle preserves:

- V Forge's ownership of execution truth even after return
- Project V's ownership of planning truth even when receiving findings
- the bounded semantic content required for Project V to assess
  the return without absorbing execution ownership

The interface is defined in
`../interfaces/v-forge-to-project-v-return-to-planning-interface.md`.

Informal return-to-planning — where execution findings arrive outside
the governed interface — must not be treated as equivalent to a
governed return.

---

## Decision Continuity Principle

The replanning workflow must preserve decision continuity throughout.

This means:

- replanning events must reference prior governing decisions rather than
  treating them as absent
- replanning outcomes must explicitly address what happened to prior
  governing decisions
- approval-sensitive decisions that were previously required remain
  approval-sensitive when revised
- the replanning event itself must be traceable as a governed change

The decision continuity doctrine is defined in
`../governance/decision-continuity-doctrine.md`.

---

## Boundary Integrity Principle

Replanning must not blur ownership boundaries.

This means:

- V Forge execution truth remains with V Forge even when findings trigger
  replanning
- VEDA observability truth remains with VEDA even when signal triggers
  replanning
- Project V planning truth remains with Project V even when revised
  through replanning
- no system gains cross-system ownership authority from triggering a
  replanning event

Triggering reconsideration is not the same as owning planning.

---

## Evidence Continuity Principle

Evidence that triggered replanning must remain traceable.

When VEDA signal, execution findings, or external changed conditions
trigger replanning, the evidence basis for the reconsideration must
be preserved:

- what signal or findings triggered reconsideration
- what trust posture applied to that evidence
- what it demonstrated about changed conditions

The evidence continuity model is defined in
`../governance/evidence-continuity-model.md`.

When the evidence that triggered replanning is itself of uncertain trust
quality — including ambiguous execution findings, low-confidence VEDA signal,
or contested external conditions — the replanning scope determination at
Stage 4 must account for that uncertainty.
Weak triggering evidence may justify a narrower reconsideration scope, a
request for better evidence before proceeding, or escalation rather than
full replanning.
The trust posture of the triggering evidence must not be ignored when
determining whether and how broadly to replan.

---

## Human-In-The-Loop Principle

Replanning is governance-sensitive because it changes what the ecosystem
will do next.

Human review may be required when:

- replanning involves superseding or invalidating prior governing decisions
- replanning involves significant scope change or priority shift
- replanning involves revised handoff activation
- replanning affects cross-system interfaces or approval posture
- the trigger for replanning involves external paid actions or evidence

The approval and escalation posture is defined in
`../governance/approval-and-escalation-model.md`.

---

## Failure and Interruption Principle

When the replanning workflow cannot legitimately progress — including when
decision context cannot be established, when prior decisions are in conflict,
or when required approval is not available — the interruption must remain
explicit rather than being smoothed over by assumption.

Failure handling should remain consistent with
`../governance/failure-and-recovery-doctrine.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- return-to-planning inputs are not automatic planning mutations
- replanning requires prior decision context before scope is determined
- replanning scope must be bounded to what the trigger requires
- maintenance activity within approved scope is not replanning
- V Forge retains execution truth even when returning findings
- replanning outcomes must be durably preserved
- decision continuity is not reset by a replanning event

If a replanning event results in the ecosystem operating as though prior
governing decisions never existed, the workflow has failed.

---

## Usage

This document should be used:

- when deciding whether a situation warrants replanning or only maintenance
- when receiving return-to-planning inputs from V Forge
- when determining the bounded scope of reconsideration
- when reviewing whether replanning preserved decision continuity
- when evaluating whether a replanning outcome was durably recorded
- when writing more specific Project V, V Forge, or launch-readiness
  workflow docs

---

## Related Docs

- `handoff-workflow.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../project-v/operational-workflow.md`
- `../project-v/v-forge-integration.md`
- `../v-forge/operational-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/invalidation-and-supersedence-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../ecosystem/cross-system-boundaries.md`
- `launch-readiness-workflow.md`
