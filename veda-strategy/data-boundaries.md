# VEDA Strategy Data Boundaries

## Purpose

This document defines the data ownership boundaries for VEDA Strategy inside
the V Ecosystem.

It exists to answer:

```text
What data does VEDA Strategy canonically own, what data may it read from other
systems without owning, what must it never store as canonical truth, and what
boundary rules prevent VEDA Strategy from becoming a second observatory, a shadow
planner, or an execution ledger?
```

This is a Tier 2 system core authority document.

---

## Scope

This document governs:

- what data VEDA Strategy canonically owns in `veda_strategy.*`
- what data VEDA Strategy may read from VEDA without owning
- what data VEDA Strategy must not store or model
- how VEDA Strategy's data boundaries relate to VEDA, Project V, and V Forge
- boundary drift patterns that are forbidden

---

## Out of Scope

This document does not define:

- the exact schema of every VEDA Strategy table
- the detailed payload format of every strategic signal package
- the full interface rules for every downstream consumer
- implementation details

Those belong in `schema-authority.md`, interface docs, and implementation docs.

---

## System

- veda_strategy

---

## Core Rule

VEDA Strategy canonically owns derived strategic intelligence.

It reads from VEDA's observatory truth and produces bounded derived records
in `veda_strategy.*`. Those derived records are VEDA Strategy's canonical truth —
they are the output of the derivation process, not copies of VEDA's evidence.

VEDA Strategy must not absorb observatory truth from VEDA, planning truth from
Project V, or execution truth from V Forge.

---

## Canonical Ownership Rule

VEDA Strategy canonically owns data that directly represents derived strategic
intelligence such as:

- opportunity scoring records
- content gap detection records at the strategic level
- clustering records
- competitive analysis records
- strategic signal packages produced for Project V and V Forge
- derivation metadata that preserves the evidence basis for strategic outputs

### Rule
Canonical VEDA Strategy data must remain bounded to derived intelligence.
If a proposed record would naturally be queried to answer "what did VEDA observe?"
or "what did Project V decide?" or "what did V Forge build?", it does not belong
in `veda_strategy.*`.

---

## Read-Without-Ownership Rule

VEDA Strategy may read VEDA's observatory truth through governed interfaces
without acquiring ownership of that truth.

This means VEDA Strategy may consume:

- SERP snapshots and search performance observations from VEDA
- keyword intelligence and volatility signals from VEDA
- source capture records from VEDA where relevant to scoring or gap detection
- any other bounded VEDA observatory outputs delivered through the governed interface

### Rule
Reading VEDA's canonical records does not transfer ownership of those records
to VEDA Strategy. VEDA remains the canonical owner of all observatory truth.
VEDA Strategy must not re-store VEDA's canonical records in `veda_strategy.*`
as though they were VEDA Strategy's own canonical data.

A local working copy of VEDA signal used within a single derivation operation
is acceptable. A persistent duplicate of VEDA's canonical records stored in
`veda_strategy.*` is a boundary violation.

---

## Derivation Boundary Rule

VEDA Strategy's canonical outputs are derived from VEDA's observatory truth.

The derivation must be traceable. VEDA Strategy records should preserve enough
provenance context to answer:

- what VEDA evidence or signal fed this derivation?
- what time window or snapshot basis does this output cover?
- is this output direct or multi-step derived?

Derived output that cannot be traced back to VEDA observatory evidence is
not well-grounded VEDA Strategy output.

### Rule
VEDA Strategy's derivation produces new records in `veda_strategy.*`.
Those records are VEDA Strategy's canonical truth — the scored opportunity,
the detected gap, the clustered signal.
They are not copies of the VEDA evidence they were derived from.
The VEDA evidence remains in `veda.*`.

---

## Forbidden Boundary Patterns

### Second observatory
VEDA Strategy must not accumulate raw SERP data, raw GA4 data, raw Search Console
data, or other raw observatory records as though it were a second VEDA.
If VEDA Strategy finds itself storing raw observatory payloads, it has drifted
into observatory territory.

### Shadow planner
VEDA Strategy must not store planning decisions, project approval records,
orchestration state, or readiness evaluations. Those belong to Project V.
A strategic signal package from VEDA Strategy that reaches Project V remains
a VEDA Strategy record until Project V acts on it. The resulting planning
decision is a Project V record, not a VEDA Strategy record.

### Execution ledger
VEDA Strategy must not store execution task state, content graph records,
or execution intelligence outputs. Those belong to V Forge.
A strategic signal package from VEDA Strategy that reaches V Forge remains
a VEDA Strategy record until V Forge acts on it. The resulting execution
decision is a V Forge record.

### Canonical duplication
VEDA Strategy must not normalize a copy of VEDA's canonical tables into its
own schema as a convenience. Even well-labeled duplicate records gradually
become treated as canonical. The boundary must be structural, not doctrinal only.

---

## Cross-System Reference Rule

When VEDA Strategy records reference entities owned by VEDA, Project V, or
V Forge, those references must remain thin: a locator or identifier pointing
to the owning system's canonical record, not a copy of that record's content.

A VEDA Strategy scoring record may reference the VEDA evidence records that
supported the score. That reference is a thin pointer — the VEDA evidence
record identity and the timestamp of the observation — not a copy of the
VEDA evidence payload.

---

## Relationship to `veda_strategy.*` Schema

VEDA Strategy's canonical records live in the `veda_strategy` schema of the
shared PostgreSQL database. That schema is VEDA Strategy's persistence boundary.

VEDA Strategy's migrations run for `veda_strategy.*` only. They must not mutate
`veda.*`, `project_v.*`, or `v_forge.*`.

The specific record families and their field-level shapes belong in
`schema-authority.md`.

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- VEDA Strategy owns derived intelligence, not observatory truth
- VEDA Strategy reads from VEDA; it does not copy VEDA's canonical records
- derivation outputs are canonical VEDA Strategy data; the underlying VEDA
  evidence remains canonical VEDA data
- thin cross-system references are allowed; ownership duplication is not
- VEDA Strategy must not behave as a second observatory, shadow planner,
  or execution ledger

If a schema design would make `veda_strategy.*` look like a mirror of `veda.*`,
a subset of `project_v.*`, or a shadow of `v_forge.*`, this doc is being ignored.

---

## Usage

This document should be used:

- when deciding whether a proposed VEDA Strategy record belongs in `veda_strategy.*`
- when reviewing whether a schema change would pull VEDA's observatory truth
  into VEDA Strategy ownership
- when checking whether cross-system references remain thin
- when evaluating whether VEDA Strategy is drifting into observatory, planning,
  or execution territory

---

## Related Docs

- `veda-strategy.md`
- `schema-authority.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/db-posture.md`
- `../ecosystem/ecosystem-schema-spine.md`
- `../interfaces/data-boundaries.md`
- `../veda/data-boundaries.md`
- `../veda/veda.md`
- `../interfaces/veda-strategy-to-project-v-signal-interface.md`
- `../interfaces/veda-strategy-to-v-forge-signal-interface.md`
