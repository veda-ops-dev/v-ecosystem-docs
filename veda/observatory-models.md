# VEDA Observatory Models

## Purpose

This document defines the conceptual model layer for VEDA's observatory domain.

It exists to answer:

```text
How are VEDA's canonical record families conceptually organized, how do they relate
to each other, what modeling boundaries must be preserved, and how does raw source
truth become VEDA observability truth without VEDA drifting into planning, execution,
or content-graph ownership?
```

Read this with:

- `schema-reference.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `system-invariants.md`
- `data-boundaries.md`
- `../ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-003-veda-brain-eliminated.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- what the observatory model layer is and how it relates to schema
- what model categories VEDA owns and what each represents
- how models within those categories relate to each other
- how raw source truth becomes VEDA observability truth
- how provenance attaches to observatory models
- what relationship types between VEDA models are allowed vs forbidden
- what downstream consumers may derive from VEDA models
- what VEDA must not model at the conceptual layer
- anti-drift rules that prevent content-graph, planning, or execution semantics from re-entering through modeling choices

---

## Out of Scope

This document does not define:

- the exact schema fields and column types for each family — that belongs in `schema-reference.md`
- database migration scripts or migration sequencing
- the full API or MCP surface contract for VEDA routes
- V Forge content graph model design
- Project V planning model design
- provider-specific ingest implementation details
- signal package payload formats for cross-system interfaces — those belong in the interface docs

---

## System

- veda

---

## Core Rule

VEDA models observatory truth. Every conceptual model VEDA owns must describe one of three things:

1. **Observed external reality** — what VEDA has recorded about the external world at a given time
2. **Observatory governance** — how VEDA scopes, configures, or logs its observatory operations
3. **Bounded derived interpretation** — conclusions drawn from observed external reality that remain explicitly subordinate to the observations that produced them

A model that describes internal project structure, planning decisions, execution state, or cross-system intelligence products does not belong in VEDA's observatory layer.

---

## Observatory Model Role

The observatory model layer is the conceptual organization above raw schema and below the API surface.

It answers:
- what kind of thing is this record?
- what other records may legitimately relate to it?
- how does provenance flow from source to observation to signal?
- when does an observation become stale, superseded, or untrustworthy?
- what is the consumer boundary between VEDA producing signal and another system acting on it?

The model layer must remain faithful to the observatory pattern that governs all VEDA design:

```text
entity + observation + time + interpretation
```

A model that cannot be explained using this pattern is presumptively misclassified or belongs in another system.

### Relationship to `schema-reference.md`

`schema-reference.md` defines the implementation-facing shape: which tables exist, what fields they carry, what constraints apply.

This document defines the conceptual organization: what categories those tables belong to, how they relate, what they model, and what modeling boundaries must be preserved as the system grows.

The two documents are complementary. A question about field types belongs in `schema-reference.md`. A question about whether a proposed relationship between models is conceptually valid belongs here.

---

## Canonical Model Categories

VEDA's canonical record families fall into five model categories. Each category has a distinct purpose and a distinct posture toward mutation, provenance, and cross-system reference.

---

### Category 1 — Project Partition Model

**Primary record:** `Project`

**What it models:** The observatory scoping container. Every VEDA observatory record belongs to exactly one project. The project partition model exists to enforce multi-project isolation — it does not model planning truth.

**Posture:**
- mutable within governed bounds (`lifecycleState`, descriptive fields)
- state changes must be logged to the observatory event ledger
- a thin governance record, not a rich orchestration object

**What it does not model:**
- project planning state, roadmap, or orchestration truth — those belong to Project V
- project readiness, approval posture, or decision continuity
- any cross-system planning semantics

**Relationship rule:** All other VEDA records in project scope carry a FK to this record. No other VEDA model may carry a FK to a Project V planning project record. The VEDA `Project` and the Project V planning `Project` are distinct records with distinct purposes; they may share a slug as a coordination convention but are not synchronized models.

---

### Category 2 — Source and Feed Models

**Primary records:** `SourceFeed`, `SourceItem`

**What they model:**
- `SourceFeed`: a recurring external source that VEDA monitors or ingests from — a durable ingest path, not an observation
- `SourceItem`: an individual captured external item — a webpage, comment, video reference, or other source artifact entered through the observatory intake

**Posture:**
- `SourceFeed` is a governance record: mutable, operator-controlled, represents a configured observation channel
- `SourceItem` is a capture record: partially mutable (status transitions), but identity and provenance fields are immutable after creation
- `SourceItem` is the primary observatory intake record; it is not a planning backlog item, publishing workflow queue entry, or execution task

**Provenance posture:**
- `SourceItem.capturedBy` and `operatorIntent` are required provenance fields — they identify who introduced the item and why
- these fields must not be suppressed, defaulted silently, or treated as optional
- `SourceItem` status transitions (`ingested → triaged → used → archived`) reflect observatory processing, not planning lifecycle or editorial workflow

**What they do not model:**
- content graph entities (pages, topics, entities) — those belong to V Forge
- planning records or readiness signals
- execution pipeline stages or content production queues

**Relationship rule:** A `SourceItem` may reference a `SourceFeed` as its ingest origin. A `SourceItem` may carry external URLs, provider-origin identifiers, and snapshot references as text or locator fields. A `SourceItem` must not carry a FK to any V Forge page or topic record, and must not implicitly model a content graph node through field design.

---

### Category 3 — Event Log Model

**Primary record:** `EventLog`

**What it models:** The canonical append-only observatory event audit trail. Records meaningful state transitions and observatory-significant events inside the VEDA boundary. Exists to make observatory history auditable, not to model operational workflow.

**Posture:**
- strictly append-only: no updates, no deletes
- project-scoped: each event belongs to a project
- actor-attributed: every event carries actor type (`human`, `llm`, `system`)
- polymorphic: `entityType + entityId` identifies which observatory model the event concerns
- event types are governed vocabulary — see `schema-reference.md` Controlled Vocabularies section

**What it does not model:**
- analytics events, telemetry, or request logs — this is a state-change audit trail, not a usage tracker
- planning workflow transitions — those belong in Project V
- execution workflow transitions — those belong in V Forge
- read-only operation records — reads must not emit `EventLog` entries

**Atomicity rule:** Where a VEDA state change requires an `EventLog` entry (e.g., `Project.lifecycleState` change, `SourceItem` status transition), the state change and the log entry must commit in the same transaction. An event log entry that is possible to lose on transaction rollback is not a trustworthy audit trail.

**Relationship rule:** `EventLog` rows reference other VEDA models via `entityType + entityId`. This reference is read-only and audit-facing — it identifies what changed, but the `EventLog` row does not create a live FK dependency on the referenced record. `EventLog` entries must never reference Project V or V Forge record identifiers as the primary subject of the event.

---

### Category 4 — Search Observatory Models

**Primary records:** `KeywordTarget`, `SERPSnapshot`, `SearchPerformance`

**What they model:**
- `KeywordTarget`: the observatory governance record for what VEDA is configured to watch — a target definition, not an observation
- `SERPSnapshot`: an immutable observation of what SERP showed for a given query scope at a given moment — the primary historical observation ledger for search
- `SearchPerformance`: a performance observation record for a query × page × date-range combination, primarily from Google Search Console — URL-based observation without content graph coupling

**Posture:**
- `KeywordTarget` is a governance record: mutable within bounds, controls what VEDA observes
- `SERPSnapshot` is an observation record: append-friendly, prior rows must not be silently overwritten, each snapshot is historical truth at its capture time
- `SearchPerformance` is an observation record: append-friendly for new windows, URL-scoped without entity FK coupling

**The observation model pattern for this category:**

```text
KeywordTarget (what to watch)
  → SERPSnapshot (what was observed at a specific moment)
     → provider raw payload archived in rawPayload
     → promoted hot fields for efficient querying
```

`KeywordTarget` does not directly own `SERPSnapshot` rows through a FK. The relationship is conceptual: snapshots are taken for query/locale/device combinations that may correspond to configured targets. The snapshot does not require a live FK to the target to be a valid observation record.

This design is intentional and must not be changed by adding a `keywordTargetId` FK to `SERPSnapshot`. The reason: a historical `SERPSnapshot` is observatory truth that must remain valid regardless of whether the corresponding `KeywordTarget` governance record still exists. If an operator deletes or modifies a `KeywordTarget` — because they stop watching a query, change its scope, or consolidate targets — that governance change must not affect the integrity of historical snapshots captured for that query. A FK from `SERPSnapshot` to `KeywordTarget` would create exactly that coupling: historical observation records would become dependent on a governance record they were not logically part of. The correlation between targets and snapshots is analytical, not structural. Queries that need to correlate them join on shared fields (`query`, `locale`, `device`). That approach is architecturally preferable even when it makes queries slightly more verbose.

**What they do not model:**
- content graph entities — `SearchPerformance.pageUrl` is a raw URL string, not a FK to any page record
- editorial intent, publishing plans, or content lifecycle
- planning decisions about what to build or optimize
- VEDA Brain-style analysis products

**YouTube SERP observation placement:** YouTube query-level SERP observations use `SERPSnapshot` per VEDA-001's vendor-primary posture. A separate `YouTubeSnapshot` family does not exist at first pass and must not be created without explicit governed architecture work.

**Relationship rule:** `SearchPerformance` and `SERPSnapshot` may be correlated in analysis, but must not be joined through a FK. The correlation is analytical, not structural. Adding a FK between them would create structural coupling that implies one owns or explains the other — that is derived interpretation, not observatory structure.

---

### Category 5 — System Configuration Model

**Primary record:** `SystemConfig`

**What it models:** Global observability configuration that applies across all projects or requires a global scope. The intentional exception to the project-scoped default.

**Posture:**
- intentionally not project-scoped
- small by design — every entry must be justified as genuinely requiring global scope
- updates are actor-attributed (`updatedBy`)
- per-project override pattern uses embedded JSON structure rather than a proliferation of per-project config rows

**What it does not model:**
- arbitrary application state
- planning configuration or orchestration preferences
- execution configuration or deployment preferences
- a junk drawer for unclassified system state

**Relationship rule:** `SystemConfig` has no FK relationships to other VEDA models or to records in other systems. It is a bounded key-value governance store, not a relational anchor.

---

## Model Relationship Rules

### Allowed relationships

The following relationship types are allowed between VEDA models:

1. **Project scoping:** Any project-scoped VEDA record carries a `projectId` FK to `Project`. This is the universal project-scope anchor.

2. **Feed-to-item origin:** A `SourceItem` may carry an optional FK to the `SourceFeed` it originated from. This is an ingest-origin reference.

3. **Event log reference:** An `EventLog` row carries `entityType + entityId` identifying which observatory model the event concerns. This is an audit reference, not a live FK constraint.

4. **Analytical correlation:** VEDA models in the same project may be correlated analytically in query results or derived views without requiring structural FKs between them. Example: correlating `SERPSnapshot` and `SearchPerformance` for the same query in a diagnostic output.

### Forbidden relationships

The following relationship types are forbidden:

1. **FK to Project V records:** No VEDA model may carry a FK to any Project V planning record — objectives, initiatives, work items, handoffs, decision records, or any other planning table.

2. **FK to V Forge records:** No VEDA model may carry a FK to any V Forge execution record — pages, topics, entities, internal links, or any other content graph table. Cross-system reference uses URLs or locator strings, not FK relationships.

3. **SearchPerformance-to-content-graph coupling:** `SearchPerformance` must not carry a FK to any content graph record. It must not be joined to content graph entities through a junction table. The prohibition applies to direct FK relationships, derived tables, and any equivalent semantic coupling. See Anti-Drift Rule 5.

4. **Cross-project FK relationships:** A VEDA record in project A must not carry a FK to a VEDA record in project B. Project isolation is a structural constraint, not a query filter.

5. **Intelligence synthesis tables:** No VEDA model may carry relationships that implement planning proposal generation, content gap scoring, or cross-system recommendation production. These are VEDA Brain patterns. They do not belong in VEDA's model layer.

---

## Provenance and Source Rules

Provenance is not optional annotation in VEDA. It is part of what makes observatory output trustworthy.

### Required provenance posture per model category

**Project partition model:**
- `lifecycleState` changes must be logged; actor context must be preserved in the event log entry

**Source and feed models:**
- `SourceItem.capturedBy` — who or what introduced the item — is a required non-nullable field
- `SourceItem.operatorIntent` — why the item was captured — is a required non-nullable non-empty field
- `SourceItem.capturedAt` — when the item was captured — is required and must reflect capture time, not ingest processing time when those differ
- source status transitions that are state-significant must be logged to `EventLog`
- specifically, a `SourceItem` transition to `archived` **must** emit an `EventLog` entry: `archived` is a terminal disposal state with an associated `archivedAt` timestamp, making it unambiguously state-significant; an implementer must not treat this transition as a silent field update
- other `SourceItem` status transitions (e.g., `ingested → triaged`, `triaged → used`) are also candidates for event logging when the observatory operation requires an auditable record; the default posture is to log state-significant transitions rather than skip them — the governing question is whether the transition represents a meaningful change in observatory state

**Event log model:**
- `EventLog.actor` — who caused the event — is required
- `EventLog.timestamp` — when the event occurred — is required
- event details must be preserved as structured JSON where the detail is needed for later reconstruction; the event type alone is not sufficient when the specific change requires context

**Search observatory models:**
- `SERPSnapshot.source` — which provider or ingest path produced this snapshot — is required
- `SERPSnapshot.capturedAt` — when the observation was recorded — is required
- `SERPSnapshot.rawPayload` — the full provider evidence archive — must be preserved; promoted fields are convenience extractions on top of this, not replacements for it
- uncertainty and confidence limits must be preserved where the provider supplies them or where the ingest path introduces them

### Derivation boundary rule

When VEDA produces derived outputs — diagnostics, summaries, signal packages, search intelligence views — those outputs must remain clearly subordinate to the canonical observation records they depend on.

Derivation rules:
- the derivation source (which observation records were used) must be traceable
- derived output must not be promoted to canonical status unless a governed architecture decision explicitly establishes a canonical derived family
- derived output that is compute-on-read should remain compute-on-read unless there is a documented operational justification to materialize it
- materialized derived output must be labeled as derived and must not be queried as though it were direct observation truth

### Raw vs structured vs derived distinction

VEDA models must preserve this three-layer distinction:

| Layer | Example | Posture |
|---|---|---|
| Raw evidence | `SERPSnapshot.rawPayload` | Full provider payload archived for evidence traceability |
| Structured observation | `SERPSnapshot.aiOverviewStatus`, `SERPSnapshot.query` | Promoted fields extracted for efficient querying |
| Derived interpretation | Search diagnostics, signal packages | Compute-on-read by default; materialization requires justification |

These layers must not be collapsed. An implementer reading a derived view must be able to tell it is derived, not direct observation truth.

---

## Consumer and Downstream Interpretation Boundary

VEDA models produce observatory truth. Downstream systems and consumers interpret that truth. These two roles must remain distinct.

### What VEDA produces

- canonical observation records
- bounded provenance context
- bounded derived signal and diagnostics from those records
- signal packages through governed interfaces

### What downstream consumers do with VEDA output

- **Project V** interprets VEDA signal for planning decisions
- **V Forge** crosses VEDA performance signal against its owned content graph for execution intelligence
- **Human operators** review VEDA diagnostics and surface conditions to inform governed decisions

### What does not happen at the consumer boundary

- Consuming VEDA signal does not transfer VEDA's observability ownership to the consumer
- Consuming VEDA signal does not give Project V or V Forge permission to write back into VEDA observatory records
- Project V interpreting VEDA signal as a planning decision does not make that planning decision a VEDA record
- V Forge crossing VEDA signal against its content graph does not make the content graph a VEDA-owned model

### No circular model coupling

VEDA models must not carry references to planning decisions, planning conclusions, or execution intelligence products derived from VEDA signal. The signal flow is unidirectional: VEDA produces signal, consumers interpret it, consumers own the resulting conclusions.

An `EvidenceLink` in Project V that references a VEDA observation locator is a Project V record, not a VEDA record. It lives in Project V's data model. VEDA does not own the link. VEDA does not need to carry a FK back to the Project V record that cited its observation.

---

## Deferred Domains

The following observatory domains are owned by VEDA but do not yet have a governed canonical record family in the first-pass model layer. They are owned-but-deferred.

### GA4 observations

VEDA owns Google Analytics 4 performance observations. No `GA4Observation` or equivalent model category exists in the first-pass model layer. Implementation must not create ad hoc tables or local model families for GA4 data. The model family must be governed through a documented architecture decision and added to `schema-reference.md` before implementation.

### YouTube enrichment data

VEDA owns YouTube search and channel observatory data. YouTube query-level SERP observations land in `SERPSnapshot` per VEDA-001. YouTube enrichment data from the YouTube Data API — video metadata, channel metadata, statistics snapshots — does not yet have a governed model family. A separate `YouTubeSnapshot` or YouTube enrichment model family must not be created without governed architecture work. The family must be defined, documented in `schema-reference.md`, and governed before implementation.

### Rule: Deferred domains must not receive ad hoc models

Deferred domains must not receive local model families, provisional schema, or JSON convenience blobs that substitute for governed model design. Adding a model family for a deferred domain without first governing it is a boundary violation regardless of how useful the shortcut seems operationally.

---

## Anti-Drift Rules

### Rule 1 — Apply the observatory test before adding any model

Before proposing a new VEDA model or model relationship, ask: can this be explained using `entity + observation + time + interpretation`? If it cannot, it is presumptively out of scope. If it sounds like it describes internal project structure rather than observed external reality, it belongs in V Forge or Project V.

### Rule 2 — Content graph semantics may not re-enter VEDA under model names

Models named `PageNode`, `TopicCluster`, `ContentEntity`, `ObservedPage`, `SemanticTopic`, or anything that models internal content structure are content graph concepts. They do not become observatory models by adding "observatory" to the name. ADR-002 transferred the content graph to V Forge. No amount of modeling vocabulary makes it an observatory concern.

### Rule 3 — VEDA Brain patterns may not re-enter VEDA as derived model categories

A model that materializes planning proposals, content gap recommendations, cross-system intelligence products, or opportunity scoring is a VEDA Brain pattern. ADR-003 eliminated VEDA Brain. A "search intelligence model" or "derived opportunity record" that encodes these patterns is VEDA Brain under a different name. If the model is needed, it belongs in Project V or V Forge.

### Rule 4 — External URLs and identifiers must not be silently upgraded into owned entities

A VEDA observation may record an external URL, a provider identifier, or a cross-system locator as a text field. Storing that URL or identifier does not create ownership of the external entity it refers to. An observed page URL stored in `SearchPerformance.pageUrl` does not make the page a VEDA-owned model. An external video identifier stored in a source item does not make the video a VEDA-owned entity. Storing a locator is not the same as modeling the referenced entity.

### Rule 5 — SearchPerformance must not acquire content-graph coupling

`SearchPerformance` is a URL-based observation record. It must not acquire a FK to any content graph entity, a junction table linking it to topics or pages, or any equivalent semantic coupling that would create a structural dependency on V Forge content graph models. Analytical correlation is allowed. Structural coupling is not. See `schema-reference.md` Anti-Drift Rule 7.

### Rule 6 — Derivation must not become canonical status without governance

A derived view, materialized summary, or computed diagnostic that becomes the practical source of truth for a domain is a second canonical truth store. Derived output may grow on top of observation records. It must not replace them or acquire canonical authority without explicit governance work that promotes it to canonical status through a documented architecture decision.

### Rule 7 — Signal interfaces are unidirectional

VEDA signal flows outward to Project V and V Forge through governed interfaces. Those systems interpret the signal. The interpretation does not flow back into VEDA models. A planning decision derived from VEDA signal is a Project V record. A content gap identified by crossing VEDA signal against V Forge's content graph is a V Forge record. VEDA does not carry FKs to those downstream conclusions, and VEDA models must not be extended to absorb them.

### Rule 8 — New model families require governed architecture decisions

Adding a new model family to VEDA requires updating `schema-reference.md` and, if the family introduces new model categories or changes model relationship patterns, updating this document. A new table created locally in an implementation without corresponding shared-root authority documentation is ungoverned schema, not an observatory model.

---

## Non-Goals

This document does not:

- define the content graph model layer — that belongs in V Forge model authority docs
- define the planning model layer — that belongs in Project V authority docs
- govern cross-system signal package payload formats — those belong in the interface docs
- constitute a full API contract or migration spec
- govern VEDA Brain capabilities — VEDA Brain does not exist
- invent new observatory families for deferred domains

---

## Final Rule

VEDA models external observable reality. A model that describes what was built, what should be built, or how well something executed is not an observatory model — it belongs in another system.

The model layer is the place where observatory discipline is either maintained or gradually dissolved. Each modeling choice that accepts a content-graph concept, a planning concept, or an intelligence-synthesis concept as an observatory concern makes the next such choice easier to rationalize. The anti-drift rules exist to prevent that rationalization.

---

## Usage

This document should be used:

- when designing a new VEDA model or model relationship
- when classifying whether a proposed model fits an existing category or requires governance
- when reviewing whether a proposed relationship between VEDA models is structurally allowed
- when deciding whether an analytical derivation should be materialized or remain compute-on-read
- when orienting an LLM or implementer on VEDA's conceptual model structure
- when checking whether content graph, planning, or execution semantics are re-entering VEDA through model design

---

## Related Docs

- `schema-reference.md`
- `veda.md`
- `system-invariants.md`
- `data-boundaries.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `mcp-surface.md`
- `operator-surfaces.md`
- `decisions/VEDA-001-youtube-observatory-truth-surface.md`
- `../ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-003-veda-brain-eliminated.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../v-forge/observatory-models.md` *(content graph models live here)*
