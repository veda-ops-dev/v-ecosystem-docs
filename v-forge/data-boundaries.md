# V Forge Data Boundaries

## Purpose

This document defines the data boundary posture for V Forge.

It exists to answer:

```text
What data does V Forge store as canonical execution truth, what may it hold
only as thin local references, what may it consume from Project V and VEDA
without absorbing their ownership, what is explicitly forbidden from V Forge
storage, and how must future capability work — particularly surface execution
condition — remain bounded to execution truth without drifting into planning
or observatory ownership?
```

This is a Tier 2 V Forge authority document.

Read alongside:
- `v-forge.md` — identity and ownership posture
- `schema-authority.md` — governed schema domains and record family posture
- `schema-specification.md` — concrete field-level schema
- `../interfaces/data-boundaries.md` — cross-system data boundary posture
- `../ecosystem/cross-system-boundaries.md` — system ownership rules

---

## Scope

This document governs:

- what V Forge stores as canonical execution truth in its own database
- what V Forge stores as thin local anchors or operational references
- what V Forge consumes from Project V without absorbing planning truth
- what V Forge consumes from VEDA without absorbing observatory truth
- what first-pass light-tracking is allowed for lightly operated surfaces
- what is explicitly forbidden from being stored as canonical V Forge truth
- how execution intelligence uses VEDA signal without becoming a shadow observatory
- how future surface execution condition work must remain inside execution truth
- anti-drift rules
- non-goals

---

## Out of Scope

This document does not define:

- the detailed internal schema of V Forge's database tables or record families
- the exact fields and types of each record family
- interface protocols or API contract details
- provider-specific data formats
- VEDA schema design
- Project V schema design

Those belong in `schema-specification.md`, interface docs, and system-specific docs.

---

## System

- v-forge

---

## Core Rule

V Forge stores execution truth in its own database.

V Forge does not store planning truth.
V Forge does not store observatory or signal truth.
V Forge does not absorb canonical ownership of data that originates in another system.

Infrastructure proximity does not transfer ownership.
Consuming another system's bounded output does not make V Forge the owner of that
output's underlying data.

All cross-system data access occurs only through governed APIs and interfaces.
V Forge has no direct database access to Project V's database or VEDA's database.
This is an ecosystem-wide invariant per ADR-009.

---

## What V Forge Stores Canonically

V Forge is the canonical owner of execution truth. The following categories belong
to V Forge as its owned data.

### Execution lifecycle state
The receipt, active state, completion, and closure of execution work.
`ExecutionEntry` records are V Forge's anchor for execution lifecycle. They reference
Project V handoffs by external ID but do not replicate handoff content.
`ExecutionFinding` records capture bounded findings produced during execution.
`ReturnToPlanning` records capture what was formally returned to Project V and when.
`MaintenanceRecord` records capture maintenance activity on execution assets.

### Content graph
The structural model of what a project has built.
Pages, topics, entities, internal links, content clusters, page-topic junctions,
and page-entity junctions are canonical V Forge truth.
Per ADR-002, the content graph belongs to V Forge. It does not belong in VEDA.
The content graph changes when V Forge does work — not when external conditions change.

### Publication and release continuity
The structured record of what has been published or released, when, and at what state.
`PublicationEvent` records are the immutable append-only event log of publication actions.
`Release` records are the versioned artifact records for release-oriented surfaces.
`StorePublication` records track when and at what state a release was submitted and
published to a distribution store surface.
This is execution truth because it records what V Forge caused to happen.

### Distribution tracking
Cross-surface distribution actions.
`DistributionAction` records capture that content from one surface was distributed to
another surface.
This is the primary cross-surface relational mechanism in V Forge.
It is execution truth because it records what V Forge did.

### Surface registry
The operational inventory of what surfaces a project operates on.
`Surface` records are canonical V Forge truth — they represent the project's
owned/operated/referenced execution footprint.
`SurfaceSnapshot` records are periodic operational pulse snapshots.
This is execution truth because it represents the surfaces V Forge operates and maintains.

### Playbook routing
Metadata routing records that tell the LLM or operator which playbook applies for
a given task type, surface type, and content archetype.
`Playbook` records are canonical V Forge truth.
Actual playbook content lives as docs referenced by path.

### Light-tracked operated surface records
`Video`, `SocialPost`, and `NewsletterIssue` records are light operational awareness
records for lightly tracked operated surfaces (YouTube, social, newsletter).
They are minimal first-pass execution-side records.
They are canonical V Forge truth within their bounded first-pass scope.

---

## What V Forge Stores as Thin Local Anchors

Thin local anchors are records V Forge must maintain for local execution scoping and
referential integrity, but which do not represent canonical ownership of the underlying data.

### Project identity anchor
V Forge maintains a `Project` anchor record in its own database. V Forge owns this
record structurally — it lives in V Forge's DB and scopes all other V Forge records.
However, V Forge does not own the project identity it represents: the external project
UUID, project type, and display name are derived from Project V at anchor creation time
and must not be treated as V Forge-originated truth.
This record carries only: the external project ID reference, the project type, and a
display name. It is the foreign-key root for all V Forge project-scoped records and
exists solely to support local referential integrity.
Project V remains the canonical owner of project identity and planning structure.
If the underlying project is deleted or reclassified in Project V, the V Forge anchor
does not automatically update — this is an operational sync concern, not a schema one.

### Handoff external reference
`ExecutionEntry` records carry a `handoff_id_external` field — the Project V handoff UUID.
This is a thin reference that anchors V Forge's execution lifecycle to the Project V handoff
that authorized it.
It does not copy handoff content, planning context, readiness state, or orchestration data.
Project V remains the canonical owner of the handoff record.

### Signal-derived context in findings and reports
When V Forge execution intelligence produces findings that are informed by VEDA signal,
those findings may note the signal source, timestamp, and trust posture.
This bounded provenance annotation is execution reporting context, not signal ownership.
VEDA remains the canonical owner of the underlying signal.

---

## What V Forge Consumes from Project V

V Forge consumes bounded planning inputs from Project V through the governed handoff interface.

### Consumed at handoff time
- the scope of approved work
- the relevant readiness context for the work
- bounded constraints or conditions that execution must respect
- bounded evidence references that execution requires
- the high-level expected outcomes or artifacts

### What consumption means
V Forge uses this context to execute approved work.
V Forge does not absorb it as canonical V Forge truth.
V Forge does not replicate planning decision records, readiness evaluations,
orchestration state, or lifecycle state as V Forge-owned schema records.

### What V Forge must not do with Project V inputs
V Forge must not:
- store richer or more authoritative copies of Project V's planning records
- treat planning context received at handoff as V Forge-owned orchestration truth
- use planning inputs to expand V Forge's scope beyond the approved execution work
- make V Forge the canonical source for project identity, classification, or lifecycle

The handoff interface is defined in:
`../interfaces/project-v-to-v-forge-handoff-interface.md`

---

## What V Forge Consumes from VEDA

V Forge consumes bounded observatory signal from VEDA through the governed signal interface
for use in execution intelligence.

### Consumed signal classes
- SERP position and ranking data for keyword targets associated with the project
- search performance metrics from Search Console — impressions, clicks, CTR, position trends
- indexation status and coverage signals
- traffic and engagement metrics from GA4 for the project's properties
- keyword volatility and intent drift signals
- SERP feature composition changes relevant to execution planning
- bounded source capture content where relevant to execution intelligence

All consumption is read-only and project-scoped.
All consumption goes through VEDA's API.
V Forge has no direct access to VEDA's database.

### What consumption means
V Forge uses consumed signal to cross against the content graph and produce
execution intelligence.
Consuming VEDA signal does not make V Forge the owner of that signal.
VEDA remains the canonical owner of all observatory records.

### What V Forge must not do with VEDA signal
V Forge must not:
- store consumed VEDA signal as canonical V Forge truth
- accumulate open-ended signal archives that duplicate VEDA's observatory function
- present consumed signal to Project V as though V Forge were the signal source
- treat signal consumption as granting observatory responsibility

The signal interface is defined in:
`../interfaces/veda-to-v-forge-signal-interface.md`

---

## What V Forge Must Not Store as Canonical Truth

The following are explicitly forbidden from being stored as canonical V Forge truth.

### Planning truth
- Project V planning decision records
- Readiness evaluation records
- Orchestration state records
- Handoff content beyond the thin external ID reference
- Project lifecycle state records
- Audit records and audit gap records that belong to Project V

### Observatory truth
- SERP snapshot records
- GA4 observation records
- Search Console indexation and coverage records
- YouTube observatory records (views, impressions, CTR, watch time as raw signal)
- Keyword intelligence records
- Evidence provenance records
- Observatory event log records
- Source capture records as primary storage

All of these belong canonically to VEDA.
V Forge reads bounded outputs. It does not own the underlying records.

### Raw provider data
Raw data from external providers (search APIs, analytics APIs, platform APIs) belongs
to VEDA where it is observatory data.
V Forge must not warehouse raw provider payloads.

### Execution intelligence as a stored record family
Execution intelligence is the analytical output of crossing the content graph against
VEDA signal. It is a query-time computation, not a stored record family.
The inputs (content graph — owned by V Forge; signal — owned by VEDA) remain with
their respective systems.
If execution intelligence outputs need to be preserved for reporting or continuity,
they belong in `ExecutionFinding` or execution report records with clear V Forge
provenance — not as a separate stored observatory-resembling record set.

### Planning context beyond the thin anchor
V Forge must not store project strategy, project theses, opportunity scoring, readiness
methodology outputs, or any Project V planning content as though V Forge originated it.

### Deferred future domain truth
Experimentation and optimization results, SaaS/runtime/commercial state, advanced
engagement analytics, and advanced graph features are deferred domains.
They must not be designed into or accumulated inside current V Forge storage.

---

## First-Pass Light-Tracking Boundary

Four surface types are lightly tracked in first-pass V Forge schema:
YouTube channels, social profiles, newsletters, and store listings.

### What is allowed
- `Video` records: YouTube video ID, title, published date, duration, visibility status,
  and optional linked page or release reference
- `SocialPost` records: post URL, content summary, posted timestamp, and optional
  linked content reference
- `NewsletterIssue` records: subject, sent date, audience description, and aggregate
  open and click rates as integer percentages
- Store listing awareness through `Surface` and `SurfaceSnapshot` records

These records are the minimum needed for distribution tracking and operational surface
awareness. They are execution-side operational records, not analytics records.

The aggregate open and click rates on `NewsletterIssue` are treated as bounded
execution feedback — summary metrics returned by the send operation itself as part
of V Forge's own publication action — not as open-ended external monitoring.
This is what distinguishes them from observatory truth: V Forge initiated the send;
the rates reflect the outcome of that specific execution action. Per-link click
tracking, subscriber behavior analysis, and audience segmentation are not covered
by this rationale and remain deferred.

### What is not allowed in first pass
- Deep YouTube analytics: per-video view counts, watch time, retention rates,
  impressions, CTR — these are VEDA observatory truth, not V Forge execution truth
- Deep social analytics: impression counts, engagement rates, follower growth — same boundary
- Newsletter subscriber management: subscriber segment records, per-link click tracking,
  automation sequence records — deferred
- Store listing analytics: install growth, rating distributions, conversion metrics — VEDA territory

### The key distinction
V Forge records that a video was published at a given time, what visibility status it has,
and what owned content it links to. That is execution truth.
V Forge does not record how many people watched it, what the retention curve looked like,
or what the CTR was. Those are observatory truth owned by VEDA.

### Expansion rule
Light-tracked surface record families must not expand beyond their minimal first-pass shape
without a governed schema expansion review.
Drift into full platform-specific content management or analytics ownership is forbidden.

---

## Future Surface Execution Condition Boundary

Surface execution condition is a recognized V Forge design thread.
It is not first-pass schema.
This section defines the data boundary constraints that must govern it when it is promoted.

The concept is documented in:
`surface-execution-state-design-note.md`

### What surface execution condition is
Surface execution condition would model the current operational reality of a surface
as V Forge sees it: what has been configured, what is missing, what execution work has been
applied, and what operational state the surface is in.

This is execution truth. It changes when V Forge does execution work on a surface.
It belongs conceptually to V Forge.

### What surface execution condition must not become

**Not observatory truth.**
Surface execution condition must not store CTR, watch time, impressions, rankings,
traffic, conversion rates, or any raw external performance signal.
Those belong to VEDA.
The test: if it changes because the external world changed (not because V Forge did work),
it does not belong in surface execution condition.

**Not planning truth.**
Surface execution condition must not store strategic direction, project prioritization,
decisions about which surfaces should exist, or intent about what to build next.
Those belong to Project V.
The test: if it answers "what should we do" rather than "what has been done and what state is it in,"
it does not belong in surface execution condition.

**Not optimization or experimentation state.**
A/B test results, variant tracking, quality scoring from systematic testing, and
improvement experiment outcomes belong to the future experimentation/optimization layer.
Surface execution condition is the layer beneath: it describes what exists and what condition
it is in, not how well it performs comparatively.

**Not a freeform knowledge dump.**
Surface execution condition is not a place for narrative notes, general observations,
or unstructured execution commentary.
If the data is not queryable and governable as structured execution truth, it does not
belong in this model.

### Data boundary rule for surface execution condition
When surface execution condition is governed and promoted:
- records must change when V Forge does execution work on the surface
- records must not change in response to external performance signals
- records must model factual operational state, not analytical conclusions
- the model must attach to the existing `Surface` record family as governed extension records
- each surface type's condition vocabulary must be governed separately before schema implementation
- the VEDA signal boundary must be re-examined explicitly before any condition category
  that touches performance or platform behavior is designed into schema

Do not pre-build surface execution condition schema before it is explicitly governed.
The design note captures the pattern; the schema comes after deliberate review.

---

## Anti-Drift Rules

### 1. Observatory data must not appear in V Forge tables
If V Forge schema contains SERP snapshots, GA4 observations, Search Console data,
keyword intelligence records, YouTube view counts or watch time, or any raw
observatory data that should belong to VEDA, the boundary has drifted.

### 2. Planning data must not appear in V Forge tables
If V Forge schema contains planning decision records, readiness evaluations, orchestration
state, or project lifecycle records that should belong to Project V, the boundary has drifted.

### 3. Consumed signal must not become canonical V Forge truth
If VEDA signal consumed through the governed interface is stored in V Forge schema as
though V Forge originated it — rather than as a bounded reference within an execution
finding or report — the boundary has drifted.

### 4. Execution intelligence must remain a query pattern
If V Forge stores execution intelligence outputs as a permanent record family resembling
VEDA observatory tables, the boundary has drifted.
Execution intelligence is the result of a cross-reference computation. The result may
appear in a bounded `ExecutionFinding` with provenance noted. It must not accumulate as
a shadow observatory.

### 5. The project anchor must remain thin
If the `Project` record family in V Forge expands to carry planning structure, readiness
state, orchestration stage, or any Project V planning field beyond the minimum identity
anchor, the boundary has drifted.

### 6. Light-tracked surfaces must not silently deepen
If YouTube, social, newsletter, or store listing record families expand into full
analytics domains without a governed schema expansion review, the boundary has drifted.

### 7. Surface execution condition must not absorb observatory data
If surface execution condition work — when it is eventually governed — introduces records
that store performance signal, analytics outcomes, or competitive intelligence, the
boundary has drifted into VEDA territory.

### 8. Surface execution condition must not absorb planning data
If surface execution condition records store strategic intent, prioritization rationale,
or decisions about what surfaces should exist or what direction to take, the boundary
has drifted into Project V territory.

### 9. Deferred domains must not be pre-built
If V Forge schema includes empty columns, nullable foreign keys, or speculative records
for experimentation, SaaS/runtime, commercial truth, or advanced engagement analytics,
the boundary has drifted.

---

## Non-Goals

V Forge data boundary governance explicitly does not pursue:

- serving as the canonical observability system for any project surface
- accumulating raw provider data or raw platform signals
- building a shadow planning layer from execution observations
- warehousing cross-project signals for portfolio views
- modeling optimization experiments or quality scoring before those domains are
  explicitly governed
- turning light-tracked surface records into full platform content management systems
- absorbing VEDA's signal-system role by incremental signal accumulation
- modeling commercial, SaaS, or runtime state before those domains are explicitly governed

---

## Final Rule

V Forge stores execution truth.
It does not store planning truth.
It does not store observatory truth.
It does not absorb ownership of data that originates elsewhere.

When a proposed V Forge storage decision cannot be clearly classified as execution truth
that V Forge owns — because it changes when V Forge does work, records what V Forge built
or did, or supports repeatable operation of execution surfaces — it likely belongs somewhere
else or requires governance review before it belongs in V Forge.

If in doubt, ask: did V Forge cause this to exist, or is it observing something external?
If V Forge caused it, it may belong here.
If it is observing something external, it belongs in VEDA.

---

## Usage

This document should be used:

- when deciding whether a proposed V Forge record or field represents canonical execution truth
- when reviewing whether a V Forge storage idea risks absorbing planning or observatory ownership
- when designing future surface execution condition schema to confirm it stays inside execution truth
- when evaluating whether V Forge signal consumption is drifting toward signal ownership
- when reviewing whether light-tracked surface records are expanding beyond their governed scope
- as the V Forge-local companion to `../interfaces/data-boundaries.md` for implementation decisions

---

## Related Docs

- `v-forge.md`
- `schema-authority.md`
- `schema-specification.md`
- `controlled-vocabularies.md`
- `surface-execution-state-design-note.md`
- `system-invariants.md`
- `../interfaces/data-boundaries.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../ecosystem/db-posture.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-009-no-direct-database-access.md`
- `../project-v/data-boundaries.md`
- `../veda/data-boundaries.md`
