# Local-First Architecture

## Purpose
Define the canonical local-first architecture for the Tauri 2 desktop host, including the relationship between canonical backend truth, local SQLite support state, and in-memory desktop application state.

## Scope
This doc governs:
- the local-first persistence model for the desktop operator application
- the role of canonical PostgreSQL-backed backend systems
- the role of local SQLite support storage
- the role of in-memory reactive desktop state
- local hydration, continuity, cache, and draft posture
- boundaries that prevent local support state from becoming fake authority

## Out of Scope
This doc does NOT redefine canonical backend doctrine for Project V, VEDA, or V Forge.
It does NOT replace `ecosystem/db-posture.md`.
It does NOT define all runtime/session mechanics in exhaustive implementation detail.
It does NOT make local SQLite a canonical database.
It does NOT allow governed state to bypass canonical backend interfaces.
It does NOT define the full desktop surface model.

## System
Cross-system desktop operator application for Project V, VEDA, and V Forge using a Tauri 2 host with canonical PostgreSQL-backed backends and a local support-state layer.

## Rules / Doctrine
- Canonical governed system truth remains in the PostgreSQL-backed backend systems for Project V, VEDA, and V Forge.
- The desktop application may use local SQLite as a support-state layer.
- Local SQLite is non-canonical.
- Local SQLite exists to improve continuity, responsiveness, cache behavior, draft handling, and operator experience.
- Local SQLite must not become a competing truth store.
- Approval events, governed mutations, canonical lifecycle state, canonical records, and cross-system source-of-truth state must still pass through canonical backend interfaces.
- In-memory reactive desktop state exists to drive the operator experience and may be hydrated from local SQLite and refreshed from canonical backends.
- Local-first behavior improves UX; it does not weaken governance.
- If local support state and canonical backend truth diverge, canonical backend truth controls.
- Local-first support must remain traceable and bounded.
- Local-first support must not silently create fake approvals, fake readiness, fake launch posture, or fake cross-system truth.

## Three-Layer Model
The desktop host uses three distinct state layers.

### 1. Canonical Backend Layer
The canonical backend layer is the source of governed system truth.
This consists of the Project V, VEDA, and V Forge backend systems backed by canonical PostgreSQL stores.

This layer owns:
- canonical records
- governed lifecycle state
- approval persistence
- planning truth
- observatory truth
- execution truth
- system-of-record mutations
- backend-owned audit and domain history where defined

This layer remains controlling for all governed truth.

### 2. Local SQLite Support Layer
The desktop application may maintain local SQLite support state on the operator's machine.

This layer exists for:
- startup hydration
- recently accessed records
- continuity artifacts
- local cache material
- drafts not yet committed to canonical backends
- local session continuity support
- UI-supportive persistence where speed and continuity matter
- bounded recovery support where explicitly allowed

This layer does NOT become:
- a fourth canonical backend
- a substitute for Project V, VEDA, or V Forge truth
- an approval authority store
- the final location for governed mutations

### 3. In-Memory Reactive State Layer
The desktop application also maintains in-memory reactive state for live operator interaction.

This layer exists for:
- rendering current desktop surfaces
- selection state
- expanded/collapsed UI state
- current interaction context
- currently loaded records or summaries
- live refresh and response behavior

This layer is ephemeral by nature and may be hydrated from the local SQLite support layer and refreshed from canonical backends.
It is not a truth source.

## Boot and Hydration Posture
The local-first model exists so the desktop application can become useful quickly without waiting for remote backend fetches before showing anything meaningful.

The standard posture is:
1. Load local support state from SQLite where available.
2. Hydrate operator-visible desktop state from that local support state.
3. Render the application in a bounded way using that support state.
4. Refresh from canonical backend systems.
5. Reconcile local support state with refreshed canonical state.
6. Update the desktop surfaces accordingly.

This means the operator may see support-state-backed continuity quickly, but canonical refresh remains required.
Support-state hydration does not reclassify the local cache as authority.

## What May Live in Local SQLite
The following are valid examples of local support-state material:
- recently viewed records
- current project/session continuity markers
- panel/layout preferences where appropriate
- cached read models used to accelerate operator workflows
- draft work not yet committed to canonical systems
- transcript support artifacts
- continuity and compaction support artifacts where allowed by canonical docs
- local trace or event support material that improves operator visibility without replacing canonical records

These support operator experience and workflow continuity.

## What Must Not Become Local Truth
The following must not be treated as local authoritative truth:
- final approval records
- canonical lifecycle transitions
- final governed readiness posture
- canonical project admission or closure state
- canonical execution status where V Forge remains source-of-truth
- canonical signal packages where VEDA remains source-of-truth
- any system-of-record state that belongs to Project V, VEDA, or V Forge

If local support material mirrors or previews such state, it must remain clearly subordinate to canonical backend truth.

## Draft and Pending Work Posture
The local support layer may hold draft or pending work for operator continuity.

This is allowed when:
- the material is clearly draft or pending
- it has not yet been represented as canonical system state
- it can be reconciled or discarded safely
- it does not masquerade as a completed governed action

Draft support is useful.
Draft support is not authority.

## Reconciliation Rule
When canonical backend refresh occurs, the desktop application must treat backend state as controlling.

If local support material conflicts with backend truth:
- backend truth controls
- any retained local material must be clearly identified as draft, stale, divergent, or pending review as appropriate
- the operator must not be silently shown stale local material as though it were current governed truth

The local-first model must favor continuity without creating deceptive certainty.

When the desktop application detects that local support-state has diverged from backend canonical state, the event consequences for the operator-visible surfaces, LLM behavior, and blocking posture are defined in `desktop-invalidation-and-refresh-matrix.md` (EVENT-18 — Local Support-State Divergence Detected). This document defines the reconciliation posture — backend truth controls, local material is subordinate — and the matrix defines what the desktop application must surface and block when that divergence condition fires.

## Governance Protection Rule
The local-first model must not be used to bypass governance.

This means:
- local support state must not create approval by implication
- local support state must not create readiness by implication
- local support state must not create handoff by implication
- local support state must not create execution authority by implication
- local support state must not override bounded backend interface rules

Operator convenience does not outrank governance correctness.

## Relationship to Runtime Layer
The runtime/sidecar layer may read from or write to the local support layer where allowed for continuity, transcript support, compaction support, or runtime assistance.

But the same rules apply:
- local persistence remains non-canonical
- runtime support does not become backend truth
- local continuity does not widen authority

## Relationship to Existing Canonical Docs
This doc establishes the local-first support posture for the desktop host.
More specific backend truth remains governed by canonical system docs and interface docs, including:
- `../ecosystem/db-posture.md`
- Project V, VEDA, and V Forge system authority docs
- runtime-sidecar placement docs
- desktop implementation and surface architecture docs

If a more specific canonical doc defines stricter truth boundaries for a given state family, that rule remains controlling.

## Usage
Use this doc when deciding:
- whether a piece of state belongs in canonical backends, local SQLite support state, or in-memory reactive state
- whether a local cache or draft behavior is overreaching into authority
- how desktop continuity and instant-load UX should be implemented without weakening canonical backend truth
- how to reason about local-first support without inventing a new truth domain

## Related Docs
- `../ecosystem/db-posture.md`
- `runtime-sidecar-and-nerve-model.md`
- `desktop-invalidation-and-refresh-matrix.md` — defines EVENT-18 (Local Support-State Divergence Detected) and the full desktop consequences when local/backend divergence is detected
- `../ecosystem/decisions/ADR-009-no-direct-database-access.md`
- `../ecosystem/decisions/ADR-011-tauri-2-desktop-is-the-operator-host.md`
- `../ux/desktop/direction/desktop-host-migration-plan.md`
