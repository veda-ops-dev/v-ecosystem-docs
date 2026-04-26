# VEDA

## Purpose

This document defines what VEDA is inside the V Ecosystem.

It exists to answer:

```text
What role does VEDA play in the V Ecosystem, what truth does it own, and how should VEDA be understood by operators and LLMs?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the identity of VEDA
- the role VEDA plays in the ecosystem
- the kinds of truth VEDA owns
- the high-level boundary between VEDA and other systems
- the default mental model used when classifying VEDA behavior

---

## Out of Scope

This document does not define:

- detailed VEDA workflows
- detailed storage or ingestion design
- detailed interface contracts
- detailed governance rules
- implementation details

Those belong in more specific VEDA, interface, workflow, or governance docs.

---

## System

- veda

---

## Core Rule

VEDA is the observatory of the V Ecosystem.

VEDA exists to observe external reality, record what it sees, and preserve that record faithfully so other systems may interpret it.

VEDA does not interpret on behalf of the ecosystem.
VEDA does not propose action.
VEDA does not plan.
VEDA does not execute.

VEDA watches and records. That is its complete role.

---

## The Observatory Mental Model

A telescope does not measure planetary distance.
It observes. The measurement, the interpretation, the conclusion — those happen elsewhere, by other systems, using what the telescope saw.

VEDA is the telescope.

It points at external reality — search behavior, performance signals, market conditions, platform activity — and records what it sees with timestamps, provenance, and fidelity. It does not ask what should be done about what it saw. It does not know what was built. It simply watches and records faithfully.

Interpretation belongs to VEDA Strategy, Project V, and V Forge, who take what the observatory saw and ask the real questions — VEDA Strategy derives scored intelligence and strategic signals from it, Project V uses those signals for planning, and V Forge uses them for execution intelligence.

This mental model is the primary guard against VEDA scope creep.
If a proposed capability cannot be described as something a telescope does, it does not belong in VEDA.

---

## VEDA Definition

VEDA is the system used to observe, capture, preserve, and expose external signals and evidence relevant to the ecosystem's projects.

It turns external inputs into:

- signal truth
- evidence truth
- observability truth
- bounded observatory outputs that other systems may consume

VEDA is not the planner.
VEDA is not the executor.
VEDA is not the content graph owner.
VEDA does not analyze what you have built.
VEDA does not propose what you should build next.

---

## Owns

VEDA owns:

- SERP data and keyword intelligence
- search volatility, intent drift, and change classification
- Google Analytics 4 performance observations
- Google Search Console indexation and performance observations
- YouTube search and channel observatory data
- raw AI-surface observability — mentions, citations, fan-out queries, brand entity appearances, and answer-surface platform metadata captured from admitted providers such as DataForSEO AI Optimization
- source capture and source item ingestion
- observatory event log
- external provider data ingestion pipelines
- signal packages produced from observatory records for ecosystem consumption

### Explanation
VEDA is where the ecosystem preserves its view of external reality.
Every capability VEDA owns is grounded in observing something that exists outside the ecosystem and recording it faithfully.

---

## Does Not Own

VEDA does not own:

- planning truth
- orchestration truth
- readiness truth
- handoff truth
- execution truth
- implementation truth
- the content graph of what was built
- proposals for what should be built
- intelligence derived from internal project structure

### Explanation
VEDA may supply signal to VEDA Strategy, Project V, and V Forge.
VEDA may observe how external reality responds to what was built.
But VEDA must not become the system that models internal project structure, makes planning proposals, or owns execution history.

The content graph — the structural model of what a project has built — belongs to V Forge.
VEDA Brain does not exist in this ecosystem. Derived strategic intelligence — opportunity scoring, gap detection, clustering, competitive analysis — is the responsibility of VEDA Strategy. Planning decisions are the responsibility of Project V. Execution intelligence is the responsibility of V Forge.

---

## Main Ecosystem Relationships

### Relationship to VEDA Strategy
VEDA provides bounded observatory signal to VEDA Strategy for strategic intelligence derivation.

VEDA Strategy reads VEDA's observatory truth and derives scored opportunities, gap signals, clustering outputs, and competitive analysis from it.

VEDA does not own the derived intelligence VEDA Strategy produces.
VEDA does not make the planning or execution decisions that follow from VEDA Strategy's outputs.

### Relationship to Project V
VEDA provides bounded, market-facing signal to Project V.

Project V uses that signal to inform planning decisions — what opportunities exist, what the market shows, what is worth pursuing.

VEDA does not become the owner of planning truth by providing signal.
The interpretation and planning conclusion belong to Project V.

### Relationship to V Forge
VEDA provides bounded observatory signal to V Forge for execution intelligence purposes.

V Forge owns the content graph and crosses it against VEDA's performance signal to answer: how is what we built performing, where are the gaps.

VEDA does not own what was built.
VEDA does not own execution intelligence.
VEDA provides the raw signal that V Forge consumes.

The governed interface for VEDA to V Forge signal consumption is defined in `../interfaces/veda-to-v-forge-signal-interface.md`.

---

## Responsibility Model

VEDA is responsible for:

- observing and capturing external signals across all governed observatory domains
- preserving evidence with provenance and time context
- maintaining ingest discipline so observatory records are clean and trustworthy
- producing bounded signal outputs for ecosystem consumption
- exposing observatory state through governed interfaces and API surfaces

VEDA is not responsible for:

- deciding what projects should be built
- modeling the internal structure of what was built
- generating planning proposals
- deriving strategic intelligence — that is VEDA Strategy's role
- generating execution intelligence
- replacing VEDA Strategy's derived intelligence role
- replacing Project V's planning role
- replacing V Forge's execution intelligence role

---

## Human-In-The-Loop Principle

VEDA is a governed observatory system.

Human review and direction remain especially important for:

- adding new external data providers to the observatory
- establishing or changing paid data pull authorization
- source trust decisions
- doctrine changes affecting observatory boundaries

VEDA may be heavily LLM-assisted, but it is not a freeform data collection blob.

---

## LLM Use Principle

A capable LLM should be able to infer from the VEDA docs that:

- VEDA is a pure observatory — it watches and records external reality
- VEDA does not plan, propose, or execute
- VEDA does not own or model internal project structure
- VEDA provides signal that other systems interpret
- signal provision is not the same as planning or execution authority

If the docs allow VEDA to drift toward planning, execution, or internal content modeling, the VEDA doctrine is wrong.

---

## Usage

This document should be used:

- as the first identity doc for VEDA in the shared root
- as the top-level VEDA role definition for operators and LLMs
- as a boundary reference when writing more specific VEDA docs
- as a check against future drift in VEDA design or implementation
- as the primary guard against VEDA scope creep

---

## Related Docs

- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `system-invariants.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `data-boundaries.md`
- `operator-surfaces.md`
- `mcp-surface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
