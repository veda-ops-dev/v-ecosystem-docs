# Pass 3 Findings — Interface Completeness

Doc audited: `veda-to-project-v-signal-interface.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\veda-to-project-v-signal-interface.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\governance\evidence-continuity-model.md` (referenced in Related Docs)

### Files excluded

None found.

---

### Checklist results

**QM-1: PARTIAL** — The interface direction is clearly stated: "This interface is unidirectional. It defines what crosses from VEDA into Project V." However, the initiation model is unresolved — the doc does not state whether VEDA pushes signal to Project V or Project V pulls it. The doc explicitly declares "detailed transport or implementation format" out of scope, so this omission is intentional, but it leaves the entry point (who calls whom, what mechanism) undefined at any level.

**QM-2: FAIL** — The doc lists semantic elements in "Minimum Interface Semantics" (what signal is being surfaced, why it matters, what concern it affects, etc.) but explicitly defers structure: "these semantics may later be represented through specific data structures, but the semantic contract comes first." No fields, types, or valid values are defined.

**QM-3: FAIL** — The doc explicitly defers response structure to future work: "these semantics may later be represented through specific data structures, but the semantic contract comes first." No fields, types, or schema are provided.

**QM-4: FAIL** — Pagination, result limits, and maximum signal package size are not addressed anywhere in the doc.

**QM-5: FAIL** — No filter options are documented. The "Signal Retention Principle" section defines what VEDA should select for transfer, but this is VEDA's internal selection logic, not caller-controllable filter parameters.

**FR-1: FAIL** — No freshness contract is defined in the interface doc. The doc references `evidence-continuity-model.md` which discusses staleness generally, but the interface doc itself imposes no freshness requirement on what Project V receives.

**FR-2: FAIL** — No staleness threshold is defined. The "Signal Transfer Validity Conditions" section mentions flagging "high provenance uncertainty" but specifies no time-based or condition-based staleness threshold.

**FR-3: FAIL** — No timestamp field is specified in the response. The Minimum Interface Semantics include "what bounded evidence or provenance supports it," which could conceptually include timestamps, but no explicit timestamp field is defined.

**AL-1: FAIL** — The doc does not mention activity trail records, activity logging, or any logging requirement. The activity-trail-model.md establishes that "any query from one system to another system's data must produce an activity record" and defines `signal.query` as the action type for "Project V querying VEDA signal" — but the interface doc contains no reference to this requirement.

**AL-2: FAIL** — No action field value is specified in the interface doc. The activity-trail-model.md defines the applicable action type as `signal.query`, but the interface doc does not reference this or specify any `action` field value.

**AL-3: FAIL** — The interface doc contains no reference to actor, target, entity_type, entity_id, cost fields, or any other activity record field. Activity record requirements are completely absent.

**DG-1: FAIL** — No degraded mode is defined. The doc does not address what happens when VEDA is unavailable, when signal production fails, or when the transfer cannot complete.

**DG-2: FAIL** — Caller behavior during degraded mode is not defined. No mention of fail-fast, cache-use, blocking, or any fallback behavior for Project V when signal is unavailable.

**DG-3: FAIL** — No recovery path is defined.

**CA-1: FAIL** — The doc does not state whether this interface incurs token cost or API cost. The Human-In-The-Loop section mentions "external paid data implications" as a governance consideration for human review, but this is not a cost statement for the interface itself.

**CA-2: FAIL** — No cost model is described. Dependent on CA-1, but even if cost exists, no per-call or per-token model is provided.

**CA-3: FAIL** — No reference to budget enforcement for this interface.

**SR-1: FAIL** — Response records are not structured. The doc explicitly says structured data formats are deferred: "these semantics may later be represented through specific data structures, but the semantic contract comes first." The semantic elements listed could be delivered as free-form text or structured fields — neither is specified.

**SR-2: FAIL** — No structure is defined, making parsing code impossible to write against this doc. The doc itself acknowledges this by deferring structure to future work.

**AP-1: PARTIAL** — The Human-In-The-Loop section acknowledges that "human review or approval may be required" based on strategic importance, source-trust concerns, paid data implications, project creation implications, and launch sensitivity, and references `approval-and-escalation-model.md`. However, the doc does not specify what approval class applies to this interface's baseline access, nor does it define the threshold at which ungated access becomes approval-gated.

**AP-2: PARTIAL** — Governance docs are referenced (`approval-and-escalation-model.md`, `evidence-continuity-model.md`). The "Signal Transfer Validity Conditions" section establishes when a transfer is valid. However, no specific governance gate classes (Class A through D) are assigned to this interface, leaving implementers without a mapped approval requirement.

---

### Score

**0 of 21 PASS — 3 PARTIAL — 18 FAIL**

---

### Critical gaps (FAIL items only)

**QM-2, QM-3, SR-1, SR-2 — No implementation-facing structure defined.** The doc is entirely a semantic contract. No fields, types, or response schemas exist. An implementer cannot build this interface from this doc without inventing the entire data contract. Risk: every implementation will diverge because there is no shared specification to conform to.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** The activity-trail-model.md defines `signal.query` as the required action type for this exact cross-system access pattern and specifies all required fields (actor, target, entity_type, entity_id, cost fields). The interface doc contains no reference to this requirement. Risk: implementations of this interface will not produce activity trail records, breaking the governance auditability requirement for cross-system access.

**FR-1, FR-2, FR-3 — No freshness contract or timestamp.** Project V has no spec for how current transferred signal must be, when it becomes too stale to act on, or how to determine the age of received signal. Risk: Project V may act on arbitrarily old signal without knowing it.

**DG-1, DG-2, DG-3 — No degraded mode.** If VEDA is unavailable, the interface doc provides no guidance on what Project V should do — whether to fail-fast, proceed without signal, block planning decisions, or queue for retry. Risk: implementations will handle VEDA unavailability inconsistently.

**CA-1, CA-2, CA-3 — No cost accounting.** Signal queries may incur token or API cost. Whether they do, and how to account for it, is unspecified. Risk: cost attribution for this interface cannot be tracked against budget.

**QM-4, QM-5 — No result limits or filters.** There is no ceiling on how much signal can transfer in one operation, and no way for the caller to filter by type, time range, or relevance. Risk: implementations may produce unbounded transfers or lack selectivity.

---

### Summary

`veda-to-project-v-signal-interface.md` is a doctrine and ownership doc, not an implementation spec. It correctly establishes the semantic meaning of the signal transfer, the ownership rules before and after transfer, and what the interface does and does not authorize — but it explicitly defers all implementation-facing specification to future work. The 18 FAIL items are concentrated in query mechanics, freshness, activity logging, degraded mode, cost accounting, and structured records — the areas where a developer would need this doc to build against. The most significant gap is the complete absence of activity trail logging requirements, which the activity-trail-model.md mandates for all cross-system access.

---

### Out-of-scope observations not included in findings

- The doc's semantic contract (ownership rules, what transfers, what does not) is well-written and internally consistent — these are not completeness gaps but architectural clarity.
- The Related Docs section references `project-intake-workflow.md` and `external-provider-integration-doctrine.md`, which were not loaded; they are workflow docs rather than interface-completeness dependencies.
