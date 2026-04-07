# Pass 2 — Interfaces and Workflows

## Purpose

This pass evaluates whether the governed seams, interfaces, and workflows form a
coherent operational model with no major missing lifecycle path, stale overlap,
approval-gate contradiction, or seam ambiguity. It assesses whether the interface
and workflow layer is strong enough to support schema authority derivation and
implementation-facing work.

This is not a governance doctrine review. Governance findings from Pass 1 are
treated as baseline unless current file text directly contradicts them.

---

## Scope of This Pass

This pass covers:

- whether each major lifecycle path is represented end-to-end
- whether approval-sensitive seams align with workflow stages and canonical
  pending-state vocabulary
- whether activity-trail mappings match actual interface and workflow events
- whether similar paths are properly separated rather than blurred
- whether the stub interfaces are sufficient bounded posture or are now
  implementation blockers
- whether `data-boundaries.md` still contains stale interface posture text
  that creates a false picture of the governed interface set

---

## Files Reviewed

**Interface docs:**
- `interfaces/data-boundaries.md`
- `interfaces/veda-to-project-v-signal-interface.md`
- `interfaces/project-v-to-v-forge-handoff-interface.md`
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `interfaces/veda-to-v-forge-signal-interface.md`
- `interfaces/project-v-to-veda-evidence-request-interface.md`
- `interfaces/v-forge-evidence-access-contract.md`
- `interfaces/project-v-to-v-forge-execution-clarification-interface.md`
- `interfaces/project-v-handoff-recall-interface.md`
- `interfaces/project-v-to-v-forge-scope-update-interface.md`
- `interfaces/operator-to-veda-observatory-scope-expansion-interface.md`

**Workflow docs:**
- `workflows/project-intake-workflow.md`
- `workflows/handoff-workflow.md`
- `workflows/maintenance-and-replanning-workflow.md`
- `workflows/launch-readiness-workflow.md`
- `workflows/post-launch-observation-workflow.md`

**Cross-check docs:**
- `governance/approval-mechanics-seam-model.md`
- `ecosystem/activity-trail-model.md`
- `ecosystem/activity-trail-integration-map.md`

---

## Executive Verdict

The interface and workflow layer is **substantially complete and operationally
coherent**. The five primary lifecycle paths (intake, handoff, return-to-planning /
replanning, launch readiness, post-launch observation) are all represented end-to-end
with concrete stages, named transitions, and approval-gate integration. The eleven
interface docs collectively cover all primary and secondary cross-system seams. The
activity trail integration map is aligned with the current interface and workflow set.

The layer is **implementation-ready for the four primary interfaces and the full
workflow set**. The three stub interfaces are sufficient bounded posture for current
purposes but are not yet full implementation contracts, and two of the three carry
an outdated activity trail forward-reference note that creates false ambiguity.

Two documentation hygiene items remain from the previous pass that were not corrected:
the stale "gated — pending artifact creation" language in `data-boundaries.md`, and
two forward-reference notes in stub interface docs claiming the activity trail action
types for their seams are not yet canonical (they are).

One genuine implementation-readiness gap exists: the `v-forge-evidence-access-contract.md`
uses a partially distinct activity-trail logging convention that is not fully reconciled
with the integration map's canonical action type and field vocabulary.

---

## Complete

The following are classified as **Complete** — coherent, strong enough to build
against, and consistent with the governing doctrine and activity trail canon.

---

### C1. VEDA → Project V Signal Interface

**Finding: Complete.**

`veda-to-project-v-signal-interface.md` is a full Tier 1 document covering the
access model (VEDA-initiated push, receipt confirmation required), both delivery
triggers (proactive and request-response), the minimum semantic package contents,
degraded-mode behavior, and activity trail requirements. The distinction table
between proactive and request-response delivery is clear and directly supports
the integration map's `signal.delivery` / `signal.delivery.confirmed` action types
with the `delivery_trigger_type` discriminator.

Cross-check: the interface references `approval-mechanics-seam-model.md` for
approval-sensitive events that follow from signal delivery without redefining
approval mechanics here. This is the correct posture.

---

### C2. Project V → V Forge Handoff Interface

**Finding: Complete.**

`project-v-to-v-forge-handoff-interface.md` is a full Tier 1 document with the
three-phase model (activation approval / delivery / receipt confirmation) stated
clearly and non-negotiably. The approval-sensitive event section correctly names
`awaiting_approval` as the pending state, references `approval-mechanics-seam-model.md`
Section A without redefining it, and is consistent with the handoff workflow's
Stage 2–5 sequence.

The distinction section from adjacent interfaces (return-to-planning, recall,
clarification, scope update) is explicit and accurate. All four adjacent paths are
correctly cross-referenced without overlap.

Activity trail coverage: references integration map Sections 2 and 5a. The
`handoff.create` / `handoff.confirmed` / `handoff.failed` / `handoff.reject` action
types are all canonical in the model. Consistent.

---

### C3. V Forge → Project V Return-to-Planning Interface

**Finding: Complete.**

`v-forge-to-project-v-return-to-planning-interface.md` is a full Tier 1 document.
The three-phase model (delivery / receipt confirmation / planning review) mirrors
the handoff interface's structure appropriately in the reverse direction. The
finding-report boundary rule ("V Forge returns bounded execution findings — not
planning instructions") is explicit and in agreement with the maintenance and
replanning workflow's core rule.

The approval-sensitive event section correctly names `awaiting_review` as the
pending state, notes that Project V governs the review request (not V Forge), and
references `approval-mechanics-seam-model.md` Section B. This is consistent with
the workflow.

Activity trail coverage: references integration map Sections 3 and 5b. The
`execution.return` / `execution.return.confirmed` / `execution.return.failed` /
`execution.return.voided` action types are canonical. Consistent.

---

### C4. VEDA → V Forge Signal Interface (Startup Layer)

**Finding: Complete.**

`veda-to-v-forge-signal-interface.md` is a full Tier 1 document. The explicit
distinction table between this startup layer and the active evidence-query layer
(`v-forge-evidence-access-contract.md`) is the right design choice: it prevents
the two complementary layers on the same seam from being conflated.

The lifecycle moment for this delivery (tied to a confirmed handoff, at execution
scope initialization, fires once per scope) is defined precisely enough to be
implementable. The constraint "if the execution scope is re-initiated after a
recall or replanning cycle, a new startup signal delivery applies for the new
scope" is correctly stated and prevents stale startup contexts.

Activity trail coverage: references integration map Section 4 (`signal.delivery.startup`
action type). Consistent.

---

### C5. Project V → VEDA Evidence Request Interface

**Finding: Complete.**

`project-v-to-veda-evidence-request-interface.md` is a full Tier 1 document. The
AD-03 bounded request-for-package model is cleanly implemented: Project V states a
bounded planning question, VEDA curates the response, the response returns through
the existing VEDA → Project V push delivery path. No new return channel is created.

The interface correctly prohibits using this path to request specific VEDA record
identifiers (which would be direct observatory access) and requires that the request
be tied to a recognized planning workflow stage.

**One stale forward-reference note to flag (documentation hygiene):**
The Activity Trail section says a new `evidence.request` action type and
`evidence_request` entity type "must be added to that model before this interface
is implemented" and "until that extension is made, implementations must not
proceed." Integration map Section 8 explicitly confirms these extensions have
already been applied to the model. The forward-reference is stale. This note
should be removed or corrected in a documentation hygiene pass.

Workflow alignment: the re-entry routing (re-enter Stage 2 or Stage 3 of the
intake workflow depending on how much framing context remains established) is
consistent with the intake workflow's Stage 6 definition.

Activity trail coverage: integration map Section 7 maps `evidence.request` action
type with required fields including `delivery_trigger_type: request_response` on
the response leg. Consistent.

---

### C6. Operator → VEDA Observatory Scope Expansion Interface

**Finding: Complete.**

Confirmed complete in Pass 1. The interface doc exists, is a full Tier 1 document,
and is fully mapped in integration map Section 11. Not reopened here.

**Same stale forward-reference note present** (same as C5 above): the interface
doc's Activity Trail section says its action types are not yet in the canonical
model. Integration map Section 8 confirms they have been applied. This note is
stale and should be corrected in the same documentation hygiene pass.

---

### C7. Project Intake Workflow

**Finding: Complete.**

`project-intake-workflow.md` is a full Tier 1 workflow document with eight distinct
named stages, concrete transitions, and a complete transition table. It correctly
handles both trigger types (VEDA-delivered signal and operator/strategy trigger),
distinguishes the Stage 6 bounded evidence request path from a forced weak outcome,
and preserves the defer/hold/reject decision continuity requirements.

The approval gate section (Stage 5, Class B or C for project creation with material
planning impact) correctly names `awaiting_review` as the pending state and
references `approval-mechanics-seam-model.md` Section E. This is consistent with
the seam model's Transition Class E definition.

Activity trail coverage: inline activity trail table references the correct canonical
action types (`project.create`, `intake.defer`, `intake.hold`, `intake.reject`,
`intake.close`, `approval.request`, `approval.decide`, `approval.escalate`) per
integration map Section 9. Consistent.

---

### C8. Handoff Workflow

**Finding: Complete.**

`handoff-workflow.md` is a full Tier 1 workflow document with eight distinct named
stages, concrete transitions, and a complete transition table. The three-phase
requirement (approval / delivery / receipt confirmation) is stated as the core rule
and is enforced through the stage model — there is no path from Stage 2 to Stage 5
that bypasses Stage 4 (delivery).

The approval gate section correctly names `awaiting_approval` as the pending state
and references `approval-mechanics-seam-model.md` Section A. The stage 8 basis
change / approval expiry assessment aligns directly with the seam model's stale
approval prohibition.

The adjacent interface routing section (handoff recall, VEDA startup signal delivery,
clarification, scope update, return-to-planning) correctly names each path's specific
entry condition and distinguishes them from each other and from the handoff workflow
itself.

Activity trail coverage: inline table references integration map Sections 2 and 5a.
Action types are canonical. Consistent.

---

### C9. Maintenance and Replanning Workflow

**Finding: Complete.**

`maintenance-and-replanning-workflow.md` is a full Tier 1 workflow document with
eight distinct named stages, a detailed transition table, and a downstream routing
section that explicitly defines five outcome paths (no planning change, scope update,
execution clarification, new handoff, deferral/cancellation) and the specific
conditions for each.

The maintenance vs. replanning distinction is explicit and important: maintenance
operates within approved scope and does not trigger this workflow; replanning does.
The "if a maintenance action changes a governing decision it is replanning, not
maintenance" guard is good.

The review gate at Stage 3 correctly names `awaiting_review` as the pending state.
The additional approval gate at Stage 5 for supersedence of prior governing decisions
references `approval-mechanics-seam-model.md` Section D, correctly treating
supersedence as a second nested approval gate within replanning.

Activity trail coverage: inline table references integration map Sections 3 and 5b.
Action types are canonical. Consistent.

---

### C10. Launch Readiness Workflow

**Finding: Complete.**

`launch-readiness-workflow.md` is a full Tier 1 workflow document with eleven
distinct named stages and a complete transition table. The key design choice —
separating Stage 4 (cross-system convergence, a precondition) from Stage 5
(authorization request) — is correct and well-explained. The workflow correctly
states that Stage 4 convergence is a precondition for the authorization request,
not the authorization itself.

The authorization gate at Stage 5 correctly names `awaiting_authorization` as the
pending state (the third and distinct canonical pending term, used only here), sets
the approval class as C, and references `approval-mechanics-seam-model.md` Section C.

One deliberate gap is correctly acknowledged: the current activity trail model does
not include explicit readiness-stage completion action types for Stages 1–4. The
workflow correctly directs implementations to use general `state_change` action types
with `details` context rather than inventing new action types. This is the right
call and is not a finding.

Activity trail coverage: inline table references integration map Section 5c.
`launch_authorization` entity type is canonical. Consistent.

---

### C11. Post-Launch Observation Workflow

**Finding: Complete.**

`post-launch-observation-workflow.md` is a full Tier 1 workflow document with eight
distinct named stages and a complete transition table. The three-phase distinction
(observation / classification / action routing) is stated as the core rule and is
maintained throughout the stage model.

The signal maturity rule (acting on pre-maturity signal produces governance noise;
the Stage 4 classification outcome for immature signal must be "continue observation"
not a forced assessment) is a strong design choice. The noise vs. material signal
rule (volume alone does not make signal material) is correctly stated.

The four outcome paths (continue-observation, maintenance, return-to-planning,
escalation) map cleanly onto the Stage 5 assessment criteria and are correctly
distinguished from each other.

Activity trail coverage: inline table references integration map Section 10.
The `observation.classify`, `observation.assess`, and `observation.cycle` canonical
action types are correctly used. Consistent.

---

## Partial

The following have meaningful work but carry a gap that will matter before
implementation or schema authority work on those specific seams is finalized.

---

### P1. V Forge Evidence Access Contract — Activity Trail Convention Partially
Divergent from Integration Map

**Classification: Partial.**

`v-forge-evidence-access-contract.md` is a full Tier 1 document and the
evidence-query layer is correctly designed. However, its Activity Logging section
uses a different convention from the canonical integration map:

The contract defines a bespoke log structure with fields named `actor`, `action`,
`query_type`, `parameters`, `result_count`, `token_cost`, and `timestamp`. The
`action` value is described as `veda_evidence_query`. The integration map does not
map `veda_evidence_access` or `veda_evidence_query` as canonical action types.
Looking at the activity trail model, the closest canonical action type for V Forge
querying VEDA evidence during execution is `evidence.query`.

The contract does not reference the integration map or the activity trail model's
canonical field vocabulary. Specifically:
- the base required fields from the activity trail model (`activity_id`,
  `actor_type`, `actor_id`, `actor_system`, `action`, `action_class`,
  `entity_type`, `entity_id`, `target_system`, `project_id`) are not referenced
- `veda_evidence_query` is not the canonical action type for this event class
- the contract's field names do not align with the activity trail model's field names

**Impact:** An implementation following the contract's Activity Logging section
verbatim would produce non-canonical activity records that cannot be replayed or
audited through the standard activity trail tooling. The integration map does
include V Forge active evidence queries (Section implied by the presence of
`evidence.query` in the model's action vocabulary), but the contract itself is not
aligned to it.

**Suggestion:** Update the Activity Logging section of `v-forge-evidence-access-contract.md`
to reference the integration map and use the canonical action type (`evidence.query`)
and canonical base fields from the activity trail model. The query-specific detail
fields (`query_type`, `parameters`, `result_count`) can be carried in the `details`
field of the canonical record. This is a focused update to one section of the doc;
the rest of the contract is sound.

---

### P2. Three Stub Interfaces — Bounded Posture, Not Full Contracts

**Classification: Partial.**

The three stub interfaces (`project-v-to-v-forge-execution-clarification-interface.md`,
`project-v-handoff-recall-interface.md`, `project-v-to-v-forge-scope-update-interface.md`)
are explicitly bounded posture documents rather than full implementation contracts.
Each defines the semantic meaning, core rule, minimum semantic elements, and boundary
posture for its seam. None defines field-level schemas, transport mechanics, or a
full approved activity trail action type mapping.

The stubs are **sufficient as governing boundary documents** — they prevent scope blur,
define which seam each path covers and under what conditions, and correctly cross-
reference the adjacent interfaces they are distinct from. They are not implementation
blockers for schema authority work on the primary systems.

However, two of the three carry an outdated Activity Trail note (same issue as C5
and C6 above) that says:

> "The exact canonical action type mapping and required fields will be defined in
> the activity trail integration map once that document is completed."
> "This stub does not finalize the activity trail action vocabulary for this interface.
> Implementations must not proceed without that mapping in place."

The integration map is complete. Integration map Section 6 (for clarification and
scope update) and Section 6b (for handoff recall) are fully mapped with canonical
action types, producing systems, and minimum required fields. These stubs' notes
are stale and create false ambiguity about whether the action types have been defined
(they have).

**Scope of the gap:** The stubs are not full implementation contracts — that is by
design and acceptable. The stale Activity Trail notes are a documentation hygiene
issue that should be corrected so that implementers reading the stub docs know
where to find the current canon rather than being told it does not yet exist.

**Suggestion:** Update the Activity Trail section of each of the three stub docs
to reference the specific integration map section that governs their action type
mapping, and remove or correct the "once that document is completed" language.
This is three small targeted edits, not a full contract upgrade.

**Regarding stub upgrade timing:** Whether these stubs need upgrading to full
contracts before schema authority work on the adjacent primary systems (handoff,
return-to-planning) can proceed is assessed in the Implementation-Readiness
Implications section below.

---

## Missing

**No missing interfaces or workflows identified on the current merged baseline.**

All primary lifecycle paths are represented end-to-end. All secondary governed paths
have at minimum a stub-level governing document. The observatory scope expansion
interface, previously flagged as missing, is confirmed complete.

---

## Blocked

**No blocked work identified.**

The evidence access contract activity trail gap (P1) is a documentation alignment
issue, not an architectural blocker. The stub interfaces (P2) are sufficient for
current purposes. No interface or workflow has a dependency that prevents progress.

---

## Key Gap Analysis

### Gap 1: Evidence access contract activity trail is not canonically aligned

This is the most concrete implementation-facing gap in the pass. The
`v-forge-evidence-access-contract.md` Activity Logging section describes a bespoke
log structure that does not map to the canonical activity trail model field vocabulary
or action type naming. An implementation following that section as written would
produce non-canonical records. The fix is targeted and does not require redesigning
the contract — it is a section-level update to align with `evidence.query` and the
base field vocabulary.

### Gap 2: Three stale Activity Trail forward-reference notes across four docs

Four docs (`project-v-to-veda-evidence-request-interface.md`,
`operator-to-veda-observatory-scope-expansion-interface.md`, and the two relevant
stubs) contain notes saying their activity trail action types have not yet been
added to the canonical model or that the integration map is not yet complete.
Integration map Section 8 confirms all these extensions are applied. These notes
are false and should be corrected in a single documentation hygiene sweep.

### Gap 3: `data-boundaries.md` interface registry is stale

`data-boundaries.md` still classifies the operator-to-VEDA observatory scope
expansion interface as "gated — pending artifact creation." It is a full merged
Tier 1 document. The Interface-Enforcement Principle section in `data-boundaries.md`
is the repo's central interface registry and should accurately reflect the current
governed interface set. It should be updated to move the operator-to-VEDA interface
into the appropriate category (fully defined), add a note about the three stubs'
mapping status, and remove the stale pending language.

---

## Suggestions and Feedback

**On lifecycle coverage:** The five-workflow model is complete and coherent. Every
major transition in the ecosystem — intake, handoff, replanning, launch, post-launch
observation — has a governing workflow. The workflows chain correctly: intake leads
to handoff (via project creation); handoff leads to replanning (via return-to-planning)
or launch readiness; launch leads to post-launch observation; post-launch observation
cycles back into maintenance/replanning or new intake. No lifecycle cul-de-sacs found.

**On seam separation:** The distinction work is strong. The three-way distinction
between execution clarification (bounded ambiguity resolution within existing scope),
scope update (post-replanning constraint update), and new handoff (fundamentally
new scope) is explicit and enforced in the handoff workflow's adjacent interface
routing section and in the maintenance and replanning workflow's downstream routing
section. This will matter at implementation time and is well-prepared.

**On the two VEDA → V Forge layers:** The startup push layer (`veda-to-v-forge-signal-interface.md`)
and the active query layer (`v-forge-evidence-access-contract.md`) are correctly
designed as complementary rather than competing. The distinction table in the
startup layer doc is the right anchor. The one area of concern is the query
contract's activity trail misalignment (P1 above), which should be fixed before
implementation rather than after.

**On pending-state vocabulary alignment:** All five approval-sensitive seam
transitions use the canonical pending-state terms (`awaiting_approval`,
`awaiting_review`, `awaiting_authorization`, `escalated_for_review`) as defined in
`approval-mechanics-seam-model.md`. No workflow or interface was found inventing
synonyms or using these terms in incorrect seam contexts. This is clean.

**On the launch readiness workflow's Stage 4 → Stage 5 design:** Requiring all
three system readiness inputs to be current simultaneously before the authorization
request may be generated is the correct design. The risk it prevents (system A's
readiness confirmation going stale while awaiting system B) is real and the
explicit stale-readiness-input rules in Stage 9 address re-entry correctly.

**Weak spot to watch:**

The maintenance and replanning workflow's downstream routing section defines a
"Scope Update" path and a "New Handoff" path and gives guidance on when to choose
between them, but the boundary condition is stated somewhat softly ("if the
replanning outcome requires fundamentally different execution scope or target"). In
practice, the distinction between a large scope update and a fundamentally different
scope requiring a new handoff may be ambiguous for complex replanning events. This
is not a gap in the current docs but is worth noting as a point of interpretation
that may surface during implementation. A future doc that gives a sharper test would
be valuable.

---

## Recommended Next Actions

### Immediate (documentation hygiene — directly identified in this pass):

1. **Correct the stale Activity Trail forward-reference notes** in four docs:
   - `interfaces/project-v-to-veda-evidence-request-interface.md` — remove
     the "must be added to the model before implementation" language; the
     `evidence.request` action type and `evidence_request` entity type are canonical.
   - `interfaces/operator-to-veda-observatory-scope-expansion-interface.md` — remove
     the "not yet in the canonical model" note; the `observatory.scope_change.*` family
     is canonical per integration map Section 8.
   - `interfaces/project-v-to-v-forge-execution-clarification-interface.md` — update
     to reference integration map Section 6a specifically.
   - `interfaces/project-v-handoff-recall-interface.md` and
     `interfaces/project-v-to-v-forge-scope-update-interface.md` — update to
     reference integration map Sections 6b and 6c respectively.

2. **Update `interfaces/data-boundaries.md` interface registry** — move the
   operator-to-VEDA observatory scope expansion interface from "gated — pending
   artifact creation" to the appropriate fully-defined category, and update the
   stub entries to reflect their integration map section references.

3. **Update the Activity Logging section of `interfaces/v-forge-evidence-access-contract.md`**
   to align with the canonical activity trail model: use `evidence.query` as the
   action type, use the model's base required fields, and carry query-specific
   detail fields (`query_type`, `parameters`, `result_count`) in the `details`
   field. Reference integration map to confirm the mapping.

### Before stub interface upgrades begin (schema authority phase):

4. **Do not upgrade the three stub interfaces to full contracts until the schema
   authority phase has defined the relevant entity schemas** for the seams they
   govern (scope update, execution clarification, handoff recall). Upgrading the
   stubs early without the entity schema context will require revision immediately
   after. The current stub posture is sufficient for schema planning.

---

## Schema-Readiness / Implementation-Readiness Implications

**The four primary interfaces are implementation-ready** as governing contracts
(handoff, return-to-planning, VEDA → Project V signal, VEDA → V Forge startup
signal). They define minimum semantic contents, approval posture, degraded-mode
behavior, and activity trail requirements at sufficient precision to begin
implementation design.

**The five workflow documents are implementation-ready** at the governance level.
Each has concrete stages, named transitions, approval gate integration, and
activity trail requirements with canonical action type mappings. None requires
additional governance work before implementation planning.

**The evidence access contract is implementation-ready in all respects except**
the activity trail section (P1). That section must be corrected before the
evidence query implementation is built, or the resulting activity records will
be non-canonical from day one.

**The three stub interfaces are not yet full implementation contracts** and should
not be treated as such. They provide sufficient boundary posture for schema planning
(the schema can reference the seam by name and define the entity type) but the
stub-to-full-contract upgrade needs to happen as part of the implementation phase
for those seams.

**The `data-boundaries.md` stale text does not create an implementation blocker**
but does create a false picture of the governed interface set that will mislead
implementers reading the boundary documentation. It should be corrected before
implementation work begins on any of the affected seams.

**Overall implementation-readiness classification: Substantially ready, with three
documentation hygiene actions and one targeted contract section update required
before implementation work begins. No architectural changes needed. No missing
interfaces or workflows.**

---

## Related Docs Referenced in This Pass

- `interfaces/data-boundaries.md`
- `interfaces/veda-to-project-v-signal-interface.md`
- `interfaces/project-v-to-v-forge-handoff-interface.md`
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `interfaces/veda-to-v-forge-signal-interface.md`
- `interfaces/project-v-to-veda-evidence-request-interface.md`
- `interfaces/v-forge-evidence-access-contract.md`
- `interfaces/project-v-to-v-forge-execution-clarification-interface.md`
- `interfaces/project-v-handoff-recall-interface.md`
- `interfaces/project-v-to-v-forge-scope-update-interface.md`
- `interfaces/operator-to-veda-observatory-scope-expansion-interface.md`
- `workflows/project-intake-workflow.md`
- `workflows/handoff-workflow.md`
- `workflows/maintenance-and-replanning-workflow.md`
- `workflows/launch-readiness-workflow.md`
- `workflows/post-launch-observation-workflow.md`
- `governance/approval-mechanics-seam-model.md`
- `ecosystem/activity-trail-model.md`
- `ecosystem/activity-trail-integration-map.md`
