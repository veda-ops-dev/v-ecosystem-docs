# Pass 3 Findings — Interface Completeness

Doc audited: `runtime-sidecar-and-nerve-model.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\runtime-sidecar-and-nerve-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\interfaces\mcp-coordination-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\nerve\README.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-010-agent-orchestration-is-an-extension-runtime-capability.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\ecosystem\decisions\ADR-011-tauri-2-desktop-is-the-operator-host.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\interfaces\desktop-agent-orchestration-model.md` (referenced in doc body as named successor)
- `C:\dev\v-ecosystem-docs\ux\desktop\direction\desktop-host-migration-plan.md` (referenced in Related Docs)

### Files excluded

None found.

---

### Checklist results

**QM-1: FAIL** — No query entry point defined. The Communication Model section states "The desktop frontend communicates with the sidecar/runtime layer through the Tauri host boundary. The sidecar/runtime layer communicates with canonical backend services through approved backend interfaces" — naming communication direction but defining no entry point, API surface, or protocol. The doc explicitly defers to `mcp-coordination-model.md` and companion implementation-design docs for specifics.

**QM-2: FAIL** — No input parameters defined. The sidecar/runtime layer's owned responsibilities are listed but no parameter names, types, or valid values are specified for any of them. The Scope section lists "MCP session/runtime coordination support," "compaction and continuity-support mechanics," "token and cost tracking support" and others, but specifies no parameters for any.

**QM-3: FAIL** — No response structure defined. The Traceability and Visibility section requires "traceable outputs" and "runtime trace/event support passed back to the frontend" but specifies no fields, types, or payload structure for any output.

**QM-4: FAIL** — Pagination and result limits not addressed. No operation is specified in sufficient detail for these to be assessable.

**QM-5: FAIL** — No filter options documented. No operation is specified in sufficient detail for filter parameters to be assessable.

**FR-1: FAIL** — No freshness contract defined. The Persistence Posture section permits local runtime-support persistence for continuity and compaction support but defines no freshness requirement, refresh cadence, or maximum age for any such data.

**FR-2: FAIL** — No staleness threshold defined. "Local runtime persistence does not replace backend records" is a posture statement, not a threshold.

**FR-3: FAIL** — No `last_updated` or equivalent timestamp field specified for any output from the sidecar/runtime layer.

**AL-1: FAIL** — Activity trail logging not mentioned anywhere in the doc. The Traceability and Visibility section requires "traceable outputs" and "visible status where materially relevant" but connects these to no activity trail obligation. The activity-trail-model.md requires records for all agent lifecycle events (`agent.start`, `agent.complete`, `agent.fail`, `agent.pause`, `agent.resume`, etc.) and system events (`system.startup`, `system.error`, etc.) — all falling within the sidecar/runtime layer's stated responsibilities. No logging requirement of any kind is stated.

**AL-2: FAIL** — No dot-namespaced action field value specified. The activity-trail-model.md defines directly applicable vocabulary: `agent.start`, `agent.heartbeat`, `agent.complete`, `agent.fail`, `agent.block`, `agent.pause`, `agent.resume`, `system.startup`, `system.shutdown`, `system.error`, `system.recovery`. None are referenced in this doc.

**AL-3: FAIL** — No activity record fields mentioned. None of the canonical required fields from the activity-trail-model.md (actor, target, entity_type, entity_id, action_class, cost fields) appear anywhere in this doc.

**DG-1: FAIL** — Degraded mode not defined. The Communication Model names the sidecar's communication paths (Tauri host boundary, approved backend interfaces) but defines no behavior for path failures, backend service unavailability, or sidecar process failure.

**DG-2: FAIL** — Caller behavior during degraded mode not defined. No specification exists for what the desktop frontend must do if the sidecar/runtime layer becomes unresponsive, or what the sidecar must do if backend services are unavailable.

**DG-3: FAIL** — No recovery path defined. No restart procedure, re-initialization trigger, retry behavior, or recovery sequence described for any degraded condition.

**CA-1: PARTIAL** — The doc lists "token and cost tracking support" as a sidecar/runtime layer responsibility. This acknowledges cost tracking as within scope. However, the doc does not state whether the sidecar's own coordination and orchestration work incurs token cost or API cost — only that it provides tracking support for costs incurred elsewhere. The distinction is not drawn.

**CA-2: FAIL** — No cost model described for any sidecar/runtime operation. The responsibility assignment ("token and cost tracking support") is not a cost model for the sidecar layer itself.

**CA-3: FAIL** — No reference to budget enforcement for sidecar/runtime operations. No budget doc, threshold, or enforcement mechanism cited.

**SR-1: FAIL** — No structured records with typed fields defined. "Runtime trace/event support passed back to the frontend" is a requirement statement, not a record schema.

**SR-2: FAIL** — No structure defined that would support writing parsing code for any output from the sidecar/runtime layer.

**AP-1: PARTIAL** — The doc establishes governance posture clearly: "The sidecar/runtime layer must not silently mutate canonical state outside approved backend interfaces and governance paths" and "runtime support may narrow or preserve scope; it must not self-authorize scope expansion." The sidecar is unambiguously subordinate to approval requirements. However, no specific approval class (Class B, Class C) is assigned to any sidecar operation, and no specific gate is identified as applicable to the sidecar layer's own access.

**AP-2: PARTIAL** — `mcp-coordination-model.md`, `ADR-010`, `ADR-011`, and multiple companion implementation-design docs are referenced. However, no specific governance gate is identified as applicable to the sidecar layer itself, no approval-and-escalation-model citation is present, and governance protection is stated as a posture rule ("must not become a shadow authority root") without citing the gate docs that enforce that constraint.

---

### Score

**0 of 21 PASS — 3 PARTIAL — 18 FAIL**

---

### Critical gaps (FAIL items only)

**QM-1 through QM-5 — No query interface defined.** The doc defines runtime placement and ownership boundaries but specifies no call chain, parameters, response structure, pagination, or filters for any sidecar operation. Risk: the sidecar/runtime layer's communication model — from the desktop frontend and toward canonical backend services — cannot be implemented from this doc; the entire interface contract must be invented.

**FR-1, FR-2, FR-3 — No freshness contract, threshold, or timestamps.** Locally persisted runtime-support data has no defined freshness requirement, age limit, or timestamp requirement. Risk: stale continuity artifacts, session state, and compaction artifacts may be used without any threshold triggering a refresh or discard.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** The sidecar/runtime layer owns agent lifecycle management — the exact operation class for which the activity-trail-model.md defines mandatory action vocabulary (`agent.start`, `agent.complete`, `agent.fail`, `agent.pause`, `agent.resume`, `system.startup`, `system.error`). The Traceability and Visibility section requires outputs to be "traceable" but connects this to no activity logging obligation. Risk: all agent lifecycle events managed by the sidecar — starts, completions, failures, blocks, pauses — will produce no ecosystem activity trail records, breaking the governance replay capability for all orchestrated execution.

**DG-1, DG-2, DG-3 — No degraded mode defined.** The sidecar/runtime layer sits between the desktop frontend and canonical backend services, making its failure mode operationally critical. No behavior is defined for sidecar unavailability, backend service unavailability seen from the sidecar, or Tauri host boundary failure. Risk: the most disruptive runtime failure mode has no defined posture, no blocking rule for governed actions, and no recovery path.

**CA-2, CA-3 — No cost model or budget enforcement reference.** The sidecar is assigned "token and cost tracking support" but no cost model or enforcement reference is provided for the sidecar's own operations. Risk: cost attribution for sidecar coordination and orchestration work itself cannot be assigned from this doc.

**SR-1, SR-2 — No structured records.** Traceability requirements are stated and output categories named (trace artifacts, runtime events, runtime status) but no field definitions are provided for any of them. Risk: runtime trace and event outputs will be structured independently by each implementation team without a shared record contract.

---

### Summary

`runtime-sidecar-and-nerve-model.md` is an architectural placement and ownership-boundary doctrine doc. Its 3 PARTIALs reflect genuine but incomplete governance coverage: the doc acknowledges cost tracking as a sidecar responsibility without stating whether the sidecar itself incurs cost, establishes that governed actions require approval without specifying which approvals apply, and references multiple governance docs without identifying which gates apply to the sidecar layer's own access. The 18 FAILs reflect the doc's intentional scope — it defines where the sidecar belongs and what it must not become, deferring all interface specifics, lifecycle details, compaction behavior, token tracking, and transcript mechanics to companion implementation-design docs. The most operationally significant gap is AL-1/AL-2/AL-3 combined with DG-1/DG-2/DG-3: the sidecar/runtime layer owns agent lifecycle events that the activity-trail-model.md explicitly requires to produce activity records, but this doc contains no logging obligation; and the sidecar is the runtime engine whose failure is most disruptive to operator work, but no degraded-mode posture, caller behavior, or recovery path is defined.
