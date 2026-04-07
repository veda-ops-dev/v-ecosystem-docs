# Project V Schema Authority

## Purpose

This document defines the schema authority for Project V's canonical entities.

It exists to answer:

```text
What entities does Project V own, what fields must each entity carry at the schema
level, what are the lifecycle states and linkage requirements for governance-critical
records such as approval_record and decision_record, and how does Project V reference
cross-system entities without duplicating their canonical data?
```

This is a Tier 1 Project V schema authority document.

---

## Scope

This document governs:

- the canonical entity set owned by Project V
- field-level schema contracts for each owned entity
- lifecycle state definitions for governance-critical entities
- cross-system reference posture for Project V records
- the Decision Record vs ADR resolution
- anti-drift rules for Project V schema work

---

## Out of Scope

This document does not define:

- VEDA-owned entity schemas (evidence, signal_package, observatory records)
- V Forge-owned entity schemas (task, content graph, execution records)
- ecosystem-layer enumerated types (defined in `ecosystem/ecosystem-schema-spine.md`)
- transport or storage engine specifics, migration files, or ORM structure
- database index strategy or physical partitioning
- implementation-specific authentication or session handling

Those belong in the respective system schema authority docs, the ecosystem schema
spine, or implementation docs.

---

## System

- project-v

---

## Relationship to Existing Authority Docs

This document derives from and must remain consistent with:

- `interfaces/data-boundaries.md` — the canonical data ownership map that defines
  which record categories Project V owns
- `ecosystem/ecosystem-schema-spine.md` — defines shared enumerated types
  (`actor_type`, `actor_system`, `action_class`, entity type vocabulary, action
  vocabulary), the activity trail record schema contract, and the cross-system
  identity reference pattern; Project V schema must not redefine those
- `governance/actor-identity-schema-spec.md` — defines the `actor_id` value-class
  contract per `actor_type`; Project V schema for `approval_record` and any
  actor-referencing field must conform to it
- `governance/approval-and-escalation-model.md` and
  `governance/approval-mechanics-seam-model.md` — define approval semantics and
  seam mechanics; the `approval_record` schema translates those into a queryable
  entity
- `governance/decision-continuity-doctrine.md` and
  `governance/invalidation-and-supersedence-doctrine.md` — define decision lifecycle
  semantics; the `decision_record` schema translates those into a queryable entity
- `interfaces/project-v-to-v-forge-handoff-interface.md` and
  `workflows/handoff-workflow.md` — define handoff semantics; the `handoff` schema
  derives from those
- `workflows/project-intake-workflow.md` — defines intake outcome semantics; the
  `intake_outcome` schema derives from it
- `workflows/launch-readiness-workflow.md` — informs readiness evaluation posture

This document does not replace any of those authority docs. It translates their
settled canon into schema-level entity contracts for Project V.

---

## Core Rule

Project V is the schema authority for planning truth, orchestration truth, readiness
truth, decision truth, and handoff truth.

Every entity schema defined here must be consistent with the system ownership
boundaries in `ecosystem/cross-system-boundaries.md` and the canonical data
ownership map in `interfaces/data-boundaries.md`.

System schema authority docs extend the ecosystem spine. They do not contradict it.

---

## Project V Schema Authority Boundary

### What Project V owns and defines here

- Project record and project metadata
- Approval record entity schema
- Decision record entity schema
- Handoff record entity schema
- Intake outcome record entity schema
- Readiness evaluation record entity schema
- Planning-side traceability references (thin cross-system pointers with provenance)

### What Project V does not own or define here

- VEDA signal truth, evidence records, observatory records
- V Forge execution truth, content graph, task records
- Ecosystem-layer enumerated types (belong in the schema spine)
- Activity trail records (produced by Project V but governed by the ecosystem layer)

Project V produces activity trail records for its governed events. Those records
conform to the ecosystem schema spine. They are not a Project V-owned entity class;
they are Project V's contribution to the ecosystem-level audit surface.

---

## Canonical Project V Entity Set

Project V owns two distinct tiers of entities, both governed by this document.

**Primary canonical entities** are the core Project V owned records named in the
canonical data ownership map in `interfaces/data-boundaries.md`. Their schema
contracts are the central purpose of this document.

**Project V-governed seam entities** are records that Project V creates and owns
as part of governing specific cross-system transitions — the bounded request or
authorization artifact that anchors the transition in the activity trail and in
Project V's persistent record set. They are included here because Project V is
the schema authority for these records; they are not owned by VEDA or V Forge.

| Entity | Tier | Activity trail entity_type | Governance criticality |
|---|---|---|---|
| `project` | Primary | `project` | Primary planning unit |
| `approval_record` | Primary | (referenced by `approval.*` events) | High — governs all approval-gated transitions |
| `decision_record` | Primary | `decision_record` | High — governs decision continuity |
| `handoff` | Primary | `handoff` | High — governs planning-to-execution transfer |
| `intake_outcome` | Primary | `intake_outcome` | Medium — governs intake decision continuity |
| `readiness_evaluation` | Primary | (referenced at launch auth) | Medium — supports readiness convergence |
| `evidence_request` | Seam | `evidence_request` | Medium — Project V-owned AD-03 request record; governs bounded evidence access to VEDA |
| `launch_authorization` | Seam | `launch_authorization` | High — Project V-owned authorization record; governs launch-sensitive action approval |

---

## Project Entity Schema Contract

The `project` entity is the primary planning unit. A project is created by the
positive outcome of the intake workflow (Stage 5, `project.create` activity event)
and remains active until explicitly archived, cancelled, or completed.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `project_id` | Yes | No | Stable, globally unique identifier assigned by Project V at creation. Immutable after assignment. Used as the reference identifier in cross-system `project_id` scope fields. |
| `created_at` | Yes | No | UTC timestamp of project creation. |
| `created_by` | Yes | No | Actor reference using the `actor_id` value class from `governance/actor-identity-schema-spec.md` for the `operator` or `agent` actor that triggered creation. |
| `planning_scope_summary` | Yes | No | Bounded description of the planning scope this project covers. Must be specific enough to distinguish this project from others in the portfolio. |
| `lifecycle_state` | Yes | No | Current lifecycle state. See lifecycle states below. |
| `intake_outcome_ref` | Yes | No | Reference to the `intake_outcome` entity that produced this project. Provides traceability from project back to the intake evaluation. |
| `governing_signal_basis_ref` | Yes | Yes | Thin reference to the VEDA signal package that informed intake evaluation, if a signal delivery triggered intake. Null for operator/strategy-triggered projects. Must carry provenance fields per the cross-system reference pattern. |
| `current_governing_decision_refs` | Yes | Yes | Array of references to `decision_record` entities that are currently active and governing for this project. May be empty for a newly created project before governing decisions are established. |
| `current_handoff_ref` | Yes | Yes | Reference to the currently active `handoff` entity for this project, if one exists. Null if no handoff is currently active. |
| `updated_at` | Yes | No | UTC timestamp of last record update. |
| `archived_at` | Yes | Yes | UTC timestamp of archiving, if applicable. Null for active projects. |

### Project lifecycle states

`lifecycle_state` represents the project's primary planning posture — the highest-level
governed condition of the project as a whole. It is a single-value field.

- `active` — project is in planning; no terminal decision has been made
- `handed_off` — an active handoff exists and execution responsibility has transferred
- `in_replanning` — the project is undergoing governed replanning after a return-to-planning event
- `completed` — project work is complete and the project is no longer active
- `archived` — project is no longer active; preserved for continuity and history
- `cancelled` — project was explicitly cancelled through a governed planning decision

**On overlapping conditions:** `lifecycle_state` reflects the primary planning posture
at any point in time. When a project is simultaneously in an active handoff and a
replanning event on a different scope, the correct `lifecycle_state` is determined
by the primary governing condition — typically `handed_off` if the handoff remains
active, or `in_replanning` if the replanning has suspended or superseded the active
handoff scope. The specific state of the active handoff and the replanning event are
tracked in the `current_handoff_ref` field and in the relevant `decision_record` and
`handoff` entities respectively. `lifecycle_state` must not be left ambiguous by
setting it to multiple values; overlapping conditions are expressed through the
referenced entity fields, not through the primary lifecycle state field.

---

## Approval Record Entity Schema Contract

The `approval_record` entity is the queryable, persistent record of a governed
approval. It answers "what is the current approval state for this transition?" and
"was this action performed under a valid, still-active approval at the time?"
without requiring replay of the full activity trail.

This entity is distinct from activity trail approval events. Activity trail records
(`approval.request`, `approval.decide`, `approval.escalate`) are immutable event log
entries. The `approval_record` entity is the current and historical state anchor
for a specific approval instance — queryable by entity reference, approval class,
and current state.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `approval_record_id` | Yes | No | Stable, globally unique identifier assigned by Project V. Immutable after assignment. |
| `approved_entity_type` | Yes | No | The `entity_type` of the entity or transition that was subject to approval. Must be a value from the canonical `entity_type` enumeration in the ecosystem schema spine (e.g., `handoff`, `intake_outcome`, `launch_authorization`, `decision_record`). |
| `approved_entity_id` | Yes | No | The `entity_id` of the specific entity or transition this approval covers. Paired with `approved_entity_type` to form the canonical cross-system entity reference. |
| `approval_class` | Yes | No | One of: `A`, `B`, `C`, `D` per `governance/approval-and-escalation-model.md`. Defines the governance class of this approval. |
| `initiating_system` | Yes | No | The `actor_system` value of the system that generated the approval request. |
| `requesting_actor_type` | Yes | No | The `actor_type` of the actor that generated the approval request (typically `agent` or `system`). |
| `requesting_actor_id` | Yes | No | The `actor_id` of the requesting actor, using the value class from `governance/actor-identity-schema-spec.md`. |
| `approval_scope_summary` | Yes | No | Bounded description of what this approval covers. Must be specific enough to determine whether a proposed action falls within the approved scope. |
| `conditions_and_limits` | Yes | Yes | Any conditions, limits, or constraints that were stated at approval time. Null if no conditions were specified. Structured as key-value pairs. |
| `approval_state` | Yes | No | Current state of this approval. See approval states below. |
| `approval_request_activity_ref` | Yes | No | Reference to the `activity_id` of the `approval.request` activity trail record that initiated this approval instance. |
| `approval_decision_activity_ref` | Yes | Yes | Reference to the `activity_id` of the `approval.decide` activity trail record. Null while in `pending` state. |
| `approving_actor_type` | Yes | Yes | The `actor_type` of the actor who granted or rejected the decision. Null while in `pending` state. Must be `operator` for Human-Required approval classes. |
| `approving_actor_id` | Yes | Yes | The `actor_id` of the approving actor, using the value class from `governance/actor-identity-schema-spec.md`. Null while in `pending` state. Must be a stable operator user record identifier for human approvals. |
| `requested_at` | Yes | No | UTC timestamp when the approval request was generated. |
| `decided_at` | Yes | Yes | UTC timestamp when the decision was reached. Null while in `pending` state. |
| `expires_at` | Yes | Yes | UTC timestamp at which this approval expires, if a time-bound applies. Null if no explicit expiry is defined. |
| `revoked_at` | Yes | Yes | UTC timestamp of revocation, if revoked. Null otherwise. |
| `superseded_by_ref` | Yes | Yes | Reference to the `approval_record_id` of the superseding approval, if this approval was superseded. Null otherwise. |

### Approval states

- `pending` — approval request generated; decision not yet reached
- `approved` — approval granted; action may proceed within stated scope
- `rejected` — approval denied; action must not proceed
- `expired` — approval was not resolved within the expected window, or the basis
  changed materially; cannot be silently reused
- `revoked` — approval was explicitly revoked after being granted
- `superseded` — approval has been replaced by a later approval for the same scope
- `escalated` — approval escalated to a higher governance level; decision pending
  at escalation surface

### Queryability requirement

The `approval_record` entity must support at minimum:

- query by `approved_entity_type` + `approved_entity_id`: retrieve all approval
  instances for a specific entity
- query by `approval_state`: retrieve all currently active (`approved`) approvals
- query by `approving_actor_id`: retrieve approvals granted by a specific actor
- query by `approval_class` + `approval_state`: retrieve pending Class C approvals, etc.

These queries support the Reviewability Principle from
`governance/approval-and-escalation-model.md`: the ecosystem must be able to
determine what was approved, who approved it, what scope applied, and whether
the approval is still active.

---

## Decision Record Entity Schema Contract

The `decision_record` entity is the persistent, queryable record of a governing
decision. It answers "what governing decisions constrain this project?" and
"what was the basis for this handoff?" and supports decision continuity across
sessions without requiring reconstruction from memory artifacts.

The decision continuity doctrine (`governance/decision-continuity-doctrine.md`)
and invalidation/supersedence doctrine (`governance/invalidation-and-supersedence-doctrine.md`)
together define the semantic contract this entity must satisfy.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `decision_record_id` | Yes | No | Stable, globally unique identifier assigned by Project V. Immutable after assignment. |
| `decision_summary` | Yes | No | A concise, human-readable statement of the governing decision. Must be sufficient for a later reviewer to understand what was decided without reconstructing conversation context. |
| `decision_class` | Yes | No | The workflow stage or governance context that produced this decision. See decision classes below. |
| `owning_system` | Yes | No | Always `project_v` for decisions owned by Project V. Included for explicit schema clarity. |
| `scope` | Yes | No | One of: `project`, `portfolio`, `ecosystem`. Defines the scope of binding force of this decision. |
| `project_id` | Yes | Yes | Reference to the `project` this decision governs. Null only for portfolio- or ecosystem-scoped decisions that span projects. |
| `lifecycle_state` | Yes | No | Current lifecycle state. See lifecycle states below. |
| `approval_record_ref` | Yes | Yes | Reference to the `approval_record_id` of the approval that made this decision governing, if one was required. Null for decisions that did not require governed approval (Class A actions). |
| `decision_content_ref` | Yes | Yes | Reference to a fuller decision artifact (such as an ADR document) if one exists. Null if the decision exists only as a `decision_record` entity without a separate artifact. See Decision Record vs ADR Resolution section. |
| `governing_evidence_refs` | Yes | Yes | Array of thin cross-system references to VEDA signal packages or evidence that informed this decision, if applicable. May be empty. Each reference must carry provenance fields per the ecosystem spine cross-system reference pattern. |
| `created_at` | Yes | No | UTC timestamp of initial record creation. |
| `created_by_actor_type` | Yes | No | The `actor_type` of the actor who created this record. |
| `created_by_actor_id` | Yes | No | The `actor_id` of the creating actor, using the value class from `governance/actor-identity-schema-spec.md`. |
| `approved_at` | Yes | Yes | UTC timestamp when the governing approval was granted. Null for decisions that did not require approval, or while in `proposed` state. |
| `superseded_at` | Yes | Yes | UTC timestamp of supersedence, if applicable. Null otherwise. |
| `superseded_by_ref` | Yes | Yes | Reference to the `decision_record_id` of the superseding decision. Null unless `lifecycle_state` is `superseded`. |
| `supersedence_reason` | Yes | Yes | The stated reason why this decision was superseded. Required when `lifecycle_state` is `superseded`. Null otherwise. |
| `invalidated_at` | Yes | Yes | UTC timestamp of invalidation, if applicable. Null otherwise. |
| `invalidated_by_ref` | Yes | Yes | Reference to the `decision_record_id` or other governing record that triggered invalidation, if applicable. Null otherwise. |
| `invalidation_reason` | Yes | Yes | The stated reason why this decision was invalidated. Required when `lifecycle_state` is `invalidated`. Null otherwise. |
| `cross_system_consequences_flag` | Yes | No | Boolean. True if this decision has cross-system consequences (e.g., if supersedence or invalidation affects an active handoff, V Forge execution, or VEDA observatory scope). Informs whether cross-system governance actions are required when this decision's state changes. |
| `updated_at` | Yes | No | UTC timestamp of last record update. |

### Decision lifecycle states

- `proposed` — a candidate decision under consideration; not yet continuity-binding;
  has not satisfied required approval posture if any is required
- `approved` — governing decision; has satisfied required approval posture (or required
  none); is active and binding
- `rejected` — a rejected decision outcome; must be preserved for rejection continuity;
  must not be treated as having binding force
- `superseded` — explicitly replaced by a newer governing decision; preserved as
  history; must not be treated as co-equal authority with the superseding decision
- `invalidated` — underlying basis is gone; explicitly marked invalid; preserved as
  history; must no longer constrain active behavior

### Decision classes

The `decision_class` field identifies the governance context that produced the decision.
The following classes are derivable from current docs:

- `intake_decision` — produced during project intake (Stage 5 of the intake workflow);
  governs whether a project is created, deferred, held, or rejected
- `handoff_decision` — produced during handoff preparation and approval; governs the
  scope and constraints of a handoff
- `planning_decision` — a governing planning choice made within Project V during active
  planning or replanning; governs future planning direction
- `replanning_decision` — produced during a replanning event; may supersede prior
  planning or handoff decisions
- `launch_decision` — produced during launch-readiness workflow; governs the scope
  and conditions of launch authorization

This list may be extended when new workflow stages produce distinct governing decisions,
but additions require a canon-level change, not local improvisation.

### Queryability requirement

The `decision_record` entity must support at minimum:

- query by `project_id` + `lifecycle_state = 'approved'`: retrieve all currently
  governing decisions for a project
- query by `lifecycle_state` + decision class: retrieve all decisions in a given state
  by type
- query by `superseded_by_ref`: trace decision history chains
- query by `cross_system_consequences_flag = true`: identify decisions with cross-system
  impact when reviewing supersedence/invalidation

---

## Handoff Entity Schema Contract

The `handoff` entity is the persistent record of a governed planning-to-execution
transfer. Its field contract derives from `interfaces/project-v-to-v-forge-handoff-interface.md`
and `workflows/handoff-workflow.md`.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `handoff_id` | Yes | No | Stable, globally unique identifier assigned by Project V. Must remain stable across re-delivery attempts. If the handoff basis changes materially and a new package is generated, the new package gets a new `handoff_id` referencing the prior one via `prior_handoff_ref`. |
| `project_id` | Yes | No | Reference to the `project` this handoff transfers execution responsibility for. |
| `source_planning_entity_ref` | Yes | No | Reference to the Project V planning entity (initiative, objective, or work item) whose readiness determination justified this handoff. Provides traceability from handoff back to planning context. |
| `approved_execution_scope` | Yes | No | Bounded description of the work being handed off. Must be specific enough that V Forge can determine what is in scope and what is not without unilateral interpretation. |
| `execution_constraints` | Yes | Yes | Any conditions, limits, or constraints execution must respect (cost bounds, external action limits, dependency conditions). Null if no constraints apply beyond the scope definition. Structured as key-value pairs. |
| `readiness_basis_ref` | Yes | No | Reference to the `readiness_evaluation` entity that justified this handoff at the planning level. Provides traceability from handoff to readiness determination. |
| `governing_evidence_refs` | Yes | Yes | Array of thin references to VEDA signal packages or evidence that support this handoff's basis. May be empty. Each reference must carry provenance fields per the ecosystem spine cross-system reference pattern. |
| `expected_execution_outcome` | Yes | No | The planning-side expectation for what execution should produce. Not a detailed specification; describes the objective. |
| `return_to_planning_triggers` | Yes | No | Explicit statement of what kinds of execution findings, failures, or changed conditions should cause V Forge to return findings through the return-to-planning path rather than proceeding autonomously. |
| `approval_record_ref` | Yes | No | Reference to the `approval_record_id` of the activation approval that authorized this handoff. |
| `activation_approval_state` | Yes | No | Current approval state of this handoff's activation approval. Derived from the referenced `approval_record`; reproduced here for efficient query without join. Must stay in sync with the referenced approval record. |
| `delivery_state` | Yes | No | Current delivery state. See delivery states below. |
| `activated_at` | Yes | Yes | UTC timestamp when activation approval was granted. Null while in `awaiting_approval` state. |
| `delivered_at` | Yes | Yes | UTC timestamp when Project V initiated push delivery. Null until delivery begins. |
| `confirmed_at` | Yes | Yes | UTC timestamp when V Forge confirmed receipt. Null until confirmation is received. |
| `package_version_posture` | Yes | No | One of: `original`, `revision`. If `revision`, the `prior_handoff_ref` must be populated. |
| `prior_handoff_ref` | Yes | Yes | Reference to the `handoff_id` of the prior package this revision supersedes. Required when `package_version_posture` is `revision`. Null for original packages. |
| `recall_ref` | Yes | Yes | Reference to the recall event if this handoff was recalled. Null if not recalled. |
| `created_at` | Yes | No | UTC timestamp of handoff record creation (package preparation). |
| `updated_at` | Yes | No | UTC timestamp of last record update. |

### Handoff delivery states

- `awaiting_approval` — activation approval has been requested; delivery has not begun
- `approved` — activation approval granted; delivery not yet initiated
- `delivered` — push delivery initiated by Project V; V Forge confirmation not yet received
- `confirmed` — V Forge has confirmed receipt; execution responsibility has transferred
- `failed` — delivery attempt produced no confirmation within the expected window
- `voided` — package was superseded or withdrawn before confirmation
- `recalled` — an operator-directed recall was issued and confirmed

---

## Intake Outcome Entity Schema Contract

The `intake_outcome` entity is the persistent record of a governed intake decision.
It supports rejection continuity, defer/hold re-evaluation, and traceability from
project records back to their intake basis.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `intake_outcome_id` | Yes | No | Stable, globally unique identifier assigned by Project V. Immutable after assignment. |
| `project_id` | Yes | Yes | Reference to the `project` created by this outcome, if outcome type is `create`. Null for non-creation outcomes (defer, hold, reject, close). |
| `outcome_type` | Yes | No | One of: `create`, `defer`, `hold`, `reject`, `close`. Corresponds to the five terminal intake outcomes defined in `workflows/project-intake-workflow.md`. |
| `signal_basis_ref` | Yes | Yes | Thin reference to the VEDA signal package that informed this intake evaluation, if a VEDA signal delivery triggered intake. Null for operator/strategy-triggered intake items with no associated signal delivery. Must carry provenance fields. |
| `evaluation_basis_summary` | Yes | No | Concise summary of the basis on which the outcome was determined. Must be sufficient for a future reconsideration to understand what was known at the time. |
| `outcome_reason` | Yes | No | The specific reason for this outcome. For `reject`: the rejection reason and scope. For `defer`: the deferral reason. For `hold`: the hold reason. For `close`: the degraded condition. For `create`: may state the opportunity basis concisely. |
| `reconsideration_conditions` | Yes | Yes | For `defer` and `hold` outcomes: the conditions or triggering events that would warrant re-evaluation. Required for `defer` and `hold`. Null for other outcome types. |
| `rejection_scope` | Yes | Yes | For `reject` outcomes: the explicit scope of what was rejected (prevents partial re-entry that pretends rejection was narrower than stated). Required when `outcome_type` is `reject`. Null otherwise. |
| `approval_record_ref` | Yes | Yes | Reference to the `approval_record_id` of the governance review approval, if a review gate was required at Stage 5. Null if no governance review was required. |
| `decided_at` | Yes | No | UTC timestamp when the outcome was produced and became active (or, if a review gate was required, when the review decision was received). |
| `decided_by_actor_type` | Yes | No | The `actor_type` of the actor that produced the outcome. |
| `decided_by_actor_id` | Yes | No | The `actor_id` of the deciding actor, using the value class from `governance/actor-identity-schema-spec.md`. |
| `workflow_trigger_type` | Yes | No | One of: `veda_signal`, `operator_strategy`. Records whether intake was triggered by a VEDA signal delivery (Type A) or an operator/strategy trigger (Type B). |
| `created_at` | Yes | No | UTC timestamp of record creation. |

### Continuity requirement

Rejected, deferred, and held intake outcomes must be retained indefinitely and must
remain queryable by `project_id` (where applicable), `outcome_type`, and time range.
They must not be purged as part of normal record lifecycle management.

A rejected intake item that resurfaces must be resolvable against its prior rejection
record. A deferred or held item re-entering intake must carry a reference to its
prior `intake_outcome_id` so that the prior history is not lost.

---

## Readiness Evaluation Entity Schema Contract

The `readiness_evaluation` entity represents Project V's planning-side determination
that a project or scope is ready for handoff or launch. It is referenced by `handoff`
entities (via `readiness_basis_ref`) and by the launch-readiness workflow.

**Partially specified.** The launch-readiness workflow and the handoff interface define
the semantic requirements for readiness evaluation, but neither specifies a full
field-level entity schema. This contract provides the derivable field posture; some
fields may need refinement when the readiness evaluation use cases are more fully
specified in Project V implementation docs.

### Required fields (derived from current docs)

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `readiness_evaluation_id` | Yes | No | Stable identifier assigned by Project V. |
| `project_id` | Yes | No | Reference to the project this readiness evaluation covers. |
| `evaluation_scope` | Yes | No | Description of what scope was evaluated for readiness (the specific work or scope being prepared for handoff or launch). |
| `evaluation_type` | Yes | No | One of: `handoff_readiness`, `launch_readiness`. Distinguishes evaluations produced during the handoff workflow from those produced during the launch-readiness workflow. |
| `planning_side_assessment` | Yes | No | Project V's determination that planning-side conditions are met. Structured summary of the governing decisions that are current, the planning scope that is bounded, and any planning-side conditions or constraints. |
| `governing_decision_refs` | Yes | Yes | Array of references to `decision_record` entities that govern the scope being evaluated as ready. May be empty for simple cases. |
| `veda_signal_basis_refs` | Yes | Yes | Array of thin references to VEDA signal packages considered in this readiness evaluation. May be empty. Must carry provenance fields. |
| `evaluation_outcome` | Yes | No | One of: `ready`, `not_ready`, `blocked`. |
| `blocking_reason` | Yes | Yes | The reason readiness cannot be confirmed. Required when `evaluation_outcome` is `not_ready` or `blocked`. Null when `ready`. |
| `evaluated_at` | Yes | No | UTC timestamp when this evaluation was produced. |
| `valid_until` | Yes | Yes | UTC timestamp at which this evaluation is expected to become stale, if the assessing actor provided a time bound. Null if no explicit validity window was stated. Implementations should treat readiness evaluations without a `valid_until` as requiring re-confirmation before use in time-sensitive decisions (e.g., launch authorization). |
| `created_at` | Yes | No | UTC timestamp of record creation. |

**Honest scope statement:** The `readiness_evaluation` entity is less sharply specified
than `approval_record`, `decision_record`, and `handoff`. In particular, the detailed
sub-fields of `planning_side_assessment` are not fully enumerated here because the
precise contents depend on what governing decisions and constraints apply to the
specific scope. Project V implementation docs should extend this contract with the
full field list for each `evaluation_type` when those use cases are built out.

---

## Launch Authorization Entity Schema Contract

The `launch_authorization` entity is the persistent record of a governed launch
authorization request and its outcome. It is the schema counterpart to the
`launch_authorization` activity trail entity type.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `launch_authorization_id` | Yes | No | Stable identifier assigned by Project V. |
| `project_id` | Yes | No | Reference to the project this launch authorization covers. |
| `launch_scope_id` | Yes | No | Stable identifier for the specific launch scope being authorized. Referenced in the `approval.request` activity trail record for this authorization. |
| `launch_scope_summary` | Yes | No | Bounded description of the specific launch-sensitive actions being authorized. |
| `stage4_convergence_ref` | Yes | No | Reference to the cross-system convergence record or assessment that established Stage 4 convergence before this authorization request was generated. |
| `reversibility_posture` | Yes | No | Statement of which actions within the authorized scope can be reversed and which cannot. Required per the launch-readiness workflow. |
| `approval_record_ref` | Yes | No | Reference to the `approval_record_id` of the Class C approval covering this launch authorization. |
| `authorization_state` | Yes | No | Current state: one of `pending`, `authorized`, `rejected`, `expired`. Derived from the referenced `approval_record`; reproduced for efficient query. |
| `authorized_at` | Yes | Yes | UTC timestamp of authorization. Null while pending. |
| `created_at` | Yes | No | UTC timestamp of record creation. |

---

## Evidence Request Entity Schema Contract

The `evidence_request` entity is the persistent record of a bounded evidence request
from Project V to VEDA under the AD-03 model. Its field contract derives from
`interfaces/project-v-to-veda-evidence-request-interface.md`.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `evidence_request_id` | Yes | No | Stable identifier assigned by Project V. Must remain stable across re-send attempts. |
| `project_id` | Yes | No | Reference to the project this request is scoped to. |
| `originating_workflow_stage` | Yes | No | The workflow stage and context that generated this request (e.g., `intake_stage_6`, `maintenance_replanning`). |
| `bounded_planning_question` | Yes | No | The specific planning-side evidence need expressed to VEDA. Not a list of records to retrieve; a statement of what planning question requires evidence. |
| `freshness_requirement` | Yes | No | Minimum signal freshness required for Project V to make an honest planning determination. |
| `request_state` | Yes | No | One of: `sent`, `failed`, `response_received`, `response_pending`. |
| `response_delivery_ref` | Yes | Yes | Reference to the `signal_package` entity_id of VEDA's response delivery, when received. Null until response is received. |
| `scope_type` | Yes | No | One of: `project`, `portfolio`. Distinguishes project-scoped from portfolio-scoped evidence requests. Portfolio-scoped requests require explicit authorization context per `ecosystem/cross-system-access-governance.md`. |
| `portfolio_authorization_ref` | Yes | Yes | Reference to the authorization basis for portfolio-scoped requests. Required when `scope_type` is `portfolio`. Null for project-scoped requests. |
| `created_at` | Yes | No | UTC timestamp of initial request record creation. |
| `sent_at` | Yes | Yes | UTC timestamp of first delivery attempt. Null before first send. |
| `response_received_at` | Yes | Yes | UTC timestamp when VEDA's response was received. Null until response arrives. |

---

## Planning-Side Traceability and Cross-System Reference Posture

Project V records reference cross-system entities — VEDA signal packages, V Forge
execution returns — by thin pointer with provenance. The rules here derive from
`ecosystem/ecosystem-schema-spine.md` (Cross-System Identity and Reference Pattern
section) and `interfaces/data-boundaries.md`.

### Thin references only

When a Project V entity references a VEDA or V Forge record, the reference must
consist of:

- the canonical `entity_type` of the referenced entity
- the `entity_id` assigned by the owning system
- provenance fields: `source_system`, `delivered_at` or `retrieved_at`, and
  `freshness_classification` or `trust_classification` where the relevant interface
  defines them

Project V must not store richer or more authoritative copies of VEDA signal packages
or V Forge execution findings than what is necessary for planning-side traceability.

### Specific cross-system reference patterns for Project V

**VEDA signal packages:** Referenced in `project`, `decision_record`,
`readiness_evaluation`, and `intake_outcome` entities via `governing_signal_basis_ref`,
`governing_evidence_refs`, and `signal_basis_ref` fields. These are thin references
pointing to the VEDA-owned `signal_package` entity by its `entity_id`. VEDA remains
the source of truth; Project V stores the reference and provenance, not the signal content.

**V Forge execution returns:** When Project V receives a return-to-planning package,
the bounded execution findings inform replanning but do not become Project V-owned
canonical execution records. Project V may reference the `execution_return` entity
by its V Forge-assigned `entity_id` in replanning decision records, carrying
`source_system: v_forge` and `delivered_at` as provenance. The execution findings
remain owned by V Forge.

**Activity trail records:** Project V produces activity trail records for its governed
events. These records reference Project V entities via `entity_type` + `entity_id`
using the ecosystem-canonical entity type vocabulary. The activity trail is an
ecosystem-layer concern; Project V does not own activity trail records — it produces them.

---

## Decision Record vs ADR Resolution

Pass 3 of the audit flagged that the governance docs reference both `decision_record`
entities and ADRs (Architecture Decision Records) as Project V canonical records,
without disambiguating whether these are the same entity at the schema level.

**Resolution: ADR is a specific representation type within the `decision_record` entity
family, not a separate entity.**

Concretely:

- The `decision_record` entity is the schema-level record of a governing decision.
  It captures the decision's lifecycle state, approval posture, scope, and linkage
  regardless of whether a fuller artifact exists.
- An ADR is a named governing document artifact — a fuller, human-readable description
  of the decision, its context, alternatives considered, and rationale. Not every
  `decision_record` has a corresponding ADR artifact; some governing decisions are
  sufficiently captured in the `decision_summary` field alone.
- When an ADR artifact exists for a decision, the `decision_record` carries a reference
  to it in the `decision_content_ref` field. The `decision_record` is the queryable
  schema entity; the ADR is the human-readable artifact it may point to.
- The `decision_record` lifecycle states, approval posture references, and linkage
  fields (`superseded_by_ref`, `invalidated_by_ref`) are authoritative for governance
  purposes. An ADR document does not have independent lifecycle authority; its governing
  status is determined by the `decision_record` entity that references it.

**What this means in practice:**

- Do not create a separate `adr` entity type in Project V's schema.
- ADR documents are files or artifacts referenced by `decision_record.decision_content_ref`.
- A `decision_record` with `decision_content_ref: null` is a fully valid governed
  decision record; the absence of an ADR artifact does not make the decision ungoverned.
- Supersedence and invalidation are tracked on `decision_record`, not on the ADR document.
  An ADR document that is "superseded" is superseded because its `decision_record`
  has `lifecycle_state: superseded` — not because the document was modified or deleted.

---

## Anti-Drift Rules

**Project V must not duplicate VEDA or V Forge canonical records as local source of truth.**
VEDA signal packages received by Project V are references, not owned copies. V Forge
execution findings received through return-to-planning are references, not Project V
execution records. Any Project V field that stores cross-system data must be a thin
reference with provenance, not a duplicate canonical record.

**Activity trail approval events do not replace `approval_record`.**
The `approval.request`, `approval.decide`, and `approval.escalate` activity trail events
are immutable event log entries. They are not a substitute for the queryable
`approval_record` entity. The `approval_record` must be created and maintained as
a separate entity that supports current-state queries without replaying the activity log.

**Decision continuity memory artifacts do not replace `decision_record`.**
A memory artifact, transcript reference, session note, or compacted summary of a
planning decision is not a `decision_record`. A governing decision that exists only
in session memory has not satisfied its persistence obligation under the decision
continuity doctrine.

**Handoff revision does not silently overwrite prior handoff history.**
When a handoff package is revised, the prior `handoff` entity must remain in the
record set with a reference to the revision. The `prior_handoff_ref` on the new
package links the revision chain. Neither record is deleted; the revision supersedes
the prior package's governing authority while the prior record remains as history.

**Rejected, superseded, and invalidated states must remain queryable.**
No record lifecycle management strategy may delete or compact `decision_record`,
`approval_record`, `handoff`, or `intake_outcome` records that are in terminal
states (`rejected`, `superseded`, `invalidated`, `voided`, `recalled`). These
records are continuity artifacts. They must remain queryable for governance replay.

**Planning traceability references must preserve provenance.**
Any cross-system reference field in a Project V entity (`governing_signal_basis_ref`,
`governing_evidence_refs`, `veda_signal_basis_refs`) must carry the minimum provenance
fields defined in the ecosystem schema spine: `source_system`, `entity_type`,
`entity_id`, and `delivered_at` or `retrieved_at`. A reference without provenance
is not a governed cross-system reference; it is unattributed data.

**`approval_record.approving_actor_id` must be a stable operator user record identifier
for Human-Required approvals.**
For approval classes that require a human actor (`Approve or Authorize: Human-Required`
per `governance/allowed-agent-actions-matrix.md`), the `approving_actor_id` field
must carry a stable operator user record identifier as defined in
`governance/actor-identity-schema-spec.md`. A free-text name, session label, or
agent-produced identifier is not a valid approving actor identity for human-required
approval decisions.

**`decision_record.lifecycle_state` must not be updated without a governed transition.**
A `decision_record` must not move from `approved` to `superseded` or `invalidated`
without a corresponding governed supersedence or invalidation action, including
the approval posture required by `governance/invalidation-and-supersedence-doctrine.md`.
Schema-level updates to `lifecycle_state` without a governance record are drift.

---

## Usage

This document should be used:

- when implementing Project V's persistence layer: use the entity schema contracts
  here as the field-level specifications for Project V database tables or collections
- when designing approval record creation and maintenance: use the `approval_record`
  schema to ensure current-state queryability without activity trail replay
- when designing decision record creation and lifecycle management: use the
  `decision_record` schema and lifecycle states to support decision continuity
  queries and governance replay
- when defining handoff record creation, delivery tracking, and revision: use the
  `handoff` schema and delivery states
- when implementing intake outcome persistence: use the `intake_outcome` schema
  to ensure rejection/defer/hold continuity is maintained
- when referencing VEDA or V Forge entities from Project V records: apply the thin
  reference pattern with provenance as defined in the cross-system reference section
- when the VEDA or V Forge schema authority docs need to know which Project V
  entities they may reference: use the entity set defined here

---

## Related Docs

- `ecosystem/ecosystem-schema-spine.md` *(shared enumerated types, activity trail record schema, cross-system reference pattern)*
- `governance/actor-identity-schema-spec.md` *(actor_id value-class contract)*
- `governance/approval-and-escalation-model.md` *(approval semantics — Tier 1)*
- `governance/approval-mechanics-seam-model.md` *(approval seam mechanics — Tier 2)*
- `governance/decision-continuity-doctrine.md` *(decision lifecycle and persistence obligations)*
- `governance/invalidation-and-supersedence-doctrine.md` *(supersedence and invalidation rules)*
- `interfaces/data-boundaries.md` *(canonical data ownership map)*
- `interfaces/project-v-to-v-forge-handoff-interface.md` *(handoff semantics and validity)*
- `interfaces/project-v-to-veda-evidence-request-interface.md` *(evidence request semantics)*
- `workflows/project-intake-workflow.md` *(intake outcome semantics)*
- `workflows/handoff-workflow.md` *(handoff delivery and approval stages)*
- `workflows/launch-readiness-workflow.md` *(launch authorization and readiness evaluation)*
- `ecosystem/activity-trail-model.md` *(activity trail field contract)*
- `ecosystem/activity-trail-integration-map.md` *(seam-to-action-type mapping)*
- `ecosystem/cross-system-boundaries.md` *(ownership boundaries)*
- `veda/veda-schema-authority.md` *(VEDA entity schemas — to be created)*
- `v-forge/v-forge-schema-authority.md` *(V Forge entity schemas — to be created)*
