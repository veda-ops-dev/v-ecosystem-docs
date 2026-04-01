# Extension State and Context Model

## Purpose

This document defines what state and context must be visible, loaded, synchronized, bounded, freshness-aware, and reviewable for the human operator and the LLM inside the V Ecosystem VS Code extension.

It exists to answer:

```text
What counts as current state in the extension, what must always be visible to the operator and to the LLM, how are workflow stage, decision context, evidence basis, session integrity, orchestration state, continuity artifacts, and tool-surface posture represented, how is stale or incomplete context surfaced, how is cross-system referenced context shown without implying ownership transfer, and what must never be treated as canonical state?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the core state categories the extension must track and surface
- the distinction between current system and referenced systems
- workflow stage context representation
- decision continuity context loading and visibility
- evidence basis and freshness visibility
- session integrity state
- orchestration state visibility
- continuity artifact visibility and non-authority posture
- session tool-surface posture visibility
- synchronization requirements across multiple state surfaces
- stale, incomplete, and uncertain context handling
- non-canonical source exclusions
- context refresh requirements before approval-sensitive actions

This document builds on and assumes the active binding of:
- `extension-llm-behavior-contract.md` — LLM posture, allowed outputs, framing requirements
- `extension-governance-and-gating-model.md` — action classes, gate requirements, approval chain
- `extension-agent-orchestration-model.md` — delegated runtime posture
- `extension-memory-and-continuity-model.md` — continuity artifact rules
- `extension-system-init-and-tool-surface-model.md` — session-basis and tool-surface assembly rules

---

## Out of Scope

This document does not define:

- specific visual layout or component design of the extension UI
- database schema or API endpoint design
- MCP tool schemas
- credential or authentication mechanics
- complete Project V, VEDA, or V Forge data models

---

## System

- interfaces

---

## Core Rule

The extension must never allow either the operator or the LLM to be uncertain about what state is actually loaded, what system is active, what workflow stage is current, what governing decisions apply, what evidence basis is loaded, what continuity artifacts are active, what delegated runtime posture is currently in play, or what the LLM does not currently know.

Context must be explicit, bounded, and visible — not inferred, not fluid, and not magical.

If context is hidden, stale, or inferred from topic drift, the extension is creating conditions for authority creep and governance failure regardless of how good the behavior contract and gating model are.

---

## Core State Categories

The extension must track and surface nine categories of state. These are not all the same kind of state — some are operator-set, some are loaded from governed records, some are session-computed. All nine must be visible and current.

### 1. Project Scope State
What project the session is bound to. Set by the operator at session start. Enforced by the session token. The LLM cannot change this.

Required visibility: always visible in the status strip, cannot be collapsed or hidden.

### 2. Current System State
Which of the three systems (Project V, VEDA, V Forge) governs the active reasoning and action posture of the current session activity.

This is an explicit operator-set or operator-confirmed context — not an inference from conversation topic. See Current System vs Referenced Systems section.

Required visibility: always visible in the status strip.

### 3. Workflow Stage State
The current lifecycle or workflow stage for the active work scope within the current system. Loaded from governed records.

Required visibility: always visible in the status strip. Must show current stage, next gate, and blocking conditions.

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
The current admitted tool posture for the session: what major system surface is primary, whether referenced-system read posture is active, whether delegated workers are operating on narrowed tool surfaces, and whether the session basis has been refreshed materially.

Required visibility: visible in bounded form so the operator is not guessing what the runtime has made available to the LLM.

---

## Current System vs Referenced Systems

The extension must maintain a clear distinction between the current system and any referenced systems.

### Current System
The current system is the system that governs the active action posture, operator permissions, and LLM output scope for the current activity. It is one of: Project V, VEDA, or V Forge.

The current system is:
- explicitly set or confirmed by the operator, not inferred from conversation topic
- displayed in the status strip at all times
- the basis for which action class table applies to the current interaction
- the basis for which system surface commands, tools, and buttons are available

The current system does not change because the conversation moved to a topic associated with a different system. It changes only when the operator explicitly switches context.

### Referenced Systems
Referenced systems are the other systems that provide bounded context into the current session. They provide read-only, non-canonical, visibly-attributed context unless a separately admitted governed path says otherwise.

Referencing V Forge execution state from within a Project V session is allowed. But that reference must remain visibly labeled as: "REFERENCED FROM V FORGE — Project V does not own this state."

The extension must show referenced system data with a visual ownership marker that cannot be removed or collapsed. The marker identifies the source system and makes clear no ownership has transferred.

### Why this matters
If the extension allows the current system to drift based on conversation topic — for example, switching from Project V planning posture to VEDA signal posture because the operator started asking about keywords — the LLM will produce outputs that mix authority frames without either party noticing. The operator will not know which system's rules currently apply. The LLM will not know either. Drift follows.

Explicit current system, maintained by operator action and shown always, is how this is prevented.

---

## Workflow Stage Context

Workflow stage is not a general feeling of "where we are." It is a specific governed state loaded from the records of the current system.

### What must be shown

For the current system and active work scope, the extension must always show:

- **Current stage** — the named lifecycle or workflow stage (e.g., `Planning — Active`, `Handoff — Awaiting Approval`, `Execution — Halted`)
- **Next gate** — what must happen before the next transition is eligible (e.g., `Readiness evaluation required`, `Operator approval required`, `Pre-launch verification incomplete`)
- **Blocking conditions** — any active conditions that prevent the next gate from being satisfied (e.g., `3 open critical gaps`, `Prior approval stale`, `Decision conflict unresolved`)
- **Pending approvals** — any approval events that have been initiated but not completed

### How it is loaded

Workflow stage context is loaded from the governed records of the current system (Project V, VEDA, or V Forge) via the MCP session. It is not inferred from conversation. It is not held in session memory across extension restarts without a reload.

### How staleness is handled

If the workflow stage cannot be loaded from current records — for example, because the MCP session has dropped or records are unavailable — the extension must display an explicit unavailability state:

```text
WORKFLOW STAGE: Unavailable — context not loaded
[Reload Context]
```

The LLM must not proceed with workflow-stage-dependent outputs when stage context is unavailable. The behavior contract requires that the LLM produce an Uncertainty Notice in this condition rather than proceeding on inference.

---

## Decision Continuity Context

Decision continuity context is the set of governing decisions that are active for the current project scope and relevant to the current work. This must be loaded and visible — not inferred.

### What must be loaded

At session start, the extension must load from Project V records:

- all active governing decisions for the current project (non-superseded, non-invalidated, in `recorded` status)
- the decision title, short description, and date for each
- whether any decision has a staleness marker

### What must be shown

The decision context must be visible in the context strip as a named set, not a count alone:

```text
GOVERNING DECISIONS (content-hub)
[dec-03] Prioritize search-first content  [2026-02-14] [active]
[dec-05] Hosting vertical over SaaS tier  [2026-03-10] [active]
```

A count without names ("2 decisions loaded") is insufficient. The LLM and the operator both need to know which specific decisions are in play.

### Change notifications

When the decision set changes during a session — a new decision is created, a decision is superseded, or a decision is invalidated — the extension must surface a notification:

```text
⚠️ GOVERNING CONTEXT CHANGED
Decision [dec-05] has been superseded by [dec-07].
Recommendations based on dec-05 may need re-evaluation.
[Review Change]
```

This notification must be shown before the LLM produces any further outputs that could have been affected by the change. The LLM must treat prior recommendations that referenced the changed decision as potentially stale.

### Conflict detection

When two or more loaded decisions appear to conflict — for example, decision A prioritizes one system target while decision B prioritizes another — the extension must surface the conflict in the decision context display rather than hiding it:

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

- the specific evidence records being loaded (by record identifier, not just category)
- the source system: always VEDA
- the capture or observation timestamp for each record
- the trust posture classification for each record (high, medium, low, uncertain)
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

The "Proceed Without Refreshing" path must require an explicit acknowledgment, which is logged. This acknowledges that the action is being approved on stale evidence, which is a governance-relevant fact that must be preserved.

### Cross-system attribution

When evidence from VEDA is displayed or referenced in a Project V or V Forge session context, the ownership label must remain attached:

```text
EVIDENCE — SOURCE: VEDA (referenced, not owned by Project V)
[obs-047] Hosting keyword snapshot ...
```

This label is not optional decoration. It enforces the cross-system reference rule. Without it, the operator and the LLM may treat VEDA evidence as Project V canonical state, which is a boundary failure.

---

## Session Integrity State

Session integrity state is the set of unresolved items from prior sessions or current session activity that require operator attention before substantive work proceeds. It prevents "fresh session amnesia" — the condition where a new session proceeds as if nothing significant was left unresolved.

### Session start check

At session start, the extension must load and display the session integrity state before presenting the LLM interaction surface:

```text
SESSION INTEGRITY CHECK — content-hub
─────────────────────────────────────
⚠️  Pending approval (unactivated, 2026-03-28): hosting-comparison handoff
⚡  Unreviewed return trigger (2026-04-01): V Forge finding — intent shift
⚪  Stale readiness state: seo-tech-audit (readiness evaluation > 7 days old)

[Review Items] [Dismiss All — I'll handle these later]
```

"Dismiss All" is allowed but must be logged. If the operator dismisses session integrity items, that dismissal is a governance-relevant fact: the operator chose to proceed without resolving them.

### Session integrity items

The session integrity state must include:

- **Pending approvals** — Class B or C approval requests that were initiated but not completed in prior sessions
- **Unresolved return triggers** — V Forge findings routed to Project V that have not been reviewed or resolved
- **Stale readiness states** — work items where the readiness evaluation is older than the governed threshold for the current workflow stage
- **Unresolved decision conflicts** — conflicts in the governing decision set that were detected but not resolved
- **Session health issues** — token expiry, MCP loss, synchronization failure, or missing required context category

### Token and scope integrity

If the session token is invalid, expired, or the MCP connection has dropped, the status strip must reflect this immediately:

```text
◈ V: content-hub  ⚠️ SESSION ERROR — MCP connection lost
```

All Class B and Class C actions must be blocked while the session is in an error state. The LLM must not produce governance-sensitive outputs while session integrity is broken. The extension must prompt re-initialization before allowing further work.

---

## Orchestration State

Orchestration state is the visible runtime state of delegated work and specialist participation.

### What must be shown when orchestration is active

When the extension is using orchestration for meaningful delegated work, the operator must be able to determine:

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

The extension must surface the current admitted tool posture in bounded form.

### What must be visible where relevant

- which system surface is primary for the current session
- whether referenced-system read posture is active
- whether the session basis was materially refreshed
- whether delegated workers are operating on narrowed tool surfaces
- whether the runtime is currently operating under restricted posture due to missing context, stale context, or gating state

The operator does not need a raw dump of every tool constantly.
But the operator must not be left guessing whether the model is operating on a broad or narrow tool basis.

---

## Context Visibility Rules

These rules govern what must be visible, when, and to whom.

### Always visible to the operator (status strip — non-collapsible)

- active project name
- current system (Project V / VEDA / V Forge)
- current workflow stage (or "unavailable" if not loaded)
- session health (active / error / expired)

These four elements must be visible at all times. They may not be hidden, collapsed, or minimized. They are the governance baseline that the operator must be able to see with a glance.

### Visible on demand but explicitly accessible (context strip or equivalent)

- governing decisions (names, not just count)
- evidence records loaded (with freshness and trust posture)
- referenced system context (labeled with ownership attribution)
- pending session integrity items
- any active conflict or staleness warnings
- active continuity artifacts
- current orchestration state when materially relevant
- session tool-surface posture summary

These must be accessible without more than one click from any active state of the extension.

### What must be visible to the LLM before it responds

The LLM must have access to the following before producing any non-trivial output:

- current project scope (via session token)
- current system
- current workflow stage
- active governing decisions (names and status)
- evidence records loaded (with trust posture and freshness)
- admitted continuity artifacts, if they are participating in the session basis
- the bounded current tool posture relevant to its runtime role

If any of these are unavailable, the LLM must produce an Uncertainty Notice indicating specifically what context is missing, rather than proceeding on inference.

### What the LLM must not claim if it is not visibly loaded

The LLM must not reference a specific governing decision, evidence record, workflow stage, continuity artifact, or runtime posture as though it is loaded context unless that item appears in the current visible session basis.

This is not about limiting the LLM's knowledge — it is about preventing the LLM from claiming context-based authority it has not been verifiably given for this session.

---

## Synchronization Rules

When multiple surfaces display context or state, they must remain synchronized. The operator and the LLM must not appear to be operating from different realities.

### Primary synchronization requirement

The status strip, context strip, and LLM interaction panel must reflect the same state. If the decision context changes (e.g., a decision is superseded), all three surfaces must update before the operator can continue interacting.

This same rule applies to:
- continuity artifact refresh
- orchestration-state changes that affect operator review
- session-basis refresh after invalidation
- current-system change

### Conflict between surfaces

If a surface appears to show different state than another — for example, the LLM references a governing decision that no longer appears in the context strip — the extension must treat this as a synchronization error and surface it:

```text
⚠️ CONTEXT SYNC ERROR
The LLM referenced [dec-05] but this decision is no longer in the active decision context.
[Reload Context] [Review Decision History]
```

The LLM must not continue producing outputs based on the stale reference until the context is synchronized.

### After write operations

After any Class B or C action succeeds — creating a record, activating a handoff, recording a decision — the context strip and status strip must refresh automatically. The operator must not need to manually refresh to see the updated state.

### Session token expiry

When the session token expires mid-session, the synchronization requirement applies to recovery: the re-initialized session must reload all context categories fresh from the governed records, not restore from the prior session's in-memory state. Prior session context is not canonical current state.

---

## Stale, Incomplete, and Uncertain Context

### Stale context

Context is stale when it was loaded at some prior point and the underlying records may have changed. Stale context must be marked with an explicit indicator — not hidden, not silently aged out.

Stale context markers apply to:
- evidence records past the validity window
- readiness evaluations past the validity threshold for the workflow stage
- pending approvals whose basis conditions may have changed
- decision context not refreshed since a material time gap
- continuity artifacts with aging or freshness risk

Stale context does not block Class A actions but must block Class B and Class C approval gates until refreshed or acknowledged where doctrine permits acknowledgment.

### Incomplete context

Incomplete context is context that should be loaded but is not — for example, governing decisions that exist but could not be retrieved because the MCP connection was unavailable.

Incomplete context must be shown explicitly:

```text
⚠️ DECISION CONTEXT INCOMPLETE
Governing decisions could not be loaded (MCP unavailable).
Operating without decision context.
[Retry Load]
```

The LLM must not produce recommendations or approval request packages while decision context is incomplete. It must produce an Uncertainty Notice instead.

### Explicit uncertainty boundaries

The extension must support an explicit "LLM does not know" state that is visible to the operator. This is different from the LLM claiming uncertainty within a response — it is the extension surfacing, before the LLM responds, that a specific category of context is not available.

When context is missing that the LLM would normally use, the context strip must show the gap:

```text
EVIDENCE CONTEXT: Not loaded — [Load Evidence]
```

The operator then sees, before asking the LLM anything, that it will be operating without evidence basis. They can choose to load it or proceed knowing the limitation.

### Context invalidation events

The following events must invalidate the relevant context category and require a reload or refresh before the extension proceeds normally:

- a governing decision is created, superseded, or invalidated → decision context invalid
- a new evidence observation arrives that contradicts loaded evidence → evidence basis flagged stale
- an approval event completes → workflow stage context invalid, must reload
- a return trigger is received → session integrity state updated
- the session token expires → all context invalid, re-initialization required
- a meaningful compaction event occurs → continuity state and visible session basis must refresh
- a delegated worker completes with admitted findings → continuity/orchestration state must refresh
- current-system posture changes → tool-surface posture and session basis must refresh

Context invalidation events must surface to both the operator and the LLM. The LLM must not continue responding in the prior context frame after an invalidation event without acknowledging the change.

---

## Context Refresh Requirements Before Actions

Certain actions require that specific context categories be confirmed current before the approval gate is presented.

### Before Class B approval gates

- Decision context must be current (loaded within the session, not stale by governance definition)
- Workflow stage context must be current
- Any session integrity items directly relevant to the action must be acknowledged
- Any delegated worker output being used as support must remain visibly non-canonical

### Before Class C approval gates

All Class B requirements plus:

- Evidence basis relevant to the action must be current (within the freshness threshold for the action type)
- Evidence staleness that has been acknowledged must be logged with the approval record
- Any conflict in governing decisions must be resolved or explicitly acknowledged and logged
- Any continuity artifact used for orientation must not replace fresh canonical verification

### Before launch-sensitive Class C gates

All Class C requirements plus:

- Evidence currency must be confirmed, not just checked (the operator must explicitly confirm it, not just see it loaded)
- Cross-system readiness state (V Forge execution verification, VEDA signal review) must be loaded as referenced context with ownership labels intact
- The evidence acknowledgment required by the launch readiness workflow must be recorded as a separate step before the final authorization gate

---

## What Must Never Be Treated as Canonical Current State

The extension must never treat the following as canonical current state:

### Prior LLM output in chat or session history
Session history is not a record system. A recommendation the LLM produced in a prior session is not a governing decision. A finding the LLM produced is not a system record. A summary the LLM produced is not the governed basis for an approval. Canonical state comes from the governed records of the current system, loaded fresh.

### Continuity artifacts
Working memory, durable memory, compact-boundary products, transcript-derived continuity, and worker findings are not canonical records. They may improve continuity. They do not become the governing basis for actions.

### Inferred system context from conversation topic
If the operator starts talking about keyword performance, the extension must not silently switch to VEDA as the current system. The current system is set by the operator, not by topic inference.

### Cached but unconfirmed state from a prior session
When a new session starts, all core state categories must be loaded fresh from governed records. Prior session cache is not canonical even if it appears current.

### A referenced system's state as the current system's truth
When Project V references V Forge execution state, that execution state is not Project V canonical state. The ownership label is the mechanism that enforces this. It must not be dropped.

### The LLM's in-session reasoning as evidence
The LLM's analysis, interpretations, and conclusions produced within the session are not evidence records. Evidence comes from VEDA-owned observatory records with provenance and freshness metadata. An LLM reasoning output is not a substitute for that.

### Unsaved panel state
Any panel that has not been saved to the governed record system is not canonical state. If the operator edits something in the extension but it has not been persisted through the governed API, the edit does not exist in governing terms.

### Data from a different project scope
Data from a project other than the one bound to the current session token is not current state for this session. It does not matter if the operator believes it is relevant — if it belongs to another project, it is not in scope.

---

## Human-In-The-Loop Principle

State and context visibility is not cosmetic. It is the mechanism by which the operator's governance role remains real.

An operator who cannot see what context the LLM is using cannot meaningfully evaluate the LLM's outputs. An operator who cannot see that evidence is stale cannot make an informed approval decision. An operator who does not know the current system cannot evaluate whether the LLM's outputs are within bounds. An operator who cannot tell whether orchestration or continuity artifacts are influencing the runtime is reviewing theater instead of a governed system.

If the extension hides, infers, or smooths over context, operator review degrades from a governance function into a ritual.

Every visibility rule in this document exists to prevent that degradation.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the LLM must not claim context it cannot see as loaded
- the current system governs its output posture — and it cannot change the current system
- referenced system data carries an ownership label that must be preserved in outputs
- stale evidence must be flagged, not cited as current
- decision conflicts must be surfaced, not navigated around
- session history and continuity artifacts are not canonical state and must not be cited as governing basis
- orchestration state is runtime state, not system ownership
- the extension will surface what the LLM does not know — the LLM must honor those boundaries rather than paper over them

If the LLM treats the richness of its loaded context as authorization to act, or cites prior session outputs or continuity artifacts as governing evidence, this state model is being violated.

---

## Usage

This document should be used:

- when designing what state the extension loads and when
- when designing what context the extension makes visible and how
- when designing synchronization behavior between extension surfaces
- when evaluating whether a stale or incomplete context condition is being surfaced correctly
- when reviewing whether cross-system referenced state is carrying the required ownership labels
- when designing the session start sequence and session integrity check
- when designing orchestration visibility and continuity visibility surfaces
- when writing interaction-model docs that depend on explicit current context

---

## Related Docs

- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-agent-orchestration-model.md`
- `extension-memory-and-continuity-model.md`
- `extension-system-init-and-tool-surface-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/evidence-continuity-model.md`
- `../governance/approval-and-escalation-model.md`
- `../governance/report-structure-and-required-fields.md`
- `../interfaces/mcp-coordination-model.md`
- `../interfaces/operator-surface-interfaces.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../workflows/handoff-workflow.md`
- `../workflows/launch-readiness-workflow.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
