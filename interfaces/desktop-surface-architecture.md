# Desktop Surface Architecture

## Purpose

This document defines the desktop surface architecture for the V Ecosystem operator application — the physical layout of surfaces, the placement of actions, the assignment of content to surfaces, and the absent-affordance rules that prevent the wrong actions from appearing in the wrong places.

It exists to answer:

```text
What are the primary desktop surfaces, what is each one for, what belongs where, what must never appear in certain places, and how does the surface architecture physically embody the behavior, governance, state/context, orchestration, continuity, and interaction doctrines already established?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the primary surface categories the desktop application uses
- the role and content rules for the left navigation panel
- the role and content rules for the right interaction/context panel
- the role and content rules for center workspace detail and review surfaces
- the role and content rules for topbar status, context indicators, badges, notifications, and modals
- the optional lower trace/log/orchestration surface
- the placement of actions and commands by surface
- the visible placement of orchestration state, continuity state, compact-boundary state, and tool-surface posture
- the absent-affordance rules that enforce system boundaries by what is not present
- the LLM surface limits that prevent the interaction panel from becoming the real system
- surface synchronization requirements

This document builds on and assumes the active binding of:
- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-state-and-context-model.md`
- `desktop-human-llm-interaction-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-memory-and-continuity-model.md`
- `desktop-system-init-and-tool-surface-model.md`
- `runtime-sidecar-and-nerve-model.md`
- `local-first-architecture.md`

---

## Out of Scope

This document does not define:

- specific visual styling, color tokens, or pixel dimensions
- exact React component implementations or Tauri API calls
- MCP server protocol details
- database schema or API endpoint design
- full keyboard shortcut or command catalog
- exact CSS animation mechanics

The architecture must be concrete enough to constrain later implementation choices without specifying every implementation detail.

---

## System

- interfaces

---

## Core Rule

The surface architecture physically embodies doctrine.

Governance is not only what the system says it will do. It is what the system makes possible and what it makes impossible through surface design. A surface that contains the wrong actions teaches the operator to expect those actions. A surface that is missing actions that should not be there enforces the boundary silently and correctly.

The desktop application has six surface categories. Each has a defined role. Content and actions must be placed in the surface that matches their role. Content placed in the wrong surface is not a cosmetic choice — it is a doctrine failure.

---

## Surface Categories

The desktop application uses six surface categories:

### 1. Navigation and State Surfaces
Show the operator where they are, what is active, what is blocked, what requires attention, and what runtime posture is currently in effect. Always visible. Never contain approval gates or silent mutation actions.

**Desktop surfaces:** Topbar system/project indicators, left navigation tree, top-level attention badges.

### 2. Interaction Surfaces
The LLM interaction surface where the operator frames work and the LLM produces typed bounded outputs. Supports the system. Does not replace it.

**Desktop surfaces:** Right context and interaction panel.

### 3. Detail and Review Surfaces
Rich read-mostly surfaces for inspecting records, evidence, decisions, handoff packages, launch readiness assessments, approval request packages, transcript/audit artifacts, and continuity-heavy review work. Open on demand within the main workspace. Support dense review work without cluttering navigation surfaces.

**Desktop surfaces:** Center workspace/detail surface.

### 4. Gate and Approval Surfaces
Surfaces specifically for approval events, typed confirmations, and escalation flows. These are where persisted approval events are created or rejected. Distinct from review surfaces.

**Desktop surfaces:** Inline approval widgets embedded in center detail surfaces for Class B actions; modal gates for Class C actions.

### 5. Alert and Notification Surfaces
Transient or persistent surfaces for session integrity warnings, decision context changes, evidence staleness notices, compaction/refresh notices, and governance-sensitive interruptions. Scaled to importance — not every notice is a modal.

**Desktop surfaces:** Topbar status indicators, inline banners, toast or in-app notifications, modal interruptions where governance requires them.

### 6. Trace and Runtime Visibility Surfaces
Secondary review surfaces for transcript artifacts, orchestration traces, continuity markers, task progression, delegated-task outcomes, and runtime-support visibility where materially relevant.

**Desktop surfaces:** Optional lower trace/log/orchestration surface and center transcript/audit review views.

---

## Shell Structure

The operator host is a unified desktop application with a stable shell.

The shell consists of:
- a topbar
- a left navigation/state panel
- a center workspace/detail surface
- a right context and interaction panel
- an optional lower trace/log/orchestration surface

The shell is unified across Project V, VEDA, and V Forge.
System switching changes content and posture within the shell. It does not swap the operator into unrelated products.

The shell must preserve these truths:
- the operator should be able to navigate and understand state without using the LLM
- review should happen in the center workspace, not in cramped support surfaces
- the right panel supports interpretation and action framing but does not become the real app
- runtime power features must be visible enough for accountability without dominating the shell by default

---

## Topbar

### Role
Persistent navigation and state surface for ecosystem-wide context.

### Required Content
The topbar must be capable of showing:
- current project scope
- current active system
- session health/integrity state
- connection/runtime posture where materially relevant
- attention indicators for pending critical items
- access to settings/help/session-integrity views where appropriate

### Allowed Functions
The topbar may support:
- project switching through the governed project-selection path
- system switching between Project V, VEDA, and V Forge
- opening session integrity or attention views
- opening bounded global commands where allowed

### Topbar Anti-Affordance Rules
The topbar must not contain:
- approval controls
- ambiguous mutation actions
- LLM prompt input
- hidden system switching that changes scope without visible acknowledgment
- actions that appear to govern state by convenience

The topbar orients and signals. It does not govern.

---

## Left Navigation Panel

### Role
Navigation and state surface. The operator uses the left panel to understand current project state across all three systems, navigate to specific records, and see what requires attention. The left panel is not a chat surface and is not where approval gates live.

### System-Aware Structure
The left panel changes content by active system while preserving a consistent tree-based navigation posture.

### Required System Views

**Project V — Planning**

Content:
- current project scope label
- objective tree
- initiative tree
- work items
- gaps section with severity indicators
- handoffs section with status indicators
- return-trigger visibility where planning response is needed

Status indicators per tree item may include: `proposed`, `active`, `blocked`, `ready`, `handed_off`, `accepted`, `closed`.

Actions available in this view:
- navigate to center workspace detail for any record
- initiate readiness review through the proper path
- create planning record through governed command path
- transition planning state through governed command path
- initiate intake through explicit command path

  *Note: As of this writing, the Project V schema does not define a dedicated intake record type. What this command creates or navigates to depends on how intake record design is settled. Until then, this action must be treated as workflow-session-derived rather than creating a specific canonical record that the navigation tree can anchor to.*

Actions NOT available in this view:
- approve or activate handoffs directly in the tree
- configure observatory scope as though it were Project V-owned
- launch execution actions as though this view owned V Forge

**VEDA — Observatory**

Content:
- observatory domains and provider sections
- signal packages ready for consumption
- provider freshness/health posture
- bounded observatory record groupings

Actions available in this view:
- navigate to center workspace detail for observatory records
- open signal package review in the center workspace
- configure observatory scope within governed operator bounds
- initiate paid data pull approval request through the governed path

Actions NOT available in this view:
- create or modify Project V planning records
- initiate or approve V Forge execution
- produce planning decisions directly from the navigation surface

**V Forge — Execution**

Content:
- active execution items with stage indicators
- content graph summary or related execution structure summaries
- return triggers shown prominently when present
- recent execution reports/findings summaries where appropriate

Actions available in this view:
- navigate to execution detail in the center workspace
- route return trigger through the governed interface
- request pre-launch verification review in the center workspace
- initiate launch authorization request through the governed path

Actions NOT available in this view:
- create or modify Project V planning records
- modify governing decisions
- configure VEDA observatory scope
- self-authorize launch-sensitive action

### Left Panel Anti-Affordance Rules

The left navigation panel must not contain:
- approval buttons or approval gate widgets
- any action that silently creates or modifies governed records without explicit command path
- any action that crosses system ownership as though ownership were local
- any LLM prompt input field or freeform mode selector
- any action labeled ambiguously enough to be confused with approval

The left panel navigates and shows. It does not govern.

---

## Right Context and Interaction Panel

### Role
Interaction surface. The LLM interaction panel lives here alongside persistent context and action framing. The operator frames work, the LLM produces typed bounded outputs, and the operator reviews and responds through defined response options. This surface supports the system. It does not contain canonical truth and it is not where workflow state becomes authoritative.

### Required Content

**Context strip** — always visible:
- current system
- current workflow stage and next gate
- governing decision context loaded
- evidence loaded with freshness/trust posture
- active staleness or conflict warnings
- active continuity artifacts when materially relevant
- orchestration state summary when materially relevant
- tool-surface posture summary in bounded form

**Interaction/output area** — the primary content area of the panel for bounded interaction and lightweight typed output review.
Each output must appear as a distinct typed card or equivalent bounded structure showing:
- output type label
- system attribution where relevant
- action class badge where relevant
- orchestration/delegation attribution where relevant
- response options where appropriate

**Operator input** — text input for framing and directing work.
Not a general chat box.
Not where governance happens.

### Right Panel Limits

The right panel must not:
- contain the primary navigation tree
- become the canonical record browser
- allow prose in the input area to substitute for an approval event
- render LLM output in a way that obscures output type, orchestration involvement, or continuity involvement
- expand by default into the sole full-work surface
- contain Class B or Class C activation controls

The interaction surface is secondary by design. It supports work that lives in the left panel and center workspace. It must not become the primary operating surface.

---

## Center Workspace and Detail Surfaces

### Role
Dense read-mostly inspection and review surfaces for specific records, packages, reviews, transcript/audit artifacts, and continuity-heavy review work. These are where the operator reviews a full record, an evidence chain, a handoff package, a launch readiness assessment, or an approval request package with enough context to make an informed decision.

### Opening Detail Views

Center detail/review views open when the operator:
- clicks a record in the left panel tree
- clicks a detail link from a typed LLM output
- explicitly navigates to a detail view through an allowed command path

Detail views do not open automatically without operator action.

### Required Detail View Types

**Record Detail View**
For: Objective, Initiative, WorkItem, Handoff, Decision Record, ResearchDoc, EvidenceLink, ExternalLink, AuditRun, ReadinessEvaluation, and other governed records as relevant.

Content areas may include:
- overview
- evidence
- decisions
- history
- actions appropriate to the record type and current workflow stage

**Handoff Package Review View**
For reviewing a prepared handoff before the operator proceeds to the approval gate.

Content:
- what is being handed off
- approved scope
- out-of-scope items
- readiness basis
- governing decisions relevant to the handoff
- what transfers and what does not transfer
- evidence references with system attribution
- current workflow stage and gate status
- **handoff posture** — whether the handoff is in `Handoff — Prepared` state (package is complete but approval or release condition may still be pending) or `Handoff — Awaiting Approval` state (explicitly awaiting the operator approval event before activation). These are distinct states. `Handoff — Prepared` does not imply that activation may proceed. The operator must be able to determine from this view whether an approval event is still required and whether it has been satisfied.
- **stale basis warning** — if the handoff's planning basis, approval status, or evidence basis has changed materially since the package was prepared, this view must surface a visible warning before the approval gate is offered. A prepared or awaiting-approval handoff whose planning basis has been materially invalidated must not reach the approval gate without that condition being visible.

**Launch Readiness Review View**
For reviewing the cross-system launch readiness picture before seeking launch authorization.

Content:
- planning-side readiness
- evidence and signal review with attribution
- execution-side verification
- cross-system readiness confirmation
- blocking conditions if any
- required acknowledgment checkpoints
- **cross-system confirmation requirement** — this view must make visible whether all three confirmation dimensions (planning-side, evidence/signal, and execution-side verification) have been satisfied. A self-certification from any single system is not a governed cross-system confirmation. The operator must be able to see, in this view, which dimensions are confirmed and which remain open before the launch authorization gate is offered.
- **post-launch state transition** — after launch authorization is granted and launch-sensitive execution completes, the workflow stage must transition to `Post-Launch — Active`. This view must not imply that entering post-launch is automatic or that it dissolves governance boundaries. Post-launch findings that require planning reconsideration route through the maintenance and replanning workflow.

**Return Trigger Review View**
For reviewing a V Forge execution finding that has been routed to Project V.

Content:
- what was found in execution
- why it was routed to planning
- execution state at the point of halting
- what the finding is NOT doing
- response options through the governed path
- **maintenance vs replanning routing** — this view must help the operator determine whether the finding warrants replanning (a governed reconsideration of prior planning decisions) or can be resolved within existing approved scope as maintenance activity. The view must surface enough context for that determination, and the response options must distinguish between routing the finding to planning for replanning consideration versus acknowledging it as a maintenance-level finding that does not require formal replanning. The view must not flatten these two outcomes into a single undifferentiated `route to planning` action.

**Transcript / Audit Review View**
For reviewing transcript artifacts, orchestration event logs, or continuity-support traces without mistaking them for canonical state.

Content:
- transcript or event chronology
- source attribution
- compact-boundary markers where present
- orchestration event sequence where present
- prominent non-authority labeling

This view exists for reviewability and debugging, not as a substitute for governed records.

---

## Lower Trace / Log / Orchestration Surface

### Role
Optional secondary runtime-visibility surface for material runtime traces, orchestration detail, task progression, delegated-task outcomes, compact-boundary markers, and failure diagnostics where needed.

This surface exists to keep runtime power visible enough for accountability without forcing every operator to live inside logs all the time.

### Allowed Content
- orchestration task states
- delegated-task progression
- failure details where review is needed
- transcript/tracing references
- compact-boundary notices where deeper review is appropriate
- runtime event chronology where materially relevant

### Lower Surface Anti-Affordance Rules
The lower trace surface must not become:
- the primary review surface for governed records
- the sole place where workflow meaning is visible
- a substitute for approval gates
- an excuse for hidden runtime behavior elsewhere

Runtime visibility belongs here when materially relevant. Runtime authority does not.

---

## Status Indicators, Badges, and Context Markers

### Top-Level Status Indicators

The shell must keep session and scope posture visible.

It must be possible to show:
- current project scope state
- healthy/degraded/broken session posture
- unresolved session integrity items
- critical pending items requiring attention

### Context Strip in Right Panel

Always visible in the right panel. Synchronized with left panel state and center review posture. Cannot be treated as optional for governance-significant work.

It must be capable of surfacing:
- decision and evidence context
- orchestration summary
- continuity summary
- tool-surface posture summary
- staleness/conflict warnings

### Compact-Boundary and Refresh Notices

When the runtime materially refreshes session basis, performs compaction, or changes the admitted continuity set, the operator must receive a visible inline notice in the interaction surface and any affected center review surface.

These notices should identify:
- what changed
- why it changed
- what remained protected
- whether review is recommended before continuing

---

## Gate and Approval Surfaces

Approval surfaces are distinct from review surfaces. They are where persisted approval events are created, not where records are merely inspected.

### Review-Before-Gate Routing Rule

The path from a typed LLM output to a completed approval event is always:

1. The LLM produces an Approval Request Package in the right interaction panel.
2. The operator selects `[Proceed to Approval Gate]` on the output card — this navigates the operator into the relevant center workspace detail/review surface.
3. The operator reviews the record, package, evidence, and relevant context in that center surface.
4. The gate widget (Class B inline widget or Class C modal) becomes available only after the operator is inside the center review surface and has completed any required review steps.
5. The operator uses the gate widget to create the persisted approval record.
6. Activation may then proceed via the governed API path.

The approval gate widget must not appear in the right interaction panel, the left navigation panel, or the topbar. The operator must navigate to the center workspace before the gate is reachable. There is no shortcut path from right-panel output to approval completion.

This routing is not cosmetic. Requiring the operator to be in the center review surface before the gate appears ensures they are working with the full record context at the moment of approval — not a compressed summary in the interaction panel.

### Class B Approval — Inline Gate Widget

Embedded within the relevant center review surface, not in the left panel, right panel, or topbar.

Components:
- approval request summary
- action class badge
- approve control that writes the approval record and then enables downstream activation through the proper path
- reject control that persists a rejection record where applicable
- defer control where appropriate

### Class C Approval — Modal Gate

For launch-sensitive, external, paid, and irreversible actions.

Triggered only after the operator has opened the relevant center review surface, completed all required review and acknowledgment checkpoints within it, and explicitly initiated the authorization. The modal must not fire from the right interaction panel. The operator must be inside the center review surface and have completed all checkpoints before the modal is offered.

Modal components:
- action being authorized
- what happens if authorized
- what does NOT change
- typed confirmation input where required
- confirm authorization control
- cancel control

### Escalation Surface

When a Class D condition is detected, the desktop application presents a non-dismissible inline banner in the relevant surface:

```text
⛔ ESCALATION REQUIRED
[What the issue is]
[What action is blocked]
[What decision or clarification is needed]
[Escalate] [Document and Hold]
```

No dismiss option.
No proceed anyway path.

---

## Notifications and Alerts

Notifications are scaled to governance importance.

### Attention Badges / Indicators
Use for:
- pending approval count
- unreviewed return trigger count
- critical gap count
- session or runtime errors requiring attention

### Topbar or Persistent Warning State
Use for:
- session token or scope issues
- runtime connection issues
- stale context categories where the operator must remain aware

### Inline Banner
Use for:
- context changes during a session
- decision supersession
- evidence staleness
- workflow-stage changes
- compaction/refresh events
- delegated-task failure that affects review

### In-App or OS Notification
Use for:
- session integrity items at session start
- successful persisted approval events where confirmation is appropriate
- return trigger received from V Forge
- notable but non-blocking runtime refresh events

### Blocking Modal
Use for:
- Class C typed confirmation gates only

---

## Action Placement Rules

### Actions that belong only in Project V surfaces
- create Objective / Initiative / WorkItem through the governed path
- transition planning record status through the governed path
- evaluate readiness
- create or review Decision Record
- initiate intake classification
- prepare handoff package
- route return trigger to planning

### Actions that belong only in VEDA surfaces
- configure observatory scope
- initiate paid data pull approval request
- review signal package
- access observatory event log or equivalent review surface

### Actions that belong only in V Forge surfaces
- view execution state and content graph
- route return trigger from V Forge to Project V
- initiate pre-launch verification review
- initiate launch authorization request

### Actions that belong only in gate surfaces
- approve a Class B action
- authorize a Class C action
- reject an approval request
- escalate a Class D condition

### Actions available across all system surfaces
- navigate to detail
- copy record ID or context for bounded use
- open session integrity view
- switch project scope
- open bounded global commands where allowed
- run hammer verification where appropriate

### Actions that must NEVER appear in the following surfaces

**In the VEDA navigation view:**
- create Planning Record
- approve handoff
- configure V Forge execution
- activate any Class B or Class C action

**In the V Forge navigation view:**
- create Planning Record
- modify governing decisions
- configure observatory scope
- approve or activate anything without routing through the proper gate

**In the right interaction panel:**
- any Class B or Class C action activation
- any action that creates a record without routing through the governed path
- any control labeled Approve or Authorize that substitutes for the persisted approval event

**In the topbar:**
- any mutation action
- any approval action
- any action that appears to govern state

**In the lower trace/orchestration surface:**
- approval controls
- hidden mutation actions
- canonical record editing controls

---

## LLM Surface Limits

The right interaction panel must not become:

**The source of canonical state.**

**The place where approvals happen by prose.**

**The sole place where cross-system context is understood.**

**The only place where workflow meaning is visible.**

**The place where orchestration disappears into invisible magic.**
When orchestration matters, the panel must surface that fact.

**The place where continuity becomes a shadow database.**
Continuity artifacts shown in the panel must remain visibly non-canonical.

**The place where system boundaries become flexible.**
The current system shown in the context strip governs the LLM's output posture and does not change because the conversation topic shifted.

---

## Surface Synchronization

The operator must not be looking at mismatched realities across surfaces.

This section defines the surface-layer synchronization requirements that apply when invalidation and refresh events fire. The canonical event definitions, affected state categories, blocking posture, and sequencing priority for each event are defined in `desktop-invalidation-and-refresh-matrix.md`. This section specifies what must happen at the surface layer — it does not define the events themselves and must not be read as a competing event-to-consequence mapping.

### Synchronization requirements

When a persisted approval event is written: the left navigation tree refreshes, top-level status indicators update, the context strip in the right panel updates, and the center detail surface for the approved record refreshes.

When a governing decision is created, superseded, or invalidated: the context strip updates immediately, an inline banner appears in any open center review surface that referenced the affected decision, and any pending LLM output cards that cited the affected decision receive a staleness marker.

When a return trigger arrives from V Forge: the V Forge navigation view shows the trigger prominently, top-level attention indicators update, and an in-app notification may fire.

When the session token expires or runtime scope is broken: the top-level session state becomes degraded, all Class B and C actions are blocked across all surfaces, and the right-panel context strip shows the session error posture.

When context is refreshed after a staleness or invalidation condition: the context strip, the relevant center review surfaces, and any affected LLM output cards receive a refresh marker.

When a meaningful delegated task completes, fails, or is cancelled: the orchestration summary in the right panel refreshes, and any affected center or lower-trace surfaces reflect the change.

When a prior approval is superseded or invalidated: the center detail surface for the affected record receives an inline banner stating that the prior approval is no longer valid. The session integrity indicator in the topbar updates to show an unresolved integrity item. The context strip reflects the changed stage or blocking condition. Any rendered LLM output cards in the right panel that assumed the invalidated approval was a completed gate receive a staleness marker: `⚠ BASIS CHANGED — prior approval for [record] has been invalidated. Re-evaluate this output.` This propagation is distinct from the approval-written case above and must be handled as a separate synchronization event.

When local support-state diverges from backend canonical state: the topbar session integrity indicator updates immediately. Any context strip category whose current value was sourced from local state rather than a confirmed backend load is annotated with a divergence marker. The operator is notified before any Class B or C gate is presented while divergence is unresolved.

### Conflict between surfaces

If any surface appears to show state inconsistent with another, the desktop application treats this as a synchronization error, surfaces a banner or integrity notice, and prompts a refresh or reload posture before governance-sensitive work proceeds.

Synchronization errors are not silent.

---

## Keeping the Desktop Application Actually Usable

The architecture must not be so governed that operators route around it.

Class A analytical work should remain lightweight.
Mode selection is only required when the operator wants typed bounded outputs that have governance significance.

Center detail/review views are opened on demand. The shell does not force detail into view unsolicited.

Top-level attention indicators show what requires attention, not a count of everything that has happened.

Approval gates appear in center review surfaces where the review context already exists.

Modals appear only for Class C irreversible or high-consequence actions.

Runtime power features such as orchestration, continuity, and compaction must become visible enough for accountability without turning every interaction into a cockpit full of blinking nonsense.

---

## Human-In-The-Loop Principle

The surface architecture physically instantiates human-in-the-loop control.

The left navigation panel makes system state visible without requiring the LLM. The center workspace makes review possible before the approval gate is reached. The approval gates require explicit deliberate action and produce persisted records. The topbar makes current scope and session posture impossible to overlook. The absent-affordance rules prevent the wrong action from appearing in the wrong place. The runtime-visibility surfaces keep orchestration and continuity visible enough that the operator is never reviewing an illusion.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the LLM interaction surface is the right panel, not the primary operating surface
- canonical state is in navigation and detail/review surfaces, not in the LLM output area
- approval events happen in gate surfaces embedded in center review surfaces or in Class C modals, not in the interaction panel
- the current system shown in the context strip governs the LLM's output posture and does not change because the conversation topic shifted
- producing a typed output card in the interaction panel does not activate anything
- orchestration and continuity must remain visible when materially relevant
- the operator does not depend on the LLM to understand what requires attention

If the LLM treats the right interaction panel as the authoritative system surface or assumes that producing an approval request package in the panel is the same as the operator using the approval gate in a center review surface, the surface architecture is being misread.

---

## Usage

This document should be used:

- when designing the desktop application's shell layout and primary surfaces
- when deciding where to place a new action, command, or surface element
- when evaluating whether a proposed UX change maintains absent-affordance rules
- when reviewing whether a surface is taking on responsibilities that belong to another surface category
- when deciding whether a new notification, alert, or badge is appropriately scaled to governance importance
- when designing synchronization behavior between surfaces
- as the physical desktop architecture reference that later implementation and UX work is bounded by
- when evaluating whether a new synchronization event needs to be added to `desktop-invalidation-and-refresh-matrix.md`

---

## Related Docs

- `runtime-sidecar-and-nerve-model.md`
- `local-first-architecture.md`
- `desktop-llm-behavior-contract.md` or successor naming
- `desktop-governance-and-gating-model.md` or successor naming
- `desktop-state-and-context-model.md` or successor naming
- `desktop-human-llm-interaction-model.md` or successor naming
- `desktop-agent-orchestration-model.md` or successor naming
- `desktop-memory-and-continuity-model.md` or successor naming
- `desktop-system-init-and-tool-surface-model.md` or successor naming
- `../governance/approval-and-escalation-model.md`
- `../governance/recommendation-packaging-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
- `operator-surface-interfaces.md`
- `mcp-coordination-model.md`
- `../workflows/handoff-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../ux/desktop/direction/desktop-host-migration-plan.md`
- `desktop-invalidation-and-refresh-matrix.md`
