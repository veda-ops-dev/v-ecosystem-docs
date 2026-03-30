# V Forge vs VEDA

## Purpose

This document defines the distinction between V Forge and VEDA, and the rules
that preserve that distinction during execution, signal consumption, and
execution intelligence production.

It exists to answer:

```text
What is the difference between what V Forge does and what VEDA does, where
does signal consumption end and signal ownership begin, and what drift patterns
must be prevented to keep those roles clean?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the fundamental distinction between V Forge's role and VEDA's role
- what V Forge may consume from VEDA and what it must not absorb
- what VEDA retains even when V Forge consumes its signal
- the boundary posture during execution intelligence production
- the drift patterns that blur the line between the two systems

---

## Out of Scope

This document does not define:

- the detailed VEDA signal package format
- the detailed execution intelligence schema inside V Forge
- internal VEDA ingest mechanics
- internal V Forge execution workflow steps

Those belong in the interface docs, VEDA system docs, and V Forge operational docs.

---

## System

- v-forge

---

## Core Rule

VEDA owns external observatory truth. V Forge owns execution truth.

V Forge may consume VEDA signal to produce execution intelligence.
Consuming signal does not transfer signal ownership to V Forge.
VEDA remains the system of record for what was observed externally.
V Forge remains the system of record for what was built and what happened during execution.

---

## The Fundamental Distinction

VEDA answers: what does the external world look like?
V Forge answers: what did we build, and how does it compare to what the external world looks like?

VEDA operates in the observatory domain:
- what search signals exist for target topics
- what the competitive SERP environment looks like
- what traffic and engagement signals show about live content
- what indexation and coverage conditions exist

V Forge operates in the execution domain:
- what content has been built (the content graph)
- how that content is performing based on VEDA signal it has consumed
- what gaps exist between the content graph and the VEDA signal picture
- what execution intelligence emerges from crossing those two datasets

These domains overlap in the analysis layer — V Forge uses VEDA signal to do
its analysis — but must not merge in ownership.

---

## The Telescope and the Workshop Analogy

VEDA is the telescope. It observes the external world and records what it sees.
V Forge is the workshop. It builds things, and after building, it uses the
telescope's readings to assess how what it built is performing.

The workshop does not own the telescope's observations just because it reads them.
The telescope does not own what the workshop built just because the workshop uses
what the telescope saw.

These are different systems doing different things with a governed signal exchange between them.

---

## What V Forge Accepts from VEDA

V Forge accepts through the governed signal interface:

- bounded observatory signal packages relevant to the handed-off execution scope
- keyword ranking and SERP data for target topics
- traffic and engagement signals for live content
- indexation and coverage signals
- competitive SERP context relevant to execution

V Forge does not accept:
- ownership of the underlying observatory records
- the right to modify VEDA evidence records
- the right to generate observatory truth independently
- the right to treat its local copy of VEDA signal as the canonical record

---

## What VEDA Retains When V Forge Consumes Signal

VEDA retains:
- canonical ownership of all observatory records
- the observatory event log
- the evidence provenance records
- the authoritative version of any signal that V Forge has consumed

Even if V Forge stores a local copy of consumed VEDA signal for operational use,
VEDA's record remains the authoritative version.
V Forge's local copy is a derivative reference, not a competing canonical record.

---

## Execution Intelligence Is V Forge's, Not VEDA's

Execution intelligence is the analysis produced by V Forge when it crosses its
content graph against VEDA observatory signal.

This is a V Forge capability, not a VEDA capability.

VEDA provides the raw signal.
V Forge asks: how does what we built compare to what the signal shows?
That cross-referencing analysis — and the conclusions it produces — belongs to V Forge.

VEDA does not produce execution intelligence.
VEDA does not model what V Forge has built.
VEDA does not assess how well built content is performing.

If execution intelligence were attributed to VEDA, that would mean VEDA is
proposing what should be built or changed — which is outside VEDA's role.
Execution intelligence belongs in V Forge because it is a conclusion about
execution, not an observatory observation.

---

## What V Forge Must Not Do with VEDA Signal

V Forge must not:
- treat consumed VEDA signal as its own observatory record
- create a richer version of VEDA signal locally and present it as though VEDA owns it
- provide VEDA signal to external consumers as though V Forge were the signal source
- absorb ongoing observatory function by building independent signal ingestion

If V Forge needs signal that VEDA is not currently providing, the correct path is
to direct VEDA to expand its observatory scope through the governed operator surface,
not for V Forge to build its own observatory capability.

---

## Drift Patterns to Prevent

### V Forge drift toward signal ownership
V Forge has drifted when it:
- maintains its own SERP data, GA4 data, or Search Console data independently of VEDA
- treats its local copy of VEDA signal as the authoritative record
- produces observatory-style outputs that make VEDA redundant for the same signals
- sources signal from external providers directly rather than through VEDA

### VEDA drift toward execution modeling
VEDA has drifted when it:
- models the content graph of what V Forge has built
- produces content gap analysis by comparing its signal to what content exists
- proposes what should be built or changed based on its signal observations
- stores V Forge execution records as part of its observatory truth

The VEDA Brain prohibition (ADR-003) specifically governs the second category.
VEDA observes and records. It does not synthesize, model, or propose.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- consuming signal from VEDA does not make V Forge the signal owner
- execution intelligence belongs to V Forge, not VEDA
- VEDA retains canonical signal ownership regardless of what V Forge does with the signal
- V Forge must not build independent observatory capability
- VEDA must not model or analyze what V Forge has built

If an LLM treats V Forge's execution intelligence as VEDA signal, or attributes
VEDA capabilities to V Forge, this doctrine is failing.

---

## Usage

This document should be used:

- when evaluating whether a proposed V Forge capability would absorb VEDA's role
- when evaluating whether VEDA is drifting into content modeling or execution analysis
- when writing V Forge or VEDA docs that involve the signal boundary
- when reviewing whether execution intelligence is correctly attributed

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `vs-project-v.md`
- `../veda/veda.md`
- `../veda/system-invariants.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
