# Extension Implementation Architecture

## Purpose

This document defines the implementation-facing architecture for the V Ecosystem VS Code extension.

It exists to answer:

```text
How should the extension be structured in code and runtime so that the already-established extension doctrine becomes a real, buildable VS Code extension without cheating governance, collapsing system boundaries, or letting the LLM interaction surface become the actual system?
```

This is a Tier 1 ecosystem authority support document for implementation.

---

## Scope

This document governs:

- the implementation module boundaries for the extension
- the required runtime responsibilities of core extension subsystems
- the relationship between canonical state surfaces, interaction surfaces, and gate surfaces
- the required state stores and service boundaries
- command routing and panel routing responsibilities
- validation and approval pipeline responsibilities
- the order in which the extension should be built
- the anti-drift implementation constraints developers must preserve

This document assumes the active binding of:

- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-state-and-context-model.md`
- `extension-human-llm-interaction-model.md`
- `extension-vscode-surface-architecture.md`

---

## Out of Scope

This document does not define:

- the final visual design language of the extension
- exact MCP tool schemas
- backend API endpoint internals
- exact TypeScript framework/library choices for webviews
- packaging, publishing, or marketplace distribution details

Those belong in implementation specs, repo-local build docs, and later engineering decisions.

---

## System

- interfaces

---

## Core Rule

The extension must be implemented so that doctrine is enforced structurally.

This means:

- canonical state must live in governed records and explicit state surfaces
- LLM interaction must remain a support surface, not the source of truth
- approval-sensitive actions must pass through the governed gate pipeline
- the wrong actions must be physically absent from the wrong surfaces
- module structure must make it hard for implementation convenience to bypass doctrine

If the implementation architecture makes it easy to route around approvals, collapse surfaces, or treat the LLM panel as the real app, the implementation architecture is wrong.

---

## Architectural Surface Split

The extension must be implemented around three architectural surface classes.

### 1. Canonical State Surfaces
These are the surfaces that display governed current state.

Examples:
- Project V tree view
- VEDA tree view
- V Forge tree view
- detail panels for records, packages, decisions, evidence, and workflow objects
- status strip / context strip surfaces

### Rule
Canonical state surfaces render governed system state. They do not infer authority from conversation and they do not store governance state in ephemeral UI objects.

---

### 2. Interaction Surface
This is the surface where the human operator and the LLM interact.

Examples:
- LLM sidebar
- operator framing controls
- typed output cards
- clarification and refinement requests

### Rule
The interaction surface produces and routes typed outputs. It does not own canonical state, does not persist approval by prose, and does not activate Class B or C actions directly.

---

### 3. Gate Surfaces
These are the surfaces where governance-sensitive activation becomes possible.

Examples:
- approval gate panel
- launch authorization panel
- escalation panel
- typed confirmation surface for irreversible Class C actions

### Rule
Gate surfaces are distinct from interaction surfaces. A Recommendation or Approval Request Package may route the operator toward a gate surface, but it must not collapse into one.

---

## Required Module Boundaries

The extension codebase should be split into the following major module groups.

### 1. Core Types
This module group defines the typed vocabulary used throughout the extension.

It should include types for:
- systems
- workflow stages
- interaction modes
- typed outputs
- action classes
- approval states
- context descriptors
- session integrity state

### Rule
Core type definitions must reflect doctrine vocabulary directly.
Implementation must not invent alternate synonyms for core governance concepts.

---

### 2. State Stores
This module group owns in-memory extension state.

It should include at minimum:

#### `projectScopeStore`
Owns:
- active project id
- active project key or display name
- session-bound scope token state

#### `contextStore`
Owns:
- current system
- referenced systems
- current workflow stage
- decision context summary
- evidence basis summary
- freshness markers
- loaded context descriptors

#### `approvalStore`
Owns:
- pending approval request packages
- approval state per actionable item
- stale or expired approvals
- rejected approval records relevant to current session

#### `integrityStore`
Owns:
- unresolved return triggers
- pending approvals from prior sessions
- stale recommendations
- stale readiness states
- unresolved conflict markers

#### `sessionState`
Owns top-level session composition:
- scope health
- connection health
- current interaction mode if selected
- current context snapshot
- current integrity snapshot

### Rule
State stores mirror extension doctrine. They do not become convenience caches for hidden behavior. Chat/session prose must not be treated as canonical store content.

---

### 3. Services
This module group owns controlled runtime behaviors.

It should include at minimum:

#### `mcpSessionService`
Responsible for:
- session initialization
- scope-bound token lifecycle
- MCP registration
- session health and reconnection state

#### `apiClient`
Responsible for:
- all backend API calls
- attaching session token
- standardized error handling
- response typing
- preserving 404 vs 403 semantics where doctrine requires non-disclosure

#### `contextLoader`
Responsible for:
- initial current-context load
- refresh of decision context
- refresh of evidence basis
- freshness checks
- session integrity checks
- bounded cross-system context retrieval

#### `approvalService`
Responsible for:
- creation of approval records
- creation of rejection records
- stale approval checks
- typed confirmation handling
- activation precondition enforcement before downstream API call

#### `conflictDetector`
Responsible for:
- decision conflict detection
- approval state conflict detection
- conflicting typed output detection where relevant

#### `recommendationValidator`
Responsible for:
- validating Recommendation outputs
- validating Approval Request Package outputs
- rejecting incomplete typed outputs before they are rendered as governed widgets

### Rule
Services centralize governed logic. Tree views, webviews, and command handlers must not each invent their own approval, context, or validation behavior.

---

### 4. Surface Providers
This module group binds doctrine to real VS Code surfaces.

It should include at minimum:

#### Sidebar providers
- Project V tree provider
- VEDA tree provider
- V Forge tree provider
- status/context strip provider if implemented as a view surface

#### LLM interaction provider
- LLM sidebar provider
- typed output renderer
- operator input controller
- interaction mode controller

#### Detail panel providers
- record detail panel router
- initiative detail panel
- decision/evidence detail panel
- handoff detail panel
- launch readiness detail panel
- approval gate panel
- escalation panel

### Rule
Surface providers render state and route actions. They must not silently mutate governed state through hidden side paths.

---

### 5. Command Handlers
This module group owns command registration and explicit command routing.

It should include at minimum:
- session commands
- navigation commands
- LLM interaction commands
- approval and gate commands
- workflow navigation commands

### Rule
Command handlers must remain explicit and narrow. A generic do-anything command is a governance smell.

---

## Required Command Categories

The extension should define commands in bounded categories.

### Session commands
Examples:
- select project
- refresh session
- show session integrity
- copy current context

### Navigation commands
Examples:
- open Project V view
- open VEDA view
- open V Forge view
- reveal record in tree
- open detail panel

### LLM interaction commands
Examples:
- set interaction mode
- submit operator input
- request Recommendation
- request Review Summary
- request Approval Request Package

### Approval and gate commands
Examples:
- open approval gate
- approve action
- reject action
- defer action
- escalate action
- confirm irreversible Class C action with typed input

### Rule
Approval and activation commands must only be callable from gate surfaces or from explicit routing into gate surfaces. They must not be attached directly to freeform LLM output prose or generic status-bar shortcuts.

---

## Required State Model

The following state categories must exist as explicit implementation concepts.

### 1. Project scope state
The extension must always know which project scope is active and whether the current session token is healthy.

### 2. Current system state
The extension must track one explicit current system.

### 3. Referenced systems state
The extension may track zero or more referenced systems, but these remain bounded references only.

### 4. Workflow state
The extension must track current stage, next gate, blocking conditions, and major pending items.

### 5. Approval state
The extension must track whether an item is pending approval, approved, rejected, revoked, stale, expired, or not approval-relevant.

### 6. Integrity state
The extension must track session-start integrity concerns and mid-session integrity changes.

### Rule
These state categories must not be reconstructed ad hoc from LLM output history. They are explicit runtime state, not narrative artifacts.

---

## Typed Output Validation Layer

The extension must implement a validation layer before rendering governance-relevant typed outputs.

### Recommendation validation
Before a Recommendation widget is rendered, validation must confirm the output contains:
- producer attribution
- proposed path
- bounded scope
- basis
- uncertainty
- governance posture
- acceptance outcome
- non-acceptance outcome

### Approval Request Package validation
Before an Approval Request Package widget is rendered, validation must confirm the output contains:
- action being requested
- action class
- scope
- basis
- what approval covers
- what approval does not cover
- default state if denied
- target detail panel or route for the approval gate

### Rule
If validation fails, the extension must not render the output as a governed widget. It must surface a validation failure and withhold the governed rendering path.

---

## Approval Pipeline

The implementation must preserve a distinct approval pipeline.

### Required chain
For Class B and C actions, the extension must implement the following chain:

1. typed output produced
2. operator explicitly chooses to proceed
3. relevant detail panel opens
4. approval gate widget is rendered in the detail panel
5. operator reviews full contextual record
6. approval event is persisted
7. for irreversible Class C actions, typed confirmation is completed
8. downstream activation API call is made
9. activation result is surfaced explicitly

### Rule
No code path may skip from typed output card to activation API call.
No code path may treat LLM-panel interaction as sufficient for approval persistence.

---

## Detail Panel Responsibility

Detail panels are the required location for dense review and gate execution.

Detail panels should own:
- full record inspection
- evidence details
- decision chain visibility
- handoff package review
- launch readiness review
- approval gate widgets
- escalation review and documentation

### Rule
If review context is too dense for a sidebar, it belongs in a detail panel. Governance-sensitive work must not be forced into cramped surfaces that encourage skimming.

---

## LLM Sidebar Responsibility

The LLM sidebar should own:
- operator input
- interaction framing controls
- typed output cards
- clarification loops
- routing actions such as `Proceed to Approval Gate`

The LLM sidebar must not own:
- canonical record storage
- final approval persistence
- activation of Class B or C actions
- the only copy of important workflow meaning

### Rule
The LLM sidebar supports reasoning and routing. It does not become the real app.

---

## Primary Sidebar Responsibility

The primary sidebar should own:
- system-separated navigation surfaces
- tree-based state visibility
- explicit project scope visibility
- blocked items and pending counts where appropriate
- return triggers and pending governance-relevant items where appropriate

The primary sidebar must not own:
- freeform chat
- dense review artifacts better suited to detail panels
- hidden approval logic

### Rule
The primary sidebar is the map of governed state, not the place where governance happens by surprise.

---

## Status and Context Surface Responsibility

The extension must maintain a persistent status/context surface showing at minimum:
- current project scope
- current system
- current workflow stage
- approval state summary
- session integrity state summary

This may be split across status bar and context strip surfaces, but the architecture must ensure these elements remain visible and synchronized.

### Rule
Status/context surfaces are architectural, not decorative. If they drift out of sync with the LLM surface or detail panels, the extension teaches the wrong reality.

---

## Notification and Alert Policy

The implementation must scale notification style to governance importance.

### Appropriate uses
- activity badge for pending approvals or unresolved return triggers
- status/context warning for session health or staleness
- inline panel banner for changed context
- session-start integrity notification for unresolved prior-state items
- blocking modal only for truly irreversible Class C confirmation or equivalent hard stop

### Rule
Modal overuse is a governance failure. If everything is modal, operators will dismiss without reading. Blocking surfaces must be reserved for genuinely blocking moments.

---

## Absent-Affordance Implementation Rule

The extension must physically enforce absent-affordance doctrine.

Examples:
- VEDA view must not expose “Create Planning Record”
- Project V view must not expose execution-only actions
- V Forge view must not expose planning-decision mutation actions
- status bar must not expose mutation actions
- LLM output cards must not expose final approval buttons for Class B or C actions

### Rule
Absent-affordance doctrine must be implemented in construction of the UI and command map, not as warnings after the operator clicks the wrong thing.

---

## Surface Synchronization Rule

The extension must ensure that:
- primary sidebar
- secondary sidebar
- detail panels
- status/context surfaces

all reflect the same current project scope, current system, and major workflow state.

### Rule
If one surface updates but the others continue showing stale or mismatched state, the extension creates governance drift. Synchronization is a first-class implementation requirement.

---

## Build Order

The extension should be built in the following order.

### Phase 1 — Skeleton and scope
Build:
- extension activation
- project selection
- primary view container
- empty system views
- LLM sidebar shell
- command registration skeleton
- session scope selection and health wiring

### Phase 2 — State spine
Build:
- project scope store
- context store
- integrity store
- initial context loading
- status/context surfaces
- session integrity checks

### Phase 3 — Typed output rendering
Build:
- typed output renderer
- interaction mode handling
- operator input controller
- Recommendation and Approval Request Package validation

### Phase 4 — Detail panels
Build:
- generic detail panel router
- record detail panels
- approval gate panel
- launch/handoff review panels

### Phase 5 — Approval pipeline
Build:
- approval persistence flow
- rejection flow
- typed confirmation flow
- stale approval detection
- activation precondition checks

### Phase 6 — Workflow-specific drill-down
Build:
- handoff review flow
- return trigger handling flow
- launch readiness flow
- conflict handling flow

### Rule
Do not begin with decorative UI. Do not begin with clever agent behavior. Build the state spine and approval pipeline before polishing the interaction surface.

---

## Anti-Drift Implementation Failures

The following are implementation failures:

- putting an approval button directly on a LLM output card for a Class B or C action
- allowing tree view items to call mutating APIs directly without the governed gate path
- letting the LLM surface become the only place where workflow meaning is understandable
- inferring interaction mode or current system too loosely from topic drift
- storing governance-relevant state in session prose rather than explicit stores and persisted records
- duplicating approval logic across multiple UI layers instead of routing through approvalService
- allowing convenience commands to bypass panel routing and approval persistence

---

## Human-In-The-Loop Principle

The implementation architecture must preserve the human operator as the accountable party by making real review and real gate completion possible, visible, and structurally required where doctrine says they are required.

If implementation convenience removes the need for dense review or permits approval through side paths, the architecture has ceased to support human-in-the-loop governance even if the UI still uses the right words.

---

## LLM Use Principle

A capable LLM should be able to infer from this architecture that:

- it operates through bounded services and explicit typed outputs
- its outputs are validated before they are rendered as governed widgets
- it may route the operator toward approval but not satisfy approval itself
- canonical state lives in governed surfaces and explicit stores, not in chat history
- context loading, approval state, and workflow state are explicit runtime concepts
- the wrong actions are absent from the wrong surfaces by design
- structural enforcement is the implementation priority, not behavioral aspiration

If the implementation lets a model jump from typed output to mutating API call, or lets the LLM surface become the only meaningful control surface, the implementation architecture is being violated.

---

## Usage

This document should be used:

- when structuring the extension codebase
- when deciding what modules, stores, and services must exist
- when reviewing whether a proposed command or panel belongs in the architecture
- when checking whether implementation shortcuts violate doctrine
- when sequencing the initial build order for the extension
- when writing more detailed repo-local implementation specs for the extension

---

## Related Docs

- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-state-and-context-model.md`
- `extension-human-llm-interaction-model.md`
- `extension-vscode-surface-architecture.md`
- `operator-surface-interfaces.md`
- `mcp-coordination-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/recommendation-packaging-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
- `../workflows/project-intake-workflow.md`
- `../workflows/handoff-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../workflows/launch-readiness-workflow.md`
