# Extension Coding Readme

## Status
Superseded by `DESKTOP-CODING-README.md`

## Purpose

This file tells developers what they must read before writing code for the legacy VS Code extension host model.

The VS Code extension is no longer the primary operator host.
ADR-011 establishes the Tauri 2 desktop application as the primary host.
Use `DESKTOP-CODING-README.md` for active implementation work.

## Supersession Rule

- Do not use this file as the implementation entry point for current work.
- Do not treat the extension-prefixed doctrine docs as the active host doctrine set.
- Use this file only for historical traceability or legacy extension review.

## Related Docs

- `DESKTOP-CODING-README.md`
- `ecosystem/decisions/ADR-011-tauri-2-desktop-is-the-operator-host.md`
- `ecosystem/decisions/ADR-008-one-unified-vscode-extension.md`
