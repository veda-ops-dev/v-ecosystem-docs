# VEDA Strategy

## Purpose

This document defines what VEDA Strategy is inside the V Ecosystem.

It exists to answer:

```text
What role does VEDA Strategy play in the V Ecosystem, what truth does it own,
and how should VEDA Strategy be understood by operators and LLMs?
```

This is a Tier 2 system core authority document.

---

## Scope

This document governs:

- the identity of VEDA Strategy
- the role VEDA Strategy plays in the ecosystem
- the kinds of truth VEDA Strategy owns
- the high-level boundary between VEDA Strategy and other systems
- the default mental model used when classifying VEDA Strategy behavior

---

## Out of Scope

This document does not define:

- detailed VEDA Strategy workflows
- detailed schema design
- detailed interface contracts
- detailed governance rules
- implementation details

Those belong in more specific VEDA Strategy, interface, workflow, or governance docs.

---

## System

- veda_strategy

---

## Core Rule

VEDA Strategy is the derived strategic intelligence system of the V Ecosystem.

VEDA Strategy exists to read VEDA's observatory truth and derive bounded strategic
intelligence from it — scoring, gap detection, clustering, and competitive analysis —
so that Project V and V Forge can make better-informed decisions.

VEDA Strategy does not own observatory truth.
VEDA Strategy does not make planning decisions.
VEDA Strategy does not issue execution instructions.

VEDA Strategy derives and signals. That is its complete role.

---

## VEDA Strategy Definition

VEDA Strategy is the system used to transform raw observatory truth from VEDA into
bounded strategic intelligence that other systems may act on.

It turns VEDA observatory inputs into:

- opportunity scores
- content gap signals at the strategic level
- clustering outputs
- competitive analysis records
- strategic signal packages for Project V and V Forge

VEDA Strategy is not the observatory.
VEDA Strategy is not the planner.
VEDA Strategy is not the executor.
VEDA Strategy does not own the signal it reads from VEDA.
VEDA Strategy does not replace Project V's planning authority.
VEDA Strategy does not replace V Forge's execution authority.

---

## Owns

VEDA Strategy owns:

- opportunity scoring records derived from VEDA observatory truth
- content gap detection records at the strategic level
- clustering records
- competitive analysis records
- strategic signal packages produced for Project V and V Forge

### Explanation
VEDA Strategy owns the derived intelligence layer that sits between raw observatory
truth and planning or execution decisions. Every capability VEDA Strategy owns is
grounded in deriving meaning from VEDA's observations — not in making observations
itself, and not in making the planning or execution decisions that follow.

---

## Does Not Own

VEDA Strategy does not own:

- observatory truth — that belongs to VEDA
- raw signal, SERP data, GA4 data, or Search Console data — those belong to VEDA
- planning truth — that belongs to Project V
- orchestration truth — that belongs to Project V
- readiness truth — that belongs to Project V
- execution truth — that belongs to V Forge
- the content graph of what was built — that belongs to V Forge
- planning decisions or execution decisions

### Explanation
VEDA Strategy reads VEDA. It does not replace VEDA.
VEDA Strategy signals Project V. It does not replace Project V.
VEDA Strategy signals V Forge. It does not replace V Forge.

Deriving intelligence from observatory truth is not the same as owning that truth.
Signaling a planning opportunity is not the same as making a planning decision.
Signaling an execution condition is not the same as issuing an execution instruction.

---

## Main Ecosystem Relationships

### Relationship to VEDA
VEDA Strategy reads VEDA's observatory truth to produce derived strategic intelligence.

VEDA remains the canonical owner of all observatory records. VEDA Strategy consumes
bounded outputs from VEDA's governed interfaces. It does not acquire ownership of
those records by reading them.

VEDA Strategy must not accumulate VEDA's canonical observatory records in its own
schema. It must not behave as a second observatory. It reads from `veda.*`; it
writes derived intelligence into `veda_strategy.*`.

### Relationship to Project V
VEDA Strategy signals Project V when scored opportunities, gap detections, or
competitive conditions warrant planning consideration.

Project V receives those signals as inputs to planning evaluation. Project V
remains the planning system of record. It decides what to do with the strategic
signals VEDA Strategy provides. VEDA Strategy does not make that decision.

The governed signal path from VEDA Strategy to Project V is defined in
`../interfaces/veda-strategy-to-project-v-signal-interface.md`.

### Relationship to V Forge
VEDA Strategy signals V Forge when in-scope optimization or execution-relevant
strategic conditions are identified.

V Forge receives those signals as inputs to execution intelligence. V Forge remains
the execution system of record. It decides what to do with the strategic signals
VEDA Strategy provides. VEDA Strategy does not make that decision.

The governed signal path from VEDA Strategy to V Forge is defined in
`../interfaces/veda-strategy-to-v-forge-signal-interface.md`.

---

## Responsibility Model

VEDA Strategy is responsible for:

- reading VEDA observatory truth through governed interfaces
- deriving bounded strategic intelligence from that truth
- producing opportunity scores, gap signals, clustering outputs, and competitive
  analysis records in `veda_strategy.*`
- packaging strategic signal for Project V and V Forge through governed interfaces
- preserving the derivation basis so signals remain traceable to observatory evidence

VEDA Strategy is not responsible for:

- gathering or owning observatory truth — that is VEDA's role
- deciding what projects should be built — that is Project V's role
- deciding what execution work should be done — that is Project V and V Forge's role
- owning planning or execution decisions that result from its signals

---

## Human-In-The-Loop Principle

VEDA Strategy is a governed derived intelligence system.

Human review and direction remain especially important for:

- changes to scoring models or evaluation dimensions
- changes to what strategic signals are produced and sent
- decisions about whether a strategic signal warrants project creation
- doctrine changes affecting VEDA Strategy's scope or boundary

VEDA Strategy may be heavily LLM-assisted, but its strategic outputs inform
human-governed planning and execution decisions. It does not replace that governance.

---

## LLM Use Principle

A capable LLM should be able to infer from the VEDA Strategy docs that:

- VEDA Strategy reads observatory truth and derives intelligence — it does not own either
- VEDA Strategy signals Project V and V Forge — it does not command them
- VEDA Strategy is distinct from VEDA (which observes), Project V (which plans),
  and V Forge (which executes)
- deriving strategic intelligence from signal is not the same as owning the signal
- signaling an opportunity is not the same as creating a project

If the docs allow VEDA Strategy to drift toward becoming a second observatory,
an autonomous planner, or an execution controller, the VEDA Strategy doctrine is wrong.

---

## Usage

This document should be used:

- as the first identity doc for VEDA Strategy in the shared root
- as the top-level VEDA Strategy role definition for operators and LLMs
- as a boundary reference when writing more specific VEDA Strategy docs
- as a check against future drift in VEDA Strategy design or implementation

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/ecosystem-schema-spine.md`
- `data-boundaries.md`
- `schema-authority.md`
- `../veda/veda.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
- `../interfaces/veda-strategy-to-project-v-signal-interface.md`
- `../interfaces/veda-strategy-to-v-forge-signal-interface.md`
