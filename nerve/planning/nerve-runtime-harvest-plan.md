# Claw-Code Runtime Harvest Plan

## Purpose

This document is the bounded planning artifact for the claw-code / runtime-pattern harvest cluster under `nerve/`.

It exists to answer:

```text
What runtime patterns should the V Ecosystem adopt from claw-code,
in what order, with what doctrine gates, and with what explicit rejects,
so the ecosystem gains runtime strength without authority drift?
```

This is a planning artifact.
It is not doctrine.
It is not an authority substitute for the canonical docs under `interfaces/`, `governance/`, `project-v/`, `veda/`, or `v-forge/`.

---

## Status

**Historical planning artifact — first-wave harvest posture captured and executed.**

This document records the approved posture that shaped the initial Nerve runtime wave.
It should now be read as:

- a record of the original adoption posture
- a source for explicit rejects and early sequencing logic
- supporting planning context

It should **not** be treated as the live next-step tracker.
For current phase status, completed artifacts, and active next moves, use:

```text
planning/nerve-runtime-roadmap.md
```

---

## Scope

This document governs:

- the current claw-code runtime harvest posture
- approved, conditional, and rejected pattern categories
- the sequence of next bounded docs and patches
- the doctrine gates required before risky runtime imports go live
- the bridge from `nerve/` investigation work into canonical shared-root doc work

---

## Out of Scope

This document does not define:

- canonical ecosystem doctrine
- final implementation code
- final MCP schemas
- final operator surface rendering details
- permanent runtime authority rules outside the canonical doc clusters

Those belong in the proper shared-root authority docs.

---

## Core Rule

The V Ecosystem may borrow runtime substrate patterns from claw-code, but it must not import claw-code's product posture, authority assumptions, memory looseness, CLI shell habits, or unguided orchestration model.

Useful patterns may be harvested.
Authority drift may not.

---

## What claw-code is for V purposes

For V purposes, claw-code is best treated as:

- a runtime-pattern mine
- a source of mechanical ideas for session handling, compaction, tool filtering, and task support
- a non-authoritative external input

It is not:

- an ecosystem blueprint
- a governance model
- a V extension product model
- an authority source for system boundaries

---

## Working classification

### Safe substrate imports
Patterns that can usually be adapted without threatening ecosystem authority:

- token budget trigger structure
- compaction strategy interface shape
- tool trait / registry shape
- read-only vs mutating partition pattern in tool orchestration
- token and usage accumulation counters

### Conditional runtime imports
Patterns that may be useful but only under strong doctrine constraints:

- governed compaction execution
- protected-context preservation mechanics
- pre-compaction memory flush
- system-init assembly mechanics
- session-scoped tool filtering
- permission policy mechanics
- transcript persistence
- task lifecycle support
- worker delegation support

### Hard rejects
Patterns that should not be imported into the V Ecosystem in current posture:

- plugin / hook capability spread
- CLI REPL product shell posture
- slash-command-first interaction model
- YOLO / aggressive auto-approval posture
- naive compaction-by-truncation logic
- unguided sub-agent expansion
- generic provider abstraction imported for its own sake

---

## Doctrine gates

### Gate 1 - Pre-compaction memory flush must be classified as a governed action
Required action:
- patch `governance/agent-operating-doctrine.md`

Why:
- the flush is a durable write to non-authoritative artifacts
- it needs an explicit write-scope leash before implementation companions reference it

### Gate 2 - Compaction implementation design must be subordinate to existing memory and continuity doctrine
Required action:
- write `interfaces/extension-compaction-implementation-design.md`

Why:
- the ecosystem already has doctrine for compaction classes, protected context, blocking rules, and failure posture
- the missing piece is the mechanical design, not new top-level doctrine

### Gate 3 - Tool-surface implementation design must be subordinate to existing system-init and tool-surface doctrine
Required action:
- write `interfaces/extension-tool-surface-implementation-design.md`

Why:
- absent-affordance is already doctrinally required
- the missing piece is the runtime registry/filtering mechanics

---

## Historical sequencing posture

This sequence records the original first-wave planning logic that has now been executed.
For current sequencing, use the roadmap.

### Do first

1. patch `governance/agent-operating-doctrine.md`
2. write `interfaces/extension-compaction-implementation-design.md`
3. write `interfaces/extension-tool-surface-implementation-design.md`

### Do second

4. patch `interfaces/extension-memory-and-continuity-model.md`
5. patch `interfaces/extension-system-init-and-tool-surface-model.md`
6. write `interfaces/extension-token-and-cost-tracking-design.md`
7. patch `interfaces/extension-state-and-context-model.md`

### Do later

8. transcript persistence implementation companion
9. task lifecycle implementation companion
10. worker delegation / memory-sync implementation work
11. session resume work

---

## Anti-drift posture

The claw-code harvest must not cause any of the following:

- memory becoming authority
- transcripts becoming pseudo-governance
- compaction silently dropping protected context
- delegation widening authority
- orchestration becoming shadow planning
- wrong-system tools appearing in the wrong runtime surface
- CLI shell assumptions leaking into extension-centered design
- `nerve/` becoming a shadow authority root

---

## Historical best next move

The best next move recorded by this plan was:

1. keep `nerve/` organized as the bounded investigation/planning cluster
2. use the doctrinal audit as the main decision input
3. patch `governance/agent-operating-doctrine.md` to classify pre-compaction memory flush as a governed bounded action
4. then write the compaction implementation companion doc

That first-wave sequence has now been executed.
For live current next moves, use:

```text
planning/nerve-runtime-roadmap.md
```
