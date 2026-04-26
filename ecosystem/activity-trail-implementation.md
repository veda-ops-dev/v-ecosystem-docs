# Ecosystem Activity Trail Implementation Contract

## Purpose

This document defines the first implementation contract for the ecosystem activity trail.

It exists to answer:

```text
How is the ecosystem activity trail stored, where are activity records written, which trail writes are fail-open or fail-closed, what minimal storage schema is required, and how is the deliberate cross-system trail write surface constrained?
```

This document implements the activity trail posture defined in `activity-trail-model.md`. It does not replace that model.

---

## Status

Ecosystem implementation contract.

This document is owned by the ecosystem spec area because the activity trail is a shared governance surface rather than the private implementation detail of Project V, VEDA, VEDA Strategy, or V Forge.

Authority basis:

- `activity-trail-model.md` defines the ecosystem-level activity trail model and vocabulary.
- `db-posture.md` defines the one-Postgres posture, the four bounded-system schemas, and the constrained `ecosystem` governance schema.
- `decisions/ADR-013-ecosystem-governance-schema.md` authorizes `ecosystem.activity_trail`, `ecosystem.activity_trail_dlq`, and the constrained `ecosystem_trail_writer` role.

---

## Scope

This document governs:

- event granularity for implementation
- the service-layer write location
- fail-open versus fail-closed trail write behavior
- the minimal `ecosystem.activity_trail` table
- the minimal `ecosystem.activity_trail_dlq` table
- required first-pass indexes
- first implementation scope
- the `ecosystem_trail_writer` role boundary

---

## Out of Scope

This document does not define:

- the canonical action vocabulary
- the canonical required fields at the model level
- the activity trail browser UI
- the governance dashboard UI
- the trail query API
- system-specific operational logs
- activity trail compaction jobs
- live event subscription mechanics

The canonical vocabulary and required-field posture belong to `activity-trail-model.md`. Seam-specific mappings belong to `activity-trail-integration-map.md`.

---

## Core Rule

Activity trail writes are implementation of governance, not debug logging.

A governed action must be written as one structured activity record when it crosses a governance-relevant boundary: state change, cross-system access, approval, budget, lifecycle, or execution outcome.

The activity trail records what governed action occurred, who or what performed it, which entity it affected, and what outcome resulted. It is not a full reasoning trace and must not attempt to store full prompts, full completions, raw provider payloads, secrets, or another system's canonical truth.

---

## Relationship to System-Internal Logs

The ecosystem activity trail is the cross-system governance surface.

System-specific operational logs may still exist inside Project V, VEDA, VEDA Strategy, and V Forge. Those logs may be more detailed, more frequent, and more implementation-specific than the ecosystem activity trail.

System-internal logs do not replace the ecosystem activity trail. Per-system trail-like tables or temporary activity records may exist only as system-internal operational logs unless later promoted by governed authority.

The ecosystem activity trail is where governed cross-system replay, approval evidence, handoff custody transfer, and shared audit visibility converge.

---

## Event Granularity

One activity record represents one discrete, attributable action by one actor at one point in time.

An action is discrete when it has:

- one identifiable actor
- one canonical action type
- one target entity
- one outcome

If an operation produces separate outcomes on separate entities, it produces separate activity records. Implementations must not merge distinct governed outcomes into one broad summary record merely for convenience.

Internal reads, in-memory steps, health checks, transport retries below the service boundary, and system-specific debug events do not produce ecosystem activity records unless they cross one of the governance boundaries defined by `activity-trail-model.md`.

---

## Write Location

Activity trail records are written at the service layer.

They are not written by UI components, API handler shells, or domain model methods without governance context.

The service layer is the correct write location because it has access to:

- actor identity
- session context
- project scope
- target entity
- operation outcome
- whether the action is governed

For agent-driven work, the agent wrapper writes lifecycle activity records. The agent's internal reasoning loop must not write directly to the ecosystem activity trail.

For cross-system delivery, the producing system writes the initiation record and the receiving system writes the confirmation, failure, or void record.

---

## Write Timing

Activity records document actions that happened.

The default timing is after the action has occurred or after a failure has been conclusively observed.

The exception is `approval.request`, which is written when the request is submitted to the approval surface. That record opens the approval chain and anchors the later `approval.decide` record.

Failure records are written when failure is established: a timeout expires, an exception is caught, a delivery confirmation is not received in the expected window, or a governed action is blocked.

---

## Write Helper Contract

Every service that writes activity trail records must use a shared write helper. The helper enforces consistent behavior for idempotency, failure handling, and DLQ routing across all services and action types.

The write helper must:

- live at the service layer, not inside domain model methods or API handler shells
- accept an activity record payload and a `fail_closed` boolean parameter
- generate `activity_id` as a UUID before any write attempt, if not already supplied by the caller for a retry
- validate that the following required base fields are present before attempting any DB operation:
  - `timestamp`
  - `actor_type`
  - `actor_id`
  - `actor_system`
  - `action`
  - `action_class`
  - `entity_type`
  - `entity_id`
- write using `INSERT ... ON CONFLICT (activity_id) DO NOTHING` so that a duplicate `activity_id` on retry is a safe no-op
- on fail-closed write failure:
  - route the full attempted payload to `ecosystem.activity_trail_dlq` if possible
  - throw or return a failure result to the caller
  - the caller must halt, hold, or roll back the primary operation
- on fail-open write failure:
  - route the full attempted payload to `ecosystem.activity_trail_dlq` if possible
  - log the failure at error level or equivalent in the system-internal operational log
  - return without throwing so the caller may continue
- preserve the original `timestamp` in the DLQ payload so recovery writes can be timestamped correctly
- never silently swallow trail write failures; failures must be observable

Retries of the same attempted trail write must reuse the same `activity_id`. Delivery retries are different events and receive new `activity_id` values.

---

## Fail-Open and Fail-Closed Behavior

Not all activity trail write failures have the same consequence.

### Fail-open default

Most trail writes are fail-open. If the trail write fails, the primary operation is not rolled back solely because the trail write failed.

Fail-open handling must:

1. record the trail write failure in system-specific operational logs
2. route the attempted activity payload to the dead-letter table or retry buffer
3. preserve the original action timestamp in the payload
4. make the failure observable
5. allow the primary operation to complete where otherwise valid

Fail-open applies to most `cross_system_access`, `budget`, `lifecycle`, and ordinary `state_change` records.

### Fail-closed set

The following activity records are fail-closed:

- `approval.request`
- `approval.decide`
- `handoff.confirmed`

For these events, the trail record must exist durably before the governed outcome is treated as effective.

If a fail-closed write fails, the implementation must not silently continue. It must hold or roll back the primary operation, route the payload to the dead-letter table or retry buffer, and raise an observable alert.

The fail-closed set is intentionally narrow. Expanding it requires explicit design review because fail-closed writes can block execution.

---

## Idempotency

The producing service generates `activity_id` before attempting the trail write.

Retries for the same attempted trail write must reuse the same `activity_id`. The activity trail store treats duplicate `activity_id` writes as an idempotent no-op or equivalent safe upsert behavior.

Delivery retries are different. A new delivery attempt is a new governed action and receives a new `activity_id`. The retry record carries retry context in `details`, such as `is_retry: true` and a reference to the prior delivery record when available.

---

## Linking Fields

### `parent_event_id`

Use `parent_event_id` for direct cause-effect links inside the same system.

Examples:

- `approval.decide` closes an `approval.request`
- `agent.block` follows a `budget.hard_stop`

Do not use `parent_event_id` as the primary cross-system linkage mechanism.

### `correlation_id`

Use `correlation_id` for multi-step cross-system flows such as handoff delivery, signal delivery, evidence request/response, and execution return.

The initiating system generates the `correlation_id`. The receiving system copies it onto the confirmation, failure, or void record.

### `ecosystem_session_id`

Use `ecosystem_session_id` to group records produced within one execution or operator context.

Replay may use `project_id`, `ecosystem_session_id`, `correlation_id`, `entity_type`, `entity_id`, and `parent_event_id` together. None of those fields alone is the whole replay model.

---

## Context Capture Rules

The `details` field must make the record understandable without embedding raw source payloads.

Capture structured references and summaries, not full underlying artifacts.

For LLM-backed governed actions, `details` should capture structured fields such as:

- `llm_model`
- `prompt_class`
- `governance_context_refs`
- `input_artifact_refs`
- `llm_output_summary`

Do not store raw prompt text, full completions, credentials, API keys, raw provider payloads, raw personal data, or Qdrant vector IDs as canonical references.

If retrieval output matters to governance, record the canonical Postgres record reference it resolves to, not the retrieval-layer identifier.

---

## Minimal Storage Schema

### `ecosystem.activity_trail`

The activity trail table lives in the `ecosystem` schema authorized by ADR-013.

It is not owned by Project V, VEDA, VEDA Strategy, or V Forge. It is a shared governance surface with a tightly constrained write path.

```sql
CREATE TABLE ecosystem.activity_trail (
    activity_id          UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp            TIMESTAMPTZ     NOT NULL,
    created_at           TIMESTAMPTZ     NOT NULL DEFAULT now(),

    ecosystem_session_id UUID            NULL,
    parent_event_id      UUID            NULL REFERENCES ecosystem.activity_trail(activity_id),
    correlation_id       UUID            NULL,

    actor_type           TEXT            NOT NULL CHECK (actor_type IN ('agent', 'operator', 'system')),
    actor_id             TEXT            NOT NULL,
    actor_system         TEXT            NOT NULL,

    action               TEXT            NOT NULL,
    action_class         TEXT            NOT NULL CHECK (action_class IN (
                                             'state_change',
                                             'cross_system_access',
                                             'approval',
                                             'budget',
                                             'lifecycle'
                                         )),

    entity_type          TEXT            NOT NULL,
    entity_id            TEXT            NOT NULL,
    target_system        TEXT            NULL,

    project_id           UUID            NULL,
    company_id           UUID            NULL,

    details              JSONB           NOT NULL DEFAULT '{}',
    result_summary       JSONB           NOT NULL DEFAULT '{}',

    token_cost           INTEGER         NULL,
    api_cost_cents       NUMERIC(10,4)   NULL
);
```

Implementation notes:

- `timestamp` is the action time.
- `created_at` is the insert time.
- `actor_id` and `entity_id` are text because the trail references multiple system-owned entity families and must not become a cross-schema join table.
- `details` and `result_summary` use JSONB for bounded structured metadata.
- The table does not enforce foreign keys to subsystem tables.

### Required indexes

```sql
CREATE INDEX idx_at_project_time
    ON ecosystem.activity_trail (project_id, timestamp)
    WHERE project_id IS NOT NULL;

CREATE INDEX idx_at_actor
    ON ecosystem.activity_trail (actor_type, actor_id, timestamp);

CREATE INDEX idx_at_entity
    ON ecosystem.activity_trail (entity_type, entity_id, timestamp);

CREATE INDEX idx_at_session
    ON ecosystem.activity_trail (ecosystem_session_id, timestamp)
    WHERE ecosystem_session_id IS NOT NULL;

CREATE INDEX idx_at_action_class_time
    ON ecosystem.activity_trail (action_class, timestamp);

CREATE INDEX idx_at_correlation
    ON ecosystem.activity_trail (correlation_id)
    WHERE correlation_id IS NOT NULL;

CREATE INDEX idx_at_approval
    ON ecosystem.activity_trail (entity_type, entity_id, action)
    WHERE action_class = 'approval';
```

### `ecosystem.activity_trail_dlq`

A first-pass dead-letter table is required before service-layer write helpers go live.

```sql
CREATE TABLE ecosystem.activity_trail_dlq (
    id          BIGSERIAL   PRIMARY KEY,
    payload     JSONB       NOT NULL,
    failed_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    retry_count INT         NOT NULL DEFAULT 0
);
```

The DLQ table receives full attempted activity payloads when trail writes fail. Draining, retry scheduling, and operator dashboards are later operational work and are not required for the first implementation pass.

---

## Shared Write Role Boundary

The activity trail requires one deliberate cross-system write surface.

That exception is the `ecosystem_trail_writer` role authorized by ADR-013.

The role may have:

- INSERT on `ecosystem.activity_trail`
- INSERT on `ecosystem.activity_trail_dlq`

The role must not have:

- UPDATE on the activity trail tables
- DELETE on the activity trail tables
- broad SELECT over the ecosystem schema
- write access to any subsystem schema

Each system service role may receive this trail writer capability and nothing else through this path.

This is a controlled exception to the normal schema isolation rule in `db-posture.md`. It must not become a precedent for casual shared tables or cross-system data reach-through.

Compaction, retention, repair, and audit jobs require a separate operational role. That role is not granted to subsystem services.

---

## First Implementation Scope

The first implementation must support the governance-load-bearing event families needed before execution workflows become operational.

### Implement first

- `approval.request`
- `approval.decide`
- `approval.escalate`
- `handoff.create`
- `handoff.confirmed`
- `handoff.failed`
- `project.create`
- `project.update`
- `project.archive`
- `agent.start`
- `agent.complete`
- `agent.fail`
- `agent.block`
- `agent.pause`
- `agent.resume`
- `budget.hard_stop`
- `budget.resume`

### Implement before cross-system interfaces go live

- `signal.delivery`
- `signal.delivery.confirmed`
- `signal.delivery.failed`
- `signal.delivery.startup`
- `evidence.query`
- `evidence.request`
- `execution.return`
- `execution.return.confirmed`
- `execution.return.failed`
- `task.create`
- `task.start`
- `task.complete`
- `task.fail`

### Implement when corresponding workflows come online

- intake outcome events
- post-launch observation events
- observatory scope change events
- execution clarification events
- scope update events
- handoff recall events
- budget warning and routine cost events
- agent heartbeat events

The first implementation pass does not require an event bus, compaction table, live subscription system, trail browser, or governance dashboard.

---

## Event Volume Controls

Implementations must avoid activity trail explosion.

- Agent heartbeat is rate-limited at the service or agent-wrapper layer.
- Budget cost events are emitted per discrete cost-incurring call or threshold event, not per token.
- Transport-level retries below the service boundary do not emit activity records.
- Service-level delivery retries do emit new activity records with retry context.
- Cross-system access fan-out is controlled by bounded query budgets and scope constraints, not by suppressing required activity records.

State-change and approval records are retained indefinitely and are not compacted.

Compaction of other action classes is deferred from the first implementation pass.

---

## First-Slice Relevance

For the first V Forge governance proving slice, the required activity trail path is:

1. `approval.request` exists for the handoff.
2. `approval.decide` exists and records an approved decision for the handoff.
3. `handoff.confirmed` is written fail-closed by V Forge before handoff state becomes confirmed.
4. `task.create` is written when the minimal task is created.
5. `agent.start` is written when the synthetic agent starts.
6. `agent.block` is written when the synthetic agent halts with `proving_slice_halt`.

The first-slice replay proof is the ordered recovery of those six records for the handoff.

---

## Anti-Drift Rules

- Do not use Qdrant as an activity trail store.
- Do not treat the trail as a full prompt/completion archive.
- Do not grant subsystem services broad ecosystem schema access because they can write trail records.
- Do not add UPDATE or DELETE rights for subsystem trail writers.
- Do not use the activity trail as a storage loophole for another system's canonical truth.
- Do not expand the fail-closed event set casually.
- Do not skip fail-closed writes in test or development flows.

---

## Related Docs

- `activity-trail-model.md`
- `activity-trail-integration-map.md`
- `cross-system-access-governance.md`
- `db-posture.md`
- `cross-system-boundaries.md`
- `decisions/ADR-013-ecosystem-governance-schema.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/agent-operating-doctrine.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/desktop-governance-and-gating-model.md`