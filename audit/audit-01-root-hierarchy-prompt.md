# Audit 01 — Root / Hierarchy / Document-Role Audit Prompt

Use this prompt for the first real Claude audit pass.

---

You are performing a **Root / Hierarchy / Document-Role Audit** of the V Ecosystem docs.

Use the audit posture below and follow it strictly.

[PASTE THE FULL CONTENTS OF `audit-posture.md` HERE]

---

## Audit goal

I want you to audit whether the V Ecosystem docs root is structurally coherent enough that:

- a competent LLM can tell what governs
- a competent implementer can tell what is live vs historical
- planning artifacts do not masquerade as authority
- implementation companions do not masquerade as doctrine
- the docs tree does not create shadow authority or stale execution guidance

This is a **root/hierarchy audit**, not a deep content audit of every individual system.

Do not drift into broad system redesign.
Stay focused on structure, role, hierarchy, staleness, and navigability.

---

## Audit target

Review the root structure and the role of these major clusters:

### Root
- `README.md`
- `EXTENSION-CODING-README.md`
- `ecosystem-docs-execution-plan.md`

### Ecosystem-level roots
- `ecosystem/`
- `governance/`
- `interfaces/`
- `workflows/`
- `onboarding/`
- `strategy/`

### System roots
- `project-v/`
- `veda/`
- `v-forge/`

### Planning / reference / investigation cluster
- `nerve/`

### Archive
- `archive/`

You do **not** need to deep-audit every file in every folder yet.
You are auditing:
- role clarity
- hierarchy clarity
- cross-cluster coherence
- live vs historical posture
- whether the tree is understandable and disciplined

---

## Core questions

Answer these, with specifics:

1. Can a new LLM or engineer tell what the authority hierarchy is?
2. Is the distinction between doctrine, implementation companion, planning, and historical material clear enough?
3. Does the docs root have any shadow-authority risk?
4. Are there stale or misleading planning/control docs still acting too “live”?
5. Is the root navigable enough for implementation-oriented work?
6. Are any top-level docs underlinked, overlinked, or role-confused?
7. Does `nerve/` behave like a bounded support cluster, or is it drifting toward shadow authority?
8. Does `ecosystem-docs-execution-plan.md` now accurately function as a temporary control doc instead of a fake permanent authority doc?

---

## What I want from you

Organize your answer exactly like this:

# 1. Direct judgment

Give a blunt root-level judgment:
- structurally sound
- mostly sound with bounded cleanup needed
- still hierarchy-confused
- or whatever you think is accurate

Explain briefly.

# 2. Authority hierarchy audit

Assess whether the current hierarchy is clear across:
- root docs
- ecosystem/governance/interfaces
- system roots
- Nerve cluster
- archive

Call out any muddy spots.

# 3. Live vs historical audit

Tell me whether the docs tree clearly distinguishes:
- live authority
- implementation support
- planning/control docs
- historical investigation artifacts

Name any files or clusters that still blur this.

# 4. Root navigability audit

Tell me whether a new session could realistically orient itself from the root without unnecessary rediscovery.

Call out:
- strong entry points
- weak entry points
- missing or excessive root-level linkage

# 5. Shadow-authority risk audit

I want a dedicated section on:
- `nerve/`
- `ecosystem-docs-execution-plan.md`
- any other cluster that might accidentally become shadow authority

Be explicit.

# 6. Naming / role confusion audit

Call out any top-level or cluster-level names that are misleading, clunky, or too vague.
Only recommend renames if they are actually worth the churn.

# 7. Bounded fixes

Split into:

## Fix now
Real root/hierarchy issues worth correcting immediately.

## Fix later
Real but lower-priority improvements.

## Leave alone
Things that may look imperfect but are correctly functioning.

# 8. Final verdict

End by answering:

> Is the docs root structurally ready for the deeper layered audits to proceed?

Then answer:
- yes
- yes, with small cleanup first
- no

And explain why in a short final paragraph.

---

## Important constraints

- This is not the ecosystem doctrine audit yet.
- This is not the Project V audit yet.
- This is not the runtime implementation-readiness audit yet.
- Stay at the hierarchy / role / root-control level.
- Do not ask for giant rewrites.
- Do not flatten the difference between doctrine and implementation companion docs.
- Do not recommend deleting planning/history material just because it exists.
- Do not reward “clean aesthetics” over functional hierarchy.

I want a sharp root/hierarchy audit, not a vibes review.
