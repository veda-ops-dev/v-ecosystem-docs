# Audit Remediation Plan

Date: 2025-04-05
Repo: `C:\dev\v-ecosystem-docs`

---

## 1. Planning premise

The completed five-pass audit established that the V Ecosystem documentation set is not ready for disciplined implementation of the cross-system interfaces, workflow state machines, or activity trail. The architectural ownership model (Project V = planning truth, VEDA = signal/evidence/observability truth, V Forge = execution truth) is correct and consistent. Everything below that level — the data contracts, transition mechanics, logging requirements, and approval flows — is either missing, deferred, or actively contradictory.

Proceeding to implementation against the current docs would produce: incompatible handoff schemas between Project V and V Forge (because both sides would invent the payload structure independently), a governance activity trail that does not capture the most significant cross-system events (handoff creation, signal transfer, return-to-planning delivery), workflows that cannot be encoded because their transition triggers do not exist, and an access governance doc that actively misdirects anyone reading it about how VEDA interacts with other systems.

This plan defines the work required to close those gaps in dependency order.

---

## 2. Remediation goals

1. Eliminate documentation that actively contradicts correct behavior (`cross-system-access-governance.md`)
2. Create the five missing interface documents that other docs already depend on
3. Convert the four primary interface docs from semantic contracts to implementation contracts
4. Wire activity trail logging requirements into every doc that governs a cross-system action
5. Add per-stage operational structure to the five workflow docs so they can be encoded
6. Define human approval flow mechanics at the seam level
7. Anchor the undefined load-bearing vocabulary terms
8. Leave the three-system ownership split intact and unmodified throughout

---

## 3. Implementation blockers

These items make implementation unsafe right now. Do not begin writing code for the affected paths until these are resolved.

**Blocker 1 — `cross-system-access-governance.md` is actively misleading.**
It declares VEDA → Project V and VEDA → V Forge "Not Applicable" — the opposite of what the signal interface docs govern. It inverts the direction label and governing interface for the return-to-planning access pair. It contains an internal contradiction about ecosystem-scoped vs project-scoped access. Any implementation team using this doc for access model guidance will build the wrong thing.

**Blocker 2 — The handoff interface and signal interface have no data contracts.**
`project-v-to-v-forge-handoff-interface.md` and `veda-to-project-v-signal-interface.md` both scored 0 of 21 PASS on interface completeness and both explicitly defer all field definitions to future work. Two teams implementing these interfaces independently will produce incompatible schemas.

**Blocker 3 — Five cross-system paths are referenced as "the governed interface path" but have no governing interface doc.**
The `interfaces/data-boundaries.md` claims four interfaces are the complete governed set. At least five additional paths are depended upon by workflow and integration docs. The project-intake-workflow.md depends on a Project V → VEDA evidence request interface that the signal interface doc explicitly says does not exist here.

**Blocker 4 — Activity trail logging is disconnected from all primary cross-system events.**
Handoff creation, signal transfer, and return-to-planning delivery have no logging requirements in their governing docs. The activity trail cannot be implemented as a coherent governance artifact from these docs.

**Blocker 5 — No workflow can be encoded as a state machine.**
All five workflow docs are missing per-stage entry conditions, exit conditions, and transition triggers. Implementing any of the five workflows requires inventing all transition logic.

**Blocker 6 — Human approval mechanics are universally undefined at the seam level.**
Every governance-sensitive transition defers approval mechanics to `approval-and-escalation-model.md`. That doc defines classes and principles but not which system initiates, what state the workflow enters while pending, or how the result re-enters the process.

---

## 4. Workstream overview

| # | Workstream | Phase | Blocks |
|---|---|---|---|
| WS-A | Correct `cross-system-access-governance.md` | 0 | Everything |
| WS-B | Known-fixes vocabulary patches | 1 | WS-D, WS-E, WS-F |
| WS-C | Create five missing interface docs | 2 | WS-E, WS-F |
| WS-D | Convert four primary interfaces to implementation contracts | 2 | WS-E, WS-F |
| WS-E | Wire activity trail into all interface and governance docs | 3 | WS-F |
| WS-F | Define approval flow mechanics at seam level | 3 | WS-G |
| WS-G | Add operational structure to workflow docs | 4 | — |
| WS-H | Vocabulary anchors and local cleanup | 5 | — |

---

## 5. Recommended remediation sequence

### Phase 0 — Stop-ship corrections

**WS-A: Rewrite `ecosystem/cross-system-access-governance.md`**

This doc must be corrected before any cross-system implementation work begins. Targeted patches are insufficient given the volume and type of errors.

Required corrections:
- Remove "VEDA → Project V (Not Applicable)" — replace with the correct entry acknowledging VEDA signal delivery to Project V as a primary governed interaction governed by `veda-to-project-v-signal-interface.md`
- Remove "VEDA → V Forge (Not Applicable)" — replace with the correct entry acknowledging VEDA signal delivery to V Forge as a primary governed interaction governed by `veda-to-v-forge-signal-interface.md`
- Correct the "Project V → V Forge (Execution Results)" label — this pair's direction is inverted; the correct behavior (Project V reading V Forge results) is data flowing V Forge → Project V; the governing interface is `v-forge-to-project-v-return-to-planning-interface.md`
- Resolve the internal contradiction between "project-scoped or ecosystem-scoped for market scanning" (Project V → VEDA) and "unscoped queries that return data across all projects are not permitted" — define what distinguishes permissible market-scanning scope from prohibited unscoped cross-project queries
- Add entries for the handoff delivery (Project V → V Forge), return-to-planning delivery (V Forge → Project V), and VEDA signal delivery (VEDA → both Project V and V Forge) as the primary governed interactions they are

This is a rewrite, not a patch. The current doc's framing suppresses the two primary VEDA signal delivery paths and misrepresents the fundamental access model.

---

### Phase 1 — Governance and seam infrastructure

**WS-B: Apply known-fixes vocabulary patches**

These patches are already specified in `audit-known-fixes-plan.md`. Apply them in the order specified there. None require design decisions; they are confirmed bounded fixes.

Priority order:
1. `governance/decision-continuity-doctrine.md` — add cautious-default materiality qualifier (Pass A, Fix 1)
2. `governance/failure-and-recovery-doctrine.md` — remove stale `*(planned)*` marker (Pass A, Fix 2)
3. `governance/evidence-continuity-model.md` — add doctrine-vs-operational-state cross-reference (Pass A, Fix 3)
4. `interfaces/v-forge-to-project-v-return-to-planning-interface.md` — add finding-report boundary constraint note (Pass A, Fix 4)
5. `governance/allowed-agent-actions-matrix.md` + `governance/approval-and-escalation-model.md` — add cross-linking note (Pass B, Fix 5)
6. `governance/daily-report-doctrine.md` — clarify "only durable artifact" condition (Pass B, Fix 7)

Additionally apply these audit-identified patches not in the prior known-fixes plan:
- `veda/system-invariants.md` Invariant 8: correct `append-friendly` to `append-only` for EventLog (Pass 2 Session C finding — `append-only` is the correct term per `schema-reference.md` and `observatory-models.md`)
- `project-v/controlled-vocabularies.md` Work Item Type: correct `handoff-preparation` hyphen to `handoff_preparation` underscore (Pass 2 Session B finding — all other multi-word values use underscores; this is a schema field value, not prose)

---

### Phase 2 — Missing and incomplete interface contracts

**WS-C: Create the five missing interface documents**

These docs must exist before the workflows and integration docs that depend on them can be considered complete. At minimum, each stub must define: interaction direction, governing systems, minimum semantic elements, and the boundary rules. Full field-level specification can follow in WS-D's pattern, but the docs must exist to close the `interfaces/data-boundaries.md` contradiction.

Missing interface docs to create:

1. **`interfaces/project-v-to-veda-evidence-request-interface.md`**
   — Project V requesting additional bounded evidence from VEDA
   — Depended on by: `workflows/project-intake-workflow.md` Stage 5 (request additional bounded evidence), `veda-to-project-v-signal-interface.md` (explicitly defers this path)
   — Design question to resolve: is this a pull-query model (Project V queries VEDA directly) or a signal-request model (Project V notifies VEDA to produce a signal package)? This question must be resolved before the doc can specify mechanics.

2. **`interfaces/v-forge-to-veda-scope-expansion-request-interface.md`**
   — V Forge requesting VEDA to expand its observatory scope
   — Depended on by: `v-forge/vs-veda.md` ("the correct path is to direct VEDA to expand its observatory scope through the governed operator surface")
   — Note: `vs-veda.md` references an "operator surface" path; confirm whether this is V Forge → VEDA directly or V Forge → operator → VEDA and design accordingly

3. **`interfaces/project-v-to-v-forge-execution-clarification-interface.md`**
   — Project V providing scope clarification or additional approval to V Forge mid-execution (without triggering full return-to-planning)
   — Depended on by: `project-v/v-forge-integration.md` ("that coordination must still occur through the governed interface path")

4. **`interfaces/project-v-handoff-recall-interface.md`**
   — Operator-directed recall of a handoff that has been transferred but on which V Forge has not yet acted
   — Depended on by: `project-v/v-forge-integration.md` Handoff Recall and Reconsideration Rule
   — Note: this must define a different path from return-to-planning; the two must be clearly distinguished

5. **`interfaces/project-v-to-v-forge-scope-update-interface.md`**
   — Project V notifying V Forge of scope or constraint changes after replanning
   — Depended on by: `workflows/maintenance-and-replanning-workflow.md` Stage 6 ("V Forge is informed of any scope or constraint changes through the governed interface")

**WS-D: Convert the four primary interface docs from semantic contracts to implementation contracts**

Follow the pattern established by `v-forge-evidence-access-contract.md`, which is the only primary interface doc that approaches implementation completeness.

For each of the four docs, add:
- Named fields for the payload or package with types and constraints
- Freshness and timestamp requirements (gathered_at, validity_window, trust_classification where applicable)
- Activity trail section: which action type applies, which system produces the record, which required fields apply
- Degraded-mode section: what the caller does when the responder is unavailable, stale, or returns an error
- Recovery path: what happens after degraded mode ends
- Cost accounting acknowledgment: whether this interface incurs token or API cost

Docs to convert (in dependency order):

1. **`interfaces/veda-to-project-v-signal-interface.md`** — scored 0 of 21 PASS in Pass 3; 18 FAILs; most critical gap set in the corpus
2. **`interfaces/project-v-to-v-forge-handoff-interface.md`** — scored 0 of 21 PASS; the handoff payload structure is the most operationally load-bearing gap
3. **`interfaces/v-forge-to-project-v-return-to-planning-interface.md`** — currently has a finding-report boundary constraint note (WS-B Fix 4) but still needs full implementation structure
4. **`interfaces/veda-to-v-forge-signal-interface.md`** — must also resolve the architectural question raised in Pass 5 Session B: the signal interface describes a passive bounded channel; the evidence access contract describes an active query model; one must be declared authoritative and the other must defer to it, or the two models must be explicitly reconciled as complementary

Additionally for the veda-to-v-forge-signal-interface.md conversion: resolve whether the access model is MCP-tool-call-mediated (as the signal interface states) or direct API query (as the evidence access contract implies). This design question must be resolved before the implementation contract can be correct.

---

### Phase 3 — Activity trail and approval integration

**WS-E: Wire activity trail action coverage into every interface doc**

The activity-trail-model.md defines a dot-namespaced action vocabulary. None of the primary interface docs reference it. The evidence access contract is the only exception.

Work required:
- For each interface doc (all four primary + the five new ones from WS-C), add an explicit "Activity Trail" section specifying: which `action` type applies (from the existing vocabulary where possible), which `action_class` applies (`cross_system_access`, `state_change`, `approval`, etc.), which system sets `actor_system`, which field maps to `entity_type` and `entity_id`, and whether `token_cost` or `api_cost_cents` apply
- Reconcile the evidence access contract's 8-field logging schema with the activity trail's required field set. The contract's `actor` field bundles what the trail separates into `actor_type`, `actor_id`, and `actor_system`. The contract's `action` field uses `veda_evidence_query` (underscore) rather than `evidence.query` (dot-namespaced). Align the contract to the canonical trail format or explicitly document why it diverges
- Add the following activity trail action types that are currently missing: a cross-system action type for return-to-planning delivery (V Forge → Project V); a lifecycle transition type for Project V project state changes relevant to cross-system events (Handed Off, Return Under Reconsideration). These may require extending the activity-trail-model.md action vocabulary

Create one new document as part of this workstream:
**`ecosystem/activity-trail-integration-map.md`** — a reference table mapping every cross-system interaction type to its action type, producing system, required fields, and any cross-doc notes. This is the artifact recommended in the master summary as the "activity trail integration map."

**WS-F: Define human approval flow mechanics at seam level**

Every governance-sensitive transition currently defers approval mechanics to `governance/approval-and-escalation-model.md`. The governance model defines classes but not the seam-level mechanics.

Work required, per governance-sensitive transition:

For **handoff activation** (Project V → V Forge):
- Which system generates the approval request
- What information the request must contain (reference the approval-and-escalation-model.md Approval Request Principle)
- What state Project V enters while pending (Awaiting-Approval-or-Activation is named in operational-workflow.md; this must be wired to the handoff interface)
- How the approval result re-enters the handoff workflow (triggers Stage 4 → Stage 5 in handoff-workflow.md)
- Which doc owns this specification (the handoff interface, the handoff workflow, or a new approval mechanics supplement)

For **return-to-planning receipt** (V Forge → Project V):
- Which system generates the review request when human review is required
- What triggers the review requirement (the return interface's Human-In-The-Loop Principle lists triggering conditions but not mechanics)
- How the review result re-enters Project V replanning

For **launch authorization** (cross-system, Stage 5 of launch-readiness-workflow.md):
- The most complex case: requires cross-system confirmation before the authorization stage even begins
- Stage 4 requires Project V, V Forge, and VEDA to all confirm readiness; the mechanics of that confirmation are undefined
- Who generates the Stage 5 approval request; what the authorization record looks like; what triggers Stage 6

For **replanning with prior decision supersedence** (Project V internal, but cross-system consequential):
- When replanning supersedes or invalidates a prior governing decision that justified a handoff, the mechanics of human review before proceeding must be defined

The output of this workstream should be either: additions to each relevant interface doc, or a single `governance/approval-mechanics-seam-model.md` that defines the mechanics for each transition type and is referenced from the interface docs. The latter is cleaner if the same approval mechanics pattern repeats across transitions.

Note: this workstream depends on the design question about push vs pull transport for handoff delivery (WS-D). The approval flow mechanics assume an answer to that question.

---

### Phase 4 — Workflow codability repairs

**WS-G: Add operational structure to the five workflow docs**

All five workflow docs are currently not codable. The universal gaps are: no per-stage entry conditions, no per-stage exit conditions, no named transition triggers, undefined human approval point mechanics, unrouted escalation paths, non-observable state changes.

The remediation work for each workflow doc is the same class of work; the docs vary in how much partial structure already exists to build on.

Priority order (most operationally critical first):

1. **`workflows/handoff-workflow.md`** — governs the most consequential cross-system boundary crossing; the three-state model (prepared / awaiting / active) is a valid starting skeleton; needs entry/exit conditions per stage, forward transition triggers, human approval mechanics at Stage 3 (blocked on WS-F), and escalation routing
2. **`workflows/project-intake-workflow.md`** — least structurally mature; needs the most work; also blocked until the Project V → VEDA evidence request interface exists (WS-C item 1)
3. **`workflows/maintenance-and-replanning-workflow.md`** — has the strongest trigger list (six workflow triggers, four non-triggers); add per-stage entry/exit conditions and transition triggers for Stages 1–6; the Stage 5 escalation overflow condition is already specific and can be used as a template for other stages
4. **`workflows/launch-readiness-workflow.md`** — has seven explicit blocking conditions and a stale-stage re-assessment rule; add per-stage entry/exit conditions, transition triggers, and the Stage 4 cross-system confirmation mechanics (blocked on WS-F)
5. **`workflows/post-launch-observation-workflow.md`** — most structurally advanced; define "governed intervals" concretely (duration, cadence, trigger authority), define "materially significant signal event" with a threshold or classification rule, and define the Stage 6 escalation path mechanics

For each workflow doc, the minimal remediation output is:
- A stage table with: stage name, entry condition (testable), exit condition (testable), responsible actor, outputs produced
- A transition table with: from-stage, trigger event or condition, to-stage, guard condition if any, failure disposition
- An escalation routing section: what condition triggers escalation, who receives it, what state the workflow enters, what closes escalation
- A reference to the approval mechanics defined in WS-F for stages that require human approval

---

### Phase 5 — Vocabulary and consistency cleanup

**WS-H: Vocabulary anchors and remaining consistency cleanup**

These items do not block implementation of the primary seams but should be completed before the repo is declared clean.

Items from known-fixes-plan.md not yet addressed above:
- `ecosystem/vocabulary.md` — add canonical definition for `governance-sensitive` (referenced across governance docs with inconsistent scope; Pass 2 Session A finding)
- `ecosystem/vocabulary.md` — add canonical definition for `operator` (used throughout governance docs to drive approval behavior; Pass 2 Session A finding)
- `ecosystem/vocabulary.md` — add canonical definition for `material/materiality` (used to determine behavior change thresholds; Pass 2 Session A finding)
- `ecosystem/vocabulary.md` — add canonical definition for `scope excess` (used as escalation trigger; Pass 2 Session A finding)
- `ecosystem/vocabulary.md` — add canonical definition for `task` (appears in action vocabulary and runtime behavior without definition; Pass 2 Session A finding)
- `ecosystem/vocabulary.md` — add canonical term for the bounded scope transferred at handoff (currently expressed as `handoff scope`, `execution scope`, `bounded execution scope`, `handed-off scope`, `admitted scope` across different docs; Pass 2 Session B finding)
- `project-v/schema-specification.md` / `project-v/controlled-vocabularies.md` — define the `actor` field format: is it a user ID, a system identifier string, an enum of actor types? "Free text — guidance only" is not sufficient for schema implementation (Pass 2 Session B finding)

Additional items from Pass 5 not in prior known-fixes-plan.md:
- `v-forge/vs-veda.md` — replace the reference to "ADR-003" for the VEDA Brain prohibition with a reference to a document that actually exists (the ADR-003 doc was not found in the repo; `veda/system-invariants.md` Invariant 6 covers the same constraint without the ADR reference)
- `interfaces/data-boundaries.md` — update the four-interface "complete set" claim to acknowledge the five additional interfaces once they are created (WS-C) and confirm the list is not exhaustive
- Pass 1 stale docs: move or mark as superseded the `interfaces/extension-*` family docs and any other self-declared superseded docs still in active folders

---

## 6. Workstream details

### WS-A — Correct cross-system-access-governance.md

**Purpose:** Remove the most actively misleading doc in the repo.
**Why it matters:** Any developer using this doc to understand VEDA's interaction model will conclude VEDA → Project V and VEDA → V Forge are "Not Applicable." The primary signal delivery paths are the opposite of "Not Applicable." Implementation teams reading this doc would design the wrong access architecture.
**Artifacts:** Rewrite of `ecosystem/cross-system-access-governance.md`
**Dependencies:** None — must happen first.
**Completion criteria:** The doc correctly describes all six system-pair interactions, the four named governing interfaces are correctly attributed, no direction-label errors remain, and the market-scanning vs unscoped-query contradiction is resolved with a definition or scope rule.

---

### WS-B — Known-fixes vocabulary patches

**Purpose:** Apply the bounded fixes already specified in `audit-known-fixes-plan.md` plus two new confirmed patches.
**Why it matters:** The `append-friendly` / `append-only` inconsistency for VEDA EventLog will produce the wrong mutation model if left unpatched. The `handoff-preparation` hyphen produces a schema field value inconsistency at implementation time.
**Artifacts:** Targeted edits to seven docs (listed in Phase 1 above)
**Dependencies:** None — can proceed immediately, but should not precede or conflict with WS-A.
**Completion criteria:** All items in `audit-known-fixes-plan.md` are marked complete. VEDA EventLog is `append-only` consistently across system-invariants.md. `handoff-preparation` uses underscore consistently with all other controlled vocabulary values.

---

### WS-C — Create five missing interface docs

**Purpose:** Close the contradiction between `interfaces/data-boundaries.md`'s claim of a complete four-interface set and the five additional paths depended on by other docs.
**Why it matters:** The project-intake-workflow.md cannot be made codable until the Project V → VEDA evidence request interface exists. The v-forge-integration.md integration rules are unenforceable without the scope clarification and handoff recall interfaces. The maintenance-and-replanning-workflow.md Stage 6 is unimplementable without the scope update interface.
**Artifacts:** Five new interface docs (listed in Phase 2 above)
**Dependencies:** WS-A (access governance corrected so new interfaces are consistent with the model). Item 1 (evidence request) requires resolving the push/pull design question for signal delivery. Item 2 (scope expansion request) requires confirming whether the path is direct or operator-mediated.
**Completion criteria:** Each new doc defines interaction direction, governing systems, minimum semantic elements, boundary rules, and at minimum a stub for the activity trail logging section. `interfaces/data-boundaries.md` is updated to reference the nine governed interfaces (not four).

---

### WS-D — Convert four primary interface docs to implementation contracts

**Purpose:** Give developers actual contracts to implement against.
**Why it matters:** Zero of the four primary interface docs have field definitions. Two of them explicitly say "semantic contract comes first" and defer all structure. Implementing these interfaces without field definitions produces incompatible schemas.
**Artifacts:** Substantive additions to four interface docs (field definitions, freshness requirements, activity trail section, degraded-mode section, recovery path, cost accounting)
**Dependencies:** WS-A (correct access model); WS-C (new interfaces exist so cross-references are valid); the push/pull design question must be resolved for the handoff and signal interfaces. For the veda-to-v-forge-signal-interface.md: the dual-access-model question (passive channel vs active query) must be resolved before the implementation contract can be written.
**Completion criteria:** Each converted interface doc can receive a Pass 3 re-audit and score at minimum 12 of 21 PASS (the evidence access contract benchmark). At minimum: named payload fields, freshness metadata, activity trail action type mapping, degraded-mode caller behavior, and recovery path.

---

### WS-E — Wire activity trail into all interface and governance docs

**Purpose:** Make the activity trail implementable as a coherent governance record across all cross-system events.
**Why it matters:** The activity trail is the primary mechanism for making ecosystem governance auditable. Without logging requirements in the interface docs, implementations will produce a trail with systematic gaps at the most governance-significant events (handoff, signal delivery, return-to-planning).
**Artifacts:** Activity trail section added to each interface doc; `ecosystem/activity-trail-integration-map.md` created; action vocabulary extended in `ecosystem/activity-trail-model.md` to cover return-to-planning delivery and Project V lifecycle transitions; evidence access contract's logging schema aligned to the activity trail's required field format.
**Dependencies:** WS-D (interface docs must be converted before logging sections can be correct); WS-C (new interface docs must exist to be included in the integration map).
**Completion criteria:** Every governed cross-system action has a named activity trail action type. Every interface doc has an explicit activity trail section. The integration map covers all nine interfaces. The evidence access contract's logging schema is either aligned to the canonical format or the divergence is explicitly documented with a governing reason.

---

### WS-F — Define human approval flow mechanics at seam level

**Purpose:** Make human approval operational rather than a reference to a principles doc.
**Why it matters:** Every governance-sensitive transition currently has undefined mechanics. Without mechanics, approval flows cannot be implemented — and implementations will diverge, some requiring approval and some not for the same class of action.
**Artifacts:** Either additions to each relevant interface doc, or a new `governance/approval-mechanics-seam-model.md` that is referenced from each interface doc. The latter is preferred if the mechanics pattern is consistent across transitions.
**Dependencies:** WS-D (interface docs converted); WS-F requires knowing the transport model for handoff delivery (push vs pull) because the approval request mechanics differ. The approval model doc's class definitions must not be changed — this workstream adds mechanics, not new classes.
**Completion criteria:** For each governance-sensitive transition (handoff activation, return-to-planning receipt, launch authorization, replanning with supersedence), a developer can determine: which system initiates the approval request, what the request contains, what state the workflow enters while pending, what the human must do, and how the result re-enters the workflow.

---

### WS-G — Add operational structure to workflow docs

**Purpose:** Make the five workflow docs codable as state machines.
**Why it matters:** A workflow that cannot be encoded is a narrative, not a specification. All five workflow docs are currently narratives. They describe the ecosystem correctly but cannot drive implementation.
**Artifacts:** For each of the five workflow docs: a stage entry/exit condition table, a transition trigger table, an escalation routing section, observable state change requirements. This work may produce supplement docs or in-doc revisions depending on the scale of additions.
**Dependencies:** WS-C (missing interfaces needed for some workflow transitions); WS-F (approval mechanics needed for human-approval stages). WS-G should begin with the workflows that have the fewest dependencies on unresolved design questions.
**Completion criteria:** Each workflow doc can receive a Pass 4 re-audit and score at minimum "Partially codable, follow-up needed" rather than "Not codable without major clarification." The three most operationally critical workflows (handoff, project-intake, maintenance-and-replanning) should reach the partial-codable threshold before Phase 4 is considered complete.

---

### WS-H — Vocabulary anchors and remaining consistency cleanup

**Purpose:** Close the undefined load-bearing term gaps and clean up residual inconsistencies.
**Why it matters:** Undefined terms like `operator`, `governance-sensitive`, and `material` drive approval behavior throughout the governance spine. Leaving them undefined means different implementers will use different thresholds.
**Artifacts:** Additions to `ecosystem/vocabulary.md`; a canonical definition for the `actor` field format; cleanup of stale `*(planned)*` markers and superseded doc statuses.
**Dependencies:** WS-B (existing vocabulary patches applied); WS-F (approval mechanics defined, which clarifies what "governance-sensitive" must include); WS-D (interface contracts written, which may inform how `operator` is defined in context).
**Completion criteria:** All five undefined terms from Pass 2 Session A have canonical definitions in `ecosystem/vocabulary.md`. The `actor` field has a defined format in `project-v/controlled-vocabularies.md`. No known `*(planned)*` markers reference docs that exist and are complete. Superseded docs in active folders are either moved to `archive/` or explicitly marked.

---

## 7. Parallelization guidance

**Can happen in parallel:**
- WS-A (access governance rewrite) and WS-B (known-fixes patches) — they touch different docs
- WS-H (vocabulary cleanup) can begin as soon as WS-A and WS-B are complete; it does not depend on WS-C, WS-D, or WS-E
- WS-C items 3, 4, and 5 (scope clarification, handoff recall, scope update interfaces) can be drafted in parallel with each other; they do not depend on the push/pull design question
- WS-G for the maintenance-and-replanning-workflow.md and post-launch-observation-workflow.md can begin as soon as WS-F is complete; these workflows have fewer missing interface dependencies than project-intake-workflow.md

**Must happen in sequence:**
- WS-A before anything else — the access governance doc is so wrong that later work built against it will compound the error
- WS-C before WS-G for the project-intake-workflow.md — the evidence request interface must exist before the intake workflow can be made codable
- WS-D before WS-E — activity trail sections must be added to complete interface docs, not stubs
- WS-F before WS-G for any workflow stages with human approval points
- The push/pull design question must be resolved before WS-D and WS-F can be completed for the handoff and signal interfaces

**Design questions that must be resolved before dependent workstreams can complete:**

These are not documentation decisions — they are architectural decisions that affect what the docs should say:

1. **Push vs pull for handoff and signal delivery** — Is the handoff a Project V-initiated push or a V Forge-initiated pull? Is VEDA signal delivery a VEDA push or a Project V pull? This affects transport mechanics in WS-D and approval flow mechanics in WS-F.

2. **Dual access model resolution for VEDA → V Forge** — The signal interface describes a passive bounded channel; the evidence access contract describes an active query model. These must be reconciled as either complementary layers (signal interface = bulk package delivery; evidence access contract = on-demand query) or one must supersede the other.

3. **Project V → VEDA evidence request model** — Is this a direct query, a signal-request notification, or an operator-mediated path? This must be resolved before WS-C item 1 can be specified beyond a stub.

4. **Centralized vs distributed approval mechanics** — Is the approval mechanics specification added to each relevant interface doc, or is a single `governance/approval-mechanics-seam-model.md` created and referenced? The latter is cleaner but adds a dependency.

---

## 8. Deferred / later items

These items were identified in the audit but should intentionally wait until the blocker and infrastructure workstreams above are complete.

**Defer until after Phase 3:**
- Provider registry consistency review (open in `audit-open-questions-and-followups.md`) — depends on the VEDA access model being settled in WS-D
- V Forge ADR gap (open in `audit-open-questions-and-followups.md`) — deferred to V Forge-specific audit phase
- `ecosystem-docs-execution-plan.md` disposition (open in `audit-open-questions-and-followups.md`) — revisit after Phase 4 is complete

**Defer until after Phase 4 (workflow codability):**
- Full workflow re-audit (Pass 4 re-run) — run after WS-G is complete to verify the workflow docs reach codable threshold
- Desktop interface doc refresh — the desktop docs had meaningful but incomplete implementation coverage; they need a targeted completeness pass after the core ecosystem seam work lands

**Defer until after Phase 5:**
- Root README refinement for accumulated audit artifacts
- Decision to move or archive the `audit/` folder content once remediation is complete

**Items that require human judgment before they can be resolved (not deferred — active decisions needed):**
- The four design questions in section 7 (push/pull, dual access model, evidence request model, centralized vs distributed approval mechanics)
- Whether the `nerve/` and `ux/` folders should be given formal sanctioned categories or remain as informal support layers
- The `opportunity-scoring-model.md` *(planned)* reference in workflows — if the doc will be created, create it; if not, remove the reference

---

## 9. Exit criteria for "safe to implement from"

The repo is safe to implement from when all of the following are true:

**Infrastructure:**
- [ ] `cross-system-access-governance.md` correctly describes all six system-pair interactions with correct direction labels and governing interface references
- [ ] `interfaces/data-boundaries.md` references all nine governed interfaces (four existing + five new)
- [ ] All five missing interface docs exist with at minimum stub-level specification

**Interface contracts:**
- [ ] The four primary interface docs each have: named payload fields, freshness metadata requirements, activity trail logging section, degraded-mode caller behavior, and recovery path
- [ ] The dual access model for VEDA → V Forge is resolved and documented

**Activity trail:**
- [ ] Every cross-system action type has a corresponding dot-namespaced action type in the activity trail vocabulary
- [ ] Every interface doc has an explicit activity trail section referencing the correct action type and producing system
- [ ] The activity trail integration map exists

**Approval mechanics:**
- [ ] For each of the four governance-sensitive transitions (handoff activation, return-to-planning receipt, launch authorization, replanning with supersedence), the producing system, request format, pending state, human action, and re-entry mechanics are defined

**Workflow codability:**
- [ ] All five workflow docs have per-stage entry and exit conditions defined as testable guards
- [ ] All five workflow docs have named transition triggers (not narrative)
- [ ] The three highest-priority workflows (handoff, project-intake, maintenance-and-replanning) pass a Pass 4 re-audit at "Partially codable or better"

**Vocabulary:**
- [ ] `operator`, `governance-sensitive`, `material/materiality`, `scope excess`, and `task` have canonical definitions in `ecosystem/vocabulary.md`
- [ ] The `actor` field format is specified as a governed type, not "free text"
- [ ] `handoff-preparation` uses underscore consistently with all controlled vocabulary values
- [ ] VEDA EventLog is `append-only` consistently across all VEDA system docs

---

## 10. Next deliverables to produce

Listed in order of dependency:

1. **`cross-system-access-governance.md` rewrite** (WS-A) — first artifact to produce; no dependencies

2. **Known-fixes patch set** (WS-B) — bounded edits to seven docs; no blocking dependencies; can produce as a single batch PR

3. **Four design decision records** — for push/pull model, dual access model reconciliation, evidence request model, and approval mechanics location. These are architectural decisions, not doc fixes. They may be ADRs or annotated decision notes. They must be resolved before WS-C and WS-D can be completed.

4. **Five missing interface stubs** (WS-C) — one doc per missing path; at minimum defines direction, governing systems, minimum semantics, and placeholder activity trail section

5. **Interface implementation contract additions** (WS-D) — field definitions, freshness, activity trail, degraded mode, recovery, cost for each of the four primary interface docs; the veda-to-v-forge reconciliation must happen in this batch

6. **`ecosystem/activity-trail-integration-map.md`** (WS-E) — new reference doc mapping all nine cross-system interaction types to action types, producing systems, and required fields

7. **Activity trail additions to all interface docs** (WS-E) — additions to each of the nine interface docs (four existing + five new) adding the explicit logging section

8. **Approval mechanics specification** (WS-F) — either additions to each relevant interface doc or a new `governance/approval-mechanics-seam-model.md`

9. **Workflow codability supplements** (WS-G) — for each of the five workflow docs: stage entry/exit table, transition trigger table, escalation routing section. These may be additions within the existing docs or companion supplement docs.

10. **Vocabulary additions to `ecosystem/vocabulary.md`** (WS-H) — five new canonical term definitions plus the canonical handoff scope term

11. **`project-v/controlled-vocabularies.md` actor field specification** (WS-H) — add a governed type definition for the `actor` field

12. **Pass 4 re-audit** (validation) — run against the workflow docs after WS-G is complete to confirm codability threshold is reached

---

## 11. Closing summary

The remediation work is substantial but it is not a rebuild. The architecture is correct. The ownership model is correct. The governance principles are sound. The work is converting an architectural specification into an implementation specification — adding the data contracts, transition mechanics, logging integrations, and approval flows that the current docs defer.

The most urgent single action is correcting `cross-system-access-governance.md`, because it is the one doc in the set that will actively mislead implementation teams about how the primary VEDA signal delivery paths work. Everything else in this plan makes the docs more complete. That doc makes them less correct.

After Phase 0, the sequencing is designed so that each phase produces artifacts that later phases depend on. Do not start Phase 3 without Phase 2 complete. Do not start Phase 4 without Phase 3 complete. The design questions in section 7 are gates, not advisory items — phases that depend on those decisions cannot produce correct artifacts until the decisions are made.

The vocabulary and consistency work (Phase 5) can proceed mostly in parallel once Phases 1 and 2 are underway. It is not blocked on the design questions and does not need to wait for the interface contracts to be complete.

When all nine exit criteria clusters in section 9 are satisfied, the docs will support disciplined implementation. Until then, any implementation proceeding against the current docs should treat the interface data contracts, transition triggers, activity trail logging requirements, and approval mechanics as "to be determined by the implementation team" — and should plan to reconcile those local decisions against the remediated docs when they land.
