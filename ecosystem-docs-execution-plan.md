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

## Current State — CORE AUTHORITY COMPLETE, EXTENSION RUNTIME DOCTRINE COMPLETE, NERVE RUNTIME IMPLEMENTATION SPINE STRONG, PROJECT V NEAR-MATURE, VEDA IMPLEMENTATION-BUILD-SPEC SPINE STRONGER, V FORGE OPERABILITY WAVE VERY NEAR FIRST-PASS COMPLETE

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
    extension-compaction-implementation-design.md
    extension-governance-and-gating-model.md
    extension-human-llm-interaction-model.md
    extension-implementation-architecture.md
    extension-llm-behavior-contract.md
    extension-memory-and-continuity-model.md
    extension-state-and-context-model.md
    extension-system-init-and-tool-surface-model.md
    extension-task-lifecycle-implementation-design.md
    extension-token-and-cost-tracking-design.md
    extension-tool-surface-implementation-design.md
    extension-transcript-persistence-design.md
    extension-vscode-surface-architecture.md
    mcp-coordination-model.md
    operator-surface-interfaces.md
    project-v-to-v-forge-handoff-interface.md
    v-forge-to-project-v-return-to-planning-interface.md
    veda-to-project-v-signal-interface.md
    veda-to-v-forge-signal-interface.md
  nerve/
    README.md
    analysis/
      nerve-runtime-pattern-analysis.md
    audits/
      nerve-doctrinal-integration-audit.md
    planning/
      nerve-implementation-ambiguities-checklist.md
      nerve-runtime-harvest-plan.md
      nerve-runtime-roadmap.md
    references/
      nerve-runtime-source-reference.md
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
      external-links.md
      research-docs.md
      decision-records.md
      status-history.md
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
    hammer-doctrine.md
    hammer-plan.md
    human-in-the-loop-doctrine.md
    mcp-surface.md
    operational-model.md
    operator-quickstart.md
    operator-surfaces/
      vscode-extension.md
    playbooks/
      content-update-playbook.md
      new-content-execution-playbook.md
      release-execution-playbook.md
      return-to-planning-playbook.md
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
    validation-and-error-taxonomy.md
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

### Extension runtime expansion wave — doctrine, implementation companions, and integration spine complete ✅
Core runtime doctrine docs written:
- `interfaces/extension-agent-orchestration-model.md` ✅
- `interfaces/extension-memory-and-continuity-model.md` ✅
- `interfaces/extension-system-init-and-tool-surface-model.md` ✅

Implementation companions written:
- `interfaces/extension-compaction-implementation-design.md` ✅
- `interfaces/extension-tool-surface-implementation-design.md` ✅
- `interfaces/extension-token-and-cost-tracking-design.md` ✅
- `interfaces/extension-transcript-persistence-design.md` ✅
- `interfaces/extension-task-lifecycle-implementation-design.md` ✅

Companion integration patches completed:
- `ecosystem/vocabulary.md` ✅
- `interfaces/extension-llm-behavior-contract.md` ✅
- `interfaces/extension-governance-and-gating-model.md` ✅
- `interfaces/extension-state-and-context-model.md` ✅
- `interfaces/extension-human-llm-interaction-model.md` ✅
- `interfaces/extension-vscode-surface-architecture.md` ✅
- `interfaces/extension-implementation-architecture.md` ✅
- `interfaces/extension-memory-and-continuity-model.md` ✅
- `interfaces/extension-system-init-and-tool-surface-model.md` ✅
- `interfaces/extension-agent-orchestration-model.md` ✅
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
- governed compaction, transcript posture, task lifecycle posture, and token/cost visibility now have implementation companions ✅

### Nerve runtime planning / harvest cluster — active implementation-support layer complete ✅
Nerve planning and reference layer written:
- `nerve/README.md` ✅
- `nerve/analysis/nerve-runtime-pattern-analysis.md` ✅
- `nerve/audits/nerve-doctrinal-integration-audit.md` ✅
- `nerve/references/nerve-runtime-source-reference.md` ✅
- `nerve/planning/nerve-runtime-harvest-plan.md` ✅
- `nerve/planning/nerve-runtime-roadmap.md` ✅
- `nerve/planning/nerve-implementation-ambiguities-checklist.md` ✅

Nerve posture locked:
- claw-code is a bounded pattern mine, not an identity donor ✅
- canonical docs remain primary authority ✅
- source-mapped claw-code reference remains secondary mechanical input only ✅
- implementation ambiguities are captured without reopening settled doctrine ✅

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

### Project V API family — first pass complete ✅
Twelve route family docs now written, reviewed, and available:
- `project-v/api/objectives.md` ✅
- `project-v/api/initiatives.md` ✅
- `project-v/api/work-items.md` ✅
- `project-v/api/dependencies.md` ✅
- `project-v/api/handoffs.md` ✅
- `project-v/api/readiness.md` ✅
- `project-v/api/audits.md` ✅
- `project-v/api/evidence-links.md` ✅
- `project-v/api/external-links.md` ✅
- `project-v/api/research-docs.md` ✅
- `project-v/api/decision-records.md` ✅
- `project-v/api/status-history.md` ✅

### VEDA implementation-build-spec layer — materially underway and stronger ✅
Core spine written and reviewed:
- `veda/schema-reference.md` ✅
- `veda/observatory-models.md` ✅
- `veda/search-intelligence-layer.md` ✅
- `veda/api-contract-principles.md` ✅
- `veda/validation-and-error-taxonomy.md` ✅

VEDA now has a substantially stronger implementation-facing API posture for contract behavior and error semantics.

### V Forge implementation-build-spec layer — schema spine complete, operability wave near first-pass complete ✅
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
- `v-forge/operator-surfaces/vscode-extension.md` ✅
- `v-forge/hammer-doctrine.md` ✅
- `v-forge/hammer-plan.md` ✅

Initial playbooks now written:
- `v-forge/playbooks/content-update-playbook.md` ✅
- `v-forge/playbooks/new-content-execution-playbook.md` ✅
- `v-forge/playbooks/release-execution-playbook.md` ✅
- `v-forge/playbooks/return-to-planning-playbook.md` ✅

**V Forge first-pass scoping is now locked:**
- two first-class project types: `content_affiliate`, `plugin_product`
- deeply modeled surfaces: website, GitHub/release
- lightly tracked surfaces: YouTube, social, newsletter, store listings
- deferred: experimentation/optimization, SaaS/runtime/commercial, advanced engagement analytics, advanced graph features

**V Forge recognized design thread (not yet first-pass schema):**
Surface execution condition is acknowledged as a real future V Forge pattern.
It is captured in `v-forge/surface-execution-state-design-note.md` and must not be lost or silently pre-built as implementation drift.

---

## What Still Needs To Be Done

The core authority completion standard is met.
What remains is the implementation-build-spec sufficiency and bounded cleanup layer needed so coding does not depend on legacy source repos.

### Priority 1 — Sync and maintain the execution/control layer

**Status:** active and ongoing

Remaining work:
1. keep `ecosystem-docs-execution-plan.md` synchronized after meaningful doc/runtime-wave changes
2. keep Nerve planning artifacts synchronized with actual implementation progress
3. archive or mark historical planning artifacts aggressively when they stop being live guidance

---

### Priority 2 — Remaining Project V cleanup / coding-readiness review

**Status:** Project V API first pass is now complete. Remaining work is cleanup and coding-readiness review, not major missing families.

Remaining cleanup passes:
4. `project-v/lifecycle.md` — check stale marker posture around `byda-in-project-v.md`
5. `project-v/schema-authority.md` — verify companion/spec references do not still sound planned where already complete
6. `project-v/github-integration.md` — bounded patch for ExternalLink single-table rationale / LLM visibility posture if still needed

---

### Priority 3 — VEDA next implementation-build-spec work

**Status:** VEDA’s immediate validation/error taxonomy blocker is closed. The implementation-build-spec spine is materially stronger.

Next likely VEDA work (not immediate blocker):
7. `veda/observatory/` subdomain docs
8. `veda/mcp/` tool-registry and tooling-principles docs

**Important adaptation rule:**
When working from legacy VEDA schema/build-spec material, content graph structures that moved to V Forge must not remain in VEDA authority docs.

---

### Priority 4 — V Forge bounded cleanup / review passes

**Status:** V Forge operability wave is very near first-pass completion.

Remaining V Forge work:
9. schema cleanup or bounded patch passes as needed after operability review
10. bounded review to ensure playbooks, hammer docs, and operator surface docs remain internally consistent with locked first-pass scoping

**Surface execution condition design thread:**
The design note is preserved and the schema-authority extension-hook posture is explicit. Do not silently pre-build the feature beyond that governed hook posture.

---

### Priority 5 — Conditional provider registries where real integrations exist

The following remain conditional:
- `v-forge/providers/registry.md`
- `project-v/providers/registry.md`

Create these only when concrete provider integrations are admitted through `ecosystem/external-provider-integration-doctrine.md`.

---

### Priority 6 — Higher-risk runtime continuation only after build feedback

**Status:** intentionally deferred

Candidate areas:
11. worker permission bridge
12. worker memory sync
13. session resume posture
14. broader orchestration continuation beyond the current documented second wave

**Rule:**
Do not expand into these just because the runtime docs are exciting.
Use build feedback and real implementation pressure first.

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
- Project V API family first pass (12 families) ✅
- `veda/schema-reference.md` ✅
- `veda/observatory-models.md` ✅
- `veda/search-intelligence-layer.md` ✅
- `veda/api-contract-principles.md` ✅
- `veda/validation-and-error-taxonomy.md` ✅
- `v-forge/schema-authority.md` ✅
- `v-forge/controlled-vocabularies.md` ✅
- `v-forge/schema-specification.md` ✅
- `v-forge/mcp-surface.md` ✅
- `v-forge/content-lifecycle-workflow.md` ✅
- `v-forge/release-lifecycle-workflow.md` ✅
- `v-forge/content-graph-operations.md` ✅
- `v-forge/execution-intelligence-operations.md` ✅
- `v-forge/operator-quickstart.md` ✅
- `v-forge/operator-surfaces/vscode-extension.md` ✅
- `v-forge/hammer-doctrine.md` ✅
- `v-forge/hammer-plan.md` ✅
- initial V Forge playbooks ✅
- V Forge schema-authority extension-hook cleanup ✅
- extension runtime doctrine wave ✅
- extension runtime implementation companions first and second wave ✅
- Nerve runtime planning / source-reference / ambiguity-support layer ✅

### Still blocking coding
- no major single-document blocker is currently called out at the same level as the former VEDA taxonomy gap

### Should happen soon
- Project V bounded cleanup passes
- V Forge bounded cleanup/review passes
- VEDA next implementation-build-spec subdomain work when implementation pressure reaches those areas
- implementation should use `nerve/planning/nerve-implementation-ambiguities-checklist.md` to avoid mistaking bounded ambiguity for missing doctrine

### Can wait until later
- higher-risk runtime continuation areas (worker permission bridge, worker memory sync, resume posture)
- conditional provider registries
- surface execution condition governed spec beyond current design-note posture

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
- ✅ extension runtime implementation companions written
- ✅ extension doctrine stack patched for integration
- ✅ agent governance doctrine patched for delegation and continuity boundaries
- ✅ control docs and root README reconciled

**The extension runtime expansion doctrine + implementation companion wave is complete.**

### Nerve runtime implementation-readiness standard
- ✅ runtime-pattern harvest documented
- ✅ doctrinal audit documented
- ✅ source-mapped claw-code reference documented
- ✅ roadmap documented and synchronized
- ✅ implementation ambiguities checklist documented
- ✅ canonical docs remain the primary authority and the claw-code source is secondary only

**The Nerve runtime implementation-readiness planning layer is complete.**

### V Forge operability wave completion standard
- ✅ V Forge MCP surface doc written
- ✅ core execution lifecycle docs written
- ✅ content graph operations doc written
- ✅ execution intelligence operations doc written
- ✅ operator quickstart written
- ✅ initial practical playbooks written
- ✅ operator surface written
- ✅ hammer doctrine written
- ✅ hammer plan written
- ✅ schema-authority extension-hook cleanup written
- ⏳ only bounded cleanup/review passes remain

**The V Forge operability wave is very near first-pass completion.**

### Implementation sufficiency standard (in progress)
The next standard is stricter:
- Project V, VEDA, and V Forge must each have enough implementation-build-spec documentation that a developer does not need to reconstruct key enums, state routes, readiness logic, audit logic, observatory models, API conventions, endpoint rules, operator-surface behavior, or runtime governance posture from legacy repos
- the shared root must be sufficient for continued implementation after legacy source repo deletion

**Project V is near first-pass implementation-build-spec sufficiency.**
**VEDA implementation-build-spec spine is materially stronger and no longer blocked by the validation/error taxonomy gap.**
**V Forge operability wave is very near first-pass completion.**
**Extension runtime/Nerve implementation-readiness for the documented runtime subset is strong enough for implementation to begin, with bounded ambiguities captured separately.**

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
- `interfaces/extension-compaction-implementation-design.md`
- `interfaces/extension-tool-surface-implementation-design.md`
- `interfaces/extension-token-and-cost-tracking-design.md`
- `interfaces/extension-transcript-persistence-design.md`
- `interfaces/extension-task-lifecycle-implementation-design.md`
- `nerve/planning/nerve-runtime-roadmap.md`
- `nerve/planning/nerve-implementation-ambiguities-checklist.md`
- `nerve/references/nerve-runtime-source-reference.md`

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
Add:
- `veda/api-contract-principles.md`
- `veda/validation-and-error-taxonomy.md`

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
10. `v-forge/playbooks/content-update-playbook.md`
11. `v-forge/playbooks/new-content-execution-playbook.md`
12. `v-forge/playbooks/release-execution-playbook.md`
13. `v-forge/playbooks/return-to-planning-playbook.md`
14. `v-forge/operator-surfaces/vscode-extension.md`
15. `v-forge/hammer-doctrine.md`
16. `v-forge/hammer-plan.md`
17. `v-forge/schema-authority.md`

Then move to:
- remaining bounded cleanup or review passes if needed

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
