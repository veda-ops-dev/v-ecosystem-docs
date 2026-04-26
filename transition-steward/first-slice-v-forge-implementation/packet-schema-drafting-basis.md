# Packet Schema Drafting Basis

## 1. Purpose

This document translates the V Ecosystem's existing semantic packet doctrine into
machine-checkable structural schema guidance.

It does not redefine packet semantics. Those are settled in the Tier 1 and Tier 2
authority documents. This document answers the implementation question: for each
packet family, what can be structurally enforced by a schema validator, what must
remain human-judged, and in what order should validation be built?

Read the relevant authority docs before this document. This document is derivation
from them, not a replacement for them.

---

## 2. Status

Transition-steward implementation support spec.

Not canonical authority doctrine.
Not implementation code.
Not a packet redesign.
Not promotion of any field definitions beyond what the source docs already define.

Load-bearing conclusions must be promoted into proper authority docs before
being treated as settled.

---

## 3. Packet Maturity Classification

### Schema now — mature enough for structural schema work immediately

**A. Project V → V Forge handoff package**
Source: `interfaces/project-v-to-v-forge-handoff-interface.md`

The required semantic fields are explicitly enumerated in the interface doc.
The validity conditions are explicit. The field names and types are stable enough
to produce a structural schema. This is the most mature packet in the repo.

**B. V Forge → Project V return-to-planning package**
Source: `interfaces/v-forge-to-project-v-return-to-planning-interface.md`

Required semantic fields are explicitly enumerated. Validity conditions are explicit.
Trigger-reason categories are bounded and named. The finding-report boundary rule is
precise. Close to the handoff package in maturity.

**C. Approval request package**
Source: `governance/approval-mechanics-seam-model.md`, `interfaces/desktop-governance-and-gating-model.md`

Required semantic contents are explicitly enumerated in the seam model (Section 2 —
Shared Mechanics Pattern). The approval class taxonomy, pending-state vocabulary, and
decision outcome set are canonical and stable. The package shape is seam-independent;
seam-specific fields are additive on top of the shared base.

**D. Governed report package (execution report basis)**
Source: `governance/report-structure-and-required-fields.md`, `v-forge/reporting-and-approval-model.md`

The eleven required field categories are explicitly named in the report structure doc.
The report-type taxonomy is named. Sufficiency criteria are explicit. This is stable
enough for a structural base schema; the V Forge-specific variant adds minimal
execution-specific required fields on top of the shared base.

### Schema later — useful but not yet specific enough

**E. VEDA → V Forge startup signal package**
Source: `interfaces/veda-to-v-forge-signal-interface.md`

Required semantic fields are named and meaningful. However, the `bounded_signal_findings`
field — the actual signal content of the package — is not yet defined at a structural
level. VEDA's schema families for signal content are deferred-but-owned (per transition
plan Batch H). A structural schema for the envelope is achievable now; a schema for
the contents cannot be finalized until the signal content families are governed. Schema
the envelope. Mark the content fields as opaque or `JSONB` for now.

**F. Project V → VEDA evidence request**
Source: `interfaces/project-v-to-veda-evidence-request-interface.md`

The request envelope fields are well-defined: request identity, planning context ref,
bounded planning question, workflow stage, freshness requirement, urgency posture.
These can be schematized now. However, the response leg is governed by a separate
interface and VEDA's curation logic is explicitly out of scope. Schema the request
envelope. The response side is governed by the signal delivery interface.

### Do not schema yet — semantics too incomplete or unstable

**G. VEDA Strategy → Project V signal package**
Source: `interfaces/veda-strategy-to-project-v-signal-interface.md`

Governed stub only. Package field specifications are explicitly deferred to Batch K.
The boundary and ownership rules are settled but the package contents are not.
No structural schema work until the full interface contract exists.

**H. VEDA Strategy → V Forge signal package**
Source: `interfaces/veda-strategy-to-v-forge-signal-interface.md`

Same status as the VEDA Strategy → Project V interface. Governed stub, Batch K
deferred. Do not schema yet.

---

## 4. Structural Schema Posture

### What structural schemas are for

Structural schemas answer the question: is this packet shaped correctly to be
processed? They enforce presence and type of required fields, constrain enum-like
vocabularies to known values, and prevent obviously malformed packets from entering
system boundaries.

Structural schemas make the following detectable automatically:

- missing required fields
- field type violations (e.g., a UUID field receiving a free-text string)
- enum vocabulary violations (e.g., an unknown trigger reason type)
- presence of structurally forbidden field combinations where expressible

### What structural schemas are not for

Structural schemas cannot detect:

- whether the content of a field is honest
- whether a readiness basis is actually sufficient
- whether the bounded planning question is genuinely bounded or is effectively
  a request for raw observatory access
- whether an approval request accurately represents the scope being authorized
- whether execution findings are execution-side in nature or are disguised
  planning instructions
- whether a handoff scope is actually bounded vs. vague
- whether the execution posture stated in a return package is accurate

A packet that passes schema validation is structurally valid. It is not semantically
honest. Schema validation and semantic sufficiency are not the same thing.

### Structural validity vs. semantic truth

This distinction must be enforced in every layer that touches packets.

A validator that reports `VALID` means: the packet is shaped correctly and all
required fields are present with the right types.

It does not mean: the packet's claims are true, its basis is sufficient, or its
contents satisfy the governance requirements of the receiving system.

The governance docs define semantic sufficiency. Schema validators enforce structure.
Both are required. Neither replaces the other.

### Passing schema is not a governance gate

The fact that a packet passes structural validation must not be used as a substitute
for human review of approval-sensitive actions. Structural validation is a first-pass
filter, not a governance clearance.

---

## 5. Packet-by-Packet Schema Drafting Basis

---

### A. Project V → V Forge Handoff Package

**Purpose:** Transfers execution responsibility from Project V to V Forge for an
approved bounded scope. The three phases — activation approval, push delivery, and
receipt confirmation — are distinct. The package governs the delivery phase.

**Required fields**

| Field | Type | Notes |
|---|---|---|
| `handoff_id` | UUID | Stable across re-delivery attempts |
| `correlation_id` | UUID | For delivery chain linkage in activity trail |
| `source_planning_entity_ref` | `{ref_type: string, ref_id: UUID}` | Reference to the Project V planning entity (objective, initiative, or work item) |
| `execution_scope_id` | UUID | Identifies the bounded execution scope being transferred |
| `approved_execution_scope` | string (non-empty) | Bounded description — see semantic note below |
| `target_system` | enum: `["v_forge"]` | Must be explicit |
| `execution_constraints` | object (structured, non-empty) | At minimum: `{cost_bound?: ..., external_action_limits?: ..., launch_conditions?: ...}` |
| `readiness_basis` | string (non-empty) | Why handoff is valid now |
| `evidence_refs` | array of `{ref_type: string, ref_id: UUID}` | Bounded references, not embedded payloads |
| `expected_execution_objective` | string (non-empty) | Planning-side objective; not a detailed spec |
| `return_to_planning_triggers` | array of string (non-empty) | At least one trigger condition required |
| `activation_timestamp` | ISO 8601 UTC datetime | When Project V activated this handoff |
| `package_revision_posture` | enum: `["original", "revision"]` | |
| `prior_handoff_id` | UUID or null | Required when `package_revision_posture = "revision"` |
| `activation_approval_ref` | UUID | Reference to the approval event record |

**Optional fields**

| Field | Type | Notes |
|---|---|---|
| `urgency_posture` | enum: `["standard", "time_sensitive"]` | |
| `launch_sensitivity` | enum: `["standard", "launch_sensitive"]` | |

**Structural constraints**

- `handoff_id` must be present and non-null. UUID format enforced.
- `approved_execution_scope` must be a non-empty string. The scope cannot be an empty
  string or whitespace. Structural validation cannot enforce that the scope is
  meaningfully bounded (see Section 6).
- `evidence_refs` may be an empty array only if `readiness_basis` explicitly states
  the basis does not depend on external evidence. In practice, expect non-empty.
- When `package_revision_posture = "revision"`, `prior_handoff_id` must not be null.
- `return_to_planning_triggers` must contain at least one non-empty string.
- `activation_approval_ref` must be present. A handoff without an approval reference
  is structurally invalid.

**What can be checked structurally**
- All required fields present
- UUID format on identity fields
- Enum conformance on `target_system`, `package_revision_posture`, `launch_sensitivity`
- Non-empty string enforcement on `approved_execution_scope`, `readiness_basis`,
  `expected_execution_objective`
- Array non-empty on `return_to_planning_triggers`
- Conditional: `prior_handoff_id` required when `package_revision_posture = "revision"`

**What cannot be checked structurally**
- Whether the execution scope is actually bounded vs. vaguely worded
- Whether the readiness basis is honest or fabricated
- Whether the evidence refs resolve to current, non-stale records
- Whether the activation approval covers the actual scope
- Whether constraints are sufficient for the work being handed off

---

### B. V Forge → Project V Return-to-Planning Package

**Purpose:** Transfers bounded execution findings from V Forge to Project V when
execution cannot continue or requires planning reconsideration. Findings are
execution-side reports, not planning instructions.

**Required fields**

| Field | Type | Notes |
|---|---|---|
| `return_package_id` | UUID | Stable across re-delivery attempts |
| `correlation_id` | UUID | For delivery chain linkage |
| `originating_handoff_id` | UUID | Ties return to its governed handoff origin |
| `trigger_reason` | enum (see below) | Explicit trigger category required |
| `execution_posture_at_return` | enum (see below) | Current V Forge execution state |
| `bounded_finding_summary` | string (non-empty) | Execution-side finding — not a planning instruction |
| `scope_completed` | string | What portion of the scope was completed |
| `scope_not_completed` | string | What remains incomplete |
| `blockers_or_constraints` | array of string | Specific blocking conditions; non-empty when trigger_reason is `blocked` or `failed` |
| `planning_concern_implicated` | string (non-empty) | What planning aspect the finding speaks to |
| `evidence_basis` | array of `{ref_type: string, ref_id: UUID}` | Execution-side provenance |
| `condition_observed_at` | ISO 8601 UTC datetime | When the triggering condition was observed |
| `finding_boundary_marker` | enum: `["bounded_execution_finding"]` | Explicit contract marker — must always be this value |
| `package_revision_posture` | enum: `["original", "revision"]` | |
| `prior_package_id` | UUID or null | Required when `package_revision_posture = "revision"` |

**trigger_reason enum values** (from interface validity conditions):
```
"blocked_cannot_proceed"
"failed_affects_planning_basis"
"incomplete_requires_planning_choice"
"changed_conditions_invalidate_assumptions"
"findings_require_planning_reconsideration"
```

**execution_posture_at_return enum values** (from integration map):
```
"halted"
"paused"
"completed_bounded"
"continuing_degraded"
```

**Optional fields**

| Field | Type | Notes |
|---|---|---|
| `urgency_posture` | enum: `["standard", "time_sensitive"]` | |
| `partial_output_refs` | array of `{ref_type: string, ref_id: UUID}` | References to any partial work artifacts produced |

**Structural constraints**

- `finding_boundary_marker` must always be `"bounded_execution_finding"`. Fixed value.
- When `trigger_reason` is `"blocked_cannot_proceed"` or `"failed_affects_planning_basis"`,
  `blockers_or_constraints` must be non-empty.
- When `package_revision_posture = "revision"`, `prior_package_id` must not be null.
- `evidence_basis` may be empty for findings that are fully execution-observable
  without external reference, but empty is a weak signal and should be flagged in review.

**What can be checked structurally**
- All required fields present
- UUID format on identity fields
- Enum conformance on `trigger_reason`, `execution_posture_at_return`,
  `finding_boundary_marker`, `package_revision_posture`
- Non-empty string on `bounded_finding_summary`, `planning_concern_implicated`
- Conditional: `blockers_or_constraints` non-empty for blocking/failure trigger reasons
- Conditional: `prior_package_id` required when revision

**What cannot be checked structurally**
- Whether the finding is genuinely execution-side or is a disguised planning instruction
- Whether `planning_concern_implicated` accurately describes what the finding implicates
- Whether the evidence basis resolves to real execution-side provenance
- Whether `scope_completed` and `scope_not_completed` are honest
- Whether the trigger reason is correctly categorized vs. misrepresenting a planning-side desire

---

### C. Approval Request Package

**Purpose:** Requests human operator approval for a Class B or Class C governed
action. The base package shape is seam-independent; each seam adds required fields
on top of the shared base.

**Base required fields** (apply to all approval request packages, all seams)

| Field | Type | Notes |
|---|---|---|
| `approval_request_id` | UUID | Stable identifier for this request |
| `correlation_id` | UUID | Links to the governed transition being approved |
| `requesting_system` | enum: `["project_v", "v_forge", "veda", "veda_strategy", "ecosystem"]` | |
| `approval_class` | enum: `["B", "C", "D"]` | Class A does not require approval |
| `action_or_transition_requested` | string (non-empty) | What specific transition is proposed |
| `workflow_stage_context` | string (non-empty) | Which workflow stage and system context |
| `scope` | string (non-empty) | What the approval would cover |
| `why_approval_needed` | string (non-empty) | Which class applies and why human review is required |
| `relevant_risks_or_conditions` | string | What the reviewer needs to know |
| `if_approved_outcome` | string (non-empty) | What proceeds and what state changes |
| `if_rejected_outcome` | string (non-empty) | Fallback path or stop condition |
| `if_escalated_outcome` | string (non-empty) | Escalation path |
| `requested_at` | ISO 8601 UTC datetime | |
| `requesting_actor_id` | string (non-empty) | Actor that generated the request |

**Seam-specific additive fields** — carry the entity reference from the integration
map for the relevant seam (e.g., `handoff_id` for handoff activation, `return_package_id`
for return-to-planning review, `launch_authorization_scope_id` for launch authorization).
These are not defined exhaustively here; each seam's activity trail mapping defines the
minimum additional fields required.

**Structural constraints**

- `approval_class` must be `"B"`, `"C"`, or `"D"`. Never `"A"` — Class A does not
  produce approval request packages.
- `action_or_transition_requested`, `scope`, `if_approved_outcome`, and
  `if_rejected_outcome` must be non-empty strings. These are the minimum readable
  fields for a reviewer. Empty strings are structurally invalid.
- `why_approval_needed` must be non-empty. A request that cannot state why it
  requires review is not a valid approval request.

**What can be checked structurally**
- All base required fields present
- UUID format on `approval_request_id` and `correlation_id`
- Enum conformance on `requesting_system`, `approval_class`
- Non-empty string enforcement on the five human-readable fields
- Datetime format on `requested_at`
- Seam-specific entity reference present (when known at schema level)

**What cannot be checked structurally**
- Whether the stated scope accurately represents what the approval covers
- Whether `if_approved_outcome` honestly describes what will actually proceed
- Whether the approval class is correctly assigned (a Class C action submitted
  as Class B passes schema but fails governance)
- Whether the action description buries the real action in vague language
- Whether the request is being generated before or after the transition has
  already informally begun

---

### D. Governed Report Package (V Forge execution report variant)

**Purpose:** Reports a governed execution outcome, finding, request, or no-action
inside V Forge. The base structure applies across all systems; the V Forge variant
adds execution-specific required fields.

**Base required fields** (from `governance/report-structure-and-required-fields.md`)

| Field | Type | Notes |
|---|---|---|
| `report_id` | UUID | |
| `report_type` | enum (see below) | |
| `system_context` | enum: `["project_v", "veda", "v_forge", "veda_strategy", "ecosystem"]` | |
| `actor_context` | string (non-empty) | Who or what produced the report |
| `workflow_or_interface_context` | string | Which workflow stage or interface; may be empty for system-level reports |
| `subject` | string (non-empty) | What the report is about |
| `action_or_outcome` | string (non-empty) | What happened, was requested, or was found |
| `basis` | string (non-empty) | Why the action or outcome is appropriate |
| `approval_or_governance_posture` | enum (see below) | |
| `status` | enum (see below) | |
| `constraints_risks_uncertainties` | string | Empty string if none; must be stated explicitly, not omitted |
| `required_next_step` | string | Empty string if no follow-up required |
| `reported_at` | ISO 8601 UTC datetime | |

**report_type enum values**:
```
"action_report"
"finding_report"
"approval_request"
"approval_outcome_report"
"escalation_report"
"handoff_report"
"return_to_planning_report"
"intake_outcome_report"
"rejection_report"
"no_action_report"
```

**approval_or_governance_posture enum values**:
```
"not_required"
"approval_requested"
"approval_pending"
"approved"
"rejected"
"escalated"
"no_action_unclear_authority"
```

**status enum values**:
```
"pending_review"
"approved_to_proceed"
"blocked"
"returned_to_planning"
"deferred"
"rejected"
"complete"
"no_action_taken"
"escalated"
```

**V Forge execution variant — additional required fields**

| Field | Type | Notes |
|---|---|---|
| `originating_handoff_id` | UUID | Required for all V Forge execution reports tied to a handoff |
| `execution_scope_completed` | string | What was completed within the approved scope |
| `execution_scope_not_completed` | string | What remains; may be empty if fully complete |
| `execution_truth_owner` | enum: `["v_forge"]` | Fixed value — V Forge retains execution truth |

**Structural constraints**

- `constraints_risks_uncertainties` must be explicitly present, even if empty string.
  Omitting this field is structurally invalid. This prevents the field from being
  silently dropped when there are no uncertainties — the explicit empty signals
  an informed determination, not an omission.
- `report_type` must match the actual content. An approval request report that omits
  the approval-specific fields fails semantic sufficiency even if it passes base schema.
- `execution_truth_owner` must always be `"v_forge"` in V Forge execution reports.

**What can be checked structurally**
- All required fields present
- Enum conformance on `report_type`, `system_context`, `approval_or_governance_posture`, `status`
- Non-empty string on `subject`, `action_or_outcome`, `basis`, `actor_context`
- UUID format on `report_id`, `originating_handoff_id`
- Datetime format on `reported_at`
- Fixed-value enforcement on `execution_truth_owner`

**What cannot be checked structurally**
- Whether the basis is sufficient to justify the stated outcome
- Whether the action or outcome is accurately described vs. framing partial
  completion as full completion
- Whether material uncertainty is present but omitted despite the field being present
  (an honest empty string vs. a dishonest empty string looks identical structurally)
- Whether the report is session-local ephemeral output or durably stored

---

### E. VEDA → V Forge Startup Signal Package (envelope only)

**Purpose:** Delivers bounded baseline execution intelligence context to V Forge at
execution scope initialization. Schema-able now at the envelope level; signal content
fields are opaque until VEDA signal content families are governed.

**Envelope required fields** (schema now)

| Field | Type | Notes |
|---|---|---|
| `package_id` | UUID | Stable across re-delivery |
| `correlation_id` | UUID | |
| `originating_handoff_id` | UUID | The confirmed handoff that triggered this delivery |
| `signal_scope` | array of string (non-empty) | Signal class labels for what this package represents |
| `startup_relevance_statement` | string (non-empty) | Why this package applies to this execution scope |
| `observation_timestamps` | array of ISO 8601 UTC datetime | When evidence was gathered; non-empty |
| `delivery_timestamp` | ISO 8601 UTC datetime | When VEDA initiated delivery |
| `freshness_classification` | enum: `["fresh", "aging", "stale", "uncertain"]` | |
| `trust_classification` | string (non-empty) | VEDA's trust assessment for included signal |
| `package_revision_posture` | enum: `["original", "revision"]` | |
| `prior_package_id` | UUID or null | Required when revision |

**Signal content field — opaque until governed**

| Field | Type | Notes |
|---|---|---|
| `signal_content` | JSONB / object | Opaque for now. Structure governed by VEDA signal content families (deferred, Batch H). Do not enforce internal shape until those families are specified. |
| `execution_facing_caveats` | string | Known gaps or uncertainty markers; empty string if none |

**Structural constraints**

- `signal_scope` array must be non-empty. A startup package with no stated scope
  is invalid.
- `observation_timestamps` array must be non-empty. Absence of timestamps prevents
  freshness assessment.
- `freshness_classification` must use the governed enum.
- When `package_revision_posture = "revision"`, `prior_package_id` must not be null.
- `signal_content` is not structurally validated at the internal field level until
  VEDA content families are governed.

---

### F. Project V → VEDA Evidence Request (request envelope)

**Purpose:** Project V issues a bounded planning-side evidence need to VEDA. The
response returns through the VEDA → Project V signal delivery path. Only the
request envelope is schematized here.

**Required fields**

| Field | Type | Notes |
|---|---|---|
| `request_id` | UUID | Stable across re-send attempts |
| `correlation_id` | UUID | Links request to response leg |
| `planning_context_ref` | `{ref_type: string, ref_id: UUID}` | Which project or bounded planning scope |
| `bounded_planning_question_summary` | string (non-empty) | The planning-side need; not a record retrieval instruction |
| `originating_workflow_stage` | string (non-empty) | e.g. `"project_intake_stage_6"` |
| `freshness_requirement` | enum: `["current_only", "recent_acceptable", "any_available"]` | |
| `requested_at` | ISO 8601 UTC datetime | |

**Optional fields**

| Field | Type | Notes |
|---|---|---|
| `urgency_posture` | enum: `["standard", "blocking_planning_decision"]` | |

**Structural constraints**

- `bounded_planning_question_summary` must be non-empty. An empty request question
  is structurally invalid and is almost certainly a request for raw observatory access
  disguised as a bounded question.
- `planning_context_ref` must carry a non-null `ref_id`. Scoped to a specific project.

**What can be checked structurally**
- All required fields present
- UUID format on `request_id` and in `planning_context_ref.ref_id`
- Non-empty string on `bounded_planning_question_summary`, `originating_workflow_stage`
- Enum conformance on `freshness_requirement`, `urgency_posture`

**What cannot be checked structurally**
- Whether the question is actually bounded or is effectively a request for
  unrestricted signal
- Whether the stated originating workflow stage is accurate
- Whether the freshness requirement is appropriate to the actual planning need

---

## 6. Human-Judgment-Only Fields

The following field categories appear structurally in one or more packet types but
require human review for honesty, sufficiency, or governance validity. Passing
structural schema does not satisfy the governance requirement for these fields.

**Scope descriptions**
`approved_execution_scope` (handoff), `scope_completed` / `scope_not_completed`
(return-to-planning). A validator can confirm non-empty string. It cannot confirm
that a scope description is actually bounded, or that completion reporting is
accurate. Human review required.

**Readiness and basis claims**
`readiness_basis` (handoff), `basis` (report). Structural validation confirms
non-empty. It cannot confirm that the basis is honest, that the cited planning
rationale actually justifies the handoff, or that the readiness evaluation was
genuine. Human review required.

**Finding characterization**
`bounded_finding_summary`, `planning_concern_implicated` (return-to-planning).
Structural validation confirms non-empty. It cannot detect whether the finding
is actually execution-side or is a disguised planning instruction, or whether the
planning concern is accurately stated. Human review required.

**Approval scope and action description**
`action_or_transition_requested`, `scope`, `if_approved_outcome` (approval request).
Structural validation confirms non-empty. It cannot detect whether the described
scope matches what will actually proceed, or whether the approval class is
correctly assigned. Human review required — this is the core of why approval
requests require a human gate.

**Trigger reason categorization**
`trigger_reason` (return-to-planning). Structural validation enforces the enum.
It cannot detect whether the trigger reason is correctly categorized — e.g., a
case where V Forge desires a planning change and categories a preference as
`"findings_require_planning_reconsideration"`. Human review required.

**Report completeness**
`constraints_risks_uncertainties` (report). Structural validation confirms the
field is present. It cannot distinguish an honest empty string (genuinely no
material uncertainty) from a dishonest empty string (uncertainty present but
omitted). Human review required for governance-sensitive reports.

**Evidence and provenance references**
`evidence_refs` (handoff), `evidence_basis` (return-to-planning). Structural
validation confirms reference format. It cannot confirm that the referenced records
exist, are current, are non-stale, or actually support the basis claimed. Human
review required before governance-sensitive approvals.

**Freshness classifications**
`freshness_classification` (startup signal package). Structural validation enforces
the enum. It cannot confirm that VEDA's classification is accurate or that a
package labeled `"fresh"` was actually gathered recently. Human review of freshness
required for high-stakes execution contexts.

---

## 7. Validation Order / Implementation Order

Implement in this order. Rationale follows.

**1. Handoff package**

The handoff is the highest-stakes cross-system transfer in the ecosystem. It is the
most complete packet spec in the repo. Implement its structural schema first. Getting
this right establishes the pattern for all others.

**2. Approval request package**

Approval request packages gate the handoff (and other critical transitions). The
base schema is seam-independent and reusable. Implementing it second means the
approval gate has structural validation in place before any approval-sensitive
interface goes live.

**3. Return-to-planning package**

Closes the handoff loop. V Forge cannot return governed findings to Project V
without this package. Implement third, after handoff and approval request schemas
are stable.

**4. Governed report package (base + V Forge execution variant)**

Implement the base schema and the V Forge execution variant together. Reports
underpin the sufficiency standard across all V Forge operations. Implement before
any V Forge execution reporting goes live.

**5. VEDA → V Forge startup signal package (envelope only)**

The envelope is implementable now. Mark `signal_content` as opaque JSONB and
document that internal structural validation is deferred until VEDA signal content
families are governed (Batch H doctrine completion). Implement the envelope schema
before the startup signal delivery interface goes live.

**6. Project V → VEDA evidence request**

The request envelope is well-defined and implementable. Implement before the
evidence request interface is wired into the intake or replanning workflows.

**7. VEDA Strategy signal packages** — defer until Batch K full contracts exist.

---

## 8. Anti-Drift Rules

**Do not treat structural validity as semantic validity.**
A packet that passes schema is shaped correctly. It may still carry dishonest,
insufficient, or governance-violating content. Schema validation is a first filter,
not a governance clearance.

**Do not widen packet fields beyond what the source docs define.**
If a field is not in the relevant interface doc's required semantic fields section,
it does not belong in the schema without a documented authority change. Schema
drafting does not authorize field invention.

**Do not allow free-form blobs where typed references are required.**
Evidence references, planning context references, and entity references must use
the structured `{ref_type, ref_id}` pattern, not free-text strings. Free-text
references are not traceable to canonical Postgres records.

**Do not silently accept partial packages for convenience.**
Missing required fields are a hard validation failure, not a soft warning. A
packet missing `activation_approval_ref` is not an acceptable partial handoff.
A packet missing `finding_boundary_marker` is not an acceptable return package.
Partial packages must be rejected and the gap surfaced explicitly.

**Do not encode doctrine ambiguities as fake enums.**
If a field's governed vocabulary is not yet settled (e.g., internal signal content
classifications in the startup package), mark the field as opaque or JSONB. Do not
invent an enum vocabulary that has no authority basis. Fake enums look like
governance but are not — they create false confidence and make real governance work
harder later.

**Do not let schema theater substitute for approval gates.**
Structural validation of an approval request package is not the approval event.
The governance gate defined in `desktop-governance-and-gating-model.md` requires
a persisted approval record. Schema validation of the request package is a
prerequisite check, not a gate.

**Do not schema the VEDA Strategy interfaces yet.**
Both VEDA Strategy signal interfaces are governed stubs with Batch K deferred.
Structural schema work on those packets cannot proceed until the full interface
contracts exist. Premature schemas for stub interfaces will embed assumptions that
the Batch K spec may contradict.

**Do not use `approved_execution_scope` as a proxy for scope governance.**
The scope field is a non-empty string that a schema validator can check. It cannot
confirm that the scope is actually bounded. Do not rely on schema validation of
this field as a substitute for human review of scope sufficiency before handoff
activation proceeds.

---

## 9. Recommended Next Move

**Immediate:** Implement Postgres-level or service-layer packet validation for the
handoff package using the field definitions in Section 5A. The handoff package is
the highest-stakes transfer in the system and the most mature spec. Start here.

**Following:** Build the base approval request package schema. Make it reusable
across seams — the base fields are seam-independent. Each seam adds its entity
reference on top.

**Before cross-system interfaces go live:** Schemas for the return-to-planning
package and the governed report base must exist. These are required for V Forge
to participate in governed cross-system operations.

**VEDA startup signal envelope:** Schema the envelope before the startup delivery
interface goes live. Document the content field as deferred-opaque pending Batch H
doctrine completion. Do not block on content schema.

**VEDA Strategy interfaces:** No schema work until Batch K full contracts exist.
Explicitly mark these as schema-deferred in any implementation tracking.

**After schemas exist:** The next move is building the service-layer write helpers
that enforce these schemas at packet creation time — not just at receipt. The
producing system must not be able to produce a structurally invalid packet.
Validation at the receiver alone is too late for governance.

---

## 10. Related Files

Authority docs this spec derives from:

- `interfaces/project-v-to-v-forge-handoff-interface.md`
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `interfaces/veda-to-v-forge-signal-interface.md`
- `interfaces/project-v-to-veda-evidence-request-interface.md`
- `interfaces/veda-strategy-to-project-v-signal-interface.md`
- `interfaces/veda-strategy-to-v-forge-signal-interface.md`
- `governance/approval-mechanics-seam-model.md`
- `governance/report-structure-and-required-fields.md`
- `v-forge/reporting-and-approval-model.md`
- `v-forge/operational-model.md`
- `interfaces/desktop-governance-and-gating-model.md`

Implementation-support context:

- `transition-steward/activity-trail-implementation-spec.md`
- `transition-steward/transition-plan.md`
