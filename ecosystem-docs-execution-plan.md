# V Ecosystem Docs Execution Plan

## Purpose

This document is the authoritative working plan for the V Ecosystem docs refoundation.

It is a **temporary planning aid** — not a doctrine doc.
It exists to answer:

```text
What has been done, what still needs to be done, in what order, by what standards,
so the V Ecosystem docs become a clean and complete authority set for future LLM-led implementation?
```

**This file must be kept current.** After any meaningful writing, review, or patch session, update it.
If this file is stale, the next session will waste time rediscovering current state.

---

## Completion Standard

This execution plan is complete only when all of the following are true:

- the shared docs root contains a clean authority set for the V Ecosystem
- Project V, VEDA, and V Forge all have core authority docs there
- cross-system boundaries are explicit
- governance, reporting, approvals, and continuity are defined
- future new-project onboarding is documented
- archive/bootstrap material is separated from active authority
- a capable LLM could reconstruct the ecosystem from these docs without relying on hidden tribal knowledge

Once all the above are met, this file should be archived or deleted.
It must not remain as a long-term substitute for the real doctrine set.

---

## Authority Model

- `C:\dev\v-ecosystem-docs` — shared docs root, sole authority
- `C:\dev\veda-ops-dev\project-v` — source reference only
- `C:\dev\veda` — source reference only
- `C:\dev\veda-ops-dev\veda` — source reference only

Legacy source repos are temporary migration inputs only.
Anything required to reconstruct, govern, continue, or implement the V Ecosystem after legacy repo deletion must live in `C:\dev\v-ecosystem-docs`.

---

## Current State — CORE AUTHORITY COMPLETE, IMPLEMENTATION-BUILD-SPEC LAYER STILL IN PROGRESS

### What exists right now

```
C:\dev\v-ecosystem-docs
  README.md
  EXTENSION-CODING-README.md
  ecosystem-docs-execution-plan.md
  ecosystem/
    cross-system-boundaries.md
    db-posture.md
    decisions/
      ADR-001-veda-is-pure-observatory.md
      ADR-002-content-graph-moves-to-v-forge.md
      ADR-003-veda-brain-eliminated.md
      ADR-004-mcp-tools-are-thin-wrappers.md
      ADR-005-session-token-model-for-project-scope.md
      ADR-006-hammer-doctrine-is-ecosystem-law.md
      ADR-007-docs-are-build-spec-db-owns-operational-state.md
      ADR-008-one-unified-vscode-extension.md
      ADR-009-no-direct-database-access.md
    doc-template.md
    doctrine-vs-operational-state.md
    external-provider-integration-doctrine.md
    v-ecosystem-overview.md
    vocabulary.md
  governance/
    agent-operating-doctrine.md
    allowed-agent-actions-matrix.md
    approval-and-escalation-model.md
    auth-and-actor-model.md
    daily-report-doctrine.md
    decision-continuity-doctrine.md
    evidence-continuity-model.md
    external-action-governance.md
    failure-and-recovery-doctrine.md
    invalidation-and-supersedence-doctrine.md
    paid-data-pull-governance.md
    recommendation-packaging-doctrine.md
    report-structure-and-required-fields.md
    testing-and-verification-doctrine.md
  interfaces/
    data-boundaries.md
    extension-governance-and-gating-model.md
    extension-human-llm-interaction-model.md
    extension-implementation-architecture.md
    extension-llm-behavior-contract.md
    extension-state-and-context-model.md
    extension-vscode-surface-architecture.md
    mcp-coordination-model.md
    operator-surface-interfaces.md
    project-v-to-v-forge-handoff-interface.md
    v-forge-to-project-v-return-to-planning-interface.md
    veda-to-project-v-signal-interface.md
    veda-to-v-forge-signal-interface.md
  onboarding/
    new-project-access-and-boundary-rules.md
    new-project-admission-checklist.md
    new-project-classification-model.md
    new-project-data-boundary-doctrine.md
    new-project-lifecycle-and-fitment-review.md
    new-project-mcp-integration-doctrine.md
    new-project-onboarding-doctrine.md
    new-project-required-docs.md
  project-v/
    byda-in-project-v.md
    controlled-vocabularies.md
    data-boundaries.md
    decisions/
      ADR-001-separate-databases-per-bounded-system.md
      ADR-002-strict-multi-project-enforcement.md
      ADR-003-governed-schema-and-endpoint-expansion.md
      ADR-004-separate-audit-and-readiness-records.md
    audit-evaluation-rules.md
    github-integration.md
    hammer-doctrine.md
    hammer-plan.md
    implementation-traceability.md
    lifecycle.md
    mcp-surface.md
    multi-project-doctrine.md
    operational-workflow.md
    project-v.md
    readiness-evaluation-rules.md
    readiness-methodology.md
    schema-authority.md
    schema-governance.md
    status-transitions.md
    system-invariants.md
    v-forge-integration.md
  strategy/
    ecosystem-objective-function.md
    opportunity-scoring-model.md
    outcome-evaluation-doctrine.md
    project-thesis-model.md
  v-forge/
    decisions/                        ← intentionally empty (no V Forge-specific ADRs found in source)
    human-in-the-loop-doctrine.md
    operational-model.md
    reporting-and-approval-model.md
    system-invariants.md
    v-forge.md
    vs-project-v.md
    vs-veda.md
  veda/
    data-boundaries.md
    decisions/
      VEDA-001-youtube-observatory-truth-surface.md
    evidence-and-source-provenance.md
    mcp-surface.md
    observability-and-signal-role.md
    operator-surfaces.md
    providers/
      registry.md
    system-invariants.md
    veda.md
  workflows/
    handoff-workflow.md
    launch-readiness-workflow.md
    maintenance-and-replanning-workflow.md
    post-launch-observation-workflow.md
    project-intake-workflow.md
  archive/
    planning-source/
      backlog-fix-pass-plan.md
      process-rules.md
      source-material-index.md
```

---

## Completion Assessment

**The core authority set is complete.**

The original cluster plan is complete:

### Core authority clusters ✅
- all governance docs complete and patched ✅
- all onboarding docs complete and patched ✅
- all cross-system interface docs complete ✅
- all workflow docs complete ✅
- all strategy docs complete ✅
- ADR hygiene done for ecosystem, Project V, and VEDA ✅
- V Forge decisions folder intentionally empty because no source ADRs were found ✅

### Extension doctrine sequence ✅
- `interfaces/extension-llm-behavior-contract.md` ✅
- `interfaces/extension-governance-and-gating-model.md` ✅
- `interfaces/extension-state-and-context-model.md` ✅
- `interfaces/extension-human-llm-interaction-model.md` ✅
- `interfaces/extension-vscode-surface-architecture.md` ✅
- `interfaces/extension-implementation-architecture.md` ✅
- `EXTENSION-CODING-README.md` ✅

### New implementation-build-spec layer work now started ✅
Project V implementation-facing doctrine now has a real first pass:
- `project-v/controlled-vocabularies.md` ✅
- `project-v/status-transitions.md` ✅
- `project-v/readiness-methodology.md` ✅
- `project-v/readiness-evaluation-rules.md` ✅
- `project-v/audit-evaluation-rules.md` ✅
- `project-v/schema-governance.md` ✅
- `project-v/hammer-doctrine.md` ✅
- `project-v/hammer-plan.md` ✅
- `project-v/mcp-surface.md` ✅

---

## What Still Needs To Be Done

The core authority completion standard is met.
What remains is the implementation-build-spec layer and final cleanup needed so coding does not depend on legacy source repos.

### Priority 1 — Finish Project V implementation layer

**Status:** partially complete and now the active next priority.

**Still needed:**

- `project-v/operator-surfaces/vscode-extension.md`
- update `project-v/lifecycle.md` to remove stale `*(planned)*` reference to `byda-in-project-v`
- update `project-v/operational-workflow.md` if stale `*(planned)*` markers remain

**Why this is next:**
Project V is the most complete source system and the highest coding urgency. The controlled vocabularies, status transitions, readiness rules, and audit rules now exist. The remaining operator-surface and stale-marker cleanup should be finished before coding leans on these docs heavily.

---

### Priority 2 — Build VEDA implementation layer

**Status:** still missing the main implementation-build-spec docs.

**Docs to write next after Project V operator surface doc:**

- `veda/observatory-models.md`
- `veda/search-intelligence-layer.md`

**Likely follow-on work:**
- additional VEDA subdomain docs as needed once the observatory/search-intelligence layer is hardened

**Why this matters:**
VEDA has strong doctrine but still needs concrete implementation-shaping docs adapted from source material so observatory behavior and search intelligence are not reconstructed ad hoc.

---

### Priority 3 — Build V Forge implementation layer fresh

**Status:** still largely unwritten at implementation-build-spec level.

**Rule:**
Do not copy old source material because there is no equivalent mature source repo for V Forge.
These docs must be written fresh from ecosystem doctrine and current V Forge role.

**Examples of likely future work:**
- V Forge operator-surface/build-spec docs
- execution package/build-spec docs
- reporting implementation specifics
- hammer/build verification specifics for V Forge

---

### Priority 4 — Provider registries where real integrations exist

The following remain conditional:

- `v-forge/providers/registry.md`
- `project-v/providers/registry.md`

Create these only when concrete provider integrations are admitted through `ecosystem/external-provider-integration-doctrine.md`.

---

## Completion Standard Check

### Core authority completion standard

- ✅ shared docs root contains a clean authority set for the V Ecosystem
- ✅ Project V, VEDA, and V Forge all have core authority docs
- ✅ cross-system boundaries are explicit
- ✅ governance, reporting, approvals, and continuity are defined
- ✅ future new-project onboarding is documented
- ✅ archive/bootstrap material is separated from active authority
- ✅ a capable LLM could reconstruct the ecosystem from these docs

**The original core authority completion standard is met.**

### New implementation sufficiency standard (still in progress)

The next standard is stricter:

- Project V, VEDA, and V Forge must each have enough implementation-build-spec documentation that a developer does not need to reconstruct key enums, state routes, readiness logic, audit logic, observatory models, or operator-surface behavior from legacy repos
- the shared root must be sufficient for continued implementation after legacy source repo deletion

**This second standard is not yet fully met.**
That is the active remaining work.

---

## How to Orient a New Session

### Step 1 — Read these in order
1. `README.md`
2. `ecosystem/v-ecosystem-overview.md`
3. `ecosystem/cross-system-boundaries.md`
4. `ecosystem/vocabulary.md`

### Step 2 — Load governance spine
- `governance/agent-operating-doctrine.md`
- `governance/approval-and-escalation-model.md`
- `governance/decision-continuity-doctrine.md`

### Step 3 — Load system anchor for specific work
- VEDA: `veda/veda.md` + `veda/system-invariants.md`
- V Forge: `v-forge/v-forge.md` + `v-forge/system-invariants.md`
- Project V: `project-v/project-v.md` + `project-v/system-invariants.md`
- Strategy: `strategy/ecosystem-objective-function.md` + `strategy/opportunity-scoring-model.md`

### Step 4 — If doing extension/build work
Read next:
- `EXTENSION-CODING-README.md`
- the six extension docs under `interfaces/` beginning with `extension-llm-behavior-contract.md`

### Step 5 — If doing Project V implementation work
Read next:
- `project-v/controlled-vocabularies.md`
- `project-v/status-transitions.md`
- `project-v/readiness-methodology.md`
- `project-v/readiness-evaluation-rules.md`
- `project-v/audit-evaluation-rules.md`
- `project-v/schema-governance.md`
- `project-v/hammer-doctrine.md`
- `project-v/hammer-plan.md`
- `project-v/mcp-surface.md`

---

## Key Architectural Decisions (Summary)

### Ecosystem-level (9 ADRs in ecosystem/decisions/)
1. VEDA is a pure observatory — telescope mental model governs
2. Content Graph moves to V Forge
3. VEDA Brain eliminated
4. MCP tools are thin wrappers — API is the enforcement layer
5. Session token model — project scope is human-set, server-side bound, LLM-invisible
6. Hammer doctrine is ecosystem law
7. Docs are the build spec — database owns operational state
8. One unified VSCode extension
9. No direct database access

### Project V-level (4 ADRs in project-v/decisions/)
1. Separate databases per bounded system
2. Strict multi-project enforcement
3. Governed schema and endpoint expansion
4. Separate audit and readiness records

### VEDA-level (1 decision in veda/decisions/)
1. YouTube observatory truth surface (vendor SERP primary, API enrichment, UI validation)

---

## Non-Negotiable Writing Rules (for any future doc work)

1. LLM-first, human-second
2. Fresh writing over copy-paste
3. Archive is not authority
4. No empty fake-authority docs
5. Stable vocabulary — extend ecosystem/vocabulary.md before introducing new terms
6. Keep this file current
7. Telescope test for VEDA
8. API-first
9. Shared-root sufficiency beats legacy-repo convenience

---

## Authority Tiers

- **Tier 1** — ecosystem/, governance/, interfaces/, workflows/ docs
- **Tier 2** — project-v/, veda/, v-forge/ core and support docs
- **Tier 3** — implementation-local support that is subordinate to shared-root authority; during refoundation some source material may still live in legacy repos, but anything needed after legacy repo deletion must be promoted into the shared root
- **Tier 4** — archive
