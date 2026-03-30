# V Forge Reporting and Approval Model

## Purpose

This document defines how reporting and approval work inside V Forge.

It exists to answer:

```text
What must V Forge report, when must it seek approval, how do reports and approval
requests relate to execution continuity and human oversight, and what makes
V Forge reporting sufficient for governed ecosystem use?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- what V Forge must report and when
- what V Forge must seek approval for and how
- how reporting and approval relate to handoff, execution, launch, and return-to-planning
- what makes a V Forge report sufficient for governance purposes
- the anti-drift rules that prevent V Forge reporting from becoming theater

---

## Out of Scope

This document does not define:

- the full governed report schema (that is in report-structure-and-required-fields.md)
- every project-specific reporting variant
- implementation-specific storage or transport for reports

---

## System

- v-forge

---

## Core Rule

V Forge reporting must describe execution reality, not execution posture.

A report that makes execution look cleaner than it is does not serve governance.
A report that surfaces uncertainty, partial completion, and blocked conditions
enables meaningful human review and correct next-step decisions.

Approval requests must be bounded, specific, and reviewable.
An approval request that buries the real ask in vague language is not a
governed approval request.

---

## When Reporting Is Required

V Forge must produce a governed report when:

### Execution completion
When a bounded execution scope reaches completion — whether full, partial,
or blocked — the outcome must be reported. This includes what was done,
what was not done, and what the current execution state is.

### Approval-sensitive action request
When V Forge execution reaches an action that requires human approval before
proceeding, V Forge must produce a bounded approval request through the
governed reporting path.

### Return-to-planning trigger
When V Forge identifies a finding that warrants planning reconsideration,
the finding must be packaged and reported through the return-to-planning
interface before it becomes a planning input.

### Scope excess detection
When V Forge detects that continuing execution would exceed the approved
handoff scope, the excess must be reported and the action must halt.

### Unexpected external condition
When execution encounters an unexpected external condition that affects
the execution basis, the condition must be reported rather than worked around.

### Governed interruption or failure
When execution halts for any governed reason, that halt and its cause
must be reported through the governed reporting path.

---

## Report Sufficiency Standard

A V Forge report is sufficient when a later reviewer can determine:

- what execution work was performed within the reporting scope
- what was not performed and why
- what the current execution state is
- what uncertainty or partial completion remains
- whether any approval, escalation, or return-to-planning action is needed
- what the approved scope was and whether execution stayed within it

A report is insufficient when it:
- presents partial completion as full completion
- omits uncertainty that affects correctness or next-step decisions
- cannot be reviewed without reconstructing the live session context
- describes a proposed or recommended action as though it already occurred
- hides a blocked condition or scope excess behind confident framing

The minimum report structure is defined in:
`../governance/report-structure-and-required-fields.md`

---

## Approval Request Model

When V Forge requires human approval before proceeding, the approval request must:

- identify the specific action requiring approval
- state why approval is required (which approval class applies)
- describe the scope the approval would cover
- describe what would happen if approval is granted
- describe what the default state is if approval is not granted
- preserve any relevant uncertainty or risk

An approval request must not:
- bury the real action in surrounding prose
- imply that approval is a formality
- widen the scope it is requesting beyond what is actually needed
- present the approved path as the only reasonable path

The approval classes are defined in:
`../governance/approval-and-escalation-model.md`

---

## Approval Classes in V Forge Context

Within V Forge, the approval classes from the ecosystem governance model
apply as follows:

**Class A** — routine bounded interpretation, packaging, and reporting
within approved execution scope. No special approval needed.

**Class B** — mutating execution state in ways that are expected but meaningful,
such as marking a bounded execution scope complete or activating a return-to-planning
transfer. May require operator confirmation depending on scope.

**Class C** — launch-sensitive execution, external paid actions, scope-expanding
execution, and public-facing publication. Requires explicit human approval.

**Class D** — actions that appear to exceed doctrine, depend on ambiguous authority,
or route around normal interfaces. Must escalate, not proceed.

---

## Reporting Relationship to Handoff

At handoff receipt, V Forge must confirm that:
- the handoff package contains the minimum semantic elements required
- the execution scope and constraints are clear enough to begin execution
- no validity conditions are missing that would make the handoff insufficient

If the handoff is insufficient, V Forge must report the insufficiency rather
than proceeding on assumptions. The correct response is governed interruption,
not improvised scope interpretation.

---

## Reporting Relationship to Return-to-Planning

When V Forge returns findings to Project V through the return-to-planning interface,
the return package must preserve:

- what findings triggered the return
- what execution state exists at the time of return
- what V Forge continues to own after the return
- what the return does and does not transfer to Project V

A return-to-planning package is not a dump of all execution state.
It is the bounded set of findings that planning needs to evaluate whether
reconsideration is warranted.

The return-to-planning interface is defined in:
`../interfaces/v-forge-to-project-v-return-to-planning-interface.md`

---

## Reporting Relationship to Launch

Pre-launch verification reporting (Stage 3 of the launch readiness workflow)
must accurately represent execution-side readiness.

The pre-launch verification report must not:
- claim verification passed when conditions are ambiguous
- omit mid-execution findings that affect launch readiness
- understate remaining execution work to move toward launch faster

An inaccurate pre-launch verification report weakens the cross-system
launch readiness confirmation that the human approval in Stage 5 depends on.

---

## Reporting Is Durable, Not Session-Local

Execution reports must be preserved in a way that is recoverable by later
sessions and reviewers — not only by the session that produced them.

A report that exists only in conversational output or ephemeral session context
is not a governed report for continuity purposes.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- reporting must describe reality, including partial completion and uncertainty
- approval requests must be specific, scoped, and reviewable
- a report that makes execution look cleaner than it is fails governance
- reports must be durable, not session-local
- the approval class determines what kind of approval V Forge needs

If a V Forge report consistently presents partial completion as full completion
to avoid triggering review, this doctrine is failing.

---

## Usage

This document should be used:

- when designing what V Forge reports at each execution stage
- when reviewing whether an execution report is sufficient for governance purposes
- when preparing an approval request for a launch-sensitive or scope-expanding action
- when reviewing whether a return-to-planning package preserves the required semantics
- when evaluating whether V Forge reporting is enabling meaningful human review

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `human-in-the-loop-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
- `../governance/failure-and-recovery-doctrine.md`
- `../governance/recommendation-packaging-doctrine.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../workflows/launch-readiness-workflow.md`
- `../workflows/handoff-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`