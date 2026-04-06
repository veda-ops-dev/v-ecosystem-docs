# Pass 3 Findings — Interface Completeness

Doc audited: `v-forge-to-project-v-return-to-planning-interface.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\v-forge-to-project-v-return-to-planning-interface.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\governance\approval-and-escalation-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\governance\report-structure-and-required-fields.md` (referenced in Related Docs)

### Files excluded

None found.

---

### Checklist results

**QM-1: PARTIAL** — The interface direction is clearly stated: "The V Forge to Project V return-to-planning interface is the bounded mechanism by which V Forge provides Project V with the execution-side findings required for planning reconsideration." Sender and receiver are identified. However, the Out of Scope section explicitly excludes "detailed transport or implementation format," and no initiation model (push vs. pull, API call chain, or mechanism) is defined.

**QM-2: FAIL** — The "What Return-to-Planning Transfers" and "Minimum Interface Semantics" sections list semantic elements (bounded execution findings, description of what happened, reason planning reconsideration is required, blockers and failures, references for interpretation), but the doc explicitly defers structure: "these semantics may later be represented through specific data structures, but the semantic contract comes first." The doc also explicitly excludes "detailed report structure" from scope. No field names, types, or valid values are defined.

**QM-3: FAIL** — No return package structure is defined, and no acknowledgment or receipt response from Project V back to V Forge is specified. The doc notes that a return-to-planning transition "does not automatically cancel or supersede the existing handoff," but nothing specifies what Project V returns to V Forge after receiving the package.

**QM-4: FAIL** — Not addressed. Return package size constraints or finding count limits are unspecified.

**QM-5: FAIL** — No selection or filter criteria defined for what findings V Forge includes in the return package. "V Forge is responsible for determining what execution-side information is included in the return" is a responsibility assignment, not a filter specification.

**FR-1: FAIL** — No freshness contract for the return package content. No specification of how current the execution findings must be relative to the execution events they describe.

**FR-2: FAIL** — Not addressed. No staleness threshold defined for return package content.

**FR-3: FAIL** — No timestamp field specified for the return package or any acknowledgment structure.

**AL-1: FAIL** — The doc contains no mention of activity trail records, activity logging, or any logging requirement. The activity-trail-model.md does not define a dot-namespaced action type for return-to-planning (the vocabulary includes `handoff.create`, `handoff.approve`, `handoff.reject`, but no `return.create` or equivalent). This is an upstream model gap in the activity trail vocabulary. Regardless, the interface doc itself makes no reference to any logging requirement for this cross-system governance event.

**AL-2: FAIL** — No action field value is specified in the interface doc, and the activity-trail-model.md defines no applicable dot-namespaced action type for return-to-planning. The closest candidates in the vocabulary (`task.fail`, `task.cancel`) are V Forge-internal, and approval actions (`approval.request`, `approval.decide`) describe the downstream planning review, not the return transfer itself.

**AL-3: FAIL** — No activity record fields mentioned — no actor, target, entity_type, entity_id, or cost fields.

**DG-1: FAIL** — No degraded mode defined. The doc does not address what happens if Project V is unavailable when V Forge attempts a return-to-planning transfer, or if the package delivery fails.

**DG-2: FAIL** — V Forge caller behavior during degraded mode is not defined. No mention of retry, queue, block, or preservation posture.

**DG-3: FAIL** — No recovery path defined.

**CA-1: FAIL** — The doc does not state whether this interface incurs token cost or API cost.

**CA-2: FAIL** — No cost model described.

**CA-3: FAIL** — No reference to budget enforcement for this interface.

**SR-1: FAIL** — No structured return package fields are defined. The Minimum Interface Semantics section explicitly defers: "these semantics may later be represented through specific data structures, but the semantic contract comes first." The Out of Scope section also explicitly excludes "detailed report structure." Semantic elements are listed as prose, not typed fields.

**SR-2: FAIL** — No structure is defined; parsing code cannot be written against this doc.

**AP-1: PARTIAL** — The Return-to-Planning Validity Conditions section establishes prerequisites for a valid return: V Forge must have "produced bounded execution findings relevant to planning reconsideration" and the return must be "triggered by blocked, failed, incomplete, or changed execution conditions that cannot be resolved within the approved handoff scope." The Human-In-The-Loop section states: "All return-to-planning transitions that affect planning direction should be reviewed by a human before planning reconsideration results in new ecosystem actions," and references `../governance/approval-and-escalation-model.md`. The loaded governance model confirms return-to-planning is a Class B action ("returning execution findings into a planning-affecting path"). However, the interface doc does not specify the approval class.

**AP-2: PARTIAL** — The doc references `../governance/approval-and-escalation-model.md` in the Human-In-The-Loop section and `../governance/report-structure-and-required-fields.md` in the Finding Boundary Constraint section. Validity conditions are established. However, no specific gate class (A/B/C/D) is assigned in the interface doc itself.

---

### Score

**0 of 21 PASS — 3 PARTIAL — 18 FAIL**

---

### Critical gaps (FAIL items only)

**QM-2, QM-3, SR-1, SR-2 — No data contract defined.** The doc explicitly defers all structure to future work and explicitly excludes "detailed report structure" from scope. No return package schema, field definitions, or acknowledgment structure exists. Risk: every implementation of the return-to-planning package will invent its own structure, making it impossible for Project V to reliably parse or validate what V Forge sends.

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent, and the activity trail model itself lacks a return-to-planning action type.** The interface doc makes no reference to logging requirements. The activity-trail-model.md defines no applicable action type for this cross-system transfer (unlike handoffs, which have `handoff.create`, `handoff.approve`, `handoff.reject`). A return-to-planning is clearly a state-changing governance event that crosses a system boundary — both categories that require activity records per the model. Risk: return-to-planning transitions will be unauditable, and the activity trail model is incomplete for this pattern.

**DG-1, DG-2, DG-3 — No degraded mode or recovery path.** If Project V is unavailable when V Forge triggers a return-to-planning, V Forge has no specified behavior. This creates the same split-state risk as the handoff interface: V Forge records a return as triggered; Project V never receives it. Risk: inconsistent handling of delivery failures, with no defined posture for V Forge to preserve the return state until recovery.

**FR-1, FR-2, FR-3 — No freshness or timestamp specification.** Return packages may include execution findings and evidence references, but no currency requirement or timestamp fields are defined. Risk: Project V may act on findings that describe outdated execution state without knowing their age.

**CA-1, CA-2, CA-3 — No cost accounting.** Return-to-planning packaging may involve LLM-assisted finding summarization. Neither cost existence nor model is stated. Risk: cost attribution for return-to-planning operations cannot be tracked.

**QM-4, QM-5 — No package constraints or selection criteria.** No ceiling on the number of findings that can be returned in one operation, and no specification of how V Forge selects which findings to include beyond the semantic principle that they must be "planning-relevant."

---

### Summary

`v-forge-to-project-v-return-to-planning-interface.md` follows the same pattern as the handoff interface and VEDA-to-Project V signal interface: a well-reasoned semantic contract documenting ownership, validity conditions, and boundary rules, with all data structure definition explicitly deferred to future work. The 18 FAILs and 3 PARTIALs reflect this gap consistently. One finding is distinct from prior interfaces: the activity-trail-model.md itself lacks a defined action type for return-to-planning, unlike handoffs (`handoff.create`/`handoff.approve`/`handoff.reject`), making the AL gap a compound problem — the interface doc is silent, and the upstream model is also incomplete for this pattern.

---

### Out-of-scope observations not included in findings

- The activity-trail-model.md is missing a dot-namespaced action type for return-to-planning, unlike the handoff vocabulary which is complete. This is a gap in the activity trail model itself; it was noted in scoring AL-2 but is a cross-system consistency issue for a later pass.
- The `report-structure-and-required-fields.md` governance doc, referenced by this interface, provides a reasonably complete minimum report structure (11 required fields) that could serve as the structural basis for the return package — but the interface doc does not incorporate it as a structural specification.
