# V Ecosystem UX Direction

**Status:** Active reference  
**Scope:** Tauri + React desktop app — local-first architecture  
**Inspiration:** Bricks Builder feel, density, and layout logic — not their code  

---

## 1. The Decision

Move away from the VSCode extension model toward a standalone desktop application.

**Why not stay in VSCode:**
- VSCode sidebar constraints force the wrong navigation model for this ecosystem
- Three-system content (Project V / VEDA / V Forge) doesn't fit cleanly into VSCode's tree view paradigm
- Approval gates, return trigger queues, and cross-system context panels need layout control VSCode doesn't allow
- The ecosystem is planning and content operations work — not code editing — so a code editor is the wrong host

**Why Tauri specifically:**
- Dramatically smaller bundle than Electron (~50MB vs ~300MB)
- Less memory, faster startup — important for an operator using this 8 hours a day
- Native system process calls for MCP integration
- Same React/TypeScript frontend, just a different shell
- Tauri 2 has a proper multi-window model and cleaner IPC for event-driven state sync

---

## 2. The Layout Model

Inspired by Bricks Builder's three-column editor shell. Direct translation:

```
┌─────────────────────────────────────────────────────────┐
│  TOPBAR: [◈ Project Name ▾]  [PV] [VEDA] [VF]  [●●●]  │
├──────────┬──────────────────────────┬───────────────────┤
│          │                          │                   │
│   LEFT   │        CENTER            │      RIGHT        │
│  260px   │       flex-grow          │      300px        │
│          │                          │                   │
│  Nav     │   Workspace / Detail     │   LLM + Actions   │
│  Tree    │                          │   Context Strip   │
│          │                          │                   │
└──────────┴──────────────────────────┴───────────────────┘
```

**Left panel:** Navigation tree. System-aware content. Switches when the operator changes system tab. Always present.

**Center panel:** The active workspace. Detail view for whatever is selected in the left tree. Changes completely based on selection and active system. Shows real data, not skeletons.

**Right panel:** Persistent context strip + LLM interaction + action panel. Reactive to selection. LLM output goes in the center as typed cards; the right panel stays as a persistent context + action surface.

**Topbar:** Project selector (left third), system tabs PV / VEDA / VF (center), session status + settings (right third). Switching systems changes left tree content and center workspace context. Shell stays constant.

Both left and right panels are resizable with a drag handle. Center takes the remainder.

---

## 3. What Bricks Actually Does (The Source of the Feel)

After reading the actual Bricks source files, here is exactly what produces the smoothness:

**No animation library.** Zero GSAP, zero Framer Motion, zero Anime.js. The entire builder UI runs on pure CSS transitions and one custom JS pattern.

### CSS Transitions

Panels and sidebars:
```css
transition: width .1s ease-in-out;
```

Hover states and interactive elements:
```css
transition: all .05s ease-in-out;
```

Control groups and dropdowns:
```css
transition: all .1s ease-in-out;
```

Notifications:
```css
transition: opacity .1s linear;
```

The `.minimize` class on a panel sets `width: 0` and the CSS transition handles everything. That's the panel slide.

### The Accordion JS Pattern (slideUp / slideDown)

The only place Bricks writes custom JS for animation is tree/accordion expand and collapse. The technique:

1. Measure the real pixel height of the element
2. Set `height: 0` and `overflow: hidden`
3. Call `target.offsetHeight` — this forces a layout reflow, making the browser recalculate before the next paint. This is the key trick that makes the animation actually work
4. Apply `transition: height 200ms ease-in-out` and set height to the measured pixel value
5. After 200ms, remove all inline styles and let CSS take over again

The duration is configurable via a `data-transition` attribute defaulting to `200`.

**The critical insight:** The `target.offsetHeight` read on a single line — with no assignment — is intentional. It forces a synchronous layout before the transition begins. Without it the browser batches the style changes and the animation doesn't happen.

### Timing Hierarchy

This is the single most important decision for replicating the feel:

| Element | Duration | Why |
|---|---|---|
| Hover states, selections | 50ms | Reads as instant but still smooth |
| Panel width changes | 100ms | Fast enough to feel responsive |
| Height collapses (tree nodes) | 200ms | Needs time to feel natural |
| Tooltip open | 0ms delay | Appears immediately |
| Tooltip close | 150ms delay | Prevents flash on accidental hover |

Most UIs default to 300ms everywhere and feel heavy. 50ms for constant interactions is what makes Bricks feel like it's responding to your intent in real time.

---

## 4. Bricks Source File Map

Files in `C:\dev\v-ecosystem-ux\bricks\` that are worth studying:

### The CSS — Design Tokens and Panel Layout

**`assets/css/builder.min.css`**  
The entire builder UI stylesheet. Contains:
- All CSS custom properties (the full `--builder-*` token system)
- Panel structure and sizing
- All transition definitions
- The minimize/expand panel patterns
- Hover, active, and focus states
- Input, button, and control styling
- Z-index layering
- The `.is-resizing` class that suppresses transitions during drag

Key sections to study:
```
--builder-gray-0 through --builder-gray-f    ← the full gray scale
--builder-bg, --builder-bg-2/3/4             ← surface hierarchy
--builder-color-accent                        ← the gold accent (#ffd54d dark / #f72684 light)
--builder-color-success/danger/info/muted     ← status colors
#bricks-panel                                 ← left panel structure
transition: width .1s ease-in-out            ← panel slide
transition: all .05s ease-in-out             ← hover states
.bricks-panel .button                         ← button pattern
```

**`assets/css/frontend.min.css`**  
Frontend (public-facing) styles. Less relevant for the builder shell but useful for seeing how Bricks handles components in isolation.

**`assets/css/elements/`**  
Individual element stylesheets. Good reference for how they scope component styles without CSS Modules or CSS-in-JS — just well-namespaced class names.

---

### The JS — Animation Patterns

**`assets/js/frontend.js`** (394KB, unminified — study this one)  
The main frontend behavior file. Key patterns to study:

- **Lines 4804–4920:** The complete `slideUp` / `slideDown` / `slideToggle` accordion implementation. This is the exact pattern to port to a React hook. The `target.offsetHeight` reflow trick is on line 4808 (slideUp) and 4862 (slideDown).

- **Lines 1721–1765:** The `animate.css` element animation pattern — how Bricks adds/removes animation classes and listens for `animationend` to clean up. The same pattern applies to LLM output card entrances.

- **Lines 1803–2091:** The parallax/motion implementation using `requestAnimationFrame` with a shared RAF scheduler. Shows how Bricks handles ongoing animation without creating per-element RAF loops.

- **Lines 341–360:** `requestAnimationFrame` usage for batching layout recalculations — relevant for the masonry/tree layout performance pattern.

**`assets/js/bricks.min.js`** (180KB)  
The compiled builder JS. Minified, but searchable for patterns. The panel resize drag-handle behavior is in here. If you want to understand how they handle the resizable panel drag without a library, search for `is-resizing`.

**`assets/js/admin.js`** (100KB, unminified)  
Admin panel behavior. Less relevant but shows their event system and how they manage UI state without a framework.

---

### Libraries They Do Use

**`assets/js/libs/choices.min.js`**  
Their custom select/dropdown component. Worth studying for accessible dropdown behavior patterns. They use this for all their styled selects in the builder.

**`assets/js/libs/flatpickr.min.js`**  
Date picker. Not relevant for V Ecosystem.

**`assets/js/libs/swiper.min.js`**, **`splide.min.js`**  
Carousel libraries for frontend elements. Not relevant.

**The key finding:** None of the builder UI smoothness comes from any library in `libs/`. The libs are for frontend page elements (carousels, galleries, etc.). The builder shell itself is pure CSS + vanilla JS.

---

## 5. Your Own Design System

Inspired by Bricks but entirely original. Different palette, different font, different accent direction.

### Color Tokens

```css
:root {
  /* Backgrounds — cool dark with slight blue undertone */
  --v-bg-base:      #0f1117;
  --v-bg-panel:     #151820;
  --v-bg-elevated:  #1c2028;
  --v-bg-hover:     #242834;
  --v-bg-active:    #2a3040;

  /* Borders */
  --v-border-subtle:  rgba(255,255,255,0.04);
  --v-border-default: rgba(255,255,255,0.08);
  --v-border-strong:  rgba(255,255,255,0.14);

  /* Text */
  --v-text-primary:   #e8edf2;
  --v-text-secondary: #8fa0b0;
  --v-text-muted:     #556070;
  --v-text-disabled:  #3a4455;

  /* Accent — electric blue, not Bricks' gold */
  --v-accent:      #4f8ef7;
  --v-accent-dim:  rgba(79,142,247,0.15);

  /* System identity — each system has its own color */
  --v-pv-color:    #7c9dff;   /* Project V — cool blue */
  --v-pv-dim:      rgba(124,157,255,0.12);
  --v-veda-color:  #52d9a4;   /* VEDA — teal green */
  --v-veda-dim:    rgba(82,217,164,0.12);
  --v-forge-color: #f0914d;   /* V Forge — warm amber */
  --v-forge-dim:   rgba(240,145,77,0.12);

  /* Status */
  --v-success:     #3dbe8a;
  --v-success-bg:  #0c2a1e;
  --v-warning:     #e8a840;
  --v-warning-bg:  #2a1e08;
  --v-danger:      #e05555;
  --v-danger-bg:   #2a0c0c;
  --v-info:        #4ab8e8;
  --v-info-bg:     #0a2030;

  /* Spacing */
  --v-space-1:  4px;
  --v-space-2:  8px;
  --v-space-3:  12px;
  --v-space-4:  16px;
  --v-space-5:  24px;
  --v-space-6:  32px;

  /* Shape */
  --v-radius-sm:  3px;
  --v-radius-md:  5px;
  --v-radius-lg:  8px;

  /* Layout */
  --v-topbar-h:     44px;
  --v-panel-left:   260px;
  --v-panel-right:  300px;
  --v-item-h:       28px;
  --v-input-h:      30px;

  /* Typography */
  --v-font:      'Geist Sans', system-ui, sans-serif;
  --v-mono:      'Geist Mono', monospace;
  --v-text-xs:   10px;
  --v-text-sm:   11px;
  --v-text-base: 12px;
  --v-text-md:   13px;
  --v-text-lg:   15px;
  --v-text-xl:   18px;

  /* Timing — exact Bricks approach */
  --v-fast:  50ms;
  --v-base:  100ms;
  --v-slow:  200ms;
  --v-ease:  ease-in-out;
}

/* System-aware cascade — set data-system on body from React */
body[data-system="project-v"] {
  --v-system-color: var(--v-pv-color);
  --v-system-dim:   var(--v-pv-dim);
}
body[data-system="veda"] {
  --v-system-color: var(--v-veda-color);
  --v-system-dim:   var(--v-veda-dim);
}
body[data-system="v-forge"] {
  --v-system-color: var(--v-forge-color);
  --v-system-dim:   var(--v-forge-dim);
}
```

When the operator switches systems, set `document.body.dataset.system = 'veda'` and the entire UI recolors through CSS cascade. No JavaScript loops, no re-renders for color changes.

### Typography

**Font:** Geist Sans (Vercel, free). Modern, precise, excellent for dense UI. Different from Bricks' Inter/Lato.  
**Mono:** Geist Mono for keys, code values, record identifiers.

### Status Shapes (Icon-first, no icon library needed)

```
●  active         solid fill, system accent color
◐  in-progress    half fill, accent color
○  proposed       outline only, muted
⊘  blocked        filled, danger color
✓  ready          filled, success color
→  handed-off     arrow, muted
⚑  return req.    flag, warning color
```

These are Unicode characters used as status indicators. No SVG library needed for status badges.

---

## 6. Animation System (Pure CSS)

All CSS transitions in one file (`animations.css`). Easy to audit and adjust globally.

### Prevent transitions on mount

```css
body:not([data-mounted]) * {
  transition: none !important;
}
```

Add `data-mounted` to body after first React render. Prevents flash of animated transitions on initial paint.

### Core transitions

```css
/* Panel resize */
.panel-left,
.panel-right {
  transition: width var(--v-base) var(--v-ease);
}

/* Suppress during drag */
.panel-left.is-resizing,
.panel-right.is-resizing {
  transition: none;
}

/* Tree items */
.tree-item {
  transition: background-color var(--v-fast) var(--v-ease);
}

/* All interactive elements */
button,
.clickable {
  transition:
    background-color var(--v-fast) var(--v-ease),
    color            var(--v-fast) var(--v-ease),
    opacity          var(--v-fast) var(--v-ease);
}

/* Dropdowns */
.dropdown[data-state="closed"] {
  opacity: 0;
  transform: translateY(-4px);
  pointer-events: none;
  transition:
    opacity   var(--v-fast) var(--v-ease),
    transform var(--v-fast) var(--v-ease);
}
.dropdown[data-state="open"] {
  opacity: 1;
  transform: translateY(0);
}

/* LLM output card entrance */
@keyframes v-card-in {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: translateY(0); }
}
.llm-card {
  animation: v-card-in var(--v-slow) var(--v-ease);
}

/* Urgent badge pulse */
@keyframes v-pulse {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0.5; }
}
.badge-urgent {
  animation: v-pulse 2s ease-in-out infinite;
}
```

### The Height Collapse Hook (the one JS animation needed)

CSS cannot animate `height: auto` to `height: 0`. This React hook replicates the exact Bricks accordion pattern:

```tsx
function useSlide(isOpen: boolean, duration = 200) {
  const ref = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const el = ref.current
    if (!el) return

    if (isOpen) {
      el.style.overflow = 'hidden'
      el.style.height = '0'
      el.offsetHeight // force reflow — this is the key
      el.style.transition = `height ${duration}ms ease-in-out`
      el.style.height = `${el.scrollHeight}px`
      const t = setTimeout(() => {
        el.style.removeProperty('height')
        el.style.removeProperty('overflow')
        el.style.removeProperty('transition')
      }, duration)
      return () => clearTimeout(t)
    } else {
      el.style.height = `${el.offsetHeight}px`
      el.offsetHeight // force reflow
      el.style.transition = `height ${duration}ms ease-in-out`
      el.style.overflow = 'hidden'
      el.style.height = '0'
    }
  }, [isOpen, duration])

  return ref
}
```

Use this for tree node expand/collapse, detail panel sections, right panel zones. The `el.offsetHeight` read without assignment is intentional — it forces the browser to flush the style queue before the transition begins.

---

## 7. CSS Architecture

Pure CSS. No preprocessor. No CSS-in-JS. No Tailwind.

### Why Pure CSS

- Tauri targets one WebView engine (WebView2 on Windows — Chromium-based). No browser compatibility chaos.
- CSS custom properties cascade through the entire component tree. The `data-system` body attribute trick works because of this.
- Bricks proved it. Their entire builder UI runs on pure CSS + one JS animation pattern.
- Modern CSS nesting is native in the WebView2 engine. No Sass needed.

### File Structure

```
src/
  styles/
    tokens.css        ← all custom properties — import first
    reset.css         ← minimal reset, box-sizing
    typography.css    ← font loading, base text rules
    layout.css        ← shell, panel structure, grid
    animations.css    ← all transitions and keyframes
  components/
    shell/
      Topbar.tsx
      Topbar.css      ← co-located with component
    left-panel/
      TreeItem.tsx
      TreeItem.css
    center/
      DetailPanel.tsx
      DetailPanel.css
    right-panel/
      ContextStrip.tsx
      ContextStrip.css
      LLMPanel.tsx
      LLMPanel.css
```

Global styles imported once in `main.tsx`. Component CSS co-located and imported directly. Vite handles it natively.

### Component CSS Convention

Namespaced root class, no hashed modules needed in a controlled Tauri environment:

```css
/* TreeItem.css */
.tree-item { ... }
.tree-item:hover { ... }
.tree-item[data-selected="true"] { ... }
.tree-item__icon { ... }
.tree-item__label { ... }
.tree-item__badge { ... }
```

### What You Don't Need

| Tool | Why not |
|---|---|
| CSS Modules | Build step + hashed names, no benefit in a single-window Tauri app |
| Tailwind | Fights the custom property cascade, verbose JSX, harder to read design system |
| Styled Components / Emotion | Runtime cost, complicates the `data-system` cascade |
| Sass / Less | Modern CSS nesting is native in WebView2 |

---

## 8. Tech Choices

### Core Stack

| Layer | Choice | Reason |
|---|---|---|
| Shell | Tauri 2 | Multi-window model, secure IPC, smaller bundle, native process calls for MCP |
| UI Framework | React 19 + TypeScript | Component tree, not a router framework |
| Bundler | Vite (built into Tauri) | Native CSS import handling |
| State — UI | Zustand | Per-system stores, no boilerplate, no dispatchers |
| State — Server | TanStack Query | Caching, staleness, background refetch, optimistic updates |
| Local storage | SQLite via `tauri-plugin-sql` | Local-first cache layer |
| Styling | Pure CSS + CSS custom properties | Token cascade, no runtime cost |
| Icons | Lucide React | Small, MIT, React-native. Supplement with custom SVGs for status shapes |
| Panels | `react-resizable-panels` | Battle-tested, accessible, exactly the three-column pattern needed |
| Tree | Custom (60–80 lines React) | Every library fights the design. Virtualize with `@tanstack/virtual` for large projects |
| Animations | CSS transitions only | No Framer Motion needed |

### Zustand Store Shape

```
sessionStore      ← active project, system, session token, connection status
projectVStore     ← objectives, initiatives, work items, gaps, handoffs, audit runs
vedaStore         ← keyword targets, SERP data, signal packages, provider status
vForgeStore       ← execution work units, content graph, release state, findings
uiStore           ← selected node, expanded sections, panel widths, mounted state
```

### TanStack Query Usage

Every API call to Project V, VEDA, and V Forge backends goes through TanStack Query. When an approval event fires, invalidate the relevant query keys. The views refetch automatically. No manual state sync.

### Local-First Architecture (Three Layers)

**Layer 1 — PostgreSQL backends**  
Project V, VEDA, V Forge APIs. Canonical truth. The app talks to them over HTTP.

**Layer 2 — SQLite (Tauri-managed)**  
On the operator's machine. Holds: active session state, recently accessed records, cached planning state for offline review, continuity artifacts, draft work not yet committed. Not a replacement for PostgreSQL — a cache and draft layer.

**Layer 3 — Zustand in-memory**  
Live reactive layer the UI reads from. TanStack Query populates it from the APIs. SQLite hydrates it on boot for instant load.

**Boot sequence:**
```
Boot → Load SQLite cache → Paint UI immediately (no loading spinner)
     → Background fetch from API → Update Zustand → Reconcile with SQLite
     → UI reflects fresh data
```

A subtle top-edge shimmer line on the center panel indicates a background refresh. No blocking spinners.

### Tauri-Specific Decisions

**AppHandle events for cross-surface sync** — when an approval event fires, emit a Tauri event that updates all relevant surfaces simultaneously. Don't poll.

**MCP server as a Tauri sidecar** — runs as a sidecar process Tauri manages. Starts with the app, dies with the app, port assigned dynamically. Frontend talks to it via Tauri IPC, not direct HTTP.

**Session token in Tauri secure store** — use `tauri-plugin-store` or OS keychain via `tauri-plugin-stronghold`. Not localStorage, not a flat file. The session token is a security boundary.

**Single window to start** — no multi-window until you know what you'd detach.

---

## 9. The One Dependency Worth Adding

**Radix UI primitives** — behavior-correct, fully unstyled, accessible UI components.

Install only what you need:

```
@radix-ui/react-dropdown-menu
@radix-ui/react-dialog
@radix-ui/react-popover
@radix-ui/react-tooltip
@radix-ui/react-scroll-area
@radix-ui/react-separator
```

These give you keyboard navigation, focus trapping, ARIA attributes, and open/closed state management. You bring all the CSS yourself. They expose `data-state` attributes (`data-state="open"` / `data-state="closed"`) that you target with pure CSS for all visual transitions.

The combination: **Radix for behavior, pure CSS for appearance.** Bricks-level smoothness, zero visual framework lock-in, entirely your own design.

What Radix handles that you don't want to write from scratch:
- Dropdown positioning (collision detection, viewport awareness)
- Focus trap in modals and dialogs (the approval gate modals)
- Keyboard navigation in menus and dropdowns
- ARIA roles and attributes
- Dismissal on Escape and outside click

---

## 10. What Makes It Distinctly Yours

- **Three-color system identity palette** (blue / teal / amber) — the UI shifts color when you switch systems. Immediate contextual orientation. No other tool does this.
- **Geist Sans** — modern and precise, nothing like Bricks' Inter/Lato stack.
- **Status shape system** (●◐○⊘✓→⚑) — Unicode status indicators, icon-first navigation without an icon library for status.
- **Left-border LLM card system** — typed output cards with a colored left border matching output type (recommendation, finding, approval request). Your own pattern.
- **System-color cascade via `data-system` body attribute** — one attribute change recolors the entire UI through CSS inheritance. No JavaScript loops.
- **Bricks smoothness without a single line of Bricks code** — the feel, the timing, the density. Entirely re-derived from first principles.

---

## 11. Build Order

Don't build everything at once. In order:

1. The shell — topbar + three columns + system switcher. Static content. Get the feel right before wiring anything.
2. Left tree for Project V — static first, then connected to API.
3. Center detail panel for a Work Item — most used view, surfaces UX problems immediately.
4. Right context strip — hardcoded content first, then reactive to selection.
5. SQLite local cache layer — add before the LLM panel. Need reliable state before adding LLM complexity.
6. LLM interaction in right panel, typed output cards in center.
7. Class B approval gates — inline in detail panel.
8. Class C approval gates — modal.
9. VEDA and V Forge trees and detail views.

Get Project V working end-to-end first. That's the proof of concept and the highest-value part of the system.

---

## 12. Key UX Improvements Over VSCode Extension Model

Problems with the VSCode model that this architecture solves:

**Cross-system context** — instead of three separate system views requiring navigation between them, a pinned cross-system context row per active work unit shows state across all three systems without switching views.

**Return trigger queue** — a first-class navigation section in the left tree, not a badge count. Each trigger shows: what project, what work unit, what happened, what decision is needed.

**Approval weight scaling** — within Class B approvals, visual weight scales with consequence. Creating a Work Item gets a light inline confirmation. Activating a handoff toward V Forge gets a heavier widget requiring the operator to read the readiness basis before clicking.

**Execution intelligence naming** — called "Performance Gap View" or "Content vs. Signal View" in the UI. Not "Execution Intelligence." The UI calls it what operators actually care about.

**Context strip tiering** — ambient context (current project, session healthy) is peripheral and quiet. Active context (stale decision, return trigger pending, approval needed) is prominent and distinct. Not all context treated as equally visible.
