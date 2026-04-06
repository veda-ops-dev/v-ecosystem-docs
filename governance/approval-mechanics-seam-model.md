# Approval Mechanics Seam Model

## Purpose

This document defines the mechanics of approval-sensitive seam transitions inside
the V Ecosystem.

It exists to answer:

```text
For each governance-sensitive cross-system transition, which system initiates the
approval request, what must the request contain, what state exists while approval
is pending, what are the possible outcomes, how does each outcome re-enter the
workflow, and how must approval events be logged?
```

This is a Tier 2 governance authority document.

This document extends `approval-and-escalation-model.md`, which is the Tier 1 authority
for approval meaning, approval classes, and escalation principles. This document does
not supersede it.

---

## Scope

This document governs:

- the shared mechanics pattern for seam-level approval-sensitive transitions
- the five primary approval-sensitive transition classes in the ecosystem
- the canonical pending-state vocabulary used across interfaces and workflows
- the activity trail logging requirements for seam-level approval events
- the rules for how interface and workflow docs must reference these mechanics

---

## Out of Scope

This document does not define:

- approval class definitions (A through D) — those belong in `approval-and-escalation-model.md`
- escalation triggers and escalation principles — those belong in `approval-and-escalation-model.md`
- approval meaning and approval posture rules — those belong in `approval-and-escalation-model.md`
- implementation payload schemas or API-level mechanics
- transport or delivery mechanics — those are governed by the transport-model decisions
  established in the ISSUE-AD-01 and ISSUE-AD-02 remediation decisions
- interface data contracts or field definitions

Those belong in more specific interface, workflow, implementation, or governance docs.

---

## System

- governance

---

## Relationship to Tier 1 Approval Model

`approval-and-escalation-model.md` defines:

- what approval means
- the approval class taxonomy (A, B, C, D)
- the escalation principle
- what governance-sensitive actions are
- the approval state model (pending, approved, rejected, expired, revoked, escalated)
- the prohibition on informal direction as governed approval
- the prohibition on treating delegation or continuity artifacts as approval

This document extends the Tier 1 approval model downward into mechanics.

Read both documents together. The Tier 1 model defines the what and why of approval.
This document defines the how — the concrete mechanics of carrying out an
approval-sensitive seam transition.

Neither document replaces the other.

---

## Core Rule

Every approval-sensitive seam transition must use explicit, reviewable, mechanically
defined behavior across four phases:

- **Request** — an explicit approval request is generated and delivered
- **Pending** — the workflow enters a named, observable, non-progressing state
- **Decision** — a governed outcome is produced (approved, rejected, escalated, or expired)
- **Re-entry** — the workflow resumes or stops based on the outcome

A transition that skips any of these phases, treats a decision as implicit, or
advances while in a pending state has violated its approval posture.

---

## Shared Mechanics Pattern

This section defines the mechanics pattern shared across all seam-level
approval-sensitive transitions. Each transition class section below applies
this pattern to its specific seam.

---

### 1. Approval Request Initiation

The system attempting the approval-sensitive transition generates the approval
request, unless the specific transition class definition below states otherwise.

The requesting system must:

- generate the request before initiating the transition
- ensure the request is deliverable to a human actor or the governed approval surface
- enter the appropriate pending state immediately after generating the request
- not proceed with the transition until a governed decision is received

Generating an approval request is not the same as receiving approval.
The request is the beginning of the approval lifecycle, not the end of it.

---

### 2. Required Semantic Contents of an Approval Request

A valid approval request must be interpretable as containing at minimum:

- **Action or transition being requested** — what specific transition or activation
  is being proposed
- **System and workflow context** — which system is requesting, which workflow stage
  is involved, what the current state is
- **Scope** — what the approval would cover, bounded to the specific transition
- **Why approval is needed** — which approval class applies and why this action
  requires governed review
- **Relevant risks, uncertainties, or conditions** — what the reviewer should know
  before deciding
- **What happens if approved** — what transition proceeds, what state changes occur
- **What happens if rejected** — what fallback path or stop condition applies
- **What happens if escalated** — what the escalation path is if the approval cannot
  be resolved at this level

A request that buries the real action inside vague language is not a valid
approval request. An approval request must make the scope and consequence of
the decision legible to the reviewer without requiring them to reconstruct
context from elsewhere.

---

### 3. Pending State Rule

While approval is unresolved, the workflow must remain in a named pending posture.

The following are required of the pending state:

- **No silent continuation** — the transition must not proceed while approval is
  pending, even if execution could technically continue
- **No partial activation** — the transition must not partially complete while
  pending; the pre-transition state must be fully preserved
- **Named posture** — the pending state must be one of the canonical pending-state
  vocabulary terms defined in this document
- **Observable and reviewable** — the pending state must be visible in the activity
  trail and interpretable by a later reviewer or session
- **Time-bounded awareness** — if approval remains unresolved for a materially
  significant duration, the pending state must not be silently treated as if
  approval has been granted; stale pending states must be surfaced explicitly

---

### 4. Approval Decision Outcomes

The governed decision outcomes for a seam-level approval event are:

| Outcome | Meaning |
|---|---|
| `approved` | The approval has been granted for the stated scope. The transition may proceed. |
| `rejected` | The approval has been denied. The transition must not proceed. The rejection is a governed outcome, not a null event. |
| `escalated` | The approval cannot be resolved at this level. The workflow enters governed escalation handling. |
| `expired` | The approval was not resolved within the expected window, or the basis for the pending approval has changed materially. The pending approval cannot be silently carried forward. |

No other outcomes are valid. A decision that cannot be classified as one of these
four must be treated as unresolved and the pending state must be preserved.

---

### 5. Re-entry Rule

The outcome of the approval decision re-enters the originating workflow as follows:

**Approved:**
The transition proceeds. The approval event is recorded in the activity trail.
The workflow advances to the post-approval stage defined for this transition.

**Rejected:**
The transition does not proceed. The workflow takes the rejection fallback or stop
path defined for this transition. The rejection is preserved as a governed outcome
with the reason and scope recorded. The rejection must not be treated as if the
request never occurred.

**Escalated:**
The workflow enters the governed escalation handling path. The workflow does not
advance. The escalation is recorded. The originating transition remains pending
until the escalation resolves or the workflow is explicitly stopped.

**Expired:**
The prior pending approval cannot be silently reused. The requesting system must
evaluate whether the approval basis is still valid before generating a new request.
If conditions have materially changed since the request was generated, a new request
must be issued reflecting the current state; the prior request must not be recycled.

---

### 6. Activity Trail Rule

Every seam-level approval event must produce a canonical activity trail record.

The three applicable action types from `../ecosystem/activity-trail-model.md` are:

- `approval.request` — produced when the requesting system generates the approval request
- `approval.decide` — produced when the decision outcome is reached (approved, rejected, or expired)
- `approval.escalate` — produced when the approval is escalated

For each approval event record, the following must be identifiable:

- **Producing system** — the system that produced this activity record
- **Target system or actor** — the system or actor the approval request was directed to
- **Entity / transition reference** — which specific transition or entity this approval covers
- **Approval class** — which class (A, B, C, D) governs this approval event
- **Outcome** — for `approval.decide`, the outcome: `approved`, `rejected`, or `expired`

Approval events that are not logged in the activity trail are not governed approval
events. Ungoverned approval events are not valid.

The activity trail integration map (`../ecosystem/activity-trail-integration-map.md`)
maps these action types to specific seam events. See Section 5 of that document
for the seam-specific minimum fields for each transition class.

---

## Transition Classes

The following five transition classes are the primary approval-sensitive seam
transitions in the ecosystem. Each applies the shared mechanics pattern above
to its specific context.

---

### A. Handoff Activation (Project V → V Forge)

#### What this covers

The activation of a governed handoff from Project V to V Forge, in which execution
responsibility transfers for the approved scope.

Handoff activation is a Class B or Class C approval-sensitive event depending on
the scope, risk level, and launch sensitivity of the handed-off work.

#### Initiating system

**Project V** generates the approval request before activating the handoff.
V Forge does not initiate handoff activation; Project V owns handoff truth.

#### Approval request

The approval request must carry the minimum semantic contents defined in the
Shared Mechanics Pattern, with specific attention to:

- the bounded execution scope being handed off
- the approval posture already satisfied (readiness evaluation, prior governance)
- any constraints, conditions, or evidence references that govern the handoff
- what return-to-planning triggers should apply if execution findings require it

#### Pending state

While handoff activation approval is pending, the workflow must be in:

**`awaiting_approval`**

The handoff package is prepared and the approval request has been generated.
Execution responsibility has not transferred. V Forge must not begin execution.
Project V must not treat the handoff as active.

If the approval basis changes materially while in `awaiting_approval` — including
changed scope, changed evidence, changed approval authority, or materially changed
conditions — the pending state does not automatically carry forward. The approval
must be treated as potentially expired and re-evaluated.

#### Post-approval

On `approved`: Project V activates the handoff through the governed push delivery
path. V Forge confirms receipt. Execution responsibility transfers
at confirmed delivery.

Approval does not equal delivery. Activation approval authorizes the push delivery;
receipt confirmation completes the transfer. Both are required.

On `rejected`: The handoff remains in Project V as a non-activated package.
The workflow returns to the appropriate planning state. The rejection is preserved.

On `escalated`: The workflow enters governed escalation handling. The handoff
package is preserved in its current state. The pending state remains.

On `expired`: The prior approval cannot be silently reused. Project V must assess
whether the handoff basis is still valid and generate a new request if so.

#### Activity trail

- `approval.request` — produced by Project V when the activation approval request is generated
- `approval.decide` — produced when the decision is reached
- `approval.escalate` — produced if escalated

---

### B. Return-to-Planning Receipt / Review (V Forge → Project V)

#### What this covers

The receipt and review of bounded execution findings returned by V Forge to
Project V, when those findings require planning reconsideration.

All return-to-planning transitions that affect planning direction must be reviewed
before planning reconsideration results in new ecosystem actions. This is a Class B
event. Depending on scope and strategic impact, it may reach Class C.

#### Initiating system

**Project V** governs the review of returned findings and generates the human
review request where required.

V Forge initiates the return-to-planning delivery through the governed push
delivery path, but V Forge does not initiate the approval/review request for the
subsequent planning reconsideration. Project V receives the findings and determines whether
human review is required before acting on them.

#### Review request

The review request must carry the minimum semantic contents defined in the
Shared Mechanics Pattern, with specific attention to:

- what execution findings V Forge returned and why
- what prior planning decisions may be affected
- what planning reconsideration is being proposed
- that returned findings do not automatically mutate planning truth

#### Pending state

While planning reconsideration review is pending, the workflow must be in:

**`awaiting_review`**

The returned findings have been received. Planning reconsideration has been
proposed. No planning mutation has occurred. No revised handoff, deferral,
or cancellation has been activated.

Project V must not treat returned findings as self-applying planning changes
while in `awaiting_review`.

#### Post-review

On `approved`: Planning reconsideration proceeds. The specific path depends on
what the reconsideration involves — revised handoff, deferral, cancellation, or
no-action. The re-entry is governed by the maintenance and replanning workflow.

On `rejected`: The proposed planning reconsideration does not proceed. The returned
findings are preserved. Planning remains in its current state. The rejection is
a governed outcome.

On `escalated`: The workflow enters governed escalation handling. Planning remains
in its current state.

#### Activity trail

- `approval.request` — produced by Project V when the human review request is generated
- `approval.decide` — produced when the review outcome is reached
- `approval.escalate` — produced if escalated

---

### C. Launch Authorization (Cross-System Launch-Readiness Path)

#### What this covers

The governed authorization to proceed with launch-sensitive, public-facing, or
spend-creating execution. This is a Class C approval event — the highest
governance class for approval-sensitive execution actions.

#### Precondition: Stage 4 convergence

Launch authorization does not begin at the moment someone believes the project
is ready. Before an authorization request may be generated, the cross-system
readiness convergence established in Stage 4 of the launch-readiness workflow
must be complete:

- planning-side readiness confirmed by Project V
- evidence and signal currency confirmed by VEDA
- execution-side verification confirmed by V Forge
- no unresolved cross-system gap

Stage 4 convergence is a **precondition** for the authorization request, not
the authorization itself. The authorization request is generated after Stage 4
convergence is established.

#### Initiating system

**Project V** generates the launch authorization request, synthesizing the
cross-system readiness picture from Stages 1–4.

V Forge must not self-authorize launch-sensitive action. An agent confirming
readiness is not launch authorization.

#### Authorization request

The authorization request must carry the minimum semantic contents defined in the
Shared Mechanics Pattern, with specific attention to:

- the specific launch-sensitive actions being authorized
- confirmation that Stage 4 convergence was established (with references)
- the approval class and specific governance basis for this launch scope
- the launch scope boundaries — approval covers exactly this scope, not a broader general launch
- the reversibility posture — what can be undone and what cannot

#### Pending state

While launch authorization is pending, the workflow must be in:

**`awaiting_authorization`**

Stage 4 convergence has been established. The authorization request has been
generated and delivered. No launch-sensitive execution has begun. V Forge must
not initiate launch execution while in this state.

If time passes or conditions change materially during `awaiting_authorization`,
Stage 1 and Stage 2 assessments may need to be refreshed before authorization
proceeds, as defined in the launch-readiness workflow.

#### Post-authorization

On `approved`: The launch activation proceeds. V Forge executes within the
authorized scope. The authorization record preserves what scope was covered.

On `rejected`: Launch does not proceed. The workflow returns to planning for
reconsideration. The rejection is preserved with the reason.

On `escalated`: Launch does not proceed. The workflow enters governed escalation handling.

On `expired`: Launch-readiness assessments may have become stale. The requesting
system must re-evaluate Stage 1 and Stage 2 before generating a new request.

#### Activity trail

- `approval.request` — produced by Project V when the authorization request is generated
- `approval.decide` — produced when the authorization outcome is reached
- `approval.escalate` — produced if escalated

---

### D. Replanning with Prior Decision Supersedence (Project V, Cross-System Consequential)

#### What this covers

Replanning that would supersede or materially invalidate a prior governing decision
that was previously approved and active. This is a Class B event at minimum; it
may reach Class C depending on the scope of the superseding decision, its
cross-system consequences, and whether it affects active handoffs.

#### Why this requires governed mechanics

The decision-continuity doctrine requires that prior governing decisions remain
active unless explicitly superseded or invalidated. Replanning that silently
proceeds past a prior governing decision without explicit approval for the
supersedence violates decision continuity.

The stale-approval prohibition in the Tier 1 approval model is specifically relevant
here: a prior approval that supported the superseded decision cannot be automatically
carried forward as if it also approves the superseding decision.

#### Initiating system

**Project V** generates the supersedence approval request. The decision to supersede
belongs to the planning system of record.

#### Supersedence approval request

The approval request must carry the minimum semantic contents defined in the
Shared Mechanics Pattern, with specific attention to:

- which prior governing decision is being superseded or materially invalidated
- what the basis for the prior decision was and why it is no longer sufficient
- what the new governing direction is
- the scope of what changes and what does not
- any cross-system consequences: whether the supersedence affects an active handoff,
  a return-to-planning event in progress, or other governed transitions
- that stale prior approval cannot be silently reused

#### Pending state

While supersedence approval is pending, the workflow must be in:

**`awaiting_approval`**

The prior governing decision remains active. Replanning has been proposed and the
approval request has been generated. Execution under the prior governing decision
may continue or must pause depending on the scope of the proposed supersedence
and the risk of continuing under the prior basis.

The requesting system must assess whether execution under the prior basis is safe
while approval is pending and must surface that assessment explicitly.

#### Post-approval

On `approved`: The supersedence proceeds. The prior decision is explicitly marked
as superseded with a reference to the new governing decision. The replanning
workflow continues. Any cross-system consequences (revised handoffs, scope updates,
etc.) are executed through their governed interfaces.

On `rejected`: The proposed supersedence does not proceed. The prior governing
decision remains active. Replanning may need to take a different path that does
not require supersedence.

On `escalated`: The workflow enters governed escalation handling. The prior
governing decision remains active. Replanning is paused.

#### Activity trail

- `approval.request` — produced by Project V when the supersedence approval request is generated
- `approval.decide` — produced when the decision is reached
- `approval.escalate` — produced if escalated

---

### E. Governed Intake Outcome Review (Project V, Planning Authority)

#### What this covers

The governed review of a proposed intake outcome in `workflows/project-intake-workflow.md`
that has material planning impact and requires human approval before the outcome
becomes active.

Not every intake outcome requires this review. Intake evaluation is primarily a
planning-authority action that Project V owns. This transition class applies only when
the proposed outcome — typically project creation with material planning impact,
significant cost implications, or cross-system scope changes — rises to the threshold
where the governing review gate at Stage 5 of the intake workflow is required.

This is a Class B event in the typical case. It may reach Class C when the intake
outcome would activate a project with significant cost or cross-system scope.

#### Distinction from Class B (Return-to-Planning)

This transition class is not the same as the Return-to-Planning Receipt / Review
(Class B). The key distinctions:

- Return-to-planning review is triggered by execution findings returning from V Forge;
  intake review is triggered by a proposed planning outcome before any cross-system
  action has occurred
- Return-to-planning review concerns whether planning reconsideration should proceed
  after an execution-side finding; intake review concerns whether a proposed intake
  outcome may become active
- Both use the `awaiting_review` pending state; the context and entity reference
  differ (see Activity Trail section below)

#### Initiating system

**Project V** governs the intake review and generates the human review request
where required. Intake evaluation is a planning-authority function; no other system
initiates or overrides this review.

#### Review request

The review request must carry the minimum semantic contents defined in the
Shared Mechanics Pattern, with specific attention to:

- the specific intake outcome being proposed (project creation, or another governed outcome)
- the signal basis and evidence posture that supports the proposed outcome
- what material planning impact, cost implication, or cross-system scope change
  triggers the review requirement
- that the intake outcome has not yet been activated — it is pending review
- what Project V's assessment is and why human review is required at this stage

#### Pending state

While intake outcome review is pending, the workflow must be in:

**`awaiting_review`**

The intake evaluation is complete and a proposed outcome has been determined.
The review request has been generated. The intake outcome has not been activated.
No downstream consequences of the proposed outcome (project creation, handoff
preparation, etc.) may proceed while in `awaiting_review`.

Project V must not treat a proposed intake outcome as active while in `awaiting_review`.

#### Post-review

On `approved`: The intake outcome becomes active. Downstream workflow routing
proceeds per the outcome type — project creation, defer, hold, or other governed
outcome. The approval event is recorded in the activity trail.

On `rejected`: The proposed intake outcome does not become active. The workflow
returns to the appropriate planning state. The rejection is preserved as a governed
outcome. Rejection continuity applies: the intake item must be preserved with the
rejection reason and scope.

On `escalated`: The workflow enters governed escalation handling. The intake item
remains in its current state. No outcome is activated.

On `expired`: The prior pending approval cannot be silently reused. If the intake
basis has materially changed since the review was requested, a new review request
must be generated. If the basis remains current, the request may be resubmitted
with the same intake item context.

#### Activity trail

- `approval.request` — produced by Project V when the intake outcome review request is generated
- `approval.decide` — produced when the review outcome is reached
- `approval.escalate` — produced if escalated

For the integration map minimum fields for intake review events, see
`../ecosystem/activity-trail-integration-map.md` Section 5 (the intake review
posture aligns with the `approval.request` / `approval.decide` family; the
`entity_type` is `intake_outcome` and the `entity_id` is the intake item identity).

---

## Pending-State Vocabulary

The following is the canonical vocabulary for approval-pending states across the
ecosystem. Interface and workflow docs must use these terms rather than inventing
new names for the same posture.

| Term | Used when |
|---|---|
| `awaiting_approval` | An explicit approval request has been generated and is unresolved. The transition has not proceeded. Covers handoff activation and replanning with supersedence. |
| `awaiting_review` | Returned findings or a proposed reconsideration requires human review before planning may act on it. The specific action pending review has not been activated. Covers return-to-planning receipt / review (Class B) and governed intake outcome review (Class E). |
| `awaiting_authorization` | A cross-system readiness convergence is established and an authorization request is pending for a launch-sensitive transition. Covers launch authorization. |
| `escalated_for_review` | The approval or review could not be resolved at the current governance level. The workflow is in governed escalation handling. Applies across all five transition classes after an escalation outcome. |

**Rules for using this vocabulary:**

- Use the term that matches the transition class as defined above.
- Do not invent synonyms. If you find yourself writing "awaiting_activation" or
  "pending_human_review," use the canonical term instead.
- `awaiting_approval` is the default pending term for most approval-sensitive
  transitions. Use the more specific terms only where defined above.
- All four terms are visible, named, non-progressing states. No transition may
  silently skip from one state to a post-approval state without a governed decision
  being recorded.

---

## Interface and Workflow Usage Rule

This section defines what local docs must and must not contain regarding approval mechanics.

### Interface docs must contain

For each approval-sensitive event on the interface:

- **Which events are approval-sensitive** — identify the specific transitions on this
  interface that require an approval event
- **Which system initiates** — for this specific seam, which system generates
  the approval request
- **What local pending state applies** — which canonical pending-state term applies
  for this interface's approval event
- **A reference to this document** — `approval-mechanics-seam-model.md` — for
  the shared mechanics

Interface docs must not independently redefine the shared approval mechanics pattern.
They own the seam-specific facts; this document owns the shared mechanics.

### Workflow docs must contain

For each approval-gate stage:

- **Which stage has the approval gate** — identify the specific stage where the
  approval event occurs
- **Which approval class applies** — Class A, B, C, or D per the Tier 1 model
- **Which local pending state applies** — which canonical term applies for this
  workflow's pending posture at this stage
- **Which outcome triggers which stage transition** — for each decision outcome,
  what stage the workflow advances to or returns to
- **A reference to this document** — `approval-mechanics-seam-model.md` — for
  the shared mechanics

Workflow docs must not independently redefine the shared approval mechanics pattern.
They own the stage-specific transitions; this document owns the shared mechanics.

### What local docs must not do

- Redefine the full shared approval mechanics pattern independently
- Invent new pending-state terms without adding them to the vocabulary section above
- Treat a deferred reference to `approval-and-escalation-model.md` as a substitute
  for specifying seam-specific facts
- Describe approval request contents in a way that contradicts the required
  semantic contents defined in this document

---

## Anti-Drift Rules

### 1. No duplicated mechanics

Interface and workflow docs must reference this document for shared mechanics.
They must not independently redefine the request/pending/decision/re-entry pattern.
If two seam docs describe the same approval mechanics in slightly different words,
they are already drifting.

### 2. No alternate approval doctrine

Interface docs and workflow docs are not approval governance authority.
If an interface doc starts describing what constitutes valid approval in language
that extends or contradicts this document, that is a governance drift event.

### 3. No casual pending-state invention

New pending-state vocabulary may only be added to the canonical vocabulary table
in this document. Workflow or interface docs that use pending-state terms not in
that table must be corrected.

### 4. No approval without activity trail

An approval event that does not produce `approval.request` and `approval.decide`
records in the activity trail is not a governed approval event. Implementations
that skip activity trail logging for approval events are not compliant.

### 5. No stale approvals silently reused

An approval event that was satisfied in a prior session, workflow stage, or
planning cycle does not carry forward automatically. If the underlying scope,
conditions, or planning basis have materially changed, the prior approval is
expired and a new request must be generated. The `expired` outcome exists for
this case.

### 6. No self-authorization

No system may approve its own approval request. Approval requires a human actor
with the required authority, as defined in the Tier 1 model. Agent systems may
generate the request and enter the pending state; they may not produce the `approved`
outcome for themselves.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- every approval-sensitive seam transition follows the request / pending / decision / re-entry pattern
- the initiating system is named per transition class and generates the request
- pending states are canonical and must not be bypassed or silently extended
- the four decision outcomes are the complete set
- activity trail logging is required for every approval event
- this document provides the shared mechanics; interface and workflow docs provide
  the seam-specific facts
- `awaiting_review` covers both return-to-planning review (Class B) and intake outcome review (Class E); the distinction is in context and entity reference, not the pending state term

If an LLM treats an approval request as equivalent to the approval itself, treats
the pending state as pauseable by convenience, skips activity trail logging, or
invents new pending-state vocabulary, this document is failing.

---

## Usage

This document should be used:

- when implementing any of the five approval-sensitive transition classes
- when writing or reviewing the approval-related sections of interface and workflow docs
- when checking whether a pending state is correctly named and observable
- when verifying that activity trail logging covers approval events on a seam
- when deciding whether a prior approval is still valid or has expired

---

## Related Docs

- `approval-and-escalation-model.md`
- `allowed-agent-actions-matrix.md`
- `decision-continuity-doctrine.md`
- `../ecosystem/activity-trail-model.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/handoff-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../workflows/project-intake-workflow.md`
