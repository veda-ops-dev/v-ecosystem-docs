# Audit Open Questions and Follow-Ups

## Purpose

This document captures the questions, possible drift points, and follow-up checks surfaced during the layered audit program that should not be forgotten, rushed, or silently assumed resolved.

It exists to answer:

```text
What audit findings or uncertainties still need verification,
what should be revisited in later audit phases,
and what should not be treated as settled just because it was noticed once?
```

This is an audit-support artifact.
It is not doctrine.
It is not implementation authority.
It is a running checklist for unresolved or deferred audit questions.

---

## Core Rule

Do not convert an audit suspicion into a repo change unless the issue is verified.

Do not forget a real open question just because the current cleanup pass chose not to touch it.

This file exists to preserve discipline between:
- things already fixed
- things clearly wrong but deferred
- things still needing verification
- things better handled in later system-specific audits

---

## Status

**Active follow-up list.**

Update this file when:
- an audit surfaces a real but deferred question
- a cleanup pass intentionally leaves an item untouched pending verification
- a later audit resolves or closes an open question

When an item is resolved, mark it clearly rather than silently deleting history.

---

## Open questions and follow-ups

### 1. `interfaces/data-boundaries.md` — role and linkage still need verification

**Current status:** open

**Why it is here:**
The root/hierarchy audit flagged `interfaces/data-boundaries.md` as possibly underlinked or orphaned relative to:
- `ecosystem/cross-system-boundaries.md`
- `project-v/data-boundaries.md`
- `veda/data-boundaries.md`
- `v-forge/data-boundaries.md`

**What needs checking:**
- what unique role this file plays
- whether it duplicates broader ecosystem boundary docs
- whether it duplicates system-local boundary docs
- whether it needs stronger linkage from root/interface docs

**Suggested handling:**
Resolve during a later audit or a bounded verification pass, not by guessing.

---

### 2. Provider registry posture still needs a consistency check

**Current status:** open

**Why it is here:**
The audit raised a possible tension between:
- `ecosystem/external-provider-integration-doctrine.md`
- the execution plan's “conditional provider registries” language
- the fact that `veda/providers/registry.md` already exists

**What needs checking:**
- whether the doctrine language and execution-plan language are still aligned
- whether VEDA’s provider registry is live, partial, or placeholder
- whether provider-registry expectations should be clarified at root or system level

**Suggested handling:**
Treat this as a later ecosystem/veda audit item, not a cleanup-pass guess.

---

### 3. `ecosystem-docs-execution-plan.md` — still temporary, not yet archived

**Current status:** intentionally deferred

**Why it is here:**
The root audit argued this file may eventually need to move out of root or be archived. We explicitly chose **not** to do that yet because the file is still actively useful as a control doc during the remaining cleanup/build-readiness phase.

**What needs checking later:**
- whether the remaining work tracked in the execution plan is actually finished
- whether the file still adds control value or has become mostly historical
- whether a shorter control file or archive move becomes the better posture

**Suggested handling:**
Revisit after the next major audit/fix waves, not now.

---

### 4. V Forge ADR gap — valid architectural question, not root-cleanup work

**Current status:** deferred to later audit phase

**Why it is here:**
The root audit suggested V Forge may need one or more ADRs for first-pass scope lock decisions, including:
- first-class project types
- deeply vs lightly modeled surfaces
- explicitly deferred domains

**What needs checking:**
- whether the current V Forge docs already preserve this strongly enough without an ADR
- whether a bounded ADR would materially improve durability and anti-drift posture
- whether this is best resolved during the V Forge authority/operability audit

**Suggested handling:**
Do not treat this as a root-layer issue. Revisit during the V Forge audit.

---

### 5. `workflows/project-intake-workflow.md` still contains a `*(planned)*` reference that needs verification

**Current status:** open

**Why it is here:**
The cleanup pass intentionally did **not** remove all `*(planned)*` markers blindly. One example left in place was:
- `../strategy/opportunity-scoring-model.md` *(planned)*

**What needs checking:**
- whether the linked doc now exists in a finished enough form
- whether the planned marker is still accurate
- whether any remaining planned markers in workflow docs are real or stale

**Suggested handling:**
Handle in a later verification pass or during the ecosystem/strategy audit.

---

### 6. Return/finding-report cross-link may still deserve a small strengthening patch

**Current status:** open but low urgency

**Why it is here:**
The audit noted that the finding-report constraint in `governance/report-structure-and-required-fields.md` may be stronger if surfaced more explicitly in return-to-planning/finding-relevant docs.

**What needs checking:**
- whether current cross-linking is already sufficient after cleanup
- whether a small explicit reference in the return-to-planning interface would reduce misread risk

**Suggested handling:**
Review during the cross-system interface audit.

---

### 7. `README.md` root orientation was improved, but should be re-evaluated after later audits

**Current status:** open for later review

**Why it is here:**
The cleanup pass strengthened root authority structure by adding:
- strategy authority visibility
- nerve visibility
- a clearer tier model

**What needs checking later:**
- whether root orientation remains sufficient after more audit artifacts accumulate
- whether `audit/` itself should eventually be listed in the root README
- whether root entry points need refinement after deeper ecosystem/governance/system audits

**Suggested handling:**
Revisit after several audit phases are complete.

---

## Recently resolved items

### A. Governance `.tmp` patch artifacts

**Status:** resolved

Removed:
- `governance/testing-hammer-corrected-sections.tmp`
- `governance/testing-hammer-sections-patch.tmp`
- `governance/testing-veda-hammer-patch.tmp`

---

### B. Confirmed stale `*(planned)*` markers in key interface/governance docs

**Status:** resolved

Cleaned in confirmed cases where target docs existed.

---

### C. Missing `nerve/` visibility in root orientation

**Status:** resolved

Root `README.md` now includes `nerve/` as a runtime support layer.

---

### D. Strategy authority visibility at root

**Status:** resolved

Root `README.md` now gives strategy an explicit authority role.

---

## Usage

Use this file when:
- deciding what audit item to verify next
- preserving deferred audit questions between sessions
- preventing accidental loss of unresolved review concerns
- deciding what belongs in a later audit phase instead of the current cleanup pass
