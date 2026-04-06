# Session 23 — Component Behavior Patterns
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–22 (all surfaces designed; full visual language formalized)
**Required before:** Session 24 (MVP Shell and Surface Priority) — the build sequence must know which behavior patterns are MVP-required vs. enhancement

---

## 1. What This Session Is

Sessions 3–22 specified *what* components look like and what they do. Session 23 specifies *how* they behave across their state transitions — the motion, the hover/focus/active states, the disabled treatments, and the interaction mechanics that make a governance application feel precise and trustworthy rather than sluggish or surprising.

This session does not invent new components. Every component referenced here was designed in a prior session. This session is a behavior layer over the existing component inventory — it completes what prior sessions deferred to "Session 23."

### The governing principle

Behavior patterns in a governance application must reinforce the cognitive model, not fight it. Motion signals meaning: a gate activating should feel consequential, a panel sliding should feel physical, a stale marker appearing should feel like a warning. Behavior that is purely decorative, or that uses motion to create excitement rather than meaning, is wrong for this application.

Every behavior decision in this session is justified by what it communicates, not by what it looks like.

---

## 2. Component Inventory

The complete set of interactive components across Sessions 3–21:

**Shell chrome:** Topbar elements (project scope indicator, system indicator, stage indicator, attention badges, session health indicator), panel resize handles, panel collapse/expand toggle, lower trace toggle chip.

**Left nav:** System switcher, section headers (expand/collapse), tree items (hover, selected, active), status dots, handoff status badges, gap severity icons, return trigger items, nav footer actions.

**Right panel:** Context strip rows (expand/collapse), compact-mode toggle, output cards (response option buttons, `[Proceed to Approval Gate]` CTA, `↓ New output` chip), mode selector dropdown, operator input field, submit button, panel collapse toggle.

**Center workspace:** Tab bar (tabs, close button, `+ New Tab`), section nav tabs, record content sections, inline banners, staleness markers.

**Gate surfaces:** Class B widget (inactive, active, post-approval, post-rejection), `[Approve]` / `[Reject]` / `[Defer]` controls, rejection reason prompt, stale-context warning acknowledgment, Class C modal trigger, Class C modal, typed confirmation input, Class D escalation banner.

**Power features:** Portfolio cards (urgency accent, switch CTA), lower trace tabs, task rows (status dots, lifecycle states), compaction event blocks, transcript entries, filter chips.

**Command palette:** Search input, result items, category headers, keyboard shortcut chips, context strip footer.

---

## 3. Global Interaction Primitives

These patterns apply universally. Every interactive component inherits them unless the component spec explicitly overrides.

### 3.1 Hover State

```
background-color: var(--state-hover-overlay)    /* rgba(255,255,255,0.06) */
transition:       --transition-instant            /* all 100ms ease */
```

Applied as a pseudo-element overlay (`::after`) on the component, not as a background-color change. This avoids clobbering the component's own background color.

**Why pseudo-element:** Components like nav tree items and output cards already have their own background colors. Applying hover as an overlay preserves the underlying color and stacks cleanly. A direct `background-color` change on hover would require each component to know its own resting background — brittle and error-prone.

**Cursor:** `pointer` on all interactive elements. `not-allowed` on disabled elements. `col-resize` on resize handles. `row-resize` on the lower trace resize handle. `default` on read-only display elements.

### 3.2 Active / Pressed State

```
background-color: var(--state-active-overlay)   /* rgba(255,255,255,0.10) */
transition:       --transition-instant
```

Appears immediately on `mousedown` / `touchstart`. The pressed state feedback must be instant — any perceptible delay between click and visual response degrades perceived responsiveness. After release, the action executes; the active overlay fades out with `--transition-fast` (150ms).

### 3.3 Focus State (Keyboard Navigation)

```
outline:        var(--state-focus-ring)          /* 2px solid #ffd64f */
outline-offset: var(--state-focus-offset)        /* 2px */
transition:     --transition-instant
```

The amber focus ring appears on `:focus-visible` (keyboard navigation only — not on mouse click). This is the Bricks behavior from `frontend-layer.min.css`: `body.bricks-is-frontend :focus-visible { outline: auto }`. The V Ecosystem replaces the browser default with the explicit amber ring.

**No focus ring on mouse click.** `:focus-visible` is the correct selector — it suppresses the ring on pointer interactions, shows it on keyboard navigation. This is standard modern practice and follows the Bricks pattern.

**Focus ring offset:** 2px creates a gap between the component edge and the ring, making the ring visible against the component's own border.

**Focus ring on input fields:** For text inputs, the focus ring is replaced by a border-color transition (per Session 22 `--input-border-focus: --accent-primary`). This follows Bricks: inputs communicate focus through their border, not an outline ring. The outline is suppressed on inputs in favor of border treatment.

### 3.4 Disabled State

```
opacity:        var(--state-disabled-opacity)    /* 0.4 */
cursor:         not-allowed
pointer-events: none  (in most contexts)
transition:     --transition-default
```

Disabled state appears immediately — no delay, no animation into disabled. The `opacity` approach means the disabled component retains its shape and position, communicating "this exists and will be available, just not now" rather than disappearing entirely.

**Important:** `pointer-events: none` must be the outermost element. If a tooltip is needed on a disabled element (explaining why it is disabled), the tooltip wrapper must be `pointer-events: auto` with the inner element at `none`. This allows hover tooltips on disabled buttons without enabling clicks.

### 3.5 Selected State

```
background-color: var(--state-selected-bg)       /* #58470e */
border-left:      2px solid var(--accent-primary) /* #ffd64f */
transition:       --transition-default
```

Used for: active nav tree item, active workspace tab, selected command palette result, currently-active portfolio card. The amber-tinted background + left-border combination is the V Ecosystem's visual vocabulary for "this item is the one you are in/on."

The `--state-selected-bg` at `#58470e` (Session 22 revision from `rgba`) gives a more solid, intentional selected appearance that works at the Bricks dark density level.

---

## 4. Motion Vocabulary by Interaction Type

This section defines which motion token applies to which type of interaction, so implementers can consistently choose the correct preset.

### 4.1 Appear / Disappear (Show / Hide)

| Scenario | Token | Notes |
|---|---|---|
| Dropdown opens (system switcher, mode selector) | `--transition-default` opacity+transform | Scale from 96%→100%, opacity 0→1 |
| Command palette opens | `--transition-default` opacity+scale | 96%→100%, 0→1 — same pattern |
| Tooltip appears | `--transition-fast` opacity | 0→1, no scale |
| Toast / notification enters | `--transition-default` translateY + opacity | Slides in from top of its zone |
| Toast / notification exits | `--transition-fast` opacity | Fades out only — no reverse slide |
| Modal opens (Class C, session integrity) | `--transition-default` opacity+scale | 97%→100%, 0→1 |
| Modal scrim | `--transition-default` opacity | 0 → 0.8 |
| Panel opens / closes (right panel, left nav) | `--transition-panel` transform | translateX, 400ms ease-in-out |
| Lower trace opens / closes | `--transition-panel` transform | translateY, 400ms ease-in-out |
| Inline banner appears | `--transition-fade` opacity | 300ms ease — banners don't slide |
| Inline banner dismisses | `--transition-fast` opacity | 150ms — quick exit |
| Attention badge count changes | `--transition-fast` | Cross-fade between numbers, no layout shift |
| Attention badge appears | `--transition-fast` scale | 0→1 scale from center |
| Attention badge disappears | `--transition-fast` opacity | 1→0 |

### 4.2 State Transitions (Within a Component)

| Scenario | Token | Notes |
|---|---|---|
| Gate widget activates | `--transition-spring` border+shadow | The amber border + glow fires with spring easing — signals consequence |
| Gate widget deactivates | `--transition-default` | Softer return — deactivation is less of an event than activation |
| Input focus | `--transition-input` border | background+border 150ms — the Bricks filter-indicator timing |
| Input blur | `--transition-input` border | Returns to resting state |
| Input correct (typed confirmation) | `--transition-default` border | Border transitions to `--border-accent` |
| Button hover | `--transition-instant` overlay | Instant — hover must feel responsive |
| Button active / pressed | `--transition-instant` overlay | Same |
| Status dot color change | `--transition-default` background-color | e.g., task running → completed |
| Running task dot pulse | 2s ease-in-out infinite opacity loop | 1.0 → 0.4 → 1.0 — the live signal |
| Checkpoint ○ → ✓ | `--transition-default` opacity+color | Individual checkpoint transition |
| Section header expand/collapse | `--transition-accordion` height | 500ms ease — deliberate; expanding context strip rows |
| Tree item expand (subtree) | `--transition-slide` transform | 200ms ease-out — snappy tree reveal |
| Tab switch (section nav) | `--transition-default` indicator | Bottom border slides between active tabs |
| Context strip row expand | `--transition-accordion` height | Same as section header; same component |
| System change tree swap | `--transition-fade` opacity | Current tree fades out, new tree fades in |
| Record detail load (center workspace) | `--transition-fade` opacity | Shimmer → content |
| Compact-mode toggle fires | `--transition-accordion` height | All rows compress simultaneously |

### 4.3 Navigation / Routing

| Scenario | Motion | Notes |
|---|---|---|
| Tab opens (workspace) | New tab enters from right at 0→1 opacity | No slide — content appears, tab appears |
| Tab closes | Tab shrinks horizontally with `--transition-default` | Other tabs fill the gap |
| Center workspace content switches | `--transition-fade` on content area only | Tab bar does not animate |
| Command palette closes (command executed) | `--transition-fast` opacity 1→0 | Quick exit, focus moves to target surface |
| Panel resize drag | No transition — live resize | Dragging must track cursor exactly; transitions interfere |

---

## 5. Component-Specific Behavior Patterns

### 5.1 Topbar Elements

**Project scope indicator (Element 1):**
- Hover: `--state-hover-overlay` on the element group (icon + name + arrow)
- Active: `--state-active-overlay`
- Dropdown opens: scale from 98%→100% + opacity 0→1, `--transition-default`, origin: top-left of dropdown (below the element)
- The project name itself is not separately hoverable — the whole element group is the click target

**System indicator (Element 3):**
- Same hover/active as project scope indicator
- System color change on system switch: cross-fade using `--transition-default` — the system name and color both transition simultaneously
- The `▾` arrow rotates 180° when dropdown is open: `transform: rotate(180deg)`, `--transition-fast`

**Attention badges (Elements 5, 6, 7):**
- Count change: the number cross-fades (opacity 1→0, number changes, opacity 0→1), `--duration-fast` (150ms) each direction — total 300ms for a count change. No layout shift.
- Badge appears (count was 0, now > 0): `transform: scale(0)` → `scale(1)` + opacity 0→1, `--transition-fast`, spring easing (`--ease-spring`) — the badge "pops" into existence
- Badge disappears: opacity 1→0, `--transition-fast`
- The `⚡` pulse animation (reconnecting state): 0.4s ease opacity loop per Session 2

**Session health indicator (Element 8):**
- State dot color changes: `--transition-default` background-color
- Recovery cross-fade (danger → success after re-initialization): `--duration-slow` (400ms) — the one slow transition in the topbar, because re-establishing a healthy session is a meaningful moment

### 5.2 Nav Tree Items

**Row hover:**
- `--state-hover-overlay` overlay appears, `--transition-instant`
- Navigation arrow `›` fades in: opacity 0→0.6, `--transition-instant`

**Row selection (click):**
- Active overlay on click, `--transition-instant`
- Then: `--state-selected-bg` background fills in, `--transition-default`; left border 2px `--accent-primary` appears simultaneously
- The center workspace begins loading the record; the nav item retains its selected state until navigation completes or fails

**Expand/collapse (section headers, subtrees):**
- Chevron `›` rotates to `⌄`: `transform: rotate(90deg)`, `--transition-fast` (150ms)
- Content below expands: `--transition-slide` (transform + opacity, 200ms ease-out) — the subtree slides down and fades in simultaneously. Not accordion/height because the tree uses absolute height for performance; it's a translateY + opacity entrance.

**Status dot color change (when invalidation event updates a record's status):**
- `--transition-default` background-color (200ms ease)
- Never instant — status changes should register visually without being startling

**Return triggers section appears (EVENT-16):**
- Section slides in at the top of the tree: the entire section enters with `--transition-slide` (translateY from -100% to 0%, opacity 0→1, 200ms ease-out)
- Other sections shift down with `--transition-default`
- This section's entrance is the most visually assertive transition in the nav — it is designed to be noticed

### 5.3 Right Panel Components

**Context strip row expand/collapse:**
- Chevron rotates 90°: `--transition-fast`
- Row height expands: `--transition-accordion` (height 500ms ease) — this is the Bricks accordion timing. Context strip rows contain dense structured content; the deliberate expansion gives the operator time to track what is appearing.
- Content within the expanding row fades in: `--transition-fade` (opacity 300ms) with a 100ms delay after height begins expanding — the content appears slightly after the space opens

**Compact-mode toggle (separator):**
- All expanded rows compress simultaneously: each row fires `--transition-accordion` with a 30ms stagger per row (row 1 at 0ms, row 2 at 30ms, row 3 at 60ms, etc.) — the cascade gives the compression a ripple quality rather than all rows snapping at once
- Total compression time for 9 rows: 500ms + (8 × 30ms) = ~740ms — deliberate

**Output card appearance (new card arrives):**
- Loading placeholder: opacity pulse using `--state-hover-overlay` on `--surface-raised` background, `--duration-moderate` (300ms) per cycle
- Card arrives: placeholder transitions to real card content using `--transition-fade` (opacity 0→1, 300ms ease). No layout shift — the placeholder occupies the same height as the arriving card (estimated from output type).

**`↓ New output` chip:**
- Enters: opacity 0→1 + translateY 8px→0, `--transition-default`
- Exits: opacity 1→0, `--transition-fast`

**`[Proceed to Approval Gate]` button:**
- Hover: amber border brightens slightly (border-color to `--accent-primary` at full opacity from a slightly dimmer default), `--transition-instant`; background fills with `--state-selected-bg`, `--transition-instant`
- Active: `--state-active-overlay`
- This button must feel distinct from standard response options — its spring-ready visual weight communicates that it is the governance path

**Operator input field:**
- Focus: border transitions from `--border-default` to `--border-accent`, `--transition-input` (150ms ease). Background shifts from `--surface-raised` to `--surface-elevated`, same timing. These two transitions fire together.
- Blur: reverses with same timing
- Input expanding (multi-line): height transitions smoothly with `transition: height 150ms ease` as lines are added. Panel height adjusts proportionally.

**Mode selector dropdown:**
- Opens: dropdown appears below the selector with opacity 0→1 + scaleY from 0.97→1, origin: top-center, `--transition-default`
- Closes: opacity 1→0, `--transition-fast`
- Selected option: highlighted with `--state-selected-bg`, `--transition-instant` on hover between options

**Submit button:**
- Hover: `--state-hover-overlay`, `--transition-instant`
- Active: `--state-active-overlay`, `--transition-instant`
- Disabled → enabled transition: opacity 0.4→1, `--transition-default` — this happens when the input field receives its first non-whitespace character

### 5.4 Center Workspace

**Tab bar:**

*Tab opens:*
- New tab appears with opacity 0→1, `--transition-fast`. No slide from right — tabs don't have directional semantics.
- Other tabs shrink proportionally to accommodate the new tab, with `--transition-default` on width.

*Tab closes:*
- The closed tab shrinks its width to 0 with opacity transition to 0, `--transition-default`
- Other tabs fill the gap simultaneously with `--transition-default`
- The `×` close control appears on tab hover: opacity 0→1, `--transition-instant`
- Active tab indicator (2px bottom border): when switching tabs, the indicator does not slide — it fades out on old tab and fades in on new, `--transition-fast` each direction. (Sliding indicators imply spatial relationship between tabs that does not exist here.)

*Tab loading state:*
- View body shows shimmer pattern: `--state-hover-overlay` pulse on `--surface-raised` background areas representing the expected content structure. Pulse timing: `--duration-moderate` (300ms) per cycle with a 600ms offset between shimmers.

**Section nav tabs (within record detail view):**
- Active indicator (2px bottom border) transitions with the tab: the old indicator fades out (opacity 1→0, `--transition-fast`), the new indicator fades in (opacity 0→1, `--transition-fast`). Both transitions fire simultaneously during the tab switch.
- Section content transition: the content area fades out and back in, `--transition-fast` each direction. No slide — section content does not have spatial directionality.

**Inline banners:**
- Appear: opacity 0→1, `--transition-fade` (300ms ease). No slide. Banners are not arriving from somewhere — they are becoming visible.
- Dismiss (dismissible banners only): opacity 1→0, `--transition-fast`, then height collapses, `--transition-accordion`. The content disappears before the space closes.
- Multiple banners stacking: each new banner slides in below existing banners with `--transition-slide` (translateY from above + opacity, 200ms ease-out).

**Staleness markers on output cards:**
- Appear: opacity 0→1, `--transition-fade` (300ms). The card itself does not move — only the marker appears above it.
- The `--staleness-bg` fill of the marker also transitions in with the opacity, giving a warm amber wash over the top of the card.

### 5.5 Gate Surfaces

**Class B widget — inactive → active transition (all checkpoints satisfied):**

This is the most important transition in the application. The gate activating communicates: you may now make a governance decision. The behavior must feel consequential without being alarming.

Sequence:
1. Final checkpoint transitions from `○` to `✓`: `--transition-default` (200ms) on opacity and color of the checkmark glyph
2. 100ms pause after final checkpoint completes
3. Checkpoint status line transitions from `○ Complete required review` to `✓ Required checkpoints complete — gate is active`: opacity cross-fade, `--transition-default`
4. Gate widget border transitions from `--border-subtle` to `--border-accent`: `--transition-spring` (200ms cubic-bezier(0.215,0.61,0.355,1)) — the spring easing adds a slight overshoot that makes the border change feel like a physical click into place
5. Simultaneously: `--gate-active-shadow` (amber glow) fades in with `--transition-spring`
6. Gate controls transition from `--state-disabled-opacity` (0.4) to full opacity: `--transition-default` (200ms), with a 50ms delay after the border spring — the controls become active slightly after the visual "unlock" signal

Total gate activation sequence duration: ~550ms from final checkpoint to fully active controls. This is deliberate — the activation should register clearly, not flash past.

**`[Approve]` button:**
- Resting: amber fill (`--accent-primary`), `--text-inverse` text
- Hover: background brightens (add 8% white to amber: approximately `#ffdc66`), `--transition-instant`
- Active: darker amber (8% black mix: approximately `#e6c046`), `--transition-instant`
- Post-click loading state: button becomes `--state-disabled-opacity` while the write is in flight (typically <500ms); an optional subtle spinner icon appears in the button text area
- Post-write success: button transitions to the post-approval confirmation state with `--transition-default`

**`[Reject]` button:**
- Resting: `--surface-raised` background, `--state-danger` border and text
- Hover: `--state-danger-bg` background fills in, `--transition-instant`; border and text retain `--state-danger`
- Active: slightly darker `--state-danger-bg`, `--transition-instant`

**Rejection reason prompt (appears on `[Reject]` click):**
- The prompt area slides down below the controls: `--transition-slide` (translateY 0 → natural height + opacity 0→1, 200ms ease-out)
- The controls row shifts down to accommodate: `--transition-default` on the widget height
- `[Cancel]` within the prompt returns the widget to its gate-active state: the prompt slides back up with `--transition-fast`

**Stale-context warning block:**
- Appears above the gate widget: `--transition-fade` opacity + `--transition-slide` translateY from above
- The gate controls remain in their prior state during this transition; they do not animate when the warning appears
- Warning acknowledgment click: the warning block fades out and slides up, `--transition-default`; gate controls re-evaluate

**Class C modal:**

*Opening:*
- Scrim: `--transition-default` opacity 0→0.8
- Modal: `--transition-default` opacity + scale (97%→100%), firing 50ms after scrim begins
- Origin: center of viewport

*Closing (cancel):*
- Modal: `--transition-fast` opacity 1→0 + scale 100%→97%
- Scrim: `--transition-fast` opacity 0.8→0
- Both fire simultaneously on cancel — quick exit

*Typed confirmation input:*
- Empty → partial → correct: only the border-color transitions (`--transition-input`, 150ms)
- Correct phrase entered: border transitions to `--border-accent`; `[Confirm Authorization]` button simultaneously transitions from 0.4→1 opacity, `--transition-default`. The button uses `--transition-default` here (not spring) because the "unlocking" of the confirm button is a quiet confirmation, not a dramatic gate activation — the drama already happened when the operator typed the phrase deliberately.
- Phrase deleted after being correct: border returns to `--border-default`, button returns to 0.4 opacity, both `--transition-input` timing

**Class D escalation banner:**
- Appears in inline banner position: `--transition-fade` opacity 0→1 + the section nav and content below shift down with `--transition-default`. The banner does not slide in — it fades in. Sliding would suggest the banner arrived from somewhere; it did not. It is a condition that has been detected.
- The banner does not exit until the condition is resolved. No dismiss behavior to animate.
- Post-escalation state transition (after `[Escalate]` click): the content area within the banner cross-fades from the three-field content to the confirmation state, `--transition-default`

### 5.6 Lower Trace Surface

**Panel open/close:**
- Opens: the lower trace panel slides up from the bottom with `--transition-panel` (translateY, 400ms ease-in-out). The center workspace simultaneously shrinks from the bottom with the same timing. Both transitions are synchronized — the workspace edge and the trace panel top move as one boundary.
- Closes: reverse — panel slides down, workspace expands down, synchronized.

**Running task dot pulse:**
- `--state-info` dot: opacity oscillates 1.0 → 0.4 → 1.0 with 2s ease-in-out infinite cycle
- This is a CSS `@keyframes` animation, not a transition — it loops continuously while the task is in `running` state
- When task completes: the pulse animation stops; the dot cross-fades to `--state-success` solid, `--transition-default`
- When task fails: cross-fades to `--state-danger` solid, `--transition-default`

**Task detail expansion:**
- Expands inline below the task row: height 0 → content height + opacity 0→1, `--transition-accordion` (500ms ease) on height, `--transition-fade` (300ms) on opacity with 100ms delay
- Collapses: same timing reversed

**Compaction event block expansion:**
- Same as task detail expansion
- The post-compaction validation table rows appear with a 30ms stagger (same ripple pattern as the compact-mode toggle) to give the multi-row table a sense of sequential loading rather than all rows snapping in at once

**Lower trace tab switch:**
- Content area fades out and in: `--transition-fast` each direction (simultaneous)
- Tab indicator: same treatment as section nav tabs (fade, not slide)

### 5.7 Command Palette

**Open:**
- Scrim: opacity 0→0.6, `--transition-default`
- Palette: opacity 0→1 + scale 96%→100%, `--transition-default`, 30ms after scrim starts (per Session 21 §3.2)
- Input field: auto-focused on open; the cursor blinks immediately

**Close:**
- Palette: opacity 1→0 + scale 100%→97%, `--transition-fast`
- Scrim: opacity 0.6→0, `--transition-fast`
- Both fire simultaneously — command palette exit should be quick and decisive

**Result list navigation (keyboard ↑↓):**
- Selected item: `--state-hover-overlay` background appears on the newly selected item, disappears from the prior item — both `--transition-instant`. Keyboard navigation must feel immediate.
- If the selected item is outside the visible scroll area: the result list scrolls to bring it into view. No animation on this scroll — `scrollIntoView({ behavior: 'instant' })`. Animated scrolling during keyboard navigation creates disorientation.

**Filtering (typing in search input):**
- Result list items that do not match the query: opacity 1→0 + height collapses, `--transition-fast`
- Result list items that match: opacity 0→1, `--transition-fast`
- New result items appearing: slide in with `--transition-slide` (translateY from above + opacity, 200ms ease-out) — appearing results slide into their position rather than just fading in, giving the filtering operation a sense of the list reorganizing

**Shortcut chips (`⌘K`, `⌘⇧P`, etc.):**
- No hover/active behavior — these are display elements, not interactive
- No visual state change on keyboard shortcut activation — the action itself is the feedback

### 5.8 Portfolio Cards

**Card left-border accent:**
- The 3px left border is always present — it does not animate. The urgency is declared, not communicated through motion.
- When a card's highest-urgency item changes (e.g., a return trigger is resolved, changing urgency from high to medium): the border color cross-fades with `--transition-default`. This is the subtle signal that something in the project's state has resolved.

**`[Switch to this project ›]` button:**
- Resting: `--surface-elevated`, `--border-default`, `--text-secondary`
- Hover: border transitions to `--border-accent`, text transitions to `--accent-primary`, `--transition-instant`
- Active: `--state-active-overlay`, `--transition-instant`

**Portfolio tab refresh (manual `[Refresh]` click):**
- All cards simultaneously apply a shimmer (opacity pulse on each card surface, `--duration-moderate` 300ms per cycle, staggered 50ms between cards)
- As data loads, cards update in place: content cross-fades with `--transition-default`
- Cards that have new attention items: a brief pulse of `--state-hover-overlay` draws attention to the updated card (opacity 0→0.15→0, ~400ms total, one pulse only — not looping)

---

## 6. Panel Resize Behavior

### 6.1 Right Panel Resize

The left-edge resize handle of the right panel:

- Handle cursor: `col-resize` on hover
- Handle color: transparent → `--border-emphasis` on hover, → `--accent-primary` while dragging — `--transition-instant` for both transitions
- While dragging: the panel width updates live, tracking the cursor exactly. No transition during drag — `transition: none` on the panel width while `dragging` class is active.
- Snap behavior: at 280px (min) and 440px (max), the panel snaps to the constraint. The snap provides a 2px "bump" sensation via a quick `transform: scaleX(1.005)` → `scaleX(1)` spring on the panel, `--transition-spring` (fast, ~150ms). Not a real scale change — a quick pulse that communicates the constraint.
- On drag end: `transition` is re-applied to the panel for subsequent state changes

### 6.2 Lower Trace Resize

The top-edge resize handle of the lower trace panel:

- Same pattern as right panel resize
- Handle cursor: `row-resize`
- While dragging: `transition: none` on the panel height and center workspace height
- Snap at 160px (min): same spring pulse as right panel at min constraint
- Snap at 400px (max): same treatment

### 6.3 Panel Collapse (Right Panel)

- Collapse trigger: `‹` button in the panel header
- Transition: `--transition-panel` (transform 400ms ease-in-out). The panel slides to the right, narrowing to the 40px rail. The center workspace simultaneously expands to the right at the same speed. The rail attention indicators fade in with `--transition-default` after the collapse completes.
- Expand: reverse. Rail indicators fade out first, then the panel slides in from the right.

---

## 7. Scroll Behavior

### 7.1 Scrollable Regions

Every scrollable region in the application:
- Custom scrollbar: 4px width, `--border-default` thumb, transparent track (per Session 22 §8)
- Scrollbar appears on hover of the scroll region, fades out 1s after last scroll activity
- `scrollbar-gutter: stable` where supported — prevents layout shift when scrollbar appears/disappears

### 7.2 `↓ New output` chip scroll

When the chip is clicked (or the user manually scrolls to the bottom):
- `scrollBehavior: 'smooth'` to the bottom of the interaction area
- Duration: approximately 300ms (browser-handled smooth scroll)
- The chip disappears with `--transition-fast` as soon as the scroll begins (not after it completes)

### 7.3 Record Detail View Scroll on `intent = 'approval_gate'`

When the workspace router opens a record with `intent = 'approval_gate'` (Session 9 §9.3):
- The view opens on the Actions section tab
- After the section content renders (post `--transition-fade`), the view body scrolls to bring the gate widget into view using `scrollBehavior: 'smooth'`
- The gate widget is scrolled to a position where it is fully visible with at least 24px of clear space below it — it should not be pressed against the panel bottom edge

### 7.4 Command Palette Scroll

- Keyboard navigation scrolls result list with `scrollIntoView({ behavior: 'instant' })` — no animation, immediate
- Overflow indicator: when more results exist below the visible area, the last visible result fades to a gradient (bottom edge of result list fades to `--surface-elevated`): this communicates "more results below" without a separate affordance

---

## 8. Timing and Feedback — Governance-Specific Rules

These rules apply specifically to governance-critical interactions. They supersede general motion defaults where they conflict.

### 8.1 Gate Activation Must Not Be Instant

The gate widget activation sequence (`--transition-spring`, 550ms total) cannot be shortened for performance or preference. An instant gate activation would feel like a glitch, not a meaningful state change. The operator must have a moment to register that the gate has become available. This is a conscious design constraint, not an animation preference.

### 8.2 Approval Write Feedback Must Be Synchronous

When the operator clicks `[Approve]` or `[Confirm Authorization]`, the button enters a loading state (opacity 0.4 + optional spinner) immediately — before the API response. If the write succeeds, the widget transitions to its post-approval state. If the write fails, the button returns to active state and a `⚠ Write failed — retry?` notice appears. **The operator must never see the post-approval confirmation state without a successful write.** Optimistic UI (showing confirmation before write success) is not permitted for approval events.

### 8.3 Staleness Markers Must Appear Before the Next Interaction

When an invalidation event produces staleness markers on output cards or the gate widget, those markers must appear before the operator's next click is registered. Implementation: the `refreshCoordinator` fires marker updates synchronously before re-enabling the gate controls after a blocking event. The operator cannot accidentally approve using stale context that the UI has registered but not yet rendered.

### 8.4 Typed Confirmation Must Not Feel Responsive in the Wrong Direction

The typed confirmation input must not give positive visual feedback until the phrase is exactly correct. Partial matches must not produce amber border, partial fill, or progress indicators. The border stays at `--border-default` until the full phrase is correct. This is intentional: partial-match feedback would train the operator to type quickly until something turns amber, not to read and understand the phrase.

### 8.5 Class D Banner Must Not Slide

The Class D escalation banner appears via `--transition-fade` (opacity), not a slide. Sliding would suggest the banner arrived from somewhere, implying it is a temporary notification. Class D conditions are not notifications — they are detected states. The fade-in communicates: "this condition was always here; now it is visible."

---

## 9. Reduced Motion

All transitions and animations in the application must respect `prefers-reduced-motion: reduce`. When reduced motion is preferred:

- All `transform`-based transitions reduce to opacity-only transitions with `--transition-fast` (150ms)
- The running task dot pulse stops (the dot shows as a solid `--state-info` dot without oscillation)
- The compaction validation table row stagger collapses to a single `--transition-fast` opacity appearance for all rows simultaneously
- The gate activation spring collapses to a `--transition-default` border + opacity change
- The return trigger section entrance collapses to `--transition-fade`

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 150ms !important;
    transition-delay: 0ms !important;
  }
}
```

The running task dot pulse requires explicit suppression:
```css
@media (prefers-reduced-motion: reduce) {
  .task-dot-running {
    animation: none !important;
    opacity: 1 !important;
  }
}
```

---

## 10. Component State Reference — Complete Matrix

This table maps every component to its behavioral states. Implementers can use this as a checklist.

| Component | Resting | Hover | Active | Focus | Disabled | Selected | Transition(s) |
|---|---|---|---|---|---|---|---|
| Nav tree item | `--surface-raised` | `+hover-overlay` | `+active-overlay` | focus-ring | dim (0.4) | `--state-selected-bg` + left-border | instant hover; default select |
| Nav section header | `--surface-raised` | `+hover-overlay` | `+active-overlay` | focus-ring | — | — | instant hover; slide chevron |
| Status dot | solid color | — | — | — | dim | — | default color change |
| Handoff status badge | styled per status | `+hover-overlay` | `+active-overlay` | focus-ring | dim | — | default |
| Context strip row | `--surface-raised` | `+hover-overlay` | — | focus-ring | — | — | accordion expand |
| Compact-mode toggle | `--text-tertiary` | `--text-secondary` | — | focus-ring | — | — | instant |
| Output card | `--surface-raised` | — | — | — | dim | — | fade in on arrival |
| Response option button | `--surface-elevated` | `+hover-overlay` | `+active-overlay` | focus-ring | dim | — | instant |
| `[Proceed to Approval Gate]` | amber border | amber fill | active-overlay | focus-ring | dim | — | instant hover |
| Mode selector | transparent | + border-subtle | active-overlay | focus-ring | dim | — | instant |
| Operator input field | `--surface-raised`, `border-default` | — | — | border-accent | dim | — | `--transition-input` |
| Submit button | `--surface-elevated` | `+hover-overlay` | active-overlay | focus-ring | dim | — | instant |
| Workspace tab | `--surface-raised` | `+hover-overlay` | active-overlay | focus-ring | — | `--surface-base` + bottom border | default |
| `×` tab close | opacity 0 | opacity 1 | active-overlay | focus-ring | — | — | instant |
| Section nav tab | secondary text | primary text | active-overlay | focus-ring | — | bottom border indicator | fast fade |
| Inline banner | `--staleness-bg` / other | — | — | — | — | — | fade in |
| Class B widget (inactive) | `border-subtle`, 0.4 controls | — | — | — | — | — | spring on activation |
| Class B widget (active) | `border-accent` + glow, full controls | — | — | — | — | — | spring from inactive |
| `[Approve]` | amber fill | brighter amber | darker amber | focus-ring | dim on amber | — | instant |
| `[Reject]` | surface + danger border | danger-bg fill | darker | focus-ring | dim | — | instant |
| `[Defer]` | surface + default border | hover-overlay | active-overlay | focus-ring | dim | — | instant |
| Typed confirmation input | `--surface-raised` | — | — | border-accent focus | dim | border-accent on correct | `--transition-input` |
| `[Confirm Authorization]` | danger fill (0.4 dim) | brighter danger | darker danger | focus-ring | — | full opacity when correct | default |
| Class D `[Escalate]` | danger fill | brighter | darker | focus-ring | — | — | instant |
| Class D `[Doc and Hold]` | surface + danger border | danger-bg | darker | focus-ring | — | — | instant |
| Resize handle | transparent | `--border-emphasis` | `--accent-primary` | — | — | — | instant |
| Panel collapse toggle | `--text-tertiary` | `--text-secondary` | active-overlay | focus-ring | — | — | instant |
| Task status dot (running) | `--state-info` pulse | — | — | — | — | — | 2s oscillation |
| Lower trace tab | inactive text | primary text | active-overlay | focus-ring | — | bottom border | fast fade |
| Compaction block expand | collapsed | `+hover-overlay` | active-overlay | focus-ring | — | — | accordion |
| Filter chip | `--surface-raised` | `+hover-overlay` | active-overlay | focus-ring | dim | accent border + text | default |
| Portfolio card | `--surface-raised` | — | — | — | — | — | default urgency accent |
| `[Switch to project]` | surface + default border | accent border + text | active-overlay | focus-ring | dim | — | instant |
| Palette result item | `--surface-elevated` | `+hover-overlay` | active-overlay | — | dim (0.4) | — | instant keyboard nav |
| Palette search input | `--surface-elevated` | — | — | — | dim | — | `--transition-input` |
| Command palette | — | — | — | — | — | — | default open/close |
| `[◫ Trace]` toggle chip | `--text-tertiary` | `--text-secondary` | active-overlay | focus-ring | — | `--text-secondary` (open) | instant |

---

## 11. What Session 23 Resolves

- Every interactive component now has a fully specified behavior model: hover, active, focus, disabled, selected states and the exact transition token for each.
- The motion vocabulary is mapped to interaction types: appear/disappear, state transition, navigation — no surface needs to invent its own timing.
- The gate activation sequence is fully specified: a 550ms choreography that gives the unlocking of the `[Approve]` control appropriate weight without being theatrical.
- The governance-specific behavior rules are explicit: gate activation must not be instant, approval write must not be optimistic, typed confirmation must not give partial feedback, Class D banner must not slide in.
- The reduced-motion path is fully specified, including the explicit suppression of the running-task pulse animation.
- The panel resize behavior is specified including the constraint-snap pulse.
- The scroll behavior rules are concrete: instant scroll for keyboard navigation in the palette, smooth scroll for content navigation, auto-scroll suppression in the output area.
- The complete component state reference matrix (§10) gives implementers a single checklist covering every component's behavioral states.

---

## 12. What Session 23 Does Not Resolve

- **Exact CSS animation keyframe code** — the specifications here are behavioral contracts, not implementation code. The engineer translates these into CSS keyframes and transitions based on the token values from Session 22.
- **Platform-specific Tauri behavior** — some interactions (window drag region, native scrollbars on certain OS versions, system-level focus management) are Tauri/OS concerns, not UX design concerns.
- **Breakpoint behavior at narrow window widths** — the desktop application has a minimum window width but narrow-window behavior (e.g., whether the left nav collapses automatically at narrow widths) is not specified here. This would be a future enhancement spec.
- **Tab persistence across sessions** — whether open workspace tabs are restored on session restart was deferred from Session 9. This remains unspecified.
- **Touch/trackpad gesture support** — swipe to collapse panels, pinch to resize, etc. The Tauri desktop application is primarily mouse/keyboard. Touch gesture support is a future enhancement.
- **Dark/light mode transitions** — if a light mode is ever added (Session 22 noted this is out of scope for MVP), the mode-switch transition would be specified then.
