# Project V Data Boundaries

## Purpose

This document defines the data-boundary posture Project V must preserve inside the V Ecosystem.

It exists to answer:

```text
What data may Project V store canonically, what data may it reference or interpret, what data must remain outside it, and what rules prevent boundary drift at the persistence layer?
```

This is a Tier 2 project core authority document.

---

## Scope

This document governs:

- what categories of data Project V may store canonically
- what categories of data Project V may reference, import, or interpret without owning canonically
- what categories of data must remain outside Project V ownership
- how cross-system data references, imported convenience data, and planning-side interpretations must remain honest
- the anti-drift rules operators and LLMs must preserve when designing Project V persistence behavior

---

## Out of Scope

This document does not define:

- exact table schemas
- exact API contracts
- detailed VEDA data modeling
- detailed V Forge data modeling
- detailed cross-system auth mechanics

Those belong in schema, interface, integration, and governance docs.

---

## System

- project-v

---

## Core Rule

Project V may store only canonical planning and orchestration truth that belongs to Project V.

Project V may reference external truth, interpret external truth for planning purposes, and preserve thin bounded linkage to external systems.

Project V must not become the canonical owner of:

- VEDA observability truth
- VEDA canonical evidence truth
- V Forge execution truth
- V Forge production workflow truth
- convenience copies of another bounded system's state masquerading as Project V truth

If data primarily answers a planning-and-orchestration question, it may belong in Project V.
If it primarily answers an observability question, it belongs in VEDA.
If it primarily answers an execution or production question, it belongs in V Forge.

---

## Data Boundary Definition

A Project V data boundary is the rule that determines whether a category of data is:

- canonically owned by Project V
- allowed only as a bounded reference
- allowed only as a planning-side interpretation
- allowed only as imported, explicitly non-canonical convenience data
- entirely out of bounds for Project V persistence

A data-boundary rule is not a storage preference.
It is an ownership rule.

---

## Canonical Project V Data

Project V may canonically own data that directly represents planning and orchestration truth such as:

- project planning identity
- objectives
- initiatives
- work items
- dependencies
- decision records
- readiness evaluations
- readiness gaps
- audit runs
- audit gaps
- handoff records
- status history for governed planning-side transitions
- research docs used for planning support
- evidence links used to support planning rationale

### Rule
Canonical Project V data must remain bounded to planning and orchestration truth.
If a proposed data category starts representing observed reality, execution-state internals, or publishing workflow internals, it is out of bounds.

---

## Allowed Planning-Side Interpretations

Project V may store planning-side interpretations derived from external inputs where those interpretations are themselves Project V truth.

Examples include:

- a planning decision informed by VEDA evidence
- a readiness judgment informed by evidence or external references
- a handoff rationale informed by external context
- a planning-side invalidation finding caused by stale linkage or changed conditions
- a bounded summary of what a referenced external record means for planning

### Rule
The interpretation may belong to Project V.
The underlying external truth does not transfer ownership just because Project V interpreted it.

---

## Allowed Bounded References

Project V may store explicit references to external or cross-system data where those references preserve planning-side clarity.

Examples include:

- a VEDA identifier or locator referenced by an `EvidenceLink`
- a V Forge identifier or locator referenced by a `Handoff` or `ExternalLink`
- a repository, issue, pull request, or other execution-facing reference used for bounded implementation traceability
- an external document locator used for planning support research

Thin external linkage records such as `ExternalLink` are bounded references, not canonical Project V data. They are allowed because they preserve planning-side traceability, but they do not represent Project V-owned planning truth. They point toward truth owned elsewhere.

### Rule
A reference is not ownership.
A bounded reference must remain:

- explicit
- directional
- project-scoped where relevant
- honest about what system owns the referenced truth

---

## Allowed Imported Convenience Data

Project V may persist selected imported or convenience data only when the imported material is clearly treated as:

- imported
- derived
- non-canonical outside Project V's own planning interpretation
- bounded to a governed Project V record family

### First-Pass Allowed Shapes
Imported convenience data must remain bounded to governed Project V shapes such as:

- `ResearchDoc`
- `EvidenceLink`
- other explicitly governed Project V record families if later approved

### Rule
Imported convenience data must not masquerade as live canonical VEDA or V Forge truth.
Non-canonical posture means Project V may use imported material to support planning decisions but must not expose it as Project V-owned source of record. Project V must not build API surfaces that present imported material as Project V truth, must not use imported material as the authoritative basis for readiness or handoff claims without explicitly preserving its non-canonical status, and must not allow imported material to become the working substitute for the actual source system.
If imported material is stale, incomplete, or insufficient for a planning claim, Project V must treat that as a planning-side gap, warning, or invalidation condition rather than silently overclaiming freshness or ownership.

---

## Out-of-Bounds Data Categories

The following categories are out of bounds for canonical Project V persistence:

- raw SERP observation data
- raw GA4 observation data
- raw Search Console observation data
- raw crawl/indexation observation data
- raw YouTube observation data
- raw LLM-citation observation data
- raw observatory event ledgers owned by VEDA
- draft content bodies owned by V Forge
- editorial workflow state owned by V Forge
- publishing workflow state owned by V Forge
- produced asset lifecycle state owned by V Forge
- CI/CD runtime history
- source-control history as canonical Project V truth
- rich execution-progress models that make Project V behave like the receiving system

### Rule
If a proposed Project V table or field would naturally be queried to answer “what happened in VEDA?” or “what is happening in execution right now?”, it is probably out of bounds.

---

## Cross-System Persistence Rule

Project V must not treat another system's canonical database as an extension of its own persistence boundary.

Project V must not:

- write directly into VEDA canonical tables as a convenience shortcut
- write directly into V Forge canonical tables as a convenience shortcut
- normalize foreign-system state into local tables as though it were now owned by Project V
- create shadow copies that become the practical source of truth in Project V workflows

### Rule
Cross-system coordination must happen through explicit interfaces, explicit handoffs, or explicit references.
Not through silent persistence shortcuts.

---

## Imported vs Canonical vs Interpreted Distinction

Project V must preserve a clean distinction between:

### 1. Canonical data
Data Project V owns as planning and orchestration truth.

### 2. Imported data
Data brought into Project V for bounded convenience that remains non-canonical outside Project V's planning interpretation.

### 3. Interpreted data
Project V's own planning meaning derived from canonical or referenced inputs.

### Rule
These categories must not be silently collapsed.
An imported external record is not automatically canonical Project V truth.
A planning interpretation is not automatically ownership of the external record it references.
Project V may derive planning-side interpretations from imported material. The interpretation itself may be canonical Project V truth; the imported source material it was derived from remains non-canonical and must not be treated as having been promoted to canonical status by the act of interpretation.

---

## Thin External Linkage Rule

Project V may preserve thin external linkage for planning-side traceability and handoff clarity.

Thin linkage means the stored data is enough to answer bounded questions such as:

- what external record is this planning record linked to?
- what system owns that external record?
- why is the linkage relevant to planning, audit, readiness, or handoff?

Thin linkage does not mean:

- mirroring external execution state locally
- storing rich editorial or production metadata
- storing observability payloads as convenience state
- rebuilding another system's internal model inside Project V

### Rule
If linkage starts looking like a local execution or observability model, it has crossed the data boundary.

---

## Project Scope Rule

Data stored in Project V must preserve explicit project scope where the concept is project-scoped.

Project V must not:

- attach another project's external references casually
- accept cross-project convenience data without explicit governed handling
- let imported or referenced data weaken same-project planning integrity
- blur project ownership because an external system uses different identifiers

### Rule
If the project scope of a data element cannot be classified honestly, it is not safe enough to store as governed Project V data.

---

## Boundary Markers Rule

Any non-canonical external or imported material stored in Project V should carry enough markers to preserve boundary honesty.

Examples of relevant markers include:

- source type
- evidence type
- target system classification
- target locator or explicit external identifier
- notes clarifying the planning-side interpretation posture
- freshness, warning, or invalidation signals where material staleness matters

### Rule
Boundary markers must make it clear whether a stored thing is:

- owned planning truth
- a bounded reference
- imported convenience material
- planning-side interpretation of foreign truth

If a stored record cannot be classified clearly, its boundary posture is too ambiguous.

---

## Data Freshness and Staleness Rule

Project V may rely on external or imported material for planning.
It must not silently assume that persisted external context remains fresh forever.

When staleness materially undermines a planning, readiness, audit, or handoff claim, Project V should:

- surface a gap
- surface a warning
- mark planning-side confidence stale
- trigger reconsideration through governed paths

### Rule
Stale imported or referenced material is a planning-side problem.
It does not become safe merely because it is stored locally.

---

## JSON and Flexible Payload Rule

Project V may use JSON or flexible payload storage only where bounded variability is genuinely justified.

Examples may include:

- imported payload traces used for bounded support purposes
- bounded metadata with genuinely variable shape

### Rule
JSON must not become a hiding place for:

- unresolved ownership decisions
- out-of-bounds observability data
- out-of-bounds execution data
- convenience blobs that should have remained outside Project V

If a payload is important enough to govern, query, validate, or classify repeatedly, it likely needs explicit bounded schema or it should remain outside Project V.

---

## Boundary Failure Modes (Explicitly Forbidden)

The following are Project V data-boundary failures:

- storing canonical observability truth in Project V
- storing canonical execution truth in Project V
- treating imported convenience material as though it were foreign-system source of record
- storing rich execution linkage until it behaves like a shadow execution tracker
- storing observability payloads until Project V behaves like a second observatory
- silently collapsing canonical, imported, and interpreted data into one undifferentiated state blob
- using JSON to bypass schema and ownership discipline
- using cross-system database access as a substitute for explicit interfaces or references
- accepting ambiguous project-scoped data that weakens project-boundary integrity

---

## Human-In-The-Loop Principle

Data-boundary decisions are governance-sensitive because they determine what Project V is allowed to become.

Human review may be required where a proposed data shape would:

- broaden Project V ownership materially
- persist foreign-system data locally in new ways
- deepen execution-facing linkage
- deepen observability-shaped storage
- weaken project-scope integrity
- introduce new imported convenience patterns

---

## LLM Use Principle

A capable LLM should be able to infer from this doc that:

- Project V owns planning and orchestration data, not observability truth or execution truth
- references and interpretations are allowed, but ownership does not transfer
- imported convenience material must remain explicitly non-canonical outside Project V's planning interpretation
- thin linkage is allowed; shadow models are not
- staleness of imported or referenced material must be handled honestly
- JSON is not permission to evade data-boundary discipline

If Project V persistence starts to look like a blended planning-observability-execution blob, the doctrine is wrong.

---

## Usage

This document should be used:

- when deciding whether a category of data belongs in Project V at all
- when evaluating whether a proposed field, table, or payload is canonical, imported, interpreted, or out of bounds
- when reviewing cross-system reference and import behavior
- when rejecting convenience-driven ownership drift
- when writing subordinate schema, integration, and persistence docs that depend on data-boundary rules

---

## Related Docs

- `project-v.md`
- `system-invariants.md`
- `schema-authority.md`
- `implementation-traceability.md`
- `byda-in-project-v.md`
- `../interfaces/veda-to-project-v-signal-interface.md`
- `../interfaces/project-v-to-v-forge-handoff-interface.md`
- `../interfaces/v-forge-to-project-v-return-to-planning-interface.md`
- `../governance/decision-continuity-doctrine.md`
- `../governance/approval-and-escalation-model.md`
- `../ecosystem/cross-system-boundaries.md`
- `../ecosystem/vocabulary.md`
