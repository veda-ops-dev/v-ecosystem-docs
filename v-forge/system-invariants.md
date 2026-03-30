# V Forge System Invariants

## Purpose

This document defines the non-negotiable invariants that must remain true for V Forge to remain V Forge inside the V Ecosystem.

It exists to answer:

```text
What must always remain true about V Forge's role, ownership, execution posture, and ecosystem boundaries so that V Forge does not drift into planning ownership, signal-system ownership, or unrestricted autonomous execution?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the non-negotiable invariants of V Forge
- what V Forge must continue to own
- what V Forge must not become
- what execution-side boundaries must remain true
- what kinds of drift are forbidden even if they seem operationally efficient
- how V Forge must relate to governance, interfaces, workflows, and neighboring systems

---

## Out of Scope

This document does not define:

- detailed execution workflows
- detailed tool/runtime design
- detailed handoff payload structure
- detailed return-to-planning payload structure
- detailed approval matrices
- detailed reporting formats
- detailed content graph schema design

Those belong in more specific V Forge, interface, workflow, or governance docs.

---

## System

- v-forge

---

## Core Rule

V Forge must remain the execution system of record.

It owns execution truth, the content graph of what was built, and the execution intelligence derived from crossing the content graph against VEDA signal.

It must not drift into planning ownership, signal-system ownership, project-creation ownership, or unrestricted open-ended action merely because doing so seems faster, more autonomous, or more convenient.

If a design change makes execution easier by weakening those invariants, the design change is wrong.

---

## Invariant Definition

A V Forge invariant is a condition that must remain true for V Forge to preserve its identity, authority, and ecosystem fit.

An invariant is not a preference.
It is not a local implementation convenience.
It is a constraint that protects the role V Forge plays in the wider ecosystem.

If an implementation, workflow, or operational shortcut violates a V Forge invariant, the shortcut must not be normalized.

When a proposed design change, implementation, or operational shortcut would violate a V Forge invariant, the correct response is to stop, surface the conflict explicitly, and escalate or redesign through a governed architecture path.
Invariant violations that are temporarily normalized for operational reasons become permanent drift.

---

## Invariant 1 — V Forge Owns Execution Truth

V Forge must remain the system of record for execution truth.

This includes:

- what execution work was actually performed
- what was produced during execution
- what happened during execution
- what bounded execution-side findings emerged during approved work
- what execution-side maintenance activity occurred
- what execution-side reports accurately describe the work and its outcomes

If another system becomes the canonical owner of those domains, or if V Forge stops preserving them clearly, the execution model is failing.

---

## Invariant 2 — V Forge Owns the Content Graph

V Forge must remain the system of record for the content graph of what was built.

The content graph includes:

- pages — the URLs and content structure of built properties
- topics — the topical vocabulary of a project
- entities — the entity vocabulary of a project
- internal links — the link structure between pages
- archetypes — the content type classification of pages
- schema usage — the structured data markup applied to pages

The content graph is execution truth because it describes what was built. It changes when V Forge does work.

V Forge must:

- own all content graph records project-scoped to the executing project
- maintain content graph integrity — no cross-project graph connections
- update the content graph as execution work builds or modifies the project
- preserve content graph history where it matters for execution continuity

VEDA must not own or store the content graph.
The content graph does not belong in the observatory — it describes internal project structure, not observed external reality.

---

## Invariant 3 — V Forge Owns Execution Intelligence

V Forge must remain the owner of the execution intelligence layer.

Execution intelligence is the analytical layer that V Forge produces by crossing the content graph against VEDA observatory signal.

This includes analysis such as:

- how built content is performing against tracked keywords
- where structural gaps exist between the content graph and SERP performance signal
- what execution-side opportunities or issues are indicated by crossing internal structure against external signal

V Forge may:

- read VEDA signal through the governed VEDA to V Forge signal interface
- cross that signal against the content graph it owns
- produce execution intelligence from that cross-referencing

V Forge must not:

- store the raw VEDA signal it consumes as canonical V Forge truth
- accumulate open-ended signal archives that duplicate VEDA's observatory function
- present execution intelligence as though VEDA produced it

The raw signal belongs to VEDA.
The execution intelligence derived from crossing signal against the content graph belongs to V Forge.

---

## Invariant 4 — V Forge Does Not Own Planning Truth

V Forge must not become the planning system of record.

V Forge may:

- execute approved work handed off from Project V
- interpret execution requirements enough to complete bounded execution correctly
- return bounded findings that require planning reconsideration
- request bounded clarification or approval through the governed path where needed

V Forge must not:

- decide project structure as canonical planning truth
- decide what should be pursued next as canonical planning truth
- own roadmap, sequencing, or orchestration truth
- silently convert execution-side findings into planning decisions

If V Forge begins acting as the planning brain of the ecosystem, the role model is failing.

---

## Invariant 5 — V Forge Does Not Own Signal or Observability Truth

V Forge must not become the signal, evidence, or observability system of record.

V Forge may:

- consume bounded signal outputs from VEDA where execution requires them
- generate bounded execution findings during approved work
- observe execution-relevant conditions enough to complete or validate approved scope

V Forge must not:

- accumulate open-ended signal ownership
- become the canonical evidence archive for ecosystem observability
- operate as a general research observatory
- replace VEDA's signal-system role through execution convenience

Execution-side findings are not a license to absorb observability ownership.
Consuming VEDA signal is not the same as owning VEDA signal.

---

## Invariant 6 — V Forge Acts Only Within Approved Execution Scope

V Forge must remain bounded by approved execution scope.

This means:

- execution begins only after governed handoff or equivalent governed authorization
- work performed must remain within the approved scope unless a governed change path is used
- scope ambiguity must not be resolved through casual self-expansion
- missing approval or missing handoff semantics must not be papered over by execution momentum

Execution energy is not approval.
Execution confidence is not scope expansion authority.

---

## Invariant 7 — Execution-Side Research Must Remain Bounded

V Forge may perform execution-side research only when that research is required to complete, validate, or safely continue approved execution.

This means:

- research must stay tied to approved scope
- research must remain execution-supporting rather than open-ended ecosystem exploration
- research findings that affect planning direction must return through governed reporting or return-to-planning paths

Where execution-side research produces findings that appear to have planning-level significance, those findings must be returned as bounded execution findings through the governed return-to-planning path, not repackaged as VEDA-equivalent signal by V Forge.

V Forge does not become VEDA when it discovers something that would normally be VEDA-originated.

---

## Invariant 8 — Content Graph Integrity Must Be Project-Scoped

Content graph records must be project-scoped and must not connect across projects.

This means:

- every content graph record belongs to exactly one project
- page-topic junctions must only connect pages and topics from the same project
- page-entity junctions must only connect pages and entities from the same project
- internal links must only connect pages from the same project
- canonical identifiers must be unique within project scope

Cross-project content graph contamination is a structural failure.

This invariant must be enforced at both:

- the application layer
- the database layer where critical integrity is at stake

---

## Invariant 9 — Handoff Does Not Blur Ownership

A valid handoff transfers execution responsibility to V Forge.
It does not transfer planning ownership into V Forge.

This means:

- V Forge owns execution truth after valid handoff
- Project V remains the owner of planning and orchestration truth
- VEDA remains the owner of signal, evidence, and observability truth
- V Forge must not treat handoff context as permission to reinterpret the ecosystem's truth boundaries

A handoff that lacks the minimum semantic content required for bounded execution must not be treated as authorization to proceed.
Missing semantics require a governed clarification or return path, not creative interpretation that expands V Forge's authority.

---

## Invariant 10 — Return-to-Planning Does Not Collapse Execution Truth

When V Forge returns bounded findings to Project V for planning reconsideration, V Forge remains the owner of execution truth.

This means:

- return-to-planning transfers bounded execution findings, not full execution ownership
- Project V may reconsider planning without becoming the execution ledger
- V Forge must preserve execution continuity and execution history even when findings return upstream
- return-to-planning must not be treated as silent execution-state deletion

Return-to-planning changes what planning may reconsider.
It does not erase who owns execution history.

---

## Invariant 11 — V Forge Must Preserve Execution Continuity

V Forge must preserve enough execution continuity that a later reader, operator, or capable LLM can determine:

- what work entered execution
- what work was actually performed
- what changed during execution
- what findings or blockers emerged
- what remained incomplete, failed, blocked, or successful
- what was returned to planning and why

At minimum, execution continuity is sufficient when a later reviewer can determine the lifecycle of each significant work unit: its entry state, its progression through execution, its final state, and its bounded findings.

An execution record that cannot answer those questions for a significant work unit is below the minimum continuity threshold.

---

## Invariant 12 — V Forge Must Preserve Boundary-Safe Reporting

V Forge must report execution outcomes and findings in a way that preserves boundary clarity.

This means:

- execution reports must remain execution-side accounts, not planning-state rewrites
- execution findings must remain bounded to what execution can honestly report
- returned findings must not be packaged as automatic planning truth mutation
- reporting must remain honest about scope, uncertainty, and whether a finding is execution-local or planning-relevant

Execution reports must preserve material uncertainty, partial completion, and ambiguity where they exist.

Reporting quality must improve ecosystem coordination without collapsing ownership.

---

## Invariant 13 — V Forge Must Remain Governed, Not Self-Authorizing

V Forge is not an unrestricted autonomous execution environment.

V Forge remains bounded by:

- actor authority
- approval posture where required
- external-action governance
- workflow stage
- handoff validity
- human-in-the-loop requirements for sensitive execution

If V Forge detects during execution that it has performed or is about to perform work exceeding approved scope, it must halt at the earliest safe stopping point, preserve the current execution state, and report the scope excess through the governed reporting path.

Mid-execution self-discovery of scope excess is not permission to continue.
It is a halt trigger.

Speed, capability, or tool access do not erase governance.

---

## Invariant 14 — External and Paid Actions Require Stronger Discipline

External-facing, launch-sensitive, or paid execution actions require stronger control discipline.

This means V Forge must not casually self-authorize:

- paid external actions
- launch-sensitive changes
- public-facing execution with material risk
- irreversible or costly external mutations

Where stronger governance is required, V Forge must stop and use the governed approval or escalation path rather than proceeding on execution momentum.

---

## Invariant 15 — Human-In-The-Loop Must Remain Real

Human review remains especially important when V Forge execution involves:

- high-risk mutations
- external paid actions
- public-facing changes
- launch-sensitive execution
- ambiguous scope interpretation
- major failure or return-to-planning conditions

LLM assistance may be heavy.
Human governance must remain real where the ecosystem requires it.

---

## Invariant 16 — V Forge Must Not Become a Shadow Project V

V Forge must not recreate Project V inside execution tooling, reporting, or convenience structures.

Forbidden shadow-Project-V behavior includes:

- building local planning-state systems for convenience
- recreating approval posture as execution-owned truth
- recreating orchestration sequencing as execution-owned truth
- turning execution work queues into canonical planning state

Execution systems may preserve execution-needed context.
They must not absorb planning ownership.

---

## Invariant 17 — V Forge Must Not Become a Shadow VEDA

V Forge must not recreate VEDA inside execution tooling, reports, or research helpers.

Forbidden shadow-VEDA behavior includes:

- storing open-ended signal history as execution-owned truth
- building execution-owned observability archives for general ecosystem use
- treating execution-side findings as a replacement for evidence-system ownership
- accumulating broad observatory context because it seems useful during execution

Execution may consume signal.
It must not become the signal system.

---

## Invariant 18 — Failure Does Not Justify Boundary Collapse

Execution failure, ambiguity, or blocked work must not be used as a reason to collapse system boundaries.

This means:

- failure does not authorize V Forge to become the planner
- failure does not authorize Project V to become the execution ledger
- failure does not authorize V Forge to become the signal system
- failure should trigger bounded reporting, return-to-planning, escalation, or governed reconsideration as appropriate

Pressure does not erase architecture.

---

## Invariant 19 — V Forge Must Remain Legible to a Capable LLM

V Forge doctrine must remain structured so that a capable LLM can reliably infer:

- what V Forge owns — execution truth, content graph, execution intelligence
- what V Forge does not own — planning truth, signal truth as a system of record
- what execution scope means
- what bounded execution-side research means
- that consuming VEDA signal does not transfer signal ownership to V Forge
- when V Forge must return findings to planning
- when V Forge must stop instead of self-authorizing further action

If a capable LLM could read V Forge as a planner, signal system, or unrestricted autonomous executor, these invariants are failing.

---

## Forbidden Drift Patterns

V Forge has drifted if it begins to function as:

- a planning system
- an orchestration brain
- a signal or observability system of record
- an unrestricted research engine
- a shadow Project V living inside execution
- a shadow VEDA living inside execution
- a self-authorizing external-action engine
- a boundary-collapsing failure-response blob
- a system that treats VEDA signal consumption as signal ownership
- a system that stores the content graph in VEDA's database or treats it as VEDA-owned

These are identity failures, not efficiency wins.

---

## Human-In-The-Loop Principle

V Forge remains valuable because it can execute effectively while staying governable.

Human review remains especially important when V Forge is involved in:

- launch-sensitive work
- major mutations
- paid external actions
- public-facing changes
- ambiguity about scope or approval
- return-to-planning conditions that may materially affect next steps

V Forge should make execution more reliable, not make governance disappear behind speed.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- V Forge owns execution truth and the content graph of what was built
- V Forge owns execution intelligence derived from crossing the content graph against VEDA signal
- V Forge does not own planning truth
- V Forge does not own signal or observability truth as a system of record
- consuming VEDA signal does not make V Forge the signal owner
- content graph records must be project-scoped — cross-project graph connections are forbidden
- execution-side research must remain bounded to approved work
- return-to-planning is a governed boundary path, not an ownership collapse
- external or paid execution may require stronger governance and human review

If an LLM could use V Forge as an all-in-one planner, signal engine, content graph owner for all systems, and executor because it seems efficient, these invariants are failing.

---

## Usage

This document should be used:

- as the non-negotiable identity constraint doc for V Forge
- when reviewing whether a new V Forge capability belongs inside V Forge at all
- when deciding whether an execution shortcut would distort V Forge's role
- when writing more specific V Forge docs so they inherit stable role constraints
- when evaluating whether V Forge is drifting toward planning, signal ownership, or uncontrolled autonomy

---

## Related Docs

- `v-forge.md`
- `operational-model.md`
- `vs-project-v.md`
- `vs-veda.md`
- `human-in-the-loop-doctrine.md`
- `reporting-and-approval-model.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/auth-and-actor-model.md`
- `../governance/external-action-governance.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/testing-and-verification-doctrine.md`
