# Session 21 — Command Palette / Keyboard-First Workflows
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–18 (all surfaces designed; complete command inventory available)
**Required before:** Session 22 (Full Visual Language Adaptation) — the command palette's visual vocabulary is part of the interaction design language that Session 22 formalizes; Session 24 (MVP Shell and Surface Priority) — the command inventory defines which commands must ship in the MVP vs. later

---

## 1. Files Read

**Prior sessions:**
- `session-02-minimal-token-decisions.md` — active token baseline
- `session-03-topbar-spec.md` — click behaviors; project and system switching; topbar is not a command surface but its switching actions have command counterparts
- `session-05-right-panel-shell-spec.md` — mode selector; operator input; output card response options
- `session-06` through `session-08` — left nav action inventories per system; `[Portfolio ›]` and `[Portfolio ranking ›]` footer affordances
- `session-09-center-workspace-foundation-spec.md` — workspace router; `+ New Tab`; `intent = 'approval_gate'` routing
- `session-10-approval-gate-surfaces-spec.md` — gate commands; `[Proceed to Approval Gate]`; checkpoint model
- `session-12-session-integrity-check-and-alert-notification-system-spec.md` — `[Review Items]`; `[Dismiss All]`; session integrity view trigger paths
- `session-15-maintenance-ranking-ux-spec.md` — `[Portfolio ranking ›]` trigger
- `session-17-portfolio-triage-dashboard-spec.md` — `[Portfolio ›]` trigger; `[Switch to this project ›]`
- `session-18-agent-transparency-lower-trace-surface-spec.md` — `[◫ Trace]` toggle; orchestration/compaction/transcript view navigation

**Doctrine:**
- `interfaces/desktop-implementation-architecture.md` — Required Command Categories: session commands, navigation commands, LLM interaction commands, approval and gate commands, runtime visibility commands; rule that approval/activation commands must only be callable from gate surfaces or explicit routing into gate surfaces
- `interfaces/desktop-surface-architecture.md` — action placement rules; absent-affordance rules; what must never appear where
- `interfaces/desktop-governance-and-gating-model.md` — action classes A–D; the command palette may route toward a gate but is never the gate

---

## 2. Session 21 Scope Confirmation

The work plan defines Session 21 — Command Palette / Keyboard-First Workflows as: last in the plan because the command inventory cannot be finalized until every surface's action set is known.

This session produces:
- **Command palette shell** — the overlay, trigger, search input, and result structure
- **Complete command inventory** — all commands organized by category, with their routing target, action class, and availability conditions
- **Keyboard-first conventions** — global shortcuts for the most important commands; shortcut display in the palette
- **Command availability rules** — when commands are available, unavailable, or blocked
- **Result anatomy** — how individual command results are displayed and acted upon
- **Command palette absent-affordances** — what the palette cannot do

This session does not:
- Design the visual design system (Session 22)
- Design component-level animation (Session 23)
- Redesign any surface (all surfaces are stable; the palette is an entry point to them, not a replacement)
- Add new action classes or approval paths

---

## 3. Command Palette Shell

### 3.1 Trigger

The command palette is opened by:
- Keyboard shortcut: `⌘K` (macOS) / `Ctrl+K` (Windows/Linux)
- Clicking the `+ New Tab` affordance in the center workspace tab bar (Session 9 §5 — deferred to this session)
- Any surface that references "command palette action" in prior session specs

### 3.2 Overlay Structure

The command palette appears as a centered overlay modal — not attached to any panel edge.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [⌘] Search commands, records, or actions…              [Esc to close]  │
│  ─────────────────────────────────────────────────────────────────────── │
│                                                                           │
│  [Result list — scrollable]                                               │
│                                                                           │
│  [Context strip — current scope/system]                                  │
└──────────────────────────────────────────────────────────────────────────┘
```

**Overlay dimensions:**
- Width: 560px
- Max-height: 60vh; result list scrolls if results exceed this
- Background: `--surface-elevated`
- Border: 1px `--border-emphasis`
- Border-radius: `--radius-lg` (6px)
- Box-shadow: `--elevation-modal`
- Z-index: `--z-modal` (500) — above all surfaces except session error critical modal

**Scrim:** Full-screen `--surface-overlay` (#1a1f23 at 60% opacity) behind the palette. Clicking the scrim closes the palette without executing a command.

**Placement:** Vertically centered in the viewport at 35% from top (slightly above center — feels more natural for a launcher). Horizontally centered.

**Entry animation:** Scales from 96% to 100% with `opacity 0 → 1` using `--transition-default` (200ms ease-out). Feels like it "pops" into existence without being jarring.

### 3.3 Search Input

```
[⌘]  Search commands, records, or actions…
```

- `[⌘]` icon: `--font-mono`, `--type-xs`, `--text-tertiary`, `--surface-raised` background, `--border-subtle` border, 20px × 18px, `--radius-sm` — the standard keyboard key indicator glyph
- Input field: full-width, `--type-base` (13px), `--text-primary`, no border (the input is embedded in the palette, not a separate box), `--surface-elevated` background
- Placeholder: `Search commands, records, or actions…` in `--text-tertiary`
- Auto-focused on open: cursor is in the input immediately
- Clears on close: the search state does not persist between opens
- Height: 52px (the input row including padding)
- Bottom border: `--border-subtle` 1px — separates input from results

### 3.4 Result List

Results appear immediately below the search input. With no input, a default set of contextual suggestions is shown (§7). With input, results are filtered.

**Result list container:**
- Min-height: 160px (shows at least ~4 results)
- Max-height: calc(60vh - 52px - 36px) — total palette height minus input minus context strip
- Overflow: `auto` with custom scrollbar (`--scrollbar-width: 4px`, `--scrollbar-color: --border-subtle`)

**Result item anatomy:**

```
[category icon]  [command label]                    [shortcut]  [badge]
                 [brief description]
```

- Category icon: 16px, `--text-tertiary` — a small glyph indicating command category (see §6.2)
- Command label: `--type-sm`, `--weight-medium`, `--text-primary`
- Brief description: `--type-xs`, `--text-secondary`, one line — optional; shown only for commands where context is helpful
- Shortcut: `--font-mono`, `--type-xs`, `--text-tertiary` — keyboard shortcut if assigned (e.g., `⌘K`, `⌘P`)
- Badge: action class badge where relevant — Class B in `--badge-class-b`, Class C in `--badge-class-c`; absent for Class A and navigation commands

**Result item states:**
- Default: background `--surface-elevated`
- Hovered/keyboard-selected: background `--state-hover-overlay`; cursor `pointer`
- Disabled/unavailable: `--state-disabled-opacity` (0.4); cursor `not-allowed`; brief note in `--type-xs`, `--text-tertiary` explaining why (e.g., "requires active project", "gate not available in current stage")
- Separator rows (category headers): `--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase, 0.3px letter-spacing, 28px height, `--border-subtle` bottom border

**Result item height:** 40px (no description) or 56px (with description)

### 3.5 Context Strip

A compact 36px footer showing current scope and system:

```
◈ content-hub   ·   V: Project V   ·   Planning — Active
```

- `--type-xs`, `--text-tertiary`
- Background: `--surface-raised` (slightly elevated from result list)
- Border-top: `--border-subtle` 1px
- Padding: `--space-3` (12px) horizontal

This strip ensures the operator knows which project and system context their commands will execute within. It prevents the disorienting experience of running a command and having it operate on the wrong project.

---

## 4. Keyboard Navigation

**Arrow keys:** `↑` / `↓` move through results. Selection wraps at top/bottom.

**Enter:** Executes the selected command. If the command routes to a surface (navigation commands), the palette closes and the surface opens. If the command opens a gate or requires further input, the palette closes and the appropriate surface activates.

**Escape:** Closes the palette without executing. Returns focus to the previously focused surface.

**Tab:** Moves focus to the next interactive element in the result list (respects keyboard accessibility).

**Typing:** Filters results. The input captures all typed characters immediately. There is no minimum character count for results to appear.

**Backspace when input is empty:** Closes the palette (ergonomic: a second `⌘K` is not required to back out of an empty search).

---

## 5. Command Availability Rules

Commands are available or unavailable based on session state. Unavailable commands are shown in the result list at `--state-disabled-opacity` with a brief explanation — they are never hidden entirely. The operator can see what exists even when it is not executable.

**Availability tiers:**

| Condition | Effect |
|---|---|
| No project selected | Session commands available; all project-scoped commands unavailable with note "Select a project first" |
| Session error (EVENT-10) | Navigation commands available (read-only); all Class B, C, D commands unavailable with note "Session error — re-initialize first" |
| Stage not loaded | Stage-dependent commands unavailable with note "Workflow stage context not loaded" |
| Gate checkpoint not complete | Gate commands unavailable until navigating to the gate surface |
| Command requires current system X | Shows with note "Switch to [system] to use this command" |

**Class B and C commands:** These commands route the operator toward the gate surface — they do not execute the gate action themselves. The command opens the relevant center workspace view with `intent = 'approval_gate'`. The actual approval event requires completing the review-before-gate sequence. This is non-negotiable: the command palette is never the gate.

---

## 6. Complete Command Inventory

Commands are organized into seven categories. Within each category, commands are listed with: label, shortcut (if assigned), action class, routing target, and availability condition.

---

### 6.1 Session Commands

Commands for project scope, session health, and context management.

| Command | Shortcut | Class | Routes to / Does | Availability |
|---|---|---|---|---|
| Select project… | — | A | Project switcher dropdown (topbar Element 1) | Always |
| Switch to [project name] | — | A | Initiates new session for the named project | Always |
| Switch system: Project V | — | A | Sets current system to Project V | Project selected |
| Switch system: VEDA | — | A | Sets current system to VEDA | Project selected |
| Switch system: V Forge | — | A | Sets current system to V Forge | Project selected |
| Open session integrity | ⌘I | A | Opens session integrity view drawer (Session 12) | Project selected |
| Refresh context | ⌘R | A | Triggers full context reload for all nine categories | Project selected |
| Re-initialize session | — | A | Triggers session re-initialization flow | Session error or degraded |
| Dismiss all integrity items | — | B | Opens Dismiss All confirmation in session integrity view | Items exist |
| Copy current context | — | A | Copies project + system + stage to clipboard | Project selected |

**Note on `Switch to [project name]`:** This command is dynamically generated from the project list. If the operator has 4 projects, there are 4 instances of this command — one per project. The palette filters them as the operator types. This is the keyboard path to the same action as clicking the topbar project dropdown.

---

### 6.2 Navigation Commands

Commands for opening records, surfaces, and views.

| Command | Shortcut | Class | Routes to | Availability |
|---|---|---|---|---|
| Open portfolio | ⌘⇧P | A | Portfolio triage view tab (Session 17) | Project selected |
| Open portfolio ranking | — | A | Portfolio ranking surface tab (Session 15) | Project selected |
| Open lower trace | ⌘⇧T | A | Opens lower trace panel, Orchestration tab (Session 18) | Project selected |
| Open orchestration view | — | A | Lower trace panel, Orchestration tab | Lower trace open |
| Open compaction log | — | A | Lower trace panel, Compaction tab | Lower trace open |
| Open transcript | — | A | Lower trace panel, Transcript tab | Lower trace open |
| Open record… | ⌘O | A | Opens search sub-mode for record navigation | Project selected |
| Go to objective… | — | A | Filters to Objective records in open record sub-mode | Project V active |
| Go to initiative… | — | A | Filters to Initiative records | Project V active |
| Go to handoff… | — | A | Filters to Handoff records | Project V active |
| Go to execution entry… | — | A | Filters to Execution Entry records | V Forge active |
| Go to decision… | — | A | Filters to Decision records | Project V active |
| Go to return trigger… | — | A | Filters to Return Trigger records | Any |
| Reveal in nav | — | A | Reveals the currently open center workspace record in the left nav tree | Record open in center |
| Open in new tab | — | A | Opens the currently focused record in a new workspace tab | Record focused |
| Close tab | ⌘W | A | Closes the currently active workspace tab | Tab open |
| Close all tabs | ⌘⇧W | A | Closes all workspace tabs (with confirmation if unsaved state) | Tabs open |
| New tab | ⌘T | A | Opens empty workspace state (`+ New Tab` behavior) | Always |

---

### 6.3 LLM Interaction Commands

Commands for setting mode and requesting typed outputs.

| Command | Shortcut | Class | Does | Availability |
|---|---|---|---|---|
| Set mode: Brainstorm | — | A | Sets right panel interaction mode to Brainstorm | Project selected |
| Set mode: Recommend | — | A | Sets mode to Recommend | Project selected |
| Set mode: Review | — | A | Sets mode to Review | Project selected |
| Set mode: Approval Request | — | A | Sets mode to Approval Request | Project selected |
| Request Recommendation | — | A | Focuses operator input with mode set to Recommend | Project selected |
| Request Review Summary | — | A | Focuses operator input with mode set to Review | Project selected |
| Request Approval Request Package | — | A | Focuses operator input with mode set to Approval Request | Project selected |
| Cancel current task | — | A | Cancels the running delegated task (Session 18 §5.7) | Task running |

---

### 6.4 Workflow Navigation Commands

Commands for navigating to workflow-specific surfaces.

| Command | Shortcut | Class | Routes to | Availability |
|---|---|---|---|---|
| Open handoff review | — | A | Center workspace: handoff detail, Overview section | Handoff exists |
| Open handoff review (approval gate) | — | B | Center workspace: handoff detail, intent = 'approval_gate' | Handoff awaiting approval |
| Open return trigger review | — | A | Center workspace: return trigger detail (Session 13) | Return trigger exists |
| Open replanning surface | — | A | Center workspace: replanning view (Session 15) | Replanning in progress |
| Open launch readiness review | — | A | Center workspace: launch readiness (Session 14) | Launch readiness in progress |
| Open launch readiness (authorization gate) | — | C | Center workspace: launch readiness, intent = 'approval_gate' | Launch authorization pending |
| Open maintenance tracking | — | A | Center workspace: execution entry detail (Session 15) | Execution active |
| Review session integrity items | ⌘I | A | Opens session integrity view (same as session command) | Items exist |
| Acknowledge return trigger | — | A | Transitions return trigger `arrived` → `acknowledged` | Trigger in `arrived` state |
| Route return trigger to replanning | — | B | Opens return trigger detail with `Route to replanning` response pre-selected | Trigger `acknowledged` |

---

### 6.5 Gate Commands

Commands that route toward gate surfaces. None of these commands complete a gate action directly — they are all routing commands that open the appropriate surface with gate context.

| Command | Shortcut | Class | Routes to | Availability |
|---|---|---|---|---|
| Proceed to approval gate | — | B | Center workspace for the pending approval, intent = 'approval_gate' | Pending approval exists |
| Proceed to authorization gate | — | C | Center workspace for the pending launch authorization | Launch authorization pending |
| Escalate current condition | — | D | Surfaces Class D escalation path for the current blocking condition | Class D condition active |
| View pending approvals | — | A | Session integrity view, scrolled to pending approvals | Project selected |

**Critical constraint:** The gate commands above navigate to the gate surface. They do not approve, authorize, or reject anything. An operator typing `Proceed to approval gate` in the command palette will land in the center workspace Actions section with the gate widget visible but inactive (checkpoints still to complete). This is structurally enforced — the `workspaceRouter` with `intent = 'approval_gate'` is the only path these commands use, and the gate widget's checkpoint system controls what happens next.

---

### 6.6 Runtime Visibility Commands

Commands for the lower trace surface and session runtime.

| Command | Shortcut | Class | Does / Routes to | Availability |
|---|---|---|---|---|
| Open lower trace | ⌘⇧T | A | Opens lower trace panel (same as navigation command) | Project selected |
| Close lower trace | — | A | Closes lower trace panel | Lower trace open |
| View orchestration | — | A | Lower trace, Orchestration tab | Project selected |
| View compaction log | — | A | Lower trace, Compaction tab | Project selected |
| View transcript | — | A | Lower trace, Transcript tab | Project selected |
| Filter transcript: events | — | A | Lower trace Transcript tab with Events filter active | Lower trace open |
| Filter transcript: tasks | — | A | Lower trace Transcript tab with Tasks filter active | Lower trace open |
| Filter transcript: gates | — | A | Lower trace Transcript tab with Gate filter active | Lower trace open |
| Cancel running task | — | A | Sends cancellation signal to current running delegated task | Task running |

---

### 6.7 Record Management Commands

Commands for creating and managing records through the governed command path.

| Command | Shortcut | Class | Routes to | Availability |
|---|---|---|---|---|
| Create objective | — | B | Governed command path for creating an Objective record | Project V active |
| Create initiative | — | B | Governed command path for creating an Initiative record | Project V active |
| Create work item | — | B | Governed command path | Project V active |
| Create decision record | — | B | Governed command path for creating a Decision Record | Project V active |
| Copy record ID | — | A | Copies the currently open record's ID to clipboard | Record open |
| Reload record | — | A | Reloads the currently open center workspace record from backend | Record open |

**On "governed command path":** These Class B commands open the relevant record creation flow — which may be a right-panel framing mode, a center workspace form surface, or both. They do not directly write a record; they initiate the governed creation path which requires the operator to complete the required fields and go through any applicable review step.

---

## 7. Default (No-Input) State

When the palette opens with no input typed, it shows contextual suggestions rather than an empty result list. This makes the palette immediately useful without requiring the operator to know what to type.

### Default suggestion structure

```
RECENT
  [Records recently opened in center workspace — up to 3]

ATTENTION REQUIRED
  [Unresolved return triggers, pending approvals — if any]

SUGGESTED FOR THIS STAGE
  [Stage-relevant commands — e.g., "Open handoff review" when stage is Handoff — Awaiting Approval]

QUICK ACTIONS
  Open portfolio       ⌘⇧P
  Open session integrity  ⌘I
  Refresh context      ⌘R
  Open lower trace     ⌘⇧T
```

**RECENT** shows the last 3 records the operator opened in the center workspace, each with its record type badge and title. Clicking a recent record navigates to it directly. These are not stored across sessions — they are the current session's workspace history.

**ATTENTION REQUIRED** shows the same items the topbar attention badges represent, but as clickable command rows. If there are no attention items, this section is absent.

**SUGGESTED FOR THIS STAGE** is the most valuable section for keyboard-driven operators. It surfaces the 2–3 most relevant actions given the current workflow stage. Examples:

| Stage | Suggested commands |
|---|---|
| `Handoff — Awaiting Approval` | "Open handoff review (approval gate)", "View pending approvals" |
| `Replanning — In Progress *` | "Open replanning surface", "Route return trigger to replanning" |
| `Launch Authorization — Pending *` | "Open launch readiness (authorization gate)" |
| `Execution — Active` | "Open maintenance tracking", "Open lower trace" |
| `Return — Pending Review` | "Open return trigger review", "Acknowledge return trigger" |

**QUICK ACTIONS** are always present — the four most broadly useful commands regardless of stage.

---

## 8. Search and Filtering

### 8.1 Search behavior

The palette uses fuzzy matching on:
- Command label
- Command description
- Record titles (when the operator types a record-like query)

Results are ranked by: exact match first, then prefix match, then fuzzy match. Within each rank tier, governance-relevant commands (those with action class badges) are deprioritized slightly relative to navigation commands — preventing the palette from defaulting to showing gate commands before navigation commands.

### 8.2 Record search sub-mode

When the operator types `>` as the first character, the palette enters record search mode. The input placeholder changes to `Search records…` and results show only records from the current project rather than commands.

Alternatively, the `Open record… (⌘O)` command activates this mode.

In record search mode:
- Results show record title, record type badge, record ID
- Pressing Enter navigates to the record in a center workspace tab
- Pressing `Escape` returns to command mode (the `>` prefix is cleared)

### 8.3 Scope indicator during search

While typing, the context strip at the bottom of the palette remains visible. This ensures the operator knows they are searching within the current project scope, not across all projects.

---

## 9. Command Palette Absent-Affordances

The command palette cannot do the following. These are structural constraints, not guidelines.

**Cannot approve, authorize, reject, or defer.** No command in the palette directly writes an approval record. All gate-related commands navigate to a gate surface. The command palette is never the gate.

**Cannot change the active project without a session boundary.** `Switch to [project name]` initiates a proper session switch — new session token, full context reload. There is no command that silently changes project scope within the current session.

**Cannot execute Class C actions.** Class C commands in the palette (like `Open launch readiness (authorization gate)`) navigate to the Class C gate surface. The typed confirmation, the `[Confirm Authorization]` button, and the authorization record write all happen in the center workspace after the operator arrives there.

**Cannot surface actions that belong only to specific surfaces.** The command palette does not expose approval gate controls, gate widget controls, lower trace editing, or any action that doctrine places exclusively in a specific surface. The palette routes to surfaces; it does not replicate them.

**Cannot reveal information outside the current session scope.** Record search results are limited to the current project. No command shows records from other projects.

---

## 10. Shortcut Reference Summary

The complete shortcut set assigned in this session:

| Shortcut | Command |
|---|---|
| `⌘K` / `Ctrl+K` | Open command palette |
| `⌘I` / `Ctrl+I` | Open session integrity view |
| `⌘R` / `Ctrl+R` | Refresh context |
| `⌘O` / `Ctrl+O` | Open record search sub-mode |
| `⌘T` / `Ctrl+T` | New workspace tab |
| `⌘W` / `Ctrl+W` | Close current workspace tab |
| `⌘⇧W` / `Ctrl+Shift+W` | Close all workspace tabs |
| `⌘⇧P` / `Ctrl+Shift+P` | Open portfolio triage view |
| `⌘⇧T` / `Ctrl+Shift+T` | Open lower trace surface |
| `Esc` | Close command palette (or close modal/drawer in focus) |

**Shortcut design principles:**

- `⌘K` is the universal command palette shortcut across most developer tools. This is the one shortcut every operator will know from other contexts.
- `⌘I` for session integrity is memorable: **I**ntegrity.
- `⌘R` for refresh is the universal reload shortcut repurposed for context reload (not page reload — the Tauri application intercepts this).
- `⌘⇧P` for portfolio echoes VS Code's `⌘⇧P` for command palette, which creates a useful muscle-memory link even though `⌘K` is the actual palette trigger here.
- `⌘⇧T` for trace echoes "terminal" muscle memory in many tools.
- Shift-modified shortcuts are used for panel-opening commands (portfolio, trace) to keep them distinct from single-surface navigation commands.

**Not assigned shortcuts:**
Gate commands intentionally have no keyboard shortcuts. An operator cannot accidentally land at a gate via keyboard shortcut. Reaching a gate requires deliberate navigation through the command palette, nav tree, or output card CTA — never a single key press.

---

## 11. Token Usage from Session 2

No new tokens introduced.

| Element | Token(s) |
|---|---|
| Palette background | `--surface-elevated` |
| Palette border | 1px `--border-emphasis` |
| Palette border-radius | `--radius-lg` (6px) |
| Palette shadow | `--elevation-modal` |
| Palette z-index | `--z-modal` (500) |
| Scrim | `--surface-overlay` at 60% opacity |
| Search input text | `--type-base` (13px), `--text-primary` |
| Search input placeholder | `--text-tertiary` |
| Search input height | 52px |
| Search input bottom border | `--border-subtle` 1px |
| `⌘` key indicator bg | `--surface-raised` |
| `⌘` key indicator border | `--border-subtle` |
| `⌘` key indicator text | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Category header | `--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase |
| Category header height | 28px |
| Category header border | `--border-subtle` 1px bottom |
| Command label | `--type-sm`, `--weight-medium`, `--text-primary` |
| Command description | `--type-xs`, `--text-secondary` |
| Command shortcut | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Command icon | 16px, `--text-tertiary` |
| Result item height (no description) | 40px |
| Result item height (with description) | 56px |
| Result item default bg | `--surface-elevated` |
| Result item hover/selected bg | `--state-hover-overlay` |
| Result item disabled | `--state-disabled-opacity` (0.4) |
| Context strip height | 36px |
| Context strip bg | `--surface-raised` |
| Context strip border | `--border-subtle` 1px top |
| Context strip text | `--type-xs`, `--text-tertiary` |
| Entry animation | scale 96%→100%, opacity 0→1, `--transition-default` (200ms ease-out) |
| Class B badge | `--badge-class-b-bg`, `--badge-class-b-text` |
| Class C badge | `--badge-class-c-bg`, `--badge-class-c-text` |
| Record type badge in results | per Session 9 record type identifier table |

---

## 12. What Session 21 Resolves

- The command palette shell is fully specified: overlay, dimensions, trigger (`⌘K`), search input, result list, context strip footer, entry animation.
- The complete command inventory is enumerated across seven categories: 57 commands total, each with label, shortcut, action class, routing target, and availability condition.
- The default (no-input) state is designed as contextual suggestions rather than an empty list: Recent, Attention Required, Suggested for This Stage, Quick Actions.
- Keyboard navigation is fully specified: arrow keys, Enter, Escape, Backspace-when-empty, Tab for accessibility.
- Command availability rules are concrete: what conditions make commands unavailable, and why unavailable commands are shown rather than hidden.
- The record search sub-mode (`>` prefix or `⌘O`) is specified as a distinct mode within the palette.
- All gate-related commands are routing commands, never gate commands: the palette routes to gate surfaces; it never executes a gate action. This is structurally enforced by all gate commands using `workspaceRouter` with `intent = 'approval_gate'`.
- Gate commands intentionally have no keyboard shortcuts: reaching a gate requires deliberate navigation, never a single key press.
- The 10-shortcut reference is complete and annotated with the mnemonic rationale for each assignment.
- The palette's absent-affordances are explicit: no direct approval/authorization writes, no session scope changes without session boundary, no Class C direct execution, no actions that belong exclusively to other surfaces.
- TIER 5 Power Features is complete. Sessions 17, 18, and 21 are all done.

---

## 13. What Session 21 Does Not Resolve Yet

- **Exact fuzzy-matching algorithm** — the "fuzzy match" ranking described in §8.1 is a behavioral specification; the exact matching algorithm (trigram, Levenshtein, etc.) is an implementation decision for the engineer building the command service.
- **Command palette keyboard shortcut conflicts with OS** — some shortcuts (`⌘R`, `⌘T`, `⌘W`) overlap with browser/OS defaults. In the Tauri context these must be explicitly intercepted. Exactly how Tauri intercepts vs. defers OS-level shortcuts is an implementation concern, not a UX design concern.
- **Shortcuts for left nav `[Portfolio ›]` and `[Portfolio ranking ›]` footer geometry** — the exact pixel placement of the left nav footer affordances that these commands share is Session 22/23 territory.
- **Command palette in the MVP vs. later** — Session 24 will determine which commands ship in the MVP shell. The full inventory here is the complete target; not all 57 commands need to ship in Phase 1.
- **Cross-session recent records** — §7 specifies Recent records as session-scoped. A future enhancement could persist recents across sessions using the local SQLite support layer. Not designed here.

---

## 14. Recommended Inputs to Session 22

Session 22 is the Full Bricks-Inspired Visual Language Adaptation — formalizing the minimal token decisions from Session 2 into a complete visual system.

**What Session 22 inherits from Session 21:**
- The command palette introduces the application's most "app-like" UI pattern — overlay, search input, result list, keyboard shortcuts. Its visual treatment will test the visual language at a different density than the approval gates or the lower trace surface.
- The `⌘` key indicator chip (keyboard shortcut display) is a new UI component introduced here. Session 22 should formalize this as a reusable component in the visual language.
- The command palette's entry animation (scale + fade) is the application's most visible motion pattern. Session 22 / Session 23 should use this as the baseline for the application's modal/overlay animation vocabulary.
- The contextual suggestion categories (Recent, Attention Required, Suggested, Quick Actions) are the palette's information architecture. Session 22 should ensure the visual weight hierarchy between category headers and result items is clear in the full Bricks adaptation.

**Key visual decisions for Session 22 to resolve:**
1. The `⌘` key indicator chip — exact dimensions, border-radius, font treatment as a reusable component
2. Command palette result item padding at the Bricks density standard
3. Hover/selected state for result items — ensuring `--state-hover-overlay` reads clearly against `--surface-elevated` in the full Bricks dark theme
4. Shortcut badge placement — right-aligned vs. inline with the command label, at the exact spacing the Bricks grid prefers
