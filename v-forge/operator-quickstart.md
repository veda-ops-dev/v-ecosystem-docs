# V Forge Operator Quickstart

## Purpose

This document gives operators and synced LLM sessions a practical starting posture for using V Forge correctly.

It exists to answer:

```text
How should an operator or LLM begin using V Forge, what should they look at first, what kinds of work belong here, what actions must stay bounded, and how can they operate V Forge effectively without drifting into planning ownership, observability ownership, or self-authorized execution?
```

This is a Tier 2 V Forge operator authority document.

---

## Scope

This document governs:

- the default operator starting posture in V Forge
- the first-read document order for V Forge work
- how to classify the work in front of you before acting
- the safe starting sequence for common V Forge sessions
- the most important do and do-not rules for operators and LLMs using V Forge
- how to recognize when work should stay in V Forge and when it must return to planning

---

## Out of Scope

This document does not define:

- every detailed workflow in V Forge
- every MCP tool schema
- full release approval matrices
- future experimentation or commercial layers
- implementation details of the VS Code extension runtime

Those belong in the more specific V Forge, interface, governance, and extension docs.

---

## System

- v-forge

---

## Core Rule

Use V Forge as the execution system of record.

Start from approved scope.
Operate inside bounded execution.
Preserve execution truth honestly.
Stop when scope, ownership, or authorization becomes unclear.

Do not use V Forge as a substitute for:
- Project V planning
- VEDA observability ownership
- freeform experimentation
- self-authorized launch behavior

---

## What V Forge Is For

Use V Forge when the work is about:
- carrying out approved work
- updating or inspecting execution truth
- operating or maintaining owned execution surfaces
- managing the content graph of what was built
- handling content lifecycle or release lifecycle work
- producing execution reports and bounded findings
- interpreting execution intelligence derived from graph plus bounded VEDA signal
- routing bounded return-to-planning findings when execution can no longer continue legitimately inside scope

If the work is fundamentally about deciding what should be pursued next, that belongs in Project V.
If the work is fundamentally about owning or gathering observatory signal, that belongs in VEDA.

---

## What To Read First

When entering V Forge work, read these in order:

1. `v-forge/v-forge.md`
2. `v-forge/system-invariants.md`
3. `v-forge/operational-model.md`
4. `v-forge/mcp-surface.md`
5. `v-forge/content-lifecycle-workflow.md`
6. `v-forge/release-lifecycle-workflow.md`
7. `v-forge/content-graph-operations.md`
8. `v-forge/execution-intelligence-operations.md`

If your work is specifically about handoff or returns, then also read:
- `interfaces/project-v-to-v-forge-handoff-interface.md`
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md`

If your work is specifically about bounded signal consumption, also read:
- `interfaces/veda-to-v-forge-signal-interface.md`

---

## First Question To Ask

Before doing anything in V Forge, ask:

**“Is this execution work, or am I about to do planning or observability work by accident?”**

That question prevents most drift.

### It belongs in V Forge when:
- the work is already approved or legitimately admitted into execution
- the work is about building, updating, releasing, maintaining, or reporting on owned execution assets
- the work is about the content graph as execution truth
- the work is about execution-local validation or bounded correction

### It does not belong in V Forge when:
- the work is deciding what opportunities to pursue
- the work is open-ended market or keyword exploration
- the work is creating planning structure
- the work is inventing broader scope because execution discovered something interesting

---

## Default Session Start Sequence

When beginning a normal V Forge session, use this sequence.

### 1. Confirm project scope
Make sure you know which project the session is bound to.

### 2. Confirm the work unit
Identify whether you are handling:
- content execution
- release execution
- maintenance
- graph correction
- execution reporting
- return-worthy finding review

### 3. Confirm the current scope basis
Identify what admitted or approved work the session is acting on.

Examples:
- a handoff from Project V
- a bounded maintenance task already inside execution scope
- a release unit already admitted through governed execution authorization

### 4. Confirm whether the task is normal execution or higher-discipline execution
Ask whether this work involves:
- public-facing release
- launch-sensitive action
- paid action
- irreversible or hard-to-undo change

If yes, assume stronger discipline and authorization checks matter.

### 5. Inspect current execution truth before mutating anything
Check:
- current execution state
- current content graph truth
- release/publication continuity if relevant
- existing execution reports or blockers if relevant

### 6. Proceed only inside bounded scope
If the scope is unclear, stop and clarify or return.

---

## Common Starting Modes

## Mode 1 — Content Work

Use when you are:
- creating or updating a content asset already in execution scope
- registering structural changes in the content graph
- handling publication-ready content inside admitted execution scope
- doing bounded maintenance on built content

Read first:
- `content-lifecycle-workflow.md`
- `content-graph-operations.md`

Start by confirming:
- what content work unit is in scope
- whether build or update is already authorized as execution work
- whether publication is part of the current scope or a separate later step

---

## Mode 2 — Release Work

Use when you are:
- preparing a release package
- validating a release target
- handling a publication-sensitive or launch-sensitive release unit
- reviewing rollback or post-release verification state

Read first:
- `release-lifecycle-workflow.md`

Start by confirming:
- what is being released
- whether the release is routine or higher-discipline
- whether current authorization posture actually covers the release action

---

## Mode 3 — Graph Work

Use when you are:
- registering or correcting content graph truth
- validating graph integrity
- inspecting structural execution state
- repairing graph drift after real execution change

Read first:
- `content-graph-operations.md`

Start by confirming:
- whether the graph issue is execution-local
- whether the graph reflects built truth or has drifted
- whether correction would stay inside execution bounds or would actually require planning reconsideration

---

## Mode 4 — Execution Intelligence Review

Use when you are:
- inspecting graph-versus-signal mismatches
- reviewing execution-side gap outputs
- evaluating maintenance candidates
- deciding whether an execution intelligence output stays local or becomes a return-to-planning finding

Read first:
- `execution-intelligence-operations.md`

Start by confirming:
- what bounded signal was admitted
- whether the output is execution-local or planning-relevant
- whether the result is strong enough to justify action, review, return, or no-action

---

## Mode 5 — Return-to-Planning

Use when execution can no longer proceed legitimately inside scope or when findings materially affect what planning should do next.

Read first:
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md`

Start by confirming:
- what execution truth is being returned
- why execution cannot or should not continue inside current scope
- what remains uncertain
- what stays owned by V Forge after the return

---

## Practical Do Rules

### Do start from admitted execution scope
Never start from vague intent or interesting signal alone.

### Do inspect existing execution truth first
Before writing, releasing, correcting, or reporting, inspect what V Forge already says is true.

### Do preserve honesty in status
Use blocked, failed, and partial states honestly.

### Do update the graph when execution truth changes materially
Do not leave structure stale after real build changes.

### Do treat release capability as separate from release authorization
Especially on public-facing or launch-sensitive work.

### Do route planning-relevant findings back through the governed return path
Do not solve planning problems locally inside V Forge because it feels faster.

### Do preserve ownership labels mentally
V Forge owns execution truth.
Project V owns planning truth.
VEDA owns signal truth.

---

## Practical Do-Not Rules

### Do not create planning truth inside V Forge
No shadow roadmap. No shadow project structure. No stealth planning.

### Do not absorb VEDA signal ownership
Using signal is not the same as owning signal.

### Do not widen scope by momentum
Execution momentum is not permission.

### Do not treat execution intelligence as automatic authorization
A strong analytical output is still not permission to build more stuff.

### Do not smooth rough reality into nicer status language
Blocked is blocked. Partial is partial. Rollback is rollback.

### Do not use maintenance as a loophole for strategic expansion
Maintenance must remain bounded.

### Do not treat return-to-planning as failure theater
It is a correct bounded response when execution should stop and planning must reconsider.

---

## Fast Boundary Checks

When unsure, use these checks.

### Check 1
**“Am I describing what was built, or deciding what should exist?”**
- describing what was built = V Forge
- deciding what should exist = Project V

### Check 2
**“Am I using bounded signal, or trying to own signal?”**
- using bounded signal = allowed in V Forge
- owning signal/archive/observability = VEDA

### Check 3
**“Am I fixing execution truth, or inventing new strategic scope?”**
- fixing execution truth = maybe V Forge
- inventing strategic scope = Project V

### Check 4
**“Would this action still look legitimate if someone audits it later?”**
- if no, stop

---

## When To Stop Immediately

Stop and do not continue casually when:
- project scope is unclear
- the work unit in scope is unclear
- the action would be public-facing, paid, irreversible, or launch-sensitive and authorization is unclear
- a graph correction actually implies a planning change
- execution intelligence is being treated like permission
- signal ownership is starting to bleed into V Forge
- you discover the real work is materially larger than the admitted unit
- you are tempted to “just finish it” even though the boundary is no longer clear

That is the moment for:
- clarification
- halt
- escalation
- return-to-planning

Not momentum.

---

## What Good V Forge Use Looks Like

Good V Forge use looks like:
- clear project scope
- clear execution unit
- honest current-state inspection
- bounded execution action
- truthful graph and continuity updates
- explicit release discipline where needed
- bounded reporting
- clean return-to-planning when execution hits a real boundary

Bad V Forge use looks like:
- freeform “while we’re here” expansion
- planning inside execution
- observatory behavior inside execution
- release by capability instead of authorization
- graph mutation by theory instead of execution truth
- hiding partial or failed work behind cleaner wording

---

## LLM Sync Reminder

A synced LLM using V Forge should remember:
- V Forge is the executor, not the planner
- V Forge owns execution truth, content graph truth, release continuity, and execution intelligence
- V Forge does not own raw signal
- execution intelligence is influential but non-authoritative
- graph truth follows what was built
- release readiness is not release authorization
- return-to-planning is a normal governed response

If the LLM starts sounding like a strategist, observatory, or self-authorizing deploy engine, it is out of bounds.

---

## Usage

This document should be used:
- by operators starting work in V Forge
- by synced LLM sessions that need a practical starting posture
- during onboarding into V Forge operability
- when deciding which V Forge workflow doc to read next
- as a quick anti-drift check before execution work begins

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `mcp-surface.md`
- `content-lifecycle-workflow.md`
- `release-lifecycle-workflow.md`
- `content-graph-operations.md`
- `execution-intelligence-operations.md`
- `data-boundaries.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
