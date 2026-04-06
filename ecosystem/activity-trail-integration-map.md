# Activity Trail Integration Map

## Purpose

This document maps the V Ecosystem's current governed interface and seam events
to their canonical activity trail action types, producing systems, required entity
references, and minimum required fields.

It exists to answer:

```text
For each governed interface event or approval-sensitive seam transition that exists
in the repo today, what activity-trail action type applies, which system produces
the record, and what fields must be present to make the record meaningful for
governance replay and audit?
```

This is a Tier 2 ecosystem authority document.

This document extends the Tier 1 activity trail model by applying it concretely
to the current governed interface set. It does not replace the model.

---

## Scope

This document governs:

- the concrete mapping from governed interface/seam events to canonical action types
- the producing system and target system for each mapped event family
- the minimum required fields beyond the base activity-trail required fields
- the mapping posture for ungated stub interfaces
- known vocabulary gaps where existing action types require extension or clarification

---

## Out of Scope

This document does not define:

- the base activity-trail required fields — those belong in `activity-trail-model.md`
- interface data contracts or payload schemas — those belong in the interface docs
- approval class definitions or seam mechanics — those belong in governance docs
- internal system logs below the ecosystem governance level
- new canonical action types not yet validated against the activity-trail model

This document is not a rewrite of any interface doc. It is the integration layer
between the model and the current governed seam set.

---

## System

- ecosystem

---

## Relationship to `activity-trail-model.md`

`activity-trail-model.md` defines:

- what produces activity records (state changes, cross-system access, approvals, budget events, lifecycle events)
- the required base fields on every record
- the canonical dot-namespaced action vocabulary

This document applies that model to the current concrete governed interface events.

Where this document identifies a real residual ambiguity or stub-level caution, it
notes this in the relevant row or section. All major action type extensions have been
applied to `activity-trail-model.md` and are fully canonical.

Read both documents together. The model defines what the trail is and how it works.
This document defines what maps to what for current governed seams.

---

## Mapping Interpretation Rule

Each mapping row covers one **event family** — a class of related activity events
that share the same action type and producing system.

Columns:

| Column | Meaning |
|---|---|
| **Source doc / seam** | The interface or governance doc that governs this event |
| **Event family** | The human-readable description of what the event represents |
| **Canonical action type** | The dot-namespaced action type from `activity-trail-model.md` |
| **Producing system** | The system responsible for writing the activity record |
| **Target system / actor** | The system or actor the event is directed at |
| **Required entity reference** | The `entity_type` and `entity_id` values that must be present |
| **Minimum additional fields** | Fields in `details` beyond the base required fields |
| **Notes / constraints** | Gaps, planned extensions, or usage constraints |

**Base required fields apply to every record** and are not repeated in the minimum
additional fields column. See `activity-trail-model.md` Required Fields section.

---

## Section 1 — VEDA → Project V Signal Delivery

Source: `interfaces/veda-to-project-v-signal-interface.md`

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Delivery initiated | `signal.delivery` | VEDA | Project V | `entity_type: signal_package`, `entity_id: <package/delivery identity>` | `delivery_trigger_type` (`proactive` or `request_response`), `planning_context_ref`, `freshness_classification`, `trust_classification` | `delivery_trigger_type` in `details` distinguishes proactive from request-response delivery. |
| Receipt confirmed | `signal.delivery.confirmed` | Project V | VEDA | `entity_type: signal_package`, `entity_id: <package/delivery identity>` | `delivery_trigger_type`, `planning_context_ref` | Producing system is Project V confirming receipt from VEDA. |
| Delivery failed / unconfirmed | `signal.delivery.failed` | VEDA | Project V | `entity_type: signal_package`, `entity_id: <package/delivery identity>` | `failure_reason`, `retry_posture` | Retry attempt must also produce a delivery-initiated record with the same identity. |
| Re-delivery initiated | `signal.delivery` | VEDA | Project V | Same package identity as original | `is_retry: true`, `prior_delivery_id` | Same action type as initial delivery; `is_retry` distinguishes retry in `details`. |

---

## Section 2 — Project V → V Forge Handoff

Source: `interfaces/project-v-to-v-forge-handoff-interface.md`

Approval events for handoff activation are covered in Section 5 (Approval Events).
The delivery events below cover the transfer itself, which occurs after activation
approval is in place.

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Handoff delivery initiated | `handoff.create` | Project V | V Forge | `entity_type: handoff`, `entity_id: <handoff/delivery identity>` | `source_planning_entity_ref`, `execution_scope_id`, `package_version_posture` | Maps to the delivery initiation event. |
| Receipt confirmed | `handoff.confirmed` | V Forge | Project V | `entity_type: handoff`, `entity_id: <handoff identity>` | `receipt_confirmed_at` | |
| Delivery failed / unconfirmed | `handoff.failed` | Project V | V Forge | `entity_type: handoff`, `entity_id: <handoff identity>` | `failure_reason`, `retry_posture` | |
| Re-delivery initiated | `handoff.create` | Project V | V Forge | Same handoff identity | `is_retry: true`, `prior_delivery_id` | Use same action type; `is_retry` in `details`. |
| Package superseded / voided | `handoff.reject` | Project V | V Forge | `entity_type: handoff`, `entity_id: <handoff identity>` | `superseded_by_ref`, `void_reason` | Use for delivery-state voiding only. Use `approval.decide` for approval-decision events. Do not conflate. |

---

## Section 3 — V Forge → Project V Return-to-Planning

Source: `interfaces/v-forge-to-project-v-return-to-planning-interface.md`

Approval/review events for return-to-planning review are covered in Section 5.
The delivery events below cover the finding transfer itself.

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Return delivery initiated | `execution.return` | V Forge | Project V | `entity_type: execution_return`, `entity_id: <return package/delivery identity>` | `originating_handoff_ref`, `trigger_reason`, `execution_posture` (`halted`, `paused`, `completed_bounded`, `continuing_degraded`) | |
| Receipt confirmed | `execution.return.confirmed` | Project V | V Forge | `entity_type: execution_return`, `entity_id: <return package identity>` | `originating_handoff_ref` | |
| Delivery failed / unconfirmed | `execution.return.failed` | V Forge | Project V | `entity_type: execution_return`, `entity_id: <return package identity>` | `failure_reason`, `retry_posture` | |
| Re-delivery initiated | `execution.return` | V Forge | Project V | Same package identity | `is_retry: true`, `prior_delivery_id` | |
| Package superseded / voided | `execution.return.voided` | V Forge | Project V | `entity_type: execution_return`, `entity_id: <original package identity>` | `superseded_by_ref`, `void_reason` | |
| Review initiated | `approval.request` | Project V | operator / approval surface | `entity_type: execution_return`, `entity_id: <return package identity>` | `approval_class`, `review_rationale` | Uses standard approval action type; see Section 5. |

---

## Section 4 — VEDA → V Forge Startup Signal Delivery

Source: `interfaces/veda-to-v-forge-signal-interface.md`

This covers the **startup push layer** only (AD-02, Layer 1). Active query events
during execution are covered in Section 4b.

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Startup delivery initiated | `signal.delivery.startup` | VEDA | V Forge | `entity_type: signal_package`, `entity_id: <package/delivery identity>` | `originating_handoff_ref`, `signal_scope`, `freshness_classification`, `trust_classification` | Distinct from `signal.delivery` (VEDA → Project V); the startup context is tied to a handoff ref. |
| Receipt confirmed | `signal.delivery.confirmed` | V Forge | VEDA | `entity_type: signal_package`, `entity_id: <package/delivery identity>` | `originating_handoff_ref` | |
| Delivery failed / unconfirmed | `signal.delivery.failed` | VEDA | V Forge | `entity_type: signal_package`, `entity_id: <package/delivery identity>` | `failure_reason`, `retry_posture` | |
| Re-delivery initiated | `signal.delivery.startup` | VEDA | V Forge | Same package identity | `is_retry: true`, `prior_delivery_id` | |
| Package superseded / voided | `signal.delivery.voided` | VEDA | V Forge | `entity_type: signal_package`, `entity_id: <original package identity>` | `superseded_by_ref`, `void_reason` | |

### Section 4b — V Forge Active Evidence Queries (VEDA → V Forge, Query Layer)

Source: `interfaces/v-forge-evidence-access-contract.md`

This covers the **active query layer** (AD-02, Layer 2). These are V Forge-initiated.

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Evidence query (any query type) | `evidence.query` | V Forge | VEDA | `entity_type: evidence_query`, `entity_id: <query session or query id>` | `query_type` (`evidence_by_project`, `evidence_by_topic`, `signal_status`, `evidence_by_id`), `project_id`, `freshness_requirement`, `api_cost_cents` if applicable | `evidence.query` is an existing canonical action type. This seam uses it directly. |

**Boundary note:** `evidence.query` records are produced by V Forge (pull initiated).
`signal.delivery.startup` records are produced by VEDA (push initiated). These two
action types must not be interchanged. See AD-02 layered coexistence model.

---

## Section 5 — Approval-Sensitive Seam Events

Source: `governance/approval-mechanics-seam-model.md`

These action types are already in the canonical vocabulary. The rows below specify
the seam-specific minimum fields for each transition class.

### 5a. Handoff Activation Approval

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Approval request generated | `approval.request` | Project V | operator / approval surface | `entity_type: handoff`, `entity_id: <handoff identity>` | `approval_class` (B or C), `execution_scope_id`, `readiness_basis_ref` | Pending state: `awaiting_approval` |
| Approval decision reached | `approval.decide` | operator / approval surface | Project V | `entity_type: handoff`, `entity_id: <handoff identity>` | `approval_class`, `decision` (`approved`, `rejected`, `expired`), `decision_scope` | |
| Approval escalated | `approval.escalate` | Project V | escalation surface | `entity_type: handoff`, `entity_id: <handoff identity>` | `approval_class`, `escalation_reason` | |

### 5b. Return-to-Planning Review Approval

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Review request generated | `approval.request` | Project V | operator / approval surface | `entity_type: execution_return`, `entity_id: <return package identity>` | `approval_class` (B or C), `originating_handoff_ref`, `review_trigger_summary` | Pending state: `awaiting_review` |
| Review decision reached | `approval.decide` | operator / approval surface | Project V | `entity_type: execution_return`, `entity_id: <return package identity>` | `approval_class`, `decision`, `reconsideration_path` if approved | |
| Review escalated | `approval.escalate` | Project V | escalation surface | `entity_type: execution_return`, `entity_id: <return package identity>` | `approval_class`, `escalation_reason` | |

### 5c. Launch Authorization Approval

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Authorization request generated | `approval.request` | Project V | operator / approval surface | `entity_type: launch_authorization`, `entity_id: <authorization request identity>` | `approval_class` (C), `stage4_convergence_ref`, `launch_scope_id`, `reversibility_posture` | Pending state: `awaiting_authorization`. |
| Authorization decision reached | `approval.decide` | operator / approval surface | Project V | `entity_type: launch_authorization`, `entity_id: <authorization request identity>` | `approval_class`, `decision`, `authorized_scope_id` if approved | |
| Authorization escalated | `approval.escalate` | Project V | escalation surface | `entity_type: launch_authorization`, `entity_id: <authorization request identity>` | `approval_class`, `escalation_reason` | |

### 5d. Replanning with Prior Decision Supersedence

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Supersedence approval request | `approval.request` | Project V | operator / approval surface | `entity_type: decision_record`, `entity_id: <prior decision identity being superseded>` | `approval_class` (B or C), `superseding_decision_summary`, `cross_system_consequences_summary` | Pending state: `awaiting_approval` |
| Supersedence decision reached | `approval.decide` | operator / approval surface | Project V | `entity_type: decision_record`, `entity_id: <prior decision identity>` | `approval_class`, `decision`, `new_governing_decision_ref` if approved | |
| Supersedence escalated | `approval.escalate` | Project V | escalation surface | `entity_type: decision_record`, `entity_id: <prior decision identity>` | `approval_class`, `escalation_reason` | |

### 5e. Governed Intake Outcome Review

Source: `governance/approval-mechanics-seam-model.md` Section E

Covers the governance review gate at Stage 5 of `workflows/project-intake-workflow.md`
when a proposed intake outcome requires human approval before becoming active.

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Review request generated | `approval.request` | Project V | operator / approval surface | `entity_type: intake_outcome`, `entity_id: <intake item identity>` | `approval_class` (B or C), `proposed_intake_outcome`, `intake_basis_ref`, `review_rationale` | Pending state: `awaiting_review` |
| Review decision reached | `approval.decide` | operator / approval surface | Project V | `entity_type: intake_outcome`, `entity_id: <intake item identity>` | `approval_class`, `decision` (`approved`, `rejected`, `expired`) | On `approved`: intake outcome becomes active. On `rejected`: outcome does not activate; rejection continuity applies. |
| Review escalated | `approval.escalate` | Project V | escalation surface | `entity_type: intake_outcome`, `entity_id: <intake item identity>` | `approval_class`, `escalation_reason` | |

---

## Section 6 — Ungated Stub Interface Mappings

These interfaces exist as governed stubs. Their activity trail mappings below provide
bounded posture appropriate to stub-level contracts. Final field-level detail must
be confirmed when these stubs are upgraded to full implementation contracts.

### 6a. Execution Clarification (Project V → V Forge)

Source: `interfaces/project-v-to-v-forge-execution-clarification-interface.md`

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Clarification delivery initiated | `execution.clarification` | Project V | V Forge | `entity_type: execution_clarification`, `entity_id: <clarification identity>` | `originating_handoff_ref`, `clarification_scope_summary` | Stub-level posture. Exact fields subject to full contract upgrade. |
| Receipt confirmed | `execution.clarification.confirmed` | V Forge | Project V | `entity_type: execution_clarification`, `entity_id: <clarification identity>` | `originating_handoff_ref` | |

### 6b. Handoff Recall (Operator-directed → Project V → V Forge)

Source: `interfaces/project-v-handoff-recall-interface.md`

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Recall delivery initiated | `handoff.recall` | Project V | V Forge | `entity_type: handoff`, `entity_id: <recalled handoff identity>` | `recall_reason`, `operator_ref` | Stub-level posture. The prior Handed-Off lifecycle state must be preserved in history. |
| Receipt confirmed | `handoff.recall.confirmed` | V Forge | Project V | `entity_type: handoff`, `entity_id: <recalled handoff identity>` | | |

### 6c. Scope Update (Project V → V Forge, Post-Replanning)

Source: `interfaces/project-v-to-v-forge-scope-update-interface.md`

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Scope update delivery initiated | `execution.scope_update` | Project V | V Forge | `entity_type: scope_update`, `entity_id: <scope update identity>` | `originating_handoff_ref`, `replanning_event_ref`, `scope_change_summary` | Stub-level posture. Governs the post-replanning notification path. |
| Receipt confirmed | `execution.scope_update.confirmed` | V Forge | Project V | `entity_type: scope_update`, `entity_id: <scope update identity>` | `originating_handoff_ref` | |

---

## Section 7 — Project V → VEDA Evidence Request

Source: `interfaces/project-v-to-veda-evidence-request-interface.md`

This covers the **request leg only** (AD-03, bounded request-for-package model). The response
returns through the VEDA → Project V signal delivery path and is covered by Section 1.

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Request initiated | `evidence.request` | Project V | VEDA | `entity_type: evidence_request`, `entity_id: <request identity>` | `planning_context_ref`, `originating_workflow_stage`, `bounded_planning_question_summary`, `freshness_requirement` | Action class: `cross_system_access`. Request identity must be stable across any re-send attempts. |
| Request send failed | `evidence.request` | Project V | VEDA | `entity_type: evidence_request`, `entity_id: <request identity>` | `planning_context_ref`, `originating_workflow_stage`, `delivery_status: failed`, `failure_reason` | Same action type as initiated; `delivery_status: failed` in `details` distinguishes failure records. |
| Request re-sent | `evidence.request` | Project V | VEDA | `entity_type: evidence_request`, `entity_id: <original request identity>` | `planning_context_ref`, `originating_workflow_stage`, `is_retry: true`, `prior_send_id` | Same request identity as original; `is_retry` distinguishes retry in `details`. |

**Response leg note:** VEDA's curated response is delivered through the existing VEDA → Project V push
delivery path. Response events are recorded per Section 1 (`signal.delivery`, `signal.delivery.confirmed`)
with `delivery_trigger_type: request_response` and the originating request identity in `details`.
Do not create separate action types for the response leg.

---

## Section 8 — Mapping Gaps Status

All action type extensions and entity type extensions identified in this map have
been applied to `activity-trail-model.md`. This includes:

- `evidence.request` action type and `evidence_request` entity type (Section 7, Project V → VEDA evidence request interface)
- `intake.defer`, `intake.hold`, `intake.reject`, `intake.close` action types and `intake_outcome` entity type (Section 9, project intake workflow outcomes)
- `observation.cycle`, `observation.classify`, `observation.assess` action types and `observation_record` entity type (Section 10, post-launch observation workflow events)

**Residual notes:**

- `launch_authorization` entity type is now canonical in the model. Use it for
  all launch-readiness approval event records (Section 5c).
- `handoff.approve` as a standalone action type is deprecated in favor of
  `approval.decide` (for approval decisions) and `handoff.confirmed` (for receipt).
  The model carries a clarifying note on this.
- Stub interface action types (`execution.clarification`, `execution.scope_update`,
  `handoff.recall`) are canonical but carry stub-level posture. Minimum fields
  for these should be reviewed when the corresponding stubs are upgraded to full
  implementation contracts.
- The `signal.delivery.startup` and `signal.delivery` action types are both in the
  model. Use `signal.delivery.startup` specifically for the VEDA → V Forge startup
  push layer (tied to a handoff ref). Use `signal.delivery` for VEDA → Project V
  delivery events. Do not interchange them.

---

## Section 9 — Project Intake Workflow Outcomes

Source: `workflows/project-intake-workflow.md`

This covers the terminal intake outcome events produced at Stage 5 (governed outcome) and
Stage 7 (degraded closure) of the project intake workflow. The positive project-creation
outcome uses the existing `project.create` action type; the table below covers the four
non-creation terminal outcomes.

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Intake item deferred | `intake.defer` | Project V | — (internal) | `entity_type: intake_outcome`, `entity_id: <intake item identity>` | `deferral_reason`, `re_evaluation_conditions`, `signal_basis_ref` | Action class: `state_change`. Decision continuity must be preserved. |
| Intake item held | `intake.hold` | Project V | — (internal) | `entity_type: intake_outcome`, `entity_id: <intake item identity>` | `hold_reason`, `triggering_conditions_for_reconsideration`, `signal_basis_ref` | Action class: `state_change`. Decision continuity must be preserved. |
| Intake item rejected | `intake.reject` | Project V | — (internal) | `entity_type: intake_outcome`, `entity_id: <intake item identity>` | `rejection_reason`, `rejection_scope`, `signal_basis_ref` | Action class: `state_change`. Rejection continuity required per `decision-continuity-doctrine.md`. |
| Intake item closed (insufficient basis) | `intake.close` | Project V | — (internal) | `entity_type: intake_outcome`, `entity_id: <intake item identity>` | `closure_reason`, `degraded_condition` | Action class: `state_change`. Stage 7 closure only. Distinct from reject — closed on insufficient basis, not on planning-posture decision. |

**Note on project creation:** `project.create` (existing canonical type) is used for the positive intake outcome. Use `project.create` with `details` capturing the signal basis and planning context reference.

**Note on review gate:** When project creation (or another intake outcome) requires a governance review, use `approval.request` / `approval.decide` per Section 5e (Governed Intake Outcome Review). The `intake_outcome` entity type is used for both the non-creation outcome events above and the Section 5e review events; the `project` entity type applies to the `project.create` event.

---

## Section 10 — Post-Launch Observation Workflow Events

Source: `workflows/post-launch-observation-workflow.md`

This covers the governance-meaningful observation, classification, and assessment events
produced during the post-launch observation workflow. Signal delivery events in this
workflow use the existing Section 1 and Section 4 mappings. Return-to-planning
activation uses Section 3. This section covers the observation-specific records.

| Event family | Canonical action type | Producing system | Target system | Required entity reference | Minimum additional fields | Notes |
|---|---|---|---|---|---|---|
| Classification produced (Stage 4) | `observation.classify` | Project V and/or V Forge | — (internal) | `entity_type: observation_record`, `entity_id: <observation cycle identity>` | `signal_maturity_assessment` (`mature` or `immature`), `classification_outcome`, `signal_basis_ref`, `producing_system` | Action class: `state_change`. Must be produced before the workflow exits Stage 4. If signal is immature, `classification_outcome: continue_observation`. |
| Assessment completed (Stage 5) | `observation.assess` | Project V | — (internal) | `entity_type: observation_record`, `entity_id: <observation cycle identity>` | `threshold_determination`, `routed_outcome` (`continue_observation`, `maintenance`, `return_to_planning`, `escalation`), `assessment_basis_summary` | Action class: `state_change`. Must be produced before the workflow routes to Stage 6a/b/c/d. |
| Observation cycle completed (Stage 6a) | `observation.cycle` | Project V | — (internal) | `entity_type: observation_record`, `entity_id: <observation cycle identity>` | `cycle_outcome` (`continue_observation`, `maintenance`, `return_to_planning`, `escalation`), `cycle_number`, `next_cycle_trigger` | Action class: `state_change`. Durable cycle-completion record. Must be produced at every terminal cycle outcome. |

**On cycle identity:** Each observation cycle should carry a stable cycle identity that links the `observation.classify`, `observation.assess`, and `observation.cycle` records for that cycle. This allows governance replay across a multi-cycle observation history.

**On signal delivery records:** Post-launch signal delivery events use `signal.delivery.confirmed` per Section 1 (Project V receipt) and Section 4 (V Forge receipt). Do not use observation action types for signal delivery.

**On return-to-planning activation:** When Stage 6c (return-to-planning) is triggered, V Forge produces an `execution.return` record per Section 3. The `observation.cycle` record captures that the assessment outcome was `return_to_planning`; the Section 3 records cover the delivery mechanics.

---

## Usage

This document should be used:

- **by interface docs** when specifying their Activity Trail section: reference the
  exact action type, producing system, and minimum fields from this map rather than
  inventing ad hoc names
- **by workflow docs** when wiring event transitions to activity trail records: use
  this map to identify the correct action type for each stage boundary event
- **by implementations** when building activity-trail record production: do not
  invent alternate action names when a mapped action exists here; use the canonical
  type or surface the gap through the governed change path
- **by stewards** when auditing whether interface and workflow docs are using
  consistent action types across the seam set

Interface docs do not need to reproduce this map inline. They should reference it
and name the specific event families that apply to their seam.

Implementations must not invent alternate action names for seams that are already
mapped here. If a seam event is not yet mapped, surface the gap through the
governed extension path (add to `activity-trail-model.md` first, then this map).

---

## Anti-Drift Rules

- Do not invent action types not in this map or the base model without following the
  governed extension path (add to `activity-trail-model.md` first, then this map)
- Do not use `signal.query` for push delivery events
- Do not conflate `handoff.approve`/`handoff.reject` with `approval.decide` — they
  are distinct event families covering different phases
- Do not use startup signal delivery action types for mid-execution evidence queries
  and vice versa
- Do not produce activity records without the required base fields; this map's
  minimum additional fields are in addition to, not instead of, those fields
- Stub interface action types are bounded to stub posture; do not treat them as
  finalized until the interface is upgraded to a full contract

---

## Related Docs

- `activity-trail-model.md` *(Tier 1 authority — read before this doc)*
- `cross-system-access-governance.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/project-v-to-veda-evidence-request-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-evidence-access-contract.md`
- `../interfaces/project-v-to-v-forge-execution-clarification-interface.md`
- `../interfaces/project-v-handoff-recall-interface.md`
- `../interfaces/project-v-to-v-forge-scope-update-interface.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/approval-and-escalation-model.md`
- `../workflows/project-intake-workflow.md`
- `../workflows/post-launch-observation-workflow.md`
