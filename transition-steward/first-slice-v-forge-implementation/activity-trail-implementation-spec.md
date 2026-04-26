# Activity Trail Implementation Spec

## Status

Transition-steward working doc. Not a canonical authority document by itself.
Load-bearing conclusions must be promoted into the proper canonical doc set.

## Purpose

This document bridges the gap between the activity trail doctrine defined in
`ecosystem/activity-trail-model.md` and the concrete implementation decisions
an engineer needs to start building.

It does not restate the model. It answers the implementation questions the model
intentionally left open.

Read `ecosystem/activity-trail-model.md` and `ecosystem/activity-trail-integration-map.md`
before this document.

---

## 1. Event Granularity Rules

### What counts as a single activity event

One activity record represents one discrete, attributable action by one actor
at one point in time.

An action is discrete if it has:
- a single identifiable actor (agent, operator, or system)
- a single action type from the canonical vocabulary
- a single target entity
- a single outcome (success, failure, or blocked)

If an operation produces two distinct outcomes on two distinct entities, it
produces two records. Do not merge them.

### Governed actions that always produce a record

Every action in the following categories must produce a record, no exceptions:

- **State-changing actions**: any create, update, delete, archive, or publish
  on a governed entity (project, task, evidence, handoff, content, intake_outcome,
  observation_record, observatory_scope_change)
- **Cross-system calls**: any query or delivery that crosses a system boundary,
  including all events in the integration map (Sections 1–11)
- **Approval events**: every `approval.request`, `approval.decide`, and
  `approval.escalate` — these are permanent governance records
- **Budget events**: every cost event, warning threshold, hard stop, and resume
- **Agent lifecycle events**: start, complete, fail, block, pause, resume
- **LLM outputs that produce a governed artifact**: when an LLM call produces an
  intake outcome classification, a planning recommendation, a scoring result, or
  a content artifact, the action that wraps that call must produce a record

### LLM outputs — specific rule

An LLM call does not automatically produce its own activity record.
The service-layer action that initiated the LLM call and consumed its output
is the unit that produces the record. The `details` field on that record must
capture what the LLM was given (see Section 4) and what it returned (via
`result_summary`).

Do not emit a record for every LLM token stream. Emit a record when the
orchestrating service acts on the LLM output.

Exception: if an LLM call directly triggers a budget event (token cost exceeds
a threshold), a `budget.cost_event` record is also required.

### What does NOT produce a record

- Internal read operations that do not cross a system boundary (e.g., a service
  reading from its own schema)
- In-memory computation steps, intermediate state, and retry loops below the
  service boundary
- Health checks, connection tests, and polling that do not produce state changes
- Qdrant vector queries that are internal to a single system's retrieval layer
  (these are below the governance surface; Qdrant is retrieval infrastructure)
- Agent heartbeat emissions below the configured heartbeat interval (one
  `agent.heartbeat` per interval is sufficient; do not emit on every loop tick)
- System-internal log events — these belong in system-specific operational logs,
  not the ecosystem activity trail

### Minimum event emission boundaries

| Boundary type | Emit at |
|---|---|
| API layer (inbound request) | After request validation passes, before execution begins — for governed action types only |
| Service layer (cross-system call) | At call initiation and at confirmed receipt/failure |
| Agent wrapper | At lifecycle transitions (start, block, pause, resume, complete, fail) |
| Approval gate | At request generation and at decision |
| Budget enforcer | At threshold evaluation that produces an outcome (warning, stop, resume) |
| LLM orchestration | At the point the output is consumed and acted upon |

---

## 2. Event Write Rules

### Where events are written

Activity records are written at the **service layer**, not the API handler layer and
not inside domain model logic.

Rationale: the API layer is too early (validation may still fail, the action may
not yet have occurred) and domain model logic is too deep (it does not have access
to actor identity and session context).

The correct location is the service function that executes the governed action,
after the action has occurred (or conclusively failed).

For agent-driven actions, the **agent wrapper** is responsible for lifecycle
event emission. The agent itself should not write activity records directly.

For cross-system delivery events (handoff, signal delivery, evidence request),
the **producing system's service layer** writes the initiation record. The
**receiving system's service layer** writes the confirmation record.

### When they are written

**After the action, not before.** The record documents what happened.

The sole exception is `approval.request`, which must be written at the moment the
request is submitted to the approval surface — not after the decision. The request
record creates the governance paper trail that the subsequent `approval.decide`
closes.

**For failures**: write the failure record immediately when the failure is
confirmed (timeout elapsed, exception caught, delivery confirmation not received
within window). Do not suppress failure records.

### Failure handling — what if logging fails

Not all trail write failures carry the same consequence. The spec distinguishes
two postures.

**Fail-open (most events)**

For the majority of action classes — `cross_system_access`, `budget`, `lifecycle`,
and most `state_change` events — the trail write must not block the primary
operation from completing. Handle write failures as follows:

1. Log the write failure to the system's internal operational log with full
   record payload for recovery.
2. Do not roll back the primary action because the trail write failed.
3. Emit to a dead-letter queue or retry buffer. Trail records may be written
   slightly out of order in recovery; the `timestamp` field preserves the
   actual action time.
4. Do not silently swallow trail write failures. They must be observable.

**Fail-closed (governance-critical decisions)**

The following events must be written durably before the primary operation is
considered complete. If the trail write fails and cannot be immediately recovered,
the primary operation must be rolled back or held pending, and an alert must be
raised immediately:

- `approval.decide` — an approval decision with no trail record is an
  unverifiable governance gap. The decision must not be treated as effective
  until the record exists.
- `approval.request` — the request record opens the governance paper trail.
  Without it, the `approval.decide` record has no anchor.
- `handoff.confirmed` — confirmed handoff receipt is a custody transfer. A
  confirmation with no trail record leaves ownership ambiguous.

For fail-closed events, the write helper must attempt a synchronous durable
write with a short timeout (suggested: 2 seconds). On failure, it must not
complete the primary operation. It must raise an alert and hold.

The fail-closed set is intentionally narrow. Do not expand it without explicit
decision. The cost of blocking on a trail write is high; reserve it for the
events where an unrecorded outcome is worse than a delayed operation.

### Idempotency rules

Every activity record has a globally unique `activity_id`. The producing service
is responsible for generating this ID before the write attempt.

If a trail write is retried due to a transient failure, the same `activity_id`
must be used. The trail store must treat a duplicate `activity_id` as an
idempotent no-op (upsert by ID, not insert).

For delivery retry patterns (re-delivery of a handoff, re-send of an evidence
request), each retry produces a **new** record with a **new** `activity_id`, but
the `details` field carries `is_retry: true` and `prior_delivery_id` pointing to
the original record. The retry is a new event, not a replacement.

---

## 3. Event Linking Model

### parent_event_id

`parent_event_id` is an optional field. Use it when one activity record is a
direct consequence of another within the same system. Examples:

- an `agent.block` that is directly caused by a `budget.hard_stop` in the same
  execution scope: the `agent.block` record carries the `budget.hard_stop` record's
  `activity_id` as its `parent_event_id`
- an `approval.decide` that closes an `approval.request`: the `approval.decide`
  record carries the `approval.request` record's `activity_id` as its
  `parent_event_id`

Do not use `parent_event_id` across system boundaries. Cross-system linkage is
handled by `correlation_id` (see below), shared entity references (`entity_id`),
and `ecosystem_session_id`.

### correlation_id

`correlation_id` is an optional field for multi-step cross-system flows where
different systems write distinct records that belong to the same logical operation.

Use `correlation_id` when:
- A delivery initiates on one system and confirms on another (handoff, signal
  delivery, execution return, evidence request/response)
- Retries are in flight and the original and retry records need to be linked
  across system boundaries
- Parallel deliveries to multiple targets are issued from one source action

How to assign it: the **initiating system** generates the `correlation_id` (UUID)
and writes it on the initiation record. The **receiving system** copies it onto
the confirmation or failure record. Both ends carry the same value.

This is distinct from `entity_id`, which identifies what the action was about.
`correlation_id` identifies which cross-system operation instance this record
belongs to. Under concurrency (multiple deliveries of the same entity type in
flight), `entity_id` alone may not distinguish them. `correlation_id` does.

`correlation_id` is not a session ID and not a parent event ID. It is a lateral
link across system boundaries for one logical operation.

For single-system events, leave `correlation_id` null.

### Session grouping

`ecosystem_session_id` is the primary grouping key for replay.

A session represents one coherent execution context — one agent run, one planning
workflow pass, one operator interaction sequence. All activity records produced
within that context carry the same `ecosystem_session_id`.

Rules for session assignment:
- Agent runs: one session per agent invocation. If an agent is paused and resumed,
  carry the same session ID through the resume.
- Operator interactions: one session per operator's active action sequence (e.g.,
  one approval review session). New session on each new login/interaction context.
- Scheduled system actions: one session per scheduled job execution.
- Cross-system delivery chains: the initiating system's session ID is recorded on
  the initiation record. The receiving system records its own session ID on the
  confirmation record. The shared `entity_id` links the two records.

Sessions are not hierarchical. There is no parent session. If replay needs to
span multiple sessions, use `project_id` as the outer grouping key.

### Reconstructing chains for replay

Given a `project_id` and a time range, replay reconstruction works as follows:

1. Fetch all activity records for the `project_id` in the time range, ordered by
   `timestamp`.
2. Group by `ecosystem_session_id` to see execution contexts.
3. For each cross-system delivery event, link the initiation and confirmation
   records by `entity_id` and `entity_type`.
4. For approval chains, link `approval.request` → `approval.decide` by
   `parent_event_id` (if set) or by matching `entity_id` + `entity_type` within
   the same time window.
5. For agent lifecycle sequences, order by `timestamp` within the session and
   follow `parent_event_id` links for cause-effect chains.

**Replay does not re-execute actions.** It produces a time-ordered, linked
sequence of what happened. The schema and indexes in Section 5 support this
directly.

### What replay cannot reconstruct — scope boundary

The activity trail is a **governed action trail**. It records discrete, attributed
actions at system and service boundaries. It is not a full agent reasoning trace.

Replay will not reconstruct:
- The internal reasoning steps, tool calls, and intermediate outputs an agent
  produced between activity trail emission points
- The exact prompt content sent to any LLM call
- The full content of evidence packets or signal packages that were consulted
- The sequence of in-memory decisions made within a single agent invocation
  before a trail-emitting boundary was crossed

This is a deliberate design boundary, not a gap to fill later. The trail records
*what governed actions occurred and what their outcomes were*. It does not record
*how an agent reasoned its way to those actions*.

Implication for operators and implementers: do not represent this trail to
stakeholders as a complete agent audit log or a full reasoning trace. It is an
auditable record of governed actions. Deeper agent inspection requires system-
specific operational logs maintained at the individual system level, which are
out of scope for this trail.

---

## 4. Context Capture Rules

### What must be captured per event

The `details` JSONB field must carry the context that makes the record self-
explanatory in isolation. An engineer reading the record six months later must
be able to understand what the actor saw, what they acted on, and what happened.

**For all events**, `details` must include:
- The action's triggering context reference (e.g., `project_id`, `handoff_ref`,
  `planning_context_ref`) where applicable — these are the links that make replay
  coherent
- Any classification or outcome label that the action produced or consumed
  (e.g., `signal_maturity_assessment: mature`, `decision: approved`)
- Status of the action (e.g., `delivery_status: delivered`, `result: blocked`)

**For LLM-backed actions**, `details` must additionally include three distinct
structured fields. Do not collapse these into a single summary blob — they answer
different governance questions and must remain independently readable.

- `llm_model`: the model identifier used (e.g., `"claude-sonnet-4-20250514"`)

- `prompt_class`: the category of prompt used. A short controlled-vocabulary label
  such as `"intake_scoring"`, `"gap_detection"`, `"content_draft"`. This identifies
  *what kind of reasoning was invoked*, not what was said.

- `governance_context_refs`: the governed records and decisions that were admitted
  as context for this LLM call. These are the things whose authority was invoked.
  Structured as a list of typed references:
  `[{ref_type: "signal_package", ref_id: "..."}, {ref_type: "planning_decision", ref_id: "..."}]`.
  If no governed records were admitted (e.g., a purely generative call), record
  `governance_context_refs: []` explicitly — the empty list is informative.

- `input_artifact_refs`: the specific evidence packets, signal packages, or
  documents that were passed as content input. These are the payloads the model
  actually read. Structured as typed references:
  `[{ref_type: "evidence_request", ref_id: "..."}, {ref_type: "handoff", ref_id: "..."}]`.
  This is distinct from `governance_context_refs` — governance context is what
  authorized the call; input artifacts are what the model consumed.

- `llm_output_summary`: a structured summary of what the LLM returned, consistent
  with what is already in `result_summary`. Do not duplicate the full output.
  Capture the classification label or decision produced, not the prose.

Do not capture raw prompt text under any of these fields.

**For cross-system delivery events**, `details` must include the fields specified
in the integration map for that seam (Sections 1–11 of the integration map).
These are not optional — they are the minimum required for the record to be
useful for governance.

### What must NOT be captured

- Raw prompt text or full LLM completions
- User credentials, API keys, tokens, or secrets of any kind
- Raw personal data (names, emails, identifiers not already present in the
  governed entity model)
- Full evidence payloads or signal package contents — carry a reference
  (`evidence_id`, `package_id`), not the payload
- Qdrant vector IDs as canonical references — if a retrieval result is relevant,
  reference the Postgres canonical record it resolves to

### Structured summaries vs raw data

When an action involves input data that is large or variable (e.g., a set of
evidence records that informed a scoring decision), the pattern is:

- Capture the count and key classification: `{evidence_count: 12, freshness_class: "recent"}`
- Carry a reference to the source entity: `{evidence_request_id: "..."}`
- Do not inline the evidence content

This keeps records compact, avoids sensitive data leakage, and keeps the trail
queryable without requiring large payload parsing.

---

## 5. Minimal Storage Schema

### Table: `ecosystem.activity_trail`

This table lives in a dedicated `ecosystem` schema (or an agreed equivalent
that is owned by no single subsystem). It is not in `project_v`, `veda`,
`v_forge`, or `veda_strategy`.

```sql
CREATE TABLE ecosystem.activity_trail (
    -- Identity
    activity_id         UUID            PRIMARY KEY DEFAULT gen_random_uuid(),
    timestamp           TIMESTAMPTZ     NOT NULL,
    created_at          TIMESTAMPTZ     NOT NULL DEFAULT now(),

    -- Session / grouping
    ecosystem_session_id UUID           NULL,
    parent_event_id      UUID           NULL REFERENCES ecosystem.activity_trail(activity_id),
    correlation_id       UUID           NULL,

    -- Actor
    actor_type          TEXT            NOT NULL CHECK (actor_type IN ('agent', 'operator', 'system')),
    actor_id            TEXT            NOT NULL,
    actor_system        TEXT            NOT NULL,

    -- Action
    action              TEXT            NOT NULL,
    action_class        TEXT            NOT NULL CHECK (action_class IN (
                                            'state_change', 'cross_system_access',
                                            'approval', 'budget', 'lifecycle')),

    -- Target
    entity_type         TEXT            NOT NULL,
    entity_id           TEXT            NOT NULL,
    target_system       TEXT            NULL,

    -- Scope
    project_id          UUID            NULL,
    company_id          UUID            NULL,

    -- Detail
    details             JSONB           NOT NULL DEFAULT '{}',
    result_summary      JSONB           NOT NULL DEFAULT '{}',

    -- Cost
    token_cost          INTEGER         NULL,
    api_cost_cents      NUMERIC(10,4)   NULL
);
```

**Notes on field types:**
- `activity_id` is UUID. Generate at the service layer before the write attempt
  (enables idempotent retry).
- `timestamp` is the actual time the action occurred. `created_at` is the DB
  insert time. They will differ when records are written from a retry buffer.
- `actor_id` and `entity_id` are TEXT, not typed foreign keys. The activity trail
  does not enforce referential integrity to subsystem tables — it is a governance
  record, not a relational join table.
- `details` and `result_summary` are JSONB. Do not use JSON (TEXT). JSONB supports
  index operators.

### Required indexes

```sql
-- Replay by project + time (primary replay query)
CREATE INDEX idx_at_project_time
    ON ecosystem.activity_trail (project_id, timestamp)
    WHERE project_id IS NOT NULL;

-- Actor filtering (audit: what did this agent/operator do?)
CREATE INDEX idx_at_actor
    ON ecosystem.activity_trail (actor_type, actor_id, timestamp);

-- Entity filtering (audit: what happened to this handoff/project/task?)
CREATE INDEX idx_at_entity
    ON ecosystem.activity_trail (entity_type, entity_id, timestamp);

-- Session grouping (replay: reconstruct one execution context)
CREATE INDEX idx_at_session
    ON ecosystem.activity_trail (ecosystem_session_id, timestamp)
    WHERE ecosystem_session_id IS NOT NULL;

-- Action class filtering (retention + compaction queries)
CREATE INDEX idx_at_action_class_time
    ON ecosystem.activity_trail (action_class, timestamp);

-- Correlation lookup (cross-system delivery chain linkage)
CREATE INDEX idx_at_correlation
    ON ecosystem.activity_trail (correlation_id)
    WHERE correlation_id IS NOT NULL;

-- Approval chain lookup (find open requests by entity)
CREATE INDEX idx_at_approval
    ON ecosystem.activity_trail (entity_type, entity_id, action)
    WHERE action_class = 'approval';
```

### No separate compaction table in first pass

Do not build a compaction table in the first implementation pass. Compaction is a
retention operation that can be added later. Start with the single table above.

---

## 6. Event Volume Control

### What gets compacted

The following action classes may be compacted after the retention windows defined
in the model:

- `cross_system_access` records older than 90 days may be replaced with a
  summary record per (actor_id, entity_type, project_id, month) carrying:
  - total event count
  - first and last timestamp
  - action types present
  - aggregate `api_cost_cents` and `token_cost`
- `lifecycle` records older than 30 days may be replaced with a summary record
  per (actor_id, project_id, action, month) carrying:
  - total event count, first and last timestamp

Compaction is a background job. It must:
1. Write the summary record first
2. Verify the summary write succeeded
3. Delete the originals in a bounded batch (not a single large DELETE)

### What never gets compacted

- `state_change` records — retain indefinitely, never compact
- `approval` records — retain indefinitely, never compact, never delete
- Any record where `action_class IN ('state_change', 'approval')` is protected
  from all compaction operations

### Avoiding event explosion

The primary explosion risks are agent heartbeat and budget cost events.

**Agent heartbeat**: `agent.heartbeat` records must be rate-limited at the service
layer. Emit at most one heartbeat record per agent per configured interval
(default: 60 seconds). The agent wrapper enforces this. Do not let heartbeat emit
on every processing loop.

**Budget cost events**: `budget.cost_event` records should be emitted at threshold
boundaries, not on every token consumed. The budget enforcer emits one record when
a cost event is logged (per discrete LLM call or API call with a cost). It does not
emit on individual tokens. The `budget.warning` and `budget.hard_stop` records are
threshold events — one per threshold crossing, not recurring.

**Cross-system access fan-out**: if a single agent action triggers N evidence
queries, each query produces one `evidence.query` record. There is no batching
at the record level. Control volume at the agent design level (bounded query
budgets per execution scope). The integration map Section 4b governs the minimum
required fields for each query record.

**Delivery retry chains**: each retry produces a new record (correct). But do not
emit a new record for every TCP-level retry or transport-level retry below the
service boundary. Emit at the service delivery attempt level.

---

## 7. First Implementation Scope

### Phase 1 — Must implement first

These are the event types that are load-bearing for governance from day one.
Nothing should go to production without these.

**Approval events (all three types):**
- `approval.request`
- `approval.decide`
- `approval.escalate`

Rationale: approval decisions are permanent governance records. If these are missing,
the entire approval model is unverifiable.

**Handoff delivery events:**
- `handoff.create`
- `handoff.confirmed`
- `handoff.failed`

Rationale: handoff is the primary cross-system transfer. Its delivery state must be
auditable from the start.

**Project state-change events:**
- `project.create`
- `project.update`
- `project.archive`

Rationale: projects are the outer container for everything. Their lifecycle must be
recorded.

**Agent lifecycle events:**
- `agent.start`
- `agent.complete`
- `agent.fail`
- `agent.block`
- `agent.pause`
- `agent.resume`

Rationale: without agent lifecycle records, there is no way to audit what agents
ran, when they ran, or why they stopped.

**Budget hard stop:**
- `budget.hard_stop`
- `budget.resume`

Rationale: budget stops that halt agent execution must be recorded. These are
governance events, not operational logs.

### Phase 2 — Implement before cross-system interfaces go live

These must be in place before any cross-system signal delivery or evidence access
is operational.

- `signal.delivery` and `signal.delivery.confirmed` / `.failed`
- `signal.delivery.startup` (VEDA → V Forge)
- `evidence.query` (V Forge → VEDA)
- `evidence.request` (Project V → VEDA)
- `execution.return` and `execution.return.confirmed` / `.failed`
- `task.create`, `task.start`, `task.complete`, `task.fail`

### Phase 3 — Implement as workflows come online

Implement these when the corresponding workflows are built.

- Intake outcome events (`intake.defer`, `intake.hold`, `intake.reject`, `intake.close`)
- Observation workflow events (`observation.classify`, `observation.assess`, `observation.cycle`)
- Observatory scope change events (`observatory.scope_change.*`)
- Execution clarification and scope update events (stub interfaces)
- Handoff recall events (stub interface)
- Budget warning events (`budget.warning`, `budget.cost_event`)
- Agent heartbeat (`agent.heartbeat`)

### Phase 4 — Can wait

These are valid and governed but not blocking anything in an initial build.

- `system.startup`, `system.shutdown`, `system.error`, `system.recovery`
- `content.create`, `content.update`, `content.publish`
- `evidence.create`, `evidence.update`, `evidence.expire`
- `budget.cost_event` for below-threshold routine LLM calls

### What the Phase 1 build requires from infrastructure

- The `ecosystem.activity_trail` table and all indexes from Section 5
- A service-layer write helper that: generates `activity_id`, validates required
  fields, writes to the trail, catches write failures and routes to the dead-letter
  buffer, and is synchronous-but-non-blocking relative to the primary operation
- A dead-letter buffer (a simple table `ecosystem.activity_trail_dlq` with
  `payload JSONB, failed_at TIMESTAMPTZ, retry_count INT` is sufficient for Phase 1)
- No event bus required in Phase 1. Live event subscription can be added in a
  later pass using Postgres LISTEN/NOTIFY or a lightweight pub-sub layer on top
  of the trail table

---

## Constraints Reminder

- No new architectural patterns introduced here. This spec works with the existing
  single-Postgres / four-schema architecture.
- Qdrant is not referenced as a trail store. Qdrant is retrieval infrastructure.
- The `ecosystem` schema for the trail table is new. It requires a DB role with
  write access granted to all four system service roles. This is a deliberate
  cross-system write surface — the only one in the architecture.

  **This shared write surface requires explicit, deliberate setup. Do not treat
  it as a casual DB grant.** When implementing, the following must be handled
  intentionally and reviewed before any system goes to production:

  - A dedicated `ecosystem_trail_writer` DB role (or equivalent) with `INSERT`
    only on `ecosystem.activity_trail` and `ecosystem.activity_trail_dlq`. No
    `UPDATE`, no `DELETE`, no cross-schema read grants.
  - Each system service role (`project_v_service`, `veda_service`, `v_forge_service`,
    `veda_strategy_service`) is granted `ecosystem_trail_writer` and nothing else
    on the ecosystem schema. They must not receive broader ecosystem schema access
    through this grant path.
  - The trail write helper is the only code path that touches the ecosystem schema
    from any subsystem. Ad hoc queries and background jobs from subsystem services
    must not be granted access to the ecosystem schema on the basis that the trail
    write role exists.
  - Compaction and retention jobs run under a separate, more privileged role that
    is not granted to any subsystem service. That role is an ops/infrastructure
    concern, not a service-layer concern.

  The risk to manage is not malice — it is convenience. Once a shared write
  surface exists, the path of least resistance is to start using it for other
  cross-system reads or writes that feel harmless. The four-schema boundary
  discipline depends on this being the controlled exception, not the beginning
  of a pattern.
- This spec does not define the trail query API or the governance dashboard UI.
  Those belong in separate implementation docs.

---

## Related Docs

- `ecosystem/activity-trail-model.md` *(Tier 1 authority — read before this doc)*
- `ecosystem/activity-trail-integration-map.md` *(seam-to-action-type mapping)*
- `ecosystem/cross-system-access-governance.md`
- `governance/approval-mechanics-seam-model.md`
- `governance/agent-operating-doctrine.md`
