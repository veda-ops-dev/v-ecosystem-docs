# VEDA Schema Reference

## Purpose

This document is the implementation-facing schema reference for VEDA in the shared-root authority.

It exists to answer:

```text
What record families does VEDA own canonically, what is their implementation-facing shape,
what ownership constraints and provenance rules apply, and how must VEDA's schema remain
faithful to its pure-observatory role without drifting back into planning, execution,
or content-graph ownership?
```

Read this with:

- `veda.md`
- `system-invariants.md`
- `data-boundaries.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `../ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-003-veda-brain-eliminated.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- what record families VEDA canonically owns
- the implementation-facing shape of each family's primary fields
- identity, timestamp, status, and provenance-relevant field posture
- how project scoping is represented across VEDA records
- how provider and source provenance is preserved in schema
- what belongs in explicit columns vs bounded JSON payloads
- what record families have been eliminated or transferred and must not be recreated
- anti-drift rules that keep VEDA schema aligned with observatory-only posture

---

## Out of Scope

This document does not define:

- database migration scripts or migration sequencing
- the full API or MCP surface contract for VEDA routes
- provider-specific ingest implementation details
- V Forge content graph schema — that belongs in V Forge authority docs
- Project V planning schema — that belongs in `../project-v/schema-specification.md`
- detailed operator-surface or UI rendering behavior
- VEDA signal package payload formats — those belong in the interface docs

---

## System

- veda

---

## Core Rule

VEDA schema represents observatory truth only.

Every table VEDA owns must be explainable as something an observatory records about external reality, governs as a scoping container for those records, or logs as a state change to observatory-owned records.

If a proposed table or field does not satisfy that test, it does not belong in VEDA schema.

This is not a preference. It is the direct schema-level consequence of ADR-001 (VEDA is a pure observatory), ADR-002 (content graph moves to V Forge), and ADR-003 (VEDA Brain eliminated).

---

## Observability Ownership Rule

VEDA canonically owns:

- project partitioning containers for observatory scoping
- source capture and source item intake records
- the observatory event log
- keyword observation targets
- SERP snapshot observation records
- search performance observation records
- bounded observability configuration

VEDA does not own:

- the content graph — pages, topics, entities, internal links, schema usage, archetypes, surfaces, sites — those belong to V Forge (ADR-002)
- planning truth of any kind — objectives, initiatives, work items, decisions — those belong to Project V
- execution truth — draft lifecycle, publishing workflow, production assets — those belong to V Forge
- VEDA Brain intelligence synthesis — that does not exist (ADR-003)

The content graph domain was previously in VEDA. ADR-002 formally transferred it to V Forge. The `Cg*` record families (`CgPage`, `CgTopic`, `CgEntity`, `CgSurface`, `CgSite`, `CgContentArchetype`, `CgPageTopic`, `CgPageEntity`, `CgInternalLink`, `CgSchemaUsage`) no longer belong to VEDA schema. They must not be recreated in VEDA under any name.

---

## Design Principle

VEDA's schema follows the core observatory pattern:

```text
entity + observation + time + interpretation
```

Where applicable, this means:

- an identifiable observed entity or external surface
- a concrete observation or evidence record with capture time
- explicit time context, especially for observation ledger records
- bounded interpretation layered on top, clearly subordinate to canonical observation records

Schema decisions must preserve this pattern. Tables that do not fit it are either misclassified or belong in another system.

---

## Canonical Record Families

VEDA owns the following canonical record families in the first-pass shared-root build. Each family is described with its primary fields, identity conventions, and constraints.

---

### 1. Project (Observatory Partitioning)

**Purpose:** Thin project-scoping container. Every VEDA observatory record belongs to exactly one project. This record exists to enforce multi-project isolation, not to model planning truth.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `name` | text | Human-readable project name |
| `slug` | text | Stable machine key, globally unique |
| `description` | text? | Optional |
| `lifecycleState` | enum | `created`, `bootstrapping`, `active`, `paused`, `archived` |
| `createdAt` | timestamptz | |
| `updatedAt` | timestamptz | |

**Constraints:**
- `slug` must be globally unique
- `lifecycleState` must use the governed enum

**Ownership rule:** This is VEDA's observatory partition record. It is not a rich planning orchestration record. Project V owns the canonical planning version of project identity. VEDA's `Project` record exists only to scope observatory data.

**Mutation rule:** `lifecycleState` may be updated. This is a governance record, not a pure append-only observation. State changes to this record must emit an `EventLog` entry.

---

### 2. SourceFeed (Recurring External Source)

**Purpose:** Represents a recurring external source that VEDA monitors or ingests from. Examples: RSS feeds, channel-like external sources, durable ingest streams.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `projectId` | uuid | FK → Project; project-scoped |
| `name` | text | Operator-visible label |
| `feedUrl` | text | Canonical URL for the feed |
| `platform` | enum | Platform classification |
| `platformLabel` | text? | Optional human label for the platform instance |
| `isActive` | boolean | Whether the feed is currently being ingested |
| `createdAt` | timestamptz | |
| `updatedAt` | timestamptz | |

**Constraints:**
- `(projectId, feedUrl)` must be unique — one feed URL per project
- `platform` must use the governed platform enum

**Relationships:**
- one-to-many: `SourceFeed` → `SourceItem`

**Mutation rule:** `isActive`, `name`, `platformLabel` are mutable governance fields. `feedUrl` and `platform` should be treated as identity fields after creation.

---

### 3. SourceItem (Captured External Item)

**Purpose:** Represents an individual captured external item — a webpage, comment, video reference, or other source artifact. This is one of the primary observatory intake tables.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `projectId` | uuid | FK → Project; project-scoped |
| `sourceType` | enum | `rss`, `webpage`, `comment`, `reply`, `video`, `other` |
| `platform` | enum | Platform classification |
| `url` | text | Source URL |
| `capturedAt` | timestamptz | When this item was captured |
| `capturedBy` | enum | `human`, `llm`, `system` |
| `contentHash` | text | Hash of source content for deduplication |
| `snapshotRef` | text? | Reference to snapshot storage location |
| `snapshotMime` | text? | MIME type of snapshot |
| `snapshotBytes` | int? | Snapshot size in bytes |
| `operatorIntent` | text | Why this item was captured — required provenance field |
| `notes` | text? | Optional operator notes |
| `status` | enum | `ingested`, `triaged`, `used`, `archived` |
| `archivedAt` | timestamptz? | Set when status transitions to `archived` |
| `sourceFeedId` | uuid? | Optional FK → SourceFeed |
| `createdAt` | timestamptz | |
| `updatedAt` | timestamptz | |

**Constraints:**
- `(projectId, url)` must be unique — one capture per URL per project
- `capturedBy` must use the governed enum
- `operatorIntent` must be non-empty — it is a required provenance field

**Provenance rule:** `capturedBy` and `operatorIntent` are provenance fields. They must not be suppressed or defaulted silently. They exist so later review can determine who introduced an item and why.

**Mutation rule:** `status`, `notes`, `archivedAt` are mutable. `url`, `contentHash`, `capturedAt`, `capturedBy`, and `operatorIntent` are creation-time identity/provenance fields that must not be changed after creation.

---

### 4. EventLog (Observatory Event Audit Trail)

**Purpose:** Canonical append-only observatory event ledger. Records meaningful state transitions and observatory-significant events inside the VEDA boundary. This is durable audit history, not a general analytics sink.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `projectId` | uuid | FK → Project; project-scoped |
| `eventType` | enum | Governed observatory event vocabulary |
| `entityType` | enum | The model discriminator for `entityId` |
| `entityId` | uuid | Identity of the affected observatory record |
| `actor` | enum | `human`, `llm`, `system` |
| `details` | jsonb? | Bounded structured event details |
| `timestamp` | timestamptz | Event time |

**Constraints:**
- `eventType` must use the governed event-type vocabulary — see Controlled Vocabularies section below
- `entityType` must use the governed entity-type vocabulary — see Controlled Vocabularies section below
- `actor` must use the governed actor-type enum
- this table is append-only: no updates, no deletes

**Atomicity rule:** EventLog entries required by a state-change mutation must be written in the same transaction as that state change. A state change that requires an event log entry must not commit without the corresponding event row.

**Scope rule:** EventLog records must not be emitted for read-only operations. This table is a state-change audit trail, not a request log or analytics feed.

---

### 5. KeywordTarget (Search Observation Target)

**Purpose:** Represents a governed decision to observe a specific query within a locale and device scope. This is a target-definition record, not an observation record itself. It records what the project chooses to watch.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `projectId` | uuid | FK → Project; project-scoped |
| `query` | text | The search query being observed |
| `locale` | text | Locale for observation scope |
| `device` | text | Device context for observation scope |
| `isPrimary` | boolean | Whether this is a primary observation target |
| `intent` | text? | Optional classification of query intent |
| `notes` | text? | Optional operator notes |
| `createdAt` | timestamptz | |
| `updatedAt` | timestamptz | |

**Constraints:**
- `(projectId, query, locale, device)` must be unique — one target definition per query scope per project

**Mutation rule:** `isPrimary`, `intent`, `notes` are mutable governance fields. `query`, `locale`, `device` are identity fields that must not change after creation — a new target must be created instead.

**Ownership rule:** `KeywordTarget` records what VEDA is watching. They are governance records, not observation records. Observation results from this target are stored in `SERPSnapshot`.

---

### 6. SERPSnapshot (SERP Observation Record)

**Purpose:** Represents an immutable SERP observation at a specific capture time. This is one of the primary historical observation ledgers in VEDA. Each snapshot is an append-friendly record of what SERP showed for a given query scope at a given moment.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `projectId` | uuid | FK → Project; project-scoped |
| `query` | text | The search query observed |
| `locale` | text | Observation locale |
| `device` | text | Observation device context |
| `capturedAt` | timestamptz | When this SERP was captured |
| `validAt` | timestamptz? | When the SERP data was valid, if different from capture time |
| `rawPayload` | jsonb | Full provider response payload — evidence archive |
| `payloadSchemaVersion` | text? | Schema version of the raw payload |
| `aiOverviewStatus` | enum | `present`, `absent`, `parse_error` |
| `aiOverviewText` | text? | Extracted AI overview text if present |
| `source` | text | Provider or ingest source identifier |
| `batchRef` | text? | Optional reference to the ingest batch |
| `createdAt` | timestamptz | |

**Constraints:**
- `(projectId, query, locale, device, capturedAt)` must be unique — one observation per query scope per capture moment per project
- `aiOverviewStatus` must use the governed enum

**Immutability rule:** `SERPSnapshot` records are append-friendly. A new observation produces a new row. Prior snapshot rows must not be silently overwritten. The historical record must remain intact.

**Raw payload rule:** `rawPayload` preserves the full provider evidence archive. Promoted fields (`aiOverviewStatus`, `aiOverviewText`) exist for efficient querying. Hot-path meaning must be promoted to explicit columns; `rawPayload` is evidence support, not the only home of meaning.

**YouTube SERP observation placement:** YouTube query-level SERP observations use the `SERPSnapshot` family in the first pass. This aligns with VEDA-001's posture that a vendor SERP source is the primary snapshot instrument for YouTube. The `query`, `locale`, and `device` fields accommodate YouTube query context within the same family. A separate `YouTubeSnapshot` family does not exist and must not be created without explicit future governance. YouTube enrichment data from the YouTube Data API (metadata, channel data, statistics) is not currently mapped to any governed family — it must not be stored in ad hoc tables and must await governed family specification before implementation.

---

### 7. SearchPerformance (GSC/Performance Observation Record)

**Purpose:** Represents query × page × date-range performance observations, primarily from Google Search Console. Pure URL-based observation — no planning or execution coupling.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `projectId` | uuid | FK → Project; project-scoped |
| `pageUrl` | text | The observed page URL |
| `query` | text | The search query observed |
| `impressions` | int | Impression count for the window |
| `clicks` | int | Click count for the window |
| `ctr` | float | Click-through rate |
| `avgPosition` | float | Average SERP position |
| `dateStart` | timestamptz | Start of the observation window |
| `dateEnd` | timestamptz | End of the observation window |
| `capturedAt` | timestamptz | When this record was ingested |

**Constraints:**
- `(projectId, query, pageUrl, dateStart, dateEnd)` must be unique — one observation per query + page + date window per project

**URL posture:** `pageUrl` is a raw URL string, not a FK to any VEDA-owned page record or V Forge content graph record. The `SearchPerformance` family does not depend on the content graph and must not be used to create a hidden dependency on it. This prohibition applies not only to direct FK relationships, but also to derived tables, junction tables, or any equivalent semantic coupling that would attach `SearchPerformance` rows to content graph entities such as pages, topics, or entities. See Anti-Drift Rule 7 for the explicit prohibition.

**Immutability rule:** Performance observation records are append-friendly. A new ingest for the same window replaces the prior record where uniqueness constraints allow — but historical records for completed windows should not be silently modified after the fact.

---

### 8. SystemConfig (Global Observability Configuration)

**Purpose:** Global observability configuration. Intentionally not project-scoped. Used for bounded system-level configuration where observatory posture genuinely requires a global value.

**Key fields:**

| Field | Type | Notes |
|---|---|---|
| `id` | uuid | Primary key |
| `key` | text | Globally unique configuration key |
| `value` | jsonb | Configuration value — may include per-project overrides in the value JSON |
| `updatedBy` | enum | `human`, `llm`, `system` |
| `updatedAt` | timestamptz | |

**Constraints:**
- `key` must be globally unique
- `updatedBy` must use the governed actor-type enum

**Global exception rule:** `SystemConfig` is an intentional exception to the project-scoped default. It must remain small. It must not become a catch-all for unclassified application state. Every key stored here should be justified as genuinely requiring global scope.

**Per-project override pattern:** Where a configuration value has a default but allows per-project overrides, the pattern is: `{ "default": value, "overrides": { "<projectId>": value } }` stored in the `value` JSON. This avoids proliferating separate project-scoped config tables for globally-defaulted settings.

---

## Deferred Owned Domains

The following observatory domains are owned by VEDA per the Observability Ownership Rule but do not yet have a governed canonical record family in this first-pass schema reference.

These domains are **owned but deferred**. Their absence from the Canonical Record Families section above is an implementation deferral, not a reclassification of ownership.

### GA4 observations

VEDA owns Google Analytics 4 performance observations. No `GA4Observation` or equivalent record family exists in the first-pass schema. This domain must not receive ad hoc tables or local schema invention. Its canonical family design must be governed and added to this document before implementation promotes it into active schema authority.

### YouTube enrichment data

VEDA owns YouTube search and channel observatory data. YouTube query-level SERP observations land in `SERPSnapshot` per VEDA-001. YouTube enrichment data from the YouTube Data API — including video metadata, channel metadata, and statistics snapshots — does not yet have a governed canonical family. This must not receive ad hoc tables. Its family design must be governed through a future VEDA architecture decision and added here before implementation.

### Rule: No ad hoc tables for deferred domains

A deferred domain must not receive an implementation-local table, a provisional schema, or a JSON convenience blob that substitutes for governed family design. Adding schema for a deferred domain without first governing the family through a documented architecture decision and updating this document is a boundary violation.

---

## Controlled Vocabularies

The following controlled vocabularies govern field values across VEDA schema. These are implementation-facing enumerations, not free-form strings.

### SourceType
Governs `SourceItem.sourceType`.

Values: `rss`, `webpage`, `comment`, `reply`, `video`, `other`

### Platform
Governs `SourceItem.platform`, `SourceFeed.platform`.

Values: `website`, `x`, `youtube`, `github`, `reddit`, `hackernews`, `substack`, `linkedin`, `discord`, `other`

### SourceItemStatus
Governs `SourceItem.status`.

Values: `ingested`, `triaged`, `used`, `archived`

### CapturedBy / ActorType
Governs `SourceItem.capturedBy`, `EventLog.actor`, `SystemConfig.updatedBy`.

Values: `human`, `llm`, `system`

### ProjectLifecycleState
Governs `Project.lifecycleState`.

Values: `created`, `bootstrapping`, `active`, `paused`, `archived`

### AiOverviewStatus
Governs `SERPSnapshot.aiOverviewStatus`.

Values: `present`, `absent`, `parse_error`

### EntityType (EventLog discriminator)
Governs `EventLog.entityType`. Identifies which VEDA model the `entityId` references.

Current first-pass values:
`sourceItem`, `sourceFeed`, `searchPerformance`, `keywordTarget`, `serpSnapshot`, `vedaProject`

Note: The content graph entity type values (`cgSurface`, `cgSite`, `cgPage`, etc.) were present in the legacy schema. They must not be included here — those entity types belong to V Forge after ADR-002.

### EventType (EventLog vocabulary)
Governs `EventLog.eventType`. Must remain observatory-scoped.

Current first-pass values:
`SOURCE_CAPTURED`, `SOURCE_TRIAGED`, `SYSTEM_CONFIG_CHANGED`, `PROJECT_CREATED`, `KEYWORD_TARGET_CREATED`, `SERP_SNAPSHOT_RECORDED`

Note: Event types for content graph operations (`CG_SURFACE_CREATED`, `CG_PAGE_CREATED`, etc.) were present in the legacy schema. They must not be included here — those events belong to V Forge after ADR-002.

**Vocabulary change rule:** New vocabulary values for any of these enumerations must not be added locally by implementation. Additions require updating this document through governed review. A value not listed here is not a valid governed value.

---

## Record Reference and Identity Rules

### Primary keys
All VEDA records use UUID primary keys generated by the database (`gen_random_uuid()` or equivalent). Caller-supplied IDs are not permitted.

### Timestamps
All tables must carry at minimum `createdAt`. Mutable records must also carry `updatedAt`. Observation records that are append-only carry `createdAt` only.

Timestamp fields use `timestamptz` (timezone-aware) throughout.

### Project scoping
All records except `SystemConfig` are project-scoped through a `projectId` FK to `Project`. Project-scoped records must carry this FK with a `NOT NULL` constraint and a `Restrict` or equivalent delete behavior to prevent orphaned records.

### Uniqueness constraints
Uniqueness constraints are listed in each family section above. Natural unique keys prevent duplicate ingest of the same observation for the same scope. They also enforce project isolation — a uniqueness constraint that spans `(projectId, ...)` ensures that two projects' records cannot collide at the constraint level.

### Foreign keys and cross-table references
Where one VEDA record references another VEDA record, that reference must be project-consistent. A `SourceItem` belonging to project A must not reference a `SourceFeed` belonging to project B. Same-project FK integrity must be enforced at the application layer where not enforceable at the DB constraint level.

VEDA records must not carry FKs to Project V tables or V Forge tables. Cross-system reference uses locators, URLs, or external identifiers, not FK relationships.

---

## Provenance and Source Rules

### Required provenance fields

These fields are not optional annotations — they are part of evidence integrity:

- `SourceItem.capturedBy` — who or what introduced the source item
- `SourceItem.operatorIntent` — why the item was captured; must be non-empty
- `SourceItem.capturedAt` — when the item was captured
- `SERPSnapshot.source` — which provider or ingest path produced this snapshot
- `SERPSnapshot.capturedAt` — when the observation was recorded
- `EventLog.actor` — who or what caused the event
- `EventLog.timestamp` — when the event occurred

These fields must not be suppressed, silently defaulted, or treated as optional in implementation. They exist so later review can assess evidence basis and trust posture.

### Raw payload posture

`SERPSnapshot.rawPayload` stores the full provider response. This is the evidence archive. Implementation rules:

- fields used for common querying or filtering must be promoted to explicit columns (`aiOverviewStatus`, `aiOverviewText` are existing examples)
- `rawPayload` must not be the only home of any field required for governed system logic
- `rawPayload` is supporting evidence, not the primary query target
- raw payload retention decisions (archival, compression, expiry) require explicit governance, not silent implementation choices

### Derivation boundary

Where VEDA produces derived outputs (summaries, diagnostics, search intelligence, signal packages), those outputs must remain clearly subordinate to the canonical observation records that produced them. Derived outputs must not become a second canonical truth store. They must remain labeled as derived and reconstructible against source observation data.

The VEDA search intelligence layer produces compute-on-read interpretation of `SERPSnapshot`, `SearchPerformance`, and `KeywordTarget` records. That interpretation must not be materialized into separate canonical tables unless there is a documented operational justification per the derived data rules in `data-boundaries.md`.

---

## Project Association and Boundary Rules

### Multi-project isolation

VEDA must preserve multi-project isolation as a structural constraint, not a courtesy. This means:

- every project-scoped record has a `projectId` FK that must be valid and non-null
- list queries must be scoped to the active project — returning records from other projects is a boundary failure
- uniqueness constraints must span `projectId` to prevent cross-project collision
- delete or cascade behavior must not allow orphaned records that cross project scope

### Cross-system reference posture

VEDA records may need to reference external URLs, provider record identifiers, or cross-system locators for evidence purposes. These references must be stored as text fields (URL strings, external IDs, locators), not as FK relationships to tables in other systems' databases.

A VEDA record referencing a V Forge content graph page does so by storing a URL or external identifier, not by carrying a FK to V Forge's `Page` table. The same applies to Project V references. Cross-system FKs are forbidden.

### VEDA Project vs Project V Project

VEDA's `Project` record is a thin observatory partitioning container. It exists to scope observatory records. It is not synchronized with or a mirror of Project V's planning project record. Both may use the same project slug as a coordination convention, but VEDA's `Project` does not own planning state, and Project V's planning project record does not own observatory partitioning state. They are distinct records with distinct purposes.

---

## Records Eliminated or Transferred — Do Not Recreate

The following record families were present in the legacy VEDA schema. They have been formally eliminated or transferred and must not be recreated in VEDA under any form.

### Transferred to V Forge (ADR-002)

The entire content graph domain belongs to V Forge:

- `CgSurface`
- `CgSite`
- `CgPage`
- `CgContentArchetype`
- `CgTopic`
- `CgEntity`
- `CgPageTopic`
- `CgPageEntity`
- `CgInternalLink`
- `CgSchemaUsage`

These models, their associated enums (`CgSurfaceType`, `CgPublishingState`, `CgPageRole`, `CgLinkRole`), and their associated event types (`CG_SURFACE_CREATED`, `CG_PAGE_CREATED`, etc.) must not appear in VEDA schema, VEDA migrations, VEDA event log vocabularies, or VEDA entity type vocabularies.

### Eliminated (ADR-003 — VEDA Brain)

Any record family associated with VEDA Brain intelligence synthesis does not exist:

- intelligence synthesis tables
- planning proposal tables
- content gap analysis tables
- cross-system scoring or ranking tables owned by VEDA Brain

These are not being moved. They simply do not exist in this build.

### Previously eliminated editorial/production models

The following models were removed in Wave 2D of the legacy build and remain out of scope:

- `Entity` (old PsyMetric entity model — not the content graph entity)
- `EntityRelation`
- `Video` (owned production model)
- `DistributionEvent`
- `DraftArtifact`
- `MetricSnapshot`
- `QuotableBlock`

---

## Structural Rules

### 1. Project-scoped isolation is the default

Every VEDA table is project-scoped unless it is an explicitly documented exception. The only first-pass exception is `SystemConfig`. Adding a new global table requires governance review and explicit justification.

### 2. Observation records are append-friendly

Observation records (`SERPSnapshot`, `SearchPerformance`) must not silently overwrite historical state. A new observation produces a new row. Prior observations are history. The append-friendly posture is what makes VEDA trustworthy as an observatory over time.

### 3. Governance records are mutable within bounds

Governance records (`Project`, `KeywordTarget`, `SourceFeed`) may be updated within governed bounds. Changes to governance records should emit `EventLog` entries where the change is state-significant.

### 4. Event log is append-only

`EventLog` must not be updated or deleted. It is a permanent append-only audit trail for observatory-significant state changes.

### 5. Raw payloads are allowed where evidence preservation requires it

JSON payloads are acceptable for preserving full provider evidence archives. Hot-path fields must still be promoted to explicit columns. JSON must not be used to hide foreign canonical truth or to avoid schema design.

### 6. Content graph structures must not be recreated in VEDA

This cannot be overstated: the `Cg*` family moved to V Forge per ADR-002. Any attempt to recreate content graph structures in VEDA — even under observatory language — is a boundary violation. VEDA may reference content URLs as strings. It does not own page or topic records.

### 7. Intelligence synthesis layers must not be introduced as schema families

Any proposed VEDA table that stores synthesized proposals, planning-adjacent outputs, or cross-system intelligence products is a VEDA Brain recreant. It does not belong in VEDA schema. If the data serves planning, it belongs in Project V. If it serves execution intelligence, it belongs in V Forge.

---

## Anti-Drift Rules

### Rule 1 — Test every proposed table against the observatory pattern

Before adding a new table to VEDA schema, ask: can this be explained as `entity + observation + time + interpretation`? If it cannot, it is presumptively out of scope.

### Rule 2 — Content graph structures may not re-enter VEDA

No matter how useful it might seem to have pages, topics, entities, or internal links in VEDA for cross-referencing signal with content structure, that path is closed. V Forge owns the content graph. The governed interface for crossing VEDA signal against V Forge content structure is `../interfaces/veda-to-v-forge-signal-interface.md`. Use that interface instead of recreating the content graph in VEDA.

### Rule 3 — VEDA Brain must not be recreated

Any table that materializes planning proposals, content gap recommendations, or cross-system intelligence products is VEDA Brain behavior. If it is needed, it belongs in Project V or V Forge. Never in VEDA.

### Rule 4 — Vocabulary additions require governance review

Adding a new `EventType`, `EntityType`, `Platform`, or other controlled vocabulary value requires updating this document. Local implementation choices that silently expand governed vocabularies are anti-drift violations.

### Rule 5 — JSON blobs must not substitute for schema design

If a field is accessed repeatedly in queries, filtering, or system logic, it must be an explicit column. JSON is evidence support. It is not a junk drawer for unresolved design decisions or cross-boundary truth hiding.

### Rule 6 — Cross-system references stay as locators, not FKs

VEDA may store URLs, external IDs, and cross-system locators. It must not carry FK relationships into Project V or V Forge tables. A FK to another system's table creates structural coupling that violates VEDA's observatory boundaries.

### Rule 7 — SearchPerformance must not acquire planning-facing FKs

`SearchPerformance` uses `pageUrl` as a raw string, not a FK to any page record. Proposals to attach `SearchPerformance` rows to content graph entities (topics, pages, entities) would recreate part of the VEDA Brain cross-referencing pattern and are forbidden.

---

## Final Rule

VEDA schema is observatory schema.

Every table it contains must describe observed external reality, scope observatory data, or log observatory-significant state changes.

If a table answers the question "what was built?" or "what should be built next?", it does not belong in VEDA.
If a table re-encodes V Forge content graph structures, it does not belong in VEDA.
If a table materializes intelligence synthesis that spans planning and observatory concerns, it does not belong in VEDA.

The schema is an implementation of the observatory doctrine. It is not a sandbox for convenient cross-system aggregation.

---

## Usage

This document should be used:

- as the primary schema reference when implementing VEDA database tables and migrations
- when classifying whether a proposed new table or field belongs in VEDA
- when reviewing whether a VEDA migration is consistent with observatory-only posture
- when orienting an LLM for VEDA schema work
- when checking whether content graph structures have re-entered VEDA
- when deciding whether a derived output requires a new table or compute-on-read

---

## Related Docs

- `veda.md`
- `system-invariants.md`
- `data-boundaries.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `mcp-surface.md`
- `operator-surfaces.md`
- `providers/registry.md`
- `../ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-003-veda-brain-eliminated.md`
- `../ecosystem/decisions/ADR-007-docs-are-build-spec-db-owns-operational-state.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../v-forge/schema-reference.md` *(content graph schema lives here)*
- `../project-v/schema-specification.md`
