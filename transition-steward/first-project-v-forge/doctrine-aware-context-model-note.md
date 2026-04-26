# Doctrine-Aware Context Model — Working Design Note

## Purpose

This note captures the current design problem behind a likely next VedaOps planning and architecture task:

> how agents should gain access to the right doctrine, planning packets, transition-support material, and execution context at the right stage, with the right authority posture, without collapsing into prompt soup or retrieval-only guessing.

This is a transition-support working note.
It is not final authority doctrine.
It does not replace existing authority docs on boundaries, memory/continuity, handoff behavior, or harness architecture.

---

## Why this note exists

Recent work clarified several things:

- Qdrant is useful as retrieval support, but is not canonical truth
- VedaOps already has meaningful harness and continuity doctrine
- first-project planning now exists in concrete form
- the next major capability seam is not “more docs”
- the next seam is **how agents should access, load, and use those docs**

The issue is no longer whether doctrine should exist.
The issue is how doctrine and other governed context should be made available to agents in a way that is:

- stage-aware
- authority-aware
- bounded
- inspectable
- resistant to drift
- supportive of continuity without turning continuity into authority

---

## Problem statement

VedaOps is accumulating multiple classes of materials that agents may need:

- authority doctrine
- transition-support notes
- planning packets
- project-specific framing docs
- execution-facing packets
- continuity artifacts
- prior decisions
- supporting inventories and research notes

The system cannot rely on any of these simplistic postures:

### Not acceptable

- **load everything**
- **let retrieval decide by itself**
- **treat all retrieved material as equal**
- **treat continuity artifacts as truth**
- **let one stage use all other stages' context by default**
- **let execution-side agents infer planning intent from weakly relevant docs**

The problem is therefore not only retrieval.
The problem is **context admission, weighting, and stage-appropriate loading**.

---

## Current anchor principle

The current working principle is:

> **Qdrant finds.  
> VedaOps decides.  
> The harness enforces.**

This implies three distinct layers:

### 1. Retrieval support layer
Qdrant or other retrieval surfaces can identify candidate materials that may be relevant.

### 2. Context admission / weighting layer
VedaOps must determine what is actually appropriate to load for the current stage, system, and task.

### 3. Runtime enforcement layer
The harness must enforce the admitted context posture during execution, planning, validation, or review.

This note is primarily about the second layer.

---

## What this model needs to solve

At minimum, the doctrine-aware context model should help answer:

- which docs are relevant for a given workflow stage?
- which docs are mandatory vs optional?
- which docs are authoritative vs supportive?
- which docs are current-system vs referenced-system context?
- what should never be loaded together by default?
- what should be visible to execution vs validation vs planning?
- how does retrieval support get filtered by authority and stage?
- how does the system distinguish:
  - canonical record
  - referenced authority
  - derived intelligence
  - transition-support note
  - planning input
  - continuity artifact
  - inert prior model output

---

## Likely stages that matter

This note does not settle the final stage model, but the likely stage-aware loading problem currently appears across at least:

- intake
- planning
- handoff creation
- execution
- validation
- publication / external mutation
- observation return / feedback

Different stages should not automatically inherit the same context posture.

---

## Why Qdrant alone is not enough

Qdrant is useful for retrieval support.
It is not sufficient to solve this problem by itself.

Qdrant can help answer:

- what may be relevant?
- what looks semantically similar?
- what doctrine or packet mentions this topic?

Qdrant cannot by itself reliably answer:

- should this be loaded now?
- is this authority or transition-support?
- is this planning truth or execution support?
- is this doc current enough?
- is this material allowed for this stage?
- does this retrieved material outrank a directly referenced canonical record?
- should this be excluded because it would bias validation or blur boundaries?

That decision belongs to VedaOps and its harness, not to retrieval infrastructure.

---

## First proving case

The first concrete proving case for this problem should be the current first-project work:

- `first-project-entity-driven-gift-discovery-site.md`
- `first-project-entity-driven-gift-discovery-planning-packet.md`

That project is useful because it already creates multiple distinct context classes:

- project shape / structural rules
- planning packet
- harness / continuity constraints
- future execution-facing needs
- later branded-network support posture
- future validation and review needs

This makes it a good concrete case for testing a doctrine-aware context model.

---

## Relationship to current doctrine

This note should be read as downstream of, not above, existing docs such as:

- cross-system boundaries
- Project V / VEDA / VEDA Strategy / V Forge identity docs
- desktop memory and continuity model
- LLM harness architecture
- handoff / intake / approval workflows

This note should not rewrite those docs.
It should help identify how their doctrine becomes operational at context-loading time.

---

## Key design tension

The design tension is:

> maximize continuity of useful LLM work  
> while preserving governance slices, authority boundaries, and review gates

This is closely related to the “loaf” framing discussed in project conversations:

- the loaf = continuous potential end-to-end capability
- the slices = governance, approval, truth, and authority seams

The doctrine-aware context model is one of the things that determines whether an LLM can move usefully across the loaf without freelancing, drifting, or crossing authority boundaries.

---

## What this model is not

This is not:

- a generic RAG note
- a Qdrant integration note
- a new canonical architecture doctrine
- a claim that all agent work should become autonomous
- a prompt-engineering memo
- a replacement for governed packets, handoffs, or approval seams

It is a design note about a specific missing layer:
**how governed context should be selected and loaded for agents.**

---

## Likely outputs of the next design pass

A future design pass against this note should try to produce something like:

- stage-aware context classes
- authority-weight / authority-class distinctions
- mandatory vs optional context per stage
- retrieval-to-admission rules
- exclusions that protect validation independence
- candidate packet/bundle model for agent context loading
- a concrete first-project mapping
- eventual support for a “Loaf Audit” or end-to-end workflow capability audit

---

## Immediate next move

The next sensible move is not broad research.

The next sensible move is to use this note to support a **bounded design pass** that asks:

> How should VedaOps load doctrine and related materials for agents by stage, authority class, and workflow role, using the first project as the proving case?

That design pass should stay transition-support only unless and until the resulting model is stable enough to promote.
