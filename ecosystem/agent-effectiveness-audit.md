# Ecosystem Agent Effectiveness Audit — Findings and Required Improvements

## Purpose

This document identifies systematic gaps across V Ecosystem docs where agent effectiveness is impaired by missing access mechanics, missing activity logging, missing cost governance, missing freshness metadata, and missing structured event contracts.

It exists to answer:

```text
Where do agents currently lack what they need to work effectively, what patterns must be applied consistently across all cross-system interfaces and workflows, and what specific docs need amendment?
```

This is a working document. It drives improvements. It is not itself a doctrine doc.

---

## Audit Method

Every interface, workflow, and governance doc was checked for:

1. **Access mechanics** — does the doc define how agents actually query or access the data it describes, or does it only say access is "bounded" without defining query types, parameters, or response shapes?
2. **Activity logging** — does the doc require that actions and access be logged in the ecosystem activity trail?
3. **Cost/token accounting** — does the doc account for token and API cost of the operations it describes?
4. **Freshness metadata** — when evidence or signal is consumed, does the doc require freshness metadata on responses?
5. **Structured event contracts** — does the doc define structured events for state transitions, or does it rely on prose descriptions of what "should happen"?
6. **Degraded-mode behavior** — does the doc define what happens when data is unavailable, stale, or returns errors?

---

## Finding 1 — Universal: "Bounded" Without Access Mechanics

**Problem:** 31 docs use the word "bounded" to describe cross-system access without defining query types, required parameters, response shapes, or scoping rules. This means an agent reading these docs knows access is *supposed to be* bounded but has no concrete mechanism to follow.

**Affected docs (all interfaces and workflows):**
- `veda-to-project-v-signal-interface.md`
- `veda-to-v-forge-signal-interface.md`
- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `mcp-coordination-model.md`
- `data-boundaries.md`
- All 5 workflow docs
- All extension docs
- Most governance docs

**Fix applied so far:** `v-forge-evidence-access-contract.md` demonstrates the pattern — concrete query types, required parameters, scoping rules, response metadata. This pattern must be applied to the remaining cross-system interfaces.

**Required improvements:**

### VEDA → Project V signal interface needs:
- Defined query types for planning-relevant signal (e.g., `market_signal_by_topic`, `opportunity_scan`, `project_signal_status`)
- Required scoping parameters (topic, market, freshness_window)
- Freshness metadata on responses (same structure as V Forge evidence contract)
- Activity logging per signal query
- Cost accounting for signal queries against Project V planning budget
- Decision boundary: signal informs planning evaluation, does not auto-create projects

### Project V → V Forge handoff interface needs:
- Structured handoff packet definition (drawing from claw-code's TaskPacket pattern)
- Required fields: objective, scope, acceptance_criteria, constraints, evidence_references, approval_record, escalation_policy, reporting_contract
- Validation rules: handoff is rejected if required fields are missing
- Activity logging for handoff creation, acceptance, and rejection events
- Handoff packet should carry VEDA evidence references (not copies) so V Forge can query fresh evidence at execution time via the evidence access contract

### V Forge → Project V return-to-planning interface needs:
- Structured return packet definition
- Required fields: finding_type (blocker, failure, changed_condition, scope_question, evidence_conflict), description, evidence_references, suggested_action, severity
- Activity logging for return events
- Cost accounting: how many tokens were consumed before the return was triggered

---

## Finding 2 — No Activity Logging in Most Interface and Workflow Docs

**Problem:** 12 out of 16 interface docs and all 5 workflow docs have no mention of activity logging, audit trails, or event recording. This means the activity trail model we just created has no integration points in the docs that govern the actual cross-system interactions.

**Affected docs with no logging mention:**
- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `veda-to-project-v-signal-interface.md`
- `extension-agent-orchestration-model.md`
- `extension-memory-and-continuity-model.md`
- `extension-llm-behavior-contract.md`
- `extension-system-init-and-tool-surface-model.md`
- `data-boundaries.md`
- All 5 workflow docs (handoff, launch-readiness, maintenance-replanning, post-launch-observation, project-intake)

**Required improvement:** Each of these docs needs an "Activity Trail Integration" section that specifies:
- What actions in this doc produce activity trail records
- What action types from the activity trail vocabulary apply
- What fields are populated for each action type
- Whether any actions require real-time event publication

---

## Finding 3 — No Freshness Model for VEDA → Project V Signal

**Problem:** The `veda-to-project-v-signal-interface.md` references signal and evidence but has no freshness metadata requirements. This means a Project V agent receiving VEDA signal has no way to know whether it's looking at data from yesterday or last month. The V Forge evidence access contract solved this for V Forge. Project V has the same gap.

**Also affected:**
- `project-intake-workflow.md` — intake decisions based on VEDA signal with no freshness awareness
- `maintenance-and-replanning-workflow.md` — replanning triggered by signal with no freshness tracking
- `data-boundaries.md` — references consumed signal without freshness requirements

**Required improvement:** The freshness metadata model from the V Forge evidence access contract should be applied universally. Every cross-system data response should carry: `gathered_at`, `source_provider`, `freshness_status` (fresh/aging/stale/expired), `trust_classification`. This should be defined once in the cross-system access governance doc and referenced by all interface docs.

---

## Finding 4 — No Cost/Token Governance Anywhere

**Problem:** Zero docs in the ecosystem define cost governance, token budgets, or spending limits. The word "budget" appears nowhere in governance or workflow docs. The word "token" appears only in technical MCP/API context (session tokens), never in resource-consumption context.

This is the single biggest operational gap. An agent can theoretically make unlimited VEDA queries, run unlimited execution cycles, and consume unlimited tokens with no governance mechanism to detect or stop runaway spending.

**Required improvement:** A new doc: `governance/cost-and-token-governance.md`

This doc should define:
- **Budget policies** — per-agent, per-project, per-system, and ecosystem-wide spending limits (drawing from Paperclip's budget service pattern)
- **Budget windows** — monthly UTC or per-task
- **Budget statuses** — ok → warning → hard_stop
- **Budget incidents** — structured records when thresholds are breached
- **Cost event tracking** — every token-consuming action produces a cost event with: agent_id, project_id, system, action, input_tokens, output_tokens, api_cost_cents, timestamp
- **Auto-pause** — when hard_stop triggers, the agent or scope is paused with a structured reason
- **Budget query** — agents should be able to check their remaining budget before starting expensive operations

Every interface and workflow doc should then reference this governance doc and specify how cost tracking applies to the operations it defines.

---

## Finding 5 — No Structured Approval Records

**Problem:** 19 docs reference "approval" without defining structured approval records. The approval-and-escalation-model.md defines approval as a concept extensively but never specifies what an approval record looks like as structured data. An agent reading these docs knows approval matters but has no schema to work with.

**Required improvement:** The approval-and-escalation-model.md needs a structured approval record definition:
- `approval_id` — unique identifier
- `approval_type` — handoff, project_creation, launch, external_action, budget_override, scope_change
- `status` — pending, approved, rejected, revision_requested, expired
- `requested_by` — actor (agent_id or operator_id)
- `requested_at` — timestamp
- `decided_by` — actor (operator_id for human approvals)
- `decided_at` — timestamp
- `decision_note` — optional structured reason
- `linked_entities` — entity references (project_id, handoff_id, task_id)
- `expiry` — optional deadline after which pending approvals expire

This draws directly from Paperclip's approvals.ts pattern. Every doc that references approval should then reference this record definition.

---

## Finding 6 — No Degraded-Mode Doctrine Applied Broadly

**Problem:** The V Forge evidence access contract defines degraded-mode behavior for evidence unavailability. But no other interface or workflow doc addresses what happens when a cross-system dependency is unavailable.

Questions currently unanswered:
- What does Project V do if VEDA signal is unavailable during project intake?
- What does V Forge do if the handoff packet from Project V is incomplete?
- What does the post-launch observation workflow do if VEDA providers go down?
- What does the maintenance workflow do if V Forge can't reach VEDA for signal?
- What does any workflow do if approval infrastructure is unavailable?

**Required improvement:** Each cross-system interface doc and each workflow doc needs a "Degraded Mode" section that defines:
- What partial availability looks like for this interface
- What the consuming system should do when the dependency is partially or fully unavailable
- Whether the consuming system should halt, continue with limitations, or escalate
- What must be recorded when degraded-mode behavior occurs

---

## Finding 7 — Agent Orchestration Model Has No Shared State for Parallel Agents

**Problem:** The `extension-agent-orchestration-model.md` defines orchestrator and specialist agent roles but has no mechanism for parallel specialist agents to coordinate. If Agent A (evidence analysis) and Agent B (content gap analysis) are both working on related subtasks for the same project, they can't see each other's intermediate findings. The orchestrator has to relay everything.

**Required improvement:** Add a "Shared Execution Context" section to the orchestration model that defines:
- A session-scoped structured scratchpad that delegated agents can read from and write to
- Scratchpad entries carry: agent_id, entry_type, content, timestamp
- The orchestrator controls scratchpad lifecycle (create, clear, scope)
- Conflict detection: if two agents write conflicting findings to the same scratchpad key, the conflict is flagged rather than silently overwritten
- Scratchpad is non-canonical — it is a coordination artifact, not a system of record

---

## Finding 8 — Memory Model Has No Active Memory Management

**Problem:** The `extension-memory-and-continuity-model.md` defines memory as a passive system — things get compacted, things survive sessions, things are clearable. But the agent has no tools to actively manage its own memory. It can't decide "this finding is important, store it durably" or "search my previous session for the competitor analysis I did."

This is the gap that Letta/MemGPT solves with self-editing memory and that Paperclip's PARA memory skill solves with file-based atomic facts.

**Required improvement:** Add a "Memory-as-Tool-Surface" section to the memory model that defines:
- Memory tools available to the agent: `memory_store(key, value, memory_class, ttl)`, `memory_retrieve(query, scope, freshness_window)`, `memory_summarize(session_id)`, `memory_forget(key)`
- Memory tools are MCP tools — they follow the same MCP coordination model as all other tools
- Memory operations produce activity trail records
- Memory operations consume tokens and count against the agent's budget
- Stored memory carries provenance: who stored it, when, from what session, from what evidence
- Memory is scoped by project and system — cross-project memory bleed is prevented

---

## Finding 9 — Post-Launch Observation Workflow Assumes Passive V Forge

**Problem:** The `post-launch-observation-workflow.md` describes VEDA observing post-launch reality and signal flowing to Project V and V Forge. But V Forge's role is largely passive — it receives signal. The workflow doesn't describe V Forge actively querying VEDA for post-launch performance data to inform maintenance decisions.

With the new evidence access contract, V Forge agents can actively check signal status and query evidence during maintenance. The post-launch workflow should reflect this.

**Required improvement:** Update the post-launch observation workflow to include:
- V Forge agents actively querying VEDA via the evidence access contract during maintenance cycles
- V Forge using `signal_status` queries to determine which signal classes have degraded since launch
- V Forge using `evidence_by_project` queries to get current performance evidence when evaluating maintenance priorities
- Activity logging for post-launch evidence queries
- Degraded-mode behavior when post-launch signal is stale or unavailable

---

## Finding 10 — Handoff Workflow Has No Structured Handoff Packet

**Problem:** The `handoff-workflow.md` describes handoff stages in detail but never defines the structured handoff packet. It references "minimum interface semantics" (what, why, scope, boundaries, references, expected outcomes) but leaves these as prose bullets, not structured fields.

An agent executing a handoff has to interpret prose descriptions instead of validating structured data.

**Required improvement:** Define a structured handoff packet (drawing from claw-code's TaskPacket):
- `handoff_id` — unique identifier
- `project_id` — the project scope
- `objective` — what V Forge is being asked to execute
- `scope` — bounded execution scope (single_content, content_set, full_project, maintenance)
- `constraints` — what V Forge must not do
- `evidence_references` — VEDA evidence IDs that V Forge should query fresh via the evidence access contract (not stale copies)
- `acceptance_criteria` — how V Forge knows the work is complete
- `approval_record` — reference to the approval that authorized this handoff
- `escalation_policy` — what V Forge should do when blocked (retry_then_escalate, auto_escalate, return_to_planning)
- `reporting_contract` — what reports V Forge must produce (event_stream, summary, completion_report)
- `budget_allocation` — token/cost budget for this handoff's execution
- `created_at`, `approved_at` — timestamps for audit

---

## Priority Order

1. **Cost/token governance doc** (Finding 4) — without this, everything else can run unchecked
2. **Structured approval records** (Finding 5) — every doc references approvals without a schema
3. **Structured handoff packet** (Finding 10) — the most critical cross-system data transfer has no structure
4. **Activity trail integration across all interface/workflow docs** (Finding 2) — the trail exists but nothing feeds it
5. **Freshness model applied to VEDA → Project V** (Finding 3) — parity with the V Forge contract
6. **VEDA → Project V query mechanics** (Finding 1, partial) — Project V agents need the same access V Forge now has
7. **Return-to-planning structured packet** (Finding 1, partial) — the other critical cross-system transfer
8. **Degraded-mode sections in all interface/workflow docs** (Finding 6) — systems need to handle partial failure
9. **Memory-as-tool-surface** (Finding 8) — agents need active memory management
10. **Shared execution context for parallel agents** (Finding 7) — multi-agent coordination gap
11. **Post-launch workflow V Forge active queries** (Finding 9) — maintenance agents need live evidence

---

## Related Docs

- `../interfaces/v-forge-evidence-access-contract.md` — the pattern for how these improvements should look
- `cross-system-access-governance.md` — the access governance framework
- `activity-trail-model.md` — the activity trail all docs should integrate with
- `../governance/agent-operating-doctrine.md` — baseline agent behavior
- `../governance/approval-and-escalation-model.md` — needs structured approval records
- `../workflows/handoff-workflow.md` — needs structured handoff packet
