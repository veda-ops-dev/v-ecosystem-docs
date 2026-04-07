# Ecosystem Schema Spine

## Purpose

This document formalizes the shared schema conventions that all three system
schema authority docs — Project V, VEDA, and V Forge — depend on.

It exists to answer:

```text
What are the shared schema-layer contracts at the ecosystem level: the activity
trail record schema, the canonical enumerated types, the cross-system identity
reference posture, and the retention rules that implementations across all three
systems must treat as fixed?
```

This is a Tier 1 ecosystem schema authority document.

---

## Scope

This document governs:

- the activity trail record schema as an ecosystem-layer schema contract
- the canonical enumerated types for `actor_type`, `actor_system`,
  `action_class`, action vocabulary, and entity type vocabulary
- the cross-system identity and reference posture applicable across all three systems
- retention and compaction constraints for ecosystem-level records
- the ecosystem-layer schema authority boundary

---

## Out of Scope

This document does not define:

- Project V local entity schemas (project, handoff, decision_record,
  approval_record, intake_outcome, readiness_evaluation)
- VEDA local entity schemas (evidence, signal_package, observatory event records,
  source capture records)
- V Forge local entity schemas (task, execution record, content graph entities,
  execution intelligence records)
- transport or storage engine implementation specifics
- database engine syntax, migration files, or index definitions
- the UI for activity trail browsing or live event subscription mechanics

System-specific entity schemas belong in their respective schema authority docs.
Implementation specifics belong in implementation docs.

---

## System

- ecosystem

---

## Relationship to Existing Authority Docs

This document translates and formalizes schema-facing shared conventions that
are already defined semantically in:

- `ecosystem/activity-trail-model.md` — defines what gets recorded, the required
  fields, the action vocabulary, the entity type vocabulary, the retention posture,
  and the query/replay expectations
- `ecosystem/activity-trail-integration-map.md` — maps each governed seam event
  to its canonical action type, producing system, entity reference, and minimum
  additional fields
- `ecosystem/cross-system-boundaries.md` — defines ownership boundaries and the
  rule that read access does not transfer ownership
- `ecosystem/cross-system-access-governance.md` — defines the six access patterns,
  the logging requirement, the provenance requirement, and the anti-drift rules
- `interfaces/data-boundaries.md` — defines the canonical data ownership map and
  the cross-system reference posture per system
- `governance/auth-and-actor-model.md` — defines actor classes, the identity
  principle, and the minimum actor semantics required for governed actions

This document does not replace any of those authority docs. It translates their
settled canon into the shared schema conventions that the three system schema
authority docs will reference.

Where this document and a source authority doc appear to conflict, the source
authority doc governs. This document derives from those docs; it does not
override them.

---

## Core Rule

The ecosystem schema spine defines the shared schema layer that every system-level
schema authority doc must be consistent with.

Any schema entity, record type, or field defined in a system schema authority doc
that touches the activity trail, references a cross-system entity, or uses
vocabulary covered here must conform to the contracts in this document.

System schema authority docs extend the ecosystem spine. They do not contradict it.

---

## Ecosystem-Layer Schema Authority Boundary

### What belongs in the ecosystem schema spine

The following are ecosystem-layer schema concerns. They are defined here and
referenced by system schema authority docs, not redefined inside them.

- The activity trail record schema: field names, types, required vs nullable
  posture, and allowed value sets for enumerated fields.
- The canonical enumerated types: `actor_type`, `actor_system`, `action_class`,
  the action vocabulary, and the entity type vocabulary.
- Cross-system identity reference conventions: how one system's records reference
  another system's entities, what makes a reference thin vs duplicative, and
  what provenance fields are required on cross-system references.
- Retention and compaction posture for ecosystem-level records.

### What belongs in system schema authority docs

The following are system-layer schema concerns and belong in the respective
system schema authority docs, not here.

- Project V entity schemas: project, handoff, decision_record, approval_record,
  intake_outcome, readiness_evaluation, planning-side traceability records.
- VEDA entity schemas: evidence, signal_package, observatory event record, source
  capture record, evidence provenance record, provider configuration record.
- V Forge entity schemas: task, execution record, content graph entities (page,
  topic, entity, internal_link, archetype, schema_usage), execution_intelligence
  record, execution_return record, bounded execution findings record.
- System-specific lifecycle states, field validation rules, and internal reference
  patterns that do not cross system lines.

A schema decision that requires choosing between two systems as the canonical owner
is a boundary question — resolve it by consulting `interfaces/data-boundaries.md`
and `ecosystem/cross-system-boundaries.md`, not this document.

---

## Canonical Enumerated Types

The following enumerated types are canonical across the ecosystem. All activity
trail records and all cross-system references must use only these values. Additions
require a canon-change edit to `ecosystem/activity-trail-model.md` first, then
reflection here.

---

### `actor_type`

Allowed values:

- `agent` — an LLM-driven or software-driven actor
- `operator` — a human participant with governed review, direction, or approval
  responsibilities
- `system` — a non-agent automated system process operating within a bounded function

These three values cover all actor types that produce activity trail records.
The External Actor class defined in `governance/auth-and-actor-model.md` is an
ecosystem governance concept; external actors do not produce activity trail records
under their own attribution. External inputs enter the ecosystem through defined
interfaces (VEDA signal, intake workflow) and the resulting activity records carry
the receiving system's actor attribution.

---

### `actor_system`

Allowed values:

- `project_v` — the Project V planning system
- `veda` — the VEDA observatory and signal system
- `v_forge` — the V Forge execution system
- `ecosystem` — ecosystem-level processes not owned by a single system
- `extension` — governed extensions or integrations operating under an explicit
  ecosystem authority grant

---

### `action_class`

Allowed values:

- `state_change` — any action that creates, updates, or transitions the state of a
  record within a system
- `cross_system_access` — any action where one system reads, receives, or queries
  data from another system through a governed interface
- `approval` — any approval request, approval decision, escalation, or governance
  gate evaluation
- `budget` — any action that incurs token cost, triggers budget evaluation, or
  records a cost event
- `lifecycle` — any agent lifecycle event (start, heartbeat, complete, fail, block,
  pause, resume) or system-level lifecycle event

---

### Action Vocabulary (Canonical Enumeration)

All activity trail records must use action types from this enumeration. The
dot-namespace pattern is mandatory. Values not in this list are not canonical and
must not appear in activity trail records.

**Cross-system access actions:**
- `evidence.query`
- `evidence.request`
- `signal.query`
- `execution.query`

**Cross-system delivery actions — VEDA → Project V:**
- `signal.delivery`
- `signal.delivery.confirmed`
- `signal.delivery.failed`
- `signal.delivery.voided`

**Cross-system delivery actions — VEDA → V Forge:**
- `signal.delivery.startup`

*(Receipt confirmation and failure on the V Forge startup delivery use
`signal.delivery.confirmed` and `signal.delivery.failed` respectively,
with `actor_system` and `target_system` set to reflect the V Forge context.)*

**Cross-system delivery actions — V Forge → Project V:**
- `execution.return`
- `execution.return.confirmed`
- `execution.return.failed`
- `execution.return.voided`

**Planning intake outcome actions:**
- `intake.defer`
- `intake.hold`
- `intake.reject`
- `intake.close`

**Post-launch observation actions:**
- `observation.cycle`
- `observation.classify`
- `observation.assess`

**Observatory scope change actions:**
- `observatory.scope_change.request`
- `observatory.scope_change.accepted`
- `observatory.scope_change.narrowed`
- `observatory.scope_change.deferred`
- `observatory.scope_change.rejected`
- `observatory.scope_change.implemented`
- `observatory.scope_change.voided`

**State change actions:**
- `project.create`
- `project.update`
- `project.archive`
- `task.create`
- `task.assign`
- `task.start`
- `task.complete`
- `task.fail`
- `task.cancel`
- `evidence.create`
- `evidence.update`
- `evidence.expire`
- `handoff.create`
- `handoff.confirmed`
- `handoff.failed`
- `handoff.reject`
- `handoff.recall`
- `handoff.recall.confirmed`
- `content.create`
- `content.update`
- `content.publish`

**Execution-seam actions (stub-level posture):**
- `execution.clarification`
- `execution.clarification.confirmed`
- `execution.scope_update`
- `execution.scope_update.confirmed`

**Approval actions:**
- `approval.request`
- `approval.decide`
- `approval.escalate`

**Budget actions:**
- `budget.cost_event`
- `budget.warning`
- `budget.hard_stop`
- `budget.resume`

**Agent lifecycle actions:**
- `agent.start`
- `agent.heartbeat`
- `agent.complete`
- `agent.fail`
- `agent.block`
- `agent.pause`
- `agent.resume`

**System actions:**
- `system.startup`
- `system.shutdown`
- `system.error`
- `system.recovery`

---

### `entity_type` (Canonical Enumeration)

The `entity_type` field on every activity trail record must use a value from
this enumeration. The owning system column indicates which system's schema
authority doc defines the full entity schema for that type.

| Entity type | Owning system | Description |
|---|---|---|
| `project` | Project V | A Project V project record |
| `evidence` | VEDA | A VEDA evidence or observatory record |
| `task` | V Forge | A V Forge task or execution record |
| `handoff` | Project V | A Project V handoff record |
| `agent` | ecosystem | An agent instance |
| `signal_package` | VEDA | A VEDA signal delivery package (used for VEDA → Project V and VEDA → V Forge delivery events) |
| `execution_return` | V Forge | A V Forge return-to-planning findings package |
| `launch_authorization` | Project V | A launch authorization request record |
| `scope_update` | Project V | A post-replanning scope update delivery record |
| `execution_clarification` | Project V | A mid-execution clarification delivery record |
| `evidence_request` | Project V | A Project V bounded evidence request record (AD-03 model) |
| `evidence_query` | V Forge | A V Forge active evidence query record or query session (V Forge → VEDA evidence access contract) |
| `intake_outcome` | Project V | A Project V intake outcome record |
| `observation_record` | Project V / V Forge | A post-launch observation record (produced collaboratively; owned by Project V for continuity purposes) |
| `observatory_scope_change` | VEDA | An operator-to-VEDA observatory scope change request record |

For the seam-level mapping of which entity type applies to which event family,
see `ecosystem/activity-trail-integration-map.md`.

---

## Activity Trail Record Schema Contract

This section translates the field specification from `ecosystem/activity-trail-model.md`
into a schema-facing contract. This is a field-level contract, not a database
engine definition. System implementations must produce records conforming to
this contract.

---

### Identity fields

| Field | Required | Nullable | Allowed values / format | Notes |
|---|---|---|---|---|
| `activity_id` | Yes | No | Unique identifier string | Stable, non-reusable. Must be unique across all records in the activity trail. |
| `timestamp` | Yes | No | ISO 8601, UTC | When the action occurred. Must be UTC. Must not be left to local system time. |
| `ecosystem_session_id` | Yes | Yes | Identifier string or null | The session or execution context that produced the action. Null when no session context applies (e.g., system-initiated events). |

---

### Actor fields

| Field | Required | Nullable | Allowed values / format | Notes |
|---|---|---|---|---|
| `actor_type` | Yes | No | `agent` \| `operator` \| `system` | Must be one of the three canonical values. See `actor_type` enumeration above. |
| `actor_id` | Yes | No | Identifier string | The identifier of the acting entity. The value class varies by `actor_type` and will be specified in the actor identity schema spec (a companion artifact to `governance/auth-and-actor-model.md`). Must not be empty or anonymous for governed actions. |
| `actor_system` | Yes | No | `project_v` \| `veda` \| `v_forge` \| `ecosystem` \| `extension` | Must be one of the five canonical values. See `actor_system` enumeration above. |

**Note on `actor_id` value class:** The exact format and value class for `actor_id`
per `actor_type` (e.g., what kind of identifier is used for an operator vs an agent
vs a system process) is deliberately not finalized here. It is deferred to the actor
identity schema spec, which must be created as the next schema authority artifact
after this document. No implementation should finalize its `actor_id` format before
that spec exists. This is the one open schema-facing item at the ecosystem layer.

---

### Action fields

| Field | Required | Nullable | Allowed values / format | Notes |
|---|---|---|---|---|
| `action` | Yes | No | Dot-namespaced string from canonical action vocabulary | Must be a value from the Action Vocabulary enumeration above. Implementations must not invent action type values. |
| `action_class` | Yes | No | `state_change` \| `cross_system_access` \| `approval` \| `budget` \| `lifecycle` | Must be one of the five canonical values. Must be consistent with the `action` value — an implementation must not assign `cross_system_access` class to a `project.create` action. |

---

### Target fields

| Field | Required | Nullable | Allowed values / format | Notes |
|---|---|---|---|---|
| `entity_type` | Yes | No | Value from canonical `entity_type` enumeration | Must be one of the fifteen canonical values in the entity type table above. |
| `entity_id` | Yes | No | Identifier string | The identifier of the affected entity in its owning system. Must be stable and resolvable against the owning system's records. |
| `target_system` | Yes | No | `project_v` \| `veda` \| `v_forge` | The system that owns the affected entity. Must be consistent with the `entity_type` value's owning system. |

---

### Scope fields

| Field | Required | Nullable | Allowed values / format | Notes |
|---|---|---|---|---|
| `project_id` | Yes | Yes | Project identifier string or null | The project context for the action. Null only for ecosystem-level actions with no project scope (e.g., `system.startup`, `observatory.scope_change.*` at the ecosystem level). Must be present for all project-scoped actions. |
| `company_id` | Yes | Yes | Reserved / null | Reserved for future multi-tenant support. Null in all current single-tenant deployments. Must not be populated with application data. |

---

### Detail fields

| Field | Required | Nullable | Allowed values / format | Notes |
|---|---|---|---|---|
| `details` | Yes | Yes | Structured key-value object or null | Action-type-specific metadata. Must not contain secrets, credentials, or raw personal data. The minimum additional fields required per action type are defined in `ecosystem/activity-trail-integration-map.md`. Null is acceptable only for action types with no defined minimum additional fields. |
| `result_summary` | Yes | Yes | Structured object or null | Brief structured outcome summary (e.g., `{"result_count": 15}` for a query, `{"status": "approved"}` for an approval decision). Null is acceptable when no outcome summary is meaningful for the action type. |

---

### Cost fields

| Field | Required | Nullable | Allowed values / format | Notes |
|---|---|---|---|---|
| `token_cost` | Yes | Yes | Numeric (integer or decimal) or null | Token cost of the action. Null for all non-LLM actions. Must be populated for any action involving LLM inference. |
| `api_cost_cents` | Yes | Yes | Numeric (integer) or null | API cost in cents. Null for all non-API-cost actions. Must be populated for any action incurring a third-party API cost. |

---

### Schema contract constraints

The following constraints apply to all activity trail records as a whole and
are not expressible as single-field rules:

1. **`action_class` must be consistent with `action`:** The assigned `action_class`
   must match the action family the `action` value belongs to. An `approval.*` action
   must carry `action_class: approval`. A `signal.delivery` action must carry
   `action_class: cross_system_access`. Mismatches are malformed records.

2. **`target_system` must be consistent with `entity_type`:** The `target_system`
   value must match the owning system of the `entity_type` as defined in the entity
   type table above. A record with `entity_type: handoff` and `target_system: veda`
   is malformed.

3. **`activity_id` must be globally unique and non-reusable:** No two records in
   the activity trail may share the same `activity_id`. Retry events for the same
   underlying action must carry a new `activity_id` while referencing the prior
   attempt in `details` (e.g., `prior_delivery_id`).

4. **Records are immutable once written:** Activity trail records must not be
   mutated after creation. Corrections to erroneous records must be expressed as
   new records with a reference to the erroneous record, not as edits to the
   original.

5. **`details` must not carry fields named in the base required set:** Fields
   such as `actor_id`, `action`, `entity_id` must not be duplicated inside
   `details`. The base fields are authoritative. `details` carries supplementary
   context only.

---

## Cross-System Identity and Reference Pattern

This section defines the shared posture for how records in one system reference
entities owned by another system. This posture is derived from
`ecosystem/cross-system-boundaries.md`, `ecosystem/cross-system-access-governance.md`,
and `interfaces/data-boundaries.md`.

---

### Thin references only

When a system's record must reference an entity owned by another system, that
reference must be thin: a pointer to the entity by its canonical identifier in the
owning system, not a copy of the entity's content.

A thin reference consists of:
- the `entity_type` of the referenced entity (from the canonical enumeration)
- the `entity_id` of the referenced entity (as assigned by the owning system)
- provenance metadata: source system, timestamp of the referenced record, and
  freshness or trust classification where defined by the relevant interface doc

A thin reference does not include a richer or more authoritative copy of the
referenced entity's fields than what is required for the referencing record's
purpose.

**Anti-rule:** A Project V planning record that embeds a full copy of a VEDA
evidence record's content as though it were canonical planning data is not a thin
reference. It is ownership blur. The receiving system stores the pointer and the
provenance; the owning system remains the source of truth for the entity's content.

---

### Owning system IDs are authoritative

The `entity_id` assigned by the owning system to its canonical records is the
authoritative identifier for cross-system references. No other system may reassign
or reinterpret that identifier.

If a receiving system needs a local operational identifier for an entity received
from another system, the local identifier must be distinct from the owning
system's `entity_id`, and the owning system's `entity_id` must be preserved as
the reference field.

---

### Activity trail cross-system references

The activity trail records cross-system events using `entity_type` and `entity_id`
together. These two fields form the canonical cross-system entity reference in
every activity trail record. The owning system column in the entity type table
above defines which system's identifier space the `entity_id` belongs to for each
`entity_type`.

This means:
- an activity trail record with `entity_type: handoff` carries an `entity_id`
  from Project V's identifier space
- an activity trail record with `entity_type: signal_package` carries an
  `entity_id` from VEDA's identifier space
- an activity trail record with `entity_type: task` carries an `entity_id`
  from V Forge's identifier space

Implementations must not populate `entity_id` with an identifier from a different
system's space than the `entity_type`'s owning system.

---

### Provenance requirement

Any field in any system's record that references a cross-system entity must carry
provenance metadata. The minimum provenance fields are:

- `source_system` — the system that owns the referenced entity (from the
  `actor_system` / `target_system` value set)
- `record_id` — the owning system's `entity_id` for the referenced entity
- `retrieved_at` or `delivered_at` — the timestamp at which the reference data
  was received by the referencing system

Where the relevant interface doc defines additional provenance fields (such as
`freshness_classification` or `trust_classification`), those fields must also be
preserved.

---

### Caching is not authority

If a system caches cross-system data for within-session performance, the cache is
not authoritative. The cache must carry the provenance fields above. A persistent
cache that outlasts the session scope must not be treated as a second canonical
source of truth for the owning system's records.

This is an anti-drift rule from `ecosystem/cross-system-access-governance.md`
expressed as a schema constraint: no system schema authority doc may define a
local entity schema that serves as a canonical duplicate of another system's
owned entity.

---

## Retention and Compaction Constraints

This section translates the retention posture from `ecosystem/activity-trail-model.md`
into schema-facing constraints. Implementations must treat these as fixed minimums,
not as defaults to be overridden for operational convenience.

---

### Retention by action class

| `action_class` | Minimum retention | Compaction allowed | Compaction constraint |
|---|---|---|---|
| `state_change` | Indefinite | No | State-change records must not be compacted or deleted. They are the governance backbone. |
| `cross_system_access` | 90 days (detailed) | Yes, after 90 days | Compaction must preserve action count, time range, entity type, and key cost metrics. Full records must be retained for at least 90 days. |
| `approval` | Indefinite | No | Approval records must not be compacted or deleted. They are permanent governance records. |
| `budget` | 12 months | No (within 12 months) | Full records must be retained for at least 12 months. Compaction posture after 12 months is not yet defined; default to retain. |
| `lifecycle` | 30 days (detailed) | Yes, after 30 days | Compaction must preserve action count, time range, and terminal outcome. Full records must be retained for at least 30 days. |

---

### Compaction definition

Compaction means replacing a set of detailed records with a summary record that
preserves the action count, time range, and key metrics for that set. Compaction
must not:

- delete `approval` or `state_change` class records
- reduce a compacted summary to fewer fields than: action count, time range,
  `action_class`, `actor_system`, `entity_type`, and key cost metrics
- discard the `activity_id` values of the original records (they must be
  referenced in the summary or retained in an archive)

Compaction is allowed only for the two action classes where it is marked above
(`cross_system_access` and `lifecycle`), and only after the minimum retention
period has elapsed.

---

### Immutability constraint (restated for retention context)

Activity trail records, once written, must not be modified as a retention
management mechanism. Retention management must operate by archiving or compacting
records under the rules above, not by editing the fields of existing records.

---

## Usage

This document should be used as follows:

**By the Project V schema authority doc:** Reference the `entity_type` table to
confirm which entity types Project V owns. Reference the activity trail record
schema contract when specifying what activity records Project V must produce.
Reference the cross-system reference pattern when defining how Project V records
reference VEDA signal packages or V Forge execution returns. Do not redefine
any enumerated type or field contract from this document.

**By the VEDA schema authority doc:** Reference the `entity_type` table to confirm
which entity types VEDA owns. Reference the activity trail record schema when
specifying VEDA's record-production obligations for delivery and scope change
events. Reference the cross-system reference pattern when defining how VEDA records
reference Project V project identifiers for scoping purposes. Do not redefine any
enumerated type or field contract from this document.

**By the V Forge schema authority doc:** Reference the `entity_type` table to
confirm which entity types V Forge owns. Reference the activity trail record schema
when specifying V Forge's record-production obligations for execution, evidence
query, and return-to-planning events. Reference the cross-system reference pattern
when defining how V Forge records reference handoff records from Project V and
signal packages from VEDA. Do not redefine any enumerated type or field contract
from this document.

**By activity trail implementation work:** Use the activity trail record schema
contract as the field-level specification for the activity trail database schema.
Use the canonical enumerated types as the value sets for enumerated columns or
fields. Use the retention and compaction constraints as the governing rules for
data lifecycle management. Resolve any gap between this contract and an
implementation requirement by surfacing it as a canon-change request, not by
deviating silently.

**For new action type or entity type additions:** Any addition to the action
vocabulary or entity type vocabulary must be made to `ecosystem/activity-trail-model.md`
first, then reflected in the enumeration sections of this document. Additions may
not appear in activity trail records before they are canonical in both documents.

---

## Related Docs

- `ecosystem/activity-trail-model.md` *(Tier 1 authority — canonical action and entity vocabulary, field definitions, retention posture)*
- `ecosystem/activity-trail-integration-map.md` *(seam-to-action-type mapping, minimum additional fields per event family)*
- `ecosystem/cross-system-boundaries.md` *(system ownership boundaries)*
- `ecosystem/cross-system-access-governance.md` *(access governance, six access patterns, anti-drift rules)*
- `interfaces/data-boundaries.md` *(canonical data ownership map, cross-system reference posture per system)*
- `governance/auth-and-actor-model.md` *(actor classes, identity principle, minimum actor semantics)*
- `governance/actor-identity-schema-spec.md` *(actor_id value-class specification per actor_type — to be created)*
- `project-v/project-v-schema-authority.md` *(Project V entity schemas — to be created)*
- `veda/veda-schema-authority.md` *(VEDA entity schemas — to be created)*
- `v-forge/v-forge-schema-authority.md` *(V Forge entity schemas — to be created)*
