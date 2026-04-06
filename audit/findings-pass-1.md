# Pass 1 Findings — Structural Integrity

Date: 2026-04-05
Branch audited: `main` (HEAD `211ed7a`)

Note: a second branch `docs/runtime-vforge-operability-wave` exists and has diverged from `main`. This audit covers `main` only. If that branch contains doc changes not yet merged, this pass should be re-run after merge before proceeding to Pass 2.

---

## 1. Folder placement issues

### Finding 1-A — `ux/` is not in the sanctioned top-level folder list

Sanctioned top-level folders per `pass-1-structural-integrity.md`:
`ecosystem`, `project-v`, `veda`, `v-forge`, `interfaces`, `governance`, `workflows`, `strategy`, `onboarding`, `archive`, `audit`

`ux/` does not appear on this list. It exists at the top level and contains substantive content.

**Flag:** Unsanctioned top-level folder.

---

### Finding 1-B — `nerve/` is not in the sanctioned top-level folder list

`nerve/` does not appear on the sanctioned list. It exists at the top level and contains substantive content.

**Flag:** Unsanctioned top-level folder.

---

## 2. Doc header issues

The Pass 1 rule flags any doc missing **two or more** of: clear title (H1), `## Purpose` or equivalent, `## System` or equivalent, tier declaration or authority statement.

### Finding 2-A — `project-v/schema-specification.md` is missing System and tier declaration

First 20 lines contain: H1 title, `## Purpose`. No `## System`. No tier declaration. Uses "Read this with:" companion list in place of standard header fields.

Missing: `## System` and tier declaration (2 of 4 required fields absent). **Flag.**

---

### Finding 2-B — `project-v/api-conventions.md` is missing System and tier declaration

First 20 lines contain: H1 title, `## Purpose`. No `## System`. No tier declaration. Uses "Read this with:" companion list.

Missing: `## System` and tier declaration (2 of 4 required fields absent). **Flag.**

---

### Finding 2-C — All 12 `project-v/api/*.md` docs are missing System and tier declaration

All twelve route-family docs (`objectives.md`, `initiatives.md`, `work-items.md`, `handoffs.md`, `readiness.md`, `audits.md`, `decision-records.md`, `dependencies.md`, `evidence-links.md`, `external-links.md`, `research-docs.md`, `status-history.md`) use the same "Read this with:" header pattern.

Exceptions: `decision-records.md`, `external-links.md`, `research-docs.md`, and `status-history.md` carry a tier declaration ("This is a Tier 2 Project V API authority document") but still lack a `## System` field. The other eight lack both.

Eight docs missing both `## System` and tier declaration. Four docs missing `## System` only (one field absent — below the two-field threshold for flagging under the strict rule).

**Flag:** Eight docs (`objectives.md`, `initiatives.md`, `work-items.md`, `handoffs.md`, `readiness.md`, `audits.md`, `dependencies.md`, `evidence-links.md`) are missing two or more required header fields.

---

### Finding 2-D — `ecosystem/doc-template.md` is missing System and tier declaration

First 20 lines contain: H1 title, `## Purpose` (one-line placeholder). No `## System`. No tier declaration.

Missing: `## System` and tier declaration. **Flag.**

Note: this is a template file, not an authority doc. The practical impact is low, but it fails the header check mechanically.

---

### Finding 2-E — `ux/desktop/direction/` session docs are missing Purpose, System, and tier declaration

All session spec docs (`session-02` through `session-24`, `v-ecosystem-desktop-ux-work-plan.md`) have no `## Purpose`, no `## System`, and no tier declaration in their first 20 lines. They begin with a title and session-status/dependency metadata.

Missing: `## Purpose`, `## System`, and tier declaration (3 of 4 required fields absent). **Flag** — applies to all 24 files in `ux/desktop/direction/`.

---

### Finding 2-F — `ux/desktop/research/2026-04-02-claude-ux-direction-report.md.md` is missing Purpose, System, and tier declaration

First 20 lines contain: H1 title, status/scope metadata. No `## Purpose`. No `## System`. No tier declaration.

Missing: 3 of 4 required fields. **Flag.**

---

### Finding 2-G — Root-level files `DESKTOP-CODING-README.md`, `EXTENSION-CODING-README.md`, and `ecosystem-docs-execution-plan.md` are missing System and tier declaration

All three have H1 title and `## Purpose`. None have `## System` or a tier declaration.

Missing: `## System` and tier declaration (2 of 4 required fields absent). **Flag.**

---

## 3. Empty and stub files

### Finding 3-A — `ecosystem/doc-template.md` contains only a title and placeholder content

The file is 20 lines, above the 10-line floor, but contains only section headings with one-line placeholders (e.g., "What this doc defines."). No substantive content. Meets the second stub condition: "contains only a title and no substantive content."

**Flag.**

---

### Finding 3-B — `archive/planning-source/source-material-index.md` is fewer than 10 lines of real content and declares itself unpopulated

The file is 357 bytes. It has a title, two placeholder sections, and a single sentence stating the index was never populated. Fewer than 10 meaningful lines. Meets the first stub condition.

**Flag.**

---

## 4. Orphan docs (broken related-doc references)

### No hard broken references found

All `## Related Docs` entries checked against the known file tree resolve to existing files. No 404-equivalent broken links were found across the cross-system interface docs, governance docs, workflow docs, system docs, or ADR clusters.

---

### Finding 4-A — Three `## Related Docs` entries carry stale `*(planned)*` annotations for files that now exist

The following files are referenced with a `*(planned)*` marker in the source doc's Related Docs section, but the target files exist in the repo:

| Source doc | Stale annotation |
|---|---|
| `interfaces/mcp-coordination-model.md` | `../veda/mcp-surface.md *(planned)*` |
| `workflows/project-intake-workflow.md` | `../strategy/opportunity-scoring-model.md *(planned)*` |
| `onboarding/new-project-onboarding-doctrine.md` | `new-project-lifecycle-and-fitment-review.md *(planned)*` |

These are not broken links, but the annotations are factually incorrect. **Flag.**

---

## 5. Undeclared archive material

### Finding 5-A — Fourteen `extension-*` docs in `interfaces/` carry explicit supersession notices but are in an active folder

The following files in `interfaces/` each begin with a `## Status: Superseded by [desktop equivalent]` declaration:

- `extension-agent-orchestration-model.md`
- `extension-compaction-implementation-design.md`
- `extension-governance-and-gating-model.md`
- `extension-human-llm-interaction-model.md`
- `extension-implementation-architecture.md`
- `extension-llm-behavior-contract.md`
- `extension-memory-and-continuity-model.md`
- `extension-state-and-context-model.md`
- `extension-system-init-and-tool-surface-model.md`
- `extension-task-lifecycle-implementation-design.md`
- `extension-token-and-cost-tracking-design.md`
- `extension-tool-surface-implementation-design.md`
- `extension-transcript-persistence-design.md`
- `extension-vscode-surface-architecture.md`

All 14 declare themselves superseded in their headers. Pass 1 Check 5 flags docs outside the `archive/` folder that contain language indicating they are superseded, deprecated, or historical-only.

**Flag:** 14 files in `interfaces/` are self-declared as superseded material and are not in `archive/`.

---

### Finding 5-B — `EXTENSION-CODING-README.md` at root carries an explicit supersession notice but is not in `archive/`

`EXTENSION-CODING-README.md` declares `## Status: Superseded by DESKTOP-CODING-README.md` in its first lines.

**Flag:** Self-declared superseded doc outside `archive/`.

---

## 6. Duplicate authority claims

### None found

No two docs within the repo claim to be the authoritative source on the same subject without differentiation by scope or tier. The layered `data-boundaries.md` pattern (one cross-system doc in `interfaces/`, one per-system doc in each system folder) is scope-differentiated. The layered hammer doctrine pattern (one ecosystem ADR, one governance doc, one per-system doc) is tier-differentiated. No duplicate authority conflicts identified.

---

## Summary

Overall structural health: functional, with clusters of real structural problems concentrated in two areas.

**Most critical issues to fix first:**

1. **Finding 5-A** — 14 superseded `extension-*` docs sitting in the active `interfaces/` folder. These are the highest-count structural problem and the most likely to cause orientation problems for LLMs or developers scanning `interfaces/` for active doctrine.

2. **Finding 1-A / 1-B** — `ux/` and `nerve/` are unsanctioned top-level folders. Neither appears in the folder-placement schema defined in `README.md` or `pass-1-structural-integrity.md`.

3. **Finding 2-C / 2-E** — Header non-conformance is widespread in two clusters: the `project-v/api/` route docs (missing System/tier) and the `ux/desktop/direction/` session docs (missing Purpose, System, and tier). These are large doc clusters with consistent header gaps.

4. **Finding 4-A** — Three stale `*(planned)*` annotations for files that now exist.

5. **Finding 3-A / 3-B** — Two stub files: `ecosystem/doc-template.md` (placeholder content only) and `archive/planning-source/source-material-index.md` (self-declared unpopulated).
