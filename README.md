# V Ecosystem Docs

## Purpose

This repository is the **single source of truth** for the V Ecosystem.

It exists to:
- define system boundaries
- define governance rules
- define shared vocabulary
- define workflows and interfaces
- provide enough structured context for LLMs and engineers to operate without relying on tribal knowledge

---

## Authority Model

### Tier 1 — Core Authority
- `ecosystem/`
- `governance/`
- `interfaces/`
- `workflows/`

These define system-wide law and must not be bypassed.

### Tier 2 — System Authority
- `project-v/`
- `veda/`
- `v-forge/`

These define system-specific behavior within the ecosystem boundaries.

### Strategy Authority
- `strategy/`

Defines evaluation models, scoring systems, and long-term ecosystem direction.

### Tier 3 — Implementation Support
- `interfaces/*-implementation-design.md`
- `EXTENSION-CODING-README.md`

These support implementation but do not override Tier 1 or Tier 2 authority.

### Nerve (Runtime Support Layer)
- `nerve/`

Runtime implementation planning and reference layer.
Contains:
- runtime roadmap
- ambiguity checklists
- source-mapped reference material

Used during extension/runtime implementation work.

### Archive
- `archive/`

Historical material. Not active authority.

---

## Entry Points

Start here for orientation:

1. `ecosystem/v-ecosystem-overview.md`
2. `ecosystem/cross-system-boundaries.md`
3. `ecosystem/vocabulary.md`

Then load governance and system docs as needed.

---

## Rule

If something important is not documented here, it is not part of the governed system.
