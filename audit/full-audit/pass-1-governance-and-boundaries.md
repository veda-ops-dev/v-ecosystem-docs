# Pass 1 — Governance and Boundary Integrity

## Purpose

This pass evaluates whether the governance and authority layer of the V Ecosystem
repository is internally coherent, strong enough to support schema authority work,
and free of meaningful contradictions, drift risks, or structural gaps.

This is not a summary pass. It answers the questions defined in `master-plan.md`
Pass 1 directly.

---

## Scope of This Pass

This pass covers:

- ownership and truth-domain integrity
- cross-system boundary and data boundary posture
- approval governance (Tier 1 meaning and Tier 2 mechanics)
- continuity, supersedence, and invalidation support
- agent and operator authority posture
- schema-readiness implications of the governance layer

---

## Files Reviewed

**Audit control docs:**
- `audit/full-audit/README.md`
- `audit/full-audit/master-plan.md`

**Core governance / boundary docs:**
- `ecosystem/cross-system-boundaries.md`
- `ecosystem/cross-system-access-governance.md`
- `interfaces/data-boundaries.md`
- `governance/approval-and-escalation-model.md`
- `governance/approval-mechanics-seam-model.md`
- `governance/external-action-governance.md`
- `governance/decision-continuity-doctrine.md`
- `governance/invalidation-and-supersedence-doctrine.md`
- `governance/allowed-agent-actions-matrix.md`

**Supporting docs (read for coherence confirmation):**
- `ecosystem/activity-trail-model.md`
- `ecosystem/activity-trail-integration-map.md`
- `governance/auth-and-actor-model.md`
- `governance/agent-operating-doctrine.md`

**Verified directly for this correction pass:**
- `interfaces/operator-to-veda-observatory-scope-expansion-interface.md`

---

## Executive Verdict

The governance and boundary layer of the V Ecosystem is **strong and internally
coherent in its core structure**. The ownership model is settled, clearly
documented, and not self-contradicting. The approval model has genuine depth —
both a Tier 1 doctrine doc and a Tier 2 mechanics doc. The continuity and
invalidation layer is explicitly built out. The agent authority posture is
well-defined.

The repo is **governance-stable enough to begin schema authority planning** for
the three primary systems.

There are three material partial areas and one stale-text issue. None are blockers
for schema planning. The stale-text issue in `data-boundaries.md` should be
corrected in the next cleanup pass but does not represent an open governance gap.

---

## Complete

The following domains are classified as **Complete** — coherent, solid, and
sufficient to build against without requiring further governance-layer work first.

---

### C1. System Ownership / Truth-Domain Integrity

**Finding: Complete.**

The three-system truth-domain model is clearly and consistently stated across
`cross-system-boundaries.md`, `cross-system-access-governance.md`, and
`data-boundaries.md`. All three docs are in agreement:

- Project V = planning truth
- VEDA = signal / evidence / observability truth
- V Forge = execution truth

The "access is not ownership" principle is explicitly stated in both
`cross-system-boundaries.md` (Rule 1) and `cross-system-access-governance.md`
("Own narrowly. Access broadly. Govern the access."). Anti-blur rules are
specific and illustrated with concrete allowed / not-allowed examples. The
VEDA Brain prohibition, the content-graph-in-VEDA prohibition, and the
planning-records-in-V-Forge prohibition are all explicit.

No ownership contradictions found across these three docs.

**Schema-time callout (not a governance gap):** The "bounded execution-side
research" carve-out under V Forge in `cross-system-boundaries.md` is
well-constrained in the doc text ("research performed in support of approved
execution, handoff, maintenance, or return-to-planning needs — not open-ended
ecosystem-wide signal gathering"). This boundary will need a schema-level
expression when V Forge's execution intelligence records are formalized, but
it is not an ambiguity in the governance layer.

---

### C2. Cross-System Access Governance

**Finding: Complete.**

`cross-system-access-governance.md` enumerates all six system-pair interaction
patterns, each with direction, access type, governing interface reference, and
boundary statement. The anti-drift rules (frequency ≠ ownership, caching ≠
second source of truth, portfolio scope ≠ unscoped access, delivery ≠ merge) are
implementation-forward guard rails that support schema authority work.

The `V Forge → VEDA` direction is correctly classified as "not an interaction"
and the operator-mediated path for observatory scope expansion is correctly defined
as the governed route. That path is now fully documented — see C3 below.

---

### C3. Operator-to-VEDA Observatory Scope Expansion Interface

**Finding: Complete.**

`interfaces/operator-to-veda-observatory-scope-expansion-interface.md` exists,
is a full Tier 1 interface document, and is fully mapped in
`ecosystem/activity-trail-integration-map.md` Section 11.

The complete `observatory.scope_change.*` action type family (seven types) and
the `observatory_scope_change` entity type are canonical in
`ecosystem/activity-trail-model.md`. Integration map Section 8 explicitly confirms
that all extensions including this family have been applied to the model.

**One stale-text issue to note (not a governance gap):** Two docs carry outdated
language about this interface:

- `interfaces/data-boundaries.md` — the "Additional governed interfaces
  (gated — pending artifact creation)" section still lists "Operator → VEDA
  observatory scope expansion" as missing and says "that interface has not yet
  been created." This text is stale. The interface exists and is merged. This
  section of `data-boundaries.md` needs updating to move the operator-to-VEDA
  interface into the fully-defined or stub set.

- `interfaces/operator-to-veda-observatory-scope-expansion-interface.md` itself —
  the Activity Trail section contains a forward-reference note saying the
  `observatory.scope_change.*` action types "are not yet in the canonical model
  and must be added before implementation." Integration map Section 8 confirms
  these extensions have already been applied. This note inside the interface doc
  is now stale and should be removed or corrected in a cleanup pass.

Neither stale-text instance creates a governance gap. Both should be cleaned up
in the next documentation maintenance sweep.

---

### C4. Approval Model (Tier 1 — Meaning and Posture)

**Finding: Complete.**

`approval-and-escalation-model.md` is one of the strongest docs in the repo.
It covers:

- approval class taxonomy (A through D) with clear criteria
- approval state vocabulary (pending, approved, rejected, expired, revoked,
  escalated)
- stale approval and changed-context rules
- the rejection-as-governed-outcome principle
- informal direction vs. governed approval distinction
- delegation ≠ approval
- continuity artifacts ≠ approval

The "Approval and Boundary Relationship" section makes clear that an approved
action still has to use correct system roles and interface paths — approval
authorizes action within doctrine, it does not authorize doctrine collapse.
This is directly usable for schema permission design.

**Schema-time callout (not a governance gap):** The Reviewability Principle
states the ecosystem should be able to determine what was approved, who approved
it, what scope applied, and whether the approval is still active. This is a sound
semantic contract, but the persisted approval record entity is not yet schema-
specified. That is a schema authority artifact to define during the schema phase,
not a missing governance doc.

---

### C5. Approval Mechanics (Tier 2 — Seam Model)

**Finding: Complete.**

`approval-mechanics-seam-model.md` defines:

- the shared request / pending / decision / re-entry mechanics pattern
- the five approval-sensitive transition classes with seam-specific facts
- canonical pending-state vocabulary (`awaiting_approval`, `awaiting_review`,
  `awaiting_authorization`, `escalated_for_review`)
- activity trail integration via the three `approval.*` action types
- interface and workflow usage rules

The dual-use of `awaiting_review` for both Return-to-Planning (Class B) and
Governed Intake Outcome Review (Class E) is deliberately designed and
internally coherent — the doc distinguishes them by context and entity reference.

The anti-drift rules section makes this doc schema-implementation ready.

---

### C6. Decision Continuity Doctrine

**Finding: Complete.**

`decision-continuity-doctrine.md` provides exactly the schema-authority reference
needed for determining what requires a durable record:

- what makes a decision continuity-binding
- decision vs. runtime continuity distinction (memory artifacts are not governing
  records)
- approved-but-unrecorded state acknowledgment
- the stale approval / changed context rule with a materiality standard
- the replanning continuity rule
- the rejection continuity rule

The "Decision vs Signal vs Findings vs Runtime Continuity" section is an explicit
anti-drift disambiguation that directly supports schema persistence design.

---

### C7. Invalidation and Supersedence Doctrine

**Finding: Complete.**

`invalidation-and-supersedence-doctrine.md` covers:

- invalidation vs. supersedence distinction (basis-is-gone vs. active-replacement)
- validity conditions for both (explicit, justified, authority-matched,
  approval-posture-matched)
- partial invalidation constraints and scope integrity rule for supersedence
- record preservation (both invalidated and superseded records remain as history)
- the governance gap created by invalidation without replacement
- agent escalation rule (identify the need; do not self-execute)

Cross-check: the authority rule (V Forge must not unilaterally invalidate governing
planning decisions; actor authority mirrors the original decision's authority) is
consistent with `auth-and-actor-model.md`'s Decision Authority Rule. No
contradiction.

---

### C8. Agent Authority Posture

**Finding: Complete.**

The combination of `allowed-agent-actions-matrix.md`, `agent-operating-doctrine.md`,
and `auth-and-actor-model.md` forms a coherent and consistent agent authority layer.

Specific strengths:

- the matrix is organized by action class and system context, directly usable for
  schema permission design
- the "Forbidden regardless of instruction" list is explicit and actionable
- the "Access is not authority / Capability is not authority / Visibility is not
  authority" triad is consistent across all three docs
- the prompt-claiming-role prohibition in `auth-and-actor-model.md` is explicit:
  "A claimed role is not a verified role"
- the pre-compaction flush principle defines a legitimate continuity-support action
  while preventing it from being used to launder authority into memory artifacts
- the cross-system agent actions section (cross-system state mutation = Forbidden
  without explicit interface path) is consistent with the boundary docs

---

### C9. External Action Governance

**Finding: Complete.**

`external-action-governance.md` covers the four external action classes (E1–E4),
preconditions for external action, the execution halt rule, and the uncertainty
withholding rule. The "Internal Preparation Is Not External Authorization" and
"Recommendation Is Not Permission to Execute" principles are clear and non-
negotiable in tone. The doc correctly references `paid-data-pull-governance.md`
for E4 refinement without over-specifying it here.

---

### C10. Activity Trail Model (as Governance Infrastructure)

**Finding: Complete (for governance purposes).**

The activity trail model is a full governance artifact with dot-namespaced
extensible action vocabulary, cost fields, retention posture, and replay
requirements. The three approval action types are integrated into the seam
model. The entity type vocabulary is explicit and current, including the
`observatory_scope_change` entity type added for the scope expansion interface.

The integration map (Section 8) explicitly confirms all action type and entity
type extensions identified across the full governed interface set have been
applied to the model. This is a reliable canon status check.

---

## Partial

The following domains have substantial, usable work, but have identifiable gaps
that will matter before schema authority work on those specific domains is finalized.

---

### P1. Approval Record Schema Undefined

**Classification: Partial.**

The approval governance docs (Tier 1 and Tier 2) define what approval means,
what approval requests must semantically contain, what the decision outcomes are,
what the pending-state vocabulary is, and what activity trail records must be
produced.

What they do not define is the **schema of a persisted approval record entity** —
the durable, queryable record that answers "what approvals are currently active
for this project?" or "what was the approval state when this handoff was activated?"

The activity trail records `approval.decide` as an event. That is a log entry.
An approval record entity represents the current and historical state of a
governed authorization — a different schema concern. The `approval-and-escalation-model.md`
Reviewability Principle names the semantic contract clearly (what was approved,
who approved it, scope, conditions, current status) but does not translate it into
a schema entity spec.

**Impact:** For schema authority work, the approval record entity schema needs to
be explicitly designed. It cannot be fully derived from current docs. This affects
Project V schema (which owns approval records for planning-side transitions) and
the cross-system schema spine.

**Suggestion:** Define an `approval_record` schema entity contract as part of the
schema authority phase for Project V. The semantic contents are already defined in
`approval-and-escalation-model.md`. They need a schema-level translation.

---

### P2. Actor Identity — No Concrete Value-Space Specification

**Classification: Partial.**

`auth-and-actor-model.md` correctly establishes the doctrine that actor identity
must be classifiable, actions must be attributable, and access ≠ authority. But
the doc explicitly defers implementation: "This does not require implementation-
specific identity systems in this document."

The activity trail requires `actor_type`, `actor_id`, and `actor_system` on every
record. These fields are defined by name but their **value sets** are not specified
beyond the three broad actor type labels (agent, operator, system). The doc's
"Minimum Actor Semantics" section defines six semantic properties that governed
actions should preserve, but there is no artifact that translates these into a
schema-level identity contract — what shape is `actor_id` for an agent vs. an
operator, what does `actor_system` contain for a cross-system session, how does
operator session identity get established and referenced in audit records.

**Impact:** Manageable now — governance doctrine is clear enough to proceed with
schema planning — but will surface as a concrete blocker when the activity trail
schema is being finalized and when approval records need to reference a human
approver identity.

**Suggestion:** During the schema authority phase, define an actor identity spec
as a companion to `auth-and-actor-model.md`. Specify the value space for
`actor_type`, `actor_id`, and `actor_system` with enough precision to support
the activity trail schema and the approval record schema.

---

### P3. Portfolio-Scoped Access Authorization — Mechanics Soft

**Classification: Partial.**

`cross-system-access-governance.md` permits portfolio-scoped access for Project V
planning market evaluation but the conditions under which portfolio scope is
"explicitly authorized" remain informal. The doc states portfolio-scoped access
must be "explicitly authorized by the requesting context" but does not specify what
that authorization looks like in schema terms — is it an operator-set session
configuration, a governed planning context record, an inline field in the evidence
request?

The evidence request interface (`project-v-to-veda-evidence-request-interface.md`)
is a stub-level ungated interface. Until that interface is fully specified, the
mechanics of how portfolio scope authorization is established and logged are
undefined at the schema level.

**Impact:** Not a blocker for core schema authority work on the three primary
systems. It becomes relevant when the VEDA → Project V signal interface and the
evidence request stub interface move from stub to full contract.

**Suggestion:** When upgrading the stub interfaces to full contracts, add an
explicit `scope_type` field (project | portfolio) and a `portfolio_authorization_ref`
field to the evidence request schema, tied to whatever operator authorization model
is established in the actor identity spec.

---

## Missing

**None identified on the current merged baseline.**

The operator-to-VEDA observatory scope expansion interface is fully documented and
its activity trail canon is complete. The prior assessment that this was missing was
based on stale language in `data-boundaries.md` and a forward-reference note inside
the interface doc that had not been cleaned up after the canon was merged. Those are
stale-text issues, not missing artifacts.

---

## Blocked

**No blocked work identified.**

The one seam that was previously flagged as blocked (observatory scope change
implementation) is unblocked: the interface doc exists, the action type family is
canonical, and the integration map is complete.

The stub interfaces (`project-v-to-v-forge-execution-clarification-interface.md`,
`project-v-handoff-recall-interface.md`, `project-v-to-v-forge-scope-update-interface.md`,
`project-v-to-veda-evidence-request-interface.md`) are explicitly listed as ungated
stubs in `data-boundaries.md`. Whether any of these needs upgrading before schema
planning proceeds is a Pass 2 (Interfaces and Workflows) question, not a governance-
layer question.

---

## Key Gap Analysis

### Gap 1: Approval persistence is governed in doctrine but not schema-specified

The approval governance is genuinely strong at the doctrine level. The Tier 1 and
Tier 2 docs together cover semantics well. But there is a gap between "what approval
events must be logged in the activity trail" (covered) and "what shape is a persisted
approval record that can be queried as an entity" (not covered). The schema authority
phase must close this.

### Gap 2: Actor identity value space is deferred

The auth and actor model correctly establishes the doctrine. The concrete value
space for activity trail actor fields is not specified. This will surface at schema
finalization time if not addressed first. It can be handled during the schema phase
alongside the approval record entity design.

### Gap 3: Two docs carry stale language about the observatory scope expansion interface

`interfaces/data-boundaries.md` still describes the operator-to-VEDA interface
as "gated — pending artifact creation." The interface doc itself still says its
action types "are not yet in the canonical model." Both statements are factually
incorrect on the current merged baseline. These are documentation hygiene issues,
not governance gaps, but they create a misleading picture for anyone reading the
boundary docs and should be corrected in the next cleanup pass.

---

## Suggestions and Feedback

**On overall quality:** This is a well-built governance layer. The docs are
internally consistent, cross-references are accurate, anti-drift rules are specific
and enforceable, and the LLM Use Principle sections are a useful calibration tool.
The level of specificity in the approval mechanics seam model and the decision
continuity doctrine is notably higher than most comparable governance layers reach.

**On the Tier 1 / Tier 2 approval split:** This is the right call. Separating
doctrine (what approval means and why) from mechanics (how seam-level approval
works step by step) keeps both docs coherent and prevents either from being
bloated. It also prevents the common drift where mechanics docs gradually
redefine doctrine.

**On the VEDA Brain prohibition:** The telescope mental model and the "VEDA Brain
does not exist in this ecosystem" statement in `cross-system-boundaries.md` is
worth preserving verbatim in schema documentation. It is the clearest anti-drift
guard for VEDA's role boundary and should be referenced explicitly in the VEDA
schema authority doc when that work begins.

**On the allowed agent actions matrix:** The matrix is schema-ready in structure.
It can be referenced directly when designing permission scopes for agent-facing
APIs. The "Forbidden regardless of instruction" section should not be weakened
during schema or implementation work on grounds of operational efficiency.

**Weak spots to watch:**

1. The approved-but-unrecorded state in `decision-continuity-doctrine.md` is
   acknowledged but the system-level detection or audit path for that state is not
   specified. The doc says agents must not defer record creation — but there is no
   process defined for detecting when this has happened. This will matter when the
   schema needs to support governance replay across decision-to-action sequences.

2. `agent-operating-doctrine.md` lists "bounded orchestration support" as an
   allowed behavior category but this does not appear as a distinct action class
   in `allowed-agent-actions-matrix.md`. The matrix's "Bounded Execute" class
   covers some of this, but coordinator-to-specialist routing and worker result
   aggregation are not explicitly classified. This is likely intentional (orchestration
   is implementation-facing) but represents a mild coherence gap between the two docs.

---

## Recommended Next Actions

### Immediate (documentation hygiene — before or alongside schema planning):

1. **Update `interfaces/data-boundaries.md`** — move the operator-to-VEDA
   observatory scope expansion interface out of the "gated — pending artifact
   creation" section. It is a full, merged interface doc. The stale language
   creates a false picture of the governed interface set.

2. **Update the Activity Trail section of `interfaces/operator-to-veda-observatory-scope-expansion-interface.md`** —
   remove or correct the forward-reference note stating the `observatory.scope_change.*`
   action types are not yet in the canonical model. They are canonical. Integration
   map Section 8 confirms this.

### During schema authority phase:

3. **Define an `approval_record` schema entity contract** alongside Project V's
   schema authority work. The semantic contents are in `approval-and-escalation-model.md`.
   They need a schema-level translation into a queryable entity spec.

4. **Define an actor identity schema spec** as a companion to `auth-and-actor-model.md`.
   Specify the value space for `actor_type`, `actor_id`, and `actor_system` at minimum.
   This is needed before the activity trail schema and the approval record entity
   schema can be finalized.

5. **Resolve portfolio-scope authorization mechanics** when upgrading the evidence
   request stub interface to a full contract. Add an explicit `scope_type` and
   `portfolio_authorization_ref` field to the evidence request schema rather than
   leaving authorization as an informal session-level concept.

### Ongoing governance hygiene:

6. **Keep the LLM Use Principle sections consistent** as new docs are added. They
   are one of the better calibration tools in the repo and should be required in
   new governance docs.

7. **Do not weaken the VEDA Brain prohibition and the "Forbidden regardless of
   instruction" agent action list** during implementation work. These are structural
   drift-protection rules, not aspirational guidance.

---

## Schema-Readiness Verdict

**The governance and boundary layer is schema-ready for the core three-system
ownership model, the approval event schema, and the activity trail schema.**

Specifically:

- The three-system ownership boundaries are clear enough to derive schema
  authority domain assignments. Each system has a well-defined canonical data
  ownership map.

- The operator-to-VEDA observatory scope expansion seam is fully governed and
  activity-trail-mapped. It is unblocked for implementation.

- The approval class taxonomy and pending-state vocabulary are defined precisely
  enough to derive the approval event schema and to specify the approval record
  entity schema once that artifact is created in the schema authority phase.

- The agent action matrix is organized in a way that directly supports permission
  scope design for agent-facing APIs.

- The activity trail model and integration map are current and complete at the
  governance and action-vocabulary level. Full schema closure for activity trail
  records depends on the actor identity value-space spec (P2), which is deferred
  to the schema authority phase.

**Not yet schema-ready:**

- The approval record entity schema (schema contract artifact to be created in
  the schema authority phase — P1)
- Actor identity value specification (schema companion artifact to be created in
  the schema authority phase — P2)
- Portfolio-scoped access authorization mechanics (to be resolved when stub
  interfaces are upgraded — P3)

**Overall schema-readiness classification: Partial — strong enough to start
schema authority work, with three known schema-phase artifact dependencies that
must be tracked and resolved before all governance-layer schema concerns are
closed. No governance-layer blockers remain.**

---

## Related Docs Referenced in This Pass

- `ecosystem/cross-system-boundaries.md`
- `ecosystem/cross-system-access-governance.md`
- `interfaces/data-boundaries.md`
- `interfaces/operator-to-veda-observatory-scope-expansion-interface.md`
- `governance/approval-and-escalation-model.md`
- `governance/approval-mechanics-seam-model.md`
- `governance/external-action-governance.md`
- `governance/decision-continuity-doctrine.md`
- `governance/invalidation-and-supersedence-doctrine.md`
- `governance/allowed-agent-actions-matrix.md`
- `ecosystem/activity-trail-model.md`
- `ecosystem/activity-trail-integration-map.md`
- `governance/auth-and-actor-model.md`
- `governance/agent-operating-doctrine.md`
