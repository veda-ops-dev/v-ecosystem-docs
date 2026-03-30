# ADR-007: Docs Are the Build Spec — Database Owns Operational State

## Status
Accepted

## Date
2026-03-29

## Context
In early ecosystem sessions, the role of documentation versus the database was ambiguous. There was risk of docs being used to store operational state (project status, BYDA scores, session context) or of the database being used to store doctrine (rules, invariants, vocabulary). Both failure modes produce confusion for LLMs operating inside the ecosystem.

The question was: what is the fundamental split between what lives in docs and what lives in the database?

## Decision
Docs are the build spec. The database owns operational state. These are not interchangeable.

**Docs own:**
Everything that defines how the ecosystem works, what it is, and what it must be — system roles, boundaries, invariants, vocabulary, governance rules, interface contracts, workflow steps, methodology (BYDA, hammer), onboarding requirements, architecture decisions. Docs are written for an LLM to build the V Ecosystem correctly. They do not change session to session.

**The database owns:**
Everything that reflects the current state of the ecosystem and its projects as they actually exist and change over time — project status and lifecycle phase, BYDA audit scores and history, decision log entries, session context, VEDA observatory records, content graph records, execution records, handoff records, event logs, approval records.

**The build spec principle:**
The docs are strong enough when — if the code disappeared — a capable LLM could rebuild the V Ecosystem correctly from the docs alone without relying on hidden tribal knowledge.

**The database completeness principle:**
The database is complete enough when a capable LLM can answer "where are we with this project" from a database query without asking the human operator to re-explain current state.

## Consequences
- Docs must never contain project-specific BYDA scores, phase indicators, or session history
- The database must capture enough operational state that session re-orientation does not require human re-explanation
- LLMs must be oriented to load docs for doctrine and query the database for current state — never the reverse
- `ecosystem/doctrine-vs-operational-state.md` is a Tier 1 ecosystem authority document
- This split is a primary design requirement for every database schema built in the ecosystem

## Related Docs
- `../../ecosystem/doctrine-vs-operational-state.md`
- `../../ecosystem/db-posture.md`
- `../../interfaces/mcp-coordination-model.md`
