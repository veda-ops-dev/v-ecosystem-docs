# Audit 02 — Ecosystem Foundation Audit Prompt

Use this prompt for the second Claude audit pass.

---

You are performing an **Ecosystem Foundation Audit** of the V Ecosystem docs.

Use the audit posture below and follow it strictly.

[PASTE THE FULL CONTENTS OF `audit-posture.md` HERE]

---

## Audit goal

I want you to audit whether the **ecosystem-level foundation docs** define a coherent, durable, cross-system law for the V Ecosystem.

This is the layer that should establish:
- shared vocabulary
- cross-system boundaries
- ecosystem-wide architectural decisions
- doctrine vs operational-state posture
- external provider integration posture
- the high-level ecosystem model that all system docs are supposed to obey

This is **not** the governance spine audit yet.
This is **not** the Project V / VEDA / V Forge deep audit yet.
This is the shared ecosystem-law audit.

Stay focused on:
- ecosystem-level consistency
- vocabulary stability
- ADR alignment
- cross-system framing
- shared-law sufficiency
- root ecosystem doctrine coherence

Do not drift into detailed system redesign.

---

## Audit target

Review these docs together as one ecosystem-law cluster:

### Core ecosystem docs
- `ecosystem/v-ecosystem-overview.md`
- `ecosystem/cross-system-boundaries.md`
- `ecosystem/vocabulary.md`
- `ecosystem/doctrine-vs-operational-state.md`
- `ecosystem/external-provider-integration-doctrine.md`
- `ecosystem/db-posture.md`

### Ecosystem ADRs
- `ecosystem/decisions/ADR-001-veda-is-pure-observatory.md`
- `ecosystem/decisions/ADR-002-content-graph-moves-to-v-forge.md`
- `ecosystem/decisions/ADR-003-veda-brain-eliminated.md`
- `ecosystem/decisions/ADR-004-mcp-tools-are-thin-wrappers.md`
- `ecosystem/decisions/ADR-005-session-token-model-for-project-scope.md`
- `ecosystem/decisions/ADR-006-hammer-doctrine-is-ecosystem-law.md`
- `ecosystem/decisions/ADR-007-docs-are-build-spec-db-owns-operational-state.md`
- `ecosystem/decisions/ADR-008-one-unified-vscode-extension.md`
- `ecosystem/decisions/ADR-009-no-direct-database-access.md`
- `ecosystem/decisions/ADR-010-agent-orchestration-is-an-extension-runtime-capability.md`

You are not auditing every downstream system doc yet.
You are auditing whether this **ecosystem cluster** provides a strong enough shared law that the downstream docs can inherit from it cleanly.

---

## Core questions

Answer these with specifics:

1. Do the ecosystem docs define a coherent shared law for all three systems?
2. Are the core ecosystem docs mutually consistent in vocabulary and role?
3. Do the ADRs still align with the live ecosystem docs, or is there drift?
4. Are any important ecosystem-level terms underdefined, multiply defined, or used inconsistently?
5. Do the ecosystem docs clearly separate:
   - observatory truth
   - planning truth
   - execution truth
   - governance/control
   - operational state
6. Do the ecosystem docs establish strong enough boundary law before system-specific details begin?
7. Are any ecosystem docs doing too much, too little, or the wrong kind of work?
8. Is there any ecosystem-level doctrine gap that would confuse later system audits or implementation work?

---

## What I want from you

Organize your answer exactly like this:

# 1. Direct judgment

Give a blunt judgment on the ecosystem foundation layer.
Examples:
- strong and coherent
- mostly coherent with bounded cleanup needed
- conceptually strong but vocabulary-drifty
- or whatever you think is accurate

Explain briefly.

# 2. Ecosystem-law coherence audit

Assess whether the core ecosystem docs work together as one coherent shared-law cluster.
Call out:
- strongest parts
- weakest parts
- any doc that is underperforming its role

# 3. Vocabulary and term-discipline audit

Audit `ecosystem/vocabulary.md` and the surrounding ecosystem docs for:
- missing terms
- duplicate terms
- inconsistent term usage
- terms doing too much work
- terms used in docs but not clearly anchored

Be concrete.

# 4. ADR alignment audit

Assess whether ADR-001 through ADR-010 still align with the live ecosystem docs.
Call out:
- ADRs that are still load-bearing and well integrated
- ADRs that may be underlinked or weakly reflected
- any drift between ADR intent and live doctrine wording

# 5. Boundary-law audit

Assess whether the ecosystem docs clearly establish:
- system ownership boundaries
- doctrine vs operational-state posture
- DB posture
- provider posture
- no-direct-DB and API/MCP posture

I want to know whether this layer gives the rest of the corpus a solid boundary foundation.

# 6. Role / overlap audit

Call out any ecosystem doc that:
- overlaps too much with another ecosystem doc
- leaves too much unsaid for its role
- risks becoming a shadow summary instead of real doctrine
- is underlinked or overlinked

Only call out real issues.

# 7. Bounded fixes

Split into:

## Fix now
Real ecosystem-foundation issues worth correcting immediately.

## Fix later
Real but lower-priority improvements.

## Leave alone
Things that may look imperfect but are functioning correctly.

# 8. Final verdict

End by answering:

> Is the ecosystem foundation layer strong enough for the governance and system-specific audits to proceed cleanly?

Then answer:
- yes
- yes, with small cleanup first
- no

And explain why in a short final paragraph.

---

## Important constraints

- This is not the governance spine audit yet.
- This is not the deep Project V / VEDA / V Forge audit yet.
- Do not ask for giant rewrites.
- Do not collapse ecosystem docs and governance docs into one layer.
- Do not drift into implementation-companion detail.
- Do not invent doctrine gaps unless they are real and consequential.
- Prefer bounded fixes over structural churn.

I want a sharp ecosystem-foundation audit, not a general summary.
