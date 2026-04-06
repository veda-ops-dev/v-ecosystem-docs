# ADR-011: Tauri 2 Desktop Is the Operator Host

## Status
Accepted

## Date
2026-04-02

## Context
The V Ecosystem has three systems — Project V, VEDA, and V Forge — and requires a unified operator host that preserves shared project scope, governance visibility, cross-system context, approval discipline, and execution traceability.

ADR-008 established that the ecosystem should not fragment into three separate operator hosts. That unification decision remains correct.

What changed is the host choice.

The VS Code extension model no longer fits the operational shape of the ecosystem. The extension container constrains navigation, review, approval, cross-system context, and especially execution-heavy V Forge surfaces. The ecosystem is planning, observatory, and execution work — not code-editing work — and should not remain architecturally centered on a code editor host.

The adopted desktop direction is a Tauri 2 desktop application with a React/TypeScript/Vite frontend, a sidecar/runtime layer for runtime support concerns, and a local-first support layer that preserves operator continuity without replacing canonical backend truth.

## Decision
The V Ecosystem operator host is a unified Tauri 2 desktop application.

The ecosystem does NOT split into separate hosts per system.
Project V, VEDA, and V Forge remain co-located inside one operator application with clear internal boundaries.

The desktop host uses:
- a unified application shell for Project V, VEDA, and V Forge
- desktop-native surface architecture rather than VS Code activity-bar, sidebar, editor-panel, or status-bar constructs
- a sidecar/runtime layer for runtime-support capabilities such as MCP coordination and Nerve runtime support
- a local-first support layer that may use local SQLite for cache, drafts, continuity, and UI hydration without creating a new canonical truth store
- canonical PostgreSQL-backed system backends that remain the source of truth for governed system state

The unification rationale from ADR-008 remains in force:
- the operator should not manage three separate hosts or contexts
- shared infrastructure such as session/project scope remains ecosystem-wide
- cross-system context and governance visibility belong to one operator environment, not separate products

## Consequences
- ADR-008 is superseded on host choice but preserved in principle on unification posture
- The primary host assumption across the docs set must move from VS Code extension constructs to Tauri 2 desktop application constructs
- Host-bound extension docs must be superseded, rewritten, or archived deliberately
- New canonical docs are required for desktop surface architecture, desktop implementation architecture, runtime/sidecar/Nerve placement, and local-first architecture
- Nerve must be re-homed as a runtime-support direction within the desktop/sidecar model rather than described as extension-bound
- Chat or LLM interaction remains a support surface and must not become approval authority, governance authority, or canonical system state
- The desktop host remains a governance-visible operator environment, not just a display shell

## Related Docs
- `ADR-008-one-unified-vscode-extension.md`
- `../../ux/desktop/direction/desktop-host-migration-plan.md`
- `../../interfaces/`
- `ADR-005-session-token-model-for-project-scope.md`
- `ADR-009-no-direct-database-access.md`
