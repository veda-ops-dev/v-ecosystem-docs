# Session 4 — Context Strip Design Spec
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Session 1 (Output Card System), Session 2 (Minimal Token Decisions), Session 3 (Topbar)
**Required before:** Session 5 (Right Panel Shell) — the panel shell's layout and sizing depend on understanding what the context strip contains

---

## 1. Files Read

- `session-02-minimal-token-decisions.md` — active token baseline
- `session-03-topbar-spec.md` — what the topbar already exposes (four always-visible elements); context strip must extend, not duplicate
- `v-ecosystem-desktop-ux-work-plan.md` — Session 4 deliverable: nine category rows, content rules per category
- `desktop-surface-architecture.md` — context strip always-visible requirement, right panel content rules, synchronization requirements
- `desktop-state-and-context-model.md` — nine state categories, all required visible content, decision display format, evidence display format, staleness markers, cross-system attribution, continuity non-authority posture, orchestration lifecycle labels
- `desktop-governance-and-gating-model.md` — what stale context blocks per class, conflict detection, incomplete context behavior
- `desktop-invalidation-and-refresh-matrix.md` — CTXSTRIP consequence per all 18 events
- `desktop-implementation-architecture.md` — contextStore, orchestrationStore, continuityStore ownership model; refreshCoordinator responsibility
- `runtime-sidecar-and-nerve-model.md` — sidecar owns canonical backend communication; context strip renders sidecar-loaded state
- `operator-surface-interfaces.md` — cross-system posture for operators
- `workflows/maintenance-and-replanning-workflow.md` — maintenance vs replanning distinction for STAGE category
- `workflows/handoff-workflow.md` — handoff stage semantics (Prepared vs Awaiting Approval)
- `workflows/launch-readiness-workflow.md` — launch readiness cross-system confirmation requirement

---

## 2. Session 4 Scope Confirmation

The work plan defines Session 4 — Context Strip as the second TIER 2 shell session. The context strip lives permanently in the right panel. It is the most doctrine-constrained surface in the application because it must surface all nine state categories that the operator and LLM require to understand current context.

This session produces:
- Nine category rows, each fully specified with label, content, freshness/trust markers, staleness treatment, conflict treatment, ownership labels, and expandable detail affordance
- All nine empty and unavailable states
- Dormancy behavior for conditionally-visible categories (ORCH, CONTINUITY, TOOLSURFACE)
- Invalidation event response for all 18 matrix events that carry a CTXSTRIP consequence
- Token usage from Session 2

This session does not:
- Design the right panel shell (Session 5)
- Design the operator input area (Session 5)
- Design the interaction/output area (Session 5)
- Design the session integrity view or modal (Session 12)
- Design inline banners (Session 12)

---

## 3. Context Strip Purpose

The context strip is the single canonical reference surface for what is loaded and active in the current session. It exists in the right panel, permanently visible, synchronized with the topbar and the center workspace.

Its purpose is precise: the operator and the LLM must never need to guess what state is actually loaded. The context strip makes explicit:
- which decisions govern the current work
- what evidence is loaded and whether it is current
- whether the current stage has any blocking conditions
- whether anything in the current integrity state is unresolved
- whether orchestration is active and what it is doing
- whether continuity artifacts are participating in the session basis
- what tool posture the runtime is currently operating under

The topbar shows four things always. The context strip shows nine things on demand. Together they provide the complete state visibility requirement from doctrine.

**What the context strip is not:**
- It is not an interaction surface — no LLM input
- It is not a navigation surface — clicking a record name does not navigate (navigation belongs to the left nav and center workspace router)
- It is not a governance control — no approval buttons, no gate widgets
- It is not a source of canonical truth — it renders what has been loaded from canonical records

---

## 4. Context Strip Architecture

### Position in the right panel

The context strip sits at the top of the right panel, above the interaction/output area. It is always visible. It cannot be collapsed in the sense of being fully hidden — this is a doctrine requirement. However, individual category rows may be in a compact (one-line) state until expanded.

The minimum height of the context strip in its most compact state is defined by the number of loaded categories and their single-line representations. The maximum height (all categories expanded) is unconstrained but the panel scroll behavior handles overflow.

### Width

The context strip fills the full width of the right panel. It must be readable at the minimum panel width: `--panel-right-min: 280px`. All content must be designed to work at 280px. At `--panel-right-width: 320px` (default) content has slightly more room but must still be legible without horizontal scroll.

### Background and border

The context strip shares the right panel's `--surface-raised` background. A `--border-subtle` bottom border separates it visually from the interaction area below. No top border — the panel chrome handles that transition.

### Z-index

Context strip renders at `--z-base` (1). It has no elevation above the panel background. Cards in the interaction area below it use `--elevation-raised`, which creates the visual hierarchy that the strip is the "ceiling" of the panel.

---

## 5. Nine Category Rows — Full Specification

Each category row follows a consistent structure:

```
[CATEGORY LABEL]                    [status indicator or count]
[primary content line]
[secondary content / expanded detail when open]
```

**Row chrome:**
- Category label: `--type-xs` (11px), `--weight-semibold` (600), `--text-tertiary`, letter-spacing 0.3px — this is the visual language of structural metadata, not content
- Primary content: `--type-sm` (12px), `--weight-normal`, `--text-primary`
- Secondary content: `--type-xs` (11px), `--weight-normal`, `--text-secondary`
- Row left padding: `--space-3` (12px)
- Row right padding: `--space-3` (12px)
- Row vertical padding: `--space-2` (8px) top and bottom in compact state; `--space-3` (12px) when expanded
- Row bottom border: `--border-subtle` 1px — separates rows
- Expand/collapse affordance: chevron `›` / `⌄` at right edge, `--text-tertiary`, `--type-xs`, only present when a row has expandable detail

**Interaction states on rows:**
- Hover: `--state-hover-overlay` (rgba white 6%) — indicates the row is expandable
- No hover on non-expandable rows
- Expand transition: `--transition-accordion` (height 500ms ease) — matches Bricks accordion pattern

---

### Category 1 — SCOPE

**Label:** `SCOPE`

**What it shows:**
The active project name and scope health posture. This row exists because the context strip must be self-contained as a governance reference — even though SCOPE is also visible in the topbar, the context strip must not require the operator to look away from the right panel to confirm scope.

**Normal state (compact):**
```
SCOPE
content-hub  ●
```
Where `●` is 6px, colored by health: `--state-success` / `--state-warning` / `--state-danger`.

**No expandable detail for SCOPE.** It is what it is. If more detail is needed, it lives in the project detail view, not in the context strip.

**Unavailable state:**
```
SCOPE
No project selected
```
Text in `--text-tertiary`. No health dot.

**Relationship to topbar:** This row and the topbar project indicator show the same value and health. They must stay synchronized (EVENT-10 reloads both).

---

### Category 2 — SYSTEM

**Label:** `SYSTEM`

**What it shows:**
Current system and any referenced systems with ownership labels.

**Normal state (compact) — one system active, no referenced systems:**
```
SYSTEM
V: Project V
```
System name in its system color (same as topbar: `--text-primary` for Project V, `--state-info` for VEDA, `--accent-primary` for V Forge).

**Normal state (compact) — referenced systems present:**
```
SYSTEM                           [+2 referenced]
V: Project V
```
`[+2 referenced]` is a `--type-xs`, `--text-tertiary` count badge; click to expand.

**Expanded state — referenced systems:**
```
SYSTEM
V: Project V                         [current]
OBS: VEDA                   [referenced · not owned]
FRG: V Forge                [referenced · not owned]
```

The `[referenced · not owned]` label is `--type-xs`, `--state-info` text, `--ownership-label-border` border, `--ownership-label-bg` fill — using the ownership label tokens from Session 2. This label cannot be collapsed or removed. It is the cross-system reference marker that doctrine requires.

**Expandable:** Yes, when referenced systems are loaded.

**Unavailable state:**
```
SYSTEM
Unavailable — system not loaded
```

---

### Category 3 — STAGE

**Label:** `STAGE`

**What it shows:**
Current workflow stage, next gate, blocking conditions. This is the most variable category in the context strip — its content depends on which workflow phase the project is in.

**Normal state (compact) — no blocking:**
```
STAGE
Planning — Active  ·  Next: readiness evaluation
```
Stage name: `--text-primary`, `--type-sm`, `--weight-medium`. Gate text: `--text-secondary`, `--type-sm`, `--weight-normal`. Separator `·`: `--text-tertiary`.

**Normal state (compact) — with blocking condition:**
```
STAGE                                    ⚠
Handoff — Awaiting Approval  ·  3 open critical gaps
```
`⚠` in `--state-warning`. Gate/blocking text in `--state-warning`.

**Normal state (compact) — hard block:**
```
STAGE                                    ⛔
Handoff — Awaiting Approval  ·  ESCALATION REQUIRED
```
`⛔` in `--state-blocked`. Text in `--state-blocked`.

**Expanded state:**
Expanded STAGE shows the full list of blocking conditions if multiple exist:
```
STAGE
Planning — Active
─────────────────
Next gate:  Readiness evaluation required
Blocking:   3 open critical gaps
            [gap-07] Search intent gap — blocking
            [gap-11] CWV threshold unmet — critical
            [gap-14] Evidence gap — hosting vertical — critical
```
Gap IDs are shown in `--font-mono`, `--type-xs`. Gap severity labels use `--state-danger` for `blocking` and `--state-warning` for `critical`.

**Schema-pending stages:**
Stages with no settled record anchor show the same `*` treatment established in Session 3:
```
STAGE
Execution — Maintenance *  ·  No active return trigger
```
A `*` at `--type-xs`, `--text-tertiary` is appended directly after the stage name. Hovering the `*` shows a tooltip: `Stage derived from workflow posture — no canonical record anchor`. This tooltip uses `--surface-elevated` background, `--elevation-overlay` shadow, `--radius-md`.

**Unavailable state:**
```
STAGE
Unavailable — context not loaded     [Reload Context]
```
`[Reload Context]` is the one action affordance allowed in the context strip for category reload. It is `--type-xs`, `--text-link` color, clickable. It does not appear on every row — only where doctrine specifies a reload path.

**Expandable:** Yes, always — to show gate and blocking detail.

---

### Category 4 — DECISIONS

**Label:** `DECISIONS`

**What it shows:**
Named list of all active governing decisions for the current project scope. Not a count — names. This is a doctrine hard requirement.

**Normal state (compact) — 2 decisions:**
```
DECISIONS (content-hub)              2 active
[dec-03] Prioritize search-first content
[dec-05] Hosting vertical over SaaS tier
```

All decision IDs in `--font-mono`, `--type-xs`, `--text-tertiary`. Decision titles in `--type-sm`, `--text-primary`. Each decision on its own line. In compact view, up to 3 decisions are shown; if more, the remaining count is shown as `[+N more]` which expands to show all.

**Expanded state — full decision set with dates:**
```
DECISIONS (content-hub)
[dec-03]  Prioritize search-first content    [2026-02-14]  [active]
[dec-05]  Hosting vertical over SaaS tier    [2026-03-10]  [active]
[dec-07]  Deprioritize SaaS vertical         [2026-03-28]  [active]
```
Dates in `--type-xs`, `--text-tertiary`. Status badge `[active]` in `--text-secondary`.

**Conflict state:**
When a conflict is detected (EVENT-04), the conflicting pair is highlighted inline:
```
DECISIONS (content-hub)                     ⚠ CONFLICT
[dec-03]  Prioritize search-first content   [active]
[dec-07]  ⚠ CONFLICTS WITH dec-03           [active]  ← target-system priority
```
`⚠ CONFLICTS WITH` text in `--state-warning`. The conflict dimension `← target-system priority` is shown as an annotation in `--type-xs`, `--state-warning`.

**Superseded decision (EVENT-02):**
Immediately after supersession, the row shows the change:
```
[dec-05]  Hosting vertical over SaaS tier   [superseded by dec-07]
```
`[superseded by dec-07]` in `--type-xs`, `--text-tertiary`. The superseded decision remains visible briefly with this treatment, then is removed from the active list on the next full refresh.

**Incomplete state:**
```
DECISIONS
⚠ Decision context incomplete               [Retry Load]
Governing decisions could not be loaded.
```
Full-row warning treatment: `--staleness-bg`, `--staleness-border` border, `--staleness-text` for the warning text.

**Empty state (no decisions):**
```
DECISIONS
No governing decisions loaded
```
`--text-tertiary`. This is not an error — it is a valid state for a new project without decisions yet.

**Expandable:** Yes, to show full decision set with dates and status.

---

### Category 5 — EVIDENCE

**Label:** `EVIDENCE`

**What it shows:**
All evidence records loaded in the current session, with source attribution (always VEDA), capture timestamp, trust posture, and freshness/staleness markers.

**Normal state (compact) — 2 records:**
```
EVIDENCE — SOURCE: VEDA                      2 loaded
[obs-047]  Hosting keyword snapshot   [high]  04-01 14:32
[obs-041]  SERP delta — hosting       [high]  03-28 09:15
```

Format per record (compact): `[id]` in `--font-mono` `--type-xs` `--text-tertiary` → space → title `--type-sm` `--text-primary` → space → trust badge `[high/med/low/uncertain]` → timestamp `--type-xs` `--text-tertiary`.

Trust badge colors:
- `[high]`: `--state-success` text
- `[med]`: `--state-warning` text
- `[low]`: `--state-danger` text
- `[uncertain]`: `--text-tertiary`

**Stale record treatment:**
```
[obs-041]  SERP delta — hosting       [high]  03-28  ⚠ STALE — 6 days old
```
`⚠ STALE` in `--staleness-text` (#ffa100). The stale marker is appended after the timestamp on the same line. In expanded state it unfolds to:
```
[obs-041]  SERP delta — hosting
           Trust: high  ·  Captured: 2026-03-28 09:15  ·  Source: VEDA
           ⚠ STALE — 6 days old · may not reflect current conditions
           [Refresh Evidence]
```
`[Refresh Evidence]` is `--type-xs`, `--text-link`, clickable — the only action affordance on the EVIDENCE row.

**Superseded record treatment (when newer record replaces older):**
```
[obs-041]  SERP delta — hosting       [high]  03-28  [superseded]
```
`[superseded]` in `--type-xs`, `--text-tertiary`. The record remains visible but grayed.

**Cross-system ownership label:**
The `EVIDENCE — SOURCE: VEDA` label in the category header enforces the ownership attribution requirement. It is always present, non-removable, in `--type-xs`, `--state-info` text, formatted as shown. If the current system is Project V or V Forge, it additionally shows:
```
EVIDENCE — SOURCE: VEDA (referenced, not owned by Project V)
```
The `(referenced, not owned by Project V)` part uses `--ownership-label-bg` fill and `--ownership-label-text` color — a small inline chip.

**Unavailable / not loaded:**
```
EVIDENCE
Not loaded                                   [Load Evidence]
```
`--text-tertiary`. `[Load Evidence]` is `--text-link`, clickable.

**Expandable:** Yes — to show full record detail per item including provenance notes.

---

### Category 6 — INTEGRITY

**Label:** `INTEGRITY`

**What it shows:**
All active session integrity items: pending approvals, unreviewed return triggers, stale readiness states, unresolved decision conflicts, session health issues. This is the context strip's window into the same state that the topbar attention badges count.

**Normal state (no items):**
```
INTEGRITY                                    ✓ Clear
```
`✓ Clear` in `--state-success`, `--type-xs`. This positive confirmation is important — it tells the operator there are no unresolved items requiring attention, rather than leaving the row blank.

**Normal state (items present — compact):**
```
INTEGRITY                                    3 items
⚠  Pending approval: hosting-comparison handoff
⚡  Return trigger (arrived): V Forge — intent shift
⚪  Stale readiness: seo-tech-audit (>7 days)
```

Each item line uses:
- Icon prefix: `⚠` `--state-warning`, `⚡` `--state-danger`, `⚪` `--text-tertiary`
- Item text: `--type-sm`, `--text-primary`
- Record reference: truncated with `...` if needed

**Expanded state:**
Each item expands to show:
- What it is
- When it arrived or became an issue
- What resolves it (navigate to center surface; route/dismiss)
- For return triggers: current lifecycle state (`arrived` / `acknowledged` / `routed` / `dismissed`)

**Return trigger lifecycle display:**
```
⚡  Return trigger — V Forge finding: intent shift
    Status: arrived  ·  2026-04-01  ·  [Review]
```
`[Review]` navigates to the return trigger detail in the center workspace. This is a navigation affordance, not a resolution action — it opens the record for the operator to read before routing or dismissing.

**Pending approval display:**
```
⚠  Pending approval — hosting-comparison handoff
    Initiated: 2026-03-28  ·  Class B  ·  [Review Gate]
```
`[Review Gate]` navigates to the relevant center review surface where the approval gate lives. This is navigation — not an approval action in the context strip.

**Stale readiness display:**
```
⚪  Stale readiness — seo-tech-audit
    Last evaluated: 2026-03-25  ·  8 days old  ·  [Review]
```

**Session health issue (when session is degraded but not fully broken):**
```
⛔  Session error — runtime connection lost
    All Class B and C actions blocked  ·  [Re-initialize]
```
`[Re-initialize]` opens the session re-initialization modal. This is the one place in the context strip where an action triggers a significant system event — but it is a recovery action, not a governance action. It does not mutate governed records.

**Expandable:** Yes — to show full item list and individual item detail.

---

### Category 7 — ORCH

**Label:** `ORCH`

**Conditional visibility:** This row is shown only when orchestration is materially participating in the current session. "Materially participating" means at least one delegated subtask is in a non-terminal state (`pending`, `running`, `awaiting_review`) or a task recently reached a terminal state (`completed`, `failed`, `cancelled`) within the current session and has not been dismissed from view.

**Dormant state (no active orchestration):**
```
ORCH
—
```
Single line. `—` in `--text-tertiary`. Row is shown but quiet. This is the resolved answer to the open question from Session 3: ORCH and CONTINUITY rows are always present in the strip structure but show a dormant `—` state when inactive. They are never fully hidden from the strip — hiding them would create a confusing layout shift when they activate. They are simply quiet.

**Normal state (compact) — orchestration active:**
```
ORCH                                         2 tasks active
[task-04]  VEDA keyword analysis   running
[task-07]  Gap severity eval       awaiting_review
```

Task ID in `--font-mono`, `--type-xs`, `--text-tertiary`. Task label in `--type-sm`, `--text-primary`. Status in `--type-xs`, colored by state:
- `running`: `--state-info`
- `pending`: `--text-tertiary`
- `awaiting_review`: `--state-pending` (#ffa100)
- `completed`: `--state-success`
- `failed`: `--state-danger`
- `cancelled`: `--text-tertiary`

**Expanded state:**
Each task expands to show:
- Task type and specialist role (if any)
- What the task is doing (bounded label from task record)
- Lifecycle state with timestamp
- If `awaiting_review`: `[Review Output]` navigation affordance

**Non-authority label in header:**
The ORCH row header includes a subtle inline note when expanded:
```
ORCH — runtime state, not canonical system truth
```
In `--type-xs`, `--text-tertiary`, italic. This enforces the non-canonical posture that doctrine requires for orchestration state.

**Task failed:**
```
ORCH                                         1 failed
[task-07]  Gap severity eval       ✗ failed
           Outputs that depended on this task may be incomplete
```
`✗ failed` in `--state-danger`. Warning note in `--type-xs`, `--state-warning`.

**Expandable:** Yes.

---

### Category 8 — CONTINUITY

**Label:** `CONTINUITY`

**Conditional visibility:** Same rule as ORCH — always structurally present, dormant `—` when no continuity artifacts are active.

**What counts as active:** Working memory entries, session-durable memory, compact-boundary products, transcript-derived continuity references, or delegated worker findings that are currently admitted to the session basis.

**Dormant state:**
```
CONTINUITY
—
```

**Normal state (compact) — active artifacts:**
```
CONTINUITY                                   3 active
[wm]  Planning context summary    fresh    session
[dm]  Decision history distill.   fresh    durable
[cb]  Compaction boundary 03-28   aging    boundary
```

Artifact type codes: `[wm]` working memory, `[dm]` durable memory, `[cb]` compact-boundary, `[tc]` transcript-continuity, `[df]` delegated finding — all in `--font-mono`, `--type-xs`, `--text-tertiary`.

Freshness states:
- `fresh`: `--state-success`, `--type-xs`
- `aging`: `--state-warning`, `--type-xs`
- `stale`: `--state-danger`, `--type-xs`

Scope/type: `session`, `durable`, `boundary`, `transcript`, `delegated` — `--type-xs`, `--text-tertiary`.

**Non-canonical label:**
The CONTINUITY row header when expanded includes:
```
CONTINUITY — NON-CANONICAL · does not substitute for canonical records
```
Using `--continuity-border` and `--continuity-bg` tokens from Session 2. The `NON-CANONICAL` label is the same visual treatment as the `NON-CANONICAL` token established in Session 2's governance tokens section.

**Aged artifact:**
```
[cb]  Compaction boundary 03-28   ⚠ aging   boundary
      Produced before most recent compaction cycle
      May not reflect current session basis
      [Clear]
```
`[Clear]` is a dismissal affordance — `--type-xs`, `--text-tertiary`, allows the operator to remove aging or stale artifacts they no longer want in the active basis. This is the only mutation affordance in the context strip, and it is narrow: clearing a continuity artifact from the session view does not delete a record, it removes it from the active basis display.

**Stale artifact blocking notice:**
```
[tc]  Transcript continuity ref.  ⚠ STALE   transcript
      This artifact was cited in an active Approval Request Package.
      Package must be re-evaluated before gate is presented.
```
`--staleness-bg`, `--staleness-border` treatment.

**Expandable:** Yes.

---

### Category 9 — TOOLSURFACE

**Label:** `TOOLSURFACE`

**Conditional visibility:** Always present, dormant when session tool posture is standard/unremarkable. "Unremarkable" means: full primary system tool surface, no referenced-system read posture, no delegated workers active, no restricted posture, no recent compaction that changed the basis.

**Dormant state:**
```
TOOLSURFACE
Standard posture — Project V primary
```
`--text-tertiary`. No action affordance.

**Active/notable state (compact):**
```
TOOLSURFACE                                  restricted
Project V primary  ·  VEDA ref. read active
```
`restricted` in `--state-warning`, `--type-xs`. Shows that the tool surface is not at full open posture.

**Expanded state:**
```
TOOLSURFACE
Primary system:    Project V
Referenced reads:  VEDA (read-only)
Delegated narrow:  task-04 (VEDA keyword analysis) — narrowed to VEDA tools only
Restricted posture: Yes — decision context stale; Class B/C tools withheld
Last refreshed:    2026-04-03 09:42
```

Labels left-aligned at `--type-xs`, `--text-tertiary`. Values right-aligned or following at `--type-sm`, `--text-primary`.

**Post-compaction state:**
```
TOOLSURFACE                                  refreshed
Basis refreshed after compaction (03-28)
Per-category validation: all categories valid ✓
```
`refreshed` in `--state-success`, `--type-xs`. The per-category validation line is critical — this enforces the per-category-not-boolean requirement from doctrine.

**Expandable:** Yes when posture is non-dormant.

---

## 6. Context Strip Structural Layout

The nine rows stack vertically in this order, always:

```
SCOPE
SYSTEM
STAGE
DECISIONS
EVIDENCE
INTEGRITY
ORCH
CONTINUITY
TOOLSURFACE
```

This order is fixed. It reflects the priority hierarchy from doctrine:
- SCOPE and SYSTEM are the scope anchors — they come first
- STAGE and DECISIONS are the governance anchors — they follow scope
- EVIDENCE is the evidentiary basis — it follows decisions
- INTEGRITY is the health surface — it follows content categories
- ORCH, CONTINUITY, TOOLSURFACE are the runtime state categories — they come last

This order must not be reordered for convenience or design preference. The order itself communicates priority.

---

## 7. Compact vs Expanded Behavior

### Default state

On session load, the context strip renders all nine rows in compact state. Compact state is one to three lines per row: the category label line, the primary content line, and optionally one secondary line.

Rows with content load immediately on session start as context is loaded. Rows whose context has not yet loaded show a loading shimmer — a subtle horizontal pulse using `--state-hover-overlay` on the content area — until content arrives. Shimmer uses `--transition-default` for the pulse cycle.

### Expand/collapse

Individual rows expand and collapse independently via the chevron affordance. Expanding one row does not collapse others. This is deliberate: the operator may need to see DECISIONS and EVIDENCE simultaneously when reviewing an output.

The expand/collapse animation uses `--transition-accordion` (height 500ms ease) — consistent with the Bricks accordion pattern from Session 2.

### Memory within session

The context strip remembers which rows the operator has expanded within the current session. If the operator expands EVIDENCE and DECISIONS to review something, those rows remain expanded until the operator collapses them or until a context refresh event triggers a full re-render. After a re-render (e.g., EVENT-10 full reload), rows return to compact state.

### Scroll behavior

If the full expanded context strip exceeds the visible panel height, the context strip section of the right panel scrolls independently from the interaction/output area below. The panel has two independently scrollable regions: the context strip (top) and the interaction/output area (below). The boundary between them is set by the panel shell (Session 5).

---

## 8. Invalidation Event Response

Every event in the invalidation matrix that carries a CTXSTRIP consequence is handled as follows. This section specifies the context strip's surface behavior — it does not redefine the events themselves.

**EVENT-01 (Decision Created):** DECISIONS row updates immediately to show the new decision. In-row notification: `New decision created` in `--state-info`, `--type-xs`, appears for 3 seconds then fades. Row auto-expands briefly to show the new decision, then returns to prior state.

**EVENT-02 (Decision Superseded):** DECISIONS row shows superseded decision with `[superseded by dec-id-new]` treatment. Prior decisions that cited the superseded decision in the STAGE or INTEGRITY rows receive inline stale markers. Row does not auto-expand.

**EVENT-03 (Decision Invalidated):** Same as EVENT-02 but with `[invalidated]` marker. If any Approval Request Package in the interaction area cited the voided decision, INTEGRITY row activates with a `⚠ Package must be re-evaluated` item.

**EVENT-04 (Decision Conflict Detected):** DECISIONS row shows conflict inline. INTEGRITY row adds conflict item. Neither row auto-expands — the topbar badge alerts the operator; the strip displays the state for when they look.

**EVENT-05 (Approval Written):** STAGE row refreshes — new stage, new next-gate, cleared blocking conditions. INTEGRITY row removes the resolved approval item. Transition uses `--transition-default`.

**EVENT-06 (Prior Approval Invalidated):** STAGE row shows `⚠ PRIOR APPROVAL INVALIDATED — Reload required`. INTEGRITY row adds `⚠ Prior approval for [record] has been invalidated` item. STAGE category label line gains `⚠` indicator.

**EVENT-07 (Evidence Loaded):** EVIDENCE row refreshes to show newly loaded records with freshness/trust posture. Row does not auto-expand.

**EVENT-08 (Evidence Stale):** Affected evidence record gains `⚠ STALE` treatment inline. INTEGRITY row receives `⚠ Evidence [obs-id] is stale` item if the staleness blocks a pending gate.

**EVENT-09 (Evidence Refreshed):** Stale marker removed from refreshed records. Staleness items in INTEGRITY row clear. Refreshed timestamp updates.

**EVENT-10 (Session Token Expiry / Runtime Breakage):** ALL nine rows immediately show session error state. Category labels remain but content lines show `[unavailable — session error]` in `--state-danger`. `[Re-initialize]` affordance appears in INTEGRITY row. This is the one event that affects all rows simultaneously.

**EVENT-11 (Current System Changed):** SYSTEM row updates immediately. STAGE row reloads for new system. DECISIONS row scope may change. TOOLSURFACE row updates. Prior ORCH and CONTINUITY states receive stale markers if the system switch invalidated their basis.

**EVENT-12 (Delegated Task Completed — findings admitted):** ORCH row updates task to `completed`. CONTINUITY row activates or adds new artifact for admitted findings, labeled `[df] delegated finding` with non-canonical treatment.

**EVENT-13 (Delegated Task Failed/Cancelled):** ORCH row updates task to `✗ failed` or `cancelled` treatment. CONTINUITY row does not add artifact (no findings to admit).

**EVENT-14 (Meaningful Compaction):** All rows add compaction boundary marker. TOOLSURFACE row shows post-compaction per-category validation result. CONTINUITY row adds or updates `[cb]` compact-boundary artifact. Context strip shows compaction boundary annotation between new content and pre-compaction content.

**EVENT-15 (Transcript Continuity Change):** CONTINUITY row updates. If an artifact expired, it shows `[expired]` treatment before being removed on next refresh cycle.

**EVENT-16 (Return Trigger Arrives):** INTEGRITY row adds `⚡ Return trigger (arrived)` item immediately. ORCH row unaffected. Stage may show `Return — Pending Review` if derivation is successful.

**EVENT-17 (Workflow Stage Change):** STAGE row reloads. New stage, new next gate, new blocking conditions.

**EVENT-18 (Local State Divergence):** INTEGRITY row adds `⚠ LOCAL STATE DIVERGENCE — [category] may not reflect backend state` items for each affected category. Affected category rows show `⚠ LOCAL DIVERGENCE` annotation in their content.

---

## 9. Empty Strip State

When no project is selected (session not yet scoped):

```
SCOPE           No project selected
SYSTEM          —
STAGE           Unavailable
DECISIONS       No decisions loaded
EVIDENCE        Not loaded
INTEGRITY       —
ORCH            —
CONTINUITY      —
TOOLSURFACE     Standard posture (no session scope)
```

All rows are visible. All content is in `--text-tertiary`. The strip is quiet but structurally present. This makes the right panel usable as a reference surface even before work begins, and prevents jarring layout shifts when a project is selected and all rows populate.

---

## 10. Token Usage from Session 2

All visual decisions in this spec reference Session 2 tokens. No new token values are introduced.

**Key tokens for context strip rows:**

| Use | Token |
|---|---|
| Category label | `--type-xs`, `--weight-semibold`, `--text-tertiary` |
| Primary content | `--type-sm`, `--weight-normal`, `--text-primary` |
| Secondary/metadata | `--type-xs`, `--weight-normal`, `--text-secondary` |
| Record identifiers | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Row background | `--surface-raised` |
| Row divider | `--border-subtle` 1px |
| Row left/right padding | `--space-3` (12px) |
| Row vertical padding compact | `--space-2` (8px) |
| Row vertical padding expanded | `--space-3` (12px) |
| Stale marker background | `--staleness-bg` |
| Stale marker border | `--staleness-border` |
| Stale marker text | `--staleness-text` |
| Staleness icon | `⚠` |
| Ownership label fill | `--ownership-label-bg` |
| Ownership label text | `--ownership-label-text` |
| Ownership label border | `--ownership-label-border` |
| Continuity non-canonical fill | `--continuity-bg` |
| Continuity border | `--continuity-border` |
| Non-canonical label text | `--continuity-label` ("NON-CANONICAL") |
| Schema pending text | `--state-schema-hold` |
| Inert/unavailable text | `--text-tertiary` |
| Action affordances (Reload/Refresh/Load) | `--text-link` (#00b0f4) |
| Expand/collapse chevron | `--text-tertiary`, `--type-xs` |
| Row hover overlay | `--state-hover-overlay` |
| Expand transition | `--transition-accordion` (height 500ms ease) |
| Loading shimmer | `--state-hover-overlay` with `--transition-default` pulse |
| Return trigger icon | `⚡`, `--state-danger` |
| Pending approval icon | `⚠`, `--state-warning` |
| Stale readiness icon | `⚪`, `--text-tertiary` |
| Clear integrity item | `✓ Clear`, `--state-success` |
| Trust high badge | `--state-success` text |
| Trust medium badge | `--state-warning` text |
| Trust low badge | `--state-danger` text |
| Trust uncertain badge | `--text-tertiary` |

---

## 11. What the Context Strip Must Never Contain

- Any LLM input field
- Any approval button or gate widget of any kind
- Any `Approve`, `Authorize`, `Activate`, or `Confirm` control
- Any create/edit/delete affordance for governed records
- Any navigation affordance that routes without the operator's deliberate intent (i.e., no auto-navigation on events)
- Any count that substitutes for named content in DECISIONS or EVIDENCE (count alone is explicitly forbidden by doctrine)
- Any visual treatment that makes continuity artifacts look like canonical state
- Any visual treatment that makes referenced system data look like current-system-owned data
- Any inline mutation of governed state other than the narrow `[Clear]` affordance for continuity artifact removal from the active basis display

**On the `[Reload Context]` and `[Load Evidence]` affordances:**
These are permitted because they are bounded triggers for a read operation — they request a reload of context from canonical records. They do not mutate governed state. They are the exception that the doctrine requires ("accessible without more than one click") rather than a contradiction of the no-mutation rule.

---

## 12. What This Session Resolves

- The context strip's nine-category structure is fully specified: content, states, visual treatment, expand/collapse behavior, empty states, unavailable states, dormancy behavior.
- The open question from Session 3 is resolved: ORCH and CONTINUITY rows are always structurally present, showing dormant `—` state when inactive, never fully hidden.
- All 18 invalidation matrix events have context strip surface responses specified.
- The cross-system ownership label is designed concretely: it cannot be collapsed, it uses the Session 2 ownership tokens, it appears in both SYSTEM and EVIDENCE headers.
- The non-canonical posture for ORCH and CONTINUITY is enforced visually through category-level labels that appear in expanded state.
- The schema-pending `*` treatment from Session 3 is carried through into the STAGE row consistently.
- The EVIDENCE row's `[Refresh Evidence]` affordance is the only place in the context strip where evidence loading is triggered — this is the single entry point for that operation, keeping it discoverable without duplicating it across surfaces.
- Action affordances in the context strip are enumerated and bounded: `[Reload Context]` (STAGE), `[Retry Load]` (DECISIONS), `[Load Evidence]` (EVIDENCE), `[Refresh Evidence]` (EVIDENCE stale item), `[Review]` (INTEGRITY items — navigation only), `[Re-initialize]` (session error), `[Clear]` (CONTINUITY aging artifact). No others.

---

## 13. What This Session Does Not Resolve Yet

- **Right panel shell sizing and panel-level behaviors** — the panel shell wraps the context strip; designed in Session 5. The strip is designed to work at 280px minimum width but the panel chrome, collapse behavior, and resize constraints are Session 5.
- **Operator input field** — Session 5.
- **Interaction/output area** — Session 5.
- **Inline banners** — referenced in EVENT responses (e.g., "inline banner appears in center surface") but the banner component itself is Session 12.
- **Session integrity view** — `[Review]` links in INTEGRITY navigate there; designed in Session 12.
- **Tooltip component behavior** — the schema-pending `*` tooltip and the ownership label tooltip use tooltips; the tooltip interaction pattern (hover delay, focus, dismiss) is Session 23 (Component Behavior Patterns).
- **Loading shimmer animation keyframes** — referenced as a `--state-hover-overlay` pulse; the exact keyframe implementation is Session 23.

---

## 14. Recommended Inputs to Session 5

Session 5 is the Right Panel Shell and Operator Input — the surface that wraps the context strip (just designed) and the output cards (Session 1).

**Session 5 should design:**

1. **Panel overall layout** — context strip (fixed top section) + interaction/output area (scrollable middle) + operator input (fixed bottom). The boundary between the context strip section and the interaction area requires a visual treatment: a slightly elevated separator, `--border-default` 1px with `--elevation-raised` shadow on the interaction area's top edge, to signal that scrolling below the strip is a different content type.

2. **Panel width behavior** — `--panel-right-min: 280px` → `--panel-right-width: 320px` default → `--panel-right-max: 440px`. Resize handle at the left edge of the right panel. Collapse behavior: when collapsed, the panel collapses to a narrow rail showing only topbar-level attention badges, not a full hide.

3. **Panel-level states** — empty/no project, loading, error/session broken. The context strip's empty state is specified in this session; the panel-level framing around it is Session 5's job.

4. **Operator input field** — the input area is not a chat box. It is a framing input for directing work. Session 5 must decide its height, placeholder text, mode selector placement (when/how modes appear — Recommendation mode, Review mode, Approval Request mode), and submit behavior.

5. **Output card list area** — how cards are laid out in the scrollable area between the context strip and the input field. Spacing, card entry animation, scroll anchoring.

**One specific question for Session 5 to resolve:**
When the context strip is fully expanded (all nine rows open), and the panel is at minimum width, the interaction area below becomes very small. Should the panel support a "collapse context strip to minimal view" affordance that temporarily reduces the strip to just its category label lines? Or should the panel simply scroll and let the operator manage? This is a usability question — the doctrine does not prevent a compact-mode for expanded rows, but it must not collapse any row to the point of hiding its state markers.
