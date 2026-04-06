# Audit Pass 1 — Structural Integrity

## Purpose

Verify that the `C:\dev\v-ecosystem-docs` folder tree is structurally sound before any content auditing begins.

Structural problems corrupt every downstream pass. Fix these first.

---

## Scope

Full repo. One session.

---

## Setup

Load this context before beginning:

1. Read the folder tree: `C:\dev\v-ecosystem-docs` (2 levels deep minimum)
2. Read `C:\dev\v-ecosystem-docs\audit\README.md`
3. Do not load individual doc content yet — this pass works from headers and structure only

---

## Checks

### 1. Folder placement

For every folder in the repo, verify it maps to one of these sanctioned top-level categories:

- `ecosystem`
- `project-v`
- `veda`
- `v-forge`
- `interfaces`
- `governance`
- `workflows`
- `strategy`
- `onboarding`
- `archive`
- `audit`

Flag any folder that does not map clearly to one of these categories. Do not flag subfolders within these — only top-level divergence.

### 2. Doc headers

For every `.md` file in the repo, read the first 20 lines. Check for:

- [ ] Is there a clear title (H1)?
- [ ] Is there a `## Purpose` or equivalent section that states what the doc is for?
- [ ] Is there a `## System` field or equivalent that declares which system owns this doc?
- [ ] Is there a tier declaration or authority statement? (e.g., "This is a Tier 1 ecosystem authority document.")

Flag any doc missing two or more of these. Flag any doc where the tier declaration is absent.

### 3. Empty and stub files

Flag any `.md` file that is:

- fewer than 10 lines, OR
- contains only a title and no substantive content

These are misleading stubs. They must either be filled or deleted.

### 4. Orphan docs

For every doc that contains a `## Related Docs` section, extract the listed filenames. Check whether each listed file exists at the expected path.

Flag any broken reference (doc listed as related but not found).

### 5. Undeclared archive material

Check the `archive` folder. Verify that any doc outside the `archive` folder does not contain language indicating it is superseded, deprecated, or historical-only.

Flag any active-folder doc that appears to be archive material based on its content or title.

### 6. Duplicate authority claims

Scan for docs that claim to be authoritative on the same topic. Flag pairs where two docs both declare authority over the same subject.

---

## Output format

Produce a structured findings report with these sections:

```
## Pass 1 Findings — Structural Integrity
Date: [date]

### Folder placement issues
[list or "None found"]

### Doc header issues
[list each file with missing fields]

### Empty/stub files
[list or "None found"]

### Orphan docs (broken related-doc references)
[list each broken reference]

### Undeclared archive material
[list or "None found"]

### Duplicate authority claims
[list pairs or "None found"]

### Summary
[2–3 sentences: overall structural health, most critical issues to fix first]
```

Save the findings report to: `C:\dev\v-ecosystem-docs\audit\findings-pass-1.md`

---

## Do not fix

This pass produces findings only. Do not edit docs during this pass. Flag problems for human review.
