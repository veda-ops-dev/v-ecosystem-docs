# Session 5 — Right Panel Shell and Operator Input
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Session 1 (Output Card System), Session 2 (Minimal Token Decisions), Session 3 (Topbar), Session 4 (Context Strip)
**Required before:** Session 6 (Left Nav Shell) — the panel sizing and collapse behavior establish the right-side spatial constraint that defines available workspace width for left nav proportioning

---

## 1. Files Read

- `session-02-minimal-token-decisions.md` — active token baseline
- `session-03-topbar-spec.md` — topbar height (48px), z-index (300), session error posture
- `session-04-context-strip-spec.md` — context strip structure, minimum width requirement (280px), two-scroll-region question posed for this session to resolve
- `desktop-surface-architecture.md` — right panel role, required content, limits, LLM surface limits, absent-affordance rules, the "secondary by design" principle
- `desktop-state-and-context-model.md` — "visible on demand but explicitly accessible" rule (must be reachable within one click), interaction mode framing
- `desktop-governance-and-gating-model.md` — Class B/C controls must not appear in the right panel; operator input is not governed approval; approval request packages route to center workspace
- `desktop-implementation-architecture.md` — right interaction panel responsibilities; interaction/output area card rendering; operator input controller; right panel must not own final approval persistence

---

## 2. Session 5 Scope Confirmation

The work plan defines Session 5 as: the right panel as a complete surface — context strip + interaction area + operator input + panel-level behaviors.

This session produces:
- Panel overall layout: three-region model (context strip, interaction/output area, operator input)
- The separator treatment between context strip and interaction area
- The interaction/output area: card list behavior, scroll, spacing, empty state
- The operator input field: framing input, not a chat box — placeholder, mode selector, submit
- Panel width behavior: default, min, max, resize handle, collapse
- Panel-level states: empty/no project, loading, error/session broken
- Resolution of the Session 4 open question on context strip scroll vs. compact-mode affordance

This session does not:
- Design individual output card types (Session 1)
- Design the context strip row content (Session 4)
- Design the session integrity view (Session 12)
- Design the notification/banner system (Session 12)
- Design the left nav (Sessions 6–8)
- Design the center workspace (Session 9)

---

## 3. Panel Purpose

The right panel is the interaction surface. This is where the operator frames work, the LLM produces typed bounded outputs, and the operator reviews those outputs and decides what to do with them.

It is a support surface. It supports the work that lives in the left nav and center workspace. It must not become the primary operating surface.

Three things follow from this that must be built into the shell:

First, the panel is fixed width by default. It does not expand to fill the workspace. It has a defined default, a minimum, and a maximum. The center workspace always gets the remaining space.

Second, the context strip is the top of the panel. It is the reference surface. The interaction area below it is where the LLM's outputs live. The operator input is at the bottom. This top-down ordering reflects the priority hierarchy: know your state first, then interact.

Third, nothing in this panel finalizes governed actions. Output cards may route the operator toward approval, but the approval itself happens in the center workspace. The input field frames work. It does not substitute for a gate.

---

## 4. Panel Spatial Constants (from Session 2)

```
--panel-right-width:   320px   (default)
--panel-right-min:     280px   (minimum, enforced)
--panel-right-max:     440px   (maximum, enforced)
--panel-topbar-height: 48px    (topbar above the panel)
--panel-border-width:  1px
```

Panel height: full viewport height minus topbar height (`calc(100vh - 48px)`). The panel fills the full remaining vertical space.

---

## 5. Three-Region Layout

The right panel is divided into three vertically stacked regions:

```
┌────────────────────────────────────┐  ← top of panel, below topbar
│  CONTEXT STRIP                     │  fixed height: determined by content
│  (nine category rows, expandable)  │  scrolls independently if expanded
├────────────────────────────────────┤  ← separator (see §6)
│                                    │
│  INTERACTION / OUTPUT AREA         │  flex: 1 — takes all remaining space
│  (output cards, chronological)     │  scrollable independently
│                                    │
├────────────────────────────────────┤  ← input separator
│  OPERATOR INPUT                    │  fixed height: 56px collapsed,
│  (framing input + mode + submit)   │  up to 120px expanded
└────────────────────────────────────┘  ← bottom of panel
```

### Region sizing rules

**Context strip region:** Not fixed-height in the sense of a pixel constant — it grows as rows expand. However it has a maximum natural height of approximately 40% of the panel height before it begins to compress the interaction area uncomfortably. This is not a hard clip but a design constraint: if all nine rows are fully expanded simultaneously, the interaction area must still show at least two output cards without scrolling. This constraint is satisfied by the answer to the Session 4 open question (see §6).

**Interaction/output area:** Gets all remaining vertical space between the context strip separator and the input separator. Uses `flex: 1` in the panel's column layout. Always scrollable.

**Operator input region:** Fixed-height range: 56px when the input field contains a single line (default), grows up to 120px for multi-line input. Does not grow beyond 120px — at that point the input field scrolls internally. The input region is always at the bottom of the panel, stuck to the panel's bottom edge.

---

## 6. Context Strip / Interaction Area Separator and Scroll Resolution

This resolves the open question from Session 4: *When all nine rows are expanded, should the panel support a "collapse context strip to minimal view" affordance, or should the panel simply scroll?*

**Resolution: Independent scroll regions, plus a compact-mode toggle.**

The panel uses two independently scrollable regions. The context strip has its own scroll container, separate from the interaction area scroll. This means:

- The operator can scroll the context strip to see ORCH/CONTINUITY/TOOLSURFACE rows without moving the output card list
- The operator can scroll the output card list without disturbing the context strip's expanded state
- Neither region hijacks the other

The separator between them is a fixed visual divider that does not move regardless of scroll position in either region.

**Compact-mode toggle:** A small affordance at the right edge of the separator line allows the operator to collapse the context strip to its "all compact" state — every row returns to its single-line compact view simultaneously. This is not a full hide; it is a reset-to-compact. The button is:

- Icon: `⌃` (collapse all) / `⌄` (restore to prior expanded state)
- Size: 16×16px touch target, 10px actual icon
- Color: `--text-tertiary`, transitions to `--text-secondary` on hover
- Position: flush right of the separator line, `--space-2` (8px) from the right edge

This satisfies both the doctrine requirement (context strip never hidden, always structurally present) and the usability need (operator can reclaim vertical space for the interaction area without losing context strip access).

### Separator visual treatment

The separator between the context strip and the interaction area is:

```
border-top: 1px solid var(--border-default)
background: var(--surface-base)
height: 24px
display: flex; align-items: center; justify-content: flex-end;
padding-right: var(--space-2)
```

The separator is 24px tall — enough to be a clear visual break without wasting space. The compact-mode toggle sits in its right edge. No text label, no section heading. The separator is spatial punctuation, not navigation.

The interaction area below the separator uses `--elevation-raised` as a box-shadow on its top edge only (`box-shadow: 0 -1px 3px rgba(0,0,0,0.4)`), creating a subtle sense that the output cards live in a slightly elevated surface relative to the context strip. This visually enforces that the context strip is the "ceiling" and the interaction area is the primary working space.

---

## 7. Interaction / Output Area

### Purpose and character

This is where output cards appear. The operator sees the history of the session's typed outputs here — findings, recommendations, review summaries, approval request packages, execution reports, uncertainty notices, continuity reminders. Each is a distinct card.

This area is not a chat transcript. It is not a conversation log. It is a structured list of typed bounded outputs. The visual vocabulary for individual card types is established in Session 1; this session specifies how they are arranged, how they enter, how they scroll, and what the area looks like when empty or loading.

### Card list layout

Cards are arranged in chronological order, newest at the bottom. The list is append-only within a session — cards are not reordered. The operator reads top-to-bottom, with the most recent work at the bottom of the scroll area.

**Card spacing:** `--space-4` (16px) vertical gap between cards. This is enough to visually separate distinct typed outputs without creating excessive whitespace.

**Card left/right margin within the area:** `--space-3` (12px) on each side. Cards do not span the full panel width — they have a small inset margin that distinguishes the card list from the panel chrome.

**No dividers between cards.** The spacing and card elevation (`--elevation-raised` per the Session 1 output card spec) provides sufficient separation. Adding horizontal rules between cards would create visual noise without adding information.

### Scroll behavior

The interaction area scrolls independently. By default it is scrolled to the bottom (newest card visible). When a new card is appended, the area automatically scrolls to bring it into view — unless the operator has manually scrolled up to review a prior card, in which case auto-scroll is suppressed until the operator returns to the bottom. A `↓ New output` chip appears at the bottom of the area when auto-scroll is suppressed and a new card arrives:

- Chip: `↓ New output` at `--type-xs`, `--text-secondary`, on `--surface-elevated` background, `--radius-pill`, `--elevation-overlay` shadow
- Position: centered horizontally, 8px above the input separator
- Click: scrolls to bottom and re-enables auto-scroll
- Disappears on reaching the bottom

### Staleness markers on output cards

When any of the 18 invalidation events fires and affects cards in the interaction area, the relevant cards receive staleness markers as defined in the invalidation matrix. The markers are rendered as an inline banner attached to the top of the affected card — not as a modification of the card's body content. The card body remains unchanged; the staleness banner precedes it.

Staleness banner anatomy (rendered above the card it applies to, within the card's boundary):
```
⚠ DECISION SUPERSEDED — [dec-05] replaced by [dec-07]. Re-evaluate this output.
```
Background: `--staleness-bg`. Border-left: 3px `--staleness-border`. Text: `--type-xs`, `--staleness-text`. Padding: `--space-2` vertical, `--space-3` horizontal.

### Empty state

When no outputs have been produced in the current session:

```
                    ·  ·  ·

         Start by framing work in the
         input below.

         The LLM will produce typed outputs
         here as the session progresses.

```

Centered vertically in the available area. Text in `--text-tertiary`, `--type-sm`. The three dots `· · ·` use `--text-tertiary` at `--type-lg` with generous spacing — a minimal ambient indicator that this space is ready, not broken.

**No suggested prompts.** No "try asking about X" shortcuts. The empty state is neutral. The operator knows why they're here.

### Loading state

When outputs are being generated (LLM is producing a response), a generation indicator appears as the last item in the card list:

```
[  ···  ]
```

A card-shaped placeholder at normal card width, containing three animated dots in `--text-tertiary`. The dots use a simple sequential opacity animation (`--duration-fast` 150ms per dot, staggered). The placeholder has the same margin and elevation as a real card so there is no layout shift when the real card arrives.

When the real card arrives, the placeholder is replaced with the typed output card using `--transition-fade` (300ms ease opacity transition). No slide-in, no bounce — just a clean fade-in.

### Session error state (within interaction area)

When the session enters error state (EVENT-10), the interaction area receives a non-scrolling overlay:

```
┌─────────────────────────────────────────────────┐
│                                                  │
│   ⚠  Session interrupted                        │
│   Runtime connection lost.                       │
│   Prior outputs preserved above.                 │
│   Re-initialize to continue.                     │
│                                                  │
└─────────────────────────────────────────────────┘
```

Background: `--surface-overlay` (base color at 80% opacity) — a scrim that covers prior cards without erasing them. Prior cards are preserved and visible through the scrim, confirming to the operator that the session history is not lost. The overlay text is `--text-primary` on the scrim. The input field is also disabled in this state (see §9).

---

## 8. Output Card Response Options

Output cards contain response options (defined in Session 1 per card type). This section specifies how those response options are rendered within the panel's interaction area.

Response options appear at the bottom of each relevant card. They are rendered as small labeled buttons:

- Height: 28px
- Padding: `--space-2` (8px) horizontal, 0 vertical
- Border: 1px `--border-default`
- Background: `--surface-elevated`
- Text: `--type-xs`, `--weight-medium`, `--text-primary`
- Border-radius: `--radius-md` (4px)
- Hover: `--state-hover-overlay`
- Active: `--state-active-overlay`

For Approval Request Package cards specifically, the `[Proceed to Approval Gate]` response option is the primary action. It is visually distinguished from other response options:

- Border: 1px `--border-accent` (`--accent-primary`)
- Text: `--accent-primary`
- On hover: `--state-selected-bg` (amber at 12%)

This treatment signals that this action is the governed path forward — not a dismissal, not a flag, but the transition into the center workspace review-before-gate sequence. It does not look like an approval button. It looks like a navigation action, because that is what it is.

**The `[Proceed to Approval Gate]` button must never be labeled `Approve`.** The label must always make clear it is routing the operator to a review surface, not completing an approval event. This is an absent-affordance rule implemented in the label text, not just the routing behavior.

---

## 9. Operator Input Field

### Purpose

The input field is for framing and directing work. It is not a chat box. The distinction matters for what it looks like and how it behaves:

- A chat box implies conversation: casual, open-ended, turn-by-turn
- A framing input implies work direction: purposeful, bounded, producing typed outputs

This surfaces in design choices: the placeholder text, the mode selector, the submit button label.

### Layout

```
┌────────────────────────────────────────────────────┐
│  [Mode ▾]  Frame the work...              [Submit] │
└────────────────────────────────────────────────────┘
```

Total input region height: 56px (single-line). The input field occupies the horizontal space between the mode selector (left) and the submit button (right).

**Background:** `--surface-elevated` — slightly elevated above the panel background to make it feel like a ready input, not a depressed trough.

**Top border of input region:** `border-top: 1px solid var(--border-default)` — consistent with the separator treatment above it.

**Overall input region padding:** `--space-2` (8px) vertical, `--space-3` (12px) horizontal.

### Input field

- Background: `--surface-raised` (same as panel background — the field is inset, not floating)
- Border: 1px `--border-default`; on focus: `--border-accent` (`--accent-primary`), focus ring `--state-focus-ring`
- Border-radius: `--radius-md` (4px)
- Text: `--type-base` (13px), `--text-primary`
- Placeholder text: `Frame the work…` in `--text-tertiary`
- Padding: `--space-2` (8px) vertical, `--space-3` (12px) horizontal
- Min-height: 36px (single line); max-height: 100px (multi-line, scrolls internally beyond that)
- Grows vertically as operator types multi-line input; the whole input region grows with it up to 120px total, then the field scrolls

**The placeholder text is not suggestive.** It says `Frame the work…` — not `Ask me anything`, not `What would you like to do?`. The framing is intentional. The operator is directing a system, not chatting with an assistant.

### Mode selector

The mode selector controls what type of output the LLM will produce. It appears as a small labeled dropdown at the left of the input row.

**Appearance:**
- Label: current mode name at `--type-xs`, `--weight-medium`, `--text-secondary`
- Dropdown arrow: `▾` at `--type-xs`, `--text-tertiary`
- Background: transparent (no fill in resting state)
- Border: none in resting state; 1px `--border-default` on hover
- Border-radius: `--radius-md`
- Padding: `--space-2` (8px) horizontal, `--space-1` (4px) vertical
- Min-width: 80px

**When mode selector is required vs optional:**

Mode selection is required when the operator needs the LLM to produce a governance-relevant typed output. It is optional (defaults to a lightweight analytical mode) for Class A work.

| Mode | Required | When shown |
|---|---|---|
| `Recommend` | Yes — produces Recommendation output | Always available |
| `Review` | Yes — produces Review Summary output | Always available |
| `Approval Req.` | Yes — produces Approval Request Package | Available when a Recommendation has been accepted |
| `Brainstorm` | No — produces informal analytical output | Always available |

The default mode when no selection has been made is `Brainstorm` — the lightest-weight Class A mode. This means the operator can use the panel for analysis without first selecting a mode. If they want governed typed outputs, they select the appropriate mode.

**Mode dropdown options:**
Displayed in the dropdown using `--elevation-overlay`, `--radius-md`, `--z-dropdown`. Each option is one line: mode name at `--type-sm`, `--text-primary` with a brief descriptor at `--type-xs`, `--text-secondary` on the same line or below.

```
Brainstorm      Analytical exploration, no gate
Recommend       Produce a Recommendation
Review          Produce a Review Summary
Approval Req.   Package for operator approval
```

Active mode is shown with `--state-selected-bg` highlight.

**Mode availability gating:** `Approval Req.` mode is only available when the context supports it — specifically, when a Recommendation output exists in the current session that has been accepted by the operator. If that precondition is not met, the option is shown at `--state-disabled-opacity` (0.4) with a tooltip: `Available after a Recommendation is accepted`.

### Submit button

- Label: `Submit` — not `Send`, not `Ask`, not `Go`
- Width: 60px
- Height: 36px (matches input field height)
- Background: `--surface-elevated`
- Border: 1px `--border-default`
- Border-radius: `--radius-md`
- Text: `--type-sm`, `--weight-medium`, `--text-primary`
- Hover: `--state-hover-overlay`
- Active: `--state-active-overlay`
- Disabled state (when input is empty or session is in error): `--state-disabled-opacity`

The submit button is deliberately understated. It is the same visual weight as the mode selector. Nothing about it suggests urgency or importance. The operator is directing the LLM; this is a normal part of the work, not a highlighted call to action.

**Keyboard submit:** `Enter` submits when the input field is focused and the input is not empty. `Shift+Enter` adds a newline without submitting. This is standard behavior for framing inputs in professional tools.

### Input disabled state

When the session is in error state (EVENT-10), both the input field and the submit button are disabled:
- Input: `--state-disabled-opacity`, `cursor: not-allowed`
- Submit: `--state-disabled-opacity`, `cursor: not-allowed`
- Placeholder text changes to: `Session unavailable — re-initialize to continue`
- Mode selector: disabled, same opacity treatment

When context is loading at session start, the input field is also disabled with placeholder: `Loading context…`. It becomes active once the context strip has loaded its minimum required categories (SCOPE, SYSTEM, STAGE, DECISIONS).

---

## 10. Panel Width Behavior

### Default and resize

The panel opens at `--panel-right-width: 320px`. The operator can resize it by dragging a handle at the left edge of the panel.

**Resize handle:**
- Width: 4px
- Background: transparent in resting state; `--border-emphasis` (#546e7a) on hover; `--accent-primary` when actively dragging
- Cursor: `col-resize`
- Transition: `--transition-instant` (100ms) for color change

The handle extends the full panel height minus the topbar. It is always present — not hidden behind a hover of the panel itself.

**Constraints:**
- Minimum: `--panel-right-min: 280px` — enforced hard. Below this the context strip becomes unusable.
- Maximum: `--panel-right-max: 440px` — enforced hard. Above this the panel starts eating center workspace space to the point of crowding review surfaces.

When the user drags past a constraint, the panel stops at the constraint. No bounce, no rubber-banding. Hard stop.

### Collapsed state

The panel supports a collapsed state — a narrow rail rather than a full hide. This preserves the topbar's attention badges and allows the operator to restore the panel easily.

**Collapsed width:** 40px — wide enough for a column of attention indicators, narrow enough to give maximum space to the center workspace.

**What is visible in collapsed state:**
```
│⚠│
│⚡│
│⊕│
│ │
│ │
│>│  ← expand handle
```

The three attention badge icons (pending approvals, return triggers, integrity items) shown as small icon indicators stacked vertically, using their respective urgency colors from the topbar spec. No count numbers in collapsed state — just presence indicators. A `>` expand handle at the bottom of the collapsed rail, in `--text-tertiary`.

**What is not visible in collapsed state:** The context strip, interaction area, and input field are fully hidden. The panel is not the primary governance surface, so this is acceptable — the topbar still shows all four always-visible state elements.

**Collapse/expand trigger:**
- A `‹` (collapse) icon at the top right of the full panel, `--text-tertiary`, `--type-sm`
- Clicking `‹` collapses to rail
- Clicking `>` in the rail expands back to prior width
- Transition: `--transition-panel` (transform 400ms `cubic-bezier(0.25,0,0.25,1)`) — the Bricks offcanvas panel easing from Session 2

**The panel does not collapse automatically.** Only operator-initiated collapse. No auto-collapse on narrow window widths (that's a Session 23 consideration for breakpoint behavior).

---

## 11. Panel-Level States

### Normal state (project loaded, session healthy)

The full three-region layout as described. Context strip loaded, interaction area showing prior outputs or empty state, input field active.

### Empty state (no project selected)

Context strip shows its empty state (all nine rows in dormant/unavailable treatment, as specified in Session 4). Interaction area shows a modified empty state:

```
                    ·  ·  ·

         Select a project to begin.

```

Input field is disabled: placeholder `Select a project to start a session…`, `--state-disabled-opacity`.

### Loading state (project selected, context loading)

Context strip shows loading shimmers on each row (as specified in Session 4 — `--state-hover-overlay` pulse on content areas). Interaction area shows the empty state (no outputs yet). Input field shows `Loading context…` placeholder and is disabled until minimum context categories load.

The loading state is transient — it exists only during the window between project selection and the first successful context load. It should not persist. If context loading takes more than ~3 seconds, a subtle inline text appears at the bottom of the context strip: `Still loading context…` in `--text-tertiary`, `--type-xs`.

### Session error state (runtime lost, token expired)

Context strip: all rows show `[unavailable — session error]` treatment (Session 4, EVENT-10).
Interaction area: the scrim overlay as specified in §7.
Input field: disabled with `Session unavailable — re-initialize to continue` placeholder.
Collapse button: still accessible (operator can collapse to rail and re-initialize from the topbar).

---

## 12. Panel Interaction Rules

### What is interactive in the panel

| Element | Interactive | Action |
|---|---|---|
| Context strip rows (expandable) | Yes | Expand/collapse row detail |
| Context strip action affordances (`[Reload]`, `[Refresh]`, etc.) | Yes | Trigger reload/refresh operations |
| Context strip `[Review]` links (INTEGRITY items) | Yes | Navigate to center workspace (navigation, not approval) |
| Compact-mode toggle (separator) | Yes | Collapse all context strip rows to compact |
| Output card body | Read-only | No interaction on body content |
| Output card response options | Yes | Execute the stated response (navigate, flag, proceed) |
| `[Proceed to Approval Gate]` on ARP cards | Yes | Navigate to center workspace review surface |
| Staleness banner on output cards | Read-only | No interaction |
| `↓ New output` chip | Yes | Scroll to bottom, re-enable auto-scroll |
| Mode selector | Yes | Open mode dropdown |
| Input field | Yes | Type framing input |
| Submit button | Yes (when enabled) | Submit input to LLM |
| `‹` collapse button | Yes | Collapse panel to rail |
| `>` expand handle (in rail) | Yes | Expand panel to prior width |
| Resize handle | Yes | Drag to resize panel width |

### What is never interactive in the panel

- Output card body text (no inline editing, no selection-triggered actions)
- Output type labels (read-only metadata)
- Staleness marker banners on cards (informational only)
- Context strip category labels (labels, not buttons)
- The context strip itself (it renders state; it does not accept input beyond the expand/collapse and action affordances already specified)

### Interaction panel absent-affordance enforcement

The following controls must never appear in this panel under any circumstances, regardless of what output type or workflow state is active:

- `Approve` button
- `Authorize` button
- `Activate` button
- Any Class B or C gate widget
- Any typed confirmation input
- Any control that creates or mutates a governed record without routing through the center workspace and governed path
- Any navigation tree elements
- Any record browser or record list that substitutes for center workspace content

---

## 13. Token Usage from Session 2

All values reference Session 2 tokens. No new values introduced.

| Element | Token(s) |
|---|---|
| Panel background | `--surface-raised` |
| Context strip background | `--surface-raised` |
| Separator (context strip / interaction area) | `border: 1px --border-default`, height 24px, `--surface-base` background |
| Interaction area elevation marker | `box-shadow: 0 -1px 3px rgba(0,0,0,0.4)` on top edge |
| Card list spacing | `--space-4` (16px) gap |
| Card list margin | `--space-3` (12px) sides |
| Staleness banner | `--staleness-bg`, `--staleness-border`, `--staleness-text` |
| Empty state text | `--text-tertiary`, `--type-sm` |
| Generation indicator dots | `--text-tertiary`, `--duration-fast` animation |
| Card fade-in | `--transition-fade` (300ms ease opacity) |
| Session error scrim | `--surface-overlay` (base at 80% opacity) |
| `↓ New output` chip | `--surface-elevated`, `--radius-pill`, `--elevation-overlay` |
| Response option buttons | `--surface-elevated`, `--border-default`, `--type-xs`, `--weight-medium` |
| `[Proceed to Approval Gate]` button | `--border-accent`, `--accent-primary` text, `--state-selected-bg` hover |
| Input region background | `--surface-elevated` |
| Input region top border | `--border-default` |
| Input field background | `--surface-raised` |
| Input field border resting | `--border-default` |
| Input field border focus | `--border-accent` + `--state-focus-ring` |
| Input text | `--type-base` (13px), `--text-primary` |
| Placeholder text | `--text-tertiary` |
| Submit button | `--surface-elevated`, `--border-default`, `--type-sm`, `--weight-medium` |
| Mode selector text | `--type-xs`, `--weight-medium`, `--text-secondary` |
| Mode dropdown | `--elevation-overlay`, `--radius-md`, `--z-dropdown` |
| Resize handle resting | transparent |
| Resize handle hover | `--border-emphasis` |
| Resize handle active | `--accent-primary` |
| Panel collapse transition | `--transition-panel` |
| Collapsed rail width | 40px |
| Compact-mode toggle icon | `--text-tertiary` → `--text-secondary` on hover |
| Disabled state | `--state-disabled-opacity` (0.4) |

---

## 14. What the Right Panel Must Never Become

Directly from doctrine, stated as design constraints:

**The primary navigation surface.** The left nav is the map of governed state. The right panel supports work in progress.

**The canonical record browser.** Center workspace record detail views exist for that. Output cards in the right panel may link to records, but they are not the record.

**The place where approvals happen.** Not by prose, not by a cleverly labeled button, not by routing around the center workspace. The panel produces outputs and routes operators. Approval events happen elsewhere.

**The sole place where workflow meaning is visible.** The topbar and context strip carry the persistent state picture. The interaction area carries outputs. If the panel were to disappear, the operator should still understand where they are and what needs doing.

**A surface that obscures who produced an output.** Every output card must show its attribution — whether it came from a direct LLM response, an orchestration coordinator, a delegated specialist, or a continuity artifact. The panel must not render outputs in a way that strips this attribution.

**A surface that makes continuity artifacts look like canonical state.** Working memory, transcript continuity, and compaction products may appear in the interaction area or be referenced in output cards. They must remain visually non-canonical (using the `NON-CANONICAL` label treatment from Session 2 governance tokens).

**A surface that grows to fill the workspace by default.** The panel has a defined maximum width. The center workspace always gets the remaining space. The panel is secondary, and its sizing enforces that.

---

## 15. What This Session Resolves

- The right panel's three-region layout is fully specified: context strip (top, independent scroll), interaction/output area (flex, independent scroll), operator input (fixed bottom).
- The Session 4 open question is resolved: two independent scroll regions plus a compact-mode toggle on the separator, not a full collapse of the context strip.
- Panel width behavior is specified: 280px min, 320px default, 440px max, resize handle at left edge, collapsed rail at 40px.
- The operator input field is specified as a framing input, not a chat box: placeholder text, mode selector with four modes, submit button, keyboard behavior, disabled states.
- Mode selection rules are concrete: Brainstorm is the default (no mode selection required for Class A work), Recommendation/Review/Approval Req. are available on demand, Approval Req. is gated on a prior accepted Recommendation existing in the session.
- The `[Proceed to Approval Gate]` response option is specified at the interaction-area level — its visual treatment (accent border, not filled, not labeled "Approve") enforces the routing distinction.
- Panel-level states (empty, loading, error) are specified.
- Absent-affordance rules are enumerated concretely.
- All token references are to Session 2; no new values introduced.

---

## 16. What This Session Does Not Resolve Yet

- **Individual output card types** — defined in Session 1; this session specifies how they sit in the panel, not what they contain.
- **Mode-specific input behavior** — for example, whether `Recommend` mode should show a scoping sub-prompt before the main input field, or whether `Approval Req.` mode locks to a structured template. These are interaction refinements for Session 23 (Component Behavior Patterns).
- **Notification banners within the panel** — the interaction area may receive inline banners for compaction events, context changes, and similar (as specified in the invalidation matrix). The banner component itself is Session 12.
- **Keyboard shortcuts for mode switching** — Session 21 (Command Palette).
- **Auto-save of in-progress input** — whether partial input is preserved if the operator navigates away mid-session. This is a Session 23/implementation consideration.
- **Lower trace/orchestration surface** — the panel spec does not include the lower surface. Its show/hide behavior and relationship to panel height is deferred to Session 8 (after left nav trees) or Session 9 (center workspace foundation).

---

## 17. Recommended Inputs to Session 6

Session 6 is the Left Nav Shell and Project V tree. The right panel shell is now specified, which means the center workspace has a defined right-side constraint.

**For Session 6 to know:**
- The right panel's default width is 320px, minimum 280px, maximum 440px
- The left nav has `--panel-left-nav-width: 260px` as its Session 2 spatial constant
- The center workspace gets the remaining width: `calc(100vw - 260px - 320px)` at defaults, meaning approximately 740–760px on a 1366px display. This is the primary review surface and it should be comfortable at that width.

**Session 6 must design:**
1. The navigation shell (panel width 260px, header with system switcher, scroll behavior, panel chrome)
2. The Project V tree structure — the most complex of the three system trees
3. Status indicators for all recognized tree item states
4. Per-item navigation affordances
5. The absent-affordance vocabulary for the nav panel — what must never appear

**Key design question for Session 6 to resolve:**
The left nav has a system switcher in its header. This is a second system switcher, alongside the one in the topbar. Both must trigger the same EVENT-11 (Current System Changed). Session 6 should specify whether the left nav's system switcher is a primary control or a redundant secondary — and whether clicking "VEDA" in the left nav header switches the full session system, or just switches which tree is visible in the nav without changing the session system. The topbar is the canonical system authority. The left nav system switcher's exact relationship to topbar state needs to be explicit to avoid creating the impression that system context can drift independently in the nav.
