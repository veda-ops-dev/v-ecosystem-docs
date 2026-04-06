# Session 14 — Launch Readiness UX
## V Ecosystem Desktop UX

**Session status:** Complete *(partial schema block — see §3 and throughout)*
**Depends on:** Sessions 1–13 + Session 13 Addendum (all shell, gate, routing, notification, and workflow surfaces established; Session 13 addendum incorporated evidence access contract metadata)
**Required before:** Session 15 (Maintenance / Ranking UX) — the launch readiness surface establishes the cross-system confirmation checklist pattern and the `Post-Launch — Active` state transition that Session 15's maintenance tracking picks up from

---

## 1. Files Read

**Prior sessions:**
- `session-02-minimal-token-decisions.md` — active token baseline
- `session-08-left-nav-v-forge-tree-spec.md` — `launch auth pending` badge treatment in V Forge tree; `◈` glyph for launch authorization pending state
- `session-09-center-workspace-foundation-spec.md` — generic record detail view template; section nav; inline banner position; record type identifiers
- `session-10-approval-gate-surfaces-spec.md` — Class C modal gate; typed confirmation; `[Proceed Without Refreshing — I Accept the Risk]` path (acknowledged-on-stale-evidence logging); checkpoint model for launch readiness
- `session-11-review-to-gate-routing-flow-spec.md` — five-step routing flow; `[Proceed to Authorization Gate]` button; Class C modal relationship to center surface
- `session-12-session-integrity-check-and-alert-notification-system-spec.md` — EVENT-05, EVENT-08, EVENT-17 surface mappings for the launch context
- `session-13-handoff-review-ux-and-return-trigger-review-ux-spec.md` — stale-basis warning pattern; "What does NOT transfer/change" block pattern; evidence row format
- `session-13-addendum-new-doctrine-integration.md` — evidence access contract metadata fields (`freshness_status` with `expired` value; `gathered_at`; `source_provider`; `trust_classification`); `expired` = absolute gate block

**Doctrine:**
- `interfaces/desktop-surface-architecture.md` — Launch Readiness Review View required content; cross-system confirmation requirement; evidence currency for launch; post-launch state transition
- `interfaces/desktop-governance-and-gating-model.md` — Class C gate requirements; typed confirmation; approval scope must cover current specific scope; `Proceed Without Refreshing` logging
- `interfaces/desktop-state-and-context-model.md` — launch readiness stage names; all four are schema-pending (`Launch Readiness — In Progress`, `Launch Readiness — Blocked`, `Launch Authorization — Pending`, `Post-Launch — Active`); evidence currency requirement; `Proceed Without Refreshing` path explicitly defined
- `interfaces/desktop-invalidation-and-refresh-matrix.md` — EVENT-05 (approval written), EVENT-08 (evidence stale), EVENT-17 (stage change) — the three events most likely during launch review
- `interfaces/v-forge-evidence-access-contract.md` — evidence freshness metadata; `expired` status; degraded-mode behavior
- `interfaces/project-v-to-v-forge-handoff-interface.md` — what a valid handoff transfers; planning ownership stays with Project V after handoff

**Workflows:**
- `workflows/launch-readiness-workflow.md` — seven stages; three confirmation dimensions; cross-system confirmation requirement; blocking conditions; scope integrity principle; Evidence Currency Principle (conservative threshold for launch); external action principle; `[Proceed Without Refreshing]` path explicitly described

---

## 2. Session 14 Scope Confirmation

The work plan defines Session 14 as: the launch readiness review surface, with partial schema block notation where required.

This session produces:
- The complete Launch Readiness Review View: all section tabs, all section content
- The three-dimension cross-system confirmation checklist — the surface's primary structural differentiator
- The blocking conditions panel
- Evidence currency treatment specific to launch-sensitive decisions
- The `[Proceed Without Refreshing — I Accept the Risk]` path and its acknowledgment logging
- The `[SCHEMA PENDING]` notation for all four launch readiness stage names
- The `Launch Authorization — Pending` Class C gate widget positioning and activation
- The post-launch state transition treatment in the center surface
- Token usage from Session 2

This session does not:
- Redesign the Class C gate widget (Session 10)
- Redesign the routing flow (Session 11)
- Design the maintenance tracking surface (Session 15)
- Invent schema anchors for the four launch readiness stages
- Design the post-launch observation workflow surface (future session)

---

## 3. Schema Block Status — All Four Launch Readiness Stages

All four launch readiness stage names have no settled schema record anchor. This must be made explicit before any design decision is made.

| Stage name | Schema status | Derivation basis if available |
|---|---|---|
| `Launch Readiness — In Progress` | **NO SCHEMA ANCHOR** | Derived from: execution entry in `active` state + launch readiness evaluation record exists + cross-system confirmation not yet complete |
| `Launch Readiness — Blocked` | **NO SCHEMA ANCHOR** | Derived from: same as above + at least one blocking condition is active |
| `Launch Authorization — Pending` | **NO SCHEMA ANCHOR** | Derived from: all three confirmation dimensions satisfied + approval record for launch action exists in `pending` state in approval store |
| `Post-Launch — Active` | **NO SCHEMA ANCHOR** | Derived from: launch authorization approval written + launch-sensitive execution completed + VEDA observatory active for launched scope |

**What this means for the surface:** Where the stage cannot be confidently derived from available context, the stage indicator shows `Launch Readiness — In Progress *` with the schema-pending `*` notation from Sessions 3 and 4, or shows `Unavailable` with the `[SCHEMA PENDING]` tag if derivation fails entirely. The surface must not claim a stage label it cannot back with record evidence.

**What this does NOT mean:** The surface can still be fully designed. The review content (planning-side readiness, evidence, execution verification) does not depend on the stage label being schema-anchored. The three-dimension checklist, the blocking conditions panel, and the Class C gate are all designable. The `[SCHEMA PENDING]` notation is applied surgically to the stage display fields, not to the entire surface.

---

## 4. What This Surface Is

The Launch Readiness Review View is the center workspace surface where the operator reviews the full cross-system launch readiness picture before seeking Class C launch authorization.

It is the most governance-intensive review surface in the application. It requires:
- Planning-side readiness confirmation (Project V)
- Evidence and signal currency confirmation (VEDA)
- Execution-side verification completion (V Forge)

All three must be satisfied simultaneously before the Class C authorization gate is available. Any single system's self-certification alone is explicitly insufficient — the surface architecture doctrine states: "A self-certification from any single system is not a governed cross-system confirmation."

This surface is opened by:
- Clicking an execution entry in `launch auth pending` state in the V Forge left nav tree
- Clicking `[Go to approval gate ›]` in the session integrity view for a pending launch authorization
- Clicking `[Proceed to Approval Gate]` on an ARP card in the right panel that packages a launch action

---

## 5. View Header

**Record type badge:** `LAUNCH READINESS` — `--state-info` text (blue — this is a cross-system confirmation surface, not a single-system handoff), 10% opacity bg, `--type-xs`, `--weight-bold`

**Record title:** e.g., `content-hub-v1 — launch readiness` — `--type-lg`, `--weight-semibold`, `--text-primary`

**Record ID:** execution entry reference, e.g., `exec-07` — `--font-mono`, `--type-xs`, `--text-tertiary`

**Stage indicator** (inline with record ID, separated by `·`):
```
exec-07  ·  Launch Authorization — Pending *
```
`*` in `--type-xs`, `--text-tertiary` — the schema-pending notation. Tooltip: `Stage derived from workflow posture — no canonical record anchor.`

If derivation fails:
```
exec-07  ·  [SCHEMA PENDING] Stage unavailable
```
`[SCHEMA PENDING]` tag: `--schema-pending-bg` fill, `--state-schema-hold` text, `--radius-sm`, `--type-xs`.

---

## 6. Evidence Currency Warning Banner

Before any section content is rendered, the surface checks whether evidence supporting the launch readiness determination is current. This check is more stringent than the handoff stale-basis check (Session 13 §4.3) because of the Evidence Currency Principle: evidence must be "current enough to be honest" for launch-sensitive decisions, applied conservatively.

**Three evidence currency states for the inline banner position:**

### State A — All evidence current

No banner. The view body renders normally. A subtle `✓ Evidence basis current` indicator appears in the Evidence section header (not the banner position).

### State B — Evidence aging or stale (not expired)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ⚠ EVIDENCE BASIS MAY NOT MEET LAUNCH CURRENCY THRESHOLD                  │
│                                                                           │
│  Evidence record:  [obs-041] SERP delta — hosting vertical               │
│  Status:           Stale — 6 days old                                    │
│  Significance:     This record supported the planning-side readiness       │
│                    determination. Stale evidence at launch carries higher   │
│                    governance cost than in ordinary planning contexts.      │
│                                                                           │
│  [Refresh Evidence]    [Proceed Without Refreshing — I Accept the Risk]  │
└──────────────────────────────────────────────────────────────────────────┘
```

Background: `--staleness-bg`
Border-left: 3px `--staleness-border`; `border-radius: 0`
Header: `--type-sm`, `--weight-semibold`, `--staleness-text`
Field labels: `--type-xs`, `--weight-semibold`, `--text-tertiary`, 120px min-width, right-aligned
Field values: `--type-sm`, `--text-primary`

`[Refresh Evidence]`: standard refresh link, `--text-link`, `--type-sm`. Triggers evidence reload from VEDA. On success, banner dismisses and the Evidence section updates with new records.

**`[Proceed Without Refreshing — I Accept the Risk]`:**
- Width: 300px
- Height: 32px
- Background: `--surface-raised`
- Border: 1px `--state-warning`
- Text: `--state-warning`, `--type-sm`, `--weight-medium`
- Border-radius: `--radius-md`
- Hover: `--state-warning-bg`

Clicking this opens a mandatory acknowledgment prompt inline below the button (not a modal):

```
You are proceeding with launch authorization on stale evidence.
This is a governance-relevant fact and will be logged.

Acknowledgment statement:
┌─────────────────────────────────────────────────────────────────────────┐
│ I acknowledge that [obs-041] is stale and that I am proceeding with      │
│ launch authorization without refreshing it. I accept this risk.          │
└─────────────────────────────────────────────────────────────────────────┘

[Confirm — Log This Acknowledgment]    [Cancel — I'll refresh instead]
```

The acknowledgment statement is pre-populated with the specific record ID(s) and the specific action (launch authorization). The operator cannot edit the statement — it is a read-only attestation that names the exact records and the action. `[Confirm]` logs the acknowledgment record (persisted: session ID, operator identity, timestamp, record IDs acknowledged as stale, action type) and dismisses the banner. The Class C gate becomes available, but the logged acknowledgment is permanently part of the approval record.

### State C — Evidence expired (absolute block)

Per the Session 13 addendum: `expired` freshness_status is an absolute gate block for launch authorization. More stringent than `stale`. There is no `[Proceed Without Refreshing]` path for expired evidence.

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ⛔ EXPIRED EVIDENCE — LAUNCH AUTHORIZATION GATE BLOCKED                  │
│                                                                           │
│  Evidence record:  [obs-038] Market positioning snapshot                  │
│  Status:           Expired — 22 days old                                  │
│  VEDA assessment:  Evidence is so old it should not be used for           │
│                    execution decisions.                                    │
│                                                                           │
│  This evidence must be refreshed before launch authorization can          │
│  be sought. There is no bypass path for expired evidence.                 │
│                                                                           │
│  [Refresh Evidence from VEDA]                                             │
└──────────────────────────────────────────────────────────────────────────┘
```

Background: `--state-danger-bg`
Border-left: 3px `--state-blocked`; `border-radius: 0`
`⛔ EXPIRED EVIDENCE`: `--type-sm`, `--weight-bold`, `--state-blocked`
Body: `--type-sm`, `--text-secondary`
"There is no bypass path": `--type-sm`, `--weight-medium`, `--text-primary` — this line should feel definitive
`[Refresh Evidence from VEDA]`: `--text-link`, `--type-sm`; no secondary option on this banner

Non-dismissible. The gate remains blocked until evidence is refreshed and freshness_status is no longer `expired`.

---

## 7. Section Content: Overview

The Overview section establishes the launch scope and confirms what is and is not being authorized.

**Layout:** Same label/value pair pattern as Session 13, followed by the Scope block and the Authorization Posture block.

**Metadata fields:**

```
Launch scope:     content-hub-v1 — full site launch to production
Execution entry:  exec-07  (--font-mono)
Parent handoff:   hdl-07 — hosting-comparison-site
Stage:            Launch Authorization — Pending *     ← schema-pending notation
Prepared:         2026-04-01 11:30
```

**AUTHORIZED SCOPE block:**

```
WHAT IS BEING AUTHORIZED
Launch-sensitive execution for content-hub-v1 within the confirmed handoff scope.
This covers: public-facing content publication, indexation actions, and
DNS/hosting configuration for veda-domination.com.

What this authorization does NOT cover:
  • Scope expansion beyond the hdl-07 approved execution boundary
  • Authorization for any future handoff or separate execution scope
  • Transfer of planning ownership — Project V retains planning truth
  • Transfer of observatory ownership — VEDA retains signal/evidence truth
  • Self-authorization for any actions V Forge discovers are outside scope

What happens if authorized:
  V Forge will proceed with launch-sensitive execution within the confirmed scope.
  External content will become publicly visible and indexable.
  Some actions (publication, DNS change) may be difficult or impossible to reverse.
```

`WHAT IS BEING AUTHORIZED` label: structural label pattern (`--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase, 0.3px letter-spacing)
Prose: `--type-sm`, `--text-primary`, `line-height: 1.6`
"What this authorization does NOT cover" list: `--type-sm`, `--text-secondary`; bullets `•` in `--text-tertiary`
"What happens if authorized": `--type-sm`, `--text-primary`

**Why the "does NOT cover" block is required:** This is the direct counterpart to the Class C modal's "What does NOT change" block (Session 10 §5.4). The modal shows this information at authorization time; the Overview section shows it during review. The operator sees the ownership boundaries before reaching the gate, not only at the moment of authorization.

**IRREVERSIBILITY NOTICE** (when the launch includes irreversible actions):

```
⚠ IRREVERSIBILITY NOTICE
Some actions within this launch scope are difficult or impossible to reverse
once execution proceeds:
  • DNS/hosting configuration changes affecting veda-domination.com
  • Public indexation — content may be crawled and indexed before rollback is possible
  • External distribution and notification actions if included in scope
```

Background: `--state-danger-bg`; border-left: 3px `--state-danger`; `border-radius: 0`; padding `--space-3` (12px).
`⚠ IRREVERSIBILITY NOTICE`: `--type-sm`, `--weight-semibold`, `--state-danger`
List: `--type-sm`, `--text-secondary`

---

## 8. Section Content: Three-Dimension Cross-System Confirmation Checklist

This checklist is the primary structural element of the launch readiness surface. It appears as its own sub-section within the Overview, or as a persistent element always visible in the section nav area (it is important enough to be visible even when the operator is in other section tabs).

**Implementation decision:** The three-dimension checklist is displayed as a fixed summary strip **between the section nav and the section body** — a second horizontal strip below the standard section nav, present on all section tabs. It is not part of the standard section nav itself. It is always visible while the operator is reviewing any section.

```
┌────────────────────────────────────────────────────────────────────────────┐
│  Overview  Evidence  Decisions  History  Actions                           │  ← section nav
├────────────────────────────────────────────────────────────────────────────┤
│  ✓ Planning-side readiness    ○ VEDA signal current    ○ V Forge verified  │  ← confirmation strip
└────────────────────────────────────────────────────────────────────────────┘
```

**Confirmation strip anatomy:**
- Height: 36px
- Background: `--surface-raised` — same level as section nav, forming a continuous header block
- Bottom border: `--border-subtle` 1px
- Padding: `--space-3` (12px) horizontal, vertically centered
- Three items, equally spaced across the strip

**Per-item:**
- `✓` (confirmed): `--state-success` 14px circle with check; label `--type-sm`, `--text-primary`, `--weight-medium`
- `○` (not yet confirmed): `--text-tertiary` 14px hollow circle; label `--type-sm`, `--text-tertiary`, `--weight-normal`
- `✗` (blocking condition active): `--state-danger` 14px; label `--type-sm`, `--state-danger`, `--weight-medium`
- `*` (schema-pending): appended to label text, same `*` treatment as elsewhere

Clicking any confirmation strip item navigates to the corresponding section tab.

**Three dimensions:**

### Dimension 1 — Planning-side readiness (Project V)
Label: `Planning-side readiness`
Confirmed when: The planning-side readiness section within Overview has been reviewed (5-second timer) AND no planning-side blocking conditions exist.

### Dimension 2 — VEDA signal current (VEDA)
Label: `VEDA signal current`
Confirmed when: The Evidence section has been reviewed (5-second timer) AND no evidence records are `expired` AND any `stale` records have been either refreshed or explicitly acknowledged via the `[Proceed Without Refreshing]` path.

### Dimension 3 — V Forge verified (V Forge)
Label: `V Forge verified`
Confirmed when: The V Forge verification record in the Actions section shows status `complete` — this is a **record state check**, not an operator click. If V Forge has not yet produced a verification completion record, this dimension shows `○` regardless of how much time the operator spends in the section.

**The Class C gate is available only when all three show `✓`.** If any dimension shows `○` or `✗`, the `[Proceed to Authorization Gate]` button in the Actions section is inactive at `--state-disabled-opacity`.

**The confirmation strip is the single place in the surface where the operator can see cross-system launch readiness at a glance.** It prevents the operator from authorizing a launch while one dimension is quietly unchecked. Its persistent visibility on every section tab enforces this without requiring the operator to navigate to a specific section to check.

---

## 9. Section Content: Evidence

The Evidence section covers the VEDA signal and evidence that informed the launch readiness determination. It follows the Session 13 addendum's updated evidence row format throughout.

**Section header:**
`EVIDENCE BASIS — SOURCE: VEDA (referenced, not owned by Project V or V Forge)`
`--type-xs`, `--weight-semibold`, `--text-tertiary`; ownership label in `--state-info` using `--ownership-label-bg` fill

**Two sub-sections:**

### Planning-side evidence (VEDA signal that supported the Project V readiness determination)

```
PLANNING READINESS EVIDENCE

  [obs-047]   Hosting keyword intent snapshot
              Source: VEDA — google_search_console  ·  Gathered: 2026-04-01 14:32
              Freshness: fresh  ·  Trust: verified
              Used for: Planning-side readiness determination

  [obs-041]   SERP delta — hosting vertical              ⚠ AGING
              Source: VEDA — semrush  ·  Gathered: 2026-03-30 09:15
              Freshness: aging  ·  Trust: verified
              Used for: Competitive positioning basis in readiness evaluation
```

The `⚠ AGING` marker: `--state-warning`, `--type-xs` — softer than stale, signals approaching the boundary.

### Execution-side evidence (VEDA signal that V Forge queried via the evidence access contract during execution)

```
EXECUTION-TIME EVIDENCE (queried by V Forge during execution)

  [obs-052]   GA4 performance — content-hub staging
              Source: VEDA — google_analytics  ·  Gathered: 2026-04-03 07:20
              Freshness: fresh  ·  Trust: verified
              V Forge attribution: queried via evidence access contract during
              pre-launch verification (exec-07, 2026-04-03 08:15)

  [obs-049]   Search Console impression baseline
              Source: VEDA — google_search_console  ·  Gathered: 2026-04-03 06:45
              Freshness: fresh  ·  Trust: verified
              V Forge attribution: queried for content completeness validation
```

The "V Forge attribution" line is new to this surface — it reflects the evidence access contract: V Forge agents actively query VEDA evidence during execution, and that access must be attributed. The format: `V Forge attribution:` label in `--type-xs`, `--weight-semibold`, `--text-tertiary`; value in `--type-xs`, `--text-secondary`.

**The two sub-sections confirm that the operator can see both dimensions of evidence:** what Project V used for planning readiness, and what V Forge used for execution verification. The cross-system confirmation requirement demands that both dimensions are visible to the operator.

**Evidence currency summary line** (at top of Evidence section, above the sub-sections):

| All evidence fresh | `✓ All evidence meets launch currency threshold` — `--state-success`, `--type-xs` |
| Any aging | `⚠ Some evidence is aging — review before authorizing` — `--state-warning`, `--type-xs` |
| Any stale | `⚠ Evidence below launch currency threshold — refresh required or acknowledge` — `--staleness-text`, `--type-xs` |
| Any expired | `⛔ Expired evidence present — gate blocked until refreshed` — `--state-blocked`, `--type-xs` |

---

## 10. Section Content: Decisions

The Decisions section shows governing decisions active at the time of the readiness determination, with their current status and relevance to the launch scope.

Same format as Session 13 §4.6 with launch-specific relevance labeling:

```
[dec-03]  Prioritize search-first content strategy     [active]  2026-02-14
          Relevance to launch: Governs content priority for the entire
          content-hub-v1 scope. Active and unchanged since readiness evaluation.

[dec-07]  Hosting vertical — revised scope             [active]  2026-03-28
          Relevance to launch: The governing decision for the hosting comparison
          scope being launched. Confirms the launch scope is within authorized
          strategic direction.
```

**Scope integrity note** (below the decision list, if all relevant decisions are active and unchanged):

```
ℹ Scope integrity check
  All governing decisions relevant to this launch scope are active and unchanged
  since the readiness evaluation was completed (2026-04-01).
  No scope has silently widened beyond what was assessed.
```

`ℹ`: `--state-info`, `--type-sm`; text: `--type-sm`, `--text-secondary`; background: `--state-info-bg`; border-left: 3px `--state-info`; `border-radius: 0`

**Scope integrity failure** (if a governing decision changed since the readiness evaluation):

```
⚠ SCOPE INTEGRITY WARNING
[dec-07] was revised after the readiness evaluation was completed.
The revised decision may have changed what scope is authorized.
Review before authorizing launch.
[View Decision Changes]
```

Same staleness banner treatment as Session 13's stale-basis warning. Material significance — gate blocked until acknowledged.

---

## 11. Section Content: History

Same format as Session 13 §4.7, using activity trail action vocabulary.

```
2026-04-01  11:30   Planning readiness assessment completed    [eval-14]
                    Planning-side readiness confirmed.
                    3 confirmation dimensions: planning ✓, VEDA pending, V Forge pending.

2026-04-01  14:32   Evidence loaded — planning basis           [obs-047, obs-041]
                    VEDA signal loaded for readiness determination.

2026-04-02  08:15   V Forge pre-launch verification initiated  [exec-07]
                    V Forge verification underway.

2026-04-03  07:20   V Forge evidence query logged              [evidence.query]
                    V Forge queried VEDA via evidence access contract.
                    Records: [obs-052], [obs-049]. Cost: 1,240 tokens.

2026-04-03  09:15   V Forge pre-launch verification complete   [exec-07]
                    All 3 verification dimensions confirmed.
                    Cross-system confirmation: all ✓.

2026-04-03  09:20   Launch authorization requested             [approval.request]
                    Class C approval requested. awaiting operator authorization.
```

The `evidence.query` entry (from the V Forge activity trail) is shown in the History section when V Forge queried evidence during verification. Its entry shows the query record type, what was queried, and the token cost — making evidence access visible in the review history. Token cost: `--type-xs`, `--text-tertiary`.

---

## 12. Section Content: Blocking Conditions Panel

The blocking conditions panel is a distinct visual element within the Actions section (above the checkpoint list and gate), visible whenever any blocking condition exists. It is the implementation of the launch readiness doctrine: "the workflow must stop and must not proceed to authorization when blocking conditions exist."

**When no blocking conditions exist:**

```
✓ No blocking conditions
  All three launch readiness dimensions are confirmed. The authorization
  gate is available.
```

`✓`: `--state-success`. Text: `--type-sm`, `--text-secondary`.

**When blocking conditions exist:**

```
BLOCKING CONDITIONS                                           [3 active]
─────────────────────────────────────────────────────────────────────────
⛔  HARD BLOCK   Evidence expired — [obs-038] must be refreshed
                 Resolves when: Evidence refreshed from VEDA

⚠   SOFT BLOCK  V Forge verification incomplete
                 V Forge has not yet produced a verification completion record.
                 Resolves when: V Forge verification record status = complete

⚠   SOFT BLOCK  Cross-system confirmation incomplete
                 Dimension: VEDA signal currency not yet confirmed.
                 Resolves when: Evidence section reviewed and currency acknowledged
─────────────────────────────────────────────────────────────────────────
```

**`BLOCKING CONDITIONS` label:** `--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase, 0.3px letter-spacing

**Count badge:** `--state-danger` if any hard block; `--state-warning` if only soft blocks; `--type-xs`, `--weight-bold`

**Per-condition row:**

- Hard block: `⛔` in `--state-blocked`; `HARD BLOCK` in `--state-blocked`, `--type-xs`, `--weight-bold`; condition description in `--type-sm`, `--text-primary`; "Resolves when:" in `--type-xs`, `--text-secondary`
- Soft block: `⚠` in `--state-warning`; `SOFT BLOCK` in `--state-warning`, `--type-xs`, `--weight-bold`; condition description in `--type-sm`, `--text-primary`; "Resolves when:" in `--type-xs`, `--text-secondary`

**Distinction between hard and soft blocks:**
- **Hard block:** Absolute. Cannot be acknowledged past. Cannot be bypassed. Gate is blocked until the condition is resolved by record state. Examples: expired evidence, V Forge verification not complete, prior approval invalidated.
- **Soft block:** Gate is blocked but the operator can take action to resolve it within the current session. Examples: stale evidence (can acknowledge), cross-system confirmation dimension unchecked (can complete review), scope integrity warning (can acknowledge change).

The blocking conditions panel is non-collapsible when active. The operator must see it.

---

## 13. Section Content: Actions

The Actions section follows the same structure as Session 10/11: blocking conditions panel (§12), then available governed actions list, then checkpoint list, then the `[Proceed to Authorization Gate]` button, then the Class C gate widget (read-only confirmation record after authorization).

### Available governed actions

```
AVAILABLE ACTIONS

  [CLASS C]  Launch authorization                     Governed path
  [CLASS A]  Copy record ID                           Immediate
  [CLASS A]  View full V Forge execution report       Navigate
```

### Checkpoints for launch authorization (from Session 10 §8.4, restated in display form)

```
REQUIRED REVIEW BEFORE AUTHORIZING

  ✓  Overview section reviewed
  ✓  Planning-side readiness reviewed
  ○  Evidence and signal reviewed           ← requires 5s on Evidence tab
  ○  Execution-side verification confirmed  ← requires record state: V Forge verification = complete
  ○  Cross-system confirmation complete     ← all three dimensions ✓
  ○  Context change notices acknowledged    ← only shown if scope integrity warning is active
```

**The `Execution-side verification confirmed` checkpoint** is a record state check. The row shows:
- `○ Execution-side verification confirmed — V Forge verification not yet complete` when V Forge verification record is not in `complete` state
- `✓ Execution-side verification confirmed` when V Forge verification record reaches `complete` state (auto-updates when the record state changes; no operator click needed)

When this checkpoint is incomplete, a note appears below the row:
```
  V Forge has not yet confirmed pre-launch verification.
  This checkpoint satisfies automatically when V Forge produces a
  verification completion record. No operator action required.
```
`--type-xs`, `--text-tertiary`

**The `Cross-system confirmation complete` checkpoint** expands to show a mini-checklist when incomplete:

```
  ○  Cross-system confirmation complete
     ✓  Planning-side readiness
     ○  VEDA signal currency
     ✓  V Forge verification
     Missing: VEDA signal currency. Review the Evidence section.
```

Mini-checklist labels: `--type-xs`, `--text-secondary`; icons same `✓`/`○` pattern at 12px. The missing dimension is named specifically — not "confirmation incomplete."

### `[Proceed to Authorization Gate]` button

Per Session 11 §8.1 — appears above the gate widget position, active only when all checkpoints are satisfied and no hard blocks exist:

- Width: 240px; Height: 40px
- Background: `--surface-elevated`; Border: 1px `--border-accent`; Text: `--accent-primary`, `--type-sm`, `--weight-bold`
- Inactive (some checkpoints incomplete or hard block active): `--state-disabled-opacity`

**When inactive due to specific conditions, a status note below the button:**
- Hard block active: `⛔ Gate blocked — [specific hard block condition]. Resolve before proceeding.`
- Soft block / checkpoint incomplete: `○ [N] required checkpoints incomplete. Complete review above.`

These notes are `--type-xs`, colored by urgency (`--state-blocked` for hard block, `--text-tertiary` for soft).

### Class C gate widget (post-authorization, read-only)

After the Class C modal authorization is written, the gate widget in the Actions section transitions to a read-only confirmation record (per Session 10 §8.3 / Session 11 §8.3):

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AUTHORIZATION REQUEST                                      [CLASS C]   │
│                                                                          │
│  Action:   Launch authorization — content-hub-v1                         │
│  Scope:    Full site launch within hdl-07 execution boundary             │
│  Covers:   Approval for launch-sensitive execution                       │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ✓ AUTHORIZED — 2026-04-03 11:22  ·  Authorization + confirmation log    │
│    written. Stale evidence acknowledgment logged.                        │
│                                                                          │
│  [Proceed to Activation ›]                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

If stale evidence was acknowledged via `[Proceed Without Refreshing]`, the confirmation line notes this: "Stale evidence acknowledgment logged." This makes the governance record of the acknowledgment visible in the center surface, not only in a backend log.

---

## 14. Post-Launch State Transition

After launch-sensitive execution completes successfully, the workflow stage transitions to `Post-Launch — Active`. This is also schema-pending, derived from workflow posture.

**Center surface treatment when the stage transitions to `Post-Launch — Active`:**

An inline banner fires in the banner position:

```
ℹ LAUNCH COMPLETE — POST-LAUNCH ACTIVE
content-hub-v1 has entered the post-launch state.

V Forge execution truth now includes the launched scope.
VEDA observatory observation has resumed for the launched scope.
Project V retains planning truth.

Post-launch findings that require planning reconsideration will
route through the maintenance and replanning workflow.
[View Post-Launch State]
```

Background: `--state-info-bg`; border-left: 3px `--state-info`; `border-radius: 0`; `--type-sm`, `--text-secondary`
Header `LAUNCH COMPLETE — POST-LAUNCH ACTIVE`: `--type-sm`, `--weight-semibold`, `--state-info`
`[View Post-Launch State]`: `--text-link`, `--type-sm`; navigates to a new center workspace tab showing the execution entry in its post-launch state (V Forge execution entry detail view)

**Why the ownership lines are in the banner:** The post-launch state is the moment most likely to produce cross-system ownership drift — operators may be tempted to think "launch is done, V Forge owns everything now." The banner explicitly re-states the ownership picture at the moment of transition. Project V retains planning truth. VEDA retains observatory truth. V Forge holds execution truth for the launched scope. None of that transferred.

**The view header stage indicator updates:**
```
exec-07  ·  Post-Launch — Active *
```
Same `*` schema-pending notation.

**The confirmation strip below the section nav updates:**
```
✓ Planning-side readiness    ✓ VEDA signal current    ✓ V Forge verified
```
All three dimensions remain `✓` in the post-launch state — confirmation is complete. The strip is read-only after authorization.

---

## 15. Synchronization with Other Surfaces

**When V Forge verification record reaches `complete` state (EVENT-17):**
- The `Execution-side verification confirmed` checkpoint auto-satisfies
- The confirmation strip Dimension 3 updates to `✓`
- If all other checkpoints are also satisfied, the `[Proceed to Authorization Gate]` button activates
- Informational toast fires: `V Forge pre-launch verification complete — launch gate now available.`

**When evidence becomes stale during review (EVENT-08):**
- Evidence currency warning banner fires in banner position per §6 State B or C
- Relevant confirmation strip dimension updates: `VEDA signal current` → `○` or `✗`
- `[Proceed to Authorization Gate]` button returns to inactive if it was active
- Toast fires per Session 12 §7 EVENT-08

**When launch authorization is written (EVENT-05):**
- Topbar attention badge clears (pending approval resolved)
- Context strip STAGE and INTEGRITY rows update
- Toast fires per Session 12 §6.4
- Left nav V Forge tree execution entry badge updates from `launch auth pending` to `active`

**When stage transitions to `Post-Launch — Active` (EVENT-17):**
- Topbar stage indicator updates: `Post-Launch — Active *`
- Context strip STAGE row updates
- Center surface inline banner fires per §14
- Toast fires: `Post-launch state active — content-hub-v1 is live.`

---

## 16. Token Usage from Session 2

No new tokens introduced.

| Element | Token(s) |
|---|---|
| `LAUNCH READINESS` record type badge | `--state-info` text, 10% opacity bg, `--type-xs`, `--weight-bold` |
| Stage `*` schema-pending notation | `--text-tertiary`, `--type-xs` |
| `[SCHEMA PENDING]` tag | `--schema-pending-bg` fill, `--state-schema-hold` text, `--radius-sm`, `--type-xs` |
| Evidence currency warning (stale) | `--staleness-bg`, `--staleness-border` (3px left), `--staleness-text` |
| Evidence currency block (expired) | `--state-danger-bg`, 3px `--state-blocked` left, `--state-blocked` header |
| `[Proceed Without Refreshing]` border | `--state-warning` |
| `[Proceed Without Refreshing]` text | `--state-warning`, `--type-sm`, `--weight-medium` |
| `[Proceed Without Refreshing]` hover | `--state-warning-bg` |
| Acknowledgment statement (pre-populated) | `--surface-raised` bg, `--border-default` border, read-only |
| `[Confirm — Log This Acknowledgment]` | `--state-warning` border + text, `--radius-md` |
| `AUTHORIZED` confirmation stale note | same `--state-success` line with `--text-secondary` stale note appended |
| `WHAT IS BEING AUTHORIZED` label | `--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase, 0.3px letter-spacing |
| "does NOT cover" list | `--type-sm`, `--text-secondary`; `•` in `--text-tertiary` |
| IRREVERSIBILITY NOTICE bg | `--state-danger-bg` |
| IRREVERSIBILITY NOTICE border | 3px `--state-danger` left |
| IRREVERSIBILITY NOTICE header | `--type-sm`, `--weight-semibold`, `--state-danger` |
| Confirmation strip height | 36px |
| Confirmation strip bg | `--surface-raised` |
| Confirmation strip bottom border | `--border-subtle` 1px |
| Dimension `✓` confirmed | `--state-success` 14px circle |
| Dimension `○` not confirmed | `--text-tertiary` 14px hollow circle |
| Dimension `✗` blocking | `--state-danger` 14px |
| Dimension label confirmed | `--type-sm`, `--text-primary`, `--weight-medium` |
| Dimension label not confirmed | `--type-sm`, `--text-tertiary`, `--weight-normal` |
| `BLOCKING CONDITIONS` label | `--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase |
| Hard block `⛔` | `--state-blocked` |
| `HARD BLOCK` text | `--state-blocked`, `--type-xs`, `--weight-bold` |
| Soft block `⚠` | `--state-warning` |
| `SOFT BLOCK` text | `--state-warning`, `--type-xs`, `--weight-bold` |
| "Resolves when:" | `--type-xs`, `--text-secondary` |
| Scope integrity `ℹ` notice | `--state-info-bg`, 3px `--state-info` left, `--state-info` icon |
| Scope integrity warning `⚠` | `--staleness-bg`, `--staleness-border` (3px left), `--staleness-text` |
| Evidence `⚠ AGING` marker | `--state-warning`, `--type-xs` |
| V Forge attribution label | `--type-xs`, `--weight-semibold`, `--text-tertiary` |
| V Forge attribution value | `--type-xs`, `--text-secondary` |
| Token cost in History | `--type-xs`, `--text-tertiary` |
| Post-launch banner bg | `--state-info-bg` |
| Post-launch banner border | 3px `--state-info` left |
| Post-launch banner header | `--type-sm`, `--weight-semibold`, `--state-info` |
| `✓ Evidence currency` line | `--state-success`, `--type-xs` |
| `⚠ Evidence aging` line | `--state-warning`, `--type-xs` |
| `⚠ Evidence stale` line | `--staleness-text`, `--type-xs` |
| `⛔ Expired evidence` line | `--state-blocked`, `--type-xs` |
| Checkpoint auto-satisfy note | `--type-xs`, `--text-tertiary` |

---

## 17. What Session 14 Resolves

- The Launch Readiness Review View is fully specified: all section tabs, the confirmation strip, the blocking conditions panel, the evidence currency treatment (including the three-state banner for aging/stale/expired), and the `[Proceed Without Refreshing — I Accept the Risk]` path with its mandatory acknowledgment attestation.
- All four launch readiness stage names are displayed with `*` schema-pending notation throughout the surface. `[SCHEMA PENDING]` tag is used for derivation failures. No stage name is presented as schema-anchored.
- The three-dimension cross-system confirmation checklist is the surface's primary structural element, designed as a persistent confirmation strip visible on every section tab — not buried in one section the operator might skip.
- The `expired` freshness status is an absolute gate block with no bypass path, distinguishing it clearly from `stale` (which has the `[Proceed Without Refreshing]` option).
- The blocking conditions panel distinguishes hard blocks (absolute, resolved only by record state) from soft blocks (resolved by operator action or review completion).
- V Forge's active evidence querying (via the evidence access contract) is visible in the History section (as `evidence.query` activity trail entries with token cost) and in the Evidence section's execution-time evidence sub-section, with V Forge attribution lines.
- The post-launch state transition is specified: what the banner says, what ownership lines it re-states, how the stage indicator updates, and why the ownership re-statement is present at that specific moment.
- The `[Proceed Without Refreshing — I Accept the Risk]` acknowledgment is a pre-populated read-only attestation naming specific record IDs and the action — not a generic "I accept" checkbox. The confirmation of that acknowledgment is visible in the post-authorization gate widget confirmation state.
- The scope integrity check (Decisions section) — whether governing decisions changed after the readiness evaluation — is designed as a first-class element of the Decisions section, with the same material/informational significance distinction as the handoff stale-basis warning.

---

## 18. What Session 14 Does Not Resolve Yet

- **The post-launch observation workflow surface** — what the operator sees when the project is in `Post-Launch — Active` and VEDA is actively monitoring. The `[View Post-Launch State]` link in the post-launch banner routes somewhere; that detail view is a future session (post-launch observation workflow, not yet in the active plan).
- **V Forge pre-launch verification content** — the verification completion record that satisfies the `Execution-side verification confirmed` checkpoint is produced by V Forge and surfaced as a record state. The center surface for viewing the full V Forge verification report is the V Forge Execution Entry detail view (referenced in Session 8/9 but not yet specialized beyond the generic template). The launch readiness surface checks its state; it does not display its full content.
- **Budget governance display** — the activity trail history shows token costs for V Forge evidence queries. When the cost/token governance doc is completed (Finding 4 from the audit), the budget allocation and budget status fields from the structured handoff packet will need to surface somewhere in this view — likely in the Overview or History sections. Currently those fields are `[SCHEMA PENDING]`.
- **The structured handoff packet fields** (`acceptance_criteria`, `escalation_policy`, `reporting_contract`) referenced in Session 13's addendum — these are still pending formal definition. When defined, the launch readiness Overview section should show the launch-specific acceptance criteria and escalation policy.

---

## 19. Recommended Inputs to Session 15

Session 15 is Maintenance / Ranking UX — the third TIER 4 workflow surface, with partial schema block.

**What Session 15 inherits from Sessions 13–14:**
- The return trigger routing decision (Session 13) leaves the ecosystem in one of two states: `Handle as maintenance` or `Route to replanning`. Session 15 designs what happens after each of those paths — what the operator sees when V Forge is executing in maintenance mode, and what the operator sees when a replanning event is in progress.
- The `Post-Launch — Active` state from Session 14 is the natural re-entry point for the maintenance and replanning workflow when post-launch conditions require reconsideration. Session 15's maintenance tracking surface must acknowledge this connection.
- The confirmation strip pattern from Session 14 (three items, persistent across section tabs) is available as a reusable pattern for multi-dimension status checks. Session 15 should evaluate whether the maintenance vs replanning status picture benefits from a similar treatment.

**Schema block status for Session 15:**
- `Execution — Maintenance`: no dedicated schema record; derived from execution-active posture with no active return trigger routed to replanning
- `Replanning — In Progress`: no dedicated `ReplanningRecord`; derived from return trigger in `routed` state combined with Project V operational posture
- Both must use `*` notation and `[SCHEMA PENDING]` tags where derivation fails

**Key design questions for Session 15:**

What does the portfolio ranking surface look like? The work plan mentions "relative priority signaling within Project V" as part of Session 15. This involves comparing multiple projects or initiatives — it's a different visual problem from the single-record detail view pattern used in Sessions 13–14. Session 15 needs to decide whether portfolio ranking belongs in the center workspace (as a multi-record view, not the generic detail template) or elsewhere.

How is the maintenance vs replanning status distinction surfaced in the left nav during an active replanning event? Session 6 established that `Execution — Maintenance *` and `Replanning — In Progress *` are schema-pending stages. Session 15 should specify what the left nav tree looks like during an active replanning event — specifically, whether the return trigger section (which floats to the top during active triggers in Session 6) remains visible or is replaced by a replanning-in-progress indicator after the trigger is routed.

How does the maintenance surface acknowledge that V Forge may be actively querying VEDA evidence during maintenance? The evidence access contract (Session 13 addendum) specifies that V Forge agents query evidence during maintenance cycles. The maintenance tracking surface should make this visible — not as a detailed technical readout, but as a confirmation that V Forge has situational awareness from current VEDA signal, rather than operating against stale handoff-time evidence.
