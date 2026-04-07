# Ecosystem Activity Trail Model

## Purpose

This document defines the structured activity trail for the V Ecosystem.

It exists to answer:

```text
What gets recorded when systems, agents, and operators take actions in the V Ecosystem, what fields must every activity record carry, how does the activity trail make governance verifiable, how does it support cross-system access auditing, and how does it differ from system-specific internal logs?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what actions produce activity trail records
- the required fields on every activity record
- how the activity trail relates to cross-system access governance
- how the activity trail relates to approval and decision auditing
- the relationship between the ecosystem activity trail and system-specific internal logs
- retention posture
- query and replay expectations

---

## Out of Scope

This document does not define:

- the internal logging infrastructure of individual systems
- the specific database schema for activity trail storage
- the UI for activity trail browsing
- system-specific event types beyond the ecosystem-level contract
- detailed implementation of event bus or pub/sub mechanics

Those belong in implementation docs and system-specific docs.

---

## System

- ecosystem

---

## Core Rule

Every meaningful action in the V Ecosystem produces a structured activity record.

The activity trail is not a debug log. It is a governance artifact. It exists so that any action — agent, operator, or system — can be traced, attributed, and reviewed after the fact.

If an action changes state, crosses a system boundary, requires approval, consumes budget, or affects execution outcomes, it must appear in the activity trail.

The activity trail makes governance verifiable. Without it, governance docs are aspirational.

---

## What Produces Activity Records

### State-changing actions

Any action that creates, updates, or deletes a record in any system must produce an activity record.

Examples:
- creating a project in Project V
- updating an evidence record in VEDA
- completing a task in V Forge
- approving a handoff
- pausing an agent

### Cross-system access

Any query from one system to another system's data must produce an activity record.

Examples:
- V Forge querying VEDA evidence
- Project V reading VEDA signal for planning
- Project V reading V Forge execution results

### Approval and governance events

Any approval request, approval decision, escalation, or governance gate evaluation must produce an activity record.

Examples:
- an agent requesting human approval
- a human approving or rejecting a handoff
- an escalation triggered by a budget threshold
- a governance gate blocking an action

### Budget and cost events

Any action that incurs token cost or triggers budget evaluation must produce an activity record.

Examples:
- a V Forge agent's execution consuming tokens
- a cross-system evidence query incurring API cost
- a budget warning threshold being reached
- a budget hard stop pausing an agent

### Agent lifecycle events

Any change in agent state must produce an activity record.

Examples:
- an agent starting execution
- an agent completing a task
- an agent entering a blocked state
- an agent being paused by budget enforcement
- an agent resuming after approval

---

## Required Fields

Every activity record must carry these fields:

### Identity fields

- `activity_id` — unique identifier for this activity record.
- `timestamp` — when the action occurred. UTC. ISO 8601.
- `ecosystem_session_id` — the session or execution context that produced this action, if applicable.

### Actor fields

- `actor_type` — one of: `agent`, `operator`, `system`.
- `actor_id` — identifier of the actor. Agent ID, operator user ID, or system identifier.
- `actor_system` — the system the actor belongs to: `project_v`, `veda`, `v_forge`, `ecosystem`, `extension`.

### Action fields

- `action` — the action type. Uses a dot-namespaced vocabulary (e.g., `evidence.query`, `task.complete`, `approval.decide`, `budget.warning`).
- `action_class` — the action classification: `state_change`, `cross_system_access`, `approval`, `budget`, `lifecycle`.

### Target fields

- `entity_type` — the type of entity affected (e.g., `project`, `evidence`, `task`, `handoff`, `agent`).
- `entity_id` — the identifier of the affected entity.
- `target_system` — the system that owns the affected entity: `project_v`, `veda`, `v_forge`.

### Scope fields

- `project_id` — the project context, if applicable. Null for ecosystem-level actions.
- `company_id` — reserved for future multi-tenant support. Null in single-tenant deployments.

### Detail fields

- `details` — structured key-value metadata specific to the action type. Must not contain secrets, credentials, or raw personal data.
- `result_summary` — brief structured summary of the action outcome (e.g., `{result_count: 15}` for a query, `{status: approved}` for an approval decision).

### Cost fields (when applicable)

- `token_cost` — token cost of the action, if applicable. Null for non-LLM actions.
- `api_cost_cents` — API cost in cents, if applicable. Null for non-API actions.

---

## Action Vocabulary

The activity trail uses a dot-namespaced action vocabulary. This prevents term drift and keeps actions machine-parseable.

### Cross-system access actions

- `evidence.query` — V Forge querying VEDA evidence (V Forge-initiated pull; active query layer per AD-02).
- `evidence.request` — Project V issuing a bounded evidence request to VEDA (AD-03 request-for-package model). This is the request leg only. The response returns through the VEDA → Project V push delivery path and is recorded with `signal.delivery` / `signal.delivery.confirmed` action types. Do not use `signal.query` for this event; the evidence request is a bounded push-request, not a pull.
- `signal.query` — Project V querying VEDA signal (pull model). **Note:** Do not use for VEDA-initiated push delivery events; use `signal.delivery` for those. Do not use for evidence requests; use `evidence.request` for those.
- `execution.query` — Project V reading V Forge execution results (pull model). **Note:** Do not use for V Forge-initiated return-to-planning push events; use `execution.return` for those.

### Cross-system delivery actions

These cover VEDA-initiated push delivery and V Forge-initiated return delivery — governed transfer events where the source-owning system initiates.

**VEDA → Project V signal delivery:**
- `signal.delivery` — VEDA initiates push delivery of a bounded signal package to Project V (proactive or request-response trigger).
- `signal.delivery.confirmed` — Project V confirms receipt of a signal delivery from VEDA.
- `signal.delivery.failed` — VEDA delivery attempt to Project V produced no confirmation within the expected window.
- `signal.delivery.voided` — A signal package was superseded or voided before confirmation.

**VEDA → V Forge startup signal delivery:**
- `signal.delivery.startup` — VEDA initiates push delivery of a bounded baseline execution-startup signal package to V Forge, tied to a specific confirmed handoff scope.

*(For receipt confirmation and failure events on the V Forge startup delivery, use `signal.delivery.confirmed` and `signal.delivery.failed` respectively, with the producing system set to the appropriate side.)*

**V Forge → Project V return-to-planning delivery:**
- `execution.return` — V Forge initiates push delivery of bounded execution findings to Project V for planning reconsideration.
- `execution.return.confirmed` — Project V confirms receipt of a return-to-planning package from V Forge.
- `execution.return.failed` — V Forge delivery attempt to Project V produced no confirmation within the expected window.
- `execution.return.voided` — A return package was superseded or voided before review.

### Planning intake outcome actions

These cover the governed intake outcome events produced by Project V at the conclusion
of the project intake workflow (Stage 5 and Stage 7 closures). They are `state_change`
class events scoped to Project V's planning authority.

- `intake.defer` — Project V records a governed deferral of an intake item: valid but not sufficiently prioritized relative to current planning posture. Decision continuity must be preserved.
- `intake.hold` — Project V records a governed hold on an intake item: valid but timing is not right; conditions may change. Decision continuity must be preserved.
- `intake.reject` — Project V records a governed rejection of an intake item: not a fit for project creation. Rejection continuity must be preserved per `governance/decision-continuity-doctrine.md`.
- `intake.close` — Project V closes an intake item that could not proceed due to a degraded or insufficient basis (Stage 7 closure). The closure reason must be recorded durably. Distinct from defer/hold/reject — this is a closure on insufficient basis, not a governed planning-posture decision.

**Note:** `project.create` remains the canonical action type for the positive intake outcome (project creation). The intake action family covers the four non-creation terminal outcomes.

### Post-launch observation actions

These cover the governed observation-cycle, classification, and assessment events produced
during the post-launch observation workflow. They are `state_change` class events.

- `observation.cycle` — A post-launch observation cycle has completed and the outcome (continue-observation, maintenance, return-to-planning, or escalation) has been recorded. Produced at Stage 6a (continue-observation cycle) and as a summary record at other terminal stages. Each cycle completion must be durably recorded.
- `observation.classify` — Project V or V Forge has produced a classification of post-launch signal (Stage 4 completion). Records the signal-maturity assessment, classification outcome, and the signal basis. Distinct from `observation.cycle` — classification is the Stage 4 interpretation event, not the full-cycle completion.
- `observation.assess` — Project V and V Forge have completed a reconsideration assessment and produced a governed assessment outcome (Stage 5 completion). Records the threshold determination and the routed outcome. Must be produced before the workflow routes to Stage 6a/b/c/d.

**Important constraints:**
- `observation.cycle` is the durable cycle-completion record. `observation.classify` and `observation.assess` are the stage-specific records within a cycle. All three should be produced within a full observation cycle.
- Do not create observation action types for every sub-step within signal capture or observatory activation. These three types cover the governance-meaningful events.
- Signal delivery records for post-launch observation use `signal.delivery` / `signal.delivery.confirmed` per the existing delivery action family, not observation action types.

### Observatory scope change actions

These cover the governed operator-to-VEDA observatory scope change events defined in
`interfaces/operator-to-veda-observatory-scope-expansion-interface.md`. They span
both the request-initiation side (operator surface or Project V acting with operator
approval) and the VEDA response/implementation side.

- `observatory.scope_change.request` — A governed scope change request has been initiated by an operator (direct) or by Project V on behalf of an operator (with documented operator approval). Records the request identity, change type, target scope, and operator approval reference. Action class: `state_change`.
- `observatory.scope_change.accepted` — VEDA has determined the request is valid and will proceed with implementation. Records that VEDA's acceptance has been produced.
- `observatory.scope_change.narrowed` — VEDA accepts a bounded subset of the requested scope change and communicates the narrowing explicitly. The narrowing reason and the accepted subset must be recorded.
- `observatory.scope_change.deferred` — VEDA cannot currently implement the request and has communicated a deferral reason. The deferral reason and re-entry posture must be recorded.
- `observatory.scope_change.rejected` — VEDA has rejected the request due to a validity failure, missing authority reference, or out-of-bounds scope. The rejection reason must be recorded.
- `observatory.scope_change.implemented` — VEDA confirms that the scope change has been implemented in the observatory. Records what specifically changed.
- `observatory.scope_change.voided` — The request has been withdrawn or superseded before VEDA acted on it. The void reason and any superseding request reference must be recorded.

**Important constraints:**
- The `observatory.scope_change.request` record must carry the `operator_approval_ref` field in `details`. A request record without a resolvable approval reference is not a valid governed event.
- `observatory.scope_change.accepted` and `observatory.scope_change.implemented` are distinct events. Accepted means VEDA will proceed; implemented means the scope change is in effect. Both must be recorded.
- Do not create action types for VEDA-internal observatory configuration steps below the governance level. These seven types cover the governance-meaningful events at the seam.
- The producing system differs by event: operator surface or Project V produces the request record; VEDA produces all response and implementation records.

### State change actions

- `project.create`, `project.update`, `project.archive`
- `task.create`, `task.assign`, `task.start`, `task.complete`, `task.fail`, `task.cancel`
- `evidence.create`, `evidence.update`, `evidence.expire`
- `handoff.create` — Project V initiates handoff delivery to V Forge.
- `handoff.confirmed` — V Forge confirms receipt of a delivered handoff package.
- `handoff.failed` — Handoff delivery attempt produced no confirmation.
- `handoff.reject` — A handoff package was voided or superseded before confirmation. **Note:** This covers delivery-state rejection only. Use `approval.decide` with `decision: rejected` for approval-decision events.
- `handoff.recall` — Operator-directed recall of a transferred handoff before V Forge has materially acted.
- `handoff.recall.confirmed` — V Forge confirms receipt of a handoff recall.
- `content.create`, `content.update`, `content.publish`

**Clarification on `handoff.approve` / `handoff.reject`:** These terms may appear in some existing docs but are ambiguous between approval-decision events and delivery-state events. Use `approval.decide` (with `details.decision: approved | rejected`) for approval-decision events. Use `handoff.confirmed` for successful delivery receipt. Use `handoff.reject` only for voided-package state.

### Execution-seam actions (ungated stub interfaces)

These action types cover the stub-level governed interfaces and should be treated as bounded posture until those interfaces are upgraded to full contracts.

- `execution.clarification` — Project V delivers a bounded execution clarification to V Forge during active execution.
- `execution.clarification.confirmed` — V Forge confirms receipt of an execution clarification.
- `execution.scope_update` — Project V delivers a post-replanning scope or constraint update to V Forge.
- `execution.scope_update.confirmed` — V Forge confirms receipt of a scope update.

### Approval actions

- `approval.request`
- `approval.decide` — with `details.decision: approved | rejected | revision_requested`
- `approval.escalate`

### Budget actions

- `budget.cost_event` — a cost-incurring action occurred.
- `budget.warning` — a budget warning threshold was reached.
- `budget.hard_stop` — a budget hard stop was triggered.
- `budget.resume` — a budget-paused scope was resumed.

### Agent lifecycle actions

- `agent.start`, `agent.heartbeat`, `agent.complete`, `agent.fail`, `agent.block`, `agent.pause`, `agent.resume`

### System actions

- `system.startup`, `system.shutdown`, `system.error`, `system.recovery`

This vocabulary is extensible. New action types must follow the dot-namespace pattern and must be added to this document before use in implementations.

### Entity type vocabulary

The `entity_type` field on activity records must use terms from this governed list. The list is extensible; additions must be made here before use.

**Existing entity types:**
- `project` — a Project V project record
- `evidence` — a VEDA evidence or observatory record
- `task` — a V Forge task or execution record
- `handoff` — a Project V handoff record
- `agent` — an agent instance

**Added entity types (from integration map):**
- `signal_package` — a VEDA signal delivery package (used for VEDA → Project V and VEDA → V Forge delivery events)
- `execution_return` — a V Forge return-to-planning findings package
- `launch_authorization` — a launch authorization request record (used for launch-readiness approval events)
- `scope_update` — a post-replanning scope update delivery record
- `execution_clarification` — a mid-execution clarification delivery record
- `evidence_request` — a Project V bounded evidence request record (used for Project V → VEDA evidence request events per AD-03; see `interfaces/project-v-to-veda-evidence-request-interface.md`)
- `intake_outcome` — a Project V intake outcome record (used for `intake.defer`, `intake.hold`, `intake.reject`, and `intake.close` events; scoped to a specific intake item within a project)
- `observation_record` — a post-launch observation record (used for `observation.cycle`, `observation.classify`, and `observation.assess` events; scoped to a specific project and observation cycle)
- `observatory_scope_change` — an operator-to-VEDA observatory scope change request record (used for `observatory.scope_change.*` events; carries the request identity, change type, and operator approval reference)
- `evidence_query` — a V Forge active evidence query record or query session (used for `evidence.query` events under the V Forge → VEDA evidence access contract; see `interfaces/v-forge-evidence-access-contract.md` and integration map Section 4b)

For the integration map reference showing which entity types apply to which seam events, see `activity-trail-integration-map.md`.

---

## Relationship to System-Specific Logs

The ecosystem activity trail is not a replacement for system-specific internal logs.

- **VEDA** may maintain its own internal event log for observatory state changes, provider sync events, and ingestion tracking. These are VEDA's internal operational logs.
- **Project V** may maintain its own planning event history, readiness evaluation logs, and schema change tracking.
- **V Forge** may maintain its own execution logs, content graph change history, and maintenance tracking.

The ecosystem activity trail captures the subset of actions that are meaningful at the ecosystem level — cross-system interactions, governance events, and state changes that affect coordination.

System-specific logs may be more detailed and more frequent. The activity trail is the governed, cross-system audit surface.

---

## Retention Posture

Activity trail records are retained indefinitely by default.

Retention may be configured per action class:

- `state_change` — retain indefinitely. These are the governance backbone.
- `cross_system_access` — retain for at least 90 days. May be compacted to summaries after 90 days.
- `approval` — retain indefinitely. Approval decisions are permanent governance records.
- `budget` — retain for at least 12 months. Cost history supports budget planning.
- `lifecycle` — retain for at least 30 days. May be compacted to summaries after 30 days.

Compaction means replacing detailed records with summary records that preserve the action count, time range, and key metrics. Compaction must not delete approval or state-change records.

---

## Query and Replay

The activity trail must support:

### Filtered queries

- by actor (agent, operator, system)
- by action class
- by target system
- by project scope
- by time range
- by entity type and entity ID

### Replay

Given a project ID and time range, it must be possible to reconstruct the sequence of cross-system actions, approvals, and state changes that occurred. This is the governance replay capability.

Replay does not mean the actions are re-executed. It means the sequence of what happened is recoverable from the activity trail alone.

### Live events

Activity records should be publishable as live events for real-time monitoring. Systems and plugins may subscribe to activity events for dashboards, alerting, or integration purposes.

---

## Usage

This document should be used:

- when building the activity trail infrastructure
- when adding activity logging to new cross-system interfaces
- when designing the activity trail query API
- when building governance dashboards or audit surfaces
- when evaluating whether an action type should produce an activity record
- when defining retention policies for activity data
- when building the live event subscription system

---

## Related Docs

- `cross-system-access-governance.md`
- `activity-trail-integration-map.md` *(concrete seam-to-action-type mapping layer)*
- `../interfaces/v-forge-evidence-access-contract.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../governance/daily-report-doctrine.md`
- `../ecosystem/cross-system-boundaries.md`
