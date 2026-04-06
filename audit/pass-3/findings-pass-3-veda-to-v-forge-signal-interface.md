# Pass 3 Findings — Interface Completeness

Doc audited: `veda-to-v-forge-signal-interface.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\veda-to-v-forge-signal-interface.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\interfaces\mcp-coordination-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\governance\testing-and-verification-doctrine.md` (referenced in Related Docs)

### Files excluded

None found.

---

### Checklist results

**QM-1: PASS** — The access model is explicitly defined with a call chain: "V Forge execution intelligence layer → MCP tool call (project-scoped session token) → VEDA API endpoint (enforces project scope, ownership, and read-only posture) → VEDA database → Response returned to V Forge." Caller (V Forge), answerer (VEDA API), direction, and read-only posture are all specified.

**QM-2: FAIL** — Four signal classes are enumerated (Search Performance Signal, Owned Performance Signal, Search Intelligence Signal, Observatory Context), but no actual input parameters are defined — no field names, types, or valid values for a signal query. The Out of Scope section explicitly excludes "the detailed MCP tool list for this interface," confirming parameter definition is intentionally deferred.

**QM-3: FAIL** — No response structure is defined. Signal classes list descriptive content ("SERP position and ranking data," "impressions, clicks, CTR") in prose but no typed schema fields or response object shape. The Out of Scope section confirms this is deferred.

**QM-4: FAIL** — Pagination, result limits, and maximum response size are not addressed anywhere in the doc.

**QM-5: FAIL** — The doc documents what signal classes are available and what is not available through this interface, but there are no caller-controllable filter options. The class listing reflects what VEDA makes available, not parameters V Forge can pass to select a subset.

**FR-1: PARTIAL** — The "Signal Freshness and Trust" section establishes that "signal consumed from VEDA should be treated according to VEDA's trust classification for that signal class" and that V Forge must "respect the trust posture established for each signal class." This is a principle requiring V Forge to honor VEDA's freshness posture, but no specific freshness window, currency requirement, or contract is defined in the interface doc.

**FR-2: FAIL** — "Stale" appears in the Failure Behavior section ("If VEDA signal is unavailable, stale, or returns an error") but staleness is not defined. No threshold for when signal becomes too old to use is specified.

**FR-3: FAIL** — No timestamp field is specified in the response structure. The "Returning Signal-Informed Findings to Project V" section notes that "V Forge should note that the finding is based on VEDA signal consumed at a specific time," implying timestamps matter, but no `last_updated` or equivalent field is defined in any response specification.

**AL-1: FAIL** — The doc contains no mention of activity trail records, activity logging, or any logging requirement. The activity-trail-model.md requires an activity record for "any query from one system to another system's data" and defines action vocabulary that would apply to this interface (the closest match is `evidence.query — V Forge querying VEDA evidence`, though a `signal.query` action type for V Forge → VEDA is not separately listed). The interface doc makes no reference to this requirement.

**AL-2: FAIL** — No action field value is specified in the interface doc. The activity-trail-model.md defines `evidence.query` for V Forge querying VEDA, but the interface doc does not reference this or specify any dot-namespaced action type.

**AL-3: FAIL** — The interface doc contains no reference to actor, target, entity_type, entity_id, cost fields, or any other activity record field. Activity record requirements are completely absent.

**DG-1: PASS** — The "Failure Behavior" section explicitly defines degraded mode: "If VEDA signal is unavailable, stale, or returns an error: V Forge must not fabricate signal to fill the gap; V Forge must preserve the signal gap explicitly in execution intelligence outputs; V Forge must not halt execution entirely unless the missing signal is critical to safe execution within the approved scope; V Forge may include the signal unavailability as a finding returned to Project V if it materially affects execution quality."

**DG-2: PASS** — The same Failure Behavior section specifies V Forge's required behavior during degraded mode across four concrete rules. The caller's behavior is defined.

**DG-3: FAIL** — The Failure Behavior section covers what V Forge does while signal is unavailable but does not define a recovery path — no retry behavior, no re-initialization, no specification of how or when normal signal consumption resumes.

**CA-1: FAIL** — The doc does not state whether signal queries through this interface incur token cost or API cost. Neither the Human-In-The-Loop section nor any other section addresses cost implications for this interface.

**CA-2: FAIL** — No cost model described. Dependent on CA-1, but even if cost exists, no per-call or per-token model is specified.

**CA-3: FAIL** — No reference to budget enforcement for this interface.

**SR-1: FAIL** — Response records are not structured with typed fields. Signal class content is described in prose ("SERP position and ranking data for keyword targets," "impressions, clicks, CTR, position trends") rather than as typed schema fields. No response object or field list is defined.

**SR-2: FAIL** — No structure is defined; parsing code cannot be written against this doc.

**AP-1: PARTIAL** — The Human-In-The-Loop section states: "Signal consumption through this interface is generally read-only and low-governance-sensitivity." This establishes that baseline signal access does not require pre-access approval. However, no explicit approval class (Class A/B/C/D) is assigned to this interface, and the cases where human review is required ("execution intelligence based on consumed signal leads to a significant execution change recommendation") are listed without a citation to the approval-and-escalation-model.md or an assigned class.

**AP-2: PARTIAL** — The doc references `mcp-coordination-model.md` and `testing-and-verification-doctrine.md` in Related Docs, and the Hammer Verification section establishes verification expectations. However, no governance gate classes are assigned, and `approval-and-escalation-model.md` is not referenced.

---

### Score

**3 of 21 PASS — 3 PARTIAL — 15 FAIL**

---

### Critical gaps (FAIL items only)

**QM-2, QM-3, SR-1, SR-2 — No implementation-facing structure defined.** Signal classes are enumerated as prose categories but no fields, types, or response schema exist. An implementer cannot build MCP tools for this interface from this doc alone. Risk: every implementation will diverge because there is no shared specification. (The doc self-declares this out of scope.)

**AL-1, AL-2, AL-3 — Activity trail logging entirely absent.** The activity-trail-model.md requires a governed activity record for every cross-system query. The closest action type in the vocabulary is `evidence.query — V Forge querying VEDA evidence`; a distinct `signal.query` for V Forge → VEDA is not defined, which is itself a gap. The interface doc contains no reference to any logging requirement. Risk: implementations will not produce activity trail records for these signal queries, breaking cross-system auditability.

**FR-2, FR-3 — Staleness and timestamp undefined.** "Stale" is used as a case in the Failure Behavior section but never defined. No timestamp field is specified in the response. Risk: V Forge has no spec for when signal is too old to act on, and no defined way to determine the age of received signal.

**DG-3 — No recovery path.** The degraded behavior is well-specified for while signal is unavailable, but what happens when VEDA becomes available again — retry, re-query, resume — is unspecified. Risk: inconsistent recovery implementations.

**CA-1, CA-2, CA-3 — No cost accounting.** Signal queries through VEDA's API may incur API call costs. Neither cost existence nor model is stated. Risk: cost attribution for this interface cannot be tracked against budget.

**QM-4, QM-5 — No result limits or caller-controlled filters.** No ceiling on response size and no mechanism for V Forge to select signal by type, time window, or other criteria. Risk: unbounded responses and no selectivity.

---

### Summary

`veda-to-v-forge-signal-interface.md` is meaningfully more implementation-oriented than its Project V sibling — it earns three PASS items by clearly defining the access model (call chain, read-only posture) and degraded mode behavior. However, it shares the same structural incompleteness: signal classes are enumerated as doctrine categories without typed fields or response schemas, activity trail logging is entirely absent, and cost accounting, staleness thresholds, and recovery paths are unspecified. The 15 FAIL items represent the same gap as the prior interface doc between a well-reasoned doctrine document and an implementation-complete interface specification.

---

### Out-of-scope observations not included in findings

- The activity-trail-model.md's action vocabulary does not include a distinct action type for V Forge querying VEDA signal (only `evidence.query` for V Forge → VEDA and `signal.query` for Project V → VEDA are defined). This gap in the activity trail model itself is a cross-system consistency issue for a later pass.
- The Hammer Verification section is a genuine differentiator from the prior interface doc and provides useful boundary verification expectations even without full completeness coverage.
