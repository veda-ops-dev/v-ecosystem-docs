# VEDA Schema Authority

## Purpose

This document defines the schema authority for VEDA's canonical entities.

It exists to answer:

```text
What entities does VEDA own, what fields must each entity carry at the schema
level, what are the delivery and provenance requirements for VEDA signal packages
and evidence records, how does VEDA govern observatory scope change records, and
how does VEDA reference cross-system entities without duplicating their canonical
data?
```

This is a Tier 1 VEDA schema authority document.

---

## Scope

This document governs:

- the canonical entity set owned by VEDA
- field-level schema contracts for the fully-specified VEDA entities: `evidence`,
  `signal_package`, and `observatory_scope_change`
- evidence provenance and source reference posture
- VEDA-owned signal delivery package entity schema, covering both delivery contexts
- observatory scope change entity schema, aligned to the canonical
  `observatory.scope_change.*` action family
- VEDA's cross-system reference posture for Project V and V Forge identifiers
- honest disclosure of VEDA entity families that are partially specified under
  current docs

---

## Out of Scope

This document does not define:

- Project V-owned entity schemas (project, handoff, decision_record, approval_record,
  intake_outcome, readiness_evaluation)
- V Forge-owned entity schemas (task, content graph, execution records,
  execution_return)
- ecosystem-layer enumerated types — those are defined in
  `ecosystem/ecosystem-schema-spine.md` and must not be redefined here
- storage engine specifics, migration files, indexing strategy, or ORM structure
- VEDA internal ingest pipeline implementation, provider integration configuration
  specifics, or observatory engine mechanics
- transport-layer implementation details for signal delivery

Those belong in the respective system schema authority docs, the ecosystem schema
spine, or implementation docs.

---

## System

- veda

---

## Relationship to Existing Authority Docs

This document derives from and must remain consistent with:

- `interfaces/data-boundaries.md` — the canonical data ownership map that defines
  which record categories VEDA owns; the primary ownership source for this document
- `ecosystem/ecosystem-schema-spine.md` — defines shared enumerated types
  (`actor_type`, `actor_system`, `action_class`, entity type vocabulary, action
  vocabulary), the activity trail record schema contract, and the cross-system
  identity reference pattern; VEDA schema must not redefine those
- `governance/actor-identity-schema-spec.md` — defines the `actor_id` value-class
  contract per `actor_type`; referenced where VEDA records carry actor attribution
- `interfaces/veda-to-project-v-signal-interface.md` — defines the semantic
  requirements for signal delivery packages to Project V; the `signal_package`
  schema derives from it
- `interfaces/veda-to-v-forge-signal-interface.md` — defines the semantic
  requirements for startup signal packages to V Forge; the `signal_package`
  schema covers this delivery context as well
- `interfaces/v-forge-evidence-access-contract.md` — defines evidence record
  freshness metadata requirements; the `evidence` schema derives the response
  field contract from it
- `interfaces/operator-to-veda-observatory-scope-expansion-interface.md` — defines
  the scope change request lifecycle; the `observatory_scope_change` schema derives
  from it
- `interfaces/project-v-to-veda-evidence-request-interface.md` — informs how VEDA
  records the originating request reference in evidence delivery contexts
- `ecosystem/cross-system-boundaries.md` and
  `ecosystem/cross-system-access-governance.md` — define ownership boundaries and
  the cross-system access governance rules VEDA must observe
- `workflows/post-launch-observation-workflow.md` — informs VEDA's observation
  record posture at the schema level

This document does not replace any of those authority docs. It translates their
settled canon into schema-level entity contracts for VEDA.

---

## Core Rule

VEDA is the schema authority for signal truth, evidence truth, and observability
truth. Every entity schema defined here must be consistent with the system ownership
boundaries in `ecosystem/cross-system-boundaries.md` and the canonical data
ownership map in `interfaces/data-boundaries.md`.

VEDA's schema layer must reflect the telescope model: VEDA observes and records
external reality, curates bounded signal packages for governed delivery, and tracks
its own observatory scope and provenance. It does not plan, execute, or make
governing decisions. Those concerns must not appear as owned field semantics in
VEDA entity schemas.

---

## VEDA Schema Authority Boundary

### What belongs in VEDA schema authority

- Evidence record entity schema and its provenance / freshness field contracts
- Signal package entity schema, covering both VEDA → Project V and VEDA → V Forge
  delivery contexts
- Observatory scope change entity schema, aligned to the canonical
  `observatory.scope_change.*` action family
- Evidence provenance and source reference posture for VEDA-owned records
- VEDA's thin references back to Project V project identifiers and to
  originating evidence requests or handoff scopes where interface docs require them
- Partially specified VEDA-owned supporting entity families (source capture,
  source item, observatory event, provider configuration) — acknowledged here,
  not yet fully contracted

### What does not belong here

- Project V decision / handoff / project / approval records
- V Forge execution / content graph / task records
- Ecosystem-layer enumerated types (belong in the schema spine)
- Activity trail records (VEDA produces these; they are governed by the ecosystem
  schema spine, not owned by VEDA)
- Storage engine implementation internals, ingest pipeline mechanics, or provider
  API contract schemas

---

## Canonical VEDA Entity Set

VEDA owns two tiers of entities, both governed by this document.

**Primary canonical entities** are the core VEDA-owned records established in the
canonical data ownership map in `interfaces/data-boundaries.md`. Their schema
contracts are the central purpose of this document.

**Partially specified VEDA entity families** are record families that VEDA clearly
owns but for which current docs do not yet provide a fully closed field contract.
They are listed in the Partially Specified VEDA Entity Families section rather than
presented as complete contracts.

| Entity | Tier | Activity trail entity_type | Status |
|---|---|---|---|
| `evidence` | Primary | `evidence` | Fully contracted below |
| `signal_package` | Primary | `signal_package` | Fully contracted below |
| `observatory_scope_change` | Primary | `observatory_scope_change` | Fully contracted below |
| Source capture record | Partial | — | Partially specified — see below |
| Source item record | Partial | — | Partially specified — see below |
| Observatory event record | Partial | — | Partially specified — see below |
| Provider configuration record | Partial | — | Partially specified — see below |

---

## Evidence Entity Schema Contract

The `evidence` entity is the canonical VEDA record of a captured external observable.
It is the atomic unit of VEDA's truth domain — a single captured data point from
a governed source, with provenance, freshness classification, and trust posture.

The field contract is derived from the freshness metadata requirements in
`interfaces/v-forge-evidence-access-contract.md` (Required fields on every evidence
response) and the provenance/trust requirements in
`interfaces/veda-to-project-v-signal-interface.md` (Trust and provenance metadata).

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `evidence_id` | Yes | No | Stable, globally unique identifier assigned by VEDA. Immutable after assignment. This is the canonical identifier referenced by `entity_id` in activity trail records with `entity_type: evidence`, and by cross-system provenance references in Project V and V Forge records. |
| `project_id` | Yes | No | The project scope this evidence record is associated with. All evidence records must be project-scoped. Cross-project queries are prohibited by the access governance rules. |
| `gathered_at` | Yes | No | UTC timestamp when this evidence was originally gathered or observed from its source. Distinct from `created_at` (record creation). The `gathered_at` timestamp is what freshness classification is calculated from. |
| `created_at` | Yes | No | UTC timestamp when this evidence record was created in VEDA's persistent store. May be later than `gathered_at` if ingestion is asynchronous. |
| `source_provider` | Yes | No | The provider or source system that generated this evidence. Examples: `google_search_console`, `semrush`, `ga4`, `manual_capture`, `source_capture_pipeline`. Used for provenance attribution and trust classification derivation. |
| `source_url` | Yes | Yes | The source URL or canonical source reference for this evidence. Null for evidence types that do not have a direct URL reference (e.g., aggregate metric records). |
| `evidence_class` | Yes | No | The evidence class or signal type this record belongs to. Examples: `search_performance`, `keyword_intelligence`, `competitor_analysis`, `serp_observation`, `source_capture`, `market_signal`, `ranking_record`. The value space for this field is governed by VEDA's observatory configuration and is not fully enumerated in this doc; new evidence classes require VEDA-internal addition before use. |
| `freshness_status` | Yes | No | One of: `fresh`, `aging`, `stale`, `expired`. VEDA's current classification of this record's freshness at the time of last freshness evaluation. Must be recalculated when queried if `freshness_window_end` has passed since the last stored classification. |
| `freshness_window_end` | Yes | No | UTC timestamp at which this record transitions to the next freshness status tier. Defined by VEDA per evidence class. Consuming systems (V Forge, Project V) use this field to determine when a cached reference to this evidence will become stale without re-querying. |
| `trust_classification` | Yes | No | VEDA's trust posture for this evidence record. One of: `verified`, `provisional`, `unverified`. Reflects the reliability of the source provider and the completeness of provenance for this record. Consuming systems must not override or ignore this classification. |
| `provenance_ref` | Yes | Yes | Reference to a source capture record or source item record that provides fuller provenance detail for this evidence, if one exists. Null if no supporting source record exists for this evidence type. |
| `evidence_content` | Yes | No | The actual observable data captured in this record. Structure varies by `evidence_class`. For schema purposes, this is a structured object whose internal shape is governed by VEDA's evidence class definitions, not fully enumerated here. |
| `inference_basis` | Yes | Yes | Where the evidence value is inferred rather than directly observed, a structured description of the inference basis. Null for directly observed evidence. Required when `evidence_class` produces inferred rather than raw captured values. |
| `updated_at` | Yes | No | UTC timestamp of last record update. Evidence records may be updated when freshness status is recalculated or provenance references are resolved. |

### Freshness status definitions

These definitions are carried from `interfaces/v-forge-evidence-access-contract.md`
and are authoritative for all systems consuming VEDA evidence:

- `fresh` — evidence was gathered within the expected refresh interval for its class;
  safe to use without qualification
- `aging` — approaching the end of its expected freshness window; safe to use but
  should be noted as aging in outputs that depend heavily on this evidence
- `stale` — has exceeded its expected freshness window; must be flagged explicitly
  in any output that depends on it; consuming systems should surface this gap
- `expired` — so old that it must not be used for execution or planning decisions;
  consuming systems must treat expired evidence as unavailable

Freshness windows are defined per evidence class by VEDA's observatory configuration.
Consuming systems do not set freshness windows.

### Queryability requirements

The `evidence` entity must support at minimum:

- query by `project_id` + `evidence_class`: retrieve all evidence of a given class
  for a project
- query by `project_id` + `freshness_status`: retrieve all fresh / aging / stale
  records for a project
- query by `evidence_id`: retrieve a specific record for re-validation or re-attribution
- query by `project_id` + `gathered_at` range: retrieve evidence captured within a
  time window

These queries support the access patterns defined in
`interfaces/v-forge-evidence-access-contract.md` (evidence_by_project,
evidence_by_topic, evidence_by_id, signal_status query types).

---

## Signal Package Entity Schema Contract

The `signal_package` entity is VEDA's canonical record of a bounded, curated signal
delivery package. A signal package is the governed unit of signal transfer — what
VEDA delivers to Project V or to V Forge through the governed push delivery interfaces.

The same entity family covers both delivery contexts. The delivery context is
distinguished by context fields (`delivery_target`, `originating_handoff_ref`,
`delivery_trigger_type`) rather than by splitting into separate entity families.
This preserves a single queryable provenance record for all VEDA-initiated signal
deliveries.

The field contract derives from the required semantic fields in
`interfaces/veda-to-project-v-signal-interface.md` and
`interfaces/veda-to-v-forge-signal-interface.md`, and from the minimum additional
fields specified in `ecosystem/activity-trail-integration-map.md` Sections 1 and 4.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `signal_package_id` | Yes | No | Stable, globally unique identifier assigned by VEDA. Immutable after assignment. Must remain stable across re-delivery attempts. This is the `entity_id` referenced in activity trail records with `entity_type: signal_package`. |
| `project_id` | Yes | No | The project scope this package is scoped to. Every signal package must be project-scoped. |
| `delivery_target` | Yes | No | One of: `project_v`, `v_forge`. Identifies which system is the intended recipient of this delivery. Determines which delivery interface and confirmation path apply. |
| `delivery_trigger_type` | Yes | No | One of: `proactive`, `request_response`, `startup`. `proactive` — VEDA-initiated delivery to Project V based on VEDA's curation judgment. `request_response` — VEDA's curated response to a Project V evidence request. `startup` — VEDA-initiated execution-startup package tied to a confirmed V Forge handoff scope. This field is the primary distinguisher between the three delivery contexts within the single entity family. |
| `originating_request_ref` | Yes | Yes | Reference to the `evidence_request_id` (Project V-owned) of the originating evidence request, when `delivery_trigger_type` is `request_response`. Null for `proactive` and `startup` deliveries. Required for `request_response` to link the delivery leg to the request leg in the activity trail. |
| `originating_handoff_ref` | Yes | Yes | Reference to the `handoff_id` (Project V-owned) of the confirmed handoff that triggered this delivery, when `delivery_trigger_type` is `startup`. Null for `proactive` and `request_response` deliveries. Required for `startup` to tie the package to a specific governed execution context. |
| `signal_scope` | Yes | No | What class or domain of signal this package represents — the bounded signal classes included. Structured as an array of evidence class labels. Bounded to what is planning-relevant or execution-startup-relevant for the delivery context. |
| `planning_concern_summary` | Yes | Yes | VEDA's curation rationale — a bounded statement of what planning concern, question, or execution context this package is intended to address. Required for `proactive` and `request_response` deliveries. May be null for `startup` deliveries where the curation rationale is the startup scope itself. This is VEDA's signal framing, not a planning instruction. |
| `bounded_evidence_refs` | Yes | No | Array of thin references to the `evidence` records included or pointed to by this package. Each reference carries: `evidence_id`, `evidence_class`, `gathered_at`, `freshness_status`, `trust_classification`. This is a reference array, not a copy of evidence content. VEDA remains the canonical owner of the referenced evidence records. |
| `freshness_classification` | Yes | No | VEDA's overall freshness assessment for this package. One of: `fresh`, `aging`, `stale`, `uncertain`. Reflects the worst-case freshness of the evidence included in the package. Consuming systems must not assume the package is more current than this classification indicates. |
| `trust_classification` | Yes | No | VEDA's overall trust posture for this package. One of: `verified`, `provisional`, `unverified`. Reflects the lowest trust level among evidence records included. Must not be upgraded by consuming systems. |
| `observation_timestamps` | Yes | No | Structured record of when the underlying evidence was gathered or observed. At minimum: `earliest_gathered_at` and `latest_gathered_at` timestamps. Both are required so consuming systems can assess how current the signal context is. |
| `delivery_initiated_at` | Yes | No | UTC timestamp when VEDA initiated this delivery. |
| `receipt_confirmed_at` | Yes | Yes | UTC timestamp when the target system confirmed receipt. Null until confirmation is received. |
| `delivery_state` | Yes | No | Current delivery state. See delivery states below. |
| `package_version_posture` | Yes | No | One of: `original`, `revision`. If `revision`, `prior_package_ref` must be populated. |
| `prior_package_ref` | Yes | Yes | Reference to the `signal_package_id` of the prior package this revision supersedes. Required when `package_version_posture` is `revision`. Null for original packages. |
| `created_at` | Yes | No | UTC timestamp of package record creation. |
| `updated_at` | Yes | No | UTC timestamp of last record update. |

### Signal package delivery states

- `pending` — package has been created but delivery has not yet been initiated
- `delivered` — VEDA has initiated push delivery; recipient confirmation not yet received
- `confirmed` — receiving system has confirmed receipt; delivery is complete
- `failed` — delivery attempt produced no confirmation within the expected window
- `voided` — package was superseded or withdrawn before confirmation

### Delivery context distinctions

The three `delivery_trigger_type` values map to distinct delivery contexts that
share the same entity structure:

| Dimension | `proactive` | `request_response` | `startup` |
|---|---|---|---|
| Delivery target | `project_v` | `project_v` | `v_forge` |
| Initiation | VEDA curation judgment | Triggered by Project V evidence request | Triggered by confirmed handoff |
| `originating_request_ref` | Null | Required | Null |
| `originating_handoff_ref` | Null | Null | Required |
| `planning_concern_summary` | Required | Required | Optional |
| Governing interface | `veda-to-project-v-signal-interface.md` | `veda-to-project-v-signal-interface.md` | `veda-to-v-forge-signal-interface.md` |

---

## Evidence Provenance and Source Reference Posture

VEDA's evidence records must preserve full provenance for every captured observable.
Provenance is not optional metadata — it is the mechanism by which trust classification
is derivable, freshness is calculable, and governance replay is possible.

### Provenance fields on every evidence record

Every `evidence` record must carry sufficient provenance to answer:
- what source or provider produced this observable?
- when was it captured?
- what is VEDA's trust assessment of that source?
- is there a source capture record with fuller provenance detail?

The `source_provider`, `gathered_at`, `trust_classification`, and `provenance_ref`
fields on the `evidence` entity collectively satisfy this requirement for the schema layer.

### Relationship between evidence records and source-supporting records

For evidence classes where a source capture record exists (see Partially Specified
VEDA Entity Families), the `evidence.provenance_ref` field carries a reference to
that supporting record. The source capture record contains the fuller provenance
detail — raw source URL, capture method, provider session or API call identity,
and any source item sub-records.

The `evidence` record is the queryable schema entity. The source capture record
is the provenance backing artifact. An evidence record without a `provenance_ref`
is still valid if the provenance is fully carried by `source_provider`, `source_url`,
and `gathered_at` alone — source capture records are additional provenance depth,
not a mandatory prerequisite.

### External-origin context is provenance, not actor identity

External sources that produce observable data are provenance context on evidence
records, not governed ecosystem actors. The `source_provider` field carries the
identity of the external source. This must not be conflated with the `actor_id`
field on activity trail records.

When VEDA produces an activity trail record for an evidence creation event, the
`actor_type` is `system` (the VEDA ingest process), the `actor_id` is the VEDA
system process identifier, and the `actor_system` is `veda`. The external source
that produced the underlying data is carried in `evidence.source_provider` and
`evidence.source_url` — not in the activity trail actor fields.

This distinction is required by `governance/actor-identity-schema-spec.md`:
external-origin context is provenance captured in record fields, not a canonical
`actor_type` value.

### Provenance preservation by consuming systems

When Project V or V Forge reference an evidence record in their own records, they
must preserve the minimum provenance fields: `source_system: veda`,
`evidence_id`, `gathered_at`, `freshness_status`, and `trust_classification`.
This requirement is derived from the cross-system reference posture in
`ecosystem/ecosystem-schema-spine.md` and from the attribution requirements in
`interfaces/v-forge-evidence-access-contract.md`.

VEDA must not deliver evidence without these provenance fields populated. Consuming
systems must not strip provenance from evidence references when including them in
their own records or outputs.

---

## Observatory Scope Change Entity Schema Contract

The `observatory_scope_change` entity is VEDA's canonical record of a governed
observatory scope change request and its processing lifecycle. This entity is the
schema counterpart to the `observatory.scope_change.*` action type family in the
activity trail.

The field contract derives from the request semantics defined in
`interfaces/operator-to-veda-observatory-scope-expansion-interface.md` and the
activity trail integration map Section 11.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `observatory_scope_change_id` | Yes | No | Stable, globally unique identifier assigned when the request is received by VEDA. This is the `entity_id` referenced in activity trail records with `entity_type: observatory_scope_change`. Must remain stable across the full request lifecycle (from request receipt through implementation or rejection). |
| `request_identity` | Yes | No | The stable request identity assigned by the initiating system and carried in the scope change request. May differ from `observatory_scope_change_id` if VEDA assigns its own internal tracking identity; both must be preserved. |
| `initiating_actor_surface` | Yes | No | One of: `operator_direct`, `project_v_mediated`. Identifies which initiation path was used. `operator_direct` means the operator issued the request directly. `project_v_mediated` means Project V routed the request on behalf of an operator with documented approval. |
| `proximate_initiator_ref` | Yes | No | Actor reference for the system or actor that sent the request. For `operator_direct`: the operator's stable user record identifier per `governance/actor-identity-schema-spec.md`. For `project_v_mediated`: the Project V system process identifier. |
| `operator_approval_ref` | Yes | No | Reference to the governed approval that authorized this scope change request. Required on all requests — a record without a resolvable approval reference is not a valid governed scope change. For `operator_direct`: the operator's own decision record reference. For `project_v_mediated`: the external operator approval record reference that Project V carried in the request. |
| `originating_context_ref` | Yes | Yes | Reference to the governance context that triggered this request, if applicable. Examples: a return-to-planning finding, a launch readiness gap, a planning review. Null when the operator initiated the request independently without a specific upstream trigger. |
| `change_type` | Yes | No | One of: `add_observation_target`, `expand_signal_coverage`, `narrow_retire_scope`, `refresh_reclassify_coverage`, `change_cadence_depth`. Must be classifiable into one of the five change categories defined in the interface doc. |
| `target_scope_summary` | Yes | No | Bounded description of what scope is being changed — at minimum one of: project or portfolio scope, signal class, source class, topic/keyword scope, or observation target/URL scope. |
| `reason` | Yes | No | The legible governance rationale for this scope change. Must be a real governance rationale, not a generic instruction. |
| `external_action_acknowledged` | Yes | No | Boolean. True if the request explicitly acknowledged that the scope change may trigger paid external retrieval, new provider integrations, or material cost increase. Required to be true when the change type implies such implications; false only when the scope change is narrowing or reclassification with no cost implications. |
| `lifecycle_state` | Yes | No | Current state of this scope change request. See lifecycle states below. |
| `veda_response_summary` | Yes | Yes | VEDA's response summary: what was accepted, what was narrowed (if any), or the rejection/deferral reason. Null until VEDA produces a response. |
| `narrowed_scope_summary` | Yes | Yes | If `lifecycle_state` is `narrowed`: a bounded description of the subset of the requested scope that VEDA accepted. Null otherwise. |
| `deferral_reason` | Yes | Yes | If `lifecycle_state` is `deferred`: the specific reason VEDA cannot currently implement. Null otherwise. |
| `rejection_reason` | Yes | Yes | If `lifecycle_state` is `rejected`: the specific reason the request was rejected (validity failure, missing authority reference, out-of-bounds scope). Null otherwise. |
| `implementation_summary` | Yes | Yes | When `lifecycle_state` is `implemented`: a description of what specifically changed in VEDA's observatory. Null until implementation is confirmed. |
| `requested_at` | Yes | No | UTC timestamp when VEDA received the scope change request. |
| `responded_at` | Yes | Yes | UTC timestamp when VEDA produced its response (accepted, narrowed, deferred, or rejected). Null until response is produced. |
| `implemented_at` | Yes | Yes | UTC timestamp when VEDA confirmed the scope change was implemented. Null until implementation is complete. |
| `voided_at` | Yes | Yes | UTC timestamp of voiding or supersedence, if applicable. Null otherwise. |
| `superseded_by_ref` | Yes | Yes | Reference to the `observatory_scope_change_id` of the superseding request, if this request was voided by a new request. Null otherwise. |

### Observatory scope change lifecycle states

These states align to the `observatory.scope_change.*` action type family in the
activity trail:

- `received` — VEDA has received the request and is assessing it
- `accepted` — VEDA has determined the request is valid and will proceed with implementation
- `narrowed` — VEDA accepts a bounded subset of the requested scope; narrowing reason
  and accepted subset are recorded
- `deferred` — VEDA cannot currently implement; deferral reason and re-entry posture
  recorded
- `rejected` — VEDA has rejected the request; rejection reason recorded
- `implemented` — VEDA confirms the scope change is in effect in the observatory
- `voided` — the request was withdrawn or superseded before VEDA acted

**Note:** `accepted` and `implemented` are distinct states. `accepted` means VEDA
will proceed; `implemented` means the change is in effect. Both must be recorded
as distinct activity trail events and both must be reflected in this entity's
lifecycle state progression.

---

## VEDA Cross-System Reference Posture

VEDA records reference Project V project identifiers and originating request/handoff
identifiers where interface docs require them. All cross-system references from VEDA
records must follow the thin-reference pattern defined in
`ecosystem/ecosystem-schema-spine.md`.

### VEDA references to Project V identifiers

VEDA uses the Project V `project_id` to scope evidence records, signal packages,
and observatory scope change records to a specific project. This reference is a
scoping identifier, not a copy of Project V's project record content.

- `evidence.project_id` — scoping reference; VEDA does not store Project V project
  metadata in evidence records
- `signal_package.project_id` — scoping reference for delivery packages
- `observatory_scope_change` records carry project or portfolio scope context in
  `target_scope_summary`; where a specific project is the target, the `project_id`
  may be carried as a scoping reference in `details` on associated activity trail records

VEDA does not own Project V project records. The `project_id` field is a foreign
key pointing to Project V's authority; VEDA must not store richer planning metadata
as though it were VEDA-owned.

### VEDA references to originating evidence requests

When `signal_package.delivery_trigger_type` is `request_response`, the package
carries `originating_request_ref` — a reference to the Project V-owned
`evidence_request_id`. This is a thin reference linking the VEDA delivery back to
its governing request. VEDA does not copy or own the evidence request record;
it references the identifier assigned by Project V.

### VEDA references to originating handoffs

When `signal_package.delivery_trigger_type` is `startup`, the package carries
`originating_handoff_ref` — a reference to the Project V-owned `handoff_id` of the
confirmed handoff that triggered startup signal delivery. This is a thin reference.
VEDA does not store handoff content; it references the handoff by its Project V-assigned
identifier to tie the startup package to a specific governed execution context.

### Provenance fields on cross-system VEDA references

Any cross-system reference carried by a VEDA record must include:
- the `entity_type` of the referenced entity
- the `entity_id` as assigned by the owning system
- a timestamp context (`requested_at`, `originating_request_created_at`, or equivalent)

VEDA must not store richer content from cross-system entities than what is required
for this reference posture.

---

## Partially Specified VEDA Entity Families

The following entity families are clearly VEDA-owned based on the canonical data
ownership map in `interfaces/data-boundaries.md`, but current docs do not yet
provide a fully closed field contract for them. They are listed here with their
ownership established and their partial specification acknowledged. Full contracts
should be added when VEDA implementation work reaches these families.

### Source Capture Record

**Ownership:** VEDA. Source capture records are provenance depth artifacts that
back evidence records with fuller capture-session context.

**What is known from current docs:**
- referenced by `evidence.provenance_ref` where applicable
- must carry: source provider identity, capture timestamp, source URL or source
  reference, and capture method or provider session identity
- relationship to source item records (where a capture session produces multiple
  items) is implied by the ownership model but not explicitly structured in current docs

**What remains soft:** The internal structure of capture session records — what fields
distinguish different capture methods, what a "provider session identity" looks like
in schema terms, how capture records chain to source item records — is not specified
in current interface or governance docs. VEDA implementation docs must extend this
contract.

**Schema-ready posture:** Ownership established; `evidence.provenance_ref` linkage
defined; internal field contract deferred to VEDA implementation docs.

---

### Source Item Record

**Ownership:** VEDA. Source item records are the sub-records within a source capture
session — individual URLs, pages, keywords, or data points captured as part of a
single observatory capture operation.

**What is known from current docs:**
- listed in the canonical data ownership map as a VEDA-owned record family
- implied parent-child relationship to source capture records
- individual items within a capture are the atomic observables that may become
  evidence records after VEDA's classification and trust evaluation

**What remains soft:** No current interface or governance doc specifies the internal
field structure of source item records. The relationship between a source item and
an evidence record (one-to-one, one-to-many, or many-to-one) is not specified.

**Schema-ready posture:** Ownership established; internal field contract and
item-to-evidence relationship deferred to VEDA implementation docs.

---

### Observatory Event Record

**Ownership:** VEDA. Observatory event records are VEDA's internal event log for
observatory state changes, ingestion events, and provider sync events.

**What is known from current docs:**
- the post-launch observation workflow and the activity trail model both reference
  VEDA's observatory event records as sources of continuity
- `observation_record` (used in activity trail for `observation.classify`,
  `observation.assess`, `observation.cycle` events) is a Project V / V Forge
  record of the classification outcome, not a VEDA observatory event record
- VEDA's internal observatory event log is distinct from the ecosystem activity trail
  and from the `observation_record` entity type; it is VEDA-internal operational logging
- evidence continuity model references observatory event log as a source for future
  reconsideration, implying retention and queryability requirements

**What remains soft:** The field structure of VEDA's internal observatory event
records is not specified in any current interface or governance doc. The distinction
between what belongs in the ecosystem activity trail vs. what belongs in VEDA's
internal event log is clear in principle but not resolved at the field level.

**Schema-ready posture:** Ownership established; ecosystem activity trail vs.
VEDA-internal log distinction clear; internal field contract deferred to VEDA
implementation docs.

---

### Provider Configuration Record

**Ownership:** VEDA. Provider integration configuration and ingest pipeline records
are VEDA-owned operational configuration records.

**What is known from current docs:**
- listed in the canonical data ownership map
- observatory scope expansion interface implies that provider configuration changes
  are a consequence of accepted scope change requests
- external-action governance and cost posture for provider integrations is referenced
  in the scope change interface

**What remains soft:** No current doc specifies the field structure of provider
configuration records, how they relate to observatory scope change records, or
how provider-specific configuration fields are organized. This is substantially
VEDA-internal implementation detail.

**Schema-ready posture:** Ownership established; relationship to scope change events
implied; full field contract deferred to VEDA implementation docs.

---

## Anti-Drift Rules

**VEDA must not absorb Project V planning truth or V Forge execution truth.**
VEDA evidence records must not store planning decisions, handoff content, or execution
findings as though they are VEDA-owned observables. If VEDA receives planning context
from Project V to scope its observatory targets, that context is a scoping reference
— not VEDA-owned planning data. The `project_id` field is a scoping foreign key,
not a stored copy of Project V's planning record.

**`signal_package` does not replace `evidence` records.**
A signal package is a curated delivery unit — a bounded set of references to evidence
records organized for a specific delivery context. It is not a denormalized copy of
evidence content. Evidence records remain the canonical VEDA observables; signal
packages are the governed transfer artifacts. Consuming systems must trace evidence
back to its canonical `evidence_id`, not treat the package as the evidence source.

**Evidence records must preserve provenance.**
An evidence record without `source_provider`, `gathered_at`, and `trust_classification`
is not a valid governed VEDA record. Provenance stripping — whether through ingest
pipeline shortcuts or schema shortcuts — produces ungoverned evidence that cannot
satisfy governance replay requirements. VEDA must not create evidence records without
full provenance.

**External source context is provenance, not canonical actor identity.**
The external source (Google Search Console, SEMrush, a scraped source URL) that
produced an observable is captured in `evidence.source_provider` and
`evidence.source_url`. This is provenance metadata on the evidence record. It must
not be inserted into activity trail `actor_type`, `actor_id`, or `actor_system`
fields, which carry the VEDA system process identity — not the external origin.

**VEDA references to Project V and V Forge are thin pointers, not copied truth.**
`signal_package.originating_request_ref`, `signal_package.originating_handoff_ref`,
and all `project_id` scope fields are thin references to identifiers owned by other
systems. VEDA must not store richer copies of Project V planning records or V Forge
execution records as though they become VEDA-owned data by being referenced.

**Observatory scope changes require operator approval reference; they must not be
self-authorized.**
An `observatory_scope_change` record without a resolvable `operator_approval_ref`
is not a valid governed record. VEDA must reject requests that do not carry this
reference. System processes, agents, and V Forge execution findings must not produce
observatory scope change records without the required operator approval chain being
present. This rule derives from the Core Rule in
`interfaces/operator-to-veda-observatory-scope-expansion-interface.md`.

**`accepted` and `implemented` observatory scope change states are distinct.**
An `observatory_scope_change` record in `accepted` state means VEDA will proceed.
The record must not be updated to `implemented` until the scope change is confirmed
in effect in VEDA's observatory. Collapsing these states produces records that cannot
be queried to determine whether a scope change is in progress vs. complete.

**VEDA must not self-expand observatory scope as a consequence of V Forge evidence
queries.**
V Forge evidence queries through `interfaces/v-forge-evidence-access-contract.md`
do not authorize VEDA to expand its observatory scope. A `signal_status` query
result showing no coverage for a signal class is a coverage gap finding — it is not
authorization to add coverage. Coverage expansion requires a governed scope change
request with operator approval.

**Signal packages that are not project-scoped are not valid.**
Every `signal_package` must carry a `project_id`. Portfolio-scoped deliveries
must still identify the portfolio or the specific projects included in scope.
Unscoped signal packages that cross project lines without a declared scope are
not valid governed deliveries.

---

## Usage

This document should be used:

- when implementing VEDA's persistence layer: use the `evidence`, `signal_package`,
  and `observatory_scope_change` schema contracts as the field-level specifications
  for VEDA database tables or collections
- when implementing VEDA signal delivery: use the `signal_package` schema to ensure
  delivery records carry the required fields for both Project V and V Forge delivery
  contexts; use `delivery_trigger_type` to distinguish contexts rather than creating
  separate entity types
- when implementing VEDA evidence curation and ingest: use the `evidence` schema
  contract to ensure every captured observable carries provenance, freshness, and
  trust classification before it enters the queryable evidence store
- when implementing the observatory scope change processing path: use the
  `observatory_scope_change` schema and lifecycle states to ensure VEDA's response
  to each governed scope change request is durably recorded
- when V Forge or Project V schemas need to reference VEDA entities: use the thin
  reference pattern defined in the VEDA Cross-System Reference Posture section and
  the ecosystem schema spine
- when VEDA implementation work reaches source capture, source item, observatory
  event, or provider configuration records: use the Partially Specified VEDA Entity
  Families section as the starting point; extend those contracts through VEDA
  implementation docs, not by modifying this document casually
- when adding new evidence classes: the value space for `evidence.evidence_class` is
  governed by VEDA's observatory configuration; new values require VEDA-internal
  addition with a corresponding update to this document's notes if the value is
  ecosystem-relevant

---

## Related Docs

- `ecosystem/ecosystem-schema-spine.md` *(shared enumerated types, activity trail record schema, cross-system reference pattern)*
- `governance/actor-identity-schema-spec.md` *(actor_id value-class contract)*
- `interfaces/data-boundaries.md` *(canonical data ownership map)*
- `interfaces/veda-to-project-v-signal-interface.md` *(signal delivery to Project V — semantic requirements for signal_package)*
- `interfaces/veda-to-v-forge-signal-interface.md` *(startup signal delivery to V Forge — semantic requirements for startup signal_package)*
- `interfaces/v-forge-evidence-access-contract.md` *(evidence freshness metadata requirements — derives evidence field contract)*
- `interfaces/operator-to-veda-observatory-scope-expansion-interface.md` *(scope change request lifecycle — derives observatory_scope_change schema)*
- `interfaces/project-v-to-veda-evidence-request-interface.md` *(evidence request semantics — informs originating_request_ref)*
- `ecosystem/activity-trail-model.md` *(activity trail field contract, entity type vocabulary)*
- `ecosystem/activity-trail-integration-map.md` *(seam-to-action-type mapping)*
- `ecosystem/cross-system-boundaries.md` *(ownership boundaries)*
- `ecosystem/cross-system-access-governance.md` *(access governance, anti-drift rules)*
- `workflows/post-launch-observation-workflow.md` *(observation record posture)*
- `project-v/project-v-schema-authority.md` *(Project V entity schemas — the cross-system reference target for project_id and evidence_request_id)*
- `v-forge/v-forge-schema-authority.md` *(V Forge entity schemas — to be created)*
