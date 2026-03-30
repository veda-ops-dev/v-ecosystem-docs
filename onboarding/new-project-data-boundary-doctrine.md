# New Project Data Boundary Doctrine

## Purpose

This document defines the data boundary posture a new project must establish before it is admitted into the V Ecosystem.

It exists to answer:

```text
What data may a new project store canonically, what may it reference or interpret without owning, what must remain entirely outside it, and how is that posture established and verified before admission?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the data boundary posture required of any new project before admission
- how canonical ownership, bounded reference, interpretation, imported convenience data, and out-of-bounds data are distinguished for a new project
- how a new project's data posture relates to existing ecosystem system ownership
- the anti-drift rules operators and LLMs must preserve when evaluating a candidate project's data claims
- how data boundary posture is verified during onboarding

---

## Out of Scope

This document does not define:

- exact schema or table design for admitted projects
- detailed database hosting or cluster configuration
- the internal data models of Project V, VEDA, or V Forge
- post-admission schema governance workflows

Those belong in project-specific data-boundaries docs, schema-authority docs, and the ecosystem db-posture doc.

---

## System

- onboarding

---

## Core Rule

A new project must define its data boundary posture before admission.

Data boundary posture is not inferred from role alone.
It must be explicit, bounded, and honest about what the project owns, what it references, and what must remain outside it.

A project with an unclear data boundary posture is not ready for admission.
Unclear data posture almost always means unclear truth ownership, which means classification is not complete.

---

## Data Boundary Definition

A data boundary defines whether a category of data is:

- **canonically owned** by the new project
- **referenced** by the new project without ownership transfer
- **interpreted** as the project's own operational or planning output
- **imported** as explicitly non-canonical convenience material
- **out of bounds** and must not be stored or claimed by the new project

Every meaningful data category the project touches must be placed into one of these five.
If a data category cannot be placed clearly, the boundary is too weak for admission.

---

## Relationship to Classification

Data boundary posture follows directly from classification.

A project classified as a real new ecosystem project must state:

- what data it canonically owns as that system
- what data it references from other systems
- what external data it may interpret without owning
- what data is entirely outside its ownership posture

A project classified as an existing-system feature cluster, workflow refinement, or tool surface must not claim canonical data ownership for data that belongs to the existing system it serves.

### Rule
The data boundary posture must be consistent with the project's classification outcome.
If a project's data claims are broader than its classification justifies, either the classification is wrong or the data posture is wrong.
One of them must be corrected before admission.

---

## Canonical Data Ownership Rule

A new project may canonically own only data that belongs to its classified truth domain.

This means:

- if the project owns a distinct truth domain not already owned by Project V, VEDA, or V Forge, it may own data that represents that truth
- the owned data must remain bounded to that truth domain
- the project must not expand canonical ownership by gradually absorbing data that answers questions belonging to another system

### Rule
Canonical ownership is determined by truth domain, not by storage location.
A project does not become the canonical owner of data merely because it stores it.
It becomes the canonical owner because its classified role makes it the system of record for that data class.

---

## Forbidden Canonical Ownership Claims

A new project must not claim canonical ownership of:

- observability truth, evidence truth, or signal records owned by VEDA
- planning truth, orchestration truth, readiness truth, or decision records owned by Project V
- execution truth, production workflow truth, or execution ledger records owned by V Forge
- convenience copies of data primarily answering questions that belong to another system

### Rule
A candidate that claims canonical ownership of data belonging to an existing system is either misclassified and should be absorbed into the appropriate existing system, or attempting to duplicate an existing system role under a different name.
Neither justifies admission as a new project.

---

## Bounded Reference Rule

A new project may reference external data without owning it.

Examples include:

- a locator or identifier pointing to a VEDA evidence record
- a reference to a Project V planning record for coordination purposes
- a bounded external link supporting traceability or handoff clarity

### Rule
A reference is not ownership.
References must remain:

- explicit — clearly identified as references to external truth, not local copies of it
- directional — pointing toward the owning system
- bounded — scoped to what the project's classified role requires
- honest — not used to overclaim ownership or to mirror foreign data locally

If accumulated references begin to reproduce the shape of another system's canonical data, they have crossed from reference into shadow ownership.

---

## Interpretation Rule

A new project may store its own interpretations of external inputs as canonical truth within its own domain.

A planning conclusion derived from signal inputs may be canonical for the system that owns planning.
An operational judgment derived from evidence may be canonical for the system that owns that decision domain.

### Rule
The interpretation may be canonical to the new project.
The underlying external data it was derived from does not transfer ownership to the new project.
A project may not treat the act of interpretation as permission to absorb or mirror the source data it interpreted.

---

## Imported Convenience Data Rule

A new project may persist limited imported or convenience data only when:

- the material is clearly labeled as imported and non-canonical outside the project's own domain
- it is bounded to a specific governed record family or purpose
- it cannot be mistaken for the project's own canonical truth
- staleness of the imported material is handled honestly

### Rule
Imported convenience data must not grow into a shadow copy of another system's canonical data.
Each import decision should be evaluated against whether accumulated imports are moving toward a duplicate truth store.
If imported material begins to answer questions that belong to another system, the import posture has drifted into ownership.

---

## Out-of-Bounds Data Rule

The following categories are out of bounds for canonical ownership by any new project unless the project is specifically classified and admitted to own them:

- raw observability payloads owned by VEDA
- observatory event ledgers owned by VEDA
- source-capture and evidence records owned by VEDA
- planning state, decision records, and readiness records owned by Project V
- execution state, draft workflow, and production asset lifecycle owned by V Forge
- rich source-control history as canonical project truth
- convenience mirrors of multi-system state that make the new project a de-facto data aggregator

### Rule
If a proposed data category would naturally be queried to answer "what happened in VEDA?", "what is planned in Project V?", or "what is executing in V Forge?", it is out of bounds for a new project's canonical ownership.

---

## Multi-Project and Project-Scope Rule

A new project's data must preserve explicit project scope where the concept is project-scoped.

This means:

- project-scoped data rows must belong to exactly one project
- the new project must not create ambiguous cross-project data links
- data from another project's scope must not be accepted without explicit governed handling
- data must be classifiable by project scope before it is treated as governed canonical data

Where a new project's classified truth domain is intentionally global rather than project-scoped, the project must justify the global posture explicitly and demonstrate that global scope is required by its role rather than chosen for convenience. Global data posture requires the same justification standard as global tables in existing systems.

### Rule
If data cannot be classified by project scope clearly, it is not safe enough to treat as governed canonical data for the new project.

---

## Data Freshness and Staleness Rule

A new project that relies on external or imported material must not silently assume that material remains fresh.

When staleness of imported or referenced data would materially affect the project's own operations or claims, the project must:

- surface a gap or warning
- mark its own confidence as stale
- trigger reconsideration through the governed path

Staleness is material when the imported or referenced data, if known to be stale, would change what the project claims, decides, or recommends in its classified truth domain. The same materiality standard used in `../governance/decision-continuity-doctrine.md` applies here: a change is material when it would have been decision-relevant at the time the claim was made.

### Rule
Stale external data does not become safe to rely on merely because it has been stored locally.
Staleness must be handled as a first-class concern, not deferred as eventual cleanup.

---

## Data Boundary Verification Rule

Before admission, the candidate project's data boundary posture must be verifiable.

Verification includes confirming that:

- canonical ownership claims are consistent with the project's classified truth domain
- no canonical ownership is claimed over data belonging to an existing system
- references are clearly identified as references and not overclaiming ownership
- imported material is explicitly bounded and labeled as non-canonical
- out-of-bounds categories are named and excluded
- project-scope handling is explicit

### Rule
A data boundary posture that exists only in conversation or informal notes is not verified.
It must be documented in the shared root as part of the project's required-docs set before admission.

---

## JSON and Flexible Payload Rule

A new project may use JSON or flexible payload storage only where bounded variability is genuinely justified.

JSON must not become:

- a hiding place for unresolved ownership decisions
- a loophole for storing out-of-bounds observability or execution data
- a mechanism for evading explicit schema and data-boundary discipline

### Rule
If a payload is important enough to govern, query, validate, or classify repeatedly, it belongs in explicit bounded schema or it should remain outside the new project entirely.

---

## Relationship to Existing System Data Boundaries

Each existing system has its own canonical data boundary doctrine:

- Project V data boundaries: `../project-v/data-boundaries.md`
- VEDA data boundaries: `../veda/data-boundaries.md`
- V Forge data posture: `../v-forge/system-invariants.md` and `../v-forge/operational-model.md`

A new project's data boundary posture must not conflict with those existing boundaries.

### Rule
Where a new project's proposed data posture overlaps with an existing system's canonical boundary doc, the conflict must be resolved explicitly before admission.
Overlap is disqualifying if resolving it requires the new project to absorb data that belongs to an existing system.

---

## Data Boundary Failure Modes (Explicitly Forbidden)

The following are data boundary failures for any new project:

- claiming canonical ownership of data that belongs to Project V, VEDA, or V Forge
- using references to accumulate a mirror of another system's canonical data
- treating imported convenience data as canonical truth after enough time or volume has passed
- using JSON to bypass explicit ownership decisions
- letting accumulated imports substitute for the genuine system of record for a data class
- asserting data ownership based on storage location rather than classified truth domain
- admitting a project without an explicit, documented, and verified data boundary posture

---

## Human-In-The-Loop Principle

Data boundary posture is governance-sensitive because it determines what the new project is allowed to become over time.

Human review may be required where a candidate project's data posture would:

- claim ownership of a genuinely new data class not yet owned by any existing system
- import or reference data from multiple existing systems in a pattern suggesting aggregation
- propose flexible or JSON-heavy storage that resists clear ownership classification
- expand canonical ownership beyond what was documented at admission

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- data boundary posture must be explicit before admission, not inferred from role alone
- canonical ownership follows classified truth domain, not storage location
- references, interpretations, and imports are allowed but must not accumulate into ownership
- out-of-bounds categories for new projects mirror the existing systems' forbidden data categories
- a data boundary posture that cannot be documented cannot be verified and therefore cannot support admission

If a new project's data posture starts to resemble a blended version of Project V, VEDA, and V Forge data, both the classification and the data boundary are wrong.

---

## Usage

This document should be used:

- when evaluating whether a candidate project has a sound data boundary posture before admission
- when reviewing whether a project's data claims are consistent with its classification outcome
- when determining whether proposed data storage is canonical, referenced, interpreted, imported, or out of bounds
- when rejecting data postures that overclaim ownership or accumulate toward aggregation drift
- when writing a candidate project's own data-boundaries doc as part of its required-docs set

---

## Related Docs

- `new-project-onboarding-doctrine.md`
- `new-project-classification-model.md`
- `new-project-required-docs.md`
- `new-project-access-and-boundary-rules.md`
- `new-project-lifecycle-and-fitment-review.md` *(planned)*
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
- `../ecosystem/db-posture.md`
- `../project-v/data-boundaries.md`
- `../veda/data-boundaries.md`
- `../v-forge/system-invariants.md`
- `../governance/approval-and-escalation-model.md`
