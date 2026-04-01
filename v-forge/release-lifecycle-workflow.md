# V Forge Release Lifecycle Workflow

## Purpose

This document defines the release lifecycle workflow V Forge uses for owned execution releases and publication-sensitive execution changes.

It exists to answer:

```text
How does V Forge move a release-shaped execution unit from governed admission through preparation, validation, authorization-sensitive release, post-release recording, rollback or failure handling, and bounded return-to-planning without collapsing execution truth into planning truth or treating release capability as self-authorization?
```

This is a Tier 2 V Forge workflow authority document.

---

## Scope

This document governs:

- the lifecycle states V Forge uses for release-shaped execution work
- how release work enters V Forge from governed handoff or equivalent governed execution authorization
- how release preparation, validation, authorization-sensitive release, post-release continuity, and rollback are handled
- how blocked, failed, partial, or changed-condition outcomes are handled for release work
- when release work remains execution-local and when it must return to planning

---

## Out of Scope

This document does not define:

- the detailed MCP wire schemas for release-related tools
- the complete approval matrix for every release surface
- future experimentation or optimization release flows
- future SaaS/runtime/commercial release workflows
- detailed CI/CD implementation mechanics

Those belong in implementation, MCP, governance, or later V Forge docs.

---

## System

- v-forge

---

## Core Rule

Release work in V Forge must move through a bounded governed execution lifecycle.

The release lifecycle exists to ensure that release-shaped execution:
- begins from approved scope
- remains legible as execution truth
- preserves release and publication continuity honestly
- respects stronger discipline for public-facing, launch-sensitive, external, or irreversible actions
- reports blockers, uncertainty, and rollback honestly
- returns to planning when execution can no longer proceed legitimately within scope

V Forge must not treat release capability as release permission.

---

## Workflow Definition

The V Forge release lifecycle workflow is the bounded execution path by which a release work unit moves through:

1. release admission
2. release readiness check
3. release preparation
4. release validation
5. authorization-sensitive release action
6. post-release continuity and verification
7. rollback or failure handling where required
8. execution reporting and bounded findings
9. return-to-planning when required

This workflow defines execution-side release truth.
It does not redefine planning truth or observatory truth.

---

## Release Work Unit Definition

A release work unit is a bounded piece of execution work inside V Forge related to making a built asset, content asset, owned surface change, or bounded release package active on an owned execution surface.

Examples include:
- releasing a plugin or extension build already admitted through approved execution scope
- publishing a bounded owned-surface change that is release-sensitive or launch-sensitive
- performing a versioned release event for a governed execution artifact
- rolling back or correcting a failed release inside approved release authority

A release work unit is not:
- a planning initiative
- a market launch strategy by itself
- a generic idea to ship something soon
- an excuse to widen execution scope

---

## Workflow States

At a minimum, release work units should move through these workflow states:

- admitted
- ready_for_preparation
- preparing
- validation_pending
- ready_for_authorization
- released
- post_release_verification
- rollback_active
- blocked
- failed
- partial
- return_required
- closed

These are workflow-legibility states.
Implementation may use additional sub-states as long as these meanings remain intact.

---

## State 1 — Admitted

A release work unit enters V Forge only after governed handoff or equivalent governed execution authorization.

At admission, V Forge must be able to determine:
- what is being released
- what owned surface or release target is in scope
- whether the release is normal, higher-discipline, or launch-sensitive
- what constraints or release conditions matter
- what should trigger halt, clarification, escalation, rollback, or return-to-planning

Admission is not yet preparation or release.
Admission means the work now sits inside V Forge’s governed release boundary.

---

## Admission Rule

A release work unit must not be admitted from:
- vague operator excitement
- execution-side momentum
- it looks ready enough inference
- raw signal or execution intelligence alone
- adjacent release opportunities discovered during unrelated execution unless separately governed

Release execution begins from approved scope, not from enthusiasm.

---

## State 2 — Ready for Preparation

Before release preparation begins, V Forge must determine whether the admitted release work unit is execution-ready for preparation.

This check asks:
- is the release target explicit enough?
- is the scope of the release bounded?
- are the relevant owned surfaces and dependencies legible?
- are missing details a narrow clarification problem or a planning problem?
- is the current authorization posture potentially sufficient for the release class involved?

A release work unit that is admitted but not ready for preparation must not be forced forward by deadline energy.

---

## Release Readiness Rule

A release work unit is ready for preparation only when V Forge can determine:
- what releaseable asset or surface change is in scope
- what constitutes release completion for the unit
- what validation or checkpoints are required before release action
- what level of authorization or human review may be required
- what should trigger pause, rollback, escalation, or return-to-planning

If those conditions are not met, the correct path is clarification or return, not improvisation.

---

## State 3 — Preparing

The work unit enters active release preparation.

During this state, V Forge may:
- assemble the bounded release package or releaseable asset set
- prepare execution-owned continuity records relevant to the release
- prepare release-local validation steps
- prepare rollback readiness where appropriate
- record preparation progress honestly

During this state, V Forge must not:
- widen the admitted release scope casually
- treat preparation as implicit authorization
- convert a release package into broader planning authority

---

## Release Preparation Rule

Release preparation must remain bounded to the admitted release work unit.

This means:
- in-scope release preparation may proceed
- newly discovered adjacent release opportunities must not be silently absorbed
- preparation convenience must not widen what the release now means
- a preparation discovery that materially changes scope must trigger pause, clarification, escalation, or return

If preparation reveals that the real release is materially larger or riskier than the admitted unit covered, the correct response is not to just finish the release anyway.

---

## State 4 — Validation Pending

Before an actual release action occurs, V Forge must complete the bounded validation required for that release unit.

Validation may include:
- release-local readiness checks
- verification of bounded execution prerequisites
- verification of required execution-owned continuity state
- bounded pre-release checks inside admitted V Forge scope

Validation is not optional theater.
It is the final bounded check that the release can proceed honestly and safely inside execution scope.

---

## Release Validation Rule

Validation must remain:
- bounded to the admitted release work unit
- execution-supporting rather than open-ended research
- honest about uncertainty, missing conditions, and failed checks

Validation must not become:
- a planning redesign session
- a VEDA-style observability takeover
- a generic excuse to keep the release in indefinite limbo without classified outcome

If validation reveals planning-level contradiction or scope illegitimacy, the correct path is report plus return, not silent reinterpretation.

---

## State 5 — Ready for Authorization

After preparation and validation are sufficiently complete, a release work unit enters authorization-sensitive posture.

This state means:
- V Forge believes the release is execution-ready to attempt
- stronger governance may now be required depending on risk, release class, visibility, cost, or irreversibility
- capability and permission must now remain distinct

Ready for authorization is not the same as authorized.
It is a release readiness state, not a release event.

---

## Authorization Rule

Release action must remain subordinate to governance and action class discipline.

This means:
- public-facing, launch-sensitive, external, irreversible, or higher-risk release action may require stronger approval posture
- release capability must not be confused with release permission
- tool availability must not be treated as authorization
- unclear authorization is a halt condition

If the authorization posture is unclear, stale, or mismatched to the actual release scope, V Forge must stop rather than release by convenience.

---

## State 6 — Released

The work unit reaches released state only when the authorized release action has actually occurred and release continuity has been updated.

Released means:
- the release action happened on the relevant owned execution surface
- V Forge preserved the release outcome as execution truth
- the relevant release continuity now reflects what actually occurred

Released does not mean:
- planning is settled forever
- signal ownership transferred to V Forge
- rollback is impossible
- future maintenance or correction is forbidden

---

## Release Continuity Rule

Once released, the work unit must preserve enough continuity that a later reviewer can determine:
- what was released
- where it was released
- when it was released
- under what execution and authorization posture it was released
- whether the release was normal, partial, failed, or later rolled back

Release continuity is execution truth.
It is not planning truth and not observatory truth.

---

## State 7 — Post-Release Verification

After release, V Forge may enter a bounded post-release verification posture.

This state exists to:
- confirm that the release action actually landed as expected
- confirm whether rollback or correction is required inside execution bounds
- preserve honest execution truth about immediate release outcome

Post-release verification remains bounded.
It is not a license for open-ended market monitoring or silent planning change.

---

## Post-Release Verification Rule

Post-release verification must:
- remain tied to the admitted release work unit
- remain bounded to execution-local confirmation
- preserve uncertainty honestly where the immediate outcome is unclear
- trigger rollback, correction, escalation, or return when bounded verification shows release legitimacy or outcome is compromised

If post-release verification reveals a planning-level issue, that issue must return through the governed path.

---

## State 8 — Rollback Active

When bounded execution judgment shows a release must be reversed inside admitted authority, the work unit enters rollback-active state.

Rollback may be appropriate when:
- the release failed materially
- the release produced an execution-local condition that invalidates continuation
- the admitted rollback path is clearly inside current authority and scope

Rollback must not be treated as invisible cleanup.
It is a first-class execution event and must be recorded honestly.

---

## Rollback Rule

Rollback must remain bounded by:
- the actual release work unit
- the current authorization posture
- the explicit rollback authority available for the work unit

If rollback itself would exceed current authority, the correct path is halt plus escalation or return, not unauthorized repair by momentum.

A rollback event must preserve:
- what was rolled back
- why rollback occurred
- what state the release returned to
- what uncertainty remains after rollback

---

## Blocked / Failed / Partial States

Not every release work unit reaches normal release and closure.

### Blocked
Use when the release cannot proceed inside current scope because of missing authorization, missing conditions, failed validation, unresolved dependency, or other bounded blocker.

### Failed
Use when the release was attempted and did not succeed.

### Partial
Use when some release steps completed but the whole release unit did not complete cleanly.

These states must be preserved honestly.
They must not be flattened into cleaner-looking success narratives.

---

## Honesty Rule

V Forge must not smooth release reality into fiction.

This means:
- blocked must remain blocked
- failed must remain failed
- partial must not be reported as fully released
- rollback must not be hidden as if nothing happened
- post-release uncertainty must not be erased for presentation comfort

Execution truth is more valuable than reassuring release theater.

---

## Clarification vs Return Rule

During the release lifecycle, narrow ambiguity may be resolved through clarification when:
- the admitted release work unit remains fundamentally valid
- the clarification does not widen scope
- the clarification does not require planning reconsideration

Return-to-planning is required when:
- the release blocker materially affects what should be done next
- release readiness depends on planning-level reinterpretation
- the admitted release no longer makes sense under current conditions
- authorization-sensitive release can no longer proceed legitimately inside execution bounds

Clarification is not a loophole for silent planning inside V Forge.

---

## Return-to-Planning Triggers

A release work unit must trigger return-to-planning when one or more of the following become true:
- admitted release scope is no longer sufficient or legitimate
- release preparation or validation reveals a planning-level contradiction
- authorization cannot be resolved inside execution-local bounds
- release findings materially affect future planning direction
- rollback, failure, or changed conditions create a planning-relevant next-step problem

Return-to-planning should transfer bounded release findings, not dump all execution ownership upstream.

---

## Release Lifecycle and Execution Intelligence

Execution intelligence may inform release understanding, but it must not silently authorize release or create new release work units.

This means:
- execution intelligence may help interpret release-local conditions
- execution intelligence may help justify a bounded finding or rollback decision inside current authority
- execution intelligence does not itself authorize release expansion, planning mutation, or open-ended release discovery

If execution intelligence reveals a broader opportunity or risk, that is a planning-relevant finding, not self-authorizing release scope.

---

## Governance and Halt Rule

V Forge must halt release work when governance conditions break.

Examples include:
- missing or unclear authorization for a release-sensitive action
- scope ambiguity that would require planning interpretation
- discovery that the release unit exceeds admitted scope
- blocker that cannot be resolved within execution-local bounds
- rollback that itself would exceed current authority

A governed halt is correct behavior.
Continuing by momentum is not.

---

## Cross-System Boundary Rule

The release lifecycle must preserve system ownership.

This means:
- Project V remains the owner of planning truth
- VEDA remains the owner of signal and observability truth
- V Forge remains the owner of execution truth, release continuity, and rollback or failure truth for release work

The workflow must not:
- mutate Project V planning truth directly
- absorb VEDA signal ownership into V Forge release records
- treat release continuity as planning authority

Cross-system inputs may inform the workflow.
They do not collapse ownership.

---

## Human-In-The-Loop Principle

Human review remains especially important when the release lifecycle reaches:
- public-facing or launch-sensitive release action
- ambiguous authorization posture
- high-risk rollback decisions
- major blocked or failed release states
- return-to-planning conditions with material planning consequences

V Forge should make release execution more governable, not less.

---

## LLM Use Principle

A capable LLM should be able to infer from this workflow that:
- release work enters V Forge from approved scope, not freeform ship-it energy
- preparation and validation are bounded execution states, not authorization by momentum
- ready-for-authorization is not the same as authorized
- released means the action actually occurred and continuity was updated
- rollback is a first-class governed execution event, not invisible cleanup
- blocked, failed, and partial states must be preserved honestly
- return-to-planning is required when release execution reveals planning-level issues

If an LLM could use this workflow to justify self-authorized release, hidden rollback, planning mutation, or release-by-convenience, the workflow is failing.

---

## Usage

This document should be used:
- when designing or reviewing V Forge release execution workflows
- when deciding how release work units move through preparation, validation, authorization-sensitive release, verification, and rollback
- when evaluating whether a release blocker should trigger clarification or return-to-planning
- when designing release-related MCP tools or operator flows
- when checking whether V Forge release execution is drifting into planning ownership or self-authorization

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `mcp-surface.md`
- `content-lifecycle-workflow.md`
- `data-boundaries.md`
- `reporting-and-approval-model.md`
- `human-in-the-loop-doctrine.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
