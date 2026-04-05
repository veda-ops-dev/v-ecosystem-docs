# Session 18 — Agent Transparency / Lower Trace Surface
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–17 (full shell backbone, all workflow surfaces, portfolio triage; the lower trace surface is the last power feature surface in TIER 5 before command palette)
**Required before:** Session 21 (Command Palette) — the lower trace surface's content inventory is part of the command set that Session 21 must cover; Session 22 (Visual Language) — the lower trace surface has its own density and visual language requirements that the full Bricks adaptation must account for

---

## 1. Files Read

**Prior sessions:**
- `session-02-minimal-token-decisions.md` — active token baseline
- `session-04-context-strip-spec.md` — ORCH and CONTINUITY rows; `[cb]` compact-boundary artifact notation; compact-boundary markers in the context strip
- `session-05-right-panel-shell-spec.md` — compaction boundary marker in the interaction area; orchestration summary in the right panel; lower surface toggle
- `session-09-center-workspace-foundation-spec.md` — center workspace tab model; workspace router; lower surface is distinct from center workspace
- `session-12-session-integrity-check-and-alert-notification-system-spec.md` — EVENT-12 and EVENT-13 toast notifications; `View trace ›` action links; compaction boundary notice (§6.6)

**Doctrine:**
- `interfaces/desktop-agent-orchestration-model.md` — orchestration is a bounded desktop/runtime capability; orchestrator and specialist roles; task and subtask lifecycle posture (`pending`, `running`, `completed`, `failed`, `cancelled`); visibility and traceability rule; meaningful delegated work must be operator-visible; anti-drift rules (no shadow system, no hidden approval, no authority amplification)
- `interfaces/desktop-memory-and-continuity-model.md` — memory classes (ephemeral, session-durable, cross-session); compact-boundary rule; compaction classes (micro, working-memory extraction, full conversational); transcript artifact posture; non-authority vocabulary rule; operator visibility and control rule
- `interfaces/desktop-surface-architecture.md` — lower trace surface role: optional secondary runtime-visibility surface; allowed content (orchestration task states, delegated-task progression, failure details, transcript/tracing references, compact-boundary notices); lower surface anti-affordance rules (must not become primary review surface, must not substitute for approval gates, must not expose hidden mutation actions)
- `interfaces/desktop-invalidation-and-refresh-matrix.md` — EVENT-12 (delegated task completed — lower surface updates with terminal state), EVENT-13 (delegated task failed or cancelled — lower surface updates with failure/cancellation state and reason), EVENT-14 (compaction event logged in trace surface)
- `interfaces/desktop-state-and-context-model.md` — ORCH and CONTINUITY state categories; orchestration visibility requirements; continuity artifact visibility requirements

---

## 2. Session 18 Scope Confirmation

The work plan defines Session 18 — Agent Transparency / Lower Trace Surface as: orchestration trace, delegated task lifecycle, compact-boundary markers, lower surface content rules.

This session produces:
- **Lower trace surface shell** — the optional secondary runtime-visibility panel: its placement, dimensions, toggle, and relationship to other surfaces
- **Orchestration trace view** — the primary content mode: task and subtask lifecycle display, specialist attribution, task state vocabulary
- **Compact-boundary event view** — how compaction events appear in the trace with per-category validation results
- **Transcript/audit view** — read-only chronological runtime event ledger
- **Lower surface content rules** — what belongs here, what does not, and why
- **Lower surface absent-affordances** — the structural enforcement of what the lower trace cannot do
- **Synchronization with upper surfaces** — how the lower trace updates in response to the events that touch it (EVENTs 12, 13, 14)
- **The non-authority label system** — how the lower trace communicates that its content is runtime visibility, not canonical state

This session does not:
- Design the command palette (Session 21)
- Design the full Bricks visual language (Session 22)
- Define exact backend storage or transcript persistence format (implementation docs)
- Add new action classes or approval paths
- Design the task lifecycle implementation details (a separate companion doc)

---

## 3. The Lower Trace Surface in the Shell

### 3.1 Placement and Dimensions

The lower trace surface is an optional panel that occupies the bottom of the desktop shell, below the center workspace and right panel. It is not visible by default.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  TOPBAR                                                          48px     │
├──────────────┬───────────────────────────────────────┬───────────────────┤
│              │                                       │                   │
│  LEFT NAV    │  CENTER WORKSPACE                     │  RIGHT PANEL      │
│  260px       │  flex                                 │  320px            │
│              │                                       │                   │
│              ├───────────────────────────────────────┤                   │
│              │  LOWER TRACE SURFACE (when open)      │                   │
│              │  flex height: 200–400px, resizable    │                   │
├──────────────┴───────────────────────────────────────┴───────────────────┤
```

**Lower trace surface dimensions:**
- Height: 240px default; resizable by dragging the top border up to 400px max, down to 160px min
- Width: spans from the left nav right edge to the right panel left edge — same width as the center workspace
- Background: `--surface-base` — same as center workspace background, slightly darker than `--surface-raised` panels; the lower trace is "below" the workspace, visually
- Top border: 1px `--border-default` (slightly more prominent than `--border-subtle`); this edge is the drag handle for resizing
- Z-index: standard document flow — it is not an overlay

**The lower trace surface does not overlap the center workspace.** When it is open, the center workspace shrinks to accommodate it. The combined center workspace + lower trace height = total available height minus topbar. The center workspace flex-shrinks when the lower trace opens.

**Minimum viable lower trace height: 160px.** Below this, content becomes illegible. The drag handle resists movement below 160px.

### 3.2 Toggle

The lower trace surface is toggled by a control in the shell chrome — specifically at the bottom edge of the right panel (a small `[◫ Trace]` chip):

```
Right panel bottom edge:
  [◫ Trace]    ← 24px height, `--text-tertiary`, `--type-xs`, `--weight-medium`
                  transitions to `--text-secondary` when lower trace has unreviewed items
```

`◫`: a compact split-panel glyph indicating the lower surface. `--text-tertiary` when trace is closed, `--text-secondary` when open.

Clicking `[◫ Trace]` toggles the lower surface open/closed with `--transition-panel` (300ms ease-out).

**When closed**, the shell shows a subtle 2px indicator strip at the very bottom of the center workspace area in `--border-subtle` color — a visual hint that the lower surface exists but is not currently open. If unreviewed items exist (failed tasks, compaction events), this strip brightens to `--state-warning` at 30% opacity.

**When the lower surface has content requiring attention** (a failed task, an unacknowledged compaction event), the `[◫ Trace]` chip gains an attention dot: an 8px `--state-warning` dot to its right. This is the only attention signal the lower trace surface generates — it does not fire topbar badges, toasts fire independently per Session 12.

### 3.3 Relationship to Other Surfaces

The lower trace is **not** a center workspace tab. It does not open via the workspace router. It is a separate shell region with its own toggle.

The lower trace is **not** the right panel's interaction area. The right panel shows LLM outputs and the context strip. The lower trace shows runtime infrastructure events.

The lower trace is **not** a substitute for the session integrity view. The session integrity view (Session 12) is for governance-relevant items requiring operator action. The lower trace is for runtime visibility — understanding what the system is doing, not acting on it.

These distinctions are spatial and structural: the lower trace lives below the center workspace, has its own toggle, and cannot contain the controls that belong in the other surfaces.

---

## 4. Lower Trace Surface Internal Structure

The lower trace has three views, selectable via a compact tab strip at the top of the panel:

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [Orchestration ●]  [Compaction]  [Transcript]        [× Close]    ↕    │
│  ─────────────────────────────────────────────────────────────────────── │
│                                                                           │
│  [Active view content]                                                   │
│                                                                           │
└──────────────────────────────────────────────────────────────────────────┘
```

**Tab strip** (28px height, `--surface-raised` background, `--border-subtle` bottom border):
- Three tabs: `Orchestration`, `Compaction`, `Transcript`
- Active tab: `--text-primary`, `--weight-medium`; 2px `--border-accent` bottom
- Inactive tab: `--text-tertiary`, `--weight-normal`
- Attention dot `●` on a tab when that view has unreviewed items: 6px `--state-warning` dot inline after the label
- `[× Close]`: right-aligned, `--text-tertiary`, `--type-xs`; closes the lower surface
- `↕` resize handle indicator: right of close button, `--text-tertiary`

**View body**: scrollable within the lower surface height. `--surface-base` background. `--space-4` (16px) horizontal padding. `--space-3` (12px) vertical padding.

---

## 5. Orchestration View

### 5.1 What It Shows

The Orchestration view is the primary view — the one most operators will look at most often. It shows the lifecycle of delegated tasks and specialist agents during the current session.

It answers the operator's question: "What is the system actually doing right now, what did it just do, and is there anything I need to know about it?"

### 5.2 Non-Authority Label

A permanent, non-dismissible header label at the top of the view body:

```
RUNTIME VISIBILITY — NOT CANONICAL STATE
Delegated task activity is shown here for operator review.
Outputs from delegated work are non-canonical until explicitly admitted.
```

- Background: `--surface-raised` (slightly elevated from the view body `--surface-base`)
- Text: `--type-xs`, `--text-tertiary`
- Border-bottom: `--border-subtle` 1px
- Height: 40px
- Non-dismissible: it cannot be collapsed or hidden

This label is the physical implementation of the orchestration model's anti-drift rule: "Worker outputs, orchestration traces, and delegated findings must not be treated as canonical system state just because they are useful." The operator sees this label every time they open the Orchestration view.

### 5.3 Active and Recent Tasks

Tasks are displayed in reverse-chronological order (newest at top). Each task is a row or collapsible block depending on its complexity.

**Simple task row** (single delegated task, no subtasks):

```
[status dot]  [task label]                [specialist role]  [duration]  [›]
              [brief scope description]
```

- Status dot: 8px, colored by lifecycle state (see §5.4)
- Task label: `--type-sm`, `--weight-medium`, `--text-primary`
- Brief scope description: `--type-xs`, `--text-secondary`, one line, truncated at 60 chars
- Specialist role: `--type-xs`, `--text-tertiary` — e.g., `analysis`, `review`, `packaging`, `consistency check`; from the orchestration model's examples of specialist roles
- Duration: `--font-mono`, `--type-xs`, `--text-tertiary` — e.g., `4.2s`, `12s`, `1.3m`; live count while running
- `›`: navigates to the task detail expansion (below); visible on hover
- Row height: 40px minimum; expands with description

**Expandable task block** (orchestrated work with subtasks):

```
▼ [status dot]  [orchestrator task label]          [subtask count]  [duration]
                [brief scope description]
   │
   ├─ [dot] [subtask A — specialist: analysis]      completed  2.1s
   ├─ [dot] [subtask B — specialist: review]        completed  3.7s
   └─ [dot] [subtask C — specialist: packaging]     running    ···
```

- `▼` / `▶` toggle: collapses/expands subtask list; `--text-tertiary`
- Subtask rows: 32px height, indented 16px from parent, `--border-left --border-subtle` connector line
- Subtask status: text badge, same vocabulary as §5.4 but at `--type-xs` scale
- Duration for running tasks: animated `···` pulse in `--text-tertiary`

### 5.4 Task Lifecycle State Vocabulary

From the orchestration model's minimum required states:

| State | Dot color | Text label | Text color |
|---|---|---|---|
| `pending` | `--text-tertiary` hollow `○` | `pending` | `--text-tertiary` |
| `running` | `--state-info` pulsing `●` | `running` | `--state-info` |
| `completed` | `--state-success` `●` | `completed` | `--state-success` |
| `failed` | `--state-danger` `●` | `failed` | `--state-danger` |
| `cancelled` | `--text-tertiary` dim `●` | `cancelled` | `--text-tertiary` |
| `awaiting_review` | `--state-warning` `●` | `awaiting review` | `--state-warning` |

**Pulsing animation for `running`:** The `--state-info` dot pulses with a 2-second ease-in-out opacity cycle (1.0 → 0.4 → 1.0). This is the only animation in the lower trace surface — restrained use of motion to signal "this is live."

### 5.5 Task Detail Expansion

Clicking `›` on a task row or expanding a task block reveals the full task detail inline:

```
▼ [●] Hosting comparison — competitive analysis          completed  4.2s

   Task ID:        task-0042
   Objective:      Analyze competitive positioning for hosting vertical
   Scope:          Bounded to [obs-047], [obs-041], Session 15 evidence
   Output type:    FINDING
   Specialist:     analysis
   Status:         completed  ·  2026-04-03 09:41:22
   Output status:  ADMITTED — non-canonical  ·  view output in panel

   ─────────────────────────────────────────────────────────────────
   NON-CANONICAL FINDING
   Admitted to session basis at 09:41:22.
   This output is not a governing decision, evidence record, or
   canonical Project V state.
   ─────────────────────────────────────────────────────────────────
```

**Field layout:** label/value pair pattern — `--type-xs`, `--weight-semibold`, `--text-tertiary` labels; `--type-sm`, `--text-primary` values. Label minimum width: 100px.

**Task ID:** `--font-mono`, `--type-xs`, `--text-tertiary`

**Output status options:**

| Output status | Treatment |
|---|---|
| `ADMITTED — non-canonical` | `--state-info` text; `view output in panel` link |
| `NOT ADMITTED — task failed` | `--state-danger` text; no link |
| `NOT ADMITTED — cancelled` | `--text-tertiary` text; no link |
| `AWAITING REVIEW` | `--state-warning` text; `[Review ›]` link |
| `PENDING` | `--text-tertiary` text |

**The non-canonical notice block** (when output is admitted):
- Background: `--surface-raised`
- Border-left: 3px `--state-info`
- Text: `--type-xs`, `--text-secondary`
- The "NOT a governing decision" language is the non-authority vocabulary rule in physical form: every admitted finding in the lower trace carries an explicit reminder that it is not canonical state

**Failed task detail** (when state = `failed`):

```
   Status:       failed  ·  2026-04-03 09:41:22
   Failure reason:  Evidence records unavailable — [obs-041] not loaded
   Output status: NOT ADMITTED — task failed

   Affected outputs: [output-card-007] has been marked stale.
   No findings were admitted from this task.
```

The `Failure reason` is surfaced here in full detail — this is the place where failure diagnostics live. It is not visible in the toast (which is brief) and it is not visible in the interaction panel (which shows only the staleness marker). The lower trace is where the operator goes for the full picture.

### 5.6 When No Tasks Exist

```
                ○

   No delegated tasks this session.

   Orchestration activity will appear here
   when the runtime delegates bounded work.
```

`○` in `--text-tertiary`, `--type-lg`. Text in `--text-tertiary`, `--type-sm`. No call to action.

### 5.7 Cancellation Control

When a task is in `running` or `pending` state, a `[Cancel]` control appears in the task detail expansion:

```
   Status:   running  ·  started 09:41:18   [Cancel]
```

`[Cancel]`: `--surface-elevated`, `--border-default`, `--text-secondary`, `--type-xs`, `--radius-md`, 28px height. Hover: `--state-danger` border, `--state-danger` text.

Clicking `[Cancel]` triggers the governed cancellation path. The task transitions to `cancelled` state. EVENT-13 fires. The lower surface updates accordingly.

**The `[Cancel]` control is the only action available in the lower trace.** It is not an approval action. It does not write a governed record. It sends a cancellation signal to the runtime. The cancellation event is logged in the transcript view. This is consistent with the orchestration model's cancellation rule: "The operator must be able to cancel meaningful delegated work."

---

## 6. Compaction View

### 6.1 What It Shows

The Compaction view shows a log of compaction events that have occurred in the current session, including what each compaction preserved, what it dropped, and the per-category validation results that followed.

It answers the question: "What happened to session context, what survived, and should I be concerned about anything?"

### 6.2 Non-Authority Label

Same persistent header as the Orchestration view:

```
RUNTIME VISIBILITY — NOT CANONICAL STATE
Compaction activity is shown here for operator review.
Compaction does not affect governed records or approval state.
```

### 6.3 Compaction Event Entry

Each compaction event appears as a collapsible block:

```
▶ [cb-03]  Full conversational compaction  ·  2026-04-03 09:30:15

  OR expanded:

▼ [cb-03]  Full conversational compaction  ·  2026-04-03 09:30:15

   Compaction class:  full-conversational
   Trigger:           Context window approaching threshold
   Duration:          1.2s

   POST-COMPACTION VALIDATION
   ─────────────────────────────────────────────────────────────────
   SCOPE          ✓ valid
   SYSTEM         ✓ valid
   STAGE          ✓ valid
   DECISIONS      ✓ valid
   EVIDENCE       ⚠ stale-refresh-required  ·  [obs-041] requires refresh
   INTEGRITY      ✓ valid
   ORCH           ✓ valid
   CONTINUITY     ✓ valid — 3 working memory entries preserved
   TOOLSURFACE    ✓ valid
   ─────────────────────────────────────────────────────────────────
   Protected context:  Preserved intact
   Artifacts retained:  3 working memory entries, 1 compact-boundary product
   Narrative history:   Compacted — accessible via Transcript view
```

**Compaction ID:** `[cb-03]` in `--font-mono`, `--type-xs`, `--text-tertiary` — the same compact-boundary notation used in Sessions 4 and 5

**Compaction class label:** `--type-sm`, `--text-primary`; classes: `micro`, `working-memory-extraction`, `full-conversational`

**Post-compaction validation table:**

Each of the nine state categories shows its post-compaction status:

| Status | Icon | Color |
|---|---|---|
| `✓ valid` | `✓` | `--state-success` |
| `⚠ stale-refresh-required` | `⚠` | `--state-warning` |
| `⚠ missing-refresh-required` | `⚠` | `--state-warning` |
| `⛔ invalid-blocking` | `⛔` | `--state-danger` |

- Category labels: `--type-xs`, `--weight-semibold`, `--text-tertiary`, fixed width 120px
- Status: icon + text; colored by status
- Any `invalid-blocking` category shows with a `[Resolve ›]` link in `--text-link` that navigates to the relevant surface for resolution

**"Protected context: Preserved intact"**: `--state-success` `✓`, `--type-xs`, `--text-secondary` — the operator can see that compaction did not silently destroy protected context.

**"Narrative history: Compacted — accessible via Transcript view"**: `--type-xs`, `--text-tertiary`, with a `[View transcript ›]` link. This is the bridge between the Compaction view and the Transcript view — the operator knows the history is preserved, just in the adjacent view.

### 6.4 Micro-Compaction Entries

Micro-compaction events are shown as single-line entries without a validation table (they do not affect protected context):

```
[cb-01]  Micro-compaction — noise removal  ·  09:22:14  ·  18 tokens reclaimed
[cb-02]  Micro-compaction — duplicate output removed  ·  09:28:31  ·  4 tokens reclaimed
```

`--type-xs`, `--text-tertiary`. No expansion needed.

### 6.5 When No Compaction Events Exist

```
                ○

   No compaction events this session.
```

---

## 7. Transcript View

### 7.1 What It Shows

The Transcript view is a chronological ledger of all runtime events in the current session — the complete audit trail. It is the most comprehensive view in the lower trace and also the most rarely needed. Most operators will use it only when debugging an unexpected behavior or reviewing what happened during a specific time window.

### 7.2 Non-Authority Label

```
RUNTIME TRANSCRIPT — NOT CANONICAL STATE
This transcript records session activity for review and debugging.
It does not replace governed records in any system.
Entries here carry no approval authority.
```

### 7.3 Event Entry Format

All events are displayed in chronological order (oldest at top; the view auto-scrolls to bottom when new events arrive). The transcript is **append-only** — no entries are deleted within the session.

Each entry is a single line or short block:

```
09:30:01  [TURN]       Operator input: "Review the hosting handoff scope"
09:30:03  [LLM-OUT]    RECOMMENDATION produced  ·  action class: B
09:30:04  [EVENT-17]   Stage change: Planning — Active → Handoff — Awaiting Approval
09:30:04  [TOPBAR]     Stage indicator updated
09:30:05  [GATE]       Approval gate activated: hdl-07
09:41:18  [TASK-START] task-0042 started  ·  objective: competitive analysis
09:41:22  [TASK-END]   task-0042 completed  ·  output: ADMITTED
09:41:22  [EVENT-12]   Delegated task completed — findings admitted
09:30:15  [CB-03]      Full compaction  ·  post-validation: 8/9 valid, 1 stale
09:30:16  [PANEL]      Compaction boundary marker placed
```

**Entry anatomy:**

```
[timestamp]  [source label]   [description]
```

- Timestamp: `--font-mono`, `--type-xs`, `--text-tertiary`, 8-character width (HH:MM:SS)
- Source label: `--font-mono`, `--type-xs`, `--weight-bold`, fixed width 12 characters, color by source category (see §7.4)
- Description: `--type-xs`, `--text-secondary`

**Source label categories and colors:**

| Label | Meaning | Color |
|---|---|---|
| `[TURN]` | Operator interaction turn | `--text-secondary` |
| `[LLM-OUT]` | LLM output produced | `--text-secondary` |
| `[EVENT-XX]` | Invalidation event from the matrix | `--state-info` |
| `[TASK-START]` | Delegated task initiated | `--state-info` |
| `[TASK-END]` | Delegated task completed/failed/cancelled | `--state-success` (completed), `--state-danger` (failed), `--text-tertiary` (cancelled) |
| `[CB-XX]` | Compaction event | `--state-warning` |
| `[GATE]` | Gate activation, approval write, or authorization | `--accent-primary` |
| `[INTEGRITY]` | Session integrity event | `--state-warning` |
| `[TOPBAR]` | Surface update: topbar | `--text-tertiary` |
| `[LEFTNAV]` | Surface update: left nav | `--text-tertiary` |
| `[PANEL]` | Surface update: right panel | `--text-tertiary` |
| `[CENTER]` | Surface update: center workspace | `--text-tertiary` |
| `[ALERT]` | Alert or notification fired | `--state-warning` |

**Surface update entries** (`[TOPBAR]`, `[LEFTNAV]`, `[PANEL]`, `[CENTER]`) are `--text-tertiary` and lower visual weight than governance events. They are present for completeness but should not draw attention.

### 7.4 Filtering

The transcript can be filtered by source category using a compact filter row below the non-authority label:

```
Show: [All ✓]  [Events]  [Tasks]  [Gate]  [Compaction]  [Surface updates □]
```

- Filter chips: `--type-xs`, `--surface-raised`, `--border-subtle`, `--text-secondary`; active chip: `--border-accent`, `--accent-primary` text
- `[Surface updates □]` is unchecked by default — surface updates (topbar, leftnav, panel, center) are hidden by default because they are lower-value for most diagnostic purposes

### 7.5 Transcript Non-Authority Enforcement

Two structural rules prevent the transcript from being misused as a substitute for canonical state:

**1. No action affordances.** No entry in the transcript view has any action button, approval control, or navigation CTA. Entries are display-only text. Clicking a gate entry does not open the gate. Clicking a task entry does not navigate to the task. The transcript is a read-only ledger.

**Exception for cross-view navigation:** A `[View in Orchestration ›]` or `[View in Compaction ›]` link appears on task and compaction entries. This navigates to the other view tab — it does not open a center workspace view.

**2. Explicit non-authority attribution.** Any entry that represents an LLM output or delegated finding shows: `(non-canonical)` appended in `--text-tertiary`. The operator cannot miss that an LLM output in the transcript is not a governed record.

---

## 8. Lower Surface Absent-Affordances

These are structural constraints — not warnings, not reminders. The lower trace surface must not contain the following.

**No approval controls.** No `[Approve]`, `[Reject]`, `[Authorize]`, or `[Proceed to Approval Gate]` buttons anywhere in the lower trace surface. Not on tasks. Not on compaction events. Not on transcript entries. Approval gates live in the center workspace Actions section. The lower trace is a visibility surface, not a governance surface.

**No canonical record editing.** No input fields for modifying decisions, evidence records, or planning state. The lower trace is read-only except for the task cancellation control (§5.7), which is a runtime signal — not a record mutation.

**No LLM prompt input.** The lower trace does not have an operator input field. Framing new work happens in the right panel's operator input. The lower trace is downstream of LLM interaction, not a site for initiating it.

**No autonomous escalation to primary review surface.** The lower trace does not push its content into the center workspace without operator action. If a task failure warrants investigation, the operator can use the `View trace ›` link from the Session 12 toast. The lower trace does not auto-open a center workspace tab.

**No hidden mutation actions.** No action in the lower trace silently changes canonical state. The only action available is `[Cancel]` on running tasks, which is a runtime signal — and even this is logged explicitly in the Transcript view so it is not hidden.

**No authority claims on outputs.** The lower trace surface must never display a delegated finding in a way that looks like a governing decision, evidence record, or approval event. The non-authority label (§5.2) and the non-canonical notice block (§5.5) are the structural enforcement mechanisms.

---

## 9. The Non-Authority Label System

Every view in the lower trace surface has a persistent, non-dismissible header label that makes the surface's non-canonical nature explicit. These labels are not warnings about misuse — they are architectural identity declarations.

**Orchestration view label:**
```
RUNTIME VISIBILITY — NOT CANONICAL STATE
Delegated task activity is shown here for operator review.
Outputs from delegated work are non-canonical until explicitly admitted.
```

**Compaction view label:**
```
RUNTIME VISIBILITY — NOT CANONICAL STATE
Compaction activity is shown here for operator review.
Compaction does not affect governed records or approval state.
```

**Transcript view label:**
```
RUNTIME TRANSCRIPT — NOT CANONICAL STATE
This transcript records session activity for review and debugging.
It does not replace governed records in any system.
Entries here carry no approval authority.
```

**Visual treatment for all three:**
- Background: `--surface-raised` (slightly elevated from view body)
- Text: `--type-xs`, `--text-tertiary`
- Padding: `--space-3` (12px) horizontal, `--space-2` (8px) vertical
- Border-bottom: `--border-subtle` 1px
- Height: 40px (single line) or 48px (two-line descriptions)
- Non-collapsible, non-dismissible

**Why these labels are permanent and prominent:**

The memory and continuity model states the non-authority vocabulary rule: "Memory and transcript-derived artifacts must not use language that implies governance authority." The orchestration model states: "Worker outputs, orchestration traces, and delegated findings must not be treated as canonical system state."

These are not behavioral aspirations — they are structural requirements. The labels are the physical manifestation of the doctrine that the lower trace surface enforces those requirements through presence, not through absence.

An operator who repeatedly sees these labels develops a trained intuition: "the lower trace is where I understand what the system is doing, not where I govern it." That intuition is exactly the one the ecosystem needs.

---

## 10. Synchronization with Upper Surfaces

The lower trace surface receives events from the invalidation matrix. These events do not require the lower trace to be open — they update the surface state so that when the operator does open it, the content is current.

### EVENT-12 — Delegated Task Completed

**Lower surface update:**
- The task's status dot transitions from `running` (pulsing `--state-info`) to `completed` (`--state-success`)
- Duration counter stops and shows final elapsed time
- Output status shows `ADMITTED — non-canonical` (or appropriate variant)
- The `[Cancel]` control disappears from the task detail
- Transcript view appends: `[TASK-END]  task-XXXX completed  ·  output: ADMITTED`
- The `●` attention dot on the `[Orchestration]` tab appears if the operator has not viewed the completed task

**Upper surface updates that the lower trace reflects but does not drive:**
- Context strip ORCH row update (Session 4)
- Right panel `DELEGATED FINDING ADMITTED` notice (Session 5)
- Toast notification (Session 12)

### EVENT-13 — Delegated Task Failed or Cancelled

**Lower surface update:**
- The task's status dot transitions to `failed` (`--state-danger`) or `cancelled` (`--text-tertiary` dim)
- Failure reason appears in the task detail (the full failure reason that the toast cannot fit)
- Output status shows `NOT ADMITTED — task failed` or `NOT ADMITTED — cancelled`
- Affected output cards are listed by ID with their staleness marker label
- Transcript view appends: `[TASK-END]  task-XXXX failed  ·  reason: [failure reason]`
- The `●` attention dot on the `[Orchestration]` tab appears

**Why the lower trace is the right home for failure reasons:** The toast (Session 12) fires immediately and is brief (one line). The context strip ORCH row shows the state label. The interaction panel cards show staleness markers. But none of these surfaces have the space for the full failure reason. The lower trace is where the operator goes to understand *why* a task failed, not just that it did.

### EVENT-14 — Meaningful Compaction Event

**Lower surface update:**
- New compaction block appears in the Compaction view
- Post-compaction validation results are populated (all nine categories with their post-compaction status)
- Transcript view appends: `[CB-XX]  [compaction class]  ·  post-validation: N/9 valid`
- If any category is `invalid-blocking` or `stale-refresh-required`, the `●` attention dot appears on the `[Compaction]` tab
- The `[◫ Trace]` toggle chip's attention dot updates accordingly

### Lower surface when closed during events

If the lower trace is closed when these events fire, the surface state updates internally but the operator sees only:
- The `[◫ Trace]` chip attention dot (if applicable)
- The 2px bottom strip (brightens to `--state-warning` at 30% opacity if there are unreviewed items)

The lower trace does not force itself open. It signals that it has something worth viewing, and waits for the operator.

---

## 11. Lower Surface and the Operator Workflow

**Most sessions will not require the lower trace.** This is by design and is important to state explicitly.

The lower trace exists for three operator use cases:

**1. Active orchestration monitoring** — when the operator initiates a complex task and wants to see the delegated subtask progression in real time. They open the lower trace, watch the orchestration view, and see tasks complete.

**2. Failure diagnosis** — when a toast fires saying a task failed, and the operator wants to understand why. They open the lower trace → Orchestration tab → find the failed task → read the full failure reason.

**3. Compaction review** — when the operator wants to confirm that a compaction event preserved all required context. They open the lower trace → Compaction tab → review the post-compaction validation table.

**The lower trace is not the operating surface.** An operator spending most of their session in the lower trace is probably looking in the wrong place. The left nav is where project state lives. The center workspace is where review happens. The right panel is where work is framed. The lower trace is where runtime infrastructure becomes legible when needed.

This usage guidance belongs in the spec because it shapes design choices: the lower trace should be informative without being overwhelming, compact without losing detail, present without demanding attention.

---

## 12. Token Usage from Session 2

No new tokens introduced.

| Element | Token(s) |
|---|---|
| Lower surface background | `--surface-base` |
| Lower surface top border | `--border-default` 1px |
| Lower surface tab strip background | `--surface-raised` |
| Lower surface tab strip bottom border | `--border-subtle` 1px |
| Active tab label | `--text-primary`, `--weight-medium` |
| Active tab indicator | 2px `--border-accent` bottom |
| Inactive tab label | `--text-tertiary`, `--weight-normal` |
| Tab attention dot | 6px `--state-warning` |
| `[◫ Trace]` toggle chip | `--text-tertiary` closed, `--text-secondary` open |
| `[◫ Trace]` attention dot | 8px `--state-warning` |
| Bottom strip (closed, idle) | 2px `--border-subtle` |
| Bottom strip (closed, unreviewed items) | 2px `--state-warning` at 30% opacity |
| Non-authority label background | `--surface-raised` |
| Non-authority label text | `--type-xs`, `--text-tertiary` |
| Non-authority label border | `--border-subtle` 1px bottom |
| View body padding | `--space-4` (16px) horizontal, `--space-3` (12px) vertical |
| Task status dot `running` | `--state-info` pulsing |
| Task status dot `completed` | `--state-success` |
| Task status dot `failed` | `--state-danger` |
| Task status dot `cancelled` | `--text-tertiary` dim |
| Task status dot `pending` | `--text-tertiary` hollow |
| Task status dot `awaiting_review` | `--state-warning` |
| Task label | `--type-sm`, `--weight-medium`, `--text-primary` |
| Task scope description | `--type-xs`, `--text-secondary` |
| Task specialist role | `--type-xs`, `--text-tertiary` |
| Task duration (live) | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Subtask connector line | `--border-subtle` left |
| Subtask indent | 16px |
| Task detail field labels | `--type-xs`, `--weight-semibold`, `--text-tertiary`, 100px min-width |
| Task detail field values | `--type-sm`, `--text-primary` |
| Task ID | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Non-canonical notice block bg | `--surface-raised` |
| Non-canonical notice border | 3px `--state-info` left |
| Non-canonical notice text | `--type-xs`, `--text-secondary` |
| `ADMITTED — non-canonical` | `--state-info` text |
| `NOT ADMITTED — task failed` | `--state-danger` text |
| `AWAITING REVIEW` output status | `--state-warning` text |
| `[Cancel]` resting | `--surface-elevated`, `--border-default`, `--text-secondary` |
| `[Cancel]` hover | `--state-danger` border, `--state-danger` text |
| Compaction ID `[cb-XX]` | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Compaction class label | `--type-sm`, `--text-primary` |
| Post-compaction table labels | `--type-xs`, `--weight-semibold`, `--text-tertiary`, 120px width |
| `✓ valid` | `--state-success` |
| `⚠ stale-refresh-required` | `--state-warning` |
| `⛔ invalid-blocking` | `--state-danger` |
| Transcript timestamp | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Transcript source label | `--font-mono`, `--type-xs`, `--weight-bold`, colored by category |
| `[EVENT-XX]` source | `--state-info` |
| `[GATE]` source | `--accent-primary` |
| `[CB-XX]` source | `--state-warning` |
| `[INTEGRITY]` source | `--state-warning` |
| `[TASK-START]` source | `--state-info` |
| `[TASK-END]` success | `--state-success` |
| `[TASK-END]` failed | `--state-danger` |
| `[TASK-END]` cancelled | `--text-tertiary` |
| `[TURN]`, `[LLM-OUT]` source | `--text-secondary` |
| Surface update sources | `--text-tertiary` |
| Transcript description | `--type-xs`, `--text-secondary` |
| `(non-canonical)` annotation | `--text-tertiary`, appended to LLM output entries |
| Filter chip resting | `--surface-raised`, `--border-subtle`, `--text-secondary` |
| Filter chip active | `--border-accent`, `--accent-primary` text |
| Empty state `○` | `--text-tertiary`, `--type-lg` |
| Empty state text | `--text-tertiary`, `--type-sm` |

---

## 13. What Session 18 Resolves

- The lower trace surface is fully specified: shell placement, dimensions, toggle (`[◫ Trace]` chip), relationship to other surfaces, three-view structure (Orchestration / Compaction / Transcript).
- The Orchestration view is fully specified: non-authority label, task and subtask lifecycle display, specialist attribution, task state vocabulary (all five states + `awaiting_review`), task detail expansion, failed task failure-reason display, the `[Cancel]` control as the only action in the surface.
- The Compaction view is fully specified: non-authority label, compaction event entries with post-compaction validation tables for all nine state categories, micro-compaction entries, bridge to Transcript view.
- The Transcript view is fully specified: non-authority label, event entry format with source labels and color vocabulary, filtering, the two structural non-authority enforcement rules (no action affordances except cross-view navigation; explicit non-canonical attribution on LLM output entries).
- The non-authority label system is specified as a permanent architectural identity declaration on every view — not a warning, not a tooltip, a physical surface element that trains operator intuition.
- The absent-affordances are structural: no approval controls, no canonical record editing, no LLM prompt input, no autonomous escalation, no hidden mutations, no authority claims on outputs. The surface cannot do governance because the surfaces that do governance are elsewhere.
- Synchronization with EVENTs 12, 13, and 14 is specified: what changes in the lower trace when tasks complete, fail, or are cancelled, and when compaction occurs. The lower trace does not force itself open — it signals through the toggle chip's attention dot.
- The operator workflow guidance is explicit: most sessions will not require the lower trace; it exists for active orchestration monitoring, failure diagnosis, and compaction review. This shapes every density decision in the surface.
- TIER 5 Power Features (Sessions 17–18) is complete. The application now has all its primary surfaces, all its governance surfaces, and both its power feature surfaces designed.

---

## 14. What Session 18 Does Not Resolve Yet

- **Session 21 — Command Palette** — the lower trace surface's toggle and cross-view navigation links are reference candidates for the command palette. Session 21 must include: "open lower trace", "view orchestration", "view transcript", "view compaction log" as commands. The lower trace's content inventory is now stable enough for Session 21 to reference.
- **Lower trace persistence across sessions** — whether the transcript and compaction logs persist when the operator closes and re-opens the application is an implementation decision about transcript retention policy. This spec defines the surface behavior during a session; the retention policy belongs in `desktop-compaction-implementation-design.md` and the transcript persistence companion doc.
- **Lower trace search/filter for Transcript view** — with long sessions the transcript may grow to hundreds of entries. A search input in the Transcript filter bar would improve usability. Not designed here — this is a Session 22/23 refinement.
- **Lower trace resizing behavior on right panel collapse** — when the right panel collapses to its 40px rail (Session 5), the lower trace's width expands proportionally. The exact animation and constraint behavior is Session 22/23 territory.
- **Task lifecycle implementation details** — the `desktop-task-lifecycle-implementation-design.md` companion doc that the orchestration model references. This defines the mechanical lifecycle tracking, event publication, and refresh triggers that implement the visibility requirements Session 18 designs for. That doc is implementation, not UX — it is outside this spec's scope.

---

## 15. Recommended Inputs to Session 21

Session 21 is the Command Palette / Keyboard-First Workflows — the final TIER 5 session before visual language work.

**What Session 21 inherits from Sessions 17–18:**
- The portfolio view opens via `[Portfolio ›]` in the left nav footer — Session 21 needs a command: `Open portfolio`
- The lower trace toggle is `[◫ Trace]` in the right panel bottom — Session 21 needs commands: `Open trace`, `Open orchestration view`, `Open compaction log`, `Open transcript`
- The Session 15 ranking surface opens via `[Portfolio ranking ›]` — Session 21 needs: `Open portfolio ranking`
- The Session 12 session integrity view opens via topbar badge click — Session 21 needs: `Open session integrity`

**Complete command inventory now available:**

With Sessions 3–18 complete (Session 16 blocked, Session 19–20 held), the full set of surfaces and their entry points is known. Session 21 can now enumerate the complete command set without guessing what surfaces exist. The inventory includes:

- Navigation commands (open record detail, reveal in nav, switch system, switch project)
- Workflow commands (proceed to approval gate, route return trigger, route to replanning, confirm reaffirmation)
- Surface commands (open portfolio, open ranking, open lower trace, open session integrity)
- LLM interaction commands (set mode, request recommendation, request ARP, request review summary)
- Session commands (refresh context, re-initialize session, dismiss all integrity items)
- Gate commands (approve, reject, defer, escalate, confirm authorization)

**The command palette should not contain:**

Any command that would activate a Class B or C gate directly without going through the review-before-gate sequence. The command palette may navigate to a gate surface. It may not be the gate surface.
