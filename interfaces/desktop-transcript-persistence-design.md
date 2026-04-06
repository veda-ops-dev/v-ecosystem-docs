# Desktop Transcript Persistence Design

## Purpose

This document defines the mechanical implementation design for transcript persistence in the V Ecosystem desktop runtime.

It exists to answer:

```text
How should the desktop application persist, label, review, and reuse transcript artifacts so operators gain audit and session-continuity value without allowing transcripts to become pseudo-governance, pseudo-evidence, or shadow canonical state?
```

This is a Tier 3 implementation companion document.
It is subordinate to the active authority in:

- `desktop-memory-and-continuity-model.md`
- `desktop-state-and-context-model.md`
- `desktop-agent-orchestration-model.md`
- `runtime-sidecar-and-nerve-model.md`
- `../governance/agent-operating-doctrine.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/report-structure-and-required-fields.md`

If this document conflicts with those docs, this document is wrong.

---

## Scope

This document governs:

- transcript persistence mechanics
- transcript event inclusion rules
- transcript metadata requirements
- transcript labeling and non-authority posture
- transcript review and retrieval posture
- transcript use in resume or recall flows
- delegated-work transcript inclusion
- transcript retention and visibility posture at runtime
- anti-drift constraints for transcript handling

---

## Out of Scope

This document does not define:

- canonical system record retention policy
- final UI component layout for transcript viewers
- full session-resume doctrine
- exact storage engine or serialization backend
- legal or compliance policy beyond current authority docs

Those belong in higher-authority or more specific operational docs.

---

## System

- interfaces

---

## Core Rule

Transcript persistence exists to support auditability, review, debugging, operator recall, and bounded continuity support.

Transcript artifacts do not create authority.
They do not replace canonical records.
They do not replace evidence records.
They do not replace decisions, approvals, or execution truth.

If a transcript begins functioning like the real place where the ecosystem actually decided something, the implementation is wrong.

---

## Relationship to Existing Authority

This document does not create new doctrine for continuity, approvals, or orchestration.
It operationalizes transcript persistence under the posture already defined elsewhere.

In particular, it assumes and must obey the active authority already defined for:

- transcript artifact non-authority posture
- continuity admission rules
- delegated findings posture
- operator visibility and reviewability
- fresh canonical loading before governance-sensitive action

This document defines how transcript artifacts are recorded and made available mechanically.

---

## Transcript Lifecycle Overview

Transcript persistence should be treated as a bounded runtime artifact lifecycle with the following stages:

1. **event capture**
2. **artifact assembly**
3. **metadata attachment**
4. **non-authority labeling**
5. **persistence**
6. **review / retrieval**
7. **bounded recall or resume support**

The transcript is an audit and continuity artifact, not a parallel record system.

---

## Event Capture

The runtime should capture transcript-worthy events as structured session events rather than relying on reconstruction from raw chat text alone.

### Minimum Event Categories

At minimum, transcript capture should support:

- operator messages
- LLM responses
- tool calls
- tool results
- delegated task lifecycle events
- compaction events
- interruption and cancellation events
- major refresh and invalidation events
- runtime warnings materially affecting the session

### Why This Matters

A transcript that only captures chat prose but not the runtime events that shaped the session is not a trustworthy audit artifact.

---

## Artifact Assembly

The runtime should assemble transcript artifacts as bounded chronological session records.

### Required Posture

The transcript should represent what happened in session order without pretending to be a canonical interpretation of what should have happened.

### Important Distinction

A transcript may preserve:

- what was said
- what was called
- what the runtime reported
- what the operator reviewed or dismissed

It must not silently promote those facts into governance conclusions.

---

## Transcript Metadata Requirements

Every persisted transcript artifact should carry enough metadata to remain attributable and non-authority-safe.

### Minimum Metadata

At minimum, a transcript artifact should carry:

- session identifier
- session lineage identifier
- project scope token or project identifier
- current-system posture at transcript creation
- creation timestamp
- most recent update timestamp
- whether delegated work participated
- whether compaction occurred in the session
- whether the transcript is complete, partial, interrupted, or recovered
- explicit non-authority classification

### Event-Level Metadata

Where relevant, individual transcript events should also preserve:

- timestamp
- event type
- actor or source
- delegated worker identifier, if applicable
- warning or error posture, if applicable

---

## Non-Authority Labeling

Every transcript artifact should be explicitly labeled as a non-canonical continuity and audit artifact.

### Required Labeling Posture

The transcript must be unmistakably classified as:

- not a decision record
- not an approval record
- not an evidence record
- not canonical Project V, VEDA, or V Forge state

### Why This Matters

This label is not decoration.
It is one of the mechanical barriers that prevents transcript history from becoming pseudo-governance.

---

## Persistence Mechanics

The runtime may persist transcripts incrementally or at bounded checkpoints.

### Acceptable Persistence Postures

Examples include:

- append-per-event
- append-per-turn
- bounded checkpoint writes
- flush-on-session-close plus interim safety writes

### Required Rule

Persistence strategy must not compromise reviewability or silently drop meaningful runtime events that would matter to later audit or resume support.

### Interrupted Sessions

If a session is interrupted, the runtime should preserve transcript state as partial or interrupted rather than pretending the transcript is complete.

---

## Review and Retrieval Posture

The operator should be able to review transcripts as audit artifacts without confusing them for authority artifacts.

### Minimum Retrieval Capabilities

At minimum, transcript retrieval should support:

- locating transcripts by session lineage
- locating transcripts by project scope
- locating transcripts by date and time
- identifying whether delegated work participated
- identifying whether compaction occurred

### Review Posture

Transcript review should preserve the transcript's non-authority classification visibly.
The operator should never be nudged into treating transcript review as equivalent to reviewing canonical records.

---

## Use in Recall and Resume Flows

Transcript artifacts may support bounded recall or controlled resume.

### Allowed Role

Transcript artifacts may help the runtime or operator understand:

- what happened previously
- what was discussed
- what warnings or unresolved conditions existed
- what delegated work had occurred

### Forbidden Role

Transcript artifacts must not be used as a substitute for:

- fresh canonical state loading
- decision continuity loading from governed records
- evidence loading from VEDA
- approval verification from the real approval path

### Resume Rule

If resume uses transcript artifacts, the resumed session must still reload canonical state fresh and visibly distinguish:

- fresh canonical loads
- carried-forward continuity artifacts
- transcript-derived recall material

### Matrix Deference for Transcript-Backed Continuity Changes

When transcript-derived continuity artifacts are admitted, updated, or expire from the active session basis, those changes constitute an event with desktop-wide consequences. The full per-surface behavior, LLM consequences, blocking posture, and sequencing for those events are defined in `desktop-invalidation-and-refresh-matrix.md` (EVENT-15 — Transcript-Backed Continuity Change). This section defines the recall and resume posture — what transcripts may and may not substitute for — not the downstream event consequences.

---

## Delegated Work in Transcripts

If delegated work participates in a session, the transcript should preserve that participation explicitly.

### Required Behavior

The transcript should not flatten delegated outputs into anonymous session truth.
It should preserve:

- worker or task identifier
- delegated role where relevant
- lifecycle state changes
- outputs or findings attributed to the delegated source

### Why This Matters

Worker outputs are already high-risk for authority confusion.
Transcript persistence must not make that worse by laundering source identity away.

---

## Relationship to Compaction

Meaningful compaction events should appear in the transcript artifact.

### Required Posture

The transcript should preserve that:

- compaction occurred
- what class of compaction occurred
- whether flush occurred
- whether warnings were raised
- whether a compact boundary was created

### Important Distinction

The transcript may record that compaction happened.
It must not reclassify compaction products as canonical state simply because they are now present in the transcript.

---

## Visibility at Runtime

Where transcript artifacts materially affect recall or resume posture, the operator should be able to tell that transcript-backed continuity is participating.

### Minimum Runtime Visibility

At minimum, the operator should be able to determine:

- that transcript artifacts exist for the current session lineage
- whether current recall is using transcript material
- whether the transcript is partial, interrupted, or complete
- whether delegated work appears in the transcript history

This does not require the transcript viewer to be always open.
It does require transcript participation to remain legible.

---

## Suggested Runtime Structure

A reasonable implementation split would separate the following concerns:

### 1. Session Event Capture Layer
Captures transcript-worthy runtime events in structured form.

### 2. Transcript Assembler
Builds ordered transcript artifacts from captured events.

### 3. Transcript Metadata Enricher
Adds session lineage, scope, delegated participation, compaction markers, and non-authority labeling.

### 4. Transcript Persistence Adapter
Writes transcript artifacts to the chosen backend or storage form.

### 5. Transcript Retrieval Layer
Supports bounded review and session-lineage lookup.

### 6. Recall / Resume Bridge
Allows transcript artifacts to participate in bounded recall flows without replacing fresh canonical loading.

This split is preferred over burying transcript persistence inside generic session storage because transcript handling has distinct anti-drift risks.

---

## Anti-Drift Constraints

Implementation must not drift into any of the following:

- treating transcript history as the real decision record
- using transcript recall instead of fresh canonical loading
- flattening delegated outputs into anonymous truth
- labeling transcript artifacts ambiguously so they look canonical
- dropping compaction or warning events from transcripts and leaving audit gaps
- presenting partial or interrupted transcripts as if they were complete
- turning transcript retrieval into a shadow governance workflow

---

## Usage

This document should be used:

- when implementing transcript persistence and retrieval
- when designing audit and review surfaces that expose transcript artifacts
- when building bounded recall or resume support
- when reviewing whether transcript handling is drifting into pseudo-governance
- when integrating delegated-work visibility into persisted session history

---

## Related Docs

- `desktop-memory-and-continuity-model.md`
- `desktop-state-and-context-model.md`
- `desktop-agent-orchestration-model.md`
- `runtime-sidecar-and-nerve-model.md`
- `desktop-invalidation-and-refresh-matrix.md` — canonical event-to-consequence mapping; EVENT-15 defines the full desktop consequences when transcript-backed continuity artifacts are admitted, updated, or expire
- `../governance/agent-operating-doctrine.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/report-structure-and-required-fields.md`
