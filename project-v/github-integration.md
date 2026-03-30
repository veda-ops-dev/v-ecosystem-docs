# Project V GitHub Integration

## Purpose

This document defines how Project V relates to GitHub and source control
as part of planning-side implementation traceability.

It exists to answer:

```text
What does Project V record about GitHub, what thin references may it preserve
for planning-side traceability, and what must it never absorb from GitHub
that would make Project V the canonical owner of source-control or execution truth?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- how Project V may reference GitHub artifacts for planning-side traceability
- what thin source-control linkage is permitted in Project V
- what GitHub-related information must remain outside Project V
- the boundary rules that prevent Project V from becoming a source-control mirror

---

## Out of Scope

This document does not define:

- the detailed schema for every traceability field
- V Forge internal execution workflow involving GitHub
- CI/CD pipeline design
- runtime observability behavior
- GitHub API implementation mechanics

Those belong in implementation docs and V Forge docs.

---

## System

- project-v

---

## Core Rule

Project V may reference GitHub artifacts for planning-side traceability.
Project V must not become the canonical owner of source-control truth.

GitHub is execution truth. Source control belongs in V Forge and in the
actual repository. Project V preserves thin bounded links — enough to
support handoff clarity, planning continuity, and bounded audit — without
replicating or displacing what lives in GitHub.

---

## What Project V May Reference

Project V may preserve thin bounded references to GitHub artifacts including:

### Repository and branch references
Links to the repository or branch where a project's implementation lives,
used to support handoff clarity and execution linkage.

### Pull request or commit references
Thin links to specific PRs or commits that correspond to planned or handed-off
work, used to support planning-to-execution traceability.
Project V records the reference — it does not replicate the PR or commit content.

### Implementation milestone references
References to GitHub milestones or issues that correspond to governed planning
work items, used to support bounded orchestration visibility.

### BYDA audit linkage
Bounded external links used by the BYDA audit layer to assess whether
planning-side intent and execution-side implementation agree at a high level.
This is planning-side audit behavior, not execution truth absorption.

---

## What Project V Must Not Absorb

Project V must not:

- replicate commit history as planning truth
- treat GitHub as the canonical source of what was built
- store rich execution lifecycle state derived from GitHub as Project V records
- mirror source-control content to the extent that V Forge becomes redundant
- use GitHub access to bypass the governed handoff and return-to-planning interfaces

GitHub provides external linkage for planning-side traceability.
V Forge is the canonical owner of execution truth, including what was built.

---

## BYDA and GitHub

The BYDA audit layer in Project V may reference GitHub for bounded
planning-side consistency checks — for example, checking whether a
planned implementation artifact appears to have a corresponding external reference.

This is a thin signal for planning audit confidence.
It is not a substitute for V Forge's execution truth or for code review.

BYDA behavior in Project V is defined in:
`byda-in-project-v.md`

---

## Boundary Preservation Rule

If Project V's GitHub integration begins to:
- replicate rather than reference
- treat GitHub content as canonical planning truth
- substitute for V Forge's execution record
- grow in granularity to where Project V is modeling source-control history

...then the integration has exceeded its bounded traceability role and
has started absorbing execution truth. That drift must be corrected.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- Project V uses GitHub for thin planning-side traceability, not source-control authority
- references to GitHub artifacts do not make Project V the execution ledger
- V Forge remains the canonical owner of what was built
- BYDA audit linkage is a planning-confidence signal, not code validation

---

## Usage

This document should be used:

- when designing planning-side traceability fields that reference GitHub
- when evaluating whether a proposed GitHub integration stays within bounded traceability
- when reviewing whether BYDA audit linkage is being used correctly
- when writing schema authority docs that include source-control reference fields

---

## Related Docs

- `project-v.md`
- `system-invariants.md`
- `implementation-traceability.md`
- `byda-in-project-v.md`
- `data-boundaries.md`
- `../v-forge/v-forge.md`
- `../v-forge/system-invariants.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`