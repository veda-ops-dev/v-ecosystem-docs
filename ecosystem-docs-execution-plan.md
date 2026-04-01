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
- `C:\dev\veda-ops-dev\project-v` — legacy source reference only
- `C:\dev\veda` — legacy source reference only
- `C:\dev\veda-ops-dev\veda` — legacy source reference only

Legacy source repos are temporary migration inputs only.
Anything required to reconstruct, govern, continue, or implement the V Ecosystem after legacy repo deletion must live in `C:\dev\v-ecosystem-docs`.

---

## Current State — CORE AUTHORITY COMPLETE, EXTENSION RUNTIME EXPANSION DOCTRINE COMPLETE, PROJECT V NEAR-MATURE, VEDA MATERIALLY UNDERWAY, V FORGE OPERABILITY WAVE MATERIALLY UNDERWAY

### What exists right now

```text
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
      ADR-010-agent-orchestration-is-an-extension-runtime-capability.md
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
    extension-agent-orchestration-model.md
    extension-governance-and-gating-model.md
    extension-human-llm-interaction-model.md
    extension-implementation-architecture.md
    extension-llm-behavior-contract.md
    extension-memory-and-continuity-model.md
    extension-state-and-context-model.md
    extension-system-init-and-tool-surface-model.md
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
    api/
      objectives.md
      initiatives.md
      work-items.md
      dependencies.md
      handoffs.md
      readiness.md
      audits.md
      evidence-links.md
    decisions/
      ADR-001-separate-databases-per-bounded-system.md
      ADR-002-strict-multi-project-enforcement.md
      ADR-003-governed-schema-and-endpoint-expansion.md
      ADR-004-separate-audit-and-readiness-records.md
    operator-surfaces/
      vscode-extension.md
    api-conventions.md
    audit-evaluation-rules.md
    byda-in-project-v.md
    controlled-vocabularies.md
    data-boundaries.md
    endpoint-governance.md
    github-integration.md
    hammer-coverage-map.md
    hammer-doctrine.md
    hammer-implementation-rules.md
    hammer-plan.md
    implementation-traceability.md
    lifecycle.md
    mcp-surface.md
    multi-project-doctrine.md
    operational-workflow.md
    polymorphic-reference-enforcement.md
    project-v.md
    readiness-evaluation-rules.md
    readiness-methodology.md
    schema-authority.md
    schema-governance.md
    schema-specification.md
    status-transitions.md
    system-invariants.md
    v-forge-integration.md
  strategy/
    ecosystem-objective-function.md
    opportunity-scoring-model.md
    outcome-evaluation-doctrine.md
    project-thesis-model.md
  v-forge/
    content-graph-operations.md
    content-lifecycle-workflow.md
    controlled-vocabularies.md
    decisions/
    execution-intelligence-operations.md
    human-in-the-loop-doctrine.md
    mcp-surface.md
    operational-model.md
    operator-quickstart.md
    release-lifecycle-workflow.md
    reporting-and-approval-model.md
    schema-authority.md
    schema-specification.md
    surface-execution-state-design-note.md
    data-boundaries.md
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
    observatory-models.md
    operator-surfaces.md
    api-contract-principles.md
    providers/
      registry.md
    schema-reference.md
    search-intelligence-layer.md
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

### Core authority clusters ✅
- all governance docs complete and patched ✅
- all onboarding docs complete and patched ✅
- all cross-system interface docs complete ✅
- all workflow docs complete ✅
- all strategy docs complete ✅
- ADR hygiene done for ecosystem, Project V, and VEDA ✅
- V Forge decisions folder intentionally empty because no source ADRs were found ✅

### Extension doctrine and implementation architecture ✅
- `interfaces/extension-llm-behavior-contract.md` ✅
- `interfaces/extension-governance-and-gating-model.md` ✅
- `interfaces/extension-state-and-context-model.md` ✅
- `interfaces/extension-human-llm-interaction-model.md` ✅
- `interfaces/extension-vscode-surface-architecture.md` ✅
- `interfaces/extension-implementation-architecture.md` ✅
- `EXTENSION-CODING-README.md` ✅

### Extension runtime expansion wave — doctrine and integration complete ✅
New runtime doctrine docs written:
- `interfaces/extension-agent-orchestration-model.md` ✅
- `interfaces/extension-memory-and-continuity-model.md` ✅
- `interfaces/extension-system-init-and-tool-surface-model.md` ✅

Companion integration patches completed:
- `ecosystem/vocabulary.md` ✅
- `interfaces/extension-llm-behavior-contract.md` ✅
- `interfaces/extension-governance-and-gating-model.md` ✅
- `interfaces/extension-state-and-context-model.md` ✅
- `interfaces/extension-human-llm-interaction-model.md` ✅
- `interfaces/extension-vscode-surface-architecture.md` ✅
- `interfaces/extension-implementation-architecture.md` ✅
- `governance/agent-operating-doctrine.md` ✅
- `governance/approval-and-escalation-model.md` ✅
- `governance/decision-continuity-doctrine.md` ✅
- `EXTENSION-CODING-README.md` ✅
- `README.md` ✅

Architectural posture locked:
- orchestration is an extension/runtime capability, not a fourth peer ecosystem system ✅
- continuity remains non-authoritative ✅
- delegated work does not create approval or mutation authority ✅
- session tool-surface posture and init-message assembly are now first-class doctrine ✅

### Project V implementation-build-spec layer — near first-pass complete ✅
Core implementation-facing docs:
- `project-v/controlled-vocabularies.md` ✅
- `project-v/status-transitions.md` ✅
- `project-v/readiness-methodology.md` ✅
- `project-v/readiness-evaluation-rules.md` ✅
- `project-v/audit-evaluation-rules.md` ✅
- `project-v/schema-governance.md` ✅
- `project-v/hammer-doctrine.md` ✅
- `project-v/hammer-plan.md` ✅
- `project-v/mcp-surface.md` ✅
- `project-v/schema-specification.md` ✅
- `project-v/polymorphic-reference-enforcement.md` ✅
- `project-v/api-conventions.md` ✅
- `project-v/endpoint-governance.md` ✅
- `project-v/hammer-coverage-map.md` ✅
- `project-v/hammer-implementation-rules.md` ✅
- `project-v/operator-surfaces/vscode-extension.md` ✅

### Project V API family — first pass substantially complete ✅
Eight route family docs written, reviewed, and patched:
- `project-v/api/objectives.md` ✅
- `project-v/api/initiatives.md` ✅
- `project-v/api/work-items.md` ✅
- `project-v/api/dependencies.md` ✅
- `project-v/api/handoffs.md` ✅
- `project-v/api/readiness.md` ✅
- `project-v/api/audits.md` ✅
- `project-v/api/evidence-links.md` ✅

### VEDA implementation-build-spec layer — materially underway
Core spine written and reviewed:
- `veda/schema-reference.md` ✅
- `veda/observatory-models.md` ✅
- `veda/search-intelligence-layer.md` ✅
- `veda/api-contract-principles.md` ✅

Remaining VEDA implementation-build-spec work: see Priority 2 below.

### V Forge implementation-build-spec layer — schema spine complete, operability wave materially underway ✅
Core schema, vocabulary, and boundary docs written, reviewed, and patched:
- `v-forge/v-forge.md` ✅
- `v-forge/schema-authority.md` ✅
- `v-forge/controlled-vocabularies.md` ✅
- `v-forge/schema-specification.md` ✅
- `v-forge/surface-execution-state-design-note.md` ✅
- `v-forge/data-boundaries.md` ✅

Operability wave docs now written:
- `v-forge/mcp-surface.md` ✅
- `v-forge/content-lifecycle-workflow.md` ✅
- `v-forge/release-lifecycle-workflow.md` ✅
- `v-forge/content-graph-operations.md` ✅
- `v-forge/execution-intelligence-operations.md` ✅
- `v-forge/operator-quickstart.md` ✅

**V Forge first-pass scoping is now locked:**
- Two first-class project types: `content_affiliate`, `plugin_product`
- Deeply modeled surfaces: website, GitHub/release
- Lightly tracked surfaces: YouTube, social, newsletter, store listings
- Deferred: experimentation/optimization, SaaS/runtime/commercial, advanced engagement analytics, advanced graph features

**V Forge recognized design thread (not yet first-pass schema):**
Surface execution condition is acknowledged as a real future V Forge pattern.
It is captured in `v-forge/surface-execution-state-design-note.md` and must not be lost or silently pre-built as implementation drift.

---

## What Still Needs To Be Done

The core authority completion standard is met.
What remains is the implementation-build-spec layer needed so coding does not depend on legacy source repos.

### Priority 1 — Remaining Project V implementation-build-spec docs

**Status:** Project V is close to first-pass implementation-build-spec sufficiency. The remaining work is narrow.

**Remaining API family docs (write if needed for coding readiness):**
1. `project-v/api/external-links.md`
2. `project-v/api/research-docs.md`
3. `project-v/api/decision-records.md`
4. `project-v/api/status-history.md`

**Remaining cleanup passes:**
- `project-v/lifecycle.md` — may need stale marker cleanup for `byda-in-project-v.md`
- `project-v/schema-authority.md` — check whether the companion-spec reference to `schema-specification.md` is still marked planned; patch if so
- `project-v/github-integration.md` — likely needs a bounded patch to carry forward the ExternalLink single-table rationale and LLM visibility posture explicitly

---

### Priority 2 — VEDA next implementation-build-spec doc

**Status:** VEDA has a written spine. One major doc is missing before VEDA has sufficient build-spec coverage to support implementation without legacy repo reference.

**Next:**
5. `veda/validation-and-error-taxonomy.md`

**Why next:** `api-contract-principles.md` establishes the 400/422 distinction and error shape posture. The validation/error taxonomy doc is the companion that enumerates what causes each error class across VEDA route families.

**Can wait until later:**
- `veda/observatory/` subdomain docs
- `veda/mcp/` tool-registry and tooling-principles docs

**Important adaptation rule:**
When working from legacy VEDA schema/build-spec material, content graph structures that moved to V Forge must not remain in VEDA authority docs.

---

### Priority 3 — V Forge Operability Wave

**Status:** V Forge operability wave is materially underway and the first execution-operability spine is now written.

Completed workstreams:
- `v-forge/mcp-surface.md` ✅
- `v-forge/content-lifecycle-workflow.md` ✅
- `v-forge/release-lifecycle-workflow.md` ✅
- `v-forge/content-graph-operations.md` ✅
- `v-forge/execution-intelligence-operations.md` ✅
- `v-forge/operator-quickstart.md` ✅

Remaining V Forge operability work:
6. `v-forge/playbooks/` initial content
7. `v-forge/operator-surfaces/vscode-extension.md`
8. `v-forge/hammer-doctrine.md`
9. `v-forge/hammer-plan.md`
10. `v-forge/schema-authority.md` extension hooks section: name surface execution condition as a future extension hook
11. schema cleanup or bounded patch passes as needed after operability review

**Surface execution condition design thread:**
The design note is written. The next deliberate action on this thread is naming surface execution condition as a named extension hook in `v-forge/schema-authority.md`. Do not silently pre-build it.

**Rule:**
Do not copy old source material for V Forge — write from current ecosystem doctrine and the content-graph material that legitimately moved from legacy VEDA source.

---

### Priority 4 — Provider registries where real integrations exist

The following remain conditional:
- `v-forge/providers/registry.md`
- `project-v/providers/registry.md`

Create these only when concrete provider integrations are admitted through `ecosystem/external-provider-integration-doctrine.md`.

---

## Coding Blockers vs Later Work

### No longer blocking (now complete)
- `project-v/schema-specification.md` ✅
- `project-v/polymorphic-reference-enforcement.md` ✅
- `project-v/api-conventions.md` ✅
- `project-v/endpoint-governance.md` ✅
- `project-v/hammer-coverage-map.md` ✅
- `project-v/hammer-implementation-rules.md` ✅
- `project-v/operator-surfaces/vscode-extension.md` ✅
- Project V API family first pass (8 families) ✅
- `veda/schema-reference.md` ✅
- `veda/observatory-models.md` ✅
- `veda/search-intelligence-layer.md` ✅
- `veda/api-contract-principles.md` ✅
- `v-forge/schema-authority.md` ✅
- `v-forge/controlled-vocabularies.md` ✅
- `v-forge/schema-specification.md` ✅
- `v-forge/mcp-surface.md` ✅
- `v-forge/content-lifecycle-workflow.md` ✅
- `v-forge/release-lifecycle-workflow.md` ✅
- `v-forge/content-graph-operations.md` ✅
- `v-forge/execution-intelligence-operations.md` ✅
- `v-forge/operator-quickstart.md` ✅
- extension runtime expansion wave docs and integration patches ✅

### Still blocking coding
- `veda/validation-and-error-taxonomy.md` — blocking VEDA implementation sufficiency

### Should happen soon
- Remaining Project V API family docs if needed for coding readiness
- `v-forge/schema-authority.md` extension hooks section: add surface execution condition as a named hook
- initial V Forge playbooks
- V Forge operator-surface VSCode doc
- V Forge hammer docs

### Can wait until later
- VEDA observatory subdomain docs
- VEDA MCP tool registry/tooling principles
- Surface execution condition governed spec

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

### Extension runtime expansion completion standard
- ✅ architecture decision locked in ADR-010
- ✅ orchestration doctrine written
- ✅ memory and continuity doctrine written
- ✅ system init and tool-surface doctrine written
- ✅ extension doctrine stack patched for integration
- ✅ agent governance doctrine patched for delegation and continuity boundaries
- ✅ control docs and root README reconciled

**The extension runtime expansion doctrine wave is complete.**

### V Forge operability wave completion standard (materially underway)
- ✅ V Forge MCP surface doc written
- ✅ core execution lifecycle docs written
- ✅ content graph operations doc written
- ✅ execution intelligence operations doc written
- ✅ operator quickstart written
- ⏳ playbooks, operator surface, hammer layer, and extension-hook cleanup remain

**The V Forge operability wave is materially underway and no longer at the “next” stage.**

### Implementation sufficiency standard (in progress)
The next standard is stricter:
- Project V, VEDA, and V Forge must each have enough implementation-build-spec documentation that a developer does not need to reconstruct key enums, state routes, readiness logic, audit logic, observatory models, API conventions, endpoint rules, operator-surface behavior, or runtime governance posture from legacy repos
- the shared root must be sufficient for continued implementation after legacy source repo deletion

**Project V is close to first-pass implementation-build-spec sufficiency.**
**VEDA is materially underway.**
**V Forge operability wave is materially underway.**

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
- the extension doctrine stack under `interfaces/`, beginning with `extension-llm-behavior-contract.md`
- `interfaces/extension-agent-orchestration-model.md`
- `interfaces/extension-memory-and-continuity-model.md`
- `interfaces/extension-system-init-and-tool-surface-model.md`

### Step 5 — If doing Project V implementation work
Read the core implementation-build-spec docs:
- `project-v/schema-specification.md`
- `project-v/polymorphic-reference-enforcement.md`
- `project-v/api-conventions.md`
- `project-v/endpoint-governance.md`
- `project-v/controlled-vocabularies.md`
- `project-v/status-transitions.md`
- `project-v/readiness-methodology.md`
- `project-v/readiness-evaluation-rules.md`
- `project-v/audit-evaluation-rules.md`
- `project-v/schema-governance.md`
- `project-v/hammer-doctrine.md`
- `project-v/hammer-plan.md`
- `project-v/hammer-coverage-map.md`
- `project-v/hammer-implementation-rules.md`
- `project-v/mcp-surface.md`
- `project-v/operator-surfaces/vscode-extension.md`

### Step 6 — If doing VEDA implementation work
Read the core VEDA docs first, then the implementation-build-spec spine.
**The active next VEDA write target is `veda/validation-and-error-taxonomy.md`.**

### Step 7 — If doing V Forge implementation work
Read the core V Forge docs first, then the operability spine in this order:
1. `v-forge/v-forge.md`
2. `v-forge/system-invariants.md`
3. `v-forge/operational-model.md`
4. `v-forge/mcp-surface.md`
5. `v-forge/content-lifecycle-workflow.md`
6. `v-forge/release-lifecycle-workflow.md`
7. `v-forge/content-graph-operations.md`
8. `v-forge/execution-intelligence-operations.md`
9. `v-forge/operator-quickstart.md`

Then move to:
- playbooks when they exist
- `v-forge/operator-surfaces/vscode-extension.md` when written
- hammer docs when written

---

## Key Architectural Decisions (Summary)

### Ecosystem-level
1. VEDA is a pure observatory
2. Content Graph moves to V Forge
3. VEDA Brain eliminated
4. MCP tools are thin wrappers
5. Session token model
6. Hammer doctrine is ecosystem law
7. Docs are the build spec
8. One unified VS Code extension
9. No direct database access
10. Agent orchestration is an extension/runtime capability, not a fourth peer system

---

## Non-Negotiable Writing Rules (for any future doc work)

1. LLM-first, human-second
2. Fresh writing over copy-paste
3. Archive is not authority
4. No empty fake-authority docs
5. Stable vocabulary — extend `ecosystem/vocabulary.md` before introducing new terms
6. Keep this file current
7. Telescope test for VEDA
8. API-first
9. Shared-root sufficiency beats legacy-repo convenience

---

## Authority Tiers

- **Tier 1** — ecosystem/, governance/, interfaces/, workflows/ docs
- **Tier 2** — project-v/, veda/, v-forge/ core and support docs
- **Tier 3** — implementation-local support subordinate to shared-root authority
- **Tier 4** — archive
