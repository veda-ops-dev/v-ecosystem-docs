# ADR-003: VEDA Brain Is Eliminated

## Status
Accepted

## Date
2026-03-29

## Context
VEDA Brain was an intelligence synthesis layer inside VEDA that generated planning proposals and content gap analysis by crossing the content graph against SERP and search performance signal. It created role tension by making VEDA act as a planner and analyst rather than a pure observatory. With the decision that VEDA is a pure observatory (ADR-001) and the content graph moves to V Forge (ADR-002), VEDA Brain has no architectural home.

Options considered:
1. Move VEDA Brain to Project V
2. Move VEDA Brain to V Forge
3. Keep VEDA Brain in VEDA but strip it to a pure signal aggregator
4. Eliminate VEDA Brain entirely and split its capabilities to the appropriate systems

## Decision
VEDA Brain does not exist in the new V Ecosystem build.

It is not moved. It is not redefined. It is not stripped down. It simply does not exist.

The intelligence it was providing splits cleanly to where it belongs:

- Pre-build market opportunity analysis belongs to Project V's planning intelligence layer. Project V reads VEDA market signal and synthesizes it into planning-relevant inputs — what opportunities exist, what the market shows, what is worth pursuing.

- Post-build content performance gap analysis belongs to V Forge's execution intelligence layer. V Forge owns the content graph and crosses it against VEDA's performance signal to answer: how is what we built performing and where are the gaps.

VEDA provides clean signal to both. It does not synthesize, propose, or cross-reference. Other systems do that using what VEDA provides.

Option 3 (strip VEDA Brain to an aggregator) was rejected because it preserved the concept under a different name. Starting fresh, the concept has no role in a pure observatory.

## Consequences
- No VEDA Brain in the new build — no code, no docs, no reference to it in active docs
- Project V gains a planning intelligence layer responsible for pre-build market synthesis
- V Forge gains an execution intelligence layer responsible for post-build performance gap analysis
- VEDA's role becomes more precise and easier to implement correctly
- The term "VEDA Brain" must not reappear in active ecosystem docs — it is an eliminated concept

## Related Docs
- `../../veda/veda.md`
- `../../veda/system-invariants.md`
- `../../v-forge/v-forge.md`
- `../../project-v/project-v.md`
- `ADR-001-veda-is-pure-observatory.md`
- `ADR-002-content-graph-moves-to-v-forge.md`
