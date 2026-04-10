# Opportunity Scoring Model

## Purpose

This document defines how the V Ecosystem evaluates the relative strength of in-scope opportunity candidates.

It exists to answer:

```text
Given a set of in-scope opportunities, how does the ecosystem determine which ones are strong enough to pursue now, which should be deferred, and which should be deprioritized or rejected?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the scoring dimensions used to evaluate in-scope opportunity candidates
- how scoring dimensions relate to intake decisions
- how signal quality and evidence confidence affect scoring
- how scoring outputs inform — but do not replace — governed intake decisions
- the anti-drift rules operators and LLMs must preserve when using scoring in intake evaluation

---

## Out of Scope

This document does not define:

- whether an opportunity is in-scope at all (see `ecosystem-objective-function.md`)
- detailed Project V internal intake workflow steps
- specific scoring weights or exact formulas for every case
- VEDA internal signal-gathering mechanics
- post-admission project evaluation or success measurement

Those belong in the objective function doc, intake workflow, VEDA docs, and Project V docs.

---

## System

- veda_strategy

---

## Core Rule

Scoring evaluates relative opportunity strength among already-in-scope candidates.

A score is an input to a governed intake decision. It is not the intake decision itself.

High scoring does not automatically authorize project creation.
Low scoring does not automatically prohibit project creation.
Scoring informs the intake evaluation. The governed intake workflow produces the outcome.

---

## Prerequisite: In-Scope Classification

An opportunity must be classified as in-scope using `ecosystem-objective-function.md` before scoring applies.

Scoring an out-of-scope opportunity is not a governed intake activity.

---

## Scoring Dimensions

Opportunities are evaluated across five dimensions. Each dimension contributes to the overall picture of opportunity strength.

---

### Dimension 1 — Demand Strength

**What it measures:** How strong and durable is the organic search demand for this opportunity?

**Stronger signals:**
- high or growing search volume for the target topics or queries
- stable or growing demand trend, not spiking and declining
- demand exists across multiple related queries, not a single narrow term
- demand is from audiences that convert to compounding value

**Weaker signals:**
- declining or highly volatile demand
- demand concentrated in a single seasonal or trend-driven spike
- demand primarily from audiences unlikely to produce compound value

**Evidence source:** VEDA signal through the governed signal interface

---

### Dimension 2 — Competitive Accessibility

**What it measures:** Can this ecosystem realistically compete for this opportunity given the current competitive environment?

**Stronger signals:**
- incumbent content in this space is weak, thin, outdated, or generic
- there are underserved angles, depths, or formats not covered well by current results
- the ecosystem can produce demonstrably better content at the required depth

**Weaker signals:**
- the space is dominated by large, high-authority, well-resourced incumbents
- incumbent content is strong, comprehensive, and actively maintained
- competing would require authority levels or resource levels the ecosystem does not currently have

**Evidence source:** VEDA SERP signal, competitive intelligence from observatory

---

### Dimension 3 — Asset Compounding Potential

**What it measures:** How much compounding value does success in this space produce over time?

**Stronger signals:**
- the opportunity produces a cluster of related topics that reinforce each other through internal linking and authority compounding
- performance in this space builds toward adjacent opportunities that can be pursued later
- the content produced has long shelf life and requires only bounded maintenance

**Weaker signals:**
- the opportunity is narrow and does not build toward broader topic or authority clusters
- content has short shelf life and requires high ongoing maintenance to remain competitive
- success in this space does not open additional adjacent opportunities

---

### Dimension 4 — Execution Confidence

**What it measures:** How confidently can the ecosystem execute this opportunity with current capabilities and resources?

**Stronger signals:**
- the topic is well-understood and well-documentable without requiring exceptional expertise
- the execution scope is clearly bounded and achievable with current planning and execution capabilities
- similar work has been executed successfully before within this ecosystem

**Weaker signals:**
- the topic requires deep domain expertise the ecosystem does not currently have
- the execution scope is unclear or unbounded
- the required content depth or format exceeds current execution capabilities

---

### Dimension 5 — Return Potential

**What it measures:** What is the plausible return from this opportunity relative to the investment required?

**Stronger signals:**
- traffic from this space would likely convert to outcomes that matter (audience building, monetization, signal feedback, reinvestment potential)
- the investment required is proportionate to the realistic return ceiling
- the opportunity contributes to a larger compounding return rather than producing isolated one-off value

**Weaker signals:**
- realistic traffic ceiling is low relative to execution investment
- the opportunity is peripheral to the ecosystem's main return drivers
- the return depends on conditions unlikely to materialize within a relevant timeframe

---

## Scoring Posture

These five dimensions do not produce a single mechanical score that determines intake outcome. They produce a structured picture of opportunity strength that informs the governed intake decision.

The intake evaluation should be able to answer:

- which dimensions are strong and supported by current signal?
- which dimensions are weak or uncertain?
- do any weak dimensions constitute a disqualifying condition given current priorities?
- does the overall picture support pursuing this opportunity now, deferring it, or rejecting it?

---

## Evidence Quality Affects Scoring Confidence

Dimension scores are only as reliable as the evidence that supports them.

If the evidence for a dimension is:

- thin — the dimension strength is uncertain, not absent
- stale — the dimension may no longer accurately reflect current conditions
- low-trust — the dimension score must carry that trust caveat forward into the intake evaluation

Scoring based on thin, stale, or low-trust evidence must not be presented as confident scoring.

The evidence continuity model is defined in `../governance/evidence-continuity-model.md`.

---

## Scoring Is Not Intake Authorization

A strong opportunity score does not automatically authorize intake.
The governed intake workflow still governs what happens next.

A high score means: this opportunity is strong enough that intake evaluation should proceed seriously.
It does not mean: this opportunity may bypass planning, approval, or intake framing.

The intake workflow is defined in `../workflows/project-intake-workflow.md`.

---

## Scoring and Operator Direction

When operator or strategy-driven intake enters through the intake workflow, scoring applies the same way as for signal-driven intake.

An operator-directed opportunity that scores weakly across dimensions is still weak.
A forceful operator preference does not override weak dimension scores — it should surface as a conflict to resolve through the governed intake evaluation, not as a shortcut to override scoring.

Operators may legitimately direct the ecosystem toward opportunities with weaker signal if they have independent reason for confidence. That confidence should be explicitly surfaced in the intake evaluation rather than silently overriding dimension scores.

---

## Intake Outcome Relationship

Scoring should inform the following intake outcomes defined in the intake workflow:

- **create project** — strong dimensions with evidence support, plausible now
- **defer** — generally sound but timing or evidence not yet right
- **hold** — plausible but not priority at this time
- **request additional evidence** — dimension confidence is too low to evaluate honestly
- **reject** — dimensions are too weak or conditions are disqualifying regardless of other factors

---

## Anti-Drift Rules

Scoring drifts when:

- out-of-scope opportunities are scored as though they qualify
- scoring confidence is overstated relative to evidence quality
- a strong score is treated as intake authorization rather than intake input
- operator direction silently overrides scoring without surfacing the conflict
- dimensions are evaluated selectively to justify a predetermined intake outcome

These patterns must not be normalized.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- scoring presupposes in-scope classification
- scores are inputs to governed intake decisions, not decisions themselves
- dimension strength depends on evidence quality, not just stated values
- weak scores do not prohibit intake and strong scores do not authorize it
- operator direction must surface as an explicit input, not as a silent override

If a scoring exercise produces an intake outcome without a governed intake decision, this doctrine is failing.

---

## Usage

This document should be used:

- when evaluating the relative strength of in-scope opportunity candidates
- when preparing intake candidates for governed intake evaluation
- when reviewing whether intake decisions are adequately grounded in dimension evidence
- when operator-directed intake needs to be evaluated against structured criteria
- when reviewing whether the intake pipeline is pursuing opportunities systematically or casually

---

## Related Docs

- `ecosystem-objective-function.md`
- `../workflows/project-intake-workflow.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../governance/evidence-continuity-model.md`
- `../project-v/project-v.md`
