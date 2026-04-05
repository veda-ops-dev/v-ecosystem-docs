# Cross-System Access Governance Addendum

## Purpose

This document adds governed access rules to the cross-system boundary model.

It exists to answer:

```text
How does the V Ecosystem distinguish between ownership boundaries and access boundaries, what are the rules for broad governed access that does not collapse ownership, and how is cross-system access tracked and audited?
```

This is a Tier 1 ecosystem authority document.

This document extends `cross-system-boundaries.md`. It does not replace it. Ownership rules in `cross-system-boundaries.md` remain authoritative.

---

## Scope

This document governs:

- the distinction between ownership boundaries and access boundaries
- the principle that access can be broad while ownership stays narrow
- access governance requirements (logging, attribution, cost accounting)
- the relationship between access scope and planning authority
- anti-drift rules specific to cross-system access

---

## Out of Scope

This document does not define:

- specific query types or API contracts for individual cross-system interfaces
- implementation-level access control mechanisms
- project-specific access configurations
- detailed MCP tool schemas

Those belong in interface-specific docs and implementation docs.

---

## System

- ecosystem

---

## Core Principle

**Own narrowly. Access broadly. Govern the access.**

The V Ecosystem separates two concerns that are often conflated:

- **Ownership boundaries** — which system is the source of truth for which kind of data. These are strict. They do not relax.
- **Access boundaries** — which systems may read data from other systems during operation. These can be broad, provided the access is governed.

Restricting access does not protect ownership. Governance protects ownership. A system that reads evidence from another system is not absorbing ownership. A system that reads evidence and then makes decisions that belong to another system's authority is violating ownership — and that violation happens regardless of whether the access was restricted.

The correct approach is: let systems access what they need to do their jobs well, and govern how that access is used so ownership stays clear.

---

## Ownership Boundaries (Unchanged)

These rules are restated from `cross-system-boundaries.md` for clarity. They are not new.

- Project V owns planning truth, orchestration truth, readiness truth, decision truth, and handoff truth.
- VEDA owns signal truth, evidence truth, and observability truth.
- V Forge owns execution truth, implementation truth, the content graph, and execution intelligence.

No cross-system access changes these ownership assignments.

Reading VEDA evidence does not make V Forge the evidence owner.
Reading V Forge execution results does not make Project V the execution owner.
Reading Project V planning state does not make VEDA the planner.

---

## Access Governance Requirements

Any system accessing another system's data must satisfy these requirements:

### 1. Access must be logged

Every cross-system data access must produce an activity log entry with:

- the requesting system and actor (agent, session, or service)
- the target system
- the query type and parameters
- the result scope (count, coverage)
- the timestamp
- the token cost, if applicable

Access that is not logged is ungoverned access. Ungoverned access is not permitted.

### 2. Access must be scoped

Cross-system queries must carry explicit scope parameters. The minimum scope is project-level. Unscoped queries that return data across all projects are not permitted through cross-system interfaces.

The target system enforces scoping. The requesting system cannot bypass it.

### 3. Results must carry provenance

Data returned through cross-system access must carry provenance metadata identifying:

- the source system
- the record identifier in the source system
- the timestamp of the data (when it was gathered or created)
- the freshness or trust classification, where applicable

The requesting system must preserve this provenance when using the data in its own outputs.

### 4. Access must be cost-accountable

Cross-system queries consume resources (tokens, API calls, compute). The cost of cross-system access counts against the requesting system's budget, not the target system's budget.

If the requesting system has a budget policy in effect, cross-system query costs are included in budget evaluation.

### 5. Access does not grant authority

Reading another system's data does not grant the requesting system authority to make decisions that belong to the target system's domain.

V Forge reading VEDA evidence does not authorize V Forge to make planning decisions.
Project V reading V Forge execution results does not authorize Project V to modify executed content directly.

The authority boundary is enforced by the requesting system's operating doctrine, not by restricting read access.

---

## Access Scope by System Pair

### V Forge → VEDA (Evidence Access)

Access type: Read-only, project-scoped, execution-time queries.

Governed by: `v-forge-evidence-access-contract.md`

Purpose: V Forge queries VEDA evidence to improve execution quality, validate outputs against current signals, and identify maintenance priorities.

Boundary: Evidence use must improve approved work quality, not change what work is approved.

### V Forge → Project V (Planning Context)

Access type: Read-only, project-scoped, limited to active handoff context.

Governed by: `project-v-to-v-forge-handoff-interface.md`

Purpose: V Forge reads the approved handoff, project structure, and planning context that defines what it should execute.

Boundary: V Forge reads planning context to understand what to do. It does not modify planning state.

### Project V → VEDA (Signal for Planning)

Access type: Read-only, project-scoped or ecosystem-scoped for market scanning.

Governed by: `veda-to-project-v-signal-interface.md`

Purpose: Project V queries VEDA signal and evidence to inform planning decisions, readiness evaluations, and project creation.

Boundary: Project V uses evidence to make planning decisions. It does not own the evidence. Evidence provenance must be preserved in planning records.

### Project V → V Forge (Execution Results)

Access type: Read-only, project-scoped.

Governed by: `v-forge-to-project-v-return-to-planning-interface.md`

Purpose: Project V reads V Forge execution findings, completion reports, and maintenance signals to inform replanning.

Boundary: Project V reads execution results. It does not modify V Forge execution state or content graph directly.

### VEDA → V Forge (Not Applicable)

VEDA does not query V Forge. VEDA observes external reality, not internal execution state. If VEDA needs to observe the effect of executed work (e.g., monitoring a published page's search performance), it observes through external provider APIs, not through V Forge's internal systems.

### VEDA → Project V (Not Applicable)

VEDA does not query Project V. VEDA provides signal to Project V through governed interfaces. VEDA does not read planning state.

---

## Anti-Drift Rules for Cross-System Access

### Access frequency does not imply ownership

A system that queries another system frequently is still not the owner of that data. Frequency of access is a cost concern, not an ownership concern.

### Caching does not create a second source of truth

If a system caches cross-system data for performance, the cache is not authoritative. The source system remains the authority. Cached data must carry provenance and must be treated as potentially stale.

Caching for within-session use is acceptable. Persistent cross-session caches of another system's data are not acceptable without explicit doctrine support.

### Access patterns must remain classifiable

If a cross-system access pattern cannot be clearly described as "system X reads system Y's data to do Z," the access pattern needs governance review. Unclassifiable access patterns are a sign of boundary drift.

### Broad access is not a backdoor

Broadening access is not a substitute for proper handoff, interface, or workflow design. If V Forge needs planning authority, the answer is to route through Project V, not to broaden V Forge's access to planning data and let the agent figure it out.

---

## Usage

This document should be used:

- when designing new cross-system interfaces to determine appropriate access scope
- when evaluating whether an existing access pattern respects ownership boundaries
- when building activity logging for cross-system access
- when reviewing budget policies that account for cross-system query costs
- when an LLM or operator needs to understand why access is broad but ownership is strict

---

## Related Docs

- `cross-system-boundaries.md`
- `../interfaces/v-forge-evidence-access-contract.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/agent-operating-doctrine.md`
