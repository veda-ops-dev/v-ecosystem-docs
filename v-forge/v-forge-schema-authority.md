# V Forge Schema Authority

## Purpose

This document defines the schema authority for V Forge's canonical entities.

It exists to answer:

```text
What entities does V Forge own, what fields must each entity carry at the schema
level, what is the schema posture for execution records and the content graph,
how does V Forge reference cross-system entities without duplicating their canonical
data, and where does V Forge schema authority stop and require a later focused
design pass?
```

This is a Tier 1 V Forge schema authority document.

---

## Scope

This document governs:

- the canonical entity set owned by V Forge
- field-level schema contracts for the fully-specified V Forge entities: `task`
  and `execution_return`
- schema-facing posture for execution records and execution lifecycle
- schema-facing posture for execution intelligence and bounded execution findings
- schema authority posture for the content graph entity family, with honest
  acknowledgment of which families require a later focused design sub-pass
- V Forge cross-system reference posture for Project V and VEDA entities
- honest disclosure of V Forge entity families that are partially specified under
  current docs

---

## Out of Scope

This document does not define:

- Project V-owned entity schemas (project, handoff, decision_record, approval_record,
  intake_outcome, readiness_evaluation)
- VEDA-owned entity schemas (evidence, signal_package, observatory records)
- ecosystem-layer enumerated types — those are defined in
  `ecosystem/ecosystem-schema-spine.md` and must not be redefined here
- storage engine specifics, migration files, indexing strategy, or ORM structure
- execution engine architecture, worker queue design, task dispatch mechanics,
  or content build pipeline internals
- transport-layer implementation details for handoff or return-to-planning delivery

Those belong in the respective system schema authority docs, the ecosystem schema
spine, or implementation docs.

---

## System

- v-forge

---

## Relationship to Existing Authority Docs

This document derives from and must remain consistent with:

- `interfaces/data-boundaries.md` — the canonical data ownership map that defines
  which record categories V Forge owns; the primary ownership source for this document
- `ecosystem/ecosystem-schema-spine.md` — defines shared enumerated types
  (`actor_type`, `actor_system`, `action_class`, entity type vocabulary, action
  vocabulary), the activity trail record schema contract, and the cross-system
  identity reference pattern; V Forge schema must not redefine those
- `governance/actor-identity-schema-spec.md` — defines the `actor_id` value-class
  contract per `actor_type`; referenced where V Forge records carry actor attribution
- `interfaces/project-v-to-v-forge-handoff-interface.md` and
  `workflows/handoff-workflow.md` — define handoff semantics; V Forge task and
  execution record posture derives from the handoff package it receives
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md` and
  `workflows/maintenance-and-replanning-workflow.md` — define return-to-planning
  package semantics; the `execution_return` schema derives from these
- `interfaces/v-forge-evidence-access-contract.md` — defines V Forge's governed
  evidence query posture; informs V Forge cross-system reference posture for VEDA
  evidence records
- `interfaces/veda-to-v-forge-signal-interface.md` — defines startup signal delivery
  semantics; informs how V Forge references startup signal context
- `interfaces/project-v-to-v-forge-execution-clarification-interface.md`,
  `interfaces/project-v-handoff-recall-interface.md`, and
  `interfaces/project-v-to-v-forge-scope-update-interface.md` — define adjacent
  execution-seam interface semantics
- `ecosystem/cross-system-boundaries.md` and
  `ecosystem/cross-system-access-governance.md` — define ownership boundaries and
  the cross-system access governance rules V Forge must observe
- `workflows/post-launch-observation-workflow.md` — informs post-launch execution
  intelligence and observation record posture at the schema level

This document does not replace any of those authority docs. It translates their
settled canon into schema-level entity contracts for V Forge.

---

## Core Rule

V Forge is the schema authority for execution truth, implementation truth, content
graph truth, and execution intelligence derived from crossing the content graph
against VEDA signal.

Every entity schema defined here must be consistent with the system ownership
boundaries in `ecosystem/cross-system-boundaries.md` and the canonical data
ownership map in `interfaces/data-boundaries.md`.

V Forge's schema layer must reflect the execution model: V Forge builds and
maintains content within approved scope, produces bounded execution findings for
planning reconsideration when needed, and maintains execution intelligence by
crossing its content graph against VEDA-delivered signal. It does not plan,
approve, or make governing decisions. Those concerns must not appear as owned
field semantics in V Forge entity schemas.

---

## V Forge Schema Authority Boundary

### What belongs in V Forge schema authority

- Task entity schema and execution lifecycle posture
- Execution return entity schema (bounded findings package for return-to-planning)
- Execution record and execution lifecycle state posture
- Execution intelligence and bounded execution findings posture
- Content graph entity families: page, topic, entity, internal_link, archetype,
  schema_usage
- Maintenance execution records
- Execution-side reporting records
- V Forge's thin references to Project V handoff identifiers and VEDA evidence
  and signal package identifiers

### What does not belong here

- Project V planning / approval / decision / project records
- VEDA evidence truth, signal packages, or observatory records
- Ecosystem-layer enumerated types (belong in the schema spine)
- Activity trail records (V Forge produces these; they are governed by the ecosystem
  schema spine, not owned by V Forge)
- Execution worker queue implementation, task dispatch engine internals, or build
  pipeline mechanics

---

## Canonical V Forge Entity Set

V Forge owns entities across two tiers. Both are governed by this document.

**Primary canonical entities** are V Forge-owned records where the field contract
is fully derivable from current interface, workflow, and activity trail docs.

**Partially specified entity families** are record families V Forge clearly owns but
for which current docs do not yet provide a closed field contract. They are listed
in the Partially Specified V Forge Entity Families section rather than presented as
complete contracts.

| Entity | Tier | Activity trail entity_type | Status |
|---|---|---|---|
| `task` | Primary | `task` | Contracted below (partial derivation — see note) |
| `execution_return` | Primary | `execution_return` | Fully contracted below |
| Execution record | Partial | — | Partially specified — see below |
| Execution intelligence record | Partial | — | Partially specified — see below |
| Bounded execution findings record | Partial | — | Partially specified — see below |
| Maintenance execution record | Partial | — | Partially specified — see below |
| Content graph: `page` | Content graph family | — | Schema authority posture stated; field contract deferred |
| Content graph: `topic` | Content graph family | — | Schema authority posture stated; field contract deferred |
| Content graph: `entity` | Content graph family | — | Schema authority posture stated; field contract deferred |
| Content graph: `internal_link` | Content graph family | — | Schema authority posture stated; field contract deferred |
| Content graph: `archetype` | Content graph family | — | Schema authority posture stated; field contract deferred |
| Content graph: `schema_usage` | Content graph family | — | Schema authority posture stated; field contract deferred |

---

## Task Entity Schema Contract

The `task` entity is V Forge's canonical record of a bounded unit of execution work.
The activity trail model defines `task.create`, `task.assign`, `task.start`,
`task.complete`, `task.fail`, and `task.cancel` as canonical action types, establishing
that tasks are a real, persisted entity class with a governed lifecycle. The field
contract here represents what is derivable from the activity trail canon, the
ownership model, and the handoff interface semantics.

**Honest scope statement:** The `task` entity is partially derivable. The activity
trail canon establishes the lifecycle action types and confirms task is a V Forge-owned
entity type. The handoff interface establishes that tasks are scoped to an approved
execution scope within a confirmed handoff. But no current doc specifies the internal
field structure of task records beyond what the activity trail base fields and
handoff reference semantics provide. The contract below formalizes what is reliably
derivable; implementers should extend it through V Forge implementation docs.

### Required fields (derivable from current docs)

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `task_id` | Yes | No | Stable, globally unique identifier assigned by V Forge. Immutable after assignment. This is the `entity_id` referenced in activity trail records with `entity_type: task`. |
| `project_id` | Yes | No | The project scope this task is associated with. All tasks must be project-scoped. Carried from the confirmed handoff that authorized this task's execution context. |
| `originating_handoff_ref` | Yes | No | Reference to the `handoff_id` (Project V-owned) of the confirmed handoff that authorized the execution scope within which this task exists. Thin reference — carries the handoff identifier, not handoff content. |
| `execution_scope_id` | Yes | No | Identifier for the bounded execution scope this task belongs to. Derived from the handoff's `execution_scope_id`. Multiple tasks may share an execution scope within a single handoff. |
| `task_objective` | Yes | No | Bounded description of what this task is intended to accomplish within the approved execution scope. Must be specific enough to be reviewable and attributable. |
| `lifecycle_state` | Yes | No | Current lifecycle state. See lifecycle states below. |
| `assigned_to` | Yes | Yes | Actor reference for the agent or system process assigned to this task. Uses the `actor_id` value class from `governance/actor-identity-schema-spec.md` for `agent` or `system` actor types. Null if not yet assigned. |
| `created_at` | Yes | No | UTC timestamp of task record creation. |
| `started_at` | Yes | Yes | UTC timestamp when task execution began. Null until task moves to `in_progress`. |
| `completed_at` | Yes | Yes | UTC timestamp of task completion (success or failure). Null until terminal state. |
| `outcome_summary` | Yes | Yes | Brief structured summary of the task outcome. Null until a terminal state is reached. Must not claim success when the outcome is failure or partial. |
| `updated_at` | Yes | No | UTC timestamp of last record update. |

### Task lifecycle states

These states are directly derivable from the canonical activity trail action vocabulary
(`task.create`, `task.assign`, `task.start`, `task.complete`, `task.fail`,
`task.cancel`):

- `created` — task record exists; not yet assigned or started
- `assigned` — task has been assigned to an agent or system process
- `in_progress` — task execution has begun
- `completed` — task has completed successfully within approved scope
- `failed` — task has failed; the failure must be recorded and may contribute to an
  `execution_return` package if the failure affects the planning basis
- `cancelled` — task was cancelled before completion through a governed cancellation event

**Note on `task.start` vs `in_progress`:** The `task.start` activity trail action
transitions the lifecycle state from `assigned` to `in_progress`. Implementations
should not conflate assignment with starting.

---

## Execution Return Entity Schema Contract

The `execution_return` entity is V Forge's canonical record of a bounded execution
findings package delivered to Project V through the return-to-planning interface.
It is the schema counterpart to the `execution_return` activity trail entity type.

The field contract is derived from the required semantic fields in
`interfaces/v-forge-to-project-v-return-to-planning-interface.md` and the minimum
additional fields in `ecosystem/activity-trail-integration-map.md` Section 3.

This entity is one of the most clearly specified V Forge entities because the
return-to-planning interface doc provides an explicit and complete semantic field
list. The contract below translates that directly.

### Required fields

| Field | Required | Nullable | Notes |
|---|---|---|---|
| `execution_return_id` | Yes | No | Stable, globally unique identifier assigned by V Forge. Immutable after assignment. Must remain stable across re-delivery attempts. This is the `entity_id` referenced in activity trail records with `entity_type: execution_return`. |
| `project_id` | Yes | No | The project scope this return package is associated with. |
| `originating_handoff_ref` | Yes | No | Reference to the `handoff_id` (Project V-owned) of the handoff or bounded execution context that generated these findings. Thin reference — the handoff_id only, not handoff content. This ties the return to its originating governed transfer and prevents orphaned findings. |
| `trigger_reason` | Yes | No | The explicit reason return-to-planning is being triggered. Must fall into one of the valid trigger categories from the interface doc: `execution_blocked`, `execution_failed`, `execution_incomplete`, `changed_conditions_invalidated_assumptions`, `findings_require_planning_reconsideration`. |
| `execution_posture_at_return` | Yes | No | V Forge's current execution posture at the time of return delivery. One of: `halted`, `paused`, `completed_bounded`, `continuing_degraded`. This is the `execution_posture` field from integration map Section 3 minimum additional fields. |
| `bounded_findings_summary` | Yes | No | Bounded description of what happened in execution — what was completed, what was not, what was blocked or changed. Execution-side reporting, not a planning instruction. |
| `scope_completion_summary` | Yes | No | What portion of the approved execution scope was completed before the triggering condition, what remains incomplete, and what the current execution state is. |
| `execution_constraints_or_blockers` | Yes | No | The specific constraint, failure, missing condition, or changed circumstance that led to this return. Must be execution-side in nature. |
| `finding_basis_summary` | Yes | No | The execution-side basis for the finding — what V Forge observed, attempted, or encountered. Findings without an execution-side basis must not appear here. |
| `planning_concern_implicated` | Yes | No | A bounded statement of what aspect of the prior plan or planning assumption the finding speaks to. This is V Forge's curation rationale — not a planning instruction. |
| `finding_provenance_refs` | Yes | Yes | Array of thin references to VEDA evidence records consulted during execution that bear on these findings, if applicable. Each reference must carry `source_system: veda`, `evidence_id`, `gathered_at`, and `freshness_status`. May be empty if the finding does not reference VEDA-sourced evidence. |
| `finding_boundary_marker` | Yes | No | Explicit boolean or structured marker indicating these are bounded execution findings for planning reconsideration — not VEDA signal, not governing planning decisions, not automatic planning mutations. Value must be `true`. This field makes the finding-report boundary contract-explicit at the record level. |
| `observation_timestamp` | Yes | No | When the triggering condition was observed or arose. Allows Project V to assess how current the finding is and whether urgency applies. |
| `delivery_state` | Yes | No | Current delivery state. See delivery states below. |
| `delivered_at` | Yes | Yes | UTC timestamp when V Forge initiated push delivery. Null until delivery begins. |
| `confirmed_at` | Yes | Yes | UTC timestamp when Project V confirmed receipt. Null until confirmation is received. |
| `package_version_posture` | Yes | No | One of: `original`, `revision`. If `revision`, `prior_execution_return_ref` must be populated. |
| `prior_execution_return_ref` | Yes | Yes | Reference to the `execution_return_id` of the prior package this revision supersedes. Required when `package_version_posture` is `revision`. Null for original packages. |
| `created_at` | Yes | No | UTC timestamp of record creation. |
| `updated_at` | Yes | No | UTC timestamp of last record update. |

### Execution return delivery states

- `pending` — package prepared; delivery not yet initiated
- `delivered` — V Forge has initiated push delivery; Project V confirmation not yet received
- `confirmed` — Project V has confirmed receipt; delivery phase is complete
- `failed` — delivery attempt produced no confirmation within the expected window
- `voided` — package superseded or withdrawn before confirmation

### Key constraints

**`execution_return` does not replace `decision_record`.** When Project V receives
an `execution_return` package and proceeds with replanning, the planning decisions
that result from that process are Project V-owned `decision_record` entities. The
`execution_return` entity is the bounded findings delivery — it does not become a
governing record after receipt.

**`execution_return` does not authorize planning changes.** Receipt of an
`execution_return` does not trigger automatic planning mutation. The review and
replanning workflow (`workflows/maintenance-and-replanning-workflow.md`) governs
the path from receipt to any planning state change.

**Planning concern is curation, not instruction.** The `planning_concern_implicated`
field captures V Forge's curation rationale — what the finding is relevant to.
It is not a planning instruction. Project V determines what to do with it.

---

## Execution Record and Execution Lifecycle Posture

V Forge's execution truth encompasses the full lifecycle of an active execution
scope — from handoff receipt through task execution, findings production, and
terminal state. The canonical data ownership map names "execution records and
execution lifecycle state" as V Forge-owned.

**Current derivable posture:**

The handoff interface and handoff workflow establish that:
- V Forge receives a confirmed handoff and takes on execution responsibility for
  the approved bounded scope
- execution responsibility is active from handoff confirmation until returned,
  recalled, or completed
- V Forge maintains execution state as the canonical ledger of what has happened
  within the scope

The activity trail action types establish that V Forge's execution actions produce
records in these families:
- task lifecycle events (`task.create`, `task.assign`, `task.start`, `task.complete`,
  `task.fail`, `task.cancel`)
- handoff receipt (`handoff.confirmed`, `handoff.recall.confirmed`)
- return-to-planning delivery (`execution.return`, `execution.return.confirmed`,
  `execution.return.failed`, `execution.return.voided`)
- content actions (`content.create`, `content.update`, `content.publish`)
- clarification and scope update receipt (`execution.clarification.confirmed`,
  `execution.scope_update.confirmed`)
- agent lifecycle events for V Forge execution agents

**What this means for the execution record schema:**

An "execution record" in V Forge terms is the durable record that represents an
active or completed execution scope instance — the top-level container that ties
together the confirmed handoff, the tasks executed within it, any findings produced,
and the terminal state. The activity trail canon provides the event-level record of
what happened within an execution scope. The execution record itself is the
persistent state anchor.

The full field contract for the V Forge execution record is partially specified —
see Partially Specified V Forge Entity Families below. The ownership is clear;
the precise field list requires a V Forge implementation doc pass to finalize.

**Derivable lifecycle states for an execution scope:**

- `awaiting_handoff` — handoff has been delivered but not yet confirmed by V Forge
- `active` — handoff confirmed; execution is underway within approved scope
- `returning` — an `execution_return` package has been initiated; planning
  reconsideration is in progress
- `paused` — execution is paused pending clarification, scope update, or
  planning decision
- `completed` — execution within the approved scope is complete
- `recalled` — handoff was recalled by operator before material execution began
- `cancelled` — execution was cancelled through a governed planning decision
  following return-to-planning

---

## Execution Intelligence and Bounded Execution Findings Posture

V Forge owns "execution intelligence records — cross-referencing outputs of content
graph against VEDA signal" and "bounded execution findings records" as canonical
record families per the data ownership map.

### What execution intelligence is

Execution intelligence is the analytical output V Forge produces by crossing its
owned content graph against VEDA-delivered signal. This includes:
- gap analysis between current content graph coverage and observed external signal
- performance interpretation of the content graph against search performance signal
- execution-side opportunity identification within the bounded scope

Execution intelligence is V Forge-derived — it is produced by V Forge from the
combination of V Forge-owned content graph data and VEDA-delivered signal. It is
not raw VEDA evidence. It is not planning analysis.

### Schema-facing posture

Execution intelligence records must:
- carry a reference to the originating handoff or execution scope
- carry references to the VEDA signal package or evidence records that were
  cross-referenced (thin references with provenance per the cross-system reference
  posture section)
- carry the content graph state at the time of analysis (or a stable reference to it)
- state the bounded scope of the analysis (project-scoped, not open-ended)
- not be used to make planning decisions — execution intelligence informs execution;
  planning decisions belong to Project V

Execution intelligence must not drift into VEDA-style evidence collection. The
distinction defined in `ecosystem/cross-system-boundaries.md` is critical: "V Forge
reads VEDA signal to produce execution intelligence. It does not own the signal."
An execution intelligence record that stores VEDA observatory data as though V Forge
originated it is an ownership blur.

### What bounded execution findings are

Bounded execution findings are the subset of execution intelligence and execution
observations that warrant delivery to Project V through the return-to-planning
interface. Not all execution intelligence becomes a return-to-planning finding.
Only findings that cannot be resolved within the approved scope become
`execution_return` packages.

Bounded execution findings that are resolved within scope — resolved through
maintenance, clarification, or execution within approved bounds — remain V Forge-owned
operational records without becoming Project V-facing deliveries.

### Partially specified

The full field contracts for execution intelligence records and bounded execution
findings records that do not result in `execution_return` packages are not specified
by current interface or governance docs. They are noted in the Partially Specified
section below.

---

## Content Graph Entity Family Posture

V Forge canonically owns the content graph — pages, topics, entities, internal links,
archetypes, and schema usage records — as established in `ecosystem/cross-system-boundaries.md`
("the content graph of what was built — pages, topics, entities, internal links,
archetypes, schema usage") and `interfaces/data-boundaries.md`.

### Schema authority posture

V Forge is the sole schema authority for all content graph entity families. No other
system may define schema for these entities. VEDA must not model the content graph;
Project V must not store content graph records as canonical execution truth.

The content graph is the most V Forge-specific schema concern in the ecosystem.
Unlike task records or execution return records, content graph entities have no
cross-system reference obligations comparable to handoffs or approvals — they are
V Forge-internal execution truth.

### Current status: field contracts deferred to a focused sub-pass

Current docs — interface docs, governance docs, workflow docs, and the activity trail
canon — do not provide field-level specifications for any content graph entity family.
The ownership is unambiguous. The field contracts are not yet derivable from existing
docs.

**Fabricating field contracts for content graph entities would be overspecification.**
The content graph schema is the largest single schema design task in V Forge and
involves decisions (e.g., how `topic` entities relate to `page` entities, how
`internal_link` records capture link structure, what distinguishes an `archetype`
record from a content type specification, what `schema_usage` tracks at the page
level) that require V Forge implementation design — not just translation of existing
docs.

### What this means in practice

- **V Forge owns the content graph.** This is non-negotiable and fully established.
- **No other system defines content graph schema.** VEDA and Project V must not
  create schemas that duplicate or substitute for V Forge content graph records.
- **Content graph field contracts require a dedicated V Forge schema design sub-pass.**
  That sub-pass should produce a V Forge content graph schema specification that
  extends this document. It should not reopen ownership or boundary decisions.
- **The activity trail action types** `content.create`, `content.update`, and
  `content.publish` are canonical for content graph state changes. Any content graph
  entity that undergoes these transitions must produce activity trail records using
  these action types, with `entity_type` and `entity_id` fields populated per the
  specific content graph entity being modified.

### Per-family authority statement

| Content graph family | V Forge-owned | Field contract status |
|---|---|---|
| `page` | Yes — a V Forge execution-built content unit | Requires dedicated sub-pass |
| `topic` | Yes — a V Forge content organization / topical cluster record | Requires dedicated sub-pass |
| `entity` | Yes — a V Forge semantic entity record within the content graph | Requires dedicated sub-pass |
| `internal_link` | Yes — a V Forge link relationship record within the content graph | Requires dedicated sub-pass |
| `archetype` | Yes — a V Forge content structure / template reference record | Requires dedicated sub-pass |
| `schema_usage` | Yes — a V Forge record of structured data / schema.org usage on built content | Requires dedicated sub-pass |

---

## V Forge Cross-System Reference Posture

V Forge references Project V and VEDA entities where interface docs require them.
All cross-system references from V Forge records must follow the thin-reference
pattern defined in `ecosystem/ecosystem-schema-spine.md`.

### V Forge references to Project V handoff records

V Forge holds `originating_handoff_ref` on task records and `execution_return` records.
These are thin references to the `handoff_id` assigned by Project V. V Forge does
not store handoff content; it references the handoff by its Project V-assigned
identifier to tie execution records to their governing approved scope.

The reference must carry:
- `entity_type: handoff`
- `entity_id: <handoff_id>` (Project V-assigned)
- `confirmed_at` — the timestamp at which V Forge confirmed receipt of this handoff

V Forge must not store richer copies of Project V handoff package content as though
it becomes V Forge-owned execution planning data. The handoff content is Project V
truth delivered to V Forge for use within the approved scope. It does not become
V Forge-canonical by being received.

### V Forge references to seam entity records

For execution clarification, scope update, and recall events, V Forge receives and
confirms seam entities (`execution_clarification`, `scope_update`) owned by Project V.
V Forge's confirmation events in the activity trail reference these entities by their
`entity_id` from Project V's identifier space. V Forge does not own these entities;
it confirms receipt and adjusts execution accordingly.

### V Forge references to VEDA signal packages

When V Forge receives a VEDA startup signal package, the startup signal delivery
provides execution intelligence context. V Forge may hold a reference to the
`signal_package_id` (VEDA-assigned) as the originating startup signal context for
the current execution scope. This reference must carry:
- `entity_type: signal_package`
- `entity_id: <signal_package_id>` (VEDA-assigned)
- `delivery_trigger_type: startup`
- `confirmed_at` — timestamp of V Forge's receipt confirmation

V Forge must not treat the delivered startup signal package as V Forge-owned signal
truth. The delivered signal remains VEDA-originated evidence with VEDA's trust and
provenance classification. V Forge's execution intelligence — derived by crossing
the startup signal against the content graph — is V Forge-owned. The startup signal
itself is not.

### V Forge references to VEDA evidence records (via governed query)

When V Forge queries VEDA evidence through the governed evidence access contract, the
returned evidence records carry `evidence_id` (VEDA-assigned), `gathered_at`,
`source_provider`, `freshness_status`, and `trust_classification`. V Forge may
reference queried evidence in execution intelligence records and bounded execution
findings using these fields as thin references.

V Forge must not accumulate VEDA evidence into a persistent local store that functions
as a shadow observatory. Evidence is queried, used within the execution session, and
attributed in execution outputs. The `evidence_id` from VEDA is the canonical
reference; V Forge does not reassign it.

When an `execution_return` package references VEDA evidence as part of its finding
provenance, the `finding_provenance_refs` array carries thin references per the
field contract above.

### Bounded execution-side research boundary at schema level

`ecosystem/cross-system-boundaries.md` defines "bounded execution-side research"
as research performed in support of approved execution, handoff, maintenance, or
return-to-planning needs — not open-ended ecosystem-wide signal gathering.

At the schema level, this boundary means:

- V Forge execution intelligence records must carry a reference to the approved
  execution scope or handoff that authorized the research context
- An execution intelligence record without a bounded execution scope reference is
  not within the governed posture
- V Forge may not create execution intelligence records that reference VEDA
  observatory data beyond what was delivered through the startup signal interface
  or queried through the governed evidence access contract
- Records that accumulate VEDA data as though V Forge is an observatory violate
  this boundary regardless of how they are labeled

---

## Partially Specified V Forge Entity Families

The following entity families are clearly V Forge-owned but do not yet have closed
field contracts derivable from current docs. Each is listed with what is known,
what remains soft, and why it stays partial.

### Execution Record

**Ownership:** V Forge. The execution record is the top-level state anchor for an
active or completed execution scope instance.

**What is known from current docs:**
- V Forge owns "execution records and execution lifecycle state" per the data
  ownership map
- the execution scope lifecycle states are derivable from the handoff, return-to-planning,
  and recall interfaces (see Execution Record and Execution Lifecycle Posture section)
- an execution record must carry a reference to the originating confirmed handoff
- activity trail records for the execution scope are linkable via `project_id` and
  the handoff reference

**What remains soft:** The internal field structure — what sub-records an execution
record aggregates, how it relates to individual task records, what "execution lifecycle
state" means as a single field vs. a compound of multiple state dimensions, whether
there is a separate execution session concept below the scope level — is not specified
in any current interface or governance doc.

**Schema-ready posture:** Ownership established; lifecycle states derivable; full
field contract requires V Forge implementation doc pass.

---

### Execution Intelligence Record

**Ownership:** V Forge. Execution intelligence records are the analytical outputs
produced by crossing the content graph against VEDA-delivered signal.

**What is known from current docs:**
- V Forge owns "execution intelligence records" per the data ownership map
- execution intelligence is V Forge-derived from content graph × VEDA signal, not
  raw VEDA data
- execution intelligence must be bounded to approved execution scope
- execution intelligence may contribute to `execution_return` packages when findings
  require planning reconsideration

**What remains soft:** No current interface or governance doc specifies the internal
field structure of execution intelligence records. The distinction between an
"execution intelligence record" and a "bounded execution findings record" that does
not reach the `execution_return` threshold is implied but not formally specified.

**Schema-ready posture:** Ownership and boundary established; full field contract
requires V Forge implementation doc pass.

---

### Bounded Execution Findings Record (Non-Return-to-Planning)

**Ownership:** V Forge. Bounded execution findings records that are resolved within
approved scope — through maintenance, clarification, or execution within approved
bounds — remain V Forge-owned operational records without becoming Project V-facing
deliveries.

**What is known from current docs:**
- V Forge owns "bounded execution findings records" per the data ownership map
- findings that cannot be resolved within approved scope become `execution_return`
  packages (fully contracted above)
- findings resolved within approved scope do not require delivery to Project V and
  remain V Forge-internal

**What remains soft:** No current doc specifies the field structure of findings
records that are resolved internally without triggering return-to-planning. The
distinction in schema terms between an internal finding record and an external
`execution_return` record is the delivery and Project V receipt — but what the
internal record looks like before that determination is made is not specified.

**Schema-ready posture:** Ownership established; the resolved-vs-returned distinction
is clear conceptually; internal field contract requires V Forge implementation doc pass.

---

### Maintenance Execution Record

**Ownership:** V Forge. Maintenance execution records track bounded maintenance work
within already-approved execution scope.

**What is known from current docs:**
- V Forge owns "maintenance execution records" per the data ownership map
- the maintenance and replanning workflow explicitly distinguishes maintenance
  (within approved scope, no replanning required) from replanning (affects planning
  basis)
- maintenance activity may produce findings that escalate to return-to-planning if
  they affect the planning basis; if not, they remain within V Forge

**What remains soft:** No current interface or governance doc specifies the field
structure of maintenance execution records. Whether a maintenance record is a
specialized sub-type of the execution record or a separate entity family is not
established.

**Schema-ready posture:** Ownership established; relationship to execution record and
return-to-planning path is clear; field contract requires V Forge implementation
doc pass.

---

### Content Graph Entity Families (page, topic, entity, internal_link, archetype, schema_usage)

**Ownership:** V Forge. All six named content graph families are V Forge-owned.

**Status:** See Content Graph Entity Family Posture section above.

**Why deferred:** These are the most V Forge-specific schema concerns and have no
current derivation base from interface or governance docs beyond the ownership claim.
They require a dedicated V Forge content graph schema design sub-pass. That sub-pass
should not reopen ownership decisions; it should design the field contracts for each
family and document how they interrelate.

---

## Anti-Drift Rules

**V Forge must not absorb Project V planning truth or VEDA evidence truth.**
V Forge task records and execution records carry thin references to Project V
handoffs and VEDA evidence by identifier and provenance — not by copying content.
An execution record that stores Project V planning records as though they are V
Forge-owned execution records is an ownership blur. A V Forge execution intelligence
record that stores VEDA observatory data as though V Forge generated it violates the
boundary in `ecosystem/cross-system-boundaries.md`.

**`execution_return` does not replace `decision_record`.**
An `execution_return` package is bounded execution findings delivered for planning
reconsideration. When Project V acts on those findings and makes planning decisions,
those decisions become Project V-owned `decision_record` entities. The
`execution_return` entity is the delivery vehicle; it does not become a governing
planning record after receipt.

**Execution intelligence is bounded to approved execution, maintenance, and
return-to-planning support.**
Execution intelligence records must carry a reference to the approved execution scope
or handoff that authorized the research context. Open-ended cross-project or
ecosystem-wide analytical records that V Forge holds without a bounded scope reference
are not within the governed posture and represent boundary drift toward VEDA's
observatory role.

**Content graph records do not authorize planning scope changes.**
A content graph state change (a page is created, a topic is restructured, a link
pattern is modified) is execution truth. It does not by itself authorize a scope
change, a new handoff, or a planning reconsideration. If content graph findings
indicate that planning reconsideration is needed, that finding routes through the
return-to-planning interface — it does not self-authorize planning changes.

**V Forge evidence queries do not authorize observatory scope expansion.**
V Forge's governed evidence queries through `v-forge-evidence-access-contract.md`
provide access to existing VEDA evidence within project scope. A query that returns
no results for a signal class is a coverage gap finding — it routes upstream through
return-to-planning for operator consideration. V Forge cannot self-authorize VEDA to
expand its observatory scope as a consequence of a coverage gap query.

**Handoff-derived scope must remain bounded and queryable.**
Every V Forge task record and execution intelligence record must trace back to an
originating confirmed handoff through `originating_handoff_ref`. V Forge must not
perform execution work that cannot be tied to an approved handoff scope. Tasks or
execution intelligence records without a resolvable `originating_handoff_ref` are
not within the governed execution posture.

**Cross-system references must preserve provenance and stay thin.**
All V Forge references to Project V or VEDA entities must be thin references: the
canonical `entity_id` from the owning system, the `entity_type`, and the minimum
provenance fields. V Forge must not store richer copies of cross-system entity
content than what is required for the referencing record's purpose.

**V Forge must not accumulate VEDA evidence as a persistent local store.**
The anti-drift rule from `interfaces/v-forge-evidence-access-contract.md` applies at
the schema level: V Forge must not define entity schemas that create a persistent
local evidence accumulation pattern. Evidence is queried per session, used, and
attributed. A V Forge entity schema that functions as a local VEDA evidence archive
violates this rule regardless of what the entity is named.

**The content graph schema design sub-pass must not reopen ownership decisions.**
When the V Forge content graph field contracts are designed in a later sub-pass,
that work must take V Forge's ownership of all six content graph families as settled.
It must not attempt to move any content graph entity to VEDA or Project V schema
authority, and it must not redesign the ecosystem boundary model.

---

## Usage

This document should be used:

- when implementing V Forge's task persistence layer: use the `task` entity schema
  contract as the field-level specification; extend through V Forge implementation
  docs for fields not yet derivable from current governance docs
- when implementing the return-to-planning delivery path: use the `execution_return`
  schema contract as the definitive field specification for the findings package
  entity; ensure `finding_boundary_marker` is always set to `true`
- when implementing execution scope state management: use the lifecycle states
  derived in the Execution Record and Execution Lifecycle Posture section as the
  governing state model; extend through V Forge implementation docs
- when implementing execution intelligence record creation: use the schema-facing
  posture and bounded scope requirement in the Execution Intelligence section;
  ensure every intelligence record carries a resolvable `originating_handoff_ref`
- when referencing Project V or VEDA entities from V Forge records: apply the thin
  reference pattern with provenance as defined in the V Forge Cross-System Reference
  Posture section
- when the content graph schema design sub-pass begins: use the Content Graph Entity
  Family Posture section as the authority statement that governs ownership and scope
  of that sub-pass; the sub-pass produces field contracts that extend this document,
  not a separate schema authority
- when V Forge implementation docs need to formalize partially specified entity
  families: use the Partially Specified V Forge Entity Families section as the
  starting point; extend those contracts through V Forge implementation docs, not
  by casually modifying this document

---

## Related Docs

- `ecosystem/ecosystem-schema-spine.md` *(shared enumerated types, activity trail record schema, cross-system reference pattern)*
- `governance/actor-identity-schema-spec.md` *(actor_id value-class contract)*
- `interfaces/data-boundaries.md` *(canonical data ownership map)*
- `interfaces/project-v-to-v-forge-handoff-interface.md` *(handoff semantics — derives task and execution record posture)*
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md` *(return-to-planning semantics — derives execution_return schema)*
- `interfaces/v-forge-evidence-access-contract.md` *(V Forge evidence query posture — informs cross-system reference rules)*
- `interfaces/veda-to-v-forge-signal-interface.md` *(startup signal delivery — informs startup signal cross-system reference)*
- `interfaces/project-v-to-v-forge-execution-clarification-interface.md` *(clarification seam)*
- `interfaces/project-v-handoff-recall-interface.md` *(recall seam)*
- `interfaces/project-v-to-v-forge-scope-update-interface.md` *(scope update seam)*
- `workflows/handoff-workflow.md` *(handoff lifecycle — informs execution scope lifecycle states)*
- `workflows/maintenance-and-replanning-workflow.md` *(replanning workflow — informs return-to-planning posture)*
- `workflows/post-launch-observation-workflow.md` *(post-launch observation — informs execution intelligence posture)*
- `ecosystem/activity-trail-model.md` *(activity trail field contract, entity type vocabulary)*
- `ecosystem/activity-trail-integration-map.md` *(seam-to-action-type mapping)*
- `ecosystem/cross-system-boundaries.md` *(ownership boundaries)*
- `ecosystem/cross-system-access-governance.md` *(access governance, anti-drift rules)*
- `project-v/project-v-schema-authority.md` *(Project V entity schemas — handoff_id and other cross-system reference targets)*
- `veda/veda-schema-authority.md` *(VEDA entity schemas — evidence_id and signal_package_id cross-system reference targets)*
