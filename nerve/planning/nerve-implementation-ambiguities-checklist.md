# Nerve Implementation Ambiguities Checklist

## Purpose

This document captures the bounded implementation ambiguities that remain after the current Nerve runtime doc wave.

It exists to answer:

```text
What implementation branch points remain open even though the current doc spine is strong enough to begin building,
so implementers do not mistake bounded ambiguity for missing doctrine or for fully frozen design?
```

This is a planning and implementation-support artifact.
It is not doctrine.
It is not a substitute for the canonical governance or interface docs.
It is not a reason to delay implementation of the first-wave and second-wave covered areas.

---

## Status

**Active implementation-support checklist.**

This document should be used when:
- starting implementation from the current Nerve doc spine
- deciding where engineers or LLMs still need to make bounded design choices
- determining whether claw-code source or the source-mapped reference should be consulted as a secondary mechanical reference

This document should not be used to reopen settled doctrine questions that are already answered in canonical docs.

---

## Core Rule

The current Nerve runtime subset is documented strongly enough to begin implementation.

The remaining items below are **bounded implementation ambiguities**, not missing authority.
Implementers should treat them as:

- branch points to resolve deliberately
- places where a small design note or implementation decision may still be needed
- areas where claw-code or the source-mapped reference may help as a secondary mechanical comparison

They should not be treated as permission to weaken:
- authority boundaries
- continuity-is-not-authority rules
- absent-affordance enforcement
- delegation narrowing
- governed compaction posture

---

## How to use this checklist

For each item below, decide one of the following before or during implementation:

- **resolve in code** — the doctrine is clear and this is a normal engineering choice
- **resolve with a tiny note** — one small implementation clarification doc or code comment convention is worth adding
- **escalate if drift risk appears** — only if implementation pressure begins pushing against established doctrine

Prefer code decisions over new docs unless a repeated ambiguity is likely to confuse future contributors.

---

## 1. Pre-compaction flush failure semantics

### Why this still matters
The compaction implementation design names four flush outcomes:

- `no-op`
- `completed`
- `failed-non-fatal`
- `failed-blocking`

But the distinction between `failed-non-fatal` and `failed-blocking` is not fully operationalized.

### What is already settled
Already settled by doctrine/design:
- the flush is a governed bounded action
- it may write only to designated non-authoritative continuity artifacts
- it must not create authority confusion
- compaction must not continue silently when flush failure invalidates compaction safety or creates authority confusion

### What is still open
Still open at implementation level:
- when a timeout or empty result counts as `no-op` vs `failed-non-fatal`
- when invalid output shape counts as `failed-non-fatal` vs `failed-blocking`
- whether a partial but compliant write can still be treated as `completed`

### Recommended implementation posture
Resolve this in code first.
A good baseline posture is:

- `no-op` = flush not needed or produced intentionally empty result without error
- `completed` = flush wrote compliant output or explicitly completed with no required write
- `failed-non-fatal` = flush failed to produce useful output but did not produce unsafe output
- `failed-blocking` = flush produced unsafe / authority-confusing / structurally invalid output that makes compaction unsafe to continue

### Secondary references
Use as secondary mechanical references only:
- `nerve/references/nerve-runtime-source-reference.md`
- claw-code runtime loop placement patterns

---

## 2. Per-category post-compaction validation matrix

### Why this still matters
The compaction implementation design correctly requires per-category validation and names outcome types such as:

- `valid`
- `stale-refresh-required`
- `missing-refresh-required`
- `conflicted-review-required`
- `invalid-blocking`

But it does not fully map those outcomes across all state/context categories.

### What is already settled
Already settled by doctrine/design:
- validation must remain per category
- one coarse session-valid boolean is insufficient
- the state-and-context model's categories remain authoritative
- missing or invalid critical basis must not be silently ignored

### What is still open
Still open at implementation level:
- which categories are always blocking when missing
- which categories are refreshable vs review-required
- which categories are conditional on current runtime posture
- how evidence-basis and approval-state failures differ from continuity-artifact failures

### Recommended implementation posture
Resolve with a small implementation matrix in code or a tiny design appendix, not a new doctrine wave.

A strong implementation move is to create a category-by-category table for at least:
- project scope state
- current system state
- workflow stage state
- decision continuity context
- evidence basis and freshness state
- session integrity state
- orchestration state
- continuity artifact state
- session tool-surface posture

### Secondary references
Primary truth is canonical docs.
Secondary comparison can use:
- `nerve/references/nerve-runtime-source-reference.md`
- any claw-code compaction trigger flow only for sequencing inspiration, not authority

---

## 3. Protected-context flagging mechanism

### Why this still matters
The docs clearly require that protected context be explicitly loaded, flagged, and frozen — not rediscovered by scanning transcript prose.
But they do not prescribe the exact internal mechanism.

### What is already settled
Already settled by doctrine/design:
- protected context categories exist and are named
- protected context must survive compaction
- transcript presence is not enough
- protected context must be structurally distinct from compactable working context

### What is still open
Still open at implementation level:
- whether flags live on message objects, context entries, or a separate registry
- whether the runtime stores protected context in a dedicated collection separate from transcript history
- how the snapshotter references protected items during freeze and rebuild

### Recommended implementation posture
Prefer structural separation over clever tagging in raw transcript history.
A separate protected-context registry or category-bound loaded-context structure is safer than trying to infer protected items from generic message streams.

### Secondary references
Use claw-code only for compaction adjacency inspiration.
Do **not** use it as the authority for protected-context mechanics because its source posture is weaker than Nerve's.

---

## 4. Task lifecycle `awaiting_review` posture

### Why this still matters
The task lifecycle design includes `awaiting_review`, but the wording leaves mild ambiguity about whether it is always required or only present where review handoff is relevant.

### What is already settled
Already settled by doctrine/design:
- meaningful delegated/runtime tasks require explicit lifecycle state
- review-sensitive work must remain visible
- task outputs do not become authority automatically
- orchestration visibility must reflect review-relevant states honestly

### What is still open
Still open at implementation level:
- whether `awaiting_review` is part of the universal task enum
- whether implementations may omit it when no review-handoff flows exist
- how review-required tasks differ from completed tasks with reviewable outputs

### Recommended implementation posture
Use `awaiting_review` in the task state model from the start.
That is the safer and more extensible choice.
It avoids later retrofitting when orchestration or delegated review flows expand.

### Secondary references
claw-code task handling may help as a state-machine seed, but Nerve task-state visibility and review posture are already more specific.

---

## 5. Simultaneous invalidation / rebuild sequencing

### Why this still matters
Multiple subsystems define refresh and invalidation triggers:
- compaction
- tool-surface rebuild
- system-init refresh
- state/context invalidation
- delegated completion

But no single doc defines combined sequencing when multiple triggers occur in the same cycle.

### What is already settled
Already settled by doctrine/design:
- rebuilds and refreshes must be explicit
- material changes to session basis must surface visibly
- stale basis must not continue invisibly
- tool-surface rebuild may require bounded system-init re-assembly

### What is still open
Still open at implementation level:
- ordering when compaction and current-system change occur together
- ordering when delegated completion changes continuity artifacts during a refresh cycle
- whether rebuilds are batched, serialized, or coordinated through a single refresh manager

### Recommended implementation posture
Resolve in architecture, not doctrine.
A single runtime refresh coordinator is likely safer than letting each subsystem free-fire its own rebuild independently.

### Secondary references
The source-mapped reference and claw-code main-loop structure may help as secondary sequencing inspiration only.

---

## 6. Transcript event volume / retention posture

### Why this still matters
The transcript persistence design correctly defines what should be captured, labeled, and retrievable.
It does not define retention volume posture for very long sessions.

### What is already settled
Already settled by doctrine/design:
- transcripts are non-authoritative artifacts
- meaningful session events should not disappear casually
- compaction, delegated work, warnings, and interruptions are transcript-worthy
- transcript retrieval must preserve reviewability

### What is still open
Still open at implementation level:
- whether transcripts are append-per-event, append-per-turn, or checkpoint-based in practice
- whether very large transcripts are segmented by session epoch or compaction boundary
- whether any retention cap exists and how it preserves audit usefulness without silent loss

### Recommended implementation posture
Do not let storage convenience decide policy implicitly.
Prefer explicit segmentation or bounded checkpointing over arbitrary truncation.
If a retention cap becomes necessary, make it visible and auditable.

### Secondary references
claw-code is only weakly useful here.
This area is mostly V-native.

---

## 7. When to consult claw-code or the source-mapped reference

### Correct posture
For the current covered runtime subset, the canonical Nerve/V docs are now the primary implementation truth.

### Secondary-reference use is still appropriate when
- comparing trait/interface shapes
- checking how a runtime loop may place pressure checks or task notifications
- seeing one working registry/orchestrator split
- understanding one possible event-emission or manager pattern

### Secondary-reference use is not appropriate when
- deciding authority boundaries
- deciding memory/continuity posture
- deciding compaction safety rules
- deciding whether delegation may widen access
- deciding how absent-affordance should work

### Practical instruction for implementers
Use:
- canonical docs first
- `nerve/references/nerve-runtime-source-reference.md` second
- actual claw-code clone/source third, as comparison only

If the source code suggests something weaker than the canonical docs, the source code loses.

---

## 8. Build-now vs clarify-now guidance

### Safe to build now
The following areas are strong enough to begin immediately:
- tool registry and tool-surface filtering
- token/cost tracking
- transcript persistence
- task lifecycle foundation
- compaction pipeline shell with protected-context scaffolding

### Clarify during implementation
The following should be resolved early in code/design review while implementing:
- flush failure result distinctions
- per-category validation matrix
- protected-context flagging mechanism
- refresh coordinator sequencing
- transcript segmentation / retention posture

### Escalate only if drift pressure appears
Only escalate back into docs if implementation pressure begins pushing toward:
- transcript-as-authority
- memory-as-authority
- weakened absent-affordance
- delegated privilege expansion
- compaction that proceeds despite blocked posture

---

## Final note

This checklist should be read together with:
- `planning/nerve-runtime-roadmap.md`
- `references/nerve-runtime-source-reference.md`
- the canonical governance/interface docs already patched in the first and second waves

Its purpose is simple:

**help implementers start building from the current doc spine without mistaking bounded implementation choice for missing doctrine or for a fully frozen internal design.**
