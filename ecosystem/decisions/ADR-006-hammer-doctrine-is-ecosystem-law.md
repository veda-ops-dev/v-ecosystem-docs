# ADR-006: Hammer Doctrine Is Ecosystem-Wide Law

## Status
Accepted

## Date
2026-03-29

## Context
The hammer — an integration and invariant verification layer — was established in VEDA. It verifies that system invariants hold under real execution: routes stay read-only when they should, project isolation holds, contracts are deterministic, atomicity works correctly.

The question arose: is the hammer a VEDA-specific tool or a universal ecosystem requirement?

## Decision
The hammer doctrine is universal ecosystem law.

Every system in the V Ecosystem — Project V, VEDA, and V Forge — must implement its own hammer layer adapted to its own invariants and surfaces.

The principles are universal:
- Invariants first — verify structural truths, not implementation trivia
- Real execution over mock theater — exercise live routes and realistic state
- Exact contract beats vibes — assertions must be precise
- Route intent must remain visible — the hammer documents what the system actually does
- Boring structure wins — organize by concern, not file growth

The three required categories are universal:
- Persistence hammer — schema and migration integrity, atomicity
- Contract hammer — request validation, response shapes, deterministic ordering
- Boundary hammer — read-only posture, project isolation, cross-project violation probes

The specifics differ per system. The doctrine does not.

A failing hammer means a system is not safe for production. This is not optional.

## Consequences
- `governance/testing-and-verification-doctrine.md` is a Tier 1 ecosystem authority document
- Project V, V Forge, and VEDA each require their own hammer implementations
- Cross-project violation probes are required in every system's hammer — not optional
- Transaction rollback testing is required in every system's hammer — not optional
- The hammer is part of every new external provider integration
- A system without a passing hammer is not considered production-ready

## Related Docs
- `../../governance/testing-and-verification-doctrine.md`
- `../../veda/system-invariants.md`
- `../../project-v/system-invariants.md`
- `../../v-forge/system-invariants.md`
