# Audit Issue-Ready Outputs

Date: 2025-04-05
Repo: `C:\dev\v-ecosystem-docs`

---

## 1. How to use this document

Each issue below is scoped for direct handoff to an implementation or documentation owner. Copy each issue as a GitHub issue, Linear item, or planning card. Issues are ordered by dependency — do not start a later phase until its blockers are resolved. Architectural decision issues (Section 5) must be resolved before their downstream work items can be completed.

These issues arise from the completed five-pass audit and are grouped to match the remediation plan workstreams. They are not exhaustive at the line level; they define the meaningful chunks of work. Sub-tasks within each issue should be tracked inside the issue itself, not split into additional top-level items.

---

## 2. Priority legend

| Level | Meaning |
|---|---|
| **Blocker** | Unsafe to proceed with implementation on the affected path until resolved. Actively misleading or structurally missing. |
| **High** | Required before implementation of the affected system or seam can begin. Does not contain an active misdirection, but leaves a critical gap. |
| **Medium** | Required before the repo is fully implementation-safe, but does not immediately mislead anyone working in adjacent areas. |
| **Low** | Cleanup, consistency, or polish. Can proceed after blockers and high-priority items land. |

---

## 3. Dependency notes

Issues form a directed dependency chain. The four architectural decision issues (ISSUE-AD-01 through ISSUE-AD-04 in Section 5) gate multiple downstream issues and must be resolved before those downstream items are scoped. The chain is:

```
ISSUE-01 (access governance rewrite)
  → ISSUE-02 (known-fixes patches)     [parallel with ISSUE-01]
  → ISSUE-AD-01, AD-02, AD-03, AD-04   [design decisions; gate ISSUE-04, ISSUE-05, ISSUE-07]
  → ISSUE-03 (missing interface stubs)
  → ISSUE-04 (interface contract upgrades)  [AD-01, AD-02 required first]
  → ISSUE-05 (activity trail integration map)
  → ISSUE-06 (activity trail wiring into interface docs)
  → ISSUE-07 (approval mechanics)           [AD-04 required first]
  → ISSUE-08–12 (workflow codability)       [ISSUE-03, ISSUE-07 required first]
  → ISSUE-13–16 (vocabulary / cleanup)      [can begin after ISSUE-02]
```

---

## 4. Issue-ready work items

---

### [ISSUE-01] Rewrite `ecosystem/cross-system-access-governance.md` — active misdirection

**Priority:** Blocker
**Phase:** Phase 0
**Workstream:** WS-A
**Depends on:** None
**Blocks:** All cross-system implementation work; ISSUE-04, ISSUE-05, ISSUE-06

**Problem**
The doc contains at least four direct errors: (1) It declares "VEDA → Project V (Not Applicable)" — the signal interface governs exactly that interaction. (2) It declares "VEDA → V Forge (Not Applicable)" — the V Forge signal interface governs exactly that interaction. (3) It labels the "Project V → V Forge (Execution Results)" access pair with the wrong direction and attributes it to the wrong governing interface (`v-forge-to-project-v-return-to-planning-interface.md` governs V Forge → Project V, not the reverse). (4) It creates an internal contradiction: it simultaneously allows "ecosystem-scoped market scanning" for Project V → VEDA while prohibiting "unscoped queries that return data across all projects."

**Why it matters**
Any implementation team using this doc to understand VEDA's interaction model will conclude that the two primary VEDA signal delivery paths do not exist. This is not a gap — it is wrong in a way that actively misdirects architectural decisions.

**Required work**
- Remove the "VEDA → Project V (Not Applicable)" entry and replace with a correct entry: VEDA → Project V signal delivery is a primary governed interaction governed by `veda-to-project-v-signal-interface.md`
- Remove the "VEDA → V Forge (Not Applicable)" entry and replace with a correct entry: VEDA → V Forge signal delivery is a primary governed interaction governed by `veda-to-v-forge-signal-interface.md`
- Correct the "Project V → V Forge (Execution Results)" entry: fix the direction label (this is V Forge → Project V data flow), correct the governing interface attribution
- Resolve the market-scanning vs unscoped-query contradiction: define what distinguishes permissible "ecosystem-scoped market scanning" from prohibited "unscoped cross-project queries" (or remove the market-scanning carve-out if it cannot be bounded)
- Add entries for the handoff delivery (Project V initiates → V Forge), governed by `project-v-to-v-forge-handoff-interface.md`
- Verify all six system-pair access entries are present, correctly directed, and correctly attributed

**Done means**
- The doc correctly describes the VEDA → Project V and VEDA → V Forge signal delivery paths as primary governed interactions
- No direction-label errors remain
- The market-scanning / unscoped contradiction is resolved with a definition or the carve-out is removed
- All six system-pair access pairs are present with correct governing interface references
- A second reviewer confirms no remaining errors

**Source audit basis**
- Pass 5 Session A Finding A-12; Session B Finding B-10; Session C Finding C-3, C-11

---

### [ISSUE-02] Apply known-fixes patch set and two new confirmed vocabulary corrections

**Priority:** High
**Phase:** Phase 1
**Workstream:** WS-B
**Depends on:** ISSUE-01 (should not conflict, but apply after ISSUE-01 to avoid merge issues)
**Blocks:** ISSUE-13 (vocabulary anchor work)

**Problem**
Seven bounded fixes are already fully specified in `audit-known-fixes-plan.md` but not yet applied. Two additional bounded corrections were confirmed by the audit: the VEDA EventLog is characterized as `append-friendly` in `veda/system-invariants.md` while the schema and model docs both specify `append-only` (no updates, no deletes); and the `handoff-preparation` Work Item Type uses a hyphen in `project-v/controlled-vocabularies.md` while every other multi-word controlled vocabulary value uses underscores.

**Why it matters**
The `append-friendly` / `append-only` discrepancy will produce the wrong VEDA EventLog mutation model. The `handoff-preparation` hyphen is a schema field value inconsistency that will produce validation failures if not corrected before schema implementation.

**Required work**
Apply all seven items from `audit-known-fixes-plan.md` Pass A and B in order. Additionally:
- `veda/system-invariants.md` Invariant 8: change the characterization of event logs from `append-friendly` to `append-only`, consistent with `schema-reference.md` and `observatory-models.md`
- `project-v/controlled-vocabularies.md` Work Item Type: change `handoff-preparation` to `handoff_preparation` (underscore) to match all other controlled vocabulary values

**Done means**
- All items in `audit-known-fixes-plan.md` marked complete
- `veda/system-invariants.md` Invariant 8 uses `append-only` for event logs
- `project-v/controlled-vocabularies.md` Work Item Type entry uses `handoff_preparation` (underscore)
- No merge conflicts with ISSUE-01

**Source audit basis**
- `audit-known-fixes-plan.md` items 1–7; Pass 2 Session C (append-friendly/append-only finding); Pass 2 Session B (handoff-preparation hyphen finding)

---

### [ISSUE-03] Create stubs for the five missing interface documents

**Priority:** High
**Phase:** Phase 2
**Workstream:** WS-C
**Depends on:** ISSUE-01; ISSUE-AD-01 (for item 1); ISSUE-AD-03 (for item 2)
**Blocks:** ISSUE-04, ISSUE-08, ISSUE-09, ISSUE-12

**Problem**
`interfaces/data-boundaries.md` presents four interfaces as the complete governed set for cross-system data exchange. At least five additional cross-system paths are referenced in other docs as "the governed interface path" with no interface doc existing for them. This directly contradicts the data-boundaries.md completeness claim and leaves the dependent docs' governance mechanisms undefined.

**Why it matters**
The `project-intake-workflow.md` depends on a Project V → VEDA evidence request interface that the signal interface explicitly says is not defined. The `v-forge-integration.md` governance rules are unenforceable without the scope clarification and handoff recall interfaces. The `maintenance-and-replanning-workflow.md` Stage 6 cannot be implemented without the scope update interface.

**Required work**
Create stub interface docs at minimum defining: interaction direction, governing systems, minimum semantic elements the package or request must carry, and a placeholder activity trail logging section. Full field-level specification follows in ISSUE-04.

Docs to create:
1. `interfaces/project-v-to-veda-evidence-request-interface.md` — Project V requesting additional bounded evidence from VEDA (requires ISSUE-AD-03 resolved first)
2. `interfaces/v-forge-to-veda-scope-expansion-request-interface.md` — V Forge requesting VEDA to expand observatory scope (requires ISSUE-AD-01 resolved for transport model; also clarify whether this is a direct V Forge → VEDA call or V Forge → operator → VEDA)
3. `interfaces/project-v-to-v-forge-execution-clarification-interface.md` — Project V providing scope clarification or additional approval to V Forge mid-execution without triggering full return-to-planning
4. `interfaces/project-v-handoff-recall-interface.md` — operator-directed recall of a transferred handoff on which V Forge has not yet acted (distinct from return-to-planning)
5. `interfaces/project-v-to-v-forge-scope-update-interface.md` — Project V notifying V Forge of scope or constraint changes after replanning

Also update `interfaces/data-boundaries.md` Interface-Enforcement Principle to reference nine governed interfaces (not four) once stubs are created.

**Done means**
- All five stub docs exist in `interfaces/`
- Each stub defines: direction, governing systems, minimum semantic elements, placeholder activity trail section
- `interfaces/data-boundaries.md` no longer presents four as the complete set
- No stub contradicts the ecosystem ownership split (planning / observability / execution)

**Source audit basis**
- Pass 5 Session A Finding A-11; Session B (missing VEDA scope expansion path); Session C Finding C-12 and interface coverage gaps section

---

### [ISSUE-04] Upgrade the four primary interface docs from semantic contracts to implementation contracts

**Priority:** High
**Phase:** Phase 2
**Workstream:** WS-D
**Depends on:** ISSUE-01; ISSUE-AD-01 (push/pull model); ISSUE-AD-02 (dual-access model for veda-to-v-forge)
**Blocks:** ISSUE-05, ISSUE-06, ISSUE-07

**Problem**
The four primary cross-system interface docs scored between 0 and 3 of 21 PASS on interface completeness. The VEDA → Project V signal interface and the Project V → V Forge handoff interface both scored 0 of 21 PASS. Both explicitly defer all data structure to "future work." Two teams implementing these interfaces independently will produce incompatible schemas.

**Why it matters**
Without field definitions, every implementation team invents the payload structure. The resulting interoperability failure between Project V and V Forge at handoff time is the most operationally dangerous gap in the repo.

**Required work**
For each of the four docs, add:
- Named payload fields with types and constraints (or required semantic fields with explicit statement that concrete types are TBD pending schema docs)
- Freshness and timestamp requirements: at minimum `gathered_at`, a validity window reference, and `trust_classification` where applicable
- Degraded-mode section: what the caller does when the responder is unavailable, stale, or returns an error
- Recovery path: what happens after degraded mode ends
- Cost accounting acknowledgment: whether this interface incurs token or API cost, and whether costs are attributed to the caller

Docs to upgrade (in dependency order):
1. `interfaces/veda-to-project-v-signal-interface.md` — 18 FAILs; highest priority for complete upgrade
2. `interfaces/project-v-to-v-forge-handoff-interface.md` — 18 FAILs; handoff payload structure is the most operationally load-bearing gap
3. `interfaces/v-forge-to-project-v-return-to-planning-interface.md` — already has the boundary constraint note from ISSUE-02; still needs full implementation structure
4. `interfaces/veda-to-v-forge-signal-interface.md` — must reconcile the architectural question from ISSUE-AD-02 before this upgrade can be correct

The `v-forge-evidence-access-contract.md` is the implementation target model — use it as the structural template.

**Done means**
- Each of the four upgraded interface docs has: named payload fields or explicit semantic field definitions, freshness metadata section, degraded-mode caller behavior, recovery path, and cost accounting acknowledgment
- Each doc would score at minimum 12 of 21 PASS on a Pass 3 re-audit (the evidence access contract benchmark)
- The veda-to-v-forge-signal-interface.md is consistent with the ISSUE-AD-02 design decision
- No upgraded doc contradicts the ecosystem ownership split

**Source audit basis**
- Pass 3 findings for veda-to-project-v-signal-interface.md (0 PASS), project-v-to-v-forge-handoff-interface.md (0 PASS), v-forge-to-project-v-return-to-planning-interface.md, veda-to-v-forge-signal-interface.md; Pass 5 Session B Finding B-1, B-11

---

### [ISSUE-05] Create `ecosystem/activity-trail-integration-map.md`

**Priority:** High
**Phase:** Phase 3
**Workstream:** WS-E
**Depends on:** ISSUE-04 (interface contracts must exist before the map can be complete); ISSUE-03 (stub docs must exist to be mapped)
**Blocks:** ISSUE-06

**Problem**
The activity trail model defines a dot-namespaced action vocabulary and required fields. No reference document exists that maps cross-system interaction types to their action types, producing systems, and required fields. Implementations must infer this mapping independently.

**Why it matters**
Without a central integration map, every implementation team must independently discover which activity trail action type applies to each cross-system event. Results will diverge. The most governance-significant events (handoff creation, signal transfer, return-to-planning delivery) currently have no activity trail specification in their governing interface docs.

**Required work**
Create `ecosystem/activity-trail-integration-map.md` as a reference table. For each of the nine cross-system interface types (four existing + five new from ISSUE-03), define:
- Interaction type and direction
- Applicable activity trail action type (dot-namespaced)
- Which system is responsible for producing the activity record (`actor_system`)
- Which existing vocabulary item maps to `entity_type` and `entity_id`
- Whether `token_cost` and/or `api_cost_cents` apply
- Any cross-doc notes or known gaps

Additionally, identify the following action vocabulary gaps in `ecosystem/activity-trail-model.md` and extend the vocabulary to cover them:
- Return-to-planning delivery (V Forge → Project V) — no current action type covers this as a cross-system push event
- Project V lifecycle stage transitions that are cross-system-relevant (Handed Off, Return Under Reconsideration) — no lifecycle state action type currently exists

Reconcile the evidence access contract's 8-field logging schema with the activity trail's required fields: the contract's `actor` field must map to `actor_type` + `actor_id` + `actor_system`; the contract's `action` value `veda_evidence_query` must align to the canonical `evidence.query` (dot-namespaced).

**Done means**
- `ecosystem/activity-trail-integration-map.md` exists and covers all nine governed interfaces
- `ecosystem/activity-trail-model.md` action vocabulary includes a type for return-to-planning delivery and Project V lifecycle transitions
- The evidence access contract's logging schema is either aligned to the canonical trail format or the divergence is explicitly documented with a governing reason
- The map can be used by an implementer to know exactly which action type to log for any cross-system event

**Source audit basis**
- Pass 3 findings AL-1/AL-2/AL-3 across all primary interface docs; Pass 5 Session B Finding B-2, B-4, B-5; Session C Finding C-4, C-5, C-6; audit-master-summary.md Section 6 Cluster 2

---

### [ISSUE-06] Wire activity trail logging into all interface docs

**Priority:** High
**Phase:** Phase 3
**Workstream:** WS-E
**Depends on:** ISSUE-05 (integration map must exist first)
**Blocks:** ISSUE-08–12 (workflow docs can reference these once wired)

**Problem**
None of the four primary interface docs contain logging requirements. The only interface doc with activity trail logging specification is the evidence access contract. Every other interface doc governing a cross-system event — including handoff creation, handoff approval, signal delivery, and return-to-planning — will produce no activity trail record in implementations built against the current docs.

**Why it matters**
The activity trail is the primary mechanism for making ecosystem governance auditable. Without logging requirements in the interface docs, implementations will produce a trail with systematic gaps at the most consequential cross-system events.

**Required work**
Add an explicit "Activity Trail" section to each of the nine interface docs (four existing + five new stubs from ISSUE-03). Each section must specify:
- Which action type applies (from the integration map created in ISSUE-05)
- Which system produces the activity record
- Which fields are required for this action type (minimum: `action`, `action_class`, `actor_system`, `entity_type`, `entity_id`, `target_system`, `project_id`)
- Whether cost fields (`token_cost`, `api_cost_cents`) apply

For interface docs with approval events (handoff, return-to-planning), also specify logging for `approval.request` and `approval.decide` events within the same section.

**Done means**
- All nine interface docs have an explicit activity trail section
- Each section references the correct action type from the integration map
- The producing system is unambiguously identified
- No interface doc governing a cross-system event is silent on logging requirements

**Source audit basis**
- Pass 3 findings AL-1/AL-2/AL-3 for all primary interface docs; audit-master-summary.md Section 6 Cluster 2

---

### [ISSUE-07] Define human approval flow mechanics at the seam level

**Priority:** High
**Phase:** Phase 3
**Workstream:** WS-F
**Depends on:** ISSUE-04 (interface contracts); ISSUE-AD-04 (centralized vs distributed approval mechanics location)
**Blocks:** ISSUE-08, ISSUE-09, ISSUE-11

**Problem**
Every interface doc and workflow doc that involves human approval defers to `governance/approval-and-escalation-model.md`. The governance model defines classes and principles but not the seam-level mechanics: which system initiates the approval request, what state the workflow enters while pending, what the human must do, and how the result re-enters the workflow.

**Why it matters**
Without seam-level mechanics, approval flows cannot be implemented. Every implementation team will independently decide which system generates the request and how the result re-enters the process. Results will diverge, producing inconsistent governance behavior across the ecosystem.

**Required work**
For each of the four governance-sensitive transitions, define the mechanics:

1. **Handoff activation** (Project V → V Forge): which system generates the approval request; what state Project V enters (Awaiting-Approval-or-Activation is named in the operational workflow but not wired to the handoff interface); what the request must contain per the approval-and-escalation-model.md Approval Request Principle; how the approval result triggers Stage 4 → Stage 5 in handoff-workflow.md

2. **Return-to-planning receipt** (V Forge → Project V): which system generates the review request when human review is required; what triggers the review requirement (the return interface lists conditions but not mechanics); how the review result re-enters Project V replanning

3. **Launch authorization** (launch-readiness-workflow.md Stage 5): which system generates the Stage 5 authorization request; what the Stage 4 cross-system readiness confirmation looks like as a concrete artifact; how the authorization record is structured; what triggers Stage 6

4. **Replanning with prior decision supersedence** (maintenance-and-replanning-workflow.md Stage 5): when replanning supersedes or invalidates a prior governing decision, who initiates human review and what state the workflow enters

Per ISSUE-AD-04 resolution: either add these mechanics to each relevant interface doc, or create `governance/approval-mechanics-seam-model.md` and reference it from each interface doc.

**Done means**
- For each of the four transitions: a developer can determine from the docs which system initiates, what the request contains, what state the workflow is in while pending, what the human does, and how the result re-enters the workflow
- No governance-sensitive transition requires a developer to "see approval-and-escalation-model.md" without further guidance
- The mechanics are consistent with the approval class definitions in the Tier 1 governance model

**Source audit basis**
- Pass 4 WF-10/WF-15/WF-16 across all five workflow docs; Pass 5 Session C Finding C-10; audit-master-summary.md Section 3 and Section 5 Blocker 6

---

### [ISSUE-08] Repair `workflows/handoff-workflow.md` codability

**Priority:** High
**Phase:** Phase 4
**Workstream:** WS-G
**Depends on:** ISSUE-03, ISSUE-07
**Blocks:** None (most operationally critical workflow but no downstream doc dependencies)

**Problem**
The handoff workflow scored 2 of 21 PASS on codability. The three-state model (handoff-prepared / awaiting-approval / actively-handed-off) is a valid starting skeleton but none of the six stages have entry or exit conditions, transition triggers are undefined, human approval mechanics at Stage 3 are undefined, escalation paths are named but not routed, and state changes are not defined as observable events.

**Why it matters**
This workflow governs the most consequential cross-system boundary crossing in the ecosystem. Implementing it without transition triggers means each implementation invents all progression logic.

**Required work**
Add to the doc:
- Stage entry/exit condition table: for each of the six stages, testable entry condition and testable exit condition
- Transition trigger table: from-stage, named trigger event or condition, to-stage, guard condition, failure disposition
- Escalation routing: what condition triggers escalation, who receives it, what state the workflow enters, what closes escalation and how the result re-enters
- Observable state section: which stage transitions must produce an activity trail record (reference ISSUE-06 wiring)
- Wire Stage 3 human approval to the mechanics defined in ISSUE-07

The "Awaiting State Principle" and the existing two re-entry paths (return to Stage 1 or Stage 2 on pending invalidation) are partial structure worth preserving and extending.

**Done means**
- Every stage has a testable entry condition and testable exit condition
- Every forward transition has a named trigger
- Human approval at Stage 3 references concrete mechanics (from ISSUE-07)
- Escalation paths are routed (not listed as an option alongside others with no destination)
- The workflow would score "Partially codable, follow-up needed" or better on a Pass 4 re-audit

**Source audit basis**
- Pass 4 findings-pass-4-handoff-workflow.md (2 PASS / 7 PARTIAL / 12 FAIL); audit-remediation-plan.md Section 5 Phase 4

---

### [ISSUE-09] Repair `workflows/project-intake-workflow.md` codability

**Priority:** High
**Phase:** Phase 4
**Workstream:** WS-G
**Depends on:** ISSUE-03 (evidence request interface must exist), ISSUE-07
**Blocks:** None

**Problem**
The project-intake workflow scored 3 of 21 PASS — the lowest codability score of the five workflow docs. No stage has entry or exit conditions. The "request additional bounded evidence" outcome in Stage 5 depends on a cross-system path (Project V → VEDA) that has no governing interface doc. Escalation is not mentioned anywhere in the workflow body.

**Why it matters**
This is the entry point for all planning work. Inventing the intake workflow logic includes inventing how planning-relevant signal becomes an intake question, how governance gates are applied, and how additional evidence is requested — load-bearing decisions with no specification.

**Required work**
- Stage entry/exit condition table for all six stages
- Transition trigger table covering forward path and the one currently-defined re-entry path (Stage 6 back to Stage 2 or Stage 3 after additional evidence)
- Define what constitutes "planning-relevant signal" as a testable Stage 1 guard
- Define the evaluation logic for when human review is required at Stage 4 as a testable condition
- Add escalation routing section
- Wire the "request additional bounded evidence" outcome to the interface created in ISSUE-03 item 1
- Wire human approval to mechanics from ISSUE-07

**Done means**
- All six stages have testable entry and exit conditions
- "Request additional bounded evidence" references a concrete interface path
- The workflow would score "Partially codable, follow-up needed" or better on a Pass 4 re-audit

**Source audit basis**
- Pass 4 findings-pass-4-project-intake-workflow.md (3 PASS / 5 PARTIAL / 13 FAIL); Pass 5 Session A Finding A-11

---

### [ISSUE-10] Repair `workflows/maintenance-and-replanning-workflow.md` codability

**Priority:** Medium
**Phase:** Phase 4
**Workstream:** WS-G
**Depends on:** ISSUE-07
**Blocks:** None

**Problem**
The maintenance-and-replanning workflow scored 2 of 21 PASS but has the strongest partial structure: a six-condition trigger list, four non-trigger conditions, a maintenance/replanning fast-path distinction, and a concrete Stage 5 escalation overflow condition. Stage-level entry/exit conditions, forward transition triggers, and escalation routing mechanics are still absent.

**Why it matters**
Return-triggered replanning is one of the most governance-sensitive activities in the ecosystem. Without transition triggers, the strong trigger list at the workflow level does not translate into per-stage codable behavior.

**Required work**
- Stage entry/exit condition table for all six stages, building on the existing trigger list
- Transition trigger table for all forward transitions and the currently-defined escalation overflow path (Stage 5 → escalation when scope cannot be bounded)
- Define the escalation path: who receives it, what state the workflow enters, what closes escalation
- Define the "materially changed conditions" detection logic for the Stage 2 pending-invalidation case as a concrete guard
- Wire Stage 5 human review to mechanics from ISSUE-07
- Add the post-replanning scope notification path (references interface from ISSUE-03 item 5)

**Done means**
- All six stages have testable entry and exit conditions
- The Stage 5 escalation overflow condition has a concrete routing path
- The workflow would score "Partially codable, follow-up needed" or better on a Pass 4 re-audit

**Source audit basis**
- Pass 4 findings-pass-4-maintenance-and-replanning-workflow.md (2 PASS / 9 PARTIAL / 10 FAIL)

---

### [ISSUE-11] Repair `workflows/launch-readiness-workflow.md` codability

**Priority:** Medium
**Phase:** Phase 4
**Workstream:** WS-G
**Depends on:** ISSUE-07
**Blocks:** None

**Problem**
The launch-readiness workflow scored 2 of 21 PASS. It has meaningful partial structure (seven explicit blocking conditions, stale-stage re-assessment rule, per-stage actor assignments) but no per-stage entry/exit conditions, no transition triggers, and the Stage 4 cross-system confirmation has no defined mechanics.

**Why it matters**
Launch authorization is Class C in the approval model — the highest governance class for execution. The Stage 4 four-system convergence is the most complex transition in the ecosystem and currently has no implementation contract.

**Required work**
- Stage entry/exit condition table for all seven stages
- Transition trigger table, with special attention to Stage 3 → Stage 4 (all three systems must complete their assessments) and Stage 4 → Stage 5 (cross-system confirmation must be a concrete artifact)
- Define what "cross-system readiness confirmation" looks like as a concrete record or signal at Stage 4
- Define the evidence materiality threshold for Stage 2 (currently deferred to evidence-continuity-model.md; must be specified or formally referenced as a testable condition)
- Wire Stage 5 authorization to mechanics from ISSUE-07
- Add escalation routing section

**Done means**
- All seven stages have testable entry and exit conditions
- Stage 4 cross-system confirmation is a defined concrete artifact
- The workflow would score "Partially codable, follow-up needed" or better on a Pass 4 re-audit

**Source audit basis**
- Pass 4 findings-pass-4-launch-readiness-workflow.md (2 PASS / 8 PARTIAL / 11 FAIL)

---

### [ISSUE-12] Repair `workflows/post-launch-observation-workflow.md` codability

**Priority:** Medium
**Phase:** Phase 4
**Workstream:** WS-G
**Depends on:** ISSUE-03 (for Stage 6 escalation routing), ISSUE-07
**Blocks:** None

**Problem**
The post-launch-observation workflow scored 2 of 21 PASS and is the most structurally advanced of the five. It has a formal entry condition, four named Stage 6 outcome paths, and the best inter-stage traceability language. The remaining gaps are two undefined key operational concepts and no per-stage exit conditions.

**Why it matters**
"Governed intervals" and "materially significant signal event" are the two trigger concepts for Stage 5 review. Both are operationally undefined. Without them, the review cycle has no triggering mechanism.

**Required work**
- Define "governed intervals" concretely: specify duration, cadence, who sets them, and where they are configured
- Define "materially significant signal event" with a threshold or classification rule sufficient to implement a trigger condition
- Define the "initial post-launch capture window" duration referenced in Stage 2
- Add per-stage exit conditions for all six stages
- Define escalation routing for the Stage 6 escalation outcome: who receives it, what state the workflow enters, how the result re-enters the four-path outcome logic
- Wire Stage 6 escalation to mechanics from ISSUE-07

**Done means**
- "Governed intervals" has a concrete definition or specification reference
- "Materially significant signal event" has a testable threshold or classification rule
- All six stages have exit conditions
- The workflow would score "Partially codable, follow-up needed" or better on a Pass 4 re-audit

**Source audit basis**
- Pass 4 findings-pass-4-post-launch-observation-workflow.md (2 PASS / 9 PARTIAL / 10 FAIL)

---

### [ISSUE-13] Add canonical definitions for five undefined load-bearing terms to `ecosystem/vocabulary.md`

**Priority:** Medium
**Phase:** Phase 5
**Workstream:** WS-H
**Depends on:** ISSUE-02 (known-fixes patches applied); ISSUE-07 (approval mechanics clarify scope of "governance-sensitive")
**Blocks:** None

**Problem**
Five terms are used throughout the governance and ecosystem docs to drive approval, escalation, and boundary behavior but have no canonical definitions: `operator`, `governance-sensitive`, `material/materiality`, `scope excess`, and `task`. A sixth missing term: there is no canonical name for the bounded scope transferred at handoff (currently expressed four ways: `handoff scope`, `execution scope`, `bounded execution scope`, `handed-off scope`, `admitted scope`).

**Why it matters**
Undefined terms produce implementation-divergent behavior. "Governance-sensitive" in particular is used to determine when approval is required; two implementations using different thresholds will produce different governance outcomes for the same actions.

**Required work**
Add canonical definitions to `ecosystem/vocabulary.md` for:
- `operator` — define the actor class; distinguish from system, agent, and LLM roles
- `governance-sensitive` — define the class of actions that require special approval posture; must be consistent with `governance/approval-and-escalation-model.md` Governance-Sensitive Action Principle
- `material / materiality` — define the threshold concept; reference or align with the materiality definitions already present in `decision-continuity-doctrine.md` and `daily-report-doctrine.md`
- `scope excess` — define the boundary condition; must be consistent with V Forge Invariant 13's halt trigger
- `task` — define the runtime unit of work referenced in the action vocabulary and agent lifecycle events
- Choose one canonical term for the bounded scope transferred at handoff and add it as a vocabulary entry; update the four docs that use divergent terms to reference the canonical term

**Done means**
- All six terms/concepts have entries in `ecosystem/vocabulary.md`
- The `governance-sensitive` definition is consistent with the approval model's Governance-Sensitive Action Principle
- The materiality definition is consistent with usages in decision-continuity-doctrine.md
- The canonical handoff scope term is used consistently across all primary docs that reference the concept

**Source audit basis**
- Pass 2 Session A findings (operator, governance-sensitive, material/materiality, scope excess, task); Pass 2 Session B finding (handoff scope term sprawl)

---

### [ISSUE-14] Specify the `actor` field format as a governed type in Project V schema

**Priority:** Medium
**Phase:** Phase 5
**Workstream:** WS-H
**Depends on:** ISSUE-02
**Blocks:** None

**Problem**
The `actor` field is required on every `StatusHistory`, `DecisionRecord`, and `AuditRun` record in Project V. It is described in `controlled-vocabularies.md` as "server-resolved from the authenticated request context — free text — guidance only." This is not a type specification. An implementation cannot produce consistent actor attribution without a defined format.

**Why it matters**
Every governed transition in Project V requires an `actor` record. If the format is free text, different sessions and different implementations will use different formats, making cross-session audit reconstruction unreliable.

**Required work**
- Define a concrete `actor` field format in `project-v/controlled-vocabularies.md`: specify whether the value is a user ID, a structured type-identifier pair (e.g., `agent:agent-id-123`), or an enum of actor types
- The format must be compatible with the activity trail's `actor_type` + `actor_id` + `actor_system` field structure so that Project V status history records can be correlated with the ecosystem activity trail
- Remove the "free text — guidance only" characterization and replace with a governed type specification
- Reference the format from `project-v/schema-specification.md` wherever the `actor` field appears

**Done means**
- The `actor` field has a governed type specification (not "free text")
- The format is compatible with the activity trail's actor field structure
- An implementer can produce consistent `actor` values from the spec without guessing

**Source audit basis**
- Pass 2 Session B finding (actor field format undefined); audit-remediation-plan.md Section 9 exit criteria

---

### [ISSUE-15] Remove or archive stale superseded docs from active folders

**Priority:** Low
**Phase:** Phase 5
**Workstream:** WS-H
**Depends on:** None
**Blocks:** None

**Problem**
Pass 1 identified 14 `interfaces/extension-*` docs that are self-declared superseded but remain in the active `interfaces/` folder. Additionally, `project-v/operator-surfaces/vscode-extension.md` references the VS Code extension as the active operator surface, but the active host is the Tauri 2 desktop per ADR-011.

**Why it matters**
Superseded docs in active folders are misleading to anyone navigating the repo. They consume audit scope and may confuse implementation teams.

**Required work**
- Move all 14 `interfaces/extension-*` docs to `archive/` or add an explicit `## Status: Superseded` header with a reference to the replacement doc
- Review `project-v/operator-surfaces/vscode-extension.md` and determine whether it should be archived, retitled, or updated to reflect the current desktop host
- Verify no active docs in the repo have `*(planned)*` markers for docs that now exist and are complete; update or remove stale markers

**Done means**
- No self-declared superseded docs remain in active folders without clear supersession markers
- `vscode-extension.md` disposition is resolved (archived, retitled, or updated)
- No known stale `*(planned)*` markers reference existing complete docs

**Source audit basis**
- Pass 1 findings (stale superseded docs); Pass 2 out-of-scope observations (stale host references in multiple sessions)

---

### [ISSUE-16] Resolve the `v-forge/vs-veda.md` ADR-003 dangling reference

**Priority:** Low
**Phase:** Phase 5
**Workstream:** WS-H
**Depends on:** None
**Blocks:** None

**Problem**
`v-forge/vs-veda.md` references "the VEDA Brain prohibition (ADR-003)" as the governing authority for one of its drift-prevention rules. ADR-003 was not found in the repo. `veda/system-invariants.md` Invariant 6 covers the same constraint without an ADR reference.

**Why it matters**
A dangling authority reference makes the governing rule appear weaker than it is and prevents future reviewers from tracing the decision chain.

**Required work**
- Verify whether ADR-003 exists elsewhere in the repo (check `ecosystem/decisions/`)
- If ADR-003 exists: add the correct path reference
- If ADR-003 does not exist: replace the ADR reference with a reference to `veda/system-invariants.md` Invariant 6, which covers the same constraint; optionally create a formal ADR for the record if the team decides it warrants one

**Done means**
- The VEDA Brain prohibition reference in `v-forge/vs-veda.md` points to a doc that exists
- No dangling authority citations remain for this constraint

**Source audit basis**
- Pass 5 Session B Finding B-9; out-of-scope observation

---

## 5. Architectural decision issues

These four items are design decisions, not documentation fixes. They gate downstream work items and cannot be completed by a doc author working independently. They require a technical decision from the team. Each should be tracked as a decision record or ADR once resolved.

---

### [ISSUE-AD-01] Resolve the push/pull transport model for handoff and signal delivery

**Priority:** Blocker (gates ISSUE-04, ISSUE-07, ISSUE-08)
**Phase:** Phase 1 (must resolve before Phase 2 work begins)
**Workstream:** Architectural decision
**Depends on:** None
**Blocks:** ISSUE-04 (handoff and veda-to-project-v signal interface upgrades), ISSUE-07 (approval mechanics), ISSUE-08 (handoff workflow codability)

**Problem**
The interface docs are inconsistent on whether the handoff and signal delivery interactions are push (initiating system delivers) or pull (receiving system queries). `veda-to-project-v-signal-interface.md` describes VEDA as providing signal to Project V; the activity trail's `signal.query` implies Project V queries VEDA. `project-v-to-v-forge-handoff-interface.md` describes Project V providing the package; the access governance doc frames it as V Forge reading. The implementation contract for these interfaces and the approval flow mechanics both depend on which model is correct.

**Decision required**
For each of the two interactions:
- **VEDA → Project V signal delivery:** push (VEDA packages and pushes to Project V) or pull (Project V polls or queries VEDA for available signal)?
- **Project V → V Forge handoff delivery:** push (Project V delivers the package to V Forge on activation) or pull (V Forge polls or queries Project V for active handoffs)?

The same transport question applies to VEDA → V Forge signal delivery per ISSUE-AD-02.

**Required work**
- Make and document the transport model decision for each interaction
- Create a decision record (ADR or equivalent) documenting the decision and rationale
- Use the decision to update the interface docs in ISSUE-04

**Done means**
- The transport model for each interaction is documented
- `veda-to-project-v-signal-interface.md` and `project-v-to-v-forge-handoff-interface.md` implementation contract work (ISSUE-04) can proceed
- ISSUE-07 approval mechanics can be specified correctly for the chosen model

**Source audit basis**
- Pass 5 Session A Finding A-1; Session C Finding C-1; audit-remediation-plan.md Section 7 design questions

---

### [ISSUE-AD-02] Reconcile the dual access model for VEDA → V Forge

**Priority:** Blocker (gates ISSUE-04 for veda-to-v-forge-signal-interface.md)
**Phase:** Phase 1
**Workstream:** Architectural decision
**Depends on:** ISSUE-AD-01 (related transport model questions)
**Blocks:** ISSUE-04 (veda-to-v-forge-signal-interface upgrade)

**Problem**
The VEDA → V Forge interaction is governed by two docs that describe fundamentally different access architectures. `veda-to-v-forge-signal-interface.md` describes a "bounded, largely passive channel" with MCP-tool-call-mediated access. `v-forge-evidence-access-contract.md` describes an active query model with four named query types (`evidence_by_project`, `evidence_by_topic`, `signal_status`, `evidence_by_id`) and no mention of MCP mediation. The evidence access contract explicitly states the passive channel model "starves V Forge agents of the evidence they need."

**Decision required**
Are these two models:
- (A) Two distinct layers — signal interface covers bulk/scheduled signal package delivery; evidence access contract covers on-demand query during execution — that are both active simultaneously? If so, the signal interface must acknowledge the query layer exists.
- (B) A supersession — the evidence access contract supersedes the passive signal interface for all V Forge access to VEDA? If so, the signal interface must be updated to defer to the contract.
- (C) Something else requiring a different reconciliation?

**Required work**
- Make and document the reconciliation decision
- Update `veda-to-v-forge-signal-interface.md` and `v-forge-evidence-access-contract.md` to be consistent with the decision
- Resolve the transport mechanism: the signal interface says MCP tool call; the evidence access contract describes direct API queries — which governs, or do they coexist at different layers?

**Done means**
- The two docs agree on how V Forge accesses VEDA signal
- The transport mechanism (MCP-mediated vs direct API) is defined consistently
- ISSUE-04's veda-to-v-forge upgrade can proceed

**Source audit basis**
- Pass 5 Session B Finding B-1, B-11; audit-remediation-plan.md Section 7 design questions

---

### [ISSUE-AD-03] Define the Project V → VEDA evidence request path model

**Priority:** High (gates ISSUE-03 item 1, ISSUE-09)
**Phase:** Phase 1
**Workstream:** Architectural decision
**Depends on:** ISSUE-AD-01 (related transport model)
**Blocks:** ISSUE-03 item 1 (evidence request interface stub), ISSUE-09 (project-intake workflow codability)

**Problem**
The project-intake-workflow.md depends on a "request additional bounded evidence" path from Project V to VEDA. `veda-to-project-v-signal-interface.md` explicitly defers this path: "any path from Project V back to VEDA is a separate interface and is not defined here." No interface doc exists for this path. Before ISSUE-03 item 1 can specify the interface beyond a stub, the path model must be decided.

**Decision required**
- Is the Project V → VEDA evidence request a direct API call (Project V queries VEDA's API with specific evidence parameters)?
- Is it a notification/request model (Project V notifies VEDA to produce a bounded signal package on a specific topic)?
- Is it operator-mediated (Project V surfaces an operator instruction; the operator directs VEDA through the operator surface)?
- Or is "request additional bounded evidence" actually handled through the existing VEDA → Project V signal interface (Project V marks itself as needing more signal; VEDA delivers when available), with no separate interface required?

**Required work**
- Make and document the path model decision
- The decision directly determines what ISSUE-03 item 1 specifies and whether the interface is Project V → VEDA or a different arrangement

**Done means**
- The evidence request path model is documented
- ISSUE-03 item 1 (interface stub) and ISSUE-09 (intake workflow) can proceed with the correct model

**Source audit basis**
- Pass 5 Session A Finding A-11; audit-remediation-plan.md Section 7 design questions

---

### [ISSUE-AD-04] Decide whether approval mechanics live in interface docs or a centralized model

**Priority:** High (gates ISSUE-07 approach)
**Phase:** Phase 1
**Workstream:** Architectural decision
**Depends on:** None
**Blocks:** ISSUE-07 (approval mechanics)

**Problem**
The remediation plan identified that seam-level approval mechanics must be defined for four governance-sensitive transitions. These mechanics can live as: (A) additions to each relevant interface doc (distributed — mechanics co-located with the interface they govern); or (B) a single new `governance/approval-mechanics-seam-model.md` referenced from each interface doc (centralized — one place to find all approval mechanics). Both approaches are valid; the choice affects what ISSUE-07 produces.

**Decision required**
Where do approval flow mechanics for the four governance-sensitive transitions live?
- Distributed: in each interface doc
- Centralized: in a new governance doc referenced from each interface doc

Considerations: the centralized approach is cleaner if the mechanics pattern is consistent across transitions; the distributed approach keeps each interface doc self-contained.

**Required work**
- Make and document the structural decision
- Use the decision to specify the output of ISSUE-07

**Done means**
- The location decision is documented
- ISSUE-07 knows exactly what artifacts to create

**Source audit basis**
- audit-remediation-plan.md Section 7 design questions; audit-master-summary.md Section 6 Cluster 3

---

## 6. Suggested first implementation batch

Open and begin these issues immediately, in dependency order:

1. **ISSUE-01** — Rewrite access governance doc (no dependencies; must happen first)
2. **ISSUE-02** — Apply known-fixes patch set (can begin immediately after ISSUE-01)
3. **ISSUE-AD-01, AD-02, AD-03, AD-04** — Architectural decisions (can be run in parallel as a decision sprint; gate everything downstream)

After decisions and ISSUE-01 are complete:

4. **ISSUE-03** — Create five missing interface stubs (items 3, 4, 5 can start before AD-01/AD-03 resolve; items 1 and 2 need AD-01 and AD-03)
5. **ISSUE-05** — Create activity trail integration map (can start drafting once ISSUE-03 stubs exist)

---

## 7. Suggested parallel batch

After the first batch completes and architectural decisions are resolved, these can proceed in parallel:

- **ISSUE-04** and **ISSUE-06** — Interface upgrades and activity trail wiring (ISSUE-04 first, then ISSUE-06 follows)
- **ISSUE-13** — Vocabulary anchor additions (does not depend on ISSUE-04)
- **ISSUE-14** — Actor field specification (does not depend on ISSUE-04)
- **ISSUE-10** and **ISSUE-12** — Maintenance-and-replanning and post-launch-observation workflow codability (these have fewer missing interface dependencies than ISSUE-08 and ISSUE-09)

After ISSUE-07 (approval mechanics) is complete:

- **ISSUE-08**, **ISSUE-09**, **ISSUE-11** — Handoff, project-intake, and launch-readiness workflow codability (these depend on ISSUE-07)

---

## 8. Deferred cleanup batch

Open these after the blocker and high-priority batches are complete:

- **ISSUE-15** — Archive stale superseded docs (no functional dependency; can proceed anytime but low urgency)
- **ISSUE-16** — ADR-003 dangling reference in vs-veda.md (similarly low urgency)
- Pass 4 re-audit — run after ISSUE-08 through ISSUE-12 are complete to verify workflows reach codable threshold
- Desktop interface doc refresh — after the core ecosystem seam work is complete, the desktop docs need a targeted completeness pass for activity trail, cost accounting, and threshold specificity
- `ecosystem-docs-execution-plan.md` disposition — revisit after Phase 4 complete

---

## 9. Closing note

The issue list above is intentionally compact. The goal is 16 substantial issues (plus 4 decision gates) that represent the real work — not 80 fragmented chores. Each issue above covers a coherent body of work that can be assigned to one person or pair without ambiguity about scope.

The four architectural decisions (ISSUE-AD-01 through AD-04) are the critical path through the early phases. They cannot be resolved by a doc author working alone; they require team input on transport model and structural choices. Everything in Phases 2–4 that touches the interface contracts or approval mechanics will be built on those decisions. Resolve them first.

The ownership split — Project V owns planning truth, VEDA owns signal/evidence/observability truth, V Forge owns execution truth — is correct and consistent throughout the repo. The work in this issue list does not challenge that split. It builds the implementation contracts, transition mechanics, and logging requirements needed to make that split operational rather than aspirational.
