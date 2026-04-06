# Extension Token and Cost Tracking Design

## Purpose

This document defines the mechanical implementation design for token, context-pressure, and cost tracking in the V Ecosystem extension runtime.

It exists to answer:

```text
How should the extension measure, accumulate, surface, and react to token usage, context pressure, and runtime cost so operators can understand session consumption without turning budget mechanics into fake authority or hidden gating?
```

This is a Tier 3 implementation companion document.
It is subordinate to the active authority in:

- `extension-state-and-context-model.md`
- `extension-system-init-and-tool-surface-model.md`
- `extension-memory-and-continuity-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`

If this document conflicts with those docs, this document is wrong.

---

## Scope

This document governs:

- token accumulation mechanics
- context-pressure tracking
- cost accumulation mechanics
- usage event publication
- operator-visible usage posture
- threshold and warning posture
- relationship between token pressure and compaction readiness
- refresh behavior for usage surfaces
- anti-drift constraints for cost-aware runtime behavior

---

## Out of Scope

This document does not define:

- provider billing policy
- final UI styling for cost displays
- model-selection policy
- approval thresholds for external spend beyond current governance docs
- detailed per-provider pricing tables
- exact persistence backend for usage analytics

Those belong in provider wiring, operator surface, or governance docs.

---

## System

- interfaces

---

## Core Rule

Token and cost tracking exist to improve operator awareness and runtime control.

They do not create authority.
They do not make an output more correct.
They do not replace governance posture.
They do not silently decide whether meaningful work should continue.

If runtime cost tracking becomes a hidden substitute for governance, the implementation is wrong.

---

## Relationship to Existing Authority

This document does not create new doctrine for approvals, action classes, or continuity posture.
It operationalizes visibility and control mechanics that support those existing doctrines.

In particular, it assumes and must obey the active authority already defined for:

- session-basis visibility
- stale / invalid / blocked runtime posture
- compaction and continuity behavior
- operator reviewability
- approval-sensitive action handling

This document defines how token and cost usage are measured and surfaced mechanically.

---

## Runtime Usage Lifecycle Overview

Token and cost tracking should be treated as a runtime measurement lifecycle with the following stages:

1. **usage capture**
2. **session accumulation**
3. **context-pressure evaluation**
4. **warning and threshold evaluation**
5. **operator-visible publication**
6. **compaction-pressure integration**
7. **refresh and reconciliation**

This is a visibility and runtime-support lifecycle, not an approval lifecycle.

---

## Usage Capture

The runtime should capture usage information from model responses and runtime events as they occur.

### Minimum Usage Fields

At minimum, each measurable turn or response event should support capture of:

- input tokens
- output tokens
- cache creation input tokens, where applicable
- cache read input tokens, where applicable
- model identifier used
- timestamp
- session lineage identifier
- delegated task identifier, if the usage came from delegated work

### Why This Matters

Without per-event capture, the runtime can only guess after the fact. That makes operator visibility weaker and makes compaction-pressure tracking less trustworthy.

---

## Session Accumulation

The runtime should maintain cumulative session-level counters.

### Minimum Session Counters

At minimum, the session runtime should maintain:

- total input tokens
- total output tokens
- total cache creation tokens
- total cache read tokens
- most recent turn input tokens
- most recent turn output tokens
- current estimated live-context token count
- current protected-context reserve estimate
- cumulative estimated session cost

### Delegated Work Posture

If delegated work participates, delegated usage may contribute to session totals, but should remain attributable.
The operator should not lose the ability to distinguish:

- parent-session usage
- delegated-session usage
- total combined usage

### Important Rule

Accumulation is a measurement activity.
It does not, by itself, create permission to continue or require forced stoppage.

---

## Context-Pressure Tracking

The runtime should track context pressure as a first-class runtime condition.

### Minimum Context-Pressure Inputs

At minimum, context-pressure calculation should use:

- current estimated live-context tokens
- reserved output budget
- protected-context reserve
- compactable working-context budget
- configured compaction threshold

### Effective Budget Posture

The runtime should not treat the full context window as freely usable working space.
Protected context permanently occupies part of the usable budget.

A reasonable posture is:

```text
effective_input_budget = context_window - reserved_output_budget
compactable_budget = effective_input_budget - protected_context_reserve
context_fill_pct = live_context_tokens / effective_input_budget
compactable_fill_pct = compactable_tokens / compactable_budget
```

### Why Two Fill Values Matter

A naive single percentage can hide whether pressure is coming from:

- protected context that must remain
- compactable working context that may be reduced

The runtime should preserve this distinction internally even if the operator sees a simplified display.

---

## Cost Accumulation Mechanics

The runtime should support estimated session-cost accumulation using provider/model pricing inputs available to the runtime.

### Minimum Cost Posture

At minimum, the runtime should be able to compute or estimate:

- cumulative estimated cost per session
- per-turn estimated cost where available
- cumulative delegated-task cost where applicable
- latest-turn cost estimate

### Important Rule

Cost should be treated as an operator-awareness metric and optional control surface.
It must not silently acquire the role of implicit approval gate.

### Uncertain Cost Conditions

If exact pricing is unavailable or stale, the runtime may surface cost as estimated or unavailable.
It must not present uncertain cost as precise truth.

---

## Usage Event Publication

The runtime should publish usage events as structured internal runtime events rather than burying usage updates inside unrelated session logic.

### Minimum Event Shape

A usage event should be able to carry, at minimum:

- input/output token counts
- cache token counts where relevant
- cost estimate delta where available
- current cumulative totals after the event
- delegated attribution where relevant
- timestamp

### Why This Matters

Structured usage events make it easier to:

- update operator surfaces
- keep usage displays synchronized
- support delegated attribution
- test cost tracking independently of other runtime logic

---

## Operator-Visible Publication

The operator should be able to understand the broad token/cost posture of the session without having to inspect logs or guess from behavior.

### Minimum Operator Visibility

At minimum, implementation should support visibility for:

- cumulative session token usage
- current context-pressure posture
- whether compaction pressure is approaching threshold
- cumulative estimated session cost
- whether delegated work is materially contributing to usage
- whether usage numbers are exact, estimated, or unavailable

### Display Posture

The operator does not need an always-expanded analytics dashboard.
But the runtime should not hide the fact that the session is becoming expensive or approaching context pressure.

### Important Distinction

Visibility is not the same thing as gating.
Showing cost or pressure is required.
Silently changing behavior because cost rose is not acceptable unless an explicit operator-controlled configuration says so.

---

## Threshold and Warning Posture

The runtime may evaluate thresholds for warning purposes.

### Warning Types

At minimum, the runtime should be able to raise warnings such as:

- **context pressure warning** — compaction threshold approaching
- **high session cost warning** — cumulative spend exceeded warning threshold
- **delegated usage spike warning** — delegated work contributing unusually high usage
- **pricing unavailable warning** — cost estimates are partial or unavailable

### Warning Behavior

Warnings should:

- be visible to the operator
- avoid overstating certainty
- not silently mutate governance posture
- not replace compaction blocking or approval rules

### Hard Rule

A warning is not a gate.
A warning may prompt operator review or caution.
It must not pretend to be a governance decision.

---

## Relationship to Compaction Pressure

Context-pressure tracking should feed the compaction lifecycle without collapsing into it.

### Required Relationship

The runtime should expose enough signal for the compaction subsystem to know:

- current token pressure
- protected-context reserve estimate
- whether the compactable budget is nearing threshold
- whether a compaction cycle has already occurred recently

### Important Rule

Usage tracking does not decide whether compaction is allowed.
Compaction still depends on the doctrinal eligibility checks and blocking rules defined elsewhere.
Usage tracking only provides pressure information.

### Companion Relationship

The compaction lifecycle that consumes pressure signals is defined in `extension-compaction-implementation-design.md`.
This document only defines how pressure and usage values are measured and surfaced.

---

## Optional Budget Controls

The runtime may support operator-configured usage or budget controls.

### Allowed Posture

If budget controls exist, they should be explicitly operator-owned and visible.
Examples include:

- warning thresholds
- soft budget targets
- explicit hard stop configurations set by the operator

### Forbidden Posture

The runtime must not silently impose hidden budget gates that interrupt governance-sensitive work without the operator understanding that this posture is active.

### Why This Matters

Budget policy is operational convenience and cost control.
It is not a substitute for governance doctrine.

---

## Refresh and Reconciliation

Usage surfaces must remain synchronized with the current session basis.

### Refresh Triggers

At minimum, the runtime should refresh visible usage posture when:

- a turn completes
- delegated work completes or is cancelled
- a compaction cycle completes
- the session basis is materially refreshed
- pricing inputs are updated or invalidated

### Session Re-entry / Resume

If the extension supports resumed sessions, usage posture must clearly distinguish between:

- carried-forward historical session totals
- newly accumulated usage since resume

The runtime must not present blended totals in a way that makes the operator think the current live session spent all of it in one uninterrupted flow if that is not true.

---

## Suggested Runtime Structure

A reasonable implementation split would separate the following concerns:

### 1. Usage Capture Adapter
Captures provider/model usage metadata from runtime responses.

### 2. Session Usage Accumulator
Maintains cumulative counters and latest-turn values.

### 3. Cost Estimator
Applies pricing inputs and produces estimated cost deltas and totals.

### 4. Context-Pressure Tracker
Computes effective pressure, fill percentages, and compaction-pressure posture.

### 5. Usage Event Publisher
Publishes structured runtime usage events for dependent surfaces.

### 6. Warning Evaluator
Computes operator-visible warnings without mutating governance posture.

### 7. Usage Surface Publisher
Provides synchronized session-level usage summaries to the operator surface and runtime-basis summaries.

This split is preferred over one giant usage blob because cost, token pressure, warnings, and publication have different failure modes and need clearer testing boundaries.

---

## Anti-Drift Constraints

Implementation must not drift into any of the following:

- treating expensive outputs as more authoritative than cheap ones
- silently blocking meaningful work because an internal cost threshold was crossed
- collapsing protected-context reserve and compactable budget into one misleading number
- hiding delegated usage inside parent totals with no attribution
- showing precise-looking costs when pricing is only partial or uncertain
- treating token pressure as if it alone decides compaction eligibility
- letting cost warnings become shadow approval gates

---

## Usage

This document should be used:

- when implementing session usage counters and cost estimation
- when building operator-visible token/cost displays
- when wiring context-pressure values into compaction support
- when reviewing whether budget-aware runtime behavior is drifting into hidden governance
- when designing usage visibility for delegated work

---

## Related Docs

- `extension-state-and-context-model.md`
- `extension-memory-and-continuity-model.md`
- `extension-system-init-and-tool-surface-model.md`
- `extension-compaction-implementation-design.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
