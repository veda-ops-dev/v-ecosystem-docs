# Extension Agent Orchestration Model

## Purpose

This document defines how agent orchestration works inside the V Ecosystem VS Code extension.

It exists to answer:

```text
How does the extension coordinate bounded delegated work, what roles do orchestrator and specialist agents play, what authority limits apply, what visibility is required, and how does orchestration increase capability without creating a fourth peer ecosystem system or a hidden governance path?
```

This is a Tier 1 ecosystem authority document for the extension/runtime layer.

---

## Scope

This document governs:

- the runtime role of the agent orchestrator
- the runtime role of specialist agents
- the delegation model for bounded subtasks
- session-scope inheritance for delegated work
- current-system preservation during delegated work
- visibility and traceability requirements for orchestration
- task and subtask lifecycle posture
- cancellation, interruption, and failure posture
- approval and gating preservation under delegation
- anti-drift rules that prevent orchestration from becoming a shadow authority layer

This document assumes the active binding of:
- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-state-and-context-model.md`
- `extension-human-llm-interaction-model.md`
- `extension-vscode-surface-architecture.md`
- `../ecosystem/decisions/ADR-010-agent-orchestration-is-an-extension-runtime-capability.md`

---

## Out of Scope

This document does not define:

- the full memory and compaction doctrine
- transcript retention policy in full detail
- exact system-init message contents
- exact MCP tool schemas
- specific backend implementation classes or TypeScript files
- system-specific route contracts for Project V, VEDA, or V Forge
- whether every future workflow must use delegation

Those belong in continuity, tool-surface, implementation, or system-specific docs.

---

## System

- interfaces

---

## Core Rule

Agent orchestration is a bounded extension/runtime capability.

It exists to coordinate admitted work inside the extension so the LLM can operate with greater specialization, continuity, and runtime usefulness.

It does not:
- create a fourth peer ecosystem system
- create a new truth domain
- create a new approval path
- weaken current-system clarity
- convert delegated work into hidden governance

If orchestration makes the system feel more capable while making authority, approval, or ownership harder to understand, the orchestration design is wrong.

---

## Orchestration Definition

Agent orchestration is the extension-runtime coordination of bounded work through:

- an **agent orchestrator** that manages runtime flow
- optional **specialist agents** that perform narrowly scoped delegated subtasks
- explicit task and subtask lifecycle tracking
- operator-visible traceability of delegated work
- governed re-entry into the normal approval and activation path when required

The orchestrator is a runtime coordinator.
It is not a system of record.
It is not a planner, observatory, or executor in the ecosystem sense.

---

## Runtime Roles

### Agent Orchestrator

The orchestrator is the runtime role responsible for:

- deciding whether admitted work should remain single-threaded or be decomposed into subtasks
- assembling bounded context packets for delegated subtasks
- assembling or filtering the session tool surface for delegated work
- tracking task and subtask lifecycle state
- collecting specialist outputs
- packaging delegated outputs back into the parent interaction flow
- surfacing orchestration status to the operator
- stopping, cancelling, or escalating work when required by governance or runtime failure

The orchestrator is not allowed to:

- become an approval source
- self-authorize governed actions
- switch the current system silently
- treat specialist outputs as automatically authoritative
- hide delegated work from the operator when that work affects review or next-step decisions

### Specialist Agent

A specialist agent is a bounded runtime worker used for narrowly scoped delegated work.

Examples include:
- focused analysis
- bounded summarization
- evidence packaging
- record-family review
- cross-checking or consistency review
- formatting or packaging inert outputs

A specialist agent may increase reasoning specialization.
It does not gain independent authority by virtue of specialization.

A specialist agent must not:
- become its own approval authority
- widen its scope casually
- access tools outside the filtered delegated tool surface
- present its output as canonical system truth

---

## Delegation Rule

Delegation is allowed only for bounded subtasks with explicit scope.

A delegated subtask must have, at minimum:

- a defined objective
- a defined scope boundary
- a filtered context packet
- a filtered tool surface
- an expected output type
- a visible lifecycle state

Delegation must not be used as a vague escape hatch for "let another agent figure it out."

If the orchestrator cannot explain the delegated scope clearly, the subtask is not bounded enough to delegate.

---

## Meaningful Delegated Work Rule

Delegated work is **meaningful** when it does more than save internal runtime effort.

At minimum, delegated work is meaningful when it:
- produces outputs that the operator will review directly or indirectly
- changes what the parent interaction flow can now say, show, or recommend
- affects approval-sensitive preparation or review state
- introduces a failure, cancellation, or interruption state the operator may need to understand

Meaningful delegated work must be operator-visible.
It must not collapse into an anonymous spinner or disappear behind generic “thinking” language.

---

## Scope Inheritance Rule

All delegated work inherits the parent session scope.

This includes:
- project scope
- current-system posture
- active approval/gating posture
- current workflow stage relevance where applicable
- current evidence and decision-context boundaries

A specialist worker does not get a broader scope than the parent session.
Delegation may narrow scope. It must not widen it.

---

## Current System Preservation Rule

Orchestration must not blur which system is active.

If the current system is Project V, VEDA, or V Forge, delegated work remains subordinate to that current-system posture even when bounded read access to referenced-system material is admitted.

Delegated work may consume bounded referenced-system context where doctrine already allows it.
Delegated work must not silently convert cross-system reading into cross-system ownership.

The operator must remain able to tell which system governs the active activity at all times.

---

## Output Rule

Delegated work must return typed, bounded outputs.

Default delegated outputs should be treated as inert intermediate products such as:
- findings
- summaries
- consistency checks
- evidence packages
- warnings
- trace artifacts

A specialist output is not automatically a recommendation, approval request, activation event, or canonical record.

If delegated work contributes to a higher-class action, the result must re-enter the existing governance and gating path before anything active occurs.

---

## Governance Preservation Rule

Orchestration does not change action class rules.

If a Class B, C, or D action would require persisted approval without delegation, it still requires persisted approval with delegation.

Delegated work may prepare or package material for a later governed action.
Delegated work may not activate that action by coordinator convenience.

The coordinator is not an approval source.
The specialist is not an approval source.
Only the governed operator path remains the approval source where doctrine requires it.

---

## Approval-In-Flight Rule

When an approval gate is actively in-flight, orchestration must not behave as though the surrounding session remains unconstrained.

At minimum:
- approval gate state must be treated as protected context
- orchestration must not silently change the basis of the in-flight approval without surfacing that change
- a delegated task that materially affects the basis of the approval must force a visible review-required condition before approval continues
- orchestration may continue only in bounded ways that do not disturb the integrity of the in-flight approval posture

A running delegated task must not quietly mutate the review basis while the operator is inside a gate surface.

---

## Visibility and Traceability Rule

Orchestration must remain operator-visible.

The operator must be able to determine, where relevant:

- whether orchestration is active
- what delegated subtasks exist
- what state each subtask is in
- which specialist role is performing each subtask
- what outputs came from which delegated subtask
- when a subtask failed, was cancelled, or was interrupted
- whether a subtask is awaiting review or escalation

Delegated work must not become hidden just because the runtime finds it convenient.

If the operator cannot tell that the extension delegated meaningful work, the system is no longer reviewable enough.

---

## Task and Subtask Lifecycle Posture

Delegated work must use explicit lifecycle states.

At minimum, delegated runtime tasks should support:
- `pending`
- `running`
- `completed`
- `failed`
- `cancelled`

Additional states such as `awaiting_review` or `awaiting_escalation` may be added if needed, but lifecycle posture must remain explicit and reviewable.

The extension must not treat a vague spinner as sufficient lifecycle visibility for meaningful delegated work.

---

## Cancellation and Interruption Rule

The operator must be able to cancel meaningful delegated work.

The runtime must also be able to stop delegated work when:
- scope becomes invalid
- required context becomes stale or missing
- governance posture changes
- a task fails in a way that makes continuation illegitimate
- a delegated step reaches a point requiring operator review before proceeding

Cancellation, failure, and interruption must be reflected in the visible runtime state.
They must not disappear into logs only.

---

## Failure Rule

Delegated work failure must be surfaced honestly.

A failed specialist task must not be presented as partial success unless that partial success is explicitly characterized and reviewable.

When failure affects the integrity of the parent activity, the orchestrator must:
- surface the failure
- stop or downgrade the affected flow as appropriate
- preserve whatever traceability is needed for review
- avoid confidence theater

If the orchestrator cannot honestly characterize what failed and what remains valid, the runtime must not pretend otherwise.

---

## Anti-Drift Rules

### 1. No shadow system rule
Orchestration must not be described or implemented as though it were a fourth peer ecosystem system.

### 2. No hidden approval rule
A coordinator or specialist must not become a secret approval path.

### 3. No authority amplification by delegation
Delegation may increase specialization. It must not increase power.

### 4. No hidden system switching
Delegated work must not silently switch the current system or blur which system governs the active task.

### 5. No fake-authority outputs
Worker outputs, orchestration traces, and delegated findings must not be treated as canonical system state just because they are useful.

### 6. No orchestration-first implementation posture
The runtime must not become orchestration-heavy before the state/context spine, init/tool-surface discipline, and governance path are sound.

---

## Relationship to Other Extension Docs

This doc defines the orchestration model.

It relies on:
- `extension-llm-behavior-contract.md` for bounded LLM posture
- `extension-governance-and-gating-model.md` for action-class and approval rules
- `extension-state-and-context-model.md` for what state must remain visible
- `extension-human-llm-interaction-model.md` for how the operator encounters delegated work
- `extension-vscode-surface-architecture.md` for where orchestration state is surfaced
- `extension-memory-and-continuity-model.md` for protected context and continuity posture
- `extension-system-init-and-tool-surface-model.md` for session basis and delegated tool-surface posture

This doc must not be used to smuggle continuity doctrine, transcript doctrine, or tool-surface doctrine into an orchestration bucket just because those topics are adjacent.

---

## Implementation Direction

The implementation should make orchestration:
- explicit
- bounded
- cancellable
- reviewable
- subordinate to the existing governance spine

The implementation must not optimize for the illusion of autonomy at the expense of operator clarity.

If a more autonomous-feeling runtime requires hidden state, hidden approvals, or blurred ownership, that autonomy is not compatible with the V Ecosystem.
