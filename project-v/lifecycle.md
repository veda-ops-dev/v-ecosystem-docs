# Project V Lifecycle

## Purpose

This document defines the lifecycle of a project as understood and governed by Project V.

It exists to answer:

```text
What is the full arc of a project inside Project V, how does a project move from recognition through planning, readiness, handoff, return-aware replanning, and closure, and what lifecycle rules prevent Project V from losing continuity or boundary discipline over time?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- the lifecycle stages of a project inside Project V
- what lifecycle transitions Project V may recognize
- how lifecycle state relates to planning, readiness, handoff, return, and closure
- how lifecycle continuity must be preserved over time
- what lifecycle drift is forbidden even if it seems operationally convenient

---

## Out of Scope

This document does not define:

- detailed workflow mechanics for every lifecycle transition
- the detailed intake workflow for the whole ecosystem
- the detailed handoff payload contract
- the detailed return-to-planning payload contract
- implementation-specific status fields or storage schemas

Those belong in more specific workflow, interface, implementation, or Project V docs.

---

## System

- project-v

---

## Core Rule

A Project V project must move through explicit lifecycle states.

A project lifecycle state must not be inferred casually, reset silently, or collapsed into vague “active/inactive” shorthand that hides planning truth.

Lifecycle change is governance-relevant.
Project V must preserve enough lifecycle structure that a later reader or capable LLM can determine where a project is, how it got there, and what kinds of transitions remain legitimate.

---

## Lifecycle Definition

The Project V lifecycle is the governed arc by which a project is:

- recognized
- admitted or rejected
- structured
- advanced through planning
- evaluated for readiness
- handed off when appropriate
- reconsidered when return-triggered replanning occurs
- closed, archived, or intentionally reactivated through a governed path

The lifecycle exists so that Project V does not treat projects as timeless containers of work with no stage discipline.

---

## Lifecycle Principle

A project lifecycle state must describe durable project posture, not just the current operational moment.

Operational workflow state and lifecycle state are related but not identical.

This means:

- operational workflow states describe what Project V is currently doing
- lifecycle states describe where the project stands in its longer planning arc

A project may be in active planning workflow while still being, for example, deferred, handed off, or under reconsideration as a lifecycle matter.
Project V must not collapse lifecycle and workflow into one flat state model.

---

## Lifecycle Stages

At the baseline level, the lifecycle of a project inside Project V should be understood through the following stages.

### 1. Recognized
A potential project has been identified or received as planning-relevant input, but Project V has not yet established it as an admitted active project.

### 2. Admitted
Project V has established that the project belongs in governed planning scope and should exist as a project within Project V.

### 3. Structuring
Project V is shaping the project’s planning truth, scope, decomposition, and governing planning context.

### 4. Active Planning
The project is actively being planned, refined, evaluated, or governed within Project V.

### 5. Deferred
The project remains part of Project V truth, but active advancement is intentionally paused.
The project is neither forgotten nor closed.

### 6. Blocked
The project cannot currently advance through legitimate planning progression because of dependencies, governance posture, missing inputs, or other material blockers.

### 7. Ready for Handoff
Project V has determined that the project, or a bounded portion of it, is planning-ready for governed handoff toward execution.
Readiness does not itself mean execution responsibility has transferred.

### 8. Handed Off
A governed handoff has occurred for the relevant execution scope.
Project V retains planning truth for the project but no longer owns execution truth for the handed-off scope.

### 9. Return Under Reconsideration
Governed return-to-planning input has caused the project to re-enter planning reconsideration.
The project is no longer simply proceeding on its prior path unchanged.

### 10. Closed
Project V has determined that the project lifecycle is complete, intentionally ended, or no longer active as a planning concern.
Closure must remain reviewable and must not silently erase continuity.

### 11. Archived
The project is no longer active in current planning use and has moved into preserved historical state.
Archive is not active planning truth, but the project’s history remains durable and referenceable.

### Rule
These stages may later be implemented through more detailed status structures, but the lifecycle logic must preserve their semantic distinction.
Project V must not reduce them to a single ambiguous “status” field with no governed meaning.

---

## Recognition Rule

A project begins in lifecycle terms when Project V recognizes that planning-relevant input may justify project existence.

Recognition does not yet mean:

- project admission
- planning commitment
- readiness
- approval
- handoff eligibility

Recognition is the governed acknowledgement that potential project formation is now in view.

---

## Admission and Rejection Rule

Project V must explicitly determine whether a recognized potential project becomes an admitted project, remains under review, is deferred before admission, or is rejected.

Project admission must not be inferred from mere discussion, operator enthusiasm, or repeated mention.

A project that remains in Recognized state without an admission or rejection determination within a reasonable planning horizon must not be silently carried forward as though its status is undecided by default.
Project V must explicitly determine the disposition: admit, defer before admission, hold for more evidence, or reject, rather than allowing unresolved recognition to accumulate as invisible planning debt.

Where rejection occurs, rejection continuity must be preserved when future reconsideration depends on it.
Rejected projects must not be rediscovered later as though no prior determination existed.

---

## Structuring Rule

Once admitted, a project enters lifecycle structuring until Project V has established enough planning truth to govern it meaningfully.

Structuring may include:

- defining project boundaries
- defining project decomposition
- relating the project to prior decisions
- identifying planning-relevant dependencies
- identifying whether the project is stand-alone or tied to portfolio-level context

A project exits Structuring and enters Active Planning when Project V has established enough planning truth to govern the project meaningfully, meaning scope is defined, governing decisions are recorded, and planning can proceed without requiring fundamental re-scoping.
The transition from Structuring to Active Planning must be explicit, not assumed from elapsed time or apparent progress.

A project that has been admitted but not structured enough to govern meaningfully must not be treated as a fully mature active project.

---

## Active Planning Rule

A project is in Active Planning when Project V is legitimately advancing its planning truth.

This may include:

- refining structure
- evaluating readiness
- processing planning-relevant signal
- preparing recommendations
- preserving continuity
- coordinating approval-sensitive planning transitions

Active Planning does not mean every project is moving at the same speed.
It means the project remains inside live governed planning use.

---

## Deferred and Blocked Rule

Deferred and Blocked are distinct lifecycle conditions.

### Deferred
Deferred means Project V is intentionally pausing advancement while preserving project legitimacy and continuity.
The project is still real and still belongs in Project V.

### Blocked
Blocked means Project V cannot legitimately advance the project under current conditions.
The blockage may come from:

- governance posture
- missing dependencies
- missing signal or evidence
- approval constraints
- cross-project conflicts
- unresolved planning uncertainty

Deferred and Blocked must not be treated as equivalent.
A deliberate pause is not the same as inability to proceed.

---

## Readiness Rule

A project enters Ready for Handoff only when Project V has established that the relevant execution scope is planning-ready for governed handoff.

Ready for Handoff means:

- Project V has completed the planning-side basis required for bounded execution transfer
- readiness has been explicitly determined
- handoff may now be prepared or activated through the governed path

Ready for Handoff does not mean:

- execution has started
- approval is complete
- handoff is already active
- Project V has stopped owning planning truth

Readiness is a lifecycle state, not an execution event.

---

## Handoff Rule

A project enters Handed Off only when the governed handoff transition has actually occurred for the relevant scope.

At that point:

- execution responsibility has transferred for the handed-off scope
- Project V retains planning truth
- Project V does not retain execution ownership for that scope

A project may remain overall in a broader planning lifecycle even while a bounded scope has been handed off.
Lifecycle handling must preserve that scope-sensitive reality rather than flattening it.

Where a project has multiple bounded scopes at meaningfully different lifecycle stages simultaneously, Project V must preserve lifecycle truth per scope where that divergence is material, rather than flattening to a single project-level label.
A project-level lifecycle stage should reflect the dominant or overall planning posture; where scope-level lifecycle diverges significantly, that divergence must be explicitly preserved rather than flattened into one label.

---

## Return Under Reconsideration Rule

A project enters Return Under Reconsideration when governed return-to-planning input causes the prior path to require real planning review.

This means:

- return input has been recognized through the governed return path
- Project V is no longer simply treating the prior plan as unchanged
- planning continuity must now be reassessed in light of the return trigger

Return Under Reconsideration is not the same as ordinary Active Planning.
It is a specific lifecycle condition marking that prior planning state is under governed reconsideration.

Return Under Reconsideration resolves when Project V has completed governed replanning reconsideration and explicitly determined the project’s next lifecycle state.
The project may transition to Active Planning if planning continues, Ready for Handoff if replanning confirms readiness, Blocked or Deferred if reconsideration reveals a constraint, or Closed if reconsideration determines the project should end.
Return Under Reconsideration must not be silently collapsed back into Active Planning by momentum.
The transition must be explicit.

---

## Closure Rule

A project may enter Closed when Project V has determined that:

- the project has completed its intended planning-relevant arc
- the project should be intentionally ended
- the project no longer belongs in active planning use
- further activity would require explicit reactivation rather than casual continuation

Closure must be:

- explicit
- reviewable
- continuity-preserving
- non-destructive to prior history

A silent disappearance of a project is not valid closure.

---

## Archive Rule

A project enters Archived when it is no longer active in current planning use but its history remains relevant for reference, audit, continuity, or future reinterpretation.

Archive is not a synonym for deletion.
Archive is not a synonym for active planning.

Archived projects must remain distinguishable from:

- active projects
- merely deferred projects
- recently closed projects that still require review follow-through

Archived project history remains referenceable as decision context for active planning, including rejection continuity, prior scope precedent, or historical evidence, even though the project is not an active planning object.

Archived state exists to preserve history without pretending old projects are still live planning objects.

---

## Reactivation Rule

A Closed or Archived project must not silently resume as though it had remained active all along.

If a project is reactivated:

- reactivation must be explicit
- the prior lifecycle state must remain visible
- the reason for reactivation must be reviewable
- Project V must determine whether the project is resuming prior planning, entering return-like reconsideration, or being treated as materially new planning work

Reactivation is a governed lifecycle event, not a casual continuation.

---

## Lifecycle Continuity Rule

Project V must preserve lifecycle continuity across the full project arc.

This means:

- recognition history must not disappear when admission occurs
- rejection, deferment, blocking, and closure must remain interpretable where future planning depends on them
- handoff does not erase planning-side continuity
- return-triggered reconsideration must preserve the relationship to prior lifecycle state
- archive does not erase history

A project lifecycle must be traceable, not merely current-state visible.

---

## Lifecycle and Workflow Relationship Rule

Lifecycle state and operational workflow state must remain distinguishable but compatible.

Examples:

- a Deferred project may still enter bounded workflow activity for reconsideration
- a Handed Off project may later enter Return Under Reconsideration
- a Blocked project may still be under active review without becoming Ready for Handoff
- a Closed project must not appear as though it is simply waiting in normal workflow

Project V must not force lifecycle truth into operational workflow shorthand.

---

## Multi-Project Lifecycle Rule

Where Project V manages multiple projects, each project must preserve its own lifecycle truth.

This means:

- portfolio visibility must not flatten lifecycle distinctions across projects
- one project becoming Ready for Handoff does not imply others do
- one project being Blocked or Deferred must not rewrite other projects’ lifecycle states
- cross-project orchestration must remain compatible with project-local lifecycle truth

Portfolio-level reasoning must not erase project-local lifecycle discipline.

---

## Governance and Approval Rule

Lifecycle state does not replace governance posture.

This means:

- project admission is not automatic approval for all future action
- Ready for Handoff is not automatic handoff activation
- Handed Off does not mean execution-side changes may be absorbed without governed return
- Closure is not permission to erase reviewability
- Reactivation is not permission to ignore prior decisions, approvals, or continuity

Lifecycle management must remain compatible with the governance spine, not act as a shortcut around it.

---

## Failure and Drift Rule

If lifecycle handling becomes vague, silent, or convenience-driven, Project V has drifted.

Common lifecycle drift failures include:

- projects appearing without explicit admission
- projects disappearing without explicit closure or archive
- deferred and blocked being treated as the same thing
- handed-off scope being treated as if Project V still owns execution truth
- return-triggered reconsideration being flattened into ordinary activity
- archived projects being resumed without explicit reactivation

Lifecycle convenience is not lifecycle governance.

---

## Reviewability Rule

Project lifecycle handling inside Project V must remain reviewable enough that a later reader can determine:

- how the project entered existence
- what lifecycle stage it is in now
- what prior lifecycle stages matter
- what major lifecycle transitions occurred
- what transition is legitimate next

If lifecycle state cannot be reconstructed after the fact, the lifecycle model is too weak.

---

## Human-In-The-Loop Principle

Human review remains especially important when Project V changes lifecycle state through:

- admission
- rejection
- major deferment or blocking decisions
- readiness determination
- handoff activation
- closure
- reactivation
- return-triggered reconsideration that changes prior planning posture

Project V should make lifecycle changes more governed and more interpretable, not more invisible.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- project lifecycle is not the same as momentary workflow state
- a project moves through explicit stages rather than vague activity labels
- readiness, handoff, closure, archive, and reactivation are distinct lifecycle events
- handoff does not erase planning truth
- return-triggered reconsideration is a special lifecycle condition, not a casual planning continuation
- projects must not silently appear, disappear, or resume

If an LLM could treat Project V projects as timeless containers that are either “active” or “not active,” this lifecycle doctrine is failing.

---

## Usage

This document should be used:

- as the lifecycle authority doc for Project V projects
- when reviewing whether project-state handling preserves continuity and planning truth
- when writing more detailed Project V project-state or workflow docs
- when checking whether lifecycle convenience is eroding Project V role discipline
- when aligning future Project V docs to a common project-arc model

---

## Related Docs

- `project-v.md`
- `system-invariants.md`
- `operational-workflow.md`
- `multi-project-doctrine.md`
- `byda-in-project-v.md` *(planned)*
- `v-forge-integration.md`
- `../workflows/project-intake-workflow.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/failure-and-recovery-doctrine.md`
