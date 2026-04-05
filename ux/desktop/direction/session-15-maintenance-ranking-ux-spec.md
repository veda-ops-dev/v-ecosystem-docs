# Session 15 — Maintenance / Ranking UX
## V Ecosystem Desktop UX

**Session status:** Complete *(partial schema block — see §3 and throughout)*
**Depends on:** Sessions 1–14 (full shell backbone, gate surfaces, routing flow, notification system, handoff review, return trigger review, and launch readiness review all established)
**Required before:** Session 17 (Portfolio Triage / Dashboard) — the maintenance tracking surface establishes the per-project execution state vocabulary that portfolio triage will aggregate

---

## 1. Files Read

**Prior sessions:**
- `session-02-minimal-token-decisions.md` — active token baseline
- `session-06-left-nav-shell-project-v-tree-spec.md` — return triggers float to top; `Execution — Maintenance *` and `Replanning — In Progress *` stage labels; schema-pending `*` notation
- `session-08-left-nav-v-forge-tree-spec.md` — execution entry status badges; `returned to planning` state; content graph section with decay markers
- `session-09-center-workspace-foundation-spec.md` — generic record detail view template; section nav; tab model; inline banner position
- `session-13-handoff-review-ux-and-return-trigger-review-ux-spec.md` — maintenance vs replanning routing decision (§5.9); `Handle as maintenance` response with two confirmations; `Route to replanning` as Class B; schema block for downstream workflow
- `session-14-launch-readiness-ux-spec.md` — `Post-Launch — Active` state as re-entry point for maintenance; confirmation strip pattern (three dimensions, persistent across section tabs); schema block treatment throughout

**Doctrine:**
- `workflows/maintenance-and-replanning-workflow.md` — maintenance vs replanning distinction; six replanning stages; maintenance activity model; decision continuity principle; boundary integrity principle; replanning does not reset decision continuity; escalation when scope cannot be bounded
- `v-forge/operational-model.md` — execution states; bounded validation; execution-side research limits; return-to-planning trigger conditions; outcome honesty rule
- `v-forge/controlled-vocabularies.md` — `execution_entry_status` vocabulary; `content_decay_status` vocabulary; `maintenance_type` vocabulary
- `interfaces/desktop-surface-architecture.md` — center workspace role; action placement rules; what belongs in each surface
- `interfaces/desktop-state-and-context-model.md` — maintenance vs replanning posture visibility rule; stage names with schema-pending status
- `interfaces/desktop-invalidation-and-refresh-matrix.md` — EVENT-05 (approval written), EVENT-16 (return trigger), EVENT-17 (stage change) — most relevant during maintenance and replanning

---

## 2. Session 15 Scope Confirmation

The work plan defines Session 15 as: surfaces for ongoing execution tracking, replanning triggers, and project ranking.

This session produces:
- **Execution maintenance state tracking** — the center workspace surface for viewing V Forge active execution items and content graph summary during `Execution — Maintenance` posture
- **Replanning trigger visibility** — what the operator sees when a condition escalates from maintenance to replanning-warranted
- **Portfolio ranking controls** — relative priority signaling within Project V for multi-project or multi-initiative contexts
- **Return-to-planning routing controls** — where maintenance findings get escalated to replanning
- Schema block notation for `Execution — Maintenance` and `Replanning — In Progress` stages throughout
- Answers to the three open questions from Session 14 §19

This session does not:
- Design the portfolio triage dashboard (Session 17)
- Design the session start integrity check or notification system (Session 12 — done)
- Redesign the return trigger review view (Session 13 — done)
- Redesign the launch readiness review (Session 14 — done)
- Invent schema anchors for schema-blocked stages

---

## 3. Schema Block Status

| Stage name | Schema status | Derivation basis |
|---|---|---|
| `Execution — Maintenance` | **NO SCHEMA ANCHOR** | Derived from: execution entry in `active` state + no return trigger in `arrived`/`acknowledged` state + no trigger in `routed` state directing replanning |
| `Replanning — In Progress` | **NO SCHEMA ANCHOR** | Derived from: return trigger in `routed` state (subtype: replanning) + Project V operational posture still active for the relevant scope |

Both stages use `*` notation in all display contexts and `[SCHEMA PENDING]` tags where derivation fails. These constraints apply throughout this session without repeating them per element.

---

## 4. Session 14 Open Questions Resolved

**Question 1 — Portfolio ranking surface location:**

**Resolution: Portfolio ranking belongs in the center workspace as a multi-record comparative view, not in the left nav and not as a generic detail view.**

The generic record detail view template (Session 9) is single-record. Portfolio ranking is inherently comparative — the operator is assessing relative priority across multiple objectives, initiatives, or projects. This is a distinct view type: the **Ranking Surface**. It opens as a center workspace tab like any detail view, but its layout is a list/matrix rather than the section-nav template. This is designed in §7.

**Question 2 — Left nav during active replanning:**

**Resolution: When a return trigger is in `routed` state (replanning subtype), the Project V left nav RETURN TRIGGERS section does NOT disappear. Instead, it transitions from its arrival treatment to a replanning-in-progress treatment.**

During `arrived`/`acknowledged` state: the section header is `⚡ RETURN TRIGGERS` in `--state-danger`. After routing to replanning: the section header transitions to `◈ REPLANNING IN PROGRESS` in `--state-warning`. The trigger item itself updates its badge from `routed` to `replanning active`. This gives the operator a persistent left nav signal that replanning is in progress, not just that a trigger arrived.

This is a new nav section state not fully specified in Session 6. Session 6 only specified the section when triggers are `arrived` or `acknowledged`. This session adds the `replanning active` state. The section disappears only when replanning is resolved (trigger reaches `dismissed` equivalent or a revised handoff is activated).

**Question 3 — V Forge evidence access during maintenance:**

**Resolution: V Forge's ongoing evidence queries during maintenance cycles are surfaced in the Execution Entry detail view's History section as `evidence.query` activity trail entries (established in Session 14 §11), and in the Maintenance Activity log described in §5.3 of this session.**

The operator can see, in the maintenance tracking surface, that V Forge is operating with current VEDA signal rather than stale handoff-time evidence. The mechanism is the same `evidence.query` history entry format from Session 14 — applied here to maintenance-cycle evidence queries with the same V Forge attribution format.

---

## 5. Execution Maintenance State Tracking

### 5.1 What It Is

The execution maintenance tracking surface shows the operator what V Forge is doing within the current approved execution scope during `Execution — Maintenance` posture. It answers: is execution proceeding normally, what maintenance activities are in flight, and are there any conditions that might require escalation to replanning?

It is the center workspace detail view for an execution entry in `active` or `paused` state when the current posture is `Execution — Maintenance *`.

Opened by:
- Clicking an execution entry in the V Forge left nav tree
- Clicking `[View execution status ›]` from an execution finding item
- Clicking through from the session integrity view when maintenance-related items are surfaced

### 5.2 View Header

**Record type badge:** `EXEC ENTRY` — `--accent-primary` text (amber), 10% opacity bg per Session 9 record type identifier table

**Record title:** execution entry name, e.g., `hosting-comparison-site` — `--type-lg`, `--weight-semibold`, `--text-primary`

**Stage indicator:**
```
exec-07  ·  Execution — Maintenance *
```
`*` schema-pending notation. Tooltip: `Stage derived from workflow posture — no canonical record anchor.`

If derivation fails (the maintenance posture cannot be confidently determined):
```
exec-07  ·  [SCHEMA PENDING] Execution posture unavailable
```

**Execution status badge** (inline after stage, separated by `·`):

| `execution_entry_status` | Badge text | Color |
|---|---|---|
| `active` | `active` | `--state-success` |
| `paused` | `paused` | `--state-warning` |
| `blocked` | `blocked` | `--state-danger` |
| `completed` | `completed` | `--accent-primary-dim` |

### 5.3 Section Content: Overview

The Overview section establishes the current execution scope, what V Forge is doing, and whether anything requires operator attention.

**Execution scope block:**

```
CURRENT EXECUTION SCOPE
Executing within: hdl-07 — hosting-comparison-site
Approved scope:   Full site content build and publication, veda-domination.com
Scope status:     No scope excess detected

V Forge owns: execution truth for this scope
Project V owns: planning truth and governing decisions
VEDA owns: signal and observability
```

The ownership line block is carried forward from Sessions 13–14's "What does NOT transfer" pattern. It is present in the maintenance tracking surface because maintenance is the posture most susceptible to silent scope creep — V Forge continuing execution while quietly expanding what it's working on. The explicit ownership reminder is structural enforcement.

**Maintenance activity summary:**

```
ACTIVE MAINTENANCE ACTIVITIES                            [3 in progress]
────────────────────────────────────────────────────────────────────────
  content_refresh  ·  [page-14] Hosting comparison hub    in progress
  broken_link_repair  ·  3 external links identified      in progress
  content_update  ·  [page-22] Provider pricing tables    in progress
────────────────────────────────────────────────────────────────────────
```

- Section label: structural label pattern (`--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase, 0.3px letter-spacing)
- Count badge: `--text-tertiary`, `--type-xs`
- Per-activity row:
  - Maintenance type: `--font-mono`, `--type-xs`, `--text-tertiary` — from the `maintenance_type` controlled vocabulary (Session 15 source: `v-forge/controlled-vocabularies.md`)
  - `·` separator: `--text-tertiary`
  - Activity description: `--type-sm`, `--text-primary`
  - Status: `in progress`, `complete`, `blocked` — same color vocabulary as execution entry status badges
- Row height: 32px; padding `--space-3` (12px) horizontal

**Content graph health summary** (below the maintenance activities):

```
CONTENT GRAPH HEALTH
  [47 pages]  —  3 critical decay, 5 stale, 39 current
  [✓ No blocking gaps]    [⚠ 8 gaps total — 5 warning]
```

- Total pages, decay summary: `--type-sm`, `--text-primary`
- Decay breakdown: `critical` in `--state-danger`, `stale` in `--state-warning`, `current` in `--state-success`; all `--type-xs`
- Gap summary: `✓ No blocking` in `--state-success`; or `⛔ [N] blocking` in `--state-danger` when blocking gaps exist
- `[View full content graph ›]`: `--text-link`, `--type-xs` — navigates to the V Forge content graph view in a new tab

**V Forge evidence access status** (below content graph health):

```
EVIDENCE ACCESS STATUS — SOURCE: VEDA
  Last queried: 2026-04-03 07:20  ·  2 records current
  [obs-052] GA4 performance  ·  fresh  ·  queried 2026-04-03 07:20
  [obs-047] Keyword intent snapshot  ·  fresh  ·  queried 2026-04-02 14:31
```

This section answers the Session 14 open question: the operator can see that V Forge is operating with current VEDA signal. Format matches the execution-time evidence display from Session 14 §9 — record ID, record name, freshness status, query timestamp. If any queried record is stale or expired: `⚠ AGING` or `⛔ EXPIRED` markers per the evidence row vocabulary.

**Escalation threshold notice** (conditional — only when conditions approaching replanning trigger exist):

```
⚠ MAINTENANCE ESCALATION THRESHOLD APPROACHING
One or more maintenance findings may warrant replanning review.

[eval-15]  Pricing change — WP Engine — categorized as changed_condition
           Scope impact not yet determined.
           [Review finding ›]

Monitor these findings. If scope impact is confirmed, use Route to replanning.
```

Background: `--staleness-bg`; border-left: 3px `--staleness-border`; `border-radius: 0`
Header: `--type-sm`, `--weight-semibold`, `--staleness-text`
Finding row: `--font-mono` ID, `--type-xs`, `--text-tertiary`; description `--type-sm`, `--text-secondary`; `[Review finding ›]` `--text-link`, `--type-xs`

This notice is not a gate block. It is an ambient signal that the operator should monitor. The `[Review finding ›]` link routes to the execution finding detail in a new center workspace tab.

### 5.4 Section Content: Activity Log

The Activity Log section replaces the generic "History" section label for this surface. It is a chronological log of all maintenance activities within the current execution scope — both those in progress and those completed.

**Section label in section nav:** `Activity Log` (not `History` for this surface)

**Entry format:**

```
2026-04-03  07:20   Evidence queried from VEDA              [evidence.query]
                    Records: [obs-052], [obs-047]  ·  Token cost: 892 tokens

2026-04-03  08:15   Content refresh initiated — [page-14]  [maint-07]
                    Type: content_refresh  ·  In progress

2026-04-02  16:40   Broken link scan completed              [scan-03]
                    3 external links identified for repair.

2026-04-02  14:31   Evidence queried from VEDA              [evidence.query]
                    Records: [obs-047]  ·  Token cost: 341 tokens
```

The `evidence.query` entry format is consistent with Session 14 §11 — showing V Forge's ongoing VEDA evidence access during maintenance. Token cost shown in `--type-xs`, `--text-tertiary` as in Session 14.

**No `NON-CANONICAL` labels in the Activity Log.** Unlike the History section in Sessions 13–14, the Activity Log for maintenance contains only execution truth records — V Forge's own activity trail. LLM outputs that referenced maintenance activities are shown in the right panel's interaction area, not here.

### 5.5 Section Content: Actions

The Actions section for maintenance-state execution entries contains:

**Available governed actions:**

```
AVAILABLE ACTIONS

  [CLASS B]  Route finding to replanning        Via governed return-to-planning path
  [CLASS A]  View full execution report          Navigate to center workspace
  [CLASS A]  Copy execution entry ID             Immediate
```

**`Route finding to replanning`:**
This is a Class B action that escalates a specific maintenance finding to the replanning workflow. It is available when:
- An execution finding exists with type `changed_condition`, `decision_point`, or `scope_gap`
- The finding has not yet been routed

Clicking it routes the operator to the return trigger review view (Session 13) for the relevant finding. The routing decision (maintenance vs replanning) is made there — the Actions section provides the entry point, not the decision surface.

**No gate widget for the maintenance tracking surface itself.** The maintenance tracking surface is a view surface, not an approval gate surface. Approvals happen when specific Class B or C actions are taken (e.g., routing a finding to replanning, which requires the Session 13 Class B gate). The Actions section surfaces the available paths without embedding a gate widget directly.

---

## 6. Replanning Trigger Visibility Surface

### 6.1 What It Is

When a return trigger is routed to replanning (Session 13 — `Route to replanning` response, approved via Class B gate), the ecosystem enters `Replanning — In Progress *` posture. The replanning trigger visibility surface is the center workspace view that shows the operator where they are in the replanning process and what decisions are under reconsideration.

This surface is the Project V perspective on the replanning event — distinct from the V Forge execution tracking surface (§5). It is opened from:
- The left nav `◈ REPLANNING IN PROGRESS` section (Session 15 §4 resolution)
- The context strip STAGE row when stage shows `Replanning — In Progress *`
- The session integrity view if a replanning event is surfaced there

### 6.2 View Header

**Record type badge:** `REPLANNING` — `--state-warning` text, 10% opacity bg, `--type-xs`, `--weight-bold`

**Record title:** e.g., `content-hub-v1 — replanning` — `--type-lg`, `--weight-semibold`, `--text-primary`

**Stage indicator:**
```
replan-04  ·  Replanning — In Progress *
```
Schema-pending `*` with tooltip.

### 6.3 Non-authority Notice Banner

The same pattern as the return trigger review surface (Session 13 §5.3), adapted for the replanning context. Non-dismissible while replanning is active.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ℹ REPLANNING IN PROGRESS — GOVERNED RECONSIDERATION                     │
│                                                                           │
│  Prior governing decisions are under bounded reconsideration.             │
│  Decision continuity is preserved — this is not a planning reset.        │
│  Only decisions affected by the trigger are in scope for reconsideration. │
│  V Forge retains execution truth. VEDA retains observatory truth.         │
└──────────────────────────────────────────────────────────────────────────┘
```

Background: `--state-info-bg`; border-left: 3px `--state-info`; non-dismissible.

This banner enforces the central doctrine of the maintenance and replanning workflow: "Replanning does not reset decision continuity. Replanning does not erase who owns what." The operator should never mistake a replanning event for a clean slate.

### 6.4 Section Content: Overview

**Trigger context block:**

```
REPLANNING TRIGGER
  Trigger:      rtn-04 — Intent shift — hosting comparison
  Routed from:  V Forge execution — exec-07
  Routing date: 2026-04-03 09:47
  Routing class: Class B (approved)  ·  Approval: arp-05

What triggered this:
  V Forge found that the primary hosting provider changed pricing structure
  during execution, affecting the accuracy of the comparison scope.

What V Forge continues to own:
  Execution truth for work completed to this point.
  Partial content graph ([page-14] through [page-22]).
  V Forge does not transfer this to planning.
```

The "What V Forge continues to own" block is required. The replanning surface must make clear that routing a finding to planning does not dissolve V Forge's execution ownership.

**Prior decision context block** (the most important block on this surface):

```
PRIOR DECISION CONTEXT — WHAT WAS DECIDED BEFORE THIS REPLANNING EVENT
────────────────────────────────────────────────────────────────────────
  [dec-03]  Prioritize search-first content         [active — being reviewed]
  [dec-07]  Hosting vertical — revised scope         [active — being reviewed]
  [dec-05]  Hosting vertical over SaaS tier          [superseded by dec-07 — not in scope]
────────────────────────────────────────────────────────────────────────
  Decisions marked [active — being reviewed] are under bounded reconsideration.
  Decisions not listed here are NOT reopened by this replanning event.
```

- `PRIOR DECISION CONTEXT` label: structural label pattern
- Decision rows: same format as Sessions 13–14 Decisions sections
- `[active — being reviewed]`: `--state-warning` text — these decisions are the subject of reconsideration
- `[superseded — not in scope]`: `--text-tertiary` — explicitly excluded from reconsideration
- Footer note: `--type-xs`, `--text-secondary`

**Why this block is required:** The maintenance and replanning workflow doctrine states: "Replanning must not reset prior decision context. The ecosystem must know what it previously decided before it decides what to do differently." The Prior Decision Context block is the UI implementation of this requirement. The operator sees exactly which decisions are under review and which are not.

**Replanning scope block:**

```
REPLANNING SCOPE
What is in scope for reconsideration:
  • The hosting provider selection assumptions underlying dec-07
  • The competitive positioning basis for the hosting comparison content

What is NOT in scope:
  • The search-first strategy (dec-03) — not affected by provider pricing
  • The overall content hub objective — remains valid
  • Work already completed in execution — [page-14] through [page-22]

Scope was bounded by: Operator routing decision — rtn-04
```

"What is in scope" bullets: `--type-sm`, `--text-primary`; `•` in `--accent-primary`
"What is NOT in scope" bullets: `--type-sm`, `--text-secondary`; `•` in `--text-tertiary`

### 6.5 Section Content: Evidence

The Evidence section for replanning shows the evidence that triggered the replanning event plus currently loaded VEDA signal.

**Trigger evidence block** (same format as Session 13 §5.5 execution-side finding evidence):

```
TRIGGER EVIDENCE — SOURCE: V FORGE FINDING
  [exec-ev-04]  WP Engine pricing page — captured 2026-04-01 07:50
                Type: Execution finding artifact  ·  Trust: high
                NOT a VEDA signal record
```

**Current VEDA signal block** (same format as Session 13 §5.5 VEDA signal sub-section):

```
CURRENT VEDA SIGNAL — SOURCE: VEDA (referenced, not owned by Project V)
  [obs-047]  Hosting keyword intent snapshot    fresh — 2026-04-01 14:32
  [obs-052]  GA4 performance — content-hub      fresh — 2026-04-03 07:20  [v-forge queried]
```

The `[v-forge queried]` annotation: `--type-xs`, `--state-info` text — indicates that V Forge queried this record during execution via the evidence access contract, providing additional context about the signal's relevance to the execution scope.

### 6.6 Section Content: Actions

The Actions section for the replanning surface contains the replanning response controls.

**Replanning response options** (direct descendants of the return trigger response model from Session 13):

```
REPLANNING ACTIONS

  What needs to happen next?

  [○ / ●]  Revise governing decision
  [○ / ●]  Reaffirm governing decision (no change needed)
  [○ / ●]  Defer reconsideration
  [○ / ●]  Escalate — scope too broad for bounded replanning

──────────────────────────────────────────────────────────

[Selected option expanded content — see §6.7]

──────────────────────────────────────────────────────────

[Confirm Replanning Response]
```

Same radio button metaphor as Session 13 §5.8. All options start unselected. `[Confirm Replanning Response]` inactive until selection is made.

### 6.7 Replanning Response Options — Expanded Content

**Option 1 — Revise governing decision**

When selected:

```
●  Revise governing decision

   This replanning event warrants a revision to one or more governing decisions.

   Which decisions to revise:
   ☑ [dec-07] Hosting vertical — revised scope
   ☐ [dec-03] Prioritize search-first content

   Revision requires Class B approval.
   The revision will create a new governing decision that supersedes or
   updates the selected decision(s).
   Decision continuity will be preserved — prior decisions will be marked
   revised, not deleted.

   [Confirm and proceed to approval gate]
```

Checkboxes for each "being reviewed" decision — the operator selects which decisions to revise. At least one must be checked before `[Confirm and proceed to approval gate]` activates.

`[Confirm and proceed to approval gate]`: `--border-accent`, `--accent-primary` text — routing CTA style. Class B gate for the decision revision action.

**Option 2 — Reaffirm governing decision (no change needed)**

When selected:

```
●  Reaffirm governing decision (no change needed)

   After reviewing the trigger and prior decisions, the governing decisions
   remain valid. No revisions are required.

   The replanning event is resolved by this reaffirmation.
   Reaffirmation is logged as a governance-relevant fact.

   Reaffirmation statement:
   The prior governing decisions for this scope remain valid despite the
   execution finding. No replanning action is required.

   [Confirm Reaffirmation]
```

`[Confirm Reaffirmation]`: standard button, `--surface-elevated`, `--border-default`. Writes the reaffirmation record. Resolves the replanning event. The replanning stage transitions back to the appropriate execution posture.

**Option 3 — Defer reconsideration**

When selected:

```
●  Defer reconsideration

   The replanning event is acknowledged but reconsideration is deferred.

   Reason (required):
   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   └──────────────────────────────────────────────────────────────────────┘

   A deferred replanning event remains open in the session integrity view.
   [Confirm Defer]
```

Same reason requirement as return trigger dismissal (Session 13) — minimum 10 characters.

**Option 4 — Escalate — scope too broad for bounded replanning**

When selected:

```
●  Escalate — scope too broad for bounded replanning

   The replanning scope cannot be bounded without reopening so many prior
   governing decisions that the reconsideration would effectively become
   a new planning baseline.

   Per doctrine: this condition requires escalation rather than replanning.
   This is a Class D condition.

   [Proceed to Escalation]
```

`[Proceed to Escalation]`: opens the Class D escalation path from Session 10 §7. This is the direct implementation of the maintenance and replanning workflow doctrine: "A replanning event that requires dissolving all prior governing decisions is not replanning — it is a new planning cycle that requires human review and governed approval before proceeding as such."

### 6.8 Replanning Resolution — Nav and Stage Updates

**When replanning is resolved** (reaffirmation confirmed, revision approved, or deferral with reason):

- Left nav Project V tree: `◈ REPLANNING IN PROGRESS` section transitions to `[RESOLVED]` state for a brief session-duration display, then disappears from the tree
- Context strip STAGE row: updates to the post-replanning stage (e.g., `Planning — Active`, or `Handoff — Prepared` if a revised handoff was produced)
- Topbar stage indicator: updates
- Toast: `Replanning resolved — [replan-id]. [Action taken — e.g., Decision revised / Reaffirmed].` — success type

---

## 7. Portfolio Ranking Surface

### 7.1 What It Is

The portfolio ranking surface is a multi-record comparative view in the center workspace. It allows the operator to see relative priority across objectives, initiatives, or projects and signal adjustments to that priority.

It is the implementation of "portfolio ranking controls — relative priority signaling within Project V" from the work plan.

It opens as a center workspace tab (per the Session 9 tab model) but uses a **list/matrix layout** instead of the generic record detail view template. The tab label is: `[RANKING]  Portfolio ranking  ×`

Opened by:
- A dedicated `[Portfolio ranking ›]` link in the left nav footer area (below the standard nav tree, above the `+ New…` footer)
- A command palette action (Session 21 territory for the command itself; the view is designed here)

### 7.2 Layout

The portfolio ranking surface fills the center workspace width. It does not use the section nav pattern — it is a single-view layout without tabs.

```
┌────────────────────────────────────────────────────────────────────────────┐
│  VIEW HEADER: [RANKING]  Portfolio ranking                                 │
├────────────────────────────────────────────────────────────────────────────┤
│  SCOPE FILTER:  [Objectives ▾]  [All statuses ▾]  [Current project ▾]    │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  RANKED LIST (drag-reorder or relative signal buttons)                     │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Scope Filter Bar

The filter bar (40px, `--surface-raised`, `--border-bottom --border-subtle`) contains three filter dropdowns:

**Record type selector:** `[Objectives ▾]` / `[Initiatives ▾]` / `[Work Items ▾]` — determines what level is being ranked. Only one level at a time. Default: Objectives.

**Status filter:** `[All statuses ▾]` or specific status values — filters to only `active` items by default (no value in ranking `proposed` or `closed` items). Options: `all`, `active`, `blocked`, `ready`.

**Scope filter:** `[Current project ▾]` — the current session's project. This filter exists because Session 9 established that the session is scoped to one project; this is a reminder that ranking is within the current project scope.

### 7.4 Ranked List

Each record appears as a ranked row. Rows are ordered by current priority signal (highest priority at top).

**Row anatomy:**

```
[rank #]  [drag handle ≡]  [status dot]  [record title]          [priority signal]  [›]
                                          [brief description]
```

- Rank number: `--font-mono`, `--type-xs`, `--text-tertiary`, right-padded to 3 characters (` 1.`, ` 2.`, `10.`)
- Drag handle `≡`: `--text-tertiary`, visible on hover; dragging to reorder is the primary ranking interaction
- Status dot: per Session 6 status vocabulary
- Record title: `--type-sm`, `--text-primary`, `--weight-medium`
- Brief description: `--type-xs`, `--text-secondary`, one line, truncated
- Priority signal: see §7.5
- `›`: navigation to record detail, visible on hover

**Row height:** 48px (taller than standard tree items to accommodate brief description line)
**Row divider:** `--border-subtle` 1px between rows

### 7.5 Priority Signal Controls

Priority signal is the operator's relative priority statement — not an absolute score, not a business metric, but a direction signal: "this should come before that."

**Priority signal display per row:**

```
[▲]  [Priority signal label]  [▼]
```

- `[▲]` up arrow: increase priority (move row up)
- `[▼]` down arrow: decrease priority (move row down)
- Priority signal label: `--type-xs`, colored by current priority level

**Priority signal levels** (not tied to backend schema — this is a runtime UI signal that informs planning posture):

| Signal | Label | Color |
|---|---|---|
| Urgent — top priority | `urgent` | `--state-danger` |
| High priority | `high` | `--state-warning` |
| Normal | `normal` | `--text-secondary` |
| Low priority | `low` | `--text-tertiary` |
| On hold | `on hold` | `--text-tertiary` (italic) |

**Important constraint:** The priority signal is **not a mutation of governed records.** It is a planning posture signal — a statement the operator is making about relative priority that informs LLM outputs and can be cited in recommendations. It is not a `Class B` action. It is `Class A` — it changes a local priority signal that the LLM and planning tools can reference, but it does not activate any governed transition without going through the governed command path.

This must be made explicit in the ranking surface with a non-dismissible note below the filter bar:

```
ℹ Priority signals inform planning posture. They do not activate governed transitions.
  Use the governed command path to change record status or create decision records.
```

`--type-xs`, `--text-tertiary`. Non-dismissible. No background color — it is ambient footer text, not a warning.

### 7.6 Drag-to-Reorder

The primary ranking interaction is drag-and-drop reordering of rows. The drag handle `≡` is the affordance.

**Drag behavior:**
- Pick up: row lifts slightly with `--elevation-overlay` shadow; background `--surface-elevated`; `cursor: grabbing`
- In-flight: a placeholder row (dashed `--border-subtle` outline) shows where the row will land; the dragged row follows the cursor
- Drop: row lands; rank numbers update immediately for all affected rows; the priority signal labels update based on position
- Transition: `--transition-default` (200ms ease) for surrounding rows shifting to accommodate the drag

**`[▲]` / `[▼]` controls** are the keyboard/accessibility alternative to drag. Each click moves the row one position up or down.

---

## 8. Return-to-Planning Routing Controls

### 8.1 Where They Live

Return-to-planning routing controls are not a separate surface — they are the Actions section affordances on specific record types that enable the operator to escalate maintenance findings toward replanning. This was partially designed in Session 13 (the return trigger review view's response options). Session 15 adds the escalation path from the maintenance tracking surface itself (§5.5 — `Route finding to replanning` Class B action).

### 8.2 Escalation Path from Maintenance to Replanning

When the operator clicks `[Route finding to replanning]` in the maintenance tracking surface Actions section:

1. The workspace router opens the relevant execution finding in a new center tab with `intent = 'approval_gate'`
2. The execution finding detail shows the finding in `open` status with the response options from Session 13 §5.8 pre-scoped to the replanning option
3. The operator confirms `Route to replanning` as their response
4. The Class B gate activates after review checkpoints are satisfied
5. The approval event writes the routing record
6. The execution entry's posture transitions from `Execution — Maintenance *` to `Replanning — In Progress *`
7. The left nav Project V tree: RETURN TRIGGERS section updates to `◈ REPLANNING IN PROGRESS` per Session 15 §4

The routing path from maintenance tracking to replanning uses the same five-step routing flow from Session 11 applied to the execution finding record. No new routing mechanism is needed — the existing patterns cover it.

### 8.3 What Cannot Be Shortcut

**The operator cannot mark a maintenance finding as replanning-worthy without going through the return trigger review view.** The `Route finding to replanning` action in §5.5 routes to the review view; it does not directly write a replanning record. This enforces the Session 13 design principle: the response decision (maintenance vs replanning) belongs in the return trigger review view, not in an inline action.

**The maintenance tracking surface cannot approve a replanning response.** It can initiate the path. It cannot complete the gate.

---

## 9. Schema Block Summary

All schema-pending elements in this session use `*` notation in display and `[SCHEMA PENDING]` tags when derivation fails. For completeness:

| Element | Schema status | Treatment |
|---|---|---|
| `Execution — Maintenance` stage name | No record anchor | `*` suffix, tooltip, `[SCHEMA PENDING]` on derivation failure |
| `Replanning — In Progress` stage name | No record anchor | Same |
| `Replanning — In Progress` tracking record (`replan-04` etc.) | No `ReplanningRecord` schema | Record ID displayed if available from session context; `[SCHEMA PENDING]` if not derivable |
| Priority signal levels in ranking surface | Not tied to backend schema | No `*` needed — explicitly stated as runtime UI signal, not a governed record field |

---

## 10. Token Usage from Session 2

No new tokens introduced.

| Element | Token(s) |
|---|---|
| `EXEC ENTRY` record type badge | `--accent-primary` text, 10% opacity bg, `--type-xs`, `--weight-bold` |
| `REPLANNING` record type badge | `--state-warning` text, 10% opacity bg, `--type-xs`, `--weight-bold` |
| `[RANKING]` tab label | `--text-tertiary` text, `--surface-raised` bg |
| Stage `*` notation | `--text-tertiary`, `--type-xs` |
| `[SCHEMA PENDING]` tag | `--schema-pending-bg` fill, `--state-schema-hold` text, `--radius-sm`, `--type-xs` |
| Escalation threshold notice | `--staleness-bg`, `--staleness-border` (3px left), `--staleness-text` |
| Non-authority banner (replanning) | `--state-info-bg`, 3px `--state-info` left, `--state-info` header |
| Prior decision `[active — being reviewed]` | `--state-warning` text |
| Prior decision `[superseded — not in scope]` | `--text-tertiary` |
| "In scope" bullets | `--type-sm`, `--text-primary`; `•` in `--accent-primary` |
| "NOT in scope" bullets | `--type-sm`, `--text-secondary`; `•` in `--text-tertiary` |
| Maintenance type label | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Activity log `evidence.query` entry | Same format as Session 14 §11 |
| Token cost in Activity Log | `--type-xs`, `--text-tertiary` |
| `[v-forge queried]` annotation | `--type-xs`, `--state-info` text |
| `◈ REPLANNING IN PROGRESS` nav section header | `--state-warning`, `--type-xs`, `--weight-semibold` |
| Rank number | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Drag handle `≡` | `--text-tertiary`, hover-visible |
| Row lifted state (drag) | `--elevation-overlay` shadow, `--surface-elevated` bg |
| Row placeholder (drag in-flight) | dashed `--border-subtle` outline |
| Priority signal `urgent` | `--state-danger`, `--type-xs` |
| Priority signal `high` | `--state-warning`, `--type-xs` |
| Priority signal `normal` | `--text-secondary`, `--type-xs` |
| Priority signal `low` / `on hold` | `--text-tertiary`, `--type-xs` |
| `[▲]` / `[▼]` controls | `--text-tertiary`, transitions to `--text-secondary` on hover |
| Ranking note (priority signals inform posture) | `--type-xs`, `--text-tertiary` |
| Filter bar | `--surface-raised`, 40px, `--border-subtle` bottom |
| Filter dropdown text | `--type-xs`, `--text-secondary` |

---

## 11. What Session 15 Resolves

- The execution maintenance tracking surface is fully specified: Overview with scope block, maintenance activity summary, content graph health summary, V Forge evidence access status, and escalation threshold notice; Activity Log replacing generic History; Actions with `Route finding to replanning` as the escalation entry point.
- The replanning trigger visibility surface is fully specified: overview with trigger context, prior decision context (the most important block — showing exactly which decisions are under review and which are not), and replanning scope; four response options with expanded content; the escalation option for when replanning scope is too broad.
- All three open questions from Session 14 are resolved: portfolio ranking in center workspace (§4/§7), left nav replanning-in-progress state transition (§4), V Forge evidence access visibility during maintenance (§5.3/§5.4).
- The `◈ REPLANNING IN PROGRESS` left nav section state is specified — the state that Project V's left nav enters after a return trigger is routed to replanning, filling the gap from Session 6 which only specified `arrived`/`acknowledged` states.
- The portfolio ranking surface is designed as a distinct view type (list/matrix, not the generic section-nav template) with drag-to-reorder and priority signal controls, with the explicit constraint that priority signals are Class A — they inform planning posture but do not activate governed transitions.
- The escalation path from maintenance to replanning uses the existing five-step routing flow (Session 11) applied to execution finding records — no new routing mechanism required.
- The "Replanning does not reset decision continuity" doctrine is implemented as a design constraint: the Prior Decision Context block and the "NOT in scope" list make the operator explicitly aware of what is and is not being reconsidered.
- Schema block notation is applied correctly throughout: `*` for derivable but schema-pending stages, `[SCHEMA PENDING]` for derivation failures, and explicit flagging of the priority signal levels as runtime UI signals rather than governed record fields.

---

## 12. What Session 15 Does Not Resolve Yet

- **Session 16 — Intake UX** — blocked on IntakeRecord schema. Not started.
- **Session 17 — Portfolio Triage / Dashboard** — the portfolio ranking surface designed here (single-project, within-project ranking) is the foundation. Session 17 extends it to multi-project aggregate views with cross-project attention badges. The priority signal vocabulary from §7.5 is a stable input.
- **The post-replanning handoff surface** — when replanning results in a revised handoff being prepared, the operator is back in Session 13 territory (Handoff Package Review View). The replanning event is the trigger; the resulting handoff review surface is already designed. No new surface is needed here.
- **Replanning record schema** — the `replan-04` style record ID in the replanning tracking surface is displayed when available from session context. When the ReplanningRecord schema is eventually defined, the record ID field will be backed by a canonical record. Until then, it is derived from session context or omitted. This is a future implementation concern, not a design concern.
- **Content graph full view** — referenced in §5.3 (`[View full content graph ›]`). The full content graph view with all pages, topics, entities, and links is a distinct center workspace view type that has been referenced across Sessions 8, 9, and 15 without being fully designed. It warrants its own design pass — likely absorbed into Session 17 or 18 as part of the power features tier.
- **Decision revision flow** — when the operator confirms `Revise governing decision` in §6.7 and clicks `[Confirm and proceed to approval gate]`, they enter a decision revision workflow. The specific center workspace view for creating or revising a governing decision is not designed in this session. It would use the generic record detail view template from Session 9 with decision-specific section content. This is a future workflow surface.

---

## 13. Recommended Inputs to Session 17

Session 16 (Intake UX) is blocked. Session 17 is Portfolio Triage / Dashboard — the first TIER 5 Power Feature.

**What Session 17 inherits from Session 15:**
- The portfolio ranking surface (§7) is the single-project foundation. Session 17 extends it with multi-project views, cross-project attention badges, and aggregate status indicators.
- The priority signal vocabulary (`urgent`, `high`, `normal`, `low`, `on hold`) from §7.5 is a stable input for the portfolio triage view.
- The confirmation strip pattern from Session 14 (three dimensions, persistent across section tabs) is available as a multi-dimension status summary pattern for portfolio-level views.
- The execution tracking surface (§5) establishes what per-project execution status looks like. Session 17 will need to aggregate this across multiple projects.

**Key design questions for Session 17:**

How does the portfolio triage view handle the multi-project display at different workflow stages simultaneously? One project might be `Planning — Active`, another `Execution — Maintenance *`, another `Replanning — In Progress *`. The triage view needs to display these heterogeneous stage states without visual noise or false equivalence between schema-anchored and schema-pending stages.

What triggers the portfolio triage view to surface a project as requiring attention? The single-project surfaces use topbar attention badges and context strip INTEGRITY rows. The portfolio view needs its own cross-project attention signal — something that tells the operator "project X has unresolved integrity items that warrant your attention today" without requiring them to individually open each project.

Should the portfolio triage view be session-scoped (one project at a time, per the session token model) or can it present multiple projects in a read-only aggregate mode? The session token model (Sessions 3, 5) scopes the session to one project — approval gates and LLM interactions are project-specific. The portfolio view may be able to show read-only aggregate state across projects without being scoped to one, as long as it does not enable governed actions for out-of-scope projects. Session 17 should take an explicit position on this.
