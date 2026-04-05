# Session 7 — Left Nav — VEDA Tree
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Session 2 (Tokens), Session 3 (Topbar), Session 6 (Left Nav Shell + Project V Tree)
**Required before:** Session 8 (V Forge Tree) — the cross-system absent-affordance vocabulary becomes fully visible by comparing all three trees; VEDA's tree establishes the observatory-record indicator vocabulary that V Forge's execution-record vocabulary will be contrasted against

---

## 1. Files Read

- `session-02-minimal-token-decisions.md` — active token baseline
- `session-06-left-nav-shell-project-v-tree-spec.md` — shell established; section header anatomy, tree item anatomy, status dot system, action affordance rules — all inherited; this session extends with VEDA-specific content and its own indicator vocabulary
- `desktop-surface-architecture.md` — VEDA nav content rules; actions available/not available in VEDA view
- `operator-surface-interfaces.md` — VEDA operator surface: what operators may do, what requires approval (paid data pulls = Class C), what they must not do
- `desktop-state-and-context-model.md` — VEDA evidence freshness and trust posture requirements; ownership label rules
- `veda/veda.md` — VEDA is a pure observatory: observes, records, preserves. Does not plan, propose, or execute.
- `veda/operator-surfaces.md` — what the VEDA operator surface exposes: view state, configure scope, initiate evidence requests, approve paid data pulls, review provider integrations
- `veda/observability-and-signal-role.md` — signal types, evidence preservation rule, signal quality markers (provenance, trust posture, time context, uncertainty)
- `veda/observatory-models.md` — five canonical model categories: Project Partition, Observatory Domain, Signal Package, Provider/Ingest, Event Log
- `interfaces/veda-to-project-v-signal-interface.md` — signal transfer semantics; VEDA does not own planning truth after signal transfer
- `interfaces/veda-to-v-forge-signal-interface.md` — V Forge consumes VEDA signal read-only; VEDA does not own execution intelligence

---

## 2. Session 7 Scope Confirmation

The work plan defines Session 7 as: the VEDA system's left nav content — distinct content rules and absent-affordances from Project V.

This session produces:
- VEDA tree structure: observatory domains, provider sections, signal packages, provider freshness/health posture
- Groupings for ready signal packages vs. in-progress observation
- VEDA-specific item indicator vocabulary (freshness/trust posture, not lifecycle status)
- VEDA-specific absent-affordances
- Paid data pull approval request path in the nav
- Empty and unavailable states
- Synchronization with SESSION-08 vocabulary (so V Forge's tree has a contrast surface)

This session does not:
- Design the V Forge tree (Session 8)
- Design the center workspace VEDA detail views (Session 9)
- Design the approval gate for paid data pulls (Session 10)

---

## 3. VEDA Tree Character

The VEDA tree is fundamentally different from the Project V tree in one key way: **Project V items have lifecycle stages; VEDA items have observatory posture.**

A Project V work item is `proposed → active → blocked → closed`. That is a lifecycle — a progression through governed states over time.

A VEDA observatory record is either current or stale, trusted or uncertain, ready to consume or still being collected. That is posture — a quality judgment about the record's freshness and reliability right now.

This distinction drives the entire visual vocabulary difference between the two trees. Where Project V uses status dots with lifecycle colors, VEDA uses freshness/trust indicators with observatory-posture colors. The section header anatomy, tree item anatomy, and action affordances from Session 6 are all inherited — but the indicator layer is completely different.

---

## 4. VEDA Tree Structure

When the current system is VEDA, the tree content region shows the VEDA observatory tree. Sections in fixed order:

```
SIGNAL PACKAGES       ← ready / pending signal outputs for ecosystem use
OBSERVATORY DOMAINS   ← what VEDA is watching, organized by domain
PROVIDERS             ← external data sources, health and spend posture
EVENT LOG             ← recent observatory state changes (bounded, not a full audit)
```

This order reflects the consumption priority hierarchy: signal packages (what's ready to use) first, then the watching domains (what's being observed), then providers (the infrastructure behind it), then the event log (recent history). The operator most often arrives at the VEDA tree to check what signal is ready — that lands at the top.

---

## 5. Section Specifications

### 5.1 Signal Packages section

Signal packages are VEDA's primary output — bounded, reviewable expressions of observatory-relevant meaning ready for ecosystem consumption by Project V or V Forge.

**Section header:**
```
SIGNAL PACKAGES                          [3 ready]
```

Count badge shows only **ready** packages — those with posture `ready` or `ready_with_caveats`. In-progress or expired packages are not counted here. Badge color:
- `--state-success` if all ready packages are fresh
- `--state-warning` if any ready package is aging or has caveats

**Item format:**
```
[posture indicator] [package label]     [freshness chip]  ›
```

**Posture indicator** (left icon, replaces the status dot from Project V items):

| Posture | Icon | Color |
|---|---|---|
| `ready` | `●` filled | `--state-success` |
| `ready_with_caveats` | `◐` half-filled | `--state-warning` |
| `in_progress` | `○` hollow pulsing | `--state-info` |
| `stale` | `●` filled | `--state-danger` dimmed via `--state-disabled-opacity` |
| `expired` | `×` | `--text-tertiary` |

The `●` / `◐` / `○` distinction is deliberate: it reads as a signal-strength metaphor rather than a lifecycle metaphor. A fully filled circle means the signal is solid and ready. A half-filled circle means ready but partial. A hollow circle means still forming.

The pulsing animation on `in_progress`: a subtle opacity oscillation (0.4s ease, opacity 1.0 → 0.5 → 1.0) — same pattern as the reconnecting dot in Session 3. Used sparingly; only on actively-collecting items.

**Freshness chip** (right of label, before `›`):

The freshness chip is a compact time-since label:

- `< 1h` — `--state-success`, `--type-xs`
- `< 24h` — `--state-success`, `--type-xs`
- `1–3d` — `--state-warning`, `--type-xs`
- `> 3d` — `--state-danger`, `--type-xs`
- `aging` — `--state-warning`, `--type-xs` (when no specific timestamp is available but posture is known to be aging)
- `expired` — `--text-tertiary`, `--type-xs`

This chip is the key visual separator from Project V's status badges. Where Project V badges say things like `awaiting approval`, VEDA chips say things like `18h` or `3d`. VEDA's primary question is always *how fresh is this*, not *what stage is this in*.

**Grouping within Signal Packages:**

Signal packages are grouped by their target consumer system:

```
SIGNAL PACKAGES                          [3 ready]
  FOR PROJECT V                              ← group header, non-navigable
    [●] Hosting keyword intent     < 1h  ›
    [◐] SERP delta — hosting       2d   ›   ← ready_with_caveats
  FOR V FORGE                                ← group header
    [●] GA4 performance snapshot   18h  ›
  UNROUTED                                   ← packages not yet targeted
    [○] Competitor coverage analysis         ← in_progress, no freshness chip
```

Group headers (`FOR PROJECT V`, `FOR V FORGE`, `UNROUTED`) follow the same section-header visual language: `--type-xs`, `--weight-semibold`, `--text-tertiary`, non-navigable, non-hoverable. They are anchors only.

**Clicking a signal package item** opens the signal package detail in the center workspace. This is navigation only — no inline actions.

**Empty state (no packages):**
```
SIGNAL PACKAGES
  No signal packages produced yet
```
`--text-tertiary`, `--type-xs`, indented.

---

### 5.2 Observatory Domains section

Observatory domains are the scoped areas VEDA is actively watching for the current project. Each domain maps to a category of observable signal (search, performance, YouTube, source capture, etc.).

**Section header:**
```
OBSERVATORY DOMAINS                      [5 active]
```

Count badge shows active domains. No urgency coloring on the badge — domains are always-on infrastructure, not attention items.

**Domain item format:**
```
[domain indicator] [domain name]         [observation status]  ›
```

**Domain indicator** (left, 8px):

| State | Treatment |
|---|---|
| `active` — collecting normally | `--state-success` dot |
| `active` — stale (not updated recently) | `--state-warning` dot |
| `degraded` — provider issue | `--state-warning` dot + `⚠` suffix |
| `inactive` / paused | `--text-tertiary` hollow dot |
| `error` | `--state-danger` dot |

**Observation status** (right of domain name, `--type-xs`):

A compact status tag showing the most recent observation time or current collection state:

- `collecting` — `--state-info`, animated pulse
- `2h ago` — `--state-success`
- `8h ago` — `--state-warning`
- `18h ago` — `--state-danger`
- `paused` — `--text-tertiary`
- `error` — `--state-danger`

**Domain items (examples):**
```
OBSERVATORY DOMAINS                      [5]
  [●] Search / SERP               2h ago  ›
  [●] Search Console              4h ago  ›
  [●] GA4 Performance             1h ago  ›
  [◌] YouTube Observatory         paused  ›
  [●] Source Capture              8h ago  ›
```

**Clicking a domain item** opens the domain detail view in the center workspace, showing current observation configuration and recent records.

**Expandable:** Domains section is expandable to show signal package counts per domain and any domain-level alerts inline. Compact by default.

---

### 5.3 Providers section

Providers are the external data sources VEDA uses to populate its observatory — Google Search Console, GA4, SerpAPI, paid keyword providers, YouTube API, etc. This section surfaces their health, spend posture, and any pending authorizations.

**Section header:**
```
PROVIDERS                                [6]
```

No urgency on the count badge unless a provider has a pending paid approval or is in error state:
- Badge `--state-warning` if any provider has a pending paid data pull awaiting approval
- Badge `--state-danger` if any provider is in error

**Provider item format:**
```
[health dot] [provider name]             [status chip]  ›
```

**Health dot colors:**

| State | Color |
|---|---|
| `connected`, data current | `--state-success` |
| `connected`, data stale | `--state-warning` |
| `degraded` — partial data | `--state-warning` |
| `disconnected` / `error` | `--state-danger` |
| `pending_approval` — paid pull awaiting auth | `--state-pending` (`--state-warning`) |
| `inactive` — configured but off | `--text-tertiary` hollow |

**Status chip** (right of name, `--type-xs`):

- `connected` — `--text-tertiary` (positive normal state, quiet)
- `stale — 12h` — `--state-warning`
- `error` — `--state-danger`
- `awaiting approval` — `--state-warning`, `--weight-bold` — this is the key attention state

**Paid data pull awaiting approval — special treatment:**

When a provider has a pending paid data pull that requires Class C operator approval, its row receives enhanced treatment:

```
[⚠] SerpAPI — Paid Keyword Pull    awaiting approval  ›
```

- `⚠` icon in `--state-warning` replaces the health dot
- Label in `--text-primary` (full brightness, not dimmed)
- `awaiting approval` chip in `--state-warning` with `--weight-bold`
- Row hover reveals: `[Proceed to Approval Gate ›]` — this navigates to the center workspace where the Class C gate lives. **This is navigation, not an approval action.**

The `[Proceed to Approval Gate ›]` affordance appears only on hover, only for `awaiting approval` rows. It is styled identically to the `[Proceed to Approval Gate]` button from Session 5 (right panel output cards): `--border-accent`, `--accent-primary` text. The visual match is intentional — it signals the same governed routing concept from a different surface.

**Clicking any provider item** opens the provider configuration and status detail in the center workspace.

---

### 5.4 Event Log section

The event log section shows a bounded window of recent observatory state changes — the most operationally relevant recent events in VEDA's lifecycle for this project.

**This is not a full audit trail.** It is a 5–10 item summary of recent events to give the operator ambient awareness. The full event log is accessible via the center workspace detail view.

**Section header:**
```
EVENT LOG                                [recent]
```

No count badge. Static `[recent]` label in `--text-tertiary`, `--type-xs` indicates this is a bounded recent window, not a total count.

**Event item format:**
```
[event icon] [event description]         [time]
```

Event items are **non-navigable by default** — they are read-only log entries. Exception: if an event requires follow-up action (e.g., a signal package became stale), the item gets a `›` navigation affordance linking to the relevant record.

**Event icon vocabulary:**

| Event type | Icon | Color |
|---|---|---|
| Signal package produced | `◆` | `--state-success` |
| Signal package expired | `◆` | `--text-tertiary` |
| Domain observation completed | `●` | `--state-info` |
| Provider connected | `↑` | `--state-success` |
| Provider degraded / error | `⚠` | `--state-warning` |
| Paid pull authorized | `✓` | `--state-success` |
| Paid pull rejected | `✗` | `--state-danger` |
| Scope configuration changed | `⚙` | `--text-secondary` |
| Evidence stale threshold crossed | `⚠` | `--state-warning` |

**Event item text:** `--type-xs`, `--text-secondary`. Timestamp: `--type-xs`, `--text-tertiary`, right-aligned.

**Example:**
```
EVENT LOG                                [recent]
  ◆  Hosting keyword snapshot produced    2h ago
  ●  Search Console observation run       4h ago
  ⚠  GA4 connection degraded              6h ago  ›
  ✓  SerpAPI paid pull authorized         1d ago
  ◆  SERP delta package produced          2d ago
```

**Collapsed by default.** The event log is the lowest-priority section in the tree. It defaults to showing only the 3 most recent events in compact state. Expanding shows up to 10. A `[View full log ›]` link at the bottom of the expanded list navigates to the full event log detail in the center workspace.

---

## 6. VEDA Item Indicator Vocabulary (Full Reference)

This is the complete indicator vocabulary for the VEDA tree — distinct from Project V's lifecycle status vocabulary.

### Primary posture indicator (replaces status dot)

| Symbol | Meaning | Token |
|---|---|---|
| `●` filled | Fresh / ready / healthy | `--state-success` |
| `◐` half-filled | Ready with caveats / aging | `--state-warning` |
| `○` hollow | In progress / collecting | `--state-info` |
| `●` filled dim | Stale / degraded | `--state-danger` at `--state-disabled-opacity` |
| `×` | Expired / disconnected | `--text-tertiary` |
| `◌` hollow | Inactive / paused | `--text-tertiary` |
| `⚠` | Requires attention / error | `--state-warning` or `--state-danger` |

The filled/half/hollow/dim progression reads as signal strength — full signal, partial signal, forming signal, degraded signal. This is a deliberately different visual language from Project V's dot-color-as-lifecycle. An engineer or designer picking up this tree should immediately sense that VEDA items answer a different question.

### Freshness chips (time-based)

Freshness chips replace Project V's lifecycle badge text. They answer "how old is this" not "what stage is this in":

| Age | Display | Color |
|---|---|---|
| Under 1 hour | `< 1h` | `--state-success` |
| 1–23 hours | `Nh ago` | `--state-success` |
| 1–3 days | `Nd ago` | `--state-warning` |
| Over 3 days | `Nd ago` | `--state-danger` |
| Unknown age | `aging` | `--state-warning` |
| Expired | `expired` | `--text-tertiary` |

Freshness chips are `--type-xs`, `--radius-pill`, light background using the same 10% opacity pattern as Session 6's handoff status badges.

### Trust posture chips (shown in expanded detail, not compact)

When a signal package or domain row is expanded in the tree, a trust posture chip appears alongside the freshness chip:

| Trust level | Chip text | Color |
|---|---|---|
| `high` | `high trust` | `--state-success` text |
| `medium` | `med trust` | `--state-warning` text |
| `low` | `low trust` | `--state-danger` text |
| `uncertain` | `unverified` | `--text-tertiary` |

Trust posture chips are the same visual treatment as evidence trust badges in the context strip (Session 4, Category 5 — EVIDENCE). Visual consistency here is intentional: when an operator sees a trust chip in the VEDA nav tree and then sees the same trust chip in the context strip's EVIDENCE row, they should read them identically.

---

## 7. Per-Item Action Affordances

### Navigation (every item)

Clicking any navigable item opens the record detail in the center workspace. The `›` glyph on hover confirms navigability. Same as Project V.

### Context menu (right-click / `⋯` on hover)

VEDA items support the same minimal context menu as Project V:
- `Open detail` — same as click
- `Copy record ID` — copies the record identifier to clipboard

**The context menu does not contain:**
- Configure scope inline
- Trigger observation run
- Approve data pull
- Any status transition

### Observatory scope configuration

Configuring observatory scope (adding/modifying keyword targets, adjusting cadence, enabling/disabling channels) routes through the center workspace, not the nav tree. The nav tree navigates to the domain detail; the detail view contains the scoped configuration controls within governed operator bounds.

### Paid data pull initiation

Initiating a paid data pull request routes through the `+ New…` nav footer command path, which opens the governed command menu for VEDA (Session 21). The nav tree does not surface an inline "request paid pull" button on provider items — the `awaiting approval` row shows the navigation path to the existing gate, but new pull requests are initiated through the command path.

---

## 8. VEDA Tree Absent-Affordance Rules

These are absolute. Nothing on this list may appear in the VEDA nav tree under any circumstances.

**Planning boundary (must never appear):**
- Create Planning Record / Objective / Initiative / WorkItem
- Approve or activate a Project V handoff
- Transition any Project V record status
- Produce planning decisions from the VEDA surface
- Any label suggesting VEDA is directing planning

**Execution boundary (must never appear):**
- Initiate V Forge execution
- Configure V Forge scope
- Route return triggers (that belongs to Project V/V Forge nav)
- Any control that implies VEDA owns execution

**Approval controls (must never appear):**
- Class B or C gate widgets anywhere in the VEDA tree
- `Approve` button on paid data pull rows (the nav shows `awaiting approval` + navigate-to-gate; the gate lives in center workspace)
- Any inline approval action on any VEDA record

**LLM interaction (must never appear):**
- Text input field
- Mode selector
- Any LLM prompt affordance

**Confusing labels (must never appear):**
- `Authorize` on any tree item (this belongs in gate surfaces only)
- `Confirm` on any tree item
- `Execute` or `Run` as tree-item actions that would initiate direct mutation

---

## 9. Panel-Level States (VEDA-specific)

### No observable domains configured

When a project has no observatory domains set up:

```
SIGNAL PACKAGES
  No signal packages yet — configure observatory domains to begin observing.

OBSERVATORY DOMAINS
  No domains configured                 [+ Configure]

PROVIDERS
  (provider items still shown — providers exist independently of per-project domains)

EVENT LOG
  No recent events
```

`[+ Configure]` navigates to the observatory scope configuration detail in the center workspace. It is not an inline creation form. `--text-link`, `--type-xs`.

### All providers degraded

When all providers show error or degraded state, the PROVIDERS section header badge turns `--state-danger` and a non-blocking inline warning appears at the top of the tree content:

```
⚠ Provider connectivity degraded — signal freshness affected
```

`--staleness-bg`, `--staleness-text`, `--type-xs`, top of tree content area. Not a modal — ambient warning. The operator can scroll past it or click to open the PROVIDERS section directly.

### Session error state

Identical to Session 6: tree items become non-interactive at `--state-disabled-opacity`, action arrows disappear, a banner appears at the top of the tree content. The nav header remains interactive.

---

## 10. Synchronization

### EVENT-07 (Evidence Loaded)
When the operator loads evidence from VEDA into the session (from the context strip or center workspace), the relevant Signal Package item in the VEDA tree may update its freshness chip to reflect that it has been accessed. This is cosmetic — it does not change the package's posture.

### EVENT-08 (Evidence Stale)
The affected signal package item's posture indicator updates from `●` to `●` dim (stale treatment). Freshness chip updates to show age in `--state-danger`. Section count badge updates.

### EVENT-09 (Evidence Refreshed)
The package item returns to `●` fresh. Freshness chip updates. An event log entry appears in the EVENT LOG section: `◆ [package name] refreshed`.

### EVENT-11 (System Changed)
Full tree content swap with `--transition-fade`. If switching away from VEDA to Project V or V Forge, the tree replaces entirely. If switching to VEDA from another system, the VEDA tree loads and populates.

### EVENT-05 (Paid Pull Approval Written)
The `awaiting approval` provider row updates — `⚠` icon replaced with health dot, `awaiting approval` chip replaced with `connected` or `collecting`. An event log entry: `✓ [provider] paid pull authorized`. The Providers section badge urgency clears.

---

## 11. Token Usage from Session 2

No new tokens introduced. All visual decisions reference Session 2.

| Element | Token(s) |
|---|---|
| Shell, headers, items | Inherited from Session 6 |
| Posture indicator `●` ready | `--state-success` |
| Posture indicator `◐` caveats | `--state-warning` |
| Posture indicator `○` in-progress | `--state-info` |
| Posture indicator stale dim | `--state-danger` + `--state-disabled-opacity` |
| Posture indicator expired | `--text-tertiary` |
| In-progress pulse animation | Opacity oscillation, 400ms ease |
| Freshness chip < 1d | `--state-success`, `--type-xs`, `--radius-pill` |
| Freshness chip 1–3d | `--state-warning`, `--type-xs`, `--radius-pill` |
| Freshness chip > 3d | `--state-danger`, `--type-xs`, `--radius-pill` |
| Trust chip `high` | `--state-success` text |
| Trust chip `medium` | `--state-warning` text |
| Trust chip `low` | `--state-danger` text |
| Trust chip `uncertain` | `--text-tertiary` |
| `awaiting approval` chip | `--state-warning`, `--weight-bold` |
| `[Proceed to Approval Gate ›]` | `--border-accent`, `--accent-primary` text |
| Provider health dot states | Per table in §5.3 |
| Event log icon colors | Per table in §5.4 |
| Event log text | `--type-xs`, `--text-secondary` |
| Event log timestamp | `--type-xs`, `--text-tertiary` |
| Provider degraded banner | `--staleness-bg`, `--staleness-text` |
| `[+ Configure]` link | `--text-link`, `--type-xs` |

---

## 12. What This Session Resolves

- The VEDA tree is fully specified with its own indicator vocabulary that is visibly distinct from Project V's lifecycle vocabulary. A developer seeing both trees simultaneously should immediately recognize they answer different questions.
- The posture indicator system (`●`/`◐`/`○`/dim/`×`/`◌`) is defined as a signal-strength metaphor appropriate to an observatory, not a lifecycle metaphor appropriate to planning records.
- Freshness chips establish time-since as the primary observable quality for VEDA items — replacing the lifecycle badge text from Session 6.
- Trust posture chips appear in expanded detail, maintaining visual consistency with the context strip's evidence trust display from Session 4.
- The paid data pull path is specified without putting an approval button in the nav: `awaiting approval` rows show a navigate-to-gate affordance (`[Proceed to Approval Gate ›]`) that routes the operator to the center workspace where the Class C gate lives. The gate never lives in the nav tree.
- The four-section structure (Signal Packages, Observatory Domains, Providers, Event Log) reflects the observatory consumption priority hierarchy.
- All VEDA-specific absent-affordances are enumerated concretely.
- Synchronization behavior for relevant events is specified.

---

## 13. What This Session Does Not Resolve Yet

- **Center workspace VEDA detail views** — clicking any VEDA nav item opens a detail view; that view's content is Session 9 (center workspace foundation) territory.
- **Observatory scope configuration UI** — operators can navigate to it from the VEDA tree; the configuration form itself is Session 9 or Session 15 (Maintenance / Ranking UX) territory.
- **Paid data pull Class C gate** — the nav routes to it; the gate design is Session 10 (Approval Gate Surfaces).
- **Signal package detail view** — the most important VEDA center view; it shows the full signal package, evidence chain, trust posture, and routing controls. Designed in Session 9.

---

## 14. Recommended Inputs to Session 8

Session 8 is the V Forge tree — the third and final system tree. By designing all three trees in sessions 6, 7, and 8, the cross-system absent-affordance vocabulary becomes fully visible through comparison.

**Session 8 key contrasts to establish:**

V Forge's tree is execution-truth focused. Its items are execution records — active execution items, content graph summaries, return triggers, execution reports. The indicator vocabulary for V Forge items should reflect execution state rather than observatory posture or planning lifecycle:

- V Forge items have execution states: `running`, `halted`, `blocked`, `awaiting_review`, `completed`
- These are distinct from both Project V's lifecycle states (`proposed`/`active`/`blocked`/`closed`) and VEDA's observatory postures (`ready`/`in_progress`/`stale`)
- Return triggers in V Forge are the most prominent item type — they deserve the same floating-to-top treatment as in the Project V tree (Session 6), and the same `⚡` icon vocabulary

**The specific design question Session 8 must resolve:**

When a return trigger exists in V Forge and the operator is viewing the V Forge tree, the trigger is prominent. When the operator is viewing the Project V tree, the same trigger is also prominent (it floats to the top of that tree too, per Session 6). These are the same trigger viewed from two different system perspectives. Session 8 should explicitly specify that the two representations are synchronized (the V Forge tree shows the trigger's V Forge-side state; the Project V tree shows its Project V routing state) and that neither tree's representation implies the other system owns the trigger.
