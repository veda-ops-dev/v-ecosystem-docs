# Session 6 — Left Nav Shell + Project V Tree
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Session 2 (Tokens), Session 3 (Topbar), Session 4 (Context Strip), Session 5 (Right Panel Shell)
**Required before:** Sessions 7–8 (VEDA and V Forge trees build directly on the shell established here)

---

## 1. Files Read

- `session-02-minimal-token-decisions.md` — active token baseline
- `session-03-topbar-spec.md` — system switcher in topbar; topbar is the canonical system authority
- `session-05-right-panel-shell-spec.md` — panel widths established; Session 5 open question about nav system switcher posed for this session to resolve
- `desktop-surface-architecture.md` — left panel role, required system views (Project V / VEDA / V Forge), action placement rules, anti-affordance rules, left panel must contain no approval gates
- `operator-surface-interfaces.md` — Project V operator surface: what operators may do, what requires approval, what they must not do directly
- `workflows/handoff-workflow.md` — handoff status vocabulary: `proposed`, `active`, `blocked`, `ready`, `handed_off`, `accepted`, `closed`; prepared vs awaiting approval distinction
- `workflows/project-intake-workflow.md` — intake workflow stages; no settled schema record anchor; intake section in nav must reflect this honestly

---

## 2. Session 6 Scope Confirmation

The work plan defines Session 6 as: the left navigation shell and the Project V system's tree content.

This session produces:
- Navigation shell (panel width, header, system switcher, scroll behavior, panel chrome)
- Project V tree structure: objective tree, initiative tree, work items, gaps section, handoffs section, return trigger visibility
- Status indicator visual vocabulary for all recognized tree item states
- Per-item action affordances (navigate only; governed command path for mutations)
- The system switcher question resolution from Session 5

This session does not:
- Design the VEDA tree (Session 7)
- Design the V Forge tree (Session 8)
- Design the center workspace (Session 9)
- Design approval gate surfaces (Session 10)

---

## 3. Resolving the Session 5 System Switcher Question

Session 5 posed the question: does the left nav's system switcher switch the full session system (same as the topbar), or just swap the nav tree view without changing session system?

**Resolution: The left nav system switcher IS the same action as the topbar system switcher. They are one control expressed in two places, and both trigger EVENT-11 (Current System Changed) identically.**

Rationale:

The current system designation governs the LLM's output posture, the action class table, and the tool surface. There must be exactly one current system at any time — not a "nav view system" that differs from the "session system." If the left nav could show a different system's tree than what the topbar declares as current, the shell would be teaching two conflicting realities simultaneously. The operator would see VEDA content in the nav while the context strip, topbar, and LLM are all operating under Project V posture. That is a synchronization failure.

**What this means for the left nav header:**

The system switcher in the nav header is a full system switch. Selecting VEDA in the nav header changes the session's current system to VEDA — the topbar system indicator updates, the context strip reloads for VEDA, the LLM posture changes. The two controls are mirrors of each other.

The topbar system switcher remains the primary visual authority (per Session 3 — it is always visible, positioned prominently in the topbar). The left nav system switcher is the contextually convenient equivalent for when the operator's attention is in the nav.

**Implication for design:** The active system in the nav header must always match the topbar system indicator. They show the same state. They trigger the same event. There is no condition where they differ.

---

## 4. Left Nav Shell

### Panel dimensions

```
--panel-left-nav-width:  260px   (from Session 2 spatial constants)
--panel-border-width:    1px
```

Height: full viewport height minus topbar (`calc(100vh - 48px)`), same as the right panel.

Background: `--surface-raised` — same surface level as the right panel. The two panels are at the same elevation; the center workspace at `--surface-base` sits one level below.

Right border: `border-right: 1px solid var(--border-subtle)` — a minimal structural separator from the center workspace. No shadow on this edge; the left nav is flush with the shell, not floating above it.

### Panel regions

The left nav panel has three stacked regions:

```
┌──────────────────────────────┐  ← top of panel
│  NAV HEADER                  │  fixed height: 48px (matches topbar height)
│  [project scope] [system ▾]  │
├──────────────────────────────┤
│                              │
│  TREE CONTENT                │  flex: 1 — scrollable
│  (system-specific tree)      │
│                              │
├──────────────────────────────┤
│  NAV FOOTER                  │  fixed height: 40px
│  [+ New…] [session tools]    │
└──────────────────────────────┘
```

### Nav header (48px)

The header is 48px — aligned with the topbar height so it forms a continuous horizontal band across the top of the shell with the topbar.

**Contents:**

Left side: project scope label — `◈` prefix glyph + project name, truncated with ellipsis if necessary. This is a read-only label, not a clickable control. Project switching is done in the topbar. The nav header shows the current project scope for orientation.

- Text: `--type-sm` (12px), `--weight-medium`, `--text-secondary`
- Prefix `◈`: `--text-tertiary`, `--type-xs`
- Max width: 120px before truncation

Right side: system switcher.

**System switcher in nav header:**

- Shows the current system abbreviated: `V:` / `OBS:` / `FRG:` prefix + system name
- Same color coding as the topbar (Project V: `--text-primary`; VEDA: `--state-info`; V Forge: `--accent-primary`)
- Dropdown arrow `▾`: `--text-tertiary`, `--type-xs`
- Background: transparent resting; `--state-hover-overlay` on hover
- Border: none resting; `--border-subtle` on hover
- Height: 28px, padding `--space-2` (8px) horizontal
- Clicking opens the same three-option popover as the topbar (Project V / VEDA / V Forge with `✓` on current)
- Selecting a different system triggers EVENT-11 exactly as the topbar does
- The topbar updates simultaneously (both are mirrors of the same state)

**Header bottom border:** `border-bottom: 1px solid var(--border-subtle)`

### Tree content region

The tree region is a single scrollable container. The scroll is the panel's native scroll — not a sub-scroll within a fixed-height container. The tree can be as tall as needed; the panel scrolls.

No sticky section headers within the tree. All sections scroll together. This is intentional: sections higher in the tree (Objectives, Initiatives) and sections lower (Gaps, Handoffs) should be equally accessible without separate scroll regions that create nested scroll complexity.

**Scroll behavior:** Standard vertical scroll. The nav header and footer are fixed (sticky) while the tree content scrolls between them. This is the standard sticky-header pattern.

### Nav footer (40px)

The footer contains global nav-level commands that are available regardless of which system tree is active.

**Contents:**

- `+ New…` — opens a bounded command menu for creating a new governed record. This is not an inline creation form — it opens a command menu (designed in Session 21) that routes to the appropriate creation path for the current system. The `+` icon is `--text-tertiary`; the label is `--type-xs`, `--text-secondary`.
- Rightmost: a `⋯` overflow menu for session-level nav tools (e.g., collapse all tree sections, copy current tree state for reference). Low priority; its exact contents are Session 21 territory.

The footer uses `border-top: 1px solid var(--border-subtle)` to separate it from the tree region.

**The `+ New…` command is not a creation shortcut.** It does not create a record directly. It opens the governed command path for creation. This distinction matters: the nav footer must not become a place where records are created without routing through the governed path.

---

## 5. Project V Tree Structure

When the current system is Project V, the tree content region shows the Project V planning tree. The tree is organized in sections, each with a section header and an expandable list of items.

### Section order (top to bottom)

```
OBJECTIVES
INITIATIVES
WORK ITEMS
GAPS
HANDOFFS
INTAKE          ← schema-blocked; honest treatment
RETURN TRIGGERS ← only shown when active
```

This order reflects the planning hierarchy: strategic → tactical → execution-ready → exceptions → intake. The RETURN TRIGGERS section floats up when triggers are present (see §5.7).

### 5.1 Section header anatomy

Each section has a header row:

```
[›] SECTION LABEL                [count badge]
```

- `›` / `⌄` expand/collapse chevron: `--text-tertiary`, `--type-xs`
- Section label: `--type-xs` (11px), `--weight-semibold`, `--text-tertiary`, letter-spacing 0.3px — same as context strip category labels
- Count badge: integer in `--type-xs`, `--weight-bold`, `--text-tertiary`, shown only when count > 0; no badge when section is empty
- Section header height: 28px
- Section header padding: `--space-3` (12px) left, `--space-2` (8px) right
- Hover: `--state-hover-overlay`
- Collapsed by default if section has no items; expanded by default if section has items

**Section headers are expandable/collapsible but not navigable.** Clicking a section header only expands or collapses; it does not navigate anywhere. Navigation happens by clicking individual tree items.

### 5.2 Tree item anatomy

Each item in the tree follows this structure:

```
[indent] [status dot] [item label]          [action ›]
```

- Indent: `--space-4` (16px) per depth level
- Status dot: 8px circle, colored by status (see §6)
- Item label: `--type-sm` (13px; matching `--type-base`), `--weight-normal`, `--text-primary`; truncated with ellipsis at panel width
- `[action ›]`: appears on hover, right-aligned. A single right-arrow glyph (`›`) in `--text-tertiary` that indicates the item is navigable. On click, opens the record detail in the center workspace.
- Row height: 32px
- Row left padding: `--space-3` (12px) base + indent depth
- Row right padding: `--space-3` (12px)
- Hover: `--state-hover-overlay`
- Selected (item currently open in center workspace): `--state-selected-bg` (amber at 12%), left border 2px `--accent-primary`

**Every tree item is navigable to a center workspace detail view.** Clicking any item navigates. The item does not expand inline — detail belongs in the center workspace.

**No inline editing.** No inline status toggles on tree items. State changes (e.g., `proposed → active`) route through the governed command path, not through the nav tree.

### 5.3 Objectives section

Shows all Objectives for the current project, with their status and health.

**Item label format:** Objective short name / title.

**Status dot colors:** See §6 status vocabulary.

**No depth nesting within Objectives.** Objectives are a flat list in the nav. Their child Initiatives appear in their own section below. This keeps the nav readable without deep nesting.

**Empty state:**
```
OBJECTIVES
  No objectives defined
```
Text in `--text-tertiary`, `--type-xs`, indented at `--space-4`.

### 5.4 Initiatives section

Shows all Initiatives across all Objectives for the current project. Grouped by parent Objective.

**Grouping treatment:**

```
INITIATIVES                              [4]
  [obj label — truncated]                    ← group header, non-navigable
    [●] Initiative A                      ›
    [●] Initiative B                      ›
  [obj label 2]
    [●] Initiative C                      ›
```

Group headers (parent objective names) are `--type-xs`, `--text-tertiary`, non-navigable, non-hoverable. They are visual anchors only.

Initiatives are indented one level within their group.

**If an initiative has no parent objective** (orphaned or unassigned): shown under a `[unassigned]` group header in `--text-tertiary`.

### 5.5 Work Items section

Shows all Work Items across all Initiatives. Grouped by parent Initiative.

Same grouping treatment as Initiatives section. Work items are one additional indent level deeper than their parent initiative group header.

Work items with `status = blocked` are shown with `--state-danger` status dot and the item label in `--text-secondary` (slightly dimmed) to visually indicate they are blocked without removing them from the tree.

### 5.6 Gaps section

Gaps are planning-identified gaps (missing evidence, unresolved conditions, capability gaps, etc.) with severity indicators. This section is the most visually distinct — gaps use a severity-first visual hierarchy rather than the standard status dot.

**Item format:**

```
GAPS                                     [7]
  [⛔] intent gap — search vertical         ›   ← blocking
  [⚠] CWV threshold unmet                  ›   ← critical
  [⚠] evidence gap — hosting               ›   ← critical
  [ℹ] competitor reference incomplete      ›   ← warning
```

Severity icons (left of label):
- `⛔` — blocking: `--state-blocked` (#fa4362), blocks gate progress
- `⚠` — critical: `--state-warning` (#ffa100), does not block but must be resolved before handoff
- `ℹ` — warning: `--state-info` (#00b0f4), informational, non-blocking

These are icons, not status dots. They replace the standard dot for this section because severity level, not lifecycle status, is the primary signal for gaps.

**Item label:** `--type-sm`, color by severity:
- Blocking: `--state-danger`
- Critical: `--state-warning`
- Warning: `--text-primary`

**Section count badge:** Shows only blocking + critical count (not total), in `--state-warning`. If any blocking gaps exist, the badge uses `--state-danger`. This surfaces the urgency of the gap picture at a glance without counting informational items.

**Empty state (no gaps):**
```
GAPS                                     ✓
  No open gaps
```
`✓` in `--state-success` in the badge position. `No open gaps` in `--text-tertiary`. A positive confirmation.

### 5.7 Handoffs section

Handoffs are the most governance-significant items in the Project V tree. They have the most complex status vocabulary and the most important visual treatment.

**Item format:**

```
HANDOFFS                                 [3]
  [●] hosting-comparison-handoff    [status badge]  ›
  [●] seo-tech-audit                [status badge]  ›
  [●] content-hub-v1                [status badge]  ›
```

**Status badges** (shown right of item label, before the `›` navigation arrow):

Status badges for handoffs are text badges, not just dots, because the distinction between states (especially `prepared` vs `awaiting_approval`) is too important to convey by color alone.

| Status | Badge text | Badge color | Status dot color |
|---|---|---|---|
| `proposed` | `proposed` | `--text-tertiary` | `--text-tertiary` |
| `active` | — (no badge) | — | `--state-success` |
| `blocked` | `blocked` | `--state-danger` | `--state-danger` |
| `ready` / prepared | `prepared` | `--state-info` | `--state-info` |
| `ready` / awaiting approval | `awaiting approval` | `--state-pending` | `--state-warning` |
| `handed_off` | `handed off` | `--state-success` | `--state-success` |
| `accepted` | `accepted` | `--state-success` | `--state-success` |
| `closed` | `closed` | `--text-tertiary` | `--text-tertiary` |

**The `prepared` vs `awaiting approval` distinction** is derived in the same way as the context strip STAGE derivation: `Handoff.status = ready` + no pending approval record = `prepared`; `Handoff.status = ready` + unsatisfied pending approval record = `awaiting approval`. The nav tree must reflect this distinction correctly. A handoff showing `prepared` when there is actually a pending unsatisfied approval is a governance error.

**Status badge anatomy:**
- Text: `--type-xs`, `--weight-bold`, colored per table above
- Background: matching color at 10% opacity
- Border: 1px matching color
- Border-radius: `--radius-pill`
- Padding: `--space-1` (4px) horizontal, 2px vertical

**Handoffs section count badge:** Shows count of `prepared` + `awaiting approval` handoffs (the ones requiring attention), not total count. `--state-warning` if any `awaiting approval` exist; `--state-info` if only `prepared` exist; no badge if all are `active`, `handed_off`, `accepted`, or `closed`.

### 5.8 Intake section (schema-blocked)

The intake section exists in the tree because intake is a real workflow activity in Project V. But the schema does not yet have a dedicated IntakeRecord or IntakeCandidate table, so this section must reflect that honestly.

**Treatment:**

```
INTAKE                                   *
  Intake tracking unavailable
  No intake record schema anchor
```

The `*` badge (same treatment as schema-pending stages in Sessions 3 and 4) is used here instead of a count. The body text `Intake tracking unavailable` is `--text-tertiary`, `--type-xs`. A secondary line `No intake record schema anchor` is `--state-schema-hold`, `--type-xs`.

**This section is collapsible but always present.** When the intake schema is settled, this section will populate with real items. Until then, it is honest about its state.

**There is no `+ New Intake` action affordance in the nav footer while the schema is unsettled.** The `+ New…` command in the footer still routes to the governed intake path when the operator chooses to initiate intake — but the nav tree cannot show a structured intake tracking view without schema anchors.

### 5.9 Return Triggers section (conditional)

This section only appears in the tree when at least one unresolved return trigger (state `arrived` or `acknowledged`) exists for the current project.

When no return triggers are active: the section is entirely absent from the tree. Unlike ORCH and CONTINUITY in the context strip (which show dormant `—`), this section does not show a dormant state — its absence communicates that there are no active triggers. The topbar attention badge and context strip INTEGRITY row cover the zero-triggers case.

**When triggers are present, this section floats to the top of the tree** — above OBJECTIVES. This is the one case where section order is not fixed. An unresolved return trigger is the highest-attention item in the Project V nav; it should be the first thing the operator sees.

**Item format:**

```
⚡ RETURN TRIGGERS                       [1]       ← section header in --state-danger
  [⚡] V Forge — intent shift            arrived ›
```

Section header uses `⚡` icon and `--state-danger` text when any triggers are in `arrived` state; `--state-warning` text when all triggers are `acknowledged` (reviewed but not resolved).

**Item status indicator:**
- `arrived`: `⚡` icon in `--state-danger`, label in `--text-primary`
- `acknowledged`: `⚡` icon in `--state-warning`, label in `--text-secondary` (reviewed, action still pending)

**Clicking a return trigger item** navigates to the return trigger detail in the center workspace. This is navigation only — the `Route` and `Dismiss` actions on the trigger live in the center workspace detail view, not in the nav tree.

---

## 6. Status Indicator Visual Vocabulary

This vocabulary applies across all Project V tree items (Objectives, Initiatives, Work Items, and partially to Handoffs). Handoffs use the badge system from §5.7 in addition to the status dot.

### Status dot color map

| Status value | Dot color token | Meaning |
|---|---|---|
| `proposed` | `--text-tertiary` | Exists, not yet active |
| `active` | `--state-success` | Currently in active governed work |
| `blocked` | `--state-danger` | Progress blocked; requires attention |
| `ready` | `--state-info` | Planning-ready; awaiting next step |
| `handed_off` | `--state-success` (dimmer) | Transferred to V Forge; planning side complete |
| `accepted` | `--state-success` | V Forge has accepted responsibility |
| `closed` | `--text-tertiary` (hollow dot) | Complete and closed |

**Hollow dot** for `closed`: the 8px dot uses a border (1px `--text-tertiary`) with transparent fill rather than a solid fill. This visually distinguishes closed items from proposed items — both are in `--text-tertiary` family, but `proposed` is solid and `closed` is hollow.

**`handed_off` vs `active`:** Both use `--state-success`, but `handed_off` uses `--accent-primary-dim` (#b89836) rather than `--state-success` to indicate successful completion with a slight distinction from actively-in-progress items.

### Status dot dimensions

8px diameter circle, `--radius-pill`, vertically centered in the 32px row height. Left margin: `--space-2` (8px) from the indent edge. Right margin: `--space-2` from the item label.

---

## 7. Per-Item Action Affordances

### Navigation (every item)

Clicking any tree item opens the record detail in the center workspace. This is the primary and only click action on tree items. The `›` glyph on hover reinforces this.

### Context menu (right-click / secondary action)

Tree items support a secondary context menu (right-click or `⋯` button appearing on hover for keyboard/trackpad users). The context menu contains only:

- `Open detail` — same as click
- `Copy record ID` — copies the record's ID to clipboard in `--font-mono` format for reference

**The context menu does not contain:**
- Approve
- Activate
- Delete
- Edit inline
- Any status transition

Status transitions route through the governed command path (`+ New…` footer → command menu). The nav tree is a view surface; mutations route through commands.

### Command path for state transitions

When an operator wants to transition a record's status (e.g., `proposed → active`, or `prepare handoff package`), they use the `+ New…` / command palette path (Session 21). The nav tree does not surface these as tree-item affordances. This is the absent-affordance rule for the left nav.

---

## 8. Panel-Level States

### Normal state (Project V active, project loaded)

Full tree as described. All sections visible per their content. Return triggers section present if active.

### Empty state (no project selected)

Tree content region shows:
```


     Select a project to view
     the planning tree.


```
Centered text in `--text-tertiary`, `--type-sm`. No sections visible. Nav header shows `◈ —` for project scope and the system switcher (still functional — the operator can switch systems even without a project).

### Loading state

Section headers appear immediately with shimmers on the item areas (same `--state-hover-overlay` pulse pattern from Session 4/5). Sections appear in order as their data loads. The tree does not hold all content behind a single loading state — sections populate as they load.

### Session error state

All items in the tree become non-interactive (`--state-disabled-opacity` on item labels). Status dots remain visible but action arrows (`›`) disappear. A non-scrolling banner appears at the top of the tree content:
```
⚠ Session error — navigation unavailable
```
`--staleness-bg`, `--staleness-text`. The nav header remains interactive (system switcher still works, as it is the path to re-initialization awareness).

---

## 9. Synchronization with Other Surfaces

### When EVENT-05 (Approval Written) fires:
The handoff that was `awaiting approval` updates to `handed_off` in the tree. The handoff's status badge refreshes. The section count badge updates. This happens automatically — the operator does not need to manually refresh the nav tree after approving.

### When EVENT-16 (Return Trigger Arrives) fires:
The RETURN TRIGGERS section appears at the top of the tree immediately. The section header and first trigger item are rendered with the `arrived` treatment. The topbar attention badge also updates (both fire simultaneously).

### When EVENT-11 (Current System Changed) fires:
The tree content region fully replaces with the new system's tree. The transition uses `--transition-fade` (300ms ease opacity): the current tree fades out, the new system's tree fades in. This is a full content swap, not a scroll. The nav header system switcher updates to show the new system in its color.

### When EVENT-17 (Workflow Stage Change) fires:
Relevant tree items may update their status dot if the stage change maps to a status change (e.g., a handoff moving from `ready` to `handed_off` after activation). The item updates in place with `--transition-default` (200ms).

### When EVENT-10 (Session Error) fires:
Tree enters session error state as described in §8.

---

## 10. Left Nav Absent-Affordance Rules

These are the absolute constraints for the left nav. Nothing on this list may appear in the nav under any circumstances.

**Governance controls (must never appear):**
- Approve button or approval gate widget of any kind
- `Authorize`, `Activate`, `Confirm` on any tree item
- Any Class B or C action button

**Mutation actions (must never appear inline):**
- Status transition buttons on tree items
- Inline edit fields on tree item labels
- Delete or archive buttons on tree items
- Handoff activation button in the tree
- Readiness evaluation trigger as an inline tree item action

**System boundary violations (must never appear in Project V tree):**
- Observatory scope configuration
- V Forge execution controls
- VEDA signal package actions
- Any action that implies Project V owns VEDA or V Forge state

**LLM interaction (must never appear):**
- Text input field
- Mode selector
- Any control that submits to the LLM from the nav panel

**Confusing labels (must never appear):**
- Any button labeled ambiguously enough to be mistaken for an approval action
- `Submit`, `Confirm`, `Accept` as tree item actions (these belong in gate surfaces only)

---

## 11. Token Usage from Session 2

No new token values introduced. All visual decisions reference Session 2.

| Element | Token(s) |
|---|---|
| Panel background | `--surface-raised` |
| Panel right border | `--border-subtle` 1px |
| Nav header height | 48px (matches `--panel-topbar-height`) |
| Nav header bottom border | `--border-subtle` 1px |
| Nav footer height | 40px |
| Nav footer top border | `--border-subtle` 1px |
| Project scope label | `--type-sm`, `--weight-medium`, `--text-secondary` |
| System switcher text | `--type-xs`, `--weight-medium`, per-system color |
| Section header label | `--type-xs`, `--weight-semibold`, `--text-tertiary`, 0.3px letter-spacing |
| Section header height | 28px |
| Section count badge | `--type-xs`, `--weight-bold`, `--text-tertiary` (or urgency color) |
| Tree item height | 32px |
| Tree item label | `--type-sm` (`--type-base` 13px), `--weight-normal`, `--text-primary` |
| Tree item indent | `--space-4` (16px) per level |
| Tree item left padding | `--space-3` (12px) |
| Status dot size | 8px, `--radius-pill` |
| Status dot `proposed` | `--text-tertiary` solid |
| Status dot `active` | `--state-success` |
| Status dot `blocked` | `--state-danger` |
| Status dot `ready` | `--state-info` |
| Status dot `handed_off` | `--accent-primary-dim` |
| Status dot `accepted` | `--state-success` |
| Status dot `closed` | hollow, `--text-tertiary` border |
| Row hover | `--state-hover-overlay` |
| Row selected | `--state-selected-bg`, left border 2px `--accent-primary` |
| Navigation arrow `›` | `--text-tertiary`, hover-visible only |
| Handoff status badge | colored per status, `--radius-pill`, text `--type-xs` `--weight-bold` |
| Gap severity icon `⛔` | `--state-blocked` |
| Gap severity icon `⚠` | `--state-warning` |
| Gap severity icon `ℹ` | `--state-info` |
| Return trigger icon `⚡` | `--state-danger` (arrived) / `--state-warning` (acknowledged) |
| Schema-pending `*` badge | `--state-schema-hold` |
| Empty state text | `--text-tertiary`, `--type-xs` |
| Positive empty state `✓` | `--state-success` |
| System switch fade transition | `--transition-fade` (300ms ease opacity) |
| Item update transition | `--transition-default` (200ms ease) |
| Session error banner | `--staleness-bg`, `--staleness-text` |

---

## 12. What This Session Resolves

- The Session 5 open question is resolved: the left nav system switcher and the topbar system switcher are the same control expressed in two places, both triggering EVENT-11. There is no separate "nav view system" distinct from the session current system.
- The navigation shell is fully specified: dimensions, header layout, tree region, footer, scroll behavior.
- The Project V tree structure is specified with seven sections (Objectives, Initiatives, Work Items, Gaps, Handoffs, Intake, Return Triggers) in their fixed order, with the Return Triggers exception for when active triggers exist.
- The handoff status vocabulary is concretely designed: `prepared` vs `awaiting approval` distinction is implemented as a text badge, not just a color, because the governance distinction matters too much to rely on color alone.
- The gaps section uses severity icons rather than status dots — a deliberate departure from the standard tree item treatment to reflect that gaps are severity-graded, not lifecycle-staged.
- The intake section is honest about its schema-blocked status without being hidden or pretending it will never exist.
- The return triggers section floats to the top when active — the one place in the nav where section order is not fixed, justified by the governance urgency of unresolved triggers.
- Status indicator vocabulary is fully specified for all recognized statuses.
- Per-item action affordances are enumerated and bounded: navigation only; mutations route through the command path.
- Absent-affordance rules are concrete and implementation-followable.
- Synchronization behavior for relevant invalidation events is specified.

---

## 13. What This Session Does Not Resolve Yet

- **VEDA tree content** — Session 7. The shell established here is the container; VEDA's content rules are substantially different (observatory domains, provider sections, signal packages, freshness posture, no planning-record affordances).
- **V Forge tree content** — Session 8. Return triggers are prominent; content graph; distinct absent-affordances.
- **The `+ New…` command menu contents** — Session 21 (Command Palette). The footer affordance is specified; its payload is not.
- **Context menu keyboard access pattern** — the `⋯` button for keyboard/trackpad users is referenced but its exact behavior is Session 23 (Component Behavior Patterns).
- **Nav collapse behavior** — the left nav panel does not have a specified collapse state in this session. The right panel has a 40px rail collapse (Session 5). Whether the left nav has an analogous collapse is not specified here. This is a usability question for Session 22/23: at narrow window widths or when the operator wants maximum center workspace space, can the left nav collapse to a rail? The answer affects the center workspace's available width. Deferred.

---

## 14. Recommended Inputs to Session 7

Session 7 is the VEDA tree. The shell from Session 6 is the container; Session 7 fills it with VEDA-specific content.

**Session 7 should design:**
1. VEDA tree structure: observatory domains, provider sections, signal packages, provider freshness/health posture
2. Groupings for ready signal packages vs. in-progress observation
3. VEDA-specific absent-affordances: no create/modify planning record controls; no execution actions; no approval controls in the tree
4. Paid data pull approval request path: navigates to governed gate path; does not trigger directly in the tree
5. Empty state for VEDA with no active observatory configurations
6. Provider health/freshness indicators — VEDA's equivalent of the gap severity icons in Project V

**Key design distinction for Session 7:**
VEDA's tree items are fundamentally different from Project V's: they represent observatory records (observation runs, signal packages, provider states), not planning lifecycle records. The status dot vocabulary from Session 6 does not directly translate — VEDA items have freshness and trust posture rather than lifecycle status. Session 7 should define VEDA's own item-level indicator vocabulary that distinguishes between "signal package ready for consumption," "observation in progress," "provider stale/degraded," and "paid data pull awaiting approval." These are not the same as `proposed` / `active` / `blocked`.
