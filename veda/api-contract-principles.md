# VEDA API Contract Principles

## Purpose

This document defines the governing API contract principles for VEDA.

It exists to answer:

```text
How does VEDA expose observatory truth through API contracts without drifting into
planning semantics, execution semantics, hidden ownership transfer, provider-specific
payload chaos, or unbounded convenience endpoint growth?
```

Read this with:

- `schema-reference.md`
- `observatory-models.md`
- `search-intelligence-layer.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `data-boundaries.md`
- `system-invariants.md`
- `mcp-surface.md`
- `../ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `../ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `../ecosystem/decisions/ADR-003-veda-brain-eliminated.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- the governing principles for all VEDA API contracts
- how the API relates to VEDA's observatory-only role
- read vs write contract posture
- server-owned vs client-supplied field posture
- raw observation vs derived output contract posture
- provenance requirements in API responses
- immutability and bounded mutability posture
- provider and payload boundary rules
- consumer and cross-system boundary rules
- multi-project and project-scope posture
- route growth and governance posture
- anti-drift rules

---

## Out of Scope

This document does not define:

- individual route family schemas or request/response body shapes — those belong in route-family authority docs
- the full validation and error taxonomy — that belongs in a dedicated validation/error doc
- MCP tool surface design — that belongs in `mcp-surface.md`
- operator surface design — that belongs in `operator-surfaces.md`
- provider-specific ingest implementation details — those belong in provider-specific docs
- signal package payload formats — those belong in the interface docs
- database migration or schema field types — those belong in `schema-reference.md`

---

## System

- veda

---

## Core Rule

VEDA API contracts expose observatory truth.

They do not expose planning decisions, execution instructions, content graph entities, or intelligence synthesis. The API contract shape must be consistent with what VEDA canonically owns: signal, evidence, and observability truth.

A contract that implies VEDA owns something it does not own is incorrect regardless of how convenient it appears.

---

## Relationship to Other VEDA Authority Docs

### Relationship to `schema-reference.md`

`schema-reference.md` governs the canonical record families, their field shapes, and their constraints. This document governs the principles under which those records are exposed through API contracts. Questions about what fields a record carries belong in `schema-reference.md`. Questions about how those fields are exposed, protected, or labeled in API responses belong here.

### Relationship to `observatory-models.md`

`observatory-models.md` governs the conceptual model organization and relationship rules. This document governs how those model relationships are reflected in API contract design — specifically, which relationships may be expressed structurally in contracts and which must remain analytical only. A relationship that is forbidden at the model layer is also forbidden at the contract layer.

### Relationship to `search-intelligence-layer.md`

`search-intelligence-layer.md` governs what the search intelligence layer may derive and expose as signal output. This document governs the contract principles under which that derived output is packaged and labeled in API responses. The compute-on-read vs materialization posture in `search-intelligence-layer.md` directly constrains how derived outputs are represented in contracts.

### Relationship to `mcp-surface.md`

`mcp-surface.md` governs the MCP tool surface that wraps the VEDA API. The MCP surface is a thin transport layer. The enforcement chain runs through the API. This document governs the API contract principles that the MCP surface depends on. MCP tool behavior is bounded by API contract behavior — a tool cannot do what the API prohibits.

### Relationship to signal interfaces

`../interfaces/veda-to-project-v-signal-interface.md` and `../interfaces/veda-to-v-forge-signal-interface.md` govern what crosses the boundary between VEDA and downstream consumers. This document governs the API contract principles that apply to those interface routes. The interface docs define what may cross. This document defines how it must be packaged and labeled when it does.

---

## Canonical Contract Posture

VEDA's API contracts must be:

- **explicit** — contract shapes must make ownership, scope, and mutation posture unambiguous
- **observatory-bounded** — contracts must not expose or imply capabilities VEDA does not own
- **scope-honest** — every project-scoped route must enforce project isolation visibly
- **provenance-preserving** — responses carrying observation truth must carry enough provenance context to support downstream trust assessment
- **derivation-honest** — derived outputs must be labeled as derived; raw observation records must not be displaced by derived outputs in canonical contract positions
- **boring** — contracts should be predictable and stable; clever or adaptive contract shapes that shift meaning at runtime are wrong

A VEDA API contract that could be mistaken for a planning API or execution API has failed the canonical posture test.

---

## Read Contract Principles

### Principle R1 — Reads are scoped to the active project

All project-scoped read routes must enforce project isolation through the session/auth context. Reads must not return records from a project other than the active session project. Cross-project reads are not a feature; they are a boundary violation.

A read route that accepts a project identifier as a caller-supplied parameter and does not validate it against the session context is not enforcing project scope — it is delegating scope enforcement to callers. See also M1 for the full multi-project scope enforcement posture.

### Principle R2 — Reading does not transfer ownership

A consumer reading VEDA observatory data through the API does not become the owner of that data. The API response is a bounded output of VEDA's canonical records. The consumer may interpret it; they do not acquire signal-system ownership by receiving it.

This principle must be reflected in contract design: read responses must not include fields that imply the consumer has write authority over the returned records.

### Principle R3 — Reads must not have hidden side effects

A route that appears to be read-only must not mutate state. VEDA has observation records that are append-friendly and governance records that are mutable within bounds. Reading either must not produce a write as a side effect.

### Principle R4 — Deterministic ordering is required for all list responses

All list-like read responses must define deterministic ordering. Ordering must include a stable tie-breaker. No read route may rely on implicit database ordering or return results in an order that varies across identical queries against identical state.

### Principle R5 — List routes use cursor pagination

First-pass list routes use cursor-based pagination. Offset pagination is not allowed.

Required posture:
- `limit` — maximum records per page; a bounded server-side maximum is enforced
- `cursor` — opaque continuation token from the previous page; omit for the first page
- `nextCursor` in response — the cursor for the next page; must be `null` (not omitted) when no further results exist

Cursor values are opaque to callers. Callers must not decode or construct cursor values. A malformed cursor fails with `400 Bad Request`. A cursor from one route family must not be used with another.

If a list family is small enough to return all records without pagination, that exception must be explicitly declared in the family contract with stated justification. The default is cursor pagination.

### Principle R6 — Observation records are returned as they exist; no silent upgrading

Read routes that return canonical observation records — `SERPSnapshot`, `SearchPerformance`, `SourceItem`, `KeywordTarget` — must return those records as they canonically exist. The response must not silently upgrade, summarize, or derive from those records without labeling the output as derived. See Derived Response Principles.

---

## Write Contract Principles

### Principle W1 — Writes are bounded to observatory-scoped mutation

The write surface of the VEDA API is narrow. VEDA owns observatory governance records (`KeywordTarget`, `SourceFeed`, `Project`) and observatory intake records (`SourceItem`). Observation records (`SERPSnapshot`, `SearchPerformance`) enter through governed ingest paths, not through direct client write routes.

A write route that allows a client to create or modify an observation record as though it were a free-form data entry surface is out of scope. Ingest paths are separate from client write routes and are governed separately.

### Principle W2 — Server-owned fields must not be caller-settable

Fields whose value is determined by server-side logic must not be accepted from callers. If a caller supplies a server-owned field, the request must fail with `400 Bad Request`. Silent ignore is not allowed.

Server-owned fields in VEDA include, at minimum:

- `SERPSnapshot.capturedAt` — set by the ingest path, not by the caller
- `SERPSnapshot.source` — set by the ingest path, not by the caller
- `SERPSnapshot.rawPayload` — set by the ingest path, not by the caller
- `SearchPerformance.capturedAt` — set by the ingest path
- `SourceItem.capturedAt` — set at creation, not modifiable
- `SourceItem.capturedBy` — set at creation, not modifiable
- `EventLog.*` — the event log is append-only and server-written; no client write route exists for it

This list is illustrative. `schema-reference.md` is the definitive authority on which fields are server-owned for each family.

Note: `SourceItem.operatorIntent` is **not** server-owned — it is required to be caller-supplied at creation time and must be non-empty. It becomes immutable after creation per W3. An implementation must not reject `operatorIntent` from callers on creation; it must require it.

### Principle W3 — Immutable fields must be rejected on update

Fields designated as immutable after creation must fail with `400 Bad Request` if supplied in a PATCH or update request. Silent ignore of immutable fields on update is not allowed.

Immutable-after-creation fields in VEDA include, at minimum:

- `SourceItem.url`
- `SourceItem.capturedAt`
- `SourceItem.capturedBy`
- `SourceItem.operatorIntent`
- `SourceItem.contentHash`
- `KeywordTarget.query`, `KeywordTarget.locale`, `KeywordTarget.device` — identity fields; a new target must be created instead of modifying these

### Principle W4 — PATCH body unknown fields must be rejected

Unknown fields in a PATCH request body must be rejected with `400 Bad Request`. Silent ignore of extra body fields is not allowed. This applies to all PATCH routes across all VEDA write surfaces.

### Principle W5 — Writes to observation-ledger records go through ingest paths, not client routes

`SERPSnapshot` and `SearchPerformance` records enter VEDA through governed ingest paths from registered providers. There is no client-facing write route that allows arbitrary creation of these records. The ingest path is governed by `providers/registry.md` and enforced at the API layer.

A request from an unregistered source attempting to write a `SERPSnapshot` must be rejected. Provider identity must be verified before an ingest write is accepted. Verification means authenticating the ingest request against the credentials or token associated with the registered provider entry — not merely accepting a caller-supplied `source` string that matches a registry entry name.

### Principle W6 — Status transitions on governance records emit EventLog entries atomically

Where a governance record state change requires an `EventLog` entry — for example, a `Project.lifecycleState` change or a `SourceItem` status transition — the state change and the log entry must be committed in the same transaction. A state change that commits without its required event log entry is a correctness violation.

### Principle W7 — Unknown query parameters on write routes must be rejected

Unknown query parameters on write routes must fail with `400 Bad Request`. Silent ignore is not allowed.

---

## Derived Response Principles

### Principle D1 — Derived outputs must be labeled as derived

Any API response that returns computed, aggregated, or interpreted output rather than direct canonical observation records must make that distinction explicit in the response. The contract must not allow a caller to mistake derived output for raw observation truth.

Acceptable labeling approaches include:
- a top-level `derived: true` field in the response envelope
- a response type or kind field that identifies the output as computed
- explicit documentation in the route contract that the response is always derived

A derived response that appears structurally identical to a canonical record response is incorrect.

### Principle D2 — Derived output must trace to its source observation records

A derived response must preserve enough provenance context that the caller can determine:
- what observation records produced the output
- what time range or snapshot window the derivation covers
- what provider or source supplied the underlying data
- whether meaningful uncertainty remains

Derived output that cannot answer these questions is provenance-deficient and must not be packaged as a VEDA signal response.

### Principle D3 — Derived output does not replace canonical records in canonical contract positions

A route that returns a canonical observation record must return the canonical record, not a derived view of it. If a route exists to serve derived search intelligence output, it is a distinct route from the route that returns raw `SERPSnapshot` records. These must not collapse into the same response shape without explicit labeling.

### Principle D4 — Compute-on-read is the default; materialized derived output requires documented justification

The default contract posture for derived search intelligence outputs is compute-on-read. A route that serves materialized derived output must document the operational justification for materialization in the route-family authority doc. The justification standard is the same as in `search-intelligence-layer.md`: compute-on-read cost must be demonstrably unsustainable at required query volumes.

### Principle D5 — Deferred observatory domains must not appear in active derived contracts

Observatory domains that are not yet governed — GA4 observations, YouTube enrichment data — must not appear in active API response shapes. A contract that includes fields for a deferred domain implicitly pre-admits that domain as active. Deferred domains must remain absent from active contracts until their canonical record families are governed and added to `schema-reference.md`.

---

## Provenance and Source Principles

### Principle P1 — Required provenance fields must be present in responses

Where a response includes a canonical observation record, the provenance fields required by `schema-reference.md` and `evidence-and-source-provenance.md` must be present in the response. These fields must not be stripped for cleanliness or response size.

Required provenance in VEDA responses includes, at minimum:

- `SERPSnapshot.source` — must be non-null and non-empty
- `SERPSnapshot.capturedAt` — must be present and accurate
- `SERPSnapshot.payloadSchemaVersion` — should be present
- `SearchPerformance.capturedAt` — must be present
- `SourceItem.capturedBy` — must be present
- `SourceItem.operatorIntent` — must be present and non-empty
- `SourceItem.capturedAt` — must be present

### Principle P2 — Source trust posture must not be stripped from responses

Where VEDA's observatory records carry trust posture context — provider identity, source classification, instrument role — that context must be preserved in responses that carry those records. A response that strips trust posture to produce a simpler output creates provenance-deficient signal.

### Principle P3 — Uncertainty must not be erased by response shaping

Where an observation or derived output carries uncertainty — provisional classification, incomplete coverage, limited provider fidelity — that uncertainty must remain visible in the response. A cleaner response shape is not a valid reason to erase uncertainty that materially affects downstream trust posture.

### Principle P4 — Cross-system signal responses must be self-sufficient for governance review

Responses packaged for consumption by Project V or V Forge through the governed signal interfaces must carry enough provenance context that a reviewer can assess the evidence basis, trust posture, and uncertainty without requiring direct access to VEDA's internal records. A signal response that requires VEDA database access to interpret is insufficient for cross-system governance review.

---

## Consumer and Interface Boundary Principles

### Principle C1 — Consuming VEDA API output does not transfer signal ownership

A downstream consumer — Project V, V Forge, an operator surface, an MCP tool caller — that reads VEDA API output does not become the owner of VEDA's observatory records. The consuming system may interpret the output for its own purposes. It does not acquire write authority over the underlying VEDA records through that consumption.

This principle must be reflected in contract design: VEDA API responses must not include mutation tokens, ownership indicators, or fields that imply the caller may subsequently modify the returned records.

### Principle C2 — Cross-system signal responses must exit through governed interfaces

API routes that package VEDA signal for Project V or V Forge consumption must be consistent with the governed signal interfaces. A route that packages planning-relevant signal must be consistent with `../interfaces/veda-to-project-v-signal-interface.md`. A route that packages execution-relevant signal must be consistent with `../interfaces/veda-to-v-forge-signal-interface.md`.

Signal that exits VEDA outside the governed interfaces is ungoverned. There is no shortcut route that bypasses the interface contract because it is operationally convenient.

### Principle C3 — Downstream conclusions must not flow back into VEDA through write routes

VEDA must not expose write routes that accept downstream interpretation as canonical VEDA records. A Project V planning decision derived from VEDA signal is a Project V record, not a VEDA record. A V Forge execution intelligence conclusion is a V Forge record, not a VEDA record. Write routes that accept these as VEDA-owned truth are boundary violations.

### Principle C4 — VEDA internal event log is not a consumer signal route

`EventLog` is VEDA's append-only observatory state-change audit trail. It is not a signal package for downstream consumers. Routes that expose the event log must restrict access to observatory-audit purposes only. Downstream systems must not treat the event log as their primary signal source.

### Principle C5 — Contract shapes must not imply cross-system FK relationships

Contract responses must not include fields that imply a structural FK relationship from VEDA records to records in Project V or V Forge. Cross-system references in responses must use locators, URLs, or external identifiers — not fields that look like FK references into another system's tables.

---

## Provider and Payload Boundary Principles

### Principle PP1 — Provider-specific payload behavior must not leak into canonical contract semantics

The raw provider payload for a `SERPSnapshot` is preserved in `rawPayload` as an evidence archive. Provider-specific field names, schema versions, and payload quirks must not leak into the promoted canonical fields of the VEDA API response. The canonical contract shape must remain stable across provider changes.

Promoted fields (`aiOverviewStatus`, `aiOverviewText`, etc.) represent governed canonical semantics. They must be populated through governed promotion logic, not by surfacing raw provider fields directly.

### Principle PP2 — Provider identity must be recorded but must not drive structural contract branching

Each observation record carries a `source` field that identifies the provider or ingest path. This is a provenance field. It must be preserved in responses. It must not drive structural branching in contract shape — the canonical contract shape for a family must remain the same regardless of which provider supplied the underlying data.

A contract that returns structurally different response shapes depending on which provider supplied the data is a provider-specific contract disguised as a canonical one.

### Principle PP3 — `rawPayload` must not be the primary response surface

`rawPayload` is evidence support. It is not the primary query surface for callers. Routes that need to expose raw provider evidence must do so alongside promoted canonical fields, not instead of them. A route that returns only `rawPayload` without promoted fields is exposing unprocessed provider data as though it were canonical contract output.

### Principle PP4 — Unregistered providers must not produce observable contract outputs

Only providers listed in `providers/registry.md` are active integrations. Ingest from an unregistered source must be rejected before it produces any observable record in the VEDA schema. A `SERPSnapshot` record whose source is not a registered provider must not exist. The API layer must enforce provider registration before accepting ingest writes.

---

## Multi-Project and Scope-Boundary Posture

### Principle M1 — All project-scoped routes enforce project isolation at the API layer

Project-scoped routes must enforce project isolation through the session/auth context at the API enforcement layer. Project scope must not be inferred from request body fields that callers supply. The API must not return records from a project other than the active session project.

A route that accepts `projectId` as a caller-supplied body field and does not validate it against the session context is not enforcing scope — it is trusting the caller.

### Principle M2 — Cross-project reads must fail with non-leaking responses

A request that attempts to read records belonging to a project outside the active session project must fail. The failure response must not leak the existence of the other project's records. A `404 Not Found` response is appropriate for absent-in-scope resources. The response must not vary in shape or message in a way that allows the caller to infer cross-project record existence.

### Principle M3 — Cross-project aggregation must not be exposed through canonical project-scoped routes

A route that aggregates records across multiple projects must be explicitly designated as a cross-project route with its own access model. The canonical project-scoped read routes must not silently aggregate across projects when no project filter is applied. An absent project filter on a project-scoped route is not permission to return all-projects data.

### Principle M4 — Global configuration routes are an explicit exception

`SystemConfig` is the intentional exception to the project-scoped default. Routes that expose global configuration must be explicitly identified as global routes. The global exception does not extend to other route families. A route that returns global data without being explicitly designated as global is incorrect.

---

## Route Growth and Governance Posture

### Principle G1 — Route families must be named after bounded observatory domain concepts

VEDA route families should be named after the canonical model families they expose:

- `serp-snapshots`
- `search-performance`
- `keyword-targets`
- `source-items`
- `source-feeds`
- `projects` — VEDA's thin observatory partition container only; not the Project V planning record (see `schema-reference.md` Project family)
- `signal-packages` — derived output route; read-only; must follow Derived Response Principles D1–D4; not a canonical observation family
- `event-log` — read-only; restricted to observatory-audit purposes only; not a signal route for downstream consumers (see C4)

Vague family names — `data`, `query`, `intel`, `observations`, `search` — are not acceptable. Names must reflect the canonical model family, not a convenience abstraction.

### Principle G2 — New route families require governance review

Adding a new route family is a governed architecture event. It requires:
- a documented observatory question the family answers
- alignment with the canonical model families in `schema-reference.md`
- explicit classification of whether the routes are read-only, write-bounded, or ingest paths
- confirmation that no existing family already covers the need
- confirmation that the family does not introduce content-graph, planning, or execution semantics

A route family added for operational convenience without this review is ungoverned surface.

### Principle G3 — Convenience endpoints must not substitute for canonical family design

A convenience endpoint that aggregates, transforms, or combines output from multiple canonical families is a derived output. It must follow the Derived Response Principles. It must not become the de facto canonical route for a domain. A convenience endpoint that displaces a canonical family route is drift.

### Principle G4 — Deferred domains must not receive active route families

Observatory domains that are deferred — GA4, YouTube enrichment — must not receive active route families until their canonical record families are governed. A route family that pre-admits a deferred domain into the active API contract is acting as though governance has occurred when it has not.

---

## Error Contract Posture

### Principle E1 — VEDA uses a two-level error distinction

- `400 Bad Request` — structural malformation: missing required fields, wrong types, malformed identifiers, malformed cursor, unknown query parameters, caller-supplied server-owned fields, unknown PATCH fields
- `422 Unprocessable Entity` — semantically invalid but well-formed input: controlled-vocabulary violations, lifecycle invalidity, same-project integrity failures, illegal status transition

This distinction is not optional. It applies consistently across all VEDA route families.

### Principle E2 — Error responses use a stable shape

Error responses must use a consistent shape across all VEDA route families:

- `error.code` — machine-readable error code
- `error.message` — human-readable message
- `error.details` — optional structured detail
- `error.requestId` — optional correlation identifier if available

The same class of error must not return wildly different shapes across families.

### Principle E3 — Non-leakage on scope failures

Where project scope is wrong or the target record is outside the active project, routes must return `404 Not Found` rather than a response that reveals the existence of out-of-scope records. The response shape and message must not vary in a way that allows inference about cross-project record existence.

---

## Anti-Drift Rules

### Rule 1 — Contract shapes must not imply planning or execution ownership

If a VEDA API response shape could be mistaken for a planning API response or an execution API response — because it includes planning decision fields, execution status fields, or content graph entity references — it is incorrect. The contract shape must reflect what VEDA canonically owns: observatory records, governance records, and bounded derived signal.

### Rule 2 — Content-graph semantics must not re-enter through route naming or response fields

Route names like `/pages`, `/topics`, `/entities`, `/content-gaps`, or response fields like `pageId`, `topicRef`, `contentArchetype` are content-graph concepts. ADR-002 transferred the content graph to V Forge. These concepts must not reappear in VEDA route families or response shapes under any name.

### Rule 3 — VEDA Brain output types must not reappear as route families or response types

Opportunity scores, content gap signals, semantic coverage maps, query cluster intelligence, competitive opportunity rankings — these are VEDA Brain output types. ADR-003 eliminated VEDA Brain. They must not reappear as VEDA API route families, response types, or derived output labels.

### Rule 4 — Raw observation records must not be displaced by derived output in canonical positions

A contract for a canonical family route must return canonical records. Derived output may be served through explicitly labeled derived routes. The derived route and the canonical route must not collapse into the same contract. When a derived output is queried as though it is the canonical record, the observation records have been effectively displaced.

### Rule 5 — Server-owned provenance fields must remain server-owned in all contract contexts

The provenance fields governed by Principle W2 must remain server-owned in all contract contexts — including signal packages, cross-system interface routes, and operator-facing routes. No contract context justifies making these fields caller-settable.

### Rule 6 — Provider-specific payload behavior must not produce provider-specific contract branching

The canonical contract shape for a family must remain the same regardless of which provider supplied the underlying data. Provider differences belong in the raw payload archive and in promoted fields normalized to canonical semantics. They must not produce different response shapes for different providers.

### Rule 7 — Cross-system signal routes must not widen into general observability dumps

Routes that package VEDA signal for Project V or V Forge must be bounded to the planning-relevant or execution-relevant signal defined in the governed signal interfaces. They must not become general-purpose routes that return all of VEDA's observatory state to the requesting system.

### Rule 8 — Deferred domains must not appear in active contracts under any field name

A deferred observatory domain must not appear in active API contracts — not as a top-level field, not as a nested field, not as an enum value in a controlled vocabulary, not as a null-valued placeholder field. Placeholders imply intent; intent implies governance; governance has not occurred for deferred domains.

---

## Non-Goals

This document does not:

- define individual VEDA route family schemas — those belong in route-family authority docs
- define the full validation and error taxonomy — that belongs in a dedicated validation/error doc
- constitute a route-by-route API specification
- govern MCP tool surface design — that belongs in `mcp-surface.md`
- govern operator surface design — that belongs in `operator-surfaces.md`
- define provider-specific ingest pipeline implementation
- define signal package payload formats in detail — those belong in the interface docs
- govern the YouTube or GA4 observatory design — those are deferred domains
- invent new canonical families or active route families that do not yet exist

---

## Final Rule

VEDA API contracts must expose the observatory faithfully without expanding it.

A contract that makes VEDA easier to use by implying it owns something it does not own, by displacing raw observation truth with convenient derived output, or by admitting deferred domains without governance is not a better contract — it is a drift vector.

The contract serves the observatory. It does not redefine it.

---

## Usage

This document should be used:

- before writing any VEDA route-family authority doc
- when deciding whether a proposed route or response shape stays within observatory scope
- when deciding read vs write posture for a new surface
- when deciding whether derived output requires explicit labeling or a separate route
- when reviewing whether a VEDA API response preserves required provenance
- when deciding whether a new route family requires governance review
- when checking whether content-graph, planning, or execution semantics have re-entered through contract language
- when building hammer expectations for API boundary and scope enforcement

---

## Related Docs

- `schema-reference.md`
- `observatory-models.md`
- `search-intelligence-layer.md`
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
- `../ecosystem/decisions/ADR-007-docs-are-build-spec-db-owns-operational-state.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/data-boundaries.md`
- `../project-v/api-conventions.md`
