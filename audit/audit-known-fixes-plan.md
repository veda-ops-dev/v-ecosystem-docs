# Audit Known Fixes Plan

## Purpose

This document captures the small, known, actionable cleanup plan for audit findings that are understood well enough to fix without more discovery.

It exists to answer:

```text
What audit findings do we already understand clearly enough to fix now or in the next bounded patch pass,
and in what order should they be handled so nothing known is left hanging unnecessarily?
```

This is an audit-support planning artifact.
It is not doctrine.
It is not implementation authority.
It is a disciplined fix list for known issues.

---

## Core Rule

If a finding is:
- clearly understood
- verified or strongly enough grounded by the audit plus repo state
- bounded enough to fix without broad redesign

then it should move onto this plan and be closed deliberately.

If a finding is still ambiguous, underverified, or likely to expand into a broader design question, it belongs in:
- `audit-open-questions-and-followups.md`

This file is for **known fixes**, not open questions.

---

## Status

**Active bounded fix plan.**

Update this file when:
- a known fix is added
- a planned fix is completed
- a fix is intentionally deferred for sequencing reasons

When a fix is completed, mark it clearly.
Do not silently delete it.

---

## Fix sequencing principle

Apply fixes in this order:

1. **governance-seam fixes first**
2. **cross-reference/linkage fixes second**
3. **vocabulary-anchor fixes third**
4. **orientation/quality-of-life fixes fourth**

This order keeps the spine clean before later system-specific audits rely on it.

---

## Known fixes

### 1. Add cautious-default materiality qualifier to `governance/decision-continuity-doctrine.md`

**Status:** planned
**Priority:** now
**Source:** Audit 03

**What to change:**
In the `Stale Approval and Changed Context Rule` section, add the cautious-default sentence already used in `invalidation-and-supersedence-doctrine.md`.

**Bounded fix:**
Add one sentence:

> When materiality is uncertain, the default is to treat the change as potentially material and apply this rule cautiously.

**Why this is a known fix:**
The concept already exists elsewhere in the governance spine.
This is a seam-alignment patch, not a new doctrine invention.

---

### 2. Remove stale `*(planned)*` marker from `governance/failure-and-recovery-doctrine.md`

**Status:** planned
**Priority:** now
**Source:** Audit 03 and prior cleanup pattern

**What to change:**
In `Related Docs`, remove the stale `*(planned)*` marker from the `testing-and-verification-doctrine.md` reference.

**Why this is a known fix:**
The target doc exists.
This is straightforward stale-marker cleanup.

---

### 3. Add doctrine-vs-operational-state cross-reference to `governance/evidence-continuity-model.md`

**Status:** planned
**Priority:** now
**Source:** Audit 03

**What to change:**
In the durability/evidence-loss area, add a short sentence clarifying that durable evidence preservation follows the doctrine-vs-operational-state split and belongs in operational state, not session memory or doc files.

**Suggested patch direction:**
Reference:
- `../ecosystem/doctrine-vs-operational-state.md`

**Why this is a known fix:**
The required doctrine already exists.
This is a missing linkage/clarification patch.

---

### 4. Add finding-report boundary constraint to `interfaces/v-forge-to-project-v-return-to-planning-interface.md`

**Status:** planned
**Priority:** now
**Source:** Audit 03

**What to change:**
Add a short note in the return-to-planning packaging semantics clarifying that execution findings must not be presented as:
- VEDA signal
- governing Project V planning decisions

Also cross-reference:
- `../governance/report-structure-and-required-fields.md`

**Why this is a known fix:**
The constraint already exists in governance.
The interface doc just needs the boundary reminder where the findings cross systems.

---

### 5. Add explicit matrix/approval-model mapping note

**Status:** planned
**Priority:** next pass
**Source:** Audit 03

**What to change:**
Add a short note linking:
- `governance/allowed-agent-actions-matrix.md`
- `governance/approval-and-escalation-model.md`

So the relationship between:
- Permitted / Requires Authorization / Human-Required
and
- Class A / B / C / D

is more explicit.

**Why not in the immediate pass:**
This is useful but not as foundational as the four seam fixes above.
It can be done immediately after the now-priority governance seam pass.

---

### 6. Add `Governance-Sensitive` to `ecosystem/vocabulary.md`

**Status:** planned
**Priority:** next pass
**Source:** Audit 03

**What to change:**
Add a canonical vocabulary entry for governance-sensitive action, based on the shared substance already present in:
- `governance/agent-operating-doctrine.md`
- `governance/approval-and-escalation-model.md`

**Why not in the immediate pass:**
This is a vocabulary-anchor improvement, not a current spine seam blocker.

---

### 7. Clarify the “only durable artifact” condition in `governance/daily-report-doctrine.md`

**Status:** planned
**Priority:** next pass
**Source:** Audit 03

**What to change:**
Add one sentence clarifying when a daily report counts as the only durable artifact from a session.

**Suggested patch direction:**
Clarify that this applies when there are no separate approval records, escalation reports, finding reports, or other governed records persisted independently.

**Why not in the immediate pass:**
This is a precision improvement, but less central than the now-priority seam fixes.

---

### 8. Add `Materiality` to `ecosystem/vocabulary.md`

**Status:** planned
**Priority:** later bounded pass
**Source:** Audit 03

**What to change:**
Add a vocabulary entry for material/materiality and later cross-reference it from the governance docs that currently restate the concept independently.

**Why later:**
This is a good canonicalization improvement, but the immediate seam fix is to patch `decision-continuity-doctrine.md` directly first.

---

## Items intentionally not on this file

The following belong in open-questions/followups, not here:

- `interfaces/data-boundaries.md` role/linkage verification
- provider registry consistency review
- whether `ecosystem-docs-execution-plan.md` should later move/archive
- whether V Forge needs new ADRs
- any remaining `*(planned)*` marker that has not been verified against repo reality

Those are not "known fixes" yet.

---

## Recommended execution order

### Pass A — Governance seam closure
1. `governance/decision-continuity-doctrine.md`
2. `governance/failure-and-recovery-doctrine.md`
3. `governance/evidence-continuity-model.md`
4. `interfaces/v-forge-to-project-v-return-to-planning-interface.md`

### Pass B — Governance model clarity
5. `governance/allowed-agent-actions-matrix.md`
6. `governance/approval-and-escalation-model.md`
7. `governance/daily-report-doctrine.md`

### Pass C — Vocabulary anchors
8. `ecosystem/vocabulary.md` — add `Governance-Sensitive`
9. `ecosystem/vocabulary.md` — add `Materiality`

---

## Success condition

This plan is complete when:
- all now-priority seam fixes are applied
- all next-pass clarity fixes are either applied or intentionally deferred with reason
- no known, understood, bounded fix is left hanging just because it is small

The goal is simple:

**if we know what the fix is, we should either do it or consciously queue it — not leave it vague.**
