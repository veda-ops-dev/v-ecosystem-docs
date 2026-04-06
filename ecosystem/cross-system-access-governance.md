# Cross-System Access Governance Addendum

## Purpose

This document adds governed access rules to the cross-system boundary model.

It exists to answer:

```text
How does the V Ecosystem distinguish between ownership boundaries and access boundaries, what are the rules for governed access that does not collapse ownership, and how is cross-system access tracked and audited?
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
- **Access boundaries** — which systems may read or receive data from other systems during operation. These can be broad, provided the access is governed.

Restricting access does not protect ownership. Governance protects ownership. A system that reads evidence from another system is not absorbing ownership. A system that reads evidence and then makes decisions that belong to another system's authority is violating ownership — and that violation happens regardless of whether the access was restricted.

The correct approach is: let systems access what they need to do their jobs well, and govern how that access is used so ownership stays clear.

---

## Ownership Boundaries (Unchanged)

These rules are restated from `cross-system-boundaries.md` for clarity. They are not new.

- Project V owns planning truth, orchestration truth, readiness truth, decision truth, and handoff truth.
- VEDA owns signal truth, evidence truth, and observability truth.
- V Forge owns execution truth, implementation truth, the content graph, and execution intelligence.

No cross-system access changes these ownership assignments.

Reading or receiving VEDA signal does not make Project V or V Forge the signal owner.
Reading V Forge execution findings does not make Project V the execution owner.
Receiving planning context from Project V does not make V Forge the planner.

---

## Access Governance Requirements

Any system accessing or receiving data from another system must satisfy these requirements:

### 1. Access must be logged

Every cross-system data access must produce an activity log entry with:

- the requesting or receiving system and actor (agent, session, or service)
- the target or source system
- the interaction type and parameters
- the result scope (count, coverage)
- the timestamp
- the token cost, if applicable

Access that is not logged is ungoverned access. Ungoverned access is not permitted.

### 2. Access must be scoped

Cross-system interactions must carry explicit scope parameters. The minimum scope is project-level.

**Project-scoped interactions** are the default for all runtime execution. A query or delivery that returns or transfers data across all projects without a project scope qualifier is not permitted through cross-system interfaces.

**Portfolio-scoped interactions** are permitted only for planning-level market signal gathering by Project V, where VEDA provides signal relevant to opportunity evaluation across projects. Portfolio-scoped access must still be explicitly authorized by the requesting context, must be logged, and must identify the portfolio or ecosystem scope explicitly rather than defaulting to unscoped. Portfolio-scoped access does not grant Project V ownership of VEDA signal.

The target system enforces scoping. The requesting system cannot bypass it.

### 3. Results must carry provenance

Data returned or delivered through cross-system access must carry provenance metadata identifying:

- the source system
- the record identifier in the source system
- the timestamp of the data (when it was gathered or created)
- the freshness or trust classification, where applicable

The receiving system must preserve this provenance when using the data in its own outputs.

### 4. Access must be cost-accountable

Cross-system interactions consume resources (tokens, API calls, compute). The cost of cross-system access counts against the requesting or receiving system's budget, not the source system's budget.

If the requesting system has a budget policy in effect, cross-system interaction costs are included in budget evaluation.

### 5. Access does not grant authority

Receiving another system's data does not grant the receiving system authority to make decisions that belong to the source system's domain.

V Forge receiving VEDA signal does not authorize V Forge to make planning decisions.
Project V receiving V Forge execution findings does not authorize Project V to modify executed content directly.

The authority boundary is enforced by the receiving system's operating doctrine, not by restricting access.

---

## Access Scope by System Pair

All six system-pair interactions are listed. Each entry states who initiates the interaction, what the allowed access pattern is, and which interface doc governs it.

---

### VEDA → Project V (Signal Delivery)

**Direction:** VEDA delivers bounded planning-relevant signal to Project V.

**Access type:** Read-only output from VEDA; project-scoped or portfolio-scoped for planning-level market evaluation (see scoping rules above).

**Governed by:** `veda-to-project-v-signal-interface.md`

**Purpose:** VEDA provides signal and evidence packages to Project V for planning interpretation. Project V uses the signal to inform project creation, prioritization, readiness evaluation, and replanning decisions.

**Boundary:** VEDA remains the owner of signal and evidence truth. Project V interprets signal for planning purposes. Receiving signal does not transfer signal ownership or signal-system responsibility to Project V.

---

### VEDA → V Forge (Signal Delivery)

**Direction:** V Forge consumes bounded observatory signal from VEDA.

**Access type:** Read-only, project-scoped, execution-time queries or bounded signal package consumption.

**Governed by:** `veda-to-v-forge-signal-interface.md` and `v-forge-evidence-access-contract.md`

**Purpose:** V Forge consumes VEDA signal to power its execution intelligence layer — understanding how built content is performing externally and where execution-side gaps exist.

**Boundary:** VEDA remains the owner of all observatory records and signal truth. V Forge uses consumed signal to produce execution intelligence. Consuming signal does not make V Forge the observer or the evidence owner.

---

### Project V → V Forge (Handoff Delivery)

**Direction:** Project V delivers a bounded handoff package to V Forge when planning-ready work is authorized for execution.

**Access type:** Project V initiates handoff; V Forge receives the execution-facing planning package. Project-scoped.

**Governed by:** `project-v-to-v-forge-handoff-interface.md`

**Purpose:** Project V transfers execution responsibility for approved work to V Forge by delivering the bounded handoff package containing execution scope, constraints, evidence references, and expected outcomes.

**Boundary:** The handoff transfers execution responsibility, not planning ownership. Project V remains the planning system of record. V Forge becomes the execution system of record for the handed-off scope. The handoff must satisfy the validity conditions defined in the handoff interface.

---

### V Forge → Project V (Return-to-Planning Delivery)

**Direction:** V Forge delivers bounded execution findings to Project V when execution requires planning reconsideration.

**Access type:** V Forge initiates return; Project V receives the bounded execution findings package. Project-scoped.

**Governed by:** `v-forge-to-project-v-return-to-planning-interface.md`

**Purpose:** V Forge surfaces blocked, failed, incomplete, or changed execution conditions to Project V through the governed return-to-planning path. Project V uses the findings to evaluate whether replanning, deferral, revised handoff, or no-action is warranted.

**Boundary:** The return-to-planning transfer delivers bounded execution findings, not full execution state ownership. V Forge remains the execution system of record. Project V receives findings as planning-reconsideration input. Returned findings do not automatically mutate planning truth.

---

### V Forge → VEDA (Not an interaction)

V Forge does not query or write to VEDA. V Forge consumes bounded signal from VEDA (see VEDA → V Forge above). V Forge does not observe external reality on VEDA's behalf.

If V Forge needs external signal that VEDA is not currently providing, the correct path is to direct VEDA to expand its observatory scope through the governed operator surface — not for V Forge to build independent observatory capability.

---

### VEDA → VEDA / Project V → Project V / V Forge → V Forge (Internal)

Internal system operations are not governed by this document. Each system governs its own internal data access through its own schema, invariant, and API governance docs.

---

## Anti-Drift Rules for Cross-System Access

### Access frequency does not imply ownership

A system that receives data from another system frequently is still not the owner of that data. Frequency of access is a cost concern, not an ownership concern.

### Caching does not create a second source of truth

If a system caches cross-system data for performance, the cache is not authoritative. The source system remains the authority. Cached data must carry provenance and must be treated as potentially stale.

Caching for within-session use is acceptable. Persistent cross-session caches of another system's canonical data are not acceptable without explicit doctrine support.

### Access patterns must remain classifiable

If a cross-system interaction cannot be clearly described as one of the six patterns above, the pattern needs governance review before implementation. Unclassifiable access patterns are a sign of boundary drift.

### Portfolio-scoped access is not unscoped access

Portfolio-scoped access for Project V planning market evaluation is explicitly permitted under defined conditions. It is not the same as unscoped access with no project parameter. Portfolio scope must be declared, logged, and bounded. It does not become a general license to return all-projects data through any interface.

### Delivery is not ownership transfer

VEDA delivering signal to Project V or V Forge does not transfer observatory ownership. Project V delivering a handoff to V Forge does not transfer planning ownership. V Forge delivering return findings to Project V does not transfer execution ownership. Delivery is a governed exchange. It is not a merge of truth domains.

### Broad access is not a backdoor

Broadening access is not a substitute for proper handoff, interface, or workflow design. If V Forge needs planning authority, the answer is to route through the governed return-to-planning path, not to broaden V Forge's access to planning data and let the agent figure it out.

---

## Usage

This document should be used:

- when designing new cross-system interfaces to determine appropriate access scope and direction
- when evaluating whether an existing access pattern respects ownership boundaries
- when building activity logging for cross-system access
- when reviewing budget policies that account for cross-system interaction costs
- when an LLM or operator needs to understand why access is broad but ownership is strict
- when checking whether a proposed interaction fits one of the six defined system-pair patterns

---

## Related Docs

- `cross-system-boundaries.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/veda-to-v-forge-signal-interface.md`
- `../interfaces/v-forge-evidence-access-contract.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/agent-operating-doctrine.md`
