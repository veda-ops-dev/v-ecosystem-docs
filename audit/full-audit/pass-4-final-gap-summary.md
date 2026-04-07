# Pass 4 — Final Gap Summary and Execution Order

## Purpose

This document synthesizes the validated findings of Passes 1, 2, and 3 into a
single execution-order artifact. It states what is complete, what is partial, what
is missing, and what should be done next, in what order.

This is not an audit narrative. It is a build-order organizer for the schema
authority phase.

---

## Scope of This Pass

This pass covers:

- cross-pass synthesis of complete / partial / missing / blocked classifications
- a final execution matrix consolidating all findings across Passes 1–3
- a priority-ordered schema artifact sequence derived from Pass 3 with sequencing
  rationale made explicit
- separation of immediate corrective tasks from deferred and later-phase work
- a final implementation-readiness verdict for the repo as of this wave

This pass does not reopen governance, seam architecture, or workflow findings.
Those are treated as baseline. Where a Pass 1 or Pass 2 finding feeds a Pass 4
action, the action is stated here without relitigating the finding.

---

## Inputs / Prior Passes Used

- `audit/full-audit/pass-1-governance-and-boundaries.md` — governance stability
  confirmed; three schema-phase artifact dependencies identified (approval record,
  actor identity spec, portfolio-scope mechanics)
- `audit/full-audit/pass-2-interfaces-and-workflows.md` — interface and workflow
  layer confirmed substantially complete; cleanup actions identified and applied
- `audit/full-audit/pass-3-schema-and-implementation-readiness.md` — schema
  readiness assessed; seven missing schema artifacts identified; evidence_query
  entity type canon mismatch confirmed; recommended artifact sequence produced

All cleanup actions from Passes 1 and 2 are treated as applied. The stale
forward-reference notes, the `data-boundaries.md` registry update, and the
`v-forge-evidence-access-contract.md` activity trail alignment are all treated
as resolved baseline for this pass.

---

## Executive Verdict

The V Ecosystem repo is **governance-stable, seam-stable, and workflow-complete**.
The authority layer, interface set, and workflow coverage are all strong enough to
build against. No architectural decisions are pending. No blocked work remains.

The repo is **ready to transition from audit to schema authority drafting**.

The remaining work is formalization and translation, not design. The governance
docs, interface docs, integration map, and ownership tables together provide
sufficient raw material to derive all required schema entities. What is missing is
the formal schema authority artifacts that consolidate that material into
per-system and ecosystem-level schema contracts.

One concrete corrective canon task remains unresolved from Pass 3: the
`evidence_query` entity type is used in integration map Section 4b but is absent
from the activity trail model's entity type vocabulary. This must be corrected
as part of Step 1 of the artifact sequence below — not as a standalone cleanup
task, and not later.

Seven schema artifacts need to be created. None is blocked by an unresolved
architectural decision. The sequence is dependency-driven, not arbitrary.

---

## Final Complete / Partial / Missing / Blocked Matrix

### Complete

The following are classified as **Complete** — coherent, stable, and strong enough
to build against without further work in that domain.

| ID  | Domain / Artifact                                      | Source Pass |
|-----|--------------------------------------------------------|-------------|
| C1  | System ownership / truth-domain model                  | Pass 1      |
| C2  | Cross-system access governance (six-pattern model)     | Pass 1      |
| C3  | Operator → VEDA observatory scope expansion interface  | Pass 1      |
| C4  | Approval model — Tier 1 (meaning and posture)          | Pass 1      |
| C5  | Approval mechanics — Tier 2 (seam model)               | Pass 1      |
| C6  | Decision continuity doctrine                           | Pass 1      |
| C7  | Invalidation and supersedence doctrine                 | Pass 1      |
| C8  | Agent authority posture (matrix + doctrine + auth)     | Pass 1      |
| C9  | External action governance                             | Pass 1      |
| C10 | Activity trail model (governance infrastructure)       | Pass 1      |
| C11 | VEDA → Project V signal interface                      | Pass 2      |
| C12 | Project V → V Forge handoff interface                  | Pass 2      |
| C13 | V Forge → Project V return-to-planning interface       | Pass 2      |
| C14 | VEDA → V Forge startup signal interface                | Pass 2      |
| C15 | Project V → VEDA evidence request interface            | Pass 2      |
| C16 | Project intake workflow                                | Pass 2      |
| C17 | Handoff workflow                                       | Pass 2      |
| C18 | Maintenance and replanning workflow                    | Pass 2      |
| C19 | Launch readiness workflow                              | Pass 2      |
| C20 | Post-launch observation workflow                       | Pass 2      |
| C21 | Canonical entity ownership assignment (all 3 systems)  | Pass 3      |
| C22 | Activity trail entity type vocabulary (14 named types) | Pass 3      |
| C23 | Approval mechanics — semantics fully specified         | Pass 3      |
| C24 | Cross-system reference rules (derivable)               | Pass 3      |
| C25 | Activity trail record — field contract fully specified | Pass 3      |
| C26 | Decision state model — lifecycle states derivable      | Pass 3      |
| C27 | Handoff entity — field contract derivable              | Pass 3      |
| C28 | Signal package entity — field contract derivable       | Pass 3      |
| C29 | Intake outcome entity — field contract derivable       | Pass 3      |
| C30 | Observation record entity — field contract derivable   | Pass 3      |

---

### Partial

The following have substantial, usable work but carry a gap that must be resolved
before the relevant schema can be finalized.

| ID  | Domain / Gap                                          | Impact                                           | Source Pass |
|-----|-------------------------------------------------------|--------------------------------------------------|-------------|
| P1  | Approval record entity schema — semantics defined,    | Blocks Project V schema authority finalization.  | Pass 1 / 3  |
|     | record shape not formalized                           | Addressed in Step 3 (artifact M1).               |             |
| P2  | Actor identity value-space — doctrine clear,          | Blocks activity trail finalization for audit     | Pass 1 / 3  |
|     | schema underspecified (actor_id value class missing)  | queries. Addressed in Step 2 (artifact M2).      |             |
| P3  | Portfolio-scoped access authorization —               | Not a blocker for core schema work. Surfaces     | Pass 1 / 3  |
|     | access model defined, schema mechanics soft           | when evidence request stub is upgraded.          |             |
| P4  | Stub interface entity schemas — action types          | Not a blocker for primary entity schemas.        | Pass 3      |
|     | canonical, field-level contracts not yet final        | Addressed in Step 5 (stub upgrades).             |             |
| P5  | v-forge-evidence-access-contract.md activity trail    | Non-canonical records if built against as-is.    | Pass 2      |
|     | convention — partially divergent from integration map | **Treated as resolved** (Pass 2 cleanup wave     |             |
|     |                                                       | applied this correction). Listed for traceability|             |
|     |                                                       | only; not an open action.                        |             |

---

### Missing

The following required artifacts genuinely do not exist on the current merged
baseline. All seven must be created.

| ID  | Artifact                                  | Priority   | Prerequisite           |
|-----|-------------------------------------------|------------|------------------------|
| M1  | `approval_record` entity schema contract  | Immediate  | M7 (ecosystem spine)   |
| M2  | Actor identity value-space spec           | Immediate  | None                   |
| M3  | `decision_record` entity schema contract  | Immediate  | M7 (ecosystem spine)   |
| M4  | Project V schema authority document       | Immediate  | M7, M1, M2, M3         |
| M5  | VEDA schema authority document            | After M4   | M7, M4 (for ref model) |
| M6  | V Forge schema authority document         | After M4   | M7, M4 (for ref model) |
| M7  | Ecosystem schema spine document           | First       | None                   |

---

### Blocked

**None.**

No work is blocked by an unresolved architectural decision, an absent prerequisite
doc, or a contested boundary. Pass 3 confirmed this explicitly. The sequential
dependencies above (M7 before M4–M6, M2 before M4) are ordering dependencies, not
blockers — all prerequisite decisions have been made.

---

## Priority-Ordered Execution Plan

The following plan is sequenced by dependency. Steps within a numbered group can
be executed in parallel. Steps across numbered groups must respect the stated order.

---

### Step 1 — Ecosystem Schema Spine (prerequisite for all system schemas)

**Artifact:** `ecosystem/ecosystem-schema-spine.md`

**What it must contain:**

- activity trail record schema: translate the complete field specification from
  `ecosystem/activity-trail-model.md` into a formal database schema definition
  (field names, types, constraints, nullable posture, retention rules per action class)
- entity type vocabulary: enumerate all named entity types as a closed enumerated
  type; see Step 1a below for the corrective action that must be resolved here
- action type vocabulary: enumerate all canonical action types as a closed
  enumerated type
- cross-system identity reference patterns: define the foreign key conventions
  for how Project V, VEDA, and V Forge records reference each other; establish
  that cross-system references are thin pointers with provenance metadata, not
  duplicated canonical records
- retention and compaction rules: express the action-class-based retention posture
  from the activity trail model as schema constraints

**Step 1a — Corrective canon task (must be resolved in this step):**

`ecosystem/activity-trail-integration-map.md` Section 4b uses
`entity_type: evidence_query` for V Forge active evidence query records.
`ecosystem/activity-trail-model.md` does not include `evidence_query` in its
entity type vocabulary.

This is a confirmed canon mismatch. The entity type is in use in the integration
map without a backing entry in the model. Resolving it requires two edits:

1. Add `evidence_query` to the entity type vocabulary in `ecosystem/activity-trail-model.md`
   with the same definition posture as other entity types in that section.
2. Confirm the addition is reflected in the ecosystem schema spine's enumerated
   entity type list.

This is a corrective task, not new design. It must be done before the ecosystem
schema spine is treated as final.

**Enables:** M1, M2, M3, M4, M5, M6 (all downstream schema work).

---

### Step 2 — Actor Identity Value-Space Spec (parallel with Step 1, or immediately after)

**Artifact:** `governance/actor-identity-schema-spec.md` (companion to
`governance/auth-and-actor-model.md`)

**What it must contain:**

- confirm the `actor_type` value set: `agent`, `operator`, `system` are named in
  the activity trail model; confirm whether `external` is a fourth valid value or
  whether External Actor events are excluded from trail records
- specify the `actor_id` value class per actor type: what kind of thing `actor_id`
  is for each actor type (e.g., "for `operator`: a stable user record ID; for
  `agent`: a stable agent session or agent-type identifier; for `system`: a
  system process identifier")
- confirm the `actor_system` value set: `project_v`, `veda`, `v_forge`,
  `ecosystem`, `extension` — confirm this is the complete enumeration

This is a small document. It resolves a deferred implementation question from
`auth-and-actor-model.md`, not new architecture.

**Enables:** M1 (approval record references approving actor identity), M4
(Project V schema authority), activity trail schema finalization.

---

### Step 3 — Project V Schema Authority (after Steps 1–2)

**Artifact:** `project-v/project-v-schema-authority.md` (or equivalent location)

**What it must contain:**

- `approval_record` entity schema (M1 / P1): translate the Reviewability Principle
  and Approval Request Principle from `governance/approval-and-escalation-model.md`
  into a schema entity spec; minimum fields: stable approval record identity,
  entity reference (type + id), approval class, initiating system, approving actor
  identity (from M2 value spec), scope, conditions, current state, activation
  timestamp, expiry/revocation/supersedence references
- `decision_record` entity schema (M3): translate from
  `governance/decision-continuity-doctrine.md` and
  `governance/invalidation-and-supersedence-doctrine.md`; minimum fields:
  stable decision identity, decision text/summary, decision class, owning system,
  scope, approval posture reference, lifecycle state (proposed | approved | rejected
  | superseded | invalidated), timestamps, superseded-by and invalidated-by
  references with reasons, cross-system consequences flag
- `handoff` entity schema: derive from `interfaces/project-v-to-v-forge-handoff-interface.md`
  and integration map Section 2; field contract is substantially complete in Pass 3
  (C7)
- `intake_outcome` entity schema: derive from intake workflow Stage 5/7 and
  integration map Section 9; all five outcome types must be supported (C9)
- `project` entity schema and project metadata schema
- `readiness_evaluation` entity schema (launch readiness workflow Stage 4)
- planning-side traceability reference posture: what Project V stores locally vs.
  what it references by pointer to other systems

**Note on decision record vs. ADR:** The governance docs reference both
`decision_record` and ADRs as Project V canonical records. The Project V schema
authority doc must explicitly resolve whether these are the same schema entity
with a type discriminator, two distinct entities, or an ADR-is-a-decision_record
subtype. This is a scoped schema-phase decision; the current docs treat them as
overlapping without disambiguating at the schema level.

**Enables:** M5, M6 (VEDA and V Forge schemas will reference approval records
and decision records from Project V by pointer).

---

### Step 4 — VEDA and V Forge Schema Authority (after Step 3, parallel with each other)

**VEDA artifact:** `veda/veda-schema-authority.md` (or equivalent location)

Priority entities:
- `evidence` record schema: derive from evidence access contract required response
  fields (`evidence_id`, `gathered_at`, `source_provider`, `source_url`,
  `freshness_status`, `freshness_window_end`, `trust_classification`) — these
  become schema fields
- `signal_package` entity schema: distinguish what persists vs. what is ephemeral
  per delivery; two delivery contexts (Project V push, V Forge startup) share the
  same entity type, distinguished by `originating_handoff_ref` presence
- observatory event record schema: VEDA's internal event log; not yet schema-specified
- source capture and source item record schemas
- evidence provenance record schema

**V Forge artifact:** `v-forge/v-forge-schema-authority.md` (or equivalent location)

Priority entities:
- `task` entity schema: activity trail maps `task.create`, `task.complete`,
  `task.fail`, etc.; no field contract exists yet
- execution record and execution lifecycle state schema
- content graph entity schemas: `page`, `topic`, `entity`, `internal_link`,
  `archetype`, `schema_usage` — these are the largest single schema design block
  in the ecosystem and have no current foundation doc beyond the ownership claim
  in `cross-system-boundaries.md`
- `execution_return` entity schema: partially specified via integration map
  Section 3; needs completion
- execution intelligence records and bounded execution-side research schema
  boundary: the governance-defined carve-out ("bounded execution-side research")
  must be expressed at schema level so that execution intelligence records are
  distinguishable from VEDA observatory records that V Forge is not permitted to hold

**Note on content graph:** The content graph entity schemas are the most V Forge-
specific schema concern and have no cross-system reference obligations comparable
to approvals or decisions. They can be designed with more flexibility, but they
also have no existing derivation base from other docs. This block warrants its
own focused design sub-pass when V Forge schema authority work begins.

**Enables:** Step 5 (stub interface contract upgrades reference handoff,
decision_record, and scope_update entities defined in Steps 3–4).

---

### Step 5 — Stub Interface Contract Upgrades (after Steps 3–4)

The three stub interfaces are sufficient as governing boundary documents for
current purposes. They become implementation blockers only when the implementation
teams need field-level schemas for those seams. The upgrade timing is after Steps
3–4 because the stub entities cross-reference entities defined in those steps.

**Stubs to upgrade:**
- `interfaces/project-v-to-v-forge-execution-clarification-interface.md` — upgrade
  to full contract; entity schema references `handoff` (Step 3) and
  `execution_clarification` (integration map Section 6a)
- `interfaces/project-v-handoff-recall-interface.md` — upgrade to full contract;
  entity schema references `handoff` (Step 3)
- `interfaces/project-v-to-v-forge-scope-update-interface.md` — upgrade to full
  contract; entity schema references `handoff` (Step 3) and `scope_update`
  (integration map Section 6c)

**Also in this step:**
- `interfaces/project-v-to-veda-evidence-request-interface.md` — when upgrading
  this stub to a full contract, add `scope_type` (project | portfolio) and
  `portfolio_authorization_ref` fields to the `evidence_request` entity schema;
  `portfolio_authorization_ref` must reference the authorization mechanism
  established in the actor identity spec (Step 2); this resolves P3

---

## Recommended Artifact Sequence

The following is the definitive artifact creation order for the schema authority
phase. Items at the same numbered level may be worked in parallel.

```
1.  ecosystem/ecosystem-schema-spine.md
    + corrective edit: add evidence_query to activity-trail-model.md entity type vocabulary

2.  governance/actor-identity-schema-spec.md

3.  project-v/project-v-schema-authority.md
    (includes approval_record and decision_record entity schemas)

4a. veda/veda-schema-authority.md
4b. v-forge/v-forge-schema-authority.md
    (4a and 4b are parallel; neither depends on the other)

5.  Stub interface contract upgrades (3 stubs + evidence request scope fields)
    (all depend on Step 3; can be sequential or parallel among themselves)
```

Total artifact count: 6 new documents + 1 corrective canon edit to an existing doc.

---

## Immediate Next Actions

The following should happen before any other schema-phase work begins.

**1. Correct the `evidence_query` entity type omission.**

Edit `ecosystem/activity-trail-model.md` to add `evidence_query` to the entity
type vocabulary. This is a confirmed canon mismatch between the integration map
(which uses the type) and the model (which does not define it). It is the only
open corrective canon task remaining after Pass 2 cleanup. It must be resolved
before the ecosystem schema spine is finalized, and it should not be deferred to a
later step.

**2. Draft `ecosystem/ecosystem-schema-spine.md`.**

This is the first schema authority artifact. It establishes the shared reference
layer (activity trail record schema, enumerated vocabularies, cross-system reference
conventions) that all three system schema authority docs will depend on. Starting
system schemas before the spine exists will produce inconsistent identity formats
and reference patterns that are hard to correct retroactively.

**3. Draft `governance/actor-identity-schema-spec.md`.**

This can be done in parallel with Step 2. It is a small document that resolves
the `actor_id` value-class deferral from `auth-and-actor-model.md`. It is a
prerequisite for the `approval_record` entity schema (which must reference the
approving actor by a durable, schema-defined identity) and for audit query
finalization on the activity trail.

---

## Deferred / Later-Phase Work

The following items are not immediate. They are either correctly deferred to the
stub-upgrade phase or are follow-on concerns that arise after schema authority
docs are in place.

**Stub interface contract upgrades (Step 5).**
All three stubs are sufficient for schema planning. Upgrading them requires the
primary entity schemas to exist first. Do not begin stub upgrades until Step 3 is
complete.

**Portfolio-scoped access authorization schema mechanics (P3).**
The access model is defined. The schema fields (`scope_type`,
`portfolio_authorization_ref`) need to be added when the evidence request stub
is upgraded to a full contract. This is correctly deferred to Step 5 and depends
on the actor identity spec (Step 2) for the authorization reference target.

**Content graph entity schemas (V Forge sub-block).**
The content graph is the largest single schema design task in the ecosystem. It
has no cross-system dependency obligations that require it to be done before VEDA
or Project V schemas. It should be treated as the primary V Forge schema design
sub-pass within Step 4b.

**Decision record vs. ADR disambiguation.**
The Project V schema authority doc (Step 3) must resolve whether `decision_record`
and ADR are the same entity or distinct. This is a scoped decision within Step 3,
not a prerequisite for starting it.

**Ongoing governance hygiene.**
The LLM Use Principle sections, the VEDA Brain prohibition, and the Forbidden
agent action list should be explicitly referenced (not paraphrased) in new schema
authority docs as they are written. This is a quality posture note, not a
scheduled action item.

---

## Final Implementation-Readiness Verdict

**Governance and boundary layer:** Complete. Stable enough to build against.
No open decisions.

**Seam and interface layer:** Complete. Four primary interfaces and the
observatory scope expansion interface are full Tier 1 documents. Three stub
interfaces are sufficient governing boundary documents. All five workflows
are complete.

**Activity trail canon:** Complete for governance-layer derivation. One
corrective canon task remains (`evidence_query` entity type omission). That
task is concrete, scoped, and must be resolved before the ecosystem schema spine
is finalized.

**Schema authority layer:** Not yet started. Seven artifacts required. None is
blocked. The sequence is well-defined. The raw material to derive all schemas
exists in the current doc set.

**Overall verdict:**

```
The repo is ready to move from audit to schema authority drafting.

Governance: locked.
Interfaces and workflows: locked.
Activity trail vocabulary: canonical (one corrective edit pending).
Schema authority artifacts: seven required, none blocked, sequence defined.

Next immediate authoring steps:
  1. Correct evidence_query omission in activity-trail-model.md
  2. Draft ecosystem-schema-spine.md
  3. Draft actor-identity-schema-spec.md (parallel with 2)
  4. Draft project-v-schema-authority.md
  5. Draft veda-schema-authority.md and v-forge-schema-authority.md (parallel)
  6. Upgrade stub interface contracts
```

No architectural work is pending. The schema phase is translation and
formalization of already-settled doctrine, ownership, and field contracts —
not new design.

---

## Related Docs Used in This Pass

- `audit/full-audit/README.md`
- `audit/full-audit/master-plan.md`
- `audit/full-audit/pass-1-governance-and-boundaries.md`
- `audit/full-audit/pass-2-interfaces-and-workflows.md`
- `audit/full-audit/pass-3-schema-and-implementation-readiness.md`
