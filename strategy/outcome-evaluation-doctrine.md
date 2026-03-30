# Outcome Evaluation Doctrine

## Purpose

This document defines how project outcomes are evaluated inside the V Ecosystem.

It exists to answer:

```text
How does the ecosystem assess whether a project succeeded, what evidence is used,
when evaluation should occur, and how evaluation outcomes affect planning,
replanning, investment, and future intake decisions?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what outcome evaluation means inside the V Ecosystem
- when evaluation should occur and at what cadence
- what evidence is used for evaluation
- how evaluation relates to the project thesis
- what evaluation outcomes may trigger
- how evaluation connects to the reinvestment and intake cycle
- the anti-drift rules that prevent evaluation from becoming theater

---

## Out of Scope

This document does not define:

- specific metric thresholds or targets for every project type
- the detailed VEDA signal capture mechanics for evaluation evidence
- the detailed Project V replanning workflow steps
- post-launch observation workflow mechanics

Those belong in the post-launch observation workflow, VEDA docs, Project V docs,
and project-specific evaluation docs.

---

## System

- strategy

---

## Core Rule

Outcome evaluation is the governed practice of honestly assessing whether a project
is performing in the direction the thesis predicted, using traceable evidence,
and using that assessment to produce a governed outcome that affects planning.

Evaluation must be honest. A project that is underperforming must not be assessed
as performing because the team is attached to the work.
A project that is performing must not be assessed as failing because new opportunities
have emerged that seem more attractive.

Evaluation is not a ritual. It is a governed input into the planning cycle.

---

## Relationship to Project Thesis

The project thesis is the governing reference for evaluation.

Evaluation asks:
- Is the project moving toward the target outcome stated in the thesis?
- Is the evidence basis that supported the thesis still valid?
- Have the failure or revision conditions identified in the thesis been met?

An evaluation that ignores the thesis is not a governed evaluation.
A project cannot be assessed as succeeding if it is not moving toward what its
thesis said success looked like.

If the thesis was vague, the evaluation will be vague.
This is why thesis quality matters before execution begins.

---

## Relationship to Post-Launch Observation

Post-launch observation is the continuous governed phase in which VEDA observes
external signals and Project V and V Forge classify whether those signals warrant action.

Outcome evaluation is a distinct but related practice:

- post-launch observation is ongoing and signal-driven
- outcome evaluation is periodic and thesis-anchored

Outcome evaluation draws on the record of post-launch observations as its primary
evidence input. It synthesizes that evidence against the thesis to produce a
governing assessment.

The post-launch observation workflow is defined in:
`../workflows/post-launch-observation-workflow.md`

---

## Evaluation Timing

Outcome evaluation should occur at three points.

### 1. Early-Phase Evaluation
Occurs after the initial post-launch signal has had time to stabilize — typically
after a meaningful period of indexation and search signal maturation.

Purpose: assess whether the launch is progressing in the expected direction.
This evaluation does not require that the project has reached full performance.
It assesses whether early signals are consistent with the thesis trajectory.

### 2. Performance-Phase Evaluation
Occurs once the project has had sufficient time to establish a stable performance pattern.

Purpose: assess whether the project is achieving what the thesis predicted.
This is the primary evaluation against the thesis target outcome.

### 3. Maintenance-Phase Evaluation
Occurs periodically while the project remains in active maintenance.

Purpose: assess whether the project continues to justify ongoing maintenance investment,
whether the thesis still reflects current conditions, and whether the project is at
risk of decay or decline.

---

## Evidence Standard

Evaluation must use traceable, VEDA-sourced observatory evidence wherever possible.

Acceptable evidence for evaluation:

- Search Console performance data showing impressions, clicks, and position trends
- GA4 traffic data showing audience behavior on the launched content
- keyword ranking data showing position movement for target queries
- SERP observation data showing competitive position changes
- indexation and coverage data showing whether the content is being found and indexed

Evidence quality posture:
- freshness matters — stale evidence from months prior does not support a current evaluation
- trend context matters — a single data point is weaker than a directional trend
- provenance matters — evidence should be attributable to its VEDA source record

Unacceptable substitutes for evaluation evidence:
- intuition or general sentiment about how the project feels
- anecdotal feedback without observatory grounding
- comparison to other projects without controlling for relevant factors
- assertion of success or failure without traceable signal

---

## Evaluation Outcomes

An outcome evaluation must produce one of the following governed outcomes.

### Performing — Continue
The project is moving toward the thesis target outcome and no material revision
is warranted. Continue post-launch observation and maintenance as appropriate.

### Performing — Expand
The project is performing well and evidence supports expanding the scope —
through additional content, extended topic clusters, or related opportunities.
Expansion is not automatic from a positive evaluation. It requires the same
intake and thesis process as a new project unless the expansion is clearly
within the existing thesis scope.

### Underperforming — Watch
Early signals are weak but it is too early to draw a conclusion. Continue
observation with a defined next evaluation point. Record what would trigger
a more decisive outcome at the next evaluation.

### Underperforming — Investigate
Signals are persistently weak or negative and the cause is unclear. Initiate
bounded investigation: classify whether the underperformance is execution-side
(content quality, structure, technical issues) or market-side (demand changed,
competition strengthened, intent shifted). Do not replan until the cause is clear.

### Underperforming — Replan
Evidence is sufficient to conclude the project needs a planning-level intervention.
This triggers the maintenance and replanning workflow. The replanning scope
must be bounded to what the evaluation actually identified — not a wholesale
restart of the project.

### Thesis Revision Required
The evaluation reveals that the thesis no longer reflects current conditions —
because market signal has shifted, the evidence basis has changed, or the target
outcome as stated is no longer achievable. The thesis must be explicitly revised
before replanning proceeds.

### Archive
The project no longer justifies continued maintenance investment. Performance
is consistently below the threshold where ongoing work produces meaningful return.
Archival is a governed lifecycle outcome, not an abandonment. The project record,
thesis, and evaluation history are preserved.

---

## Evaluation Outcome Is Not Automatic Action

An evaluation outcome is a governing input into the planning cycle.

- "Replan" means enter the maintenance and replanning workflow, not immediately change the project
- "Expand" means initiate an intake evaluation for the expansion, not immediately execute more content
- "Archive" means record the governed archive decision, not delete the project record

Every evaluation outcome that requires planning action flows through the relevant
governed workflow, not through direct execution.

---

## Reinvestment Connection

The V Ecosystem's longer-term goal is a compounding reinvestment loop:
performing projects generate return, return funds new project investment,
new projects generate more return.

Outcome evaluation is the governed checkpoint that feeds that loop honestly:

- performing projects with strong evidence justify continued investment
- performing projects that reveal adjacent opportunities inform new intake
- underperforming projects prevent misallocation of execution capacity
- archived projects free capacity for higher-return opportunities

An evaluation system that consistently rates projects as performing regardless
of evidence breaks the reinvestment loop by misdirecting capacity.

---

## Evaluation Record Requirement

Every outcome evaluation must be preserved as a reviewable record.

At minimum, an evaluation record must contain:

- which project was evaluated
- which evaluation phase this represents (early, performance, maintenance)
- what evidence was used and its freshness context
- what the evaluation concluded against each thesis element
- what governed outcome was produced
- what the next evaluation point is or what triggered transition to a different outcome

An evaluation that exists only in session memory or conversational output is not
a governed evaluation record. It must be durably preserved through the project's
planning record.

---

## Anti-Drift Rules

Evaluation has drifted when:

- outcomes are assessed against a vague or forgotten thesis rather than the actual governing statement
- evidence is substituted by intuition or attachment to the project
- underperformance is relabeled as "early stage" indefinitely without a defined next evaluation point
- expansion is initiated without a clear evidence basis or thesis scope connection
- archive decisions are avoided indefinitely because no one wants to make them
- evaluation records are not preserved and cannot be recovered in later sessions

These failures do not make evaluation more encouraging — they make the ecosystem's
planning less honest and its reinvestment loop less effective.

---

## Human-In-The-Loop Principle

Outcome evaluation is governance-sensitive because it affects how the ecosystem
allocates its planning and execution capacity.

Human review is appropriate when:

- an evaluation outcome would trigger major replanning with significant scope or spend implications
- thesis revision is identified and requires deliberate human judgment about the project's future
- archive is the conclusion and the decision to close a project carries meaningful consequence
- the evidence basis is genuinely ambiguous and a human judgment call is required

An agent may support evaluation by synthesizing VEDA signal, referencing the thesis,
and packaging a draft evaluation for review. An agent must not self-authorize
governed evaluation outcomes that trigger planning changes.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- evaluation is anchored to the thesis, not to the agent's general impression of the project
- evaluation uses traceable observatory evidence, not intuition
- evaluation outcomes are governed inputs, not authorizations to act
- evaluation records must be durable, not session-local
- a project that is consistently assessed as performing without traceable evidence
  is not being evaluated — it is being protected from evaluation

If evaluation produces the same positive outcome regardless of evidence, this
doctrine is failing.

---

## Usage

This document should be used:

- when conducting an early-phase, performance-phase, or maintenance-phase evaluation
- when determining what evidence is needed for an honest evaluation
- when classifying an evaluation outcome and determining what governed path it triggers
- when reviewing whether past evaluations were grounded in evidence or in intuition
- when connecting evaluation outcomes to the intake and reinvestment cycle

---

## Related Docs

- `project-thesis-model.md`
- `ecosystem-objective-function.md`
- `opportunity-scoring-model.md`
- `../workflows/post-launch-observation-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../workflows/project-intake-workflow.md`
- `../governance/evidence-continuity-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/invalidation-and-supersedence-doctrine.md`
- `../project-v/lifecycle.md`
- `../veda/veda.md`
