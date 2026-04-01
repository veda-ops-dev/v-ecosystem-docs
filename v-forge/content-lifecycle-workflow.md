# V Forge Content Lifecycle Workflow

## Purpose

This document defines the content lifecycle workflow V Forge uses for owned execution work.

It exists to answer:

```text
How does content move through V Forge from handed-off execution scope to build, structure, publication, maintenance, and bounded return-to-planning without collapsing execution truth into planning truth or signal ownership?
```

This is a Tier 2 V Forge workflow authority document.

---

## Scope

This document governs:

- the content lifecycle states V Forge uses for owned execution work
- how content enters execution from governed handoff
- how content moves through build, structural registration, publication, and maintenance
- how execution-side validation and bounded research fit into content work
- how blocked, partial, failed, or changed-condition outcomes are handled
- when content work remains execution-local and when it must return to planning

---

## Out of Scope

This document does not define:

- the detailed MCP wire schemas for V Forge tools
- the complete publication approval matrix for every content surface
- the detailed content graph schema
- future experimentation or optimization workflows
- future SaaS/runtime/commercial execution workflows

Those belong in implementation, MCP, schema, governance, or later V Forge docs.

---

## System

- v-forge

---

## Core Rule

Content work in V Forge must move through a bounded execution lifecycle.

The lifecycle exists to ensure that content execution:
- begins from approved scope
- remains legible as execution truth
- updates the content graph honestly
- preserves publication continuity
- reports blockers and uncertainty honestly
- returns to planning when execution can no longer proceed legitimately within scope

V Forge must not use the content lifecycle as a loophole for planning, open-ended research, or self-authorized expansion.

---

## Workflow Definition

The V Forge content lifecycle workflow is the bounded execution path by which a content work unit moves through:

1. execution admission
2. execution readiness check
3. content build or update
4. structural registration in the content graph
5. publication or release state handling where applicable
6. maintenance or follow-on execution state where applicable
7. execution reporting and bounded findings
8. return-to-planning when required

This workflow defines execution-side truth for content work.
It does not redefine planning truth.

---

## Content Work Unit Definition

A content work unit is a bounded piece of execution work inside V Forge related to creating, updating, publishing, maintaining, or structurally modifying owned content.

Examples include:
- creating a new page already admitted through planning scope
- materially updating an existing page inside approved execution scope
- registering or correcting content graph structure after execution work
- publishing or releasing approved content to an owned surface
- maintenance work on previously published content

A content work unit is not:
- a planning initiative
- a market opportunity
- an open-ended research thread
- a strategy proposal

---

## Workflow States

At a minimum, content work units should move through these workflow states:

- `admitted`
- `ready_for_execution`
- `building`
- `structure_pending`
- `ready_for_publication`
- `published`
- `maintenance_active`
- `blocked`
- `failed`
- `partial`
- `return_required`
- `closed`

These are workflow-legibility states.
Implementation may use additional sub-states as long as these meanings remain intact.

---

## State 1 — Admitted

A content work unit enters V Forge only after governed handoff or equivalent governed execution authorization.

At admission, V Forge must be able to determine:
- what content work is being requested
- what scope is in-bounds
- what surfaces or assets are affected
- what constraints matter
- whether publication or release is part of scope now or later

Admission is not yet execution.
Admission means the work is now inside V Forge’s governed execution boundary.

---

## Admission Rule

A content work unit must not be admitted from:
- vague conversational intent
- execution-side enthusiasm
- open-ended execution intelligence observations
- raw signal or evidence alone
- adjacent work discovered during execution unless separately governed

Content execution begins from approved scope, not from “this seems like a good idea while we’re here.”

---

## State 2 — Ready for Execution

Before active content work begins, V Forge must determine whether the admitted work unit is execution-ready.

This check asks:
- is the scope operationally sufficient?
- are the needed content targets explicit enough?
- are publication constraints understood where relevant?
- are missing details a narrow clarification issue or a planning problem?
- does active approval posture still cover this work unit if publication or higher-discipline action is involved?

A work unit that is admitted but not execution-ready must not be forced forward by momentum.

---

## Execution Readiness Rule

A content work unit is ready for execution only when V Forge can determine:
- what is being built or modified
- which owned surface or asset is in scope
- what structural updates will likely be required
- what would count as completion for this work unit
- what should trigger pause, clarification, or return-to-planning

If those conditions are not met, the correct path is clarification or return — not improvisation.

---

## State 3 — Building

The work unit enters active build/update execution.

During this state, V Forge may:
- create or modify the owned content asset
- update execution state as work progresses
- perform bounded execution-side validation needed to continue the build
- preserve partial completion honestly where work is incomplete

During this state, V Forge must not:
- expand the scope of the work unit casually
- redefine planning intent
- treat execution-side findings as automatic authority to create more content work units

---

## Build Scope Rule

The build state is bounded by the admitted content work unit.

This means:
- in-scope content work may proceed
- newly discovered adjacent opportunities must not be silently absorbed
- a structural problem may justify pause or bounded correction, but not freeform scope growth
- execution convenience must not widen what the work unit now means

If the build reveals a materially larger or different content need than the admitted unit covered, the correct response is a bounded finding and possible return-to-planning.

---

## State 4 — Structure Pending

When content work changes what was built, V Forge must ensure that execution truth is reflected in the content graph.

This state exists to ensure that:
- newly built assets are registered
- materially changed assets are updated
- internal links, topics, entities, archetypes, and schema usage remain accurate where relevant
- execution truth and graph truth do not drift apart

A content work unit should not be considered operationally whole if the built asset changed but the content graph was left behind.

---

## Structural Registration Rule

Structural registration must reflect what was actually built.

This means:
- the graph must not get ahead of execution truth
- the graph must not remain stale when execution truth changed materially
- graph updates must remain project-scoped
- graph writes must not become hypothetical planning structure

If structural registration cannot be completed because the work is genuinely incomplete, blocked, or failed, the execution record must preserve that honestly.

---

## State 5 — Ready for Publication

Where the content work unit includes publication or release, the work unit enters a publication-ready posture after build and structural registration are sufficiently complete.

This state means:
- V Forge believes the content asset is execution-ready for publication within the admitted scope
- publication-sensitive constraints are now relevant
- stronger governance may be required depending on surface, visibility, risk, and action class

Ready for publication is not the same as published.
It is an execution readiness state, not automatic authorization.

---

## Publication Rule

Publication must remain subordinate to governance and surface discipline.

This means:
- publication action must stay inside owned execution surfaces
- public-facing, launch-sensitive, or higher-risk publication may require stronger approval posture
- publication capability must not be confused with publication permission
- publication continuity must record what happened honestly after the action occurs

If publication authorization is unclear, V Forge must halt rather than publish by convenience.

---

## State 6 — Published

The work unit reaches published state when the approved publication action has actually occurred and publication continuity has been updated.

Published means:
- the content asset has been made live or released on the relevant owned surface
- V Forge has preserved the publication outcome as execution truth
- the content graph and publication continuity are now aligned with what actually happened

Published does not mean:
- planning is complete forever
- the work unit can never re-enter maintenance
- external performance is now owned by V Forge as signal truth

---

## Publication Continuity Rule

Once published, the work unit must preserve enough execution continuity that a later reviewer can determine:
- what was published
- where it was published
- when it was published
- under what execution state it was published
- whether the outcome was normal, partial, rolled back, or failed

Publication continuity is execution truth.
It is not planning truth and not observatory truth.

---

## State 7 — Maintenance Active

Published or otherwise closed content work may later re-enter V Forge under bounded maintenance scope.

Maintenance may include:
- corrective updates
- structural corrections
- bounded refresh work
- owned-surface operational upkeep

Maintenance must remain a governed execution activity.
It must not become an open-ended backdoor for strategy rewriting or uncontrolled content expansion.

---

## Maintenance Rule

Maintenance work must:
- remain explicitly scoped
- preserve continuity with the prior work unit or asset history
- update the content graph and publication continuity honestly if material changes occur
- return to planning when maintenance reveals a planning-level change rather than an execution-local correction

Maintenance is not blanket permission to keep changing content indefinitely.

---

## Blocked / Failed / Partial States

Not all content work will reach normal publication or closure.

### Blocked
Use when the work cannot continue within current scope because of missing conditions, missing authorization, unresolved dependency, or other execution blocker.

### Failed
Use when the work attempted execution and did not succeed.

### Partial
Use when part of the admitted work unit completed but the whole unit did not complete.

These states must be preserved honestly.
They must not be flattened into cleaner-looking success states.

---

## Honesty Rule

V Forge must not smooth content execution reality into fiction.

This means:
- partial must not be reported as complete
- blocked must not be presented as waiting quietly with no consequence
- failed must not be disguised as a minor detour
- structural registration gaps must not be hidden after build activity
- publication uncertainty must not be erased for appearance

Execution truth is more valuable than reassuring status theater.

---

## Clarification vs Return Rule

During the content lifecycle, narrow ambiguity may be resolved through clarification when:
- the admitted work unit remains fundamentally valid
- the clarification does not widen scope
- the clarification does not require planning reconsideration

Return-to-planning is required when:
- the blocker materially affects what should be done next
- the content work revealed a larger planning issue
- the admitted scope no longer makes sense under current conditions
- publication or completion cannot continue legitimately inside execution bounds

Clarification is not a loophole for silent planning inside V Forge.

---

## Return-to-Planning Triggers

A content work unit must trigger return-to-planning when one or more of the following become true:
- admitted scope is no longer sufficient or legitimate
- execution reveals a planning-level contradiction
- publication cannot proceed because approval or planning basis is materially unclear
- bounded execution findings materially affect future planning direction
- maintenance revealed a need that exceeds execution-local correction

Return-to-planning should transfer bounded findings, not dump all execution ownership upstream.

---

## Content Lifecycle and Execution Intelligence

Execution intelligence may inform content execution, but it must not silently create new content work units.

This means:
- execution intelligence may help interpret what is happening with built content
- execution intelligence may help justify a bounded finding or maintenance need
- execution intelligence does not itself authorize new content creation or planning mutation

If execution intelligence reveals a broader opportunity or gap, that is a planning-relevant finding, not self-authorizing content scope.

---

## Governance and Halt Rule

V Forge must halt content work when governance conditions break.

Examples include:
- missing or unclear approval for publication-sensitive action
- scope ambiguity that would require planning interpretation
- discovery that the work unit exceeds admitted scope
- blocker that cannot be resolved within execution-local bounds

A governed halt is correct behavior.
Continuing by momentum is not.

---

## Cross-System Boundary Rule

The content lifecycle must preserve system ownership.

This means:
- Project V remains the owner of planning truth
- VEDA remains the owner of signal/observability truth
- V Forge remains the owner of execution truth, content graph truth, and publication continuity

The lifecycle must not:
- mutate Project V planning truth directly
- absorb VEDA signal ownership into V Forge execution records
- treat publication continuity as planning authority

Cross-system inputs may inform the workflow.
They do not collapse ownership.

---

## Human-In-The-Loop Principle

Human review remains especially important when the content lifecycle reaches:
- publication-sensitive action
- high-risk public-facing change
- ambiguous scope interpretation
- major blocked or failed states
- return-to-planning conditions with material planning consequences

V Forge should make content execution more governable, not less.

---

## LLM Use Principle

A capable LLM should be able to infer from this workflow that:
- content work enters V Forge from approved scope, not freeform idea generation
- build/update execution is bounded by the admitted work unit
- content graph updates must reflect what was actually built
- publication readiness is not publication authorization
- maintenance is bounded execution, not endless strategy creep
- blocked, failed, and partial states must be preserved honestly
- return-to-planning is required when content execution reveals planning-level issues

If an LLM could use this workflow to justify self-authorized content expansion, planning mutation, or publication by convenience, the workflow is failing.

---

## Usage

This document should be used:
- when designing or reviewing V Forge content execution workflows
- when deciding how content work units move through build, graph registration, publication, and maintenance
- when evaluating whether a content blocker should trigger clarification or return-to-planning
- when designing content-lifecycle-related MCP tools or operator flows
- when checking whether V Forge content execution is drifting into planning or signal ownership

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `mcp-surface.md`
- `data-boundaries.md`
- `reporting-and-approval-model.md`
- `human-in-the-loop-doctrine.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
