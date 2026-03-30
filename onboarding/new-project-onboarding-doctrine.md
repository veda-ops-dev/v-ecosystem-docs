# New Project Onboarding Doctrine

## Purpose

This document defines how a new project is admitted into the V Ecosystem.

It exists to answer:

```text
How does a new project enter the ecosystem in a governed way, what must be true before it is admitted, and what rules prevent casual project accumulation, boundary blur, and doctrine-free fitment?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the onboarding model for admitting new projects into the V Ecosystem
- what onboarding is supposed to produce before a project is considered admitted
- what must be evaluated before a project is allowed to join the ecosystem
- how new projects are classified, bounded, and fit to existing ecosystem roles
- the anti-drift rules operators and LLMs must preserve during new-project onboarding

---

## Out of Scope

This document does not define:

- the detailed classification taxonomy for all future project types
- the full required-docs checklist for every project shape
- the full access-control model for every system and tool
- detailed MCP implementation mechanics
- detailed project-specific workflow design after admission

This document governs adding a new bounded system to the V Ecosystem. It does not govern adding a new work project inside Project V. If the candidate is a new piece of work for Project V to plan, use `../workflows/project-intake-workflow.md` instead of this doc.

Those belong in more specific onboarding, governance, interface, and project docs.

---

## System

- onboarding

---

## Core Rule

A new project may join the V Ecosystem only through a governed onboarding process that makes its role, boundaries, required docs, access posture, and ecosystem fit explicit before admission.

A project is not admitted because it seems useful.
A project is not admitted because implementation wants a place to put code.
A project is not admitted because an LLM or operator can imagine a role for it after the fact.

If a project cannot explain what truth it owns, what truth it does not own, how it fits the existing ecosystem, and what doctrine it must satisfy before joining, it is not ready for admission.

---

## Onboarding Definition

New-project onboarding is the governed process by which a candidate project is evaluated, classified, bounded, documented, and either admitted, deferred, rejected, or returned for refinement before it becomes part of the active V Ecosystem authority set.

This process exists so the ecosystem can grow deliberately rather than accumulate doctrine-free projects that blur ownership, duplicate roles, or bypass governance.

---

## Admission Principle

Admission into the ecosystem is a governed outcome.
It is not a casual naming event.
It is not a repo-creation event.
It is not a UI or MCP registration event.

Admission means the ecosystem has determined that:

- the project has a bounded role
- the project has a bounded truth domain
- the project does not collapse an existing system role
- the project has enough required doctrine to be understood and governed
- the project has an explicit access and boundary posture
- the project can be operated by humans and LLMs without hidden tribal assumptions

---

## Why Onboarding Exists

The V Ecosystem is expected to grow.
That growth must be governed.

Onboarding exists to prevent:

- duplicate system roles
- convenience projects with no durable doctrine
- boundary collapse across planning, observability, and execution
- access sprawl before ownership is clear
- project admission without minimum documentation
- LLM-led implementation against undefined or contradictory project roles

A project added without onboarding is not an ecosystem expansion.
It is an ecosystem drift event.

---

## Required Onboarding Outcomes

A valid onboarding process must produce enough clarity to answer at least these questions:

- what is this project for?
- what truth does it own?
- what truth does it explicitly not own?
- how does it relate to Project V, VEDA, and V Forge?
- what interfaces does it require?
- what docs must exist before it is admitted?
- what access and boundary rules apply?
- what data-boundary posture applies?
- what lifecycle and fitment expectations apply after admission?

If onboarding cannot answer those questions explicitly, the candidate project is not ready.

---

## Entry Preconditions

A candidate project should enter onboarding only when there is a real ecosystem question to evaluate, such as:

- a proposed new truth domain that is not already owned cleanly by an existing system
- a sustained role need that cannot be handled by Project V, VEDA, or V Forge without boundary drift
- a repeated workflow or coordination need that suggests a genuinely new bounded system role
- an explicit operator or strategic direction to evaluate a new project for ecosystem fit

A project should not enter onboarding merely because:

- a repo exists
- a feature cluster feels large
- a tool surface wants a label
- a workflow is inconvenient inside an existing system
- implementation detail is being mistaken for system identity

---

## Primary Onboarding Stages

## Stage 1 - Candidate Proposal

### Description
A candidate project is proposed as a possible new ecosystem project.

The proposal should be explicit enough to state:

- the candidate project name
- the proposed role
- the proposed truth domain
- the problem the project is intended to solve
- why existing systems may be insufficient

### Rule
A candidate proposal is not admission.
It is the start of evaluation.

---

## Stage 2 - Role and Boundary Classification

### Description
The ecosystem evaluates what kind of project this is supposed to be.

This includes determining:

- what role the project plays
- what truth domain it may own
- what truth domains it must not own
- whether it overlaps dangerously with Project V, VEDA, or V Forge
- whether the project belongs as a real ecosystem project at all

### Rule
If the candidate cannot be classified without blurry language or overlapping ownership claims, onboarding must not proceed as though the project is fit.

---

## Stage 3 - Fitment Evaluation

### Description
The ecosystem evaluates whether the proposed project actually belongs in the ecosystem.

This includes evaluating:

- whether the role is real and durable
- whether the role is distinct from existing systems
- whether the role is bounded enough to govern
- whether the project adds clarity instead of complexity theater
- whether ecosystem growth is actually warranted

### Rule
Not every useful idea deserves admission as a new project.
A candidate may be rejected because it should remain:

- inside an existing system
- inside an existing workflow
- inside repo-local implementation support
- outside the ecosystem entirely

---

## Stage 4 - Required Doctrine Identification

### Description
If the candidate survives fitment evaluation, onboarding identifies the minimum doctrine set required before admission.

This includes identifying:

- the identity anchor doc
- system-invariants doc
- data-boundaries doc
- any core operational or interface docs required for the project to be safely understood
- any onboarding, access, MCP, or workflow docs needed before activation

### Rule
A new project must not be admitted on vibes with the promise that doctrine will be written later.
Minimum doctrine is a precondition for admission, not cleanup after admission.

---

## Stage 5 - Access and Data Boundary Evaluation

### Description
Before admission, the ecosystem evaluates:

- what systems the project may read from
- what systems it may write to
- what interfaces it requires
- what data may be stored canonically
- what data may be referenced only
- what data must remain out of bounds

### Rule
Access posture must follow role clarity.
Access must not be granted first and justified later.

---

## Stage 6 - Admission Decision

### Description
A governed admission decision is made.

Allowed outcomes include:

- admit
- defer
- reject
- return for refinement

### Rule
Admission is valid only when the minimum onboarding outputs are explicit, bounded, and reviewable.
Admission is a governed approval event under the ecosystem approval and escalation model. An operator asserting that a project is admitted does not constitute a governed admission without satisfying the required approval posture. The approval requirements for new-project admission are defined in `../governance/approval-and-escalation-model.md`.
If approval is required, lack of explicit approval is not permission to admit.

---

## Stage 7 - Post-Admission Activation

### Description
After admission, the project may enter the active authority set and begin receiving more specific doctrine, implementation, workflow, or integration work.

### Rule
Post-admission activation does not erase onboarding constraints.
The admitted project must continue to honor its classified role, truth domain, and access posture.
If later implementation pressure pushes the project outside its admitted role, that is a new governance problem, not proof that the original boundary was unnecessary.
When post-admission implementation pressure pushes an admitted project outside its classified role or truth domain, the correct response is to treat it as a classification revision event requiring the same onboarding review posture, not to normalize the expansion silently. Re-evaluation and re-admission under a revised role is the governed path.

---

## Allowed Onboarding Outcomes

A candidate project may result in one of these governed outcomes:

### Admit
The project is accepted as a bounded ecosystem project.

### Defer
The idea may be valid later, but current ecosystem timing, maturity, or priority does not justify admission yet.

### Reject
The candidate should not join the ecosystem as a distinct project.

### Return for Refinement
The candidate may be promising, but its role, boundary, doctrine, or fitment posture is too weak or ambiguous for admission.

### Rule
These outcomes must remain explicit.
A vague "maybe later" without a classified outcome weakens continuity and encourages casual resurrection of half-formed project ideas.

---

## Non-Admission Cases

A candidate should be rejected or returned when it is actually:

- a feature cluster inside an existing system
- a repo-local implementation support concern
- an MCP surface rather than a real system
- a workflow refinement rather than a new project
- a reporting or governance refinement rather than a new truth owner
- a duplicate planner, duplicate observability role, or duplicate execution role in disguise

### Rule
System count should grow only when bounded truth ownership grows.
If the proposed project does not create a genuine bounded truth role, it probably should not exist as a new ecosystem project.

---

## Minimum Admission Standard

A candidate project is not ready for admission unless all of the following are true:

- its role is clear
- its truth domain is clear
- its non-ownership boundaries are clear
- its relationship to Project V, VEDA, and V Forge is clear
- its required doctrine set is identified
- its data-boundary posture is clear
- its access and interface posture is clear
- its admission outcome is reviewable

This is the minimum standard.
It is not an ideal future state.

---

## Relationship to Existing Systems

A new project must fit the existing ecosystem rather than casually redefining it.

That means onboarding must explicitly evaluate whether the candidate:

- overlaps with Project V planning ownership
- overlaps with VEDA evidence or observability ownership
- overlaps with V Forge execution ownership
- requires a new interface or only a better use of an existing one
- changes ecosystem complexity in a way that is justified by clearer ownership rather than architecture vanity

### Rule
A new project does not get to redefine the ecosystem merely by existing.
It must be admitted into the ecosystem that already has defined roles.

---

## Documentation-First Principle

A new project must be doctrine-legible before it is considered admitted.

This means a capable LLM should be able to understand, from the shared-root docs:

- why the project exists
- what it owns
- what it does not own
- how it fits the ecosystem
- what its minimum rules are

If the project only makes sense through oral explanation, onboarding has failed.

---

## Access-Follows-Boundary Principle

A new project's access posture must follow from its classified role and boundary posture.

This means onboarding must not normalize:

- broad access before role clarity
- cross-system write access by default
- MCP or tool exposure before doctrine exists
- local implementation shortcuts becoming ecosystem-wide access assumptions

### Rule
Technical possibility is not admission evidence.
Access is not authority.

---

## Data-Follows-Ownership Principle

A new project must have a clear data-boundary posture before admission.

This includes determining:

- what data it may own canonically
- what external data it may reference
- what external data it may interpret without owning
- what data must remain entirely outside it

### Rule
A project with an unclear data posture is not ready for admission, because unclear data posture usually means unclear truth ownership.

---

## Human-In-The-Loop Principle

New-project admission is governance-sensitive because it changes the ecosystem itself.

Human review may be required where admission would:

- add a new truth owner
- add new cross-system interfaces
- broaden access posture materially
- increase ecosystem operational complexity
- create a new LLM-facing system role

A candidate project must not be admitted as an unreviewed convenience expansion.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- not every useful idea becomes a new ecosystem project
- onboarding is a governed fitment process, not a naming exercise
- a project must have a bounded role, truth domain, doctrine set, and access posture before admission
- role clarity comes before access, implementation, or MCP exposure
- ecosystem growth is governed expansion, not convenience sprawl

If onboarding is used to rubber-stamp vaguely useful project ideas into the ecosystem, the doctrine is wrong.

---

## Usage

This document should be used:

- when evaluating whether a candidate should become a new ecosystem project
- when deciding whether a proposal belongs in onboarding at all
- when structuring the rest of the onboarding doc cluster
- when rejecting casual or doctrine-free ecosystem expansion
- when orienting humans and LLMs to how new projects join the ecosystem

---

## Related Docs

- `../README.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `new-project-classification-model.md`
- `new-project-required-docs.md`
- `new-project-access-and-boundary-rules.md`
- `new-project-data-boundary-doctrine.md`
- `new-project-lifecycle-and-fitment-review.md` *(planned)*
- `../governance/approval-and-escalation-model.md`
- `../governance/agent-operating-doctrine.md`
- `../workflows/project-intake-workflow.md`
