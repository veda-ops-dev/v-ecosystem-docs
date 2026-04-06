# Pass 3 Findings — Interface Completeness

Doc audited: `desktop-surface-architecture.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\desktop-surface-architecture.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\interfaces\desktop-state-and-context-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-governance-and-gating-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-human-llm-interaction-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-agent-orchestration-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-memory-and-continuity-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-invalidation-and-refresh-matrix.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\runtime-sidecar-and-nerve-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\local-first-architecture.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\mcp-coordination-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\operator-surface-interfaces.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-011-tauri-2-desktop-is-the-operator-host.md` (referenced in Related Docs)

### Files excluded

- `C:\dev\v-ecosystem-docs\interfaces\desktop-llm-behavior-contract.md` — referenced in Related Docs; behavioral contract doc; not required to assess surface architecture completeness
- `C:\dev\v-ecosystem-docs\interfaces\desktop-system-init-and-tool-surface-model.md` — referenced in Related Docs; tool-surface mechanics are out of scope per this doc's own Out of Scope section
- `C:\dev\v-ecosystem-docs\governance\recommendation-packaging-doctrine.md` — referenced in Related Docs; not required
- `C:\dev\v-ecosystem-docs\governance\report-structure-and-required-fields.md` — same reason
- Workflow docs — referenced in Related Docs; workflow mechanics outside this checklist's scope
- `C:\dev\v-ecosystem-docs\ecosystem\vocabulary.md` — not required
- `C:\dev\v-ecosystem-docs\ux\desktop\direction\desktop-host-migration-plan.md` — UX direction doc

---

### Checklist results

**QM-1: FAIL** — No query entry point defined. The doc defines the physical layout, content assignment, and absent-affordance rules for the six desktop surface categories, but specifies no call chain, API entry point, or system that calls and answers for any surface interaction. The doc explicitly states it "does not define: specific visual styling... exact React component implementations or Tauri API calls." The Surface Synchronization section defines surface consequence rules but delegates the canonical event list to `desktop-invalidation-and-refresh-matrix.md`.

**QM-2: FAIL** — No input parameters defined. The doc defines which actions belong in which surfaces and what content each surface must contain, but specifies no input fields, parameter types, or valid values for any surface interaction. Detail view content requirements list categories but specify no data fetch parameters.

**QM-3: FAIL** — No response structure defined. The doc defines content requirements for each surface category in prose rules, not as typed field definitions. Context strip requirements ("current system, current workflow stage and next gate, governing decision context loaded...") are display requirements, not a response schema.

**QM-4: FAIL** — Pagination and result limits not addressed. No operation is specified in sufficient detail for these to be assessable.

**QM-5: FAIL** — No filter options documented for any surface operation.

**FR-1: FAIL** — No freshness contract defined for any surface. The Surface Synchronization section requires surfaces to receive "a refresh marker" after staleness or invalidation events, but these are event consequence rules, not freshness contracts governing how current the data shown in any surface must be. Freshness contract is deferred to companion docs.

**FR-2: FAIL** — No staleness threshold defined. The phrase "stale context categories where the operator must remain aware" appears in the Notifications and Alerts section as a use case for persistent warnings, but no threshold value is specified.

**FR-3: FAIL** — No `last_updated` or equivalent timestamp field specified for any data shown in any surface. Surface Synchronization states surfaces receive "a refresh marker" but defines no timestamp field on those markers or on any surface data payload.

**AL-1: FAIL** — Activity trail logging not mentioned anywhere in the doc. The Review-Before-Gate Routing Rule describes the five-step path that produces a persisted approval record — which the activity-trail-model.md requires to produce `approval.decide` records — but contains no reference to activity trail logging. The Class D Escalation Surface defines a non-dismissible escalation banner for Class D conditions — which the activity-trail-model.md requires `approval.escalate` records for — but no logging requirement is stated.

**AL-2: FAIL** — No dot-namespaced action field value specified. The activity-trail-model.md defines `approval.decide`, `approval.request`, `approval.escalate` as applicable action types for the approval gates this doc defines. None are referenced.

**AL-3: FAIL** — No activity record fields mentioned. None of the canonical required fields from the activity-trail-model.md (actor, target, entity_type, entity_id, action_class, cost fields) appear anywhere in this doc.

**DG-1: PARTIAL** — The Surface Synchronization section addresses the degraded-mode surface consequence for session token expiry: "when the session token expires or runtime scope is broken: the top-level session state becomes degraded, all Class B and C actions are blocked across all surfaces, and the right-panel context strip shows the session error posture." The section also addresses local-state divergence: "when local support-state diverges from backend canonical state: the topbar session integrity indicator updates immediately." These cover two specific degraded cases. Backend service unavailability causing individual surfaces to show incomplete content without session token expiry is not defined.

**DG-2: PARTIAL** — For session token expiry: "all Class B and C actions are blocked across all surfaces." For local-state divergence: "the operator is notified before any Class B or C gate is presented while divergence is unresolved." Behavior for individual surface load failures (e.g., center detail view unable to load a specific record) is not defined.

**DG-3: PARTIAL** — The Surface Synchronization section states "when context is refreshed after a staleness or invalidation condition: the context strip, the relevant center review surfaces, and any affected LLM output cards receive a refresh marker" — implying a recovery path. Session token expiry recovery is referenced indirectly through companion docs. No unified recovery path is defined for partial failures; individual record load failures have no defined recovery path.

**CA-1: FAIL** — The doc does not state whether any surface operation, content load, or interaction incurs token cost or API cost.

**CA-2: FAIL** — No cost model described.

**CA-3: FAIL** — No reference to budget enforcement for any surface interaction.

**SR-1: PARTIAL** — Several surface content requirements are specified with enough consistency to imply structured records. The context strip content requirements enumerate named elements: "current system, current workflow stage and next gate, governing decision context loaded, evidence loaded with freshness/trust posture, active staleness or conflict warnings..." The Class B inline gate components are enumerated: "approval request summary, action class badge, approve control, reject control, defer control." The Class C modal components are enumerated: "action being authorized, what happens if authorized, what does NOT change, typed confirmation input where required, confirm authorization control, cancel control." These are partial structural definitions, not formal typed schemas.

**SR-2: PARTIAL** — The Class B and Class C gate surface definitions are specific enough to constrain implementation. The Review-Before-Gate Routing Rule specifies a five-step sequence with named steps. The Class C modal components are enumerated with stable labels. The action placement rules across all six surface categories are stable enough to constrain surface construction. However, no formal typed field definitions exist; all structure is derived from content requirement lists rather than a schema.

**AP-1: PASS** — The Review-Before-Gate Routing Rule is the most explicit access restriction in any audited doc: "The approval gate widget must not appear in the right interaction panel, the left navigation panel, or the topbar. The operator must navigate to the center workspace before the gate is reachable. There is no shortcut path from right-panel output to approval completion." Class C modals "must not fire from the right interaction panel" and "the operator must be inside the center review surface and have completed all checkpoints before the modal is offered." Access to approval gates is strictly conditioned on surface navigation.

**AP-2: PASS** — Governance gates are extensively and specifically referenced throughout the doc. The Gate and Approval Surfaces section defines Class B and Class C gate surface types with explicit components and routing rules. The Escalation Surface section defines a Class D non-dismissible banner with no proceed-anyway path. The Actions That Must NEVER Appear list explicitly prohibits "any control labeled Approve or Authorize that substitutes for the persisted approval event" from the right interaction panel. References to `desktop-governance-and-gating-model.md`, `approval-and-escalation-model.md`, and `desktop-invalidation-and-refresh-matrix.md` are in Related Docs.

---

### Score

**2 of 21 PASS — 5 PARTIAL — 14 FAIL**

---

### Critical gaps (FAIL items only)

**QM-1 through QM-5 — No query interface defined.** The doc defines surface layout, content assignment, and absent-affordance rules but specifies no call chain, input parameters, response structure, pagination, or filter options for any surface operation. Risk: the data access contract for populating each surface cannot be implemented from this doc; implementers must invent the entire surface data model.

**FR-1, FR-2, FR-3 — No freshness contract, threshold, or timestamp fields.** The Surface Synchronization section defines consequence behavior after staleness events but defines no freshness contract, maximum age, or timestamp field for any surface's displayed data. Risk: individual surface implementations will define independent staleness detection without a shared freshness contract.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** The doc defines the approval gate surfaces where `approval.decide` events must occur and the escalation surface where `approval.escalate` events must occur — both of which the activity-trail-model.md requires to produce records. The Review-Before-Gate Routing Rule describes the exact path that produces a persisted approval record but contains no reference to activity trail logging. Risk: approval decisions, Class C typed confirmations, and Class D escalations produced through these surfaces will produce no ecosystem activity trail records.

**CA-1, CA-2, CA-3 — No cost accounting.** No surface operation is assigned a token cost or API cost, and no budget enforcement reference is present. Risk: cost attribution for surface-initiated data loads cannot be assigned from this doc.

---

### Summary

`desktop-surface-architecture.md` earns its 2 PASSes from the Review-Before-Gate Routing Rule and the gate surface definitions — the most physically specific approval-access model in any audited doc, with explicit surface placement rules for Class B and Class C gates and a five-step routing path that prevents shortcutting. The 5 PARTIALs reflect real but incomplete coverage: partial degraded mode for session token expiry and local-state divergence (DG-1 through DG-3), and partial surface content structure derivable from display requirement enumerations (SR-1, SR-2). The 14 FAILs follow the same pattern established across all doctrine-heavy docs in this pass: the doc governs what belongs where and what must not appear where, but commits to no query mechanics, freshness contract, timestamp fields, activity trail logging, or cost accounting for any surface operation. The most significant gap remains AL-1 through AL-3: this doc defines the exact surfaces where approval events are created but imposes no activity trail logging requirement on those events, leaving the governance-critical desktop operations outside the ecosystem audit trail.
