# Pass 3 Findings — Interface Completeness

Doc audited: `v-forge-evidence-access-contract.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\v-forge-evidence-access-contract.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\governance\agent-operating-doctrine.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md` (referenced in Related Docs)

### Files excluded

None found.

---

### Checklist results

**QM-1: PASS** — Caller (V Forge agents), answerer (VEDA), and four distinct query types are explicitly defined: `evidence_by_project`, `evidence_by_topic`, `signal_status`, and `evidence_by_id`. "V Forge agents may issue the following query types against VEDA evidence." Exact MCP tool schemas and VEDA API endpoints are out of scope per the doc, but the interface entry point is specified at the contract level with clear direction and read-only posture.

**QM-2: PASS** — All four query types have defined required and optional parameters with constraints. `evidence_by_project` requires `project_id` and `freshness_window`, with optional `evidence_class`, `max_results` (default 20, max 100), and `sort`. `evidence_by_topic` requires `project_id`, `topic`, and `freshness_window`. `signal_status` requires `project_id`. `evidence_by_id` requires `evidence_id` and `project_id`. Freshness_window format is described by example (`30d`, `7d`, `24h`); formal type notation is absent but coverage is sufficient for implementation.

**QM-3: PARTIAL** — The Freshness Metadata section defines 7 required named fields on every evidence response: `evidence_id`, `gathered_at`, `source_provider`, `source_url`, `freshness_status`, `freshness_window_end`, `trust_classification`. The `signal_status` return structure is also specified with defined content. However, "the content of specific evidence records" is explicitly out of scope — the actual evidence record payload beyond these 7 wrapper fields is not defined in this doc.

**QM-4: PASS** — Result limits are defined per query type with defaults and hard ceilings: `evidence_by_project` (default 20, max 100), `evidence_by_topic` (default 10, max 50). `signal_status` and `evidence_by_id` return single objects and do not require limits.

**QM-5: PASS** — Filter options are documented per query type: `evidence_class` (optional, applicable to `evidence_by_project` and `evidence_by_topic`), `freshness_window` (required time filter on two query types), `sort` (`freshness` or `relevance`, optional on `evidence_by_project`), and `topic` (required filter on `evidence_by_topic`). Filter options are present and described for each applicable query type.

**FR-1: PASS** — A comprehensive freshness contract is defined. The Freshness Metadata section states "every evidence record returned through this contract must carry freshness metadata" and requires `freshness_status`, `gathered_at`, and `freshness_window_end` on every response. The Freshness Status Definitions section defines all four states (`fresh`, `aging`, `stale`, `expired`) with concrete V Forge behavioral requirements per state.

**FR-2: PARTIAL** — The staleness mechanism is fully specified: the `freshness_status` field communicates staleness state, and V Forge behavioral requirements are defined per state ("stale — evidence has exceeded its expected freshness window. Must be flagged explicitly in any execution output that depends on it"). However, the actual threshold values per evidence class are deferred: "freshness windows are defined per evidence class by VEDA. V Forge does not set freshness windows." An implementer must consult VEDA-side docs for the concrete threshold values.

**FR-3: PASS** — `gathered_at` ("timestamp when this evidence was originally gathered from its source") and `freshness_window_end` ("the timestamp at which this evidence transitions to the next freshness status") are both required on every evidence response. `signal_status` also returns "last update timestamp per signal class."

**AL-1: PASS** — Activity logging is explicitly required and tied to the ecosystem activity trail: "Every evidence query from V Forge must be logged. This log is part of the ecosystem activity trail. It makes evidence access auditable without restricting it." This is the only audited interface doc that explicitly mandates activity trail logging.

**AL-2: PARTIAL** — The Activity Logging section specifies an `action` field value: "action — the query type (e.g., `veda_evidence_query`)." However, the activity-trail-model.md defines the canonical dot-namespaced action type as `evidence.query — V Forge querying VEDA evidence.` The interface doc's action value uses underscore format (`veda_evidence_query`) rather than the canonical dot-namespaced format (`evidence.query`), diverging from the model's vocabulary requirement.

**AL-3: PARTIAL** — The Activity Logging section covers: `actor`, `action`, `query_type`, `project_id`, `parameters`, `result_count`, `token_cost`, and `timestamp`. Cost field and actor identification are present. However, several canonical activity-trail-model.md required fields are absent from the specified log format: `activity_id` (unique record identifier), `actor_type` and `actor_system` (bundled into a single `actor` field rather than separately specified), `entity_type` and `entity_id` (which evidence entity was queried), `target_system` (should be `veda`), `ecosystem_session_id`, and `action_class` (should be `cross_system_access`).

**DG-1: PASS** — The Degraded-Mode Behavior section explicitly defines what happens when VEDA evidence is unavailable, stale, or returns errors: "V Forge must not fabricate evidence to fill gaps. V Forge must not halt execution entirely unless the missing evidence is critical to safe execution within approved scope. V Forge must record the evidence gap explicitly in execution outputs and reports." Partial availability is addressed explicitly: "Partial evidence availability is first-class."

**DG-2: PASS** — The same Degraded-Mode Behavior section defines five concrete V Forge caller rules during degraded mode. Caller behavior is fully specified for the unavailable, stale, and error-return cases.

**DG-3: FAIL** — The Degraded-Mode Behavior section specifies what V Forge does while VEDA is unavailable but does not define a recovery path. No retry mechanism, re-query timing, or specification of when to resume normal evidence access after VEDA becomes available again is defined.

**CA-1: PASS** — The Token and Cost Accounting section explicitly states: "Evidence queries consume tokens and may incur API costs. Token cost of evidence queries counts against V Forge's execution budget for the active task."

**CA-2: PARTIAL** — The cost accounting policy is stated (costs count against execution budget; `signal_status` is cheapest, `evidence_by_project` and `evidence_by_topic` are more expensive). The Activity Logging section includes `token_cost` as a required log field. However, no actual cost rates, per-call amounts, or per-token pricing are defined.

**CA-3: PARTIAL** — Budget enforcement is acknowledged: "If evidence queries push V Forge to a budget warning or hard stop threshold, standard budget governance applies." This is a real reference to enforcement consequences. However, no specific budget governance doc is cited and no enforcement mechanism is specified in this contract.

**SR-1: PARTIAL** — The Freshness Metadata section defines 7 named required fields on every evidence response, and `signal_status` has a defined structured return with named content categories. However, "the content of specific evidence records" is explicitly listed in the Out of Scope section — the evidence record payload beyond the 7 wrapper fields is not defined here.

**SR-2: PARTIAL** — Parsing code can be written for the 7-field freshness metadata wrapper and the `signal_status` structured return. Parsing code cannot be written for the evidence record content itself, as that structure is explicitly deferred to VEDA-side docs.

**AP-1: PASS** — Access approval posture is explicitly and unambiguously stated: "This access is governed, not gated. V Forge does not need human approval to query evidence. It does need a record that the query happened." The ungated-but-logged posture is clear.

**AP-2: PASS** — Governance references are present: `agent-operating-doctrine.md` is cited in the extending docs list and Related Docs; `approval-and-escalation-model.md` is in Related Docs; "standard budget governance applies" is referenced in the Token and Cost Accounting section. The Decision Boundary section explicitly defines when V Forge must route through return-to-planning rather than proceeding locally.

---

### Score

**12 of 21 PASS — 8 PARTIAL — 1 FAIL**

---

### Critical gaps (FAIL items only)

**DG-3 — No recovery path defined.** The Degraded-Mode Behavior section fully specifies what V Forge must do while VEDA evidence is unavailable, but does not address how or when to resume normal evidence querying once VEDA becomes available again. No retry mechanism, re-query timing, or resumption posture is defined. Risk: inconsistent post-degradation behavior — implementations may retry continuously, fail to resume without a session restart, or leave V Forge in a permanently degraded posture after VEDA recovers.

---

### Summary

`v-forge-evidence-access-contract.md` is substantively more implementation-complete than all four previously audited interface docs, earning 12 PASSes across query mechanics, freshness, activity logging, degraded mode, cost accounting, and approval references. It defines four named query types with explicit parameters, a 7-field required freshness metadata envelope, mandatory activity logging tied to the ecosystem activity trail, concrete degraded-mode caller rules, and an explicit ungated-but-logged access posture. The 8 PARTIALs reflect genuine but bounded gaps: evidence record content is out of scope, the activity log `action` value diverges from the canonical dot-namespaced vocabulary in the activity trail model, and cost accounting and budget enforcement lack specific rates or cited docs. The sole FAIL is the missing recovery path for when VEDA becomes available again after a degraded period.

---

### Out-of-scope observations not included in findings

- The activity log `action` value `veda_evidence_query` diverges from the activity-trail-model.md's `evidence.query` dot-namespaced vocabulary. This is a cross-system consistency issue between this contract and the ecosystem model; noted in AL-2 scoring, full treatment belongs in Pass 5.
- The `evidence_class` filter values (`search_performance`, `competitor_analysis`, `market_signal`, `source_capture`) do not align with the signal class names defined in `veda-to-v-forge-signal-interface.md` (`Search Performance Signal`, `Owned Performance Signal`, etc.). Cross-system vocabulary consistency issue for Pass 5.
