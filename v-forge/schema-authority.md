# V Forge Schema Authority

## Purpose

This document defines the canonical schema authority for V Forge.

It exists to answer:

```text
What records does V Forge canonically own, what classes of records belong in
the first-pass schema, what belongs only as extension hooks, what does not
belong in V Forge schema at all, and how is schema expansion governed so
V Forge remains the execution system of record without absorbing planning
or observatory truth?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the canonical first-pass schema shape V Forge is allowed to own
- the meaning and ownership posture of each first-pass schema domain
- which schema domains are deeply modeled in first pass vs lightly tracked vs deferred
- the structural rules the schema must preserve
- the extension-hook posture for future domains
- how schema expansion must be governed without blurring system boundaries
- the anti-drift constraints operators and LLMs must preserve when extending V Forge schema

---

## Out of Scope

This document does not define:

- exact columns, exact SQL types, or exact indexes for every field
- detailed migration sequencing
- detailed endpoint contracts
- detailed controlled vocabulary enumerations
- VEDA schema design
- Project V schema design

Those belong in subordinate schema-specification, controlled-vocabularies,
API contract, and system-specific docs.

---

## System

- v-forge

---

## Core Rule

V Forge schema must model only canonical execution truth that V Forge owns.

V Forge schema must not model:

- canonical planning truth that belongs to Project V
- canonical observatory or signal truth that belongs to VEDA
- convenience copies of another system's canonical state
- raw SERP data, GA4 data, Search Console data, or YouTube observatory data
- planning decision records, readiness evaluations, or orchestration state

V Forge schema must remain:

- multi-project-safe
- explicit
- bounded to execution truth and its operational support structures
- queryable by real operator and LLM execution workflows
- hard to drift casually toward planning or observatory ownership

Consuming VEDA signal through the governed interface does not justify storing
that signal as canonical V Forge truth. Receiving a handoff from Project V does
not justify replicating planning state inside V Forge schema.

V Forge schema resides in V Forge's own database — separate from Project V's
database and VEDA's database. Cross-system data access occurs only through
governed APIs and interfaces. No system accesses another system's database
directly. This is an ecosystem-wide invariant per ADR-009.

---

## Relationship to V Forge Identity and Scope

This schema authority implements the identity established in `v-forge.md` and
the scope boundaries set by the V Forge initial scope decision.

### From `v-forge.md` — V Forge owns:
- execution truth
- the content graph of what was built
- release and publication continuity
- owned/branded execution surfaces
- operator playbooks, checklists, and execution guidance
- execution intelligence (as a query pattern, not stored observatory data)
- bounded execution-side research findings
- execution-side maintenance truth
- execution-side reporting

### From the initial scope decision — first pass supports:
- two first-class project types: content/affiliate and plugin/product
- deeply modeled surfaces: website and GitHub/release
- lightly tracked surfaces: YouTube, social, newsletter, store listings
- deferred domains: experimentation/optimization, SaaS/runtime/commercial,
  advanced engagement analytics, advanced graph features

This schema authority doc translates those ownership and scope commitments
into governed schema boundaries.

---

## Schema Authority Rule

This document is the canonical authority for the first-pass V Forge schema shape.

If implementation, migrations, route design, or convenience schema ideas diverge
from this document, the divergence must be reviewed explicitly.

Schema authority must not be inferred from:

- ad hoc route payloads
- migration convenience
- local implementation assumptions
- source material from legacy repos
- one-off operator expectations

If a proposed record family is not clearly justified here or in an explicitly
subordinate schema-specification doc, it is not yet governed schema.

---

## Scope Classification Rule

Every V Forge table or canonical record family must be classifiable as one of:

- **project-scoped** — belongs to exactly one project
- **intentionally global** — rare, must be justified
- **system metadata** — must not become a loophole for storing project truth
  or cross-system convenience state

### Rule
Project-scoped tables must belong to exactly one project.
Global tables must be rare and justified.
System metadata must not become a loophole for storing planning truth,
observatory truth, or cross-project convenience state.

### Project Identity Anchoring in V Forge

V Forge may maintain a thin local Project anchor record that carries
`project_id` and the minimal identity fields needed to scope V Forge
database records and enforce referential integrity.

This local anchor:
- is not a replication of Project V's planning state
- does not carry planning structure, readiness state, orchestration data,
  or any other Project V truth
- exists solely to support local execution scoping and bounded-system
  database integrity
- does not give V Forge authority over project identity, classification,
  or lifecycle

Project V remains the canonical owner of project identity and planning
structure. V Forge's local anchor is a foreign-key anchor, not a
planning record.

---

## What the Schema Governs

V Forge schema governs the persistent structured records needed to preserve
execution truth and support LLM-assisted project operation.

The schema exists so that a capable LLM, at any point in a project's lifecycle,
can query V Forge and answer:

- what surfaces does this project operate on?
- what has been built on each surface?
- what is the content graph structure?
- what has been published or released, when, and where?
- what content has been distributed to which surfaces?
- what needs maintenance?
- what playbook applies to the current task?
- what is the publication or release backlog?

These are execution-truth questions. The schema must support them.

---

## First-Pass Schema Domains

The first-pass V Forge schema is organized into seven domains.

### Domain 1 — Surface Registry

**Depth:** Core-modeled.

**Purpose:** The surface registry tracks what surfaces a project operates on,
what type each surface is, and what ownership class applies. It is the
foundational inventory that scopes all other V Forge records.

**Record families:**

`Surface` — The top-level registry of all surfaces a project operates on.
May carry governed structured metadata fields for surface-specific operational
configuration and tactic knowledge — for example, publishing cadence, preferred
content archetype constraints, or surface-specific operational norms. This is
where V Forge's execution-side tactic and application knowledge for a surface
lands as governed structured metadata, not as freeform notes or external docs.

`SurfaceSnapshot` — Periodic health and size snapshots per surface (subscriber
count, follower count, install count, page count, star count). Captures
surface-level vitals without full analytics.

**Ownership:** V Forge owns this canonically. No other system owns the surface
registry. Execution-side tactic knowledge specific to a surface is owned here,
not in a freeform external store.

**Constraints:**
- every surface belongs to exactly one project
- surface_type must use the controlled vocabulary
- ownership_class must use the controlled vocabulary (owned, operated, referenced)
- snapshot records must be project-scoped and surface-scoped

---

### Domain 2 — Content Graph

**Depth:** Core-modeled. This is V Forge's most important schema domain.

**Purpose:** The content graph is the structural model of what a project has
built. It describes pages, topics, entities, internal links, archetypes, and
schema usage. This is execution truth — it changes when V Forge does work.

Per ADR-002, the content graph belongs to V Forge. It does not belong in VEDA.

**Record families:**

`Page` — The core content graph unit. Carries URL, slug, title, content
archetype, primary topic, publication status, schema markup type, word count,
publish/modify/review dates, content decay status, and handoff reference.

`Topic` — The topical vocabulary of a project. Carries topic name, topic type,
optional parent topic reference for shallow hierarchy.

`Entity` — Named things that appear across pages. Carries entity name and
entity type (product, brand, person, tool, concept).

`InternalLink` — Link structure between pages. Carries source page, target page,
anchor text, and link type (contextual, navigational, related_post, footer).

`PageTopic` — Junction: page to topic, with is_primary flag.

`PageEntity` — Junction: page to entity, with optional mention context.

`ContentCluster` — Pillar-spoke grouping. Carries pillar page reference and
cluster name. Spoke pages link through their primary topic.

**Ownership:** V Forge owns this canonically per ADR-002. VEDA must not own or
maintain the content graph. Project V must not replicate it.

**Constraints:**
- all content graph records must be project-scoped
- page-topic junctions must only connect pages and topics from the same project
- page-entity junctions must only connect pages and entities from the same project
- internal links must only connect pages from the same project
- cross-project content graph connections are forbidden
  (per system invariant 8 — content graph integrity must be project-scoped)
- content_archetype, publication_status, schema_markup_type, topic_type,
  entity_type, and link_type must all use controlled vocabularies

---

### Domain 3 — Publication and Release Continuity

**Depth:** Core-modeled.

**Purpose:** Tracks the structured record of what has been published or released,
when, and at what state. This domain supports both continuous-publishing surfaces
(website pages edited in place) and release-oriented surfaces (versioned immutable
artifacts).

**Record families:**

`PublicationEvent` — Records every publish, update, republish, archive, or
redirect action on a continuous-publishing surface. Carries surface reference,
page reference, event type, timestamp, and handoff reference.

`Release` — The version-centric publication unit for release-oriented surfaces.
Carries surface reference (GitHub repo), version tag, release name, changelog
summary, prerelease flag, publish timestamp, asset count, and handoff reference.

`StorePublication` — Records when a release was published to a distribution
store surface. Carries release reference, store surface reference, published
version, publish timestamp, and status (pending_review, published, rejected).

**Ownership:** V Forge owns this canonically. Publication and release continuity
is execution truth.

**Constraints:**
- all records must be project-scoped
- PublicationEvent.page_id must reference a page in the same project
- Release.surface_id must reference a surface in the same project
- StorePublication.release_id must reference a release in the same project
- StorePublication.store_surface_id must reference a surface in the same project
- event_type and store_publication_status must use controlled vocabularies

---

### Domain 4 — Distribution Tracking

**Depth:** Core-modeled.

**Purpose:** Records cross-surface distribution actions. When a blog post is
promoted on social media, when a release is announced via newsletter, when a
YouTube video covers the same topic as a blog post — the distribution action
records that connection.

This is the primary cross-surface relational mechanism. It transforms V Forge
from a collection of per-surface trackers into an integrated multi-surface
execution system.

**Record families:**

`DistributionAction` — Records that surface X distributed content from surface Y.
Carries source surface, source content type and ID, distribution surface,
distribution URL, distribution timestamp, and notes.

**Ownership:** V Forge owns this canonically. Distribution tracking is
execution truth.

**Constraints:**
- all records must be project-scoped
- source surface and distribution surface must belong to the same project
- source_content_type must use a controlled vocabulary (page, release, video, newsletter_issue)

---

### Domain 5 — Playbook Routing

**Depth:** Core-modeled as metadata routing records, not as a workflow engine.

**Purpose:** Playbook records tell the LLM which playbook to load for a given
task type, surface type, and content archetype. The playbook registry is a
routing mechanism. Actual playbook content lives as structured docs or
checklists, referenced by path — not as deeply modeled step/action sequences
in the database.

This preserves V Forge as an execution system of record without turning it
into a workflow engine.

**Record families:**

`Playbook` — Metadata reference record. Carries playbook name, playbook type,
surface type scope, archetype scope, version, status, and doc path reference.
Playbook records are the schema-side routing home for execution-side tactic
knowledge that is workflow-shaped rather than surface-configuration-shaped.
Tactic knowledge that is surface-operational in nature belongs on `Surface`;
tactic knowledge that is task-workflow in nature is routed through `Playbook`.

**Ownership:** V Forge owns this canonically. Playbook routing is execution
guidance truth.

**Constraints:**
- playbooks are project-scoped (different projects may have different playbooks
  for the same task type)
- playbook_type must use a controlled vocabulary
- the doc_path field references playbook content; it does not store the content
  inline in the database
- playbook content is doctrine (belongs in docs) while playbook routing metadata
  is operational state (belongs in the database), consistent with ADR-007

---

### Domain 6 — Light-Tracked Operated Surfaces

**Depth:** Tracked but light. These domains have minimal first-pass schema
representation.

**Purpose:** YouTube, social, newsletter, and store listing surfaces are real
operated surfaces but are not deeply modeled in first pass. They get the minimum
records needed for distribution tracking and surface-level awareness.

**Record families:**

`Video` — Light YouTube video tracking. Carries YouTube video ID, title, publish
date, duration, visibility status, and optional linked page or release reference.

`SocialPost` — Light social post tracking. Carries content summary, post URL,
publish timestamp, and linked content type/ID.

`NewsletterIssue` — Light newsletter issue tracking. Carries subject, send date,
audience description, and aggregate-level open and click rates.

Store listing specifics are tracked through the Surface and SurfaceSnapshot
records in Domain 1, plus the StorePublication records in Domain 3. No
additional store-listing-specific record family is needed in first pass.

**Ownership:** V Forge owns these as execution-adjacent operational records.
They are not observatory truth.

**Constraints:**
- all records must be project-scoped
- all records must reference a surface in the same project
- these record families are intentionally minimal; they must not expand into
  full platform-specific content management without governed schema expansion
- engagement metrics beyond basic newsletter open/click rates are not first-pass
  schema; they are extension hooks

---

### Domain 7 — Execution Continuity Support

**Depth:** Core-modeled where needed.

**Purpose:** Records that support execution lifecycle tracking, handoff receipt,
finding production, and maintenance state. These exist to preserve the execution
continuity required by system invariant 11.

**Record families:**

`ExecutionEntry` — The V Forge-side receipt of work entering execution. Records
that a handoff arrived, references the handoff ID from Project V, and anchors
subsequent execution tracking to that entry point. Does not replicate planning
content — carries only the reference and local execution state.

`ExecutionFinding` — A bounded finding produced during execution. Records a
specific finding (issue, changed condition, blocker, decision point) scoped to
an active execution entry. Findings are execution-originated and bounded — they
do not become a shadow planning system.

`ReturnToPlanning` — A record that a finding or condition was formally returned
to Project V for planning reconsideration. Carries a reference to the originating
execution finding and the return timestamp. This is the schema representation of
the V Forge-to-Project V return path.

`MaintenanceRecord` — A record of maintenance activity performed on an execution
asset (a surface, a page, a release). Carries asset reference, maintenance type,
person or agent that performed it, timestamp, and outcome summary.

These families will be specified in full detail (columns, types, constraints)
in the subordinate schema-specification doc. The family boundaries defined here
must be the starting point — do not invent new families without governed review.

This domain must not replicate Project V planning state. It tracks what
happened in execution, not what was planned.

**Ownership:** V Forge owns this canonically.

**Constraints:**
- all records must be project-scoped
- handoff receipt records reference the handoff but do not replicate
  planning truth from Project V
- findings records must remain bounded to execution-originated findings;
  they must not become a shadow planning system

---

## Extension Hooks

The following domains are not part of first-pass schema but have natural
attachment points in the schema for future extension.

### Engagement metrics per distribution action
DistributionAction can later add performance fields (clicks, impressions,
conversions) without restructuring. Deferred because engagement analytics
crosses into VEDA signal territory and the ownership boundary needs careful
design before schema representation.

### Deep YouTube metadata
Video record can later add tags, category, chapters, thumbnail URL, end screens,
and cards when YouTube workflow modeling is needed. The YouTube video ID foreign
key is the extension anchor.

### Social engagement metrics
SocialPost can later add impression count, like count, reply count, retweet
count when social analytics modeling is warranted.

### Newsletter subscriber management
Newsletter surface can later link to subscriber segment records, automation
sequence records, and per-link click tracking when full email operations are
in scope.

### Content scoring
Page can later add computed content_score, seo_score, readability_score fields
when scoring methodology is defined.

### Experimentation and optimization
Page can later add experiment_id and variant_id when A/B testing is in scope.
This is explicitly a future extension per `v-forge.md` and must not be designed
into base schema.

### Surface execution condition
Surface execution condition is a recognized future extension hook for representing
the current operational condition, readiness, or execution-state posture of a
specific operated surface when V Forge needs more than static surface metadata or
periodic snapshots.

This hook is intentionally not first-pass schema.
It is acknowledged because some future V Forge workflows may need a governed way
to represent statements such as:
- this surface is ready for routine execution
- this surface is blocked by a surface-local condition
- this surface is under temporary execution constraint
- this surface requires heightened handling before certain execution actions

If admitted later, this hook must:
- remain execution-side operational truth, not planning truth
- remain surface-local rather than becoming a generic orchestration layer
- avoid duplicating release state, maintenance state, or planning readiness where existing records already cover the need
- be introduced through governed schema expansion rather than speculative pre-build

The current design anchor for this hook is `surface-execution-state-design-note.md`.
That design note is not schema authority by itself. It is the preserved design thread for future governed expansion.

### Advanced content graph features
Entity relationships beyond page-entity junctions, semantic clustering, topic
hierarchy depth beyond one level. These can extend naturally from existing
Topic and Entity records later.

### Rule for extension hooks
Extension hooks must not be pre-built into first-pass schema as empty columns,
nullable foreign keys, or speculative junction tables. The extension point is
the existing record family to which new fields or related records would attach.
Building speculative schema for unscoped future domains is not governed schema
expansion — it is drift.

---

## What the Schema Does Not Govern

V Forge schema does not govern and must not contain:

### Planning truth
Project V planning records, readiness evaluations, orchestration state,
decision records, audit records, and planning-side traceability belong to
Project V. V Forge schema must not replicate them.

### Observatory truth
VEDA observatory records — SERP snapshots, GA4 observations, Search Console
data, YouTube observatory records, keyword intelligence, evidence provenance —
belong to VEDA. V Forge schema must not store them.

V Forge consumes bounded VEDA signal through the governed VEDA-to-V-Forge
signal interface. That consumption produces execution intelligence as a
query-time cross-referencing of content graph against consumed signal.
The raw signal does not become a V Forge schema record.

### Raw provider data
Raw data from external providers (Ahrefs, Google APIs, social platform APIs)
belongs to VEDA where it is observatory data, or is ephemeral where it is
not retained. V Forge does not warehouse raw provider data.

### Execution intelligence as stored records
Execution intelligence is a query pattern, not a stored record family. It is
the cross-referencing of V Forge's content graph against VEDA's signal at
query time. The inputs (content graph records, VEDA signal) are owned by their
respective systems. The analytical output belongs to V Forge as a derived
computation, not as a separate stored canonical record.

If execution intelligence outputs need to be preserved for reporting or
continuity, they belong in execution-side reporting records with clear
provenance — not as a parallel observatory record set.

### SaaS, runtime, or commercial truth
These are explicitly deferred future extension domains per `v-forge.md`.
They must not be designed into base schema.

### Cross-project data
V Forge schema is project-scoped. Cross-project queries, portfolio views,
and cross-project content graph connections are not first-pass schema concerns.

---

## Schema Expansion Rule

Schema expansion beyond the first-pass domains defined in this document requires
governed review.

### What triggers a schema expansion review:
- a proposed new record family
- a proposed new domain that does not fit within the seven first-pass domains
- a proposed field that introduces a new controlled vocabulary
- a proposed relationship that connects V Forge records to another system's
  canonical records beyond the thin reference model
- a proposed change that broadens V Forge ownership posture

### What a schema expansion review must confirm:
- the proposed addition is execution truth that V Forge should own
- the proposed addition does not replicate planning truth or observatory truth
- the proposed addition preserves project-scoped integrity
- the proposed addition has a governed controlled vocabulary where applicable
- the proposed addition has been documented before it is implemented
- hammer coverage can be extended to verify the new schema element

### What is not schema expansion:
- adding a new value to an existing controlled vocabulary (governed by the
  controlled-vocabularies doc, not this doc)
- adding an index to improve query performance
- adjusting a field type or constraint within the same semantic meaning

---

## Anti-Drift Rules

V Forge schema has drifted if:

### 1. Observatory truth appears in V Forge tables
If V Forge schema contains SERP snapshots, GA4 observation records, Search
Console coverage data, keyword intelligence records, or any raw observatory
data that should belong to VEDA, the schema has drifted.

### 2. Planning truth appears in V Forge tables
If V Forge schema contains planning decision records, readiness evaluations,
orchestration state, or project lifecycle records that should belong to
Project V, the schema has drifted.

### 3. Signal is stored as canonical V Forge truth
If consumed VEDA signal is stored in V Forge schema as though V Forge
originated it — rather than as a derivative reference within an execution
report or finding — the schema has drifted.

### 4. Light-tracked surfaces become deeply modeled without governance
If YouTube, social, newsletter, or store listing record families expand
significantly beyond their minimal first-pass shape without a governed schema
expansion review, the schema has drifted.

### 5. Extension hooks are pre-built
If first-pass schema contains empty columns, speculative junction tables,
or placeholder record families for unscoped future domains (experimentation,
SaaS/runtime, advanced engagement), the schema has drifted.

### 6. Playbook routing becomes a workflow engine
If the playbook record family expands to include step sequences, action nodes,
condition branches, or execution state tracking that turns V Forge into a
workflow orchestration system, the schema has drifted.

### 7. Cross-project data appears
If any V Forge record connects data from two different projects, or if
a query pattern requires cross-project joins, the schema has drifted.
Per system invariant 8, content graph integrity must be project-scoped.

### 8. Execution intelligence becomes stored observatory data
If execution intelligence outputs are stored in a record family that
resembles VEDA observatory tables — with raw signal data, observation
timestamps, and provider attribution — rather than as bounded execution
findings with clear V Forge provenance, the schema has drifted.

### 9. Surface execution condition becomes a shadow orchestration layer
If a future surface execution condition hook is implemented in a way that:
- duplicates planning readiness or planning-side gating
- becomes a generalized cross-surface workflow engine
- overrides release, maintenance, or return posture rather than complementing them
- stores speculative future posture rather than current execution-side condition
then the schema has drifted.

---

## Integrity Rules

### 1. No orphaned project-scoped records
A project-scoped row must not exist without a valid project anchor.

### 2. No illegal cross-project relations
If one project-scoped row references another, project compatibility must
be enforced. A page-topic junction connecting a page from project A to a
topic from project B must fail.

### 3. Content graph integrity must be structurally enforced
Cross-project content graph contamination is a structural failure per system
invariant 8. Critical integrity should be enforced at the database layer
where practical, not only in application logic.

### 4. Uniqueness must match real ownership scope
If a key or identifier is unique only within a project, uniqueness must
include project_id in the constraint.

### 5. Surface references must be project-consistent
Any record that references a surface must reference a surface belonging
to the same project.

### 6. Publication and release records must trace to surfaces
PublicationEvent, Release, and StorePublication records must reference
surfaces and content that belong to the same project.

### 7. Distribution actions must be intra-project
DistributionAction source and distribution surfaces must belong to the
same project.

### 8. Controlled vocabularies must be enforced
Fields that use controlled vocabularies must enforce valid values. The
valid values are defined in the subordinate controlled-vocabularies doc,
not invented at implementation time.

---

## Required Common Fields Posture

Project-scoped record families should strongly prefer the following where relevant:

- `id` — stable primary key
- `project_id` — project ownership anchor
- `created_at` — creation timestamp
- `updated_at` — last modification timestamp

Additional common fields where applicable:
- `status` — where the record has a meaningful lifecycle
- `surface_id` — where the record belongs to a specific surface
- `handoff_ref` — where the record was produced by a specific handoff

Not every record family needs every field, but omission must be deliberate.

---

## Index Posture

The first-pass schema should be indexable for real multi-project,
multi-surface access patterns.

At minimum, schema design should support queries such as:

- list surfaces for a project
- list pages for a project, filterable by archetype and publication status
- list pages by content decay status
- list topics for a project
- list internal links for a project
- list pages for a topic (through PageTopic)
- list publication events for a surface
- list releases for a project
- list store publications for a release
- list distribution actions for a project, filterable by source or distribution surface
- list playbooks for a project, filterable by type and surface scope
- list videos, social posts, newsletter issues for a project

This implies deliberate indexing on:

- `project_id`
- `surface_id`
- common status and type filters
- common relation joins (page-topic, page-entity, source-target links)
- common date ordering fields

---

## Ordering Rule

List surfaces must have deterministic ordering.

Schema design must support predictable ordering with stable tie-breakers.

---

## JSON Rule

JSON fields may be used only where flexible payload storage is genuinely
justified, such as:

- imported external metadata traces from handoff packages
- bounded metadata with truly variable shape per surface type

JSON must not become a substitute for unresolved schema design.

### Rule
If a concept is important enough to govern, query, validate, or classify
repeatedly, it probably needs explicit schema rather than a JSON field.

---

## Freeze Posture

This first-pass schema set should be treated as the governed base.

After approval:

- endpoint and mutation design should conform to it
- later schema additions should be exceptional
- schema expansion requires governance review

This is not a ban on future change. It is a ban on casual schema drift.

---

## Companion Implementation Rule

Before implementation begins, each first-pass record family above should be
converted into a more specific schema specification with:

- exact columns
- exact types
- exact relations
- exact constraints
- exact indexes

That specification is subordinate to this authority doc. It must not silently
replace or override it.

The subordinate docs are:
- `schema-specification.md` — exact column-level schema
- `controlled-vocabularies.md` — exact enumeration values for all controlled vocabulary fields
- `data-boundaries.md` — V Forge-specific data ownership boundary rules

---

## Human-In-The-Loop Principle

Schema authority is governance-sensitive because schema shape determines what
V Forge can and cannot become.

Human review is required where schema change would:

- broaden V Forge's ownership posture
- introduce new record families
- increase cross-system reference depth
- weaken multi-project integrity
- add record families that resemble planning truth or observatory truth
- promote a light-tracked surface to deeply modeled status

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- V Forge schema must stay strictly inside execution truth
- the content graph is V Forge's most important schema domain
- first-pass schema covers seven domains: surface registry, content graph,
  publication/release continuity, distribution tracking, playbook routing,
  light-tracked surfaces, and execution continuity support
- website and GitHub/release surfaces are deeply modeled; YouTube, social,
  newsletter, and store listings are lightly tracked
- VEDA signal is consumed through the governed interface, not owned in V Forge schema
- execution intelligence is a query pattern, not a stored record family
- extension hooks exist but must not be pre-built
- surface execution condition is a recognized future extension hook, not a first-pass schema feature
- schema expansion requires governed review, not implementation convenience

If schema design makes V Forge broader, more planning-shaped, more
observatory-shaped, less project-safe, or harder to classify as execution
truth, the doctrine is wrong.

---

## Usage

This document should be used:

- when deciding whether a proposed record family belongs in V Forge schema
- when evaluating whether a schema concept is first-pass, extension-hook, or out of bounds
- when writing subordinate schema-specification or controlled-vocabularies docs
- when reviewing whether schema ideas preserve multi-project integrity and
  ownership boundaries
- when rejecting convenience-driven schema drift

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `surface-execution-state-design-note.md`
- `vs-project-v.md`
- `vs-veda.md`
- `human-in-the-loop-doctrine.md`
- `reporting-and-approval-model.md`
- `operator-surfaces/vscode-extension.md`
- `hammer-doctrine.md`
- `hammer-plan.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../ecosystem/doctrine-vs-operational-state.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-007-docs-are-build-spec-db-owns-operational-state.md`
- `../ecosystem/decisions/ADR-009-no-direct-database-access.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/data-boundaries.md`
- `../project-v/schema-authority.md`
