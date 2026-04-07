# Schema Authority Wave Checkpoint

## Purpose

This document records the completed schema-authority foundation wave as a clean
handoff artifact. It states what was done, what is now closed, what is intentionally
still partial, and what the recommended next work order is.

It is not an audit pass. It does not contain new schema design. It exists so that
future threads can restart cleanly without reconstructing the wave from earlier
audit docs or individual artifact post-write reports.

---

## Scope of This Checkpoint

This checkpoint covers:

- the outputs of the schema-authority foundation wave that followed Pass 4
- the closed foundations that implementations and future schema work may rely on
- the intentionally partial areas that remain as known next-layer work
- confirmed canon and boundary decisions that must not be reopened
- recommended next execution order
- explicit deferred items and why they are deferred, not blocked
- restart guidance for the next steward thread

---

## Inputs Reviewed

- `audit/full-audit/pass-3-schema-and-implementation-readiness.md`
- `audit/full-audit/pass-4-final-gap-summary.md`
- `ecosystem/ecosystem-schema-spine.md`
- `governance/actor-identity-schema-spec.md`
- `project-v/project-v-schema-authority.md`
- `veda/veda-schema-authority.md`
- `v-forge/v-forge-schema-authority.md`
- `ecosystem/activity-trail-model.md` (corrected canon)

---

## What Was Completed in This Wave

### 1. Canon correction: `evidence_query` entity type added to `ecosystem/activity-trail-model.md`

A confirmed mismatch existed between `ecosystem/activity-trail-integration-map.md`
Section 4b (which uses `entity_type: evidence_query` for V Forge active evidence
query records) and `ecosystem/activity-trail-model.md` (which did not list
`evidence_query` in its entity type vocabulary). This was a surgical corrective
edit to the model's "Added entity types" block. The entry now reads: `evidence_query`
— a V Forge active evidence query record or query session, used for `evidence.query`
events under the V Forge → VEDA evidence access contract. The integration map and
the model are now aligned.

### 2. `ecosystem/ecosystem-schema-spine.md`

Created the ecosystem-layer schema spine — the shared schema foundation that all
three system schema authority docs reference. It settled: the full activity trail
record schema contract (all fields, required/nullable posture, allowed values); the
canonical enumerated types for `actor_type`, `actor_system`, `action_class`, the
full action vocabulary, and the full entity type vocabulary (now fifteen types
including `evidence_query`); the cross-system thin-reference pattern and provenance
requirements; and retention and compaction constraints per action class. This
document is the fixed reference layer — system schema authority docs extend it,
not contradict it.

### 3. `governance/actor-identity-schema-spec.md`

Created the actor identity value-class specification, resolving the deferral in
`governance/auth-and-actor-model.md`. It settled: `actor_type` as a closed
three-value enumeration (`agent`, `operator`, `system`); `actor_id` value-class
requirements per type (operator = stable user record identifier; agent = stable
governed agent identifier or instance identifier; system = stable system process
identifier); `actor_system` confirmed as five values (`project_v`, `veda`,
`v_forge`, `ecosystem`, `extension`); and the explicit schema-layer decision that
External Actor is outside the canonical `actor_type` enumeration and that
`external` is not a valid value. External-origin context is preserved in `details`
fields, not in `actor_type`.

### 4. `project-v/project-v-schema-authority.md`

Created the Project V system schema authority document. It settled the field-level
schema contracts for Project V's primary canonical entities: `project`, `approval_record`,
`decision_record`, `handoff`, `intake_outcome`, `launch_authorization`, and
`evidence_request`. It also established the two-tier entity set framing (primary
canonical entities vs. Project V-governed seam entities). It explicitly resolved the
Decision Record vs. ADR question: ADR is an optional representation/artifact linked
from `decision_record.decision_content_ref`, not a separate schema entity. It
identified `readiness_evaluation` as partially specified and established the cross-system
thin-reference posture for all Project V-owned records that reference VEDA or V Forge
entities.

### 5. `veda/veda-schema-authority.md`

Created the VEDA system schema authority document. It settled the field-level schema
contracts for VEDA's three primary entities: `evidence` (with full provenance,
freshness, and trust fields), `signal_package` (as a single entity family across
all three delivery contexts — `proactive`, `request_response`, and `startup` —
distinguished by `delivery_trigger_type` rather than split into separate types),
and `observatory_scope_change` (aligned to the canonical `observatory.scope_change.*`
action family and lifecycle). It established evidence provenance posture (external
source context is provenance metadata, not actor identity). It explicitly
acknowledged four partially specified VEDA entity families.

### 6. `v-forge/v-forge-schema-authority.md`

Created the V Forge system schema authority document. It settled the field-level
schema contract for `execution_return` (the clearest V Forge entity, fully derivable
from the return-to-planning interface), and the partial but actionable schema posture
for `task` (lifecycle states derivable from activity trail canon; core reference
fields derivable from handoff interface; internal structure deferred). It established
the schema authority boundary for V Forge execution intelligence and bounded
execution findings (bounded to approved execution scope, must not drift into VEDA
observatory patterns). It explicitly identified the six content graph entity families
as V Forge-owned but requiring a dedicated sub-pass for field contract design. It
acknowledged four additional partially specified entity families.

---

## Current Closed Foundations

The following are strong enough to build against now. Later threads must not
treat these as open questions.

**Ecosystem schema spine:** The activity trail record schema contract, all canonical
enumerated types (including `evidence_query`), the cross-system thin-reference
pattern, and the retention and compaction constraints are all formally specified in
`ecosystem/ecosystem-schema-spine.md`. Implementations should use this as the
fixed shared reference layer.

**Actor identity value-space:** `actor_type` is three values (closed). `actor_system`
is five values (closed). `actor_id` value-class requirements are specified per
actor type. External Actor is definitively outside the canonical `actor_type`
enumeration. These decisions are in `governance/actor-identity-schema-spec.md`
and must not be relitigated.

**Project V governance-critical entity closure:** The `approval_record` schema
contract (including the Reviewability Principle translation, lifecycle states,
approval class linkage, and actor identity reference rules) and the `decision_record`
schema contract (including five lifecycle states, supersedence/invalidation linkage,
cross-system consequences flag, and decision class taxonomy) are both fully specified
in `project-v/project-v-schema-authority.md`. The `handoff` and `intake_outcome`
field contracts are also fully closed there.

**ADR resolved as representation within `decision_record`:** ADR documents are
optional artifacts referenced by `decision_record.decision_content_ref`. No separate
`adr` entity type exists in Project V's schema. Supersedence and invalidation are
tracked on `decision_record`, not on ADR documents. This is settled.

**VEDA primary entity closure:** The `evidence` entity schema contract (including
all provenance, freshness, trust, and `evidence_class` fields) and the `signal_package`
entity schema (single family across all three delivery contexts) are fully specified
in `veda/veda-schema-authority.md`. The `observatory_scope_change` schema and
lifecycle states are also fully contracted there.

**`signal_package` as one unified entity family:** VEDA → Project V proactive
delivery, request-response delivery, and VEDA → V Forge startup delivery all use
the same `signal_package` entity type, distinguished by `delivery_trigger_type`.
This is a closed design decision. No split into separate entity families is warranted.

**V Forge `execution_return` closure:** The `execution_return` schema contract is
fully specified in `v-forge/v-forge-schema-authority.md`, derived completely from
the return-to-planning interface doc and integration map Section 3. The
`finding_boundary_marker` field makes the finding-report boundary contract-explicit
at the record level.

**Shared cross-system thin-reference posture:** The pattern for how any system
references entities owned by another system — `entity_type` + `entity_id` from
the owning system + minimum provenance fields — is settled in the ecosystem schema
spine and applied consistently across all three system schema authority docs.

---

## Current Intentional Partial Areas

The following areas are intentionally still partial. They are not forgotten and not
secretly missing. They represent the next layer of schema work, to be done in focused
passes after the foundation wave.

**Project V — `readiness_evaluation`:** Core fields (scope, type, outcome,
governing decision refs, evidence refs, validity window) are documented. The
sub-fields of `planning_side_assessment` depend on implementation context and
are not yet enumerated. Marked as partially specified with an honest scope statement
in `project-v/project-v-schema-authority.md`.

**VEDA — source capture record:** Ownership established; `evidence.provenance_ref`
linkage defined. The internal field structure of a capture session — what fields
distinguish capture methods, what a "provider session identity" looks like, how
capture records chain to source item records — is not specified. Deferred to VEDA
implementation docs.

**VEDA — source item record:** Ownership established; parent-child relationship
to source capture records implied. Item-to-evidence relationship (one-to-one vs.
aggregation) is not yet specifiable from current docs. Deferred.

**VEDA — observatory event record:** Ownership established; distinction from the
ecosystem activity trail and from the `observation_record` entity type is clarified.
VEDA's internal observatory event log field structure is deferred to VEDA
implementation docs.

**VEDA — provider configuration record:** Ownership established; relationship to
scope change events implied. This is substantially VEDA-internal implementation
detail. Deferred.

**V Forge — `task` internal field structure:** Core reference fields (`project_id`,
`originating_handoff_ref`, `execution_scope_id`) and lifecycle states are specified.
The full internal field structure beyond the derivable core is deferred to V Forge
implementation docs.

**V Forge — execution record:** Ownership established; lifecycle states are derivable
(see the Execution Record and Execution Lifecycle Posture section). The internal
field structure — how it aggregates task records, what constitutes an execution
"session" vs. a scope — is deferred.

**V Forge — execution intelligence record:** Ownership and boundary (bounded to
approved execution scope, must not hold VEDA observatory data) are established.
Internal field structure deferred.

**V Forge — bounded execution findings record (non-return-to-planning):** Ownership
established; the distinction between internal findings and `execution_return` packages
is clear conceptually. Internal field structure of findings resolved within scope
(not delivered to Project V) is deferred.

**V Forge — maintenance execution record:** Ownership established; relationship to
the execution record and the maintenance-vs-replanning distinction is clear. Field
structure deferred.

**V Forge — content graph entity families (page, topic, entity, internal_link,
archetype, schema_usage):** V Forge's ownership of all six is unambiguous and fully
established. Field contracts for all six require a dedicated focused sub-pass.
No current doc provides a derivation base for field-level contracts. This is
explicitly the largest single remaining schema design task in the ecosystem.

---

## Confirmed Canon / Boundary Decisions That Must Not Be Reopened

The following decisions are settled. Future threads must treat them as baseline
and must not reopen them without specific file-text evidence of a contradiction.

**Project V = planning truth. VEDA = signal / evidence / observability truth.
V Forge = execution truth.** These ownership assignments are stable across all
boundary docs, all schema authority docs, and all audit passes. They must not
be blurred.

**Operator-mediated observatory scope expansion is settled.** The
`operator-to-veda-observatory-scope-expansion-interface.md` is a full Tier 1
document. The `observatory.scope_change.*` action type family (seven types) and
the `observatory_scope_change` entity type are canonical. V Forge never directly
invokes this interface. The path is: V Forge surfaces gap via `execution.return`
→ operator decides → Project V routes request with operator approval reference →
VEDA responds. This is closed and must not be redesigned.

**External Actor is outside the canonical `actor_type` enumeration.** `external`
is not a valid `actor_type` value. External-origin context is captured in `details`
fields, not as a new `actor_type`. Adding `external` to the enumeration requires
a canon-change edit to `ecosystem/activity-trail-model.md` first. This decision
is in `governance/actor-identity-schema-spec.md` and must not be silently overridden.

**ADR is not a separate Project V schema entity.** It is an optional representation
artifact linked from `decision_record.decision_content_ref`. Governance status
(proposed/approved/superseded/invalidated) is tracked on `decision_record`, not
on the ADR document. No `adr` entity type should be added to the schema.

**`signal_package` remains one VEDA entity family across all three delivery contexts.**
`delivery_trigger_type` (`proactive`, `request_response`, `startup`) is the
discriminator. No split into separate entity families is needed or warranted.

**Content graph ownership belongs entirely to V Forge and must not be reassigned.**
The six content graph families (page, topic, entity, internal_link, archetype,
schema_usage) are V Forge-owned. When the content graph schema design sub-pass
begins, it must take this ownership as settled and produce field contracts for
V Forge-owned entities — not reassign any family to VEDA or Project V.

**`execution_return` does not become planning truth.** When Project V receives an
`execution_return` package and proceeds with replanning, the resulting planning
decisions become Project V-owned `decision_record` entities. The `execution_return`
entity is a bounded findings delivery vehicle. It does not govern anything after
receipt.

**Activity trail records are immutable and produced at the ecosystem layer.** All
three systems produce activity trail records conforming to the ecosystem schema spine.
Activity trail records are not owned by any individual system. They are not editable
after creation. This is not a V Forge, VEDA, or Project V schema decision; it is a
fixed ecosystem-layer constraint.

---

## Recommended Next Execution Order

The following names the practical next fronts in order. Do not start new workstreams
not listed here without a specific gap justification.

**1. V Forge content graph schema design sub-pass.**
This is the largest remaining schema design task and the one with the least
derivation base from existing docs. It should be a focused pass producing field
contracts for all six content graph entity families (page, topic, entity,
internal_link, archetype, schema_usage) and their interrelationships. Input: the
ownership claim in `ecosystem/cross-system-boundaries.md` and the V Forge schema
authority doc as the authority boundary setter. Output: a V Forge content graph
schema spec, likely in `v-forge/content-graph-schema.md` or equivalent.

**2. Partially specified entity families — as implementation approach requires them.**
The partial entity families in Project V, VEDA, and V Forge do not need to be
closed simultaneously. Close them as the implementation work that depends on them
approaches. The priority order within this bucket:
- V Forge execution record (needed when execution scope state management is built)
- VEDA source capture / source item records (needed when VEDA ingest persistence is built)
- Project V readiness_evaluation deeper field structure (needed when launch readiness
  workflow is implemented)
- V Forge execution intelligence record (needed when V Forge intelligence layer is built)
- VEDA observatory event record and provider configuration record (needed when VEDA
  internal logging and provider config are built)

**3. Stub interface contract upgrades — when implementation reaches those seams.**
The three stub interfaces (`execution-clarification`, `handoff-recall`,
`scope-update`) and the evidence request interface (portfolio-scope fields) are
sufficient as governing boundary documents for now. Upgrade them to full contracts
when the implementation teams reach those seams and need field-level schemas. Do
not upgrade them preemptively.

**4. Implementation docs derived from the schema authority layer.**
Once the schema authority layer (this wave's output) is treated as stable, the
natural next layer is implementation-facing persistence docs — actual table/collection
definitions, query API specs, and migration plans — derived from the schema contracts
established in this wave. Those docs should reference, not re-derive, the schema
authority layer.

---

## What Is Explicitly Deferred

The following items are deferred by sequencing, not because the architecture is
unresolved or the ownership is unclear.

**Content graph field contracts** — V Forge owns the content graph; the field
contracts require a dedicated design sub-pass. Deferred until that sub-pass is
scheduled.

**`readiness_evaluation` deep field structure** — core fields are specified; the
sub-fields of `planning_side_assessment` depend on implementation context. Deferred
to Project V implementation docs.

**Source capture and source item record topology** — VEDA owns both; the
parent-child structure and item-to-evidence relationship require VEDA implementation
doc input. Deferred.

**Observatory event record internal schema** — VEDA owns it; the field structure is
VEDA-internal operational logging. Deferred to VEDA implementation docs.

**Execution record deep modeling** — V Forge owns it; the aggregation structure
(execution record → task records) and session concept require V Forge implementation
doc input. Deferred.

**Provider configuration schema** — VEDA owns it; substantially VEDA-internal
implementation detail. Deferred.

**Stub interface contract upgrades** — deferred until implementation teams reach
those seams and need field-level schemas. The current stub posture is sufficient
as governing boundary documentation.

**Portfolio-scoped access authorization schema mechanics (P3 from Pass 4)** —
the `scope_type` and `portfolio_authorization_ref` fields on `evidence_request`
are correctly deferred to the evidence request stub upgrade. Deferred.

---

## Restart Guidance for the Next Steward Thread

**Read these files first, in this order:**

1. `audit/full-audit/schema-authority-wave-checkpoint.md` (this file) — to understand
   what the current state is without re-reading all the wave outputs from scratch
2. The specific schema authority doc for the system you are working on:
   `ecosystem/ecosystem-schema-spine.md`, `project-v/project-v-schema-authority.md`,
   `veda/veda-schema-authority.md`, or `v-forge/v-forge-schema-authority.md`
3. The source doc for the specific entity or gap you are working on — interface doc,
   workflow doc, or governance doc as relevant

**Safe assumptions when restarting:**

- All five schema authority documents in this wave are in place and represent the
  current authoritative schema-layer baseline.
- The `evidence_query` entity type is canonical in `ecosystem/activity-trail-model.md`.
  Do not re-flag it as a missing canon item.
- The three system schema authority docs (`project-v`, `veda`, `v-forge`) can be
  referenced by implementation docs. They are stable.
- The partially specified entity families are known and intentional. Do not treat
  them as audit gaps or missing artifacts. They are next-layer work.
- The governance, seam, and workflow layers are locked. Do not reopen them unless
  specific file text contradicts something.

**Drift traps to avoid:**

- Do not confuse a partially specified entity family with a missing artifact.
  "Partial" means ownership is clear and some fields are specified. "Missing"
  means no artifact exists at all. The wave closed all seven previously-missing
  artifacts (M1–M7 from Pass 4).
- Do not reopen the content graph ownership question. V Forge owns all six
  families. The sub-pass designs field contracts within that settled ownership.
- Do not add `external` to `actor_type` without first editing
  `ecosystem/activity-trail-model.md` and creating a new canon-change justification.
- Do not create a separate `adr` entity type in Project V. ADR is a representation
  artifact linked from `decision_record.decision_content_ref`.
- Do not upgrade stub interface contracts before the primary entity schemas they
  depend on (particularly `handoff` and `decision_record`) are being used in
  implementation. The current stub posture is sufficient.

**What not to reopen:**

- System ownership assignments (Project V / VEDA / V Forge truth domains)
- Observatory scope expansion governance (operator-mediated path is settled)
- `signal_package` as a single entity family with `delivery_trigger_type`
  discriminator
- `execution_return` as a bounded findings delivery, not planning truth
- Actor type enumeration (three values, closed)
- ADR vs. `decision_record` (resolved: ADR is a representation artifact, not a
  separate entity)

**How to classify future work:**

Use these definitions, consistent with the audit pass rubric:

- **Complete** — strong enough to build against now; no additional schema work
  required in this domain before implementation begins
- **Partial** — meaningful schema work exists (ownership clear, some fields
  specified) but the full field contract is not yet closed; known next-layer work
- **Missing** — required artifact genuinely does not exist yet; must be created
  before the gap can be treated as closed
- **Blocked** — cannot responsibly proceed until a prerequisite is settled;
  the current schema wave produced no blocked items

When classifying future work, check the "Current Intentional Partial Areas" section
above before labeling something missing. A partial is not missing.

**The core question for any new proposed work:**

Is this translating existing settled doctrine into schema contracts (permitted),
or is it designing new architecture or reopening settled decisions (not permitted
without a specific file-text contradiction trigger)?

If it is translation: proceed, following the existing schema authority doc structure.
If it is new design: it requires a separate, explicitly scoped design pass, not
a quiet addition to an existing schema authority doc.

---

## Related Docs

- `audit/full-audit/README.md`
- `audit/full-audit/master-plan.md`
- `audit/full-audit/pass-3-schema-and-implementation-readiness.md`
- `audit/full-audit/pass-4-final-gap-summary.md`
- `ecosystem/ecosystem-schema-spine.md`
- `governance/actor-identity-schema-spec.md`
- `project-v/project-v-schema-authority.md`
- `veda/veda-schema-authority.md`
- `v-forge/v-forge-schema-authority.md`
- `ecosystem/activity-trail-model.md`
