# Coding-Readiness Classification

## 1. Purpose

This document classifies the current state of the `v-ecosystem-docs` repo for
coding-readiness, so that future coding work — whether by a human engineer or
a coding LLM — knows which files are safe direct inputs, which are useful
support context, which are derivation history that should not be fed directly,
and what still blocks or constrains coding.

It is optimized for the first slice: handoff acceptance + approval gate +
activity trail, no content execution.

---

## 2. Status

Transition-support implementation-planning doc only.
Not authority doctrine. Not implementation code.

---

## 3. Classification Rules

**Tier 1 direct authority** — Canonical doctrine. A coding LLM should treat
these as the governing truth. Contradicting them is an implementation error.

**Tier 2 system authority** — System-specific doctrine within ecosystem
boundaries. Load for the relevant system. Treat as binding for that system's
behavior.

**Implementation-support (transition-steward)** — Engineering-facing derivations
from authority docs. Safe to load alongside authority docs. Must not outrank
them if there is a conflict. Transition-support docs that are contradicted by
an authority doc are wrong; the authority doc wins.

**Derivation history / do not feed directly** — Background work, design
exploration, parked workstreams, or superseded reasoning. Useful for a human
needing to understand why a decision was made. Should not be primary coding
input because it may contain contradicted assumptions, open questions, or
scope that is not part of the first slice.

**Blocked / not ready** — Doc families or areas where the underlying doctrine
is unsettled, provider-dependent, or deferred to a later batch. Feeding these
into a coding LLM for the first slice would introduce uncertainty or cause
the LLM to speculate.

---

## 4. Safe Direct Coding Inputs

These files are safe primary inputs for coding the first slice. A coding LLM
can be handed these directly and should treat them as authoritative.

### Tier 1 ecosystem authority

| File | Why it's in scope |
|---|---|
| `ecosystem/db-posture.md` | Governs the four-schema Postgres model, credential isolation rules, and migration ownership — directly needed for T-01 |
| `ecosystem/activity-trail-model.md` | Canonical action vocabulary, required fields, and entity type vocabulary — directly needed for T-02 and T-05 |
| `ecosystem/cross-system-boundaries.md` | Defines ownership model enforced in T-01 and throughout the slice |

### Tier 2 V Forge and interface authority

| File | Why it's in scope |
|---|---|
| `v-forge/system-invariants.md` | Invariants 6, 8, 9, 11, 13 directly govern the first slice's behavior; Invariant 8 drives the `project_id` non-null requirement |
| `v-forge/operational-model.md` | Defines handoff receipt, validity check, and governed halt — the operational flow the slice implements |
| `v-forge/reporting-and-approval-model.md` | Defines what V Forge must report at handoff receipt and after a halt; governs T-12 |
| `interfaces/project-v-to-v-forge-handoff-interface.md` | Canonical authority on handoff package semantics, validity conditions, and required fields — primary source for T-06 validator |
| `interfaces/desktop-governance-and-gating-model.md` | Governs Class B/C approval gate enforcement, persisted approval record requirement, and fail-closed behavior — primary source for T-07 and T-10 |
| `governance/approval-mechanics-seam-model.md` | Governs `approval.request` / `approval.decide` mechanics and pending-state vocabulary — primary source for T-09 |

### Transition-steward implementation-support (first-slice specific)

| File | Why it's in scope |
|---|---|
| `transition-steward/activity-trail-implementation-spec.md` | Specifies the exact table schema, indexes, write helper behavior, fail-closed vs fail-open distinction, and DLQ — directly implements T-02 and T-05 |
| `transition-steward/packet-schema-drafting-basis.md` | Specifies the structural constraints for handoff packet validation (Section A), approval request packet (Section C base fields) — directly implements T-06 |
| `transition-steward/invariant-enforcement-plan.md` | Maps each invariant to its enforcement layer and mechanism — directly implements T-01 through T-08 |
| `transition-steward/minimum-codable-first-slice.md` | Defines the exact slice scope, component list, record shapes, success/failure states |
| `transition-steward/first-slice-implementation-task-breakdown.md` | 14 concrete tasks with dependencies and acceptance criteria — the primary engineering-facing input for the first slice |

---

## 5. Useful Support Guidance

These files provide valuable context and should be available to a coding LLM
as reference, but they are not primary authorities for the first slice. If
they conflict with files in Section 4, Section 4 wins.

| File | Role |
|---|---|
| `ecosystem/v-ecosystem-overview.md` | Orientation — system roles and ecosystem mental model; useful for LLM context-setting but not a coding authority for the slice |
| `v-forge/v-forge.md` | V Forge identity doc; useful for understanding what V Forge is and is not; the `system-invariants.md` is more actionable for the slice |
| `interfaces/v-forge-to-project-v-return-to-planning-interface.md` | Useful background for understanding what happens *after* the governed halt; not in scope for the first slice but relevant for the second slice |
| `README.md` | Authority tier structure; useful for a coding LLM to understand the hierarchy it is working within |

---

## 6. Derivation History — Do Not Feed Directly to a Coding LLM

These files contain background work, design explorations, parked workstreams,
or superseded reasoning. A human engineer may benefit from reading them to
understand why decisions were made. A coding LLM given these as primary inputs
may import out-of-scope assumptions, open questions, or schema designs that
conflict with what the first slice requires.

### First-project V Forge cluster (`transition-steward/first-project-v-forge/`)

This entire subfolder is derivation history for the first-project (gift
discovery affiliate site) execution design. It contains valuable schema-facing
work for future V Forge slices, but it covers content graph, product records,
affiliate links, and execution packet design — none of which are in scope for
the first slice.

Specifically do not feed:
- `first-project-v1-execution-packet-draft.md` — a real execution packet for a specific project, not a governance spec
- `first-project-v-forge-schema-drafting-basis-note.md` — useful later for content graph; premature for the first slice
- `doctrine-aware-context-model-design-pass.md` and related — context-loading design that predates the current first slice definition
- All other files in `first-project-v-forge/` — they are derivation history per the subfolder README

### Batch H notes (`transition-steward/batch-h-*`)

| File | Why not to feed |
|---|---|
| `batch-h-veda-family-design-pass.md` | VEDA schema design work; completely outside first slice scope |
| `batch-h-veda-family-design-pass-corrections.md` | Corrections to the above; same scope issue |
| `batch-h-dataforseo-confidence-layer.md` | DataForSEO provider work; provider-dependent, outside first slice |
| `batch-h-dataforseo-surface-inventory.md` | DataForSEO surface mapping; same |
| `batch-h-waiting-on-provider-credits.md` | Blocked work note; not a coding input |

### Other transition-steward files outside first slice scope

| File | Why not to feed |
|---|---|
| `dataforseo-capture-plan.md` | Provider capture planning; outside first slice |
| `dataforseo-research-tracker.md` | Research tracking; outside first slice |
| `byda-spec-audit-findings-adjudicated.md` | BYDA audit spec work; outside first slice |
| `hammer-upgrade-plan.md` | Tooling upgrade notes; outside first slice |
| `first-archetype-affiliate-content-site-note.md` | First-archetype site note; outside first slice |
| `first-project-entity-driven-gift-discovery-site.md` | First-project site spec; outside first slice |
| `first-project-entity-driven-gift-discovery-planning-packet.md` | First-project planning packet; outside first slice |
| `dataforseo-json/` (directory) | Raw JSON samples; not a coding authority |
| `firecrawl/` (directory) | Firecrawl provider baseline samples; not a coding authority for the first slice |

### VEDA and VEDA Strategy doc families

The `veda/` and `veda-strategy/` doc families are entirely outside the first
slice scope. They govern observatory and derived intelligence work. Do not
load these into a coding session focused on the first slice.

### Transition plan

`transition-steward/transition-plan.md` is the control spine document for the
full repo correction sequence. It is useful for understanding the broader
authority context but does not add actionable implementation detail for the
first slice. Include it as orientation if the LLM needs to understand batch
sequencing; exclude it from the primary coding packet.

---

## 7. Real Blockers and Constrained Areas

### For the first slice — no blockers

The first slice is fully unblocked. All required authority docs are present,
stable, and consistent. All required implementation-support specs are written.
No provider credits, no deferred Batch H work, and no unsettled interfaces
are required.

The credential verification script (T-14) does require a running Postgres
environment, but that is an infrastructure requirement, not a documentation gap.

### What remains blocked outside the first slice

**Batch H VEDA schema work** — The `observatory_scope`, `topic_monitor`, and
Firecrawl/DataForSEO capture families are deferred as "deferred-but-owned"
schema families. No implementation work on VEDA signal ingestion, crawl
capture, or AI-surface observability is unblocked until Batch H doctrine work
completes. This does not affect the first slice.

**VEDA Strategy interfaces (Batch K)** — Both VEDA Strategy signal interfaces
are governed stubs with full contracts deferred to Batch K. No schema or
implementation work on those interfaces is unblocked. Does not affect the
first slice.

**Content graph implementation** — The `v_forge.pages`, `v_forge.topics`,
`v_forge.entities`, and junction tables are not in scope for the first slice.
The first-project V Forge cluster provides useful schema-facing drafting basis
notes, but those notes carry open questions (multi-product page reference
mechanism, price signal field design, link verification cadence) that are
not yet resolved. Content graph work is the second or third slice, not the
first.

**Human authority review of landed batches** — The transition plan notes that
Batches A through G, J, and L are on branch but pending human review and
acceptance. None of those batches are blockers for the first slice, which works
from the V Forge and ecosystem authority docs (already well-specified and
stable). But any doc changes that emerge from the human review process could
in principle affect docs in the first slice's coding packet. This is low risk
for the ecosystem and V Forge docs, which are among the most stable in the
repo.

**Return-to-planning interface — not a blocker, but a boundary**
`interfaces/v-forge-to-project-v-return-to-planning-interface.md` is fully
specified. The first slice ends at a governed halt and does not implement the
return delivery. This interface is ready for the second slice.

---

## 8. Recommended Coding Packet

This is the smallest file set that should be handed to a coding LLM for the
first slice. Load in the order listed. Do not add files not listed here without
explicit justification.

### Primary coding packet (load all of these)

**Authority docs — load first:**
```
ecosystem/db-posture.md
ecosystem/activity-trail-model.md
v-forge/system-invariants.md
v-forge/operational-model.md
v-forge/reporting-and-approval-model.md
interfaces/project-v-to-v-forge-handoff-interface.md
interfaces/desktop-governance-and-gating-model.md
governance/approval-mechanics-seam-model.md
```

**Implementation-support specs — load second:**
```
transition-steward/activity-trail-implementation-spec.md
transition-steward/packet-schema-drafting-basis.md
transition-steward/invariant-enforcement-plan.md
transition-steward/minimum-codable-first-slice.md
transition-steward/first-slice-implementation-task-breakdown.md
```

**Total: 13 files.**

### Optional orientation (load only if the LLM needs ecosystem-level grounding):
```
ecosystem/v-ecosystem-overview.md
ecosystem/cross-system-boundaries.md
README.md
```

These three add ecosystem identity context. They are not required for a coding
LLM that already has the 13 primary files, but they help if the LLM asks
questions about why boundaries exist.

### Do not add to the coding packet without explicit justification:
- Anything in `transition-steward/first-project-v-forge/`
- Anything in `transition-steward/batch-h-*`
- `veda/` or `veda-strategy/` doc families
- `v-forge/content-execution-module.md` — content execution is not in scope
- `v-forge/bounded-analytical-tools-and-plugin-doctrine.md` — plugin doctrine is not in scope
- `transition-steward/transition-plan.md` — batch sequencing context, not coding guidance

---

## 9. Anti-Drift Rules

**Do not feed the first-project V Forge cluster into first-slice coding.**
Those docs cover content graph, product records, affiliate links, and
execution packet design for a specific affiliate site project. None of that
is the first slice. A coding LLM given those files will try to implement
content graph tables, product records, or affiliate link schemas that are
explicitly out of scope.

**Do not feed Batch H notes into V Forge first-slice work.**
Batch H covers VEDA provider schema work and is provider-credit-dependent.
It has nothing to do with the handoff/approval/trail slice.

**Do not treat transition-steward derivation notes as higher authority than
Tier 1 docs.** The implementation-support specs are derivations from the
authority docs. If any spec statement appears to conflict with an authority
doc, the authority doc is correct and the spec is the error. The authority
doc wins.

**Do not broaden the coding packet during implementation.**
If a task seems to need a file not in the packet, stop and ask whether the
task has drifted outside the first slice. The 13-file packet is sufficient
for the first slice. Adding files casually is how scope expands.

**Do not skip the credential verification step before writing application code.**
T-14 is a deployment gate, not a nice-to-have. The classification is that
T-01 and T-14 must be complete before application code is written. This rule
must not be relaxed for development velocity.

**Do not treat the first-project V Forge schema drafting basis note as a
substitute for first-slice table definitions.**
`first-project-v-forge-schema-drafting-basis-note.md` is a derivation history
document with open questions. The minimal table definitions in
`first-slice-implementation-task-breakdown.md` (T-04) are the correct source
for the three tables needed in the first slice.

**Do not use `veda/` or `veda-strategy/` docs as coding inputs for the
first slice.** VEDA is not involved in the first slice. Loading VEDA docs
into a coding session for the handoff/approval slice will prompt the LLM to
speculate about signal interfaces and provider integrations that are explicitly
out of scope and not yet governed to a codable level.

---

## 10. Recommended Next Move

**Immediate:** Hand the 13-file primary coding packet to an engineer or a
coding LLM session. Start with T-01 (Postgres schema and role setup) because
it is the foundation for everything else and has no dependencies. Run T-14
(credential verification script) before writing any application code.

**Concurrently with DB setup:** Begin T-06 (handoff packet validator) and
T-08 (session scope check) — both have no DB dependency and can be written
and unit-tested while the DB infrastructure is being set up.

**First checkpoint:** Before proceeding past T-09, run CI-01 (credential
verification) in the actual environment. Do not assume credential isolation
is working until the script confirms it.

**After the first slice passes all integration tests:** Conduct a human review
of the trail replay output. Confirm the six expected trail records exist in
order for a completed handoff lifecycle. This is the governance proof — the
thing the slice is designed to demonstrate.

**After the governance proof is confirmed:** Update this classification document
to reflect that the first slice is complete, and produce a classification for
the second slice (return-to-planning delivery), which will require adding
`interfaces/v-forge-to-project-v-return-to-planning-interface.md` to the
coding packet and extending the packet schema drafting basis to include the
Section B return-to-planning validator.

---

## 11. Related Files

Authority docs classified in this document:
- `ecosystem/db-posture.md`
- `ecosystem/activity-trail-model.md`
- `ecosystem/cross-system-boundaries.md`
- `ecosystem/v-ecosystem-overview.md`
- `v-forge/system-invariants.md`
- `v-forge/operational-model.md`
- `v-forge/v-forge.md`
- `v-forge/reporting-and-approval-model.md`
- `interfaces/project-v-to-v-forge-handoff-interface.md`
- `interfaces/desktop-governance-and-gating-model.md`
- `governance/approval-mechanics-seam-model.md`

Implementation-support docs classified in this document:
- `transition-steward/activity-trail-implementation-spec.md`
- `transition-steward/packet-schema-drafting-basis.md`
- `transition-steward/invariant-enforcement-plan.md`
- `transition-steward/minimum-codable-first-slice.md`
- `transition-steward/first-slice-implementation-task-breakdown.md`
- `transition-steward/transition-plan.md`

Derivation history clusters classified in this document:
- `transition-steward/first-project-v-forge/` (entire subfolder)
- `transition-steward/batch-h-*` files
- `transition-steward/dataforseo-*` files
- `transition-steward/firecrawl/` (directory)
- `veda/` (doc family — outside first slice scope)
- `veda-strategy/` (doc family — outside first slice scope)
