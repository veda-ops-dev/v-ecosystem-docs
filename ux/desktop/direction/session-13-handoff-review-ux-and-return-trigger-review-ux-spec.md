# Session 13 — Handoff Review UX + Return Trigger Review UX
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–12 (shell backbone, gate surfaces, routing flow, notification system all stable)
**Required before:** Session 14 (Launch Readiness UX) — the handoff review surface is the closest structural cousin to the launch readiness review; the two surfaces share the stale-basis warning vocabulary and the checkpoint-to-gate pattern; Session 14 builds on the conventions Session 13 establishes

---

## 1. Files Read

**Prior sessions:**
- `session-02-minimal-token-decisions.md` — active token baseline
- `session-09-center-workspace-foundation-spec.md` — generic record detail view template; section nav (Overview / Evidence / Decisions / History / Actions); Actions section gate widget placement; inline banner position; cross-surface sync markers
- `session-10-approval-gate-surfaces-spec.md` — Class B inline gate widget; checkpoint model (shared + handoff-specific checkpoints); stale-context warning above gate; Class D escalation banner
- `session-11-review-to-gate-routing-flow-spec.md` — five-step routing flow; `intent = 'approval_gate'` behavior; section tab `✓` reviewed suffix; scroll-to-gate on activation
- `session-12-session-integrity-check-and-alert-notification-system-spec.md` — return trigger routing from integrity view; `[Review in center surface ›]` routing link; return trigger lifecycle state transitions and their notifications
- `session-06-left-nav-shell-project-v-tree-spec.md` — handoff status badge vocabulary; `prepared` vs `awaiting approval` distinction; return triggers section floating to top

**Doctrine:**
- `interfaces/desktop-surface-architecture.md` — Handoff Package Review View required content; Return Trigger Review View required content; maintenance vs replanning routing distinction; stale basis warning before gate; cross-system confirmation posture
- `interfaces/desktop-governance-and-gating-model.md` — Class B gate; rejection must be persisted; what makes a pending approval invalid; stale approval detection; the approval event is distinct from activation
- `interfaces/desktop-state-and-context-model.md` — nine state categories; handoff lifecycle states; return trigger lifecycle states (`arrived → acknowledged → routed | dismissed`)
- `interfaces/desktop-invalidation-and-refresh-matrix.md` — EVENT-02, EVENT-05, EVENT-06, EVENT-08, EVENT-16, EVENT-17 — the events most likely to fire during handoff and return trigger review
- `interfaces/project-v-to-v-forge-handoff-interface.md` — what a handoff transfers; what it does not transfer; minimum interface semantics; forbidden interpretations
- `interfaces/v-forge-to-project-v-return-to-planning-interface.md` — what return-to-planning transfers; retention principle; what findings may and may not be interpreted as; ownership after return

**Workflows:**
- `workflows/handoff-workflow.md` — six stages; prepared vs awaiting approval vs activated distinction; awaiting state principle; insufficient handoff principle; stale awaiting-approval state
- `workflows/maintenance-and-replanning-workflow.md` — maintenance vs replanning distinction; trigger classification; the replanning event is not an automatic planning mutation; maintenance does not require this workflow

---

## 2. Session 13 Scope Confirmation

The work plan defines Session 13 as: two workflow-specific center workspace surfaces, designed as variants of the same template. These are the highest-frequency governance surfaces in the application.

This session produces:
- **Handoff Package Review View** — the complete center workspace surface for reviewing a handoff record before the Class B approval gate
- **Return Trigger Review View** — the complete center workspace surface for reviewing a V Forge return trigger finding before routing or dismissing
- The stale-basis warning vocabulary specific to handoff records (distinct from the general staleness warning from Session 10 §4.7)
- The maintenance vs replanning routing distinction, designed concretely with named options and semantically unambiguous labels
- The return trigger response selection checkpoint mechanics
- The partial schema block notation for maintenance/replanning stage derivation

This session does not:
- Redesign the gate widget (Session 10)
- Redesign the routing flow (Session 11)
- Design launch readiness review (Session 14)
- Design the maintenance/ranking workflow surface (Session 15)
- Invent schema anchors that do not exist

---

## 3. The Two Surfaces as Variants of One Template

Both the Handoff Package Review View and the Return Trigger Review View are specialized instances of the generic record detail view template from Session 9. They inherit:

- the tab bar (workspace tabs), view header, and section nav from Session 9 §4–5
- the section tab structure: Overview / Evidence / Decisions / History / Actions
- the inline banner position (between view header and section nav)
- the Actions section gate widget placement (bottom of Actions, below checkpoint list)
- the section tab `✓` reviewed suffix from Session 11 §6.2

What Session 13 specifies for each surface:
- the exact content within each section tab
- which sections carry review checkpoints (and which checkpoints)
- the stale-basis warning specific to handoff records
- the response options in the return trigger surface (which replace the approval gate for non-Class-B return trigger decisions)

The two surfaces share the same structural skeleton. Their content is fundamentally different because they answer different questions: the handoff surface asks "should this work transfer to V Forge?" and the return trigger surface asks "does this finding warrant replanning, maintenance, or dismissal?"

---

## 4. Handoff Package Review View

### 4.1 What It Is

The Handoff Package Review View is the center workspace surface where the operator reviews a prepared handoff before approving its activation. It is opened by:
- clicking the handoff item in the left nav tree (any handoff in any state)
- clicking `[Go to approval gate ›]` in the session integrity view (for a pending approval)
- clicking `[Proceed to Approval Gate]` on an ARP card in the right panel

The surface applies to handoffs in any state: `proposed`, `prepared`, `awaiting approval`, `handed_off`, `accepted`, `closed`. The gate widget is only active for handoffs in `awaiting approval` state — for all other states, the gate widget is absent and replaced by a read-only status line.

### 4.2 View Header

Per the Session 9 record type identifier vocabulary:

- Record type badge: `HANDOFF` — amber at 10% bg, `--state-warning` text, `--type-xs`, `--weight-bold`
- Record title: the handoff short name, e.g., `hosting-comparison-site` — `--type-lg`, `--weight-semibold`, `--text-primary`
- Record ID: `hdl-07` — `--font-mono`, `--type-xs`, `--text-tertiary`

### 4.3 Stale-Basis Warning (Handoff-Specific)

The handoff review surface has its own stale-basis warning distinct from the general staleness warning from Session 10 §4.7. The handoff workflow doctrine requires this: "if the handoff's planning basis, approval status, or evidence basis has changed materially since the package was prepared, this view must surface a visible warning before the approval gate is offered."

**When it appears:** The stale-basis warning appears in the inline banner position (between view header and section nav) when any of the following are true:
- A governing decision relevant to the handoff scope has been created, superseded, or invalidated since the handoff package was prepared (EVENTs 01, 02, 03)
- Evidence cited in the handoff package has become stale (EVENT-08)
- A prior approval associated with this handoff has been invalidated (EVENT-06)
- New blocking or critical gaps have opened since the package was prepared
- The readiness evaluation that supported the handoff has exceeded its validity window

**Difference from the general staleness warning:** The handoff stale-basis warning identifies which dimension of the handoff basis has changed, because the operator must understand whether the stale dimension is material to the handoff's scope. A stale evidence record used in the readiness basis is more alarming than a new governing decision that does not touch the handoff scope.

**Banner anatomy:**

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ⚠ HANDOFF BASIS HAS CHANGED SINCE THIS PACKAGE WAS PREPARED            │
│                                                                           │
│  Basis dimension:  [which dimension changed — see table below]           │
│  What changed:     [specific identification of the change]               │
│  Significance:     [material / informational — see below]                │
│                                                                           │
│  Review the updated context before proceeding to the approval gate.      │
│  [Review Change]                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

Background: `--staleness-bg`
Border-left: 3px `--staleness-border`; `border-radius: 0` on that side
`⚠ HANDOFF BASIS HAS CHANGED`: `--type-sm`, `--weight-semibold`, `--staleness-text`
Field labels (`Basis dimension:`, `What changed:`, `Significance:`): `--type-xs`, `--weight-semibold`, `--text-tertiary`, min-width 120px, right-aligned within the label column
Field values: `--type-sm`, `--text-primary`
`[Review Change]`: `--text-link`, `--type-sm`; clicking logs the acknowledgment and dismisses the banner (for `informational` significance) or scrolls the operator to the relevant section (for `material` significance)

**Basis dimensions and their significance:**

| Change | Dimension label | Significance |
|---|---|---|
| Governing decision created, superseded, or invalidated that affects handoff scope | `Governing decision` | Material — gate blocked until acknowledged |
| Evidence cited in the readiness basis is now stale | `Evidence basis` | Material — gate blocked until acknowledged |
| New blocking gap opened since package was prepared | `Planning gaps` | Material — gate blocked; blocking gaps checkpoint will also fail |
| Prior approval associated with this handoff invalidated | `Prior approval` | Material — gate blocked |
| New critical gap opened | `Planning gaps` | Informational — gate not blocked; review recommended |
| New governing decision that does not affect handoff scope | `Governing decision` | Informational — gate not blocked |
| Readiness evaluation age exceeds validity window | `Readiness basis` | Informational — review recommended |

For `material` significance: The gate widget controls remain at `--state-disabled-opacity`. The banner shows with no `×` dismiss option — the operator must click `[Review Change]` which logs the acknowledgment. After acknowledgment, controls activate (if all other checkpoints are also complete).

For `informational` significance: The banner appears but is dismissible with `×`. The gate is not blocked. The operator is informed but not stopped.

**Multiple simultaneous stale-basis conditions** stack as separate dimension lines within the same banner:

```
│  ⚠ HANDOFF BASIS HAS CHANGED SINCE THIS PACKAGE WAS PREPARED            │
│                                                                           │
│  Governing decision:  [dec-05] has been superseded by [dec-07]          │
│  Evidence basis:      [obs-041] is now stale (6 days old)               │
│                                                                           │
│  Both changes are material. Review before proceeding.                    │
│  [Review Changes]                                                         │
```

### 4.4 Section Content: Overview

The Overview section is the identity and scope section. It answers: what is this handoff and is it ready?

**Layout:** Two-column label/value pairs for metadata fields, followed by two structured block sections (Scope block and Transfer block). All labels: `--type-xs`, `--weight-semibold`, `--text-tertiary`, right-aligned in a 140px left column. All values: `--type-sm`, `--text-primary`.

**Metadata fields (label/value pairs at top):**

```
Status:           Awaiting Approval        ← colored per handoff status badge vocabulary
Prepared:         2026-03-28 14:22
Prepared basis:   Planning readiness confirmed; 3 of 3 gaps resolved
Handoff ID:       hdl-07  (--font-mono)
Parent objective: Hosting vertical authority
```

**Status value visual treatment:** The status value uses the same badge vocabulary as the left nav handoff status badges from Session 6 §5.7 — rendered inline as a colored text value (not a pill badge in this context, just the colored text):
- `Prepared`: `--state-info`
- `Awaiting Approval`: `--state-warning`, `--weight-medium`
- `Handed Off` / `Accepted`: `--state-success`
- `Proposed` / `Closed`: `--text-tertiary`
- `Blocked`: `--state-danger`

**`Handoff — Prepared` vs `Handoff — Awaiting Approval` distinction:** The Status field makes this explicit. The operator cannot mistake a prepared handoff for one that is awaiting formal approval. The surface architecture doctrine requires these states be visually and semantically distinct: "`Handoff — Prepared` does not imply that activation may proceed." The Status field with its colored value is the primary signal; the gate widget's inactive vs. active state reinforces it.

**Scope block** (below the metadata fields, separated by a `--border-subtle` hairline):

```
APPROVED SCOPE
What is handed off:
  The full approved scope of the hosting comparison initiative,
  as defined in Initiative [init-04]. Includes: site architecture,
  content execution, and publication to veda-domination.com.

Out-of-scope items:
  • YouTube channel integration — deferred to separate handoff
  • Paid promotion — outside current approved scope
  • Blog integration — remains in planning

What this handoff does NOT transfer:
  Planning ownership remains with Project V.
  Observatory and signal ownership remains with VEDA.
  V Forge receives execution responsibility for the approved scope only.
```

- `APPROVED SCOPE` label: `--type-xs`, `--weight-semibold`, `--text-tertiary`, letter-spacing 0.3px, uppercase — the structural section label pattern used throughout
- "What is handed off" body: `--type-sm`, `--text-primary`, `line-height: 1.6`
- "Out-of-scope items" list: `--type-sm`, `--text-secondary`; bullet `•` in `--text-tertiary`
- "What this handoff does NOT transfer": `--type-sm`, `--text-secondary`; this block is required by doctrine for every handoff review — it makes ownership boundaries explicit

**Transfer block** (below Scope block):

```
TRANSFER POSTURE
Execution responsibility transfers to V Forge upon activation.
Return-to-planning triggers will route back to Project V if
execution requires planning reconsideration.

Activation posture:   Approval required before activation
Expected receipt:     V Forge accepts on successful handoff activation
```

### 4.5 Section Content: Evidence

The Evidence section shows all evidence records that informed the handoff readiness basis, with their current freshness and trust posture.

**Section header line** (non-section-nav — a label within the section body):
`EVIDENCE BASIS — SOURCE: VEDA (referenced, not owned by Project V)`
`--type-xs`, `--weight-semibold`, `--text-tertiary`; the ownership label in `--state-info` using `--ownership-label-bg` fill (Session 2 governance tokens)

**Evidence record rows:** One row per loaded evidence record, matching the context strip EVIDENCE row format from Session 4 §5 (Category 5) but at the wider center workspace width — giving room for more detail:

```
[obs-047]   Hosting keyword intent snapshot
            Source: VEDA  ·  Captured: 2026-04-01 14:32  ·  Trust: high
            Used as: Readiness basis for search intent signal

[obs-041]   SERP delta — hosting vertical               ⚠ STALE — 6 days old
            Source: VEDA  ·  Captured: 2026-03-28 09:15  ·  Trust: high
            Used as: Competitive positioning basis
            [Refresh Evidence]
```

- Record ID: `--font-mono`, `--type-xs`, `--text-tertiary`
- Record title: `--type-sm`, `--text-primary`, `--weight-medium`
- Metadata line (Source / Captured / Trust): `--type-xs`, `--text-secondary`
- "Used as" line: `--type-xs`, `--text-tertiary` — this field is specific to the handoff review surface; it shows why this evidence record was included in the handoff package, so the operator understands the relevance
- `⚠ STALE`: inline on the title line; `--staleness-text`, `--type-xs`
- `[Refresh Evidence]`: `--text-link`, `--type-xs`

**If all evidence is current:** A `✓ All evidence current as of [most recent timestamp]` line appears at the top of the section in `--state-success`, `--type-xs`. This positive confirmation is important — the operator should know the evidence basis is solid, not just that it isn't stale.

**If any evidence is missing (referenced in the handoff package but not loaded):**

```
[obs-049]   ⚠ NOT LOADED — referenced in handoff package but not in session basis
            [Load Evidence]
```
`⚠ NOT LOADED` in `--state-warning`. `[Load Evidence]`: `--text-link`, `--type-xs`.

### 4.6 Section Content: Decisions

The Decisions section shows all governing decisions relevant to this handoff's scope, with their current status.

**Section note:**
`Governing decisions active at time of package preparation: [date]`
`--type-xs`, `--text-tertiary`

**Decision rows:** Named list — not a count. One row per decision, using the context strip DECISIONS row format (Session 4 §5 Category 4) at full center workspace width:

```
[dec-03]  Prioritize search-first content strategy     [active]  2026-02-14
          Relevance to this handoff: Governs content priority for execution scope.

[dec-05]  Hosting vertical over SaaS tier              [superseded → dec-07]  2026-03-10
          Relevance to this handoff: Was governing decision at time of package
          preparation. Now superseded — review before approving.

[dec-07]  Hosting vertical — revised scope             [active]  2026-03-28
          Relevance to this handoff: Supersedes dec-05. May affect handoff scope.
```

- Decision ID: `--font-mono`, `--type-xs`, `--text-tertiary`
- Decision title: `--type-sm`, `--text-primary`, `--weight-medium`
- Status badge: `[active]` in `--text-secondary`; `[superseded → dec-07]` in `--state-warning` text
- Date: `--type-xs`, `--text-tertiary`
- "Relevance to this handoff" line: `--type-xs`, `--text-secondary` — this field is specific to the handoff review surface; it provides the operator with the connection between the decision and the handoff scope

**Superseded decision treatment:** Superseded decisions that were governing at time of package preparation are shown with `[superseded → dec-id-new]` status and a callout: `Review before approving.` in `--state-warning`, `--type-xs`. This is the concrete implementation of the handoff doctrine requirement that a "stale awaiting-approval state is not authorization to proceed."

### 4.7 Section Content: History

The History section shows the handoff's state change timeline.

**History entry rows** (chronological, oldest first):

```
2026-03-25  14:08   Readiness evaluation completed           [eval-12]
                    3 of 3 gaps resolved. Readiness confirmed.

2026-03-28  14:22   Handoff package prepared                 [hdl-07]
                    Scope bounded. Evidence loaded. Package submitted.

2026-03-28  14:30   Approval request initiated               [arp-03]
                    Class B approval requested. Awaiting operator review.

2026-04-02  09:15   [dec-05] superseded by [dec-07]         [EVENT-02]
                    Governing decision changed after package preparation.
                    Stale-basis warning active.
```

- Timestamp: `--font-mono`, `--type-xs`, `--text-tertiary`; two columns (date | time), tab-aligned
- Event label: `--type-sm`, `--text-primary`, `--weight-medium`
- Record reference: `--font-mono`, `--type-xs`, `--text-tertiary`, right-aligned in the row
- Description line: `--type-xs`, `--text-secondary`

**Non-canonical events** (LLM outputs, continuity artifact events) in the history are shown with a `NON-CANONICAL` label using `--continuity-bg` fill and `--continuity-label` text (Session 2 governance tokens). They are never removed from the history — they are labeled to distinguish them from canonical state changes.

### 4.8 Section Content: Actions

The Actions section is where the approval gate lives. Its structure follows Session 10 §10.1 exactly:

1. Available governed actions list
2. Required review checkpoints
3. Gate widget (inactive or active)

**Handoff-specific checkpoints** (from Session 10 §8.4, restated here in their display form):

```
Required review before approving:

  ✓  Overview section reviewed
  ✓  Governing decisions reviewed
  ○  Evidence basis reviewed
  ○  No blocking gaps
  ○  Scope and out-of-scope items reviewed
  ○  Context change notices acknowledged     ← only shown when banner is active
```

**Note on the `No blocking gaps` checkpoint:** This checkpoint is satisfied by record state (no blocking gaps exist in the project), not by operator click. When blocking gaps exist:

```
  ○  Blocking gaps unresolved — 2 blocking gaps remain
     [gap-14] Intent gap — search vertical  ·  [gap-16] CWV threshold unmet
     These must be resolved before the handoff can be approved.
```

Gap IDs in `--font-mono`, `--type-xs`. The two gap IDs are links: `--text-link` — clicking each navigates to the gap detail in a new center workspace tab without closing the current handoff view.

**Gate widget for `awaiting approval` handoffs:** The standard Class B inline gate widget from Session 10 §4.2 populated with:
- Action: `Activate handoff — [handoff name]`
- Scope: `Execution scope as defined in [hdl-id]`
- Basis: `[Readiness evaluation result] — [gap resolution summary]`
- Covers: `Transfer of execution responsibility for [handoff name] to V Forge`
- Default: `Handoff remains in Awaiting Approval state`

**Gate widget for non-`awaiting approval` handoffs:**

For `proposed` or `prepared` handoffs (no pending approval):
```
No pending approval request.
This handoff is in [status] state — no approval action is available.
```
`--text-tertiary`, `--type-sm`

For `handed_off`, `accepted`, or `closed` handoffs:
```
✓ This handoff has been activated.
  Approval written: [timestamp]
  Execution responsibility transferred to V Forge.
```
`--state-success`, `--type-sm`

For `blocked` handoffs:
```
⛔ This handoff is blocked.
   [Blocking reason — specific]
   Resolve the blocking condition before proceeding.
```
`--state-blocked`, `--type-sm`

---

## 5. Return Trigger Review View

### 5.1 What It Is

The Return Trigger Review View is the center workspace surface where the operator reviews a V Forge execution finding that has been routed to Project V. It is opened by:
- clicking a return trigger item in the left nav tree (V Forge tree or Project V tree)
- clicking `[Review in center surface ›]` in the session integrity view
- clicking `[Review]` on the return trigger item in the context strip INTEGRITY row

The surface shows the operator what V Forge found, why it was routed to planning, and what options are available for responding. It is the decision point: does this finding require replanning, can it be handled as maintenance, or should it be dismissed?

### 5.2 View Header

- Record type badge: `RTN TRIGGER` — `--state-danger` bg at 10%, `--state-danger` text (the danger treatment is consistent with the return trigger `⚡` icon vocabulary throughout the system)
- Record title: a brief description of the finding, e.g., `Intent shift — hosting comparison` — `--type-lg`, `--weight-semibold`, `--text-primary`
- Record ID: `rtn-04` — `--font-mono`, `--type-xs`, `--text-tertiary`
- Lifecycle state badge: shown in the view header alongside the record ID: `arrived` / `acknowledged` / `routed` / `dismissed` — using the same color vocabulary as the left nav V Forge tree return trigger badges from Session 8 §7.1

**Lifecycle state badge in view header:**

| State | Text | Color |
|---|---|---|
| `arrived` | `UNREVIEWED` | `--state-danger` text, `--state-danger-bg` background |
| `acknowledged` | `REVIEWED — ACTION PENDING` | `--state-warning` text, `--state-warning-bg` background |
| `routed` | `ROUTED TO PLANNING` | `--state-info` text, `--state-info-bg` background |
| `dismissed` | `DISMISSED` | `--text-tertiary` text, `--surface-border` background |

When the operator opens a return trigger in `arrived` state, opening the view automatically transitions the state to `acknowledged`. This is the same behavior as the `[Acknowledge]` button in the session integrity view drawer — opening the detail view counts as acknowledgment. The badge updates immediately on view open: `UNREVIEWED` → `REVIEWED — ACTION PENDING`. The EVENT-16 state transition fires.

### 5.3 Non-authority Notice Banner

The return trigger review surface must surface a persistent non-authority notice that cannot be dismissed. This enforces the doctrine requirement that return-to-planning inputs are not automatic planning mutations.

**Non-authority notice** (appears in the inline banner position, non-dismissible, always present while the trigger is in `arrived` or `acknowledged` state):

```
┌──────────────────────────────────────────────────────────────────────────┐
│  ℹ THIS IS A V FORGE FINDING — NOT A PLANNING DIRECTIVE                  │
│                                                                           │
│  This finding was produced in execution and routed to Project V for       │
│  operator evaluation. It does not automatically change planning state.   │
│  V Forge retains execution ownership. Your response determines whether   │
│  this finding warrants replanning, maintenance, or dismissal.            │
└──────────────────────────────────────────────────────────────────────────┘
```

Background: `--state-info-bg`
Border-left: 3px `--state-info`; `border-radius: 0` on that side
`ℹ THIS IS A V FORGE FINDING`: `--type-sm`, `--weight-semibold`, `--state-info`
Body text: `--type-sm`, `--text-secondary`

This banner is non-dismissible. It remains visible in all sections while the trigger is unresolved. When the trigger is `routed` or `dismissed`, the banner is removed.

### 5.4 Section Content: Overview

The Overview section answers: what happened in execution, and why is it here?

**Layout:** Label/value pairs for metadata, followed by two structured prose blocks (Finding block and Execution state block).

**Metadata fields:**

```
Trigger ID:        rtn-04  (--font-mono)
From execution:    hosting-comparison-site  ·  [exec-entry-07]
Trigger type:      Changed condition
Arrived:           2026-04-01 08:22
Current state:     Reviewed — action pending
```

**Finding block:**

```
WHAT WAS FOUND
V Forge detected that the primary hosting provider (WP Engine) has changed
its enterprise pricing structure, increasing the cost tier relevant to the
comparison site's target audience segment.

This affects the accuracy of the hosting comparison content produced under
the approved execution scope.

Finding type:  changed_condition  ·  V Forge assessment: material to scope
```

- `WHAT WAS FOUND` label: `--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase, letter-spacing 0.3px
- Finding prose: `--type-sm`, `--text-primary`, `line-height: 1.6`
- `Finding type` metadata line: `--type-xs`, `--text-secondary`; finding type ID in `--font-mono`

**Execution state block:**

```
EXECUTION STATE AT TIME OF HALT
Execution halted at: Content production stage — 60% complete
What was complete:   Site architecture, initial keyword integration
What was NOT done:   Pricing comparison tables, provider ranking content
What was preserved:  Partial content graph ([page-14] through [page-22])

V Forge retains: All execution truth for hosted content produced to this point.
                 Partial content is not transferred to planning.
```

- `EXECUTION STATE AT TIME OF HALT` label: same structural label treatment
- "What was NOT done" line: `--text-secondary` — the "not done" is important; it tells the operator what remains incomplete, so they understand the impact scope
- `V Forge retains:` line: `--type-xs`, `--state-info` — reinforces the ownership boundary; V Forge has not surrendered the content it produced; this finding is an input to planning, not a transfer of execution state

### 5.5 Section Content: Evidence

The Evidence section shows the evidence V Forge cited in the finding and any VEDA signal that is relevant.

**Two sub-sections:**

**Execution-side finding evidence** (what V Forge used to detect the condition):

```
EXECUTION EVIDENCE — SOURCE: V FORGE FINDING
  [exec-ev-04]  WP Engine pricing page — captured 2026-04-01 07:50
                Type: Execution finding artifact  ·  Trust: high (direct observation)
                NOT a VEDA signal record — bounded to this execution finding
```

The `NOT a VEDA signal record` note is required by doctrine — execution evidence must not be confused with VEDA-sourced signal.

**VEDA signal currently loaded** (for operator context):

```
VEDA SIGNAL — CURRENTLY IN SESSION BASIS (referenced, not owned by Project V)
  [obs-041]  SERP delta — hosting vertical         ⚠ STALE — 6 days old
  [obs-047]  Hosting keyword intent snapshot        fresh — 2026-04-01 14:32
```

Using the same evidence row format as the handoff review Evidence section (§4.5). The staleness treatment is identical.

### 5.6 Section Content: Decisions

The Decisions section shows the governing decisions that were in effect when the original handoff was activated and when this finding arrived.

**Note at top:**
`Active at time of handoff activation: [date]  ·  Active at time of trigger arrival: [date]`
`--type-xs`, `--text-tertiary`

**Decision rows** using the same format as the handoff review §4.6, with the `Relevance to this finding` line:

```
[dec-03]  Prioritize search-first content strategy     [active]
          Relevance to this finding: The pricing change may affect which
          hosting providers best serve the search-first strategy. Routing
          this finding to planning may trigger a scope reconsideration.

[dec-07]  Hosting vertical — revised scope             [active]
          Relevance to this finding: This is the governing decision for
          the hosting comparison scope that was handed off. A price change
          at the provider level may require dec-07 to be reconsidered.
```

### 5.7 Section Content: History

The History section shows the return trigger lifecycle.

```
2026-04-01  08:22   Return trigger arrived from V Forge         [rtn-04]
                    V Forge routed: changed_condition — provider pricing.
                    State: arrived.

2026-04-03  09:30   Trigger reviewed by operator                [session-18]
                    Opened in center surface. State: acknowledged.
```

If the trigger is subsequently routed or dismissed, those events appear here. Same format as the handoff History section.

### 5.8 Section Content: Actions — The Most Important Part

The Actions section is where the operator makes their response. This section contains no approval gate widget — return trigger responses are not Class B approval events. They are routing decisions. The operator selects a response; the response is logged as a governance-relevant fact.

**Section structure:**

```
ACTIONS

Response options:

  [○ / ●]  Route to replanning
  [○ / ●]  Handle as maintenance
  [○ / ●]  Dismiss

──────────────────────────────────────────────────────

[Selected option expanded content — see §5.9]

──────────────────────────────────────────────────────

[Confirm Response]        ← becomes active after a response option is selected

──────────────────────────────────────────────────────

This response is a Class B governed action — it requires the approval gate.
[Proceed to Approval Gate]     ← only shown for Route to replanning option
```

**Response option selection anatomy:**

- Radio button metaphor: `○` hollow circle (unselected, `--text-tertiary`) → `●` filled (selected, `--accent-primary`)
- Option label: `--type-sm`, `--weight-medium`, `--text-primary` when selected; `--text-secondary` when unselected
- Row height: 36px
- Left padding: `--space-3` (12px)
- Hover: `--state-hover-overlay`

The `[Confirm Response]` button is inactive at `--state-disabled-opacity` until a response option is selected. This selection is also the **Response type selected** review checkpoint from Session 10 §8.4. The moment an option is selected: the checkpoint row in the checkpoint list (above the gate, if applicable) transitions to `✓`.

### 5.9 The Maintenance vs Replanning Distinction — Concrete Design

This is the most important design decision in Session 13. The work plan states: "The view must not flatten these two outcomes into a single undifferentiated `route to planning` action." The surface architecture doctrine requires the distinction to be visible and the response options semantically unambiguous.

**Option 1 — Route to replanning**

Label: `Route to replanning`

When selected, this expanded content appears below the option row:

```
●  Route to replanning

   This finding warrants a governed reconsideration of prior planning decisions.

   What this does:
   • Routes this finding to Project V through the governed return-to-planning interface
   • Initiates a formal replanning event — decision continuity is preserved, not reset
   • The governing decisions this finding affects must be explicitly reviewed
   • A new or revised handoff may follow replanning

   What this does NOT do:
   • Does not automatically change any planning decision or governing decision
   • Does not cancel or invalidate the prior handoff record
   • Does not transfer execution state to Project V
   • V Forge retains execution truth for work completed to this point

   Governing decisions that may be affected:
   [dec-03]  Prioritize search-first content strategy
   [dec-07]  Hosting vertical — revised scope

   This response requires Class B approval before routing proceeds.
   [Proceed to Approval Gate]
```

- "What this does" items: `--type-sm`, `--text-primary`, bullet `•` in `--accent-primary`
- "What this does NOT do" items: `--type-sm`, `--text-secondary`, bullet `•` in `--text-tertiary`
- Decision IDs in `--font-mono`, `--type-xs`
- `[Proceed to Approval Gate]`: amber border, `--accent-primary` text — the same routing CTA style used throughout the system. Clicking it routes to the Class B approval gate for this routing decision.

**Why `Route to replanning` is Class B:** Routing a finding to replanning is a governed status transition — it initiates a formal replanning event that will affect decision continuity. It is not a casual note. It requires a persisted approval event before the routing proceeds.

**Option 2 — Handle as maintenance**

Label: `Handle as maintenance`

When selected, this expanded content appears:

```
●  Handle as maintenance

   This finding can be addressed within the existing approved execution scope
   without reconsidering prior governing decisions.

   What this means:
   • V Forge continues execution within the current approved scope
   • The finding is resolved through bounded maintenance activity
   • No governing decisions need to be reconsidered
   • No replanning event is initiated

   Confirm that:
   ○  The finding does not invalidate any governing decision    ← operator must confirm
   ○  The resolution stays within the approved handoff scope    ← operator must confirm

   [Confirm Response]   ← becomes active after both confirmations are checked
```

The two confirmation checkboxes are required before `[Confirm Response]` activates for the maintenance option. They are literal checkboxes (not radio buttons) — the operator must explicitly confirm both conditions:

- Checkbox 1: `The finding does not invalidate any governing decision`
- Checkbox 2: `The resolution stays within the approved handoff scope`

Checkbox anatomy: `○` unchecked → `✓` checked; `--text-tertiary` → `--state-success`; label `--type-sm`, `--text-primary`. Clicking a label checks/unchecks the box.

**Why maintenance does not require Class B approval:** Handling a finding as maintenance is an acknowledgment that it is within approved scope. No new governed state transition is initiated. The maintenance response is logged as a governance-relevant fact (with the two confirmations) but does not require a separate persisted approval event.

**[PARTIAL SCHEMA BLOCK NOTE]** The maintenance vs replanning classification is routing decision logic whose downstream workflow stages (`Execution — Maintenance`, `Replanning — In Progress`) have no settled schema anchors. The routing decision itself is persisted as a governance-relevant fact tied to the return trigger record. The downstream stage derivation from that record is where the schema gap lives — and that is Session 15 territory. Session 13 designs the routing decision surface; it does not design the downstream maintenance or replanning workflow stages. Those stages are handled in Session 15 with explicit `[SCHEMA PENDING]` notation where applicable.

**Option 3 — Dismiss**

Label: `Dismiss`

When selected, this expanded content appears:

```
●  Dismiss

   This finding does not require action at this time.

   Reason (required):
   ┌──────────────────────────────────────────────────────────────────────┐
   │                                                                      │
   └──────────────────────────────────────────────────────────────────────┘
   Dismissal reason is required. It will be logged with the dismissal record.

   [Confirm Response]   ← active after reason is entered (min 10 characters)
```

Unlike the rejection reason prompt in the handoff gate (which is optional), the dismissal reason for a return trigger is **required**. Doctrine states: "Dismissal is logged as a governance-relevant fact." A reason-free dismissal weakens the audit trail. The `[Confirm Response]` button is inactive until at least 10 characters are entered in the reason field.

**Reason field:** `--surface-raised` background, `--border-default` border, `--type-base` (13px), `--text-primary`, placeholder `Enter reason for dismissal…` in `--text-tertiary`.

### 5.10 After `[Confirm Response]` Is Clicked

**For `Route to replanning`:** The operator is routed to the Class B approval gate (clicking `[Proceed to Approval Gate]` opens the relevant record detail with `intent = 'approval_gate'`). The return trigger record does not transition to `routed` until the approval is written and the routing API call succeeds.

**For `Handle as maintenance`:** `[Confirm Response]` writes the maintenance response record (logging the two confirmations). The trigger state transitions to `routed` (with subtype `maintenance`) immediately on write. A success toast fires per Session 12 §6 EVENT-16 state transition: `Return trigger routed — [rtn-id]. Maintenance response logged.` The non-authority notice banner and the response options section are replaced by a confirmation state:

```
●  Response recorded — Handle as maintenance
   Logged: 2026-04-03 09:47  ·  Both scope confirmations accepted
   V Forge may continue execution within approved scope.
```

`--state-success` icon; `--type-sm`, `--text-secondary` text.

**For `Dismiss`:** `[Confirm Response]` writes the dismissal record with the reason. The trigger state transitions to `dismissed`. A success toast fires: `Return trigger dismissed — [rtn-id]. Dismissal logged.` The section replaces with:

```
✗  Dismissed — 2026-04-03 09:50
   Reason: [logged reason text]
   Dismissal record written.
```

`--state-danger` `✗` icon (dismissal is not a failure, but the red keeps it distinct from approval-type success); `--type-sm`, `--text-secondary`.

### 5.11 Return Trigger Review Checkpoints

The return trigger review view does not have a Class B approval gate widget embedded in the Actions section for the trigger record itself (the gate only appears for the "Route to replanning" option, and it gates the routing decision, not the trigger review). The review checkpoints for the trigger are simpler:

```
Required review before responding:

  ✓  Overview section reviewed
  ✓  Governing decisions reviewed
  ○  Response type selected
```

Three checkpoints. The third — `Response type selected` — is satisfied when the operator clicks one of the three option rows. The `[Confirm Response]` button is the terminal action for maintenance and dismiss; the `[Proceed to Approval Gate]` is the terminal action for replanning routing.

---

## 6. States for Non-Actionable Return Triggers

When the return trigger is in `routed` or `dismissed` state (already resolved), the view is read-only. The non-authority notice banner is absent (the trigger is resolved). The Actions section shows the resolution record rather than the response options.

**Routed state — Actions section:**

```
RESPONSE RECORDED

  Route to replanning   ●  (selected)

  Routing approved: 2026-04-03 09:47  ·  Approval record [arp-04]
  Replanning initiated. Governing decisions under review.

  [View approval record ›]    [View replanning context ›]
```

**Dismissed state — Actions section:**

```
RESPONSE RECORDED

  Dismiss   ●  (selected)

  Dismissed: 2026-04-03 09:50
  Reason: The provider pricing change is within expected variance for the
          comparison scope. Execution can proceed with a note.

  [View dismissal record ›]
```

---

## 7. Synchronization with Other Surfaces

**When a handoff is activated (EVENT-05 fires after approval written):**
- Left nav handoff status badge updates from `awaiting approval` to `handed off`
- Context strip STAGE row updates to `Handoff — Activated`
- Center surface for the handoff record shows the post-activation state in its Actions section
- Right panel ARP card transitions to `APPROVED` label per Session 11 §9.3
- Success toast fires per Session 12 §6.4

**When the handoff basis changes during review (EVENT-02, EVENT-08):**
- Stale-basis warning banner fires in the handoff review surface inline banner position (§4.3)
- Gate widget controls return to `--state-disabled-opacity` if they were active
- Checkpoint `Context change notices acknowledged` reverts to `○` incomplete

**When a return trigger is routed (state → `routed`):**
- Left nav return trigger item in both V Forge and Project V trees updates to `returned to planning` / `routed` badge per Sessions 6, 8
- Context strip INTEGRITY row item resolves
- Topbar attention badge (return trigger badge, Element 6) decrements or clears
- Toast fires per Session 12 §6 EVENT-16 routed transition

**When a return trigger is dismissed (state → `dismissed`):**
- Same surface updates as routing, with `dismissed` state labels
- Dismissal logged as governance-relevant fact (required)

---

## 8. Token Usage from Session 2

No new tokens introduced.

| Element | Token(s) |
|---|---|
| `HANDOFF` record type badge | `--state-warning` text, 10% opacity bg, `--type-xs`, `--weight-bold` |
| `RTN TRIGGER` record type badge | `--state-danger` text, 10% opacity bg, `--type-xs`, `--weight-bold` |
| Stale-basis warning bg | `--staleness-bg` |
| Stale-basis warning border | `--staleness-border` (3px left) |
| Stale-basis warning header | `--type-sm`, `--weight-semibold`, `--staleness-text` |
| Stale-basis field labels | `--type-xs`, `--weight-semibold`, `--text-tertiary`, 140px min-width |
| `[Review Change]` link | `--text-link`, `--type-sm` |
| Scope block / Transfer block labels | `--type-xs`, `--weight-semibold`, `--text-tertiary`, uppercase, 0.3px letter-spacing |
| "What this does NOT transfer" prose | `--type-sm`, `--text-secondary` |
| Evidence record ID | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Evidence record title | `--type-sm`, `--text-primary`, `--weight-medium` |
| Evidence metadata line | `--type-xs`, `--text-secondary` |
| "Used as" / "Relevance to" lines | `--type-xs`, `--text-tertiary` |
| `⚠ STALE` inline marker | `--staleness-text`, `--type-xs` |
| `[Refresh Evidence]` / `[Load Evidence]` | `--text-link`, `--type-xs` |
| Evidence source ownership label | `--state-info` text, `--ownership-label-bg` fill |
| Decision ID | `--font-mono`, `--type-xs`, `--text-tertiary` |
| Decision title | `--type-sm`, `--text-primary`, `--weight-medium` |
| Decision `[active]` status | `--text-secondary` |
| Decision `[superseded]` status | `--state-warning` text |
| History timestamp | `--font-mono`, `--type-xs`, `--text-tertiary` |
| History event label | `--type-sm`, `--text-primary`, `--weight-medium` |
| History description line | `--type-xs`, `--text-secondary` |
| `NON-CANONICAL` history marker | `--continuity-bg` fill, `--continuity-label` text |
| Non-authority notice bg | `--state-info-bg` |
| Non-authority notice border | 3px `--state-info` left |
| Non-authority notice header | `--type-sm`, `--weight-semibold`, `--state-info` |
| Return trigger lifecycle badge (view header) | Per lifecycle state color table §5.2 |
| Response option `○` unselected | `--text-tertiary` |
| Response option `●` selected | `--accent-primary` |
| Response option label unselected | `--type-sm`, `--text-secondary` |
| Response option label selected | `--type-sm`, `--text-primary`, `--weight-medium` |
| "What this does" bullets | `--type-sm`, `--text-primary`; `•` in `--accent-primary` |
| "What this does NOT do" bullets | `--type-sm`, `--text-secondary`; `•` in `--text-tertiary` |
| Maintenance confirmation checkbox `○` | `--text-tertiary` |
| Maintenance confirmation checkbox `✓` | `--state-success` |
| Dismissal reason field | `--surface-raised` bg, `--border-default` border |
| `[SCHEMA PENDING]` notation | `--state-schema-hold` text (`--text-tertiary`), `--schema-pending-bg` fill |
| `[Confirm Response]` inactive | `--state-disabled-opacity` |
| `[Confirm Response]` active | Standard button treatment — `--surface-elevated`, `--border-default` |
| Post-response confirmation `●` | `--state-success` |
| Post-dismissal `✗` | `--state-danger` |

---

## 9. What Session 13 Resolves

- The Handoff Package Review View is fully specified: all five section tabs, exact content within each, stale-basis warning vocabulary (handoff-specific, distinct from the general staleness warning), the `Handoff — Prepared` vs `Handoff — Awaiting Approval` distinction implemented as a colored Status field, and the gate widget behavior for each handoff state.
- The stale-basis warning is concrete: it names which dimension of the handoff basis changed, rates the significance as material or informational, and either blocks or warns accordingly. It is not a generic "something changed" notice.
- The Return Trigger Review View is fully specified: all five sections, the non-authority notice banner (non-dismissible, persistent while unresolved), the three response options with named labels and expanded content.
- The maintenance vs replanning distinction is designed concretely with three named options (`Route to replanning`, `Handle as maintenance`, `Dismiss`) — not flattened into a single undifferentiated routing action. Each option has semantically unambiguous expanded content showing what it does and what it does not do.
- The `Handle as maintenance` option requires two explicit confirmations before proceeding. These enforce the doctrine requirement that maintenance activity must not be used to smuggle planning mutations that should go through the replanning workflow.
- The `Dismiss` option requires a written reason (minimum 10 characters). Dismissal without reason is not permitted.
- `Route to replanning` is identified as a Class B governed action — it requires an approval event before routing proceeds, consistent with the governance model for governed status transitions.
- The partial schema block for maintenance/replanning stage derivation is flagged explicitly — Session 13 designs the routing decision surface; Session 15 handles the downstream workflow stages where the schema gap lives.
- The `Response type selected` checkpoint mechanics are specified: selecting an option row satisfies the checkpoint; `[Confirm Response]` is the terminal action.
- Return trigger lifecycle state transitions on view open (`arrived → acknowledged`) and on response recorded (`→ routed | dismissed`) are specified, with their notification and surface synchronization consequences.

---

## 10. What Session 13 Does Not Resolve Yet

- **The downstream replanning workflow surface** — what happens after `Route to replanning` is approved and the trigger is routed. The operator enters a replanning flow in Project V. That flow's UX is Session 15 (Maintenance / Ranking UX). Session 13 specifies the routing decision; Session 15 specifies what the operator does in the replanning context.
- **The maintenance execution tracking surface** — what the operator sees when a finding is handled as maintenance and V Forge continues. Session 15.
- **The post-handoff activation surface** — after a handoff is activated, the center surface shows a confirmation state, but the operator may want to see what V Forge is doing with the handed-off scope. That view is the V Forge Execution Entry detail view, which is touched in Session 9's generic template but not specialized here.
- **Handoff rejection continuity** — when a handoff approval is rejected, the rejection record must appear in the History section. The History section format is specified, but the specific rejected-handoff event entry format (what the rejection record looks like in the history timeline) is a Session 9 generic template extension.
- **Evidence loading from the handoff review surface** — `[Load Evidence]` is specified as a link, but the evidence loading flow (where the operator goes to load a missing evidence record) is part of the broader evidence management surface that is not yet designed. Session 13 specifies the affordance; the target flow is deferred.
- **The Launch Readiness Review surface** — Session 14. The handoff review surface established the structural conventions (stale-basis warning, scope block with "what does NOT transfer," evidence sub-sections with ownership labels). Session 14 extends these conventions to the cross-system launch readiness context, where all three confirmation dimensions must be visible.

---

## 11. Recommended Inputs to Session 14

Session 14 is Launch Readiness UX — a partial schema block session.

**What Session 14 inherits from Session 13:**
- The stale-basis warning vocabulary (§4.3) is the template for the launch readiness stale-basis treatment. Session 14 should extend it with the launch-specific dimension: the Evidence Currency Principle from the launch readiness workflow requires evidence to be "current enough to be honest" for a launch-sensitive decision — the threshold is tighter than for a handoff.
- The "What this does NOT transfer" / "What this does NOT do" block pattern (§4.4) is the template for the launch readiness authorization modal's "What does NOT change" block (already specified in Session 10 §5.4 for the Class C modal). Session 14 should make the center workspace review surface's equivalent block consistent with that modal pattern.
- The three-dimension cross-system confirmation requirement (planning-side, evidence/signal, execution-side) from the launch readiness workflow is the primary structural differentiator of the launch readiness surface from the handoff surface. Session 14 must design this three-dimension checklist visibly and concretely — it cannot be collapsed into a single readiness indicator.

**Specific design questions for Session 14:**

What does the blocking conditions panel look like? The launch readiness workflow doctrine specifies that when a blocking condition exists, the workflow must stop and not proceed to authorization. Session 14 needs to design a blocking conditions panel within the launch readiness surface that names each blocking condition, what resolves it, and whether it is hard-blocking or soft-blocking.

How does the evidence staleness treatment differ from the handoff review? For handoffs, stale evidence is a material warning but the operator can acknowledge and proceed. For launch readiness, the Evidence Currency Principle applies with a conservative threshold — stale evidence at launch time carries higher cost than in ordinary planning. Session 14 should specify whether and under what conditions a `[Proceed Without Refreshing — I Accept the Risk]` option is available, and what acknowledgment logging that option requires.

How are the three schema-blocked stage names surfaced honestly? The work plan identifies `Launch Readiness — In Progress`, `Launch Authorization — Pending`, and `Post-Launch — Active` as having no settled schema anchors. Session 14 must show these with `[SCHEMA PENDING]` notation where derivation fails, not paper over the ambiguity.
