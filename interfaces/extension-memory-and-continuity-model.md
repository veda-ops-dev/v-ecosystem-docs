# Extension Memory and Continuity Model

## Status
Superseded by `desktop-memory-and-continuity-model.md`

This document reflects the legacy VS Code extension host model.
The Tauri 2 desktop application defined in ADR-011 is now the primary operator host.
Use `desktop-memory-and-continuity-model.md` for active doctrine.

## Purpose

This document defines how memory, continuity, transcripts, and compaction work inside the V Ecosystem VS Code extension.

It exists to answer:

```text
What kinds of memory and continuity artifacts may exist in the extension, what must remain protected from compaction, how are long-running sessions preserved without creating fake authority, and how does the extension remain powerful across long interactions without letting memory or transcript artifacts replace canonical system state?
```

This is a Tier 1 ecosystem authority document for the extension/runtime layer.

---

## Scope

This document governs:

- the distinction between canonical state and runtime continuity artifacts
- the allowed memory classes inside the extension
- transcript artifact posture
- protected context categories
- compaction posture and compact-boundary behavior
- admission posture for continuity artifacts
- continuity visibility requirements
- freshness, aging, and supersedence rules for memory artifacts
- source attribution requirements for memory and delegated findings
- operator controls for reviewing and clearing continuity artifacts
- anti-drift rules that prevent memory from becoming fake authority

This document assumes the active binding of:
- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-state-and-context-model.md`
- `extension-agent-orchestration-model.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/report-structure-and-required-fields.md`

---

## Out of Scope

This document does not define:

- exact backend storage engines or file formats
- exact summarization prompts or LLM compaction templates
- exact UI component design for memory or transcript surfaces
- exact system-init message content
- the full task-orchestration model for delegated work
- project-specific memory heuristics
- canonical system record retention rules

Those belong in implementation docs, tool-surface docs, or system-specific doctrine.

---

## System

- interfaces

---

## Core Rule

Memory and continuity features exist to preserve useful runtime context.
They do not create canonical authority.

The extension may preserve useful working context across turns, compaction events, and session resume flows.
It must not allow memory, transcripts, compaction products, or delegated findings to replace:

- decision records
- approval records
- evidence records
- canonical Project V state
- canonical VEDA state
- canonical V Forge state

If a continuity artifact begins to function like a system of record, the continuity model is wrong.

---

## Canonical State vs Continuity Artifact Rule

The extension must maintain a hard distinction between:

### Canonical state
Governed records owned by the proper system of record and loaded through admitted APIs and MCP surfaces.

Examples include:
- Project V decision records
- Project V readiness and audit records
- VEDA evidence and signal records
- V Forge execution records
- persisted approval events
- current workflow-state records

### Continuity artifacts
Runtime artifacts used to preserve operator usefulness and LLM continuity across time, compaction, and delegation.

Examples include:
- working memory entries
- durable memory entries
- transcript artifacts
- compact-boundary products
- worker findings retained for parent-session context
- runtime continuity summaries

Canonical state governs.
Continuity artifacts assist.
Assistance must never be confused with governance.

---

## Memory Classes

The extension may support the following memory classes.

### 1. Ephemeral Working Memory

Ephemeral working memory preserves useful session-local runtime understanding across turns and compaction events during the active session.

Examples include:
- current analytical focus
- operator-stated preferences relevant to the session
- working hypotheses or non-authoritative conclusions
- task progress notes
- current runtime reminders

Ephemeral working memory:
- is session-scoped
- is non-canonical
- must remain visible when active
- may be cleared without governance side effects

### 2. Session-Durable Memory

Session-durable memory persists beyond the immediate active turn window and may survive compaction or controlled session resume for the same session lineage.

Examples include:
- persisted analytical focus for the active session lineage
- durable worker findings retained for review during an ongoing effort
- operator preferences relevant to the active session lineage

Session-durable memory:
- remains non-canonical
- must carry age/freshness metadata
- must remain reviewable and clearable
- must not silently become cross-project or cross-session authority

### 3. Cross-Session Memory

Cross-session memory is the highest-risk memory class and is optional.

If admitted at all, it must be:
- explicitly scoped
- operator-visible at session start
- attributable to source and age
- dismissible or clearable
- blocked from bleeding across project scope or current-system boundaries

Cross-session memory must never be treated as decision continuity, approval continuity, or evidence continuity.

---

## Continuity Admission Rule

A continuity artifact is **admitted** only when the runtime deliberately allows it to participate in the active session basis.

Admission is not automatic just because an artifact exists.
Admission requires all of the following:
- the artifact fits an allowed memory class
- the artifact remains within active project scope
- the artifact remains within the active or explicitly referenced current-system posture
- the artifact carries source attribution and freshness state where relevant
- the artifact remains visibly non-canonical

Admission may be denied or withdrawn when:
- the artifact is stale enough to mislead the session
- the artifact conflicts with freshly loaded canonical state
- the operator clears or dismisses it
- current-system posture changes and the artifact no longer belongs in the active basis

---

## Transcript Artifact Posture

Transcript artifacts are persisted records of runtime interaction and delegated work used for audit, review, debugging, resume support, or operator recall.

Transcript artifacts may include:
- messages
- tool calls and results
- delegated task events
- compaction events
- interruption/cancellation events
- runtime continuity notes

Transcript artifacts are not:
- canonical decisions
- approval records
- evidence records
- systems of record

A transcript artifact may help a later reviewer understand what happened.
It must not be cited as a substitute for the governing record that should have been created elsewhere.

The mechanical persistence, metadata, labeling, retrieval, and recall posture for transcript artifacts are defined in `extension-transcript-persistence-design.md`.
That companion implements transcript handling without changing the non-authority rule defined here.

---

## Protected Context Rule

Certain categories of context must be protected from compaction loss because they are necessary for correct governed behavior.

Protected context includes, at minimum:
- current project scope
- current system posture
- current workflow-stage state relevant to the active work
- active approval and gating state
- loaded decision continuity context
- loaded evidence basis markers and freshness state
- session integrity state
- active runtime warnings that affect correctness

Protected context may be re-packed or re-presented.
It must not be silently dropped.

If compaction removes protected context, the runtime has violated continuity doctrine even if the session still appears usable.

The mechanical implementation design for preserving protected context, freezing protected context before lossy compaction, and validating protected-context survival after compaction is defined in `extension-compaction-implementation-design.md`.

---

## Compaction Rule

The extension may compact runtime context to preserve usability during long sessions.

Compaction is allowed only when it preserves:
- protected context
- clear operator visibility into what changed
- source attribution for retained continuity artifacts
- the distinction between continuity artifacts and canonical state

Compaction must not be treated as a magic summarization event that silently rewrites the session basis.

The mechanical trigger model, eligibility checks, flush integration point, compact-boundary construction, and post-compaction validation mechanics are defined in `extension-compaction-implementation-design.md`.

---

## Compaction Classes

The extension may implement different compaction classes.

### Micro-Compaction
Noise removal that strips redundant or low-value runtime material without changing the governing context basis.

Examples:
- duplicate tool output
- repetitive read traces
- redundant chatter not carrying continuity value

Micro-compaction is the safest compaction class.

### Working-Memory Extraction
Compaction that extracts bounded continuity artifacts from prior session interaction so useful understanding is preserved after raw conversational history is reduced.

Working-memory extraction must:
- remain non-authoritative
- preserve source attribution
- avoid decision-language and approval-language
- remain visible to the operator when active

### Full Conversational Compaction
A bounded replacement of prior narrative history with a compacted continuity product plus retained protected context.

This is the highest-risk compaction class and must be visibly marked with a compact boundary.

The implementation must map these doctrinal compaction classes into distinct mechanical execution paths rather than one generic compaction blob.

---

## Compaction Blocking Rule

Compaction must not occur at arbitrary runtime moments.

At minimum, compaction must be blocked when:
- an approval gate is actively in-flight
- protected context cannot be preserved faithfully
- current-system posture is being switched or re-established
- session integrity state is unresolved in a way that would make compaction misleading
- the runtime cannot clearly characterize what will be preserved and what will be dropped

When compaction is blocked, the runtime must prefer:
- delaying compaction
- asking the operator to review the situation
- entering a bounded degraded mode

It must not silently compact anyway and hope for the best.

The runtime implementation must perform an explicit eligibility check against these blocking rules before a lossy compaction cycle proceeds.

---

## Compaction Failure Posture

If the runtime cannot preserve all protected context, it must not proceed with full conversational compaction.

In that case, the runtime must:
- halt the compaction attempt
- surface the failure or degraded condition explicitly to the operator
- preserve the session in a review-required posture until the operator or runtime resolves the condition

The correct fallback is not to drop protected context and continue pretending continuity remains sound.

The implementation companion doc defines the mechanical halt, refresh, and per-category validation posture that should follow a failed or incomplete compaction cycle.

---

## Compact Boundary Rule

When full conversational compaction occurs, the runtime must create a visible compact boundary.

The compact boundary exists so the operator and the LLM can both understand:
- that compaction occurred
- what continuity artifacts were preserved
- what protected context was retained
- what older narrative history is no longer present in the active model context

A compact boundary improves continuity transparency.
It does not convert compaction output into canonical state.

The compact-boundary artifact is mechanically defined in `extension-compaction-implementation-design.md`, but its non-canonical posture is governed here.

---

## Memory Source Attribution Rule

All non-trivial memory and continuity artifacts must carry source attribution.

At minimum, attribution should identify:
- how the artifact was created
- when it was created
- whether it came from operator interaction, delegated work, compaction, or resume flow
- what session lineage it belongs to

If a continuity artifact came from delegated work, the delegated source must be visible.
The parent runtime must not flatten worker-originated context into anonymous truth.

---

## Freshness, Aging, and Supersedence Rule

Continuity artifacts must carry age or freshness state where relevant.

Older memory and transcript-derived continuity should not be treated as equally current with freshly loaded governed state.

The runtime must support the idea that a continuity artifact may be:
- current
- aging
- stale
- superseded
- cleared

When canonical state conflicts with a continuity artifact, canonical state wins.

When a continuity artifact is stale enough to risk misleading the LLM or operator, that staleness must be surfaced rather than hidden.

---

## Non-Authority Vocabulary Rule

Memory and transcript-derived artifacts must not use language that implies governance authority unless the authority came from canonical records loaded from the proper system.

Continuity artifacts should avoid phrases like:
- approved
- decided
- authorized
- canonically determined

unless those statements are explicitly quoting or referencing the real governing record.

Preferred posture is observational language such as:
- discussed
- noted
- analyzed
- flagged
- expressed interest in
- working focus
- provisional conclusion

The language used for continuity artifacts must help prevent authority confusion, not create it.

---

## Operator Visibility and Control Rule

The operator must be able to review meaningful continuity artifacts.

Where memory, compaction, transcript, or retained delegated findings materially affect the session, the operator must be able to determine:
- what continuity artifacts are currently active
- what was preserved through compaction
- what came from delegated work
- what is stale or aging
- what can be cleared or dismissed

The operator must be able to clear or dismiss non-canonical continuity artifacts without creating governance side effects.

Hidden continuity is not acceptable.
A memory system the operator cannot inspect is not compatible with this ecosystem.

---

## Current-System Switch Rule

When the operator explicitly changes the current system, the runtime must not silently carry forward all continuity artifacts as though nothing changed.

On current-system switch:
- continuity artifacts from the prior current-system posture must be re-evaluated for admission
- artifacts that remain relevant may be retained only with clear source-system labeling
- artifacts that no longer belong in the active basis must be withdrawn from active participation
- the runtime must not present prior-system continuity artifacts as active local truth for the new current system

Switching current system does not require pretending prior continuity never existed.
It does require preventing cross-system continuity bleed.

---

## Resume Rule

If the extension supports session resume or controlled continuity across re-entry, the resumed session must make continuity status explicit.

A resumed session must not pretend that runtime continuity artifacts are identical to freshly loaded canonical state.

On resume, the operator should be able to see:
- what state was freshly loaded from governed systems
- what continuity artifacts were brought forward
- what memory or transcript-derived items may need review due to age or staleness

Resume is a continuity convenience, not a state-authority shortcut.

---

## Delegated Findings and Worker Memory Rule

Specialist workers may produce delegated findings and worker-originated continuity artifacts that help the parent session avoid redundant work.

These worker-originated artifacts must:
- remain attributable to the worker/task source
- remain non-canonical
- be reviewable by the parent runtime and operator
- avoid decision-language and approval-language

Delegated findings may improve runtime usefulness.
They must not become automatic truth just because they came from a specialist.

---

## Anti-Drift Rules

### 1. No fake authority rule
Memory, transcripts, compaction products, and worker findings must not function as substitute governance.

### 2. No silent protected-context loss rule
Protected context must not disappear invisibly during compaction.

### 3. No hidden memory rule
Meaningful active continuity artifacts must remain operator-visible.

### 4. No cross-scope bleed rule
Continuity artifacts must not leak across project scope, current-system posture, or unrelated session lineages.

### 5. No stale-memory confidence rule
The runtime must not present stale memory with the same confidence posture as current canonical state.

### 6. No transcript-as-record rule
Transcript artifacts must not become the real place where decisions or approvals are treated as settled.

---

## Relationship to Other Extension Docs

This doc defines memory and continuity posture.

It relies on:
- `extension-state-and-context-model.md` for visibility expectations
- `extension-governance-and-gating-model.md` for approval boundaries
- `extension-agent-orchestration-model.md` for delegated-work posture
- `extension-system-init-and-tool-surface-model.md` for how continuity is loaded at session start
- `extension-compaction-implementation-design.md` for the mechanical compaction lifecycle that enforces the doctrine defined here
- `extension-transcript-persistence-design.md` for the mechanical transcript persistence, labeling, and recall posture that stays subordinate to the continuity rules defined here

This doc must not be used to blur canonical state boundaries just because continuity makes the system feel smarter.

---

## Implementation Direction

Implementation should make continuity:
- explicit
- bounded
- inspectable
- clearable
- freshness-aware
- subordinate to governed records

The extension should become much better at surviving long-running sessions.
It must not become a memory-shaped shadow database.
