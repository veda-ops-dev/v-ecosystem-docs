# Ecosystem Objective Function

## Purpose

This document defines what the V Ecosystem is trying to accomplish and what kinds of opportunities count as in-scope.

It exists to answer:

```text
What is the V Ecosystem pursuing, what kinds of opportunities fall inside that pursuit, and what criteria distinguish an in-scope opportunity from one that does not belong here?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the top-level objective that the V Ecosystem is designed to serve
- what kinds of opportunities count as in-scope for the ecosystem
- what distinguishes a valid opportunity from one that is out-of-scope or misclassified
- the objective function used when evaluating project candidates at intake
- the criteria operators and LLMs should use when classifying whether a proposed opportunity belongs inside this ecosystem

---

## Out of Scope

This document does not define:

- detailed project scoring formulas or weighted criteria
- how signal is gathered or organized by VEDA
- Project V internal intake workflow steps
- implementation-specific tooling decisions
- what constitutes a strong vs. weak opportunity within in-scope territory

Those belong in the opportunity scoring model, strategy docs, VEDA docs, and Project V workflow docs.

---

## System

- veda_strategy

---

## Core Rule

The V Ecosystem exists to build, maintain, and improve content-driven digital properties that generate sustainable organic search traffic and compounding return over time.

An opportunity is in-scope when it fits that pursuit.
An opportunity that does not fit is not in-scope regardless of how interesting it seems.

---

## Ecosystem Objective

The V Ecosystem is designed to:

- identify underserved or emerging opportunities in organic search
- build content-driven digital properties that capture those opportunities
- maintain and improve those properties over time as conditions change
- generate compounding return by building assets that accumulate value across sessions

The ecosystem is not designed to:

- build one-off outputs with no ongoing compound value
- pursue opportunities with no organic search dimension
- create projects where the execution cost consistently exceeds the return potential
- pursue opportunities that require indefinite manual maintenance without compounding asset value

---

## In-Scope Opportunity Characteristics

An opportunity is in-scope when it has all of the following:

### 1. Organic search demand
There is observable search intent related to the opportunity — queries, topics, or content types that people are already searching for or where demand is emerging.

Search demand does not have to be large. It must be real, durable, and reachable within the ecosystem's execution capabilities.

### 2. Content addressability
The opportunity can be addressed through content that the ecosystem can research, structure, write, maintain, and improve.

Opportunities that require primarily non-content execution — physical production, software development, hardware, or services — are not content-addressable and are not in-scope for this ecosystem.

### 3. Asset compounding potential
The work produces assets that accumulate value over time — pages, topics, authority signals, internal link structures, and evidence of performance that compounds into a stronger position with continued effort.

Opportunities where each execution cycle produces no carry-forward value are not in-scope.

### 4. Execution feasibility within the ecosystem
The opportunity can be pursued using the planning, signal, and execution capabilities this ecosystem provides.

Opportunities that require capabilities the ecosystem does not have and cannot develop are out-of-scope until those capabilities are available.

### 5. Return potential relative to investment
The opportunity has plausible return potential that justifies the planning, execution, and maintenance investment required.

Zero-return opportunities — even well-aligned ones — are not worth pursuing.

---

## Out-of-Scope Opportunity Characteristics

An opportunity is out-of-scope when it has one or more of the following:

- no organic search demand dimension
- no content addressability
- no asset compounding potential
- execution requirements that exceed current ecosystem capabilities without a governed path to build them
- return potential that cannot plausibly justify the investment
- primary value through one-off output rather than compounding asset building

An otherwise interesting opportunity that is out-of-scope must not be pursued as though the objective function does not apply.

---

## Operator Direction and Strategy

The objective function does not prohibit operator direction.

An operator may direct the ecosystem toward specific opportunities within the in-scope territory — including opportunities that VEDA signal does not currently highlight but that the operator has independent reason to pursue.

Operator direction that falls outside the objective function criteria should be recognized as a possible objective function update, not treated as a routine in-scope opportunity.
If operator direction consistently leads toward out-of-scope territory, the objective function itself should be reviewed rather than silently stretched.

---

## Relationship to Project Intake

The project intake workflow accepts two types of intake triggers:

1. Signal-driven intake — from VEDA through the governed signal interface
2. Operator or strategy-driven intake — from operator direction or strategic input

For intake trigger type 2, this document defines the objective function that a strategy-driven intake must satisfy to be treated as a legitimate in-scope intake candidate.

An operator-directed intake that does not satisfy the objective function criteria is not automatically an in-scope opportunity. It must be evaluated against this document and treated as an objective function question before it becomes an intake candidate.

---

## Relationship to Opportunity Scoring

This document defines what is in-scope.
The opportunity scoring model defines how to evaluate relative strength among in-scope opportunities.

A weak in-scope opportunity is still in-scope.
A strong out-of-scope opportunity is still out-of-scope.

Scoring presupposes in-scope classification.

---

## Usage

This document should be used:

- when evaluating whether a proposed opportunity belongs inside the ecosystem
- when operator direction needs to be grounded against objective function criteria
- when signal-driven intake candidates need to be classified as in-scope or out-of-scope
- when reviewing whether the ecosystem is drifting toward out-of-scope work
- when writing strategy and scoring docs that need an objective function anchor

---

## Related Docs

- `opportunity-scoring-model.md`
- `../workflows/project-intake-workflow.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../project-v/project-v.md`
- `../veda/veda.md`
