# Session 22 — Full Bricks-Inspired Visual Language Adaptation
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–21 (all surfaces designed; Session 2 minimal token baseline tested across 18 design sessions)
**Required before:** Session 23 (Component Behavior Patterns) — the animation, state-transition, and hover/focus vocabulary built here is the input Session 23 formalizes per-component; Session 24 (MVP Shell) — the visual language is what engineering receives as the styling system

---

## 1. What This Session Is

Session 2 established a working token baseline — enough to keep sessions 3–21 consistent. It explicitly stated: *"It is not the final Bricks adaptation (Session 22)."*

Session 22 is that adaptation. It does three things:

1. **Formalizes the Session 2 baseline** — confirming which values survived intact, which need adjustment after being tested against real surface designs, and which were too coarse and need refinement.

2. **Integrates the builder gray scale** — the Bricks builder CSS (`builder.min.css`) contains a 16-step gray scale (`--builder-gray-0` through `--builder-gray-f`) and a dark-mode surface system that Session 2 approximated. This session replaces the approximation with the real values.

3. **Adds the visual language elements that didn't exist yet in Session 2** — scrollbars, input states, selection highlights, icon sizing, the `⌘` key indicator chip from Session 21, the record type badge system from Session 9, left-border accent patterns from Sessions 10–15, and the command palette visual vocabulary.

This session does not invent new interaction behaviors. Those are Session 23. It does not define component-level animation timing beyond what Session 2 already established. It does not change what any surface does — only what it looks like.

---

## 2. Source Material Summary

### From `frontend-layer.min.css` (the Bricks website layer — already fully extracted in Session 2)

```css
/* Semantic state colors — all confirmed retained from Session 2 */
--bricks-color-primary:   #ffd64f   → --accent-primary:   #ffd64f  ✓
--bricks-text-info:       #00b0f4   → --state-info:        #00b0f4  ✓
--bricks-text-success:    #11b76b   → --state-success:     #11b76b  ✓
--bricks-text-warning:    #ffa100   → --state-warning:     #ffa100  ✓
--bricks-text-danger:     #fa4362   → --state-danger:      #fa4362  ✓
--bricks-bg-dark:         #263238   → --surface-raised:    #263238  ✓
--bricks-tooltip-bg:      #23282d   (used for --surface-elevated in Session 2 — see §4)
--bricks-tooltip-text:    #eaecef   → --text-primary:      #eaecef  ✓
```

### From `builder.min.css` (the Bricks builder dark-mode UI — NEW to Session 22)

```css
/* The complete dark-mode gray scale */
--builder-gray-0:  #090a0c   /* near-black */
--builder-gray-1:  #0d0f12   /* black surface */
--builder-gray-2:  #161a1d   /* builder background (--builder-bg) */
--builder-gray-3:  #293038   /* builder raised surface (--builder-bg-2) */
--builder-gray-4:  #3d4752   /* builder elevated surface (--builder-bg-3) */
--builder-gray-5:  #4e5c6a   /* builder top surface (--builder-bg-4) */
--builder-gray-6:  #687a8d   /* border emphasis */
--builder-gray-7:  #8a99a8   /* description/secondary text */
--builder-gray-8:  #b3bdc7   /* medium text */
--builder-gray-9:  #e2e6e9   /* primary text */
--builder-gray-a:  #848f9a   /* muted text */
--builder-gray-b:  #9aa3ac   /* lighter muted text */
--builder-gray-c:  #abb3ba   /* scrollbar thumb hover */
--builder-gray-d:  #c1c7cd   /* light border */
--builder-gray-e:  #d2d6da   /* very light */
--builder-gray-f:  #e9ebed   /* near-white */

/* Builder semantic layers */
--builder-bg:      #161a1d   (= gray-2) — deepest background
--builder-bg-2:    #293038   (= gray-3) — raised
--builder-bg-3:    #3d4752   (= gray-4) — elevated
--builder-bg-4:    #4e5c6a   (= gray-5) — top layer
--builder-color:   #e2e6e9   (= gray-9) — primary text
--builder-color-description: #8a99a8 (= gray-7) — secondary text

/* Builder accent system */
--builder-color-accent:         #ffd54d   /* amber — note: slightly warmer than #ffd64f */
--builder-bg-accent:            #58470e   /* dark amber background for selected items */
--builder-color-accent-inverse: #1e2124   /* dark text on amber */

/* Builder structural */
--builder-toolbar-height:  48px
--builder-input-height:    32px
--builder-spacing:         16px
--builder-spacing-s:       8px
--builder-border-radius:   4px
--builder-box-shadow:      0 0 12px rgba(0,0,0,.4)
--builder-border-color:    #3d4752   (= gray-4)

/* Builder scrollbar */
--builder-canvas-scrollbar-thumb:       #abb3ba  (= gray-c)
--builder-canvas-scrollbar-thumb_hover: #848f9a  (= gray-a)
--builder-canvas-scrollbar-track:       #e9ebed  (= gray-f)  ← note: light track on dark bg

/* Builder state colors (dark mode) */
--builder-color-info:    #33bbff   → slightly lighter than --state-info
--builder-bg-info:       #00334d
--builder-color-danger:  #e13333
--builder-bg-danger:     #470b0b
--builder-color-success: #2caf84
--builder-bg-success:    #104131
--builder-bg-muted:      #2b333b
--builder-color-muted:   #6c7f93
```

---

## 3. The Complete Token System (Session 22 Final)

This section supersedes Session 2 where values differ. Session 2 values that are confirmed unchanged are marked ✓. New or refined values are marked NEW or REVISED.

### 3.1 Surface Colors

The builder's gray scale provides a more nuanced surface system than Session 2's four-step approximation. The V Ecosystem desktop now maps precisely to this scale.

```css
/* SURFACE TOKENS — FINAL */

--surface-void:      #090a0c   /* NEW: window chrome edges, true-black insets */
                               /* builder-gray-0 */

--surface-deep:      #0d0f12   /* NEW: the darkest panel background; rarely used */
                               /* builder-gray-1 */

--surface-base:      #161a1d   /* REVISED: was #1a1f23 in Session 2; now exact builder-gray-2 */
                               /* center workspace background, main content area */

--surface-raised:    #263238   /* ✓ CONFIRMED: exact bricks-bg-dark; nav panels, cards */
                               /* Session 2 value retained — used in hundreds of surface refs */
                               /* NOTE: builder uses #293038 (gray-3) for its "raised" surface */
                               /* The V Ecosystem retains #263238 because it was extracted from */
                               /* the frontend layer and matches the actual Bricks site panels */

--surface-elevated:  #293038   /* REVISED: was #2e3a42; now exact builder-gray-3 */
                               /* popovers, dropdowns, command palette, modal backgrounds */

--surface-top:       #3d4752   /* REVISED: was not in Session 2; now exact builder-gray-4 */
                               /* input backgrounds, active states, highlighted items */

--surface-overlay:   #161a1d99 /* REVISED: was #1a1f23cc (80%); now base at 60% per Session 21 */
                               /* modal scrim — 60% feels less oppressive on dark surfaces */

--surface-border:    #3d4752   /* REVISED: was #37474f; now exact builder-gray-4 (builder-border-color) */
```

**Why `--surface-raised` stays at `#263238` and not builder `#293038`:**

The Sessions 3–21 designs all use `--surface-raised` as the nav panel and card background. The Bricks website (`frontend.min.css`) defines `--bricks-bg-dark: #263238` which is this same value. The builder uses a slightly different `#293038` for its own panels. Since the V Ecosystem desktop is derived from the Bricks design system (not the builder's own UI), the frontend layer value `#263238` is the correct reference. This is a 6% brightness difference — the panels will look like the Bricks website panels, not like the Bricks builder panels.

### 3.2 Text Colors

```css
/* TEXT TOKENS — FINAL */

--text-primary:      #eaecef   /* ✓ CONFIRMED: bricks-tooltip-text; exact builder-gray-9 is #e2e6e9 */
                               /* Close enough to retain — #eaecef is visually equivalent */

--text-secondary:    #9e9e9e   /* ✓ CONFIRMED: bricks-text-light */
                               /* Note: builder gray-b (#9aa3ac) is the closer builder match */
                               /* But #9e9e9e from bricks frontend is retained for consistency */

--text-tertiary:     #616161   /* ✓ CONFIRMED: bricks-text-medium */
                               /* Builder uses gray-7 (#8a99a8) for description text — but */
                               /* our tertiary is for disabled/placeholder; #616161 is correct */

--text-muted:        #6c7f93   /* NEW: builder-color-muted; for very low-priority annotations */

--text-inverse:      #212121   /* ✓ CONFIRMED: bricks-text-dark; dark text on amber fills */

--text-link:         #00b0f4   /* ✓ CONFIRMED: bricks-text-info / state-info */

--text-description:  #8a99a8   /* NEW: builder-color-description / gray-7; for long-form help text */
                               /* Used in: command palette descriptions, help tooltips */
```

### 3.3 Accent Colors

```css
/* ACCENT TOKENS — FINAL */

--accent-primary:     #ffd64f   /* ✓ CONFIRMED: bricks-color-primary */
                                /* Note: builder uses #ffd54d — 1-digit difference, imperceptible */

--accent-primary-dim: #b89836   /* ✓ CONFIRMED: Session 2 value; used for completed/dim states */

--accent-bg:          #58470e   /* NEW: builder-bg-accent; dark amber for selected/active items */
                                /* Sessions 10–11 needed this for selected result items in palette */
                                /* and gate active background tints */

--accent-inverse:     #1e2124   /* NEW: builder-color-accent-inverse; dark text on amber fills */
                                /* Replaces --text-inverse for amber-fill contexts specifically */
                                /* (--text-inverse #212121 is also acceptable; accent-inverse is */
                                /* the precise builder value) */

--accent-secondary:   #fc5778   /* ✓ CONFIRMED: bricks-color-secondary */
```

### 3.4 State Colors

```css
/* STATE TOKENS — FINAL */
/* All semantic state colors confirmed from bricks frontend layer */

--state-info:         #00b0f4   /* ✓ */
--state-info-bg:      #00334d   /* REVISED: was #0d2a3d; now exact builder-bg-info */

--state-success:      #11b76b   /* ✓ */
--state-success-bg:   #104131   /* REVISED: was #0d2d1f; now exact builder-bg-success */

--state-warning:      #ffa100   /* ✓ */
--state-warning-bg:   #2d2000   /* ✓ CONFIRMED */

--state-danger:       #fa4362   /* ✓ */
--state-danger-bg:    #2d0d12   /* ✓ CONFIRMED */
                                /* Note: builder uses #470b0b for its danger-bg; slightly darker. */
                                /* #2d0d12 was derived from bricks-bg-danger inverted and is */
                                /* used throughout Sessions 10–18 — retained for consistency. */
```

### 3.5 Border Colors

```css
/* BORDER TOKENS — FINAL */

--border-subtle:    #2e3a42   /* ✓ CONFIRMED: barely-visible structural division */
                              /* (between gray-3 and gray-4 — appropriate for dark surfaces) */

--border-default:   #3d4752   /* REVISED: was #37474f; now exact builder-gray-4 / builder-border-color */

--border-emphasis:  #4e5c6a   /* REVISED: was #546e7a; now exact builder-gray-5 */

--border-accent:    #ffd64f   /* ✓ CONFIRMED: amber accent for focused/selected states */

--border-danger:    #fa4362   /* ✓ CONFIRMED: error state borders */
```

### 3.6 Governance-Specific Colors

```css
/* GOVERNANCE TOKENS — FINAL */
/* All retained from Session 2 — tested and confirmed across sessions 3–21 */

--staleness-bg:          #2d2000   /* = --state-warning-bg */
--staleness-border:      #ffa100   /* = --state-warning */
--staleness-text:        #ffa100   /* = --state-warning */

--schema-pending-bg:     rgba(158, 158, 158, 0.08)
--schema-pending-text:   #616161   /* = --text-tertiary */
--schema-pending-border: #2e3a42   /* = --border-subtle */

--ownership-label-bg:    rgba(0, 176, 244, 0.08)
--ownership-label-text:  #00b0f4   /* = --state-info */
--ownership-label-border:#00b0f4

--inert-label-bg:        rgba(97, 97, 97, 0.15)
--inert-label-text:      #616161   /* = --text-tertiary */

--gate-active-border:    #ffd64f   /* = --accent-primary */
--gate-active-shadow:    0 0 0 2px rgba(255, 214, 79, 0.25)

--continuity-bg:         rgba(255, 161, 0, 0.06)
--continuity-border:     rgba(255, 161, 0, 0.30)
```

### 3.7 Approval Class Badges

```css
/* BADGE TOKENS — FINAL */
/* Confirmed from Sessions 10–11 usage */

--badge-class-a:      #37474f   /* subtle dark — class A is no-gate, low visual weight */
--badge-class-a-text: #9e9e9e

--badge-class-b:      #0d2a3d   /* dark info-blue — awaiting operator approval */
--badge-class-b-text: #00b0f4

--badge-class-c:      #2d0d12   /* dark danger-red — typed confirmation required */
--badge-class-c-text: #fa4362

--badge-class-d:      #fa4362   /* full danger fill — escalation required */
--badge-class-d-text: #ffffff
```

---

## 4. Revised Surface Elevation Model

Session 2 defined four elevation levels. With the builder gray scale now available, the elevation model becomes more precise.

### The Surface Hierarchy

```
--surface-void:     #090a0c   z-depth -∞   window chrome, true-black insets
--surface-deep:     #0d0f12   z-depth 0    (rarely used directly)
--surface-base:     #161a1d   z-depth 1    center workspace background
──────── AMBIENT SURFACE LINE ────────────────────────────────────────
--surface-raised:   #263238   z-depth 2    nav panels, cards, right panel
--surface-elevated: #293038   z-depth 3    dropdowns, popovers, palette
--surface-top:      #3d4752   z-depth 4    inputs, active items, hover targets
```

The `--surface-raised` gap (from `#1a1f23` to `#263238`) is intentionally larger than the other steps. This is the most visually important elevation — the distinction between "the workspace" and "the panels that sit on it." The larger gap ensures panels read as sitting above the workspace without needing drop shadows at normal display densities.

### Shadow by Elevation

```css
--elevation-flat:    none
/* In-panel content, tree items, context strip rows */

--elevation-raised:  0 1px 3px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3)
/* Cards, left nav panel, topbar, right panel */
/* Matches builder: 0 0 12px rgba(0,0,0,.4) compressed */

--elevation-overlay: 0 4px 12px rgba(0,0,0,0.5), 0 2px 4px rgba(0,0,0,0.4)
/* Dropdowns, command palette, floating tooltips */

--elevation-modal:   0 16px 48px rgba(0,0,0,0.6), 0 6px 16px rgba(0,0,0,0.5)
/* Class C modal gate, session integrity overlay */
```

---

## 5. Typography — Final

Session 2's type scale survives intact. Two additions from builder inspection:

```css
/* TYPE SCALE — FINAL (Session 2 values + additions) */

--type-xs:      11px   /* ✓ — metadata, timestamps, badges */
--type-sm:      12px   /* ✓ — labels, context strip rows */
--type-base:    13px   /* ✓ — body text in cards */
--type-md:      14px   /* ✓ — primary UI text, nav items */
--type-lg:      16px   /* ✓ — section headings, card titles */
--type-xl:      20px   /* ✓ — modal titles */

/* ADDITIONS from builder inspection */

--type-builder-sm:  12px   /* builder uses 12px for context menus, tooltips */
                            /* = --type-sm; named explicitly for cross-reference */
--type-code:        13px   /* inline code, record IDs, monospace content */
                            /* builder: font-size: 12px for shortcut labels, code */
                            /* V Ecosystem uses 13px (= --type-base) for readability */

/* WEIGHT SCALE — FINAL */

--weight-normal:    400   /* ✓ */
--weight-medium:    500   /* ✓ */
--weight-semibold:  600   /* ✓ */
--weight-bold:      700   /* ✓ */

/* FONT STACKS — FINAL */

--font-ui: -apple-system, "system-ui", "Segoe UI", roboto, helvetica, arial,
           sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"
/* ✓ — exact Bricks frontend stack */

--font-mono: "SF Mono", "Consolas", "Fira Code", "Cascadia Code",
             "Roboto Mono", monospace
/* ✓ — Session 2 value; builder uses: menlo, "Consolas", monaco, "Courier New", monospace */
/* Retaining Session 2 stack because it prioritizes higher-quality fonts on modern systems */
```

---

## 6. Interaction States — Final

```css
/* INTERACTION STATE TOKENS — FINAL */

--state-hover-overlay:    rgba(255, 255, 255, 0.06)   /* ✓ */
--state-active-overlay:   rgba(255, 255, 255, 0.10)   /* ✓ */

--state-selected-bg:      #58470e   /* REVISED: was rgba(255,214,79,0.12); now exact */
                                    /* builder-bg-accent which is the builder's selected item bg */
                                    /* This is used in: command palette selected result, */
                                    /* active nav item background tint */

--state-selected-border:  #ffd64f   /* ✓ = --accent-primary */

--state-focus-ring:       2px solid #ffd64f   /* ✓ = 2px solid --accent-primary */
--state-focus-offset:     2px                 /* ✓ */

--state-disabled-opacity: 0.4   /* ✓ */

--state-inert-opacity:    0.75  /* ✓ */
--state-inert-border:     #3d4752   /* REVISED: now = --border-default */
```

---

## 7. New Visual Components Added in Sessions 3–21

These components appeared in the design work but were not in Session 2's token set. They are formalized here.

### 7.1 Left-Border Accent Pattern

Used extensively in Sessions 10–15 for inline banners, card left accents, gate widget activation, and the lower trace surface. The pattern is:

```css
/* Left-border accent — the V Ecosystem's primary visual urgency signal */
/* Usage: session integrity items, portfolio cards, gate stale-context warnings */
/* Always 3px, always left-only, never radiused on that side */

.left-accent-danger  { border-left: 3px solid var(--state-danger); }
.left-accent-warning { border-left: 3px solid var(--state-warning); }
.left-accent-info    { border-left: 3px solid var(--state-info); }
.left-accent-success { border-left: 3px solid var(--state-success); }
.left-accent-blocked { border-left: 3px solid var(--state-blocked); }
.left-accent-accent  { border-left: 3px solid var(--accent-primary); }

/* Active project card in portfolio: 3px accent-primary — overrides urgency */
/* Width: always 3px. 4px reserved for the Class D escalation banner only. */
```

**The Class D escalation banner** (Session 10 §7.3) uses 4px — slightly wider than standard to signal it is the most severe banner category.

### 7.2 Record Type Badge System

Defined in Session 9 §8. The badge pattern:

```css
/* Record type badge — appears in tab bar and view header */
/* Background: system color at 10% opacity */
/* Text: system color, full opacity */
/* Padding: 2px horizontal, 1px vertical */
/* Radius: --radius-sm (2px) */

/* Each system has a badge color family: */
/* Project V:     --text-primary */
/* VEDA:          --state-info */
/* V Forge:       --accent-primary */
/* Cross-system:  --state-danger (return triggers) or --state-pending (approvals) */

/* Special case: HANDOFF badge uses --state-warning (amber) per handoff urgency vocabulary */
/* DECISION badge uses --accent-primary (the most governance-significant Project V record) */
/* GAP badge uses --state-danger */
```

### 7.3 Keyboard Key Indicator Chip

Introduced in Session 21 for the command palette and shortcut display.

```css
/* ⌘ key indicator chip */
/* Used in: command palette search input, shortcut display in results */

.key-chip {
  background-color: var(--surface-raised);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);   /* 2px */
  padding: 2px 5px;
  font-family: var(--font-mono);
  font-size: var(--type-xs);          /* 11px */
  color: var(--text-tertiary);
  line-height: 1.4;
  display: inline-flex;
  align-items: center;
  height: 18px;
  min-width: 20px;
}

/* Multi-key combos (e.g., ⌘⇧P): */
/* Render as separate chips side by side with --space-1 (4px) gap */
/* "+" separator between chips: --text-tertiary, same size */
```

### 7.4 Stage Badge `*` Notation

Schema-pending stages use a `*` suffix appended to the stage label. The `*` is styled identically to the label text except at `--type-xs` size with reduced opacity (`--text-tertiary`). It is never bolded. It is a transparency marker, not an alarm.

```css
/* Schema-pending * suffix */
.stage-pending-suffix {
  font-size: var(--type-xs);
  color: var(--text-tertiary);
  font-weight: var(--weight-normal);
  margin-left: 2px;
}
```

### 7.5 Compact Boundary Marker (`[cb-XX]`)

Used in the lower trace Compaction view and context strip CONTINUITY row.

```css
/* Compact boundary ID marker */
.compact-boundary-id {
  font-family: var(--font-mono);
  font-size: var(--type-xs);
  color: var(--text-tertiary);
  background-color: var(--continuity-bg);
  border: 1px solid var(--continuity-border);
  border-radius: var(--radius-sm);
  padding: 1px 4px;
}
```

### 7.6 Non-Canonical Notice Block

Used in the lower trace surface (Session 18) and throughout the system wherever non-canonical content must be labeled.

```css
/* Non-canonical notice block */
/* Always left-border 3px --state-info, --surface-raised background */
/* Never dismissible when it is a permanent architectural identity declaration */
.non-canonical-notice {
  background-color: var(--surface-raised);
  border-left: 3px solid var(--state-info);
  padding: var(--space-2) var(--space-3);   /* 8px 12px */
  font-size: var(--type-xs);
  color: var(--text-tertiary);
  line-height: 1.5;
}
```

### 7.7 `[SCHEMA PENDING]` Inline Tag

Used in detail view headers and surface areas where stage derivation fails.

```css
/* [SCHEMA PENDING] inline tag */
.schema-pending-tag {
  background-color: var(--schema-pending-bg);   /* rgba(158,158,158,0.08) */
  border: 1px solid var(--schema-pending-border);
  border-radius: var(--radius-sm);
  padding: 1px 5px;
  font-size: var(--type-xs);
  color: var(--schema-pending-text);   /* --text-tertiary */
  font-weight: var(--weight-medium);
}
```

---

## 8. Scrollbar System

Session 2 did not define scrollbars. The builder provides a clear model.

```css
/* SCROLLBAR SYSTEM */
/* Thin scrollbars — 4px width — for all scrollable panels */
/* Matches Bricks builder's clean minimal scrollbar treatment */

::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

::-webkit-scrollbar-track {
  background: transparent;
  /* Note: builder uses --builder-gray-f (#e9ebed) for its canvas scrollbar track */
  /* V Ecosystem dark surfaces use transparent track — less visual noise */
}

::-webkit-scrollbar-thumb {
  background-color: var(--border-default);   /* #3d4752 = builder-gray-4 */
  border-radius: 2px;
}

::-webkit-scrollbar-thumb:hover {
  background-color: var(--border-emphasis);   /* #4e5c6a = builder-gray-5 */
}

/* Firefox */
scrollbar-width: thin;
scrollbar-color: var(--border-default) transparent;
```

---

## 9. Input and Form Element System

The builder's input system establishes:
- `--builder-input-height: 32px` for compact inputs
- `--builder-popup-input-height: 40px` for modal/popup inputs

```css
/* INPUT SYSTEM — FINAL */

--input-height-compact:  32px   /* inline inputs, search fields, small form elements */
--input-height-default:  40px   /* modal forms, standalone inputs */
--input-height-large:    44px   /* typed confirmation input (Session 10 §6.4) */

--input-padding-x:       12px   /* = builder-input-padding-x; horizontal input padding */
--input-padding-y:       8px    /* derived from builder's line-height patterns */

--input-bg:              var(--surface-raised)   /* #263238 */
--input-bg-focus:        var(--surface-elevated)  /* #293038 — subtle lift on focus */

--input-border:          var(--border-default)    /* #3d4752 */
--input-border-focus:    var(--accent-primary)    /* #ffd64f — amber on focus */
--input-border-error:    var(--state-danger)      /* #fa4362 */
--input-border-success:  var(--state-success)     /* #11b76b — e.g., typed confirmation correct */

--input-text:            var(--text-primary)      /* #eaecef */
--input-placeholder:     var(--text-tertiary)     /* #616161 */

--input-radius:          var(--radius-md)         /* 4px — exact Bricks --builder-border-radius */
```

---

## 10. Icon System

The builder establishes `--builder-icon-width: 28px` for toolbar icons. The V Ecosystem uses smaller icons for its dense information surfaces.

```css
/* ICON SIZE SYSTEM */

--icon-xs:   12px   /* inline glyphs in compact rows: attention badges, compact badges */
--icon-sm:   14px   /* in-line state icons: ⚡ ⊕ ⚠ ◈ ⛔ in attention items */
--icon-md:   16px   /* standard icon size: nav tree items, button icons */
--icon-lg:   20px   /* section header icons, panel header icons */
--icon-xl:   24px   /* modal title icons, large state indicators */
--icon-hero: 40px   /* empty state icons (◈ in center workspace) */
```

**Governance glyph reference** (used throughout the system):

| Glyph | Meaning | Used in |
|---|---|---|
| `◈` | Scope anchor / authorization pending | Topbar project prefix, `[Currently active]` portfolio card, schema-pending stages in certain contexts |
| `⚡` | Urgent / return trigger | Attention badge, return trigger items, blocked execution |
| `⊕` | Pending approval | Attention badge, ARP cards |
| `⛔` | Hard block / expired | Blocking conditions, expired evidence, escalation |
| `◐` | Partial / paused | Surface paused status, partial posture indicators |
| `⚠` | Warning / stale | Integrity badge, staleness markers |
| `✓` | Complete / confirmed | Post-approval confirmation, checkpoint satisfied |
| `✗` | Rejected | Post-rejection confirmation |
| `○` | Inactive / incomplete | Checkpoint incomplete, empty state |
| `●` | Active / complete | Status dots, completed state |
| `◷` | Deferred | Deferred gate state |
| `≡` | Drag handle | Portfolio ranking drag-to-reorder |
| `◫` | Lower trace toggle | Lower trace panel toggle chip |
| `⌘` | Command key | Command palette key chips |

---

## 11. Z-Index — Confirmed Final

```css
/* Z-INDEX SCALE — FINAL (confirmed across all sessions) */

--z-base:      1      /* normal document flow */
--z-raised:    10     /* output cards above panel content */
--z-dropdown:  100    /* dropdowns, tooltips */
--z-panel:     200    /* left nav, right panel */
--z-topbar:    300    /* topbar — above all panels */
--z-overlay:   400    /* session integrity drawer, tile flyout */
--z-modal:     500    /* Class C modal gate, command palette */
--z-toast:     600    /* in-app notifications */
--z-critical:  700    /* session error overlay, Class D escalation banner */
```

---

## 12. Motion — Confirmed Final

Session 2's motion system survives intact. One addition from builder inspection:

```css
/* From builder: */
/* .bricks-control-popup input filter transitions: background-color 0.15s ease, border-color 0.15s ease */
/* This suggests a 150ms pattern for input state changes specifically */

/* ADDITION: */
--transition-input: background-color 150ms ease, border-color 150ms ease
/* Use for: input focus/blur transitions, input validation state changes */
/* More specific than --transition-fast; only for input background+border combos */
```

All other motion tokens from Session 2 are confirmed:
- `--transition-default: all 200ms ease` ✓
- `--transition-panel: transform 400ms cubic-bezier(0.25,0,0.25,1), opacity 400ms cubic-bezier(0.25,0,0.25,1)` ✓
- `--transition-spring: transform 200ms cubic-bezier(0.215,0.61,0.355,1)` ✓ (gate activation)
- `--transition-fade: opacity 300ms ease` ✓
- `--transition-slide: transform 200ms cubic-bezier(0,0,0.2,1)` ✓
- `--transition-fast: all 150ms ease` ✓

---

## 13. The Complete Final Token Reference

A consolidated reference — the master list every component implementation draws from.

### Colors
```css
/* Surfaces */
--surface-void:       #090a0c
--surface-deep:       #0d0f12
--surface-base:       #161a1d
--surface-raised:     #263238
--surface-elevated:   #293038
--surface-top:        #3d4752
--surface-overlay:    #161a1d99

/* Text */
--text-primary:       #eaecef
--text-secondary:     #9e9e9e
--text-tertiary:      #616161
--text-muted:         #6c7f93
--text-inverse:       #212121
--text-link:          #00b0f4
--text-description:   #8a99a8

/* Accent */
--accent-primary:     #ffd64f
--accent-primary-dim: #b89836
--accent-bg:          #58470e
--accent-inverse:     #1e2124
--accent-secondary:   #fc5778

/* States */
--state-info:         #00b0f4
--state-info-bg:      #00334d
--state-success:      #11b76b
--state-success-bg:   #104131
--state-warning:      #ffa100
--state-warning-bg:   #2d2000
--state-danger:       #fa4362
--state-danger-bg:    #2d0d12
--state-blocked:      #fa4362
--state-pending:      #ffa100
--state-inert:        #616161
--state-schema-hold:  #9e9e9e

/* Borders */
--border-subtle:      #2e3a42
--border-default:     #3d4752
--border-emphasis:    #4e5c6a
--border-accent:      #ffd64f
--border-danger:      #fa4362

/* Interaction */
--state-hover-overlay:   rgba(255,255,255,0.06)
--state-active-overlay:  rgba(255,255,255,0.10)
--state-selected-bg:     #58470e
--state-selected-border: #ffd64f
--state-disabled-opacity: 0.4
--state-inert-opacity:    0.75

/* Governance */
--staleness-bg:         #2d2000
--staleness-border:     #ffa100
--staleness-text:       #ffa100
--schema-pending-bg:    rgba(158,158,158,0.08)
--schema-pending-text:  #616161
--schema-pending-border: #2e3a42
--ownership-label-bg:   rgba(0,176,244,0.08)
--ownership-label-text: #00b0f4
--ownership-label-border: #00b0f4
--inert-label-bg:       rgba(97,97,97,0.15)
--inert-label-text:     #616161
--gate-active-border:   #ffd64f
--gate-active-shadow:   0 0 0 2px rgba(255,214,79,0.25)
--continuity-bg:        rgba(255,161,0,0.06)
--continuity-border:    rgba(255,161,0,0.30)

/* Badges */
--badge-class-a:      #37474f
--badge-class-a-text: #9e9e9e
--badge-class-b:      #0d2a3d
--badge-class-b-text: #00b0f4
--badge-class-c:      #2d0d12
--badge-class-c-text: #fa4362
--badge-class-d:      #fa4362
--badge-class-d-text: #ffffff
```

### Spatial
```css
/* Spacing */
--space-1:   4px
--space-2:   8px
--space-3:   12px
--space-4:   16px
--space-5:   20px
--space-6:   24px
--space-8:   32px
--space-10:  40px
--space-12:  48px

/* Panels */
--panel-topbar-height:    48px
--panel-left-nav-width:   260px
--panel-right-width:      320px
--panel-right-min:        280px
--panel-right-max:        440px
--panel-lower-height:     240px
--panel-border-width:     1px

/* Radius */
--radius-sm:    2px
--radius-md:    4px
--radius-lg:    6px
--radius-pill:  100px

/* Elevation (box-shadow) */
--elevation-flat:    none
--elevation-raised:  0 1px 3px rgba(0,0,0,0.4), 0 1px 2px rgba(0,0,0,0.3)
--elevation-overlay: 0 4px 12px rgba(0,0,0,0.5), 0 2px 4px rgba(0,0,0,0.4)
--elevation-modal:   0 16px 48px rgba(0,0,0,0.6), 0 6px 16px rgba(0,0,0,0.5)

/* Z-index */
--z-base:      1
--z-raised:    10
--z-dropdown:  100
--z-panel:     200
--z-topbar:    300
--z-overlay:   400
--z-modal:     500
--z-toast:     600
--z-critical:  700
```

### Typography
```css
/* Type scale */
--type-xs:    11px
--type-sm:    12px
--type-base:  13px
--type-md:    14px
--type-lg:    16px
--type-xl:    20px

/* Weights */
--weight-normal:    400
--weight-medium:    500
--weight-semibold:  600
--weight-bold:      700

/* Font stacks */
--font-ui:   -apple-system, "system-ui", "Segoe UI", roboto, helvetica, arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"
--font-mono: "SF Mono", "Consolas", "Fira Code", "Cascadia Code", "Roboto Mono", monospace

/* Input */
--input-height-compact:  32px
--input-height-default:  40px
--input-height-large:    44px
--input-padding-x:       12px
--input-padding-y:       8px
--input-bg:              #263238
--input-bg-focus:        #293038
--input-border:          #3d4752
--input-border-focus:    #ffd64f
--input-border-error:    #fa4362
--input-border-success:  #11b76b
--input-text:            #eaecef
--input-placeholder:     #616161
--input-radius:          4px

/* Icons */
--icon-xs:   12px
--icon-sm:   14px
--icon-md:   16px
--icon-lg:   20px
--icon-xl:   24px
--icon-hero: 40px
```

### Motion
```css
/* Easing */
--ease-default:    ease
--ease-out:        cubic-bezier(0, 0, 0.2, 1)
--ease-in-out:     cubic-bezier(0.25, 0, 0.25, 1)
--ease-spring:     cubic-bezier(0.215, 0.61, 0.355, 1)
--ease-anticipate: cubic-bezier(0.55, 0.055, 0.675, 0.19)
--ease-bounce:     cubic-bezier(0.68, -0.55, 0.265, 1.55)

/* Duration */
--duration-instant:    100ms
--duration-fast:       150ms
--duration-default:    200ms
--duration-moderate:   300ms
--duration-slow:       400ms
--duration-deliberate: 500ms

/* Transitions */
--transition-instant:  all var(--duration-instant) var(--ease-default)
--transition-fast:     all var(--duration-fast) var(--ease-default)
--transition-default:  all var(--duration-default) var(--ease-default)
--transition-input:    background-color 150ms ease, border-color 150ms ease
--transition-panel:    transform var(--duration-slow) var(--ease-in-out), opacity var(--duration-slow) var(--ease-in-out)
--transition-slide:    transform var(--duration-default) var(--ease-out)
--transition-spring:   transform var(--duration-default) var(--ease-spring)
--transition-fade:     opacity var(--duration-moderate) var(--ease-default)
--transition-accordion: height var(--duration-deliberate) var(--ease-default)
```

---

## 14. What Changed from Session 2

Summary of revisions for implementers who built against Session 2:

| Token | Session 2 | Session 22 | Change |
|---|---|---|---|
| `--surface-base` | `#1a1f23` | `#161a1d` | Darker — exact builder value |
| `--surface-elevated` | `#2e3a42` | `#293038` | Exact builder-gray-3 |
| `--surface-border` | `#37474f` | `#3d4752` | Exact builder-gray-4 |
| `--state-info-bg` | `#0d2a3d` | `#00334d` | Exact builder-bg-info |
| `--state-success-bg` | `#0d2d1f` | `#104131` | Exact builder-bg-success |
| `--border-default` | `#37474f` | `#3d4752` | Exact builder-border-color |
| `--border-emphasis` | `#546e7a` | `#4e5c6a` | Exact builder-gray-5 |
| `--state-selected-bg` | `rgba(255,214,79,0.12)` | `#58470e` | Exact builder-bg-accent |
| `--state-inert-border` | (derived) | `#3d4752` | Explicit = --border-default |
| `--accent-bg` | (missing) | `#58470e` | NEW |
| `--accent-inverse` | (missing) | `#1e2124` | NEW (= builder-color-accent-inverse) |
| `--surface-void` | (missing) | `#090a0c` | NEW |
| `--surface-deep` | (missing) | `#0d0f12` | NEW |
| `--surface-top` | (missing) | `#3d4752` | NEW |
| `--text-muted` | (missing) | `#6c7f93` | NEW (= builder-color-muted) |
| `--text-description` | (missing) | `#8a99a8` | NEW (= builder-color-description) |
| `--input-*` tokens | (missing) | Full set | NEW |
| `--icon-*` tokens | (missing) | Full set | NEW |
| `--transition-input` | (missing) | Added | NEW |

All other Session 2 tokens are confirmed unchanged.

---

## 15. What Session 22 Resolves

- The Session 2 baseline is upgraded to the full Bricks visual language: the builder's 16-step gray scale replaces Session 2's approximation wherever precision is needed.
- The surface hierarchy now has 6 levels (void/deep/base/raised/elevated/top) instead of 4, with each level mapped precisely to a builder gray value.
- `--state-selected-bg` is now the exact `--builder-bg-accent` value (`#58470e`) rather than a transparency calculation — this makes "selected item" backgrounds consistent with how the Bricks builder itself shows active/selected states.
- The scrollbar system is defined — thin (4px), dark track, dark thumb, hover brightens.
- The input system is fully defined with height, padding, and state tokens.
- The icon size system provides named sizes from 12px to 40px.
- The governance glyph reference is formalized — all special characters used throughout sessions 3–21 are listed with their semantic meanings.
- The new visual components introduced in sessions 3–21 (left-border accents, record type badges, key indicator chips, schema-pending `*` notation, compact boundary markers, non-canonical notices) are formalized as reusable patterns.
- The complete final token reference in §13 is a single implementation handoff document — an engineer can copy this directly into a CSS custom property block and have the full visual system.

---

## 16. What Session 22 Does Not Resolve

- **Component-level motion and state transitions** — how each component animates between its states is Session 23 (Component Behavior Patterns). Session 22 provides the timing and easing tokens; Session 23 specifies which tokens apply where.
- **Dark/light mode toggle** — the builder ships with `[data-builder-mode=light]` overrides. The V Ecosystem desktop is dark-first. A light mode is not designed here and is not needed for the MVP. If a future light mode is required, the builder's light-mode values provide the starting point.
- **Right-to-left (RTL) support** — the builder has `-rtl.min.css` variants. Not addressed here.
- **Tauri window chrome styling** — the OS-level window frame, titlebar buttons, and window drag region are Tauri/OS concerns, not CSS tokens.
- **Color accessibility audit** — a formal WCAG contrast audit against these values is an engineering task, not a UX design task. The values are derived from Bricks which was designed for production use; WCAG compliance should be verified by the implementation engineer using the contrast ratios of the specific text/background pairings in each surface.
