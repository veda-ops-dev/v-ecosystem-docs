# Project V Multi-Project Doctrine

## Purpose

This document defines how Project V governs planning and orchestration across more than one project at a time.

It exists to answer:

```text
How does Project V reason across multiple projects without collapsing project boundaries, lifecycle truth, approval posture, or planning discipline into portfolio-level mush?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- how Project V handles multi-project planning and orchestration
- what Project V may and may not do when reasoning across multiple projects
- how cross-project prioritization, dependency handling, and conflict handling must remain bounded
- how project-local truth must be preserved inside portfolio-level visibility
- what multi-project drift patterns are forbidden even if they seem strategically efficient

---

## Out of Scope

This document does not define:

- detailed scoring formulas for portfolio prioritization
- detailed strategy or objective-function doctrine
- implementation-specific portfolio dashboards
- every workflow-specific rule for cross-project coordination
- detailed resource-allocation algorithms

Those belong in strategy docs, workflow docs, implementation docs, or more specific Project V docs.

---

## System

- project-v

---

## Core Rule

Project V may reason across projects, but it must not govern across projects in a way that erases project-local truth.

Portfolio visibility is real.
Portfolio-level planning is real.
But portfolio-level reasoning must not collapse:

- project identity
- project lifecycle truth
- project readiness truth
- project approval posture
- project-specific decision continuity

If cross-project planning makes Project V behave like one big undifferentiated work bucket, the doctrine is failing.

---

## Doctrine Definition

The Project V multi-project doctrine is the set of rules that governs how Project V:

- sees across multiple projects
- compares and prioritizes projects
- handles cross-project dependencies and conflicts
- coordinates planning without collapsing project-local governance

This doctrine exists so that Project V can be portfolio-capable without becoming boundary-free.

---

## Multi-Project Principle

Project V must preserve two truths at once:

- the ecosystem may require cross-project planning, sequencing, and prioritization
- each project still has its own bounded planning truth, lifecycle state, readiness state, approval posture, and decision continuity

A correct Project V can see across projects without flattening them.

---

## Project-Local Truth Rule

Every project inside Project V must preserve its own project-local truth even when viewed inside a wider portfolio context.

This includes:

- project identity
- project scope
- project lifecycle state
- project readiness posture
- project-specific decisions
- project-specific blockers
- project-specific approval posture

Cross-project reasoning must not overwrite those truths by implication.

---

## Portfolio Visibility Rule

Project V may maintain portfolio-level visibility across projects.

Portfolio visibility may include:

- comparative priority view
- shared dependency view
- readiness comparison
- blocked-state comparison
- sequencing awareness
- cross-project conflict detection

Portfolio visibility is allowed because it improves planning quality.
But visibility is not permission to mutate projects casually.
Portfolio visibility must not be used as a substitute for explicit prioritization decisions.
Comparative rankings, readiness comparisons, or dependency views do not themselves constitute prioritization decisions or readiness determinations.
An LLM or operator viewing portfolio state must not infer project priority, readiness, or urgency from comparative position alone.
Those determinations require explicit governed evaluation.

---

## Cross-Project Prioritization Rule

Project V may prioritize across projects when doing so is part of governed planning.

Cross-project prioritization must remain explicit and reviewable.
It must not:

- silently rewrite project-local readiness
- silently rewrite project-local decisions
- silently override project-local approval requirements
- convert strategic preference into immediate execution authority

Cross-project prioritization decisions require the same actor authority and approval posture as other significant planning decisions.
Actor authority is defined in `../governance/auth-and-actor-model.md`.

A project being lower priority does not automatically mean it is blocked, rejected, or closed.
A project being higher priority does not automatically mean it is approved, ready, or entitled to bypass normal gates.

---

## Cross-Project Dependency Rule

When one project depends materially on another project, Project V must preserve that dependency explicitly.

This means:

- dependent projects must remain distinguishable
- the dependency must not be treated as project merger by convenience
- one project’s unresolved dependency must not silently rewrite the lifecycle truth of another project
- dependency handling must remain reviewable and continuity-supporting

A cross-project dependency is a relationship, not a license to collapse project boundaries.

---

## Cross-Project Conflict Rule

When two or more projects have materially conflicting planning states, Project V must surface that conflict explicitly rather than resolving it by momentum, recency, or operator convenience.

Examples include:

- conflicting readiness determinations
- conflicting handoff eligibility
- conflicting resource claims
- conflicting dependency assumptions
- conflicting timing assumptions
- conflicting approval-sensitive sequencing

Cross-project conflict resolution requires the same governed decision and approval posture as other planning-significant decisions.
A cross-project conflict must not be resolved informally simply because the preferred answer appears obvious.

---

## Shared Resource Rule

When projects compete for shared bounded resources, Project V must preserve that competition as governed planning truth.

This means:

- resource contention must be surfaced explicitly
- contention resolution must be reviewable
- one project must not silently absorb another project’s resource assumptions
- project-local readiness must not be rewritten without explicit determination

Shared resource pressure is a planning fact, not an excuse for invisible reprioritization.

---

## Lifecycle Preservation Rule

Multi-project planning must preserve lifecycle truth per project.

This means:

- one project becoming Ready for Handoff does not change another project’s lifecycle stage
- one project being Deferred or Blocked does not automatically defer or block another project
- one project entering Return Under Reconsideration does not flatten another project’s planning continuity
- one project being Closed or Archived does not erase related but still-active project states

Portfolio-level visibility must not erase per-project lifecycle discipline.

---

## Readiness Preservation Rule

Readiness must remain project-local unless a governed cross-project dependency explicitly affects it.

This means:

- project readiness must be determined per project or per bounded project scope
- readiness must not be inferred from portfolio preference alone
- a portfolio-level desire to move one project first does not automatically make another project not ready
- a blocked dependency may affect readiness, but the reason must remain explicit

Preparedness across the portfolio is not the same as readiness within a project.

---

## Approval Preservation Rule

Approval posture must remain bounded per project and per action scope.

This means:

- approval for one project does not automatically apply to another project
- approval for one bounded scope does not automatically widen to portfolio-level authority
- one operator’s strategic preference across multiple projects does not automatically satisfy project-local governed approval requirements

Approval laundering means using cross-project planning context to imply that approval for one project or scope covers another project or scope for which approval has not been independently obtained.
Cross-project planning must not be used to launder approval across project boundaries.

---

## Decision Continuity Preservation Rule

Project V must preserve decision continuity per project even when making portfolio-level comparisons.

This means:

- project-specific decisions must remain referenceable in their own context
- cross-project prioritization must not silently supersede project-local decisions
- previous rejection, deferment, or approval-sensitive history must remain interpretable per project
- portfolio-level reasoning must not erase the decision trail of an individual project

Cross-project comparison is not cross-project supersedence by default.

---

## Scope Preservation Rule

Project V must preserve scope boundaries across projects.

This means:

- work from different projects must not be merged casually because it looks related
- one project’s handoff scope must not be widened by bundling in another project’s unresolved work
- cross-project themes, shared capabilities, or similar intent do not automatically create one combined project

Where a broader portfolio-level initiative is actually needed, that must be established explicitly through governed planning rather than implied from similarity.
Where a broader portfolio-level initiative is genuinely warranted, it must be established through explicit project intake and admission, recognizing the combined initiative as its own governed project rather than silently folding existing projects together.
The decision to combine or subsume existing projects must be governed, documented, and continuity-preserving rather than implied by operational convenience.

---

## Multi-Project Handoff Rule

Project V may coordinate handoffs across multiple projects, but it must not treat them as one undifferentiated execution transfer unless the planning doctrine has explicitly established that combined scope.

This means:

- each project’s handoff posture must remain identifiable
- each project’s readiness and approval posture must remain reviewable
- one project’s readiness must not be used to smuggle another project’s incomplete scope into execution

Coordinated handoff is allowed.
Collapsed handoff is not.

---

## Return and Reconsideration Rule

When multiple projects are affected by returned findings, changed conditions, or revised evidence, Project V must determine the impact per project rather than treating all affected projects as equally changed by default.

This means:

- return-triggered reconsideration must remain explicit per project
- changed conditions must be mapped to the projects they actually affect
- one project’s returned findings must not automatically mutate another project’s planning truth

When shared impact is confirmed across multiple projects, each affected project must still enter its own explicit Return Under Reconsideration lifecycle state.
Per-project reconsideration may proceed in parallel or sequence depending on dependency and priority, but the return path must remain explicit and separate per project.
A shared impact finding that affects five projects requires five governed reconsideration events, not one portfolio-level override.

Shared impact may exist.
It must still be evaluated through governed per-project reconsideration.

---

## Strategy vs Governance Rule

Project V may support strategic portfolio reasoning.
It must not let strategy dissolve governance.

This means:

- strategic importance does not override approval posture automatically
- strategic urgency does not erase lifecycle discipline
- strategic preference does not erase interface discipline
- strategic portfolio logic does not authorize execution shortcuts

Strategy may guide prioritization.
It does not self-authorize mutation.

---

## Reviewability Rule

Multi-project planning must remain reviewable enough that a later reader can determine:

- what projects were involved
- what project-local truths remained distinct
- what cross-project relationship or conflict existed
- what prioritization or sequencing decision occurred
- what governance posture still applied per project

If portfolio reasoning cannot be reconstructed without reading between the lines, the multi-project doctrine is being used incorrectly.

---

## Forbidden Multi-Project Drift Patterns

Project V has drifted if multi-project reasoning begins to:

- flatten projects into one work bucket
- treat project-local approval as portfolio-wide approval
- rewrite one project’s lifecycle by implication from another project
- merge scopes casually because they appear related
- hide cross-project conflict instead of surfacing it
- use portfolio urgency to bypass governance
- treat one project’s returned findings as automatic mutation authority over another project

These are doctrine failures, not optimization wins.

---

## Human-In-The-Loop Principle

Human review remains especially important when multi-project planning affects:

- priority ordering
- shared resource contention
- cross-project conflict resolution
- coordinated handoff sequencing
- portfolio-level changes that materially affect project-local posture

Project V should make multi-project reasoning more structured and more reviewable, not more opaque.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- portfolio-level visibility is allowed
- project-local truth must remain distinct
- cross-project prioritization is not the same as project-local approval
- cross-project conflict must be surfaced explicitly
- one project’s lifecycle, readiness, approval, or returned findings do not automatically rewrite another project
- coordinated planning is not permission to collapse boundaries

If an LLM could use portfolio awareness to treat multiple projects as one interchangeable mass of work, this doctrine is failing.

---

## Usage

This document should be used:

- when Project V is reasoning across multiple projects at once
- when reviewing whether portfolio logic is weakening project-local truth
- when deciding whether cross-project conflict or dependency handling remains governed
- when writing more detailed Project V portfolio or prioritization docs
- when checking whether strategic reasoning is blurring governance boundaries

---

## Related Docs

- `project-v.md`
- `system-invariants.md`
- `operational-workflow.md`
- `lifecycle.md`
- `byda-in-project-v.md` *(planned)*
- `v-forge-integration.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/auth-and-actor-model.md`
