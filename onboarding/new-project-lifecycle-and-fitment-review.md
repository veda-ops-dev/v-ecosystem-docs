# New Project Lifecycle and Fitment Review

## Purpose

This document defines the lifecycle and fitment review posture a new project must satisfy before and after admission into the V Ecosystem.

It exists to answer:

```text
Why was this project admitted, how is its ongoing ecosystem fit reviewed, what post-admission expectations apply, and what events trigger re-evaluation, reclassification, or possible de-fitment?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what lifecycle and fitment review must establish before a new project is admitted
- what post-admission fitment expectations must remain reviewable
- what kinds of drift, overlap, or ecosystem-friction events trigger re-evaluation
- how admission rationale, post-admission expectations, and re-review posture must be recorded
- the anti-drift rules operators and LLMs must preserve when evaluating whether an admitted project still belongs in the ecosystem as classified

---

## Out of Scope

This document does not define:

- the initial classification model itself
- the required-docs package itself
- the detailed access-control model itself
- the detailed data-boundary doctrine itself
- project-specific implementation workflow after admission

Those belong in the other onboarding docs and project-specific authority docs.

---

## System

- onboarding

---

## Core Rule

Admission is not the end of onboarding truth.
A new project must remain fit for the ecosystem after admission, not just at the moment it was approved.

A project that was once admissible does not become permanently valid merely because it already exists.
If its role, boundaries, access posture, data posture, or operational behavior drift away from the fitment basis that justified admission, that drift must be reviewed explicitly.

---

## Lifecycle and Fitment Review Definition

Lifecycle and fitment review is the governed record of:

- why a project was admitted
- what classification justified its admission
- what ecosystem role it was expected to fill
- what boundaries and constraints were part of that admission basis
- what later conditions would require re-evaluation, reclassification, tighter constraints, or possible de-fitment

This review exists so ecosystem admission remains explainable after the fact.
Without a fitment record, the ecosystem cannot later distinguish between a project that still belongs and a project that merely accumulated momentum.

---

## Admission-Basis Rule

Before admission, the lifecycle and fitment review must state at least:

- why the project exists as a distinct ecosystem project
- what classification outcome justified admission
- what truth domain justified admission
- what overlapping-system risks were considered
- what access and data-boundary assumptions were part of the admission basis
- what post-admission expectations must remain true for the project to continue fitting the ecosystem

### Rule
If the ecosystem cannot explain why a project was admitted in bounded doctrinal terms, the project is not ready for admission.

---

## Fitment Definition

A project is fit for the ecosystem when:

- its classified role is still real
- its truth domain is still bounded
- its existence still adds clarity rather than duplication
- its access posture still matches its role
- its data posture still matches its role
- its interaction with other systems does not create boundary blur or unnecessary ecosystem complexity

### Rule
Fitment is not popularity.
Fitment is not current usefulness.
Fitment is not sunk-cost protection.
Fitment is bounded ecosystem legitimacy.

---

## Minimum Review Record

A lifecycle and fitment review record must be explicit enough to preserve:

- admission date or approval point
- classification outcome
- admitted role summary
- admitted truth-domain summary
- key non-ownership boundaries
- access posture summary
- data-boundary posture summary
- identified overlap risks
- identified review triggers
- current fitment status

The lifecycle and fitment review record must live in the shared root under the admitted project's own folder, alongside its other required docs. It must not exist only in onboarding notes, approval threads, or operator memory.

### Rule
If later readers cannot reconstruct the admission logic and current fitment posture from the review record, the record is too weak.

---

## Post-Admission Expectations Rule

After admission, a project is expected to preserve at least the following:

- its classified role remains legible
- its truth-domain claims remain bounded
- its access posture does not expand without review
- its data posture does not drift into aggregation or duplicate ownership
- its interfaces remain explicit
- its MCP or tool surfaces do not broaden beyond their governed purpose
- its continued existence remains easier to justify than absorption into an existing system

### Rule
Post-admission expectations are not aspirational.
They are the continuing conditions of legitimate fit.

---

## Fitment Review Triggers

A project must be re-reviewed when one or more of the following occur:

- classification pressure appears because the project’s role no longer matches its admitted type
- access drift occurs or newly requested access exceeds the approved posture
- data-boundary drift occurs or canonical ownership claims expand
- boundary integrity violations appear
- overlap with Project V, VEDA, or V Forge increases materially
- MCP or tool-surface growth changes the project’s practical role
- implementation pressure pushes the project toward becoming a second planner, second observability system, or second executor
- the project’s continued distinct existence becomes harder to justify than absorption into an existing system

### Rule
A fitment trigger is not a suggestion.
It is a governed prompt for re-evaluation.

---

## Material Fitment Drift Rule

Fitment drift is material when the change would alter:

- the original admission decision
- the project’s classification outcome
- the project’s access posture
- the project’s data-boundary posture
- the project’s legitimacy as a distinct ecosystem project

### Rule
A change is material when, if it had been true at admission time, it would have affected whether or how the project was admitted.
Minor implementation evolution is not automatically fitment drift.
But boundary, ownership, or role changes are.

---

## Review Outcomes

A lifecycle and fitment review may conclude with one of the following outcomes:

### 1. Continue as Classified
The project still fits the ecosystem as admitted.

### 2. Continue with Tighter Constraints
The project still fits, but only if access, data posture, interface posture, or operational scope is tightened.

### 3. Reclassify
The project no longer fits its admitted type and must be explicitly reclassified.

### 4. Absorb into Existing System
The project no longer justifies distinct existence and should be merged back into an existing system role.

### 5. Defer Further Expansion
The project may continue in its current bounded role, but proposed growth or new scope is not approved.

### 6. De-Fit for Ecosystem Admission
The project should no longer remain an admitted ecosystem project under its current posture.

### Rule
These outcomes must remain explicit.
A project must not drift between review states through vague verbal consensus.
Review outcomes that narrow, constrain, absorb, or de-fit an admitted project require the same governance posture as original admission. The authority to reach these outcomes does not belong to the project being reviewed. Outcomes 1 and 5 may be reached by routine governance review. Outcomes 2 through 4 and 6 require explicit governed approval through `../governance/approval-and-escalation-model.md`.

---

## Reclassification and Re-Review Rule

If lifecycle review shows the project no longer matches its admitted classification, the correct response is:

- explicit re-evaluation
- explicit revised classification or constrained continuation
- explicit review of access posture
- explicit review of data posture
- explicit review of whether the project should still exist distinctly

### Rule
An admitted project does not get to rewrite its own admission basis through accumulated usage.
Reclassification follows the same governance posture as original admission.

---

## Absorption Test

A project should be considered for absorption into an existing system when one or more of the following become true:

- its distinct truth domain is no longer meaningfully distinct
- its primary value is now implementation convenience rather than bounded ownership clarity
- its access and data posture increasingly depend on another system’s truth domain
- its role can be described more honestly as a capability of an existing system
- keeping it separate adds more ecosystem complexity than boundary clarity

### Rule
Separate existence must remain justified.
When separate existence is no longer the clearer option, fitment review must say so explicitly.

---

## De-Fit Rule

De-fitment does not necessarily mean deletion.
It means the project is no longer justified as an admitted ecosystem project under its current role, posture, or scope.

A de-fit outcome may require:

- absorption into an existing system
- reduction to a non-admitted support or repo-local concern
- reclassification under a different bounded role
- retirement from active ecosystem doctrine

### Rule
The ecosystem must be allowed to become simpler again when a project no longer justifies its own admission.

---

## Review Cadence Rule

Fitment review does not need to be constant, but it must not be absent.

A project should be reviewed:

- at admission
- whenever a fitment trigger occurs
- whenever major access or data-boundary changes are proposed
- whenever reclassification pressure appears
- whenever separate existence is materially questioned

### Rule
Review cadence follows change pressure, not calendar ritual alone.

---

## Documentation and Traceability Rule

Lifecycle and fitment review must leave behind an explicit record strong enough to answer:

- why does this project exist?
- why is it still separate?
- what boundaries justified its admission?
- what later changes triggered review?
- what outcome did the review reach?

### Rule
If fitment review leaves no durable trace, future reviewers will reconstruct it from folklore.
That is governance failure.

---

## Human-In-The-Loop Principle

Lifecycle and fitment review is governance-sensitive because it determines whether the ecosystem should continue to contain a project as currently admitted.

Human review may be required where fitment review would:

- tighten or revoke access
- constrain or revise data posture
- reclassify a project
- absorb a project into an existing system
- conclude that the project no longer fits as admitted

A project must not self-certify its own continuing fit merely because it remains active.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- admission rationale must remain reconstructable after admission
- a project can stop fitting the ecosystem even if it once fit correctly
- fitment review is triggered by role, access, data, and boundary drift
- explicit review outcomes matter more than accumulated usage or convenience
- separate existence must remain continuously justifiable

If a project remains admitted only because unwinding it feels annoying, the doctrine is wrong.

---

## Usage

This document should be used:

- when recording why a candidate project was admitted
- when defining post-admission fitment expectations
- when evaluating whether an admitted project still belongs as classified
- when triggering re-review, reclassification, tighter constraints, absorption, or de-fitment
- when writing or reviewing a project’s lifecycle and fitment review record

---

## Related Docs

- `new-project-onboarding-doctrine.md`
- `new-project-classification-model.md`
- `new-project-required-docs.md`
- `new-project-access-and-boundary-rules.md`
- `new-project-data-boundary-doctrine.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/decision-continuity-doctrine.md`
