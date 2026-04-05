# Desktop Invalidation and Refresh Matrix

## Purpose

This document is the canonical reference for every event that triggers context invalidation or refresh in the V Ecosystem desktop application.

It exists to answer:

```text
For each event that can change the validity of loaded context, what state categories are affected, what invalidation or refresh is required, what must happen on each UI surface, what must the LLM do, what is the blocking posture, and in what order must these consequences fire?
```

This is a Tier 1 companion to `desktop-state-and-context-model.md`. That doc is the authority for:
- what state categories exist
- what each category represents
- general per-category freshness rules and validity posture
- what may and may not be treated as canonical current state

This document is the authority for:
- the complete enumeration of trigger events that cause context invalidation or refresh
- what state categories each event affects
- the specific invalidation and refresh requirement per event
- the per-surface UI consequence per event
- the LLM consequence per event
- the blocking posture per event
- sequencing priority when multiple events fire

All other docs that reference invalidation, refresh, or synchronization events defer to this matrix for the canonical event list and consequence mapping. No other doc should maintain a competing trigger list or per-event consequence specification.

---

## Scope

This document governs:

- the complete enumeration of trigger events that cause context invalidation or refresh
- the affected state categories per event
- the invalidation and refresh requirement per event
- the UI consequence per surface per event
- the LLM consequence per event
- the blocking posture per event
- the sequencing rule when multiple events fire concurrently
- the owning doc for detailed behavior of each event family

This document does not define:

- the internal mechanics of how each state category is stored or loaded
- the exact visual styling of banners, markers, or modals
- backend API or schema design
- approval class definitions (see `desktop-governance-and-gating-model.md`)
- memory class definitions (see `desktop-memory-and-continuity-model.md`)

---

## System

- interfaces

---

## Core Rule

Every event in this matrix must produce its stated consequences. Partial propagation — where some surfaces update but others do not — is a synchronization failure. Silent propagation — where surfaces update without notifying the operator — is a governance failure.

The LLM consequences in this matrix are not optional surface polish. They define what the LLM must do to remain within bounds after a context-changing event.

---

## State Category Reference

The nine state categories from `desktop-state-and-context-model.md` are referenced throughout this matrix using the short labels below:

| Label | Full Name |
|---|---|
| **SCOPE** | Project Scope State |
| **SYSTEM** | Current System State |
| **STAGE** | Workflow Stage State |
| **DECISIONS** | Decision Continuity Context |
| **EVIDENCE** | Evidence Basis and Freshness State |
| **INTEGRITY** | Session Integrity State |
| **ORCH** | Orchestration State |
| **CONTINUITY** | Continuity Artifact State |
| **TOOLSURFACE** | Session Tool-Surface Posture |

---

## Surface Reference

| Label | Surface |
|---|---|
| **TOPBAR** | Topbar status/project layer |
| **LEFTNAV** | Left navigation panel |
| **CTXSTRIP** | Context strip in right panel |
| **PANEL** | Right interaction/output panel |
| **CENTER** | Center detail/review surfaces |
| **ALERT** | Alert, banner, and notification surfaces |
| **LOWER** | Lower trace/orchestration surface (when active) |

---

## Sequencing Rules

When multiple events fire concurrently or in close sequence, the following priority order applies:

1. **Session token expiry / runtime scope breakage** — supersedes all other in-flight events. All surfaces enter degraded posture immediately. No other event processing continues until re-initialization.
2. **Blocking invalidation events** (events marked `BLOCK` in the matrix) — must complete their propagation before the next LLM turn begins. If a blocking event fires while a turn is in progress, the turn completes but its output is marked stale before rendering.
3. **Non-blocking refresh events** — may propagate asynchronously but must complete before any Class B or Class C gate is presented.
4. **Informational surface updates** — may complete in background without interrupting the current interaction.

When two blocking events fire simultaneously, propagate in the order listed in this matrix. The later event's consequences layer on top of the earlier event's already-applied consequences.

---

## The Matrix

---

### EVENT-01 — Governing Decision Created

**Trigger:** A new governing decision is written to Project V records.

| Dimension | Specification |
|---|---|
| **Affected categories** | DECISIONS |
| **Invalidation requirement** | Decision context is stale immediately upon creation. Must reload before any Class B or C output that would reference the decision set. |
| **Refresh requirement** | Reload full active decision set from Project V records. |
| **Topbar** | No change required unless the new decision creates a conflict (see EVENT-03). |
| **Left nav** | No change required. |
| **Context strip** | Updates immediately to show the new decision in the named decision list. |
| **Interaction panel** | Any in-progress or rendered output cards that could be affected by the new decision receive a `⚠ CONTEXT UPDATED — new governing decision` staleness marker. |
| **Center surfaces** | Any open center surface showing the decision set updates immediately. Inline banner: `New governing decision created: [dec-id]. Prior outputs may not reflect this decision.` |
| **Alert surface** | In-app notification if the operator is mid-session and has active outputs that could be affected. |
| **Lower surface** | No change required. |
| **LLM consequence** | Must not produce further outputs referencing the prior decision set as complete until context strip reflects the reload. Must acknowledge the new decision exists before producing Class B recommendations. |
| **Blocking posture** | Non-blocking for Class A. Blocks Class B and C gates until context strip shows the reloaded decision set. |
| **Sequencing priority** | Level 3 (non-blocking refresh). |
| **Owning doc** | `desktop-state-and-context-model.md` § Decision Continuity Context |

---

### EVENT-02 — Governing Decision Superseded

**Trigger:** An active governing decision is superseded by a newer decision.

| Dimension | Specification |
|---|---|
| **Affected categories** | DECISIONS |
| **Invalidation requirement** | Decision context invalid immediately. Prior outputs that cited the superseded decision are stale. |
| **Refresh requirement** | Reload full active decision set. Remove superseded decision from active set. |
| **Topbar** | No required change unless conflict results. |
| **Left nav** | No required change. |
| **Context strip** | Updates immediately. Superseded decision removed from named list or shown with `[superseded]` marker. New decision added. |
| **Interaction panel** | All rendered output cards that cited the superseded decision receive: `⚠ DECISION SUPERSEDED — [dec-id] replaced by [dec-id-new]. This output may need re-evaluation.` |
| **Center surfaces** | Any open center surface showing the superseded decision receives an inline banner: `[dec-id] has been superseded by [dec-id-new]. Review before proceeding.` |
| **Alert surface** | Modal-level alert if any pending approval request package cited the superseded decision. Otherwise in-app notification. |
| **Lower surface** | No change required. |
| **LLM consequence** | Must not continue producing outputs based on the superseded decision without surfacing an Uncertainty Notice. Must treat prior recommendations that referenced the superseded decision as potentially invalid until the operator acknowledges. |
| **Blocking posture** | Blocks Class B and C gates until the operator has acknowledged the supersession via the `[Review Change]` control. |
| **Sequencing priority** | Level 2 (blocking). |
| **Owning doc** | `desktop-state-and-context-model.md` § Decision Continuity Context — Change notifications |

---

### EVENT-03 — Governing Decision Invalidated

**Trigger:** An active governing decision is invalidated (not superseded by a specific replacement — voided).

| Dimension | Specification |
|---|---|
| **Affected categories** | DECISIONS |
| **Invalidation requirement** | Decision context invalid immediately. All outputs citing the voided decision are stale. No replacement decision exists to substitute. |
| **Refresh requirement** | Reload active decision set. Voided decision removed entirely. |
| **Topbar** | No required change. |
| **Left nav** | No required change. |
| **Context strip** | Updates immediately. Voided decision removed. |
| **Interaction panel** | All rendered output cards that cited the voided decision receive: `⚠ DECISION INVALIDATED — [dec-id] is no longer active. Outputs citing it require re-evaluation.` |
| **Center surfaces** | Inline banner on any open surface that referenced the voided decision. |
| **Alert surface** | In-app notification. Modal if an active approval request package cited the voided decision. |
| **Lower surface** | No change required. |
| **LLM consequence** | Same as EVENT-02. Must surface Uncertainty Notice for any output that depended on the voided decision. Must not proceed toward Class B or C outputs until operator acknowledges. |
| **Blocking posture** | Blocks Class B and C gates until acknowledgment. |
| **Sequencing priority** | Level 2 (blocking). |
| **Owning doc** | `desktop-state-and-context-model.md` § Decision Continuity Context |

---

### EVENT-04 — Decision Conflict Detected

**Trigger:** Two or more loaded governing decisions are detected as conflicting on a material dimension.

| Dimension | Specification |
|---|---|
| **Affected categories** | DECISIONS, INTEGRITY |
| **Invalidation requirement** | No category is fully invalidated, but decision context is in conflict state. Conflict must be surfaced before governance-sensitive outputs proceed. |
| **Refresh requirement** | No reload required. Conflict state is resolved by operator action, not by reload. |
| **Topbar** | Session integrity indicator updates to show unresolved conflict. |
| **Left nav** | No required change. |
| **Context strip** | Conflict warning shown inline in decision context strip: `⚠ DECISION CONFLICT — [dec-id] and [dec-id-2] conflict on [dimension]. Resolve before approval-sensitive outputs.` |
| **Interaction panel** | No automatic marking of prior outputs unless a subsequent output is produced that navigates around the conflict rather than surfacing it. |
| **Center surfaces** | No automatic change. Operator may open decision detail to resolve. |
| **Alert surface** | In-app notification. |
| **Lower surface** | No change required. |
| **LLM consequence** | Must surface the conflict explicitly if producing any output that touches the conflicting dimension. Must not navigate around the conflict in recommendation framing. Must not produce an Approval Request Package on the conflicted dimension until the operator has acknowledged or resolved the conflict. |
| **Blocking posture** | Does not block Class A. Blocks Class B and C on the conflicted dimension until the operator acknowledges or resolves. |
| **Sequencing priority** | Level 2 (blocking for affected gates). |
| **Owning doc** | `desktop-state-and-context-model.md` § Decision Continuity Context — Conflict detection |

---

### EVENT-05 — Approval Written (Class B or C action completed)

**Trigger:** A persisted approval event is written — a Class B or C action is approved and recorded.

| Dimension | Specification |
|---|---|
| **Affected categories** | STAGE, INTEGRITY, DECISIONS (if the approval changes governing context) |
| **Invalidation requirement** | Workflow stage context is invalid immediately after the write. Prior stage context must not be used for any further gate evaluation. |
| **Refresh requirement** | Reload workflow stage context from governed records. Session integrity state re-evaluated to remove the resolved approval from pending items. |
| **Topbar** | Status/stage indicator updates immediately to reflect new stage. |
| **Left nav** | Refreshes to reflect new item state for the approved record. |
| **Context strip** | Updates immediately — stage, next gate, and blocking conditions reflect the post-approval state. |
| **Interaction panel** | No automatic marking unless prior outputs referenced the pre-approval state as still pending. |
| **Center surfaces** | Center detail surface for the approved record refreshes. Approval confirmation shown. |
| **Alert surface** | Confirmation notification. |
| **Lower surface** | No change required unless orchestration was tracking this approval. |
| **LLM consequence** | Must not reference the pre-approval state as current in any subsequent output. If the approval changes governing decisions or workflow stage, must treat the new state as loaded context for all further outputs. |
| **Blocking posture** | Non-blocking (approval already completed). Stage context must be refreshed before any subsequent gate is presented. |
| **Sequencing priority** | Level 3 (non-blocking refresh), but stage reload must complete before next gate is shown. |
| **Owning doc** | `desktop-state-and-context-model.md` § Context Invalidation Events; `desktop-surface-architecture.md` § Surface Synchronization |

---

### EVENT-06 — Prior Approval Superseded or Invalidated

**Trigger:** A prior approval event is rendered invalid — either superseded by a newer approval, voided by a decision change, or invalidated by changed basis conditions.

| Dimension | Specification |
|---|---|
| **Affected categories** | STAGE, INTEGRITY |
| **Invalidation requirement** | The workflow state that depended on the invalidated approval is stale. Any dependent gate that has not yet been passed must re-evaluate. |
| **Refresh requirement** | Reload workflow stage context. Re-evaluate session integrity state to surface the invalidated approval as an unresolved item. |
| **Topbar** | Session integrity indicator updates to show unresolved item. Stage indicator reflects stale or blocked state if the approved transition is now invalidated. |
| **Left nav** | Item in the navigation tree that was showing post-approval state reverts to blocked or pending state. |
| **Context strip** | Stage context shows: `⚠ PRIOR APPROVAL INVALIDATED — workflow stage context may have changed. Reload before proceeding.` |
| **Interaction panel** | Any rendered output cards that were produced assuming the prior approval was valid receive a staleness marker: `⚠ BASIS CHANGED — prior approval has been invalidated. Re-evaluate this output.` |
| **Center surfaces** | If the center surface for the affected record is open, inline banner: `Prior approval for [record] has been invalidated. Review required.` |
| **Alert surface** | Modal-level alert — approval invalidation is a governance-significant event. |
| **Lower surface** | No change required. |
| **LLM consequence** | Must not reference the invalidated approval as a completed gate. Must surface an Uncertainty Notice if asked to produce any output that depended on the approval. Must not proceed toward any follow-on gate that required the now-invalidated approval as a prerequisite. |
| **Blocking posture** | Blocks any gate that required the invalidated approval as a prerequisite. Blocks Class B and C outputs in the affected workflow scope until the operator acknowledges. |
| **Sequencing priority** | Level 2 (blocking). |
| **Owning doc** | `desktop-state-and-context-model.md` § Session Integrity State |

---

### EVENT-07 — Evidence Record Loaded

**Trigger:** The operator loads evidence records into the session basis.

| Dimension | Specification |
|---|---|
| **Affected categories** | EVIDENCE |
| **Invalidation requirement** | N/A — this is a load event, not an invalidation. |
| **Refresh requirement** | Evidence context strip updates to show newly loaded records with freshness and trust posture. |
| **Topbar** | No change required. |
| **Left nav** | No change required. |
| **Context strip** | Evidence section updates immediately to show loaded records: identifier, source, capture timestamp, trust posture, freshness marker. |
| **Interaction panel** | No automatic change. The LLM will see the newly loaded evidence on the next turn. |
| **Center surfaces** | No change required. |
| **Alert surface** | No change required. |
| **Lower surface** | No change required. |
| **LLM consequence** | May reference newly loaded evidence on the next turn, with required ownership attribution if evidence is from VEDA. Must not treat evidence as canonical state. Must include freshness and trust posture in any output that cites the evidence. |
| **Blocking posture** | Non-blocking. |
| **Sequencing priority** | Level 4 (informational). |
| **Owning doc** | `desktop-state-and-context-model.md` § Evidence Basis and Freshness |

---

### EVENT-08 — Evidence Record Becomes Stale

**Trigger:** A loaded evidence record exceeds its validity window, or newer contradicting evidence is loaded.

| Dimension | Specification |
|---|---|
| **Affected categories** | EVIDENCE |
| **Invalidation requirement** | The affected evidence record is marked stale. It remains visible but must not be cited as current. |
| **Refresh requirement** | No automatic reload — the operator must initiate a refresh. The staleness marker persists until refresh completes. |
| **Topbar** | No change required. |
| **Left nav** | No change required. |
| **Context strip** | Affected record shows: `⚠ STALE — [age/reason]`. Freshness marker updates. |
| **Interaction panel** | All rendered output cards that cited the now-stale evidence receive: `⚠ EVIDENCE STALE — [obs-id] is now stale. This output's evidence basis may not reflect current conditions.` |
| **Center surfaces** | If the center surface showing the affected record is open, inline banner. |
| **Alert surface** | In-app notification if the operator has active outputs or pending gates that depend on the stale evidence. |
| **Lower surface** | No change required. |
| **LLM consequence** | Must not cite the stale record as current in any subsequent output. Must include an Uncertainty Notice in any output that would depend on the stale record. Must treat the evidence as unavailable for Class C gate support until refreshed. |
| **Blocking posture** | Does not block Class A. Blocks Class C gates that require evidence currency. Does not automatically block Class B unless doctrine for the specific action requires current evidence. |
| **Sequencing priority** | Level 3 (non-blocking refresh). |
| **Owning doc** | `desktop-state-and-context-model.md` § Evidence Basis and Freshness — Staleness markers |

---

### EVENT-09 — Evidence Refreshed

**Trigger:** The operator initiates and completes an evidence refresh, loading current records to replace stale ones.

| Dimension | Specification |
|---|---|
| **Affected categories** | EVIDENCE |
| **Invalidation requirement** | The prior stale evidence records are replaced. Staleness marker removed for records that are now current. |
| **Refresh requirement** | Evidence context strip updates to reflect refreshed records with new capture timestamps and freshness posture. |
| **Topbar** | No change required. |
| **Left nav** | No change required. |
| **Context strip** | Affected records updated: staleness marker removed, new capture timestamp shown, trust posture confirmed. |
| **Interaction panel** | Prior output cards that carried `⚠ EVIDENCE STALE` markers receive an updated annotation: `Evidence basis refreshed [timestamp]. Re-evaluate if needed.` Prior output cards are not automatically re-validated — the operator must re-request outputs if they want fresh versions. |
| **Center surfaces** | Staleness banners on affected center surfaces dismissed. |
| **Alert surface** | Confirmation notification. |
| **Lower surface** | No change required. |
| **LLM consequence** | May now cite the refreshed evidence as current on the next turn, with required freshness and ownership attribution. Prior outputs based on stale evidence remain stale — refresh of evidence does not retroactively validate them. |
| **Blocking posture** | Removes the evidence-staleness block on Class C gates for the refreshed records. |
| **Sequencing priority** | Level 3 (non-blocking). |
| **Owning doc** | `desktop-state-and-context-model.md` § Evidence Basis and Freshness |

---

### EVENT-10 — Session Token Expiry or Runtime Scope Breakage

**Trigger:** The session token expires mid-session, or the runtime/sidecar connection is lost.

| Dimension | Specification |
|---|---|
| **Affected categories** | ALL nine categories invalid immediately. |
| **Invalidation requirement** | All context categories are invalid. No category may be carried forward from prior session in-memory state. |
| **Refresh requirement** | Full re-initialization required. All context categories must be reloaded fresh from governed records on re-init. Prior session cache is not acceptable as a substitute. |
| **Topbar** | Immediate: `◈ [project] ⚠ SESSION ERROR — runtime connection lost`. All gate and action controls disabled. |
| **Left nav** | No navigation change, but all action affordances disabled. |
| **Context strip** | Shows session error posture. All context categories show `[unavailable — session error]`. |
| **Interaction panel** | Input disabled. Current interaction shows: `Session interrupted. Re-initialize to continue.` |
| **Center surfaces** | All approval gate widgets and mutation actions disabled. Read-only posture maintained. |
| **Alert surface** | Modal: `Session Error — Runtime connection lost. Re-initialize before continuing.` with `[Re-initialize Session]` control. |
| **Lower surface** | Shows runtime error state if active. |
| **LLM consequence** | Must not produce governance-sensitive outputs while session is in error state. If a turn was in progress at the moment of expiry, the output must be marked incomplete and not treated as a valid output. |
| **Blocking posture** | Blocks all Class B and C actions. Blocks all LLM outputs beyond acknowledgment of the error state. |
| **Sequencing priority** | Level 1 (supersedes all other in-flight events). |
| **Owning doc** | `desktop-state-and-context-model.md` § Session Integrity State — Token and scope integrity |

---

### EVENT-11 — Current System Changed

**Trigger:** The operator explicitly switches the current system (Project V → VEDA → V Forge or any combination).

| Dimension | Specification |
|---|---|
| **Affected categories** | SYSTEM, STAGE, TOOLSURFACE, DECISIONS (scope changes), EVIDENCE (scope changes) |
| **Invalidation requirement** | All system-posture-dependent context is invalid for the prior system. Stage context, tool surface, and applicable action classes must reload for the new current system. |
| **Refresh requirement** | Reload: current system designation, workflow stage for the new system, tool-surface posture for the new system, applicable governing decisions for the new system scope. |
| **Topbar** | Immediate update: system indicator changes to new current system. |
| **Left nav** | Navigation tree updates to show content appropriate for the new current system. |
| **Context strip** | Full context strip refresh: new system, new stage, new decision context, new tool surface posture. |
| **Interaction panel** | Prior outputs that were produced under the prior system posture receive a system-change marker: `⚠ SYSTEM CHANGED — this output was produced under [prior system] posture. Review before applying in [new system] context.` |
| **Center surfaces** | Any open center surface for a record belonging to the prior system remains visible but is labeled with its system ownership. No automatic close. |
| **Alert surface** | In-app notification: `Current system changed to [new system]. Context has been refreshed.` |
| **Lower surface** | Orchestration and trace surfaces update to reflect new system posture. |
| **LLM consequence** | Must immediately operate under the new current system's action class table and governing posture. Must not apply the prior system's rules to outputs produced after the switch. Must treat prior outputs as belonging to the prior system context. |
| **Blocking posture** | Non-blocking for Class A. Context reload must complete before any Class B or C gate is presented under the new system. |
| **Sequencing priority** | Level 2 (blocking until reload complete). |
| **Owning doc** | `desktop-state-and-context-model.md` § Current System vs Referenced Systems |

---

### EVENT-12 — Delegated Task Completed (with admitted findings)

**Trigger:** A delegated worker task completes and its findings are admitted to the parent session basis.

| Dimension | Specification |
|---|---|
| **Affected categories** | ORCH, CONTINUITY |
| **Invalidation requirement** | Prior orchestration state showing the task as running or pending is now stale. Continuity artifact state updates to include admitted findings. |
| **Refresh requirement** | Orchestration state reloads to reflect terminal task state. Continuity artifact state updates. The findings are non-canonical and must be labeled as such. |
| **Topbar** | Attention badge updates if the admitted findings require operator review. |
| **Left nav** | No change required. |
| **Context strip** | Orchestration summary updates: task shown as `completed`. Continuity section updates to show admitted findings as non-canonical artifact. |
| **Interaction panel** | If findings are admitted to the session basis, the LLM may reference them on the next turn with required non-canonical attribution. A `DELEGATED FINDING ADMITTED` notice appears in the panel. |
| **Center surfaces** | No automatic change. Operator may open finding detail in center surface. |
| **Alert surface** | In-app notification if review is required. |
| **Lower surface** | Orchestration surface updates to show completed task with terminal state. |
| **LLM consequence** | May reference admitted findings on subsequent turns, but must label them as non-canonical delegated findings — not as canonical system state, not as governing decisions, not as evidence records. |
| **Blocking posture** | Non-blocking unless findings contain a return trigger (see EVENT-16). |
| **Sequencing priority** | Level 3 (non-blocking refresh). |
| **Owning doc** | `desktop-state-and-context-model.md` § Orchestration State; `desktop-task-lifecycle-implementation-design.md` § Refresh and Synchronization |

---

### EVENT-13 — Delegated Task Failed or Cancelled

**Trigger:** A delegated worker task fails or is cancelled before completion.

| Dimension | Specification |
|---|---|
| **Affected categories** | ORCH |
| **Invalidation requirement** | Prior orchestration state is stale. Any session outputs that assumed the task would complete successfully are potentially affected. |
| **Refresh requirement** | Orchestration state updates to reflect failed/cancelled terminal state. No findings are admitted. |
| **Topbar** | Attention badge updates if the failure affects operator workflow. |
| **Left nav** | No change required. |
| **Context strip** | Orchestration summary updates: task shown as `failed` or `cancelled`. |
| **Interaction panel** | If any prior outputs in the panel were predicated on the task completing, they receive: `⚠ DELEGATED TASK [failed/cancelled] — outputs that depended on this task's completion may be incomplete.` |
| **Center surfaces** | No automatic change. |
| **Alert surface** | In-app notification. Modal if the failure blocks a required workflow step. |
| **Lower surface** | Orchestration surface updates with failure or cancellation state and any failure reason surfaced. |
| **LLM consequence** | Must not treat the failed/cancelled task as having produced findings. Must surface an Uncertainty Notice if asked to produce outputs that depended on the task's expected output. |
| **Blocking posture** | Non-blocking for other tasks. May block specific workflow gates if the failed task was a required prerequisite. |
| **Sequencing priority** | Level 3 (non-blocking refresh). |
| **Owning doc** | `desktop-task-lifecycle-implementation-design.md` § Refresh and Synchronization |

---

### EVENT-14 — Meaningful Compaction Event

**Trigger:** A compaction cycle completes, changing the active runtime session basis.

| Dimension | Specification |
|---|---|
| **Affected categories** | CONTINUITY, TOOLSURFACE, potentially all categories (post-compaction per-category validation required) |
| **Invalidation requirement** | All context categories must be re-validated per-category after compaction. A single boolean `session_valid = true` is not acceptable. |
| **Refresh requirement** | Post-compaction per-category validation runs for all required categories. Any category that is stale-refresh-required or missing-refresh-required must be refreshed before the next normal turn. Protected context must be confirmed intact. |
| **Topbar** | Compaction notice shown: `Session compacted. Context basis updated.` |
| **Left nav** | No change required. |
| **Context strip** | All context categories re-render post-validation. Any category showing `stale-refresh-required` or `missing-refresh-required` is shown with explicit markers. |
| **Interaction panel** | Compaction boundary marker shown: `COMPACTION BOUNDARY — context basis was refreshed. Outputs produced before this boundary may reflect a different session basis.` Prior outputs above the boundary are not deleted but are visually separated from post-compaction outputs. |
| **Center surfaces** | No automatic change. |
| **Alert surface** | In-app notification. Modal if any category is `invalid-blocking` post-compaction. |
| **Lower surface** | Compaction event logged in trace surface. |
| **LLM consequence** | Must not carry forward claims from pre-compaction turns as though they are still in active context. Must acknowledge the compaction boundary if asked about prior turn content. Must use only the post-compaction validated context as its current basis. |
| **Blocking posture** | Any `invalid-blocking` category blocks all Class B and C actions and LLM governance-sensitive outputs until resolved. `stale-refresh-required` categories must be refreshed before gates are presented. |
| **Sequencing priority** | Level 2 (blocking) if any category is `invalid-blocking`. Level 3 (non-blocking) if all categories are valid or stale-refresh-required. |
| **Owning doc** | `desktop-compaction-implementation-design.md` § Post-Compaction Per-Category Validation |

---

### EVENT-15 — Transcript-Backed Continuity Change

**Trigger:** A transcript-derived continuity artifact is admitted, updated, or expires from the active session basis.

| Dimension | Specification |
|---|---|
| **Affected categories** | CONTINUITY |
| **Invalidation requirement** | The prior continuity artifact state for the affected artifact is stale. |
| **Refresh requirement** | Continuity artifact section in context strip updates to reflect current admission status. Freshness and aging markers updated. |
| **Topbar** | No change required. |
| **Left nav** | No change required. |
| **Context strip** | Continuity section updates to show current admitted artifacts with freshness markers. Aged or expired artifacts shown with explicit marker or removed. |
| **Interaction panel** | If an admitted continuity artifact expires or is removed during an active session, prior outputs that cited it receive: `⚠ CONTINUITY ARTIFACT CHANGED — [artifact type] referenced in this output is no longer in the active session basis.` |
| **Center surfaces** | No automatic change. |
| **Alert surface** | In-app notification if an active artifact expires. |
| **Lower surface** | No change required. |
| **LLM consequence** | Must not reference a continuity artifact that is no longer in the active session basis. Must not treat transcript-derived continuity as canonical state in any output. If a relied-upon artifact expires mid-session, must surface an Uncertainty Notice for any subsequent output that would have depended on it. |
| **Blocking posture** | Non-blocking for Class A. Does not block gates unless the expired artifact was serving as the basis for an active approval request package, in which case the package must be re-evaluated. |
| **Sequencing priority** | Level 3 (non-blocking refresh). |
| **Owning doc** | `desktop-state-and-context-model.md` § Continuity Artifact State; `desktop-memory-and-continuity-model.md` |

---

### EVENT-16 — Return Trigger Arrives

**Trigger:** A return trigger is routed from V Forge to Project V, signaling that a V Forge finding may warrant planning attention.

**Return trigger lifecycle states:** `arrived` → `acknowledged` → `routed` | `dismissed`

| Dimension | Specification |
|---|---|
| **Affected categories** | INTEGRITY |
| **Invalidation requirement** | Session integrity state updates to include the unresolved return trigger. No other category is automatically invalidated by trigger arrival alone. |
| **Refresh requirement** | Session integrity state must reflect the trigger as `arrived` and unresolved. |
| **Topbar** | Attention badge updates immediately: `⚡ Return trigger — unreviewed`. |
| **Left nav** | V Forge navigation section shows the trigger prominently. |
| **Context strip** | Session integrity section shows: `⚡ RETURN TRIGGER (arrived) — [trigger summary]. Route or dismiss.` |
| **Interaction panel** | In-app notification fires. If the operator is mid-session, a non-blocking banner appears: `Return trigger received from V Forge. Review when ready.` |
| **Center surfaces** | Operator can open the return trigger detail in a center surface to review the finding before routing. |
| **Alert surface** | In-app notification. Not a modal unless the trigger contains a blocking finding that affects current workflow stage. |
| **Lower surface** | Logged in trace surface if active. |
| **LLM consequence** | The return trigger is a finding, not an automatic replanning event. The LLM must not treat trigger arrival as authorization to replan. If asked about the trigger, must describe it as a finding for operator evaluation and routing, not as a planning directive. |
| **Blocking posture** | Non-blocking on arrival. Becomes a blocking integrity item if left unresolved past the session integrity threshold defined in governance doctrine. |
| **Sequencing priority** | Level 4 (informational on arrival). Level 2 (blocking) if unresolved and the operator attempts a Class C gate. |
| **State transition — acknowledged** | Operator opens the trigger detail. State changes to `acknowledged`. Attention badge remains. No other surface change. |
| **State transition — routed** | Operator selects `Route return trigger`. Trigger is routed to the Project V planning surface through the governed return-to-planning interface. State changes to `routed`. Attention badge clears. Session integrity item resolved. STAGE and DECISIONS may be affected depending on the routed finding's content — those changes follow EVENT-01 through EVENT-03 as applicable. |
| **State transition — dismissed** | Operator selects `Dismiss return trigger`. State changes to `dismissed`. Dismissal is logged as a governance-relevant fact. Attention badge clears. Session integrity item resolved. |
| **Owning doc** | `desktop-state-and-context-model.md` § Session Integrity State; `desktop-surface-architecture.md` § Surface Synchronization; `desktop-human-llm-interaction-model.md` § Execution Report |

---

### EVENT-17 — Workflow Stage Change

**Trigger:** The workflow stage for the active work scope transitions — either as the result of an approval (see EVENT-05), a gate passage, a system-generated stage update, or an operator-initiated stage change.

| Dimension | Specification |
|---|---|
| **Affected categories** | STAGE, INTEGRITY (blocking conditions update) |
| **Invalidation requirement** | Prior stage context is stale. Blocking conditions, next-gate requirements, and pending approval requirements must all be re-evaluated for the new stage. |
| **Refresh requirement** | Reload workflow stage context from governed records: current stage, next gate, blocking conditions, pending approvals. |
| **Topbar** | Stage indicator updates immediately. |
| **Left nav** | Navigation tree item for the affected work scope updates to reflect new stage. |
| **Context strip** | Stage section updates: new stage name, new next gate, updated blocking conditions. |
| **Interaction panel** | If the stage change affects what actions are available, a notice appears: `Workflow stage updated to [stage]. Gate and action posture has changed.` Prior output cards that referenced the old stage as current receive a staleness marker. |
| **Center surfaces** | Any open center surface for the affected work scope refreshes. If new blocking conditions apply, they are shown prominently. |
| **Alert surface** | In-app notification if the stage change creates new blocking conditions or gates. |
| **Lower surface** | No change required. |
| **LLM consequence** | Must operate under the new stage's action posture from the next turn forward. Must not reference the prior stage's gating rules as still applicable. Must surface an Uncertainty Notice if asked to produce approval-sensitive outputs before stage context is confirmed reloaded. |
| **Blocking posture** | Stage context reload must complete before any gate or approval surface is presented. |
| **Sequencing priority** | Level 2 (blocking until reload). |
| **Owning doc** | `desktop-state-and-context-model.md` § Workflow Stage Context |

---

### EVENT-18 — Local Support-State Divergence Detected

**Trigger:** The local SQLite support-state layer shows state that differs from the backend canonical state — detected at session start, during reconciliation, or on a manual refresh.

| Dimension | Specification |
|---|---|
| **Affected categories** | INTEGRITY, and whichever categories are affected by the diverged state |
| **Invalidation requirement** | The diverged local state must not be treated as canonical. Any context category whose current value came from local state rather than a fresh backend load is suspect. |
| **Refresh requirement** | Backend canonical state must be used to resolve the divergence. Local state is updated to reflect backend truth, not the reverse. |
| **Topbar** | Session integrity indicator updates: `⚠ LOCAL STATE DIVERGENCE — context may not reflect backend state.` |
| **Left nav** | No change required. |
| **Context strip** | Affected categories shown with: `⚠ LOCAL DIVERGENCE — [category] loaded from local state. Verify against backend.` |
| **Interaction panel** | If any rendered output cards were produced while local state was authoritative and backend was unavailable, they receive: `⚠ LOCAL STATE WARNING — this output was produced while backend sync was unavailable. Verify before acting.` |
| **Center surfaces** | If open center surfaces show data that may reflect diverged local state, inline banner. |
| **Alert surface** | In-app notification. Modal if divergence affects a category required for an active Class B or C gate. |
| **Lower surface** | No change required. |
| **LLM consequence** | Must not treat outputs produced during a local-state-divergence window as having been produced against canonical context. Must surface an Uncertainty Notice if asked to produce governance-sensitive outputs while divergence is unresolved. |
| **Blocking posture** | Blocks Class B and C gates if the affected categories are required for those gates and divergence is unresolved. |
| **Sequencing priority** | Level 2 (blocking for affected gates). |
| **Owning doc** | `desktop-state-and-context-model.md` § Session Integrity State; `local-first-architecture.md` |

---

## Cross-Event Rules

### Output Card Staleness Marking

Any rendered LLM output card in the interaction panel that was produced when its basis context was subsequently changed by an event in this matrix must receive a staleness marker before the next turn begins. This includes outputs produced in the same session before a blocking event was acknowledged.

Output cards are never deleted by context events. They are marked. The operator's record of what was produced and when is preserved. Only the operator can dismiss or archive output cards.

### Concurrent Event Handling

When two or more events fire in the same session tick, apply the sequencing priority rules. If two events are at the same priority level, process them in the order they are listed in this matrix and layer their consequences. Do not collapse them into a single undifferentiated notification.

### LLM Turn Boundary Rule

A blocking event (Level 1 or 2) that fires while an LLM turn is in progress does not interrupt the turn mid-generation. The turn completes. The output is marked stale before it is rendered in the panel. The blocking posture takes effect before the next turn begins. The operator sees both the output and its staleness marker.

### Dismiss and Acknowledge Logging

Every operator action that dismisses or acknowledges an invalidation or integrity item must be logged as a governance-relevant fact with timestamp and operator identity. The log record is not optional and must be preserved in the session audit record.

---

## Usage

This document should be used:

- when implementing `refreshCoordinator` event handling and ordering
- when designing surface synchronization behavior for any new event type
- when evaluating whether a new doc, feature, or runtime behavior introduces a new invalidation event that needs to be added to this matrix
- when auditing whether a given event's consequences are fully propagated across all surfaces and to the LLM
- as the cross-reference anchor for trigger lists in all companion docs
- when writing hardening additions to `desktop-human-llm-interaction-model.md`, `desktop-surface-architecture.md`, or `desktop-state-and-context-model.md`

---

## Related Docs

- `desktop-state-and-context-model.md` — defines state categories, per-category validity rules, general staleness/blocking rules
- `desktop-surface-architecture.md` — defines surface roles and synchronization requirements
- `desktop-implementation-architecture.md` — defines `refreshCoordinator` and frontend service responsibilities
- `desktop-human-llm-interaction-model.md` — defines LLM output types and operator response options
- `desktop-compaction-implementation-design.md` — defines post-compaction per-category validation
- `desktop-task-lifecycle-implementation-design.md` — defines task event publication and refresh triggers
- `desktop-agent-orchestration-model.md` — defines orchestration authority limits
- `desktop-memory-and-continuity-model.md` — defines continuity artifact classes and memory posture
- `desktop-governance-and-gating-model.md` — defines approval classes and gate requirements
- `local-first-architecture.md` — defines local SQLite support-state and reconciliation posture
- `v-forge-to-project-v-return-to-planning-interface.md` — defines return trigger routing mechanics

---
