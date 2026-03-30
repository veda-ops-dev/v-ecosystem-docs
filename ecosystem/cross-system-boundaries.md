# Cross-System Boundaries

## Purpose

This document defines the primary boundaries between the core systems of the V Ecosystem.

It exists to answer:

```text
What does each core system own, what does it not own, and what kinds of cross-system behavior are allowed or forbidden?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- cross-system ownership boundaries
- what kinds of truth belong to which system
- high-level rules for cross-system interaction
- the boundary posture used by operators and LLMs when classifying behavior

---

## Out of Scope

This document does not define:

- detailed interface contracts
- detailed workflow steps
- detailed approval rules
- detailed data models
- implementation-specific integration logic

Those belong in interface, workflow, governance, and project-specific docs.

---

## System

- ecosystem

---

## Core Rule

Each core system in the V Ecosystem owns a different kind of truth.

Cross-system cooperation is required.
Cross-system ownership blur is not allowed.

A system may consume outputs from another system without becoming the owner of that other system's truth.

---

## System Ownership Boundaries

## Project V

### Owns
- planning truth
- orchestration truth
- readiness truth
- decision truth
- handoff truth
- pre-build planning intelligence derived from VEDA market signal

### Does Not Own
- long-lived execution truth
- signal and observability truth
- raw external evidence as canonical system truth
- the content graph of what was built
- post-build execution intelligence

### Boundary Rule
Project V may interpret evidence and receive execution findings, but it must not absorb execution-state ownership or observability-state ownership.
Project V reads VEDA signal to inform planning. It does not own the signal.

---

## VEDA

### Owns
- signal truth from external reality
- evidence truth captured from external sources
- observability truth — SERP data, keyword intelligence, search performance, GA4, Search Console, YouTube observatory
- source capture and source item ingestion
- observatory event log
- external provider data ingestion pipelines

### Does Not Own
- planning truth
- orchestration truth
- execution truth
- the content graph of what was built
- execution intelligence derived from content graph analysis
- intelligence synthesis or proposals — VEDA Brain does not exist in this ecosystem

### Boundary Rule
VEDA is a pure observatory. It observes external reality and records what it sees.
VEDA may provide bounded signal to Project V and V Forge through governed interfaces.
VEDA must not become the planner, the executor, the content modeler, or the intelligence synthesizer.

The telescope mental model applies: if a telescope would not do it, VEDA should not do it.

---

## V Forge

### Owns
- execution truth
- implementation truth
- the content graph of what was built — pages, topics, entities, internal links, archetypes, schema usage
- execution intelligence — cross-referencing the content graph against VEDA signal to assess performance and identify gaps
- bounded execution-side research
- execution-side maintenance truth
- execution-side reporting

### Does Not Own
- planning truth
- orchestration truth
- signal truth as a system of record
- observability truth as a system of record
- raw SERP data, GA4 data, Search Console data, or YouTube observatory data

### Boundary Rule
V Forge may consume planning inputs from Project V and bounded signal from VEDA.
V Forge owns what was built and what happened during execution.
V Forge reads VEDA signal to produce execution intelligence. It does not own the signal.
Bounded execution-side research means research performed in support of approved execution, handoff, maintenance, or return-to-planning needs. It does not mean open-ended ecosystem-wide signal gathering.

---

## Cross-System Access Rules

## Rule 1 — Read access is not ownership
A system may read or consume bounded outputs from another system without becoming the owner of that system's truth.

## Rule 2 — Direct cross-system mutation is exceptional
Direct cross-system mutation should be avoided by default.

Cross-system movement of meaning should normally happen through:

- interfaces
- handoffs
- packages
- governed approval and reporting behavior

Not through casual direct mutation.

## Rule 3 — Cross-system behavior must be classifiable
If a proposed action cannot be clearly classified as planning, observability, execution, interface, workflow, or governance behavior, it is not ready to be implemented.

## Rule 4 — Shared context must not erase system ownership
A shared ecosystem view does not mean a shared undifferentiated truth model.

The ecosystem is coordinated, not merged.

## Rule 5 — MCP tools do not bypass system ownership
MCP tools are thin interfaces that call APIs. They do not grant ownership of another system's truth domain. A tool that reads VEDA data does not make the caller the owner of VEDA's signal.

---

## Boundary Examples

### Allowed
VEDA provides a bounded market signal package to Project V.
Project V uses that package to decide whether a new project should be created.

This is allowed because:
- VEDA remains the signal and evidence system of record
- Project V remains the planning system of record

### Allowed
Project V creates a handoff for V Forge.
V Forge executes the work and reports findings back.

This is allowed because:
- Project V owns the planning and handoff truth
- V Forge owns the execution truth

### Allowed
V Forge reads VEDA's performance signal through the governed interface.
V Forge crosses that signal against the content graph to identify execution-side gaps.

This is allowed because:
- VEDA remains the owner of the raw signal
- V Forge remains the owner of the content graph and execution intelligence
- the cross-referencing happens inside V Forge, not inside VEDA

### Not Allowed
VEDA models the content graph of what a project has built and treats it as observatory truth.

This is not allowed because:
- the content graph is execution truth owned by V Forge
- it describes what was built internally, not what was observed externally

### Not Allowed
VEDA generates planning proposals or content gap analysis and presents them as signal outputs.

This is not allowed because:
- planning proposals belong to Project V's planning intelligence layer
- content gap analysis belongs to V Forge's execution intelligence layer
- VEDA Brain does not exist in this ecosystem

### Not Allowed
Project V starts storing rich execution lifecycle state and treating it as canonical execution truth.

This is not allowed because:
- execution truth belongs to V Forge

### Not Allowed
V Forge becomes the canonical owner of raw SERP data, GA4 data, or search performance observation history.

This is not allowed because:
- observatory truth belongs to VEDA
- V Forge reads signal but does not own it

---

## Data Boundary Principle

Cross-system database proximity or shared infrastructure does not remove logical ownership boundaries.

Even if systems later share a cluster or infrastructure layer, the docs must still define:

- who owns what data
- what is local vs shared
- what is readable vs mutable
- what must move through interfaces instead of direct access

Infrastructure convenience must not redefine system ownership.

---

## Interface Principle

Whenever one system needs something from another, the interaction should be documented through a bounded interface model.

That interface may be:

- a signal interface
- a handoff interface
- a return-to-planning interface
- an MCP coordination interface
- another explicit ecosystem interface

Unbounded reach into another system is drift.

---

## Human-In-The-Loop Principle

Cross-system boundaries are especially important because human-in-the-loop review depends on clear responsibility.

If the boundary is blurry then:
- approvals become unclear
- reports become unclear
- accountability becomes unclear
- LLM behavior becomes harder to govern

Clear boundaries make governance possible.

---

## Usage

This document should be used:

- when deciding where a concept belongs
- when deciding whether a proposed action crosses a boundary
- when writing project-specific doctrine
- when writing interface docs
- when evaluating future new-project fitment into the ecosystem

---

## Related Docs

- `v-ecosystem-overview.md`
- `vocabulary.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../onboarding/new-project-access-and-boundary-rules.md`
