# Pass 3 Findings — Interface Completeness

Doc audited: `desktop-system-init-and-tool-surface-model.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\desktop-system-init-and-tool-surface-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\interfaces\desktop-governance-and-gating-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-state-and-context-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-agent-orchestration-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-memory-and-continuity-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-invalidation-and-refresh-matrix.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\runtime-sidecar-and-nerve-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\local-first-architecture.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-tool-surface-implementation-design.md` (referenced in doc body as "the tool-surface implementation-design companion")
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-004-mcp-tools-are-thin-wrappers.md` (referenced in binding list)
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-005-session-token-model-for-project-scope.md` (referenced in binding list)
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-009-no-direct-database-access.md` (referenced in binding list)
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-011-tauri-2-desktop-is-the-operator-host.md` (referenced in binding list)

### Files excluded

- `C:\dev\v-ecosystem-docs\interfaces\desktop-llm-behavior-contract.md` — referenced in Related Docs; behavioral contract doc; not required to assess this doc's completeness

---

### Checklist results

**QM-1: PARTIAL** — The doc defines the session init assembly as a deliberate seven-step sequence. The Session Init Assembly Rule section specifies the ordered steps: project scope binding via session token → current system posture → workflow and gating context → decision and evidence basis → admitted continuity artifacts → session tool surface → behavior and constraint distillation. This defines what the init assembly must accomplish and in what order. The Refresh Rule section defines conditions that trigger a re-assembly. However, no external API entry point is defined for calling the init assembly — no specification of what system initiates it, through what mechanism, or what the caller interface looks like. The doc refers to "the tool-surface implementation-design companion" for mechanical filtering details, deferring the actual assembly mechanics.

**QM-2: PARTIAL** — The Required Init Message Categories section specifies seven named input categories that must be assembled: role and posture, scope and current system, workflow and gating posture, decision and evidence context summary, continuity artifacts admitted to the session, tool surface summary, runtime warnings or protected-context notes. The Tool Surface Assembly Rule section specifies five named filtering considerations: project scope binding, current system relevance, referenced-system posture, action-class posture, runtime task posture. These are named input categories, not typed field definitions. No field names, data types, or valid values are specified for any input.

**QM-3: PARTIAL** — The Required Init Message Categories section specifies seven named required output categories for the assembled init message. The Session Tool Surface Definition section specifies that the surface is assembled from "admitted MCP surfaces and filtered according to: project scope, current system posture, governance and action-class rules, referenced-system read posture where allowed, runtime mode or flow constraints where admitted." The doc states the surface "must not simply mirror every tool the runtime could theoretically access" and that it must be a "deliberate assembly product." These constitute partial output structure specifications. No formal typed schema or field-level definitions are provided.

**QM-4: FAIL** — Pagination and result limits not addressed. No constraints on tool surface size, init message length, or continuity artifact count are specified.

**QM-5: PARTIAL** — The Tool Surface Assembly Rule specifies five named filtering dimensions that govern what enters the session tool surface: project scope binding, current system relevance, referenced-system posture, action-class posture, runtime task posture. The Referenced-System Read Rule and Delegated Tool Surface Narrowing Rule add further named filtering constraints. These are defined filter categories applied during assembly. However, they are not caller-configurable filter parameters — they are fixed policy-driven filtering rules. No configurable query-time filter options are documented.

**FR-1: PARTIAL** — A freshness model exists for the session basis. The Refresh Rule section defines conditions that require a session basis refresh: "project scope change, current-system change, workflow-stage change that affects gating or context needs, approval-state change, evidence-basis refresh or invalidation, meaningful continuity change after compaction or resume, delegated work completion that changes the admitted continuity set." The doc states "A stale init basis must not be allowed to linger just because the interaction session is still open." The Refresh Implementation Posture section requires that refresh must surface "that the session basis changed" and "identify the categories that changed." These constitute a real freshness posture. However, no concrete staleness threshold or maximum age is defined.

**FR-2: FAIL** — No staleness threshold defined. "Stale init basis must not be allowed to linger" is a posture statement, not a threshold. No numeric or temporal value defines when the session init basis crosses from current to stale. Refresh is triggered by named conditions, not time-based thresholds.

**FR-3: PARTIAL** — The Refresh Implementation Posture section requires that when a material refresh occurs, the runtime must "surface that the session basis changed" and "identify the categories that changed" — implying category-level change tracking. The doc defers to `desktop-invalidation-and-refresh-matrix.md` for how "those changes propagate to desktop surfaces, the LLM, and the interaction layer." However, no `last_updated`, `assembled_at`, or equivalent timestamp field is specified on the init message or session tool surface records.

**AL-1: FAIL** — Activity trail logging not mentioned anywhere in the doc. Session init assembly and session basis refresh are operations with significant governance implications — they determine what context and tools the LLM receives. The activity-trail-model.md requires records for cross-system access (loading decision context, evidence, workflow stage from canonical backends) and for agent lifecycle events. The doc contains no reference to any activity trail requirement for any init assembly, tool surface build, or session refresh operation.

**AL-2: FAIL** — No dot-namespaced action field value specified. The activity-trail-model.md defines `signal.query`, `execution.query`, `evidence.query` as applicable to the canonical loads that init assembly triggers. None are referenced in this doc.

**AL-3: FAIL** — No activity record fields mentioned. None of the canonical required fields from the activity-trail-model.md (actor, target, entity_type, entity_id, action_class, cost fields) appear anywhere in this doc.

**DG-1: PARTIAL** — The Anti-Drift Rules section defines "No stale-basis confidence rule: The runtime must not behave as though an old session basis remains correct after a material context change." The Refresh Rule states "A stale init basis must not be allowed to linger." These establish a degraded posture for the stale-basis case. However, no explicit degraded mode is defined for when canonical backend systems are unavailable during init assembly — what happens if workflow stage cannot be loaded, or if evidence basis cannot be retrieved at session start.

**DG-2: PARTIAL** — For the stale-basis case: the runtime must refresh and not "behave as though an old session basis remains correct." For the tool surface: the Absent-Affordance Runtime Rule states wrong tools must be absent, not merely behind a permission check. These define implicit caller behavior for specific degraded conditions. Explicit caller behavior when backend systems are unavailable during init assembly is not defined.

**DG-3: PARTIAL** — The Refresh Rule section defines conditions that trigger re-assembly, implying that a re-assembly after detecting staleness is the recovery path. The doc defers to `desktop-invalidation-and-refresh-matrix.md` for the "canonical event-to-consequence mapping that governs when session-basis refresh is triggered." This is a partial recovery path through explicit delegation. No standalone recovery sequence is defined for init assembly failure.

**CA-1: FAIL** — The doc does not state whether session init assembly, canonical context loading, or session tool surface construction incurs token cost or API cost. The doc governs how the session basis is assembled, not cost accounting.

**CA-2: FAIL** — No cost model described.

**CA-3: FAIL** — No reference to budget enforcement for any session init or tool surface operation.

**SR-1: PARTIAL** — The Required Init Message Categories section specifies seven named required output categories for the init message. The Tool Surface Assembly Rule section enumerates five named filtering considerations. The Anti-Drift Rules section defines six named rules as stable labels. The Referenced-System Read Rule specifies four named constraints on referenced-system admission (bounded, visible, non-owning, non-mutating unless explicitly authorized). These are partial structural definitions. No formal typed schema is provided for the init message or tool surface record.

**SR-2: PARTIAL** — The seven required init message categories are stable named labels that constrain implementation. The five tool surface assembly filtering considerations are stable enough to implement as a filter checklist. The six Anti-Drift Rules are stable enough to implement as validation checks. The four referenced-system read posture constraints are stable enough to constrain implementation. These are stable enough to guide implementation choices but are derived from prose requirement descriptions rather than formal schemas.

**AP-1: PASS** — The doc explicitly defines access restrictions throughout. The Core Rule states: "The LLM must only receive the context and tool surface it is currently entitled to use." The Tool Surface Assembly Rule states: "If the runtime cannot explain why a tool is available in the session, that tool should not be in the session tool surface." The Delegated Tool Surface Narrowing Rule states: "Delegated subtasks must receive a narrower tool surface than or equal to the parent session surface. A delegated worker must not receive broader authority than the parent session." The Absent-Affordance Runtime Rule states: "wrong tools must be absent from the LLM's effective tool surface, not just hidden behind a nicer interface." Access control is the doc's organizing principle.

**AP-2: PASS** — Governance gates are explicitly referenced throughout. The doc is explicitly subordinate to `desktop-governance-and-gating-model.md` (listed in the binding docs). The Tool Surface Assembly Rule specifies "Mutation-capable tools must remain subordinate to the existing governance and gating model." The Action-class posture filtering consideration requires tools to be filtered by action-class posture. The Referenced-System Read Rule requires referenced-system tools to remain "non-mutating unless an explicit ecosystem interface doc and separately governed path authorize more than reading." ADR-004, ADR-005, ADR-009, and ADR-011 are all cited as active bindings. `desktop-invalidation-and-refresh-matrix.md` is cited for event-consequence mapping.

---

### Score

**2 of 21 PASS — 11 PARTIAL — 8 FAIL**

---

### Critical gaps (FAIL items only)

**QM-4 — No result limits defined.** No constraints on tool surface size, init message length, or continuity artifact count are specified. Risk: init messages may grow unboundedly without defined caps, creating token pressure that the doc itself acknowledges compaction exists to address.

**FR-2 — No staleness threshold defined.** "Stale init basis must not be allowed to linger" is a posture statement, not a threshold. No numeric or temporal value defines when the session basis is stale. Risk: implementations will define independent staleness triggers with no shared definition of currency.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** Session init assembly triggers cross-system access (loading decision context, evidence basis, workflow stage from canonical backends), which the activity-trail-model.md requires to produce records (`signal.query`, `execution.query`). The doc contains no reference to any activity trail obligation for init assembly, tool surface construction, or session refresh. Risk: all session-start canonical loads — the operations that establish what context the LLM operates with for the entire session — will produce no ecosystem activity trail records.

**CA-1, CA-2, CA-3 — No cost accounting.** Session init assembly triggers canonical backend reads that may incur API cost. Tool surface construction involves backend API calls. No cost model or budget enforcement reference is provided. Risk: cost attribution for session initialization operations cannot be assigned from this doc.

---

### Summary

`desktop-system-init-and-tool-surface-model.md` scores identically to `desktop-tool-surface-implementation-design.md` at 2 PASS / 11 PARTIAL / 8 FAIL — fitting, since the two docs govern complementary aspects of the same system (doctrine vs. mechanics). The 2 PASSes come from the same strength: the Core Rule and Tool Surface Assembly Rule define the most complete access control model for session context and tool exposure in any audited Tier 1 doc, with the Absent-Affordance Runtime Rule making structural exclusion (not just permission checking) the primary enforcement mechanism, and governance gate references throughout. The 11 PARTIALs reflect genuine partial coverage: named seven-step init assembly sequence and five filtering considerations (QM-1, QM-2, QM-5), named seven required init message categories (QM-3, SR-1, SR-2), real freshness model with named refresh triggers (FR-1, FR-3), partial degraded posture for stale basis (DG-1 through DG-3). The 8 FAILs follow the same pattern as its companion doc: no result limits, no staleness threshold, no activity trail logging for session-start canonical loads, and no cost accounting — with AL-1 through AL-3 being the most significant gap since session init is the mechanism through which all cross-system access during a session originates, yet produces no activity trail records.
