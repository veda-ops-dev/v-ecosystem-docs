# Session 9 — Center Workspace Foundation
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–8 (all shell surfaces and nav trees fully specified)
**Required before:** Sessions 10–15 (all approval gates and workflow surfaces live here)

---

## 1. Files Read

- `session-02-minimal-token-decisions.md` — active token baseline
- `session-03` through `session-08` — topbar (48px), right panel (320px default), left nav (260px), three tree systems fully specified with nav item anatomy; the center workspace's available width = `calc(100vw - 260px - 320px)`
- `desktop-surface-architecture.md` — center workspace role: dense read-mostly inspection and review; opens on operator action only; required detail view types; review-before-gate routing rule
- `desktop-implementation-architecture.md` — `workspaceRouter` responsibility; center workspace components list; center workspace must own full record inspection, evidence, decision chain, gate widgets

---

## 2. Session 9 Scope Confirmation

This session produces:
- Center workspace shell: tab bar, panel chrome, empty state
- Workspace router pattern: how records from nav trees and right-panel output cards route to center views
- Generic record detail view template: the base layout all detail views share
- Detail view opening rules
- Cross-surface synchronization markers (inline banner treatment)
- Resolution of the Session 8 open question: tabs vs replace on navigate

This session does not:
- Design handoff review, return trigger review, or launch readiness review (Sessions 13–14)
- Design approval gate widgets (Session 10)
- Design individual record types in detail (each has a session or is implied by the template)

---

## 3. Resolving the Session 8 Tab Question

Session 8 posed: when the operator navigates to a record from the nav, does it open in a new tab (preserving what's open) or replace the current view?

**Resolution: Tab-based model. Navigate opens in a new tab. Tabs are closeable. Maximum 5 open tabs.**

Rationale: This application requires dense review work — comparing evidence against decisions, checking handoff basis against execution findings, reviewing signal packages alongside planning records. A replace model forces the operator to re-navigate constantly. The governance work is comparative by nature. Tabs enable that without requiring a full multi-pane layout.

**Tab constraints:**
- Maximum 5 open tabs. At the 5th, opening a 6th closes the least-recently-used non-pinned tab.
- Tabs are not pinnable in this version — that is Session 22/23 refinement territory.
- The tab bar is always visible when at least one view is open.
- Tabs are closeable via an `×` on hover.
- The active tab is visually distinct (selected treatment).

---

## 4. Center Workspace Shell

### Dimensions

```
Width:  calc(100vw - 260px - 320px)   at default panel widths
         ≈ 740px on a 1366px display
         ≈ 1100px on a 1920px display
Min:    480px (enforced — below this center workspace becomes unusable for review)
```

When the right panel collapses to its 40px rail (Session 5), center workspace gains ~280px. When the right panel is at max width (440px), center workspace shrinks accordingly.

### Background

`--surface-base: #1a1f23` — the center workspace sits one level below the nav panels and right panel in elevation, reinforcing that the panels are the chrome and the workspace is the work surface.

### Top boundary

The workspace top edge is directly below the topbar (48px). No additional gap. The workspace and topbar are flush.

### Layout structure

```
┌────────────────────────────────────────────────────────┐
│  TAB BAR                                       48px    │
│  [Tab 1 ×] [Tab 2 ×] [+ New Tab]                      │
├────────────────────────────────────────────────────────┤
│  VIEW HEADER                                   56px    │
│  [Record type label]  [Record title]  [Record ID]     │
│  [Inline banner — appears here when active]           │
├────────────────────────────────────────────────────────┤
│                                                        │
│  VIEW BODY                        flex: 1, scrollable  │
│  (record content, sections)                           │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 5. Tab Bar

### Height: 48px — matches topbar height

This alignment is intentional. The tab bar and topbar form a continuous 48px horizontal band across the top of the application. Visually they are at the same level; functionally they are distinct surfaces (topbar is persistent state; tab bar is workspace navigation).

### Tab anatomy

```
[● Record type icon]  [Tab label — truncated]  [×]
```

- Tab label: `--type-sm` (13px), `--weight-medium`, `--text-primary` when active, `--text-secondary` when inactive
- Record type icon: 12px colored dot or icon indicating record type (see §8 Record Type Identifiers)
- `×` close: appears on hover, `--text-tertiary`, transitions to `--text-secondary` on hover
- Tab width: min 120px, max 220px; tabs shrink equally when space is constrained
- Tab height: 40px (centered in the 48px bar with 4px bottom border active treatment)
- Active tab: bottom border 2px `--accent-primary`, background `--surface-base` (blends with workspace)
- Inactive tab: no bottom border, background `--surface-raised` (slightly elevated — matches nav panel level)
- Hover on inactive: `--state-hover-overlay`

### Tab bar background

`--surface-raised` — sits slightly above the workspace body, creating a physical sense that tabs are "sitting on top of" the workspace.

### Tab bar bottom border

`border-bottom: 1px solid var(--border-subtle)` — separates tab bar from view header.

### `+ New Tab` affordance

A `+` icon at the right end of the tab strip, `--text-tertiary`, transitions to `--text-secondary` on hover. Clicking opens a minimal record search/navigation prompt (Session 21 territory — for now just opens an empty workspace state).

### Empty tab bar (no views open)

Tab bar is present but shows no tabs and no `+ New Tab` until the operator navigates to a record. The empty workspace state (§7) is shown in the view body area.

---

## 6. View Header

### Height: 56px

The view header is the identity band of the currently active view. It does not scroll — it sticks to the top of the view body area.

### Content

```
[Record type badge]  [Record title]                    [Record ID]  [⋯]
```

- **Record type badge:** Small colored chip showing the record type — `OBJECTIVE`, `HANDOFF`, `SIGNAL PACKAGE`, `EXECUTION ENTRY`, etc. Background: type-color at 10% opacity. Text: `--type-xs`, `--weight-bold`, type-color.
- **Record title:** `--type-lg` (16px), `--weight-semibold`, `--text-primary`. Truncated with ellipsis if longer than available width.
- **Record ID:** `--font-mono`, `--type-xs`, `--text-tertiary`. Right-aligned.
- **`⋯` overflow:** Small overflow menu for view-level actions: `Copy record ID`, `Open in new tab`, `Reveal in nav`. Non-governance actions only.

### View header background

`--surface-raised` — same as the tab bar. The header and tab bar form a unified chrome layer above the view body.

### View header bottom border

`border-bottom: 1px solid var(--border-default)` — clear separation from scrollable view body.

### Inline banner position

When a cross-surface synchronization event requires a banner (e.g., a governing decision loaded in this view was superseded), the banner appears **between the view header and the view body**, as a non-scrolling element:

```
┌──────────────────────────────────────────────────────────┐
│  VIEW HEADER                                    56px     │
├──────────────────────────────────────────────────────────┤
│  ⚠ GOVERNING CONTEXT CHANGED — [dec-05] superseded...   │  ← inline banner
│  [Review Change]                                         │
├──────────────────────────────────────────────────────────┤
│  VIEW BODY (scrolls)                                     │
```

Inline banner anatomy:
- Background: `--staleness-bg` (warning) or `--state-danger-bg` (error/block)
- Left border: 3px `--staleness-border` or `--state-danger`
- Text: `--type-sm`, `--staleness-text` or `--state-danger`
- Padding: `--space-3` (12px) vertical, `--space-4` (16px) horizontal
- Action link: `--text-link`, `--type-sm` — e.g., `[Review Change]`, `[Reload Context]`
- Non-dismissible for blocking events; dismissible (×) for informational events

Multiple banners can stack if multiple events are active simultaneously. They stack vertically in the header-to-body gap.

---

## 7. Empty Workspace State

When no tabs are open (fresh session, or operator closed all tabs):

```
                        ◈

              Select a record to review.

        Navigate using the left panel,
        or follow a link from an output card.

```

Centered vertically and horizontally in the workspace. `◈` in `--text-tertiary` at `--type-xl` (20px). Text in `--text-tertiary`, `--type-sm`. No suggested records, no shortcuts. Clean and neutral.

---

## 8. Record Type Identifiers

Every tab and view header uses a record type badge. This is the first place in the spec where record types across all three systems need a unified identity vocabulary. The colors are drawn from the system they belong to.

| Record type | System | Badge color | Badge label |
|---|---|---|---|
| Objective | Project V | `--text-primary` | `OBJECTIVE` |
| Initiative | Project V | `--text-primary` | `INITIATIVE` |
| Work Item | Project V | `--text-primary` | `WORK ITEM` |
| Handoff | Project V | `--state-warning` | `HANDOFF` |
| Decision Record | Project V | `--accent-primary` | `DECISION` |
| Gap | Project V | `--state-danger` | `GAP` |
| Signal Package | VEDA | `--state-info` | `SIGNAL PKG` |
| Observatory Domain | VEDA | `--state-info` | `OBS DOMAIN` |
| Provider | VEDA | `--state-info` | `PROVIDER` |
| Execution Entry | V Forge | `--accent-primary` | `EXEC ENTRY` |
| Content Page | V Forge | `--accent-primary` | `PAGE` |
| Execution Finding | V Forge | `--state-warning` | `FINDING` |
| Surface | V Forge | `--accent-primary` | `SURFACE` |
| Return Trigger | Cross-system | `--state-danger` | `RTN TRIGGER` |
| Approval Request | Cross-system | `--state-pending` | `APPROVAL REQ` |

Badge background: listed color at 10% opacity. Badge text: listed color, `--type-xs`, `--weight-bold`.

---

## 9. Workspace Router Pattern

The `workspaceRouter` is the single entry point that all navigation actions flow through. No surface opens a center view directly — they all call the router.

### Routing sources

1. **Left nav item click** — passes record type + record ID
2. **Right-panel output card detail link** — passes record type + record ID
3. **`[Proceed to Approval Gate]` button** — passes record type + record ID + intent `approval_gate`
4. **`[Review]` link in context strip INTEGRITY row** — passes item type + item ID
5. **Inline banner action link** (e.g., `[Review Change]`) — passes record type + record ID
6. **`+ New Tab` / command palette** — passes search or empty intent

### Router behavior

```
workspaceRouter.navigate(recordType, recordId, intent?)
```

1. Check if the record is already open in an existing tab — if yes, activate that tab (no duplicate)
2. If not open and tabs < 5: open a new tab, load the record detail view
3. If tabs = 5: close least-recently-used tab, open new tab
4. Set the new tab as active
5. Load view content via `apiClient` (IPC → sidecar → backend)
6. While loading: tab shows a loading shimmer in the view body
7. On load: render the generic record detail view template (§10) or a specialized view type

### Intent-aware routing

When `intent = 'approval_gate'`, the router:
- Opens the record detail view normally
- After the view loads, scrolls to and activates the approval gate section
- The gate widget activates only after required review checkpoints are confirmed (Session 10 spec)

---

## 10. Generic Record Detail View Template

Every record detail view — regardless of system or record type — is built on this template. Specialized views (handoff review, return trigger review, etc.) extend it but do not replace its structure.

### Template layout

```
┌────────────────────────────────────────────────────────┐
│  VIEW HEADER (non-scrolling, from §6)                  │
├────────────────────────────────────────────────────────┤
│  [Inline banner if active]                             │
├────────────────────────────────────────────────────────┤
│                                                        │
│  SECTION NAV (horizontal tab strip)                    │
│  [Overview] [Evidence] [Decisions] [History] [Actions] │
│                                                        │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ACTIVE SECTION BODY (scrolls)                         │
│                                                        │
│  [Section content — record-type specific]              │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### Section nav

A horizontal strip of section labels directly below the inline banner position (or view header border if no banner). Not to be confused with the workspace tab bar above — this is intra-record section navigation.

- Height: 40px
- Section label: `--type-sm`, `--weight-medium`, `--text-secondary` inactive; `--text-primary` active
- Active section: bottom border 2px `--border-accent` (`--accent-primary`)
- Background: `--surface-raised` — same as view header, creating a unified header block
- Separator from body: `border-bottom: 1px solid var(--border-subtle)`

**Standard sections (not all sections appear on every record type):**

| Section | Appears on |
|---|---|
| `Overview` | All record types — always first |
| `Evidence` | Records with evidence links or VEDA references |
| `Decisions` | Records governed by decisions |
| `History` | Records with state change history or event log |
| `Actions` | Records where operator actions are available |
| `Findings` | Execution entries, return triggers |
| `Graph` | Content pages, execution entries (content graph context) |

Records that have no relevant content for a section omit that section tab entirely. An Objective record might show Overview, Evidence, Decisions, History, Actions. A Signal Package might show Overview, Evidence, History.

### Section body content principles

**Overview section:** The essential facts about the record. What it is, what it represents, its current status, when it was created, what project it belongs to. Dense but scannable. Uses a two-column label/value layout for metadata fields, then freeform content below.

**Evidence section:** Evidence records linked to this record. Each evidence item shows: record ID (`--font-mono`), source system (with ownership label if cross-system), capture timestamp, trust posture, freshness marker. Staleness markers applied per Session 4 vocabulary.

**Decisions section:** Governing decisions that apply to this record. Named list — not a count. Each decision shows: decision ID, title, date, status. Conflict markers if applicable.

**History section:** State change log. Each entry: timestamp, what changed, who/what triggered it. Read-only. Non-canonical events (LLM outputs, continuity artifacts) are visually distinguished from canonical state changes.

**Actions section:** Operator-available actions for this record in its current state. These are governed command-path actions — not inline mutation buttons. Each action shows: action label, class badge (A/B/C), brief description of what it does. Clicking routes through the governed command path. Class B and C actions route to the approval gate flow (Session 10).

**Gate widget location:** When a record has a pending approval and the operator has navigated here via `[Proceed to Approval Gate]`, the gate widget appears at the bottom of the Actions section — not embedded in Overview. It is never the first thing the operator sees. The operator sees the full record context first; the gate appears after review. This is the review-before-gate requirement implemented as layout.

### Section body background

`--surface-base` — one level below the header/section-nav chrome. The body is the work surface; the header chrome sits above it.

### Section body padding

`--space-6` (24px) top, `--space-5` (20px) sides, `--space-8` (32px) bottom. Generous padding — this is dense review content that benefits from breathing room.

---

## 11. Cross-Surface Synchronization Markers

When a record loaded in the center workspace is affected by an invalidation event, a banner appears in the view header area (§6 inline banner position). Each event type has a specific banner treatment:

**Decision superseded (EVENT-02):**
```
⚠ GOVERNING CONTEXT CHANGED
[dec-05] has been superseded by [dec-07]. This record may have referenced the prior decision.
[Review Change]
```
Warning treatment. Dismissible after `[Review Change]` is clicked.

**Prior approval invalidated (EVENT-06):**
```
⚠ PRIOR APPROVAL INVALIDATED
The approval for this record is no longer valid. Review required before proceeding.
[Reload Context]
```
Warning treatment. Non-dismissible until context is reloaded.

**Evidence stale while record is open (EVENT-08):**
```
⚠ EVIDENCE BASIS MAY BE STALE
Evidence supporting this record has become stale. Review evidence before approval.
[View Evidence]
```
Warning treatment. Dismissible.

**Session error while record is open (EVENT-10):**
```
⛔ SESSION ERROR
This view is read-only until the session is re-initialized.
[Re-initialize Session]
```
Danger treatment. Non-dismissible. All actions in the Actions section disabled.

**Local state divergence (EVENT-18):**
```
⚠ LOCAL STATE WARNING
This record may reflect local state that has not been confirmed against backend.
[Verify]
```
Warning treatment. Non-dismissible until verified.

---

## 12. Detail View Opening Rules

**Detail views open only on operator action.** No view opens automatically. This is a hard rule from doctrine.

**Triggers that open a detail view:**
1. Clicking a tree item in the left nav
2. Clicking a detail link from a right-panel output card
3. Clicking `[Proceed to Approval Gate]` on an Approval Request Package card
4. Clicking `[Review]` on a context strip INTEGRITY item
5. Clicking an inline banner action link (e.g., `[Review Change]`)
6. Explicit command palette navigation (Session 21)

**What does NOT open a detail view:**
- An invalidation event (no auto-open on context change)
- An LLM output that mentions a record (mention ≠ navigation)
- A return trigger arriving (topbar badge and INTEGRITY row update; view does not auto-open)

---

## 13. Empty and Loading States Within Views

### Loading state (record is being fetched)

The view body shows a skeleton layout — the section nav appears with tabs, the Overview tab is active, and the body shows shimmer placeholders at the typical height of label/value pairs. The shimmer uses `--state-hover-overlay` pulse on `--surface-raised` background. Duration: `--duration-moderate` (300ms) per shimmer cycle.

The record type badge and title in the view header show `Loading…` in `--text-tertiary` while the record loads.

### Record not found

If a record navigated to no longer exists (was deleted or is out of scope):

```
◈  Record not found

   This record is no longer available in the current project scope.
   It may have been deleted or the project scope may have changed.

   [Close Tab]
```

Centered in view body. `◈` in `--text-tertiary`, `--type-xl`. Text in `--text-tertiary`, `--type-sm`.

### Record access denied (403)

Same treatment as not found, different message:

```
◈  Access restricted

   This record is outside the current session scope.
   Switch to the project that owns this record to view it.

   [Close Tab]
```

Doctrine requires 403 and 404 to have distinct but non-disclosing error messages. The operator sees enough to understand they need to change project scope without the application revealing whether the record exists in another project.

---

## 14. Token Usage from Session 2

No new tokens. All values from Session 2.

| Element | Token(s) |
|---|---|
| Workspace background | `--surface-base` |
| Tab bar + view header background | `--surface-raised` |
| Tab bar bottom border | `--border-subtle` |
| Active tab bottom border | 2px `--accent-primary` |
| Active tab label | `--type-sm`, `--weight-medium`, `--text-primary` |
| Inactive tab label | `--text-secondary` |
| View header title | `--type-lg`, `--weight-semibold`, `--text-primary` |
| View header record ID | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Record type badge | type-color at 10% opacity bg, `--type-xs`, `--weight-bold` |
| Inline banner warning | `--staleness-bg`, `--staleness-border`, `--staleness-text` |
| Inline banner danger | `--state-danger-bg`, `--state-danger` |
| Section nav labels active | `--text-primary`, `--weight-medium`, bottom border `--border-accent` |
| Section nav labels inactive | `--text-secondary` |
| Section nav background | `--surface-raised` |
| Section body background | `--surface-base` |
| Section body padding top | `--space-6` (24px) |
| Section body padding sides | `--space-5` (20px) |
| Loading shimmer | `--state-hover-overlay` pulse |
| Empty state text | `--text-tertiary`, `--type-sm` |
| Empty state `◈` | `--text-tertiary`, `--type-xl` |

---

## 15. What This Session Resolves

- Tab-based navigation model is resolved: tabs open on navigate, max 5, close via `×`, least-recently-used closes at max.
- Center workspace shell is fully specified: tab bar (48px), view header (56px), section nav (40px), scrollable section body.
- Workspace router pattern is specified: single entry point, all surfaces route through it, duplicate detection, intent-aware routing for approval gate flow.
- Generic record detail view template is specified: Overview / Evidence / Decisions / History / Actions sections; gate widget appears in Actions, after review, not before.
- Inline banner position is specified: between view header and section nav — non-scrolling, above content.
- Record type identifier vocabulary covers all record families across all three systems.
- Detail view opening rules are explicit: operator action only, enumerated triggers, enumerated non-triggers.
- Cross-surface sync markers (inline banners) are specified for the five most critical invalidation events.
- 403 vs 404 handling is distinct but non-disclosing per doctrine.
- TIER 2 Shell Backbone is now complete. Sessions 3–9 have produced a fully specified shell: topbar, context strip, right panel shell, left nav shell, all three system trees, and the center workspace foundation.

---

## 16. What This Session Does Not Resolve Yet

- **Approval gate widgets** (Class B inline, Class C modal, escalation banner) — Session 10. The gate widget placement is specified here (Actions section, bottom, after review); the gate widget design is Session 10.
- **Review-to-gate routing flow detail** — Session 11 specifies the full five-step transition from output card to approval event.
- **Specific workflow detail views** — handoff review (Session 13), return trigger review (Session 13), launch readiness (Session 14). The generic template is the foundation; these add specialized section content and workflow-specific banners.
- **Content graph full view** — referenced in Session 8 (V Forge tree content graph section navigates here); needs its own specialized section content beyond the generic template.
- **VEDA signal package detail view** — referenced in Session 7; needs specialized sections for evidence chain, trust posture, and routing controls.
- **Tab persistence across sessions** — whether open tabs are restored on session restart. Deferred to Session 22/23.

---

## 17. Recommended Inputs to Session 10

Session 10 is Approval Gate Surfaces — Class B inline widget, Class C modal, typed confirmation, escalation banner.

**What Session 10 inherits from this session:**
- The gate widget lives in the Actions section of the generic record detail view template, at the bottom, only after required review checkpoints are satisfied
- The review-before-gate routing is enforced by layout (the operator sees the full record first) and by the `intent = 'approval_gate'` router behavior (scroll to gate after load)
- Inline banners for stale context appear above the view body and the operator must acknowledge them before the gate activates — this is enforced by the banner's non-dismissibility until `[Review Change]` or `[Reload Context]` is clicked

**Session 10 must specify:**
1. The Class B inline gate widget: approval request summary, action class badge, Approve/Reject/Defer controls — positioned at the bottom of the Actions section, inactive until review checkpoints complete
2. The Class C modal: triggered from within the center workspace only, after all checkpoints; typed confirmation input (not a checkbox, not pre-populated, specific phrase required)
3. Checkpoint mechanism: what "required review checkpoints" means concretely — what must the operator have done before the gate activates? This is the most important design decision in Session 10 and it must be stated as concrete criteria, not "after reviewing the record."
4. The escalation banner (Class D): non-dismissible, `[Escalate]` and `[Document and Hold]` controls, appears as an inline banner at the top of the view rather than a modal
5. Staleness check before gate presentation: the gate widget must not activate if relevant context (decisions, evidence) has changed since the approval request was produced — the staleness banner blocks the gate until acknowledged
