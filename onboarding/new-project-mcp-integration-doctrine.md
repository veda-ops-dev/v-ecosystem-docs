# New Project MCP Integration Doctrine

## Purpose

This document defines how MCP integration posture must be established for a new project before it is admitted into the V Ecosystem.

It exists to answer:

```text
When may a candidate new project expose or consume MCP surfaces, what must be true before those surfaces are allowed, and what rules prevent MCP integration from becoming a shortcut around project classification, interface doctrine, access posture, or governance?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- how MCP integration posture is defined during onboarding
- what MCP roles a candidate project may have before admission
- what must be explicit before MCP exposure or MCP consumption is allowed
- how MCP surfaces relate to project classification, access posture, interface doctrine, and governance
- the anti-drift rules operators and LLMs must preserve when evaluating MCP fitment for a new project

---

## Out of Scope

This document does not define:

- low-level MCP protocol mechanics
- transport implementation details
- secrets management
- repo-local implementation architecture
- post-admission operational workflow design for an admitted project

Those belong in implementation, infra, interface, and project-local docs.

---

## System

- onboarding

---

## Core Rule

MCP integration follows project classification.

A candidate project does not get MCP surfaces because:

- a tool exists
- an interface would be convenient
- implementation wants a faster path
- an LLM could theoretically use the surface
- another project already exposes MCP

If the project’s role, truth domain, access posture, interface needs, and governance posture are not explicit first, MCP integration is not ready.

---

## MCP Integration Definition

For onboarding purposes, MCP integration means any governed posture by which a candidate project:

- exposes MCP surfaces to other systems, operators, or agents
- consumes MCP surfaces from other systems
- relies on MCP-mediated actions, reads, writes, or coordination to perform its admitted role

MCP is an integration surface.
It is not a substitute for role clarity, interface doctrine, or approval posture.

---

## MCP Admission Principle

A candidate project must not be admitted on the basis that MCP will explain the role later.

MCP integration is downstream of:

- role classification
- truth-domain classification
- access and boundary posture
- required doctrine identification
- interface clarity where cross-system interaction is live at admission time

If MCP is doing the conceptual work that doctrine should have done, onboarding has failed.

---

## Why This Doctrine Exists

MCP surfaces can create the appearance of clean integration while hiding major doctrine gaps.

This doctrine exists to prevent:

- MCP-first project admission
- tool exposure before role clarity
- hidden action authority through MCP surfaces
- undocumented cross-system interaction disguised as tooling
- candidate projects being admitted as wrappers around capabilities instead of bounded truth owners
- access expansion through MCP convenience

A project with unclear MCP posture is often a project with unclear boundary posture.

---

## MCP Role Categories

A candidate project’s MCP posture must be classified explicitly.

The candidate may be one or more of the following, if justified:

### 1. MCP Consumer
The project consumes bounded MCP surfaces exposed by other governed systems.

### 2. MCP Provider
The project exposes bounded MCP surfaces that allow governed reads, writes, actions, or other operations aligned to its role.

### 3. MCP Non-Participant
The project does not expose or consume MCP as part of admission posture.

### Rule
A candidate must not be treated as an MCP participant by default.
No MCP role is the default role.
MCP fitment must be explicit.

---

## Preconditions for MCP Exposure or Consumption

Before a candidate project may expose or consume MCP surfaces as part of admission posture, all of the following must be explicit:

- the project’s classified role
- the project’s truth domain
- the project’s non-ownership boundaries
- the project’s access posture
- the relevant cross-system interface posture where live interaction is required
- the governance posture for approval-sensitive MCP-mediated operations

If any of those remain materially unclear, MCP posture is not admission-ready.

---

## MCP Consumer Rule

A candidate project may consume MCP surfaces only when:

- the consumed surface is relevant to the candidate’s classified role
- the consumed capability is consistent with the candidate’s access posture
- the source surface is governed by the exposing system
- the cross-system interaction does not create ownership blur

### Rule
Consuming MCP does not grant ownership.
Consuming MCP does not justify storing another system’s truth as local canonical truth.
Consuming MCP does not justify bypassing the source system’s interface doctrine.

If a candidate project’s MCP consumption pattern would make it functionally behave like another system, the candidate’s MCP posture is out of bounds.

---

## MCP Provider Rule

A candidate project may expose MCP surfaces only when:

- the exposed operations are aligned to the project’s classified role
- the exposed operations do not exceed the project’s admitted authority
- the surface does not grant hidden cross-system power that the docs have not justified
- the surface can be understood through explicit doctrine rather than implementation inference

### Rule
An MCP surface must not expose broader power than the project itself is allowed to have.
A project must not become a governance bypass layer by wrapping restricted actions in a convenient MCP surface.

---

## MCP Non-Participant Rule

A candidate project may be admitted with no MCP role at all.

### Rule
A project does not need MCP exposure or consumption merely because the ecosystem uses MCP elsewhere.
MCP absence is valid when it better preserves boundary clarity or when the project’s role does not require tool-surface participation at admission time.

---

## MCP and Interface Doctrine Rule

MCP does not replace interface doctrine.

When a candidate project would use MCP for live cross-system interaction at admission time, the underlying interaction must still be explainable in shared-root doctrine as:

- who owns the source truth
- who is consuming or acting
- what crosses the boundary
- what does not cross the boundary
- what approval or governance posture applies

### Rule
An MCP endpoint name, tool name, or implementation contract is not enough.
If the cross-system meaning of the interaction is undocumented, the MCP integration is not doctrine-valid.

---

## MCP and Access Posture Rule

MCP operations must remain inside the candidate project’s approved access categories.

This includes:

- read operations
- write operations
- action-triggering operations
- coordination operations

Coordination operations must be classified under one of the governing access categories defined in `new-project-access-and-boundary-rules.md`.
"Coordination" is not an additional access category.
It is a description of purpose that does not change the underlying access classification.
MCP posture verification is part of the admission checklist's access posture completeness check defined in `new-project-admission-checklist.md`.

### Rule
MCP must not be used to smuggle in broader access than the project’s access and boundary posture allows.
An operation exposed through MCP is still read access, write access, action access, or interface access in doctrine terms and must be governed accordingly.

---

## MCP and Governance Rule

MCP integration does not downgrade approval requirements.

If an operation would require:

- human review
- escalation
- explicit authorization
- bounded approval posture

outside MCP, it still requires that same governance posture when surfaced through MCP.

### Rule
A candidate project must not be admitted with an MCP design that assumes tool invocation is self-justifying permission.
Tool path does not outrank governance path.

---

## Required MCP Admission Questions

Before MCP posture is considered admission-ready, onboarding must be able to answer at least these questions:

- does this project need MCP at admission time at all?
- is it an MCP consumer, provider, both, or neither?
- what role-justified operations are exposed or consumed?
- what systems are on the other side of those operations?
- what truth remains owned by the source system?
- what access category does each operation belong to?
- what governance posture applies to approval-sensitive operations?
- what doctrine explains the interaction if a later LLM needs to reconstruct it?

If those questions cannot be answered explicitly, the project’s MCP posture is not ready.

---

## Forbidden MCP Patterns

The following are forbidden during onboarding and admission:

- exposing MCP surfaces before role classification is stable
- using MCP as the reason the project should exist
- using MCP to bypass interface doctrine
- using MCP to bypass access review
- using MCP to bypass approval posture
- using MCP to turn a candidate project into a hidden planner, hidden observability layer, or hidden execution layer
- admitting a project whose primary identity is merely being an MCP wrapper around another system’s powers

### Rule
If MCP convenience is doing boundary-erasing work, the candidate is not ready for admission.

---

## MCP Drift Rule

MCP posture must not expand silently after admission planning begins.

Examples of expansion include:

- new consumed surfaces
- new exposed operations
- new write or action capabilities through an existing surface
- new cross-system coordination responsibilities through MCP

### Rule
If MCP scope expands beyond what onboarding established, the expansion must be re-evaluated, documented, and approved under the same governance posture that would apply to equivalent non-MCP access expansion.
A project may not self-certify that MCP growth is merely implementation detail when the effective authority or access surface has expanded.

---

## Admission Blocking Conditions

A candidate project is not ready for admission when:

- MCP need is asserted but the role is still unclear
- MCP surfaces are proposed but access categories are undefined
- MCP-mediated cross-system interaction exists but no interface meaning is documented
- MCP operations would effectively give the project another system’s core role
- governance-sensitive operations are presented as safe merely because they are surfaced as tools

### Rule
MCP ambiguity is admission ambiguity.
If the MCP posture is load-bearing and unclear, admission must not proceed.

---

## Human-In-The-Loop Principle

MCP posture is governance-sensitive because it can expand what a project can do and what agents can trigger.

Human review may be required when:

- a candidate wants MCP write or action capability
- MCP would expose new cross-system power
- MCP would surface approval-sensitive operations
- the candidate’s MCP posture appears to blur system boundaries
- there is doubt about whether MCP participation is truly required at admission time

A candidate project must not be admitted with unresolved doubt about a load-bearing MCP posture.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- MCP follows role and boundary doctrine rather than replacing it
- a candidate project may be a provider, consumer, both, or neither, but not by default
- MCP-mediated actions remain governed by the same access and approval rules as non-MCP actions
- undocumented MCP interaction is still undocumented cross-system behavior
- MCP convenience must not be allowed to create hidden system-role duplication

If an LLM could read the onboarding docs and conclude that “MCP exists, therefore the project can probably do it,” this doctrine is failing.

---

## Usage

This document should be used:

- when deciding whether a candidate new project needs MCP participation at admission time
- when defining whether the candidate is an MCP provider, consumer, both, or neither
- when reviewing whether proposed MCP surfaces are aligned to classification, access posture, and governance
- when rejecting MCP-first candidate projects that lack a real bounded system role
- when deciding whether a proposed MCP expansion is actually an access or authority expansion requiring re-evaluation

---

## Related Docs

- `new-project-onboarding-doctrine.md`
- `new-project-classification-model.md`
- `new-project-required-docs.md`
- `new-project-access-and-boundary-rules.md`
- `new-project-data-boundary-doctrine.md`
- `new-project-lifecycle-and-fitment-review.md`
- `new-project-admission-checklist.md`
- `../ecosystem/cross-system-boundaries.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/agent-operating-doctrine.md`
