# V Forge Content Graph Operations

## Purpose

This document defines how V Forge operates the content graph it owns as execution truth inside the V Ecosystem.

It exists to answer:

```text
How should V Forge create, update, maintain, validate, and use the content graph as execution truth for built assets without turning the graph into planning truth, signal truth, or cross-project structural contamination?
```

This is a Tier 2 V Forge implementation-build-spec authority document.

---

## Scope

This document governs:

- the operational role of the content graph inside V Forge
- the core operational actions performed on content graph records
- how content graph operations relate to execution work units
- when graph records are created, updated, or retired
- integrity and validation posture for graph operations
- how graph operations support execution intelligence without absorbing signal ownership
- anti-drift rules that keep the content graph as execution truth rather than planning or observatory truth

---

## Out of Scope

This document does not define:

- the full database schema for content graph records
- the exact MCP wire schema for every graph-related tool
- the detailed experimentation or optimization layer
- future commercial/runtime graph extensions
- raw observatory signal storage or provider integrations

Those belong in schema, MCP, observability, or later V Forge docs.

---

## System

- v-forge

---

## Core Rule

The V Forge content graph is the structural record of what was actually built.

Content graph operations must preserve that truth honestly.
The graph must reflect execution reality, remain project-scoped, stay structurally coherent, and support execution intelligence without becoming planning structure or signal ownership.

If the graph gets ahead of what was built, lags behind what changed materially, or starts modeling hypothetical future structure, the graph is wrong.

---

## Content Graph Operational Definition

The content graph is the project-scoped structural model of owned execution assets and their relationships.

At minimum, it includes execution-side records such as:
- pages or equivalent content assets
- topics
- entities
- internal links
- archetypes
- schema usage
- execution-owned graph relationships between those records

Operationally, the content graph exists so V Forge can:
- preserve structural execution truth
- inspect what has been built
- update structural truth as execution changes assets
- support execution intelligence by crossing structure against VEDA signal
- support maintenance, reporting, and bounded execution review

The graph is not a hypothetical plan.
It is not a market map.
It is not an observatory archive.

---

## Graph Ownership Principle

V Forge owns the content graph because the graph describes what execution has built.

This means:
- graph records are execution truth
- graph records are created and updated from execution events and execution-owned review
- graph records must not be treated as planning truth just because they are useful upstream
- graph records must not become VEDA-owned observatory truth just because they are useful for analysis

Ownership of the graph remains in V Forge even when other systems consume bounded outputs derived from it.

---

## Operational Goals

Content graph operations should achieve all of the following:

1. keep the graph aligned with actual built assets
2. keep graph relationships coherent and project-scoped
3. preserve enough continuity that later execution review is possible
4. support bounded execution intelligence reads
5. make maintenance and structural correction operable without planning drift

A graph operation that makes the graph more convenient but less truthful is a bad operation.

---

## Core Graph Operations

V Forge content graph operations should be understood through the following operational categories.

## 1. Registration Operations

Registration operations create the initial graph record for an execution-built asset or relationship.

Examples:
- create page record after a page is actually built
- register a topic record when the built execution asset now legitimately requires it
- register a page-topic relationship after the relationship exists in execution truth
- register internal links actually created in the built asset
- register schema usage actually applied to an asset

### Rule
Registration follows execution truth.
It does not precede it as hypothetical structure modeling.

---

## 2. Update Operations

Update operations modify graph records when execution materially changes built structure.

Examples:
- update a page record after a material execution-side revision
- update internal link relationships after structure changes
- update schema usage after structured data changes
- update archetype assignment if the execution asset materially changed type

### Rule
An update operation must reflect a real structural change in execution truth.
It must not be used to quietly remodel the graph into what planning wishes existed.

---

## 3. Relationship Operations

Relationship operations create, change, or retire graph relationships.

Examples:
- connect page to topic
- connect page to entity
- connect page to archetype
- connect page to schema usage
- record internal links between pages
- retire obsolete relationships after real structural change

### Rule
Relationships must remain:
- project-scoped
- execution-grounded
- structurally coherent
- free of hypothetical future-state assumptions

---

## 4. Validation Operations

Validation operations inspect graph integrity and graph-to-execution alignment.

Examples:
- confirm page records correspond to actual built assets
- confirm graph relationships are project-scoped
- confirm links reference valid graph nodes
- confirm structural registration completed after execution change
- confirm no stale structural assumptions remain after major execution work

### Rule
Validation exists to protect graph truth.
It does not create permission to rebuild the graph speculatively.

---

## 5. Correction Operations

Correction operations fix graph truth when the graph and execution reality drift apart.

Examples:
- repair incorrect graph relationships
- correct wrong archetype assignment
- remove or retire graph relationships that no longer exist in execution truth
- align graph state after incomplete or failed structural registration

### Rule
Correction operations restore truth.
They must not smuggle in new planning structure under the banner of cleanup.

---

## 6. Inspection Operations

Inspection operations read graph state for operators, LLMs, or bounded execution intelligence.

Examples:
- inspect page neighborhood
- inspect topic coverage within the graph
- inspect internal link structure
- inspect entity relationships
- inspect schema usage footprint
- inspect graph completeness for a bounded execution target

### Rule
Inspection may inform planning or execution review, but inspection output does not change graph truth by itself.

---

## Graph Lifecycle Rule

Content graph records should follow the execution lifecycle of the built assets they describe.

At a minimum, graph operations must preserve the idea that:
- a record is registered when the relevant asset or relationship becomes real in execution
- a record is updated when execution changes it materially
- a record may be retired, deactivated, or marked obsolete when execution truth no longer supports its active form
- historical continuity should remain available where it matters for execution review

The graph must not represent assets that only exist as proposals.

---

## Registration Timing Rule

A graph record should be registered at the earliest point where the relevant execution truth is real enough to be durable.

This means:
- not so early that the graph models work that does not yet exist
- not so late that structural truth lags behind execution materially

In practice:
- draft planning intent is too early
- actual built or materially changed asset state is the right trigger
- known incomplete or failed work should be reflected honestly rather than hidden from the graph when structural registration already partially occurred

---

## Partial and Failed Operation Rule

Content graph operations must preserve honesty under partial or failed execution.

When execution only partially completes a structural change:
- the graph must not pretend the full intended structure now exists
- partial registration must either be reflected explicitly or corrected back to the last truthful stable state

When a graph operation fails:
- failure must be preserved as execution truth where it matters
- the system must not quietly leave the graph in a misleading half-updated state without visible correction or repair posture

Truthful partial state is better than confident structural fiction.

---

## Project Scope Integrity Rule

All content graph operations must remain project-scoped.

This means:
- every graph node belongs to exactly one project
- every graph relationship joins records from the same project only
- no cross-project links, topics, entities, or structural joins may be created
- graph reads and writes must respect the active session token project scope

Cross-project graph contamination is a structural failure, not a minor bug.

---

## Graph Integrity Rule

Content graph operations must preserve structural integrity.

At minimum, this means:
- relationships point only to valid records
- required parent or related records exist where the graph model requires them
- retired or obsolete records do not continue to appear as active truth without justification
- duplicated structural truth is minimized and never allowed to create contradictory graph state

A graph that is convenient but structurally incoherent is not acceptable execution truth.

---

## Graph vs Planning Rule

The content graph must not become a shadow planning model.

This means graph operations must not be used to:
- pre-model assets that are only planned
- encode future desired structure as though it already exists
- replace Project V planning records with graph nodes
- turn graph completeness into planning approval

The graph describes what execution has built.
It does not describe what planning hopes will eventually exist unless and until execution makes it real.

---

## Graph vs Signal Rule

The content graph must not become a shadow observatory.

This means graph operations must not be used to:
- store raw VEDA signal as graph-owned truth
- encode observatory signal as if it were structural execution state
- accumulate open-ended signal context in graph records for convenience

The graph may be crossed against VEDA signal to produce execution intelligence.
That does not make the signal part of graph ownership.

---

## Graph and Execution Intelligence Rule

Execution intelligence may read the content graph heavily.
It may compare graph structure against VEDA signal.

But:
- execution intelligence does not authorize graph mutation by itself
- signal mismatch does not automatically mutate graph truth
- observed performance gaps do not become structural graph facts until execution changes the structure or bounded correction confirms a graph-truth issue

Graph mutation must remain grounded in execution truth, not analytical temptation.

---

## Graph Correction vs Planning Return Rule

When graph inspection reveals a problem, V Forge must distinguish between:

### Execution-local correction
Use when:
- the graph is wrong relative to actual execution truth
- the fix is bounded to restoring truthful structural state
- no planning-level reinterpretation is required

### Return-to-planning
Use when:
- the graph issue reflects a planning-level contradiction
- the structural problem cannot be resolved without changing what should be built next
- the corrective path would effectively widen execution scope or alter planning truth

Graph correction is not a loophole for silent replanning.

---

## Maintenance Rule

Content graph operations are part of maintenance as well as fresh execution.

Maintenance may include:
- structural corrections
- cleanup of obsolete relationships after real execution change
- bounded graph refresh after maintenance work on built assets
- validating that graph truth still matches owned execution surfaces

Maintenance remains execution work.
It must stay bounded and truthful.

---

## Operator and LLM Inspection Rule

Operators and LLMs may inspect the content graph to understand execution reality.

They should be able to answer questions such as:
- what assets exist
- how those assets are structurally related
- what topics/entities/archetypes are currently represented
- what schema usage exists
- where graph structure appears incomplete or inconsistent

Inspection is powerful.
It must not be confused with authority to mutate graph truth outside governed execution bounds.

---

## Governance and Halt Rule

Graph operations must halt or withhold mutation when:
- project scope is unclear
- the operation would create cross-project contamination
- the mutation would encode hypothetical planning structure
- the mutation would effectively absorb observatory signal into graph truth
- the operation would exceed approved execution scope

A graph operation that cannot be justified as execution-truth maintenance must not proceed.

---

## Human-In-The-Loop Principle

Human review remains especially important when graph operations involve:
- major structural corrections
- large-scale relationship repair
- graph state that may affect public-facing release behavior
- ambiguity about whether a graph problem is execution-local or planning-level
- situations where correction, rollback, or return-to-planning may materially change next steps

The graph should become more legible and governable through operations, not more magical.

---

## Anti-Drift Rules

### 1. No hypothetical graph rule
Do not model future desired structure as if it already exists.

### 2. No cross-project contamination rule
Do not create graph nodes or relationships that cross project boundaries.

### 3. No signal-ownership-by-graph rule
Do not turn observatory inputs into graph-owned truth.

### 4. No planner-by-graph rule
Do not use graph operations to recreate planning state inside V Forge.

### 5. No silent half-update rule
Do not leave graph truth in misleading partial state without explicit correction or partial-state honesty.

### 6. No analytics-driven mutation rule
Do not let execution intelligence or signal mismatch mutate graph truth automatically.

---

## LLM Use Principle

A capable LLM should be able to infer from this document that:
- the content graph is the structural record of what execution has actually built
- graph operations follow execution truth rather than leading it
- graph mutation is bounded by project scope and execution scope
- graph inspection is powerful but not self-authorizing
- graph correction is different from planning change
- signal may inform graph review but does not become graph-owned truth

If an LLM could use this document to justify building hypothetical future structure into the graph, absorbing observatory signal into graph records, or using graph mutation as silent replanning, this document is failing.

---

## Usage

This document should be used:
- when designing or reviewing content graph-related MCP tools
- when deciding when graph records should be registered, updated, validated, or corrected
- when checking whether a graph issue is execution-local or planning-level
- when reviewing whether graph operations preserve execution truth and project scope integrity
- when evaluating whether V Forge is drifting toward shadow planning or shadow observatory behavior through graph operations

---

## Related Docs

- `v-forge.md`
- `system-invariants.md`
- `operational-model.md`
- `mcp-surface.md`
- `content-lifecycle-workflow.md`
- `data-boundaries.md`
- `schema-specification.md`
- `surface-execution-state-design-note.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
