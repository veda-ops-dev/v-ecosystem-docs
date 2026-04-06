# Pass 3 Findings — Interface Completeness

Doc audited: `mcp-coordination-model.md`
Date: 2026-04-05

---

### Files loaded

- `C:\dev\v-ecosystem-docs\interfaces\mcp-coordination-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\activity-trail-model.md`
- `C:\dev\v-ecosystem-docs\ecosystem\cross-system-boundaries.md`
- `C:\dev\v-ecosystem-docs\governance\auth-and-actor-model.md` (referenced in Related Docs)
- `C:\dev\v-ecosystem-docs\governance\testing-and-verification-doctrine.md` (referenced in Related Docs)

### Files excluded

None found.

---

### Checklist results

**QM-1: PASS** — The MCP call chain is explicitly defined: "LLM declares intent → MCP tool (thin wrapper — transport only) → API call (enforcement layer — business rules, scope, ownership) → Database (never accessed directly by MCP tools)." Session initialization direction is also specified: the desktop application calls the MCP server's session initialization endpoint, and the MCP server returns an opaque session token. Both the call direction and the participants are clear.

**QM-2: PARTIAL** — Session initialization input is specified: the MCP server must "accept the project UUID from the desktop application." Individual MCP tool call parameters are explicitly out of scope: "the specific list of MCP tools for each system" is listed in the Out of Scope section. Rule 2 establishes that tools must not accept project ID from the LLM and that session token is passed as a header, but per-tool input parameter definitions are not provided here.

**QM-3: PARTIAL** — Session initialization response is defined: "return an opaque session token" with stated properties (opaque, bound to exactly one project, revocable, expiring per session expiration policy). General tool response requirements exist via Rule 6: "Tool responses must use stable field names, clear ordering, and explicit nullability." However, no specific field definitions for any tool response are provided, and the error response for an invalid/expired token — "reject the tool call with a governed error response" — has no defined structure.

**QM-4: FAIL** — Pagination and result limits are not addressed. Specific tool schemas, which would contain result limit or pagination parameters, are explicitly out of scope per the doc.

**QM-5: FAIL** — No filter options are documented. The doc distinguishes project-scoped from global tools as an architectural distinction, but no callable filter parameters are defined. Specific tool schemas are out of scope.

**FR-1: FAIL** — No freshness contract is defined. The session token has an expiration policy, but the doc explicitly defers the duration: "The session expiration policy is an implementation decision. This doc does not specify a duration." No freshness requirement exists for data returned through MCP tool calls.

**FR-2: FAIL** — No staleness threshold is defined. Same basis as FR-1.

**FR-3: FAIL** — No timestamp field is specified for session tokens, tool responses, or any other output from this coordination layer.

**AL-1: FAIL** — Activity trail logging is not specified for MCP operations. The doc states that the API is responsible for "emitting canonical event log entries where required," delegating logging to the backend API layer. The doc does not specify whether session initialization, session token issuance, or MCP tool call routing themselves produce activity trail records. The activity-trail-model.md requires records for cross-system access — which MCP tool calls enable — but this interface doc does not address that requirement.

**AL-2: FAIL** — No dot-namespaced action field value is specified for any MCP operation. The activity-trail-model.md defines applicable action types (e.g., `evidence.query`, `signal.query`, `handoff.create`) but this doc does not reference or assign any of them to MCP operations.

**AL-3: FAIL** — No activity record fields are mentioned in the doc. Actor, target, cost, entity_type, entity_id, and all other canonical activity record fields are absent.

**DG-1: PARTIAL** — The "What happens when a session token is invalid or expired" section defines behavior for that specific degraded case: the MCP server must reject with a governed error response, not silently proceed, not fall back to a default project, and must surface the error for re-initialization. However, MCP server unavailability and backend API unavailability are not addressed as degraded cases.

**DG-2: PARTIAL** — For the invalid/expired token case, caller behavior (the desktop application) is specified: reinitialize the session. No caller behavior is defined for MCP server unavailability or backend API failure scenarios.

**DG-3: PARTIAL** — Recovery path for the invalid/expired token degraded case is specified: session re-initialization ("the desktop application or operator can reinitialize the session"). No recovery path is defined for other failure modes such as MCP server downtime or backend API unavailability.

**CA-1: FAIL** — The doc does not state whether MCP session initialization or tool call routing incurs token cost or API cost. Cost accounting is not addressed in this coordination model.

**CA-2: FAIL** — No cost model described.

**CA-3: FAIL** — No reference to budget enforcement for MCP operations.

**SR-1: PARTIAL** — The session initialization response is partially specified: "return an opaque session token" with properties that it must be opaque, bound to exactly one project, revocable, and expiring. Rule 6 establishes general requirements for tool responses ("stable field names, clear ordering, and explicit nullability"), but no actual field definitions for any tool response or error response are provided.

**SR-2: FAIL** — No concrete response structure is defined that would support parsing code. Session initialization returns an opaque token with no internal field structure. Tool response schemas are explicitly out of scope. The error response for an invalid session token is called "a governed error response" with no defined fields.

**AP-1: PASS** — The access model is explicitly governed: "The human operator selects the active project in the desktop application," which initializes the session. MCP tool invocation requires a valid session token, which can only be issued after human project selection. Write tools that require human approval must "surface the recommendation for review rather than executing immediately" — the tool is not the approval.

**AP-2: PASS** — Multiple governance gates are referenced and specified: session token as the structural access gate, human-only project selection (six contamination-prevention layers enumerated), write tool approval posture via the Propose → Review → Apply model, hammer verification as an enforcement expectation, and references to `auth-and-actor-model.md`, `external-action-governance.md`, and `testing-and-verification-doctrine.md` in Related Docs.

---

### Score

**3 of 21 PASS — 6 PARTIAL — 12 FAIL**

---

### Critical gaps (FAIL items only)

**QM-4, QM-5 — No result limits or filter options.** These are explicitly deferred to per-tool schemas which are out of scope for this coordination model. Risk: individual MCP tool implementations will define limits and filters inconsistently without a baseline contract at the coordination layer.

**FR-1, FR-2, FR-3 — No freshness contract or timestamps.** The session token expiration duration is explicitly deferred as an implementation decision. No freshness requirements exist for data returned through any MCP operation. Risk: the coordination layer imposes no freshness floor, leaving each tool implementation to make independent decisions.

**AL-1, AL-2, AL-3 — Activity trail logging not addressed.** The doc delegates event logging to the backend API layer but does not specify whether session creation, token issuance, or tool call routing produce activity trail records at the coordination layer. The activity-trail-model.md requires records for all cross-system access, which MCP tool calls enable. Risk: session-layer operations (initialization, token expiry, rejection) will not appear in the activity trail, and the coordination layer has no stated logging contract.

**CA-1, CA-2, CA-3 — No cost accounting.** MCP tool routing and session management impose no stated cost accounting at this layer. Risk: cost attribution for operations routed through MCP cannot be tracked at the coordination layer; each tool must independently address cost without a shared model.

**SR-2 — No parseable structure.** No tool response schema or error response structure is defined. The "governed error response" for an invalid session token has no field specification. Risk: error handling implementations will diverge across systems without a shared error shape contract.

---

### Summary

`mcp-coordination-model.md` is a coordination governance and architecture doctrine doc, not a data-exchange interface in the same sense as the other audited docs. It earns 3 PASSes for the explicitly defined call chain, the human-gated access model, and the governance references — and 6 PARTIALs for the session initialization contract and partial invalid-token degraded mode coverage. The 12 FAILs largely reflect the doc's intentional scope: specific tool schemas, result limits, filter options, freshness contracts, and response structures are all explicitly deferred to per-tool or per-system docs. The most significant structural gap is activity trail logging — the doc delegates logging to the API layer without specifying what coordination-layer events (session creation, token expiry, rejection) must themselves be recorded.

---

### Out-of-scope observations not included in findings

- The "governed error response" for an invalid/expired session token is referenced but never defined in any loaded doc. This is a concrete error contract gap across the coordination layer.
- The doc explicitly states `../veda/mcp-surface.md` is `*(planned)*` — meaning the VEDA-specific MCP tool surface, which would carry per-tool parameter and response definitions, does not yet exist as of this audit.
