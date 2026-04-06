# Extension Compaction Implementation Design

## Status
Superseded by `desktop-compaction-implementation-design.md`

This document reflects the legacy VS Code extension host model.
The Tauri 2 desktop application defined in ADR-011 is now the primary operator host.
Use `desktop-compaction-implementation-design.md` for active implementation guidance.

## Purpose

This document defines the mechanical implementation design for runtime compaction in the V Ecosystem extension.

It exists to answer:

```text
How should the extension perform compaction mechanically so long-running sessions remain usable without violating the already-established continuity, governance, state, and operator-visibility doctrine?
```

This is a Tier 3 implementation companion document.
It is subordinate to the active authority in:

- `extension-memory-and-continuity-model.md`
- `extension-state-and-context-model.md`
- `extension-system-init-and-tool-surface-model.md`
- `../governance/agent-operating-doctrine.md`

If this document conflicts with those docs, this document is wrong.

---

## Scope

This document governs:

- compaction trigger mechanics
- runtime budget posture for compaction
- protected-context preservation mechanics
- the pre-compaction flush integration point
- compact-boundary creation mechanics
- post-compaction validation mechanics
- failure posture when required context does not survive compaction
- implementation structure needed to support the above

---

## Out of Scope

This document does not define:

- the canonical doctrine for whether compaction is allowed
- the canonical protected-context categories
- the canonical memory classes
- the final UI rendering of compaction controls
- the full operator wording for compaction notifications
- exact LLM prompt text for every compaction stage

Those are governed by higher-authority docs or later implementation detail.

---

## System

- interfaces

---

## Core Rule

Compaction in the V Ecosystem is a governed lossy runtime operation.

It exists to preserve session usability under token pressure.
It must not weaken governance, erase protected context, convert continuity artifacts into authority, or hide from the operator what basis the runtime is using.

If compaction preserves convenience while weakening authority clarity, the implementation is wrong.

---

## Relationship to Existing Authority

This document does not introduce new compaction doctrine.
It operationalizes existing doctrine.

In particular, it assumes and must obey the existing authority already defined for:

- compaction classes
- compaction blocking conditions
- compaction failure posture
- compact-boundary posture
- protected-context categories
- memory visibility and non-authority rules
- session-state freshness and invalidation rules

This document defines how those existing rules are enforced mechanically.

---

## Compaction Lifecycle Overview

Runtime compaction is implemented as a bounded lifecycle with the following stages:

1. **pressure detection**
2. **compaction eligibility check**
3. **pre-compaction flush opportunity**
4. **protected-context freeze**
5. **compaction execution**
6. **compact-boundary creation**
7. **post-compaction per-category validation**
8. **runtime refresh or halt posture**

Each stage exists to prevent a specific form of drift.

---

## Pressure Detection

The runtime must continuously track session token pressure.

At minimum, the runtime should maintain:

- total input token accumulation
- total output token accumulation
- latest-turn input token count
- current estimated live-context token count
- current protected-context token count
- current compaction threshold posture

### Budget Model

The compaction budget model should separate:

- **context window**
- **reserved output budget**
- **protected-context reserve**
- **compactable working-context budget**

A compaction trigger must never behave as though the full context window is available for compactable material.
Protected context permanently occupies part of the usable budget.

### Working Formula Posture

The implementation should model usable compaction pressure approximately as:

```text
effective_input_budget = context_window - reserved_output_budget
compactable_budget = effective_input_budget - protected_context_reserve
```

Compaction pressure should be evaluated against the compactable budget, not against the naive full input budget.

---

## Compaction Eligibility Check

Pressure alone is not enough.
The runtime must check whether compaction is currently allowed under the higher-authority continuity doctrine.

### Required Check

Before any compaction stage begins, the runtime must evaluate the current session against the canonical compaction blocking rules already defined in `extension-memory-and-continuity-model.md`.

This implementation doc does not restate those blocking rules as doctrine.
It requires an explicit mechanical eligibility check against them.

### Result Types

The eligibility check should produce one of three results:

- **allowed**
- **blocked**
- **review-required**

### Enforcement

If compaction is blocked:

- do not compact
- surface the blocked posture to the operator
- preserve current context state
- enter the applicable failure or review posture defined by higher-authority doctrine

If compaction is review-required:

- do not silently continue into lossy compaction
- surface the reason and required operator intervention

---

## Pre-Compaction Flush Opportunity

Before lossy compaction occurs, the runtime should provide a bounded opportunity for pre-compaction memory flush where doctrine permits.

### Role of Flush

The flush exists to preserve useful **non-authoritative working continuity** before older compactable context is reduced.

It is not a substitute for canonical state.
It is not an evidence promotion path.
It is not a decision-record path.

### Governance Binding

The flush must obey the `Pre-Compaction Flush Principle` in `../governance/agent-operating-doctrine.md`.

This means the implementation must enforce that flush writes:

- target only designated non-authoritative continuity artifacts
- stay within the current runtime scope
- use observational, non-governing language
- remain attributable and reviewable

### Flush Trigger Posture

The runtime should offer flush only when:

- compaction is allowed
- compactable context exceeds threshold
- a flush has not already run for the current compaction cycle
- no blocking condition forbids continuity mutation in the current posture

### Flush Result Posture

The flush step should return one of:

- **no-op**
- **completed**
- **failed-non-fatal**
- **failed-blocking**

If flush fails in a way that increases authority confusion or invalidates compaction safety, compaction must not continue silently.

---

## Protected-Context Freeze

Before compaction touches message history, the runtime must freeze the currently active protected-context set.

### Source of Truth

The protected-context categories are defined by higher-authority doctrine.
This document defines only the mechanical preservation behavior.

### Required Mechanical Behavior

At compaction start, the runtime must create a protected-context snapshot that captures the currently loaded protected context by category.

This snapshot must be structurally distinct from compactable working context.

### Design Requirement

Protected context should not be preserved merely because it happens to appear somewhere in freeform transcript history.
It should be preserved because it is explicitly loaded, flagged, and frozen as protected context.

### Minimum Snapshot Shape

A protected-context snapshot should be representable as category-bound entries, not as one monolithic blob.

At minimum, each entry should carry:

- state category
- load source
- freshness posture
- timestamp or load time
- active/inactive status
- whether post-compaction refresh is required

---

## Compaction Execution

After eligibility passes, flush completes or is safely skipped, and protected context is frozen, the runtime may compact the compactable portion of session context.

### Compaction Classes

The implementation must map directly to the compaction classes already defined in higher-authority doctrine.
This document does not redefine them.

The implementation should support the doctrinal compaction classes as distinct execution paths rather than one generic summarization blob.

### Hard Rule

Protected context must be excluded from lossy compaction.

### Compactable Material

Only compactable working context may be:

- reduced
- summarized
- restructured
- replaced by compact-boundary support artifacts

### Strategy Interface Posture

Implementation should use an explicit compaction strategy interface rather than burying compaction behavior in generic session code.

That strategy layer should accept:

- compactable context input
- target budget
- compact cycle metadata
- any allowed flush outputs admitted for this cycle

And it should return:

- compacted context payload
- removed/replaced segment metadata
- estimated tokens saved
- any warnings raised during compaction

### Forbidden Execution Posture

The compaction executor must not:

- drop protected context silently
- convert transcript residue into fake authority
- imply that compacted prose is canonical state
- merge different state categories into ambiguous continuity mush
- continue after a governance-critical preservation failure as though nothing happened

---

## Compact Boundary Creation

Every successful lossy compaction cycle must create an explicit compact boundary.

### Role of the Boundary

The compact boundary marks the line between:

- what is no longer present as live transcript context
- what remains live runtime context after compaction

### Required Boundary Behavior

The boundary artifact must be:

- visible to the operator
- attributable to the compaction event
- non-canonical by construction
- tied to the current session lineage

### Minimum Boundary Metadata

A compact boundary should carry at least:

- compaction timestamp
- compaction class used
- operator-visible cycle identifier or count
- count of replaced/removed segments
- whether flush occurred
- whether any warnings were raised

### Prohibited Interpretation

The compact boundary must not be treated as:

- a decision record
- an approval record
- an evidence record
- a canonical state snapshot

It is a continuity aid only.

---

## Post-Compaction Per-Category Validation

After compaction completes, the runtime must validate the active session basis before the next normal turn proceeds.

### Why Per-Category Validation Matters

The state-and-context model already defines multiple independent context/state categories with their own freshness and invalidation behavior.
A single boolean such as `context_valid = true/false` is not sufficient.

### Required Validation Posture

Validation must be performed per relevant state/context category.

At minimum, the runtime must verify that categories required for the current session posture are still:

- present where required
- fresh where required
- project-scope-correct where required
- system-posture-correct where required
- non-contradictory where required

### Validation Outcomes

Per-category validation should produce statuses such as:

- **valid**
- **stale-refresh-required**
- **missing-refresh-required**
- **conflicted-review-required**
- **invalid-blocking**

### Required Response Behavior

If a category requires refresh, the runtime should refresh it before continuing where possible.

If a category is invalid-blocking or review-required:

- do not silently proceed into a normal turn
- surface the issue to the operator
- enter the applicable halt or review posture defined by higher-authority doctrine

---

## Runtime Refresh After Compaction

Compaction may require bounded runtime re-assembly.

### Refresh Targets

Depending on what changed, the runtime may need to refresh or rebuild:

- loaded protected-context snapshot
- current system-init basis
- current tool-surface definition
- freshness markers on continuity artifacts
- any context strip / operator-visible basis summary

### Important Rule

Compaction is not just transcript compression.
In the V Ecosystem it is a runtime-basis transition.
If the runtime basis changed materially, refresh must occur before the next normal turn.

---

## Failure Posture

If compaction cannot preserve the doctrinally required basis, the runtime must fail safely.

### Safe Failure Means

- preserve remaining live context where possible
- do not fabricate a successful compacted state
- surface the failure clearly to the operator
- enter halt, blocked, or review-required posture as higher-authority doctrine requires

### Examples of Blocking Failure

Examples include:

- protected context required for the current session posture is missing after compaction
- flush produced authority-confusing output
- compaction output conflicts with active protected context
- current project scope or current system posture cannot be revalidated

---

## Operator Visibility Requirements

The operator must be able to understand that compaction happened and what basis remains active afterward.

At minimum, implementation should support operator visibility for:

- that compaction occurred
- what class of compaction occurred
- whether flush occurred
- whether warnings were raised
- what protected context remains loaded
- whether refresh or review is required before normal continuation

The implementation must not treat compaction as invisible maintenance.

---

## Suggested Runtime Structure

A reasonable implementation split would separate the following concerns:

### 1. Pressure Tracker
Tracks token pressure, protected-context reserve, and compaction threshold posture.

### 2. Compaction Eligibility Checker
Evaluates doctrinal blocking conditions and returns allowed/blocked/review-required posture.

### 3. Flush Coordinator
Runs the bounded pre-compaction flush where permitted and captures flush-cycle results.

### 4. Protected-Context Snapshotter
Freezes protected context by category before lossy execution begins.

### 5. Compaction Strategy Executor
Performs the actual compaction on compactable material only.

### 6. Compact Boundary Builder
Produces the operator-visible continuity boundary artifact for the compaction cycle.

### 7. Post-Compaction Validator
Validates session basis per state/context category and triggers refresh or halt posture.

This split is preferred over one giant compaction function because it makes doctrine violations easier to isolate and test.

---

## Anti-Drift Constraints

Implementation must not drift into any of the following:

- compaction treated as harmless transcript cleanup
- flush treated as a shortcut to memory authority
- protected context preserved only accidentally via prose summaries
- compact boundary treated like a canonical snapshot
- post-compaction validity reduced to one coarse boolean
- compaction hidden from the operator because the UI wants to look smooth
- refresh skipped because stale context is easier than rebuilding basis cleanly

---

## Usage

This document should be used:

- when implementing token-pressure handling in the extension runtime
- when designing the compaction pipeline and its internal service split
- when validating that compaction mechanics remain subordinate to existing doctrine
- when reviewing whether future runtime work is weakening continuity or authority posture

---

## Related Docs

- `extension-memory-and-continuity-model.md`
- `extension-state-and-context-model.md`
- `extension-system-init-and-tool-surface-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
