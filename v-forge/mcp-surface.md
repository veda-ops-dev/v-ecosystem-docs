# V Forge MCP Surface

## Purpose

This document defines the MCP surface V Forge exposes inside the V Ecosystem.

It exists to answer:

```text
What tools and operations should V Forge expose through MCP, how are those tools bounded by execution scope, governance, and system ownership, and how should operators and LLMs understand the V Forge MCP surface without turning V Forge into a planner, a signal system, or an unrestricted autonomous executor?
```

This is a Tier 2 V Forge implementation-build-spec authority document.

---

## Scope

This document governs:

- the role of the V Forge MCP surface
- the categories of tools V Forge may expose through MCP
- the read/write posture of V Forge tool families
- the execution-scope and governance constraints on V Forge tools
- which operations are admitted, bounded, or forbidden through the MCP surface
- how V Forge MCP tools relate to Project V and VEDA interfaces
- how operators and LLMs should understand V Forge MCP tool availability inside the extension runtime

---

## Out of Scope

This document does not define:

- the exact wire schema for every MCP tool response
- detailed database schema internals
- the full VS Code operator surface design
- the full approval matrix for every execution action
- the future experimentation or SaaS/runtime layer

Those belong in implementation, operator-surface, governance, or later V Forge docs.

---

## System

- v-forge

---

## Core Rule

The V Forge MCP surface exists to expose bounded execution capabilities.

It must let operators and LLMs read execution truth, update execution truth within approved scope, manage the content graph and owned execution surfaces, produce execution-side reporting, and route bounded findings back into the ecosystem.

It must not expose planning ownership, observability ownership, or unrestricted action merely because those capabilities would be convenient.

If the V Forge MCP surface would let a capable LLM behave like a planner, a signal-system owner, or a self-authorizing external-action engine, the MCP surface is wrong.

---

## MCP Surface Definition

The V Forge MCP surface is the governed set of tools by which the extension and LLM runtime interact with V Forge execution truth.

It is the execution-facing interface layer for:
- reading execution state
- reading and updating the content graph
- reading and updating owned execution surface state within approved bounds
- reading and writing release/publication continuity where execution owns it
- producing execution reports and bounded findings
- routing return-to-planning packages
- performing bounded execution-side validation and maintenance actions

The MCP surface is not a generic remote-control shell.
It is a bounded execution interface.

---

## V Forge MCP Surface Principles

### 1. Execution-first principle
V Forge tools exist to support execution work already admitted into execution scope.
They do not exist to improvise planning.

### 2. Scope-bound principle
All project-scoped V Forge tools operate within the active project scope bound by the session token.

### 3. Ownership-preserving principle
V Forge tools expose execution truth, not planning truth or observatory truth.

### 4. Bounded research principle
V Forge may expose bounded validation or execution-side research helpers only where they support approved execution.
These helpers must not become open-ended signal gathering.

### 5. Governance-preserving principle
Tool availability is not permission.
High-impact, launch-sensitive, external, or paid actions remain subordinate to governance and approval posture.

---

## MCP Tool Posture

The V Forge MCP surface should be understood through three posture classes.

### 1. Read tools
Read tools retrieve V Forge-owned execution truth without mutating it.

Examples:
- execution item retrieval
- content graph reads
- release/publication continuity reads
- execution report reads
- owned surface state reads
- bounded execution intelligence reads

### 2. Governed write tools
Governed write tools mutate V Forge-owned execution truth inside approved execution scope.

Examples:
- update execution item state
- create or modify content graph records
- write release/publication continuity records
- write execution reports
- write bounded findings
- record blocked/failed/partial execution state

These tools remain governed by scope, workflow, and approval posture.

### 3. High-discipline action tools
These are V Forge tools that may interact with high-risk, external-facing, launch-sensitive, or paid execution operations.

Examples:
- launch-sensitive publication activation
- paid execution-side actions
- external mutation with public consequence

These tools must not be treated as generally available just because the MCP surface can technically expose them.
They require stronger gating and runtime discipline.

---

## Primary V Forge Tool Families

V Forge should expose its MCP surface through bounded tool families.

## 1. Execution State Tools

These tools expose the lifecycle state of execution work.

### Purpose
To let the runtime and operator inspect and update execution work units without collapsing execution truth into planning truth.

### Allowed operations
Read:
- get execution item by id
- list execution items by project
- list execution items by status or lifecycle state
- inspect execution blockers and unresolved conditions

Write:
- mark execution item active
- mark execution item blocked
- mark execution item paused
- mark execution item partially completed
- mark execution item completed
- record failure state with bounded explanation

### Constraints
- execution items must remain traceable to approved handoff or equivalent execution authorization
- execution item mutations must not become planning-state mutation by proxy
- execution tools must not create new planning structure

---

## 2. Content Graph Tools

These tools expose and mutate the content graph V Forge owns.

### Purpose
To let V Forge maintain the structural record of what was built.

### Allowed operations
Read:
- get page records
- get topic records
- get entity records
- get internal link relationships
- get archetype assignments
- get schema usage relationships
- inspect graph relationships for a project

Write:
- create page record
- update page record
- create topic or entity record where execution legitimately requires it
- link page to topic/entity/archetype/schema usage
- record internal links
- update graph relationships after execution work changes structure

### Constraints
- all graph records must remain project-scoped
- no cross-project graph connections
- content graph mutation must reflect execution truth, not hypothetical planning structure
- graph writes must not become freeform strategy modeling

---

## 3. Owned Surface Operation Tools

These tools expose and update owned/branded execution surface state inside V Forge’s current bounded model.

### Purpose
To let V Forge operate the project’s owned execution footprint across relevant surfaces.

### Allowed operations
Read:
- inspect owned surface records
- inspect publication/release state
- inspect execution-side maintenance state
- inspect what execution work has been applied to a surface

Write:
- record execution work applied to a surface
- update owned surface operational state where execution owns that state
- record maintenance completion or maintenance blockers
- attach execution-side notes relevant to repeatable operation

### Constraints
- this is not a generalized future surface-condition system beyond admitted first-pass scope
- do not silently design the future surface execution condition model into every current tool
- owned surface state remains execution truth, not observatory signal

---

## 4. Release and Publication Continuity Tools

These tools manage the continuity of what was published or released as part of owned execution.

### Purpose
To preserve structured continuity for publication and release without confusing it with planning authority.

### Allowed operations
Read:
- inspect release records
- inspect publication history
- inspect publication state by asset or surface

Write:
- create release/publication record
- update release/publication state
- record release or publication outcome
- record rollback, failed release, or blocked publication

### Constraints
- release/publication records are execution continuity, not planning truth
- public-facing or launch-sensitive changes may require stronger approval posture before action tools are admitted
- publication continuity must remain bounded to owned execution surfaces

---

## 5. Execution Reporting and Findings Tools

These tools expose and write bounded execution-side reporting.

### Purpose
To preserve honest execution truth and bounded findings during or after execution.

### Allowed operations
Read:
- inspect execution reports
- inspect bounded findings
- inspect blocked/failed/partial execution history

Write:
- create execution report
- create bounded finding
- update finding classification where execution truth becomes clearer
- record whether a finding is execution-local or return-to-planning relevant

### Constraints
- findings are not planning decisions
- reports are not automatic replanning triggers
- execution reporting must preserve uncertainty and partial completion honestly

---

## 6. Return-to-Planning Tools

These tools route bounded execution findings back to Project V through the governed interface.

### Purpose
To let V Forge return planning-relevant execution findings without collapsing ownership.

### Allowed operations
Read:
- inspect prior return packages
- inspect return status for a finding or execution item

Write:
- create return-to-planning package
- attach bounded supporting execution context to a return package
- mark return package sent or acknowledged through the governed interface

### Constraints
- these tools do not mutate Project V planning truth directly
- these tools do not create planning records inside V Forge
- these tools must remain aligned to `v-forge-to-project-v-return-to-planning-interface.md`

---

## 7. Execution Intelligence Read Tools

These tools expose bounded execution intelligence V Forge derives by crossing its content graph against VEDA signal.

### Purpose
To let the runtime and operator inspect execution-side analytical outputs without turning V Forge into the signal system.

### Allowed operations
Read:
- inspect execution intelligence summaries
- inspect graph-vs-signal gap views
- inspect execution-side performance mismatch indicators

### Constraints
- these are read tools in first-pass posture
- raw observatory signal remains VEDA-owned
- execution intelligence results must remain execution intelligence, not raw signal ownership
- V Forge must not accumulate open-ended observatory archives as part of this tool family

---

## 8. Bounded Execution Validation Tools

These tools support bounded validation needed to continue or safely complete approved execution.

### Purpose
To validate execution prerequisites, local conditions, or bounded execution assumptions.

### Allowed operations
Read / action within bounds:
- inspect local execution prerequisites
- validate publication readiness conditions already inside V Forge scope
- validate whether execution-local dependencies are present
- record validation outcome inside execution truth

### Constraints
- these are execution-supporting tools, not general research tools
- they must not become open-ended market or signal gathering
- if validation reveals planning-level significance, the correct path is report + return, not silent scope expansion

---

## Tools V Forge Must Not Expose

The V Forge MCP surface must not expose tools that make V Forge behave like another system.

### Forbidden tool categories
- create or mutate Project V planning records
- create governing decisions for Project V
- mutate VEDA observatory truth
- maintain raw signal archives as V Forge-owned truth
- configure VEDA provider scope
- create new projects as canonical ecosystem entities
- perform unrestricted open-ended market research under the guise of execution
- self-authorize high-risk external or paid actions

If a tool would make V Forge act like Project V or VEDA, the tool should not exist on the V Forge MCP surface.

---

## Read vs Write Admission Rules

### Read admission
Read tools may be admitted when:
- they are relevant to the current execution task
- they remain inside project scope
- they preserve ownership boundaries

### Write admission
Write tools may be admitted when:
- the action is inside approved execution scope
- the current workflow and governance posture allow the mutation
- the mutation updates V Forge-owned truth rather than another system’s truth

### High-discipline action admission
High-discipline action tools may be admitted only when:
- the relevant governance posture is satisfied
- the operator/runtime is in the correct execution phase
- the action’s scope is explicit and bounded
- the session tool posture is intentionally narrowed and reviewed where required

Tool admission must not default to “available unless forbidden.”
It should default to “absent unless admitted.”

---

## Relationship to Extension Runtime Tool Surface

The V Forge MCP surface is not the same thing as the active session tool surface inside the extension.

The V Forge MCP surface defines what V Forge can expose.
The session tool surface defines what the runtime actually admits for the current session.

This means:
- not every V Forge MCP tool appears in every V Forge session
- delegated workers may receive narrower V Forge tool subsets than the parent session
- high-discipline action tools may be absent even in a V Forge session if the current posture does not admit them

The extension runtime must assemble V Forge tools according to:
- current system posture
- project scope
- workflow/gating posture
- current task objective
- delegated-role narrowing where applicable

---

## Cross-System Relationship Rules

### Relationship to Project V
V Forge MCP tools may consume handoff context and emit return-to-planning packages.
They must not mutate Project V planning truth directly.

### Relationship to VEDA
V Forge MCP tools may read bounded VEDA-derived signal through governed interfaces where execution intelligence or execution validation requires it.
They must not become VEDA-owned signal archives or signal mutation tools.

### Rule
Cross-system context consumption does not transfer ownership.
Cross-system tool availability does not authorize cross-system truth mutation.

---

## Governance and Halt Rules for the MCP Surface

The MCP surface must preserve V Forge’s governed execution posture.

### Halt conditions
The runtime or tool layer must halt or withhold relevant write/action tools when:
- scope is unclear
- approval posture is unclear for the action class
- the tool would exceed approved execution scope
- the action would cross into planning or observatory ownership
- a high-discipline action lacks the required authorization basis

### Honesty rule
A tool should not be exposed in a misleading posture.
If the runtime knows a launch-sensitive publication action cannot proceed legitimately, it should not expose it as casually callable and merely fail later by surprise.

---

## Operator and LLM Mental Model

A capable operator or LLM should understand the V Forge MCP surface as:
- the bounded execution interface for what V Forge owns
- the place where execution truth, content graph truth, publication continuity, and bounded execution findings are made operable
- not the place where planning truth is created
- not the place where observatory truth is owned
- not the place where approval requirements disappear

If the MCP surface reads like “tools to do whatever is useful,” it is wrong.
It should read like “tools to execute what V Forge legitimately owns.”

---

## Anti-Drift Rules

### 1. No planner-by-tools rule
Do not expose V Forge tools that let execution silently become planning.

### 2. No observatory-by-tools rule
Do not expose V Forge tools that let execution silently become signal ownership.

### 3. No open-ended research rule
Do not expose research helpers that are not bounded to execution support.

### 4. No tool-availability-is-permission rule
Tool existence does not erase workflow or governance requirements.

### 5. No cross-project graph contamination rule
Content graph tools must remain project-scoped.

### 6. No high-discipline casual exposure rule
Launch-sensitive, public-facing, external, or paid action tools must not appear in casual always-on posture.

---

## Usage

This document should be used:
- when designing or reviewing the V Forge MCP server surface
- when deciding which tool families belong in first-pass V Forge operability
- when checking whether a proposed V Forge tool would violate ownership or governance boundaries
- when assembling V Forge tool subsets inside the extension runtime
- when reviewing whether V Forge operability is drifting into planning or observability ownership

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `data-boundaries.md`
- `reporting-and-approval-model.md`
- `human-in-the-loop-doctrine.md`
- `surface-execution-state-design-note.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/mcp-coordination-model.md`
- `../interfaces/extension-system-init-and-tool-surface-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
