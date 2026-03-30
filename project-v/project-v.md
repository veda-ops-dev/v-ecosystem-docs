# Project V

## Purpose

This document defines what Project V is inside the V Ecosystem.

It exists to answer:

```text
What role does Project V play in the V Ecosystem, what truth does it own, and how should Project V be understood by operators and LLMs?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the identity of Project V
- the role Project V plays in the ecosystem
- the kinds of truth Project V owns
- the high-level boundary between Project V and other systems
- the default mental model used when classifying Project V behavior

---

## Out of Scope

This document does not define:

- detailed Project V workflows
- detailed schema or route design
- detailed interface contracts
- detailed governance rules
- implementation details

Those belong in more specific Project V, interface, workflow, or governance docs.

---

## System

- project-v

---

## Core Rule

Project V is the planning and orchestration system of record in the V Ecosystem.

Project V exists to decide what should be pursued, how it should be structured, when it is ready, and when responsibility should be handed off for execution.

Project V must not expand into long-lived execution ownership or signal-system ownership.

---

## Project V Definition

Project V is the system used to create, organize, govern, and hand off work inside the V Ecosystem.

It turns inputs such as signal, evidence, strategic intent, operator direction, and prior findings into:

- project structure
- planning decisions
- readiness decisions
- handoff decisions
- orchestration truth

Project V is not the long-term home of execution truth.
It is not the signal/observability system of record.

---

## Owns

Project V owns:

- planning truth
- orchestration truth
- project decomposition
- readiness truth
- decision truth
- handoff truth
- planning-side traceability

### Explanation
Project V is where the ecosystem decides:

- what work exists
- how that work is organized
- what is ready
- what is blocked
- what should move next
- what should be handed off

---

## Does Not Own

Project V does not own:

- long-lived execution truth
- implementation truth
- signal truth
- observability truth
- raw external evidence as a canonical store
- rich execution lifecycle state

### Explanation
Project V may consume evidence and findings.
Project V may issue handoffs.
Project V may receive bounded execution findings back.

But Project V must not become the system that owns what happened in execution as the canonical execution record.

---

## Main Ecosystem Relationships

## Relationship to VEDA
Project V consumes bounded planning-relevant outputs from VEDA.

Project V does not own VEDA’s observability or evidence role.
VEDA remains the signal, evidence, and observability system of record.

## Relationship to V Forge
Project V creates and governs handoff truth for work that should move into execution.

V Forge owns execution truth after execution responsibility is handed off.
Project V may receive bounded execution findings back when execution, changed conditions, or revised evidence require planning reconsideration.
Project V does not remain the owner of long-lived execution truth after handoff.

---

## Responsibility Model

Project V is responsible for:

- turning opportunity or intent into governed project structure
- preserving planning continuity
- preserving decision continuity on the planning side
- determining readiness
- creating bounded handoff packages
- re-entering planning when bounded execution findings, changed conditions, or revised evidence require it

Project V is not responsible for:

- serving as the final execution ledger
- becoming a signal warehouse
- acting as a general-purpose implementation workspace

---

## Human-In-The-Loop Principle

Project V is a governed planning and orchestration system.

Human review and direction remain especially important for:

- project creation
- prioritization changes
- major decision changes
- approval-sensitive handoffs
- doctrine changes

Project V may be heavily LLM-assisted, but it is not designed to dissolve human planning authority.

---

## LLM Use Principle

A capable LLM should be able to infer from the Project V docs that:

- Project V is the planner
- Project V is the orchestrator
- Project V is not the executor
- Project V is not the signal system
- Project V must hand off execution rather than absorb it

If the docs allow Project V to drift toward execution ownership, the Project V doctrine is wrong.

---

## Usage

This document should be used:

- as the first identity doc for Project V in the shared root
- as the top-level Project V role definition for operators and LLMs
- as a boundary reference when writing more specific Project V docs
- as a check against future drift in Project V design or implementation

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `system-invariants.md`
- `multi-project-doctrine.md`
- `operational-workflow.md`
- `lifecycle.md`
- `v-forge-integration.md`
