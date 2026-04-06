# Desktop Tool-Surface Implementation Design

## Purpose

This document defines the mechanical implementation design for the desktop tool surface in the V Ecosystem.

It exists to answer:

```text
How should the desktop application construct, filter, refresh, and enforce the active tool surface so the runtime only receives the tools it is currently entitled to use under system, scope, governance, and delegation constraints?
```

This is a Tier 3 implementation companion document.
It is subordinate to the active authority in:

- `desktop-system-init-and-tool-surface-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-state-and-context-model.md`
- `runtime-sidecar-and-nerve-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`

If this document conflicts with those docs, this document is wrong.

---

## Scope

This document governs:

- tool registry mechanics
- tool metadata needed for structural filtering
- session-scoped tool-surface assembly
- current-system and referenced-system filtering mechanics
- project-scope filtering mechanics
- action-posture filtering mechanics
- delegated tool-surface narrowing mechanics
- refresh and invalidation mechanics for the active tool surface
- runtime enforcement posture for tool execution

---

## Out of Scope

This document does not define:

- the final doctrine for tool-surface entitlement
- the canonical meaning of current system or referenced system
- the final MCP schemas for every tool
- detailed UI rendering of tool lists or controls
- the full approval semantics for every system-specific action

Those belong in higher-authority docs or more specific implementation docs.

---

## System

- interfaces

---

## Core Rule

The active tool surface must be assembled deliberately and enforced structurally.

The runtime must only expose tools that are currently in-bounds for:

- the active system posture
- the active project scope
- the current governance and action posture
- the current delegated-runtime posture

If the runtime exposes tools outside those bounds and relies on the LLM to behave correctly anyway, the implementation is wrong.

---

## Relationship to Existing Authority

This document does not create new doctrine for tool entitlement.
It operationalizes existing doctrine.

In particular, it assumes and must obey the active authority already defined for:

- session tool-surface assembly
- absent-affordance enforcement
- current-system posture
- referenced-system read posture
- delegated runtime narrowing
- current runtime scope
- approval-sensitive action handling

This document defines how those rules are enforced mechanically.

---

## Tool-Surface Lifecycle Overview

The active tool surface should be treated as a runtime-built, invalidation-sensitive artifact with the following lifecycle:

1. **tool registration**
2. **candidate surface collection**
3. **current-session context binding**
4. **structural filtering**
5. **active surface publication**
6. **runtime execution enforcement**
7. **refresh / invalidation / rebuild**

The active surface is not static configuration.
It is a governed runtime product of the current session basis.

---

## Tool Registry Mechanics

The runtime should maintain an explicit registry of known tools rather than constructing tool lists ad hoc from whatever happens to be reachable.

### Registry Role

The registry exists to provide:

- canonical tool identity within the runtime
- tool metadata needed for filtering
- deterministic session-surface assembly
- deterministic execution enforcement

### Minimum Registry Requirements

Every registered tool should expose enough metadata for the runtime to determine whether it belongs in the current session surface.

At minimum, a registered tool should carry:

- stable tool identifier
- display name and description
- owning system classification
- read / write / governance-sensitive posture
- project-scope requirements, if any
- whether it is cross-system-readable
- whether it is delegation-admissible
- execution adapter or dispatcher binding

### Hard Rule

A tool must not become available in session merely because it is installed, reachable, or technically callable.
Registry presence is not exposure permission.

---

## Tool Metadata Requirements

To enforce absent-affordance doctrine structurally, the runtime must classify tools in a way the filter pipeline can use deterministically.

### Minimum Classification Dimensions

At minimum, the runtime should classify each tool by:

- **owning system**
  - ecosystem
  - project-v
  - veda
  - v-forge

- **access posture**
  - read-only
  - bounded mutation
  - governance-sensitive mutation

- **scope posture**
  - global/runtime-level
  - project-scoped
  - session-scoped
  - task-scoped

- **cross-system posture**
  - current-system only
  - referenced-system read-allowed
  - broader runtime support tool

- **delegation posture**
  - parent-only
  - delegable with narrowing
  - non-delegable

### Why This Matters

Without classification dimensions like these, filtering becomes a pile of ad hoc conditions and the active surface becomes impossible to reason about.

---

## Candidate Surface Collection

At surface-build time, the runtime should collect candidate tools from the registry rather than immediately publishing the full registry.

The candidate set is only the raw input to filtering.
It is not the final active surface.

### Inputs to Candidate Collection

At minimum, the runtime should know:

- the current system posture
- the current project scope token, if any
- referenced-system state, if any
- current workflow or runtime stage where relevant
- current governance and action posture
- whether the session is parent, delegated, or resumed

---

## Current-Session Context Binding

Before structural filtering begins, the runtime should bind the current session basis to the surface-build pipeline.

### Minimum Bound Context

At minimum, the filter pipeline should receive:

- active system
- active project scope
- referenced systems currently admitted into the session
- active action posture or gating posture
- delegated and runtime role posture
- current operator-visible scope warnings, if any

This prevents the active surface from being built in isolation from the actual session basis.

---

## Structural Filtering

The active surface must be produced through explicit structural filtering stages.

A reasonable filtering pipeline is:

1. **system ownership filter**
2. **project-scope filter**
3. **referenced-system posture filter**
4. **action-posture / governance filter**
5. **delegation filter**
6. **final publication filter**

Each stage exists for a different reason.
They should not be collapsed into one opaque allowed function if doing so makes the runtime harder to reason about.

---

## System Ownership Filter

The first meaningful filter should remove tools that do not belong in the active system posture.

### Required Behavior

If the current session is operating in one current system posture, the default rule is:

- tools owned by the current system may proceed to later filters
- tools owned by non-current systems do not proceed unless another doctrinally valid posture explicitly admits them

### Why First

Current-system clarity is one of the strongest anti-drift constraints in the desktop model.
The runtime should not even consider wrong-system tools as normal candidates unless the session basis explicitly allows referenced-system visibility.

---

## Referenced-System Posture Filter

Where the higher-authority docs allow referenced-system visibility, the runtime may admit a narrower set of non-current-system tools.

### Required Behavior

Referenced-system admission should be narrower than current-system admission.

As a default implementation posture:

- current-system tools may remain eligible for full later filtering
- referenced-system tools should be admitted only where the current doctrine allows read posture
- non-referenced wrong-system tools should be excluded entirely

### Hard Rule

Referenced-system admission must not silently widen into wrong-system mutation capability.

If a tool belongs to a referenced system and mutation is not explicitly allowed by doctrine, it must not appear as an active tool.

---

## Project-Scope Filter

After system-level posture is evaluated, the runtime must enforce project-scope binding.

### Required Behavior

A project-scoped tool must not appear in the active surface unless its scope requirements are satisfied by the current session basis.

### Examples of Required Exclusion

The runtime should exclude tools when:

- no project scope is active but the tool requires one
- the tool targets a different project scope than the current bound scope
- delegated work has a narrower scope token than the parent session and the tool exceeds that narrower scope

### Why This Matters

Tool exposure is one of the easiest ways for scope confusion to turn into real drift.
The active surface must not allow a tool to imply that current scope is broader than it really is.

---

## Action-Posture / Governance Filter

The tool surface must reflect the current governance posture, not just technical capability.

### Required Behavior

A tool may be technically callable yet still be absent from the active surface because the current action posture does not permit it.

The filter should account for distinctions such as:

- read-support posture
- recommendation and support posture
- bounded write posture
- approval-sensitive mutation posture

### Important Rule

Tool availability is not equivalent to approval.

Even when a tool is present in the active surface, its actual execution may still require runtime enforcement and or operator review.
But the active surface should not include tools that are clearly out of bounds for the current posture.

### Why Structural Filtering Still Matters

It is not enough to say the permission check will stop it later.
Absent-affordance doctrine requires that obviously wrong tools be absent before the LLM reasons over them.

---

## Delegation Filter

Delegated sessions must receive a narrowed surface, not a copied parent surface.

### Required Behavior

If the session is delegated:

- the child surface must be derived from the parent surface
- the child surface must be narrowed to the delegated scope
- non-delegable tools must be removed
- governance-sensitive tools that exceed delegated posture must be removed

### Hard Rule

Delegation must not widen authority.
A delegated tool surface must never be broader than the eligible parent surface for the same scope and posture.

### Design Requirement

The runtime should model delegation filtering as an explicit stage, not as an accidental side effect of general filtering.
That makes testing and doctrine review much easier.

---

## Final Publication Filter

Before the active tool surface is published to the runtime and system-init layer, the runtime should run a final sanity filter.

### Purpose

This stage exists to catch any contradictions that survived earlier stages, such as:

- wrong-system mutators surviving referenced-system posture
- cross-scope tools surviving delegation narrowing
- governance-sensitive tools surviving a read-only posture

### Publication Output

The published active surface should be a deterministic artifact that can be:

- exposed to the LLM
- summarized for operator visibility
- compared against prior surface versions for refresh tracking

---

## Active Surface Publication

Once filtering completes, the runtime should publish the active surface as a current session artifact.

### Published Surface Should Support

At minimum:

- LLM-visible tool definitions
- operator-visible summary of active tool posture
- internal enforcement metadata for execution checks
- surface version or revision identifier for refresh tracking

### Important Rule

The published surface should be treated as part of the current runtime basis, not as a hidden implementation detail.
If the active surface changes materially, that is a session-basis change and may require system-init refresh.

---

## Runtime Execution Enforcement

Filtering the visible surface is not enough.
Execution must still be enforced at call time.

### Required Rule

Every execution request should be checked against the active published surface and current runtime basis at execution time.

### Why

The session basis may have changed after the surface was built.
A stale or bypassed active surface must not allow an out-of-bounds call through.

### Minimum Execution Checks

At execution time, the runtime should verify:

- tool is present in the currently active published surface
- current system posture still allows the tool
- current scope still allows the tool
- current governance and action posture still allows the tool
- delegated posture has not narrowed since the tool was published

### Hard Rule

Execution enforcement is a second gate, not the first gate.
The first gate is structural absence.
The second gate is runtime call validation.
Both are required.

---

## Refresh and Invalidation Mechanics

The active surface must be rebuilt when the session basis changes materially.

### Rebuild Triggers

The canonical enumeration of events that change the session basis — and their full per-surface, LLM, and sequencing consequences — is defined in `desktop-invalidation-and-refresh-matrix.md`. This section defines which of those session-basis changes require a tool-surface rebuild specifically. It does not define the events themselves or their broader propagation.

At minimum, the runtime should rebuild the active surface when any of the following changes materially:

- current system posture
- project scope token
- referenced-system set
- active action / approval posture
- delegated task scope
- parent/child runtime role posture
- tool registry version or registration set
- meaningful compaction event that changes the session basis or protected-context snapshot

### Why This Matters

A tool surface built for one session basis is not automatically safe for a different one.
The runtime must treat the surface as invalidatable.

### Refresh Relationship to System Init

A material active-surface rebuild may require:

- system-init partial re-assembly
- operator-visible surface update
- updated runtime-basis summary

---

## Suggested Runtime Structure

A reasonable implementation split would separate the following concerns:

### 1. Tool Registry
Owns registered tool metadata and dispatcher bindings.

### 2. Session Surface Builder
Collects candidates and binds current session context.

### 3. Structural Filter Pipeline
Runs system, scope, posture, referenced-system, and delegation filters in explicit order.

### 4. Active Surface Publisher
Publishes the final deterministic active surface to runtime consumers.

### 5. Execution Gate
Validates runtime calls against the active surface and current session basis.

### 6. Surface Refresh Coordinator
Rebuilds the active surface when invalidation triggers occur.

This split is preferred over a single giant permission function because it keeps absent-affordance, scope, governance, and delegation logic legible.

---

## Operator Visibility Requirements

The operator should be able to understand the broad posture of the active tool surface.

At minimum, implementation should support visibility for:

- current-system tool posture
- whether referenced-system read posture is active
- whether delegated narrowing is active
- whether tool refresh occurred
- whether the active surface is in a restricted or review-sensitive posture

The operator does not need a noisy dump of every raw internal filter step, but the runtime must not hide that the surface is being materially constrained.

---

## Anti-Drift Constraints

Implementation must not drift into any of the following:

- publishing the full registry and hoping execution checks are enough
- letting referenced-system visibility silently become mutation availability
- treating tool presence as authority or approval
- copying parent tool surfaces into delegated sessions without narrowing
- letting registry convenience erase current-system clarity
- rebuilding the surface invisibly when the operator should understand posture changed
- reducing structural filtering to a generic permission yes/no that hides why tools were excluded

---

## Usage

This document should be used:

- when implementing the runtime tool registry and surface builder
- when designing absent-affordance enforcement in the desktop runtime
- when reviewing whether delegated runtime mechanics are widening tool access incorrectly
- when validating that tool exposure remains subordinate to doctrine rather than replacing it

---

## Related Docs

- `desktop-system-init-and-tool-surface-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-state-and-context-model.md`
- `desktop-memory-and-continuity-model.md`
- `runtime-sidecar-and-nerve-model.md`
- `desktop-invalidation-and-refresh-matrix.md` — canonical event-to-consequence mapping; the rebuild triggers in this doc are the tool-surface layer's response to the session-basis-changing events defined there
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
