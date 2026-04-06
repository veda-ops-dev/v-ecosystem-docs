# Pass 3 Findings — Interface Completeness

Doc audited: `desktop-llm-behavior-contract.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\desktop-llm-behavior-contract.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\interfaces\desktop-invalidation-and-refresh-matrix.md` (referenced in Related Docs; previously loaded)
- `C:\dev\v-ecosystem-docs\interfaces\mcp-coordination-model.md` (referenced in Related Docs; previously loaded)
- `C:\dev\v-ecosystem-docs\interfaces\operator-surface-interfaces.md` (referenced in Related Docs; previously loaded)
- `C:\dev\v-ecosystem-docs\interfaces\runtime-sidecar-and-nerve-model.md` (referenced in Related Docs; previously loaded)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-surface-architecture.md` (referenced in Related Docs; previously loaded)
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md` (referenced in Related Docs; previously loaded)
- `C:\dev\v-ecosystem-docs\governance\decision-continuity-doctrine.md` (referenced in Related Docs; previously loaded)

### Files excluded

- `C:\dev\v-ecosystem-docs\governance\agent-operating-doctrine.md` — referenced in Related Docs; not loaded; not required to assess this doc's completeness
- `C:\dev\v-ecosystem-docs\governance\auth-and-actor-model.md` — referenced in Related Docs; not loaded
- `C:\dev\v-ecosystem-docs\governance\recommendation-packaging-doctrine.md` — referenced in Related Docs; not loaded
- `C:\dev\v-ecosystem-docs\governance\report-structure-and-required-fields.md` — referenced in Related Docs; not loaded
- ADR docs — referenced in Related Docs; not required to assess this doc's completeness
- `C:\dev\v-ecosystem-docs\ecosystem\vocabulary.md` — not required

---

### Checklist results

**QM-1: FAIL** — No query entry point defined. `desktop-llm-behavior-contract.md` defines the LLM's operating posture, allowed output types, triggering rules, and structural enforcement requirements. It specifies no call chain, API entry point, or system that calls and answers for any LLM interaction operation. The Out of Scope section explicitly excludes "API endpoint design" and "implementation-specific session management." The doc is entirely a behavioral constraint doc, not a data-exchange interface definition.

**QM-2: FAIL** — No input parameters defined. The Allowed Output Types section defines seven output types with named required elements, but these are content requirements for the LLM to produce, not typed input parameter definitions for any API or IPC call. The Operator Framing Rules section defines examples of valid framing but not as typed input fields.

**QM-3: PARTIAL** — The Allowed Output Types section defines seven named output types with required element lists. Recommendation must contain: "producer attribution, proposed path, bounded scope, basis, uncertainty, governance posture, acceptance outcome, non-acceptance outcome." Approval Request Package must contain: "action class, the scope, what approval covers, what it does not cover, and what the default state is if approval is not granted." Uncertainty Notice must contain: "what specific context or evidence would resolve the uncertainty." Continuity Reminder, Finding, Review Summary, and Execution Report are defined behaviorally. The Structural Enforcement Requirement §7 specifies that Recommendation outputs must be "validated against the required elements before rendering." These constitute partial output type specifications with named required fields. No formal typed schema with field names, data types, and nullability is provided.

**QM-4: FAIL** — Pagination and result limits not addressed. The doc governs LLM behavior posture, not data query mechanics. No output size limits or pagination constraints are defined.

**QM-5: FAIL** — No filter options documented. The doc governs what the LLM may produce, not how outputs are queried or filtered.

**FR-1: PARTIAL** — A freshness model exists for the LLM's context obligations. The Stale or Incomplete Context section specifies: "an evidence observation older than a governed freshness threshold must be flagged as potentially stale," "a prior readiness evaluation that predates a material gap change must be treated as requiring re-evaluation," "a continuity artifact with freshness risk must not be treated as if it were fresh canonical state." The What Must Be Shown as Loaded section requires that context freshness be visible to the operator before the LLM responds. These constitute real freshness obligations on the LLM's behavior. However, no concrete freshness window, maximum age, or staleness threshold is defined in this doc.

**FR-2: FAIL** — No staleness threshold defined. "An evidence observation older than a governed freshness threshold" defers the threshold value to other docs without specifying it. "A prior readiness evaluation that predates a material gap change" is qualitative, not threshold-based.

**FR-3: FAIL** — No `last_updated` or equivalent timestamp field specified for any LLM output type. The doc requires that loaded context show freshness status but does not specify that any output type must carry a timestamp field.

**AL-1: FAIL** — Activity trail logging not mentioned anywhere in the doc. The Structural Enforcement Requirements section defines ten hard rules for what the API and UI must enforce, including persisted approval records and rejection records. These are governance-critical events that the activity-trail-model.md requires to produce activity records. The doc does not reference the ecosystem activity trail for any of them.

**AL-2: FAIL** — No dot-namespaced action field value specified. The activity-trail-model.md defines `approval.decide`, `approval.request`, `approval.escalate` as applicable action types for the approval events this doc governs. None are referenced.

**AL-3: FAIL** — No activity record fields mentioned. None of the canonical required fields from the activity-trail-model.md (activity_id, actor_type, actor_id, actor_system, entity_type, entity_id, target_system, action_class, cost fields) appear anywhere in this doc.

**DG-1: FAIL** — Degraded mode not defined. The Stale or Incomplete Context section defines how the LLM must behave when context is stale or incomplete ("produce an Uncertainty Notice"), but does not define a degraded mode for when the LLM's backend dependencies are unavailable. The doc governs LLM behavior, not system availability.

**DG-2: FAIL** — Caller behavior during degraded mode not defined. The doc defines the LLM's behavior under stale context ("surface this before producing outputs that depend on that context") but not under system unavailability.

**DG-3: FAIL** — No recovery path defined for any degraded condition. Recovery behavior is deferred to `desktop-invalidation-and-refresh-matrix.md`.

**CA-1: FAIL** — The doc does not state whether LLM output generation, context loading, or any operation described incurs token cost or API cost. The doc governs behavioral posture, not cost accounting.

**CA-2: FAIL** — No cost model described.

**CA-3: FAIL** — No reference to budget enforcement for any LLM operation. Token consumption by the LLM is not addressed in this doc.

**SR-1: PARTIAL** — The Allowed Output Types section specifies named required elements for seven output types. Recommendation: eight named required elements. Approval Request Package: five named required elements. Uncertainty Notice: one named required element ("what specific context or evidence would resolve the uncertainty"). The Structural Enforcement Requirement §7 specifies that Recommendation validation must confirm the presence of eight named elements before rendering. These are partial structural definitions. No formal typed field schema is provided for any output type.

**SR-2: PARTIAL** — The seven output type names (Finding, Recommendation, Review Summary, Approval Request Package, Execution Report, Uncertainty Notice, Continuity Reminder) are stable named labels that constrain implementation. The eight Recommendation required elements and five Approval Request Package required elements are stable enough to implement as validation functions. The ten Structural Enforcement Requirements are stable enough to implement as API-level and UI-level constraints. These are stable enough to guide implementation but derived from prose rather than formal schemas.

**AP-1: PASS** — The doc defines access restrictions exhaustively. The Structural Enforcement Requirements section states: "Class B and Class C actions may not proceed unless the API confirms a valid persisted approval record exists for the specific action and scope." Requirement §2 states: "The approval gate widget is the only path to activated Class B and Class C actions." The Operator Framing Rules section states: "Governed approval requires: explicit operator action through the approval gate widget, a persisted approval record, the approval being scoped to the specific action being approved." The What the LLM Must Never Infer section lists "operator conversational agreement constitutes governed approval" as a forbidden inference. Access restrictions are the organizing principle of the entire doc.

**AP-2: PASS** — Governance gates are explicitly referenced and operationally specified throughout. The Structural Enforcement Requirements section defines ten hard requirements including: API rejection without persisted approval, conversation-to-activation bypass forbidden, scope enforcement from session token, server-owned fields non-settable. `desktop-invalidation-and-refresh-matrix.md` is cited as the canonical authority for invalidation event consequences. `approval-and-escalation-model.md`, `decision-continuity-doctrine.md`, ADR-004, ADR-005, ADR-009, ADR-010, and ADR-011 are cited in Related Docs. The Multi-Model Coexistence section establishes that governance gates apply regardless of which model is in use.

---

### Score

**2 of 21 PASS — 5 PARTIAL — 14 FAIL**

---

### Critical gaps (FAIL items only)

**QM-1, QM-2, QM-4, QM-5 — No query interface defined.** The doc defines the LLM's behavioral posture and output type requirements but specifies no call chain, input parameters, result limits, or filter options for any LLM interaction operation. Risk: the mechanical interface for submitting operator input, receiving LLM outputs, and validating output types cannot be implemented from this doc alone.

**FR-2, FR-3 — No staleness threshold or timestamp fields.** Freshness obligations for the LLM are defined behaviorally ("flag as potentially stale," "treat as requiring re-evaluation") but no threshold values or timestamp fields are specified. Risk: staleness detection thresholds will be defined independently per evidence type and context category.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** The Structural Enforcement Requirements define persisted approval and rejection records as hard requirements — exactly the records the activity-trail-model.md requires to produce `approval.decide` and `approval.escalate` entries. The doc does not reference the ecosystem activity trail for any of these. Risk: the governance-critical events this doc requires to be persisted will not be systematically connected to the ecosystem's cross-system audit mechanism.

**DG-1, DG-2, DG-3 — No degraded mode defined.** The doc governs the LLM's behavior under stale context but not under system unavailability. Risk: LLM behavior when backend systems are unreachable is not defined by this doc; implementations must infer degraded posture from companion docs.

**CA-1, CA-2, CA-3 — No cost accounting.** Token consumption and API cost for LLM interactions are not addressed. Risk: cost attribution for LLM output generation cannot be assigned from this doc.

---

### Summary

`desktop-llm-behavior-contract.md` scores 2 PASS / 5 PARTIAL / 14 FAIL — an identical profile to `desktop-surface-architecture.md` (2/5/14). Both PASSes come from the same source: the ten Structural Enforcement Requirements and the exhaustive access restriction framework (AP-1, AP-2) are the most complete governance constraint specifications in the audited set, establishing that conversational approval has no effect, approval gate widgets are the only path to Class B/C activation, and API-level enforcement is required for every constraint. The 5 PARTIALs reflect genuine partial coverage: seven named output types with partial required element lists (QM-3, SR-1, SR-2), and a real freshness obligation model without threshold values (FR-1). The 14 FAILs follow the same pattern as all behavioral doctrine docs in this pass: no query mechanics, no staleness thresholds, no timestamp fields, no activity trail logging despite defining the exact events that require activity trail records, no degraded mode, and no cost accounting. The most notable gap relative to the doc's purpose is AL-1/AL-2/AL-3: this doc establishes that approval events must be persisted as durable database records (Structural Enforcement Requirement §8 — "An approval event is a persisted record in the database, not a statement in the interaction surface") but contains no connection to the ecosystem activity trail's machine-parseable action vocabulary, leaving the most governance-critical desktop operations outside the cross-system audit mechanism.
