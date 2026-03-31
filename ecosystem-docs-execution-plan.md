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

- `C:\\dev\\v-ecosystem-docs` — shared docs root, sole authority
- `C:\\dev\\veda-ops-dev\\project-v` — legacy source reference only
- `C:\\dev\\veda` — legacy source reference only
- `C:\\dev\\veda-ops-dev\\veda` — legacy source reference only

Legacy source repos are temporary migration inputs only.
Anything required to reconstruct, govern, continue, or implement the V Ecosystem after legacy repo deletion must live in `C:\\dev\\v-ecosystem-docs`.

---

## Current State — CORE AUTHORITY COMPLETE, PROJECT V NEAR-MATURE, VEDA MATERIALLY UNDERWAY, V FORGE SCHEMA SPINE WRITTEN AND SURFACE EXECUTION CONDITION DESIGN THREAD ACTIVE

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
    api/                              ← ACTIVE — major first-pass API family docs already written
      objectives.md                   ✅
      initiatives.md                  ✅
      work-items.md                   ✅
      dependencies.md                 ✅
      handoffs.md                     ✅
      readiness.md                    ✅
      audits.md                       ✅
      evidence-links.md               ✅
    decisions/
      ADR-001-separate-databases-per-bounded-system.md
      ADR-002-strict-multi-project-enforcement.md
      ADR-003-governed-schema-and-endpoint-expansion.md
      ADR-004-separate-audit-and-readiness-records.md
    operator-surfaces/
      vscode-extension.md             ✅
    api-conventions.md                ✅
    audit-evaluation-rules.md
    byda-in-project-v.md
    controlled-vocabularies.md
    data-boundaries.md
    endpoint-governance.md            ✅
    github-integration.md
    hammer-coverage-map.md            ✅
    hammer-doctrine.md
    hammer-implementation-rules.md    ✅
    hammer-plan.md
    implementation-traceability.md
    lifecycle.md
    mcp-surface.md
    multi-project-doctrine.md
    operational-workflow.md
    polymorphic-reference-enforcement.md  ✅
    project-v.md
    readiness-evaluation-rules.md
    readiness-methodology.md
    schema-authority.md
    schema-governance.md
    schema-specification.md           ✅
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
    controlled-vocabularies.md        ✅  ← NEW: first-pass enum vocabulary, reviewed and patched
    human-in-the-loop-doctrine.md
    operational-model.md
    reporting-and-approval-model.md
    schema-authority.md               ✅  ← NEW: first-pass schema domain and record family authority, reviewed and patched
    schema-specification.md           ✅  ← NEW: concrete first-pass field-level schema spec, reviewed and patched
    surface-execution-state-design-note.md  ✅  ← NEW: design note for deferred surface execution condition pattern (execution condition is the canonical concept name)
    system-invariants.md
    v-forge.md                        ✅  ← strengthened identity layer
    vs-project-v.md
    vs-veda.md
  veda/
    data-boundaries.md
    decisions/
      VEDA-001-youtube-observatory-truth-surface.md
    evidence-and-source-provenance.md
    mcp-surface.md
    observability-and-signal-role.md
    observatory-models.md             ✅
    operator-surfaces.md
    api-contract-principles.md        ✅
    providers/
      registry.md
    schema-reference.md               ✅
    search-intelligence-layer.md      ✅
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

### V Forge implementation-build-spec layer — schema spine now written ✅
Core schema and vocabulary docs written, reviewed, and patched this session:
- `v-forge/v-forge.md` ✅ (strengthened identity layer)
- `v-forge/schema-authority.md` ✅ (7 domains, record families, ownership posture, anti-drift rules)
- `v-forge/controlled-vocabularies.md` ✅ (first-pass enums for all governed fields, reviewed and patched)
- `v-forge/schema-specification.md` ✅ (22 record families, full field-level spec, reviewed and patched)
- `v-forge/surface-execution-state-design-note.md` ✅ (deferred pattern acknowledged and captured)

**V Forge first-pass scoping is now locked:**
- Two first-class project types: `content_affiliate`, `plugin_product`
- Deeply modeled surfaces: website, GitHub/release
- Lightly tracked surfaces: YouTube, social, newsletter, store listings
- Deferred: experimentation/optimization, SaaS/runtime/commercial, advanced engagement analytics, advanced graph features

**V Forge recognized design thread (not yet first-pass schema):**
Surface execution condition — the structured representation of what has been configured, what is missing, and what operational state each owned surface is in — is now acknowledged as a real future V Forge pattern.
It is not first-pass schema. It is captured in `v-forge/surface-execution-state-design-note.md` and must not be lost or silently pre-built as implementation drift.

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

These are the four remaining API families not yet written as first-pass authority docs. Write them if and when their routes are needed for coding. They follow the same admission gate defined in `endpoint-governance.md`.

**Remaining cleanup passes:**
- `project-v/lifecycle.md` — may need stale `*(planned)*` marker cleanup for `byda-in-project-v.md`
- `project-v/schema-authority.md` — check whether the companion-spec reference to `schema-specification.md` is still marked planned; patch if so
- `project-v/github-integration.md` — likely needs a bounded patch to carry forward the ExternalLink single-table rationale and LLM visibility posture explicitly

---

### Priority 2 — VEDA next implementation-build-spec doc

**Status:** VEDA has a written spine (schema-reference, observatory-models, search-intelligence-layer, api-contract-principles). One major doc is missing before VEDA has sufficient build-spec coverage to support implementation without legacy repo reference.

**Next:**

5. `veda/validation-and-error-taxonomy.md`

**Why next:** `api-contract-principles.md` establishes the 400/422 distinction and error shape posture. The validation/error taxonomy doc is the companion that enumerates what causes each error class across VEDA route families — the reference implementers need to build consistent validation behavior without reinventing it per route.

**Can wait until later:**
- `veda/observatory/` subdomain docs
- `veda/mcp/` tool-registry and tooling-principles docs

**Important adaptation rule:**
When working from legacy VEDA schema/build-spec material, content graph structures that moved to V Forge must not remain in VEDA authority docs.

---

### Priority 3 — V Forge remaining implementation-build-spec docs

**Status:** V Forge now has a real schema/build-spec spine. The three core schema docs (schema-authority, controlled-vocabularies, schema-specification) are written, reviewed, and patched. The design note for surface execution-state is also written.

**The remaining V Forge implementation-build-spec work is:**

6. `v-forge/mcp-surface.md`
   — defines the V Forge MCP tool surface: what tools exist, what they do, what they expose, session scoping posture

7. `v-forge/data-boundaries.md`
   — V Forge-specific data ownership boundary rules; companion to the ecosystem-level `interfaces/data-boundaries.md`

**Should happen after those:**

8. Review and patch pass on new V Forge schema docs
   — the schema-authority, controlled-vocabularies, and schema-specification docs are fresh; a structured review pass (similar to what was done this session) should be planned before implementation starts in earnest

9. `v-forge/operator-surfaces/vscode-extension.md`
   — V Forge operator surface for the VSCode extension; analogous to `project-v/operator-surfaces/vscode-extension.md`

10. `v-forge/hammer-doctrine.md` and `v-forge/hammer-plan.md`
    — V Forge hammer layer; deferred until schema docs are stable but should happen before implementation goes far

**Surface execution condition design thread:**
The design note is written. The next deliberate action on this thread is either:
- updating `v-forge/schema-authority.md` to name surface execution condition as a named extension hook (currently the extension hooks section names "Deep YouTube metadata" but not this broader pattern)
- or leaving it in the design note until surface-specific feature vocabularies are researched and a governed spec pass is warranted

Do not let this thread disappear. Do not silently pre-build it.

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

### Still blocking coding

- `veda/validation-and-error-taxonomy.md` — blocking VEDA implementation sufficiency
- `v-forge/mcp-surface.md` — blocking V Forge MCP tool implementation
- `v-forge/data-boundaries.md` — blocking V Forge data boundary enforcement implementation

### Should happen soon

- Remaining Project V API family docs if needed for coding readiness (external-links, research-docs, decision-records, status-history)
- Review/patch pass on new V Forge schema docs before implementation begins in earnest
- `v-forge/schema-authority.md` extension hooks section: add surface execution-state as a named hook

### Can wait until later

- VEDA observatory subdomain docs
- VEDA MCP tool registry/tooling principles
- V Forge operator-surface VSCode doc
- V Forge hammer docs
- Surface execution-state governed spec (deferred until feature vocabularies are researched per surface type)

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

### Implementation sufficiency standard (in progress)

The next standard is stricter:

- Project V, VEDA, and V Forge must each have enough implementation-build-spec documentation that a developer does not need to reconstruct key enums, state routes, readiness logic, audit logic, observatory models, API conventions, endpoint rules, or operator-surface behavior from legacy repos
- the shared root must be sufficient for continued implementation after legacy source repo deletion

**Project V is close to first-pass implementation-build-spec sufficiency.**
Project V schema, polymorphic enforcement, API conventions, endpoint governance, all major first-pass API family docs, hammer coverage, and the VSCode operator surface are now written.
The remaining Project V gap is the four remaining API family docs (external-links, research-docs, decision-records, status-history), which should be written on demand as coding needs them.

**VEDA is materially underway.**
The VEDA implementation-build-spec spine — schema-reference, observatory-models, search-intelligence-layer, api-contract-principles — is written and reviewed. The next missing doc is `veda/validation-and-error-taxonomy.md`.

**V Forge is no longer the untouched frontier.**
V Forge now has a real implementation-build-spec spine: strengthened identity, schema authority, controlled vocabularies (reviewed and patched twice), and a concrete 22-record-family schema specification (reviewed and patched). First-pass scoping is locked. The design note for the surface execution condition pattern is written.
The remaining V Forge gaps are mcp-surface, data-boundaries, a schema-doc review pass, the operator-surface doc, and the hammer layer.

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

Then load specific API family docs as needed from `project-v/api/`.

The active next Project V work is the remaining four API family docs (external-links, research-docs, decision-records, status-history) on demand as coding requires them, plus bounded cleanup patches to schema-authority, github-integration, and lifecycle.

### Step 6 — If doing VEDA implementation work
Read the core VEDA docs first:
- `veda/veda.md`
- `veda/system-invariants.md`
- `veda/data-boundaries.md`
- `veda/observability-and-signal-role.md`
- `veda/evidence-and-source-provenance.md`

Then load the implementation-build-spec spine:
- `veda/schema-reference.md`
- `veda/observatory-models.md`
- `veda/search-intelligence-layer.md`
- `veda/api-contract-principles.md`

**The active next VEDA write target is `veda/validation-and-error-taxonomy.md`.**

### Step 7 — If doing V Forge implementation work
Read the core V Forge docs first:
- `v-forge/v-forge.md`
- `v-forge/system-invariants.md`
- `v-forge/operational-model.md`

Then load the implementation-build-spec spine:
- `v-forge/schema-authority.md`
- `v-forge/controlled-vocabularies.md`
- `v-forge/schema-specification.md`

Also read the design note if surface/execution-state work is on the agenda:
- `v-forge/surface-execution-state-design-note.md`

**The active next V Forge write targets are `v-forge/mcp-surface.md` and `v-forge/data-boundaries.md`.**

These are now the V Forge implementation blockers. Schema, vocabulary, and field-level spec are done.
Do not treat schema authority or schema spec as still missing — they are written.

**Surface execution condition design thread:** The design note is written and must be preserved. The next deliberate action on this thread is adding surface execution condition as a named extension hook in `v-forge/schema-authority.md`. Do not silently pre-build it into schema before that governed step.

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

### V Forge scope decisions (locked in schema-authority and schema-specification)
- Two first-class project types: content_affiliate, plugin_product
- Deeply modeled surfaces: website, GitHub/release
- Lightly tracked surfaces: YouTube, social, newsletter, store listings
- Deferred: experimentation/optimization, SaaS/runtime/commercial

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
