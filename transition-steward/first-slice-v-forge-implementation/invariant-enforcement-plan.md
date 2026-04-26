# Invariant Enforcement Plan

## 1. Purpose

This document translates doctrine-level invariants — drawn primarily from
`v-forge/system-invariants.md`, `ecosystem/cross-system-boundaries.md`,
`ecosystem/db-posture.md`, and `interfaces/data-boundaries.md` — into an
implementation-facing enforcement plan.

For each invariant it classifies where enforcement belongs, what can be checked
mechanically, and what must remain under human governance. It does not rewrite
invariants or invent new ones.

Read the authority docs before this document. This document is derivation from
them, not a replacement for them.

---

## 2. Status

Transition-steward implementation support spec.

Not canonical authority doctrine.
Not implementation code.
Not permission to rewrite or relax any invariant.

Load-bearing conclusions must be promoted into proper authority docs before
being treated as settled.

---

## 3. Enforcement Posture

### Invariants differ in enforceability

Some invariants map cleanly to DB constraints or API checks. Others describe
behavioral posture — how a system must respond under conditions — that no
constraint can verify. The enforcement plan must be honest about which is which.

### Not all doctrine should become DB constraints

A DB constraint enforces a structural condition at write time. It is always on,
costs nothing at query time, and fails atomically. It is the right tool for
invariants that are expressible as structural facts about data shape.

For invariants that describe behavioral intent ("V Forge must not drift toward
planning ownership"), DB constraints are the wrong tool. Attempting to encode
them as constraints produces fake certainty and blocks legitimate operations
without actually preventing the drift they describe.

### Three enforcement layers

**DB enforcement** — Postgres-level constraints, foreign keys, check constraints,
and schema-credential isolation. These enforce structural facts. They cannot be
reasoned around at runtime.

**API/service enforcement** — Service-layer checks that run before or after an
operation. These enforce rules that require runtime context — session identity,
project scope, approval record presence, packet validity. They are slightly softer
than DB constraints (they can be bypassed if someone reaches the DB directly)
but are the right layer for rules that need context.

**Audit/guardrail enforcement** — Monitoring queries, activity trail checks, and
admin-level assertions. These detect drift after it has occurred. They are not
prevention; they are detection. They are appropriate for behavioral invariants
that cannot be verified structurally.

**Human governance** — Invariants that describe posture, intent, or bounded
judgment. No code check can enforce that V Forge is not becoming a shadow planner.
Human review, doctrine docs, and LLM behavior contracts handle these.

### Over-enforcement is harmful

Encoding ambiguous or behavioral invariants as hard DB constraints creates problems:
- legitimate operations fail for spurious reasons
- engineers work around the constraints rather than through them
- the constraint creates a false sense of enforcement for something that was never
  actually verifiable structurally

Reserve hard enforcement for invariants that are genuinely structural. Accept
audit-and-review for the rest.

---

## 4. Invariant Classification

### DB enforce now

| Invariant | Source |
|---|---|
| Content graph records must be project-scoped | V Forge Invariant 8 |
| No cross-project graph connections (page-topic, page-entity, internal-link junctions) | V Forge Invariant 8 |
| Each schema owned by exactly one system; credentials scoped per schema | `db-posture.md` |
| No direct cross-schema writes from a system service role | `db-posture.md`, `data-boundaries.md` |
| `v_forge.*` tables must carry a non-null `project_id` for all content graph and execution records | V Forge Invariant 8, `data-boundaries.md` |
| Handoff identity must be unique and non-null; `activation_approval_ref` must be present | Packet schema + V Forge Invariant 9 |
| Publication continuity records must be written atomically with publication events | V Forge content execution module |

### API/service enforce now

| Invariant | Source |
|---|---|
| Activation API rejects Class B/C actions without a valid persisted approval record | `desktop-governance-and-gating-model.md` |
| Session token enforces project scope; no cross-project activation | `desktop-governance-and-gating-model.md` |
| Handoff package structural validity (required fields present, enums valid) | Packet schema drafting basis — Section A |
| Return-to-planning package structural validity | Packet schema drafting basis — Section B |
| Approval request package structural validity | Packet schema drafting basis — Section C |
| Execution only begins after handoff receipt confirmation is recorded | V Forge Invariant 6, handoff interface |
| V Forge service role cannot write to `project_v.*`, `veda.*`, or `veda_strategy.*` | `db-posture.md` credentials rule |
| Content graph record creation is blocked if `project_id` does not match the active session scope | V Forge Invariant 8 |
| Activity trail writes for fail-closed events (`approval.decide`, `approval.request`, `handoff.confirmed`) must succeed before primary operation completes | Activity trail implementation spec |

### Guardrail/audit enforce later

| Invariant | Source |
|---|---|
| Content graph is not accumulating VEDA signal records as canonical V Forge truth | V Forge Invariants 3, 5, 17 |
| `v_forge.*` is not storing Project V planning state as execution records | V Forge Invariant 16 |
| Evidence refs in handoff packages resolve to current non-stale VEDA records | V Forge Invariant 9 |
| Activity trail coverage for governed events (detect gaps in trail writes) | Activity trail implementation spec |
| No direct cross-schema SQL appearing in any system service's query logs | `db-posture.md` |
| Bounded analytical tool outputs are not accumulating as independent signal archives | Bounded analytical tools doctrine |
| Content graph records are not being pre-populated for planned-but-not-built assets | Content execution module |
| Publication continuity records exist for all publication events in a given project | Content execution module |

### Human governance only

| Invariant | Source |
|---|---|
| V Forge does not own planning truth (Invariant 4) | V Forge Invariants 4, 16 |
| V Forge does not become a shadow VEDA (Invariant 17) | V Forge Invariant 17 |
| Execution-side research remains bounded to approved scope (Invariant 7) | V Forge Invariant 7 |
| Return-to-planning does not collapse execution truth (Invariant 10) | V Forge Invariant 10 |
| Handoff scope descriptions are actually bounded, not vaguely worded | Packet schema — Section 6 |
| Readiness basis claims in handoffs are honest | Packet schema — Section 6 |
| Return-to-planning findings are genuinely execution-side, not disguised planning instructions | Packet schema — Section 6 |
| Analytical tool outputs are not being used as de facto approvals | Bounded analytical tools doctrine |
| V Forge reporting preserves material uncertainty rather than smoothing it | V Forge Invariant 12 |
| Failure does not justify boundary collapse (Invariant 18) | V Forge Invariant 18 |
| Human-in-the-loop remains real for launch-sensitive and paid actions (Invariant 15) | V Forge Invariant 15 |

---

## 5. Invariant-by-Invariant Enforcement Basis

---

### Invariant 8 — Content Graph Integrity Is Project-Scoped

**Why it matters:** Cross-project graph contamination means execution truth from
one project bleeds into another. This corrupts content graph accuracy, makes
execution intelligence unreliable, and violates the canonical ownership model.

**Enforcement layer:** DB primary; API/service secondary.

**Mechanism:**

At the DB layer: every content graph table in `v_forge.*` must carry a non-null
`project_id` column. Junction tables (page-topic, page-entity, internal-link)
must carry a `project_id` and have a CHECK constraint or enforced pattern that
prevents junctions across different `project_id` values. The simplest reliable
approach: carry `project_id` on the junction table and enforce that the referenced
records belong to the same project via a composite foreign key or DB trigger.

At the API/service layer: content graph record creation must validate that the
incoming `project_id` matches the session's active project scope before any write
proceeds. Reject mismatches; do not silently rewrite the `project_id`.

**What can be checked mechanically:**
- `project_id` NOT NULL on all content graph tables
- Junction table records where the referenced entities carry different `project_id` values
- Session token project scope vs. record `project_id` on write operations

**What cannot be checked mechanically:**
- Whether the content registered for a project actually belongs to it semantically
- Whether content is being duplicated across projects through a workaround pattern
  (two separate well-scoped records that represent the same content)

**Implementation notes:**
The composite foreign key approach is straightforward for PostgreSQL. For junction
tables, include `project_id` as a non-nullable column and add a CHECK or unique
constraint that enforces scope consistency. Add `project_id` columns to all
content graph tables in the first schema pass — retrofitting later is harder.

---

### Schema Credential Isolation (DB Posture)

**Why it matters:** Credential isolation is the primary enforcement mechanism for
the four-schema ownership model. Without it, "separate schemas" is a naming
convention, not a boundary.

**Enforcement layer:** DB configuration + deployment verification.

**Mechanism:**
Four separate DB roles, one per bounded system service. Each role has:
- `CONNECT` on the shared database
- `USAGE` on its own schema
- `SELECT`, `INSERT`, `UPDATE`, `DELETE` on its own schema's tables as appropriate
- No privileges on other systems' schemas

The `ecosystem_trail_writer` role described in the activity trail implementation
spec is a deliberate exception: `INSERT`-only on `ecosystem.activity_trail` and
`ecosystem.activity_trail_dlq`, granted to all four service roles. This is the
only cross-schema grant, and it is insert-only.

**What can be checked mechanically:**
Postgres `information_schema.role_table_grants` can be queried to verify no
service role has access to a schema it should not. This should be run as a
deployment-time verification check.

**What cannot be checked mechanically:**
Whether someone has added an ad-hoc superuser credential to the system that
bypasses role-based isolation. Deployment policy, not DB constraints, governs this.

**Implementation notes:**
Write a verification script that:
1. Connects as each service role
2. Attempts a trivial query against another system's schema
3. Verifies the query is rejected

Run this in CI as a deployment gate, not just as a one-time manual check. This
is the "verification rule" from `db-posture.md` made concrete.

---

### Activation API Requires Persisted Approval Record (Class B/C)

**Why it matters:** If the API does not enforce this, the entire approval gate
structure is theater. Conversational approval or UI-level soft checks are
insufficient — an engineer can always reach the API directly.

**Enforcement layer:** API/service.

**Mechanism:**
For every endpoint that activates a Class B or Class C action, the service layer
checks for the existence of a valid persisted approval record for the specific
`(action_type, entity_id, scope)` before executing the operation. If no valid
record exists, return a 403-class error with a structured response that identifies
the missing approval. The UI surfaces this error. There is no fallback.

For fail-closed approval events (`approval.decide`, `approval.request`,
`handoff.confirmed`), the activity trail write must succeed before the primary
operation is considered complete. The service layer does not return success until
the trail record exists.

**What can be checked mechanically:**
- Approval record presence and validity for the specific action scope
- Approval not expired, not revoked, not superseded
- Actor identity on the approval record matches a valid operator identity
- Approval covers the current action scope (not a stale or different-scope approval)

**What cannot be checked mechanically:**
- Whether the approval was granted with genuine understanding of the scope
- Whether the scope described in the approval record accurately covers the
  operation being activated
- Whether the approval class was correctly assigned

**Implementation notes:**
Implement as a service-layer middleware or decorator that runs before any Class B/C
activation handler. The check must query the `ecosystem.*` approval record table
(or equivalent), not trust a flag on the entity being activated. The approval record
is canonical; the entity flag is derived.

---

### Session Token Enforces Project Scope

**Why it matters:** Without this, the UI-level project scoping can be bypassed by
calling the API directly with a different project ID, causing cross-project
contamination.

**Enforcement layer:** API/service.

**Mechanism:**
The session token encodes the bound project ID. Every mutating API endpoint that
touches project-scoped records extracts the project ID from the session token and
validates it against the `project_id` in the request body or path. Mismatches are
rejected. The project ID in the session token is authoritative.

**What can be checked mechanically:**
- Session token project ID matches request body/path project ID
- No mutating operation proceeds against a project outside the session scope

**What cannot be checked mechanically:**
- Whether the session token was issued for the correct project in the first place
- Whether project scope was correctly set at session creation

---

### Handoff, Return, Approval, and Report Packet Structural Validity

**Why it matters:** Structurally invalid packets enter the system and produce
downstream failures that are harder to diagnose than a packet rejection at entry.

**Enforcement layer:** API/service (at packet receipt and at packet creation).

**Mechanism:**
Validate packet structure at the service layer both when a packet is created
(producing system) and when it is received (receiving system). The validation
schema is derived from the packet schema drafting basis (transition-steward doc).
Invalid packets are rejected with a structured error identifying which fields
failed. Do not silently accept partial packets and fill in defaults.

Key structural checks (from packet schema drafting basis):
- Handoff: `handoff_id` UUID, `activation_approval_ref` present and non-null,
  `target_system` enum must be `"v_forge"`, `return_to_planning_triggers` non-empty,
  `package_revision_posture` conditional on `prior_handoff_id`
- Return-to-planning: `finding_boundary_marker` must be `"bounded_execution_finding"`,
  `trigger_reason` must be in canonical enum, `execution_posture_at_return` enum enforced
- Approval request: `approval_class` never `"A"`, all five human-readable fields non-empty

**What can be checked mechanically:**
All structural constraints from packet schema drafting basis Section 5.

**What cannot be checked mechanically:**
All human-judgment fields from packet schema drafting basis Section 6 — scope
honesty, readiness basis truthfulness, finding characterization accuracy.

---

### Publication Continuity Records Written Atomically With Publication Events

**Why it matters:** A publication event without a continuity record means the
execution ledger does not reflect what was actually published. This breaks the
execution continuity invariant (Invariant 11).

**Enforcement layer:** DB (transaction) + API/service.

**Mechanism:**
Publication events and their continuity records must be written in the same
database transaction. If the transaction fails, both are rolled back — there is
no state where a publication event exists without its continuity record.

Implement as a single transactional write: insert the publication event record and
the publication continuity record together. Do not write them separately with
application-level retry logic that could leave them inconsistent.

**What can be checked mechanically:**
Within a transaction: both records exist or neither does.
As an audit query: detect publication event records in `v_forge.*` that lack
a corresponding continuity record (orphan detection).

**What cannot be checked mechanically:**
Whether the continuity record accurately describes what was published.

---

### V Forge Service Role Cannot Write to Other Systems' Schemas

**Why it matters:** This is the persistence-layer enforcement of the canonical
ownership model. If V Forge can write to `project_v.*` or `veda.*`, the
schema boundary is nominal, not real.

**Enforcement layer:** DB credentials (primary) + deployment verification.

**Mechanism:**
The `v_forge_service` DB role must not have `INSERT`, `UPDATE`, or `DELETE`
grants on `project_v.*`, `veda.*`, or `veda_strategy.*`. The only cross-schema
grant permitted is `ecosystem_trail_writer` (insert-only on the activity trail
table), as specified in the activity trail implementation spec.

This is enforced by the credential model, not by application code. Application
code that attempts a write to another schema will fail at the DB level, not at
the service layer.

**Verification:**
Run the credential verification script described in the Schema Credential Isolation
section. Include this in deployment CI.

---

### Invariants 4, 16, 17 — V Forge Must Not Drift Into Planning, Shadow-VEDA, Shadow-Project-V

**Why these matter:** These are the core identity invariants. If V Forge starts
accumulating planning records, storing signal archives, or recreating approval
state inside execution tooling, the role model is failing regardless of whether
individual records look structurally valid.

**Enforcement layer:** Human governance primary; audit/guardrail secondary.

**What can be checked mechanically (guardrail queries):**
- Is `v_forge.*` accumulating tables whose naming or content suggests planning
  state (roadmap tables, sequencing tables, orchestration state)?
- Is `v_forge.*` storing VEDA-originating records directly rather than bounded
  references with foreign IDs?
- Are content graph records being written for assets with no corresponding
  execution event (pre-populating planned-but-not-built assets)?
- Are there `v_forge.*` records that mirror columns from `project_v.*` beyond
  what is needed for handoff context?

**What cannot be checked mechanically:**
Whether the nature of V Forge's operation is drifting toward planning behavior.
A capable LLM operating in V Forge that starts making planning decisions is
violating these invariants regardless of how cleanly the data is structured.
This requires human review of V Forge sessions, doctrine docs, and the LLM
behavior contract.

---

### Invariants 7, 12 — Bounded Research and Boundary-Safe Reporting

**Why these matter:** Invariant 7 prevents V Forge from becoming an observatory
under the guise of execution-side research. Invariant 12 prevents V Forge reports
from quietly rewriting planning state. Both are identity invariants.

**Enforcement layer:** Human governance primary; bounded analytical tools doctrine
provides behavioral guardrails; activity trail provides after-the-fact visibility.

**What can be checked mechanically:**
The activity trail records what actions V Forge takes. A high volume of `evidence.query`
events relative to execution events is a signal worth reviewing. Research commands
that produce VEDA-scale signal volumes are detectable in aggregate.

**What cannot be checked mechanically:**
Whether any particular piece of research was "bounded to approved execution" or
"open-ended exploration." This requires human review of what the research was
for, not just that it occurred.

---

### Invariant 15 — Human-In-The-Loop Remains Real for Launch-Sensitive and Paid Actions

**Why it matters:** This is the meta-invariant for the approval model. If Class C
gates can be bypassed — conversationally, through delegation, through a weak
code check — governance becomes theater.

**Enforcement layer:** API/service enforcement for the gate; human governance for
whether the gate is being correctly used.

**What can be checked mechanically:**
The API activation enforcement described above (Class B/C approval record required)
is the mechanical layer. The API verifies the approval record exists. It cannot
verify that the approval was meaningful.

**What cannot be checked mechanically:**
Whether the approval was rubber-stamped, whether the operator understood what
they were approving, or whether the scope in the approval record accurately
reflects the action that followed.

---

## 6. First Enforcement Set

Implement in this order. Rationale follows each.

**1. Schema credential isolation + verification script**

This is the foundation of everything else. Without credential isolation, all
other boundary enforcement is advisory. Implement this first: four scoped
DB roles, the `ecosystem_trail_writer` cross-schema grant, and a CI-runnable
verification script that confirms no service role can reach another system's
schema. This should be in place before any application code is written.

**2. Project-scoped `project_id` on all `v_forge.*` content graph tables**

Include this in the first schema pass. Retrofitting `project_id` columns and
cross-project junction constraints after tables are populated is significantly
harder. Non-null `project_id`, composite foreign key or CHECK constraint on
junctions, and session-scope validation at the service layer. This enforces
Invariant 8 structurally and permanently.

**3. Activation API approval-record gate**

Implement before any Class B or C action goes to production. The service
middleware that checks for a persisted approval record before executing a
governed activation. This is the mechanical enforcement of the governance gate
model. Without it, the approval flow works in development and demos but is not
actually enforced.

**4. Packet structural validation at service layer**

Implement handoff and return-to-planning packet validation before the cross-system
interfaces go live. Validate at both creation and receipt. Specifically: the
`activation_approval_ref` presence check on handoffs, the `finding_boundary_marker`
fixed-value check on return packages, and the `approval_class != "A"` check on
approval request packages. These three checks catch the most governance-critical
structural errors.

**5. Publication continuity atomic writes**

Implement as part of the first content publication flow. Transactional write
of publication event + continuity record. This is a one-time implementation
decision that is trivially correct if done from the start and significantly
harder to retrofit.

**6. Activity trail fail-closed events**

Implement the fail-closed write behavior for `approval.decide`, `approval.request`,
and `handoff.confirmed` as defined in the activity trail implementation spec. These
three event types must succeed before their primary operations complete. Implement
alongside the approval-record gate.

---

## 7. Anti-Drift Rules

**Do not convert behavioral invariants into fake hard constraints.**
Invariants 4, 7, 12, 16, 17, and 18 describe operational posture. Attempting
to enforce "V Forge must not drift into planning ownership" as a DB constraint
will either block legitimate operations or produce a constraint that is trivially
satisfied while the drift continues unnoticed. These invariants belong in human
governance, LLM behavior contracts, and audit review — not in CHECK constraints.

**Do not enforce at the wrong layer.**
DB constraints run always, cost nothing, and are the right tool for structural
facts. Service-layer checks run per request, have context, and are the right
tool for rules requiring runtime state. Approval record checks belong at the
service layer, not in DB triggers (triggers do not have session context).
Project-scope checks belong in application code, not in CHECK constraints
(the DB does not know which project the current operator session is bound to).

**Do not confuse audit detection with prevention.**
A guardrail query that detects cross-project contamination after it occurred is
useful. It is not a substitute for the DB constraint that prevents it from occurring.
Run both, but be clear which one prevents and which one detects.

**Do not confuse packet structural validity with invariant satisfaction.**
A packet that passes the structural schema validator is correctly shaped. It may
still carry a readiness basis that is fabricated, an execution scope that is
vaguely worded, or a finding that is a planning instruction disguised as an
execution report. Structural validation does not satisfy Invariants 9, 10, or 12.
Make this distinction explicit in any code commentary on validation logic.

**Do not let schema credential isolation become the only enforcement.**
Credential isolation prevents direct cross-schema writes at the DB level. It does
not prevent a service from making API calls to another system's service that
cause writes. API-layer enforcement and interface governance are required in
addition to credential isolation.

**Do not encode doctrine ambiguities as fake enums.**
If a field's valid values are not yet fully settled — for example, signal
classification categories in the startup signal package — do not invent an enum
and claim it is governed. Use opaque JSONB or free-text with a note that the
structure is deferred until the relevant doctrine is settled. A premature enum
creates false confidence and will conflict with the settled vocabulary when it
arrives.

**Do not treat the first enforcement set as the complete set.**
The six items in Section 6 are the minimum to implement first. The full
enforcement surface includes audit queries, guardrail checks, activity trail
coverage monitoring, and ongoing human review. The first set prevents the most
critical structural failures. It does not prevent drift.

---

## 8. Recommended Next Move

**Immediate:** Run the schema credential verification now — before any application
code is written. Verify that each system's service role is correctly scoped to its
own schema and that cross-schema writes fail at the DB level. If this is not
already in place, establish it as the first infrastructure task.

**During first schema pass:** Add `project_id` non-null constraints and cross-project
junction guards to all `v_forge.*` content graph tables. Do not defer this to a
later migration.

**Before interfaces go live:** Implement the activation API approval-record gate
and the packet structural validation middleware. These are prerequisites for the
handoff and return-to-planning interfaces to be genuinely governed.

**Alongside the approval gate:** Implement fail-closed activity trail writes for
`approval.decide`, `approval.request`, and `handoff.confirmed`.

**After the first enforcement set is in place:** Write the credential verification
script as a CI check. Write the first set of audit queries for the guardrail/audit
class of invariants. Run them periodically and review results. Do not wait for
drift to become visible before establishing detection.

**Before V Forge operational use:** Review the bounded analytical tools and plugin
doctrine against whatever plugin/tool implementation is proposed. Verify that
no plugin is admitting forbidden inputs (direct provider signal ownership,
open-ended research) and that all outputs are correctly classified and routed
before the plugin is deployed.

---

## 9. Related Files

Authority docs this plan derives from:

- `v-forge/system-invariants.md`
- `v-forge/v-forge.md`
- `v-forge/operational-model.md`
- `v-forge/content-execution-module.md`
- `v-forge/bounded-analytical-tools-and-plugin-doctrine.md`
- `ecosystem/cross-system-boundaries.md`
- `ecosystem/db-posture.md`
- `interfaces/data-boundaries.md`
- `interfaces/desktop-governance-and-gating-model.md`
- `governance/approval-mechanics-seam-model.md`

Implementation-support context:

- `transition-steward/activity-trail-implementation-spec.md`
- `transition-steward/packet-schema-drafting-basis.md`
- `transition-steward/transition-plan.md`
