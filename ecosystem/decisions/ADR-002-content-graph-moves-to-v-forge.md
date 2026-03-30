# ADR-002: Content Graph Moves to V Forge

## Status
Accepted

## Date
2026-03-29

## Context
The content graph — the structural model of what a project has built (pages, topics, entities, internal links, archetypes, schema usage) — was previously owned by VEDA. This created ownership tension. The content graph describes internal project structure, not observed external reality. It changes when V Forge does execution work. Having it in VEDA caused VEDA's database to change every time V Forge built something, creating hidden coupling between two systems meant to be independent.

Additionally, VEDA Brain was using the content graph to generate content gap proposals by crossing it against SERP signal. Once VEDA Brain was eliminated, the content graph had no natural home in VEDA.

## Decision
The content graph belongs to V Forge.

The content graph is execution truth — it describes what was built. It changes when V Forge does work. It belongs in the system that does execution.

V Forge owns: pages, topics, entities, internal links, archetypes, schema usage for all built projects.

VEDA does not own or maintain the content graph in any form.

## Consequences
- The content graph is removed from VEDA's schema, docs, and invariants
- V Forge's database contains the content graph
- V Forge's system invariants include content graph integrity rules
- V Forge can cross the content graph against VEDA signal through the governed VEDA-to-V-Forge signal interface to produce execution intelligence
- VEDA's schema becomes purely observatory — external signals only
- VEDA and V Forge are now more cleanly decoupled

## Related Docs
- `../../v-forge/v-forge.md`
- `../../v-forge/system-invariants.md`
- `../../veda/system-invariants.md`
- `../../interfaces/veda-to-v-forge-signal-interface.md`
- `ADR-001-veda-is-pure-observatory.md`
