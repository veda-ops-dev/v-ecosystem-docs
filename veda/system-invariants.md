# VEDA System Invariants

## Purpose

This document defines the non-negotiable invariants that must remain true for VEDA to remain VEDA inside the V Ecosystem.

It exists to answer:

```text
What must always remain true about VEDA's role, ownership, behavior, and boundaries so that VEDA does not drift into planning ownership, execution ownership, content modeling, or general-purpose system sprawl?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the non-negotiable invariants of VEDA
- what VEDA must continue to own
- what VEDA must not become
- what observatory model traits must remain true
- what kinds of drift are forbidden even if they seem operationally convenient
- how VEDA must relate to governance, interfaces, workflows, and neighboring systems

---

## Out of Scope

This document does not define:

- detailed schema design for every VEDA model
- detailed provider-specific ingest mechanics
- detailed UI or operator-surface design
- detailed search-intelligence implementation internals
- detailed MCP surface behavior
- detailed deployment and hosting selection

Those belong in more specific VEDA, interface, workflow, or implementation docs.

---

## System

- veda

---

## Core Rule

VEDA must remain a pure observatory.

It must not drift into planning ownership, execution ownership, content graph ownership, intelligence synthesis, or a convenience-blob meta-system that absorbs responsibilities from neighboring systems.

If a design change makes VEDA easier to use by weakening those invariants, the design change is wrong.

---

## Invariant Definition

A VEDA invariant is a condition that must remain true for VEDA to preserve its identity, authority, and ecosystem fit.

An invariant is not a preference.
It is not a local implementation convenience.
It is a constraint that protects the role VEDA plays in the wider ecosystem.

If an implementation, workflow, or operational shortcut violates a VEDA invariant, the shortcut must not be normalized.

When a proposed design change, implementation, or operational shortcut would violate a VEDA invariant, the correct response is to stop, surface the conflict explicitly, and escalate or redesign through a governed architecture path.
Invariant violations that are temporarily normalized for operational reasons become permanent drift.

---

## Invariant 1 — VEDA Owns External Observatory Truth Only

VEDA must remain the system of record for observed external reality relevant to the ecosystem.

VEDA owns:

- SERP data and keyword intelligence
- search volatility, intent drift, and change classification
- Google Analytics 4 performance observations
- Google Search Console indexation and performance observations
- YouTube search and channel observatory data
- source capture and source item ingestion
- observatory event log
- external provider data ingestion pipelines
- signal packages produced from observatory records for ecosystem consumption

VEDA does not own:

- the content graph of what was built — that belongs to V Forge
- planning truth — that belongs to Project V
- execution truth — that belongs to V Forge
- intelligence derived from internal project structure
- proposals for what should be built next

If another system becomes the canonical owner of VEDA's observatory domains, VEDA has been displaced.
If VEDA begins owning domains outside this list, VEDA has drifted.

---

## Invariant 2 — VEDA Is Observatory-Only

VEDA must remain observatory-only.

Its valid model pattern is:

```text
entity + observation + time + interpretation
```

A capability that cannot be explained in those terms is presumptively out of bounds for VEDA until classified otherwise through governed architecture work.

The telescope mental model applies: if a telescope would not do it, VEDA should not do it.

Observatory sophistication does not justify ownership expansion.

---

## Invariant 3 — VEDA Does Not Own Planning Truth

VEDA must not become the planning system of record.

VEDA may:

- supply governed signal to Project V
- preserve evidence relevant to planning
- produce diagnostics and interpretation that may inform planning

VEDA must not:

- own project planning state
- own roadmap or orchestration truth
- decide what should happen next as canonical planning truth
- silently convert observatory interpretation into planning decisions

If VEDA begins acting as the planning brain of the ecosystem, the role model is failing.

---

## Invariant 4 — VEDA Does Not Own Execution Truth

VEDA must not become the execution system of record.

VEDA may:

- observe execution-relevant external outcomes where they appear as observable reality
- preserve evidence and signals that matter to execution review
- return findings or signal that may influence planning or execution governance through the governed paths

VEDA must not:

- become the canonical execution ledger
- own production workflow state
- own draft or publishing workflow state
- treat execution activity as though it were observatory truth by default

Observed execution-adjacent reality is not the same as owning execution truth.

---

## Invariant 5 — VEDA Does Not Own the Content Graph

The content graph — the structural model of what a project has built — belongs to V Forge.

VEDA must not:

- own, store, or maintain the content graph as canonical truth
- model internal project structure as an observatory concern
- treat pages, topics, entities, internal links, or archetypes as VEDA-owned records
- use observatory language to justify content graph ownership

V Forge owns what was built.
VEDA observes what external reality shows about what was built.
Those are different things.

---

## Invariant 6 — VEDA Brain Does Not Exist

VEDA does not have an intelligence synthesis layer.

There is no VEDA Brain in this ecosystem.

Intelligence synthesis that was previously attributed to VEDA Brain is split cleanly:

- pre-build market opportunity analysis belongs to Project V's planning intelligence layer
- post-build content performance gap analysis belongs to V Forge's execution intelligence layer

VEDA must not:

- generate planning proposals
- generate content gap analysis
- synthesize cross-system intelligence as though it were an observatory output
- recreate VEDA Brain under any other name

If a capability sounds like VEDA Brain, it belongs in Project V or V Forge, not in VEDA.

---

## Invariant 7 — VEDA Preserves Project-Scoped Isolation

VEDA must preserve project-scoped isolation as a structural rule, not a courtesy.

This means:

- observatory rows are project-scoped unless intentionally global
- reads and writes must enforce project ownership
- project existence leakage across boundaries must not be normalized

Cross-project contamination is a system failure, not a minor hygiene issue.

---

## Invariant 8 — VEDA Preserves Time-Aware Observability

Time must remain first-class where observation history matters.

VEDA observatory records fall into two distinct time-handling patterns:

- governance records, such as monitoring targets and bounded configuration objects, may be updated over time
- observation records, such as snapshot captures, performance captures, and event logs, are append-friendly and must not have their historical state silently overwritten

A new observation about the same entity is a new record, not an update to the prior record.

An observability system that forgets time becomes a convenience cache, not a trustworthy observatory.

---

## Invariant 9 — VEDA Preserves Evidence Before Interpretation

VEDA may derive interpretation, diagnostics, summaries, and operator-facing intelligence from observatory records.

But VEDA must preserve the distinction between:

- observed evidence
- derived interpretation
- advisory output
- planning decision
- execution action

Interpretation may grow on top of evidence.
It must not replace evidence as canonical truth.

Signal and evidence produced by VEDA must preserve source provenance and trust-relevant metadata.
Source provenance is part of evidence integrity, not an implementation detail.

---

## Invariant 10 — VEDA Must Prefer Explicit Schema Over JSON Sludge

VEDA may store raw provider payloads and other bounded variable-shape evidence where justified.

VEDA must not:

- use JSON as a substitute for unresolved schema design
- hide hot-path logic fields inside flexible blobs because it is convenient
- use JSON to smuggle planning or execution state into observatory storage

Fields used for querying, filtering, validation, or stable system logic must be promoted into explicit structure.

---

## Invariant 11 — VEDA Preserves Event Auditability Where Required

Where observatory state changes require durable auditability, VEDA must preserve canonical event history.

This means:

- event logs remain append-only
- state-change events remain observatory-scoped
- event vocabulary remains bounded and meaningful
- evented state changes must remain attributable and time-aware
- read-only operations must not emit state-change event log entries

An observability system that cannot explain what changed, when, and under whose action is not governed strongly enough.

---

## Invariant 12 — VEDA Preserves Transaction Integrity for Multi-Write Mutations

Any operation that changes persisted state across multiple writes must remain transaction-safe.

This means:

- partial multi-write persistence is forbidden
- required event logging and required state changes must remain atomic when both are required
- rollback posture must remain real, not assumed
- event log entries required by a state-change mutation must be written inside the same transaction as that state change

If VEDA can leave behind partial observatory state after mutation failure, the trust model is broken.

---

## Invariant 13 — VEDA Must Keep Search Intelligence Derived, Not Sovereign

VEDA may produce search diagnostics, volatility interpretation, event timelines, causality summaries, and operator-facing search intelligence.

VEDA must not let the search-intelligence layer become:

- a second canonical truth store
- a planning engine in disguise
- a hidden write path
- a strategy blob that self-authorizes downstream changes

Search intelligence is derived from observatory truth.
It does not replace observatory truth or planning governance.

---

## Invariant 14 — VEDA Must Remain Governed, Not Self-Authorizing

VEDA is not a self-authorizing system sovereign.

VEDA remains bounded by:

- actor authority
- approval posture where relevant
- reporting requirements
- cross-system boundaries
- workflow stage
- human-in-the-loop governance

Diagnostics, evidence quality, or model sophistication do not erase governance.

---

## Invariant 15 — VEDA Must Preserve Deterministic Retrieval and Reproducibility

VEDA must prefer deterministic retrieval and reproducible interpretation.

This means:

- explicit ordering must be used where result order matters
- stable tie-breakers must exist where needed
- validation must be deterministic and reproducible
- interpretation layers should prefer reproducible truth over unstable cleverness

If the same query against the same state produces different observatory meaning without an explicit reason, VEDA has degraded.

---

## Invariant 16 — VEDA Must Not Normalize Convenience Drift

VEDA must not absorb neighboring responsibilities merely because doing so seems operationally easier.

Forbidden convenience drift includes:

- storing planning truth because it helps operators think faster
- storing execution workflow state because it helps dashboards look complete
- storing the content graph because it was previously owned here
- storing strategic conclusions as though they were observations
- turning global config or JSON payloads into junk drawers for unclassified system truth
- using observatory language to justify role expansion

Convenience is not ownership.
Convenience is not invariance.

---

## Invariant 17 — VEDA Must Remain Legible to a Capable LLM

VEDA doctrine must remain structured so that a capable LLM can reliably infer:

- what VEDA owns — external observatory truth only
- what VEDA does not own — planning truth, execution truth, content graph, intelligence synthesis
- what counts as observatory truth
- what is derived from observatory truth
- what may cross into Project V or V Forge and how
- when VEDA must stay bounded instead of acting like a planner or executor

If a capable LLM could read VEDA as a generic intelligence layer that is free to mutate planning or execution truth, or that owns the content graph, these invariants are failing.

---

## Forbidden Drift Patterns

VEDA has drifted if it begins to function as:

- a planning system
- an execution ledger
- a content graph owner
- an intelligence synthesis layer
- a proposal engine
- a publishing workflow engine
- a draft or revision manager
- a strategic blob that stores conclusions instead of evidence
- a cross-project observability swamp
- a JSON junk drawer for unclassified truth
- a second canonical truth store above its own observatory records
- a recreation of VEDA Brain under any name

These are identity failures, not efficiency wins.

---

## Human-In-The-Loop Principle

VEDA remains valuable because it helps preserve signal, evidence, and observability truth without replacing governed human judgment.

Human review remains especially important when VEDA is involved in:

- introducing a new observatory domain
- adding a new external data provider
- changing event vocabulary
- changing project isolation or integrity rules
- changing what counts as canonical observatory truth
- changing cross-system signal packaging behavior

VEDA should make observability more trustworthy, not turn human governance into post-hoc spectatorship.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- VEDA owns external observatory truth only
- VEDA is observatory-only — the telescope, not the analyst
- VEDA does not own planning truth, execution truth, or the content graph
- VEDA Brain does not exist — intelligence synthesis belongs to Project V and V Forge
- evidence and interpretation must remain distinct
- observatory models must stay project-scoped, time-aware, and structurally sound
- event auditability and transaction integrity matter

If an LLM could use VEDA as an all-in-one planning, execution, content modeling, and observability layer because it seems efficient, these invariants are failing.

---

## Usage

This document should be used:

- as the non-negotiable identity constraint doc for VEDA
- when reviewing whether a new VEDA capability belongs inside VEDA at all
- when deciding whether an implementation shortcut would distort observatory ownership
- when writing more specific VEDA docs so they inherit stable role constraints
- when evaluating whether interpretation layers are eroding evidence-first discipline

---

## Related Docs

- `veda.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `data-boundaries.md`
- `operator-surfaces.md`
- `mcp-surface.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../governance/auth-and-actor-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/testing-and-verification-doctrine.md`
