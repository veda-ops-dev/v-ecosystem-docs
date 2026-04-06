# Launch Readiness Workflow

## Purpose

This document defines the governed cross-system workflow by which the V Ecosystem
confirms launch readiness and obtains governed authorization before launch-sensitive,
public-facing, or spend-creating execution proceeds.

It exists to answer:

```text
What stages does the launch-readiness workflow move through, what readiness inputs
each stage depends on, what event causes each transition, what pending state applies,
how readiness convergence differs from authorization, and what happens when readiness
is missing, stale, or contradicted?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the concrete stage sequence from pre-launch readiness evaluation through
  cross-system convergence to governed launch authorization and activation
- readiness inputs and convergence criteria per system
- authorization gate behavior and canonical pending state
- degraded-mode and interruption handling when readiness cannot be confirmed
- re-entry rules when readiness basis becomes stale or contradicted
- downstream routing after authorization approved, rejected, or expired
- activity-trail obligations for authorization events

---

## Out of Scope

This document does not define:

- detailed execution mechanics of specific launch types
- vendor-specific publication or distribution workflows
- post-launch observation — that belongs in `workflows/post-launch-observation-workflow.md`
- full approval class definitions and escalation principles — those belong in
  `governance/approval-and-escalation-model.md` and
  `governance/approval-mechanics-seam-model.md`
- external action preconditions in detail — those belong in
  `governance/external-action-governance.md`
- Project V internal planning workflow
- V Forge internal execution workflow

---

## System

- workflows

---

## Relationship to Governing Docs

This workflow governs sequencing and transition rules. Approval mechanics, interface
contracts, and external action governance remain in their respective authority docs.

- `governance/approval-mechanics-seam-model.md` — defines the shared seam-level
  approval mechanics pattern used at Stage 5 (authorization). This workflow carries
  the seam-specific facts; the mechanics doc carries the shared pattern.
- `governance/approval-and-escalation-model.md` — Tier 1 authority for approval
  classes, escalation triggers, and approval posture. Launch authorization is Class C.
- `ecosystem/activity-trail-integration-map.md` — defines the canonical action type
  mapping for authorization events in this workflow.

---

## Core Rule

Readiness convergence and launch authorization are two distinct required phases.
Neither may substitute for or imply the other.

- **Readiness convergence** (Stage 4) — all three systems have confirmed their
  dimension of launch readiness and no unresolved cross-system gap exists.
  This is a **precondition** for authorization, not the authorization itself.
- **Launch authorization** (Stage 5) — a human operator with the required authority
  grants explicit governed approval for the specific launch scope.
  This is the authorization, not a restatement of readiness.

Convergence does not mean launch is approved. A system cannot self-authorize launch.
An agent confirming readiness is not launch authorization.

---

## Launch-Sensitive Action Definition

A launch-sensitive action is any action that:

- creates or changes externally visible content, products, or services
- initiates public-facing distribution, publication, or communication
- activates paid spend or billable external activity at launch scale
- creates changes that are difficult or impossible to reverse
- commits the ecosystem to external-facing obligations or representations

Launch-sensitive actions require Class C approval posture.

---

## Entry Conditions

This workflow may begin only when:

- execution is approaching a scope that involves launch-sensitive action
- V Forge has reached a point in the active handoff scope where launch-sensitive
  execution is the next governed step
- the handoff is confirmed active (Stage 5 complete in `workflows/handoff-workflow.md`)
- there is sufficient basis in Project V to begin a planning-side launch readiness
  assessment

This workflow must not be entered because:

- the work looks complete internally
- the timeline is pressing
- a prior launch succeeded without issue
- an operator believes the work is ready
- the launch scope appears small or low-risk

---

## Readiness Inputs and Convergence Criteria

Stage 4 convergence is achieved only when all three of the following are confirmed
simultaneously. Each must be current — a prior confirmation does not carry forward
indefinitely.

### Project V readiness input
- Planning-side launch readiness determination is complete
- The governing decisions supporting this launch scope are current and applicable
- The launch scope is bounded and consistent with the approved handoff
- No planning-side conditions would block or defer launch

### VEDA readiness input
- Current VEDA signal and evidence support the planned launch scope
- Evidence freshness meets the materiality standard for launch-sensitive decisions
  (applied conservatively — see Evidence Currency Principle below)
- No recently surfaced signal contradicts the planning basis
- Evidence trust posture is adequate for launch-sensitive decision-making

### V Forge readiness input
- Execution work within the launch scope is complete and verified
- Pre-launch verification obligations from `governance/testing-and-verification-doctrine.md`
  are satisfied (Class V1 precondition verification, Class V4 external action
  verification where applicable, Class V5 outcome verification for completed work)
- No mid-execution findings have emerged that affect launch safety
- External action preconditions are satisfied per `governance/external-action-governance.md`

### Convergence failure
Convergence fails if any of the above is missing, incomplete, contradictory, or
has become stale. A single system's readiness posture being absent or unresolved
is sufficient to block convergence.

---

## Workflow Stages

### Stage 1 — Planning-Side Launch Readiness Assessment

**Entry event:** Workflow entered per entry conditions above.

**What happens:**
Project V confirms the planning basis supports launch readiness for the relevant scope:
- identifies the launch scope and governing decisions
- confirms approval posture class (Class C for launch-sensitive)
- confirms which VEDA signal and evidence informed the planning-side basis
- identifies any planning-side blockers, conditions, or constraints
- produces a planning-side readiness confirmation that can be referenced at Stage 4

**Exit condition → Stage 2:** Planning-side readiness confirmed and documented.
**Exit condition → Stage 7 (blocked):** Planning-side basis cannot be confirmed;
launch is blocked at planning level.

**Boundary rule:** Project V confirming planning readiness does not authorize
V Forge to begin launch-sensitive execution. This is one input to Stage 4
convergence, not an authorization event.

---

### Stage 2 — VEDA Evidence and Signal Currency Confirmation

**Entry event:** Stage 1 complete.

**What happens:**
Project V reviews whether VEDA signal and evidence support the planned launch scope:
- confirms evidence freshness against the materiality standard
- confirms no recently surfaced signal contradicts the planning basis
- flags any signal or evidence gaps that would make an honest launch
  readiness determination impossible

VEDA provides evidence and signal through the governed delivery path
(`interfaces/veda-to-project-v-signal-interface.md`). If additional evidence
is needed, it may be requested through the evidence request path (AD-03).

**Exit condition → Stage 3:** VEDA evidence and signal confirmed current and supportive.
**Exit condition → Stage 7 (blocked):** Evidence is insufficient, stale, or contradictory.

**Stale-evidence rule:** If the evidence basis used at Stage 1 has become materially
stale since that assessment was made, Stage 2 must not pass on the prior evidence.
A Stage 2 confirmation is only valid for a limited window. If authorization is not
obtained before that window closes, Stage 2 must be re-confirmed.

**Boundary rule:** VEDA signal confirming a favorable condition is not launch
authorization. VEDA does not make launch decisions.

---

### Stage 3 — V Forge Execution-Side Pre-Launch Verification

**Entry event:** Stage 2 complete.

**What happens:**
V Forge confirms execution is prepared for the launch-sensitive scope:
- confirms completion and verification status of execution work within scope
- applies pre-launch verification obligations per `governance/testing-and-verification-doctrine.md`
- surfaces any unresolved execution findings that affect launch safety
- confirms external action preconditions per `governance/external-action-governance.md`

If verification cannot be completed — due to unclear conditions, unavailable tooling,
or ambiguous execution findings — V Forge must surface that gap explicitly rather
than proceeding as though verification passed.

**Exit condition → Stage 4:** V Forge execution-side verification complete; no
unresolved launch-blocking findings.
**Exit condition → Stage 7 (blocked):** Verification cannot be completed or unresolved
findings exist.

**Boundary rule:** V Forge surfacing verification results is an execution-side
assessment. It is not authorization. V Forge must not begin launch-sensitive
execution at this stage.

---

### Stage 4 — Cross-System Convergence Assessment

**Entry event:** Stages 1, 2, and 3 all complete and current.

**What happens:**
Project V synthesizes the cross-system readiness picture. Convergence is assessed
against the criteria in the Readiness Inputs and Convergence Criteria section above.

All three system readiness inputs must be current. If time has passed between
individual stage completions, stages that have become stale must be re-confirmed
before convergence is assessed.

Convergence must establish:
- planning-side readiness basis is present and current (Stage 1 confirmed)
- VEDA evidence and signal are current and supportive (Stage 2 confirmed)
- V Forge execution verification is complete and no blocking findings exist (Stage 3 confirmed)
- no unresolved cross-system gap exists
- the launch scope has not silently widened beyond what was assessed at each stage

**A cross-system convergence confirmation is not produced by any single system
in isolation.** A self-certification of convergence by V Forge or Project V alone
is not a governed cross-system convergence.

**Exit condition → Stage 5:** Convergence achieved; all three inputs current and consistent.
**Exit condition → Stage 7 (blocked):** Convergence fails due to missing input,
contradiction, or scope drift.

**Boundary rule:** Stage 4 convergence is a precondition for authorization, not
the authorization itself. Achieving convergence does not authorize launch.

---

### Stage 5 — Authorization Request Generated

**Entry event:** Stage 4 convergence achieved.

**What happens:**
Project V generates the launch authorization request per the approval mechanics model.
The request must contain: the specific launch-sensitive actions being authorized,
confirmation that Stage 4 convergence was established (with references to each system's
readiness confirmation), the approval class (C), the launch scope boundaries, and the
reversibility posture.

**Pending state:** `awaiting_authorization` — begins immediately on request generation.
No launch-sensitive execution may proceed while in `awaiting_authorization`.

**Approval class:** Class C. The highest governance class for approval-sensitive actions.

**Activity trail:** `approval.request` record produced by Project V. Required fields from
`ecosystem/activity-trail-integration-map.md` Section 5c: `entity_type: launch_authorization`,
`entity_id: <authorization request identity>`, `approval_class` (C), `stage4_convergence_ref`,
`launch_scope_id`, `reversibility_posture`.

**Exit condition → Stage 6:** Governed authorization decision received.
**Exit condition → Stage 8 (escalation):** Authorization escalated.
**Exit condition → Stage 9 (expired):** Authorization expires before decision.

**Boundary rule:** While in `awaiting_authorization`, no launch-sensitive execution
may proceed. V Forge must not begin launch-sensitive execution. An agent recommending
approval is not authorization.

---

### Stage 6 — Authorization Decision Received

**Entry event:** Human operator or governed approval surface reaches a decision.

**Decision outcomes and workflow consequences:**

| Outcome | Workflow action |
|---|---|
| `approved` | Proceed to Stage 7 (launch activation) |
| `rejected` | Launch does not proceed. Workflow routes to Stage 10 (no-launch / defer). |
| `escalated` | Enter Stage 8 (escalation handling). Workflow remains in `awaiting_authorization`. |
| `expired` | Authorization cannot be silently reused. Re-evaluate readiness per Stage 9. |

**Activity trail:** `approval.decide` record at decision time. Required fields from
integration map Section 5c: `entity_type: launch_authorization`,
`entity_id: <authorization request identity>`, `approval_class`, `decision`
(`approved`, `rejected`, or `expired`), `authorized_scope_id` if approved.

**Boundary rule:** Authorization approval authorizes launch-sensitive execution
within the confirmed scope. It does not authorize scope expansion. Authorization
covers the specific scope confirmed at Stage 4 — not a broader launch category.

---

### Stage 7 — Launch Activation and Execution

**Entry event:** `approved` outcome from Stage 6.

**What happens:**
V Forge proceeds with launch-sensitive execution within the authorized scope and
constraints. V Forge must:
- remain within the authorized launch scope
- halt at the earliest safe stopping point if conditions change materially
- preserve a reviewable record of what actions were taken
- surface unexpected conditions through governed reporting, not improvisation

**Exit condition:** Launch-sensitive execution completes within confirmed scope.
Workflow advances to Stage 11 (post-launch state).
**Exit condition → Stage 10 (interrupted):** Material conditions change during
execution; V Forge halts and surfaces the interruption.

**Boundary rule:** Launch authorization does not transfer planning ownership to V Forge.
Launch execution does not transfer observability ownership to V Forge. If execution
produces findings requiring planning reconsideration, the maintenance and replanning
workflow applies.

---

### Stage 8 — Escalation Handling

**Entry event:** Authorization escalated at Stage 6.

**What happens:**
The workflow remains in `awaiting_authorization`. No launch-sensitive execution proceeds.
The escalation is preserved through the governed escalation path.

**Activity trail:** `approval.escalate` record produced by Project V. Required fields
from integration map Section 5c: `entity_type: launch_authorization`,
`entity_id: <authorization request identity>`, `approval_class`, `escalation_reason`.

**Exit condition:** Escalation resolves. Outcome re-enters Stage 6 as a governed decision.

---

### Stage 9 — Authorization Expired / Readiness Reassessment

**Entry event:** Authorization expires before decision; or readiness basis changes
materially while in `awaiting_authorization`.

**What happens:**
A stale `awaiting_authorization` state is not authorization to proceed. The prior
authorization cannot be silently reused.

Project V must assess which stages have become stale during the pending window:
- Stages 1 and 2 are time-sensitive and must be re-confirmed if material time
  has passed or conditions have changed
- Stage 3 must be re-confirmed if execution-side conditions have changed
- If all three stages remain current, re-generate the authorization request (Stage 5)
- If any stage is stale, re-confirm the stale stage(s) before returning to Stage 4

**Exit condition → Stage 4:** All stages re-confirmed; convergence re-assessed.
**Exit condition → Stage 7 (blocked):** Re-assessment reveals a blocking condition.

---

### Stage 10 — No-Launch / Defer / Interrupted

**Entry event:** Authorization rejected at Stage 6; or launch-sensitive execution
interrupted at Stage 7; or blocking condition at any stage that cannot be resolved.

**What happens:**
Launch does not proceed. The outcome is a governed result — a rejected authorization
or a block is not a null event. The reason must be preserved.

Route to the appropriate path:
- If the planning basis is no longer valid: route to `workflows/maintenance-and-replanning-workflow.md`
- If a new or revised handoff is needed: route through `workflows/handoff-workflow.md`
- If the block is deferral pending additional readiness work: remain in this workflow
  with the specific blocked stage identified and the resumption criteria documented

**Boundary rule:** A blocked or rejected launch must not be resolved by proceeding
anyway. The block must be surfaced and resolved through the governed path.

---

### Stage 11 — Post-Launch State

**Entry event:** Launch-sensitive execution completes within confirmed scope at Stage 7.

**What happens:**
The ecosystem enters the post-launch state. V Forge execution truth now includes the
launched scope. VEDA's observatory role resumes for the launched scope. Project V
retains planning truth.

The post-launch observation phase begins and is governed by
`workflows/post-launch-observation-workflow.md`.

Post-launch findings requiring planning reconsideration route through the governed
return-to-planning path in `workflows/maintenance-and-replanning-workflow.md`.

**Boundary rule:** Post-launch state does not dissolve governance boundaries. The
same ownership model applies after launch as before.

---

## Transition Summary Table

| From | Event | To |
|---|---|---|
| Entry conditions met | — | Stage 1 |
| Stage 1 | Planning readiness confirmed | Stage 2 |
| Stage 1 | Planning basis cannot be confirmed | Stage 10 (blocked) |
| Stage 2 | VEDA evidence current and supportive | Stage 3 |
| Stage 2 | Evidence insufficient, stale, or contradictory | Stage 10 (blocked) |
| Stage 3 | V Forge verification complete; no blocking findings | Stage 4 |
| Stage 3 | Verification cannot complete or findings block | Stage 10 (blocked) |
| Stage 4 | Convergence achieved | Stage 5 |
| Stage 4 | Convergence fails (missing input, contradiction, scope drift) | Stage 10 (blocked) |
| Stage 5 | Request generated; decision pending | Stage 6 |
| Stage 6 | `approved` | Stage 7 |
| Stage 6 | `rejected` | Stage 10 |
| Stage 6 | `escalated` | Stage 8 |
| Stage 6 | `expired` | Stage 9 |
| Stage 7 | Execution complete within scope | Stage 11 |
| Stage 7 | Material condition change; execution halted | Stage 10 (interrupted) |
| Stage 8 | Escalation resolves | Stage 6 |
| Stage 9 | All stages re-confirmed current | Stage 4 |
| Stage 9 | Re-assessment reveals blocking condition | Stage 10 |
| Stage 10 | Planning basis invalid | `maintenance-and-replanning-workflow.md` |
| Stage 10 | New/revised handoff needed | `handoff-workflow.md` |
| Stage 10 | Deferral; resumption criteria documented | Remain in workflow |
| Stage 11 | — | `post-launch-observation-workflow.md` |

---

## Degraded-Mode and Interruption Handling

### Missing readiness input from one system

If a required stage confirmation is absent at Stage 4 — because one system has not
produced its readiness input — convergence cannot be achieved. The workflow blocks
at Stage 4. The specific missing input must be identified. The workflow does not
proceed until that stage's confirmation is provided or the block is resolved
through deferral or replanning.

### Stale VEDA evidence or signal basis

If VEDA evidence used at Stage 2 has become materially stale before authorization
is obtained, Stage 2 must be re-confirmed with current signal before proceeding
to Stage 4. A prior Stage 2 pass does not carry forward indefinitely. The window
depends on the materiality standard for the specific launch — applied conservatively
for launch-sensitive decisions.

### Execution verification not complete

If V Forge cannot complete pre-launch verification at Stage 3 — due to unclear
conditions, unavailable tooling, or unresolved execution findings — the workflow
blocks at Stage 3. V Forge must surface the specific gap. The block must be
resolved before Stage 4.

### Cross-system contradiction at convergence

If Stage 4 assessment reveals that two system readiness inputs contradict each
other — e.g., VEDA signal contradicts the planning basis used at Stage 1, or
V Forge findings contradict Stage 1 launch scope assumptions — convergence fails.
The contradicting systems must reconcile through the governed path before Stage 4
can be re-attempted. This may require returning to the maintenance and replanning
workflow if the contradiction reflects a planning-basis problem.

### Readiness basis changes while authorization is pending

If any of the three readiness inputs change materially while in `awaiting_authorization`
— conditions shift, evidence is contradicted, or execution findings emerge — the
pending authorization is potentially stale. Project V must assess whether the
change is material to the authorized scope. If material: authorization process must
be re-evaluated starting from Stage 9. Do not proceed with the original authorization
on a basis that is no longer current.

### Launch-sensitive execution interrupted mid-launch

If V Forge must halt during Stage 7 due to unexpected conditions, scope excess,
or authorization questions, V Forge must halt at the earliest safe stopping point,
preserve the current execution state, and surface the interruption through governed
reporting. The interruption routes to Stage 10. Failure handling is governed by
`governance/failure-and-recovery-doctrine.md`.

---

## Approval Gate: Seam-Specific Facts

Launch authorization is an approval-sensitive event. This section carries the
seam-specific facts. The shared mechanics pattern is governed by
`governance/approval-mechanics-seam-model.md`.

| Fact | Value |
|---|---|
| Initiating system | Project V |
| Canonical pending state | `awaiting_authorization` |
| Approval class | Class C |
| Stage 4 convergence is a precondition | True — authorization request may not be generated without convergence established |
| Convergence does not equal authorization | True — authorization requires an explicit human approval decision |
| Agent self-authorization | Never permitted |

For the full mechanics — authorization request contents, decision re-entry rules,
escalation path, activity trail obligations — see `governance/approval-mechanics-seam-model.md`
Section C (Launch Authorization).

---

## Activity Trail Requirements

All authorization events in this workflow must produce activity trail records using
the canonical action types from `ecosystem/activity-trail-integration-map.md` Section 5c.

| Workflow event | Action type | Producing system |
|---|---|---|
| Authorization request generated (Stage 5) | `approval.request` | Project V |
| Authorization decision received (Stage 6) | `approval.decide` | Operator / approval surface |
| Authorization escalated (Stage 8) | `approval.escalate` | Project V |

Activity records that are not produced are not governed events.

**Activity trail coverage for launch execution itself:** The current activity-trail
model (`ecosystem/activity-trail-model.md`) covers state-change, agent lifecycle,
and budget/cost events. Launch activation as a discrete event type is covered under
the general state-change and agent-lifecycle action types. Implementations should
log `agent.start`, relevant `content.publish` or equivalent state-change action types,
and `budget.cost_event` records as applicable to the specific launch actions taken.

**Readiness stage completions:** The current canonical action vocabulary does not
include explicit readiness-stage completion action types. Do not invent them. Stages
1–4 are governance workflow stages; their completion is traceable through the Stage 5
authorization request, which carries the `stage4_convergence_ref` reference linking
back to the readiness assessment. If detailed readiness-stage logging is required,
map to appropriate `state_change` action types using the `details` field to capture
stage-specific context.

See `ecosystem/activity-trail-model.md` for base required fields that apply to
every record.

---

## Evidence Currency Principle

Evidence used at Stage 2 must be current enough to support an honest launch
readiness determination. The materiality standard from `governance/evidence-continuity-model.md`
applies, but must be applied conservatively for launch-sensitive decisions — because
the cost of proceeding on stale evidence at launch is higher than in ordinary
planning contexts.

A Stage 2 evidence confirmation has a limited validity window. If authorization
is not obtained before conditions change materially or a significant time window
passes, Stage 2 must be re-confirmed.

---

## Scope Integrity Principle

Launch readiness must be assessed for the actual launch scope, not a simpler version.

If the launch scope has grown beyond what was originally assessed at any stage:
- all stage assessments must cover the full current scope
- prior readiness determinations for a narrower scope do not carry over
- the additional scope requires its own readiness assessment
- Stage 4 convergence and the authorization request must reflect the full current scope

---

## Human-In-The-Loop Principle

Launch authorization is Class C — the highest governance class. Human review and
approval are required. No exception.

An agent may support readiness assessment at Stages 1–4.
An agent must not self-authorize launch-sensitive action.
An operator expressing confidence that a launch is ready is not governed authorization
unless the required approval posture has been satisfied through the governed path.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the launch-readiness workflow has eleven distinct named stages with concrete transitions
- readiness convergence (Stage 4) and authorization (Stages 5–6) are two separate
  required phases — achieving convergence does not authorize launch
- `awaiting_authorization` is the canonical pending state while authorization is unresolved
- no launch-sensitive execution may proceed while in `awaiting_authorization`
- all three system readiness inputs must be current before convergence can be assessed
- a stale readiness basis or changed conditions while authorization is pending require
  re-assessment, not silent continuation
- a rejected, expired, or escalated authorization does not proceed to launch
- activity trail records are required for all authorization events
- no system or agent may self-authorize launch-sensitive action

If the workflow is implemented as "Stage 4 looks complete, so launch can start,"
the doctrine is wrong.

---

## Usage

This document should be used:

- when implementing the launch-readiness workflow states and transitions
- when determining whether readiness convergence has been genuinely achieved
  or only assumed
- when reviewing whether convergence and authorization are being treated as distinct
- when evaluating whether a readiness basis has become stale before authorization
- when routing to adjacent workflows (replanning, new handoff, post-launch observation)
- when auditing whether the activity trail covers required authorization events

---

## Related Docs

- `handoff-workflow.md`
- `maintenance-and-replanning-workflow.md`
- `post-launch-observation-workflow.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/approval-mechanics-seam-model.md`
- `../governance/external-action-governance.md`
- `../governance/testing-and-verification-doctrine.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-evidence-access-contract.md`
- `../ecosystem/activity-trail-model.md`
- `../ecosystem/activity-trail-integration-map.md`
- `../ecosystem/cross-system-boundaries.md`
- `../project-v/project-v.md`
- `../v-forge/v-forge.md`
