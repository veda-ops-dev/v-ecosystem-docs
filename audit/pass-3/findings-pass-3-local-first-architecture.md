# Pass 3 Findings — Interface Completeness

Doc audited: `local-first-architecture.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\local-first-architecture.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\interfaces\runtime-sidecar-and-nerve-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-invalidation-and-refresh-matrix.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\ecosystem\db-posture.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-009-no-direct-database-access.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-011-tauri-2-desktop-is-the-operator-host.md` (referenced in Related Docs)

### Files excluded

- `C:\dev\v-ecosystem-docs\ux\desktop\direction\desktop-host-migration-plan.md` — UX direction doc; not required to assess completeness

---

### Checklist results

**QM-1: FAIL** — No query entry point defined. The Boot and Hydration Posture section enumerates a six-step sequence ("Load local support state from SQLite where available… Refresh from canonical backend systems") but names no caller, no API, no method, and no transport. The doc states it "does NOT define all runtime/session mechanics in exhaustive implementation detail."

**QM-2: FAIL** — No input parameters defined. Content categories permissible in local SQLite are listed ("recently viewed records," "cached read models," "draft work not yet committed") but no parameter names, types, or valid values are specified for any operation against the local support layer or canonical backend refresh path.

**QM-3: FAIL** — No response structure defined. The three-layer model describes what each layer holds categorically but defines no field names, types, or structural payload for any read or write operation.

**QM-4: FAIL** — Pagination and result limits not addressed anywhere in the doc.

**QM-5: FAIL** — No filter options documented. Content categories are enumerated but no query-time filter parameters are defined at any layer.

**FR-1: FAIL** — No freshness contract defined. The Reconciliation Rule requires divergent material to be "clearly identified as draft, stale, divergent, or pending review as appropriate" but no freshness window, maximum age threshold, or minimum refresh cadence is specified. The doc delegates EVENT-18 consequences to `desktop-invalidation-and-refresh-matrix.md` but does not define the threshold at which divergence is declared.

**FR-2: FAIL** — No staleness threshold defined. "Local-first behavior improves UX; it does not weaken governance" is a posture statement, not a threshold. No numeric or temporal definition of when local support state crosses from valid to stale is provided.

**FR-3: FAIL** — No `last_updated` or equivalent timestamp field specified for any data returned from the local SQLite layer or any canonical backend refresh payload. The Reconciliation Rule requires divergent material to be "clearly identified" but does not specify a timestamp field on those records.

**AL-1: FAIL** — Activity trail logging not mentioned anywhere in the doc. Hydration and reconciliation operations — the desktop application reading from canonical backend systems during refresh — constitute cross-system access that the activity-trail-model.md requires to produce activity records. Neither the Governance Protection Rule, the Reconciliation Rule, nor the Boot and Hydration Posture section references any activity logging requirement.

**AL-2: FAIL** — No dot-namespaced action field value specified. The activity-trail-model.md defines no `local.hydrate` or `local.reconcile` action type — a gap in the authority model itself — and this doc makes no reference to any action vocabulary for the operations it describes.

**AL-3: FAIL** — No activity record fields mentioned. None of the canonical required fields from the activity-trail-model.md (actor, target, entity_type, entity_id, action_class, cost fields) appear anywhere in this doc.

**DG-1: FAIL** — Degraded mode not defined. The doc states "the desktop application can become useful quickly without waiting for remote backend fetches" — implying local-state-only operation — but no conditions, notification requirements, or duration limits for that window are defined. No degraded posture rules are specified.

**DG-2: FAIL** — Caller behavior during degraded mode not defined. The Reconciliation Rule applies only "when canonical backend refresh occurs" — it has no binding for the case where refresh does not occur at all. No retry, warning, or action-blocking posture is defined.

**DG-3: FAIL** — No recovery path defined. No re-initialization trigger, retry interval, or recovery sequence described for resuming normal reconciliation posture after a degraded period.

**CA-1: FAIL** — Doc does not state whether local SQLite read/write operations, canonical backend refresh calls, or reconciliation operations incur token cost or API cost.

**CA-2: FAIL** — No cost model described.

**CA-3: FAIL** — No reference to budget enforcement for any operation described in this doc.

**SR-1: FAIL** — No structured records with typed fields defined. "What May Live in Local SQLite" enumerates content categories ("recently viewed records," "current project/session continuity markers," "cached read models," "draft work not yet committed") but these are governance categories, not record schemas.

**SR-2: FAIL** — No structure defined that would support writing parsing code. The Reconciliation Rule describes a behavioral outcome ("local material must be clearly identified as draft, stale, divergent, or pending review") without defining the data structure that carries that identification.

**AP-1: PASS** — The Governance Protection Rule explicitly enumerates what local support state must not create: "local support state must not create approval by implication," "local support state must not create readiness by implication," "local support state must not create handoff by implication," "local support state must not create execution authority by implication," and "local support state must not override bounded backend interface rules." The "What Must Not Become Local Truth" section lists six categories that must pass through canonical backend interfaces. The access restriction is unambiguous.

**AP-2: PARTIAL** — The Governance Protection Rule and Rules/Doctrine section state governed mutations "must still pass through canonical backend interfaces." Three governance docs are cited in Related Docs (db-posture.md, ADR-009, ADR-011). However, no approval class (Class B, Class C) is assigned to any local-first operation, no specific governance gate is named as applicable to reconciliation or divergence resolution, and no approval-and-escalation-model reference is present. Governance protection is stated in principle without citing the gate docs that enforce the protected actions.

---

### Score

**1 of 21 PASS — 1 PARTIAL — 19 FAIL**

---

### Critical gaps (FAIL items only)

**QM-1 through QM-5 — No query interface defined.** The doc defines governance posture and layering but specifies no query entry point, parameters, response structure, pagination, or filters for any operation against the local SQLite layer or the canonical backend refresh path. Risk: the desktop application's local hydration and backend refresh behavior cannot be implemented from this doc; implementers must invent the entire data access model.

**FR-1, FR-2, FR-3 — No freshness contract, threshold, or timestamps.** No freshness window, maximum age, minimum refresh cadence, or timestamp field requirement is defined. EVENT-18 in `desktop-invalidation-and-refresh-matrix.md` handles divergence consequences but the threshold at which divergence is declared is not defined. Risk: implementations will define independent freshness thresholds; local state may remain stale indefinitely without triggering any visible divergence signal or action block.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** Hydration and reconciliation operations constitute cross-system access that the activity-trail-model.md requires to produce records. No logging reference exists. The activity-trail-model.md also defines no `local.hydrate` or `local.reconcile` action type — a compound gap across both docs. Risk: the ecosystem cannot audit whether a governed action was taken against verified canonical state or against diverged local state.

**DG-1, DG-2, DG-3 — No degraded mode defined.** The boot sequence implies local-state-only operation before backend refresh, but duration limits, operator notification, action blocking posture, and recovery sequence are entirely absent. Risk: implementations will handle backend unavailability inconsistently; governed actions may proceed against unverified local state for an unbounded period.

**CA-1, CA-2, CA-3 — No cost accounting.** No cost model for canonical backend refresh calls or any other operation described. Risk: cost attribution for the hydration/reconciliation layer cannot be assigned from this doc.

**SR-1, SR-2 — No structured records.** Content categories for local SQLite are enumerated but no typed field definitions are provided. Risk: local SQLite schema will be designed independently per implementation team, producing inconsistent local stores that cannot be queried, reconciled, or migrated uniformly.

---

### Summary

`local-first-architecture.md` is a governance posture and persistence-boundary doctrine doc. Its single PASS is for the Governance Protection Rule — a clear enumeration of what local support state must not create, with a matching "What Must Not Become Local Truth" section. The 19 FAILs reflect the doc's intentional scope: it defines the three-layer model and governance rules but commits to no query mechanics, freshness contract, activity logging, degraded-mode posture, cost accounting, or record structure. The most operationally significant gap is the combination of missing degraded-mode definition (DG-1 through DG-3) with missing freshness thresholds (FR-1, FR-2): local-state-only operation is enabled before backend refresh completes but no duration limit, action-blocking posture, or recovery sequence is defined — while activity trail logging is entirely absent, making it impossible to audit whether a governed action was taken against verified canonical state or against diverged local state.
