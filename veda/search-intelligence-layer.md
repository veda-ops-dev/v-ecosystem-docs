# VEDA Search Intelligence Layer

## Purpose

This document defines the governed search intelligence layer for VEDA.

It exists to answer:

```text
How do keyword targets, SERP snapshots, and search-performance observations work together,
what transformations and correlations are legitimate, what outputs count as observatory signal
versus downstream consumer interpretation, and how does this layer remain observability truth
without becoming a planning engine, execution engine, or content graph?
```

Read this with:

- `schema-reference.md`
- `observatory-models.md`
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

- what the search intelligence layer is and what role it plays inside VEDA
- which canonical model families participate in the search intelligence layer
- how search observations are captured, normalized, and correlated
- what derivation and correlation rules apply
- how provider and source provenance remains explicit through the layer
- what the layer may expose as signal output
- what the layer must not produce, model, or own
- how downstream consumers interact with search intelligence output without transferring ownership
- anti-drift rules that keep the layer observatory-bounded

---

## Out of Scope

This document does not define:

- the exact schema fields and column types for each participating family — that belongs in `schema-reference.md`
- the conceptual model categories for observatory families — that belongs in `observatory-models.md`
- the full API or MCP surface contract for search intelligence routes
- provider-specific ingest pipeline implementation details
- signal package payload formats for cross-system interfaces — those belong in the interface docs
- V Forge execution intelligence that crosses VEDA search signal against the content graph — that belongs in V Forge authority docs and the `veda-to-v-forge-signal-interface.md`
- ranking algorithms or recommendation systems — VEDA does not own those

---

## System

- veda

---

## Core Rule

The search intelligence layer is an observatory layer.

Its purpose is to derive bounded, deterministic, reviewable interpretation from search observation records. It does not produce planning decisions, content recommendations, or execution instructions. It does not own content-graph entities. It does not absorb downstream interpretation back into its own model.

Search intelligence inside VEDA answers questions of the form:
- what does external search reality show for a given query scope?
- how has that shown reality changed over time?
- what does performance signal say about how external platforms respond?
- what observatory conditions appear noteworthy enough to surface?

Search intelligence inside VEDA does not answer questions of the form:
- what content should the project build or optimize?
- what are the content gaps in this project's coverage?
- what page should rank for this query?
- how should the execution plan change based on SERP conditions?

Those questions belong to Project V's planning intelligence or V Forge's execution intelligence. VEDA provides the search evidence those systems use to reason. It does not do the reasoning on their behalf.

---

## Search Intelligence Layer Role

The search intelligence layer sits above the raw observation records and below the cross-system signal interface.

```text
External search reality (SERP, GSC, provider payloads)
  ↓
Observation records (SERPSnapshot, SearchPerformance, KeywordTarget)
  ↓
Search intelligence layer (compute-on-read correlation, change detection, diagnostics)
  ↓
Signal output (observable patterns, change signals, performance conditions)
  ↓
Cross-system interfaces (Project V, V Forge) — interpretation happens in the consuming system
```

The layer's job is to make the raw observation records more usable without replacing them as the source of truth. It produces derived outputs. It does not produce canonical observatory records that would then themselves be the observatory source.

### Relationship to `schema-reference.md`

`schema-reference.md` governs what canonical families exist, their field shapes, and their constraints. The search intelligence layer operates on the records defined there. This doc governs how those records are used together and what may be derived from them — not their field-level shape.

### Relationship to `observatory-models.md`

`observatory-models.md` governs the conceptual model organization and relationship rules. The search intelligence layer must respect those relationship rules: `SearchPerformance` and `SERPSnapshot` remain analytically correlatable but must not be structurally coupled. `KeywordTarget` is a governance/configuration aid, not an owned semantic search entity. This doc does not relax any of those rules; it governs how the layer operates within them.

### Relationship to `observability-and-signal-role.md`

`observability-and-signal-role.md` establishes that VEDA's valid operating pattern is `entity + observation + time + interpretation`. The search intelligence layer is the interpretation portion of that pattern applied to search-domain observations. "Interpretation" in that context means bounded observatory interpretation — change detection, condition classification, diagnostic outputs — not planning recommendations or execution decisions.

---

## Participating Model Families

Three canonical model families participate in the search intelligence layer as first-class inputs:

### `KeywordTarget` — observatory governance input

`KeywordTarget` defines what VEDA is watching: which query, locale, and device combinations are configured for observation. It is the governance input that shapes what search intelligence the layer can produce.

**Role in the layer:** determines observation scope; makes explicit which query spaces have active observation history.

**What it is not:** `KeywordTarget` is not a semantic search entity. It is not an owned representation of a topic, intent cluster, or keyword category. Creating a `KeywordTarget` does not give VEDA semantic ownership over the query it describes. The target exists to configure observation; what VEDA observes about that query is in `SERPSnapshot`.

**Relationship posture:** `KeywordTarget` does not directly own `SERPSnapshot` rows through a FK. Snapshots are correlated to targets analytically through shared `(query, locale, device)` fields. A historical snapshot remains valid observatory truth even if the corresponding target is deleted or modified. See `observatory-models.md` Category 4 for the full reasoning.

### `SERPSnapshot` — primary search observation ledger

`SERPSnapshot` records what SERP showed for a given query scope at a given capture moment. It is the primary historical observation record for the search intelligence layer.

**Role in the layer:** provides the raw observed evidence for change detection, SERP composition analysis, AI overview tracking, and competitive landscape observation.

**What it is not:** `SERPSnapshot` is not a planning record about what content should rank. It is not a target representing desired search outcomes. It records what was observed; it does not express what should happen.

**Immutability posture:** `SERPSnapshot` records are append-friendly. A new observation adds a new row. Prior snapshots must not be modified. Historical SERP truth must remain intact. The search intelligence layer reads from snapshots; it does not update them.

**Raw payload posture:** `rawPayload` preserves the full provider response as an evidence archive. Fields promoted to explicit columns (`aiOverviewStatus`, `aiOverviewText`) exist for efficient querying. The search intelligence layer may access either, but derived outputs must trace back to the canonical snapshot record, not to a processed version that has replaced it.

### `SearchPerformance` — performance observation input

`SearchPerformance` records query × page × date-range performance observations, primarily from Google Search Console. It provides click, impression, CTR, and position data over defined observation windows.

**Role in the layer:** provides performance-side evidence for the same search domains covered by SERP observations — how external platforms respond to a project relative to what SERP shows for relevant queries.

**What it is not:** `SearchPerformance` is not a content-performance tracker or a content graph record. `pageUrl` is a raw URL string — an observed URL at which performance was measured. It does not model a V Forge page entity, and must not be coupled to one through a FK, junction table, or equivalent semantic binding. This prohibition applies even when the URL happens to correspond to a page in V Forge's content graph. The correlation between a performance observation and an owned content page is an analytical act performed in the consuming system, not a structural relationship owned by VEDA.

### `SourceItem` and `SourceFeed` — supporting evidence inputs

`SourceItem` and `SourceFeed` records may supply supporting evidence and context for search intelligence analysis where source capture has produced material relevant to a search domain. They are not primary inputs to the search intelligence layer in the same way as the three families above, but they may inform provenance context and source-trust posture for intelligence outputs.

---

## Observation Capture and Normalization Posture

### Capture posture

Search observations enter VEDA through governed ingest paths from registered providers. Only providers listed in `providers/registry.md` are active integrations.

**SERP capture:** `SERPSnapshot` records are created by ingest from a vendor SERP source (per VEDA-001). Each capture creates a new immutable snapshot row. The capture path must preserve the full raw provider payload alongside promoted fields. Captures must carry explicit `capturedAt`, `source`, and `payloadSchemaVersion` markers.

**Performance capture:** `SearchPerformance` records are created by ingest from Google Search Console or an equivalent governed provider. Each observation window produces a record or updates an existing record for the same `(projectId, query, pageUrl, dateStart, dateEnd)` combination. Performance data for a completed window should not be silently modified after ingest; re-ingesting a window must produce an explicit update or replacement, not a silent overwrite of a different record.

**Target management:** `KeywordTarget` records are created or modified through governed operator action. They are not inferred or auto-generated from observed SERP data. A query appearing in a SERP result does not automatically create a `KeywordTarget`; the target represents a deliberate governance decision to observe that query scope.

### Normalization rules

Normalization within the search intelligence layer means promoting raw provider data into consistent structured fields for analysis. It does not mean creating new canonical truth records that replace the source observations.

Allowed normalization:
- extracting and promoting frequently-queried fields from `rawPayload` into explicit columns on `SERPSnapshot`
- normalizing `pageUrl` format (trailing slash, protocol) for consistent querying within `SearchPerformance`
- normalizing locale and device strings for consistent target/snapshot correlation

Forbidden normalization:
- creating a separate "normalized snapshot" record family that replaces the raw snapshot as the query target
- mapping raw query strings to owned semantic categories or topic entities without a governed canonical family
- deriving a URL-to-entity mapping from `SearchPerformance.pageUrl` that creates a hidden content-graph dependency
- discarding or compressing historical snapshot records after normalization

---

## Correlation and Derivation Rules

### Legitimate correlation types

The following correlation patterns are legitimate within the search intelligence layer:

**1. Temporal correlation across SERPSnapshots**
Comparing `SERPSnapshot` records for the same `(projectId, query, locale, device)` tuple across different `capturedAt` timestamps to detect SERP changes, volatility, rank movement, AI overview presence changes, or competitive shifts.

This is the primary search intelligence pattern. It operates entirely within `SERPSnapshot` records and requires no FK to external systems.

**2. Performance correlation across SearchPerformance windows**
Comparing `SearchPerformance` records for the same `(projectId, query, pageUrl)` combination across different observation windows to detect trend, decay, or improvement in impressions, clicks, CTR, or position.

**3. Query-space analytical correlation between SERPSnapshot and SearchPerformance**
For a given `(projectId, query)` space, analytically correlating observed SERP conditions from `SERPSnapshot` with performance signals from `SearchPerformance` to produce a combined observatory picture of how external search behaves for that query.

This correlation is analytical and must not create a structural FK or junction table between the two families. The join is expressed at query time on shared fields. See `observatory-models.md` Model Relationship Rules and the Category 4 explanation.

**4. Target coverage assessment**
For a given `projectId`, assessing which `KeywordTarget` records have corresponding `SERPSnapshot` history and which do not. This identifies observation gaps in the configured watch list. The assessment is analytical, not structural.

**5. Source-to-signal continuity tracking**
Where a `SourceItem` capture contributes evidence relevant to a search domain, maintaining traceable continuity between the source record and any derived search intelligence output that depends on it.

### Forbidden coupling patterns

The following coupling patterns are forbidden regardless of how useful they appear:

**1. FK from `SERPSnapshot` or `SearchPerformance` to `KeywordTarget`**
A historical observation must remain valid even if the governance record that motivated its capture is deleted or changed. Structural coupling to `KeywordTarget` violates historical observation integrity. See `observatory-models.md` Category 4.

**2. FK from `SearchPerformance` to any content graph entity**
`pageUrl` is a raw URL string. Attaching it to a V Forge page, topic, or entity via FK, junction table, or derived mapping table creates content-graph coupling inside VEDA. This is forbidden at every level — direct FK, junction table, or structural semantic equivalent. See `observatory-models.md` Anti-Drift Rule 5.

**3. Materializing query-to-topic or query-to-entity mappings as canonical VEDA records**
Mapping query strings to owned semantic categories (topics, intent clusters, entity clusters) and storing those mappings as canonical VEDA records creates content-graph semantics inside VEDA. The queries VEDA observes are evidence. They are not semantic entities VEDA owns.

**4. Scoring tables that encode planning or execution recommendations**
Any derived table that stores opportunity scores, content gap scores, priority signals, or actionability rankings for planning or execution purposes is a VEDA Brain pattern. These must not exist in the search intelligence layer. VEDA surfaces observable conditions. It does not score them for planning or execution priority.

**5. Cross-project analytical aggregation stored as canonical records**
Aggregating search intelligence across project boundaries and storing the result as a VEDA-owned record weakens project isolation. Cross-project analysis may occur in consuming systems or in operator-facing views, but must not produce VEDA canonical records that span multiple project scopes.

### Derivation posture

Derived search intelligence outputs produced by this layer are compute-on-read by default.

Compute-on-read means: the output is calculated from canonical observation records at query time and is not stored as a separate canonical VEDA record unless there is an explicit operational justification documented in a governed architecture decision.

Materialization is justified only when:
- the compute-on-read cost is demonstrably unsustainable at the query volumes required
- the materialized output is labeled as derived and clearly does not replace the observation records that produced it
- the derivation source is traceable: which observation records were used, over what time window, with what logic

Materialization is not justified when:
- it makes queries simpler or dashboards cleaner without a documented performance need
- the materialized output is queried as though it were direct observation truth;
- removing the materialized data and computing on-read would produce the same result

---

## Provenance and Source Rules

Provider and source provenance is first-class in the search intelligence layer. Derived outputs must remain traceable to the observation records that produced them.

### Required provenance on observation records

- `SERPSnapshot.source` — the provider or ingest path that produced this snapshot — must be non-empty
- `SERPSnapshot.capturedAt` — when the observation was recorded — must be present and accurate
- `SERPSnapshot.rawPayload` — the full provider response — must be preserved alongside promoted fields
- `SERPSnapshot.payloadSchemaVersion` — the schema version of the raw payload — should be present to support future payload interpretation
- `SearchPerformance.capturedAt` — when the record was ingested — must be present

### Derivation provenance requirements

When the search intelligence layer produces derived output — diagnostics, change signals, SERP condition summaries, performance condition alerts — that output must preserve enough provenance context to answer:

- what observation records produced this output?
- what time range or snapshot window does this output cover?
- what provider or source supplied the underlying data?
- is this direct observation or derived interpretation?

Derived output that cannot answer these questions is provenance-deficient. Provenance-deficient derived output must not be packaged as VEDA signal for downstream consumers.

### Source trust posture

Not all provider-sourced search observations carry equal trust. Provider-specific trust posture — whether data is a primary snapshot instrument, an enrichment instrument, or a validation instrument — is governed by `providers/registry.md` and VEDA-001 for the YouTube domain.

The search intelligence layer must preserve source trust posture in any output it produces. A derived output sourced from a less-trusted or secondary instrument must not be packaged with the same confidence posture as one sourced from the primary snapshot instrument.

---

## Consumer and Downstream Boundary

### What the search intelligence layer produces for downstream consumers

The layer may produce:

- observable SERP conditions for a given query scope and time range
- change signals indicating that SERP composition, position, or AI overview status has changed meaningfully since a prior observation
- performance condition signals indicating how click, impression, CTR, or position metrics are trending for observed query scopes
- volatility and drift classification for query spaces based on historical snapshot comparison
- provenance-carrying evidence summaries that downstream systems can use to inform planning or execution decisions
- escalation-worthy signals — conditions that, based on evidence, appear to warrant governed review

### What the search intelligence layer does not produce

- planning decisions or planning recommendations — those belong to Project V
- content gap analysis or content optimization instructions — those belong to V Forge's execution intelligence layer
- ranked priority lists of what to build next — those are planning outputs
- execution assignments or task instructions — those belong to V Forge
- approval events, readiness assessments, or governance decisions — those belong to the consuming system and its governance chain

### Consumer interpretation boundary

When Project V or V Forge receives search intelligence output from VEDA through a governed interface:

- VEDA remains the owner of the observatory observations that produced the output
- the consuming system interprets the output for its own purposes
- the consuming system's interpretation does not become a VEDA record
- the consuming system's conclusions do not flow back into VEDA as new canonical records
- a Project V planning decision derived from VEDA search signal is a Project V record, not a VEDA record
- a V Forge content performance gap identified by crossing VEDA search signal against the V Forge content graph is a V Forge record, not a VEDA record

VEDA must not carry FK references to planning records or execution intelligence records that cite its observations. The signal flow is unidirectional outward through the governed interface. VEDA does not maintain awareness of how its outputs were used by downstream systems.

### Escalation-worthy signal posture

Where the search intelligence layer identifies conditions that appear to warrant governed review — significant SERP volatility, unexpected ranking changes, performance cliff events — it may surface those as escalation-worthy signals.

The escalation-worthy classification belongs to the observatory layer. The decision about how to respond — whether to replan, to reprioritize, to trigger execution review — belongs to the consuming system and the governed review process, not to VEDA.

VEDA surfaces the signal. The ecosystem governs the response.

---

## Deferred Domains

The following observatory domains are owned by VEDA but do not yet have governed search intelligence integration in the first-pass layer:

### GA4 observations

VEDA owns Google Analytics 4 performance observations. GA4 data will eventually participate in the search intelligence layer, particularly for correlating organic search performance with on-site behavioral metrics. No GA4 record family exists in the first-pass schema. The search intelligence layer must not attempt to incorporate GA4 data through ad hoc schema or local modeling until the GA4 record family is governed and added to `schema-reference.md`.

### YouTube enrichment data

VEDA owns YouTube search and channel observatory data. YouTube query-level SERP observations land in `SERPSnapshot` per VEDA-001. YouTube Data API enrichment data — video metadata, channel metadata, statistics snapshots — does not yet have a governed record family. The search intelligence layer must not create YouTube-specific correlation or intelligence patterns that assume the existence of an ungoverned YouTube enrichment model.

### Rule: Do not implement intelligence patterns for deferred domains

Intelligence patterns — correlation logic, derivation functions, signal output types — must not be designed for deferred domains before their canonical record families are governed. An intelligence pattern built on top of an ungoverned record family is ungoverned intelligence. Both the record family and the intelligence pattern must be governed together.

---

## Anti-Drift Rules

### Rule 1 — Search intelligence is observatory interpretation, not planning logic

Every search intelligence output must be explainable as an interpretation of observed external search reality. If an output answers "what should the project do next?" rather than "what does external search reality show?", it is planning logic and does not belong in this layer.

### Rule 2 — Query strings are observations, not owned semantic entities

A query string that VEDA observes through `SERPSnapshot` or `SearchPerformance` is evidence. It is not a VEDA-owned semantic entity. Storing a mapping from observed query strings to topic clusters, intent categories, or semantic entities as canonical VEDA records creates content-graph-adjacent semantics inside the observatory. That mapping belongs in V Forge or Project V if it is needed for planning or execution purposes.

### Rule 3 — Page URLs are observation artifacts, not content graph entities

`SearchPerformance.pageUrl` stores the URL at which performance was measured. The URL is an observation artifact. It is not a V Forge content page. Any correlation between a performance URL and an owned content page happens in the consuming system. VEDA does not model or store that correlation. A URL-to-page mapping stored in VEDA is a content-graph boundary violation.

### Rule 4 — The search intelligence layer must not self-authorize downstream action

An escalation-worthy signal is a noteworthy observation. It is not an instruction to replan, reprioritize, or trigger execution review. The search intelligence layer may classify a condition as escalation-worthy. It may not act on that classification. The governed response belongs to the consuming system and the human-in-the-loop review process.

### Rule 5 — Compute-on-read is the default posture; materialization requires justification

Materializing search intelligence outputs into standing tables without documented operational justification produces a derived truth store that risks becoming the practical source of truth. When materialized outputs are queried instead of observation records, the observation records are effectively displaced. That displacement is a drift toward a second canonical truth store.

### Rule 6 — VEDA Brain patterns must not re-enter through search intelligence vocabulary

"Opportunity score," "content gap signal," "semantic coverage map," "query cluster intelligence," "competitive opportunity ranking" — these are VEDA Brain output types. They do not belong in the search intelligence layer under any name. If a proposed output type describes a planning recommendation or an execution optimization, it belongs in Project V or V Forge, not in VEDA's search intelligence layer.

### Rule 7 — Cross-system signal interfaces remain the governed path out

Search intelligence output that is intended for Project V or V Forge must exit VEDA through the governed signal interfaces: `veda-to-project-v-signal-interface.md` and `veda-to-v-forge-signal-interface.md`. Routing search intelligence output directly into planning records or execution records outside those interfaces is a boundary violation, regardless of the technical convenience.

### Rule 8 — New correlation or derivation patterns require documented rationale

Adding a new correlation type, derivation type, or materialized output to the search intelligence layer requires explicit rationale: what observatory question does this answer, what observation records does it depend on, why compute-on-read is insufficient if materialization is proposed, and why this output belongs in VEDA rather than in a downstream system. A correlation pattern without documented rationale is ungoverned logic.

---

## Non-Goals

This document does not:

- define a ranking algorithm or recommendation system
- govern content gap analysis — that belongs to V Forge's execution intelligence layer
- govern planning recommendation packaging — that belongs to Project V
- constitute a full API contract or migration spec for search intelligence routes
- define the signal package payload format for cross-system interfaces
- govern the YouTube observatory design in detail — that belongs to VEDA-001 and future YouTube-specific implementation docs
- govern GA4 observatory integration — that is deferred pending family design

---

## Final Rule

The search intelligence layer makes VEDA's search observations more useful without making VEDA more than an observatory.

If a search intelligence output requires VEDA to own content-graph entities, generate planning decisions, produce execution recommendations, or absorb downstream interpretation back into its canonical records, the output is out of scope.

The layer serves the telescope. It does not replace it with a planning engine.

---

## Usage

This document should be used:

- when implementing search intelligence derivation logic within VEDA
- when deciding whether a proposed correlation or materialization pattern is legitimate
- when reviewing whether a search intelligence output is observatory truth or planning/execution logic
- when designing search intelligence signal packages for downstream consumers
- when checking whether content-graph semantics are re-entering VEDA through search intelligence vocabulary
- when determining whether a proposed search intelligence feature belongs in VEDA or in a downstream system

---

## Related Docs

- `schema-reference.md`
- `observatory-models.md`
- `veda.md`
- `system-invariants.md`
- `data-boundaries.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `mcp-surface.md`
- `operator-surfaces.md`
- `providers/registry.md`
- `decisions/VEDA-001-youtube-observatory-truth-surface.md`
- `../ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-003-veda-brain-eliminated.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
