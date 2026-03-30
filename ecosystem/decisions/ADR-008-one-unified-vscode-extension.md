# ADR-008: One Unified VSCode Extension

## Status
Accepted

## Date
Earlier session — recorded here for ADR hygiene

## Context
The V Ecosystem has three systems — Project V, VEDA, and V Forge. The question arose whether to build one VSCode extension for each system (three separate extensions) or one unified extension that surfaces all three.

## Decision
The V Ecosystem ships as one unified VSCode extension.

The three systems are surfaced as panels and views inside the single extension. Internal module boundaries within the extension mirror ecosystem boundaries. Commands are namespaced per system (e.g., `projectv.`, `veda.`, `vforge.`).

Three separate extensions were rejected for these reasons:
- UX complexity — the operator would need to manage three separate extensions and context-switch between them
- Shared infrastructure — session token management, active project state, and status bar belong to the ecosystem as a whole, not to any one system
- Maintenance overhead — three extensions mean three separate release cycles, three package manifests, three sets of configuration

The single extension is the operator's unified workspace for the entire ecosystem.

## Consequences
- One extension package with internal module separation by system
- The active project selector, session token management, and status bar live in shared extension infrastructure
- System-specific panels and commands are namespaced but co-located
- Extension implementation sessions must use the special extension prompt — do not carry over assumptions from docs sessions
- The extension is a governance layer for project scope, not just a display surface

## Related Docs
- `../../interfaces/mcp-coordination-model.md`
- `ADR-005-session-token-model-for-project-scope.md`
