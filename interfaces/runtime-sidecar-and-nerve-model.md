# Runtime Sidecar and Nerve Model

## Purpose
Define the canonical runtime model for the Tauri 2 desktop host, including sidecar placement, Nerve placement, runtime ownership boundaries, and the relationship between the desktop application, runtime-support layer, and canonical backend systems.

## Scope
This doc governs the runtime placement and ownership model for:
- the Tauri 2 desktop operator application
- the sidecar/runtime layer
- Nerve as the V-native runtime-support direction
- MCP-related coordination and runtime-support concerns
- runtime/session/tooling support responsibilities that do not belong in canonical system backends or purely presentational UI surfaces

## Out of Scope
This doc does NOT redefine ecosystem doctrine for Project V, VEDA, or V Forge.
It does NOT replace `mcp-coordination-model.md`.
It does NOT define the detailed desktop surface architecture.
It does NOT make Nerve a fourth ecosystem system.
It does NOT make the sidecar a canonical truth store.
It does NOT define implementation code in exhaustive detail.

## System
Cross-system desktop operator application for Project V, VEDA, and V Forge using a Tauri 2 host with a sidecar/runtime layer.

## Rules / Doctrine
- The operator host is a Tauri 2 desktop application.
- The desktop application includes a runtime-support layer implemented as a managed sidecar/runtime process.
- Nerve is the V Ecosystem's runtime-support direction for this sidecar/runtime layer.
- Nerve is not a fourth ecosystem system.
- Nerve does not create new truth ownership, approval authority, planning authority, observatory authority, or execution authority.
- The sidecar/runtime layer is subordinate to canonical system doctrine and backend truth.
- The sidecar/runtime layer may support session management, tool-surface assembly, compaction, transcript persistence, token/cost tracking, runtime orchestration support, and bounded execution support.
- The sidecar/runtime layer must not silently mutate canonical state outside approved backend interfaces and governance paths.
- The sidecar/runtime layer must not become a shadow authority root.
- The sidecar/runtime layer must not cause chat or LLM output to become approval or system truth by convenience.
- Canonical governed system state remains in the PostgreSQL-backed system backends reached through approved interfaces.
- Local runtime support state may exist for continuity and operation, but it does not supersede canonical backend truth.

## Runtime Placement Model
The desktop host is composed of distinct layers:

### 1. Frontend Application Layer
The React/TypeScript desktop frontend owns:
- operator-visible surfaces
- interaction handling
- context display
- desktop shell layout
- local UI state and rendering behavior
- bounded calls into runtime and backend services

The frontend is a product surface, not the runtime authority layer.
It must not own hidden execution pathways that bypass canonical runtime or backend boundaries.

### 2. Sidecar / Runtime Layer
The sidecar/runtime layer owns runtime-support concerns that should not live purely in the frontend surface layer.
These may include:
- MCP session/runtime coordination support
- Nerve runtime support behavior
- session initialization and runtime scope support
- tool-surface filtering and protected tool exposure
- compaction and continuity-support mechanics
- transcript persistence support
- token and cost tracking support
- runtime orchestration support
- bounded long-running runtime tasks that do not belong in the frontend view layer

MCP session management specifically — including session initialization calls to the MCP server, session token storage, scope binding, and session token forwarding on tool calls — is a sidecar responsibility. The frontend does not call the MCP server directly. The frontend requests session operations through the sidecar, and the sidecar owns the actual MCP server communication. This keeps session token handling out of the frontend layer and preserves the boundary between presentation surface and runtime-support layer.

The sidecar/runtime layer exists so runtime machinery is separated from presentation surfaces.
It is the governed engine room, not the operator surface itself.

### 3. Canonical Backend Layer
The canonical backend layer owns governed system truth.
This includes Project V, VEDA, and V Forge backend services backed by canonical PostgreSQL stores.

These systems remain authoritative for:
- planning truth
- observatory truth
- execution truth
- approval events
- governed lifecycle state
- system-owned records

The sidecar/runtime layer does not replace these systems and does not become a competing authority source.

## Nerve Placement
Nerve is placed in the sidecar/runtime layer.

Nerve is the V-native runtime-support direction that shapes how the desktop host handles:
- governed runtime session support
- bounded orchestration support
- compaction posture
- tool-surface management
- transcript and continuity support
- runtime-support implementation patterns needed to make the desktop operator application viable without violating V doctrine

Nerve remains bounded by these rules:
- it is not a planning authority
- it is not an observatory authority
- it is not an execution truth authority
- it is not a substitute for canonical interface docs
- it is not claw-code
- external repos remain pattern mines only

## Ownership Boundaries

### Frontend owns
- shell layout
- operator-visible surface composition
- panel and workspace rendering
- immediate interaction state
- presenting context, warnings, outputs, and actions
- invoking approved runtime or backend pathways

### Sidecar/runtime owns
- runtime session support
- runtime-only protected mechanics
- tool-surface support logic
- long-running or process-bound runtime work
- Nerve runtime-support behaviors
- runtime trace/event support passed back to the frontend

### Backend systems own
- canonical records
- canonical lifecycle state
- approval persistence
- governed mutations
- cross-system system-of-record data
- business/domain truth

## Communication Model
The desktop frontend communicates with the sidecar/runtime layer through the Tauri host boundary.
The sidecar/runtime layer communicates with canonical backend services through approved backend interfaces.

This means:
- the frontend does not directly become the runtime engine
- the sidecar does not become the UI surface
- the sidecar does not become a direct substitute for canonical backend services
- host/runtime communication must preserve scope, visibility, and governance boundaries

## Session and Scope Posture
Project/session scope remains governed.
The runtime layer may support scope enforcement and session continuity, but it must do so within the canonical session-token and backend-boundary posture.

The sidecar/runtime layer must not widen scope simply because runtime support is available.
Runtime support may narrow or preserve scope; it must not self-authorize scope expansion.

## Persistence Posture
Runtime-support data may be persisted locally or operationally for continuity, transcript support, compaction support, or session recovery support where allowed.

But:
- this data is non-canonical unless explicitly defined otherwise in canonical docs
- local runtime persistence does not replace backend records
- approval and governed state changes must still pass through the canonical backend path

## Traceability and Visibility
If the sidecar/runtime layer performs work that affects operator interpretation, workflow decisions, or review posture, the resulting outputs must remain traceable.

The runtime layer must support:
- visible status where materially relevant
- traceable outputs
- failure surfacing
- bounded orchestration visibility where orchestration is active
- clear distinction between support output and canonical system truth

The runtime layer must not create hidden governance by doing material work off-screen with no visible accountability.

## Relationship to Existing Canonical Docs
This doc establishes architectural placement.
More specific behavior remains governed by related canonical docs, including:
- `mcp-coordination-model.md`
- `desktop-agent-orchestration-model.md` or its successor naming
- compaction, tool-surface, transcript, token/cost, and task-lifecycle implementation-design docs
- desktop surface and implementation architecture docs

If a more specific canonical doc defines a bounded rule for a runtime-support area, that rule remains controlling for that area.

## Usage
Use this doc when deciding:
- whether a capability belongs in the frontend, the sidecar/runtime layer, or canonical backends
- where Nerve belongs in the Tauri 2 desktop model
- whether a runtime-support feature is overreaching into system authority
- how to preserve runtime support without creating shadow authority or host confusion

## Related Docs
- `mcp-coordination-model.md`
- `../nerve/README.md`
- `../ecosystem/decisions/ADR-010-agent-orchestration-is-an-extension-runtime-capability.md`
- `../ecosystem/decisions/ADR-011-tauri-2-desktop-is-the-operator-host.md`
- `../ux/desktop/direction/desktop-host-migration-plan.md`
