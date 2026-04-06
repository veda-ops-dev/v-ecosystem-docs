## Pass 5 Findings — Cross-System Consistency

Session: A
Systems audited: Project V ↔ VEDA
Date: 2025-04-05

### Files loaded
- `C:\dev\v-ecosystem-docs\audit\pass-5\pass-5-cross-system-consistency.md`
- `C:\dev\v-ecosystem-docs\project-v\project-v.md`
- `C:\dev\v-ecosystem-docs\project-v\system-invariants.md`
- `C:\dev\v-ecosystem-docs\project-v\operational-workflow.md`
- `C:\dev\v-ecosystem-docs\project-v\data-boundaries.md`
- `C:\dev\v-ecosystem-docs\project-v\v-forge-integration.md`
- `C:\dev\v-ecosystem-docs\veda\veda.md`
- `C:\dev\v-ecosystem-docs\veda\system-invariants.md`
- `C:\dev\v-ecosystem-docs\veda\observability-and-signal-role.md`
- `C:\dev\v-ecosystem-docs\veda\data-boundaries.md`
- `C:\dev\v-ecosystem-docs\interfaces\veda-to-project-v-signal-interface.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-access-governance.md`

### Files excluded
- `C:\dev\v-ecosystem-docs\project-v\lifecycle.md` — internal Project V lifecycle; no direct seam relevance for VEDA
- `C:\dev\v-ecosystem-docs\project-v\mcp-surface.md` — MCP surface detail; not needed to judge Project V ↔ VEDA seam
- `C:\dev\v-ecosystem-docs\veda\evidence-and-source-provenance.md` — internal VEDA provenance; not needed to judge cross-system consistency at the seam level
- `C:\dev\v-ecosystem-docs\veda\observatory-models.md` — internal VEDA model; not needed to judge seam consistency
- `C:\dev\v-ecosystem-docs\veda\mcp-surface.md` — MCP surface detail; not needed for seam consistency
- `C:\dev\v-ecosystem-docs\veda\schema-reference.md` — internal schema; not needed for seam consistency
- `C:\dev\v-ecosystem-docs\veda\search-intelligence-layer.md` — internal VEDA layer; not needed for seam consistency

---

### Interface coverage

**Expected interactions for Project V ↔ VEDA:**

1. VEDA → Project V: signal/evidence transfer for planning use
   - Status: EXISTS — `veda-to-project-v-signal-interface.md`
   - Caller behavior (VEDA packaging): defined
   - Responder behavior (Project V interpretation): defined at principle level in interface doc; Project V system-invariants and operational-workflow also cover receipt and interpretation obligations
   - Both system docs agree on direction: PASS

2. Project V → VEDA: request for additional bounded evidence (referenced in project-intake-workflow.md and VEDA signal interface)
   - Status: **MISSING** — no interface doc governs how Project V requests additional evidence from VEDA
   - The `veda-to-project-v-signal-interface.md` states the interface is "unidirectional" and "any path from Project V back to VEDA is a separate interface and is not defined here." The project-intake-workflow.md references "request additional bounded evidence" as a valid intake outcome and that VEDA may later supply more bounded signal "if requested through the correct path." No interface doc for that return request path exists.
   - cross-system-access-governance.md lists "Project V → VEDA" as read-only access governed by the signal interface, but does not acknowledge the request-for-evidence direction as a separate interaction type requiring its own interface.

3. VEDA → Project V: no reverse query direction
   - cross-system-access-governance.md: "VEDA does not query Project V."
   - VEDA docs: consistent — VEDA provides signal but does not read planning state.
   - Status: PASS (non-interaction correctly agreed on both sides)

---

### Access rule consistency

**Finding A-1: Activity trail action type `signal.query` maps to Project V reading VEDA, but access governance describes the direction as VEDA providing signal to Project V**

The activity-trail-model.md defines `signal.query` as: "Project V querying VEDA signal." The cross-system-access-governance.md describes the interaction as "Project V queries VEDA signal and evidence." However, the veda-to-project-v-signal-interface.md consistently describes the interaction as VEDA providing bounded signal to Project V — VEDA packages and delivers, Project V receives. This is not a hard contradiction (query and receive can be compatible), but the two framings create a latent implementation ambiguity: does Project V make active pull queries against VEDA's API, or does VEDA push bounded signal packages to Project V? The interface doc describes what crosses the boundary but not whether it is push or pull. The activity trail assumes a query (pull) model. The interface doc is silent on transport direction.

Docs involved:
- `activity-trail-model.md`: "Project V querying VEDA signal"
- `cross-system-access-governance.md`: "Project V queries VEDA signal and evidence to inform planning decisions"
- `veda-to-project-v-signal-interface.md`: "VEDA provides Project V with planning-relevant signal and evidence outputs" — describes VEDA as provider and Project V as receiver, not as requester

**Finding A-2: Project V data-boundaries.md allows ecosystem-scoped (cross-project) VEDA access; cross-system-access-governance.md limits access to project-scoped only**

`cross-system-access-governance.md` states under "Project V → VEDA": access is "Read-only, project-scoped or ecosystem-scoped for market scanning." This implies cross-project VEDA reads are permitted for Project V in market-scanning contexts.

However, `cross-system-access-governance.md` also states as a general access requirement: "Cross-system queries must carry explicit scope parameters. The minimum scope is project-level. Unscoped queries that return data across all projects are not permitted through cross-system interfaces."

These two statements are in the same document and are in tension: the per-pair entry allows ecosystem-scoped market scanning but the general access requirement says unscoped (cross-project) queries are not permitted. "Ecosystem-scoped" is effectively cross-project. The document does not define what distinguishes permissible "ecosystem-scoped market scanning" from prohibited "unscoped cross-project queries." No resolution is provided.

Docs involved:
- `cross-system-access-governance.md`: "project-scoped or ecosystem-scoped for market scanning" vs. "Unscoped queries that return data across all projects are not permitted"

**Finding A-3: VEDA data-boundaries.md and Project V data-boundaries.md both discuss imported cross-system data but with asymmetric detail**

VEDA's data-boundaries.md includes an "Imported Cross-System Data Rule" that governs what happens when VEDA receives data from other systems — it must remain visibly non-canonical. Project V's data-boundaries.md includes equivalent rules for imported convenience data from VEDA.

However, neither data-boundaries doc clearly addresses the scenario where Project V stores a planning interpretation derived from VEDA signal and that interpretation is later treated as canonical planning truth. Project V's data-boundaries.md states: "The interpretation itself may be canonical Project V truth; the imported source material it was derived from remains non-canonical." VEDA's data-boundaries.md does not address this consumer-side interpretation scenario at all — it governs VEDA's own storage but not how consumers may reclassify VEDA outputs once interpreted.

This is an asymmetry rather than a direct contradiction: VEDA's doc says it is the consumer's problem, but Project V's doc (which is the consumer) permits reclassification of interpretations as Project V canonical truth. No seam doc reconciles whether VEDA should retain any say in how its signal is reclassified once interpreted.

Docs involved:
- `veda\data-boundaries.md`: "If a downstream consumer misclassifies correctly labeled VEDA output, the misclassification is a consumer-side boundary failure governed by the consuming system's own data-boundary rules, not by VEDA's packaging posture."
- `project-v\data-boundaries.md`: "The interpretation itself may be canonical Project V truth; the imported source material it was derived from remains non-canonical."

---

### Activity / traceability mismatches

**Finding A-4: No activity trail action type covers VEDA packaging or signal transfer initiation**

The activity-trail-model.md action vocabulary defines `signal.query` as Project V querying VEDA signal. There is no action type for:
- VEDA packaging a signal for transfer to Project V
- VEDA initiating a signal delivery
- the signal transfer event itself

If the model is push-based (VEDA sends), there is no action type covering the VEDA side of the transfer. If pull-based (Project V queries), `signal.query` covers the Project V side but still nothing covers VEDA's signal-package production event.

VEDA system-invariants.md (Invariant 11) requires event auditability for observatory state changes, but signal packaging for Project V consumption is not listed as a state change requiring an event record. The activity trail model would not capture VEDA's half of the cross-system transfer.

Docs involved:
- `activity-trail-model.md`: action vocabulary lists `signal.query` only; no VEDA-side production action type
- `veda\system-invariants.md` Invariant 11: covers observatory state changes; does not address signal packaging events

**Finding A-5: No activity trail action type covers Project V requesting additional evidence from VEDA**

The "request additional bounded evidence" intake outcome is referenced in project-intake-workflow.md and the veda-to-project-v-signal-interface.md. Neither the activity trail vocabulary nor any interface doc defines what activity record this produces, who produces it (Project V requesting, or the resulting VEDA response), or what action type applies. The interface for this path does not exist (see Interface Coverage Finding), and the activity trail has no action type for it.

Docs involved:
- `workflows\project-intake-workflow.md`: "request additional bounded evidence" as a Stage 5 intake outcome
- `activity-trail-model.md`: no action type for Project V → VEDA evidence request

**Finding A-6: Activity trail ownership is ambiguous for the signal transfer event**

The activity-trail-model.md states "Any query from one system to another system's data must produce an activity record" with Project V reading VEDA signal listed as an example. But the interface doc describes VEDA as the provider of a bounded signal package. If VEDA pushes the package, the activity record should be produced by VEDA (as the acting system). If Project V pulls via a query, Project V produces the record. The activity trail model does not specify which system is responsible for producing the activity record for the signal transfer event. The actor_system field would be different depending on the model.

Docs involved:
- `activity-trail-model.md`: "Project V reading VEDA signal for planning" listed under cross-system access examples; `actor_system` field must be set to the correct system
- `veda-to-project-v-signal-interface.md`: describes VEDA as providing rather than Project V as querying

---

### Role boundary violations

**Finding A-7: VEDA observability-and-signal-role.md describes VEDA producing "escalation-worthy signal" classifications that imply governance action**

`veda\observability-and-signal-role.md` defines "Escalation-Worthy Signal" as a legitimate VEDA signal type: "Signal that, based on its evidence basis and observability characteristics, appears to justify governed attention or explicit review." The doc adds a caveat: "The escalation determination belongs to the governed review process, not to VEDA's classification of the signal."

However, VEDA classifying a signal as "escalation-worthy" is a step beyond purely neutral observation. The telescope mental model (which the same doc uses) would not classify its own observations as "this warrants escalation." Classification of governance-action-worthiness is a mild but real step toward planning judgment. The cross-system-boundaries.md forbids VEDA from making "intelligence synthesis or proposals." The escalation-worthy signal classification is close to a proposal. The caveat mitigates but does not eliminate the tension.

Docs involved:
- `veda\observability-and-signal-role.md`: "Escalation-Worthy Signal" type
- `ecosystem\cross-system-boundaries.md`: "VEDA Brain does not exist in this ecosystem... VEDA must not become the planner, the executor, the content modeler, or the intelligence synthesizer"

**Finding A-8: veda-to-project-v-signal-interface.md permits VEDA to determine "what Project V should consider or reconsider" — a mild planning-adjacent framing**

The interface doc's Minimum Interface Semantics section states a signal transfer should carry "what Project V should consider or reconsider." Telling Project V what it should consider or reconsider is a governance-adjacent framing that edges toward planning direction rather than pure evidence provision. This is inconsistent with veda.md's core rule: "VEDA does not interpret on behalf of the ecosystem" and "VEDA watches and records."

The VEDA docs consistently describe signal as informing Project V rather than directing it. But the interface doc's semantic element ("what Project V should consider or reconsider") frames VEDA as having a view about Project V's planning agenda. This is not consistent with the telescope model.

Docs involved:
- `interfaces\veda-to-project-v-signal-interface.md`: "what Project V should consider or reconsider" listed as a minimum interface semantic element
- `veda\veda.md`: "VEDA does not interpret on behalf of the ecosystem. VEDA does not propose action."
- `veda\observability-and-signal-role.md`: "VEDA supplies the raw material. Other systems do the thinking."

---

### Approval/governance gate consistency

**Finding A-9: Both system docs acknowledge approval may be required for planning actions triggered by VEDA signal, but neither specifies who initiates the approval request**

The veda-to-project-v-signal-interface.md Human-In-The-Loop Principle states: "Human review or approval may be required" for signal-influenced planning decisions. The project-intake-workflow.md's Human-In-The-Loop Principle also states approval may be required for "high-significance intake outcomes."

Neither doc specifies whether VEDA surfaces an approval recommendation, or whether Project V generates the approval request entirely independently after receiving signal. The cross-system-access-governance.md does not address approval initiation for the VEDA → Project V seam. This is a process gap at the seam: the two systems agree approval may be required but neither owns the initiation mechanics.

This is consistent with the Pass 4 finding that human approval mechanics are universally underspecified in workflow docs. The finding here is that the system-level docs at the seam also do not close this gap.

Docs involved:
- `interfaces\veda-to-project-v-signal-interface.md`: Human-In-The-Loop Principle
- `workflows\project-intake-workflow.md`: Human-In-The-Loop Principle
- Neither assigns initiation ownership

**Finding A-10: VEDA data-boundaries.md specifies paid data pull authorization as requiring human review; approval-and-escalation-model.md Class C covers paid external actions — but the seam between VEDA and the approval model is not explicitly mapped**

`veda\veda.md` Human-In-The-Loop Principle lists "establishing or changing paid data pull authorization" as requiring human review. The approval-and-escalation-model.md Class C covers "paid data pulls." However, no doc specifies whether VEDA-initiated paid data pull authorization requests are Class C approvals that Project V is involved in, or whether VEDA handles them autonomously with an operator only. The interface docs are silent on this flow. The seam between VEDA governance and the shared approval model is not explicitly mapped for this action class.

Docs involved:
- `veda\veda.md`: "establishing or changing paid data pull authorization" requires human review
- `governance\approval-and-escalation-model.md`: Class C covers paid data pulls
- No interface or workflow doc maps this to a concrete cross-system approval flow

---

### Direct contradictions

**Finding A-11: veda-to-project-v-signal-interface.md describes the interface as unidirectional, but project-intake-workflow.md assumes a bidirectional request path exists**

`veda-to-project-v-signal-interface.md`: "This interface is unidirectional. It defines what crosses from VEDA into Project V. Any path from Project V back to VEDA is a separate interface and is not defined here."

`project-intake-workflow.md` Stage 6 / Stage 5: "request additional bounded evidence" is a valid intake outcome. Stage 6 states: "if more evidence is needed, the appropriate bounded evidence path is triggered." The workflow assumes this path exists and is usable. The intake workflow's re-entry logic (Stage 2 or Stage 3 after additional evidence returns) structurally depends on the path.

This is a direct contradiction: the signal interface doc says the return path is not defined here, and the intake workflow doc depends on that path being operative. No separate interface doc for Project V → VEDA evidence request exists (confirmed by directory scan). The ecosystem therefore has a workflow that depends on an interface that is explicitly deferred and does not yet exist.

Docs involved:
- `interfaces\veda-to-project-v-signal-interface.md`: "any path from Project V back to VEDA is a separate interface and is not defined here"
- `workflows\project-intake-workflow.md`: "request additional bounded evidence" as operational intake outcome; Stage 6 re-entry depends on this path being functional

**Finding A-12: cross-system-access-governance.md omits VEDA → Project V signal packaging as a governed interaction type**

`cross-system-access-governance.md` defines four access pairs: V Forge → VEDA, V Forge → Project V, Project V → VEDA, Project V → V Forge. The fifth pair entry explicitly states: "VEDA → V Forge (Not Applicable)" and "VEDA → Project V (Not Applicable)."

But VEDA → Project V is not inapplicable — it is the primary described interaction in the entire veda-to-project-v-signal-interface.md and in every VEDA doc. The access governance doc's assertion that "VEDA → Project V (Not Applicable)" directly contradicts the existence and purpose of the veda-to-project-v-signal-interface.md. The governance doc attempts to frame all interactions as pull-based (consuming system queries), which means VEDA providing signal to Project V is not captured as a governed access event at all in this model.

Docs involved:
- `ecosystem\cross-system-access-governance.md`: "VEDA → Project V (Not Applicable). VEDA does not query Project V."
- `interfaces\veda-to-project-v-signal-interface.md`: entire doc describes VEDA → Project V as the primary governed cross-system interaction
- `veda\veda.md`, `veda\observability-and-signal-role.md`: consistently describe VEDA providing signal to Project V

---

### Summary

The Project V ↔ VEDA seam is doctrinally consistent on its core ownership split: VEDA owns observable external reality, Project V owns planning truth, neither absorbs the other's domain. The system-level docs, system-invariants, and data-boundaries docs all agree on this and show no meaningful role-boundary violations between the two systems.

The three substantive gaps are: (1) a missing interface — no doc governs the Project V → VEDA evidence request path that the intake workflow depends on, creating a direct structural dependency on a nonexistent interface; (2) a direct contradiction in cross-system-access-governance.md, which declares VEDA → Project V "Not Applicable" while the entire veda-to-project-v-signal-interface.md governs exactly that interaction, and which creates an internal tension between ecosystem-scoped market scanning access and the general prohibition on cross-project queries; (3) a mild role-boundary tension in the signal interface's use of "what Project V should consider or reconsider" as a minimum semantic element, which edges toward planning direction inconsistently with VEDA's pure-observatory identity.

Recommended resolution priority: (1) the missing Project V → VEDA evidence request interface is the most operationally blocking gap — the intake workflow cannot be implemented without it; (2) the cross-system-access-governance.md VEDA → Project V omission must be corrected since it misrepresents the primary VEDA interaction model; (3) the ecosystem-scoped vs. project-scoped access tension in access-governance.md needs a definition of what qualifies as "market scanning" to resolve the internal conflict.

---

### Out-of-scope observations not included in findings
The `veda\operator-surfaces.md` and `veda\mcp-surface.md` are both marked *(planned)* in the observability-and-signal-role.md Related Docs. These are missing docs that would affect the VEDA surface model. Not a cross-system consistency issue but a structural gap noted for completeness.
