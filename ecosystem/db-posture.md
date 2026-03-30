# Ecosystem Database Posture

## Purpose

This document defines the database posture for the V Ecosystem.

It exists to answer:

```text
What database family, cluster shape, ownership boundaries, migration posture, and future expansion rules should govern persistence across the V Ecosystem?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the database engine family posture for the ecosystem
- the cluster and database separation model
- canonical ownership boundaries at the persistence layer
- cross-system database access rules
- migration ownership rules
- future onboarding rules for new bounded systems
- future vector-capable expansion posture

---

## Out of Scope

This document does not define:

- vendor-specific hosting selection as permanent doctrine
- application-specific ORM or query-library choices
- exact schema design for each bounded system
- backup and restore runbooks in detail
- production sizing, capacity planning, or cost modeling

Those belong in system-specific docs, deployment docs, or later operational runbooks.

---

## System

- ecosystem

---

## Core Rule

The V Ecosystem standardizes on a PostgreSQL-family database posture.

The ecosystem uses one shared PostgreSQL-family cluster with one separate database per bounded system.

Canonical truth must remain separated by bounded system.
Shared infrastructure is allowed.
Shared canonical ownership is not.

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

A different database family must not be introduced for a core bounded system unless an explicit governed exception is approved.

---

## Cluster Shape Rule

The standard cluster shape is:

- one shared PostgreSQL-family cluster
- one separate database per bounded system

The initial ecosystem database shape is:

- `project_v` for Project V
- `veda` for VEDA
- `v_forge` for V Forge

Future bounded systems should normally follow the same shape.

This rule preserves bounded ownership while keeping infrastructure reasonably simple.

---

## Canonical Ownership Rule

Each bounded system owns its own canonical persistence boundary.

This means:

- Project V owns planning and orchestration truth in `project_v`
- VEDA owns signal, evidence, and observability truth in `veda`
- V Forge owns execution truth in `v_forge`

A record has one canonical home.
A system must not treat another system’s database as an extension of its own domain.

---

## Cross-System Access Rule

Cross-system coordination must not depend on direct database reach-through.

This means:

- one system must not directly write canonical tables in another system’s database as a convenience shortcut
- one system must not read another system’s database as though it were part of its own bounded schema
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

Each bounded system should have separate database credentials.

Those credentials must be scoped so that one system’s application identity cannot query or mutate another system’s database by default.

Cross-database credential isolation is a real boundary requirement, not an optional hygiene preference.

This isolation should be verified as an environment and deployment check.

---

## Migration Ownership Rule

Each bounded system owns its own migrations.

This means:

- Project V runs migrations for `project_v`
- VEDA runs migrations for `veda`
- V Forge runs migrations for `v_forge`

One system’s migration runner must not mutate another system’s database.

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

- its own database inside the shared PostgreSQL-family cluster
- its own migration ownership
- its own canonical persistence boundary
- its own bounded system doctrine

A new bounded system must not be onboarded by casually sharing another system’s canonical database as a convenience shortcut.

If an exception is proposed, that exception must be explicit, governed, and justified.

---

## Verification Rule

This posture must be verified, not merely declared.

Verification should include:

- confirming that each system uses its own database
- confirming that one system’s credentials cannot query another system’s database by default
- confirming that migration runners are scoped to the owning system’s database
- confirming that cross-system coordination occurs through governed boundaries rather than hidden DB shortcuts

A declared boundary that is not verified is weak architecture.

---

## Failure and Drift Rule

The ecosystem database posture has drifted if:

- multiple bounded systems begin storing mixed canonical truth in the same database by convenience
- one system begins writing directly into another system’s canonical tables
- one system’s credentials can freely reach into another system’s database without governed reason
- JSON blobs become a storage loophole for cross-boundary truth copying
- a new bounded system is added without its own persistence boundary
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

- the ecosystem standardizes on PostgreSQL-family infrastructure
- each bounded system gets its own database
- canonical ownership stays separated by system
- cross-system direct DB shortcuts are forbidden
- migration ownership stays local to the owning system
- future vector capability should be added without fragmenting the database family casually
- future onboarded systems normally receive their own persistence boundary

If an LLM could read this posture as permission to mix canonical truth across systems inside one convenience database, this document is failing.

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
- `../project-v/project-v.md`
- `../veda/veda.md`
- `../v-forge/v-forge.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../archive/planning-source/process-rules.md`
