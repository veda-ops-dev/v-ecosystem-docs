# Transition Plan — VedaOps Authority Sync

## Purpose

This document defines the controlled sequence for aligning the VedaOps
documentation authority to the current architecture direction.

This is not an implementation plan.
This is a documentation authority correction plan.

A future LLM reading this document should be able to determine immediately:
- what the current architecture direction is
- what phase the transition is in
- what has already been settled
- what batch to execute next
- what must not be done all at once

---

## Current Architecture Direction (Settled — Do Not Reopen)

### System map

| System | Role |
|---|---|
| Project V | Planning truth |
| VEDA | Observatory truth |
| VEDA Strategy | Derived strategic intelligence |
| V Forge | Execution truth |

### Database posture

- 1 physical Postgres database
- 4 schemas with strict logical separation
- `project_v.*` — owned by Project V
- `veda.*` — owned by VEDA
- `veda_strategy.*` — owned by VEDA Strategy
- `v_forge.*` — owned by V Forge
- Logical boundaries enforced by: schema ownership, DB roles, service-layer
  boundaries, MCP/tool boundaries
- Physical consolidation does not imply conceptual merger
- No cross-schema convenience queries or shared truth

### Retrieval and blob posture

- Postgres is canonical truth
- Qdrant is retrieval support only — must not become shadow truth
- Retrieval must resolve back to canonical Postgres records
- Qdrant doctrine must be governed by a dedicated architecture doc after the
  Postgres+Qdrant research has been reviewed (see Batch I)
- Local blob storage now; must map cleanly to future R2/bucket posture

### VEDA posture

- VEDA is observatory-only — no scoring, no gap detection, no clustering
- Firecrawl belongs in VEDA as an observatory provider
- DataForSEO AI Optimization belongs in VEDA as an observatory provider
- Pre-project observability is required — observation does not require an
  existing project
- Key concepts to formalize: `observatory_scope`, `topic_monitor`
- Raw AI-surface observability (mentions, citations, fan-out queries, brand
  entities, surface metadata) belongs in VEDA; derived interpretation later
  belongs in VEDA Strategy

---

## Current Transition Status

**Phase: Branch carries landed documentation work through Batch G, partial Batch H, verified Batch J, and a same-day cleanup set — pending human review and remaining Batch H residual doctrine work.**

The following has been done on branch `docs/batch-h-firecrawl-provider-governance`:
- Full spec-doc context read across all Tier 1 and Tier 2 authority docs
- Transition review and diagnosis pass completed
- Transition plan corrected (this document)
- Qdrant+Postgres architecture research prompt executed (output to be
  uploaded as reference material — not stored in this repo)
- Batch A docs landed: `ecosystem/v-ecosystem-overview.md` and
  `ecosystem/cross-system-boundaries.md` updated with VEDA Strategy as
  the fourth governed system
- Batch B docs landed: `ecosystem/db-posture.md` rewritten for single-Postgres/
  four-schema posture; `interfaces/data-boundaries.md` updated with VEDA Strategy
  ownership map entry; `ecosystem/decisions/ADR-012-single-postgres-multi-schema.md`
  created
- Batch C docs landed: `ecosystem/ecosystem-schema-spine.md` updated with
  `veda_strategy` in canonical enumerations and with first-pass VEDA Strategy
  entity coverage
- Batch D docs landed: `veda-strategy/veda-strategy.md`,
  `veda-strategy/data-boundaries.md`, and `veda-strategy/schema-authority.md`
  created
- Batch E docs landed: `veda/veda.md`, `veda/system-invariants.md`, and
  `veda/observability-and-signal-role.md` updated to name VEDA Strategy as the
  governed destination for non-observatory capabilities
- Batch F stubs landed: `interfaces/veda-strategy-to-project-v-signal-interface.md`
  and `interfaces/veda-strategy-to-v-forge-signal-interface.md` created
- Batch G docs landed: `project-v/project-v.md` updated with VEDA Strategy
  relationship section and updated Related Docs; `workflows/project-intake-workflow.md`
  tightened so that VEDA Strategy-originated signals are explicitly named as entering
  intake through the governed VEDA Strategy → Project V interface under Trigger Type B
- Firecrawl admitted into `veda/providers/registry.md` as an active observatory
  provider with supporting provider/admission docs in `veda/providers/`
- Firecrawl transition-support baseline capture is now documented under
  `transition-steward/firecrawl/`, including a direct API baseline sample,
  Playground comparison artifacts, a primary inventory note, and folder README
  clarifying raw API shape versus Playground wrapper shape
- DataForSEO AI Optimization admitted into `veda/providers/registry.md` as an
  active observatory provider; raw AI-surface observability is now explicitly
  classified as VEDA input rather than VEDA Strategy logic
- Batch H partial posture landed: `veda/data-boundaries.md` updated with bucket/
  snapshot storage posture for large Firecrawl captures; `veda/schema-reference.md`
  updated to formalize `observatory_scope`, `topic_monitor`, crawled page
  observability families, and AI-surface observability families as
  deferred-but-owned VEDA model families with an explicit no-ad-hoc-tables rule
- Batch J verified complete: all four `strategy/*` docs already carry
  `system: veda_strategy`; root `README.md` strategy section already reflects
  VEDA Strategy as the authority-owning system; no file changes were required
- Same-day cleanup set landed:
  - `project-v/decisions/ADR-001-separate-databases-per-bounded-system.md`
    status updated to Superseded by ADR-012; supersession notice added;
    ADR-012 added to Related Docs
  - `ecosystem/vocabulary.md` updated with VEDA Strategy as a canonical term
    entry parallel to the other three system entries
  - `v-forge/v-forge.md` updated with a Relationship to VEDA Strategy section
    and the VEDA Strategy → V Forge interface added to Related Docs
  - `veda/observatory-models.md` Anti-Drift Rule 3 corrected to name VEDA
    Strategy as the first-named governed destination for derived strategic
    intelligence types (opportunity scoring, gap detection, clustering,
    competitive analysis) rather than routing them generically to
    "Project V or V Forge"
  - `veda/search-intelligence-layer.md` Rule 6 and Rule 7 corrected with the
    same destination fix and with an explicit acknowledgment of the governed
    VEDA → VEDA Strategy read path

The following remains unfinished or not yet human-accepted:
- None of the landed work has been marked human-reviewed and accepted yet
- Batch H remains partial: Firecrawl admission, transition-support baseline
  capture, bucket/blob posture, and deferred-but-owned schema family posture
  are all landed; remaining Batch H work is the governed doctrine design for
  the Firecrawl capture families and AI-surface observability families in
  `veda/schema-reference.md` — exact family design is not yet settled and
  requires a governed schema design pass, not a text edit
- Batch I remains blocked on external research review
- Batch K remains deferred

**Next action:** Human reviews the branch state and accepts or corrects the landed work. After transition-control truth is synced to reality, complete remaining Batch H schema design work before Batch I or K.

---

## Core Transition Objectives

1. Lock the four-system ecosystem map in all Tier 1 docs
2. Correct database posture docs from multi-database to single-Postgres/four-schema
3. Introduce VEDA Strategy as a first-class governed system with identity docs
4. Add VEDA Strategy to all cross-system enumerations and ownership maps
5. Correct VEDA docs: name VEDA Strategy as destination for non-observatory capabilities
6. Correct Project V docs: Project V consumes strategy signals, does not generate them
7. Create VEDA Strategy interface stubs for signal routing to Project V and V Forge
8. Formalize pre-project observability concepts in VEDA docs
9. Add Firecrawl and DataForSEO AI Optimization to VEDA provider governance and
   classify what they settle now vs. what remains deferred
10. Promote Qdrant doctrine into a governed infrastructure posture doc
11. Clean up strategy/* system field and align with VEDA Strategy identity

---

## Batch Structure

Each batch maps to one git branch and one reviewable PR.
No batch should touch docs outside its defined scope.
Batches A through C must complete before any system-level doc work begins.

---

### Batch A — Four-System Ecosystem Map
**Branch:** `docs/transition-batch-a-four-system-ecosystem-map`
**Status:** Landed on current branch — pending human review

Docs:
- `ecosystem/v-ecosystem-overview.md`
- `ecosystem/cross-system-boundaries.md`

Changes:
- Add VEDA Strategy as the fourth core system in the ecosystem overview
- Add VEDA Strategy ownership section to cross-system-boundaries
- Define what VEDA Strategy owns (scoring, gap detection, clustering,
  competitive analysis, strategic signals) and does not own
- Clarify boundary between V Forge execution-side gap detection and VEDA
  Strategy content gap detection — these are different things
- Update related docs lists in both files

**Why first:** Every downstream doc that currently says "belongs in Project V or
V Forge, not VEDA" is pointing at the wrong target. Until VEDA Strategy exists
in the ecosystem overview, all subsequent corrections reference a ghost system.

---

### Batch B — Database Posture Correction
**Branch:** `docs/transition-batch-b-database-posture-correction`
**Status:** Landed on current branch — pending human review

Docs:
- `ecosystem/db-posture.md` — rewrite
- `interfaces/data-boundaries.md` — update ownership map
- `ecosystem/decisions/ADR-012-single-postgres-multi-schema.md` — new file

Changes:
- Rewrite `db-posture.md`: replace all multi-database language with
  single-physical-Postgres/multi-schema posture; add `veda_strategy` schema;
  update enforcement language from credential-database isolation to
  role-based schema isolation; preserve all ownership doctrine
- Update `interfaces/data-boundaries.md`: add `veda_strategy` to canonical
  ownership map; update persistence-layer ownership language
- Create `ADR-012`: document the single-database/multi-schema decision,
  explicitly supersede the prior multi-database posture that was described
  in `db-posture.md` as prose doctrine (no prior ADR existed for it)

**Note on ADR-001:** `project-v/decisions/ADR-001-separate-databases-per-bounded-system.md`
exists and has been updated in the same-day cleanup set: its status is now
Superseded by ADR-012 and a supersession notice has been added. The historical
content is preserved. ADR-012 governs the current posture.

**Why second:** The db-posture doc is the most actively misleading doc in the
repo. Every LLM that reads it picks up multi-database posture as current doctrine.
Must be corrected before schema or system docs reference it.

---

### Batch C — Schema Spine Enumeration Updates
**Branch:** `docs/transition-batch-c-schema-spine-enumerations`
**Status:** Landed on current branch — pending human review

Docs:
- `ecosystem/ecosystem-schema-spine.md`

Changes:
- Add `veda_strategy` to the `actor_system` canonical enumeration
- Add VEDA Strategy entity types to the `entity_type` canonical table
- Update the owning-system column for any entity types that VEDA Strategy
  will own once its schema authority doc exists
- Update related docs list

**Why third:** `ecosystem-schema-spine.md` defines the canonical enumerations
that all system schema authority docs must be consistent with. No system-level
schema work for VEDA Strategy can proceed before its system appears in these
enumerations. This is a prerequisite for Batch D.

---

### Batch D — VEDA Strategy System Introduction
**Branch:** `docs/transition-batch-d-veda-strategy-introduction`
**Status:** Landed on current branch — pending human review

New files to create:
- `veda-strategy/veda-strategy.md` — identity doc
- `veda-strategy/data-boundaries.md` — what it owns, reads, must not absorb
- `veda-strategy/schema-authority.md` — stub: `veda_strategy.*` schema posture,
  owned record families (scoring outputs, gap signals, cluster records)

Changes:
- `veda-strategy/veda-strategy.md`: role, owns, does not own, relationships
  to VEDA / Project V / V Forge; modeled on `veda/veda.md` structure
- `veda-strategy/data-boundaries.md`: VEDA Strategy reads from `veda.*` but
  does not own observatory truth; produces derived intelligence records in
  `veda_strategy.*`; must not duplicate VEDA canonical records
- `veda-strategy/schema-authority.md`: first-pass stub covering owned record
  families; no implementation detail required yet

**Why this order:** System identity docs must exist before VEDA docs can name
VEDA Strategy as a destination and before interface stubs can reference it.

---

### Batch E — VEDA Docs Narrow Correction
**Branch:** `docs/transition-batch-e-veda-docs-narrow-correction`
**Status:** Landed on current branch — pending human review

Docs (targeted additions only — these docs are already well-aligned):
- `veda/veda.md`
- `veda/system-invariants.md`
- `veda/observability-and-signal-role.md`

Changes:
- `veda/veda.md`: update "Does Not Own" section to name VEDA Strategy
  explicitly as the destination for scoring, gap detection, clustering,
  competitive analysis
- `veda/system-invariants.md`: Invariant 6 (VEDA Brain Does Not Exist)
  should name VEDA Strategy as the correct governed destination for those
  capabilities; update related docs reference
- `veda/observability-and-signal-role.md`: update "What VEDA Does Not Do"
  section to name VEDA Strategy by name rather than just "Project V or V Forge"
- Update VEDA docs to recognize DataForSEO AI Optimization as observatory input
  for raw AI-surface behavior, not embedded interpretation logic

**Scope note:** Do not rewrite these docs. They are already the best-specified
boundary docs in the repository. Only add the explicit VEDA Strategy references
where "belongs elsewhere" currently has no named destination, and add only the
minimum DataForSEO AI Optimization recognition needed to preserve observatory posture.

---

### Batch F — VEDA Strategy Interface Stubs
**Branch:** `docs/transition-batch-f-veda-strategy-interface-stubs`
**Status:** Landed on current branch — pending human review

New files to create:
- `interfaces/veda-strategy-to-project-v-signal-interface.md` — stub
- `interfaces/veda-strategy-to-v-forge-signal-interface.md` — stub

Changes:
- Create governance stubs for how scored opportunity signals and strategic
  signals flow from VEDA Strategy to Project V and V Forge respectively
- Stubs must define: access model, signal ownership rule, what the package
  does not provide, boundary rule; full specification deferred to Batch K
- Update `interfaces/data-boundaries.md` interface list to include these
  as governed stubs

**Scope note:** These are stubs, not full interface contracts. Full
specification of these interfaces is deferred to Batch K. The stubs must
exist so that Batch G (Project V correction) has a named governed path to
reference.

---

### Batch G — Project V and Intake Workflow Corrections
**Branch:** `docs/transition-batch-g-project-v-intake-workflow`
**Status:** Landed on current branch — pending human review

Docs:
- `project-v/project-v.md`
- `workflows/project-intake-workflow.md`

Changes:
- `project-v/project-v.md`: add VEDA Strategy relationship section; Project V
  consumes scored opportunity signals from VEDA Strategy, does not generate
  them; update related docs list
- `workflows/project-intake-workflow.md`: clarify how VEDA Strategy-originated
  signals enter intake (as operator/strategy trigger or as a signal delivery
  from VEDA Strategy through its governed interface stub); no workflow
  structural rewrite required

**Scope note:** `project-v/data-boundaries.md` and `project-v/schema-authority.md`
are already well-aligned and do not need changes in this batch. Touch only
the identity doc and intake workflow.

---

### Batch H — VEDA Infrastructure: Firecrawl, Blob, Pre-Project Observability
**Branch:** `docs/transition-batch-h-veda-infrastructure`
**Status:** Partially landed on current branch — provider admission and Firecrawl baseline sample-governance artifacts are present, pending human review and residual doctrine work

Docs:
- `veda/providers/registry.md`
- `veda/schema-reference.md`
- provider docs under `veda/providers/`

Changes:
- `veda/providers/registry.md`: add Firecrawl as an admitted observatory
  provider after completing the admission process defined in
  `ecosystem/external-provider-integration-doctrine.md`; include
  classification, data supplied, trust posture, spend posture, approval
  posture, status, admitted date
- Keep DataForSEO AI Optimization admitted in the registry and use this batch to
  clarify what that admission settles now vs. what remains deferred at schema
  and strategy layers
- Transition-support evidence now exists under `transition-steward/firecrawl/`
  for one direct API baseline scrape plus paired Playground artifacts; use
  those artifacts to ground the remaining Firecrawl doctrine work rather than
  infer structure from vendor docs or UI behavior alone
- `veda/schema-reference.md`: formalize `observatory_scope` and `topic_monitor`
  as deferred-but-owned model families required for pre-project observability;
  specify they must not receive ad hoc tables before governed family design
- Add first-pass VEDA schema/reference posture for Firecrawl page-capture
  families and AI-surface observability, including what belongs in canonical
  observatory truth versus raw/archive capture, while keeping exact
  normalization and downstream derivation conservative
- Blob/page-capture posture: add doctrine note on local blob storage posture
  and R2/bucket compatibility requirement; home is `veda/data-boundaries.md`
  or a new infrastructure posture doc depending on scope

**Prerequisite:** Firecrawl admission requires completing the provider
admission process — this batch cannot fully close until that process runs.
The registry entry is the output of that process, not a shortcut around it.
DataForSEO AI Optimization has already been admitted; this batch handles its
follow-on doctrine implications rather than re-admitting it.

---

### Batch I — Qdrant Doctrine Promotion
**Branch:** `docs/transition-batch-i-qdrant-doctrine-promotion`
**Status:** Blocked — awaiting Qdrant+Postgres research output review

Docs:
- New: `ecosystem/retrieval-infrastructure-posture.md`

Changes:
- After the Postgres+Qdrant research output has been reviewed, distill the
  governing rules into a new Tier 1 ecosystem doc that establishes:
  Qdrant-as-retrieval-support-only posture, ID-only vector storage pattern,
  canonical resolution requirement, per-schema collection ownership rules,
  cross-system retrieval boundary enforcement
- Update `ecosystem/db-posture.md` related docs list to reference this doc
- This doc becomes the single authority for Qdrant integration posture;
  nothing about Qdrant integration should be embedded in system-specific
  docs before this exists

**Why deferred:** The research output has not yet been reviewed and promoted.
Do not write Qdrant doctrine from memory or assumption. Wait for the research
material to be supplied as reference.

---

### Batch J — Strategy Folder System Field and README Cleanup
**Branch:** `docs/transition-batch-j-strategy-folder-cleanup`
**Status:** Verified complete — all four strategy docs already carry `system: veda_strategy`; README `strategy/` section already reflects VEDA Strategy as the authority-owning system; no file changes required

Docs:
- `strategy/ecosystem-objective-function.md`
- `strategy/opportunity-scoring-model.md`
- `strategy/outcome-evaluation-doctrine.md`
- `strategy/project-thesis-model.md`
- `README.md` (repo root)

Changes:
- Update `system:` field in all four strategy files from `strategy` to
  `veda_strategy` to align with the governed system name established in Batch D
- Update `README.md` strategy authority section: reflect VEDA Strategy as
  a Tier 2 system authority folder, not a free-floating strategy doc cluster

**Why last among cleanup:** These files are usable as-is during the earlier
batches. The system field correction is bookkeeping, not architecture.
Do not do this before Batch D establishes the VEDA Strategy system identity.

---

### Batch K — VEDA Strategy Interface Full Specification (Deferred)
**Branch:** deferred
**Status:** Deferred — do not start until Batches A–F are complete and stable

Docs (when ready):
- `interfaces/veda-strategy-to-project-v-signal-interface.md` — full spec
- `interfaces/veda-strategy-to-v-forge-signal-interface.md` — full spec

**Why deferred:** Full interface specification requires understanding VEDA
Strategy's schema and signal posture, which cannot be final until Batch D
docs are reviewed and stable. The stubs from Batch F are sufficient until then.

---

## Sequencing Summary

```
Batch A  →  Batch B  →  Batch C  →  Batch D
                                         ↓
               Batch E ←←←←←←←←←←←←←←←←
                   ↓
               Batch F
                   ↓
               Batch G
                   ↓
               Batch H  (Firecrawl admission runs in parallel)
                   ↓
               Batch I  (blocked until research reviewed)
                   ↓
               Batch J  (follows Batch D, independent of H/I)
                   ↓
               Batch K  (deferred, follows A–F stable)
```

Batches A, B, C must run in order.
Batches D through H run in sequence after C.
Batch I is blocked on external research input.
Batch J may run after Batch D regardless of H or I status.
Batch K is the last phase — do not start it early.

---

## What Must Not Happen in One Pass

- Do not rewrite all VEDA docs at once. They are already well-aligned. Only
  add VEDA Strategy name references where "belongs elsewhere" has no destination.
- Do not rewrite the existing signal interfaces. They are fully specified
  and correct. Batch F creates new stubs; it does not touch existing interfaces.
- Do not create VEDA Strategy docs before Batch A locks the four-system map.
  A system doc that references a system not yet in the ecosystem overview
  exists in a governance vacuum.
- Do not embed Qdrant doctrine into db-posture or system docs before
  Batch I promotes the research into governed doctrine.
- Do not correct the strategy/* system field before Batch D establishes
  the VEDA Strategy identity. The files are usable as-is.
- Do not let provider capability imply settled schema or strategy doctrine.
  DataForSEO AI Optimization admission means the source is admitted as VEDA
  observatory input; it does not mean normalization, weighting, derived models,
  or tactics are already canonized.
- Do not treat the transition-steward folder as a replacement for authority
  docs. Any load-bearing conclusion must be promoted into the proper doc
  cluster and removed from here.

---

## Operating Rules

- No silent architecture changes
- No weakening of system boundaries
- No reintroduction of VEDA Brain under any name
- No assumption that current implementation reflects correct doctrine
- Flag missing authority instead of inventing it
- One branch per batch — no mixing batch scope
- Merge and review each batch before starting the next
- Physical consolidation does not mean conceptual merger

---

## End Condition

The transition is complete when:

- All Tier 1 and Tier 2 docs reflect the four-system map
- No docs reference multi-database posture
- VEDA Strategy has identity docs, schema stub, and interface stubs
- VEDA docs name VEDA Strategy explicitly where relevant
- `ecosystem-schema-spine.md` includes `veda_strategy` in all enumerations
- Firecrawl is in the VEDA provider registry via the governed process
- DataForSEO AI Optimization is reflected consistently as VEDA observatory input,
  with later schema and strategy implications clarified in the proper batches
- Qdrant retrieval posture is in a governed ecosystem doc
- Pre-project observability concepts are formalized in VEDA docs
- No contradictions remain between Tier 1 docs
- Implementation can proceed from docs without drift assumptions





