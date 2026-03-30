# Project Intake Workflow

## Purpose

This document defines the cross-system workflow by which planning-relevant signal becomes a Project V intake decision inside the V Ecosystem.

It exists to answer:

```text
How does planning-relevant signal move through the ecosystem to become a project-intake decision, and what systems are responsible at each step?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the workflow from VEDA signal into Project V intake consideration
- the workflow from operator or strategy-driven intake entry into Project V intake consideration
- the main stages of intake before a project is created, deferred, rejected, or held
- which systems are responsible at each stage
- the boundary posture operators and LLMs should use during intake

---

## Out of Scope

This document does not define:

- detailed Project V internal project schema
- detailed scoring formulas
- detailed source-trust policy
- detailed approval rules
- detailed handoff workflow after intake

Those belong in Project V docs, governance docs, strategy docs, and other workflow docs.

---

## System

- workflows

---

## Core Rule

Project intake is the governed workflow by which planning-relevant signal is interpreted inside Project V and turned into a planning outcome.

Signal does not become a project automatically.
Execution does not create projects directly.
Intake is where planning decides whether something should become governed project work.

---

## Workflow Definition

The project intake workflow is the bounded workflow that moves from:

- signal or evidence that may matter
- or operator / strategy-driven intake triggers that require planning evaluation

through:

- planning interpretation and intake evaluation

into one of several planning outcomes, such as:

- create project
- defer
- reject
- request more evidence
- hold for later reconsideration

This workflow exists so that the ecosystem can create projects deliberately rather than casually.

---

## Workflow Preconditions

Project intake should begin only when:

- planning-relevant signal or evidence has reached Project V through the appropriate signal path
  - or
- operator direction or strategic input has created a valid planning intake question
- the intake question is clear enough to evaluate at a planning level

Operator direction or strategic input that does not originate from VEDA enters the intake workflow at Stage 2 — Intake Framing, and must follow the same planning and governance boundary rules from that point forward.

Project intake must not begin from:

- raw unbounded observability state
- execution-state ownership
- casual project creation without planning interpretation

---

## Primary Workflow Stages

## Stage 1 — Signal Reaches Planning

### Description
VEDA provides bounded planning-relevant signal or evidence to Project V through the VEDA to Project V signal interface.

### Responsibility
- VEDA owns the signal/evidence truth being surfaced
- Project V receives the signal for planning interpretation

### Boundary Rule
The signal is still VEDA-owned signal/evidence truth.
At this stage, Project V has received planning-relevant input, not a planning decision.

---

## Stage 2 — Intake Framing

### Description
Project V frames the intake question.

This means Project V determines what is being considered at a planning level, such as:

- whether a possible project exists
- whether an existing project may need reconsideration
- whether the signal is insufficient for project creation but relevant for later review
- whether operator direction or strategic input should become a formal intake candidate

### Responsibility
- Project V owns intake framing

### Boundary Rule
VEDA does not frame the intake decision for Project V.
Signal informs framing, but does not replace it.
Operator direction or strategic input may enter here, but does not bypass planning boundaries.

---

## Stage 3 — Planning Interpretation

### Description
Project V interprets the bounded signal, evidence, or intake trigger in planning terms.

This may include considering:

- project relevance
- priority implications
- readiness implications
- whether the signal affects an existing project or suggests a new one
- what the intake item means for planning

### Responsibility
- Project V owns planning interpretation

### Boundary Rule
Interpretation is not yet project creation.
Interpretation is where planning decides what the intake item means, not whether it is sufficient to act on and not where execution begins.

---

## Stage 4 — Intake Evaluation

### Description
Project V evaluates the intake using the current planning, governance, and strategy posture.

This may include evaluating:

- whether there is enough bounded signal or justified planning input to act
- whether the intake item should create new work
- whether the item should be deferred or held
- whether more bounded evidence is needed
- whether governance review or human review is required before the intake outcome becomes active

### Responsibility
- Project V owns intake evaluation
- governance rules may affect what can be finalized

### Boundary Rule
This stage determines whether planning should produce a formal intake outcome.
It does not skip directly to execution.
Governance review or human review may be required before an intake outcome becomes active. See the Human-In-The-Loop section below.

---

## Stage 5 — Intake Outcome

### Description
Project V produces an intake outcome.

Allowed intake outcomes include:

- create project
- defer
- reject
- hold for later reconsideration
- request additional bounded evidence

### Responsibility
- Project V owns the intake outcome

### Boundary Rule
VEDA does not create the intake outcome.
V Forge does not create the intake outcome.
Only Project V creates intake outcomes.

---

## Stage 6 — Post-Intake Direction

### Description
After an intake outcome exists, the ecosystem follows the appropriate next step.

Examples:

- if a project is created, Project V continues planning and decomposition
- if more evidence is needed, the appropriate bounded evidence path is triggered
- if the item is deferred or held, Project V preserves the planning-side status
- if the item is rejected, Project V preserves the decision continuity for that rejection as a durable planning-side decision when the item may resurface later

When additional bounded evidence is returned through the appropriate signal path, intake resumes at:

- Stage 2 if the intake framing question still needs work
- Stage 3 if the intake framing question is already established and the new evidence is being interpreted against that frame

### Responsibility
- Project V owns post-intake planning direction
- VEDA may later supply more bounded signal if requested through the correct path

### Boundary Rule
Intake does not automatically imply handoff.
A created project is still in planning until later readiness and handoff conditions are met.
Rejection continuity requirements are further governed by `../governance/decision-continuity-doctrine.md`.

---

## Intake Outcome Semantics

A valid intake outcome should be interpretable as answering:

- what was considered
- what signal or evidence mattered
- what planning question was evaluated
- what outcome was produced
- whether more evidence is needed
- whether later reconsideration is expected

For inconclusive cases:

- hold is appropriate when the item is valid but timing is not yet right
- defer is appropriate when the item is valid but priority is not sufficient
- request additional bounded evidence is appropriate when the item cannot yet be evaluated with enough confidence

These semantics may later be represented through specific records or workflow structures, but the semantic contract comes first.

---

## Retention Principle

Not every planning-relevant signal should become a project.

The intake workflow exists partly to prevent project sprawl.

Signal that is interesting but not strong enough, clear enough, or timely enough for project creation should remain:

- deferred
- held
- rejected
- or routed for additional bounded evidence

Project creation is one possible intake outcome, not the default outcome.

---

## Human-In-The-Loop Principle

Project intake is a governance-sensitive workflow because it can create new project work or materially alter planning direction.

Human review or approval may be required depending on:

- project creation significance
- strategic importance
- uncertainty or source-trust concerns
- cost implications
- whether the intake result would materially change ecosystem priorities

The governance and approval model for these decisions is defined in `../governance/approval-and-escalation-model.md`.

For approval class reference: high-significance intake outcomes such as project creation with material planning impact are Class B or Class C depending on scope and cost implications; lower-significance intake outcomes such as defer, hold, or request additional evidence are typically Class A or Class B. See `../governance/approval-and-escalation-model.md` for class definitions.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- VEDA provides signal to planning, but does not create projects
- operator direction may enter intake, but does not bypass planning boundaries
- Project V owns intake framing, interpretation, evaluation, and outcome
- intake is a multi-stage workflow, not a single state flip
- project creation is only one possible intake outcome
- the intake workflow is one of the main places where evidence-to-project drift must be prevented

If the workflow is implemented as automatic project creation from signal or as a boundary-free shortcut from operator intent to project creation, the doctrine is wrong.

---

## Usage

This document should be used:

- when designing project intake records or workflow states
- when deciding whether signal should become a project-intake question
- when deciding how operator or strategy-driven intake enters the planning workflow
- when reviewing whether the ecosystem is creating projects too casually
- when writing Project V and VEDA workflow docs related to intake
- when evaluating whether governance is being bypassed during project creation

---

## Related Docs

- `../interfaces/veda-to-project-v-signal-interface.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/project-v.md`
- `../strategy/opportunity-scoring-model.md` *(planned)*
- `../governance/approval-and-escalation-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../workflows/handoff-workflow.md`
