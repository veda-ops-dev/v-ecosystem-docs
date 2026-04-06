# V Forge Evidence Access Contract

## Purpose

This document defines the governed evidence access contract that allows V Forge agents to query VEDA evidence during execution.

It exists to answer:

```text
What evidence can V Forge agents query from VEDA at execution time, how must those queries be scoped and logged, what freshness and attribution requirements apply, what is the boundary between using evidence to improve execution quality and using evidence to make planning decisions, and how does the ecosystem prevent broad evidence access from collapsing into ownership blur?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the query types V Forge agents may issue against VEDA evidence
- required scoping parameters for every query
- freshness metadata requirements on evidence responses
- attribution requirements when V Forge uses VEDA evidence in outputs
- activity logging requirements for every evidence access
- token and cost accounting for evidence queries
- the decision boundary that separates execution-quality use from planning-authority use
- degraded-mode behavior when VEDA evidence is unavailable or stale
- anti-drift rules that prevent evidence access from becoming ownership absorption

This document extends and complements:
- `veda-to-v-forge-signal-interface.md` — the existing signal consumption interface
- `../ecosystem/cross-system-boundaries.md` — system ownership rules
- `../v-forge/data-boundaries.md` — V Forge data boundary posture
- `../governance/agent-operating-doctrine.md` — agent behavior constraints

---

## Out of Scope

This document does not define:

- the internal VEDA API implementation
- the exact MCP tool schemas for evidence queries
- VEDA's internal storage, indexing, or retrieval mechanics
- the content of specific evidence records
- V Forge's internal execution intelligence algorithms
- provider-specific data formats within VEDA

Those belong in VEDA-specific, V Forge-specific, and implementation docs.

---

## System

- interfaces

---

## Core Rule

V Forge agents may actively query VEDA evidence during execution.

This access is governed, not gated.

The principle is: **own narrowly, access broadly, govern the access.**

V Forge does not become an observer by reading evidence.
V Forge does not acquire planning authority by seeing market data.
V Forge improves execution quality by working with current evidence instead of stale handoff snapshots.

If evidence access makes execution better without making authority harder to trace, the access model is working. If evidence access causes V Forge to make planning decisions, bypass approval gates, or accumulate its own evidence store, the access model has failed.

---

## Why This Contract Exists

The existing `veda-to-v-forge-signal-interface.md` defines VEDA signal consumption as a bounded, largely passive channel. That design protects ownership boundaries but starves V Forge agents of the evidence they need to execute well.

Problems with restricted access:

- **Stale handoff evidence.** If all VEDA evidence reaches V Forge only through Project V handoff packets, the evidence is frozen at handoff time. Execution that runs for days or weeks works against outdated context.
- **Duplicate research.** V Forge agents performing bounded execution-side research may re-discover things VEDA has already captured, wasting tokens and time.
- **Blind maintenance.** V Forge maintenance execution requires current signals to know what needs maintaining. Without live VEDA access, maintenance agents operate without situational awareness.
- **Bloated handoff packets.** Without execution-time evidence access, handoff packets must contain copies of every potentially relevant VEDA finding. This inflates context windows and creates governance questions about which copy is authoritative.

This contract enables active, governed evidence access that solves these problems without collapsing system boundaries.

---

## Query Types

V Forge agents may issue the following query types against VEDA evidence.

### evidence_by_project

Returns evidence records associated with a specific project.

Required parameters:
- `project_id` — the active project. Must match the agent's current execution context.
- `freshness_window` — maximum age of evidence to return. Expressed as a duration (e.g., `30d`, `7d`, `24h`).

Optional parameters:
- `evidence_class` — filter by evidence class (e.g., `search_performance`, `competitor_analysis`, `market_signal`, `source_capture`).
- `max_results` — maximum number of evidence records to return. Default 20. Maximum 100.
- `sort` — `freshness` (newest first, default) or `relevance`.

### evidence_by_topic

Returns evidence records matching a topic query within project scope.

Required parameters:
- `project_id` — the active project.
- `topic` — the topic query. Scoped to evidence relevant to the project.
- `freshness_window` — maximum age of evidence to return.

Optional parameters:
- `evidence_class` — filter by evidence class.
- `max_results` — maximum number of evidence records to return. Default 10. Maximum 50.

### signal_status

Returns the current signal health summary for a project. Does not return raw evidence. Returns a structured status object indicating signal availability, freshness, and coverage.

Required parameters:
- `project_id` — the active project.

Returns:
- signal classes available for this project
- freshness status per signal class (fresh / aging / stale / unavailable)
- last update timestamp per signal class
- coverage summary (what is being tracked vs. what has data)

### evidence_by_id

Returns a specific evidence record by its VEDA-issued identifier.

Required parameters:
- `evidence_id` — the VEDA evidence record identifier.
- `project_id` — must match the evidence record's project scope.

This query exists so V Forge can retrieve a specific record it has previously referenced, for re-validation or freshness checking.

---

## Scoping Rules

Every evidence query must be project-scoped.

- V Forge agents may only query evidence for the project they are currently executing against.
- Cross-project evidence queries must fail at the VEDA API level with a scope violation error.
- The `project_id` parameter is mandatory on every query type. There is no unscoped query path.
- VEDA enforces project scoping. V Forge cannot bypass it.

If a V Forge agent needs evidence from a project it is not currently executing against, that need must be routed through Project V as a planning concern. V Forge does not self-authorize cross-project evidence access.

---

## Freshness Metadata

Every evidence record returned through this contract must carry freshness metadata.

Required fields on every evidence response:

- `evidence_id` — VEDA's canonical identifier for this evidence record.
- `gathered_at` — timestamp when this evidence was originally gathered from its source.
- `source_provider` — the provider or source that generated this evidence (e.g., `google_search_console`, `semrush`, `manual_capture`).
- `source_url` — the source URL or reference, where applicable.
- `freshness_status` — one of: `fresh`, `aging`, `stale`, `expired`.
- `freshness_window_end` — the timestamp at which this evidence transitions to the next freshness status.
- `trust_classification` — VEDA's trust posture for this evidence class (e.g., `verified`, `provisional`, `unverified`).

V Forge agents must not treat all evidence as equally current or equally trustworthy. Freshness metadata is the mechanism that prevents this.

---

## Freshness Status Definitions

- **fresh** — evidence was gathered within the expected refresh interval for its class. Safe to use without qualification.
- **aging** — evidence is approaching the end of its expected freshness window. Safe to use but should be noted as aging in execution outputs if the output depends heavily on this evidence.
- **stale** — evidence has exceeded its expected freshness window. Must be flagged explicitly in any execution output that depends on it. V Forge should request fresh evidence through the return-to-planning interface if the stale evidence is critical.
- **expired** — evidence is so old that it should not be used for execution decisions. V Forge must treat expired evidence as unavailable and report the gap.

Freshness windows are defined per evidence class by VEDA. V Forge does not set freshness windows.

---

## Attribution Requirements

When V Forge uses VEDA evidence in execution outputs, the output must attribute the evidence source.

Required attribution fields in execution outputs that depend on VEDA evidence:

- `evidence_source: veda` — identifies VEDA as the source system.
- `evidence_id` — the VEDA evidence record identifier.
- `gathered_at` — when the evidence was gathered.
- `freshness_status` — the freshness status at the time of use.

V Forge must not present VEDA-sourced evidence as though V Forge originated it. The attribution chain must be traceable from execution output back to VEDA evidence record.

This does not mean V Forge outputs must read like citations in a paper. It means the structured metadata on execution outputs must include provenance. Human-readable outputs may reference evidence naturally. Machine-readable outputs must carry the attribution fields.

---

## Activity Logging

Every evidence query from V Forge must be logged.

Log fields per query:

- `actor` — the V Forge agent or session issuing the query.
- `action` — the query type (e.g., `veda_evidence_query`).
- `query_type` — the specific query type (e.g., `evidence_by_project`, `evidence_by_topic`).
- `project_id` — the project scope of the query.
- `parameters` — the query parameters (freshness_window, evidence_class, topic, max_results).
- `result_count` — number of evidence records returned.
- `token_cost` — token cost of the query and response, if applicable.
- `timestamp` — when the query was issued.

This log is part of the ecosystem activity trail. It makes evidence access auditable without restricting it.

V Forge does not need human approval to query evidence. It does need a record that the query happened.

---

## Token and Cost Accounting

Evidence queries consume tokens and may incur API costs.

- Token cost of evidence queries counts against V Forge's execution budget for the active task.
- If V Forge has a budget policy in effect, evidence query costs are included in budget evaluation.
- If evidence queries push V Forge to a budget warning or hard stop threshold, standard budget governance applies.
- V Forge agents should be aware of evidence query costs and avoid redundant or overly broad queries.

The `signal_status` query is the cheapest way for V Forge to check what evidence exists before issuing more expensive `evidence_by_project` or `evidence_by_topic` queries. Agents should prefer `signal_status` as a first check.

---

## The Decision Boundary

Evidence access improves execution quality. It does not grant planning authority.

V Forge agents may use VEDA evidence to:

- produce higher-quality execution outputs informed by current market reality
- validate that executed work aligns with current external conditions
- identify execution-side gaps by crossing evidence against the content graph
- inform bounded execution-side research to avoid duplicating known evidence
- determine maintenance priorities based on current signal health
- include evidence-informed context in execution reports

V Forge agents must not use VEDA evidence to:

- override approved execution scope without returning to Project V
- make planning decisions (create projects, change strategy, reprioritize work)
- self-authorize work that was not in the approved handoff
- bypass human approval gates by citing evidence as justification
- accumulate evidence into a local store that functions as a shadow observatory

The test: **does the evidence make the approved work better, or does it change what work is approved?**

If the former, the access is within bounds.
If the latter, the agent must report the finding through the return-to-planning interface and wait for planning-level decisions.

---

## Degraded-Mode Behavior

When VEDA evidence is unavailable, stale, or returns errors:

- V Forge must not fabricate evidence to fill gaps.
- V Forge must not halt execution entirely unless the missing evidence is critical to safe execution within approved scope.
- V Forge must record the evidence gap explicitly in execution outputs and reports.
- V Forge may proceed with execution using whatever evidence is available, provided the output notes the limitations.
- V Forge may include the evidence gap as a finding in its return-to-planning report.

Partial evidence availability is first-class. If VEDA can provide competitor data but not search performance data, V Forge uses what is available and notes what is missing. It does not treat partial evidence as total failure.

---

## Anti-Drift Rules

### No local evidence accumulation
V Forge must not build a persistent local store of VEDA evidence that outlives the execution session. Evidence is queried, used, and attributed in the current session. It is not archived by V Forge.

### No evidence re-serving
V Forge must not serve VEDA evidence to other systems as though it originated in V Forge. If Project V needs evidence, it queries VEDA directly. V Forge does not become an evidence proxy.

### No freshness override
V Forge must not override VEDA's freshness classifications. If VEDA says evidence is stale, V Forge treats it as stale. V Forge does not decide that stale evidence is "good enough" without noting the staleness.

### No scope escalation
V Forge must not attempt to broaden query scope beyond the active project. If an agent needs broader evidence, that need is a planning concern routed through Project V.

### No evidence-driven self-authorization
Evidence of a market change does not self-authorize V Forge to change execution direction. Evidence informs. Planning decides. Execution executes.

---

## Relationship to Existing Signal Interface

This contract extends the existing `veda-to-v-forge-signal-interface.md`.

The existing interface defines signal classes that V Forge may consume (search performance, owned performance, search intelligence, observatory context). This contract adds:

- explicit query types with required parameters
- freshness metadata on every response
- attribution requirements on execution outputs
- activity logging per query
- token cost accounting
- the decision boundary definition
- degraded-mode behavior
- anti-drift rules

The existing interface remains authoritative for what signal classes are available. This contract governs how that signal is accessed, tracked, and used during execution.

---

## Usage

This document should be used:

- when building V Forge agents that need VEDA evidence during execution
- when designing VEDA API endpoints that serve evidence to V Forge
- when building MCP tools for V Forge evidence queries
- when building the activity logging pipeline for evidence access
- when evaluating whether V Forge evidence usage stays within the decision boundary
- when designing budget policies that account for evidence query costs
- when reviewing evidence attribution in V Forge execution outputs

---

## Related Docs

- `veda-to-v-forge-signal-interface.md`
- `../ecosystem/cross-system-access-governance.md`
- `../ecosystem/cross-system-boundaries.md`
- `../v-forge/data-boundaries.md`
- `../v-forge/v-forge.md`
- `../veda/veda.md`
- `../veda/evidence-and-source-provenance.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `mcp-coordination-model.md`
