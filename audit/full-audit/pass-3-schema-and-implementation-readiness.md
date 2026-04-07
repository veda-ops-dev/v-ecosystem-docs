# Pass 3 — Schema and Implementation Readiness

## Purpose

This pass determines what schema authority and persistence-support work is still
required to make the current merged doctrine, interfaces, workflows, and activity-trail
canon implementation-ready.

The governance and interface layers have been confirmed stable by Passes 1 and 2.
The cleanup actions identified in those passes (stale forward-reference notes,
`data-boundaries.md` registry, evidence access contract activity trail alignment)
have been applied. This pass treats those as resolved baseline.

This pass does not reopen governance or seam architecture findings. It reads the
current docs for what they explicitly provide and what they leave unspecified at
the schema level.

---

## Scope of This Pass

This pass covers:

- what canonical entity families are already derivable from current docs
- which entities belong to which system for schema ownership purposes
- which records need durable identity, state, and history support
- whether approval, decision continuity, invalidation/supersedence, and
  activity-trail requirements are sharp enough to derive persistent schemas
- whether actor identity fields are schema-ready or still underspecified
- whether cross-system reference rules are explicit enough for implementation
- whether stub interfaces can be schema-backed without full contract upgrades
- what schema-facing artifacts are still required

---

## Files Reviewed

**Audit control:**
- `audit/full-audit/README.md`
- `audit/full-audit/master-plan.md`
- `audit/full-audit/pass-1-governance-and-boundaries.md`
- `audit/full-audit/pass-2-interfaces-and-workflows.md`

**Governance / ecosystem / activity canon:**
- `ecosystem/cross-system-boundaries.md`
- `ecosystem/cross-system-access-governance.md`
- `ecosystem/activity-trail-model.md`
- `ecosystem/activity-trail-integration-map.md`
- `governance/approval-and-escalation-model.md`
- `governance/approval-mechanics-seam-model.md`
- `governance/decision-continuity-doctrine.md`
- `governance/invalidation-and-supersedence-doctrine.md`
- `governance/allowed-agent-actions-matrix.md`
- `governance/auth-and-actor-model.md`

**Interfaces and workflows (as reviewed in Pass 2, treated as current baseline):**
- All eleven interface docs in `interfaces/`
- All five workflow docs in `workflows/`

---

## Executive Verdict

The canonical entity family is substantially derivable from current docs. Three
system-owned entity families (Project V, VEDA, V Forge) and one ecosystem-layer
entity family (activity trail) can be identified with confidence from the canonical
data ownership map and the activity trail model's entity type vocabulary. The
ownership assignment for every named entity type is clear and uncontested.

The primary schema-phase gaps are seven missing artifacts: the approval record
entity schema, the actor identity value-space specification, the decision record
entity schema, system-specific schema authority docs for each of the three systems,
and an ecosystem schema spine document. There are also four partial areas: actor
identity value-space underspecification, portfolio-scoped access schema mechanics,
stub interface entity contracts, and one entry-vocabulary gap in the activity trail
model (the `evidence_query` entity type is used in the integration map's Section 4b
but is absent from the model's entity type vocabulary).

No schema work is blocked by unresolved architectural decisions. The governance
layer, seam layer, and activity trail canon are all stable enough to begin schema
authority work. The recommended sequence is: ecosystem-layer schemas first
(activity trail record, actor identity), then Project V schemas (the most
complex system), then VEDA and V Forge schemas in parallel.

---

## Complete

The following are classified as **Complete** at the schema-readiness level —
the existing docs provide sufficient specification to derive or assign schema
authority without additional artifact creation.

---

### C1. Canonical Entity Ownership Assignment — All Three Systems

**Finding: Complete.**

The canonical data ownership map in `interfaces/data-boundaries.md` (Canonical
Data Ownership Map section) provides a directly usable entity ownership assignment
for all three systems. It names each owned record category explicitly:

**Project V owns canonically:**
project records, project metadata, planning decision records, ADRs within project
scope, readiness evaluation records, handoff records, intake outcome records,
orchestration state and lifecycle state, BYDA audit run records and audit gap
records, planning-side traceability records, multi-project portfolio state.

**VEDA owns canonically:**
observatory event records and observation history, SERP data, keyword intelligence,
ranking records, GA4 performance observation records, Search Console records,
YouTube observatory records, source capture records and source items, evidence
provenance records, provider integration configuration and ingest pipeline records,
signal packages produced from observatory records.

**V Forge owns canonically:**
execution records and execution lifecycle state, content graph records (pages,
topics, entities, internal links, archetypes, schema usage), execution intelligence
records, bounded execution findings records, maintenance execution records,
execution-side reporting records.

This ownership map is internally consistent and supported by `cross-system-boundaries.md`
and `cross-system-access-governance.md`. No contradictions exist across the three
boundary documents. The assignment can be used directly as the schema ownership table
for the three system schema authority docs.

---

### C2. Activity Trail Entity Type Vocabulary — Substantially Canonical

**Finding: Complete for governance-layer derivation; one entry-vocabulary gap noted below.**

The activity trail model defines a governed entity type vocabulary covering fourteen
named entity types. Each is explicitly mapped to the action types and seam events
that produce records referencing it. The full list:

**Original entity types:** `project`, `evidence`, `task`, `handoff`, `agent`

**Added entity types (from integration map):** `signal_package`, `execution_return`,
`launch_authorization`, `scope_update`, `execution_clarification`, `evidence_request`,
`intake_outcome`, `observation_record`, `observatory_scope_change`

Integration map Section 8 confirms all named entity type extensions have been
applied to the model. However, integration map Section 4b uses
`entity_type: evidence_query` for V Forge active evidence query records, and
`evidence_query` is **not listed** in the model's entity type vocabulary. This is
a concrete omission: the entity type is in use in the integration map without a
backing entry in the model.

This gap is addressed as a concrete finding in the Suggestions section and in the
Step 1 action of the Proposed Schema Authority Sequence. It does not affect the
schema-derivation completeness of the other fourteen entity types.

**Schema-phase implication:** The activity trail record itself needs a formal
database schema (table or collection definition). The required fields are fully
specified in the activity trail model (identity fields, actor fields, action fields,
target fields, scope fields, detail fields, cost fields). The action type vocabulary
is canonical. The entity type vocabulary is canonical for all fourteen listed types;
`evidence_query` must be added before the evidence query record schema is finalized.

---

### C3. Approval Mechanics — Semantics Fully Specified

**Finding: Complete (for semantic derivation; see P1 for the record entity gap).**

The approval and escalation model (Tier 1) and the approval mechanics seam model
(Tier 2) together provide a schema-sufficient semantic specification for approval
events:

- the four approval classes (A, B, C, D) are defined with examples
- the approval state vocabulary (not required, pending, approved, rejected, expired,
  revoked, escalated) is explicit
- the four decision outcomes (approved, rejected, escalated, expired) are the
  complete set — no other outcomes are valid
- the five transition classes (handoff activation, return-to-planning review, launch
  authorization, supersedence approval, intake outcome review) are each named with
  their initiating system, pending state, and activity trail action types
- the canonical pending-state vocabulary (`awaiting_approval`, `awaiting_review`,
  `awaiting_authorization`, `escalated_for_review`) is defined and stable

The activity trail integration map (Sections 5a–5e) provides the minimum additional
fields for each approval event class, including `approval_class`, `decision`, and
the specific entity type/entity id pattern for each transition class.

**This is sufficient to derive the approval *event* schema** (activity trail records
for `approval.request`, `approval.decide`, `approval.escalate`). See P1 below for
why the approval *record entity* schema is a separate, still-missing artifact.

---

### C4. Cross-System Reference Rules — Derivable

**Finding: Complete.**

The "What Each System May Reference Without Owning" section in `data-boundaries.md`
defines cross-system reference posture precisely enough for schema design:

- Project V may reference: bounded VEDA signal packages received through the
  signal interface, bounded execution findings received through return-to-planning,
  thin external linkage records for planning-side traceability.
- VEDA may reference: project identifiers from Project V to scope observatory targets,
  configuration direction from Project V or operators.
- V Forge may reference: bounded VEDA signal packages received through the signal
  interface for execution intelligence, handoff package content from Project V.

The constraint that cross-system references must be "thin" and must not store "richer
or more authoritative copies" of another system's canonical data is schema-applicable:
it means cross-system foreign keys should point to the owning system's canonical
record, and local derivative copies must carry provenance metadata and not be treated
as canonical.

The six-pattern access model in `cross-system-access-governance.md` maps directly
to the interface set, providing the complete join-point specification for cross-system
references.

---

### C5. Activity Trail Record Schema — Field Contract Fully Specified

**Finding: Complete (field contract derivable; database schema artifact not yet written).**

The activity trail model specifies all required fields by name, type semantics,
and cardinality with sufficient precision to write the database schema. The field
contract is schema-ready for all fields except `actor_id`, where the value class
per actor type is deferred to the schema phase (see P2). The `evidence_query`
entity type omission noted in C2 applies here as well: that entry must be added
to the model's entity type vocabulary before evidence query records are formally
schema-backed, though it does not block the rest of the activity trail schema.

- `activity_id` (unique identifier)
- `timestamp` (UTC, ISO 8601)
- `ecosystem_session_id` (nullable)
- `actor_type` (one of: `agent`, `operator`, `system`)
- `actor_id` (actor identifier — see P2 for value-space gap)
- `actor_system` (one of: `project_v`, `veda`, `v_forge`, `ecosystem`, `extension`)
- `action` (dot-namespaced action type from canonical vocabulary)
- `action_class` (one of: `state_change`, `cross_system_access`, `approval`,
  `budget`, `lifecycle`)
- `entity_type` (from canonical entity type vocabulary)
- `entity_id` (identifier of affected entity)
- `target_system` (one of: `project_v`, `veda`, `v_forge`)
- `project_id` (nullable for ecosystem-level actions)
- `company_id` (reserved, currently null)
- `details` (structured key-value metadata)
- `result_summary` (structured outcome summary)
- `token_cost` (nullable)
- `api_cost_cents` (nullable)

Retention posture is also specified by action class. The field contract is complete
enough to write the database schema directly. The main open item is `actor_id`
value-space precision (P2 below).

---

### C6. Decision State Model — Lifecycle Derivable

**Finding: Complete (lifecycle states are named; see M3 for the decision record schema contract).**

`decision-continuity-doctrine.md` establishes a five-state lifecycle for decisions
that is schema-derivable:

- `proposed` — a candidate decision under consideration; not yet continuity-binding
- `approved` (governing) — has approval posture, is active and binding
- `rejected` — a rejected decision outcome; must be preserved for continuity
- `superseded` — replaced by a new governing decision; history preserved
- `invalidated` — basis gone; history preserved; no longer binding

These are the required states on a decision record entity. The doctrine also
establishes the persistence obligations: "Rejection records must be preserved in
a form accessible to future planning sessions. Ephemeral conversation-level notes
do not satisfy rejection continuity." This means the schema must support all five
states as queryable, not just the active state.

The invalidation and supersedence doctrine further specifies that both invalidated
and superseded records must be marked with date, reason, and (for supersedence)
a reference to the superseding decision. These become schema fields.

---

### C7. Handoff Entity — Field Contract Derivable

**Finding: Complete.**

The handoff interface (`project-v-to-v-forge-handoff-interface.md`) defines the
required semantic fields of a handoff package with enough precision to derive the
schema for a `handoff` entity:

- stable handoff/delivery identity
- originating planning context or source entity reference
- approved execution scope (bounded description)
- target system (V Forge, explicit)
- execution constraints and boundaries
- readiness basis
- evidence references or supporting planning basis
- expected outcomes or intended execution objective
- conditions that should trigger return-to-planning
- activation timestamp
- package revision posture (original vs revision; prior handoff identity reference)

The activity trail integration map Section 2 adds: `source_planning_entity_ref`,
`execution_scope_id`, `package_version_posture`, `receipt_confirmed_at`.

The approval gate integration adds: `approval_class`, `readiness_basis_ref`.

Together these provide sufficient field coverage to write a `handoff` schema entity
spec. The `entity_type: handoff` is canonical in the activity trail vocabulary and
maps to this record.

---

### C8. Signal Package Entity — Field Contract Derivable

**Finding: Complete.**

The VEDA → Project V signal interface defines the required semantic fields of a
signal delivery package precisely enough for schema derivation:

- package/delivery identity (stable, for re-delivery de-duplication)
- planning context reference (which project or planning scope)
- signal/evidence scope (class or domain)
- observation/capture timestamps
- delivery timestamp
- freshness classification
- trust and provenance metadata
- planning concern or question addressed
- bounded evidence references or included evidence elements
- delivery trigger context (`proactive` vs `request_response`; originating request
  identity if request-response)

The integration map Section 1 adds: `delivery_trigger_type`, `freshness_classification`,
`trust_classification`. The `entity_type: signal_package` is canonical.

The VEDA → V Forge startup signal interface adds: `originating_handoff_ref`,
`signal_scope` — making this entity appear in two delivery contexts with the same
entity type, distinguished by the action type (`signal.delivery` vs
`signal.delivery.startup`) and the presence of `originating_handoff_ref`.

---

### C9. Intake Outcome Entity — Field Contract Derivable

**Finding: Complete.**

The project intake workflow (Stage 5 and Stage 7) and integration map Section 9
define the intake outcome record precisely:

- intake item identity (stable `entity_id`)
- outcome type: one of `project.create`, `intake.defer`, `intake.hold`,
  `intake.reject`, `intake.close`
- signal basis reference (`signal_basis_ref`)
- for defer: `deferral_reason`, `re_evaluation_conditions`
- for hold: `hold_reason`, `triggering_conditions_for_reconsideration`
- for reject: `rejection_reason`, `rejection_scope` (rejection continuity required)
- for close (Stage 7): `closure_reason`, `degraded_condition`

The decision continuity doctrine makes the retention requirement explicit: rejected
items must be "preserved in a form accessible to future planning sessions." The
schema must therefore retain all terminal outcome records, not just active projects.

---

### C10. Observation Record Entity — Field Contract Derivable

**Finding: Complete.**

Integration map Section 10 and the post-launch observation workflow define the
observation record entity:

- observation cycle identity (stable, linking classify/assess/cycle records for
  a single cycle)
- for `observation.classify`: `signal_maturity_assessment` (mature | immature),
  `classification_outcome`, `signal_basis_ref`, `producing_system`
- for `observation.assess`: `threshold_determination`,
  `routed_outcome` (continue_observation | maintenance | return_to_planning | escalation),
  `assessment_basis_summary`
- for `observation.cycle`: `cycle_outcome`, `cycle_number`, `next_cycle_trigger`

The workflow specifies that "observation cycle events must be durably recorded" and
that classification history must be accessible to later reconsideration sessions.
This is a clear persistence requirement.

---

## Partial

The following have substantial doc support but require a schema-phase artifact
or a sharpening step before the schema can be finalized.

---

### P1. Approval Record Entity Schema — Semantics Defined, Record Shape Missing

**Classification: Partial.**

The approval governance layer (Tier 1 and Tier 2 docs together) defines what
approval means, what requests must contain, what outcomes are possible, and what
activity trail events must be produced. The Reviewability Principle in
`approval-and-escalation-model.md` states the ecosystem should be able to
determine after the fact:

> "what action or transition was approved, who approved it, what scope the approval
> covered, what conditions or limits applied, whether the approval is still active,
> expired, revoked, or superseded"

This is a semantic contract for a queryable, persistent approval record entity.
But the semantic contract has not been translated into a schema entity spec.

**The activity trail records approval *events*** (`approval.request`,
`approval.decide`, `approval.escalate`). These are immutable log records.
They are not the same as a queryable *current approval state* record — which must
answer "what is the current approval state for this handoff?" or "was this handoff
activated under a still-valid approval?" without replaying the full activity log.

The gap: the approval record entity needs fields including at minimum:
- stable approval record identity
- entity reference (what was approved — `entity_type` + `entity_id`)
- approval class (A, B, C, D)
- initiating system
- approving actor identity
- scope (bounded description of what the approval covers)
- conditions or limits
- current state (pending | approved | rejected | expired | revoked | superseded)
- activation timestamp
- expiry or revocation reference (if applicable)
- supersedence reference (if applicable)

None of these are explicitly specified as a schema entity. The semantic content
is present but not formalized.

**Impact:** Needed for Project V schema authority, since Project V owns approval
records for planning-side transitions. Needed before the activity trail schema
can reference approval record identity as a foreign key. Needed before governance
replay can query "was this action performed under a valid approval at the time?"

**Suggestion:** Create an `approval_record` schema entity spec as the first
artifact in the Project V schema authority phase. The semantic contents are in
`approval-and-escalation-model.md`'s Reviewability Principle and Approval Request
Principle sections. They need schema-level translation only, not new design.

---

### P2. Actor Identity Value-Space — Doctrine Clear, Schema Underspecified

**Classification: Partial.**

`auth-and-actor-model.md` defines four actor classes (Human Operator, Agent,
System Process, External Actor) and states the Minimum Actor Semantics: what actor
class, system context, governed role, action mode, and authority posture must be
determinable. The activity trail requires three actor fields: `actor_type`,
`actor_id`, `actor_system`.

What is not specified at schema level:

**`actor_type`:** The model names three values (`agent`, `operator`, `system`)
in the activity trail model field definition. External Actor is a fourth class but
is not listed as a valid `actor_type` value. This needs to be resolved — either
`external` is added to the `actor_type` value set or External Actor events are
excluded from the activity trail. The three-value set appears to be the intended
one, but it is not definitively stated.

**`actor_id`:** No format or value-space is specified. For an operator, is this
a user record ID? A session token? An email address? For an agent, is this an
agent instance ID? An agent type name? An LLM session hash? This is implementation-
specific by design, but the activity trail schema cannot be finalized as a
queryable record set until `actor_id` has at least a value-class contract (what
kind of thing it is per actor type).

**`actor_system`:** Five values are listed in the activity trail model
(`project_v`, `veda`, `v_forge`, `ecosystem`, `extension`). This is the most
specified of the three fields. It is schema-ready as a value set.

**Impact:** The activity trail record schema can be written and mostly finalized
now. The `actor_id` underspecification becomes a concrete blocker when audit
queries need to filter activity by a specific operator or agent instance, and when
approval records need to identify the approving human actor by a durable reference.

**Suggestion:** Define an actor identity schema spec as a companion to
`auth-and-actor-model.md`. At minimum: confirm the `actor_type` value set,
specify the value-class for `actor_id` per actor type (e.g., "for `operator`:
a stable user record ID; for `agent`: a stable agent session or agent-type
identifier"), and confirm whether External Actor is in or out of the trail
record scope.

---

### P3. Portfolio-Scoped Access Authorization — Access Model Defined, Schema Mechanics Soft

**Classification: Partial.**

`cross-system-access-governance.md` explicitly permits portfolio-scoped access
for Project V planning market evaluation, requiring that portfolio-scoped access
"be explicitly authorized by the requesting context" and "logged." The evidence
request interface (`project-v-to-veda-evidence-request-interface.md`) is the
primary path through which this access would occur.

At the schema level, neither the `evidence_request` entity spec nor the signal
package spec currently defines a `scope_type` field (project | portfolio) or a
`portfolio_authorization_ref` field. Without these, the activity trail record for
a portfolio-scoped evidence request cannot distinguish itself from a project-scoped
one, and the authorization requirement ("explicitly authorized by the requesting
context") cannot be verified from the record.

**Impact:** Manageable for initial schema work since the evidence request interface
is a stub. Becomes a concrete blocker when the stub is upgraded to a full contract,
because the schema must support the access governance logging requirement for
portfolio-scoped interactions.

**Suggestion:** When the `project-v-to-veda-evidence-request-interface.md` stub
is upgraded to a full contract, add `scope_type` (project | portfolio) and
`portfolio_authorization_ref` fields to the `evidence_request` entity schema.
Note that `portfolio_authorization_ref` must reference whatever authorization
mechanism is established in the actor identity spec (P2), so these two artifacts
should be designed in coordination.

---

### P4. Stub Interface Entity Schemas — Action Types Canonical, Entity Contracts Not Yet Final

**Classification: Partial.**

The three stub interfaces (execution clarification, handoff recall, scope update)
have canonical activity trail action types and entity types, defined in integration
map Sections 6a, 6b, and 6c. The action types (`execution.clarification`,
`handoff.recall`, `execution.scope_update`) and entity types (`execution_clarification`,
`handoff`, `scope_update`) are usable for schema planning purposes.

However, the stub interface docs themselves do not define field-level schemas for
the entities they govern. The integration map section for each stub carries the
note "Stub-level posture. Exact fields subject to full contract upgrade." This is
correct and by design.

**What this means for schema work:**
- The entity types are usable as references in the activity trail schema
- The minimum additional fields shown in the integration map provide a working
  set for initial schema design
- Finalizing the entity schemas for these three entities requires the stubs to be
  upgraded to full contracts first

**Impact:** These are not blockers for the activity trail schema or for Project V /
VEDA / V Forge primary entity schemas. They are stubs-first dependencies: the
primary schemas can proceed, and the stub entities get their schemas when the
contracts are upgraded.

**Suggestion:** Do not upgrade stubs to full contracts before the primary entity
schemas are defined. The primary schemas will establish the cross-reference patterns
(e.g., `execution_clarification` references a `handoff` record identity) that the
stub schemas will need to be consistent with.

---

## Missing

The following required schema-facing artifacts genuinely do not exist on the current
merged baseline. Each is a distinct artifact that must be created.

---

### M1. Approval Record Entity Schema Contract

**Classification: Missing.**

Identified as a partial in Pass 1 and confirmed here. The semantic content is
derivable from current docs (see P1 above). The artifact itself — a spec that
defines the fields, types, constraints, and lifecycle of a persisted approval
record entity — does not exist.

This is the highest-priority missing schema artifact because it is a dependency
for both the Project V schema authority doc and the activity trail schema
finalization.

**Artifact to create:** `approval_record` entity schema spec. Recommend placing
this in a Project V schema authority doc or a shared governance schema doc,
since Project V owns approval records for planning-side transitions.

---

### M2. Actor Identity Value-Space Specification

**Classification: Missing.**

Identified as a partial in Pass 1 and confirmed here. The doctrine exists in
`auth-and-actor-model.md`. The schema-level artifact — specifying `actor_type`
value set (including or excluding `external`), `actor_id` value class per actor
type, and `actor_system` value set confirmation — does not exist.

**Artifact to create:** Actor identity schema spec, as a companion document to
`auth-and-actor-model.md` or as part of an ecosystem schema spine document. This
artifact is a prerequisite for finalizing the activity trail record schema and the
approval record entity schema.

---

### M3. Decision Record Entity Schema Contract

**Classification: Missing.**

The decision state lifecycle is derivable from current governance docs (see C6),
and the persistence obligations are stated explicitly in both
`decision-continuity-doctrine.md` and `invalidation-and-supersedence-doctrine.md`.
But the schema entity itself — defining stable identity, lifecycle state fields,
approval posture reference, scope, supersedence/invalidation linking fields —
does not exist. The `decision_record` entity type appears in integration map
Section 5d (supersedence approval events) without a backing schema contract.

The governance-facing content that must be captured is derivable from current
docs and has not been assembled into a spec. Required fields include at minimum:

- stable decision identity
- decision text or summary
- decision class (corresponding to the workflow stage and action class that produced it)
- owning system
- scope (project, portfolio, or ecosystem-level)
- approval posture satisfied (reference to approval record)
- lifecycle state (proposed | approved | rejected | superseded | invalidated)
- created timestamp
- approved timestamp (if applicable)
- superseded-by reference (if superseded)
- invalidated-by reference and reason (if invalidated)
- cross-system consequences flag (whether supersedence/invalidation has cross-system
  effects, per the invalidation doctrine's authority rule)

**Impact:** Project V schema authority depends on this, since Project V owns
planning decision records. The decision record entity is the anchor for
decision continuity queries ("what governing decisions apply to this project?"
"what was the basis for this handoff?"). It is also referenced by the supersedence
approval events in integration map Section 5d (which use `entity_type: decision_record`).

**Artifact to create:** `decision_record` entity schema spec, as part of
Project V schema authority (alongside M1). The semantic contents are distributed
across `decision-continuity-doctrine.md` and `invalidation-and-supersedence-doctrine.md`
and need to be consolidated into a schema entity definition. No new design is
required — this is a formalization task.

---

### M4. Project V Schema Authority Document

**Classification: Missing.**

There is no schema authority document for Project V. Such a document would:

- enumerate the canonical entities owned by Project V (from the data ownership map)
- define or reference the schema for each entity: `project`, `handoff`,
  `intake_outcome`, `decision_record`, `approval_record`, plus planning-side
  traceability records and readiness evaluation records
- specify lifecycle states, required fields, and identity requirements for each
- specify how Project V entities reference cross-system entities (VEDA signal
  packages by reference, V Forge execution records by reference)
- establish the schema authority boundary: what Project V may store and what
  it may not duplicate

Project V's schema is the most complex of the three systems because it owns the
approval record, the decision record, the handoff record, and the intake outcome
record — all of which carry lifecycle state, history requirements, and
cross-system reference obligations.

**Artifact to create:** `project-v-schema-authority.md` or equivalent, in
a schema authority folder or the `project-v/` folder.

---

### M5. VEDA Schema Authority Document

**Classification: Missing.**

VEDA's schema authority domain is large (observatory records, signal packages,
evidence records, source capture records, provider configuration) but internally
cleaner than Project V's because VEDA's records are predominantly append-only
or event-log in nature — they accumulate rather than mutate through complex
lifecycle states.

The primary schema concerns for VEDA:

- `evidence` record schema: what fields must every evidence record carry? The
  evidence access contract specifies required response fields (`evidence_id`,
  `gathered_at`, `source_provider`, `source_url`, `freshness_status`,
  `freshness_window_end`, `trust_classification`) — these become schema fields.
- `signal_package` entity schema: what persists vs. what is ephemeral per delivery?
- Observatory event records: what is the schema for VEDA's internal event log?
- Source capture and source item records: not yet schema-specified.
- Evidence provenance records: referenced in ownership map but not schema-specified.

**Artifact to create:** `veda-schema-authority.md` or equivalent.

---

### M6. V Forge Schema Authority Document

**Classification: Missing.**

V Forge's canonical entity family is also well-defined in ownership terms. The
primary schema concerns:

- `task` entity schema: the activity trail model defines `task.create`,
  `task.complete`, `task.fail`, etc. but no task field contract exists.
- Content graph entity schemas: `pages`, `topics`, `entities`, `internal links`,
  `archetypes`, `schema usage` are named in the ownership map but not yet
  schema-specified. The content graph is the most V Forge-specific schema concern.
- Execution record and execution lifecycle state schema: references in the ownership
  map; not yet schema-specified.
- Execution intelligence records: `execution_return` entity is partially specified
  via the integration map (Section 3 minimum fields); not fully schema-specified.
- Execution findings and maintenance records: named in ownership map; not schema-specified.

The "bounded execution-side research" carve-out noted in Pass 1 will need schema-level
expression when V Forge's execution intelligence records are designed — specifically,
what distinguishes an execution-intelligence record from a VEDA observatory record
that V Forge is not allowed to hold.

**Artifact to create:** `v-forge-schema-authority.md` or equivalent.

---

### M7. Ecosystem Schema Spine Document

**Classification: Missing.**

An ecosystem-level schema spine document would:

- define the activity trail record schema (from the complete field specification)
- confirm the entity type vocabulary as an enumerated type
- confirm the action type vocabulary as an enumerated type
- define cross-system identity reference patterns (how Project V records reference
  VEDA records, how activity trail records reference all three systems' entities)
- specify the retention and compaction rules as schema constraints
- establish the schema authority boundary for the ecosystem layer vs. system layers

This document is the prerequisite integration layer that the three system schema
authority docs will reference. Without it, each system schema authority doc will
make independent decisions about identity formats and reference patterns, creating
inconsistencies that are hard to fix later.

**Artifact to create:** `ecosystem-schema-spine.md` or equivalent, in the
`ecosystem/` folder. This should be created before or alongside M1–M3, as it
provides the shared schema context those artifacts depend on.

---

## Blocked

**No blocked work identified.**

All schema-phase work identified in this pass can proceed without resolving
any open architectural decisions. The governance layer is stable (Pass 1), the
seam layer is stable (Pass 2), the stale documentation issues were corrected,
and no cross-system identity or reference decision is contested.

The schema-phase artifacts are sequentially dependent (M7 before M4–M6, M1–M3
alongside M4) but none is blocked by a prerequisite decision that has not been made.

---

## Key Gap Analysis

### Gap 1: Three schema authority docs — none yet exist

This is the primary gap. The entity ownership map is complete. The canonical
entity types are named. The field contracts for several key entities (handoff,
signal package, intake outcome, observation record) are partially derivable from
interface and integration map docs. But the system-specific schema authority docs
that would consolidate this into a coherent per-system schema have not been created.
Without them, implementation teams cannot derive the database schema without
re-reading all the governance, interface, and workflow docs themselves.

### Gap 2: Approval record and decision record entity schemas are missing

These two entities are the most governance-critical persistent records in the
ecosystem. The approval record is what makes governance verifiable beyond the
activity trail log (you can query "is this approval currently valid?" rather than
replaying all events). The decision record is what makes decision continuity
queryable ("what governing decisions constrain this project?"). Both are well-defined
semantically. Neither has been translated into a schema entity spec.

### Gap 3: Actor identity value-space gap will surface at activity trail finalization

The `actor_id` field on activity trail records has no specified value class per
actor type. This is deferred by design in `auth-and-actor-model.md`, but the
deferral must resolve before the activity trail schema can be finalized as a
queryable record set. The gap is small but concrete.

### Gap 4: Content graph entity schemas are the largest V Forge schema gap

V Forge's execution truth domain is well-defined in ownership terms. But the
content graph — pages, topics, entities, internal links, archetypes, schema usage
— is the largest block of schema work not yet touched by any doc in the current
set. The content graph is V Forge's most unique data domain, and its schema design
has no current foundation doc beyond the ownership claim in `cross-system-boundaries.md`.

---

## Suggestions and Feedback

**On the overall state:** The doc set has done more schema-preparation work than
typical governance repos reach. The canonical data ownership map, the entity type
vocabulary, the action type vocabulary, the field contracts in interface docs, and
the integration map minimum field specifications together constitute a significant
amount of schema-derivation material. The translation from this material to formal
schema entities is the remaining step — it is a focused task, not a design task.

**On sequencing:** The recommended sequence (ecosystem spine first, then Project V,
then VEDA and V Forge) is driven by dependency, not importance. Project V is first
among the system schemas because it owns the approval record and decision record —
the two entities that cross-cut all workflows. If VEDA or V Forge schemas were
written first, they would need to reference approval records and decision records
that don't yet have schema definitions, creating placeholder references that need
retroactive updating.

**On the content graph:** The V Forge content graph schema is probably the largest
single schema design task in the ecosystem. It is also the most internally V Forge-
specific — the content graph entities don't have cross-system reference obligations
the way handoffs and approvals do. This means it can be designed with somewhat more
flexibility, but it also means there is no existing spec to derive from other than
the ownership claim. It warrants its own design pass when V Forge schema authority
work begins.

**On the decision record vs. ADR:** The governance docs reference "ADRs within
project scope" as a Project V canonical record. Whether a `decision_record` schema
entity and an `ADR` entity are the same thing or two different representations of
the same governance artifact is a question the Project V schema authority doc will
need to resolve explicitly. The current docs treat them as overlapping concepts
without disambiguating them at the schema level. This is not a gap in the current
docs (it's appropriately deferred), but it is a schema-phase decision that should
be made early.

**On the `evidence_query` entity type:** Integration map Section 4b uses
`entity_type: evidence_query` for V Forge active evidence queries. But `evidence_query`
is not listed in the activity trail model's entity type vocabulary. It appears to
have been added in the integration map without being backported to the model. This
should be confirmed and, if it was an oversight, added to the model's entity type
vocabulary before the activity trail schema is finalized.

---

## Recommended Next Actions

### Step 1 — Ecosystem schema spine (prerequisite for everything else)

Create `ecosystem-schema-spine.md`. This document should:
- formalize the activity trail record schema (use the field specification from
  `activity-trail-model.md` as the direct input)
- confirm the entity type and action type vocabularies as enumerated schema types
- define cross-system identity reference patterns (foreign key conventions)
- specify retention and compaction rules as schema constraints
- confirm or correct the `evidence_query` entity type status (see Suggestions)

This document will be the shared reference for M4–M6. It should be written before
the system schema authority docs are started.

### Step 2 — Resolve actor identity value-space (in parallel with Step 1 or immediately after)

Create the actor identity schema spec as a companion to `auth-and-actor-model.md`.
At minimum: confirm `actor_type` value set, specify `actor_id` value class per
actor type, confirm whether External Actor produces activity trail records. This
is a small document — it is resolving a deferred implementation question, not
designing new architecture.

### Step 3 — Project V schema authority doc (after Steps 1–2)

Create `project-v-schema-authority.md`. This document is the most complex of the
three system docs and should be written first because it defines the approval
record and decision record entities that VEDA and V Forge schemas will reference.
It should include:
- the `approval_record` entity schema (M1 / P1)
- the `decision_record` entity schema (M3)
- the `handoff` entity schema (derivable from interface doc)
- the `intake_outcome` entity schema (derivable from integration map)
- readiness evaluation record schema
- project record and project metadata schema
- cross-system reference posture (what Project V references by ID vs. stores locally)

### Step 4 — VEDA and V Forge schema authority docs (after Step 3, can be parallel)

Create `veda-schema-authority.md` and `v-forge-schema-authority.md`. These depend
on the ecosystem spine (Step 1) and the Project V schemas (Step 3) for cross-system
reference consistency. VEDA and V Forge do not depend on each other's schemas, so
they can be written in parallel.

VEDA priority entities: `evidence` record, `signal_package`, observatory event
records, source capture records.

V Forge priority entities: `task`, execution record, content graph entities (pages,
topics, internal links, archetypes, schema usage), `execution_return` (partially
specified), execution intelligence records.

### Step 5 — Stub interface contracts (after Steps 3–4)

Upgrade the three stub interfaces to full contracts once the primary entity schemas
(particularly `handoff` and the Project V decision record) are defined. The stub
entity schemas (`execution_clarification`, `scope_update`) will need to reference
handoff records by stable identity. Attempting this before the handoff entity schema
is finalized would require placeholder references.

---

## Proposed Schema Authority Sequence

The following sequence reflects dependencies and minimizes rework:

```
1. ecosystem-schema-spine.md
   └── activity trail record schema (field contract → database schema)
   └── entity type vocabulary (enumerated)
   └── action type vocabulary (enumerated)
   └── cross-system reference pattern (foreign key conventions)
   └── confirm / add: evidence_query entity type in model

2. actor-identity-schema-spec.md (companion to auth-and-actor-model.md)
   └── actor_type value set
   └── actor_id value class per actor type
   └── External Actor trail record scope decision

3. project-v-schema-authority.md
   └── approval_record entity schema       ← M1 / P1
   └── decision_record entity schema       ← M3
   └── handoff entity schema               ← C7
   └── intake_outcome entity schema        ← C9
   └── project entity schema
   └── readiness_evaluation entity schema
   └── planning_traceability reference posture

4a. veda-schema-authority.md              (parallel with 4b)
    └── evidence record schema
    └── signal_package entity schema
    └── observatory event record schema
    └── source capture / source item schemas
    └── evidence provenance record schema

4b. v-forge-schema-authority.md           (parallel with 4a)
    └── task entity schema
    └── execution record and lifecycle schema
    └── content graph entity schemas
           (page, topic, entity, internal_link, archetype, schema_usage)
    └── execution_intelligence record schema
    └── execution_return entity schema (complete)
    └── bounded execution-side research schema boundary

5. Stub interface contract upgrades         (after Steps 3–4)
   └── project-v-to-v-forge-execution-clarification-interface.md
   └── project-v-handoff-recall-interface.md
   └── project-v-to-v-forge-scope-update-interface.md
   + evidence request interface (scope_type / portfolio_authorization_ref fields)
```

---

## Implementation-Readiness Verdict

**The governance and seam layers are implementation-ready.** Pass 1 confirmed
governance stability. Pass 2 confirmed interface and workflow completeness.
The cleanup actions from those passes have been applied. This is a stable
foundation.

**The activity trail event layer is implementation-ready.** The field contract
is complete, the action type vocabulary is canonical, the entity type vocabulary
is canonical, and the integration map provides minimum additional fields per
seam event. The only open item is `actor_id` value-space precision (P2 / M2),
which does not block the schema from being written but must be resolved before
audit queries filtering by actor identity can be finalized.

**The primary entity schemas are not yet written.** The ownership assignments
are clear. The field contracts are partially derivable. But the formal schema
entity specs for approval records, decision records, handoffs, evidence records,
and content graph entities do not exist as schema authority documents. This is
the primary remaining gap before implementation teams can build the persistence
layer.

**The recommended first implementation step is the ecosystem schema spine.**
It establishes the shared reference patterns that all three system schemas will
use. It is relatively contained (activity trail record formalization + vocabulary
enumeration + reference conventions) and unlocks all downstream schema work.

**Overall implementation-readiness classification: Partially ready — governance
and seam layers are locked, activity trail event vocabulary is canonical, entity
ownership is clear, and the schema-phase artifact sequence is well-defined.
Seven schema-facing artifacts are still required before the persistence layer
can be built with confidence. No architectural decisions are pending. The work
is translation and formalization, not new design.**

---

## Related Docs Referenced in This Pass

- `audit/full-audit/pass-1-governance-and-boundaries.md`
- `audit/full-audit/pass-2-interfaces-and-workflows.md`
- `ecosystem/cross-system-boundaries.md`
- `ecosystem/cross-system-access-governance.md`
- `ecosystem/activity-trail-model.md`
- `ecosystem/activity-trail-integration-map.md`
- `interfaces/data-boundaries.md`
- `interfaces/project-v-to-v-forge-handoff-interface.md`
- `interfaces/veda-to-project-v-signal-interface.md`
- `interfaces/veda-to-v-forge-signal-interface.md`
- `interfaces/v-forge-evidence-access-contract.md`
- `interfaces/project-v-to-veda-evidence-request-interface.md`
- `governance/approval-and-escalation-model.md`
- `governance/approval-mechanics-seam-model.md`
- `governance/decision-continuity-doctrine.md`
- `governance/invalidation-and-supersedence-doctrine.md`
- `governance/auth-and-actor-model.md`
- `governance/allowed-agent-actions-matrix.md`
- `workflows/project-intake-workflow.md`
- `workflows/post-launch-observation-workflow.md`
