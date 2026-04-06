# Audit Pass 2 — Vocabulary & Term Consistency

## Purpose

Identify term drift, undefined load-bearing terms, and near-synonym sprawl across the V Ecosystem docs.

Term drift is a primary cause of LLM confusion during implementation and reconstruction. A word that means two things means nothing.

---

## Scope

Per system. Run once per system. 3–4 sessions total:

- Session A: `ecosystem` + `governance` folders
- Session B: `project-v` folder
- Session C: `veda` folder
- Session D: `v-forge` folder + `interfaces` folder

---

## Setup

For each session, load:

1. All `.md` files within the session's assigned folders (full content)
2. The canonical vocabulary reference if one exists — check `C:\dev\v-ecosystem-docs\ecosystem\` for any file named `vocabulary`, `glossary`, or `terms`
3. `C:\dev\v-ecosystem-docs\audit\findings-pass-1.md` — do not audit docs that were flagged as stubs or archive material

---

## Checks

### 1. Load-bearing terms without definitions

Identify terms that are used to drive decisions, constrain behavior, or define boundaries — but are never explicitly defined within the loaded docs.

Examples of load-bearing terms: `signal`, `evidence`, `handoff`, `readiness`, `execution scope`, `governance gate`, `operator`.

For each undefined load-bearing term, record:
- the term
- which docs use it
- whether a definition exists anywhere in the loaded set

### 2. Near-synonym sprawl

Look for cases where multiple words are used to mean the same thing.

Common patterns to check:
- Does the doc use both `task` and `work item` interchangeably?
- Does the doc use both `operator` and `user` without distinction?
- Does the doc use both `agent` and `AI` or `LLM` for the same concept?
- Does the doc use both `activity trail` and `audit log` or `event log`?
- Does the doc use both `evidence` and `data` or `signal` interchangeably?

For each near-synonym pair found, record:
- the two (or more) terms
- where each appears
- which one is the canonical term (if determinable)
- whether the distinction is intentional or accidental

### 3. Canonical terms used incorrectly

Check for cases where a defined term is used in a way that contradicts its definition.

Example: if `signal` is defined as VEDA's real-time observable data, flag any doc that uses `signal` to mean something else.

### 4. Undefined pronouns and vague references

Flag uses of:
- "the system" (which system?)
- "the agent" (which agent? in what context?)
- "the user" (operator? human? end user?)
- "it" used ambiguously across system boundaries

### 5. Inconsistent capitalization of proper nouns

Check that system names are consistently capitalized and formatted:
- `Project V` (not `project v`, `ProjectV`, `project-v` in prose)
- `VEDA` (all caps)
- `V Forge` (not `VForge`, `v-forge` in prose)

Flag inconsistencies.

---

## Output format

```
## Pass 2 Findings — Vocabulary & Term Consistency
Session: [A / B / C / D]
Folders audited: [list]
Date: [date]

### Undefined load-bearing terms
[term | docs that use it | definition found? Y/N]

### Near-synonym sprawl
[term pair | locations | canonical term | intentional? Y/N]

### Canonical terms used incorrectly
[term | doc | how it's misused]

### Vague references
[reference | doc | why it's ambiguous]

### Capitalization inconsistencies
[term | incorrect form | correct form | docs affected]

### Summary
[2–3 sentences: vocabulary health for this session's scope, most urgent fixes]
```

Save findings to: `C:\dev\v-ecosystem-docs\audit\findings-pass-2-[session-letter].md`

---

## Do not fix

This pass produces findings only. Do not edit docs during this pass.

If a canonical vocabulary doc does not exist and should, flag that as a finding — do not create it during this pass.
