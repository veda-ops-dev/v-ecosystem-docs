# External Technology Research Doctrine

## Purpose

This document defines how external technology research is captured, governed, and used inside Project V.

It exists to answer:

```text
When Project V planning depends on external technologies such as databases,
frameworks, APIs, libraries, runtimes, infrastructure components, or
third-party platforms, what research must be captured, what must it contain,
and how does it affect decisions, readiness, audit, and handoff?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- what external technology research is inside Project V
- why it belongs in Project V planning support rather than VEDA or V Forge
- the record posture it takes inside Project V canonical data
- the minimum semantics it must preserve
- how it connects to decisions, readiness, audit, and handoff
- how staleness and re-validation must be handled
- the anti-drift rules operators and LLMs must preserve when using it

---

## Out of Scope

This document does not define:

- exact schema fields or SQL types
- controlled vocabulary definitions themselves
- provider integration mechanics
- VEDA observatory evidence
- V Forge execution truth

Those belong in schema, vocabulary, ecosystem, and interface docs.

---

## System

- project-v

---

## Core Rule

External technology research is planning-support evidence owned by Project V.

If a planning decision depends on external technology behavior, constraints,
features, or version-specific capabilities, that dependency must be captured as
recoverable governed research that is:

- version-aware
- source-attributed
- timestamped
- freshness-classified

Undated, unversioned, or unattributed technology claims must not support
continuity-binding Project V decisions.

---

## Definition

External Technology Research (ETR) is a bounded planning-support research
artifact that captures what Project V believes about a specific external
technology at a specific version and time for a specific planning purpose.

External technology includes but is not limited to:

- databases and data stores
- frameworks and runtimes
- third-party APIs and SaaS providers
- libraries and open-source components
- infrastructure components and platforms
- developer tooling consumed at implementation time

ETR exists because implementation-target planning decisions often depend on
claims such as:

- what version is intended
- what capabilities the chosen version has
- what constraints or caveats apply
- what official guidance currently says

Those claims must not live only in transient chat, implied memory, or
unstructured handoff prose.

---

## What ETR Is Not

ETR is not:

- VEDA observatory evidence
- V Forge execution truth
- a `DecisionRecord`
- a thin execution-facing `ExternalLink`
- a free-floating markdown note with no governed Project V record posture

VEDA observes reality. Vendor documentation and external platform references are
claims about tools and platforms, not observatory truth.

V Forge owns what was actually built or executed with a technology. ETR only
captures the planning-time basis for believing certain technology facts,
constraints, or version behavior.

---

## Why ETR Belongs in Project V

Project V owns:

- planning truth
- decision truth
- readiness truth
- handoff truth

ETR belongs in Project V because implementation-target planning decisions are
Project V decisions, and the evidence basis for those decisions must be
recoverable.

If a planning decision depends on PostgreSQL 16 rather than PostgreSQL 14,
or on a Stripe API behavior documented in one version rather than another,
that dependency is part of planning truth.

The external vendor documentation itself is not Project V-owned canonical truth.
Project V owns the bounded captured research artifact that records what planning
believed, from what source, at what version, and when.

---

## Record Posture

ETR is not a new record family.

ETR is a specialized posture of `ResearchDoc`.

The governed posture is:

```text
ResearchDoc.source_type = external_reference
```

This does not change the ResearchDoc family. It narrows one existing source
posture into a stronger governed interpretation when the research concerns
external technology.

When a `ResearchDoc` is used as ETR, it must preserve the additional semantics
defined in this document.

---

## Minimum Semantic Contract

Every ETR record must preserve enough information to answer the following.

### 1. Technology identity

What product, library, framework, API, runtime, or platform does this research
concern?

### 2. Version or version range

What exact version or bounded version range does the research reflect?

`latest` is not a valid version.

### 3. Source attribution

What authoritative source supports the research?

Examples include:

- vendor documentation URL
- spec section
- official API reference
- repository documentation at a known commit or release

A summary with no attributable source is not valid ETR.

### 4. Capture timestamp

When was this research captured?

This is distinct from a record creation timestamp where the two differ.

### 5. Freshness classification

The record must preserve explicit freshness posture such as:

- `current`
- `aging`
- `stale`
- `unknown`

The exact representation remains subordinate to schema and vocabulary docs.

### 6. Supported decision references

The record must preserve what planning decisions it supports.

ETR without a decision relationship for too long is either premature or
orphaned and should be treated as a hygiene or audit concern.

---

## Relationship to ResearchDoc

`ResearchDoc` remains the governed canonical Project V family for planning
support research artifacts.

ETR does not replace general planning research. It identifies the subset of
planning research that is:

- externally sourced
- technology-specific
- version-sensitive
- implementation-relevant

General planning research may remain broader.
ETR is stricter because implementation-target decisions create stronger
freshness, attribution, and recoverability requirements.

---

## Relationship to Decisions

If a `DecisionRecord` depends on an external technology claim, the supporting
ETR must be recoverable.

Examples include decisions about:

- what database version to use
- what framework version to target
- what provider API contract is assumed
- what platform constraint or feature is relied on

A decision that cites external technology behavior without recoverable ETR is
weaker than it appears because its basis cannot be checked later.

Project V must not treat:

- remembered vendor behavior
- unrecorded web research
- chat-level explanation
- intuition about "the current docs"

as sufficient substitutes for governed ETR.

---

## Relationship to Readiness

ETR matters to readiness when a record's forward progression depends on an
implementation-target technology assumption.

If readiness depends on:

- a database choice
- a framework version
- a provider API behavior
- a platform constraint

then missing or stale ETR is a planning-side deficiency.

Readiness must not assume technology basis is sound merely because the planning
team previously discussed it.

---

## Relationship to Audit

ETR matters to audit because BYDA must be able to ask whether the evidence basis
for implementation-target planning is actually sufficient.

A research audit or implementation-readiness audit should be able to detect
failures such as:

- implementation-target planning depends on external technology but no ETR exists
- ETR exists but lacks version information
- ETR exists but lacks source attribution
- ETR exists but is stale for the current planning moment

Without those checks, audit can overclaim confidence while implementation rests
on ungoverned assumptions.

---

## Relationship to Handoff

If a handoff depends on implementation-target technology assumptions, the
planning basis for those assumptions must remain recoverable.

Project V should not hand work to V Forge on the basis of vague claims such as:

- use Postgres
- use the Stripe API
- target the latest framework docs

without recoverable ETR that makes clear:

- what was researched
- what version was in view
- what source was used
- how fresh the planning basis is

Handoff may reference ETR. Handoff must not replace it.

---

## Freshness and Re-Validation Rule

ETR must not be treated as permanently fresh simply because it is stored.

Re-validation may be required when:

- substantial time has passed since capture
- a relevant version release materially changes the target technology posture
- the supported decision is reopened, superseded, or reconsidered
- handoff is being prepared significantly later than the original research
- audit determines the prior basis is no longer trustworthy enough

A stale ETR record is a planning-side problem.
It must not be silently reused.

---

## Data Boundary Rule

ETR is canonical Project V planning-support data.

Project V owns:

- the bounded captured research artifact
- its interpretation for planning
- the linkage from that research to planning records

Project V does not own:

- the external source system
- the full vendor documentation corpus
- observatory truth about the world
- execution truth about what was actually built

ETR must remain bounded.
It must not turn Project V into:

- a second observatory
- a second execution ledger
- a mirror of external vendor documentation

---

## Anti-Drift Rules

The following are forbidden drift patterns:

- decisions citing external technology behavior with no recoverable ETR
- ETR records with no version information
- ETR records with no source attribution
- ETR stored only in chat or ungoverned prose
- stale ETR being reused silently
- handoff or implementation docs paraphrasing unsupported technology claims as
  though they were grounded — see `implementation-document-doctrine.md` for
  the minimum ETR linkage requirements on implementation documents
- treating vendor documentation as VEDA-style observatory evidence
- letting ETR expand into uncontrolled documentation hoarding unrelated to a
  planning need

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- implementation-target technology assumptions require governed research
- `ResearchDoc.source_type = external_reference` may carry a stricter posture
  when the artifact is ETR
- version, source, timestamp, and freshness are not optional niceties
- decisions, readiness, audit, and handoff may all depend on ETR quality
- chat memory is not sufficient evidence continuity

If an LLM produces implementation-target planning output that depends on
external technology claims without preserving ETR, this doctrine is failing.

---

## Usage

This document should be used:

- when capturing external technology research in Project V
- when reviewing whether a decision has adequate technology basis
- when checking readiness and audit sufficiency for implementation-target work
- when deciding how implementation docs and handoff material should preserve
  technology assumptions
- when rejecting convenience-driven drift into unstored technology assumptions

---

## Related Docs

- `project-v.md`
- `data-boundaries.md`
- `schema-authority.md`
- `implementation-traceability.md`
- `implementation-document-doctrine.md`
- `readiness-evaluation-rules.md`
- `audit-evaluation-rules.md`
- `controlled-vocabularies.md`
- `../governance/evidence-continuity-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../ecosystem/external-provider-integration-doctrine.md`
