# New Project Access and Boundary Rules

## Purpose

This document defines how access and boundary posture must be established for a new project before it is admitted into the V Ecosystem.

It exists to answer:

```text
What access can a new project have, what must it never have, and how do we ensure access follows role and boundary classification instead of convenience or implementation pressure?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- how access posture is defined during onboarding
- how cross-system boundaries must be respected by new projects
- what kinds of access are allowed, constrained, or forbidden
- how MCP and tool surfaces must be governed
- the anti-drift rules that prevent access expansion beyond classification

---

## Out of Scope

This document does not define:

- low-level auth implementation
- credentials or secrets management
- transport-layer protocols
- detailed MCP implementation

Those belong in implementation and infra docs.

---

## System

- onboarding

---

## Core Rule

Access must follow classification and data-boundary posture.

A project does not get access because:

- it would be convenient
- it can technically connect
- it shares infrastructure
- it was granted access during experimentation

If access is not justified by the project’s classified role and truth domain, it must not be granted.

---

## Access Definition

Access is any capability that allows a project to:

- read data from another system
- write data into another system
- trigger actions in another system
- expose or consume MCP/tool surfaces

Access is not neutral.
It is an extension of system power and must be governed accordingly.

---

## Access Categories

A project’s access posture must be defined across:

### 1. Read Access
What the project may observe.

### 2. Write Access
What the project may change.

### 3. Action Access
What the project may trigger.

### 4. Interface Access
What explicit interfaces it uses.

### 5. MCP / Tool Surface Access
What MCP or tool surfaces it exposes or consumes.

All five must be explicitly defined before admission.

---

## Read Access Rule

A project may only read data that is:

- relevant to its role
- consistent with its data-boundary posture
- explicitly allowed by the source system

Read access is scoped to data that directly serves the project’s classified truth domain and governed operations.
A project must not use read access to build aggregated views of other systems, to shadow-mirror another system’s data locally, or to create operational dependencies that effectively make the project a hub for data owned by multiple systems.

### Rule
Reading does not imply ownership.
Reading does not justify copying.
Reading does not justify expanding into the source system’s role.
If a project’s read pattern begins to resemble that of a second VEDA, a second Project V, or a second V Forge, the read access is out of bounds even if nothing is being written.

---

## Write Access Rule

Write access is high-risk and must be tightly constrained.

A project may only write when:

- its role requires it
- the receiving system allows it
- the interface is explicitly defined

### Rule
Default posture is no write access.
Write access must be justified, not assumed.

---

## Action Access Rule

Action access includes triggering workflows, pipelines, or system behaviors.

Action access is valid only when the triggered action is required for the project’s classified operational role and cannot reasonably be satisfied through a read or write path.

Examples of forbidden action-access patterns include:

- triggering planning state changes in Project V from a project that does not own planning truth
- triggering observatory operations in VEDA from a project that does not own observability truth
- triggering execution actions in V Forge from a project that does not own execution truth

### Rule
A project must not be able to trigger actions that effectively make it behave like the target system.
Action access that effectively grants control over another system’s core workflow belongs in that system, not in the accessing project.

---

## Interface Rule

All cross-system interaction must occur through explicit interfaces.

An explicit interface is one that is documented in the shared docs root and that names:

- the owning system
- the accessing system
- what crosses the boundary
- what does not cross
- what approval or governance conditions apply

A call to another system’s API is not an explicit interface in this sense unless it is backed by a shared-root interface doc.
Convenience integrations, shared configuration, shared infrastructure access, and undocumented API calls are not explicit interfaces regardless of how well they work technically.

### Rule
No hidden integration.
No implicit coupling.
No “it just works” connections.

---

## MCP and Tool Surface Rule

A project must explicitly define:

- what MCP surfaces it exposes
- what MCP surfaces it consumes
- what operations those surfaces allow
- what governance constraints apply

### Rule
MCP surfaces are not free capability expansion.
They must align with the project’s classified role and boundary.

---

## Forbidden Access Patterns

The following are forbidden:

- broad cross-system write access without explicit interface doctrine
- reading data outside the project’s truth domain for convenience
- shadow access through shared infrastructure
- using MCP surfaces to bypass boundary rules
- access granted during experimentation becoming permanent by inertia

---

## Access Drift Rule

Access must not expand silently over time.

New access means any access category or scope not explicitly covered by the project’s admission access posture, including:

- new read paths to previously inaccessible data
- new write targets
- new triggered action types
- new MCP surface operations

### Rule
If new access is required:

- it must be re-evaluated
- it must be documented
- it must be approved under governance

Re-evaluation follows the same governance path as original access approval under `../governance/approval-and-escalation-model.md`.
A project may not self-certify that expanded access falls within its existing approved posture.

---

## Access Revocation Rule

When classification changes or access is found to be excessive:

- access must be reduced or removed
- previous access does not persist by default

Revocation review is triggered when:

- a project is reclassified to a narrower role
- a boundary integrity violation is found
- access drift is discovered

### Rule
Revocation follows the same governance path as original access approval under `../governance/approval-and-escalation-model.md`.
A project may not resist revocation by asserting that accumulated usage has established legitimate access.

---

## Boundary Integrity Rule

A project must not behave like another system through access.

A project is functionally equivalent to another system when its access pattern allows it to:

- answer the questions that system is supposed to answer
- perform the operations that system is supposed to perform
- store the truth that system is supposed to own

This is true regardless of naming or framing.

Examples include:

- a project reading broad observability data from multiple systems until it functions like a second VEDA
- a project triggering planning mutations and maintaining planning continuity until it functions like a second Project V
- a project driving execution actions and execution-state control until it functions like a second V Forge

### Rule
If access makes a project functionally equivalent to another system, the boundary is broken.
When a boundary integrity violation is found, the access must be revoked or reduced and the project must be re-evaluated under the classification model. A boundary integrity violation does not resolve itself through accumulated usage.

---

## Human-In-The-Loop Principle

Access posture is governance-sensitive.

Human review may be required when:

- write access is requested
- action access is requested
- MCP surfaces expose new capabilities
- cross-system boundaries are extended
- boundary integrity appears to be at risk or already violated

---

## LLM Use Principle

A capable LLM should infer:

- access is constrained by role and ownership
- default is minimal access
- expansion requires justification and governance
- MCP is not a shortcut around boundaries

If a capable LLM reviewing a new project’s access posture cannot determine from shared-root docs what every access category covers and why it is justified by classification, the access posture is not documented well enough for admission.
If access expands faster than classification and doctrine, the system is drifting.

---

## Usage

Use this doc when:

- defining the access posture for a new project during onboarding
- reviewing whether a proposed cross-system read, write, action, or MCP access is justified by classification
- evaluating whether an admitted project’s access has drifted beyond its original posture
- initiating access revocation or reduction after reclassification or boundary integrity violation
- writing the new project’s own access and boundary rules doc

---

## Related Docs

- `new-project-onboarding-doctrine.md`
- `new-project-classification-model.md`
- `new-project-required-docs.md`
- `../ecosystem/cross-system-boundaries.md`
- `../governance/approval-and-escalation-model.md`
