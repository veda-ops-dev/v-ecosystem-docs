# Cross-System Data Boundaries

## Purpose

This document defines the data boundary posture across the V Ecosystem at the
cross-system level.

It exists to answer:

```text
Which system owns which data canonically, what may one system read or reference
from another system without owning it, what cross-system data access is forbidden,
and how does the data boundary model protect system ownership from persistence-layer blur?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- canonical data ownership at the cross-system level
- what cross-system data reading and referencing is allowed
- what cross-system data mutation is forbidden
- how infrastructure proximity or shared clusters must not be used to erase ownership
- the boundary posture operators, agents, and LLMs must preserve when data crosses
  or could cross system lines
- the relationship between this interface-level doc and the system-specific
  data boundary docs

---

## Out of Scope

This document does not define:

- the internal data models or schemas of each system
- the detailed implementation of each system's database tables or collections
- provider-specific data formats or ingest mechanics
- migration or infrastructure configuration specifics

Those belong in system-specific data boundary docs, schema authority docs,
and the ecosystem db-posture doc.

---

## System

- interfaces

---

## Core Rule

Data ownership follows system role.

The system that owns a category of truth is the canonical owner of the data
that represents that truth. Other systems may consume bounded outputs from
the owning system but do not thereby become owners of the underlying data.

Infrastructure proximity does not transfer ownership.
Two systems sharing a cluster or physical infrastructure do not share canonical
data ownership.
Direct database access across system lines is forbidden.
All cross-system data access goes through the governing API.

ADR-009 (no direct database access) is the architectural decision that enforces
this model. The enforcement model is defined in `../interfaces/mcp-coordination-model.md`.

---

## Canonical Data Ownership Map

### Project V owns canonically:
- project records and project metadata
- planning decision records and ADRs within project scope
- readiness evaluation records
- handoff records
- intake outcome records
- orchestration state and lifecycle state
- BYDA audit run records and audit gap records
- planning-side traceability records
- multi-project portfolio state

### VEDA owns canonically:
- observatory event records and observation history
- SERP data, keyword intelligence, and ranking records
- GA4 performance observation records
- Search Console indexation and coverage records
- YouTube observatory records
- source capture records and source items
- evidence provenance records
- provider integration configuration and ingest pipeline records
- signal packages produced from observatory records

### V Forge owns canonically:
- execution records and execution lifecycle state
- content graph records — pages, topics, entities, internal links, archetypes, schema usage
- execution intelligence records — cross-referencing outputs of content graph against VEDA signal
- bounded execution findings records
- maintenance execution records
- execution-side reporting records

---

## What Each System May Reference Without Owning

### Project V may reference:
- bounded VEDA signal packages received through the VEDA to Project V signal interface
- bounded execution findings received through the V Forge return-to-planning interface
- thin external linkage records used for planning-side traceability (not canonical execution state)

Project V must not store richer or more authoritative copies of VEDA evidence records
or V Forge execution records than what is required for planning-side traceability.

### VEDA may reference:
- project identifiers from Project V to scope observatory targets to specific projects
- configuration direction from Project V or operators about what to watch

VEDA must not store planning state, execution state, or content graph data.

### V Forge may reference:
- bounded VEDA signal packages received through the VEDA to V Forge signal interface
  for use in execution intelligence
- handoff package content received from Project V to define execution scope and constraints
- the bounded planning context included in the handoff

V Forge must not store richer or more authoritative copies of VEDA signal records
than what is consumed for execution intelligence.
V Forge must not store Project V planning records as though they are execution records.

---

## Forbidden Cross-System Data Patterns

The following are forbidden regardless of technical feasibility or operational convenience.

### Direct cross-system database access
No system may query another system's database directly.
All cross-system data access must go through the governing API.
Shared infrastructure does not grant database-level access rights.

### Cross-system canonical ownership duplication
No system may store a richer or more authoritative copy of another system's
canonical data as though it becomes the owner of that data.
A planning-side reference to a VEDA evidence record is a reference, not a duplicate.
A V Forge reference to a VEDA signal package is a consumed input, not an observatory record.

### Content graph in VEDA
VEDA must not store or maintain a model of what V Forge has built.
The content graph is execution truth. It belongs to V Forge.
This is governed by ADR-002 (content graph moves to V Forge).

### Planning records in V Forge
V Forge must not store or maintain Project V planning state as though it were
an execution-side canonical record.
V Forge receives handoff packages. It does not absorb planning ownership.

### Signal or evidence creation in Project V or V Forge
Neither Project V nor V Forge may produce observatory records or evidence records
as though they were VEDA.
Signal originates from VEDA's observatory. Other systems receive and interpret
bounded outputs. They do not generate observatory truth.

### Cross-system mutation outside interfaces
A system may not mutate another system's canonical data through any path
other than the governed API.
This includes shared storage paths, shared job queues, or shared infrastructure
access that bypasses the API enforcement layer.

---

## Persistence-Layer Ownership Rule

Even when systems share physical or logical infrastructure — a shared database cluster,
a shared hosting environment, or shared storage — logical ownership boundaries must
still be enforced through:

- separate databases or schemas per system
- API-layer enforcement that prevents cross-schema direct access
- no shared tables that mix canonical data from two systems
- governed interface-only cross-system reads

Infrastructure convenience must not redefine logical data ownership.

The ecosystem database posture is defined in:
`../ecosystem/db-posture.md`

---

## Cross-System Read Principle

A system reading data from another system through the governed API receives
a bounded output of the owning system's canonical data.

That read:
- does not make the reading system an owner of the data
- does not give the reading system the right to mutate the source data
- does not mean the reading system's local copy is authoritative

If the reading system needs to store the received data locally for operational
purposes, that local copy is a derivative reference, not a competing canonical record.

---

## Interface-Enforcement Principle

Cross-system data exchange must happen through governed interfaces. The governed
interface set is not static — it expands as the ecosystem matures.

### Primary interfaces (fully defined)

- VEDA signal to Project V: `veda-to-project-v-signal-interface.md`
- VEDA signal to V Forge: `veda-to-v-forge-signal-interface.md`
- Project V handoff to V Forge: `project-v-to-v-forge-handoff-interface.md`
- V Forge return to Project V: `v-forge-to-project-v-return-to-planning-interface.md`

### Additional governed interfaces (stub-level, ungated)

The following interfaces have been established as governed paths and have stub
documents. They are not yet full implementation contracts but are part of the
governed interface set:

- Project V execution clarification to V Forge: `project-v-to-v-forge-execution-clarification-interface.md`
- Project V handoff recall: `project-v-handoff-recall-interface.md`
- Project V scope update to V Forge after replanning: `project-v-to-v-forge-scope-update-interface.md`
- Project V bounded evidence request to VEDA: `project-v-to-veda-evidence-request-interface.md`

### Additional governed interfaces (gated — pending artifact creation)

The following interface path is required by the ecosystem but does not yet have
a governing interface document:

- Operator → VEDA observatory scope expansion

The routing decision for observatory scope expansion is settled: direct
`V Forge → VEDA` scope expansion is not the governed path. If V Forge identifies
a signal need that VEDA is not currently providing, the correct path is to surface
that need through the governed return-to-planning interface to Project V, and for
the operator to direct VEDA to expand observatory scope through the governed
operator surface. V Forge must not build independent observatory capability or
self-authorize scope expansion.

The missing artifact is the operator-mediated interface governing how operators
(or operator-facing authorities) direct VEDA to adjust observatory scope. That
interface has not yet been created. Do not create `v-forge-to-veda-*` interfaces
for this purpose — the initiating authority is the operator, not V Forge.

Data that crosses system lines outside the interfaces listed above is crossing
outside governed exchange. It must not be treated as equivalent to a governed
interface exchange.

As new interfaces are created and architectural decisions resolved, this section
must be updated to reflect the current governed set.

---

## Agent and LLM Posture

Agents must not blur data ownership when handling cross-system data.

This means agents must not:
- present a planning-side reference to VEDA evidence as though it is the VEDA record itself
- treat a V Forge-summarized version of VEDA signal as equivalent to the VEDA source
- store cross-system data in one system's context in a way that makes it appear canonical
- mutate one system's data records from within another system's session context

The allowed agent actions matrix is defined in:
`../governance/allowed-agent-actions-matrix.md`

---

## Human-In-The-Loop Principle

Clear data boundaries protect meaningful human oversight.

When data ownership is blurry:
- approvals become harder to attribute correctly
- reports become ambiguous about which system's truth is being presented
- replanning may act on the wrong system's records
- audit and review cannot reconstruct what happened

Operators must not approve actions that blur data ownership as a convenience.
If an action would cause one system to store another system's canonical data,
that action must be reconsidered through the boundary posture, not approved as expedient.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- data ownership follows system role and does not shift through reading or referencing
- cross-system data access goes through APIs, never through direct database access
- a planning-side reference to VEDA evidence is a reference, not ownership
- infrastructure proximity does not grant data access rights
- forbidden cross-system data patterns must not be rationalized as operationally convenient

If an implementation creates shared tables, direct cross-schema access, or richer
local duplicates that compete with the owning system's canonical records, this
doctrine is failing.

---

## Usage

This document should be used:

- when designing cross-system data flows and confirming they go through governed interfaces
- when reviewing whether a proposed storage pattern creates ownership blur
- when evaluating whether two systems are accidentally sharing canonical data
- when writing system-specific data boundary docs that must be consistent with
  this cross-system posture
- when auditing whether infrastructure-level decisions are respecting logical ownership

---

## Related Docs

- `mcp-coordination-model.md`
- `veda-to-project-v-signal-interface.md`
- `veda-to-v-forge-signal-interface.md`
- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `../ecosystem/db-posture.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/data-boundaries.md`
- `../veda/data-boundaries.md`
- `../governance/allowed-agent-actions-matrix.md`
