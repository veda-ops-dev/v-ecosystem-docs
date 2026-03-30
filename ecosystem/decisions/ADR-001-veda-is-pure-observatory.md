# ADR-001: VEDA Is a Pure Observatory

## Status
Accepted

## Date
2026-03-29

## Context
Early VEDA implementation included VEDA Brain — an intelligence synthesis layer that crossed content graph data against SERP signal to generate planning proposals and content gap analysis. This caused role tension inside VEDA. VEDA was drifting from observing external reality into interpreting what operators should build next, which is a planning and execution function, not an observatory function.

The question arose: should VEDA continue to own intelligence synthesis, or should that responsibility be split to the systems that own the decisions being informed?

## Decision
VEDA is a pure observatory.

VEDA observes external reality — search behavior, performance signals, market conditions, platform activity — and records what it sees with timestamps, provenance, and fidelity.

VEDA does not interpret, propose, plan, or execute on behalf of the ecosystem.

The telescope mental model governs VEDA's role: a telescope does not measure planetary distance. It observes. Measurement and interpretation happen elsewhere. VEDA is the telescope.

If a proposed VEDA capability cannot be described as something a telescope does, it does not belong in VEDA.

## Consequences
- VEDA Brain is eliminated entirely from the new build
- Intelligence synthesis splits cleanly: pre-build market opportunity analysis goes to Project V's planning intelligence layer; post-build content performance gap analysis goes to V Forge's execution intelligence layer
- VEDA's role becomes unambiguous and easier to govern
- VEDA's database contains only observatory truth — external signals, not internal project structure
- VEDA scope creep becomes easier to detect and reject

## Related Docs
- `../../veda/veda.md`
- `../../veda/system-invariants.md`
- `../../veda/observability-and-signal-role.md`
- `../../ecosystem/vocabulary.md`
- `ADR-002-content-graph-moves-to-v-forge.md`
- `ADR-003-veda-brain-eliminated.md`
