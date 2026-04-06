# Nerve Runtime Roadmap

## Purpose

This document is the placeholder roadmap and working checklist for the Nerve runtime-support build inside the V Ecosystem shared docs root.

It exists to answer:

```text
What is the full current roadmap for Nerve-related planning, doctrine-gated implementation design,
and shared-root promotion work, in what order, with what dependencies,
so work can proceed without drift or rediscovery?
```

This is a planning and coordination document.
It is not doctrine.
It is not an authority substitute for canonical docs elsewhere in the shared root.

---

## Scope

This document governs:

- the current Nerve roadmap structure
- roadmap phases and sequencing
- bounded deliverables and checkpoints
- doctrine gates before risky runtime features advance
- status tracking for the current Nerve doc wave
- the bridge from `nerve/` investigation work into canonical shared-root doc work

---

## Out of Scope

This document does not define:

- final doctrine wording
- final implementation code
- final MCP schemas
- final UI component designs
- final cross-system runtime behavior outside canonical docs

Those belong in the proper authority docs.

---

## Core Rule

Nerve is the V Ecosystem's own governed runtime-support direction.

External repos may be studied for bounded runtime patterns, but the roadmap must always prioritize:

- V authority clarity
- V governance posture
- V system boundaries
- operator-visible runtime behavior
- non-authoritative continuity discipline
- implementation usefulness without drift

Convenience is not the roadmap driver.
Doctrine fit is.

---

## Current roadmap phase

**Current phase:** utility-support second wave established.

This means:

- the first-wave doctrine-gated implementation-design spine is already in place
- the core governance gate patch has landed
- the core compaction and tool-surface implementation companions are written
- the canonical interface docs have already been patched to integrate those companions
- the next lower-risk support artifacts for token/cost tracking, transcript persistence, and task lifecycle are now also written
- the next work is no longer basic scaffolding; it is second-wave integration, selective canonical patching, and careful planning for any higher-risk continuation

---

## Roadmap overview

### Phase 0 - Investigation cluster setup
**Status:** complete

Completed outcomes:
- established `nerve/` as bounded planning / analysis / implementation-design cluster
- separated analysis, audits, references, planning, and archive roles
- clarified that Nerve is V-native and external repos are reference inputs only
- created first-pass planning and audit artifacts

Artifacts:
- `nerve/README.md`
- `nerve/analysis/nerve-runtime-pattern-analysis.md`
- `nerve/audits/nerve-doctrinal-integration-audit.md`
- `nerve/references/nerve-runtime-source-reference.md`
- `nerve/planning/nerve-runtime-harvest-plan.md`

Checkpoint:
- `nerve/` is readable, role-separated, and not speaking borrowed identity language

---

### Phase 1 - Roadmap and governance-gate planning
**Status:** complete

Objective:
- establish the full working roadmap and checklist for the Nerve wave so shared-root work proceeds in sequence and does not get rediscovered session to session

Primary deliverables:
- this roadmap document
- explicit sequence for first canonical patches and implementation companion docs
- status/checklist tracking for each next artifact

Exit criteria:
- roadmap is clear enough that the next doc pass can begin immediately
- first doctrine gate is identified and accepted
- artifact order is locked

Completed outcome:
- roadmap structure and sequencing are now established

---

### Phase 2 - Doctrine gate patch
**Status:** complete

Objective:
- create the smallest required canonical patch that unlocks safe implementation-design work for the highest-risk runtime feature

Primary deliverable:
- bounded patch to `governance/agent-operating-doctrine.md`

Patch intent:
- classify pre-compaction memory flush as a governed bounded action
- constrain its write scope to designated non-authoritative artifacts
- bind it to non-authority vocabulary and source attribution posture

Why this phase exists:
- memory flush is one of the highest-risk future runtime behaviors
- the compaction implementation companion should not describe it without an explicit doctrinal leash

Exit criteria:
- the governing patch exists in canonical docs
- future Nerve implementation companions can reference the flush as a bounded governed action

Completed artifact:
- `governance/agent-operating-doctrine.md` patched with `Pre-Compaction Flush Principle`

Checklist:
- [x] draft patch language
- [x] review against current governance language
- [x] apply bounded patch
- [x] note patch relationship inside Nerve planning docs if needed

---

### Phase 3 - Compaction implementation companion
**Status:** complete

Objective:
- define the mechanical compaction implementation design for Nerve without creating a parallel doctrine source

Primary deliverable:
- `interfaces/extension-compaction-implementation-design.md`

This companion must be explicitly subordinate to existing canonical docs, especially:
- `interfaces/extension-memory-and-continuity-model.md`
- `interfaces/extension-state-and-context-model.md`
- `governance/agent-operating-doctrine.md`

Primary content areas:
- trigger conditions
- token budget model
- protected-context preservation mechanics
- pre-compaction flush integration point
- compaction class mapping to existing doctrine
- compact boundary creation
- post-compaction per-category re-validation
- failure posture when required context does not survive

Why this phase exists:
- long sessions need compaction
- compaction is the highest-value runtime substrate gap
- naive borrowing is unsafe
- the current doctrine already says what must be protected; the missing piece is how

Exit criteria:
- shared-root has a bounded implementation companion for compaction
- companion clearly references and obeys existing doctrine
- no parallel authority language is introduced

Completed artifact:
- `interfaces/extension-compaction-implementation-design.md`

Checklist:
- [x] outline companion structure
- [x] map existing doctrinal compaction rules by name
- [x] define mechanics only, not replacement doctrine
- [x] include re-validation behavior
- [x] include operator-visible compaction posture

---

### Phase 4 - Tool-surface implementation companion
**Status:** complete

Objective:
- define the mechanical tool registry and session-scoped filtering model that enforces absent-affordance doctrine structurally

Primary deliverable:
- `interfaces/extension-tool-surface-implementation-design.md`

This companion must be explicitly subordinate to:
- `interfaces/extension-system-init-and-tool-surface-model.md`
- relevant governance docs for action posture
- orchestration docs where delegated tool narrowing applies

Primary content areas:
- tool trait / registry role
- current-system filtering
- referenced-system read posture
- project-scope filtering
- action-class filtering
- delegated tool-surface narrowing
- structural absent-affordance enforcement
- runtime refresh/invalidation triggers for the active tool surface

Why this phase exists:
- doctrine already requires wrong actions to be absent from wrong surfaces
- the missing piece is the runtime enforcement design

Exit criteria:
- tool-surface mechanics are clear enough for future implementation
- current-system and cross-system posture are unambiguous
- tool availability is clearly an exposure decision, not an authority grant

Completed artifact:
- `interfaces/extension-tool-surface-implementation-design.md`

Checklist:
- [x] outline companion structure
- [x] map current-system / referenced-system rules
- [x] define filtering stages
- [x] define delegated narrowing rule
- [x] define refresh triggers for tool-surface rebuild

---

### Phase 5 - Canonical doc integration patches
**Status:** complete

Objective:
- patch existing canonical docs so the new implementation companions are integrated into the real authority spine

Primary deliverables:
- bounded patch to `interfaces/extension-memory-and-continuity-model.md`
- bounded patch to `interfaces/extension-system-init-and-tool-surface-model.md`
- bounded patch to `interfaces/extension-state-and-context-model.md`

Patch intent:
- add companion cross-references
- tighten any wording needed to connect doctrine to implementation support
- explicitly note mechanical companions where appropriate

Why this phase exists:
- implementation companions should not float loose
- shared-root readers need a clear bridge from doctrine to support docs

Exit criteria:
- companion docs are discoverable from the relevant doctrine docs
- no ambiguity remains about document hierarchy

Completed artifacts:
- `interfaces/extension-memory-and-continuity-model.md` patched
- `interfaces/extension-system-init-and-tool-surface-model.md` patched
- `interfaces/extension-state-and-context-model.md` patched

Checklist:
- [x] patch memory-and-continuity doc
- [x] patch system-init/tool-surface doc
- [x] patch state-and-context doc
- [x] verify doc hierarchy language stays clean

---

### Phase 6 - Utility support docs
**Status:** complete

Objective:
- add lower-risk implementation support docs that improve runtime usefulness without leading the authority model

Deliverables:
- `interfaces/extension-token-and-cost-tracking-design.md`
- `interfaces/extension-transcript-persistence-design.md`
- `interfaces/extension-task-lifecycle-implementation-design.md`

Why this phase existed:
- the first-wave spine was complete
- these were the most useful next artifacts with lower drift risk than delegation-heavy continuation
- they expand runtime usefulness while still remaining subordinate to the current authority spine

Exit criteria:
- token/cost, transcript, and task-lifecycle support docs exist
- utility-support second wave is documented in bounded implementation-support form
- lower-risk support work does not outrun the canonical authority posture

Completed artifacts:
- `interfaces/extension-token-and-cost-tracking-design.md`
- `interfaces/extension-transcript-persistence-design.md`
- `interfaces/extension-task-lifecycle-implementation-design.md`

Checklist:
- [x] choose next utility-support artifact
- [x] write token/cost doc
- [x] write transcript persistence companion
- [x] write task lifecycle companion

---

### Phase 7 - Utility-support integration and second-wave canonical linking
**Status:** active planning

Objective:
- determine whether and where the new utility-support companions should be linked back into existing canonical authority docs so the second-wave support layer is discoverable without bloating Tier 1 docs

Candidate deliverables:
- bounded patch linking token/cost tracking into the most appropriate canonical interface doc(s)
- bounded patch linking transcript persistence into the memory/continuity spine if needed
- bounded patch linking task lifecycle into the orchestration/state spine if needed
- updated roadmap/checklist synchronization as utility-support docs land

Why now:
- the utility-support docs now exist
- the core question is no longer whether to write them, but how much canonical linkage is actually useful
- this phase should stay bounded and avoid turning every Tier 1 doc into a cross-reference swamp

Exit criteria:
- decide which utility docs deserve canonical cross-links
- apply only the minimal useful linking patches
- keep hierarchy clear and readable

Checklist:
- [ ] decide whether token/cost needs canonical cross-linking
- [ ] decide whether transcript persistence needs canonical cross-linking
- [ ] decide whether task lifecycle needs canonical cross-linking
- [ ] apply only bounded, justified patching

---

### Phase 8 - Higher-risk runtime continuation
**Status:** deferred

Objective:
- only after the foundation proves stable, evaluate whether higher-risk runtime behaviors deserve formal design work

Candidate areas:
- worker delegation mechanics
- worker permission bridge
- worker memory sync
- session resume posture
- broader orchestration-support mechanics

Why deferred:
- these areas are riskier
- they are more likely to create authority confusion or governance leakage
- they should not lead the Nerve wave

Exit criteria:
- compaction and tool-surface foundation is already solid
- doctrine remains legible
- the utility-support second wave has settled cleanly
- there is a real implementation need for the next wave

Checklist:
- [ ] do not start early
- [ ] revisit only after first-wave and utility-support docs are absorbed
- [ ] require new doctrine-gate review before advancement

---

## Current artifact map

### Nerve planning cluster
- `nerve/README.md`
- `nerve/analysis/nerve-runtime-pattern-analysis.md`
- `nerve/audits/nerve-doctrinal-integration-audit.md`
- `nerve/references/nerve-runtime-source-reference.md`
- `nerve/planning/nerve-runtime-harvest-plan.md`
- `nerve/planning/nerve-runtime-roadmap.md`

### Canonical governance / interface outputs — first-wave spine
- `governance/agent-operating-doctrine.md` — patched
- `interfaces/extension-compaction-implementation-design.md` — created
- `interfaces/extension-tool-surface-implementation-design.md` — created
- `interfaces/extension-memory-and-continuity-model.md` — patched
- `interfaces/extension-system-init-and-tool-surface-model.md` — patched
- `interfaces/extension-state-and-context-model.md` — patched

### Canonical interface outputs — utility-support second wave
- `interfaces/extension-token-and-cost-tracking-design.md` — created
- `interfaces/extension-transcript-persistence-design.md` — created
- `interfaces/extension-task-lifecycle-implementation-design.md` — created

---

## Master checklist

### Investigation / cluster hygiene
- [x] create `nerve/` structure
- [x] create Nerve README
- [x] separate analysis / audits / references / planning / archive
- [x] rename docs to Nerve-first names
- [x] create first-pass harvest plan
- [x] create roadmap placeholder and checklist

### First-wave spine
- [x] patch `governance/agent-operating-doctrine.md`
- [x] write `interfaces/extension-compaction-implementation-design.md`
- [x] write `interfaces/extension-tool-surface-implementation-design.md`
- [x] patch `interfaces/extension-memory-and-continuity-model.md`
- [x] patch `interfaces/extension-system-init-and-tool-surface-model.md`
- [x] patch `interfaces/extension-state-and-context-model.md`

### Utility-support second wave
- [x] write `interfaces/extension-token-and-cost-tracking-design.md`
- [x] write `interfaces/extension-transcript-persistence-design.md`
- [x] write `interfaces/extension-task-lifecycle-implementation-design.md`

### Second-wave integration decisions
- [ ] decide whether utility docs need canonical cross-linking
- [ ] apply bounded linking patches only where justified

### Deferred higher-risk wave
- [ ] worker delegation mechanics
- [ ] worker permission bridge
- [ ] worker memory sync
- [ ] session resume posture
- [ ] broader orchestration continuation

---

## Prioritization rules

When choosing next work, use this order:

1. smallest doctrine gate that prevents future drift
2. highest-value mechanical companion for an already-established doctrine area
3. bounded patch that integrates new support docs into canonical authority
4. lower-risk utility support docs
5. higher-risk continuity / delegation / orchestration expansion only after the first and second waves prove stable

---

## Anti-drift checklist

The roadmap should be considered off-track if any of the following begin to happen:

- Nerve starts being described as if it is a generic agent harness
- external reference repos start shaping naming or identity instead of only patterns
- implementation companions begin redefining doctrine instead of supporting it
- memory starts sounding authoritative
- transcripts start sounding like governance records
- tool availability starts being confused with permission or approval
- task state starts being treated as canonical completion
- delegation starts widening capability or authority
- `nerve/` starts functioning like a shadow authority root

---

## Current best next move

The current best next move is to decide whether the three utility-support companions need bounded canonical linking patches.

Recommended evaluation order:

1. transcript persistence -> likely memory/continuity linkage candidate
2. task lifecycle -> likely orchestration/state linkage candidate
3. token/cost tracking -> likely light state/tool-surface linkage candidate

That keeps the roadmap moving without jumping early into the higher-risk continuation wave.
