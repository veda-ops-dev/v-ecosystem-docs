# First Project V Forge — Transition-Support Cluster

## Purpose

This subfolder contains the transition-support workstream for the first-project
V Forge / context-loading design cluster. It covers the doctrine-aware context
model, the execution-scoped planning digest seam, the first-project execution
packet, and the V Forge structural decisions for products, affiliate links, and
page/content records.

These are transition-support notes, spec exercises, and bounded design decisions.
None of them are final V Forge doctrine. They are the working basis from which
later schema specification and doctrine work should begin.

---

## What This Cluster Covers

- **Context-loading model:** Stage-aware, authority-aware context loading for
  VedaOps. Defines context classes, workflow stages, admission enforcement,
  load record posture, and validation independence.

- **Execution-scoped planning digest seam:** Whether and how planning-side
  constraints can safely reach execution context without loading the planning
  packet. Concluded: a digest is rarely needed when the execution packet is
  properly formed.

- **First-project execution packet:** The primary execution truth carrier for
  the gift discovery v1 scope. Absorbs the digest for this proving case.

- **V Forge structural decisions:** Product record family, affiliate-link record
  family, page/content graph posture, schema-facing drafting basis.

---

## Recommended Reading Order

Read in this order to follow the derivation chain:

1. `doctrine-aware-context-model-note.md` — problem statement, anchor principle
2. `doctrine-aware-context-model-design-pass.md` — tightened context model with
   stage rules and authority ranking
3. `doctrine-aware-context-enforcement-and-inspectability-note.md` — enforcement
   and load record posture
4. `execution-scoped-planning-digest-spec-note.md` — digest spec (what it is,
   what it must not be, alignment with handoff interface)
5. `first-project-draft-execution-scoped-planning-digest.md` — draft digest
   exercise against first-project materials
6. `first-project-digest-against-execution-packet-closure-note.md` — closure:
   digest is empty against the execution packet
7. `first-project-v1-execution-packet-draft.md` — **the primary execution
   artifact for the first-project v1 scope**
8. `first-project-affiliate-link-record-posture-note.md` — affiliate link
   record shape, lifecycle states, product/link separation
9. `affiliate-link-placement-in-v-forge-note.md` — placement decision:
   content-graph-adjacent execution record family
10. `first-project-v-forge-record-families-spec-note.md` — record families,
    join posture, lifecycle separation, integrity rules
11. `product-record-graph-posture-note.md` — graph posture decision:
    product records are not graph nodes; pages are
12. `first-project-v-forge-schema-drafting-basis-note.md` — **current best
    starting point for V Forge schema drafting**

---

## Current Settled Conclusions

These should be treated as working truth for schema and spec work unless
the repo or first-project exercise contradicts them:

- **Execution packet is primary.** The execution packet is the primary carrier
  of execution truth. The digest is auxiliary and, for this first project,
  is not needed.

- **Digest seam is closed for this proving case.** The draft execution packet
  absorbs all five digest items. The digest concept is validated as a
  safety-net mechanism, not a routine artifact.

- **Product is the primary durable object.** Product records are stable
  execution truth. Their identity does not change due to merchant churn, page
  publication, or link decay.

- **Affiliate-link records are subordinate, separate, content-graph-adjacent
  execution records.** They join to products by product identifier. They are
  outside the content graph. They have their own lifecycle posture independent
  of product lifecycle.

- **Product records are not content graph nodes.** Page/content representations
  are the graph participants. Page nodes carry product identifier references.
  The join direction is one-way: page → product.

- **The schema drafting starting point is `first-project-v-forge-schema-drafting-
  basis-note.md`.** It consolidates all settled decisions into a schema-facing
  drafting basis.

---

## What Remains Open

- Multi-product page reference mechanism: foreign key list vs. association
  table (M1 vs. M2 in the schema drafting basis note). Must be decided before
  drafting guide/browse page schema.
- Whether product lifecycle transitions produce activity trail records.
- Price signal field design (simple column vs. structured object).
- Link verification cadence and dead-link detection mechanism.
- Handoff interface alignment for the digest concept (approval scope ambiguity;
  digest is not needed for this first project so this is moot for now).
- Affiliate link schema specifics (field types, constraints, migration).

---

## Files That Are Derivation History vs. Current Starting Points

**Current starting points (read these first for new work):**
- `first-project-v-forge-schema-drafting-basis-note.md` — for V Forge schema
  drafting
- `first-project-v1-execution-packet-draft.md` — for first-project execution
  preparation
- `execution-scoped-planning-digest-spec-note.md` — for digest governance in
  future projects with underspecified execution packets

**Derivation history (read if you need to understand why decisions were made):**
- `doctrine-aware-context-model-note.md`
- `doctrine-aware-context-model-design-pass.md`
- `doctrine-aware-context-enforcement-and-inspectability-note.md`
- `first-project-draft-execution-scoped-planning-digest.md`
- `first-project-digest-against-execution-packet-closure-note.md`
- `first-project-affiliate-link-record-posture-note.md`
- `affiliate-link-placement-in-v-forge-note.md`
- `first-project-v-forge-record-families-spec-note.md`
- `product-record-graph-posture-note.md`

---

## Related Files (Outside This Subfolder)

**Planning materials (stay at `transition-steward/` top level):**
- `../first-project-entity-driven-gift-discovery-site.md`
- `../first-project-entity-driven-gift-discovery-planning-packet.md`
- `../transition-plan.md`

**Authority docs:**
- `../../v-forge/v-forge.md`
- `../../v-forge/content-execution-module.md`
- `../../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../../interfaces/llm-harness-architecture.md`
- `../../interfaces/desktop-memory-and-continuity-model.md`
- `../../project-v/project-v.md`
