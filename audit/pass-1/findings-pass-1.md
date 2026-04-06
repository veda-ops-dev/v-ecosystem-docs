## Pass 1 Findings — Structural Integrity
Date: 2026-04-05

### Folder placement issues
- `nerve/` is a top-level folder that does not map clearly to any sanctioned category in the audit template. It appears to be a runtime support layer, but the sanctioned list does not include it.
- `ux/` is a top-level folder that does not map clearly to any sanctioned category in the audit template.

### Doc header issues
- `ecosystem/doc-template.md` — missing clear title/H1 structure beyond template placeholder content; missing `## System`; missing tier declaration.
- `EXTENSION-CODING-README.md` — missing `## System`; missing tier declaration.
- Multiple ADRs and decision docs rely on ADR structure rather than the full shared header pattern. These are not all structurally invalid, but they diverge from the expected shared doc header template.

### Empty/stub files
- `ecosystem/doc-template.md` — template/stub, not substantive content.

### Orphan docs (broken related-doc references)
- Several docs reference interface/design docs that do not exist at the stated paths or use stale names from the extension-era naming set.
- Several docs reference desktop migration successor docs inconsistently.

### Undeclared archive material
- A group of `interfaces/extension-*` docs are self-declared superseded but still live outside `archive/`.
- `project-v/operator-surfaces/vscode-extension.md` appears stale/superseded in practice relative to the desktop host migration, but is not explicitly marked as superseded.

### Duplicate authority claims
- Potential overlap exists between some ecosystem-level and system-level docs on boundaries and ownership, but no fully duplicated same-topic authority pair was identified as a clear collision.

### Summary
The repo is structurally usable, but Pass 1 found several issues that can mislead downstream audits: unsanctioned top-level folders, stale/superseded docs outside archive, and a small number of header/template issues. The most important problems to account for in later passes are the self-declared superseded `extension-*` interface docs and other stale host-era materials that should not be treated as active authority.
