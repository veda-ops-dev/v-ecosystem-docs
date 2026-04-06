# V Ecosystem Desktop UX Work Plan

## Document Purpose

This is the active UX work plan for the V Ecosystem Tauri 2 desktop operator application.

It exists to answer:

```
What do we design, in what order, how long does each session take,
what must be true before each session starts, and what are we not designing yet?
```

This document replaces the previous phase-structure plan. That plan had the right items but wrong sequencing, inverted dependency order, and no honest accounting of schema-blocked work.

---

## Ground Rules (Non-Negotiable)

These are constraints, not preferences. Any session that violates them is wasted motion.

**Surface assignments are doctrine, not taste.**
The right panel is interaction and support. The center workspace is review and gates. The topbar and left nav are navigation and state. Nothing migrates between surfaces for convenience.

**No governance shortcuts in UX.**
Every workflow surface must expose the review-then-gate sequence. The LLM panel does not contain approval controls. No design decision may route around a gate.

**No schema fiction.**
Several workflow stages have no settled record anchor. Those surfaces do not get fully designed until the schema is settled. They get designed to the boundary of what is known and no further.

**One serious deliverable per session.**
A session that touches three things finishes none of them. Pick one item. Finish it. Move on.

**Doctrine is constraint, not the workstream.**
The doctrine docs define what must be true. This plan defines how to get there. If a design decision conflicts with doctrine, the doctrine wins.

---

## The Core Dependency Chain

Everything downstream depends on this chain being correct:

```
Output card system
  → Context strip
    → Right panel shell
      → Center workspace foundation
        → Approval gate surfaces
          → Review-to-gate routing
            → Workflow surfaces
```

Plus orthogonally:
```
Left nav shell (Project V tree)
  → Left nav VEDA tree
    → Left nav V Forge tree
```

And foundationally, running in parallel with item 1:
```
Minimal token decisions (spacing, type, color roles)
```

Violate this chain and you will design things twice.

---

## Schema-Blocked Items Tracker

Items marked **BLOCKED** must not be fully designed until the listed condition is met.
Design to the known boundary. Stop. Note what's missing. Come back when it's resolved.

| Item | Blocked On | Status |
|---|---|---|
| Intake UX | IntakeRecord / IntakeCandidate schema — no dedicated record type exists | **BLOCKED** |
| Launch Readiness UX (partial) | Three of four stage names are workflow-session-derived with no schema anchor: `Launch Readiness — In Progress`, `Launch Authorization — Pending`, `Post-Launch — Active` | **PARTIAL BLOCK** |
| Return Trigger UX (partial) | Maintenance-vs-replanning routing distinction — no `MaintenanceRecord` or `ReplanningRecord` schema exists | **PARTIAL BLOCK** |
| Maintenance / Ranking UX | Same as above — maintenance vs replanning stage derivation has no schema anchor | **PARTIAL BLOCK** |
| Decision Continuity Timeline | Design after decision record schema is fully stable | **HOLD** |
| Evidence Freshness / Signal Views | Design after VEDA signal interface schema is stable | **HOLD** |

---

## Active Work Plan

Sessions are sequenced by dependency order, not by architectural phase.
Each session has a single primary deliverable.
An `*` marks sessions with schema-partial status — these produce bounded deliverables that acknowledge their own limits.

---

### TIER 1 — Vocabulary and Tokens

#### Session 1 — Output Card System

**What this produces:**
The complete visual and interaction vocabulary for LLM typed outputs. Every workflow surface downstream contains these cards. This is the highest-leverage design session in the plan.

**Deliverable:**
Card templates for all seven output types with full required elements for each:
- **FINDING** — source system attribution, what was found, what was NOT done, operator response options
- **RECOMMENDATION** — `awaiting review` treatment, action class badge, proposed path, basis, uncertainty, acceptance/non-acceptance outcomes, Proceed to Approval Request CTA
- **REVIEW SUMMARY** — read-only label, no approval badge
- **APPROVAL REQUEST PACKAGE** — action class badge, `APPROVAL REQUEST — [Class B / Class C]` label, action, scope, basis, what approval covers, `[Proceed to Approval Gate]` CTA
- **EXECUTION REPORT** — V FORGE attribution, return trigger treatment (distinct embedded sub-card)
- **UNCERTAINTY NOTICE** — prominent warning treatment, what is uncertain, what would resolve it
- **CONTINUITY REMINDER** — non-blocking, non-canonical, prior-context reference

**Also in this session:**
- Action class badge design (Class A / B / C / D treatments)
- Staleness marker variants (seven types per the invalidation matrix)
- Inertness / "awaiting review" visual treatment
- Orchestration attribution label (when delegated work contributed to output)
- Continuity artifact attribution label (non-canonical)
- Referenced system ownership label (e.g., `REFERENCED FROM V FORGE — not owned by Project V`)

**Why first:**
Nothing downstream can be designed without knowing what a card looks like. Workflow surfaces, center workspace layouts, and gate flows all contain or reference cards. Getting this wrong means every subsequent session inherits the error.

**Not in this session:**
Shell layout, panel sizing, workflow logic, any surface outside the card itself.

---

#### Session 2 — Minimal Token Decisions

**What this produces:**
The minimum visual decisions needed to work consistently across subsequent sessions. Not a full design system. Not the Bricks adaptation. Just enough to stop making inconsistent choices.

**Deliverable:**
- Spacing scale (4-point or 8-point base, 4–5 steps minimum)
- Type scale (4–5 steps: body, label, caption, heading variants)
- Color roles (not hex values yet — role names: `surface.primary`, `surface.elevated`, `text.primary`, `text.secondary`, `state.warning`, `state.error`, `state.info`, `state.success`, `accent.primary`)
- 3–4 elevation/depth tokens (flat, raised, overlay, modal)
- Interaction state tokens (hover, active, disabled, focused)

**Why second:**
Sessions 3–24 all make visual decisions. Without shared tokens they'll all be inconsistent with each other. The token set doesn't need to be final — it needs to be consistent enough that later sessions build on it rather than starting from scratch.

**Not in this session:**
Bricks-specific visual adaptation, full component library, animation, final color palette.

---

### TIER 2 — Shell Backbone

#### Session 3 — Topbar

**What this produces:**
The topbar design, including all required states.

**Deliverable:**
- Project scope indicator (name, health state: active / warning / error)
- Current system indicator (Project V / VEDA / V Forge with distinct treatment)
- Session health/integrity state indicator
- Attention badge(s) for pending approvals, unreviewed return triggers, unresolved conflicts
- Empty states (no project selected)
- Error states (session token expired, runtime lost)

**Topbar must not contain:**
- Any mutation action
- Any approval control
- Any LLM input
- Any ambiguous action that could be confused with governance

**Why third:**
Topbar is the simplest surface, provides the outer frame reference for all subsequent surface designs, and establishes the persistent state visibility pattern every other surface anchors to.

---

#### Session 4 — Context Strip

**What this produces:**
The context strip design — the most doctrine-constrained element in the application. This lives in the right panel and must surface all nine state categories.

**Deliverable:**
Nine category rows, each with:
- Category label
- Current value or `Unavailable` state
- Freshness/trust markers where applicable
- Staleness warning treatment
- Conflict warning treatment
- Ownership label for referenced systems
- Expandable detail affordance where needed

The nine categories and their minimum visible information:

1. **SCOPE** — active project name, scope health
2. **SYSTEM** — current system with visual distinction; referenced systems with `[referenced, not owned]` label
3. **STAGE** — current stage name, next gate, blocking conditions (for stages with no schema anchor, show `Unavailable` if derivation fails)
4. **DECISIONS** — named list of active governing decisions (not count — names), staleness markers, conflict warnings
5. **EVIDENCE** — record identifiers, source, capture timestamp, trust posture, staleness markers
6. **INTEGRITY** — pending approvals, unreviewed return triggers, stale readiness states, unresolved conflicts, session health issues
7. **ORCH** — active orchestration summary, delegated task states (only when materially relevant)
8. **CONTINUITY** — active non-canonical artifacts, freshness markers, clearability (only when active)
9. **TOOLSURFACE** — current tool posture summary in bounded form

**Context strip must:**
- Always be visible in the right panel
- Remain synchronized with topbar and center surface state
- Show conflicts before they become blocking
- Never show counts alone for decisions or evidence — names or identifiers

**Why fourth:**
The context strip is contained in the right panel but it's designed before the right panel shell because the shell's sizing and layout depend on understanding what the context strip contains. Every workflow surface includes the right panel. Getting the context strip right early means every workflow session has the right primary reference surface.

---

#### Session 5 — Right Panel Shell and Operator Input

**What this produces:**
The right panel as a complete surface — context strip + interaction area + operator input + panel-level behaviors.

**Deliverable:**
- Panel overall layout (context strip above, interaction area in center, input at bottom)
- Interaction/output area (how cards are listed, scrolling, spacing)
- Operator input field (framing input, not a chat box)
- Mode selector (when and how it appears — required for Recommendation, Approval Request Package, Intake mode; optional/conversational for Review, Brainstorm, Execution Report Review)
- Panel width behavior (default width, resize constraints, collapse behavior)
- Panel-level states: empty/no project, loading, error/session broken

**Right panel must not:**
- Contain approval controls for Class B or C actions
- Become the primary navigation surface
- Allow output cards to substitute for center workspace review
- Show canonical records as though they are the record browser

**Why fifth:**
The shell wraps the context strip (just designed) and the output cards (Session 1). Both must exist before the shell can be designed. The right panel is the entry point for all operator-LLM interaction, so it must be stable before workflow surfaces reference it.

---

#### Session 6 — Left Nav Shell + Project V Tree

**What this produces:**
The left navigation shell and the Project V system's tree content.

**Deliverable:**
- Navigation shell (panel width, header, system switcher, scroll behavior)
- Project V tree structure:
  - Objective tree with status indicators
  - Initiative tree with status indicators
  - Work items
  - Gaps section with severity indicators (blocking / critical / warning)
  - Handoffs section with status: `proposed`, `active`, `blocked`, `ready`, `handed_off`, `accepted`, `closed`
  - Return trigger visibility (when a trigger exists and is unreviewed)
- Status indicator visual vocabulary for all recognized stage names
- Per-item action affordances (navigate to center surface; governed command path only — no inline approval)

**Project V left nav must not contain:**
- Approve or activate handoffs directly in the tree
- Configure observatory scope
- Launch execution actions
- Any LLM prompt input
- Any action that creates or mutates governed records without routing through the governed command path

**Note on intake:**
Intake-related navigation items exist but must reflect the schema-blocked status honestly. If intake stages cannot be derived from backend records, show `Unavailable` rather than a false-confident state label.

**Why sixth:**
Left nav content rules vary substantially per system. Project V has the most complex tree. Designing it first establishes the template that VEDA and V Forge trees refine. Shell must exist before system-specific trees.

---

#### Session 7 — Left Nav — VEDA Tree

**What this produces:**
The VEDA system's left nav content — distinct content rules and absent-affordances from Project V.

**Deliverable:**
- VEDA tree structure: observatory domains, provider sections, signal packages, provider freshness/health posture
- Groupings for ready signal packages vs. in-progress observation
- VEDA-specific absent-affordances clearly implemented:
  - No create/modify planning record controls
  - No execution actions
  - No approval controls in the tree
- Paid data pull approval request path — navigates to governed gate path, does not trigger in the tree directly

**Why seventh:**
Builds directly on the nav shell from Session 6. VEDA's content and absent-affordance rules are substantially different from Project V's — they require a separate design pass.

---

#### Session 8 — Left Nav — V Forge Tree

**What this produces:**
The V Forge system's left nav content.

**Deliverable:**
- V Forge tree structure: active execution items with stage indicators, content graph summary, return triggers (prominent when present), recent execution reports/findings
- Return trigger visual treatment when trigger state is `arrived` or `acknowledged`
- V Forge-specific absent-affordances:
  - No create/modify planning records
  - No governing decision mutation
  - No observatory configuration
  - No self-authorize launch actions

**Why eighth:**
Third system tree. Builds on the shell and the cross-system absent-affordance vocabulary that becomes visible by comparing all three trees. V Forge has the most distinctive content (return triggers, content graph) — it's worth designing last so the tree-level visual vocabulary is established.

---

#### Session 9 — Center Workspace Foundation

**What this produces:**
The center workspace shell, the workspace router pattern, and the generic record detail view template.

**Deliverable:**
- Center workspace shell (tab bar or breadcrumb-based surface switching, panel chrome, empty state)
- Workspace router pattern (how records from left nav and output cards route to center views)
- Generic record detail view template (overview, evidence, decisions, history, actions layout pattern)
- Detail view opening rules (opened by operator action only — never auto-opens)
- Cross-surface synchronization markers (inline banner treatment for when a loaded record changes while viewed)

**Why ninth:**
The center workspace is a dependency of every workflow surface. But the center workspace itself depends on understanding what output cards look like (Session 1), what the right panel contains (Sessions 4–5), and what the left nav structure is (Sessions 6–8). It cannot be designed before its surrounding surfaces.

---

### TIER 3 — Approval and Gate Surfaces

#### Session 10 — Approval Gate Surfaces

**What this produces:**
The complete gate surface designs — Class B inline widget, Class C modal, typed confirmation, and escalation banner.

**Deliverable:**

**Class B — Inline Approval Widget (embedded in center review surface):**
- Approval request summary
- Action class badge
- Approve control (writes approval record, enables downstream activation)
- Reject control (persists rejection record)
- Defer control where applicable
- Staleness warning treatment (context has changed since recommendation was produced)

**Class C — Modal Gate (irreversible / high-consequence):**
- Triggered only after operator is inside the center review surface and all required checkpoints are complete
- Action being authorized
- What happens if authorized
- What does NOT change
- Typed confirmation input field (specific phrase required; not pre-populated; not a checkbox)
- Confirm authorization control
- Cancel control

**Typed Confirmation Input:**
- Required for irreversible Class C actions
- Separate distinct input element (not part of the modal's main flow)
- Must not be dismissible without completing the input

**Escalation Banner (Class D):**
- Non-dismissible inline banner
- What the issue is
- What action is blocked
- What decision or clarification is needed
- `[Escalate]` and `[Document and Hold]` controls
- No dismiss option, no proceed-anyway path

**Gate surfaces must not appear in:**
- Right interaction panel
- Left navigation panel
- Topbar

**Why tenth:**
Every workflow surface from Session 12 onward contains or routes to a gate. The gate surfaces must exist as a specified design before any workflow surface is designed. Getting the gate design wrong propagates errors through every subsequent workflow session.

---

#### Session 11 — Review-to-Gate Routing Flow

**What this produces:**
The single canonical routing pattern from typed output card to completed approval event.

**Deliverable:**
The five-step flow, fully specified with transitions and states:

1. LLM produces Approval Request Package in right panel → card appears with `[Proceed to Approval Gate]` CTA
2. Operator selects `[Proceed to Approval Gate]` → center workspace opens to the relevant review surface
3. Operator reviews full record/package/evidence in center surface (gate widget not yet active)
4. Operator completes required review checkpoints → gate widget activates
5. Operator uses gate widget to create persisted approval record → activation path opens

States to specify:
- Right panel card before operator selects proceed
- Center surface during review (gate not yet active — visual treatment of pre-activation state)
- Center surface when required checkpoints are complete (gate activates)
- Center surface during typed confirmation (Class C only)
- Center surface after approval written (confirmation state)
- Right panel card staleness marker if context changed while operator was in review

**Context-changed-since-recommendation notice:**
- When context has changed since the recommendation was produced, this must appear before the gate widget activates
- Changed: what changed
- Basis of recommendation may be affected
- Gate remains available but operator sees the notice first
- If the change is severe (superseded decision that the recommendation depended on): gate is blocked until recommendation is re-evaluated

**Why eleventh:**
This is a universal pattern. It applies to handoff approval, launch authorization, intake outcome activation, and every other Class B or C gate. Specifying it once before any specific workflow surface prevents each workflow surface from inventing its own variant.

---

#### Session 12 — Session Start Integrity Check + Alert/Notification System

**What this produces:**
The session start integrity check flow and the complete alert/notification surface designs.

**Deliverable:**

**Session Start Integrity Check:**
- Full-screen or modal-overlay check that appears before substantive interaction
- Shows: pending approvals, unreviewed return triggers, stale readiness states, unresolved decision conflicts, session health issues
- `[Review Items]` and `[Dismiss All — I'll handle these later]` controls
- Dismiss All must be logged as a governance-relevant fact

**Alert/Notification Scaling:**
The system must scale to governance importance. Not everything is modal.

| Importance | Surface | When |
|---|---|---|
| Informational | Attention badge (topbar) | Pending approvals, unreviewed return triggers, critical gaps |
| Persistent state | Topbar warning indicator | Session health issues, stale context categories |
| Contextual | Inline banner (center surface) | Context changes, decision supersessions, evidence staleness, compaction events |
| Session event | In-app notification | Approval written, return trigger received, notable refresh events |
| Blocking | Modal | Class C typed confirmation only |
| Hard block | Non-dismissible escalation banner | Class D conditions only |

**Output card staleness markers (all seven types):**
These apply to rendered output cards in the right panel when their basis changes:
- `⚠ CONTEXT CHANGED — produced during context change`
- `⚠ DECISION SUPERSEDED — [dec-id] replaced by [dec-id-new]`
- `⚠ EVIDENCE STALE — [obs-id] is now stale`
- `⚠ BASIS CHANGED — prior approval invalidated`
- `⚠ SYSTEM CHANGED — produced under [prior system] posture`
- `⚠ CONTINUITY ARTIFACT CHANGED — [artifact] no longer in active basis`
- `⚠ COMPACTION BOUNDARY — produced before this compaction cycle`

**18-event invalidation coverage:**
Map all 18 events from the invalidation matrix to the notification system. For each event: which surface type fires, what message, what operator action is offered. This is not cosmetic — each event has doctrine-specified consequences.

**Why twelfth:**
Alert and notification patterns are used in every workflow surface. Session start integrity check sets the governance posture for the entire session. Designing these before workflow surfaces ensures each workflow surface can reference a complete notification vocabulary rather than inventing ad-hoc treatments.

---

### TIER 4 — Core Workflow Surfaces

#### Session 13 — Handoff Review UX + Return Trigger UX *(partial schema block)*

**What this produces:**
Two workflow-specific center workspace surfaces, designed as variants of the same template. These are the highest-frequency governance surfaces in the application.

**Handoff Package Review View:**
- What is being handed off
- Approved scope / out-of-scope items
- Readiness basis
- Governing decisions relevant to the handoff
- What transfers / what does not transfer
- Evidence references with system attribution and ownership labels
- Workflow stage: `Handoff — Prepared` vs `Handoff — Awaiting Approval` (distinction matters — `Prepared` does not imply activation may proceed)
- Stale basis warning: if planning basis, approval status, or evidence basis has changed materially since package was prepared — visible warning before the approval gate is offered
- Gate widget routing (Session 11 pattern applied here)

**Return Trigger Review View:**
- What was found in execution
- Why it was routed to planning
- Execution state at point of halting
- What the finding is NOT doing (not a planning mutation, not automatic replanning)
- Response options:
  - `Route return trigger` → governed return-to-planning interface
  - `Dismiss return trigger` → logged with optional reason

**Maintenance vs Replanning routing distinction:** *(Partial schema block)*
The doctrine requires this view to help the operator determine whether the finding warrants replanning vs. can be resolved within existing approved scope as maintenance. This is a meaningful UX problem. **Design the response option distinction clearly. Flag that the derivation logic for these two paths has no settled schema anchor. The two options must be visually distinct and semantically unambiguous.** Do not flatten them into a single `Route to planning` action.

Return trigger lifecycle states must be surfaced:
- `arrived` → attention badge + prominent left nav indicator
- `acknowledged` → viewed but not actioned
- `routed` → session integrity item resolved, audit log entry
- `dismissed` → logged, preserved in session audit record

**Why thirteenth:**
Handoff and return trigger are the most frequent governance surfaces. They're also direct variants of the same center workspace template. Designing them together in one session is efficient and produces a reusable pattern. They come first among workflow surfaces because they occur at the core of the planning-execution loop.

---

#### Session 14 — Launch Readiness UX *(partial schema block)*

**What this produces:**
The launch readiness review surface.

**What to design now:**
- Planning-side readiness section
- Evidence and signal review section with VEDA attribution
- Execution-side verification section
- Cross-system readiness confirmation requirements (must make visible which of the three dimensions are confirmed vs. open)
- Blocking conditions panel
- Required acknowledgment checkpoints before gate is offered
- The `Launch Authorization — Pending` gate widget routing (Session 11 pattern applied)

**Schema-blocked portions — design to the boundary, stop:**
The following three stage names have no settled schema anchor:
- `Launch Readiness — In Progress` — show derivation basis, accept `Unavailable` state
- `Launch Authorization — Pending` — derive from approval store state
- `Post-Launch — Active` — explicitly note this requires post-launch state transition to be defined

For each schema-blocked element: specify the surface treatment, mark it with a `[SCHEMA PENDING]` note in the deliverable, and move on. Do not invent schema behavior to make the design feel complete.

**Cross-system confirmation requirement:**
This is not optional. All three confirmation dimensions (planning-side, evidence/signal, execution-side verification) must be visible in the review surface. A self-certification from any single system is not a governed cross-system confirmation.

**Evidence currency treatment:**
If evidence supporting the launch readiness determination is stale, the approval gate must be blocked with a `[Refresh Evidence]` path. The `Proceed Without Refreshing — I Accept the Risk` option must be available but must require explicit acknowledgment, which is logged.

---

#### Session 15 — Maintenance / Ranking UX *(partial schema block)*

**What this produces:**
Surfaces for ongoing execution tracking, replanning triggers, and project ranking.

**What to design now:**
- Execution maintenance state tracking (V Forge active items, content graph summary)
- Replanning trigger visibility — when a condition escalates from maintenance to replanning-warranted
- Portfolio ranking controls (relative priority signaling within Project V)
- Return-to-planning routing controls (where maintenance findings get escalated)

**Schema-blocked portions:**
- `Execution — Maintenance` stage has no dedicated schema record — derive from execution-active posture with no active return trigger routed to replanning. Accept `Unavailable` state if derivation fails.
- `Replanning — In Progress` has no dedicated schema record — derive from return trigger in `routed` state combined with Project V operational posture.

Mark these limitations in the deliverable. Design the surface treatment. Stop at the schema boundary.

---

#### Session 16 — Intake UX *(BLOCKED — do not start)*

**Blocked on:** IntakeRecord / IntakeCandidate schema. No dedicated record type or navigation tree anchor exists as of this writing.

**When unblocked:** Schedule this session only after the intake record model is explicitly settled in the doctrine. When it is settled:
- Intake stages (`Intake — Framing`, `Intake — Evaluation`, `Intake — Outcome Pending`) will have schema anchors
- Left nav intake section can be designed with real navigation nodes
- The intake classification output card (Recommendation typed as intake classification) can be fully specified
- Intake outcome options (create project, defer, reject, hold, request evidence) can be represented as distinct gate paths

**What to do now:** Nothing. Any intake UX designed before schema settlement will require redesign. Use the session time on something else.

---

### TIER 5 — Power Features

*Design these sessions only after the Tier 4 functional operator loop is solid. In practice, Tier 5 sessions should not begin until at least Sessions 13–15 are complete and have been reviewed against doctrine.*

#### Session 17 — Portfolio Triage / Dashboard

Multi-project aggregate view. Relative priority signaling. Cross-project attention badges. Blocked until single-project loop is designed and stable.

---

#### Session 18 — Agent Transparency / Lower Trace Surface

Orchestration trace, delegated task lifecycle, compact-boundary markers, lower surface content rules. Design after the core operator loop is proven so the lower surface doesn't dominate a UI that most operators should rarely need to enter.

---

#### Session 19 — Decision Continuity Timeline *(HOLD)*

Blocked until decision record schema is fully stable. The timeline visualizes historical decision state — designing it speculatively risks building the wrong artifact.

---

#### Session 20 — Evidence Freshness / Signal Views *(HOLD)*

Blocked until VEDA signal interface schema is stable. These views visualize VEDA observatory outputs — the schema shapes what's displayable.

---

#### Session 21 — Command Palette / Keyboard-First Workflows

Last in the plan because the command inventory cannot be finalized until every surface's action set is known. A command palette designed before the surfaces are done will either be too narrow or will invent commands that don't map to real surface affordances.

---

### TIER 6 — Visual and Component System

#### Session 22 — Full Bricks-Inspired Visual Language Adaptation

The full visual system adaptation using the Bricks theme as reference. By this point the minimal token decisions from Session 2 will have been tested against real surface designs. This session formalizes them into the full visual language.

---

#### Session 23 — Component Behavior Patterns

Motion, state transitions, interaction behaviors, hover/focus/active states across the complete component set. Emerges from everything built above — cannot be speculatively designed before the components exist.

---

### TIER 7 — Build-Order Planning

#### Session 24 — MVP Shell and Surface Priority

The actual build sequence for engineering. By this point every surface is designed and the schema-blocked items are either resolved or explicitly held. This session translates the design sequence into a build sequence and identifies what the minimum viable operator loop looks like.

---

#### Ongoing — Schema-Blocked Items Living Document

After every design session, update the schema-blocked items tracker at the top of this document. If a schema question resolves between sessions, the corresponding UX session moves from HOLD/BLOCKED to the active queue. If a new ambiguity is discovered during design, it gets added to the tracker.

This tracker is not a failure list. It's a precision instrument. It keeps speculation out of the work and ensures that when schema resolves, the design sessions that were waiting can pick up cleanly.

---

## Full Sequence at a Glance

```
TIER 1 — Vocabulary and Tokens
  1.  Output card system (all 7 types, badges, staleness markers, inertness)
  2.  Minimal token decisions (spacing, type, color roles)

TIER 2 — Shell Backbone
  3.  Topbar
  4.  Context strip
  5.  Right panel shell + operator input
  6.  Left nav shell + Project V tree
  7.  Left nav — VEDA tree
  8.  Left nav — V Forge tree
  9.  Center workspace foundation

TIER 3 — Approval and Gate Surfaces
  10. Approval gate surfaces (Class B inline, Class C modal, typed confirmation, escalation)
  11. Review-to-gate routing flow
  12. Session start integrity check + alert/notification system

TIER 4 — Core Workflow Surfaces
  13. Handoff Review UX + Return Trigger UX  *(partial schema block)*
  14. Launch Readiness UX                    *(partial schema block)*
  15. Maintenance / Ranking UX              *(partial schema block)*
  16. Intake UX                              *(BLOCKED — hold until schema settled)*

TIER 5 — Power Features
  17. Portfolio triage / dashboard
  18. Agent transparency / lower trace surface
  19. Decision continuity timeline           *(HOLD — schema)*
  20. Evidence freshness / signal views      *(HOLD — schema)*
  21. Command palette / keyboard-first

TIER 6 — Visual and Component System
  22. Full Bricks-inspired visual language adaptation
  23. Component behavior patterns

TIER 7 — Build-Order Planning
  24. MVP shell and surface priority
  Ongoing: Schema-blocked items living document
```

---

## What the Next Session Is

**Session 1: Output Card System.**

Read `desktop-human-llm-interaction-model.md` § Output Presentation Model before starting. Every output type's required elements are specified there. The session produces the card template for each type. When it's done, every subsequent session can reference the output card vocabulary without re-deriving it.

The session is done when all seven card types are designed with their full required element sets, action class badges are specified, and all seven staleness marker variants are specified.

It is not done when the cards look good. It is done when every element that doctrine requires is present and locatable.
