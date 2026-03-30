# Post-Launch Observation Workflow

## Purpose

This document defines the cross-system workflow by which the V Ecosystem
observes, evaluates, and responds to what happens after a project has launched.

It exists to answer:

```text
How does the ecosystem move from active launch into ongoing observation,
what does VEDA observe once a project is live, how do Project V and V Forge
use those observations, and what triggers the transition from observation
into maintenance or replanning?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the workflow by which the ecosystem enters and sustains the post-launch
  observation phase
- what VEDA observes once a project scope is live
- how Project V and V Forge consume post-launch observatory signal
- how post-launch findings are classified as maintenance, return-to-planning,
  or non-actionable noise
- what conditions trigger the transition from observation into maintenance
  or replanning
- the boundary posture operators and LLMs must preserve during post-launch
  observation

---

## Out of Scope

This document does not define:

- the detailed execution mechanics of maintenance work within V Forge
- the detailed Project V replanning workflow steps
- the detailed VEDA provider or ingest mechanics for specific signal sources
- post-launch campaign, paid media, or distribution management specifics
- every project-specific post-launch variant

Those belong in V Forge docs, Project V docs, VEDA docs, and project-specific docs.

---

## System

- workflows

---

## Core Rule

Post-launch observation is a continuous governed phase, not a single event.

After a project launches, VEDA continues to observe external reality as it
relates to the live scope. Project V and V Forge receive those observations
through governed interfaces and classify them. Observations that warrant
action enter the maintenance and replanning workflow through governed paths.
Observations that do not warrant action are preserved and may inform later
reconsideration.

The ecosystem must not treat the post-launch phase as an ungoverned quiet
period where observation is informal and findings are ignored.
The ecosystem must also not treat every post-launch signal as automatic
authorization to replan or re-execute.

Observation and action are distinct. Both must be governed.

---

## Entry Condition

This workflow begins from the post-launch state established in Stage 7 of
`launch-readiness-workflow.md`.

That state requires:

- V Forge has completed launch-sensitive execution within confirmed scope
- V Forge execution truth now includes the launched scope
- VEDA's observatory role has resumed for the launched scope
- Project V retains planning truth for the launched work
- no active replanning or mid-launch interruption has returned the ecosystem
  to the maintenance and replanning workflow

If the ecosystem re-enters this workflow after a replanning cycle, the
entry condition is that governed replanning has completed and revised
execution (if any) has concluded, returning the launched scope to a stable
observed state.

---

## Primary Workflow Stages

## Stage 1 — Observatory Scope Activation

### Description
VEDA activates or confirms its observatory scope for the launched project.

This means VEDA establishes or updates what it is watching for the live scope,
including:

- search performance signals for the launched content
- indexation and crawl state from Search Console
- keyword ranking behavior relevant to the launched scope
- traffic and engagement signals from GA4
- SERP volatility or intent drift for the target topic cluster
- any YouTube or platform signals relevant to the launched scope

### Responsibility
- VEDA owns observatory scope activation for the launched project
- the operator or Project V may direct VEDA to prioritize specific signal
  types or monitoring targets relevant to the launched scope
- the MCP coordination model governs how observatory scope is configured

### Boundary Rule
Observatory scope activation does not give VEDA planning authority.
VEDA is identifying what to watch and recording observations.
It is not deciding what the observations mean for the project or what to do next.
That interpretation belongs to Project V and V Forge.

---

## Stage 2 — Initial Post-Launch Signal Capture

### Description
VEDA captures initial post-launch signal for the launched scope and
packages it for ecosystem consumption through the governed signal interface.

This includes capturing:

- initial indexation signals — whether the launched content is being found
  and crawled as expected
- early search performance signals — impressions, clicks, position where
  available and meaningful
- early traffic behavior from GA4 where applicable
- SERP context for the target topic cluster — what competitors are doing
  in the same space immediately post-launch

The initial post-launch capture window is the period shortly after launch
where indexation state, crawl behavior, and early performance signals
provide the first honest read on launch health.

### Responsibility
- VEDA owns signal capture
- the observatory event log preserves the capture record with provenance
  and freshness context

### Boundary Rule
Initial signal is not yet a finding about performance.
It is early evidence that requires interpretation.
Low initial signal does not automatically mean the launch failed.
Strong initial signal does not automatically confirm long-term success.

VEDA captures what it sees. It does not interpret the implications
for planning or execution.

---

## Stage 3 — Post-Launch Signal Classification

### Description
Project V and V Forge receive post-launch signal from VEDA through the
governed signal interfaces and classify what the signal means.

Classification must determine:

- whether the signal indicates the launch is performing as expected
- whether there are early signs of an indexation, crawl, or performance problem
- whether observations are within the range of expected early-phase variation
- whether any signal is strong enough to warrant immediate action
- whether the signal requires a waiting period before it can be meaningfully
  interpreted (many post-launch signals require weeks to stabilize)

### Responsibility
- Project V interprets signal for planning-side implications
- V Forge interprets signal for execution-side implications
- the classification must distinguish signal that warrants action from
  signal that should continue to be observed

### Boundary Rule
Signal classification is not the same as a replanning decision.
Classifying that a signal looks concerning is not authorization to replan.
Classifying that a signal looks healthy is not confirmation that no future
reconsideration will be needed.

Classification produces a bounded interpretation.
It does not produce a mandate to act.

---

## Stage 4 — Ongoing Observatory Monitoring

### Description
VEDA continues to observe the live scope over time, capturing signals
at appropriate intervals as conditions evolve.

Ongoing monitoring includes:

- periodic keyword ranking and SERP position tracking
- traffic and engagement trend monitoring from GA4
- Search Console performance and coverage monitoring
- indexation health over time — detecting drops, crawl anomalies,
  or coverage changes
- intent drift detection — whether the queries the launched content
  targets are changing in ways that affect the launch's relevance
- competitive SERP change detection — whether incumbent content or
  new entrants are displacing the launched scope

### Responsibility
- VEDA owns ongoing observatory monitoring for the launched scope
- monitoring cadence and focus may be adjusted by operator direction
  within governed observatory scope bounds

### Boundary Rule
Ongoing monitoring is not continuous replanning authorization.
VEDA watches and records. The observations feed classification cycles.
Classification cycles may eventually trigger the maintenance or replanning
workflow. That trigger must be explicit, not implicit from monitoring volume.

---

## Stage 5 — Signal Review and Reconsideration Assessment

### Description
At governed intervals or when a materially significant signal event occurs,
Project V and V Forge conduct a structured review of post-launch observatory
signal to assess whether any reconsideration is warranted.

This review must determine:

- whether observed trends confirm, question, or contradict the planning
  basis for the launched work
- whether V Forge execution truth remains consistent with what was planned
- whether any signal is strong enough and reliable enough to warrant entering
  the maintenance and replanning workflow
- whether the evidence quality and trust posture of the signal supports
  a reconsideration conclusion or whether more observation time is needed

The review may conclude:

- continue observation — current signal does not warrant action
- enter maintenance — bounded work within existing scope can address the finding
- enter return-to-planning — the finding affects the planning basis and
  requires the maintenance and replanning workflow
- escalate — a signal event is significant enough or uncertain enough to
  require human review before classification

### Responsibility
- Project V owns planning-side reconsideration assessment
- V Forge owns execution-side reconsideration assessment
- the classification follows the trigger conditions defined in
  `maintenance-and-replanning-workflow.md`

### Boundary Rule
A reconsideration assessment must remain a classification exercise,
not a premature planning mutation.

The assessment determines which governed path is appropriate.
It does not itself constitute a replanning decision, a maintenance authorization,
or an execution instruction.

---

## Stage 6 — Governed Path Activation

### Description
When the reconsideration assessment concludes that action is warranted,
the ecosystem activates the appropriate governed path.

### Outcome: Continue Observation
No material trigger has been met. The ecosystem records that the review
occurred, captures the current interpretation of post-launch signal,
and continues Stage 4 monitoring.

### Outcome: Maintenance
Bounded work within existing approved scope can address the finding.
This follows the maintenance activity model defined in
`maintenance-and-replanning-workflow.md` — no replanning is required,
and the work can proceed within the already-approved scope.

### Outcome: Return-to-Planning
The finding materially affects the planning basis. The ecosystem enters
Stage 1 of `maintenance-and-replanning-workflow.md` through the governed
return-to-planning path. V Forge surfaces the relevant execution findings
through the governed return-to-planning interface where applicable.

### Outcome: Escalation
The signal event is significant enough, ambiguous enough, or governance-sensitive
enough to require human review before the correct path can be determined.
The escalation follows the escalation model defined in
`../governance/approval-and-escalation-model.md`.

### Responsibility
- Project V activates the appropriate planning-side path
- V Forge activates the appropriate execution-side path
- the governed interface is used for return-to-planning transfers

### Boundary Rule
Activating a governed path does not skip the workflow defined in that path.
Entering the maintenance and replanning workflow means following its stages.
Activating maintenance means following maintenance activity constraints.
Neither entry is shortcut authorization to act freely.

---

## Observation Continuity Principle

Post-launch observations must be preserved in a way that supports later
reconsideration, review, and reconstruction.

This means:

- observatory event records must remain traceable with provenance and
  timestamp even when they do not immediately trigger action
- signal that was assessed as "continue observation" must remain accessible
  as context when a later signal event triggers reconsideration
- the history of what was observed, when, and at what confidence level
  must not be discarded because it seemed unactionable at the time

Evidence continuity during the post-launch observation phase is governed by
`../governance/evidence-continuity-model.md`.

An observation that is inconclusive today may become part of the
evidence basis for a governing decision six weeks later.
Its provenance must be preserved accordingly.

---

## Signal Patience Principle

Many post-launch signals require time to stabilize before they can be
meaningfully interpreted.

Search performance signals in particular often require weeks to reflect
indexation, ranking, and traffic behavior that represents the actual
steady-state response to the launched content.

This means:

- early weak signal should not automatically trigger replanning
- early strong signal should not automatically confirm success and
  suspend further monitoring
- the classification at Stage 3 and Stage 5 must account for the
  expected maturation window for the relevant signal type
- acting on pre-maturity signal produces governance noise and
  wastes planning and execution capacity

### Rule
When signal has not yet matured to a reliably interpretable state,
"continue observation" is the correct governed outcome.
Impatience with slow signal is not a trigger for replanning.

---

## Noise vs. Signal Principle

Not every post-launch fluctuation is an actionable finding.

The ecosystem must distinguish:

- material signal — a trend, event, or pattern strong enough and consistent
  enough to support a governed reconsideration conclusion
- observation noise — natural variation in signal that does not reflect
  a meaningful change in external conditions

### Rule
An observation is noise until there is enough evidence to classify it otherwise.
Noise must not be treated as a replanning trigger.
Accumulating noise does not become material signal through volume alone.

When the boundary between noise and signal is genuinely uncertain, that
uncertainty must be surfaced explicitly rather than resolved by assumption.
The correct governed outcome for uncertain signal is continued observation
or escalation, not premature action.

---

## VEDA Boundary Principle

VEDA observes and records what the external world is doing in relation to
the launched scope.

VEDA does not:

- determine whether the launch was successful at a business level
- decide whether replanning is warranted
- propose execution changes
- model what V Forge has built as a substitute for the content graph

These interpretations belong to Project V and V Forge, who cross VEDA's
observatory signal against their own planning truth and execution truth
to produce the reconsideration assessment.

The telescope mental model applies throughout the post-launch observation phase.
VEDA watches and records. Interpretation and action happen elsewhere.

---

## Human-In-The-Loop Principle

Post-launch observation is governance-sensitive because its findings may
affect ongoing planning, execution scope, and resource allocation.

Human review may be required when:

- a signal event is significant enough to suggest a major replanning event
  is warranted
- a reconsideration assessment concludes that escalation is the correct path
- the signal quality or trust posture is too uncertain to support a
  classification conclusion without human review
- a maintenance or return-to-planning activation involves significant scope
  or spend implications
- the post-launch observation reveals conditions that affect other projects
  in the portfolio

An agent may support signal classification and reconsideration assessment.
An agent must not self-authorize replanning, scope changes, or external action
based on post-launch signal alone.

---

## Failure and Interruption Principle

When post-launch observation reveals a material failure — a significant
indexation problem, a launch-damaging external event, or an unexpected
consequence of the launched work — the ecosystem must handle it as a
governed failure, not as background noise.

Material failures during the post-launch observation phase must:

- be surfaced explicitly through the governed reporting path
- be classified for their planning and execution implications
- trigger the appropriate governed path (maintenance, return-to-planning,
  or escalation) without delay
- not be left in a "watching and hoping" state that treats severity as
  a reason to avoid governance

Failure handling during post-launch observation is governed by
`../governance/failure-and-recovery-doctrine.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- post-launch observation is a continuous governed phase, not a passive
  quiet period
- VEDA observes and records; Project V and V Forge interpret and classify
- signal classification must account for signal maturity before drawing
  reconsideration conclusions
- noise and material signal are distinct and must not be conflated
- "continue observation" is a valid and often correct governed outcome
- action requires a governed path activation, not an informal finding

If an LLM treats every post-launch signal fluctuation as a replanning
authorization, or treats the post-launch phase as governance-free,
this doctrine is failing.

---

## Usage

This document should be used:

- when establishing the observatory scope for a newly launched project scope
- when evaluating post-launch signal to determine whether action is warranted
- when classifying post-launch findings as maintenance, return-to-planning,
  escalation, or continue-observation outcomes
- when reviewing whether the ecosystem is acting too quickly or too slowly
  on post-launch signal
- when writing V Forge, VEDA, or Project V docs related to post-launch behavior

---

## Related Docs

- `launch-readiness-workflow.md`
- `maintenance-and-replanning-workflow.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/evidence-continuity-model.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../veda/veda.md`
- `../veda/system-invariants.md`
- `../project-v/operational-workflow.md`
- `../v-forge/operational-model.md`
- `../ecosystem/cross-system-boundaries.md`
