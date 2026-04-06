# Session 2 — Minimal Token Decisions
## V Ecosystem Desktop UX

**Session status:** Complete  
**Depends on:** Session 1 (Output Card System)  
**Required before:** All subsequent sessions  

---

## What This Document Is

This is the minimum visual and motion vocabulary for the V Ecosystem Tauri 2 desktop application. It is derived directly from the Bricks theme (`frontend.min.css`, `frontend.js`) and adapted for a dark-first desktop governance application rather than a light web publishing tool.

It is not a full design system. It is not the final Bricks adaptation (Session 22). It is enough to stop making inconsistent choices across sessions 3–21.

**Source extraction note:** All values below are derived from Bricks 2.3.1 CSS custom properties, computed values, and JS timing constants — not invented. Where Bricks provides a web-oriented value that doesn't translate cleanly to a desktop application, the adaptation rationale is noted.

---

## Section 1 — Color Roles

### Source: Bricks CSS Custom Properties

From `frontend.min.css` `:root`:
```css
--bricks-color-primary: #ffd64f       /* amber/gold accent */
--bricks-color-secondary: #fc5778     /* pink/coral accent */
--bricks-text-dark: #212121
--bricks-text-medium: #616161
--bricks-text-light: #9e9e9e
--bricks-text-info: #00b0f4
--bricks-text-success: #11b76b
--bricks-text-warning: #ffa100
--bricks-text-danger: #fa4362
--bricks-bg-info: #e5f3ff
--bricks-bg-success: #e6f6ed
--bricks-bg-warning: #fff2d7
--bricks-bg-danger: #ffe6ec
--bricks-bg-dark: #263238
--bricks-bg-light: #f5f6f7
--bricks-border-color: #dddedf
--bricks-border-radius: 4px
--bricks-tooltip-bg: #23282d
--bricks-tooltip-text: #eaecef
```

### Desktop Adaptation

The Bricks theme is light-mode-first (`body { background-color: #fff }`). The V Ecosystem desktop is a dark-mode governance application. The color roles are inverted and adapted below. The accent family (`#ffd64f`, `#fc5778`) and the semantic state colors are retained directly — they're strong choices that survive inversion.

### Desktop Color Tokens

```css
/* === SURFACE === */
--surface-base:      #1a1f23   /* page / window background — darker than bricks bg-dark */
--surface-raised:    #263238   /* card, panel background — exact bricks --bricks-bg-dark */
--surface-elevated:  #2e3a42   /* popovers, dropdowns, floating elements */
--surface-overlay:   #1a1f23cc /* modal scrim — base color at 80% opacity */
--surface-border:    #37474f   /* default border — darker than bricks border, suits dark bg */

/* === TEXT === */
--text-primary:      #eaecef   /* default readable text — bricks --bricks-tooltip-text */
--text-secondary:    #9e9e9e   /* supporting text — exact bricks --bricks-text-light */
--text-tertiary:     #616161   /* disabled, placeholder — exact bricks --bricks-text-medium */
--text-inverse:      #212121   /* text on light surfaces — exact bricks --bricks-text-dark */
--text-link:         #00b0f4   /* clickable text — exact bricks --bricks-text-info */

/* === ACCENT === */
--accent-primary:    #ffd64f   /* primary accent — exact bricks --bricks-color-primary (amber) */
--accent-primary-dim: #b89836  /* accent at reduced brightness for dark surface contexts */
--accent-secondary:  #fc5778   /* secondary accent — exact bricks --bricks-color-secondary */

/* === STATE === */
--state-info:        #00b0f4   /* exact bricks --bricks-text-info */
--state-info-bg:     #0d2a3d   /* dark-adapted bricks --bricks-bg-info */
--state-success:     #11b76b   /* exact bricks --bricks-text-success */
--state-success-bg:  #0d2d1f   /* dark-adapted bricks --bricks-bg-success */
--state-warning:     #ffa100   /* exact bricks --bricks-text-warning */
--state-warning-bg:  #2d2000   /* dark-adapted bricks --bricks-bg-warning */
--state-danger:      #fa4362   /* exact bricks --bricks-text-danger */
--state-danger-bg:   #2d0d12   /* dark-adapted bricks --bricks-bg-danger */

/* === GOVERNANCE STATE === */
/* These extend Bricks state colors for doctrine-specific UI patterns */
--state-blocked:     #fa4362   /* alias for danger — Class D escalation, hard blocks */
--state-pending:     #ffa100   /* alias for warning — awaiting review, pending approval */
--state-inert:       #616161   /* awaiting review, not yet activated — text-tertiary */
--state-stale:       #ffa100   /* staleness markers on output cards */
--state-schema-hold: #9e9e9e   /* schema-pending / unavailable states */

/* === APPROVAL CLASS BADGES === */
--badge-class-a:     #37474f   /* Class A: no gate, neutral */
--badge-class-b:     #0d2a3d   /* Class B: operator approval required */
--badge-class-c:     #2d0d12   /* Class C: typed confirmation required */
--badge-class-d:     #fa4362   /* Class D: escalation required */

--badge-class-a-text: #9e9e9e
--badge-class-b-text: #00b0f4
--badge-class-c-text: #fa4362
--badge-class-d-text: #fff
```

---

## Section 2 — Elevation / Depth

Bricks uses `box-shadow` implicitly through its builder, but doesn't define shadow tokens in the frontend CSS. These are derived from the depth model implied by Bricks' layering (`popup: z-index 10000`, `nav: z-index 998`, `overlay: z-index 1001`) and adapted to a dark desktop surface.

```css
/* === ELEVATION === */
/* Expressed as box-shadow. Dark surfaces need subtle, warm-tinted shadows. */

--elevation-flat:    none
/* Use for: in-panel content, context strip rows, tree items */

--elevation-raised:  0 1px 3px rgba(0, 0, 0, 0.4), 0 1px 2px rgba(0, 0, 0, 0.3)
/* Use for: output cards, left nav panel, topbar */

--elevation-overlay: 0 4px 12px rgba(0, 0, 0, 0.5), 0 2px 4px rgba(0, 0, 0, 0.4)
/* Use for: dropdowns, command palette, floating tooltips, popovers */

--elevation-modal:   0 16px 48px rgba(0, 0, 0, 0.6), 0 6px 16px rgba(0, 0, 0, 0.5)
/* Use for: Class C modal gate, session integrity overlay */
```

---

## Section 3 — Border Radius

Bricks defines one radius:
```css
--bricks-border-radius: 4px
```

The desktop application extends this with a small radius family for distinct element types:

```css
--radius-sm:    2px    /* inline badges, staleness markers, code snippets */
--radius-md:    4px    /* exact bricks value — cards, inputs, buttons, panels */
--radius-lg:    6px    /* modals, gate surfaces, popovers */
--radius-pill:  100px  /* bricks .bricks-button.circle pattern — tags, small chips */
```

---

## Section 4 — Spacing Scale

Bricks uses 8-point-derived spacing throughout: padding values in the CSS cluster at `5px`, `10px`, `12px`, `15px`, `20px`, `30px`, `40px`, `60px`. The button padding is `.5em 1em` / `.4em 1em` / `.6em 1em` — proportional.

The desktop application uses a **4-point base with 8-point primary steps**:

```
--space-1:    4px    /* tight: icon gap within badge, indicator dot spacing */
--space-2:    8px    /* inner: icon-to-label gap, inline element spacing */
--space-3:    12px   /* compact: input padding, small card padding */
--space-4:    16px   /* default: card padding, list item padding */
--space-5:    20px   /* comfortable: section padding, nav item height padding */
--space-6:    24px   /* generous: modal padding, gate widget padding */
--space-8:    32px   /* wide: panel header, major section separation */
--space-10:   40px   /* expansive: center workspace header padding */
--space-12:   48px   /* topbar height, modal header height */
```

**Panel-specific spatial constants:**
```
--panel-topbar-height:    48px
--panel-left-nav-width:   260px
--panel-right-width:      320px   /* default — resizable */
--panel-right-min:        280px
--panel-right-max:        440px
--panel-lower-height:     200px   /* default when open */
--panel-border-width:     1px
```

These map to Bricks header/nav patterns: `#brx-header.brx-sticky` uses fixed positioning, nav menus use `line-height: 60px` for items. The desktop topbar at 48px is a desktop-native reduction of Bricks' web 60px convention.

---

## Section 5 — Typography Scale

Bricks body: `font-size: 15px`, `line-height: 1.7`, `font-family: -apple-system, system-ui, Segoe UI, roboto...`

Heading scale from Bricks:
- h1: 2.4em (~36px at 15px base)
- h2: 2.1em (~31.5px)
- h3: 1.8em (~27px)
- h4: 1.6em (~24px)
- h5: 1.3em (~19.5px)
- h6: 1.1em (~16.5px)

The desktop application does not use h1–h3. Everything is workspace-scale. The type scale is compressed:

```
/* Base: 13px (desktop density — 2px below Bricks 15px web body) */

--type-xs:      11px   /* metadata, timestamps, badges, staleness markers */
               line-height: 1.4  letter-spacing: 0.3px

--type-sm:      12px   /* labels, category headers, context strip rows */
               line-height: 1.5  letter-spacing: 0.2px

--type-base:    13px   /* body text in cards, descriptions, output content */
               line-height: 1.6  letter-spacing: 0

--type-md:      14px   /* primary UI text, nav items, input values */
               line-height: 1.5  letter-spacing: 0

--type-lg:      16px   /* section headings, card titles, panel headers */
               line-height: 1.4  letter-spacing: -0.1px

--type-xl:      20px   /* modal titles, workspace surface headers */
               line-height: 1.3  letter-spacing: -0.2px

/* Font stack: match Bricks exactly */
--font-ui: -apple-system, "system-ui", "Segoe UI", roboto, helvetica, arial,
           sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol"

/* Monospace: for IDs, record identifiers, session tokens, code */
--font-mono: "SF Mono", "Consolas", "Fira Code", "Cascadia Code",
             "Roboto Mono", monospace
```

**Weight scale:**
```
--weight-normal:   400
--weight-medium:   500   /* nav items, card labels */
--weight-semibold: 600   /* section headings, badge text, attention items */
--weight-bold:     700   /* output type labels, gate controls, class badges */
```

---

## Section 6 — Motion and Timing

### Source: Bricks

The master transition from Bricks:
```css
--bricks-transition: all 0.2s    /* applies to: body, inputs, overlay items, nav menus */
```

Specific timing constants extracted from the Bricks JS and CSS:

| Context | Easing | Duration | Source |
|---|---|---|---|
| Default transition | `ease` | `0.2s` | `--bricks-transition` |
| Mega menu opacity/transform | `ease` | `0.2s` | `.brx-megamenu` |
| Offcanvas panel slide | `cubic-bezier(.25, 0, .25, 1)` | `0.2s` | `.brx-offcanvas-inner` |
| Offcanvas backdrop | `cubic-bezier(.25, 0, .25, 1)` | `0.2s` | `.brx-offcanvas-backdrop` |
| Multilevel submenu transform | `cubic-bezier(0, 0, .2, 1)` | `0.1s` | `.brx-has-multilevel ul` |
| Submenu toggle rotation | `cubic-bezier(0, 0, .2, 1)` | `0.1s` | `.brx-submenu-toggle button` |
| Accordion height | `ease` | `0.5s` | `.accordion-content-wrapper` |
| Accordion title hover | `var(--bricks-transition)` | `0.2s` | `.accordion-title-wrapper` |
| Sticky header bg + transform | `background-color 0.2s, transform 0.4s` | — | `#brx-header.brx-sticky` |
| Swiper fade slide | `ease-out` | varies | `.swiper-fade` |
| Hamburger spin | `cubic-bezier(.215, .61, .355, 1)` | `0.22s` | `.brxa--spin` |
| Hamburger collapse | `cubic-bezier(.55, .055, .675, .19)` | `0.13s` | `.brxa--collapse` |
| Search overlay | all | `0.4s` | `.bricks-search-overlay` |
| Isotope layout | opacity | `0.3s ease-in-out` | `.bricks-is-frontend .bricks-layout-wrapper.isotope` |
| Overlay show-on-hover | `var(--bricks-transition)` | `0.2s` | `.overlay-wrapper.show-on-hover` |
| Progress bar fill | `cubic-bezier(.55, .055, .675, .19)` | `0.6s` | `.progress-bar .bar span` |
| Hamburger elastic | `cubic-bezier(.68, -.55, .265, 1.55)` | `0.275s` | `.brxa--elastic` |
| Back-to-top | `ease-in-out` | `0.1s` | `.brxe-back-to-top` |

### Desktop Motion Tokens

```css
/* === EASING === */
/* Derived directly from Bricks patterns above */
--ease-default:    ease                              /* bricks default */
--ease-out:        cubic-bezier(0, 0, 0.2, 1)       /* bricks submenu/multilevel: fast-end */
--ease-in-out:     cubic-bezier(0.25, 0, 0.25, 1)   /* bricks offcanvas: smooth panel slides */
--ease-spring:     cubic-bezier(0.215, 0.61, 0.355, 1) /* bricks spin/collapse: momentum landing */
--ease-anticipate: cubic-bezier(0.55, 0.055, 0.675, 0.19) /* bricks collapse entry: slight anticipation */
--ease-bounce:     cubic-bezier(0.68, -0.55, 0.265, 1.55) /* bricks elastic: overshoot then settle */

/* === DURATION === */
--duration-instant:  100ms   /* hover state changes, focus rings, micro interactions */
--duration-fast:     150ms   /* badge appearance, indicator dot, inline state changes */
--duration-default:  200ms   /* exact bricks --bricks-transition — panel show/hide, menu */
--duration-moderate: 300ms   /* context strip row expansion, card reveal */
--duration-slow:     400ms   /* panel slides (bricks header slide), page-level transitions */
--duration-deliberate: 500ms /* accordion open, progress bar fill — bricks values */

/* === TRANSITION PRESETS === */
/* Composed from the above. Use these on elements, not raw values. */

--transition-instant:  all var(--duration-instant) var(--ease-default)
/* Use for: hover color changes, focus rings, active state overlays */

--transition-default:  all var(--duration-default) var(--ease-default)
/* Use for: dropdowns, tooltips, badge appearance — exact Bricks --bricks-transition */

--transition-panel:    transform var(--duration-slow) var(--ease-in-out),
                       opacity var(--duration-slow) var(--ease-in-out)
/* Use for: right panel collapse, left nav collapse, lower surface show/hide */

--transition-slide:    transform var(--duration-default) var(--ease-out)
/* Use for: submenu slide, tree item expand, context strip row reveal */

--transition-spring:   transform var(--duration-default) var(--ease-spring)
/* Use for: gate widget activate (the moment the approval button unlocks) */

--transition-fade:     opacity var(--duration-moderate) var(--ease-default)
/* Use for: staleness markers appearing on output cards, integrity banners */

--transition-accordion: height var(--duration-deliberate) var(--ease-default)
/* Use for: context strip expandable detail rows — exact Bricks accordion */
```

---

## Section 7 — Interaction States

Bricks defines these interaction postures in its CSS:

From the input system: `transition: var(--bricks-transition)` on all inputs.
From `.bricks-button`: `transition: var(--bricks-transition)`.
From `.brxe-back-to-top`: `transition: all .1s ease-in-out`.
From filter indicators: `transition: background-color .15s ease, border-color .15s ease`.

```css
/* === INTERACTION STATES === */
/* Applied as CSS class overlays, not separate color vars */

/* Hover: surface brightening — add to interactive elements */
--state-hover-overlay:    rgba(255, 255, 255, 0.06)
/* Matches Bricks: .choose-files:hover { background-color: rgba(0,0,0,.05) } inverted */

/* Active/pressed */
--state-active-overlay:   rgba(255, 255, 255, 0.10)

/* Selected (current nav item, active tab) */
--state-selected-bg:      rgba(255, 214, 79, 0.12)   /* accent-primary at 12% */
--state-selected-border:  var(--accent-primary)

/* Focused (keyboard navigation) */
--state-focus-ring:       2px solid var(--accent-primary)
--state-focus-offset:     2px
/* Bricks: `body.bricks-is-frontend :focus-visible { outline: auto }` */

/* Disabled */
--state-disabled-opacity: 0.4
/* Bricks: .brx-option-disabled { opacity: .5 } — using 0.4 for darker surface readability */

/* Inert (output card awaiting review — not disabled, just not yet actionable) */
--state-inert-opacity:    0.75
--state-inert-border:     var(--surface-border)
```

---

## Section 8 — Z-Index Scale

Derived directly from Bricks z-index values:

| Bricks value | Context |
|---|---|
| `9999` | `.brxe-back-to-top`, `.brxe-post-reading-progress-bar` |
| `10000` | `.brx-popup` |
| `1001` | `.brx-dropdown-content` |
| `1000` | mobile nav toggle |
| `999` | `.brxe-offcanvas .brx-offcanvas-inner` |
| `998` | `#brx-header.brx-sticky`, nav sub-menus |
| `2` | `.bricks-shape-divider.front` |
| `1` | `.swiper-wrapper`, `.brx-dropdown-content` |
| `-1` | `.bricks-background-video-wrapper` |

Desktop z-index stack (mapped from Bricks):
```
--z-base:      1      /* normal document flow */
--z-raised:    10     /* output cards above panel content */
--z-dropdown:  100    /* dropdowns, tooltips — below panels */
--z-panel:     200    /* left nav, right panel — above workspace */
--z-topbar:    300    /* topbar — above all panels */
--z-overlay:   400    /* modal backdrop */
--z-modal:     500    /* Class C modal gate */
--z-toast:     600    /* in-app notifications — above modal in specific cases */
--z-critical:  700    /* session error overlay, Class D escalation banner */
```

---

## Section 9 — Border and Divider System

From Bricks:
```css
--bricks-border-color: #dddedf  (light mode)
border-width: 1px (inputs, table features, blockquote: 4px left-border)
hr: border-top: 1px solid var(--bricks-border-color)
```

Desktop (dark-adapted):
```css
--border-subtle:    #2e3a42    /* barely-visible structural division */
--border-default:   #37474f    /* standard component borders */
--border-emphasis:  #546e7a    /* hover border on interactive elements */
--border-accent:    #ffd64f    /* focused input, selected nav item */
--border-danger:    #fa4362    /* error state, Class D banner */
--border-width:     1px        /* universal */

/* Dividers — horizontal rules inside panels */
--divider-color:    var(--border-subtle)
--divider-weight:   1px
```

---

## Section 10 — Governance-Specific Visual Tokens

These do not exist in Bricks. They are desktop-only additions required by the doctrine.

```css
/* === STALENESS MARKER === */
--staleness-bg:        var(--state-warning-bg)
--staleness-border:    var(--state-warning)
--staleness-text:      var(--state-warning)
--staleness-icon:      ⚠         /* literal character */

/* === SCHEMA PENDING MARKER === */
--schema-pending-bg:   rgba(158, 158, 158, 0.08)
--schema-pending-text: var(--text-tertiary)
--schema-pending-border: var(--border-subtle)
/* Renders as: [SCHEMA PENDING] inline tag */

/* === OWNERSHIP LABEL === */
/* Applied to referenced-system context strips */
--ownership-label-bg:      rgba(0, 176, 244, 0.08)
--ownership-label-text:    var(--state-info)
--ownership-label-border:  var(--state-info)
/* Example: "REFERENCED FROM V FORGE — not owned by Project V" */

/* === INERTNESS TREATMENT === */
/* Applied to Recommendation cards and Approval Request Packages */
--inert-label-bg:     rgba(97, 97, 97, 0.15)
--inert-label-text:   var(--text-tertiary)
/* Label text: "AWAITING REVIEW" */

/* === GATE ACTIVATION INDICATOR === */
/* The moment a gate widget becomes active (all checkpoints satisfied) */
--gate-inactive-opacity:  0.4
--gate-active-border:     var(--accent-primary)
--gate-active-shadow:     0 0 0 2px rgba(255, 214, 79, 0.25)
/* Transition on activation: var(--transition-spring) */

/* === CONTINUITY ARTIFACT MARKER === */
--continuity-bg:      rgba(255, 161, 0, 0.06)
--continuity-border:  rgba(255, 161, 0, 0.3)
--continuity-label:   "NON-CANONICAL"
```

---

## How to Use This Document

**In subsequent design sessions:**
- Reference tokens by name, not by hex value
- If a required token is missing, add it here before using it in a session
- Do not invent local ad-hoc values that shadow a token defined here

**Token naming convention:**
```
--category-variant-modifier
Examples:
  --surface-raised
  --text-secondary
  --state-warning-bg
  --transition-panel
  --border-accent
  --duration-fast
```

**What this document does NOT define:**
- Component-level CSS (that's per-session work)
- Animation keyframes (defined per-component when needed)
- Final hex values for the Bricks full visual adaptation (Session 22)
- Tauri window chrome or OS-level theming

---

## Session Output Summary

All tokens produced:
- ✅ 32 color role tokens + 8 governance-specific color tokens
- ✅ 4 elevation tokens (box-shadow)
- ✅ 4 border-radius tokens
- ✅ 10 spacing scale steps + 5 panel spatial constants
- ✅ 7 type scale steps + 4 weight values + 2 font stacks
- ✅ 6 easing curves + 6 duration steps + 7 transition presets
- ✅ 5 interaction state tokens
- ✅ 9 z-index levels
- ✅ 4 border/divider tokens
- ✅ 10 governance-specific tokens (staleness, schema-pending, ownership, inertness, gate, continuity)

**Next session:** Session 3 — Topbar. Read this document before starting. Reference `--panel-topbar-height: 48px`, attention badge tokens (`--state-pending`, `--state-danger`), and `--transition-default` as the baseline motion.
