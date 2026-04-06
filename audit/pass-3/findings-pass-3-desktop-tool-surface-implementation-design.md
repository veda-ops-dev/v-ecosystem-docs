# Pass 3 Findings — Interface Completeness

Doc audited: `desktop-tool-surface-implementation-design.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\desktop-tool-surface-implementation-design.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\interfaces\desktop-system-init-and-tool-surface-model.md` (referenced in Related Docs; primary authority doc this design is subordinate to)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-agent-orchestration-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-state-and-context-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-memory-and-continuity-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\runtime-sidecar-and-nerve-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-invalidation-and-refresh-matrix.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md` (referenced in Related Docs)

### Files excluded

- `C:\dev\v-ecosystem-docs\governance\agent-operating-doctrine.md` — referenced in Related Docs; governance doctrine doc; not required to assess implementation design completeness

---

### Checklist results

**QM-1: PARTIAL** — The doc defines a call chain for tool-surface assembly more mechanically than any other audited doc. The Tool-Surface Lifecycle Overview section defines a seven-stage pipeline: tool registration → candidate surface collection → current-session context binding → structural filtering → active surface publication → runtime execution enforcement → refresh/invalidation/rebuild. The Suggested Runtime Structure section defines six named components: Tool Registry, Session Surface Builder, Structural Filter Pipeline, Active Surface Publisher, Execution Gate, Surface Refresh Coordinator. The flow from runtime context inputs to published surface to execution validation is clear. However, no external API entry point is defined — no specification of what system calls the surface builder, through what mechanism, or what the call interface looks like. The assembly is defined as an internal runtime pipeline, not as a queryable interface with defined callers.

**QM-2: PARTIAL** — The Current-Session Context Binding section specifies the minimum inputs to the filter pipeline: "active system, active project scope, referenced systems currently admitted into the session, active action posture or gating posture, delegated and runtime role posture, current operator-visible scope warnings, if any." The Candidate Surface Collection section specifies additional inputs: "the current system posture, the current project scope token, if any, referenced-system state, if any, current workflow or runtime stage where relevant, current governance and action posture, whether the session is parent, delegated, or resumed." These are named input categories, not typed field definitions. No field names, data types, or valid values are specified for any input.

**QM-3: PARTIAL** — The Active Surface Publication section specifies what the published surface must support: "LLM-visible tool definitions, operator-visible summary of active tool posture, internal enforcement metadata for execution checks, surface version or revision identifier for refresh tracking." The Tool Registry section specifies minimum metadata per registered tool: stable tool identifier, display name and description, owning system classification, read/write/governance-sensitive posture, project-scope requirements if any, whether it is cross-system-readable, whether it is delegation-admissible, execution adapter or dispatcher binding. The Tool Metadata Requirements section specifies five classification dimensions with named enumerated values (owning system: ecosystem/project-v/veda/v-forge; access posture: read-only/bounded mutation/governance-sensitive mutation; scope posture: four values; cross-system posture: three values; delegation posture: three values). These constitute partial response structure. No formal typed schema with field names, types, and nullability is provided.

**QM-4: FAIL** — Pagination and result limits not addressed. The active surface is a filtered collection of tools but no limits on registry size, candidate set size, or published surface size are specified.

**QM-5: PARTIAL** — The Structural Filtering section defines a six-stage filter pipeline: system ownership filter, project-scope filter, referenced-system posture filter, action-posture/governance filter, delegation filter, final publication filter. Each stage is named and its purpose is described. These constitute defined filter options for surface assembly. However, these are fixed pipeline stages applied to all assembly operations, not caller-configurable filter parameters.

**FR-1: PARTIAL** — A freshness model exists for the active surface. The Refresh and Invalidation Mechanics section defines rebuild triggers including: "current system posture, project scope token, referenced-system set, active action/approval posture, delegated task scope, parent/child runtime role posture, tool registry version or registration set, meaningful compaction event that changes the session basis." The Runtime Execution Enforcement section requires that execution checks verify "current governance and action posture still allows the tool" — implying the surface may become stale between build and execution. The Published Surface Should Support includes "surface version or revision identifier for refresh tracking." However, no concrete staleness threshold or maximum surface age is defined.

**FR-2: FAIL** — No staleness threshold defined. The Refresh and Invalidation Mechanics section defines conditions that require a rebuild but specifies no time-based threshold or maximum age for the active surface. "Meaningful compaction event" and "material changes" are qualitative triggers with no quantitative definitions.

**FR-3: PARTIAL** — The Published Surface Should Support section specifies "surface version or revision identifier for refresh tracking" — a versioning mechanism that functions as a form of currency tracking, though not a timestamp. The Tool Registry requirements do not include a `last_updated` or `registered_at` timestamp field. PARTIAL because a versioning mechanism is specified for tracking surface currency even though no formal timestamp field is defined.

**AL-1: FAIL** — Activity trail logging not mentioned anywhere in the doc. Tool surface assemblies, filter decisions, tool execution calls, and surface rebuilds are all operations with governance significance — tool exposure directly determines what the LLM may do. The activity-trail-model.md requires records for cross-system access (MCP tool calls through the assembled surface call backend APIs) and for agent lifecycle events. This doc makes no reference to any activity trail obligation for any of the operations it defines.

**AL-2: FAIL** — No dot-namespaced action field value specified. The activity-trail-model.md defines action types such as `evidence.query`, `signal.query`, `execution.query` for the cross-system calls that tool execution enables, and `agent.start`, `agent.complete` for runtime operations — all of which pass through the tool surface governed by this doc. None of these vocabulary terms appear in this doc.

**AL-3: FAIL** — No activity record fields mentioned. None of the canonical required fields from the activity-trail-model.md (actor_type, actor_id, actor_system, entity_type, entity_id, target_system, action_class, cost fields) appear anywhere in this doc.

**DG-1: PARTIAL** — The Runtime Execution Enforcement section defines behavior for one degraded case: "A stale or bypassed active surface must not allow an out-of-bounds call through" — the execution gate remains a second line of defense even if the surface is stale. The Final Publication Filter section defines a catch for contradictions that survived earlier stages. The Refresh and Invalidation Mechanics section acknowledges that "a tool surface built for one session basis is not automatically safe for a different one." However, no explicit degraded mode is defined for when the tool registry is unavailable, when the filter pipeline fails, or when the surface cannot be built due to missing context.

**DG-2: PARTIAL** — For stale surface at execution time: "Every execution request should be checked against the active published surface and current runtime basis at execution time" — the execution gate runs regardless. This defines caller behavior when the surface may be stale. No behavior is defined for when the registry is unavailable or the filter pipeline fails at surface build time.

**DG-3: PARTIAL** — The Surface Refresh Coordinator is defined as a named component responsible for rebuilding "the active surface when invalidation triggers occur." The doc defers full invalidation consequences to `desktop-invalidation-and-refresh-matrix.md` by name. This constitutes a partial recovery path through explicit delegation. No explicit recovery sequence is defined for surface build failure.

**CA-1: FAIL** — The doc does not state whether any tool surface operation — building the surface, running the filter pipeline, executing a tool call through the surface — incurs token cost or API cost. Tool execution through MCP tools results in API calls that consume tokens, but this doc makes no cost statement.

**CA-2: FAIL** — No cost model described for any tool surface operation.

**CA-3: FAIL** — No reference to budget enforcement for any tool surface operation. Budget governance is not mentioned. The activity-trail-model.md requires `budget.cost_event` records for cost-incurring actions — which would include all LLM tool calls routed through this surface — but this doc makes no reference to budget tracking.

**SR-1: PARTIAL** — The Tool Metadata Requirements section defines five classification dimensions with named enumerated values. The minimum registry entry fields are named: stable tool identifier, display name, description, owning system classification, access posture, project-scope requirements, cross-system-readable flag, delegation-admissible flag, execution adapter/dispatcher binding. The Published Surface Should Support section names four output categories. The Minimum Execution Checks section names five runtime validation checks. These constitute a partial structured record definition. No formal typed schema is provided.

**SR-2: PARTIAL** — The five owning-system values, three access posture values, four scope posture values, and three delegation posture values are all stable enough to implement enum types. The six-stage filter pipeline is stable enough to implement as named pipeline stages. The five minimum execution checks are stable enough to implement as a validation gate. The four published surface output categories are stable enough to constrain implementation. These are stable enough to write implementation code against, derived from named requirement lists rather than formal schemas.

**AP-1: PASS** — The doc's entire purpose is to define how tool access is restricted. The Core Rule states: "The runtime must only expose tools that are currently in-bounds for: the active system posture, the active project scope, the current governance and action posture, the current delegated-runtime posture." The Hard Rule in the Tool Registry section states: "A tool must not become available in session merely because it is installed, reachable, or technically callable." The Anti-Drift Constraints section explicitly prohibits "publishing the full registry and hoping execution checks are enough" and "treating tool presence as authority or approval." The Delegation Filter Hard Rule states: "A delegated tool surface must never be broader than the eligible parent surface."

**AP-2: PASS** — Governance gates are referenced specifically and consistently. The doc is explicitly subordinate to `desktop-governance-and-gating-model.md` and `approval-and-escalation-model.md` (listed as authority docs in the header). The Action-Posture/Governance Filter section states: "Even when a tool is present in the active surface, its actual execution may still require runtime enforcement and or operator review." The Absent-Affordance Runtime Rule from `desktop-system-init-and-tool-surface-model.md` is operationalized here. The doc defers to `desktop-invalidation-and-refresh-matrix.md` for canonical event-to-consequence mapping for rebuild triggers.

---

### Score

**2 of 21 PASS — 11 PARTIAL — 8 FAIL**

---

### Critical gaps (FAIL items only)

**QM-4 — No result limits defined.** No constraints on registry size, candidate set size, or published surface size are specified. Risk: uncontrolled growth of the tool registry or surface could expose the LLM to surface sizes that impair reasoning quality without any defined cap.

**FR-2 — No staleness threshold defined.** Rebuild triggers are qualitative ("material changes," "meaningful compaction event") with no time-based threshold. Risk: implementations will define independent rebuild triggers with no shared currency standard, producing inconsistent surface freshness across sessions.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** The tool surface governs all MCP tool calls, which are the primary mechanism through which cross-system access occurs in this ecosystem. The activity-trail-model.md requires records for all cross-system access (`evidence.query`, `signal.query`, `execution.query`). This doc defines how those tool calls are enabled but contains no activity trail logging requirement. Risk: all MCP tool executions through the governed surface will produce no surface-layer activity trail records, making it impossible to reconstruct from the audit trail what tools were available and what calls were made in any governed session.

**CA-1, CA-2, CA-3 — No cost accounting.** All LLM tool calls generate token costs and may generate API costs. The activity-trail-model.md requires `budget.cost_event` records for cost-incurring actions. This doc defines the surface through which all such calls are routed but makes no cost statement. Risk: cost attribution for all tool-mediated operations cannot be assigned from this doc; budget enforcement has no defined hook in the surface assembly or execution layers.

---

### Summary

`desktop-tool-surface-implementation-design.md` is the most implementation-complete doc audited in this pass after `v-forge-evidence-access-contract.md`, earning 2 PASSes and 11 PARTIALs — the highest PARTIAL count in the entire pass. The 11 PARTIALs reflect genuine partial implementation coverage: a named seven-stage lifecycle and six-stage filter pipeline (QM-1 PARTIAL), named input categories for filter context binding (QM-2 PARTIAL), tool metadata requirements with five named classification dimensions and enumerated values (QM-3, SR-1, SR-2 PARTIAL), a versioning mechanism for surface currency tracking (FR-3 PARTIAL), named filter stages as filter options (QM-5 PARTIAL), qualitative rebuild triggers (FR-1 PARTIAL), and execution-gate second-line-of-defense as partial degraded-mode posture (DG-1 through DG-3 PARTIAL). The 8 FAILs are the fewest of any audited doc except `v-forge-evidence-access-contract.md` (1 FAIL) and `desktop-governance-and-gating-model.md` (9 FAIL). The most significant gap is AL-1 through AL-3: this doc defines the surface through which all MCP tool calls are routed — the primary mechanism for cross-system access — yet contains no activity trail logging requirement for any tool execution, surface build, or filter decision. All cross-system access events that the activity-trail-model.md requires to produce records pass through this surface invisibly from a logging perspective.
