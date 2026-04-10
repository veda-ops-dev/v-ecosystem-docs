# VEDA Strategy Schema Authority

## Purpose

This document defines the first-pass schema authority for VEDA Strategy.

It exists to answer:

```text
What record families does VEDA Strategy canonically own in `veda_strategy.*`,
what is the ownership and scope posture for each family, and what structural
rules must the schema preserve?
```

This is a Tier 2 system core authority document.

---

## Scope

This document governs:

- the canonical first-pass record families VEDA Strategy owns
- the meaning and ownership posture of each record family
- the structural rules the schema must preserve
- anti-drift constraints that keep `veda_strategy.*` bounded to derived
  strategic intelligence

---

## Out of Scope

This document does not define:

- exact columns, exact SQL types, or exact indexes for every field
- detailed migration sequencing
- detailed endpoint contracts
- VEDA schema design — that belongs in `../veda/schema-reference.md`
- Project V schema design — that belongs in `../project-v/schema-authority.md`
- V Forge schema design — that belongs in V Forge schema authority docs

Those belong in more specific schema-specification, migration, API, and
system-specific docs.

---

## System

- veda_strategy

---

## Core Rule

VEDA Strategy schema must model only derived strategic intelligence that VEDA
Strategy owns.

VEDA Strategy schema must not model:

- raw observatory truth — that belongs in `veda.*`
- planning or orchestration truth — that belongs in `project_v.*`
- execution truth or content graph truth — that belongs in `v_forge.*`
- convenience copies of another system's canonical records

The `veda_strategy.*` schema exists to hold the outputs of derivation —
scored opportunities, detected gaps, clustered signals, competitive analysis
records — not the observatory inputs those derivations consumed.

---

## Schema Authority Rule

This document is the canonical authority for the first-pass VEDA Strategy
schema posture.

If implementation, migrations, or schema ideas diverge from this document,
the divergence must be reviewed explicitly.

Schema authority must not be inferred from:

- ad hoc local schema decisions
- convenience tables created during implementation
- old assumptions about VEDA Brain capabilities

If a proposed record family is not justified here, it is not yet governed schema.

---

## Ownership and Scope Classification

Every VEDA Strategy table must be classifiable as one of:

- **project-scoped** — belongs to exactly one project
- **intentionally global** — rare, justified, not project-specific

Project-scoped tables are the default. Global tables must be explicitly justified.

---

## Canonical First-Pass Record Families

The following record families constitute the governed first-pass schema for
VEDA Strategy. These are the record families needed to support VEDA Strategy's
core role. Implementation detail — exact columns, constraints, indexes — belongs
in a companion schema-specification doc to be created when implementation begins.

---

### 1. `OpportunityScore`

**Scope:** Project-scoped.

**Purpose:** Represents a scored opportunity candidate derived from VEDA
observatory truth. Records the scoring dimensions, the evidence basis, and
the resulting score for a bounded opportunity at a point in time.

**Posture:**
- append-friendly: a new score for the same opportunity produces a new record,
  preserving scoring history
- must carry derivation provenance: which VEDA evidence records or signal
  packages informed this score, and over what time window
- must not store copies of VEDA canonical records — only thin references to them

**What it does not model:**
- the VEDA observatory evidence that fed the score — that stays in `veda.*`
- whether a project was created as a result — that belongs in `project_v.*`

---

### 2. `ContentGapSignal`

**Scope:** Project-scoped.

**Purpose:** Represents a detected gap at the strategic level — a topic area,
query space, or market condition where the project's current coverage appears
insufficient relative to observed signal.

This is strategic-level gap detection, not execution-side gap detection.
Execution-side gap detection (comparing the content graph against VEDA signal)
belongs to V Forge's execution intelligence layer.

**Posture:**
- must carry derivation provenance linking to VEDA signal basis
- must be clearly distinguishable from execution-side gap records in V Forge
- must not store the VEDA signal it was derived from

**What it does not model:**
- execution gaps identified by crossing the content graph against VEDA signal —
  those belong in V Forge
- planning decisions about whether to address the gap — those belong in Project V

---

### 3. `ClusterRecord`

**Scope:** Project-scoped.

**Purpose:** Represents a clustered grouping of signals, topics, or opportunity
candidates derived from VEDA observatory truth. Clustering supports opportunity
discovery and competitive analysis by revealing patterns across the signal space.

**Posture:**
- derived from VEDA signal; must carry derivation provenance
- the cluster itself is VEDA Strategy's derived output; the constituent signals
  remain owned by VEDA
- cluster records are point-in-time derivations; updating a cluster produces
  a new record or a versioned update, not a silent overwrite

---

### 4. `CompetitiveAnalysisRecord`

**Scope:** Project-scoped.

**Purpose:** Represents a bounded competitive analysis output derived from VEDA
observatory truth — SERP composition observations, competitor presence signals,
or market positioning analysis at the strategic level.

**Posture:**
- derived from VEDA SERP and observatory data; must carry derivation provenance
- must not store VEDA SERP snapshots directly — only thin references and derived conclusions
- competitive analysis conclusions are VEDA Strategy's canonical truth; the
  underlying SERP data remains VEDA's canonical truth

---

### 5. `StrategicSignalPackage`

**Scope:** Project-scoped.

**Purpose:** Represents a packaged strategic signal delivery — a bounded package
of VEDA Strategy-derived intelligence prepared for delivery to Project V or V Forge
through a governed interface.

This is the record family that corresponds to the `strategic_signal_package`
entity type in `ecosystem/ecosystem-schema-spine.md`.

**Posture:**
- represents the delivery package, not the underlying derived records
- carries references to the underlying derived records (OpportunityScore,
  ContentGapSignal, etc.) that make up the package
- carries delivery metadata: target system, delivery status, provenance summary
- append-only: a new package for the same project is a new record

**What it does not model:**
- the planning or execution decision that follows delivery — that belongs in the
  receiving system

---

## Structural Rules

### 1. Project-scoped by default
All VEDA Strategy tables are project-scoped unless explicitly documented as global.
Every project-scoped row must carry a valid `projectId` reference.

### 2. Provenance is required on derived records
Every derived record family must carry enough provenance to trace the derivation
back to the VEDA evidence or signal that produced it. Derivation without traceable
provenance is ungoverned intelligence.

### 3. VEDA canonical records must not be duplicated
No VEDA Strategy table may store a copy of a VEDA canonical record. Cross-system
references use thin identifiers or locators, not payload copies.

### 4. Schema expansion requires governance review
Adding a new record family to `veda_strategy.*` requires updating this document.
A table created locally in implementation without corresponding authority
documentation is ungoverned schema.

### 5. The boundary with execution-side gap detection must remain explicit
`ContentGapSignal` records are strategic-level outputs. They must not be confused
with or merged with V Forge execution-side gap detection records. The distinction
is: strategic gap detection operates at the market-and-opportunity level; execution
gap detection operates at the content-graph level. Both are necessary; neither
replaces the other.

---

## Anti-Drift Rules

### Rule 1 — Test every proposed table against the derivation pattern
Before adding a new table, ask: does this record represent something VEDA Strategy
derived from VEDA observatory truth? If it could be answered "this is what VEDA
observed" or "this is what Project V decided" or "this is what V Forge built",
it does not belong here.

### Rule 2 — VEDA Brain must not re-enter through schema
A table that materializes planning proposals, direct project creation records,
or content production instructions is VEDA Brain behavior. It does not belong in
`veda_strategy.*`. If the record is needed, it belongs in Project V or V Forge.

### Rule 3 — Scoring, gap detection, clustering, and competitive analysis stay bounded
These are the four owned capability domains. Schema expansion should stay within
these domains. New domains require explicit governance rather than implementation
convenience.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- `veda_strategy.*` holds derived intelligence — scored outputs, gap signals,
  clusters, competitive analysis, and delivery packages
- it does not hold observatory records, planning records, or execution records
- every derived record must carry provenance traceable to VEDA evidence
- VEDA canonical records must not be duplicated here
- schema expansion requires updating this document, not local implementation decisions

If schema design makes `veda_strategy.*` look like a VEDA mirror, a Project V
planning ledger, or a V Forge execution tracker, this document is being ignored.

---

## Usage

This document should be used:

- when deciding whether a proposed record family belongs in VEDA Strategy schema
- when writing companion schema-specification or migration docs
- when reviewing whether a proposed schema addition preserves derivation boundaries
- when checking whether VEDA Strategy schema is drifting toward observatory,
  planning, or execution territory

---

## Related Docs

- `veda-strategy.md`
- `data-boundaries.md`
- `../ecosystem/ecosystem-schema-spine.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/db-posture.md`
- `../interfaces/data-boundaries.md`
- `../veda/schema-reference.md`
- `../interfaces/veda-strategy-to-project-v-signal-interface.md`
- `../interfaces/veda-strategy-to-v-forge-signal-interface.md`
