# Desktop Host Migration Plan

## Purpose
Define the official migration plan for moving the V Ecosystem documentation set from a VS Code extension-centered host model to a Tauri 2 desktop application host model.

## Scope
This plan governs documentation migration sequencing, authority realignment, desktop-host replacement work, Nerve re-homing posture, and archive/supersession handling for host-bound extension material.

## Out of Scope
This plan does NOT rewrite governance doctrine.
It does NOT change Project V, VEDA, or V Forge system boundaries.
It does NOT make `ux/desktop/` an authority root.
It does NOT act as a substitute for ADRs, interface docs, or system authority docs.
It does NOT define implementation code tasks in full detail.

## System
Cross-system desktop operator application for Project V, VEDA, and V Forge using a Tauri 2 host model.

## Rules / Doctrine
- This is a host migration, not a doctrine rewrite.
- Canonical authority remains in `ecosystem/`, `governance/`, `interfaces/`, `project-v/`, `veda/`, and `v-forge/`.
- `ux/desktop/` remains implementation-support material subordinate to shared-root authority.
- Research reports and audits may inform migration work but do not become authority by existing.
- Host-neutral doctrine must be preserved wherever possible.
- Host-bound extension material must be replaced, superseded, or archived deliberately.
- No VS Code document should be silently deleted if it contains still-useful doctrinal or implementation value.
- Nerve must remain a V-native runtime-support direction and must not become a shadow authority root.
- The desktop host model must explicitly account for the Tauri 2 shell, the sidecar/runtime layer, the local-first SQLite layer, and the canonical PostgreSQL backends.
- The migration must not allow chat or LLM surfaces to become authority, approval, or canonical operating state.

## Migration Phases

### Phase 0 - Authority Anchor
Create the canonical authority basis for the host shift before editing downstream documents.

Required work:
- Write `ecosystem/decisions/ADR-011-tauri-2-desktop-is-the-operator-host.md`.
- Mark `ecosystem/decisions/ADR-008-one-unified-vscode-extension.md` as superseded by ADR-011.
- Update root-level references so the docs set no longer presents the VS Code extension as the accepted primary host.

Phase 0 completion standard:
- The docs root has one clear accepted host decision.
- New desktop docs do not conflict with accepted ADR-level authority.

### Phase 1 - Runtime and Persistence Spine
Define the new runtime and persistence architecture before renaming or rewriting extension-facing support docs.

Required work:
- Write `interfaces/runtime-sidecar-and-nerve-model.md`.
- Write `interfaces/local-first-architecture.md`.

Phase 1 completion standard:
- Nerve has an explicit architectural home in the Tauri 2 model.
- The sidecar/runtime boundary is defined.
- The SQLite local-first layer is defined as non-canonical support state.
- The PostgreSQL canonical-backend posture remains explicit and uncontested.

### Phase 2 - Desktop Surface and Implementation Authority
Replace the extension host surface model and implementation-host assumptions with desktop-native authority docs.

Required work:
- Write `interfaces/desktop-surface-architecture.md`.
- Write `interfaces/desktop-implementation-architecture.md`.

Required preservation rule:
- All load-bearing absent-affordance rules, gate-surface rules, synchronization rules, and LLM-surface limits from the extension surface architecture must be preserved unless explicitly and deliberately changed.

Phase 2 completion standard:
- The desktop host has a canonical surface architecture.
- The desktop host has a canonical implementation architecture.
- The desktop surface model preserves governance force rather than weakening it.

### Phase 3 - Extension Doc Migration Pass
Rename or update extension-prefixed docs whose substance remains valid but whose host framing is stale.

Priority migration targets:
- `extension-llm-behavior-contract.md`
- `extension-governance-and-gating-model.md`
- `extension-agent-orchestration-model.md`
- `extension-state-and-context-model.md`
- `extension-memory-and-continuity-model.md`
- `extension-human-llm-interaction-model.md`
- `extension-system-init-and-tool-surface-model.md`
- `extension-compaction-implementation-design.md`
- `extension-tool-surface-implementation-design.md`
- `extension-token-and-cost-tracking-design.md`
- `extension-transcript-persistence-design.md`
- `extension-task-lifecycle-implementation-design.md`
- `mcp-coordination-model.md`
- `operator-surface-interfaces.md`

Migration rule:
- Preserve doctrine first.
- Replace host framing second.
- Rewrite only the parts that are truly host-bound.

Phase 3 completion standard:
- The docs set no longer relies on extension framing for host-neutral doctrine.
- Renamed or updated docs do not contain stale VS Code surface assumptions.

### Phase 4 - Nerve Language and Planning Alignment
Update the Nerve cluster so its planning and support posture align with the Tauri 2 desktop + sidecar model.

Required work:
- Update `nerve/README.md` language to reflect the desktop/sidecar runtime host.
- Update active Nerve planning artifacts so sidecar/runtime framing replaces extension-host framing.
- Preserve historical investigation docs as historical support artifacts where appropriate.

Phase 4 completion standard:
- Nerve remains bounded, readable, and non-authoritative.
- Nerve planning language aligns with the new runtime host.
- Historical research material is not mistaken for current host authority.

### Phase 5 - Archive and Supersession Pass
Archive or supersede deeply host-bound extension documents after desktop replacements exist.

Priority archive/supersession targets:
- `EXTENSION-CODING-README.md`
- `interfaces/extension-vscode-surface-architecture.md`
- `interfaces/extension-implementation-architecture.md`
- other deeply VS Code-bound docs after replacement validation

Archive rule:
- Every archived or superseded document must state its status explicitly at the top and reference the replacing doc or ADR.

Phase 5 completion standard:
- The active docs set no longer depends on VS Code host docs.
- Archived material remains available for traceability without masquerading as authority.

### Phase 6 - Verification and Cleanup
Run a final consistency pass after the migration wave is complete.

Required work:
- Search for stale host-language references such as `VSCode`, `VS Code`, `activity bar`, `view container`, `secondary sidebar`, `editor-area`, and similar extension-specific surface terms.
- Update `Related Docs` sections in affected files.
- Confirm that no document under `ux/desktop/` is being treated as canonical authority by omission or convenience.

Phase 6 completion standard:
- The active docs set is internally consistent.
- Host-bound references are either intentional historical references or fully migrated.
- The authority hierarchy remains clear to humans and LLMs.

## Priority Files
The first files to create or edit are:
1. `ecosystem/decisions/ADR-011-tauri-2-desktop-is-the-operator-host.md`
2. `ecosystem/decisions/ADR-008-one-unified-vscode-extension.md` (status update only)
3. `interfaces/runtime-sidecar-and-nerve-model.md`
4. `interfaces/local-first-architecture.md`
5. `interfaces/desktop-surface-architecture.md`
6. `interfaces/desktop-implementation-architecture.md`

## Archive Rules
- Archive is not authority.
- Superseded docs must identify the replacing doc or ADR directly.
- Historical research, migration audits, and AI-generated reports belong under `ux/desktop/research/` unless and until their conclusions are promoted into canonical docs.
- `direction/` docs may guide implementation but do not override canonical authority.
- No file should remain ambiguously active if a replacement exists.

## Usage
Use this plan as the working migration sequence for the host transition.
Use research reports and audits as supporting inputs only.
Promote any load-bearing migration conclusion into the correct ADR or interface doc before treating it as settled.

## Related Docs
- `README.md`
- `ux/desktop/README.md`
- `ecosystem/doc-template.md`
- `ecosystem/decisions/ADR-008-one-unified-vscode-extension.md`
- `interfaces/`
- `nerve/`
