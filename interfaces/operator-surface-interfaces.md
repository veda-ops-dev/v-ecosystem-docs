# Operator Surface Interfaces

## Purpose

This document defines how human operators interact with the V Ecosystem
across its three core systems.

It exists to answer:

```text
What surfaces does each system expose to the human operator, what actions
may an operator take through those surfaces, what must operators not do
directly that must instead go through governed paths, and how are operator
interactions kept consistent with system boundaries and approval posture?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- what operator-facing surfaces exist across Project V, VEDA, and V Forge
- what kinds of operator actions are permitted through each surface
- what operator actions require governed approval before they become active
- what operators must not do directly that must instead route through a governed path
- how the desktop application serves as the primary operator surface across all three systems
- the boundary posture operators must preserve when using ecosystem surfaces

---

## Out of Scope

This document does not define:

- implementation-specific UI layout or component design
- detailed API endpoint design
- detailed MCP tool lists per system
- detailed session management implementation
- operator authentication and credential mechanics

Those belong in system-specific operator surface docs, implementation docs, and
the MCP coordination model.

---

## System

- interfaces

---

## Core Rule

Operator surfaces are governance surfaces, not raw access surfaces.

An operator interacting with a system through its surface is still bound by the
system's role, ownership boundaries, approval posture, and interface constraints.

Access to a surface does not grant authority to act outside the system's
classified role. A surface is the mechanism through which governed interaction
happens. It is not a bypass of governance.

---

## Primary Operator Surface: Desktop Application

The unified Tauri 2 desktop application is the primary operator interface for the V Ecosystem.

Governed by ADR-011 (Tauri 2 desktop as operator host) and ADR-005 (session token model),
the desktop application provides:

- a project selector that establishes the active project scope for the session
- a status bar element showing the active project at all times
- system-specific panels for Project V, VEDA, and V Forge
- the mechanism through which LLM sessions are scoped to a specific project

The desktop application is a governance layer, not merely a display surface.
Through its sidecar/runtime layer, it initializes a session with the MCP server when the operator selects a project; the MCP server issues an opaque session token bound to that project. All MCP tool calls within the session carry that token automatically. The LLM never sees the project UUID — it sees only the opaque session token. This prevents cross-project contamination at the tool-call level.

The MCP coordination model is defined in:
`../interfaces/mcp-coordination-model.md`

---

## Project V Operator Surface

### What operators may do through the Project V surface

- view current planning state across all active projects
- initiate intake evaluation for a new candidate
- review and approve or reject pending intake outcomes
- review planning records, decisions, and handoff packages
- approve or reject handoff activation for approval-gated handoffs
- initiate return-to-planning reviews
- approve or reject replanning proposals
- review and approve audit results
- configure portfolio visibility and sequencing preferences within governed bounds

### What requires approval before becoming active

- intake outcome activation (Class B or C depending on scope)
- handoff activation (Class B or C depending on scope and launch sensitivity)
- significant planning mutations or governing decision revisions (Class B or C)
- project thesis revision (Class B)
- project archive decisions (Class B)

### What operators must not do directly

- mutate VEDA observatory records from the Project V surface
- mutate V Forge execution records from the Project V surface
- self-authorize approval-gated planning actions without the required approval posture

The operator authority model is defined in:
`../governance/auth-and-actor-model.md`
The approval posture is defined in:
`../governance/approval-and-escalation-model.md`

---

## VEDA Operator Surface

### What operators may do through the VEDA surface

- view current observatory state for active projects
- configure observatory scope — what signals to watch for which projects
- review signal packages and evidence records
- initiate bounded evidence requests for specific signals
- approve paid data pulls and spend-creating external actions
- review and configure provider integrations within governed bounds
- view the observatory event log for a project

### What requires approval before becoming active

- activating a new paid data provider or spend-creating data pull (Class C)
- significantly expanding observatory scope beyond currently approved bounds (Class B or C)
- any external action that creates spend or triggers paid retrieval (Class C)

### What operators must not do directly

- mutate Project V planning records from the VEDA surface
- mutate V Forge execution records from the VEDA surface
- treat observatory signal as planning decisions

VEDA is a pure observatory. The operator surface reflects that role.
Operators may direct what VEDA watches. They may not use VEDA to make
planning or execution decisions.

External action governance is defined in:
`../governance/external-action-governance.md`
Paid data pull governance is defined in:
`../governance/paid-data-pull-governance.md`

---

## V Forge Operator Surface

### What operators may do through the V Forge surface

- view current execution state for active handed-off work
- review execution findings and bounded execution reports
- approve or reject launch-sensitive execution actions that require operator authorization
- initiate or approve return-to-planning when execution findings warrant it; operators must distinguish between findings that can be resolved within existing approved scope as maintenance activity and findings that warrant governed return-to-planning and potential replanning — routing a maintenance finding as though it were a replanning trigger is a governance error, and the V Forge surface must support that distinction through clearly differentiated response paths
- review pre-launch verification status
- approve launch activation for approval-gated launches
- review the content graph for handed-off projects
- configure bounded execution scope preferences within approved handoff bounds

### What requires approval before becoming active

- launch-sensitive execution activation (Class C — requires explicit operator approval)
- external publication, distribution, or spend-creating execution actions (Class C)
- scope expansions beyond the approved handoff scope (Class B or C)
- return-to-planning activation that materially affects planning direction (Class B)

### What operators must not do directly

- create or modify Project V planning records from the V Forge surface
- create or modify VEDA observatory records from the V Forge surface
- self-authorize launch-sensitive actions without confirmed launch readiness and approval

V Forge governance is defined in:
`../v-forge/system-invariants.md`
Launch readiness is governed by:
`../workflows/launch-readiness-workflow.md`

---

## Cross-System Operator Posture

When an operator is working across multiple systems in a single session,
the cross-system actor rules from the auth and actor model apply.

Operators retain distinct responsibilities in each system:

- in Project V: the operator is the planning and approval authority
- in VEDA: the operator is the observatory scope and spend authority
- in V Forge: the operator is the execution authorization and launch authority

Cross-system visibility does not merge those roles.
An operator with access to all three surfaces does not gain merged authority
to act in any system without the constraints of that system's posture.

Cross-system actor rules are defined in:
`../governance/auth-and-actor-model.md`

---

## Operator Direction and Agent Assistance

Operators frequently work with agents through the operator surfaces.

The division of responsibility is:

- the operator provides direction, makes approval-sensitive decisions, and authorizes actions
- the agent assists with interpretation, packaging, reporting, and bounded preparation
- the agent must not treat operator direction as governed approval unless the required
  approval posture has been satisfied

Informal operator direction through a conversation surface is not governed approval.
Where governance requires explicit approval, the operator must satisfy that approval
posture through the governed path, not through conversational permission.

Agent authority rules are defined in:
`../governance/agent-operating-doctrine.md`
`../governance/allowed-agent-actions-matrix.md`

---

## Session Scope Principle

Every operator session that uses MCP tools is scoped to a single active project
through the session token model.

This means:

- the operator must select a project before MCP tool calls are available
- all tool calls within the session are automatically scoped to that project
- the operator cannot contaminate one project's records with another project's session
- changing the active project requires a new session token

The session token model is defined in:
`../interfaces/mcp-coordination-model.md`

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- operator surfaces are governance surfaces, not raw access channels
- each system surface has a distinct operator role and permitted action set
- approval-gated actions require satisfied approval posture, not just operator presence
- cross-system surface access does not merge authority across systems
- operator direction through conversation is not governed approval

If an LLM treats operator presence at a surface as authorization for any action
on that surface, this doctrine is failing.

---

## Usage

This document should be used:

- when designing the operator-facing behavior of any system surface
- when deciding whether an operator action requires approval or may proceed
- when reviewing whether an operator interaction stayed within governed surface bounds
- when designing agent-assisted workflows that involve operator review or approval
- when writing system-specific operator surface docs that must be consistent with
  this cross-system posture

---

## Related Docs

- `mcp-coordination-model.md`
- `veda-to-project-v-signal-interface.md`
- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `data-boundaries.md`
- `../governance/auth-and-actor-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/allowed-agent-actions-matrix.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/external-action-governance.md`
- `../ecosystem/cross-system-boundaries.md`
