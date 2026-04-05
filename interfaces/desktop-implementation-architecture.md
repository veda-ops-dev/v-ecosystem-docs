# Desktop Implementation Architecture

## Purpose

This document defines the implementation-facing architecture for the V Ecosystem Tauri 2 desktop application.

It exists to answer:

```text
How should the desktop application be structured in code and runtime so that the already-established doctrine becomes a real, buildable Tauri 2 operator application without cheating governance, collapsing system boundaries, letting the LLM interaction surface become the actual system, or turning runtime power features into hidden authority paths?
```

This is a Tier 1 ecosystem authority support document for implementation.

---

## Scope

This document governs:

- the implementation module boundaries for the desktop application
- the required responsibilities of frontend, sidecar/runtime, and backend-facing subsystems
- the relationship between canonical state surfaces, interaction surfaces, gate surfaces, and runtime visibility surfaces
- the required state stores and service boundaries
- routing and workspace responsibilities
- validation and approval pipeline responsibilities
- orchestration, continuity, compaction, and tool-surface implementation boundaries
- runtime refresh and invalidation responsibilities
- the order in which the desktop application should be built
- the anti-drift implementation constraints developers must preserve

This document assumes the active binding of:

- `desktop-surface-architecture.md`
- `runtime-sidecar-and-nerve-model.md`
- `local-first-architecture.md`
- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-state-and-context-model.md`
- `desktop-human-llm-interaction-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-memory-and-continuity-model.md`
- `desktop-system-init-and-tool-surface-model.md`

---

## Out of Scope

This document does not define:

- the final visual design language of the desktop application
- exact MCP tool schemas
- backend API endpoint internals
- exact React component implementation details
- packaging, installer, update, or distribution details
- exact CSS implementation patterns

Those belong in implementation specs, repo-local build docs, and later engineering decisions.

---

## System

- interfaces

---

## Core Rule

The desktop application must be implemented so that doctrine is enforced structurally.

This means:

- canonical state must live in governed backend records and explicit state surfaces
- LLM interaction must remain a support surface, not the source of truth
- approval-sensitive actions must pass through the governed gate pipeline
- the wrong actions must be physically absent from the wrong surfaces
- orchestration, continuity, and tool-surface logic must remain bounded runtime capabilities rather than hidden authority layers
- frontend structure, sidecar structure, and service boundaries must make it hard for implementation convenience to bypass doctrine

If the implementation architecture makes it easy to route around approvals, collapse surfaces, let continuity artifacts masquerade as canonical state, or treat the right interaction panel as the real app, the implementation architecture is wrong.

---

## Architectural Layer Split

The desktop application must be implemented around four architectural layer classes.

### 1. Canonical Backend Layer
These are the systems that own governed truth.

Examples:
- Project V backend services
- VEDA backend services
- V Forge backend services

### Rule
Canonical backend services own governed records, approval persistence, lifecycle truth, and system-of-record mutations. The desktop application does not replace them.

---

### 2. Frontend Application Layer
This is the operator-visible desktop product surface.

Examples:
- topbar
- left navigation panel
- center workspace/detail views
- right interaction/context panel
- lower trace/runtime visibility surface

### Rule
The frontend renders state, routes operator actions, and presents typed outputs. It does not become the hidden runtime engine and does not persist approval by prose.

---

### 3. Runtime / Sidecar Layer
This is the Tauri-managed runtime-support layer.

Examples:
- Nerve runtime support
- session/runtime support
- orchestration support
- compaction support
- tool-surface support
- transcript persistence support
- token/cost tracking support

### Rule
The runtime/sidecar layer supports the operator host. It does not become canonical system truth and it does not become an invisible governance layer.

---

### 4. Gate Layer
This is the implementation path where governance-sensitive activation becomes possible.

Examples:
- Class B inline approval pipeline
- Class C typed confirmation pipeline
- escalation handling path

### Rule
Gate logic is distinct from interaction logic and detail rendering logic. A Recommendation or Approval Request Package may route the operator toward a gate path, but must not collapse into one.

---

## Frontend / Sidecar Communication and Backend Ownership

The desktop application uses a Tauri-based architecture where the frontend (web view) and sidecar/runtime (Rust backend) communicate via IPC.

### Backend Communication Ownership

**All backend API calls to Project V, VEDA, and V Forge must originate from the sidecar/runtime layer, not directly from the frontend.**

This means:
- The frontend **never** makes HTTP calls directly to Project V, VEDA, or V Forge APIs
- The frontend invokes Tauri commands that route to sidecar/runtime services
- Sidecar/runtime services perform the actual backend API communication
- API responses flow back through IPC to update frontend state stores

### Why Sidecar Owns Backend Communication

1. **Session token management**: The sidecar owns the MCP session token and project scope binding
2. **Tool surface coordination**: Runtime services need direct backend access for MCP tool execution
3. **Governed write enforcement**: Approval persistence must route through runtime validation before backend mutation
4. **Local-first coordination**: The sidecar manages SQLite local state alongside backend sync

### Frontend Service Clarification

**`apiClient` is not a direct HTTP client.** It is the frontend's **IPC interface layer** that:
- Provides typed method calls for frontend code to request backend operations
- Routes those requests through Tauri IPC to the appropriate sidecar services
- Handles IPC response typing and error surfacing
- Maintains consistent error semantics (404 vs 403) as defined by doctrine

### Runtime Service Backend Communication

The following sidecar/runtime services own actual backend API communication:

**`approvalService`** (sidecar):
- Receives approval/rejection commands from frontend via IPC
- Performs validation and precondition checks
- Makes the backend API call to persist the approval record
- Returns success/failure status to frontend for state update

**`contextLoader`** (sidecar/runtime coordinated):
- Can be invoked from frontend but executes in sidecar context
- Loads canonical state from backend APIs
- Performs freshness and integrity checks
- Returns loaded context to frontend for store population

**`systemInitBuilder`** and **`toolSurfaceAssembler`** (sidecar):
- Query backend state as needed during session initialization
- Assemble runtime session basis
- Never expose raw backend access to frontend

### Validation Placement

**Pre-render validation** (`recommendationValidator`) runs in the sidecar/runtime:
- Receives typed outputs from LLM interaction
- Validates structure before allowing frontend rendering
- Returns validation result via IPC
- Frontend only renders validated outputs as governed widgets

**Conflict detection** (`conflictDetector`) runs in the sidecar/runtime:
- Compares proposed actions against loaded canonical state
- Detects cross-record or cross-session conflicts
- Surfaces conflicts to frontend for operator review

### Data Flow for Governed Writes

The canonical approval flow is:

1. **Frontend**: Operator clicks approval in gate widget
2. **Frontend**: Calls `apiClient.approveAction()` (IPC invocation)
3. **Sidecar**: `approvalService` receives IPC command
4. **Sidecar**: Validates preconditions, checks staleness
5. **Sidecar**: Makes HTTP call to backend API to persist approval
6. **Sidecar**: Returns result via IPC
7. **Frontend**: Updates `approvalStore` and triggers refresh
8. **Frontend**: Surfaces activation result to operator

This preserves the doctrine requirement that approval persistence happens through governed paths while clarifying that "governed path" means sidecar-mediated backend communication, not direct frontend HTTP calls.

### Rule

The frontend must never bypass the sidecar layer to communicate directly with Project V, VEDA, or V Forge backend APIs. All backend communication for governed operations must route through sidecar services that enforce doctrine constraints before making HTTP calls.

---

## Required Module Boundaries

The desktop application codebase should be split into the following major module groups.

### 1. Core Types
This module group defines the typed vocabulary used throughout the desktop host.

It should include types for:
- systems
- workflow stages
- interaction modes
- typed outputs
- action classes
- approval states
- context descriptors
- session integrity state
- orchestration task states
- continuity artifact types
- tool-surface posture descriptors
- runtime visibility descriptors
- local-support-state descriptors

### Rule
Core type definitions must reflect doctrine vocabulary directly.
Implementation must not invent alternate synonyms for core governance concepts.

---

### 2. In-Memory State Stores
This module group owns in-memory reactive desktop state.

It should include at minimum:

#### `sessionStore`
Owns:
- active project id
- active project display name
- session-bound scope token state summary
- current system
- connection and session health
- current interaction posture

#### `projectVStore`
Owns operator-visible Project V state required for desktop surfaces.

#### `vedaStore`
Owns operator-visible VEDA state required for desktop surfaces.

#### `vForgeStore`
Owns operator-visible V Forge state required for desktop surfaces.

#### `contextStore`
Owns:
- current system
- referenced systems
- current workflow stage
- decision context summary
- evidence basis summary
- freshness markers
- loaded context descriptors
- current tool-surface posture summary

*Implementation note on workflow stage:* Some workflow stages in `desktop-state-and-context-model.md` are directly anchored to governed record fields (e.g., `Handoff.status = ready` → `Handoff — Prepared`). Others are runtime-derived posture with no settled schema record anchor as of this writing — notably intake stages, maintenance vs replanning posture, and launch readiness stages. The `contextStore` must track the workflow stage and its derivation basis. Where the stage is derived rather than record-loaded, the store must preserve that distinction so the UI can correctly surface `Unavailable` rather than a false-confident stage label when derivation inputs are missing. See `desktop-state-and-context-model.md` § Recognized Stage Names for per-stage record-anchor status.

#### `approvalStore`
Owns:
- pending approval request packages
- approval posture per actionable item
- stale or expired approvals relevant to the current session
- rejection markers relevant to current work

#### `integrityStore`
Owns:
- unresolved return triggers
- pending approvals from prior sessions where surfaced
- stale recommendations
- stale readiness states
- unresolved conflict markers
- session integrity flags

#### `orchestrationStore`
Owns:
- active orchestrator posture summary
- delegated subtasks visible to the operator
- specialist-role assignments where surfaced
- task lifecycle state
- failure/cancellation markers
- orchestration event summaries for UI use

#### `continuityStore`
Owns:
- active working continuity entries
- active session-durable continuity entries
- compact-boundary records
- continuity freshness markers
- visible transcript-derived continuity references
- clearability/dismissal state

#### `uiStore`
Owns:
- selected workspace node
- active center view
- panel sizes/collapse posture
- lower surface visibility
- non-canonical UI interaction posture

### Rule
Stores mirror doctrine and frontend operating needs. They do not become convenience caches for hidden behavior. Chat or session prose must not be treated as canonical store content.

---

### 3. Local Support-State Layer
This module group owns local SQLite persistence and hydration support.

It should include at minimum:
- local cache persistence
- recently accessed record persistence
- draft persistence where allowed
- local continuity support persistence
- layout/session restoration support
- support-state reconciliation hooks

### Rule
The local support-state layer is non-canonical. It exists for continuity, startup speed, drafts, and recovery support. It must not become the real source of governed truth.

---

### 4. Frontend Services
This module group owns controlled frontend-side behaviors.

It should include at minimum:

#### `apiClient`
Responsible for:
- all backend API calls
- attaching session/scope posture as required
- standardized error handling
- response typing
- preserving 404 vs 403 semantics where doctrine requires non-disclosure

#### `contextLoader` (frontend-facing interface to sidecar service)
Responsible for:
- coordinating initial current-context load requests
- coordinating refresh of decision context
- coordinating refresh of evidence basis
- requesting freshness checks
- requesting session integrity checks
- coordinating bounded cross-system context retrieval

Note: Actual backend communication is performed by the sidecar; this is the frontend's request interface.

#### `workspaceRouter`
Responsible for:
- opening and switching center review/detail surfaces
- routing from left navigation and right-panel outputs into the proper center views
- preventing the wrong content from appearing in the wrong surface

#### `approvalFlowController`
Responsible for:
- opening the correct gate surface
- enforcing review-before-gate posture
- routing approval completion to the proper persisted path
- preventing direct activation from interaction surfaces

#### `refreshCoordinator`
Responsible for:
- invalidation event handling
- cross-store refresh triggers
- surface synchronization after approvals, context changes, compaction events, delegated-task completion, or system changes

**Event taxonomy:** The `refreshCoordinator` must handle every trigger event defined in `desktop-invalidation-and-refresh-matrix.md`. It must not maintain its own informal internal list of events. The matrix is the authoritative source.

**Sequencing rules:** Events must be processed according to the priority order defined in `desktop-invalidation-and-refresh-matrix.md` § Sequencing Rules:
1. Session token expiry / runtime scope breakage supersedes all other in-flight events. All surface updates stop and degraded posture is applied immediately.
2. Blocking events (Level 2) must complete their full propagation before the next LLM turn is enabled.
3. Non-blocking refresh events (Level 3) must complete before any Class B or C gate is presented, but do not interrupt the current interaction flow.
4. Informational updates (Level 4) may complete asynchronously.

**Concurrent event handling:** When two or more events fire in the same session tick at the same priority level, the `refreshCoordinator` processes them in matrix-listed order and layers their consequences. Events must not be collapsed into a single undifferentiated notification. Each event's full consequence set must fire independently.

**Turn boundary rule:** A blocking event that fires while an LLM turn is in progress does not interrupt the turn. The turn completes. The output is marked stale before rendering. The blocking posture takes effect before the next turn begins.

**Anti-drift rule:** The `refreshCoordinator` must not invent shortcuts — for example, marking a whole session as valid/invalid instead of applying per-category validation, or silently skipping a surface update because it appears cosmetic. Every consequence in the matrix for a given event must fire.

#### `notificationCoordinator`
Responsible for:
- scaling alerts to importance
- routing topbar warnings, inline banners, notifications, and modals
- preventing modal overuse

### Rule
Frontend services route and coordinate. They must not invent their own approval logic, orchestration logic, or backend truth shortcuts.

---

### 5. Runtime / Sidecar Services
This module group owns controlled runtime-support behaviors.

It should include at minimum:

#### `runtimeSessionService`
Responsible for:
- runtime/session initialization
- scope-bound token lifecycle support
- runtime health and reconnection posture
- sidecar-level session integrity support

#### `systemInitBuilder`
Responsible for:
- assembling the runtime session basis
- building the structured runtime init posture
- converting loaded canonical state into faithful runtime distillation
- marking missing or stale required categories

#### `toolSurfaceAssembler`
Responsible for:
- assembling the session tool surface
- filtering tools by project scope, current system, action posture, and delegated-role posture
- narrowing delegated worker tool surfaces
- surfacing bounded tool posture to state/UI layers

#### `orchestrationService`
Responsible for:
- subtask creation and routing
- specialist invocation within admitted bounds
- task lifecycle management
- cancellation and failure handling
- packaging delegated outputs back into the parent interaction flow

#### `memoryManager`
Responsible for:
- creating and updating working continuity artifacts
- session-durable continuity handling
- freshness and age metadata maintenance
- source attribution for continuity artifacts
- clear/dismiss operations where allowed

#### `compactionService`
Responsible for:
- micro-compaction and working-continuity extraction where admitted
- preserving protected context across compaction
- creating compact-boundary records
- triggering visible refresh notices after material compaction

#### `transcriptService`
Responsible for:
- transcript capture
- transcript artifact retrieval
- orchestration event log integration
- non-authority labeling support for transcript and trace surfaces

#### `approvalService`
Responsible for:
- creation of approval records through the proper path
- creation of rejection records
- stale approval checks
- typed confirmation handling
- activation precondition enforcement before downstream API call

#### `conflictDetector`
Responsible for:
- decision conflict detection
- approval state conflict detection
- conflicting typed output detection where relevant
- conflicts between canonical state and continuity or worker artifacts

#### `recommendationValidator`
Responsible for:
- validating Recommendation outputs
- validating Approval Request Package outputs
- rejecting incomplete typed outputs before they are rendered as governed widgets

### Rule
Runtime services centralize governed runtime-support logic. Frontend views must not each invent their own approval, context, orchestration, continuity, or validation behavior.

---

### 6. Surface Components and Providers
This module group binds doctrine to real desktop surfaces.

It should include at minimum:

#### Shell components
- topbar
- left navigation panel
- center workspace shell
- right context/interaction panel
- lower trace/runtime surface

#### Navigation components
- Project V tree/navigation renderer
- VEDA tree/navigation renderer
- V Forge tree/navigation renderer
- attention and session indicators

#### Interaction components
- interaction shell
- typed output renderer
- operator input controller
- orchestration summary renderer
- continuity summary renderer
- context strip renderer

#### Center workspace components
- record detail router
- record detail views
- handoff review views
- launch readiness review views
- return-trigger review views
- transcript/audit review views
- inline gate widgets

#### Gate components
- Class B inline approval widgets
- Class C modal confirmation surfaces
- escalation banners or escalation review surfaces

### Rule
Surface components render state and route actions. They must not silently mutate governed state through hidden side paths.

---

### 7. Command and Action Routing Layer
This module group owns bounded command routing and global action entry points.

It should include at minimum:
- session commands
- navigation commands
- interaction commands
- gate-opening commands
- workflow navigation commands
- transcript/audit review commands
- bounded orchestration inspection commands

### Rule
Command handlers must remain explicit and narrow. A generic do-anything command is a governance smell.

---

## Required Command Categories

The desktop application should define commands in bounded categories.

### Session commands
Examples:
- select project
- refresh session
- show session integrity
- copy current context

### Navigation commands
Examples:
- switch system
- reveal record in navigation tree
- open detail view
- open trace or audit review

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

### Runtime visibility commands
Examples:
- show transcript/audit review
- show continuity detail
- show orchestration detail
- review compact-boundary event

### Rule
Approval and activation commands must only be callable from gate surfaces or from explicit routing into gate surfaces. They must not be attached directly to freeform LLM output prose or generic topbar shortcuts.

---

## Required State Model

The following state categories must exist as explicit implementation concepts.

### 1. Project scope state
The desktop application must always know which project scope is active and whether the current scope/session posture is healthy.

### 2. Current system state
The desktop application must track one explicit current system.

### 3. Referenced systems state
The desktop application may track zero or more referenced systems, but these remain bounded references only.

### 4. Workflow state
The desktop application must track current stage, next gate, blocking conditions, and major pending items.

### 5. Approval state
The desktop application must track whether an item is pending approval, approved, rejected, revoked, stale, expired, or not approval-relevant.

### 6. Integrity state
The desktop application must track session-start integrity concerns and mid-session integrity changes.

### 7. Orchestration state
The desktop application must track meaningful delegated-task lifecycle and review status.

### 8. Continuity state
The desktop application must track what non-canonical continuity artifacts are active and whether they are aging, stale, or cleared.

### 9. Tool-surface posture state
The desktop application must track what general runtime tool posture is currently active and whether delegated work is narrowed from the parent session.

### 10. Local-support-state posture
The desktop application must track what local support material is current, stale, draft, pending reconciliation, or cleared.

### Rule
These state categories must not be reconstructed ad hoc from LLM output history. They are explicit runtime and frontend state, not narrative artifacts.

---

## Typed Output Validation Layer

The desktop application must implement a validation layer before rendering governance-relevant typed outputs.

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
- target center-review or gate route

### Delegated output validation
Where delegated worker outputs are surfaced distinctly, validation must confirm:
- worker/source attribution
- bounded task scope
- non-authority posture
- lifecycle result state

### Rule
If validation fails, the desktop application must not render the output as a governed widget. It must surface a validation failure and withhold the governed rendering path.

---

## Approval Pipeline

The implementation must preserve a distinct approval pipeline.

### Required chain
For Class B and Class C actions, the desktop application must implement the following chain:

1. typed output produced
2. operator explicitly chooses to proceed
3. relevant center review surface opens
4. approval gate widget is rendered in the center review surface or modal path
5. operator reviews full contextual record
6. approval event is persisted through the proper path
7. for irreversible Class C actions, typed confirmation is completed
8. downstream activation API call is made
9. activation result is surfaced explicitly

### Rule
No code path may skip from typed output card to activation API call.
No code path may treat interaction-panel input, delegated worker output, transcript artifact, or continuity artifact as sufficient for approval persistence.

---

## Workspace Responsibility

Center workspace surfaces are the required location for dense review and gate execution.

Center workspace surfaces should own:
- full record inspection
- evidence details
- decision chain visibility
- handoff package review
- launch readiness review
- approval gate widgets
- escalation review and documentation
- transcript and audit review where runtime traceability matters

### Rule
If review context is too dense for a support panel, it belongs in the center workspace. Governance-sensitive work must not be forced into cramped surfaces that encourage skimming.

---

## Right Interaction Panel Responsibility

The right interaction panel should own:
- operator input
- interaction framing controls
- typed output cards or bounded typed output summaries
- clarification loops
- routing actions such as proceed-to-review or open-detail
- bounded orchestration summary visibility
- bounded continuity summary visibility
- context strip visibility

The right interaction panel must not own:
- canonical record storage
- final approval persistence
- activation of Class B or Class C actions
- the only copy of important workflow meaning

### Rule
The interaction panel supports reasoning and routing. It does not become the real app.

---

## Left Navigation Responsibility

The left navigation surfaces should own:
- system-separated navigation structures
- tree-based state visibility
- explicit project scope visibility
- blocked items and pending counts where appropriate
- return triggers and pending governance-relevant items where appropriate

The left navigation surfaces must not own:
- freeform chat
- dense review artifacts better suited to the center workspace
- hidden approval logic

### Rule
The left navigation surface is the map of governed state, not the place where governance happens by surprise.

---

## Topbar and Status Responsibility

The desktop application must maintain a persistent top-level status/context layer showing at minimum:
- current project scope
- current system
- current workflow stage summary where appropriate
- session integrity posture summary
- orchestration summary when materially relevant
- continuity summary when materially relevant
- current tool-surface posture summary in bounded form

### Rule
Status/context surfaces are architectural, not decorative. If they drift out of sync with the interaction panel or center workspace, the application teaches the wrong reality.

---

## Notification and Alert Policy

The implementation must scale notification style to governance importance.

### Appropriate uses
- attention badges for pending approvals or unresolved return triggers
- top-level status warning for session health or staleness
- inline banner for changed context
- session-start integrity notification for unresolved prior-state items
- visible compaction/refresh notice for material continuity changes
- blocking modal only for truly irreversible Class C confirmation or equivalent hard stop

### Rule
Modal overuse is a governance failure. If everything is modal, operators will dismiss without reading. Blocking surfaces must be reserved for genuinely blocking moments.

---

## Absent-Affordance Implementation Rule

The desktop application must physically enforce absent-affordance doctrine.

Examples:
- VEDA navigation must not expose create-planning-record actions
- Project V surfaces must not expose execution-only actions
- V Forge surfaces must not expose planning-decision mutation actions
- topbar must not expose mutation actions
- interaction-panel output cards must not expose final approval buttons for Class B or Class C actions
- delegated-worker surfaces must not expose broader authority than the parent session
- lower trace/runtime surfaces must not expose approval controls

### Rule
Absent-affordance doctrine must be implemented in construction of the UI, tool surface, and command map, not as warnings after the operator clicks the wrong thing.

---

## Surface Synchronization Rule

The desktop application must ensure that:
- topbar
- left navigation panel
- right interaction panel
- center workspace surfaces
- lower trace/runtime surfaces where open

all reflect the same current project scope, current system, and major workflow posture.

### Rule
If one surface updates but the others continue showing stale or mismatched state, the application creates governance drift. Synchronization is a first-class implementation requirement.

This includes:
- approval writes
- decision invalidation
- evidence refresh
- compaction events
- delegated-task completion/failure/cancellation
- current-system changes
- session token expiry or scope breakage

---

## Build Order

The desktop application should be built in the following order.

### Phase 1 — Shell and scope
Build:
- desktop shell
- project selection
- topbar
- left navigation shell
- center workspace shell
- right interaction shell
- command routing skeleton
- session scope selection and health wiring

### Phase 2 — State spine
Build:
- sessionStore
- contextStore
- integrityStore
- system stores
- initial context loading
- topbar/status surfaces
- session integrity checks

### Phase 3 — Local-first spine
Build:
- local SQLite support layer
- startup hydration path
- local cache shell
- draft persistence shell
- support-state reconciliation hooks

### Phase 4 — Runtime session basis
Build:
- runtimeSessionService
- systemInitBuilder
- toolSurfaceAssembler
- continuity store shell
- orchestration store shell
- refreshCoordinator

### Phase 5 — Typed output rendering
Build:
- typed output renderer
- interaction mode handling
- operator input controller
- Recommendation and Approval Request Package validation
- delegated-output rendering rules

### Phase 6 — Center review surfaces
Build:
- generic center workspace router
- record detail views
- approval gate surfaces
- launch and handoff review views
- transcript and audit review views

### Phase 7 — Approval pipeline
Build:
- approval persistence flow
- rejection flow
- typed confirmation flow
- stale approval detection
- activation precondition checks

### Phase 8 — Runtime power features
Build:
- orchestrationService
- memoryManager
- compactionService
- transcriptService
- orchestration event logging
- visible continuity and orchestration refresh flows
- lower trace/runtime surface

### Phase 9 — Workflow-specific drill-down
Build:
- handoff review flow
- return-trigger handling flow
- launch readiness flow
- conflict handling flow

### Rule
Do not begin with decorative UI. Do not begin with clever agent behavior. Build the shell, state spine, local-first layer, runtime basis, and approval pipeline before polishing the interaction surface.

---

## Anti-Drift Implementation Failures

The following are implementation failures:

- putting an approval button directly on a typed LLM output card for a Class B or Class C action
- allowing navigation items to call mutating APIs directly without the governed gate path
- letting the interaction panel become the only place where workflow meaning is understandable
- inferring interaction mode or current system too loosely from topic drift
- storing governance-relevant state in session prose rather than explicit stores and persisted records
- duplicating approval logic across multiple UI layers instead of routing through approval services
- allowing convenience commands to bypass workspace routing and approval persistence
- letting continuity artifacts become indistinguishable from canonical state in code or UI
- letting delegated runtime gain broader tool surfaces or hidden mutation paths through implementation shortcuts
- letting local SQLite support state become easier to trust than backend truth

---

## Human-In-The-Loop Principle

The implementation architecture must preserve the human operator as the accountable party by making real review and real gate completion possible, visible, and structurally required where doctrine says they are required.

If implementation convenience removes the need for dense review, hides orchestration influence, or permits approval through side paths, the architecture has ceased to support human-in-the-loop governance even if the UI still uses the right words.

---

## LLM Use Principle

A capable LLM should be able to infer from this architecture that:

- it operates through bounded services and explicit typed outputs
- its outputs are validated before they are rendered as governed widgets
- it may route the operator toward approval but not satisfy approval itself
- canonical state lives in governed backend records, explicit stores, and governed surfaces, not in chat history or continuity artifacts
- context loading, approval state, workflow state, orchestration state, continuity state, and local-support-state posture are explicit runtime concepts
- the wrong actions are absent from the wrong surfaces by design
- structural enforcement is the implementation priority, not behavioral aspiration

If the implementation lets a model jump from typed output to mutating API call, lets delegated runtime become a hidden authority layer, or lets the interaction surface become the only meaningful control surface, the implementation architecture is being violated.

---

## Usage

This document should be used:

- when structuring the desktop application codebase
- when deciding what modules, stores, and services must exist
- when reviewing whether a proposed command or surface belongs in the architecture
- when checking whether implementation shortcuts violate doctrine
- when sequencing the initial build order for the desktop application
- when writing more detailed repo-local implementation specs for the desktop application

---

## Related Docs

- `desktop-surface-architecture.md`
- `runtime-sidecar-and-nerve-model.md`
- `local-first-architecture.md`
- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-state-and-context-model.md`
- `desktop-human-llm-interaction-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-memory-and-continuity-model.md`
- `desktop-system-init-and-tool-surface-model.md`
- `operator-surface-interfaces.md`
- `mcp-coordination-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/recommendation-packaging-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
- `../workflows/project-intake-workflow.md`
- `../workflows/handoff-workflow.md`
- `../workflows/maintenance-and-replanning-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../ux/desktop/direction/desktop-host-migration-plan.md`
- `desktop-invalidation-and-refresh-matrix.md`
