# V Forge

## Purpose

This document defines what V Forge is inside the V Ecosystem.

It exists to answer:

```text
What role does V Forge play in the V Ecosystem, what truth does it own, and how should V Forge be understood by operators and LLMs?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the identity of V Forge
- the role V Forge plays in the ecosystem
- the kinds of truth V Forge owns
- the high-level boundary between V Forge and other systems
- the default mental model used when classifying V Forge behavior

---

## Out of Scope

This document does not define:

- detailed V Forge workflows
- detailed execution tooling or runtime design
- detailed interface contracts
- detailed governance rules
- implementation details

Those belong in more specific V Forge, interface, workflow, or governance docs.

---

## System

- v-forge

---

## Core Rule

V Forge is the execution system of record in the V Ecosystem.

V Forge exists to carry out approved work, preserve execution truth, own the content graph of what was built, perform bounded execution-side research required to complete or validate approved handoffs, and report bounded execution findings back into the ecosystem.

Execution-side research is bounded to work required to complete or validate an approved handoff. V Forge must not conduct open-ended signal gathering and must not propose unsolicited changes to planning direction.

V Forge must not expand into planning ownership or signal-system ownership.

---

## V Forge Definition

V Forge is the system used to execute approved work after responsibility has been handed off from planning.

It turns inputs such as approved handoffs, bounded evidence inputs, operator direction, and prior findings into:

- execution truth
- implementation truth
- content graph truth for built projects
- bounded execution findings
- execution intelligence derived from crossing content graph against VEDA signal
- maintenance execution outputs
- execution-side reporting

V Forge is not the planner.
V Forge is not the signal/observability system of record.

---

## Owns

V Forge owns:

- execution truth
- implementation truth
- the content graph of what was built — pages, topics, entities, internal links, archetypes, schema usage
- execution intelligence — the cross-referencing of the content graph against VEDA observatory signal
- bounded execution-side research
- execution-side maintenance truth
- execution-side reporting
- bounded execution findings produced during approved work

### Content Graph Ownership Explanation
The content graph is the structural model of what a project has built. It describes pages, topics, entities, internal links, archetypes, and schema usage. This is execution truth because it reflects what V Forge has built. It changes when V Forge does work — when pages are created, when structure changes, when content is added.

The content graph does not belong in VEDA because VEDA is a pure observatory of external reality. The content graph is not an observation of external reality. It is a record of what was built.

### Execution Intelligence Explanation
V Forge owns the execution intelligence layer — the analysis of how what was built is performing and where the gaps are. This is done by reading VEDA's observatory signal through a governed interface and crossing it against the content graph.

Questions like "we have these pages but SERP data shows we are missing coverage here" are V Forge execution intelligence questions, not VEDA questions. VEDA provides the raw signal. V Forge does the cross-referencing against what was actually built.

---

## Does Not Own

V Forge does not own:

- planning truth
- orchestration truth
- readiness truth
- handoff truth
- signal truth
- observability truth as a system of record
- project-creation authority
- raw SERP data, GA4 data, Search Console data, or YouTube observatory data

### Explanation
V Forge may consume handoffs from Project V.
V Forge may consume bounded signal outputs from VEDA through the governed interface.
V Forge may produce bounded execution findings that matter to Project V or VEDA.

But V Forge must not become the canonical owner of planning structure or signal-system truth.
V Forge reads VEDA signal. It does not own it.

Project-creation authority belongs to Project V. V Forge executes work for projects that already exist in the ecosystem. V Forge does not decide that a project should exist, what it should be, or what its planning structure should be. Those are planning decisions owned by Project V.

---

## Main Ecosystem Relationships

### Relationship to Project V
Project V hands off approved work to V Forge.

V Forge executes that work and may return bounded execution findings (including issues or changed conditions) back to Project V where planning reconsideration is needed.

Project V remains the planning and orchestration system of record.
V Forge remains the execution system of record.

### Relationship to VEDA
V Forge consumes bounded observatory signal from VEDA through the governed signal interface.

V Forge uses that signal to power its execution intelligence layer — understanding how what was built is performing externally and where execution-side gaps exist.

VEDA remains the signal, evidence, and observability system of record.
V Forge must not absorb the signal-system role by accumulating open-ended signal ownership.
V Forge reads what VEDA observed. V Forge does not replace VEDA as the observer.

The governed signal path is defined in `../interfaces/veda-to-v-forge-signal-interface.md`.

---

## Responsibility Model

V Forge is responsible for:

- executing approved work
- preserving execution continuity
- owning and maintaining the content graph of what was built
- performing bounded execution-side research in support of approved work
- crossing the content graph against VEDA signal to produce execution intelligence
- reporting execution outcomes and bounded execution findings
- supporting maintenance execution
- returning bounded execution findings back into the ecosystem where needed
- returning blocked, failed, or incomplete execution to planning through bounded reporting

V Forge is not responsible for:

- deciding project structure
- deciding what should be pursued in planning
- serving as the canonical observability system
- owning raw SERP, GA4, Search Console, or YouTube data
- replacing Project V's orchestration role
- replacing VEDA's signal and evidence role

---

## Human-In-The-Loop Principle

V Forge is a governed execution system.

Human review and direction remain especially important for:

- execution approvals where required
- external paid actions
- significant mutations
- launch-sensitive execution
- doctrine changes affecting execution boundaries

V Forge may be heavily LLM-assisted, but it is not an unrestricted autonomous execution environment.

---

## LLM Use Principle

A capable LLM should be able to infer from the V Forge docs that:

- V Forge is the executor
- V Forge owns the content graph of what was built
- V Forge owns execution intelligence derived from content graph plus VEDA signal
- V Forge is not the planner
- V Forge does not create projects — it executes work for projects that Project V has planned
- V Forge is not the signal system
- V Forge reads VEDA signal but does not own it
- V Forge must preserve execution truth without absorbing planning or observability truth

If the docs allow V Forge to drift toward planning ownership, observability ownership, or raw signal accumulation, the V Forge doctrine is wrong.

---

## Usage

This document should be used:

- as the first identity doc for V Forge in the shared root
- as the top-level V Forge role definition for operators and LLMs
- as a boundary reference when writing more specific V Forge docs
- as a check against future drift in V Forge design or implementation

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `system-invariants.md`
- `operational-model.md`
- `vs-project-v.md`
- `vs-veda.md`
- `human-in-the-loop-doctrine.md`
- `reporting-and-approval-model.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
