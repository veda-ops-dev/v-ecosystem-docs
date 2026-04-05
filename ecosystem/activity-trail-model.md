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

- `evidence.query` — V Forge querying VEDA evidence.
- `signal.query` — Project V querying VEDA signal.
- `execution.query` — Project V reading V Forge execution results.

### State change actions

- `project.create`, `project.update`, `project.archive`
- `task.create`, `task.assign`, `task.start`, `task.complete`, `task.fail`, `task.cancel`
- `evidence.create`, `evidence.update`, `evidence.expire`
- `handoff.create`, `handoff.approve`, `handoff.reject`
- `content.create`, `content.update`, `content.publish`

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

This vocabulary is extensible. New action types must follow the dot-namespace pattern and should be added to this document before use.

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
- `../interfaces/v-forge-evidence-access-contract.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../governance/daily-report-doctrine.md`
- `../ecosystem/cross-system-boundaries.md`
