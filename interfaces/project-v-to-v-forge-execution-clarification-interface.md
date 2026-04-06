# Project V to V Forge Execution Clarification Interface

## Purpose

This document defines the interface by which Project V provides bounded scope
clarification or additional execution guidance to V Forge during active execution,
without triggering full return-to-planning.

It exists to answer:

```text
How does Project V deliver a bounded clarification or constraint update to V Forge
during execution when the clarification does not require replanning, a new handoff,
or a transfer of planning ownership into V Forge?
```

This is a Tier 1 ecosystem authority document.

---

## Scope

This document governs:

- the meaning of a Project V to V Forge execution clarification
- when execution clarification is appropriate vs when return-to-planning is required
- what may cross through this interface and what may not
- the boundary posture that prevents clarification from becoming informal planning transfer

---

## Out of Scope

This document does not define:

- detailed transport or implementation format
- approval mechanics beyond the boundary note below
- field-level schemas
- Project V internal replanning workflow
- V Forge internal execution workflow

Those belong in workflow, governance, and implementation-specific docs.

---

## System

- interfaces

---

## Interface Direction

**Project V → V Forge**

Project V initiates. V Forge receives bounded clarification within the active
execution relationship.

---

## Governing Systems

- **Initiator:** Project V (planning truth owner)
- **Receiver:** V Forge (execution truth owner)

---

## Core Rule

An execution clarification delivers a bounded update from Project V to V Forge
to resolve a specific ambiguity, constraint, or scope question that arose during
execution — without requiring full return-to-planning, a new handoff, or any
transfer of planning authority into V Forge.

Execution clarification is not:

- a new handoff
- a scope expansion authorization
- a return-to-planning substitute
- a transfer of planning ownership into V Forge
- permission for V Forge to reinterpret planning intent beyond the bounded notice

If the clarification would change what planning should do next, require replanning,
or alter governing decisions, that is a return-to-planning event, not a clarification.

---

## Minimum Semantic Elements

A valid execution clarification must be interpretable as carrying at minimum:

- what active handoff or execution context the clarification applies to
- what specific question, ambiguity, or constraint is being clarified
- what the clarified scope, constraint, or guidance is
- that this clarification does not expand approved execution scope beyond what
  was already authorized
- what, if any, limits apply to how V Forge may act on this clarification

---

## Boundary and Ownership Rule

After a valid execution clarification:

- V Forge remains the owner of execution truth for the handed-off scope
- Project V remains the owner of planning and orchestration truth
- the clarification updates V Forge's execution context within the existing
  approved scope; it does not constitute a new approval or a new handoff
- V Forge must not treat a clarification as authorization to widen execution
  scope beyond the originally approved bounds

A clarification that would materially widen scope must be routed through the
original handoff approval path or a governed scope update, not through this interface.

---

## Activity Trail

Activity trail integration is required for this interface.

The exact canonical action type mapping and required fields will be defined in
the activity trail integration map (`../ecosystem/activity-trail-integration-map.md`)
once that document is completed.

This stub does not finalize the activity trail action vocabulary for this interface.
Implementations must not proceed without that mapping in place.

---

## Usage

This document should be used:

- when V Forge has raised a bounded question during execution that Project V
  must answer without triggering full return-to-planning
- when reviewing whether a proposed mid-execution communication should be
  routed through this interface or through return-to-planning
- when evaluating whether a clarification stays within existing approved scope

---

## Related Docs

- `project-v-to-v-forge-handoff-interface.md`
- `v-forge-to-project-v-return-to-planning-interface.md`
- `project-v-to-v-forge-scope-update-interface.md`
- `../project-v/v-forge-integration.md`
- `../ecosystem/cross-system-boundaries.md`
- `../governance/approval-and-escalation-model.md`
