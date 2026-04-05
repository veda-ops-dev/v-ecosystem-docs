# Session 17 — Portfolio Triage / Dashboard
## V Ecosystem Desktop UX

**Session status:** Complete *(partial schema block — all four launch readiness stage names remain schema-pending; carried forward from Session 14)*
**Depends on:** Sessions 1–15 (full shell backbone, all workflow surfaces, and the per-project execution state vocabulary established in Session 15)
**Required before:** Session 18 (Agent Transparency / Lower Trace Surface) — the portfolio triage view is the first surface that aggregates cross-project state; Session 18 builds on the attention signal vocabulary established here

---

## 1. Files Read

**Prior sessions:**
- `session-02-minimal-token-decisions.md` — active token baseline
- `session-03-topbar-spec.md` — topbar attention badges; project scope indicator; session health indicator
- `session-04-context-strip-spec.md` — SCOPE/SYSTEM/STAGE/INTEGRITY rows; stage unavailability treatment
- `session-06-left-nav-shell-project-v-tree-spec.md` — nav tree structure for reference
- `session-09-center-workspace-foundation-spec.md` — center workspace tab model; workspace router; view types
- `session-12-session-integrity-check-and-alert-notification-system-spec.md` — attention scaling hierarchy; topbar badge behavior
- `session-15-maintenance-ranking-ux-spec.md` — portfolio ranking surface (single-project foundation); priority signal vocabulary; per-project execution state vocabulary

**Doctrine:**
- `interfaces/mcp-coordination-model.md` — session token bound to ONE project; LLM cannot change scope; global tools (list projects) exist but suppressed from project scope; cross-project contamination prevention (six structural layers); project switching = deliberate operator action
- `interfaces/desktop-state-and-context-model.md` — nine state categories; project scope state is operator-set; stage names with schema-pending status; maintenance vs replanning posture visibility rule
- `interfaces/desktop-surface-architecture.md` — center workspace role; action placement rules; absent-affordance rules; what belongs in each surface

---

## 2. Session 17 Scope Confirmation

The work plan defines Session 17 — Portfolio Triage / Dashboard as: the first TIER 5 Power Feature. Cross-project read-only aggregate view, attention signal vocabulary, and the explicit position on session scope.

This session produces:
- **Explicit position on session scope** — the definitive answer to whether portfolio triage can display multiple projects or is strictly single-project per session token
- **Portfolio Triage view** — the multi-project read-only aggregate center workspace surface
- **Cross-project attention signal vocabulary** — what causes a project to surface as requiring attention
- **Heterogeneous stage display** — how the triage view shows projects at different workflow stages simultaneously without visual noise or false equivalence
- **Project card anatomy** — the per-project summary card used in the triage view
- **Triage view layout and navigation** — how the operator moves from aggregate overview to single-project work

This session does not:
- Design the lower trace surface (Session 18)
- Design the command palette (Session 21)
- Invent any new schema anchors
- Design the post-triage project-switching flow in detail (that is the desktop application's session initialization path, already specified in doctrine)

---

## 3. Explicit Position on Session Scope

**The portfolio triage view shows read-only aggregate state across multiple projects. It does not change the session scope. It does not enable governed actions for out-of-scope projects.**

This position requires explanation because the MCP coordination model is unambiguous: the session token is bound to one project. The LLM operates within that scope. The operator cannot pass a different project ID through the LLM.

But the portfolio triage view does not need the LLM to display cross-project state. It uses global read tools — the MCP coordination model explicitly acknowledges that "global tools (such as list projects) exist" and that they "do not send project scope headers." The portfolio triage view uses those global read tools to fetch summary-level state for multiple projects. It displays that state to the operator without routing any of it through the session-scoped LLM.

**What this means in practice:**

- The portfolio triage view is a frontend read surface, not an LLM-mediated surface
- It calls global API endpoints (list projects, get project summary) that are not session-scoped
- It displays the results as read-only cards — no LLM output, no ARP cards, no gate widgets
- When the operator decides to work on a specific project, they click `[Switch to this project]` — which triggers the governed project-switching flow (new session token, full context reload, topbar updates)
- Only after switching is the session scope changed; the LLM does not see other projects' data during the switch

**What this does NOT mean:**

- The triage view is not a backdoor around session scoping — it shows summaries only, not the full record detail views
- The triage view cannot initiate approvals, route triggers, or activate handoffs for out-of-scope projects
- A project that appears in the triage view as requiring attention must still be switched to before the operator can act on that attention item
- The absence of LLM mediation is the enforcement mechanism: no MCP tool call is made for out-of-scope projects; only global list/summary endpoints are called

This position is consistent with the six-layer cross-project contamination prevention model from the MCP coordination model. The portfolio triage view operates at layer 1 (human selection) and the global tool tier — it never reaches layer 2 (session token binding) for out-of-scope projects.

---

## 4. What Causes a Project to Surface as Requiring Attention

Before designing the layout, this question must be answered concretely. Vague attention signals create noise; the operator learns to ignore them. Specific, doctrine-grounded attention signals are actionable.

**A project surfaces as requiring attention in the triage view when any of the following are true:**

| Attention condition | Urgency | Display treatment |
|---|---|---|
| Unresolved return trigger (`arrived` or `acknowledged` state) | High | `⚡` red badge |
| Pending approval from prior session (not yet written) | High | `⊕` amber badge |
| Blocking gap at critical severity | High | `⛔` red badge |
| Active replanning event (`Replanning — In Progress *`) | Medium | `◈` amber badge |
| Evidence expired for a pending launch action | High | `⛔` red badge |
| Launch authorization pending | Medium | `◈` amber badge |
| Session integrity items from prior session (unresolved) | Medium | `⚠` amber badge |
| Blocking gap at warning severity | Low | `⚠` amber badge |
| Stale readiness evaluation | Low | `○` dim badge |
| No activity in N days (configurable threshold) | Informational | no badge — gray treatment on card |

**A project does not surface as requiring attention for:**
- Normal `Planning — Active` or `Execution — Active` state with no unresolved items
- Schema-pending stage derivation failures (these show `*` but are not attention items)
- Priority signal changes within the ranking surface

The attention signal vocabulary uses the same icons established throughout Sessions 3–15: `⚡` for urgent/return triggers, `⊕` for pending approvals, `⛔` for blocked/expired states, `◈` for pending authorization or replanning, `⚠` for warnings. No new icons are introduced.

---

## 5. Portfolio Triage View Layout

### 5.1 Where It Sits

The portfolio triage view opens as a center workspace tab. Tab label: `[PORTFOLIO]  Portfolio  ×`

It uses the same tab model as Sessions 9 and 15's ranking surface — a distinct view type, not the generic section-nav record detail template. No section nav strip. Single-view layout.

Triggered by:
- A `[Portfolio ›]` affordance in the left nav footer area (below the OBJECTIVES/INITIATIVES tree, above the `+ New…` footer; present regardless of which system is active)
- A command palette action (Session 21)

### 5.2 View Header

```
[PORTFOLIO]  Portfolio                                     [List ▾]  [Refresh]
All projects  ·  [N] projects  ·  [N] requiring attention
```

- `[PORTFOLIO]` badge: `--state-info` text, 10% opacity bg, `--type-xs`, `--weight-bold` — same record type badge pattern as Sessions 9, 13–15; blue/info treatment because portfolio is a cross-system surface, not owned by any single system
- `Portfolio` title: `--type-lg`, `--weight-semibold`, `--text-primary`
- `[List ▾]` view toggle: list view (default) or matrix view; `--text-secondary`, `--type-xs`
- `[Refresh]` button: `--text-link`, `--type-xs`; triggers a fresh pull from global project list API; the last refresh timestamp appears next to it in `--text-tertiary`, `--type-xs`
- Subtitle: `All projects · [N] projects · [N] requiring attention` — `--text-secondary`, `--type-xs`; the "[N] requiring attention" count is in `--state-warning` when > 0, `--text-tertiary` when 0

### 5.3 Filter Bar (below view header)

```
[All stages ▾]   [All systems ▾]   [Attention items only □]   [Sort: attention ▾]
```

- `[All stages ▾]`: filter by workflow stage — shows all or filters to a specific stage
- `[All systems ▾]`: filter by which system is the active system for each project (Project V / VEDA / V Forge)
- `[Attention items only □]`: checkbox filter — when checked, hides projects with no attention items
- `[Sort ▾]`: sort order options — `attention` (projects with highest-urgency items first, default), `name` (alphabetical), `last activity` (most recently active first), `stage`

Filter bar height: 40px. Background: `--surface-raised`. Bottom border: `--border-subtle` 1px. Filter labels: `--type-xs`, `--text-secondary`.

---

## 6. Project Card Anatomy (List View)

Each project is displayed as a card in the list view. Cards are stacked vertically. The list is the primary view — the matrix view (§7) is a compact alternative.

### 6.1 Card Structure

```
┌───────────────────────────────────────────────────────────────────────────┐
│  [attention badges]        [project name]                   [stage badge] │
│                            [project type label]             [system dot]  │
│  ─────────────────────────────────────────────────────────────────────── │
│  [attention items list — top 3, truncated]                                │
│  ─────────────────────────────────────────────────────────────────────── │
│  [execution summary]    [content graph]    [last activity]                │
│                                                              [Switch ›]   │
└───────────────────────────────────────────────────────────────────────────┘
```

Card dimensions:
- Width: full width of center workspace content area (with `--space-5` horizontal padding)
- Min-height: 96px; expands with attention items
- Background: `--surface-raised`
- Border: 1px `--border-subtle`
- Border-radius: `--radius-md` (4px)
- Left border: 3px left accent colored by highest-urgency attention item (see §6.3)
- Padding: `--space-4` (16px) all sides
- Margin bottom: `--space-3` (12px) between cards

### 6.2 Card Header Row

**Left side — attention badges:**
Up to 3 attention badges displayed as small icon+count pairs:

```
⚡ 1   ⊕ 2   ⚠ 3
```

- Icon: 12px glyph
- Count: `--font-mono`, `--type-xs`, `--weight-bold`, colored by urgency
- Gap between badge groups: `--space-2` (8px)
- If no attention items: no badges shown; left edge has 12px dead space to maintain alignment

**Center — project name and type:**
- Project name: `--type-sm` (13px), `--weight-semibold`, `--text-primary`
- Project type label: `--type-xs`, `--text-tertiary` — `content_affiliate` or `plugin_product` from V Forge controlled vocabulary; displayed as `content / affiliate` and `plugin / product` respectively (human-readable form)

**Right side — stage badge and system dot:**
- Stage badge: see §6.4 for stage display rules
- System dot: 8px dot in the system's color: Project V = `--text-primary` (neutral), VEDA = `--state-info`, V Forge = `--accent-primary`; represents the currently active system for this project

### 6.3 Left Border Accent Color

The 3px left border carries the highest-urgency attention signal for the project:

| Highest urgency item | Left border color |
|---|---|
| Unresolved return trigger, pending approval, expired evidence, critical gap | `--state-danger` (#fa4362) |
| Active replanning, launch auth pending, session integrity items, warning gap | `--state-warning` (#ffa100) |
| Stale readiness, low-priority attention items | `--state-info` (#00b0f4) at 50% opacity |
| No attention items | `--border-subtle` (default, no accent) |

This mirrors the session integrity item left-border pattern from Session 12 §4.4 — the most urgent thing about a project is immediately visible from the card's left edge color before the operator reads any text.

### 6.4 Stage Badge

The stage badge displays the project's current workflow stage. This is the most complex part of the card because projects may be at heterogeneous stages, some schema-anchored and some schema-pending.

**Stage badge anatomy:**
```
[stage label]   or   [stage label *]   or   [unavailable]
```

- Stage label text: `--type-xs`, `--weight-medium`
- Background: stage-family color at 10% opacity (see table below)
- Border-radius: `--radius-sm` (2px)
- Padding: 2px horizontal, 1px vertical

**Stage family colors:**

| Stage family | Background base | Label color |
|---|---|---|
| Planning / Intake | `--text-primary` | `--text-secondary` |
| Handoff | `--state-warning` | `--state-warning` |
| Execution / Maintenance | `--state-success` | `--state-success` |
| Return / Replanning | `--state-danger` | `--state-danger` |
| Launch Readiness / Authorization | `--state-info` | `--state-info` |
| Post-Launch | `--accent-primary` | `--accent-primary` |

**Schema-pending stages** (`*` notation): the `*` suffix is appended to the stage label text. Background and label colors are identical — the `*` is the only signal. No color change for schema-pending vs. schema-anchored. This maintains visual calm: the portfolio view should not make the schema-pending situation alarming; it is a known and expected condition.

**Stage unavailable** (derivation fails): the stage badge shows `—` (en dash) in `--text-tertiary`. No `[SCHEMA PENDING]` tag — that tag is for the detail view. In the compact portfolio card, absence is signaled by `—`.

**Why this resolves the heterogeneous stage display question from Session 15 §13:**

The stage badge is visually consistent across schema-anchored and schema-pending stages. An operator looking at a list of 8 projects where 3 have `*` stages does not see 3 broken states — they see 3 stages that are runtime-derived. The `*` is a transparency marker, not a failure indicator. Color treatment is determined by stage family, not by schema status. A project in `Execution — Maintenance *` uses the same green family as a project in `Execution — Active`. The `*` tells the operator "this is runtime-derived" without screaming "something is wrong."

### 6.5 Attention Items List

Below the card header, a list of the top 3 most urgent attention items:

```
⚡ Return trigger unreviewed — hosting-comparison-site  ·  arrived 2 days ago
⊕ Pending approval — hosting-comparison-site handoff   ·  initiated 6 days ago
⚠ Stale readiness — seo-tech-audit  ·  9 days old
```

- Each item: icon + description + age/timestamp
- Icon: 12px, colored by urgency
- Description: `--type-xs`, `--text-secondary`, truncated at 60 chars
- Age: `--type-xs`, `--text-tertiary`
- Row height: 24px
- If more than 3 attention items: `[+N more]` in `--text-link`, `--type-xs` after the third item
- If no attention items: a single line `✓ No items requiring attention` in `--state-success`, `--type-xs`

The attention items list is non-navigable from the portfolio card. It is a read-only summary. The operator must switch to the project to take action on any item. This enforces the session scope constraint: cross-project attention items are visible but not actionable without switching.

### 6.6 Execution Summary Strip

Below the attention items, a compact 3-column summary strip:

```
[execution]            [content graph]       [last activity]
Execution — Active *   47 pages · 3 critical  2 days ago
```

- Column labels: `--type-xs`, `--weight-semibold`, `--text-tertiary`, lowercase
- Column values: `--type-xs`, `--text-secondary`
- `[execution]` column: shows the V Forge execution entry status if available — `active`, `paused`, `blocked`, or `—`; follows the Session 8 execution status badge vocabulary but at `--type-xs` scale
- `[content graph]` column: page count + highest decay severity if any — `47 pages · 3 critical` in `--state-danger`, `47 pages · 5 stale` in `--state-warning`, `47 pages` with no suffix when all current
- `[last activity]` column: relative time since the project's most recent governed event — `2 days ago`, `today`, `6 hours ago`; in `--text-tertiary` if recent (< 3 days), `--state-warning` if stale (> 7 days), `--state-danger` if very stale (> 14 days with unresolved items)

### 6.7 `[Switch to this project]` CTA

Right-aligned in the card footer area, separated from the execution summary strip by `--space-2` (8px):

```
[Switch to this project ›]
```

- Width: auto (fits label)
- Height: 28px
- Background: `--surface-elevated`
- Border: 1px `--border-default`
- Text: `--text-secondary`, `--type-xs`, `--weight-medium`
- Border-radius: `--radius-md`
- Hover: `--state-hover-overlay`; border transitions to `--border-accent`; text transitions to `--accent-primary`

Clicking `[Switch to this project ›]` triggers the governed project switching flow:
1. The desktop application initializes a new session with the selected project's UUID
2. A new session token is issued; the prior token is invalidated
3. The topbar updates to show the new project scope
4. The context strip reloads for the new project
5. The left nav tree reloads for the new project
6. The session start integrity check fires if the new project has integrity items
7. The center workspace clears its open tabs (the portfolio view tab remains open but other tabs close — the operator starts fresh in the new project context)

This is the doctrine-correct path. The portfolio view cannot route the operator directly to a record in another project without a session switch. The `[Switch to this project ›]` CTA is the transition point between aggregate viewing and project-specific action.

**The `[Switch to this project ›]` CTA is the only action available on a portfolio card.** No inline approve, no inline route, no inline dismiss. The card is read-only except for this one navigation action.

### 6.8 Currently Active Project Treatment

The project that matches the current session's active project scope receives a distinct treatment:

- Left border: `--border-accent` (`--accent-primary`) regardless of attention level — the amber accent overrides the urgency color for the active project
- Background: `--surface-elevated` (one level above the resting `--surface-raised` for other cards)
- `[Switch to this project ›]` CTA is replaced with `[Currently active]` — a read-only label in `--state-success`, `--type-xs`
- A small `◈` icon in `--accent-primary` appears next to the project name

This tells the operator at a glance which project they are currently working in, and removes the redundant switch affordance for the active project.

---

## 7. Matrix View (Compact Alternate)

The matrix view is a compact grid of project tiles, useful when the operator has many projects and wants a high-level scan before drilling into list view or switching projects.

### 7.1 Layout

Each project is a tile. Tiles are arranged in a responsive grid: 3 columns at default center workspace width (~740px), 4 columns at larger widths.

Tile dimensions: 200px wide × 120px tall (fixed). `--radius-md` border-radius. `--surface-raised` background. 1px `--border-subtle` border. Left border 3px urgency accent (same rules as §6.3). `--space-2` gap between tiles.

### 7.2 Tile Content

```
┌──────────────────────────────┐ ← 3px urgency border
│  [⚡ 1]  [⊕ 2]              │ ← attention badges (top-right)
│                               │
│  [project name]               │ ← --type-sm, --weight-semibold
│  [stage badge]                │ ← compact stage badge
│                               │
│  [last activity] · [N pages]  │ ← --type-xs, --text-tertiary
└──────────────────────────────┘
```

The tile shows: attention badges (top-right corner, up to 2), project name, stage badge, last activity, and content graph page count if available. No execution summary strip — that's list view territory. No attention items list — too dense for a tile.

Clicking anywhere on a tile in matrix view: opens that project's expanded state in a side-panel flyout (§7.3) without switching the session scope.

### 7.3 Tile Flyout (Matrix View Only)

When a tile is clicked in matrix view, a 360px flyout panel slides in from the right edge of the center workspace (not the right panel — this is a center workspace element):

```
┌─────────────────────────────────────────────────────────┐
│  [project name]                            [× close]    │
│  [stage badge]  ·  [type label]                         │
│  ─────────────────────────────────────────────────────  │
│  ATTENTION ITEMS                                        │
│  [full attention items list — no truncation]            │
│  ─────────────────────────────────────────────────────  │
│  SUMMARY                                                │
│  [execution summary strip]                              │
│  ─────────────────────────────────────────────────────  │
│                         [Switch to this project ›]      │
└─────────────────────────────────────────────────────────┘
```

- Flyout width: 360px
- Flyout height: full center workspace height
- Background: `--surface-elevated`
- Border-left: 1px `--border-default`
- Box-shadow: `--elevation-overlay` on the left edge
- Z-index: `--z-overlay` (400) — overlaps the tile grid but not the right panel
- Slide-in transition: `--transition-panel` (transform 300ms `--ease-out`)

The flyout contains the full list view card content (§6.4–§6.7) in a vertical layout. It is not a new surface type — it reuses the card content in a wider, taller panel.

The `[× close]` button dismisses the flyout; the tile remains visible in the grid. Clicking a different tile updates the flyout without closing it.

---

## 8. Empty States

### 8.1 No Projects Exist

```
                    ◈

              No projects yet.

        Create a project in Project V to
        see it appear here.

```

Centered. `◈` in `--text-tertiary`, `--type-xl`. Text in `--text-tertiary`, `--type-sm`.

### 8.2 No Projects Match Filter

```
                    ○

        No projects match the current filter.

        [Clear filters]
```

`[Clear filters]`: `--text-link`, `--type-sm`.

### 8.3 Load Error

```
                    ⚠

        Portfolio data could not be loaded.

        [Retry]
```

`⚠` in `--state-warning`. `[Retry]` triggers the global list API call again.

---

## 9. Refresh Behavior

The portfolio view is a read-only snapshot, not a live feed. It does not auto-refresh. Refreshing is an explicit operator action.

**Manual refresh** (`[Refresh]` button in view header): pulls fresh summary data from the global project list API. Updates all cards simultaneously. Loading state: each card shows a subtle shimmer (`--state-hover-overlay` pulse) while the refresh is in progress. On completion: cards update in place; new attention items appear; resolved items disappear. The last refresh timestamp updates.

**Implicit refresh on return**: when the operator switches to a project, does work, and then navigates back to the Portfolio tab, the portfolio view automatically refreshes. The rationale: the operator may have resolved attention items during their work session; the portfolio should reflect that when they return.

**No real-time push**: the portfolio view does not subscribe to live event streams. Attention items do not appear and disappear dynamically without an explicit refresh. This is by design — a portfolio view that updates itself constantly while the operator is trying to read it would be unusable.

---

## 10. The Portfolio View and the Left Nav Relationship

The left nav tree shows the currently active project's structure. The portfolio view shows aggregate cross-project state. These are complementary, not redundant.

**The left nav does not change when the portfolio view is open.** The left nav always reflects the current session's active project. Opening the portfolio tab does not alter the left nav content.

**The portfolio view does not replace the left nav.** It is a center workspace tab — one of up to 5 open tabs. The operator can have the portfolio view open in one tab and a handoff detail in another. The left nav shows the handoff's project structure regardless.

**The `[Portfolio ›]` left nav footer affordance** is placed in the left nav footer area below the standard nav tree. It is present regardless of which system is active and regardless of which project is active. It is a shortcut to open the portfolio tab, not a change to the nav tree itself.

---

## 11. What the Portfolio View Cannot Do

These absent-affordances must be built into the view, not enforced by warning text.

**Cannot approve, activate, or authorize for out-of-scope projects.** No gate widgets. No `[Approve]` buttons. No `[Proceed to Approval Gate]` CTAs. The only action on a card is `[Switch to this project ›]`.

**Cannot route return triggers for out-of-scope projects.** The attention item list shows that a trigger exists; it does not offer `[Review]` or `[Route]` buttons. The operator must switch to the project.

**Cannot dismiss session integrity items for out-of-scope projects.** Read-only display only.

**Cannot change the LLM's operating context to an out-of-scope project.** The portfolio view is a frontend-only read surface. No MCP tool calls are made for out-of-scope projects. The LLM does not see other projects' data.

**Cannot show full record detail for out-of-scope projects.** Clicking an attention item row does nothing. It is display-only text. Only `[Switch to this project ›]` is actionable.

---

## 12. Synchronization with the Active Project

When the active session project has attention items resolve (e.g., a pending approval is written, a return trigger is routed), the portfolio view's card for the active project is updated on the next implicit refresh. This does not happen in real-time during the session — it happens when the operator returns to the portfolio tab (§9 implicit refresh on return).

The portfolio view does not receive EVENT-05, EVENT-16, or other invalidation events during an active work session. Those events fire against the active project's surfaces (topbar, context strip, center workspace detail views). The portfolio view is a snapshot — it reflects state as of last refresh, not as of right now.

---

## 13. Token Usage from Session 2

No new tokens introduced.

| Element | Token(s) |
|---|---|
| `[PORTFOLIO]` badge | `--state-info` text, 10% opacity bg, `--type-xs`, `--weight-bold` |
| View title | `--type-lg`, `--weight-semibold`, `--text-primary` |
| Subtitle attention count | `--state-warning` text when > 0; `--text-tertiary` when 0 |
| Filter bar | `--surface-raised`, 40px, `--border-subtle` bottom |
| Card background | `--surface-raised` |
| Card border | 1px `--border-subtle` |
| Card left accent — high urgency | 3px `--state-danger` |
| Card left accent — medium urgency | 3px `--state-warning` |
| Card left accent — low urgency | 3px `--state-info` at 50% opacity |
| Card left accent — no items | 3px `--border-subtle` |
| Card left accent — active project | 3px `--border-accent` (`--accent-primary`) |
| Active project card bg | `--surface-elevated` |
| Active project `◈` icon | `--accent-primary`, `--type-xs` |
| `[Currently active]` label | `--state-success`, `--type-xs` |
| Project name | `--type-sm`, `--weight-semibold`, `--text-primary` |
| Project type label | `--type-xs`, `--text-tertiary` |
| Stage badge — planning family | `--text-primary` 10% bg, `--text-secondary` text |
| Stage badge — handoff family | `--state-warning` 10% bg, `--state-warning` text |
| Stage badge — execution family | `--state-success` 10% bg, `--state-success` text |
| Stage badge — return/replanning family | `--state-danger` 10% bg, `--state-danger` text |
| Stage badge — launch family | `--state-info` 10% bg, `--state-info` text |
| Stage badge — post-launch family | `--accent-primary` 10% bg, `--accent-primary` text |
| Stage badge `*` suffix | same color as label text, `--type-xs` |
| Stage unavailable `—` | `--text-tertiary` |
| Attention badge icon | 12px, colored by urgency |
| Attention badge count | `--font-mono`, `--type-xs`, `--weight-bold`, urgency color |
| Attention item row icon | 12px, urgency color |
| Attention item description | `--type-xs`, `--text-secondary` |
| Attention item age | `--type-xs`, `--text-tertiary` |
| `✓ No items` | `--state-success`, `--type-xs` |
| `[+N more]` | `--text-link`, `--type-xs` |
| Execution summary column labels | `--type-xs`, `--weight-semibold`, `--text-tertiary` |
| Execution summary values | `--type-xs`, `--text-secondary` |
| Content graph decay `critical` suffix | `--state-danger`, `--type-xs` |
| Content graph decay `stale` suffix | `--state-warning`, `--type-xs` |
| Last activity recent | `--text-tertiary`, `--type-xs` |
| Last activity stale (> 7 days) | `--state-warning`, `--type-xs` |
| Last activity very stale (> 14 days, items) | `--state-danger`, `--type-xs` |
| `[Switch to this project ›]` resting | `--surface-elevated`, `--border-default`, `--text-secondary`, `--type-xs` |
| `[Switch to this project ›]` hover | `--border-accent`, `--accent-primary` text |
| Matrix tile dimensions | 200px × 120px fixed |
| Matrix tile gap | `--space-2` (8px) |
| Tile flyout width | 360px |
| Tile flyout border | 1px `--border-default` left |
| Tile flyout shadow | `--elevation-overlay` |
| Tile flyout z-index | `--z-overlay` (400) |
| Tile flyout transition | `--transition-panel` (300ms `--ease-out`) |
| Load shimmer | `--state-hover-overlay` pulse |
| `[Portfolio ›]` left nav footer | `--text-link`, `--type-xs` |

---

## 14. What Session 17 Resolves

- The session scope question is answered definitively: portfolio triage shows read-only aggregate state across multiple projects using global read tools; it does not change the session scope; it does not enable governed actions for out-of-scope projects; the LLM never sees out-of-scope project data.
- The cross-project attention signal vocabulary is specified concretely: 10 conditions, each with urgency level and display treatment, using only icons and colors already established in Sessions 3–15.
- The heterogeneous stage display problem is solved with the stage badge pattern: schema-anchored and schema-pending stages use identical color treatment (determined by stage family, not schema status); `*` signals runtime-derivation without alarm; unavailable stages show `—` without `[SCHEMA PENDING]` tags (those belong in detail views, not portfolio cards).
- The project card anatomy is fully specified: left border urgency accent, attention badges, stage badge, attention items list (top 3, truncated), execution summary strip, `[Switch to this project ›]` CTA.
- The actively-scoped project's distinct card treatment is specified: amber left border, elevated background, `◈` icon, `[Currently active]` replacing the switch CTA.
- The matrix view is specified as a compact tile grid with tile flyout — a secondary view for operators with many projects, reusing list view card content without inventing new patterns.
- The absent-affordances are explicit and structural: no action buttons on out-of-scope project cards except `[Switch to this project ›]`. The portfolio view cannot approve, route, dismiss, or take any governed action for a project the operator has not switched to.
- The refresh model is explicit: manual + implicit-on-return, no real-time push. A portfolio view that updates itself constantly while being read is unusable.
- TIER 5 Power Features is opened. The portfolio view is the first surface in the application that aggregates state across the session boundary.

---

## 15. What Session 17 Does Not Resolve Yet

- **Session 18 — Agent Transparency / Lower Trace Surface** — the orchestration trace, task progression, and compact-boundary visibility surface. The portfolio view's execution summary strip shows `[last activity]` and status at a summary level; the lower trace surface shows the full V Forge activity trail and LLM orchestration events. These are complementary — the portfolio view is the map, the lower trace is the ledger.
- **Portfolio view filtering by priority signal** — the `[Sort: attention ▾]` filter bar option exists, but filtering by the Session 15 priority signal levels (`urgent`, `high`, `normal`, `low`) across projects is not designed here. That would require the priority signal to be persisted to a backend record rather than being a runtime UI signal. Until priority signals are persisted, sorting by them in a cross-session view is not possible. This is a known limitation, not a design oversight.
- **The `[Portfolio ›]` left nav footer affordance pixel placement** — the left nav footer is referenced across Sessions 15 and 17 but its exact geometry (height, border, other footer items) has not been specified. This is Session 22/23 territory (Component Behavior Patterns and Left Nav Refinements).
- **Post-switch center workspace behavior** — when the operator clicks `[Switch to this project ›]`, the center workspace clears open tabs (except the portfolio tab). The exact animation and UX of this tab clearing is Session 22/23 territory.
- **Multi-project batch operations** — a future capability where the operator could, for example, mark multiple projects as `on hold` simultaneously from the portfolio view. This would require batch write API endpoints and a different action model. Not designed here and not recommended until the single-project action paths are stable.
