# Project V and V Forge Integration Doctrine

## Purpose

This document defines how Project V governs its relationship with V Forge inside the V Ecosystem.

It exists to answer:

```text
How does Project V prepare work for V Forge, what does Project V remain responsible for after handoff, what must Project V not do once execution responsibility has transferred, and how should Project V handle return-to-planning inputs from V Forge without re-absorbing execution ownership?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- how Project V relates to V Forge as its execution-side counterpart
- what Project V owns before handoff, during handoff preparation, and after handoff
- what Project V must not do after execution responsibility transfers
- how Project V should interpret and handle returned findings or return-triggering inputs from V Forge
- how boundary discipline between planning truth and execution truth must remain intact

---

## Out of Scope

This document does not define:

- the detailed handoff payload structure
- the detailed return-to-planning payload structure
- V Forge internal execution doctrine
- implementation-specific transport or queueing mechanisms
- detailed approval mechanics beyond the shared governance model

Those belong in interface docs, governance docs, V Forge docs, or implementation docs.

---

## System

- project-v

---

## Core Rule

Project V governs planning truth and handoff readiness.
V Forge governs execution truth after governed handoff.

Project V must not continue acting as though it still owns execution once execution responsibility has transferred.
V Forge outputs may change planning posture only through governed return-to-planning handling, not by silent re-absorption of execution-side state.

---

## Integration Definition

Project V and V Forge integration is the governed boundary relationship by which:

- Project V prepares bounded execution-ready planning output
- execution responsibility transfers through governed handoff
- V Forge executes within the handed-off scope
- execution findings or changed conditions may later return to Project V through the governed return path

This integration exists so planning and execution remain tightly coordinated without becoming one blurred system.

---

## Integration Principle

Project V and V Forge must cooperate without collapsing ownership.

This means:

- Project V may prepare, sequence, and evaluate execution-directed work
- V Forge may execute, observe, and return findings
- neither system may silently absorb the other system’s truth domain

Fast coordination is allowed.
Boundary collapse is not.

---

## Pre-Handoff Rule

Before handoff, Project V owns:

- planning truth
- readiness evaluation
- bounded execution scope definition
- planning-side dependency interpretation
- the decision to prepare work for handoff
- the planning-side basis for why handoff is justified

Before handoff, V Forge does not own the execution work as active execution responsibility.
Visibility into a possible future handoff does not itself transfer ownership.

---

## Handoff Readiness Rule

Project V must determine handoff readiness before execution responsibility can transfer.

This means Project V must establish, at the level required for the handed-off scope:

- what work is in scope
- what is out of scope
- what dependencies materially affect execution legitimacy
- what planning decisions justify execution transfer
- what approval posture still applies
- whether execution should proceed now, wait, or remain withheld

A handoff package that is merely detailed is not necessarily handoff-ready.
Readiness is a governed planning determination, not a formatting achievement.

---

## Handoff Transfer Rule

Execution responsibility transfers only through the governed Project V to V Forge handoff path.

Once handoff has occurred for a bounded scope:

- V Forge owns execution truth for that scope
- Project V retains planning truth
- Project V must not mutate execution truth as though handoff had not happened
- Project V must not continue issuing execution-direction changes outside the governed path

A prepared handoff is not a transferred handoff.
A desired handoff is not a transferred handoff.

---

## Post-Handoff Boundary Rule

After handoff, Project V must remain on the planning side of the boundary.

This means Project V may:

- preserve planning continuity
- track that handoff occurred
- maintain planning-side lifecycle and readiness context
- await governed return-to-planning inputs where needed
- perform governance-compatible review of planning consequences

Project V must not:

- treat execution progress as if it were still planning state
- rewrite execution truth directly
- act as the canonical execution ledger
- absorb execution findings as automatic planning mutation

Post-handoff visibility is not post-handoff ownership.

---

## Execution Non-Interference Rule

Project V must not interfere with active V Forge execution by issuing planning-side reinterpretation as though it were direct execution control.

If Project V needs execution to pause, change, or stop after handoff, that must occur through the governed path appropriate to the current approval, authority, and workflow posture.

Project V must not use planning ownership as a pretext for ungoverned execution override.

---

## Returned Findings Rule

When V Forge returns findings, those findings are execution-side outputs.

Project V must treat them as:

- bounded returned findings
- return-triggering planning input where applicable
- possible causes of reconsideration, revision, escalation, deferment, or no-action

Project V must not treat returned findings as:

- automatic planning truth mutation
- automatic decision supersedence
- automatic approval replacement
- proof that execution ownership has reverted by default

Returned findings may influence planning.
They do not self-apply planning changes.

---

## Return-to-Planning Rule

When V Forge outputs trigger return-to-planning, Project V must re-enter planning through the governed return path.
The governed return path is defined in `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`.
Project V's handling of return-to-planning inputs must follow that interface's minimum semantic requirements.

This means Project V must:

- classify the returned content
- determine what part of prior planning remains valid
- determine whether planning should be reaffirmed, revised, superseded, invalidated, deferred, blocked, or escalated
- preserve continuity between the pre-handoff planning state and the reconsidered state

Return-to-planning is not silent execution-state ingestion.
It is a governed re-entry event.

---

## Scope Integrity Rule

Project V must preserve scope integrity across the integration boundary.

This means:

- Project V must not widen execution scope after handoff by implication
- V Forge findings about one bounded scope must not automatically rewrite unrelated planning scope
- returned findings must be mapped to the planning scopes they actually affect
- one bounded handoff must not become open-ended execution authority

Integration quality depends on scope discipline, not just system cooperation.

---

## Approval and Authority Rule

Project V and V Forge integration must remain compatible with the shared approval and actor-authority model.

This means:

- handoff readiness does not eliminate approval requirements
- Project V recommendations do not self-authorize V Forge execution
- V Forge execution-side outputs do not self-authorize planning changes in Project V
- actor authority remains relevant on both sides of the boundary

Where V Forge requires additional planning-side approval or scope clarification during execution, without full return-to-planning being required, that coordination must still occur through the governed interface path, not through informal side-channel communication.
Project V's response to such coordination must be limited to the approval or clarification requested and must not be used as an opportunity to reclaim execution oversight.
Approval coordination is not execution re-ownership.

Project V must not treat integration speed as a reason to blur approval or actor-legitimacy rules.

---

## Handoff Recall and Reconsideration Rule

If a handoff requires reconsideration after preparation or after transfer, Project V must not silently collapse the handoff state.

This means:

- pre-transfer reconsideration must return to the correct planning or approval state explicitly
- post-transfer reconsideration must follow a governed path compatible with current authority, approval, and workflow posture
- Project V must not behave as though the handoff never existed simply because planning now wishes to change direction

Post-transfer reconsideration must be initiated through a governed recall mechanism, either through an operator-directed instruction that reverses the handoff with the required approval posture, or through a V Forge return-to-planning input where V Forge has not yet acted on the handoff.
In both cases, the recall must produce an explicit governed event, not a silent state collapse.
The Handed-Off lifecycle state must not be overwritten without a traceable governing reason.

A changed planning preference is not enough to erase handoff history.

---

## Failure Boundary Rule

When execution-side failure, ambiguity, or unexpected outcome occurs, Project V must not use that fact as permission to re-absorb execution ownership.

Instead, Project V must:

- preserve the planning implications of the failure
- accept governed returned findings or return-triggering inputs
- re-evaluate planning through the governed return path
- escalate where the planning consequence cannot be determined safely

Failure does not collapse the boundary.

---

## Reviewability Rule

Project V’s side of the V Forge integration must remain reviewable enough that a later reader can determine:

- what planning basis justified handoff
- what scope was handed off
- what remained planning-side after handoff
- what findings or return inputs came back
- how Project V interpreted those returned inputs
- what planning state changed as a result, if any

If this cannot be reconstructed, the integration doctrine is being used weakly.

---

## Forbidden Integration Drift Patterns

Project V has drifted in its relationship to V Forge if it begins to:

- treat prepared handoff as active execution transfer
- act as though it still owns execution truth after handoff
- act as a shadow execution owner by monitoring, directing, or reinterpreting execution work post-handoff as though planning authority extends to execution authority
- absorb returned findings as direct planning mutation
- use planning urgency to override execution boundary discipline
- widen handed-off scope after the fact by implication
- treat execution failure as permission to collapse ownership back into planning
- rewrite handoff history because later planning changed direction

These are integration failures, not coordination wins.

---

## Human-In-The-Loop Principle

Human review remains especially important where Project V and V Forge integration affects:

- handoff activation
- post-handoff reconsideration
- return-triggered planning revision
- approval-sensitive execution changes
- ambiguous execution findings with planning consequences
- integration-boundary disputes

Project V should make the planning-execution boundary more governable, not more theatrical.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- Project V owns planning truth before and after handoff
- V Forge owns execution truth after governed handoff
- returned findings are not self-applying planning mutations
- return-to-planning is a governed re-entry path
- handoff history and execution boundary discipline must remain visible even when planning changes later
- failure does not collapse planning and execution into one system

If an LLM could use Project V as a post-handoff execution controller or treat V Forge findings as direct planning truth, this integration doctrine is failing.

---

## Usage

This document should be used:

- when evaluating whether Project V is interacting with V Forge correctly
- when reviewing handoff readiness from the Project V side
- when checking whether post-handoff behavior is boundary-safe
- when interpreting returned findings or return-triggering inputs from V Forge
- when writing more detailed integration or handoff-adjacent docs

---

## Related Docs

- `project-v.md`
- `system-invariants.md`
- `operational-workflow.md`
- `lifecycle.md`
- `multi-project-doctrine.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/auth-and-actor-model.md`
- `../governance/failure-and-recovery-doctrine.md`
