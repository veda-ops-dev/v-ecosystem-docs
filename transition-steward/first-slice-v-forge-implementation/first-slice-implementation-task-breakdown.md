# First Slice Implementation Task Breakdown

## 1. Purpose

This document decomposes the chosen first codable slice into concrete implementation
tasks with dependencies and acceptance criteria.

It does not redesign the slice. It translates `minimum-codable-first-slice.md`
into engineering-facing tasks a developer can pick up and execute.

---

## 2. Status

Transition-support implementation-planning doc only.
Not authority doctrine. Not implementation code.

---

## 3. Slice Restatement

The slice is: handoff acceptance + approval gate + activity trail, no content execution.

End-to-end path:
1. A structurally valid handoff package arrives at V Forge (from a test harness stub)
2. V Forge validates packet structure
3. V Forge verifies a persisted approval record exists for this handoff
4. V Forge writes `handoff.confirmed` to the activity trail (fail-closed)
5. V Forge stores a minimal handoff context record in `v_forge.*`
6. V Forge creates a task record and runs a synthetic agent through `pending -> active -> blocked`
7. Trail records are written for each governed event
8. V Forge writes a minimal execution report

Supporting infrastructure: four-schema Postgres with scoped roles, `ecosystem.activity_trail`
with DLQ, `ecosystem.approval_records`, activity trail write helper, packet validators,
approval record check middleware, session scope enforcement.

Explicitly excluded from this slice: content graph, VEDA signal, return-to-planning
delivery, content execution, desktop UI, provider dependencies, real agent autonomy.

---

## 4. Task Breakdown

Tasks are numbered in dependency order.

---

### T-01 — Postgres schema and role setup

**Why it exists:** Four-schema isolation is the foundation of all boundary enforcement.
No application code before credential isolation is in place.

**Dependencies:** None.

**Acceptance criteria:**
- Four schemas exist: `project_v`, `veda`, `veda_strategy`, `v_forge`, `ecosystem`
- Four service roles exist: `project_v_service`, `veda_service`, `veda_strategy_service`, `v_forge_service`
- Each role has USAGE on its own schema and SELECT/INSERT/UPDATE/DELETE on its own schema's tables only
- `ecosystem_trail_writer` role exists with INSERT-only on `ecosystem.activity_trail` and `ecosystem.activity_trail_dlq`
- All four service roles are granted `ecosystem_trail_writer`
- A credential verification script exists that connects as each role, attempts a trivial query against
  each other system's schema, and asserts all cross-schema queries are rejected
- Verification script exits non-zero on any failure and exits 0 on a correctly configured environment
- Script passes

---

### T-02 — `ecosystem.activity_trail` and DLQ tables

**Why it exists:** Trail writes cannot happen without the table. DLQ must exist before the write
helper can route failures.

**Dependencies:** T-01

**Acceptance criteria:**
- `ecosystem.activity_trail` created with all columns from activity trail implementation spec Section 5:
  `activity_id UUID PK`, `timestamp TIMESTAMPTZ NOT NULL`, `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`,
  `ecosystem_session_id UUID`, `parent_event_id UUID REFERENCES ecosystem.activity_trail(activity_id)`,
  `correlation_id UUID`,
  `actor_type TEXT NOT NULL CHECK (actor_type IN ('agent','operator','system'))`,
  `actor_id TEXT NOT NULL`, `actor_system TEXT NOT NULL`,
  `action TEXT NOT NULL`,
  `action_class TEXT NOT NULL CHECK (action_class IN ('state_change','cross_system_access','approval','budget','lifecycle'))`,
  `entity_type TEXT NOT NULL`, `entity_id TEXT NOT NULL`, `target_system TEXT`,
  `project_id UUID`, `company_id UUID`,
  `details JSONB NOT NULL DEFAULT '{}'`, `result_summary JSONB NOT NULL DEFAULT '{}'`,
  `token_cost INTEGER`, `api_cost_cents NUMERIC(10,4)`
- All six indexes from the spec created (project+time, actor, entity, session, action_class+time,
  correlation partial, approval partial)
- `ecosystem.activity_trail_dlq` created:
  `id BIGSERIAL PK`, `payload JSONB NOT NULL`, `failed_at TIMESTAMPTZ NOT NULL DEFAULT now()`,
  `retry_count INT NOT NULL DEFAULT 0`
- `ecosystem_trail_writer` has INSERT on both tables; no UPDATE, no DELETE

---

### T-03 — `ecosystem.approval_records` table (minimal)

**Why it exists:** The approval gate check queries this table. Must exist before the check
middleware can run.

**Dependencies:** T-01

**Acceptance criteria:**
- `ecosystem.approval_records` created:
  `approval_id UUID PK`, `entity_type TEXT NOT NULL`, `entity_id TEXT NOT NULL`,
  `approval_class TEXT NOT NULL CHECK (approval_class IN ('B','C','D'))`,
  `scope TEXT NOT NULL`, `actor_id TEXT NOT NULL`,
  `decision TEXT NOT NULL CHECK (decision IN ('approved','rejected','expired'))`,
  `expires_at TIMESTAMPTZ`, `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- Index on `(entity_type, entity_id, decision)`
- `project_v_service` has INSERT and SELECT (Project V writes approvals)
- `v_forge_service` has SELECT only (V Forge reads to verify, never writes)

---

### T-04 — `v_forge.*` minimal execution tables

**Why it exists:** V Forge needs three tables for the slice: handoff context, task, execution report.
All must carry non-null `project_id`.

**Dependencies:** T-01

**Acceptance criteria:**
- `v_forge.handoff_contexts` created:
  `handoff_id UUID PK`, `project_id UUID NOT NULL`, `execution_scope_id UUID NOT NULL`,
  `activation_approval_ref UUID NOT NULL`, `state TEXT NOT NULL`,
  `confirmed_at TIMESTAMPTZ`, `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- `v_forge.tasks` created:
  `task_id UUID PK`, `handoff_id UUID NOT NULL REFERENCES v_forge.handoff_contexts(handoff_id)`,
  `project_id UUID NOT NULL`, `state TEXT NOT NULL`, `block_reason TEXT`,
  `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`, `updated_at TIMESTAMPTZ`
- `v_forge.execution_reports` created:
  `report_id UUID PK`, `handoff_id UUID NOT NULL`, `project_id UUID NOT NULL`,
  `report_type TEXT NOT NULL`, `execution_state TEXT NOT NULL`, `basis TEXT NOT NULL`,
  `constraints_risks TEXT NOT NULL`, `required_next_step TEXT NOT NULL`,
  `reported_at TIMESTAMPTZ NOT NULL`
- `project_id` NOT NULL enforced at DB level on all three tables
- `v_forge_service` has SELECT/INSERT/UPDATE on all three; no other service role has write access

---

### T-05 — Activity trail write helper

**Why it exists:** Single code path for all trail writes. Enforces the fail-closed vs fail-open
distinction and routes failures to the DLQ.

**Dependencies:** T-02

**Acceptance criteria:**
- Accepts a record payload and a `fail_closed: boolean` parameter
- Generates `activity_id` UUID before the write attempt
- Validates required base fields present before attempting any DB write:
  `timestamp`, `actor_type`, `actor_id`, `actor_system`, `action`, `action_class`, `entity_type`, `entity_id`
- Writes to `ecosystem.activity_trail`
- Fail-closed path: if write fails for any reason, throws (does not return success),
  routes full payload to DLQ, logs at ERROR level
- Fail-open path: if write fails, routes to DLQ, does not throw, calling code continues
- Idempotency: duplicate `activity_id` on retry is a no-op (PK constraint); caller is
  responsible for passing the same ID on retry
- Unit tests: successful write, fail-closed failure (throws + DLQ), fail-open failure (no throw + DLQ),
  missing required field (validation error before DB), duplicate activity_id (no-op)

---

### T-06 — Handoff packet structural validator

**Why it exists:** Invalid packets must be rejected before any state is written. Pure logic, no DB.

**Dependencies:** None

**Acceptance criteria:**
The validator rejects — with a structured error naming the failing field — any packet where:
- `handoff_id` absent or not a valid UUID
- `correlation_id` absent or not a valid UUID
- `activation_approval_ref` absent or null
- `source_planning_entity_ref` absent or missing `ref_type` / `ref_id`
- `execution_scope_id` absent or not a valid UUID
- `approved_execution_scope` absent or empty string
- `target_system` absent or not exactly `"v_forge"`
- `execution_constraints` absent or empty object
- `readiness_basis` absent or empty string
- `evidence_refs` absent (empty array is acceptable if explicitly present)
- `expected_execution_objective` absent or empty string
- `return_to_planning_triggers` absent, not an array, or empty array
- `activation_timestamp` absent or not valid ISO 8601 UTC
- `package_revision_posture` absent or not in `["original","revision"]`
- `package_revision_posture = "revision"` and `prior_handoff_id` null or absent

Accepts a packet where all required fields are present and valid.

Unit tests: valid packet passes; each required field absent individually fails;
`prior_handoff_id` conditional; `target_system` enum violation; empty `return_to_planning_triggers`.

---

### T-07 — Approval record presence check middleware

**Why it exists:** Core governance gate. Runs at the service layer before any confirmation
state is written. Missing or invalid approval record must produce a clear structured error.

**Dependencies:** T-03

**Acceptance criteria:**
- Accepts `(entity_type, entity_id)` parameters
- Queries `ecosystem.approval_records` for `entity_type = 'handoff'`, `entity_id = handoff_id`,
  `decision = 'approved'`
- No record found: returns structured 403 `{ error: "APPROVAL_REQUIRED", entity_type, entity_id }`
- Record found but `expires_at` is non-null and in the past: returns 403 `{ detail: "approval record expired" }`
- Record found and valid: returns the record for use in the handler
- Unit tests: valid record present, no record, expired record, decision = 'rejected'

---

### T-08 — Session token project scope enforcement

**Why it exists:** Prevents cross-project activation. Session token's `project_id` is authoritative.

**Dependencies:** None (pure middleware logic)

**Acceptance criteria:**
- Every mutating endpoint in the slice extracts `project_id` from the session token
- Before any write, service validates `session.project_id == request.project_id` (or equivalent)
- Mismatch: 403 `{ error: "PROJECT_SCOPE_MISMATCH" }`
- Check runs in service layer, not UI layer
- Unit tests: matching project ID passes, mismatched ID rejected

---

### T-09 — Approval trail record pre-verification

**Why it exists:** Before confirming a handoff, `approval.request` and `approval.decide` trail records
must already exist. Fail-closed pre-check — absent records halt the operation.

**Dependencies:** T-02, T-05

**Acceptance criteria:**
- Handoff confirmation handler queries `ecosystem.activity_trail` for:
  - `approval.request` record with `entity_type = 'handoff'` and `entity_id = handoff_id`
  - `approval.decide` record with same entity fields and `details->>'decision' = 'approved'`
- Either absent: structured error `{ error: "TRAIL_PRECONDITION_FAILED", missing: [...] }`, no writes
- Both present: check passes, handler proceeds
- Unit tests: both present (passes), `approval.request` absent (halts), `approval.decide` absent (halts),
  `approval.decide` present but decision not `approved` (halts)

---

### T-10 — Handoff confirmation handler

**Why it exists:** The core of the slice. Sequences all checks and writes for a governed handoff confirmation.

**Dependencies:** T-04, T-05, T-06, T-07, T-08, T-09

**Acceptance criteria — happy path:**
1. Packet structural validation passes (T-06)
2. Session scope check passes (T-08)
3. Approval record presence check passes — valid approved record found (T-07)
4. Approval trail pre-verification passes — both records present (T-09)
5. `handoff.confirmed` trail record written fail-closed via write helper:
   `action = "handoff.confirmed"`, `action_class = "state_change"`,
   `entity_type = "handoff"`, `entity_id = handoff_id`,
   `actor_type = "system"`, `actor_system = "v_forge"`,
   `project_id` non-null, `correlation_id` from handoff package
   — write must succeed before step 6; if write fails, handler throws
6. `v_forge.handoff_contexts` record inserted: `state = "confirmed"`, `confirmed_at = now()`,
   `project_id` from session token
7. Handler returns success to caller

**Acceptance criteria — failure paths:**
- Packet validation failure: structured validation error, no DB writes
- Scope mismatch: 403, no DB writes
- Approval record missing: 403, no DB writes
- Trail pre-verification failure: structured error, no DB writes
- `handoff.confirmed` fail-closed write failure: handler throws, no state record written,
  payload in DLQ

---

### T-11 — Task creation and lifecycle handler

**Why it exists:** After handoff confirmed, V Forge creates a task and runs the synthetic agent
lifecycle to exercise `task.create`, `agent.start`, and `agent.block` trail writes.

**Dependencies:** T-04, T-05, T-10

**Acceptance criteria:**
- After successful handoff confirmation, task record inserted: `state = "pending"`,
  `project_id` non-null, `handoff_id` referencing confirmed handoff
- `task.create` trail record written fail-open: `action_class = "state_change"`,
  `entity_type = "task"`, `entity_id = task_id`, `project_id` non-null
- Task transitions to `"active"`; `agent.start` trail record written fail-open:
  `action_class = "lifecycle"`, `entity_type = "agent"`
- Task transitions to `"blocked"` with `block_reason = "proving_slice_halt"`;
  `agent.block` trail record written fail-open: `action_class = "lifecycle"`,
  `details` carries `block_reason`
- All state transitions reflected in `v_forge.tasks.updated_at`
- Unit tests: task created with correct `project_id`, lifecycle produces correct trail records,
  `project_id` NOT NULL enforced at DB level

---

### T-12 — Execution report writer

**Why it exists:** After governed halt, V Forge writes a minimal execution report
satisfying Invariants 11 and 12 for the slice.

**Dependencies:** T-04, T-11

**Acceptance criteria:**
- After `agent.block`, execution report inserted with:
  `report_type = "action_report"`, `execution_state = "blocked"`,
  `basis = "proving_slice_halt — no content execution performed"`,
  `constraints_risks` explicitly set (empty string acceptable, but field must be present and not null),
  `required_next_step = "return_to_planning or operator review"`,
  `project_id` non-null, `handoff_id` referencing confirmed handoff,
  `reported_at` set to current UTC
- Unit test: report written with all required non-null fields

---

### T-13 — Test harness: approval record seed and handoff package builder

**Why it exists:** The slice needs a valid approval record, prerequisite trail records, and a valid
handoff package before the confirmation handler runs. Test-only code — not in the production service path.

**Dependencies:** T-03, T-06

**Acceptance criteria:**
- Seed function creates a valid approval record in `ecosystem.approval_records`:
  `entity_type = "handoff"`, `decision = "approved"`, valid `actor_id`,
  `approval_class = "B"`, `expires_at = null`
- Seed function creates prerequisite trail records in `ecosystem.activity_trail`:
  `approval.request` and `approval.decide` with matching `entity_type = "handoff"` and `entity_id`
- Builder constructs a structurally valid handoff package:
  all required fields present, valid UUIDs, `target_system = "v_forge"`,
  `activation_approval_ref` matching the seeded approval record's `approval_id`
- Builder can optionally produce intentionally invalid packets for failure path tests
  (by omitting a specified field)
- Both seed functions and the builder are test-only; they do not exist in production code paths

---

### T-14 — Credential verification script

**Why it exists:** Makes schema credential isolation a testable claim, not a declaration.

**Dependencies:** T-01

**Acceptance criteria:**
- Connects as `project_v_service`, asserts cannot SELECT from `v_forge.*`, `veda.*`, `veda_strategy.*`
- Connects as `v_forge_service`, asserts cannot INSERT into `project_v.*`, `veda.*`, `veda_strategy.*`
- Connects as `v_forge_service`, asserts CAN INSERT into `ecosystem.activity_trail`
- Connects as `v_forge_service`, asserts CANNOT UPDATE or DELETE from `ecosystem.activity_trail`
- Script exits non-zero if any assertion fails; exits 0 on a correctly configured environment
- Runnable in CI without manual intervention

---

## 5. Suggested Task Order

```
T-01
  |-- T-02 -- T-05 --.
  |-- T-03 -- T-07 --+-- T-09 -- T-10 -- T-11 -- T-12
  |-- T-04 ----------'
  '-- T-14  (parallel after T-01)

T-06  (no DB dependency; parallel with DB setup)
T-08  (no DB dependency; parallel with DB setup)
T-13  (after T-03 and T-06; just before integration testing)
```

**In words:**
- T-01 always first — credential isolation before any application code
- T-02, T-03, T-04, T-14 in parallel after T-01
- T-06, T-08 written and unit-tested independent of DB
- T-05 requires T-02
- T-07 requires T-03
- T-09 requires T-02 and T-05
- T-10 is the integration point — requires T-04, T-05, T-06, T-07, T-08, T-09
- T-11 and T-12 follow T-10 in sequence
- T-13 built alongside or just before integration testing begins

---

## 6. Minimal Test Plan

### Unit tests (per task, no DB required unless noted)

**UT-01 — Handoff packet validator (T-06)**
~15 cases: valid packet passes; each required field absent fails with the field named;
`target_system` enum violation; empty `return_to_planning_triggers`; `prior_handoff_id`
conditional when revision.

**UT-02 — Approval record check middleware (T-07, DB or mock)**
4 cases: valid approved record present; no record (403); record expired (403);
decision = 'rejected' (403).

**UT-03 — Session scope check (T-08)**
2 cases: matching project ID passes; mismatched ID produces PROJECT_SCOPE_MISMATCH.

**UT-04 — Trail write helper (T-05, DB or mock)**
5 cases: successful write; required field absent (validation error, no DB attempt);
fail-closed DB failure (throws + DLQ); fail-open DB failure (no throw + DLQ);
duplicate activity_id (no-op).

**UT-05 — Approval trail pre-verification (T-09, DB or mock)**
4 cases: both records present (passes); `approval.request` absent (halts);
`approval.decide` absent (halts); `approval.decide` present but decision not 'approved' (halts).

### Integration tests (require T-01 through T-04 complete)

**IT-01 — Happy path: full confirmed handoff lifecycle**

Setup: seed approval record and prerequisite trail records (T-13); construct valid
handoff package (T-13); establish session with matching `project_id`.

Assert:
1. `handoff.confirmed` trail record written with correct fields
2. `v_forge.handoff_contexts` record exists with `state = "confirmed"`
3. `v_forge.tasks` record created with `state = "pending"`
4. Task lifecycle ran to `state = "blocked"`
5. `task.create`, `agent.start`, `agent.block` trail records written
6. `v_forge.execution_reports` record written with all required non-null fields
7. Query `ecosystem.activity_trail` by `entity_id = handoff_id`: exactly 6 records
   in order — `approval.request`, `approval.decide`, `handoff.confirmed`,
   `task.create`, `agent.start`, `agent.block`
8. All `project_id` fields non-null across all `v_forge.*` records

Pass criterion: all 8 assertions pass.

**IT-02 — Packet validation rejection**

Setup: handoff package with `activation_approval_ref` null.
Assert: 400-class structured error names `activation_approval_ref`;
no records written to `v_forge.*`; no `handoff.confirmed` in trail.

**IT-03 — Approval record missing rejection**

Setup: valid handoff package; no approval record seeded.
Assert: 403 with `APPROVAL_REQUIRED`; no records written to `v_forge.*`.

**IT-04 — Fail-closed trail write failure**

Setup: valid handoff, approval record present, approval trail records present.
Inject DB failure on the `handoff.confirmed` trail write.
Assert: handler throws; `v_forge.handoff_contexts` NOT written; payload in `activity_trail_dlq`.

**IT-05 — Project scope mismatch rejection**

Setup: valid handoff, approval record present; session `project_id` differs from handoff scope.
Assert: 403 with `PROJECT_SCOPE_MISMATCH`; no records written to `v_forge.*`.

**IT-06 — Approval trail pre-verification failure**

Setup: valid handoff, approval record present; `approval.decide` trail record NOT seeded.
Assert: `TRAIL_PRECONDITION_FAILED` error listing `approval.decide` as missing;
no `handoff.confirmed` written; no state written to `v_forge.*`.

### Credential isolation test

**CI-01 — Schema credential isolation**

Run T-14 credential verification script against the actual configured DB environment.
Pass criterion: script exits 0. All cross-schema access attempts rejected.
`ecosystem_trail_writer` INSERT grant confirmed working. UPDATE/DELETE on trail table rejected.

This test must pass before the slice is considered deployable. Passing unit tests
while credential isolation is unverified in the actual environment does not count.

---

## 7. Out of Scope

Do not pull these into this build:

- Content graph tables (`v_forge.pages`, `v_forge.topics`, `v_forge.entities`, junction tables)
- Content execution handlers
- Publication continuity records and publication events
- Return-to-planning package producer or delivery to Project V
- Real Project V service — the test harness stub is sufficient
- Desktop approval UI and gate widget
- VEDA signal interface, startup signal package receipt
- VEDA Strategy signal interface
- Any LLM calls
- External provider dependencies (Firecrawl, DataForSEO, GA4, etc.)
- Batch H work
- Activity trail compaction, retention jobs, live event subscription
- DLQ retry worker (DLQ table receives payloads; draining it is a later concern)
- Budget enforcement trail events
- `agent.heartbeat` trail events
- Agent autonomy beyond the synthetic halt in T-11

---

## 8. Anti-Drift Rules

**Do not add content-adjacent tables "for future convenience."**
`v_forge.pages` is not in scope. A stub added now becomes a partial implementation
with untested constraints. The slice proves governance on the handoff path. Content
execution is a next slice.

**Do not make the test harness a real Project V service.**
If intake workflow logic or planning state appears in the harness, stop. The harness
seeds records and builds packets. That is all it does.

**Do not skip trail writes in any test mode.**
IT-01 must verify all six trail records exist after the happy path. If trail writes
are conditionally disabled in tests, the integration tests prove nothing about trail
behavior. Every trail write runs in every integration test run.

**Do not soften the fail-closed throw.**
IT-04 specifically tests that a fail-closed write failure halts the operation and
leaves no partial state. If the throw is converted to a log-and-continue anywhere in
the codebase during development, IT-04 silently stops failing and the governance
property is lost. The fail-closed distinction must be real from the first commit.

**Do not expand the approval records table.**
The minimal schema in T-03 is sufficient for the slice. Approval workflow state,
delegation records, and approval class escalation logic belong in a later task.

**Do not treat CI-01 as optional.**
The slice is not complete until CI-01 passes in a running deployed environment.
Credential isolation that exists in migration files but has not been verified in
a running DB is not enforced.

**Do not write cross-schema SQL in `v_forge_service` application code.**
Even though credential isolation will reject it at the DB level, application code
should not rely on DB rejection as its first defense. No SQL referencing
`project_v.*`, `veda.*`, or `veda_strategy.*` in the V Forge service.

---

## 9. Recommended Next Move After Task Breakdown

**Immediate:** Begin T-01. Run CI-01 before writing any application code. The
credential isolation is the foundation — everything else is advisory without it.

**Parallel early work:** T-06 (packet validator) and T-08 (scope check) have no DB
dependency. Write and unit-test these in parallel with DB setup. T-13 (test harness)
can be drafted alongside T-06 and T-03.

**First integration test target:** IT-01 — the happy path. All fourteen tasks must
be complete before IT-01 can run. If IT-01 passes cleanly, run IT-02 through IT-06
as confirmatory tests.

**After all integration tests pass:** Deploy to a real environment (not just local),
run CI-01 in that environment, and do a human review of the trail replay output —
confirm the six events are present, correctly attributed, and in the right order.
This is the governance proof, not just a passing test suite.

**Second slice:** Once the first slice is verified end-to-end, the next slice is
return-to-planning: after the governed halt, V Forge produces a minimal return-to-planning
package, delivers it to the Project V stub, the stub confirms receipt with an
`execution.return.confirmed` trail record, and the return packet validator
(packet schema drafting basis Section B) is added. This exercises the second
major cross-system governance path on a proven foundation.

---

## 10. Related Files

- `transition-steward/minimum-codable-first-slice.md` — slice definition this breakdown implements
- `transition-steward/activity-trail-implementation-spec.md` — trail table schema, write helper, fail-closed rules
- `transition-steward/packet-schema-drafting-basis.md` — handoff and approval packet field specs
- `transition-steward/invariant-enforcement-plan.md` — enforcement layer assignments
- `interfaces/project-v-to-v-forge-handoff-interface.md` — handoff package semantic authority
- `interfaces/desktop-governance-and-gating-model.md` — approval gate and Class B/C enforcement doctrine
- `ecosystem/activity-trail-model.md` — action vocabulary and required fields
- `ecosystem/db-posture.md` — schema and credential isolation authority
- `governance/approval-mechanics-seam-model.md` — approval request/decide/escalate mechanics
- `v-forge/reporting-and-approval-model.md` — execution report requirements
