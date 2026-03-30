# Launch Readiness Workflow

## Purpose

This document defines the cross-system workflow by which the V Ecosystem
confirms that a project or execution scope is ready for launch-sensitive,
public-facing, or external-visible action.

It exists to answer:

```text
What must be confirmed before launch-sensitive or public-facing execution
proceeds, what systems are responsible at each stage, and what prevents
the ecosystem from treating internal readiness as launch authorization?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the workflow by which launch readiness is evaluated and confirmed
  before launch-sensitive execution proceeds
- the stages of launch readiness assessment from planning through
  pre-launch verification to authorized launch activation
- the responsibility boundaries between Project V, VEDA, V Forge,
  and governance at each stage
- what makes a launch-ready state genuine rather than assumed
- what must stop the workflow when launch readiness cannot be confirmed

---

## Out of Scope

This document does not define:

- the detailed execution mechanics of specific launch types
- vendor-specific publication or distribution workflows
- detailed campaign or content publishing mechanics
- the post-launch observation workflow
- every project-specific launch variant

Those belong in V Forge docs, interface docs, and project-specific docs.

---

## System

- workflows

---

## Core Rule

Launch-sensitive execution must not proceed on the basis of internal
confidence alone.

Launch readiness is a specific governance state that must be explicitly
confirmed across planning, evidence, and execution dimensions before any
public-facing, external-visible, or spend-creating launch action occurs.

Internal readiness is not launch authorization.
Execution capability is not launch authorization.
Prior successful launches are not launch authorization for the current scope.

---

## Launch-Sensitive Action Definition

A launch-sensitive action is any action that:

- creates or changes externally visible content, products, or services
- initiates public-facing distribution, publication, or communication
- activates paid spend or billable external activity at launch scale
- creates launch-visible changes that are difficult or impossible to reverse
- commits the ecosystem to external-facing obligations or representations

Launch-sensitive actions require stronger governance than internal execution
because their consequences extend beyond the ecosystem boundary and may be
hard to recover from.

---

## Workflow Preconditions

The launch readiness workflow should begin only when:

- execution is approaching a scope that involves launch-sensitive action
- V Forge has reached a state where launch-sensitive execution is the
  next governed step within the approved handoff scope
- planning-side launch readiness basis has been established in Project V
- the ecosystem has sufficient signal and evidence from VEDA to support
  an honest launch readiness assessment

The workflow must not be bypassed because:

- the work looks complete internally
- the timeline is pressing
- a prior version was launched without issue
- the operator believes it is ready
- the execution scope is small enough to seem low-risk

---

## Primary Workflow Stages

## Stage 1 — Planning-Side Launch Readiness Assessment

### Description
Project V confirms that the planning basis supports launch-readiness
determination for the relevant scope.

This includes confirming:

- what scope is being evaluated for launch readiness
- what governing decisions support launching this scope now
- what approval posture applies to the specific launch-sensitive actions
- what evidence or signal from VEDA informed the planning-side readiness basis
- what constraints or conditions apply to the launch
- what would block or defer launch from the planning perspective

### Responsibility
- Project V owns the planning-side launch readiness assessment

### Boundary Rule
Planning-side launch readiness is a planning determination.
It is not execution authorization.
Project V confirming planning readiness does not authorize V Forge to
begin launch-sensitive execution without the remaining stages being satisfied.

---

## Stage 2 — Evidence and Signal Review

### Description
The ecosystem reviews whether VEDA signal and evidence support the
planned launch scope and timing.

This includes reviewing:

- whether current signal supports the planned launch scope
- whether evidence quality and freshness are sufficient for an honest
  launch readiness determination
- whether any recently surfaced signal contradicts the planning basis
- whether the evidence trust posture is adequate for launch-sensitive
  decision-making

### Responsibility
- VEDA owns the signal and evidence that inform this review
- Project V interprets signal for planning-side launch readiness purposes
- the review follows the governed signal interface

For launch-sensitive decisions, evidence is current enough when it reflects
conditions that existed close enough to the launch timing that material
conditions are unlikely to have changed in ways that would affect the launch
readiness determination.
The materiality standard from `../governance/evidence-continuity-model.md`
applies, but must be applied conservatively for launch-sensitive decisions —
because the cost of proceeding on stale evidence at launch is higher than
in ordinary planning contexts.

### Boundary Rule
VEDA signal review informs launch readiness determination.
It does not itself constitute launch authorization.
Signal confirming a favorable condition is not the same as approval
to launch.
VEDA does not make launch decisions — it provides the evidential basis
on which launch decisions are made.

---

## Stage 3 — Execution-Side Pre-Launch Verification

### Description
V Forge confirms that execution is prepared to carry out the launch-sensitive
scope within the approved constraints.

This includes confirming:

- what execution work is complete and ready for launch activation
- what execution work remains incomplete or unverified
- whether the execution scope matches what was handed off and approved
- whether any mid-execution findings have emerged that affect launch readiness
- whether external action preconditions are satisfied for launch-sensitive steps

This stage applies the pre-action verification obligations from
`../governance/testing-and-verification-doctrine.md`, including:

- Class V1 precondition verification for launch-sensitive actions
- Class V4 external action and approval verification where applicable
- Class V5 outcome verification for any execution work already completed

### Responsibility
- V Forge owns execution-side pre-launch verification
- verification results are surfaced through governed reporting

### Boundary Rule
V Forge pre-launch verification is an execution-side assessment.
If verification cannot be completed at the level required — because
conditions are unclear, verification tooling is unavailable, or execution
findings are ambiguous — the correct response is to surface that gap
explicitly rather than proceeding as though verification passed.

---

## Stage 4 — Cross-System Launch Readiness Confirmation

### Description
The ecosystem confirms that planning-side readiness, evidence support,
and execution-side verification are all satisfied before launch
authorization is sought.

This cross-system confirmation must establish:

- planning-side launch readiness basis is present and current
- evidence and signal support the planned launch scope
- execution-side verification is complete at the required level
- no unresolved cross-system gap exists that would make launch unsafe
- the launch scope has not silently widened beyond what was assessed

### Responsibility
- Project V synthesizes the cross-system readiness picture
- V Forge surfaces execution-side verification status
- VEDA provides evidence currency confirmation where needed

### Boundary Rule
Cross-system launch readiness confirmation must not be produced by
any single system in isolation.
A self-certification of cross-system readiness by V Forge or by
Project V alone is not a governed cross-system confirmation.

---

## Stage 5 — Launch Authorization

### Description
The required approval posture for the specific launch-sensitive actions
is satisfied before execution proceeds.

This requires:

- identifying the specific approval required for the launch class
- confirming the approving actor has the required authority
- confirming approval covers the current scope, not merely the general
  launch category
- confirming no conditions have materially changed since the basis
  for approval was established

### Responsibility
- the approval and escalation model governs what approval is required
- human actors with the required authority must provide approval where
  doctrine requires it
- V Forge must not self-authorize launch-sensitive action

### Boundary Rule
Launch authorization is a governed approval event.
An operator expressing confidence that a launch is ready is not governed
approval unless the required approval posture has been satisfied.
An agent recommending launch is not launch authorization.
The approval and escalation posture is defined in
`../governance/approval-and-escalation-model.md`.

---

## Stage 6 — Launch Activation and Execution

### Description
With cross-system readiness confirmed and launch authorization in place,
V Forge proceeds with the launch-sensitive execution within the approved
scope and constraints.

During launch-sensitive execution, V Forge must:

- remain within the approved launch scope
- halt at the earliest safe stopping point if conditions change materially
- preserve a reviewable record of what actions were taken
- surface unexpected conditions through governed reporting rather than
  improvising around them

### Responsibility
- V Forge owns launch-sensitive execution
- Project V retains planning truth
- VEDA retains observability truth

### Boundary Rule
Launch authorization does not transfer planning ownership to V Forge.
Launch execution does not transfer observability ownership to V Forge.
If launch-sensitive execution produces findings that require planning
reconsideration, the maintenance and replanning workflow applies.

---

## Stage 7 — Post-Launch State

### Description
After launch-sensitive execution completes successfully within the confirmed scope,
the ecosystem enters the post-launch state.

The post-launch state must be explicitly established. It does not occur by
implication or by the absence of failure.

Entering the post-launch state means:

- V Forge execution truth now includes the launched scope
- V Forge continues to hold execution-side ownership for the launched work
- VEDA's ongoing observatory role resumes for the launched scope,
  observing search performance, traffic behavior, indexation state, and
  other relevant external signals for the live project
- Project V retains planning truth and may initiate replanning if
  post-launch findings require it
- The post-launch observation phase begins and is governed by
  `post-launch-observation-workflow.md`

The post-launch state is not a terminal state.
It is the beginning of ongoing observation and the natural re-entry point
for the maintenance and replanning workflow when post-launch conditions require reconsideration.

### Responsibility
- V Forge retains execution truth for the launched scope
- VEDA resumes observatory observation for the launched scope
- Project V retains planning truth and monitors for conditions that
  trigger return-to-planning through the governed maintenance and replanning path
- governance and reporting requirements continue during post-launch observation

### Boundary Rule
Entering the post-launch state does not transfer planning ownership to V Forge.
It does not transfer observatory ownership to V Forge.
It does not dissolve governance boundaries.

Post-launch findings that require planning reconsideration enter the maintenance
and replanning workflow through the governed return-to-planning path.
Post-launch findings that can be resolved within approved scope are handled
through maintenance activity, not replanning.

The distinction between maintenance, return-to-planning, and replanning that
applies before launch also applies after launch.

---

## Launch Readiness Blocking Conditions

The launch readiness workflow must stop and must not proceed to
authorization when:

- planning-side launch readiness cannot be confirmed
- evidence or signal quality is insufficient for honest launch
  readiness determination
- execution-side verification cannot be completed at the required level
- a cross-system gap exists that has not been resolved
- the launch scope has silently widened beyond what was assessed
- required approval authority is unclear or unavailable
- V Forge has surfaced unresolved execution findings that affect
  launch safety

### Rule
A blocked launch readiness workflow must not be resolved by proceeding
anyway.
The block must be surfaced explicitly and resolved through the governed
path — which may include deferral, replanning, additional verification,
or escalation.

When a blocked launch readiness workflow is later cleared and the workflow
resumes, any stage assessments that have become materially stale during
the blocking period must be refreshed before proceeding to authorization.
A block that resolves after a significant time gap does not carry forward
prior stage assessments as still current.
Stages 1 and 2 in particular are time-sensitive and must be re-confirmed
if material time has passed or conditions have changed since they were
completed.

---

## Scope Integrity Principle

Launch readiness must be assessed for the actual launch scope, not for
a simpler version of it.

If the launch scope has grown beyond what was originally assessed:

- the assessment must cover the full current scope
- prior readiness determinations for a narrower scope do not carry over
- the additional scope requires its own readiness assessment
- authorization must cover the full current scope

A launch scope that expands incrementally does not accumulate prior
readiness determinations into a combined readiness state.

---

## Evidence Currency Principle

Evidence used to support launch readiness determination must be current
enough to be honest.

Stale evidence that supported a prior readiness determination does not
automatically support the current one.

When the evidence basis for launch readiness has become materially stale
since the planning-side assessment was made, the evidence review at
Stage 2 must be refreshed before proceeding to authorization.

The evidence continuity model is defined in
`../governance/evidence-continuity-model.md`.

---

## External Action Principle

Launch-sensitive actions that involve external-facing execution are
governed by the external action doctrine as well as this workflow.

This workflow establishes readiness.
The external action governance model governs the specific preconditions
and controls for the external actions themselves.

Both must be satisfied.

The external action governance model is defined in
`../governance/external-action-governance.md`.

---

## Human-In-The-Loop Principle

Launch readiness is governance-sensitive because launch-sensitive execution
creates consequences that extend beyond the ecosystem boundary.

Human review or approval is required for:

- launch authorization for any public-facing or external-visible action
- launch scope that involves paid spend at launch scale
- launch activation that is difficult or impossible to reverse
- launch that creates reputational, contractual, or compliance obligations

An agent may support launch readiness assessment.
An agent must not self-authorize launch-sensitive action.

---

## Failure and Interruption Principle

When launch-sensitive execution must stop after it has begun — due to
unexpected conditions, scope excess, authorization questions, or
execution-side findings — the interruption must remain explicit.

V Forge must halt at the earliest safe stopping point, preserve the
current execution state, and surface the interruption through the
governed reporting and escalation path.

A mid-launch interruption must not be resolved through improvisation.

Failure handling is governed by `../governance/failure-and-recovery-doctrine.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- launch readiness is a multi-stage cross-system confirmation, not a
  single-system assessment
- internal readiness is not launch authorization
- evidence currency must be confirmed, not assumed, at launch time
- execution-side verification must be complete before launch authorization
  is sought
- approval for launch must cover the actual current scope
- a blocked launch readiness workflow must be resolved explicitly,
  not bypassed

If an LLM treats operator confidence, internal completion, or prior
launch success as sufficient authorization for the current launch,
this doctrine is failing.

---

## Usage

This document should be used:

- when approaching a scope where launch-sensitive execution is the next step
- when confirming that planning, evidence, and execution dimensions
  of readiness are all satisfied before launch authorization is sought
- when deciding whether a launch readiness gap blocks authorization
- when reviewing whether launch activation stayed within confirmed scope
- when writing V Forge, Project V, or project-specific docs that involve
  launch-sensitive workflows

---

## Related Docs

- `handoff-workflow.md`
- `maintenance-and-replanning-workflow.md`
- `post-launch-observation-workflow.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
- `../governance/testing-and-verification-doctrine.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/operational-workflow.md`
- `../v-forge/operational-model.md`
