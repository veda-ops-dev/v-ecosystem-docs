# VEDA Data Boundaries

## Purpose

This document defines VEDA’s data ownership boundaries inside the V Ecosystem.

It exists to answer:

```text
What data does VEDA canonically own, what data may VEDA reference or package without owning, what data must remain outside VEDA, and what boundary rules prevent VEDA from becoming a planning, execution, or cross-system data swamp?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- what data VEDA canonically owns
- what data VEDA may preserve as evidence, observation, or bounded local interpretation
- what data VEDA may reference without owning
- what data VEDA must not store as canonical truth
- how VEDA’s data boundaries relate to Project V and V Forge
- what boundary drift patterns are forbidden

---

## Out of Scope

This document does not define:

- the exact schema of every VEDA table
- the exact payload format of every cross-system package
- the full interface rules for every downstream consumer
- the full operator-surface design
- detailed deployment, hosting, or database configuration

Those belong in more specific VEDA, interface, or ecosystem docs.

---

## System

- veda

---

## Core Rule

VEDA canonically owns signal, evidence, and observability truth.

VEDA may preserve bounded local interpretation and bounded packaging context, but it must not absorb planning truth, execution truth, or convenience copies of neighboring systems’ canonical data merely because doing so appears operationally useful.

A cleaner dashboard is not a valid reason to erase data boundaries.

---

## Boundary Definition

A VEDA data boundary defines whether a class of data is:

- canonically owned by VEDA
- preserved locally by VEDA as bounded supporting material
- referenced by VEDA without ownership
- or forbidden from becoming VEDA canonical truth

When the same data class appears in more than one context, each appearance must be classified by its role in that context, not by the original data class alone.
A packaged copy of VEDA canonical truth is not canonical truth in the packaging context.
It is bounded supporting material or bounded derived material for that consumer, depending on use.
The context of use determines the classification.

If a data class cannot be placed clearly into one of those categories, the boundary is too weak.

---

## Canonical Ownership Rule

VEDA canonically owns data that belongs to its observability role.

This includes, at the level of doctrine:

- project-scoped observatory partitioning data
- source capture and source item intake records
- observatory event history
- keyword observation targets
- SERP observation records
- search performance observation records
- content graph structural observability records
- bounded observability-relevant configuration
- bounded derived observability outputs that remain explicitly derived and do not become a second canonical truth store

Canonical ownership means VEDA is the system of record for those domains.

---

## Project Partition Rule

VEDA owns project partitioning data only to the degree needed to scope observatory truth.

This means:

- VEDA may own its own thin `Project` partitioning container
- that container exists to partition observatory records cleanly
- it must not become a rich planning/orchestration record by stealth

Project identity inside VEDA is an observatory partitioning concern, not a license to recreate Project V.

---

## Source and Capture Ownership Rule

VEDA canonically owns source capture and source-item intake records.

This includes:

- source identity within VEDA’s intake model
- intake status within the observatory layer
- capture time and capture context
- source provenance relevant to observatory use
- bounded operator intent relevant to why source material was captured

This does not authorize VEDA to turn source capture into a planning backlog, publishing workflow, or execution queue.

---

## Observation Ledger Ownership Rule

VEDA canonically owns observation-ledger data where the ecosystem is recording what was observed over time.

This includes:

- governed observation targets such as `KeywordTarget`
- immutable or append-friendly observation records such as `SERPSnapshot`
- search-performance observation records
- bounded structural observation records in the content graph

VEDA owns what was observed.
It does not own what should happen next because of the observation.

---

## Event Ownership Rule

VEDA canonically owns observatory event history for meaningful persisted observatory state changes inside the VEDA boundary.

This means VEDA owns:

- event type, entity type, entity identity, project scope, actor attribution, and time context for observatory events
- append-only observatory event history
- bounded structured event details relevant to observatory reconstruction

VEDA must not use its event ledger to model planning-state transitions, execution workflow transitions, or generic analytics sludge that belongs elsewhere.

---

## Content Graph Ownership Rule

VEDA canonically owns the observed structural state of content surfaces inside its content graph.

This includes:

- surfaces
- sites
- pages
- structural archetypes
- topics and entities in the content-graph sense
- page-topic and page-entity junctions
- internal links
- schema usage

This ownership is structural and observatory-grounded.
It is not ownership of editorial workflow, CMS state, or execution planning.

---

## Derived Data Rule

VEDA may preserve bounded derived data when that derived data remains clearly subordinate to canonical observatory truth.

This means:

- derived search intelligence may exist
- derived summaries and classifications may exist
- operator-facing derived views may exist
- materialized derived results may exist only when operationally justified and clearly bounded

Materialization of derived data is operationally justified only when there is a documented performance or operational requirement that compute-on-read cannot satisfy at acceptable cost.
The materialized result must remain clearly labeled as derived and must not be promoted to canonical observatory status.
Materialization for convenience, to simplify queries, or to avoid computing from source records is not operational justification.
The test is: would removing the materialized data and computing on-read produce the same result?
If yes, materialization is optional.
If no, the materialized data may have drifted toward canonical truth.

Derived data must not become:

- a second canonical truth store
- a planning state machine
- a hidden write-owned domain
- a strategy ledger disguised as observability support

Derived data may support VEDA’s role.
It must not redefine it.

---

## Local Supporting Material Rule

VEDA may preserve bounded local supporting material when doing so helps evidence traceability, packaging, or bounded observability use.

Examples may include:

- raw provider payloads
- provenance markers
- trust posture markers
- packaging metadata
- bounded summary context tied to evidence continuity

Supporting material must remain explicitly subordinate to VEDA’s canonical observatory records.
It must not be used to smuggle foreign canonical truth into VEDA by convenience.

---

## Reference Without Ownership Rule

VEDA may reference entities or systems outside its canonical ownership boundary without owning their truth.

This means VEDA may preserve:

- source locators
- external URLs
- provider identifiers
- cross-system references needed for governed packaging or coordination
- bounded foreign identifiers where they help traceability or interface behavior

Reference does not imply ownership.
A foreign identifier stored inside VEDA does not make the foreign record VEDA truth.

---

## Project V Boundary Rule

VEDA must not canonically own Project V planning and orchestration truth.

This includes data such as:

- project planning state
- roadmap or sequencing state
- approval posture
- planning decisions
- decision continuity state
- handoff readiness truth
- orchestration workflow state

VEDA may package signal that influences those things.
It must not store them as its own canonical domain.

---

## V Forge Boundary Rule

VEDA must not canonically own V Forge execution truth.

This includes data such as:

- execution task state
- draft lifecycle state
- publishing workflow state
- production asset state
- revision workflow state
- execution queue state
- deployment or distribution execution truth

VEDA may observe execution-adjacent external reality or package evidence relevant to execution review.
It must not become the execution ledger.

---

## Imported Cross-System Data Rule

Where VEDA receives cross-system data through a governed interface or bounded packaging flow, that imported data must remain visibly non-canonical unless governance explicitly establishes a local VEDA-owned observatory representation of it.

This means:

- imported planning context remains planning context, not VEDA-owned planning truth
- imported execution context remains execution context, not VEDA-owned execution truth
- imported material must remain labeled, bounded, and reconstructible

The accumulation of bounded imported context must be reviewed periodically as a boundary-posture concern, not only evaluated at the point of each individual import.
If the aggregate of imported context begins to reconstruct a neighboring system’s canonical truth domain, the accumulated imports are collectively a boundary violation even if each individual import was justified.
VEDA must not allow incremental import to substitute for governed cross-system interface design.

Receiving cross-system context does not grant canonical ownership.

---

## JSON and Payload Boundary Rule

JSON, raw payloads, and flexible structures must not become a loophole for boundary drift.

This means:

- payloads may preserve supporting evidence
- payloads may preserve provider-origin data
- payloads must not become a hiding place for planning truth or execution truth
- payloads must not become the only home of hot-path meaning that should be explicitly modeled

A boundary violation stored in JSON is still a boundary violation.

---

## Global Data Exception Rule

Global data inside VEDA must remain rare, explicit, and observability-justified.

This means:

- global configuration is allowed only where observability posture genuinely requires it
- global tables must not become convenience dumps for data that should be project-scoped
- a globally stored datum must not quietly weaken multi-project isolation

Global is an exception posture.
Not a convenience default.

---

## Cross-Project Isolation Rule

Project-scoped VEDA data must not cross project boundaries by implication, convenience, or structural leakage.

This means:

- project-scoped rows belong to exactly one project unless explicitly global
- reads and writes must enforce project ownership
- graph junctions and graph links must not connect across projects
- derived outputs must preserve project isolation
- foreign references must not be used to leak cross-project existence

Cross-project contamination is a data-boundary failure, not a cleanup issue.

---

## Packaging and Exposure Rule

When VEDA packages or exposes data for downstream systems, the exposed material must preserve its correct boundary classification.

A package should remain clear about whether the included material is:

- canonical VEDA observatory truth
- bounded derived interpretation
- supporting evidence
- external reference
- non-canonical imported context

A downstream consumer must not need to guess what kind of truth it is receiving.

VEDA’s packaging obligation is to expose data with correct boundary classification.
If a downstream consumer misclassifies correctly labeled VEDA output, the misclassification is a consumer-side boundary failure governed by the consuming system’s own data-boundary rules, not by VEDA’s packaging posture.

---

## Boundary Verification Rule

VEDA’s data boundaries must be verifiable in implementation and review.

Verification should include checking that:

- VEDA-owned tables remain observatory-scoped
- Project V and V Forge truth are not silently recreated inside VEDA
- imported context remains visibly non-canonical
- derived material does not become a second truth store
- cross-project contamination attempts fail
- payload fields are not hiding foreign canonical truth

A declared boundary that cannot be checked is weak doctrine.

---

## Forbidden Data Drift Patterns

VEDA data boundaries have drifted if VEDA begins to:

- recreate Project V planning state locally for convenience
- recreate V Forge execution state locally for convenience
- store strategic or orchestration truth as though it were observatory data
- treat foreign identifiers as though they make foreign records locally owned
- materialize derived layers until they overshadow canonical observations
- use JSON blobs to hide cross-boundary truth copying
- let global tables weaken project-scoped isolation
- blur imported context into canonical VEDA truth

These are data-boundary failures, not smart integrations.

---

## Human-In-The-Loop Principle

Human review remains especially important when VEDA data-boundary questions involve:

- new observatory domains
- new cross-system packaging paths
- proposals to materialize more derived data
- proposals to store foreign system context inside VEDA
- proposals to create global tables or broaden existing ones
- proposals that look convenient but weaken observatory ownership clarity

Good boundary discipline is rarely maintained by convenience pressure alone.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- VEDA canonically owns observatory truth and bounded supporting material for that role
- VEDA may reference foreign systems without owning their truth
- VEDA must not absorb Project V planning truth or V Forge execution truth
- derived material must remain subordinate to canonical observatory data
- JSON and packaging do not erase data-boundary rules
- imported context remains non-canonical unless explicitly reclassified through governed architecture work

If an LLM could use this doc to justify copying planning or execution truth into VEDA because it seems useful for a unified surface, this document is failing.

---

## Usage

This document should be used:

- when deciding whether a data class belongs canonically inside VEDA
- when reviewing whether a schema change would weaken VEDA’s observability boundary
- when designing packaging or exposure behavior for downstream systems
- when deciding whether derived or imported material remains bounded correctly
- when checking whether VEDA is drifting into a cross-system data swamp

---

## Related Docs

- `veda.md`
- `system-invariants.md`
- `observability-and-signal-role.md`
- `evidence-and-source-provenance.md`
- `operator-surfaces.md` *(planned)*
- `mcp-surface.md` *(planned)*
- `../ecosystem/db-posture.md`
- `../ecosystem/cross-system-boundaries.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../governance/auth-and-actor-model.md`
- `../governance/failure-and-recovery-doctrine.md`
