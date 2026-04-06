# Desktop Task Lifecycle Implementation Design

## Purpose

This document defines the mechanical implementation design for task lifecycle handling in the V Ecosystem desktop runtime.

It exists to answer:

```text
How should the desktop application represent, track, surface, and control runtime tasks so multi-step operations, delegated work, and long-running flows remain visible, cancellable, attributable, and non-authoritative?
```

This is a Tier 3 implementation companion document.
It is subordinate to the active authority in:

- `desktop-agent-orchestration-model.md`
- `desktop-state-and-context-model.md`
- `desktop-memory-and-continuity-model.md`
- `desktop-system-init-and-tool-surface-model.md`
- `runtime-sidecar-and-nerve-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/report-structure-and-required-fields.md`

If this document conflicts with those docs, this document is wrong.

---

## Scope

This document governs:

- runtime task representation
- task lifecycle states and transitions
- task attribution and source labeling
- task visibility requirements
- cancellation and cleanup posture
- delegated task handling
- task output posture
- task event publication
- task and runtime relationship to orchestration state
- anti-drift constraints for task handling

---

## Out of Scope

This document does not define:

- canonical execution truth in V Forge
- final orchestration doctrine
- final UI layout of task panels
- exact backend queueing technology
- worker memory-sync doctrine
- approval semantics beyond current authority docs

Those belong in higher-authority or more specific runtime docs.

---

## System

- interfaces

---

## Core Rule

Tasks are runtime coordination artifacts.

They exist to make multi-step work, delegated work, and long-running runtime operations visible and controllable.
They do not create canonical state.
They do not create decisions.
They do not create approvals.
They do not become execution truth merely because they are tracked cleanly.

If task state starts behaving like the real system of record, the implementation is wrong.

---

## Relationship to Existing Authority

This document does not create new doctrine for orchestration, approvals, or continuity.
It operationalizes runtime task handling under the posture already defined elsewhere.

In particular, it assumes and must obey the active authority already defined for:

- delegated runtime narrowing
- worker outputs as non-authoritative findings
- operator visibility requirements
- continuity artifact posture
- runtime-basis refresh and synchronization

This document defines how task artifacts are represented and managed mechanically.

---

## Task Lifecycle Overview

The runtime should treat tasks as explicit bounded objects that move through a controlled lifecycle.

A reasonable lifecycle is:

1. **task creation**
2. **queued / pending state**
3. **running state**
4. **terminal state**
5. **output preservation / publication**
6. **review, dismissal, or cleanup**

Tasks should not be modeled as invisible side effects hiding behind generic spinners.

---

## Task Representation

The runtime should maintain an explicit task model rather than treating long-running work as anonymous async operations.

### Minimum Task Fields

At minimum, a task record should carry:

- stable task identifier
- task type or classification
- task title or summary
- session lineage identifier
- project scope token or project identifier
- current system posture
- parent task identifier, if delegated or nested
- lifecycle state
- created timestamp
- started timestamp, if running
- ended timestamp, if terminal
- attribution and source metadata
- non-authority classification

### Why This Matters

Without explicit task representation, the runtime cannot surface orchestration state honestly or keep delegated work attributable.

---

## Task Types

The runtime should classify tasks into types relevant to the desktop application instead of importing generic CLI-oriented task categories blindly.

### Example Task Classes

Examples may include:

- analysis task
- retrieval task
- report-generation task
- orchestration or delegation task
- bounded runtime-maintenance task
- review-required task

The exact final taxonomy may evolve, but tasks should be typed strongly enough that visibility, narrowing, and cleanup behavior do not depend on guessing.

---

## Lifecycle States

The runtime should use explicit lifecycle states instead of vague in-progress flags.

### Minimum States

At minimum, tasks should support states such as:

- `pending`
- `running`
- `completed`
- `failed`
- `cancelled`
- `awaiting_review` where relevant

### Terminal States

At minimum, `completed`, `failed`, and `cancelled` should be terminal states.

### Important Rule

A task in terminal state must not silently accept further runtime updates as though it were still active.

---

## State Transition Rules

Task transitions should be explicit and constrained.

### Required Posture

The runtime should only allow valid state transitions such as:

- `pending -> running`
- `running -> completed`
- `running -> failed`
- `running -> cancelled`
- `running -> awaiting_review` where review handoff is required
- `awaiting_review -> completed` or other bounded terminal or continued posture where doctrine permits

### Why This Matters

Loose task-state mutation creates fake visibility. The operator thinks the runtime is tracking meaningful lifecycle, but the actual transitions are arbitrary.

---

## Attribution and Source Labeling

Every meaningful task must preserve where it came from.

### Minimum Attribution

At minimum, task attribution should support:

- created-by source, such as operator action, runtime trigger, or delegated coordinator
- delegated worker identifier, if relevant
- parent task and session linkage
- current system posture at creation
- current project scope at creation

### Hard Rule

Task attribution must not be flattened away for convenience.
A delegated task that loses its delegated identity becomes much harder to review safely.

---

## Non-Authority Classification

Tasks and task outputs must remain explicitly non-authoritative unless separately persisted through the proper canonical path.

### Required Posture

The runtime should make clear that:

- task state is runtime state
- task output is not canonical by default
- task completion is not approval
- task completion is not record activation

### Why This Matters

A clean task tracker can easily create the illusion that work being done in runtime is the same thing as work being canonically resolved. That illusion must be blocked.

---

## Task Output Posture

Tasks may produce useful outputs, but those outputs must remain classified correctly.

### Allowed Output Roles

Task outputs may function as:

- findings
- intermediate results
- review material
- runtime diagnostics
- operator-facing summaries

### Forbidden Promotion

Task outputs must not silently become:

- evidence records
- approval records
- canonical execution records
- governing decisions

### Delegated Output Rule

If a delegated task produces output, that output must remain visibly attributable to the delegated source until or unless it is promoted through the proper governed path.

---

## Visibility Requirements

Task handling must remain operator-visible when materially relevant.

### Minimum Visibility

Where task participation matters, the operator should be able to determine:

- what tasks currently exist
- what state each meaningful task is in
- whether delegated work is active
- whether any task is blocked, failed, cancelled, or awaiting review
- whether task outputs contributed to current continuity or runtime basis

### Important Rule

Meaningful tasks must not collapse into generic loading indicators when that would hide runtime reality from the operator.

---

## Cancellation and Cleanup

The runtime should support bounded task cancellation and cleanup.

### Required Posture

Where cancellation is supported, the runtime should:

- move the task into `cancelled`
- stop accepting normal forward progress updates
- record cancellation timestamp
- preserve relevant task history for audit and review posture
- release runtime resources where applicable

### Important Distinction

Cancellation is a runtime event.
It is not a canonical rollback unless the proper system of record separately records one.

---

## Task Event Publication

The runtime should publish task events as structured events rather than hiding them inside generic session logs.

### Minimum Event Types

At minimum, task event publication should support:

- task created
- task started
- task state changed
- task output updated or published
- task cancelled
- task failed
- task review required
- task terminal cleanup completed

### Why This Matters

Structured events make it much easier to:

- synchronize task panels
- update orchestration state
- preserve audit and review clarity
- test lifecycle handling independently

---

## Relationship to Orchestration State

Task lifecycle handling should feed visible orchestration state without replacing orchestration doctrine.

### Required Relationship

Task state may provide runtime evidence of:

- active delegated work
- pending review handoffs
- failed or cancelled subtasks
- active runtime coordination load

### Important Rule

Task handling provides mechanics.
It does not define whether orchestration is allowed or what governance posture a worker has. That comes from the orchestration doctrine.

---

## Relationship to Continuity

Tasks may contribute to continuity, but task state itself is not continuity authority.

### Allowed Relationship

Task outputs or terminal summaries may be admitted as continuity artifacts only under the existing continuity doctrine.

### Forbidden Relationship

The runtime must not assume that because a task completed, its output automatically becomes durable memory or canonical current truth.

---

## Refresh and Synchronization

Task surfaces must remain synchronized with the current session basis.

The full desktop-wide consequences of delegated task completion, failure, and cancellation — per-surface behavior, LLM consequences, blocking posture, and sequencing — are defined in `desktop-invalidation-and-refresh-matrix.md` (EVENT-12 — Delegated Task Completed with admitted findings; EVENT-13 — Delegated Task Failed or Cancelled). This section defines the task-surface refresh posture that supports those consequences. It does not define the broader event consequences or their cross-surface propagation.

### Refresh Triggers

At minimum, the runtime should refresh visible task posture when:

- a task is created
- a task changes lifecycle state
- delegated review becomes required
- task output is published into the current session basis
- the active session basis refreshes materially
- a task is cancelled or fails

### Important Rule

If task state changes materially, orchestration visibility and any related continuity visibility must refresh accordingly.

---

## Suggested Runtime Structure

A reasonable implementation split would separate the following concerns:

### 1. Task Model / Registry
Owns explicit task records and lifecycle metadata.

### 2. Task State Machine
Validates legal state transitions and terminal-state behavior.

### 3. Task Event Publisher
Publishes structured lifecycle events to dependent runtime surfaces.

### 4. Task Output Publisher
Handles bounded publication of task outputs without promoting them to authority.

### 5. Cancellation / Cleanup Controller
Stops, marks, and cleans up runtime tasks responsibly.

### 6. Task Visibility Surface Adapter
Feeds orchestration and task visibility surfaces with synchronized state.

This split is preferred over burying task state inside generic orchestration code because lifecycle, attribution, outputs, and cleanup have different anti-drift risks.

---

## Anti-Drift Constraints

Implementation must not drift into any of the following:

- treating runtime task completion as canonical completion
- flattening delegated task attribution away
- hiding meaningful runtime work behind generic loading indicators
- letting terminal tasks continue receiving silent updates
- treating task outputs as evidence or decisions by default
- collapsing task state and orchestration doctrine into one ambiguous blob
- using cancellation language that implies canonical rollback when none occurred

---

## Usage

This document should be used:

- when implementing task and state tracking for long-running runtime work
- when designing orchestration and task visibility surfaces
- when wiring delegated work into bounded lifecycle tracking
- when reviewing whether task outputs are being promoted incorrectly
- when adding cancellation and cleanup behavior to runtime tasks

---

## Related Docs

- `desktop-agent-orchestration-model.md`
- `desktop-state-and-context-model.md`
- `desktop-memory-and-continuity-model.md`
- `desktop-transcript-persistence-design.md`
- `runtime-sidecar-and-nerve-model.md`
- `desktop-invalidation-and-refresh-matrix.md` — canonical event-to-consequence mapping; EVENT-12 and EVENT-13 define the full desktop consequences of delegated task completion, failure, and cancellation that this doc's lifecycle mechanics feed into
- `../governance/agent-operating-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
