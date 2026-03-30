# New Project Required Docs

## Purpose

This document defines the minimum documentation set a candidate new project must produce before it can be admitted into the V Ecosystem.

It exists to answer:

```text
What docs must exist before a new project is admitted, what does each required doc need to establish, and what documentation failures block admission?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the minimum required documentation set for new-project admission
- what each required doc must establish at a minimum
- which docs are mandatory before admission versus deferrable until after admission
- how missing, vague, or fake-authority docs should be handled during onboarding
- the anti-drift rules operators and LLMs must preserve when deciding whether a candidate project is documented enough to join the ecosystem

---

## Out of Scope

This document does not define:

- the full contents of every future project-specific doc
- the detailed access-control rules for every admitted project
- the detailed MCP model for every admitted project
- detailed post-admission implementation planning
- repo-local engineering documentation expectations

Those belong in more specific onboarding, governance, interface, project, and repo-local docs.

---

## System

- onboarding

---

## Core Rule

A new project must not be admitted until it has the minimum doctrine needed to make its role, truth ownership, boundaries, and admission posture legible to humans and LLMs.

A project is not documentation-ready because:

- there is a repo
- there are notes
- there is a backlog
- there is code
- there is an oral explanation

If the project cannot be understood and governed from explicit shared-root docs, it is not ready for admission.

---

## Required-Docs Definition

The required-docs set is the minimum documentation package that makes a candidate project doctrine-legible before admission.

This package exists so the ecosystem can answer, before admission:

- what the project is
- what truth it owns
- what truth it does not own
- what data posture applies
- what interfaces or surfaces matter
- what access posture applies
- what lifecycle and fitment posture applies

Required docs are not ceremony.
They are the minimum authority surface needed to prevent undefined projects from entering the ecosystem.

---

## Minimum Admission Documentation Set

Before admission, a candidate new project must have the following docs identified and in the shared docs root:

### 1. Identity Anchor Doc
The project’s top-level identity doc.

### 2. System Invariants Doc
The project’s non-negotiable identity and anti-drift constraints.

### 3. Data Boundaries Doc
The project’s canonical-data, reference-data, and out-of-bounds data posture.

### 4. Access and Boundary Rules Doc
The project’s access posture and cross-system boundary posture.

### 5. Lifecycle and Fitment Review Doc
The doc that records how the project fits the ecosystem and what lifecycle expectations apply after admission.

These are the minimum required docs.
If one of them is missing, the project is not admission-ready.

---

## Mandatory Before Admission vs Deferrable After Admission

### Mandatory Before Admission
The following must exist before admission:

- identity anchor doc
- system invariants doc
- data boundaries doc
- access and boundary rules doc
- lifecycle and fitment review doc
- any interface doc required to prevent immediate cross-system ambiguity at admission time

### Deferrable After Admission
The following may be written after admission if they are not required to make admission safe:

- deeper operational workflow docs
- secondary support docs
- implementation-facing docs
- repo-local engineering docs
- non-load-bearing reporting or maintenance refinements

### Rule
Only docs that are genuinely non-blocking may be deferred.
A doc is not deferrable merely because writing it is inconvenient.

---

## What the Identity Anchor Doc Must Establish

The identity anchor doc must establish at least:

- what the project is
- what role it plays in the ecosystem
- what truth it owns
- what truth it does not own
- how it relates to Project V, VEDA, and V Forge
- why it exists as a distinct project rather than as a subordinate concern

### Rule
If the identity doc cannot explain why the project exists as a distinct truth owner, the candidate should not be admitted.

---

## What the System Invariants Doc Must Establish

The system invariants doc must establish at least:

- what conditions must remain true for the project to preserve its identity
- what drift patterns are forbidden
- what ownership boundaries must remain intact
- what governance and interface posture must not be bypassed

### Rule
If the invariants doc is vague, the project has no hard anti-drift spine and is not ready for admission.

---

## What the Data Boundaries Doc Must Establish

The data boundaries doc must establish at least:

- what data the project owns canonically
- what data it may reference only
- what data it may interpret without owning
- what data is out of bounds
- how imported or convenience data must remain honest where relevant

### Rule
If the project cannot explain its data posture, it cannot explain its truth posture.
That blocks admission.

---

## What the Access and Boundary Rules Doc Must Establish

The access and boundary rules doc must establish at least:

- what systems or surfaces the project may read from
- what systems or surfaces it may write to
- what interfaces are required
- what access is forbidden
- how access follows role and boundary classification
- what MCP or tool surfaces the project may expose or consume, and under what governance conditions

### Rule
A project must not be admitted with access assumptions that only exist in someone’s head.

---

## What the Lifecycle and Fitment Review Doc Must Establish

The lifecycle and fitment review doc must establish at least:

- why the project was admitted
- what classification justified admission
- what ecosystem role it fills
- what overlap risks were reviewed
- what post-admission fitment expectations apply
- what would trigger re-evaluation or reclassification later

### Rule
Admission must leave behind a reviewable fitment record.
If the ecosystem cannot later explain why the project was admitted, the onboarding model has failed.

---

## Required Interface Docs Rule

If a candidate project would immediately require cross-system interaction at admission time, the relevant interface docs must exist before admission whenever their absence would create ambiguity about:

- what crosses system boundaries
- what ownership is transferred or not transferred
- what access is legitimate
- what system remains the owner of the truth involved

### Rule
A project must not be admitted into interface ambiguity.
If admission would immediately create a new live cross-system interface question, that question must be documented before admission.
The determination of whether a cross-system interface is immediately required is made by the onboarding reviewer, not by the candidate project. A candidate may not self-certify that its interfaces are deferrable. If there is genuine uncertainty about whether a live interface question would exist at admission, the conservative position is to require the interface doc before admitting.

---

## Documentation Quality Rule

A required doc is not satisfied merely because a file exists.

A required doc must be:

- explicit
- bounded
- load-bearing
- reviewable
- usable by a capable LLM without hidden oral context

The following do not satisfy the requirement:

- placeholder docs
- note dumps
- brainstorming files
- TODO-shaped fake doctrine
- prose that only gestures at boundaries without stating them

### Rule
A weak required doc counts as missing.

---

## Fake-Authority Rule

A candidate project must not be admitted using fake authority such as:

- empty doc shells
- copied old repo docs treated as current without refoundation
- implementation notes pretending to be doctrine
- oral explanations replacing required docs
- scattered issue comments substituting for authority

### Rule
The shared root must contain the real authority set.
If authority is fragmented or performative, admission is not valid.

---

## Naming and Placement Rule

Required docs must:

- live in the shared-root onboarding and project folders as appropriate
- use stable, legible names
- be placed where later readers can find them predictably
- be referenced by the onboarding cluster and the admitted project’s own doc set

An admitted project’s core authority docs must live in their own named top-level folder inside the shared root, following the same pattern as `project-v/`, `veda/`, and `v-forge/`. The folder name must match the project’s canonical identifier.

### Rule
Documentation discoverability is part of documentation validity.
If a capable later reader cannot find the minimum admission docs quickly, the documentation set is too weak.

---

## Deferred-Docs Guardrail

Deferral is allowed only for docs that do not weaken admission clarity.

A deferred doc must not be one that later readers would need in order to answer:

- what is this project?
- what truth does it own?
- what truth does it not own?
- what access does it have?
- what data posture applies?
- why was it admitted?

### Rule
If deferring a doc would make admission depend on memory or inference, the doc is not deferrable.

---

## Documentation Failure Outcomes

When required docs are missing or weak, the correct onboarding outcome is one of:

- return for refinement
- defer
- reject

### Rule
Missing required docs must not be normalized as “close enough.”
Documentation failure is an admission blocker, not a cleanup task for later.

---

## Human-In-The-Loop Principle

Required-docs sufficiency is governance-sensitive because poor documentation quality changes what the ecosystem can understand and govern.

Human review may be required where:

- a candidate claims a doc is deferrable
- a candidate claims an existing doc is "good enough"
- a candidate relies on inherited or migrated authority from an old repo
- a candidate’s required docs are present but still ambiguous in load-bearing ways

A project must not be admitted because reviewers are tired of asking for the missing docs.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the minimum required-docs set is mandatory before admission
- a file existing is not the same as a doc being valid
- fake-authority docs do not count
- deferral is narrow and must not weaken admission clarity
- documentation failure blocks admission rather than becoming later cleanup

If the required-docs model is used to admit doctrine-thin projects with the promise that clarity will appear later, the doctrine is wrong.

---

## Usage

This document should be used:

- when deciding whether a candidate project has enough docs for admission
- when structuring the initial doctrine package for a candidate project
- when rejecting fake-authority or placeholder documentation sets
- when deciding whether a doc is mandatory before admission or genuinely deferrable
- when reviewing whether the onboarding cluster is being applied honestly

---

## Related Docs

- `new-project-onboarding-doctrine.md`
- `new-project-classification-model.md`
- `new-project-access-and-boundary-rules.md`
- `new-project-data-boundary-doctrine.md`
- `new-project-lifecycle-and-fitment-review.md` *(planned)*
- `../README.md`
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../governance/approval-and-escalation-model.md`
