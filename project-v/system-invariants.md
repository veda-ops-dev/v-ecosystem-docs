# Project V System Invariants

## Purpose

This document defines the non-negotiable conditions that must remain true for Project V to preserve its identity and role inside the V Ecosystem.

It exists to answer:

```text
What must remain true about Project V so it continues to function as the planning and orchestration system of record without drifting into other system roles?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the non-negotiable behavior and boundary constraints that preserve Project V's role
- the conditions that must remain true across planning, orchestration, handoff, and replanning behavior
- the invariants operators and LLMs must preserve when extending Project V doctrine or implementation
- the anti-drift rules that prevent Project V from collapsing into execution or signal ownership

---

## Out of Scope

This document does not define:

- detailed Project V workflow steps
- detailed schema design
- detailed approval thresholds
- detailed implementation structure
- detailed interface payload formats

Those belong in more specific Project V, workflow, governance, and interface docs.

---

## System

- project-v

---

## Core Rule

Project V must remain the planning and orchestration system of record.

Any design, workflow, storage pattern, interface behavior, or operator practice that causes Project V to absorb execution truth, signal-system truth, or unguided governance authority violates Project V system invariants.

BYDA-related audit capabilities operate within Project V's planning and governance truth domain. Their full scope within Project V is defined in `byda-in-project-v.md`. Until that doc is overridden by a later decision, BYDA must not be implemented in a way that extends Project V's ownership into execution truth or signal truth domains.

---

## Invariant Definition

A Project V system invariant is a condition that must remain true for Project V to preserve its ecosystem identity, authority boundaries, and planning role.

An invariant is not a local preference.
It is not a temporary implementation convenience.
It is not a stylistic choice.

If an invariant is violated, Project V may still appear functional while becoming doctrinally wrong.

---

## Invariant 1 - Project V Owns Planning and Orchestration Truth

Project V must remain the system of record for:

- planning truth
- orchestration truth
- readiness truth
- decision truth on the planning side
- handoff truth

### Rule
Project V must be the place where the ecosystem decides:

- what work exists
- how work is structured
- what is ready
- what should move next
- what should be handed off
- what planning changes are required when conditions change

### Violation Examples
The invariant is violated if Project V is treated as:

- optional planning metadata attached to another system's truth
- a passive mirror of execution decisions made elsewhere
- a thin wrapper around observability inputs that already determine what planning must do

---

## Invariant 2 - Project V Does Not Own Execution Truth

Project V must not become the canonical owner of execution truth.

### Rule
Project V may:

- create handoff truth
- preserve planning-side traceability about what was handed off
- receive bounded execution findings that matter for planning reconsideration
- preserve planning outcomes that result from replanning

Project V must not:

- become the long-lived execution ledger
- store rich execution lifecycle state as though it were the canonical execution record
- substitute for V Forge as the owner of what happened during execution

### Explanation
Project V must know enough about execution to govern planning continuity.
It must not know so much, or own so much, that execution truth migrates out of V Forge.

### Violation Examples
The invariant is violated if Project V becomes the place where operators or agents go to determine:

- canonical execution status history
- canonical implementation state
- canonical record of what was done in execution

---

## Invariant 3 - Project V Does Not Own Signal or Observability Truth

Project V must not become the canonical owner of signal, evidence, or observability truth.

### Rule
Project V may consume bounded signal and evidence outputs relevant to planning.
Project V may preserve planning interpretations of signal.

Project V must not:

- become a signal warehouse
- absorb VEDA's evidence record as its own canonical store
- treat received signal as though it changed VEDA ownership boundaries
- replace VEDA as the system of record for reality-facing inputs

### Explanation
Planning depends on evidence.
That does not make planning the owner of evidence truth.

### Violation Examples
The invariant is violated if Project V becomes the default home for:

- accumulated observability history
- source-of-record evidence archives
- rich provenance storage that belongs to VEDA's evidence role

---

## Invariant 4 - Project V Governs Handoff Without Becoming Execution

Project V must govern the transition into execution without collapsing planning into execution.

### Rule
Project V is responsible for:

- determining readiness for handoff
- creating bounded handoff truth
- preserving the planning basis for why work was handed off
- constraining execution through approved scope and handoff conditions

Project V is not responsible for:

- carrying out the execution itself as the execution system of record
- keeping full execution-state continuity inside planning records
- redefining execution truth after responsibility transfers

### Explanation
Handoff is a boundary-preserving transition, not a merge.
Project V remains responsible for planning and orchestration before and after handoff, but execution responsibility moves to V Forge.

---

## Invariant 5 - Project V Replans Through Governed Return Paths

Project V must re-enter planning through governed return paths rather than through silent ownership blur.

### Rule
When execution findings, changed conditions, or revised evidence affect planning:

- Project V may reconsider planning
- Project V may revise planning outcomes through governed paths
- Project V may trigger new planning, revised handoff decisions, deferral, restructuring, or cancellation where justified

But Project V must do so by interpreting bounded returned inputs, not by absorbing full external truth domains.

### Explanation
Replanning is part of Project V's identity.
Ownership collapse is not.

### Violation Examples
The invariant is violated if replanning behavior assumes that:

- all execution state now belongs in Project V
- all evidence history now belongs in Project V
- returned findings automatically rewrite governing planning decisions without the appropriate planning and governance path

---

## Invariant 6 - Project V Preserves Decision Continuity

Project V must preserve planning-side decision continuity across intake, planning, handoff, and replanning.

### Rule
Project V must:

- reference relevant prior governing decisions
- preserve rejection continuity where planning outcomes were rejected
- avoid silently discarding prior decisions during replanning
- avoid creating contradictory planning truth without explicit resolution

When a proposed planning action would violate decision continuity, Project V must not proceed as though continuity is advisory. The correct response is to surface the conflict explicitly and apply the governed conflict path defined in `../governance/decision-continuity-doctrine.md`, including reaffirmation, revision, supersedence, invalidation, or escalation as appropriate.

### Explanation
Project V is not just a planner of the current moment.
It is the planning continuity anchor for the ecosystem.

If Project V loses decision continuity, orchestration becomes rediscovery rather than governed planning.

---

## Invariant 7 - Project V Does Not Treat Interpretation as Decision

Project V must preserve the distinction between input interpretation, recommendation, decision, approval, and action.

### Rule
Within Project V:

- signal interpretation is not automatically a decision
- planning recommendation is not automatically an approved decision
- readiness is not automatically handoff activation
- returned findings are not automatically planning mutation

### Explanation
Because Project V sits at the center of planning, it is one of the easiest places for semantic compression to create governance drift.
Project V must therefore preserve stage distinctions cleanly.

### Violation Examples
The invariant is violated if Project V behavior treats:

- strong signal as self-authorizing project creation
- drafted planning language as active governing decision
- handoff preparation as equivalent to an approved active handoff

---

## Invariant 8 - Project V Must Remain Multi-Project Capable

Project V must preserve the ability to govern multiple projects without collapsing them into a single undifferentiated planning stream.

### Rule
Project V planning and orchestration behavior must support:

- bounded project identity
- bounded project-level planning context
- bounded decision continuity per project where relevant
- cross-project prioritization without losing project separation

### Explanation
Project V is not a single-project scratchpad.
Its planning model must remain compatible with ecosystem-scale portfolio behavior.

### Violation Examples
The invariant is violated if Project V evolves toward:

- one giant planning thread with no durable project boundaries
- cross-project decision blur that makes project-specific continuity unrecoverable
- execution-driven state being used as the only practical organizer of work

---

## Invariant 9 - Project V Must Remain Governed

Project V must remain a governed planning system, not an autonomous planning sovereign.

### Rule
Project V behavior must remain compatible with:

- approval requirements
- escalation requirements
- reviewable planning transitions
- externalized reporting
- human-in-the-loop control where doctrine requires it

### Explanation
Project V is where many high-impact ecosystem decisions are shaped.
That makes governance discipline more important, not less.

### Violation Examples
The invariant is violated if Project V is treated as a place where:

- planning recommendations become active without required approval
- operator conversation is treated as self-sufficient governance state
- planning mutation happens without reviewable continuity or reporting

---

## Invariant 10 - Project V Must Remain Interface-Respecting

Project V must interact with other systems through bounded interfaces and workflows rather than through casual ownership-breaking reach.

### Rule
Project V must receive and emit cross-system meaning through:

- the VEDA to Project V signal interface
- the Project V to V Forge handoff interface
- the V Forge to Project V return-to-planning interface
- other explicit ecosystem interfaces and workflows as they are defined

Project V must not normalize boundary-blind behavior just because technical access exists.
Project V must also not normalize accepting inputs that bypass the governed interface path. Inbound bypass degrades interface governance as much as outbound bypass. An input arriving through an informal or non-governed path must not be treated as equivalent to properly interfaced input.

### Explanation
Project V is central.
Centrality is not permission to bypass interfaces.

---

## Invariant 11 - Project V Must Preserve Planning-Side Traceability

Project V must preserve enough planning-side traceability that operators and agents can understand how planning outcomes were formed and how they relate to handoff and replanning.

### Rule
Project V must remain able to show, at a planning level:

- what was considered
- what decision or planning outcome was reached
- what inputs materially mattered
- what handoff or replanning consequence followed
- what prior governing decisions constrained the outcome

### Explanation
Traceability does not require Project V to duplicate other systems' full records.
It requires Project V to preserve the planning-side chain of meaning needed for review and continuity.

---

## Invariant 12 - Project V Must Not Collapse Into Implementation Detail

Project V doctrine must remain planning doctrine, not implementation mush.

### Rule
Project V may reference implementation-facing consequences where planning needs them.
But Project V core authority must not become dominated by:

- repo-local engineering detail
- schema trivia that does not govern planning behavior
- transport-specific assumptions that replace doctrinal rules
- implementation narration that obscures planning responsibility

### Explanation
When planning doctrine collapses into implementation detail, the ecosystem loses the authority layer that implementation is supposed to follow.

---

## Failure Modes (Explicitly Forbidden)

The following are invariant failures:

- Project V becoming the canonical execution ledger
- Project V becoming the canonical signal or evidence warehouse
- handoff being treated as a soft internal state flip with no real responsibility transfer
- replanning being treated as permission to absorb execution or evidence ownership
- recommendations, drafts, or readiness states being treated as active approved planning decisions automatically
- cross-project planning collapsing into undifferentiated context mush
- planning mutation bypassing approval, escalation, continuity, or reporting requirements
- technical access being treated as permission to bypass interfaces
- Project V doctrine being replaced by implementation-specific convenience

---

## Human-In-The-Loop Principle

Project V invariants matter especially because Project V shapes what the ecosystem will do next.

Human review remains important where doctrine requires it, especially for:

- project creation
- major planning changes
- handoff activation
- high-impact replanning
- strategic reprioritization
- doctrine changes affecting Project V scope

Human review does not weaken Project V.
It is part of what keeps Project V governed.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- Project V is the planner and orchestrator
- Project V must not become the executor
- Project V must not become the signal system
- replanning must preserve boundaries rather than absorb other truth domains
- planning semantics and governance stages must remain explicit
- Project V's central role increases its need for anti-drift discipline

If Project V implementation or workflow evolution makes it behave like a merged planner-executor-observability blob, these invariants are being violated.

---

## Usage

This document should be used:

- when evaluating whether a proposed Project V feature preserves Project V identity
- when deciding whether a Project V workflow change causes ownership drift
- when writing more specific Project V doctrine
- when reviewing whether planning, handoff, or replanning behavior is still in-bounds
- when evaluating whether implementation choices are starting to redefine doctrine

---

## Related Docs

- `project-v.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/project-intake-workflow.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/decision-continuity-doctrine.md`
- `multi-project-doctrine.md`
- `operational-workflow.md`
- `lifecycle.md`
