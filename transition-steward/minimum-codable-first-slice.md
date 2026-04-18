# Minimum Codable First Slice

## 1. Purpose

This document defines the smallest doctrine-aligned implementation slice that
can be built first in VedaOps — the one that proves governance works without
requiring the full system to exist.

It does not design the full system. It picks one real slice, defines its
boundaries precisely, and makes clear what it proves and what it does not.

Read the authority docs and the three prior implementation-support specs before
this document. This document builds on them.

---

## 2. Status

Transition-steward implementation-planning doc only.

Not authority doctrine.
Not implementation code.
Not a product roadmap.
Not promotion of any transition-support note into settled doctrine.

---

## 3. Candidate Slices Considered

### Candidate A — Schema and credential isolation only

Build the four-schema Postgres setup, scoped DB roles, the ecosystem trail
schema, and the credential verification script. Nothing runs above the DB layer.

**Assessment:** Necessary but not a slice on its own. It is infrastructure
setup, not a proving slice. It produces no observable governed behavior. Include
it as a prerequisite, not as the slice itself.

### Candidate B — Packet validation only (no handoff flow, no DB)

Build the handoff packet validator and approval request packet validator as
standalone service-layer functions with unit tests. No DB writes, no real
delivery, no approval gate.

**Assessment:** Testable and useful, but proves almost nothing about governance.
Packet validation detached from the approval gate and trail writes is just a
library function. It does not prove that the governance model is real.

### Candidate C — Handoff acceptance + approval gate + activity trail (no content execution)

Build the slice where:
- a handoff package arrives at V Forge
- it is structurally validated
- an approval request record is written (fail-closed)
- a human approval event is recorded
- V Forge confirms receipt (fail-closed trail write)
- V Forge transitions to `execution_active` state
- a task record is written to `v_forge.*`
- one activity trail record is produced for each governed event

No actual content execution. No VEDA signal. No content graph writes beyond a
minimal task record. No provider dependencies.

**Assessment:** This is the right slice. It is small, fully self-contained,
exercises the load-bearing governance path from handoff receipt through approval
to execution activation, and proves that the approval model, trail writes, and
packet validation all work end-to-end. See Section 4.

### Candidate D — Minimal content execution slice (includes content graph)

Build the handoff path plus actual content execution: a task executes, a content
record is written to the content graph, a publication continuity record is written
atomically with a publication event, and a return-to-planning package is produced
on failure.

**Assessment:** Too wide for a first slice. Content graph schema, publication
continuity, and the return-to-planning delivery path all need to work correctly.
Each adds real surface area. The right approach is to prove governance first
(Candidate C), then add content execution on top of a proven foundation.

### Candidate E — Return-to-planning only (no handoff, no approval gate)

Build only the return-to-planning package producer, the delivery path, and
Project V's receipt confirmation.

**Assessment:** This starts in the middle of the flow. Return-to-planning is
meaningless without an established handoff context. Cannot be a first slice.

---

## 4. Recommended First Slice

**Candidate C: Handoff acceptance + approval gate + activity trail, no content execution.**

### What starts the slice

A valid handoff package arrives at V Forge from Project V. The package is
structurally complete per the handoff packet schema (packet schema drafting
basis, Section A). It carries:
- a stable `handoff_id` (UUID)
- a non-null `activation_approval_ref` referencing a valid approval event record
- `target_system: "v_forge"`
- a non-empty `approved_execution_scope` string
- at least one `return_to_planning_triggers` entry
- `package_revision_posture: "original"`

For the proving slice, the handoff is constructed by a test harness or a minimal
Project V service stub. No real Project V planning workflow is required.

### What actions happen

1. **Handoff packet validation.** V Forge's service layer validates the incoming
   package against the structural schema. Missing or malformed fields produce a
   structured rejection response. The package is not stored if it fails validation.

2. **Approval record check.** The service layer queries the `ecosystem.*` approval
   record for the `activation_approval_ref` carried in the handoff. If no valid,
   non-expired approval record exists for this `handoff_id` and scope, the service
   returns a 403-class error. The handoff is not confirmed.

3. **Approval request trail write (fail-closed).** If the package is valid and the
   approval record exists, the `approval.request` trail record that initiated the
   approval must already exist (it was written when the approval request was
   generated). Verify it is present. If not present, surface the gap — do not
   proceed silently.

4. **Approval decision trail write (fail-closed).** The `approval.decide` trail
   record for this handoff must exist before the handoff is treated as active.
   If the trail write does not succeed, do not confirm the handoff.

5. **Handoff confirmed — receipt written.** V Forge writes a `handoff.confirmed`
   activity trail record (fail-closed). The record is written before the handoff
   state is updated to confirmed. If the write fails, the confirmation does not
   proceed.

6. **Handoff record stored in `v_forge.*`.** A minimal handoff context record is
   written to `v_forge.*`. It carries: `handoff_id`, `project_id`, `execution_scope_id`,
   `activation_approval_ref`, `state: "confirmed"`, `confirmed_at`. This is not
   a copy of the full handoff package; it is V Forge's local execution reference.

7. **Execution task record created.** A single task record is written to `v_forge.*`
   representing the top-level execution unit for the handed-off scope. Fields:
   `task_id` (UUID), `handoff_id`, `project_id`, `state: "pending"`, `created_at`.
   No content execution occurs at this point.

8. **Task created trail write.** `task.create` activity trail record is written.
   Action class: `state_change`. This is fail-open (not fail-closed).

9. **Agent start.** An `agent.start` lifecycle trail record is written when
   execution begins (or would begin). For the proving slice, the agent simply
   transitions the task to `state: "active"` and immediately to `state: "blocked"`
   with a `block_reason: "proving_slice_halt"` — no real execution occurs.

10. **Agent block + halt.** `agent.block` trail record written. Task record updated
    to `state: "blocked"`. This simulates the governed halt condition cleanly.

11. **Execution report written.** A minimal V Forge execution report record is
    written to `v_forge.*` capturing: what work was attempted (none — proving slice),
    current state (blocked), what triggered the block, and that no content execution
    occurred. This satisfies the reporting invariant without requiring real execution.

### What records are written

In `ecosystem.activity_trail`:
- `approval.request` (verified present, fail-closed)
- `approval.decide` (verified present, fail-closed)
- `handoff.confirmed` (written fail-closed by V Forge)
- `task.create` (written fail-open)
- `agent.start` (written fail-open)
- `agent.block` (written fail-open)

In `v_forge.*`:
- handoff context record (minimal, as described above)
- task record (with lifecycle state transitions)
- execution report record (minimal)

In `ecosystem.*`:
- approval request record (prerequisite, exists before the slice begins)
- approval decision record (prerequisite, exists before the slice begins)

### What validations occur

- Handoff packet structural validation (all required fields, enum conformance,
  `activation_approval_ref` non-null, `return_to_planning_triggers` non-empty)
- Approval record presence check (API/service layer, before confirmation)
- Session token project scope vs. handoff `project_id` (API/service layer)
- Fail-closed trail writes succeed before state transitions complete
  (for `approval.decide`, `approval.request` presence, `handoff.confirmed`)
- `project_id` non-null on all `v_forge.*` records written in the slice

### What success/failure states exist

**Success:** Handoff confirmed, task created in `pending → active → blocked` state,
six activity trail records written, execution report written. All validations pass.
The governed halt is clean and observable.

**Failure modes that must be visible (not silent):**
- Packet validation failure: structured error response identifying missing fields
- Approval record missing: 403-class error with approval gap identified
- Fail-closed trail write failure: operation halted, alert raised, no state
  transition until trail write recovers
- Project scope mismatch: rejection at API layer with clear error

---

## 5. In-Scope Components

### Database

- `ecosystem` schema: `activity_trail` table and `activity_trail_dlq` table
  (from activity trail implementation spec)
- `v_forge` schema: handoff context table, task table, execution report table
  (minimal, first-pass — not full content execution schema)
- `ecosystem` schema: approval records table (minimal: `approval_id`,
  `entity_type`, `entity_id`, `scope`, `actor_id`, `decision`, `expires_at`,
  `created_at`)
- Four scoped DB roles + `ecosystem_trail_writer` cross-schema grant
- Credential verification script

### Service layer

- Handoff packet structural validator (from packet schema drafting basis, Section A)
- Approval request packet structural validator (from packet schema drafting basis,
  Section C base fields only — no seam-specific additive fields required for
  the slice)
- Approval record presence check middleware (service layer, pre-activation)
- Session token project scope enforcement
- Activity trail write helper (from activity trail implementation spec):
  generates `activity_id`, validates required fields, writes, routes failures
  to DLQ, distinguishes fail-closed from fail-open behavior
- Handoff confirmation handler (runs the sequence in Section 4)
- Task creation and lifecycle transition handler (minimal)
- Execution report writer (minimal)

### Activity trail

Phase 1 events only (from activity trail implementation spec, Section 7):
- `approval.request` (presence verification)
- `approval.decide` (presence verification)
- `handoff.confirmed` (fail-closed write by V Forge)
- `agent.start`, `agent.block` (fail-open)
- `task.create` (fail-open)

### Test harness

- A minimal Project V stub that constructs a valid handoff package (no real
  Project V planning workflow)
- An approval record seed that creates the prerequisite approval event before
  the slice runs (simulates the operator approval that would have preceded delivery)
- Integration tests covering: valid handoff happy path, packet validation failure
  paths, missing approval record rejection, project scope mismatch rejection,
  fail-closed trail write behavior

---

## 6. Out-of-Scope Components

The following are explicitly excluded from this slice. Do not include them,
do not stub them in a way that implies they are partially built, and do not
treat their absence as a gap to fill before the slice can run.

**Content graph tables and operations.** No pages, topics, entities, internal
links, archetypes, or schema usage records. The content graph is a later slice.

**Content execution module.** No content creation, update, or publication.
No publication continuity records. The proving slice halts at task activation
without executing content work.

**VEDA signal and startup delivery.** No VEDA signal interface, no startup
signal package receipt, no evidence query. The slice is self-contained within
V Forge and does not require VEDA to be running.

**VEDA Strategy signal.** Stub interfaces only. Do not wire these in.

**Batch H provider-dependent work.** No Firecrawl, no DataForSEO, no external
provider calls of any kind. The slice has zero provider dependencies.

**Return-to-planning delivery.** The slice produces a governed halt and an
execution report, but does not initiate a return-to-planning package delivery
to Project V. That is a later slice.

**Plugin and analytical tool architecture.** No bounded analytical tools,
specialist agents, or plugin runtime.

**Project V service (real).** The slice uses a test harness stub for the
handoff origin. Project V does not need to be implemented.

**Full approval workflow UI.** The approval record is seeded by the test
harness. No desktop UI for approval is required for the proving slice.

**Agent autonomy and reasoning.** The proving slice uses a synthetic agent
that confirms the task, does minimal work, and halts cleanly. No LLM calls,
no tool invocations, no autonomous decision-making in the slice.

**Content graph junction constraints.** These are required in the final schema
but the content graph tables are not in scope for this slice. Add them when
the content graph slice is built.

**Compaction, retention, live event subscription.** All deferred. The trail
table exists and accepts inserts. No compaction job, no pub/sub.

---

## 7. Required Enforcement and Validation for the Slice

Derived from the invariant enforcement plan, applying only what the slice touches.

### Packet validation (service layer)

Handoff packet: `handoff_id` UUID format, `activation_approval_ref` non-null,
`target_system` enum must be `"v_forge"`, `return_to_planning_triggers` non-empty
array, `package_revision_posture` in `["original", "revision"]`, conditional check
that `prior_handoff_id` is present when `package_revision_posture = "revision"`.

Approval request packet (for the seeded approval record): `approval_class` not
`"A"`, five core human-readable fields non-empty.

### Approval record enforcement (service layer)

Before `handoff.confirmed` is written, the service must verify:
- an approval record exists for `(entity_type: "handoff", entity_id: handoff_id)`
- the record's `decision` is `"approved"`
- the record is not expired (`expires_at` null or in the future)

If any check fails: return 403, write nothing, raise alert.

### Activity trail fail-closed events

`approval.request` must exist before handoff confirmation proceeds.
`approval.decide` must exist before handoff confirmation proceeds.
`handoff.confirmed` must be written and confirmed before the handoff state
record is updated to `confirmed`.

Fail-closed behavior: if write fails, halt the operation, log to DLQ with
full payload, raise an observable alert. Do not silently proceed.

### Project scoping

`project_id` non-null on all `v_forge.*` records written in the slice.
Session token `project_id` validated against handoff package `project_id`
before any write. Mismatch produces a rejection, not a silent rewrite.

### Schema credential isolation

`v_forge_service` role must not be able to write to `project_v.*`, `veda.*`,
or `veda_strategy.*`. The `ecosystem_trail_writer` grant (INSERT-only on
`ecosystem.activity_trail` and `ecosystem.activity_trail_dlq`) is the only
permitted cross-schema write. Credential verification script must pass before
the slice is considered deployable.

---

## 8. What This Slice Proves

### What it proves

**The approval model is real, not theater.** A handoff without a valid approval
record is rejected at the API layer. The rejection is observable, not a warning.
This cannot be bypassed by conversational framing or UI soft checks because the
check runs in the service layer against the DB.

**Fail-closed trail writes actually block operations.** If `handoff.confirmed`
cannot be written, the handoff confirmation does not complete. The system
demonstrates that trail write failures surface as operational failures, not
silent gaps.

**Packet validation rejects malformed inputs at entry.** Invalid packets produce
structured rejections before any state is written. The validation is not just
a UI hint.

**Schema credential isolation is real.** The credential verification script
demonstrates that V Forge cannot write to other systems' schemas. The
`ecosystem_trail_writer` pattern is the only deliberate exception.

**Project scoping is enforced end-to-end.** `project_id` is non-null on all
written records, and the session token check prevents cross-project activation.

**The governance trail is coherent for one complete handoff lifecycle.** After
the slice runs successfully, querying `ecosystem.activity_trail` by `handoff_id`
produces a complete, ordered, attributable sequence of what happened.

### What it does not prove

**It does not prove content execution is correct.** No content is executed. The
content graph, publication continuity, and return-to-planning delivery path are
all untested.

**It does not prove VEDA signal integration works.** No signal is consumed. VEDA
is not involved.

**It does not prove the approval UI works.** The approval record is seeded by
the test harness. The desktop gating UI is not exercised.

**It does not prove agent autonomy is safe.** The agent is synthetic and halts
immediately. Autonomous execution behavior is not tested.

**It does not prove the return-to-planning path is functional.** The slice
produces a clean halt but does not deliver a return package to Project V.

---

## 9. Implementation Order Inside the Slice

Build in this order. Each step must be complete and passing before the next begins.

**Step 1 — DB foundation**
- Create the four schemas and four scoped service roles
- Create `ecosystem_trail_writer` role with INSERT-only on `ecosystem.activity_trail`
  and `ecosystem.activity_trail_dlq`
- Create `ecosystem.activity_trail` table and `ecosystem.activity_trail_dlq` table
  (schema from activity trail implementation spec, Section 5)
- Create minimal `ecosystem.approval_records` table
- Write and run credential verification script — must pass before Step 2

**Step 2 — `v_forge.*` minimal schema**
- Create `v_forge.handoff_contexts` table:
  `handoff_id UUID PK, project_id UUID NOT NULL, execution_scope_id UUID NOT NULL,`
  `activation_approval_ref UUID NOT NULL, state TEXT NOT NULL, confirmed_at TIMESTAMPTZ,`
  `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`
- Create `v_forge.tasks` table:
  `task_id UUID PK, handoff_id UUID NOT NULL REFERENCES v_forge.handoff_contexts,`
  `project_id UUID NOT NULL, state TEXT NOT NULL, block_reason TEXT,`
  `created_at TIMESTAMPTZ NOT NULL DEFAULT now(), updated_at TIMESTAMPTZ`
- Create `v_forge.execution_reports` table (minimal):
  `report_id UUID PK, handoff_id UUID NOT NULL, project_id UUID NOT NULL,`
  `report_type TEXT NOT NULL, execution_state TEXT NOT NULL, basis TEXT NOT NULL,`
  `constraints_risks TEXT NOT NULL, required_next_step TEXT NOT NULL,`
  `reported_at TIMESTAMPTZ NOT NULL`
- Verify `project_id` NOT NULL on all three tables

**Step 3 — Activity trail write helper**
- Implement the write helper as described in the activity trail implementation
  spec: generates `activity_id`, validates required base fields, writes to
  `ecosystem.activity_trail`, catches failures and routes to DLQ
- Implement fail-closed vs fail-open distinction in the helper
- Unit test: successful write, DLQ routing on failure, fail-closed halt behavior

**Step 4 — Packet validators**
- Implement handoff packet structural validator (from packet schema drafting
  basis Section A constraints)
- Implement approval request packet validator (base fields only)
- Unit test each validator against valid packets, packets with missing required
  fields, packets with enum violations, and the `prior_handoff_id` conditional

**Step 5 — Approval record check middleware**
- Implement the service-layer approval record presence check
- Unit test: approved record present, record missing, record expired, record
  for wrong scope

**Step 6 — Handoff confirmation handler**
- Implement the full handoff confirmation sequence from Section 4
- Integration test: happy path (all validations pass, all trail writes succeed),
  packet validation failure, approval record missing, fail-closed trail write
  failure simulated

**Step 7 — Task and agent lifecycle**
- Implement task creation and `pending → active → blocked` transition
- Implement `task.create`, `agent.start`, `agent.block` trail writes (fail-open)
- Integration test: task lifecycle runs to governed halt, trail records are
  present and correctly attributed

**Step 8 — Execution report writer**
- Implement minimal execution report write at halt
- Integration test: report is written with correct fields, `project_id` non-null

**Step 9 — End-to-end integration test**
- Run the full slice: seed approval records, deliver handoff package, confirm
  receipt, activate execution, trigger governed halt, inspect all trail records
- Verify trail replay: query by `handoff_id`, confirm ordered sequence of six
  expected trail events

---

## 10. Anti-Drift Rules

**Do not widen into content execution while building this slice.**
The temptation will be to add content graph tables "while we're in the schema
anyway" or to add a real task execution step "just to see if it works." Resist
this. The slice proves governance. Content execution is a later slice built on
a proven foundation.

**Do not add provider-backed dependencies.**
No Firecrawl. No DataForSEO. No external API calls. If a component in the
slice seems to need external data to run, that component is out of scope for
this slice. The slice must run entirely on local infrastructure.

**Do not skip trail writes temporarily.**
Trail writes that are omitted "temporarily" during development become trail
writes that are omitted permanently. Every governed event in the slice must
write its trail record from the first integration test run. The trail is not
a feature added at the end.

**Do not relax the approval record gate for development convenience.**
It is tempting to comment out the approval record check to make development
faster. Do not. The check is the most important thing the slice proves. If
the gate is commented out, the slice proves nothing. Use the test harness to
seed approval records — do not bypass the gate.

**Do not treat the test harness stub as a real Project V service.**
The stub constructs a valid handoff package. It is not Project V. Do not add
planning workflow, intake logic, or readiness evaluation to the stub. It is
a thin packet producer, nothing more.

**Do not add the return-to-planning delivery path to this slice.**
The slice ends at a governed halt with an execution report. It does not deliver
a return package to Project V. Adding the return delivery path means also building
Project V's receipt confirmation, which means also building the cross-system
delivery infrastructure. That is a different slice.

**Do not add the desktop approval UI to this slice.**
The approval record is seeded by the test harness. Building the approval UI would
require the desktop application, the session surface, and the gate widget. That
is a different slice. Prove the API gate first, then add the UI on top.

**Do not treat the proving slice as production-ready.**
The synthetic agent halts immediately. The execution report is minimal. The
approval record is seeded, not operator-produced. This is a proving slice, not
a release. It demonstrates that the governance model is real and codable. It is
not a deployable product.

---

## 11. Recommended Next Move After the Slice

Once the first slice is working and all integration tests pass:

**Verify the governance claims are real.** Before building anything else, run
the credential verification script in CI, confirm the trail replay query returns
the correct ordered sequence, and confirm the approval gate rejects without a
valid record. Do not proceed until these are verified in a running environment,
not just passing in unit tests.

**Build the return-to-planning slice.** The natural next slice is: after the
governed halt, V Forge produces a minimal return-to-planning package, delivers
it to Project V (stub), and Project V writes a `execution.return.confirmed`
trail record. This exercises the second major cross-system path and adds the
return package validator from the packet schema drafting basis (Section B).

**Add the desktop approval gate.** After the API gate is proven, add the
desktop-side approval UI on top of it. The UI calls the same API. The gate
behavior is the same. The UI makes it operator-usable rather than
test-harness-driven.

**Add the minimal content graph.** After the return path works, add the content
graph tables (`v_forge.pages`, `v_forge.topics`, minimal content graph) with
`project_id` non-null and cross-project junction guards. This enables the content
execution slice to be built on top.

Do not jump to content execution, VEDA signal, or the full product before the
above sequence is working. Each next slice should build on a proven foundation,
not race ahead.

---

## 12. Related Files

Authority docs this slice derives from:

- `v-forge/operational-model.md`
- `v-forge/system-invariants.md`
- `interfaces/project-v-to-v-forge-handoff-interface.md`
- `interfaces/desktop-governance-and-gating-model.md`
- `v-forge/reporting-and-approval-model.md`
- `ecosystem/db-posture.md`
- `ecosystem/activity-trail-model.md`
- `governance/approval-mechanics-seam-model.md`
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md`

Implementation-support context:

- `transition-steward/activity-trail-implementation-spec.md`
- `transition-steward/packet-schema-drafting-basis.md`
- `transition-steward/invariant-enforcement-plan.md`
- `transition-steward/transition-plan.md`
