# Ecosystem Database Posture

## Purpose

This document defines the database posture for the V Ecosystem.

It exists to answer:

```text
What database family, physical shape, schema separation model, ownership
boundaries, migration posture, and boundary enforcement rules govern
persistence across the V Ecosystem?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the database engine family posture for the ecosystem
- the physical database shape and schema separation model
- canonical ownership boundaries at the persistence layer
- boundary enforcement mechanisms
- cross-system data access rules
- migration ownership rules
- future onboarding rules for new bounded systems
- future vector-capable and retrieval expansion posture

---

## Out of Scope

This document does not define:

- vendor-specific hosting selection as permanent doctrine
- application-specific ORM or query-library choices
- exact schema design for each bounded system
- backup and restore runbooks in detail
- production sizing, capacity planning, or cost modeling
- detailed Qdrant or retrieval infrastructure posture — that belongs in
  `retrieval-infrastructure-posture.md` once governed

Those belong in system-specific docs, deployment docs, or later operational runbooks.

---

## System

- ecosystem

---

## Core Rule

The V Ecosystem uses one physical PostgreSQL-family database with four schemas,
one per bounded system.

Physical consolidation into one database does not imply shared ownership.
Each schema is an independently governed canonical persistence boundary.
The systems that own those schemas do not share truth because they share infrastructure.

---

## Database Family Rule

The database engine family for core V Ecosystem systems must be PostgreSQL-family.

This rule exists because the ecosystem requires:

- strong relational integrity
- explicit schema discipline
- transaction safety
- deterministic queryability
- clean multi-project isolation support where applicable
- compatibility with multiple access-layer styles
- future vector-capable expansion without re-platforming the ecosystem

A different database family must not be introduced for a core bounded system
unless an explicit governed exception is approved.

---

## Physical Shape Rule

The physical database shape is:

- one shared PostgreSQL-family database instance
- four schemas, one per bounded system

The current schema set is:

- `project_v` — owned by Project V
- `veda` — owned by VEDA
- `veda_strategy` — owned by VEDA Strategy
- `v_forge` — owned by V Forge

Each schema is a hard logical boundary, not a naming convention.
Being in the same database instance does not make schemas interchangeable or
co-owned. A schema is a canonical ownership container, not a folder.

This shape is governed by ADR-012.

---

## Canonical Ownership Rule

Each bounded system owns its own canonical persistence boundary.

This means:

- Project V owns planning and orchestration truth in `project_v`
- VEDA owns signal, evidence, and observability truth in `veda`
- VEDA Strategy owns derived strategic intelligence in `veda_strategy`
- V Forge owns execution truth in `v_forge`

A record has one canonical home.
A system must not treat another system’s schema as an extension of its own domain.

---

## Cross-System Access Rule

Cross-system coordination must not depend on direct schema reach-through.

This means:

- one system must not directly write canonical tables in another system’s schema as a convenience shortcut
- one system must not read another system’s schema as though it were part of its own bounded domain
- cross-system coordination must occur through governed interfaces, governed workflows, or thin explicit references

Thin explicit references are allowed.
Ownership mixing is not.

---

## Imported and Derived Local View Rule

A bounded system may import, cache, or preserve selected external information for local planning, observability, or execution purposes only when that imported material remains explicitly non-canonical outside the receiving system’s own interpretation.

Imported or derived local views must be clearly treated as:

- imported
- derived
- non-canonical outside the receiving system’s own local use

Imported convenience state must not masquerade as canonical truth from the source system.

---

## Credentials and Isolation Rule

Each bounded system must have separate database credentials scoped to its own schema.

Those credentials must be scoped so that one system’s application identity cannot query or mutate another system’s schema by default.

Schema-level credential isolation is a real boundary requirement, not an optional hygiene preference.

This isolation should be verified as an environment and deployment check.

---

## Migration Ownership Rule

Each bounded system owns its own migrations.

This means:

- Project V runs migrations for `project_v`
- VEDA runs migrations for `veda`
- VEDA Strategy runs migrations for `veda_strategy`
- V Forge runs migrations for `v_forge`

One system’s migration runner must not mutate another system’s schema.

Migration tooling may differ between systems.
Migration ownership may not.

---

## Access-Layer Flexibility Rule

The ecosystem standardizes the database family and ownership posture, not one universal access-layer implementation.

This means bounded systems may use different access-layer approaches where appropriate, including:

- direct SQL
- query libraries
- ORMs
- migration frameworks suited to the owning system

Access-layer flexibility is allowed.
Database-family drift is not.

---

## JSON Discipline Rule

JSON may be used only where flexible payload storage is genuinely justified.

Examples include:

- raw external provider payloads
- bounded metadata with legitimately variable structure
- controlled configuration payloads where explicit schema is not the better fit

JSON must not become a substitute for unresolved schema design.
JSON must not become a loophole for smuggling another system’s canonical truth into local storage.

---

## Vector-Capable Future Rule

The ecosystem’s future vector-search and embedding-oriented expansion should remain PostgreSQL-family compatible.

This means:

- future vector capability should be introduced in ways that preserve the ecosystem’s PostgreSQL-family posture
- vector-capable expansion must not be used as a reason to fragment the ecosystem into unrelated storage families without governed justification
- future retrieval improvements should prefer additive extension of the current posture before introducing a separate canonical storage family

The ecosystem should remain vector-capable without requiring a full persistence re-foundation.

---

## Graph-Like Retrieval Rule

Graph-like retrieval, traversal, and relationship reasoning may grow on top of the PostgreSQL-family posture.

The ecosystem must not prematurely treat graph-style future needs as automatic justification for introducing a separate graph database as a new canonical truth home.

A separate graph-oriented component may only be introduced when:

- a concrete requirement exists
- the requirement cannot be met cleanly enough within the current posture
- canonical ownership and boundary rules remain explicit

Future graph-oriented work must remain bounded, not architecture-fashion driven.

---

## Local-to-Hosted Portability Rule

The database posture must remain portable across local and hosted PostgreSQL-family environments.

This means:

- local development may run on standard PostgreSQL-family infrastructure
- hosted deployment may use a PostgreSQL-family managed provider
- ecosystem doctrine must remain PostgreSQL-family based, not dependent on one vendor’s special features unless explicitly approved later

Vendor alignment is allowed.
Vendor lock as hidden doctrine is not.

---

## Future System Onboarding Rule

A new bounded system joining the V Ecosystem should normally receive:

- its own schema inside the shared PostgreSQL-family database
- its own migration ownership
- its own canonical persistence boundary
- its own bounded system doctrine

A new bounded system must not be onboarded by casually sharing another system’s canonical schema as a convenience shortcut.

If an exception is proposed, that exception must be explicit, governed, and justified.

---

## Verification Rule

This posture must be verified, not merely declared.

Verification should include:

- confirming that each system uses its own schema
- confirming that one system’s credentials cannot query another system’s schema by default
- confirming that migration runners are scoped to the owning system’s schema
- confirming that cross-system coordination occurs through governed boundaries rather than hidden DB shortcuts

A declared boundary that is not verified is weak architecture.

---

## Failure and Drift Rule

The ecosystem database posture has drifted if:

- multiple bounded systems begin storing mixed canonical truth across schemas by convenience
- one system begins writing directly into another system’s canonical tables
- one system’s credentials can freely reach into another system’s schema without governed reason
- JSON blobs become a storage loophole for cross-boundary truth copying
- a new bounded system is added without its own schema and persistence boundary
- vendor-specific convenience becomes hidden doctrine without explicit approval

These are not harmless shortcuts.
They are persistence-boundary failures.

---

## Human-In-The-Loop Principle

Changes to ecosystem database posture should remain human-governed.

Human review remains especially important for:

- introducing a new bounded system
- changing the engine family posture
- proposing cross-system database exceptions
- altering migration ownership rules
- introducing vendor-specific dependencies that reduce portability

Database posture is too load-bearing to drift through convenience decisions.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- the ecosystem uses one physical PostgreSQL-family database with four schemas
- each bounded system owns its own schema; physical consolidation does not mean shared ownership
- canonical ownership stays separated by schema and enforced by credentials, service boundaries, and API enforcement
- cross-system direct schema access is forbidden
- migration ownership stays local to the owning system’s schema
- future vector capability should be added without fragmenting the database family casually
- future onboarded systems normally receive their own schema and persistence boundary

If an LLM could read this posture as permission to mix canonical truth across schemas because they share one database instance, this document is failing.

---

## Usage

This document should be used:

- when deciding database posture for current ecosystem systems
- when onboarding a new bounded system into the ecosystem
- when reviewing whether a storage proposal preserves system boundaries
- when deciding whether a vendor or tooling decision is compatible with ecosystem doctrine
- when checking whether persistence convenience is eroding bounded ownership

---

## Related Docs

- `v-ecosystem-overview.md`
- `cross-system-boundaries.md`
- `decisions/ADR-012-single-postgres-multi-schema.md`
- `../project-v/project-v.md`
- `../veda/veda.md`
- `../veda-strategy/veda-strategy.md`
- `../v-forge/v-forge.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../archive/planning-source/process-rules.md`
