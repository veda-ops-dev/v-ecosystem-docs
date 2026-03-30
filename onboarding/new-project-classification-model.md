# New Project Classification Model

## Purpose

This document defines how a candidate new project is classified during onboarding in the V Ecosystem.

It exists to answer:

```text
How do we determine what kind of project a candidate is, what truth domain it may own, what truth domain it must not own, and whether it belongs as a real ecosystem project at all?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the classification model used during new-project onboarding
- how candidate projects are typed by role and truth domain
- how overlap with existing systems is detected and handled
- how to distinguish real bounded ecosystem projects from misclassified features, workflows, tools, or support surfaces
- the anti-drift rules operators and LLMs must preserve when assigning a candidate project type

---

## Out of Scope

This document does not define:

- the full required-docs set for every admitted project
- the full access-control policy for every admitted project
- detailed MCP implementation rules
- detailed project-specific lifecycle doctrine after admission
- detailed interface contracts for future admitted systems

Those belong in more specific onboarding, interface, governance, and project docs.

---

## System

- onboarding

---

## Core Rule

A candidate project must be classified by bounded role and bounded truth domain before it can be admitted into the V Ecosystem.

Classification is not naming.
Classification is not branding.
Classification is not architecture theater.

If a candidate cannot be classified without overlap blur, vague ownership claims, or convenience-driven exceptions, it is not ready for admission.

---

## Classification Definition

New-project classification is the governed process of determining:

- what kind of system the candidate is
- what truth domain it may own
- what truth domains it must not own
- whether it is distinct from existing ecosystem systems
- whether it is actually a new project rather than a misclassified non-project concept

Classification exists to stop ecosystem growth from becoming role duplication with prettier names.

---

## Classification Principle

A real ecosystem project must be classifiable through bounded ownership.

The first question is not:

- what stack will it use?
- what UI will it have?
- what repo will hold it?
- what tools will connect to it?

The first question is:

- what truth does it own?

If that question cannot be answered clearly, the candidate is not yet a valid ecosystem project.

---

## Primary Classification Axes

Every candidate project must be classified across at least these axes:

### 1. Role Type
What ecosystem role the project plays.

### 2. Truth Domain
What kind of truth it may own canonically.

### 3. Non-Ownership Boundary
What truth domains it must explicitly not own.

### 4. Fitment Status
Whether it belongs as a real ecosystem project, a subordinate concern, or a non-admitted concept.

### 5. Access Implication
What level and kind of cross-system access this classification would justify, if admitted.

A candidate that cannot be classified cleanly across these axes is not ready.

---

## Baseline Existing Role Types

The existing V Ecosystem already contains these core role types:

### Planning and Orchestration
Owned today by **Project V**.

### Signal, Evidence, and Observability
Owned today by **VEDA**.

### Execution
Owned today by **V Forge**.

### Rule
A candidate project must not be admitted merely by rephrasing one of these existing roles with a narrower label or trendier wrapper.
If the candidate is only a duplicate planner, duplicate observability system, or duplicate executor, it should be rejected or absorbed into the appropriate existing system.

---

## Candidate Classification Outcomes

A candidate must be classified into one of the following fitment outcomes:

### 1. Real New Ecosystem Project
A genuinely distinct bounded truth owner that may justify admission.

### 2. Existing-System Feature Cluster
A capability that belongs inside Project V, VEDA, or V Forge rather than as a new project.

### 3. Workflow or Interface Refinement
A coordination or process concern that belongs in workflow or interface doctrine rather than as a new truth owner.

### 4. Tool Surface or MCP Surface
A surface, control plane, operator surface, or MCP exposure that does not itself justify a new project.

### 5. Repo-Local Implementation Support
An engineering or implementation concern that belongs in repo-local support docs, code, or tooling rather than ecosystem doctrine.

### 6. Out-of-Ecosystem Concept
A concept that may be useful somewhere, but should not join the V Ecosystem as an admitted project.

### Rule
Most candidates should fail to become real new ecosystem projects.
That is a feature of the model, not a weakness.

---

## Real New Ecosystem Project Test

A candidate may be classified as a real new ecosystem project only if all of the following are true:

- it owns a bounded truth domain not already owned cleanly by an existing system
- that truth domain is durable enough to justify its own doctrine and operational surface
- the project adds clarity to the ecosystem rather than duplicating an existing role
- the project can state what it does not own as clearly as what it does own
- the project requires its own admission because keeping it inside an existing system would create boundary drift

### Rule
A candidate that merely concentrates a subset of an existing system's work is not automatically a new project.
Specialization is not the same as distinct truth ownership.

---

## Misclassification Tests

A candidate is probably misclassified if it is primarily:

- a new UI for an existing system
- a reporting surface for an existing system
- a package of workflows that already fit an existing system role
- a cross-system integration convenience layer with no bounded truth domain
- a thin wrapper around tools or MCP access
- an implementation cluster mistaken for a system
- a policy or governance refinement mistaken for a project
- a storage location looking for a justification

### Rule
A candidate that fails the misclassification tests should not be rescued by creative storytelling.
It should be reclassified honestly.

---

## Truth Domain Classification Rule

A candidate project must identify its canonical truth domain in a way that is both positive and negative.

It must say:

- what truth it owns
- what truth it does not own

A positive-only claim is insufficient.
For example, saying only "it helps with planning" or "it supports execution" is not enough.
The candidate must specify whether it owns planning truth, execution truth, observability truth, governance truth, or some distinct bounded domain that does not overlap them improperly.

### Rule
If a candidate truth domain can be re-described as "really still Project V," "really still VEDA," or "really still V Forge" without losing meaning, the candidate probably does not justify admission.

---

## Boundary Conflict Rule

If a candidate project's proposed role overlaps materially with an existing system, the overlap must be resolved explicitly.

Examples of overlap conflict include:

- candidate planning truth overlapping Project V planning truth
- candidate evidence or observability truth overlapping VEDA ownership
- candidate execution or implementation truth overlapping V Forge ownership
- candidate governance posture pretending to own decisions rather than support them

### Rule
Unresolved overlap is disqualifying for admission.
A candidate does not become distinct merely because it narrows its name or claims to be "specialized."

---

## Distinctness Rule

Distinctness must be structural, not rhetorical.

A candidate is distinct only when it introduces a genuinely different bounded ownership role that improves ecosystem clarity.

Distinctness is not established by:

- a different stack
- a different repo
- a different operator surface
- a narrower operational focus inside an already-owned truth domain
- a desire for separate team ownership

### Rule
Team structure, implementation preference, or tool preference do not by themselves justify ecosystem-level admission.

---

## Classification Questions

A candidate project should be classifiable through questions such as:

- what truth does this project own canonically?
- what truth does it explicitly not own?
- what existing system would own this if the candidate did not exist?
- why is keeping it inside that existing system insufficient?
- is this a truth owner, a workflow, a surface, a tool, or an implementation cluster?
- what cross-system interfaces would this classification require?
- what access would this classification justify?
- what would break if this candidate were rejected and absorbed elsewhere?

These questions are meant to expose whether the candidate is real or merely convenient.

---

## Project Type Families

The ecosystem may eventually admit new project types beyond the first three systems.
But any candidate should still fit one of these broad families:

### 1. New Truth Owner
A new bounded system of record for a distinct truth domain.

### 2. Subordinate to Existing Truth Owner
A concept that belongs under an existing system rather than as a new project.

### 3. Coordination Layer Without Independent Truth Ownership
Not admissible as a separate project unless it can demonstrate a distinct durable truth domain independent of its coordination function.

### Rule
Coordination by itself is not enough.
A coordination concern without durable truth ownership must remain an interface, workflow, or governance construct unless it can demonstrate a distinct durable truth domain independent of its coordination function.

---

## Access Implication Rule

Classification has access consequences.

A candidate classified as a real truth owner may justify:

- bounded interfaces
- bounded read paths
- possibly bounded write paths where doctrine allows
- its own access and boundary docs

A candidate classified as a workflow, tool surface, or implementation support concern should not be used to justify ecosystem-level access expansion.

### Rule
Do not let a candidate gain access by being overclassified.
Access posture must follow correct classification, not wishful classification.
When a project is reclassified to a lower-access type, access granted under the prior incorrect classification must be reviewed and adjusted to match the corrected classification. It does not persist by default.

---

## Data Implication Rule

Classification also has data-boundary consequences.

A candidate classified as a real new ecosystem project must be able to state:

- what it stores canonically
- what it references only
- what it may interpret without owning
- what remains entirely outside it

A candidate that cannot state those data implications is not ready to be classified as a real ecosystem project.

---

## Reclassification Rule

Classification is not allowed to drift silently after admission.

If later evidence shows that an admitted project's classification was wrong, incomplete, or materially changed by implementation pressure, the correct response is:

- explicit re-evaluation
- explicit revised classification
- explicit doctrine update
- explicit review of whether the project still belongs as admitted

### Rule
Reclassification may be initiated by any operator with governance authority over the admitted project, or by the ecosystem governance layer when implementation evidence shows material divergence from the admitted classification. Reclassification follows the same approval posture required for original admission. An admitted project cannot block its own reclassification merely by asserting that implementation pressure justified the drift.
Silent post-admission reclassification is a governance failure.

---

## Anti-Proliferation Principle

The classification model should reject more candidates than it admits.

This is desirable because the ecosystem should grow only when bounded truth ownership grows.

The model must resist pressure from:

- convenience
- enthusiasm
- implementation momentum
- repo count
- UI count
- MCP count
- "it might be useful later" logic

### Rule
A candidate should not become a project merely because it is easier to name than to classify honestly.

---

## Human-In-The-Loop Principle

Classification is governance-sensitive because it determines what kinds of systems the ecosystem is allowed to contain.

Human review may be required where classification would:

- add a new truth owner
- create a new cross-system access path
- create a new bounded interface family
- materially increase ecosystem complexity
- challenge an existing system's ownership boundary

A candidate must not self-classify into admission through LLM confidence alone.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- classification is about bounded role and bounded truth ownership
- most candidates should not become new ecosystem projects
- duplication of Project V, VEDA, or V Forge roles is disqualifying
- UI, MCP, workflow, and implementation concerns usually do not justify admission
- access and data posture depend on correct classification
- post-admission drift requires explicit reclassification rather than silent expansion

If classification is used to justify system proliferation without distinct truth ownership, the doctrine is wrong.

---

## Usage

This document should be used:

- when classifying a candidate during onboarding
- when deciding whether a candidate is a real ecosystem project or a misclassified non-project concept
- when structuring required-docs, access, and data-boundary onboarding docs
- when rejecting duplicate-system proposals
- when reviewing whether an admitted project's role is drifting beyond its original classification

---

## Related Docs

- `new-project-onboarding-doctrine.md`
- `new-project-required-docs.md`
- `new-project-access-and-boundary-rules.md`
- `new-project-data-boundary-doctrine.md`
- `new-project-lifecycle-and-fitment-review.md` *(planned)*
- `../ecosystem/v-ecosystem-overview.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../governance/approval-and-escalation-model.md`
- `../project-v/project-v.md`
- `../veda/veda.md`
- `../v-forge/v-forge.md`
