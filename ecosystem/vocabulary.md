# Vocabulary (Canonical Terms)

## Purpose

This document defines controlled, load-bearing terms for the V Ecosystem.

It exists to answer:

```text
Which terms must be used consistently across the V Ecosystem docs so LLM drift stays low and authority remains clear?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- canonical terminology for the V Ecosystem
- load-bearing terms that should not drift across docs
- the default meaning of shared ecosystem terms

---

## Out of Scope

This document does not define:

- project-specific internal field names unless they are ecosystem-relevant
- implementation-specific naming decisions that do not affect doctrine
- historical terminology except where needed to prevent confusion

---

## System

- ecosystem

---

## Core Rule

If a term is load-bearing, it should mean one thing.

Do not casually introduce synonyms for canonical terms.
If a new load-bearing term is needed, add it here before it spreads across active docs.

---

## Canonical Terms

## Project V
Planning and orchestration system of record.

## VEDA
The pure observatory of the V Ecosystem. VEDA observes external reality, records what it sees, and preserves that record faithfully. VEDA does not plan, propose, execute, or model internal project structure.

## V Forge
Execution system of record. V Forge carries out approved work, owns the content graph of what was built, and produces execution intelligence by crossing the content graph against VEDA signal.

## Observatory
The role and mental model that defines VEDA's purpose. An observatory watches and records. It does not interpret on behalf of the ecosystem. It does not model what was built internally. It does not propose what should be built next.

The canonical mental model: a telescope does not measure planetary distance. It observes. Measurement and interpretation happen elsewhere, by other systems, using what the telescope saw. VEDA is the telescope.

If a proposed capability cannot be described as something a telescope does, it does not belong in VEDA.

## Content Graph
The structural model of what a project has built — pages, topics, entities, internal links, archetypes, and schema usage. The content graph is execution truth. It belongs to V Forge because it describes what was built, not what was observed externally. The content graph changes when V Forge does work.

The content graph does not belong in VEDA. VEDA observes external reality. The content graph is a record of internal project structure.

## Execution Intelligence
The analysis layer owned by V Forge that cross-references the content graph against VEDA observatory signal to answer: how is what we built performing, and where are the execution-side gaps. This is a V Forge capability, not a VEDA capability. VEDA provides the raw signal. V Forge does the cross-referencing.

## Planning Intelligence
The analysis layer owned by Project V that interprets VEDA market signal to answer: what opportunities exist, what does the external market show, and what is worth pursuing. This is a Project V capability. VEDA provides the raw market signal. Project V does the interpretation for planning purposes.

## Handoff
A structured transfer from Project V to V Forge.
A handoff transfers execution responsibility without transferring planning ownership.

## Execution Responsibility
The obligation to carry out approved work, produce execution outputs, preserve execution truth, and report execution outcomes and findings.
Execution responsibility is transferred via handoff.
Planning ownership is not.

## Signal
Observable evidence or data organized by VEDA that may matter to the ecosystem.
A signal is not automatically a decision, plan, or execution instruction.
Signal provision is not the same as signal authority.
VEDA organizes signal from external reality. VEDA does not produce outcomes — it records observations.

## Evidence
Any input used to inform, support, or justify a governing decision, planning record, observatory finding, or operational judgment.

Signal often becomes evidence when it is used in a governed decision or review context, but signal and evidence are not identical terms.
Signal is VEDA-organized observable data. Evidence is the broader support basis used when something is being evaluated, justified, or decided.

## Findings
Bounded execution-side outputs produced by V Forge during approved work, returned to the ecosystem for review, replanning, reporting, or archival.
Findings are not VEDA signal or evidence unless they are explicitly processed through the appropriate signal or evidence interface.

## Decision
A formalized choice recorded in a durable decision record or ADR.
A decision is stronger than a recommendation or discussion note.

## ADR (Architecture Decision Record)
A documented, durable decision that affects system behavior, structure, or doctrine.

## Invariant
A condition that must remain true for a system to preserve its identity, authority, and ecosystem fit.
An invariant is not a preference or a local convenience.
It is a constraint that protects the system's role in the wider ecosystem.

## Authority
A document or system that defines behavior, constraints, ownership, or rules that other docs or systems are expected to follow.

## Archive
Non-authoritative historical material kept for provenance, source reference, or migration history.
Archive material must not be treated as current doctrine.

## Bounded
Constrained by explicit scope, ownership, interface rules, approval rules, or authority rules.
If something is bounded, it must not expand casually outside those limits.

## Tier 1 Authority Document
A top-level ecosystem authority document.
These docs define cross-system identity, boundaries, governance, shared vocabulary, shared rules, or shared doctrine for the V Ecosystem as a whole.

## Tier 2 Authority Document
A system-specific authority document.
These docs inherit from Tier 1 ecosystem law and define identity, boundaries, invariants, and rules within the scope of one ecosystem system such as Project V, VEDA, or V Forge.

## External Data Provider
Any external service, API, or data source that the ecosystem integrates with to supply observatory inputs, execution tooling, or planning-support data. External data providers must be integrated through governed patterns defined in `external-provider-integration-doctrine.md`. Adding a new external data provider is a governed architecture event, not a casual implementation choice.

## Hammer
The invariant verification layer used to confirm that a system's behavioral invariants hold under real execution. Every system in the V Ecosystem must implement its own hammer layer adapted to its own surfaces and invariants. The hammer is not a unit test suite or a code coverage tool. It is a boundary and invariant verification system.

## BYDA
The audit methodology used inside Project V for structured planning, readiness, and implementation-oriented evaluation.

BYDA is a Project V method rather than a whole-ecosystem peer system, but it is referenced broadly enough that it needs a canonical vocabulary anchor. See `../project-v/byda-in-project-v.md` for the full Project V-specific posture.

---

## Desktop Runtime Vocabulary

The terms below are load-bearing for desktop/runtime doctrine and implementation work.
They are part of the ecosystem vocabulary set, but they are usually only needed when working on the unified Tauri 2 desktop application and its runtime behavior.

## Session Token
An opaque, server-side-bound identifier that represents an active MCP session scoped to a specific project.

The session token is created by the MCP server when the operator selects a project in the desktop application. It binds the session to the selected project UUID server-side. The LLM never sees the project UUID — it only sees the opaque session token. All MCP tool calls within the session automatically inherit the project scope bound to the token.

The session token is not a credential. It is a project scope binding mechanism. It does not grant access beyond what the underlying API already permits for the scoped project.

## Agent Orchestrator
The desktop runtime role that coordinates bounded session behavior, delegated subtasks, runtime continuity, and tool-surface assembly without becoming a new truth-owning system.

An agent orchestrator is a runtime coordinator, not a peer ecosystem system and not an approval authority.

## Specialist Agent
A bounded delegated runtime worker used for narrowly scoped reasoning or packaging work inside the desktop runtime.

A specialist agent may increase reasoning specialization.
It does not gain independent governance authority, project authority, or system ownership by virtue of specialization.

## Delegated Subtask
A bounded runtime task delegated by the desktop orchestrator to a specialist agent or equivalent worker.

A delegated subtask inherits the parent session scope and constraints.
It does not create a new approval path or a new authority domain.

## Session Tool Surface
The governed set of MCP tools and related runtime capabilities exposed to the LLM for the active session.

The session tool surface is assembled from admitted system surfaces according to current system posture, project scope, and governance constraints.
The LLM must not be shown tools it is not currently entitled to use.

## Protected Context
The categories of session context that must not be dropped, obscured, or casually compacted because they are required to preserve correct governed behavior.

Protected context includes the items defined in the desktop state and continuity doctrine such as current-system posture, active approval state, decision continuity context, evidence basis markers, and session integrity items.

## Working Memory
Non-canonical runtime continuity context used to preserve useful operational understanding across turns or compaction events inside the desktop runtime.

Working memory is not system truth.
It must remain visible, bounded, and subordinate to canonical governed records.

## Durable Memory
A longer-lived form of non-canonical runtime continuity context retained beyond the immediately active turn window.

Durable memory may improve continuity across longer sessions or controlled resume flows.
It is still not canonical authority and must never override governed system state.

## Transcript Artifact
A persisted runtime record of session interaction, tool use, compaction events, or delegated work used for audit, review, or continuity support.

A transcript artifact is not a governing decision record and must not be treated as canonical system truth.

## Compact Boundary
An explicit runtime marker showing where prior conversation context was compacted and replaced by governed continuity artifacts such as preserved protected context, memory records, or structured compaction products.

A compact boundary improves visibility into what the LLM currently sees.
It does not convert compaction output into canonical authority.

## System Init Message
The structured runtime context assembled at session start to communicate the active system posture, scope, tool surface, constraints, and other admitted context to the LLM.

The system init message is a runtime assembly product. It must reflect current governed state and must not be ad-hoc or stale.

## Orchestration Event Log
The runtime record of orchestration activity such as task creation, delegation, completion, cancellation, failure, compaction events, and continuity events.

The orchestration event log supports reviewability and operator visibility. It does not replace canonical system records.

---

## Usage

This document should be used:

- when choosing terms for new docs
- when tightening ambiguous wording
- when checking whether two docs are using the same term differently
- when reviewing docs for LLM drift risk
- when a new load-bearing term emerges and needs to be locked before it spreads

---

## Related Docs

- `v-ecosystem-overview.md`
- `cross-system-boundaries.md`
- `doc-template.md`
- `external-provider-integration-doctrine.md`
- `doctrine-vs-operational-state.md`
- `../governance/testing-and-verification-doctrine.md`
- `../interfaces/mcp-coordination-model.md`
