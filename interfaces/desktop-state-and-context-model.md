# Desktop State and Context Model

## Purpose

This document defines what state and context must be visible, loaded, synchronized, bounded, freshness-aware, and reviewable for the human operator and the LLM inside the V Ecosystem desktop application.

It exists to answer:

```text
What counts as current state in the desktop application, what must always be visible to the operator and to the LLM, how are workflow stage, decision context, evidence basis, session integrity, orchestration state, continuity artifacts, and tool-surface posture represented, how is stale or incomplete context surfaced, how is cross-system referenced context shown without implying ownership transfer, and what must never be treated as canonical state?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the core state categories the desktop application must track and surface
- the distinction between current system and referenced systems
- workflow stage context representation
- decision continuity context loading and visibility
- evidence basis and freshness visibility
- session integrity state
- orchestration state visibility
- continuity artifact visibility and non-authority posture
- session tool-surface posture visibility
- synchronization requirements across multiple desktop surfaces
- stale, incomplete, and uncertain context handling
- non-canonical source exclusions
- context refresh requirements before approval-sensitive actions

This document builds on and assumes the active binding of:
- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-memory-and-continuity-model.md`
- `desktop-system-init-and-tool-surface-model.md`
- `desktop-surface-architecture.md`
- `runtime-sidecar-and-nerve-model.md`
- `local-first-architecture.md`

---

## Out of Scope

This document does not define:

- specific visual layout or component design of the desktop UI
- database schema or API endpoint design
- MCP tool schemas
- credential or authentication mechanics
- complete Project V, VEDA, or V Forge data models

---

## System

- interfaces

---

## Core Rule

The desktop application must never allow either the operator or the LLM to be uncertain about what state is actually loaded, what system is active, what workflow stage is current, what governing decisions apply, what evidence basis is loaded, what continuity artifacts are active, what delegated runtime posture is currently in play, or what the LLM does not currently know.

Context must be explicit, bounded, and visible — not inferred, not fluid, and not magical.

If context is hidden, stale, or inferred from topic drift, the desktop application is creating conditions for authority creep and governance failure regardless of how good the behavior contract and gating model are.

---

## Core State Categories

The desktop application must track and surface nine categories of state. These are not all the same kind of state — some are operator-set, some are loaded from governed records, some are session-computed. All nine must be visible and current.

### 1. Project Scope State
What project the session is bound to. Set by the operator at session start. Enforced by the session token. The LLM cannot change this.

Required visibility: always visible in the topbar status layer, cannot be collapsed or hidden.

### 2. Current System State
Which of the three systems, Project V, VEDA, or V Forge, governs the active reasoning and action posture of the current session activity.

This is an explicit operator-set or operator-confirmed context, not an inference from conversation topic. See Current System vs Referenced Systems section.

Required visibility: always visible in the topbar status layer.

### 3. Workflow Stage State
The current lifecycle or workflow stage for the active work scope within the current system. Loaded from governed records.

Required visibility: always visible in the status/context layer. Must show current stage, next gate, and blocking conditions.

### 4. Decision Continuity Context
The governing decisions currently active for the project scope. Loaded from Project V records at session start and refreshed when the record set changes.

Required visibility: visible in the context strip and on demand. Changes to this context must surface a notification.

### 5. Evidence Basis and Freshness State
The VEDA signal, evidence, and observatory outputs currently loaded for use in the session. Includes trust posture and freshness markers.

Required visibility: visible in the context strip and on demand. Staleness must surface as a marker, not be hidden.

### 6. Session Integrity State
Pending approvals, unresolved return triggers, stale readiness states, unresolved decision conflicts, and session health conditions from prior sessions or current session activity that require operator attention before proceeding.

Required visibility: surfaced at session start and updated when conditions change. Unresolved session integrity items must be visible before the operator and LLM proceed with substantive work.

### 7. Orchestration State
Whether orchestration is active, what delegated subtasks exist, what lifecycle state each subtask is in, whether specialist roles are active, and whether delegated work is awaiting review, blocked, cancelled, or failed.

Required visibility: visible whenever orchestration is materially participating in the session. Meaningful delegated work must not be hidden behind generic loading indicators.

### 8. Continuity Artifact State
What working memory, durable memory, transcript-derived continuity, compact-boundary products, and delegated findings are currently active in the session basis.

Required visibility: visible in the context strip or equivalent continuity surface when active. Non-canonical continuity artifacts must remain distinguishable from canonical loaded state.

### 9. Session Tool-Surface Posture
The current admitted tool posture for the session: what major system surface is primary, whether referenced-system read posture is active, whether delegated workers are operating on narrowed tool surfaces, whether the session basis has been refreshed materially, and whether compaction or refresh changed the currently active runtime basis.

Required visibility: visible in bounded form so the operator is not guessing what the runtime has made available to the LLM.

---

## Current System vs Referenced Systems

The desktop application must maintain a clear distinction between the current system and any referenced systems.

### Current System
The current system is the system that governs the active action posture, operator permissions, and LLM output scope for the current activity. It is one of: Project V, VEDA, or V Forge.

The current system is:
- explicitly set or confirmed by the operator, not inferred from conversation topic
- displayed in the topbar and context surfaces at all times
- the basis for which action class table applies to the current interaction
- the basis for which system surface commands, tools, and controls are available

The current system does not change because the conversation moved to a topic associated with a different system. It changes only when the operator explicitly switches context.

### Referenced Systems
Referenced systems are the other systems that provide bounded context into the current session. They provide read-only, non-canonical, visibly attributed context unless a separately admitted governed path says otherwise.

Referencing V Forge execution state from within a Project V session is allowed. But that reference must remain visibly labeled as: `REFERENCED FROM V FORGE — Project V does not own this state.`

The desktop application must show referenced system data with a visible ownership marker that cannot be removed or collapsed. The marker identifies the source system and makes clear no ownership has transferred.

### Why this matters
If the desktop application allows the current system to drift based on conversation topic — for example, switching from Project V planning posture to VEDA signal posture because the operator started asking about keywords — the LLM will produce outputs that mix authority frames without either party noticing. The operator will not know which system's rules currently apply. The LLM will not know either. Drift follows.

Explicit current system, maintained by operator action and shown always, is how this is prevented.

---

## Workflow Stage Context

Workflow stage is not a general feeling of "where we are." It is a specific governed state loaded from the records of the current system.

### What must be shown

For the current system and active work scope, the desktop application must always show:

- **Current stage** — the named lifecycle or workflow stage, for example `Planning — Active`, `Handoff — Awaiting Approval`, `Execution — Maintenance`, or `Execution — Halted`
- **Next gate** — what must happen before the next transition is eligible, for example `Readiness evaluation required`, `Operator approval required`, or `Pre-launch verification incomplete`
- **Blocking conditions** — any active conditions that prevent the next gate from being satisfied, for example `3 open critical gaps`, `Prior approval stale`, or `Decision conflict unresolved`
- **Pending approvals** — any approval events that have been initiated but not completed
- **Maintenance vs replanning posture** — when execution is active, whether the current posture is `Execution — Maintenance` (bounded work within approved scope requiring no replanning) or whether a return trigger or changed condition has escalated posture to `Replanning — In Progress`. These two postures must be visibly distinct. An operator must not need to open a detail view to determine whether the ecosystem is in routine maintenance or in active governed replanning.

### How it is loaded

Workflow stage context is loaded from the governed records of the current system, Project V, VEDA, or V Forge, via the governed backend and runtime/session path. It is not inferred from conversation. It is not held in session memory across desktop restarts without a reload.

Not all stage names map directly to a single record field. Some stages are derived composite states:

- Stages in the **planning and handoff family** are anchored to `Handoff.status` values and `WorkItem` / `Initiative` / `Objective` status values as defined in `controlled-vocabularies.md`. These have settled record anchors.
- `Handoff — Prepared` and `Handoff — Awaiting Approval` both correspond to `Handoff.status = ready`. The distinction between them is governance-posture-derived: `Handoff — Awaiting Approval` means a pending approval record exists in the approval store for that handoff and has not yet been satisfied. The desktop derives this from `Handoff.status = ready` **plus** the presence of an unsatisfied pending approval record. There is no separate `Handoff.status` value for `awaiting-approval`.
- **Intake stages** (`Intake — Framing`, `Intake — Evaluation`, `Intake — Outcome Pending`) are operational-workflow-level states. As of this writing, the Project V schema does not include a dedicated `IntakeRecord` or `IntakeCandidate` table. These stages have no settled single-record anchor. An implementer deriving intake stage must treat it as a workflow-session-derived posture rather than a backend-record load until the intake record model is explicitly settled.
- **Maintenance vs replanning stages** (`Execution — Maintenance`, `Replanning — In Progress`) are workflow-posture distinctions, not schema-field distinctions. The Project V schema has no `MaintenanceRecord` or `ReplanningRecord`. These stages are derived from return trigger state and Project V operational posture. Implementers must treat them as runtime-derived posture rather than backend-record loads.
- **Launch readiness stages** (`Launch Readiness — In Progress`, `Launch Readiness — Blocked`, `Launch Authorization — Pending`, `Post-Launch — Active`) are cross-system process-level states. The Project V schema does not include a dedicated launch readiness record family. These stages are workflow-session-derived posture until a launch readiness record model is explicitly settled.

Where a stage has no settled record anchor, the desktop application must not claim it is loaded from canonical governed records. It must surface it as the current workflow posture based on available evidence, and must be willing to show `Unavailable` if the posture cannot be determined from loaded context.

### Recognized Stage Names

The desktop application must represent workflow stage using names that are consistent with the workflow spine. Recognized stage names are:

**Intake stages (Project V):**
- `Intake — Framing` — intake question is being formed. *No settled schema record anchor; treat as workflow-session-derived posture.*
- `Intake — Evaluation` — intake candidate is being evaluated against planning and governance posture. *No settled schema record anchor; treat as workflow-session-derived posture.*
- `Intake — Outcome Pending` — intake evaluation is complete; outcome awaits operator confirmation or approval. *No settled schema record anchor; treat as workflow-session-derived posture.*

**Planning and handoff stages (Project V):**
- `Planning — Active` — work is in active governed planning. *Anchored to `Objective`, `Initiative`, or `WorkItem` status = `active`.*
- `Handoff — Prepared` — handoff package is prepared but not yet activated; approval or release condition may still be pending. *Anchored to `Handoff.status = ready` with no pending approval record for that handoff.*
- `Handoff — Awaiting Approval` — handoff is prepared and explicitly awaiting operator approval before activation may occur. *Derived from `Handoff.status = ready` plus the presence of an unsatisfied pending approval record in the approval store. There is no distinct schema status value for this sub-state.*
- `Handoff — Activated` — handoff has been activated and execution responsibility has transferred to V Forge. *Anchored to `Handoff.status = handed_off`.*

**Execution and maintenance stages (V Forge):**
- `Execution — Active` — V Forge is executing within the handed-off scope. *Derived from handoff in `handed_off` status with no active return trigger or replanning event.*
- `Execution — Maintenance` — ongoing bounded work within existing approved scope that does not require replanning. *No dedicated schema record; derived from execution-active posture with no active return trigger routed to replanning.*
- `Execution — Halted` — execution is stopped pending return-to-planning, operator review, or resolved blocking condition. *Derived from execution context; no dedicated halt record in current schema.*

**Return and replanning stages (cross-system):**
- `Return — Pending Review` — a return trigger has arrived and has not yet been reviewed or routed by the operator. *Anchored to return trigger lifecycle state `arrived` or `acknowledged` in session integrity state.*
- `Replanning — In Progress` — a governed replanning event is active; prior governing decisions are under bounded reconsideration. *No dedicated schema record; derived from return trigger in `routed` state combined with Project V operational posture. No `ReplanningRecord` exists in current schema.*

**Launch readiness stages:**
- `Launch Readiness — In Progress` — the multi-stage cross-system launch readiness confirmation is underway. *No dedicated schema record; workflow-session-derived posture.*
- `Launch Readiness — Blocked` — a blocking condition prevents launch authorization from being sought. *No dedicated schema record; workflow-session-derived posture.*
- `Launch Authorization — Pending` — all readiness stages are confirmed; launch authorization is being sought from the operator. *No dedicated schema record; derived from approval store state for the launch action.*
- `Post-Launch — Active` — launch-sensitive execution has completed; VEDA observatory observation is active for the launched scope; maintenance and replanning may follow from post-launch findings. *No dedicated schema record; workflow-session-derived posture.*

These names must remain stable across surfaces. Stage naming must not drift based on conversation topic or operator shorthand. An LLM that reads only this document should be able to recognize which workflow phase each stage name belongs to, and which stages have settled record anchors vs. which are workflow-posture-derived pending schema settlement.

### How staleness is handled

If the workflow stage cannot be loaded from current records, for example because runtime/session support is unavailable or records are unavailable, the desktop application must display an explicit unavailability state:

```text
WORKFLOW STAGE: Unavailable — context not loaded
[Reload Context]
```

The LLM must not proceed with workflow-stage-dependent outputs when stage context is unavailable. The behavior contract requires that the LLM produce an Uncertainty Notice in this condition rather than proceeding on inference.

---

## Decision Continuity Context

Decision continuity context is the set of governing decisions that are active for the current project scope and relevant to the current work. This must be loaded and visible, not inferred.

### What must be loaded

At session start, the desktop application must load from Project V records:

- all active governing decisions for the current project, non-superseded and non-invalidated
- the decision title, short description, and date for each
- whether any decision has a staleness marker

### What must be shown

The decision context must be visible in the context strip as a named set, not a count alone:

```text
GOVERNING DECISIONS (content-hub)
[dec-03] Prioritize search-first content  [2026-02-14] [active]
[dec-05] Hosting vertical over SaaS tier  [2026-03-10] [active]
```

A count without names, such as `2 decisions loaded`, is insufficient. The LLM and the operator both need to know which specific decisions are in play.

### Change notifications

When the decision set changes during a session — a new decision is created, a decision is superseded, or a decision is invalidated — the desktop application must surface a notification:

```text
⚠️ GOVERNING CONTEXT CHANGED
Decision [dec-05] has been superseded by [dec-07].
Recommendations based on dec-05 may need re-evaluation.
[Review Change]
```

This notification must be shown before the LLM produces any further outputs that could have been affected by the change. The LLM must treat prior recommendations that referenced the changed decision as potentially stale.

### Conflict detection

When two or more loaded decisions appear to conflict — for example, decision A prioritizes one system target while decision B prioritizes another — the desktop application must surface the conflict in the decision context display rather than hiding it:

```text
⚠️ DECISION CONFLICT DETECTED
[dec-03] and [dec-07] may conflict on target-system priority.
Resolve before producing approval-sensitive outputs.
```

A conflict does not block Class A outputs, but it must block Class B and Class C approval gates until the operator has explicitly acknowledged or resolved the conflict.

### What governing decisions are not

A governing decision loaded into the decision context strip is not:

- an instruction to the LLM to execute anything
- an automatic approval of any action class
- a planning record that the LLM may modify

It is context for reasoning. The LLM must reference it, not act on it autonomously.

---

## Evidence Basis and Freshness

Evidence basis context is the VEDA signal, evidence, and observatory outputs currently loaded into the session for use in planning, recommendation, or review. It is never planning truth. It is always VEDA truth, referenced with explicit ownership labels.

### What must be loaded

At session start or when the operator loads evidence context:

- the specific evidence records being loaded, by record identifier, not just category
- the source system, always VEDA
- the capture or observation timestamp for each record
- the trust posture classification for each record, such as high, medium, low, or uncertain
- any known provenance gaps or limitations

### What must be shown

The evidence context must be visible in the context strip:

```text
EVIDENCE LOADED (content-hub) — SOURCE: VEDA
[obs-047] Hosting keyword snapshot  [2026-04-01 14:32]  [high trust]
[obs-041] SERP delta — hosting      [2026-03-28 09:15]  [high trust]  ⚠️ 3 days old
[rd-003]  Research doc (imported)   [2026-02-14]         [medium trust]
```

Freshness and trust posture are not optional display elements. They are required. An evidence record shown without its freshness and trust posture has had its continuity integrity stripped, which is a violation of the evidence continuity model.

### Staleness markers

Evidence is marked stale when:

- it has exceeded the typical validity window for its evidence type
- newer contradicting evidence has been loaded
- the conditions it described have visibly changed

Stale evidence must be shown with an explicit marker:

```text
[obs-041] SERP delta — hosting  [2026-03-28]  ⚠️ STALE — 3 days old, may not reflect current conditions
```

The LLM must not cite stale evidence as though it were current. When evidence is stale, the LLM must include an Uncertainty Notice in any output that depends on it.

### Evidence that blocks actions

For Class C actions — particularly launch-sensitive and external actions — evidence basis must be confirmed current before the approval gate is presented. If the evidence basis is stale, the approval gate must be blocked:

```text
⛔ EVIDENCE STALE — approval gate blocked
Evidence [obs-041] supporting this action is stale.
Refresh evidence before proceeding.
[Refresh Evidence] [Proceed Without Refreshing — I Accept the Risk]
```

The `Proceed Without Refreshing` path must require an explicit acknowledgment, which is logged. This acknowledges that the action is being approved on stale evidence, which is a governance-relevant fact that must be preserved.

### Evidence refresh triggers

Evidence transitions from stale to refreshed when the operator initiates a refresh and new records are successfully loaded from VEDA. The following trigger paths are recognized:

- **Operator-initiated manual refresh** — the operator clicks `[Refresh Evidence]` in the context strip or within the stale evidence gate block. This is the primary path.
- **New VEDA observation loaded** — if the operator loads a newer VEDA observation record that covers the same signal or topic as a stale record, the newer record is shown as current and the older record is superseded in the evidence context. The older record is not deleted from the session's evidence history; it is marked `[superseded]`.
- **Operator explicit acknowledgment without refresh** — for Class C gates only: the operator may select `Proceed Without Refreshing — I Accept the Risk`. This does not mark the evidence as refreshed. It marks the gate action as acknowledged-on-stale-evidence and logs that acknowledgment. The evidence record remains stale.

The following do not trigger a transition to refreshed:
- Passage of time alone
- Session restart without an explicit reload
- LLM output that describes what refreshed evidence might say
- Any continuity artifact referencing the prior evidence load

### Post-refresh consequence to prior outputs

Refreshing evidence does not retroactively validate prior LLM outputs that were produced when the evidence was stale. Those outputs retain their staleness markers. If the operator wants a fresh output reflecting the refreshed evidence, they must re-request it explicitly. The LLM must not treat evidence refresh as permission to silently revise or re-issue a prior output without explicit operator framing.

### Cross-system attribution

When evidence from VEDA is displayed or referenced in a Project V or V Forge session context, the ownership label must remain attached:

```text
EVIDENCE — SOURCE: VEDA (referenced, not owned by Project V)
[obs-047] Hosting keyword snapshot ...
```

This label is not optional decoration. It enforces the cross-system reference rule. Without it, the operator and the LLM may treat VEDA evidence as Project V canonical state, which is a boundary failure.

---

## Session Integrity State

Session integrity state is the set of unresolved items from prior sessions or current session activity that require operator attention before substantive work proceeds. It prevents `fresh session amnesia` — the condition where a new session proceeds as if nothing significant was left unresolved.

### Session start check

At session start, the desktop application must load and display the session integrity state before presenting substantive interaction:

```text
SESSION INTEGRITY CHECK — content-hub
─────────────────────────────────────
⚠️  Pending approval (unactivated, 2026-03-28): hosting-comparison handoff
⚡  Unreviewed return trigger (2026-04-01): V Forge finding — intent shift
⚪  Stale readiness state: seo-tech-audit (readiness evaluation > 7 days old)

[Review Items] [Dismiss All — I'll handle these later]
```

`Dismiss All` is allowed but must be logged. If the operator dismisses session integrity items, that dismissal is a governance-relevant fact: the operator chose to proceed without resolving them.

### Session integrity items

The session integrity state must include:

- **Pending approvals** — Class B or C approval requests that were initiated but not completed in prior sessions
- **Unresolved return triggers** — V Forge findings routed to Project V that have not been reviewed or resolved
- **Stale readiness states** — work items where the readiness evaluation is older than the governed threshold for the current workflow stage
- **Unresolved decision conflicts** — conflicts in the governing decision set that were detected but not resolved
- **Session health issues** — token expiry, runtime loss, synchronization failure, or missing required context category

### Return trigger lifecycle

A return trigger is a finding routed from V Forge to Project V signaling that an execution result may warrant planning attention. It is not an automatic replanning event. It is a bounded finding that the operator must evaluate and act on.

Return triggers have four valid states:

**`arrived`**
The trigger has been received and is visible in the session integrity state. It has not yet been reviewed by the operator.
- Session integrity indicator shows `⚡ Return trigger — unreviewed`.
- V Forge navigation view shows the trigger prominently.
- The LLM must not treat the trigger's content as a planning directive.
- The operator may continue Class A work without resolving the trigger.
- The trigger is non-blocking on arrival. It becomes a blocking integrity item if left unresolved when the operator attempts a Class C gate in the affected workflow scope. Acknowledgment alone (opening the trigger detail) does not clear the block — resolution requires routing or dismissal.

**`acknowledged`**
The operator has opened the return trigger detail in the center surface and reviewed the finding.
- Session integrity indicator updates: `⚡ Return trigger — reviewed, action pending`.
- No further surface change occurs automatically.
- The LLM may now reference the trigger's content as a reviewed finding if the operator frames work in that context.

**`routed`**
The operator has used the `Route return trigger` response option to route the finding to the Project V planning surface through the governed return-to-planning interface.
- Session integrity item resolved. Attention badge clears.
- The routing is logged as a governance-relevant fact with timestamp.
- Any downstream effects on DECISIONS or STAGE that result from the routed finding follow the applicable governing decision or workflow stage events in `desktop-invalidation-and-refresh-matrix.md`.
- The return trigger record is preserved in the session audit record. It is not deleted.

**`dismissed`**
The operator has used the `Dismiss return trigger` response option.
- Session integrity item resolved. Attention badge clears.
- The dismissal is logged as a governance-relevant fact with timestamp and optional reason.
- The return trigger record is preserved in the session audit record. Dismissal does not delete the finding.
- The LLM must not re-surface the dismissed trigger in subsequent outputs unless the operator explicitly re-opens the topic.

**What constitutes resolution:**
A return trigger is resolved when its state reaches either `routed` or `dismissed`. An `acknowledged` trigger is not resolved — it has been seen but not acted on. Unresolved return triggers (both `arrived` and `acknowledged`) are shown as active session integrity items at the next session start.

**What a return trigger is not:**
- It is not a planning authorization.
- It is not a replanning event.
- It is not a signal transfer that automatically imports V Forge findings as Project V canonical state.
- The LLM must not treat trigger arrival or acknowledgment as authorization to produce Recommendations that replan in response to the trigger's content without explicit operator framing.

### Token and scope integrity

If the session token is invalid, expired, or runtime/session support has dropped, the status layer must reflect this immediately:

```text
◈ V: content-hub  ⚠️ SESSION ERROR — runtime connection lost
```

All Class B and Class C actions must be blocked while the session is in an error state. The LLM must not produce governance-sensitive outputs while session integrity is broken. The desktop application must prompt re-initialization before allowing further work.

---

## Orchestration State

Orchestration state is the visible runtime state of delegated work and specialist participation.

### What must be shown when orchestration is active

When the desktop application is using orchestration for meaningful delegated work, the operator must be able to determine:

- whether orchestration is active
- what delegated subtasks exist
- what role each specialist is performing
- what lifecycle state each subtask is in
- whether a subtask is awaiting review, failed, cancelled, or blocked
- whether a subtask contributed outputs to the active session basis

### Minimum lifecycle visibility

Meaningful delegated work must not collapse into a generic spinner. At minimum, delegated subtasks should surface states such as:
- `pending`
- `running`
- `completed`
- `failed`
- `cancelled`
- `awaiting_review` where relevant

### State boundary rule

Orchestration state is runtime state, not canonical system state.
It is visible because the operator needs to understand how the current session is functioning, not because orchestration owns any truth domain.

The mechanical task modeling, lifecycle transitions, attribution, and cancellation posture that support this runtime visibility are defined in the task lifecycle implementation-design companion.

---

## Continuity Artifact State

Continuity artifact state is the set of non-canonical runtime artifacts currently participating in the session basis.

### What may appear here

- active working memory entries
- active session-durable memory entries
- active compact-boundary products
- transcript-derived continuity references admitted to the session
- delegated worker findings retained for parent-session continuity

### Visibility rule

Where continuity artifacts are materially influencing the current session basis, the operator must be able to tell:
- what kind of artifact is active
- where it came from
- whether it is aging or stale
- whether it can be cleared or dismissed

### Non-authority rule

Continuity artifacts must remain visibly distinct from canonical state.
A memory artifact must not look like a decision record.
A transcript artifact must not look like an approval record.
A compacted summary must not look like loaded evidence.

---

## Session Tool-Surface Posture

The desktop application must surface the current admitted tool posture in bounded form.

### What must be visible where relevant

- which system surface is primary for the current session
- whether referenced-system read posture is active
- whether the session basis was materially refreshed
- whether delegated workers are operating on narrowed tool surfaces
- whether the runtime is currently operating under restricted posture due to missing context, stale context, or gating state
- whether compaction or other refresh events changed the currently active runtime basis

The operator does not need a raw dump of every tool constantly.
But the operator must not be left guessing whether the model is operating on a broad or narrow tool basis.

The mechanical rebuild and publication of this posture are defined in the tool-surface implementation-design companion.

---

## Context Visibility Rules

These rules govern what must be visible, when, and to whom.

### Always visible to the operator (topbar/status layer — non-collapsible)

- active project name
- current system, Project V, VEDA, or V Forge
- current workflow stage, or `unavailable` if not loaded
- session health, active, error, or expired

These four elements must be visible at all times. They may not be hidden, collapsed, or minimized. They are the governance baseline that the operator must be able to see with a glance.

### Visible on demand but explicitly accessible (context strip or equivalent)

- governing decisions, names, not just count
- evidence records loaded with freshness and trust posture
- referenced system context labeled with ownership attribution
- pending session integrity items
- any active conflict or staleness warnings
- active continuity artifacts
- current orchestration state when materially relevant
- session tool-surface posture summary

These must be accessible without more than one click from any active state of the desktop application.

### What must be visible to the LLM before it responds

The LLM must have access to the following before producing any non-trivial output:

- current project scope via session token
- current system
- current workflow stage
- active governing decisions, names and status
- evidence records loaded, with trust posture and freshness
- admitted continuity artifacts if they are participating in the session basis
- the bounded current tool posture relevant to its runtime role

If any of these are unavailable, the LLM must produce an Uncertainty Notice indicating specifically what context is missing, rather than proceeding on inference.

### What the LLM must not claim if it is not visibly loaded

The LLM must not reference a specific governing decision, evidence record, workflow stage, continuity artifact, or runtime posture as though it is loaded context unless that item appears in the current visible session basis.

This is not about limiting the LLM's knowledge — it is about preventing the LLM from claiming context-based authority it has not been verifiably given for this session.

---

## Synchronization Rules

When multiple surfaces display context or state, they must remain synchronized. The operator and the LLM must not appear to be operating from different realities.

### Primary synchronization requirement

The topbar/status layer, context strip, center review surfaces, and interaction surfaces must reflect the same state. If the decision context changes, for example a decision is superseded, all relevant surfaces must update before the operator can continue interacting.

This same rule applies to:
- continuity artifact refresh
- orchestration-state changes that affect operator review
- session-basis refresh after invalidation
- current-system change
- active-tool-surface rebuilds that materially change runtime posture
- meaningful compaction events that change the active session basis

### Conflict between surfaces

If a surface appears to show different state than another — for example, the LLM references a governing decision that no longer appears in the context strip — the desktop application must treat this as a synchronization error and surface it:

```text
⚠️ CONTEXT SYNC ERROR
The LLM referenced [dec-05] but this decision is no longer in the active decision context.
[Reload Context] [Review Decision History]
```

The LLM must not continue producing outputs based on the stale reference until the context is synchronized.

### After write operations

After any Class B or C action succeeds — creating a record, activating a handoff, recording a decision — the context strip and status layer must refresh automatically. The operator must not need to manually refresh to see the updated state.

### Session token expiry

When the session token expires mid-session, the synchronization requirement applies to recovery: the re-initialized session must reload all context categories fresh from the governed records, not restore from the prior session's in-memory state. Prior session context is not canonical current state.

---

## Stale, Incomplete, and Uncertain Context

### Stale context

Context is stale when it was loaded at some prior point and the underlying records may have changed. Stale context must be marked with an explicit indicator, not hidden, not silently aged out.

Stale context markers apply to:
- evidence records past the validity window
- readiness evaluations past the validity threshold for the workflow stage
- pending approvals whose basis conditions may have changed
- decision context not refreshed since a material time gap
- continuity artifacts with aging or freshness risk

Stale context does not block Class A actions. Whether stale context blocks Class B or Class C gates depends on the category and the specific gate:
- Stale decision context blocks Class B and Class C gates until refreshed or acknowledged.
- Stale evidence blocks Class C gates that require evidence currency. It does not automatically block Class B gates unless doctrine for the specific action requires current evidence.
- Other stale categories follow the blocking rules defined per-event in `desktop-invalidation-and-refresh-matrix.md`.

Do not treat the general staleness rule as a single blanket Class B + C block. The per-category and per-event rules in the matrix govern.

### Incomplete context

Incomplete context is context that should be loaded but is not — for example, governing decisions that exist but could not be retrieved because runtime/session support was unavailable.

Incomplete context must be shown explicitly:

```text
⚠️ DECISION CONTEXT INCOMPLETE
Governing decisions could not be loaded.
Operating without decision context.
[Retry Load]
```

The LLM must not produce recommendations or approval request packages while decision context is incomplete. It must produce an Uncertainty Notice instead.

### Explicit uncertainty boundaries

The desktop application must support an explicit `LLM does not know` state that is visible to the operator. This is different from the LLM claiming uncertainty within a response — it is the desktop application surfacing, before the LLM responds, that a specific category of context is not available.

When context is missing that the LLM would normally use, the context strip must show the gap:

```text
EVIDENCE CONTEXT: Not loaded — [Load Evidence]
```

The operator then sees, before asking the LLM anything, that it will be operating without evidence basis. They can choose to load it or proceed knowing the limitation.

### Context invalidation events

This document defines what state categories exist and their general freshness and blocking posture. The canonical mapping of each specific event to its full set of consequences — affected categories, per-surface behavior, LLM consequences, blocking posture, and sequencing — is defined in `desktop-invalidation-and-refresh-matrix.md`. That document is the authority for event-to-consequence mapping. This document does not maintain a competing list.

The event families that can trigger invalidation or refresh of one or more state categories include:

- governing decision changes (creation, supersession, invalidation, conflict detection)
- approval events (written, superseded, or invalidated)
- evidence changes (loaded, stale, or refreshed)
- session token expiry or runtime scope breakage
- compaction events with per-category post-compaction validation
- delegated task completion or failure
- current-system change
- return trigger arrival and lifecycle transitions
- local support-state divergence from backend canonical state

For each event family, see `desktop-invalidation-and-refresh-matrix.md` for the specific trigger definition, affected categories, blocking posture, and sequencing priority.

Context invalidation events must surface to both the operator and the LLM. The LLM must not continue responding in the prior context frame after an invalidation event without acknowledging the change.

### Per-category validation rule

Validation and freshness must remain per category.
The runtime must not collapse state validity into one coarse session-valid/session-invalid boolean.

A session may be valid in one category and stale, missing, conflicted, or blocked in another.
The desktop application must preserve that distinction visibly.

The compaction implementation companion relies on this rule for post-compaction per-category validation and refresh behavior.

---

## Context Refresh Requirements Before Actions

Certain actions require that specific context categories be confirmed current before the approval gate is presented.

### Before Class B approval gates

- decision context must be current, loaded within the session and not stale by governance definition
- workflow stage context must be current
- any session integrity items directly relevant to the action must be acknowledged
- any delegated worker output being used as support must remain visibly non-canonical

### Before Class C approval gates

All Class B requirements plus:

- evidence basis relevant to the action must be current, within the freshness threshold for the action type
- evidence staleness that has been acknowledged must be logged with the approval record
- any conflict in governing decisions must be resolved or explicitly acknowledged and logged
- any continuity artifact used for orientation must not replace fresh canonical verification

### Before launch-sensitive Class C gates

All Class C requirements plus:

- evidence currency must be confirmed, not just checked
- cross-system readiness state, including V Forge execution verification and VEDA signal review, must be loaded as referenced context with ownership labels intact
- the evidence acknowledgment required by the launch readiness workflow must be recorded as a separate step before the final authorization gate

---

## What Must Never Be Treated as Canonical Current State

The desktop application must never treat the following as canonical current state:

### Prior LLM output in chat or session history
Session history is not a record system. A recommendation the LLM produced in a prior session is not a governing decision. A finding the LLM produced is not a system record. A summary the LLM produced is not the governed basis for an approval. Canonical state comes from the governed records of the current system, loaded fresh.

### Continuity artifacts
Working memory, durable memory, compact-boundary products, transcript-derived continuity, and worker findings are not canonical records. They may improve continuity. They do not become the governing basis for actions.

### Inferred system context from conversation topic
If the operator starts talking about keyword performance, the desktop application must not silently switch to VEDA as the current system. The current system is set by the operator, not by topic inference.

### Cached but unconfirmed state from a prior session
When a new session starts, all core state categories must be loaded fresh from governed records. Prior session cache is not canonical even if it appears current.

### A referenced system's state as the current system's truth
When Project V references V Forge execution state, that execution state is not Project V canonical state. The ownership label is the mechanism that enforces this. It must not be dropped.

### The LLM's in-session reasoning as evidence
The LLM's analysis, interpretations, and conclusions produced within the session are not evidence records. Evidence comes from VEDA-owned observatory records with provenance and freshness metadata. An LLM reasoning output is not a substitute for that.

### Unsaved UI state
Any workspace state that has not been saved to the governed record system is not canonical state. If the operator edits something in the desktop application but it has not been persisted through the governed API, the edit does not exist in governing terms.

### Data from a different project scope
Data from a project other than the one bound to the current session token is not current state for this session. It does not matter if the operator believes it is relevant — if it belongs to another project, it is not in scope.

---

## Human-In-The-Loop Principle

State and context visibility is not cosmetic. It is the mechanism by which the operator's governance role remains real.

An operator who cannot see what context the LLM is using cannot meaningfully evaluate the LLM's outputs. An operator who cannot see that evidence is stale cannot make an informed approval decision. An operator who does not know the current system cannot evaluate whether the LLM's outputs are within bounds. An operator who cannot tell whether orchestration or continuity artifacts are influencing the runtime is reviewing theater instead of a governed system.

If the desktop application hides, infers, or smooths over context, operator review degrades from a governance function into a ritual.

Every visibility rule in this document exists to prevent that degradation.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the LLM must not claim context it cannot see as loaded
- the current system governs its output posture, and it cannot change the current system
- referenced system data carries an ownership label that must be preserved in outputs
- stale evidence must be flagged, not cited as current
- decision conflicts must be surfaced, not navigated around
- session history and continuity artifacts are not canonical state and must not be cited as governing basis
- orchestration state is runtime state, not system ownership
- the desktop application will surface what the LLM does not know — the LLM must honor those boundaries rather than paper over them
- post-compaction state validity is per category, not a single yes or no session claim

If the LLM treats the richness of its loaded context as authorization to act, or cites prior session outputs or continuity artifacts as governing evidence, this state model is being violated.

---

## Usage

This document should be used:

- when designing what state the desktop application loads and when
- when designing what context the desktop application makes visible and how
- when designing synchronization behavior between desktop surfaces
- when evaluating whether a stale or incomplete context condition is being surfaced correctly
- when reviewing whether cross-system referenced state is carrying the required ownership labels
- when designing the session start sequence and session integrity check
- when designing orchestration visibility and continuity visibility surfaces
- when writing interaction-model docs that depend on explicit current context
- when implementing post-compaction validation and refresh so they remain per-category rather than collapsing into coarse session-valid claims

---

## Related Docs

- `desktop-llm-behavior-contract.md`
- `desktop-governance-and-gating-model.md`
- `desktop-agent-orchestration-model.md`
- `desktop-memory-and-continuity-model.md` or successor naming
- `desktop-system-init-and-tool-surface-model.md` or successor naming
- `runtime-sidecar-and-nerve-model.md`
- `desktop-surface-architecture.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/report-structure-and-required-fields.md`
- `mcp-coordination-model.md`
- `operator-surface-interfaces.md`
- `veda-to-project-v-signal-interface.md`
- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/handoff-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../ecosystem/decisions/ADR-011-tauri-2-desktop-is-the-operator-host.md`
- `desktop-invalidation-and-refresh-matrix.md`
