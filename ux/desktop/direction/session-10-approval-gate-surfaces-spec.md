# Session 10 — Approval Gate Surfaces
## V Ecosystem Desktop UX

**Session status:** Complete
**Depends on:** Sessions 1–9 (full shell backbone established; center workspace foundation including Actions section gate placement decided)
**Required before:** Session 11 (Review-to-Gate Routing Flow) — the gate widget designs must exist before the routing pattern can be specified; Session 12 (Alerts/Notifications) — escalation banner is gate-surface territory, not notification territory; Sessions 13–15 (all workflow surfaces contain or route to gates)

---

## 1. Files Read

**Work plan and prior sessions:**
- `v-ecosystem-desktop-ux-work-plan.md` — Session 10 deliverable, gate surface placement rules, TIER 3 positioning
- `session-02-minimal-token-decisions.md` — active token baseline; all values here reference Session 2
- `session-03-topbar-spec.md` — gate surfaces must not appear in topbar (confirmed)
- `session-04-context-strip-spec.md` — gate surfaces must not appear in context strip; `[Review Gate]` navigation affordance in INTEGRITY row is navigation only
- `session-05-right-panel-shell-spec.md` — gate surfaces must not appear in right panel; `[Proceed to Approval Gate]` is a routing action, not an approval action
- `session-06-left-nav-shell-project-v-tree-spec.md` — gate surfaces must not appear in left nav
- `session-07-left-nav-veda-tree-spec.md` — `[Proceed to Approval Gate ›]` on VEDA provider rows is navigation only; gate lives in center workspace
- `session-08-left-nav-v-forge-tree-spec.md` — launch auth pending treatment in nav is display only; gate lives in center workspace
- `session-09-center-workspace-foundation-spec.md` — gate widget lives in Actions section, at the bottom, after review; `intent = 'approval_gate'` router behavior; inline banner position above view body; review-before-gate is enforced by layout

**Doctrine:**
- `interfaces/desktop-governance-and-gating-model.md` — action classes A–D; approval event definition; typed confirmation structural requirement; what must be blocked vs warned; invalidation conditions; structural enforcement requirements
- `interfaces/desktop-surface-architecture.md` — gate surfaces category; review-before-gate routing rule; Class B inline widget; Class C modal; Class D escalation banner; absent-affordance rules
- `interfaces/desktop-human-llm-interaction-model.md` — operator as accountable party; LLM produces inert outputs; approval request package is not approval
- `interfaces/desktop-state-and-context-model.md` — nine state categories; staleness markers; session integrity requirements
- `interfaces/desktop-invalidation-and-refresh-matrix.md` — 18 invalidation events; gate-blocking consequences per event
- `interfaces/desktop-implementation-architecture.md` — approval record write before activation call; gate widget owned by center workspace

**Workflows:**
- `workflows/handoff-workflow.md` — awaiting-approval vs prepared distinction; what makes a pending approval invalid
- `workflows/launch-readiness-workflow.md` — Class C gate context; cross-system confirmation requirement; evidence currency principle
- `workflows/maintenance-and-replanning-workflow.md` — maintenance vs replanning routing distinction; Class D escalation triggers

**UX reference:**
- `v-ecosystem-ux/docs/desktop/sessions/session-02-minimal-token-decisions.md` — confirms token baseline
- `v-ecosystem-ux/bricks/` — visual language density and interaction feel reference; Bricks patterns already extracted in Session 2; no new values added here

---

## 2. Session 10 Scope Confirmation

The work plan defines Session 10 — Approval Gate Surfaces as the first TIER 3 session. Its purpose is to design the complete gate surface set so that Sessions 11–15 can reference a stable, concrete gate vocabulary without inventing their own variants.

This session produces:
- Class B inline approval widget — embedded in Actions section of center workspace detail view
- Class C modal gate — triggered from center workspace after all checkpoints satisfied
- Typed confirmation input — explicitly designed as a distinct element for irreversible Class C actions
- Class D escalation banner — non-dismissible inline banner in center surface
- Review checkpoint model — the concrete criteria that determine when gates activate

This session does not:
- Design the five-step routing flow from output card to approval event (Session 11)
- Design the alert/notification system or session start integrity check (Session 12)
- Design handoff review, return trigger review, or launch readiness review surfaces (Sessions 13–15)
- Invent new action classes
- Invent approval paths outside doctrine
- Design the right panel, left nav, or topbar (those are done; gates do not appear there)

---

## 3. Approval Gate Surface Principles

These principles govern every design decision in this session. They are derived from doctrine. None of them are preferences.

**Gates live in the center workspace.** Class B gates are embedded in the Actions section of center workspace detail views. Class C gates are modals triggered from within center workspace surfaces. Class D escalation banners appear as non-dismissible inline banners in center surfaces. None appear in the right panel, left nav, or topbar. Not in a compressed form. Not as a routing shortcut. Not ever.

**Review comes before the gate is reachable.** The gate widget does not activate until the operator has completed required review checkpoints in the center workspace. Layout enforces this — the gate is at the bottom of the Actions section, below review content. The operator must scroll through the review surface to reach it. This is intentional. If the gate appeared at the top, the sequence would drift toward rubber-stamp behavior.

**The gate is not the review.** Showing the operator a gate widget is not equivalent to having them review the record. The review happens in the center workspace. The gate widget is the terminal action after review, not a summary of review.

**Approval events must be persisted before activation proceeds.** The gate widget writes the approval record. The activation API is called only after the write succeeds. If the write fails, activation does not proceed. This is a structural enforcement requirement, not a UI convention.

**Typed confirmation is a separate, distinct input element.** For irreversible Class C actions, typed confirmation is a text field requiring a specific phrase. It is not a checkbox. It is not pre-populated. It cannot be dismissed without completing the required input. The gate widget's confirm control remains inactive until the phrase is correctly entered.

**Staleness and changed context must appear before the gate.** If relevant context has changed since the approval request was produced, the staleness notice appears before the gate widget and the operator must acknowledge it before proceeding. The gate does not appear first and warn second.

**Rejection must be persisted.** The Reject control writes a rejection record with the same persistence requirements as an approval event. Rejection is not a UI-only interaction. The rejection record must be sufficient to answer what was rejected, by whom, when, and why.

**Class D is not a failure state.** When a Class D condition is detected, the correct application behavior is to surface the escalation banner, withhold the action, and give the operator `[Escalate]` and `[Document and Hold]` as the only paths. There is no dismiss, no proceed-anyway, and no "I understand the risk" override. Class D exists precisely because the current governance posture cannot safely resolve the situation.

---

## 4. Class B Inline Approval Widget

### 4.1 What It Is

The Class B inline approval widget is the UI element that creates a persisted operator approval record for bounded, reviewable mutations and governed transitions. It is the governed approval gate for Class B actions — creating records, executing status transitions, activating handoffs, routing findings, recording readiness outcomes.

It lives in the Actions section of the center workspace generic record detail view (established in Session 9). It is always the last element in the Actions section — below all action items, below all review content, below all evidence and decision context. The operator scrolls to it; it does not scroll to the operator.

### 4.2 Widget Anatomy

```
┌─────────────────────────────────────────────────────────────────────────┐
│  APPROVAL REQUEST                                          [CLASS B]     │
│                                                                          │
│  Action:    Activate handoff — hosting-comparison-site                   │
│  Scope:     Handed-off scope as defined in hdl-07                        │
│  Basis:     Planning readiness confirmed; 3 of 3 gaps resolved           │
│  Covers:    Approval to transfer execution responsibility to V Forge      │
│  Default:   Handoff remains in Awaiting Approval state if not approved    │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ✓ Required checkpoints complete — gate is active                        │
│                                                                          │
│  [Approve]          [Reject]          [Defer]                            │
└─────────────────────────────────────────────────────────────────────────┘
```

### 4.3 Element Specifications

**Widget container:**
- Background: `--surface-elevated`
- Border: 1px `--border-default`; activated state: 1px `--border-accent` (`--accent-primary`)
- Border-radius: `--radius-lg` (6px)
- Padding: `--space-6` (24px)
- Box shadow on activation: `--gate-active-shadow` (0 0 0 2px rgba(255,214,79,0.25)) — the amber glow defined in Session 2 gate activation tokens
- Activation transition: `--transition-spring` (transform + opacity 200ms cubic-bezier(0.215,0.61,0.355,1)) — the spring easing from Session 2, used for the moment the gate activates

**Header row:**
- Label `APPROVAL REQUEST`: `--type-xs` (11px), `--weight-semibold`, `--text-tertiary`, letter-spacing 0.3px — the structural metadata label pattern from Sessions 4–6
- Class badge `[CLASS B]`: `--badge-class-b-bg` (#0d2a3d fill), `--badge-class-b-text` (#00b0f4 text), `--type-xs`, `--weight-bold`, `--radius-pill` — the Class B badge from Session 2 governance tokens
- Badge position: right edge of header row, vertically aligned with label

**Summary block (Action / Scope / Basis / Covers / Default):**
- Label column: `--type-xs`, `--weight-semibold`, `--text-tertiary`, min-width 80px, right-aligned
- Value column: `--type-sm` (12px), `--weight-normal`, `--text-primary`
- Row padding: `--space-2` (8px) vertical per row
- The five fields are fixed — they map exactly to the required Approval Request Package elements from the governance model: action identified, scope bounded, basis, what approval covers, what the default state is if not approved. No fields may be omitted.

**Divider:** `--border-subtle` 1px horizontal rule, `--space-4` (16px) vertical margin

**Checkpoint status line:**
- When active: `✓ Required checkpoints complete — gate is active` — `--type-sm`, `--text-secondary`; `✓` in `--state-success`
- When inactive: `○ Complete required review before approving` — `--type-sm`, `--text-tertiary`; `○` in `--text-tertiary`
- The checkpoint status line is the signal to the operator of gate readiness. When it shows `✓`, the controls below are active. When it shows `○`, the controls are inactive at `--state-disabled-opacity` (0.4).

**Controls:**

The three controls are arranged in a horizontal row at the bottom of the widget.

**`[Approve]`:**
- Width: 120px
- Height: 36px
- Background: `--accent-primary` (#ffd64f) — this is the one place in the application where the amber accent is used as a filled button background. It is used here because this is the primary governance action the gate surfaces.
- Text: `--text-inverse` (#212121), `--type-sm`, `--weight-bold` — dark text on amber fill
- Border: none
- Border-radius: `--radius-md` (4px)
- Hover: background lightens by 8% (mix amber with white at 8%)
- Active: `--state-active-overlay` on the amber fill
- Disabled (gate inactive): `--state-disabled-opacity` on the entire button; cursor: not-allowed
- On click: writes approval record, then enables downstream activation path; not clickable again after approval written (becomes a read-only `Approved` confirmation label)

**`[Reject]`:**
- Width: 100px
- Height: 36px
- Background: `--surface-raised`
- Border: 1px `--state-danger`
- Text: `--state-danger`, `--type-sm`, `--weight-medium`
- Border-radius: `--radius-md`
- Hover: `--state-danger-bg` background fill
- Disabled: `--state-disabled-opacity`; cursor: not-allowed
- On click: opens rejection reason prompt (see §4.5), then writes rejection record

**`[Defer]`:**
- Width: 100px
- Height: 36px
- Background: `--surface-raised`
- Border: 1px `--border-default`
- Text: `--text-secondary`, `--type-sm`, `--weight-normal`
- Border-radius: `--radius-md`
- Hover: `--state-hover-overlay`
- Disabled: `--state-disabled-opacity`; cursor: not-allowed
- Defer availability: only present when the approval request is deferrable (not all Class B actions support deferral — non-deferrable requests omit this control entirely; the layout shifts to two controls left-aligned)
- On click: logs defer event; returns operator to center workspace without writing approval or rejection record; the gate widget returns to its inactive state with a `Deferred — return when ready` note replacing the checkpoint status line

**Control spacing:** `--space-3` (12px) gap between controls. Controls are left-aligned within the widget.

### 4.4 Inactive Gate State

When the gate widget is present but not yet active (checkpoints incomplete), the entire widget is visible but muted:

- Widget border: `--border-subtle` (not `--border-accent`)
- Widget box-shadow: none
- All three controls: `--state-disabled-opacity` (0.4); cursor: not-allowed
- Checkpoint status line: `○ Complete required review before approving`
- The widget is clearly present — it communicates that this is where the gate will be — but it is not operable. The operator understands they have remaining review steps.

This inactive treatment enforces two things simultaneously: the review-before-gate sequence (operator knows the gate is coming but must complete review first), and the honest state of the gate (the widget does not lie about being ready when it is not).

### 4.5 Rejection Reason Prompt

When the operator clicks `[Reject]`, a small inline prompt appears below the controls before the rejection is written:

```
Rejection reason (optional — logged if provided):
┌─────────────────────────────────────────────────────────────────┐
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
[Confirm Rejection]    [Cancel]
```

- The text field is a single-line input, `--surface-raised` background, `--border-default` border, `--type-base` text, `--type-sm` placeholder (`Enter reason…`)
- The rejection reason is optional — the operator may confirm rejection without entering a reason
- `[Confirm Rejection]`: `--state-danger` border, `--state-danger` text, `--radius-md` — writes the rejection record with the reason (or without if blank); the gate widget transitions to a read-only `Rejected` confirmation state
- `[Cancel]`: returns to the gate widget in its prior state; no rejection record written
- The prompt appears inline below the controls without pushing other content — it is absolutely positioned within the widget container

### 4.6 Post-Approval State

After `[Approve]` is clicked and the approval record is confirmed written:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  APPROVAL REQUEST                                          [CLASS B]     │
│                                                                          │
│  Action:    Activate handoff — hosting-comparison-site                   │
│  [... summary fields ...]                                                │
│                                                                          │
│  ─────────────────────────────────────────────────────────────────────  │
│                                                                          │
│  ✓ APPROVED — 2026-04-03 09:47  ·  Approval record written              │
│                                                                          │
│  [Proceed to Activation ›]                                               │
└─────────────────────────────────────────────────────────────────────────┘
```

- Checkpoint status line replaces with: `✓ APPROVED — [timestamp]  ·  Approval record written` in `--state-success`, `--type-sm`, `--weight-semibold`
- `[Approve]` / `[Reject]` / `[Defer]` controls are replaced with a single `[Proceed to Activation ›]` button
- `[Proceed to Activation ›]`: `--border-accent`, `--accent-primary` text, `--radius-md` — styled like the `[Proceed to Approval Gate]` button from Session 5, communicating that this is the governed routing action forward, not another governance action
- Widget border retains `--border-accent` from the active state
- Widget retains `--gate-active-shadow`

The `[Proceed to Activation ›]` button triggers the activation path — the API call that makes the approved action active. This call happens only after the approval record write is confirmed. If the write failed for any reason, this button is not shown; instead a `⚠ Approval record write failed — retry?` notice appears with a `[Retry]` link.

### 4.7 Stale-Context Warning Treatment

When relevant context has changed since the approval request was produced, a warning appears **above the gate widget**, between the Actions section content and the widget itself. The gate widget's controls remain at `--state-disabled-opacity` until the operator acknowledges the warning.

```
┌──────────────────────────────────────────────────────────────────────┐
│  ⚠ CONTEXT HAS CHANGED SINCE THIS REQUEST WAS PRODUCED               │
│                                                                       │
│  Changed: [dec-07] governing decision superseded [dec-05]             │
│  Basis of this approval request may be affected.                      │
│  Review the updated context before approving.                         │
│                                                                       │
│  [I have reviewed the change — proceed to gate]                       │
└──────────────────────────────────────────────────────────────────────┘
```

- Container: `--staleness-bg` background, `--staleness-border` left border (3px), `--radius-md`
- Padding: `--space-4` (16px)
- Header: `⚠ CONTEXT HAS CHANGED SINCE THIS REQUEST WAS PRODUCED` — `--type-sm`, `--weight-semibold`, `--staleness-text`
- Changed item: specific identification of what changed — decision ID, evidence record ID, or description of the change. Never vague. Never "context has changed."
- `[I have reviewed the change — proceed to gate]`: `--text-link`, `--type-sm`. Clicking this acknowledges the change (logged), removes the staleness warning block, and activates the gate widget controls if all checkpoints are also complete.

**Severe change — gate blocked:** If the change is severe enough that the approval request basis is clearly invalid (e.g., a governing decision the recommendation depended on has been superseded), the warning text changes and `[I have reviewed the change — proceed to gate]` is replaced with a non-clickable notice:

```
⚠ CONTEXT CHANGE IS SEVERE — Re-evaluation required before approval
This approval request was produced under [dec-05], which has been
superseded by [dec-07]. The approval request must be re-evaluated.
Request the LLM to re-package under current context.
```

In this state, the gate widget controls remain permanently inactive until a new approval request package is produced. The operator cannot acknowledge their way past a severe change.

---

## 5. Class C Modal Gate

### 5.1 What It Is

The Class C modal gate is the approval surface for launch-sensitive, external, paid, and irreversible actions. It is a full modal overlay, distinct from the Class B inline widget, triggered only after the operator has completed all required review checkpoints in the center workspace and explicitly initiated the authorization.

The Class C modal is triggered by a `[Proceed to Authorization Gate]` button in the Actions section — a distinct CTA that only becomes available when all checkpoints are satisfied. The modal is not a widget embedded in the view — it is an overlay that takes the full attention of the operator.

### 5.2 What Triggers It

The `[Proceed to Authorization Gate]` button in the Actions section of the center review surface becomes active when:
- All required review checkpoints are satisfied (see §8)
- No stale-context warning is blocking (or the warning has been acknowledged)
- The approval request package is current (not invalidated by a severe change)

The modal must not fire from:
- The right interaction panel
- Any nav tree item
- The topbar
- Any surface that bypasses the center workspace review

### 5.3 Modal Structure

The modal uses `--elevation-modal`, `--z-modal: 500`, and the `--surface-overlay` scrim behind it (base color at 80% opacity covering the entire center workspace and surrounding surfaces).

Modal dimensions:
- Width: 600px
- Min-height: 400px; grows with content
- Max-height: 80vh; scrolls internally if content exceeds this
- Border-radius: `--radius-lg` (6px)
- Background: `--surface-elevated`
- Border: 1px `--border-emphasis` (`--surface-border`)
- Padding: `--space-8` (32px) — generous; this is a high-consequence action surface

**Scrim:** `--surface-overlay` (#1a1f23cc — base at 80% opacity). Full-screen. Not clickable. The only way to close the modal is via the explicit `[Cancel]` control. Clicking outside the modal does nothing.

### 5.4 Modal Content Anatomy

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  Authorization Required                                         [CLASS C]   │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  What is being authorized:                                                   │
│  Launch activation — content-hub-v1 to public-facing production              │
│                                                                              │
│  What happens if authorized:                                                 │
│  V Forge will proceed with launch-sensitive execution within the confirmed   │
│  scope. The content hub site will become externally visible. Publication     │
│  and indexation actions will proceed.                                        │
│                                                                              │
│  What does NOT change:                                                       │
│  Planning ownership remains with Project V. Observatory scope remains        │
│  with VEDA. V Forge execution remains bounded to the confirmed handoff       │
│  scope. Authorization does not grant scope expansion.                        │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  ⚠  This action is irreversible once activation proceeds.                   │
│     External publication and indexation cannot be undone.                    │
│                                                                              │
│  ─────────────────────────────────────────────────────────────────────────  │
│                                                                              │
│  To confirm authorization, type exactly:                                     │
│  AUTHORIZE LAUNCH content-hub-v1                                             │
│                                                                              │
│  ┌────────────────────────────────────────────────────────────────────────┐ │
│  │                                                                        │ │
│  └────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│                                   [Confirm Authorization]    [Cancel]        │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 5.5 Modal Element Specifications

**Modal title:**
- `Authorization Required` — `--type-xl` (20px), `--weight-semibold`, `--text-primary`
- Class badge `[CLASS C]` — `--badge-class-c-bg` (#2d0d12), `--badge-class-c-text` (#fa4362), `--type-xs`, `--weight-bold`, `--radius-pill` — Session 2 Class C badge tokens
- Title and badge on the same row, badge right-aligned

**Section label pattern:**
Each content block uses a bold section label (`--type-sm`, `--weight-semibold`, `--text-secondary`) followed by the block content (`--type-base` (13px), `--weight-normal`, `--text-primary`). Section label and content are in the same visual column with `--space-2` (8px) gap between label and text.

**"What is being authorized" block:**
Specific, bounded description of the exact action. Not a category. Not "launch activation." Includes: action type, specific record or scope identifier, what system is responsible.

**"What happens if authorized" block:**
Concrete description of the downstream consequences. Must be honest about external-facing consequences. Must not minimize. If the action is irreversible, the consequences must reflect that.

**"What does NOT change" block:**
Explicit statement of what authorization does not cover. This block exists to prevent scope drift — the operator must see that authorization of this action does not constitute authorization for adjacent actions, scope expansion, or cross-system ownership transfer. This block is required for every Class C modal. It is not optional.

**Horizontal divider:** `--border-default` 1px rule, `--space-5` (20px) vertical margin

**Irreversibility notice:**
Only present for irreversible actions. Not present for reversible Class C actions (e.g., a paid data pull authorization that could theoretically be cancelled before execution proceeds).

```
⚠  This action is irreversible once activation proceeds.
   [Specific description of what cannot be undone]
```

- Background: `--state-danger-bg` (#2d0d12)
- Border-left: 3px `--state-danger`
- Padding: `--space-4` (16px)
- `⚠`: `--state-danger`, `--type-md`
- First line: `--type-sm`, `--weight-semibold`, `--state-danger`
- Second line: `--type-sm`, `--weight-normal`, `--text-secondary`
- `--radius-md`

**Second horizontal divider** separates the irreversibility notice from the typed confirmation block.

**Typed confirmation section:** See §6 for full specification.

**Control row:**
`[Confirm Authorization]` and `[Cancel]` are right-aligned in the modal footer.

**`[Confirm Authorization]`:**
- Width: 200px
- Height: 40px (slightly taller than standard — this is a high-consequence control)
- Background: `--state-danger` (#fa4362) — danger fill for the most consequential action in the system
- Text: `--text-primary` (#eaecef), `--type-sm`, `--weight-bold`
- Border-radius: `--radius-md`
- **Disabled state:** `--state-disabled-opacity` (0.4); cursor: not-allowed; background still `--state-danger` but at opacity — this is the correct state before the typed confirmation phrase is correctly entered
- **Active state:** full opacity; clickable; on click: writes approval record and typed confirmation log, then enables activation path
- The confirm button is inactive by default. It becomes active only when the typed confirmation input contains the exact required phrase. See §6.

**`[Cancel]`:**
- Width: 100px
- Height: 40px
- Background: `--surface-raised`
- Border: 1px `--border-default`
- Text: `--text-secondary`, `--type-sm`, `--weight-normal`
- Border-radius: `--radius-md`
- On click: closes modal; no approval record written; approval request package remains in its prior pending state; operator returns to the center review surface

### 5.6 Modal Behavior Rules

**Cannot be opened from the right panel.** The `[Proceed to Authorization Gate]` CTA in the Actions section is the only trigger. The right panel's output cards may have a `[Proceed to Approval Gate]` navigation button that routes to the center workspace, but that navigation button does not open the modal — it opens the center review surface. The modal is available only after the operator is in the center surface and all checkpoints are complete.

**Cannot be bypassed by context switch.** If the operator switches project or system while the modal is open, the modal must close without writing an approval record. A session-level context switch while a modal gate is open is treated as a cancellation. The operator must re-navigate to the gate.

**Context change while modal is open.** If a relevant invalidation event fires while the modal is open (e.g., EVENT-02 decision superseded), the modal surface responds:
- The modal remains open (no auto-close)
- A warning stripe appears above the typed confirmation section: `⚠ Context changed while this modal was open — [what changed]. Review before confirming.`
- The `[Confirm Authorization]` button returns to disabled state even if the phrase was already entered correctly
- The operator must re-enter the phrase after reviewing the change
- If the change is severe (the approval basis is clearly invalidated), the modal surfaces a non-dismissible error: `⛔ This authorization can no longer proceed — context has materially changed. Close and re-evaluate.` The `[Confirm Authorization]` button is removed entirely; only `[Cancel]` remains.

---

## 6. Typed Confirmation Input

### 6.1 When It Appears

The typed confirmation input appears in the Class C modal gate for irreversible actions. It does not appear for:
- Class B approval (Class B uses the `[Approve]` button; typed confirmation is not required)
- Reversible Class C actions (e.g., paid data pulls where cancellation is possible — the typed confirmation block is omitted from the modal for these)
- Any surface outside the Class C modal

The irreversibility threshold that triggers the typed confirmation is: once activation proceeds, the external consequences cannot be undone. Publication, launch, external distribution, financial commitment at launch scale. If there is genuine ambiguity about reversibility, the typed confirmation is included. When in doubt, include it.

### 6.2 Exact Role in the Modal

The typed confirmation input is the final checkpoint before the `[Confirm Authorization]` button becomes active. It is positioned at the bottom of the modal content, after all informational content and after the irreversibility notice. The operator has read:
- what is being authorized
- what happens if authorized
- what does not change
- that the action is irreversible

Then — and only then — the typed confirmation input is encountered.

The input's role is to require deliberate, active, specific entry of the authorization phrase. It is not a summary. It is not a checkbox. It is a mechanical enforcement of deliberate operator intent: the operator must type the specific phrase to demonstrate they have read and understood what they are authorizing.

### 6.3 Why It Is Not a Checkbox

A checkbox is a single motor action: move cursor, click. It requires no deliberate mental engagement with the content. An operator can check a checkbox while mentally somewhere else.

Typing a specific phrase requires: reading the phrase, encoding the phrase, actively entering it character by character. The action is congruent with the cognitive demand: something irreversible requires active, specific, deliberate engagement. The typed confirmation is the structural embodiment of "you must mean this."

From the governance model (Structural Enforcement Requirement 5): "For irreversible Class C actions, typed confirmation must be a distinct input element, for example a text field requiring a specific phrase, rendered after the approval gate has been satisfied. It must not be a checkbox. It must not be pre-populated. It must not be dismissible without completing the input."

This is not a design preference. It is a doctrine requirement.

### 6.4 Typed Confirmation Input Specification

**The required phrase pattern:**

```
AUTHORIZE [ACTION TYPE] [RECORD IDENTIFIER]
```

Examples:
- `AUTHORIZE LAUNCH content-hub-v1`
- `AUTHORIZE PAID PULL serpapi-keyword-2026-04`
- `AUTHORIZE HANDOFF hosting-comparison-site`

The phrase is always uppercase. It always begins with `AUTHORIZE`. It always includes a specific record or scope identifier that is unique to this authorization request. The phrase is rendered in `--font-mono`, `--type-sm`, with `--state-warning` color (amber, slightly alarming — this phrase matters), in the modal content directly above the input field.

**The required phrase is shown as static, non-copyable text above the input.** It is not rendered as selectable text. The operator cannot copy-paste it. They must type it. The implementation achieves this by rendering the phrase as a display element with `user-select: none`, not as input content or selectable label text.

**Input field:**
- Full-width within the modal content area
- Height: 44px
- Background: `--surface-raised`
- Border: 1px `--border-default` resting; transitions to `--border-accent` when the correct phrase is entered
- Border-radius: `--radius-md`
- Text: `--font-mono`, `--type-base` (13px), `--text-primary`
- Placeholder: `Type the phrase above to confirm` — `--text-tertiary`
- Padding: `--space-3` (12px) horizontal, `--space-2` (8px) vertical

**Validation behavior:**

Input is validated character-by-character as the operator types. The validation is exact-match and case-sensitive. No leading/trailing whitespace tolerance.

| Input state | Border color | Confirm button state |
|---|---|---|
| Empty | `--border-default` | Inactive (`--state-disabled-opacity`) |
| Partial or incorrect | `--border-default` | Inactive |
| Exactly correct | `--border-accent` (`--accent-primary`) | Active |
| Correct then edited to incorrect | `--border-default` | Returns to inactive |

When the phrase is exactly correct:
- Input border transitions to `--border-accent` using `--transition-default` (200ms ease)
- `[Confirm Authorization]` button transitions from `--state-disabled-opacity` to full opacity using `--transition-default`
- The phrase text above the input gains a `✓` prefix in `--state-success`
- No sound, no animation, no celebration — the transition is quiet and clear

**Not pre-populated.** The input field is always empty when the modal opens. The operator must enter the phrase from scratch every time.

**Not autocompleted.** The input must have `autocomplete="off"` and must not be filled by browser or OS autofill. This is structural, not preference.

**Cannot be dismissed without completing.** While the modal is open, `Escape` key does not close the modal (unlike most dialogs). The only ways to exit the modal are: complete the typed confirmation and click `[Confirm Authorization]`, or click the explicit `[Cancel]` button. This is consistent with the governance model: "It must not be dismissible without completing the input."

### 6.5 Context Change While Modal Is Open

If a relevant context change occurs while the operator is typing:

1. The warning stripe appears above the typed confirmation input (see §5.6)
2. The `[Confirm Authorization]` button returns to inactive, regardless of whether the phrase was already correctly entered
3. The input field clears — the operator must re-enter the phrase after reviewing the change
4. If the change is severe, the `[Confirm Authorization]` button is removed entirely

The operator must re-read the warning, evaluate the change, decide whether to proceed, and then re-enter the phrase. This sequence cannot be shortcut. The change may affect what they are authorizing; they must engage with it before authorizing.

---

## 7. Class D Escalation Banner

### 7.1 What It Is

The Class D escalation banner appears when the application detects a condition that the current governance posture cannot safely resolve: doctrine-unclear actions, boundary-exceeding requests, ambiguous authority, exception conditions. It surfaces the issue, withholds the action, and offers exactly two paths: escalate or document and hold.

It is a non-dismissible inline banner. It is not a modal (Class D conditions do not require the operator's exclusive focus — they require the operator's response, but the operator may need to read other context in the surface before responding). It is not a toast (toasts are transient; Class D conditions are persistent until resolved through the governed path).

### 7.2 Placement

The Class D escalation banner appears in the inline banner position established in Session 9: between the view header and the section nav, above all section content, non-scrolling.

```
┌────────────────────────────────────────────────────────────────────────────┐
│  VIEW HEADER                                                        56px   │
├────────────────────────────────────────────────────────────────────────────┤
│  ⛔ ESCALATION REQUIRED                                                     │
│                                                                            │
│  Issue:          [What the issue is — specific]                            │
│  Blocked action: [What action cannot proceed]                              │
│  Resolution:     [What decision or clarification is needed]                │
│                                                                            │
│  [Escalate]      [Document and Hold]                                       │
├────────────────────────────────────────────────────────────────────────────┤
│  SECTION NAV                                                               │
│  [Overview] [Evidence] [Decisions] [History] [Actions]                     │
```

The escalation banner lives between the view header and the section nav. It is always above section content. The section nav and section body are still accessible and scrollable — the operator can read the full record while the escalation banner is active.

### 7.3 Banner Anatomy

**Container:**
- Background: `--state-danger-bg` (#2d0d12)
- Border-left: 4px `--state-blocked` (#fa4362) — the red left-border treatment used for hard blocks throughout the system, but at 4px (wider than inline warning banners at 3px) to signal that this is the most severe banner category
- Border-bottom: 1px `--border-danger` — separates from section nav below
- Padding: `--space-5` (20px)
- No border-radius — the banner is a full-width strip, flush with the view edges

**Header line:**
```
⛔ ESCALATION REQUIRED
```
- `⛔` glyph: `--state-blocked`, `--type-md` (14px)
- `ESCALATION REQUIRED`: `--type-base` (13px), `--weight-bold`, `--state-blocked`, letter-spacing 0.3px
- `--space-2` (8px) between glyph and text

**Content block (Issue / Blocked action / Resolution):**

Three labeled lines, each with the same label/value pattern used throughout the system:

| Label | Token | Content |
|---|---|---|
| `Issue:` | `--type-xs`, `--weight-semibold`, `--text-tertiary` | What the Class D condition is. Specific — names the doctrine question or boundary being crossed. Never vague. |
| `Blocked action:` | same | The exact action that cannot proceed. The operator must understand what they were trying to do that triggered the condition. |
| `Resolution:` | same | What decision or clarification is required to resolve the condition. This is actionable: "Escalation required to determine whether [X] constitutes cross-system boundary violation" or "Operator must confirm which approval path applies to [action Y]". |

Label minimum width: 120px. Label right-aligned within that width. Value in `--type-sm`, `--text-primary`.

The `Issue:`, `Blocked action:`, and `Resolution:` content is always filled by the application from the Class D condition detection — it is never left as generic placeholder text. Every Class D banner must answer all three fields specifically. If the condition cannot be described specifically, that is itself a governance failure.

**Control row:**
`[Escalate]` and `[Document and Hold]` are the only controls. They are positioned below the content block, `--space-4` (16px) top margin.

**`[Escalate]`:**
- Width: 120px
- Height: 36px
- Background: `--state-blocked` (#fa4362)
- Text: `--text-primary` (#eaecef), `--type-sm`, `--weight-bold`
- Border-radius: `--radius-md`
- Hover: background lightens (8% white mix)
- On click: opens the escalation recording flow (route to designated escalation path; write escalation record per governance model Structural Enforcement Requirement 8); the banner transitions from the three-field state to a confirmation state: `⛔ ESCALATED — Escalation record written [timestamp]. Awaiting resolution.`
- After escalation is written: the banner remains non-dismissible but is visually quieter — the `[Escalate]` and `[Document and Hold]` buttons are replaced with the confirmation state

**`[Document and Hold]`:**
- Width: 180px
- Height: 36px
- Background: `--surface-elevated`
- Border: 1px `--state-blocked`
- Text: `--state-blocked`, `--type-sm`, `--weight-medium`
- Border-radius: `--radius-md`
- Hover: `--state-danger-bg` background
- On click: writes a governance hold record (action is formally held, not escalated — the operator is documenting that they know about this condition and are explicitly holding the action until resolution); the banner transitions to: `⛔ DOCUMENTED AND HELD — Hold record written [timestamp]. Action remains blocked.`

**No dismiss control.** There is no `×`. There is no "I understand and want to continue anyway." There is no "close this for now." The Class D escalation banner is permanently present until the condition is resolved through the governed path. After resolution (escalation answered, hold lifted), the banner is removed by the application on the next context refresh.

**No proceed-anyway path.** The Action section's other controls remain visible but the blocked action itself is not accessible. If the Action section contains the blocked action as a button, that button shows at `--state-disabled-opacity` with a tooltip: `Blocked — Class D escalation required. See banner above.` The operator can see the blocked action, understand what is blocked, and then use the banner's controls to respond.

### 7.4 Class D Conditions That Trigger the Banner

The banner appears when the application detects:
- A request to perform an action that requires a doctrine exception or override
- A request to route around the normal governed approval path
- An action that depends on ambiguous or unclear approval authority
- A request to merge system roles or collapse system ownership
- A request that makes the action class genuinely ambiguous (not "probably B" — genuinely unclear)
- A request to let continuity artifacts or transcripts substitute for canonical records as the activation basis
- A request to let a delegated worker approve or self-activate a governed mutation
- Any condition where the application cannot safely determine whether an action is within governed bounds

The application must not present this banner as a false positive for Class B or A actions. The Class D classification is reserved for genuine doctrine-level ambiguity or boundary violations. Using it liberally would train operators to dismiss it mentally. It must remain a rare, serious signal.

---

## 8. Review Checkpoint Model

This is the most important section of Session 10. Vague checkpoint definitions produce approval theater. The checkpoint model must be concrete enough that an implementer can write code against it and an auditor can verify that it worked.

### 8.1 What a Completed Checkpoint Is

A completed checkpoint is a specific, verifiable condition that has been met within the current session for the specific record being reviewed. It is not:
- The operator having been on the page for a certain number of seconds
- The operator having scrolled to a certain position
- The operator having reviewed any similar record
- An LLM output asserting that review has occurred
- The presence of a prior approval for a different record

A checkpoint is completed when the operator has taken a specific, explicit action — clicking an expand affordance, confirming a specific review item, or navigating to and returning from a required linked record — within the current session, in the context of the specific record the gate widget is attached to.

### 8.2 How the UI Shows Completed vs Incomplete Checkpoints

Checkpoints are shown as a vertical list in the Actions section, above the gate widget. Each checkpoint is one line:

```
[○ / ✓]  [Checkpoint label]
```

- `○` incomplete: `--text-tertiary`, 16px dot glyph
- `✓` complete: `--state-success`, 16px checkmark glyph
- Checkpoint label: `--type-sm`, `--weight-normal`; color `--text-tertiary` when incomplete, `--text-primary` when complete
- Row height: 32px
- Row padding: `--space-3` (12px) horizontal

When all checkpoints are complete:
- The checkpoint status line above the gate widget transitions from `○ Complete required review before approving` to `✓ Required checkpoints complete — gate is active`
- The gate widget activates (border, shadow, control states update per §4.2)
- Transition: `--transition-spring` for the gate activation moment

When any checkpoint becomes incomplete (because context changed or was invalidated while reviewing):
- That checkpoint's row returns to `○` treatment
- The gate widget returns to inactive state
- The checkpoint status line returns to `○` state
- Any already-entered typed confirmation in an adjacent Class C modal is cleared (if applicable)

### 8.3 Shared Checkpoints (Required on All Records That Have a Gate)

These checkpoints are required for every record with a Class B or C gate, regardless of record type:

**Checkpoint: Overview reviewed**
- Completion condition: The operator has navigated to the Overview section tab. The section must have been the active section for a minimum of 5 seconds (prevents instant tab-click completion). The 5-second timer starts when the section becomes visible, resets if the operator navigates away before 5 seconds.
- Label in UI: `Overview section reviewed`

**Checkpoint: Active governing decisions acknowledged**
- Completion condition: The operator has expanded the DECISIONS row in the context strip during this review session. Alternatively, the Decisions section tab in the center workspace has been the active section for at minimum 5 seconds.
- Label in UI: `Governing decisions reviewed`
- Why: A gate must not activate if the operator has not engaged with the decisions that govern the action being approved. Decision context is the primary governance basis.

**Checkpoint: Staleness notices acknowledged (if any)**
- Completion condition: If any staleness marker is active on the approval request package (in the right panel output card) or on the record being reviewed (inline banner in center surface), the operator must have clicked `[I have reviewed the change — proceed to gate]` on each staleness warning. If no staleness warnings exist, this checkpoint is auto-satisfied.
- Label in UI: `Context change notices acknowledged` (only shown when staleness warnings exist)

**Checkpoint: Session integrity clear (or integrity items acknowledged)**
- Completion condition: No unresolved Class D conditions exist for this record. If any INTEGRITY items in the context strip are flagged as blocking (e.g., a prior approval for this record has been invalidated), those items must be resolved or explicitly acknowledged before the gate activates. If the session integrity is fully clear, this checkpoint is auto-satisfied.
- Label in UI: `Session integrity verified` (only shown when integrity items exist)

### 8.4 Record-Type-Specific Checkpoints

These checkpoints apply only when the gate is attached to a specific record type. They are in addition to the shared checkpoints above.

**Handoff records (Class B gate — handoff activation):**

`Evidence basis reviewed`
- Completion condition: The operator has navigated to the Evidence section tab and remained there for minimum 5 seconds. If any evidence records shown are flagged as stale, the operator must have clicked the expand affordance on at least one stale evidence item.
- Label in UI: `Evidence basis reviewed`

`Scope confirmed: out-of-scope items reviewed`
- Completion condition: The Overview section must show the out-of-scope items list for this handoff, and the operator must have interacted with the expand affordance on that section (or the list is empty, in which case auto-satisfied).
- Label in UI: `Scope and out-of-scope items reviewed`

`All blocking gaps resolved`
- Completion condition: No gaps with severity `blocking` are currently open for the project scope relevant to this handoff. This is checked against current gap records, not against what the approval request package declared at time of packaging. If blocking gaps exist: checkpoint shows as incomplete with a note: `○ Blocking gaps unresolved — [count] blocking gaps remain. Resolve before approving.`
- Label in UI: `No blocking gaps` or `○ [N] blocking gaps unresolved`
- This checkpoint cannot be satisfied by the operator clicking something — it requires actual record state. The gate is blocked until the gap record state changes.

**Launch readiness (Class C gate — launch authorization):**

`Planning-side readiness confirmed`
- Completion condition: The launch readiness review surface's planning-side section has been reviewed (operator has been on the planning readiness sub-section for minimum 5 seconds, or has expanded all collapsed items in it).
- Label in UI: `Planning-side readiness reviewed`

`VEDA signal reviewed`
- Completion condition: The evidence and signal review section has been reviewed (operator has been on the VEDA signal section for minimum 5 seconds). If any signal packages supporting the launch readiness are stale, the operator must have interacted with the `[Refresh Evidence]` affordance or explicitly acknowledged the staleness.
- Label in UI: `Evidence and signal reviewed`
- If evidence is stale and the operator has not acknowledged it: checkpoint shows `○ Signal evidence stale — review before authorizing`

`Execution-side verification confirmed`
- Completion condition: The execution-side verification section has been reviewed and the V Forge verification status is `complete` (a record state check, not an operator click). If verification is not yet complete, the checkpoint shows: `○ Execution verification not yet complete — V Forge has not confirmed readiness`
- Label in UI: `Execution-side verification complete` or `○ Awaiting V Forge verification`
- This checkpoint cannot be satisfied by operator click — it requires record state.

`Cross-system confirmation: all three dimensions satisfied`
- Completion condition: All three dimensions (planning-side, evidence/signal, execution-side) are confirmed in the current launch readiness surface. The UI shows a three-item checklist within the checkpoint (mini-checklist, not separate full checkpoints). If any dimension is unconfirmed, the checkpoint shows incomplete with which dimension is missing.
- Label in UI: `Cross-system confirmation complete` or `○ Cross-system confirmation incomplete — [missing dimension]`

**Return trigger records (Class B gate — routing classification):**

`Finding reviewed: what was found`
- Completion condition: The return trigger overview section has been reviewed (5-second rule applies).
- Label in UI: `Execution finding reviewed`

`Response type selected`
- Completion condition: The operator has selected either `Route to planning` or `Dismiss` (or the maintenance vs replanning distinction sub-choice) from the response options in the review surface. The selection must be explicit — the default state is unselected.
- Label in UI: `Response type selected`
- This checkpoint is completed by the operator making a selection, not by reviewing content. The gate widget activates to confirm the selected response.

**Paid data pull (Class C gate — VEDA paid authorization):**

`Pull scope and cost reviewed`
- Completion condition: The provider detail view showing the pull scope and estimated cost has been active for minimum 5 seconds.
- Label in UI: `Pull scope and cost reviewed`

`External spend acknowledged`
- Completion condition: The operator has clicked a specific `[I have reviewed the cost and scope]` affordance in the provider detail view. This affordance only appears after the scope-and-cost review checkpoint above is satisfied.
- Label in UI: `External spend acknowledged`

### 8.5 What Blocks Class B Gate Activation

The Class B gate widget controls remain at `--state-disabled-opacity` and cursor: not-allowed when any of the following conditions are true:

- Any shared checkpoint is incomplete
- Any record-type-specific checkpoint is incomplete
- A staleness warning has not been acknowledged
- A severe context change has been detected (gate blocked regardless of checkpoints)
- Any blocking gap exists for the relevant scope (handoff-specific)
- A prior approval for this record has been invalidated (EVENT-06) and the inline banner has not been acknowledged via `[Reload Context]`
- A session integrity error is unresolved (EVENT-10)
- Local state divergence exists for any category the gate depends on (EVENT-18)

### 8.6 What Blocks Class C Modal Availability

The `[Proceed to Authorization Gate]` button in the Actions section remains at `--state-disabled-opacity` when any of the following are true:

- Any Class B gate activation blocker from §8.5 is present (the full Class B checkpoint set is a prerequisite for Class C modal availability)
- Cross-system confirmation is incomplete (launch readiness specific)
- Execution-side verification is not confirmed by record state
- Evidence is stale and not acknowledged (for launch readiness)
- The approval request package has been invalidated by a severe context change

### 8.7 Warnings That Require Acknowledgment Before Gate Activates

The following conditions produce warnings that must be acknowledged via `[I have reviewed the change — proceed to gate]` before gate controls activate:

- Decision superseded (EVENT-02) — if the decision was referenced by the approval request package
- Decision created (EVENT-01) — if the new decision is relevant to the action scope (operator must confirm they've read the new decision)
- Evidence stale (EVENT-08) — for records whose approval basis depends on specific evidence records
- Prior approval invalidated (EVENT-06) — requires `[Reload Context]` click, not just reading
- Continuity artifact changed (EVENT-15) — if the approval request package cited a continuity artifact that has changed

### 8.8 How Stale / Changed Context Interrupts Gate Readiness

**Before checkpoint completion:** Staleness or context change markers appear as warnings in the inline banner position. Checkpoints that depended on stale context revert to incomplete.

**After checkpoint completion but before gate control click:** The gate widget remains active but the stale-context warning block appears above it (§4.7). The `[Approve]` / `[Confirm Authorization]` button is suppressed behind the acknowledgment affordance.

**During typed confirmation entry (Class C):** The warning stripe appears in the modal; `[Confirm Authorization]` returns to disabled; typed phrase is cleared (§6.5).

**After approval is clicked but before write confirms:** If the write fails for any reason, the approval event does not occur and the gate returns to its active (pre-click) state with a `⚠ Write failed — retry?` notice.

---

## 9. Gate Activation / Blocking / Staleness Rules — Summary Table

| Condition | Effect on Class B gate | Effect on Class C modal | Recovery path |
|---|---|---|---|
| All shared + record-specific checkpoints complete | Gate activates | Modal button becomes available | N/A — this is the normal active state |
| Any checkpoint incomplete | Gate inactive | Modal button inactive | Complete the checkpoint |
| Staleness warning present, unacknowledged | Gate inactive (warning blocks) | Modal button inactive | Click `[I have reviewed the change — proceed to gate]` |
| Severe context change | Gate blocked (permanent until re-evaluation) | Modal button inactive (permanent) | Request new approval request package from LLM |
| Blocking gap exists (handoff) | Gate inactive | N/A | Resolve the gap record |
| Execution verification incomplete (launch) | N/A | Modal button inactive | Await V Forge verification record update |
| Cross-system confirmation incomplete (launch) | N/A | Modal button inactive | Satisfy missing dimension |
| Prior approval invalidated (EVENT-06) | Gate inactive | Modal button inactive | Acknowledge via `[Reload Context]` |
| Session error (EVENT-10) | Gate inactive | Modal button inactive | Re-initialize session |
| Local state divergence (EVENT-18) | Gate inactive | Modal button inactive | Verify via INTEGRITY row |
| Typed phrase correct (Class C) | N/A | `[Confirm Authorization]` active | N/A |
| Typed phrase incorrect / empty (Class C) | N/A | `[Confirm Authorization]` inactive | Enter correct phrase |
| Context change while modal open | N/A | `[Confirm Authorization]` inactive; phrase cleared | Re-read change; re-enter phrase |
| Severe change while modal open | N/A | `[Confirm Authorization]` removed; only `[Cancel]` | Close modal; re-evaluate |

---

## 10. Placement Within the Center Workspace

### 10.1 Actions Section Position

Session 9 established that the Actions section is the last section tab in the generic record detail view template. Within the Actions section, the layout is:

```
ACTIONS section body
│
├─ Available governed actions (list of action items, each showing action label, class badge, description)
│   Example:
│   [CLASS B] Activate handoff — routes through governed command path
│   [CLASS A] Copy record ID — immediate, no gate
│
├─ Required review checkpoints
│   ○ Overview section reviewed
│   ○ Governing decisions reviewed
│   ○ Evidence basis reviewed
│   ✓ Context change notices acknowledged
│
├─ Gate widget (Class B inline) — LAST ELEMENT IN SECTION
│   [inactive or active per checkpoint state]
│   [Approve]    [Reject]    [Defer]
│
```

The gate widget is always the last element in the Actions section. Nothing appears below it. This is a layout rule, not a preference.

### 10.2 Why Not a Floating Element or Sticky Footer

The gate widget scrolls with the section content. It is not sticky. It is not floating. The operator must scroll to reach it. This is intentional:

If the gate widget were sticky or floating, it would always be visible regardless of whether the operator had engaged with the review content above it. The visual presence of the active gate controls would create implicit pressure to click — "the button is right there, why not just approve?" Requiring a scroll enforces the sequence: review content first, gate at the end.

The 5-second timer on section review checkpoints is also enforced by this scrolling pattern — the operator arrives at the overview section, must stay there to satisfy the timer, then scrolls down through evidence and decisions, and eventually reaches the gate widget. The layout supports the governance sequence rather than fighting it.

### 10.3 When `intent = 'approval_gate'` Routes to This View

When the workspace router opens a record with `intent = 'approval_gate'` (triggered by clicking `[Proceed to Approval Gate]` on a right-panel output card):

1. The record detail view opens in a new tab, with the Actions section tab as the initial active section
2. The view scrolls to the gate widget position — the operator lands at the gate
3. The gate widget is in its inactive state (checkpoints not yet complete)
4. The checkpoint list is fully visible above the gate widget
5. The operator reads the checkpoint list, understands what review is needed, and navigates to the other sections to complete the checkpoints

This sequence makes the governance requirement transparent: the operator arrives at the gate, sees they cannot use it yet, and sees exactly what they need to do. There is no mystery about why the gate is inactive.

### 10.4 Class D Banner Location in Center Surface

The Class D escalation banner appears in the inline banner position from Session 9: between the view header and the section nav. It is always visible regardless of which section tab is active. The section tabs and section body remain accessible — the operator can scroll the record, read context, and then use the `[Escalate]` or `[Document and Hold]` controls.

If both an inline staleness banner (from §6 of Session 9) and a Class D escalation banner are active simultaneously, they stack vertically in the banner position. The Class D banner appears first (higher urgency). The staleness banner appears below it.

---

## 11. Token Usage from Session 2

All visual decisions in this spec reference Session 2 tokens. No new values are introduced.

| Element | Token(s) |
|---|---|
| Class B widget background | `--surface-elevated` |
| Class B widget border resting | `--border-default` 1px |
| Class B widget border active | `--border-accent` (`--accent-primary`) |
| Class B widget active shadow | `--gate-active-shadow` (0 0 0 2px rgba(255,214,79,0.25)) |
| Gate activation transition | `--transition-spring` |
| Widget padding | `--space-6` (24px) |
| Widget border-radius | `--radius-lg` (6px) |
| Class B badge background | `--badge-class-b` (#0d2a3d) |
| Class B badge text | `--badge-class-b-text` (#00b0f4) |
| Class C badge background | `--badge-class-c` (#2d0d12) |
| Class C badge text | `--badge-class-c-text` (#fa4362) |
| `APPROVAL REQUEST` label | `--type-xs`, `--weight-semibold`, `--text-tertiary`, 0.3px letter-spacing |
| Summary field labels | `--type-xs`, `--weight-semibold`, `--text-tertiary` |
| Summary field values | `--type-sm`, `--text-primary` |
| Checkpoint `✓` complete | `--state-success` |
| Checkpoint `○` incomplete | `--text-tertiary` |
| Checkpoint label complete | `--type-sm`, `--text-primary` |
| Checkpoint label incomplete | `--type-sm`, `--text-tertiary` |
| Gate inactive overlay | `--state-disabled-opacity` (0.4) |
| `[Approve]` background | `--accent-primary` (#ffd64f) |
| `[Approve]` text | `--text-inverse` (#212121), `--weight-bold` |
| `[Reject]` border | `--state-danger` |
| `[Reject]` text | `--state-danger` |
| `[Reject]` hover bg | `--state-danger-bg` |
| `[Defer]` border | `--border-default` |
| `[Defer]` text | `--text-secondary` |
| Control height | 36px |
| Control border-radius | `--radius-md` (4px) |
| Control spacing | `--space-3` (12px) |
| Stale-context warning bg | `--staleness-bg` |
| Stale-context warning border | `--staleness-border` (3px left) |
| Stale-context warning text | `--staleness-text` |
| Stale-context ack link | `--text-link`, `--type-sm` |
| Post-approval confirmed text | `--state-success`, `--type-sm`, `--weight-semibold` |
| `[Proceed to Activation ›]` | `--border-accent`, `--accent-primary` text |
| Class C modal background | `--surface-elevated` |
| Class C modal border | 1px `--border-emphasis` |
| Class C modal border-radius | `--radius-lg` (6px) |
| Class C modal padding | `--space-8` (32px) |
| Class C modal shadow | `--elevation-modal` |
| Class C modal z-index | `--z-modal` (500) |
| Modal scrim | `--surface-overlay` (#1a1f23cc) |
| Modal title | `--type-xl` (20px), `--weight-semibold`, `--text-primary` |
| Modal section labels | `--type-sm`, `--weight-semibold`, `--text-secondary` |
| Modal section content | `--type-base` (13px), `--weight-normal`, `--text-primary` |
| Irreversibility notice bg | `--state-danger-bg` |
| Irreversibility notice border | 3px `--state-danger` left |
| Irreversibility header | `--type-sm`, `--weight-semibold`, `--state-danger` |
| `[Confirm Authorization]` bg | `--state-danger` (#fa4362) |
| `[Confirm Authorization]` text | `--text-primary`, `--weight-bold` |
| `[Confirm Authorization]` inactive | `--state-disabled-opacity` (0.4) |
| `[Cancel]` | `--surface-raised`, `--border-default`, `--text-secondary` |
| Typed confirmation required phrase | `--font-mono`, `--type-sm`, `--state-warning` |
| Typed confirmation input bg | `--surface-raised` |
| Typed confirmation input border resting | `--border-default` |
| Typed confirmation input border correct | `--border-accent` |
| Typed confirmation input text | `--font-mono`, `--type-base`, `--text-primary` |
| Typed confirmation placeholder | `--text-tertiary` |
| Typed confirmation correct `✓` | `--state-success` |
| Class D banner bg | `--state-danger-bg` (#2d0d12) |
| Class D banner left border | 4px `--state-blocked` (#fa4362) |
| Class D banner bottom border | 1px `--border-danger` |
| Class D banner padding | `--space-5` (20px) |
| Class D `⛔` header | `--state-blocked`, `--type-base` |
| Class D `ESCALATION REQUIRED` | `--type-base`, `--weight-bold`, `--state-blocked`, 0.3px letter-spacing |
| Class D content labels | `--type-xs`, `--weight-semibold`, `--text-tertiary` |
| Class D content values | `--type-sm`, `--text-primary` |
| `[Escalate]` bg | `--state-blocked` (#fa4362) |
| `[Escalate]` text | `--text-primary`, `--weight-bold` |
| `[Document and Hold]` border | 1px `--state-blocked` |
| `[Document and Hold]` text | `--state-blocked`, `--weight-medium` |
| Control height (Class D) | 36px |
| Actions section body padding | Inherited from Session 9: `--space-5` sides, `--space-6` top |

---

## 12. What Session 10 Resolves

- The complete gate surface set is specified: Class B inline widget, Class C modal, typed confirmation input, Class D escalation banner. Sessions 13–15 can reference these designs directly without inventing local variants.
- The review checkpoint model is concrete: specific verifiable conditions per checkpoint, shared checkpoints that apply to all record types with gates, record-type-specific checkpoints for handoffs, launch readiness, return triggers, and paid data pulls.
- "What blocks gate activation" is answerable by implementers: a list of specific conditions, each with a recovery path. No vague "after review is complete."
- The typed confirmation input is explicitly designed to doctrine requirements: distinct element, not a checkbox, not pre-populated, not dismissible without completion, case-sensitive exact match, context-change interrupts require re-entry.
- The Class D escalation banner is designed as the highest-urgency non-modal surface: non-dismissible, two paths only (`[Escalate]` and `[Document and Hold]`), no dismiss option, no proceed-anyway option.
- The stale-context warning treatment is concrete: specific content (what changed, not vague "context changed"), acknowledgment affordance, severe-change blocks gate permanently pending re-evaluation.
- Placement rules are confirmed and concrete: gate widget at the bottom of the Actions section, below all review content; Class D banner in the inline banner position above section nav.
- The `[Approve]` button's amber-fill treatment is the single exception in the application where the accent color is used as a filled button background — this signals the primary governance action at the gate.
- The `[Confirm Authorization]` button's danger-fill treatment communicates the irreversible consequence of Class C actions.
- Post-approval and post-escalation states are specified so the operator receives clear confirmation that a governance event has been persisted.
- The context-change-while-modal-is-open behavior is specified: warning stripe, button returns to inactive, phrase cleared, severe change removes confirm button entirely.

---

## 13. What Session 10 Does Not Resolve Yet

- **The five-step routing flow from output card to approval event** — Session 11. The gate design is now a stable input. Session 11 specifies the full state sequence: right-panel card before `[Proceed to Approval Gate]` click, center surface during review (gate inactive), center surface when checkpoints complete (gate activates), center surface during typed confirmation, center surface after approval written, right-panel card staleness marker if context changed during review.
- **The `[Proceed to Activation ›]` activation path** — referenced in §4.6 as the button that appears after approval is written. The exact activation API call sequence (write approval record → confirm write → call activation API) is the implementation architecture's domain, not UX; but Session 11 should specify the UX state during activation and the success/failure treatments that follow.
- **Notification events for approval written** — when an approval record is persisted, a session-level notification fires. That notification's design (toast-style, in-app notification) is Session 12 (Session Start Integrity Check + Alert/Notification System).
- **The handoff review surface** — the review content that appears in sections Overview, Evidence, Decisions, and History for a handoff record is Session 13's deliverable. Session 10 specifies where the gate widget sits within the Actions section; Session 13 specifies what the operator reviews before reaching that gate widget.
- **The return trigger review surface** — the review content for return trigger records, including the maintenance vs replanning response selection (which is itself a checkpoint per §8.4), is Session 13.
- **The launch readiness review surface** — the three-dimension review content, blocking conditions panel, VEDA signal review section, and cross-system confirmation checklist are Session 14. Session 10 specifies the checkpoint criteria; Session 14 designs the review content those criteria are checking.
- **The VEDA paid data pull review surface** — the provider detail view that satisfies the paid data pull checkpoints is Session 9/15 territory.
- **Escalation record format and resolution workflow** — what happens after `[Escalate]` is clicked (who receives the escalation, what the record contains, how it is resolved) is the governance model and potentially a future workflow doc. Session 10 specifies the UX surface; the downstream escalation workflow is out of scope.
- **Hold record format** — similarly, what the `[Document and Hold]` record contains and how it is lifted is governance/workflow territory.
- **The rejection continuity path** — Session 10 specifies that rejection records are persisted and that rejected actions appear in the record's history. The History section's display of rejection records is part of the generic record detail template that Session 9 established; specific rejection record treatment in the History section is a Session 9 extension, not Session 10's job to invent.

---

## 14. Recommended Inputs to Session 11

Session 11 is the Review-to-Gate Routing Flow — the single canonical pattern from typed output card to completed approval event.

**Session 11 must specify the five states:**

1. **Right-panel output card before `[Proceed to Approval Gate]` click.** The Approval Request Package card in the right panel, in its inert-awaiting-review state. The `[Proceed to Approval Gate]` button should be visually distinguished from standard response options (amber border, established in Session 5). The card should show the action class badge, the action summary, and the `AWAITING REVIEW` inertness treatment from Session 2 governance tokens.

2. **Center surface during review (gate not yet active).** The operator is in the center workspace. The Actions section tab is the initial active section (per `intent = 'approval_gate'` router behavior from Session 9). The gate widget is visible in inactive state. The checkpoint list is visible. The operator understands they need to review other sections before the gate activates. Session 11 should specify what the incomplete checkpoint list looks like in context of a real handoff record and define the sequence the operator follows.

3. **Center surface when required checkpoints are complete (gate activates).** The `--transition-spring` animation fires on the gate widget. The checkpoint status line transitions from `○` to `✓`. The `[Approve]` / `[Reject]` / `[Defer]` controls become fully active. Session 11 should specify whether the gate widget scrolls into view automatically at this moment, or whether the operator is expected to have already scrolled to the Actions section.

4. **Center surface during typed confirmation (Class C only).** The `[Proceed to Authorization Gate]` button has been clicked. The Class C modal is open. The operator is in the typed confirmation phase. Session 11 should specify the modal's relationship to the center workspace behind the scrim.

5. **Center surface after approval written (confirmation state).** Post-approval state per §4.6. The `[Proceed to Activation ›]` button is available. Session 11 should specify what happens to the right-panel output card at this moment — does it update to reflect that the approval has been written? Does it receive a different status treatment?

**One open question Session 11 should resolve:**

When the operator clicks `[Proceed to Approval Gate]` on a right-panel output card and navigates to the center workspace, should the right-panel card remain visible in the interaction area, or does navigating away from the right panel suppress it? This matters for the experience of returning to the right panel after completing an approval — does the operator see the card with an updated status, or has it scrolled away? Session 11 should take a clear position.

**What Session 11 should not redesign:**

The gate widget designs from this session are stable inputs to Session 11. Session 11 specifies transitions and states between the surfaces; it does not redesign the gate widget itself. If Session 11 encounters a genuine contradiction with Session 10's designs, that contradiction should be documented and resolved explicitly — not resolved by silently redefining the gate widget's behavior.
