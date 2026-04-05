# Extension VS Code Surface Architecture

## Status
Superseded by `desktop-surface-architecture.md`

This document reflects the legacy VS Code extension host model.
The Tauri 2 desktop application defined in ADR-011 is now the primary operator host.
Use `desktop-surface-architecture.md` for active doctrine.

## Purpose

This document defines the VS Code surface architecture for the V Ecosystem extension — the physical layout of surfaces, the placement of actions, the assignment of content to surfaces, and the absent-affordance rules that prevent the wrong actions from appearing in the wrong places.

It exists to answer:

```text
What are the primary extension surfaces, what is each one for, what belongs where, what must never appear in certain places, and how does the surface architecture physically embody the behavior, governance, state/context, orchestration, continuity, and interaction doctrines already established?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the primary surface categories the extension uses
- the role and content rules for the primary sidebar
- the role and content rules for the secondary sidebar
- the role and content rules for detail panels in the editor area
- the role and content rules for status strips, context strips, badges, notifications, and modals
- the placement of actions and commands by surface
- the visible placement of orchestration state, continuity state, compact-boundary state, and tool-surface posture
- the absent-affordance rules that enforce system boundaries by what is not present
- the LLM surface limits that prevent the interaction panel from becoming the real system
- surface synchronization requirements

This document builds on and assumes the active binding of:
- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-state-and-context-model.md`
- `extension-human-llm-interaction-model.md`
- `extension-agent-orchestration-model.md`
- `extension-memory-and-continuity-model.md`
- `extension-system-init-and-tool-surface-model.md`

---

## Out of Scope

This document does not define:

- specific visual styling, color tokens, or pixel dimensions
- exact VS Code API method calls or implementation patterns
- MCP server protocol details
- database schema or API endpoint design
- full command palette catalog (that belongs in an implementation doc)

The architecture must be concrete enough to constrain later implementation choices without specifying every implementation detail.

---

## System

- interfaces

---

## Core Rule

The surface architecture physically embodies doctrine.

Governance is not only what the system says it will do. It is what the system makes possible and what it makes impossible through surface design. A surface that contains the wrong actions teaches the operator to expect those actions. A surface that is missing actions that should not be there enforces the boundary silently and correctly.

The extension has five surface categories. Each has a defined role. Content and actions must be placed in the surface that matches their role. Content placed in the wrong surface is not a cosmetic choice — it is a doctrine failure.

---

## Surface Categories

The extension uses five surface categories:

### 1. Navigation and State Surfaces
Show the operator where they are, what is active, what is blocked, what requires attention, and what runtime posture is currently in effect. Always visible. Never contain mutation actions.

**VS Code surfaces:** Primary sidebar views, status bar items, activity bar badge.

### 2. Interaction Surfaces
The LLM interaction panel where the operator frames work and the LLM produces typed bounded outputs. Supports the system. Does not replace it.

**VS Code surfaces:** Secondary sidebar webview (LLM panel).

### 3. Detail and Review Surfaces
Rich read-mostly surfaces for inspecting records, evidence, decisions, handoff packages, launch readiness assessments, approval request packages, transcript/audit artifacts, and continuity detail where needed. Open on demand. Support dense review work without cluttering navigation surfaces.

**VS Code surfaces:** Editor-area webview panels opened on demand.

### 4. Gate and Approval Surfaces
Surfaces specifically for approval events, typed confirmations, and escalation flows. These are where persisted approval events are created or rejected. Distinct from review surfaces.

**VS Code surfaces:** Modal dialogs for Class C actions and irreversible confirmations; inline approval widgets embedded in Detail surfaces for Class B actions.

### 5. Alert and Notification Surfaces
Transient or persistent surfaces for session integrity warnings, decision context changes, evidence staleness notices, compaction/refresh notices, and governance-sensitive interruptions. Scaled to importance — not every notice is a modal.

**VS Code surfaces:** Status bar warnings, informational notifications, inline panel banners, session-start integrity notice, activity bar badge counts.

---

## Primary Sidebar

### Role
Navigation and state surface. The operator uses the primary sidebar to understand current project state across all three systems, navigate to specific records, and see what requires attention. The primary sidebar is not a chat surface and is not where approval gates live.

### View Container
One activity bar icon. One view container. Three views within it — one per system. Each view is labeled by system name and cannot be visually confused with another.

### Required Views

**View 1: Project V — Planning**

Content:
- Current project scope label (non-collapsible header)
- Objective tree (collapsible, badge count for blocked objectives)
- Initiative tree (collapsible, badge count for blocked and handed-off)
- Work items (collapsible, badge count for ready and blocked)
- Gaps section (collapsible, badge count by severity — critical shown first)
- Handoffs section (collapsible, status badges per handoff)

Status badges per tree item: `proposed`, `active`, `blocked`, `ready`, `handed_off`, `accepted`, `closed`.

Actions available in this view:
- navigate to detail panel for any record
- trigger readiness evaluation (opens framed LLM interaction or direct API call where appropriate)
- create planning record via governed command
- transition status via governed command path
- initiate intake via explicit command

Actions NOT available in this view:
- approve or activate handoffs
- access VEDA signal packages as if they were Project V-owned records
- configure observatory scope
- view or launch execution state as if this view owned it

**View 2: VEDA — Observatory**

Content:
- Observatory domains (keyword targets, SERP snapshots, GA4, Search Console, YouTube) — collapsible sections with record counts and freshness indicators
- Signal packages ready for consumption — labeled with target system (Project V or V Forge)
- Provider status — green/amber/red per integration

Actions available in this view:
- navigate to detail panel for observatory records
- view signal package contents in detail panel
- configure observatory scope within governed operator bounds
- initiate paid data pull approval request (routes to approval gate — does not activate spend directly)

Actions NOT available in this view:
- create or modify Project V planning records
- initiate or approve V Forge execution
- produce planning recommendations from VEDA signal directly inside the navigation surface

**View 3: V Forge — Execution**

Content:
- Active execution items with status and stage indicators
- Content graph summary (page count, topic count, last updated)
- Return triggers — prominently shown when present, not buried
- Recent execution reports

Actions available in this view:
- navigate to execution detail in detail panel
- route return trigger to Project V through the governed interface
- request pre-launch verification status in detail panel
- request launch authorization (routes to gate surface — does not activate launch directly)

Actions NOT available in this view:
- create or modify Project V planning records
- modify governing decisions
- access or configure VEDA observatory scope
- self-authorize any launch-sensitive action

### Primary Sidebar Anti-Affordance Rules

The primary sidebar must not contain:

- any approval button or approval gate widget
- any action that silently creates or modifies governed records without an explicit command plus confirmation
- any action that crosses system ownership as though ownership were local
- any LLM prompt input field or mode selector
- any action labeled ambiguously enough to be confused with approval

The sidebar navigates and shows. It does not govern.

---

## Secondary Sidebar

### Role
Interaction surface. The LLM interaction panel lives here. The operator frames work, the LLM produces typed bounded outputs, and the operator reviews and responds through defined response options. This surface supports the system. It does not contain system truth and it is not where workflow state is authoritative.

### Required Content

**Mode selector** — visible at the top of the LLM panel for governance-significant work.

**Context strip** — below the mode selector, always visible:
- Current system
- Current workflow stage and next gate
- Decision context: governing decisions loaded
- Evidence loaded: record identifiers with freshness and trust posture
- Any active staleness or conflict warnings
- Active continuity artifacts when materially relevant
- Orchestration state summary when materially relevant
- Tool-surface posture summary in bounded form

This strip mirrors the state defined in `extension-state-and-context-model.md`. The LLM panel cannot operate correctly without it.

**LLM output area** — the primary content area. Each output appears as a distinct typed card:
- output type label at top of card
- system attribution where relevant
- action class badge for Recommendations and Approval Request Packages
- orchestration/delegation attribution where relevant
- response option buttons at the bottom of each card

**Operator input** — at the bottom. Text input for framing and directing work. Not a general chat box. Not where governance happens.

### Secondary Sidebar Limits

The secondary sidebar must not:

- contain any primary navigation tree
- be the place where canonical records are browsed as authoritative detail
- allow prose in the input area to substitute for an approval event
- render LLM output in a way that obscures the output type, orchestration involvement, or continuity involvement
- allow the LLM panel to expand into a full-screen surface that replaces the primary sidebar
- contain Class B or C activation controls

The LLM interaction surface is secondary by design. It supports the work that lives in the primary sidebar and detail panels. It must not become the primary operating surface.

---

## Detail and Review Surfaces (Editor-Area Panels)

### Role
Dense read-mostly inspection surfaces for specific records, packages, reviews, transcript/audit artifacts, and continuity-heavy review work. Opened on demand. These are where the operator reviews a full record, an evidence chain, a handoff package, a launch readiness assessment, or an approval request package with enough context to make an informed decision.

### Opening Detail Panels

Detail panels open when the operator:
- clicks a record in the primary sidebar tree
- clicks a detail link on a typed LLM output card
- explicitly navigates to a detail view via command

Detail panels do not open automatically without operator action.

### Required Detail Panel Types

**Record Detail Panel**
For: Objective, Initiative, WorkItem, Handoff, Decision Record, ResearchDoc, EvidenceLink, ExternalLink, AuditRun, ReadinessEvaluation.

Content tabs within panel:
- **Overview** — record fields, status, current readiness state, target system
- **Evidence** — linked evidence records with system attribution, freshness, trust posture
- **Decisions** — governing decision chain relevant to this record
- **History** — status history and transitions
- **Actions** — only the actions appropriate to this record type and current workflow stage

**Handoff Package Review Panel**
For: reviewing a prepared handoff before the operator proceeds to the approval gate.

Content:
- what is being handed off
- approved scope
- out-of-scope items
- readiness basis
- governing decisions relevant to the handoff
- what transfers and what does not transfer
- evidence references with system attribution
- current workflow stage and gate status

**Launch Readiness Review Panel**
For: reviewing the cross-system launch readiness picture before seeking launch authorization.

Content:
- Planning-side readiness (Project V)
- Evidence and signal review (VEDA referenced with attribution)
- Execution-side verification (V Forge)
- Cross-system readiness confirmation
- Blocking conditions if any
- required acknowledgment checkpoints

**Return Trigger Review Panel**
For: reviewing a V Forge execution finding that has been routed to Project V.

Content:
- what was found in V Forge execution
- why it was routed to planning
- current V Forge execution state at the point of halting
- what the finding is NOT doing
- response options through the governed path

**Transcript / Audit Review Panel**
For: reviewing transcript artifacts, orchestration event logs, or continuity-support traces without mistaking them for canonical state.

Content:
- transcript or event chronology
- source attribution
- compact-boundary markers where present
- orchestration event sequence where present
- prominent non-authority labeling

This panel exists for reviewability and debugging, not as a substitute for governed records.

---

## Status Bar, Context Strip, and Badges

### Status Bar Items

The extension contributes two status bar items. Both are always visible when the extension is active.

**Project scope item**:
```text
◈ V: [project-name]
```
- Green when session is healthy and scoped
- Amber when no project is selected
- Red when session token is invalid or MCP connection is lost

**Session integrity item**:
- Shows badge count when there are unresolved session integrity items
- Click opens the session integrity surface

### Activity Bar Badge

The extension's activity bar icon shows a badge count when any of the following exist:
- pending approval events that have not been completed
- unreviewed return triggers from V Forge
- critical-severity gaps in the active project
- session errors or MCP connection failures

### Context Strip in Secondary Sidebar

Always visible in the secondary sidebar. Synchronized with primary sidebar state. Cannot be collapsed.
It must be capable of surfacing:
- decision and evidence context
- orchestration summary
- continuity summary
- tool-surface posture summary
- staleness/conflict warnings

### Compact-Boundary and Refresh Notices

When the runtime materially refreshes the session basis, performs compaction, or changes the admitted continuity set, the operator must receive a visible inline notice in the interaction surface and any affected detail surface.

These notices should identify:
- what changed
- why it changed
- what remained protected
- whether review is recommended before continuing

---

## Gate and Approval Surfaces

Approval surfaces are distinct from review surfaces. They are where persisted approval events are created, not where records are inspected.

### Class B Approval — Inline Gate Widget

Embedded within the relevant detail panel, not in the sidebar or the LLM surface.

Components:
- Approval request summary
- Action class badge: `Class B`
- `[Approve]` button — writes the approval record, then enables downstream activation
- `[Reject — with reason]` button — persists a rejection record
- `[Defer]` — logs deferred state only

### Class C Approval — Modal Gate

For launch-sensitive, external, paid, and irreversible actions.

Triggered after the operator completes all acknowledgment checkpoints in the relevant detail panel.

Modal components:
- action being authorized
- what happens if authorized
- what does NOT change
- typed confirmation input
- `[Confirm Authorization]`
- `[Cancel]`

### Escalation Surface

When a Class D condition is detected, the extension presents a non-dismissible inline banner in the relevant surface:

```text
⛔ ESCALATION REQUIRED
[What the issue is]
[What action is blocked]
[What decision or clarification is needed]
[Escalate] [Document and Hold]
```

No "dismiss" option. No "proceed anyway."

---

## Notifications and Alerts

Notifications are scaled to governance importance.

### Activity Bar Badge
Use for: pending approval count, unreviewed return trigger count, critical gap count, session error.

### Status Bar Warning
Use for: MCP connection issues, expired session token, stale context categories.

### Inline Panel Banner
Use for: context changes during a session, decision supersession, evidence staleness, workflow-stage change, compaction/refresh events, or delegated-task failure that affects review.

### VS Code Notification
Use for: session integrity items at session start, successful persisted approval events, return trigger received from V Forge, notable but non-blocking runtime refresh events.

### Blocking Modal
Use for: Class C typed confirmation gates only.

---

## Action Placement Rules

### Actions that belong only in Project V surfaces
- Create Objective / Initiative / WorkItem
- Transition planning record status
- Evaluate readiness
- Create or review Decision Record
- Initiate intake classification
- Prepare handoff package
- Route return trigger to planning

### Actions that belong only in VEDA surfaces
- Configure observatory scope
- Initiate paid data pull approval request
- Review signal package
- Access observatory event log

### Actions that belong only in V Forge surfaces
- View execution state and content graph
- Route return trigger from V Forge to Project V
- Initiate pre-launch verification review
- Initiate launch authorization request

### Actions that belong only in gate surfaces
- Approve a Class B action
- Authorize a Class C action
- Reject an approval request
- Escalate a Class D condition

### Actions available across all system surfaces
- Navigate to detail
- Copy record ID or context for LLM use
- Open session integrity notice
- Switch project scope
- Open command palette
- Run hammer verification

### Actions that must NEVER appear in the following surfaces

**In the VEDA sidebar view:**
- Create Planning Record
- Approve handoff
- Configure V Forge execution
- Activate any Class B or C action

**In the V Forge sidebar view:**
- Create Planning Record
- Modify governing decisions
- Configure observatory scope
- Approve or activate anything without routing through the proper gate

**In the secondary sidebar (LLM panel):**
- Any Class B or C action activation
- Any action that creates a record without routing through the governed command
- Any button labeled "Approve" or "Authorize" that substitutes for the persisted approval event

**In the status bar:**
- Any mutation action
- Any approval action
- Any action that appears to govern state

---

## LLM Surface Limits

The secondary sidebar LLM panel must not become:

**The source of canonical state.**

**The place where approvals happen by prose.**

**The sole place where cross-system context is understood.**

**The only place where workflow meaning is visible.**

**The place where orchestration disappears into invisible magic.**
When orchestration matters, the panel must surface that fact.

**The place where continuity becomes a shadow database.**
Continuity artifacts shown in the panel must remain visibly non-canonical.

**The place where system boundaries become flexible.**
The current system shown in the context strip governs the LLM's output posture.

---

## Surface Synchronization

The operator must not be looking at mismatched realities across surfaces.

### Synchronization requirements

When a persisted approval event is written: the primary sidebar tree refreshes, the status strip updates, the context strip in the LLM panel updates, and the detail panel for the approved record refreshes.

When a governing decision is created, superseded, or invalidated: the context strip updates immediately, an inline banner appears in any open detail panel that referenced the affected decision, and any pending Recommendation output cards that cited the affected decision receive a staleness marker.

When a return trigger arrives from V Forge: the V Forge sidebar view shows the trigger prominently, the activity bar badge increments, and a VS Code notification fires.

When the session token expires: the status bar item turns red, all Class B and C actions are blocked across all surfaces, and the LLM context strip shows the session error state.

When context is refreshed after a staleness or invalidation condition: the context strip, the relevant detail panel tabs, and any affected LLM output cards receive a refresh marker.

When a meaningful delegated task completes, fails, or is cancelled: the orchestration summary in the interaction surface refreshes, and any affected detail or transcript surfaces reflect the change.

### Conflict between surfaces

If any surface appears to show state inconsistent with another, the extension treats this as a synchronization error, surfaces a banner notification, and prompts a reload before governance-sensitive work proceeds.

Synchronization errors are not silent.

---

## Keeping the Extension Actually Usable

The architecture must not be so governed that operators route around it.

Class A analytical work should remain lightweight.
Mode selection is only required when the operator wants typed bounded outputs that have governance significance.

Detail panels are opened on demand. The sidebar does not push detail into the operator's view unsolicited.

The activity bar badge shows what requires attention, not a count of everything that has happened.

Approval gates appear in detail panels where the review context already exists.

Modals appear only for Class C irreversible actions.

Runtime power features such as orchestration, continuity, and compaction must become visible enough for accountability without turning every interaction into a cockpit full of blinking nonsense.

---

## Human-In-The-Loop Principle

The surface architecture physically instantiates human-in-the-loop control.

The primary sidebar makes system state visible without requiring the LLM. The detail panels make review possible before the approval gate is reached. The approval gates require explicit deliberate action and produce persisted records. The status strip makes current context impossible to overlook. The absent-affordance rules prevent the wrong action from appearing in the wrong place. The orchestration and continuity surfaces keep runtime power visible enough that the operator is never reviewing an illusion.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the LLM interaction surface is the secondary sidebar, not the primary operating surface
- canonical state is in the primary sidebar and detail panels, not in the LLM output area
- approval events happen in gate surfaces embedded in detail panels or in Class C modals, not in the LLM panel
- the current system shown in the context strip governs the LLM's output posture and does not change because the conversation topic shifted
- producing a typed output card in the LLM panel does not activate anything
- orchestration and continuity must remain visible when materially relevant
- the operator does not depend on the LLM to understand what requires attention

If the LLM treats the secondary sidebar as the authoritative system surface or assumes that producing an Approval Request Package in the LLM panel is the same as the operator using the approval gate in a detail panel, the surface architecture is being misread.

---

## Usage

This document should be used:

- when designing the extension's surface layout and view contribution points
- when deciding where to place a new action, command, or surface element
- when evaluating whether a proposed UX change maintains absent-affordance rules
- when reviewing whether a surface is taking on responsibilities that belong to another surface category
- when deciding whether a new notification, alert, or badge is appropriately scaled to governance importance
- when designing synchronization behavior between surfaces
- as the physical architecture reference that later implementation and UI work is bounded by

---

## Related Docs

- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-state-and-context-model.md`
- `extension-human-llm-interaction-model.md`
- `extension-agent-orchestration-model.md`
- `extension-memory-and-continuity-model.md`
- `extension-system-init-and-tool-surface-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/recommendation-packaging-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
- `../interfaces/operator-surface-interfaces.md`
- `../interfaces/mcp-coordination-model.md`
- `../workflows/handoff-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
