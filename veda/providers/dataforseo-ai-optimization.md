# DataForSEO AI Optimization — provider posture for VEDA

## Purpose

This document defines how DataForSEO AI Optimization data is admitted into VEDA as observatory input.

It exists to answer:

```text
What AI-surface data from DataForSEO may enter VEDA as observatory truth,
what must remain raw observation rather than interpretation, and what inputs
may later feed VEDA Strategy as derived intelligence?
```

This is a VEDA provider/doctrine document.

---

## Provider identity

| Field          | Value                                                                                                         |
| -------------- | ------------------------------------------------------------------------------------------------------------- |
| Provider name  | DataForSEO AI Optimization                                                                                    |
| Classification | Observatory Input                                                                                             |
| Role           | Supplies raw AI-surface observations for answer-surface, mention, citation, and related LLM behavior tracking |

---

## Why this provider belongs in VEDA

VEDA is the observatory truth system of the V Ecosystem.

DataForSEO’s AI Optimization product line supplies raw observable data about AI-generated answer surfaces, including mentions, citations, fan-out queries, and brand-entity-related outputs across major AI platforms.

That makes it a VEDA input provider, not a strategy engine.

VEDA records what was observed.
VEDA does not decide what it means.

---

## What this provider may supply into VEDA

The following data families may be admitted into VEDA as observatory input:

* LLM mention observations
* LLM citation observations
* cited source domain observations
* cited source page observations
* AI-platform response metadata
* Google AI Overview citation/source observations
* fan-out query observations
* brand entity observations
* platform/time/location/language observation metadata
* raw aggregate observability metrics supplied by the provider

These are observatory records because they describe what an external AI surface produced or referenced at a given time.

---

## What this provider must NOT produce inside VEDA

DataForSEO AI Optimization must not be used inside VEDA to produce:

* citation opportunity scoring
* answer-surface opportunity scoring
* strategic gap detection
* tactical recommendations
* copywriting recommendations
* schema-markup recommendations
* prioritization decisions
* execution instructions
* project-creation recommendations

Those belong outside VEDA.

VEDA is the telescope.
It records what answer surfaces did.
It does not interpret what should happen next.

---

## Core observatory rule

A DataForSEO AI Optimization record is admissible into VEDA only when it preserves the distinction between:

* what the provider observed or returned
* what VedaOps may later derive from that observation

The record in VEDA must remain an observatory record.

It may support later strategic interpretation.
It must not embed that interpretation itself.

---

## Admitted observatory families

### 1. LLM mention observations

These record when a keyword, brand, product, service, domain, or page is mentioned in supported AI-surface outputs.

### 2. LLM citation observations

These record when a source is cited, linked, quoted, or referenced by a supported AI surface.

### 3. Source/domain/page observability

These record what domains and pages appear as cited or referenced sources.

### 4. Fan-out query observations

These record related queries generated or explored by the AI surface as part of response construction.

### 5. Brand entity observations

These record structured brand/entity appearances surfaced by the provider.

### 6. AI-surface response metadata

These record platform, timestamp, locale, query context, and other provider-supplied observability context.

---

## Supported-surface posture

The provider may expose data across multiple answer surfaces and AI platforms.

VEDA should treat surface coverage as an observability dimension, not a doctrine shortcut.

A record should preserve, where available:

* platform / surface
* timestamp
* locale / market
* query or target basis
* source/citation relationship
* provider response provenance

Different surfaces may behave differently.
VEDA records that difference.
VEDA does not flatten it into one universal truth.

---

## What later may feed VEDA Strategy

The following classes of derived intelligence may later be built from these VEDA observatory records, but they are not part of VEDA itself:

* citation opportunity scoring
* answer-surface gap detection
* platform-priority models
* fan-out expansion interpretation
* citation volatility interpretation
* brand/entity visibility interpretation
* cross-platform strategic comparison

These belong to VEDA Strategy as derived intelligence outputs built from VEDA observatory truth.

---

## Provenance requirements

Every DataForSEO AI Optimization observatory record admitted into VEDA must preserve sufficient provenance, including where available:

* provider name
* provider product family / endpoint family
* source platform / answer surface
* query or target basis
* observation timestamp
* retrieval timestamp
* raw provider record ID or stable source reference
* location / language context if supplied
* citation/mention relationship context if supplied

A record without provenance is not admissible observatory truth.

---

## Boundary rule

The existence of citation or mention data does not make VEDA an answer-surface optimization engine.

It only makes VEDA capable of observing AI-surface behavior.

Interpretation belongs to VEDA Strategy.
Planning belongs to Project V.
Execution belongs to V Forge.

---

## Deferred questions

The following should remain deferred until later doctrine/research work is complete:

* exact VEDA schema families for AI-surface observability
* exact normalization model for fan-out queries and brand entities
* exact VEDA Strategy models derived from these observations
* exact downstream tactic/playbook implications
* exact cross-platform weighting or prioritization doctrine

These should not be guessed early.

---

## Related docs

* `veda/providers/registry.md`
* `veda/observability-and-signal-role.md`
* `veda/schema-reference.md`
* `veda/evidence-and-source-provenance.md`
* `../veda-strategy/veda-strategy.md`
* `../veda-strategy/data-boundaries.md`
