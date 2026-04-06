## Pass 5 Findings — Cross-System Consistency

Session: C
Systems audited: Project V ↔ V Forge
Date: 2025-04-05

### Files loaded
- `C:\dev\v-ecosystem-docs\audit\pass-5\pass-5-cross-system-consistency.md`
- `C:\dev\v-ecosystem-docs\project-v\project-v.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\project-v\system-invariants.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\project-v\operational-workflow.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\project-v\data-boundaries.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\project-v\v-forge-integration.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\project-v\lifecycle.md`
- `C:\dev\v-ecosystem-docs\v-forge\v-forge.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\v-forge\system-invariants.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\v-forge\data-boundaries.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\v-forge\vs-project-v.md`
- `C:\dev\v-ecosystem-docs\v-forge\reporting-and-approval-model.md`
- `C:\dev\v-ecosystem-docs\interfaces\project-v-to-v-forge-handoff-interface.md`
- `C:\dev\v-ecosystem-docs\interfaces\v-forge-to-project-v-return-to-planning-interface.md`
- `C:\dev\v-ecosystem-docs\interfaces\data-boundaries.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-access-governance.md` (loaded prior session)

### Files excluded
- `C:\dev\v-ecosystem-docs\project-v\multi-project-doctrine.md` — internal Project V multi-project scope; not needed for seam consistency judgment
- `C:\dev\v-ecosystem-docs\project-v\schema-specification.md` — internal schema; not needed for seam consistency
- `C:\dev\v-ecosystem-docs\v-forge\operational-model.md` — internal V Forge operational workflow; not needed for seam consistency
- `C:\dev\v-ecosystem-docs\v-forge\content-lifecycle-workflow.md` — internal V Forge workflow; not needed for seam consistency
- `C:\dev\v-ecosystem-docs\v-forge\human-in-the-loop-doctrine.md` — internal V Forge governance; not needed for seam consistency

---

### Interface coverage gaps

**Expected interactions for Project V ↔ V Forge:**

1. Project V → V Forge: handoff (planning-ready work becomes active execution responsibility)
   - Status: EXISTS — `project-v-to-v-forge-handoff-interface.md`
   - Both system docs agree on direction and semantics: PASS

2. V Forge → Project V: return-to-planning (execution findings requiring planning reconsideration)
   - Status: EXISTS — `v-forge-to-project-v-return-to-planning-interface.md`
   - Both system docs agree on direction and semantics: PASS

3. Project V → V Forge: mid-execution scope clarification or approval coordination (referenced in `project-v\v-forge-integration.md`)
   - Status: **PARTIAL / MISSING** — `v-forge-integration.md` states: "Where V Forge requires additional planning-side approval or scope clarification during execution, without full return-to-planning being required, that coordination must still occur through the governed interface path." No interface doc governs this coordination path. The sentence asserts a governed path exists but the path is not defined.

4. Project V → V Forge: handoff recall / post-transfer reconsideration initiation
   - Status: **MISSING** — `v-forge-integration.md` defines a "Handoff Recall and Reconsideration Rule" requiring a "governed recall mechanism, either through an operator-directed instruction that reverses the handoff with the required approval posture, or through a V Forge return-to-planning input where V Forge has not yet acted on the handoff." No interface doc governs the operator-directed recall path. The return-to-planning path is covered by the return interface, but the operator-directed recall path has no governing doc.

5. Project V → V Forge: scope change notification after replanning
   - Status: **MISSING** — `maintenance-and-replanning-workflow.md` (reviewed in Pass 4) states that Stage 6 requires V Forge to be "informed of any scope or constraint changes through the governed interface" but does not name the interface. No interface doc governs this post-replanning notification path from Project V to V Forge.

---

### Access rule mismatches

**Finding C-1: `cross-system-access-governance.md` describes "Project V → V Forge" as read-only access for planning context — but this conflicts with Project V's role as the handoff initiator, which is a write-governance action**

`cross-system-access-governance.md` under "V Forge → Project V (Planning Context)": "Access type: Read-only, project-scoped, limited to active handoff context. Purpose: V Forge reads the approved handoff, project structure, and planning context that defines what it should execute."

This entry conflates two distinct directions: the access governance doc describes V Forge reading Project V planning context (V Forge → Project V), but in doing so implies Project V does not actively push or deliver anything to V Forge — it only sits there to be read. The handoff interface (`project-v-to-v-forge-handoff-interface.md`) describes Project V as the initiating system that "provides V Forge with the execution-facing package." Whether the handoff is a push (Project V delivers) or a pull (V Forge reads) is unresolved at the governance level, mirroring the Session A and B finding for VEDA → Project V.

The handoff is not simply a read-only V Forge pull. It is a governed transfer event initiated by Project V. The cross-system-access-governance.md's framing suppresses the Project V side of the handoff as an access governance event entirely.

Docs involved:
- `ecosystem\cross-system-access-governance.md`: frames the interaction as V Forge reading Project V; no entry for Project V initiating handoff as a governed access event
- `interfaces\project-v-to-v-forge-handoff-interface.md`: "Project V provides V Forge with the execution-facing package required to carry out approved work"

**Finding C-2: Activity trail has `execution.query` for Project V reading V Forge execution results, but no action type for V Forge return-to-planning delivery**

`ecosystem\activity-trail-model.md` Cross-system access actions include: `execution.query` — "Project V reading V Forge execution results." This implies a pull model (Project V queries V Forge). However, the `v-forge-to-project-v-return-to-planning-interface.md` describes return-to-planning as V Forge delivering bounded execution findings to Project V — a push initiated by V Forge, not a Project V query.

The activity trail has no action type for V Forge delivering a return-to-planning package. The `execution.query` action type covers Project V reading execution results, but does not cover V Forge initiating a return-to-planning transfer. If the return is modeled as a push, there is no activity trail action type for it. If it is a pull (`execution.query`), then the interface doc's description of V Forge as the initiator is inconsistent with the access model.

Docs involved:
- `ecosystem\activity-trail-model.md`: `execution.query` = "Project V reading V Forge execution results"; no return-to-planning delivery action type
- `interfaces\v-forge-to-project-v-return-to-planning-interface.md`: V Forge provides bounded findings to Project V; V Forge is the initiator

**Finding C-3: `cross-system-access-governance.md` governs "Project V → V Forge" under the return-to-planning interface but the return direction is V Forge → Project V**

`cross-system-access-governance.md` under "Project V → V Forge (Execution Results)": "Access type: Read-only, project-scoped. Governed by: `v-forge-to-project-v-return-to-planning-interface.md`. Purpose: Project V reads V Forge execution findings, completion reports, and maintenance signals to inform replanning."

The governance doc names the return-to-planning interface as the governing doc for "Project V → V Forge" access, but that interface governs V Forge → Project V, not Project V → V Forge. The access direction label and the governing interface direction are inverted. This is a direct error in the access governance doc — the access pair label says "Project V → V Forge" but the described behavior is Project V reading V Forge, which is V Forge → Project V in the direction of data flow.

Docs involved:
- `ecosystem\cross-system-access-governance.md`: access pair labeled "Project V → V Forge (Execution Results)" governed by `v-forge-to-project-v-return-to-planning-interface.md`
- `interfaces\v-forge-to-project-v-return-to-planning-interface.md`: governs V Forge → Project V data flow

---

### Activity / traceability mismatches

**Finding C-4: No activity trail action type covers handoff initiation by Project V**

The activity trail model defines `handoff.create` and `handoff.approve` and `handoff.reject` as state change actions. These action types cover the handoff record lifecycle but not the cross-system delivery event of the handoff package from Project V to V Forge at activation time.

`handoff.create` could be interpreted as covering the creation of a handoff record in Project V. `handoff.approve` covers approval. But the moment execution responsibility transfers — the cross-system event of the active handoff being delivered — has no dedicated action type. The handoff interface describes this as a governance-sensitive transition ("A handoff should never be treated as a casual internal state flip if it changes who is responsible for execution"), but the activity trail treats it as a state change within Project V rather than a cross-system boundary crossing event.

Docs involved:
- `ecosystem\activity-trail-model.md`: `handoff.create`, `handoff.approve`, `handoff.reject` — all state change actions; no cross-system transfer action type for handoff activation
- `interfaces\project-v-to-v-forge-handoff-interface.md`: handoff is a governance-sensitive cross-system transfer event

**Finding C-5: Return-to-planning transition produces no named activity trail record from V Forge's side**

Related to Finding C-2. The activity trail model defines `approval.request` and `approval.decide` for approval events, and state changes for handoff records. No action type exists for V Forge initiating a return-to-planning transition. `v-forge\reporting-and-approval-model.md` specifies that return-to-planning findings "must be packaged and reported through the return-to-planning interface before it becomes a planning input" — this is a governed cross-system event. The ecosystem activity trail has no vocabulary for it.

Docs involved:
- `ecosystem\activity-trail-model.md`: no action type for return-to-planning initiation or delivery
- `v-forge\reporting-and-approval-model.md`: return-to-planning is a required reporting event

**Finding C-6: Project V lifecycle state changes (Handed Off, Return Under Reconsideration) are cross-system-relevant events with no corresponding activity trail action types**

`project-v\lifecycle.md` defines 11 lifecycle stages including "Handed Off" and "Return Under Reconsideration" — stages that are directly triggered by or paired with cross-system events (handoff activation, return-to-planning receipt). Neither lifecycle stage transition appears in the activity trail action vocabulary. The activity trail's `handoff.create` and `handoff.approve` action types track handoff record state but do not map to the Project V lifecycle state change events that occur in parallel.

This creates a traceability gap: a later reviewer using the activity trail cannot determine when a Project V project transitioned into the "Handed Off" lifecycle state or when it entered "Return Under Reconsideration," even though both are governance-relevant cross-system events.

Docs involved:
- `project-v\lifecycle.md`: "Handed Off" and "Return Under Reconsideration" as explicitly defined lifecycle stages with cross-system triggers
- `ecosystem\activity-trail-model.md`: no lifecycle state transition action types; `handoff.create` covers record creation but not lifecycle stage change

---

### Role boundary violations

**Finding C-7: `v-forge\reporting-and-approval-model.md` assigns approval classes for V Forge context — but approval class assignment is a governance authority, not a V Forge authority**

`v-forge\reporting-and-approval-model.md` "Approval Classes in V Forge Context" section assigns specific V Forge behaviors to each Class A–D: "Class C — launch-sensitive execution, external paid actions, scope-expanding execution, and public-facing publication. Requires explicit human approval." This section is a V Forge-authored interpretation of what the shared ecosystem approval model means in V Forge's context.

The `governance\approval-and-escalation-model.md` (loaded in prior sessions) is the Tier 1 authority for approval class definitions. V Forge applying those classes to its own context is expected and appropriate — the concern is whether V Forge's local interpretation in `reporting-and-approval-model.md` matches the Tier 1 definitions. This requires checking whether V Forge's Class B definition matches the governance model's Class B.

The governance model's Class B covers: "activating an intake outcome that materially changes planning status; preparing or activating a handoff; returning execution findings into a planning-affecting path." V Forge's reporting model defines Class B as: "mutating execution state in ways that are expected but meaningful, such as marking a bounded execution scope complete or activating a return-to-planning transfer." These are not contradictory, but V Forge's Class B definition omits "preparing or activating a handoff" as a Class B example even though handoff activation is one of the governance model's primary Class B examples. An implementer reading only V Forge's doc would not know handoff activation is explicitly Class B in the governance model.

Docs involved:
- `v-forge\reporting-and-approval-model.md`: Class B = "mutating execution state... marking a bounded execution scope complete or activating a return-to-planning transfer"
- `governance\approval-and-escalation-model.md` (Tier 1): Class B includes "preparing or activating a handoff" — not reflected in V Forge's local Class B definition

**Finding C-8: `v-forge\vs-project-v.md` says "V Forge does not decide that replanning is needed" — but `v-forge\reporting-and-approval-model.md` lists "return-to-planning trigger" as a required V Forge reporting event, implying V Forge does identify when return is needed**

`v-forge\vs-project-v.md`: "V Forge does not decide that replanning is needed. V Forge identifies that a finding may warrant reconsideration and returns it."

`v-forge\reporting-and-approval-model.md` under "When Reporting Is Required": "Return-to-planning trigger — When V Forge identifies a finding that warrants planning reconsideration, the finding must be packaged and reported through the return-to-planning interface before it becomes a planning input."

The distinction between "identifying that a finding warrants reconsideration" and "deciding that replanning is needed" is a semantic hairline. The vs-project-v.md doc uses it to preserve the principle that planning decisions belong to Project V. However, `v-forge-to-project-v-return-to-planning-interface.md` defines validity conditions for return: the return is valid when triggered by "findings that change what planning should do next." V Forge must evaluate whether a finding meets this condition to determine if a return-to-planning is warranted — which is itself a judgment call that edges toward planning-relevant decision-making. The seam between "V Forge identifies a finding may warrant reconsideration" and "V Forge decides reconsideration is needed" is not defined with a testable boundary.

This is a mild role tension at the seam, not a direct contradiction. V Forge making a threshold judgment about return-worthiness is unavoidable in practice, but neither the interface doc nor the vs-project-v.md doc defines the threshold or decision rule.

Docs involved:
- `v-forge\vs-project-v.md`: "V Forge does not decide that replanning is needed"
- `v-forge\reporting-and-approval-model.md`: return-to-planning trigger requires V Forge to identify when a finding "warrants planning reconsideration"
- `interfaces\v-forge-to-project-v-return-to-planning-interface.md`: return valid when triggered by "findings that change what planning should do next"

---

### Approval flow contradictions

**Finding C-9: `project-v-to-v-forge-handoff-interface.md` defers the full approval model to governance docs, but `v-forge\reporting-and-approval-model.md` provides a concrete approval class mapping that omits handoff activation from Class B**

`project-v-to-v-forge-handoff-interface.md` Human-In-The-Loop Principle: "The governance and approval model for handoff authorization is defined in `../governance/approval-and-escalation-model.md`." No approval class is specified in the handoff interface itself.

`v-forge\reporting-and-approval-model.md` Class B definition does not include handoff activation as a V Forge Class B event, even though it is a Class B event in the governance model and even though V Forge receives the handoff and must validate it. A V Forge implementer using only V Forge docs would not know that handoff activation requires Class B approval posture on the Project V side, since V Forge's own approval model omits it.

The seam gap is asymmetric: the handoff interface defers to governance for the approval model, but V Forge's local approval mapping does not include handoff-receipt confirmation as a relevant approval event class from V Forge's perspective.

Docs involved:
- `interfaces\project-v-to-v-forge-handoff-interface.md`: defers to governance model for approval class
- `v-forge\reporting-and-approval-model.md`: Class B examples omit handoff activation entirely
- `governance\approval-and-escalation-model.md` (Tier 1): Class B includes "preparing or activating a handoff"

**Finding C-10: Both interface docs (handoff and return-to-planning) defer human approval mechanics to governance docs, but neither system doc fills the gap at the seam level**

`project-v-to-v-forge-handoff-interface.md` Human-In-The-Loop Principle: "The governance and approval model for handoff authorization is defined in `../governance/approval-and-escalation-model.md`."

`v-forge-to-project-v-return-to-planning-interface.md` Human-In-The-Loop Principle: "All return-to-planning transitions that affect planning direction should be reviewed by a human before planning reconsideration results in new ecosystem actions. The governance and approval model for these decisions is defined in `../governance/approval-and-escalation-model.md`."

Both seam interface docs defer human approval mechanics entirely to the governance model. The governance model (loaded in Session A) defines approval principles and classes but does not specify which system initiates the approval request or how the result re-enters the handoff or return workflow. This deferral pattern is consistent with the Pass 4 finding that human approval mechanics are systematically underspecified. The seam-specific finding here is that neither the handoff nor the return interface doc assigns initiation responsibility (Project V, V Forge, or human operator) for the approval request at the seam, and neither system's own docs fill that gap.

Docs involved:
- `interfaces\project-v-to-v-forge-handoff-interface.md`: defers handoff approval to governance model
- `interfaces\v-forge-to-project-v-return-to-planning-interface.md`: defers return approval to governance model
- Neither assigns approval initiation responsibility at the seam level

---

### Direct contradictions

**Finding C-11: `cross-system-access-governance.md` mislabels "Project V → V Forge (Execution Results)" when the described behavior and governing interface are both V Forge → Project V**

Fully described in Finding C-3. This is a direct error: the access pair direction label ("Project V → V Forge") is inverted relative to the described behavior (Project V reads V Forge results, which is data flowing V Forge → Project V) and the named governing interface (`v-forge-to-project-v-return-to-planning-interface.md`).

Docs involved:
- `ecosystem\cross-system-access-governance.md`: access pair "Project V → V Forge (Execution Results)" governed by `v-forge-to-project-v-return-to-planning-interface.md`
- `interfaces\v-forge-to-project-v-return-to-planning-interface.md`: governs V Forge → Project V

**Finding C-12: `interfaces\data-boundaries.md` lists four governing interfaces as the complete set for cross-system data exchange, but multiple additional paths are referenced in other docs without interface coverage**

`interfaces\data-boundaries.md` Interface-Enforcement Principle: "Cross-system data exchange must happen through the governed interfaces: [four named interfaces]." These are presented as the complete set.

However, the following additional cross-system exchange paths are referenced in other docs without interface coverage:
- Project V → V Forge mid-execution scope clarification (referenced in `project-v\v-forge-integration.md`)
- Project V operator-directed handoff recall (referenced in `project-v\v-forge-integration.md`)
- Project V → V Forge post-replanning scope change notification (referenced in `maintenance-and-replanning-workflow.md`)
- Project V → VEDA evidence request (referenced in `project-intake-workflow.md` — established in Session A)

The data-boundaries doc presents the four-interface list as exhaustive. The other docs create paths outside that list. This is a direct contradiction: the data-boundaries doc forbids cross-system data exchange outside the named interfaces, while other docs reference exchange paths that are not in that list.

Docs involved:
- `interfaces\data-boundaries.md`: "Cross-system data exchange must happen through the governed interfaces" — four interfaces listed as complete set
- `project-v\v-forge-integration.md`: "that coordination must still occur through the governed interface path" — unnamed interface
- `workflows\maintenance-and-replanning-workflow.md`: "informed of any scope or constraint changes through the governed interface" — unnamed interface
- `workflows\project-intake-workflow.md`: "request additional bounded evidence" through "the correct path" — no interface exists

---

### Summary

The Project V ↔ V Forge seam has the cleanest ownership doctrine in the audit: both system docs, both interface docs, and both comparison docs (`vs-project-v.md`, `v-forge-integration.md`) agree precisely on the planning truth / execution truth split and the boundary discipline rules around handoff and return-to-planning. There are no role boundary violations between these two systems.

The structural gaps follow two patterns. First, the `cross-system-access-governance.md` contains two errors specific to this pair: it suppresses the Project V handoff initiation event as a governed access event, and it mislabels the "Project V → V Forge (Execution Results)" pair with an inverted direction and an incorrect governing interface. Second, three cross-system exchange paths referenced in the V Forge integration doctrine and maintenance-and-replanning workflow have no governing interface docs — mid-execution scope clarification, operator-directed handoff recall, and post-replanning scope change notification. These paths are stated to use "the governed interface path" but no such interface exists, directly contradicting `interfaces\data-boundaries.md`'s claim that the four named interfaces are the complete set.

The approval flow is consistently deferred to governance docs at both seam interface points, leaving initiation responsibility unassigned at the seam level — consistent with the systemic pattern identified across all Pass 4 and Pass 5 sessions.

---

### Out-of-scope observations not included in findings
Session C confirms the cross-system-access-governance.md error pattern (direction labeling errors, "Not Applicable" misclassifications) is present for all three system pairs. This doc requires comprehensive correction as a single unit, not pair-by-pair. Flagged for the Pass 5 rollup.
