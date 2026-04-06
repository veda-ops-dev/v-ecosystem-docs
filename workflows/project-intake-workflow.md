# Project Intake Workflow

## Purpose

This document defines the governed workflow by which planning-relevant signal or
a valid operator/strategy trigger becomes a Project V intake outcome.

It exists to answer:

```text
What stages does the project intake workflow move through, what kind of trigger
started it, what event causes each transition, when is the intake basis sufficient
to act, when is a bounded evidence request the right move, and what governed
outcome is produced?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the concrete stage sequence from intake trigger to governed intake outcome
- trigger types and entry conditions
- how signal receipt, framing, interpretation, evaluation, and outcome differ
- approval / review gate behavior where governance-sensitive outcomes apply
- degraded-mode handling when the intake basis is insufficient, stale, or contradictory
- re-entry rules when additional bounded evidence returns
- outcome routing for create / defer / hold / reject / request-more-evidence
- activity-trail obligations for intake events

---

## Out of Scope

This document does not define:

- the VEDA → Project V signal interface data contract — that belongs in
  `interfaces/veda-to-project-v-signal-interface.md`
- the AD-03 evidence request interface contract — that belongs in
  `interfaces/project-v-to-veda-evidence-request-interface.md`
- detailed Project V internal project schema
- detailed opportunity scoring or evaluation formulas
- full approval class definitions — those belong in
  `governance/approval-and-escalation-model.md` and
  `governance/approval-mechanics-seam-model.md`
- the handoff workflow after a project is created — that belongs in
  `workflows/handoff-workflow.md`

---

## System

- workflows

---

## Relationship to Governing Docs

This workflow governs intake sequencing and transition rules. Interface contracts and
approval mechanics remain in their respective authority docs.

- `interfaces/veda-to-project-v-signal-interface.md` — defines how VEDA delivers
  planning-relevant signal to Project V. This workflow begins after a valid signal
  delivery has been confirmed, or when a valid operator/strategy trigger exists.
- `governance/approval-mechanics-seam-model.md` — defines shared seam-level approval
  mechanics. This workflow references it for governance-sensitive intake outcomes.
- `ecosystem/activity-trail-integration-map.md` — defines canonical action type
  mapping for events this workflow produces.

---

## Core Rule

Signal does not become a project automatically.
Intake is where planning decides whether and what something should become.

The five phases of intake are distinct:
- **Receipt** — signal or trigger reaches Project V
- **Framing** — Project V identifies the planning question
- **Interpretation** — Project V interprets the trigger in planning terms
- **Evaluation** — Project V determines whether there is enough basis to act
- **Outcome** — Project V produces a governed intake outcome

None of these phases may substitute for or imply the others.

---

## Trigger Types and Entry Conditions

### Valid trigger types

**Trigger Type A — VEDA-delivered signal**
A valid VEDA → Project V signal delivery has been received and confirmed through
`interfaces/veda-to-project-v-signal-interface.md`. The delivery carries bounded
planning-relevant signal, freshness classification, trust/provenance metadata, and
a planning concern reference.

Entry: Receipt is confirmed (Stage 1 entry). Workflow enters normally.

**Trigger Type B — Operator or strategy-driven trigger**
An operator or strategy review has identified a specific planning question that
requires intake evaluation. The trigger must be:
- specific enough to frame a planning question
- within Project V's planning authority
- not merely a loose instruction to "explore" or "go create projects"

Entry: Workflow enters at Stage 2 (framing) directly — bypassing Stage 1 because
no VEDA delivery event has occurred. The same planning and governance boundary
rules apply from Stage 2 forward.

### What does NOT validly start intake

- Raw unbounded VEDA observability state (not a delivery package)
- Execution-side findings without a planning question attached
- Informal operator mentions without a bounded planning question
- VEDA signal that has not passed the validity conditions in the signal interface
- Signal that is known to be stale or of insufficient trust posture at receipt

### Minimum clarity for evaluation

An intake item must be clear enough to frame a planning question before Stage 3
can begin. If the trigger is too vague to frame, it must be rejected at Stage 2
or classified as requiring additional bounded evidence before evaluation.

---

## Workflow Stages

### Stage 1 — Signal Delivery Received and Confirmed (Trigger Type A only)

**Entry event:** VEDA delivers a bounded planning-relevant signal package to Project V;
Project V confirms receipt.

**What happens:**
Project V confirms receipt of the VEDA signal delivery per the signal interface.
The package is now available for framing. Receipt does not mean framing has occurred
or a project will be created. The signal remains VEDA-owned truth.

**Activity trail:** Signal delivery receipt is covered in
`ecosystem/activity-trail-integration-map.md` Section 1: `signal.delivery.confirmed`
record produced by Project V on receipt.

**Exit condition → Stage 2:** Receipt confirmed; intake item can be framed.
**Exit condition → Stage 7 (degraded):** Delivery package fails freshness or
validity check at receipt; signal is too stale or provenance is insufficient.

**Boundary rule:** VEDA retains signal/evidence ownership. Receipt does not transfer
signal ownership to Project V. Project V does not begin planning mutation at this stage.

---

### Stage 2 — Intake Framing

**Entry event:** Stage 1 complete (Type A), or valid operator/strategy trigger exists (Type B).

**What happens:**
Project V frames the intake question:
- what is being considered at a planning level (possible new project, reconsideration
  of an existing project, strategic opportunity evaluation)
- what planning question needs to be answered
- whether the trigger is sufficiently clear to evaluate
- what signal, evidence, or basis is available to evaluate against

If the trigger is a Type B operator/strategy input, framing must translate that
input into a bounded planning question without blurring planning ownership.

**Exit condition → Stage 3:** A bounded planning question is framed and the trigger
is clear enough for interpretation.
**Exit condition → Stage 7 (degraded):** Trigger too vague; cannot frame a planning
question without additional bounded evidence or operator clarification.

**Boundary rule:** VEDA does not frame the intake decision. Signal informs framing;
it does not replace it. Operator direction may enter here but does not bypass
planning boundaries.

---

### Stage 3 — Planning Interpretation

**Entry event:** Stage 2 complete; planning question framed.

**What happens:**
Project V interprets the intake trigger in planning terms:
- project relevance and priority implications
- whether the signal affects an existing project or suggests a new one
- what the intake item means for current planning posture
- what evidence trust posture applies to the signal basis
- any planning-side constraints or conditions

**Exit condition → Stage 4:** Interpretation complete; enough context to evaluate
whether a planning outcome is warranted.
**Exit condition → Stage 7 (degraded):** Signal is contradictory, trust posture is
too low, or interpretation reveals insufficient basis to continue without more evidence.

**Boundary rule:** Interpretation is not project creation. Interpreting that something
might be relevant does not commit Project V to any outcome.

---

### Stage 4 — Intake Evaluation

**Entry event:** Stage 3 complete; planning interpretation established.

**What happens:**
Project V evaluates whether there is enough basis to produce a governed intake outcome:
- is the signal or planning basis strong enough and current enough to act?
- is the intake item clear and bounded enough for project creation?
- does the basis require more evidence before an honest outcome is possible?
- is the intake item valid but not timely (defer) or not prioritized (hold)?
- does the intake item conflict with or duplicate existing project work?

**Exit condition → Stage 5 (sufficient basis):** Evaluation concludes there is
enough basis to produce an intake outcome.
**Exit condition → Stage 6 (additional evidence needed):** Evaluation concludes
the basis is insufficient for an honest outcome — a bounded evidence request is
the right next step rather than forcing an outcome on weak signal.
**Exit condition → Stage 7 (degraded):** Basis is too stale, contradictory, or
insufficient even for a deferred outcome; the trigger must be closed or escalated.

**Governance-sensitive evaluation:** If the anticipated intake outcome is project
creation with material planning impact, governance review may be required before
the outcome is finalized. If so, the evaluation stage identifies this requirement
and the workflow proceeds to Stage 5 with that gate noted.

**Boundary rule:** Evaluation is where Project V makes an honest determination
about sufficiency. Forcing an outcome when the basis is weak defeats the purpose
of intake governance. "Request additional bounded evidence" is a valid outcome,
not a failure.

---

### Stage 5 — Intake Outcome Produced

**Entry event:** Stage 4 evaluation concludes sufficient basis exists for a governed
outcome.

**What happens:**
Project V produces one of the allowed intake outcomes:

| Outcome | When appropriate |
|---|---|
| **Create project** | Signal basis is strong, current, and sufficient; planning question is bounded; project creation is warranted |
| **Defer** | Item is valid but not sufficiently prioritized relative to current planning posture |
| **Hold for later reconsideration** | Item is valid but timing is not right; conditions may change |
| **Reject** | Item is not a fit for project creation; rejection continuity must be preserved |

**Governance-sensitive outcomes:** If project creation involves material planning
impact, significant cost implications, or cross-system scope changes, human review
may be required before the outcome becomes active.

If human review is required:
- pending state: `awaiting_review` per `governance/approval-mechanics-seam-model.md`
- Project V generates a review request; outcome does not activate until review returns
- review decision outcomes follow the mechanics in the seam-approval model

**Activity trail:** Intake outcomes must be durably recorded. Use `project.create`
for the project creation outcome. For defer, hold, and reject outcomes, use the
canonical action types `intake.defer`, `intake.hold`, and `intake.reject` respectively,
per `ecosystem/activity-trail-integration-map.md` Section 9. If a review gate is
required, use `approval.request` and `approval.decide` action types per integration
map Section 5b posture (closest applicable mapping for planning-side review).

**Exit condition → Stage 8 (outcome routing):** Outcome is produced and active;
workflow routes to the appropriate next governed path.

**Boundary rule:** VEDA does not produce the intake outcome. V Forge does not produce
the intake outcome. Only Project V produces intake outcomes.

---

### Stage 6 — Bounded Evidence Request

**Entry event:** Stage 4 evaluation concludes that additional bounded evidence is needed
before an honest intake outcome is possible.

**What happens:**
Project V issues a bounded evidence request to VEDA through the evidence request path
(AD-03 model):
- Project V sends a bounded planning-side request specifying the specific planning
  question that requires additional evidence
- VEDA curates a bounded response package relevant to that planning need
- VEDA delivers the response through the existing VEDA → Project V push delivery path
  (the same `interfaces/veda-to-project-v-signal-interface.md` path, triggered by
  the request rather than proactively)

**The evidence request must be bounded.** It is not open-ended observatory access.
Project V expresses a specific planning need ("we need evidence on topic X to evaluate
whether this intake item meets threshold Y"). VEDA curates; Project V does not
specify which records to retrieve.

**Re-entry:** When VEDA delivers the evidence response:
- If the framing question is still open: re-enter at Stage 2 (framing)
- If framing is established and the question is whether the basis is sufficient:
  re-enter at Stage 3 (interpretation) with the new evidence in context

**Activity trail:** The evidence request leg and VEDA's delivery response both
produce activity records per `ecosystem/activity-trail-integration-map.md`:
- evidence request: `evidence.request` action type per integration map Section 7
- VEDA delivery response: `signal.delivery` record (delivery trigger type:
  `request_response`) per integration map Section 1

**Exit condition → Stage 2 or Stage 3:** Evidence delivered and confirmed; re-enter
at appropriate stage.
**Exit condition → Stage 5 (reject or hold):** If evidence returns and still does
not provide sufficient basis, Stage 4 evaluation should produce a defer/hold/reject
outcome rather than looping indefinitely.

**Boundary rule:** No new return channel is created. Evidence returns through the
existing VEDA → Project V delivery path. Project V does not query VEDA's records
directly.

---

### Stage 7 — Degraded / Insufficient Basis

**Entry event:** Signal fails validity at receipt (Stage 1); trigger too vague to
frame (Stage 2); interpretation reveals contradictory or insufficient basis (Stage 3);
or evaluation determines basis is too weak even for a deferred outcome (Stage 4).

**What happens:**
The intake item cannot proceed normally. The specific degraded condition must be
identified and handled:

| Condition | Handling |
|---|---|
| Signal stale or invalid at receipt | Do not enter framing; intake is not triggered; preserve the delivery failure in trail |
| Trigger too vague (Type B) | Request operator clarification or close the trigger; do not force framing |
| Contradictory signal | Flag contradiction explicitly; route to bounded evidence request (Stage 6) or close |
| Trust posture too low | Do not produce an outcome on low-trust signal; route to Stage 6 or close |
| Basis too weak for any outcome | Close intake item; preserve the closure reason as a durable planning record |

**Exit condition:** The specific degraded condition is resolved (route to appropriate
stage) or the item is closed with a durable record of why it could not proceed.

**Boundary rule:** A degraded intake item must not be resolved by producing an
intake outcome on an insufficient basis. Forcing a project creation on weak signal
is worse than closing the intake item honestly.

---

### Stage 8 — Post-Intake Outcome Routing

**Entry event:** Stage 5 outcome active.

**What happens:**
Project V follows the appropriate next step based on the intake outcome.

See Outcome Routing section below for detailed routing per outcome type.

---

## Transition Summary Table

| From | Event | To |
|---|---|---|
| Valid Type A trigger | Signal delivery confirmed | Stage 1 |
| Valid Type B trigger | Operator/strategy trigger | Stage 2 |
| Stage 1 | Receipt confirmed | Stage 2 |
| Stage 1 | Package fails validity / freshness | Stage 7 |
| Stage 2 | Planning question framed | Stage 3 |
| Stage 2 | Trigger too vague to frame | Stage 7 |
| Stage 3 | Interpretation complete; sufficient context | Stage 4 |
| Stage 3 | Basis contradictory or insufficient | Stage 7 |
| Stage 4 | Sufficient basis for outcome | Stage 5 |
| Stage 4 | Insufficient basis; evidence needed | Stage 6 |
| Stage 4 | Basis too weak for any outcome | Stage 7 |
| Stage 5 | Outcome produced and active | Stage 8 (routing) |
| Stage 5 (review required) | Review request generated | `awaiting_review` → Stage 5 on review |
| Stage 6 | Evidence delivered and confirmed | Stage 2 or Stage 3 (re-entry) |
| Stage 6 | Evidence returns; still insufficient | Stage 5 (defer/hold/reject) |
| Stage 7 | Condition resolved | Appropriate stage |
| Stage 7 | Cannot resolve | Closed with durable record |
| Stage 8 | — | Per outcome routing |

---

## Degraded Mode and Interruption Handling

### Signal stale or invalid at receipt

If the signal package received at Stage 1 carries a freshness classification of
stale or expired, or if provenance cannot be established, Project V must not proceed
into framing. The delivery failure must be recorded. VEDA may be prompted to
re-evaluate whether a refreshed package is available. Alternatively, the item may
wait until VEDA delivers a current signal package.

### Operator/strategy trigger too vague

If a Type B trigger cannot be translated into a bounded planning question, the
trigger must be closed or returned to the operator with a request for clarification.
It must not be forced into framing as-is.

### Signal contradictory within a delivery package

If the signal delivered includes components that contradict each other (e.g.,
one signal class supports project creation while another contradicts the opportunity
thesis), Project V must surface the contradiction explicitly rather than resolving
it by ignoring half the signal. This is a Stage 3 condition that routes to Stage 6
(bounded evidence request for clarifying signal) or Stage 7 (close if unresolvable).

### Intake basis changes while review is pending

If a governance-sensitive intake outcome has generated a review request and
conditions materially change before the review completes — new contradicting signal
arrives, the planning priority shifts, or the intake basis is otherwise invalidated —
Project V must assess whether the pending review is still valid. If the basis has
changed materially, the review request must be re-evaluated. A `awaiting_review`
state pending on a stale basis must not automatically proceed when a decision arrives
on the old basis.

### Intake item resurfaces after defer / hold / reject

If an intake item was previously deferred, held, or rejected, and new signal or
changed conditions cause it to resurface:
- deferred and held items may re-enter at Stage 2 (new trigger) with the prior
  intake history preserved as context — not as a clean slate
- rejected items must be assessed against the rejection continuity record; if
  conditions have genuinely changed materially, a new intake may begin; if conditions
  are substantially the same, the re-entry must acknowledge the prior rejection
  explicitly

---

## Outcome Routing

After Stage 5 produces a governed intake outcome, route to the appropriate next step.

### Create Project

Project V begins project planning and decomposition within Project V.

**This does not equal handoff.** A created project is in planning until
readiness and handoff conditions are later met through the governed handoff
workflow (`workflows/handoff-workflow.md`).

The created project enters Project V's planning lifecycle. VEDA continues to own
signal truth. V Forge is not yet involved.

### Defer

The intake item is valid but not sufficiently prioritized. Project V records the
deferral with the reason and expected re-evaluation conditions. Decision continuity
is preserved. The item may re-enter the workflow if conditions change.

### Hold for Later Reconsideration

The intake item is valid but timing is not right. Project V records the hold with
the reason and expected triggering conditions for reconsideration. The item is not
active but is preserved for future re-entry.

### Reject

The intake item is not a fit for project creation. Project V records the rejection
with the reason and the scope of what was rejected. Rejection continuity must be
preserved per `governance/decision-continuity-doctrine.md` — a rejected item must
not be repeatedly rediscovered as if no prior decision existed.

### Request Additional Bounded Evidence (→ Stage 6)

When this is an evaluation outcome rather than a final intake outcome, the workflow
routes to Stage 6. See Stage 6 definition above for full mechanics.

---

## Approval Gate: Seam-Specific Facts

Not every intake outcome requires a human approval gate. Intake evaluation is
primarily a planning-authority action that Project V owns.

Where governance review is required — particularly for project creation with material
planning impact, significant cost implications, or cross-system scope — the following
applies:

| Fact | Value |
|---|---|
| Initiating system for review | Project V |
| Canonical pending state | `awaiting_review` |
| Approval class | Class B or Class C depending on scope and cost (per `governance/approval-and-escalation-model.md`) |
| Review does not equal project creation | True — the intake outcome activates only after review approves |

For the full mechanics — review request contents, decision re-entry rules, escalation
path — see `governance/approval-mechanics-seam-model.md`.

**Important:** The current `governance/approval-mechanics-seam-model.md` does not
define intake-specific shared mechanics as a named transition class. The closest
applicable seam is Section B (Return-to-Planning Receipt / Review), which covers
Project V governing a review of received findings. Use that posture as a reference
for governance-sensitive intake outcomes. If intake-specific mechanics are later
added to the seam-approval model, defer to those.

---

## AD-03 Evidence Request Posture

When Stage 6 (bounded evidence request) is triggered, the following posture applies:

- Project V expresses a specific planning-side evidence need to VEDA
- The request is bounded — Project V states what planning question requires more
  evidence, not which VEDA records to retrieve
- VEDA curates a bounded response and delivers it through the existing
  VEDA → Project V push delivery path
- No separate return channel is created
- The response returns to this workflow at Stage 2 or Stage 3 depending on
  how much framing context remains established

This is consistent with AD-03 (request-for-package model). Project V does not
query VEDA's observatory records directly.

---

## Activity Trail Requirements

Intake events must produce activity trail records using canonical action types from
`ecosystem/activity-trail-model.md` and `ecosystem/activity-trail-integration-map.md`.

| Workflow event | Action type | Producing system |
|---|---|---|
| Signal delivery confirmed (Stage 1) | `signal.delivery.confirmed` | Project V |
| Project creation outcome (Stage 5) | `project.create` | Project V |
| Defer outcome (Stage 5) | `intake.defer` | Project V |
| Hold outcome (Stage 5) | `intake.hold` | Project V |
| Reject outcome (Stage 5) | `intake.reject` | Project V |
| Degraded closure (Stage 7) | `intake.close` | Project V |
| Review request generated (Stage 5, if review required) | `approval.request` | Project V |
| Review decision received | `approval.decide` | Operator / review surface |
| Review escalated | `approval.escalate` | Project V |

For the full field-level mapping detail — including required entity references and minimum
additional fields — see `ecosystem/activity-trail-integration-map.md` Section 9.

**Evidence request activities:** The evidence request leg (Stage 6 outbound) uses
the `evidence.request` action type per integration map Section 7. The VEDA delivery
response uses `signal.delivery.confirmed` per integration map Section 1 (with
`delivery_trigger_type: request_response`).

Activity records that are not produced are not governed events. Intake outcomes must
be durably recorded, not left only in session memory.

---

## Decision Continuity

Intake outcomes must be preserved so that later sessions, operators, and workflow
stages can understand what was decided and why:

- rejected items must be preserved with rejection reason and scope
- deferred and held items must be preserved with expected re-evaluation conditions
- a re-entered item after defer/hold must reference the prior intake history

If an intake event leaves no durable record, it has not produced governed continuity —
it has produced drift.

See `governance/decision-continuity-doctrine.md`.

---

## Human-In-The-Loop Principle

Project intake is governance-sensitive because it can create new project work or
materially alter planning direction.

Human review may be required for:

- project creation with material planning impact
- project creation with significant cost or cross-system implications
- intake outcomes that would significantly change ecosystem priorities

Class A intake outcomes (defer, hold, request evidence) typically do not require
human review unless circumstances are unusual. Class B or C outcomes (project creation
with material impact) may.

An agent may support framing, interpretation, and evaluation at Stages 2–4.
An agent must not self-authorize a governance-sensitive intake outcome.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the intake workflow has eight distinct named stages with concrete transitions
- signal receipt, framing, interpretation, evaluation, and outcome are five separate
  phases — none may substitute for another
- project creation is not automatic from signal or operator direction
- "request additional bounded evidence" is a valid, governed Stage 6 path — not a
  failure or a workaround
- evidence requests use the AD-03 model: Project V expresses a bounded need; VEDA
  curates; response returns through the existing delivery path
- deferred, held, and rejected outcomes preserve decision continuity for future
  reconsideration
- a created project is in planning — it is not a handoff
- activity trail records are required for governed intake outcomes

If the workflow is implemented as automatic project creation from signal, or as a
boundary-free shortcut from operator intent to project creation, the doctrine is wrong.

---

## Usage

This document should be used:

- when implementing intake workflow states and transitions
- when deciding whether a signal or trigger validly starts intake
- when determining whether evaluation basis is sufficient for an outcome
- when routing to a bounded evidence request instead of forcing a weak outcome
- when preserving defer/hold/reject continuity for future reconsideration
- when auditing whether intake outcomes are durably recorded

---

## Related Docs

- `../interfaces/veda-to-project-v-signal-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/activity-trail-integration-map.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/project-v.md`
- `handoff-workflow.md`
- `maintenance-and-replanning-workflow.md`
