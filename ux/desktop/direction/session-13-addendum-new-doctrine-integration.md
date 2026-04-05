# Session 13 — Addendum: New Doctrine Integration
## V Ecosystem Desktop UX

**Addendum to:** `session-13-handoff-review-ux-and-return-trigger-review-ux-spec.md`
**Reason:** Four new Tier 1 documents were added to the doctrine set after Session 13 was written. This addendum records their impact on Session 13 and their forward implications.

**New docs read:**
- `ecosystem/cross-system-access-governance.md`
- `ecosystem/activity-trail-model.md`
- `interfaces/v-forge-evidence-access-contract.md`
- `ecosystem/agent-effectiveness-audit.md`

---

## What These Docs Add

### cross-system-access-governance.md

Formalises the "own narrowly, access broadly, govern the access" principle. Every cross-system data read must be: logged in the activity trail, project-scoped, cost-accounted, and carry provenance metadata. This is the governance backbone for what the desktop application already surfaces as ownership labels and evidence attribution.

**Effect on Session 13:** No contradiction. Confirms that the ownership labels in the Evidence sections ("SOURCE: VEDA — referenced, not owned by Project V") and the `NOT a VEDA signal record` note on execution evidence are correct applications of this principle. These labels are not cosmetic — they correspond to a real governed access model.

### activity-trail-model.md

Every meaningful action produces a structured activity record. The action vocabulary includes `handoff.approve`, `handoff.reject`, `approval.request`, `approval.decide`, `agent.start`, `agent.complete`, `evidence.query`, and others.

**Effect on Session 13 — History section entries:**

The History section entries in both the Handoff Review View (§4.7) and the Return Trigger Review View (§5.7) should reference the activity trail action types in their Record ID column. The history timeline is a projected view of the activity trail for the current record, not a separate bespoke log.

**Updated event label vocabulary for History section rows:**

| Activity trail action | History section label |
|---|---|
| `approval.request` | `Approval request initiated` |
| `approval.decide` (approved) | `Approval recorded` |
| `approval.decide` (rejected) | `Approval rejected` |
| `handoff.approve` | `Handoff activated` |
| `handoff.reject` | `Handoff activation rejected` |
| `handoff.create` | `Handoff package prepared` |
| `agent.start` | `Execution started` |
| `agent.complete` | `Execution completed` |
| `agent.block` | `Execution blocked` |
| `agent.pause` | `Execution paused` |
| `evidence.query` | `Evidence queried` (only surfaced in trace surface, not in handoff History) |

The Record ID column in History entries now maps to the activity trail `activity_id` for the event, rather than a vague bracketed reference. This allows future implementations to link from a history entry directly to the full activity trail record.

### v-forge-evidence-access-contract.md

V Forge agents may actively query VEDA evidence during execution using four query types. Evidence responses carry a required freshness metadata set: `evidence_id`, `gathered_at`, `source_provider`, `source_url`, `freshness_status` (fresh / aging / stale / expired), `freshness_window_end`, `trust_classification`.

**Effect on Session 13 — Evidence section rows:**

The evidence row format specified in §4.5 (Handoff Review Evidence section) and §5.5 (Return Trigger Evidence section) needs one update: the metadata line should use the canonical field names from the evidence access contract, not informal equivalents.

**Updated evidence row format (replaces the metadata line in §4.5 and §5.5):**

```
[obs-047]   Hosting keyword intent snapshot
            Source: VEDA — google_search_console  ·  Gathered: 2026-04-01 14:32
            Freshness: fresh  ·  Trust: verified
            Used as: Readiness basis for search intent signal
```

Field mapping:
- `Source: VEDA — [source_provider]` — combines system ownership with the `source_provider` field from the contract
- `Gathered: [gathered_at]` — replaces "Captured:" to match the contract field name
- `Freshness: [freshness_status]` — exact contract field values: `fresh`, `aging`, `stale`, `expired`
- `Trust: [trust_classification]` — exact contract values: `verified`, `provisional`, `unverified`

The `freshness_status` field drives the inline stale marker:
- `fresh`: no marker — the row is clean
- `aging`: `⚠ AGING` in `--state-warning`, `--type-xs` (softer than stale — approaching but not yet exceeded)
- `stale`: `⚠ STALE — [age]` in `--staleness-text` — same as Session 13 §4.5
- `expired`: `⛔ EXPIRED — should not be used for execution decisions` in `--state-blocked`, `--type-xs` — stronger than stale; expired evidence should not be cited in approval basis

**The "Used as" field** — confirmed correct by the evidence access contract. The contract states handoff packets should carry VEDA evidence *references* (not copies), so the "Used as" line correctly contextualises why a referenced record was included, while the actual record content is queried fresh through the access contract.

**New: `source_url` display** (in expanded evidence row, not compact):

When a History section or Evidence section row is expanded:

```
[obs-047]   Hosting keyword intent snapshot
            Source: VEDA — google_search_console
            Source URL: https://search.google.com/search-console/...  (truncated)
            Gathered: 2026-04-01 14:32  ·  Freshness: fresh  ·  Trust: verified
            Freshness window ends: 2026-04-08 14:32
            Used as: Readiness basis for search intent signal
```

`Source URL`: `--text-link`, `--type-xs` — clickable, opens in the operator's browser. `Freshness window ends`: `--type-xs`, `--text-tertiary`.

### agent-effectiveness-audit.md

A working audit identifying 10 systematic gaps. The UX-relevant findings:

**Finding 5 (Structured Approval Records):** The approval record fields proposed in Finding 5 (`approval_id`, `approval_type`, `status`, `requested_by`, `requested_at`, `decided_by`, `decided_at`, `decision_note`, `linked_entities`, `expiry`) are consistent with what the Session 10 gate widget post-approval confirmation state displays. When `approval-and-escalation-model.md` is updated with these fields, the History section's approval events can reference `approval_id` directly.

**Finding 10 (Structured Handoff Packet):** The proposed handoff packet fields are consistent with the Session 13 Handoff Review Overview section layout. When the structured packet is formally defined, the following field mappings apply:

| Handoff packet field | Session 13 Overview location |
|---|---|
| `objective` | "What is handed off" prose block |
| `scope` | `APPROVED SCOPE` block |
| `constraints` | Out-of-scope items list |
| `evidence_references` | Evidence section rows (references, not copies) |
| `acceptance_criteria` | Not yet surfaced — add to Overview as `Completion criteria:` field |
| `approval_record` | History entry for `approval.decide` |
| `escalation_policy` | Not yet surfaced — add to Transfer block |
| `reporting_contract` | Not yet surfaced — add to Transfer block |
| `budget_allocation` | Not surfaced in UX — backend concern; surfaced in trace surface (Session 18) |

**Action: Two fields to add to the Handoff Review Overview section** when the structured packet is formally defined:

To the **Scope block**, after "What this handoff does NOT transfer":
```
Completion criteria:
  [acceptance_criteria from handoff packet]
  These define when V Forge's execution responsibility is considered discharged.
```

To the **Transfer block**, after "Activation posture":
```
Escalation policy:  [escalation_policy value — e.g., "return_to_planning on block"]
Reporting contract: [reporting_contract value — e.g., "event_stream + completion_report"]
```

These fields are marked `[SCHEMA PENDING]` until the structured handoff packet is formally defined and the packet fields have canonical record anchors. Show as `--state-schema-hold` text with `[SCHEMA PENDING]` inline tag if the field cannot be derived from current records.

**Finding 2 (Activity Trail Integration):** The handoff and return-to-planning interface docs are listed as lacking activity trail integration sections. When those docs are updated, the History sections in Session 13's surfaces will automatically have richer backing data. The Session 13 History section format is compatible — it just needs the `activity_id` references populated once the trail integration is in place.

**Finding 3 (Freshness model for VEDA → Project V):** Currently, VEDA signal consumed by Project V for planning decisions does not carry the same freshness metadata that V Forge evidence queries now carry. When this gap is addressed, the context strip's EVIDENCE category and the center workspace Evidence sections will already be displaying the right fields (`freshness_status`, `trust_classification`, `gathered_at`) — the evidence access contract has established the canonical field vocabulary.

---

## Impact on Sessions 1–12

Sessions 1–12 are not contradicted by these four docs. The new docs confirm and deepen the foundations already established:

- Sessions 4–5 (Context Strip, Right Panel): Evidence attribution, ownership labels, freshness markers — all confirmed by `cross-system-access-governance.md` and `v-forge-evidence-access-contract.md`.
- Session 9 (Center Workspace): History section concept confirmed by `activity-trail-model.md`. Action vocabulary now has canonical names.
- Session 10–11 (Gate Surfaces, Routing Flow): Approval event persistence confirmed by `activity-trail-model.md`. `approval.decide` is a named activity trail action type.
- Session 12 (Alerts/Notifications): No conflict. Budget governance events (`budget.warning`, `budget.hard_stop`) from `activity-trail-model.md` are not yet surfaced in the notification system — that's Session 18 (Agent Transparency / Lower Trace Surface) territory.

---

## Impact on Sessions 14+

**Session 14 (Launch Readiness UX):** The evidence access contract metadata fields (`freshness_status` = `expired` is now possible as a distinct value, not just `stale`) should be incorporated into the launch readiness Evidence section. The Evidence Currency Principle from the launch readiness workflow has an even stricter threshold for launch-sensitive decisions — the `expired` freshness_status should be an absolute block on the launch authorization gate, not just a warning.

**Session 15 (Maintenance / Ranking UX):** Finding 9 in the audit document specifically addresses maintenance: "V Forge agents actively querying VEDA via the evidence access contract during maintenance cycles." The maintenance UX surface should reflect that V Forge has live evidence access during maintenance — the return trigger findings V Forge produces may already incorporate freshly-queried evidence, which should be visible in the Return Trigger Evidence section.

**Session 18 (Agent Transparency / Lower Trace Surface):** The activity trail model is the primary data source for the lower trace surface. The action vocabulary, required fields, and `cross_system_access` action class from `activity-trail-model.md` define what the trace surface displays. Budget events (`budget.warning`, `budget.hard_stop`, `budget.cost_event`) should also appear in the trace surface.

---

*This addendum is part of the Session 13 spec record. All Session 13 section references remain valid; this addendum adds precision to §4.5, §4.7, §5.5, and §5.7.*
