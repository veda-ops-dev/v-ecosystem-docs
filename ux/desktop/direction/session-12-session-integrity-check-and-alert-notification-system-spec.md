# Session 12 — Session Start Integrity Check + Alert/Notification System
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–11 (all shell surfaces, gate surfaces, and routing flow fully specified)
**Required before:** Sessions 13–15 (every workflow surface references the notification vocabulary; the session start integrity check is the entry point for pending approvals from prior sessions)

---

## 1. Files Read

**Prior sessions:**
- `session-02-minimal-token-decisions.md` — active token baseline; all values here reference Session 2
- `session-03-topbar-spec.md` — attention badges (§5), session health indicator (§8), click behaviors opening session integrity view; badge appearance/disappearance transitions
- `session-04-context-strip-spec.md` — INTEGRITY category row; `[Review]` navigation affordances; all 18 event CTXSTRIP consequences already specified
- `session-05-right-panel-shell-spec.md` — interaction area card staleness markers (§7); session error scrim; `↓ New output` chip; panel-level disabled states
- `session-09-center-workspace-foundation-spec.md` — inline banner position (between view header and section nav); five critical event banner specifications (EVENTs 02, 06, 08, 10, 18); cross-surface sync markers
- `session-10-approval-gate-surfaces-spec.md` — Class D escalation banner; staleness warning above gate widget; stale-context warning acknowledgment logging; approval event persistence requirements
- `session-11-review-to-gate-routing-flow-spec.md` — approval-written notification placeholder; session start integrity check as routing entry point; seven ARP card staleness marker types; context-changed notice design

**Doctrine:**
- `interfaces/desktop-invalidation-and-refresh-matrix.md` — all 18 events: affected categories, per-surface consequences, LLM consequences, blocking posture, sequencing priority
- `interfaces/desktop-surface-architecture.md` — notification scaling table (attention badge → persistent warning → inline banner → in-app notification → blocking modal → non-dismissible escalation); session start integrity check requirements; `[Review Items]` and `[Dismiss All]` controls; Dismiss All logging requirement
- `interfaces/desktop-state-and-context-model.md` — nine state categories; session integrity items; return trigger lifecycle states; schema-blocked stages
- `interfaces/desktop-governance-and-gating-model.md` — rejection must be persisted; escalation records must be persisted; dismiss actions must be logged
- `interfaces/desktop-implementation-architecture.md` — `refreshCoordinator` responsibility; event publication ordering

---

## 2. Session 12 Scope Confirmation

The work plan defines Session 12 — Session Start Integrity Check + Alert/Notification System as: the session start integrity check flow and the complete alert/notification surface designs.

This session produces:
- Session start integrity check: the full-screen overlay, its content, `[Review Items]` and `[Dismiss All]` controls, and the logging requirement for Dismiss All
- Alert/notification scaling table: the complete mapping of governance importance to surface type
- The session integrity view: the right-side panel or modal that the topbar attention badges and the session start check route to
- All 18 invalidation events mapped to their surface type: which surface fires, what message, what operator action is offered
- Output card staleness markers: all seven types with exact text, linked to their trigger events
- Approval-written confirmation notification design
- Return trigger arrival notification design
- Compaction boundary notice design
- The `[Dismiss All — I'll handle these later]` posture and what it logs

This session does not:
- Design handoff review surface content (Session 13)
- Design the command palette (Session 21)
- Add new action classes or approval paths
- Invent events outside the 18-event matrix

---

## 3. Notification Scaling Principle

Not everything is a modal. Not everything is a toast. Governance importance determines surface type. This principle is stated in doctrine (`desktop-surface-architecture.md`) and concretized here as a five-level hierarchy.

The five levels, from lowest to highest governance weight:

| Level | Surface type | When | Operator action required? |
|---|---|---|---|
| 1 — Informational | Attention badge (topbar) | Pending approvals, unreviewed return triggers, critical gaps exist | No — badge is ambient |
| 2 — Persistent state | Topbar warning indicator or context strip marker | Session health issues, stale context categories, local state divergence | No — persistent until condition resolves |
| 3 — Contextual | Inline banner in center surface | Context changes, decision supersessions, evidence staleness during active review | Soft — dismissible for informational events; non-dismissible for blocking events |
| 4 — Session event | In-app notification (toast) | Approval written, return trigger received, evidence refreshed, compaction complete | No — auto-dismisses after N seconds; has an optional action link |
| 5 — Hard block | Non-dismissible surface | Class C typed confirmation (modal); Class D escalation (banner); session error (modal) | Yes — no path forward without responding |

Rule: escalate to the next level only when the governance weight requires it. A decision being created (EVENT-01) is level 4. A prior approval being invalidated (EVENT-06) is level 3 + level 2. A session token expiring (EVENT-10) is level 5. An operator cannot be modally interrupted for every context event or they will route around the system.

---

## 4. Session Start Integrity Check

### 4.1 Purpose

The session start integrity check is a full-screen overlay that appears at the start of every session before the operator begins substantive work. It answers: "Before you start, here is everything that requires your attention."

It is not a welcome screen. It is not onboarding. It is a governance-first orientation surface.

### 4.2 When It Appears

The integrity check overlay appears:
- At session start, every time, after context loads but before any LLM interaction is enabled
- After session re-initialization following EVENT-10 (session error recovery)
- After a system switch where integrity items exist for the newly active system

It does not appear mid-session as an interruption. Mid-session events use inline banners, in-app notifications, or attention badge updates per the scaling table above.

### 4.3 Overlay Structure

The session start integrity check uses a full-screen `--surface-overlay` scrim (`--z-critical: 700` — above modals, which are at `--z-modal: 500`) with a centered content panel.

**Content panel:**
- Width: 560px
- Background: `--surface-elevated`
- Border: 1px `--border-emphasis`
- Border-radius: `--radius-lg` (6px)
- Padding: `--space-8` (32px)
- Box-shadow: `--elevation-modal`
- Max-height: 70vh; scrollable internally if many items

**Content panel anatomy:**

```
┌─────────────────────────────────────────────────────────┐
│  Session integrity check                                 │
│  content-hub  ·  Project V  ·  2026-04-03 09:30         │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  [integrity item list — scrollable if needed]            │
│                                                          │
│  ─────────────────────────────────────────────────────  │
│                                                          │
│  [Review Items]          [Dismiss All — I'll handle      │
│                           these later]                   │
└─────────────────────────────────────────────────────────┘
```

**Title:**
`Session integrity check` — `--type-xl` (20px), `--weight-semibold`, `--text-primary`

**Subtitle:**
`[project name]  ·  [system]  ·  [date and time]` — `--type-sm`, `--weight-normal`, `--text-secondary`

**If no integrity items exist** (session is clean):

```
│  ✓ No items require your attention.                      │
│  The session is ready.                                   │
│                                                          │
│                              [Continue]                  │
```

`✓` in `--state-success`. Text in `--text-secondary`, `--type-sm`. Single `[Continue]` control, amber border, `--accent-primary` text — the routing-forward style consistent with other "proceed" actions in the system. No `[Review Items]` or `[Dismiss All]` when there is nothing to review.

### 4.4 Integrity Item List

Items are grouped into four categories, in priority order top to bottom:

**Group 1 — Unreviewed return triggers** (highest urgency)
**Group 2 — Pending approvals**
**Group 3 — Stale readiness states and unresolved conflicts**
**Group 4 — Session health issues**

Each group has a header label (`--type-xs`, `--weight-semibold`, `--text-tertiary`, 0.3px letter-spacing, uppercase) only if it contains items. Empty groups are absent — no empty group headers.

**Individual item anatomy:**

```
[urgency icon]  [item title]                    [type badge]
                [brief description]
                [Record ID if applicable]                 [Review ›]
```

- Row height: varies; minimum 44px to accommodate description
- Vertical padding: `--space-2` (8px) top and bottom
- Left border: 3px left-border colored by urgency, `border-radius: 0`
- Background: `--surface-raised` on hover, `--surface-elevated` resting
- Horizontal padding: `--space-4` (16px)
- Bottom border: `--border-subtle` 1px between items

**Urgency icon and left-border color:**

| Group | Icon | Left-border color |
|---|---|---|
| Return triggers | `⚡` | `--state-danger` (#fa4362) |
| Pending approvals | `⊕` | `--state-warning` (#ffa100) |
| Stale readiness / conflicts | `⚠` | `--state-warning` (#ffa100) |
| Session health | `●` pulse | `--state-danger` (#fa4362) |

**Item title:** `--type-sm`, `--weight-medium`, `--text-primary`

**Brief description:** `--type-xs`, `--weight-normal`, `--text-secondary`; one line, truncated with ellipsis. Examples:
- Return trigger: `V Forge finding — intent shift detected during hosting comparison execution`
- Pending approval: `Class B · Activate handoff — hosting-comparison-site · Initiated 2026-03-28`
- Stale readiness: `Readiness state for seo-tech-audit has not been evaluated in 8 days`
- Conflict: `[dec-03] and [dec-07] conflict on target-system priority dimension`
- Session health: `Prior session ended with unresolved integrity items`

**Record ID** (where applicable): `--font-mono`, `--type-xs`, `--text-tertiary`; e.g., `hdl-07`, `rtn-04`

**`[Review ›]` affordance:** `--text-link`, `--type-xs`, right-aligned, visible always (not hover-only). Clicking navigates the operator to the relevant surface — closes the overlay, opens the session integrity view pre-scrolled to this item. For pending approvals specifically, `[Review ›]` on that item routes directly to the center workspace record detail via `intent = 'approval_gate'` (the five-step routing flow from Session 11 begins here, not at a right-panel ARP card).

**Multiple pending approvals:** Each pending approval is its own item row. The operator sees a discrete row per record awaiting their decision. This is the answer to the Session 11 open question about multi-approval sessions: the integrity check surfaces them individually, not as an aggregate count.

### 4.5 `[Review Items]` Control

- Width: 160px
- Height: 40px
- Background: `--accent-primary` (#ffd64f)
- Text: `--text-inverse` (#212121), `--type-sm`, `--weight-bold`
- Border-radius: `--radius-md`
- On click: closes the overlay, opens the session integrity view (§5) with all items visible

`[Review Items]` is the primary control. It closes the integrity check overlay and opens the full session integrity view where the operator can work through items one by one.

### 4.6 `[Dismiss All — I'll handle these later]` Control

- Width: 240px
- Height: 40px
- Background: `--surface-raised`
- Border: 1px `--border-default`
- Text: `--text-secondary`, `--type-sm`, `--weight-normal`
- Border-radius: `--radius-md`
- Hover: `--state-hover-overlay`

On click: a brief confirmation prompt appears inline below the two controls (does not open a modal — it is a short inline text):

```
Dismissing all items. This action is logged as a governance-relevant fact.
[Confirm Dismiss All]    [Cancel]
```

`[Confirm Dismiss All]`: `--state-warning` border, `--state-warning` text, `--radius-md`. Clicking this: closes the overlay, logs the dismiss event (timestamp, operator session identity, list of items dismissed, session ID), and resumes normal session posture.

`[Cancel]`: returns to the full overlay without logging anything.

**What the dismiss log contains:** The persist record for a Dismiss All action must include: the session ID, the operator identity, the timestamp, and the full list of item IDs that were dismissed (pending approval record IDs, return trigger IDs, conflict IDs, etc.). This is the logging requirement stated in doctrine: "Dismiss All must be logged as a governance-relevant fact."

**What Dismiss All does not do:** It does not resolve any items. It does not write an approval record. It does not route any return triggers. The items remain in their existing states — pending approvals remain pending, return triggers remain arrived or acknowledged. The only thing that changes is that the operator has acknowledged they are aware of these items and have chosen to defer addressing them. The topbar attention badges remain active. The context strip INTEGRITY row retains all items.

**Dismiss All is not a governance shortcut.** It is a session-start posture declaration. An operator using it repeatedly without resolving items will accumulate a growing integrity view and a growing audit trail of deferrals. That is the correct governance outcome.

---

## 5. Session Integrity View

### 5.1 What It Is

The session integrity view is the full detailed list of all unresolved session integrity items, accessible at any time during the session. It is not a modal. It is a right-side drawer panel that slides in from the right edge of the application.

**Why not a modal:** A modal blocks the workspace. The operator may need to look at the workspace content (a record detail, the nav tree, the context strip) while reviewing integrity items to understand their context. A drawer does not block.

**Trigger paths:**
- Clicking any topbar attention badge (§ Session 3 click behaviors)
- Clicking `[Review Items]` in the session start integrity check
- Clicking the session health indicator when it shows a non-active state
- Clicking `[Review]` links in the context strip INTEGRITY row

### 5.2 Drawer Structure

The session integrity view appears as a drawer sliding in from the right side, overlapping the right panel by the drawer's width. The left panel and center workspace remain fully usable behind it.

**Drawer dimensions:**
- Width: 400px
- Height: full viewport height minus topbar (48px)
- Background: `--surface-elevated`
- Left border: 1px `--border-default`
- Box-shadow: `--elevation-overlay` on the left edge only
- Z-index: `--z-overlay` (400) — above center workspace and right panel, below modals
- Slide-in transition: `--transition-panel` (transform 400ms `--ease-in-out`)

**Drawer header (48px):**
`Session integrity` — `--type-lg` (16px), `--weight-semibold`, `--text-primary`
`×` close button at right edge: `--text-tertiary`, transitions to `--text-secondary` on hover

**Drawer body:** scrollable; same four-group structure as the session start integrity check but with richer per-item detail.

### 5.3 Item Detail in the Drawer

Each item in the drawer expands to show full context, replacing the compact one-liner from the integrity check overlay.

**Return trigger item (expanded):**
```
⚡  Return trigger — V Forge finding: intent shift
    Status: arrived  ·  2026-04-01 08:22  ·  rtn-04
    V Forge halted hosting-comparison execution due to changed
    pricing signal from primary provider.
    [Review in center surface ›]    [Acknowledge]
```

- `[Review in center surface ›]`: opens the return trigger detail in center workspace; `--text-link`, `--type-sm`
- `[Acknowledge]`: transitions trigger state from `arrived` to `acknowledged`; the icon updates from `⚡` in `--state-danger` to `⚡` in `--state-warning`; the item remains in the drawer (acknowledged is not resolved)

**Pending approval item (expanded):**
```
⊕  Pending approval — hosting-comparison-site handoff
    Status: awaiting approval  ·  Initiated 2026-03-28  ·  hdl-07
    Class B  ·  Activate handoff — transfer execution responsibility
    to V Forge for the hosting comparison scope.
    [Go to approval gate ›]
```

- `[Go to approval gate ›]`: closes the drawer, routes to the center workspace record detail via `intent = 'approval_gate'`; begins the five-step routing flow from Session 11 Step 2

**Stale readiness item (expanded):**
```
⚠  Stale readiness — seo-tech-audit
    Last evaluated: 2026-03-25  ·  9 days old  ·  eval-12
    The readiness evaluation for this initiative has not been
    refreshed in 9 days. May not reflect current conditions.
    [Review in center surface ›]    [Mark as acknowledged]
```

**Conflict item (expanded):**
```
⚠  Decision conflict — [dec-03] vs [dec-07]
    Detected: 2026-04-02  ·  Dimension: target-system priority
    [dec-03] prioritizes search-first; [dec-07] deprioritizes SaaS
    vertical. These conflict on how the hosting vertical fits the
    target system priority stack.
    [Review decisions ›]    [Mark as acknowledged]
```

**Session health item:**
```
●  Prior session ended with unresolved items
    2026-04-02 session ended with: 1 return trigger (dismissed),
    2 pending approvals (still pending).
    This is informational — the pending approvals appear above.
```
No action affordance — this is a read-only historical note.

### 5.4 Drawer Footer

At the bottom of the drawer, a footer row (40px, `--border-top: 1px --border-subtle`) shows:

`[Dismiss all remaining ›]` — `--text-tertiary`, `--type-xs`; same confirmation prompt as the session start check Dismiss All; same logging requirements.

---

## 6. In-App Notification (Toast) System

### 6.1 What It Is

In-app notifications are brief, non-blocking, auto-dismissing notices for session events that require the operator's awareness but not their immediate action. They are the Level 4 surface in the scaling hierarchy.

They are distinct from:
- Topbar attention badges (persistent, count-based, Level 1)
- Inline banners in center surfaces (tied to a specific open record, Level 3)
- Modals (block interaction, Level 5)
- The session start integrity check (session-start only)

### 6.2 Toast Anatomy

Toasts appear in the top-right corner of the center workspace, stacked vertically if multiple arrive close together. They do not cover the topbar.

**Position:** `position: absolute` within the center workspace area; top: 16px; right: 16px; `--z-toast: 600`

**Individual toast:**
- Width: 320px
- Background: `--surface-elevated`
- Border: 1px `--border-default`
- Border-left: 3px colored by event type (see §6.4)
- Border-radius: `--radius-md` (4px); `border-radius: 0` on the left-border side — no rounded corners on single-sided borders per design system rules
- Padding: `--space-3` (12px) all sides
- Box-shadow: `--elevation-overlay`

**Toast content:**

```
[icon]  [title — 1 line, --type-sm, --weight-medium]       [×]
        [body — 1-2 lines, --type-xs, --text-secondary]
        [action link — optional, --type-xs, --text-link]
```

- Icon: 14px, colored by event type
- Title: `--type-sm`, `--weight-medium`, `--text-primary`; max one line
- Body: `--type-xs`, `--weight-normal`, `--text-secondary`; max two lines; truncated beyond that
- Action link: `--type-xs`, `--text-link`; optional; clicking it routes to the relevant surface; clicking the link also dismisses the toast
- `×` close: `--text-tertiary`, `--type-xs`, appears on hover

**Auto-dismiss timing:** 6 seconds for informational events. 10 seconds for events that have an action link (giving the operator time to read and decide). Timing restarts if the operator moves the cursor over the toast (hover-to-pause behavior).

**Toast entry animation:** Slides in from the right: `translateX(120px)` → `translateX(0)`, `--transition-default` (200ms `--ease-out`). Fades out on dismiss: `opacity 1 → 0`, `--transition-fade` (300ms ease).

**Stacking:** Up to 4 toasts visible simultaneously. A 5th arriving while 4 are present replaces the oldest. Stack grows upward (newest at top).

### 6.3 Toast Types and Left-Border Colors

| Event type | Left-border color | Icon | Icon color |
|---|---|---|---|
| Success (approval written, evidence refreshed, task completed) | `--state-success` (#11b76b) | `✓` | `--state-success` |
| Informational (decision created, system switched, stage changed) | `--state-info` (#00b0f4) | `ℹ` | `--state-info` |
| Warning (evidence stale, decision conflict, compaction complete) | `--state-warning` (#ffa100) | `⚠` | `--state-warning` |
| Urgent (return trigger arrived, prior approval invalidated) | `--state-danger` (#fa4362) | `⚡` | `--state-danger` |

### 6.4 Approval-Written Confirmation Notification

Fired by: EVENT-05 (approval written).
Type: Success toast.

**Title:** `Approval recorded — [record name]`
**Body:** `[Action label] — [timestamp]`
**Action link:** `View approval record ›`

Example:
```
✓  Approval recorded — hosting-comparison-site
   Activate handoff — 2026-04-03 09:47
   View approval record ›
```

This toast fires at the moment the approval record is confirmed written to the database — the same moment the center workspace gate widget transitions to its post-approval confirmation state (Session 10 §4.6). The two events are simultaneous and complementary: the gate widget shows the governance confirmation in the center surface; the toast provides a brief ambient confirmation visible regardless of where in the application the operator is looking.

Auto-dismiss: 10 seconds (has an action link).

### 6.5 Return Trigger Arrival Notification

Fired by: EVENT-16 (return trigger arrives).
Type: Urgent toast.

**Title:** `Return trigger received from V Forge`
**Body:** `[Brief description of finding]  ·  [rtn-id]`
**Action link:** `Review ›`

Example:
```
⚡  Return trigger received from V Forge
   Intent shift — hosting-comparison execution  ·  rtn-04
   Review ›
```

`Review ›` opens the return trigger detail in the center workspace. Auto-dismiss: 10 seconds. The topbar attention badge also updates simultaneously — the toast and the badge fire together.

### 6.6 Compaction Boundary Notice

Fired by: EVENT-14 (meaningful compaction event).
Type: Informational toast, plus a persistent compaction boundary marker in the interaction area.

**Toast:**
**Title:** `Session context compacted`
**Body:** `Context basis has been refreshed. Per-category validation complete.`
**Action link:** None (or `View validation results ›` if any category required attention)

Auto-dismiss: 6 seconds.

**Compaction boundary marker in the interaction area (separate from the toast):**
A horizontal divider appears in the right panel interaction area between pre-compaction and post-compaction output cards:

```
──────────────────  COMPACTION BOUNDARY  ──────────────────
   Context basis refreshed — outputs below this line reflect
   the post-compaction session basis.
```

- Divider line: `--border-subtle` 1px with center label
- Label: `COMPACTION BOUNDARY` — `--type-xs`, `--weight-semibold`, `--text-tertiary`, 0.3px letter-spacing, uppercase
- Description line below: `--type-xs`, `--text-tertiary`
- Background: none (transparent — the divider sits in the flow of the card list)
- This marker is permanent for the session — it does not fade or dismiss. It is the historical record in the interaction area that marks which outputs were produced before and after the compaction.

---

## 7. Complete 18-Event Alert Surface Mapping

This is the complete mapping: every event, the surface(s) that fire, the exact message (title and body), and the operator action offered. All 18 events from the invalidation matrix are covered. No event is left unmapped.

The mapping uses the five-level scaling hierarchy from §3. Some events trigger multiple surfaces simultaneously (e.g., a blocking event triggers both an inline banner in the center surface and a topbar badge update).

---

### EVENT-01 — Governing Decision Created

**Surfaces that fire:**
- Level 4: In-app notification (toast)
- Level 3: Inline banner in any open center surface if it may reference the decision set

**Toast:**
Title: `New governing decision — [dec-id]`
Body: `[Decision title] added to active decision set.`
Action link: `View decision ›`
Type: Informational. Auto-dismiss: 6 seconds.

**Center surface inline banner** (only if an open record's decision context may be affected):
```
ℹ New governing decision created: [dec-id] — [title].
  Prior outputs in this view may not reflect this decision.
  [Review decision ›]
```
Treatment: `--state-info-bg`, `--state-info` left-border (3px), dismissible `×`.

**Topbar:** No badge change unless a conflict results (→ EVENT-04).
**Context strip:** Updates immediately per Session 4 EVENT-01 specification — decision added to named list.
**Blocking posture:** Non-blocking for Class A. Class B and C gates blocked until context strip shows reloaded decision set.

---

### EVENT-02 — Governing Decision Superseded

**Surfaces that fire:**
- Level 2: Topbar attention badge updates (integrity badge, Element 7)
- Level 3: Inline banner in any open center surface that referenced the superseded decision
- Level 4: In-app notification (toast) — unless an active ARP cites the superseded decision, in which case → Level 5 modal alert

**Toast (standard case — no active ARP affected):**
Title: `Decision superseded — [dec-id]`
Body: `[dec-id] replaced by [dec-id-new]. Outputs citing it are now stale.`
Action link: `Review change ›`
Type: Warning. Auto-dismiss: 10 seconds.

**Toast (ARP affected case — escalates to modal):**
Not a toast. A modal alert fires instead:
```
⚠ GOVERNING DECISION SUPERSEDED
[dec-id] has been superseded by [dec-id-new].
This decision was cited in a pending approval request package.
The approval package must be re-evaluated before proceeding.
[Review Change]    [View Approval Package]
```
Modal: `--elevation-modal`, `--z-modal` (500), `--surface-elevated`, centered. `[Review Change]` and `[View Approval Package]` are the only controls. No dismiss without clicking one. This is Level 5 for the ARP case because the governance consequence is significant: the operator cannot simply notice the event and continue — they must engage with what it means for their pending approval.

**Center surface inline banner** (on any open record view referencing the superseded decision):
```
⚠ GOVERNING CONTEXT CHANGED
[dec-id] has been superseded by [dec-id-new]. This record may have
referenced the prior decision.
[Review Change]
```
Treatment: `--staleness-bg`, `--staleness-border` (3px left), `--staleness-text`. Non-dismissible until `[Review Change]` is clicked.

**Context strip:** Updates per Session 4 EVENT-02 — superseded decision shown with `[superseded by dec-id-new]` marker.
**Blocking posture:** Blocks Class B and C gates on the affected dimension until acknowledgment.

---

### EVENT-03 — Governing Decision Invalidated

**Surfaces that fire:** Identical to EVENT-02 except the wording reflects invalidation (not supersession) and no replacement decision exists.

**Toast (standard case):**
Title: `Decision invalidated — [dec-id]`
Body: `[dec-id] is no longer active. No replacement decision. Outputs require re-evaluation.`
Action link: `Review ›`
Type: Warning. Auto-dismiss: 10 seconds.

**Toast (ARP affected):** Modal alert, same treatment as EVENT-02 modal case with wording adjusted: `[dec-id] has been invalidated and has no replacement decision. This changes the basis for any outputs that cited it.`

**Center surface inline banner:**
```
⚠ GOVERNING DECISION INVALIDATED
[dec-id] has been voided. No replacement governs this dimension.
Review affected outputs before proceeding.
[Review ›]
```
Non-dismissible until clicked.

**Context strip:** Voided decision removed from named list per Session 4 EVENT-03.
**Blocking posture:** Same as EVENT-02.

---

### EVENT-04 — Decision Conflict Detected

**Surfaces that fire:**
- Level 1: Topbar attention badge (integrity badge, Element 7) activates or increments
- Level 3: Context strip conflict warning (already specified in Session 4)
- Level 4: In-app notification (toast)

**Toast:**
Title: `Decision conflict detected`
Body: `[dec-id] and [dec-id-2] conflict on [dimension].`
Action link: `View conflict ›`
Type: Warning. Auto-dismiss: 10 seconds.

**Context strip:** Per Session 4 EVENT-04 — conflict shown inline in DECISIONS row.
**No center surface inline banner** unless the operator is viewing a record where the conflicting decisions are the direct governing context for a pending gate.
**Blocking posture:** Blocks Class B and C on the conflicted dimension until acknowledged or resolved.

---

### EVENT-05 — Approval Written

**Surfaces that fire:**
- Level 4: In-app notification (toast) — the approval-written confirmation notification (§6.4)
- Level 1: Topbar attention badge updates (pending approval count decrements, may clear)

**Toast:** Per §6.4 — success type, 10-second auto-dismiss, `View approval record ›` action link.

**Left nav:** Tree item updates — handoff badge changes from `awaiting approval` to `handed off`, etc. per Session 6 EVENT-05.
**Context strip:** Stage and integrity rows update per Session 4 EVENT-05.
**Center surface:** Confirmation state on the record detail per Session 11 Step 5.
**No center surface inline banner** — the gate widget confirmation state covers this.

---

### EVENT-06 — Prior Approval Superseded or Invalidated

**Surfaces that fire:**
- Level 2: Topbar attention badge (integrity badge, Element 7) activates
- Level 3: Inline banner in the center surface for the affected record
- Level 5: Modal alert — approval invalidation is a governance-significant event

**Modal alert:**
```
⚠ PRIOR APPROVAL INVALIDATED

The approval for [record name] ([record-id]) is no longer valid.

Reason: [Why the approval was invalidated — specific]

All actions that required this approval are now blocked.
Review the changed conditions before proceeding.

[View Affected Record]    [Reload Context]
```
Modal: `--elevation-modal`, `--z-modal`, `--surface-elevated`, 560px width. `[View Affected Record]` opens the record in center workspace. `[Reload Context]` triggers a full context reload. Neither button closes the modal without action — clicking either one closes the modal after the action begins.

**Center surface inline banner** (on the affected record's detail view if it is open):
Per Session 9 EVENT-06 specification: `Prior approval for [record] has been invalidated. Review required.` `--state-danger-bg`, `--state-danger` left-border (3px). Non-dismissible until `[Reload Context]` is clicked.

**ARP card in right panel:** Per Session 11 §10.3 — receives `⚠ BASIS CHANGED` staleness marker.
**Blocking posture:** Blocks any gate requiring the invalidated approval as a prerequisite.

---

### EVENT-07 — Evidence Record Loaded

**Surfaces that fire:**
- Level 2: Context strip EVIDENCE row updates (ambient, no notification needed)

**No toast.** Evidence loading is a routine operator-initiated action. The context strip update is the sufficient acknowledgment. No attention badge change. No inline banner.

Exception: if the newly loaded evidence contradicts an existing governing decision or a pending approval basis, the contradiction surfaces as EVENT-08 (evidence stale) or EVENT-02/03 (decision affected) — not as an escalation of EVENT-07 itself.

---

### EVENT-08 — Evidence Record Becomes Stale

**Surfaces that fire:**
- Level 4: In-app notification (toast) — if an active approval or pending gate depends on the now-stale evidence
- Level 3: Inline banner in center surface if the affected record is open
- Level 2: Context strip EVIDENCE row staleness marker

**Toast** (when an active gate depends on stale evidence):
Title: `Evidence basis stale — [obs-id]`
Body: `[obs-id] has exceeded its validity window. Pending gates that depend on it are blocked.`
Action link: `Refresh evidence ›`
Type: Warning. Auto-dismiss: 10 seconds.

**No toast** when no active gates depend on the stale evidence — the context strip marker is sufficient.

**Center surface inline banner** (on the open record view if it has a pending gate that depends on this evidence):
```
⚠ EVIDENCE BASIS MAY BE STALE
[obs-id] has become stale. Review evidence before approval.
[View Evidence]
```
`--staleness-bg`, `--staleness-border` (3px left). Dismissible `×`.

**Context strip:** Per Session 4 EVENT-08 — `⚠ STALE — Nh` inline in the evidence record row.
**ARP cards in right panel:** Cards that cited the now-stale evidence receive `⚠ EVIDENCE STALE — [obs-id] is now stale.`
**Blocking posture:** Blocks Class C gates that require evidence currency.

---

### EVENT-09 — Evidence Refreshed

**Surfaces that fire:**
- Level 4: In-app notification (toast) — brief confirmation

**Toast:**
Title: `Evidence refreshed — [obs-id]`
Body: `[obs-id] updated. Evidence basis is current.`
Action link: None.
Type: Success. Auto-dismiss: 6 seconds.

**Context strip:** Staleness marker removed per Session 4 EVENT-09.
**Center surface:** Any staleness banners related to the refreshed evidence are dismissed.
**ARP cards:** Staleness markers on ARP cards that cited the now-refreshed evidence receive an annotation: `Evidence basis refreshed [timestamp]. Re-evaluate if needed.` (per Session 5 / invalidation matrix).
No blocking posture change — evidence-staleness block on Class C gates is cleared.

---

### EVENT-10 — Session Token Expiry or Runtime Scope Breakage

**Surfaces that fire:**
- Level 5: Modal alert (full-screen blocking)
- Level 2: Topbar session error state (persists after modal acknowledged, until re-initialization)

**Modal:**
```
⛔ SESSION ERROR

Runtime connection lost.

All governance-sensitive actions are blocked.
Your session context has been preserved where possible.
Re-initialize to continue.

[Re-initialize Session]
```
Modal: `--elevation-modal`, `--z-critical` (700 — above everything), `--surface-elevated`, 480px width, danger-accented header. `[Re-initialize Session]` is the only control. No dismiss. No cancel. No close button. The session must be re-initialized before the operator can do any substantive work.

**Topbar:** Per Session 3 EVENT-10 — `Session error`, `--state-danger` dot, all badges show static `⚠`.
**All panels:** Disabled state per their respective session error specs (Sessions 5, 6, 7, 8, 9).
**Context strip:** All categories show `[unavailable — session error]` per Session 4 EVENT-10.
**Interaction area:** Session error scrim per Session 5 §7.
**Blocking posture:** Blocks all Class B and C actions. Level 1 sequencing priority.

---

### EVENT-11 — Current System Changed

**Surfaces that fire:**
- Level 4: In-app notification (toast) — brief confirmation
- Level 2: Topbar and context strip update (ambient, simultaneous with the switch)

**Toast:**
Title: `System switched to [new system]`
Body: `Context has been refreshed for [new system] posture.`
Action link: None.
Type: Informational. Auto-dismiss: 6 seconds.

**Topbar, left nav, context strip:** All update per their respective EVENT-11 specifications (Sessions 3, 4, 6, 7, 8).
**Right panel:** Prior output cards under the old system posture receive `⚠ SYSTEM CHANGED — produced under [prior system] posture.`
**Center surfaces:** Open records belonging to the prior system remain visible and labeled with system ownership; no auto-close.
**Blocking posture:** Context reload for new system must complete before Class B or C gate is presented.

---

### EVENT-12 — Delegated Task Completed (with admitted findings)

**Surfaces that fire:**
- Level 4: In-app notification (toast)
- Level 4: Right panel notice: `DELEGATED FINDING ADMITTED` (per invalidation matrix)

**Toast:**
Title: `Delegated task complete — [task-id]`
Body: `Findings admitted to session basis. Non-canonical.`
Action link: `Review findings ›`
Type: Informational. Auto-dismiss: 6 seconds.

**Context strip:** ORCH and CONTINUITY rows update per Session 4 EVENT-12.
**No center surface inline banner** unless the admitted findings contain information that affects an open record's review context.
**Blocking posture:** Non-blocking unless findings contain a return trigger.

---

### EVENT-13 — Delegated Task Failed or Cancelled

**Surfaces that fire:**
- Level 4: In-app notification (toast)
- Level 4: Right panel — staleness marker on outputs that depended on the task (if applicable)

**Toast:**
Title: `Delegated task [failed / cancelled] — [task-id]`
Body: `[task label]  ·  Outputs that depended on this task may be incomplete.`
Action link: `View trace ›` (routes to lower trace surface if active)
Type: Warning. Auto-dismiss: 10 seconds.

**Context strip:** ORCH row updates to `✗ failed` or `cancelled` per Session 4 EVENT-13.
**Right panel:** Affected output cards receive `⚠ DELEGATED TASK [failed/cancelled] — outputs that depended on this task may be incomplete.`
**Blocking posture:** Non-blocking unless the failed task was required for a specific gate.

---

### EVENT-14 — Meaningful Compaction Event

**Surfaces that fire:**
- Level 4: In-app notification (toast) — per §6.6
- Level 3: Compaction boundary marker in right panel interaction area — per §6.6
- Level 5: Modal alert if any category is `invalid-blocking` post-compaction

**Toast:** Per §6.6 — informational or includes action link if category validation requires attention.

**Modal** (only if `invalid-blocking` category exists post-compaction):
```
⚠ COMPACTION — CONTEXT VALIDATION REQUIRED

The session context was compacted, but [category] could not be
fully validated. This category is required for governance-sensitive
actions.

Reload context before continuing.

[Reload Context]    [View Details]
```
`[Reload Context]`: triggers full reload. `[View Details]`: opens session integrity view filtered to the invalid category.

**Context strip:** Per Session 4 EVENT-14 — all categories re-render post-validation; `[cb]` compact-boundary artifact appears in CONTINUITY row; TOOLSURFACE shows per-category validation result.
**Right panel:** Compaction boundary marker appears between pre- and post-compaction cards per §6.6.
**Blocking posture:** `invalid-blocking` category → Level 2 blocking. `stale-refresh-required` → must refresh before gates are shown.

---

### EVENT-15 — Transcript-Backed Continuity Change

**Surfaces that fire:**
- Level 4: In-app notification (toast) — only if an artifact that was cited in an active ARP expires

**Toast** (artifact expiry affecting active ARP):
Title: `Continuity artifact expired — [artifact type]`
Body: `Referenced in an active approval package. Package must be re-evaluated.`
Action link: `Review package ›`
Type: Warning. Auto-dismiss: 10 seconds.

**No toast** for routine continuity artifact updates (admitted, freshness-updated) — the context strip is sufficient.

**Context strip:** CONTINUITY row updates per Session 4 EVENT-15.
**Right panel:** ARP cards that cited the expired artifact receive `⚠ CONTINUITY ARTIFACT CHANGED — [artifact] no longer in active session basis.`
**Blocking posture:** Non-blocking unless the artifact was the basis for an active ARP, in which case the ARP must be re-evaluated before the gate is presented.

---

### EVENT-16 — Return Trigger Arrives

**Surfaces that fire:**
- Level 1: Topbar attention badge (return trigger badge, Element 6) activates or increments
- Level 4: In-app notification (toast) — per §6.5
- Level 2: Context strip INTEGRITY row update (immediately)
- Left nav: Return trigger section appears/updates in both V Forge and Project V trees

**Toast:** Per §6.5 — urgent type, 10-second auto-dismiss, `Review ›` action link.

**Return trigger lifecycle state changes** (after arrival):
- `arrived → acknowledged`: no new notification fires; attention badge remains; `[Acknowledge]` in integrity view updates the row icon from `⚡` `--state-danger` to `⚡` `--state-warning`; no toast for this transition
- `acknowledged → routed`: success toast fires: `Return trigger routed — [rtn-id]. Planning review initiated.`; attention badge clears; context strip INTEGRITY item resolves
- `acknowledged → dismissed`: informational toast fires: `Return trigger dismissed — [rtn-id]. Dismissal logged.`; attention badge clears; context strip INTEGRITY item resolves; dismissal logged as governance-relevant fact per the dismiss logging requirement

**Blocking posture:** Non-blocking on arrival. Blocking (Level 2) if unresolved when the operator attempts a Class C gate.

---

### EVENT-17 — Workflow Stage Change

**Surfaces that fire:**
- Level 2: Topbar stage indicator updates immediately (ambient)
- Level 4: In-app notification (toast) if the stage change creates new blocking conditions or gates
- Level 3: Inline banner in any open center surface for the affected work scope

**Toast** (when stage change creates a new gate or new blocking condition):
Title: `Workflow stage updated — [new stage name]`
Body: `Gate and action posture has changed.`
Action link: `View record ›`
Type: Informational. Auto-dismiss: 6 seconds.

**No toast** for routine stage progression that the operator just caused (e.g., they just approved something and the stage advanced — they know this happened).

**Center surface inline banner** (on the open record for the affected work scope):
```
ℹ Workflow stage updated to [new stage name].
  Gate and action posture has changed.
  [Review updated actions ›]
```
`--state-info-bg`, `--state-info` left-border (3px). Dismissible `×`.

**Topbar, left nav, context strip:** Update per their respective EVENT-17 specifications (Sessions 3, 4, 6).
**Right panel:** Prior output cards that referenced the old stage as current receive staleness markers.
**Blocking posture:** Stage context reload must complete before next gate is shown.

---

### EVENT-18 — Local Support-State Divergence Detected

**Surfaces that fire:**
- Level 2: Topbar session integrity indicator updates: `⚠ State divergence` (per Session 3 §6)
- Level 1: Topbar attention badge (integrity badge, Element 7) activates
- Level 5: Modal alert if divergence affects a category required for an active Class B or C gate

**Modal** (when divergence affects an active gate's required categories):
```
⚠ LOCAL STATE DIVERGENCE

[Category name] loaded from local state and may not reflect
backend canonical state.

This category is required for the pending approval gate.
Verify before proceeding.

[Verify Now]    [Dismiss — I'll verify later]
```
`[Verify Now]`: triggers a backend reconciliation load for the affected category. `[Dismiss — I'll verify later]`: logs the dismissal; the gate remains blocked; the operator can proceed with other work.

**Toast** (when divergence does not affect active gates — informational):
Title: `Local state divergence detected`
Body: `[Category] may not reflect backend state. Verify before acting.`
Action link: `Verify ›`
Type: Warning. Auto-dismiss: 10 seconds.

**Context strip:** Affected categories shown with `⚠ LOCAL DIVERGENCE` annotation per Session 4 EVENT-18.
**Center surfaces:** If open surfaces show data from the diverged category, inline banner per Session 9 EVENT-18.
**Blocking posture:** Blocks Class B and C gates if affected categories are required and divergence is unresolved.

---

## 8. Output Card Staleness Markers — Complete Specification

All seven staleness marker types, with exact text, trigger events, and visual treatment. These apply to rendered LLM output cards in the right panel's interaction area. Each marker appears as an inline banner attached to the top of the affected card, within the card boundary (per Session 5 §7).

**Staleness marker anatomy:**
- Background: `--staleness-bg`
- Border-left: 3px `--staleness-border`; `border-radius: 0` on that side
- Text: `--type-xs`, `--staleness-text`
- Padding: `--space-2` (8px) vertical, `--space-3` (12px) horizontal
- Multiple markers stack vertically within the card boundary, each as its own banner strip

| Marker | Exact text | Triggered by |
|---|---|---|
| `CONTEXT CHANGED` | `⚠ CONTEXT CHANGED — produced during a context change. Review before acting.` | Catch-all; used when a specific marker type does not apply |
| `DECISION SUPERSEDED` | `⚠ DECISION SUPERSEDED — [dec-id] replaced by [dec-id-new]. This output cited the prior decision.` | EVENT-02, EVENT-03 |
| `EVIDENCE STALE` | `⚠ EVIDENCE STALE — [obs-id] is now stale. This output's evidence basis may not reflect current conditions.` | EVENT-08 |
| `BASIS CHANGED` | `⚠ BASIS CHANGED — prior approval for [record] has been invalidated. Re-evaluate this output.` | EVENT-06 |
| `SYSTEM CHANGED` | `⚠ SYSTEM CHANGED — produced under [prior system] posture. Review before applying in [new system] context.` | EVENT-11 |
| `CONTINUITY ARTIFACT CHANGED` | `⚠ CONTINUITY ARTIFACT CHANGED — [artifact type] referenced in this output is no longer in the active session basis.` | EVENT-15 |
| `COMPACTION BOUNDARY` | `⚠ COMPACTION BOUNDARY — produced before this compaction cycle. Context basis has since been refreshed.` | EVENT-14 |

**The `[dec-id]`, `[obs-id]`, `[record]`, `[prior system]`, and `[artifact type]` placeholders are always filled with specific identifiers.** Generic markers are not acceptable. An implementer reading `⚠ DECISION SUPERSEDED — [dec-id] replaced by [dec-id-new]` must produce `⚠ DECISION SUPERSEDED — [dec-03] replaced by [dec-07]` in the actual UI. The specificity is the point.

**Markers are never deleted.** They accumulate on a card. A card may carry multiple markers from multiple events. The operator's session record of what happened to each output is preserved.

**Marker appearance animation:** `--transition-fade` (300ms ease opacity: 0 → 1). The marker fades into position above the card content. It does not push card content down with a layout animation — it appears in place, and the card expands slightly to accommodate it.

---

## 9. What Session 12 Resolves

- The session start integrity check is fully specified: full-screen overlay, four item groups, per-item content, `[Review Items]` control, `[Dismiss All — I'll handle these later]` with inline confirmation prompt, and the exact contents of the Dismiss All log record (session ID, operator identity, timestamp, full list of dismissed item IDs).
- The session integrity view is fully specified: drawer format (not modal), 400px width, four item groups, expanded per-item content, per-item action affordances, `[Review in center surface ›]` and `[Go to approval gate ›]` routing links.
- All 18 invalidation events are mapped to their surface types, exact messages, and operator actions. No event is unmapped, no event is treated identically to all others.
- The notification scaling table is concrete: five levels, each tied to specific event types, not left as abstract principle.
- The approval-written confirmation notification is specified: success toast, title and body format, `View approval record ›` action link, 10-second auto-dismiss.
- The return trigger arrival notification is specified: urgent toast, and the lifecycle state transition notifications (acknowledged → no notification; routed → success toast; dismissed → informational toast + logged).
- The compaction boundary notice is specified: informational toast plus the permanent compaction boundary marker in the right panel interaction area.
- All seven output card staleness marker types are specified with exact text and their trigger events. The specificity requirement (no generic markers) is stated as an implementation requirement.
- The `[Dismiss All]` posture and logging requirement is concrete: what is logged, when confirmation is required, what the action does and does not do.
- The pending-approval multi-item handling is resolved: each pending approval appears as its own item row in both the session start check and the integrity view, with individual `[Go to approval gate ›]` affordances that route into the Session 11 five-step flow.
- The escalation-to-modal logic for EVENTs 02, 03, 06, 10, 14, and 18 is specified: conditions under which a toast escalates to a modal, modal content, and modal controls.

---

## 10. What Session 12 Does Not Resolve Yet

- **Full session integrity view behavior for resolved items** — when a pending approval is approved or a return trigger is routed, the item disappears from the integrity view. The transition animation for item removal (fade out, remaining items shift up) is Session 23 (Component Behavior Patterns).
- **Toast stacking behavior when more than 4 arrive simultaneously** — the rule (oldest dismissed at 5th arrival) is specified; the exact animation for the displaced toast is Session 23.
- **The lower trace surface** — EVENT-12 and EVENT-13 reference `View trace ›` action links in toasts. The lower trace surface's layout and content are Session 18 (Agent Transparency / Lower Trace Surface).
- **Command palette notification** — when the operator uses the command palette to explicitly request a context reload or integrity check, the command palette triggers these surfaces. The command palette's own interface is Session 21.
- **OS-level notifications** — the work plan references "OS notification" as a delivery vehicle for session integrity items at session start. Whether to use OS-level (outside the application window) notifications for return trigger arrival when the application is backgrounded is an implementation decision outside UX scope. The in-app surfaces are fully specified here; OS-level notifications are deferred.
- **Notification preference settings** — whether operators can configure which toast types they receive is a feature that would appear in application settings. Not designed in this session.

---

## 11. Recommended Inputs to Session 13

Session 13 is Handoff Review UX + Return Trigger Review UX — the first two TIER 4 workflow surfaces.

**What Session 13 inherits from Sessions 10–12:**
- The gate widget, checkpoint model, and routing flow are stable. Session 13 designs the review content (Overview, Evidence, Decisions, History sections) that the operator works through before the gate activates. It does not redesign the gate.
- The return trigger routing flow through the session integrity view is specified: `[Review in center surface ›]` routes to the return trigger detail. Session 13 designs what that detail view contains.
- The staleness marker vocabulary is complete. Session 13 surfaces should use the seven marker types from §8 when context changes during handoff or return trigger review.
- The maintenance vs replanning routing distinction (from Session 9 and the work plan) is the most important design problem in Session 13. The response options in the return trigger review view must distinguish these two paths visually and semantically. Session 13 must not flatten them into a single `Route to planning` action.

**Key design questions for Session 13:**

What does the Handoff Package Review View's Overview section contain? It needs: what is being handed off, approved scope, out-of-scope items, readiness basis, what transfers and what does not transfer, and the `Handoff — Prepared` vs `Handoff — Awaiting Approval` state distinction. Session 13 must design the layout of this information within the generic record detail view template from Session 9.

What do the maintenance vs replanning response options look like in the return trigger review? These must be two visually distinct options with semantically unambiguous labels. The Session 13 spec should name the options explicitly (not leave them as `Option A` / `Option B`) and show what additional context appears when each is selected.

How are the stale-basis warnings on handoff records presented before the approval gate? The handoff workflow doctrine requires that if the handoff's planning basis has changed materially since the package was prepared, a visible warning appears before the approval gate is offered. Session 13 should design the specific stale-basis warning treatment for the handoff review surface — it will resemble but be distinct from the general staleness warning from Session 10 §4.7, because the handoff stale-basis warning must describe what specifically changed in the handoff's basis (readiness? evidence? governing decision?), not just that context changed.
