# Session 3 — Topbar Design Spec
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Session 1 (Output Card System), Session 2 (Minimal Token Decisions)
**Required before:** Sessions 4–24 (all surfaces reference the topbar as the outer governance frame)

---

## 1. Files Read

- `v-ecosystem-desktop-ux-work-plan.md` — session sequence, Session 3 deliverable requirements, topbar anti-affordance rules
- `session-02-minimal-token-decisions.md` — active token baseline; all token references in this document map to values defined there
- `desktop-surface-architecture.md` — topbar role, required content, allowed functions, anti-affordance rules, surface sync requirements
- `desktop-state-and-context-model.md` — nine state categories, always-visible requirements, session integrity, return trigger lifecycle, workflow stage names, schema-block status per stage
- `desktop-governance-and-gating-model.md` — action classes A–D, gating rules, what must be blocked vs warned
- `desktop-invalidation-and-refresh-matrix.md` — 18 events and topbar-specific surface consequences per event
- `operator-surface-interfaces.md` — operator role per system, cross-system surface posture
- `workflows/handoff-workflow.md` — handoff stage names and posture (prepared vs awaiting approval vs activated)
- `workflows/launch-readiness-workflow.md` — launch readiness stages, blocking conditions, cross-system confirmation requirement
- `v-ecosystem-ux/docs/desktop/sessions/session-02-minimal-token-decisions.md` — UX reference repo mirror of session 2 (confirms token source)
- `v-ecosystem-ux/bricks/` — Bricks theme inspected; visual language and spacing density already extracted in Session 2; no new values added here

**Architecture doc not found:** `v-ecosystem-desktop-ux-architecture.md` — file did not exist at the specified path. Session 3 proceeds from doctrine docs and the work plan directly.

---

## 2. Session 3 Scope Confirmation

The work plan defines Session 3 — Topbar as the first TIER 2 shell session. Its purpose is to design the topbar as the persistent governance baseline for the desktop shell.

This session produces exactly what the work plan requires:

- project scope indicator
- current system indicator
- session health / integrity state indicator
- attention badges for pending approvals, unreviewed return triggers, unresolved conflicts
- empty states
- error states

This session does not:

- design the left nav
- design the context strip
- design the right panel
- design any approval gate surfaces
- invent token values beyond Session 2

The topbar produced here is the outer frame that every subsequent session references. Getting it right means the rest of the shell has a stable anchor.

---

## 3. Topbar Purpose

The topbar is the persistent navigation and state surface for ecosystem-wide context. It tells the operator, at all times and with a single glance:

- which project they are working in
- which system is currently active
- what the current workflow stage is
- whether the session is healthy
- whether anything requires attention right now

It is not an interaction surface. It does not govern. It does not accept LLM input. It does not contain approval controls. It orients and signals. Nothing more.

The topbar is the one surface that must always be honest. If the operator cannot trust the topbar to reflect real state, the governance posture of the entire application degrades — because every other surface is scoped by the context the topbar declares.

The topbar operationalizes the "always visible to the operator" requirement from `desktop-state-and-context-model.md` § Context Visibility Rules:

> Always visible to the operator (topbar/status layer — non-collapsible):
> - active project name
> - current system (Project V / VEDA / V Forge)
> - current workflow stage, or `unavailable` if not loaded
> - session health: active, error, or expired

All four must be visible at all times. Not behind a click. Not collapsed. Always.

---

## 4. Topbar Information Architecture

### Height

`--panel-topbar-height: 48px` (from Session 2 spatial constants)

### Z-index

`--z-topbar: 300` — sits above left nav (`--z-panel: 200`), above workspace content

### Background

`--surface-raised: #263238` — same elevation as the panel layer it visually frames

### Border

`border-bottom: 1px solid var(--border-subtle)` — minimal separation from workspace below; the topbar should feel like the top of the shell, not a floating bar

### Layout model

The topbar is a single horizontal strip, 48px tall, spanning the full application width. It contains three zones: Left, Center, and Right. Elements within each zone are laid out using a flex row with `align-items: center`.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│  LEFT ZONE                 CENTER ZONE               RIGHT ZONE                 │
│  [◈ Project][▾][|][System] [Stage · Gate / Blocking] [⚡][⚠][●][Session]        │
└─────────────────────────────────────────────────────────────────────────────────┘
```

Zone boundaries are not visually separated by dividers — the element groupings and spacing produce the visual structure. A faint vertical separator `|` of color `--border-subtle` is used only between the Project Scope indicator and the System indicator within the left zone.

---

## 5. Left-to-Right Element Specification

The topbar contains exactly eight elements, ordered left to right as follows.

---

### Element 1 — Project Scope Indicator

**Zone:** Left
**Position:** Far left, padding-left `--space-4` (16px)

**What it shows:**
The name of the active project, styled as primary UI text. This is the project scope bound to the current session token.

**Visual treatment:**
- Label: project name at `--type-md` (14px), `--weight-medium` (500), `--text-primary` color
- Prefix icon: `◈` at `--type-sm` (12px), `--text-secondary`, `--space-2` (8px) right margin — this glyph is the scope anchor; it visually marks "you are here in project scope"
- Health dot: a 6px circle appended immediately after the project name, with `--space-2` left margin, colored by project health state (see Element States)
- Dropdown arrow: `▾` at `--type-xs` (11px), `--text-tertiary`, `--space-2` left margin; indicates this element is clickable for project switching

**Normal state:**
```
◈  content-hub  ●  ▾
```
Where `●` is `--state-success` (#11b76b) for a healthy active project.

**Gap between prefix icon and project name:** `--space-2` (8px)

---

### Element 2 — Vertical Separator

**Zone:** Left (between project indicator and system indicator)

A single 1px vertical line, height 20px (centered in the 48px bar), color `--border-subtle`. `--space-3` (12px) margin on each side. Non-interactive.

---

### Element 3 — System Indicator

**Zone:** Left
**Position:** Immediately right of separator

**What it shows:**
The currently active system: Project V, VEDA, or V Forge.

**Visual treatment:**
- System name at `--type-md` (14px), `--weight-medium` (500)
- Color per system (see System Color Assignments below)
- A small system badge/icon prefix at `--type-xs` to visually distinguish systems before reading the label
- Dropdown arrow `▾` at `--type-xs`, `--text-tertiary`, `--space-2` left margin; indicates switchable

**System color assignments:**
These are derived from the Session 2 state/accent token palette, chosen for distinct identity without introducing new token values:

| System | Text color token | Prefix label |
|---|---|---|
| Project V | `--text-primary` | `V:` |
| VEDA | `--state-info` (#00b0f4) | `OBS:` |
| V Forge | `--accent-primary` (#ffd64f) | `FRG:` |

The prefix labels (`V:`, `OBS:`, `FRG:`) are rendered at `--type-xs` (11px), `--weight-bold` (700), with `--space-1` (4px) right margin before the system name. They allow peripheral recognition without reading.

**Normal state (Project V active):**
```
V: Project V  ▾
```

**Normal state (VEDA active):**
```
OBS: VEDA  ▾   (text in --state-info)
```

**Normal state (V Forge active):**
```
FRG: V Forge  ▾   (text in --accent-primary)
```

---

### Element 4 — Stage + Gate Indicator

**Zone:** Center
**Position:** Horizontally centered in the available width between left and right zones

**What it shows:**
The current workflow stage for the active project and system, and the next gate or blocking condition if one exists.

This is the topbar's most contextually variable element. It must be informative but compact. It does not expand into full workflow detail — that belongs in the context strip. It surfaces the single most important workflow-position fact the operator needs to see at a glance.

**Structure:**
Two-part inline label:
```
[Stage name]  ·  [Next gate or blocking condition]
```

The `·` separator is `--text-tertiary`. The stage name is `--text-primary` at `--type-sm` (12px), `--weight-medium`. The gate/condition is `--text-secondary` at `--type-sm`, `--weight-normal`.

If no blocking condition exists, the second half shows the next gate in muted form:
```
Planning — Active  ·  Next: readiness evaluation
```

If a blocking condition exists, it is shown with a warning indicator:
```
Handoff — Awaiting Approval  ·  ⚠ 3 open critical gaps
```

If the stage cannot be loaded (schema-unavailable or runtime failure):
```
Stage: Unavailable  ·  —
```

**Width behavior:**
This element is the only one that truncates. If the available center zone is too narrow, the gate/condition part is truncated with an ellipsis before the stage name is. The stage name is the higher-priority visible datum. Maximum display width: 320px.

**Stage name vocabulary:**
Uses only the recognized stage names from `desktop-state-and-context-model.md` § Recognized Stage Names. No invented shorthand. If a stage name maps to a schema-blocked derivation (intake stages, launch readiness stages, maintenance/replanning stages), it is shown only if derivable; otherwise `Unavailable`.

---

### Element 5 — Attention Badge: Pending Approvals

**Zone:** Right
**Position:** Right zone, leftmost badge, right of center zone

**What it shows:**
Count of pending Class B or C approval requests that have been initiated but not completed.

**Visual treatment:**
- Icon: `⊕` or a simple document-with-checkmark glyph at 16px
- Badge count: integer, at `--type-xs` (11px), `--weight-bold`, on a `--state-pending` (#ffa100) fill, `--radius-pill` border-radius, min-width 18px, height 18px
- If count is 0: badge is hidden entirely (not shown as `0`)
- If count is 1–9: shows exact number
- If count ≥ 10: shows `9+`
- The icon itself is `--text-secondary` when no pending approvals exist; `--state-pending` when count > 0

**Clickable:** Yes — opens session integrity view (see Click / Interaction Rules)

---

### Element 6 — Attention Badge: Return Triggers

**Zone:** Right
**Position:** Right of pending approvals badge

**What it shows:**
Count of unreviewed return triggers (state `arrived` or `acknowledged`, not yet `routed` or `dismissed`).

**Visual treatment:**
- Icon: `⚡` at 14px
- Badge: same pill treatment as Element 5 but using `--state-danger` (#fa4362) fill when > 0 (return triggers carry higher urgency signal than pending approvals in the context of the topbar)
- Hidden when count is 0
- Color when active: icon color `--state-danger`, badge fill `--state-danger-bg` (#2d0d12) with `--state-danger` text

**Rationale for danger vs warning:** A return trigger is a V Forge finding routed to planning — it represents an interruption to execution. This is a stronger urgency signal than an approval that is pending but not blocking anything yet. The visual distinction enforces this.

**Clickable:** Yes — opens session integrity view filtered to return triggers

---

### Element 7 — Attention Badge: Decision Conflicts / Unresolved Integrity

**Zone:** Right
**Position:** Right of return trigger badge

**What it shows:**
A combined badge for any unresolved session integrity item beyond the two specific badges above: unresolved decision conflicts, stale readiness states, compaction-boundary integrity items, or local state divergence warnings.

**Visual treatment:**
- Icon: `⚠` at 14px
- Badge: `--state-warning` (#ffa100) fill when active, hidden when 0
- This badge consolidates lower-urgency integrity items that are real but not as acute as pending approvals or return triggers

**Clickable:** Yes — opens session integrity view

---

### Element 8 — Session Health Indicator

**Zone:** Right
**Position:** Far right, padding-right `--space-4` (16px)

**What it shows:**
Session health state: active, degraded, error, or expired. This is the highest-priority signal on the topbar — if the session is broken, nothing else in the application can be trusted.

**Visual treatment:**
- No icon — this is a text+dot combination, not a badge
- State dot: 8px circle at `--space-2` right margin
- Text label: `--type-sm` (12px), `--weight-normal`
- Color and text per state (see Element States section)

**Normal state:**
```
● Session active
```
Dot: `--state-success`. Text: `--text-secondary`.

**Clickable:** Yes when in warning, error, or expired state — opens session integrity modal / re-initialization flow. Not clickable in normal active state (no action available).

---

## 6. Element States and Behaviors

### Project Scope Indicator (Element 1) — States

| State | Health dot color | Project name color | Notes |
|---|---|---|---|
| Active, healthy | `--state-success` | `--text-primary` | Default |
| Active, warning | `--state-warning` | `--text-primary` | At least one open critical gap or stale readiness state |
| Active, error | `--state-danger` | `--text-primary` | Blocked handoff, unresolved conflict blocking Class C, or session integrity error |
| No project selected | — | `Select project…` in `--text-tertiary` | Empty state; no health dot; dropdown arrow still visible |
| Project unavailable | `--state-danger` dot | `[project name]` in `--text-secondary` | Project load failed; name shown if cached, `Unknown project` if not |

The health dot is not a proxy for session health. It reflects the state of the project scope itself — gaps, readiness, conflict posture — independent of whether the session token is valid.

---

### System Indicator (Element 3) — States

| State | Visual change |
|---|---|
| Normal (any system) | As specified in Element 3 above |
| System unavailable | System name shown in `--text-tertiary`, `(unavailable)` appended, dropdown arrow dimmed |
| System switching in progress | Name shows `Loading…` in `--text-tertiary`; arrow hidden during transition |

---

### Stage + Gate Indicator (Element 4) — States

| State | Display |
|---|---|
| Stage known, no gate pending | `[Stage name]  ·  Next: [next gate]` |
| Stage known, blocking condition | `[Stage name]  ·  ⚠ [blocking condition summary]` — condition text in `--state-warning` |
| Stage known, hard block (Class D) | `[Stage name]  ·  ⛔ ESCALATION REQUIRED` — condition text in `--state-blocked` |
| Stage unavailable (no schema anchor or derivation fail) | `Stage: Unavailable  ·  —` — both parts in `--state-schema-hold` |
| Stage unavailable (runtime/session error) | `Stage: Error  ·  Reload required` — in `--state-danger` |
| Stage is schema-pending but partially derivable | Stage name shown if derivable, with `*` suffix; tooltip-accessible note: "Stage derived from workflow posture — no canonical record anchor" |

The `*` suffix pattern and tooltip note for schema-pending stages is the honest representation that doctrine requires. It does not hide the ambiguity; it names it.

**Schema-pending stages that must use `*`:**
- Any intake stage: `Intake — Framing *`, `Intake — Evaluation *`, `Intake — Outcome Pending *`
- Maintenance/replanning stages: `Execution — Maintenance *`, `Replanning — In Progress *`
- Launch readiness stages: `Launch Readiness — In Progress *`, `Launch Authorization — Pending *`, `Post-Launch — Active *`

**Stages with settled schema anchors (no `*`):**
- `Planning — Active`
- `Handoff — Prepared`
- `Handoff — Awaiting Approval`
- `Handoff — Activated`
- `Execution — Active`
- `Execution — Halted`
- `Return — Pending Review`

---

### Attention Badges (Elements 5, 6, 7) — States

| Badge | Shown when | Hidden when |
|---|---|---|
| Pending Approvals (Element 5) | Count > 0 | Count = 0 |
| Return Triggers (Element 6) | Count > 0 (arrived or acknowledged) | All triggers routed or dismissed |
| Integrity / Conflicts (Element 7) | Any unresolved integrity item beyond the above | All items resolved |

Badge transitions use `--transition-fast` (150ms) for appearance/disappearance. Count changes animate with a brief `--transition-default` (200ms) for the number swap — not a jarring jump.

---

### Session Health Indicator (Element 8) — States

| State | Dot color | Text | Text color | Clickable |
|---|---|---|---|---|
| Active | `--state-success` | `Session active` | `--text-secondary` | No |
| Degraded (partial context unavailable) | `--state-warning` | `Session degraded` | `--state-warning` | Yes |
| Error (runtime lost, token expired) | `--state-danger` | `Session error` | `--state-danger` | Yes |
| Reconnecting | `--state-warning` (pulsing) | `Reconnecting…` | `--state-warning` | No |
| Local state divergence detected | `--state-warning` | `State divergence` | `--state-warning` | Yes |

In `Reconnecting` state, the dot uses a subtle opacity pulse animation (0.4s ease, opacity 1.0 → 0.5 → 1.0 loop) to signal active recovery. No spinner. No loading bar. Just the breathing dot.

When the session returns to `Active` from `Error` after re-initialization, there is a brief (400ms) transition where the dot cross-fades from `--state-danger` to `--state-success` using `--transition-slow`. This confirms recovery visually without an alert.

---

## 7. Click / Interaction Rules

### What is clickable

| Element | Clickable | What it does |
|---|---|---|
| Project Scope Indicator (full element) | Yes | Opens project switcher dropdown |
| Vertical Separator (Element 2) | No | Visual divider only |
| System Indicator | Yes | Opens system switcher popover |
| Stage + Gate Indicator | No | Read-only; this is a display element |
| Pending Approvals Badge | Yes | Opens session integrity view, scrolled to pending approvals section |
| Return Triggers Badge | Yes | Opens session integrity view, scrolled to return triggers section |
| Integrity Badge | Yes | Opens session integrity view, scrolled to unresolved integrity items |
| Session Health Indicator | Yes (when not active) | Opens session integrity view or re-initialization modal |

**The Stage + Gate indicator is not clickable.** It displays context. If the operator wants to act on the stage or the gate, they navigate via the left nav or the right panel. The topbar does not open a workflow detail view directly. This is intentional: the topbar orients. It does not route to workflow actions.

---

### Project Switching

**Trigger:** Operator clicks the Project Scope Indicator.

**Behavior:**
1. A dropdown appears (`--elevation-overlay`, `--radius-lg`, `--z-dropdown`) below the project name element.
2. The dropdown lists available projects with their current health dot.
3. Selecting a project initiates a new session with the selected project as scope.
4. During the session re-initialization: project name shows the new project name immediately, health dot becomes a loading indicator (animated `--state-info` dot pulse), stage shows `Loading…`, all badges are cleared.
5. When the new session loads: all topbar elements update from the new session's state. The `--transition-default` (200ms) is used for the element state transitions.
6. **The project switch is a session boundary.** Prior session context does not carry over. Per doctrine, all nine state categories reload fresh from governed records.

**Empty state in dropdown:** If no other projects are available, the dropdown shows `No other projects` in `--text-tertiary` with a disabled affordance.

**Keyboard:** The dropdown is keyboard-navigable. `Escape` closes without switching.

---

### System Switching

**Trigger:** Operator clicks the System Indicator.

**Behavior:**
1. A small popover appears below the system name (`--elevation-overlay`, `--z-dropdown`) listing the three systems: Project V, VEDA, V Forge. Current system shown with a `✓` mark.
2. Selecting a new system triggers EVENT-11 (Current System Changed) as defined in the invalidation matrix.
3. System indicator immediately shows the new system in its color.
4. Stage indicator reloads for the new system.
5. Left nav content reloads for the new system.
6. Context strip reloads for the new system.
7. Prior output cards in the right panel receive the `⚠ SYSTEM CHANGED` staleness marker.

**The system switch is not a session boundary.** The session token scope (project) does not change. Only the active system designation changes. The topbar reflects this by updating the system indicator and stage, while the project indicator and session health indicator remain unchanged.

**Keyboard:** Same as project switcher — `Escape` closes without switching.

---

### Session Integrity View

**Trigger:** Operator clicks any attention badge (Elements 5, 6, or 7) or the session health indicator when it shows a non-active state.

**What opens:** The session integrity view — a right-side drawer or modal (designed in Session 12) showing the full list of unresolved session integrity items. The topbar click is the entry point; the view is not designed in this session.

**For this session:** the topbar spec establishes that clicking any of these elements opens the session integrity view, and clicking badges opens it pre-scrolled to the relevant section. The exact session integrity view design is deferred to Session 12.

---

## 8. Error / Empty / Unavailable States

### Empty State — No Project Selected

Shown at application launch before the operator has selected a project, or if the current project scope is cleared.

```
◈  Select project…  ▾    |    —    [ — ]    [ Stage: Unavailable  ·  — ]    ● Session active
```

- Project name: `Select project…` in `--text-tertiary`
- No health dot
- System indicator shows `—` (no system context without a project)
- Stage indicator shows `Stage: Unavailable  ·  —`
- All attention badges hidden
- Session health indicator shows `Session active` (the session runtime may be fine; only the scope is unset)

The topbar in the empty state is visually quieter than in an active state. The `--text-tertiary` treatment for the project placeholder communicates that this is the first required operator action.

---

### Error State — Session Token Expired

Triggered by EVENT-10 (Session Token Expiry or Runtime Scope Breakage).

```
◈  [project name]  ⚠  ▾    |    ⚠ V Forge  ▾    [ Stage: Error  ·  Reload required ]    ⚠  ⚠  ⚠    ● Session error
```

- Project health dot becomes `--state-danger`
- System indicator text becomes `--text-tertiary`
- Stage shows `Stage: Error  ·  Reload required` in `--state-danger`
- All three badge positions show a static `⚠` in `--state-danger` (not counts — just presence indicators that something requires attention; exact counts cannot be trusted while session is broken)
- Session health: dot `--state-danger`, text `Session error` in `--state-danger`, clickable to open re-initialization modal
- A non-dismissible inline banner appears immediately below the topbar (not inside it): `⚠ SESSION ERROR — Runtime connection lost. All governance-sensitive actions are blocked. [Re-initialize Session]`

The topbar itself does not contain the re-initialization control. That control lives in the banner below it or in the session integrity modal. The topbar only signals the error state and provides the clickable entry point.

---

### Error State — Runtime Lost (Sidecar/MCP Connection Dropped)

Same visual treatment as Session Token Expired. The differentiation between "token expired" and "runtime lost" is surfaced in the session integrity view, not in the topbar text. Both produce `Session error` in the topbar. This prevents the topbar from becoming a diagnostic readout while still being accurate about what matters: the session cannot be trusted.

---

### Degraded State — Partial Context Unavailable

Shown when the session is technically active (token valid, runtime connected) but one or more context categories failed to load.

- Session health dot: `--state-warning`, text `Session degraded`
- Relevant attention badge (Element 7) activates with count ≥ 1
- Stage indicator may show `Unavailable` for affected categories
- Project health dot may change to `--state-warning` if the degradation affects project-level state

This is a softer state than full error. The operator can continue Class A work. Class B and C gates that depend on the missing categories are blocked until the degradation is resolved.

---

### Unavailable State — Stage Cannot Be Derived

When the current workflow stage cannot be determined because:
- The stage has no settled schema anchor (schema-blocked stage family), AND
- The derivation from workflow posture also fails (insufficient context loaded)

The stage indicator shows:
```
Stage: Unavailable  ·  —
```

Both parts in `--state-schema-hold` (#9e9e9e). This is distinct from the error treatment (`--state-danger`). Unavailability is not an error — it is an honest representation that the current state cannot be derived from available context.

---

## 9. Token Usage from Session 2

All values used in this spec are drawn directly from Session 2. The following is an explicit mapping of Session 2 tokens to topbar usage.

**Spatial constants:**
- `--panel-topbar-height: 48px` — topbar height
- `--space-1: 4px` — icon internal gap (prefix label to system name)
- `--space-2: 8px` — icon-to-label gap, health dot margin, dropdown arrow margin
- `--space-3: 12px` — separator horizontal margin
- `--space-4: 16px` — left and right edge padding

**Color tokens:**
- `--surface-raised: #263238` — topbar background
- `--border-subtle: #2e3a42` — bottom border, vertical separator, separator opacity
- `--text-primary: #eaecef` — project name, system name (Project V), stage name
- `--text-secondary: #9e9e9e` — "Session active" text, gate text, separator between stage and gate
- `--text-tertiary: #616161` — dropdown arrows, placeholder text, loading states
- `--state-success: #11b76b` — healthy session dot, healthy project dot
- `--state-warning: #ffa100` — degraded session dot, project warning dot, blocking condition text, badge fill (approvals)
- `--state-warning-bg: #2d2000` — badge background for pending approvals
- `--state-danger: #fa4362` — error session dot, error project dot, hard block stage text
- `--state-danger-bg: #2d0d12` — return trigger badge background
- `--state-info: #00b0f4` — VEDA system name text, return trigger badge count text
- `--accent-primary: #ffd64f` — V Forge system name text
- `--state-schema-hold: #9e9e9e` — schema-pending and unavailable stage text
- `--state-blocked: #fa4362` — Class D escalation indicator in stage

**Elevation:**
- `--elevation-raised` — topbar shadow (lifted above workspace)
- `--elevation-overlay` — project/system switcher dropdowns

**Border radius:**
- `--radius-pill: 100px` — attention badge chips
- `--radius-lg: 6px` — switcher dropdowns

**Typography:**
- `--type-xs: 11px` — badge counts, prefix labels (V:, OBS:, FRG:), separator
- `--type-sm: 12px` — stage name, gate text, session health text, badge empty-state icon size context
- `--type-md: 14px` — project name, system name
- `--weight-normal: 400` — gate text, session health text
- `--weight-medium: 500` — project name, system name, stage name
- `--weight-bold: 700` — badge counts, prefix labels

**Motion:**
- `--transition-default: all 200ms ease` — dropdown show/hide, system/project switch element transitions
- `--transition-fast: all 150ms ease` — badge appearance/disappearance
- `--transition-slow: transform 400ms cubic-bezier(0.25, 0, 0.25, 1)` — session health state cross-fade on recovery

**Z-index:**
- `--z-topbar: 300` — topbar itself
- `--z-dropdown: 100` — switcher dropdowns (correct — below topbar z, rendered as children)

**No new tokens are introduced in this session.** All visual decisions map to the Session 2 baseline.

---

## 10. What the Topbar Must Never Contain

This list combines the work plan's constraints, the surface architecture's anti-affordance rules, and the governance model's enforcement requirements. These are absolute constraints, not guidelines.

**Governance controls:**
- No approval buttons
- No approval gate widgets (Class B or C)
- No Class D escalation controls
- No `Approve`, `Authorize`, `Confirm`, `Accept`, or `Activate` labels on any element

**Mutation actions:**
- No `Create`, `Edit`, `Delete`, or `Archive` controls
- No planning record creation affordance
- No decision creation affordance
- No scope expansion controls

**LLM interaction:**
- No text input field of any kind
- No prompt submission area
- No mode selector
- No chat bubble or conversation affordance

**Navigation that implies ownership:**
- No `Configure` controls for any system
- No observatory scope controls
- No execution configuration controls
- No "go to approval" navigation that bypasses the governed review-before-gate path

**Ambiguous affordances:**
- No control labeled generically enough that an operator might confuse it with a governance action
- No "Continue" or "Proceed" controls that could be mistaken for approving something
- No progress indicators for work-in-progress that imply the topbar is managing that work

**Visual confusion:**
- No inline banners inside the topbar itself (banners belong below the topbar or in center surfaces)
- No error modals anchored to the topbar (the topbar can trigger them via click; it does not contain them)
- No secondary navigation rows stacked below the topbar (the topbar is a single 48px strip)

**Collapse or hide:**
- The topbar must not be collapsible, hideable, or fullscreen-overrideable in a way that removes the four always-visible elements from the operator's view

---

## 11. What This Session Resolves

- The persistent outer frame of the desktop shell is fully specified.
- The four always-visible state elements (project, system, stage, session health) are defined with their exact content, states, and visual treatment.
- Attention badges for the three main integrity categories are defined with count semantics, color, and trigger behavior.
- Project switching and system switching interactions are fully specified.
- The topbar's role as an orienting surface — not a governing surface — is concretely instantiated rather than just stated as a principle.
- All six empty/error/unavailable states are specified.
- Schema-blocked stages have an honest representation (`*` suffix, `Unavailable` fallback) that does not paper over the ambiguity.
- All topbar behavior references Session 2 tokens exclusively; no new values are introduced.
- The topbar anti-affordance boundaries are explicit and implementation-followable.
- The click behaviors are specified to the level needed for implementation: what clicks do, what opens, what does not open.
- The topbar is the synchronization anchor: when any of the 18 invalidation matrix events fires, the topbar's response is now specified (project dot, system indicator, stage indicator, badge counts, session health dot all update per their event-specific states defined in Section 6).

---

## 12. What This Session Does Not Resolve Yet

- **Session integrity view content and layout** — the topbar opens it; its design is Session 12.
- **Session start integrity check overlay** — referenced in session health click behavior; designed in Session 12.
- **Left nav tree content** — the system indicator click opens a system switcher, not the left nav; left nav design is Sessions 6–8.
- **Context strip content** — the topbar syncs with it but does not design it; Session 4.
- **Right panel layout** — Session 5.
- **In-app notification surface** — referenced in the invalidation matrix as the delivery vehicle for several events; designed in Session 12.
- **Banner below the topbar** — the session error state calls for a non-dismissible banner immediately below the topbar; that banner's full behavior is designed in Session 12.
- **Re-initialization modal** — triggered by clicking session health in error state; designed in Session 12.
- **Topbar responsiveness at narrow window widths** — the Tauri desktop application has a minimum window width. Responsive breakpoint behavior is not required at this stage but should be noted as an implementation consideration.
- **Keyboard shortcut to focus topbar elements** — the command catalog is Session 21; topbar keyboard affordances are resolved then.
- **Exact dropdown component behavior** (focus trap, escape key, outside-click dismiss) — these are Session 23 (Component Behavior Patterns).

---

## 13. Recommended Inputs to Session 4

Session 4 is the Context Strip — the most doctrine-constrained element in the application, living in the right panel. Based on what Session 3 resolves:

**Session 4 should read:**
- This document (Session 3) to understand what the topbar already exposes and does not expose — the context strip should not duplicate what the topbar already shows (project name, system, session health dot) but must extend it with the full nine-category detail the topbar compresses.
- `desktop-state-and-context-model.md` § Core State Categories — all nine categories must be visible in the context strip; Session 3 covers four of them at the "always visible" level; the context strip must cover all nine at the "accessible on demand" level.
- `desktop-invalidation-and-refresh-matrix.md` — every event has a `CTXSTRIP` consequence; Session 4 must design for all 18.
- The Session 2 token file — the context strip will use the same token vocabulary; pay particular attention to `--state-schema-hold`, `--staleness-bg/border/text`, `--ownership-label-*`, and `--continuity-*` tokens which see their first real design use in the context strip.

**Session 4 scope note:**
The context strip is designed before the right panel shell (Session 5) because the panel's sizing and layout depend on understanding what the context strip contains. The context strip is the densest information surface in the application. It is nine categories, each potentially multi-row, with freshness markers, conflict warnings, and expandable detail. Design it as if it must be readable at the right panel's minimum width (`--panel-right-min: 280px`) before designing the panel that contains it.

**One open question to resolve before Session 4:**
The context strip shows `ORCHESTRATION` and `CONTINUITY` categories that are only relevant when those features are active. Should these rows be fully hidden when inactive, or should they show an empty/dormant state? The doctrine is clear that they should be visible "when materially relevant" — but the context strip must have a coherent visual layout at both the minimal (no orch, no continuity) and maximal (all nine categories with content) states. Session 4 should resolve this before designing row-by-row.
