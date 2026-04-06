# Session 11 — Review-to-Gate Routing Flow
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–10 (all shell surfaces, gate surfaces, and checkpoint model fully specified)
**Required before:** Sessions 12–15 (every workflow surface uses this routing pattern; Session 12 references the right-panel card staleness marker vocabulary defined here)

---

## 1. Files Read

**Prior sessions:**
- `session-02-minimal-token-decisions.md` — active token baseline
- `session-05-right-panel-shell-spec.md` — `[Proceed to Approval Gate]` button on ARP cards specified as accent-border navigation action; interaction area card staleness marker treatment; card persistence in interaction area
- `session-09-center-workspace-foundation-spec.md` — workspace router; `intent = 'approval_gate'` routing behavior; inline banner position; tab-based navigation; Actions section as gate location; detail view opening rules
- `session-10-approval-gate-surfaces-spec.md` — Class B inline gate widget (all states); Class C modal gate (all states); typed confirmation input; Class D escalation banner; checkpoint model; staleness warning treatment above gate; post-approval state; `[Proceed to Activation ›]` button; `--transition-spring` activation animation

**Doctrine:**
- `interfaces/desktop-governance-and-gating-model.md` — approval event definition; approval record must be written before activation call; review is not approval; activation is distinct from approval; rejection must be persisted; stale approval detection before gate presentation; structural enforcement requirements
- `interfaces/desktop-surface-architecture.md` — review-before-gate routing rule (the canonical five-step sequence); approval gate widget must not appear in right panel, left nav, or topbar; gate available only after operator is in center review surface and checkpoints are complete
- `interfaces/desktop-human-llm-interaction-model.md` — Approval Request Package is inert output; `[Proceed to Approval Gate]` CTA routes to review, not to approval; operator is accountable party

**Workflow docs:**
- `workflows/handoff-workflow.md` — handoff awaiting-approval vs prepared distinction; what the routing flow looks like for the most common Class B gate
- `workflows/launch-readiness-workflow.md` — cross-system confirmation requirement; what the routing flow looks like for the Class C gate

---

## 2. Session 11 Scope Confirmation

The work plan defines Session 11 — Review-to-Gate Routing Flow as: the single canonical routing pattern from typed output card to completed approval event.

This session produces:
- The canonical five-step flow, fully specified with all transitions and states
- The right-panel card in its pre-navigate inert state
- The center surface during review (gate inactive)
- The center surface when checkpoints complete (gate activates)
- The center surface during typed confirmation (Class C only)
- The center surface after approval written (confirmation state)
- Right-panel card staleness markers if context changed during review
- The context-changed-since-recommendation notice, both standard and severe-change variants
- Resolution of the open question from Session 10: card persistence in the right panel during and after navigation to center workspace
- The activation path: UX state during activation, success state, failure treatment

This session does not:
- Redesign the gate widget (Session 10 is the authoritative source)
- Design the notification that fires when an approval is written (Session 12)
- Design the handoff review surface content (Session 13)
- Design the launch readiness review surface content (Session 14)
- Invent new approval paths outside doctrine

---

## 3. The Canonical Flow — Overview

The surface architecture doctrine defines the review-before-gate routing rule as five steps. This session makes those five steps fully concrete.

```
Step 1  LLM produces Approval Request Package in right panel
        → ARP card appears with [Proceed to Approval Gate] CTA
        → Card is inert: AWAITING REVIEW treatment

Step 2  Operator clicks [Proceed to Approval Gate]
        → Center workspace opens to the relevant review surface
        → Right-panel card remains visible; persists in interaction area

Step 3  Operator reviews full record/package/evidence in center surface
        → Gate widget visible but inactive (checkpoints incomplete)
        → Operator works through required review checkpoints

Step 4  Operator completes required review checkpoints
        → Gate widget activates (--transition-spring)
        → Operator uses gate widget to create persisted approval record
        → For Class C: [Proceed to Authorization Gate] button activates
          → Modal opens → typed confirmation → [Confirm Authorization]
          → Approval record + confirmation log written

Step 5  Approval written → confirmation state in center surface
        → [Proceed to Activation ›] available
        → Right-panel ARP card updates to reflect approval
        → Activation path opens
```

This flow applies universally — handoff activation, launch authorization, paid data pull, return trigger routing, and every other Class B or Class C gate. Individual workflow surfaces (Sessions 13–15) will apply this pattern to their specific record types; this session specifies the pattern itself.

---

## 4. Step 1 — LLM Produces Approval Request Package in Right Panel

### 4.1 Card Appearance

When the LLM produces an Approval Request Package (ARP), it appears as a distinct typed output card in the right panel's interaction/output area. The card anatomy is established by Session 1 (Output Card System); this session specifies the card's visual state at the routing moment.

**Card header:**
```
APPROVAL REQUEST PACKAGE              [CLASS B]
```
or
```
APPROVAL REQUEST PACKAGE              [CLASS C]
```

- `APPROVAL REQUEST PACKAGE`: `--type-xs`, `--weight-bold`, `--text-tertiary`, letter-spacing 0.3px — the output type label treatment
- Class badge: rendered using Session 2 badge tokens — `--badge-class-b` / `--badge-class-c` background + text per class
- `AWAITING REVIEW` inertness label appears below the output type label: `--type-xs`, `--weight-normal`, `--inert-label-bg` fill, `--inert-label-text` color — this is the Session 2 inertness treatment applied to ARP cards specifically

**Card body fields** (in order):

| Field | Content |
|---|---|
| `Action:` | The specific action being requested — bounded and precise |
| `Scope:` | What the action covers and what it does not |
| `Basis:` | Why this action is recommended now — evidence and decision references |
| `Covers:` | What approval grants |
| `Default:` | What happens if the operator does not approve |

Field labels: `--type-xs`, `--weight-semibold`, `--text-tertiary`, minimum width 60px.
Field values: `--type-sm`, `--text-primary`.

**Orchestration attribution** (if the ARP was assembled with delegated-worker contribution):
A small attribution line below the body: `Packaged with orchestration contribution — [task ID]` in `--type-xs`, `--text-tertiary`. Non-clickable, read-only attribution per Session 5's absent-affordance for attribution stripping.

### 4.2 The `[Proceed to Approval Gate]` CTA

This is the primary response option on an ARP card. It is visually distinguished from secondary response options on the same card.

**Treatment:**
- Label: `[Proceed to Approval Gate]` — exact wording; not `[Approve]`, not `[Start Approval]`, not `[Review]`. The label makes explicit that clicking routes to a review surface, not to an approval event.
- Border: 1px `--border-accent` (`--accent-primary`)
- Text: `--accent-primary`, `--type-xs`, `--weight-medium`
- Background: transparent resting; `--state-selected-bg` (amber at 12%) on hover
- Height: 28px
- Border-radius: `--radius-md` (4px)
- Padding: `--space-2` (8px) horizontal

**Why amber border, not amber fill:**
The `[Approve]` button in the Class B gate widget uses amber fill (established in Session 10) because it is the final decisive governance action. The `[Proceed to Approval Gate]` CTA uses only amber border because it is a navigation action — the operator is going somewhere, not doing something. The visual distinction between "navigate toward approval" (amber border) and "approve" (amber fill) is structural and must not drift.

**Secondary response options** on the same card (optional, record-type-specific):
- `[Not now — I'll review later]`: `--surface-elevated`, `--border-default`, `--text-secondary` — moves the card to a deferred state (card remains in the interaction area, CTA dims, `DEFERRED` label replaces `AWAITING REVIEW`)
- `[Flag for discussion]`: same treatment — marks the card with a `FLAGGED` annotation in `--state-warning`

These secondary options are always lower-weight than the primary `[Proceed to Approval Gate]` CTA and must not be styled in a way that makes them look like reasonable alternatives to proceeding.

### 4.3 Card Inertness Treatment

The ARP card in its `AWAITING REVIEW` state communicates that it is not yet actionable in any governance sense. The card body content is readable and complete. But the `AWAITING REVIEW` treatment signals that this output has not yet been acted upon.

`AWAITING REVIEW` label:
- Position: directly below the `APPROVAL REQUEST PACKAGE` type label, above the card body
- Background: `--inert-label-bg` (rgba(97,97,97,0.15))
- Text: `--inert-label-text` (`--text-tertiary`), `--type-xs`, `--weight-normal`
- Padding: `--space-1` (4px) horizontal, 2px vertical
- Border-radius: `--radius-sm` (2px)

The card's `AWAITING REVIEW` state is the default when the ARP card is first rendered. It changes when the operator takes a response action (navigate, defer, flag).

---

## 5. Step 2 — Operator Clicks `[Proceed to Approval Gate]`

### 5.1 What Happens to the Right Panel Card

**Resolution of the Session 10 open question:** The ARP card **remains visible in the right panel interaction area** during and after the operator navigates to the center workspace. It does not disappear. It does not scroll away. It persists in its current position in the card list.

Rationale: The right panel is the operator's session record. Output cards are the history of what the LLM produced during the session. Removing a card because the operator navigated to act on it would create a continuity gap — on returning to the right panel, the operator would find no record of what they were working on. The card stays.

**Card state change on click:**
- The `AWAITING REVIEW` label is replaced with `IN REVIEW` — `--state-info` (#00b0f4), same visual treatment as `AWAITING REVIEW` but in info color. This signals: the operator has started the review process.
- The `[Proceed to Approval Gate]` CTA remains visible but transitions to a navigation affordance state: `[Return to Gate →]` label replaces `[Proceed to Approval Gate]`, same amber border treatment. This allows the operator to return to the center workspace gate view if they navigate away and come back to the right panel.
- The card body fields remain fully readable and unchanged.

**Right-panel focus:** Clicking the CTA opens the center workspace view. The right panel does not collapse and does not change width. The operator can see both surfaces simultaneously (right panel interaction area on the right; center workspace on the left) at the default panel configuration.

### 5.2 What Happens in the Center Workspace

The workspace router receives `navigate(recordType, recordId, intent='approval_gate')`.

**Router behavior:**
1. Checks if the record is already open in an existing tab — if yes, activates that tab and scrolls to the Actions section
2. If not open: opens a new center workspace tab for the record; tab label shows the record type badge + record title
3. The Actions section tab is set as the initial active section (intent-aware routing behavior from Session 9)
4. The view loads; the Actions section is visible; the gate widget is at the bottom of the section in inactive state; the checkpoint list is visible above it
5. Scroll position: the view initially shows the Actions section tab content from the top — the operator sees the checkpoint list first, then scrolls down to the gate widget

**Tab label:**
```
[HANDOFF]  hosting-comparison-site  ×
```
Record type badge (amber at 10% bg, `--state-warning` text for handoffs per Session 9 record type identifiers) + truncated record title + `×` close affordance.

**The view does not scroll to the gate widget on open.** The operator lands at the top of the Actions section, sees the checkpoint list, and understands what review is required. The gate widget is visible below the fold — the operator must scroll to see it. This is intentional: the operator's attention is first directed to what they need to do (checkpoints), not to the control they want to use (gate).

---

## 6. Step 3 — Operator Reviews Full Record in Center Surface (Gate Inactive)

### 6.1 Actions Section on Arrival

The operator arrives at the Actions section with the gate in inactive state. The section shows:

```
ACTIONS

Available governed actions:
  [CLASS B]  Activate handoff                    Route through governed path
  [CLASS A]  Copy record ID                      Immediate, no gate

──────────────────────────────────────────────────────

Required review before approving:

  ○  Overview section reviewed
  ○  Governing decisions reviewed
  ○  Evidence basis reviewed
  ✓  Context change notices acknowledged          ← auto-satisfied (no active warnings)

──────────────────────────────────────────────────────

[GATE WIDGET — INACTIVE]

APPROVAL REQUEST                                      [CLASS B]
Action:    Activate handoff — hosting-comparison-site
Scope:     Handed-off scope as defined in hdl-07
Basis:     Planning readiness confirmed; 3 of 3 gaps resolved
Covers:    Transfer of execution responsibility to V Forge
Default:   Handoff remains in Awaiting Approval state if not approved

─────────────────────────────────────────────────────────────────

○  Complete required review before approving

[Approve ░░░]    [Reject ░░░]    [Defer ░░░]        ← disabled (░░░ = dim)
```

**Checkpoint list anatomy in full:**

Each checkpoint row:
- Height: 32px
- Left padding: `--space-3` (12px)
- Icon: `○` (incomplete) or `✓` (complete), 16px, with `--space-2` (8px) right margin
- Label: `--type-sm`, `--text-tertiary` (incomplete) / `--text-primary` (complete), `--weight-normal`
- No hover state on individual checkpoint rows — they are status indicators, not interactive elements
- The checkpoint list has a top and bottom hairline divider (`--border-subtle` 1px) separating it from the available actions list above and the gate widget below

**Available governed actions list anatomy:**

Each action row:
- Class badge: rendered per Session 2 badge tokens, left-aligned
- Action label: `--type-sm`, `--text-primary`, `--weight-medium`
- Brief description: `--type-xs`, `--text-tertiary`, same row

Class A actions in this list are immediately actionable (no gate). Class B and C actions in this list have a `[Go to gate ›]` affordance that, when clicked, scrolls the operator to the gate widget below. This redundant navigation affordance is for cases where the operator has already completed review and wants to jump directly to the gate rather than scrolling manually.

### 6.2 Navigating to Other Sections for Review

The operator clicks the section tabs to navigate:

**Overview tab:** Operator reviews record identity, status, key metadata. The 5-second timer for the Overview checkpoint begins when this tab becomes active. The operator does not see a timer countdown — the checkpoint status in the Actions section simply does not update to `✓` until the timer completes. If the operator leaves before 5 seconds and returns, the timer restarts.

**Evidence tab:** Operator reviews evidence records. Staleness markers on evidence items use the Session 4 context strip evidence treatment — `⚠ STALE — Nh ago` appended inline. If the evidence basis reviewed checkpoint requires interacting with a stale evidence item's expand affordance, the operator must do so before the checkpoint satisfies.

**Decisions tab:** Operator reviews governing decisions. The Session 4 context strip decisions treatment applies here too — decision IDs in `--font-mono`, `--type-xs`, conflict markers if active.

**History tab:** Read-only. No checkpoint is attached to History review — it is available for context but not required.

**Actions tab:** Returns the operator to the checkpoint list and gate widget. This is where the flow completes.

**Section tab state during review:**

Active tab (operator is currently viewing):
- Bottom border: 2px `--border-accent` (`--accent-primary`)
- Label: `--text-primary`, `--weight-medium`

Reviewed tab (checkpoint satisfied — applicable sections only):
- A small `✓` appears after the section label: `Overview ✓`
- Label remains `--text-primary`
- Bottom border returns to neutral (no special treatment for reviewed but not active)

Unreached tab (not yet visited):
- Label: `--text-secondary`, `--weight-normal`
- No bottom border

The `✓` on reviewed section tabs provides ambient confirmation that the operator has completed review requirements for that section, without forcing them back to the Actions section to check. They can see their progress across the tab strip without interrupting their review flow.

### 6.3 Context Strip Behavior During Review

While the operator is in the center workspace reviewing, the right panel's context strip remains live and synchronized. If any of the 18 invalidation events fires during the review:

- The context strip updates immediately per its established behavior (Sessions 4, 9)
- If the event is relevant to the record under review, an inline banner fires in the center workspace inline banner position (between view header and section nav)
- The relevant checkpoint may revert to incomplete if the change invalidates the review the operator had already completed (e.g., if a governing decision is superseded — EVENT-02 — after the operator satisfied the "Governing decisions reviewed" checkpoint, that checkpoint reverts to `○`)

The operator is not punished for events that occur during review — the checkpoints revert to protect the governance posture, not to frustrate the operator. The staleness warning treatment from Session 10 §4.7 fires if the change is relevant to the approval basis.

---

## 7. Step 4a — Operator Completes Required Checkpoints (Class B: Gate Activates)

### 7.1 Checkpoint Completion and Gate Activation Sequence

When the final required checkpoint satisfies, the following occurs in this exact sequence:

**1. Checkpoint row updates:**
The completing checkpoint row transitions from `○` incomplete to `✓` complete.
- Icon: `○` `--text-tertiary` → `✓` `--state-success`; transition: `--transition-fast` (150ms)
- Label: `--text-tertiary` → `--text-primary`; transition: `--transition-fast`

**2. Checkpoint status line updates:**
`○ Complete required review before approving` → `✓ Required checkpoints complete — gate is active`
- Icon: same `○` → `✓` transition
- Text color: `--text-tertiary` → `--text-secondary`; transition: `--transition-default` (200ms)

**3. Gate widget activates:**
The gate widget transitions from inactive to active. The `--transition-spring` animation fires on the widget's border and shadow:
- Border: `--border-default` → `--border-accent`; transition: `--transition-spring` (200ms cubic-bezier(0.215,0.61,0.355,1))
- Box-shadow: none → `--gate-active-shadow` (0 0 0 2px rgba(255,214,79,0.25)); transition: `--transition-spring`

**4. Controls activate:**
The three controls (`[Approve]`, `[Reject]`, `[Defer]`) transition from `--state-disabled-opacity` (0.4) to full opacity simultaneously:
- Transition: `--transition-default` (200ms ease)
- Cursor: `not-allowed` → `pointer`

**5. Scroll behavior:**
When the gate activates, if the gate widget is below the visible area of the Actions section (the operator is viewing a different section or has not scrolled to the gate), the application performs a smooth scroll to bring the gate widget into view.
- Scroll behavior: `scroll-behavior: smooth` equivalent; approximately 300ms ease
- Scroll target: the top of the gate widget, with `--space-4` (16px) clearance above it (not flush to top of viewport)
- This scroll does not interrupt anything the operator is doing — it is a gentle notification that the gate is now ready

The scroll-to-gate behavior only fires once: at the moment the final checkpoint is satisfied. If the operator has already scrolled to the gate widget manually, the scroll is a no-op (the element is already visible).

**The sequence is fast and quiet.** The four transitions happen within 200ms total. There is no sound, no celebration badge, no modal. The gate simply becomes available. The amber spring-eased border change and the soft scroll are the only signals.

### 7.2 Gate Widget in Active State (Full Specification)

With all checkpoints satisfied and no staleness warnings blocking, the gate widget in active state:

```
┌─────────────────────────────────────────────────────────────────────────┐  ← --border-accent 1px
│  APPROVAL REQUEST                                          [CLASS B]     │    --gate-active-shadow
│                                                                          │
│  Action:    Activate handoff — hosting-comparison-site                   │
│  Scope:     Handed-off scope as defined in hdl-07                        │
│  Basis:     Planning readiness confirmed; 3 of 3 gaps resolved           │
│  Covers:    Transfer of execution responsibility to V Forge              │
│  Default:   Handoff remains in Awaiting Approval state if not approved   │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ✓ Required checkpoints complete — gate is active                        │
│                                                                          │
│  [Approve]          [Reject]          [Defer]                            │
└─────────────────────────────────────────────────────────────────────────┘
```

Controls are fully active. The operator may click any of the three.

**If a staleness warning is present (context changed since ARP was produced):**
The stale-context warning block appears between the checkpoint status line and the controls, per Session 10 §4.7. The controls remain at `--state-disabled-opacity` until the operator clicks `[I have reviewed the change — proceed to gate]`. The warning block's presence does not change the checkpoint status line — checkpoints can be complete while a staleness warning blocks the controls. These are two independent blocking conditions.

### 7.3 Operator Clicks `[Approve]`

**Immediate UI response (before write confirms):**

The `[Approve]` button enters a loading state:
- Button shows a subtle inline loading indicator: three dots animating in sequence (same pattern as the right-panel generation indicator from Session 5 — `--text-inverse` dots on the amber fill background)
- Button text `Approve` is replaced by `···` during the write
- `[Reject]` and `[Defer]` buttons become disabled at `--state-disabled-opacity` during the write
- Duration: typically < 1 second; the write must complete before UI updates further

**On write success:**

The gate widget transitions to its post-approval state (Session 10 §4.6):

```
┌─────────────────────────────────────────────────────────────────────────┐
│  APPROVAL REQUEST                                          [CLASS B]     │
│                                                                          │
│  Action:    Activate handoff — hosting-comparison-site                   │
│  [... summary fields unchanged ...]                                      │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ✓ APPROVED — 2026-04-03 09:47  ·  Approval record written              │
│                                                                          │
│  [Proceed to Activation ›]                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

- The three controls are replaced by the confirmation line + `[Proceed to Activation ›]`
- Confirmation line: `✓ APPROVED — [timestamp]  ·  Approval record written`; `--state-success`, `--type-sm`, `--weight-semibold`
- Timestamp: `--font-mono`, `--type-xs` embedded in the line, same color
- `[Proceed to Activation ›]`: amber border, `--accent-primary` text, `--radius-md` — the navigation-forward treatment consistent with all governed routing CTAs in the system
- Widget border retains `--border-accent`; shadow retains `--gate-active-shadow`

**On write failure:**

If the approval record write fails (network error, API rejection, session boundary error):

- Button returns to its normal active state (not loading)
- An inline error notice appears below the checkpoint status line:

```
⚠ Approval record write failed — please retry
[Retry]   The gate remains open. Your review is preserved.
```

- `⚠`: `--state-warning`, `--type-sm`
- Notice text: `--type-sm`, `--text-secondary`
- `[Retry]`: `--text-link`, `--type-sm` — clicking re-attempts the write
- The gate widget remains in active state; all checkpoints remain satisfied; the operator does not need to re-review
- If the failure is due to a session error (EVENT-10): the session error treatment takes precedence — the center surface shows the session error scrim, and the gate is blocked along with all other Class B/C actions

### 7.4 Operator Clicks `[Reject]`

The rejection reason prompt opens inline below the controls per Session 10 §4.5.

**After rejection is confirmed and rejection record written:**

The gate widget transitions to a post-rejection state:

```
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ✗ REJECTED — 2026-04-03 10:02  ·  Rejection record written             │
│  Reason: Blocking gap [gap-14] was not resolved                          │
│                                                                          │
│  Continuation options:                                                   │
│  [Revise and Resubmit]     [Defer — I'll return to this]     [Escalate] │
└─────────────────────────────────────────────────────────────────────────┘
```

- Rejection confirmation line: `✗ REJECTED — [timestamp]  ·  Rejection record written`; `--state-danger`, `--type-sm`, `--weight-semibold`
- Reason line (only if reason was provided): `--type-sm`, `--text-secondary`
- Continuation options row: three lower-weight options styled as text links or subdued buttons — `--text-link` treatment, `--type-sm`
- `[Revise and Resubmit]`: routes the operator back to the right panel to request a revised ARP from the LLM; the existing ARP card in the right panel receives a `REJECTED` status label treatment
- `[Defer — I'll return to this]`: logs a defer event; leaves the record detail view open; the gate widget remains in its rejected state
- `[Escalate]`: opens the escalation path for cases where rejection is because governance posture is unclear (routes toward Class D handling)

**The rejected gate widget does not offer `[Approve]` again.** If the operator wants to approve the action after a rejection, they must request a new ARP from the LLM (which creates a new governed packaging), then navigate to the gate from the new ARP card. A prior rejection does not prevent future approval — it is a record, not a permanent block. But the rejected gate widget itself does not offer a second approval path.

### 7.5 Operator Clicks `[Defer]`

The gate widget returns to its inactive state with a modified checkpoint status line:

```
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ◷ Deferred — review is preserved; return when ready                    │
│                                                                          │
│  [Resume ›]           [Reject this request instead]                     │
└─────────────────────────────────────────────────────────────────────────┘
```

- `◷` clock glyph: `--text-tertiary`, `--type-sm`
- Defer status text: `--type-sm`, `--text-secondary`
- `[Resume ›]`: restores the gate widget to active state; all checkpoints remain satisfied (defer does not invalidate review); re-checks for staleness before showing active controls
- `[Reject this request instead]`: routes to the rejection reason prompt as if `[Reject]` had been clicked

Defer does **not** write a record unless the operator then returns and explicitly approves or rejects. A deferred gate is in a held state — neither governed outcome has occurred.

---

## 8. Step 4b — Class C Gate Specific: Modal Gate Sequence

For Class C actions, Step 4 has an additional phase between checkpoint completion and approval event.

### 8.1 `[Proceed to Authorization Gate]` Becomes Available

When all Class C checkpoints are satisfied (the full set from Session 10 §8.6 — which is the complete Class B checkpoint set plus the Class C-specific additional checkpoints), a `[Proceed to Authorization Gate]` button appears in the Actions section, **above** the gate widget position:

```
ACTIONS

[CLASS C]  Launch activation — content-hub-v1     Route through governed path

──────────────────────────────────────────────────

Required review before authorizing:

  ✓  Overview section reviewed
  ✓  Governing decisions reviewed
  ✓  Planning-side readiness reviewed
  ✓  Evidence and signal reviewed
  ✓  Execution-side verification confirmed
  ✓  Cross-system confirmation complete
  ✓  Context change notices acknowledged

──────────────────────────────────────────────────

  ✓ All required checkpoints complete

  [Proceed to Authorization Gate]

──────────────────────────────────────────────────

[Gate widget — inactive until modal completes]
```

`[Proceed to Authorization Gate]`:
- Width: 240px
- Height: 40px (slightly taller than standard 36px controls — this is the entry to the most consequential gate)
- Background: `--surface-elevated`
- Border: 1px `--border-accent` (`--accent-primary`)
- Text: `--accent-primary`, `--type-sm`, `--weight-bold`
- Border-radius: `--radius-md`
- Hover: `--state-selected-bg` (amber at 12%)
- This button is centered below the checkpoint list, above the gate widget

**The Class C gate widget below is shown as inactive** even when all checkpoints are satisfied. The modal gate is the activation mechanism for Class C — the gate widget becomes a read-only confirmation record after the modal completes. The operator does not interact with the inline gate widget directly for Class C.

### 8.2 Operator Clicks `[Proceed to Authorization Gate]`

The Class C modal opens. Per Session 10 §5:
- Scrim (`--surface-overlay` at 80%) covers the center workspace and surrounding surfaces
- Modal appears centered in the viewport
- Modal initial focus is set to the modal container (not the typed confirmation input — the operator must read before typing)
- `Escape` key does not close the modal
- Outside-modal click on scrim does nothing

**The center workspace behind the scrim remains visible** through the semi-transparent overlay. The operator can see the review surface they worked through. This is intentional — the connection between "I reviewed this" and "I am now authorizing this" is made visible by the scrim treatment rather than being a full-blind overlay.

The right panel is also partially covered by the scrim (the scrim is full-screen at `--z-modal: 500`, above the right panel's `--z-panel: 200`). The right panel's ARP card remains in the interaction area but is covered during the modal.

### 8.3 Operator Completes Typed Confirmation and Clicks `[Confirm Authorization]`

**Immediate response (before write confirms):**
Same loading state pattern as Class B `[Approve]` — `[Confirm Authorization]` button shows loading indicator; `[Cancel]` button becomes disabled.

**On write success (approval record + confirmation log written):**

The modal closes. The scrim fades out (`--transition-fade`, 300ms ease opacity). The center workspace returns to full visibility.

The Actions section now shows the Class C post-authorization state:

```
  ✓ AUTHORIZED — 2026-04-03 11:22  ·  Authorization record written

  [Proceed to Activation ›]
```

The inline Class C gate widget (below the modal-activation button) also transitions to a read-only confirmation record:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  AUTHORIZATION REQUEST                                     [CLASS C]     │
│  [... summary fields ...]                                                │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ✓ AUTHORIZED — 2026-04-03 11:22  ·  Authorization + confirmation log   │
│    written                                                               │
│                                                                          │
│  [Proceed to Activation ›]                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

### 8.4 Operator Clicks `[Cancel]` in the Modal

The modal closes. The scrim fades out. The center workspace returns to full visibility.

The `[Proceed to Authorization Gate]` button is restored to its pre-click state. All checkpoints remain satisfied. The operator may re-open the modal immediately by clicking `[Proceed to Authorization Gate]` again.

No record is written. No governance event occurs. The approval request package remains in its pending state.

The right-panel ARP card: `IN REVIEW` label remains. The `[Return to Gate →]` CTA remains.

---

## 9. Step 5 — Approval Written: Confirmation State and Activation Path

### 9.1 Center Surface Confirmation State

After the approval record (Class B) or authorization record + confirmation log (Class C) is successfully written, the center surface is in its confirmation state as specified in Session 10 §4.6 / §8.3.

The `[Proceed to Activation ›]` button is the terminal action in the center surface. It triggers the activation path.

**`[Proceed to Activation ›]` — full specification:**
- Label: `Proceed to Activation ›` — exact wording; the `›` glyph signals forward routing
- Width: 200px
- Height: 36px
- Background: transparent
- Border: 1px `--border-accent` (`--accent-primary`)
- Text: `--accent-primary`, `--type-sm`, `--weight-medium`
- Border-radius: `--radius-md`
- Hover: `--state-selected-bg` (amber at 12%)

### 9.2 Activation Flow (UX States)

The activation sequence is: write approval record → confirm write → call activation API. The UX state follows each step:

**During activation API call:**

`[Proceed to Activation ›]` enters a loading state:
- Button shows inline loading indicator (`···` animation)
- A brief status line appears below the button: `Activating…` in `--text-tertiary`, `--type-xs`

**On activation success:**

The record detail view shows the activation success state:

```
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ✓ AUTHORIZED — 2026-04-03 09:47  ·  Approval record written            │
│  ✓ ACTIVATED — 2026-04-03 09:47  ·  Execution responsibility transferred │
│                                                                          │
│  The activated scope is now in V Forge execution.                        │
│  This record has been updated to reflect the transition.                 │
│                                                                          │
```

- Two confirmation lines: the prior `✓ APPROVED/AUTHORIZED` line, plus a new `✓ ACTIVATED — [timestamp]  ·  [brief consequence statement]`
- Both lines: `--state-success`, `--type-sm`, `--weight-semibold`
- Consequence statement: a brief literal description of what has transferred — "Execution responsibility transferred" for handoffs, "Launch-sensitive execution has begun" for launch authorization, etc.
- A short read-only context note below: `--type-sm`, `--text-secondary` — confirms what system now owns the activated scope
- `[Proceed to Activation ›]` button is replaced by nothing — the activation is complete; no further action is available in this surface

The record's left-nav tree item updates simultaneously (e.g., handoff status badge changes from `awaiting approval` to `handed off`). The context strip INTEGRITY row clears the relevant pending-approval item. These synchronization events fire per doctrine without requiring additional operator action.

**On activation failure (API rejection):**

The activation API rejected the call — most commonly because the approval record was not found or was already used.

```
│  ✓ APPROVED — 2026-04-03 09:47  ·  Approval record written              │
│  ✗ ACTIVATION FAILED                                                     │
│                                                                          │
│  The activation API rejected the call.                                   │
│  Reason: [API-returned reason]                                           │
│                                                                          │
│  [Retry Activation]    [View Approval Record]    [Contact Support]       │
```

- `✗ ACTIVATION FAILED`: `--state-danger`, `--type-sm`, `--weight-semibold`
- Reason: displayed verbatim from the API response where available; `--type-sm`, `--text-secondary`
- The approval record confirmation line (`✓ APPROVED`) remains — the approval was written; it is the activation that failed. These are recorded as distinct events.
- `[Retry Activation]`: re-attempts the API call; shown in `--text-link` treatment
- `[View Approval Record]`: navigates to the approval record in a new center workspace tab — the operator can confirm the record was actually written
- `[Contact Support]`: `--text-tertiary`, non-link — a placeholder for the support escalation path; exact target is implementation-specific

The critical design rule here: **the approval record is not unwound on activation failure.** The approval event is a separate persisted record from the activation. The UI makes this explicit by keeping the `✓ APPROVED` line visible while showing the `✗ ACTIVATION FAILED` line. The operator and any future auditor can see: approval happened, activation did not.

### 9.3 Right Panel ARP Card Update After Approval Written

When the approval record is written and the center surface shows its confirmation state, the right-panel ARP card updates:

**Card label change:**
- `IN REVIEW` label (set in Step 2) → `APPROVED` label
- `APPROVED`: `--state-success` (#11b76b) text, same visual treatment as `AWAITING REVIEW` / `IN REVIEW` but in success color
- For Class C: `AUTHORIZED` label in `--state-success`

**CTA change:**
- `[Return to Gate →]` CTA (set in Step 2) is replaced by `[View Approval Record ›]`
- `[View Approval Record ›]`: `--border-default`, `--text-secondary`, `--type-xs` — subdued treatment; this is a historical navigation link, not a call to action
- Clicking it opens the approval record (a governed record in its own center workspace tab) — for the operator or future session reference

**Card body fields:** Unchanged. The approval request summary remains visible as the session record of what was requested.

**The card does not disappear from the interaction area.** It is now a historical record of what was approved and when. In a long session, the operator may have multiple approved ARP cards in the interaction area — this is correct; they represent the governance trail of the session.

**For Class B rejected actions:**
- `IN REVIEW` → `REJECTED`: `--state-danger` (#fa4362) text
- `[Return to Gate →]` → `[View Rejection Record ›]`: same subdued treatment

---

## 10. Context-Changed-Since-Recommendation Notice

This is a universal condition in the routing flow: context can change between when the LLM produced the ARP and when the operator arrives at the gate. The routing flow must surface this honestly before the gate is reachable.

### 10.1 Standard Context Change

**Where it appears:** As the stale-context warning block above the gate widget controls, per Session 10 §4.7. It appears in the Actions section of the center review surface, between the checkpoint status line and the gate controls.

**When it appears:** When the application detects that any of the following has changed since the ARP was produced:
- A governing decision was created, superseded, or invalidated (EVENTs 01, 02, 03)
- Evidence that the ARP cited is now stale (EVENT-08)
- The workflow stage has changed (EVENT-17)
- A readiness state has changed materially
- New blocking gaps have opened at blocking or critical severity
- A material change in VEDA signal for the scope being approved

**Content:**

```
┌──────────────────────────────────────────────────────────────────────┐
│  ⚠ CONTEXT HAS CHANGED SINCE THIS REQUEST WAS PRODUCED               │
│                                                                       │
│  Changed: [dec-07] was created after this request was packaged.       │
│           Review this decision before approving.                      │
│                                                                       │
│  [I have reviewed the change — proceed to gate]                       │
└──────────────────────────────────────────────────────────────────────┘
```

The `Changed:` field is always specific. Examples of correct content:
- `[dec-07] governing decision superseded [dec-05] after this request was packaged.`
- `Evidence [obs-047] has become stale (now 8 days old). Review evidence before approving.`
- `Workflow stage changed from Planning — Active to Handoff — Awaiting Approval.`
- `3 new blocking gaps opened since this request was packaged: [gap-15], [gap-16], [gap-17].`

Examples of incorrect (vague, unacceptable) content:
- `Context has changed.`
- `Some information may be out of date.`
- `Please review before approving.`

**The gate controls remain at `--state-disabled-opacity`** until the operator clicks `[I have reviewed the change — proceed to gate]`. This click is logged: a context-change acknowledgment event is persisted with the timestamp, what was acknowledged, and the operator session identity. It does not substitute for the approval event — it is a precondition to presenting the gate controls.

**Multiple simultaneous changes:** If more than one change has occurred, they are listed as separate `Changed:` lines within the same warning block. The operator acknowledges all of them with a single click. Each change is logged in the acknowledgment record.

### 10.2 Severe Context Change

A severe change is one that makes the approval request basis clearly invalid: a governing decision the recommendation depended on has been superseded; the evidence record that provided the core basis for the action has been superseded by contradictory new evidence; the workflow stage has moved in a direction that makes the proposed action inapplicable.

**Where it appears:** Same location as the standard warning block (above gate controls in the Actions section), but with different content and no acknowledgment affordance.

**Content:**

```
┌──────────────────────────────────────────────────────────────────────┐
│  ⛔ CONTEXT CHANGE IS SEVERE — Re-evaluation required                  │
│                                                                       │
│  This approval request was produced when [dec-05] was the governing   │
│  decision for hosting scope. [dec-07] has superseded [dec-05] and     │
│  changes the strategic direction this request assumed.                │
│                                                                       │
│  This request cannot proceed on its current basis.                    │
│  Request the LLM to re-package under current governing context.       │
└──────────────────────────────────────────────────────────────────────┘
```

- Background: `--state-danger-bg`
- Border-left: 3px `--state-blocked`
- `⛔` icon: `--state-blocked`
- Header: `--type-sm`, `--weight-bold`, `--state-blocked`
- Body: `--type-sm`, `--text-secondary`

**No acknowledgment affordance.** The operator cannot click through a severe change. The gate controls remain permanently inactive until a new ARP is produced.

**Right-panel card update for severe change:**

When a severe change is detected for an in-review ARP:
- The card in the right panel receives the `⚠ BASIS CHANGED` staleness marker (Session 2 staleness marker vocabulary): `⚠ BASIS CHANGED — prior approval invalidated. Re-evaluate this output.`
- The `[Return to Gate →]` CTA on the card dims to `--state-disabled-opacity` and becomes non-clickable
- A note appears below the CTA: `Gate blocked — re-evaluation required` in `--text-tertiary`, `--type-xs`
- The `IN REVIEW` label updates to `REQUIRES RE-EVALUATION` in `--state-warning`

The operator's path from a severe change: return to the right panel, note the staleness marker on the ARP card, frame new work in the operator input to request a re-packaged ARP under current context, receive a new ARP card, proceed through the routing flow again from Step 1.

### 10.3 Right-Panel Staleness Markers on ARP Cards During Review

While the operator is in the center workspace reviewing, any of the seven staleness marker types from Session 2 / Session 5 may fire on the ARP card in the right panel. These are independent of the staleness warning in the center surface — both can fire simultaneously for the same event.

The seven staleness marker types applied to ARP cards:

| Marker | Trigger | Banner text |
|---|---|---|
| `CONTEXT CHANGED` | Catch-all for context changes during review | `⚠ CONTEXT CHANGED — produced during context change` |
| `DECISION SUPERSEDED` | EVENT-02 — a decision cited in the ARP was superseded | `⚠ DECISION SUPERSEDED — [dec-id] replaced by [dec-id-new]` |
| `EVIDENCE STALE` | EVENT-08 — evidence cited in the ARP is now stale | `⚠ EVIDENCE STALE — [obs-id] is now stale` |
| `BASIS CHANGED` | Prior approval the ARP depended on was invalidated | `⚠ BASIS CHANGED — prior approval for [record] has been invalidated. Re-evaluate this output.` |
| `SYSTEM CHANGED` | EVENT-11 — system posture changed during review | `⚠ SYSTEM CHANGED — produced under [prior system] posture` |
| `CONTINUITY ARTIFACT CHANGED` | EVENT-15 — a continuity artifact cited in the ARP changed | `⚠ CONTINUITY ARTIFACT CHANGED — [artifact] no longer in active basis` |
| `COMPACTION BOUNDARY` | EVENT-14 — compaction occurred during review | `⚠ COMPACTION BOUNDARY — produced before this compaction cycle` |

Staleness marker anatomy on ARP cards (appears as an inline banner attached to the top of the card, within the card's boundary — same treatment as Session 5 §7 staleness banners on output cards):
- Background: `--staleness-bg`
- Left border: 3px `--staleness-border`
- Text: `--type-xs`, `--staleness-text`
- Padding: `--space-2` vertical, `--space-3` horizontal
- The card body content below the marker remains unchanged and readable

Multiple staleness markers on the same card stack vertically within the card boundary, each as its own banner strip.

---

## 11. Flow Variants by Action Class

The canonical five-step flow applies universally. The following table summarizes the class-specific variations:

| Aspect | Class B | Class C |
|---|---|---|
| Gate surface | Inline widget in Actions section | `[Proceed to Authorization Gate]` button → modal |
| Approval control | `[Approve]` button (amber fill) | `[Confirm Authorization]` button (danger fill), active only after typed confirmation phrase correctly entered |
| Typed confirmation | Not required | Required for irreversible actions; optional (modal lacks confirmation block) for reversible Class C actions |
| Post-approval CTA | `[Proceed to Activation ›]` | `[Proceed to Activation ›]` |
| Checkpoint set | Shared + record-type-specific (per Session 10 §8.3–§8.4) | Full Class B checkpoint set + Class C-specific additional checkpoints (per Session 10 §8.6) |
| Checkpoint count | Typically 3–5 | Typically 5–7 |
| Right-panel card label sequence | `AWAITING REVIEW` → `IN REVIEW` → `APPROVED` / `REJECTED` | `AWAITING REVIEW` → `IN REVIEW` → `AUTHORIZED` |
| Modal scrim | No | Yes — full-screen at `--z-modal`, center workspace visible through `--surface-overlay` |
| Rejection path | `[Reject]` → reason prompt → rejection record | `[Cancel]` in modal (no record written); explicit rejection routes through Class B-style `[Reject]` on the inline widget before modal stage |
| Context switch while gate open | Gate checkpoints may revert; widget remains | Modal closes without writing record; treated as cancellation |

---

## 12. Token Usage from Session 2

No new tokens introduced. All values reference Session 2.

| Element | Token(s) |
|---|---|
| ARP card `AWAITING REVIEW` label | `--inert-label-bg`, `--inert-label-text`, `--type-xs` |
| ARP card `IN REVIEW` label | `--state-info` text, same inert-label shape |
| ARP card `APPROVED` label | `--state-success` text, same inert-label shape |
| ARP card `AUTHORIZED` label | `--state-success` text |
| ARP card `REJECTED` label | `--state-danger` text |
| ARP card `REQUIRES RE-EVALUATION` label | `--state-warning` text |
| `[Proceed to Approval Gate]` CTA border | `--border-accent` (`--accent-primary`) |
| `[Proceed to Approval Gate]` CTA text | `--accent-primary`, `--type-xs`, `--weight-medium` |
| `[Proceed to Approval Gate]` CTA hover | `--state-selected-bg` (amber at 12%) |
| `[Return to Gate →]` CTA | same amber border treatment as `[Proceed to Approval Gate]` |
| `[View Approval Record ›]` CTA | `--border-default`, `--text-secondary`, `--type-xs` |
| Checkpoint `○` icon | `--text-tertiary`, 16px |
| Checkpoint `✓` icon | `--state-success`, 16px |
| Checkpoint icon transition | `--transition-fast` (150ms) |
| Checkpoint label incomplete | `--type-sm`, `--text-tertiary` |
| Checkpoint label complete | `--type-sm`, `--text-primary` |
| Checkpoint status line `○` | `--text-tertiary` |
| Checkpoint status line `✓` | `--text-secondary` |
| Section tab reviewed `✓` suffix | `--state-success`, `--type-xs` |
| Gate activation border | `--border-accent` → `--transition-spring` |
| Gate activation shadow | `--gate-active-shadow` → `--transition-spring` |
| Gate controls activation | `--state-disabled-opacity` → full, `--transition-default` |
| `[Approve]` loading indicator | `···` in `--text-inverse` on amber fill |
| Write failure `⚠` | `--state-warning`, `--type-sm` |
| `[Retry]` on write failure | `--text-link`, `--type-sm` |
| Post-approval `✓ APPROVED` line | `--state-success`, `--type-sm`, `--weight-semibold` |
| Post-rejection `✗ REJECTED` line | `--state-danger`, `--type-sm`, `--weight-semibold` |
| `✓ ACTIVATED` line | `--state-success`, `--type-sm`, `--weight-semibold` |
| `✗ ACTIVATION FAILED` line | `--state-danger`, `--type-sm`, `--weight-semibold` |
| `[Proceed to Activation ›]` | `--border-accent`, `--accent-primary` text, `--type-sm`, `--weight-medium` |
| `[Proceed to Authorization Gate]` | `--border-accent`, `--accent-primary` text, `--type-sm`, `--weight-bold`, 40px height |
| Modal scrim | `--surface-overlay` (#1a1f23cc), `--z-modal` (500) |
| Modal close transition | `--transition-fade` (300ms ease opacity) |
| Standard staleness warning | `--staleness-bg`, `--staleness-border` (3px left), `--staleness-text` |
| Severe change warning | `--state-danger-bg`, 3px `--state-blocked` left, `--state-blocked` header |
| ARP card staleness banner | `--staleness-bg`, `--staleness-border` (3px left), `--type-xs`, `--staleness-text` |
| `BASIS CHANGED` marker | `--staleness-bg`, `--staleness-text`, specific text per §10.3 |

---

## 13. What Session 11 Resolves

- The canonical five-step routing flow is fully specified: all five steps, all transition states, all control states, all surface behaviors. Sessions 13–15 can apply this pattern to their specific workflow surfaces without inventing local variants.
- The Session 10 open question is resolved: ARP cards remain visible in the right panel throughout the routing flow. They do not disappear on navigation. They update their label and CTA to reflect the operator's progress (`AWAITING REVIEW` → `IN REVIEW` → `APPROVED` / `REJECTED` / `AUTHORIZED`).
- The right-panel card state sequence is fully specified: five label states, two CTA states, staleness marker behavior, severe-change treatment that dims the card's CTA and adds `REQUIRES RE-EVALUATION`.
- The checkpoint completion animation sequence is specified: checkpoint icon and label transition (`--transition-fast`), status line transition (`--transition-default`), gate widget activation (`--transition-spring`), scroll-to-gate behavior (once, at the moment of activation).
- The activation path UX is specified: loading state during API call, success state (two confirmation lines), failure treatment (approval record retained, activation failure shown separately, retry affordance).
- The context-changed-since-recommendation notice is specified concretely: what it says (specific, not vague), where it appears (Actions section, above gate controls), how it blocks (controls remain disabled until acknowledged), what acknowledgment logs (timestamp, what was acknowledged, session identity).
- The severe-change treatment is specified as a permanent block (no acknowledgment affordance, permanent gate closure, requires new ARP) distinct from the standard acknowledgeable warning.
- The seven right-panel staleness marker types are mapped to their ARP card treatment: inline banner at the top of the card, within the card boundary, stacked if multiple fire.
- The rejection path is fully specified through to post-rejection state: continuation options (`[Revise and Resubmit]`, `[Defer]`, `[Escalate]`), no second-approval path from the same gate, historical record of rejection preserved.
- The defer state is specified: no record written, checkpoints preserved, `[Resume ›]` restores gate, `[Reject this request instead]` is available.
- The Class C modal relationship to the center workspace and right panel during the modal is specified: scrim covers both; center workspace is visible through the scrim; right panel is covered but card is preserved; modal close (cancel) restores all surfaces to pre-modal state.

---

## 14. What Session 11 Does Not Resolve Yet

- **Specific workflow surface review content** — the Actions section and its ordered review sections (Overview, Evidence, Decisions, History, Actions) as populated for specific record types are Sessions 13–15. Session 11 specifies the universal routing pattern; Sessions 13–15 specify what the operator is actually reviewing in Steps 3 and 4 for handoff, return trigger, and launch readiness records.
- **The notification that fires when approval is written** — Session 12. When the approval record is persisted in Step 4, a session-level notification fires. That notification's design (in-app notification, what it says, how it behaves) is the alert/notification system's domain.
- **Session start integrity check** — Session 12. If a session starts with pending approvals that were initiated in a prior session, the session start integrity check surfaces them. The routing flow from the session start check to the center workspace gate is the same five-step pattern specified here, but the entry point (session start check rather than right-panel CTA) is Session 12's design territory.
- **Command palette activation of the routing flow** — Session 21. An operator using the command palette to navigate to a pending approval navigates to the record's Actions section. The flow from that point is the same five-step pattern. The command palette's interface is Session 21.
- **Activation API response details** — the exact error codes and messages the activation API may return are implementation territory. Session 11 specifies the UX treatment for success and failure; the mapping of specific API error codes to specific display messages is a future implementation detail.
- **Multi-approval sessions** — if the operator has multiple pending approvals in a single session (e.g., two handoffs both in `Awaiting Approval`), the right panel may contain two ARP cards simultaneously. The routing flow applies independently to each. How the operator manages multiple simultaneous in-review gates (potentially two `IN REVIEW` cards, two center workspace tabs open) is an ergonomic question that is partly answered by the tab system (Session 9, max 5 tabs) and partly by Session 12's session start integrity check (which surfaces the full list of pending approvals). No new design is needed here — existing mechanisms handle it — but it is worth noting as an area that Session 13+ workflow surface design should be mindful of.

---

## 15. Recommended Inputs to Session 12

Session 12 is the Session Start Integrity Check and Alert/Notification System.

**What Session 12 inherits from Sessions 10–11:**
- The approval event is a persisted record. When it is written, a notification should fire — not a modal (that's only for Class C typed confirmation), but an in-app notification confirming the governance event. Session 12 designs this notification.
- The session start integrity check must surface pending approvals. The routing path from the integrity check to the center workspace gate is the five-step flow specified in Session 11 — the entry point is the integrity check rather than a right-panel card, but the flow is identical from Step 2 onward.
- The 18-event invalidation matrix drives the alert system. Session 11 has shown what two of those events (decision superseded, evidence stale) look like at the routing-flow level. Session 12 must design the full alert/notification surface for all 18 events, using the inline banner, attention badge, in-app notification, and modal categories established in Sessions 5 and 9.
- The staleness marker vocabulary for ARP cards (seven types per §10.3) is part of the output card staleness system that Session 12's alert system must be consistent with.

**Specific design questions Session 12 should answer:**

How does the session start integrity check handle multiple pending approvals? If the operator starts a session with three pending Class B approvals from a prior session, the integrity check shows all three. Clicking `[Review Items]` opens the session integrity view. From the session integrity view, clicking a pending approval item should route the operator into the five-step flow for that specific approval. Session 12 must specify the integrity view's pending-approval item affordance in enough detail that the routing is unambiguous.

What does the approval-written notification say and how does it behave? It should be informational (not modal), specific (names the record and action approved), brief (one or two lines), and time-limited (it disappears after a few seconds or on operator acknowledgment). Session 12 should specify: where it appears, what it says, how long it persists, whether it has an action affordance.

How does the inline banner system scale from Session 11's two examples to all 18 invalidation events? Session 11 designed the inline banner treatment for the staleness warning in the routing flow context. Session 12 must produce the complete mapping: each of the 18 events → which surface type fires (attention badge, topbar warning, inline banner, in-app notification, modal) → what message → what operator action is offered.
