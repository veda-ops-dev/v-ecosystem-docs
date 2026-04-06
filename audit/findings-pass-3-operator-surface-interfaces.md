# Pass 3 Findings — Interface Completeness

Doc audited: `operator-surface-interfaces.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\operator-surface-interfaces.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\governance\auth-and-actor-model.md` (referenced in Related Docs)

### Files excluded

None found.

---

### Checklist results

**QM-1: FAIL** — This doc defines operator surface governance, not a query interface between systems. No call chain, API endpoint, or request/response model is defined. The doc explicitly excludes "detailed API endpoint design" from scope. The desktop application is named as the primary operator surface, but the underlying query mechanism is delegated entirely to `mcp-coordination-model.md`.

**QM-2: FAIL** — No input parameters are defined for any operator action. Actions are listed by name ("approve or reject handoff activation," "initiate intake evaluation") but no fields, types, or valid values are specified. "Detailed API endpoint design" is explicitly out of scope.

**QM-3: FAIL** — No response structure is defined for any operator action or surface query.

**QM-4: FAIL** — Pagination and result limits are not addressed anywhere in the doc.

**QM-5: FAIL** — No filter options are documented. "Configure portfolio visibility and sequencing preferences" is listed as a permitted operator action, but no filter parameter definitions are provided.

**FR-1: FAIL** — No freshness contract is defined for state presented to operators through any system surface.

**FR-2: FAIL** — No staleness threshold is defined.

**FR-3: FAIL** — No timestamp field is specified for any data returned through operator surface interactions.

**AL-1: FAIL** — The doc contains no mention of activity trail records, activity logging, or any logging requirement. The activity-trail-model.md requires activity records for "any approval request, approval decision, escalation, or governance gate evaluation," and defines `approval.decide` and `approval.request` as action types. This doc lists numerous approval actions operators take across all three surfaces (approve/reject handoffs, approve launch activation, approve paid data pulls, approve replanning proposals) — all of which should produce activity records — but makes no reference to this requirement.

**AL-2: FAIL** — No dot-namespaced action field values are specified for any operator action.

**AL-3: FAIL** — No activity record fields are mentioned.

**DG-1: FAIL** — No degraded mode is defined. The doc does not address what operators experience if a system surface is unavailable or if the desktop application cannot reach backend systems.

**DG-2: FAIL** — Operator behavior during degraded mode is not defined.

**DG-3: FAIL** — No recovery path is defined.

**CA-1: FAIL** — The doc does not state whether operator surface interactions incur token cost or API cost. The VEDA surface section acknowledges that some approved actions create external spend ("approve paid data pulls and spend-creating external actions," "activating a new paid data provider or spend-creating data pull (Class C)"), but this describes external spend from governed actions, not cost accounting for the operator surface interaction layer itself.

**CA-2: FAIL** — No cost model described.

**CA-3: FAIL** — No budget enforcement reference for the operator surface interaction layer. References to `paid-data-pull-governance.md` and `external-action-governance.md` cover external action spend governance, not interface-layer cost accounting.

**SR-1: FAIL** — No response records with typed fields are defined anywhere in the doc.

**SR-2: FAIL** — No structure defined; parsing code cannot be written against this doc.

**AP-1: PASS** — Approval requirements are explicitly documented with assigned classes for each action type across all three system surfaces. Project V: intake outcome activation (Class B or C), handoff activation (Class B or C), significant planning mutations (Class B or C), project thesis revision (Class B), project archive (Class B). VEDA: new paid data provider activation (Class C), observatory scope expansion (Class B or C), any external spend action (Class C). V Forge: launch-sensitive execution activation (Class C), external publication or spend-creating actions (Class C), scope expansions (Class B or C), return-to-planning activation affecting planning direction (Class B). Governance docs cited: `approval-and-escalation-model.md`, `auth-and-actor-model.md`.

**AP-2: PASS** — Multiple governance gates are explicitly referenced with specific doc citations across all three surfaces: `auth-and-actor-model.md`, `approval-and-escalation-model.md`, `external-action-governance.md`, `paid-data-pull-governance.md`, `agent-operating-doctrine.md`, `allowed-agent-actions-matrix.md`, `v-forge/system-invariants.md`, and `workflows/launch-readiness-workflow.md`. The "What operators must not do directly" sections define hard cross-system boundaries per surface.

---

### Score

**2 of 21 PASS — 0 PARTIAL — 19 FAIL**

---

### Critical gaps (FAIL items only)

**QM-1 through QM-5 — No query interface defined.** This doc governs operator surface permissions, not the underlying query/response contract. No call chain, parameters, response structure, pagination, or filters are defined. Risk: operator surface implementation teams have no field-level contract to build against from this doc; they must look elsewhere entirely.

**FR-1, FR-2, FR-3 — No freshness contract or timestamps.** No specification of how current the planning state, execution state, or observatory state shown to operators must be, or how to signal to operators that they may be looking at stale data. Risk: operators may take approval decisions based on stale system state without any indication of its age.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** The doc defines numerous operator approval actions that the activity-trail-model.md explicitly requires to produce records (`approval.decide`, `approval.request`). None of the approval events listed across all three surfaces is connected to any logging requirement in this doc. Risk: operator approval decisions — the most governance-critical actions in the ecosystem — will not reliably produce activity trail records, breaking the audit trail for handoff approvals, launch activations, and paid data pull authorizations.

**DG-1, DG-2, DG-3 — No degraded mode or recovery path.** If a backend system is unavailable, the doc provides no guidance on what operators should see or do. Risk: operators may attempt to take approval actions without verified current state, producing approvals based on stale or missing information.

**CA-1, CA-2, CA-3 — No cost accounting for the surface interaction layer.** While external spend from governed actions is acknowledged for VEDA surfaces, the interface layer itself has no stated cost implications. Risk: token cost attribution for LLM-assisted operator sessions through the surface is untracked.

**SR-1, SR-2 — No structured response records.** No field definitions exist for any surface response. Risk: surface implementations will diverge in what they render for operators without a shared record structure.

---

### Summary

`operator-surface-interfaces.md` is a governance permissions and boundary doctrine doc, not a query interface contract. It earns both its PASSes from the same strength: the approval class assignments and governance gate references are the most detailed of any audited interface doc, with named classes (Class B, Class C) explicitly assigned per action type for all three system surfaces and eight governance docs cited. The 19 FAILs reflect the doc's intentional scope — it defines what operators may do, not how those actions are implemented, logged, or monitored. The most operationally significant gap is AL-1/AL-2/AL-3: operator approval decisions are the most governance-critical events in the ecosystem, but the doc makes no reference to activity trail logging requirements for any of them.

---

### Out-of-scope observations not included in findings

- The V Forge surface section contains a notably long inline paragraph embedding a governance judgment about maintenance vs. return-to-planning routing: "operators must distinguish between findings that can be resolved within existing approved scope as maintenance activity and findings that warrant governed return-to-planning..." This is implementation guidance embedded in what is otherwise a permissions list — it belongs in a workflow doc per the doc's own out-of-scope declaration.
- The doc references `allowed-agent-actions-matrix.md` and `paid-data-pull-governance.md` in Related Docs and inline, but these do not appear to be loaded in the session; they were cited for completeness.
