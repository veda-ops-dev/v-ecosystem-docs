## Pass 5 Findings — Cross-System Consistency

Session: B
Systems audited: V Forge ↔ VEDA
Date: 2025-04-05

### Files loaded
- `C:\dev\v-ecosystem-docs\audit\pass-5\pass-5-cross-system-consistency.md`
- `C:\dev\v-ecosystem-docs\v-forge\v-forge.md`
- `C:\dev\v-ecosystem-docs\v-forge\vs-veda.md`
- `C:\dev\v-ecosystem-docs\v-forge\data-boundaries.md`
- `C:\dev\v-ecosystem-docs\v-forge\system-invariants.md`
- `C:\dev\v-ecosystem-docs\v-forge\execution-intelligence-operations.md`
- `C:\dev\v-ecosystem-docs\veda\veda.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\veda\system-invariants.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\veda\data-boundaries.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\veda\observability-and-signal-role.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\interfaces\veda-to-v-forge-signal-interface.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\interfaces\v-forge-evidence-access-contract.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md` (loaded prior session)
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-access-governance.md` (loaded prior session)

### Files excluded
- `C:\dev\v-ecosystem-docs\v-forge\operational-model.md` — internal V Forge operational workflow; not needed to judge seam consistency
- `C:\dev\v-ecosystem-docs\v-forge\content-graph-operations.md` — internal content graph operations; not needed for seam consistency
- `C:\dev\v-ecosystem-docs\v-forge\reporting-and-approval-model.md` — V Forge reporting internals; not needed for seam consistency
- `C:\dev\v-ecosystem-docs\v-forge\human-in-the-loop-doctrine.md` — internal V Forge governance; not needed for seam consistency
- `C:\dev\v-ecosystem-docs\veda\evidence-and-source-provenance.md` — VEDA internal provenance; not needed for seam consistency

---

### Interface coverage gaps

**Expected interactions for V Forge ↔ VEDA:**

1. VEDA → V Forge: signal consumption for execution intelligence
   - Status: EXISTS — `veda-to-v-forge-signal-interface.md`
   - Caller behavior (V Forge consuming): defined
   - Responder behavior (VEDA providing): defined
   - Both system docs agree on direction: PASS

2. V Forge → VEDA: active evidence queries during execution
   - Status: EXISTS — `v-forge-evidence-access-contract.md`
   - Query types, scoping, freshness, attribution, logging: defined
   - VEDA system docs: silent on whether VEDA acknowledges the active query model as a governed access path
   - **One-sided interface assumption (see Finding B-1 below)**

3. VEDA → V Forge: no reverse query (VEDA does not query V Forge)
   - `cross-system-access-governance.md`: "VEDA → V Forge (Not Applicable). VEDA observes through external provider APIs, not through V Forge's internal systems."
   - VEDA docs: consistent — VEDA observes external reality, not V Forge internals.
   - Status: PASS (non-interaction correctly agreed on both sides)

4. V Forge → VEDA: signal expansion requests (V Forge directing VEDA to expand observatory scope)
   - `vs-veda.md` states: "If V Forge needs signal that VEDA is not currently providing, the correct path is to direct VEDA to expand its observatory scope through the governed operator surface, not for V Forge to build its own observatory capability."
   - Status: **MISSING** — no interface doc governs how V Forge requests VEDA observatory scope expansion. The "governed operator surface" path is referenced but undefined.

---

### Access rule mismatches

**Finding B-1: `v-forge-evidence-access-contract.md` defines active query types against VEDA evidence, but `veda-to-v-forge-signal-interface.md` describes a bounded passive signal consumption model — the two interface docs represent different access architectures without reconciliation**

`veda-to-v-forge-signal-interface.md` describes VEDA as the provider of "bounded signal packages" through a "bounded, largely passive channel." It defines signal classes V Forge may consume and states V Forge accesses signal through "MCP tool call → VEDA API endpoint → VEDA database → Response returned."

`v-forge-evidence-access-contract.md` explicitly acknowledges this is insufficient and defines a fundamentally different model: V Forge agents may actively issue structured queries (`evidence_by_project`, `evidence_by_topic`, `signal_status`, `evidence_by_id`) with required parameters, freshness windows, max_results caps, and explicit logging obligations. The contract's own rationale section states the passive model "starves V Forge agents of the evidence they need."

Neither interface doc acknowledges the other as the authoritative model, and the relationship section in the evidence access contract states only that it "extends" the signal interface without explaining which architectural model takes precedence when they differ. This is a one-sided interface design: V Forge's access contract governs behavior that VEDA's own signal interface doc does not acknowledge or define as a governed path on VEDA's side.

Docs involved:
- `interfaces\veda-to-v-forge-signal-interface.md`: "bounded, largely passive channel"; MCP tool → VEDA API access model
- `interfaces\v-forge-evidence-access-contract.md`: "V Forge agents may actively query VEDA evidence during execution"; four defined query types; "extends the existing interface"

**Finding B-2: `cross-system-access-governance.md` governs V Forge → VEDA under the signal interface only; the evidence access contract's query types are not reflected in the governance doc**

`cross-system-access-governance.md` describes "V Forge → VEDA (Evidence Access)" as governed by `v-forge-evidence-access-contract.md`, which appears to acknowledge the contract. However, the access pair description states "Read-only, project-scoped, execution-time queries" governed by the contract — but the general access requirements in the same doc require that "every cross-system data access must produce an activity log entry" using the ecosystem activity trail format. The evidence access contract defines its own per-query logging schema (actor, action, query_type, project_id, parameters, result_count, token_cost, timestamp) which differs in field names and structure from the activity trail's required fields (activity_id, timestamp, actor_type, actor_id, actor_system, action, action_class, entity_type, entity_id, target_system, project_id, details, result_summary).

The two logging schemas are parallel but not reconciled. The evidence access contract's log is not explicitly mapped to the ecosystem activity trail format, and neither doc acknowledges whether the contract's per-query log satisfies or supplements the ecosystem trail requirement.

Docs involved:
- `interfaces\v-forge-evidence-access-contract.md`: defines its own 8-field logging schema per query
- `ecosystem\activity-trail-model.md`: requires specific required fields on every activity record including `activity_id`, `actor_type`, `actor_system`, `action_class`, `entity_type`, `entity_id`, `target_system`
- `ecosystem\cross-system-access-governance.md`: lists V Forge → VEDA as governed by evidence access contract but states the general logging requirement applies to all cross-system access

**Finding B-3: `veda-to-v-forge-signal-interface.md` lists VEDA's internal event log as explicitly unavailable to V Forge; `v-forge-evidence-access-contract.md` defines `evidence_by_project` that may implicitly reach observatory event records**

`veda-to-v-forge-signal-interface.md`: "VEDA's internal event log — event logs are VEDA's own audit trail for observatory state changes, not a signal package for consumption by V Forge."

`v-forge-evidence-access-contract.md` defines `evidence_by_project` as returning "evidence records associated with a specific project" filterable by `evidence_class`. The contract lists `evidence_class` examples including `search_performance`, `competitor_analysis`, `market_signal`, `source_capture`. It does not explicitly exclude observatory event records from the returnable set. The enforcement mechanism (VEDA API scoping) is referenced but not specified within either the signal interface doc or the contract — there is no explicit statement in the evidence access contract that observatory event records are excluded from `evidence_by_project` responses.

This creates an implicit gap: the signal interface explicitly excludes event logs, but the evidence access contract does not carry that exclusion forward into its query specification.

Docs involved:
- `interfaces\veda-to-v-forge-signal-interface.md`: "VEDA's internal event log... not a signal package for consumption by V Forge"
- `interfaces\v-forge-evidence-access-contract.md`: `evidence_by_project` query type with `evidence_class` filter — does not enumerate excluded evidence classes

---

### Activity / traceability mismatches

**Finding B-4: Activity trail action vocabulary has no action type for V Forge active evidence queries**

`ecosystem\activity-trail-model.md` defines cross-system access actions as: `evidence.query` (V Forge querying VEDA evidence), `signal.query` (Project V querying VEDA signal), `execution.query` (Project V reading V Forge execution results).

`evidence.query` appears to cover the V Forge → VEDA evidence access pattern. However, `v-forge-evidence-access-contract.md` defines four distinct query types: `evidence_by_project`, `evidence_by_topic`, `signal_status`, `evidence_by_id`. The activity trail uses a single undifferentiated `evidence.query` action type for all four. The contract also defines a per-query logging field `query_type` to distinguish them, but this field has no counterpart in the activity trail's `action` vocabulary. The trail cannot distinguish between a `signal_status` health check query and an `evidence_by_project` bulk retrieval in its action vocabulary.

Docs involved:
- `ecosystem\activity-trail-model.md`: `evidence.query` — single action type for all V Forge → VEDA evidence access
- `interfaces\v-forge-evidence-access-contract.md`: four distinct query types with different scopes and cost profiles

**Finding B-5: Responsibility for producing the activity trail record for V Forge → VEDA evidence queries is ambiguous**

The activity trail model states "Any query from one system to another system's data must produce an activity record" but does not specify which system produces it. The evidence access contract states V Forge must log each query (with its own 8-field schema), implying V Forge produces the log. But the access governance doc states "The target system enforces scoping" and the cross-system access governance generally places logging responsibility on the requesting system. No doc explicitly assigns the activity trail record production obligation to V Forge vs VEDA for this interaction. If VEDA also logs the inbound query (which would be consistent with VEDA's own event auditability invariant), there would be two parallel records for the same event with no stated reconciliation policy.

Docs involved:
- `ecosystem\activity-trail-model.md`: logging obligation stated but actor not specified per query type
- `interfaces\v-forge-evidence-access-contract.md`: V Forge-side logging obligation defined implicitly by "V Forge must log every evidence query"
- `veda\system-invariants.md` Invariant 11: "Where observatory state changes require durable auditability, VEDA must preserve canonical event history" — a V Forge query is not a VEDA state change, but VEDA inbound access logging is not explicitly excluded

---

### Role boundary violations

**Finding B-6: `v-forge\data-boundaries.md` describes `NewsletterIssue` aggregate open and click rates as "execution feedback" owned by V Forge; VEDA docs describe engagement performance metrics as observatory truth**

`v-forge\data-boundaries.md`: "The aggregate open and click rates on `NewsletterIssue` are treated as bounded execution feedback — summary metrics returned by the send operation itself as part of V Forge's own publication action — not as open-ended external monitoring." This framing is used to justify V Forge owning these metrics rather than VEDA.

`veda\veda.md` Owns section: "Google Analytics 4 performance observations" and "source capture and source item ingestion" are VEDA-owned observatory truth. Newsletter engagement rates (open rates, click rates) are a class of performance observation. VEDA's docs do not explicitly address newsletter metrics, but the pattern — external platform reporting aggregate performance metrics about content V Forge published — is structurally identical to GA4 performance observations that VEDA owns.

`cross-system-boundaries.md` VEDA Owns: "observability truth — SERP data, keyword intelligence, search performance, GA4." The boundary between "execution feedback on a V Forge-initiated action" and "external performance observation" is asserted by V Forge's own data-boundaries doc but is not validated against VEDA's ownership model. No seam doc adjudicates this specific case.

This is not a direct contradiction (VEDA docs do not mention newsletter metrics), but it is a one-sided ownership assertion at the edge of V Forge's data boundary without acknowledgment from VEDA's side.

Docs involved:
- `v-forge\data-boundaries.md`: newsletter open/click rates framed as execution feedback owned by V Forge
- `veda\veda.md`: owns GA4 performance observations and "observability truth" broadly
- `ecosystem\cross-system-boundaries.md`: VEDA owns observability truth; does not adjudicate newsletter metrics

**Finding B-7: `v-forge\execution-intelligence-operations.md` describes execution intelligence operations that include interpreting "how a built asset or asset group appears to be performing" — this is the same class of analysis VEDA's docs explicitly exclude from VEDA but do not confirm as V Forge territory**

This is a role assignment question, not a contradiction. Both VEDA's and V Forge's docs agree: "VEDA does not assess how well built content is performing" (`vs-veda.md`) and execution intelligence belongs to V Forge (`v-forge.md`). The seam is consistent on this point.

Status: PASS — no role boundary violation.

---

### Approval flow contradictions

**Finding B-8: `v-forge-evidence-access-contract.md` states "V Forge does not need human approval to query evidence" — but VEDA's Human-In-The-Loop Principle implies human review when signal consumption leads to significant execution change recommendations**

`v-forge-evidence-access-contract.md`: "V Forge does not need human approval to query evidence. It does need a record that the query happened."

`veda-to-v-forge-signal-interface.md` Human-In-The-Loop Principle: "Human review remains important when: execution intelligence based on consumed signal leads to a significant execution change recommendation... signal indicates a material external change that may require planning reconsideration."

These statements are not directly contradictory (one governs the query, one governs the use of results), but they are not aligned in a way that an implementer would find unambiguous. The evidence access contract does not acknowledge that the downstream use of evidence — not the query itself — may trigger human review obligations described in the signal interface doc. The two docs govern adjacent events (query vs. use) without connecting them.

Docs involved:
- `interfaces\v-forge-evidence-access-contract.md`: "V Forge does not need human approval to query evidence"
- `interfaces\veda-to-v-forge-signal-interface.md`: Human-In-The-Loop Principle listing conditions where review is required downstream of signal consumption

**Finding B-9: `v-forge\vs-veda.md` references "the VEDA Brain prohibition (ADR-003)" but no ADR-003 document is present in the accessible doc set**

`v-forge\vs-veda.md`: "The VEDA Brain prohibition (ADR-003) specifically governs the second category." This is a direct reference to a governance decision record that is not present in the loaded doc set. The `veda\system-invariants.md` Invariant 6 also states "VEDA Brain Does Not Exist" but does not reference ADR-003 by name.

This is not an approval flow contradiction per se, but it is an unresolvable reference at the seam: the V Forge doc appeals to a governance authority that is either inaccessible or does not exist in the current doc set. If ADR-003 has been superseded or relocated, the reference in vs-veda.md is a dangling authority citation.

Docs involved:
- `v-forge\vs-veda.md`: "The VEDA Brain prohibition (ADR-003)"
- ADR-003: not found in the doc set

---

### Direct contradictions

**Finding B-10: `cross-system-access-governance.md` declares "VEDA → V Forge (Not Applicable)" — the same error found in Session A**

As established in Session A Finding A-12 for the VEDA → Project V direction, the access governance doc's assertion that VEDA → V Forge is "Not Applicable" is in direct tension with `veda-to-v-forge-signal-interface.md`, which governs exactly the VEDA → V Forge signal delivery path as a primary ecosystem interaction.

`cross-system-access-governance.md`: "VEDA → V Forge (Not Applicable). VEDA observes external reality, not internal execution state. If VEDA needs to observe the effect of executed work (e.g., monitoring a published page's search performance), it observes through external provider APIs, not through V Forge's internal systems."

The rationale given (VEDA does not read V Forge internals) is correct, but the conclusion (the interaction is Not Applicable) is wrong — VEDA → V Forge signal delivery is a primary governed interaction, not an inapplicable one. The access governance doc conflates "VEDA does not query V Forge" (correct) with "VEDA does not interact with V Forge" (incorrect).

This contradiction is confirmed by both `veda-to-v-forge-signal-interface.md` (which defines VEDA providing signal to V Forge) and `v-forge.md` (which defines V Forge consuming bounded observatory signal from VEDA as a primary ecosystem relationship).

Docs involved:
- `ecosystem\cross-system-access-governance.md`: "VEDA → V Forge (Not Applicable)"
- `interfaces\veda-to-v-forge-signal-interface.md`: entire doc governs VEDA → V Forge signal delivery
- `v-forge\v-forge.md`: "V Forge consumes bounded observatory signal from VEDA through the governed signal interface"

**Finding B-11: `veda-to-v-forge-signal-interface.md` and `v-forge-evidence-access-contract.md` give inconsistent accounts of whether the V Forge → VEDA interaction is governed by MCP tool call or by direct query**

`veda-to-v-forge-signal-interface.md` Access Model: "V Forge execution intelligence layer → MCP tool call (project-scoped session token) → VEDA API endpoint → VEDA database → Response returned to V Forge."

`v-forge-evidence-access-contract.md` defines query types as API-level interactions with structured parameters (`project_id`, `freshness_window`, `evidence_class`, `max_results`, `sort`). MCP tool calls are not mentioned in the evidence access contract. The contract's related docs include `mcp-coordination-model.md` but the contract body describes API query types, not MCP tools.

The two docs cannot both be fully authoritative on how V Forge accesses VEDA. One describes MCP-mediated access; the other describes direct API query types with no mention of MCP mediation. This is a direct implementation-level contradiction at the transport layer of the seam.

Docs involved:
- `interfaces\veda-to-v-forge-signal-interface.md`: access occurs via MCP tool call
- `interfaces\v-forge-evidence-access-contract.md`: access defined as direct API query types; MCP not mentioned in contract body

---

### Summary

The V Forge ↔ VEDA seam is doctrinally consistent on its core ownership split: VEDA owns observatory truth, V Forge owns execution truth and the content graph, and execution intelligence is a V Forge product derived from VEDA signal. Both system docs, their invariants, and the `vs-veda.md` comparison doc all agree on this. The role boundary is the cleanest seam in the audit so far.

The three substantive structural gaps are: (1) The evidence access contract and the signal interface represent two architecturally distinct access models (active query vs. passive bounded signal) that coexist without reconciliation — neither explicitly supersedes the other, creating an implementation ambiguity for VEDA's API design; (2) `cross-system-access-governance.md` repeats the Session A error of declaring VEDA → V Forge "Not Applicable" when the signal interface governs exactly that interaction as a primary path; (3) the two interface docs describe different transport mechanisms (MCP tool call vs. direct API query) for the same V Forge → VEDA access path.

Additionally, the evidence access contract introduces a per-query logging schema that does not map cleanly to the ecosystem activity trail's required field set, creating a traceability gap, and the missing "V Forge requests VEDA scope expansion" path leaves V Forge's observatory direction channel undefined at the interface level.

---

### Out-of-scope observations not included in findings
`v-forge\vs-veda.md` references "ADR-003" for the VEDA Brain prohibition, but no ADR-003 is present in the accessible doc set. This may indicate a missing governance decision record rather than a cross-system consistency issue per se. Flagged for human review.
