# V Forge Release Execution Playbook

## Purpose

This playbook gives operators and synced LLM sessions a practical operating sequence for release-shaped execution work inside V Forge.

It exists to answer:

```text
How should an operator or LLM execute a bounded release work unit, prepare and validate the release honestly, preserve authorization discipline, handle post-release verification or rollback, and know when the release must stop, clarify, escalate, or return to planning?
```

This is a Tier 2 V Forge operator support document.

---

## Scope

This playbook governs:

- bounded release-shaped execution work already admitted into V Forge scope
- preparation and validation of release work units
- authorization-sensitive release execution
- post-release verification and rollback posture
- stop / clarify / escalate / return decisions during release work

---

## Out of Scope

This playbook does not govern:

- deciding whether a release should exist in the first place
- open-ended launch strategy design
- broad product-planning decisions
- raw observability ownership or post-launch signal ownership
- general-purpose CI/CD implementation detail

Those belong in Project V, VEDA, the release lifecycle workflow, or implementation-specific docs.

---

## System

- v-forge

---

## Core Rule

A release execution playbook starts only after a release work unit is already inside legitimate execution scope.

The goal is not to “ship because we can.”
The goal is to:
- prepare the bounded release honestly
- validate the release honestly
- distinguish capability from authorization
- preserve release continuity and execution truth
- verify the release outcome honestly
- rollback or return when the release no longer remains legitimate inside scope

Release capability is never the same thing as release permission.

---

## When To Use This Playbook

Use this playbook when all of the following are true:
- the work is a release-shaped execution unit already admitted into V Forge
- the release target is bounded enough to describe clearly
- the work includes actual release preparation, authorization-sensitive execution, or post-release handling
- the work is not merely an internal draft or speculative future release idea

Examples:
- release a plugin build already in approved execution scope
- execute a versioned GitHub/release-surface release already admitted into execution
- publish a bounded release-sensitive owned-surface change under current release discipline
- perform a governed rollback after a real release event

---

## Do Not Use This Playbook When

Do not use this playbook when:
- the real question is whether a launch or release should happen at all
- the release target is still strategically undefined
- the work depends on broader planning decisions not yet resolved
- the work is only a content update without release-sensitive posture
- the work is just open-ended “ship something soon” energy

In those cases:
- Project V may need to resolve planning first
- a content lifecycle playbook may be more appropriate
- return-to-planning may be required
- stronger governance review may be needed before any release action exists

---

## Inputs You Should Have Before Starting

Before beginning, you should have:
- project scope clarity
- the admitted execution basis for the release work unit
- a clearly identified release target
- current execution truth for what is being released
- current release/publication continuity state if the target has prior releases
- enough clarity to know whether this is routine, higher-discipline, or launch-sensitive release work

Helpful inputs may include:
- handoff or equivalent execution authorization
- current build/package/version context
- release notes or bounded release intent already inside scope
- rollback posture if it exists
- current blockers or findings relevant to release legitimacy

If those inputs do not exist in usable form, do not bluff the release into existence.
Clarify or stop.

---

## Default Operating Sequence

## Step 1 — Confirm the work is truly a release work unit

Ask:
- is this a real bounded release target?
- is the release already admitted into execution scope?
- is this actual release work, not strategic launch planning disguised as execution?

If any of those are unclear, stop and classify correctly before acting.

### Good signs
- release target is explicit
- execution basis already exists
- release posture is recognized as routine or higher-discipline

### Bad signs
- release target is vague
- the work sounds like “we should launch something” rather than “release this admitted unit”
- planning questions are still unresolved but being ignored

---

## Step 2 — Inspect current execution and release truth

Before changing anything, inspect what V Forge already says is true.

Check:
- current execution state of the release target
- prior release/publication continuity if any
- current blockers, failures, or partial states
- whether a previous rollback or failed release already affects this unit

Do not release from assumption alone.
A surprising amount of release chaos starts when people act from memory instead of current truth.

---

## Step 3 — Restate the bounded release scope

Restate the release in bounded terms.

Examples:
- release build X to GitHub release surface
- publish bounded release Y to owned surface Z
- execute rollback for release unit Q under current authority

The restated scope should make clear:
- what is being released
- where it is being released
- what is explicitly not included
- whether post-release verification and rollback are inside the current work unit

If you cannot restate the release cleanly, you are not ready to proceed.

---

## Step 4 — Confirm whether the release is routine or higher-discipline

Ask whether the release involves:
- public-facing change
- launch-sensitive posture
- irreversible or hard-to-undo consequence
- paid external action
- unusually high visibility or risk

### Routine examples
- ordinary bounded release inside already understood surface posture

### Higher-discipline examples
- public launch-sensitive release
- high-risk external mutation
- release with meaningful rollback consequence or public-facing exposure

If the discipline level is unclear, assume stronger discipline, not weaker.

---

## Step 5 — Prepare the bounded release

Once scope is clear, prepare only the admitted release unit.

During preparation:
- stay inside the stated release boundary
- prepare the release package honestly
- preserve partial preparation truth if interrupted
- avoid absorbing adjacent release ideas into the same unit
- treat new opportunities as findings, not permissions

Preparation is not authorization.
It is only preparation.

---

## Step 6 — Validate the release honestly

Before executing the release action, validate what the current work unit actually needs.

Examples:
- bounded release-local readiness checks
- release target integrity checks
- presence of required execution-owned continuity state
- bounded prerequisites needed for the admitted release action

Validation should tell you whether the release is actually ready to attempt.
It should not become a vague waiting room with no classified outcome.

If validation fails, preserve that honestly.
Do not slide into release-by-momentum.

---

## Step 7 — Confirm authorization posture before release action

Ask:
- does the current authorization posture actually cover this release action?
- is the release more sensitive than originally assumed?
- would someone auditing this later agree that the release was legitimately authorized?

If authorization is unclear, stale, or mismatched to the real release scope:
- stop
- clarify
- escalate
- or return, depending on what the boundary problem really is

Do not treat tool availability as approval.
Do not treat preparedness as approval.
Do not treat confidence as approval.

---

## Step 8 — Execute the release action only if posture is clear

Once preparation, validation, and authorization posture are all sound, execute the bounded release action.

During release execution:
- remain inside the admitted release target
- preserve truthful state if interruption occurs
- avoid piggybacking unrelated release work onto the same action
- record the actual release event, not the hoped-for one

Release execution should feel disciplined and explicit, not magical.

---

## Step 9 — Update release continuity immediately after real action

Once the release action actually occurs, update release continuity honestly.

Record at minimum:
- what was released
- where it was released
- when it was released
- what the resulting execution state is
- whether the outcome is normal, partial, blocked, failed, or rollback-prone

If release continuity was not updated, the work is not operationally whole.

---

## Step 10 — Perform bounded post-release verification

After release, perform bounded verification of immediate release outcome.

Examples:
- confirm the release landed where intended
- confirm the release state matches what actually happened
- confirm whether bounded rollback or correction is needed

Post-release verification remains execution-local.
It is not a license to absorb observability ownership or rewrite planning.

If verification reveals a serious issue, classify it honestly.
Do not massage it into a prettier story.

---

## Step 11 — Roll back only if the rollback path is truly legitimate

Rollback may be correct when:
- the release failed materially
- the release produced an execution-local condition that invalidates continuation
- rollback is inside current admitted authority

Before rollback, ask:
- is rollback actually in-bounds here?
- would rollback itself exceed current authority?
- does rollback solve an execution-local problem, or are we now in planning territory?

If rollback is not clearly in-bounds, stop and escalate or return.
Do not do unauthorized cleanup theater.

---

## Step 12 — Classify the outcome honestly

At the end of the work, classify the result truthfully.

Possible outcomes:
- completed
- partial
- blocked
- failed
- rollback_active
- return_required

### Use completed when
- the release action occurred legitimately
- release continuity is aligned
- post-release verification does not leave unresolved boundary-breaking issues

### Use partial when
- some release steps completed
- but the release unit did not complete cleanly

### Use blocked when
- the release could not continue inside current execution bounds because of real blocker or missing authorization/condition

### Use failed when
- the release was attempted and did not succeed

### Use rollback_active when
- the rollback path is legitimately active and now part of the truth of this work unit

### Use return_required when
- the release revealed a planning-level contradiction, scope issue, or authorization problem V Forge should not resolve alone

Do not classify for optics.
Classify for truth.

---

## Step 13 — Record findings if they matter

If the release surfaced meaningful findings, record them.

Examples:
- release scope was less stable than assumed
- rollback assumptions were weaker than expected
- publication constraints were tighter than assumed
- release outcome exposed a planning-level contradiction

A finding is bounded execution truth.
It is not a stealth strategy override.

---

## Step 14 — Return to planning if needed

Return-to-planning is required when release execution crosses out of legitimate execution handling.

Common triggers:
- the release no longer makes sense under current planning conditions
- the admitted release scope is too narrow for the real work needed
- the release revealed a planning contradiction
- authorization cannot be resolved inside execution-local bounds
- rollback/failure creates a planning-relevant next-step problem

When returning:
- preserve what actually happened
- preserve what remains blocked or uncertain
- package bounded findings
- do not dump all execution ownership upstream

Return is a correct governed outcome, not embarrassment.

---

## Fast Checks During the Work

Use these quick questions during release execution.

### Check 1
**Am I still executing the admitted release, or am I quietly expanding the launch scope?**

### Check 2
**Did validation actually succeed, or am I substituting momentum for readiness?**

### Check 3
**Is authorization truly clear, or am I treating capability as permission?**

### Check 4
**If audited later, would this look like disciplined release execution or reckless ship-it behavior?**

If the answers start drifting, stop.

---

## Stop Immediately Conditions

Stop and do not continue casually when:
- the release target is no longer clearly bounded
- the admitted scope is unclear or missing
- the real release now depends on broader unresolved planning decisions
- authorization posture is unclear, stale, or visibly weaker than the release actually needs
- rollback itself would exceed current authority
- the work is turning into “while we’re here, let’s also push these adjacent changes”
- post-release issues are being smoothed over for optics

That is the point for:
- clarification
- halt
- escalation
- bounded finding
- return-to-planning

Not momentum.

---

## Good Use of This Playbook Looks Like

Good use looks like:
- clear release target
- inspection before action
- honest preparation and validation
- clear authorization discipline
- explicit release execution
- immediate release continuity update
- bounded post-release verification
- rollback only when truly in-bounds
- honest final state classification
- clean return-to-planning when boundaries are crossed

Bad use looks like:
- ship-it energy replacing real readiness
- preparedness treated as authorization
- public-facing release by convenience
- hidden rollback or hidden partial failure
- using release execution to smuggle broader planning or scope expansion

---

## LLM Sync Reminder

A synced LLM using this playbook should remember:
- this is for already-admitted release work units
- preparation is not authorization
- validation is not authorization
- release capability is not release permission
- release continuity must be updated after real release action
- rollback is a first-class governed execution event
- return-to-planning is correct when release handling becomes a planning problem

If the LLM starts sounding like an autonomous deploy engine or launch strategist, it is out of bounds.

---

## Usage

This playbook should be used:
- by operators executing bounded release work in V Forge
- by synced LLM sessions handling release-sensitive execution
- when deciding whether release work stays local, escalates, rolls back, or returns to planning
- as the practical operator layer for disciplined release execution in V Forge

---

## Related Docs

- `../v-forge.md`
- `../operator-quickstart.md`
- `../release-lifecycle-workflow.md`
- `../content-lifecycle-workflow.md`
- `../mcp-surface.md`
- `../reporting-and-approval-model.md`
- `../../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../../governance/approval-and-escalation-model.md`
- `../../governance/external-action-governance.md`
