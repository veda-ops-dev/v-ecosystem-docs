# Extension VS Code Surface Architecture

## Purpose

This document defines the VS Code surface architecture for the V Ecosystem extension — the physical layout of surfaces, the placement of actions, the assignment of content to surfaces, and the absent-affordance rules that prevent the wrong actions from appearing in the wrong places.

It exists to answer:

```text
What are the primary extension surfaces, what is each one for, what belongs where, what must never appear in certain places, and how does the surface architecture physically embody the behavior, governance, state/context, and interaction doctrines already established?
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
- the absent-affordance rules that enforce system boundaries by what is not present
- the LLM surface limits that prevent the interaction panel from becoming the real system
- surface synchronization requirements

This document builds on and assumes the active binding of:
- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-state-and-context-model.md`
- `extension-human-llm-interaction-model.md`

---

## Out of Scope

This document does not define:

- specific visual styling, color tokens, or pixel dimensions
- exact VSCode API method calls or implementation patterns
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
Show the operator where they are, what is active, what is blocked, and what requires attention. Always visible. Never contain mutation actions.

**VS Code surfaces:** Primary sidebar views, status bar items, activity bar badge.

### 2. Interaction Surfaces
The LLM interaction panel where the operator frames work and the LLM produces typed bounded outputs. Supports the system. Does not replace it.

**VS Code surfaces:** Secondary sidebar webview (LLM panel).

### 3. Detail and Review Surfaces
Rich read-mostly surfaces for inspecting records, evidence, decisions, handoff packages, launch readiness assessments, and approval request packages. Open on demand. Support dense review work without cluttering navigation surfaces.

**VS Code surfaces:** Editor-area webview panels opened on demand.

### 4. Gate and Approval Surfaces
Surfaces specifically for approval events, typed confirmations, and escalation flows. These are where persisted approval events are created or rejected. Distinct from review surfaces.

**VS Code surfaces:** Modal dialogs for Class C actions and irreversible confirmations; inline approval widgets embedded in Detail surfaces for Class B actions.

### 5. Alert and Notification Surfaces
Transient or persistent surfaces for session integrity warnings, decision context changes, evidence staleness notices, and governance-sensitive interruptions. Scaled to importance — not every notice is a modal.

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

Status badges per tree item: `proposed`, `active`, `blocked`, `ready`, `handed_off`, `accepted`, `closed`. Colors must be consistent and semantically meaningful, not decorative.

Actions available in this view:
- navigate to detail panel for any record
- trigger readiness evaluation (opens framed LLM interaction or direct API call where appropriate)
- create planning record (Objective / Initiative / WorkItem) via command
- transition status via context menu (routes through governed transition with required reason where doctrine mandates it)
- initiate intake via explicit command

Actions NOT available in this view:
- approve or activate handoffs (those happen in detail panels with the appropriate gate surface)
- access VEDA signal packages directly
- configure observatory scope
- view or launch execution state

**View 2: VEDA — Observatory**

Content:
- Observatory domains (keyword targets, SERP snapshots, GA4, Search Console, YouTube) — collapsible sections with record counts and freshness indicators
- Signal packages ready for consumption — labeled with target system (Project V or V Forge)
- Provider status — green/amber/red per integration

Actions available in this view:
- navigate to detail panel for observatory records
- view signal package contents in detail panel
- configure observatory scope within governed operator bounds (requires explicit operator action, not LLM initiation)
- initiate paid data pull approval request (routes to approval gate — does not activate spend directly)

Actions NOT available in this view:
- create or modify Project V planning records
- initiate or approve V Forge execution
- produce planning recommendations from VEDA signal directly (that belongs in LLM interaction surface with explicit framing)

**View 3: V Forge — Execution**

Content:
- Active execution items with status and stage indicators
- Content graph summary (page count, topic count, last updated)
- Return triggers — prominently shown when present, not buried
- Recent execution reports

Actions available in this view:
- navigate to execution detail in detail panel
- route return trigger to Project V (through governed interface)
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
- any action that crosses system ownership (e.g., a "send to V Forge" button inside the VEDA view)
- any LLM prompt input field or mode selector
- any action labeled ambiguously enough to be confused with approval (e.g., "confirm," "proceed," "finalize" without explicit governance framing)

The sidebar navigates and shows. It does not govern.

---

## Secondary Sidebar

### Role
Interaction surface. The LLM interaction panel lives here. The operator frames work, the LLM produces typed bounded outputs, and the operator reviews and responds through defined response options. This surface supports the system. It does not contain system truth and it is not where workflow state is authoritative.

### Required Content

**Mode selector** — visible at the top of the LLM panel. The operator selects the interaction mode before the LLM produces typed bounded outputs. Mode options: Brainstorm, Review, Intake, Recommendation Packaging, Approval Request Preparation, Execution Report Review. This selector is a framing signal, not an authority class. It does not unlock actions or override gates.

**Context strip** — below the mode selector, always visible:
- Current system (Project V / VEDA / V Forge)
- Current workflow stage and next gate
- Decision context: governing decisions loaded (names, not count)
- Evidence loaded: record identifiers with freshness and trust posture
- Any active staleness or conflict warnings

This strip mirrors the state defined in `extension-state-and-context-model.md`. The LLM panel cannot operate without it. If context is unavailable, the strip shows the unavailability explicitly and the LLM must not produce typed outputs that depend on missing context.

**LLM output area** — the primary content area. Each output appears as a distinct typed card:
- output type label at top of card (FINDING, RECOMMENDATION, REVIEW SUMMARY, APPROVAL REQUEST, EXECUTION REPORT, UNCERTAINTY, CONTINUITY REMINDER)
- system attribution where relevant
- action class badge for Recommendations and Approval Request Packages
- response option buttons at the bottom of each card

**Operator input** — at the bottom. Text input for framing and directing work. Not a general chat box. Not where governance happens.

### Secondary Sidebar Limits

The secondary sidebar must not:

- contain any primary navigation tree
- be the place where records are browsed or canonical state is inspected (that belongs in the primary sidebar or detail panels)
- allow prose in the input area to substitute for an approval event
- render LLM output in a way that obscures the output type
- allow the LLM panel to expand into a full-screen surface that replaces the primary sidebar

The LLM interaction surface is secondary by design. It supports the work that lives in the primary sidebar and detail panels. It must not become the primary operating surface.

---

## Detail and Review Surfaces (Editor-Area Panels)

### Role
Dense read-mostly inspection surfaces for specific records, packages, and reviews. Opened on demand. These are where the operator reviews a full record, an evidence chain, a handoff package, a launch readiness assessment, or an approval request package with enough context to make an informed decision.

Detail panels earn more screen space than a sidebar can provide. They are appropriate for work that requires reading and thinking, not for casual navigation.

### Opening Detail Panels

Detail panels open when the operator:
- clicks a record in the primary sidebar tree
- clicks "view details" on a typed LLM output card
- explicitly navigates to a detail view via command

Detail panels do not open automatically. The operator chooses to drill in.

### Required Detail Panel Types

**Record Detail Panel**
For: Objective, Initiative, WorkItem, Handoff, Decision Record, ResearchDoc, EvidenceLink, ExternalLink, AuditRun, ReadinessEvaluation.

Content tabs within panel:
- **Overview** — record fields, status, current readiness state, target system
- **Evidence** — linked evidence records with system attribution (VEDA-owned evidence labeled as such), freshness, trust posture
- **Decisions** — governing decision chain relevant to this record
- **History** — status history and transitions
- **Actions** — only the actions appropriate to this record type and current workflow stage; no cross-system actions

The Evidence tab must always show system attribution. Evidence from VEDA shown in a Project V record detail must carry the label `SOURCE: VEDA — Project V does not own this state`. This is not a tooltip. It is a persistent label on every evidence entry.

**Handoff Package Review Panel**
For: reviewing a prepared handoff before the operator proceeds to the approval gate.

Content:
- what is being handed off
- approved scope (explicit)
- out-of-scope items (explicit)
- readiness basis
- governing decisions relevant to the handoff
- what transfers (execution responsibility)
- what does NOT transfer (planning ownership)
- evidence references with system attribution
- current workflow stage and gate status

Actions available: `Proceed to Approval Gate`, `Route to LLM for Recommendation`, `Return to Planning`, `Defer`.

`Proceed to Approval Gate` does not activate the handoff. It opens the Class B approval gate for the handoff activation. The detail panel itself does not contain the approval event mechanism — it navigates to it.

**Launch Readiness Review Panel**
For: reviewing the cross-system launch readiness picture before seeking launch authorization.

Content (structured by workflow stage):
- Planning-side readiness (Project V)
- Evidence and signal review (VEDA signal referenced with system attribution)
- Execution-side verification (V Forge)
- Cross-system readiness confirmation
- Blocking conditions if any

Acknowledgment checkboxes — one per material item:
- "I have reviewed planning-side readiness"
- "I have reviewed the VEDA signal advisory"
- "I have reviewed execution-side verification"
- "I acknowledge any unresolved advisory conditions"

The Class C launch authorization gate button is grayed out until all applicable acknowledgment checkboxes are checked. The gate widget appears within this panel, not in the sidebar or the LLM surface.

**Return Trigger Review Panel**
For: reviewing a V Forge execution finding that has been routed to Project V.

Content:
- what was found in V Forge execution
- why it was routed to planning
- current V Forge execution state at the point of halting
- what the finding is NOT doing (not deciding replanning, not authorizing scope change)
- response options: Route to governed return-to-planning path / Dismiss with acknowledged execution risk

This panel must explicitly state what has not happened: "No planning reconsideration has been initiated. No governing decisions have changed. No execution scope has been altered." This is not a warning — it is a factual status statement that must be visible before the operator acts.

---

## Status Bar, Context Strip, and Badges

### Status Bar Items

The extension contributes two status bar items. Both are always visible when the extension is active.

**Project scope item** (left side):
```
◈ V: [project-name]
```
- Green when session is healthy and scoped
- Amber when no project is selected
- Red when session token is invalid or MCP connection is lost

Click behavior: opens project quick pick for session initialization or project switching.

On hover: shows session token age, MCP connection status, last successful API call timestamp.

**Session integrity item** (left side, adjacent to project scope):
- Shows badge count when there are unresolved session integrity items (pending approvals, unreviewed return triggers, stale readiness states)
- Click: opens session integrity panel or surfaces the integrity notice

### Activity Bar Badge

The extension's activity bar icon shows a badge count when any of the following exist:
- pending approval events that have not been completed
- unreviewed return triggers from V Forge
- critical-severity gaps in the active project
- session errors or MCP connection failures

The badge is a governance signal, not a notification count. It tells the operator that something requiring attention exists. It does not try to summarize that something.

### Context Strip in Secondary Sidebar

Defined fully in `extension-state-and-context-model.md`. Always visible in the secondary sidebar. Synchronized with primary sidebar state. Cannot be collapsed.

---

## Gate and Approval Surfaces

Approval surfaces are distinct from review surfaces. They are where persisted approval events are created, not where records are inspected.

### Class B Approval — Inline Gate Widget

Embedded within the relevant detail panel, not in the sidebar or the LLM surface.

Components:
- Approval request summary (what is being approved, scope, what approval covers, what it does not)
- Action class badge: `Class B`
- `[Approve]` button — calls the approval event API, writes the approval record, then enables downstream activation
- `[Reject — with reason]` button — opens a brief text input; persists a rejection record
- `[Defer]` — logs a deferred state; does not write an approval or rejection record

`[Approve]` is not a checkbox. It is not a dismiss. It is an explicit API call that writes to the database before anything downstream is permitted.

### Class C Approval — Modal Gate

For launch-sensitive, external, paid, and irreversible actions.

Triggered after the operator completes all acknowledgment checkboxes in the relevant detail panel.

Modal components:
- Action being authorized (specific, not vague)
- What happens if authorized
- What does NOT change as a result of authorization (system ownership stays intact)
- Typed confirmation input: requires the operator to type a specific phrase (e.g., `AUTHORIZE LAUNCH`)
- `[Confirm Authorization]` — only enabled after the typed phrase is correctly entered; writes the approval record and persists it before downstream activation proceeds
- `[Cancel]` — closes modal; no record written

The typed phrase is not a password. It is a deliberate cognitive engagement requirement. The operator must stop and actively decide. A modal they can click through in under a second is not a sufficient gate for an irreversible action.

### Escalation Surface

When a Class D condition is detected, the extension presents a non-dismissible inline banner in the relevant surface:

```
⛔ ESCALATION REQUIRED
[What the issue is]
[What action is blocked]
[What decision or clarification is needed]
[Escalate] [Document and Hold]
```

`[Escalate]` routes to the governed escalation path and persists an escalation record.
`[Document and Hold]` creates a persisted hold record with the issue documented. The blocked action remains blocked.

No "dismiss" option. No "proceed anyway." An escalation condition must be resolved or held — not dismissed.

---

## Notifications and Alerts

Notifications are scaled to governance importance. Not every event warrants a modal. Modals are reserved for conditions where the operator cannot safely proceed without addressing the notice.

### Activity Bar Badge
Use for: pending approval count, unreviewed return trigger count, critical gap count, session error.

### Status Bar Warning
Use for: MCP connection issues, expired session token, stale context categories.

### Inline Panel Banner
Use for: context changes during a session (decision superseded, evidence stale, workflow stage changed), conflict detected in governing decisions, recommendation basis potentially affected by changed context.

Inline banners appear inside the relevant panel or sidebar view. They are not disruptive to the operator's current focus. They are visible and require acknowledgment before the affected surface is used for approval-sensitive work.

### VS Code Notification (bottom-right)
Use for: session integrity items at session start, successful persisted approval events, return trigger received from V Forge.

These are informational. They do not block work.

### Blocking Modal
Use for: Class C typed confirmation gates only. No other surface warrants a blocking modal under normal operation.

Blocking modals for non-Class-C conditions are a UX failure — they train operators to dismiss without reading.

---

## Action Placement Rules

This section defines where actions belong and where they must not appear.

### Actions that belong only in Project V surfaces
- Create Objective / Initiative / WorkItem
- Transition planning record status
- Evaluate readiness
- Create or review Decision Record
- Initiate intake classification
- Prepare handoff package
- Route return trigger to planning
- Open project-intake workflow

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
- Approve a Class B action (inline gate widget in detail panel)
- Authorize a Class C action (modal gate after detail panel acknowledgment)
- Reject an approval request (inline rejection with reason)
- Escalate a Class D condition

### Actions available across all system surfaces
- Navigate to project detail
- Copy record ID or context for LLM use
- Open session integrity notice
- Switch project scope (initiates new session — not a silent context change)
- Open command palette
- Run hammer verification (task runner)

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
- Any Class B or C action activation (the LLM surface contains the Approval Request Package output; the gate widget lives in the detail panel, not in the LLM output card)
- Any action that creates a record without routing through the governed command
- Any button labeled "Approve" or "Authorize" that substitutes for the persisted approval event

**In the status bar:**
- Any mutation action
- Any approval action
- Any action that appears to govern state

The status bar shows state. It does not change state.

---

## LLM Surface Limits

The secondary sidebar LLM panel must not become:

**The source of canonical state.** Records browsed in the LLM panel context strip are read-only loaded context. The LLM panel does not mutate records. Canonical state lives in governed records accessible through the primary sidebar and detail panels.

**The place where approvals happen by prose.** No approval event is created because an operator typed "approved" or "yes" in the LLM input field. The LLM panel input field is a framing and direction surface. It has no API write path to approval records.

**The sole place where cross-system context is understood.** The primary sidebar shows system state for all three systems. The status strip shows current system. The context strip shows governing decisions and evidence. Cross-system context is visible outside the LLM panel. The operator does not need to ask the LLM what system they are in — the status strip tells them.

**The only place where workflow meaning is visible.** Workflow stage, next gate, blocking conditions, and pending approvals are visible in the primary sidebar trees and the status strip. The LLM panel may reference these in its outputs but it is not the authoritative display of workflow state.

**The place where system boundaries become flexible.** The current system shown in the context strip governs the LLM's output posture. The LLM panel does not silently switch that current system because the operator asked about a different system's topic. The current system is a persistent explicit state that the operator changes deliberately, not a fluid inference.

---

## Surface Synchronization

The operator must not be looking at mismatched realities across surfaces.

### Synchronization requirements

When a persisted approval event is written: the primary sidebar tree refreshes, the status strip updates, the context strip in the LLM panel updates, and the detail panel that was open for the approved record refreshes.

When a governing decision is created, superseded, or invalidated: the context strip in the LLM panel updates immediately, an inline banner appears in any open detail panel that referenced the affected decision, and any pending Recommendation output cards that cited the affected decision receive a staleness marker.

When a return trigger arrives from V Forge: the V Forge sidebar view shows the trigger prominently, the activity bar badge increments, and a VS Code notification fires. The operator sees the trigger in three places. They cannot miss it through normal extension use.

When the session token expires: the status bar item turns red, all Class B and C actions are blocked across all surfaces, and the LLM context strip shows the session error state. The operator cannot proceed with governance-sensitive work until re-initialization.

When context is refreshed after a staleness condition: the context strip, the relevant detail panel tabs, and any LLM output cards that cited the stale context receive a refresh marker.

### Conflict between surfaces

If any surface appears to show state inconsistent with another — for example, the primary sidebar shows a handoff as `active` but the context strip shows it as `awaiting_approval` — the extension treats this as a synchronization error, surfaces a banner notification, and prompts a reload before governance-sensitive work proceeds.

Synchronization errors are not silent. The operator must see them.

---

## Keeping the Extension Actually Usable

The architecture must not be so governed that operators route around it.

Class A analytical work — asking the LLM to interpret context, summarizing a record, reviewing decision history — requires no special ceremony. The operator navigates in the primary sidebar, selects a record, the detail panel opens, they ask the LLM for a Review Summary. Two actions.

The LLM mode selector is required only when the operator wants typed bounded outputs that have governance significance. For pure exploration and analysis, mode selection is optional and defaults to an appropriate analytical posture.

Detail panels are opened on demand. The sidebar does not push detail into the operator's view unsolicited.

The activity bar badge only shows what requires attention, not a count of everything that has happened. An operator who sees a badge knows something needs them. An operator who sees no badge can focus on their current work.

Approval gates appear in detail panels where the review context already exists. The operator does not navigate to a separate "approval console." They read the record, form a view, and the gate is right there below what they reviewed. This reduces the cognitive distance between review and decision without collapsing them into the same action.

Modals appear only for Class C irreversible actions. For everything else, inline banners and panel-embedded gates preserve context without interruption.

---

## Human-In-The-Loop Principle

The surface architecture physically instantiates human-in-the-loop control.

The primary sidebar makes system state visible without requiring the LLM. The detail panels make review possible before the approval gate is reached. The approval gates require explicit deliberate action and produce persisted records. The status strip makes current context impossible to overlook. The absent-affordance rules prevent the wrong action from appearing in the wrong place.

The operator's governance role is not enforced only by policy. It is enforced by what the surfaces allow and what they do not allow. A surface that shows the right things and hides the wrong things teaches the operator correct habits without requiring them to memorize a governance document.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the LLM interaction surface is the secondary sidebar, not the primary operating surface
- canonical state is in the primary sidebar and detail panels, not in the LLM output area
- approval events happen in gate surfaces embedded in detail panels or in Class C modals, not in the LLM panel
- the current system shown in the context strip governs the LLM's output posture and does not change because the conversation topic shifted
- producing a typed output card in the LLM panel does not activate anything — activation requires the operator to use the gate surface in the appropriate detail panel
- the activity bar badge and status strip are visible to the operator independently of the LLM panel, which means the operator does not depend on the LLM to understand what requires attention

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
- `../governance/approval-and-escalation-model.md`
- `../governance/recommendation-packaging-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
- `../interfaces/operator-surface-interfaces.md`
- `../interfaces/mcp-coordination-model.md`
- `../workflows/handoff-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
