# Project V VS Code Extension Operator Surface

## Purpose

This document defines the governed operator surface for Project V inside the VS Code extension.

It exists to answer:

```text
What may the VS Code extension surface show from Project V, what actions may it initiate,
what must remain hidden or server-owned, and what rules keep this surface aligned with
Project V API and governance authority rather than drifting into invented behavior?
```

Read this with:

- `../api-conventions.md`
- `../endpoint-governance.md`
- `../mcp-surface.md`
- `../data-boundaries.md`
- `../system-invariants.md`
- `../status-transitions.md`
- `../../interfaces/extension-governance-and-gating-model.md`
- `../../interfaces/extension-llm-behavior-contract.md`
- `../../interfaces/operator-surface-interfaces.md`
- `../../interfaces/extension-vscode-surface-architecture.md`

This is a Tier 2 project implementation-build-spec authority document.

---

## Scope

This document governs:

- what Project V information the extension surface may present to the operator
- what Project V actions the extension surface may initiate
- how this surface relates to the Project V API families and MCP surface
- how extension actions map to governed backend routes
- which fields and states must remain hidden or server-owned in the operator surface
- how project scope and non-leakage posture must be preserved
- what initiation posture applies to each action category (human-initiated, suggested, or disallowed as automated)
- how the surface must avoid inventing backend semantics
- anti-drift rules specific to this surface

---

## Out of Scope

This document does not define:

- the global extension architecture — that belongs in `../../interfaces/extension-vscode-surface-architecture.md`
- the LLM behavior contract — that belongs in `../../interfaces/extension-llm-behavior-contract.md`
- the governance and gating model — that belongs in `../../interfaces/extension-governance-and-gating-model.md`
- the full Project V API family contracts — those belong in `project-v/api/`
- VEDA or V Forge operator surface rules — those belong in their respective operator surface docs
- implementation-specific UI component design, styling, or pixel layout

---

## System

- project-v

---

## Core Rule

The VS Code extension operator surface for Project V is a governed presentation and action layer over Project V API authority.

It is not an alternate authority layer.
It does not redefine route contracts, state semantics, or controlled vocabulary values.
It does not create new backend permissions through UI affordances.
It may only expose governed Project V capabilities that already exist through the API or MCP surface.

If the extension surface shows something, the underlying truth remains in the Project V database, governed by the API.
If the extension surface initiates an action, that action routes through the Project V API enforcement chain.
Nothing the extension surface does bypasses that chain.

---

## Surface Role

The Project V panel inside the VS Code extension serves three bounded purposes:

1. **Visibility** — showing the operator the current Project V planning state for the active project
2. **Action initiation** — allowing the operator to initiate governed Project V actions through the extension UI
3. **Review and decision support** — surfacing context that helps the operator make planning decisions without making those decisions on the operator's behalf

The surface is not a second Project V backend.
It is not an intelligent planning sovereign.
It is an operator-facing governance surface backed by the Project V API.

---

## Allowed Visibility

The extension surface may display the following categories of Project V information. Each is scoped to the active project only.

### Planning record state

- Project identity, name, key, and current status
- Objectives: key, title, status, priority
- Initiatives: key, title, status, priority, targetSystem, objectiveId linkage
- Work items: key, title, type, status, readinessState, targetSystem, blocked flag
- Dependencies: sourceEntityType, sourceEntityId, targetEntityType, targetEntityId, dependencyType, status

### Readiness and gap state

- ReadinessEvaluation records: entityType, entityId, evaluationType, result, rulePackage, summary, createdAt
- ReadinessGap records: severity, description, remediationSuggestion, resolved status
- Current readinessState per WorkItem (server-computed — displayed read-only, never editable)

### Audit and gap state

- AuditRun records: auditType, targetEntityType, result, summary, startedAt, completedAt
- AuditGap records: severity, description, remediation, status

### Decision and history state

- DecisionRecord records: title, decisionSummary, rationale, status, actor, entityType/entityId linkage
- StatusHistory records for governed entities: previousStatus, newStatus, reason, actor, createdAt

### Handoff state

- Handoff records: sourceEntityType, sourceEntityId, targetSystem, handoffType, status, readinessBasisSummary, completedAt
- Current handoff lifecycle stage

### Evidence and linkage

- EvidenceLink records: sourceEntityType, sourceEntityId, evidenceType, targetLocator, note, relevanceScore
  — displayed with explicit VEDA attribution where the evidence source is VEDA-owned; the extension must not present evidence content as Project V canonical truth
- ExternalLink records: sourceEntityType, targetSystem, linkType, url, externalId, label
- ResearchDoc records: title, sourceType, status, summary

### Portfolio and cross-record views

- Gap summary by severity across the active project
- Handoff pipeline summary for the active project
- WorkItem readiness summary for the active project
- Blocked item count and list for the active project

### Visibility constraints

- All visibility is scoped to the active session project. Records from other projects must never appear in any view.
- The extension must not render data it did not receive from the governed API for the active project.
- Server-owned fields — including readiness results, audit results, readinessState, completedAt, startedAt, actor — must be displayed as read-only. The extension must not render them in editable form.
- Evidence from VEDA must always display its source attribution. The label must appear on the record, not only as a tooltip.

---

## Allowed Action Types

The extension surface may initiate the following Project V actions. Each must route through the Project V API or MCP surface — not through a direct database call or a convenience shortcut.

### Planning record creation

- Create Objective — maps to `POST /objectives`
- Create Initiative — maps to `POST /initiatives`
- Create Work Item — maps to `POST /work-items`
- Create Dependency — maps to `POST /dependencies`
- Create Decision Record — maps to `POST /decision-records`
- Create Research Doc — maps to `POST /research-docs`
- Create Evidence Link — maps to `POST /evidence-links`
- Create External Link — maps to `POST /external-links`

All creation actions must supply only caller-permitted fields. Server-owned fields such as `readinessState`, `result`, `summary`, `completedAt`, and `actor` must not be included in creation payloads.

### Bounded field mutations

- Update Objective fields — maps to `PATCH /objectives/{id}` (bounded patchable fields only)
- Update Initiative fields — maps to `PATCH /initiatives/{id}`
- Update Work Item fields — maps to `PATCH /work-items/{id}`
- Update Dependency fields — maps to `PATCH /dependencies/{id}`
- Update Handoff fields — maps to `PATCH /handoffs/{id}` (readinessBasisSummary only)
- Update Evidence Link — maps to `PATCH /evidence-links/{id}` (note and relevanceScore only)
- Resolve or update Readiness Gap — maps to `PATCH /readiness-evaluations/{eid}/gaps/{gid}`
- Update Audit Gap — maps to `PATCH /audit-runs/{rid}/gaps/{gid}`

All mutation payloads must contain only governed patchable fields. Unknown or forbidden fields must not be submitted. The extension must not speculatively patch fields beyond what the API family authority docs permit.

### Governed status transitions

- Transition Objective status — maps to `POST /objectives/{id}/status`
- Transition Initiative status — maps to `POST /initiatives/{id}/status`
- Transition Work Item status — maps to `POST /work-items/{id}/status`
- Transition Handoff status — maps to `POST /handoffs/{id}/status`
- Supersede Decision Record — maps to `POST /decision-records/{id}/status`

Transition actions must supply the target status and, where the transition category requires it, a non-empty reason. The extension UI must surface a reason input for all reason-required transitions. The transition must be rejected if the reason is empty and doctrine requires one.

The extension must not permit transitions that are forbidden in `status-transitions.md` by rendering them as inactive or hidden rather than as greyed-out temptations with overridable warnings.

### Evaluation and audit initiation

- Evaluate readiness — maps to `POST /readiness-evaluations`
- Initiate audit run — maps to `POST /audit-runs`
- Mark audit run stale — maps to `POST /audit-runs/{id}/stale`

Evaluation and audit initiation must not supply caller-settable result or summary fields. Results are server-computed. The operator initiates; the server evaluates and returns the result.

### Handoff creation and lifecycle

- Create Handoff — maps to `POST /handoffs`
- Transition Handoff status (covered above under governed status transitions)

Handoff creation from the extension surface is a Class B action and requires operator approval before the API call is made. The approval event must be persisted before the creation request is sent. See Action Initiation and Approval Posture.

### Intake initiation

- Initiate project intake — initiates the intake classification workflow through the governed Project V path

Intake initiation is a Class B action. It must not proceed through conversational approval or LLM suggestion alone.

---

## Action Initiation and Approval Posture

Not all Project V extension actions have the same initiation posture. The posture is governed by the extension gating model in `../../interfaces/extension-governance-and-gating-model.md`. This section states the Project V-specific posture for each action category.

### Class A — No gate required

These actions may proceed without an explicit operator approval event:

- Reading and displaying any Project V planning record within the active project scope
- Evaluating readiness in read-only mode (not persisting the evaluation)
- Viewing gap lists, handoff state, decision history, status history
- Navigating the planning tree
- Bounded PATCH operations on support records with no lifecycle or governance consequence: updating an EvidenceLink's `note` or `relevanceScore`; setting a ReadinessGap's `resolved` flag or `remediationSuggestion`; updating an AuditGap's `status` or `remediation` field

### Class B — Persisted operator approval required before action proceeds

These Project V actions require a persisted approval event before the API call that creates or mutates governed state:

- Creating a new Objective, Initiative, or Work Item (primary planning record creation)
- Creating a new Handoff record (`POST /handoffs`)
- Activating a Handoff (transitioning a handoff to `ready` or `handed_off`)
- Closing or completing a Handoff
- Creating a governing Decision Record
- Executing a major status transition on a planning record that has downstream consequences (e.g., `active → completed` on an Objective or Initiative)
- Initiating a persisted readiness evaluation (`POST /readiness-evaluations`)
- Initiating an audit run (`POST /audit-runs`)
- Initiating project intake classification
- Initiating a return-to-planning path from a V Forge execution finding
- Superseding a prior Decision Record

### Suggested — LLM may suggest, operator must explicitly confirm

The LLM may surface a suggestion for the following, but the operator must explicitly confirm before the action proceeds. Confirmation is not conversational approval; it is a deliberate UI action that the operator takes after reviewing the suggestion:

- Filing an evidence link for a record the LLM identified as needing evidence
- Flagging a readiness gap as resolved
- Updating a WorkItem's blocked flag or blockedReason

### Automated — not permitted

The following must never be initiated automatically by the LLM or the extension without explicit operator instruction:

- Any status transition
- Any handoff creation or activation
- Any readiness evaluation persisted to the database
- Any audit run initiation
- Any Decision Record creation
- Any project intake classification

UI affordances that make these actions easy are welcome. Affordances that initiate them without operator direction are not.

---

## Relationship to Project V API Families

The extension operator surface is a consumer of the Project V API. It does not redefine contracts.

For each API family, the extension surface must:

- use only the request fields permitted by that family's authority doc
- submit payloads that conform to the error-code and validation posture in `api-conventions.md`
- handle `400`, `404`, `409`, and `422` responses correctly and surface errors to the operator without hiding them
- not retry rejected requests by stripping or overriding forbidden fields silently
- not treat a `404` response as indicating the resource exists in another project

Specific family constraints the extension surface must respect:

**Objectives, Initiatives, Work Items:** Status transitions must follow `status-transitions.md` exactly. The extension must not surface transition options for forbidden transitions. The reason input must be required where doctrine requires it.

**Readiness:** The result field is server-owned. The extension surface must not allow the operator to supply a result value or override the server-computed evaluation. The LLM may not suggest a result value as a shortcut to evaluation.

**Audits:** The result, summary, startedAt, and completedAt fields are server-owned. Same posture as readiness. The extension must not supply them in any creation or mutation payload.

**Handoffs:** The `completedAt` field is server-owned and set atomically on the `closed` transition. The extension must never supply it in a payload. It must display the value as read-only after the transition.

**Evidence Links:** The identity fields — sourceEntityType, sourceEntityId, evidenceType, targetLocator — are immutable after creation. The extension must not supply them in a PATCH payload. The `note` and `relevanceScore` fields are patchable.

**Dependencies:** A dependency cannot reference the same entity as both source and target. The extension should prevent self-reference selection in the UI before the API rejects it, but must handle the `422` rejection correctly if self-reference is submitted.

---

## Relationship to MCP Surface

The extension operator surface and the Project V MCP surface are parallel governed surfaces over the same Project V API. They are not substitutes for each other and must remain independently coherent.

Where an operator action in the extension initiates a Project V capability, that action should route through the same bounded API enforcement chain that MCP tools use. The extension must not implement a shortcut write path that the MCP surface does not also respect, and vice versa.

The session token model governs project scope for both surfaces. The extension operator surface must not permit scope drift that the MCP surface would prevent, and must not rely on the MCP layer to enforce scope that the extension UI should already be respecting.

When the LLM uses MCP tools inside an extension session to perform Project V operations, the same server-owned field rules, same transition rules, and same non-leakage posture apply as when the operator uses the extension's native UI actions.

---

## Relationship to Extension Governance and Gating

This document inherits the full gating model from `../../interfaces/extension-governance-and-gating-model.md`. All Project V actions that fall into Class B or Class C under that model require a persisted approval event before the downstream API call is permitted.

The extension operator surface for Project V must:

- present the approval gate widget within the relevant record detail panel, not in the LLM interaction panel
- write the approval record to the database before calling the Project V API for the gated action
- block the API call if the approval write fails, and surface the failure to the operator
- not allow conversational statements in the LLM panel to substitute for the persisted approval event
- treat rejected approval requests as persisted rejection events, not as soft dismissals

---

## Hidden, Non-Visible, and Server-Owned State Rules

### Server-owned fields — never editable in the operator surface

The following fields are produced by server-side execution logic. The extension surface may display their values but must never allow the operator to supply or override them:

- `WorkItem.readinessState` — server-managed, updated atomically on readiness evaluation
- `ReadinessEvaluation.result` — server-computed by governed evaluation logic
- `ReadinessEvaluation.summary` — server-generated by evaluation execution
- `AuditRun.result` — server-computed by governed audit logic
- `AuditRun.summary` — server-generated by audit execution
- `AuditRun.startedAt` — set by the server at audit creation
- `AuditRun.completedAt` — set by the server at audit completion
- `Handoff.completedAt` — set atomically by the server on the `closed` transition
- `StatusHistory.actor` — resolved server-side from the session context

If the extension receives these fields in an API response, it must display them as read-only values. If any UI element would allow a user to edit one of these fields, that UI element is a doctrine violation regardless of whether the API would reject the resulting payload.

### Hidden state — must not be surfaced in the operator or LLM surface

The following must not be surfaced in the extension operator or LLM surface:

- Internal database IDs beyond the record IDs needed to identify and navigate records
- Session token content — the operator and LLM see the project name and scope, not the session token itself
- Records belonging to projects other than the active session project — must return `404` and must not be displayed
- Server-side enforcement error internals beyond the governed error shape (`error.code`, `error.message`, `error.details`)
- Internal implementation details of readiness or audit evaluation logic beyond the governed summary and gaps

### Non-leakage in the operator surface

When the extension makes a request that returns `404 Not Found` for an out-of-scope resource:

- the extension must display a generic not-found message, not a message that hints the resource exists in another project
- the extension must not attempt to re-fetch the resource from a different project scope to "help" the operator find it
- the extension must not log or display the existence of out-of-scope resources

The non-leakage posture applies in both directions: the extension must not tell the operator what they cannot see, and must not tell the LLM either.

---

## Multi-Project and Non-Leakage Rules

The extension operator surface for Project V operates within a single active project scope established by the session token. The following rules apply:

### Scope constraint

- Every Project V API call made by the extension must be scoped to the active session project.
- The extension must not construct API calls that reference records from a different project.
- If the operator requests information about a record that belongs to a different project, the surface returns a not-found state rather than switching scope or leaking cross-project state.

### Scope change

- Changing the active project requires explicit operator action through the project selector, which initiates a new session token.
- The extension must not silently change scope because the operator mentions a different project in conversation.
- When scope changes, all cached planning state from the prior session must be cleared before the new project's state is loaded.

### LLM and non-leakage

- The LLM operating inside the extension session must not be provided with data from a project other than the active session project.
- The extension must not construct LLM context payloads by combining records from multiple project scopes.
- If the LLM asks about a resource that appears to be from a different project, the extension must return a not-found result to the LLM — not the cross-project data.

### Multi-project portfolio visibility

Portfolio-level visibility across multiple projects — where the operator wants to compare or prioritize across projects — requires an explicit cross-project portfolio mode that is governed separately. This doc does not establish that mode. Until a governed cross-project portfolio surface is documented, the Project V extension operator surface is single-session-project-scoped only.

---

## Anti-Drift Rules

### Rule 1 — Extension actions must map to governed API families

Every action available in the Project V extension operator surface must correspond to a governed Project V API route or MCP tool that already exists. The extension must not implement write behaviors that are not backed by a governed endpoint.

If a new extension affordance would require an endpoint that does not yet exist in a Project V API family authority doc, the endpoint must be governed first. The extension surface must not outrun endpoint governance.

### Rule 2 — UI affordances do not create new backend permissions

Displaying a button or menu item in the extension does not add a new Project V capability. The capability must exist in the API first. A button that calls a route the API will reject is still wrong — the API rejection does not make the affordance acceptable.

### Rule 3 — The extension surface must not invent state semantics

The extension must not define its own meaning for planning statuses, readiness states, or audit results. All vocabulary values and state semantics come from `controlled-vocabularies.md` and the API family authority docs. The extension surface must display and label states using the governed vocabulary.

### Rule 4 — Evidence and VEDA-sourced content must preserve attribution

When the extension surface displays an EvidenceLink or ResearchDoc that references VEDA-owned material, it must label the source system. The display must not present VEDA evidence content as Project V canonical planning truth.

### Rule 5 — The surface must not suggest that read-only evaluations are editable

ReadinessEvaluation and AuditRun records are immutable after creation (except for the governed staleness path on audits). The extension must not display an edit affordance for these records. Displaying a result as though it can be revised by clicking on it is a UI anti-pattern that teaches the operator incorrect semantics.

### Rule 6 — Convenience shortcuts must not bypass governed transition rules

The extension must not implement "quick transition" buttons that bypass the transition posture in `status-transitions.md`. If a transition requires a reason, the UI must require a reason. If a transition is forbidden, the UI must not offer it. A one-click convenience action is acceptable; a one-click bypass of a governed constraint is not.

### Rule 7 — The surface must not claim to know the current Project V state without fetching it

The extension must not render cached or stale planning state as current truth. When an action is performed that affects planning state, the relevant views must refresh from the API before the operator's next governance-sensitive interaction. Stale display that makes outdated state look current is a visibility failure that can lead to incorrect operator decisions.

---

## Non-Goals

This document does not:

- define VEDA or V Forge extension operator surface behavior
- govern MCP tool schemas beyond their relationship to extension actions
- specify the visual design or layout of the Project V panel beyond what doctrine requires
- govern the cross-system portfolio view surface
- grant new action classes or bypass existing gating posture
- replace the API family authority docs for their respective contracts

---

## Final Rule

The extension surface for Project V is bounded by Project V API authority. Everything it can show comes from the governed API. Everything it can do routes through the governed API enforcement chain.

An extension surface that makes things visible that the API has not returned, or that initiates actions the API would not govern, has broken this boundary — regardless of how useful the shortcut appeared.

---

## Usage

This document should be used:

- when building the Project V panel inside the VS Code extension
- when deciding whether a proposed extension affordance is backed by a governed API family
- when reviewing whether an extension action correctly handles server-owned fields, rejection posture, and non-leakage
- when deciding whether a proposed UI shortcut bypasses a governed transition or approval requirement
- when reviewing whether extension-displayed state preserves system attribution for evidence and external references

---

## Related Docs

- `../api-conventions.md`
- `../endpoint-governance.md`
- `../mcp-surface.md`
- `../data-boundaries.md`
- `../system-invariants.md`
- `../status-transitions.md`
- `../controlled-vocabularies.md`
- `../multi-project-doctrine.md`
- `../api/objectives.md`
- `../api/initiatives.md`
- `../api/work-items.md`
- `../api/dependencies.md`
- `../api/handoffs.md`
- `../api/readiness.md`
- `../api/audits.md`
- `../api/evidence-links.md`
- `../../interfaces/extension-governance-and-gating-model.md`
- `../../interfaces/extension-llm-behavior-contract.md`
- `../../interfaces/operator-surface-interfaces.md`
- `../../interfaces/extension-vscode-surface-architecture.md`
- `../../interfaces/extension-state-and-context-model.md`
- `../../interfaces/mcp-coordination-model.md`
- `../../governance/approval-and-escalation-model.md`
- `../../governance/auth-and-actor-model.md`
- `../../ecosystem/cross-system-boundaries.md`
- `../../ecosystem/vocabulary.md`
