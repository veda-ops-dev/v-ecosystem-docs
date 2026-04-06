# Session 8 — Left Nav — V Forge Tree
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Session 2 (Tokens), Session 3 (Topbar), Session 6 (Left Nav Shell + Project V Tree), Session 7 (VEDA Tree)
**Required before:** Session 9 (Center Workspace Foundation) — all three system trees are now specified; the cross-system absent-affordance vocabulary is complete; Session 9 can reference the nav as a stable anchor

---

## 1. Files Read

- `session-02-minimal-token-decisions.md` — active token baseline
- `session-06-left-nav-shell-project-v-tree-spec.md` — shell, section header anatomy, tree item anatomy, action affordance rules, absent-affordances — all inherited
- `session-07-left-nav-veda-tree-spec.md` — observatory posture indicator vocabulary established; Session 8 must use distinct execution-state vocabulary
- `session-08-open-question` — return trigger dual-representation synchronized between Project V and V Forge trees
- `desktop-surface-architecture.md` — V Forge nav content rules; actions available/not available in V Forge view; return trigger prominent when present
- `operator-surface-interfaces.md` — V Forge operator surface: view execution state, review findings, approve/reject launch-sensitive actions, initiate/approve return-to-planning, review pre-launch verification, approve launches, configure bounded execution scope
- `v-forge/v-forge.md` — V Forge owns execution truth, content graph, publication continuity; not planning truth, not signal truth
- `v-forge/operational-model.md` — execution_entry_status vocabulary: `received`, `pending_clarification`, `active`, `paused`, `completed`, `blocked`, `returned`, `closed`
- `v-forge/controlled-vocabularies.md` — `execution_entry_status`, `execution_finding_type`, `execution_finding_status`, `surface_status`, `publication_status`, `content_decay_status`
- `v-forge/reporting-and-approval-model.md` — what V Forge must report, approval class context, return-to-planning package
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md` — return trigger lifecycle; what transfers, what doesn't; V Forge retains execution truth after return
- `workflows/maintenance-and-replanning-workflow.md` — maintenance vs replanning distinction; return trigger as classification question

---

## 2. Session 8 Scope Confirmation

The work plan defines Session 8 as: the V Forge system's left nav content — the most distinctive of the three trees, with return triggers, content graph, and absent-affordances distinct from both Project V and VEDA.

This session produces:
- V Forge tree structure: active execution items, content graph summary, return triggers (prominent), recent findings summaries
- Return trigger visual treatment when state is `arrived` or `acknowledged`
- Execution state indicator vocabulary (distinct from Project V lifecycle and VEDA observatory posture)
- V Forge-specific absent-affordances
- Resolution of the Session 7 open question: return trigger dual-representation across Project V and V Forge trees
- Panel-level states, synchronization behavior

This session does not:
- Design the center workspace V Forge detail views (Session 9)
- Design the return trigger review view (Session 13)
- Design the launch readiness review (Session 14)

---

## 3. V Forge Tree Character

V Forge's tree is the execution window. Where Project V shows what has been planned and VEDA shows what has been observed, V Forge shows what is being built and what has happened during building.

The three trees now form a complete cross-system vocabulary contrast:

| System | Primary question answered | Indicator vocabulary |
|---|---|---|
| Project V | What stage is this planning record in? | Lifecycle status dots |
| VEDA | How fresh and trustworthy is this observation? | Posture indicators + freshness chips |
| V Forge | What is the execution state of this work? | Execution state indicators |

V Forge's execution state is operationally specific. An execution entry is not `active` in the abstract — it is `active` meaning execution is currently in progress within approved scope. `blocked` means it cannot continue without external resolution. `returned` means a return-to-planning has been triggered. These are precise execution states from the controlled vocabulary, not general lifecycle labels.

---

## 4. V Forge Tree Structure

When the current system is V Forge, the tree content region shows the V Forge execution tree. Sections in fixed order:

```
RETURN TRIGGERS       ← floats to top when active (highest urgency)
EXECUTION ENTRIES     ← active execution work from handed-off scope
CONTENT GRAPH         ← structural summary of what has been built
EXECUTION FINDINGS    ← open findings from execution
SURFACES              ← owned/operated surfaces and their status
```

**RETURN TRIGGERS floats to the top** whenever at least one trigger is in `arrived` or `acknowledged` state — identical to the Project V tree behavior from Session 6. This is the one exception to fixed section order, justified by the governance urgency of an unresolved return trigger.

When no return triggers are active: section absent entirely. Same rationale as Session 6 — the topbar badge and context strip INTEGRITY row cover the zero-triggers case; the nav tree does not need a dormant placeholder.

---

## 5. Resolving the Session 7 Return Trigger Dual-Representation Question

Session 7 posed: when a return trigger exists, both the V Forge tree and the Project V tree show it. Are these synchronized? Does either tree imply ownership?

**Resolution: Both trees show the same trigger from their respective system perspectives. They are synchronized. Neither implies the other system owns the trigger.**

The two representations are intentionally different in what they show:

**V Forge tree (this session):**
- Shows the trigger from V Forge's execution perspective
- The trigger item label reflects what V Forge found and routed back
- Status reflects V Forge's execution state: `arrived` (V Forge has sent it), `acknowledged` (operator has seen it), `returned` (it is now in Project V's hands — the V Forge side resolves)
- When state reaches `returned` or `dismissed`, the V Forge tree item updates to show resolution and the section clears when all triggers are resolved

**Project V tree (Session 6):**
- Shows the trigger from Project V's planning perspective
- The trigger item label reflects the routing decision facing Project V
- Status reflects the planning-side lifecycle: `arrived`, `acknowledged`, `routed`, `dismissed`

**What synchronization means here:** When the operator views the Project V tree and sees a trigger in `routed` state, the V Forge tree should show the same trigger in `returned` state. The states map to each other across system perspectives — they are not the same values (V Forge uses `returned`; Project V uses `routed`) but they reflect the same resolution event.

**What it does not mean:** The V Forge tree does not imply V Forge owns the routing decision. The Project V tree does not imply Project V owns the execution finding. Both trees display their system's perspective on the same cross-system event. The return-to-planning interface governs what actually transferred; the nav trees show that transfer honestly from each side.

---

## 6. Execution State Indicator Vocabulary

V Forge items use **execution state indicators** — distinct from Project V's lifecycle dots and VEDA's observatory posture indicators.

### Primary indicator (replaces status dot)

The indicator for V Forge execution entries is a labeled status badge rather than a dot or posture symbol. This is because execution state names carry specific operational meaning that color alone cannot communicate. A `blocked` execution entry and a `paused` one look the same in color (both `--state-warning`) but mean very different things.

**Execution entry status badges:**

| `execution_entry_status` | Badge text | Badge color | Dot color |
|---|---|---|---|
| `received` | `received` | `--text-tertiary` | `--text-tertiary` |
| `pending_clarification` | `needs clarification` | `--state-warning` | `--state-warning` |
| `active` | `active` | `--state-success` | `--state-success` |
| `paused` | `paused` | `--state-warning` | `--state-warning` |
| `completed` | `completed` | `--state-success` dim | `--accent-primary-dim` |
| `blocked` | `blocked` | `--state-danger` | `--state-danger` |
| `returned` | `returned to planning` | `--state-info` | `--state-info` |
| `closed` | `closed` | `--text-tertiary` hollow | `--text-tertiary` hollow |

The **dot** (8px, left of label) carries the color. The **badge text** (right of label) carries the name. Together they give both ambient color recognition and precise name recognition. This is more visual weight than a Project V item, which is appropriate — V Forge execution entries have operational urgency that planning tree items do not.

**Why `returned` is `--state-info` and not warning/danger:** A return-to-planning is not a failure state. It is a governed operational response. Using blue/info communicates "this has moved to another system for deliberate reason" rather than "something is wrong." The Project V tree uses `⚡` `--state-danger` for the trigger because unresolved triggers on the planning side require urgent action. On the V Forge side, once routed, the trigger is resolved — the V Forge item updates to `returned` in a neutral acknowledgment color.

### Content graph item indicators

Content graph items (pages, topics, entities) use simpler indicators:

| State | Indicator |
|---|---|
| `published` | `●` `--state-success` |
| `draft` | `○` hollow `--text-secondary` |
| `archived` | `●` `--text-tertiary` dim |
| `redirected` | `→` `--text-tertiary` |
| `stale` decay status | `⚠` `--state-warning` appended |
| `critical` decay status | `⛔` `--state-danger` appended |

### Surface status indicators

| `surface_status` | Dot | Color |
|---|---|---|
| `active` | `●` | `--state-success` |
| `paused` | `◐` | `--state-warning` |
| `retired` | `●` dim | `--text-tertiary` |

---

## 7. Section Specifications

### 7.1 Return Triggers section (conditional — floats to top when active)

Identical architecture to Session 6 (Project V tree), with V Forge-specific state vocabulary.

**Section header when triggers present:**
```
⚡ RETURN TRIGGERS                       [2]
```
Header in `--state-danger` when any trigger is `arrived`. `--state-warning` when all triggers are `acknowledged`.

**Item format:**
```
[⚡] [trigger label]              [state badge]  ›
```

**State badges for V Forge-side return trigger states:**

| V Forge-side state | Badge text | Color |
|---|---|---|
| `arrived` | `unreviewed` | `--state-danger`, `--weight-bold` |
| `acknowledged` | `reviewed — action pending` | `--state-warning` |
| `returned` | `returned to planning` | `--state-info` |

When all triggers reach `returned` state, the section clears from the tree on next refresh.

**Clicking a return trigger item** opens the return trigger review in the center workspace. Navigation only — the `Route` and `Dismiss` response options live in the center workspace detail view, not in the nav tree.

**Important — what this section does NOT contain:**
- `[Route to planning]` button inline
- `[Dismiss]` button inline
- Any action that resolves the trigger from within the nav

The nav shows the trigger prominently. It does not govern the response.

---

### 7.2 Execution Entries section

Execution entries are the handed-off work scopes that V Forge is currently executing or has executed. Each entry corresponds to a governed handoff received from Project V.

**Section header:**
```
EXECUTION ENTRIES                        [3]
```

Count badge shows non-closed entries. No urgency coloring unless an entry is `blocked` (→ `--state-danger` badge) or `returned` (→ `--state-info` badge).

**Item format:**
```
[dot] [entry label]              [status badge]  ›
```

**Examples:**
```
EXECUTION ENTRIES                        [3]
  [●] hosting-comparison-site     active  ›
  [●] seo-tech-audit              paused  ›
  [⚡] content-hub-v1             blocked  ›
```

`[⚡]` replaces the status dot for `blocked` entries — using the same `⚡` glyph at `--state-danger` communicates that this item requires attention, consistent with the return trigger icon vocabulary.

**Expandable:** Yes. Expanded view shows:
- Start date / received date
- Handoff reference (e.g., `from handoff: [hdl-07]`)
- Any open execution findings count
- Any return triggers associated with this entry
- Brief scope note from the handoff (truncated to 80 chars)

**Clicking an execution entry** opens the execution entry detail in the center workspace.

---

### 7.3 Content Graph section

The content graph is V Forge's structural model of what has been built — pages, topics, entities, internal links. The nav tree shows a high-level summary rather than the full graph (that lives in the center workspace content graph view).

**Section header:**
```
CONTENT GRAPH                            [47 pages]
```

Count badge shows total published pages. No urgency coloring unless decay-critical pages exist (→ badge `--state-danger`).

**Sub-sections within Content Graph:**

The content graph section has three fixed sub-groups:

```
CONTENT GRAPH                            [47 pages]
  PAGES                                  [47]
    ⚠ 3 pages — critical decay                    ← inline alert, non-navigable
    [●] Hosting comparison hub           pillar  ›
    [●] WP Engine vs Kinsta              comparison ›
    [⛔] Best WordPress hosting 2026     critical  ›
    [+12 more]                                    ← expand to show all
  TOPICS                                 [8]
    [●] WordPress hosting
    [●] Managed hosting
    [○] VPS hosting                             ← draft/planned, not yet published against
  ENTITIES                               [5]
    [●] WP Engine
    [●] Kinsta
    [●] SiteGround
```

**PAGES sub-section:**
Each page shows: publication status dot + page title + content archetype badge + navigation arrow. Archetype badges use `--type-xs`, `--text-tertiary` label: `pillar`, `spoke`, `comparison`, `review`, etc. — the `content_archetype` vocabulary from the controlled vocabularies doc.

Decay status appended to item where relevant:
- `⚠` `--state-warning` for `stale` decay
- `⛔` `--state-danger` for `critical` decay

The `[+12 more]` expansion pattern: compact view shows 5 items max. Additional items collapsed to `[+N more]` with expand affordance. This prevents the content graph section from dominating the nav at scale.

**Decay alert** (inline, non-navigable):
```
⚠ 3 pages — critical decay
```
`--staleness-bg`, `--staleness-text`, `--type-xs`, shown above the page list when any pages have `critical` decay status. Clicking anywhere in the row expands the section (not a separate navigation action).

**TOPICS sub-section:**
Topics are shown as a flat list with publication status dots. No count in sub-header — topics don't have the same count urgency as pages. Topics are navigable to the topic detail in the center workspace.

**ENTITIES sub-section:**
Entities shown as a flat list with status dots. Navigable to entity detail.

**Collapsed by default** when content graph has more than 5 pages. Expanded by default when 5 or fewer pages (new project context).

---

### 7.4 Execution Findings section

Open findings from execution — items that have been recorded but not yet resolved. This is V Forge's equivalent of Project V's Gaps section, but scoped to execution-side findings rather than planning-side gaps.

**Section header:**
```
EXECUTION FINDINGS                       [4 open]
```

Count badge shows `open` finding count. Badge color:
- `--state-danger` if any `blocker` type findings are open
- `--state-warning` if only `changed_condition`, `decision_point`, `scope_gap`, or `quality_issue` findings
- No badge if only `informational` findings

**Item format:**
```
[severity icon] [finding label]         [type badge]  ›
```

**Severity icons** (using `execution_finding_type`):

| Finding type | Icon | Color |
|---|---|---|
| `blocker` | `⛔` | `--state-blocked` |
| `changed_condition` | `⚡` | `--state-warning` |
| `decision_point` | `◈` | `--state-warning` |
| `scope_gap` | `⚠` | `--state-warning` |
| `quality_issue` | `ℹ` | `--state-info` |
| `informational` | `·` | `--text-tertiary` |

**Type badge** (right of label): abbreviated finding type in `--type-xs`, `--text-tertiary`: `blocker`, `changed`, `decision`, `scope gap`, `quality`, `info`.

**Example:**
```
EXECUTION FINDINGS                       [4 open]
  [⛔] CWV threshold not met            blocker  ›
  [⚡] Hosting provider changed pricing  changed  ›
  [◈] Review: expand scope to include VPS?  decision  ›
  [ℹ] Alt text missing — 3 images       info  ›
```

**Clicking a finding** navigates to the finding detail in the center workspace.

**`resolved_locally` and `returned` findings** are not shown in this section. They are accessible from the execution entry detail view. The Execution Findings section shows only `open` findings that need operator awareness.

---

### 7.5 Surfaces section

Surfaces are V Forge's owned and operated execution surfaces — website, GitHub/release, YouTube channel, etc. This section gives ambient awareness of surface operational state.

**Section header:**
```
SURFACES                                 [3]
```

**Item format:**
```
[dot] [surface name]             [type] [status]  ›
```

**Example:**
```
SURFACES                                 [3]
  [●] veda-domination.com         website  active  ›
  [●] YT: Veda SEO Channel        youtube  active  ›
  [◐] WP Plugin Directory         store    paused  ›
```

Surface type labels: `website`, `github`, `youtube`, `social`, `newsletter`, `store` — abbreviated from `surface_type` vocabulary. `--type-xs`, `--text-tertiary`.

Status text: `active`, `paused`, `retired` — from `surface_status` vocabulary. Same color treatment as execution entry status badges but without bold (surfaces are infrastructure, lower urgency than execution entries).

**Clicking a surface** navigates to the surface detail in the center workspace.

---

## 8. V Forge Tree Absent-Affordance Rules

**Planning boundary (must never appear):**
- Create Planning Record / Objective / Initiative / WorkItem
- Modify governing decisions
- Approve or activate a Project V handoff (the handoff received V Forge's way is a different thing — V Forge accepts a handoff; it cannot approve one)
- Configure Project V portfolio visibility or sequencing

**Observatory boundary (must never appear):**
- Configure VEDA observatory scope
- Initiate a VEDA paid data pull
- Modify VEDA provider integrations
- Present V Forge execution intelligence as though it were VEDA-originated signal

**Governance controls (must never appear):**
- Class B or C gate widgets
- `Approve` or `Authorize` buttons on any tree item
- Launch authorization inline (the nav can surface that launch authorization is pending; it cannot complete the authorization)
- Self-authorize execution actions that require operator approval

**Route/dismiss in the tree (must never appear directly):**
- `[Route return trigger]` button on tree items
- `[Dismiss return trigger]` button on tree items
- These response options live in the center workspace return trigger review — the nav shows the trigger and navigates to it, nothing more

**LLM interaction (must never appear):**
- Text input
- Mode selector
- Any LLM prompt affordance

---

## 9. Launch Authorization Pending — Special Treatment

When V Forge execution reaches the `Launch Authorization — Pending` workflow stage (launch readiness is confirmed, authorization is being sought), this state appears in the Execution Entries section with elevated treatment:

```
EXECUTION ENTRIES                        [1]
  [◈] content-hub-v1         launch auth pending  ›
```

The `◈` glyph replaces the status dot (same `◈` used for the project scope indicator in the topbar — communicating "scope anchor" or "awaiting scoped authorization"). Badge text: `launch auth pending`. Badge color: `--state-pending` (`--state-warning`), `--weight-bold`.

The entry is navigable to the launch readiness review in the center workspace. The nav does not contain the authorization gate.

---

## 10. Panel-Level States

### Empty state (no execution entries yet — project handed off but work not started)

```
EXECUTION ENTRIES
  No active execution entries
  Awaiting handoff from Project V

CONTENT GRAPH
  Not yet built — execution has not begun

EXECUTION FINDINGS
  —

SURFACES
  No surfaces registered
```

Each section shows its own empty state. `--text-tertiary`, `--type-xs`. The empty state is honest: it distinguishes "no work started" from "work complete."

### Active project, all entries completed and closed

```
EXECUTION ENTRIES                        [0 active]
  All execution entries closed           ✓

CONTENT GRAPH                            [47 pages]
  (full content graph shown — still valuable after execution complete)
```

`✓` in `--state-success` badge position. Content graph remains visible and browsable even when no active execution entries exist — the content graph is a persistent record of what was built, not just an active execution view.

### Session error state

Identical to Sessions 6 and 7: items become non-interactive at `--state-disabled-opacity`, action arrows disappear, error banner at top of tree content.

---

## 11. Synchronization

### EVENT-16 (Return Trigger Arrives)
The RETURN TRIGGERS section appears at the top of the V Forge tree immediately, above EXECUTION ENTRIES. Item shows `unreviewed` badge in `--state-danger`. The relevant execution entry in EXECUTION ENTRIES may also update to show the associated trigger.

### EVENT-05 (Approval Written — launch authorization)
The execution entry badge updates from `launch auth pending` to `active` (if launch proceeds) or the entry moves to `blocked` (if denied). The EXECUTION ENTRIES section count badge updates.

### When a return trigger reaches `returned` (via the Project V surface routing it):
The V Forge tree's RETURN TRIGGERS item updates its badge from `reviewed — action pending` to `returned to planning` in `--state-info`. Once all triggers are `returned` or their V Forge-side equivalent is resolved, the section clears on next refresh.

### EVENT-11 (System Changed)
Full tree content swap with `--transition-fade`. Same behavior as Sessions 6 and 7.

### EVENT-17 (Workflow Stage Change — execution enters/exits active)
Relevant execution entry status badge updates in place with `--transition-default`.

### When execution finding status changes (`open` → `resolved_locally`)
The finding item disappears from the EXECUTION FINDINGS section (it moves to the execution entry's own history). Section count badge updates.

---

## 12. Token Usage from Session 2

No new tokens introduced.

| Element | Token(s) |
|---|---|
| Shell, headers, items | Inherited from Session 6 |
| Execution status badge text | `--type-xs`, `--weight-bold` per state |
| `active` badge | `--state-success` |
| `paused` badge | `--state-warning` |
| `blocked` badge | `--state-danger` |
| `needs clarification` badge | `--state-warning` |
| `completed` badge | `--accent-primary-dim` |
| `returned to planning` badge | `--state-info` |
| `closed` dot | hollow, `--text-tertiary` |
| `received` badge | `--text-tertiary` |
| `launch auth pending` badge | `--state-pending` (`--state-warning`), `--weight-bold` |
| Return trigger header | `⚡`, `--state-danger` (arrived) / `--state-warning` (acknowledged) |
| Return trigger `unreviewed` badge | `--state-danger`, `--weight-bold` |
| Return trigger `reviewed — action pending` badge | `--state-warning` |
| Return trigger `returned to planning` badge | `--state-info` |
| Page `published` dot | `--state-success` |
| Page `draft` dot | `○` hollow, `--text-secondary` |
| Page `archived` dot | `--text-tertiary` dim |
| Decay `stale` marker | `⚠`, `--state-warning` |
| Decay `critical` marker | `⛔`, `--state-danger` |
| Finding `blocker` icon | `⛔`, `--state-blocked` |
| Finding `changed_condition` icon | `⚡`, `--state-warning` |
| Finding `decision_point` icon | `◈`, `--state-warning` |
| Finding `scope_gap` icon | `⚠`, `--state-warning` |
| Finding `quality_issue` icon | `ℹ`, `--state-info` |
| Decay alert inline banner | `--staleness-bg`, `--staleness-text` |
| Surface `active` dot | `--state-success` |
| Surface `paused` dot | `◐`, `--state-warning` |
| Surface `retired` dot | `--text-tertiary` dim |
| `[+N more]` expand affordance | `--text-link`, `--type-xs` |
| `✓ All entries closed` | `--state-success` |

---

## 13. What This Session Resolves

- The V Forge tree is fully specified with its own execution-state vocabulary — named status badges rather than colored dots, because execution state names carry precise operational meaning that color alone cannot communicate.
- The Session 7 return trigger dual-representation question is resolved: V Forge and Project V trees show the same trigger from their respective system perspectives. States are synchronized but expressed in system-appropriate vocabulary (`returned` on V Forge side; `routed` on Project V side). Neither tree implies ownership of the other side.
- The three-tree cross-system vocabulary contrast is now complete: lifecycle dots (Project V) / observatory posture indicators (VEDA) / execution state badges (V Forge). A developer or designer looking at all three trees simultaneously should see three visually distinct languages answering three distinct questions.
- Launch authorization pending state is surfaced in the nav tree with `◈` treatment and `launch auth pending` badge — visible without being an action. The authorization gate stays in the center workspace.
- The content graph section includes decay status markers (`⚠`/`⛔`) so the operator can see content health in the nav without needing to open individual page detail views.
- Return triggers float to the top of the V Forge tree when active — same rule as Project V, same governance rationale.
- All V Forge-specific absent-affordances are enumerated: no planning controls, no observatory controls, no inline route/dismiss, no self-authorization.
- Return trigger section uses navigation-only affordances — consistent with the Session 6 principle that the nav tree shows, it does not govern.

---

## 14. What This Session Does Not Resolve Yet

- **Center workspace V Forge detail views** — execution entry detail, content graph view, execution finding detail, surface detail, launch readiness review. All designed in Session 9 (shell foundation) and Sessions 13–15 (workflow surfaces).
- **Return trigger review view** — the response options (`Route`, `Dismiss`, maintenance vs replanning distinction) live in the center workspace; designed in Session 13.
- **Launch readiness review view** — the cross-system confirmation surface; designed in Session 14.
- **Content graph full view** — the nav shows a compact summary; the full graph with all pages, topics, entities, and link structure lives in the center workspace content graph view. This is Session 9+ territory.
- **Left nav collapse behavior** — still deferred from Session 6. Applies to all three trees equally; resolved in Session 22/23.

---

## 15. Recommended Inputs to Session 9

Session 9 is the Center Workspace Foundation. All three system trees are now specified. The center workspace is the surface that everything in the nav navigates to.

**What Session 9 inherits from Sessions 6–8:**

Every navigation affordance (`›`) in the three nav trees opens a detail view in the center workspace. Session 9 must specify:
1. The workspace router pattern — how records from the nav (and from right-panel output cards) route to the correct center view
2. The generic record detail view template — the base layout that all V Forge, Project V, and VEDA detail views share before being specialized
3. The tab bar or breadcrumb system — how the operator knows where they are in the center workspace and can navigate back
4. Cross-surface synchronization markers — how the center workspace shows an inline banner when a loaded record changes while it is being viewed

**Key constraint from the nav tree specs:**

The center workspace must handle record detail views for three very different record families:
- Project V: objectives, initiatives, work items, handoffs, decisions (lifecycle records)
- VEDA: signal packages, observatory domains, providers (observatory records)
- V Forge: execution entries, content graph pages/topics/entities, execution findings, surfaces (execution records)

Each family has a different density of information and different action affordances available. The generic record detail template must be flexible enough to accommodate all three without forcing any one family into an inappropriate layout.

**One design question for Session 9 to resolve:**

When the operator navigates to a record from the nav, should the center workspace open that record in a new tab (preserving what was already open) or replace the current view? Session 9 needs an explicit position on this. The answer affects how the tab bar or workspace header works and how the operator navigates between multiple open records. A "replace current" model is simpler but forces the operator to re-navigate if they want to compare two records. A "new tab" model is more powerful but adds complexity. Given the density of review work this application requires (comparing evidence against decisions against handoffs), a tab-based model is likely the right call — but Session 9 should commit to one pattern and specify it fully.
